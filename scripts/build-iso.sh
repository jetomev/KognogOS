#!/usr/bin/env bash
# build-iso.sh — stage the KognogOS identity into the archiso profile and
# build the ISO. Run as regular user; mkarchiso itself is invoked via sudo.
#
# Staging (before every build, so repo sources stay canonical):
#   skel/                 -> airootfs/etc/skel  AND  airootfs/home/liveuser
#   config/nog.conf       -> airootfs/etc/nog/
#   config/tier-pins.toml -> airootfs/etc/nog/
#   config/pacman.conf    -> airootfs/etc/pacman.conf   (the BOOTED system's;
#                            the build-time iso/pacman.conf is separate)
#   config/nanorc         -> airootfs/etc/nanorc
#   config/sudoers-kognog -> airootfs/etc/sudoers.d/10-kognog
#   wallpapers + emblem   -> airootfs/usr/share/... (mirrors install-look.sh)
#
# Work dir lives ON DISK under iso/work (NOT /tmp — it's a 16G tmpfs and a
# Plasma airootfs would eat it). iso/work + iso/out are gitignored.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
ISO="$REPO/iso"
AIR="$ISO/airootfs"
DEFAULT_WP="Kognog OS Semi - Logo Catpuccin Mocha.png"

[[ -f "$ISO/local-repo/kognog-local.db.tar.gz" ]] || {
    echo "!! local repo missing — run scripts/build-local-repo.sh first" >&2
    exit 1
}

echo "==> staging skel"
rm -rf "$AIR/etc/skel" "$AIR/home/liveuser"
mkdir -p "$AIR/etc" "$AIR/home"
cp -r "$REPO/skel" "$AIR/etc/skel"
cp -r "$REPO/skel" "$AIR/home/liveuser"
# Live session only: Chrome cannot ride the ISO, so the default-browser
# references swap to Brave (installed systems keep Chrome — installforge
# fetches it with consent).
for d in "$AIR/etc/skel" "$AIR/home/liveuser"; do
    sed -i 's/google-chrome.desktop/brave-browser.desktop/g' \
        "$d/.config/mimeapps.list" "$d/.config/kdeglobals"
done

echo "==> staging system configs"
mkdir -p "$AIR/etc/nog" "$AIR/etc/sudoers.d"
cp "$REPO/config/nog.conf"       "$AIR/etc/nog/nog.conf"
cp "$REPO/config/tier-pins.toml" "$AIR/etc/nog/tier-pins.toml"
cp "$REPO/config/pacman.conf"    "$AIR/etc/pacman.conf"
cp "$REPO/config/nanorc"         "$AIR/etc/nanorc"
cp "$REPO/config/sudoers-kognog" "$AIR/etc/sudoers.d/10-kognog"

echo "==> staging the look"
PKG="$AIR/usr/share/wallpapers/KognogSemi"
mkdir -p "$PKG/contents/images" "$AIR/usr/share/wallpapers/kognog" "$AIR/usr/share/pixmaps"
cp "$REPO/assets/wallpapers/$DEFAULT_WP" "$PKG/contents/images/3840x2160.png"
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
cp "$REPO/assets/wallpapers/"*.png "$AIR/usr/share/wallpapers/kognog/"
cp "$REPO/assets/wallpapers/$DEFAULT_WP" "$AIR/usr/share/wallpapers/kognog/default.png"
cp "$REPO/assets/icons/kognogos.png" "$AIR/usr/share/pixmaps/kognogos.png"
cp "$REPO/assets/icons/plymouth-spinner.png" "$AIR/usr/share/pixmaps/kognogos-spinner.png"
install -Dm644 "$REPO/assets/icons/kognogos.png" "$AIR/usr/share/icons/hicolor/256x256/apps/kognogos.png"
install -Dm644 "$REPO/config/os-release" "$AIR/usr/share/kognog/os-release"

echo "==> staging plymouth theme assets"
PLY="$AIR/usr/share/plymouth/themes/kognog"
cp "$REPO/assets/icons/kognogos.png"        "$PLY/logo.png"
cp "$REPO/assets/icons/plymouth-spinner.png" "$PLY/spinner.png"

echo "==> building ISO (sudo mkarchiso)"
# mkarchiso caches completed steps in the work dir and silently SKIPS them
# on rerun — a stale work dir means a sub-second "build" that changes
# nothing (learned live, 2026-07-30). Always start clean.
sudo rm -rf "$ISO/work"
mkdir -p "$ISO/work" "$ISO/out"
sudo rm -f "$ISO/out/"kognogos-*.iso
sudo mkarchiso -v -w "$ISO/work" -o "$ISO/out" "$ISO"
echo
ls -lh "$ISO/out/"
