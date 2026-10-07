# KognogOS — the list

**Target: v1.0 in April 2027** (now v0.9.0-beta). The live handoff between work sessions: updated after every step. Started 2026-10-05 (Javier: KognogOS had no TODO.md — every project carries the full kit).

**KognogOS = nog + the Forge Suite** (2026-10-05, D-60): the Forge apps now live in one repository, [jetomev/forge-suite](https://github.com/jetomev/forge-suite), with hypeForge as its first section.

**The direction (2026-10-05, hypeForge D-56):** KognogOS will ship with **Sway only, through hypeForge** — no KDE. The order from here: finish the hypeForge Sway setup → the pending Forge Suite apps → the first KognogOS release.

---

## Now
- [ ] **Decided by Javier, 2026-10-07 — the disc ships Google Chrome, Claude Desktop and Claude Terminal pre-installed; Brave goes.** *"People like it or not… I do not care about what people think about that. During the installing process they will be able to switch if they want."* How, given `iso/packages.x86_64`'s note that Chrome's licence forbids shipping it inside a disc image: **the installer downloads and installs the three during the install** (Chrome from Google's own repository, Claude Desktop from the AUR `claude-desktop` recipe, Claude Terminal with Anthropic's installer or the AUR `claude-code`), so the finished system has them pre-installed without the image redistributing them. The installer offers the switch (another browser; no Claude). `brave-bin` leaves `iso/packages.x86_64` and the editions' app lists; the README's app tables, kognogos.org and welcomeForge follow. hypeForge's Chrome entry (`LIBVA_DRIVER_NAME=nvidia`, F-41) comes along. Issue **#14**
- [x] README + kognogos.org: the full list of coming Forge apps (2026-10-06); welcomeForge is the name used (the site said firstrunForge)
- [x] **GitHub review (Javier, 2026-10-06):** README on main says hypeForge on Sway (D-56) with the Plasma-era parts marked † (editions' app lists, login screen, graphical file manager — to be decided, not invented); Forge Suite table and versions current; About + topics (`kde-plasma` out; `sway`, `wayland`, `hypeforge`, `kognogos` in; homepage kognogos.org); **Where We Stand** re-checked against AUR + GitHub + each recipe's signature (it still claimed nog 1.2.0 / forgekit 0.3.0 "current"); **the missing v0.9.0-beta GitHub Release** published (the tag existed since July; "Latest" showed v0.8.1-alpha); #3 closed (no Plasma lock screen to fork). Commit `2a8c8a0`
- [x] **The `hypeforge-edition` branch (Javier, 2026-10-06: "Save the installer and delete the branch")**: installer, GRUB theme, the build safety fix (efivars), the clean-chroot mechanism, the live welcome line and the ignore rules moved to main (`c8aff19`); the Hyprland disc kept as tag `archive/hypeforge-edition-hyprland`; branch deleted here and on GitHub
- [ ] **The editions' app lists, the login screen for Sway, a graphical file manager** — redo for hypeForge (README †)
- [ ] **Fonts on the disc** (Javier, "very important"): every font hypeForge needs is listed in [hypeForge docs/FONTS.md](https://github.com/jetomev/forge-suite/blob/main/hypeforge/docs/FONTS.md). Added `ttf-nerd-fonts-symbols` (the bar's icons) to `iso/packages.x86_64` on 2026-10-05; proven on the next disc build
- [x] README: **sudoForge 1.0.0** in the Forge Suite table, the tech stack (Passwords), the AUR line and Done; forgekit 0.6.0 → **0.8.0** (it was two versions behind) (2026-10-06)
- [ ] **sudoForge on the disc** (released 2026-10-06, AUR `sudoforge`): the Sway path needs it (no admin pop-up or `sudo -A` window otherwise); add to `iso/packages.x86_64` with the Sway rebuild (#13), and run `sudoforge setup` at first boot (welcomeForge)
- [ ] `iso/packages.x86_64` lists `nano` and `tmux` twice (harmless; found 2026-10-05) — remove the repeats
- [ ] **The disc for the Sway path (#13):** build it on main around Sway + hypeForge as hypeForge's pieces settle (the Hyprland recipe is in the archive tag; `build-iso.sh` still stages the Plasma desktop). The issue carries the four things only a build can close: the fonts proven, the `build-iso.sh` path, the nano/tmux repeats, #11

- [ ] `scripts/build-iso.sh` looks for hypeForge at `~/Programs/hypeforge` (line 42): now `~/Programs/forge-suite/hypeforge` (a shortcut keeps the old path working on the test desktop) — update it with the Sway rebuild of the disc

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
