"""Legal and compliance pages: notes, privacy, cookies, passenger rights, terms, accessibility.

Texts are drafts for review by Sun Lines' lawyer or accountant. Data still missing is shown with todo() markers.
"""
from layout import *

UPDATED = "22 ottobre 2026"
ART_SITE = "https://www.autorita-trasporti.it"
ART_FORM = "https://autorita-trasporti.it/wp-content/uploads/2024/04/ART_ReclamiAutobus_UE_181_2011.pdf"
CARTA = BASE + "/pdf/carta-qualita-sunlines.pdf"


def legal_page(*, slug, path, crumb, h1, lead, title, desc, sections, toc=True):
    crumbs = [("Home", "index.html"), (crumb, "")]
    nav = ""
    if toc and len(sections) > 3:
        nav = '<nav class="legal-toc" aria-label="In questa pagina"><p class="label muted">In questa pagina</p><ol>' + "".join(
            f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t, _ in sections) + '</ol></nav>'
    secs = "".join(f'<section id="{sid}" class="legal-sec"><h2 class="h2">{esc(t)}</h2>{html}</section>' for sid, t, html in sections)
    body = f'''
<section class="page-hero"><div class="wrap" style="display:grid;gap:16px">{breadcrumb_html(crumbs)}
  <h1 class="h1">{esc(h1)}</h1><p class="lead">{lead}</p><p class="small muted">Ultimo aggiornamento: {UPDATED}</p></div></section>
<section class="section section-white"><div class="wrap legal-grid">{nav}<div class="prose legal">{secs}</div></div></section>'''
    ld = jsonld(ORG, breadcrumb_ld([("Home", "/"), (crumb, path)]))
    return page(slug=slug, title=title, desc=desc, canonical_path=path, active=None, body=body, ld=ld)


def company_block():
    su = COMPANY.get("socio_unico")
    su_txt = todo("società con socio unico: sì / no") if su is None else ("Società con socio unico" if su else "")
    return f'''<dl class="kv">
<dt>Ragione sociale</dt><dd>{esc(COMPANY["name"])}</dd>
<dt>Sede legale</dt><dd>{co("sede_legale", "sede legale")} {todo("verificare: il sito indica anche Via Pozzo 23, Olbia")}</dd>
<dt>Sede operativa</dt><dd>Via Pozzo 23, 07026 Olbia (SS)</dd>
<dt>Registro delle Imprese</dt><dd>{co("registro", "ufficio del Registro delle Imprese")}</dd>
<dt>Numero REA</dt><dd>{co("rea", "numero REA")}</dd>
<dt>Partita IVA e codice fiscale</dt><dd class="tnum">{COMPANY["piva"]}</dd>
<dt>Capitale sociale</dt><dd>{co("capitale", "capitale sociale versato")}</dd>
{f"<dt>Compagine sociale</dt><dd>{su_txt}</dd>" if su_txt else ""}
<dt>PEC</dt><dd>{co("pec", "indirizzo PEC")}</dd>
<dt>Email</dt><dd>{EMAIL}</dd>
<dt>Telefono</dt><dd class="tnum">+39 {PHONE}</dd>
</dl>'''


# ---------------------------------------------------------------- Note legali
def note_legali():
    s = [
        ("societa", "Dati della società", f"<p>Il sito www.sunlines.it è gestito da:</p>{company_block()}"),
        ("associazioni", "Associazioni", "<p>Sun Lines è associata ad ANAV (Associazione Nazionale Autotrasporto Viaggiatori), CNA e Confcommercio. I loghi delle associazioni sono marchi dei rispettivi titolari e sono usati per indicare l’appartenenza.</p>"),
        ("contenuti", "Contenuti e proprietà intellettuale", "<p>Testi, marchi, logo Sun Lines, grafica e fotografie del sito appartengono a Sun Lines Elite Service S.r.l. o ai rispettivi autori. Non possono essere riprodotti senza autorizzazione scritta, salvo l’uso personale e non commerciale.</p><p>Il carattere tipografico Barlow è distribuito con licenza SIL Open Font License.</p>"),
        ("immagini", "Crediti fotografici", "<p>Le fotografie delle destinazioni sono di Domenico Adornato, Nicolò Canu, Daniel Dorfer e Massimo Virgilio, usate secondo le rispettive licenze. Le altre immagini sono di Sun Lines.</p>"),
        ("responsabilita", "Limitazione di responsabilità", "<p>Orari, tariffe e informazioni pubblicate possono cambiare. Fanno fede gli orari ufficiali in PDF, gli avvisi in corso e le condizioni indicate al momento dell’acquisto. I link a siti esterni, come il portale di vendita dei biglietti, portano a pagine gestite da terzi.</p>"),
        ("documenti", "Altri documenti", '<ul><li><a href="privacy.html">Informativa privacy</a></li><li><a href="cookie-policy.html">Cookie policy</a></li><li><a href="condizioni-generali.html">Condizioni generali di trasporto</a></li><li><a href="condizioni-di-vendita.html">Condizioni di vendita dei biglietti</a></li><li><a href="diritti-dei-passeggeri.html">Diritti dei passeggeri</a></li><li><a href="accessibilita.html">Dichiarazione di accessibilità</a></li></ul>'),
    ]
    return legal_page(slug="note-legali", path="/note-legali", crumb="Note legali", h1="Note legali",
                      lead="Dati societari di Sun Lines Elite Service S.r.l. e condizioni d’uso del sito.",
                      title="Note legali | Sun Lines", desc="Dati societari, sede, REA, partita IVA e condizioni d’uso del sito di Sun Lines Elite Service S.r.l.", sections=s)


# ---------------------------------------------------------------- Privacy
TREAT = [
    ("preventivi", "Richieste di preventivo (noleggio bus, transfer e NCC)", "Nome, email, telefono, dettagli del viaggio",
     "Misure precontrattuali richieste da te (art. 6.1.b GDPR)", f"12 mesi dalla richiesta se non segue un contratto {todo('confermare durata')}"),
    ("assistenza", "Assistenza, reclami e segnalazioni", "Nome, contatti, dati del viaggio, contenuto della richiesta",
     "Esecuzione del contratto di trasporto e obblighi di legge sulla gestione dei reclami (art. 6.1.b e 6.1.c; Reg. UE 181/2011)", f"24 mesi dalla chiusura della pratica {todo('confermare durata')}"),
    ("fattura", "Richiesta fattura", "Dati di fatturazione, partita IVA, codice SDI, dati e copia del biglietto",
     "Obblighi fiscali (art. 6.1.c)", "10 anni, come previsto per le scritture contabili (art. 2220 c.c.)"),
    ("biglietti", "Biglietti e abbonamenti acquistati online", "Dati del passeggero e della prenotazione",
     "Esecuzione del contratto di trasporto (art. 6.1.b) e obblighi fiscali (art. 6.1.c)", "Per la durata del contratto e poi 10 anni per gli obblighi fiscali"),
    ("studenti", "Abbonamenti studenti", "Dati dello studente e del genitore o tutore, certificato di iscrizione, ISEE se richiesto",
     "Esecuzione del contratto (art. 6.1.b) e regole regionali sulle agevolazioni (art. 6.1.c)", f"Durata dell’abbonamento più 10 anni per gli obblighi fiscali {todo('confermare')}"),
    ("parcheggio", "Prenotazione del parcheggio", "Nome, contatti, targa, date di sosta",
     "Esecuzione del contratto (art. 6.1.b)", f"Durata della sosta più 10 anni per gli obblighi fiscali {todo('confermare')}"),
    ("whatsapp", "Messaggi WhatsApp (solo preventivi e parcheggio)", "Numero di telefono, nome del profilo, contenuto dei messaggi",
     "Misure precontrattuali richieste da te (art. 6.1.b)", f"12 mesi dall’ultimo messaggio {todo('confermare durata')}"),
    ("candidature", "Candidature di lavoro", "Curriculum, documenti di guida e di identità, contatti",
     "Valutazione della candidatura su tua richiesta (art. 6.1.b e art. 111-bis D.Lgs. 196/2003)", f"12 mesi dalla ricezione {todo('confermare durata')}"),
    ("marketing", "Offerte e novità (solo se acconsenti)", "Nome ed email",
     "Consenso, facoltativo e revocabile in ogni momento (art. 6.1.a)", "Fino alla revoca del consenso"),
    ("navigazione", "Navigazione del sito", "Indirizzo IP e dati tecnici registrati dal server",
     "Legittimo interesse alla sicurezza e al funzionamento del sito (art. 6.1.f)", f"Massimo 30 giorni {todo('confermare con il fornitore di hosting')}"),
]


def privacy_new():
    rows = "".join(f'<tr id="t-{i}"><th scope="row">{t}</th><td>{d}</td><td>{b}</td><td>{r}</td></tr>' for i, t, d, b, r in TREAT)
    s = [
        ("titolare", "Chi tratta i tuoi dati", f'''<p>Il titolare del trattamento è <strong>{esc(COMPANY["name"])}</strong>, sede legale {co("sede_legale", "sede legale")}, P. IVA {COMPANY["piva"]}.</p>
<p>Per qualsiasi domanda sulla privacy scrivi a <strong>{EMAIL}</strong> {todo("indirizzo dedicato alla privacy, se diverso")} o alla PEC {co("pec", "indirizzo PEC")}.</p>
<p>Responsabile della protezione dei dati (DPO): {todo("nome e contatto del DPO, oppure togliere questa riga se non è nominato")}.</p>'''),
        ("finalita", "Quali dati, perché e per quanto tempo", f'''<p>Raccogliamo solo i dati necessari per ciascun servizio. La tabella indica, per ogni attività, i dati trattati, la base giuridica e per quanto tempo li conserviamo.</p>
<div class="table-wrap" tabindex="0" role="region" aria-label="Tabella dei trattamenti, scorrevole"><table class="legal-table"><caption class="sr-only">Trattamenti di dati personali</caption>
<thead><tr><th scope="col">Attività</th><th scope="col">Dati</th><th scope="col">Base giuridica</th><th scope="col">Conservazione</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Se non fornisci i dati obbligatori dei moduli non possiamo rispondere alla richiesta. I dati facoltativi sono indicati come tali.</p>'''),
        ("particolari", "Dati sulla salute e persone a mobilità ridotta", "<p>Se chiedi assistenza per una disabilità o per mobilità ridotta, potremmo ricevere informazioni sulla tua salute. Le usiamo solo per organizzare l’assistenza, chiediamo il minimo indispensabile e le cancelliamo al termine del viaggio, salvo che servano per un reclamo. La base giuridica è il tuo consenso esplicito (art. 9.2.a GDPR).</p>"),
        ("minori", "Minori", "<p>Gli abbonamenti studenti possono riguardare minorenni. Per i minori di 14 anni la richiesta e il consenso, quando necessario, sono dati dal genitore o tutore, che riceve questa informativa.</p>"),
        ("destinatari", "A chi comunichiamo i dati", f'''<p>I dati non sono diffusi né venduti. Possono riceverli, solo per le finalità indicate:</p>
<ul><li><strong>{PORTAL_PROVIDER}</strong>, che gestisce il portale di vendita di biglietti e abbonamenti {todo("indicare se responsabile del trattamento o titolare autonomo")};</li>
<li>FormSubmit (formsubmit.co), il servizio che inoltra i moduli del sito via email a {EMAIL} {todo("verificare sede del fornitore e garanzie per eventuali trasferimenti fuori dall’UE")};</li>
<li>il fornitore di hosting del sito {todo("nome del fornitore di hosting")};</li>
<li><strong>Meta Platforms Ireland Ltd.</strong>, per i messaggi WhatsApp;</li>
<li>il consulente fiscale e la banca, per fatture e pagamenti;</li>
<li>la Regione Sardegna e gli enti competenti, per le agevolazioni sugli abbonamenti;</li>
<li>autorità pubbliche, quando la legge lo richiede.</li></ul>
<p>I fornitori che trattano dati per nostro conto sono nominati responsabili del trattamento (art. 28 GDPR).</p>'''),
        ("trasferimenti", "Dati fuori dall’Unione Europea", "<p>WhatsApp può trasferire dati negli Stati Uniti. Il trasferimento avviene sulla base dell’EU-U.S. Data Privacy Framework o delle clausole contrattuali standard approvate dalla Commissione europea. Se preferisci, puoi contattarci per telefono o email.</p>"),
        ("diritti", "I tuoi diritti", f'''<p>Puoi chiedere in qualsiasi momento di:</p>
<ul><li>accedere ai tuoi dati e riceverne copia;</li><li>correggerli o completarli;</li><li>cancellarli, quando non servono più o non c’è un obbligo di conservarli;</li><li>limitarne il trattamento;</li><li>riceverli in un formato leggibile da un computer (portabilità);</li><li>opporti ai trattamenti basati sul legittimo interesse;</li><li>revocare il consenso, senza effetti sui trattamenti già fatti.</li></ul>
<p>Scrivi a <strong>{EMAIL}</strong>. Rispondiamo entro un mese. Puoi anche presentare reclamo al <a href="https://www.garanteprivacy.it">Garante per la protezione dei dati personali</a>.</p>'''),
        ("decisioni", "Decisioni automatizzate", "<p>Non prendiamo decisioni basate unicamente su trattamenti automatizzati, profilazione compresa.</p>"),
        ("cookie", "Cookie", '<p>Per i cookie usati dal sito consulta la <a href="cookie-policy.html">cookie policy</a>.</p>'),
    ]
    return legal_page(slug="privacy", path="/privacy", crumb="Privacy", h1="Informativa privacy",
                      lead="Come Sun Lines tratta i dati personali di passeggeri, clienti e candidati, ai sensi degli articoli 13 e 14 del Regolamento UE 2016/679 (GDPR).",
                      title="Informativa privacy | Sun Lines", desc="Informativa sul trattamento dei dati personali di Sun Lines Elite Service S.r.l. ai sensi del GDPR: finalità, basi giuridiche, conservazione e diritti.", sections=s)


# ---------------------------------------------------------------- Cookie policy
def cookie_policy():
    s = [
        ("cosa", "Cosa sono i cookie", "<p>I cookie sono piccoli file che il sito salva sul tuo dispositivo. Alcuni servono a far funzionare il sito, altri, solo con il tuo consenso, a misurare le visite o a mostrare pubblicità.</p>"),
        ("usati", "Cookie usati da questo sito", f'''<div class="table-wrap" tabindex="0" role="region" aria-label="Tabella dei cookie, scorrevole"><table class="legal-table"><caption class="sr-only">Cookie del sito</caption>
<thead><tr><th scope="col">Nome</th><th scope="col">Tipo</th><th scope="col">A cosa serve</th><th scope="col">Durata</th></tr></thead>
<tbody><tr><th scope="row"><code>sl_consent</code></th><td>Tecnico, di prima parte</td><td>Ricorda le tue scelte sui cookie</td><td>6 mesi</td></tr>
<tr><th scope="row">Statistiche</th><td>Analitico</td><td>Nessuno strumento attivo al momento {todo("indicare lo strumento se verrà aggiunto")}</td><td>—</td></tr>
<tr><th scope="row">Marketing</th><td>Profilazione</td><td>Nessuno strumento attivo al momento</td><td>—</td></tr></tbody></table></div>
<p>Il sito non usa servizi esterni che installano cookie: il carattere tipografico e la mappa sono ospitati sul sito stesso.</p>'''),
        ("consenso", "Come gestire il consenso", '''<p>Alla prima visita un banner ti chiede se accettare i cookie non necessari. Puoi accettarli, rifiutarli o scegliere per categoria. Chiudere il banner con la X equivale a rifiutare. Lo scorrimento della pagina non vale come consenso.</p>
<p>Ti chiediamo di nuovo il consenso dopo 6 mesi o se cambiano gli strumenti usati. Puoi cambiare idea in ogni momento:</p>
<p><button type="button" class="btn btn-outline btn-sm" data-cookie-prefs>Apri le preferenze cookie</button></p>
<p>Puoi anche cancellare o bloccare i cookie dalle impostazioni del tuo browser.</p>'''),
        ("esterni", "Siti esterni", f"<p>Il portale di vendita dei biglietti, WhatsApp, Facebook e Instagram sono siti esterni con le proprie cookie policy, che si applicano quando li visiti.</p>"),
        ("privacy", "Titolare e diritti", f'<p>Il titolare è {esc(COMPANY["name"])}. Per i tuoi diritti consulta l’<a href="privacy.html">informativa privacy</a>.</p>'),
    ]
    return legal_page(slug="cookie", path="/cookie-policy", crumb="Cookie policy", h1="Cookie policy",
                      lead="Quali cookie usa il sito di Sun Lines e come scegliere quali accettare.",
                      title="Cookie policy | Sun Lines", desc="Cookie policy del sito Sun Lines: cookie tecnici, statistiche e marketing, e come gestire il consenso.", sections=s)


# ---------------------------------------------------------------- Passenger rights
def diritti():
    s = [
        ("ambito", "A quali viaggi si applicano", f'''<p>Il Regolamento UE 181/2011 tutela chi viaggia su servizi regolari di autobus. Tutte le linee Sun Lines, Airbus 90 compreso, coprono distanze inferiori a 250 km: per questi viaggi valgono i diritti elencati qui sotto.</p>
<p>Le linee di trasporto pubblico locale seguono anche la <a href="{CARTA}">Carta della qualità dei servizi Sun Lines</a> (PDF), che indica standard di qualità, rimborsi e reclami.</p>'''),
        ("diritti", "I tuoi diritti", '''<ul>
<li><strong>Nessuna discriminazione</strong>: tariffe e condizioni non cambiano in base alla nazionalità o al luogo di acquisto.</li>
<li><strong>Persone con disabilità o a mobilità ridotta</strong>: possono prenotare e viaggiare senza costi aggiuntivi. L’accesso può essere rifiutato solo se il veicolo o le fermate non consentono un trasporto sicuro; in quel caso ti spieghiamo il motivo.</li>
<li><strong>Ausili per la mobilità</strong>: in caso di perdita o danno a una sedia a rotelle o a un altro ausilio per colpa del vettore, hai diritto al risarcimento.</li>
<li><strong>Incidenti</strong>: in caso di incidente hai diritto al risarcimento per morte, lesioni, perdita o danno al bagaglio, e all’assistenza immediata.</li>
<li><strong>Informazioni</strong>: hai diritto a informazioni adeguate per tutto il viaggio e su questi diritti, anche in formati accessibili.</li>
<li><strong>Reclami</strong>: puoi presentare un reclamo e ricevere una risposta definitiva entro 3 mesi.</li></ul>
<p>Rimborsi o assistenza per ritardi e cancellazioni previsti dal Regolamento valgono solo per i viaggi di 250 km o più. Per le nostre linee si applicano le regole della Carta della qualità dei servizi e delle <a href="condizioni-generali.html">Condizioni generali di trasporto</a>.</p>'''),
        ("assistenza", "Assistenza per mobilità ridotta", f'''<p>Per viaggiare con una sedia a rotelle o chiedere assistenza, contattaci prima della partenza al <strong class="tnum">+39 {PHONE}</strong> o a <strong>{EMAIL}</strong>.</p>
<p>{todo("indicare quali autobus sono accessibili e con quanto anticipo chiedere l’assistenza")}</p>'''),
        ("reclami", "Come presentare un reclamo", f'''<ol><li>Scrivici con il <a href="assistenza.html#reclami">modulo reclami</a> o a {EMAIL} entro 3 mesi dalla data del viaggio.</li>
<li>Confermiamo la ricezione entro un mese e ti diamo una risposta definitiva entro 3 mesi.</li>
<li>Se non rispondiamo entro 3 mesi o la risposta non ti soddisfa, puoi rivolgerti all’Autorità di Regolazione dei Trasporti.</li></ol>'''),
        ("art", "Autorità di Regolazione dei Trasporti", f'''<p>L’ART è l’organismo nazionale che vigila sui diritti dei passeggeri in autobus. Puoi inviare un reclamo gratuitamente con il sistema online SiTe o con il <a href="{ART_FORM}">modulo ART</a> (PDF), via PEC o raccomandata.</p>
<p><strong>Autorità di Regolazione dei Trasporti</strong><br>Via Nizza 230, 10126 Torino<br><a href="{ART_SITE}">www.autorita-trasporti.it</a></p>'''),
    ]
    return legal_page(slug="diritti", path="/diritti-dei-passeggeri", crumb="Diritti dei passeggeri", h1="Diritti dei passeggeri",
                      lead="I diritti di chi viaggia sulle linee Sun Lines secondo il Regolamento UE 181/2011, e come presentare un reclamo.",
                      title="Diritti dei passeggeri in autobus | Sun Lines", desc="Diritti dei passeggeri sulle linee Sun Lines (Reg. UE 181/2011): mobilità ridotta, incidenti, informazioni, reclami e Autorità di Regolazione dei Trasporti.", sections=s)


# ---------------------------------------------------------------- Carriage terms
def condizioni_trasporto():
    s = [
        ("premessa", "Premessa", f'''<p>Queste condizioni regolano il trasporto di passeggeri su autobus effettuato da {esc(COMPANY["name"])}, sede legale {co("sede_legale", "sede legale")}, P. IVA {COMPANY["piva"]}, REA {co("rea", "numero REA")}, tel. +39 {PHONE}, email {EMAIL}.</p>
<p>L’acquisto dei biglietti è regolato dalle <a href="condizioni-di-vendita.html">Condizioni di vendita</a>. I diritti dei passeggeri sono riassunti nella pagina <a href="diritti-dei-passeggeri.html">Diritti dei passeggeri</a>. Le linee di trasporto pubblico locale seguono anche la <a href="{CARTA}">Carta della qualità dei servizi</a> (PDF).</p>'''),
        ("viaggio", "Il viaggio", '''<ul><li>Presentati alla fermata almeno 10 minuti prima della partenza e mostra il biglietto all’autista.</li>
<li>Resta seduto mentre il bus è in movimento e allaccia la cintura dove presente.</li>
<li>A bordo è vietato fumare, anche sigarette elettroniche, e bere alcolici.</li>
<li>L’autista può rifiutare il trasporto a chi mette a rischio la sicurezza o disturba gli altri passeggeri.</li></ul>'''),
        ("bagagli", "Bagagli", '''<ul><li>Airbus 90: 1 valigia fino a 50×30×25 cm e 20 kg, più 1 borsa o zaino piccolo a bordo. Bagagli in più o speciali si aggiungono a pagamento durante l’acquisto online.</li>
<li>Non sono ammessi merci pericolose, materiali esplosivi o infiammabili e liquidi in genere.</li>
<li>Gli oggetti lasciati a bordo vanno segnalati all’<a href="assistenza.html#assistenza">assistenza</a> con linea, data, orario e descrizione.</li></ul>'''),
        ("bambini", "Bambini e minori", f'''<p>I bambini piccoli viaggiano nel proprio seggiolino, fissato alle cinture del bus e portato dal genitore o accompagnatore. {todo("età minima per viaggiare da soli e condizioni")}</p>'''),
        ("animali", "Animali", f'''<p>Non sono ammessi animali oltre 40 kg. {todo("regole per animali piccoli: trasportino, costo, cani guida")}</p>'''),
        ("ritardi", "Ritardi, cancellazioni e variazioni", f'''<p>Orari e fermate possono cambiare per traffico, maltempo o lavori: le variazioni sono pubblicate negli avvisi del sito. Le regole su rimborsi e indennizzi sono quelle della <a href="{CARTA}">Carta della qualità dei servizi</a> e, per i biglietti online, delle <a href="condizioni-di-vendita.html">Condizioni di vendita</a>.</p>'''),
        ("responsabilita", "Responsabilità", "<p>Sun Lines risponde dei danni a persone e bagagli secondo il Codice civile e il Regolamento UE 181/2011. Non risponde di oggetti di valore lasciati incustoditi a bordo.</p>"),
        ("reclami", "Reclami", '<p>Puoi presentare un reclamo entro 3 mesi dal viaggio con il <a href="assistenza.html#reclami">modulo reclami</a>. Procedura e tempi sono descritti nella pagina <a href="diritti-dei-passeggeri.html#reclami">Diritti dei passeggeri</a>.</p>'),
    ]
    return legal_page(slug="condizioni", path="/condizioni-generali", crumb="Condizioni di trasporto", h1="Condizioni generali di trasporto",
                      lead="Le regole del viaggio sugli autobus Sun Lines: a bordo, bagagli, minori, animali, ritardi e responsabilità.",
                      title="Condizioni generali di trasporto | Sun Lines", desc="Condizioni generali di trasporto passeggeri di Sun Lines Elite Service S.r.l.: bagagli, minori, animali, ritardi, responsabilità e reclami.", sections=s)


# ---------------------------------------------------------------- Sales terms
def condizioni_vendita():
    s = [
        ("acquisto", "Dove si comprano i biglietti", f'''<p>I biglietti dell’Airbus 90 e gli abbonamenti si acquistano sul portale di vendita Sun Lines, gestito da {PORTAL_PROVIDER}. Il portale applica anche le proprie condizioni e la propria informativa privacy, mostrate prima del pagamento.</p>
<p><a href="{PORTAL}">Portale biglietti</a> · <a href="{SHOP}">Portale abbonamenti</a></p>'''),
        ("prezzi", "Prezzi", f'''<p>I prezzi indicati sul portale sono finali e comprendono l’IVA. Eventuali bagagli aggiuntivi o servizi extra sono mostrati prima del pagamento.</p>
<p>A bordo dell’Airbus 90 si può pagare con un supplemento di 5 €, solo se ci sono posti liberi. {todo("tariffe in vigore o link al tariffario")}</p>'''),
        ("prenotazione", "Prenotazione e posto", "<p>La vendita online chiude 1 ora prima della partenza o quando i posti finiscono. Il biglietto online garantisce il posto sulla corsa scelta.</p>"),
        ("modifiche", "Modifiche e rimborsi", f'''<p>I biglietti della Linea 90 non si modificano e non si rimborsano. Se non ti presenti alla partenza il biglietto è perso. Controlla data, orario e fermata prima di pagare.</p>
<p>Se la corsa è cancellata da Sun Lines, {todo("indicare rimborso o riprotezione")}.</p>'''),
        ("recesso", "Diritto di recesso", "<p>Il diritto di recesso di 14 giorni non si applica ai biglietti di trasporto con data e ora di partenza stabilite (art. 59, comma 1, lettera n, del Codice del Consumo).</p>"),
        ("fattura", "Fattura", '<p>Puoi chiedere la fattura con il <a href="assistenza.html#fattura">modulo richiesta fattura</a>, indicando numero del biglietto e codice SDI.</p>'),
        ("preventivi", "Noleggio bus, transfer e NCC", f'''<p>I preventivi per noleggio autobus, transfer e auto con conducente non sono vincolanti finché Sun Lines non conferma per iscritto il servizio. {todo("condizioni di pagamento, acconto e cancellazione")}</p>'''),
        ("controversie", "Reclami e controversie", f'''<p>Per i reclami segui la procedura nella pagina <a href="diritti-dei-passeggeri.html#reclami">Diritti dei passeggeri</a>. Per le controversie con i consumatori è competente il foro del luogo di residenza del consumatore.</p>'''),
    ]
    return legal_page(slug="vendita", path="/condizioni-di-vendita", crumb="Condizioni di vendita", h1="Condizioni di vendita dei biglietti",
                      lead="Come si comprano biglietti e abbonamenti Sun Lines: prezzi, prenotazione, modifiche, rimborsi e fattura.",
                      title="Condizioni di vendita dei biglietti | Sun Lines", desc="Condizioni di vendita di biglietti e abbonamenti Sun Lines: acquisto online, prezzi, modifiche, rimborsi, recesso e fattura.", sections=s)


# ---------------------------------------------------------------- Accessibility statement
def accessibilita():
    s = [
        ("impegno", "Il nostro impegno", f"<p>{esc(COMPANY['name'])} vuole che il sito www.sunlines.it e l’acquisto dei biglietti siano utilizzabili da tutti, comprese le persone con disabilità. Questa dichiarazione è redatta ai sensi del D.Lgs. 82/2022, che recepisce la Direttiva UE 2019/882 (European Accessibility Act).</p>"),
        ("servizio", "Il servizio", f"<p>Il sito offre informazioni su linee, orari, Airbus 90, noleggio, transfer e parcheggio, moduli di contatto e collegamenti al portale di vendita dei biglietti gestito da {PORTAL_PROVIDER}.</p>"),
        ("misure", "Come rendiamo accessibile il sito", '''<ul><li>Struttura con titoli, punti di riferimento e un link per saltare al contenuto.</li>
<li>Tutto il sito si usa con la tastiera, con il focus sempre visibile.</li>
<li>Contrasto dei colori conforme al livello AA.</li>
<li>Testi alternativi per immagini e mappa, con le stesse informazioni anche in forma di elenco.</li>
<li>Moduli con etichette, campi obbligatori indicati e messaggi di errore chiari.</li>
<li>Pulsanti e link di almeno 44 pixel sugli schermi touch.</li>
<li>Animazioni ridotte quando il dispositivo lo richiede.</li></ul>'''),
        ("conformita", "Stato di conformità", f'''<p>Il sito è <strong>parzialmente conforme</strong> alle WCAG 2.1 livello AA e alla norma EN 301 549. Ultima verifica: {UPDATED}, controllo automatico di tutte le pagine {todo("data e esito della verifica manuale o dell’audit esterno")}.</p>
<p>Limiti noti:</p>
<ul><li>Gli orari delle linee sono in PDF che potrebbero non essere accessibili. Su richiesta li forniamo in altro formato.</li>
<li>Il portale di vendita è gestito da {PORTAL_PROVIDER} {todo("link alla dichiarazione di accessibilità del portale")}.</li></ul>'''),
        ("segnala", "Segnala un problema", f'''<p>Se trovi una barriera o ti serve un contenuto in un altro formato, scrivi a <strong>{EMAIL}</strong> o chiama il <strong class="tnum">+39 {PHONE}</strong>. Rispondiamo entro 30 giorni.</p>'''),
        ("vigilanza", "Autorità di vigilanza", '''<p>Se la risposta non è soddisfacente puoi rivolgerti all’Agenzia per l’Italia Digitale (AgID), che vigila sull’applicazione della normativa: <a href="https://www.agid.gov.it">www.agid.gov.it</a>.</p>'''),
    ]
    return legal_page(slug="accessibilita", path="/accessibilita", crumb="Accessibilità", h1="Dichiarazione di accessibilità",
                      lead="Come rendiamo il sito Sun Lines utilizzabile da tutti, i limiti noti e come segnalarci un problema.",
                      title="Dichiarazione di accessibilità | Sun Lines", desc="Dichiarazione di accessibilità del sito Sun Lines ai sensi del D.Lgs. 82/2022 (European Accessibility Act): conformità WCAG 2.1 AA, limiti e contatti.", sections=s)


LEGAL_CSS = """
/* legal pages */
.legal-grid{display:grid;gap:32px}
@media (min-width:960px){.legal-grid{grid-template-columns:240px minmax(0,1fr);align-items:start}.legal-toc{position:sticky;top:96px}}
.legal-toc{display:grid;gap:8px;padding:16px;border:1px solid var(--hairline);border-radius:var(--r-md);background:var(--sand)}
.legal-toc ol{margin:0;padding-left:1.2em;display:grid;gap:6px;font-size:15px}
.legal-sec{display:grid;gap:12px;scroll-margin-top:96px}
.legal .legal-sec+.legal-sec{padding-top:20px;border-top:1px solid var(--hairline)}
.kv{display:grid;grid-template-columns:minmax(0,200px) minmax(0,1fr);gap:8px 16px;margin:0}
.kv dt{font-weight:600}.kv dd{margin:0}
@media (max-width:599px){.kv{grid-template-columns:1fr}.kv dd{margin-bottom:8px}}
.table-wrap{overflow-x:auto;max-width:100%}.table-wrap:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.legal-table{border-collapse:collapse;width:100%;min-width:640px;font-size:15px}
.legal-table th,.legal-table td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--hairline)}
.legal-table thead th{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);background:var(--sand)}
.legal-table tbody th{font-weight:600}
mark.todo{background:#FFF1D6;color:#6B3E00;border:1px dashed #D99A2B;border-radius:3px;padding:0 4px;font-weight:600;font-size:.9em}
"""
