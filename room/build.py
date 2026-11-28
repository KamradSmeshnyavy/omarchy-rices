#!/usr/bin/env python3
"""Темы room-* — пиксельный райс Cozy Room (свой): тёплая lofi-комната. Бар — полка с книгами-столами, Super+M —
инвентарь предметов, дашборд — сама комната с живыми предметами (окно — погода, кружка — CPU, растение — диск,
кот — память, лампа — батарея, книги — окна, радио — плеер, дверь — выключение).

Варианты: evening (вечер, тёплое дерево), rain (ливень, холодный синий с тёплой лампой), sakura (светлая розовая).

Кроме тем приложений (поверх ../nothing/build.py) пишет:
  room.json             — токены для оболочки (цвета дерева, стен, лампы, бумаги; шрифты; места предметов на фоне);
  room/<предмет>.png    — спрайты предметов в цветах варианта, room/dash.png — пустая комната для дашборда (320×180);
  apps/fastfetch.jsonc  — кот полублоками и «записка» с системой (apps/room-logo.txt);
  backgrounds/          — 1-scene.png (комната генератора) и обои пользователя из ~/Wallpapers (0-original / 0r-*).

  python3 build.py              все варианты
  python3 build.py evening      выбранные
"""
import json
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nothing"))
sys.path.insert(0, os.path.join(HERE, "..", "pixel"))
import build as nb  # noqa: E402
import kit  # noqa: E402
from palettes import contrast  # noqa: E402

# Токены: wall/wall2 — обои стены полосами, floor/floor2 — доски пола, wood/wood2/dark — дерево (стол, полка, рама),
# night — стекло окна, lamp — свет лампы и акцент, text/dim — текст на тёмном дереве, ink — контур, paper/paperink —
# записки, red/grn/cyan/pink — книги, растение, дождь, кружка.
VARIANTS = {
    "evening": {
        "title": "Cozy Room Evening", "mode": "dark", "weather": "clear",
        "wall": "#4a3340", "wall2": "#3c2834", "floor": "#6b4437", "floor2": "#5a382d", "night": "#1b2944",
        "lamp": "#f2b25c", "text": "#f4e3c1", "dim": "#c9a98a", "ink": "#21161d", "wood": "#8b5a3c", "wood2": "#5c3a2e",
        "dark": "#3b241c", "paper": "#f4e3c1", "paperink": "#3b241c", "red": "#d9675f", "grn": "#7aa860",
        "cyan": "#7fb2d9", "pink": "#e48aa0",
        "walls": [("reading", "pixel-reading.png"), ("comfy-home", "comfy-home.png"), ("cat-vibin", "cat-vibin.png"),
                  ("lantern-room", "lantern-light-room.png"), ("kitchen", "kitchen.png"), ("retro-live", "retro2_live.gif"),
                  ("coffee-shop", "coffee-shop.png"), ("cabin-3", "cabin-3.png")],
    },
    "rain": {
        "title": "Cozy Room Rain", "mode": "dark", "weather": "rain",
        "wall": "#36404f", "wall2": "#2b3341", "floor": "#4b4b57", "floor2": "#3d3d48", "night": "#121b29",
        "lamp": "#f0c070", "text": "#e8ecf2", "dim": "#a9b4c4", "ink": "#161a22", "wood": "#6e5a4c", "wood2": "#4a4e5c",
        "dark": "#2a2d37", "paper": "#e8e4da", "paperink": "#2a2d37", "red": "#d98a7a", "grn": "#7fa58a",
        "cyan": "#9cc3e6", "pink": "#c89ab8",
        "walls": [("cat-vibin", "cat-vibin.png"), ("flowering-rain", "flowering-rain.png"), ("rainnight", "Rainnight.jpg"),
                  ("cold-alley", "cold-alley.png"), ("japan-alley", "japan-alley.png"), ("street-4", "street-4.png"),
                  ("cabin", "cabin.png")],
    },
    "sakura": {
        "title": "Cozy Room Sakura", "mode": "light", "weather": "clear",
        "wall": "#e3b7c2", "wall2": "#d2a0ae", "floor": "#a8707a", "floor2": "#93606a", "night": "#8fb8e0",
        "lamp": "#c98a1c", "text": "#4c2a38", "dim": "#7a5464", "ink": "#3a2030", "wood": "#9a6a5a", "wood2": "#7a4a5a",
        "dark": "#4c2a38", "paper": "#fff6f0", "paperink": "#4c2a38", "red": "#c8406a", "grn": "#5e9a4c",
        "cyan": "#4a86b0", "pink": "#e06c8c",
        "walls": [("comfy-home", "comfy-home.png"), ("laundry", "laundry.jpg"), ("napping", "pixel-napping.png"),
                  ("coffee-shop", "coffee-shop.png"), ("prairie", "pixel-prairie.jpg"), ("main-street", "main-street.png")],
    },
}


def readable(c, bg, need, light=False):
    for _ in range(60):
        if contrast(c, bg) >= need:
            break
        c = nb.mix(c, "#000000" if light else "#ffffff", 0.05)
    return c


def palette(v):
    t = VARIANTS[v]
    light = t["mode"] == "light"
    bg = t["paper"] if light else nb.mix(t["ink"], t["wall2"], 0.35)
    fg = t["paperink"] if light else t["text"]
    r = lambda c, need=4.5: readable(c, bg, need, light)  # noqa: E731
    p = {
        "mode": t["mode"], "title": t["title"], "name": f"room-{v}", "out": os.path.join(HERE, v),
        "bg": bg, "panel": nb.mix(bg, t["wood2"], 0.25), "raised": nb.mix(bg, t["wood2"], 0.45),
        "line": nb.mix(bg, t["wood"], 0.55), "fg": fg, "dim": r(t["dim"]), "comment": r(nb.mix(t["dim"], bg, 0.3), 3),
        "accent": r(t["lamp"], 3), "on_accent": t["ink"] if not light else t["paper"],
        "selection": nb.mix(bg, t["lamp"], 0.22),
        "error": r(t["red"]), "info": r(t["cyan"]), "warn": r(t["lamp"]), "hint": r(t["dim"]), "ok": r(t["grn"]),
        "diff_add": nb.mix(bg, t["grn"], 0.25), "diff_del": nb.mix(bg, t["red"], 0.25), "diff_change": nb.mix(bg, t["cyan"], 0.22),
        # синтаксис тёплый: ключевые — свет лампы, строки — растение, типы — дождь, функции — розовая кружка
        "keyword": r(t["lamp"]), "string": r(t["grn"]), "number": r(nb.mix(t["lamp"], t["red"], 0.55)), "type": r(t["cyan"]),
        "function": r(t["pink"]), "property": r(nb.mix(fg, t["dim"], 0.5)), "special": r(t["red"]),
        "constant": r(nb.mix(t["lamp"], t["grn"], 0.5)), "ansi_yellow": r(t["lamp"]),
        "min_de": 8,
    }
    if light:
        p["light_mode_file"] = True
    p["wallpapers"] = lambda pp, d, v=v: walls(v, d)
    return p


def sprite_colors(v):
    t = VARIANTS[v]
    return {"k": t["ink"], "W": t["text"] if t["mode"] == "dark" else t["paper"], "w": t["paper"], "n": t["wood"],
            "N": t["dark"], "y": t["lamp"], "r": t["red"], "g": t["grn"], "c": t["cyan"], "s": t["dim"], "m": t["pink"],
            "p": t["pink"], "b": t["night"], "e": t["lamp"], "h": t["lamp"], "f": t["lamp"]}


# ── Комната (низкое разрешение): общая для обоев и для дашборда ───────────────
# Места предметов на фоне дашборда 320×180 (QML рисует живые предметы поверх, масштаб = ширина / 320).
# Предметы рисуются в масштабе scale (2: пиксель спрайта — 2 клетки комнаты).
DASH = {"w": 320, "h": 180, "scale": 2, "window": [22, 22, 84, 64], "clock": [128, 26], "shelf": [186, 54, 118],
        "desk": [150, 116, 160], "radio": [160, 98], "plant": [214, 100], "mug": [188, 100], "lamp": [272, 102],
        "door": [112, 92, 22, 50], "floor": 142, "cat": [30, 130]}


def room_bg(t, W, H, full=False):
    """Пустая комната (стена, пол, окно, стол, полка, дверь). full — с предметами и котом (обои)."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), kit.hex2rgb(t["wall"]))
    d = ImageDraw.Draw(img)
    sx = W / DASH["w"]
    S = lambda *a: [round(x * sx) for x in a]  # noqa: E731
    fl = round(DASH["floor"] * H / DASH["h"])
    for x in range(0, W, 8):
        if (x // 8) % 2:
            d.rectangle([x, 0, x + 7, fl], fill=t["wall2"])
    d.rectangle([0, fl - 6, W, fl - 1], fill=t["wood2"])           # плинтус
    d.rectangle([0, fl, W, H], fill=t["floor"])
    for x in range(0, W, 24):
        d.line([(x, fl), (x - 10, H)], fill=t["floor2"])
    # коврик
    d.rectangle(S(40, 150, 140, 168), fill=nb.mix(t["red"], t["floor"], 0.4))
    d.rectangle(S(44, 153, 136, 165), outline=t["lamp"])
    # окно
    x, y, w, h = DASH["window"]
    d.rectangle(S(x - 4, y - 4, x + w + 4, y + h + 6), fill=t["wood"])
    d.rectangle(S(x, y, x + w, y + h), fill=t["night"])
    d.rectangle(S(x - 6, y + h + 2, x + w + 6, y + h + 6), fill=t["wood2"])   # подоконник
    if full:
        rnd = kit.Rng(5)
        for cx in range(x, x + w, 9):                                     # огни города
            hh = 10 + int(rnd() * 24)
            d.rectangle(S(cx, y + h - hh, cx + 7, y + h), fill=t["ink"])
            for yy in range(y + h - hh + 3, y + h - 2, 5):
                if rnd() < 0.35:
                    d.rectangle(S(cx + 3, yy, cx + 3, yy), fill=t["lamp"])
        if t["weather"] == "rain":
            for i in range(40):
                rx, ry = x + (i * 37) % w, y + (i * 53) % h
                d.line(S(rx, ry, rx, ry + 3), fill=t["cyan"])
    d.rectangle(S(x + w // 2 - 1, y, x + w // 2 + 1, y + h), fill=t["wood"])
    d.rectangle(S(x, y + h // 2 - 1, x + w, y + h // 2 + 1), fill=t["wood"])
    # дверь
    x, y, w, h = DASH["door"]
    d.rectangle(S(x, y, x + w, y + h), fill=t["wood"])
    d.rectangle(S(x + 3, y + 4, x + w - 3, y + 20), outline=t["dark"])
    d.rectangle(S(x + 3, y + 25, x + w - 3, y + h - 4), outline=t["dark"])
    d.rectangle(S(x + w - 5, y + 24, x + w - 3, y + 26), fill=t["lamp"])
    # полка
    x, y, w = DASH["shelf"]
    d.rectangle(S(x, y, x + w, y + 3), fill=t["wood"])
    d.rectangle(S(x + 6, y + 3, x + 8, y + 9), fill=t["dark"])
    d.rectangle(S(x + w - 8, y + 3, x + w - 6, y + 9), fill=t["dark"])
    # стол
    x, y, w = DASH["desk"]
    d.rectangle(S(x, y, x + w, y + 4), fill=t["wood"])
    d.rectangle(S(x + 4, y + 4, x + 8, DASH["floor"]), fill=t["dark"])
    d.rectangle(S(x + w - 8, y + 4, x + w - 4, DASH["floor"]), fill=t["dark"])
    if full:
        cols = sprite_colors_t(t)
        sc = max(1, round(sx * DASH["scale"]))
        # книги на полке
        bx, by, bw = DASH["shelf"]
        for i, c in enumerate([t["red"], t["grn"], t["lamp"], t["cyan"], t["pink"], t["text"], t["red"]]):
            hh = 14 - (i % 3) * 2
            d.rectangle(S(bx + 10 + i * 7, by - hh, bx + 15 + i * 7, by - 1), fill=c)
        for name, key in (("radio", "radio"), ("plant", "plant"), ("mug", "mug"), ("lamp", "lamp"), ("clock", "clock")):
            px, py = DASH[key]
            kit.draw(img, name, round(px * sx), round(py * sx), cols, sc)
        kit.draw(img, "cat-sleep", round(DASH["cat"][0] * sx), round(DASH["cat"][1] * sx), cols, sc)
        # свет лампы — дизеринг вокруг
        px = img.load()
        lx, ly = round((DASH["lamp"][0] + 7) * sx), round((DASH["lamp"][1] + 4) * sx)
        R = round(30 * sx)
        glow = kit.hex2rgb(t["lamp"])
        for yy in range(max(0, ly - R), min(H, ly + R)):
            for xx in range(max(0, lx - R), min(W, lx + R)):
                dd = math.hypot(xx - lx, yy - ly) / R * 16
                if dd < 16 and dd < kit.BAYER[yy % 4][xx % 4] + 3:
                    c = px[xx, yy]
                    px[xx, yy] = tuple(int(a + (b - a) * 0.25) for a, b in zip(c, glow))
    return img


def sprite_colors_t(t):
    return {"k": t["ink"], "W": t["text"] if t["mode"] == "dark" else t["paper"], "w": t["paper"], "n": t["wood"],
            "N": t["dark"], "y": t["lamp"], "r": t["red"], "g": t["grn"], "c": t["cyan"], "s": t["dim"], "m": t["pink"],
            "p": t["pink"], "b": t["night"], "e": t["lamp"], "h": t["lamp"], "f": t["lamp"]}


def walls(v, out_dir):
    from PIL import Image
    t = VARIANTS[v]
    os.makedirs(out_dir, exist_ok=True)
    low = room_bg(t, 320, 180, full=True)
    low.resize((320 * 9, 180 * 9), Image.NEAREST).save(os.path.join(out_dir, "1-scene.png"), optimize=True)
    kit.place_local(out_dir, t["walls"])


# ── Файлы райса поверх тем nothing ─────────────────────────────────────────

def tokens(v):
    t = VARIANTS[v]
    keys = ("wall", "wall2", "floor", "floor2", "night", "lamp", "text", "dim", "ink", "wood", "wood2", "dark", "paper",
            "paperink", "red", "grn", "cyan", "pink")
    return {"rice": "room", "variant": v, "title": t["title"], "mode": t["mode"], "weather": t["weather"],
            "font": "Pixelify Sans", "mono": "Departure Mono", "dash": DASH, **{k: t[k] for k in keys}}


def hypr_lua(v):
    t = VARIANTS[v]
    a, i = t["lamp"].lstrip("#"), t["wood2"].lstrip("#")
    return f"""-- {t['title']}: рамка окна — свет лампы, у неактивного — тёмное дерево (omarchy-themes/rices/room/build.py).
hl.config({{
	general = {{ col = {{ active_border = "rgb({a})", inactive_border = "rgb({i})" }} }},
	group = {{ col = {{ border_active = "rgb({a})", border_inactive = "rgb({i})" }} }},
}})
"""


def fastfetch_conf(v):
    t = VARIANTS[v]
    dark = t["mode"] == "dark"
    ink = t["text"] if dark else t["paperink"]
    e = lambda h: "38;2;%d;%d;%d" % kit.hex2rgb(h)  # noqa: E731
    esc = lambda h: "\x1b[%sm" % e(h)  # noqa: E731
    sw = "".join("\x1b[48;2;%d;%d;%dm   " % kit.hex2rgb(c) for c in
                 (t["dark"], t["wood"], t["red"], t["grn"], t["lamp"], t["cyan"], t["pink"], t["paper"]))
    mod = lambda typ, key, fmt=None: dict({"type": typ, "key": key}, **({"format": fmt} if fmt else {}))  # noqa: E731
    custom = lambda s: {"type": "custom", "format": s}  # noqa: E731
    conf = {
        "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
        "logo": {"type": "file-raw", "source": "~/.local/state/omarchy/current/theme/apps/room-logo.txt",
                 "padding": {"top": 1, "left": 2, "right": 4}},
        "display": {
            "separator": "  ",
            "color": {"keys": e(t["lamp"]), "title": e(ink), "output": e(ink), "separator": e(t["dim"])},
            "key": {"width": 9},
        },
        "modules": [
            custom(esc(t["lamp"]) + "☕ " + esc(ink) + "записка на холодильнике"), custom(esc(t["dim"]) + "┄" * 26),
            mod("title", "жилец", "{user-name}@{host-name}"), mod("os", "дом", "{pretty-name}"),
            mod("wm", "окна", "{pretty-name}"), mod("shell", "шёпот", "{pretty-name}"),
            mod("uptime", "дома уже"), mod("memory", "на полках", "{used} / {total}"),
            "break", custom(sw + "\x1b[0m"),
        ],
    }
    return f"// {t['title']}: omarchy-themes/rices/room/build.py\n" + json.dumps(conf, indent=2, ensure_ascii=False) + "\n"


def shelf_tile(t, dst):
    """Тайл полки для бара (скин room, texture): 32×26 клеток × 2 = 64×52 px — тень стены, доска с волокнами,
    светлая кромка и передний бортик. Тайлится по горизонтали; бар высотой 52 px."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (32, 26), kit.hex2rgb(t["wood"]))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 1], fill=t["dark"])
    rnd = kit.Rng(3)
    for y in (7, 13):
        for x in range(32):
            if rnd() < 0.55:
                d.point((x, y), fill=nb.mix(t["wood"], t["dark"], 0.45))
    for _ in range(12):
        d.point((int(rnd() * 32), 2 + int(rnd() * 17)), fill=nb.mix(t["wood"], t["dark"], 0.3))
    d.rectangle([0, 20, 31, 21], fill=nb.mix(t["wood"], "#ffffff", 0.18))
    d.rectangle([0, 22, 31, 24], fill=t["wood2"])
    d.rectangle([0, 25, 31, 25], fill=t["ink"])
    big = img.resize((64, 52), Image.NEAREST)
    big.save(dst, optimize=True)
    big.save(dst.replace(".png", "-dark.png"), optimize=True)


def sprites(v, out):
    from PIL import Image
    cols = sprite_colors(v)
    shelf_tile(VARIANTS[v], os.path.join(out, "room", "shelf.png"))
    for name in kit.ROOM:
        kit.png(name, cols, os.path.join(out, "room", name + ".png"))
    room_bg(VARIANTS[v], 320, 180).save(os.path.join(out, "room", "dash.png"), optimize=True)


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
    lines[0] = f"# {p['title']} — omarchy-rices/room (свой пиксельный райс; сборка: build.py поверх ../nothing/build.py)."
    open(f, "w").write("\n".join(lines))
    open(os.path.join(out, "hyprland.lua"), "w").write(hypr_lua(v))
    with open(os.path.join(out, "room.json"), "w") as fh:
        json.dump(tokens(v), fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    open(os.path.join(out, "apps", "room-logo.txt"), "w").write(kit.ansi_logo("cat", sprite_colors(v)))
    open(os.path.join(out, "apps", "fastfetch.jsonc"), "w").write(fastfetch_conf(v))
    sprites(v, out)
    shutil.copyfile(os.path.join(HERE, "starship.toml"), os.path.join(out, "starship.toml"))


DYNAMIC_BASE = "evening"
DYNAMIC_MODE = "dark"


def base_modes():
    return {v: VARIANTS[v]["mode"] for v in VARIANTS if v != "dynamic"}


def dynamic(s, out, name, base=DYNAMIC_BASE, scheme="wallpaper", flip=False):
    t = dict(VARIANTS[base])
    t["lamp"] = s["accent"]
    t["title"] = "Cozy Room Dynamic"
    VARIANTS["dynamic"] = t
    make("dynamic", out, name)


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if not a.startswith("--")] or list(VARIANTS):
        make(v)
