# Where We Stand — Security and the Forge Family

*Javier (jetomev) & Claude · August 2026 · the canonical copy of this document lives in the [KognogOS repository](https://github.com/jetomev/KognogOS/blob/main/docs/where-we-stand.md)*

> **Update — 14 August 2026: the AUR is open again, and every staged package is live.**
> `nog` **v1.2.0**, `python-forgekit` **v0.3.0** (our first new AUR submission),
> `alacrittyforge` **v0.2.0**, `bitlaforge` **v0.2.1** and `grubforge` **v1.0.3** all
> install from the AUR now, each verifying our release signature at build time.
> Nothing is held back behind the freeze any more, and the table below is current.

> **TL;DR** — Our packages were never compromised. Every release is GPG-signed,
> every commit carries a Verified badge, and our AUR packages verify signatures at
> build time. This page tells you exactly what's current, how to verify everything
> yourself, and what we changed so you never have to take our word for it.

---

## What happened on the AUR

Through June–August 2026, the Arch User Repository was hit by a sustained
supply-chain campaign: attackers filed orphan requests against unmaintained
packages, adopted them, and pushed malicious updates — obfuscated ELF binaries
(`validator`, `linter`, `hasher`) smuggled into build paths, plus fresh `-bin`
typosquats of popular names, backed by a Tor-based second stage. Over a hundred
packages were affected across the waves. Arch's response escalated from removals
to **disabling package adoption (July 30)** and finally **freezing all AUR pushes
(August 1)** — a freeze that held with no announced end date until **August 14**,
when pushes reopened.

This matters to us because the Forge family lives partly on the AUR:
[nog](https://aur.archlinux.org/packages/nog),
[grubforge](https://aur.archlinux.org/packages/grubforge),
[alacrittyforge](https://aur.archlinux.org/packages/alacrittyforge),
[bitlaforge](https://aur.archlinux.org/packages/bitlaforge), and
[python-forgekit](https://aur.archlinux.org/packages/python-forgekit).

## Our audit — August 4, 2026

We reviewed our own exposure the way we'd want any maintainer to:

- **None of our packages were compromised.** We hold their AUR maintainership;
  no adoption, no foreign commits, no orphan window.
- **Our development machine came back clean**: every foreign and third-party-repo
  package on it was checked against the published compromise lists, and the
  packages updated during the attack window were verified against their cached
  build recipes.
- The audit *did* surface a hardening gap in our own tooling — nog, our
  tier-aware update manager, treated an unreachable AUR as "nothing to do,"
  which could silently release version holds during an outage. **That
  fail-open bug is fixed** (nog v1.0.9 fails closed and gained explicit
  kill-switches for AUR and third-party repos). We found it because this
  campaign made us look harder at our own assumptions — the honest way to
  benefit from someone else's bad week.

## What we changed

**Everything is signed now.**

- Releases on every Forge repository ship a source tarball, a SHA256 manifest,
  and detached GPG signatures (`.asc`) for both.
- Every commit and tag from us is GPG-signed — look for the **Verified** badge
  on GitHub.
- All five of our AUR packages pull the **signed release tarball** and carry
  `validpgpkeys`, so `makepkg` cryptographically verifies the source against our
  key before a single line builds. This is live — it shipped with the packages on
  14 August.

**Our signing key** (published on [keys.openpgp.org](https://keys.openpgp.org)):

```
Javier (jetomev) <jetomev@gmail.com>
32E1D2AB 9380BFD6 BFE3BC1E AC2A3407 CC070F9E
ed25519 · created 2026-08-09 · expires 2028-08-08
```

**We watch for impersonators.** A weekly sentry queries the AUR for exact
lookalikes of our package names (`nog-bin`, `bitlaforge-git`, and friends — the
suffix pattern this campaign used) and for new packages shadowing our names.
If someone tries to typosquat the Forge family, we'll know within the week and
say so publicly.

**Account hygiene**: AUR credentials rotated, fresh SSH keys, and our AUR
account activity is part of the weekly review.

## Verify us — don't trust us

```bash
# 1. Import the key
gpg --keyserver keys.openpgp.org --recv-keys 32E1D2AB9380BFD6BFE3BC1EAC2A3407CC070F9E

# 2. Grab any release + its signature (nog shown; same shape everywhere)
curl -LO https://github.com/jetomev/nog/releases/download/v1.2.0/nog-1.2.0.tar.gz
curl -LO https://github.com/jetomev/nog/releases/download/v1.2.0/nog-1.2.0.tar.gz.asc

# 3. Verify
gpg --verify nog-1.2.0.tar.gz.asc nog-1.2.0.tar.gz
# expect: Good signature from "Javier (jetomev) <jetomev@gmail.com>"
```

If a "Forge" package ever reaches you without that signature chain, it isn't ours.

## What's current where

Since 14 August 2026 the AUR and GitHub agree — every package is at its
latest release, and each one verifies our signature during the build:

| Package | AUR | Latest (GitHub) | Notes |
|---|---|---|---|
| nog | v1.2.0 | v1.2.0 | current ✓ — Ironhold hardening, plus Flatpak and Snap as first-class sources |
| python-forgekit | v0.3.0 | v0.3.0 | current ✓ — new package; the shared Forge TUI shell |
| alacrittyforge | v0.2.0 | v0.2.0 | current ✓ — rebuilt on forgekit |
| bitlaforge | v0.2.1 | v0.2.1 | current ✓ — first Forge app on forgekit |
| grubforge | v1.0.3 | v1.0.3 | current ✓ |

Two things changed in how these are packaged while the freeze was on, and
both survive it. Every PKGBUILD now takes its source from the **signed
release asset** rather than an unauthenticated archive tarball, and names
our key in `validpgpkeys` — so `makepkg` refuses to build if the tarball
does not carry our signature. And each AUR repository holds packaging
files only: `PKGBUILD`, `.SRCINFO` and nothing else. You can read every
one of them end to end in under a minute, which is the point.

## The stance, in one paragraph

The AUR's openness is why it's valuable and why it was attacked. We don't get
to control the repository — we *do* get to control whether trusting our little
corner of it requires faith. As of August 2026 it doesn't: signatures you can
check, badges GitHub checks for you, build-time verification `makepkg` performs
automatically, and a public paper trail (see
[Operation Ironhold](operation-ironhold.md)) of what we did and when. That's
where we stand.

---

*Questions or something that doesn't verify? Open an issue on any of our
repositories — that's exactly what they're for.*
