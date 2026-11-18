# Темы crt-*

[🇬🇧 English](README.md)

Темы Omarchy по мотивам стиля **Retro** из [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) (Eli Fouts) — старый
терминал с зелёным экраном (GPL-3.0). Цвета — ровно его схемы трубок (`.config/wal/colorschemes/dark/*.json`): чёрный
фон, текст — color7, акцент — color9; схема лежит в теме и файлом `tube.json`.

Трубки — его профиль по умолчанию (фильтр выключен: чёрный экран) с трубкой с его страницы COLORS:

- `crt-phosphor`, `crt-amber`, `crt-cyan`, `crt-paper`.

Его сохранённые профили (`Retro/tweaks/saved/desktop/*.json`) как есть — палитра, обои через фильтр с его настройками,
ручки ЭЛТ-шейдера:

| Тема | Палитра | Обои | Фильтр |
|---|---|---|---|
| `crt-car` | gruvbox, акцент бирюзовый | `car-03` | lines, pixel 1, 12 уровней |
| `crt-arcade` | pywal по `cat-08` | `cat-08` | palette, bayer, pixel 4, 5 уровней |
| `crt-wallpaper` | pywal по `cat-10` | `cat-10` | source, fine, pixel 2 |
| `crt-windows` | github dark dimmed | `oth-03` | source, pixel 1, 12 уровней |
| `crt-zen` | pywal по `ind-06` | `ind-06` | palette, bayer, pixel 6, 5 уровней |

Его pywal-профили делают `wal -i <обои> -n --cols16`; палитры здесь посчитаны тем же pywal16 3.8 по тем же картинкам.
Картинки — из его полной библиотеки [elifouts/wallpapers](https://github.com/elifouts/wallpapers) (без лицензии, в git
их нет): `build.py` скачивает их, держит исходник рядом с темой (`source/`, `source.json`) и фильтрует. Ручки шейдера и
настройки фильтра профиля — в его `tube.json`.
- Окна как в его `style.lua`: рамка 1 px цветом трубки (у неактивных — он же на 20 %), прямые углы, без размытия, тени
  и свечения.
- Обои трубок: `0-black.png` (его по умолчанию) и `0r-*` — картинки его профилей контурами в цвет трубки.

```sh
python3 build.py              # все
python3 build.py amber cyan   # только эти
```

## Фильтр обоев — `omarchy-crt-filter`

`filter.py`, порт его `Retro/base/wallpaper.sh` (те же вызовы ImageMagick). Прорисовывает или дизерит любую картинку в
цвет трубки текущей темы:

| `--tone` | Что делает |
|---|---|
| `lines` | контуры (canny) цветом трубки по фону — его вид по умолчанию |
| `tube` | яркость → три тона трубки с дизерингом |
| `source` | свои цвета картинки с дизерингом, приглушённые к фону |
| `palette` | картинка, сведённая к 16 цветам темы |

`--dither bayer|fine|halftone|diffuse|none`, `--pixel`, `--levels`, `--contrast`, `--bright`. Настройки: его по
умолчанию ← профиль темы (`tube.json`) ← свои для этой темы (`~/.config/omarchy/crt.json` → `themes.<тема>.filter`).
Без `-o` результат ложится в `~/.cache/omarchy/crt-wall/` (60 последних, рядом `.src` — исходник). `--set tone palette …
--apply` сохраняет свои настройки для текущей темы и пересобирает текущие обои из исходника (его `wallpaper.sh --apply`);
это делает панель настроек (Super+Alt+I → SCREEN). В пикере Retro CRT выбранная картинка показывается уже через фильтр
и ставится через него.

```sh
omarchy-crt-filter ~/Pictures/car.jpg --tone lines
```

## ЭЛТ-шейдер — `omarchy-crt-shader`

`shader.py` + `crt.frag` — его `Retro/base/crt.lua` + `crt.frag`: строки развёртки, выпуклость, свечение, зерно,
виньетка, скруглённые углы и подкраска в цвет трубки — на весь экран и все приложения. Шейдер собирается под текущую тему
в `~/.config/omarchy/customizer/shaders/retro-crt.frag`; переключатель экранного шейдера Customizer (Super+Alt+C)
включает и выключает его, стиль Retro CRT включает. Хук theme-set пересобирает его при смене темы.

```sh
omarchy-crt-shader set lines 0.5 bend 0     # свои ручки для этой темы: bend corners glow grain lines mono vignette
omarchy-crt-shader get
omarchy-crt-shader reset                    # вернуть ручки профиля
```

Пока `bend` больше 0, экран перерисовывается целиком на каждое изменение (Hyprland `damage_tracking = 1`); `bend 0`
дешевле.

## Терминал на обоях

Его виджет `term`: настоящий bash на обоях. `omarchy-desk-term` (dotfiles, порт его `desk.sh`) держит прозрачную
`kitten panel` на фоновом слое там, где стоит виджет стола «Терминал»; приглашение — его `starship.toml` (`READY >`),
он лежит в каждой теме crt. Стиль Retro CRT включает виджет.
