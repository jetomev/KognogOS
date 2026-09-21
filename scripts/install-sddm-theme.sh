#!/usr/bin/env bash
#
# Install the KognogOS greeter from this repo to /usr/share/sddm/themes.
#
# READ THIS FIRST: the kognogos theme is ALREADY the active one
# (/etc/sddm.conf.d/kde_settings.conf says Current=kognogos), so this
# changes your real login screen the moment it finishes. Test with
# scripts/test-sddm-theme.sh before running it.
#
# If the login screen ever comes up broken, switch back to Breeze from a
# text console -- Ctrl+Alt+F3, log in, then:
#
#   sudo sed -i 's/^Current=kognogos/Current=breeze/' \
#        /etc/sddm.conf.d/kde_settings.conf
#   sudo systemctl restart sddm
#
set -euo pipefail

SRC="$HOME/Programs/kognog/iso/airootfs/usr/share/sddm/themes/kognogos"
DST="/usr/share/sddm/themes/kognogos"

[ -d "$SRC" ] || { echo "source missing: $SRC"; exit 1; }

echo "source: $SRC"
echo "target: $DST"
echo
echo "This needs root to write into /usr/share. You will be asked for your"
echo "password. The two elevated commands are exactly:"
echo "    sudo cp -r --no-preserve=ownership \"\$SRC/.\" \"\$DST/\""
echo "    sudo chmod -R a+rX \"\$DST\""
echo

sudo cp -r --no-preserve=ownership "$SRC/." "$DST/"
sudo chmod -R a+rX "$DST"

echo "--- verifying the installed copy matches the repo ---"
ok=1
for f in Main.qml theme.conf metadata.desktop preview.png; do
    a=$(sha256sum "$SRC/$f"  | cut -d' ' -f1)
    b=$(sha256sum "$DST/$f" 2>/dev/null | cut -d' ' -f1 || echo MISSING)
    if [ "$a" = "$b" ]; then printf '  %-18s ok\n' "$f"
    else printf '  %-18s MISMATCH\n' "$f"; ok=0; fi
done
echo
if [ "$ok" -eq 1 ]; then
    echo "Installed and verified. The theme now appears in"
    echo "System Settings > Colors & Themes > Login Screen (SDDM),"
    echo "and is what you will see at the next login."
else
    echo "SOMETHING DID NOT COPY. Do not log out until this is resolved."
    exit 1
fi
