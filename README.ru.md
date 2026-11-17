# omarchy-rices

[🇬🇧 English](README.md)

Темы Omarchy девяти райсов и **динамическая тема из обоев** для каждого из них. Вкладка Customizer **«Райсы»**
применяет варианты райсов, вкладка **Dynamic** настраивает динамическую тему.

| Райс | Варианты | По мотивам |
|---|---|---|
| **Vitreus** | Retro, UwU, Cyber, Milkbox, Doodle, Paper, Proxy (Glass — динамическая тема) | [natepayn3/Vitreus](https://github.com/natepayn3/Vitreus) (MIT) |
| **Glyph** | Glyph тёмная / светлая (+ mono) | [glyph-rice](https://github.com/Nebelung-cloud/glyph-rice) (GPL-3.0) |
| Nothing (тот же генератор, `nothing/`) | Signal, CMF, Ash, Ember, Steel (+ mono), Ash Light (+ mono), Glyph White | свои |
| **yami** | Blood, Ash, Sakura, Amber, Venom, Ice, Dusk | [Trendorin/yami](https://github.com/Trendorin/yami) (MIT) |
| **Bruteon** | светлая, тёмная (+ цветные) | [Darkkal44/Bruteon](https://github.com/Darkkal44/Bruteon) (GPL-3.0) |
| **Cozytile** | Cozy, Sakura, Natura, Everforest, Carbon (+ цветные) | [Darkkal44/Cozytile](https://github.com/Darkkal44/Cozytile) (только облик) |
| **Rumda** | тёмная, светлая (+ цветные) | [hexonide/rumda](https://github.com/hexonide/rumda) (только облик) |
| **surface** | тёмная, светлая (+ цветные) | [snes19xx/surface-dots](https://github.com/snes19xx/surface-dots) (с указанием автора) |
| **Unit-3** | тёмная, Бумага | [samyns/Unit-3](https://github.com/samyns/Unit-3) (MIT) |
| **DOT-MATRIX** | DOT-MATRIX | свой |

Палитры и формы сделаны здесь заново, каждую тему генерирует `build.py` её райса поверх `nothing/build.py`.
Оригинальных обоев райсов в репозитории **нет**: `install.sh` скачивает их из исходных репо, и они остаются на условиях
своих авторов (см. [NOTICE](NOTICE)).

## Установка

С Customizer: `bash install.sh` из [omarchy-customizer](https://github.com/KamradSmeshnyavy/omarchy-customizer)
предлагает `rices` как компаньона. Вручную:

```sh
sudo pacman -S --needed python-pillow python-numpy ffmpeg
git clone https://github.com/KamradSmeshnyavy/omarchy-rices ~/.local/share/omarchy-rices
bash ~/.local/share/omarchy-rices/install.sh      # --no-build — только ссылки; --list — имена тем
```

Скрипт собирает темы, кладёт ссылки `~/.config/omarchy/themes/<райс>-<вариант>` и `~/.local/bin/omarchy-rice-dynamic`.
Существующие пути, которые не являются ссылками, он не трогает. Чтобы тема перекрашивалась при смене обоев, нужен
плагин обоев [omarchy-wallpaper-fx](https://github.com/KamradSmeshnyavy/omarchy-wallpaper-fx); без него тему
пересобирают вручную.

## Динамическая тема

`omarchy-rice-dynamic` пишет `~/.config/omarchy/themes/dynamic-<райс>` (или `dynamic` без райса) из обоев и применяет её.

```sh
omarchy-rice-dynamic build vitreus [ОБОИ]            # разовая сборка (настройки не сохраняются)
omarchy-rice-dynamic set vitreus --scheme accent --look Liquid-Retro --mode dark   # запомнить и пересобрать
omarchy-rice-dynamic build plain                     # тема dynamic из любых обоев, без райса
omarchy-rice-dynamic add vitreus КАРТИНКА… --local   # в ~/.config/omarchy/backgrounds/dynamic-vitreus/
omarchy-rice-dynamic wallhaven search vitreus "liquid abstract"   # SFW-миниатюры в кэш
omarchy-rice-dynamic wallhaven get vitreus ID…        # скачать выбранные в пул
omarchy-rice-dynamic list [РАЙС]                      # райсы и настройки или обои райса
```

- **Цвета** читает [Iris](https://github.com/Harman1307/iris) (`scripts/iris_colors.py`) — им Vitreus читает обои
  для Glass. Фон, панели, текст, акцент и красный / зелёный / жёлтый он берёт из реальных цветов картинки. У видео и
  GIF цвета берутся из представительного кадра (ffmpeg), а обои остаются живыми.
- **Режимы** (`--scheme`, `nothing/dynamic_map.py`):

  | Режим | Что делает |
  |---|---|
  | `vitreus` | в точности одиннадцать цветов Vitreus |
  | `wallpaper` / `soft` / `vivid` | обои по-Vitreus: как есть / тише / ярче |
  | `pure` / `pure-soft` / `pure-vivid` | то же, но в терминале и коде только оттенки, которые есть на картинке |
  | `mono` | один оттенок обоев |
  | `grey` | серые Vitreus |
  | `accent` | палитра варианта облика, с обоев только акцент |

- **Облик** (`--look`, пресет Customizer) — вариант, в форме которого стоит тема. Retro в цветах обоев — всё ещё Retro.
- **Светлая / тёмная** (`--mode`): `auto` — по обоям. В режиме `accent` противоположный режим переворачивает палитру
  варианта (OKLab: оттенки те же, фоны и чернила меняются светлотой).
- **Движки**: `rice` кладёт цвета в палитру райса, и его `build.py` (`dynamic()`) собирает темы всех приложений в
  характере райса. `colors` пишет только `colors.toml`, остальное делают шаблоны Omarchy. У DOT-MATRIX и `plain` —
  только `colors`.
- **Пул** обоев райса: `<райс>/wallpapers/`, `backgrounds/` всех вариантов и свои в
  `~/.config/omarchy/backgrounds/dynamic-<райс>/`.
- **Перекраска**: плагин обоев при каждой смене зовёт `omarchy-rice-dynamic on-wallpaper`. Работает один процесс,
  последний запрос побеждает, лог — в `$XDG_RUNTIME_DIR/omarchy-rice-dynamic.log`.
- **Настройки**: `~/.config/omarchy/dynamic.json`. Пресеты Customizer ищутся через `$OMARCHY_CUSTOMIZER_DIR` или
  в `~/.config/omarchy/plugins/kamradsmeshnyavy.customizer`.

## Устройство

`<райс>/build.py` содержит палитры и генерирует `<райс>/<вариант>/`. `nothing/` — общий генератор (терминалы, nvim,
helix, btop, VS Code, TUI-приложения) и палитры Glyph, в `nothing/efter/` — шаблоны из catppuccin-mocha-efter.
`originals.py` скачивает оригинальные обои райсов. В `scripts/` — `omarchy-rice-dynamic`, `wallpaper_colors.py` и
Iris.

GPL-3.0 — [LICENSE](LICENSE), сторонние части — [NOTICE](NOTICE).
