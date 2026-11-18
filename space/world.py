#!/usr/bin/python3
"""omarchy-space-world — мир дикой системы звёздной карты Space (по мотивам World.qml / Overview.qml из
github.com/elifouts/Dotfiles, GPL-3.0, Eli Fouts: посадка на неизведанную звезду перекрашивает рабочий стол в её мир
и пересобирает землю с новым сидом).

Мир — одна из его девяти палитр (build.THEMES) и акцент 3..8 из неё. Тема пишется в
~/.config/omarchy/themes/space-world (как dynamic-*: собирается заново, руками не править), обои — свежий снимок пейзажа
с сидом звезды и рядом .scene.json — плагин обоев рисует по нему живую сцену.

  omarchy-space-world <тема> <акцент 3..8> <сид> [стол] [--no-apply]
  omarchy-space-world --list          миры: тема, акцент, цвет акцента, палитра (для карты)
  omarchy-space-world --preview <тема> <акцент> <сид>   снимок пейзажа 320×200 в кэш (путь — в stdout)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
# space/build.py сам импортирует ../nothing/build.py как build — свой грузим под другим именем
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("space_build", os.path.join(HERE, "build.py"))
sb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sb)

NAME = "space-world"
THEMES_DIR = os.path.expanduser("~/.config/omarchy/themes")
MARKER = ".space-world.json"
CURRENT = os.path.expanduser("~/.local/state/omarchy/current/theme.name")
CACHE = os.path.expanduser("~/.cache/omarchy/space-worlds")


def die(msg):
    print(f"omarchy-space-world: {msg}", file=sys.stderr)
    sys.exit(1)


def title(theme, acc):
    return f"{sb.THEME_NAMES[theme]} // {sb.ACCENT_NAMES[acc]}"


def build(theme, acc, seed, ws=1):
    if theme not in sb.THEMES:
        die(f"нет мира {theme} (есть: {', '.join(sb.THEMES)})")
    if not 3 <= acc <= 8:
        die("акцент — 3..8")
    sb.VARIANTS["world"] = {"title": "Space " + title(theme, acc), "theme": theme, "acc": acc, "land": {}}
    target = os.path.join(THEMES_DIR, NAME)
    if os.path.islink(target) or (os.path.exists(target) and not os.path.exists(os.path.join(target, MARKER))):
        die(f"{target} создан не этим скриптом — не трогаю")
    os.makedirs(THEMES_DIR, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix=f".{NAME}-", dir=THEMES_DIR)
    try:
        os.chmod(tmp, 0o755)
        sb.make("world", tmp, NAME)
        # снимок: имя со сидом — новое у каждого мира, иначе omarchy-theme-bg-set решит, что обои те же
        stem = f"1-world-{seed}"
        sb.SHOTS = [(stem, seed, ws)]
        sb.walls("world", os.path.join(tmp, "backgrounds"))
        jpg = os.path.join(tmp, "backgrounds", stem + ".jpg")
        if not os.path.exists(jpg):
            die("снимок пейзажа не получился (нужен плагин обоев kamradsmeshnyavy.background)")
        info = {"theme": theme, "acc": acc, "seed": seed, "title": title(theme, acc)}
        with open(os.path.join(tmp, MARKER), "w") as f:
            json.dump(info, f, ensure_ascii=False)
        # копия маркера без точки: omarchy-theme-set копирует её в current/theme — так карта видит, какой мир стоит
        with open(os.path.join(tmp, "world.json"), "w") as f:
            json.dump(info, f, ensure_ascii=False)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    old = None
    if os.path.exists(target):
        old = target + f".old-{os.getpid()}"
        os.rename(target, old)
    os.rename(tmp, target)
    if old:
        shutil.rmtree(old)
    return os.path.join(target, "backgrounds", stem + ".jpg")


def apply(image):
    # обои ставим сами: omarchy-theme-set той же темы иначе перешёл бы на следующие
    env = dict(os.environ, OMARCHY_THEME_SKIP_BACKGROUND="1")
    try:
        same = open(CURRENT).read().strip() == NAME
    except OSError:
        same = False
    if same:
        env["OMARCHY_DYNAMIC_RECOLOR"] = "1"
    subprocess.run(["omarchy-theme-set", NAME], check=True, env=env)
    subprocess.run(["omarchy-theme-bg-set", image], check=False)


def preview(theme, acc, seed):
    """Мини-снимок мира для карточки звёздной карты: кэш по (тема, акцент, сид), рисуется один раз."""
    if theme not in sb.THEMES or not 3 <= acc <= 8:
        die("нет такого мира")
    os.makedirs(CACHE, exist_ok=True)
    jpg = os.path.join(CACHE, f"{theme}-{acc}-{seed}.jpg")
    if os.path.exists(jpg):
        return jpg
    sb.VARIANTS["world"] = {"title": title(theme, acc), "theme": theme, "acc": acc, "land": {}}
    png = jpg[:-4] + f".{os.getpid()}.png"
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="rhi", QSG_RHI_BACKEND="opengl",
               QT_SCALE_FACTOR="1")
    qml = "/usr/lib/qt6/bin/qml" if os.path.exists("/usr/lib/qt6/bin/qml") else "qml6"
    subprocess.run([qml, sb.SHOT, "--", json.dumps(sb.scene("world", seed, 1)), png, "320", "200"], env=env,
                   timeout=60, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(png):
        die("снимок не получился")
    from PIL import Image
    Image.open(png).convert("RGB").save(jpg, quality=88)
    os.unlink(png)
    return jpg


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--list" in sys.argv:
        print(json.dumps([{"theme": t, "acc": i, "color": c[i], "bg": c[0], "fg": c[1], "palette": c, "title": title(t, i)}
                          for t, c in sb.THEMES.items() for i in range(3, 9)], ensure_ascii=False))
        return
    if "--preview" in sys.argv:
        print(preview(a[0], int(a[1]), int(a[2])))
        return
    if len(a) < 3:
        die("omarchy-space-world <тема> <акцент 3..8> <сид> [стол] [--no-apply]")
    image = build(a[0], int(a[1]), int(a[2]), int(a[3]) if len(a) > 3 else 1)
    print(f"{NAME}: {title(a[0], int(a[1]))}, seed {a[2]}")
    if "--no-apply" not in sys.argv:
        apply(image)


if __name__ == "__main__":
    main()
