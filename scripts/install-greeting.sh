#!/usr/bin/env bash
# install-greeting.sh — install the KognogOS shell greeting (run with sudo).
#
#   sudo bash scripts/install-greeting.sh
#
# Two halves:
#   system  /usr/share/kognog/kognogos.ansi   pre-rendered emblem panel
#   user    ~/.config/fish/sysinfo.py         the greeting itself
#           ~/.config/fish/conf.d/kognog-prompt.fish   prompt identity
#
# The user half is written into the INVOKING user's home, not root's --
# under sudo $HOME is root's, and copying there would leave the greeting
# installed for an account nobody logs into.
#
# The update snapshot this greeting reads comes from a separate service;
# install it with scripts/install-update-check.sh if you have not already.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"

[[ -f "$REPO/assets/icons/kognogos.ansi" ]] || {
    echo "emblem panel missing -- run: python3 scripts/make-emblem-ansi.py" >&2
    exit 1; }

install -Dm644 "$REPO/assets/icons/kognogos.ansi" /usr/share/kognog/kognogos.ansi
echo "installed /usr/share/kognog/kognogos.ansi"

who="${SUDO_USER:-${USER:-root}}"
home="$(getent passwd "$who" | cut -d: -f6)"
group="$(id -gn "$who")"
fish="$home/.config/fish"

[[ -n "$home" && -d "$home" ]] || { echo "cannot resolve home for $who" >&2; exit 1; }

install -o "$who" -g "$group" -Dm644 "$REPO/config/sysinfo.py" "$fish/sysinfo.py"
install -o "$who" -g "$group" -Dm644 \
    "$REPO/skel/.config/fish/conf.d/kognog-prompt.fish" \
    "$fish/conf.d/kognog-prompt.fish"
echo "installed $fish/sysinfo.py"
echo "installed $fish/conf.d/kognog-prompt.fish  (for user $who)"

echo
echo "Open a NEW terminal to see it. The prompt icon changes too."
if [[ ! -f "$home/.cache/kognog/updates.json" ]]; then
    echo
    echo "NOTE: no update snapshot yet -- the status line will say so."
    echo "      Install and enable it with:"
    echo "        sudo bash scripts/install-update-check.sh"
fi
