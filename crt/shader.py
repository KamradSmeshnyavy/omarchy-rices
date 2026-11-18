#!/usr/bin/python3
"""omarchy-crt-shader — ЭЛТ-шейдер райса Retro CRT под текущую тему. Порт Retro/base/crt.lua + crt.frag из
github.com/elifouts/Dotfiles (GPL-3.0, Eli Fouts): его шейдер, в который подставлены #define — цвет трубки (акцент
темы) и ручки: профиль темы (tube.json → crt, у тем crt-* — его сохранённые профили) и свои для темы
(~/.config/omarchy/crt.json → themes.<тема>, пишет `set`).

Готовый шейдер пишется в ~/.config/omarchy/customizer/shaders/retro-crt.frag — Customizer (scripts/crt-toggle.sh,
Super+Alt+C) находит его по имени retro-crt раньше копии в плагине. Если шейдер сейчас включён — применяется заново.

  omarchy-crt-shader                      собрать под текущую тему (хук theme-set)
  omarchy-crt-shader set lines 0.5 …      поменять ручки текущей темы (bend corners glow grain lines mono vignette)
  omarchy-crt-shader reset                вернуть ручки профиля темы
  omarchy-crt-shader get                  ручки JSON-ом
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
SETTINGS = os.path.expanduser("~/.config/omarchy/crt.json")
THEME = os.path.expanduser("~/.local/state/omarchy/current/theme")
OUT = os.path.expanduser("~/.config/omarchy/customizer/shaders/retro-crt.frag")
STATE = os.path.join(os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state")), "hypr/screen-shader")
# его Retro/tweaks/default-look.json → desktop.crt
DEFAULTS = {"bend": 1, "corners": 0.65, "glow": 0.5, "grain": 0.25, "lines": 0.35, "mono": 0.5, "vignette": 0}


def load():
    try:
        return json.load(open(SETTINGS))
    except (OSError, ValueError):
        return {}


def theme_name():
    try:
        return open(os.path.expanduser("~/.local/state/omarchy/current/theme.name")).read().strip()
    except OSError:
        return ""


def knobs():
    """Ручки: его по умолчанию ← профиль темы (tube.json → crt) ← свои для этой темы (crt.json → themes.<тема>)."""
    c = dict(DEFAULTS)
    try:
        c.update({k: v for k, v in (json.load(open(os.path.join(THEME, "tube.json"))).get("crt") or {}).items() if k in DEFAULTS})
    except (OSError, ValueError):
        pass
    c.update({k: v for k, v in ((load().get("themes") or {}).get(theme_name()) or {}).items() if k in DEFAULTS})
    return c


def tint():
    try:
        return json.load(open(os.path.join(THEME, "tube.json")))["accent"]
    except (OSError, ValueError, KeyError):
        pass
    try:
        m = re.search(r'^accent\s*=\s*"(#[0-9a-fA-F]{6})"', open(os.path.join(THEME, "colors.toml")).read(), re.M)
        return m.group(1) if m else "#33ff66"
    except OSError:
        return "#33ff66"


def source(c, hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    bend = float(c["bend"]) * 0.08
    defs = ("#define TINT vec3(%.3f, %.3f, %.3f)\n#define MONO %.2f\n#define LINES %.2f\n#define GLOW %.2f\n"
            "#define VIGNETTE %.2f\n#define GRAIN %.3f\n#define BEND %.3f\n#define CURVED %d\n#define ROUND %.3f\n") % (
        r, g, b, c["mono"], c["lines"], c["glow"], c["vignette"], float(c["grain"]) * 0.06, bend,
        1 if bend > 0 else 0, c["corners"])
    tpl = open(os.path.join(HERE, "crt.frag")).read()
    return tpl.replace("// defs\n", defs)


def hypr(path, dt):
    subprocess.run(["hyprctl", "eval", f'hl.config({{ decoration = {{ screen_shader = "{path}" }}, '
                    f'debug = {{ damage_tracking = {dt} }} }})'], capture_output=True)


def build():
    c = knobs()
    src = source(c, tint())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    try:
        if open(OUT).read() == src:
            return
    except OSError:
        pass
    with open(OUT + ".tmp", "w") as f:
        f.write(src)
    os.replace(OUT + ".tmp", OUT)
    # включён — Hyprland перечитает шейдер, только если путь сменится: сначала пусто, потом снова он
    try:
        cur = open(STATE).read().split()
    except OSError:
        cur = []
    if cur and os.path.basename(cur[0]) == "retro-crt.frag":
        dt = 1 if float(c["bend"]) > 0 else 2
        hypr("", 2)
        hypr(OUT, dt)
        with open(STATE, "w") as f:
            f.write(f"{OUT} {dt}\n")


def main(a):
    if a[:1] == ["get"]:
        print(json.dumps(knobs()))
        return
    if a[:1] == ["set"]:
        s = load()
        th = s.setdefault("themes", {})
        c = dict(th.get(theme_name()) or {})
        for k, v in zip(a[1::2], a[2::2]):
            if k not in DEFAULTS:
                sys.exit(f"omarchy-crt-shader: нет ручки {k} (есть: {' '.join(DEFAULTS)})")
            c[k] = float(v)
        th[theme_name()] = c
        os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
        with open(SETTINGS + ".tmp", "w") as f:
            json.dump(s, f, indent=1)
        os.replace(SETTINGS + ".tmp", SETTINGS)
    if a[:1] == ["reset"]:
        s = load()
        (s.get("themes") or {}).pop(theme_name(), None)
        with open(SETTINGS + ".tmp", "w") as f:
            json.dump(s, f, indent=1)
        os.replace(SETTINGS + ".tmp", SETTINGS)
    build()


if __name__ == "__main__":
    main(sys.argv[1:])
