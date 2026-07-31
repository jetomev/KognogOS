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
PKGS=(nog grubforge alacrittyforge fresh-editor-bin proton-ge-custom-bin)

mkdir -p "$OUT"
for p in "${PKGS[@]}"; do
    echo "==> $p"
    git clone --depth 1 "https://aur.archlinux.org/$p.git" "$WORK/$p"
    ( cd "$WORK/$p" && makepkg -s --noconfirm --clean )
    cp "$WORK/$p/"*.pkg.tar.zst "$OUT/"
done

# (Re)generate the repo database from everything present.
rm -f "$OUT"/kognog-local.db* "$OUT"/kognog-local.files*
repo-add "$OUT/kognog-local.db.tar.gz" "$OUT"/*.pkg.tar.zst
rm -rf "$WORK"
echo
echo "local repo ready: $OUT ($(ls "$OUT"/*.pkg.tar.zst | wc -l) packages)"
