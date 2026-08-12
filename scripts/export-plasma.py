#!/usr/bin/env python3
"""export-plasma — capture the live Plasma configuration into skel/.

Phase 1 of the KognogOS v1.0 roadmap: the reference desktop (Javier's
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

# Whole directories copied verbatim (upstream theme content — no personal
# data inside, no sanitization pass). The active LookAndFeel package
# (kdeglobals LookAndFeelPackage=) is user-local, so it must travel.
MANIFEST_DIRS = [
    ".local/share/plasma/look-and-feel/Catppuccin-Mocha-Mauve",
    # Referenced by the LnF defaults (window decoration) — user-local, 136K
    ".local/share/aurorae/themes/CatppuccinMocha-Modern",
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
    # Cursor theme: Javier switched to Breeze (2026-07-31, "don't like the
    # Catppuccin" cursors) — ships with Plasma, no extra package. Any stale
    # Catppuccin reference in captured layers normalizes to it.
    (re.compile(r"^(cursorTheme)=Catppuccin-Mocha-Mauve-Cursors$"),
     lambda m: f"{m.group(1)}=breeze_cursors"),
    # Application Launcher icon: the KognogOS tier emblem on every panel.
    # (distributor-logo-windows was the pre-distro placeholder; either it
    # or a hand-picked stand-in may appear across the per-screen panels.)
    (re.compile(r"^icon=(distributor-logo-windows|applications-all)$"),
     lambda m: "icon=/usr/share/pixmaps/kognogos.png"),
]

# Pinned-launcher substitutions applied inside filter_launchers, for when the
# distro default differs from the reference machine. Currently empty: Dolphin
# is the default file manager again (Javier, 2026-08-01 — Nemo misbehaved under
# KDE and was dropped; still searching for a keeper).
LAUNCHER_SWAPS = {}

# Launchers never shipped even if resolvable on the reference machine:
# apps whose licenses keep them off the ISO (fetched at install instead).
LAUNCHER_DROPS = {
    "spotify.desktop",
    "google-chrome.desktop",
    "visual-studio-code.desktop",
    "code.desktop",
}


def filter_launchers(line, dropped):
    """Keep only panel launchers every fresh install can resolve:
    preferred:// URIs and .desktop entries present in /usr/share/applications.
    User-local launchers (Chrome web-app shims, Lutris game entries, personal
    shortcuts) are the user's, not the distro's — dropped and reported."""
    key, _, value = line.partition("=")
    kept = []
    for entry in value.split(","):
        raw = entry.strip()
        if raw in LAUNCHER_SWAPS:
            # Distro-decided substitution: guaranteed by profiles.toml,
            # exempt from the local-existence check (the reference machine
            # may not have the package installed).
            kept.append(LAUNCHER_SWAPS[raw])
            continue
        if raw.startswith("preferred://"):
            kept.append(raw)
            continue
        name = raw.removeprefix("applications:")
        if name in LAUNCHER_DROPS:
            dropped.add(name + " (license-excluded from ISO)")
        elif (Path("/usr/share/applications") / name).exists():
            kept.append(raw)
        else:
            dropped.add(name)
    return f"{key}={','.join(kept)}"


def sanitize(text, warnings, relpath, dropped_launchers):
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
        if stripped.startswith("launchers="):
            out.append(filter_launchers(stripped, dropped_launchers))
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


def patch_lnf_defaults():
    """Distro-ize the LookAndFeel package's defaults after copying.

    On a fresh account Plasma cannot match the shipped desktop containment
    (it is bound to an Activity UUID that does not exist yet), so it builds
    a new desktop from the ACTIVE LookAndFeel package's `defaults` — which
    is therefore the authoritative place for the default wallpaper. Also
    rewrite the cursor theme to the system package's name (the user-local
    copy is 6.5M and identical content under a different name)."""
    path = (SKEL / ".local/share/plasma/look-and-feel/"
            "Catppuccin-Mocha-Mauve/contents/defaults")
    if not path.exists():
        return
    text = path.read_text()
    text = text.replace(
        "cursorTheme=Catppuccin-Mocha-Mauve-Cursors",
        "cursorTheme=breeze_cursors",
    )
    if "[Wallpaper]" not in text:
        # Wallpaper PACKAGE name (like Breeze's `Image=Next`) — Plasma does
        # not resolve flat file paths here.
        text = text.rstrip() + "\n\n[Wallpaper]\nImage=KognogSemi\n"
    path.write_text(text)
    print("  ~ patched LnF defaults (wallpaper package + packaged cursor theme)")

    # Fresh desktops also consult kdeglobals for the default wallpaper theme.
    kg = SKEL / ".config/kdeglobals"
    if kg.exists() and "[Wallpaper]" not in kg.read_text():
        with kg.open("a") as f:
            f.write("\n[Wallpaper]\ndefaultWallpaperTheme=KognogSemi\n")
        print("  ~ ensured kdeglobals [Wallpaper] defaultWallpaperTheme=KognogSemi")


# Identity markers every shippable skel must carry. Verified after capture
# so a bad export can never leave the repo silently.
IDENTITY_CHECKS = [
    # Plasma 6 inlines the effective color scheme into kdeglobals as
    # [Colors:*] sections (the name lives in kdedefaults) — assert both.
    (".config/kdeglobals", "[Colors:View]"),
    (".config/kdeglobals", "BackgroundNormal=30, 30, 46"),  # Mocha base
    (".config/kdedefaults/kdeglobals", "ColorScheme=CatppuccinMochaMauve"),
    (".config/kdeglobals", "LookAndFeelPackage=Catppuccin-Mocha-Mauve"),
    (".config/kdeglobals", "Theme=candy-icons"),
    (".local/share/plasma/look-and-feel/Catppuccin-Mocha-Mauve/contents/defaults",
     "Image=KognogSemi"),
    (".config/kdeglobals", "defaultWallpaperTheme=KognogSemi"),
    (".config/plasma-org.kde.plasma.desktop-appletsrc",
     "icon=/usr/share/pixmaps/kognogos.png"),
    (".config/plasma-org.kde.plasma.desktop-appletsrc",
     "applications:org.kde.dolphin.desktop"),
    (".config/mimeapps.list", "inode/directory=org.kde.dolphin.desktop"),
    (".config/fish/functions/fish_greeting.fish", "sysinfo.py"),
    (".config/fish/conf.d/_tide_init.fish", None),
    (".config/fish/fish_plugins", "ilancosman/tide"),
    (".config/mimeapps.list", "x-scheme-handler/https=google-chrome.desktop"),
    (".config/alacritty/alacritty.toml", "program = \"/usr/bin/fish\""),
    (".config/kdedefaults/ksplashrc", "org.kognogos.splash"),
    (".local/share/plasma/look-and-feel/Catppuccin-Mocha-Mauve/metadata.json", None),
    (".local/share/color-schemes/CatppuccinMochaMauve.colors", None),
    (".local/share/aurorae/themes/CatppuccinMocha-Modern/metadata.json", None),
    (".config/plasma-org.kde.plasma.desktop-appletsrc", "launchers="),
]


def verify_skel():
    failures = []
    for rel, needle in IDENTITY_CHECKS:
        path = SKEL / rel
        if not path.exists():
            failures.append(f"missing: {rel}")
        elif needle and needle not in path.read_text(errors="replace"):
            failures.append(f"{rel}: expected `{needle}`")
    if failures:
        print("\n✗ IDENTITY CHECK FAILED — skel is NOT shippable:")
        for f in failures:
            print(f"  ✗ {f}")
        sys.exit(1)
    print(f"\n✓ identity check passed ({len(IDENTITY_CHECKS)} markers) — "
          "the KognogOS face is in the skel")


def ensure_terminal_stack():
    """The KognogOS terminal experience, from repo-canonical sources
    (config/ in the repo, NOT captured from the reference home): Alacritty
    config, fish config, and the sysinfo.py welcome box the greeting runs.
    Discovered missing during the first live-ISO test (Javier, 2026-07-30:
    'fish installed, not our setup') — the files existed in config/ since
    April but nothing ever shipped them."""
    fish = SKEL / ".config/fish"
    fish.mkdir(parents=True, exist_ok=True)
    (SKEL / ".config/alacritty").mkdir(parents=True, exist_ok=True)
    # The prompt suite is the REFERENCE MACHINE's working fisher setup
    # (tide v6 + autopair + fzf.fish + sponge + catppuccin theme, all MIT/
    # open) — captured live so the shipped shell IS the developed shell
    # (Javier, 2026-07-31: "rescue that").
    src = HOME / ".config/fish"
    for d in ("functions", "conf.d", "completions", "themes"):
        if (src / d).exists():
            shutil.copytree(src / d, fish / d, dirs_exist_ok=True)
    for f in ("config.fish", "fish_plugins", "fish_variables"):
        if (src / f).exists():
            shutil.copy(src / f, fish / f)
    # (fish_variables<suffix> atomic-write temp files never ship)
    shutil.copy(REPO / "config/sysinfo.py", fish / "sysinfo.py")
    shutil.copy(REPO / "config/fish_greeting.fish",
                fish / "functions/fish_greeting.fish")
    shutil.copy(REPO / "config/alacritty.toml",
                SKEL / ".config/alacritty/alacritty.toml")
    print("  ~ staged terminal stack (alacritty + live fish/tide suite + sysinfo greeting)")


def ensure_splash():
    """Point the captured session at the standalone KognogOS splash.

    This used to overwrite the third-party Catppuccin package's own
    Splash.qml in place. That worked, but it vandalized someone else's
    package: any theme update reverted it silently, and the result was
    unselectable in the splash KCM. The splash now lives in its own
    package (org.kognogos.splash, installed system-wide by
    install-look.sh and shipped in iso/airootfs), so all skel has to do
    is name it — and the Catppuccin package travels untouched.
    """
    rc = SKEL / ".config/kdedefaults/ksplashrc"
    rc.parent.mkdir(parents=True, exist_ok=True)
    rc.write_text("[KSplash]\nEngine=KSplashQML\nTheme=org.kognogos.splash\n")
    print("  ~ pointed KSplash at org.kognogos.splash")


def ensure_web_shortcuts():
    """profiles.toml web_shortcuts as real launcher entries (they were a
    spec line no artifact implemented — noticed missing on the live ISO)."""
    apps = SKEL / ".local/share/applications"
    apps.mkdir(parents=True, exist_ok=True)
    for name, url in [("Claude", "https://claude.ai"),
                      ("WhatsApp Web", "https://web.whatsapp.com")]:
        slug = name.lower().split()[0]
        (apps / f"kognog-{slug}.desktop").write_text(
            "[Desktop Entry]\n"
            "Type=Application\n"
            f"Name={name}\n"
            f"Exec=xdg-open {url}\n"
            "Icon=internet-web-browser\n"
            "Categories=Network;\n"
        )
    print("  ~ declared web shortcuts (Claude, WhatsApp Web)")


def ensure_default_apps():
    """Distro default-application bindings (not captured — declared).

    Nemo is the default file manager (Javier, 2026-07-30): the mimeapps
    binding makes every open-folder action route to Nemo while Dolphin
    stays installed. The reference machine's own mimeapps.list is personal
    (its handlers reflect installed apps + habits) and is never captured.
    """
    path = SKEL / ".config/mimeapps.list"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "[Default Applications]\n"
        "inode/directory=org.kde.dolphin.desktop\n"
        # Chrome is the distro default browser (Javier, 2026-07-31);
        # build-iso.sh swaps these to brave for the live session only
        # (Chrome cannot be redistributed inside the ISO).
        "x-scheme-handler/http=google-chrome.desktop\n"
        "x-scheme-handler/https=google-chrome.desktop\n"
        "text/html=google-chrome.desktop\n"
    )
    print("  ~ declared default apps (inode/directory -> dolphin)")


def main():
    check = "--check" in sys.argv
    warnings, captured, missing = [], [], []
    dropped_launchers = set()

    if not check:
        for top in (".config", ".local"):
            if (SKEL / top).exists():
                shutil.rmtree(SKEL / top)

    for rel in MANIFEST:
        src = HOME / rel
        if not src.exists():
            missing.append(rel)
            continue
        body = sanitize(src.read_text(errors="replace"), warnings, rel,
                        dropped_launchers)
        captured.append(rel)
        if not check:
            dst = SKEL / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(body)

    for rel in MANIFEST_DIRS:
        src = HOME / rel
        if not src.exists():
            missing.append(rel + "/")
            continue
        captured.append(rel + "/")
        if not check:
            shutil.copytree(src, SKEL / rel)

    if not check:
        patch_lnf_defaults()
        ensure_default_apps()
        ensure_terminal_stack()
        ensure_splash()
        ensure_web_shortcuts()

    mode = "CHECK (nothing written)" if check else f"captured into {SKEL}"
    print(f"export-plasma: {len(captured)} entries {mode}")
    for rel in captured:
        print(f"  + {rel}")
    if dropped_launchers:
        print(f"\n{len(dropped_launchers)} personal panel launchers filtered "
              "(no system-wide .desktop):")
        for name in sorted(dropped_launchers):
            print(f"  ✂ {name}")
    if missing:
        print(f"\n{len(missing)} manifest entries not present on this machine (skipped):")
        for rel in missing:
            print(f"  - {rel}")
    if warnings:
        print(f"\n⚠ {len(warnings)} lines still reference the home directory — review before shipping:")
        for w in warnings:
            print(f"  ⚠ {w}")
        sys.exit(2)
    print("\nNo personal paths survive.")
    if not check:
        verify_skel()


if __name__ == "__main__":
    main()
