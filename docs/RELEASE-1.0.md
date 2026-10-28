# KognogOS 1.0 — the cut and the road

*Written from the board's snapshot of 2026-10-27 20:44 by `scripts/board-release-doc.py` — do not edit by hand. The live record is Javier's planning board (private). He judged every pending item there (2026-10-21) and ordered the road (2026-10-21/22).*

**153 ship in v1.0 · 78 come during the first year (1.x) · 6 dropped · 0 still open. The road: 49 of 148 steps done.**

v1.0 ships the **Basic** and **Work** editions with four desktop looks — the floating-island bar (the default), the taskbar with Start, the floating panel with a pager, and the plain classic look — and a smaller set of colour themes. The two menu-bar looks, the top panel with a dock, and the Full, Gaming and Development editions come during the year.

**Beyond the year — v2.0 (Javier, 2026-10-21):** *KognogOS + AI (Claude) full integration. Claude alive while the OS is on, with a tray chat bubble available for one to request directly there anything. We will create Claude commands to manipulate and control the OS, and even develop new functionalities, or make changes to it.*

## The road to launch

### 00 · Settle what shapes everything — late Oct 2026 (8/15 done)

*Decisions that change what we build next. Cheap now, expensive later — a name change or an edition dropped after the disc exists costs weeks.*

1. ✅ Which editions ship in 1.0: Basic, Work and Full? Is Work the old Office? Does Full leave out gaming and developer apps? (your note, 10-21) — *Your note says no developer, no gaming in 1.0; the Gaming and Development lists are marked v1.0.* **Javier:** Answered 10-22: Basic + Work only. Work = the old Office. Full, Gaming and Development come during the year.
2. ✅ One and two screens work in 1.0 (the one-to-six setup stays 1.x) (the cut, 10-21) — *Most people have one screen, a VM has one; today's settings assume this desk's three.* **Javier:** Javier, 10-22: it works. Checked the same day on a hidden one-screen Sway with the shipped settings (they name this desk's DP-3/DP-2/DP-1): switching workspaces worked, the applet stayed up.
3. ✅ This desktop runs nog's stock tier list, not KognogOS's. On purpose? (hypeForge open question) — *Open question since 09-28.* **Javier:** Javier, 10-22: switch this desktop to KognogOS's list. Done: backup /etc/nog/tier-pins.toml.bak-20261022, KognogOS's list copied in (sudoForge box). Proven: linux-firmware and bash 3→1, bluez 3→2. The disc already ships this list (build-iso.sh). nog's own AUR default stays generic unless you decide otherwise.
4. ✅ Which AUR helper the disc ships (yay or paru) (new) — *Not decided anywhere.* **Javier:** yay (Javier, 10-22).
5. ✅ Flatpak and Flathub ready out of the box (new) — *nog manages Flatpak since 2.0.* **Javier:** Yes: Flatpak and Flathub ready out of the box (Javier, 10-22).
6. ✅ Is bitlaForge on the disc at all? (new) — *A mining app is an odd default.* **Javier:** Yes, in the installer's Forge Suite section, not pre-selected: there for anyone who wants to try it (Javier, 10-22).
7. Is 'KognogOS' free to use as a name? (new) — *A trademark search before the public launch.* **Javier:** PARKED until the LLC's bank account is open (rel-309). Split 10-24 into its steps (rel-303 to rel-308); everything found is in the brief (the Brief tag). Plan agreed 10-22.
8. Open Kognog Labs LLC's bank account (your call, 10-24) — *Everything in the name work is paid, filed and held by the LLC, so it all waits on this.* **Javier:** Your step (10-24: "I need to open the bank account first"). The brief has everything ready for after.
9. Name 1/4: your $25 Florida Bar consult (the 10-22 plan, split 10-24) — *A lawyer's half hour on KOGNOGOS vs IBM's COGNOS, who should own the name (Kognog Labs LLC?), and whether a free download counts as use in commerce. Claude prepares a one-page brief to bring.* **Javier:** PARKED until the LLC's bank account is open. The brief is ready (Brief tag): 7 questions, the search, today's fees. Book: 1-800-342-8011, Mon-Fri 8:00-5:30, or floridabar.org/public/lrs; 30 minutes for at most $25.
10. Name 2/4: KognogOS™ and one spelling everywhere (the 10-22 plan, split 10-24) — *The ™ on first mention in the READMEs and on kognogos.org; no 'Kognog OS' or other spellings left.* **Javier:** Sweep 10-24: every public page, README and the site already say KognogOS. Left: the LOGO ARTWORK reads 'Kognog OS' with a space (your call: close the gap and regenerate everywhere?); the private Vault folders 'Kognog OS' and 'Kognogos Portal' (rename or leave?); this desktop's installed wallpapers keep old file names until the package is reinstalled. The ™ waits for the consult (question 5), claimed for Kognog Labs LLC. Details in the brief, Part 3.
11. ✅ Name 3/4: a USPTO search for HYPEFORGE (and KOGNOGOS) (the 10-22 plan, split 10-24) — *The official trademark database: is any live software mark close? Rename only if one is.* **Javier:** USPTO Trademark Search, 24 Oct: HYPEFORGE, HYPE FORGE, NOGFORGE, KOGNOGOS, KOGNOG, COGNOG, KOGNOS: no marks, live or dead (the search checked against COGNOS first: it works). hypeForge keeps its name. IBM's COGNOS is live and registered in Class 9 (serial 74214762): question 1 for the lawyer.
12. Name 4/4: file KOGNOGOS, Class 9 word mark (~$350) (the 10-22 plan, split 10-24) — *After the consult, on the USPTO's site; Claude has the form's answers ready.* **Javier:** PARKED until the LLC's bank account is open. Filed by Kognog Labs LLC, not personally (your decision 10-24). USPTO fees read 24 Oct: $350 per class online; +$100 if information is missing; +$200 if the goods are not from the ID Manual; +$150 later only for an intent-to-use filing.
13. A 'support the project' button, for Kognog Labs LLC (your idea, 10-24) — *Covers costs only: the trademark, domains, the server. Development stays voluntary. The LLC's own sponsor profile, never a personal one; on the repos and kognogos.org. Wording after the consult (an LLC isn't a charity).* **Javier:** PARKED until the LLC's bank account is open. Your idea, 10-24. Options in the brief, Part 2: GitHub Sponsors takes no fee from people (up to 6% from companies; GitHub's docs) — Claude's suggestion, as a Kognog Labs organization; Open Collective's host said to take about 10% (unconfirmed); Ko-fi and Liberapay, no platform fee (secondhand). Wording after the consult.
14. Everything in Kognog Labs LLC's name (your decision, 10-24) — *From now on every registration, account, fee and payment is the LLC's; nothing in your personal name. What already is (the GitHub account and repos, kognogos.org and the other domains, the AUR packages) moves over in the order the lawyer gives.* **Javier:** Your decision, 10-24: nothing new in your personal name. What already is moves in the order the lawyer gives (question 2 of the brief). Waits on the bank account.
15. ✅ A place for people to talk (Discord, Matrix, forum) (new) — *Or GitHub only.* **Javier:** Javier, 10-22: (1) now, GitHub only; (2) then a forum in GitHub with Q&A, topics and rooms; (3) a Discord much later, if people ask.

### 01 · Clean house — Oct – Nov 2026 (12/12 done)

*Everything already built gets pushed, tested and released, so the rest builds on solid ground.*

1. ✅ Push the 9 waiting commits, issues F-79 to F-81, the Vault entry (forge-suite TODO) — *With the next phase.* **Javier:** Done 10-22 (Javier: "Push, Update, Document, make publish"): forge-suite and KognogOS pushed; issues #108–#110 opened and closed; READMEs current; Vault: hypeForge (85), Kognog OS Day 10, Forge Suite (9), the nog note; kognogos.org updated with a server backup.
2. ✅ The KognogOS project kit: CLAUDE.md for how it's built, tested, shipped (KognogOS TODO) — *Written 2026-10-22 (KognogOS CLAUDE.md: what it is, the board first, v1.0 as decided, the factory tier list, where scripts may run, tests, words and names); the board-links rule added the same night.* **Javier:** What is pending for Kognog for v2.0 is KognogOS + AI (Claude) full integration. Claude alive while the OS is on, with a tray chat bubble available for one to request directly there anything. We will create Claude commands to manipulate and control the OS, and even develop new functionalities, or make changes to it.
3. ✅ Write the per-app release recipe down (forge-suite TODO) — *Done 2026-10-22 (forge-suite 3bf99ef): docs/RELEASE-RECIPE.md + scripts/release-app.sh (build, --no-sign, --verify). Found on the way: release files weren't reproducible; now pinned to the tag's commit time.*
4. ✅ nogForge: the old commit with the book persona's name (nogForge TODO) — *Done 2026-10-22 (you ran the script: dry-run, local, push). main c60eb99 and the 8 tags re-signed and pushed; every commit holds the same files; the AUR's release file is unchanged. GitHub still serves the old commit by its exact address only; a GitHub Support request would remove it (optional).* **Javier:** fix
5. ✅ Your pending test runs: grubForge 2.2, alacrittyForge 1.1, bitlaForge 1.1, nogForge 1.4 (app TODOs) — *They had been run: 2026-10-08 inside hypeForge Settings, all passed (each app's Test Results file); nogForge 1.5.0 passed every step 2026-10-17. The TODO lines were stale. The next runs are the new versions' matrices (alacrittyForge 1.1.1, bitlaForge 1.1.1, grubForge 2.2.2).*
6. ✅ grubForge: fixes that touch Arch (#17, #19, #20, #22) (grubForge issues) — *Frozen entries, duplicates, --version.*
7. ✅ Desktop entries in every Forge app's package (grubforge #37 · alacrittyforge #18 · bitlaforge #12 · nogforge #16) — *Done 2026-10-22: alacrittyForge 1.1.1, bitlaForge 1.1.1 and grubForge 2.2.2 ship their launcher entry (nogForge's since 1.5.0); your local test all pass; all three on the AUR; #114, #118, grubForge #37 closed.*
8. ✅ Move alacrittyForge, bitlaForge, nogForge, grubForge into forge-suite (forge-suite D-60) — *Done 2026-10-22: alacrittyForge, bitlaForge, nogForge and grubForge all live in forge-suite with their full history, tags re-created signed as <app>-vX.Y.Z, open issues moved (#112-#120), old repositories archived with a pointer, ~/Programs/<app> are shortcuts. Every shipped Forge app lives in one repository now.*
9. ✅ README: the tech-stack table still says "Chrome + Brave (both shipped)" (the CLAUDE.md review, 10-22) — *Done (49284f3): the README, config/profiles.toml and the old dependency list now follow #14 — Chrome is the browser; Chrome, Claude Desktop and Claude Terminal ticked by default; Brave and Firefox offered instead. #14 stays open until the Sway disc proves it.*
10. ✅ README: the deferred list still says nogForge "now v1.4.0" (the CLAUDE.md review, 10-22) — *Done (49284f3): the README says nogForge v1.5.0.*
11. ✅ One spelling: "Kognog OS" is still in the wallpaper names and labels (the CLAUDE.md review, 10-22) — *Done (49284f3): the ten wallpapers (repo + disc copies), the disc's wallpaper package name and both scripts say KognogOS. The CHANGELOG keeps the old names as history. This desktop's Plasma configs repointed with backups. The ™ goes with Friday's trademark session.*
12. ✅ TODO.md: a stale line about build-iso.sh's hypeForge path (the CLAUDE.md review, 10-22) — *Done (49284f3): removed; build-iso.sh on main never used that path.*

### 02 · nog and nogForge, finished — Nov 2026 (15/15 done)

*The installer and the welcome app drive nog without a person; nog has to be done first.*

1. ✅ nog update --yes (unattended updates) (nog #56) — *The installer and welcome need it.* **Javier:** Released in nog 2.1.0 (10-23): GitHub + AUR 2.1.0-1 after your local install; #56 closed.
2. ✅ nog: an unattended update that ends honestly (F-21–F-24) (nog 2.1.0, 10-23) — *Found on the way to --yes, from the real update of 10-22: long AUR builds keep sudo awake (#57), an unfinished update exits 3 and says incomplete (#58), --yes checks sudo first (#59), error messages say the exit status once (#60). Built in 2.1.0; close at its release.* **Javier:** Released in nog 2.1.0 with F-25 to F-27 from your run and the VM; #57 to #63 closed.
3. ✅ nog install --yes for repository packages through the AUR helper (nog #32)
4. ✅ nog remove warns before taking an optional dependency; nog keep (nog F-13 #49) — *Elisa almost took VLC's formats with it.*
5. ✅ nog: confirm the missing 'continue?' prompt of 1 Oct is gone (nog TODO)
6. ✅ nog: the AUR helper's questions racing its table (nog TODO)
7. ✅ nog: the 'last update' record per user or per system (nog TODO) **Javier:** Your call 10-23: whole computer. Built in nog 2.1.0 rc2 (/var/lib/nog/last-update), proven in your §5.4.
8. ✅ nog: the rare library mismatch (priority 4) (nog #5)
9. ✅ nog: small follow-ups (search shows 30, info on Flatpak, reinstall, lock by version) (nog 2.0 notes) **Javier:** Your call 10-23: works as designed; lock by version moved to 1.x (pkg-156).
10. ✅ nog: the AUR description wording (nog TODO) — *At the next package bump.* **Javier:** AUR 2.1.0-1 carries the About wording with where it runs (249 bytes: the AUR refused the first, 290-byte try).
11. ✅ nog: watch the first real update that installs something (nog 2.0 matrix) — *Matrix 7.3 / 7.4, never seen on real data.*
12. ✅ nogForge: unticking with the mouse jumps the list to the top (nogForge #17)
13. ✅ nogForge: Tick all / Untick all (nogForge #18)
14. ✅ nogForge: update one package by itself (nogForge #20) — *'Too hard to get one package updated.'*
15. ✅ nogForge: Update and Uninstall buttons on each installed app (nogForge #19)

### 03 · The desktop, finished — Nov – Dec 2026 (14/14 done)

*The base every style and app sits on: the bar never vanishes, one or two screens work, pop-ups follow the standard.*

1. ✅ The bar guard: the bar comes back by itself if it ever disappears (hypeForge Phase 12) — *D-115. Built 2026-10-22 after the empty-screen login (F-82, forge-suite bc9cc2b). Why Waybar crashes is still open.*
2. ✅ One title row on every pop-up (hypeForge D-116) — *Quick Settings has none today.* **Javier:** Done 10-24, your OK: "looks good!". Every pop-up's title row drawn by the panel kit (forge-suite f3d802a, 570caf4): Quick Settings got one, seven made the same, then Power, Workspaces and the switcher ("give all popups their title"). The launchers stay each style's own.
3. ✅ Three widths only: narrow, medium, wide (hypeForge D-116)
4. ✅ The hover tip stops covering an open pop-up (hypeForge D-116)
5. ✅ The notification cards on the pop-up standard (hypeForge D-116)
6. ✅ Quick Settings: the Wi-Fi page — pick a network, connect, disconnect, the cable (hypeForge D-117) — *D-117 (Javier, 2026-10-25): inside the Quick Settings card (‹ Quick Settings to go back), or alone from a bar icon. Networks nearby, strongest first; a password box when needed. Mock first.*
7. ✅ Quick Settings: the Bluetooth page — on/off, your devices, connect, disconnect (hypeForge D-117) — *D-117: 'Pair a new device…' opens bluetoothForge (bluetui until it exists). Mock first.*
8. ✅ Quick Settings holds night light and sound too; the moon leaves every bar (hypeForge D-117) — *D-117 (Javier, 2026-10-25): the Night light and Sound pages inside Quick Settings; the moon off every style's bar, nightForge's own icon steps aside (1.1.1). The optional bar icons moved to 1.x (pop-092).*
9. ✅ Night light hides its own tray icon where the bar already shows the moon (forge-suite #82) — *nightForge 1.1.*
10. ✅ displayForge: tested with one and two screens (displayForge 1.1.x)
11. ✅ displayForge: 80 / 90 % sizes on real apps (displayForge 1.1.x) — *X11 apps blur at non-whole sizes.*
12. ✅ displayForge: tested on a plain text console (displayForge 1.1.x)
13. ✅ displayForge: the 'not tried yet' text during the countdown (displayForge 1.1.x) — *A small bug seen in screenshots.* **Javier:** Fixed 10-24 (F-8, forge-suite #121, 52b9a24): during the countdown the bar says 'Trying N changes on your screens'. Ships with displayForge's next release and its test run.
14. ✅ workspaceForge: tested with one or two screens, and on a text console (workspaceForge Phase 2)

### 04 · The four styles and their colours — Dec 2026 (0/7 done)

*Rice, Windows 11, KDE and Classic, each reviewed piece by piece; then the colour themes that make the cut; then themeForge 1.0.*

1. The floating-island bar (the Rice) ships in 1.0 — KognogOS's default look (hypeForge D-78) — *In review since 2026-10-27 (look-071): the bar approved; the launcher is now COSMIC's App Library (D-118); its icons wear the text colour in every theme (D-119).*
2. The taskbar-with-Start look ships in 1.0 (hypeForge D-71) — *Your daily driver right now.*
3. The floating-panel-with-a-pager look ships in 1.0 (hypeForge D-76)
4. Classic style ships in 1.0 (hypeForge) — *The plain first look.*
5. Full review of each style that ships: bar, launcher, tray, every pop-up (hypeForge Phase 12) — *Step by step, your look on each piece. The Rice first (started 10-27, checklist in hypeForge testing/): ✅ the bar · ✅ its icons wear the text colour in all 25 themes (D-119) · ✅ the launcher = COSMIC's App Library, the list saved as a theme option (D-118) · ✅ Quick Settings: one-colour icons + short sound names, every style (D-120) · found on the way: a switch brings the theme's own wallpaper (D-121), the volume chimes on letting go (D-122), the see-through strip under floating windows' title bars (F-87, live at next login) · ⏳ the calendar · then system pop-ups, clipboard, power, lists, Alt + Tab, notifications, windows · the tray + the whole look on your real desktop at the end. Then Windows 11, KDE, Classic.* **Javier:** Only what we will be shipping!
6. Ship fewer colour themes in 1.0 and add the rest during the year (new) — *25 × every style is a lot to prove.*
7. themeForge 1.0 released (GitHub + AUR) (themeForge Phase 3) — *The Look settings app.*

### 05 · Passwords — Dec 2026 – Jan 2027 (0/8 done)

*walletForge has to replace KDE's wallet before the disc ships without KDE; sudoForge gets its compact box and its GPG prompt.*

1. walletForge: research what the saved-logins standard needs (walletForge Phase 0) — *Must land before KDE leaves.*
2. walletForge: the store and its encryption (walletForge Phase 0)
3. walletForge: copy the entries over from KDE's wallet (walletForge Phase 0)
4. walletForge: the service, unlocked at login (walletForge Phase 1) — *Chrome, Claude Desktop and Discord keep their logins.*
5. walletForge: the Passwords page in Settings (walletForge Phase 0) — *Like Chrome's password manager.*
6. sudoForge: a compact password box (forge-suite #62) — *'To much real state waste.'*
7. sudoForge: our own GPG passphrase prompt (sudoForge later) — *Drops a GNOME piece.*
8. sudoForge: fold the session agent back into forgekit (sudoForge later)

### 06 · The Settings apps — Jan 2027 (0/11 done)

*The Mint-sized set, in the order you set on 10-07: sound, network, Bluetooth first.*

1. Sound app (outputs, inputs, each app's volume) (hypeForge track 7) — *Today: wiremix, themed.*
2. networkForge: the Network & Wi-Fi app (hypeForge track 8) — *Named 2026-10-25 (D-117): saved networks, forget, hidden networks, details; VPN, hotspot, fixed IP in 1.x. Today: the network menu + nmtui.*
3. bluetoothForge: the Bluetooth app (hypeForge track 9) — *Named 2026-10-25 (D-117): pair a new device (search, pair, trust), forget. Today: bluetui.*
4. Default apps: defaultappsForge 1.0 after your run (defaultappsForge) — *Built 10-09, waiting on your run.*
5. Power & Lock (idle, sleep, lock screen) (hypeForge track 13)
6. Keyboard (layout, repeat, the key chart) (hypeForge track 16)
7. Typing Chinese, Japanese or Korean (input methods) (new) **Javier:** Yes, typing in 1.0; the OS in other languages comes later (Javier, 10-22).
8. Mouse & Touchpad (hypeForge track 17) — *Touchpad matters on laptops.*
9. Time & Language (hypeForge track 18)
10. Users (hypeForge track 21)
11. About this computer (hypeForge track 22) — *The greeting window does it today.*

### 07 · First boot — Jan – Feb 2027 (0/8 done)

*What someone sees the first time: the greeting, the prompt, the Welcome Center, the tier guide, the help pages, now that the desktop has settled.*

1. A shell prompt that looks right on a plain text console (KognogOS #12) — *It looks awful on a tty today.*
2. The KognogOS greeting as its own packaged app (KognogOS #4)
3. greetForge: a text-console version of the greeting (KognogOS #8)
4. The tier guide: a plain-language manual of what each tier means (KognogOS roadmap) — *How to read and edit tier-pins.toml, with examples.*
5. welcomeForge: the Welcome Center (KognogOS roadmap) — *Opens at session start. On the live disc it leads with Install; once installed, a 'show at startup' switch.*
6. welcomeForge: a guided nog tour (KognogOS roadmap)
7. welcomeForge: where to give feedback (KognogOS roadmap) — *Points to GitHub Issues.*
8. Help & Keys pages current for 1.0 (new) — *Every guide page checked against what ships.*

### 08 · Our Sway, packaged — Feb 2027 (0/3 done)

*The disc can't build Sway in a home folder. A package, held back until our patches fit each new Sway. Moved here on 10-24 (Javier): the desktop and the styles decide the final set of patches, and until the disc nobody else runs it; this desktop is already safe (our build falls back to Arch's Sway when it doesn't fit).*

1. Our Sway build as a KognogOS package (hypeForge D-111) — *Today it's built in your home folder; the disc needs a package.*
2. Hold Sway updates until our patches fit the new version (new) — *So an Arch update never ships a desktop without its buttons.*
3. Offer our patches to Sway upstream (new) — *The title bar buttons and the pointer position.*

### 09 · The disc's foundations — Feb 2027 (0/20 done)

*The ISO recipe rebuilt for Sway: what goes on it, the known install bugs, the editions, the login screen, a live session that starts on any graphics card.*

1. Decide the machine that builds the ISO (a VM?) (the CLAUDE.md review, 10-22) — *build-iso.sh doesn't check where it runs; the 09-30 accident happened on this desktop.*
2. build-iso.sh: stop staging Plasma, point at forge-suite/hypeforge (KognogOS TODO) — *Line 42 still looks for ~/Programs/hypeforge.*
3. The disc's package list = what hypeForge and the Forge apps need (forge-suite #91) — *Measured in each app's docs/PACKAGING.md (the dependency audit).*
4. Prove every font hypeForge needs is on the disc (KognogOS TODO) — *docs/FONTS.md lists them; the Nerd Font symbols were added 10-05, never proven by a build.*
5. Remove the repeated nano and tmux lines (KognogOS TODO) — *Harmless, but sloppy.*
6. sudoForge on the disc, set up at first boot (KognogOS TODO) — *Without it there is no admin password window on Sway.*
7. Brightness keys: brightnessctl on the disc, or bind them to displayForge (forge-suite #94) — *A laptop's brightness keys do nothing today.*
8. The login's pam_kwallet_init is missing on the disc (forge-suite #95) — *Either kwallet-pam ships, or walletForge replaces it.*
9. nogForge on the disc (nogForge TODO) — *It isn't in the package list yet.*
10. Boot identity required in the installed system, not just the live disc (KognogOS #2) — *Installer recipe.*
11. Fresh install lacks fakeroot and nog's signing key (KognogOS #9) — *Found by nog's VM test.*
12. AUR builds work on an installed system (base-devel) (KognogOS #11) — *Fixed on main; close after the next disc build proves it.*
13. The os-release hook errors inside every clean chroot (KognogOS #16) — *Seen when building packages on a KognogOS box.*
14. Basic edition: the app list redone without KDE apps (KognogOS README) — *Today's lists date from the Plasma build.*
15. Work edition (the old Office): the app list redone (KognogOS README) — *OnlyOffice, Obsidian, Thunderbird… minus the KDE pieces.* **Javier:** Renamed Work (Javier, 10-22).
16. The Craft apps (storytold / ArtCraft): try them, then decide which join the recommended apps (Javier, 10-26) — *Javier, 2026-10-26: consider the Craft Suite for our recommended apps, after he tries them. About 15 apps, all open source (Apache-2.0), written in Rust: WordCraft, GridCraft, DeckCraft and PdfCraft (Word, Excel, PowerPoint and PDF style: the Work edition), plus PhotoCraft, LightCraft, VectorCraft, FilmCraft, EffectCraft, SoundCraft, DesignCraft, CADCraft and FigCraft (a creative set). Linux builds for each; the Craft Launcher installs and updates them all and is on the AUR (artcraft-launcher 0.8.1). Very young and moving daily (launcher 0.7 → 0.8.1 in two days), so: his try on this desktop (via nog), then a pick per edition: Work, the optional apps in installForge, or later (Full).*
17. Chrome, Claude Desktop and Claude Terminal pre-selected; Brave no longer the default (KognogOS #14) — *Your decision of 10-07.*
18. Proprietary apps marked in the installer, with a free swap (KognogOS README) — *Defined in config/profiles.toml.*
19. Pick and theme the login screen for Sway (KognogOS roadmap) — *The roadmap says it's part of the hypeForge disc; nothing is chosen yet.*
20. The live disc starts Sway on any graphics card (VM, NVIDIA, AMD, Intel) (new) — *Today it's only proven on this desktop.*

### 10 · installForge — Feb – Mar 2027 (0/13 done)

*The installer, step by step in the order a person meets them, then the advanced parts.*

1. installForge: the terminal installer as a Forge Suite section (KognogOS Phase 3) — *Today it's a first-draft shell script.*
2. installForge installs online (the CLAUDE.md review, 10-22) — *Today's draft (kognog-install.sh) copies the live disc, so it installs offline.*
3. installForge: keyboard layout, language and time zone steps (new) — *Not written down anywhere yet.*
4. installForge: Wi-Fi setup inside the installer (new) — *The install is online-only, so a laptop needs Wi-Fi before anything else.*
5. installForge: guided disk setup (whole disk, or free space next to Windows) (KognogOS Phase 3) — *Dual boot is the common case.*
6. installForge: user creation (KognogOS Phase 3) — *Name, password, the admin rights.*
7. installForge: the edition picker (KognogOS Phase 3) — *Reads config/profiles.toml.*
8. installForge: a Forge Suite section of optional apps (bitlaForge offered, not pre-selected) (your answer, 10-22) — *People who want to try an app tick it.*
9. installForge: pick the graphics driver (NVIDIA, AMD, Intel) by itself (new) — *Sway on NVIDIA needs its own flags; the installer must know.*
10. installForge: bootable snapshots from the boot menu (KognogOS Phase 3) — *btrfs snapshots you can boot into after a bad update.*
11. installForge: 'prepare for a new owner' mode (KognogOS Phase 3) — *The personal questions wait for the new owner's first boot.*
12. System Lock: only nog may drive package changes (managed mode) (KognogOS #10)
13. Rebuild the disc around Sway + hypeForge (KognogOS #13) — *The ISO still stages the Plasma desktop. The 1.0 disc is Sway only.*

### 11 · Testing — Mar 2027 (0/9 done)

*A VM until zero problems, then the real thing: the NVMe in this PC, then a laptop.*

1. Good behaviour inside a VM (guest tools, screen size) (new) — *Many people try a new distro in a VM first.*
2. Install the disc in a VM until a run has zero problems (KognogOS Phase 4) **Javier:** and we are going to install it in the NVMe that is waiting in this pc
3. Our Sway's login fallback on a fresh install (hypeForge) — *Proven in the VM; not from the disc.*
4. Screen sharing in Chrome and Discord out of the box (new) — *Worked here after installing the portal by hand.*
5. Firewall on by default, checked on the installed system (new) — *The README promises it.*
6. A test pass per edition (new)
7. Wipe a real machine and install from the disc alone, until zero problems (KognogOS Phase 4)
8. Test on a laptop (Intel or AMD graphics, battery, Wi-Fi) (new) — *Everything so far ran on this NVIDIA desktop.*
9. Laptops: install the first full beta ISO on a laptop and try it — what's missing decides 1.0 or 1.x (the cut, 10-21) — *Wi-Fi, touchpad, brightness, battery, lid, sleep: judged on real hardware, not on paper.* **Javier:** Javier, 10-22: move it to when we have the first ISO beta, with everything, for me to install on a laptop and try.

### 12 · The release kit — late Mar – early Apr 2027 (0/10 done)

*Everything a stranger needs before they download: the legal and privacy lines, the site, the guide, the ISO's home and signature.*

1. A licence check of everything the disc installs (new) — *Proprietary apps marked; nothing redistributed that can't be.*
2. A privacy line: what KognogOS does and doesn't send anywhere (new)
3. Issue templates on GitHub for feedback (new) — *GitHub Issues is the one door.*
4. Check what kognogos.org shows people who aren't signed in (new) — *The portal guards our sites; the public page must stay public.*
5. Screenshots and a banner of 1.0 for the site and the README (new)
6. A getting-started guide on the site (new) — *Install, first boot, nog, where help lives.*
7. The KognogOS manual: one source, two places — the built-in Help and a Docs section on kognogos.org (Javier, 2026-10-25) — *Javier, 2026-10-25: the artifacts 'can become part of our KognogOS manual, and online (or in system offline) documentation' → 'two places for the manual'. One source: the repos' text files (hypeForge's Help guide, each app's manual). Offline: the Help app and each app's M key. Online: a Docs section on kognogos.org built from the same files. A full manual pass once the apps stop changing.*
8. Where the ISO is downloaded from (hosting) (KognogOS Phase 5)
9. Checksums and a signature for the ISO (KognogOS Phase 5)
10. kognogos.org: a download page and the release notes (KognogOS Phase 5)

### 13 · Launch — the week of 19 April 2027 (0/3 done)

*Two years after the wish that started it.*

1. The KognogOS 1.0 GitHub Release (KognogOS Phase 6)
2. Announcements (KognogOS Phase 6) — *Where, and in what words.*
3. DistroWatch submission (KognogOS Phase 6) — *Their queue takes months.*

## 1.x — during the first year (78)

### The disc and the installer

- Gaming edition: the app list redone (KognogOS README) — *Steam, Lutris, Heroic, Proton-GE, RetroArch… checked on Sway.* **Javier:** Not in 1.0: only Basic + Work ship (Javier, 10-22).
- Development edition: the app list redone (KognogOS README) — *VS Code, Neovim, toolchains, Docker…* **Javier:** Not in 1.0: only Basic + Work ship (Javier, 10-22).
- Full edition: everything above (KognogOS README) — *Follows from the four lists.* **Javier:** Not in 1.0: only Basic + Work ship (Javier, 10-22).
- installForge: disk encryption on by default, with a way to skip it (KognogOS Phase 3) — *Learned from Omarchy's installer.*
- installForge: the Development edition suggests reviewing tier pins (KognogOS Phase 3) — *For people whose toolchain needs newer packages.*

### First boot and welcome

- promptForge: switch prompt themes without editing fish files (KognogOS #5)

### The desktop

- Any number of screens, from one to six (hypeForge track 12b) — *Today's settings assume this desk's three. The roadmap calls it 'the ISO gate'.*
- Laptops: battery on the bar, closing the lid, sleep (new) — *Not written down anywhere yet. This desk has no battery.*
- Screens at high resolution: a sensible size on first boot (new) — *A 4K laptop at 100 % is unreadable.*
- A tray restart that keeps Electron apps' icons (hypeForge Phase 12) — *Today: never restart the tray live; changes wait for the next login.*
- Folder-style tabs (hypeForge Phase 12) — *Small tabs like folders in a holder, replacing Sway's even tab row.*
- Drag and drop windows onto each other to tab or stack them (hypeForge track 25)
- Apps that draw their own title bar (Chrome…): switch it off where the app allows (hypeForge Phase 12) — *You moved it last in Phase 12.*
- More than nine workspaces (workspaceForge D-6) — *The cell numbering has to change first.*
- Workspace sharing, rethought (workspaceForge D-7) — *Waiting on your thinking.*
- The frost: see-through, blurred bars on the FX login (forge-suite #83)
- The notch on big windows' rounded corners (SwayFX) (forge-suite #64) — *Reported upstream as swayfx#600.*
- Screen recording (new) — *Screenshots are done; video isn't.*

### Styles and colour themes

- The top-panel-with-a-dock look ships in 1.0 (hypeForge D-77) — *Your score: 0/100.*
- The classic menu-bar look ships in 1.0 (hypeForge D-72) — *Your call: held for the year.*
- The modern menu-bar-with-a-dock look ships in 1.0 (hypeForge D-74) — *Your call: held for the year.*
- The top-panel look's launcher: a full page of apps (hypeForge D-116) — *Goes with the COSMIC style.*
- All 25 colour themes reviewed on each style that ships (hypeForge Phase 12) — *Light and dark, readable everywhere.*
- The menu card for the two menu-bar looks' Window, Special and Help (hypeForge D-116) — *Goes with the Mac styles.*
- The app name's odd 'gimp' box on the menu-bar looks (hypeForge review) — *Goes with the Mac styles.*
- The lock screen's box follows the corners switch (hypeForge D-81)
- Separate corners for the bar and for windows (themeForge) — *An idea from 10-10.*
- themeForge: a Corners page (themeForge Phase 2)
- themeForge: Pop-ups, Icons and Fonts pages (themeForge Phase 2)
- themeForge: the quick-switch tray icon (themeForge D-78)
- themeForge: drop old wallpaper copies right away (themeForge) — *Today they wait for the 40-picture cap.*

### Pop-ups

- Pop-ups open right under what you clicked (hypeForge D-116) — *Our Sway's patch 3 makes it possible; plain Sway keeps today's spots.* **Javier:** this has been a MAC OSes issue. We will work later.
- A setting for where each pop-up opens (hypeForge settings catalogue) — *Centre, under the button, a corner.*
- Bar icons optional: the combined status piece, or separate icons per style (hypeForge D-117) — *D-117, moved to 1.x by Javier on 2026-10-25 ('yes, move it to 1.x'): Wi-Fi, Bluetooth, sound, night light, printer each with its own bar icon, chosen in themeForge's element pages.*

### Settings apps

- Notifications app (mako's settings) (hypeForge track 14)
- Startup apps (hypeForge track 15) — *Applet 10 does it from a folder today.*
- printerForge (the Printers app) (hypeForge track 19) — *Printing already works driverless.*
- USB drives & disks app (hypeForge track 20) — *The Disks pop-up does mount and eject today.*
- Windows app: placement, float rules, tiling (hypeForge track 12b)
- Launcher settings: sections, favourites, its look (hypeForge Settings)
- Lock screen look settings (hypeForge Settings)
- A Calculator in our look (hypeForge roadmap) — *galculator meanwhile.*
- fileForge: our own file manager (hypeForge Phase 13) — *Thunar meanwhile.*
- Game controllers + the G13 app (hypeForge after 1.0)
- Accessibility (large text and pointer) (hypeForge after 1.0)
- Online accounts (hypeForge after 1.0)
- Remote desktop (hypeForge after 1.0)
- Touchscreen (hypeForge after 1.0)
- App permissions (hypeForge after 1.0)
- Spell check (hypeForge after 1.0)
- Animations (hypeForge after 1.0)
- displayForge: profiles that switch when screens plug in or out (displayForge later)
- Our own text-mode versions of the other apps we use (hypeForge Phase 14) — *Phase 14: fork or write from zero.*

### Passwords and security

- An update reminder people actually see (new) — *Quick Settings shows a count; nothing pings.*
- Secure Boot (new) — *Many laptops ship with it on.*

### Packages: nog and nogForge

- nogForge: Downgrade button (nogForge #19) — *Needs a design pass and nog's say.*
- nogForge: the Settings page (holds, sources, repositories) (nogForge TODO) — *Security-sensitive.*
- nogForge: nog's run inside the window, redesigned (nogForge TODO) — *'It is not beautiful, it is disrupting.'*
- nog: lock a package by version (your answer, 10-23) — *Lock a package at the version it has, so a new one waits; today nog lock is by name only. From the 2.0.0 follow-ups (pkg-142).*

### The other Forge apps

- grubForge: other distros (#24, #25, #34, #35) (grubForge issues) — *Debian, Ubuntu, Fedora, openSUSE.*
- grubForge: screenshots still show old labels (grubForge TODO)
- alacrittyForge: edit the hints, mouse shortcuts (alacrittyforge #16 #17)
- bitlaForge: bug fixes (Esc in a field, the console key) (bitlaforge #3)
- bitlaForge: new features (charts, saved setups, restart the miner…) (bitlaforge #9 #10 #11)
- The 'where it runs' AUR descriptions, app by app (app TODOs) — *At each app's next release.*
- cloneForge: moving a system to a new drive (KognogOS README)

### Leaving KDE

- List every KDE piece still in use on the Sway desktop (new) — *The wallet, the network applet, breeze… measured, not guessed.*
- Remove KDE from this desktop (Phase 15) (hypeForge Phase 15 · forge-suite #10) — *The very last step, once everything is proven.*

### Release kit and public face

- A forum in GitHub (Discussions): Q&A, common topics, rooms, GitHub activity gathered (your answer, 10-22) — *Step 2 of the community, after GitHub alone.*
- A Discord, if people ask for it (your answer, 10-22) — *Step 3 of the community, much later.*

### Testing before release

- Games on Sway: Steam, Proton, full screen, the pointer (new) — *WoW's pointer bug was found this way.*

### Gaps nobody had written down

- Languages other than English in our apps (new) — *Every Forge app is English only.* **Javier:** Later (Javier, 10-22).
- A screen reader (new) **Javier:** Later (Javier, 10-22). A screen reader reads the screen aloud for people who can't see it.
- Snapshots before every update, with a way back (new) **Javier:** Later (Javier, 10-22).
- A backup app for people's own files (new) **Javier:** Later (Javier, 10-22).
- An emoji and special-character picker (new)
- A 'report a problem' button that opens a pre-filled issue (new)
- Hibernate (new) — *Sleep yes; hibernate is fragile on NVIDIA.* **Javier:** Later (Javier, 10-22).

## Dropped (6)

### The disc and the installer

- A graphical installer (KognogOS README) — *Already deferred: after installForge proves the flow.*
- Our own package repository (KognogOS README) — *Already deferred: the official repos and the AUR carry everything.*

### The desktop

- World of Warcraft (Wine) matched to its workspace (workspaceForge) — *Its window calls itself wow.exe.* **Javier:** World of Warcraft it is not part of the distro. Azerothcore is a project only for me, my family, and friends.

### The other Forge apps

- alacrittyForge: onto the newer forgekit pieces (alacrittyForge TODO) **Javier:** Dropped (Javier, 2026-10-22): no line said which forgekit pieces; 1.1.0 is already on forgekit 0.10.0.
- mcForge (Midnight Commander settings or fork) (forge-suite ideas)

### Release kit and public face

- The 'Arch' brand variant (KognogOS README) — *Already deferred to a future year.*
