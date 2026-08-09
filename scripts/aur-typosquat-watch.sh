#!/bin/bash
# aur-typosquat-watch.sh — Operation Ironhold B4 (2026-08-09)
#
# Watches the AUR for packages that could impersonate the Forge family:
#   1. EXACT lookalikes of our names (-bin/-git/-opt suffixes etc.) — the
#      pattern the July-Aug 2026 attack wave used for its second stage.
#      These alert LOUDLY every run until they disappear.
#   2. NEW packages matching our watch terms — delta against a known-set
#      baseline (first run seeds the baseline silently; later runs alert
#      only on additions, then absorb them).
#
# Fails gracefully when the AUR is unreachable (exit 0, log only) — it
# was built mid-freeze and must never cry wolf about downtime.
#
# Runs from a systemd --user timer (weekly). No root required.

set -u

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/aur-typosquat"
KNOWN="$STATE_DIR/known-packages.txt"
NTFY_URL="${NTFY_URL:-http://192.168.1.200:2586/aur-watch}"
RPC="https://aur.archlinux.org/rpc/v5/search"

# Our real packages — never alerted on.
OURS="nog bitlaforge grubforge alacrittyforge nogforge python-forgekit"

# Exact-name lookalikes to probe individually (the -bin trap and friends).
LOOKALIKES=""
for base in $OURS forgekit; do
    LOOKALIKES="$LOOKALIKES ${base}-bin ${base}-git ${base}-opt ${base}2"
done

# Broad watch terms for the delta scan. Deliberately narrow: bare
# "forge" matches hundreds of legit packages; the suffixed terms and the
# delta model keep noise near zero after the seed run.
TERMS="nog bitlaforge grubforge alacrittyforge forgekit nogforge"

mkdir -p "$STATE_DIR"
touch "$KNOWN"

fetch_names() {  # $1 = search term -> package names, one per line
    curl -sf --max-time 20 "$RPC/$1?by=name" \
        | python3 -c "import json,sys; [print(r['Name']) for r in json.load(sys.stdin).get('results',[])]" 2>/dev/null
}

notify() {  # $1 = title, $2 = body, $3 = priority
    curl -sf --max-time 10 -H "Title: $1" -H "Priority: ${3:-default}" \
        -d "$2" "$NTFY_URL" >/dev/null 2>&1
}

# Reachability probe — quiet exit while the AUR (or the LAN) is down.
if ! curl -sf --max-time 20 "$RPC/nog?by=name" >/dev/null 2>&1; then
    echo "$(date -Iseconds) AUR RPC unreachable — skipping (freeze or outage)"
    exit 0
fi

alerts=""

# 1. Exact lookalike probe.
for name in $LOOKALIKES; do
    hit=$(fetch_names "$name" | grep -Fx "$name")
    if [ -n "$hit" ]; then
        alerts="$alerts
⚠ EXACT lookalike live on AUR: $name  (https://aur.archlinux.org/packages/$name)"
    fi
done

# 2. Delta scan on watch terms.
scan=$(mktemp)
for term in $TERMS; do fetch_names "$term"; done | sort -u > "$scan"

if [ -s "$KNOWN" ]; then
    new=$(comm -13 "$KNOWN" "$scan" | grep -vxF -e nog -e bitlaforge -e grubforge -e alacrittyforge -e nogforge -e python-forgekit)
    if [ -n "$new" ]; then
        alerts="$alerts
New AUR packages matching Forge watch terms:
$new"
    fi
    seeded=""
else
    seeded="yes"
fi

# Absorb current scan into the baseline (seed run or post-alert).
sort -u "$KNOWN" "$scan" > "$KNOWN.tmp" && mv "$KNOWN.tmp" "$KNOWN"
rm -f "$scan"

if [ -n "$alerts" ]; then
    echo "$(date -Iseconds) ALERTS:$alerts"
    notify "AUR typosquat watch" "$alerts" high
elif [ -n "$seeded" ]; then
    echo "$(date -Iseconds) baseline seeded: $(wc -l < "$KNOWN") package names"
else
    echo "$(date -Iseconds) clean ($(wc -l < "$KNOWN") known names)"
fi
exit 0
