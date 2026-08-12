#!/usr/bin/env bash
# Apply the KognogOS GRUB polish pass to this machine.
#
#   1. Install the regenerated background (title raised clear of the
#      theme's countdown label at top=31%, indented to x=160).
#   2. Strip GRUB's "Loading Linux ... / Loading initial ramdisk ..."
#      echoes, which paint text on a black screen between the menu and
#      the Plymouth splash.
#   3. Regenerate grub.cfg.
#
# Entries live in /etc/grub.d/40_custom because grubForge froze them
# there with the generators disabled — see grubForge issue #19.
#
# Run:  sudo bash scripts/apply-grub-polish.sh <path-to-background.png>
set -euo pipefail

BG="${1:?usage: apply-grub-polish.sh <background.png>}"
THEME=/boot/grub/themes/kognogos
CUSTOM=/etc/grub.d/40_custom

[[ -f "$BG" ]] || { echo "no such background: $BG" >&2; exit 1; }

cp -a "$CUSTOM" "$CUSTOM.bak-$(date +%Y%m%d-%H%M%S)"
install -Dm644 "$BG" "$THEME/background.png"
echo "background installed -> $THEME/background.png"

sed -i "/^[[:space:]]*echo[[:space:]]*'Loading /d" "$CUSTOM"
echo "remaining Loading echoes: $(grep -c "echo.*'Loading " "$CUSTOM" || true)"

grub-mkconfig -o /boot/grub/grub.cfg
