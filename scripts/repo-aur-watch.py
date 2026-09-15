#!/usr/bin/env python3
"""
repo-aur-watch.py — the weekly "is anyone waiting on us?" sweep.

WHY THIS EXISTS
    Outside contact is rare, and nothing on this machine announces it.
    grubForge issue #18 sat unanswered for 26 days, #23 for 2 days, and #27
    for 13 days before anyone noticed. AUR comments are worse: nothing
    surfaces them at all.

WHAT IT DOES
    Once a week it looks at three places and asks one question per item:
    "is the last word in this conversation ours?" If it is not, the item is
    WAITING — and it stays WAITING, reported every single week, until we
    reply. A one-shot "tell me about new things" routine would have gone
    quiet about #27 after week one.

      GitHub  every issue and pull request across the account, plus THREE
              separate comment streams (conversation, code review, commit).
              Checking only the first reports "no comments" while missing
              the other two.
      AUR     comments on our published packages, out-of-date flags, vote
              counts, and whether we still maintain them at all.
      ctx     Luca King's project (github.com/ctxrs/ctx) — informational
              only; nothing there needs a reply from us.

FAIL-LOUD RULE
    An empty result is never trusted. If any source fails, the run reports
    INCOMPLETE and alerts anyway. It never says "all clear" unless every
    source actually answered. A sweep that returns nothing because a command
    broke looks exactly like good news — that already happened, 2026-08-31.

OUTPUT
    stdout   -> the journal (journalctl --user -u repo-aur-watch)
    digest   -> ~/Projects/watch-reports/  (dated file + latest.md)
    ntfy     -> only when something is waiting, or the run was incomplete
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
import unicodedata
import sys
import urllib.error
import urllib.request

ME = "jetomev"
OWNER = "jetomev"

# Packages actually published on the AUR. nogforge is NOT here on purpose:
# it has never been submitted. If that changes, add it.
AUR_PACKAGES = ["nog", "grubforge", "alacrittyforge", "bitlaforge", "python-forgekit"]

OUTSIDE_REPO = "ctxrs/ctx"          # Luca King's ctx — watched, not answered
AUR_RPC = "https://aur.archlinux.org/rpc/v5"
AUR_PKG_URL = "https://aur.archlinux.org/packages"

STATE_DIR = os.path.join(
    os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state")),
    "repo-aur-watch",
)
STATE_FILE = os.path.join(STATE_DIR, "state.json")
REPORT_DIR = os.path.expanduser("~/Projects/watch-reports")
NTFY_URL = os.environ.get("NTFY_URL", "http://192.168.1.200:2586/repo-watch")

NOW = dt.datetime.now(dt.timezone.utc)

# Problems are collected, never raised. A failed source must still produce a
# report — a crash is a silent week.
ERRORS = []


def note_error(where, exc):
    msg = f"{where}: {str(exc)[:300]}"
    ERRORS.append(msg)
    print(f"  !! ERROR {msg}", file=sys.stderr)


# ---------------------------------------------------------------- helpers

def parse_ts(s):
    """GitHub ISO timestamp -> aware datetime."""
    if not s:
        return None
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def days_since(when):
    if not when:
        return 0
    return max(0, (NOW - when).days)


def is_bot(login):
    return not login or login.endswith("[bot]") or login in ("github-actions",)


def load_multi_json(txt):
    """gh --paginate emits one JSON document per page, concatenated.

    Decode however many are present, so this works whether gh returns one
    array or six. Guessing at the format is how a sweep silently returns
    nothing.
    """
    out, i, dec = [], 0, json.JSONDecoder()
    while i < len(txt):
        while i < len(txt) and txt[i].isspace():
            i += 1
        if i >= len(txt):
            break
        obj, i = dec.raw_decode(txt, i)
        out.append(obj)
    return out


def gh_api(path, paginate=True):
    """Call the GitHub API. Raises on failure — callers decide what that means."""
    cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json", path]
    if paginate:
        cmd.append("--paginate")
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:300] or f"exit {p.returncode}")
    txt = p.stdout.strip()
    if not txt:
        return []
    docs = load_multi_json(txt)
    if docs and isinstance(docs[0], list):
        flat = []
        for d in docs:
            flat.extend(d)
        return flat
    return docs[0] if len(docs) == 1 else docs


def reachable(url, timeout=10):
    try:
        urllib.request.urlopen(
            urllib.request.Request(url, method="HEAD",
                                   headers={"User-Agent": "repo-aur-watch/1.0"}),
            timeout=timeout)
        return True
    except urllib.error.HTTPError:
        return True          # it answered; the status code is not our concern
    except Exception:
        return False


def http_get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "repo-aur-watch/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


# ------------------------------------------------------------ github pass

def collect_github():
    """Return (waiting, seen_repos). Every thread whose last word isn't ours."""
    waiting = []

    # /user/repos, NOT /users/<name>/repos — the second one silently returns
    # public repos only. It quietly skipped all three private repos on the
    # very first rehearsal and still reported success.
    repos_raw = gh_api("user/repos?per_page=100&affiliation=owner")
    mine = [r for r in repos_raw
            if (r.get("owner") or {}).get("login") == OWNER]
    repos = [r["name"] for r in mine if not r.get("archived")]
    if not repos:
        raise RuntimeError("repo list came back empty — refusing to call that 'clean'")
    print(f"  github: {len(repos)} active repos")

    for repo in sorted(repos):
        full = f"{OWNER}/{repo}"
        try:
            issues = gh_api(f"repos/{full}/issues?state=all&per_page=100")
            conv = gh_api(f"repos/{full}/issues/comments?per_page=100")
            review = gh_api(f"repos/{full}/pulls/comments?per_page=100")
            commit_c = gh_api(f"repos/{full}/comments?per_page=100")
        except Exception as e:
            note_error(f"github/{repo}", e)
            continue

        threads = {}
        for it in issues:
            n = it["number"]
            threads[n] = {
                "repo": repo,
                "number": n,
                "title": it.get("title", "")[:90],
                "is_pr": "pull_request" in it,
                "state": it.get("state"),
                "closed_at": parse_ts(it.get("closed_at")),
                "url": it.get("html_url", ""),
                "opened_by": (it.get("user") or {}).get("login", "?"),
                "last_actor": (it.get("user") or {}).get("login", "?"),
                "last_at": parse_ts(it.get("created_at")),
            }

        def fold(comments, url_key):
            for c in comments:
                ref = c.get(url_key) or ""
                m = re.search(r"/(\d+)$", ref)
                if not m:
                    continue
                n = int(m.group(1))
                t = threads.get(n)
                if not t:
                    continue
                at = parse_ts(c.get("created_at"))
                who = (c.get("user") or {}).get("login", "?")
                if at and (t["last_at"] is None or at > t["last_at"]):
                    t["last_at"], t["last_actor"] = at, who

        fold(conv, "issue_url")
        fold(review, "pull_request_url")

        for t in threads.values():
            if t["last_actor"] == ME or is_bot(t["last_actor"]):
                continue
            # Closing the thread after their last word counts as an answer.
            if t["state"] == "closed" and t["closed_at"] and t["last_at"] \
                    and t["closed_at"] >= t["last_at"]:
                continue
            waiting.append({
                "kind": "PR" if t["is_pr"] else "issue",
                "where": f"{repo} #{t['number']}",
                "who": t["last_actor"],
                "what": t["title"],
                "days": days_since(t["last_at"]),
                "closed": t["state"] == "closed",
                "url": t["url"],
            })

        for c in commit_c:
            who = (c.get("user") or {}).get("login", "?")
            if who == ME or is_bot(who):
                continue
            waiting.append({
                "kind": "commit comment",
                "where": f"{repo} {(c.get('commit_id') or '')[:7]}",
                "who": who,
                "what": (c.get("body") or "")[:90].replace("\n", " "),
                "days": days_since(parse_ts(c.get("created_at"))),
                "closed": False,
                "url": c.get("html_url", ""),
            })

    return waiting, repos


# --------------------------------------------------------------- aur pass

COMMENT_RE = re.compile(
    r'<h4 id="comment-(\d+)" class="comment-header">(.*?)</h4>', re.S)
DATE_RE = re.compile(r'class="date">([^<]+)<')


def aur_comments(pkg):
    """[(comment_id, author, datetime)] from the package page, newest page only.

    Verified against a busy package (google-chrome, 11 comments) so a zero
    here means zero, not a broken selector.
    """
    page = http_get(f"{AUR_PKG_URL}/{pkg}")
    out = []
    for cid, block in COMMENT_RE.findall(page):
        dm = DATE_RE.search(block)
        when = None
        if dm:
            try:
                when = dt.datetime.strptime(
                    dm.group(1).replace(" (UTC)", ""), "%Y-%m-%d %H:%M"
                ).replace(tzinfo=dt.timezone.utc)
            except ValueError:
                pass
        text = html.unescape(re.sub(r"<[^>]+>", " ", block))
        am = re.match(r"\s*(\S+)\s+commented on", text)
        out.append((cid, am.group(1) if am else "?", when))
    return out


def collect_aur():
    waiting, stats = [], []

    args = "".join(f"&arg[]={p}" for p in AUR_PACKAGES)
    info = json.loads(http_get(f"{AUR_RPC}/info?{args[1:]}"))
    found = {r["Name"]: r for r in info.get("results", [])}

    for pkg in AUR_PACKAGES:
        r = found.get(pkg)
        if not r:
            waiting.append({
                "kind": "AUR", "where": pkg, "who": "—",
                "what": "PACKAGE IS GONE from the AUR",
                "days": 0, "closed": False,
                "url": f"{AUR_PKG_URL}/{pkg}",
            })
            continue

        stats.append({
            "pkg": pkg, "version": r.get("Version", "?"),
            "votes": r.get("NumVotes", 0), "pop": r.get("Popularity", 0.0),
        })

        if r.get("OutOfDate"):
            flagged = dt.datetime.fromtimestamp(r["OutOfDate"], dt.timezone.utc)
            waiting.append({
                "kind": "AUR", "where": pkg, "who": "a user",
                "what": "flagged OUT OF DATE",
                "days": days_since(flagged), "closed": False,
                "url": f"{AUR_PKG_URL}/{pkg}",
            })

        if r.get("Maintainer") != ME:
            waiting.append({
                "kind": "AUR", "where": pkg, "who": "—",
                "what": f"maintainer is now {r.get('Maintainer')!r}, not us",
                "days": 0, "closed": False,
                "url": f"{AUR_PKG_URL}/{pkg}",
            })

        try:
            cs = aur_comments(pkg)
        except Exception as e:
            note_error(f"aur-comments/{pkg}", e)
            continue

        mine = [c[2] for c in cs if c[1] == ME and c[2]]
        newest_mine = max(mine) if mine else None
        for cid, who, when in cs:
            if who == ME or not when:
                continue
            if newest_mine and when <= newest_mine:
                continue
            waiting.append({
                "kind": "AUR comment", "where": pkg, "who": who,
                "what": "comment with no reply from us",
                "days": days_since(when), "closed": False,
                "url": f"{AUR_PKG_URL}/{pkg}#comment-{cid}",
            })

    return waiting, stats


# --------------------------------------------------------------- ctx pass

def collect_ctx(state):
    repo = gh_api(f"repos/{OUTSIDE_REPO}", paginate=False)
    info = {
        "stars": repo.get("stargazers_count", 0),
        "pushed": (repo.get("pushed_at") or "")[:10],
        "release": None,
        "release_at": None,
        "new_release": False,
        "open_issues": repo.get("open_issues_count", 0),
    }
    try:
        rel = gh_api(f"repos/{OUTSIDE_REPO}/releases/latest", paginate=False)
        info["release"] = rel.get("tag_name")
        info["release_at"] = (rel.get("published_at") or "")[:10]
        info["new_release"] = bool(
            info["release"] and state.get("ctx_release") not in (None, info["release"])
        )
    except Exception:
        pass  # a project with no releases is not an error
    info["star_delta"] = info["stars"] - state.get("ctx_stars", info["stars"])
    return info


# ----------------------------------------------------------------- output

def build_report(waiting, gh_repos, aur_stats, ctx, state):
    L = []
    day = NOW.astimezone().strftime("%A %-d %B %Y")
    L.append(f"# Watch report — {day}\n")

    if ERRORS:
        L.append("## ⚠ This run was INCOMPLETE\n")
        L.append("Some checks did not answer, so this report is **not** proof "
                 "that everything is fine:\n")
        for e in ERRORS:
            L.append(f"- {e}")
        L.append("")

    if waiting:
        L.append(f"## {len(waiting)} waiting for a reply from you\n")
        L.append("Sorted by how long they have been waiting. These reappear "
                 "every week until the last word in the thread is yours.\n")
        L.append("| Waiting | Where | Who | What |")
        L.append("|---|---|---|---|")
        for w in sorted(waiting, key=lambda x: -x["days"]):
            age = "today" if w["days"] == 0 else f"**{w['days']} days**"
            tag = " _(closed)_" if w.get("closed") else ""
            where = f"[{w['where']}]({w['url']})" if w["url"] else w["where"]
            L.append(f"| {age} | {where}{tag} | `{w['who']}` | {w['what']} |")
        L.append("")
    elif not ERRORS:
        L.append("## Nothing is waiting for a reply\n")
        L.append("Every conversation across GitHub and the AUR ends with your "
                 "word. All checks answered.\n")

    if aur_stats:
        L.append("## AUR packages\n")
        L.append("| Package | Version | Votes | Popularity |")
        L.append("|---|---|---|---|")
        for s in aur_stats:
            prev = state.get("aur_votes", {}).get(s["pkg"])
            delta = ""
            if prev is not None and s["votes"] != prev:
                delta = f" ({s['votes'] - prev:+d})"
            L.append(f"| {s['pkg']} | {s['version']} | {s['votes']}{delta} "
                     f"| {s['pop']:.2f} |")
        L.append("")

    if ctx:
        L.append("## ctx — Luca King (watched, nothing to answer)\n")
        d = f" ({ctx['star_delta']:+d} this week)" if ctx.get("star_delta") else ""
        L.append(f"- **Stars:** {ctx['stars']}{d}")
        L.append(f"- **Last push:** {ctx['pushed']}")
        if ctx.get("release"):
            new = "  ← **NEW**" if ctx.get("new_release") else ""
            L.append(f"- **Latest release:** {ctx['release']} "
                     f"({ctx['release_at']}){new}")
        L.append(f"- **Open issues:** {ctx['open_issues']}")
        L.append("")

    L.append("---\n")
    L.append(f"Checked {len(gh_repos)} GitHub repos and "
             f"{len(AUR_PACKAGES)} AUR packages at "
             f"{NOW.astimezone().strftime('%Y-%m-%d %H:%M %Z')}.")
    return "\n".join(L) + "\n"


# HTTP headers are latin-1 only. An em dash in a notification title raises
# UnicodeEncodeError and the push never leaves the machine — found the hard
# way on the very first live test, 2026-09-15. The message BODY is fine as
# UTF-8; only headers need flattening.
_HEADER_SUBS = {
    "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
    "\u2192": "->", "\u2022": "*", "\u26a0": "!",
}


def ascii_header(value):
    for bad, good in _HEADER_SUBS.items():
        value = value.replace(bad, good)
    # Strip accents rather than delete the letter: cafe, not caf.
    value = unicodedata.normalize("NFKD", value)
    return value.encode("ascii", "ignore").decode("ascii")


def notify(title, body, priority="default", tags=""):
    data = body.encode("utf-8")
    req = urllib.request.Request(NTFY_URL, data=data, method="POST")
    req.add_header("Title", ascii_header(title))
    req.add_header("Priority", ascii_header(priority))
    req.add_header("Content-Type", "text/plain; charset=utf-8")
    if tags:
        req.add_header("Tags", ascii_header(tags))
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


# ------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Weekly repo + AUR watch")
    ap.add_argument("--no-notify", action="store_true",
                    help="run everything but send no push")
    ap.add_argument("--no-state", action="store_true",
                    help="do not write the state file (safe rehearsal)")
    ap.add_argument("--test-notify", action="store_true",
                    help="send one test push and exit")
    args = ap.parse_args()

    if args.test_notify:
        try:
            notify("Repo watch — test", "If you can read this, the weekly "
                   "watch can reach your phone.", "default", "white_check_mark")
            print("test push sent to", NTFY_URL)
            return 0
        except Exception as e:
            print("test push FAILED:", e, file=sys.stderr)
            return 1

    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            state = json.load(open(STATE_FILE))
        except Exception as e:
            note_error("state-file", e)

    print(f"{NOW.isoformat()} repo-aur-watch starting")

    # If the whole machine is offline, this is not news — he already knows.
    # Write an honest INCOMPLETE report, but do not push. Nothing is lost:
    # "waiting" is recomputed from scratch every run against real dates, so a
    # missed week cannot hide an item. It simply reappears next Monday.
    offline = not (reachable("https://api.github.com")
                   or reachable("https://aur.archlinux.org"))
    if offline:
        note_error("network", "machine appears offline — no source reachable")

    waiting, gh_repos = [], []
    try:
        waiting, gh_repos = collect_github()
    except Exception as e:
        note_error("github", e)

    aur_stats = []
    try:
        w, aur_stats = collect_aur()
        waiting += w
    except Exception as e:
        note_error("aur", e)

    ctx = None
    try:
        ctx = collect_ctx(state)
    except Exception as e:
        note_error("ctx", e)

    report = build_report(waiting, gh_repos, aur_stats, ctx, state)
    stamp = NOW.astimezone().strftime("%Y-%m-%d")
    dated = os.path.join(REPORT_DIR, f"{stamp}-watch.md")
    latest = os.path.join(REPORT_DIR, "latest.md")
    for path in (dated, latest):
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
    print(f"  report written: {dated}")

    # Push only when it matters: something is waiting, or we cannot prove
    # nothing is. A quiet phone must mean a genuinely quiet week.
    if not args.no_notify and not offline:
        try:
            if ERRORS and not waiting:
                notify("Repo watch INCOMPLETE",
                       "Some checks failed, so nothing can be ruled out.\n"
                       + "\n".join(f"• {e[:120]}" for e in ERRORS[:5])
                       + f"\n\n{latest}", "high", "warning")
            elif waiting:
                top = sorted(waiting, key=lambda x: -x["days"])[:6]
                lines = [f"• {w['where']} — {w['who']} — {w['days']}d"
                         for w in top]
                if len(waiting) > len(top):
                    lines.append(f"• …and {len(waiting) - len(top)} more")
                if ERRORS:
                    lines.append(f"⚠ {len(ERRORS)} check(s) also FAILED")
                notify(f"{len(waiting)} waiting for your reply",
                       "\n".join(lines) + f"\n\n{latest}", "high", "speech_balloon")
        except Exception as e:
            note_error("ntfy", e)

    if not args.no_state:
        state["last_run"] = NOW.isoformat()
        state["aur_votes"] = {s["pkg"]: s["votes"] for s in aur_stats}
        if ctx:
            state["ctx_stars"] = ctx["stars"]
            if ctx.get("release"):
                state["ctx_release"] = ctx["release"]
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    if ERRORS:
        print(f"{NOW.isoformat()} INCOMPLETE — {len(ERRORS)} check(s) failed, "
              f"{len(waiting)} waiting")
        return 2
    print(f"{NOW.isoformat()} complete — {len(waiting)} waiting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
