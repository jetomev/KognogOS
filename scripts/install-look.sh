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
#   * Plymouth theme     -> /usr/share/plymouth/themes/kognog/
#   * Plasma splash      -> /usr/share/plasma/look-and-feel/org.kognogos.splash/
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
        "Authors": [{ "Name": "Javier (jetomev)" }]
    }
}
EOF

# Flat wallpaper dir (slideshow source configured in skel)
install -d /usr/share/wallpapers/kognog
install -m644 "$REPO/assets/wallpapers/"*.png /usr/share/wallpapers/kognog/
install -m644 "$REPO/assets/wallpapers/$DEFAULT" /usr/share/wallpapers/kognog/default.png

# Launcher icon (the tier emblem) + the splash spinner
install -Dm644 "$REPO/assets/icons/kognogos.png" /usr/share/pixmaps/kognogos.png
install -Dm644 "$REPO/assets/icons/plymouth-spinner.png" /usr/share/pixmaps/kognogos-spinner.png

# Distro identity: os-release content + the self-healing pacman hook
# (Arch's filesystem package owns /usr/lib/os-release and would revert the
# identity on every upgrade; the hook restores it post-transaction).
install -Dm644 "$REPO/config/os-release" /usr/share/kognog/os-release
install -Dm644 "$REPO/iso/airootfs/etc/pacman.d/hooks/kognog-os-release.hook" \
    /etc/pacman.d/hooks/kognog-os-release.hook
cp /usr/share/kognog/os-release /usr/lib/os-release
install -Dm644 "$REPO/assets/icons/kognogos.png" \
    /usr/share/icons/hicolor/256x256/apps/kognogos.png

# Boot identity — the two screens that bracket login. Both draw from the
# SAME logo.png/spinner.png so the pre-login and post-login screens read
# as one system. Deliberately does NOT touch mkinitcpio, the kernel
# cmdline or GRUB: those are per-machine and belong to installforge
# (KognogOS issue #2), not to a look installer.
install -d /usr/share/plymouth/themes/kognog
install -m644 "$REPO/iso/airootfs/usr/share/plymouth/themes/kognog/"* \
    /usr/share/plymouth/themes/kognog/

SPLASH=/usr/share/plasma/look-and-feel/org.kognogos.splash
install -d "$SPLASH/contents/splash/images"
install -m644 "$REPO/iso/airootfs/usr/share/plasma/look-and-feel/org.kognogos.splash/metadata.json" "$SPLASH/"
install -m644 "$REPO/iso/airootfs/usr/share/plasma/look-and-feel/org.kognogos.splash/contents/splash/Splash.qml" \
    "$SPLASH/contents/splash/"
install -m644 "$REPO/iso/airootfs/usr/share/plasma/look-and-feel/org.kognogos.splash/contents/splash/images/"* \
    "$SPLASH/contents/splash/images/"

echo "installed: KognogSemi wallpaper package, $(ls /usr/share/wallpapers/kognog | wc -l) slideshow wallpapers, launcher emblem, Plymouth theme, Plasma splash"
echo
echo "Boot identity is installed but not yet ACTIVE. Per machine:"
echo "  plymouth-set-default-theme kognog && mkinitcpio -P"
echo "  kwriteconfig6 --file ksplashrc --group KSplash --key Theme org.kognogos.splash"
echo "  (plus 'splash' on the kernel cmdline -- see KognogOS issue #2)"
