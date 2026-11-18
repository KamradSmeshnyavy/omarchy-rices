#!/usr/bin/python3
"""omarchy-crt-library — библиотека обоев райса Retro CRT: вся его библиотека github.com/elifouts/wallpapers (Eli Fouts;
без лицензии — в git её нет, качается к тебе) в ~/Pictures/Wallpapers/elifouts/<папка>/, его favorites.txt и индекс для
пикера SCREENS — порт его utilities/wallpaper/wallpaper-index.py (elifouts/Dotfiles, GPL-3.0): миниатюры 640×360 и
pywal-палитры (wal --cols16, если pywal16 стоит).

  omarchy-crt-library             скачать недостающее (уже лежащие файлы не трогает)
  omarchy-crt-library index       обновить ~/.cache/omarchy/crt-walls/index.json (печатает путь)
  omarchy-crt-library fav <путь>  избранное вкл / выкл (favorites.txt библиотеки)
  omarchy-crt-library path        где библиотека
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

LIBRARY = os.environ.get("CRT_WALLPAPERS", os.path.expanduser("~/Pictures/Wallpapers/elifouts"))
CACHE = os.path.expanduser("~/.cache/omarchy/crt-walls")
THUMBS = os.path.join(CACHE, "thumbs")
INDEX = os.path.join(CACHE, "index.json")
PALETTES = os.path.join(CACHE, "palettes.json")
REPO = "elifouts/wallpapers"
FAVS_URL = "https://raw.githubusercontent.com/elifouts/Dotfiles/main/wallpapers/library/favorites.txt"
EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "omarchy-crt-library"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download():
    tree = json.loads(get(f"https://api.github.com/repos/{REPO}/git/trees/HEAD?recursive=1", 60))["tree"]
    files = [t["path"] for t in tree if t["type"] == "blob" and "/" in t["path"]
             and os.path.splitext(t["path"])[1].lower() in EXT]
    todo = [p for p in files if not os.path.exists(os.path.join(LIBRARY, p))]

    def one(p):
        dst = os.path.join(LIBRARY, p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            data = get(f"https://raw.githubusercontent.com/{REPO}/HEAD/" + urllib.parse.quote(p))
        except Exception as e:  # noqa: BLE001
            return f"{p}: {e}"
        with open(dst + ".part", "wb") as f:
            f.write(data)
        os.replace(dst + ".part", dst)
        return None

    with ThreadPoolExecutor(6) as ex:
        errs = [e for e in ex.map(one, todo) if e]
    fav = os.path.join(LIBRARY, "favorites.txt")
    if not os.path.exists(fav):
        try:
            open(fav, "wb").write(get(FAVS_URL, 30))
        except Exception:  # noqa: BLE001
            open(fav, "w").close()
    for e in errs:
        print("  не скачалось:", e, file=sys.stderr)
    print(f"{len(files)} обоев в {LIBRARY} (скачано {len(todo) - len(errs)})")


def key_for(p):
    st = os.stat(p)
    return hashlib.sha1(f"{p}:{st.st_mtime_ns}:{st.st_size}".encode()).hexdigest()


def thumb(p, key):
    t = os.path.join(THUMBS, key + ".jpg")
    if not os.path.exists(t):
        tmp = t + f".{os.getpid()}.jpg"
        subprocess.run(["magick", "-define", "jpeg:size=1280x720", p + "[0]", "-auto-orient", "-thumbnail", "640x360^",
                        "-gravity", "center", "-extent", "640x360", "-quality", "85", tmp], check=True, capture_output=True)
        os.replace(tmp, t)
    return t


def palette(p):
    wal = shutil.which("wal")
    if not wal:
        return None
    d = tempfile.mkdtemp(prefix="crt-wal-")
    try:
        env = dict(os.environ, XDG_CACHE_HOME=d, XDG_CONFIG_HOME=os.path.join(d, "cfg"))
        subprocess.run([wal, "-i", p, "-n", "-s", "-t", "-e", "-q", "--cols16", "--out-dir", d],
                       env=env, check=True, capture_output=True, timeout=60)
        c = json.load(open(os.path.join(d, "colors.json")))["colors"]
        return [c[f"color{i}"].lower() for i in range(16)]
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        return None
    finally:
        shutil.rmtree(d, ignore_errors=True)


def favs():
    try:
        return {x.strip() for x in open(os.path.join(LIBRARY, "favorites.txt")) if x.strip()}
    except OSError:
        return set()


def index():
    os.makedirs(THUMBS, exist_ok=True)
    try:
        pals = json.load(open(PALETTES))
    except (OSError, ValueError):
        pals = {}
    files = sorted(os.path.join(r, f) for r, _, fs in os.walk(LIBRARY) for f in fs
                   if os.path.splitext(f)[1].lower() in EXT and os.path.dirname(os.path.join(r, f)) != LIBRARY)
    fv = favs()

    def work(p):
        k = key_for(p)
        try:
            t = thumb(p, k)
        except (subprocess.CalledProcessError, OSError):
            return None
        if k not in pals:
            c = palette(p)
            if c:
                pals[k] = c
        rel = os.path.relpath(p, LIBRARY)
        return {"path": p, "name": os.path.splitext(os.path.basename(p))[0], "theme": os.path.basename(os.path.dirname(p)),
                "fav": rel in fv, "thumb": t, "colors": pals.get(k)}

    with ThreadPoolExecutor(4) as ex:
        out = [x for x in ex.map(work, files) if x]
    for name, data in ((PALETTES, pals), (INDEX, out)):
        with open(name + ".tmp", "w") as f:
            json.dump(data, f)
        os.replace(name + ".tmp", name)
    print(INDEX)


def fav(p):
    rel = os.path.relpath(os.path.realpath(p), os.path.realpath(LIBRARY))
    fv = favs()
    fv.symmetric_difference_update({rel})
    with open(os.path.join(LIBRARY, "favorites.txt"), "w") as f:
        f.write("\n".join(sorted(fv)) + "\n")
    try:
        idx = json.load(open(INDEX))
        for w in idx:
            if os.path.realpath(w["path"]) == os.path.realpath(p):
                w["fav"] = rel in fv
        with open(INDEX + ".tmp", "w") as f:
            json.dump(idx, f)
        os.replace(INDEX + ".tmp", INDEX)
    except (OSError, ValueError):
        pass


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        download()
    elif a[0] == "index":
        index()
    elif a[0] == "fav" and len(a) > 1:
        fav(a[1])
    elif a[0] == "path":
        print(LIBRARY)
    else:
        sys.exit(__doc__)
