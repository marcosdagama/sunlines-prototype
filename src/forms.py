"""Contact forms: markup, sending and the thank-you page.

Sending goes through a form service that emails each submission to FORM_TO as a formatted table.
Default service: FormSubmit (formsubmit.co) — free, no account. The first submission sends an
activation email to FORM_TO; click the link in it once and every later submission is delivered.

To switch service later, change FORM_ACTION / FORM_AJAX (any service that accepts a normal form
POST and returns JSON works), or point them at Sun Lines' own mail endpoint.
"""
from common import esc, icon, EMAIL, PHONE

FORM_TO = EMAIL                                     # info@sunlines.it
FORM_ACTION = f"https://formsubmit.co/{FORM_TO}"    # normal POST (used when a file is attached)
FORM_AJAX = f"https://formsubmit.co/ajax/{FORM_TO}" # background POST, returns JSON
# After activation FormSubmit gives a random alias for the address: put it in place of FORM_TO
# in the two URLs above, so the email address is no longer readable in the page source.

SUBJECTS = {
    "q-bus": "Preventivo noleggio autobus",
    "q-ncc": "Preventivo transfer e NCC",
    "f-assist": "Richiesta di assistenza",
    "f-reclami": "Reclamo o segnalazione",
    "f-fattura": "Richiesta fattura",
}
AUTORESPONSE = ("Grazie, abbiamo ricevuto la tua richiesta a Sun Lines e ti rispondiamo il prima possibile. "
                f"Per urgenze chiama lo 0789 50885. Questo è un messaggio automatico: per scriverci rispondi a {EMAIL}.")


def form(fid, fields, submit="Invia richiesta", notice="finalita", marketing=False):
    """fields: list of (id, label, type, required); type in text, email, tel, number, date, textarea, file.
    Field names are the visible labels, so the email reads as a clean table."""
    subject = SUBJECTS.get(fid, "Richiesta dal sito")
    has_file = any(t == "file" for _, _, t, _ in fields)
    rows, pending = [], []

    def render(f):
        i, label, typ, req = f
        star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
        r = ' required' if req else ''
        ac = {"email": ' autocomplete="email"', "tel": ' autocomplete="tel"'}.get(typ, '')
        if i.endswith("nome") and typ == "text":
            ac = ' autocomplete="name"'
        name = "email" if typ == "email" else ("attachment" if typ == "file" else esc(label))
        extra = ' accept=".pdf,.jpg,.jpeg,.png"' if typ == "file" else ''
        if typ == "textarea":
            ctl = f'<textarea id="{fid}-{i}" name="{name}"{r}></textarea>'
        else:
            ctl = f'<input id="{fid}-{i}" name="{name}" type="{typ}"{r}{ac}{extra}>'
        hint = '<p class="field-hint" id="{0}-{1}-h">PDF o foto, massimo 5 MB.</p>'.format(fid, i) if typ == "file" else ''
        if hint:
            ctl = ctl.replace('>', f' aria-describedby="{fid}-{i}-h">', 1)
        return f'<div class="field"><label for="{fid}-{i}">{esc(label)}{star}</label>{ctl}{hint}</div>'

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

    mk = (f'<label class="check" for="{fid}-mkt"><input id="{fid}-mkt" name="Consenso offerte via email" type="checkbox" value="Sì"> '
          f'<span>Facoltativo: voglio ricevere offerte e novità di Sun Lines via email. Posso revocare il consenso in ogni momento.</span></label>' if marketing else "")
    enctype = ' enctype="multipart/form-data"' if has_file else ''
    return f'''<form class="form" id="{fid}" action="{FORM_ACTION}" method="post"{enctype} data-send="{'post' if has_file else 'ajax'}" data-ajax="{FORM_AJAX}" data-subject="{esc(subject)}" novalidate>
<input type="hidden" name="_subject" value="Sito Sun Lines · {esc(subject)}">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_autoresponse" value="{esc(AUTORESPONSE)}">
<input type="hidden" name="_next" value="">
<input type="hidden" name="Modulo" value="{esc(subject)}">
<input type="hidden" name="Pagina" value="">
<div class="hp" aria-hidden="true"><label for="{fid}-hp">Non compilare questo campo</label><input id="{fid}-hp" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
{"".join(rows)}
{mk}
<p class="form-privacy small">I dati servono solo a rispondere a questa richiesta. Leggi come li trattiamo nell’<a href="privacy.html#{notice}">informativa privacy</a>.</p>
<div class="actions"><button class="btn btn-primary" type="submit"><span class="btn-label">{esc(submit)}</span></button></div>
<div class="form-msg" role="status" aria-live="polite" tabindex="-1" hidden></div>
<p class="form-req small muted"><span class="req" aria-hidden="true">*</span> Campi obbligatori.</p>
</form>'''


CSS = """
/* forms: sending states */
.hp{position:absolute!important;left:-9999px;width:1px;height:1px;overflow:hidden}
.field input,.field textarea,.form-msg{scroll-margin-top:110px}
.field-hint{margin:0;font-size:14px;color:var(--muted)}
.field input[type=file]{padding:10px;background:var(--white)}
.field.err input,.field.err textarea{border-color:var(--terracotta)}
.field-err{margin:0;font-size:14px;font-weight:600;color:var(--terracotta)}
.form button[aria-busy="true"]{opacity:.75;cursor:progress}
.form-msg{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;padding:14px 16px;border-radius:var(--r-md);border:1px solid var(--hairline);background:var(--white)}
.form-msg:focus{outline:2px solid var(--navy);outline-offset:2px}
.form-msg.ok{border-left:4px solid var(--macchia)}.form-msg.ok .i{color:var(--macchia)}
.form-msg.ko{border-left:4px solid var(--terracotta)}.form-msg.ko .i{color:var(--terracotta)}
.form-msg p{margin:0}
.form-req{margin:0}
"""

JS = r"""
(function(){
  var OK='<svg class="i" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l4 4 10-10"/></svg>';
  var KO='<svg class="i" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17h.01"/></svg>';
  var MAX=5*1024*1024;
  function clearErrs(f){f.querySelectorAll('.field.err').forEach(function(x){x.classList.remove('err');var m=x.querySelector('.field-err');if(m)m.remove();var c=x.querySelector('input,textarea');if(c){c.removeAttribute('aria-invalid');var d=(c.getAttribute('aria-describedby')||'').split(' ').filter(function(t){return t&&t.indexOf('-e')!==t.length-2}).join(' ');if(d)c.setAttribute('aria-describedby',d);else c.removeAttribute('aria-describedby')}})}
  function errText(c){var v=c.validity;if(v.valueMissing)return c.type==='file'?'Allega una copia del biglietto.':'Questo campo è obbligatorio.';
    if(v.typeMismatch&&c.type==='email')return 'Inserisci un’email completa, per esempio nome@dominio.it.';
    if(v.rangeUnderflow||v.badInput)return 'Inserisci un numero valido.';return 'Controlla questo campo.'}
  function markErr(c,msg){var w=c.closest('.field');if(!w)return;w.classList.add('err');var id=c.id+'-e';var p=document.createElement('p');p.className='field-err';p.id=id;p.textContent=msg;w.appendChild(p);
    c.setAttribute('aria-invalid','true');c.setAttribute('aria-describedby',((c.getAttribute('aria-describedby')||'')+' '+id).trim())}
  function validate(f){clearErrs(f);var first=null;
    f.querySelectorAll('input:not([type=hidden]):not([name=_honey]),textarea').forEach(function(c){var bad=!c.checkValidity();
      if(!bad&&c.type==='file'&&c.files&&c.files[0]&&c.files[0].size>MAX){bad=true;markErr(c,'Il file supera 5 MB: allega una versione più leggera.')}
      else if(bad)markErr(c,errText(c));if(bad&&!first)first=c});
    if(first)first.focus();return !first}
  function show(f,kind,html){var m=f.querySelector('.form-msg');m.className='form-msg '+kind;m.innerHTML=(kind==='ok'?OK:KO)+'<div>'+html+'</div>';m.hidden=false;m.focus()}
  function busy(f,on){var b=f.querySelector('button[type=submit]'),l=b.querySelector('.btn-label');if(on){b.dataset.t=l.textContent;l.textContent='Invio in corso…';b.setAttribute('aria-busy','true');b.disabled=true}else{l.textContent=b.dataset.t||l.textContent;b.removeAttribute('aria-busy');b.disabled=false}}
  function prepare(f){var g=function(n){return f.querySelector('input[name="'+n+'"]')};
    g('Pagina').value=location.href.split('#')[0];
    var who=f.querySelector('input[autocomplete=name]');var d=new Date();var when=d.toLocaleDateString('it-IT')+' '+d.toLocaleTimeString('it-IT',{hour:'2-digit',minute:'2-digit'});
    g('_subject').value='Sito Sun Lines · '+f.dataset.subject+(who&&who.value?' · '+who.value.trim():'')+' · '+when;
    g('_next').value=new URL('grazie.html',location.href).href}
  var FALLBACK='Riprova tra poco oppure scrivi a <a href="mailto:info@sunlines.it">info@sunlines.it</a> o chiama lo <a href="tel:+39078950885">0789 50885</a>.';
  document.querySelectorAll('form[data-send]').forEach(function(f){
    f.addEventListener('submit',function(e){
      if(!validate(f)){e.preventDefault();return}
      if(f.querySelector('input[name=_honey]').value){e.preventDefault();return}
      prepare(f);
      if(f.dataset.send==='post'){busy(f,true);return}   /* file attached: normal POST, the service redirects to grazie.html */
      e.preventDefault();busy(f,true);
      var fd=new FormData(f);f.querySelectorAll('input[type=date]').forEach(function(c){if(c.value){var a=c.value.split('-');fd.set(c.name,a[2]+'/'+a[1]+'/'+a[0])}});var mk=f.querySelector('input[name="Consenso offerte via email"]');if(mk&&!mk.checked)fd.append(mk.name,'No');
      var ctl=('AbortController' in window)?new AbortController():null;var to=setTimeout(function(){if(ctl)ctl.abort()},20000);
      fetch(f.dataset.ajax,{method:'POST',body:fd,headers:{'Accept':'application/json'},signal:ctl?ctl.signal:undefined})
        .then(function(r){return r.json().catch(function(){return {}}).then(function(j){return {ok:r.ok,j:j}})})
        .then(function(x){clearTimeout(to);busy(f,false);
          if(x.ok&&String(x.j.success)!=='false'){f.reset();show(f,'ok','<p><strong>Richiesta inviata.</strong></p><p class="small">Ti abbiamo mandato una conferma via email e ti rispondiamo il prima possibile.</p>')}
          else{show(f,'ko','<p><strong>Non siamo riusciti a inviare la richiesta.</strong></p><p class="small">'+FALLBACK+'</p>')}})
        .catch(function(){clearTimeout(to);busy(f,false);show(f,'ko','<p><strong>Connessione non riuscita.</strong></p><p class="small">'+FALLBACK+'</p>')});
    });
  });
})();
"""


def grazie_page(page):
    body = f'''
<section class="section"><div class="wrap" style="display:grid;gap:18px;max-width:720px">
  <p class="label eyebrow">Richiesta inviata</p>
  <h1 class="h1">Grazie, abbiamo ricevuto la tua richiesta</h1>
  <p class="lead">Ti abbiamo mandato una conferma via email e ti rispondiamo il prima possibile. Per urgenze chiama lo <strong class="tnum">0789 50885</strong>.</p>
  <div class="actions"><a class="btn btn-primary" href="index.html">Torna alla home</a><a class="btn btn-outline" href="domande-frequenti.html">Domande frequenti</a></div>
</div></section>'''
    html = page(slug="grazie", title="Richiesta inviata | Sun Lines", desc="Conferma di invio della richiesta a Sun Lines.",
                canonical_path="/grazie", active=None, body=body, ld="")
    return html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
