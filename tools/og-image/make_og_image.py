#!/usr/bin/env python3
"""Draw the link preview image (Discord, Slack, social embeds) for Mine avganger.

It shows a departure board in the dashboard's dark theme with made-up lines and
destinations, next to the Oslo S clock tower photo. Everything is fixed in this
file, so running it again gives the same image.

    python3 tools/og-image/make_og_image.py            # writes IMGs/og-image.png
    python3 tools/og-image/make_og_image.py out.png    # writes somewhere else

Needs Pillow (pip install Pillow). The Barlow Semi Condensed fonts next to this
script are the ones the page uses, under the SIL Open Font License (fonts/OFL.txt).
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PHOTO = ROOT / "IMGs" / "clock-tower.jpg"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "IMGs" / "og-image.png"

# ---------- content ----------
BOARD_TITLE = "Mine Avganger"
BOARD_SUB = "Sanntid for tog, T-bane, trikk og buss"
FOOTER = "Sanntid fra Entur, oppdatert 10:42"
CLOCK = "10:42"

# Mode colours match MODES in index.html. Regional buses have no mode of their own
# there, so they use the express bus green.
MODES = {
    "bus": "#d40d0d",
    "tram": "#0b78c8",
    "metro": "#d9640a",
    "rail": "#00824a",
    "regional": "#5a7d00",
}

# (line, mode, name, platform, time, status). The name is the transport type. A time of "Nå" gets
# the yellow highlight, as on the page. Status is one of:
#   None                      on time
#   ("late", "10:47")         delayed: "Rute 10:47" under the time, in the delay colour
#   ("cancelled", "10:52")    cancelled: "Innstilt" in red, the planned time struck through,
#                             and the name struck through and dimmed
ROWS = [
    ("XX", "bus", "Buss", "A", "Nå", None),
    ("XX", "tram", "Trikk", "B", "3 min", None),
    ("X", "metro", "T-bane", "2", "7 min", ("late", "10:47")),
    ("RE", "rail", "Tog", "4", "Innstilt", ("cancelled", "10:52")),
    ("XXX", "regional", "Regionsbuss", "C", "11:05", None),
]

# ---------- design (the dark theme from index.html) ----------
W, H = 1200, 630
S = 2  # draw at 2x and scale down, for smooth edges
BG = "#0a1424"
PANEL = "#12223a"
BAND = "#1c3355"
INK = "#eef2f7"
MUTED = "#97a6ba"
RULE = "#22364f"
NOW = "#ffd23f"
NOW_INK = "#0e1a2b"
LATE = "#fbbf24"
DANGER = "#ff6b7d"


def font(weight, size):
    return ImageFont.truetype(str(HERE / "fonts" / f"BarlowSemiCondensed-{weight}.ttf"), size * S)


def px(value):
    return round(value * S)


def hex_rgb(colour):
    colour = colour.lstrip("#")
    return tuple(int(colour[i:i + 2], 16) for i in (0, 2, 4))


def photo_layer():
    """The clock tower on the right, fading into the background towards the left."""
    layer = Image.new("RGB", (px(W), px(H)), BG)
    photo = Image.open(PHOTO).convert("RGB")
    height = px(H * 1.55)  # crop in on the clock faces and the top of the tower
    width = round(photo.width * height / photo.height)
    photo = photo.resize((width, height), Image.LANCZOS)
    left = px(W) - width + px(40)
    top = -px(H * 0.18)
    layer.paste(photo, (left, top))

    # Fade: solid background up to 52 % of the width, then the photo shows through.
    fade = Image.new("L", (px(W), 1))
    for x in range(px(W)):
        t = x / px(W)
        fade.putpixel((x, 0), 255 if t < 0.52 else round(255 * max(0.0, 1 - (t - 0.52) / 0.33) ** 1.4))
    fade = fade.resize((px(W), px(H)))
    background = Image.new("RGB", (px(W), px(H)), BG)
    return Image.composite(background, layer, fade)


def text_right(draw, x_right, y, text, fnt, fill):
    draw.text((x_right - draw.textlength(text, font=fnt), y), text, font=fnt, fill=fill)


def text_center(draw, x_center, y, text, fnt, fill):
    draw.text((x_center - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def blend(colour, background, opacity):
    """A colour at the given opacity over a background, like CSS opacity on the page."""
    a, b = hex_rgb(colour), hex_rgb(background)
    return tuple(round(x * opacity + y * (1 - opacity)) for x, y in zip(a, b))


def strike(draw, x, y, text, fnt, fill):
    """A line through text drawn at (x, y), at roughly the middle of lower-case letters."""
    left, top, right, bottom = draw.textbbox((x, y), text, font=fnt)
    mid = top + (bottom - top) * 0.55
    draw.line((left, mid, right, mid), fill=fill, width=px(1.5))


def main():
    image = photo_layer()
    draw = ImageDraw.Draw(image)

    # Board panel
    x0, y0, x1 = 56, 56, 656
    band_h, cols_h, row_h, footer_h = 92, 40, 70, 46
    y1 = y0 + band_h + cols_h + row_h * len(ROWS) + footer_h
    draw.rounded_rectangle((px(x0), px(y0), px(x1), px(y1)), radius=px(10), fill=PANEL)
    # Band: rounded top, square bottom
    draw.rounded_rectangle((px(x0), px(y0), px(x1), px(y0 + band_h)), radius=px(10), fill=BAND)
    draw.rectangle((px(x0), px(y0 + band_h - 12), px(x1), px(y0 + band_h)), fill=BAND)
    draw.text((px(x0 + 26), px(y0 + 14)), BOARD_TITLE, font=font("Bold", 40), fill="#ffffff")
    draw.text((px(x0 + 26), px(y0 + 60)), BOARD_SUB, font=font("Regular", 19), fill="#c9d3e0")

    # Column positions, as in the page's grid: line, destination, platform, time
    pad = 26
    c_line = x0 + pad
    c_dest = c_line + 74
    c_plat = x1 - pad - 112 - 18
    c_time = x1 - pad

    y = y0 + band_h
    small = font("Medium", 16)
    draw.text((px(c_line), px(y + 12)), "Linje", font=small, fill=MUTED)
    draw.text((px(c_dest), px(y + 12)), "Til", font=small, fill=MUTED)
    text_center(draw, px(c_plat), px(y + 12), "Spor", small, MUTED)
    text_right(draw, px(c_time), px(y + 12), "Avgang", small, MUTED)
    y += cols_h
    draw.line((px(x0), px(y), px(x1), px(y)), fill=RULE, width=px(1))

    badge_font = font("Bold", 21)
    dest_font = font("Medium", 26)
    plat_font = font("SemiBold", 25)
    time_font = font("Bold", 26)
    note_font = font("Regular", 16)
    for i, (line, mode, dest, plat, when, status) in enumerate(ROWS):
        kind, planned = status or (None, None)
        mid = y + row_h / 2
        # Line badge
        badge_w = max(62, draw.textlength(line, font=badge_font) / S + 18)
        draw.rounded_rectangle((px(c_line), px(mid - 17), px(c_line + badge_w), px(mid + 17)),
                               radius=px(5), fill=MODES[mode])
        text_center(draw, px(c_line + badge_w / 2), px(mid - 14), line, badge_font, "#ffffff")
        # Name, struck through and dimmed when cancelled, and platform
        if kind == "cancelled":
            dim = blend(INK, PANEL, 0.6)
            draw.text((px(c_dest), px(mid - 17)), dest, font=dest_font, fill=dim)
            strike(draw, px(c_dest), px(mid - 17), dest, dest_font, dim)
        else:
            draw.text((px(c_dest), px(mid - 17)), dest, font=dest_font, fill=INK)
        text_center(draw, px(c_plat), px(mid - 17), plat, plat_font, INK)
        # Departure time: the "Nå" highlight, a delay note, or cancelled
        time_y = mid - (25 if kind else 17)
        if kind == "cancelled":
            text_right(draw, px(c_time), px(time_y), when, time_font, DANGER)
            note_x = px(c_time) - draw.textlength(planned, font=note_font)
            draw.text((note_x, px(mid + 6)), planned, font=note_font, fill=MUTED)
            strike(draw, note_x, px(mid + 6), planned, note_font, MUTED)
        elif when == "Nå":
            w = draw.textlength(when, font=time_font) / S
            draw.rounded_rectangle((px(c_time - w - 18), px(mid - 18), px(c_time), px(mid + 18)),
                                   radius=px(5), fill=NOW)
            text_right(draw, px(c_time - 9), px(time_y), when, time_font, NOW_INK)
        else:
            text_right(draw, px(c_time), px(time_y), when, time_font, INK)
        if kind == "late":
            text_right(draw, px(c_time), px(mid + 6), "Rute " + planned, note_font, LATE)
        y += row_h
        if i < len(ROWS) - 1:
            draw.line((px(x0 + pad), px(y), px(x1 - pad), px(y)), fill=RULE, width=px(1))

    draw.line((px(x0), px(y), px(x1), px(y)), fill=RULE, width=px(1))
    draw.text((px(x0 + pad), px(y + 13)), FOOTER, font=font("Regular", 16), fill=MUTED)

    # Big clock, bottom right over the photo, like the dashboard header
    clock_font = font("SemiBold", 84)
    text_right(draw, px(W - 56), px(H - 56 - 92), CLOCK, clock_font, "#ffffff")

    out = image.resize((W, H), Image.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)
    print(f"Wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
