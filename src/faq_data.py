"""Quick-answer FAQ. Each answer: a one-line short answer first, then the useful detail, then the next step.
Only facts published by Sun Lines; where a figure is not public (fares, exact times) the answer points to the source."""
import re
from common import *

PDF = {"20": BASE + "/pdf/LINEA-20.pdf", "30": BASE + "/images/pdf/LINEA-30.pdf", "50": BASE + "/pdf/LINEA-50.pdf", "90": BASE + "/images/pdf/LINEA-90.pdf"}

# Destination -> line finder (from the published line descriptions)
DESTINATIONS = [
    ("Aeroporto di Alghero, Alghero, Sassari", "90", "15 aprile – 18 ottobre, tutti i giorni", "airbus-olbia-sassari-alghero.html"),
    ("Porto Rotondo, Marinella, Portisco, Capriccioli", "20", "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-20"),
    ("Porto Cervo, Poltu Quatu, Baja Sardinia", "20", "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-20"),
    ("Cannigione, La Conia, Isuledda", "20", "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-20"),
    ("Calangianus, Tempio Pausania, Aggius", "30", "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-30"),
    ("Costa Paradiso, Trinità d’Agultu, Badesi, Valledoria", "30", "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-30"),
    ("Castelsardo, Lu Bagnu, Platamona, Porto Torres", "30", "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-30"),
    ("Priatu, Sant’Antonio di Gallura", "50", "Tutto l’anno, dal lunedì al sabato (non festivi)", "linee-e-orari.html#linea-50"),
]

def a(href, text):
    ext = href.startswith("http")
    return f'<a href="{href}">{text}{" " + icon("external", 14) if ext else ""}</a>'

FAQ = [
 ("airbus", "Airbus 90: aeroporti di Olbia e Alghero", [
  ("airbus-come", "Come vado dall’aeroporto di Olbia a Sassari o ad Alghero?",
   "Con l’Airbus Linea 90: diretto, aeroporto di Olbia → aeroporto di Alghero in meno di 2 ore.",
   ["Ferma anche al porto di Olbia (Isola Bianca), a Olbia centro, a Sassari e ad Alghero centro. Circola dal 15 aprile al 18 ottobre, domeniche e festivi compresi.",
    f"{a(PDF['90'], 'Orari e fermate (PDF)')} · {a(PORTAL, 'Prenota il biglietto')}"]),
  ("airbus-prenotare", "Devo prenotare? Posso pagare a bordo?",
   "Sì, prenota online: è l’unico modo per avere il posto garantito.",
   ["La vendita online chiude 1 ora prima della partenza o quando i posti finiscono.",
    "A bordo si paga con un supplemento di 5 €, ma solo se c’è ancora posto: nei giorni pieni puoi restare a terra.",
    a(PORTAL, "Prenota online")]),
  ("airbus-cambi", "Posso cambiare orario o farmi rimborsare?",
   "No: i biglietti della Linea 90 non si modificano e non si rimborsano.",
   ["Se non ti presenti alla partenza, il biglietto è perso. Controlla data, orario e fermata prima di pagare."]),
  ("airbus-bagagli", "Quanti bagagli posso portare sull’Airbus?",
   "1 valigia fino a 50×30×25 cm e 20 kg, più 1 borsa o zaino piccolo a bordo.",
   ["Bagagli in più o speciali si aggiungono a pagamento durante l’acquisto online."]),
  ("airbus-email", "Ho comprato il biglietto ma non mi è arrivata l’email.",
   "Controlla spam e promozioni, e che l’indirizzo inserito fosse corretto.",
   [f"Se non la trovi, {a('assistenza.html#assistenza', 'scrivi all’assistenza')} con nome del passeggero, tratta, data del viaggio e numero d’ordine."]),
  ("airbus-fermate", "Dove si prende l’Airbus? La fermata è cambiata?",
   "Le fermate sono nel PDF degli orari; le variazioni temporanee sono negli avvisi.",
   [f"{a(PDF['90'], 'Orari e fermate (PDF)')} · {a('airbus-olbia-sassari-alghero.html#avvisi', 'Avvisi in corso')}"]),
 ]),
 ("linee", "Linee in Gallura: 20, 30 e 50", [
  ("linee-quale", "Quale autobus prendo per la mia destinazione?",
   "Usa la tabella “Dove vuoi andare?” qui sopra: trovi linea e periodo in un colpo d’occhio.",
   ["Linea 20 per la Costa Smeralda, Linea 30 verso Tempio, Costa Paradiso, Castelsardo e Porto Torres, Linea 50 per Sant’Antonio di Gallura, Linea 90 per Sassari e Alghero."]),
  ("linee-quando", "Quando circolano le linee?",
   "Linee 20 e 30: dal 1° giugno al 30 settembre, tutti i giorni. Linea 50: tutto l’anno, esclusi domeniche e festivi.",
   [f"Orari: {a(PDF['20'], 'Linea 20')} · {a(PDF['30'], 'Linea 30')} · {a(PDF['50'], 'Linea 50')}"]),
  ("linee-biglietto", "Dove compro il biglietto delle linee 20, 30 e 50?",
   "A bordo o prima, sull’app Around Sardinia.",
   ["A bordo si paga in contanti (con carta dove possibile) con un sovrapprezzo. Porta contanti: in alcune zone la rete è debole e la carta può non funzionare.",
    "Con l’app compri prima e convalidi quando sali. Screenshot, stampe e fotocopie non sono validi.",
    f"{a('https://apps.apple.com/it/app/around-sardinia/id1629824982', 'App Store')} · {a('https://play.google.com/store/apps/details?id=com.openmove.sardegna', 'Google Play')}"]),
  ("linee-posto", "Posso prenotare il posto?",
   "No, sulle linee 20, 30 e 50 non si prenota: si sale alla fermata.",
   ["Il posto a sedere non è garantito in anticipo."]),
  ("linee-cambio", "Posso cambiare data o orario?",
   "Sì, purché la tratta resti la stessa."),
  ("linee-bagagli", "Valigie e bici sulle linee 20, 30 e 50?",
   "2 bagagli gratis fino a 50×30×25 cm e 20 kg ciascuno.",
   ["La bici viaggia smontata in due parti e chiusa in una sacca, e paga come un passeggero. In quel caso porti al massimo un altro bagaglio oltre a quello a mano.",
    "I bagagli vanno nelle cappelliere o sotto il sedile, sotto la tua responsabilità."]),
 ]),
 ("fermata", "In fermata e a bordo", [
  ("fermata-anticipo", "Quanto prima devo essere alla fermata?",
   "Almeno 10 minuti prima della partenza."),
  ("fermata-fermare", "Come faccio fermare l’autobus?",
   "Quando lo vedi arrivare, fai un cenno con la mano all’autista."),
  ("fermata-bambini", "Posso viaggiare con bambini piccoli?",
   "Sì, ma i più piccoli viaggiano nel loro seggiolino, fissato alle cinture del bus.",
   ["Il seggiolino lo porta il genitore o l’accompagnatore: non è fornito a bordo."]),
  ("fermata-vietato", "Animali e oggetti: cosa non posso portare?",
   "Non sono ammessi animali oltre 40 kg, merci pericolose, materiali esplosivi o infiammabili e liquidi in genere."),
  ("fermata-regole", "Regole a bordo?",
   "Resta seduto mentre il bus è in movimento; vietato fumare (anche sigarette elettroniche) e bere alcolici.",
   ["Preparati per tempo quando si avvicina la tua fermata."]),
 ]),
 ("gruppi", "Gruppi, transfer privati e parcheggio", [
  ("gruppi-bus", "Noleggiate autobus per gruppi?",
   "Sì, con conducente, da 20 e 50 posti, in tutta la Sardegna. Preventivo gratuito, risposta in poche ore.",
   [f"Indica numero di persone, data e tratta: {a('noleggio-autobus.html#preventivo', 'richiedi il preventivo')}."]),
  ("gruppi-ncc", "Fate transfer privati da porto e aeroporto di Olbia?",
   "Sì, con auto con conducente (NCC), su prenotazione, verso hotel e qualsiasi destinazione dell’isola.",
   [a("transfer-ncc.html#preventivo", "Richiedi il transfer")]),
  ("gruppi-parcheggio", "Dove lascio l’auto all’aeroporto di Olbia?",
   "Al Promo Parking by Sunlines: 3 minuti a piedi dal terminal, custodito e videosorvegliato.",
   [f"Tariffe giornaliere su {a('https://www.parkingmycar.it/', 'Parkingmycar')}, {a('https://parkos.it/', 'Parkos')} e {a('https://www.myparking.it/', 'Myparking')}. Per abbonamenti semestrali o annuali e per l’area camper: {a('parcheggio-aeroporto-olbia.html', 'pagina parcheggio')}."]),
 ]),
 ("studenti", "Abbonamenti studenti", [
  ("studenti-chi", "Chi ha diritto all’abbonamento studenti?",
   "Gli studenti fino a 27 anni, sulla Linea 50 Olbia – Sant’Antonio di Gallura.",
   ["Due tariffe: Ridotta 60% e Ridotta 80%. La Ridotta 80% richiede un ISEE inferiore a 25.501 €.",
    "Mensile o annuale, digitale con QR code da convalidare a ogni viaggio. Fai richiesta almeno 48 ore prima del primo viaggio.",
    a("abbonamenti-studenti.html", "Come richiederlo")]),
 ]),
 ("assistenza", "Assistenza", [
  ("assist-oggetto", "Ho dimenticato un oggetto sull’autobus.",
   "Scrivi all’assistenza indicando linea, data, orario del viaggio e una descrizione dell’oggetto.",
   [f"{a('assistenza.html#assistenza', 'Modulo di assistenza')} · {EMAIL}"]),
  ("assist-fattura", "Mi serve la fattura del biglietto.",
   "Compila la richiesta fattura con numero del biglietto, codice SDI e una copia del biglietto.",
   [a("assistenza.html#fattura", "Richiedi la fattura")]),
  ("assist-reclamo", "Voglio fare un reclamo.",
   "Usa il modulo reclami e segnalazioni.",
   [f"Per i diritti dei passeggeri puoi rivolgerti anche all’Autorità di Regolazione dei Trasporti (Via Nizza 230, 10126 Torino). {a('assistenza.html#reclami', 'Modulo reclami')}"]),
 ]),
]

KEYWORDS = {
    "airbus-come": "olbia alghero sassari aeroporto transfer navetta shuttle airport",
    "airbus-prenotare": "prenotazione prezzo costo tariffa pagare online posto",
    "airbus-cambi": "rimborso annullare cancellare disdire modificare cambio",
    "airbus-bagagli": "valigia bagaglio zaino peso misure",
    "airbus-email": "conferma ricevuta mail biglietto",
    "airbus-fermate": "fermata dove partenza molo brin isola bianca catalogna",
    "linee-quale": "destinazione porto cervo castelsardo tempio cannigione",
    "linee-quando": "orari calendario stagione inverno estate domenica",
    "linee-biglietto": "prezzo costo tariffa app contanti carta pagare",
    "linee-bagagli": "valigia bicicletta bike bagaglio",
    "fermata-bambini": "neonato bimbo seggiolino passeggino",
    "fermata-vietato": "cane gatto animali pet liquidi",
    "fermata-regole": "fumare sigaretta alcol",
    "gruppi-bus": "noleggio pullman gruppo matrimonio scuola gita evento",
    "gruppi-ncc": "taxi auto privato hotel",
    "gruppi-parcheggio": "parking auto camper sosta aeroporto",
    "studenti-chi": "abbonamento scuola isee universita",
    "assist-oggetto": "perso smarrito dimenticato",
    "assist-fattura": "ricevuta partita iva sdi",
    "assist-reclamo": "lamentela problema segnalazione",
}

def item(fid, q, short, more=None, open_=False):
    body = f'<p class="short">{short}</p>' + "".join(f"<p>{m}</p>" for m in (more or []))
    return f'<details id="{fid}" data-k="{KEYWORDS.get(fid, "")}"{" open" if open_ else ""}><summary>{esc(q)}</summary><div class="ans">{body}</div></details>'

def group_html(gid, filter_ids=None, open_first=False):
    for g, title, qs in FAQ:
        if g == gid:
            out = [item(*q, open_=(open_first and i == 0)) for i, q in enumerate(qs) if not filter_ids or q[0] in filter_ids]
            return '<div class="faq">' + "".join(out) + '</div>'
    return ""

def destination_table():
    rows = "".join(f'<tr><td>{esc(d)}<span class="dest-when">{esc(s)}</span></td><td><a class="badge-sm{" b90" if n == "90" else ""}" href="{h}">{n}</a></td><td class="small muted dest-col">{esc(s)}</td></tr>' for d, n, s, h in DESTINATIONS)
    return f'''<div class="dest"><table><caption class="sr-only">Quale linea per la tua destinazione</caption>
<thead><tr><th scope="col">Dove vuoi andare?</th><th scope="col">Linea</th><th scope="col" class="dest-col">Quando</th></tr></thead><tbody>{rows}</tbody></table></div>'''

def strip(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()

def faq_schema():
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q[1], "acceptedAnswer": {"@type": "Answer", "text": strip(" ".join([q[2]] + list(q[3] if len(q) > 3 else [])))}}
        for _, _, qs in FAQ for q in qs]}
