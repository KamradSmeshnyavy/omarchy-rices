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

Цвета — из темы: по умолчанию текущей (~/.local/state/omarchy/current/theme/colors.toml), или --theme <каталог>.
Настройки: его по умолчанию ← профиль темы (tube.json → filter) ← свои (~/.config/omarchy/crt.json → filter).

  omarchy-crt-filter <картинка> [-o out.png] [--theme dir] [--tone lines] [--dither bayer] [--pixel 2]
                     [--levels 6] [--contrast 0.5] [--bright 0.4]
Печатает путь готовой картинки (без -o — кэш ~/.cache/omarchy/crt-wall/<ключ>.png, 60 последних; рядом .src — исходник).

  omarchy-crt-filter --get                       настройки фильтра текущей темы (JSON, on — включён)
  omarchy-crt-filter --set tone palette … [--apply]  свои настройки для текущей темы; --apply — пересобрать обои
  omarchy-crt-filter --apply                     пересобрать текущие обои из их исходника
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
CURRENT = os.path.expanduser("~/.local/state/omarchy/current/theme")
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


def theme_name():
    try:
        return open(os.path.expanduser("~/.local/state/omarchy/current/theme.name")).read().strip()
    except OSError:
        return ""


def load_user():
    try:
        return json.load(open(SETTINGS))
    except (OSError, ValueError):
        return {}


def profile(theme):
    try:
        return dict(json.load(open(os.path.join(theme, "tube.json"))).get("filter") or {})
    except (OSError, ValueError):
        return {}


def settings(theme, user=True):
    """Настройки фильтра: его по умолчанию ← профиль темы (tube.json → filter) ← свои для текущей темы
    (crt.json → themes.<тема>.filter; пишет --set). Ключ on — фильтр включён (у профилей с обоями — да)."""
    o = dict(DEFAULTS, on=False)
    o.update({k: v for k, v in profile(theme).items() if k in o})
    if user and os.path.realpath(theme) == os.path.realpath(CURRENT):
        o.update({k: v for k, v in (((load_user().get("themes") or {}).get(theme_name()) or {}).get("filter") or {}).items() if k in o})
    return o


def source_of(path):
    """Исходник картинки: у кэша фильтра — <out>.src, у обоев темы crt-* — source.json темы; иначе — она сама."""
    real = os.path.realpath(path)
    try:
        return open(real + ".src").read().strip() or real
    except OSError:
        pass
    try:
        bg = os.path.dirname(real)
        src = json.load(open(os.path.join(os.path.dirname(bg), "source.json"))).get(os.path.basename(real))
        if src:
            return os.path.join(os.path.dirname(bg), src)
    except (OSError, ValueError):
        pass
    return real


def apply_current():
    """Пересобрать текущие обои по настройкам (его wallpaper.sh --apply): фильтр включён — из исходника через фильтр,
    выключен — сам исходник."""
    cur = os.path.expanduser("~/.local/state/omarchy/current/background")
    src = source_of(cur)
    if not os.path.isfile(src):
        sys.exit("omarchy-crt-filter: не нашёл исходник текущих обоев")
    o = settings(CURRENT)
    out = filtered(src, CURRENT, o) if o["on"] else src
    if os.path.realpath(out) != os.path.realpath(cur):
        subprocess.run(["omarchy-theme-bg-set", out])
    print(out)


def filtered(src, theme, o, out=None):
    col = theme_colors(theme)
    keep = out
    if not out:
        key = json.dumps([os.path.realpath(src), os.stat(src).st_mtime, col, {k: o[k] for k in DEFAULTS}], sort_keys=True)
        out = os.path.join(CACHE, hashlib.md5(key.encode()).hexdigest()[:16] + ".png")
    if not os.path.exists(out) or keep:
        render(src, out, col, o)
        if not keep:
            with open(out + ".src", "w") as f:
                f.write(os.path.realpath(src))
            old = sorted((os.path.join(CACHE, f) for f in os.listdir(CACHE) if f.endswith(".png")),
                         key=os.path.getmtime, reverse=True)[60:]
            for f in old:
                os.unlink(f)
                if os.path.exists(f + ".src"):
                    os.unlink(f + ".src")
    return out


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
    if sys.argv[1:2] == ["--get"]:
        print(json.dumps(settings(CURRENT)))
        return
    if sys.argv[1:2] == ["--set"]:
        # --set k v … [--apply]: свои настройки фильтра текущей темы, затем пересобрать обои
        args = [x for x in sys.argv[2:] if x != "--apply"]
        u = load_user()
        f = u.setdefault("themes", {}).setdefault(theme_name(), {}).setdefault("filter", {})
        for k, v in zip(args[::2], args[1::2]):
            if k == "on":
                f[k] = v in ("1", "true", "True")
            elif k in ("tone", "dither"):
                f[k] = v
            elif k in DEFAULTS:
                f[k] = type(DEFAULTS[k])(float(v))
        os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
        with open(SETTINGS + ".tmp", "w") as fh:
            json.dump(u, fh, indent=1)
        os.replace(SETTINGS + ".tmp", SETTINGS)
        if "--apply" in sys.argv:
            apply_current()
        return
    if sys.argv[1:2] == ["--apply"]:
        apply_current()
        return
    ap = argparse.ArgumentParser(description="фильтр обоев Retro CRT")
    ap.add_argument("src")
    ap.add_argument("-o", "--out")
    ap.add_argument("--theme", default=CURRENT)
    ap.add_argument("--no-settings", action="store_true", help="без своих настроек из crt.json (сборка тем)")
    for k, v in DEFAULTS.items():
        ap.add_argument("--" + k, type=type(v))
    a = ap.parse_args()
    if not shutil.which("magick"):
        sys.exit("omarchy-crt-filter: нужен ImageMagick (magick)")
    if not os.path.isfile(a.src):
        sys.exit(f"omarchy-crt-filter: нет файла {a.src}")
    o = settings(a.theme, not a.no_settings)
    for k in DEFAULTS:
        if getattr(a, k) is not None:
            o[k] = getattr(a, k)
    print(filtered(a.src, a.theme, o, a.out))


if __name__ == "__main__":
    main()
