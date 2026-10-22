# Sun Lines — website prototype

First version of the new sunlines.it: today's content, reorganised navigation, the Sun Lines brand (logo, colours, Barlow type), SEO/GEO markup and a mobile-first layout. Italian for now; English is next, and the language menu is built for 5–10 languages.

## Structure

```
docs/                 the built site, served by GitHub Pages
  img/flotta/         fleet photos
  img/destinazioni/   destination photos (Unsplash, free licence)
  img/parcheggio/     car park and camper area photos
  img/README.md       every image: where it is used, source, status
  fonts/              Barlow 400–700 (woff2, SIL Open Font Licence), served from the site itself
  llms.txt            summary for AI assistants
  sitemap.xml
  robots.txt          preview version: blocks search engines
src/                  the page generator
  build.py            builds everything into docs/
  common.py           contacts, navigation, shared helpers, structured data
  layout.py           styles, header, footer, mobile contact bar
  pages_a.py          Home, Airbus 90, Linee e orari
  pages_b.py          Noleggio bus, Transfer e NCC, Parcheggio, Chi siamo
  pages_c.py          FAQ, Abbonamenti studenti, Assistenza, Lavora con noi
  pages_legal.py      Note legali, Privacy, Cookie policy, Diritti dei passeggeri, Condizioni di trasporto e di vendita, Accessibilità
  cookie_consent.py   cookie banner (Garante 2021 rules); COOKIE_BANNER switches it on or off
  sardinia_map.py     "Dove andiamo" interactive map on the home page (self-contained)
  sardinia_coast.txt  Sardinia coastline for the map (Natural Earth, public domain)
  assets/             logo files (SVG)
  robots.production.txt   robots rules for the live site
```

## Languages

Languages are listed once, in `LANGS` in `src/common.py`: code, name in its own language, and whether its pages exist. The header menu (visible on desktop and mobile), the menu inside the mobile drawer and the `hreflang` links all read from that list.

- A language marked `False` shows in the menu as "in arrivo" and gets no `hreflang`.
- To publish one: add its translated pages under `docs/<code>/` (for example `docs/en/`), then set it to `True` and rebuild.
- Italian stays at the root and is the `x-default`.

## Legal pages and missing company data

Company data lives in `COMPANY` in `src/common.py`. Anything still unknown (share capital, PEC, single shareholder) shows on the site as a yellow "[da completare: …]" marker, and so do the retention periods and terms Sun Lines must confirm in `src/pages_legal.py`. Search the built pages for "da completare" to list what is left.

The registered office and REA come from the current site's Condizioni generali (Via dei Fornai, REA 65706); confirm them on the visura camerale.

The cookie banner is on in the prototype so it can be reviewed. If the live site uses only technical cookies, set `COOKIE_BANNER = False` in `src/cookie_consent.py`: no banner is then required, and the footer "Preferenze cookie" link disappears too.

## Forms

The five forms (bus hire quote, transfer and NCC quote, support, complaints, invoice request) are sent by FormSubmit (formsubmit.co) to info@sunlines.it as a table email, with the form name, page, sender's name and time in the subject. The sender gets an automatic confirmation. Settings are in `src/forms.py`.

- **Activate once:** the first submission from the live site sends an activation email to info@sunlines.it. Click the link in it; until then nothing is delivered.
- **Hide the address:** after activation FormSubmit offers a random alias; put it in `FORM_ACTION` and `FORM_AJAX` so the email address is not in the page source.
- **Invoice form** carries a file, so it posts normally and lands on `grazie.html`; the others send in the background and show the result in place.
- **Spam:** a hidden honeypot field; FormSubmit's captcha is off to keep the form on the page.
- **Switching service:** any service that accepts a form POST and returns JSON works; change the two URLs.

## Map section

The home page has a "Dove andiamo" map with switchable layers (Airbus 90, lines 20/30/50, bus hire and NCC, parking) and a north / whole-island view. Its markup, styles, script and data all live in `src/sardinia_map.py`.

- **Remove it:** delete `{map_section()}` in `home()` and the `from sardinia_map import map_section` line in `src/pages_a.py`, then rebuild.
- **Alt text:** the map's description for screen readers is rebuilt from the layers that are switched on (`LAYER_DESC` in the same file). The list beside the map carries the same information as text.
- **Stop positions** are approximate; ask Sun Lines to confirm them (Priatu especially) before going live.

## Rebuild after editing

```
python3 src/build.py            # preview mode (default): pages carry noindex
PREVIEW=0 python3 src/build.py  # live mode: indexable, real robots.txt
```

Edit text in `src/pages_*.py`, then rebuild. Do not edit files in `docs/` by hand: the next build overwrites them.

## Replace a photo

Put the new file in the same folder with the same name (for example `docs/img/flotta/classe-v.jpg`). No code change needed. Use JPG, about 2000 px on the long side. See `docs/img/README.md` for which photos still need replacing.

## GitHub Pages

Repository Settings → Pages → Build and deployment → Deploy from a branch → `main`, folder `/docs`.

## Tickets: today and later

Today tickets are sold on the external Sun Lines sales portal (sites.bigosolutions.it for the Airbus 90, shop.bigosolutions.it for student passes), exactly as on the current sunlines.it. Every ticket button in the site leads to the "Biglietti" section of the Airbus page (`airbus-olbia-sassari-alghero.html#biglietti`) or straight to the portal, and is marked as an external link.

When on-site ticketing becomes possible, replace the content of that section with the booking widget or checkout. Navigation, the header button and the mobile bar already point there, so nothing else needs to change.

## Before going live

- Rebuild with `PREVIEW=0` so search engines and AI assistants can index the site.
- Replace the AI-generated fleet photos and the three "Foto da scattare" placeholders.
- Replace the 800 px prototype images with the original high-resolution files.
- Fill every "da completare" marker and have the legal pages signed off by Sun Lines' lawyer or accountant.
- Forms: activate FormSubmit (see below) and replace the address in `src/forms.py` with FormSubmit's random alias.
- Add the English pages under `docs/en/` and set English to available in `LANGS`.
