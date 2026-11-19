# modern-* themes

[🇷🇺 Русский](README.ru.md)

Omarchy themes after the **Modern** style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) by Eli Fouts
(GPL-3.0): dark frosted glass over the wallpaper, colours from the wallpaper (pywal), rounded corners, a soft shadow.

Colours are his: the 16 colours of pywal16 (`wal -i <wallpaper> -n --cols16`, his `color-apply.sh`) or one of his
schemes, with the roles of his `ThemeBaseShared` (accent color9, second accent 13, ok 10, caution 11, info 14, warn 1).
The variants are his saved profiles:

| Theme | Colours | Wallpaper |
|---|---|---|
| `modern-default`, `modern-sun` | pywal | `nature/nat-09` |
| `modern-gruvbox` | gruvbox | `gruvbox/gru-04` |
| `modern-neon` | pywal | `industrial/ind-05` |
| `modern-zen` | pywal | `gruvbox/gru-07` |

The pywal palettes were computed by pywal16 from the same pictures. The pictures come from his library
([elifouts/wallpapers](https://github.com/elifouts/wallpapers), no licence, not in git): `~/Pictures/Wallpapers/elifouts`
(`omarchy-crt-library`) or downloaded at build.

`omarchy-modern-colors` keeps colours apart from the wallpaper, like his Settings → Themes: «Pywal» of the current
wallpaper or one of his schemes, and an accent slot; it builds the theme `modern-live`.
