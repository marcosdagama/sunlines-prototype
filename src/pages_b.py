from layout import *
from parking_map import parking_map


def form(fid, fields, submit="Invia richiesta", notice="finalita", marketing=False):
    """fields: list of (id, label, type, required) ; type in text,email,tel,number,date,textarea,file"""
    rows = []
    pending = []
    def render(f):
        i, label, typ, req = f
        star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
        r = ' required' if req else ''
        ac = {"email": ' autocomplete="email"', "tel": ' autocomplete="tel"'}.get(typ, '')
        if i.endswith("nome") and typ == "text":
            ac = ' autocomplete="name"'
        if typ == "textarea":
            ctl = f'<textarea id="{fid}-{i}" name="{i}"{r}></textarea>'
        else:
            ctl = f'<input id="{fid}-{i}" name="{i}" type="{typ}"{r}{ac}>'
        return f'<div class="field"><label for="{fid}-{i}">{esc(label)}{star}</label>{ctl}</div>'
    for f in fields:
        if f[2] in ("textarea", "file"):
            if pending:
                rows.append('<div class="field-row">' + "".join(render(p) for p in pending) + '</div>'); pending = []
            rows.append(render(f))
        else:
            pending.append(f)
            if len(pending) == 2:
                rows.append('<div class="field-row">' + "".join(render(p) for p in pending) + '</div>'); pending = []
    if pending:
        rows.append('<div class="field-row">' + "".join(render(p) for p in pending) + '</div>')
    mk = (f'<label class="check" for="{fid}-mkt"><input id="{fid}-mkt" name="marketing" type="checkbox"> <span>Facoltativo: voglio ricevere offerte e novità di Sun Lines via email. Posso revocare il consenso in ogni momento.</span></label>' if marketing else "")
    return f'''<form class="form" id="{fid}" data-proto novalidate>
{"".join(rows)}
{mk}
<p class="form-privacy small">I dati servono solo a rispondere a questa richiesta. Leggi come li trattiamo nell’<a href="privacy.html#{notice}">informativa privacy</a>.</p>
<div class="actions"><button class="btn btn-primary" type="submit">{esc(submit)}</button></div>
<p class="form-note" role="status" hidden></p>
<p class="proto-note"><span class="req">*</span> Campi obbligatori. Il controllo anti-spam “Rispondi prima di inviare” del sito attuale andrà sostituito da un controllo invisibile.</p>
</form>'''


QUOTE_FIELDS = [("nome", "Nome e cognome", "text", True), ("email", "E-mail", "email", True), ("telefono", "Telefono", "tel", False),
                ("persone", "Numero di persone", "number", True), ("data", "Data del servizio", "date", True), ("richiesta", "Richiesta", "textarea", False)]


def noleggio_autobus():
    crumbs = [("Home", "index.html"), ("Noleggio bus", "")]
    body = f'''
<section class="page-hero"><div class="wrap hero-grid">
  <div class="hero-copy">{breadcrumb_html(crumbs)}
    <p class="label eyebrow">Gruppi, scuole, aziende, eventi</p>
    <h1 class="h1">Noleggio autobus con conducente in Sardegna</h1>
    <p class="lead">Sun Lines mette a disposizione autobus con conducente da 20 e 50 posti per gruppi, escursioni in Gallura, transfer aeroportuali collettivi, gite scolastiche, matrimoni ed eventi aziendali in tutta la Sardegna.</p>
    <div class="actions"><a class="btn btn-primary" href="#preventivo">Richiedi un preventivo gratuito</a><a class="btn btn-wa" href="{WA["bus"]}">{icon("chat",18)} Preventivo su WhatsApp</a></div>
  </div>
  {photo("Minibus Mercedes Sun Lines", "attuale", "16/10", eager=True, src="sprinter-costa")}
</div></section>
<section class="section section-white"><div class="wrap grid grid-2" style="align-items:start">
  <div class="prose">
    <h2 class="h2">Un servizio su misura</h2>
    <p>Ogni servizio viene organizzato su misura in base a numero di partecipanti, tratta e durata del noleggio.</p>
    <p>Richiedi un preventivo gratuito compilando il modulo qui sotto. Rispondiamo in poche ore.</p>
  </div>
  <div class="grid grid-2">
    <div class="panel"><p class="label muted">Flotta</p><p class="h2 tnum">20 posti</p><p class="small muted">Minibus per gruppi piccoli, transfer ed escursioni.</p></div>
    <div class="panel"><p class="label muted">Flotta</p><p class="h2 tnum">50 posti</p><p class="small muted">Autobus gran turismo per gruppi, scuole ed eventi.</p></div>
  </div>
</div></section>
<section class="section" id="preventivo"><div class="wrap grid grid-2" style="align-items:start">
  <div class="prose">
    <p class="label eyebrow">Preventivo</p>
    <h2 class="h1">Richiedi un preventivo gratuito</h2>
    <p>Indica numero di persone, data e tratta: ti rispondiamo in poche ore.</p>
    <p>Preferisci scriverci? WhatsApp <strong class="tnum">{WA_DISPLAY}</strong> · Email <strong>{EMAIL}</strong></p>
    <p><a class="btn btn-wa" href="{WA["bus"]}">{icon("chat",18)} Scrivici su WhatsApp</a></p>
  </div>
  <div class="panel">{form("q-bus", QUOTE_FIELDS, notice="t-preventivi", marketing=True)}</div>
</div></section>'''
    svc = {"@type": "Service", "name": "Noleggio autobus con conducente", "serviceType": "Noleggio autobus con conducente", "provider": {"@id": BASE + "/#org"},
           "description": "Autobus con conducente da 20 e 50 posti per gruppi, escursioni in Gallura, transfer aeroportuali collettivi, gite scolastiche, matrimoni ed eventi aziendali in tutta la Sardegna.",
           "areaServed": {"@type": "Place", "name": "Sardegna"}, "audience": {"@type": "Audience", "audienceType": "Gruppi, scuole, aziende, eventi"},
           "offers": {"@type": "Offer", "description": "Preventivo gratuito, risposta in poche ore"}}
    ld = jsonld(ORG, svc, breadcrumb_ld([("Home", "/"), ("Noleggio bus", "/noleggio-autobus")]))
    return page(slug="noleggio-autobus", title="Noleggio autobus con conducente in Sardegna | Sun Lines",
                desc="Noleggio autobus con conducente in Sardegna per gruppi, escursioni, transfer ed eventi. Mezzi da 20 e 50 posti. Richiedi un preventivo gratuito a Sun Lines.",
                canonical_path="/noleggio-autobus", active="bus", body=body, ld=ld, cta=("#preventivo", "Preventivo"), wa="bus")


def transfer():
    crumbs = [("Home", "index.html"), ("Transfer e NCC", "")]
    body = f'''
<section class="page-hero"><div class="wrap hero-grid">
  <div class="hero-copy">{breadcrumb_html(crumbs)}
    <p class="label eyebrow">Noleggio con conducente (NCC)</p>
    <h1 class="h1">Transfer privati e auto con conducente in Sardegna</h1>
    <p class="lead">Sun Lines offre un servizio di noleggio auto con conducente (NCC) a Olbia e in tutta la Sardegna, ideale per trasferimenti privati, viaggi di lavoro e spostamenti personalizzati.</p>
    <div class="actions"><a class="btn btn-primary" href="#preventivo">Richiedi preventivo</a><a class="btn btn-wa" href="{WA["ncc"]}">{icon("chat",18)} Scrivici su WhatsApp</a></div>
  </div>
  {photo("Mercedes Classe V Sun Lines", "attuale", "16/10", eager=True, src="classe-v")}
</div></section>
<section class="section section-white"><div class="wrap grid grid-2" style="align-items:start">
  <div class="prose">
    <h2 class="h2">Da e per porto, aeroporto e hotel</h2>
    <p>Effettuiamo transfer da e per il Porto di Olbia, l’Aeroporto di Olbia Costa Smeralda, hotel, strutture ricettive e altre destinazioni dell’isola. Il servizio viene organizzato su prenotazione, in base alle esigenze del cliente.</p>
  </div>
  <div class="contact-strip" style="grid-template-columns:1fr">
    <div class="cbox"><p class="label muted">WhatsApp</p><p class="val tnum">{WA_DISPLAY}</p></div>
    <div class="cbox"><p class="label muted">Email</p><p class="val">{EMAIL}</p></div>
  </div>
</div></section>
<section class="section" id="preventivo"><div class="wrap grid grid-2" style="align-items:start">
  <div class="prose">
    <p class="label eyebrow">Preventivo</p>
    <h2 class="h1">Richiedi il servizio</h2>
    <p>Per richiedere il servizio usa il modulo oppure, in alternativa, scrivi su WhatsApp al <strong class="tnum">{WA_DISPLAY}</strong> o all’indirizzo <strong>{EMAIL}</strong>.</p>
  </div>
  <div class="panel">{form("q-ncc", QUOTE_FIELDS, notice="t-preventivi", marketing=True)}</div>
</div></section>'''
    svc = {"@type": "TaxiService", "name": "Noleggio auto con conducente (NCC) e transfer", "provider": {"@id": BASE + "/#org"},
           "description": "Transfer privati su prenotazione da e per il Porto di Olbia, l’Aeroporto di Olbia Costa Smeralda, hotel e altre destinazioni della Sardegna.",
           "areaServed": [{"@type": "Place", "name": "Olbia"}, {"@type": "Place", "name": "Sardegna"}]}
    ld = jsonld(ORG, svc, breadcrumb_ld([("Home", "/"), ("Transfer e NCC", "/transfer-ncc")]))
    return page(slug="transfer-ncc", title="Transfer e auto con conducente (NCC) a Olbia | Sun Lines",
                desc="Servizio NCC e transfer privati a Olbia e in Sardegna, da e per porto e aeroporto, hotel e strutture ricettive. Su prenotazione, preventivo via modulo o WhatsApp.",
                canonical_path="/transfer-ncc", active="transfer", body=body, ld=ld, cta=("#preventivo", "Preventivo"), wa="ncc")


def parcheggio():
    crumbs = [("Home", "index.html"), ("Parcheggio", "")]
    body = f'''
<section class="page-hero"><div class="wrap hero-grid">
  <div class="hero-copy">{breadcrumb_html(crumbs)}
    <p class="label eyebrow">Promo Parking by Sunlines</p>
    <h1 class="h1">Parcheggio aeroporto di Olbia</h1>
    <p class="lead">A soli 3 minuti a piedi dall’aeroporto di Olbia Costa Smeralda, con passaggio pedonale diretto per il terminal: la soluzione più comoda per chi parte e vuole lasciare l’auto vicinissima, senza navette o attese.</p>
    <div class="actions"><a class="btn btn-wa" href="{WA["parking"]}">{icon("chat",18)} Tariffe su WhatsApp</a></div>
  </div>
  {photo("Promo Parking: l’area coperta con vista sulla torre di controllo dell’aeroporto di Olbia", "attuale", "16/10", eager=True, src="parcheggio-1")}
</div></section>
<section class="section section-white"><div class="wrap grid grid-2" style="align-items:start">
  <article class="panel" id="auto">
    <h2 class="h2">Parcheggio auto</h2>
    <p>Il parcheggio è custodito e dotato di videosorveglianza.</p>
    <p>Offriamo tariffe giornaliere tramite i principali portali di prenotazione, a prezzi competitivi:</p>
    <div class="partner-btns">
      <a class="partner-btn" href="https://www.parkingmycar.it/parcheggio-aeroporto-olbia-costa-smeralda/promo-parking-sun-lines-0"><img src="img/parcheggio-partner/parkingmycar.svg" alt="" width="40" height="40"><span><strong>ParkingMyCar</strong><small>Prenota su parkingmycar.it</small></span>{icon("external",16)}</a>
      <a class="partner-btn" href="https://parkos.it/"><img src="img/parcheggio-partner/parkos.png" alt="" width="40" height="40"><span><strong>Parkos</strong><small>Prenota su parkos.it</small></span>{icon("external",16)}</a>
      <a class="partner-btn" href="https://www.myparking.it/"><img src="img/parcheggio-partner/myparking.png" alt="" width="40" height="40"><span><strong>MyParking</strong><small>Prenota su myparking.it</small></span>{icon("external",16)}</a>
    </div>
    <p>Sono disponibili anche formule semestrali e annuali: contattaci su WhatsApp al <strong class="tnum">(+39) {WA_DISPLAY}</strong> per tariffe e disponibilità.</p>
  </article>
  <article class="panel" id="camper">
    <h2 class="h2">Parcheggio camper</h2>
    <p>Dal 2021 Sun Lines offre anche un’area attrezzata per la sosta e il pernottamento dei camper, con allaccio elettrico, acqua e bagno pubblico, autorizzata dallo SUAPE del Comune di Olbia.</p>
    <p>Per informazioni e prenotazioni: <strong class="tnum">(+39) {WA_DISPLAY}</strong>.</p>
  </article>
</div></section>
<section class="section"><div class="wrap">
  <div class="sec-head"><h2 class="h2">Le foto della struttura</h2></div>
  <div class="grid grid-3">{"".join(photo(f"Promo Parking e area camper, foto {n}", "attuale", "16/9", src=f"parcheggio-{n}") for n in (2,3,4,5,1))}{photo("Area camper con camper in sosta", "scattare", "16/9")}</div>
</div></section>
{parking_map()}'''
    fac = {"@type": "ParkingFacility", "name": "Promo Parking by Sunlines", "description": "Parcheggio custodito e videosorvegliato a 3 minuti a piedi dall’aeroporto di Olbia Costa Smeralda, con passaggio pedonale diretto per il terminal. Area camper attrezzata con allaccio elettrico, acqua e bagno pubblico.",
           "address": {"@type": "PostalAddress", "streetAddress": "Via dei Fornai 5", "postalCode": "07026", "addressLocality": "Olbia", "addressRegion": "SS", "addressCountry": "IT"},
           "openingHours": "Mo-Su 00:00-23:59", "telephone": "+39 346 320 6740", "parentOrganization": {"@id": BASE + "/#org"},
           "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Custodito", "Videosorveglianza", "Area camper", "Allaccio elettrico camper", "Acqua", "Bagno pubblico"]]}
    ld = jsonld(ORG, fac, breadcrumb_ld([("Home", "/"), ("Parcheggio", "/parcheggio-aeroporto-olbia")]))
    return page(slug="parcheggio", title="Parcheggio aeroporto di Olbia – Promo Parking | Sun Lines",
                desc="Promo Parking by Sunlines: parcheggio custodito a 3 minuti a piedi dall’aeroporto di Olbia, con videosorveglianza. Area camper attrezzata. Tariffe giornaliere, semestrali e annuali.",
                canonical_path="/parcheggio-aeroporto-olbia", active="parking", body=body, ld=ld, cta=("#auto", "Prenota online"), wa="parking")


def chi_siamo():
    crumbs = [("Home", "index.html"), ("Chi siamo", "")]
    body = f'''
<section class="page-hero"><div class="wrap hero-grid">
  <div class="hero-copy">{breadcrumb_html(crumbs)}
    <p class="label eyebrow">Informazioni</p>
    <h1 class="h1">Sun Lines: mobilità e servizi di trasporto in Sardegna</h1>
    <p class="lead">Sun Lines è un’azienda di trasporto passeggeri con sede a Olbia che da oltre 60 anni offre servizi di mobilità in Sardegna.</p>
  </div>
  {photo("Autobus Setra Sun Lines sulla costa", "attuale", "16/10", eager=True, src="setra-costa")}
</div></section>
<section class="section section-white"><div class="wrap prose" style="max-width:72ch">
  <p>Ogni giorno accompagniamo persone, residenti e viaggiatori attraverso soluzioni di trasporto affidabili, comode e pensate per diverse esigenze: dalle linee autobus regionali ai collegamenti aeroportuali, dai servizi turistici ai trasferimenti privati con conducente fino al parking aeroportuale.</p>
  <h2 class="h2">La nostra storia</h2>
  <p>Sun Lines nasce dall’esperienza e dalla visione imprenditoriale di Luca Cassitta, che ha fondato l’azienda con l’obiettivo di creare un servizio di trasporto passeggeri affidabile, attento alle esigenze dei viaggiatori e profondamente legato al territorio. Con passione, determinazione e impegno quotidiano, Luca Cassitta ha guidato la crescita di Sun Lines, trasformandola negli anni in una realtà di riferimento per la mobilità in Sardegna.</p>
  <p>Il suo approccio, basato sulla qualità del servizio, sulla sicurezza dei passeggeri e sull’attenzione alle persone e al territorio, ha contribuito a costruire i valori che ancora oggi caratterizzano l’azienda e ne accompagnano lo sviluppo.</p>
  {photo("Ritratto del fondatore o della famiglia, con foto d’archivio dei primi autobus", "scattare", "16/9")}
  <h2 class="h2">I nostri servizi</h2>
  <p>Nel corso degli anni Sun Lines ha sviluppato una gamma completa di servizi di mobilità per rispondere alle diverse esigenze di chi vive e visita la Sardegna.</p>
  <p>Dalle linee autobus regionali che collegano Olbia con la Gallura e il nord Sardegna, ai collegamenti aeroportuali tra Olbia e Alghero, fino ai servizi di noleggio con conducente, ai bus panoramici turistici e al parcheggio adiacente all’Aeroporto di Olbia.</p>
  <p>Un’offerta pensata per accompagnare ogni tipo di viaggio: dagli spostamenti quotidiani ai trasferimenti privati, dalle esigenze dei gruppi alle esperienze alla scoperta del territorio.</p>
  <h2 class="h2">Esperienza, sicurezza e qualità</h2>
  <p>La sicurezza dei passeggeri e la qualità del servizio sono da sempre una priorità per Sun Lines.</p>
  <p>L’azienda opera secondo standard certificati di gestione della qualità e dell’ambiente, con l’obiettivo di garantire servizi efficienti, puntuali e rispettosi delle esigenze dei viaggiatori.</p>
  <h2 class="h2">Certificazioni</h2>
  <div class="grid grid-2">
    <div class="panel"><p class="h3">ISO 9001:2015</p><p class="small muted">Sistema di gestione della qualità.</p><a class="more" href="{BASE}/pdf/certificazione-ISO-9001-2015.pdf">{icon("file",18)} Scaricala qui</a></div>
    <div class="panel"><p class="h3">ISO 14001:2015</p><p class="small muted">Sistema di gestione ambientale.</p><a class="more" href="{BASE}/pdf/certificazione-ISO-14001-2015.pdf">{icon("file",18)} Scaricala qui</a></div>
  </div>
  <h2 class="h2">Hai bisogno di informazioni?</h2>
  <p><a href="domande-frequenti.html">Consulta la nostra sezione FAQ</a> per trovare rapidamente le risposte alle domande più comuni sui nostri servizi, orari, biglietti e modalità di viaggio. Per ulteriori informazioni puoi contattarci all’email <strong>{EMAIL}</strong>.</p>
</div></section>'''
    about = {"@type": "AboutPage", "name": "Chi siamo – Sun Lines", "about": {"@id": BASE + "/#org"}}
    org = dict(ORG); org["hasCredential"] = [{"@type": "EducationalOccupationalCredential", "name": "ISO 9001:2015 – Sistema di gestione della qualità"}, {"@type": "EducationalOccupationalCredential", "name": "ISO 14001:2015 – Sistema di gestione ambientale"}]
    ld = jsonld(org, about, breadcrumb_ld([("Home", "/"), ("Chi siamo", "/chi-siamo")]))
    return page(slug="chi-siamo", title="Chi siamo – oltre 60 anni di trasporti a Olbia | Sun Lines",
                desc="Sun Lines: azienda di trasporto passeggeri a Olbia da oltre 60 anni, fondata da Luca Cassitta. Linee autobus, Airbus, NCC, bus turistici e parking aeroporto. Certificata ISO 9001 e ISO 14001.",
                canonical_path="/chi-siamo", active=None, body=body, ld=ld)
