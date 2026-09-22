#!/usr/bin/env python3
"""
project-staleness-watch.py — the weekly "are our own projects going stale?" sweep.

WHY THIS EXISTS
    repo-aur-watch.py asks whether anyone is waiting on US. This asks the
    opposite question: is anything of ours quietly rotting while nobody looks?
    Nothing on this machine notices a dependency going a year out of date, a
    repo that has not shipped since spring, or a GitHub About box that still
    says nothing. All three are invisible until someone happens to look, and
    all three are what a potential follower sees first.

WHAT IT CHECKS, per repo we own on GitHub
    shipping     days since the last commit; commits piled up since the last
                 tag; whether the newest tag was ever published as a Release
    dependencies Cargo.toml / pyproject.toml / package.json declared versions
                 against crates.io / PyPI / the npm registry
    security     the same declared versions against OSV (osv.dev), which
                 covers all three ecosystems in one call
    shop window  description, homepage and topics — the things a stranger
                 reads before they read a line of code. Topics rot silently:
                 nothing breaks when they are wrong, so nothing reports it.

WHAT IT DELIBERATELY DOES NOT DO
    It changes nothing and pushes nothing. Javier's ruling, 2026-09-22:
    report only. A green test suite is not the same as a good release.
    It also skips repos whose origin is not github.com/<OWNER> — clones of
    other people's work are not ours to keep fresh — and skips the unpushed /
    uncommitted question entirely, which mindForge and the reply-watch already
    answer. Two tools reporting the same fact is how a fact stops being read.

FAIL-LOUD RULE
    Inherited from repo-aur-watch, and for the same reason: an empty result is
    never trusted. Every source failure is collected, never raised. The run
    then reports INCOMPLETE and alerts anyway. It cannot print "nothing is
    stale" unless every check actually answered. A sweep that finds nothing
    because a request failed looks exactly like good news.

OUTPUT
    stdout -> the journal (journalctl --user -u project-staleness-watch)
    digest -> ~/Projects/watch-reports/YYYY-MM-DD-staleness.md + latest-staleness.md
    ntfy   -> only when something is stale, or the run was incomplete
"""

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tomllib
import unicodedata
import urllib.error
import urllib.request

OWNER = "jetomev"

# Where repos live. Depth 2 is deliberate: a store inside a monorepo
# (dropkit/DecadeDrop) is its own repo and must not be invisible because it
# sits one level further down. That exact blind spot cost us a repo with no
# remote at all — see mindforge#33.
ROOTS = [os.path.expanduser("~/Programs"), os.path.expanduser("~/Projects")]
MAX_DEPTH = 2

STATE_DIR = os.path.join(
    os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state")),
    "project-staleness-watch")
STATE_FILE = os.path.join(STATE_DIR, "state.json")
REPORT_DIR = os.path.expanduser("~/Projects/watch-reports")
NTFY_URL = os.environ.get("NTFY_URL", "http://192.168.1.200:2586/repo-watch")

UA = "project-staleness-watch (github.com/jetomev/kognog)"

NOW = dt.datetime.now(dt.timezone.utc)

# --- thresholds ------------------------------------------------------------
# Deliberately generous. A watch that cries every week teaches you to ignore
# it, and the whole value of this thing is that a push means something.
COMMIT_QUIET_DAYS = 75        # no commit at all in this long
TAG_QUIET_DAYS = 120          # nothing shipped in this long, with work waiting
UNRELEASED_COMMITS = 12       # this many commits stacked on top of a tag

# Topics that carry the human+AI thesis. L1 release.md calls these two
# load-bearing: they are how the collaboration is discoverable at all.
REQUIRED_TOPICS = ["ai-collaboration", "human-ai"]

# Deliberately parked work. A parked repo is NOT exempt from the checks — its
# dependencies and public surface are still read, and a security advisory in
# one still shouts. Only the "you have not committed in months" finding is
# withdrawn, because for these that is the plan and not the problem.
# Parking is printed in every digest WITH ITS REASON. A silent exclusion is
# how a thing rots: the entry disappears and nobody remembers agreeing to it.
PARKED = {
    "chronicles-of-rullynastre-game":
        "Phase 0 paused until the book is nearer done — parked 2026-09-22",
}

ERRORS = []


def note_error(where, exc):
    msg = f"{where}: {exc}"
    ERRORS.append(msg)
    print("  ! " + msg, file=sys.stderr)


# ------------------------------------------------------------------ helpers

def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{' '.join(args[:3])} -> {p.returncode}: "
                           f"{p.stderr.strip()[:200]}")
    return p.stdout.strip()


def git(repo, *args, default=None):
    """git that answers 'unknown' rather than exploding. A repo with no tags
    is a normal state, not a failure, and must not poison the whole run."""
    try:
        return run(["git", "-C", repo, *args])
    except Exception:
        return default


def days_since(when):
    if not when:
        return None
    return (NOW - when).days


def parse_ts(s):
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def http_json(url, timeout=25, data=None):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("User-Agent", UA)          # crates.io rejects a blank one
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def reachable(url, timeout=10):
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", UA)
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except urllib.error.HTTPError:
        return True                # an answer of any kind is reachability
    except Exception:
        return False


def gh_api(path):
    return json.loads(run(["gh", "api", path]))


# ------------------------------------------------------------- version maths

_NUM = re.compile(r"\d+")


def vtuple(v):
    """Compare versions without depending on a packaging library. Good enough
    to answer 'is the major number behind', which is the only judgement this
    script makes about a version. It never decides an upgrade is safe."""
    if not v:
        return ()
    core = v.split("+")[0].split("-")[0]
    return tuple(int(x) for x in _NUM.findall(core)[:4])


def behind(current, latest):
    c, l = vtuple(current), vtuple(latest)
    if not c or not l:
        return None
    if l <= c:
        return None
    if l[0] > c[0]:
        return "major"
    if len(l) > 1 and len(c) > 1 and l[1] > c[1]:
        return "minor"
    return "patch"


_SPEC = re.compile(r"^([A-Za-z0-9_.\-]+)")


def clean_version(spec):
    """Pull a comparable version out of '^1.2.3', '>=0.5', '~> 2.0'."""
    if not isinstance(spec, str):
        return None
    m = re.search(r"\d+(?:\.\d+)*", spec)
    return m.group(0) if m else None


# --------------------------------------------------------- manifest reading

def deps_cargo(path):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    out = []
    for section in ("dependencies", "build-dependencies"):
        for name, spec in (data.get(section) or {}).items():
            if isinstance(spec, dict):
                if "path" in spec or "git" in spec:
                    continue          # local or git deps have no registry
                spec = spec.get("version")
            v = clean_version(spec)
            if v:
                out.append((name, v, "crates.io"))
    return out


def deps_pyproject(path):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    out = []
    for raw in (data.get("project", {}).get("dependencies") or []):
        m = _SPEC.match(raw.strip())
        if not m:
            continue
        v = clean_version(raw[m.end():])
        if v:
            out.append((m.group(1), v, "PyPI"))
    return out


def deps_package_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for section in ("dependencies", "devDependencies"):
        for name, spec in (data.get(section) or {}).items():
            if not isinstance(spec, str) or spec.startswith(("file:", "link:",
                                                             "workspace:",
                                                             "git+", "github:")):
                continue
            v = clean_version(spec)
            if v:
                out.append((name, v, "npm"))
    return out


# ----------------------------------------------------------- lockfiles
# A declared range is not a version. nog declares tar = "0.4"; the lockfile
# resolves it to 0.4.45, and asking OSV about "0.4" returned four advisories
# that were fixed years before the version actually in use. A security finding
# that is wrong is worse than no security finding at all, because the second
# time you see one you stop reading it.
#
# So: advisories are checked ONLY against versions resolved from a lockfile.
# No lockfile means the check is declared NOT RUN, in the digest, by name.

def _lock_cargo(path):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return {(p["name"], "crates.io"): p["version"]
            for p in data.get("package", []) if p.get("version")}


def _lock_npm_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for key, meta in (data.get("packages") or {}).items():
        if not key.startswith("node_modules/"):
            continue
        name = key.split("node_modules/")[-1]
        if meta.get("version"):
            out[(name, "npm")] = meta["version"]
    return out


_PNPM_PKG = re.compile(r"^  '?([^\s']+)@([0-9][^\s'(]*)'?:", re.M)


def _lock_pnpm(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    head = text.find("\npackages:")
    if head == -1:
        return {}
    out = {}
    for m in _PNPM_PKG.finditer(text[head:]):
        out[(m.group(1), "npm")] = m.group(2)
    return out


LOCKFILES = [
    ("Cargo.lock", _lock_cargo),
    ("package-lock.json", _lock_npm_json),
    ("source/package-lock.json", _lock_npm_json),
    ("pnpm-lock.yaml", _lock_pnpm),
    ("source/pnpm-lock.yaml", _lock_pnpm),
]


def read_lock(repo):
    """(resolved dict, lockfile name) or (None, None) when there is none."""
    for rel, fn in LOCKFILES:
        p = os.path.join(repo, rel)
        if os.path.exists(p):
            try:
                got = fn(p)
            except Exception as e:
                note_error(f"lockfile/{os.path.basename(repo)}/{rel}", e)
                return None, rel
            if got:
                return got, rel
            note_error(f"lockfile/{os.path.basename(repo)}/{rel}",
                       "parsed to zero packages — the format probably changed")
            return None, rel
    return None, None


MANIFESTS = [
    ("Cargo.toml", deps_cargo),
    ("pyproject.toml", deps_pyproject),
    ("package.json", deps_package_json),
    ("source/package.json", deps_package_json),
]


def read_deps(repo):
    """Returns (deps, manifest_name, unparsed_reason). A repo with no manifest
    is a normal state here: three of the Forge apps declare their runtime in a
    PKGBUILD and nowhere else."""
    for rel, fn in MANIFESTS:
        p = os.path.join(repo, rel)
        if os.path.exists(p):
            try:
                return fn(p), rel, None
            except Exception as e:
                return [], rel, str(e)[:160]
    return [], None, None


# ------------------------------------------------------------ registry facts

_LATEST_CACHE = {}


def latest_version(name, ecosystem):
    key = (name, ecosystem)
    if key in _LATEST_CACHE:
        return _LATEST_CACHE[key]
    try:
        if ecosystem == "crates.io":
            d = http_json(f"https://crates.io/api/v1/crates/{name}")
            v = (d.get("crate") or {}).get("max_stable_version")
        elif ecosystem == "PyPI":
            d = http_json(f"https://pypi.org/pypi/{name}/json")
            v = (d.get("info") or {}).get("version")
        else:
            d = http_json(f"https://registry.npmjs.org/{name}")
            v = (d.get("dist-tags") or {}).get("latest")
    except Exception as e:
        note_error(f"registry/{ecosystem}/{name}", e)
        v = None
    _LATEST_CACHE[key] = v
    return v


def osv_query(deps):
    """One batch call covers every ecosystem. A vulnerability in something we
    depend on is the one finding here that is not a matter of taste."""
    if not deps:
        return {}
    # A full transitive tree is hundreds of packages; OSV caps a batch, and a
    # rejected oversized batch would come back as "no vulnerabilities".
    CHUNK = 400
    hits = {}
    for i in range(0, len(deps), CHUNK):
        part = deps[i:i + CHUNK]
        queries = [{"package": {"name": n, "ecosystem": eco}, "version": v}
                   for n, v, eco in part]
        try:
            res = http_json("https://api.osv.dev/v1/querybatch",
                            data=json.dumps({"queries": queries}).encode())
        except Exception as e:
            note_error(f"osv/batch-{i // CHUNK}", e)
            return None
        results = res.get("results", [])
        if len(results) != len(part):
            note_error("osv", f"asked about {len(part)} packages, got "
                              f"{len(results)} answers — results misaligned")
            return None
        for (n, v, eco), r in zip(part, results):
            vulns = r.get("vulns") or []
            if vulns:
                hits[(n, eco)] = (v, [x.get("id") for x in vulns[:4]])
    return hits


# --------------------------------------------------------------- discovery

def find_repos():
    found = []
    for root in ROOTS:
        if not os.path.isdir(root):
            note_error("root", f"{root} does not exist")
            continue
        stack = [(root, 0)]
        while stack:
            d, depth = stack.pop()
            if depth > MAX_DEPTH:
                continue
            try:
                entries = sorted(os.scandir(d), key=lambda e: e.name)
            except OSError as e:
                note_error(f"scan/{d}", e)
                continue
            for e in entries:
                if not e.is_dir(follow_symlinks=False) or e.name.startswith("."):
                    continue
                if os.path.isdir(os.path.join(e.path, ".git")):
                    found.append(e.path)
                stack.append((e.path, depth + 1))
    return sorted(set(found))


def github_slug(repo):
    url = git(repo, "remote", "get-url", "origin")
    if not url:
        return None
    m = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", url)
    if not m:
        return None                       # AUR and other non-GitHub remotes
    if m.group(1).lower() != OWNER.lower():
        return None                       # someone else's project, not ours
    return f"{m.group(1)}/{m.group(2)}"


# ------------------------------------------------------------- the checks

def inspect(repo, slug, want_network=True):
    r = {"path": repo, "name": os.path.relpath(repo, os.path.dirname(repo)),
         "slug": slug, "findings": [], "notes": []}
    r["name"] = slug.split("/", 1)[1] if slug else os.path.basename(repo)

    # --- shipping cadence, entirely local
    last = parse_ts(git(repo, "log", "-1", "--format=%cI"))
    r["last_commit_days"] = days_since(last)
    tag = git(repo, "describe", "--tags", "--abbrev=0")
    r["tag"] = tag
    if tag:
        tdate = parse_ts(git(repo, "log", "-1", "--format=%cI", tag))
        r["tag_days"] = days_since(tdate)
        n = git(repo, "rev-list", "--count", f"{tag}..HEAD")
        r["since_tag"] = int(n) if n and n.isdigit() else None
    else:
        r["tag_days"], r["since_tag"] = None, None

    parked = PARKED.get(os.path.basename(repo)) or PARKED.get(r["name"])
    r["parked"] = parked
    if r["last_commit_days"] is not None and r["last_commit_days"] > COMMIT_QUIET_DAYS:
        if parked:
            r["notes"].append(f"quiet {r['last_commit_days']} days — expected: {parked}")
        else:
            r["findings"].append(("quiet", f"no commit in {r['last_commit_days']} days"))
    if r["since_tag"]:
        if r["since_tag"] >= UNRELEASED_COMMITS:
            r["findings"].append(
                ("unreleased",
                 f"{r['since_tag']} commits since {tag} — nothing shipped from them"))
        elif r["tag_days"] and r["tag_days"] > TAG_QUIET_DAYS:
            r["findings"].append(
                ("unreleased",
                 f"{tag} is {r['tag_days']} days old with {r['since_tag']} "
                 f"commits waiting behind it"))
    if not tag:
        r["notes"].append("no tags yet — release cadence not measurable")

    if not want_network or not slug:
        return r

    # --- the shop window: what a stranger sees first
    try:
        meta = gh_api(f"repos/{slug}")
        r["private"] = meta.get("private", False)
        if not meta.get("private"):
            if not (meta.get("description") or "").strip():
                r["findings"].append(("surface", "no About description"))
            topics = meta.get("topics") or []
            r["topics"] = topics
            if not topics:
                r["findings"].append(("surface", "no topics at all"))
            else:
                missing = [t for t in REQUIRED_TOPICS if t not in topics]
                if missing:
                    r["findings"].append(
                        ("surface", "missing topic(s): " + ", ".join(missing)))
            if not (meta.get("homepage") or "").strip():
                r["notes"].append("no website set in About")
    except Exception as e:
        note_error(f"github/{slug}", e)

    # --- was the newest tag ever actually published?
    if tag and not r.get("private"):
        try:
            rel = gh_api(f"repos/{slug}/releases/latest")
            r["release"] = rel.get("tag_name")
            if rel.get("tag_name") != tag:
                r["findings"].append(
                    ("release", f"newest tag {tag} has no GitHub Release "
                                f"(latest published is {rel.get('tag_name')})"))
            elif not (rel.get("body") or "").strip():
                r["findings"].append(("release", f"Release {tag} has empty notes"))
        except Exception as e:
            if "404" in str(e) or "Not Found" in str(e):
                r["findings"].append(
                    ("release", f"tag {tag} exists but the repo has no Releases"))
            else:
                note_error(f"releases/{slug}", e)

    return r


def check_deps(r):
    deps, manifest, broken = read_deps(r["path"])
    r["manifest"] = manifest
    if broken:
        note_error(f"manifest/{r['name']}/{manifest}", broken)
        return
    if not deps:
        return
    r["dep_count"] = len(deps)
    stale = []
    for name, cur, eco in deps:
        latest = latest_version(name, eco)
        if not latest:
            continue                       # already recorded as an error
        lvl = behind(cur, latest)
        if lvl in ("major", "minor"):
            stale.append((name, cur, latest, lvl))
    majors = [s for s in stale if s[3] == "major"]
    if majors:
        r["findings"].append(
            ("deps", f"{len(majors)} dependency major version(s) behind: "
                     + ", ".join(f"{n} {c}→{l}" for n, c, l, _ in majors[:4])))
    elif stale:
        r["notes"].append(f"{len(stale)} minor dependency update(s) available")
    r["stale_deps"] = stale

    resolved, lockname = read_lock(r["path"])
    r["lockfile"] = lockname
    if not resolved:
        # Not an error — plenty of repos legitimately have no lockfile. But it
        # must be SAID, or a silent skip reads as a clean bill of health.
        r["notes"].append(
            "advisories NOT checked — no lockfile, so exact versions are unknown"
            + (f" ({lockname} could not be read)" if lockname else ""))
        r["security_checked"] = False
        return
    r["security_checked"] = True
    ecos = {eco for _, _, eco in deps}
    lockdeps = [(n, v, eco) for (n, eco), v in resolved.items() if eco in ecos]
    r["locked_count"] = len(lockdeps)
    hits = osv_query(lockdeps)
    if hits is None:
        return
    if hits:
        # ONE finding, not one per package. A transitive npm tree can carry a
        # dozen advisories at once; twelve lines on a phone is a wall, and a
        # wall gets dismissed. The count goes in the alert, the names go in
        # the digest, and nothing is dropped.
        names = sorted(hits)
        r["advisories"] = [(n, hits[(n, eco)][0], hits[(n, eco)][1])
                           for n, eco in names]
        total = sum(len(v[1]) for v in hits.values())
        r["findings"].append(
            ("security",
             f"{len(hits)} package(s) with {total} known advisory/advisories: "
             + ", ".join(n for n, _ in names[:5])
             + (f" and {len(names) - 5} more" if len(names) > 5 else "")))


SEVERITY = {"security": 0, "deps": 1, "unreleased": 2, "release": 3,
            "surface": 4, "quiet": 5}


# ----------------------------------------------------------------- report

def build_report(repos, skipped, online=True):
    stale = [r for r in repos if r["findings"]]
    lines = []
    stamp = NOW.astimezone().strftime("%Y-%m-%d %H:%M")
    lines.append(f"# Project staleness — {stamp}")
    lines.append("")
    if not online:
        # Without the network this saw git history and nothing else. Saying
        # "clean" here would be the false all-clear the watch exists to stop.
        lines.append("> ⚠ **LOCAL CHECKS ONLY — the network was not reachable.**")
        lines.append("> Dependencies, security advisories, releases and the "
                     "public surface were NOT checked. Nothing below is an "
                     "all-clear; it is half an answer.")
        lines.append("")
    if ERRORS:
        lines.append(f"> ⚠ **INCOMPLETE — {len(ERRORS)} check(s) failed.** "
                     "Nothing below can be read as an all-clear.")
        lines.append("")
        for e in ERRORS[:20]:
            lines.append(f"> - {e}")
        lines.append("")
    lines.append(f"{len(repos)} repo(s) of ours checked · "
                 f"**{len(stale)} with something to look at** · "
                 f"{len(skipped)} skipped (not ours)")
    lines.append("")

    if not stale:
        lines.append("Nothing is stale. Every repo has shipped recently, every "
                     "dependency is current, and the public surface is intact."
                     if online else
                     "Nothing stale in the local history. The other three "
                     "quarters of this check did not run.")
        lines.append("")
    for r in sorted(stale, key=lambda x: min(SEVERITY[f[0]] for f in x["findings"])):
        lines.append(f"## {r['name']}")
        lines.append("")
        bits = []
        if r.get("last_commit_days") is not None:
            bits.append(f"last commit {r['last_commit_days']}d ago")
        if r.get("tag"):
            bits.append(f"newest tag `{r['tag']}`")
        if r.get("since_tag"):
            bits.append(f"{r['since_tag']} commits since it")
        if r.get("dep_count"):
            bits.append(f"{r['dep_count']} declared dependencies")
        if r.get("locked_count"):
            bits.append(f"{r['locked_count']} resolved from `{r['lockfile']}`")
        lines.append(" · ".join(bits) if bits else "_no local history read_")
        lines.append("")
        for kind, msg in sorted(r["findings"], key=lambda f: SEVERITY[f[0]]):
            lines.append(f"- **{kind}** — {msg}")
        for n in r["notes"]:
            lines.append(f"- _{n}_")
        if r.get("advisories"):
            lines.append("")
            lines.append("<details><summary>every advisory, by package</summary>")
            lines.append("")
            for n, ver, ids in r["advisories"]:
                lines.append(f"- `{n}` {ver} — " + ", ".join(ids))
            lines.append("")
            lines.append("</details>")
        if r.get("stale_deps"):
            minors = [s for s in r["stale_deps"] if s[3] != "major"]
            if minors:
                lines.append("")
                lines.append("<details><summary>minor updates available</summary>")
                lines.append("")
                for n, c, l, _ in minors:
                    lines.append(f"- `{n}` {c} → {l}")
                lines.append("")
                lines.append("</details>")
        lines.append("")

    parked = [r for r in repos if r.get("parked")]
    if parked:
        lines.append("## Parked on purpose")
        lines.append("")
        for r in parked:
            lines.append(f"- `{r['name']}` — {r['parked']}")
        lines.append("")

    quiet = [r for r in repos if not r["findings"] and not r.get("parked")]
    if quiet:
        lines.append("## Clean" if online else "## Clean on local checks only")
        lines.append("")
        lines.append(", ".join(f"`{r['name']}`" for r in quiet))
        lines.append("")

    if skipped:
        lines.append("## Skipped — not ours")
        lines.append("")
        lines.append(", ".join(f"`{os.path.basename(s)}`" for s in skipped))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("This watch reports and changes nothing — Javier's ruling, "
                 "2026-09-22. Its counterpart `repo-aur-watch` asks whether "
                 "anyone is waiting on **us**; this one asks whether anything "
                 "of **ours** is rotting.")
    lines.append("")
    return "\n".join(lines)


# -------------------------------------------------------------------- ntfy

_HEADER_SUBS = {
    "—": "-", "–": "-", "‘": "'", "’": "'",
    "“": '"', "”": '"', "…": "...", " ": " ",
    "→": "->", "•": "*", "⚠": "!",
}


def ascii_header(value):
    # HTTP headers are latin-1. An em dash in a title raised UnicodeEncodeError
    # and the push never left the machine — repo-aur-watch, 2026-09-15.
    for bad, good in _HEADER_SUBS.items():
        value = value.replace(bad, good)
    value = unicodedata.normalize("NFKD", value)
    return value.encode("ascii", "ignore").decode("ascii")


def notify(title, body, priority="default", tags=""):
    req = urllib.request.Request(NTFY_URL, data=body.encode("utf-8"),
                                 method="POST")
    req.add_header("Title", ascii_header(title))
    req.add_header("Priority", ascii_header(priority))
    req.add_header("Content-Type", "text/plain; charset=utf-8")
    if tags:
        req.add_header("Tags", ascii_header(tags))
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


# -------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Weekly project staleness watch")
    ap.add_argument("--no-notify", action="store_true",
                    help="run everything but send no push")
    ap.add_argument("--no-state", action="store_true",
                    help="do not write the state file (safe rehearsal)")
    ap.add_argument("--offline", action="store_true",
                    help="local git checks only — no registry or GitHub calls")
    ap.add_argument("--test-notify", action="store_true",
                    help="send one test push and exit")
    ap.add_argument("--only", metavar="NAME",
                    help="check a single repo by directory name (rehearsal)")
    args = ap.parse_args()

    if args.test_notify:
        try:
            notify("Staleness watch - test",
                   "If you can read this, the staleness watch can reach "
                   "your phone.", "default", "white_check_mark")
            print("test push sent to", NTFY_URL)
            return 0
        except Exception as e:
            print("test push FAILED:", e, file=sys.stderr)
            return 1

    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    print(f"{NOW.isoformat()} project-staleness-watch starting")

    online = True
    if args.offline:
        online = False
    else:
        online = reachable("https://api.github.com")
        if not online:
            # Same doctrine as the reply-watch: if the machine is offline he
            # already knows. Write an honest INCOMPLETE digest, skip the push.
            note_error("network", "api.github.com unreachable — local checks only")

    repos, skipped = [], []
    for path in find_repos():
        slug = github_slug(path)
        if not slug:
            skipped.append(path)
            continue
        if args.only and os.path.basename(path) != args.only:
            continue
        try:
            r = inspect(path, slug, want_network=online)
            if online:
                check_deps(r)
            repos.append(r)
            mark = "!" if r["findings"] else "."
            print(f"  {mark} {r['name']}: {len(r['findings'])} finding(s)")
        except Exception as e:
            note_error(f"inspect/{os.path.basename(path)}", e)

    report = build_report(repos, skipped, online=online)
    stamp = NOW.astimezone().strftime("%Y-%m-%d")
    dated = os.path.join(REPORT_DIR, f"{stamp}-staleness.md")
    latest = os.path.join(REPORT_DIR, "latest-staleness.md")
    for p in (dated, latest):
        with open(p, "w", encoding="utf-8") as f:
            f.write(report)
    print(f"  report written: {dated}")

    stale = [r for r in repos if r["findings"]]
    if not args.no_notify and online:
        try:
            if ERRORS and not stale:
                notify("Staleness watch INCOMPLETE",
                       "Some checks failed, so nothing can be ruled out.\n"
                       + "\n".join(f"• {e[:120]}" for e in ERRORS[:5])
                       + f"\n\n{latest}", "high", "warning")
            elif stale:
                worst = sorted(
                    stale,
                    key=lambda x: min(SEVERITY[f[0]] for f in x["findings"]))[:6]
                lines = []
                for r in worst:
                    kind, msg = sorted(r["findings"],
                                       key=lambda f: SEVERITY[f[0]])[0]
                    lines.append(f"• {r['name']} — {msg[:70]}")
                if len(stale) > len(worst):
                    lines.append(f"• …and {len(stale) - len(worst)} more")
                if ERRORS:
                    lines.append(f"⚠ {len(ERRORS)} check(s) also FAILED")
                sec = any(f[0] == "security" for r in stale for f in r["findings"])
                notify(f"{len(stale)} project(s) going stale",
                       "\n".join(lines) + f"\n\n{latest}",
                       "high" if sec else "default",
                       "rotating_light" if sec else "hourglass")
        except Exception as e:
            note_error("ntfy", e)

    if not args.no_state:
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"last_run": NOW.isoformat(),
                           "checked": len(repos),
                           "stale": [r["name"] for r in stale]}, f, indent=2)
        except Exception as e:
            note_error("state-file", e)

    if ERRORS:
        print(f"{NOW.isoformat()} INCOMPLETE — {len(ERRORS)} check(s) failed, "
              f"{len(stale)} stale")
        return 2
    print(f"{NOW.isoformat()} complete — {len(stale)} stale of {len(repos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
