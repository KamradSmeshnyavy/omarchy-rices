#!/usr/bin/python3
"""omarchy-modern-colors — цвета райса Modern отдельно от обоев, как его Settings → Themes (github.com/elifouts/Dotfiles,
GPL-3.0: Modern/settings/Themes.qml, utilities/colors/color-apply.sh): «Pywal» — 16 цветов pywal16 по текущим обоям, или
одна из его схем (../crt/schemes без трубок), и акцент — один из 16 слотов. Сборка — тема modern-live
(~/.config/omarchy/themes/modern-live, руками не править) с текущими обоями как есть. Состояние —
~/.local/state/omarchy/modern-live.json. Общая часть (схемы, pywal, квантование) — ../crt/colors.py.

  omarchy-modern-colors --list               плитки: id, имя, 16 цветов, слот, текущая (JSON)
  omarchy-modern-colors <id> [слот]          сменить цвета (обои остаются)
  omarchy-modern-colors --wallpaper <файл>   сменить обои (при цветах pywal — ещё и перекрасить), печатает путь
  omarchy-modern-colors --state <файл.json>  собрать из сохранённого состояния (профили панели настроек)
  omarchy-modern-colors --dump               текущее состояние (JSON)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.realpath(__file__))


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


cc = _load("crt_colors", os.path.join(HERE, "..", "crt", "colors.py"))
mb = _load("modern_build", os.path.join(HERE, "build.py"))

NAME = "modern-live"
THEMES = os.path.expanduser("~/.config/omarchy/themes")
TARGET = os.path.join(THEMES, NAME)
MARKER = ".modern-live.json"
STATE = os.path.expanduser("~/.local/state/omarchy/modern-live.json")
CURRENT_NAME = os.path.expanduser("~/.local/state/omarchy/current/theme.name")
CURRENT_BG = os.path.expanduser("~/.local/state/omarchy/current/background")
PROFILE = {"default": ("pywal", 9), "sun": ("pywal", 9), "neon": ("pywal", 9), "zen": ("pywal", 9), "gruvbox": ("gruvbox", 9)}


def die(msg):
    print(f"omarchy-modern-colors: {msg}", file=sys.stderr)
    sys.exit(1)


def schemes():
    return [x for x in cc.schemes() if x[0] not in cc.TUBES]


def source_of(path):
    real = os.path.realpath(path)
    try:
        bg = os.path.dirname(real)
        src = json.load(open(os.path.join(os.path.dirname(bg), "source.json"))).get(os.path.basename(real))
        if src:
            p = os.path.join(os.path.dirname(bg), src)
            return os.path.realpath(p)
    except (OSError, ValueError):
        pass
    return real


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


def scheme_of(cid, src):
    if cid == "pywal":
        t = cc.wal_palette(src)
        if t:
            return t
        return mb.VARIANTS["default"]["tube"]
    for sid, _, s in schemes():
        if sid == cid:
            return s
    die(f"нет цветов {cid}")


def current():
    try:
        return open(CURRENT_NAME).read().strip()
    except OSError:
        return ""


def fresh_state():
    s = load_state()
    s["source"] = source_of(CURRENT_BG)
    cur = current()
    if cur != NAME and cur.startswith("modern-") and cur[7:] in PROFILE:
        cid, slot = PROFILE[cur[7:]]
        s["colors"] = cid
        s.setdefault("slots", {})[cid] = slot
    s.setdefault("colors", "pywal")
    return s


def build(state):
    src = state.get("source") or source_of(CURRENT_BG)
    if not os.path.isfile(src):
        die(f"нет исходника обоев: {src}")
    cid = state.get("colors") or "pywal"
    slot = int((state.get("slots") or {}).get(cid, 9))
    tube = scheme_of(cid, src)
    title = "Modern · " + ("Pywal" if cid == "pywal" else next((n for i, n, _ in schemes() if i == cid), cid))
    mb.VARIANTS["live"] = {"title": title, "tube": tube, "acc": slot}
    if os.path.islink(TARGET) or (os.path.exists(TARGET) and not os.path.exists(os.path.join(TARGET, MARKER))):
        die(f"{TARGET} создан не этим скриптом — не трогаю")
    os.makedirs(THEMES, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix=f".{NAME}-", dir=THEMES)
    try:
        os.chmod(tmp, 0o755)
        mb.make("live", tmp, NAME)
        bg = os.path.join(tmp, "backgrounds")
        os.makedirs(bg, exist_ok=True)
        tag = hashlib.md5(json.dumps([src, cid, slot]).encode()).hexdigest()[:8]
        stem = f"0-live-{tag}{os.path.splitext(src)[1]}"
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
    return os.path.join(TARGET, "backgrounds", stem)


def apply(image):
    env = dict(os.environ, OMARCHY_THEME_SKIP_BACKGROUND="1")
    if current() == NAME:
        env["OMARCHY_DYNAMIC_RECOLOR"] = "1"
    subprocess.run(["omarchy-theme-set", NAME], check=True, env=env)
    subprocess.run(["omarchy-theme-bg-set", image], check=False)


def listing():
    s = fresh_state() if current().startswith("modern-") else load_state()
    active = s.get("colors") if current().startswith("modern-") else ""
    src = source_of(CURRENT_BG)
    out = []
    w = scheme_of("pywal", src) if os.path.isfile(src) else None
    for sid, name, sc in [("pywal", "Pywal", w)] + schemes():
        cols = [sc["colors"][f"color{i}"] for i in range(16)] if sc else []
        out.append({"id": sid, "name": name, "colors": cols, "slot": int((s.get("slots") or {}).get(sid, 9)),
                    "on": sid == active, "tube": False})
    return out


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "--list":
        print(json.dumps(listing(), ensure_ascii=False))
    elif a[0] == "--dump":
        print(json.dumps(fresh_state(), ensure_ascii=False))
    elif a[0] == "--state":
        st = json.load(open(a[1]))
        apply(build(st.get("modernState", st)))
    elif a[0] == "--wallpaper":
        s = fresh_state()
        s["source"] = os.path.realpath(a[1])
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
