#!/usr/bin/env bash
# Install the Craft apps by ArtCraft (github.com/storytold, Apache-2.0) for Javier's try-out
# (kognog TODO, board app-01; Javier, 2026-10-29: "Install the Craft Suite of Apps").
# Through nog, ready-made copies from the repositories (Chaotic-AUR): building the AUR versions
# from source would mean 13 long Rust builds. The Craft Launcher is left out on purpose: it
# updates the apps by itself, and nog keeps the updates here.
set -uo pipefail

here=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$here/logs"
log="$here/logs/craft-install-$(date +%Y%m%d-%H%M%S).log"
ln -sfn "$(basename "$log")" "$here/logs/craft-install-latest.log"

apps=(wordcraft gridcraft deckcraft pdfcraft
      photocraft vectorcraft designcraft lightcraft figcraft
      filmcraft effectcraft soundcraft cadcraft)

{
  echo "craft-install: ${#apps[@]} apps through nog, $(date)"
  nog install "${apps[@]}"
  rc=$?
  echo
  echo "installed now:"
  pacman -Q "${apps[@]}" 2>&1
  [ "$rc" -eq 0 ] && pacman -Q "${apps[@]}" >/dev/null 2>&1 && echo "OK" || echo "FAILED (nog exit $rc)"
} 2>&1 | tee "$log"
