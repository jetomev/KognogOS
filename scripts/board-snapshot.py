#!/usr/bin/env python3
"""The KognogOS board's snapshot (2026-10-22): the board itself lives in an Artifact's database
(https://claude.ai/artifact/6UswcvpQ4EnWek5iVtBy5G); a terminal can't read it, so after every change
Claude exports it (ArtifactData list, out_dir) and this folds the export into docs/board/state.json —
what scripts/status.sh shows, and what git keeps as the history of the road.

    board-snapshot.py <export-dir>      the folder ArtifactData wrote (holds items/ and road/)
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
STATE = HERE / "docs/board/state.json"


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    items = {}
    for f in sorted((src / "items").glob("*.json")):
        d = json.loads(f.read_text())
        items[f.stem] = d.get("data", d)
    road_file = src / "road/plan.json"
    road = json.loads(road_file.read_text()) if road_file.exists() else None
    road = road.get("data", road) if road else None
    if not items or not road:
        sys.exit(f"board-snapshot: {src} has {len(items)} items and {'a' if road else 'no'} road — nothing written")
    keep = ("area", "title", "detail", "source", "suggest", "pick", "note", "new", "done", "doneAt", "order")
    state = {"taken": time.strftime("%Y-%m-%d %H:%M"), "board": "https://claude.ai/artifact/6UswcvpQ4EnWek5iVtBy5G",
             "road": road, "items": {k: {f: v[f] for f in keep if f in v} for k, v in sorted(items.items())}}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n")
    on_road = [i for s in road["stages"] for i in s["items"]]
    done = sum(1 for i in on_road if items.get(i, {}).get("done"))
    print(f"board-snapshot: {len(items)} items, {len(on_road)} on the road, {done} done → {STATE.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
