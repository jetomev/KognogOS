# KognogOS — the list

**Target: v1.0 in April 2027** (now v0.9.0-beta). The live handoff between work sessions: updated after every step. Started 2026-10-05 (Javier: KognogOS had no TODO.md — every project carries the full kit).

**KognogOS = nog + the Forge Suite** (2026-10-05, D-60): the Forge apps now live in one repository, [jetomev/forge-suite](https://github.com/jetomev/forge-suite), with hypeForge as its first section.

**The board is the live road (Javier, 2026-10-22):** https://claude.ai/artifact/6UswcvpQ4EnWek5iVtBy5G opens beside the chat whenever this project is called (`scripts/status.sh`, first line). Items are added, marked done and re-ordered **there**; its snapshot is `docs/board/state.json` ([docs/board/README.md](docs/board/README.md)). This TODO keeps the repo's own housekeeping.

**The 1.0 cut (Javier, 2026-10-21):** every pending item across KognogOS, the Forge Suite and nog judged one by one — **127 ship in v1.0, 67 come during the first year (1.x), 5 dropped, 8 still open**. The list, by area: [docs/RELEASE-1.0.md](docs/RELEASE-1.0.md) (snapshot of the live board). v1.0 styles: Rice, Windows 11, KDE, Classic; the Mac styles and COSMIC in 1.x. **v2.0:** Claude built into the OS.

**The direction (2026-10-05, hypeForge D-56):** KognogOS will ship with **Sway only, through hypeForge** — no KDE. The order from here: finish the hypeForge Sway setup → the pending Forge Suite apps → the first KognogOS release.

---

## Now
- [x] **2026-10-28 evening: defaultappsForge 1.0.0 and nogForge 1.6.0 released** (GitHub + AUR after his installs; kognogos.org card) — board set-092 done, snapshot `25887db` (54/152)
- [x] **Stage 04, 2026-10-28: Javier's tries all passed** — the Rice's pieces 6–11 approved (hypeForge D-126); Quick Search, the calendar day, the chime, defaultappsForge's run and nogForge's search all passed; next: his decisions one at a time, then two releases; board snapshot `11cd61f` (53/152)
- [x] **Stage 04 "The four styles" started 2026-10-27** — the Rice first, piece by piece (look-071); the board brought current overnight: set-301 done, sway-171 drafted, links in step, snapshot `2068c96` (53 / 152)
- [ ] **The manual: one source, two places** (Javier, 2026-10-25: *"two places for the manual"*; board rel-310, stage 12): the repos' text files (hypeForge's Help guide, each app's manual) shown offline in the system (the Help app, each app's M key) and online as a Docs section on kognogos.org; a full pass when the apps stop changing. **Done 2026-10-25:** the 19 old design/look artifacts checked against the repos, 11 archived (forge-suite `8fd12d9`), all 19 deleted on his OK (*"yes, delete all 19"*), every link repointed to the GitHub copies; the boards and the trademark brief stay
- [x] **Stage 03 "The desktop, finished": 8 / 11 (2026-10-24)** — done: the bar guard, the night-light icon, displayForge's countdown text (F-8), the one title row on every pop-up, displayForge one and two screens · 80 / 90 % · text console (released as **displayForge 1.1.4**, GitHub + AUR), workspaceForge one and two screens · text console. Waiting for Javier's look: the three widths, the hover tip, the notification cards. Next: the menu card, every pop-up under what was clicked. Stage 00's name work parked on the Kognog Labs LLC bank account (rel-309). The board: `docs/board/` snapshot `76c92ce`
- [ ] **The Sway path's package list = what hypeForge and the Forge apps need, measured** (the Forge Suite dependency audit, 2026-10-11, [forge-suite#91](https://github.com/jetomev/forge-suite/issues/91)). Every app's list, with why, is in its `docs/PACKAGING.md`; hypeForge's is [hypeforge/docs/PACKAGING.md](https://github.com/jetomev/forge-suite/blob/main/hypeforge/docs/PACKAGING.md). `config/profiles.toml` is still Plasma-era and lists **none of these 34** hypeForge needs: sway, swaybg, waybar, mako, fuzzel, gtklock, swayidle, python-gobject, gtk3, gtk-layer-shell, python-textual, python-forgekit, python-pillow, python-numpy, adw-gtk-theme, wl-clipboard, cliphist, grim, slurp, swappy, libnotify, networkmanager-dmenu, libpulse, udisks2, udiskie, playerctl, xdg-user-dirs, xdg-utils, thunar, nightforge, sudoforge, python-cairo, glib2, brightnessctl. The `kognog_suite` list is behind too (nog, grubforge, alacrittyforge; nogforge commented): the Sway path adds sudoforge, nightforge, displayforge, workspaceforge, nogforge (and themeforge, defaultappsforge when packaged). Becomes the Sway profile with #13; Javier's call on the profile's shape.
- [ ] **Two hypeForge findings that touch the disc** (same audit): brightness keys bound to **brightnessctl**, not installed (forge-suite#94: a laptop needs it, or bind the keys to displayForge's ddcutil); Sway starts **pam_kwallet_init**, missing (forge-suite#95: walletForge's question, or kwallet-pam on the disc).
- [x] **The shell greeting follows the theme** (2026-10-10, `a10de55`, issue #15): `config/sysinfo.py` uses the terminal's colour names instead of fixed Mocha colours (it was pale on light themes); the skel and ISO copies synced. hypeForge's "About This Computer" opens it; it grows into **greeterForge** later (Javier, 10-10)
- [ ] **Decided by Javier, 2026-10-07 — Google Chrome, Claude Desktop and Claude Terminal are pre-selected in the installer, always; Brave is no longer the default.** *"People like it or not… During the installing process they will be able to switch if they want."* Clarified the same night: **no app is bundled in the ISO** (Arch-based, the install needs the internet); everything is installed from the repositories and the AUR during the install, and those three are **ticked by default** (Chrome from Google's repository, Claude Desktop via the AUR `claude-desktop`, Claude Terminal via Anthropic's installer or the AUR `claude-code`). The person installing unticks or picks another browser. `brave-bin` leaves the default lists; README tables, kognogos.org and welcomeForge follow. hypeForge's Chrome entry (`LIBVA_DRIVER_NAME=nvidia`, F-41) comes along. Issue **#14**
- [x] README + kognogos.org: the full list of coming Forge apps (2026-10-06); welcomeForge is the name used (the site said firstrunForge)
- [x] **GitHub review (Javier, 2026-10-06):** README on main says hypeForge on Sway (D-56) with the Plasma-era parts marked † (editions' app lists, login screen, graphical file manager — to be decided, not invented); Forge Suite table and versions current; About + topics (`kde-plasma` out; `sway`, `wayland`, `hypeforge`, `kognogos` in; homepage kognogos.org); **Where We Stand** re-checked against AUR + GitHub + each recipe's signature (it still claimed nog 1.2.0 / forgekit 0.3.0 "current"); **the missing v0.9.0-beta GitHub Release** published (the tag existed since July; "Latest" showed v0.8.1-alpha); #3 closed (no Plasma lock screen to fork). Commit `2a8c8a0`
- [x] **The `hypeforge-edition` branch (Javier, 2026-10-06: "Save the installer and delete the branch")**: installer, GRUB theme, the build safety fix (efivars), the clean-chroot mechanism, the live welcome line and the ignore rules moved to main (`c8aff19`); the Hyprland disc kept as tag `archive/hypeforge-edition-hyprland`; branch deleted here and on GitHub
- [ ] **The editions' app lists, the login screen for Sway, a graphical file manager** — redo for hypeForge (README †)
  - [ ] **The Craft apps (storytold / ArtCraft) for the recommended apps** (Javier, 2026-10-26; board app-01, stage 09 beside the Work list): ~15 open-source Rust apps (Word/Excel/PowerPoint/PDF-style for Work; photo, vector, video, effects, sound, layout, CAD, interface design); Linux builds, the Craft Launcher on the AUR (artcraft-launcher 0.8.1). **First his try on this desktop**, then a pick per edition (Work, installForge's optional apps, or later)
- [ ] **Fonts on the disc** (Javier, "very important"): every font hypeForge needs is listed in [hypeForge docs/FONTS.md](https://github.com/jetomev/forge-suite/blob/main/hypeforge/docs/FONTS.md). Added `ttf-nerd-fonts-symbols` (the bar's icons) to `iso/packages.x86_64` on 2026-10-05; proven on the next disc build
- [x] README: **sudoForge 1.0.0** in the Forge Suite table, the tech stack (Passwords), the AUR line and Done; forgekit 0.6.0 → **0.8.0** (it was two versions behind) (2026-10-06)
- [ ] **sudoForge on the disc** (released 2026-10-06, AUR `sudoforge`): the Sway path needs it (no admin pop-up or `sudo -A` window otherwise); add to `iso/packages.x86_64` with the Sway rebuild (#13), and run `sudoforge setup` at first boot (welcomeForge)
- [ ] `iso/packages.x86_64` lists `nano` and `tmux` twice (harmless; found 2026-10-05) — remove the repeats
- [ ] **The disc for the Sway path (#13):** build it on main around Sway + hypeForge as hypeForge's pieces settle (the Hyprland recipe is in the archive tag; `build-iso.sh` still stages the Plasma desktop). The issue carries the four things only a build can close: the fonts proven, the `build-iso.sh` path, the nano/tmux repeats, #11


## Open issues
- [ ] #2 Boot identity mandatory in the installed system, not just the live disc (installer recipe)
- [x] #3 closed 2026-10-06 — hypeForge's lock screen is gtklock (D-58); the Sway login screen gets its own issue when chosen
- [ ] #4 kognog-greeting as a standalone, packaged, distro-aware app
- [ ] #5 A Forge app for the shell prompt (with #12 → promptForge)
- [ ] #8 greetForge on a text console needs a tty version
- [ ] #9 Fresh install lacks fakeroot and nog's signing key
- [ ] #10 System Lock (managed mode): only nog may drive package transactions
- [ ] #11 AUR builds failed on an installed KognogOS (base-devel) — fixed on main (`2128566`); close after the next disc build proves it
- [ ] #12 The shell prompt looks awful on a text console → promptForge (not created as a project yet)

## The project kit
- [x] TODO.md (this file, 2026-10-05)
- [ ] CLAUDE.md — how KognogOS is built, tested and shipped (missing)
