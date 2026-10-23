#!/usr/bin/env python3
"""KognogOS's board, linked to the projects it is made of (Javier, 2026-10-22: "KognogOS exists thanks to all
other projects… did you cross them out? if not, you should").

The 1.0 cut (2026-10-21) COPIED every pending line from nog, the Forge Suite and the other apps onto the board;
from then on the copies drifted. The bar guard was done on hypeForge's board and open here; nogForge #17–#20
had shipped on 10-07 and were still on the cut. docs/board/links.json now ties each item to its twin:

    "steps":  ["<project>:<step id>", …]   the project's TODO.md lines (mindForge's board.py ids); done = all ticked
    "issues": ["<owner/repo>#<n>", …]       GitHub issues; done = all closed
    "own":    "<why>"                       KognogOS's own step (the disc, a test, a decision): no twin
    "unclear": "<what to ask>"              not linked until Javier says what it means

The project's TODO stays the record: ticks flow from the project to this board, never back. A tick here with
its twin still open is reported for a person to settle.

    board-links.py check [<export-dir>]           the drift, in plain words (the board: an export, or docs/board/state.json)
    board-links.py check <export-dir> --plan F    and the ArtifactData batch that brings the board in step, to F
    board-links.py badges <out-dir>               per project, the 1.0 badge for each linked step (for board.py build --badges)

Exit 0 when the board and its projects agree, 1 when they don't, 2 on a usage error.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LINKS = HERE / "docs/board/links.json"
STATE = HERE / "docs/board/state.json"
PROGRAMS = Path.home() / "Programs"
# alacrittyForge and bitlaForge moved into forge-suite on 2026-10-22 (~/Programs/<app> are shortcuts to there)
DIRS = {"nog": "nog", "nogforge": "nogforge", "grubforge": "grubforge", "alacrittyforge": "forge-suite/alacrittyforge",
        "bitlaforge": "forge-suite/bitlaforge", "forge-suite": "forge-suite", "hypeforge": "forge-suite/hypeforge",
        "displayforge": "forge-suite/displayforge", "forgekit": "forge-suite/forgekit", "sudoforge": "forge-suite/sudoforge",
        "workspaceforge": "forge-suite/workspaceforge", "defaultappsforge": "forge-suite/defaultappsforge",
        "themeforge": "forge-suite/themeforge", "walletforge": "forge-suite/walletforge", "nightforge": "forge-suite/nightforge"}
NAMES = {"nog": "nog", "nogforge": "nogForge", "grubforge": "grubForge", "alacrittyforge": "alacrittyForge",
         "bitlaforge": "bitlaForge", "forge-suite": "Forge Suite", "hypeforge": "hypeForge", "displayforge": "displayForge",
         "forgekit": "forgekit", "sudoforge": "sudoForge", "workspaceforge": "workspaceForge",
         "defaultappsforge": "defaultappsForge", "themeforge": "themeForge", "walletforge": "walletForge",
         "nightforge": "nightForge"}
REPOS = {"jetomev/nog": "nog", "jetomev/nogforge": "nogforge", "jetomev/grubforge": "grubforge",
         "jetomev/alacrittyforge": "alacrittyforge", "jetomev/bitlaforge": "bitlaforge", "jetomev/forge-suite": "forge-suite"}


def board_tool():
    spec = importlib.util.spec_from_file_location("board", PROGRAMS / "mindforge/boards/board.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def steps_by_project() -> dict[str, dict[str, dict]]:
    board = board_tool()
    out = {}
    for key, rel in DIRS.items():
        todo = PROGRAMS / rel / "TODO.md"
        out[key] = {it["id"]: dict(it, stage=s["name"]) for s in board.parse(todo)[1] for it in s["items"]} if todo.exists() else {}
    return out


def issue_state(ref: str) -> str | None:
    repo, n = ref.split("#")
    try:
        r = subprocess.run(["gh", "issue", "view", n, "-R", repo, "--json", "state", "-q", ".state"],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout.strip() or None


def load_board(src: Path | None) -> tuple[dict, dict]:
    """(items, versions) from an export directory (items/<id>.json), or the committed snapshot."""
    if src and (src / "items").is_dir():
        items, versions = {}, {}
        for p in (src / "items").glob("*.json"):
            d = json.loads(p.read_text())
            items[p.stem] = d.get("data", d)
            versions[p.stem] = d.get("version")
        # ArtifactData's export files hold the fields only; the listing that wrote them names each version —
        # saved beside them as _versions.json ({id: version}) so a write can be pinned
        if (src / "_versions.json").exists():
            versions.update(json.loads((src / "_versions.json").read_text()))
        return items, versions
    return json.loads(STATE.read_text())["items"], {}


def project_of(link: dict) -> str | None:
    if link.get("steps"):
        return link["steps"][0].split(":")[0]
    if link.get("issues"):
        return REPOS.get(link["issues"][0].split("#")[0])
    return None


def judge(links: dict, steps: dict) -> dict[str, dict]:
    """Per linked item: {done: True/False/None, open: [what is still open], broken: [...], label}."""
    out = {}
    issues = {i for l in links.values() for i in l.get("issues", [])}
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=12) as pool:          # ~40 issues: seconds, not a minute
        states = dict(zip(sorted(issues), pool.map(issue_state, sorted(issues))))
    for iid, link in links.items():
        if "own" in link or "unclear" in link:
            continue
        left, broken, unknown = [], [], False
        for ref in link.get("steps", []):
            proj, sid = ref.split(":")
            st = steps.get(proj, {}).get(sid)
            if st is None:
                broken.append(ref)
            elif not st["done"]:
                left.append(f"{NAMES[proj]}: {st['title'][:70]}")
        for ref in link.get("issues", []):
            s = states.get(ref)
            if s is None:
                unknown = True
            elif s != "CLOSED":
                left.append(ref)
        done = None if (broken or unknown) else not left
        out[iid] = {"done": done, "left": left, "broken": broken, "project": project_of(link)}
    return out


def check(args: list[str]) -> int:
    src = Path(args[0]) if args and not args[0].startswith("--") else None
    plan = Path(args[args.index("--plan") + 1]) if "--plan" in args else None
    links = json.loads(LINKS.read_text())
    items, versions = load_board(src)
    verdict = judge(links, steps_by_project())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    to_tick, ticked_open, broken, writes = [], [], [], []
    for iid, v in sorted(verdict.items()):
        it = items.get(iid)
        if it is None:
            broken.append(f"{iid}: not on the board")
            continue
        if v["broken"]:
            broken.append(f"{iid}: its project line is gone ({', '.join(v['broken'])}) — the line was reworded or removed")
        elif v["done"] and not it.get("done"):
            to_tick.append(f"{iid}  {it['title'][:80]}")
            if versions.get(iid):
                writes.append({"op": "update", "collection": "items", "doc_id": iid, "if_version": versions[iid],
                               "data": {"done": True, "doneAt": now, "doneFrom": NAMES.get(v["project"], v["project"])}})
        elif v["done"] is False and it.get("done"):
            ticked_open.append(f"{iid}  {it['title'][:70]}  ← still open: {'; '.join(v['left'])[:120]}")
    unclear = [f"{k}: {l['unclear']}" for k, l in links.items() if "unclear" in l]
    print(f"KognogOS board ↔ its projects: {len(verdict)} items linked, "
          f"{sum(1 for l in links.values() if 'own' in l)} KognogOS's own, {len(unclear)} unclear")
    for head, rows in (("Done in its project, still open on the board (the board catches up)", to_tick),
                       ("Ticked on the board, still open in its project (a person settles it)", ticked_open),
                       ("Broken links (fix links.json)", broken), ("Unclear (ask Javier)", unclear)):
        if rows:
            print(f"\n{head}: {len(rows)}")
            for r in rows:
                print("  " + r)
    if plan is not None:
        plan.write_text(json.dumps(writes, indent=1, ensure_ascii=False))
        print(f"\nplan: {len(writes)} write(s) → {plan}")
    if not (to_tick or ticked_open or broken):
        print("\nin step: every linked item agrees with its project")
    unknown = sum(1 for v in verdict.values() if v["done"] is None and not v["broken"])
    if unknown:
        print(f"\n{unknown} item(s) not judged: GitHub didn't answer (offline?)")
    return 0 if not (to_tick or ticked_open or broken) else 1


def badges(args: list[str]) -> int:
    """Per project, {step id: "KognogOS 1.0 · stage NN"} (or "KognogOS 1.x") for every step linked to an item."""
    out = Path(args[0])
    out.mkdir(parents=True, exist_ok=True)
    st = json.loads(STATE.read_text())
    stage_of = {i: n for n, s in enumerate(st["road"]["stages"]) for i in s["items"]}
    per = {}
    for iid, link in json.loads(LINKS.read_text()).items():
        it = st["items"].get(iid, {})
        if iid in stage_of:
            text = f"KognogOS 1.0 · stage {stage_of[iid]:02d}"
        elif it.get("pick") == "1.x":
            text = "KognogOS 1.x"
        elif it.get("pick") == "1.0":
            text = "KognogOS 1.0"
        else:
            continue
        for ref in link.get("steps", []):
            proj, sid = ref.split(":")
            per.setdefault(proj, {})[sid] = text
    for proj, b in per.items():
        (out / f"{proj}.json").write_text(json.dumps(b, indent=1, ensure_ascii=False) + "\n")
    print(f"badges: {sum(len(b) for b in per.values())} steps in {len(per)} projects → {out}")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["check"]:
        return check(argv[1:])
    if argv[:1] == ["badges"] and len(argv) == 2:
        return badges(argv[1:])
    print(__doc__.strip().split("\n\n")[-2], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
