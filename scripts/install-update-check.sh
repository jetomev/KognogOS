#!/usr/bin/env bash
# install-update-check.sh — install the KognogOS update snapshot service
# (run with sudo).
#
#   sudo bash scripts/install-update-check.sh
#
# Installs the refresh script and its user-scope timer. Does NOT enable
# the timer: user units are enabled by the user, not by root, and running
# `systemctl --user` under sudo would target root's own session instead of
# Javier's. The command to run afterwards is printed at the end -- the
# same install-then-activate boundary as install-greeter.sh.
#
# What this buys: the shell greeting reads a cached JSON snapshot instead
# of running `checkupdates` itself, which was costing ~1.2s of network on
# every single terminal launch.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
AIR="$REPO/iso/airootfs"

[[ -f "$AIR/usr/lib/kognog/update-check" ]] || {
    echo "sources missing: $AIR/usr/lib/kognog/update-check" >&2; exit 1; }

install -Dm755 "$AIR/usr/lib/kognog/update-check" /usr/lib/kognog/update-check
install -Dm644 "$AIR/usr/lib/systemd/user/kognog-updates.service" \
    /usr/lib/systemd/user/kognog-updates.service
install -Dm644 "$AIR/usr/lib/systemd/user/kognog-updates.timer" \
    /usr/lib/systemd/user/kognog-updates.timer
install -Dm644 "$AIR/usr/lib/systemd/user-preset/90-kognog.preset" \
    /usr/lib/systemd/user-preset/90-kognog.preset

echo "installed:"
echo "  /usr/lib/kognog/update-check"
echo "  /usr/lib/systemd/user/kognog-updates.{service,timer}"
echo "  /usr/lib/systemd/user-preset/90-kognog.preset"

if ! command -v checkupdates >/dev/null 2>&1; then
    echo
    echo "NOTE: pacman-contrib is not installed, so the service will stay"
    echo "      dormant (ConditionPathExists). Install it with:"
    echo "        nog install pacman-contrib"
fi

cat <<'EOF'

Installed but not enabled. As YOUR user (no sudo):

  systemctl --user daemon-reload
  systemctl --user enable --now kognog-updates.timer

Then check it:

  systemctl --user list-timers kognog-updates.timer
  cat ~/.cache/kognog/updates.json
EOF
