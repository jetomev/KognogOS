# KognogOS — project rules

*How this project is built, tested and shipped. Written for the AI co-developer, and public on purpose: it is part of how the human + AI method is documented.*

## What it is
An Arch-based Linux distribution where updates wait by risk: every package sits in one of three **tiers** (30, 15 or 7 days), enforced by **nog**, our package manager. **KognogOS = nog + the [Forge Suite](https://github.com/jetomev/forge-suite)**, with **hypeForge on Sway** as the only desktop: no KDE on the disc (hypeForge D-56). This repo holds the distro itself: the disc recipe, the factory settings, the installer draft, the look, the road to 1.0. nog and the Forge apps live in their own repositories, each with its own rules.

## The board comes first
- **The planning board is the live road to v1.0** (private): https://claude.ai/artifact/6UswcvpQ4EnWek5iVtBy5G. Calling this project = **open the board beside the chat FIRST** (Artifact `open`). `scripts/status.sh` says so on its first line, then prints the road from the last snapshot.
- **The board moves with the work, never after it.** Mark steps done, add new items (issues, findings, missing pieces, changes) and place them on the road, through ArtifactData (`items/<id>`, `road/plan`).
- **Then snapshot it:** export the board (`list` + `get` with `out_dir`), run `python3 scripts/board-snapshot.py <export-dir>`. It writes `docs/board/state.json` **and** regenerates `docs/RELEASE-1.0.md`. Commit both together.
- **`docs/RELEASE-1.0.md` is generated** by `scripts/board-release-doc.py`. Never edit it by hand: change the board, or the script's fixed text.
- `TODO.md` keeps only this repo's own housekeeping; the road lives on the board. How the board works: `docs/board/README.md`.
- **The board is linked to the projects KognogOS is made of** (Javier, 2026-10-22: *"KognogOS exists thanks to all other projects"*): nog, nogForge, grubForge, alacrittyForge, bitlaForge and the Forge Suite sections. Not AzerothCore, HomeLab, anything Rullynastre, mindForge, AI Collab, the portal, dropkit or DecadeDrop. `docs/board/links.json` ties each item to its twin: the project's TODO step(s) or GitHub issue(s); a few items are KognogOS's own (the disc, tests, decisions).
- **Ticks flow from the project to the board, never back:** the project's TODO is the record. `scripts/status.sh` runs `scripts/board-links.py check` every time; a ⚠ means bring the board in step (`check <export> --plan F`, then send F with ArtifactData). A new item that comes from a project gets its twin in links.json the same day, and a split item gets split lines in the project's TODO, never one line ticking several items.
- Each project board shows a "KognogOS 1.0 · stage NN" badge on the steps the road waits on: `scripts/board-links.py badges <dir>`, then mindForge's `board.py build … --badges <dir>/<project>.json`.

## v1.0, as decided
- **The week of 19 April 2027**: the project's second birthday. Now v0.9.0-beta (a Plasma-era disc).
- **Two editions in 1.0: Basic and Work** (Work is the former Office). Gaming, Development and Full come during the first year. Editions are defined in `config/profiles.toml`, which the installer reads.
- **Sway only, through hypeForge.** Nothing that brings another desktop back onto the disc.
- **The installer installs online**: every package comes from the mirrors during the install; nothing is bundled in the ISO. Proprietary apps are marked and fetched with consent, never redistributed. Chrome, Claude Desktop and Claude Terminal are ticked by default; the person installing can untick them (#14).
- **One ISO a year.** Work goes into nog and the Forge Suite all year and reaches installed systems through normal updates; only a critical installer or security bug gets a respin.

## The factory tier list
- **`config/tier-pins.toml` is KognogOS's factory tier list.** `build-iso.sh` copies it onto the disc as `/etc/nog/tier-pins.toml`, and the test desktop runs this same list since 2026-10-22. A change here changes the test desktop's own update holds when it is copied in, so say so first.
- The chaotic-aur Tier 1 block is **generated**: `scripts/chaotic-tier-audit.py` (prints) / `--write` (splices between the `BEGIN`/`END CHAOTIC-TIER1` markers). Rerun it each release; never edit inside the markers by hand.
- nog's own settings file is **not** shipped: nog's package owns it. Only the tier list is ours.

## Building, and where things may run
- **Nothing that builds the ISO or touches a disk ever runs against the test desktop's own system.** Which script is for what:
  - **The build machine:** `scripts/build-local-repo.sh` (builds our AUR-only packages into a local repo), then `scripts/build-iso.sh` (stages the repo's files into `iso/` and runs `mkarchiso` under sudo). Its work folder is `iso/work/`, never `/tmp`. **Keep its safety guard:** a past build left the computer's firmware folder attached inside `iso/work/`, and deleting it erased the machine's boot entries (2026-09-30). The script detaches everything first, stops if anything is still attached, and deletes with `--one-file-system`.
  - **A virtual machine only:** `installer/tui/kognog-install.sh` erases a whole disk. It refuses to run outside the live disc; test it in a VM, never on real hardware without Javier.
  - **Change the machine they run on** (Plasma-era, ask before running any): `apply-grub-polish.sh`, `install-greeter.sh`, `install-sddm-theme.sh`, `install-look.sh`, `install-greeting.sh`, `install-update-check.sh`.
  - **Safe anywhere** (read or write only repo files): `status.sh`, `board-*.py`, `chaotic-tier-audit.py`, `make-*.py`, `test-sddm-theme.sh`.
- `mkarchiso` reuses old steps from a stale work folder and "finishes" in a second having changed nothing, so `build-iso.sh` always starts clean. Squash with zstd (xz fails on this squashfs version).
- The disc is still the Plasma recipe (`iso/packages.x86_64`). Rebuilding it around Sway + hypeForge is issue **#13**; its package list is what hypeForge and the Forge apps measured they need (each app's `docs/PACKAGING.md`).
- `scripts/export-plasma.py` captured the old desktop into `skel/`. Its rule stays for any capture: **ship what is in use, strip everything personal.** No names, places, accounts, history or this desk's screen layout in a default.

## Tests
- `python3 scripts/tests/test-repo-aur-watch.py` and `python3 scripts/tests/test-project-staleness-watch.py` (the weekly watches, run by the user timers in `scripts/systemd-user/`).
- **The disc's real test is a VM install**, then a wiped physical machine, repeated until a run has zero deviations (README Phase 4). Findings are numbered F-n and each gets an issue.

## Words and names
- **The brand is KognogOS: one word, that spelling, always.** Trademark work is under way.
- **Public front doors (README, kognogos.org) describe the desktop looks plainly**, by what they are: "the taskbar with Start", "the floating panel with a pager". Never name other operating systems or desktops there, and never compare KognogOS with anyone. Credit what we learn from, with thanks.
- **Plain words.** The readers are not engineers; say what a technical term means in the same sentence.

## Documentation, at every step
- The README stays accurate top to bottom at every commit; parts that still describe the Plasma build are marked **†** until reworked. Roadmap and changelog newest first; `docs/CHANGELOG.md` holds the full history.
- `config/os-release` carries the version: bump it together with the tag.
- `docs/where-we-stand.md` is the public security page: re-check every claim in it against the AUR and GitHub before saying it is current.
