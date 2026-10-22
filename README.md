# Sun Lines — website prototype

First version of the new sunlines.it: today's content, reorganised navigation, the Sun Lines brand (logo, colours, Barlow type), SEO/GEO markup and a mobile-first layout. Italian for now; English is next, and the language menu is built for 5–10 languages.

## Structure

```
docs/                 the built site, served by GitHub Pages
  img/flotta/         fleet photos
  img/destinazioni/   destination photos (Unsplash, free licence)
  img/parcheggio/     car park and camper area photos
  img/README.md       every image: where it is used, source, status
  llms.txt            summary for AI assistants
  sitemap.xml
  robots.txt          preview version: blocks search engines
src/                  the page generator
  build.py            builds everything into docs/
  common.py           contacts, navigation, shared helpers, structured data
  layout.py           styles, header, footer, mobile contact bar
  pages_a.py          Home, Airbus 90, Linee e orari
  pages_b.py          Noleggio bus, Transfer e NCC, Parcheggio, Chi siamo
  pages_c.py          FAQ, Abbonamenti studenti, Assistenza, legal pages, Lavora con noi
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
- Rewrite the privacy policy for GDPR: the current text cites Legislative Decree 196/2003 and names another company.
- Connect the forms (quote, support, complaints, invoice) to email or a form service; in the prototype they validate but do not send.
- Add the English pages under `docs/en/` and set English to available in `LANGS`.
