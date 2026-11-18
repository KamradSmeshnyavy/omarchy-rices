# Темы space-*

[🇬🇧 English](README.md)

Темы Omarchy по мотивам стиля **Space** из [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) автора Eli Fouts —
HUD в духе No Man's Sky, обои которого — шейдер пейзажа (GPL-3.0). Цвета — ровно его `World.qml`: мир — одна из его
палитр и акцент из неё, 16 цветов терминала — его `World.palette()` (color9 — акцент, color13 — цвет через четыре от него).

- `space-mars` — gruvbox, красный; его сохранённый мир *Mars* (голая красная пустыня, базы, корабли, галактика).
- `space-atlas` — nord, красный; его мир *Atlas*: Атлас вместо луны.
- `space-frost` — tokyonight, голубой; его мир *Frost* (снег, леса).
- `space-dusk` — dracula, розовый; розовый мир с его скриншотов.
- Окна как в его `style.lua`: без рамки, у активного — свечение акцентом.
- Обои — снимки его пейзажа (`1-land`, `2-ridge`, `3-camp`), рядом с каждым — `.scene.json`. С плагином обоев
  [omarchy-wallpaper-fx](https://github.com/KamradSmeshnyavy/omarchy-wallpaper-fx) пейзаж живой: панорамирует при
  смене стола. Снимки лежат в репо; недостающие `build.py` рисует через `scripts/scene-shot.qml` этого плагина (путь —
  `SCENE_SHOT`).

```sh
python3 build.py              # все
python3 build.py mars frost   # выбранные
python3 build.py --reshoot    # перерисовать снимки
```

## Дикие миры

Звёздная карта райса Space (обзор столов, Super + `) показывает вокруг неизведанные системы, у каждой свой мир — одна
из его девяти палитр (everforest, gruvbox, nord, catppuccin, tokyo night, rosé pine, dracula, kanagawa, solarized) и
акцент из неё. Посадка на такую звезду занимает свободный стол на её месте и перекрашивает рабочий стол в этот мир с
новым пейзажем: `world.py` (`install.sh` ставит его как `omarchy-space-world`) собирает
`~/.config/omarchy/themes/space-world` и снимок пейзажа с сидом звезды, потом применяет тему.

```sh
omarchy-space-world nord 8 844 3   # мир nord // cyan, сид 844, панорама на стол 3
omarchy-space-world --list         # все 54 мира
```
