#!/usr/bin/env python3
"""Темы crt-* — по мотивам стиля Retro из github.com/elifouts/Dotfiles (GPL-3.0, Eli Fouts): старый зелёный терминал,
весь экран — через ЭЛТ-шейдер, обои прорисованы или задизерены в цвет трубки.

Цвета — ровно его wal-схемы трубок (.config/wal/colorschemes/dark/{phosphor,amber,cyan,paper}.json): фон чёрный,
текст color7, акцент — color9 (его color-roles accent по умолчанию 9). 16 цветов терминала — как у него. Схема лежит
в теме файлом tube.json — по нему фильтр обоев (filter.py) и шейдер (shader.py) берут цвет трубки.
Окна как у него (Retro/base/style.lua): рамка 1 px акцентом, у неактивных — акцент …33, без скруглений, без размытия,
тени и свечения.

Обои: 1-black.png — его обои по умолчанию (фильтр выключен — просто чёрный экран, на нём живёт терминал); 0r-* — его
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
VARIANTS = {
    "phosphor": {"title": "Retro CRT Phosphor"},
    "amber": {"title": "Retro CRT Amber"},
    "cyan": {"title": "Retro CRT Cyan"},
    "paper": {"title": "Retro CRT Paper"},
}
for _v in VARIANTS:
    VARIANTS[_v]["tube"] = TUBES[_v]
ACCENT = 9  # его state/color-roles.json: accent 9

# его обои (wallpapers/library) через фильтр: (имя, путь в его репо, тон фильтра)
REPO, BRANCH = "elifouts/Dotfiles", "main"
WALLS = [("0r-gru-04", "wallpapers/library/gruvbox/gru-04.jpg", "lines"),
         ("0r-nat-09", "wallpapers/library/nature/nat-09.jpg", "tube"),
         ("0r-cat-10", "wallpapers/library/catppuccin/cat-10.png", "lines"),
         ("0r-gru-01", "wallpapers/library/gruvbox/gru-01.jpg", "tube")]


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
    acc = t.get("accent") or a[ACCENT]
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
    for role in ("error", "info", "warn", "ok", "keyword", "string", "number", "type", "function", "special",
                 "constant", "ansi_yellow"):
        p[role] = readable(p[role], bg, 4.5)
    p["wallpapers"] = lambda pp, d, v=v: walls(v, d)
    return p


def walls(v, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    black = os.path.join(out_dir, "1-black.png")
    if not os.path.exists(black):
        from PIL import Image
        Image.new("RGB", (64, 64), VARIANTS[v]["tube"]["special"]["background"]).save(black)
    theme = os.path.dirname(out_dir)
    for stem, rel, tone in WALLS:
        dst = os.path.join(out_dir, stem + ".png")
        if os.path.exists(dst):
            continue
        src = originals.fetch(REPO, BRANCH, rel, env="ELIFOUTS_SRC", clone=os.path.expanduser("~/src/rice-refs/elifouts"))
        if not src:
            continue
        r = subprocess.run([sys.executable, os.path.join(HERE, "filter.py"), src, "-o", dst, "--theme", theme,
                            "--tone", tone, "--pixel", "2"], capture_output=True, text=True)
        if r.returncode:
            print(f"  {stem}: фильтр не сработал: {r.stderr.strip()}", file=sys.stderr)


def hypr_lua(v):
    """Его style.lua: рамка 1 px акцентом, неактивные — акцент …33; без скруглений, размытия, тени, свечения."""
    t = VARIANTS[v]
    acc = (t.get("accent") or t["tube"]["colors"][f"color{ACCENT}"]).lstrip("#")
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
    tube = dict(VARIANTS[v]["tube"], accent=p["accent"], title=p["title"])
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


# omarchy-rice-dynamic: тема из обоев. Его профиль «Wallpaper» — pywal красит трубку: оттенок трубки — акцент обоев,
# остальное — как у phosphor, но повёрнуто к этому оттенку.
DYNAMIC_BASE = "phosphor"
DYNAMIC_MODE = "dark"


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
    if scheme == "accent":
        t = {"tube": TUBES[base], "accent": s["accent"]}
    else:
        h = colorsys.rgb_to_hls(*(x / 255 for x in nb.hex2rgb(s["accent"])))[0]
        t = {"tube": tinted(h)}
    t["title"] = "Retro CRT Dynamic"
    VARIANTS["dynamic"] = t
    make("dynamic", out, name)


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if not a.startswith("--")] or [x for x in VARIANTS if x != "dynamic"]:
        make(v)
