#!/usr/bin/env python3
"""Compose the travel poster — SOLMARA (final).

The poster is painted the way the classic railway and shipping-line
posters were: one landmark, one promise of light and weather, and
the place's name set into the picture — and no other copy at all.

SOLMARA — a sunset bay that does not exist. In the foreground a
striped umbrella and two deck chairs on warm golden sand, one
chair taken by a traveller seen from behind, watching the sun go
down. The sea carries a path of light to the horizon, and the
beach curves away to a headland of layered green hills. The whole
scene is printed like a vintage silkscreen: flat inks, halftone
grain, aged paper.

This program finishes the painting into the entry: it downscales
the artwork to the bounty's 1024x1024, sets the place's name
across the sky in Playfair Display with wide letterspacing
(the font is SIL Open Font License 1.1, see assets/OFL.txt), and
writes a PNG under the 1 MiB cap via a 256-colour adaptive palette
with Floyd–Steinberg dithering.

Deterministic: no clock, no network, no randomness.
Environment overrides (used while proofing the design):
  POSTER_ART, POSTER_NAME, POSTER_STYLE ("ink" | "cream" | "rust"),
  POSTER_OUT.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MAX_BYTES = 1_048_576

ART = os.environ.get("POSTER_ART", os.path.join(HERE, "assets", "solmara-final.png"))
NAME = os.environ.get("POSTER_NAME", "SOLMARA")
STYLE = os.environ.get("POSTER_STYLE", "ink")
OUT = os.environ.get("POSTER_OUT", os.path.join(HERE, "entry.png"))
FONT_PATH = os.path.join(HERE, "assets", "PlayfairDisplay.ttf")

INK = (18, 58, 71)        # deep teal ink for a light sky
CREAM = (250, 243, 224)   # warm cream for a darker canopy
SHADOW = (10, 38, 48)     # teal shadow under cream letters
RUST = (150, 62, 40)      # deep rust ink for a cream sky


def load_font(size):
    f = ImageFont.truetype(FONT_PATH, size)
    try:
        f.set_variation_by_name("Bold")
    except Exception:
        pass
    return f


def tracked_width(draw, font, text, tracking):
    w = 0.0
    for ch in text:
        w += draw.textlength(ch, font=font)
    return w + tracking * (len(text) - 1)


def draw_tracked(draw, cx, y, font, text, tracking, fill):
    total = tracked_width(draw, font, text, tracking)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def fit_title(draw, text, max_width):
    """Largest (font, tracking) whose tracked width fits max_width."""
    for size in range(170, 60, -2):
        font = load_font(size)
        tracking = size * 0.16
        if tracked_width(draw, font, text, tracking) <= max_width:
            return font, tracking
    font = load_font(60)
    return font, 60 * 0.16


def main():
    art = Image.open(ART).convert("RGB")
    img = art.resize((W, H), Image.LANCZOS)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    font, tracking = fit_title(od, NAME, 810)
    if STYLE == "cream":
        draw_tracked(od, W / 2, 43, font, NAME, tracking, SHADOW + (170,))
        draw_tracked(od, W / 2, 40, font, NAME, tracking, CREAM + (255,))
    elif STYLE == "rust":
        draw_tracked(od, W / 2, 40, font, NAME, tracking, RUST + (255,))
    else:
        draw_tracked(od, W / 2, 40, font, NAME, tracking, INK + (255,))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    q = img.quantize(colors=256, method=Image.MEDIANCUT,
                     dither=Image.FLOYDSTEINBERG)
    q.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} ({size} bytes, name={NAME}, art={os.path.basename(ART)})")
    assert size <= MAX_BYTES, f"{size} bytes over the 1 MiB cap"


if __name__ == "__main__":
    main()
