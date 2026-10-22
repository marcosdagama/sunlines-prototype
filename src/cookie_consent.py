"""Cookie consent banner following the Italian Garante guidelines of 10 June 2021.

- Accept and Reject have equal weight; the X closes and refuses; scrolling never counts as consent.
- Granular choice per category; choice stored for 6 months in a first-party technical cookie (sl_consent).
- Asked again after 6 months or when CONSENT_VERSION changes (bump it when tools are added or removed).
- Scripts that need consent listen for the "sl:consent" event or read window.slConsent.

Set COOKIE_BANNER = False if the live site uses only technical cookies: no banner is then required.
"""
from common import esc, icon

COOKIE_BANNER = True
CONSENT_VERSION = "1"
CATEGORIES = [
    ("necessari", "Necessari", "Fanno funzionare il sito e ricordano le tue scelte sui cookie. Sempre attivi.", True),
    ("statistiche", "Statistiche", "Misurano le visite in forma aggregata per migliorare il sito. Nessuno strumento attivo al momento.", False),
    ("marketing", "Marketing", "Mostrano pubblicità in linea con i tuoi interessi su altri siti. Nessuno strumento attivo al momento.", False),
]


def banner():
    if not COOKIE_BANNER:
        return ""
    rows = "".join(
        f'''<div class="ck-cat"><div><label for="ck-{k}" class="ck-name">{esc(n)}</label><p class="small muted" id="ck-{k}-d">{esc(d)}</p></div>
<input type="checkbox" class="ck-switch" id="ck-{k}" data-cat="{k}" aria-describedby="ck-{k}-d"{" checked disabled" if fixed else ""}></div>'''
        for k, n, d, fixed in CATEGORIES)
    return f'''<section class="ck" id="cookie-banner" role="dialog" aria-labelledby="ck-t" aria-describedby="ck-d" data-version="{CONSENT_VERSION}" hidden>
  <button type="button" class="ck-x" data-ck="reject" aria-label="Chiudi e rifiuta i cookie non necessari">{icon("close", 20)}</button>
  <h2 id="ck-t" tabindex="-1">Cookie e privacy</h2>
  <p id="ck-d" class="small">Usiamo cookie tecnici per far funzionare il sito. Con il tuo consenso useremmo anche cookie di statistica e di marketing. Puoi accettare, rifiutare o scegliere per categoria; chiudendo con la X rifiuti quelli non necessari. <a href="cookie-policy.html">Cookie policy</a></p>
  <div class="ck-prefs" id="ck-prefs" hidden>{rows}</div>
  <div class="ck-actions">
    <button type="button" class="btn ck-btn" data-ck="reject">Rifiuta</button>
    <button type="button" class="btn ck-btn" data-ck="accept">Accetta tutti</button>
    <button type="button" class="ck-link" data-ck="custom" aria-expanded="false" aria-controls="ck-prefs">Personalizza</button>
    <button type="button" class="btn ck-btn" data-ck="save" hidden>Salva le scelte</button>
  </div>
</section>'''


CSS = """
/* cookie consent */
.ck{position:fixed;z-index:90;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));
  max-width:560px;max-height:calc(100vh - 32px);overflow-y:auto;background:var(--white);color:var(--navy);border:1px solid var(--hairline);border-radius:var(--r-md);
  box-shadow:0 12px 40px rgba(11,37,69,.22);padding:20px 20px 16px;display:grid;gap:12px}
.ck h2{margin:0;font-size:20px;padding-right:40px}.ck h2:focus{outline:none}
.ck p{margin:0}
.ck-x{position:absolute;top:8px;right:8px;width:44px;height:44px;display:grid;place-items:center;border:0;background:none;color:var(--navy);border-radius:50%;cursor:pointer}
.ck-x:hover{background:var(--sand)}
.ck-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.ck-btn{flex:1 1 140px;background:var(--navy);color:#fff;border:2px solid var(--navy)}
.ck-btn:hover{background:#13345C;border-color:#13345C}
.ck-link{min-height:44px;padding:8px 6px;border:0;background:none;font:600 15px var(--font);color:var(--link);text-decoration:underline;cursor:pointer}
.ck-prefs{display:grid;gap:4px;border-top:1px solid var(--hairline);padding-top:8px}
.ck-cat{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid var(--hairline)}
.ck-name{font-weight:600}
.ck-switch{appearance:none;-webkit-appearance:none;width:48px;height:28px;border-radius:999px;background:#C3CCD6;position:relative;cursor:pointer;flex:none;margin:0;transition:background .2s}
.ck-switch::after{content:"";position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 1px 2px rgba(0,0,0,.2)}
.ck-switch:checked{background:var(--blue)}.ck-switch:checked::after{transform:translateX(20px)}
.ck-switch:disabled{opacity:.6;cursor:not-allowed}
.ck-switch:focus-visible,.ck button:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
@media (max-width:767px){.ck{left:0;right:0;bottom:0;max-width:none;border-radius:var(--r-md) var(--r-md) 0 0;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))}}
@media (prefers-reduced-motion:reduce){.ck-switch,.ck-switch::after{transition:none}}
.ft-legal-links{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0;padding:0;list-style:none;font-size:14px}
.ft-legal-links a,.ft-legal-links button{color:var(--on-navy);text-decoration:none;background:none;border:0;padding:0;font:inherit;cursor:pointer}
.ft-legal-links a:hover,.ft-legal-links button:hover{color:#fff;text-decoration:underline}
"""

JS = r"""
(function(){
  var b=document.getElementById('cookie-banner');
  var VER=b?b.dataset.version:'1',MAX=180*24*3600*1000,NAME='sl_consent';
  function read(){var v=null;try{var m=document.cookie.match(/(?:^|; )sl_consent=([^;]*)/);if(m)v=JSON.parse(decodeURIComponent(m[1]))}catch(e){}
    if(!v){try{v=JSON.parse(localStorage.getItem(NAME))}catch(e){}}
    if(!v||v.v!==VER||!v.ts||Date.now()-v.ts>MAX)return null;return v}
  function write(c){var v={v:VER,ts:Date.now(),c:c},s=encodeURIComponent(JSON.stringify(v));
    try{document.cookie=NAME+'='+s+'; Max-Age='+(180*24*3600)+'; Path=/; SameSite=Lax'+(location.protocol==='https:'?'; Secure':'')}catch(e){}
    try{localStorage.setItem(NAME,JSON.stringify(v))}catch(e){}
    window.slConsent=c;try{document.dispatchEvent(new CustomEvent('sl:consent',{detail:c}))}catch(e){}}
  var saved=read();window.slConsent=saved?saved.c:{necessari:true};
  if(!b)return;
  var prefs=b.querySelector('#ck-prefs'),cust=b.querySelector('[data-ck="custom"]'),save=b.querySelector('[data-ck="save"]');
  var opener=null;
  function sync(c){b.querySelectorAll('.ck-switch:not([disabled])').forEach(function(s){s.checked=!!(c&&c[s.dataset.cat])})}
  function open(expand,from){opener=from||null;sync(window.slConsent);b.hidden=false;showPrefs(!!expand);if(from)b.querySelector('#ck-t').focus()}
  function close(){b.hidden=true;if(opener){opener.focus();opener=null}}
  function showPrefs(on){prefs.hidden=!on;save.hidden=!on;cust.hidden=on;cust.setAttribute('aria-expanded',on)}
  function all(val){var c={necessari:true};b.querySelectorAll('.ck-switch:not([disabled])').forEach(function(s){c[s.dataset.cat]=val});return c}
  b.addEventListener('click',function(e){var t=e.target.closest('[data-ck]');if(!t)return;var a=t.dataset.ck;
    if(a==='custom'){showPrefs(true);var f=prefs.querySelector('.ck-switch:not([disabled])');if(f)f.focus();return}
    if(a==='accept')write(all(true));
    else if(a==='reject')write(all(false));
    else if(a==='save'){var c={necessari:true};b.querySelectorAll('.ck-switch:not([disabled])').forEach(function(s){c[s.dataset.cat]=s.checked});write(c)}
    close()});
  b.addEventListener('keydown',function(e){if(e.key==='Escape'&&opener){close()}});
  document.querySelectorAll('[data-cookie-prefs]').forEach(function(x){x.addEventListener('click',function(){open(true,x)})});
  if(!saved)open(false);
})();
"""
