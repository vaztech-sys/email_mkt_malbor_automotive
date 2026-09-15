#!/usr/bin/env python3
"""Rasterize the vector logos to transparent PNGs — email clients do not render SVG."""
import cairosvg
from PIL import Image

# name, display width (px in the email), retina scale
JOBS = [("logo-light", 152, 3), ("logo-dark", 152, 3), ("logo-footer", 175, 3), ("check", 20, 4)]

for name, width, scale in JOBS:
    out = f"assets/{name}.png"
    cairosvg.svg2png(url=f"build/svg/{name}.svg", write_to=out, scale=scale)
    im = Image.open(out).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    im.save(out)
    print(f"{name}: {im.size} (displays at {width}px)")
