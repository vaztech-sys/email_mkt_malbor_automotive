#!/usr/bin/env python3
"""Build the email-ready image set from the Figma export.

Every asset is rendered at 2x the size it is displayed at, so it stays sharp on
retina screens while the HTML pins the display width. Rounded corners are baked
into the pixels (against the panel colour behind them) because Outlook ignores
border-radius on images.
"""
from PIL import Image, ImageDraw

RAW = "assets/raw"
HERO_SRC = f"{RAW}/2268ffca474745f43f019408011a6fedd8610aec.png"
BOGO_SRC = f"{RAW}/logo_BOGO.png"
STORY_SRC = f"{RAW}/b11ea89c2bc1427d2bc5c6a60a60206c7bc6d1ab.png"
PRODUCTS = [
    ("product-apc", f"{RAW}/ccd308befe699871ae233645cefb6f29cd95357d.png"),
    ("product-shampoo", f"{RAW}/598a9f408abf9e3ff59aacfad4f1ab8ca6e9c36d.png"),
    ("product-polymer", f"{RAW}/ed866f33b3e121c138d651b3d30e5b558670d778.png"),
]

X2 = 2  # retina factor


def rounded(im, radius, corners=(True, True, True, True)):
    """Return im with its corners cut to transparency."""
    mask = Image.new("L", im.size, 255)
    d = ImageDraw.Draw(mask)
    r = radius
    w, h = im.size
    box = [(0, 0), (w - 1, h - 1)]
    square = Image.new("L", im.size, 0)
    ImageDraw.Draw(square).rounded_rectangle(box, radius=r, fill=255)
    mask = square
    # put back any corner that should stay square
    tl, tr, br, bl = corners
    patch = ImageDraw.Draw(mask)
    if not tl: patch.rectangle([(0, 0), (r, r)], fill=255)
    if not tr: patch.rectangle([(w - 1 - r, 0), (w - 1, r)], fill=255)
    if not br: patch.rectangle([(w - 1 - r, h - 1 - r), (w - 1, h - 1)], fill=255)
    if not bl: patch.rectangle([(0, h - 1 - r), (r, h - 1)], fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def flatten(im, bg):
    canvas = Image.new("RGBA", im.size, bg)
    canvas.alpha_composite(im.convert("RGBA"))
    return canvas.convert("RGB")


def cover(im, size):
    """Scale-and-centre-crop im to exactly size."""
    tw, th = size
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def contain(im, size, bg, pad=0):
    """Fit the whole of im inside size on a bg plate, with optional padding."""
    tw, th = size
    iw, ih = tw - 2 * pad, th - 2 * pad
    sw, sh = im.size
    scale = min(iw / sw, ih / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", size, bg)
    canvas.alpha_composite(im.convert("RGBA"), ((tw - im.width) // 2, (th - im.height) // 2))
    return canvas


# ---------------------------------------------------------------- hero 600x416
# The Figma hero crops into the photo; mirror that framing, then bake the
# white MALBOR lockup in so the header survives clients that block backgrounds.
HERO_W, HERO_H = 600 * X2, 416 * X2
hero = Image.open(HERO_SRC).convert("RGBA")
hero = hero.crop((128, 0, 1475, 897))          # matches the design's zoom/offset
hero = hero.resize((HERO_W, HERO_H), Image.LANCZOS)
logo = Image.open("assets/logo-light.png").convert("RGBA")
LOGO_W = 114 * X2                               # 152px design logo at 0.75 scale
logo = logo.resize((LOGO_W, round(logo.height * LOGO_W / logo.width)), Image.LANCZOS)
hero.alpha_composite(logo, (24 * X2, 30 * X2))
flatten(hero, "#12100c").save("assets/hero.jpg", quality=88, optimize=True)
print("hero.jpg", (HERO_W, HERO_H), "-> displays 600x416")

# ------------------------------------------------------- products 178x200 each
PW, PH, RAD = 178 * X2, 200 * X2, 16 * X2
for name, src in PRODUCTS:
    im = Image.open(src).convert("RGBA")
    plate = contain(im, (PW, PH), "#ffffff", pad=10 * X2)
    plate = rounded(plate, RAD, corners=(True, True, False, False))  # card top only
    flatten(plate, "#ffffff").save(f"assets/{name}.jpg", quality=90, optimize=True)
    print(f"{name}.jpg", (PW, PH), "-> displays 178x200")

# --------------------------------------------------------------- story 240x183
STORY_X = 3  # 3x: this one goes full-width when the layout stacks on phones
SW_, SH_ = 240 * STORY_X, 183 * STORY_X
story = cover(Image.open(STORY_SRC).convert("RGBA"), (SW_, SH_))
story = rounded(story, 16 * STORY_X)
flatten(story, "#f4f4f2").save("assets/story.jpg", quality=88, optimize=True)
print("story.jpg", (SW_, SH_), "-> displays 240x183")

# ---------------------------------------------------------------- bogo 150x126
BW, BH = 150 * X2, 126 * X2
bogo = contain(Image.open(BOGO_SRC).convert("RGBA"), (BW, BH), "#f4f4f2")
flatten(bogo, "#f4f4f2").save("assets/bogo.png")
print("bogo.png", (BW, BH), "-> displays 150x126")
