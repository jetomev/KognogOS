#!/usr/bin/env python3
"""export-plasma — capture the live Plasma configuration into skel/.

Phase 1 of the KognogOS v1.0 roadmap: the reference desktop (Balih's
machine) IS the distro default. This script copies a curated manifest of
KDE/Plasma config files from the running user's $HOME into the repo's
skel/ tree (which ships as /etc/skel), stripping personal residue by rule.

Deliberately reusable: the final look is frozen LATE (just before release,
with the final wallpapers) — until then this can be re-run after any
polish pass. Re-runs are full rewrites of skel/.config, so the diff shows
exactly what changed.

Sanitization rules (the weather-widget lesson — distro defaults carry no
personal data, locations, accounts, or history):
  * sections whose name matches STRIP_SECTIONS are dropped whole
  * keys matching STRIP_KEYS are dropped wherever they appear
  * wallpaper Image= lines are rewritten to the distro wallpaper path
  * any surviving line still containing /home/<user> is rewritten when a
    rule knows how, otherwise the file+line is WARNED for human review —
    the script never ships a personal path silently

Usage:  scripts/export-plasma.py            # capture into skel/
        scripts/export-plasma.py --check    # dry-run: report only
"""

import re
import shutil
import sys
from pathlib import Path

HOME = Path.home()
REPO = Path(__file__).resolve().parent.parent
SKEL = REPO / "skel"

# The distro default wallpaper as installed on target systems. Final image
# is decided at look-freeze; the path is stable so only the asset changes.
DISTRO_WALLPAPER = "/usr/share/wallpapers/kognog/default.png"

# Files that define the KognogOS face. Paths relative to $HOME; everything
# lands at the same relative path under skel/.
MANIFEST = [
    ".config/kdeglobals",
    ".config/kwinrc",
    ".config/plasmarc",
    ".config/plasmashellrc",
    ".config/plasma-org.kde.plasma.desktop-appletsrc",
    ".config/kglobalshortcutsrc",
    ".config/kcminputrc",
    ".config/kscreenlockerrc",
    ".config/krunnerrc",
    ".config/dolphinrc",
    ".config/katerc",
    ".config/konsolerc",
    ".config/kdedefaults/kcminputrc",
    ".config/kdedefaults/kdeglobals",
    ".config/kdedefaults/ksplashrc",
    ".config/kdedefaults/kwinrc",
    ".config/kdedefaults/package",
    ".config/kdedefaults/plasmarc",
    ".config/gtk-3.0/settings.ini",
    ".config/gtk-4.0/settings.ini",
    # The color scheme is a single small file — shipping it per-user via
    # skel is fine. Icons + cursors are system packages instead
    # (candy-icons-git, catppuccin-cursors-mocha — profiles.toml `theming`).
    ".local/share/color-schemes/CatppuccinMochaMauve.colors",
]

# INI sections dropped entirely (name matched case-insensitively).
STRIP_SECTIONS = re.compile(
    r"(recent|history|session:|dirselect|filedialog size|klipper)",
    re.IGNORECASE,
)

# Keys dropped wherever they appear.
STRIP_KEYS = re.compile(
    r"^(History Items|Recent(Files|URLs| Files)?|LastUsedVersion|"
    r"ViewPropsTimestamp|Version|State|WindowState|.*[Gg]eometry.*|"
    r"database|FirstRun|"
    # Personal desktop residue: user wallpaper dirs, slideshow de-selections,
    # and the desktop-icon layout (positions + file mappings are the user's)
    r"usersWallpapers|UncheckedSlides|screenMapping|itemGeometries.*"
    r")\s*[=\[]",
)

# Line-level rewrites that resolve a personal path to its distro location.
REWRITES = [
    # Wallpaper choices point at the distro wallpaper; asset lands later.
    (re.compile(r"^(Image|PreviewImage)=.*$"), lambda m: f"{m.group(1)}=file://{DISTRO_WALLPAPER}"),
    (re.compile(r"^(Wallpaper)=.*$"), lambda m: f"{m.group(1)}={DISTRO_WALLPAPER}"),
    # Slideshow mode: point at the distro wallpaper set only.
    (re.compile(r"^(SlidePaths)=.*$"), lambda m: f"{m.group(1)}=/usr/share/wallpapers/kognog/"),
]


def sanitize(text, warnings, relpath):
    out, current_section, section_dropped = [], None, False
    for line in text.splitlines():
        stripped = line.strip()
        m = re.match(r"^\[(.+)\]$", stripped)
        if m:
            current_section = m.group(1)
            section_dropped = bool(STRIP_SECTIONS.search(current_section))
            if section_dropped:
                continue
            out.append(line)
            continue
        if section_dropped:
            continue
        if STRIP_KEYS.match(stripped):
            continue
        for rx, sub in REWRITES:
            m = rx.match(stripped)
            if m:
                line = sub(m)
                break
        if str(HOME) in line:
            warnings.append(f"{relpath}: personal path survives → {line.strip()[:90]}")
        out.append(line)
    # Collapse runs of blank lines left by dropped sections.
    cleaned, blank = [], False
    for line in out:
        if line.strip() == "":
            if blank:
                continue
            blank = True
        else:
            blank = False
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def main():
    check = "--check" in sys.argv
    warnings, captured, missing = [], [], []

    if not check and (SKEL / ".config").exists():
        shutil.rmtree(SKEL / ".config")

    for rel in MANIFEST:
        src = HOME / rel
        if not src.exists():
            missing.append(rel)
            continue
        body = sanitize(src.read_text(errors="replace"), warnings, rel)
        captured.append(rel)
        if not check:
            dst = SKEL / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(body)

    mode = "CHECK (nothing written)" if check else f"captured into {SKEL}"
    print(f"export-plasma: {len(captured)} files {mode}")
    for rel in captured:
        print(f"  + {rel}")
    if missing:
        print(f"\n{len(missing)} manifest entries not present on this machine (skipped):")
        for rel in missing:
            print(f"  - {rel}")
    if warnings:
        print(f"\n⚠ {len(warnings)} lines still reference the home directory — review before shipping:")
        for w in warnings:
            print(f"  ⚠ {w}")
        sys.exit(2)
    print("\nNo personal paths survive. skel/ is shippable.")


if __name__ == "__main__":
    main()
