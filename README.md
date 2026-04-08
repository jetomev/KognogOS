<p align="center">
  <img src="logo/logo-transparent.png" alt="KognogOS" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License"/>
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg" alt="Platform"/>
  <img src="https://img.shields.io/badge/Base-Arch%20Linux-1793d1.svg" alt="Base"/>
  <img src="https://img.shields.io/badge/Desktop-KDE%20Plasma-1d99f3.svg" alt="Desktop"/>
  <img src="https://img.shields.io/badge/Kernel-Zen-blueviolet.svg" alt="Kernel"/>
  <img src="https://img.shields.io/badge/Status-Alpha-orange.svg" alt="Status"/>
  <img src="https://img.shields.io/badge/Version-v0.8.0--alpha-purple.svg" alt="Version"/>
</p>

---

## What is KognogOS?

KognogOS is a Linux distribution built on top of Arch Linux, designed around a simple but powerful idea: **not all updates are equal**.

Most rolling-release distributions treat every package the same — when an update is available, it gets installed. This is fast, but it means your kernel, bootloader, and core system libraries can be updated automatically alongside a trivial icon theme. One bad kernel update and your machine doesn't boot.

KognogOS solves this with a **three-tier update model**, managed by its custom package manager `nog`. Tier 1 packages — the kernel, bootloader, glibc, systemd — are held and require your explicit sign-off before they ever get upgraded. Tier 2 packages — desktop environment, key applications — are held for 10 days to let the community catch regressions. Tier 3 — everything else — flows through quickly.

The result is a distribution that feels like a rolling release for most of your software, but behaves like a stable distribution for the parts that actually matter.

**Today**, KognogOS is an Arch-based distribution with custom tooling layered on top. **The long-term vision** is a fully independent Arch-based distribution — with its own package repository, its own build infrastructure, and an identity entirely its own.

---

## Philosophy

- **Stability where it counts** — the kernel, bootloader, and core libraries are never auto-updated
- **Freshness everywhere else** — Tier 3 packages stay current without ceremony
- **Safety by default** — every system action requires confirmation; every change is reversible
- **Beautiful by design** — KDE Plasma on Wayland, Zen kernel, Catppuccin Mocha throughout
- **Transparent tooling** — `nog` is a thin, readable Rust wrapper around pacman — no magic, no surprises
- **Built to grow** — the architecture is designed from day one to eventually support a fully independent repo and build pipeline

---

## The Three-Tier Update System

The heart of KognogOS is `nog`'s tier model. Every package on the system belongs to one of three tiers:

### Tier 1 — Manual Sign-Off Required
The most critical packages on your system. These are **never updated automatically** — not even during a full system upgrade. To update a Tier 1 package you must explicitly unlock it first with `nog unlock <package> --promote`.

Current Tier 1 packages include:
`linux`, `linux-zen`, `linux-lts`, `systemd`, `glibc`, `grub`, `efibootmgr`, `mkinitcpio`, `pacman`, `mesa`

### Tier 2 — 10-Day Hold
Key desktop applications and system services. These are held for **10 days** after a new version is published, giving the community time to catch regressions before the update reaches your machine.

Current Tier 2 packages include:
`plasma-desktop`, `sddm`, `pipewire`, `networkmanager`, `firefox`, `dolphin`, `konsole`, `kate`, `grubforge`

### Tier 3 — Fast Track (3-Day Hold)
Everything else. A minimal 3-day hold applies, then updates flow through automatically on the next `nog update`.

---

## nog — The Package Manager

`nog` is KognogOS's custom package manager, written in Rust. It wraps `pacman` with tier-awareness, giving you a familiar interface with intelligent update management underneath.

### Installation

nog is available on the Arch User Repository:
[https://aur.archlinux.org/packages/nog](https://aur.archlinux.org/packages/nog)

```bash
yay -S nog
```

On a fresh KognogOS install, nog comes pre-installed with sensible default tier assignments already configured in `/etc/nog/tier-pins.toml`.

### Usage

```bash
# Install a package (respects tier rules)
sudo nog install <package>

# Update the system (Tier 1 packages automatically held)
sudo nog update

# Search with tier annotations
nog search <query>

# Pin a package to a specific tier
nog pin <package> --tier=<1|2|3>

# Unlock a Tier 1 package for manual upgrade
sudo nog unlock <package> --promote

# Remove a package
sudo nog remove <package>
```

### How nog update works

When you run `sudo nog update`, nog:

1. Loads `tier-pins.toml` and identifies all Tier 1 packages
2. Displays them clearly as `[HELD]` — they will not be touched
3. Passes the upgrade to `pacman -Syu` with Tier 1 packages excluded
4. Tier 2 and Tier 3 packages update normally

---

## GrubForge — Included by Default

KognogOS ships with **GrubForge**, a full terminal UI for managing the GRUB bootloader — built by the same team.

GrubForge gives you:
- A safe, guided interface for editing `/etc/default/grub`
- Theme browser with color palette preview and one-key apply
- Timestamped backups before every single change
- Boot entry reordering, renaming, and custom entry creation
- OS detection via os-prober
- grub-mkconfig integration

GrubForge is pinned to **Tier 2** in KognogOS — it manages your bootloader, so it deserves the same careful update handling as your desktop environment.

```bash
sudo grubforge
```

GrubForge is also available standalone on the AUR:
[https://aur.archlinux.org/packages/grubforge](https://aur.archlinux.org/packages/grubforge)

---

## Tech Stack

| Component | Choice |
|-----------|--------|
| Base | Arch Linux |
| Kernel | Zen |
| Desktop | KDE Plasma on Wayland |
| Display Manager | SDDM |
| Package Manager | pacman + nog (custom) |
| nog language | Rust |
| Shell | Fish + Tide v6 |
| Terminal | Alacritty + AlacrittyForge |
| Font | JetBrainsMono Nerd Font |
| Theme | Catppuccin Mocha |
| GRUB Manager | GrubForge |
| Terminal Config | AlacrittyForge |

---

## Project Structure

```
KognogOS/
|-- nog/                         # nog package manager (Rust)
|   |-- src/
|   |   |-- main.rs              # Entry point, CLI definition
|   |   |-- tiers.rs             # Tier classification engine
|   |   |-- pacman.rs            # pacman subprocess wrapper
|   |   |-- config.rs            # Config loader (/etc/nog/nog.conf)
|   |   |-- commands/
|   |       |-- mod.rs           # All subcommand implementations
|   |-- Cargo.toml
|-- config/
|   |-- nog.conf                 # nog system configuration
|   |-- tier-pins.toml           # Tier 1/2/3 package assignments
|   |-- dependencies.toml        # Full KognogOS package manifest
|   |-- alacritty.toml           # Default Alacritty terminal config
|   |-- config.fish              # Default fish shell config
|   |-- fish_greeting.fish       # Terminal welcome box trigger
|   |-- sysinfo.py               # Terminal welcome box script
|   |-- tide_config.fish         # Default tide prompt configuration
|-- logo/
|   |-- logo.png                 # Light background version
|   |-- logo-transparent.png     # Transparent background version
|   |-- logo-black-bckg.png      # Black background version
|-- nog.1                        # nog man page
|-- assets/
|   |-- wallpapers/
|       |-- Kognog OS - Logo Black.png        # Dark wallpaper variant
|       |-- Kognog OS - Logo Catpuccin Mocha.png  # Catppuccin Mocha wallpaper
|       |-- Kognog OS - Logo White.png        # Light wallpaper variant
|-- bootstrap/                   # Future: OS bootstrapper scripts
|-- docs/                        # Future: documentation
```

---

## Current State

KognogOS is in **active early development**. The core package manager is working and installed system-wide. The distribution layer — installer, custom repos, ISO build pipeline — is on the roadmap.

What works today:
- `nog install` — installs packages with full tier enforcement
- `nog update` — system upgrade with Tier 1 packages genuinely excluded
- `nog search` — package search with color-coded tier annotations
- `nog pin` — tier assignment persisted to tier-pins.toml
- `nog unlock` — manual Tier 1 promotion
- `nog remove` — package removal
- System-wide install at `/usr/local/bin/nog`
- GrubForge included and pinned to Tier 2
- Terminal welcome box with live system info and tier notifications

---

## Roadmap

- [x] nog CLI skeleton — all subcommands defined
- [x] Tier system — three-tier classification engine
- [x] Real pacman calls — nog wraps pacman for real installs/updates
- [x] nog search — with color-coded tier annotations
- [x] System-wide install — nog at `/usr/local/bin/nog`
- [x] GrubForge — GRUB manager included and pinned to Tier 2
- [x] KognogOS logo
- [x] nog update — properly exclude Tier 1 via pacman --ignore flags
- [x] nog pin — persist tier changes to tier-pins.toml
- [x] Terminal welcome box with tier notifications
- [x] Default terminal stack — Alacritty, Fish, Tide, AlacrittyForge
- [x] nog AUR package
- [ ] Calamares installer — five profiles: Minimal, Desktop, Developer, Gamer, Full
- [ ] ISO build pipeline
- [ ] Custom package repository
- [ ] Full independent distribution

---

## Changelog

### v0.8.0-alpha — April 7, 2026
**Default terminal stack**
- Alacritty config with Catppuccin Mocha, JetBrainsMono Nerd Font, 150x50 window
- Fish shell config with cargo path
- fish_greeting.fish — triggers sysinfo.py on every new terminal session
- tide_config.fish — applies KognogOS default tide v6 prompt configuration
- alacritty, fish, alacrittyforge pinned to Tier 2
- ttf-jetbrains-mono-nerd added to dependencies
- alacrittyforge added to system tools and dependencies

### v0.7.1-alpha — April 7, 2026
**nog AUR package + man page**
- `nog` is now available on the AUR — install with `yay -S nog`
- Man page added — `nog.1` installed to `/usr/share/man/man1/`
- nog version bumped to 0.6.0 to match project version
- Version now reads from `CARGO_PKG_VERSION` — no more hardcoded strings
- PKGBUILD installs binary, config files, license, and man page

### v0.6.0-alpha — April 5, 2026
**Terminal Welcome Box**
- KognogOS branded terminal welcome box on every new session
- Shows OS, Kernel, Desktop, CPU, GPU, Uptime and resource bars
- Live weather via Open-Meteo API
- Tier notifications — only shown when action is needed:
  - Tier 1 packages ready for manual sign-off shown in red
  - Tier 2 packages ready to install shown in green
- Welcome message with user name
- Built with Python + Rich, Catppuccin Mocha colors throughout

### v0.5.0-alpha — April 5, 2026
**nog pin — tier changes persist to tier-pins.toml**
- `nog pin <package> --tier=<1|2|3>` now writes changes directly to `/etc/nog/tier-pins.toml`
- Pinning to Tier 1 or 2 adds the package to the correct section
- Pinning to Tier 3 removes it from Tier 1/2 — Tier 3 is the default, no entry needed
- Changes survive reboots and are immediately reflected in `nog search` tier annotations

### v0.4.0-alpha — April 5, 2026
**nog update — Tier 1 properly excluded**
- `nog update` now passes Tier 1 packages to pacman via `--ignore` flags
- Tier 1 packages are genuinely untouchable during a system upgrade
- Previously they were listed as held but pacman could still update them
- Confirmed: system upgraded 14 packages, zero Tier 1 packages touched

### v0.3.0-alpha — April 4, 2026
**nog search + system install + GrubForge + Logo**
- `nog search` now shows color-coded tier annotations for every result
- nog installed system-wide at `/usr/local/bin/nog`
- Config files at `/etc/nog/nog.conf` and `/etc/nog/tier-pins.toml`
- GrubForge added to Tier 2 — ships as a default KognogOS tool
- `nog` callable from anywhere on the system without a path
- KognogOS logo designed and added to repository

### v0.2.0-alpha — March 25, 2026
**Tier system + real pacman calls**
- Three-tier classification engine fully implemented in `tiers.rs`
- `tier-pins.toml` defines all Tier 1/2/3 package assignments
- `pacman.rs` wires real subprocess calls — nog now actually installs/removes/updates packages
- `nog install` blocks Tier 1 packages with clear error message
- `nog update` displays all held Tier 1 packages before running upgrade
- `nog unlock --promote` allows manual Tier 1 upgrades
- `config.rs` reads `/etc/nog/nog.conf` with graceful fallback

### v0.1.0-alpha — March 25, 2026
**Initial release — nog CLI skeleton**
- Full KognogOS project structure established
- nog v0.1.0 Rust CLI with clap
- All subcommands defined: install, remove, update, search, pin, unlock
- Three-tier architecture designed and stubbed
- Project committed to GitHub

---

## Authors

**jetomev** — idea, vision, direction, testing

**Claude (Anthropic)** — co-developer, architecture, implementation

This project is a collaboration between a human with a clear vision for what Linux package management should feel like, and an AI that helped design and build the tools to make it real — one command at a time.

---

## License

KognogOS is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0** as published by the Free Software Foundation.

See [LICENSE](LICENSE) for the full license text.

---

## Contributing

KognogOS is in early alpha. Ideas, feedback, and contributions are welcome — open an issue or pull request on GitHub.

If this project resonates with you, consider starring the repository. It helps others find it and motivates continued development.
