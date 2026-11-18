# space-* themes

[🇷🇺 Русский](README.ru.md)

Omarchy themes after the **Space** style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) by Eli Fouts — a
No Man's Sky–like HUD whose wallpaper is a landscape shader (GPL-3.0). Colours are exactly those of its `World.qml`:
a world is one of its palettes plus an accent picked from it, and the 16 terminal colours are its `World.palette()`
(color9 is the accent, color13 the colour four steps after it).

- `space-mars` — gruvbox, red; its saved world *Mars* (bare red desert, bases, ships, galaxy).
- `space-atlas` — nord, red; its world *Atlas*: the Atlas instead of the moon.
- `space-frost` — tokyonight, cyan; its world *Frost* (snow, forests).
- `space-dusk` — dracula, pink; the pink world of its screenshots.
- Windows as in its `style.lua`: no border, an accent glow on the active window.
- Wallpapers — stills of its landscape (`1-land`, `2-ridge`, `3-camp`) with a `.scene.json` next to each. With the
  wallpaper plugin [omarchy-wallpaper-fx](https://github.com/KamradSmeshnyavy/omarchy-wallpaper-fx) the landscape is
  live: it pans when you switch workspaces. The stills are in the repo; `build.py` renders missing ones with that
  plugin's `scripts/scene-shot.qml` (path in `SCENE_SHOT`).

```sh
python3 build.py              # all
python3 build.py mars frost   # only these
python3 build.py --reshoot    # render the stills again
```

## Wild worlds

The star map of the Space rice (workspace overview, Super + `) shows uncharted systems around you, each with a world:
one of his nine palettes (everforest, gruvbox, nord, catppuccin, tokyo night, rosé pine, dracula, kanagawa, solarized)
and an accent from it. Landing on one takes a free workspace at that star and recolours the desktop into that world
with a fresh landscape: `world.py` (linked by `install.sh` as `omarchy-space-world`) builds
`~/.config/omarchy/themes/space-world` and a still of the landscape with the star's seed, then applies it.

```sh
omarchy-space-world nord 8 844 3   # world nord // cyan, seed 844, panned to workspace 3
omarchy-space-world --list         # all 54 worlds
```
