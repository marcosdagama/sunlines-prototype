"""Home hero: 5-photo fleet carousel (WAI-ARIA carousel pattern).

Swipe or use the arrows and dots; auto-advances every 6 s with a pause button, stops for good after
any manual navigation, and never auto-advances when the device asks for reduced motion.
Edit SLIDES to change photos (files in docs/img/flotta/).
"""
from common import esc, icon

SLIDES = [
    ("irizar-blu-costa-smeralda", "Autobus Sun Lines da 50 posti lungo la Costa Smeralda", "Noleggio bus", "Gruppi fino a 50 posti", "noleggio-autobus.html"),
    ("classe-v", "Mercedes Classe V Sun Lines davanti a una villa sul mare", "Transfer e NCC", "Transfer privati con auto e conducente", "transfer-ncc.html"),
    ("sprinter-costa", "Minibus Mercedes Sprinter Sun Lines su una strada costiera", "Minibus", "Escursioni e transfer fino a 20 posti", "noleggio-autobus.html"),
    ("irizar-verde-tramonto", "Pullman Sun Lines verde sulla costa al tramonto", "Escursioni", "Tour e gite in tutta la Sardegna", "noleggio-autobus.html"),
    ("bus-olbia-ruota", "Autobus Sun Lines al porto di Olbia, accanto alla ruota panoramica", "Linee e Airbus 90", "Da Olbia a Sassari, Alghero e la Gallura", "linee-e-orari.html"),
]


def carousel():
    n = len(SLIDES)
    slides = "".join(
        f'''<figure class="hc-slide" id="hc-s{i}" role="group" aria-roledescription="slide" aria-label="{i + 1} di {n}: {esc(tag)}">
  <img src="img/flotta/{src}.jpg" alt="{esc(alt)}" width="800" height="450" loading="{"eager" if i == 0 else "lazy"}" decoding="async"{' fetchpriority="high"' if i == 0 else ''}>
  <figcaption><span class="hc-tag">{esc(tag)}</span><a class="hc-cap" href="{href}">{esc(cap)} {icon("arrow", 16)}</a></figcaption>
</figure>'''
        for i, (src, alt, tag, cap, href) in enumerate(SLIDES))
    dots = "".join(f'<button type="button" class="hc-dot" data-i="{i}" aria-label="Foto {i + 1} di {n}: {esc(tag)}"{" aria-current=\"true\"" if i == 0 else ""}></button>'
                   for i, (_, _, tag, _, _) in enumerate(SLIDES))
    return f'''<section class="hc" aria-roledescription="carousel" aria-label="La flotta Sun Lines">
  <div class="hc-track" tabindex="0" aria-label="Foto della flotta, scorri per vederle tutte">{slides}</div>
  <div class="hc-bar">
    <button type="button" class="hc-btn hc-play" aria-label="Metti in pausa" data-on="1">{icon("pause", 18)}{icon("play", 18)}</button>
    <div class="hc-dots" role="group" aria-label="Scegli la foto">{dots}</div>
    <button type="button" class="hc-btn hc-prev" aria-label="Foto precedente">{icon("chevl", 20)}</button>
    <button type="button" class="hc-btn hc-next" aria-label="Foto successiva">{icon("chevr", 20)}</button>
  </div>
</section>'''


CSS = """
/* hero carousel */
.hc{position:relative;display:grid;gap:12px;min-width:0}
.hc-track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;border-radius:var(--r-md);scrollbar-width:none;aspect-ratio:4/3;max-width:100%;background:var(--navy)}
.hc-track::-webkit-scrollbar{display:none}
.hc-track:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
.hc-slide{position:relative;flex:0 0 100%;margin:0;scroll-snap-align:start;scroll-snap-stop:always}
.hc-slide img{display:block;width:100%;height:100%;object-fit:cover}
.hc-slide figcaption{position:absolute;left:0;right:0;bottom:0;display:grid;gap:4px;justify-items:start;padding:48px 18px 16px;background:linear-gradient(180deg,rgba(11,37,69,0),rgba(11,37,69,.82))}
.hc-tag{font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--orange);color:var(--navy);padding:3px 8px;border-radius:4px}
.hc-cap{color:#fff;font-weight:600;font-size:17px;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.hc-cap:hover{text-decoration:underline}.hc-cap:focus-visible{outline:2px solid #fff;outline-offset:3px}
.hc-bar{display:flex;align-items:center;gap:8px}
.hc-dots{display:flex;gap:2px;margin-right:auto}
.hc-dot{width:32px;height:44px;border:0;background:none;cursor:pointer;padding:0;display:grid;place-items:center}
.hc-dot::before{content:"";width:22px;height:4px;border-radius:2px;background:var(--hairline);transition:background .2s,width .2s}
.hc-dot[aria-current="true"]::before{background:var(--orange);width:28px}
.hc-dot:hover::before{background:var(--granite)}
.hc-btn{width:44px;height:44px;display:grid;place-items:center;border-radius:50%;border:1px solid var(--hairline);background:var(--white);color:var(--navy);cursor:pointer;flex:none}
.hc-btn:hover{border-color:var(--navy)}
.hc-btn:focus-visible,.hc-dot:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.hc-play .i:last-child{display:none}.hc-play[data-on="0"] .i:first-child{display:none}.hc-play[data-on="0"] .i:last-child{display:block}
@media (prefers-reduced-motion:reduce){.hc-track{scroll-behavior:auto}.hc-play{display:none}}
"""

JS = r"""
(function(){
  var c=document.querySelector('.hc');if(!c)return;
  var t=c.querySelector('.hc-track'),s=[].slice.call(c.querySelectorAll('.hc-slide')),d=[].slice.call(c.querySelectorAll('.hc-dot'));
  var play=c.querySelector('.hc-play'),cur=0,timer=null,stopped=false,hold=false;
  var red=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function mark(i){cur=i;d.forEach(function(x,k){x.setAttribute('aria-current',k===i?'true':'false')});
    s.forEach(function(x,k){var on=k===i;x.setAttribute('aria-hidden',on?'false':'true');x.querySelectorAll('a').forEach(function(a){a.tabIndex=on?0:-1})})}
  function go(i){i=(i+s.length)%s.length;t.scrollTo({left:i*t.clientWidth,behavior:red?'auto':'smooth'});mark(i)}
  var raf=null;t.addEventListener('scroll',function(){if(raf)cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){var i=Math.round(t.scrollLeft/Math.max(1,t.clientWidth));if(i!==cur)mark(i)})},{passive:true});
  function tick(){if(!hold&&!stopped&&!document.hidden)go(cur+1)}
  function start(){if(red||stopped)return;clearInterval(timer);timer=setInterval(tick,6000);play.dataset.on='1';play.setAttribute('aria-label','Metti in pausa')}
  function stop(forever){clearInterval(timer);timer=null;if(forever)stopped=true;play.dataset.on='0';play.setAttribute('aria-label','Avvia lo scorrimento automatico')}
  play.addEventListener('click',function(){if(play.dataset.on==='1'){stop(true)}else{stopped=false;start()}});
  c.querySelector('.hc-prev').addEventListener('click',function(){stop(true);go(cur-1)});
  c.querySelector('.hc-next').addEventListener('click',function(){stop(true);go(cur+1)});
  d.forEach(function(x){x.addEventListener('click',function(){stop(true);go(+x.dataset.i)})});
  t.addEventListener('pointerdown',function(){stop(true)});t.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))stop(true)},{passive:true});
  t.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();stop(true);go(cur+1)}else if(e.key==='ArrowLeft'){e.preventDefault();stop(true);go(cur-1)}});
  c.addEventListener('mouseenter',function(){hold=true});c.addEventListener('mouseleave',function(){hold=false});
  c.addEventListener('focusin',function(){hold=true});c.addEventListener('focusout',function(){hold=false});
  window.addEventListener('resize',function(){t.scrollTo({left:cur*t.clientWidth,behavior:'auto'})});
  mark(0);start();
})();
"""
