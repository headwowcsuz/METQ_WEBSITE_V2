"""Barcha fayllarni yaratadi: SVG, chizma, mockup/PDF/PNG uchun HTML, poster, render ishlari ro'yxati."""
import os, json, html
import designs as D, textpath as tp
from meta import META

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TMP = os.environ.get("BUILD_TMP", "/tmp/metq_build"); os.makedirs(TMP, exist_ok=True)
FILES = {D.T_DIR: "BOSH_DIREKTOR", D.T_QAB: "QABULXONA"}
jobs = []
def esc(s): return html.escape(s, quote=True)
def wr(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(s)

def T(text, font, cap, x, y, fill, anchor="start", tracking=0.0):
    d, w, _ = tp.path(text, font, tp.size_for_cap(font, cap), x, y, anchor, tracking)
    return f'<path d="{d}" fill="{fill}"/>', w

# ---------------------------------------------------------------- texnik chizma
def arrow(x, y, ang):
    import math
    a = math.radians(ang); L, Wd = 2.2, 0.7
    p1 = (x - L*math.cos(a) + Wd*math.sin(a), y - L*math.sin(a) - Wd*math.cos(a))
    p2 = (x - L*math.cos(a) - Wd*math.sin(a), y - L*math.sin(a) + Wd*math.cos(a))
    return f'<path d="M{x:.2f},{y:.2f}L{p1[0]:.2f},{p1[1]:.2f}L{p2[0]:.2f},{p2[1]:.2f}Z" fill="#1565c0"/>'

def hdim(x1, x2, y, label, ext_from):
    t, w = T(label, "inter-500", 2.6, (x1+x2)/2, y-1.6, "#1565c0", "middle")
    return (f'<line x1="{x1}" y1="{ext_from}" x2="{x1}" y2="{y+1.5}" stroke="#1565c0" stroke-width="0.15"/>'
            f'<line x1="{x2}" y1="{ext_from}" x2="{x2}" y2="{y+1.5}" stroke="#1565c0" stroke-width="0.15"/>'
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#1565c0" stroke-width="0.2"/>'
            + arrow(x1, y, 180) + arrow(x2, y, 0) + t)

def vdim(y1, y2, x, label, ext_from):
    t, w = T(label, "inter-500", 2.6, 0, 0, "#1565c0", "middle")
    cy = (y1+y2)/2
    return (f'<line x1="{ext_from}" y1="{y1}" x2="{x-1.5}" y2="{y1}" stroke="#1565c0" stroke-width="0.15"/>'
            f'<line x1="{ext_from}" y1="{y2}" x2="{x-1.5}" y2="{y2}" stroke="#1565c0" stroke-width="0.15"/>'
            f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#1565c0" stroke-width="0.2"/>'
            + arrow(x, y1, 270) + arrow(x, y2, 90) +
            f'<g transform="translate({x-1.6} {cy}) rotate(-90)">{t}</g>')

def drawing_svg(m, title=D.T_DIR, p="dr"):
    n = m["n"]
    inner, shape, holes = D.sign_svg(n, title, p, False)
    g = [f'<rect x="-34" y="-30" width="268" height="172" fill="#ffffff"/>',
         f'<g opacity="0.28">{inner}</g>',
         f'<path d="{shape}" fill="none" stroke="#e53935" stroke-width="0.25"/>']
    for (x, y, r) in holes:
        g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#1565c0" stroke-width="0.25"/>'
                 f'<line x1="{x-r-1.5}" y1="{y}" x2="{x+r+1.5}" y2="{y}" stroke="#1565c0" stroke-width="0.12"/>'
                 f'<line x1="{x}" y1="{y-r-1.5}" x2="{x}" y2="{y+r+1.5}" stroke="#1565c0" stroke-width="0.12"/>')
    g.append(hdim(0, 200, -12, "200 mm", -1))
    g.append(vdim(0, 100, -12, "100 mm", -1))
    if holes:
        x, y, r = holes[0]
        g.append(hdim(0, x, 108, f"{x:g}", 101) if x < 100 else "")
        g.append(vdim(0, y, 212, f"{y:g}", 201))
        lab, _ = T(f"Teshik Ø{2*r:g} mm × {len(holes)}", "inter-500", 2.6, x + r + 3, y + 7, "#1565c0")
        g.append(lab)
    if n == 9:   # LED texnik elementlari
        g.append('<path d="M8,8H186L192,14V92H14L8,86Z" fill="none" stroke="#00a152" stroke-width="0.6" stroke-dasharray="2 1.2"/>')
        g.append('<rect x="92" y="94" width="16" height="4" fill="none" stroke="#00a152" stroke-width="0.3"/>'
                 '<path d="M100,98 V113 H128" fill="none" stroke="#00a152" stroke-width="0.4"/>')
        l1, _ = T("LED tasma 12 V (ramka ichida, perimetr)", "inter-500", 2.4, 132, 111, "#00a152")
        l2, _ = T("Kabel chiqishi / drayver", "inter-500", 2.4, 132, 115.5, "#00a152")
        g += [l1, l2]
    leg = [("#e53935", "Kesish konturi (CUT)"), ("#1565c0", "Teshiklar va o‘lchamlar")]
    if n == 9: leg.append(("#00a152", "LED va kabel (ichki)"))
    x = 0
    for c, s in leg:
        t, w = T(s, "inter-500", 2.4, x + 7, 128.5, "#333")
        g.append(f'<line x1="{x}" y1="127.6" x2="{x+5}" y2="127.6" stroke="{c}" stroke-width="0.6"/>' + t)
        x += w + 16
    head, _ = T(f"{n:02d} — {m['name'].upper()}  ·  TEXNIK CHIZMA  ·  M 1:1  ·  O‘LCHAMLAR MM DA", "inter-600", 2.6, -30, -22, "#111")
    g.append(head)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="268mm" height="172mm" viewBox="-34 -30 268 172">'
            f'<title>{n:02d} {m["name"]} — texnik chizma</title>' + "".join(g) + "</svg>")

# ---------------------------------------------------------------- mockup (eshik)
DOORS = {
  "walnut": dict(base=("#6b4429", "#4d2f1c", "#5f3c25"), grain=("0.09 0.0025", 0.55, "0.06 0.035 0.015"), casing="#4a2d1b", wall=("#ecebe7", "#d9d7d1")),
  "oak":    dict(base=("#d2b183", "#b8935f", "#caa673"), grain=("0.08 0.003", 0.35, "0.35 0.24 0.12"), casing="#b8935f", wall=("#e9e7e2", "#d3d0c9")),
  "white":  dict(base=("#f7f6f3", "#e8e6e1", "#f1efeb"), grain=None, casing="#f2f1ee", wall=("#d9dcd8", "#c3c7c2")),
  "grey":   dict(base=("#5b6064", "#43474a", "#52575b"), grain=None, casing="#3f4346", wall=("#e8e8e6", "#d1d1ce")),
}
def mockup_html(m, title):
    n = m["n"]; dr = DOORS[m["door"]]
    inner, shape, holes = D.sign_svg(n, title, "mk", False)
    dep = m["depth"]
    b0, b1, b2 = dr["base"]
    grain = ""
    if dr["grain"]:
        fr, al, col = dr["grain"]; r, g_, b = col.split()
        grain = (f'<filter id="dg" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                 f'<feTurbulence type="fractalNoise" baseFrequency="{fr}" numOctaves="4" seed="12"/>'
                 f'<feColorMatrix type="matrix" values="0 0 0 0 {r}  0 0 0 0 {g_}  0 0 0 0 {b}  0 0 1.8 0 -{0.75-al*0.3}"/></filter>')
    white_panels = ""
    if m["door"] in ("white",):
        white_panels = ('<rect x="300" y="-200" width="700" height="1040" rx="2" fill="none" stroke="#d6d3cd" stroke-width="5"/>'
                        '<rect x="306" y="-194" width="688" height="1028" rx="2" fill="none" stroke="#ffffff" stroke-width="2"/>')
    if m["door"] == "grey":
        white_panels = '<rect x="236" y="-100" width="6" height="1100" fill="#35393c"/><rect x="242" y="-100" width="2" height="1100" fill="#6c7175"/>'
    sh = f'<filter id="ss" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur stdDeviation="{0.45*dep+1.2}"/></filter>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="150 190 1000 730" width="1300" height="950">
<defs>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{dr['wall'][0]}"/><stop offset="1" stop-color="{dr['wall'][1]}"/></linearGradient>
<linearGradient id="door" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{b1}"/><stop offset="0.12" stop-color="{b0}"/><stop offset="0.6" stop-color="{b2}"/><stop offset="1" stop-color="{b1}"/></linearGradient>
<radialGradient id="light" cx="0.45" cy="0.05" r="0.9"><stop offset="0" stop-color="#fff" stop-opacity="0.28"/><stop offset="0.55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.32"/></radialGradient>
<linearGradient id="cas" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0.18"/><stop offset="0.3" stop-color="#fff" stop-opacity="0.12"/><stop offset="1" stop-color="#000" stop-opacity="0.22"/></linearGradient>
<linearGradient id="hnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f5f6"/><stop offset="0.45" stop-color="#a9afb4"/><stop offset="1" stop-color="#5d6368"/></linearGradient>
<filter id="wn" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="2"/><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0 0.05"/></filter>
<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>
{grain}{sh}
</defs>
<rect width="1300" height="950" fill="url(#wall)"/>
<rect width="1300" height="950" filter="url(#wn)"/>
<rect x="128" y="-20" width="1044" height="1000" fill="#000" opacity="0.25" filter="url(#blur8)"/>
<rect x="140" y="-20" width="1020" height="1000" fill="{dr['casing']}"/>
<rect x="140" y="-20" width="1020" height="1000" fill="url(#cas)" opacity="0.8"/>
<rect x="210" y="-20" width="880" height="1000" fill="#000" opacity="0.55"/>
<rect x="218" y="-20" width="864" height="1000" fill="url(#door)"/>
{'<rect x="218" y="-20" width="864" height="1000" fill="#000" filter="url(#dg)"/>' if grain else ''}
{white_panels}
<rect x="218" y="-20" width="14" height="1000" fill="#000" opacity="0.12"/>
<g transform="translate(0 0)">
<path d="{shape}" transform="translate({550+0.25*dep} {300+0.45*dep})" fill="#000" opacity="{0.42 if dep>10 else 0.34}" filter="url(#ss)"/>
<svg x="550" y="300" width="200" height="100" viewBox="0 0 200 100" overflow="visible">{inner}</svg>
</g>
<g>
<ellipse cx="985" cy="912" rx="30" ry="30" fill="#000" opacity="0.25" filter="url(#blur8)"/>
<circle cx="980" cy="905" r="27" fill="url(#hnd)"/>
<rect x="840" y="893" width="150" height="24" rx="12" fill="url(#hnd)"/>
<rect x="845" y="896" width="140" height="5" rx="2.5" fill="#fff" opacity="0.6"/>
</g>
<rect width="1300" height="950" fill="url(#light)"/>
</svg>'''
    return f'<html><head><style>html,body{{margin:0;background:#fff}}svg{{display:block}}</style></head><body>{svg}</body></html>'

# ---------------------------------------------------------------- PDF/PNG HTML
def sign_page(svg):
    return ('<html><head><style>@page{size:200mm 100mm;margin:0}html,body{margin:0;padding:0;background:transparent}'
            'body{width:200mm;height:100mm;overflow:hidden}svg{display:block;width:200mm;height:100mm}</style></head>'
            f'<body>{svg}</body></html>')

def png_page(svg):
    return ('<html><head><style>html,body{margin:0;padding:0;background:transparent}svg{display:block;width:1920px;height:960px}</style></head>'
            f'<body>{svg}</body></html>')

def spec_html(m):
    n = m["n"]
    s1, _, _ = D.sign_svg(n, D.T_DIR, "a", False)
    s2, _, _ = D.sign_svg(n, D.T_QAB, "b", False)
    drw = drawing_svg(m, p="c").replace('width="268mm" height="172mm"', 'width="100%"')
    pal = "".join(f'<div class="sw"><i style="background:{c}"></i><b>{c}</b><span>{esc(nm)}</span></div>' for c, nm in m["palette"])
    notes = "".join(f"<li>{esc(x)}</li>" for x in m["notes"])
    rows = [("O‘lcham", "200 × 100 mm (aniq kesish o‘lchami, bleed yo‘q)"), ("Material", m["material"]),
            ("Ishlab chiqarish", m["production"]), ("O‘rnatish", m["mount"]),
            ("Logotip", "Rasmiy METQ logotipi asl nisbat va ranglarda, oq fonsiz (o‘zgartirilmagan)." + " Fayldagi logotip rastr (402×249 px, tablichkada ≈ 400 dpi). Lazer gravyura yoki plyonka kesish uchun logotipning vektor asl nusxasini (AI/CDR/SVG/PDF) korxonadan so‘rang."),
            ("F.I.O", "Lavozim ostidagi qator: " + (D.FIO.get(D.T_DIR) or "—") + ". Haqiqiy F.I.O _MANBA/fio.json fayliga yoziladi va fayllar qayta yaratiladi. Xodim almashganda faqat shu qator o‘zgaradi."),
            ("Shrift", m["font"] + " — fayllarda matn vektor konturga aylantirilgan (shrift o‘rnatish shart emas)."),
            ("O‘rnatish balandligi", "Tablichka markazi poldan 1550–1650 mm, eshik tutqichi tomonidan yoki eshik markazida."),
            ("Fayllar", "BOSH_DIREKTOR / QABULXONA: .svg (vektor matn + logotip), .pdf (200×100 mm, vektor), .png (3840×1920), MOCKUP_*.jpg, TEXNIK_CHIZMA.svg")]
    tr = "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in rows)
    return f'''<html><head><meta charset="utf-8"><style>
@page{{size:A4;margin:12mm}} body{{font-family:Inter,'DejaVu Sans',sans-serif;color:#1b1f1d;font-size:9.5pt;margin:0}}
h1{{font-size:17pt;margin:0 0 1mm;font-weight:700;letter-spacing:-.01em}} .sub{{color:#5c6762;font-size:9pt;margin-bottom:5mm}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;background:{m['bg']};padding:6mm;border-radius:3mm}}
.pair svg{{width:100%;height:auto;display:block;filter:drop-shadow(0 .6mm 1mm rgba(0,0,0,.25))}}
h2{{font-size:10.5pt;margin:6mm 0 2mm;text-transform:uppercase;letter-spacing:.06em;color:#2e6b45}}
table{{border-collapse:collapse;width:100%}} th,td{{text-align:left;vertical-align:top;padding:1.6mm 2mm;border-bottom:.2mm solid #dde3df}}
th{{width:34mm;color:#5c6762;font-weight:600}}
.pal{{display:flex;gap:3mm;flex-wrap:wrap}} .sw{{display:flex;align-items:center;gap:1.6mm;font-size:8.5pt}} .sw i{{width:6mm;height:6mm;border-radius:1mm;border:.2mm solid #ccc;display:inline-block}}
.sw span{{color:#5c6762}} .drw svg{{display:block}} ul{{margin:0;padding-left:5mm}} .foot{{margin-top:4mm;color:#7a847f;font-size:7.5pt}}
</style></head><body>
<h1>{n:02d} — {esc(m['name'])}</h1>
<div class="sub">{esc(m['uz'])} · {esc(m['style'])} · {esc(D.CO)} · Kabinet tablichkasi 200 × 100 mm</div>
<div class="pair"><svg viewBox="0 0 200 100">{s1}</svg><svg viewBox="0 0 200 100">{s2}</svg></div>
<h2>Material va ishlab chiqarish</h2><table>{tr}</table>
<h2>Ranglar palitrasi</h2><div class="pal">{pal}</div>
<div class="foot">Rang kodlari ekran uchun (HEX). Bosmadan oldin ishlab chiqaruvchidan rang namunasini (proof) so‘rang.</div>
{f"<h2>Muhim eslatmalar</h2><ul>{notes}</ul>" if notes else ""}
<h2 style="break-before:page">Texnik chizma (BOSH DIREKTOR misolida, QABULXONA kontur va teshiklari bir xil)</h2>
<div class="drw">{drw}</div>
</body></html>'''

# ---------------------------------------------------------------- poster
def poster():
    PW, PH = 841, 594
    g = [f'<rect width="{PW}" height="{PH}" fill="#f3f5f4"/>', f'<rect width="{PW}" height="8" fill="#2c9a54"/>']
    t, _ = T("PREMIUM KABINET TABLICHKALARI — 15 VARIANT", "inter-700", 11, 30, 42, "#14201a"); g.append(t)
    t, _ = T(f"{D.CO}  ·  BOSH OFIS  ·  200 × 100 MM  ·  BOSH DIREKTOR / QABULXONA", "inter-500", 3.6, 30, 56, "#5c6762", tracking=0.08); g.append(t)
    cw, gx0, gy0 = 146.2, 30, 76
    sw = 130; sc = sw / 200; shh = 100 * sc
    for i, m in enumerate(META):
        c, r = i % 5, i // 5
        x = gx0 + c * (cw + 12); y = gy0 + r * 168
        g.append(f'<rect x="{x}" y="{y}" width="{cw}" height="160" rx="4" fill="{m["bg"]}"/>')
        sx = x + (cw - sw) / 2
        for k, tt in enumerate(D.TITLES):
            inner, shape, _ = D.sign_svg(m["n"], tt, f"p{m['n']}{k}", False)
            sy = y + 8 + k * (shh + 5)
            g.append(f'<g transform="translate({sx:.2f} {sy:.2f}) scale({sc})">'
                     f'<path d="{shape}" transform="translate(0.8 1.4)" fill="#000" opacity="0.22"/>{inner}</g>')
        lab, _ = T(f"{m['n']:02d}", "inter-700", 4.2, x + 8, y + 151, "#2c9a54"); g.append(lab)
        lab, _ = T(m["name"].upper(), "inter-600", 3.1, x + 20, y + 151, "#1b1f1d", tracking=0.04); g.append(lab)
    t, _ = T("Har bir variantning SVG, PDF, PNG, mockup va texnik tavsif fayllari tegishli papkada.", "inter-400", 3, 30, 584, "#7a847f"); g.append(t)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">'
            f'<title>15 variant — taqqoslash posteri</title>' + "".join(g) + "</svg>")

# ---------------------------------------------------------------- asosiy
def main():
    for m in META:
        fd = os.path.join(ROOT, m["folder"])
        for title, fn in FILES.items():
            svg = D.sign_svg(m["n"], title)
            wr(os.path.join(fd, fn + ".svg"), svg)
            h = os.path.join(TMP, f"{m['n']:02d}_{fn}_pdf.html"); wr(h, sign_page(svg))
            jobs.append(dict(kind="pdf", html=h, out=os.path.join(fd, fn + ".pdf"), width="200mm", height="100mm"))
            h = os.path.join(TMP, f"{m['n']:02d}_{fn}_png.html"); wr(h, png_page(svg))
            jobs.append(dict(kind="png", html=h, out=os.path.join(fd, fn + ".png"), vw=1920, vh=960, dsf=2, transparent=True))
            h = os.path.join(TMP, f"{m['n']:02d}_{fn}_mock.html"); wr(h, mockup_html(m, title))
            jobs.append(dict(kind="jpg", html=h, out=os.path.join(fd, f"MOCKUP_{fn}.jpg"), vw=1300, vh=950, dsf=2))
        wr(os.path.join(fd, "TEXNIK_CHIZMA.svg"), drawing_svg(m))
        h = os.path.join(TMP, f"{m['n']:02d}_spec.html"); wr(h, spec_html(m))
        jobs.append(dict(kind="pdf", html=h, out=os.path.join(fd, "TEXNIK_TAVSIF.pdf"), format="A4"))
        wr(os.path.join(fd, "TAVSIF.txt"), "\n".join([
            f"{m['n']:02d} — {m['name']} ({m['uz']})", f"Uslub: {m['style']}", "O‘lcham: 200 × 100 mm",
            f"Material: {m['material']}", f"Ishlab chiqarish: {m['production']}", f"O‘rnatish: {m['mount']}",
            f"Shrift: {m['font']} (fayllarda matn konturga aylantirilgan)",
            "Ranglar: " + ", ".join(f"{c} {nm}" for c, nm in m["palette"])] + [f"Eslatma: {x}" for x in m["notes"]]) + "\n")
    ps = poster(); wr(os.path.join(ROOT, "POSTER_15_VARIANT.svg"), ps)
    h = os.path.join(TMP, "poster_pdf.html")
    wr(h, '<html><head><style>@page{size:841mm 594mm;margin:0}html,body{margin:0}body{width:841mm;height:594mm;overflow:hidden}svg{display:block;width:841mm;height:594mm}</style></head><body>' + ps + '</body></html>')
    jobs.append(dict(kind="pdf", html=h, out=os.path.join(ROOT, "POSTER_15_VARIANT.pdf"), width="841mm", height="594mm"))
    h = os.path.join(TMP, "poster_png.html")
    wr(h, '<html><head><style>html,body{margin:0}svg{display:block;width:2523px;height:1782px}</style></head><body>' + ps + '</body></html>')
    jobs.append(dict(kind="png", html=h, out=os.path.join(ROOT, "POSTER_15_VARIANT.png"), vw=2523, vh=1782, dsf=2))
    json.dump(jobs, open(os.path.join(TMP, "jobs.json"), "w"), indent=0)
    print(len(jobs), "ta render ishi")

if __name__ == "__main__": main()
