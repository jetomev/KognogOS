#!/usr/bin/env python3
"""
Tests for project-staleness-watch.py — the parts that fail QUIETLY.

Nothing here touches the network. These cover the three things that can be
wrong without anything looking wrong:

  1. version comparison — decides whether a dependency is "major behind"
  2. lockfile parsing   — a parser that returns {} turns the security check
                          into a silent all-clear, which is the one outcome
                          this watch exists to prevent
  3. the parked list    — a parked repo must still be checked, and must still
                          be PRINTED; silently vanishing is not parking

Run: python3 scripts/tests/test-project-staleness-watch.py
"""

import importlib.util
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "project-staleness-watch.py")

spec = importlib.util.spec_from_file_location("watch", TARGET)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

FAILS = []


def check(name, got, want):
    if got == want:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}: got {got!r}, wanted {want!r}")
        FAILS.append(name)


def section(t):
    print(f"\n{t}")


# ------------------------------------------------------- version comparison
section("version comparison")
check("major jump", w.behind("0.8", "1.1.6"), "major")
check("minor jump", w.behind("0.13", "0.14.0"), "minor")
check("patch jump", w.behind("1.4.1", "1.4.9"), "patch")
check("already current", w.behind("2.0.0", "2.0.0"), None)
# A newer local version than the registry is normal mid-release. It must not
# be reported as being behind.
check("ahead of registry", w.behind("2.1.0", "2.0.0"), None)
check("unknown latest", w.behind("1.0", None), None)
# crates.io really does return strings like this.
check("build metadata ignored", w.behind("1.1.6", "1.1.6+spec-1.1.0"), None)

section("version extraction from a declared range")
check("caret", w.clean_version("^1.2.3"), "1.2.3")
check("gte", w.clean_version(">=8.0"), "8.0")
check("bare", w.clean_version("0.4"), "0.4")
check("tag not a version", w.clean_version("latest"), None)
check("non-string spec", w.clean_version({"version": "1.0"}), None)


# ------------------------------------------------------------ lockfiles
section("lockfile parsing")

CARGO_LOCK = '''version = 3

[[package]]
name = "tar"
version = "0.4.45"
source = "registry+https://github.com/rust-lang/crates.io-index"

[[package]]
name = "zstd"
version = "0.13.3"
'''

# pnpm lockfile v9. The `importers:` block above `packages:` also contains
# name@version-looking text; only the packages section may be read, or the
# resolved set is polluted with specifier ranges.
PNPM_LOCK = """lockfileVersion: '9.0'

importers:

  .:
    dependencies:
      react:
        specifier: ^19.2.6
        version: 19.2.6

packages:

  '@alloc/quick-lru@5.2.0':
    resolution: {integrity: sha512-fake}

  '@babel/core@7.29.0':
    resolution: {integrity: sha512-fake}

  vite@8.0.13:
    resolution: {integrity: sha512-fake}
"""

NPM_LOCK = json.dumps({
    "lockfileVersion": 3,
    "packages": {
        "": {"name": "root"},
        "node_modules/undici": {"version": "7.24.8"},
        "node_modules/@types/node": {"version": "22.19.19"},
    },
})


def with_repo(files):
    d = tempfile.mkdtemp()
    for rel, body in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(body)
    return d


r = with_repo({"Cargo.lock": CARGO_LOCK})
got, name = w.read_lock(r)
check("cargo: file found", name, "Cargo.lock")
check("cargo: count", len(got), 2)
check("cargo: resolves the exact version", got.get(("tar", "crates.io")), "0.4.45")

r = with_repo({"source/pnpm-lock.yaml": PNPM_LOCK})
got, name = w.read_lock(r)
check("pnpm: file found", name, "source/pnpm-lock.yaml")
check("pnpm: scoped package", got.get(("@babel/core", "npm")), "7.29.0")
check("pnpm: unquoted package", got.get(("vite", "npm")), "8.0.13")
# The importers block names react with a specifier, not a resolved entry.
# Reading it would invent a package that is not in the packages section.
check("pnpm: importers block not harvested", ("react", "npm") in got, False)
check("pnpm: count", len(got), 3)

r = with_repo({"package-lock.json": NPM_LOCK})
got, name = w.read_lock(r)
check("npm: file found", name, "package-lock.json")
check("npm: version", got.get(("undici", "npm")), "7.24.8")
check("npm: root entry skipped", len(got), 2)

# THE ONE THAT MATTERS. A lockfile whose format has moved on parses to zero
# packages. Returning {} would hand the caller an empty set, the OSV query
# would be skipped, and the digest would say nothing is wrong. It must come
# back as None AND record an error, so the run reports INCOMPLETE.
w.ERRORS.clear()
r = with_repo({"Cargo.lock": "version = 3\n# no packages at all\n"})
got, name = w.read_lock(r)
check("empty lockfile -> None, not {}", got, None)
check("empty lockfile is recorded as an error", len(w.ERRORS), 1)

w.ERRORS.clear()
r = with_repo({"pnpm-lock.yaml": "this is not: [valid yaml at all"})
got, name = w.read_lock(r)
check("unreadable lockfile -> None", got, None)
check("unreadable lockfile raises an error", len(w.ERRORS) >= 1, True)

w.ERRORS.clear()
got, name = w.read_lock(with_repo({"README.md": "nothing here"}))
check("no lockfile -> None", got, None)
check("no lockfile is NOT an error", len(w.ERRORS), 0)


# ------------------------------------------------------------- ntfy headers
section("ntfy headers must be latin-1 safe")
# An em dash in a title raised UnicodeEncodeError and the push never left the
# machine — repo-aur-watch, 2026-09-15. Same lesson, same code path.
check("em dash flattened", w.ascii_header("5 projects — stale"),
      "5 projects - stale")
check("accents kept as letters", w.ascii_header("café"), "cafe")
check("warning sign", w.ascii_header("⚠ incomplete"), "! incomplete")
try:
    w.ascii_header("• bullet → arrow …").encode("latin-1")
    print("  ok   encodes as latin-1")
except UnicodeEncodeError:
    print("  FAIL latin-1 encode")
    FAILS.append("latin-1")


# --------------------------------------------------------------- parked
section("parked repos")
# Parking withdraws ONE finding and nothing else, and it must be visible.
check("the parked entry carries a reason",
      bool(w.PARKED.get("chronicles-of-rullynastre-game")), True)
report = w.build_report(
    [{"name": "paused-thing", "findings": [], "notes": [], "path": "/x",
      "parked": "because we said so"}], [], online=True)
check("a parked repo is printed", "Parked on purpose" in report, True)
check("the reason is printed", "because we said so" in report, True)
check("not also listed as clean", "## Clean" in report, False)

section("an offline run may never read as an all-clear")
rep = w.build_report([{"name": "x", "findings": [], "notes": [], "path": "/x"}],
                     [], online=False)
check("local-only banner present", "LOCAL CHECKS ONLY" in rep, True)
check("does not claim dependencies are current",
      "every dependency is current" in rep, False)
rep_on = w.build_report([{"name": "x", "findings": [], "notes": [], "path": "/x"}],
                        [], online=True)
check("a full run may say it plainly",
      "every dependency is current" in rep_on, True)


print()
if FAILS:
    print(f"FAILED: {len(FAILS)} — {', '.join(FAILS)}")
    sys.exit(1)
print("all checks passed")
