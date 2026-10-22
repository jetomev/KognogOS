# The atomized pending list for the KognogOS 1.0 cut (2026-10-21). Writes items.json for the board.
# Fields: area, title, detail, source, suggest ("1.0" | "1.x" | "drop" | "?"), new (not discussed before).
import json

A = []
def item(area, title, detail, source, suggest, new=False):
    A.append({"area": area, "title": title, "detail": detail, "source": source, "suggest": suggest, "new": new})

# ---- The disc and the installer
d = "disc"
item(d, "Rebuild the disc around Sway + hypeForge", "The ISO still stages the Plasma desktop. The 1.0 disc is Sway only.", "KognogOS #13", "1.0")
item(d, "build-iso.sh: stop staging Plasma, point at forge-suite/hypeforge", "Line 42 still looks for ~/Programs/hypeforge.", "KognogOS TODO", "1.0")
item(d, "The disc's package list = what hypeForge and the Forge apps need", "Measured in each app's docs/PACKAGING.md (the dependency audit).", "forge-suite #91", "1.0")
item(d, "Prove every font hypeForge needs is on the disc", "docs/FONTS.md lists them; the Nerd Font symbols were added 10-05, never proven by a build.", "KognogOS TODO", "1.0")
item(d, "Remove the repeated nano and tmux lines", "Harmless, but sloppy.", "KognogOS TODO", "1.0")
item(d, "sudoForge on the disc, set up at first boot", "Without it there is no admin password window on Sway.", "KognogOS TODO", "1.0")
item(d, "Brightness keys: brightnessctl on the disc, or bind them to displayForge", "A laptop's brightness keys do nothing today.", "forge-suite #94", "1.0")
item(d, "The login's pam_kwallet_init is missing on the disc", "Either kwallet-pam ships, or walletForge replaces it.", "forge-suite #95", "1.0")
item(d, "Boot identity required in the installed system, not just the live disc", "Installer recipe.", "KognogOS #2", "1.0")
item(d, "Fresh install lacks fakeroot and nog's signing key", "Found by nog's VM test.", "KognogOS #9", "1.0")
item(d, "AUR builds work on an installed system (base-devel)", "Fixed on main; close after the next disc build proves it.", "KognogOS #11", "1.0")
item(d, "The os-release hook errors inside every clean chroot", "Seen when building packages on a KognogOS box.", "KognogOS #16", "1.0")
item(d, "Basic edition: the app list redone without KDE apps", "Today's lists date from the Plasma build.", "KognogOS README", "1.0")
item(d, "Office edition: the app list redone", "OnlyOffice, Obsidian, Thunderbird… minus the KDE pieces.", "KognogOS README", "1.0")
item(d, "Gaming edition: the app list redone", "Steam, Lutris, Heroic, Proton-GE, RetroArch… checked on Sway.", "KognogOS README", "1.0")
item(d, "Development edition: the app list redone", "VS Code, Neovim, toolchains, Docker…", "KognogOS README", "1.0")
item(d, "Full edition: everything above", "Follows from the four lists.", "KognogOS README", "1.0")
item(d, "Ship fewer editions in 1.0 (say Basic + Full) and add the rest during the year", "Five editions means five things to test on every disc.", "new", "?", True)
item(d, "Chrome, Claude Desktop and Claude Terminal pre-selected; Brave no longer the default", "Your decision of 10-07.", "KognogOS #14", "1.0")
item(d, "Proprietary apps marked in the installer, with a free swap", "Defined in config/profiles.toml.", "KognogOS README", "1.0")
item(d, "Pick and theme the login screen for Sway", "The roadmap says it's part of the hypeForge disc; nothing is chosen yet.", "KognogOS roadmap", "1.0")
item(d, "installForge: the terminal installer as a Forge Suite section", "Today it's a first-draft shell script.", "KognogOS Phase 3", "1.0")
item(d, "installForge: the edition picker", "Reads config/profiles.toml.", "KognogOS Phase 3", "1.0")
item(d, "installForge: guided disk setup (whole disk, or free space next to Windows)", "Dual boot is the common case.", "KognogOS Phase 3", "1.0")
item(d, "installForge: disk encryption on by default, with a way to skip it", "Learned from Omarchy's installer.", "KognogOS Phase 3", "?")
item(d, "installForge: user creation", "Name, password, the admin rights.", "KognogOS Phase 3", "1.0")
item(d, "installForge: keyboard layout, language and time zone steps", "Not written down anywhere yet.", "new", "1.0", True)
item(d, "installForge: pick the graphics driver (NVIDIA, AMD, Intel) by itself", "Sway on NVIDIA needs its own flags; the installer must know.", "new", "1.0", True)
item(d, "installForge: Wi-Fi setup inside the installer", "The install is online-only, so a laptop needs Wi-Fi before anything else.", "new", "1.0", True)
item(d, "installForge: 'prepare for a new owner' mode", "The personal questions wait for the new owner's first boot.", "KognogOS Phase 3", "1.x")
item(d, "installForge: bootable snapshots from the boot menu", "btrfs snapshots you can boot into after a bad update.", "KognogOS Phase 3", "1.x")
item(d, "installForge: the Development edition suggests reviewing tier pins", "For people whose toolchain needs newer packages.", "KognogOS Phase 3", "1.x")
item(d, "The live disc starts Sway on any graphics card (VM, NVIDIA, AMD, Intel)", "Today it's only proven on this desktop.", "new", "1.0", True)
item(d, "System Lock: only nog may drive package changes (managed mode)", "", "KognogOS #10", "1.x")
item(d, "This desktop runs nog's stock tier list, not KognogOS's. On purpose?", "Open question since 09-28.", "hypeForge open question", "?")
item(d, "A graphical installer", "Already deferred: after installForge proves the flow.", "KognogOS README", "drop")
item(d, "Our own package repository", "Already deferred: the official repos and the AUR carry everything.", "KognogOS README", "drop")
item(d, "The KognogOS project kit: CLAUDE.md for how it's built, tested, shipped", "The only project still missing it.", "KognogOS TODO", "1.0")

# ---- First boot and welcome
d = "boot"
item(d, "welcomeForge: the Welcome Center", "Opens at session start. On the live disc it leads with Install; once installed, a 'show at startup' switch.", "KognogOS roadmap", "1.0")
item(d, "welcomeForge: a guided nog tour", "", "KognogOS roadmap", "1.0")
item(d, "welcomeForge: where to give feedback", "Points to GitHub Issues.", "KognogOS roadmap", "1.0")
item(d, "The tier guide: a plain-language manual of what each tier means", "How to read and edit tier-pins.toml, with examples.", "KognogOS roadmap", "1.0")
item(d, "A shell prompt that looks right on a plain text console", "It looks awful on a tty today.", "KognogOS #12", "1.0")
item(d, "promptForge: switch prompt themes without editing fish files", "", "KognogOS #5", "1.x")
item(d, "The KognogOS greeting as its own packaged app", "", "KognogOS #4", "1.x")
item(d, "greetForge: a text-console version of the greeting", "", "KognogOS #8", "1.x")

# ---- The desktop (hypeForge core)
d = "desk"
item(d, "The bar guard: the bar comes back by itself if it ever disappears", "D-115. The 10-17 silent exit is still unexplained.", "hypeForge Phase 12", "1.0")
item(d, "Any number of screens, from one to six", "Today's settings assume this desk's three. The roadmap calls it 'the ISO gate'.", "hypeForge track 12b", "1.0")
item(d, "Laptops: battery on the bar, closing the lid, sleep", "Not written down anywhere yet. This desk has no battery.", "new", "1.0", True)
item(d, "Screens at high resolution: a sensible size on first boot", "A 4K laptop at 100 % is unreadable.", "new", "1.0", True)
item(d, "Night light hides its own tray icon where the bar already shows the moon", "nightForge 1.1.", "forge-suite #82", "1.0")
item(d, "Help & Keys pages current for 1.0", "Every guide page checked against what ships.", "new", "1.0", True)
item(d, "A tray restart that keeps Electron apps' icons", "Today: never restart the tray live; changes wait for the next login.", "hypeForge Phase 12", "1.x")
item(d, "Folder-style tabs", "Small tabs like folders in a holder, replacing Sway's even tab row.", "hypeForge Phase 12", "1.x")
item(d, "Drag and drop windows onto each other to tab or stack them", "", "hypeForge track 25", "1.x")
item(d, "Apps that draw their own title bar (Chrome…): switch it off where the app allows", "You moved it last in Phase 12.", "hypeForge Phase 12", "1.x")
item(d, "More than nine workspaces", "The cell numbering has to change first.", "workspaceForge D-6", "1.x")
item(d, "Workspace sharing, rethought", "Waiting on your thinking.", "workspaceForge D-7", "1.x")
item(d, "World of Warcraft (Wine) matched to its workspace", "Its window calls itself wow.exe.", "workspaceForge", "1.x")
item(d, "The frost: see-through, blurred bars on the FX login", "", "forge-suite #83", "1.x")
item(d, "The notch on big windows' rounded corners (SwayFX)", "Reported upstream as swayfx#600.", "forge-suite #64", "1.x")
item(d, "Screen recording", "Screenshots are done; video isn't.", "new", "1.x", True)

# ---- Styles and colour themes
d = "look"
item(d, "The Rice ships in 1.0 (KognogOS's default look)", "", "hypeForge D-78", "1.0")
item(d, "Windows 11 style ships in 1.0", "Your daily driver right now.", "hypeForge D-71", "1.0")
item(d, "KDE style ships in 1.0", "", "hypeForge D-76", "?")
item(d, "Classic style ships in 1.0", "The plain first look.", "hypeForge", "?")
item(d, "COSMIC style ships in 1.0", "Your score: 0/100.", "hypeForge D-77", "1.x")
item(d, "Mac OS 9 style ships in 1.0", "Your call: held for the year.", "hypeForge D-72", "1.x")
item(d, "macOS style ships in 1.0", "Your call: held for the year.", "hypeForge D-74", "1.x")
item(d, "COSMIC's launcher: full page, like GNOME's", "Goes with the COSMIC style.", "hypeForge D-116", "1.x")
item(d, "Full review of each style that ships: bar, launcher, tray, every pop-up", "Step by step, your look on each piece.", "hypeForge Phase 12", "1.0")
item(d, "All 25 colour themes reviewed on each style that ships", "Light and dark, readable everywhere.", "hypeForge Phase 12", "?")
item(d, "Ship fewer colour themes in 1.0 and add the rest during the year", "25 × every style is a lot to prove.", "new", "?", True)
item(d, "The menu card for the Mac styles' Window, Special and Help", "Goes with the Mac styles.", "hypeForge D-116", "1.x")
item(d, "The app name's odd 'gimp' box on the Mac bars", "Goes with the Mac styles.", "hypeForge review", "1.x")
item(d, "The lock screen's box follows the corners switch", "", "hypeForge D-81", "1.x")
item(d, "Separate corners for the bar and for windows", "An idea from 10-10.", "themeForge", "1.x")
item(d, "themeForge 1.0 released (GitHub + AUR)", "The Look settings app.", "themeForge Phase 3", "1.0")
item(d, "themeForge: a Corners page", "", "themeForge Phase 2", "1.x")
item(d, "themeForge: Pop-ups, Icons and Fonts pages", "", "themeForge Phase 2", "1.x")
item(d, "themeForge: the quick-switch tray icon", "", "themeForge D-78", "1.x")
item(d, "themeForge: drop old wallpaper copies right away", "Today they wait for the 40-picture cap.", "themeForge", "1.x")

# ---- Pop-ups
d = "pop"
item(d, "Pop-ups open right under what you clicked", "Our Sway's patch 3 makes it possible; plain Sway keeps today's spots.", "hypeForge D-116", "1.0")
item(d, "The hover tip stops covering an open pop-up", "", "hypeForge D-116", "1.0")
item(d, "One title row on every pop-up", "Quick Settings has none today.", "hypeForge D-116", "1.0")
item(d, "Three widths only: narrow, medium, wide", "", "hypeForge D-116", "1.0")
item(d, "The notification cards on the pop-up standard", "", "hypeForge D-116", "1.0")
item(d, "A setting for where each pop-up opens", "Centre, under the button, a corner.", "hypeForge settings catalogue", "1.x")

# ---- Settings apps
d = "set"
item(d, "Sound app (outputs, inputs, each app's volume)", "Today: wiremix, themed.", "hypeForge track 7", "1.0")
item(d, "Network & Wi-Fi app", "Today: the network menu + nmtui.", "hypeForge track 8", "1.0")
item(d, "Bluetooth app", "Today: bluetui.", "hypeForge track 9", "1.0")
item(d, "Default apps: defaultappsForge 1.0 after your run", "Built 10-09, waiting on your run.", "defaultappsForge", "1.0")
item(d, "Power & Lock (idle, sleep, lock screen)", "", "hypeForge track 13", "1.0")
item(d, "Keyboard (layout, repeat, the key chart)", "", "hypeForge track 16", "1.0")
item(d, "Mouse & Touchpad", "Touchpad matters on laptops.", "hypeForge track 17", "1.0")
item(d, "Time & Language", "", "hypeForge track 18", "1.0")
item(d, "About this computer", "The greeting window does it today.", "hypeForge track 22", "1.0")
item(d, "Notifications app (mako's settings)", "", "hypeForge track 14", "1.x")
item(d, "Startup apps", "Applet 10 does it from a folder today.", "hypeForge track 15", "1.x")
item(d, "printerForge (the Printers app)", "Printing already works driverless.", "hypeForge track 19", "1.x")
item(d, "USB drives & disks app", "The Disks pop-up does mount and eject today.", "hypeForge track 20", "1.x")
item(d, "Users", "", "hypeForge track 21", "1.x")
item(d, "Windows app: placement, float rules, tiling", "", "hypeForge track 12b", "1.x")
item(d, "Launcher settings: sections, favourites, its look", "", "hypeForge Settings", "1.x")
item(d, "Lock screen look settings", "", "hypeForge Settings", "1.x")
item(d, "A Calculator in our look", "galculator meanwhile.", "hypeForge roadmap", "1.x")
item(d, "fileForge: our own file manager", "Thunar meanwhile.", "hypeForge Phase 13", "1.x")
item(d, "Game controllers + the G13 app", "", "hypeForge after 1.0", "1.x")
item(d, "Accessibility (large text and pointer)", "", "hypeForge after 1.0", "1.x")
item(d, "Online accounts", "", "hypeForge after 1.0", "1.x")
item(d, "Remote desktop", "", "hypeForge after 1.0", "1.x")
item(d, "Touchscreen", "", "hypeForge after 1.0", "1.x")
item(d, "App permissions", "", "hypeForge after 1.0", "1.x")
item(d, "Spell check", "", "hypeForge after 1.0", "1.x")
item(d, "Animations", "", "hypeForge after 1.0", "1.x")
item(d, "displayForge: tested with one and two screens", "", "displayForge 1.1.x", "1.0")
item(d, "displayForge: 80 / 90 % sizes on real apps", "X11 apps blur at non-whole sizes.", "displayForge 1.1.x", "1.0")
item(d, "displayForge: tested on a plain text console", "", "displayForge 1.1.x", "1.0")
item(d, "displayForge: the 'not tried yet' text during the countdown", "A small bug seen in screenshots.", "displayForge 1.1.x", "1.0")
item(d, "displayForge: profiles that switch when screens plug in or out", "", "displayForge later", "1.x")
item(d, "workspaceForge: tested with one or two screens, and on a text console", "", "workspaceForge Phase 2", "1.0")
item(d, "Our own text-mode versions of the other apps we use", "Phase 14: fork or write from zero.", "hypeForge Phase 14", "drop")

# ---- Passwords and security
d = "sec"
item(d, "walletForge: research what the saved-logins standard needs", "Must land before KDE leaves.", "walletForge Phase 0", "1.0")
item(d, "walletForge: the store and its encryption", "", "walletForge Phase 0", "1.0")
item(d, "walletForge: copy the entries over from KDE's wallet", "", "walletForge Phase 0", "1.0")
item(d, "walletForge: the service, unlocked at login", "Chrome, Claude Desktop and Discord keep their logins.", "walletForge Phase 1", "1.0")
item(d, "walletForge: the Passwords page in Settings", "Like Chrome's password manager.", "walletForge Phase 0", "1.x")
item(d, "sudoForge: a compact password box", "'To much real state waste.'", "forge-suite #62", "1.0")
item(d, "sudoForge: our own GPG passphrase prompt", "Drops a GNOME piece.", "sudoForge later", "1.x")
item(d, "sudoForge: fold the session agent back into forgekit", "", "sudoForge later", "1.x")
item(d, "Firewall on by default, checked on the installed system", "The README promises it.", "new", "1.0", True)
item(d, "An update reminder people actually see", "Quick Settings shows a count; nothing pings.", "new", "?", True)
item(d, "Secure Boot", "Many laptops ship with it on.", "new", "1.x", True)

# ---- Packages
d = "pkg"
item(d, "nog update --yes (unattended updates)", "The installer and welcome need it.", "nog #56", "1.0")
item(d, "nog remove warns before taking an optional dependency; nog keep", "Elisa almost took VLC's formats with it.", "nog F-13 #49", "1.0")
item(d, "nog: confirm the missing 'continue?' prompt of 1 Oct is gone", "", "nog TODO", "1.0")
item(d, "nog: watch the first real update that installs something", "Matrix 7.3 / 7.4, never seen on real data.", "nog 2.0 matrix", "1.0")
item(d, "nog install --yes for repository packages through the AUR helper", "", "nog #32", "1.x")
item(d, "nog: the AUR helper's questions racing its table", "", "nog TODO", "1.x")
item(d, "nog: the 'last update' record per user or per system", "", "nog TODO", "1.x")
item(d, "nog: the rare library mismatch (priority 4)", "", "nog #5", "1.x")
item(d, "nog: small follow-ups (search shows 30, info on Flatpak, reinstall, lock by version)", "", "nog 2.0 notes", "1.x")
item(d, "nog: the AUR description wording", "At the next package bump.", "nog TODO", "1.x")
item(d, "nogForge on the disc", "It isn't in the package list yet.", "nogForge TODO", "1.0")
item(d, "nogForge: unticking with the mouse jumps the list to the top", "", "nogForge #17", "1.0")
item(d, "nogForge: Tick all / Untick all", "", "nogForge #18", "1.0")
item(d, "nogForge: update one package by itself", "'Too hard to get one package updated.'", "nogForge #20", "1.0")
item(d, "nogForge: Update and Uninstall buttons on each installed app", "", "nogForge #19", "1.0")
item(d, "nogForge: Downgrade button", "Needs a design pass and nog's say.", "nogForge #19", "1.x")
item(d, "nogForge: the Settings page (holds, sources, repositories)", "Security-sensitive.", "nogForge TODO", "1.x")
item(d, "nogForge: nog's run inside the window, redesigned", "'It is not beautiful, it is disrupting.'", "nogForge TODO", "1.x")
item(d, "Which AUR helper the disc ships (yay or paru)", "Not decided anywhere.", "new", "1.0", True)
item(d, "Flatpak and Flathub ready out of the box", "nog manages Flatpak since 2.0.", "new", "?", True)
item(d, "nogForge: the old commit with the book persona's name", "History rewrite: your call.", "nogForge TODO", "?")

# ---- The other Forge apps
d = "apps"
item(d, "Desktop entries in every Forge app's package", "So they show in any launcher.", "grubforge #37 · alacrittyforge #18 · bitlaforge #12 · nogforge #16", "1.0")
item(d, "Is bitlaForge on the disc at all?", "A mining app is an odd default.", "new", "?", True)
item(d, "grubForge: fixes that touch Arch (#17, #19, #20, #22)", "Frozen entries, duplicates, --version.", "grubForge issues", "1.x")
item(d, "grubForge: other distros (#24, #25, #34, #35)", "Debian, Ubuntu, Fedora, openSUSE.", "grubForge issues", "1.x")
item(d, "grubForge: screenshots still show old labels", "", "grubForge TODO", "1.x")
item(d, "grubForge: over ssh the password policy refuses. Keep it?", "", "grubForge TODO", "?")
item(d, "alacrittyForge: edit the hints, mouse shortcuts", "", "alacrittyforge #16 #17", "1.x")
item(d, "alacrittyForge: onto the newer forgekit pieces", "", "alacrittyForge TODO", "1.x")
item(d, "bitlaForge: bug fixes (Esc in a field, the console key)", "", "bitlaforge #3", "1.x")
item(d, "bitlaForge: new features (charts, saved setups, restart the miner…)", "", "bitlaforge #9 #10 #11", "1.x")
item(d, "Your pending test runs: grubForge 2.2, alacrittyForge 1.1, bitlaForge 1.1, nogForge 1.4", "Matrices written, not run.", "app TODOs", "?")
item(d, "Move alacrittyForge, bitlaForge, nogForge, grubForge into forge-suite", "", "forge-suite D-60", "1.x")
item(d, "Write the per-app release recipe down", "Proven, not documented.", "forge-suite TODO", "1.0")
item(d, "The 'where it runs' AUR descriptions, app by app", "At each app's next release.", "app TODOs", "1.x")
item(d, "cloneForge: moving a system to a new drive", "", "KognogOS README", "1.x")
item(d, "mcForge (Midnight Commander settings or fork)", "", "forge-suite ideas", "drop")

# ---- Our Sway build
d = "sway"
item(d, "Our Sway build as a KognogOS package", "Today it's built in your home folder; the disc needs a package.", "hypeForge D-111", "1.0")
item(d, "Hold Sway updates until our patches fit the new version", "So an Arch update never ships a desktop without its buttons.", "new", "1.0", True)
item(d, "Offer our patches to Sway upstream", "The title bar buttons and the pointer position.", "new", "1.x", True)

# ---- Leaving KDE
d = "kde"
item(d, "List every KDE piece still in use on the Sway desktop", "The wallet, the network applet, breeze… measured, not guessed.", "new", "1.0", True)
item(d, "Remove KDE from this desktop (Phase 15)", "The very last step, once everything is proven.", "hypeForge Phase 15 · forge-suite #10", "1.0")

# ---- Release kit and public face
d = "rel"
item(d, "Where the ISO is downloaded from (hosting)", "", "KognogOS Phase 5", "1.0")
item(d, "Checksums and a signature for the ISO", "", "KognogOS Phase 5", "1.0")
item(d, "kognogos.org: a download page and the release notes", "", "KognogOS Phase 5", "1.0")
item(d, "Check what kognogos.org shows people who aren't signed in", "The portal guards our sites; the public page must stay public.", "new", "1.0", True)
item(d, "Screenshots and a banner of 1.0 for the site and the README", "", "new", "1.0", True)
item(d, "A getting-started guide on the site", "Install, first boot, nog, where help lives.", "new", "1.0", True)
item(d, "A privacy line: what KognogOS does and doesn't send anywhere", "", "new", "1.0", True)
item(d, "Issue templates on GitHub for feedback", "GitHub Issues is the one door.", "new", "1.0", True)
item(d, "A licence check of everything the disc installs", "Proprietary apps marked; nothing redistributed that can't be.", "new", "1.0", True)
item(d, "Is 'KognogOS' free to use as a name?", "A trademark search before the public launch.", "new", "?", True)
item(d, "A place for people to talk (Discord, Matrix, forum)", "Or GitHub only.", "new", "?", True)
item(d, "The KognogOS 1.0 GitHub Release", "", "KognogOS Phase 6", "1.0")
item(d, "Announcements", "Where, and in what words.", "KognogOS Phase 6", "1.0")
item(d, "DistroWatch submission", "Their queue takes months.", "KognogOS Phase 6", "1.0")
item(d, "Push the 9 waiting commits, issues F-79 to F-81, the Vault entry", "With the next phase.", "forge-suite TODO", "1.0")
item(d, "The 'Arch' brand variant", "Already deferred to a future year.", "KognogOS README", "drop")

# ---- Testing before release
d = "test"
item(d, "Install the disc in a VM until a run has zero problems", "", "KognogOS Phase 4", "1.0")
item(d, "Wipe a real machine and install from the disc alone, until zero problems", "", "KognogOS Phase 4", "1.0")
item(d, "Test on a laptop (Intel or AMD graphics, battery, Wi-Fi)", "Everything so far ran on this NVIDIA desktop.", "new", "1.0", True)
item(d, "A test pass per edition", "", "new", "1.0", True)
item(d, "Our Sway's login fallback on a fresh install", "Proven in the VM; not from the disc.", "hypeForge", "1.0")
item(d, "Good behaviour inside a VM (guest tools, screen size)", "Many people try a new distro in a VM first.", "new", "1.0", True)
item(d, "Screen sharing in Chrome and Discord out of the box", "Worked here after installing the portal by hand.", "new", "1.0", True)
item(d, "Games on Sway: Steam, Proton, full screen, the pointer", "WoW's pointer bug was found this way.", "new", "1.0", True)

# ---- Gaps nobody has written down
d = "gaps"
item(d, "Languages other than English in our apps", "Every Forge app is English only.", "new", "1.x", True)
item(d, "Typing Chinese, Japanese or Korean (input methods)", "", "new", "1.x", True)
item(d, "A screen reader", "", "new", "1.x", True)
item(d, "Snapshots before every update, with a way back", "", "new", "?", True)
item(d, "A backup app for people's own files", "", "new", "1.x", True)
item(d, "An emoji and special-character picker", "", "new", "1.x", True)
item(d, "A 'report a problem' button that opens a pre-filled issue", "", "new", "1.x", True)
item(d, "Hibernate", "Sleep yes; hibernate is fragile on NVIDIA.", "new", "drop", True)

for i, x in enumerate(A, 1):
    x["order"] = i
    x["id"] = f"{x['area']}-{i:03d}"
json.dump(A, open(__file__.replace("items.py", "items.json"), "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(A), Counter(x["area"] for x in A), Counter(x["suggest"] for x in A), sum(x["new"] for x in A), "new")
