#!/usr/bin/env python3
"""Темы crt-* — по мотивам стиля Retro из github.com/elifouts/Dotfiles (GPL-3.0, Eli Fouts): старый зелёный терминал,
весь экран — через ЭЛТ-шейдер, обои прорисованы или задизерены в цвет трубки.

Цвета — ровно его wal-схемы трубок (.config/wal/colorschemes/dark/{phosphor,amber,cyan,paper}.json): фон чёрный,
текст color7, акцент — color9 (его color-roles accent по умолчанию 9). 16 цветов терминала — как у него. Схема лежит
в теме файлом tube.json — по нему фильтр обоев (filter.py) и шейдер (shader.py) берут цвет трубки.
Окна как у него (Retro/base/style.lua): рамка 1 px акцентом, у неактивных — акцент …33, без скруглений, без размытия,
тени и свечения.

Обои: 0-black.png — его обои по умолчанию (фильтр выключен — просто чёрный экран, на нём живёт терминал); 0r-* — его
обои из wallpapers/library, прогнанные через фильтр в цвет трубки (картинки — чужой арт: в git их нет, скачиваются
при сборке).

  python3 build.py              все варианты
  python3 build.py amber cyan   выбранные
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nothing"))
sys.path.insert(0, os.path.join(HERE, ".."))
import build as nb  # noqa: E402
import originals  # noqa: E402
from palettes import contrast  # noqa: E402

# его wal-схемы трубок
TUBES = {
    "phosphor": {"special": {"background": "#000000", "foreground": "#5ae27c", "cursor": "#a8fabc"}, "colors": {
        "color0": "#000000", "color1": "#14cb0b", "color2": "#00c230", "color3": "#0ce96b", "color4": "#1a9364",
        "color5": "#14b820", "color6": "#16ca79", "color7": "#5ae27c", "color8": "#194d26", "color9": "#1aff53",
        "color10": "#00ff03", "color11": "#52ff9c", "color12": "#19e696", "color13": "#34f441", "color14": "#47f5a7",
        "color15": "#a8fabc"}},
    "amber": {"special": {"background": "#000000", "foreground": "#e2b05a", "cursor": "#fadca8"}, "colors": {
        "color0": "#000000", "color1": "#cb4a0b", "color2": "#c27a00", "color3": "#e9bf0c", "color4": "#93921a",
        "color5": "#b85e14", "color6": "#cabd16", "color7": "#e2b05a", "color8": "#4d3a19", "color9": "#ffaa1a",
        "color10": "#ff6300", "color11": "#ffde52", "color12": "#e6e319", "color13": "#f48a34", "color14": "#f5e947",
        "color15": "#fadca8"}},
    "cyan": {"special": {"background": "#000000", "foreground": "#5ae2e2", "cursor": "#a8fafa"}, "colors": {
        "color0": "#000000", "color1": "#0bcb92", "color2": "#00c2c2", "color3": "#0cc1e9", "color4": "#1a6893",
        "color5": "#14b89a", "color6": "#1694ca", "color7": "#5ae2e2", "color8": "#194d4d", "color9": "#1affff",
        "color10": "#00ffc2", "color11": "#52e0ff", "color12": "#199ce6", "color13": "#34f4d2", "color14": "#47c1f5",
        "color15": "#a8fafa"}},
    "paper": {"special": {"background": "#000000", "foreground": "#c9c7b8", "cursor": "#d6d6cc"}, "colors": {
        "color0": "#000000", "color1": "#776f60", "color2": "#6d6c55", "color3": "#84886d", "color4": "#595e4f",
        "color5": "#706b5c", "color6": "#757b65", "color7": "#c9c7b8", "color8": "#4a4940", "color9": "#f0eee0",
        "color10": "#dcdac9", "color11": "#b0b39e", "color12": "#848c73", "color13": "#9f9a88", "color14": "#a3a994",
        "color15": "#ffffff"}},
}
# его схемы под профили (colorschemes/dark/gruvbox.json, github-dark-dimmed.json) и pywal-палитры его обоев:
# у профилей с colors.theme = pywal он делает `wal -i <обои> -n --cols16` по исходной картинке — палитры ниже посчитаны
# тем же pywal16 3.8 по тем же картинкам (elifouts/wallpapers), чтобы сборке не нужен был сам pywal
def _scheme(bg, fg, cur, *c):
    return {"special": {"background": bg, "foreground": fg, "cursor": cur},
            "colors": {f"color{i}": x.lower() for i, x in enumerate(c)}}


TUBES.update({
    "gruvbox": _scheme("#282828", "#ebdbb2", "#ebdbb2", "#282828", "#fb4934", "#b8bb26", "#fabd2f", "#83a598", "#d3869b",
                       "#8ec07c", "#ebdbb2", "#928374", "#fe8019", "#b8bb26", "#fabd2f", "#83a598", "#d3869b", "#8ec07c",
                       "#fbf1c7"),
    "github-dark-dimmed": _scheme("#22272e", "#adbac7", "#adbac7", "#22272e", "#f47067", "#57ab5a", "#c69026", "#539bf5",
                                  "#b083f0", "#76e3ea", "#909dab", "#2d333b", "#ff938a", "#6bc46d", "#daaa3f", "#6cb6ff",
                                  "#dcbdfb", "#b3f0ff", "#909dab"),
    "wal-cat-08": _scheme("#0c0e1d", "#c2c2c6", "#c2c2c6", "#0c0e1d", "#3d404e", "#484b5a", "#535768", "#635b63", "#5c6377",
                          "#646f84", "#8f919a", "#5c5e70", "#525669", "#616579", "#6F758B", "#857A84", "#7B859F",
                          "#8694B1", "#c2c2c6"),
    "wal-cat-10": _scheme("#0f0f23", "#c3c3c8", "#c3c3c8", "#0f0f23", "#50566c", "#7e5766", "#5a637e", "#776e85", "#a56d7e",
                          "#6e7b9d", "#92929c", "#5e5e74", "#6B7390", "#A87489", "#7985A9", "#9F93B2", "#DD92A9",
                          "#93A5D2", "#c3c3c8"),
    "wal-ind-06": _scheme("#0e1a20", "#c2c5c7", "#c2c5c7", "#0e1a20", "#534d47", "#67372a", "#665850", "#5d605f", "#6b635c",
                          "#92604b", "#90979b", "#5d6b72", "#6F675F", "#8A4A39", "#88766B", "#7D807F", "#8F847B",
                          "#C38065", "#c2c5c7"),
})

# варианты: трубки — его профиль по умолчанию (Retro/tweaks/default-look.json: фильтр выключен — чёрный экран) с
# трубкой из его COLORS; остальные — его сохранённые профили (Retro/tweaks/saved/desktop/*.json) как есть: палитра,
# обои через фильтр с его настройками и ручки ЭЛТ-шейдера. crt / filter — в tube.json (их читают shader.py и filter.py).
CRT_DEFAULT = {"bend": 1, "corners": 0.65, "glow": 0.5, "grain": 0.25, "lines": 0.35, "mono": 0.5, "vignette": 0}
VARIANTS = {
    "phosphor": {"title": "Retro CRT Phosphor", "tube": "phosphor", "crt": CRT_DEFAULT},
    "amber": {"title": "Retro CRT Amber", "tube": "amber", "crt": CRT_DEFAULT},
    "cyan": {"title": "Retro CRT Cyan", "tube": "cyan", "crt": CRT_DEFAULT},
    "paper": {"title": "Retro CRT Paper", "tube": "paper", "crt": CRT_DEFAULT},
    # акцент Car — бирюзовый color6 (клетка стола на его retro/wall-car.jpg: #8ec07c под шейдером), Windows — color7
    "car": {"title": "Retro CRT Car", "tube": "gruvbox", "wall": "car-03", "acc": 6,
            "crt": {"bend": 0.2, "corners": 0.7, "glow": 1.5, "grain": 0.3, "lines": 0.9, "mono": 0.3, "vignette": 0.6},
            "filter": {"bright": 0.5, "contrast": 0.8, "levels": 12, "pixel": 1, "tone": "lines"}},
    "arcade": {"title": "Retro CRT Arcade", "tube": "wal-cat-08", "wall": "cat-08",
               "crt": {"bend": 1, "corners": 0.55, "glow": 1.5, "grain": 1, "lines": 0.1, "mono": 0, "vignette": 0.2},
               "filter": {"bright": 0.35, "contrast": 0.8, "dither": "bayer", "levels": 5, "pixel": 4, "tone": "palette"}},
    "wallpaper": {"title": "Retro CRT Wallpaper", "tube": "wal-cat-10", "wall": "cat-10",
                  "crt": {"bend": 1, "corners": 0.25, "glow": 1.05, "grain": 0.3, "lines": 0.25, "mono": 0.3, "vignette": 0.05},
                  "filter": {"dither": "fine", "pixel": 2, "tone": "source"}},
    "windows": {"title": "Retro CRT Windows", "tube": "github-dark-dimmed", "wall": "oth-03", "acc": 7,
                "crt": {"bend": 0, "corners": 0, "glow": 0.7, "grain": 0, "lines": 0.25, "mono": 0, "vignette": 0.6},
                "filter": {"bright": 0.5, "contrast": 0.8, "levels": 12, "pixel": 1, "tone": "source"}},
    "zen": {"title": "Retro CRT Zen", "tube": "wal-ind-06", "wall": "ind-06",
            "crt": {"bend": 1, "corners": 0, "glow": 1.5, "grain": 0, "lines": 0, "mono": 0, "vignette": 0.2},
            "filter": {"bright": 0.4, "contrast": 0.75, "dither": "bayer", "levels": 5, "pixel": 6, "tone": "palette"}},
}
for _v in VARIANTS.values():
    _v["tube"] = TUBES[_v["tube"]]
ACCENT = 9  # его state/color-roles.json: accent 9

# его обои — полная библиотека elifouts/wallpapers (без лицензии: в git их нет, скачиваются при сборке)
REPO, BRANCH = "elifouts/wallpapers", "main"
LIBRARY = {"car-03": "cars/car-03.jpg", "cat-08": "catppuccin/cat-08.jpg", "cat-10": "catppuccin/cat-10.png",
           "oth-03": "other/oth-03.jpg", "ind-06": "industrial/ind-06.jpg", "ind-01": "industrial/ind-01.jpg"}


def readable(c, bg, need):
    for _ in range(40):
        if contrast(c, bg) >= need:
            break
        c = nb.mix(c, "#ffffff", 0.06)
    return c


def palette(v):
    t = VARIANTS[v]
    tube = t["tube"]
    col, sp = tube["colors"], tube["special"]
    a = [col[f"color{i}"] for i in range(16)]
    bg, fg = sp["background"], sp["foreground"]
    acc = t.get("accent") or a[t.get("acc", ACCENT)]
    dim = readable(a[8], bg, 4.5)
    p = {
        "mode": "dark", "title": t["title"], "name": f"crt-{v}", "out": os.path.join(HERE, v),
        "bg": bg, "panel": nb.mix(bg, acc, 0.06), "raised": nb.mix(bg, acc, 0.1), "line": nb.mix(bg, acc, 0.3),
        "fg": fg, "dim": dim, "comment": readable(a[8], bg, 3),
        "accent": acc, "on_accent": bg, "selection": nb.mix(bg, acc, 0.3),
        # трубка одноцветная: роли — оттенки трубки, как у него в терминале
        "error": a[1], "info": a[4], "warn": a[3], "hint": dim, "ok": a[2],
        "diff_add": nb.mix(bg, a[2], 0.3), "diff_del": nb.mix(bg, a[1], 0.3), "diff_change": nb.mix(bg, a[4], 0.25),
        "keyword": a[13], "string": a[2], "number": a[11], "type": a[6], "function": a[12],
        "property": nb.mix(fg, a[8], 0.3), "special": acc, "constant": a[11], "ansi_yellow": a[3],
        "min_de": 0, "ansi16": a,
    }
    # все роли, что проверяет nothing/palettes.check, — не ниже 4.5 к фону (комментарии — 3): палитры pywal бывают тусклыми
    from palettes import SYNTAX
    for role in set(SYNTAX) | {"fg", "dim", "error", "info", "warn", "ok", "special", "ansi_yellow"}:
        p[role] = readable(p[role], bg, 4.5)
    p["comment"] = readable(p["comment"], bg, 3)
    p["wallpapers"] = lambda pp, d, v=v: walls(v, d)
    return p


def walls(v, out_dir):
    """Обои варианта: у профиля — его картинка через фильтр с его настройками (0-original.png, главная); у трубок —
    чёрный экран (его профиль по умолчанию, фильтр выключен), плюс его картинки профилей контурами в цвет трубки."""
    os.makedirs(out_dir, exist_ok=True)
    t = VARIANTS[v]
    theme = os.path.dirname(out_dir)
    jobs = []
    if t.get("wall"):
        jobs.append(("0-original", t["wall"], t.get("filter") or {}))
    else:
        black = os.path.join(out_dir, "0-black.png")
        if not os.path.exists(black):
            from PIL import Image
            Image.new("RGB", (64, 64), t["tube"]["special"]["background"]).save(black)
        jobs += [("0r-" + k, k, {"tone": "lines", "pixel": 1, "levels": 12, "contrast": 0.8, "bright": 0.5})
                 for k in ("car-03", "ind-01")]
    for stem, key, opts in jobs:
        dst = os.path.join(out_dir, stem + ".png")
        if os.path.exists(dst) and os.path.exists(os.path.join(theme, "source.json")):
            continue
        src = originals.fetch(REPO, BRANCH, LIBRARY[key], env="ELIFOUTS_WALLS_SRC",
                              clone=os.path.expanduser("~/src/rice-refs/elifouts-wallpapers"))
        if not src:
            continue
        # исходник — рядом с темой (source/, в git его нет): из него фильтр пересобирает обои при смене настроек
        keep = os.path.join(theme, "source", key + os.path.splitext(src)[1])
        if not os.path.exists(keep):
            os.makedirs(os.path.dirname(keep), exist_ok=True)
            import shutil
            shutil.copyfile(src, keep)
        sj = os.path.join(theme, "source.json")
        m = json.load(open(sj)) if os.path.exists(sj) else {}
        m[stem + ".png"] = os.path.relpath(keep, theme)
        with open(sj, "w") as f:
            json.dump(m, f, indent=1)
            f.write("\n")
        args = [sys.executable, os.path.join(HERE, "filter.py"), src, "-o", dst, "--theme", theme, "--no-settings"]
        for k, val in opts.items():
            args += ["--" + k, str(val)]
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode:
            print(f"  {stem}: фильтр не сработал: {r.stderr.strip()}", file=sys.stderr)


def hypr_lua(v):
    """Его style.lua: рамка 1 px акцентом, неактивные — акцент …33; без скруглений, размытия, тени, свечения."""
    t = VARIANTS[v]
    acc = (t.get("accent") or t["tube"]["colors"][f"color{t.get('acc', ACCENT)}"]).lstrip("#")
    return f"""-- Retro CRT ({t['title']}): рамка 1 px цветом трубки (omarchy-themes/rices/crt/build.py, по elifouts/Dotfiles).
hl.config({{
	general = {{ col = {{ active_border = "rgba({acc}ff)", inactive_border = "rgba({acc}33)" }} }},
	group = {{ col = {{ border_active = "rgba({acc}ff)", border_inactive = "rgba({acc}33)" }} }},
	misc = {{ background_color = "rgba({t['tube']['special']['background'].lstrip('#')}ff)" }},
}})
"""


def make(v, out=None, name=None):
    p = palette(v)
    if out:
        p["out"], p["name"] = out, name
        p.pop("wallpapers", None)
    nb.PALETTES[v] = p
    t = VARIANTS[v]
    tube = dict(t["tube"], accent=p["accent"], title=p["title"], crt=t.get("crt") or CRT_DEFAULT,
                filter=dict(t.get("filter") or {}, on=bool(t.get("wall"))))
    # tube.json — до сборки: фильтр обоев (walls) читает из него цвет трубки
    os.makedirs(p["out"], exist_ok=True)
    with open(os.path.join(p["out"], "tube.json"), "w") as f:
        json.dump(tube, f, indent=1)
        f.write("\n")
    nb.build(v)
    out = p["out"]
    f = os.path.join(out, "colors.toml")
    lines = open(f).read().split("\n")
    lines[0] = f"# {p['title']} — omarchy-rices/crt (по мотивам Retro из elifouts/Dotfiles, GPL-3.0; сборка: build.py поверх ../nothing/build.py)."
    open(f, "w").write("\n".join(lines))
    open(os.path.join(out, "hyprland.lua"), "w").write(hypr_lua(v))
    import shutil
    shutil.copyfile(os.path.join(HERE, "starship.toml"), os.path.join(out, "starship.toml"))


# omarchy-rice-dynamic: тема из обоев — его профиль с colors.theme = pywal: `wal -i <обои> -n --cols16` (pywal16, если
# установлен: `pip install pywal16` / AUR python-pywal16); без него — схема phosphor, повёрнутая к оттенку акцента обоев.
# accent — трубка варианта base как есть, с обоев только акцент.
DYNAMIC_BASE = "phosphor"
DYNAMIC_MODE = "dark"


def pywal(img):
    """Палитра pywal16 картинки, как у него в color-apply.sh; None — если pywal нет или не вышло."""
    import shutil
    import tempfile
    wal = shutil.which("wal")
    if not wal or not img or not os.path.isfile(img):
        return None
    d = tempfile.mkdtemp(prefix="crt-wal-")
    try:
        env = dict(os.environ, XDG_CACHE_HOME=d, XDG_CONFIG_HOME=os.path.join(d, "cfg"))
        r = subprocess.run([wal, "-i", img, "-n", "-s", "-t", "-e", "-q", "--cols16", "--out-dir", d],
                           env=env, capture_output=True, timeout=60)
        if r.returncode:
            return None
        w = json.load(open(os.path.join(d, "colors.json")))
        return {"special": {k: v.lower() for k, v in w["special"].items()},
                "colors": {k: v.lower() for k, v in w["colors"].items()}}
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        return None
    finally:
        import shutil as _sh
        _sh.rmtree(d, ignore_errors=True)


def base_modes():
    return {v: "dark" for v in VARIANTS if v != "dynamic"}


def tinted(h):
    """Схема phosphor, повёрнутая к оттенку h (его pywal-трубка): светлота и насыщенность — как у phosphor."""
    import colorsys
    base = TUBES["phosphor"]
    h0 = colorsys.rgb_to_hls(*(x / 255 for x in nb.hex2rgb(base["colors"]["color9"])))[0]

    def turn(c):
        if c == "#000000":
            return c
        hh, ll, ss = colorsys.rgb_to_hls(*(x / 255 for x in nb.hex2rgb(c)))
        r, g, b = colorsys.hls_to_rgb((hh - h0 + h) % 1, ll, ss)
        return nb.rgb2hex(round(r * 255), round(g * 255), round(b * 255))
    return {"special": {k: turn(c) for k, c in base["special"].items()},
            "colors": {k: turn(c) for k, c in base["colors"].items()}}


def dynamic(s, out, name, base=DYNAMIC_BASE, scheme="wallpaper", flip=False):
    import colorsys
    base = base if base in VARIANTS and base != "dynamic" else DYNAMIC_BASE
    if scheme == "accent":
        t = {"tube": VARIANTS[base]["tube"], "accent": s["accent"]}
    else:
        tube = pywal(s.get("image"))
        if not tube:
            h = colorsys.rgb_to_hls(*(x / 255 for x in nb.hex2rgb(s["accent"])))[0]
            tube = tinted(h)
        t = {"tube": tube}
    t["crt"] = VARIANTS["wallpaper"]["crt"]  # его профиль Wallpaper (pywal)
    t["title"] = "Retro CRT Dynamic"
    VARIANTS["dynamic"] = t
    make("dynamic", out, name)


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if not a.startswith("--")] or [x for x in VARIANTS if x != "dynamic"]:
        make(v)
