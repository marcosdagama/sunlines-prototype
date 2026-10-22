"""Interactive map of Sun Lines services in Sardinia — a self-contained home-page section.

To remove the map: delete the `map_section()` call (and its import) in pages_a.py.
Everything else (markup, styles, script, data) lives in this file and sardinia_coast.txt.

Coastline: Natural Earth 1:10m land (public domain), simplified.
Positions are indicative: the map is schematic, not a route planner.
"""
import json, math, os
from common import esc, icon
from faq_data import PDF

K = 400
COS = math.cos(math.radians(40.2))

def xy(lat, lon):
    return round((lon - 7.95) * COS * K, 1), round((41.35 - lat) * K, 1)

COAST = open(os.path.join(os.path.dirname(__file__), "sardinia_coast.txt")).read().strip()

# Views as viewBox [x, y, w, h]
def vb(lon0, lon1, lat1, lat0):
    x0, y0 = xy(lat1, lon0); x1, y1 = xy(lat0, lon1)
    return [x0, y0, round(x1 - x0, 1), round(y1 - y0, 1)]

VIEWS = {"nord": vb(8.12, 10.02, 41.33, 40.42), "isola": vb(7.98, 9.98, 41.34, 38.82)}

# Stops: id -> (name, lat, lon, label level, label anchor)
# label level: 1 both views, 2 north view only, 3 whole-island view only, 0 never (name shows on tap)
S = {
    "olbia": ("Olbia — centro, porto e aeroporto", 40.920, 9.505, 1, "se"),
    "sassari": ("Sassari", 40.727, 8.560, 1, "s"),
    "alghero-aer": ("Aeroporto di Alghero Fertilia", 40.632, 8.291, 2, "e"),
    "alghero": ("Alghero", 40.558, 8.319, 1, "e"),
    "marinella": ("Marinella", 41.014, 9.564, 0, "e"),
    "porto-rotondo": ("Porto Rotondo", 41.032, 9.541, 0, "e"),
    "portisco": ("Portisco", 41.039, 9.517, 0, "w"),
    "capriccioli": ("Capriccioli", 41.095, 9.566, 0, "e"),
    "porto-cervo": ("Porto Cervo", 41.135, 9.533, 1, "e"),
    "poltu-quatu": ("Poltu Quatu", 41.141, 9.493, 0, "n"),
    "baja-sardinia": ("Baja Sardinia", 41.138, 9.473, 0, "n"),
    "cannigione": ("Cannigione", 41.107, 9.444, 2, "s"),
    "la-conia": ("La Conia", 41.115, 9.428, 0, "w"),
    "isuledda": ("Isuledda", 41.125, 9.413, 0, "w"),
    "calangianus": ("Calangianus", 40.925, 9.192, 0, "s"),
    "tempio": ("Tempio Pausania", 40.900, 9.104, 2, "s"),
    "aggius": ("Aggius", 40.931, 9.065, 0, "w"),
    "trinita": ("Trinità d’Agultu", 40.986, 8.913, 0, "e"),
    "costa-paradiso": ("Costa Paradiso", 41.050, 8.942, 2, "n"),
    "badesi": ("Badesi", 40.966, 8.882, 0, "s"),
    "valledoria": ("Valledoria", 40.931, 8.823, 0, "s"),
    "la-muddizza": ("La Muddizza", 40.947, 8.796, 0, "n"),
    "castelsardo": ("Castelsardo", 40.914, 8.713, 2, "s"),
    "lu-bagnu": ("Lu Bagnu", 40.917, 8.679, 0, "n"),
    "platamona": ("Platamona", 40.814, 8.476, 0, "n"),
    "porto-torres": ("Porto Torres", 40.836, 8.401, 1, "n"),
    "priatu": ("Priatu", 40.955, 9.330, 0, "s"),
    "sant-antonio": ("Sant’Antonio di Gallura", 40.991, 9.302, 2, "n"),
}
SHORT = {"alghero-aer": "Aeroporto"}
# Reference towns, for orientation only (not served by a line)
REF = [("Cagliari", 39.223, 9.121), ("Nuoro", 40.321, 9.330), ("Oristano", 39.904, 8.592)]

ROUTES = [
    # id, layer, colour, title, stops, season, page link, schedule PDF
    ("90", "airbus", "#1A75BB", "Airbus 90 · Olbia – Sassari – Alghero",
     ["olbia", "sassari", "alghero-aer", "alghero"],
     "15 aprile – 18 ottobre, tutti i giorni", "airbus-olbia-sassari-alghero.html", PDF["90"]),
    ("20", "linee", "#0F6E6C", "Linea 20 · Olbia – Costa Smeralda",
     ["olbia", "marinella", "porto-rotondo", "portisco", "capriccioli", "porto-cervo", "poltu-quatu", "baja-sardinia", "cannigione", "la-conia", "isuledda"],
     "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-20", PDF["20"]),
    ("30", "linee", "#B5462F", "Linea 30 · Olbia – Tempio – Castelsardo – Porto Torres",
     ["olbia", "calangianus", "tempio", "aggius", "trinita", "costa-paradiso", "badesi", "valledoria", "la-muddizza", "castelsardo", "lu-bagnu", "platamona", "porto-torres"],
     "1 giugno – 30 settembre, tutti i giorni", "linee-e-orari.html#linea-30", PDF["30"]),
    ("50", "linee", "#4F6B3A", "Linea 50 · Olbia – Sant’Antonio di Gallura",
     ["olbia", "priatu", "sant-antonio"],
     "Tutto l’anno, dal lunedì al sabato", "linee-e-orari.html#linea-50", PDF["50"]),
]

LAYERS = [
    ("airbus", "Airbus 90", "#1A75BB"),
    ("linee", "Linee 20 · 30 · 50", "#0F6E6C"),
    ("ncc", "Noleggio e NCC", "#F68221"),
    ("parking", "Parcheggio", "#F68221"),
]

# Descriptions read by screen readers; the visible <desc> is rebuilt from the active layers.
LAYER_DESC = {
    "airbus": "Airbus 90, in blu: dal porto, dal centro e dall’aeroporto di Olbia attraversa il nord dell’isola fino a Sassari, all’aeroporto di Alghero Fertilia e al centro di Alghero, dal 15 aprile al 18 ottobre.",
    "linee": "Linee di trasporto pubblico in Gallura, tutte in partenza da Olbia: Linea 20, in verde, verso nord lungo la Costa Smeralda fino a Porto Cervo, Baja Sardinia, Cannigione e Isuledda, in estate; Linea 30, in rosso mattone, verso ovest per Calangianus, Tempio Pausania, Aggius, Costa Paradiso, Badesi, Castelsardo e Porto Torres, in estate; Linea 50, in verde oliva, per Priatu e Sant’Antonio di Gallura, tutto l’anno dal lunedì al sabato.",
    "ncc": "Noleggio autobus con conducente e auto NCC, a righe arancioni: coprono tutta la Sardegna, su prenotazione, con partenza da Olbia.",
    "parking": "Parcheggio Sun Lines per auto e camper, segnato con una P arancione accanto all’aeroporto di Olbia.",
}
INTRO = {"nord": "Mappa schematica del nord della Sardegna con i servizi Sun Lines. Olbia, dove hanno sede porto, aeroporto e azienda, è il punto di partenza di tutte le linee.",
         "isola": "Mappa schematica di tutta la Sardegna con i servizi Sun Lines. Le linee si concentrano nel nord, attorno a Olbia; Cagliari, Nuoro e Oristano sono indicate solo come riferimento."}

PARK = (40.903, 9.522)   # beside Olbia airport
PARK_BADGE = (40.775, 9.625)  # badge placed out at sea, with a leader line, so it never covers the Olbia hub


def smooth(points, t=0.5):
    """Catmull-Rom spline through the points, as an SVG path."""
    if len(points) < 3:
        return "M" + "L".join(f"{x},{y}" for x, y in points)
    p = [points[0]] + points + [points[-1]]
    d = f"M{p[1][0]},{p[1][1]}"
    for i in range(1, len(p) - 2):
        x0, y0 = p[i - 1]; x1, y1 = p[i]; x2, y2 = p[i + 1]; x3, y3 = p[i + 2]
        c1 = (x1 + (x2 - x0) * t / 3, y1 + (y2 - y0) * t / 3)
        c2 = (x2 - (x3 - x1) * t / 3, y2 - (y3 - y1) * t / 3)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x2},{y2}"
    return d


def map_section():
    stop_routes = {k: [] for k in S}
    for rid, layer, col, title, stops, *_ in ROUTES:
        for s in stops:
            stop_routes[s].append(rid)

    routes_svg = "".join(
        f'<path class="mp-route" data-r="{rid}" data-layer="{layer}" d="{smooth([xy(S[s][1], S[s][2]) for s in stops])}" stroke="{col}"/>'
        for rid, layer, col, title, stops, *_ in ROUTES)

    stops_svg, labels_svg = "", ""
    for sid, (name, lat, lon, lvl, anc) in S.items():
        x, y = xy(lat, lon)
        layers = sorted({r[1] for r in ROUTES if sid in r[4]})
        hub = sid == "olbia"
        stops_svg += f'<circle class="mp-stop{" mp-hub" if hub else ""}" data-s="{sid}" data-layer="{" ".join(layers)}" cx="{x}" cy="{y}" r="4"/>'
        if lvl:
            labels_svg += f'<text class="mp-lbl{" mp-lbl-hub" if hub else ""}" data-lv="{lvl}" data-a="{anc}" data-x="{x}" data-y="{y}" data-layer="{" ".join(layers)}" x="{x}" y="{y}">{esc(SHORT.get(sid, name.split(" — ")[0]))}</text>'
    for name, lat, lon in REF:
        x, y = xy(lat, lon)
        stops_svg += f'<circle class="mp-ref" cx="{x}" cy="{y}" r="2.5"/>'
        labels_svg += f'<text class="mp-lbl mp-lbl-ref" data-lv="3" data-a="e" data-x="{x}" data-y="{y}" x="{x}" y="{y}">{name}</text>'

    px, py = xy(*PARK); bx, by = xy(*PARK_BADGE)
    park_svg = (f'<g class="mp-park" data-layer="parking" data-s="parcheggio"><line x1="{px}" y1="{py}" x2="{bx}" y2="{by}"/>'
                f'<circle class="mp-park-dot" cx="{px}" cy="{py}" r="3"/>'
                f'<g class="mp-park-badge" data-x="{bx}" data-y="{by}"><rect x="{bx}" y="{by}" width="20" height="20" rx="4"/><text x="{bx}" y="{by}">P</text></g></g>')

    full_desc = INTRO["nord"] + " " + " ".join(LAYER_DESC[k] for k, *_ in LAYERS if k != "ncc") + " Le posizioni sono indicative: per orari e fermate esatte vedi l’elenco accanto alla mappa."

    chips = "".join(
        f'<button type="button" class="mp-chip" data-layer="{k}" aria-pressed="{"false" if k == "ncc" else "true"}"><span class="mp-sw mp-sw-{k}" aria-hidden="true"></span>{esc(n)}</button>'
        for k, n, _ in LAYERS)

    key = "".join(
        f'''<li data-layer="{layer}" data-r="{rid}"><span class="mp-key-badge" style="background:{col}">{rid}</span><div>
<p class="mp-key-t">{esc(title.split(" · ", 1)[1])}</p><p class="small muted">{esc(season)}</p>
<p class="small"><a href="{href}">{"Pagina Airbus 90" if rid == "90" else "Fermate e orari"}</a></p></div></li>'''
        for rid, layer, col, title, stops, season, href, pdf in ROUTES)
    key += f'''<li data-layer="ncc"><span class="mp-key-badge mp-key-ncc" aria-hidden="true"></span><div>
<p class="mp-key-t">Noleggio bus e auto con conducente</p><p class="small muted">In tutta la Sardegna, su prenotazione</p>
<p class="small"><a href="noleggio-autobus.html">Noleggio bus</a> · <a href="transfer-ncc.html">Transfer e NCC</a></p></div></li>
<li data-layer="parking"><span class="mp-key-badge mp-key-p" aria-hidden="true">P</span><div>
<p class="mp-key-t">Parcheggio aeroporto di Olbia</p><p class="small muted">Auto e camper, accanto all’aeroporto</p>
<p class="small"><a href="parcheggio-aeroporto-olbia.html">Tariffe e prenotazione</a></p></div></li>'''

    data = {
        "views": VIEWS,
        "intro": INTRO,
        "desc": LAYER_DESC,
        "order": [k for k, *_ in LAYERS],
        "stops": {k: {"n": v[0], "r": stop_routes[k]} for k, v in S.items()},
        "routes": {r[0]: {"t": r[3], "c": r[2], "h": r[6], "s": r[5]} for r in ROUTES},
    }

    x, y, w, h = VIEWS["nord"]
    return f'''
<section class="section section-white mp" id="mappa" aria-labelledby="mappa-h">{CSS}
<div class="wrap mp-grid">
  <div class="mp-head">
    <p class="label eyebrow">Dove andiamo</p>
    <h2 class="h1" id="mappa-h">I nostri servizi sulla mappa</h2>
    <p class="muted">Tutto parte da Olbia: aeroporto, porto e centro. Accendi o spegni i livelli per vedere linee, transfer e parcheggio.</p>
  </div>
  <div class="mp-controls">
    <div class="mp-chips" role="group" aria-label="Livelli della mappa">{chips}</div>
    <div class="mp-views" role="group" aria-label="Area della mappa">
      <button type="button" data-view="nord" aria-pressed="true">Nord Sardegna</button><button type="button" data-view="isola" aria-pressed="false">Tutta l’isola</button>
    </div>
  </div>
  <figure class="mp-fig">
    <svg class="mp-svg" viewBox="{x} {y} {w} {h}" style="aspect-ratio:{w} / {h}" role="img" aria-labelledby="mappa-title mappa-desc" xmlns="http://www.w3.org/2000/svg">
      <title id="mappa-title">Mappa dei servizi Sun Lines in Sardegna</title>
      <desc id="mappa-desc">{esc(full_desc)}</desc>
      <defs><pattern id="mp-stripes" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#FFFFFF"/><rect width="8" height="2" fill="#FDE9D6"/></pattern></defs>
      <rect class="mp-sea" x="-1500" y="-500" width="3600" height="2200"/>
      <path class="mp-land" d="{COAST}"/>
      <path class="mp-ncc" data-layer="ncc" d="{COAST}" fill="url(#mp-stripes)"/>
      <g class="mp-routes">{routes_svg}</g>
      <g class="mp-stops">{stops_svg}</g>
      {park_svg}
      <g class="mp-labels">{labels_svg}</g>
      <circle class="mp-sel" r="9" cx="-50" cy="-50"/>
    </svg>
    <figcaption class="mp-card" aria-live="polite"><p class="small muted">Tocca un punto della mappa per vedere quali servizi ci passano.</p></figcaption>
    <p class="mp-note small muted">Mappa schematica, posizioni indicative. Costa: Natural Earth.</p>
  </figure>
  <div class="mp-key-wrap"><h3 class="h3">Cosa vedi sulla mappa</h3><ul class="mp-key">{key}</ul></div>
</div>
<script type="application/json" id="mappa-data">{json.dumps(data, ensure_ascii=False)}</script>
<script>{JS}</script>
</section>'''


CSS = '''<style>
.mp-grid{display:grid;gap:20px;grid-template-areas:"head" "controls" "fig" "key"}
@media (min-width:960px){.mp-grid{grid-template-columns:minmax(0,5fr) minmax(0,7fr);column-gap:40px;grid-template-areas:"head fig" "controls fig" "key fig";grid-template-rows:auto auto 1fr;align-items:start}}
.mp-head{grid-area:head;display:grid;gap:10px}.mp-controls{grid-area:controls;display:grid;gap:12px}.mp-fig{grid-area:fig;margin:0;display:grid;gap:10px}.mp-key-wrap{grid-area:key;display:grid;gap:12px}
@media (min-width:960px){.mp-fig{position:sticky;top:88px}}
.mp-chips{display:flex;flex-wrap:wrap;gap:8px}
.mp-chip{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 14px;border-radius:999px;border:1px solid var(--hairline);background:var(--white);font:600 15px var(--font);color:var(--muted);cursor:pointer}
.mp-chip[aria-pressed="true"]{color:var(--navy);border-color:var(--navy);background:var(--sand)}
.mp-chip:focus-visible,.mp-views button:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.mp-sw{width:18px;height:6px;border-radius:3px;flex:none;opacity:.35}.mp-chip[aria-pressed="true"] .mp-sw{opacity:1}
.mp-sw-airbus{background:#1A75BB}.mp-sw-linee{background:linear-gradient(90deg,#0F6E6C 33%,#B5462F 33% 66%,#4F6B3A 66%)}
.mp-sw-ncc{height:14px;background:repeating-linear-gradient(180deg,#F68221 0 3px,#FDE3CC 3px 6px)}.mp-sw-parking{width:16px;height:16px;border-radius:3px;background:#F68221}
.mp-views{display:inline-flex;border:1px solid var(--hairline);border-radius:var(--r-md);padding:3px;width:max-content;background:var(--white)}
.mp-views button{min-height:40px;padding:6px 14px;border:0;border-radius:7px;background:none;font:600 15px var(--font);color:var(--muted);cursor:pointer}
.mp-views button[aria-pressed="true"]{background:var(--navy);color:#fff}
.mp-svg{display:block;width:100%;margin-inline:auto;height:auto;max-height:78vh;border-radius:var(--r-md);border:1px solid var(--hairline);cursor:pointer;touch-action:manipulation;font-family:var(--font)}
.mp-sea{fill:#EAF2F8}.mp-land{fill:#fff;stroke:#BFCDDA;stroke-width:1;vector-effect:non-scaling-stroke}
.mp-ncc{stroke:#F8C08F;stroke-width:1.5;vector-effect:non-scaling-stroke}
.mp-route{fill:none;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;transition:opacity .2s}
.mp-stop{fill:#fff;stroke:#0B2545;stroke-width:1.75;vector-effect:non-scaling-stroke}
.mp-hub{fill:#0B2545;stroke:#fff;stroke-width:2.5}
.mp-ref{fill:#7D8794}
.mp-lbl{fill:#0B2545;font-weight:600;paint-order:stroke;stroke:#fff;stroke-linejoin:round;pointer-events:none}
.mp-lbl-hub{font-weight:700}.mp-lbl-ref{fill:#4F5B6B;font-weight:500}
.mp-park line{stroke:#0B2545;stroke-width:1;stroke-dasharray:3 3;vector-effect:non-scaling-stroke}
.mp-park-dot{fill:#F68221;stroke:#0B2545;stroke-width:1;vector-effect:non-scaling-stroke}
.mp-park-badge rect{fill:#F68221}.mp-park-badge text{fill:#0B2545;font-weight:700;text-anchor:middle;dominant-baseline:central}
.mp-sel{fill:none;stroke:#F68221;stroke-width:3;vector-effect:non-scaling-stroke;pointer-events:none}
.mp [data-off]{display:none}
.mp[data-hl] .mp-route{opacity:.15}.mp[data-hl] .mp-route.hl{opacity:1}
.mp-card{min-height:72px;padding:12px 14px;border:1px solid var(--hairline);border-radius:var(--r-md);background:var(--sand);display:grid;gap:6px}
.mp-card h3{margin:0;font-size:18px}.mp-card ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.mp-card li{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.mp-badge{display:inline-grid;place-items:center;min-width:34px;height:26px;padding:0 6px;border-radius:4px;color:#fff;font-weight:700;font-size:14px}
.mp-note{margin:0}
.mp-key{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.mp-key li{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start;padding:12px;border:1px solid var(--hairline);border-radius:var(--r-md);background:var(--white)}
.mp-key li p{margin:0}.mp-key-t{font-weight:600}
.mp-key-badge{display:grid;place-items:center;width:40px;height:32px;border-radius:4px;color:#fff;font-weight:700}
.mp-key-ncc{background:repeating-linear-gradient(180deg,#F68221 0 4px,#FDE3CC 4px 8px)}.mp-key-p{background:#F68221;color:#0B2545}
</style>'''

JS = r'''(function(){
var root=document.getElementById('mappa');if(!root)return;
var D=JSON.parse(document.getElementById('mappa-data').textContent);
var svg=root.querySelector('.mp-svg'),desc=svg.querySelector('desc'),card=root.querySelector('.mp-card'),sel=svg.querySelector('.mp-sel');
var on={};D.order.forEach(function(k){on[k]=k!=='ncc'});
var view='nord',vbx=D.views.nord.slice(),u=1;
var OFF={se:[7,15,'start'],e:[8,4,'start'],w:[-8,4,'end'],n:[0,-9,'middle'],s:[0,16,'middle']};
function layout(){
  svg.style.maxWidth=Math.round(window.innerHeight*.78*vbx[2]/vbx[3])+'px';
  var w=svg.getBoundingClientRect().width;if(!w)return;u=vbx[2]/w;
  svg.style.fontSize=(13*u)+'px';
  svg.querySelectorAll('.mp-lbl').forEach(function(t){
    var lv=+t.dataset.lv,show=lv===1||(lv===2&&view==='nord'&&u<1.05)||(lv===3&&view==='isola');
    t.style.display=show&&visible(t)?'':'none';
    var o=OFF[t.dataset.a];t.setAttribute('x',+t.dataset.x+o[0]*u);t.setAttribute('y',+t.dataset.y+o[1]*u);t.setAttribute('text-anchor',o[2]);
    t.style.strokeWidth=(3*u)+'px'});
  svg.querySelectorAll('.mp-stop').forEach(function(c){c.setAttribute('r',(c.classList.contains('mp-hub')?7:4)*u)});
  svg.querySelectorAll('.mp-ref').forEach(function(c){c.setAttribute('r',2.5*u)});
  svg.querySelectorAll('.mp-park-dot').forEach(function(c){c.setAttribute('r',3.5*u)});
  var b=svg.querySelector('.mp-park-badge');if(b){var s=22*u,bx=+b.dataset.x,by=+b.dataset.y,r=b.querySelector('rect'),tx=b.querySelector('text');
    r.setAttribute('x',bx-s/2);r.setAttribute('y',by-s/2);r.setAttribute('width',s);r.setAttribute('height',s);r.setAttribute('rx',4*u);
    tx.setAttribute('x',bx);tx.setAttribute('y',by);tx.style.fontSize=(15*u)+'px'}
  sel.setAttribute('r',11*u)}
function visible(el){var l=(el.dataset.layer||'').split(' ').filter(Boolean);return !l.length||l.some(function(k){return on[k]})}
function apply(){
  root.querySelectorAll('[data-layer]').forEach(function(el){if(el.classList.contains('mp-chip'))return;
    if(visible(el))el.removeAttribute('data-off');else el.setAttribute('data-off','')});
  var act=D.order.filter(function(k){return on[k]});
  desc.textContent=D.intro[view]+' '+(act.length?act.map(function(k){return D.desc[k]}).join(' '):'Nessun livello attivo: è visibile solo la sagoma dell’isola.')+' Le posizioni sono indicative: per orari e fermate esatte vedi l’elenco accanto alla mappa.';
  layout()}
root.querySelectorAll('.mp-chip').forEach(function(b){b.addEventListener('click',function(){
  var k=b.dataset.layer;on[k]=!on[k];b.setAttribute('aria-pressed',on[k]);apply()})});
function setView(v){if(v===view)return;view=v;
  root.querySelectorAll('.mp-views button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.view===v)});
  var a=vbx.slice(),z=D.views[v],t0=null,red=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function step(ts){if(!t0)t0=ts;var p=red?1:Math.min(1,(ts-t0)/450),e=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
    vbx=a.map(function(n,i){return n+(z[i]-n)*e});svg.setAttribute('viewBox',vbx.join(' '));svg.style.aspectRatio=vbx[2]+' / '+vbx[3];
    layout();if(p<1)requestAnimationFrame(step);else apply()}
  requestAnimationFrame(step)}
root.querySelectorAll('.mp-views button').forEach(function(b){b.addEventListener('click',function(){setView(b.dataset.view)})});
function badge(r){var R=D.routes[r];return '<span class="mp-badge" style="background:'+R.c+'">'+r+'</span>'}
function show(id,x,y){
  if(id==='parcheggio'){card.innerHTML='<h3>Parcheggio aeroporto di Olbia</h3><p class="small">Auto e camper, accanto all’aeroporto. Prenoti online.</p><p class="small"><a href="parcheggio-aeroporto-olbia.html">Tariffe e prenotazione</a></p>'}
  else{var s=D.stops[id],rs=s.r.filter(function(r){return on[r==='90'?'airbus':'linee']});
    card.innerHTML='<h3>'+s.n+'</h3><ul>'+rs.map(function(r){var R=D.routes[r];return '<li>'+badge(r)+'<span class="small">'+R.t.split(' · ')[1]+' · '+R.s+'</span> <a class="small" href="'+R.h+'">Orari</a></li>'}).join('')+'</ul>'
      +(id==='olbia'?'<p class="small">Da qui partono anche <a href="noleggio-autobus.html">noleggio bus</a> e <a href="transfer-ncc.html">transfer NCC</a>, e c’è il <a href="parcheggio-aeroporto-olbia.html">parcheggio aeroporto</a>.</p>':'')}
  sel.setAttribute('cx',x);sel.setAttribute('cy',y)}
svg.addEventListener('click',function(ev){
  var pt=svg.createSVGPoint();pt.x=ev.clientX;pt.y=ev.clientY;var p=pt.matrixTransform(svg.getScreenCTM().inverse());
  var best=null,bd=22*u;
  svg.querySelectorAll('.mp-stop:not([data-off])').forEach(function(c){var d=Math.hypot(c.cx.baseVal.value-p.x,c.cy.baseVal.value-p.y);if(d<bd){bd=d;best=c}});
  var pk=svg.querySelector('.mp-park:not([data-off]) .mp-park-badge');
  if(pk){var d=Math.hypot(+pk.dataset.x-p.x,+pk.dataset.y-p.y);if(d<bd){show('parcheggio',+pk.dataset.x,+pk.dataset.y);return}}
  if(best)show(best.dataset.s,best.cx.baseVal.value,best.cy.baseVal.value)});
root.querySelectorAll('.mp-key li[data-r]').forEach(function(li){
  function hl(){root.setAttribute('data-hl',li.dataset.r);svg.querySelectorAll('.mp-route').forEach(function(p){p.classList.toggle('hl',p.dataset.r===li.dataset.r)})}
  function un(){root.removeAttribute('data-hl')}
  li.addEventListener('mouseenter',hl);li.addEventListener('mouseleave',un);li.addEventListener('focusin',hl);li.addEventListener('focusout',un)});
window.addEventListener('resize',layout);apply();
})();'''
