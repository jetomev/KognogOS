#!/usr/bin/env bash
# install-greeter.sh — install the KognogOS SDDM greeter (run with sudo).
#
#   sudo bash scripts/install-greeter.sh              # install only
#   sudo bash scripts/install-greeter.sh --activate   # install + make it SDDM's theme
#
# Installation is safe to repeat. Activation edits the theme name in
# /etc/sddm.conf.d/, backing up whatever it changes to /var/backups/kognog.
#
# Preview without installing anything, as a normal user:
#   sddm-greeter-qt6 --test-mode --theme iso/airootfs/usr/share/sddm/themes/kognogos
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO/iso/airootfs/usr/share/sddm/themes/kognogos"
DST=/usr/share/sddm/themes/kognogos
BACKUPS=/var/backups/kognog
CONFD=/etc/sddm.conf.d

[[ -f "$SRC/Main.qml" ]] || { echo "greeter sources missing: $SRC" >&2; exit 1; }

install -d "$DST/assets"
install -m644 "$SRC/Main.qml" "$SRC/theme.conf" "$SRC/metadata.desktop" "$DST/"
install -m644 "$SRC/assets/"* "$DST/assets/"
echo "installed greeter -> $DST"

if [[ "${1:-}" != "--activate" ]]; then
    echo
    echo "Not activated. To make it SDDM's theme, re-run with --activate."
    exit 0
fi

install -d -m755 "$BACKUPS"
stamp="$(date +%Y%m%d-%H%M%S)"

# Prefer editing the file the KDE SDDM KCM manages, so the KCM keeps
# showing the truth. sddm.conf.d files are read in alphabetical order
# with later files winning, so dropping a second file that merely
# out-sorts kde_settings.conf would leave the KCM displaying the old
# theme while a different one actually rendered.
target=""
for f in "$CONFD"/*.conf; do
    [[ -e "$f" ]] || continue
    if grep -qE '^\s*Current\s*=' "$f"; then target="$f"; break; fi
done

if [[ -n "$target" ]]; then
    install -m600 "$target" "$BACKUPS/$(basename "$target").$stamp"
    sed -i -E 's/^\s*Current\s*=.*/Current=kognogos/' "$target"
    echo "activated in $(basename "$target") (backup in $BACKUPS)"
else
    install -d "$CONFD"
    printf '[Theme]\nCurrent=kognogos\n' > "$CONFD/kognogos.conf"
    echo "activated via $CONFD/kognogos.conf"
fi

echo
grep -rE '^\s*Current\s*=' "$CONFD" || true
echo
echo "Takes effect at the next login screen. Verify BEFORE logging out:"
echo "  sddm-greeter-qt6 --test-mode --theme $DST"
