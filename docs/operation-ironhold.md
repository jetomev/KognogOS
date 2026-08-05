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
- **A2** · `nog deactivate aur` / `nog activate aur`: config-driven master switch
  (the `[aur] helper = "none"` path already exists — the command flips persisted state,
  every AUR path refuses while off, state shown in the update banner).
- **A3** · `nog deactivate chaotic-aur` / `activate chaotic-aur`: nog comments the repo
  section in/out of `pacman.conf` (timestamped backup first) + DB refresh. User never edits.
- **A4** · Freebie rider (trivial): Held table sorted by days-remaining ascending.
- **A5** · TEST-MATRIX dogfood on the live desktop, docs, changelog, **tag v1.0.9,
  GitHub Release** (GitHub-before-AUR per standing discipline). AUR `makepkg`/push staged
  in `~/Programs/aur-nog-remote/`, **executed the day the freeze lifts**.

### Phase B — signing & hardening (~2–3 nights, Aug 12–14)
- **B1** · GPG: verify/create Balih's signing key; `git config commit.gpgsign` across
  nog + grubForge + alacrittyForge + BitlaForge + forgekit + kognog; key uploaded to
  GitHub (Verified badge on all future commits).
- **B2** · Signed release artifacts starting with nog v1.0.9 (sha256 manifest + `.asc`);
  PKGBUILD updates with `validpgpkeys` prepared locally for all 4 AUR packages —
  staged, pushed when AUR reopens.
- **B3** · AUR account hardening completed (from N0) + documented.
- **B4** · Typosquat watch: small script querying AUR RPC for `nog*`, `*forge*` lookalikes,
  weekly systemd timer, ntfy alert on hits. Fails gracefully while AUR is down.

### Phase C — communication: "Where We Stand" article (~2 nights, Aug 16–17)
- **C1** · One article, written once, linked everywhere: what happened in the AUR,
  what we verified on our own systems, what we changed (fail-closed holds, kill switch,
  signing), and the KognogOS doctrine — tiered holds + curated pins as the design answer
  to supply-chain risk. Honest tone; no fear-marketing.
- **C2** · Cross-linking pass: README section in nog, grubForge, alacrittyForge,
  BitlaForge, forgekit, kognog → the article. (Canonical home: this repo's `docs/`.)

### Phase D — closure (1 night, Aug 18–19)
- **D1** · Sweep: all tasks green or explicitly accepted; memories + vault session log.
- **D2** · **Orlando checklist:** nothing open in risk/security/safety; nog is manual
  (nothing auto-updates while away); Pi realm unaffected by this topic (Ubuntu);
  AUR ship staged and waiting only on Arch.

**Slack:** Aug 15 + weekend nights are unscheduled buffer. If A overruns, C compresses to
one night before anything else moves.

---

## 3 · External dependencies

- **AUR push freeze (Arch, no ETA):** the only item that can remain open on Aug 20 is
  *"press send on the staged AUR pushes"* — by design a 15-minute action, safe to do
  post-Orlando. Our definition of done is **our side complete**.
- AUR RPC availability affects B4 testing only; the script degrades gracefully.

## 4 · Decisions
| Decision | Call | Rationale |
|----------|------|-----------|
| Co-maintainer on AUR packages | **Deferred — accepted risk** | No trusted candidate today; signing + hygiene mitigate; revisit at Forge v2 |
| Maintainer-change detector | **nog v2 roadmap** | Right feature, wrong sprint |
| snap support | **Parked** (standing) | Unchanged |
| Article canonical home | kognog `docs/` — pending Balih confirmation | Umbrella repo = doctrine home |
