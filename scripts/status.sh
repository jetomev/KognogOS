#!/usr/bin/env bash
# KognogOS's short status (2026-10-22), printed by `mindforge active` and the brief when this project is
# called. Javier: "this page is what I want to see, which opens on the side of the chat area" — so the
# first lines say to open the board, and the rest is the road from the board's snapshot.
cd "$(dirname "$0")/.." || exit 1
python3 - <<'PY'
import json, subprocess
from pathlib import Path

state = json.loads(Path("docs/board/state.json").read_text())
road, items = state["road"], state["items"]
head = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
ahead = subprocess.run(["git", "rev-list", "--count", "@{u}..HEAD"], capture_output=True, text=True).stdout.strip()

stages = road["stages"]
on_road = [i for s in stages for i in s["items"] if i in items]
done = sum(1 for i in on_road if items[i].get("done"))
now = next((n for n, s in enumerate(stages) if any(not items[i].get("done") for i in s["items"] if i in items)), None)

print("\n╭─ KognogOS · the road to v1.0 — the week of 19 April 2027")
print(f"│  BOARD — open it beside the chat FIRST (Artifact open): {state['board']}")
print(f"│  {done} of {len(on_road)} steps done · snapshot {state['taken']} (the board is live; refresh: ArtifactData list → scripts/board-snapshot.py)")
print(f"│  {head}" + ("  ⚠ uncommitted changes" if dirty else "  ✓ clean") + (f" · {ahead} unpushed" if ahead not in ("", "0") else ""))
print("╰─" + "─" * 60)
for n, s in enumerate(stages):
    mine = [items[i] for i in s["items"] if i in items]
    d = sum(1 for it in mine if it.get("done"))
    mark = "✅" if mine and d == len(mine) else ("🔄" if d or n == now else "⬜")
    print(f"  {mark} {n:02d} · {s['name']:<40} {d}/{len(mine):<3} {s['when']}")
if now is not None:
    s = stages[now]
    todo = [items[i] for i in s["items"] if i in items and not items[i].get("done")]
    print(f"\n  NOW — stage {now:02d} · {s['name']}")
    for it in todo[:6]:
        tag = "  [answer this]" if not it.get("pick") else ""
        print(f"    □ {it['title'][:96]}{tag}")
    if len(todo) > 6:
        print(f"    … {len(todo) - 6} more in this stage")
open_q = [items[i]["title"] for i in road.get("open", []) if i in items]
if open_q:
    print(f"\n  STILL OPEN (off the road until decided): {len(open_q)}")
PY
# The board's links to the projects it is made of (2026-10-22): an item done in its project but open on the
# board, or the other way round, shows here every time KognogOS is called — drift is seen, not discovered.
links=$(timeout 30 python3 scripts/board-links.py check 2>&1); rc=$?
if [ "$rc" -eq 0 ]; then
  printf '\n  LINKS ✓ %s\n' "$(head -1 <<<"$links" | sed 's/^KognogOS board ↔ its projects: //')"
else
  printf '\n  LINKS ⚠ the board and its projects disagree — bring the board in step (scripts/board-links.py check <export> --plan F):\n'
  tail -n +2 <<<"$links" | sed 's/^/  /'
fi
