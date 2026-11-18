# crt-* themes

[🇷🇺 Русский](README.ru.md)

Omarchy themes after the **Retro** style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) by Eli Fouts — an
old green-screen terminal (GPL-3.0). The colours are exactly his tube schemes (`.config/wal/colorschemes/dark/*.json`):
a black background, the text in color7, the accent in color9; the scheme is also saved in the theme as `tube.json`.

- `crt-phosphor` — the green phosphor tube of his default profile; the wallpaper is a black screen.
- `crt-amber` — the amber tube.
- `crt-cyan` — the cyan tube.
- `crt-paper` — the paper-white tube.
- Windows as in his `style.lua`: a 1 px border in the tube colour (inactive — the same at 20 %), square corners, no blur,
  shadow or glow.
- Wallpapers: `1-black.png` (his default) and `0r-*` — his library wallpapers run through his filter in the tube colour.
  They are someone else's art, so they are not in git: `build.py` downloads and filters them.

```sh
python3 build.py              # all
python3 build.py amber cyan   # only these
```

## Wallpaper filter — `omarchy-crt-filter`

`filter.py`, a port of his `Retro/base/wallpaper.sh` (the same ImageMagick calls). It traces or dithers any picture into
the tube colour of the current theme:

| `--tone` | What it does |
|---|---|
| `lines` | contours (canny) in the tube colour on the background — his default |
| `tube` | brightness → three tube tones with dithering |
| `source` | the picture's own colours, dithered and dimmed towards the background |
| `palette` | the picture reduced to the theme's 16 colours |

`--dither bayer|fine|halftone|diffuse|none`, `--pixel`, `--levels`, `--contrast`, `--bright`. Defaults come from
`~/.config/omarchy/crt.json` → `filter`. Without `-o` the result goes to `~/.cache/omarchy/crt-wall/` (60 newest kept).

```sh
omarchy-crt-filter ~/Pictures/car.jpg --tone lines
```

## CRT shader — `omarchy-crt-shader`

`shader.py` + `crt.frag`, his `Retro/base/crt.lua` + `crt.frag`: scanlines, bend, glow, grain, vignette, round corners
and a tint to the tube colour, over the whole screen and every app. The shader is built for the current theme into
`~/.config/omarchy/customizer/shaders/retro-crt.frag`; the Customizer's screen-shader switch (Super+Alt+C) turns it on
and off, and the Retro CRT style turns it on. The theme-set hook rebuilds it when the theme changes.

```sh
omarchy-crt-shader set lines 0.5 bend 0     # knobs: bend corners glow grain lines mono vignette
omarchy-crt-shader get
```

With `bend` above 0 the screen is redrawn whole on every change (Hyprland `damage_tracking = 1`); `bend 0` is cheaper.
