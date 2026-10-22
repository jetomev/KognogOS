#!/usr/bin/env python3
"""docs/RELEASE-1.0.md, written from the board's snapshot (docs/board/state.json) — never by hand, so the
document can't drift from the board (2026-10-22: the hand-written one still listed five editions a day after
Javier cut them to two). board-snapshot.py runs this after every snapshot.

    board-release-doc.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
STATE = HERE / "docs/board/state.json"
OUT = HERE / "docs/RELEASE-1.0.md"
AREAS = [("disc", "The disc and the installer"), ("boot", "First boot and welcome"), ("desk", "The desktop"),
         ("look", "Styles and colour themes"), ("pop", "Pop-ups"), ("set", "Settings apps"),
         ("sec", "Passwords and security"), ("pkg", "Packages: nog and nogForge"), ("apps", "The other Forge apps"),
         ("sway", "Our Sway build"), ("kde", "Leaving KDE"), ("rel", "Release kit and public face"),
         ("test", "Testing before release"), ("gaps", "Gaps nobody had written down")]
VISION = ("*KognogOS + AI (Claude) full integration. Claude alive while the OS is on, with a tray chat bubble "
          "available for one to request directly there anything. We will create Claude commands to manipulate and "
          "control the OS, and even develop new functionalities, or make changes to it.*")


def line(it: dict) -> str:
    mark = "✅ " if it.get("done") else ""
    detail = f" — *{it['detail']}*" if it.get("detail") else ""
    note = f" **Javier:** {it['note']}" if it.get("note") else ""
    return f"{mark}{it['title']} ({it.get('source', '')}){detail}{note}"


def main() -> int:
    st = json.loads(STATE.read_text())
    road, items = st["road"], st["items"]
    count = {k: sum(1 for it in items.values() if it.get("pick") == k) for k in ("1.0", "1.x", "drop", "?")}
    undecided = sum(1 for it in items.values() if not it.get("pick"))
    on_road = [i for s in road["stages"] for i in s["items"] if i in items]
    done = sum(1 for i in on_road if items[i].get("done"))
    out = ["# KognogOS 1.0 — the cut and the road", "",
           f"*Written from the board's snapshot of {st['taken']} by `scripts/board-release-doc.py` — do not edit by hand. "
           f"The live board: [KognogOS 1.0 Cut]({st['board']}). Javier judged every pending item there (2026-10-21) "
           "and ordered the road (2026-10-21/22).*", "",
           f"**{count['1.0']} ship in v1.0 · {count['1.x']} come during the first year (1.x) · {count['drop']} dropped · "
           f"{count['?'] + undecided} still open. The road: {done} of {len(on_road)} steps done.**", "",
           "v1.0 ships the **Basic** and **Work** editions with the **Rice, Windows 11, KDE and Classic** styles and a smaller set "
           "of colour themes. The Mac styles, COSMIC, and the Full, Gaming and Development editions come during the year.", "",
           "**Beyond the year — v2.0 (Javier, 2026-10-21):** " + VISION, "",
           "## The road to launch", ""]
    for n, s in enumerate(road["stages"]):
        mine = [items[i] for i in s["items"] if i in items]
        d = sum(1 for it in mine if it.get("done"))
        out += [f"### {n:02d} · {s['name']} — {s['when']} ({d}/{len(mine)} done)", "", f"*{s['why']}*", ""]
        out += [f"{k}. {line(it)}" for k, it in enumerate(mine, 1)] + [""]
    left = [items[i] for i in road.get("open", []) if i in items]
    if left:
        out += ["### Still open, off the road until decided", ""] + [f"- {line(it)}" for it in left] + [""]
    for label, key in (("1.x — during the first year", "1.x"), ("Dropped", "drop")):
        sel = sorted((it for it in items.values() if it.get("pick") == key), key=lambda x: x.get("order", 1e9))
        out += [f"## {label} ({len(sel)})", ""]
        for a, name in AREAS:
            s = [it for it in sel if it["area"] == a]
            if s:
                out += [f"### {name}", ""] + [f"- {line(it)}" for it in s] + [""]
    OUT.write_text("\n".join(out))
    print(f"board-release-doc: {OUT.relative_to(HERE)} ({len(out)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
