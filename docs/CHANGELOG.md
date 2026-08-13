# KognogOS — full changelog

*The README carries the two most recent entries; the complete history lives here, newest-first.*

### v0.8.1-alpha — 2026-04-20
**nog spun out; KognogOS repositioned around external nog + in-house Forge suite**

Clean repositioning release. No new distro-level capability ships, but every piece of repo drift since v0.8.0-alpha is resolved and the product surface is redefined around the new reality: `nog` is now a standalone stable project, and KognogOS is the distro that ships it by default alongside a curated Forge suite.

**Repository cleanup:**
- 🗑 Removed the vestigial `nog/` subtree — nog now lives at [github.com/jetomev/nog](https://github.com/jetomev/nog) and ships as an external AUR package
- 🗑 Removed empty `docs/DESIGN.md` and `docs/TIERS.md` stubs
- 🖼 Wallpaper set expanded: the old three-variant set was replaced by two five-variant sets ("Kognog OS Arch" + "Kognog OS Semi"), ten wallpapers total; new default is **Semi Catppuccin Mocha**

**New configuration surface:**
- 📋 `config/profiles.toml` — canonical edition-definition file with five editions (Basic, Office, Gaming, Development, Full). Calamares will read this at install time.
- 📦 `config/pacman.conf` — was a 0-byte placeholder; now ships with `core` / `extra` / `multilib` / `chaotic-aur` enabled, plus the distro's pacman tweaks (`Color`, `VerbosePkgLists`, `ILoveCandy`, `ParallelDownloads=5`)
- 🎚 `config/tier-pins.toml` — **full factory pin coverage**: every package the distro ships now has an explicit Tier 1 or Tier 2 assignment, so a fresh install has opinionated protection out of the box. Tier 1 expanded to cover `linux-firmware`, `base`/`base-devel`, all four kernel headers, CPU microcode, Vulkan ICDs, 32-bit graphics, and all seven Nvidia kernel module variants. Tier 2 expanded to cover `okular`, `bluez`, `python`, `yay`, `pacman-contrib`, `fresh-editor-bin`, `cups`, `docker`, and the Wayland-on-Nvidia glue. Legacy `hold_days` fields removed (since nog v0.8.0 these live in `nog.conf`). `manual_signoff` default flipped to `false` to match nog v0.9.0+ novice-friendly behavior. Browsers moved to Tier 3 (implicit default).

**Positioning:**
- 📖 README rewritten top-to-bottom around the new product surface
- 🌳 Tier model description updated to match nog v1.0 (30 / 15 / 7 days, not the old 10 / 3)
- 🧩 The Forge suite replaces the old per-tool README sections — one coherent story for `nog` + `grubforge` + `alacrittyforge` + upcoming `nogforge`
- 🎨 Editions section added — the product surface made explicit for the first time

### v0.8.0-alpha — 2026-04-07
**Default terminal stack**
- Alacritty config with Catppuccin Mocha, JetBrains Mono Nerd Font, 150x50 window
- Fish shell config with cargo path
- `fish_greeting.fish` triggers `sysinfo.py` on every new terminal session
- `tide_config.fish` applies the KognogOS default Tide v6 prompt
- `alacritty`, `fish`, `alacrittyforge` pinned to Tier 2
- `ttf-jetbrains-mono-nerd` and `alacrittyforge` added to dependencies

### v0.7.1-alpha — 2026-04-07
**nog AUR package + man page** *(work subsequently migrated to the standalone nog repo)*
- `nog` available on the AUR
- Man page added
- Version reads from `CARGO_PKG_VERSION`

### v0.6.0-alpha — 2026-04-05
**Terminal welcome box**
- KognogOS-branded terminal welcome box on every new session
- Live weather (Open-Meteo), live tier notifications (red for Tier 1 sign-off, green for Tier 2 ready)
- Built with Python + Rich, Catppuccin Mocha throughout

### v0.5.0-alpha — 2026-04-05
**nog pin persistence** *(work migrated to the standalone nog repo)*

### v0.4.0-alpha — 2026-04-05
**nog update — Tier 1 exclusion** *(work migrated to the standalone nog repo)*

### v0.3.0-alpha — 2026-04-04
**nog search + system install + GrubForge included + KognogOS logo**

### v0.2.0-alpha — 2026-03-25
**Tier system + real pacman calls** *(work migrated to the standalone nog repo)*

### v0.1.0-alpha — 2026-03-25
**Initial release — nog CLI skeleton** *(work migrated to the standalone nog repo)*

---
