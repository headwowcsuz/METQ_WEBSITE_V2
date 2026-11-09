"""index.html katalogi + WebP preview rasmlar."""
import os, json, sys
from PIL import Image
from meta import META
import designs as D
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FN = ["BOSH_DIREKTOR", "QABULXONA"]

def previews():
    for m in META:
        fd = os.path.join(ROOT, m["folder"]); pv = os.path.join(fd, "preview"); os.makedirs(pv, exist_ok=True)
        for fn in FN:
            Image.open(os.path.join(fd, fn + ".png")).resize((1200, 600), Image.LANCZOS).save(os.path.join(pv, fn + ".webp"), quality=88, method=5)
            Image.open(os.path.join(fd, f"MOCKUP_{fn}.jpg")).resize((1300, 950), Image.LANCZOS).convert("RGB").save(os.path.join(pv, f"MOCKUP_{fn}.webp"), quality=82, method=5)
    Image.open(os.path.join(ROOT, "POSTER_15_VARIANT.png")).resize((2000, 1413), Image.LANCZOS).convert("RGB").save(os.path.join(ROOT, "POSTER_preview.webp"), quality=85)

def data():
    out = []
    for m in META:
        out.append(dict(n=m["n"], f=m["folder"], name=m["name"], uz=m["uz"], style=m["style"], font=m["font"], bg=m["bg"],
                        pal=m["palette"], material=m["material"], mount=m["mount"], production=m["production"], notes=m["notes"]))
    return out

CSS = r"""
/* Layout: katalog = material namunalari stendi. Yuqorida boshqaruv paneli, pastda 3/2/1 ustunli setka. */
:root{
  --bg:#eef1ef; --panel:#ffffff; --ink:#18201c; --muted:#5d6a63; --line:#d6ddd8; --accent:#1f7f47; --accent-ink:#ffffff; --chip:#e3e9e5;
  --f-display:"Unbounded","Arial Black",system-ui,sans-serif; --f-body:"Onest","Segoe UI",system-ui,sans-serif; --f-mono:"JetBrains Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#111614;--panel:#1a211e;--ink:#e8eeea;--muted:#9aa8a0;--line:#2c3631;--accent:#4cc07a;--accent-ink:#0b1a11;--chip:#24302a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#111614;--panel:#1a211e;--ink:#e8eeea;--muted:#9aa8a0;--line:#2c3631;--accent:#4cc07a;--accent-ink:#0b1a11;--chip:#24302a;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:15px;line-height:1.5;margin:0}
.wrap{max-width:1320px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header.top{padding-block:40px 20px;display:grid;gap:14px}
.eyebrow{font-family:var(--f-mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h1{font-family:var(--f-display);font-weight:600;font-size:clamp(26px,4.2vw,46px);line-height:1.08;margin:0;letter-spacing:-.01em;text-wrap:balance}
.lead{color:var(--muted);max-width:68ch;margin:0}
.specs{display:flex;flex-wrap:wrap;gap:8px 18px;font-family:var(--f-mono);font-size:12.5px;color:var(--muted)}
.specs b{color:var(--ink);font-weight:500}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.bar .wrap{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;padding-block:10px}
.seg{display:inline-flex;background:var(--chip);border-radius:999px;padding:3px}
.seg button{font:inherit;font-size:13px;font-weight:600;border:0;background:transparent;color:var(--muted);padding:7px 14px;border-radius:999px;cursor:pointer;letter-spacing:.02em}
.seg button[aria-pressed="true"]{background:var(--panel);color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.12)}
.bar .sp{flex:1}
a.btn,button.btn{font:inherit;font-size:13px;font-weight:600;text-decoration:none;color:var(--ink);border:1px solid var(--line);background:var(--panel);padding:7px 12px;border-radius:8px;cursor:pointer;display:inline-flex;gap:6px;align-items:center}
a.btn:hover,button.btn:hover{border-color:var(--accent);color:var(--accent)}
a.btn.pri{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;padding-block:26px 40px}
@media (max-width:1040px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:660px){.grid{grid-template-columns:minmax(0,1fr)}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-width:0}
.stage{position:relative;aspect-ratio:13/8;max-width:100%;display:grid;place-items:center;cursor:zoom-in;border:0;padding:0;width:100%}
.stage img{width:82%;height:auto;filter:drop-shadow(0 6px 10px rgba(0,0,0,.22))}
.stage.mock img{width:100%;height:100%;object-fit:cover;filter:none}
.stage .no{position:absolute;left:12px;top:10px;font-family:var(--f-display);font-weight:600;font-size:13px;color:rgba(0,0,0,.55);background:rgba(255,255,255,.65);padding:2px 8px;border-radius:6px}
.body{padding:16px 16px 18px;display:grid;gap:12px;min-width:0}
.ttl{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.ttl h2{font-family:var(--f-display);font-weight:500;font-size:17px;margin:0;line-height:1.2}
.ttl small{display:block;color:var(--muted);font-size:13px;margin-top:2px}
.tag{font-family:var(--f-mono);font-size:11px;white-space:nowrap;color:var(--muted);border:1px solid var(--line);padding:2px 7px;border-radius:5px}
.pal{display:flex;gap:6px;flex-wrap:wrap}
.pal span{display:inline-flex;align-items:center;gap:5px;font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.pal i{width:16px;height:16px;border-radius:4px;border:1px solid rgba(0,0,0,.15);display:inline-block}
.mat{font-size:13.5px;color:var(--muted);margin:0}
.mat b{color:var(--ink);font-weight:600}
.dl{display:flex;flex-wrap:wrap;gap:6px}
.mini{display:flex;gap:6px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.mini .seg button{padding:5px 10px;font-size:12px}
section.poster{padding-block:10px 60px;display:grid;gap:14px}
section.poster h2{font-family:var(--f-display);font-weight:500;font-size:22px;margin:0}
section.poster img{border-radius:12px;border:1px solid var(--line);cursor:zoom-in;display:block;width:100%}
.note{font-size:13px;color:var(--muted)}
footer{border-top:1px solid var(--line);padding-block:20px 36px;color:var(--muted);font-size:13px}
dialog{border:0;padding:0;background:transparent;max-width:none;max-height:none;width:100%;height:100%}
dialog::backdrop{background:#0b100e}
.lb{background:#0b100e}
.lb{height:100%;display:grid;grid-template-rows:auto 1fr auto;gap:10px;padding:max(14px,env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) max(14px,env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));color:#e8eeea}
.lb .hd{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.lb .hd h3{font-family:var(--f-display);font-weight:500;font-size:17px;margin:0;flex:1;min-width:0}
.lb .view{min-height:0;display:grid;place-items:center;border-radius:12px;overflow:hidden}
.lb .view img{max-width:100%;max-height:100%;object-fit:contain}
.lb .view.sign img{width:min(100%,1400px);filter:drop-shadow(0 10px 18px rgba(0,0,0,.35))}
.lb .seg{background:#25302b}.lb .seg button{color:#aab6af}.lb .seg button[aria-pressed="true"]{background:#e8eeea;color:#111614}
.lb .btn{background:#1a211e;color:#e8eeea;border-color:#38443e}
.lb .ft{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:13px;color:#aab6af}
@media (prefers-reduced-motion:no-preference){.card{transition:transform .2s ease,box-shadow .2s ease}.card:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.08)}}
"""

JS = r"""
const D = window.__DATA, LOCAL = window.__LOCAL;
const T = [{k:"BOSH_DIREKTOR",l:"BOSH DIREKTOR"},{k:"QABULXONA",l:"QABULXONA"}];
let gTitle = 0, gView = "sign";
const st = D.map(()=>0);
const grid = document.getElementById("grid");
function src(d, t, v){ return `${d.f}/preview/${v==="mock"?"MOCKUP_":""}${T[t].k}.webp`; }
function card(d,i){
  const el = document.createElement("article"); el.className="card";
  const pal = d.pal.map(([c,n])=>`<span title="${n}"><i style="background:${c}"></i>${c}</span>`).join("");
  const dl = LOCAL ? `<div class="dl">
     <a class="btn pri" data-k="png" download>PNG</a><a class="btn" data-k="svg" download>SVG</a><a class="btn" data-k="pdf" download>PDF</a>
     <a class="btn" data-k="mock" download>Mockup</a><a class="btn" href="${d.f}/TEXNIK_TAVSIF.pdf" download>Texnik PDF</a><a class="btn" href="${d.f}/TEXNIK_CHIZMA.svg" download>Chizma</a></div>` : "";
  el.innerHTML = `<button class="stage" style="background:${d.bg}" aria-label="${d.name} — katta ko‘rish"><span class="no">${String(d.n).padStart(2,"0")}</span><img alt="" loading="lazy" width="1200" height="600"></button>
   <div class="body">
     <div class="ttl"><div><h2>${String(d.n).padStart(2,"0")} — ${d.name}</h2><small>${d.uz}</small></div><span class="tag">${d.style}</span></div>
     <div class="pal">${pal}</div>
     <p class="mat"><b>Material:</b> ${d.material}</p>
     <p class="mat"><b>O‘rnatish:</b> ${d.mount}</p>
     <div class="mini"><div class="seg" role="group" aria-label="Yozuv"><button data-t="0">Bosh direktor</button><button data-t="1">Qabulxona</button></div></div>
     ${dl}
   </div>`;
  el.querySelector(".stage").onclick = ()=>openLb(i, gView);
  el.querySelectorAll("[data-t]").forEach(b=>b.onclick=()=>{st[i]=+b.dataset.t; paint(i);});
  grid.appendChild(el); return el;
}
const cards = D.map(card);
function paint(i){
  const d=D[i], el=cards[i], t=st[i];
  const stg=el.querySelector(".stage"); stg.classList.toggle("mock", gView==="mock");
  stg.style.background = gView==="mock" ? "#222" : d.bg;
  const img=el.querySelector(".stage img"); img.src = src(d,t,gView); img.alt = `${d.name}: ${T[t].l}`;
  if(gView==="mock"){img.width=1300;img.height=950}else{img.width=1200;img.height=600}
  el.querySelectorAll("[data-t]").forEach(b=>b.setAttribute("aria-pressed", String(+b.dataset.t===t)));
  if(LOCAL){ const k=T[t].k;
    el.querySelector('[data-k="png"]').href=`${d.f}/${k}.png`;
    el.querySelector('[data-k="svg"]').href=`${d.f}/${k}.svg`;
    el.querySelector('[data-k="pdf"]').href=`${d.f}/${k}.pdf`;
    el.querySelector('[data-k="mock"]').href=`${d.f}/MOCKUP_${k}.jpg`; }
}
function paintAll(){ D.forEach((_,i)=>paint(i));
  document.querySelectorAll("[data-gt]").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.gt===gTitle)));
  document.querySelectorAll("[data-gv]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.gv===gView))); }
document.querySelectorAll("[data-gt]").forEach(b=>b.onclick=()=>{gTitle=+b.dataset.gt; st.fill(gTitle); paintAll();});
document.querySelectorAll("[data-gv]").forEach(b=>b.onclick=()=>{gView=b.dataset.gv; paintAll();});
paintAll();
// lightbox
const dlg=document.getElementById("lb"); let li=0, lv="sign";
function lbPaint(){
  const d=D[li], t=st[li], k=T[t].k;
  dlg.querySelector("h3").textContent=`${String(d.n).padStart(2,"0")} — ${d.name} · ${T[t].l}`;
  const view=dlg.querySelector(".view"), img=view.querySelector("img");
  view.className="view"+(lv==="sign"?" sign":""); view.style.background = lv==="sign"? d.bg : (lv==="draw"?"#fff":"transparent");
  img.src = lv==="sign" ? `${d.f}/${k}.svg` : lv==="mock" ? (LOCAL?`${d.f}/MOCKUP_${k}.jpg`:`${d.f}/preview/MOCKUP_${k}.webp`) : `${d.f}/TEXNIK_CHIZMA.svg`;
  img.alt = `${d.name}: ${T[t].l}`;
  dlg.querySelectorAll("[data-lv]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.lv===lv)));
  dlg.querySelectorAll("[data-lt]").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.lt===t)));
  dlg.querySelector(".info").textContent = `${d.font} · 200 × 100 mm · ${d.production}`;
}
function openLb(i,v){ li=i; lv=v==="mock"?"mock":"sign"; lbPaint(); dlg.showModal(); }
dlg.querySelectorAll("[data-lv]").forEach(b=>b.onclick=()=>{lv=b.dataset.lv; lbPaint();});
dlg.querySelectorAll("[data-lt]").forEach(b=>b.onclick=()=>{st[li]=+b.dataset.lt; paint(li); lbPaint();});
dlg.querySelector("[data-prev]").onclick=()=>{li=(li+D.length-1)%D.length; lbPaint();};
dlg.querySelector("[data-next]").onclick=()=>{li=(li+1)%D.length; lbPaint();};
dlg.querySelector("[data-close]").onclick=()=>dlg.close();
dlg.addEventListener("click",e=>{ if(e.target.classList.contains("view")) dlg.close(); });
document.addEventListener("keydown",e=>{ if(!dlg.open) return;
  if(e.key==="ArrowRight") dlg.querySelector("[data-next]").click();
  if(e.key==="ArrowLeft") dlg.querySelector("[data-prev]").click(); });

"""

def page(local):
    data = json.dumps(data_list, ensure_ascii=False)
    dl_poster = ('<div class="dl"><a class="btn pri" href="POSTER_15_VARIANT.pdf" download>Poster PDF (A1)</a>'
                 '<a class="btn" href="POSTER_15_VARIANT.png" download>Poster PNG</a><a class="btn" href="POSTER_15_VARIANT.svg" download>Poster SVG</a></div>') if local else \
                '<p class="note">Bu veb-ko‘rinishda faqat preview rasmlar bor. PNG (3840×1920), SVG, PDF, mockup va texnik fayllar <b>METQ_TABLICHKALAR_15_VARIANT</b> papkasidagi index.html orqali yuklab olinadi.</p>'
    body = f"""<header class="top wrap">
 <div class="eyebrow">{D.CO} · Bosh ofis</div>
 <h1>Kabinet tablichkalari: 15 variant</h1>
 <p class="lead">Har bir variantda BOSH DIREKTOR va QABULXONA juftligi. Kartani bosing: tablichka katta formatda, eshikdagi mockup va texnik chizma ochiladi.</p>
 <div class="specs"><span>O‘lcham <b>200 × 100 mm</b></span><span>Matn <b>vektor kontur</b></span><span>PNG <b>3840 × 1920</b></span><span>PDF <b>1:1, vektor</b></span><span>Til <b>o‘zbek (lotin)</b></span></div>
</header>
<div class="bar"><div class="wrap">
 <div class="seg" role="group" aria-label="Barcha kartalardagi yozuv"><button data-gt="0">BOSH DIREKTOR</button><button data-gt="1">QABULXONA</button></div>
 <div class="seg" role="group" aria-label="Ko‘rinish"><button data-gv="sign">Tablichka</button><button data-gv="mock">Eshikda</button></div>
 <span class="sp"></span>
 <a class="btn" href="#poster">Taqqoslash posteri</a>
</div></div>
<main class="wrap"><div class="grid" id="grid"></div>
<section class="poster" id="poster"><h2>Barcha variantlar bitta posterda</h2>
 <img id="pimg" src="POSTER_preview.webp" alt="15 variant taqqoslash posteri" width="2000" height="1413" loading="lazy">
 {dl_poster}
</section></main>
<footer class="wrap">Barcha variantlarda rasmiy METQ logotipi asl nisbat va ranglarda joylangan. Logotip oq fonsiz, to‘g‘ridan-to‘g‘ri tablichka ustida. F.I.O qatoridagi «Familiya Ism Otasining ismi» namuna matni: haqiqiy ism-sharif berilgach almashtiriladi. Fayldagi logotip rastr nusxadan olingan: ishlab chiqarishdan oldin logotipning vektor asl nusxasini korxonadan so‘rang. Rang kodlari ekran uchun (HEX): bosmadan oldin ishlab chiqaruvchidan rang namunasini so‘rang.</footer>
<dialog id="lb" aria-label="Katta ko‘rish"><div class="lb">
 <div class="hd"><h3></h3>
  <div class="seg" role="group" aria-label="Yozuv"><button data-lt="0">Bosh direktor</button><button data-lt="1">Qabulxona</button></div>
  <div class="seg" role="group" aria-label="Ko‘rinish"><button data-lv="sign">Tablichka</button><button data-lv="mock">Eshikda</button><button data-lv="draw">Chizma</button></div>
  <button class="btn" data-prev aria-label="Oldingi">←</button><button class="btn" data-next aria-label="Keyingi">→</button><button class="btn" data-close>Yopish ✕</button></div>
 <div class="view"><img alt=""></div>
 <div class="ft"><span class="info"></span><span>← → tugmalari bilan almashtiring</span></div>
</div></dialog>
<script>window.__DATA={data};window.__LOCAL={str(local).lower()};</script>
<script>{JS}</script>"""
    head = ('<title>METQ kabinet tablichkalari</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&family=Unbounded:wght@500;600&family=JetBrains+Mono:wght@400;500&display=swap">\n'
            f'<style>{CSS}</style>\n')
    if local:
        return ('<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                + head + '<style>img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + body + '</body></html>')
    return head + body

data_list = data()
if __name__ == "__main__":
    if "--no-previews" not in sys.argv: previews()
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page(True))
    open(os.path.join(ROOT, "_MANBA", "katalog_web.html"), "w", encoding="utf-8").write(page(False))
    print("ok")
