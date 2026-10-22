from layout import *
from sardinia_map import map_section  # map section: remove this line and {map_section()} in home() to drop it
from faq_data import group_html, destination_table

PDF20 = BASE + "/pdf/LINEA-20.pdf"
PDF30 = BASE + "/images/pdf/LINEA-30.pdf"
PDF50 = BASE + "/pdf/LINEA-50.pdf"
PDF90 = BASE + "/images/pdf/LINEA-90.pdf"

ALERTS = f'''<div class="alerts">
  <div class="alert"><span class="alert-ic info">{icon("ticket",18)}</span><div><h3>Linea 90 · Corse di ottobre</h3>
    <p>Consulta e prenota le corse disponibili in tempo reale sul nostro portale di vendita.</p>
    <p class="actions" style="margin-top:10px"><a class="btn btn-primary btn-sm" href="{PORTAL}">Consulta e prenota {icon("external",16)}</a></p>
    <p class="small muted" style="margin-top:8px">Informazioni: {EMAIL}</p></div></div>
  <div class="alert"><span class="alert-ic">{icon("alert",18)}</span><div><h3>Linea 90 · Fermata Olbia</h3>
    <p>La fermata <strong>Molo Brin</strong> è temporaneamente spostata in <strong>Viale Isola Bianca 1 (lato Ittiturismo)</strong>.</p></div></div>
  <div class="alert"><span class="alert-ic">{icon("alert",18)}</span><div><h3>Linea 90 · Fermata Alghero</h3>
    <p>Dal <strong>14 al 21 ottobre 2026 compresi</strong>, la fermata di <strong>Via Catalogna 38</strong> è temporaneamente spostata in <strong>Via Catalogna 62 (lato carcere)</strong>.</p></div></div>
</div>'''

SERVICES = [
    ("linee-e-orari.html", "TPL – Autolinee extraurbane", "Linee TPL tra Olbia, Porto Cervo, Porto Torres e Sant’Antonio di Gallura.", "Orari, itinerari e tariffe", "Autobus Irizar Sun Lines al tramonto", "irizar-verde-tramonto"),
    ("airbus-olbia-sassari-alghero.html", "Airbus Olbia – Sassari – Alghero", "Collegamento diretto tra i due aeroporti del nord Sardegna.", "Orari, itinerari e tariffe", "Autobus Setra Sun Lines sulla costa", "setra-costa"),
    ("noleggio-autobus.html", "Noleggio autobus con conducente", "Per gruppi, scuole, aziende ed eventi.", "Richiedi preventivo", "Minibus Mercedes Sun Lines", "sprinter-costa"),
    ("transfer-ncc.html", "Noleggio auto con conducente", "Transfer privati da aeroporto e porto verso ogni destinazione.", "Richiedi preventivo", "Mercedes Classe V Sun Lines", "classe-v"),
]


def home():
    doors = f'''<div class="doors">
  <div class="door"><span class="door-ic">{icon("plane",22)}</span><h2 class="h3">Arrivo in Sardegna</h2>
    <p class="small muted">Dall’aeroporto o dal porto di Olbia verso Sassari, Alghero e la tua destinazione.</p>
    <div class="links"><a href="airbus-olbia-sassari-alghero.html">Airbus Olbia – Sassari – Alghero {icon("arrow",18)}</a><a href="transfer-ncc.html">Transfer privato con conducente {icon("arrow",18)}</a><a href="parcheggio-aeroporto-olbia.html">Parcheggio aeroporto {icon("arrow",18)}</a></div></div>
  <div class="door"><span class="door-ic">{icon("users",22)}</span><h2 class="h3">Organizzo un gruppo</h2>
    <p class="small muted">Autobus da 20 e 50 posti per escursioni, transfer collettivi, scuole, matrimoni ed eventi.</p>
    <div class="links"><a href="noleggio-autobus.html">Noleggio autobus con conducente {icon("arrow",18)}</a><a href="noleggio-autobus.html#preventivo">Richiedi un preventivo {icon("arrow",18)}</a></div></div>
  <div class="door"><span class="door-ic">{icon("route",22)}</span><h2 class="h3">Viaggio in Gallura</h2>
    <p class="small muted">Linee di trasporto pubblico tra Olbia, la Costa Smeralda, Porto Torres e Sant’Antonio di Gallura.</p>
    <div class="links"><a href="linee-e-orari.html">Linee, orari e fermate {icon("arrow",18)}</a><a href="abbonamenti-studenti.html">Abbonamenti studenti {icon("arrow",18)}</a></div></div>
</div>'''
    cards = "".join(f'''<article class="card">{photo(ph, src=img)}<div class="card-body"><h3 class="h3">{esc(t)}</h3><p class="small muted">{esc(d)}</p>
<a class="more" href="{h}">{esc(c)} {icon("arrow",18)}</a></div></article>''' for h, t, d, c, ph, img in SERVICES)
    body = f'''
<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="stripes" aria-hidden="true"></span>
    <h1 class="display">La Sardegna inizia dal viaggio</h1>
    <p class="lead">Da oltre 60 anni colleghiamo Olbia, la Gallura e il nord della Sardegna con servizi di trasporto pubblico e privato. Uniamo aeroporti, porti e le principali destinazioni del territorio, offrendo soluzioni affidabili a residenti e viaggiatori.</p>
    <div class="actions"><a class="btn btn-primary" href="airbus-olbia-sassari-alghero.html#biglietti">{icon("ticket",18)} Biglietti Airbus 90</a><a class="btn btn-outline" href="domande-frequenti.html">{icon("help",18)} Domande rapide</a></div>
  </div>
  {photo("Autobus Sun Lines al porto di Olbia, accanto alla ruota panoramica", "attuale", "4/3", eager=True, src="bus-olbia-ruota")}
</div></section>
<section class="section-tight"><div class="wrap">
  <h2 class="sr-only" style="position:absolute;left:-999px">Scegli il tuo viaggio</h2>
  {doors}
</div></section>
<section class="section section-white" id="servizi"><div class="wrap">
  <div class="sec-head"><p class="label eyebrow">Servizi</p><h2 class="h1">Sun Lines offre una gamma completa di servizi di trasporto in Sardegna</h2></div>
  <div class="grid grid-4">{cards}</div>
  <div class="panel" style="margin-top:20px;grid-template-columns:minmax(0,1fr) auto;align-items:center">
    <div><h3 class="h3">Parcheggio</h3><p class="small muted">Promo Parking by Sunlines, custodito e con videosorveglianza, a 3 minuti a piedi dall’aeroporto di Olbia.</p></div>
    <a class="btn btn-outline" href="parcheggio-aeroporto-olbia.html">Scopri il parcheggio</a></div>
</div></section>
{map_section()}
<section class="section" id="avvisi"><div class="wrap">
  <div class="sec-head"><p class="label eyebrow">Avvisi</p><h2 class="h1">Consulta gli avvisi</h2><p class="muted">Linea 90 (Olbia – Sassari – Alghero)</p></div>
  {ALERTS}
</div></section>
<section class="section-tight section-white"><div class="wrap" style="display:grid;gap:16px">
  <p class="label muted">Associazioni di categoria</p>
  <div class="partners"><span class="partner">ANAV · Associazione Nazionale Autotrasporto Viaggiatori</span><span class="partner">CNA</span><span class="partner">Confcommercio</span></div>
</div></section>'''
    ld = jsonld(ORG, {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Sun Lines", "inLanguage": "it", "publisher": {"@id": BASE + "/#org"}},
                {"@type": "ItemList", "name": "Servizi Sun Lines", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": t, "url": BASE + "/" + h.replace(".html", "")} for i, (h, t, *_ ) in enumerate(SERVICES)]})
    return page(slug="home", title="Sun Lines | La Sardegna inizia dal viaggio",
                desc="Sun Lines: trasporto pubblico e privato con sede a Olbia, per scoprire la Gallura e la Sardegna da oltre 60 anni. Autobus TPL, Airbus Olbia-Sassari-Alghero, NCC e Promo Parking aeroporto.",
                canonical_path="/", active=None, body=body, ld=ld, is_index=False,
                cta=("airbus-olbia-sassari-alghero.html#biglietti", "Biglietti Airbus"))


def airbus():
    crumbs = [("Home", "index.html"), ("Airbus 90", "")]
    body = f'''
<section class="page-hero"><div class="wrap hero-grid">
  <div class="hero-copy">{breadcrumb_html(crumbs)}
    <p class="label eyebrow">Linea 90 · Airbus</p>
    <h1 class="h1">Airbus Linea 90 – Olbia, Sassari e Alghero</h1>
    <p class="lead">L’Airbus Sun Lines (Linea 90) collega Olbia, Sassari e Alghero con un servizio diretto e confortevole, mettendo in comunicazione due importanti aeroporti della Sardegna e i principali centri del nord dell’isola.</p>
    <div class="actions"><a class="btn btn-primary" href="{PORTAL}">{icon("ticket",18)} Prenota il biglietto online {icon("external",16)}</a><a class="btn btn-outline" href="{PDF90}">{icon("file",18)} Orari e fermate (PDF)</a></div>
  </div>
  {photo("Autobus Setra dell’Airbus Linea 90", "attuale", "16/10", eager=True, src="airbus-setra-citta")}
</div></section>
<section class="section section-white"><div class="wrap grid grid-2" style="align-items:start">
  <div class="prose">
    <h2 class="h2">Il collegamento</h2>
    <p>La linea collega il Porto di Olbia Isola Bianca, il centro città e l’Aeroporto di Olbia Costa Smeralda con Sassari, l’Aeroporto di Alghero Fertilia e il centro di Alghero, offrendo una soluzione pratica per chi arriva in Sardegna o deve spostarsi tra la costa nord-est e il nord-ovest dell’isola.</p>
    <p>Il collegamento diretto tra l’Aeroporto di Olbia Costa Smeralda e l’Aeroporto di Alghero Fertilia permette di viaggiare comodamente in meno di 2 ore.</p>
    <p>Il servizio è disponibile su prenotazione, con biglietto acquistabile comodamente online, per organizzare il proprio viaggio in modo semplice e sicuro.</p>
    {photo("Spiaggia vicino ad Alghero in estate", ratio="16/9", src="alghero", credit="Domenico Adornato")}
  </div>
  <div class="panel">
    <p class="label muted">In breve</p>
    <div class="line"><span class="badge b90">90</span><div><p class="h3">Olbia – Sassari – Alghero</p><p class="stops">Porto Isola Bianca · Olbia centro · Aeroporto Olbia Costa Smeralda · Sassari · Aeroporto Alghero Fertilia · Alghero centro</p></div></div>
    <p><span class="pill season">Dal 15 aprile al 18 ottobre, domeniche e festivi compresi</span></p>
    <p class="small">Aeroporto di Olbia → Aeroporto di Alghero in meno di 2 ore.</p>
    <a class="more" href="{PDF90}">{icon("file",18)} Consulta orari e fermate</a>
  </div>
</div></section>
<section class="section" id="biglietti"><div class="wrap">
  <div class="sec-head"><p class="label eyebrow">Biglietti e tariffe</p><h2 class="h1">Modalità di acquisto dei titoli di viaggio</h2></div>
  <div class="grid grid-2" style="align-items:start">
    <div class="panel">
      <p><strong>La Linea 90 è un servizio su prenotazione: il biglietto va acquistato online in anticipo.</strong> È comunque possibile l'acquisto a bordo, con supplemento, ma non è garantita la disponibilità del posto.</p>
      <p class="small muted">La vendita online è disponibile fino a un’ora prima dell’orario di partenza previsto oppure fino al raggiungimento della capienza massima disponibile.</p>
      <div class="actions"><a class="btn btn-primary" href="{PORTAL}">{icon("ticket",18)} Prenota il tuo biglietto online {icon("external",16)}</a></div>
      <p class="small muted">Si apre il portale di vendita Sun Lines, dove scegli la corsa e paghi.</p>
    </div>
    <div style="display:grid;gap:10px">
      <h3 class="h3">Domande rapide</h3>
      {group_html("airbus", ["airbus-bagagli", "airbus-cambi", "airbus-email", "airbus-fermate"])}
      <p class="small"><a href="domande-frequenti.html">Tutte le domande frequenti</a></p>
    </div>
  </div>
</div></section>
<section class="section section-white" id="avvisi"><div class="wrap">
  <div class="sec-head"><p class="label eyebrow">Avvisi</p><h2 class="h2">Avvisi Linea 90</h2></div>
  {ALERTS}
</div></section>
<section class="section-tight"><div class="wrap panel" style="grid-template-columns:minmax(0,1fr) auto;align-items:center">
  <div><h2 class="h3">Lasci l’auto all’aeroporto di Olbia?</h2><p class="small muted">Promo Parking by Sunlines è a 3 minuti a piedi dal terminal, custodito e con videosorveglianza.</p></div>
  <a class="btn btn-outline" href="parcheggio-aeroporto-olbia.html">Parcheggio aeroporto</a>
</div></section>'''
    trip = {"@type": "BusTrip", "name": "Airbus Linea 90 Olbia – Sassari – Alghero", "provider": {"@id": BASE + "/#org"},
            "description": "Collegamento diretto in autobus tra porto e aeroporto di Olbia, Sassari, aeroporto di Alghero Fertilia e Alghero centro. Su prenotazione, biglietto online. In servizio dal 15 aprile al 18 ottobre.",
            "busNumber": "90",
            "departureBusStop": {"@type": "BusStop", "name": "Aeroporto di Olbia Costa Smeralda", "address": {"@type": "PostalAddress", "addressLocality": "Olbia", "addressCountry": "IT"}},
            "arrivalBusStop": {"@type": "BusStop", "name": "Aeroporto di Alghero Fertilia", "address": {"@type": "PostalAddress", "addressLocality": "Alghero", "addressCountry": "IT"}},
            "offers": {"@type": "Offer", "url": PORTAL, "availability": "https://schema.org/InStock", "description": "Biglietto online; acquisto a bordo con supplemento di 5 € senza garanzia del posto."}}
    ld = jsonld(ORG, trip, breadcrumb_ld([("Home", "/"), ("Airbus 90", "/airbus-olbia-sassari-alghero")]))
    return page(slug="airbus", title="Airbus Linea 90 – Olbia, Sassari e Alghero | Sun Lines",
                desc="Collegamento diretto in autobus tra l’aeroporto di Olbia, Sassari e Alghero. Biglietto online, posto garantito. Orari e prenotazione Linea 90.",
                canonical_path="/airbus-olbia-sassari-alghero", active="airbus", body=body, ld=ld,
                cta=(PORTAL, "Prenota biglietto"), og_type="article")


def linee():
    crumbs = [("Home", "index.html"), ("Linee e orari", "")]
    lines = [
        ("20", "Olbia – Porto Cervo – Baja Sardinia – Isuledda", "Attiva dal 1° giugno al 30 settembre, tutti i giorni inclusi domeniche e festivi.",
         "Collega Olbia con le principali località della Costa Smeralda, con fermate lungo il percorso a Porto Rotondo, Marinella, Portisco, Capriccioli, Porto Cervo, Poltu Quatu, Baja Sardinia, Cannigione, La Conia e Isuledda. È possibile salire e scendere anche alle fermate intermedie.", PDF20, ""),
        ("30", "Olbia – Porto Torres", "Attiva dal 1° giugno al 30 settembre, tutti i giorni inclusi domeniche e festivi.",
         "Collega Olbia con Porto Torres e la Costa Paradiso, con fermate lungo il percorso a Calangianus, Tempio Pausania, Aggius, Trinità d’Agultu, Badesi, Valledoria, La Muddizza, Castelsardo, Lu Bagnu e Platamona. È possibile salire e scendere anche alle fermate intermedie.", PDF30, ""),
        ("50", "Olbia – Sant’Antonio di Gallura", "Attiva tutto l’anno, escluse domeniche e festivi.",
         "Collega Olbia con Priatu e Sant’Antonio di Gallura, pensata principalmente per pendolari e residenti.", PDF50, ""),
        ("90", "Airbus Olbia – Sassari – Alghero", "Dal 15 aprile al 18 ottobre, domeniche e festivi compresi.",
         "Servizio su prenotazione con biglietto online. Collega porto, centro e aeroporto di Olbia con Sassari, l’aeroporto di Alghero Fertilia e il centro di Alghero.", PDF90, "b90"),
    ]
    LIMG = {"20": ("Costa Smeralda dall’alto", "costa-smeralda", "Nicolò Canu"), "30": ("Castelsardo", "castelsardo", "Daniel Dorfer"),
            "50": ("Mare e graniti della Gallura, Valle dell’Erica", "gallura-mare", "Massimo Virgilio"), "90": ("Spiaggia vicino ad Alghero in estate", "alghero", "Domenico Adornato")}
    items = "".join(f'''<article class="card" id="linea-{n}">{photo(LIMG[n][0], ratio="16/8", src=LIMG[n][1], credit=LIMG[n][2])}<div class="card-body"><div class="line"><span class="badge {c}">{n}</span><div style="display:grid;gap:8px">
<h3 class="h3">Linea {n} — {esc(name)}</h3><p><span class="pill season">{esc(season)}</span></p><p class="small">{esc(text)}</p>
<div class="actions"><a class="btn btn-outline btn-sm" href="{pdf}">{icon("file",16)} Scarica orari e fermate</a>{'<a class="btn btn-primary btn-sm" href="airbus-olbia-sassari-alghero.html">Pagina Airbus 90</a>' if n=="90" else ""}</div></div></div></div></article>''' for n, name, season, text, pdf, c in lines)
    body = f'''
<section class="page-hero"><div class="wrap hero-grid">
  <div class="hero-copy">{breadcrumb_html(crumbs)}
    <p class="label eyebrow">Trasporto pubblico locale</p>
    <h1 class="h1">Linee e orari in Gallura</h1>
    <p class="lead">Sun Lines gestisce le linee di Trasporto Pubblico Locale (TPL) in concessione con la Regione Sardegna, collegando Olbia — aeroporto, porto e centro città — con le principali località della Gallura. Qui sotto trovi orari, fermate e info utili di ogni linea.</p>
  </div>
  {photo("Autobus Irizar blu sulla Costa Smeralda", "attuale", "16/10", eager=True, src="irizar-blu-costa-smeralda")}
</div></section>
<section class="section section-white"><div class="wrap">
  <div class="sec-head"><h2 class="h2">Consulta gli orari e le fermate aggiornate di tutte le linee Sun Lines</h2></div>
  <div class="grid grid-2">{items}</div>
</div></section>
<section class="section-tight section-white" id="dove"><div class="wrap" style="display:grid;gap:14px">
  <h2 class="h2">Dove vuoi andare?</h2>
  {destination_table()}
</div></section>
<section class="section" id="biglietti"><div class="wrap grid grid-2" style="align-items:start">
  <div class="prose">
    <p class="label eyebrow">Biglietti</p>
    <h2 class="h2">Biglietti linee TPL (Linea 20, Linea 30, Linea 50)</h2>
    <p>È possibile acquistare i titoli di viaggio per corsa semplice:</p>
    <ul><li>A bordo del bus, in contanti e, ove possibile, con carta di credito.</li><li>Mobile Ticketing Online tramite il nuovo canale digitale Around Sardinia.</li></ul>
    <p>Per i titoli acquistati tramite app, il biglietto va acquistato in anticipo e validato al momento della salita a bordo ed esibito in originale nel caso il personale addetto alla controlleria lo richieda, tramite l’app utilizzata per l’acquisto, che dovrà essere usata anche per validare il titolo stesso.</p>
    <p><strong>Attenzione: non sono validi gli screenshot, stampe cartacee di abbonamenti digitali o fotocopie di titoli cartacei. In caso di smarrimento o distruzione non potrà essere rilasciato nessun duplicato.</strong></p>
    <p>Scarica l'app Around Sardinia per info sulla mobilità e acquisto biglietti dallo smartphone.</p>
    <div class="actions"><a class="btn btn-outline btn-sm" href="https://apps.apple.com/it/app/openmove/id945799463">App Store</a><a class="btn btn-outline btn-sm" href="https://play.google.com/store/apps/details?id=com.openmove">Google Play</a><a class="btn btn-outline btn-sm" href="https://sardegna.openmove.com">Versione web</a></div>
    <p class="small">Per maggiori informazioni e per dettagli e istruzioni sull'utilizzo del servizio, visita il sito <a href="https://www.openmove.com/it/app/guida/progetto-around-sardinia/">Sardegna Mobilità</a>.</p>
  </div>
  <div style="display:grid;gap:20px">
    <div class="panel"><h2 class="h3">Abbonamenti studenti</h2><p class="small">Sun Lines offre condizioni agevolate per gli studenti pendolari.</p><a class="more" href="abbonamenti-studenti.html">Consulta l’informativa abbonamenti studenti {icon("arrow",18)}</a></div>
    <div style="display:grid;gap:10px"><h2 class="h3">Domande rapide</h2>{group_html("linee", ["linee-posto", "linee-bagagli", "linee-cambio"])}<p class="small"><a href="domande-frequenti.html">Tutte le domande frequenti</a></p></div>
    <div class="panel"><h2 class="h3">Condizioni di viaggio</h2><p class="small">Per tutte le condizioni di viaggio consulta le <a href="condizioni-generali.html">Condizioni Generali</a> e le <a href="domande-frequenti.html">Domande Frequenti</a>.</p></div>
  </div>
</div></section>'''
    svc = {"@type": "Service", "name": "Trasporto Pubblico Locale in Gallura", "serviceType": "Autolinee extraurbane", "provider": {"@id": BASE + "/#org"},
           "areaServed": [{"@type": "Place", "name": n} for n in ["Olbia", "Porto Cervo", "Baja Sardinia", "Cannigione", "Porto Torres", "Tempio Pausania", "Castelsardo", "Sant’Antonio di Gallura"]],
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Linee", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Linea {n} — {name}", "description": season}} for n, name, season, *_ in lines]}}
    ld = jsonld(ORG, svc, breadcrumb_ld([("Home", "/"), ("Linee e orari", "/linee-e-orari")]))
    return page(slug="linee", title="Linee e orari autobus in Gallura | Sun Lines",
                desc="Autobus da Olbia aeroporto, porto e centro verso Porto Cervo, Cannigione, Porto Torres e Sant’Antonio di Gallura. Orari, fermate e tariffe delle linee 20, 30, 50 e 90.",
                canonical_path="/linee-e-orari", active="linee", body=body, ld=ld,
                cta=("#biglietti", "Biglietti"))
