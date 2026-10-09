#!/usr/bin/env python3
"""Emit index.html + plain-text.txt for the Boat Show pieces (ML-17).

Both pieces reuse the table/inline-CSS structure of the BOGO piece in
email/automotive/. Copy is the Fernando-pending text, verbatim.
"""
from pathlib import Path

LP_T = ("https://bogo.malborcoatings.com/?utm_source=mailchimp&utm_medium=email"
        "&utm_campaign=boatshow_oct2026&utm_content=malbor")
LP = LP_T.replace("&", "&amp;")
A = "https://ASSET-BASE-REPLACE-ME"
MONT = "'Montserrat','Helvetica Neue',Helvetica,Arial,sans-serif"
POP = "'Poppins','Helvetica Neue',Helvetica,Arial,sans-serif"
WORK = "'Work Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
ADDR = "4634 Waycross Dr, Coconut Creek, FL 33073"

PRODUCTS = [
    ("product-hydro-coat", "Hydro Coat", "$89", "473ml", "$19",
     "SiO2 spray sealant. Spray after the wash for a deep, slick gloss that sheds water."),
    ("product-nano-polymer-spray", "Nano Polymer Spray", "$139", "473ml", "$29",
     "Nano polymer protection in a quick spray-and-wipe step. Automotive and Marine versions."),
    ("product-max-pro-shampoo", "Max Pro Shampoo", "$45", "946ml", "$19",
     "SiO2 shampoo that maintains gloss and protection every wash. Safe on clear coat, gelcoat, "
     "plastics, trim and metals."),
    ("product-deep-cleaning-apc", "Deep Cleaning APC", "$39", "473ml", "$12",
     "Super-concentrated cleaner for interiors, engine bays and heavy soil. Rinses clean without residue."),
]

TERMS = [
    "The free size is added with each gallon. Discount applied at checkout.",
    "October 15 &ndash; November 1, 2026, while supplies last.",
    "Local pickup in Pompano Beach or at Safe Harbor Lauderdale Marine Center.",
]

STYLE = """@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Poppins:wght@400;500;600;700&family=Work+Sans:wght@700&display=swap');
body,table,td,a{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}
table,td{mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse}
img{-ms-interpolation-mode:bicubic;border:0;outline:none;text-decoration:none;display:block}
body{margin:0!important;padding:0!important;width:100%!important;background-color:#f4f4f2}
a{text-decoration:none}
.em-body{margin:0;padding:0;width:100%;background-color:#f4f4f2}
@media only screen and (max-width:600px){
  .em-shell{width:100%!important;max-width:100%!important}
  .em-pad{padding-left:20px!important;padding-right:20px!important}
  .em-pad-y{padding-top:32px!important;padding-bottom:32px!important}
  .em-stack{display:block!important;width:100%!important;max-width:100%!important;box-sizing:border-box!important;padding-left:0!important;padding-right:0!important}
  .em-stack-gap{padding-bottom:20px!important}
  .em-center{text-align:center!important}
  .em-h1{font-size:26px!important;line-height:1.2!important;letter-spacing:-0.6px!important}
  .em-h2{font-size:22px!important;line-height:1.15!important}
  .em-img-full{width:100%!important;height:auto!important;max-width:100%!important;margin-left:auto!important;margin-right:auto!important}
  .em-btn{width:100%!important}
  .em-btn a{width:auto!important;display:block!important;padding-left:16px!important;padding-right:16px!important;font-size:16px!important}
  .em-card{width:100%!important;max-width:100%!important;margin-left:auto!important;margin-right:auto!important}
}"""


def head(title, preheader):
    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="format-detection" content="telephone=no,address=no,email=no,date=no,url=no" />
<meta name="color-scheme" content="light only" />
<meta name="supported-color-schemes" content="light only" />
<title>{title}</title>
<!--[if mso]>
<xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml>
<![endif]-->
<style type="text/css">
{STYLE}
</style>
</head>
<body class="em-body">

<!-- preheader -->
<div style="display:none;font-size:1px;color:#f4f4f2;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">{preheader}</div>
<div style="display:none;font-size:1px;color:#f4f4f2;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">{'&#847;&nbsp;' * 20}</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f4f2;">
<tr><td align="center" style="padding:0;">

<table role="presentation" class="em-shell" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background-color:#ffffff;">

  <!-- ============ HEADER ============ -->
  <tr>
    <td align="center" bgcolor="#24211e" style="background-color:#24211e;padding:25px 18px;font-size:0;line-height:0;">
      <a href="{LP}" target="_blank" style="text-decoration:none;">
        <img src="{A}/malbor-logo-white.png" width="114" height="34" alt="Malbor Coatings" style="display:block;width:114px;height:34px;border:0;" />
      </a>
    </td>
  </tr>

  <!-- ============ HERO ============ -->
  <tr>
    <td align="center" style="padding:0;font-size:0;line-height:0;">
      <a href="{LP}" target="_blank" style="text-decoration:none;">
        <img src="{A}/hero-boatshow.jpg" width="600" height="270" alt="Varnished wooden sailboat moored at the dock" class="em-img-full" style="display:block;width:100%;max-width:600px;height:auto;border:0;" />
      </a>
    </td>
  </tr>
"""


def button(label):
    return f"""      <table role="presentation" class="em-btn" cellpadding="0" cellspacing="0" border="0" style="width:317px;">
        <tr>
          <td align="center" bgcolor="#ea560d" style="background-color:#ea560d;border-radius:4px;">
            <!--[if mso]>
            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{LP}" style="height:48px;v-text-anchor:middle;width:317px;" arcsize="9%" stroke="f" fillcolor="#ea560d">
            <w:anchorlock/><center style="color:#f4f4f2;font-family:Arial,sans-serif;font-size:18px;font-weight:bold;">{label}</center>
            </v:roundrect>
            <![endif]-->
            <!--[if !mso]><!-- -->
            <a href="{LP}" target="_blank" style="display:block;padding:12px 20px;font-family:{WORK};font-weight:700;font-size:18px;line-height:24px;letter-spacing:-0.4px;color:#f4f4f2;text-decoration:none;border-radius:4px;">{label}</a>
            <!--<![endif]-->
          </td>
        </tr>
      </table>"""


def card(slug, name, price, small, value, desc, full):
    """full=True renders price + description (E1); False is the compact recap (E2)."""
    detail = f"""                    <tr>
                      <td style="padding-bottom:6px;">
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                          <tr>
                            <td align="left" style="font-family:{POP};font-weight:400;font-size:18px;line-height:1.6;color:#000000;">3.78L</td>
                            <td align="right" style="font-family:{MONT};font-weight:700;font-size:18px;line-height:1.1;color:#000000;">{price}</td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td style="font-family:{POP};font-weight:600;font-size:13px;line-height:1.5;color:#ea560d;padding-bottom:8px;">
                        + free {small} ({value} value)
                      </td>
                    </tr>
                    <tr>
                      <td style="font-family:{POP};font-weight:500;font-size:12px;line-height:1.7;color:#525252;">
                        {desc}
                      </td>
                    </tr>""" if full else f"""                    <tr>
                      <td style="font-family:{POP};font-weight:600;font-size:13px;line-height:1.5;color:#ea560d;">
                        3.78L + free {small}
                      </td>
                    </tr>"""
    return f"""            <table role="presentation" class="em-card" width="258" cellpadding="0" cellspacing="0" border="0" style="width:258px;max-width:258px;">
              <tr>
                <td style="border:1px solid #cacaca;border-bottom:0;border-radius:16px 16px 0 0;background-color:#f4f4f2;font-size:0;line-height:0;">
                  <!-- ARTE PARCIAL: {slug}.jpg (516x380) - galao real da loja + lockup tipografico; falta a foto do brinde (Borges 12/10) -->
                  <a href="{LP}" target="_blank" style="text-decoration:none;">
                    <img src="{A}/{slug}.jpg" width="258" height="190" alt="Malbor {name} 3.78L with free {small}" class="em-img-full" style="display:block;width:100%;max-width:258px;height:auto;border:0;border-radius:16px 16px 0 0;" />
                  </a>
                </td>
              </tr>
              <tr>
                <td style="border:1px solid #cacaca;border-top:0;border-radius:0 0 16px 16px;background-color:#ffffff;padding:14px;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td style="font-family:{MONT};font-weight:700;font-size:16px;line-height:1.4;color:#000000;padding-bottom:4px;">
                        <a href="{LP}" target="_blank" style="color:#000000;text-decoration:none;">{name}</a>
                      </td>
                    </tr>
{detail}
                  </table>
                </td>
              </tr>
            </table>"""


def grid(full):
    rows = []
    for i in range(0, len(PRODUCTS), 2):
        pair = PRODUCTS[i:i + 2]
        last_row = i + 2 >= len(PRODUCTS)
        cells = []
        for j, p in enumerate(pair):
            gap = "" if j == len(pair) - 1 else "padding-right:12px;"
            cls = "em-stack" if (j == len(pair) - 1 and last_row) else "em-stack em-stack-gap"
            cells.append(f"""          <td class="{cls}" width="258" valign="top" style="width:258px;{gap}{'' if last_row else 'padding-bottom:12px;'}">
{card(*p, full=full)}
          </td>""")
        rows.append("        <tr>\n" + "\n".join(cells) + "\n        </tr>")
    return "\n".join(rows)


def terms_block():
    out = []
    for i, t in enumerate(TERMS):
        last = i == len(TERMS) - 1
        pad = "0 10px 0 0" if last else "0 10px 8px 0"
        pb = "" if last else "padding-bottom:8px;"
        out.append(f"""              <tr>
                <td width="16" valign="top" style="width:16px;padding:{pad};"><img src="{A}/check.png" width="16" height="16" alt="" style="display:block;width:16px;height:16px;border:0;" /></td>
                <td valign="top" style="{pb}">{t}</td>
              </tr>""")
    return "\n".join(out)


FOOTER = f"""
  <!-- ============ FOOTER ============ -->
  <tr>
    <td align="center" bgcolor="#47423c" class="em-pad" style="background-color:#47423c;padding:36px 24px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td align="center" style="padding-bottom:14px;">
            <img src="{A}/malbor-logo-white.png" width="114" height="34" alt="Malbor Coatings" style="display:block;width:114px;height:34px;border:0;" />
          </td>
        </tr>
        <tr>
          <td align="center" style="font-family:{POP};font-weight:400;font-size:12px;line-height:1.8;color:#ffffff;padding-bottom:12px;">
            {ADDR}
          </td>
        </tr>
        <tr>
          <td align="center" style="font-family:{POP};font-weight:600;font-size:12px;line-height:1.8;color:#ffffff;">
            <a href="*|UNSUB|*" style="color:#ffffff;text-decoration:underline;">unsubscribe</a>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href="*|UPDATE_PROFILE|*" style="color:#ffffff;text-decoration:underline;">update preferences</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>

</table>

</td></tr>
</table>

</body>
</html>
"""


def terms_section(pad_top=0):
    return f"""
  <!-- ============ TERMS ============ -->
  <tr>
    <td bgcolor="#f4f4f2" class="em-pad em-pad-y" style="background-color:#f4f4f2;padding:{pad_top or 36}px 38px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family:{POP};font-weight:700;font-size:14px;line-height:1.6;color:#5c574c;">
{terms_block()}
      </table>
    </td>
  </tr>
"""


# ----------------------------------------------------------------- E1
e1 = head("Buy the gallon, get the small one free",
          "Hydro Coat, Nano Polymer Spray, Max Pro Shampoo and Deep Cleaning APC &mdash; through Nov 1.")
e1 += f"""
  <!-- ============ HEADLINE + INTRO ============ -->
  <tr>
    <td class="em-pad em-pad-y" style="padding:36px 36px 24px 36px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td align="center" class="em-h1" style="font-family:{MONT};font-weight:700;font-size:30px;line-height:1.15;letter-spacing:-0.8px;color:#7c2c12;padding-bottom:16px;">
            BUY THE GALLON.<br />THE SMALL ONE IS ON US.
          </td>
        </tr>
        <tr>
          <td align="center" style="font-family:{POP};font-weight:400;font-size:14px;line-height:1.6;color:#525252;">
            From October 15 to November 1, every 3.78L gallon below comes with the small size of the same product, free. One click adds both to your cart.
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ============ CTA 1 ============ -->
  <tr>
    <td align="center" class="em-pad" style="padding:0 36px 36px 36px;">
{button("SHOP THE GALLONS")}
    </td>
  </tr>

  <!-- ============ PRODUCTS ============ -->
  <tr>
    <td class="em-pad" style="padding:0 36px 36px 36px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{grid(full=True)}
      </table>
    </td>
  </tr>

  <!-- ============ AUTOMOTIVE BLOCK ============ -->
  <tr>
    <td bgcolor="#f4f4f2" class="em-pad em-pad-y" style="background-color:#f4f4f2;padding:48px 38px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td class="em-stack em-stack-gap" valign="top" style="padding-right:36px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td class="em-h2" style="font-family:{MONT};font-weight:700;font-size:26px;line-height:1.1;color:#726c5c;padding-bottom:18px;">
                  BUILT FOR SALT.<br />PROVEN ON PAINT.
                </td>
              </tr>
              <tr>
                <td style="font-family:{POP};font-weight:400;font-size:14px;line-height:1.6;color:#525252;">
                  Malbor formulas were developed for the marine environment, where salt and constant sun break down protection faster than anything a car sees on the road.
                </td>
              </tr>
            </table>
          </td>
          <td class="em-stack" width="226" valign="top" style="width:226px;font-size:0;line-height:0;">
            <img src="{A}/auto-block.jpg" width="226" height="151" alt="Malbor coating being applied to a classic car" class="em-img-full" style="display:block;width:100%;max-width:226px;height:auto;border:0;border-radius:16px;" />
          </td>
        </tr>
      </table>
    </td>
  </tr>
{terms_section()}
  <!-- ============ CTA 2 ============ -->
  <tr>
    <td align="center" class="em-pad em-pad-y" style="padding:36px;">
{button("SHOP NOW")}
    </td>
  </tr>
{FOOTER}"""

# ----------------------------------------------------------------- E2
e2 = head("Ends Sunday: free small size with every gallon",
          "Last days of the offer &mdash; through November 1.")
e2 += f"""
  <!-- ============ HEADLINE + BODY ============ -->
  <tr>
    <td class="em-pad em-pad-y" style="padding:36px 36px 24px 36px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td align="center" class="em-h1" style="font-family:{MONT};font-weight:700;font-size:34px;line-height:1.15;letter-spacing:-0.8px;color:#7c2c12;padding-bottom:16px;">
            LAST CALL.
          </td>
        </tr>
        <tr>
          <td align="center" style="font-family:{POP};font-weight:400;font-size:14px;line-height:1.6;color:#525252;">
            Through Sunday, November 1, every 3.78L gallon of Hydro Coat, Nano Polymer Spray, Max Pro Shampoo and Deep Cleaning APC comes with the small size free.
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ============ CTA ============ -->
  <tr>
    <td align="center" class="em-pad" style="padding:0 36px 36px 36px;">
{button("SHOP BEFORE SUNDAY")}
    </td>
  </tr>

  <!-- ============ PRODUCTS (recap) ============ -->
  <tr>
    <td class="em-pad" style="padding:0 36px 36px 36px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{grid(full=False)}
      </table>
    </td>
  </tr>
{terms_section()}{FOOTER}"""

Path("email/boatshow-e1/index.html").write_text(e1, encoding="utf-8")
Path("email/boatshow-e2/index.html").write_text(e2, encoding="utf-8")
print(f"e1 index.html: {len(e1)} bytes")
print(f"e2 index.html: {len(e2)} bytes")
