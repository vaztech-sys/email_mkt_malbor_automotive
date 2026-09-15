# MALBOR Coatings — "Two gallons. One price." email

The Figma Make export (`EMAIL_MKT_Automotive`) rebuilt as a Mailchimp-ready HTML email.

The original export is a React + Tailwind app: flexbox, `<svg>` logos, CSS `object-fit`,
`gap`, and a fixed 800px canvas. None of that survives an email client, so the layout was
rebuilt as nested tables with inline styles at the 600px email standard, and every vector
and cropped asset was flattened to a PNG/JPG.

## Deliverables

| File | What it is |
| --- | --- |
| `dist/malbor-bogo-mailchimp.html` | The campaign HTML — paste into Mailchimp |
| `dist/preview/index.html` | Same markup with local images, for opening in a browser |
| `assets/*.png`, `assets/*.jpg` | The 9 images to upload to Mailchimp's Content Studio |
| `src/email.html` | Template source (`{{IMG_BASE}}` / `{{SHOP_URL}}` placeholders) |
| `build/` | Scripts that regenerate the assets and the HTML |

## Sending it in Mailchimp

1. **Upload the images.** Mailchimp → *Content Studio* → upload everything in `assets/`
   except the `raw/` folder (9 files, ~300 KB). Copy the folder URL they land on —
   it looks like `https://mcusercontent.com/<id>/images/`.

2. **Stamp that URL into the HTML** and set where the button goes:

   ```bash
   python3 build/build.py \
     --img-base https://mcusercontent.com/<your-id>/images/ \
     --shop-url https://malborcoatings.com/collections/classic-line
   ```

   Re-run this any time either URL changes — it rewrites `dist/malbor-bogo-mailchimp.html`.

3. **Create the campaign.** *Campaigns → Email → Regular*, then under Content choose
   **Code your own → Paste in code**, and paste the whole file.
   To reuse it later instead, *Content → Email templates → Create → Code your own →
   Paste in code* saves it as a template — the nine `mc:edit` regions below become
   editable blocks in the drag-and-drop editor.

4. **Suggested subject / preview:**
   - Subject: `Two gallons. One price.`
   - Preview text is already baked into the HTML: *"Buy one 3.78L gallon of the Classic
     Line, get the second free — through September 29 or while stock lasts."*

5. **Send a test** to Gmail, Outlook and an iPhone before scheduling.

### Editable regions (`mc:edit`)

`headline`, `offer`, `products_title`, `product_1`, `product_2`, `product_3`,
`story`, `terms`, `contact`

## What it does on its own

- **600px wide**, stacks to a single column below 620px (product cards, the story
  section and the BOGO/terms row all collapse).
- **Retina images** — every asset is rendered at 2x (the story photo at 3x, since it
  goes full-width on phones) and pinned to its display size in the HTML.
- **Outlook**: the two orange CTAs are VML `roundrect` buttons, so they render as real
  filled buttons rather than bare links.
- **Merge tags** already in place: `*|UNSUB|*`, `*|LIST:ADDRESS|*`, and the
  view-in-browser link wrapped in `*|IFNOT:ARCHIVE_PAGE|*` so it disappears on the
  archive page. Mailchimp will not let a campaign send without the first two.
- **Hidden preheader** so the inbox preview line is not scraped from the body.
- **Dark mode**: Apple Mail is told to keep the cream panels instead of inverting them.

## Rebuilding the images

```bash
pip install pillow cairosvg
node    build/make-logos.mjs   # Figma path data -> build/svg/*.svg
python3 build/rasterize.py     # SVG -> transparent PNG (email clients do not render SVG)
python3 build/make-images.py   # crops, retina scaling, baked rounded corners
python3 build/build.py         # -> dist/
```

`assets/raw/` holds the untouched Figma export that these scripts read from.

## Deliberate differences from the Figma file

- **Canvas 800px → 600px.** 800px is wider than every major client's reading pane.
  Type sizes were scaled to match (48px headline → 40px, 32px section heads → 30/28px),
  staying above the 11px floor used in the product copy.
- **Product photos are letterboxed, not cropped.** Figma used `object-fit: cover` on a
  225×238 box, which cut the cap and base off the gallons. They are now fitted whole onto
  a white plate, so the full bottle shows.
- **Rounded corners are baked into the images** rather than set with `border-radius`,
  because Outlook ignores the CSS. The panel and card corners still use `border-radius`,
  which simply squares off in Outlook.
- **Fonts.** Montserrat, Poppins and Work Sans load from Google Fonts for Apple Mail and
  iOS; everywhere else (Gmail, Outlook) they fall back to Arial/Helvetica, which is why
  the weights and sizes were chosen to hold up in both.
- **The footer address is `*|LIST:ADDRESS|*`**, pulled from your Mailchimp audience
  settings, instead of the hardcoded "4634 Waycross Dr, Coconut Creek, FL 33073". That is
  what keeps the campaign CAN-SPAM compliant. If you want the literal line instead,
  replace the tag in `src/email.html` — but the audience address must still be set.
