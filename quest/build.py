#!/usr/bin/env python3
"""Темы quest-* — пиксельный райс в духе 16-битных ролевых игр (свой, не порт): окна-диалоги с градиентом и двойной
светлой рамкой, курсор-рука, батарея — HP, память — MP, аптайм — опыт.

Варианты: classic (синие окна, ночь), dusk (фиолетовые, закат), forest (зелёные, лес), dungeon (подземелье: чёрное и
алое, кость, готический пиксельный шрифт), parchment (светлый: пергамент и чернила).

Кроме тем приложений (поверх ../nothing/build.py) пишет:
  quest.json            — токены окон для оболочки (бар, Super+M, дашборд, плеер, уведомления, OSD, блокировка);
  apps/fastfetch.jsonc  — «лист персонажа» с героем полублоками (apps/quest-logo.txt);
  backgrounds/          — 1-scene.png (сцена генератора в цветах варианта) и обои пользователя из ~/Wallpapers
                          (0-original / 0r-*, в git не входят).

  python3 build.py              все варианты
  python3 build.py classic      выбранные
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nothing"))
sys.path.insert(0, os.path.join(HERE, "..", "pixel"))
import build as nb  # noqa: E402
import kit  # noqa: E402
from palettes import contrast  # noqa: E402

# Токены окна: w1/w2 — градиент окна сверху вниз, frame/frame2 — внешняя и внутренняя рамка, text/dim — текст,
# hi — курсор и выделение, hp/mp — полоски, red — урон и ошибки, ink — самый тёмный (контур спрайтов).
# Сцена: sky1→sky2 — небо сверху вниз, mtn2/mtn — дальние и ближние горы, ground — земля, lit — окна замка.
VARIANTS = {
    "classic": {
        "title": "Quest Classic", "mode": "dark", "scene": "night",
        "w1": "#2a4cc0", "w2": "#0d1a66", "frame": "#f4f4f4", "frame2": "#8f9ac8", "text": "#f4f4f4", "dim": "#a9b4e8",
        "hi": "#ffd84a", "hp": "#5ee06a", "mp": "#5cb4ff", "red": "#ff6a5a", "ink": "#0a0c20",
        "sky1": "#070b26", "sky2": "#3a3f8f", "mtn": "#151a44", "mtn2": "#262c68", "ground": "#0f1330",
        "walls": [("clouds", "clouds-5.jpg"), ("tropic-night", "tropic_island_night.jpg"),
                  ("tropic-morning", "tropic_island_morning.jpg"), ("tropic-day", "tropic_island_day.jpg"),
                  ("tropic-evening", "tropic_island_evening.jpg"), ("voyager-10", "voyager-10.jpg"),
                  ("voyager-17", "voyager-17.jpg"), ("prairie", "pixel-prairie.jpg")],
    },
    "dusk": {
        "title": "Quest Dusk", "mode": "dark", "scene": "dusk",
        "w1": "#6a2f8f", "w2": "#24103d", "frame": "#f4f4f4", "frame2": "#c2a3d6", "text": "#f6eefa", "dim": "#d9bfeb",
        "hi": "#ffb347", "hp": "#7ee08a", "mp": "#7fd0e8", "red": "#ff6a7a", "ink": "#12081c",
        "sky1": "#160926", "sky2": "#c04f6c", "mtn": "#2a1236", "mtn2": "#53204f", "ground": "#170a1d",
        "walls": [("clouds-2", "clouds-2.png"), ("mountains", "mountain-range.jpg"), ("voyager-8", "voyager-8.jpg"),
                  ("waves", "waves.png"), ("clouds-3", "clouds-3.png"), ("plane", "plane-purple.png")],
    },
    "forest": {
        "title": "Quest Forest", "mode": "dark", "scene": "forest",
        "w1": "#2c7a4e", "w2": "#0b2d1d", "frame": "#f4f4f4", "frame2": "#9fc7a9", "text": "#f2f8ee", "dim": "#bde4c4",
        "hi": "#f5e663", "hp": "#8ee06a", "mp": "#6fd3e0", "red": "#ff7a5a", "ink": "#06140c",
        "sky1": "#061a15", "sky2": "#3a7d5e", "mtn": "#0d2c20", "mtn2": "#1b4b35", "ground": "#08170f",
        "walls": [("stall", "stall.jpg"), ("voyager-4", "voyager-4.jpg"), ("voyager-5", "voyager-5.jpg"),
                  ("voyager-13", "voyager-13.jpg"), ("village-gate", "village-gate.jpg"),
                  ("sunflowers", "my-neighbor-totoro-sunflowers.png"), ("napping", "pixel-napping.png")],
    },
    "dungeon": {
        "title": "Quest Dungeon", "mode": "dark", "scene": "dungeon", "font": "Jacquard 12 Hell",
        "w1": "#3a0d12", "w2": "#120406", "frame": "#d9cbb0", "frame2": "#7a2a2a", "text": "#ece0c8", "dim": "#b39a80",
        "hi": "#ff3b30", "hp": "#e0453a", "mp": "#9a7ae8", "red": "#ff3b30", "ink": "#050102",
        "sky1": "#050203", "sky2": "#2a0a0e", "mtn": "#1a0709", "mtn2": "#2e0d10", "ground": "#0a0304",
        # золото курсора здесь — алое, как кровь; числа и константы — тусклое золото и кость, чтобы не слиться
        "syn": {"number": "#d8a630", "constant": "#e8b89a", "special": "#c86a9a"},
        "walls": [("knight-sit", "knight-sit.png"), ("pompeii", "pompeii.png"), ("voyager-20", "voyager-20.jpg"),
                  ("pixel-castle", "pixel-castle.png"), ("voyager-2", "voyager-2.jpg")],
    },
    "parchment": {
        "title": "Quest Parchment", "mode": "light", "scene": "day",
        "w1": "#f8efd6", "w2": "#eadbb0", "frame": "#4a3220", "frame2": "#b08f5e", "text": "#2e2216", "dim": "#6e5636",
        "hi": "#b0302a", "hp": "#3d7a2a", "mp": "#2a5a9a", "red": "#b0302a", "ink": "#2a1c10",
        "sky1": "#8fc4ec", "sky2": "#e6f2f6", "mtn": "#7a9a6a", "mtn2": "#a8c0a0", "ground": "#6a8a4a",
        # красные чернила — и курсор, и ошибки; числа — сепия, константы — фиолетовые чернила
        "syn": {"number": "#9a5a14", "constant": "#6a3a8a"},
        "walls": [("castle", "castle.png"), ("windmills", "voyager-12.jpg"), ("prairie", "pixel-prairie.jpg"),
                  ("cat-clouds", "cat-in-clouds.png"), ("tropic-day", "tropic_island_day.jpg")],
    },
}


def readable(c, bg, need, light=False):
    """Темнее (светлая тема) или светлее (тёмная), пока контраст к фону не станет need."""
    for _ in range(60):
        if contrast(c, bg) >= need:
            break
        c = nb.mix(c, "#000000" if light else "#ffffff", 0.05)
    return c


def palette(v):
    t = VARIANTS[v]
    light = t["mode"] == "light"
    bg = t["w1"] if light else t["w2"]
    fg = t["text"]
    r = lambda c, need=4.5: readable(c, bg, need, light)  # noqa: E731
    p = {
        "mode": t["mode"], "title": t["title"], "name": f"quest-{v}", "out": os.path.join(HERE, v),
        "bg": bg, "panel": nb.mix(bg, t["w2" if light else "w1"], 0.3), "raised": nb.mix(bg, t["w2" if light else "w1"], 0.55),
        "line": nb.mix(bg, t["frame2"], 0.6), "fg": fg, "dim": r(t["dim"]), "comment": r(nb.mix(t["dim"], bg, 0.35), 3),
        "accent": r(t["hi"], 3), "on_accent": t["ink"] if not light else t["w1"],
        "selection": nb.mix(bg, t["w1"] if not light else t["frame2"], 0.55 if not light else 0.35),
        "error": r(t["red"]), "info": r(t["mp"]), "warn": r(nb.mix(t["hi"], t["red"], 0.35)), "hint": r(t["dim"]),
        "ok": r(t["hp"]),
        "diff_add": nb.mix(bg, t["hp"], 0.25), "diff_del": nb.mix(bg, t["red"], 0.25), "diff_change": nb.mix(bg, t["mp"], 0.22),
        # Синтаксис по-ролевому: ключевые слова — золото курсора, строки — HP, типы — MP, функции — светлый цвет окна
        "keyword": r(t["hi"]), "string": r(t["hp"]), "number": r(nb.mix(t["hi"], t["red"], 0.5)), "type": r(t["mp"]),
        "function": r(nb.mix(t["w1"], "#ffffff" if not light else "#000000", 0.55)),
        "property": r(nb.mix(fg, t["dim"], 0.55)), "special": r(nb.mix(t["red"], t["mp"], 0.45)),
        "constant": r(nb.mix(t["hi"], t["hp"], 0.45)), "ansi_yellow": r(t["hi"]),
        "min_de": 8,
    }
    for role, c in t.get("syn", {}).items():
        p[role] = r(c)
    if light:
        p["light_mode_file"] = True
    p["wallpapers"] = lambda pp, d, v=v: walls(v, d)
    return p


# ── Сцены генератора (320×200 → 2880×1800 без сглаживания) ─────────────────

def scene_castle(t, dst):
    from PIL import ImageDraw
    import math
    img = kit.canvas(t["sky1"])
    kit.dither_v(img, t["sky1"], t["sky2"], 10, 130)
    d = ImageDraw.Draw(img)
    rnd = kit.Rng(11)
    light = t["scene"] == "day"
    # звёзды (ночью) или облака (днём)
    if not light:
        for _ in range(140):
            x, y = int(rnd() * kit.LOW_W), int(rnd() * 90)
            d.point((x, y), fill=t["frame"] if rnd() > 0.2 else t["hi"])
    else:
        for cx, cy, w in ((40, 30, 46), (180, 22, 60), (260, 48, 40)):
            d.rectangle([cx, cy + 4, cx + w, cy + 10], fill="#ffffff")
            d.rectangle([cx + 8, cy, cx + w - 14, cy + 4], fill="#ffffff")
            d.rectangle([cx + 2, cy + 10, cx + w - 4, cy + 12], fill=t["sky2"])
    # луна / солнце
    sun = {"day": "#ffe08a", "dusk": t["hi"]}.get(t["scene"], t["frame"])
    cx, cy, rr = {"dusk": (110, 112, 22), "day": (60, 40, 14)}.get(t["scene"], (250, 46, 14))
    for y in range(-rr, rr + 1):
        for x in range(-rr, rr + 1):
            if x * x + y * y <= rr * rr and (light or t["scene"] == "dusk" or (x + 5) ** 2 + (y - 3) ** 2 > rr * rr * 0.6):
                d.point((cx + x, cy + y), fill=sun)

    def ridge(c, base, amp, f, ph):
        for x in range(kit.LOW_W):
            h = base - abs(math.sin(x * f + ph)) * amp - math.sin(x * f * 2.7 + ph) * amp * 0.25
            d.line([(x, int(h)), (x, kit.LOW_H)], fill=c)
    ridge(t["mtn2"], 132, 44, 0.022, 1.0)
    ridge(t["mtn"], 150, 26, 0.04, 3.0)
    # замок на холме
    ink = t["ink"] if not light else nb.mix(t["mtn"], "#000000", 0.45)
    lit = t["hi"]
    bx = 196
    d.rectangle([bx, 112, bx + 56, 152], fill=ink)
    d.rectangle([bx - 8, 92, bx + 6, 152], fill=ink)
    d.rectangle([bx + 50, 92, bx + 64, 152], fill=ink)
    d.rectangle([bx + 20, 80, bx + 36, 116], fill=ink)
    for i in range(0, 14, 4):
        d.rectangle([bx - 8 + i, 88, bx - 6 + i, 92], fill=ink)
        d.rectangle([bx + 50 + i, 88, bx + 52 + i, 92], fill=ink)
    d.polygon([(bx + 18, 80), (bx + 28, 62), (bx + 38, 80)], fill=ink)
    d.line([(bx + 28, 62), (bx + 28, 52)], fill=ink)
    d.rectangle([bx + 29, 52, bx + 36, 56], fill=t["red"])
    if not light:
        for x, y in ((bx - 3, 100), (bx + 55, 100), (bx + 26, 90), (bx + 10, 124), (bx + 42, 124), (bx + 26, 128)):
            d.rectangle([x, y, x + 2, y + 4], fill=lit)
    d.rectangle([bx + 22, 136, bx + 34, 152], fill=nb.mix(ink, lit, 0.15))
    # земля
    d.rectangle([0, 152, kit.LOW_W, kit.LOW_H], fill=t["ground"])
    for x in range(0, kit.LOW_W, 3):
        d.point((x, 152 + (x * 7) % 5), fill=t["mtn"])
    # тропинка к воротам и герой у костра
    for i in range(18):
        d.rectangle([bx + 26 - i * 4, 154 + i * 2, bx + 32 - i * 4, 155 + i * 2], fill=nb.mix(t["ground"], t["dim"], 0.25))
    cols = {"k": ink, "s": t["frame2"], "W": t["frame"], "w": t["text"], "e": t["hi"], "h": t["hi"], "b": t["w1"],
            "r": t["red"], "f": t["red"], "y": t["hi"], "n": nb.mix(t["ground"], "#8a5a2b", 0.7)}
    kit.draw(img, "hero", 96, 164, cols)
    kit.draw(img, "torch", 118, 172, cols)
    kit.save_scene(img, dst)


def scene_dungeon(t, dst):
    from PIL import ImageDraw
    img = kit.canvas(t["w2"])
    d = ImageDraw.Draw(img)
    stone, mortar = t["w1"], t["ink"]
    # кладка
    for row, y in enumerate(range(0, 170, 10)):
        off = 0 if row % 2 else 10
        for x in range(-off, kit.LOW_W, 20):
            shade = nb.mix(stone, t["ink"], 0.15 * ((x // 20 + row) % 3))
            d.rectangle([x + 1, y + 1, x + 19, y + 9], fill=shade)
        d.line([(0, y), (kit.LOW_W, y)], fill=mortar)
    # арка-проход в центре
    cx = kit.LOW_W // 2
    for y in range(60, 170):
        for x in range(cx - 40, cx + 41):
            dx, dy = (x - cx) / 40, (y - 100) / 40
            if y >= 100 or dx * dx + dy * dy <= 1:
                d.point((x, y), fill=t["ink"])
    # пол
    d.rectangle([0, 170, kit.LOW_W, kit.LOW_H], fill=nb.mix(t["ink"], stone, 0.4))
    for x in range(0, kit.LOW_W, 24):
        d.line([(x, 170), (x - 30, kit.LOW_H)], fill=t["ink"])
    # свет факелов (дизеринг вокруг огня)
    px = img.load()
    glow = kit.hex2rgb(t["red"])
    for fx, fy in ((70, 92), (250, 92)):
        for y in range(fy - 40, fy + 50):
            for x in range(fx - 40, fx + 41):
                if 0 <= x < kit.LOW_W and 0 <= y < kit.LOW_H:
                    dist = ((x - fx) ** 2 + (y - fy) ** 2) ** 0.5 / 40 * 16
                    if dist < kit.BAYER[y % 4][x % 4] - 4:
                        c = px[x, y]
                        px[x, y] = tuple(int(a + (b - a) * 0.35) for a, b in zip(c, glow))
    cols = {"f": t["red"], "y": t["hi"] if t["hi"] != t["red"] else "#ffb347", "n": "#3a2410", "k": t["ink"],
            "W": t["frame"], "h": "#d8a630"}
    kit.draw(img, "torch", 68, 88, cols, 1)
    kit.draw(img, "torch", 248, 88, cols, 1)
    kit.draw(img, "chest", cx - 5, 160, cols, 1)
    kit.draw(img, "skull", 40, 166, cols, 1)
    kit.save_scene(img, dst)


def walls(v, out_dir):
    t = VARIANTS[v]
    (scene_dungeon if t["scene"] == "dungeon" else scene_castle)(t, os.path.join(out_dir, "1-scene.png"))
    kit.place_local(out_dir, t["walls"])


# ── Файлы райса поверх тем nothing ─────────────────────────────────────────

def tokens(v):
    """quest.json — для оболочки: окна, полоски, шрифты, сцена."""
    t = VARIANTS[v]
    keys = ("w1", "w2", "frame", "frame2", "text", "dim", "hi", "hp", "mp", "red", "ink")
    return {"rice": "quest", "variant": v, "title": t["title"], "mode": t["mode"],
            "font": t.get("font", "Press Start 2P"), "body": "Pixelify Sans", "mono": "Departure Mono",
            "radius": 6 if v != "dungeon" else 0, **{k: t[k] for k in keys}}


def hypr_lua(v):
    t = VARIANTS[v]
    a, i = t["frame"].lstrip("#"), t["frame2"].lstrip("#")
    return f"""-- {t['title']}: рамка окна — светлая рамка диалога, у неактивного — её внутренний цвет
-- (omarchy-themes/rices/quest/build.py). Толщину и углы задаёт стиль Customizer «quest».
hl.config({{
	general = {{ col = {{ active_border = "rgb({a})", inactive_border = "rgb({i})" }} }},
	group = {{ col = {{ border_active = "rgb({a})", border_inactive = "rgb({i})" }} }},
}})
"""


def fastfetch_conf(v):
    """«Лист персонажа»: герой полублоками слева, справа характеристики по-ролевому."""
    t = VARIANTS[v]
    e = lambda h: "38;2;%d;%d;%d" % kit.hex2rgb(h)  # noqa: E731
    esc = lambda h: "\x1b[%sm" % e(h)  # noqa: E731
    sw = "".join("\x1b[48;2;%d;%d;%dm   " % kit.hex2rgb(c) for c in
                 (t["w2"], t["w1"], t["frame2"], t["red"], t["hp"], t["mp"], t["hi"], t["frame"]))
    mod = lambda typ, key, fmt=None: dict({"type": typ, "key": key}, **({"format": fmt} if fmt else {}))  # noqa: E731
    custom = lambda s: {"type": "custom", "format": s}  # noqa: E731
    head = "ЛИСТ ПЕРСОНАЖА" if v != "dungeon" else "† СВИТОК ПРОКЛЯТОГО †"
    conf = {
        "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
        "logo": {"type": "file-raw", "source": "~/.local/state/omarchy/current/theme/apps/quest-logo.txt",
                 "padding": {"top": 1, "left": 2, "right": 4}},
        "display": {
            "separator": "  ",
            "color": {"keys": e(t["hi"]), "title": e(t["frame"]), "output": e(t["text"]), "separator": e(t["frame2"])},
            "key": {"width": 8},
            "bar": {"char": {"elapsed": "■", "total": "·"}, "width": 10, "border": {"left": "", "right": ""}},
            "percent": {"type": 3, "color": {"green": e(t["hp"]), "yellow": e(t["hi"]), "red": e(t["red"])}},
        },
        "modules": [
            custom(esc(t["hi"]) + "▶ " + esc(t["frame"]) + head), custom(esc(t["frame2"]) + "═" * 26),
            mod("title", "HERO", "{user-name}@{host-name}"), mod("os", "CLASS", "{pretty-name}"),
            mod("wm", "WEAPON", "{pretty-name}"), mod("shell", "SPELL", "{pretty-name}"),
            mod("uptime", "EXP"), mod("battery", "HP", "{capacity-bar} {capacity}"),
            mod("memory", "MP", "{percentage-bar} {used}"), mod("disk", "GOLD", "{size-available} free"),
            "break", custom(sw + "\x1b[0m"),
        ],
    }
    return f"// {t['title']}: omarchy-themes/rices/quest/build.py\n" + json.dumps(conf, indent=2, ensure_ascii=False) + "\n"


def logo(v):
    return kit.ansi_logo("hero", sprite_colors(v))


def sprite_colors(v):
    """Роли спрайтов в цветах варианта (как у героя в fastfetch)."""
    t = VARIANTS[v]
    dark = t["mode"] == "dark"
    ink = nb.mix(t["w1"], t["ink"], 0.5) if dark else t["frame"]
    return {"k": ink, "s": t["frame2"], "W": t["frame"] if dark else t["w1"], "w": t["text"], "e": t["hi"],
            "h": t["hi"] if v != "dungeon" else "#d8a630", "b": t["w1"] if dark else t["mp"], "r": t["red"],
            "n": "#8a5a2b" if v != "dungeon" else "#5a3418", "m": t["mp"], "f": t["red"],
            "y": t["hi"] if v != "dungeon" else "#ffb347", "g": t["hp"], "c": t["mp"]}


def sprites(v, out):
    """Спрайты оболочки: <тема>/quest/<имя>.png в масштабе 1 (QML увеличивает без сглаживания, smooth: false)."""
    cols = sprite_colors(v)
    for name in kit.SPRITES:
        kit.png(name, cols, os.path.join(out, "quest", name + ".png"))
    # рука курсора — всегда светлая с тёмным контуром, как в окне диалога
    t = VARIANTS[v]
    kit.png("hand", {"k": t["ink"], "W": "#f4f4f4" if t["mode"] == "dark" else "#fffaf0"}, os.path.join(out, "quest", "hand.png"))


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
    lines[0] = f"# {p['title']} — omarchy-rices/quest (свой пиксельный райс; сборка: build.py поверх ../nothing/build.py)."
    open(f, "w").write("\n".join(lines))
    open(os.path.join(out, "hyprland.lua"), "w").write(hypr_lua(v))
    with open(os.path.join(out, "quest.json"), "w") as fh:
        json.dump(tokens(v), fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    open(os.path.join(out, "apps", "quest-logo.txt"), "w").write(logo(v))
    sprites(v, out)
    open(os.path.join(out, "apps", "fastfetch.jsonc"), "w").write(fastfetch_conf(v))
    shutil.copyfile(os.path.join(HERE, "starship.toml"), os.path.join(out, "starship.toml"))


# omarchy-rice-dynamic: акцент обоев вместо золота курсора, остальное — как у base.
DYNAMIC_BASE = "classic"
DYNAMIC_MODE = "dark"


def base_modes():
    return {v: VARIANTS[v]["mode"] for v in VARIANTS if v != "dynamic"}


def dynamic(s, out, name, base=DYNAMIC_BASE, scheme="wallpaper", flip=False):
    t = dict(VARIANTS[base])
    t["hi"] = s["accent"]
    if scheme != "accent":
        t["w2"] = s.get("background", t["w2"]) if t["mode"] == "dark" else t["w2"]
        t["w1"] = nb.mix(t["w2"], s["accent"], 0.35)
    t["title"] = "Quest Dynamic"
    VARIANTS["dynamic"] = t
    make("dynamic", out, name)


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if not a.startswith("--")] or list(VARIANTS):
        make(v)
