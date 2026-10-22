# Sun Lines × Bigo — integrazione del portale di vendita nel nuovo sito

**Versione:** 1.0 · 22 ottobre 2026  
**Da:** Sun Lines Elite Service S.r.l., con Relevant (progetto del nuovo sito)  
**Per:** Bigo Solutions, team del portale `sites.bigosolutions.it/sunlines`

## 1. Obiettivo

Sun Lines sta rifacendo il sito www.sunlines.it. Il portale Bigo resta il sistema di vendita dei biglietti Airbus 90 e Linea 50. Chiediamo che il portale abbia **lo stesso aspetto del nuovo sito** e che il sito possa **portare il cliente direttamente ai risultati di una ricerca**, senza perdere nessuna funzione attuale: ricerca, scelta della corsa, dati passeggeri, bagagli, pagamento, biglietto, lingue.

Risultato atteso: chi compra un biglietto non deve accorgersi di passare da un sito all’altro.

Obiettivo di messa online: **entro il 1° aprile 2027**, prima dell’inizio della stagione Airbus 90 (15 aprile). Collaudo a marzo 2027.

## 2. Cosa chiediamo (lavori da quotare)

| # | Lavoro | Priorità |
| --- | --- | --- |
| A | Tema grafico Sun Lines sul portale (colori, carattere, logo, componenti) | Indispensabile |
| B | Header e footer Sun Lines con link al sito | Indispensabile |
| C | Indirizzo `biglietti.sunlines.it` con HTTPS | Indispensabile |
| D | Link di prenotazione con tratta, data e passeggeri (§ 5) | Indispensabile |
| E | Cookie e privacy allineati al sito Sun Lines (§ 7) | Indispensabile |
| F | Accessibilità WCAG 2.1 AA e contributo alla dichiarazione di accessibilità (§ 8) | Indispensabile per legge |
| G | Eventi di misurazione delle vendite, solo con consenso (§ 9) | Consigliato |
| H | Disponibilità di API o widget di ricerca da incorporare nel sito (§ 10) | Da valutare |

Per ogni voce chiediamo costo una tantum, eventuale canone, tempi e cosa serve da parte nostra.

## 3. Cosa trovate nel pacchetto

| Cartella | Contenuto |
| --- | --- |
| `01-brand/logo` | Logo Sun Lines a colori e in bianco (SVG e PNG), simbolo del sole |
| `01-brand/font` | Barlow 400, 500, 600, 700 in WOFF2, con licenza SIL Open Font License |
| `01-brand/sunlines-tokens.json` | Palette completa con regole d’uso e contrasti |
| `02-tema/sunlines-tokens.css` | Variabili CSS (colori, tipografia, raggi, spazi) |
| `02-tema/sunlines-bigo-theme.css` | Tema pronto: componenti con prefisso `sl-` (§ 4) |
| `02-tema/header.html`, `footer.html` | Header e footer da inserire nel portale |
| `03-mockup/*.html` | Le 4 schermate del portale con il tema Sun Lines, apribili nel browser |
| `03-mockup/screenshot` | Le stesse schermate in PNG, desktop e mobile |

Nei mockup orari, prezzi e nomi sono **dati di esempio**. I testi delle condizioni (bagaglio, chiusura vendite, rimborsi) sono quelli in vigore.

## 4. Grafica

### 4.1 Regole base

- **Carattere:** solo Barlow (400 testo, 500 etichette, 600 pulsanti e sottotitoli, 700 titoli). Ospitato sul vostro server dai file forniti: **non caricare Google Fonts** (oggi il portale carica Lato da Google, che trasmette l’indirizzo IP dei visitatori a Google).
- **Colori:** sfondo pagina mist `#F2F6F9`, card bianche, testo navy `#0B2545`, pulsante primario blu `#1A75BB` con testo bianco, accento arancio `#F68221` usato poco (righe del sole, passo attivo, pallino d’arrivo). Testo sull’arancio sempre navy, mai bianco.
- **Avvisi:** disservizi in terracotta `#B5462F`, conferme in verde macchia `#4F6B3A`, sempre con icona e testo, mai solo colore.
- **Forme:** raggio 10 px per card e pulsanti, 4 px per i campi; aree toccabili di almeno 44 px.
- **Logo:** colori su fondo bianco, bianco su navy. Altezza minima 36 px. Non ridisegnare, deformare o ricolorare.

### 4.2 Mappatura dei componenti

| Elemento del portale | Classe del tema |
| --- | --- |
| Pulsante “cerca”, “scegli”, “paga” | `sl-btn sl-btn-primary` |
| Pulsante secondario (“modifica”) | `sl-btn sl-btn-secondary` |
| Partenza, arrivo, data, campi testo | `sl-field` + `sl-select` / `sl-input` |
| Errore di un campo | `sl-field err` + `sl-err` |
| Numero passeggeri e bagagli (− / +) | `sl-stepper` |
| Solo andata / andata e ritorno | `sl-seg` |
| Barra delle date | `sl-dates` + `sl-date` (attiva: `aria-current="date"`) |
| Corsa nei risultati | `sl-trip` (esaurita: `full`) |
| “Ultimi posti”, “esaurita”, numero linea | `sl-badge-warn`, `sl-badge-line` |
| Avvisi di servizio | `sl-alert sl-alert-warn` |
| Riepilogo e totale | `sl-summary` |
| Fasi dell’acquisto | `sl-steps` |
| Biglietto emesso | `sl-ticket` |

Le classi sono un riferimento: potete applicare gli stessi valori ai vostri componenti esistenti invece di usare il CSS così com’è.

### 4.3 Header e footer

- **Header:** logo a sinistra con link a `https://www.sunlines.it/`, a destra “Info Airbus 90”, “Assistenza” e il selettore lingua. Su mobile restano logo e lingua.
- **Footer:** link a sito, condizioni di vendita, condizioni di trasporto, diritti dei passeggeri, privacy, cookie, accessibilità; riga legale con ragione sociale, P. IVA e “Portale di vendita gestito da Bigo Solutions per conto di Sun Lines”.
- Il codice è in `02-tema/header.html` e `footer.html`.

## 5. Link di prenotazione (deep link)

Oggi una ricerca porta sempre a `/sunlines/it/booking` senza parametri, quindi il sito non può aprire una tratta precisa. Chiediamo che il portale accetti questi parametri:

| Parametro | Valori | Obbligatorio | Esempio |
| --- | --- | --- | --- |
| lingua (nel percorso) | `it`, `en`, `de`, `es`, `fr` | sì | `/it/booking` |
| `da` | codice località come nel portale: `OLBIA`, `SASSARI`, `ALGHERO` | no | `da=OLBIA` |
| `a` | come sopra; anche `LINEA50` se vendete la Linea 50 | no | `a=ALGHERO` |
| `data` | data di andata `AAAA-MM-GG` | no | `data=2027-06-15` |
| `ritorno` | data di ritorno `AAAA-MM-GG` (attiva andata e ritorno) | no | `ritorno=2027-06-22` |
| `adulti` | 1–9, predefinito 1 | no | `adulti=2` |
| `utm_*` | parametri di campagna, da conservare fino al pagamento | no | `utm_source=sunlines.it` |

**Comportamento richiesto:**

1. Con `da`, `a` e `data` validi, il portale mostra subito i risultati, senza altri clic.
2. Con parametri parziali, il modulo di ricerca si apre già compilato con quelli validi.
3. Se la data è passata o fuori stagione, mostrare la prima data disponibile con un messaggio chiaro, non una pagina vuota.
4. Parametri non validi vengono ignorati senza errori tecnici.
5. Se esistono codici di fermata (aeroporto, porto, centro), indicateci i nomi dei parametri: li useremo per le fermate.

**Esempio:** `https://biglietti.sunlines.it/it/booking?da=OLBIA&a=ALGHERO&data=2027-06-15&adulti=2`

## 6. Indirizzo e aspetti tecnici

- **Sottodominio:** `biglietti.sunlines.it`. Sun Lines crea il record DNS (CNAME o A) che ci indicherete; voi attivate il certificato HTTPS e il rinnovo automatico.
- **Vecchio indirizzo:** reindirizzamento permanente (301) da `sites.bigosolutions.it/sunlines/...` alle stesse pagine sul nuovo indirizzo, per non perdere link salvati.
- **Lingue:** mantenere le 5 lingue e i tag `hreflang` già presenti, aggiornati al nuovo indirizzo.
- **Motori di ricerca:** la pagina di ricerca di ogni lingua può essere indicizzata; risultati, dati passeggero, pagamento e conferma con `noindex`.
- **Titoli di pagina:** “Biglietti Airbus 90 Olbia – Sassari – Alghero | Sun Lines” e simili, per lingua.
- **Icona del sito:** simbolo del sole (`sun-lines-sun-mark.svg`).
- **Prestazioni su mobile:** obiettivo LCP sotto 2,5 s e nessuno spostamento del layout al caricamento.

## 7. Cookie e privacy

- **Un solo consenso.** Il sito Sun Lines usa un proprio banner conforme alle linee guida del Garante (10 giugno 2021) e salva le scelte nel cookie tecnico `sl_consent` (validità 6 mesi):
  `{"v":"1","ts":<millisecondi>,"c":{"necessari":true,"statistiche":false,"marketing":false}}`.
  Sul nuovo indirizzo il cookie sarà impostato sul dominio `.sunlines.it`, quindi leggibile dal portale. Chiediamo che il portale legga questo cookie e mostri il proprio banner solo se manca o è scaduto, con le stesse tre categorie e lo stesso stile (Accetta e Rifiuta con lo stesso peso, X che chiude rifiutando).
- **Nessuno strumento non necessario prima del consenso:** analytics e pubblicità solo dopo consenso della categoria corrispondente.
- **Ruoli privacy:** Sun Lines è titolare del trattamento dei dati di vendita. Chiediamo conferma che Bigo agisca come responsabile del trattamento (art. 28 GDPR) e il relativo accordo, con l’elenco dei sub-responsabili, compreso il fornitore dei pagamenti.
- **Testi:** nelle pagine del portale, link all’informativa privacy, alla cookie policy e alle condizioni di vendita del sito Sun Lines. Sotto i dati del passeggero il testo informativo dei mockup.
- **Dati minimi:** obbligatori solo nome, cognome ed email; telefono facoltativo. Eventuale consenso marketing facoltativo e non preselezionato.

## 8. Accessibilità

Il portale fa parte del servizio di trasporto Sun Lines e rientra nel D.Lgs. 82/2022 (European Accessibility Act).

- Conformità **WCAG 2.1 livello AA** (EN 301 549) su tutte le fasi, pagamento compreso.
- Uso completo da tastiera, focus sempre visibile, ordine di tabulazione logico.
- Etichette su tutti i campi; errori spiegati a parole accanto al campo, non solo in rosso.
- Selettore della data utilizzabile da tastiera e con lettore di schermo.
- Numero di risultati annunciato ai lettori di schermo (regione `aria-live`).
- Se il posto è bloccato per un tempo limitato, avvisare prima della scadenza e permettere di prolungare (WCAG 2.2.1).
- Attributo `lang` corretto per ogni lingua.
- Chiediamo la vostra **dichiarazione di accessibilità** del portale, o i dati per completare la nostra: stato di conformità, limiti noti, data dell’ultima verifica.

I mockup forniti superano il controllo automatico WCAG 2.1 AA (axe-core) su desktop e mobile.

## 9. Misurazione delle vendite (dopo consenso “statistiche”)

Eventi da inviare a `window.dataLayer`, solo se `sl_consent.c.statistiche` è `true`:

| Evento | Quando | Dati |
| --- | --- | --- |
| `sl_search` | ricerca eseguita | `da`, `a`, `data`, `adulti`, numero di corse trovate |
| `sl_select_trip` | corsa scelta | orario, prezzo |
| `sl_begin_checkout` | passaggio al pagamento | totale, valuta |
| `sl_purchase` | pagamento riuscito | totale, valuta, numero ordine (senza dati personali) |

## 10. API o widget (da valutare)

Il sito vorrebbe mostrare una casella di ricerca nel proprio stile (home, pagina Airbus 90). Con i link del § 5 basta un modulo del sito che apre il portale. Se offrite un’API documentata (località, corse disponibili, posti) o un widget incorporabile, indicateci condizioni e costi. Non useremo l’API interna del portale senza un accordo scritto.

## 11. Collaudo

Il lavoro è accettato quando:

- [ ] Le 4 fasi (ricerca, corse, passeggeri, pagamento e conferma) corrispondono ai mockup su desktop e mobile.
- [ ] Barlow è caricato dal vostro server; nessuna richiesta a Google Fonts.
- [ ] `biglietti.sunlines.it` risponde in HTTPS; il vecchio indirizzo reindirizza con 301.
- [ ] I link del § 5 aprono i risultati giusti in tutte e 5 le lingue.
- [ ] Il consenso dato sul sito vale sul portale e viceversa; nessuno strumento non necessario prima del consenso.
- [ ] Controllo WCAG 2.1 AA senza errori su tutte le fasi; prova da tastiera e con lettore di schermo (VoiceOver o NVDA).
- [ ] Un acquisto di prova completo, con e-mail e biglietto PDF in stile Sun Lines.
- [ ] Il footer porta alle pagine legali del sito Sun Lines.

## 12. Domande per Bigo

1. Quali di questi lavori sono già possibili con la configurazione attuale del portale?
2. Costi e tempi per le voci A–H.
3. Il portale può leggere un cookie di consenso sul dominio `.sunlines.it`?
4. Esistono codici di fermata oltre alle città?
5. Avete un’API o un widget documentato? A quali condizioni?
6. Il portale ha già una dichiarazione di accessibilità?
7. Chi è il fornitore dei pagamenti e quali metodi sono attivi (carte, Apple Pay, Google Pay, PayPal)?
8. Durata del contratto attuale, costo (canone o commissione) e preavviso.

## 13. Contatti

- **Sun Lines:** Pietro, info@sunlines.it, +39 0789 50885
- **Relevant (sito e grafica):** Marcos da Gama, marcos.dagama@relevant.es
