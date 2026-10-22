# The KognogOS board

**Live:** https://claude.ai/artifact/6UswcvpQ4EnWek5iVtBy5G — every pending item for KognogOS, judged
(v1.0 · 1.x · Drop · Not sure) and laid out as **the road to launch** (14 stages to the week of 19 April
2027). Javier, 2026-10-22: *"this page is what I want to see… as we work, we can update it taking out
stuff, and adding whatever we need like issues, missing things, new, changes. It is very visual."*

| File | What it is |
|---|---|
| `kognogos-cut.html` | the page itself — published from here to the same link (Artifact `url`) |
| `state.json` | the board's snapshot: every item, its pick, note and done mark, and the road. What `scripts/status.sh` shows; git keeps its history |
| `road.json` | the road as first written (2026-10-21); the live one is the board's `road/plan` document |
| `seed-items.py` | how the first 207 items were gathered (every TODO + open issues + 40 new gaps) |

**How it stays current:** the board's database is the live record (items: `items/<id>`, the road:
`road/plan`). Claude changes it with ArtifactData — new items, done marks, stages — then exports it
(`list` + `get` with `out_dir`) and runs `scripts/board-snapshot.py <export>`; the snapshot is committed.
`mindforge active ~/Programs/kognog` (and the brief) prints `scripts/status.sh`, whose first line says to
open the board beside the chat.

## Linked to its projects (2026-10-22)

The cut copied pending lines from nog, the Forge Suite and the other apps; the copies drifted (nogForge #17–#20 shipped on 10-07 and were still on the cut). Now:

- `links.json` — each item's twin: `steps` (`<project>:<step id>`, mindForge board.py ids), `issues` (`owner/repo#n`), or `own` / `unclear`.
- `scripts/board-links.py check [<export>] [--plan F]` — what is done in its project but open here, ticked here but open there, broken links (a TODO line reworded), unclear ones. Runs in `scripts/status.sh`.
- `scripts/board-links.py badges <dir>` — the badge each project board shows on its linked steps.
- The page reads `links/all` (project name + board address per item) and shows a clickable project tag.
