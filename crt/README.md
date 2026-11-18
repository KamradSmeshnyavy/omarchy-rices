# crt-* themes

[🇷🇺 Русский](README.ru.md)

Omarchy themes after the **Retro** style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) by Eli Fouts — an
old green-screen terminal (GPL-3.0). The colours are exactly his tube schemes (`.config/wal/colorschemes/dark/*.json`):
a black background, the text in color7, the accent in color9; the scheme is also saved in the theme as `tube.json`.

Tubes — his default profile (filter off: a black screen) with a tube from his COLORS page:

- `crt-phosphor`, `crt-amber`, `crt-cyan`, `crt-paper`.

His saved profiles (`Retro/tweaks/saved/desktop/*.json`) as they are — palette, wallpaper through the filter with his
settings, the CRT knobs:

| Theme | Palette | Wallpaper | Filter |
|---|---|---|---|
| `crt-car` | gruvbox, accent aqua | `car-03` | lines, pixel 1, 12 levels |
| `crt-arcade` | pywal of `cat-08` | `cat-08` | palette, bayer, pixel 4, 5 levels |
| `crt-wallpaper` | pywal of `cat-10` | `cat-10` | source, fine dither, pixel 2 |
| `crt-windows` | github dark dimmed | `oth-03` | source, pixel 1, 12 levels |
| `crt-zen` | pywal of `ind-06` | `ind-06` | palette, bayer, pixel 6, 5 levels |

His pywal profiles run `wal -i <wallpaper> -n --cols16`; the palettes here were computed by the same pywal16 3.8 from the
same pictures. The pictures are from his full library [elifouts/wallpapers](https://github.com/elifouts/wallpapers) (no
licence, so not in git): `build.py` downloads them, keeps the source next to the theme (`source/`, `source.json`) and
filters it. The CRT knobs and the filter settings of a profile are in its `tube.json`.
- Windows as in his `style.lua`: a 1 px border in the tube colour (inactive — the same at 20 %), square corners, no blur,
  shadow or glow.
- Wallpapers of the tubes: `0-black.png` (his default) and `0r-*` — his profile pictures traced in the tube colour.

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

`--dither bayer|fine|halftone|diffuse|none`, `--pixel`, `--levels`, `--contrast`, `--bright`. Settings: his defaults ←
the profile of the theme (`tube.json`) ← your own for this theme (`~/.config/omarchy/crt.json` → `themes.<theme>.filter`).
Without `-o` the result goes to `~/.cache/omarchy/crt-wall/` (60 newest kept, `.src` next to each — its source).
`--set tone palette … --apply` saves your settings for the current theme and rebuilds the current wallpaper from its
source (his `wallpaper.sh --apply`); the Settings sheet (Super+Alt+I → SCREEN) does that. In the Retro CRT picker the
selected picture is shown already filtered and is set filtered.

```sh
omarchy-crt-filter ~/Pictures/car.jpg --tone lines
```

## CRT shader — `omarchy-crt-shader`

`shader.py` + `crt.frag`, his `Retro/base/crt.lua` + `crt.frag`: scanlines, bend, glow, grain, vignette, round corners
and a tint to the tube colour, over the whole screen and every app. The shader is built for the current theme into
`~/.config/omarchy/customizer/shaders/retro-crt.frag`; the Customizer's screen-shader switch (Super+Alt+C) turns it on
and off, and the Retro CRT style turns it on. The theme-set hook rebuilds it when the theme changes.

```sh
omarchy-crt-shader set lines 0.5 bend 0     # your knobs for this theme: bend corners glow grain lines mono vignette
omarchy-crt-shader get
omarchy-crt-shader reset                    # back to the profile's knobs
```

With `bend` above 0 the screen is redrawn whole on every change (Hyprland `damage_tracking = 1`); `bend 0` is cheaper.

## Terminal on the wallpaper

His `term` widget: a real bash on the wallpaper. `omarchy-desk-term` (dotfiles, a port of his `desk.sh`) keeps a
transparent `kitten panel` on the background layer where the desktop widget «Terminal» stands; the prompt is his
`starship.toml` (`READY >`), shipped in every crt theme. The Retro CRT style turns the widget on.
