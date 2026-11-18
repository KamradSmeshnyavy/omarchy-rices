#!/usr/bin/python3
"""omarchy-crt-colors — цвета райса Retro CRT отдельно от обоев и экрана, как его COLORS (github.com/elifouts/Dotfiles,
GPL-3.0: Retro/settings/Settings.qml → colors, utilities/colors/color-apply.sh, color-roles.sh, Retro/base/wallpaper.sh).

Цвета — трубка (phosphor / amber / cyan / paper), одна из его схем (schemes/*.json — его colorschemes/dark как есть) или
wallpaper — pywal16 по текущим обоям (`wal -i … --cols16`, как у него). Акцент — один из 16 цветов (у него — 12 полосок:
слоты 9–14 и 1–6). Сборка — тема crt-live (~/.config/omarchy/themes/crt-live, руками не править): палитра + ручки
экрана и фильтра, перенесённые из текущей темы, и текущие обои, заново прогнанные фильтром в новые цвета.
Состояние — ~/.local/state/omarchy/crt-live.json (цвета, слот по каждой схеме, исходник обоев, ручки, фильтр).

  omarchy-crt-colors --list                 плитки для COLORS: id, имя, 16 цветов, слот, текущая (JSON)
  omarchy-crt-colors <id> [слот]            сменить цвета (обои остаются, перефильтровываются)
  omarchy-crt-colors --wallpaper <картинка> сменить обои (при цветах wallpaper — ещё и перекрасить), печатает путь
  omarchy-crt-colors --state <файл.json>    собрать из сохранённого состояния (профили панели настроек)
  omarchy-crt-colors --dump                 текущее состояние (JSON) — для «save as»
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
import importlib.util  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


cb = _load("crt_build", "build.py")
cf = _load("crt_filter", "filter.py")
cs = _load("crt_shader", "shader.py")

NAME = "crt-live"
THEMES = os.path.expanduser("~/.config/omarchy/themes")
TARGET = os.path.join(THEMES, NAME)
MARKER = ".crt-live.json"
STATE = os.path.expanduser("~/.local/state/omarchy/crt-live.json")
CURRENT_NAME = os.path.expanduser("~/.local/state/omarchy/current/theme.name")
CURRENT_BG = os.path.expanduser("~/.local/state/omarchy/current/background")
PALS = os.path.expanduser("~/.cache/omarchy/crt-walls/palettes.json")
TUBES = ["phosphor", "amber", "cyan", "paper"]
SLOTS = [9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6]


def die(msg):
    print(f"omarchy-crt-colors: {msg}", file=sys.stderr)
    sys.exit(1)


def schemes():
    """[(id, имя, схема)] — трубки, потом его схемы по имени файла."""
    out = []
    d = os.path.join(HERE, "schemes")
    files = sorted(f[:-5] for f in os.listdir(d) if f.endswith(".json"))
    for sid in TUBES + [f for f in files if f not in TUBES]:
        s = json.load(open(os.path.join(d, sid + ".json")))
        name = s.get("name") or sid
        out.append((sid, name, {"special": {k: v.lower() for k, v in s["special"].items()},
                                "colors": {k: v.lower() for k, v in s["colors"].items()}}))
    return out


def load_state():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE + ".tmp", "w") as f:
        json.dump(s, f, indent=1)
    os.replace(STATE + ".tmp", STATE)


def wal_palette(src):
    """pywal по картинке (кэш — общий с библиотекой), как у него color-apply.sh: wal -i … --cols16."""
    try:
        st = os.stat(src)
    except OSError:
        return None
    key = hashlib.sha1(f"{os.path.realpath(src)}:{st.st_mtime_ns}:{st.st_size}".encode()).hexdigest()
    try:
        pals = json.load(open(PALS))
    except (OSError, ValueError):
        pals = {}
    c = pals.get(key)
    if not c:
        t = cb.pywal(src)
        if not t:
            return None
        c = [t["colors"][f"color{i}"] for i in range(16)]
        pals[key] = c
        os.makedirs(os.path.dirname(PALS), exist_ok=True)
        with open(PALS + ".tmp", "w") as f:
            json.dump(pals, f)
        os.replace(PALS + ".tmp", PALS)
    return {"special": {"background": c[0], "foreground": c[15], "cursor": c[15]},
            "colors": {f"color{i}": c[i] for i in range(16)}}


def scheme_of(cid, src):
    if cid == "wallpaper":
        t = wal_palette(src)
        if t:
            return t
        # без pywal — трубка, повёрнутая к оттенку картинки (как dynamic без pywal)
        import colorsys
        r = subprocess.run(["magick", src + "[0]", "-resize", "1x1!", "-format", "%[hex:p{0,0}]", "info:"],
                           capture_output=True, text=True)
        hx = "#" + (r.stdout.strip()[:6] or "33ff66")
        h = colorsys.rgb_to_hls(*(int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)))[0]
        return cb.tinted(h)
    for sid, _, s in schemes():
        if sid == cid:
            return s
    die(f"нет цветов {cid} (есть: wallpaper, {', '.join(x[0] for x in schemes())})")


def current_knobs():
    """Ручки экрана и фильтра, что сейчас на экране (тема + свои), — переносятся в новые цвета."""
    try:
        f = cf.settings(cf.CURRENT)
    except Exception:  # noqa: BLE001
        f = dict(cf.DEFAULTS, on=False)
    return cs.knobs(), f


def build(state):
    src = state.get("source") or cf.source_of(CURRENT_BG)
    if not os.path.isfile(src):
        die(f"нет исходника обоев: {src}")
    cid = state.get("colors") or "phosphor"
    slot = int((state.get("slots") or {}).get(cid, state.get("slot", 9)))
    tube = scheme_of(cid, src)
    crt, flt = state.get("crt") or cs.DEFAULTS, dict(state.get("filter") or {})
    title = "Retro CRT · " + ("Wallpaper" if cid == "wallpaper" else next((n for i, n, _ in schemes() if i == cid), cid))
    cb.VARIANTS["live"] = {"title": title, "tube": tube, "acc": slot, "crt": crt, "filter": flt}
    if os.path.islink(TARGET) or (os.path.exists(TARGET) and not os.path.exists(os.path.join(TARGET, MARKER))):
        die(f"{TARGET} создан не этим скриптом — не трогаю")
    os.makedirs(THEMES, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix=f".{NAME}-", dir=THEMES)
    try:
        os.chmod(tmp, 0o755)
        cb.make("live", tmp, NAME)
        # tube.json: «on» фильтра — из состояния (make пишет on = есть ли у варианта картинка)
        tj = os.path.join(tmp, "tube.json")
        t = json.load(open(tj))
        t["filter"] = dict(flt)
        t["colors_id"], t["slot"] = cid, slot
        with open(tj, "w") as f:
            json.dump(t, f, indent=1)
        bg = os.path.join(tmp, "backgrounds")
        os.makedirs(bg, exist_ok=True)
        o = dict(cf.DEFAULTS, **{k: v for k, v in flt.items() if k in cf.DEFAULTS}, on=bool(flt.get("on")))
        tag = hashlib.md5(json.dumps([src, cid, slot, o], sort_keys=True).encode()).hexdigest()[:8]
        ext = ".png" if o["on"] else os.path.splitext(src)[1]
        stem = f"0-live-{tag}{ext}"
        if o["on"]:
            cf.render(src, os.path.join(bg, stem), cf.theme_colors(tmp), o)
        else:
            shutil.copyfile(src, os.path.join(bg, stem))
        with open(os.path.join(tmp, "source.json"), "w") as f:
            json.dump({stem: os.path.realpath(src)}, f)
        info = {"colors": cid, "slot": slot, "source": os.path.realpath(src), "title": title}
        for n in (MARKER, "live.json"):
            with open(os.path.join(tmp, n), "w") as f:
                json.dump(info, f, ensure_ascii=False)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    old = None
    if os.path.exists(TARGET):
        old = TARGET + f".old-{os.getpid()}"
        os.rename(TARGET, old)
    os.rename(tmp, TARGET)
    if old:
        shutil.rmtree(old)
    state = dict(state, source=os.path.realpath(src), colors=cid, slot=slot)
    state.setdefault("slots", {})[cid] = slot
    save_state(state)
    # свои ручки темы crt-live уже внутри неё — снять старые переопределения
    u = cs.load()
    if (u.get("themes") or {}).pop(NAME, None) is not None:
        with open(cs.SETTINGS + ".tmp", "w") as f:
            json.dump(u, f, indent=1)
        os.replace(cs.SETTINGS + ".tmp", cs.SETTINGS)
    return os.path.join(TARGET, "backgrounds", stem)


def apply(image):
    env = dict(os.environ, OMARCHY_THEME_SKIP_BACKGROUND="1")
    try:
        if open(CURRENT_NAME).read().strip() == NAME:
            env["OMARCHY_DYNAMIC_RECOLOR"] = "1"
    except OSError:
        pass
    subprocess.run(["omarchy-theme-set", NAME], check=True, env=env)
    subprocess.run(["omarchy-theme-bg-set", image], check=False)


def fresh_state():
    """Состояние из того, что на экране: цвета и слот — из текущей темы crt-*, ручки и фильтр — действующие."""
    s = load_state()
    crt, flt = current_knobs()
    s["crt"], s["filter"] = crt, {k: v for k, v in flt.items()}
    s["source"] = cf.source_of(CURRENT_BG)
    try:
        cur = open(CURRENT_NAME).read().strip()
    except OSError:
        cur = ""
    # тема-профиль (crt-car …): его цвета этого профиля — схема и слот, у pywal-профилей — wallpaper
    prof = {"car": ("gruvbox", 6), "windows": ("github-dark-dimmed", 7), "arcade": ("wallpaper", 9),
            "wallpaper": ("wallpaper", 9), "zen": ("wallpaper", 9), **{t: (t, 9) for t in TUBES}}
    if cur != NAME and cur.startswith("crt-") and cur[4:] in prof:
        cid, slot = prof[cur[4:]]
        s["colors"] = cid
        s.setdefault("slots", {})[cid] = slot
    s.setdefault("colors", "phosphor")
    return s


def listing():
    s = load_state()
    try:
        cur = open(CURRENT_NAME).read().strip()
    except OSError:
        cur = ""
    active = s.get("colors") if cur == NAME else fresh_state().get("colors") if cur.startswith("crt-") else ""
    src = cf.source_of(CURRENT_BG)
    out = []
    w = scheme_of("wallpaper", src) if os.path.isfile(src) else None
    items = [("wallpaper", "Wallpaper", w)] + schemes()
    for sid, name, sc in items:
        cols = [sc["colors"][f"color{i}"] for i in range(16)] if sc else []
        out.append({"id": sid, "name": name, "colors": cols, "slot": int((s.get("slots") or {}).get(sid, 9)),
                    "on": sid == active, "tube": sid in TUBES})
    return out


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "--list":
        print(json.dumps(listing(), ensure_ascii=False))
    elif a[0] == "--dump":
        print(json.dumps(fresh_state(), ensure_ascii=False))  # с действующими ручками и фильтром
    elif a[0] == "--state":
        st = json.load(open(a[1]))
        apply(build(st.get("crtState", st)))  # файл пресета профиля (crtState внутри) или само состояние
    elif a[0] == "--wallpaper":
        s = fresh_state()
        s["source"] = os.path.realpath(a[1])
        # у него обои всегда проходят фильтр (выключен — чёрный экран); у нас выключенный фильтр — картинка как есть
        img = build(s)
        apply(img)
        print(img)
    else:
        s = fresh_state()
        s["colors"] = a[0]
        if len(a) > 1:
            s.setdefault("slots", {})[a[0]] = int(a[1])
        apply(build(s))


if __name__ == "__main__":
    main()
