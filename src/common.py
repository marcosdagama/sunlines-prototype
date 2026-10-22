import json, html

BASE = "https://www.sunlines.it"
PHONE = "0789 50885"
PHONE_INTL = "+39078950885"
WA_DISPLAY = "346 320 6740"
WA_NUM = "393463206740"
EMAIL = "info@sunlines.it"
PORTAL = "https://sites.bigosolutions.it/sunlines/it"
SHOP = "https://shop.bigosolutions.it/sunlines/"
FB = "https://www.facebook.com/sunlinesbus"
IG = "https://www.instagram.com/sunlinesbus"

WA = {
    "general": "https://wa.me/393463206740?text=Ciao%20Sun%20Lines%2C%20ho%20una%20domanda%3A%20",
    "bus": "https://wa.me/393463206740?text=Ciao%20Sun%20Lines%2C%20vorrei%20un%20preventivo%20per%20un%20autobus%20con%20conducente.%0ANumero%20di%20persone%3A%20%0AData%3A%20%0APartenza%20da%3A%20%0ADestinazione%3A%20%0ANote%3A%20",
    "ncc": "https://wa.me/393463206740?text=Ciao%20Sun%20Lines%2C%20vorrei%20un%20preventivo%20per%20un%27auto%20con%20conducente.%0APasseggeri%3A%20%0AData%20e%20ora%3A%20%0ARitiro%3A%20%0ADestinazione%3A%20",
    "airbus": "https://wa.me/393463206740?text=Ciao%20Sun%20Lines%2C%20ho%20una%20domanda%20sull%27Airbus%20Olbia%E2%80%93Sassari%E2%80%93Alghero%20%28linea%2090%29%3A%20",
    "parking": "https://wa.me/393463206740?text=Ciao%20Sun%20Lines%2C%20vorrei%20informazioni%20sul%20parcheggio.%0ADal%3A%20%0AAl%3A%20%0AVeicolo%20%28auto%20/%20camper%29%3A%20",
}

# Languages: add one line per language. available=True once its pages exist under /<code>/ ; the menu and hreflang follow this list.
LANGS = [
    ("it", "Italiano", True),
    ("en", "English", False),
]
CURRENT_LANG = "it"

NAV = [
    ("transfer-ncc.html", "Transfer e NCC", "transfer"),
    ("noleggio-autobus.html", "Noleggio bus", "bus"),
    ("airbus-olbia-sassari-alghero.html", "Airbus 90", "airbus"),
    ("linee-e-orari.html", "Linee e orari", "linee"),
    ("parcheggio-aeroporto-olbia.html", "Parcheggio", "parking"),
]

ORG = {
    "@type": "LocalBusiness",
    "@id": BASE + "/#org",
    "name": "Sun Lines",
    "legalName": "Sun Lines Elite Service S.r.l.",
    "slogan": "La Sardegna inizia dal viaggio",
    "description": "Azienda di trasporto passeggeri con sede a Olbia, attiva da oltre 60 anni: linee di trasporto pubblico locale in Gallura, Airbus Olbia–Sassari–Alghero, noleggio autobus e auto con conducente, parcheggio vicino all'aeroporto di Olbia.",
    "url": BASE + "/",
    "logo": BASE + "/sun-lines-logo.svg",
    "telephone": "+39 0789 50885",
    "email": EMAIL,
    "vatID": "IT00358880904",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Pozzo 23", "postalCode": "07026", "addressLocality": "Olbia", "addressRegion": "SS", "addressCountry": "IT"},
    "founder": {"@type": "Person", "name": "Luca Cassitta"},
    "areaServed": [{"@type": "Place", "name": "Olbia"}, {"@type": "Place", "name": "Gallura"}, {"@type": "Place", "name": "Sardegna"}],
    "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": "+39 346 320 6740", "email": EMAIL, "availableLanguage": ["it"]}],
    "memberOf": [{"@type": "Organization", "name": "ANAV"}, {"@type": "Organization", "name": "CNA"}, {"@type": "Organization", "name": "Confcommercio"}],
    "sameAs": [FB, IG],
}

def esc(s):
    return html.escape(s, quote=True)

# ---------- icons (simple line icons, 24px grid) ----------
def icon(name, size=20):
    p = {
        "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
        "chat": '<path d="M3 20l1.3-3.9A8 8 0 1 1 7.9 19.7L3 20"/><path d="M9 10h.01M12 10h.01M15 10h.01"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "close": '<path d="M6 6l12 12M18 6L6 18"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
        "file": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/>',
        "ticket": '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z"/><path d="M13 7v10"/>',
        "alert": '<path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17h.01"/>',
        "plane": '<path d="M3 13l18-7-5 14-4-6z"/><path d="M12 14l-3 3"/>',
        "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>',
        "route": '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5"/>',
        "mail": '<path d="M3 6h18v12H3z"/><path d="M3 7l9 6 9-6"/>',
        "pin": '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12"/><circle cx="12" cy="9" r="2.5"/>',
        "check": '<path d="M5 12l4 4 10-10"/>',
        "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5V14M12 17h.01"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
        "chev": '<path d="M6 9l6 6 6-6"/>',
        "fb": '<path d="M14 21v-7.5h2.6l.4-3H14V8.6c0-.9.3-1.6 1.6-1.6H17V4.3A19 19 0 0 0 14.9 4C12.6 4 11 5.4 11 8v2.5H8.5v3H11V21"/>',
        "ig": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17 7h.01"/>',
        "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
        "external": '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v6H4V6h6"/>',
    }[name]
    return f'<svg class="i" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

IMGDIR = {'bus-olbia-ruota': 'flotta', 'setra-costa': 'flotta', 'sprinter-costa': 'flotta', 'classe-v': 'flotta', 'irizar-blu-costa-smeralda': 'flotta', 'irizar-verde-tramonto': 'flotta', 'airbus-setra-citta': 'flotta', 'setra-mare': 'flotta', 'abbonamenti-studenti': 'flotta', 'alghero': 'destinazioni', 'costa-smeralda': 'destinazioni', 'castelsardo': 'destinazioni', 'gallura-mare': 'destinazioni', 'parcheggio-1': 'parcheggio', 'parcheggio-2': 'parcheggio', 'parcheggio-3': 'parcheggio', 'parcheggio-4': 'parcheggio', 'parcheggio-5': 'parcheggio'}

def photo(caption, kind="attuale", ratio="16/10", eager=False, src=None, credit=None):
    if src:
        cr = f'<figcaption class="credit">Foto: {esc(credit)}</figcaption>' if credit else ""
        return (f'<figure class="pic" style="aspect-ratio:{ratio}"><img src="img/{IMGDIR[src]}/{src}.jpg" alt="{esc(caption)}" width="800" height="450" '
                f'loading="{"eager" if eager else "lazy"}" decoding="async">{cr}</figure>')
    """Branded placeholder for a photo slot.
    kind='attuale': the current site's photo goes here; 'scattare': photo to be shot."""
    label = "Foto attuale" if kind == "attuale" else "Foto da scattare"
    cls = "ph" + (" ph-shoot" if kind != "attuale" else "")
    return (f'<figure class="{cls}" style="aspect-ratio:{ratio}" role="img" aria-label="{esc(label)}: {esc(caption)}">'
            f'<span class="ph-sun" aria-hidden="true"></span>'
            f'<figcaption><span class="ph-tag">{icon("camera",16)} {label}</span><span class="ph-cap">{esc(caption)}</span></figcaption></figure>')

def jsonld(*objs):
    graph = {"@context": "https://schema.org", "@graph": list(objs)}
    return '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False) + '</script>'

def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

def breadcrumb_html(items):
    parts = []
    for i, (name, href) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            parts.append(f'<li><a href="{href}">{esc(name)}</a></li>')
    return '<nav class="crumbs" aria-label="Percorso"><ol>' + "".join(parts) + '</ol></nav>'
