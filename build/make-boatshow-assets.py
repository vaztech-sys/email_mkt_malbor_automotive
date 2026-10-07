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
    ("product-hydro-coat", "HYDRO COAT", "3.78L", "473ml"),
    ("product-nano-polymer-spray", "NANO POLYMER SPRAY", "3.78L", "473ml"),
    ("product-max-pro-shampoo", "MAX PRO SHAMPOO", "3.78L", "946ml"),
    ("product-deep-cleaning-apc", "DEEP CLEANING APC", "3.78L", "473ml"),
]

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


def placeholder_product(name, gallon, small, size):
    """A plate that cannot be mistaken for finished art."""
    w, h = size
    im = Image.new("RGB", (w, h), PLATE)
    d = ImageDraw.Draw(im)
    # dashed frame
    step, dash = 24, 13
    for x in range(10, w - 10, step):
        d.line([(x, 10), (min(x + dash, w - 10), 10)], fill=MUTED, width=3)
        d.line([(x, h - 10), (min(x + dash, w - 10), h - 10)], fill=MUTED, width=3)
    for y in range(10, h - 10, step):
        d.line([(10, y), (10, min(y + dash, h - 10))], fill=MUTED, width=3)
        d.line([(w - 10, y), (w - 10, min(y + dash, h - 10))], fill=MUTED, width=3)
    # two bottle silhouettes: the gallon and the free small size
    gw, gh = int(w * 0.20), int(h * 0.52)
    gx, gy = int(w * 0.24), int(h * 0.30)
    d.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=10, outline=INK, width=4)
    d.rectangle([gx + gw // 3, gy - 16, gx + 2 * gw // 3, gy], outline=INK, width=4)
    sw_, sh_ = int(w * 0.12), int(h * 0.30)
    sx, sy = int(w * 0.60), gy + gh - sh_
    d.rounded_rectangle([sx, sy, sx + sw_, sy + sh_], radius=7, outline=ORANGE, width=4)
    d.rectangle([sx + sw_ // 3, sy - 12, sx + 2 * sw_ // 3, sy], outline=ORANGE, width=4)
    d.text((sx + sw_ + 10, sy + sh_ // 2 - 10), "FREE", font=ImageFont.truetype(BOLD, 18), fill=ORANGE)

    def centred(text, y, font, fill):
        f = ImageFont.truetype(*font)
        tw = d.textbbox((0, 0), text, font=f)[2]
        d.text(((w - tw) // 2, y), text, font=f, fill=fill)

    centred(name, int(h * 0.09), (BOLD, 22), INK)
    centred(f"{gallon}  +  FREE {small}", int(h * 0.17), (REG, 17), MUTED)
    centred("PLACEHOLDER", int(h * 0.845), (BOLD, 19), ORANGE)
    centred("foto da loja / arte final Borges 12-10", int(h * 0.915), (REG, 15), MUTED)
    return im


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

    print("product plates (ALL PLACEHOLDERS):")
    for slug, name, gallon, small in PRODUCTS:
        write(placeholder_product(name, gallon, small, (258 * X2, 190 * X2)), slug, "258x190")


if __name__ == "__main__":
    main()
