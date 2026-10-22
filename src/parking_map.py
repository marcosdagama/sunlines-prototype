"""Schematic location map for Promo Parking by Sun Lines (Via dei Fornai 5, Olbia airport).

Same visual language as the Sardinia map: brand colours, inline SVG, layer chips, text alternative.
Not to scale: positions follow the street layout around Olbia Costa Smeralda airport.
"""
from common import esc, icon

ADDRESS = "Via dei Fornai 5, 07026 Olbia (SS)"
Q = "Via+dei+Fornai+5,+07026+Olbia+SS"
LINKS = [
    ("Google Maps", f"https://www.google.com/maps/search/?api=1&amp;query={Q}"),
    ("Apple Mappe", f"https://maps.apple.com/?q=Promo+Parking+Sun+Lines&amp;address={Q}"),
    ("Waze", f"https://waze.com/ul?q={Q}&amp;navigate=yes"),
]
DESC = {
    "auto": "In auto: dalla SS729 o dalla SP24 segui le indicazioni per l’aeroporto; alla rotatoria prendi Via degli Aviatori verso il terminal e svolta per Via dei Fornai, dove si trova l’ingresso del parcheggio.",
    "piedi": "A piedi: dal parcheggio al terminal dell’aeroporto sono circa 200 metri, 3 minuti, con passaggio pedonale diretto.",
}


def parking_map():
    chips = "".join(f'<button type="button" class="mp-chip" data-pm="{k}" aria-pressed="true"><span class="pm-sw pm-sw-{k}" aria-hidden="true"></span>{n}</button>'
                    for k, n in (("auto", "In auto"), ("piedi", "A piedi")))
    links = "".join(f'<a class="btn btn-outline btn-sm" href="{h}">{n} {icon("external", 14)}</a>' for n, h in LINKS)
    desc = ("Mappa schematica dell’area dell’aeroporto di Olbia Costa Smeralda, non in scala. Il parcheggio Promo Parking by Sun Lines, segnato con una P arancione, "
            "si trova in Via dei Fornai 5, a ovest del terminal, accanto a Via degli Aviatori. " + DESC["auto"] + " " + DESC["piedi"])
    return f'''
<section class="section section-white pm" id="dove-siamo" aria-labelledby="pm-h">
<div class="wrap pm-grid">
  <div class="pm-info">
    <p class="label eyebrow">Dove siamo</p>
    <h2 class="h2" id="pm-h">Accanto al terminal, a 3 minuti a piedi</h2>
    <p class="pm-addr"><strong>Promo Parking by Sun Lines</strong><br>{ADDRESS}</p>
    <ul class="pm-facts">
      <li>{icon("check",18)} Aperto 24 ore su 24</li>
      <li>{icon("check",18)} Custodito e videosorvegliato</li>
      <li>{icon("check",18)} Posti coperti e scoperti</li>
      <li>{icon("check",18)} Circa 200 m dal terminal</li>
    </ul>
    <div class="mp-chips" role="group" aria-label="Percorsi sulla mappa">{chips}</div>
    <ol class="pm-steps">
      <li data-pm="auto"><strong>In auto</strong> — {esc(DESC["auto"].split(": ",1)[1])}</li>
      <li data-pm="piedi"><strong>A piedi</strong> — {esc(DESC["piedi"].split(": ",1)[1])}</li>
    </ol>
    <div class="actions">{links}</div>
    <div hidden><span data-pm-text="base">{esc(desc.split(" In auto:")[0])}</span><span data-pm-text="auto">{esc(DESC["auto"])}</span><span data-pm-text="piedi">{esc(DESC["piedi"])}</span></div>
  </div>
  <figure class="pm-fig">
    <svg class="pm-svg" viewBox="0 0 640 440" role="img" aria-labelledby="pm-t pm-d" xmlns="http://www.w3.org/2000/svg">
      <title id="pm-t">Come arrivare a Promo Parking by Sun Lines</title>
      <desc id="pm-d">{esc(desc)}</desc>
      <defs><pattern id="pm-stripes" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#E3ECF4"/><rect width="10" height="3" fill="#D6E3EE"/></pattern></defs>
      <rect width="640" height="440" fill="#F7F4EE"/>
      <!-- airport grounds -->
      <path d="M400 150 L640 90 L640 440 L330 440 Z" fill="url(#pm-stripes)"/>
      <path d="M410 440 L640 262 L640 314 L478 440 Z" fill="#C9D6E2"/>
      <text class="pm-lbl pm-lbl-muted" x="560" y="372" text-anchor="middle" transform="rotate(-37 560 372)">Pista</text>
      <!-- roads -->
      <path class="pm-road pm-road-major" d="M-10 60 L120 62 C200 64 280 40 360 -10"/>
      <text class="pm-lbl pm-lbl-road" x="14" y="44">SS729 · Olbia centro, Sassari</text>
      <path class="pm-road" d="M120 62 C130 150 150 230 172 282"/>
      <text class="pm-lbl pm-lbl-road" x="112" y="190" text-anchor="end">SP24</text>
      <path class="pm-road" d="M60 440 C100 390 140 330 168 300"/>
      <circle class="pm-rbt" cx="180" cy="290" r="16"/>
      <path class="pm-road" d="M196 288 C250 276 300 266 330 258 C370 248 400 240 418 236"/>
      <circle class="pm-rbt" cx="428" cy="234" r="10"/>
      <path class="pm-road pm-road-minor" d="M330 258 L324 210"/>
      <text class="pm-lbl pm-lbl-road" x="236" y="306" transform="rotate(-12 236 306)">Via degli Aviatori</text>
      <text class="pm-lbl pm-lbl-road pm-small" x="340" y="244">Via dei Fornai</text>
      <!-- terminal -->
      <rect x="436" y="186" width="196" height="60" rx="6" fill="#0B2545"/>
      <text class="pm-lbl pm-lbl-inv" x="534" y="211" text-anchor="middle">Terminal</text>
      <text class="pm-lbl pm-lbl-inv pm-small" x="534" y="230" text-anchor="middle">Aeroporto Olbia Costa Smeralda</text>
      <!-- routes -->
      <path class="pm-route pm-route-auto" data-pm="auto" d="M-10 60 L120 62 C130 150 150 230 172 282 Q180 296 196 292 C250 278 300 266 330 258 L325 214"/>
      <path class="pm-route pm-route-piedi" data-pm="piedi" d="M336 204 C376 204 406 210 436 214"/>
      <text class="pm-lbl pm-walk" data-pm="piedi" x="388" y="196" text-anchor="middle">3 min · 200 m</text>
      <!-- parking pin -->
      <g class="pm-pin" transform="translate(324 210)">
        <path d="M0 0 C-16 -18 -22 -28 -22 -40 A22 22 0 1 1 22 -40 C22 -28 16 -18 0 0 Z" fill="#F68221" stroke="#0B2545" stroke-width="2"/>
        <text x="0" y="-32" text-anchor="middle" class="pm-p">P</text>
      </g>
      <g class="pm-callout"><rect x="128" y="150" width="166" height="42" rx="6" fill="#fff" stroke="#0B2545" stroke-width="1.5"/>
        <text class="pm-lbl" x="140" y="168">Promo Parking</text><text class="pm-lbl pm-small" x="140" y="184">by Sun Lines · Via dei Fornai 5</text></g>
      <text class="pm-lbl pm-lbl-muted pm-small" x="630" y="430" text-anchor="end">Mappa schematica, non in scala</text>
    </svg>
  </figure>
</div></section>'''


CSS = """
/* parking location map */
.pm .mp-chips{display:flex;flex-wrap:wrap;gap:8px}
.pm .mp-chip{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 14px;border-radius:999px;border:1px solid var(--hairline);background:var(--white);font:600 15px var(--font);color:var(--muted);cursor:pointer}
.pm .mp-chip[aria-pressed="true"]{color:var(--navy);border-color:var(--navy);background:var(--sand)}
.pm .mp-chip:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.pm-grid{display:grid;gap:28px}
@media (min-width:960px){.pm-grid{grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;gap:40px}}
.pm-info{display:grid;gap:14px;align-content:start}
.pm-info h2,.pm-addr{margin:0}
.pm-facts{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 16px}
.pm-facts li{display:flex;gap:8px;align-items:center;font-size:15px}.pm-facts .i{color:var(--emerald-ink,#0F6E6C);flex:none}
@media (max-width:420px){.pm-facts{grid-template-columns:1fr}}
.pm-steps{margin:0;padding-left:1.2em;display:grid;gap:8px;font-size:15px}
.pm-sw{width:18px;height:4px;border-radius:2px;flex:none;opacity:.35}.mp-chip[aria-pressed="true"] .pm-sw{opacity:1}
.pm-sw-auto{background:#1A75BB}.pm-sw-piedi{background:repeating-linear-gradient(90deg,#F68221 0 4px,transparent 4px 7px)}
.pm-fig{margin:0}
.pm-svg{display:block;width:100%;height:auto;border-radius:var(--r-md);border:1px solid var(--hairline);font-family:var(--font)}
.pm-road{fill:none;stroke:#fff;stroke-width:12;stroke-linecap:round}
.pm-road-major{stroke:#fff;stroke-width:18}
.pm-road-minor{stroke-width:7}
.pm-svg .pm-road{filter:drop-shadow(0 0 0.6px #B9C6D3)}
.pm-rbt{fill:#F7F4EE;stroke:#fff;stroke-width:8}
.pm-route{fill:none;stroke-linecap:round;stroke-linejoin:round;transition:opacity .2s}
.pm-route-auto{stroke:#1A75BB;stroke-width:5}
.pm-route-piedi{stroke:#F68221;stroke-width:4;stroke-dasharray:2 7}
.pm-lbl{font-size:14px;font-weight:600;fill:#0B2545}
.pm-small{font-size:11.5px;font-weight:500}
.pm-lbl-road{font-size:12px;font-weight:600;fill:#4F5B6B;paint-order:stroke;stroke:#F7F4EE;stroke-width:4px;stroke-linejoin:round}
.pm-lbl-inv{fill:#fff}.pm-lbl-muted{fill:#4F5B6B;font-weight:500}
.pm-walk{font-size:13px;fill:#9A4A06;paint-order:stroke;stroke:#fff;stroke-width:4px}
.pm-p{font-size:22px;font-weight:700;fill:#0B2545}
.pm [data-off]{display:none}
"""

JS = r"""
(function(){
  var r=document.querySelector('.pm');if(!r)return;
  var on={auto:true,piedi:true},d=r.querySelector('#pm-d');
  function t(k){var e=r.querySelector('[data-pm-text="'+k+'"]');return e?e.textContent:''}
  r.querySelectorAll('.mp-chip[data-pm]').forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.pm;on[k]=!on[k];b.setAttribute('aria-pressed',on[k]);
    r.querySelectorAll('svg [data-pm="'+k+'"]').forEach(function(el){if(on[k])el.removeAttribute('data-off');else el.setAttribute('data-off','')});
    d.textContent=t('base')+' '+['auto','piedi'].filter(function(x){return on[x]}).map(function(x){return t(x)}).join(' ')})});
})();
"""
