from common import *

CSS = r"""
/* Layout: sticky white header, sand page, white cards, one navy footer; mobile gets a fixed contact bar. Single light look, like the real operator site. */
:root{
  --blue:#1A75BB; --link:#0E5F96; --orange:#F68221; --navy:#0B2545; --sand:#F2F6F9;
  --white:#FFFFFF; --muted:#4F5B6B; --emerald:#1FA3A0; --emerald-ink:#0F6E6C; --terracotta:#B5462F;
  --macchia:#4F6B3A; --granite:#7D8794; --hairline:#DCE3EA; --wa:#25D366; --on-navy:#C9D3E0;
  --font:"Barlow","Helvetica Neue",Arial,sans-serif;
  --r-sm:4px; --r-md:10px;
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{background:var(--sand);color:var(--navy);font-family:var(--font);font-size:17px;line-height:1.53;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:60;background:var(--white)}
a{color:var(--link)}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--navy);outline-offset:2px;border-radius:2px}
img{max-width:100%;display:block}
h1,h2,h3{margin:0;text-wrap:balance;letter-spacing:-0.005em}
p{margin:0}
.wrap{max-width:1200px;margin-inline:auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.skip{position:absolute;left:-999px;top:8px;background:var(--navy);color:var(--white);padding:8px 12px;z-index:100}
.skip:focus{left:16px}
.i{flex:none}

/* type scale */
.display{font-size:clamp(36px,6vw,52px);line-height:1.06;font-weight:700;letter-spacing:-0.01em}
.h1{font-size:clamp(30px,4.6vw,38px);line-height:1.12;font-weight:700}
.h2{font-size:clamp(24px,3.4vw,28px);line-height:1.2;font-weight:700}
.h3{font-size:20px;line-height:1.3;font-weight:600}
.lead{font-size:clamp(18px,2.2vw,20px);line-height:1.5;color:var(--navy);max-width:62ch}
.small{font-size:15px;line-height:1.45}
.muted{color:var(--muted)}
.label{font-size:13px;line-height:16px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.prose{display:grid;gap:14px;max-width:68ch}
.prose ul,.prose ol{margin:0;padding-left:1.2em;display:grid;gap:6px}
.prose h3{margin-top:10px}
.tnum{font-variant-numeric:tabular-nums}

/* header */
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:50;background:var(--white);border-bottom:1px solid var(--hairline)}
.hdr{display:flex;align-items:center;gap:24px;min-height:72px}
.logo{display:block;flex:none}
.logo img{height:44px;width:auto}
.mainnav{display:flex;gap:4px;margin-left:auto}
.mainnav a{color:var(--navy);text-decoration:none;font-weight:600;font-size:16px;padding:10px 12px;border-radius:var(--r-sm)}
.mainnav a:hover{background:var(--sand)}
.mainnav a[aria-current="page"]{color:var(--blue);box-shadow:inset 0 -3px 0 var(--orange)}
.hdr-tools{display:flex;align-items:center;gap:10px}
.langmenu{position:relative}
.langmenu summary{list-style:none;display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:8px 10px;border:1px solid var(--hairline);border-radius:var(--r-md);font-weight:600;font-size:15px;color:var(--navy);cursor:pointer;background:var(--white)}
.langmenu summary::-webkit-details-marker{display:none}
.langmenu summary:hover{border-color:var(--blue)}
.langmenu[open] summary .i:last-child{transform:rotate(180deg)}
.langmenu .lang-list{position:absolute;right:0;top:calc(100% + 6px);z-index:70;min-width:220px;background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md);box-shadow:0 8px 24px rgba(11,37,69,.12);padding:6px}
.lang-list{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.lang-list a,.lang-list span{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:44px;padding:10px 12px;border-radius:var(--r-sm);text-decoration:none;color:var(--navy);font-weight:500}
.lang-list a:hover{background:var(--sand)}
.lang-list a[aria-current]{font-weight:700;color:var(--blue)}
.lang-list span{color:var(--muted);cursor:default}
.lang-list small{font-size:12px;font-weight:600;color:var(--muted);background:var(--sand);border-radius:999px;padding:2px 8px}
.drawer-lang{display:grid;gap:8px}
.menu-btn{display:none;margin-left:auto;align-items:center;gap:6px;background:none;border:1px solid var(--hairline);border-radius:var(--r-md);padding:10px 12px;font:600 16px var(--font);color:var(--navy);min-height:44px}
@media (max-width:1079px){.mainnav,.hdr-tools .btn{display:none}.hdr-tools{margin-left:auto}.menu-btn{display:inline-flex;margin-left:0}.hdr{gap:10px}.logo img{height:38px}.hdr{min-height:64px}}

/* drawer */
.drawer{position:fixed;inset:0;z-index:80;background:rgba(11,37,69,.45)}
.drawer-panel{position:absolute;top:0;right:0;bottom:0;width:min(360px,100%);background:var(--white);display:flex;flex-direction:column;gap:20px;
  padding-top:calc(16px + env(safe-area-inset-top,0px));padding-bottom:calc(24px + env(safe-area-inset-bottom,0px));padding-left:24px;padding-right:max(24px,env(safe-area-inset-right,0px));overflow-y:auto}
.drawer-top{display:flex;justify-content:space-between;align-items:center}
.drawer nav{display:grid}
.drawer nav a{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--hairline);color:var(--navy);text-decoration:none;font-size:20px;font-weight:600}
.drawer nav a[aria-current="page"]{color:var(--blue)}
.drawer .contact-list{display:grid;gap:10px}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:12px 20px;border-radius:var(--r-md);font:600 16px/1.2 var(--font);text-decoration:none;border:2px solid transparent;cursor:pointer}
.btn-primary{background:var(--blue);color:var(--white)}
.btn-primary:hover{background:#155f99}
.btn-outline{background:var(--white);color:var(--link);border-color:var(--blue)}
.btn-outline:hover{background:var(--sand)}
.btn-wa{background:var(--wa);color:var(--navy);border-radius:999px}
.btn-wa:hover{background:#1fbe5b}
.btn-sm{min-height:40px;padding:8px 14px;font-size:15px}
.actions{display:flex;flex-wrap:wrap;gap:12px}

/* stripes: the logo's sun bands, one per screen at most */
.stripes{display:block;width:72px;height:30px;background:repeating-linear-gradient(to bottom,var(--orange) 0 6px,transparent 6px 12px)}

/* sections */
.section{padding-block:56px}
.section-tight{padding-block:36px}
.section-white{background:var(--white)}
.sec-head{display:grid;gap:10px;margin-bottom:28px;max-width:70ch}
.eyebrow{color:var(--terracotta)}
@media (max-width:767px){.section{padding-block:40px}}

/* hero */
.hero{padding-block:48px 56px}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:40px;align-items:center}
.hero-copy{display:grid;gap:18px}
@media (max-width:899px){.hero-grid{grid-template-columns:1fr}.hero{padding-block:28px 40px}}
.page-hero{padding-block:28px 40px}
.page-hero .hero-grid{align-items:end}

/* audience doors */
.doors{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
@media (max-width:899px){.doors{grid-template-columns:1fr}}
.door{display:grid;gap:10px;align-content:start;background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md);padding:20px;text-decoration:none;color:var(--navy)}
.door:hover{border-color:var(--blue)}
.door .door-ic{width:40px;height:40px;border-radius:999px;display:grid;place-items:center;background:var(--sand);color:var(--blue)}
.door .links{display:grid;gap:6px;margin-top:4px}
.door .links a{display:flex;align-items:center;justify-content:space-between;gap:8px;font-weight:600;text-decoration:none;color:var(--link);padding:6px 0;border-top:1px solid var(--hairline)}

/* cards */
.grid{display:grid;gap:20px}
.grid-2{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.grid-4{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:1079px){.grid-4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:899px){.grid-3{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.grid-2,.grid-3,.grid-4{grid-template-columns:1fr}}
.card{background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md);overflow:hidden;display:flex;flex-direction:column;min-width:0}
.card-body{padding:20px;display:flex;flex-direction:column;gap:10px;flex:1}
.card-body .btn,.card-body .more{margin-top:auto}
.more{display:inline-flex;align-items:center;gap:6px;font-weight:600;text-decoration:none;color:var(--link)}
.panel{background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md);padding:24px;display:grid;gap:14px;min-width:0}

/* photo placeholder */
.ph{position:relative;margin:0;width:100%;max-width:100%;background:var(--navy);overflow:hidden;display:flex;align-items:flex-start;color:var(--white)}
.card .ph{border-radius:0}
.hero .ph,.page-hero .ph,.ph.rounded{border-radius:var(--r-md)}
.ph-sun{position:absolute;right:8%;bottom:-30%;width:42%;aspect-ratio:1;border-radius:50%;
  background:repeating-linear-gradient(to bottom,var(--orange) 0 14%,transparent 14% 17%);opacity:.9}
.ph-shoot{background:#24364F}
.ph-shoot .ph-sun{opacity:.35}
.ph figcaption{position:relative;display:grid;gap:4px;padding:14px 16px;max-width:88%}
.ph-tag{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--white)}
.ph-shoot .ph-tag{color:var(--orange)}
.ph-cap{font-size:15px;line-height:1.3;color:var(--on-navy)}

.pic{position:relative;margin:0;width:100%;max-width:100%;overflow:hidden;background:var(--sand)}
.pic img{width:100%;height:100%;object-fit:cover}
.hero .pic,.page-hero .pic,.prose .pic,.grid>.pic,.panel .pic{border-radius:var(--r-md)}
.pic .credit{position:absolute;right:8px;bottom:8px;font-size:11px;line-height:1.3;background:rgba(11,37,69,.72);color:var(--white);padding:2px 6px;border-radius:3px}
/* alerts */
.alerts{display:grid;gap:16px}
.alert{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px;background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md);padding:18px 20px}
.alert-ic{width:36px;height:36px;border-radius:999px;display:grid;place-items:center;background:var(--terracotta);color:var(--white)}
.alert-ic.info{background:var(--blue)}
.alert h3{font-size:18px;font-weight:600;margin-bottom:4px}

/* line badges */
.line{display:grid;grid-template-columns:auto minmax(0,1fr);gap:16px;align-items:start}
.badge{min-width:52px;height:52px;padding:0 8px;border-radius:var(--r-sm);display:grid;place-items:center;background:var(--navy);color:var(--white);font-weight:700;font-size:22px;font-variant-numeric:tabular-nums}
.badge.b90{background:var(--blue)}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--sand);color:var(--navy)}
.pill.season{background:#E3F1F0;color:var(--emerald-ink);border-radius:var(--r-sm)}
.stops{color:var(--muted);font-size:15px}

/* faq */
.faq{display:grid;gap:10px}
.faq details{background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md)}
.faq summary{cursor:pointer;list-style:none;padding:16px 48px 16px 20px;font-weight:600;font-size:17px;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:20px;top:12px;font-size:24px;font-weight:400;color:var(--blue)}
.faq details[open] summary::after{content:"–"}
.faq .ans{padding:0 20px 18px;display:grid;gap:10px;max-width:72ch}
.faq-group{display:grid;gap:12px}
.faq-group+.faq-group{margin-top:28px}

/* quick answers */
.faq .ans .short{font-weight:600;color:var(--navy)}
.faq details[hidden]{display:none}
.faq-search{display:flex;align-items:center;gap:10px;background:var(--white);border:2px solid var(--blue);border-radius:var(--r-md);padding:0 14px;max-width:640px;color:var(--blue)}
.faq-search input{flex:1;min-width:0;border:0;outline:0;font:400 18px var(--font);padding:14px 0;color:var(--navy);background:transparent}
.faq-search:focus-within{outline:2px solid var(--navy);outline-offset:2px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;min-height:40px;padding:8px 14px;border-radius:999px;background:var(--white);border:1px solid var(--hairline);color:var(--navy);text-decoration:none;font-weight:600;font-size:15px}
.chip:hover{border-color:var(--blue);color:var(--blue)}
.dest{overflow-x:auto;border:1px solid var(--hairline);border-radius:var(--r-md);background:var(--white)}
.dest table{width:100%;border-collapse:collapse;min-width:480px}
.dest th{text-align:left;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:12px 16px;border-bottom:1px solid var(--hairline)}
.dest td{padding:12px 16px;border-bottom:1px solid var(--hairline);vertical-align:middle}
.dest tr:last-child td{border-bottom:0}
.badge-sm{display:inline-grid;place-items:center;min-width:40px;height:32px;padding:0 8px;border-radius:var(--r-sm);background:var(--navy);color:var(--white);font-weight:700;text-decoration:none;font-variant-numeric:tabular-nums}
.badge-sm.b90{background:var(--blue)}
.dest-when{display:none}
@media (max-width:600px){.dest table{min-width:0}.dest-col{display:none}.dest-when{display:block;font-size:14px;color:var(--muted);margin-top:2px}.dest td,.dest th{padding:12px}}
/* forms */
.form{display:grid;gap:16px}
.field{display:grid;gap:6px}
.field label{font-size:14px;font-weight:500}
.field input,.field textarea,.field select{font:400 17px var(--font);color:var(--navy);background:var(--white);border:1px solid var(--granite);border-radius:var(--r-sm);padding:12px 14px;min-height:48px;width:100%}
.field textarea{min-height:120px;resize:vertical}
.field input:focus,.field textarea:focus{outline:2px solid var(--navy);outline-offset:1px;border-color:var(--navy)}
.field-row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
@media (max-width:640px){.field-row{grid-template-columns:1fr}}
.check{display:flex;gap:10px;align-items:flex-start;font-size:15px}
.check input{width:20px;height:20px;margin-top:2px;flex:none}
.req{color:var(--terracotta)}
.form-note{font-size:15px;color:var(--macchia);font-weight:600}
.proto-note{font-size:14px;color:var(--muted)}

/* breadcrumbs */
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px;font-size:14px;color:var(--muted)}
.crumbs li+li::before{content:"/";margin-right:6px;color:var(--granite)}
.crumbs a{color:var(--muted)}

/* contact strip */
.contact-strip{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
@media (max-width:899px){.contact-strip{grid-template-columns:1fr}}
.cbox{display:grid;gap:6px;background:var(--white);border:1px solid var(--hairline);border-radius:var(--r-md);padding:18px 20px}
.cbox .val{font-size:20px;font-weight:700;user-select:all}

/* partners */
.partners{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.partner{border:1px solid var(--hairline);border-radius:var(--r-sm);padding:10px 16px;font-weight:700;letter-spacing:.04em;color:var(--muted);background:var(--white)}

/* footer */
.site-footer{position:relative;overflow:hidden;background:var(--navy);color:var(--white);padding-block:0 28px}
.ft-stripes{display:grid;gap:3px;margin-bottom:56px}
.ft-stripes i{display:block;background:var(--orange)}.ft-stripes i:nth-child(1){height:6px}.ft-stripes i:nth-child(2){height:3px;opacity:.75}.ft-stripes i:nth-child(3){height:1.5px;opacity:.5}
.ft-sun{position:absolute;right:-90px;bottom:-110px;width:420px;height:420px;opacity:.07;pointer-events:none}
.site-footer .wrap{position:relative}
.ft-top{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:48px;align-items:start;padding-bottom:48px;border-bottom:1px solid rgba(255,255,255,.12)}
.ft-brand{display:grid;gap:16px;align-content:start;max-width:440px}
.ft-brand img{height:46px;width:auto}
.ft-claim{margin:8px 0 0;font-size:clamp(26px,3vw,34px);line-height:1.15;font-weight:500;letter-spacing:-.01em}
.ft-sub{margin:0;color:var(--on-navy);font-size:16px}
.ft-contact{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.ft-contact a{display:flex;gap:12px;align-items:center;min-height:64px;padding:12px 14px;border:1px solid rgba(255,255,255,.12);border-radius:var(--r-md);color:var(--white);text-decoration:none;background:rgba(255,255,255,.03);transition:background .2s,border-color .2s}
.ft-contact a:hover{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.28)}
.ft-contact small{display:block;font-size:13px;color:var(--on-navy);margin-bottom:2px}
.ft-contact a>span:last-child{font-weight:600;min-width:0;overflow-wrap:anywhere}
.ft-ic{flex:none;display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:rgba(246,130,33,.14);color:var(--orange)}
.ft-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;padding-block:40px}
.site-footer h2{margin:0 0 14px;font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--on-navy)}
.ft-col ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.ft-col a{color:var(--white);text-decoration:none;font-size:16px;background:linear-gradient(var(--orange),var(--orange)) 0 100%/0 1.5px no-repeat;transition:background-size .25s;padding-bottom:2px}
.ft-col a:hover,.ft-col a:focus-visible{background-size:100% 1.5px}
.ft-assoc{display:flex;flex-wrap:wrap;align-items:center;gap:16px 32px;padding-block:28px;border-top:1px solid rgba(255,255,255,.12)}
.ft-assoc p{margin:0;font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--on-navy)}
.ft-assoc ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;gap:20px 36px}
.ft-assoc img{display:block;height:52px;width:auto;opacity:.82;transition:opacity .2s}
.ft-assoc li:hover img{opacity:1}
.ft-legal{display:flex;flex-wrap:wrap;gap:16px 24px;justify-content:space-between;align-items:center;padding-top:24px;border-top:1px solid rgba(255,255,255,.12)}
.ft-legal p{margin:0;font-size:14px;color:var(--on-navy)}.ft-br{display:none}
.ft-social{display:flex;gap:8px;align-items:center}
.ft-social a{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.2);color:var(--white)}
.ft-social a:hover{border-color:var(--orange);color:var(--orange)}
.ft-social .ft-up{width:auto;display:inline-flex;gap:6px;padding:0 16px;border-radius:999px;font-size:14px;font-weight:600;text-decoration:none;margin-left:8px}
.site-footer a:focus-visible{outline:2px solid var(--orange);outline-offset:3px}
@media (max-width:959px){.ft-top{grid-template-columns:1fr;gap:32px}}
@media (max-width:599px){.ft-stripes{margin-bottom:40px}.ft-contact{grid-template-columns:1fr}.ft-links{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 20px}.ft-links .ft-col:last-child{grid-column:1/-1}
  .ft-legal{flex-direction:column;align-items:flex-start}.ft-assoc ul{gap:16px 28px}.ft-assoc img{height:42px}.ft-sun{width:300px;height:300px;right:-110px;bottom:40px}}

/* mobile contact bar */
.mbar{display:none}
@media (max-width:767px){
  .mbar{display:grid;grid-template-columns:1fr 1fr 1.4fr;gap:8px;position:fixed;left:0;right:0;bottom:0;z-index:40;background:var(--white);border-top:1px solid var(--hairline);
    padding-top:8px;padding-bottom:calc(8px + env(safe-area-inset-bottom,0px));padding-left:max(12px,env(safe-area-inset-left,0px));padding-right:max(12px,env(safe-area-inset-right,0px))}
  .mbar a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:52px;border-radius:var(--r-md);text-decoration:none;font-weight:600;font-size:14px;color:var(--navy);background:var(--sand)}
  .mbar a.wa{background:var(--wa)}
  .mbar a.cta{background:var(--blue);color:var(--white);flex-direction:row;gap:8px;font-size:16px}
  body{padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
}
"""

JS = r"""
(function(){
  var btn=document.getElementById('menu-open'),dr=document.getElementById('drawer'),cl=document.getElementById('menu-close');
  function open(){dr.hidden=false;btn.setAttribute('aria-expanded','true');document.body.style.overflow='hidden';cl.focus()}
  function close(){dr.hidden=true;btn.setAttribute('aria-expanded','false');document.body.style.overflow='';btn.focus()}
  if(btn){btn.addEventListener('click',open);cl.addEventListener('click',close);
    dr.addEventListener('click',function(e){if(e.target===dr)close()});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!dr.hidden)close()});}
  var lm=document.querySelector('.langmenu');
  if(lm){document.addEventListener('click',function(e){if(lm.open&&!lm.contains(e.target))lm.open=false});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lm.open){lm.open=false;lm.querySelector('summary').focus()}});}
  document.querySelectorAll('form[data-proto]').forEach(function(f){
    f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.form-note');
      if(!f.checkValidity()){f.reportValidity();return}
      n.hidden=false;n.textContent='Prototipo: il modulo funziona come esempio e non invia dati.';});
  });
})();
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&display=swap">'


def lang_items():
    out = []
    for code, name, ok in LANGS:
        if code == CURRENT_LANG:
            out.append(f'<li><a href="index.html" lang="{code}" hreflang="{code}" aria-current="true">{name}{icon("check",16)}</a></li>')
        elif ok:
            out.append(f'<li><a href="{code}/index.html" lang="{code}" hreflang="{code}">{name}</a></li>')
        else:
            out.append(f'<li><span lang="{code}" aria-disabled="true">{name}<small>in arrivo</small></span></li>')
    return "".join(out)


def lang_menu():
    cur_name = dict((c, n) for c, n, _ in LANGS)[CURRENT_LANG]
    return (f'<details class="langmenu"><summary aria-label="Lingua: {cur_name}. Cambia lingua">{icon("globe",18)}<span>{CURRENT_LANG.upper()}</span>{icon("chev",16)}</summary>'
            f'<ul class="lang-list">{lang_items()}</ul></details>')


def cur(k, active):
    return ' aria-current="page"' if k == active else ''


def header(active):
    links = "".join(
        f'<a href="{h}"{cur(k, active)}>{esc(t)}</a>' for h, t, k in NAV)
    dlinks = "".join(
        f'<a href="{h}"{cur(k, active)}>{esc(t)}{icon("arrow",18)}</a>' for h, t, k in NAV)
    return f'''<a class="skip" href="#main">Vai al contenuto</a>
<header class="site-header"><div class="wrap hdr">
  <a class="logo" href="index.html" aria-label="Sun Lines, home"><img src="sun-lines-logo.svg" alt="Sun Lines Elite Service" width="149" height="40"></a>
  <nav class="mainnav" aria-label="Principale">{links}</nav>
  <div class="hdr-tools">
    {lang_menu()}
    <a class="btn btn-primary btn-sm" href="airbus-olbia-sassari-alghero.html#biglietti">{icon("ticket",18)} Biglietti Airbus</a>
  </div>
  <button class="menu-btn" id="menu-open" type="button" aria-controls="drawer" aria-expanded="false">{icon("menu",22)} Menu</button>
</div></header>
<div class="drawer" id="drawer" hidden><div class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="drawer-top"><img src="sun-lines-logo.svg" alt="Sun Lines" height="34" style="height:34px;width:auto"><button class="menu-btn" style="display:inline-flex;margin:0" id="menu-close" type="button">{icon("close",22)} Chiudi</button></div>
  <nav aria-label="Principale">{dlinks}</nav>
  <a class="btn btn-primary" href="airbus-olbia-sassari-alghero.html#biglietti">{icon("ticket",18)} Biglietti Airbus 90</a>
  <div class="contact-list">
    <p class="label muted">Contatti</p>
    <p><strong>Telefono</strong> <span class="tnum">{PHONE}</span></p>
    <p><strong>Email</strong> {EMAIL}</p>
    <p><strong>WhatsApp</strong> <span class="tnum">{WA_DISPLAY}</span> <span class="muted small">(solo preventivi e parcheggio)</span></p>
    <a class="btn btn-outline" href="domande-frequenti.html">{icon("help",18)} Domande frequenti</a>
    <a class="btn btn-outline" href="assistenza.html">Assistenza</a>
  </div>
  <div class="drawer-lang"><p class="label muted">Lingua / Language</p><ul class="lang-list">{lang_items()}</ul></div>
</div></div>'''


def footer():
    groups = [
        ("Servizi", [("transfer-ncc.html", "Transfer e NCC"), ("noleggio-autobus.html", "Noleggio autobus"),
                     ("airbus-olbia-sassari-alghero.html", "Airbus Olbia – Alghero"), ("linee-e-orari.html", "Linee e orari"),
                     ("parcheggio-aeroporto-olbia.html", "Parcheggio aeroporto")]),
        ("Sun Lines", [("chi-siamo.html", "Chi siamo"), ("domande-frequenti.html", "Domande frequenti"),
                       ("abbonamenti-studenti.html", "Abbonamenti studenti"), ("lavora-con-noi.html", "Lavora con noi"),
                       (BASE + "/customer-satisfaction.html?view=question&amp;id=1", "Questionario TPL")]),
        ("Assistenza", [("assistenza.html#assistenza", "Richiesta di assistenza"), ("assistenza.html#reclami", "Reclami e segnalazioni"),
                        ("assistenza.html#fattura", "Richiesta fattura"), ("condizioni-generali.html", "Condizioni di trasporto"),
                        ("privacy.html", "Privacy")]),
    ]
    cols = "".join(f'<nav class="ft-col" aria-label="{t}"><h2>{t}</h2><ul>' + "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in links) + '</ul></nav>'
                   for t, links in groups)
    contact = [
        (f"tel:{PHONE_INTL}", "phone", "Telefono", f'<span class="tnum">{PHONE}</span>'),
        (f"mailto:{EMAIL}", "mail", "Email", EMAIL),
        ("https://wa.me/" + WA_NUM, "chat", "WhatsApp preventivi", f'<span class="tnum">{WA_DISPLAY}</span>'),
        ("https://www.google.com/maps/search/?api=1&amp;query=Via+Pozzo+23+07026+Olbia", "pin", "Sede", "Via Pozzo 23, Olbia"),
    ]
    rows = "".join(f'<li><a href="{h}"><span class="ft-ic">{icon(ic, 18)}</span><span><small>{lab}</small>{val}</span></a></li>' for h, ic, lab, val in contact)
    return f"""<footer class="site-footer">
<div class="ft-stripes" aria-hidden="true"><i></i><i></i><i></i></div>
<img class="ft-sun" src="sun-lines-sun-mark.svg" alt="" aria-hidden="true" width="84" height="84">
<div class="wrap">
  <div class="ft-top">
    <div class="ft-brand">
      <img src="sun-lines-logo-white.svg" alt="Sun Lines Elite Service" width="173" height="46">
      <p class="ft-claim">La Sardegna inizia dal viaggio.</p>
      <p class="ft-sub">Da oltre 60 anni colleghiamo Olbia, la Gallura e il nord della Sardegna.</p>
    </div>
    <ul class="ft-contact">{rows}</ul>
  </div>
  <div class="ft-links">{cols}</div>
  <div class="ft-assoc">
    <p>Associati a</p>
    <ul>
      <li><img src="img/associazioni/anav.png" alt="ANAV – Associazione Nazionale Autotrasporto Viaggiatori" width="255" height="111" loading="lazy"></li>
      <li><img src="img/associazioni/cna.png" alt="CNA – Confederazione Nazionale dell’Artigianato" width="110" height="111" loading="lazy"></li>
      <li><img src="img/associazioni/confcommercio.png" alt="Confcommercio – Imprese per l’Italia" width="255" height="110" loading="lazy"></li>
    </ul>
  </div>
  <div class="ft-legal">
    <p>© Sun Lines Elite Service S.r.l. · P. IVA 00358880904</p>
    <div class="ft-social">
      <a href="{FB}" aria-label="Sun Lines su Facebook">{icon("fb", 18)}</a><a href="{IG}" aria-label="Sun Lines su Instagram">{icon("ig", 18)}</a>
      <a class="ft-up" href="#main">{icon("up", 16)} Torna su</a>
    </div>
  </div>
</div></footer>"""


def mbar(cta, wa_key=None):
    """Sales pages (wa_key set): Call, WhatsApp, quote. All other pages: timetables, FAQ, main action."""
    cta = cta or ("airbus-olbia-sassari-alghero.html#biglietti", "Biglietti Airbus")
    if wa_key:
        a = f'<a href="tel:{PHONE_INTL}">{icon("phone",20)}Chiama</a><a class="wa" href="{WA[wa_key]}">{icon("chat",20)}WhatsApp</a>'
    else:
        a = f'<a href="linee-e-orari.html">{icon("route",20)}Orari</a><a href="domande-frequenti.html">{icon("help",20)}Domande</a>'
    return f'<nav class="mbar" aria-label="Azioni rapide">{a}<a class="cta" href="{cta[0]}">{esc(cta[1])}</a></nav>'


def hreflang_links(path):
    # one line per available language; Italian at the root is also x-default
    out = []
    for code, _, ok in LANGS:
        if ok:
            p = path if code == "it" else f"/{code}" + path
            out.append(f'<link rel="alternate" hreflang="{code}" href="{BASE + p}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE + path}">')
    return "\n".join(out)


def page(*, slug, title, desc, canonical_path, active, body, ld, cta=None, wa=None, is_index=False, og_type="website"):
    canon = BASE + canonical_path
    meta = f'''<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{hreflang_links(canonical_path)}
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Sun Lines"><meta property="og:locale" content="it_IT">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/og/{slug}.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="sun-lines-sun-mark.svg" type="image/svg+xml">
{FONTS}
<style>{CSS}</style>
{ld}'''
    content = f'''{header(active)}
<main id="main">{body}</main>
{footer()}
{mbar(cta, wa)}
<script>{JS}</script>'''
    if is_index:
        return meta + "\n" + content
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
{meta}</head><body>
{content}
</body></html>'''
