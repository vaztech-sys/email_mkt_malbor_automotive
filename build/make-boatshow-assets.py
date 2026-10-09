#!/usr/bin/env python3
"""Build the Boat Show (ML-17) asset set for E1 and E2.

PRODUCT IMAGES ARE PLACEHOLDERS. The real store photos live on
cdn.shopify.com, which this session's egress policy blocks, and Borges
delivers the final art on Mon 12 Oct. Each placeholder is drawn at the exact
display size the HTML expects, so swapping is a straight file replacement —
no markup change. The live store URLs are recorded in STORE_PHOTOS below;
build/fetch-product-images.py turns them into finished composites from any
machine that can reach the CDN.
"""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

X2 = 2
PLATE = "#f4f4f2"
INK = "#24211e"
ORANGE = "#ea560d"
MUTED = "#8a8578"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

AUTO = Path("email/automotive/assets")
RAW = Path("assets/raw")
MARINES = Path("/home/user/vaztech-sys/email_mkt_malbor_marines/email/marines/assets")
OUTS = [Path("email/boatshow-e1/assets"), Path("email/boatshow-e2/assets")]

# Offer line-up. value = retail price of the free size, from the live store.
PRODUCTS = [
    ("product-hydro-coat", "HYDRO COAT", "3.78L", "473ml", "hydro-coat-gallon.webp"),
    ("product-nano-polymer-spray", "NANO POLYMER SPRAY", "3.78L", "473ml", "nano-polymer-spray-gallon.webp"),
    ("product-max-pro-shampoo", "MAX PRO SHAMPOO", "3.78L", "946ml", "max-pro-shampoo-gallon.webp"),
    ("product-deep-cleaning-apc", "DEEP CLEANING APC", "3.78L", "473ml", "deep-cleaning-apc-gallon.webp"),
]

GALLONS = RAW / "products"
CARD = (258 * X2, 190 * X2)

# Live store photo URLs, verified against the Shopify catalogue on 7 Oct 2026.
STORE_PHOTOS = {
    "product-hydro-coat": (
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/HydroCoat37.webp?v=1748634707",
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/HYDROCOAT_1_2da775a3-cbcc-47a7-9291-8a2e959b4638.webp?v=1753992283"),
    "product-nano-polymer-spray": (
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/NANOPOLYMER3L_1.webp?v=1747579616",
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/NANO_POLYMER.webp?v=1746226744"),
    "product-max-pro-shampoo": (
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/MAX_PRO_SHAMPOO_3L.webp?v=1746222688",
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/Max_Pro_Shampoo_946ml.webp?v=1746222687"),
    "product-deep-cleaning-apc": (
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/DEEP_CLEANING_3L.webp?v=1746222688",
        "https://cdn.shopify.com/s/files/1/0929/1828/4608/files/DEEP_CLEANING.webp?v=1746222688"),
}


def flatten(im, bg):
    c = Image.new("RGBA", im.size, bg)
    c.alpha_composite(im.convert("RGBA"))
    return c.convert("RGB")


def cover(im, size):
    tw, th = size
    sw, sh = im.size
    s = max(tw / sw, th / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    return im.crop((l, t, l + tw, t + th))


def trim(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def compose_plate(gallon, small, free_size, size=None):
    """The product plate: the real gallon, plus the free size beside it.

    `small` is the photo of the free size when we have one; until then it is
    None and we set a typographic lockup in its place rather than inventing
    product art.
    """
    w, h = size or CARD
    plate = Image.new("RGBA", (w, h), PLATE)
    pad = 30
    gh = h - 2 * pad
    gallon = trim(gallon.convert("RGBA"))
    gw = round(gallon.width * gh / gallon.height)
    gallon = gallon.resize((gw, gh), Image.LANCZOS)

    d = ImageDraw.Draw(plate)
    if small is not None:
        small = trim(small.convert("RGBA"))
        sh = round(gh * 0.62)
        sw = round(small.width * sh / small.height)
        total = gw + 18 + sw
        x = (w - total) // 2
        plate.alpha_composite(gallon, (x, pad))
        plate.alpha_composite(small, (x + gw + 18, pad + gh - sh))
        f = ImageFont.truetype(BOLD, 20)
        label = f"FREE {free_size}"
        tw = d.textbbox((0, 0), label, font=f)[2]
        d.text((x + gw + 18 + (sw - tw) // 2, pad + gh - sh - 28), label, font=f, fill=ORANGE)
    else:
        # no photo of the free size yet -> typographic lockup, never fake art
        block_w = 190
        total = gw + 24 + block_w
        x = max(pad, (w - total) // 2)
        plate.alpha_composite(gallon, (x, pad))
        bx = x + gw + 24
        cy = h // 2
        fp = ImageFont.truetype(BOLD, 60)
        ff = ImageFont.truetype(BOLD, 34)
        fs = ImageFont.truetype(BOLD, 40)
        d.text((bx, cy - 92), "+", font=fp, fill=ORANGE)
        d.text((bx, cy - 18), "FREE", font=ff, fill=ORANGE)
        d.text((bx, cy + 22), free_size, font=fs, fill=INK)
        # No "pending" wording is burned into the plate: this lockup is
        # ship-ready on its own. The outstanding gift photo is tracked by the
        # ARTE PARCIAL comment in the HTML and by check.mjs.
    return flatten(plate, PLATE)


def write(im, name, display, jpeg=True, targets=None):
    for out in (targets or OUTS):
        p = out / (name + (".jpg" if jpeg else ".png"))
        im.save(p, quality=84, optimize=True, progressive=True) if jpeg else im.save(p, optimize=True)
    print(f"  {name}{'.jpg' if jpeg else '.png'}  {im.size}  displays {display}")


def main():
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)

    print("carried over from the BOGO piece:")
    for f in ["malbor-logo-white.png", "check.png"]:
        for out in OUTS:
            shutil.copy2(AUTO / f, out / f)
        print(f"  {f}")

    print("hero (PLACEHOLDER — marine opening, pending Borges):")
    hero = Image.open(MARINES / "hero-marina.jpg").convert("RGBA")
    write(flatten(cover(hero, (600 * X2, 270 * X2)), "#12100c"), "hero-boatshow", "600x270")

    print("automotive block photo:")
    car = Image.open(RAW / "2268ffca474745f43f019408011a6fedd8610aec.png").convert("RGBA")
    write(flatten(cover(car, (226 * X2, 151 * X2)), PLATE), "auto-block", "226x151", targets=OUTS[:1])  # E1 only

    print("product plates (galao real da loja; foto do brinde pendente):")
    for slug, name, gallon, small, art in PRODUCTS:
        write(compose_plate(Image.open(GALLONS / art), None, small), slug, "258x190")


if __name__ == "__main__":
    main()
