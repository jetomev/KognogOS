#!/usr/bin/env bash
# Open the KognogOS greeter in a window, straight from the repo.
#
# This runs the REAL greeter against the REAL theme files, as your own
# user, with no root and no change to the installed system. Nothing here
# can lock you out: the live login screen is untouched until the theme is
# deliberately installed.
#
# Test mode has no SDDM daemon behind it, so:
#   - "Log In" will not log you in
#   - "Restart" and "Shut Down" are correctly greyed out
# Everything else -- colours, border, shadow, both dropdowns, keyboard
# navigation -- is exactly what the login screen will do.
#
# Close it with Alt+F4, or Super then click away.

set -euo pipefail
THEME="$HOME/Programs/kognog/iso/airootfs/usr/share/sddm/themes/kognogos"

[ -d "$THEME" ] || { echo "theme not found: $THEME"; exit 1; }

echo "theme:   $THEME"
echo "greeter: $(command -v sddm-greeter-qt6)"
echo
echo "Opening. Close the window when you are done looking."
echo

exec sddm-greeter-qt6 --test-mode --theme "$THEME"
