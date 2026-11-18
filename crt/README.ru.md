# Темы crt-*

[🇬🇧 English](README.md)

Темы Omarchy по мотивам стиля **Retro** из [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) (Eli Fouts) — старый
терминал с зелёным экраном (GPL-3.0). Цвета — ровно его схемы трубок (`.config/wal/colorschemes/dark/*.json`): чёрный
фон, текст — color7, акцент — color9; схема лежит в теме и файлом `tube.json`.

- `crt-phosphor` — зелёная фосфорная трубка его профиля по умолчанию; обои — чёрный экран.
- `crt-amber` — янтарная трубка.
- `crt-cyan` — бирюзовая трубка.
- `crt-paper` — белая «бумажная» трубка.
- Окна как в его `style.lua`: рамка 1 px цветом трубки (у неактивных — он же на 20 %), прямые углы, без размытия, тени
  и свечения.
- Обои: `1-black.png` (его по умолчанию) и `0r-*` — его обои из библиотеки, прогнанные через его фильтр в цвет трубки.
  Это чужой арт, поэтому в git их нет: `build.py` скачивает и фильтрует их.

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

`--dither bayer|fine|halftone|diffuse|none`, `--pixel`, `--levels`, `--contrast`, `--bright`. По умолчанию — из
`~/.config/omarchy/crt.json` → `filter`. Без `-o` результат ложится в `~/.cache/omarchy/crt-wall/` (60 последних).

```sh
omarchy-crt-filter ~/Pictures/car.jpg --tone lines
```

## ЭЛТ-шейдер — `omarchy-crt-shader`

`shader.py` + `crt.frag` — его `Retro/base/crt.lua` + `crt.frag`: строки развёртки, выпуклость, свечение, зерно,
виньетка, скруглённые углы и подкраска в цвет трубки — на весь экран и все приложения. Шейдер собирается под текущую тему
в `~/.config/omarchy/customizer/shaders/retro-crt.frag`; переключатель экранного шейдера Customizer (Super+Alt+C)
включает и выключает его, стиль Retro CRT включает. Хук theme-set пересобирает его при смене темы.

```sh
omarchy-crt-shader set lines 0.5 bend 0     # ручки: bend corners glow grain lines mono vignette
omarchy-crt-shader get
```

Пока `bend` больше 0, экран перерисовывается целиком на каждое изменение (Hyprland `damage_tracking = 1`); `bend 0`
дешевле.
