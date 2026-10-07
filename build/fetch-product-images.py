#!/usr/bin/env python3
"""Replace the Boat Show product placeholders with the real store photos.

Run this from any machine that can reach cdn.shopify.com (this session's egress
policy blocks it). It downloads the gallon and the free small size for each
product, composites them onto the same #f4f4f2 plate at the exact size the HTML
expects, and overwrites the placeholder in both e1/ and e2/ asset folders.

    python3 build/fetch-product-images.py

Nothing in the HTML changes — the filenames and dimensions are identical.
If Borges's final art arrives first, just drop his files over the same names.
"""
import io
import urllib.request
from pathlib import Path
from PIL import Image

import sys

# single source of truth for the URLs and the output folders; importing is safe
# because that module keeps its generation behind a __main__ guard
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location("mba", Path(__file__).with_name("make-boatshow-assets.py"))
mba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mba)

PLATE = "#f4f4f2"
W, H = 258 * 2, 190 * 2
PAD = 24


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "malbor-email-build"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGBA")


def compose(gallon, small):
    """Gallon on the left at full height, the free small size beside it, baselines aligned."""
    plate = Image.new("RGBA", (W, H), PLATE)
    gh = H - 2 * PAD
    gw = round(gallon.width * gh / gallon.height)
    gallon = gallon.resize((gw, gh), Image.LANCZOS)
    sh = round(gh * 0.60)
    sw = round(small.width * sh / small.height)
    small = small.resize((sw, sh), Image.LANCZOS)
    total = gw + 16 + sw
    x = (W - total) // 2
    base = PAD + gh
    plate.alpha_composite(gallon, (x, base - gh))
    plate.alpha_composite(small, (x + gw + 16, base - sh))
    out = Image.new("RGBA", (W, H), PLATE)
    out.alpha_composite(plate)
    return out.convert("RGB")


for slug, (gal_url, small_url) in mba.STORE_PHOTOS.items():
    img = compose(fetch(gal_url), fetch(small_url))
    for out in mba.OUTS:
        img.save(out / f"{slug}.jpg", quality=84, optimize=True, progressive=True)
    print(f"  {slug}.jpg  {img.size}  <- loja")
print("pronto — rode check.mjs e build-zip.sh nas duas pecas")
