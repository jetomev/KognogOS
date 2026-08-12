#!/usr/bin/env bash
# Apply the KognogOS GRUB polish pass to this machine. Idempotent —
# safe to re-run after regenerating the background.
#
#   1. Evict rogue generators from /etc/grub.d/ (see the warning below).
#   2. Drop the frozen snapshots submenu when grub-btrfs already emits one.
#   3. Install the regenerated background.
#   4. Strip GRUB's "Loading Linux ... / Loading initial ramdisk ..."
#      echoes, which paint text on a black screen between the menu and
#      the Plymouth splash.
#   5. Regenerate grub.cfg and report the entry counts.
#
# Entries live in /etc/grub.d/40_custom because grubForge froze them
# there with the generators disabled — see grubForge issue #19.
#
# Run:  sudo bash scripts/apply-grub-polish.sh <path-to-background.png>
set -euo pipefail

BG="${1:?usage: apply-grub-polish.sh <background.png>}"
THEME=/boot/grub/themes/kognogos
GRUBD=/etc/grub.d
CUSTOM="$GRUBD/40_custom"
BACKUPS=/var/backups/kognog

[[ -f "$BG" ]] || { echo "no such background: $BG" >&2; exit 1; }

install -d -m755 "$BACKUPS"

# ── 1. Rogue generators ───────────────────────────────────────────────
# grub-mkconfig executes EVERY executable file in /etc/grub.d/. A backup
# left there with the +x bit runs as a second generator and duplicates
# the entire menu. That is exactly what an earlier `cp -a "$CUSTOM"
# "$CUSTOM.bak-..."` in this script did, and grubForge could not clean it
# up because the entries were not grubForge's. Backups now go to
# $BACKUPS, and any stragglers get evicted here.
shopt -s nullglob
for f in "$GRUBD"/*.bak* "$GRUBD"/*.orig "$GRUBD"/*~ "$GRUBD"/*.dpkg-* "$GRUBD"/*.pacnew "$GRUBD"/*.pacsave; do
    mv -f "$f" "$BACKUPS/$(basename "$f")"
    echo "evicted rogue generator: $(basename "$f") -> $BACKUPS/"
done
shopt -u nullglob

install -m600 "$CUSTOM" "$BACKUPS/40_custom.$(date +%Y%m%d-%H%M%S)"

# ── 2. Frozen snapshots submenu ───────────────────────────────────────
# grubForge froze the whole generated menu into 40_custom, snapshots
# submenu included. 41_snapshots-btrfs is still executable and emits its
# own, so the submenu appears twice. Both only `configfile` the same
# grub-btrfs.cfg, so dropping the frozen copy loses nothing and keeps the
# live generator as the single source.
if [[ -x "$GRUBD/41_snapshots-btrfs" ]] && grep -q "submenu 'KognogOS snapshots'" "$CUSTOM"; then
    # Non-greedy /s, NOT [^}]* -- the body is
    # `configfile "${prefix}/grub-btrfs.cfg"`, whose ${prefix} contains a
    # closing brace, so a negated-brace class silently matches nothing.
    perl -0777 -i -pe "s/\nsubmenu 'KognogOS snapshots' \{\n.*?\n\}\n//s" "$CUSTOM"
    echo "dropped frozen snapshots submenu (41_snapshots-btrfs owns it)"
fi

# ── 3. Background ─────────────────────────────────────────────────────
install -Dm644 "$BG" "$THEME/background.png"
echo "background installed -> $THEME/background.png"

# ── 4. Loading echoes ─────────────────────────────────────────────────
sed -i "/^[[:space:]]*echo[[:space:]]*'Loading /d" "$CUSTOM"
echo "remaining Loading echoes: $(grep -c "echo.*'Loading " "$CUSTOM" || true)"

# ── 5. Regenerate + verify ────────────────────────────────────────────
grub-mkconfig -o /boot/grub/grub.cfg

echo
echo "── generated menu ──"
printf 'KognogOS entries:  %s  (expect 1)\n' \
    "$(grep -cE "^menuentry 'KognogOS'" /boot/grub/grub.cfg || true)"
printf 'Windows entries:   %s  (expect 2: Windows 11 + Recovery)\n' \
    "$(grep -cE "^menuentry 'Windows" /boot/grub/grub.cfg || true)"
printf 'Advanced submenus: %s  (expect 1)\n' \
    "$(grep -cE "^submenu 'Advanced options" /boot/grub/grub.cfg || true)"
printf 'Snapshot submenus: %s  (expect 1)\n' \
    "$(grep -cE "submenu 'KognogOS snapshots'" /boot/grub/grub.cfg || true)"
