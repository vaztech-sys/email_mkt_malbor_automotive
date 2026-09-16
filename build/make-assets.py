#!/usr/bin/env python3
"""Build the automotive email asset set from the Figma Make export.

Mirrors the geometry of the finished marine piece so the two campaign sends are
siblings. Every asset is exported at exactly 2x its display size, except the
product shots, which stay at the artwork's native 248px width rather than being
upscaled (the HTML caps them with .em-img-prod).

Rules carried over from the marine build:
  - the product PNGs carry alpha; they are flattened onto #f4f4f2, never white,
    or a white rectangle shows through the card's image cell
  - logos are rasterised from the Figma path data, since email clients do not
    render SVG
"""
import cairosvg
from PIL import Image

RAW = "assets/raw"
OUT = "email/automotive/assets"
PLATE = "#f4f4f2"          # card image cell + grey section background

HERO_SRC = f"{RAW}/2268ffca474745f43f019408011a6fedd8610aec.png"
STORY_SRC = f"{RAW}/b11ea89c2bc1427d2bc5c6a60a60206c7bc6d1ab.png"
BADGE_SRC = f"{RAW}/logo_BOGO.png"
PRODUCTS = [
    ("product-deep-cleaning-apc", f"{RAW}/ccd308befe699871ae233645cefb6f29cd95357d.png"),
    ("product-max-pro-shampoo", f"{RAW}/598a9f408abf9e3ff59aacfad4f1ab8ca6e9c36d.png"),
    ("product-max-shield-polymer", f"{RAW}/ed866f33b3e121c138d651b3d30e5b558670d778.png"),
]


def flatten(im, bg):
    canvas = Image.new("RGBA", im.size, bg)
    canvas.alpha_composite(im.convert("RGBA"))
    return canvas.convert("RGB")


def cover(im, size):
    tw, th = size
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def contain(im, size, bg, pad=0):
    tw, th = size
    sw, sh = im.size
    scale = min((tw - 2 * pad) / sw, (th - 2 * pad) / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", size, bg)
    canvas.alpha_composite(im.convert("RGBA"), ((tw - im.width) // 2, (th - im.height) // 2))
    return canvas


def jpg(im, name, display):
    im.save(f"{OUT}/{name}.jpg", quality=82, optimize=True, progressive=True)
    print(f"  {name}.jpg  {im.size}  displays {display}")


def png(im, name, display):
    im.save(f"{OUT}/{name}.png", optimize=True)
    print(f"  {name}.png  {im.size}  displays {display}")


print("logos (rasterised from the Figma vector paths):")
for svg, name, disp_w in [("logo-light", "malbor-logo-white", 114), ("logo-dark", "malbor-logo", 114)]:
    tmp = f"/tmp/{svg}-2x.png"
    cairosvg.svg2png(url=f"build/svg/{svg}.svg", write_to=tmp, output_width=disp_w * 2)
    im = Image.open(tmp).convert("RGBA")
    im = im.crop(im.getbbox())
    png(im, name, f"{disp_w}x{round(im.height * disp_w / im.width)}")

cairosvg.svg2png(url="build/svg/check.svg", write_to=f"{OUT}/check.png", output_width=32, output_height=32)
print(f"  check.png  (32, 32)  displays 16x16")

print("photos:")
# hero — a 600x270 banner cut from the full-bleed car shot
hero = Image.open(HERO_SRC).convert("RGBA").crop((0, 160, 1601, 880))
jpg(flatten(hero.resize((1200, 540), Image.LANCZOS), "#12100c"), "hero-automotive", "600x270")

# product shots — kept at the artwork's native 248px width, never upscaled
for name, src in PRODUCTS:
    plate = contain(Image.open(src).convert("RGBA"), (248, 262), PLATE, pad=10)
    jpg(flatten(plate, PLATE), name, "168x178 (native 248px, capped by .em-img-prod)")

# grey-section photo
jpg(flatten(cover(Image.open(STORY_SRC).convert("RGBA"), (452, 302)), PLATE), "story-marine-origin", "226x151")

# BOGO badge keeps its alpha so it sits on the grey panel cleanly
badge = Image.open(BADGE_SRC).convert("RGBA")
png(badge.resize((290, round(290 * badge.height / badge.width)), Image.LANCZOS), "bogo-badge", "145x122")
