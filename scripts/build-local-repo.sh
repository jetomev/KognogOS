#!/usr/bin/env bash
# build-local-repo.sh — build the AUR-only KognogOS packages into a local
# pacman repo the ISO build can consume (run as regular user; makepkg
# sudo-prompts only if build deps are missing).
#
# Why: the live ISO ships nog + the Forge suite + Fresh, but those are
# AUR-only (not in any binary repo mkarchiso can reach). Standard archiso
# answer: a file:// repo baked from locally built packages, referenced by
# iso/pacman.conf as [kognog-local].
#
# Rebuild whenever one of these ships a new version, then rebuild the ISO.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/iso/local-repo"
WORK="$(mktemp -d /tmp/kognog-localrepo.XXXX)"
PKGS=(python-forgekit nog grubforge alacrittyforge fresh-editor-bin proton-ge-custom-bin)
# Ready-made programs, only repackaged: built WITHOUT installing their runtime
# dependencies on this computer (makepkg -d). Without -d, makepkg tried to
# install Walker's parts here (2026-09-30).
NODEPS_PKGS=()   # Walker + elephant left with D-40 (Noctalia); the mechanism stays for later
# Built in a clean chroot (devtools), never on this computer: their build needs
# packages we do not want installed here. hyprland-plugins needs Hyprland itself
# to build hyprbars, hypeForge's title bars (2026-09-30).
CHROOT_PKGS=(hyprland-plugins cliamp monique)
CHROOT="$REPO/iso/chroot"

mkdir -p "$OUT"
# Start from an empty repo, so an old version can never ride along next to a new one.
rm -f "$OUT"/*.pkg.tar.zst
for p in "${PKGS[@]}"; do
    echo "==> $p"
    git clone --depth 1 "https://aur.archlinux.org/$p.git" "$WORK/$p"
    ( cd "$WORK/$p" && makepkg -s --noconfirm --clean )
    cp "$WORK/$p/"*.pkg.tar.zst "$OUT/"
done

for p in "${NODEPS_PKGS[@]}"; do
    echo "==> $p (repackaged, nothing installed here)"
    git clone --depth 1 "https://aur.archlinux.org/$p.git" "$WORK/$p"
    ( cd "$WORK/$p" && makepkg -d --noconfirm --clean )
    cp "$WORK/$p/"*.pkg.tar.zst "$OUT/"
done

for p in "${CHROOT_PKGS[@]}"; do
    echo "==> $p (clean chroot)"
    command -v mkarchroot >/dev/null || { echo "!! devtools missing: nog install devtools" >&2; exit 1; }
    # mkarchroot needs the parent folder to exist, or it cannot resolve the path
    # and stops with "Please specify a working directory" (2026-09-30).
    mkdir -p "$CHROOT"
    [[ -d "$CHROOT/root" ]] || sudo mkarchroot "$CHROOT/root" base-devel
    sudo arch-nspawn "$CHROOT/root" pacman -Syu --noconfirm
    git clone --depth 1 "https://aur.archlinux.org/$p.git" "$WORK/$p"
    ( cd "$WORK/$p" && makechrootpkg -c -r "$CHROOT" )
    cp "$WORK/$p/"*.pkg.tar.zst "$OUT/"
done

# (Re)generate the repo database from everything present.
rm -f "$OUT"/kognog-local.db* "$OUT"/kognog-local.files*
repo-add "$OUT/kognog-local.db.tar.gz" "$OUT"/*.pkg.tar.zst
rm -rf "$WORK"
echo
echo "local repo ready: $OUT ($(ls "$OUT"/*.pkg.tar.zst | wc -l) packages)"
