#!/usr/bin/env python3
"""Темы modern-* — по мотивам стиля Modern из github.com/elifouts/Dotfiles (GPL-3.0, Eli Fouts): тёмное матовое стекло
поверх обоев, цвета — pywal по обоям, скругления 10, мягкая тень, плавные анимации.

Цвета — как у него: 16 цветов pywal16 (`wal -i <обои> -n --cols16`, его utilities/colors/color-apply.sh) или его схема
(colorschemes/dark, ../crt/schemes), роли — его ThemeBaseShared (акцент color9, второй акцент 13, ok 10, caution 11,
info 14, warn 1). Палитры его профилей посчитаны тем же pywal16 по тем же картинкам и вписаны сюда, сборке pywal не
нужен. Варианты — его сохранённые профили (Modern/tweaks/saved/desktop/*.json):

  default — его профиль по умолчанию (pywal, nature/nat-09), sun — тот же мир с баром zen;
  gruvbox — схема gruvbox, gruvbox/gru-04;  neon — pywal, industrial/ind-05;  zen — pywal, gruvbox/gru-07.

Окна — его Modern/base/style.lua: без рамки, скругление 10, тень 15 (её даёт стиль Customizer). Обои — его библиотека
(elifouts/wallpapers, без лицензии — в git их нет: берутся из omarchy-crt-library или качаются при сборке).

  python3 build.py              все варианты
  python3 build.py neon zen     выбранные
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nothing"))
sys.path.insert(0, os.path.join(HERE, ".."))
import build as nb  # noqa: E402
import originals  # noqa: E402
from palettes import contrast, SYNTAX  # noqa: E402


def _wal(*c):
    c = [x.lower() for x in c]
    return {"special": {"background": c[0], "foreground": c[15], "cursor": c[15]},
            "colors": {f"color{i}": x for i, x in enumerate(c)}}


def _scheme(name):
    s = json.load(open(os.path.join(HERE, "..", "crt", "schemes", name + ".json")))
    return {"special": {k: v.lower() for k, v in s["special"].items()}, "colors": {k: v.lower() for k, v in s["colors"].items()}}


PALS = {
    "wal-nat-09": _wal("#0f2024", "#85523a", "#23625a", "#48675b", "#7f6f56", "#bb6b33", "#ab7047", "#929a9c", "#5e7074",
                       "#B26E4E", "#2F8379", "#608A7A", "#AA9473", "#FA8F44", "#E5965F", "#c3c7c8"),
    "wal-ind-05": _wal("#0e1721", "#243951", "#3a3958", "#214b68", "#3d3e66", "#4e476f", "#6f487d", "#91959b", "#5d6772",
                       "#314C6C", "#4E4D76", "#2C648B", "#525389", "#685F95", "#9461A7", "#c2c5c7"),
    "wal-gru-07": _wal("#1e1f25", "#605e4a", "#5a6350", "#6c6c53", "#787558", "#7d7b5c", "#878566", "#95989f", "#636779",
                       "#817E63", "#79846B", "#90916F", "#A09D76", "#A7A57B", "#B4B289", "#c6c7c8"),
}
REPO, BRANCH = "elifouts/wallpapers", "main"
LIBRARY_DIR = os.environ.get("CRT_WALLPAPERS", os.path.expanduser("~/Pictures/Wallpapers/elifouts"))
VARIANTS = {
    "default": {"title": "Modern Default", "pal": "wal-nat-09", "wall": "nature/nat-09.jpg"},
    "sun": {"title": "Modern Sun", "pal": "wal-nat-09", "wall": "nature/nat-09.jpg"},
    "gruvbox": {"title": "Modern Gruvbox", "pal": "gruvbox", "wall": "gruvbox/gru-04.jpg"},
    "neon": {"title": "Modern Neon", "pal": "wal-ind-05", "wall": "industrial/ind-05.jpg"},
    "zen": {"title": "Modern Zen", "pal": "wal-gru-07", "wall": "gruvbox/gru-07.jpg"},
}
for _v in VARIANTS.values():
    _v["tube"] = PALS.get(_v["pal"]) or _scheme(_v["pal"])
ROLES = {"accent": 9, "accent2": 13, "ok": 10, "caution": 11, "info": 14, "warn": 1}  # его ThemeBaseShared.roleSlots


def readable(c, bg, need):
    for _ in range(40):
        if contrast(c, bg) >= need:
            break
        c = nb.mix(c, "#ffffff", 0.06)
    return c


def palette(v):
    t = VARIANTS[v]
    col, sp = t["tube"]["colors"], t["tube"]["special"]
    a = [col[f"color{i}"] for i in range(16)]
    bg, fg = sp["background"], a[7]
    acc = t.get("accent") or a[t.get("acc", ROLES["accent"])]
    p = {
        "mode": "dark", "title": t["title"], "name": f"modern-{v}", "out": os.path.join(HERE, v),
        # его панели — фон на 60 % поверх размытых обоев; у тем — смесь к тексту
        "bg": bg, "panel": nb.mix(bg, fg, 0.06), "raised": nb.mix(bg, fg, 0.11), "line": nb.mix(bg, fg, 0.14),
        "fg": fg, "dim": nb.mix(fg, bg, 0.45), "comment": a[8],
        "accent": acc, "on_accent": bg, "selection": nb.mix(bg, acc, 0.3),
        "error": a[ROLES["warn"]], "info": a[ROLES["info"]], "warn": a[ROLES["caution"]], "hint": a[8], "ok": a[ROLES["ok"]],
        "diff_add": nb.mix(bg, a[10], 0.3), "diff_del": nb.mix(bg, a[9], 0.3), "diff_change": nb.mix(bg, a[12], 0.25),
        "keyword": a[13], "string": a[10], "number": a[11], "type": a[14], "function": a[12],
        "property": nb.mix(fg, a[8], 0.3), "special": acc, "constant": a[11], "ansi_yellow": a[3],
        "min_de": 0, "ansi16": a,
    }
    for role in set(SYNTAX) | {"fg", "dim", "error", "info", "warn", "ok", "special", "ansi_yellow"}:
        p[role] = readable(p[role], bg, 4.5)
    p["comment"] = readable(p["comment"], bg, 3)
    p["wallpapers"] = lambda pp, d, v=v: walls(v, d)
    return p


def walls(v, out_dir):
    """Его картинка профиля как есть — 0-original.<ext> (главная); исходник — в source.json (для пикера и цветов)."""
    os.makedirs(out_dir, exist_ok=True)
    rel = VARIANTS[v]["wall"]
    ext = os.path.splitext(rel)[1]
    dst = os.path.join(out_dir, "0-original" + ext)
    if not os.path.exists(dst):
        src = os.path.join(LIBRARY_DIR, rel)
        if not os.path.isfile(src):
            src = originals.fetch(REPO, BRANCH, rel, env="ELIFOUTS_WALLS_SRC",
                                  clone=os.path.expanduser("~/src/rice-refs/elifouts-wallpapers"))
        if not src:
            return
        shutil.copyfile(src, dst)
    theme = os.path.dirname(out_dir)
    with open(os.path.join(theme, "source.json"), "w") as f:
        json.dump({"0-original" + ext: os.path.relpath(dst, theme)}, f)
        f.write("\n")


def hypr_lua(v):
    """Его style.lua: рамка (если включат) — акцент / color5; окна без рамки, скругление и тень — стиль Customizer."""
    t = VARIANTS[v]
    c = t["tube"]["colors"]
    acc, c5 = (t.get("accent") or c["color9"]).lstrip("#"), c["color5"].lstrip("#")
    return f"""-- Modern ({t['title']}): рамка акцентом / color5, как у его style.lua (omarchy-themes/rices/modern/build.py, по elifouts/Dotfiles).
hl.config({{
	general = {{ col = {{ active_border = "rgba({acc}ff)", inactive_border = "rgba({c5}ff)" }} }},
	group = {{ col = {{ border_active = "rgba({acc}ff)", border_inactive = "rgba({c5}ff)" }} }},
}})
"""


def make(v, out=None, name=None):
    p = palette(v)
    if out:
        p["out"], p["name"] = out, name
        p.pop("wallpapers", None)
    nb.PALETTES[v] = p
    os.makedirs(p["out"], exist_ok=True)
    # wal.json — его ~/.cache/wal/colors.json: 16 цветов и роли (их читают части шелла Modern)
    with open(os.path.join(p["out"], "wal.json"), "w") as f:
        json.dump(dict(VARIANTS[v]["tube"], accent=p["accent"], title=p["title"], roles=ROLES), f, indent=1)
        f.write("\n")
    nb.build(v)
    out = p["out"]
    f = os.path.join(out, "colors.toml")
    lines = open(f).read().split("\n")
    lines[0] = f"# {p['title']} — omarchy-rices/modern (по мотивам Modern из elifouts/Dotfiles, GPL-3.0; сборка: build.py поверх ../nothing/build.py)."
    open(f, "w").write("\n".join(lines))
    open(os.path.join(out, "hyprland.lua"), "w").write(hypr_lua(v))
    import shutil
    shutil.copyfile(os.path.join(HERE, "starship.toml"), os.path.join(out, "starship.toml"))


# omarchy-rice-dynamic: тема из обоев — его pywal (`wal -i … --cols16`), без pywal — квантование как у pywal
DYNAMIC_BASE = "default"
DYNAMIC_MODE = "dark"


def base_modes():
    return {v: "dark" for v in VARIANTS if v != "dynamic"}


def dynamic(s, out, name, base=DYNAMIC_BASE, scheme="wallpaper", flip=False):
    import importlib.util
    spec = importlib.util.spec_from_file_location("crt_colors", os.path.join(HERE, "..", "crt", "colors.py"))
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)
    base = base if base in VARIANTS and base != "dynamic" else DYNAMIC_BASE
    if scheme == "accent":
        t = {"tube": VARIANTS[base]["tube"], "accent": s["accent"]}
    else:
        t = {"tube": cc.wal_palette(s.get("image", "")) or VARIANTS[base]["tube"]}
    t["title"] = "Modern Dynamic"
    VARIANTS["dynamic"] = t
    make("dynamic", out, name)


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if not a.startswith("--")] or [x for x in VARIANTS if x != "dynamic"]:
        make(v)
