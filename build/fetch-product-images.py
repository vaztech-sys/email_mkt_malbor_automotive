#!/usr/bin/env python3
"""Drop the free-size photo into the Boat Show product plates.

The gallons are already real: they live in assets/raw/products/ and the build
composites them with a typographic "+ FREE <size>" lockup. What is still
missing is the photo of the free size (473ml / 946ml). Those live on
cdn.shopify.com, which this session's egress policy blocks.

Run this from any machine that can reach the CDN:

    python3 build/fetch-product-images.py

It fetches only the small sizes, rebuilds each plate as gallon + free size at
the exact dimensions the HTML already expects, and overwrites the files in both
e1/ and e2/. No markup changes. If Borges's final art arrives first, just drop
his files over the same names instead of running this.
"""
import importlib.util
import io
import urllib.request
from pathlib import Path
from PIL import Image

# make-boatshow-assets.py keeps its generation behind a __main__ guard, so
# importing it only gives us the URL table, the product list and compose_plate
spec = importlib.util.spec_from_file_location("mba", Path(__file__).with_name("make-boatshow-assets.py"))
mba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mba)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "malbor-email-build"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read()))


for slug, name, gallon_size, free_size, art in mba.PRODUCTS:
    small_url = mba.STORE_PHOTOS[slug][1]
    plate = mba.compose_plate(Image.open(mba.GALLONS / art), fetch(small_url), free_size)
    for out in mba.OUTS:
        plate.save(out / f"{slug}.jpg", quality=84, optimize=True, progressive=True)
    print(f"  {slug}.jpg  galao local + brinde da loja")

print("\npronto. Agora:")
print("  1. troque ARTE PARCIAL por um comentario normal em build/make-boatshow-html.py")
print("  2. rode check.mjs e build-zip.sh nas duas pecas")
