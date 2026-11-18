#!/usr/bin/python3
"""omarchy-crt-filter — фильтр обоев райса Retro CRT: картинка «прорисовывается» или дизерится в цвет трубки.
Порт Retro/base/wallpaper.sh из github.com/elifouts/Dotfiles (GPL-3.0, Eli Fouts) — те же вызовы ImageMagick.

Тоны (tone):
  lines    — контуры (canny) цветом трубки по фону: «чертёж», его вид по умолчанию;
  tube     — яркость → три тона трубки (фон · тёмный · акцент) с дизерингом;
  source   — цвета картинки с дизерингом, приглушённые к фону;
  palette  — цвета картинки, сведённые к 16 цветам темы.
Дизеринг (dither): bayer · fine · halftone · diffuse · none. pixel — размер «пикселя», levels — уровни,
contrast / bright — 0..1.

Цвета — из темы: по умолчанию текущей (~/.config/omarchy/current/theme/colors.toml), или --theme <каталог>.
Настройки по умолчанию — ~/.config/omarchy/crt.json → "filter" (как его settings.json → filter).

  omarchy-crt-filter <картинка> [-o out.png] [--theme dir] [--tone lines] [--dither bayer] [--pixel 2]
                     [--levels 6] [--contrast 0.5] [--bright 0.4]
Печатает путь готовой картинки (без -o — кэш ~/.cache/omarchy/crt-wall/<ключ>.png, 60 последних).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CACHE = os.path.expanduser("~/.cache/omarchy/crt-wall")
SETTINGS = os.path.expanduser("~/.config/omarchy/crt.json")
CURRENT = os.path.expanduser("~/.config/omarchy/current/theme")
DEFAULTS = {"tone": "lines", "dither": "bayer", "pixel": 2, "levels": 6, "contrast": 0.5, "bright": 0.4}


def theme_colors(d):
    """background, accent, color0..15 темы: tube.json темы crt-* (его wal-схема как есть), иначе colors.toml."""
    try:
        t = json.load(open(os.path.join(d, "tube.json")))
        return {"background": t["special"]["background"], "accent": t["accent"], **t["colors"]}
    except (OSError, ValueError, KeyError):
        pass
    s = open(os.path.join(d, "colors.toml")).read()
    v = dict(re.findall(r'^(\w+)\s*=\s*"(#[0-9a-fA-F]{6})"', s, re.M))
    c = {"background": v.get("background", "#000000"), "accent": v.get("accent", "#33ff66")}
    for i in range(16):
        if f"color{i}" in v:
            c[f"color{i}"] = v[f"color{i}"]
    # без color0..15 — по именам Omarchy
    names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    for i, n in enumerate(names):
        c.setdefault(f"color{i}", v.get(n, c["background"] if i == 0 else c["accent"]))
        c.setdefault(f"color{i + 8}", v.get("bright_" + n, c[f"color{i}"]))
    return c


def settings():
    try:
        return {**DEFAULTS, **(json.load(open(SETTINGS)).get("filter") or {})}
    except (OSError, ValueError):
        return dict(DEFAULTS)


def render(src, out, col, o):
    bg, acc, c8 = col["background"], col["accent"], col["color8"]
    pixel = max(1, int(o["pixel"]))
    levels = max(2, int(o["levels"]))
    contrast, bright = float(o["contrast"]), float(o["bright"])
    w, h = 1920 // pixel, 1080 // pixel
    sig = round(contrast * 8, 2)
    dim = int((1 - bright) * 85)
    hi = int(30 - contrast * 24)
    dith = {"bayer": ["-ordered-dither", f"o4x4,{levels}"], "fine": ["-ordered-dither", f"o8x8,{levels}"],
            "halftone": ["-ordered-dither", f"h6x6a,{levels}"],
            "diffuse": ["-dither", "FloydSteinberg", "-posterize", str(levels)]}.get(
        o["dither"], ["+dither", "-posterize", str(levels)])
    curve = [] if sig == 0 else ["-sigmoidal-contrast", f"{sig}x50%"]
    tmp = tempfile.mkdtemp(prefix="crt-filter-")
    try:
        tone = o["tone"]
        if tone == "lines":
            body = ["-colorspace", "gray", "-blur", "0x1", "-canny", f"0x1+{hi // 3}%+{hi}%",
                    "(", f"xc:{bg}", "(", f"xc:{acc}", "-fill", bg, "-colorize", f"{dim}%", ")", "+append",
                    "-resize", "256x1!", ")", "-clut"]
        elif tone == "source":
            body = curve + dith + ["-fill", bg, "-colorize", f"{dim}%"]
        elif tone == "palette":
            pal = os.path.join(tmp, "palette.png")
            subprocess.run(["magick"] + [f"xc:{x}" for x in [bg] + [col[f"color{i}"] for i in range(1, 9)] + [acc]]
                           + ["+append", pal], check=True)
            d = ["+dither"] if o["dither"] == "none" else ["-dither", "FloydSteinberg"]
            body = curve + ["-fill", bg, "-colorize", f"{dim}%"] + d + ["-remap", pal]
        else:  # tube
            body = ["-colorspace", "gray", "-contrast-stretch", "2%x1%"] + curve + dith + \
                   ["(", f"xc:{bg}", f"xc:{c8}", "(", f"xc:{acc}", "-fill", bg, "-colorize", f"{dim}%", ")",
                    "+append", "-resize", "256x1!", ")", "-clut"]
        part = os.path.join(tmp, "out.png")
        subprocess.run(["magick", src + "[0]", "-auto-orient", "-resize", f"{w}x{h}^"] + body +
                       ["-filter", "point", "-resize", f"{pixel}00%", "-strip", part], check=True)
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        shutil.move(part, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="фильтр обоев Retro CRT")
    ap.add_argument("src")
    ap.add_argument("-o", "--out")
    ap.add_argument("--theme", default=CURRENT)
    for k, v in DEFAULTS.items():
        ap.add_argument("--" + k, type=type(v))
    a = ap.parse_args()
    if not shutil.which("magick"):
        sys.exit("omarchy-crt-filter: нужен ImageMagick (magick)")
    if not os.path.isfile(a.src):
        sys.exit(f"omarchy-crt-filter: нет файла {a.src}")
    o = settings()
    for k in DEFAULTS:
        if getattr(a, k) is not None:
            o[k] = getattr(a, k)
    col = theme_colors(a.theme)
    out = a.out
    if not out:
        key = json.dumps([os.path.realpath(a.src), os.stat(a.src).st_mtime, col, o], sort_keys=True)
        out = os.path.join(CACHE, hashlib.md5(key.encode()).hexdigest()[:16] + ".png")
    if not os.path.exists(out) or a.out:
        render(a.src, out, col, o)
        if not a.out:
            old = sorted((os.path.join(CACHE, f) for f in os.listdir(CACHE) if f.endswith(".png")),
                         key=os.path.getmtime, reverse=True)[60:]
            for f in old:
                os.unlink(f)
    print(out)


if __name__ == "__main__":
    main()
