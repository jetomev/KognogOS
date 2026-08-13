#!/usr/bin/env python3
"""
Render the KognogOS emblem to an ANSI art panel for the shell greeting.

Run once, at authoring time -- the greeting reads the resulting text file
and prints it, so no image library and no rendering cost land in the path
of every terminal launch:

    python3 scripts/make-emblem-ansi.py

Half-block technique: each text row carries TWO pixel rows, drawn as U+2580
(upper half block) with the top pixel as foreground and the bottom pixel as
background. Because half a cell is roughly square, a square logo needs
COLS = ROWS * 2 -- getting that wrong is what makes terminal logos look
vertically stretched.

Transparent pixels emit the terminal's DEFAULT background (SGR 49) rather
than a hardcoded colour, so the panel sits on whatever theme the user runs
instead of painting a subtly-wrong box behind itself. KognogOS's own
Alacritty theme uses #1a1a1a, Catppuccin Mocha uses #1e1e2e -- close
enough to look identical if you hardcode either one, and wrong on both if
you pick the other.

SPDX-FileCopyrightText: 2026 Javier
SPDX-License-Identifier: GPL-3.0-or-later
"""

import pathlib
import sys

from PIL import Image

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "assets/icons/kognogos.png"
OUT = REPO / "assets/icons/kognogos.ansi"

ROWS = 8
COLS = ROWS * 2          # square on screen; see the note above
ALPHA_CUTOFF = 128       # below this a pixel is background, not emblem

UPPER, LOWER, FULL = "▀", "▄", "█"
RESET = "\x1b[0m"


def fg(rgb):
    return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def bg(rgb):
    return f"\x1b[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def render(src=SRC, rows=ROWS, cols=COLS):
    img = Image.open(src).convert("RGBA").resize((cols, rows * 2), Image.LANCZOS)
    px = img.load()

    lines = []
    for row in range(rows):
        out = []
        for col in range(cols):
            tr, tg, tb, ta = px[col, row * 2]
            br, bgr, bb, ba = px[col, row * 2 + 1]
            top, bot = ta >= ALPHA_CUTOFF, ba >= ALPHA_CUTOFF

            if top and bot:
                out.append(fg((tr, tg, tb)) + bg((br, bgr, bb)) + UPPER)
            elif top:
                out.append("\x1b[49m" + fg((tr, tg, tb)) + UPPER)
            elif bot:
                out.append("\x1b[49m" + fg((br, bgr, bb)) + LOWER)
            else:
                out.append("\x1b[49m ")
        lines.append("".join(out) + RESET)
    return lines


def main():
    if not SRC.exists():
        print(f"missing emblem source: {SRC}", file=sys.stderr)
        return 1
    lines = render()
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT}  ({ROWS} rows x {COLS} cols, {OUT.stat().st_size} bytes)")
    print()
    for line in lines:
        print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
