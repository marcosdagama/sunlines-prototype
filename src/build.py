import os, shutil, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import layout
layout.CSS += """
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.prose .ph,.grid>.ph{border-radius:var(--r-md)}
.form-privacy{margin:0;color:var(--muted)}
.note-box{display:grid;gap:8px;padding:16px;border:1px solid var(--hairline);border-left:4px solid var(--blue);border-radius:var(--r-sm);background:var(--sand)}
.note-box p,.note-box h3{margin:0}
.steps-list{display:grid;gap:10px;padding-left:1.3em;margin:0}
"""
from pages_a import home, airbus, linee
from pages_c import noleggio_autobus, transfer, parcheggio, chi_siamo, faq, abbonamenti, assistenza, lavora
from pages_legal import note_legali, privacy_new as privacy, cookie_policy, diritti, condizioni_trasporto as condizioni, condizioni_vendita, accessibilita, LEGAL_CSS
layout.CSS += LEGAL_CSS + layout.CK_CSS
layout.JS += layout.CK_JS
import hero_carousel, parking_map, forms
layout.CSS += forms.CSS
layout.JS += forms.JS
layout.CSS += parking_map.CSS + """
.partner-btns{display:grid;gap:10px}
.partner-btn{display:flex;align-items:center;gap:14px;min-height:64px;padding:10px 14px;border:1px solid var(--hairline);border-radius:var(--r-md);background:var(--white);color:var(--navy);text-decoration:none}
.partner-btn:hover{border-color:var(--navy);box-shadow:0 2px 8px rgba(11,37,69,.08)}
.partner-btn img{width:40px;height:40px;border-radius:10px;object-fit:contain;flex:none;background:#fff;border:1px solid var(--hairline)}
.partner-btn span{display:grid;flex:1;min-width:0}.partner-btn small{color:var(--muted);font-size:14px}
.partner-btn .i{color:var(--muted);flex:none}
.store-badges{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.store-badges img{display:block;height:46px;width:auto}
.store-badges a:focus-visible{outline:3px solid var(--blue);outline-offset:3px;border-radius:8px}
"""
layout.JS += parking_map.JS
layout.CSS += hero_carousel.CSS
layout.JS += hero_carousel.JS
from common import BASE, EMAIL, PHONE, WA_DISPLAY, PORTAL

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs")
# PREVIEW = True keeps the hosted prototype out of search engines. Set to False for the live site.
PREVIEW = os.environ.get("PREVIEW", "1") != "0"
os.makedirs(OUT, exist_ok=True)
PAGES = {
    "index.html": home, "airbus-olbia-sassari-alghero.html": airbus, "linee-e-orari.html": linee,
    "noleggio-autobus.html": noleggio_autobus, "transfer-ncc.html": transfer, "parcheggio-aeroporto-olbia.html": parcheggio,
    "chi-siamo.html": chi_siamo, "domande-frequenti.html": faq, "abbonamenti-studenti.html": abbonamenti,
    "assistenza.html": assistenza, "condizioni-generali.html": condizioni, "privacy.html": privacy, "lavora-con-noi.html": lavora,
    "condizioni-di-vendita.html": condizioni_vendita, "diritti-dei-passeggeri.html": diritti, "note-legali.html": note_legali,
    "cookie-policy.html": cookie_policy, "accessibilita.html": accessibilita,
    "grazie.html": lambda: forms.grazie_page(layout.page),
}
for fn, fnc in PAGES.items():
    html = fnc()
    if PREVIEW and 'name="robots"' not in html:
        html = html.replace('<meta name="description"', '<meta name="robots" content="noindex, nofollow">\n<meta name="description"', 1)
    open(os.path.join(OUT, fn), "w").write(html)
open(os.path.join(OUT, ".nojekyll"), "w").write("")

up = os.path.join(HERE, "assets")
for f in ["sun-lines-logo.svg", "sun-lines-logo-white.svg", "sun-lines-sun-mark.svg"]:
    shutil.copy(os.path.join(up, f), OUT)

paths = ["/", "/transfer-ncc", "/noleggio-autobus", "/airbus-olbia-sassari-alghero", "/linee-e-orari", "/parcheggio-aeroporto-olbia",
         "/abbonamenti-studenti", "/chi-siamo", "/domande-frequenti", "/assistenza", "/condizioni-generali", "/privacy", "/lavora-con-noi",
         "/condizioni-di-vendita", "/diritti-dei-passeggeri", "/note-legali", "/cookie-policy", "/accessibilita"]
from common import LANGS as _LANGS
paths = paths + [f"/{c}" + p for c, _, ok in _LANGS if ok and c != "it" for p in paths]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}{p}</loc><lastmod>2026-10-22</lastmod></url>\n" for p in paths) + "</urlset>\n")

ROBOTS_LIVE = (f"""# Sun Lines — crawler rules
# Search engines and AI assistants may read all public pages; form endpoints and admin stay private.
User-agent: *
Allow: /
Disallow: /administrator/
Disallow: /api/
Disallow: /*?view=form

# AI assistants: explicitly welcome on public content
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: OAI-SearchBot
User-agent: ClaudeBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: Applebot-Extended
Allow: /
Disallow: /administrator/
Disallow: /api/

Sitemap: {BASE}/sitemap.xml
""")
open(os.path.join(HERE, "robots.production.txt"), "w").write(ROBOTS_LIVE)
open(os.path.join(OUT, "robots.txt"), "w").write("# Preview copy: not for search engines. The live rules are in src/robots.production.txt\nUser-agent: *\nDisallow: /\n" if PREVIEW else ROBOTS_LIVE)

open(os.path.join(OUT, "llms.txt"), "w").write(f"""# Sun Lines

> Sun Lines (Sun Lines Elite Service S.r.l.) is a passenger transport company based in Olbia, Sardinia, operating for over 60 years. It runs public bus lines in Gallura, the Airbus line 90 between Olbia airport, Sassari and Alghero airport, coach hire and private car transfers with driver (NCC), and a car and camper park next to Olbia Costa Smeralda airport.

Last updated: 2026-10-22. Website languages: Italian, with an English version at {BASE}/en/. Contact: phone +39 {PHONE}, email {EMAIL}, support and invoice forms at {BASE}/assistenza. WhatsApp +39 {WA_DISPLAY} is for coach hire and private transfer quotes and long-term or camper parking only; questions about timetables, tickets and luggage are answered at {BASE}/domande-frequenti. Address: Via Pozzo 23, 07026 Olbia (SS), Italy.

## Services

- [Airbus Linea 90 – Olbia, Sassari, Alghero]({BASE}/airbus-olbia-sassari-alghero): Direct bus between Olbia port (Isola Bianca), Olbia centre, Olbia Costa Smeralda airport, Sassari, Alghero Fertilia airport and Alghero centre. Airport to airport in under 2 hours. Runs 15 April to 18 October, including Sundays and holidays. Booking required: buy tickets online ({PORTAL}) up to one hour before departure; on-board purchase costs €5 extra and a seat is not guaranteed. Tickets are not refundable or changeable. One standard bag (50x30x25 cm, max 20 kg) plus one small hand bag included.
- [Linee e orari (public bus lines)]({BASE}/linee-e-orari): Line 20 Olbia – Porto Rotondo – Porto Cervo – Baja Sardinia – Cannigione – Isuledda (1 June to 30 September, daily). Line 30 Olbia – Tempio Pausania – Costa Paradiso – Castelsardo – Porto Torres (1 June to 30 September, daily). Line 50 Olbia – Priatu – Sant'Antonio di Gallura (all year, not on Sundays and holidays). Tickets on board (cash, card where available, with surcharge) or in the Around Sardinia app. No seat reservation. Two bags up to 50x30x25 cm and 20 kg free.
- [Noleggio autobus con conducente (coach hire)]({BASE}/noleggio-autobus): Coaches with driver, 20 and 50 seats, for groups, excursions in Gallura, group airport transfers, school trips, weddings and corporate events anywhere in Sardinia. Free quote, reply within hours.
- [Transfer e NCC (private car with driver)]({BASE}/transfer-ncc): Private transfers from and to Olbia port, Olbia Costa Smeralda airport, hotels and other destinations in Sardinia, on booking.
- [Parcheggio aeroporto Olbia (Promo Parking by Sunlines)]({BASE}/parcheggio-aeroporto-olbia): Guarded, video-monitored car park a 3-minute walk from Olbia Costa Smeralda airport terminal, with direct pedestrian access. Daily rates via Parkingmycar, Parkos and Myparking; 6-month and annual plans via WhatsApp. Camper area with electricity, water and public toilet.
- [Abbonamenti studenti Linea 50]({BASE}/abbonamenti-studenti): Discounted monthly or annual passes for students up to 27, requested online.

## Help

- [Domande frequenti (FAQ)]({BASE}/domande-frequenti): Short answers on which line to take for each destination, Airbus booking, changes and refunds, luggage limits, bikes, children, pets, student passes, parking, lost property, invoices and complaints.
- [Assistenza e contatti]({BASE}/assistenza): Support requests, complaints, invoice requests.
- [Chi siamo]({BASE}/chi-siamo): Company history, founder Luca Cassitta, ISO 9001:2015 and ISO 14001:2015 certifications.
- [Condizioni generali di trasporto]({BASE}/condizioni-generali)
""")
# ---- other languages: translate the built Italian pages (src/i18n.py)
import i18n
from common import LANGS
i18n.fix_italian_lang_menu(LANGS)
for code, _, ok in LANGS:
    if code == "it" or not ok:
        continue
    if not os.path.exists(os.path.join(HERE, "i18n", f"{code}.json")):
        print(f"  {code}: no dictionary yet (src/i18n/{code}.json), skipped"); continue
    missing = i18n.render(code, LANGS)
    if missing:
        json.dump({k: sorted(v) for k, v in missing.items()}, open(os.path.join(HERE, "i18n", f"missing-{code}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"  {code}: {len(PAGES)} pages, {len(missing)} strings still in Italian")
print("built", len(PAGES), "pages into docs/ (preview mode)" if PREVIEW else "pages into docs/ (live mode)")
