#!/usr/bin/env bash
# install-look.sh — install the KognogOS look system-wide (run with sudo).
#
# Mirrors what the future kognog-theme package will do at install time:
#   * KognogSemi wallpaper PACKAGE -> /usr/share/wallpapers/KognogSemi/
#     (Plasma resolves default wallpapers by package name — kdeglobals
#      [Wallpaper] defaultWallpaperTheme= and the LnF defaults Image= both
#      point here; a flat PNG path does NOT work for fresh desktops)
#   * all repo wallpapers -> /usr/share/wallpapers/kognog/  (slideshow dir)
#   * tier emblem        -> /usr/share/pixmaps/kognogos.png (launcher icon)
#
# skel/ configs reference these stable paths (scripts/export-plasma.py),
# so run this once on any machine that tests skel before packaging exists.
# Icons + cursors come from packages instead:
#   nog install candy-icons-git catppuccin-cursors-mocha
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEFAULT="Kognog OS Semi - Logo Catpuccin Mocha.png"   # canonical default

# Wallpaper package (metadata + sized image, Plasma package layout)
PKG=/usr/share/wallpapers/KognogSemi
install -d "$PKG/contents/images"
install -m644 "$REPO/assets/wallpapers/$DEFAULT" "$PKG/contents/images/3840x2160.png"
cat > "$PKG/metadata.json" <<'EOF'
{
    "KPlugin": {
        "Id": "KognogSemi",
        "Name": "Kognog OS Semi",
        "License": "GPL-3.0-or-later",
        "Authors": [{ "Name": "Balih Kognog" }]
    }
}
EOF

# Flat wallpaper dir (slideshow source configured in skel)
install -d /usr/share/wallpapers/kognog
install -m644 "$REPO/assets/wallpapers/"*.png /usr/share/wallpapers/kognog/
install -m644 "$REPO/assets/wallpapers/$DEFAULT" /usr/share/wallpapers/kognog/default.png

# Launcher icon (the tier emblem)
install -Dm644 "$REPO/assets/icons/kognogos.png" /usr/share/pixmaps/kognogos.png

echo "installed: KognogSemi wallpaper package, $(ls /usr/share/wallpapers/kognog | wc -l) slideshow wallpapers, launcher emblem"
