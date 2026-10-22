# KognogOS 1.0 — the cut

*Decided by Javier on 2026-10-21, item by item, on the board [KognogOS 1.0 Cut](https://claude.ai/artifact/6UswcvpQ4EnWek5iVtBy5G) (207 items from every project's TODO and the open issues, plus 40 gaps written down for the first time). The board stays the live record; this file is its snapshot.*

**127 ship in v1.0 (April 2027) · 67 come during the first year (1.x updates) · 5 dropped · 8 still open.**

In short: v1.0 ships the **Rice, Windows 11, KDE and Classic** styles with a **smaller set of colour themes**; the Mac styles and COSMIC come during the year. The installer ships with bootable snapshots and the new-owner mode. nog, nogForge, walletForge and sudoForge are finished for 1.0, and the shipped apps move into forge-suite. Pop-ups opening under the click, any number of screens, laptop polish and removing KDE from the test desktop are 1.x.

**Beyond the year — v2.0 (Javier):** *KognogOS + AI (Claude) full integration. Claude alive while the OS is on, with a tray chat bubble available for one to request directly there anything. We will create Claude commands to manipulate and control the OS, and even develop new functionalities, or make changes to it.*

## v1.0 (127)

### The disc and the installer

- Rebuild the disc around Sway + hypeForge (KognogOS #13) — *The ISO still stages the Plasma desktop. The 1.0 disc is Sway only.*
- build-iso.sh: stop staging Plasma, point at forge-suite/hypeforge (KognogOS TODO) — *Line 42 still looks for ~/Programs/hypeforge.*
- The disc's package list = what hypeForge and the Forge apps need (forge-suite #91) — *Measured in each app's docs/PACKAGING.md (the dependency audit).*
- Prove every font hypeForge needs is on the disc (KognogOS TODO) — *docs/FONTS.md lists them; the Nerd Font symbols were added 10-05, never proven by a build.*
- Remove the repeated nano and tmux lines (KognogOS TODO) — *Harmless, but sloppy.*
- sudoForge on the disc, set up at first boot (KognogOS TODO) — *Without it there is no admin password window on Sway.*
- Brightness keys: brightnessctl on the disc, or bind them to displayForge (forge-suite #94) — *A laptop's brightness keys do nothing today.*
- The login's pam_kwallet_init is missing on the disc (forge-suite #95) — *Either kwallet-pam ships, or walletForge replaces it.*
- Boot identity required in the installed system, not just the live disc (KognogOS #2) — *Installer recipe.*
- Fresh install lacks fakeroot and nog's signing key (KognogOS #9) — *Found by nog's VM test.*
- AUR builds work on an installed system (base-devel) (KognogOS #11) — *Fixed on main; close after the next disc build proves it.*
- The os-release hook errors inside every clean chroot (KognogOS #16) — *Seen when building packages on a KognogOS box.*
- Basic edition: the app list redone without KDE apps (KognogOS README) — *Today's lists date from the Plasma build.*
- Office edition: the app list redone (KognogOS README) — *OnlyOffice, Obsidian, Thunderbird… minus the KDE pieces.*
- Gaming edition: the app list redone (KognogOS README) — *Steam, Lutris, Heroic, Proton-GE, RetroArch… checked on Sway.*
- Development edition: the app list redone (KognogOS README) — *VS Code, Neovim, toolchains, Docker…*
- Full edition: everything above (KognogOS README) — *Follows from the four lists.*
- Chrome, Claude Desktop and Claude Terminal pre-selected; Brave no longer the default (KognogOS #14) — *Your decision of 10-07.*
- Proprietary apps marked in the installer, with a free swap (KognogOS README) — *Defined in config/profiles.toml.*
- Pick and theme the login screen for Sway (KognogOS roadmap) — *The roadmap says it's part of the hypeForge disc; nothing is chosen yet.*
- installForge: the terminal installer as a Forge Suite section (KognogOS Phase 3) — *Today it's a first-draft shell script.*
- installForge: the edition picker (KognogOS Phase 3) — *Reads config/profiles.toml.*
- installForge: guided disk setup (whole disk, or free space next to Windows) (KognogOS Phase 3) — *Dual boot is the common case.*
- installForge: user creation (KognogOS Phase 3) — *Name, password, the admin rights.*
- installForge: keyboard layout, language and time zone steps (new) — *Not written down anywhere yet.*
- installForge: pick the graphics driver (NVIDIA, AMD, Intel) by itself (new) — *Sway on NVIDIA needs its own flags; the installer must know.*
- installForge: Wi-Fi setup inside the installer (new) — *The install is online-only, so a laptop needs Wi-Fi before anything else.*
- installForge: 'prepare for a new owner' mode (KognogOS Phase 3) — *The personal questions wait for the new owner's first boot.*
- installForge: bootable snapshots from the boot menu (KognogOS Phase 3) — *btrfs snapshots you can boot into after a bad update.*
- The live disc starts Sway on any graphics card (VM, NVIDIA, AMD, Intel) (new) — *Today it's only proven on this desktop.*
- System Lock: only nog may drive package changes (managed mode) (KognogOS #10)
- This desktop runs nog's stock tier list, not KognogOS's. On purpose? (hypeForge open question) — *Open question since 09-28.*
- The KognogOS project kit: CLAUDE.md for how it's built, tested, shipped (KognogOS TODO) — *The only project still missing it.* **Javier:** What is pending for Kognog for v2.0 is KognogOS + AI (Claude) full integration. Claude alive while the OS is on, with a tray chat bubble available for one to request directly there anything. We will create Claude commands to manipulate and control the OS, and even develop new functionalities, or make changes to it.

### First boot and welcome

- welcomeForge: the Welcome Center (KognogOS roadmap) — *Opens at session start. On the live disc it leads with Install; once installed, a 'show at startup' switch.*
- welcomeForge: a guided nog tour (KognogOS roadmap)
- welcomeForge: where to give feedback (KognogOS roadmap) — *Points to GitHub Issues.*
- The tier guide: a plain-language manual of what each tier means (KognogOS roadmap) — *How to read and edit tier-pins.toml, with examples.*
- A shell prompt that looks right on a plain text console (KognogOS #12) — *It looks awful on a tty today.*
- The KognogOS greeting as its own packaged app (KognogOS #4)
- greetForge: a text-console version of the greeting (KognogOS #8)

### The desktop

- The bar guard: the bar comes back by itself if it ever disappears (hypeForge Phase 12) — *D-115. The 10-17 silent exit is still unexplained.*
- Night light hides its own tray icon where the bar already shows the moon (forge-suite #82) — *nightForge 1.1.*
- Help & Keys pages current for 1.0 (new) — *Every guide page checked against what ships.*

### Styles and colour themes

- The Rice ships in 1.0 (KognogOS's default look) (hypeForge D-78)
- Windows 11 style ships in 1.0 (hypeForge D-71) — *Your daily driver right now.*
- KDE style ships in 1.0 (hypeForge D-76)
- Classic style ships in 1.0 (hypeForge) — *The plain first look.*
- Full review of each style that ships: bar, launcher, tray, every pop-up (hypeForge Phase 12) — *Step by step, your look on each piece.* **Javier:** Only what we will be shipping!
- Ship fewer colour themes in 1.0 and add the rest during the year (new) — *25 × every style is a lot to prove.*
- themeForge 1.0 released (GitHub + AUR) (themeForge Phase 3) — *The Look settings app.*

### Pop-ups

- The hover tip stops covering an open pop-up (hypeForge D-116)
- One title row on every pop-up (hypeForge D-116) — *Quick Settings has none today.*
- Three widths only: narrow, medium, wide (hypeForge D-116)
- The notification cards on the pop-up standard (hypeForge D-116)

### Settings apps

- Sound app (outputs, inputs, each app's volume) (hypeForge track 7) — *Today: wiremix, themed.*
- Network & Wi-Fi app (hypeForge track 8) — *Today: the network menu + nmtui.*
- Bluetooth app (hypeForge track 9) — *Today: bluetui.*
- Default apps: defaultappsForge 1.0 after your run (defaultappsForge) — *Built 10-09, waiting on your run.*
- Power & Lock (idle, sleep, lock screen) (hypeForge track 13)
- Keyboard (layout, repeat, the key chart) (hypeForge track 16)
- Mouse & Touchpad (hypeForge track 17) — *Touchpad matters on laptops.*
- Time & Language (hypeForge track 18)
- About this computer (hypeForge track 22) — *The greeting window does it today.*
- Users (hypeForge track 21)
- displayForge: tested with one and two screens (displayForge 1.1.x)
- displayForge: 80 / 90 % sizes on real apps (displayForge 1.1.x) — *X11 apps blur at non-whole sizes.*
- displayForge: tested on a plain text console (displayForge 1.1.x)
- displayForge: the 'not tried yet' text during the countdown (displayForge 1.1.x) — *A small bug seen in screenshots.*
- workspaceForge: tested with one or two screens, and on a text console (workspaceForge Phase 2)

### Passwords and security

- walletForge: research what the saved-logins standard needs (walletForge Phase 0) — *Must land before KDE leaves.*
- walletForge: the store and its encryption (walletForge Phase 0)
- walletForge: copy the entries over from KDE's wallet (walletForge Phase 0)
- walletForge: the service, unlocked at login (walletForge Phase 1) — *Chrome, Claude Desktop and Discord keep their logins.*
- walletForge: the Passwords page in Settings (walletForge Phase 0) — *Like Chrome's password manager.*
- sudoForge: a compact password box (forge-suite #62) — *'To much real state waste.'*
- sudoForge: our own GPG passphrase prompt (sudoForge later) — *Drops a GNOME piece.*
- sudoForge: fold the session agent back into forgekit (sudoForge later)
- Firewall on by default, checked on the installed system (new) — *The README promises it.*

### Packages: nog and nogForge

- nog update --yes (unattended updates) (nog #56) — *The installer and welcome need it.*
- nog remove warns before taking an optional dependency; nog keep (nog F-13 #49) — *Elisa almost took VLC's formats with it.*
- nog: confirm the missing 'continue?' prompt of 1 Oct is gone (nog TODO)
- nog: watch the first real update that installs something (nog 2.0 matrix) — *Matrix 7.3 / 7.4, never seen on real data.*
- nog install --yes for repository packages through the AUR helper (nog #32)
- nog: the AUR helper's questions racing its table (nog TODO)
- nog: the 'last update' record per user or per system (nog TODO)
- nog: the rare library mismatch (priority 4) (nog #5)
- nog: small follow-ups (search shows 30, info on Flatpak, reinstall, lock by version) (nog 2.0 notes)
- nog: the AUR description wording (nog TODO) — *At the next package bump.*
- nogForge on the disc (nogForge TODO) — *It isn't in the package list yet.*
- nogForge: unticking with the mouse jumps the list to the top (nogForge #17)
- nogForge: Tick all / Untick all (nogForge #18)
- nogForge: update one package by itself (nogForge #20) — *'Too hard to get one package updated.'*
- nogForge: Update and Uninstall buttons on each installed app (nogForge #19)
- Which AUR helper the disc ships (yay or paru) (new) — *Not decided anywhere.*
- Flatpak and Flathub ready out of the box (new) — *nog manages Flatpak since 2.0.*
- nogForge: the old commit with the book persona's name (nogForge TODO) — *History rewrite: your call.* **Javier:** fix

### The other Forge apps

- Desktop entries in every Forge app's package (grubforge #37 · alacrittyforge #18 · bitlaforge #12 · nogforge #16) — *So they show in any launcher.*
- Is bitlaForge on the disc at all? (new) — *A mining app is an odd default.*
- grubForge: fixes that touch Arch (#17, #19, #20, #22) (grubForge issues) — *Frozen entries, duplicates, --version.*
- Your pending test runs: grubForge 2.2, alacrittyForge 1.1, bitlaForge 1.1, nogForge 1.4 (app TODOs) — *Matrices written, not run.*
- Move alacrittyForge, bitlaForge, nogForge, grubForge into forge-suite (forge-suite D-60)
- Write the per-app release recipe down (forge-suite TODO) — *Proven, not documented.*

### Our Sway build

- Our Sway build as a KognogOS package (hypeForge D-111) — *Today it's built in your home folder; the disc needs a package.*
- Hold Sway updates until our patches fit the new version (new) — *So an Arch update never ships a desktop without its buttons.*
- Offer our patches to Sway upstream (new) — *The title bar buttons and the pointer position.*

### Release kit and public face

- Where the ISO is downloaded from (hosting) (KognogOS Phase 5)
- Checksums and a signature for the ISO (KognogOS Phase 5)
- kognogos.org: a download page and the release notes (KognogOS Phase 5)
- Check what kognogos.org shows people who aren't signed in (new) — *The portal guards our sites; the public page must stay public.*
- Screenshots and a banner of 1.0 for the site and the README (new)
- A getting-started guide on the site (new) — *Install, first boot, nog, where help lives.*
- A privacy line: what KognogOS does and doesn't send anywhere (new)
- Issue templates on GitHub for feedback (new) — *GitHub Issues is the one door.*
- A licence check of everything the disc installs (new) — *Proprietary apps marked; nothing redistributed that can't be.*
- Is 'KognogOS' free to use as a name? (new) — *A trademark search before the public launch.*
- A place for people to talk (Discord, Matrix, forum) (new) — *Or GitHub only.* **Javier:** GitHub only... for now
- The KognogOS 1.0 GitHub Release (KognogOS Phase 6)
- Announcements (KognogOS Phase 6) — *Where, and in what words.*
- DistroWatch submission (KognogOS Phase 6) — *Their queue takes months.*
- Push the 9 waiting commits, issues F-79 to F-81, the Vault entry (forge-suite TODO) — *With the next phase.*

### Testing before release

- Install the disc in a VM until a run has zero problems (KognogOS Phase 4) **Javier:** and we are going to install it in the NVMe that is waiting in this pc
- Wipe a real machine and install from the disc alone, until zero problems (KognogOS Phase 4)
- Test on a laptop (Intel or AMD graphics, battery, Wi-Fi) (new) — *Everything so far ran on this NVIDIA desktop.*
- A test pass per edition (new)
- Our Sway's login fallback on a fresh install (hypeForge) — *Proven in the VM; not from the disc.*
- Good behaviour inside a VM (guest tools, screen size) (new) — *Many people try a new distro in a VM first.*
- Screen sharing in Chrome and Discord out of the box (new) — *Worked here after installing the portal by hand.*

## 1.x — during the first year (67)

### The disc and the installer

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

- COSMIC style ships in 1.0 (hypeForge D-77) — *Your score: 0/100.*
- Mac OS 9 style ships in 1.0 (hypeForge D-72) — *Your call: held for the year.*
- macOS style ships in 1.0 (hypeForge D-74) — *Your call: held for the year.*
- COSMIC's launcher: full page, like GNOME's (hypeForge D-116) — *Goes with the COSMIC style.*
- All 25 colour themes reviewed on each style that ships (hypeForge Phase 12) — *Light and dark, readable everywhere.*
- The menu card for the Mac styles' Window, Special and Help (hypeForge D-116) — *Goes with the Mac styles.*
- The app name's odd 'gimp' box on the Mac bars (hypeForge review) — *Goes with the Mac styles.*
- The lock screen's box follows the corners switch (hypeForge D-81)
- Separate corners for the bar and for windows (themeForge) — *An idea from 10-10.*
- themeForge: a Corners page (themeForge Phase 2)
- themeForge: Pop-ups, Icons and Fonts pages (themeForge Phase 2)
- themeForge: the quick-switch tray icon (themeForge D-78)
- themeForge: drop old wallpaper copies right away (themeForge) — *Today they wait for the 40-picture cap.*

### Pop-ups

- Pop-ups open right under what you clicked (hypeForge D-116) — *Our Sway's patch 3 makes it possible; plain Sway keeps today's spots.* **Javier:** this has been a MAC OSes issue. We will work later.
- A setting for where each pop-up opens (hypeForge settings catalogue) — *Centre, under the button, a corner.*

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

### The other Forge apps

- grubForge: other distros (#24, #25, #34, #35) (grubForge issues) — *Debian, Ubuntu, Fedora, openSUSE.*
- grubForge: screenshots still show old labels (grubForge TODO)
- alacrittyForge: edit the hints, mouse shortcuts (alacrittyforge #16 #17)
- alacrittyForge: onto the newer forgekit pieces (alacrittyForge TODO)
- bitlaForge: bug fixes (Esc in a field, the console key) (bitlaforge #3)
- bitlaForge: new features (charts, saved setups, restart the miner…) (bitlaforge #9 #10 #11)
- The 'where it runs' AUR descriptions, app by app (app TODOs) — *At each app's next release.*
- cloneForge: moving a system to a new drive (KognogOS README)

### Leaving KDE

- List every KDE piece still in use on the Sway desktop (new) — *The wallet, the network applet, breeze… measured, not guessed.*
- Remove KDE from this desktop (Phase 15) (hypeForge Phase 15 · forge-suite #10) — *The very last step, once everything is proven.*

### Testing before release

- Games on Sway: Steam, Proton, full screen, the pointer (new) — *WoW's pointer bug was found this way.*

### Gaps nobody had written down

- An emoji and special-character picker (new)
- A 'report a problem' button that opens a pre-filled issue (new)

## Still open (8)

### The disc and the installer

- Ship fewer editions in 1.0 (say Basic + Full) and add the rest during the year (new) — *Five editions means five things to test on every disc.* **Javier:** Actually, v1.0 may ship basic, work, full (no developer, no gaming)

### The other Forge apps

- grubForge: over ssh the password policy refuses. Keep it? (grubForge TODO)

### Gaps nobody had written down

- Languages other than English in our apps (new) — *Every Forge app is English only.*
- Typing Chinese, Japanese or Korean (input methods) (new)
- A screen reader (new)
- Snapshots before every update, with a way back (new)
- A backup app for people's own files (new)
- Hibernate (new) — *Sleep yes; hibernate is fragile on NVIDIA.*

## Dropped (5)

### The disc and the installer

- A graphical installer (KognogOS README) — *Already deferred: after installForge proves the flow.*
- Our own package repository (KognogOS README) — *Already deferred: the official repos and the AUR carry everything.*

### The desktop

- World of Warcraft (Wine) matched to its workspace (workspaceForge) — *Its window calls itself wow.exe.* **Javier:** World of Warcraft it is not part of the distro. Azerothcore is a project only for me, my family, and friends.

### The other Forge apps

- mcForge (Midnight Commander settings or fork) (forge-suite ideas)

### Release kit and public face

- The 'Arch' brand variant (KognogOS README) — *Already deferred to a future year.*
