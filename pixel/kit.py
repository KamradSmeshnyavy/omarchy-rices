"""Общий набор пиксельных райсов (quest, cozy, handheld, fantasy): спрайты из строковых карт, логотип fastfetch
полублоками, сцены-обои, обои пользователя из ~/Wallpapers и фильтр картинки под палитру темы.

Спрайт — список строк одинаковой длины; буква — роль цвета, «.» — прозрачно. Роли красит словарь {буква: "#hex"}.
"""
import os
import shutil

# ── Спрайты ──────────────────────────────────────────────────────────────
# Роли: k контур, W белый, w светлый, s сталь, h золото, r красный, b синий (цвет окна), e глаза, g зелёный,
# c голубой, y жёлтый, n коричневый, m пурпур, f пламя, o оранжевый.
SPRITES = {
    "hero": [
        ".......rr.......",
        "......rrk.......",
        ".....kkkkk......",
        "....ksssssk.....",
        "....kssssssk....",
        "....kskkkksk....",
        "....ksweweskk...",
        "....kssssssk.h..",
        "...kkbbbbbkk.hW.",
        "..kssbbhbbssk.h.",
        "..ksbbbbbbbsk.h.",
        "..kskbbbbbksk.h.",
        "...kkbbbbbkk.khk",
        "....kssksskk..k.",
        "....kssk.ssk....",
        "...kkkk..kkkk...",
    ],
    "heart": [".rr.rr.", "rWrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."],
    "hand": [".kkkk....", "kWWWWkkkk", "kWWWWWWWk", "kWWWWkkkk", "kWWWWk...", ".kkkk...."],
    "potion": ["..nnn..", "...k...", "..kWk..", ".kmmmk.", "kmWmmmk", "kmmmmmk", "kmmmmmk", ".kkkkk."],
    "sword": ["......W", ".....Ws", "....Ws.", "...Ws..", "h.Ws...", ".hs....", "nkh....", "n..h..."],
    "chest": [".kkkkkkkk.", "knnnnnnnnk", "knhhhhhhnk", "kkkkhhkkkk", "knnnhhnnnk", "knnnnnnnnk",
              "knnnnnnnnk", ".kkkkkkkk."],
    "torch": ["..f..", ".fyf.", ".fyf.", "..f..", ".nnn.", "..n..", "..n..", "..n..", "..n.."],
    "skull": [".kkkkk.", "kWWWWWk", "kWkWkWk", "kWWWWWk", ".kWkWk.", "..kkk.."],
    "star": ["..y..", "..y..", "yyyyy", ".yyy.", "y...y"],
}


def size(name):
    rows = SPRITES[name]
    return max(len(r) for r in rows), len(rows)


def pixels(name):
    """[(x, y, буква)] непрозрачных клеток."""
    return [(x, y, ch) for y, row in enumerate(SPRITES[name]) for x, ch in enumerate(row) if ch != "."]


def draw(img, name, x0, y0, colors, scale=1):
    """Рисует спрайт на PIL-картинке (RGB) в точке x0, y0; colors — {буква: "#hex"}."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    for x, y, ch in pixels(name):
        c = colors.get(ch)
        if c:
            d.rectangle([x0 + x * scale, y0 + y * scale, x0 + (x + 1) * scale - 1, y0 + (y + 1) * scale - 1], fill=c)


def png(name, colors, dst, scale=1):
    """Спрайт отдельным PNG с прозрачным фоном (иконки оболочки, unlock)."""
    from PIL import Image
    w, h = size(name)
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw(img, name, 0, 0, colors, scale)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    img.save(dst, optimize=True)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ansi_logo(name, colors, pad=0):
    """Логотип fastfetch: спрайт полублоками ▀ / ▄ (две клетки спрайта — одна строка терминала), truecolor."""
    w, h = size(name)
    grid = {(x, y): colors.get(ch) for x, y, ch in pixels(name)}
    rows = []
    for y in range(0, h + (h % 2), 2):
        line = " " * pad
        for x in range(w):
            a, b = grid.get((x, y)), grid.get((x, y + 1))
            if a is None and b is None:
                line += "\x1b[0m "
            elif b is None:
                line += "\x1b[0m\x1b[38;2;%d;%d;%dm▀" % hex2rgb(a)
            elif a is None:
                line += "\x1b[0m\x1b[38;2;%d;%d;%dm▄" % hex2rgb(b)
            else:
                line += "\x1b[38;2;%d;%d;%dm\x1b[48;2;%d;%d;%dm▀" % (hex2rgb(a) + hex2rgb(b))
        rows.append(line + "\x1b[0m")
    return "\n".join(rows) + "\n"


# ── Холст сцены: рисуем в низком разрешении, увеличиваем без сглаживания ─────
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
LOW_W, LOW_H, SCALE = 320, 200, 9      # 320×200 × 9 = 2880×1800 (16:10, как у остальных райсов)


class Rng:
    """Детерминированный шум: одна и та же сцена при каждой сборке."""

    def __init__(self, seed):
        self.s = seed or 1

    def __call__(self):
        self.s = (self.s * 16807) % 2147483647
        return self.s / 2147483647


def canvas(color="#000000"):
    from PIL import Image
    return Image.new("RGB", (LOW_W, LOW_H), hex2rgb(color))


def dither_v(img, top, bottom, y0, y1):
    """Вертикальный переход двух цветов дизерингом Байера между y0 и y1 (и сплошной bottom ниже)."""
    px = img.load()
    a, b = hex2rgb(top), hex2rgb(bottom)
    for y in range(y0, LOW_H):
        t = min(1.0, max(0.0, (y - y0) / max(1, y1 - y0))) * 16
        for x in range(LOW_W):
            px[x, y] = b if t > BAYER[y % 4][x % 4] else a


def save_scene(img, dst):
    from PIL import Image
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    img.resize((LOW_W * SCALE, LOW_H * SCALE), Image.NEAREST).save(dst, optimize=True)


# ── Обои пользователя: из ~/Wallpapers (в git их нет — чужой арт без лицензии) ──
WALLS = os.environ.get("PIXEL_WALLS", os.path.expanduser("~/Wallpapers"))


def place_local(out_dir, items):
    """items: [(имя без расширения, файл в ~/Wallpapers)]. Первое — 0-original (обои темы по умолчанию), остальные —
    0r-<имя>. Нет файла — пропускаем молча (у другого пользователя своих обоев нет, останутся сцены генератора)."""
    os.makedirs(out_dir, exist_ok=True)
    placed = 0
    for i, (stem, rel) in enumerate(items):
        src = os.path.join(WALLS, rel)
        if not os.path.isfile(src):
            continue
        name = ("0-original" if i == 0 else f"0r-{stem}") + os.path.splitext(rel)[1].lower()
        dst = os.path.join(out_dir, name)
        if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src):
            placed += 1
            continue
        shutil.copyfile(src, dst)
        placed += 1
    return placed


def quantize(src, dst, palette, pixel=3, dither=0.19, tones=False):
    """Картинка под палитру темы: уменьшение в pixel раз, дизеринг Байера, ближайший цвет палитры, увеличение.
    tones=True — по яркости в цвета палитры по порядку (тёмный → светлый), как экран карманной консоли."""
    import numpy as np
    from PIL import Image
    im = Image.open(src)
    im.seek(0)
    im = im.convert("RGB")
    im = im.resize((2880, round(im.height * 2880 / im.width)), Image.LANCZOS)
    small = im.resize((im.width // pixel, im.height // pixel), Image.BOX)
    a = np.asarray(small, dtype=float)
    h, w, _ = a.shape
    B = (np.array(BAYER) / 16 - 0.5)[np.arange(h)[:, None] % 4, np.arange(w)[None, :] % 4]
    P = np.array([hex2rgb(c) for c in palette], dtype=float)
    if tones:
        lum = (a @ [0.299, 0.587, 0.114]) / 255
        idx = (np.clip(lum + B * dither * 1.7, 0, 0.999) * len(palette)).astype(int)
    else:
        a = a + B[..., None] * dither * 255
        idx = ((a[:, :, None, :] - P[None, None]) ** 2).sum(-1).argmin(-1)
    out = Image.fromarray(P[idx].astype("uint8"))
    out.resize((w * pixel, h * pixel), Image.NEAREST).save(dst, optimize=True)
