# Operation Ironhold — AUR-attack response sprint

**Opened:** 2026-08-04 · **Hard deadline:** 2026-08-19 (night) — Orlando travel Aug 20, 4 days away
**Budget:** 1–2 h/night, 5 nights/week ≈ 11–13 sessions ≈ 16–20 h
**Scope:** everything pending across **nog, the Forge Suite, and KognogOS** in response to the July–August 2026 AUR supply-chain attacks. Goal state: **zero open risk/security/safety items** on our side before travel.

**Context (2026-08-04 review):** multi-wave AUR campaign — spam orphan requests → malicious
adoptions of orphans (~50 KB ELF payloads: `validator`, `linter`, `hasher`…) → new `-bin`
typosquat packages with sudo-time malware. Arch response: package adoption disabled 07-30,
**all AUR pushes disabled ~08-02, no ETA**. Our desktop audit: **clean** (all 19 AUR + 18
chaotic-aur packages off every published infected list; the three attack-window updates
verified via cached PKGBUILD git histories). The audit also surfaced a nog bug: **AUR holds
fail open when AUR metadata is unreachable** — the trigger for this sprint.

---

## 1 · Gap analysis — every Weakness/Threat mapped

| # | SWOT item | Solution | Workstream | Status |
|---|-----------|----------|------------|--------|
| W1 | AUR holds fail open when AUR is unreachable | Fail-closed holds fix | A1 | planned (v1.0.9) |
| W2 | No GPG signing (AUR commits, release artifacts) | Sign commits everywhere; signed artifacts + `validpgpkeys` in PKGBUILDs | B1–B2 | planned |
| W3 | Single AUR account = SPOF for 4 packages | Credential hygiene now; co-maintainer **deferred → accepted risk** (no candidate; revisit at Forge v2) | B3 / decision | planned + decided |
| W4 | No typosquat monitoring (`nog-bin`, `*forge-bin`…) | Weekly AUR-RPC watch script | B4 | planned |
| W5 | chaotic-aur auto-builds AUR PKGBUILDs into binaries, no local review | Kill switch (A2–A3) + trust-chain documented in the article; tier-pin audit cadence noted | A2–A3, C1 | planned |
| T1 | AUR freeze, no ETA — can't ship | "Ready-to-ship" doctrine: everything tagged/staged, AUR push = 15-min action when it reopens | A5, B2 | planned |
| T2 | Attacker pivot to maintainer credentials | = W2 + W3 hardening | B1–B3 | planned |
| T3 | chaotic-aur poisoning window | = W5 (kill switch is the incident response) | A2–A3 | planned |
| T4 | AUR policy aftershocks (new rules, friction) | Monitor aur-general; adapt post-sprint — **no pre-emptive action possible** | watch item | accepted |
| — | Maintainer-change / adoption detector | Genuine roadmap feature, **not in this sprint** — nog v2 candidate | roadmap | deferred |

Everything is either **planned in this sprint**, an **explicit accepted risk**, or a
**named roadmap deferral**. Nothing floats.

---

## 2 · Workstreams and schedule

### N0 — Tonight (Aug 4): open the operation ✅ CLOSED 2026-08-04
- [x] This document committed; sprint scoped
- [x] Desktop loose end: ufw port-8000 LAN rule deleted
- [x] AUR account hygiene: password rotated, dedicated `~/.ssh/aur` key confirmed (in place since 2026-04-04), account email verified
- [x] Bonus detour: spectacle GLIBC_2.44 breakage → **new nog bug-class "tier ABI skew"** (T3 ffmpeg/gcc-libs released built against held T1 glibc); fixed by promoting the glibc family (`nog install glibc lib32-glibc` — the promote-family gap reproduced, 2nd live hit); linchpin-heuristic + user-coupling-groups filed as nog candidates (post-sprint scope)

### Phase A — nog v1.0.9 "Ironhold" security cycle (~5–6 nights, Aug 5–12)
The core. Scope is **locked** to these five items — no riders except the freebie below.
- **A1** ✅ **DONE 2026-08-05** · Fail-closed AUR holds — shipped as the **foreign fence**
  (nog commit `a4a6fb4`, issue [#2](https://github.com/jetomev/nog/issues/2) opened+closed):
  every foreign package is ignored at handoff unless nog cleared it this run. The 08-01
  bypass is a unit test; tests 42→45; field-verified live (176 pending, 4 released,
  172 held, 19 fenced, zero unsanctioned upgrades). Cycle issues #2–#6 filed; AUR-freeze
  footer convention started with #2's closing comment.
- **A2** ✅ **DONE 2026-08-05** · `nog deactivate aur` / `nog activate aur` — shipped
  (nog commit `f1139cc`, issue [#3](https://github.com/jetomev/nog/issues/3) closed):
  state in new nog-owned `/etc/nog/sources.toml` (Javier's design pick over editing
  nog.conf), single gate upstream of helper detection (helper-agnostic), corrupted
  state fails closed. Tests 45→49; round trip field-verified. Bonus: dogfooding spawned
  the **System Lock doctrine feature** (KognogOS issue #1 — /usr/local/bin shims with
  branded message + PreTransaction token hook + root-gated `sudo nog lock`).
- **A3** ✅ **DONE 2026-08-05** · `nog deactivate chaotic-aur` / `activate chaotic-aur` —
  shipped (nog commit `a417a0e`, issue [#4](https://github.com/jetomev/nog/issues/4) closed):
  `#nog# `-marker section toggle in pacman.conf (user comments survive; byte-exact restore
  proven by unit test AND live `diff` against the pre-deactivation backup), timestamped
  backup → sudo-tee write → sources.toml mirror → `-Sy` refresh. Field-verified: chaotic
  vanished from the sync list, then returned as the fourth DB. Tests 49→54. **The
  incident-response toolkit (#2 fence + #3 aur switch + #4 chaotic switch) is complete.**
- **A4** ✅ **DONE 2026-08-05** · Held table sorted by days-remaining ascending — shipped
  (nog commit `78e6164`, issue [#6](https://github.com/jetomev/nog/issues/6) closed;
  field-verified on a 171-row hold list — the table now visualizes the tier gradient,
  1-day T3 movers on top, 23-day T1 kernels at the bottom; CSV log mirrors the order).
- **A5** ✅ **DONE 2026-08-05** · Release ritual complete: version sync (F-1 caught: in-tree
  PKGBUILD had been stale at 1.0.7 since v1.0.8), man page + README sweep (privilege-model
  honesty pass, sources.toml section, roadmap + changelog, AUR-freeze notice under the
  badges), `testing/` Matrix §19 + Results, audit gates green (54/54 locked, no scaffolding,
  no path leak, warnings steady at 7), docs commit `85b58e0` + `7913e46`, **tag `v1.0.9`
  pushed, [GitHub Release live](https://github.com/jetomev/nog/releases/tag/v1.0.9)**.
  AUR remote **staged locally** (`a91b72c`, checksums from the real tag tarball, ahead-1
  DO-NOT-PUSH) — fires the day the freeze lifts (checklist steps 9–11).

**🏁 PHASE A COMPLETE — nog v1.0.9 "Ironhold" released, 2026-08-05, in a single evening.**

### Phase B — signing & hardening (~2–3 nights, Aug 12–14)
- **B1 ✅ (2026-08-09)** · GPG: verify/create Javier's signing key; `git config commit.gpgsign` across
  → DONE: no prior key existed; ed25519 key `32E1D2AB9380BFD6BFE3BC1EAC2A3407CC070F9E` cast (expires 2028-08-08 — RENEW ~June 2028), passphrase in the password manager, revocation cert in `~/.gnupg/openpgp-revocs.d/`; `commit.gpgsign` + `tag.gpgSign` set GLOBALLY (covers all repos); public key uploaded to GitHub (`gh gpg-key add`, scope refreshed). This very commit is the first signed one.
  nog + grubForge + alacrittyForge + BitlaForge + forgekit + kognog; key uploaded to
  GitHub (Verified badge on all future commits).
- **B2 ✅ (2026-08-09)** · Signed release artifacts starting with nog v1.0.9 (sha256 manifest + `.asc`);
  PKGBUILD updates with `validpgpkeys` prepared locally for all 4 AUR packages —
  staged, pushed when AUR reopens.
- **B3 ✅ (2026-08-04, documented 08-09)** · AUR account hardening completed (from N0): password rotated + new SSH key.
- **B4 ✅ (2026-08-09)** · Typosquat watch: small script querying AUR RPC for `nog*`, `*forge*` lookalikes,
  weekly systemd timer, ntfy alert on hits. Fails gracefully while AUR is down.


**Phase B execution notes (2026-08-09 — completed in ONE evening, 3 nights ahead):**
- B2: signed tarball + SHA256SUMS + detached `.asc` pairs attached to the current
  GitHub release of ALL five repos (nog v1.0.9, forgekit v0.2.1, bitlaforge v0.2.1,
  grubforge v1.0.3, alacrittyforge v0.1.1); key published to keys.openpgp.org.
  All five AUR PKGBUILDs re-pointed at the signed release assets with
  `validpgpkeys` and verified end-to-end via `makepkg --verifysource` —
  committed locally, DO-NOT-PUSH until the AUR reopens. ⚠️ Cache lesson: stale
  same-named tarballs in the package dir make updpkgsums lie — purge sources
  before re-summing after a source-URL change.
- B4: `scripts/aur-typosquat-watch.sh` + user-timer units (in
  `scripts/systemd-user/`, installed on the desktop, Mondays 09:00): exact
  `-bin/-git/-opt` lookalike probes (loud, every run) + delta scan against a
  seeded baseline (47 names) for watch terms; ntfy topic `aur-watch`
  (delivery tested); silent graceful exit while the AUR is unreachable.
- 🔑 Key fingerprint: `32E1D2AB9380BFD6BFE3BC1EAC2A3407CC070F9E` — expires
  2028-08-08, **renew ~June 2028**; passphrase in the password manager;
  revocation cert in `~/.gnupg/openpgp-revocs.d/`.

### Phase C ✅ (2026-08-09 — a week early) — communication: "Where We Stand" article
- **C1** · One article, written once, linked everywhere: what happened in the AUR,
  what we verified on our own systems, what we changed (fail-closed holds, kill switch,
  signing), and the KognogOS doctrine — tiered holds + curated pins as the design answer
  to supply-chain risk. Honest tone; no fear-marketing.
- **C2** · Cross-linking pass: README section in nog, grubForge, alacrittyForge,
  BitlaForge, forgekit, kognog → the article. (Canonical home: this repo's `docs/`.)


**Phase C execution notes (2026-08-09):** `docs/where-we-stand.md` written and live
(canonical home = this repo, per plan): the attack story, our Aug-4 audit verdict,
the full signing chain with the key fingerprint, a verify-us-don't-trust-us recipe,
and the AUR-vs-GitHub version table for the freeze period. Security block
cross-linked in all 6 READMEs (kognog, nog, grubforge, alacrittyforge, bitlaforge,
forgekit — all pushed, all Verified). The four closed nog Ironhold issues (#2/3/4/6)
got the article link as a follow-up comment. On AUR reopen: add the dated banner at
the TOP of the article naming the versions that went live, and refresh the table.

### Phase D — closure (1 night, Aug 18–19)
- **D1** · Sweep: all tasks green or explicitly accepted; memories + vault session log.
- **D2** · **Orlando checklist:** nothing open in risk/security/safety; nog is manual
  (nothing auto-updates while away); Pi realm unaffected by this topic (Ubuntu);
  AUR ship staged and waiting only on Arch.

**Slack:** Aug 15 + weekend nights are unscheduled buffer. If A overruns, C compresses to
one night before anything else moves.

---

## 3 · External dependencies

- **AUR push freeze (Arch, no ETA):** ✅ **CLOSED 2026-08-14 — the AUR reopened and every
  staged package shipped**, five days ahead of the Orlando deadline. Live: `nog` v1.2.0,
  `python-forgekit` v0.3.0 (first new submission), `alacrittyforge` v0.2.0,
  `bitlaforge` v0.2.1, `grubforge` v1.0.3 (B2 hardening). All five reinstalled from the
  AUR through nog/yay and verified end to end. The "ready-to-ship" doctrine paid off
  exactly as designed: the push itself was the 15-minute action it was planned to be.

  Two findings from pressing send, worth keeping:

  1. **Local `makepkg` runs had polluted all five AUR repos.** `pkg/`, `src/` and the
     downloaded tarballs were committed — including `.BUILDINFO` and `.MTREE`, which
     describe the local build environment. Nothing published was ever affected, but it
     sat in the staged commits. **AUR's own hook refused the push** (`the repository
     must not contain subdirectories`) — and it validates *every commit in the push*,
     not just the resulting tree, so a cleanup commit on top was not enough. Each
     repo's unpushed work was rebuilt as one clean commit and a `.gitignore` now blocks
     the class outright.
  2. **The key was fine; the agent was missing.** Auth failed with
     `Permission denied (publickey)` even though the server logged `Server accepts key`
     — the AUR key is passphrase-protected and no ssh-agent was running. Worth
     remembering before assuming an account problem.

- Our definition of done was **our side complete**, and it held: nothing external
  remained once Arch reopened.
- AUR RPC availability affects B4 testing only; the script degrades gracefully.

## 4 · Decisions
| Decision | Call | Rationale |
|----------|------|-----------|
| Co-maintainer on AUR packages | **Deferred — accepted risk** | No trusted candidate today; signing + hygiene mitigate; revisit at Forge v2 |
| Maintainer-change detector | **nog v2 roadmap** | Right feature, wrong sprint |
| snap support | **Parked** (standing) | Unchanged |
| Article canonical home | kognog `docs/` — pending Javier confirmation | Umbrella repo = doctrine home |
