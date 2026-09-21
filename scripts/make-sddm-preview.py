#!/usr/bin/env python3
"""
Render the KognogOS SDDM theme's preview.png from theme.conf.

The preview is GENERATED, never hand-drawn. A hand-drawn one is a second
copy of the palette, and a second copy of anything is a thing that drifts:
retune a colour in theme.conf and the picture in System Settings quietly
starts advertising the old one. This reads the same file the greeter reads,
so the two cannot disagree.

It is a faithful mock of the layout, not a screenshot of a live greeter --
it draws the same geometry with the same colours, but it does not prove the
QML renders. Run it after any palette change:

    python3 scripts/make-sddm-preview.py

SPDX-FileCopyrightText: 2026 Javier
SPDX-License-Identifier: GPL-3.0-or-later
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

THEME = Path(__file__).resolve().parent.parent / \
    "iso/airootfs/usr/share/sddm/themes/kognogos"
W, H = 1920, 1080


def load_conf(path):
    conf = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            conf[k.strip()] = v.strip()
    return conf


def font(size, bold=False):
    names = (["NotoSans-SemiBold.ttf", "NotoSans-Bold.ttf"] if bold
             else ["NotoSans-Regular.ttf"])
    for n in names:
        for base in ("/usr/share/fonts/noto", "/usr/share/fonts/TTF",
                     "/usr/share/fonts"):
            for p in Path(base).rglob(n):
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size)


def main():
    conf = load_conf(THEME / "theme.conf")
    g = lambda k, d: conf.get(k, d)
    gi = lambda k, d: int(conf.get(k, d))

    img = Image.new("RGB", (W, H), g("background", "#1e1e2e"))

    cw, ch = gi("cardWidth", 880), gi("cardHeight", 400)
    pad, logo_sz = gi("cardPadding", 44), gi("logoSize", 256)
    radius = gi("cardRadius", 4)
    cx, cy = (W - cw) // 2, (H - ch) // 2

    # Shadow: the same stacked-rectangle construction the QML uses, so the
    # preview shows the real falloff rather than a prettier invented one.
    layers = gi("shadowLayers", 14)
    spread = gi("shadowSpread", 48)
    offset = gi("shadowOffset", 14)
    op = float(g("shadowOpacity", "0.055"))
    sc = ImageColorRGB(g("shadowColor", "#11111b"))
    img = img.convert("RGBA")
    for i in range(layers):
        t = (i + 1) / layers
        a = int(255 * op * (1 - t) ** 2)
        if a <= 0:
            continue
        d = t * spread
        # Each layer is composited SEPARATELY. Drawing them all onto one
        # RGBA scratch image does not work: ImageDraw REPLACES pixels
        # rather than blending them, so every larger, fainter ring wiped
        # out the darker one beneath it and the last ring -- alpha 0 by
        # construction -- erased the lot. The first version of this script
        # produced a preview with a measured contrast of exactly zero and
        # still looked plausible. QML Rectangles really do blend, so the
        # greeter was never affected; only this picture of it was.
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle(
            [cx - d, cy - d + offset, cx + cw + d, cy + ch + d + offset],
            radius=radius + d, fill=sc + (a,))
        img = Image.alpha_composite(img, layer)
    img = img.convert("RGB")
    dr = ImageDraw.Draw(img)

    # Card
    dr.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=radius,
                         fill=g("cardColor", "#313244"),
                         outline=g("cardBorderColor", "#cba6f7"),
                         width=gi("cardBorderWidth", 1))

    # Emblem, native size, vertically centred
    logo = Image.open(THEME / g("logo", "assets/logo.png")).convert("RGBA")
    if logo.size != (logo_sz, logo_sz):
        logo = logo.resize((logo_sz, logo_sz), Image.NEAREST)
    img.paste(logo, (cx + pad, cy + (ch - logo_sz) // 2), logo)

    fx = cx + pad + logo_sz + pad
    fw = cw - (fx - cx) - pad
    # Font sizes are the REAL pixel sizes from Main.qml. They were doubled
    # in the first version of this script, on unchanged 1x geometry, which
    # is why the buttons ran into each other -- the preview was lying about
    # the layout it is supposed to be previewing.
    f13, f14, f15 = font(13, True), font(14), font(15)
    card_text = g("cardTextColor", "#cdd6f4")
    field_text = g("fieldTextColor", "#cdd6f4")

    # Form block, vertically centred the way the Column is
    rows_h = 18 + 10 + 44 + 10 + 18 + 10 + 44 + 10 + 20 + 10 + 40
    y = cy + (ch - rows_h) // 2

    for label, value in (("User", "Javier"), ("Password", "\u2022" * 10)):
        dr.text((fx, y), label, font=f13, fill=card_text, anchor="la")
        y += 18 + 10
        dr.rounded_rectangle([fx, y, fx + fw, y + 44], radius=3,
                             fill=g("fieldColor", "#181825"))
        dr.text((fx + 14, y + 22), value, font=f15, fill=field_text,
                anchor="lm")
        if label == "User":
            caret(dr, fx + fw - 14 - 11, y + 22 - 3, field_text)
        y += 44 + 10

    y += 20 + 10

    # Buttons
    bx = fx
    for text, fill, tc in (
            ("Log In", g("accentColor", "#0363ef"), g("accentTextColor", "#ffffff")),
            ("Restart", g("warningColor", "#fab387"), g("warningTextColor", "#11111b")),
            ("Shut Down", g("dangerColor", "#d9400e"), g("dangerTextColor", "#ffffff"))):
        bw = int(dr.textlength(text, font=f13)) + 34
        dr.rounded_rectangle([bx, y, bx + bw, y + 40], radius=3, fill=fill)
        dr.text((bx + bw / 2, y + 20), text, font=f13, fill=tc, anchor="mm")
        bx += bw + 10

    # Session line below the card. The caret is drawn, not typed, for the
    # same reason it is drawn in the QML: Noto Sans has no U+25BE.
    sy = cy + ch + 22 + 13
    dr.text((cx, sy), "Session:", font=f14,
            fill=g("footerTextColor", "#a6adc8"), anchor="lm")
    sx = cx + dr.textlength("Session:", font=f14) + 8
    dr.text((sx, sy), "Plasma (Wayland)", font=f14,
            fill=g("footerTextColor", "#a6adc8"), anchor="lm")
    cw_ = dr.textlength("Plasma (Wayland)", font=f14)
    caret(dr, sx + cw_ + 10, sy - 3, g("footerTextColor", "#a6adc8"))

    out = THEME / "preview.png"
    img.save(out)
    print(f"wrote {out} ({W}x{H})")


def caret(dr, x, y, fill, w=11, h=6):
    """The dropdown triangle, drawn as a polygon.

    Not a character. Noto Sans contains neither U+25BE nor U+25BC, so the
    glyph version renders as a tofu box -- which is exactly what the first
    version of this preview showed, and exactly what the greeter itself
    would have shown on any machine with two sessions installed.
    """
    dr.polygon([(x, y), (x + w, y), (x + w / 2, y + h)], fill=fill)


def ImageColorRGB(hexstr):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    sys.exit(main())
