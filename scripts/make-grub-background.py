#!/usr/bin/env python3
"""Generate the KognogOS GRUB background.

Layout borrowed from the windows-11 GRUB theme Javier likes — dark body,
angled band across the top, mark upper-left — wearing KognogOS's own
identity: the logo's blue and ember sweeping through the band, Catppuccin
Mocha beneath, the icon that also fronts the Plymouth splash.

Run:  python scripts/make-grub-background.py [output.png]
Then: sudo cp <output> /boot/grub/themes/kognogos/background.png
      sudo grub-mkconfig -o /boot/grub/grub.cfg
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BODY = (30, 30, 46)        # Catppuccin base   #1e1e2e
CRUST = (17, 17, 27)       # Catppuccin crust  #11111b
BLUE = (3, 99, 239)        # logo blue         #0363ef
EMBER = (217, 64, 14)      # logo ember        #d9400e
TEXT = (205, 214, 244)     # Catppuccin text   #cdd6f4
MUTED = (127, 132, 156)    # Catppuccin overlay0

REPO = Path(__file__).resolve().parents[1]
LOGO = REPO / "iso/airootfs/usr/share/plymouth/themes/kognog/logo.png"
FONT = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-{}.ttf"

BAND_LEFT, BAND_RIGHT = 260, 45     # band height at each edge
LOGO_H, LOGO_X, LOGO_Y = 190, 100, 32


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def band_colour(t):
    """crust → blue (40%) → ember (78%) → crust, left to right."""
    if t < 0.40:
        return lerp(CRUST, BLUE, t / 0.40)
    if t < 0.78:
        return lerp(BLUE, EMBER, (t - 0.40) / 0.38)
    return lerp(EMBER, CRUST, (t - 0.78) / 0.22)


img = Image.new("RGB", (W, H), BODY)
draw = ImageDraw.Draw(img)

for x in range(W):
    t = x / (W - 1)
    edge = round(BAND_LEFT + (BAND_RIGHT - BAND_LEFT) * t)
    draw.line([(x, 0), (x, edge)], fill=band_colour(t))

# Ember seam — the line that reads as intentional rather than accidental.
draw.line([(0, BAND_LEFT), (W - 1, BAND_RIGHT)], fill=EMBER, width=2)

logo = Image.open(LOGO).convert("RGBA")
logo = logo.resize((round(logo.width * LOGO_H / logo.height), LOGO_H), Image.LANCZOS)
img.paste(logo, (LOGO_X, LOGO_Y), logo)

# Field note (2026-08-11): theme.txt puts the countdown label at top=31%
# (y=335) and the boot menu at top=40% (y=432). The title has to live in
# the clear band between the logo (ends y=222) and that countdown, so it
# is anchored at y=250 — 30px tall, clearing 335 with room to spare.
# Indented past the logo's left edge on Javier's eye, not a rule.
TITLE_X, TITLE_Y = 160, 250

big = ImageFont.truetype(FONT.format("Bold"), 30)
small = ImageFont.truetype(FONT.format("Regular"), 20)
draw.text((TITLE_X, TITLE_Y), "Choose an operating system to start", font=big, fill=TEXT)

help_text = ("Use the up and down keys to select which entry is highlighted.  "
             "Enter boots it,  'e' edits its commands,  'c' opens a command line.")
w = draw.textbbox((0, 0), help_text, font=small)[2]
draw.text(((W - w) / 2, 1020), help_text, font=small, fill=MUTED)

out = sys.argv[1] if len(sys.argv) > 1 else "kognogos-grub-bg.png"
img.save(out)
print("wrote", out, img.size)
