#!/usr/bin/env python3
"""Render src/email.html into the deliverables.

  dist/malbor-bogo-mailchimp.html  paste-in-code / template HTML for Mailchimp
  dist/preview/index.html          same markup with local images, for eyeballing

Usage:
  python3 build/build.py                          # placeholder image host
  python3 build/build.py --img-base https://...   # your uploaded image folder
  python3 build/build.py --shop-url https://...   # CTA destination
"""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "email.html"
DIST = ROOT / "dist"
ASSETS = ROOT / "assets"

IMAGES = [
    "hero.jpg", "product-apc.jpg", "product-shampoo.jpg", "product-polymer.jpg",
    "story.jpg", "bogo.png", "check.png", "logo-dark.png", "logo-footer.png",
]

DEFAULT_IMG_BASE = "https://REPLACE-WITH-YOUR-IMAGE-HOST/malbor-bogo/"
DEFAULT_SHOP_URL = "https://malborcoatings.com"


def render(template: str, img_base: str, shop_url: str) -> str:
    return template.replace("{{IMG_BASE}}", img_base).replace("{{SHOP_URL}}", shop_url)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--img-base", default=DEFAULT_IMG_BASE,
                    help="absolute URL of the folder holding the images (keep the trailing slash)")
    ap.add_argument("--shop-url", default=DEFAULT_SHOP_URL, help="CTA destination")
    args = ap.parse_args()

    img_base = args.img_base if args.img_base.endswith("/") else args.img_base + "/"
    template = SRC.read_text(encoding="utf-8")

    DIST.mkdir(exist_ok=True)
    out = DIST / "malbor-bogo-mailchimp.html"
    out.write_text(render(template, img_base, args.shop_url), encoding="utf-8")

    preview = DIST / "preview"
    (preview / "images").mkdir(parents=True, exist_ok=True)
    for name in IMAGES:
        shutil.copy2(ASSETS / name, preview / "images" / name)
    # the preview is opened in a browser, so strip the Mailchimp-only merge tags
    html = render(template, "images/", args.shop_url)
    html = re.sub(r"\*\|IFNOT:ARCHIVE_PAGE\|\*|\*\|END:IF\|\*", "", html)
    html = html.replace("*|ARCHIVE|*", "#").replace("*|UNSUB|*", "#")
    html = html.replace("*|LIST:ADDRESS|*", "4634 Waycross Dr, Coconut Creek, FL 33073")
    (preview / "index.html").write_text(html, encoding="utf-8")

    kb = sum((ASSETS / n).stat().st_size for n in IMAGES) / 1024
    print(f"{out.relative_to(ROOT)}  ({out.stat().st_size / 1024:.0f} KB HTML)")
    print(f"{(preview / 'index.html').relative_to(ROOT)}  (+{len(IMAGES)} images, {kb:.0f} KB total)")
    print(f"image base: {img_base}")
    print(f"CTA url:    {args.shop_url}")


if __name__ == "__main__":
    main()
