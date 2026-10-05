# KognogOS — the list

**Target: v1.0 in April 2027** (now v0.9.0-beta). The live handoff between work sessions: updated after every step. Started 2026-10-05 (Javier: KognogOS had no TODO.md — every project carries the full kit).

**The direction (2026-10-05, hypeForge D-56):** KognogOS will ship with **Sway only, through hypeForge** — no KDE. The order from here: finish the hypeForge Sway setup → the pending Forge Suite apps → the first KognogOS release.

---

## Now
- [ ] **Fonts on the disc** (Javier, "very important"): every font hypeForge needs is listed in [hypeForge docs/FONTS.md](https://github.com/jetomev/hypeforge/blob/main/docs/FONTS.md). Added `ttf-nerd-fonts-symbols` (the bar's icons) to `iso/packages.x86_64` on 2026-10-05; proven on the next disc build
- [ ] `iso/packages.x86_64` lists `nano` and `tmux` twice (harmless; found 2026-10-05) — remove the repeats
- [ ] **The disc for the Sway path:** the `hypeforge-edition` branch still builds the first-attempt Hyprland desktop; rebuild it around Sway + hypeForge as hypeForge's pieces settle

## Open issues
- [ ] #2 Boot identity mandatory in the installed system, not just the live disc (installer recipe)
- [ ] #3 Lock screen to match the KognogOS greeter — **revisit**: hypeForge's lock screen is gtklock (D-58)
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
