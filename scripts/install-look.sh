#!/usr/bin/env bash
# install-look.sh — install the KognogOS look system-wide (run with sudo).
#
# Mirrors what the future kognog-theme package will do at install time:
#   * repo wallpapers -> /usr/share/wallpapers/kognog/
#   * default.png     -> the current distro default wallpaper
#
# skel/ configs point at these stable paths (scripts/export-plasma.py),
# so this must be run once on any machine that tests skel before the
# packaging exists. Icons + cursors come from packages instead:
#   nog install candy-icons-git catppuccin-cursors-mocha
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST=/usr/share/wallpapers/kognog
DEFAULT="Kognog OS Semi - Logo Catpuccin Mocha.png"   # v0.8.1 default

install -d "$DEST"
install -m644 "$REPO/assets/wallpapers/"*.png "$DEST/"
install -m644 "$REPO/assets/wallpapers/$DEFAULT" "$DEST/default.png"
echo "installed $(ls "$DEST" | wc -l) wallpapers to $DEST (default = $DEFAULT)"
