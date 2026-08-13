#!/usr/bin/env python3
"""
KognogOS shell greeting.

Prints the emblem, a single-column system table, and an update status line.

Three rules shape this file:

  * One column, and it degrades. This is opened in whatever window the
    user happens to have, so the layout adapts: the emblem is dropped when
    the table would no longer fit beside it, long sentences wrap under
    themselves rather than back to the left margin, and the URL is never
    broken because a split URL stops being clickable.

  * It runs in front of EVERY prompt, so it may not do slow work. It used
    to call `checkupdates`, which syncs a package database over the
    network -- about 1.2s of the 1.5s this took. That job now belongs to
    kognog-updates.timer, and the greeting just reads the JSON snapshot it
    leaves in ~/.cache/kognog/updates.json. Everything else comes from
    /proc, /etc and two cheap subprocesses.

  * Nothing here may raise. A greeting that throws is a shell that looks
    broken, so every probe falls back to "N/A" and a missing snapshot is
    reported as unknown rather than assumed healthy.

The emblem is pre-rendered ANSI (scripts/make-emblem-ansi.py), not an
image decoded at launch.

SPDX-FileCopyrightText: 2026 Javier
SPDX-License-Identifier: GPL-3.0-or-later
"""

import getpass
import json
import math
import os
import pathlib
import subprocess
import textwrap
import time

from rich.console import Console
from rich.text import Text

console = Console()

# ── palette ───────────────────────────────────────────────────────────────────
LABEL   = "#89b4fa"
VALUE   = "#cdd6f4"
MUTED   = "#a6adc8"
FAINT   = "#585b70"
TRACK   = "#313244"
GREEN   = "#a6e3a1"
YELLOW  = "#f9e2af"
RED     = "#f38ba8"
PINK    = "#f5c2e7"
WHITE   = "#ffffff"

# ── geometry ──────────────────────────────────────────────────────────────────
# The emblem panel is 16 cells wide because a square logo drawn in half
# blocks needs cols = rows * 2 (see make-emblem-ansi.py).
EMBLEM   = pathlib.Path("/usr/share/kognog/kognogos.ansi")
EMBLEM_W = 16
GAP      = 2

# One column, not two. A second column only fits on a wide terminal, and
# the greeting has to stay readable wherever it is opened -- a narrow
# window used to fold the right-hand column back under the left.
LABEL_W  = 9
METRIC_W = 12      # value cell for the metered rows, so the bars line up
INFO_W   = 26      # hard cap for the descriptive values
BAR_W    = 18
CONTENT  = 74      # divider length

SUBTITLE = "SEMI-ROLLING, ARCH BASED, TIER-AWARE"

# The narrowest table that still shows a full CPU model and an unbroken
# subtitle. The emblem is only drawn when this much room survives beside
# it -- otherwise it is taking columns the content needs, and the values
# start folding back to the left margin.
MIN_CONTENT = max(LABEL_W + INFO_W, len(SUBTITLE))

SNAPSHOT = pathlib.Path(
    os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
) / "kognog/updates.json"

URL = "https://github.com/jetomev/KognogOS"


# ── probes ────────────────────────────────────────────────────────────────────

def run(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=3,
                             env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"})
        return out.stdout.strip()
    except Exception:
        return ""


def read(path, default=""):
    try:
        return pathlib.Path(path).read_text()
    except OSError:
        return default


def os_release():
    """NAME + VERSION from os-release, e.g. 'KognogOS v0.9.0-beta'."""
    fields = {}
    for line in read("/etc/os-release").splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            fields[k.strip()] = v.strip().strip('"')
    name = fields.get("NAME") or "Linux"
    ver = fields.get("VERSION") or fields.get("VERSION_ID")
    return f"{name} v{ver}" if ver else name


def desktop():
    de = os.environ.get("XDG_CURRENT_DESKTOP", "").split(":")[0] or "N/A"
    if de.upper() == "KDE":
        # plasmashell --version would spawn a Qt process; the package
        # version is the same number for free.
        ver = run(["pacman", "-Q", "plasma-workspace"]).split()
        return f"KDE Plasma {ver[1].split('-')[0]}" if len(ver) > 1 else "KDE Plasma"
    return de


def cpu_model():
    for line in read("/proc/cpuinfo").splitlines():
        if line.startswith("model name"):
            name = line.split(":", 1)[1].strip()
            for junk in ("(R)", "(TM)"):
                name = name.replace(junk, "")
            for cut in (" with ", " Processor"):
                name = name.split(cut)[0]
            return name.strip()
    return "N/A"


def gpu_model():
    for line in run(["lspci"]).splitlines():
        low = line.lower()
        if "vga" in low or "3d controller" in low:
            name = line.split("[", 1)[-1].split("]")[0] if "[" in line else line
            # Marketing suffixes that describe the SKU, not the hardware.
            for junk in (" Lite Hash Rate", " LHR", " OEM"):
                name = name.replace(junk, "")
            return name.strip()
    return "N/A"


def uptime():
    """Compact enough to live in a 12-column cell: '5d 3h', '2h 41m', '7m'."""
    try:
        secs = int(float(read("/proc/uptime", "0").split()[0]))
    except (ValueError, IndexError):
        return "N/A"
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m = rem // 60
    if d:
        return f"{d}d {h}h"
    if h:
        return f"{h}h {m}m"
    return f"{m}m"


def human(kib, ceil=False):
    """KiB -> the units `free -h` and `df -h` print.

    They disagree on rounding: df rounds UP (741G for 740.1), free rounds
    to nearest (31Gi for 31.04). Matching each one keeps the greeting from
    quietly contradicting the command the user would check it against.
    """
    v = float(kib)
    for unit in ("Ki", "Mi", "Gi", "Ti"):
        if v < 1024 or unit == "Ti":
            if v >= 10:
                return f"{math.ceil(v) if ceil else round(v)}{unit}"
            tenths = math.ceil(v * 10) if ceil else round(v * 10)
            return f"{tenths / 10:.1f}{unit}"
        v /= 1024
    return f"{round(v)}Ti"


def memory():
    info = {}
    for line in read("/proc/meminfo").splitlines():
        k, _, v = line.partition(":")
        info[k] = int(v.split()[0]) if v.split() else 0
    total = info.get("MemTotal", 0)
    if not total:
        return "N/A", 0
    # What `free` calls "used" is total - available. NOT
    # total - free - buffers - cache: that undercounts by ~0.5Gi here,
    # because MemAvailable also discounts cache the kernel cannot actually
    # reclaim. Older kernels without MemAvailable fall back to the
    # subtraction.
    if "MemAvailable" in info:
        used = total - info["MemAvailable"]
    else:
        cache = info.get("Cached", 0) + info.get("SReclaimable", 0)
        used = total - info.get("MemFree", 0) - info.get("Buffers", 0) - cache
    return f"{human(used)}/{human(total)}", round(used * 100 / total)


def disk(path="/"):
    try:
        st = os.statvfs(path)
    except OSError:
        return "N/A", 0
    unit = st.f_frsize / 1024
    total = st.f_blocks * unit
    used = (st.f_blocks - st.f_bfree) * unit
    if not total:
        return "N/A", 0
    # df's percentage ignores root-reserved blocks, so it is used/(used+avail).
    avail = st.f_bavail * unit
    pct = round(used * 100 / (used + avail)) if used + avail else 0
    return f"{human(used, ceil=True).rstrip('i')}/{human(total, ceil=True).rstrip('i')}", pct


def cpu_percent():
    """Busy share since boot -- cheap, and honest about being an average."""
    for line in read("/proc/stat").splitlines():
        if line.startswith("cpu "):
            # [1:5] is user, nice, system, idle. Busy is user + system --
            # including idle here reads as a permanent 100%.
            user, nice, system, idle = (int(x) for x in line.split()[1:5])
            total = user + nice + system + idle
            return round((user + system) * 100 / total) if total else 0
    return 0


def snapshot():
    try:
        return json.loads(SNAPSHOT.read_text())
    except (OSError, ValueError):
        return None


# ── rendering ─────────────────────────────────────────────────────────────────

def bar(pct, width):
    filled = round(pct * width / 100)
    color = GREEN if pct < 60 else YELLOW if pct < 85 else RED
    b = Text()
    b.append("|" * filled, style=color)
    b.append("." * (width - filled), style=TRACK)
    return b


def clamp(value, width):
    """Hard cap, because '{:<n}' is a MINIMUM -- an over-long value used to
    shove the whole right-hand column sideways."""
    value = value or "N/A"
    return value if len(value) <= width else value[: width - 1] + "…"


def status_line(snap):
    """Colour comes from the snapshot's level; see update-check for the rule."""
    if snap is None:
        return (FAINT, "Update status unknown — is kognog-updates.timer enabled?", "")

    level, count = snap.get("level"), snap.get("count", 0)
    stale = snap.get("stale") or []

    if level == "green":
        text = "System and packages are up to date!"
    elif level == "red":
        text = ('System and package update is highly encouraged. '
                'Please run "nog update" for more info.')
    else:
        text = ('System and package updates are available. '
                'Please run "nog update" for more info.')

    # Detail goes on its own line rather than being appended: the headline
    # already runs to ~85 columns, and appending to it wrapped the sentence
    # back to column 0.
    detail = []
    if count:
        detail.append(f"{count} pending")
    if stale:
        worst = stale[0]
        detail.append(f"oldest {worst['pkg']} {worst['age']}d (tier {worst['tier']})")
    # A snapshot the timer stopped refreshing must not read as fresh news.
    age_h = (time.time() - snap.get("generated", 0)) / 3600
    if age_h > 24:
        detail.append(f"checked {int(age_h // 24)}d ago")

    return ({"green": GREEN, "red": RED}.get(level, YELLOW), text,
            "  ·  ".join(detail))


def main():
    width = console.width

    # The emblem is only worth its 18 columns if what remains still holds a
    # readable table; below that the table wins and the emblem is dropped.
    emblem = []
    indent = 0
    if width >= EMBLEM_W + GAP + MIN_CONTENT:
        emblem = read(EMBLEM).splitlines()
        indent = EMBLEM_W + GAP

    content_w = max(MIN_CONTENT, min(CONTENT, width - indent))
    bar_w = max(6, min(BAR_W, content_w - LABEL_W - METRIC_W))
    info_w = max(8, min(INFO_W, content_w - LABEL_W))

    mem_txt, mem_pct = memory()
    dsk_txt, dsk_pct = disk()
    cpu_pct = cpu_percent()

    # What the machine IS, then how it is DOING. The third field is the
    # meter percentage (None draws no bar); the fourth marks the readings
    # block, whose values share a fixed cell so the bars line up -- Uptime
    # belongs to it despite having nothing to meter.
    rows = [
        ("OS",      os_release(),       None,     False),
        ("Kernel",  os.uname().release, None,     False),
        ("Desktop", desktop(),          None,     False),
        ("CPU",     cpu_model(),        None,     False),
        ("GPU",     gpu_model(),        None,     False),
        ("CPU",     f"{cpu_pct}%",      cpu_pct,  True),
        ("Memory",  mem_txt,            mem_pct,  True),
        ("Disk",    dsk_txt,            dsk_pct,  True),
        ("Uptime",  uptime(),           None,     True),
    ]

    title = Text()
    title.append("\U000F0DBC", style=f"bold {WHITE}")      # md-chevron_triple_up
    title.append("KognogOS", style=f"bold {VALUE}")

    block = [title,
             Text(SUBTITLE, style=FAINT),
             Text("─" * content_w, style=LABEL)]

    for label, value, pct, is_reading in rows:
        line = Text()
        line.append(f"{label:<{LABEL_W}}", style=LABEL)
        if is_reading:
            line.append(f"{clamp(value, METRIC_W):<{METRIC_W}}", style=MUTED)
            if pct is not None:
                line.append_text(bar(pct, bar_w))
        else:
            # Nothing sits to the right of these, so they need clamping
            # but no padding.
            line.append(clamp(value, info_w), style=VALUE)
        block.append(line)

    block.append(Text("─" * content_w, style=TRACK))

    console.print()
    for i, line in enumerate(block):
        row = Text()
        if emblem:
            row.append_text(Text.from_ansi(emblem[i]) if i < len(emblem)
                            else Text(" " * EMBLEM_W))
            row.append(" " * GAP)
        row.append_text(line)
        console.print(row, no_wrap=True, overflow="ellipsis")

    # Two spaces, NOT the emblem's indent: these lines are wider than the
    # table and indenting them to match it pushed the sentence off the
    # right edge. Sitting at the margin also reads as "below the table",
    # which is where they belong.
    pad = "  "
    # Four columns: past the two-space margin and past the "● ". Everything
    # under the headline hangs from the headline's own text, so the block
    # reads as one paragraph.
    sub = pad + "  "

    color, text, detail = status_line(snapshot())

    # Wrapped by hand rather than left to the console: rich would fold the
    # continuation back to column 0, which breaks the sentence apart on a
    # narrow terminal.
    lines = textwrap.wrap(text, width=max(20, width - len(sub))) or [text]

    status = Text(f"\n{pad}")
    status.append("● ", style=color)
    status.append(lines[0], style=VALUE)
    console.print(status)
    for extra in lines[1:]:
        console.print(Text(sub + extra, style=VALUE))

    if detail:
        for chunk in textwrap.wrap(detail, width=max(20, width - len(sub))):
            console.print(Text(sub + chunk, style=FAINT))

    # The URL is never allowed to wrap: a split URL stops being clickable,
    # and rich would fold it to column 0. If the sentence and the address
    # do not share a line, the address gets its own.
    prompt = "For more info or help please visit:"
    if len(sub) + len(prompt) + 1 + len(URL) <= width:
        link = Text(sub)
        link.append(prompt + " ", style=FAINT)
        link.append(URL, style=f"{LABEL} underline link {URL}")
        console.print(link)
    else:
        console.print(Text(sub + prompt, style=FAINT))
        console.print(Text(sub, style=FAINT).append(
            URL, style=f"{LABEL} underline link {URL}"), overflow="ignore",
            crop=False)

    welcome = Text(f"\n{pad}")
    welcome.append("Welcome ", style=GREEN)
    welcome.append(getpass.getuser(), style=f"bold {PINK}")
    welcome.append(", let's rock this session! 🧙\n", style=GREEN)
    console.print(welcome)


if __name__ == "__main__":
    main()
