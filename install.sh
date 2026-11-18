#!/usr/bin/env bash
# omarchy-rices: Omarchy themes of the rices (Vitreus, Glyph, yami, Bruteon, Cozytile, Rumda, surface, Unit-3,
# Space, DOT-MATRIX) and the dynamic theme from the wallpaper (omarchy-rice-dynamic).
#
#   bash install.sh             build the themes (downloads the rices' original wallpapers), link them, link the script
#   bash install.sh --no-build  only the links (themes as they are in the repo)
#   bash install.sh --list      print "theme-name<TAB>path" of every theme and exit
#
# Links: ~/.config/omarchy/themes/<rice>-<variant> → <repo>/<rice>/<variant> (DOT-MATRIX: dot-matrix),
#        ~/.local/bin/omarchy-rice-dynamic, ~/.local/bin/omarchy-space-world (wild worlds of the Space star map).
#        A path that exists and is not a link is never touched.
# The Customizer (github.com/KamradSmeshnyavy/omarchy-customizer) shows the rices and the Dynamic tab;
# the wallpaper plugin (omarchy-wallpaper-fx) recolours the dynamic theme on every wallpaper change.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
themes="$HOME/.config/omarchy/themes"
bin="$HOME/.local/bin"
rices=(vitreus unit3 space yami bruteon cozytile rumda surface nothing)

list() {
  [[ -f $here/dot-matrix/colors.toml ]] && printf 'dot-matrix\t%s\n' "$here/dot-matrix"
  local r v
  for r in "${rices[@]}"; do
    for v in "$here/$r"/*/; do
      v=${v%/}
      [[ -f $v/colors.toml ]] && printf '%s-%s\t%s\n' "$r" "$(basename "$v")" "$v"
    done
  done
}

build=1
case ${1:-} in
--list) list; exit 0 ;;
--no-build) build=0 ;;
-h | --help) sed -n '2,13p' "$0"; exit 0 ;;
"") ;;
*) echo "unknown option: $1" >&2; exit 1 ;;
esac

# The generators and Iris need Pillow and NumPy of the system Python (mise / pyenv ones usually lack them),
# live wallpapers — ffmpeg.
if ! /usr/bin/python3 -c 'import PIL, numpy' 2>/dev/null; then
  echo "Needs Pillow and NumPy for /usr/bin/python3:  sudo pacman -S --needed python-pillow python-numpy ffmpeg" >&2
  exit 1
fi
command -v ffmpeg >/dev/null || echo "• ffmpeg not found: live (video / GIF) wallpapers will not give colours" >&2

if ((build)); then
  for r in "${rices[@]}"; do
    echo "• building $r …"
    (cd "$here/$r" && /usr/bin/python3 build.py >/dev/null) || echo "  $r: build failed — the themes in the repo stay" >&2
  done
fi

link() { # target link
  if [[ -L $2 ]]; then
    ln -sfn "$1" "$2"
  elif [[ -e $2 ]]; then
    echo "• $2 exists and is not a link — skipping" >&2
  else
    ln -s "$1" "$2"
  fi
}

mkdir -p "$themes" "$bin"
n=0
while IFS=$'\t' read -r name path; do
  link "$path" "$themes/$name"
  n=$((n + 1))
done < <(list)
link "$here/scripts/omarchy-rice-dynamic" "$bin/omarchy-rice-dynamic"
link "$here/space/world.py" "$bin/omarchy-space-world"
echo "Done: $n themes in $themes, omarchy-rice-dynamic and omarchy-space-world in $bin."
case ":$PATH:" in *":$bin:"*) ;; *) echo "• add $bin to PATH" >&2 ;; esac
