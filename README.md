<p align="center">
  <img src="logo/logo-transparent.png" alt="KognogOS" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License"/>
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg" alt="Platform"/>
  <img src="https://img.shields.io/badge/Base-Arch%20Linux-1793d1.svg" alt="Base"/>
  <img src="https://img.shields.io/badge/Model-Semi--Rolling-f38ba8.svg" alt="Model"/>
  <img src="https://img.shields.io/badge/Desktop-KDE%20Plasma-1d99f3.svg" alt="Desktop"/>
  <img src="https://img.shields.io/badge/Status-Alpha-orange.svg" alt="Status"/>
  <img src="https://img.shields.io/badge/Version-v0.8.1--alpha-purple.svg" alt="Version"/>
</p>

---

## What is KognogOS?

KognogOS is an **Arch-based, semi-rolling, tier-aware Linux distribution**. It's built on one simple idea: **not all updates are equal**.

Most rolling-release distributions treat every package the same — when an update is available, it gets installed. Your kernel and core system libraries update automatically alongside a trivial icon theme. One bad kernel sync and your machine doesn't boot.

KognogOS solves this with a **three-tier update model** enforced by [`nog`](https://github.com/jetomev/nog), its tier-aware package manager. Tier 1 packages — kernel, bootloader, glibc, systemd, mesa — are held for 30 days after upstream publish, giving the community time to catch regressions. Tier 2 — desktop environment and key applications — are held for 15 days. Tier 3 — everything else — flows through in 7.

The result feels like a rolling release for most of your software, but behaves like a stable distribution for the parts that actually matter.

KognogOS ships with a curated in-house **Forge suite** — TUI tools for package management, bootloader configuration, and terminal customization — and is available in **five editions** matched to how you actually use a Linux machine: Basic, Office, Gaming, Development, and Full.

---

## Philosophy

- **Stability where it counts** — kernel, bootloader, and core libraries get a 30-day community buffer before they land on your machine
- **Freshness everywhere else** — Tier 3 packages stay current without ceremony
- **Safety by default** — `nog` invokes pacman as a subprocess; every transaction goes through pacman's own signature verification
- **Beautiful by design** — KDE Plasma on Wayland, Catppuccin Mocha throughout, one opinionated terminal stack
- **Transparent tooling** — the Forge suite is readable source code, no magic
- **Built to grow** — the architecture is designed to eventually support a fully independent repo and build pipeline

---

## Editions

KognogOS ships as five editions, all sharing the same core (KDE Plasma, nog-managed updates, the Forge suite, drivers, default terminal stack) and differing only in the app stack layered on top. Edition definitions live in [`config/profiles.toml`](config/profiles.toml) — the single source of truth `installforge` reads at install time.

### Basic
The shared core. Boots straight into a KDE Plasma Wayland desktop with the KognogOS terminal welcome box, **Fresh Editor** as the default text editor, both **Google Chrome** and **Brave** ready to go, and `nog` + `grubforge` + `alacrittyforge` installed out of the box. Daily-life floor included: Gwenview, Ark, KCalc, Spectacle, full font coverage (Noto + emoji + Liberation), printing and scanning (CUPS + Skanlite), and **ufw enabled by default** (deny incoming).

### Office
Basic + **OnlyOffice**, **Obsidian**, **Thunderbird**, **Xournalpp**, **Elisa**, **Spotify**, **GIMP**, **Pinta**, **Kdenlive**, **Discord**, **Telegram**.

### Gaming
Basic + **Steam**, **Lutris**, **Heroic**, **Wine**, **Proton-GE**, **RetroArch with a starter core set** (NES/SNES/Genesis/PS1/N64/GBA), 32-bit graphics, **Gamescope**, **GameMode**, **MangoHud**, and **OBS Studio** for streaming.

### Development
Basic + **VS Code**, **Neovim**, **rustup**, **Node.js**, **Go**, **OpenJDK**, **Docker**, **Tmux**, a modern CLI toolkit (bat, eza, fd, ripgrep, fzf, zoxide), build tools (cmake, meson, ninja), and both compiler families with their debuggers (gcc/gdb, clang/lldb).

### Full
Basic + Office + Gaming + Development — everything KognogOS ships.

---

## The Three-Tier Update System

Every package on the system belongs to one of three tiers, enforced by `nog`:

### Tier 1 — 30-Day Hold
The most critical packages on your system — kernel, bootloader, glibc, systemd, mesa. Updates are held for **30 days** after upstream publish. Once the hold expires, the update flows through `nog update` like any other package. **Expert mode:** set `manual_signoff = true` in `/etc/nog/tier-pins.toml` to require explicit `nog unlock <pkg> --promote` for every Tier 1 upgrade.

### Tier 2 — 15-Day Hold
Desktop environment and key applications — Plasma, SDDM, PipeWire, NetworkManager, the Forge suite, and more. Held for **15 days**.

### Tier 3 — 7-Day Hold
Everything else. A short **7-day** safety buffer, then updates flow through automatically.

For full details, see [the `nog` documentation](https://github.com/jetomev/nog#the-three-tier-system).

---

## The Forge Suite

KognogOS ships with an in-house suite of TUI tools that replace the "edit a config file and pray" workflow with safe, guided interfaces for common system tasks. All Forge tools are pinned to Tier 2.

### nog — Package manager
Tier-aware pacman wrapper in Rust. Classifies every package, enforces hold windows via pacman's own `--ignore` mechanism, and delegates to `yay`/`paru` for AUR. Runs as your user; escalates only to `sudo pacman` when necessary.
→ **v1.0.8 stable** · [github.com/jetomev/nog](https://github.com/jetomev/nog) · `yay -S nog`

### grubforge — Bootloader manager
Full TUI for managing GRUB: safely edit `/etc/default/grub`, browse and apply themes, reorder boot entries, detect other operating systems, with timestamped backups before every change.
→ **Shipping** · [github.com/jetomev/grubforge](https://github.com/jetomev/grubforge) · `yay -S grubforge`

### alacrittyforge — Terminal configurator
TUI for managing Alacritty's TOML config — font, colors, opacity, keybindings — with live previews and reversible edits.
→ **Shipping** · [github.com/jetomev/alacrittyforge](https://github.com/jetomev/alacrittyforge)

### nogforge — Unified package TUI *(coming soon)*
A TUI companion for `nog` plus a unified interface across AUR helpers, Flatpak, and Snap. In active development.
→ **Upcoming** · [github.com/jetomev/nogforge](https://github.com/jetomev/nogforge)

---

## Tech Stack

| Component | Choice |
|-----------|--------|
| Base | Arch Linux |
| Kernel | Linux (mainline) + Linux-LTS fallback |
| Microcode | Auto-detected at install time (intel-ucode / amd-ucode) |
| Desktop | KDE Plasma on Wayland |
| Display Manager | SDDM |
| Audio | PipeWire + WirePlumber |
| Network | NetworkManager |
| GPU drivers | Mesa + Vulkan (AMD / Intel) · Nvidia-Open DKMS |
| Package Manager | pacman + **nog** |
| Bootloader Manager | **grubforge** |
| Terminal | **Alacritty** + AlacrittyForge-driven config |
| Shell | **Fish** + Tide v6 prompt |
| Default Editor | **Fresh Editor** |
| Default Browsers | Google Chrome + Brave (both shipped) |
| Font | JetBrains Mono Nerd Font |
| Theme | Catppuccin Mocha |
| Extra Repos | chaotic-aur |

---

## Project Structure

```
KognogOS/
|-- assets/
|   |-- wallpapers/                # 10 wallpapers across Arch + Semi variants
|-- config/
|   |-- pacman.conf                # Shipped pacman.conf (core/extra/multilib/chaotic-aur)
|   |-- profiles.toml              # Edition definitions (Basic/Office/Gaming/Development/Full)
|   |-- dependencies.toml          # Legacy package manifest (being migrated into profiles.toml)
|   |-- tier-pins.toml             # Tier 1/2 package assignments shipped as distro default
|   |-- nog.conf                   # Shipped /etc/nog/nog.conf
|   |-- alacritty.toml             # Default Alacritty terminal config
|   |-- config.fish                # Default Fish shell config
|   |-- tide_config.fish           # Default Tide v6 prompt configuration
|   |-- fish_greeting.fish         # Terminal welcome-box trigger
|   |-- sysinfo.py                 # Terminal welcome-box script
|-- docs/                          # Future: documentation
|-- installer/                     # Future: Calamares configuration
|-- logo/                          # KognogOS logo (transparent, light, dark)
|-- repo/                          # Future: custom package repository
|-- LICENSE
|-- README.md
```

---

## Current State

KognogOS is in **active early development**, on the road to a **v1.0 public ISO targeted for April 2027** — the project's origin week, two years after the wish that started it ("create an installer of my arch linux setup", 2025-04-19).

**What's solid today:**
- `nog` v1.0.8 stable on AUR — tier-aware updates, AUR integration, lib32/base hold coupling, tabled update reports, CSV run logging, documented privilege model, dogfooded on every release
- The Forge suite shipping on AUR — `grubforge` (GRUB TUI), `alacrittyforge` (terminal configurator), `bitlaforge` (solo-mining TUI), with `forgekit` as the shared v2 UI library
- Five-edition product surface formalized in `config/profiles.toml`
- Default terminal stack: Alacritty + Fish + Tide v6 + KognogOS welcome box
- Full `pacman.conf` shipped as distro default — **chaotic-aur enabled from the start** (decided 2026-07-30): its packages are governed by the tier system like every other repo, with **63 pre-assigned Tier 1 pins** (kernels, mesa/nvidia builds, `glibc-eac`, `pacman-git`, ZFS modules, boot-entry writers) generated by `scripts/chaotic-tier-audit.py` and refreshed each annual release. Everything else in chaotic rides Tier 3's automatic 7-day hold. (Honest scope note: tiers guard against *regressions*; repo-integrity failures remain the job of pacman's signature verification.)
- Wallpaper set: ten wallpapers across Arch + Semi variants

**First release scope (decided 2026-07-30):** KognogOS **Semi** only — the tier-aware semi-rolling flagship — with all five editions selectable at install time. The "Arch" brand variant is reserved for a future year. The installer will be **`installforge`**, a Forge-style TUI (own repo + AUR package, like its siblings) that reads `config/profiles.toml`, and installs **online** (decided 2026-07-30): all packages come from the mirrors at install time, so the ISO contains no redistributable payload at all and proprietary edition apps (browsers, Spotify, Discord, …) are simply fetched with user consent like everything else — never carried inside the ISO. A network connection is required to install.

---

## Release model — one ISO a year

KognogOS follows an **annual release cadence, on purpose**. This is a two-person project (one human, one AI), and the honest way to run it:

- **Year-round**, the work goes into `nog` and the Forge suite — updates, fixes, new Forge apps. That's where the daily energy lives, and every improvement lands on existing installs immediately through normal updates (this is still a semi-rolling Arch system — the ISO is an installer snapshot, not a feature gate).
- **Once a year**, the accumulated year of work crystallizes into a new ISO release.
- **Feedback** has a single door: [GitHub Issues](https://github.com/jetomev/kognog/issues). Distro-level findings batch into the next annual ISO (the same findings-batch discipline used across the Forge suite). The only out-of-band trigger is a critical or security-relevant installer bug, which gets an ISO respin.
- **Horizon:** this is a 3–5 year project and that's fine. By the time it's "done," the Forge library will be deep and the distro will be genuinely fun.

---

## Roadmap

The road to v1.0 (target: **April 2027**), phased in the same discipline as every Kognog project:

- [x] **Phase 1 — KDE Plasma config export** ✅ **DONE 2026-07-30** (validated over 4 kogtest rounds; see below) — a reusable capture script (live config → `/etc/skel/`, personal residue stripped by rule). Panel layout: the single bottom bar. The final look (wallpapers, polish pass) is deliberately frozen **late** — just before release, from Balih's wallpapers
- [ ] **Phase 2 — First bootable ISO** — archiso profile: live Plasma session, branding, terminal stack, nog + Forge preinstalled. No installer yet — the "it boots!" milestone. Includes the **display-manager decision**: SDDM is not locked in — evaluate alternatives (greetd family, Ly) vs. a custom forgekit-inspired SDDM theme
- [ ] **Phase 3 — `installforge`** — the Forge-style TUI installer (own repo + AUR): edition picker reading `config/profiles.toml`, guided disk setup, user creation. **App-selection flow (decided 2026-07-30):** each edition shows its recommended package list; proprietary apps are marked and de-selectable; de-selecting one offers a curated free/open-source replacement to pick instead (e.g. Chrome → Firefox, VS Code → `code`). The **Development edition** additionally shows a pre-install notice recommending a review of the tier pins against the user's toolchain needs
- [ ] **Tier reference guide** — a plain-language manual for the tier system: what each tier means, how to read and hand-edit `tier-pins.toml`, `nog pin`/`unlock` recipes, and worked examples (ships in the repo + as a page on the project site)
- [ ] **Phase 4 — Dogfood + validation** — VM matrix first, then the wipe-and-rebuild method: install a real machine from the ISO alone until a zero-deviation run
- [ ] **Phase 5 — Release kit** — ISO hosting (SourceForge for the image, GitHub for source — GitHub Releases caps files at 2 GiB), checksums + signature, project site on GitHub Pages
- [ ] **Phase 6 — v1.0 public release** — GitHub Release → project page → community announcements → DistroWatch submission (their queue takes months; the annual cadence shrugs)

**Deferred by design (honest scope control):**
- Calamares GUI installer — v2+, once `installforge` has proven the flow
- Custom package repository (`repo.kognog.org`) — not needed while official repos + AUR carry everything we ship
- "Kognog OS Arch" brand variant — a future year's release
- `nogforge` — continues on the year-round Forge track, ships when ready (not gated to the ISO)

**Done:**
- [x] Product surface formalized — five editions in `config/profiles.toml`
- [x] `nog` extracted to its own stable repo + AUR package (v1.0.8 as of 2026-07-29)
- [x] `pacman.conf` shipped as distro default
- [x] Default terminal stack (Alacritty + Fish + Tide v6 + welcome box)

---

## Changelog

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

## Related Projects

The KognogOS ecosystem lives across several repositories. All are developed by the same team.

- **[nog](https://github.com/jetomev/nog)** — tier-aware package manager, the engine that makes KognogOS semi-rolling. Stable on the AUR.
- **[grubforge](https://github.com/jetomev/grubforge)** — GRUB bootloader manager. Stable on the AUR.
- **[alacrittyforge](https://github.com/jetomev/alacrittyforge)** — Alacritty terminal configurator. Shipping.
- **[nogforge](https://github.com/jetomev/nogforge)** — unified TUI for nog / AUR helpers / Flatpak / Snap. In development.

---

## Authors

**jetomev** — idea, vision, direction, testing

**Claude (Anthropic)** — co-developer, architecture, implementation

KognogOS is a collaboration between a human with a clear vision for what a Linux distro should feel like, and an AI that helped design and build the pieces — one `config/profiles.toml` entry at a time.

---

## License

KognogOS is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0** as published by the Free Software Foundation.

See [LICENSE](LICENSE) for the full license text.

---

## Contributing

KognogOS is in early alpha. Ideas, feedback, and contributions are welcome — open an issue or pull request on GitHub.

If this project resonates with you, consider starring the repository. It helps others find it and motivates continued development.
