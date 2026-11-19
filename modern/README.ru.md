# Темы modern-*

[🇬🇧 English](README.md)

Темы Omarchy по мотивам стиля **Modern** из [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) (Eli Fouts,
GPL-3.0): тёмное матовое стекло поверх обоев, цвета из обоев (pywal), скругления, мягкая тень.

Цвета — его: 16 цветов pywal16 (`wal -i <обои> -n --cols16`, его `color-apply.sh`) или одна из его схем, роли — его
`ThemeBaseShared` (акцент color9, второй акцент 13, ok 10, caution 11, info 14, warn 1). Варианты — его сохранённые
профили:

| Тема | Цвета | Обои |
|---|---|---|
| `modern-default`, `modern-sun` | pywal | `nature/nat-09` |
| `modern-gruvbox` | gruvbox | `gruvbox/gru-04` |
| `modern-neon` | pywal | `industrial/ind-05` |
| `modern-zen` | pywal | `gruvbox/gru-07` |

Палитры pywal посчитаны pywal16 по тем же картинкам. Картинки — из его библиотеки
([elifouts/wallpapers](https://github.com/elifouts/wallpapers), без лицензии, в git нет): `~/Pictures/Wallpapers/elifouts`
(`omarchy-crt-library`) или качаются при сборке.

`omarchy-modern-colors` держит цвета отдельно от обоев, как его Settings → Themes: «Pywal» по текущим обоям или одна из
его схем и слот акцента; собирает тему `modern-live`.
