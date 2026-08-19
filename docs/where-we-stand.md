# Where We Stand — Security and the Forge Family

*Javier (jetomev) & Claude · August 2026 · the original of this document lives in the [KognogOS repository](https://github.com/jetomev/KognogOS/blob/main/docs/where-we-stand.md)*

> **The short version** — our packages were never compromised. Every release we
> publish is signed, every commit carries GitHub's Verified badge, and our AUR
> packages check that signature automatically before they build. This page explains
> what happened, what we changed, and how to check all of it yourself instead of
> taking our word for it.

> **Update — 14 August 2026:** the AUR reopened and every package we had waiting is
> live. `nog` **v1.2.0**, `python-forgekit` **v0.3.0** (our first new submission),
> `alacrittyforge` **v0.2.0**, `bitlaforge` **v0.2.1** and `grubforge` **v1.0.3**
> all install normally again, each verifying our signature at build time.

---

## What happened on the AUR

The AUR — the Arch User Repository — is where the Arch community shares build
recipes for software that isn't in the official repositories. Anyone can publish
there, which is exactly what makes it useful and exactly what makes it a target.

Between June and August 2026 it was attacked, repeatedly. The pattern went like
this: find a package whose maintainer had gone quiet, request ownership of it,
get it, then push an update with malware hidden inside. The malicious files were
disguised with innocent names like `validator` and `linter` so they'd look like
part of a normal build. Attackers also published fresh packages with names one
typo away from popular ones, hoping people would install the wrong thing.

More than a hundred packages were affected. Arch escalated in steps: first
removing the bad packages, then **blocking new ownership requests on 30 July**,
and finally **freezing all uploads on 1 August**. That freeze held with no
announced end date until **14 August**, when uploads reopened.

This concerns us because part of the Forge family lives on the AUR:
[nog](https://aur.archlinux.org/packages/nog),
[grubforge](https://aur.archlinux.org/packages/grubforge),
[alacrittyforge](https://aur.archlinux.org/packages/alacrittyforge),
[bitlaforge](https://aur.archlinux.org/packages/bitlaforge), and
[python-forgekit](https://aur.archlinux.org/packages/python-forgekit).

## What we found — 4 August 2026

We checked our own exposure the way we'd want any maintainer to check theirs.

- **None of our packages were touched.** We hold ownership of all of them. There
  was no ownership change, no commit that wasn't ours, and no window where any of
  them sat unmaintained and adoptable.
- **Our development machine came back clean.** We checked every package on it
  against the published lists of compromised ones, and re-verified the packages
  that had updated during the attack window against their stored build recipes.
- **We did find a weakness — in our own tool.** nog is supposed to hold packages
  back for a set number of days. But when it couldn't reach the AUR, it treated
  the silence as "nothing to update" and quietly let those holds lapse. A safety
  feature that switches itself off during an outage isn't a safety feature.

  That's fixed. nog now fails the other way: if it can't verify something, it
  holds it rather than releasing it. It also gained switches to turn the AUR and
  other third-party repositories off entirely, on demand.

  We found it because this campaign made us look harder at our own assumptions —
  the honest way to benefit from somebody else's bad week.

## What we changed

**Everything is signed now.**

A signature is a cryptographic seal. We create it with a private key only we hold,
and anyone can check it against our public key. If the file changes by even one
byte after we sign it, the check fails.

- Every release ships the source, a checksum file, and a signature for both.
- Every commit and tag we push is signed — that's the **Verified** badge on GitHub.
- All five AUR packages take their source from the signed release and name our key
  in the recipe. Your machine checks the signature **before it builds anything**.
  If the check fails, the build stops.

**Our signing key** (published on [keys.openpgp.org](https://keys.openpgp.org)):

```
Javier (jetomev) <jetomev@gmail.com>
32E1D2AB 9380BFD6 BFE3BC1E AC2A3407 CC070F9E
ed25519 · created 2026-08-09 · expires 2028-08-08
```

**We watch for impersonators.** A script runs every week and asks the AUR whether
anyone has published a package pretending to be one of ours — the near-miss names
this campaign used, like `nog-bin` or `bitlaforge-git`. If someone tries it, we'll
know within the week and say so publicly.

**Account hygiene.** AUR credentials rotated, fresh SSH keys, and the account's
activity is part of the weekly review.

## Verify us — don't trust us

Three commands. The first fetches our public key, the second downloads a release
and its signature, the third checks one against the other.

```bash
# 1. Import the key
gpg --keyserver keys.openpgp.org --recv-keys 32E1D2AB9380BFD6BFE3BC1EAC2A3407CC070F9E

# 2. Download any release and its signature (nog shown; every repo works the same)
curl -LO https://github.com/jetomev/nog/releases/download/v1.2.0/nog-1.2.0.tar.gz
curl -LO https://github.com/jetomev/nog/releases/download/v1.2.0/nog-1.2.0.tar.gz.asc

# 3. Check it
gpg --verify nog-1.2.0.tar.gz.asc nog-1.2.0.tar.gz
# expect: Good signature from "Javier (jetomev) <jetomev@gmail.com>"
```

If a "Forge" package ever reaches you without that signature, it isn't ours.

## What's current, where

Since 14 August 2026 the AUR and GitHub agree. Every package is at its latest
release, and each verifies our signature during the build.

| Package | AUR | Latest (GitHub) | |
|---|---|---|---|
| nog | v1.2.0 | v1.2.0 | current ✓ — security hardening, plus Flatpak and Snap support |
| python-forgekit | v0.3.0 | v0.3.0 | current ✓ — new package; the shared Forge foundation |
| alacrittyforge | v0.2.0 | v0.2.0 | current ✓ — rebuilt on forgekit |
| bitlaforge | v0.2.1 | v0.2.1 | current ✓ — first Forge app on forgekit |
| grubforge | v1.0.3 | v1.0.3 | current ✓ |

Two packaging changes came out of this and are staying. Every build recipe now
takes its source from the **signed release** rather than an unsigned archive, and
names our key — so the build refuses to start if the signature doesn't match. And
each AUR repository holds nothing but the packaging files. You can read every one
of them end to end in under a minute, which is the entire point.

## Where we stand

The AUR is open by design. That openness is why it's valuable, and why it was
attacked. We don't control the repository — but we do control whether trusting our
corner of it requires faith.

As of August 2026, it doesn't. There are signatures you can check, badges GitHub
checks for you, verification your own machine performs automatically before it
builds, and a public record of what we did and when
(see [Operation Ironhold](operation-ironhold.md)).

That's where we stand.

---

*Questions, or something that doesn't verify? Open an issue on any of our
repositories — that's exactly what they're for.*
