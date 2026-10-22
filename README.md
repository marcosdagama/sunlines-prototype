# Sun Lines — website prototype

First version of the new sunlines.it: today's content, reorganised navigation, the Sun Lines brand (logo, colours, Barlow type), SEO/GEO markup and a mobile-first layout. Italian only for now; English and German are planned.

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
  assets/             logo files (SVG)
  robots.production.txt   robots rules for the live site
```

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

## Before going live

- Rebuild with `PREVIEW=0` so search engines and AI assistants can index the site.
- Replace the AI-generated fleet photos and the three "Foto da scattare" placeholders.
- Replace the 800 px prototype images with the original high-resolution files.
- Rewrite the privacy policy for GDPR: the current text cites Legislative Decree 196/2003 and names another company.
- Connect the forms (quote, support, complaints, invoice) to email or a form service; in the prototype they validate but do not send.
- Add English and German pages, then their `hreflang` links.
