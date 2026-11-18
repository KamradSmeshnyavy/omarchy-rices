#!/usr/bin/env python3
"""Темы space-* — по мотивам стиля Space из github.com/elifouts/Dotfiles (GPL-3.0, Eli Fouts): HUD в духе No Man's
Sky, обои — шейдер пейзажа, который панорамирует при смене стола.

Цвета — ровно его World.qml: тема мира — одна из готовых палитр (themes), акцент — один из её цветов 3..8, а 16 цветов
терминала — его World.palette(): color0 фон, color7/15 текст, color8 серый, 1–6 и 9–14 — цвета палитры, color9 — акцент,
color13 — цвет через четыре от акцента. Варианты — его сохранённые миры (Space/tweaks/saved/desktop): Mars (gruvbox,
красный), Atlas (nord, красный, Atlas вместо луны), Frost (tokyonight, голубой), и Dusk — розовый мир с его скриншота
(dracula, розовый).
Окна как у него: без рамки, свечение акцентом (glow …40), неактивные — без свечения.

Обои — снимки его пейзажа (shaders/terrain из плагина обоев kamradsmeshnyavy.background, scripts/scene-shot.qml) и
рядом <имя>.scene.json (снимок — <имя>.jpg): плагин обоев видит его и рисует живую сцену поверх снимка. Снимки лежат в репо; build.py
перерисовывает только недостающие (нужен плагин обоев, путь — SCENE_SHOT или ~/.config/omarchy/plugins/…).

  python3 build.py              все варианты
  python3 build.py mars frost   выбранные
  python3 build.py --reshoot    перерисовать снимки
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nothing"))
sys.path.insert(0, os.path.join(HERE, ".."))
import build as nb  # noqa: E402
from palettes import contrast  # noqa: E402

# его World.themes: [фон, текст, серый, красный, зелёный, жёлтый, синий, фиолетовый, бирюзовый]
THEMES = {
    "gruvbox": ["#282828", "#ebdbb2", "#665c54", "#fb4934", "#b8bb26", "#fabd2f", "#83a598", "#d3869b", "#8ec07c"],
    "nord": ["#2e3440", "#d8dee9", "#4c566a", "#bf616a", "#a3be8c", "#ebcb8b", "#81a1c1", "#b48ead", "#88c0d0"],
    "tokyonight": ["#24283b", "#c0caf5", "#565f89", "#f7768e", "#9ece6a", "#e0af68", "#7aa2f7", "#bb9af7", "#7dcfff"],
    "dracula": ["#282a36", "#f8f8f2", "#6272a4", "#ff5555", "#50fa7b", "#f1fa8c", "#8be9fd", "#bd93f9", "#ff79c6"],
    # остальные миры его World.themes — для диких систем звёздной карты (world.py)
    "everforest": ["#2d353b", "#d3c6aa", "#475258", "#e67e80", "#a7c080", "#dbbc7f", "#7fbbb3", "#d699b6", "#83c092"],
    "catppuccin": ["#24273a", "#cad3f5", "#5b6078", "#ed8796", "#a6da95", "#eed49f", "#8aadf4", "#c6a0f6", "#8bd5ca"],
    "rosepine": ["#191724", "#e0def4", "#524f67", "#eb6f92", "#9ccfd8", "#f6c177", "#31748f", "#c4a7e7", "#ebbcba"],
    "kanagawa": ["#1f1f28", "#dcd7ba", "#54546d", "#e82424", "#98bb6c", "#e6c384", "#7e9cd8", "#957fb8", "#7aa89f"],
    "solarized": ["#002b36", "#93a1a1", "#586e75", "#dc322f", "#859900", "#b58900", "#268bd2", "#6c71c4", "#2aa198"],
}
# имена как у него (World.themes name, accentNames)
THEME_NAMES = {"everforest": "everforest", "gruvbox": "gruvbox", "nord": "nord", "catppuccin": "catppuccin",
               "tokyonight": "tokyo night", "rosepine": "rosé pine", "dracula": "dracula", "kanagawa": "kanagawa",
               "solarized": "solarized"}
ACCENT_NAMES = ["", "", "", "red", "green", "yellow", "blue", "purple", "cyan"]

# земля — его Space/tweaks/saved/desktop/<Мир>.json (space.land); пусто — значения по умолчанию (Schema.js LAND)
VARIANTS = {
    "mars": {"title": "Space Mars", "theme": "gruvbox", "acc": 3, "land": {
        "atlas": False, "bases": 1, "comets": 3, "dusk": 0.6, "fleet": 0.4, "flora": 0, "galaxy": 0.7,
        "galaxyTilt": 40, "grass": 0.3, "haze": 1, "height": 0.5, "relief": 1, "rocks": 2, "ships": 0.7, "snow": 0,
        "starSize": 0.5, "stars": 2}},
    "atlas": {"title": "Space Atlas", "theme": "nord", "acc": 3, "land": {"atlas": True}},
    "frost": {"title": "Space Frost", "theme": "tokyonight", "acc": 8, "land": {
        "comets": 3, "dusk": 0.75, "flora": 2, "height": 1, "relief": 0.65, "rocks": 2, "snow": 1, "treeSize": 1.1}},
    "dusk": {"title": "Space Dusk", "theme": "dracula", "acc": 8, "land": {}},
}
# снимки: (имя, seed, стол — сдвиг панорамы)
SHOTS = [("1-land", 17, 1), ("2-ridge", 431, 3), ("3-camp", 802, 6)]
SHOT = os.environ.get("SCENE_SHOT", os.path.expanduser(
    "~/.config/omarchy/plugins/kamradsmeshnyavy.background/scripts/scene-shot.qml"))


def readable(c, bg, need):
    for _ in range(40):
        if contrast(c, bg) >= need:
            break
        c = nb.mix(c, "#ffffff", 0.06)
    return c


def ansi16(c, i):
    """Его World.palette(h) для темы c и акцента c[i]."""
    a = [c[0]] + c[3:9] + [c[1], c[2]] + c[3:9] + [c[1]]
    a[9] = c[i]
    a[13] = c[3 + (i - 3 + 4) % 6]
    return a


def colors_of(t):
    """(палитра из 9, акцент, 16 цветов терминала) варианта t: готовая тема или своя (dynamic)."""
    c = t.get("c") or THEMES[t["theme"]]
    acc = t.get("accent") or c[t["acc"]]
    return c, acc, t.get("ansi") or ansi16(c, t["acc"])


def palette(v):
    t = VARIANTS[v]
    c, acc, ansi = colors_of(t)
    bg, fg, grey = c[0], c[1], c[2]
    red, green, yellow, blue, purple, cyan = c[3:9]
    p = {
        "mode": "dark", "title": t["title"], "name": f"space-{v}", "out": os.path.join(HERE, v),
        "bg": bg, "panel": nb.mix(bg, fg, 0.05), "raised": nb.mix(bg, fg, 0.1), "line": nb.mix(bg, fg, 0.18),
        "fg": fg, "dim": readable(grey, bg, 4.5), "comment": readable(grey, bg, 3),
        "accent": acc, "on_accent": bg, "selection": nb.mix(bg, acc, 0.28),
        "error": red, "info": blue, "warn": yellow, "hint": readable(grey, bg, 4.5), "ok": green,
        "diff_add": nb.mix(bg, green, 0.3), "diff_del": nb.mix(bg, red, 0.3), "diff_change": nb.mix(bg, blue, 0.25),
        "keyword": purple, "string": green, "number": yellow, "type": cyan, "function": blue,
        "property": nb.mix(fg, grey, 0.35), "special": acc, "constant": yellow, "ansi_yellow": yellow,
        "min_de": 0, "ansi16": ansi,
    }
    # роли текста — не ниже 4.5 к фону (gruvbox-красный на #282828 — 4.29); акцент и 16 цветов терминала — как у него
    for role in ("error", "info", "warn", "ok", "keyword", "string", "number", "type", "function", "special",
                 "constant", "ansi_yellow"):
        p[role] = readable(p[role], bg, 4.5)
    p["wallpapers"] = lambda pp, d, v=v: walls(v, d)
    return p


def scene(v, seed, ws):
    """Сцена для плагина обоев: его Terrain.qml — bg color0, accent color9, fg color15, tone color4."""
    t = VARIANTS[v]
    c, acc, _ = colors_of(t)
    return {"scene": "terrain", "seed": seed, "workspace": ws, "land": t["land"],
            "colors": {"bg": c[0], "accent": acc, "fg": c[1], "tone": c[6]}}


RESHOOT = "--reshoot" in sys.argv


def walls(v, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for stem, seed, ws in SHOTS:
        cfg = scene(v, seed, ws)
        side = os.path.join(out_dir, stem + ".scene.json")
        jpg = os.path.join(out_dir, stem + ".jpg")
        png = jpg[:-4] + ".shot.png"
        with open(side, "w") as f:
            json.dump(cfg, f, indent=1)
            f.write("\n")
        if os.path.exists(jpg) and not RESHOOT:
            continue
        if not os.path.exists(SHOT):
            print(f"  {stem}: нет {SHOT} — снимок не нарисован (нужен плагин обоев kamradsmeshnyavy.background)",
                  file=sys.stderr)
            continue
        # Qt без экрана рисует шейдеры только через RHI/OpenGL (программный рендер их не умеет); масштаб 1 — ровно W×H
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="rhi", QSG_RHI_BACKEND="opengl",
                   QT_SCALE_FACTOR="1")
        qml = "/usr/lib/qt6/bin/qml" if os.path.exists("/usr/lib/qt6/bin/qml") else "qml6"
        r = subprocess.run([qml, SHOT, "--", json.dumps(cfg), png, "2880", "1800"], env=env, timeout=60)
        if r.returncode or not os.path.exists(png):
            print(f"  {stem}: снимок не получился ({r.returncode})", file=sys.stderr)
            continue
        # снимок Qt — RGBA PNG 2880×1800; в репо — JPEG (небо с дизерингом шейдера, PNG градиентов весит ~2 МБ)
        from PIL import Image
        Image.open(png).convert("RGB").save(jpg, quality=92, optimize=True)
        os.unlink(png)


def hypr_lua(v):
    """Его style.lua: border_size 0, свечение акцентом …40 у активного окна; рамка (если включат) — акцент cc / серый 44."""
    t = VARIANTS[v]
    c, acc, _ = colors_of(t)
    acc, grey = acc.lstrip("#"), c[2].lstrip("#")
    return f"""-- Space ({t['title']}): свечение окна акцентом, рамки нет (omarchy-themes/rices/space/build.py, по elifouts/Dotfiles).
hl.config({{
	general = {{ col = {{ active_border = "rgba({acc}cc)", inactive_border = "rgba({grey}44)" }} }},
	group = {{ col = {{ border_active = "rgba({acc}cc)", border_inactive = "rgba({grey}44)" }} }},
	decoration = {{ glow = {{ enabled = true, range = 8, render_power = 3, color = "rgba({acc}40)", color_inactive = "rgba({acc}00)" }} }},
}})
"""


def make(v, out=None, name=None):
    p = palette(v)
    if out:
        p["out"], p["name"] = out, name
        p.pop("wallpapers", None)
    nb.PALETTES[v] = p
    nb.build(v)
    out = p["out"]
    f = os.path.join(out, "colors.toml")
    lines = open(f).read().split("\n")
    lines[0] = f"# {p['title']} — omarchy-rices/space (по мотивам Space из elifouts/Dotfiles, GPL-3.0; сборка: build.py поверх ../nothing/build.py)."
    open(f, "w").write("\n".join(lines))
    open(os.path.join(out, "hyprland.lua"), "w").write(hypr_lua(v))


# omarchy-rice-dynamic: тема из обоев. Его «случайный мир» — World.palette(h): вся палитра из одного оттенка (HSL);
# оттенок — акцент обоев. accent — вариант base как есть, с обоев только акцент. Space всегда тёмный.
DYNAMIC_BASE = "dusk"
DYNAMIC_MODE = "dark"


def base_modes():
    return {v: "dark" for v in VARIANTS if v != "dynamic"}


def world(h):
    """Его World.palette(h) без готовой темы: 16 цветов по тонам вокруг h."""
    import colorsys

    def c(dh, sat, li):
        r, g, b = colorsys.hls_to_rgb(((h + dh) % 1 + 1) % 1, li, sat)
        return nb.rgb2hex(round(r * 255), round(g * 255), round(b * 255))
    tones = [0, 0.07, 0.14, 0.5, 0.57, -0.08]
    a = [c(0, 0.35, 0.06)] + [c(x, 0.5, 0.52) for x in tones] + [c(0, 0.14, 0.78), c(0, 0.18, 0.32)] + \
        [c(x, 0.7, 0.68) for x in tones] + [c(0, 0.1, 0.94)]
    # палитра из 9 (фон, текст, серый, 6 цветов) — как у готовых тем; акцент — color9
    return [a[0], a[15], a[8]] + a[1:7], a[9], a


def dynamic(s, out, name, base=DYNAMIC_BASE, scheme="wallpaper", flip=False):
    import colorsys
    if scheme == "accent":
        t = dict(VARIANTS[base])
        t["accent"] = s["accent"]
    else:
        r, g, b = (x / 255 for x in nb.hex2rgb(s["accent"]))
        h = colorsys.rgb_to_hls(r, g, b)[0]
        c, acc, ansi = world(h)
        t = {"c": c, "accent": acc, "ansi": ansi, "land": VARIANTS[base]["land"]}
    t["title"] = "Space Dynamic"
    VARIANTS["dynamic"] = t
    make("dynamic", out, name)


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if not a.startswith("--")] or list(VARIANTS):
        make(v)
