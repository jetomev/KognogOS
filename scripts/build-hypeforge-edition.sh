#!/usr/bin/env bash
# build-hypeforge-edition.sh — build the KognogOS hypeForge edition ISO in one go
# (hypeForge D-37). Run it yourself in a terminal: it asks for your password,
# and the ISO step may ask which package to use for a few things; press Enter
# to take the default each time.
#
#   1. the local package repo (nog, the Forge apps, Walker, the title bars …)
#   2. the ISO itself
#
# Everything it prints is also saved to logs/build-<date>.log, and
# logs/build-latest.log always points at the newest one. When you say
# "done", Claude reads that file; no pasting needed. The last line says
# BUILD FINISHED OK, or the log stops at the error.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$REPO/logs"
LOG="$REPO/logs/build-$(date +%Y%m%d-%H%M).log"
ln -sfn "$(basename "$LOG")" "$REPO/logs/build-latest.log"
{
    echo "== 1 of 2 · local package repo"
    bash "$REPO/scripts/build-local-repo.sh"
    echo "== 2 of 2 · the ISO"
    bash "$REPO/scripts/build-iso.sh"
    echo "== BUILD FINISHED OK"
} 2>&1 | tee "$LOG"
echo "Log saved: $LOG"
