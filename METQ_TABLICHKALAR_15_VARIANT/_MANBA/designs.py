"""15 ta premium kabinet tablichkasi dizayni. Barcha koordinatalar millimetrda: 200 x 100 mm."""
import math
import textpath as tp

T_DIR = "BOSH DIREKTOR"
T_QAB = "QABULXONA"
TITLES = [T_DIR, T_QAB]
CO = "«MAXSUSELEKTRTARMOQQURILISH» AJ"
W, H = 200, 100

def f(v): return ("%.3f" % v).rstrip("0").rstrip(".")

def rrect(x, y, w, h, r):
    if r <= 0: return f"M{f(x)},{f(y)}H{f(x+w)}V{f(y+h)}H{f(x)}Z"
    return (f"M{f(x+r)},{f(y)}H{f(x+w-r)}A{f(r)},{f(r)} 0 0 1 {f(x+w)},{f(y+r)}V{f(y+h-r)}"
            f"A{f(r)},{f(r)} 0 0 1 {f(x+w-r)},{f(y+h)}H{f(x+r)}A{f(r)},{f(r)} 0 0 1 {f(x)},{f(y+h-r)}"
            f"V{f(y+r)}A{f(r)},{f(r)} 0 0 1 {f(x+r)},{f(y)}Z")

def chamfer(x, y, w, h, c):
    return (f"M{f(x+c)},{f(y)}H{f(x+w-c)}L{f(x+w)},{f(y+c)}V{f(y+h-c)}L{f(x+w-c)},{f(y+h)}"
            f"H{f(x+c)}L{f(x)},{f(y+h-c)}V{f(y+c)}Z")

def poly(pts): return "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + "Z"

def concave(d, r):
    """Ichki botiq burchakli plaket konturi, d mm ichkariga surilgan."""
    R = r + d
    a = math.sqrt(max(R*R - d*d, 0))
    return (f"M{f(a)},{f(d)}H{f(W-a)}A{f(R)},{f(R)} 0 0 0 {f(W-d)},{f(a)}V{f(H-a)}"
            f"A{f(R)},{f(R)} 0 0 0 {f(W-a)},{f(H-d)}H{f(a)}A{f(R)},{f(R)} 0 0 0 {f(d)},{f(H-a)}"
            f"V{f(a)}A{f(R)},{f(R)} 0 0 0 {f(a)},{f(d)}Z")

def grad(id_, stops, x1=0, y1=0, x2=0, y2=1, units=None):
    u = f' gradientUnits="{units}"' if units else ""
    s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in [(st + (None,))[:3] for st in stops])
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{s}</linearGradient>'

def rgrad(id_, stops, cx=0.5, cy=0.5, r=0.6, fx=None, fy=None):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in [(st + (None,))[:3] for st in stops])
    fxy = (f' fx="{fx}"' if fx is not None else "") + (f' fy="{fy}"' if fy is not None else "")
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}"{fxy}>{s}</radialGradient>'

def noise_filter(id_, freq, alpha, octaves=2, seed=3, tone=1.0):
    """Material teksturasi (cho'tkalangan metall / mat sirt / xira shisha)."""
    return (f'<filter id="{id_}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}" seed="{seed}"/>'
            f'<feColorMatrix type="matrix" values="{tone} 0 0 0 0  {tone} 0 0 0 0  {tone} 0 0 0 0  0 0 0 0 {alpha}"/>'
            f'</filter>')

def shadow_filter(id_, dx, dy, blur, op, color="#000"):
    return (f'<filter id="{id_}" x="-20%" y="-30%" width="140%" height="160%">'
            f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{blur}" flood-color="{color}" flood-opacity="{op}"/></filter>')

def glow_filter(id_, blur, color, op=1.0, strength=2):
    merges = "".join('<feMergeNode in="g"/>' for _ in range(strength))
    return (f'<filter id="{id_}" x="-10%" y="-40%" width="120%" height="180%">'
            f'<feGaussianBlur in="SourceAlpha" stdDeviation="{blur}" result="b"/>'
            f'<feFlood flood-color="{color}" flood-opacity="{op}"/><feComposite in2="b" operator="in" result="g"/>'
            f'<feMerge>{merges}<feMergeNode in="SourceGraphic"/></feMerge></filter>')

def T(text, font, size, x, y, fill, anchor="start", tracking=0.0, max_w=None, extra=""):
    d, w, s = tp.path(text, font, size, x, y, anchor, tracking, max_w)
    return f'<path d="{d}" fill="{fill}"{extra}/>', w

def standoff(p, x, y, r, kind="chrome"):
    """Distansion ushlagich qopqog'i (yuqoridan ko'rinish)."""
    g = f"{p}so_{kind}"
    return (f'<circle cx="{f(x+0.5)}" cy="{f(y+0.7)}" r="{f(r)}" fill="#000" opacity="0.25" filter="url(#{p}soft)"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="url(#{g})"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r*0.78)}" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="{f(r*0.06)}"/>'
            f'<ellipse cx="{f(x-r*0.3)}" cy="{f(y-r*0.35)}" rx="{f(r*0.38)}" ry="{f(r*0.18)}" fill="#fff" opacity="0.7" transform="rotate(-35 {f(x-r*0.3)} {f(y-r*0.35)})"/>')

def standoff_defs(p, kind="chrome"):
    if kind == "chrome":
        st = [(0, "#ffffff"), (0.35, "#d7dbdf"), (0.6, "#8e959c"), (0.85, "#c9ced3"), (1, "#6f767d")]
    elif kind == "gold":
        st = [(0, "#fff4cf"), (0.4, "#d8b56a"), (0.75, "#8f6b2c"), (1, "#c9a457")]
    else:
        st = [(0, "#f0f0f0"), (0.5, "#9a9a9a"), (1, "#5d5d5d")]
    return (rgrad(f"{p}so_{kind}", st, cx=0.4, cy=0.35, r=0.75) +
            f'<filter id="{p}soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.6"/></filter>')

# ---------------------------------------------------------------- logotip
import base64, os as _os
_LP = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "LOGOTIP", "METQ_logo_transparent.png")
LOGO_AR = 402 / 249          # asl nisbat (kenglik / balandlik) — o'zgartirilmaydi
_LOGO_URI = "data:image/png;base64," + base64.b64encode(open(_LP, "rb").read()).decode()

def logo(x, y, h, anchor="start"):
    """Rasmiy logotip: faqat proporsional masshtab, rang va shakl o'zgarmaydi."""
    w = h * LOGO_AR
    if anchor == "middle": x -= w / 2
    return f'<image x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" href="{_LOGO_URI}" preserveAspectRatio="xMidYMid meet"/>'

def logo_plate(cx, y, h, pad, fill, stroke=None, sw=0.3, r=1.6, extra=""):
    """To'q fonli dizaynlar uchun logotip ostidagi och plashka (logotipning o'zi o'zgarmaydi)."""
    w = h * LOGO_AR
    pw, ph = w + 2*pad, h + 2*pad
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{f(cx-pw/2)}" y="{f(y)}" width="{f(pw)}" height="{f(ph)}" rx="{r}" fill="{fill}"{st}{extra}/>'
            + logo(cx, y + pad, h, "middle")), pw, ph

# ---------------------------------------------------------------- dizaynlar
def d01(title, p):
    shape = rrect(0, 0, W, H, 5)
    fnt = "montserrat-700"; size = tp.fit_size(TITLES, fnt, 12.5, 142, 0.01)
    t, w = T(title, fnt, size, 34, 59, "#1e2b2f", tracking=0.01)
    co, cw = T(CO, "montserrat-600", tp.size_for_cap("montserrat-600", 3.0), 62, 26.6, "#4f9f34", tracking=0.12)
    defs = (grad(f"{p}bg", [(0, "#ffffff"), (1, "#f2f5f3")]) +
            grad(f"{p}gr", [(0, "#8fd05a"), (1, "#56a83a")], 0, 0, 1, 1) + standoff_defs(p) +
            f'<clipPath id="{p}clip"><path d="{shape}"/></clipPath>')
    body = (f'<path d="{shape}" fill="url(#{p}bg)"/>'
            f'<g clip-path="url(#{p}clip)">'
            f'<path d="{poly([(0,0),(22,0),(13,100),(0,100)])}" fill="url(#{p}gr)"/>'
            f'<path d="{poly([(25.2,0),(27,0),(18,100),(16.2,100)])}" fill="#b6df8c"/></g>'
            f'<path d="{rrect(0.15,0.15,W-0.3,H-0.3,4.85)}" fill="none" stroke="#dfe6e2" stroke-width="0.3"/>'
            + logo(34, 15, 15.5) + co + t +
            f'<rect x="34" y="66" width="28" height="1.3" fill="#56a83a"/>'
            f'<rect x="65" y="66.5" width="{f(max(40, 34+w-65))}" height="0.3" fill="#c9d4ce"/>'
            + "".join(standoff(p, x, y, 6) for x, y in [(9, 9), (9, 91), (191, 9), (191, 91)]))
    return defs, body, shape, [(9, 9, 3), (9, 91, 3), (191, 9, 3), (191, 91, 3)], "Distansion ushlagich Ø12 mm (4 dona)"

def d02(title, p):
    shape = chamfer(0, 0, W, H, 8)
    fnt = "cormorant-600"; size = tp.fit_size(TITLES, fnt, 13.5, 160, 0.08)
    t, w = T(title, fnt, size, 100, 60, f"url(#{p}gold)", "middle", 0.08)
    cs = tp.size_for_cap("cormorant-600", 2.9)
    co, cw = T(CO, "cormorant-600", cs, 100, 81, f"url(#{p}gold)", "middle", 0.22)
    gx = 100 - cw/2 - 4; gx2 = 100 + cw/2 + 4
    def diamond(x, y, s): return f'<path d="{poly([(x,y-s),(x+s,y),(x,y+s),(x-s,y)])}" fill="url(#{p}gold)"/>'
    defs = (grad(f"{p}gold", [(0, "#8a6a2f"), (0.25, "#e9d08c"), (0.45, "#b48c3d"), (0.7, "#f4e3a8"), (1, "#9b7834")], 0, 0, 1, 1) +
            rgrad(f"{p}bg", [(0, "#202020"), (1, "#0a0a0a")], r=0.75) +
            noise_filter(f"{p}matte", "0.9", 0.05, 2, 7))
    body = (f'<path d="{shape}" fill="url(#{p}bg)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}matte)"/>'
            f'<path d="{chamfer(4.5,4.5,W-9,H-9,6.2)}" fill="none" stroke="url(#{p}gold)" stroke-width="0.7"/>'
            f'<path d="{chamfer(6.3,6.3,W-12.6,H-12.6,5.4)}" fill="none" stroke="url(#{p}gold)" stroke-width="0.22"/>'
            f'<line x1="62" y1="21.5" x2="84" y2="21.5" stroke="url(#{p}gold)" stroke-width="0.3"/>'
            f'<line x1="116" y1="21.5" x2="138" y2="21.5" stroke="url(#{p}gold)" stroke-width="0.3"/>'
            + diamond(84.6, 21.5, 1.1) + diamond(115.4, 21.5, 1.1)
            + logo_plate(100, 12, 15.5, 1.6 - 0.8, "#f7f1e3", f"url(#{p}gold)", 0.45, 1.2)[0] + t +
            f'<line x1="{f(max(18, gx-24))}" y1="80" x2="{f(gx)}" y2="80" stroke="url(#{p}gold)" stroke-width="0.25"/>'
            f'<line x1="{f(gx2)}" y1="80" x2="{f(min(182, gx2+24))}" y2="80" stroke="url(#{p}gold)" stroke-width="0.25"/>'
            + co)
    return defs, body, shape, [], "Yashirin: 3M VHB ikki tomonlama lenta (orqa tomonda)"

def d03(title, p):
    shape = rrect(0, 0, W, H, 1.5)
    fnt = "inter-700"; size = tp.fit_size(TITLES, fnt, 14, 168, 0.0)
    t, w = T(title, fnt, size, 100, 64.5, "#111315", "middle", 0.0)
    co, cw = T(CO, "inter-600", tp.size_for_cap("inter-600", 2.9), 100, 36, "#1d2023", "middle", 0.16)
    a = 100 - cw/2 - 5; b = 100 + cw/2 + 5
    defs = (grad(f"{p}al", [(0, "#cfd3d7"), (0.22, "#f3f4f5"), (0.5, "#b6bbc0"), (0.78, "#e9ebed"), (1, "#c0c5ca")], 0, 0, 0.25, 1) +
            noise_filter(f"{p}brush", "0.0015 1.8", 0.32, 2, 11) +
            rgrad(f"{p}screw", [(0, "#ffffff"), (0.5, "#bfc4c9"), (1, "#7a8087")], 0.4, 0.35, 0.7))
    screws = "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="url(#{p}screw)" stroke="#8a9096" stroke-width="0.15"/>'
                     f'<circle cx="{x-0.6}" cy="{y-0.7}" r="0.7" fill="#fff" opacity="0.8"/>' for x, y in [(8,8),(192,8),(8,92),(192,92)])
    body = (f'<path d="{shape}" fill="url(#{p}al)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}brush)" style="mix-blend-mode:multiply"/>'
            f'<path d="{rrect(0.25,0.25,W-0.5,H-0.5,1.3)}" fill="none" stroke="#ffffff" stroke-opacity="0.8" stroke-width="0.35"/>'
            f'<path d="{shape}" fill="none" stroke="#7f868d" stroke-width="0.25"/>'
            f'<line x1="22" y1="35" x2="{f(a)}" y2="35" stroke="#1d2023" stroke-width="0.35"/>'
            f'<line x1="{f(b)}" y1="35" x2="178" y2="35" stroke="#1d2023" stroke-width="0.35"/>'
            + logo(100, 9, 15, "middle") + co + t +
            f'<rect x="88" y="75" width="24" height="1.1" fill="#111315"/>' + screws)
    return defs, body, shape, [(8,8,1.75),(192,8,1.75),(8,92,1.75),(192,92,1.75)], "Dekorativ qopqoqli vintlar M4 (4 dona) + VHB lenta"

def d04(title, p):
    shape = rrect(0, 0, W, H, 3)
    fnt = "jost-500"; size = tp.fit_size(TITLES, fnt, 13, 138, 0.06)
    t, w = T(title, fnt, size, 100, 59, "#18744a", "middle", 0.06)
    co, cw = T(CO, "jost-500", tp.size_for_cap("jost-500", 3.0), 100, 78.5, "#2f6f55", "middle", 0.2)
    defs = (grad(f"{p}fr", [(0, "#f3f8f7", 0.9), (0.5, "#e2ecea", 0.84), (1, "#d3e2df", 0.88)], 0, 0, 1, 1) +
            noise_filter(f"{p}frost", "1.6", 0.13, 1, 5) + standoff_defs(p) +
            grad(f"{p}sheen", [(0, "#ffffff", 0.55), (0.35, "#ffffff", 0), (1, "#ffffff", 0.0)], 0, 0, 0.6, 1))
    body = (f'<path d="{shape}" fill="url(#{p}fr)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}frost)"/>'
            f'<path d="{shape}" fill="url(#{p}sheen)"/>'
            f'<path d="{rrect(0.7,0.7,W-1.4,H-1.4,2.3)}" fill="none" stroke="#ffffff" stroke-opacity="0.85" stroke-width="1.2"/>'
            f'<path d="{shape}" fill="none" stroke="#8fbcb0" stroke-width="0.45"/>'
            + logo(100, 12, 17, "middle") + t + f'<rect x="70" y="67" width="60" height="0.4" fill="#18744a"/>'
            f'<circle cx="100" cy="67.2" r="1" fill="#18744a"/>' + co
            + "".join(standoff(p, x, y, 9.5) for x, y in [(14,14),(186,14),(14,86),(186,86)]))
    return defs, body, shape, [(14,14,4),(186,14,4),(14,86,4),(186,86,4)], "Xromlangan distansion ushlagich Ø19 mm (4 dona)"

def d05(title, p):
    shape = concave(0, 7)
    fnt = "playfair-700"; size = tp.fit_size(TITLES, fnt, 12.5, 160, 0.04)
    t, w = T(title, fnt, size, 100, 61, "#ffffff", "middle", 0.04)
    co, cw = T(CO, "montserrat-500", tp.size_for_cap("montserrat-500", 2.7), 100, 80, f"url(#{p}gold)", "middle", 0.24)
    defs = (rgrad(f"{p}em", [(0, "#176a4f"), (0.6, "#0e4836"), (1, "#082c21")], 0.5, 0.45, 0.75) +
            grad(f"{p}gold", [(0, "#b38b3f"), (0.4, "#f1d999"), (0.7, "#c49a48"), (1, "#e6c67b")], 0, 0, 1, 1) +
            noise_filter(f"{p}n", "0.8", 0.05, 2, 21))
    orn = (f'<line x1="64" y1="21.5" x2="84" y2="21.5" stroke="url(#{p}gold)" stroke-width="0.3"/>'
           f'<line x1="116" y1="21.5" x2="136" y2="21.5" stroke="url(#{p}gold)" stroke-width="0.3"/>'
           + logo_plate(100, 11.5, 15.5, 1.0, "#ffffff", f"url(#{p}gold)", 0.5, 2.2)[0])
    body = (f'<path d="{shape}" fill="url(#{p}em)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}n)"/>'
            f'<path d="{concave(3.6,7)}" fill="none" stroke="url(#{p}gold)" stroke-width="0.6"/>'
            f'<path d="{concave(5,7)}" fill="none" stroke="url(#{p}gold)" stroke-width="0.18"/>'
            + orn + t + f'<rect x="88" y="68.5" width="24" height="0.35" fill="url(#{p}gold)"/>' + co)
    return defs, body, shape, [], "Yashirin: 3M VHB lenta yoki orqa tomondan yelim"

def d06(title, p):
    shape = (f"M14,0H200V86A14,14 0 0 1 186,100H0V14A14,14 0 0 1 14,0Z")
    fnt = "raleway-700"; size = tp.fit_size(TITLES, fnt, 13.5, 150, 0.04)
    d, w, s = tp.path(title, fnt, size, 100, 60, "middle", 0.04)
    cd, cw, _ = tp.path(CO, "raleway-500", tp.size_for_cap("raleway-500", 2.9), 100, 73.5, "middle", 0.16)
    defs = (grad(f"{p}ac", [(0, "#eaf6f3", 0.42), (1, "#cfe5df", 0.3)], 0, 0, 1, 1) +
            grad(f"{p}sh", [(0, "#ffffff", 0.6), (0.3, "#ffffff", 0.05), (0.7, "#ffffff", 0), (1, "#ffffff", 0.25)], 0, 0, 1, 1) +
            shadow_filter(f"{p}ds", 0.5, 0.9, 0.55, 0.55) + standoff_defs(p))
    body = (f'<path d="{shape}" fill="url(#{p}ac)"/>'
            f'<path d="{shape}" fill="url(#{p}sh)"/>'
            f'<path d="M14.6,1.2H198.8V86A12.8,12.8 0 0 1 186,98.8H1.2V14.6A13.4,13.4 0 0 1 14.6,1.2Z" fill="none" stroke="#ffffff" stroke-opacity="0.9" stroke-width="0.6"/>'
            f'<path d="{shape}" fill="none" stroke="#7fb7a6" stroke-opacity="0.9" stroke-width="0.5"/>'
            f'<rect x="0" y="80" width="74" height="1.7" fill="#36a356"/>'
            f'<rect x="0" y="83.6" width="52" height="0.7" fill="#7cc98a"/>'
            f'<rect x="128" y="18" width="72" height="0.7" fill="#7cc98a"/>'
            f'<rect x="150" y="20.6" width="50" height="1.7" fill="#36a356"/>'
            f'<path d="{d}" fill="#9aa8a4" transform="translate(0.35 0.35)"/>'
            f'<path d="{d}" fill="#ffffff" filter="url(#{p}ds)"/>'
            f'<path d="{cd}" fill="#ffffff" filter="url(#{p}ds)"/>'
            + logo_plate(100, 13, 16, 1.2, "#ffffff", None, 0, 2, f' filter="url(#{p}ds)"')[0]
            + "".join(standoff(p, x, 50, 6.5) for x in (10, 190)))
    return defs, body, shape, [(10,50,3),(190,50,3)], "Xromlangan distansion ushlagich Ø16 mm (2 dona)"

def d07(title, p):
    shape = rrect(0, 0, W, H, 0.8)
    fnt = "cinzel-700"; size = tp.fit_size(TITLES, fnt, 12.5, 162, 0.06)
    d, w, s = tp.path(title, fnt, size, 100, 57.5, "middle", 0.06)
    cd, cw, _ = tp.path(CO, "cinzel-500", tp.size_for_cap("cinzel-500", 2.8), 100, 82, "middle", 0.18)
    defs = (grad(f"{p}wd", [(0, "#5b3923"), (0.35, "#43291a"), (0.65, "#573621"), (1, "#3a2416")], 0, 0, 0, 1) +
            f'<filter id="{p}grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.006 0.22" numOctaves="4" seed="9"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 0.09  0 0 0 0 0.05  0 0 0 0 0.02  0 0 1.6 0 -0.55"/></filter>'
            f'<filter id="{p}grain2" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="turbulence" baseFrequency="0.01 0.6" numOctaves="2" seed="4"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 0.75  0 0 0 0 0.5  0 0 0 0 0.3  1.2 0 0 0 -0.55"/></filter>' +
            grad(f"{p}steel", [(0, "#fbfbfb"), (0.35, "#c3c8cc"), (0.55, "#8d949a"), (0.8, "#e9ecee"), (1, "#a6adb3")], 0, 0, 0, 1) +
            shadow_filter(f"{p}ds", 0.45, 0.8, 0.5, 0.75) +
            grad(f"{p}edge", [(0, "#ffffff", 0.22), (0.06, "#ffffff", 0), (0.94, "#000", 0), (1, "#000", 0.35)], 0, 0, 0, 1))
    body = (f'<path d="{shape}" fill="url(#{p}wd)"/>'
            f'<path d="{shape}" fill="#000" filter="url(#{p}grain)"/>'
            f'<path d="{shape}" fill="#000" filter="url(#{p}grain2)" opacity="0.5"/>'
            f'<path d="{shape}" fill="url(#{p}edge)"/>'
            + logo_plate(100, 6.5, 15, 1.2, f"url(#{p}steel)", "#6f767c", 0.25, 0.8, f' filter="url(#{p}ds)"')[0] +
            f'<rect x="40" y="27" width="120" height="1.2" fill="url(#{p}steel)" filter="url(#{p}ds)"/>'
            f'<rect x="40" y="68" width="120" height="1.2" fill="url(#{p}steel)" filter="url(#{p}ds)"/>'
            f'<path d="{d}" fill="url(#{p}steel)" filter="url(#{p}ds)"/>'
            f'<path d="{cd}" fill="url(#{p}steel)" filter="url(#{p}ds)"/>')
    return defs, body, shape, [], "Yashirin: orqa tomonda freza qilingan kalit-teshik (keyhole) yoki VHB"

def d08(title, p):
    shape = rrect(0, 0, W, H, 0)
    fnt = "inter-400"; size = tp.fit_size(TITLES, fnt, 10.5, 172, 0.2)
    t, w = T(title, fnt, size, 100, 57, "#111111", "middle", 0.2)
    co, cw = T(CO, "inter-500", tp.size_for_cap("inter-500", 2.3), 100, 85, "#8a8d8f", "middle", 0.3)
    body = (f'<path d="{shape}" fill="#ffffff"/>'
            f'<path d="{rrect(0.1,0.1,W-0.2,H-0.2,0)}" fill="none" stroke="#e4e6e7" stroke-width="0.2"/>'
            + logo(100, 15, 13, "middle") + t + f'<rect x="88" y="66" width="24" height="0.5" fill="#2e9e5b"/>' + co)
    return "", body, shape, [], "Yashirin: 3M VHB ikki tomonlama lenta"

def d09(title, p):
    shape = "M0,0H190L200,10V100H10L0,90Z"
    inner = "M3,3H188.76L197,11.24V97H11.24L3,88.76Z"
    fnt = "orbitron-700"; size = tp.fit_size(TITLES, fnt, 11, 158, 0.07)
    t, w = T(title, fnt, size, 100, 58, "#d9ffe9", "middle", 0.07, extra=f' filter="url(#{p}glow)"')
    co, cw = T(CO, "exo2-500", tp.size_for_cap("exo2-500", 2.6), 100, 78, "#9db5a9", "middle", 0.2)
    led = "#2bff88"
    circ = ""
    for pts in [[(186,16),(170,16),(164,22),(148,22)], [(186,20),(176,20),(172,24)], [(186,88),(166,88),(162,84),(150,84)], [(186,91.5),(174,91.5),(171,88.5)]]:
        circ += f'<polyline points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="none" stroke="#1f9c5c" stroke-width="0.3"/>'
        circ += f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="0.8" fill="none" stroke="#2bff88" stroke-width="0.3"/>'
    defs = (grad(f"{p}bk", [(0, "#121a17"), (0.5, "#070b0a"), (1, "#020403")], 0, 0, 0, 1) +
            grad(f"{p}gl", [(0, "#ffffff", 0.1), (1, "#ffffff", 0)], 0, 0, 0.4, 1) +
            glow_filter(f"{p}glow", 0.9, led, 1, 3) + glow_filter(f"{p}lglow", 0.7, led, 1, 3))
    body = (f'<path d="{shape}" fill="url(#{p}bk)"/>'
            f'<clipPath id="{p}c"><path d="{shape}"/></clipPath>'
            f'<path d="M0,0H120L60,100H0Z" fill="url(#{p}gl)" clip-path="url(#{p}c)" opacity="0.6"/>'
            f'<path d="{inner}" fill="none" stroke="{led}" stroke-width="0.45" filter="url(#{p}lglow)"/>'
            + circ + logo_plate(30, 9, 13, 1.0, "#eef7f2", led, 0.4, 1.2, f' filter="url(#{p}lglow)"')[0] + t +
            f'<rect x="72" y="67" width="56" height="0.35" fill="{led}" filter="url(#{p}lglow)"/>' + co +
            f'<path d="{shape}" fill="none" stroke="#2a3330" stroke-width="0.3"/>')
    return defs, body, shape, [], "Alyuminiy orqa ramka 15 mm + yashirin kronshteyn; LED tasma ichida"

def d10(title, p):
    shape = rrect(0, 0, W, H, 0)
    front = [(5, 5), (168, 5), (195, 32), (195, 95), (20, 95), (5, 80)]
    fnt = "archivo-800"; cap = 15.5
    size = tp.fit_size(["DIREKTOR", T_QAB], fnt, cap, 160, 0.01)
    if " " in title:
        a, b = title.split(" ", 1)
        t1, _ = T(a, fnt, size, 22, 45, "#1f2428", tracking=0.01, extra=f' filter="url(#{p}ts)"')
        t2, _ = T(b, fnt, size, 22, 68, "#1f2428", tracking=0.01, extra=f' filter="url(#{p}ts)"')
        tt = t1 + t2
    else:
        tt, _ = T(title, fnt, size, 22, 64, "#1f2428", tracking=0.01, extra=f' filter="url(#{p}ts)"')
    co, cw = T(CO, "archivo-500", tp.size_for_cap("archivo-500", 2.6), 22, 85, "#2c9a54", tracking=0.14)
    defs = (grad(f"{p}bk", [(0, "#353b40"), (1, "#1f2327")], 0, 0, 1, 1) +
            grad(f"{p}fr", [(0, "#ffffff"), (1, "#eceff0")], 0, 0, 1, 1) +
            grad(f"{p}g1", [(0, "#58c26f"), (1, "#1f7f43")], 0, 0, 1, 1) +
            shadow_filter(f"{p}ls", 1.2, 1.6, 1.1, 0.55) + shadow_filter(f"{p}ts", 0.35, 0.55, 0.3, 0.35))
    body = (f'<path d="{shape}" fill="url(#{p}bk)"/>'
            f'<path d="{poly([(176,0),(200,0),(200,24)])}" fill="url(#{p}g1)"/>'
            f'<path d="{poly([(0,84),(0,100),(16,100)])}" fill="#2c9a54"/>'
            f'<path d="{poly(front)}" fill="url(#{p}fr)" filter="url(#{p}ls)"/>'
            f'<path d="{poly([(150,95),(195,50),(195,95)])}" fill="#e3e8e6"/>'
            f'<path d="{poly([(166,95),(195,66),(195,95)])}" fill="url(#{p}g1)"/>'
            f'<rect x="22" y="{25 if " " in title else 36}" width="10" height="1.6" fill="#2c9a54"/>'
            + logo(132, 11, 18) + tt + co)
    return defs, body, shape, [], "Yashirin: VHB lenta; old qatlam orqa qatlamga 3 mm distansion lenta bilan"

def d11(title, p):
    shape = rrect(0, 0, W, H, 14)
    fnt = "marcellus-400"; size = tp.fit_size(TITLES, fnt, 12, 156, 0.07)
    t, w = T(title, fnt, size, 100, 60, "#15120d", "middle", 0.07)
    co, cw = T(CO, "marcellus-400", tp.size_for_cap("marcellus-400", 2.7), 100, 82, "#2b2418", "middle", 0.24)
    defs = (grad(f"{p}ch", [(0, "#d6c09b"), (0.25, "#f2e5c9"), (0.5, "#c8b088"), (0.75, "#ecdcbc"), (1, "#cbb38c")], 0, 0, 1, 0.6) +
            noise_filter(f"{p}br", "0.002 1.5", 0.22, 2, 17))
    body = (f'<path d="{shape}" fill="url(#{p}ch)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}br)" style="mix-blend-mode:multiply"/>'
            f'<path d="{rrect(0.3,0.3,W-0.6,H-0.6,13.7)}" fill="none" stroke="#fff8e8" stroke-width="0.4"/>'
            f'<path d="{shape}" fill="none" stroke="#a48d66" stroke-width="0.3"/>'
            f'<path d="{rrect(4.5,4.5,W-9,H-9,10)}" fill="none" stroke="#5c4c33" stroke-width="0.35"/>'
            f'<path d="{rrect(5.8,5.8,W-11.6,H-11.6,8.8)}" fill="none" stroke="#5c4c33" stroke-width="0.15"/>'
            + logo(100, 11, 22, "middle") + t + f'<rect x="91" y="68" width="18" height="0.3" fill="#5c4c33"/>' + co +
            "".join(f'<circle cx="{x}" cy="88" r="0.5" fill="#5c4c33"/>' for x in (96, 100, 104)))
    return defs, body, shape, [], "Yashirin: 3M VHB lenta"

def d12(title, p):
    shape = rrect(0, 0, W, H, 2)
    fnt = "oswald-600"; size = tp.fit_size(TITLES, fnt, 16, 136, 0.04)
    d, w, s = tp.path(title, fnt, size, 16, 60, "start", 0.04)
    co, cw = T(CO, "oswald-400", tp.size_for_cap("oswald-400", 2.9), 16, 30, "#a7adb2", tracking=0.18)
    hatch = "".join(f'<line x1="{x}" y1="100" x2="{x+100}" y2="0" stroke="#7d8388" stroke-width="0.55"/>' for x in range(40, 200, 3))
    ticks = "".join(f'<line x1="{16+i*5}" y1="70" x2="{16+i*5}" y2="{72.6 if i%2==0 else 71.4}" stroke="#a7adb2" stroke-width="0.25"/>' for i in range(28))
    def hexb(x, y, r=3.1):
        pts = [(x + r*math.cos(math.radians(30+60*k)), y + r*math.sin(math.radians(30+60*k))) for k in range(6)]
        return (f'<circle cx="{x+0.4}" cy="{y+0.5}" r="{r}" fill="#000" opacity="0.45"/>'
                f'<path d="{poly(pts)}" fill="url(#{p}bolt)" stroke="#2a2c2e" stroke-width="0.2"/>'
                f'<circle cx="{x}" cy="{y}" r="{r*0.42}" fill="#2c2f31"/>'
                f'<path d="{poly([(x+r*0.24*math.cos(math.radians(60*k)), y+r*0.24*math.sin(math.radians(60*k))) for k in range(6)])}" fill="#121314"/>')
    defs = (grad(f"{p}gp", [(0, "#45494d"), (0.5, "#33363a"), (1, "#26282b")], 0, 0, 1, 1) +
            noise_filter(f"{p}sb", "1.2", 0.12, 2, 31) +
            grad(f"{p}bolt", [(0, "#e3e6e8"), (0.5, "#8d9398"), (1, "#5a5f63")], 0, 0, 1, 1) +
            f'<clipPath id="{p}hc"><rect x="160" y="34" width="26" height="52"/></clipPath>')
    body = (f'<path d="{shape}" fill="url(#{p}gp)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}sb)"/>'
            f'<path d="{rrect(0.3,0.3,W-0.6,H-0.6,1.7)}" fill="none" stroke="#5d6267" stroke-width="0.45"/>'
            f'<g clip-path="url(#{p}hc)">{hatch}</g>'
            f'<rect x="160" y="34" width="26" height="52" fill="none" stroke="#a7adb2" stroke-width="0.3"/>'
            + logo_plate(173, 14, 14.4, 1.0, "#d9dde0", "#2a2c2e", 0.2, 0.6)[0]
            + co +
            f'<path d="{d}" fill="#141516" transform="translate(0 -0.3)"/>'
            f'<path d="{d}" fill="#c9ced2"/>'
            f'<line x1="16" y1="70" x2="151" y2="70" stroke="#a7adb2" stroke-width="0.3"/>' + ticks
            + "".join(hexb(x, y) for x, y in [(8,8),(192,8),(8,92),(192,92)]))
    return defs, body, shape, [(8,8,2.25),(192,8,2.25),(8,92,2.25),(192,92,2.25)], "Olti qirrali boshli M4 boltlar (4 dona), shayba bilan"

def d13(title, p):
    shape = rrect(0, 0, W, H, 3)
    fnt = "manrope-800"; size = tp.fit_size(["DIREKTOR", T_QAB], fnt, 13, 104, 0.0)
    if " " in title:
        a, b = title.split(" ", 1)
        t1, _ = T(a, fnt, size, 14, 45, "#0f4a2c"); t2, _ = T(b, fnt, size, 14, 64, "#0f4a2c")
        tt = t1 + t2
    else:
        tt, _ = T(title, fnt, size, 14, 60, "#0f4a2c")
    co, cw = T(CO, "manrope-600", tp.size_for_cap("manrope-600", 2.5), 14, 85, "#3f8f45", tracking=0.1)
    defs = (grad(f"{p}g1", [(0, "#c8eba0"), (1, "#3c9c4b")], 0, 0, 1, 1) +
            grad(f"{p}g2", [(0, "#2f8a45"), (1, "#0d4a2a")], 0, 0, 1, 1) +
            grad(f"{p}g3", [(0, "#e3f5cc"), (1, "#9fd68a")], 0, 0, 1, 1) +
            grad(f"{p}ln", [(0, "#a6dc7e"), (1, "#0f5a31")], 0, 0, 1, 0) +
            f'<clipPath id="{p}c"><path d="{shape}"/></clipPath>')
    body = (f'<path d="{shape}" fill="#ffffff"/>'
            f'<g clip-path="url(#{p}c)">'
            f'<path d="{poly([(128,100),(200,100),(200,0),(170,0)])}" fill="url(#{p}g1)"/>'
            f'<path d="{poly([(152,100),(200,100),(200,34)])}" fill="url(#{p}g2)"/>'
            f'<path d="{poly([(118,100),(123,100),(181,0),(176,0)])}" fill="url(#{p}g3)"/>'
            f'<path d="{poly([(184,0),(200,0),(200,18)])}" fill="#0d4a2a"/>'
            f'<path d="{poly([(176,64),(190,40),(197,52)])}" fill="#ffffff" opacity="0.22"/></g>'
            f'<path d="{rrect(0.15,0.15,W-0.3,H-0.3,2.85)}" fill="none" stroke="#e1e7e3" stroke-width="0.3"/>'
            + logo(13, 8, 16) + tt + f'<rect x="14" y="74" width="26" height="1.3" fill="url(#{p}ln)"/>' + co)
    return defs, body, shape, [], "Yashirin: 3M VHB lenta"

def d14(title, p):
    shape = rrect(0, 0, W, H, 2)
    fnt = "michroma-400"; size = tp.fit_size(TITLES, fnt, 8.6, 168, 0.04)
    t, w = T(title, fnt, size, 100, 53 + tp.cap_height(fnt, size)/2, "#ffffff", "middle", 0.04)
    co, cw = T(CO, "michroma-400", tp.size_for_cap("michroma-400", 2.3), 100, 85, "#121416", "middle", 0.1)
    defs = (grad(f"{p}ti", [(0, "#8e959c"), (0.3, "#c3c8cd"), (0.55, "#80878f"), (0.8, "#b2b8be"), (1, "#7b828a")], 0, 0, 1, 1) +
            noise_filter(f"{p}br", "0.0018 2", 0.28, 2, 41) +
            grad(f"{p}gl", [(0, "#2a2f34"), (0.48, "#111417"), (0.52, "#07090a"), (1, "#14171a")], 0, 0, 0, 1))
    body = (f'<path d="{shape}" fill="url(#{p}ti)"/>'
            f'<path d="{shape}" fill="#fff" filter="url(#{p}br)" style="mix-blend-mode:multiply"/>'
            f'<path d="{rrect(0.25,0.25,W-0.5,H-0.5,1.8)}" fill="none" stroke="#e8ebee" stroke-opacity="0.8" stroke-width="0.35"/>'
            f'<path d="{shape}" fill="none" stroke="#5f666d" stroke-width="0.25"/>'
            + logo_plate(100, 7, 16.5, 1.2, "#f3f4f5", "#5f666d", 0.25, 1)[0] + co +
            f'<rect x="8" y="34" width="184" height="38" rx="1" fill="url(#{p}gl)"/>'
            f'<rect x="8.2" y="34.2" width="183.6" height="37.6" rx="0.9" fill="none" stroke="#4a5057" stroke-width="0.3"/>'
            f'<rect x="8" y="34" width="184" height="10" rx="1" fill="#fff" opacity="0.05"/>'
            + t +
            f'<rect x="88" y="77" width="24" height="0.5" fill="#121416"/>')
    return defs, body, shape, [], "Yashirin: 3M VHB lenta (titan rangli anodlangan alyuminiy)"

def tower(cx, base, h, sc=1.0, stroke="#9aa3ab", sw=0.28):
    """Yuqori kuchlanishli elektr uzatish tayanchi (ramziy siluet)."""
    bw, tw = 14*sc, 3.2*sc
    top = base - h
    L = []
    def ln(x1, y1, x2, y2): L.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')
    def xat(y, side):
        k = (base - y) / h
        half = bw/2 + (tw/2 - bw/2) * k
        return cx + side*half
    ln(xat(base, -1), base, xat(top, -1), top); ln(xat(base, 1), base, xat(top, 1), top)
    levels = [base - h*k for k in (0, 0.18, 0.36, 0.52, 0.66, 0.8, 1.0)]
    for i in range(len(levels)-1):
        y1, y2 = levels[i], levels[i+1]
        ln(xat(y1, -1), y1, xat(y2, 1), y2); ln(xat(y1, 1), y1, xat(y2, -1), y2)
        ln(xat(y2, -1), y2, xat(y2, 1), y2)
    arms = []
    for k, aw in ((0.66, 12*sc), (0.8, 9*sc), (0.93, 6.5*sc)):
        y = base - h*k
        ln(cx-aw, y, cx+aw, y)
        ln(cx-aw, y, xat(y - h*0.06, -1), y - h*0.06); ln(cx+aw, y, xat(y - h*0.06, 1), y - h*0.06)
        ln(cx-aw, y, cx-aw, y+2.2*sc); ln(cx+aw, y, cx+aw, y+2.2*sc)
        arms.append((cx-aw, y+2.2*sc)); arms.append((cx+aw, y+2.2*sc))
    ln(cx, top, cx, top-2.5*sc)
    return f'<g stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" fill="none">' + "".join(L) + "</g>", arms

def d15(title, p):
    shape = rrect(0, 0, W, H, 4)
    fnt = "exo2-700"; size = tp.fit_size(TITLES, fnt, 11.5, 122, 0.03)
    t, w = T(title, fnt, size, 14, 50, f"url(#{p}tg)", tracking=0.03)
    co, cw = T(CO, "exo2-500", tp.size_for_cap("exo2-500", 2.5), 14, 67, "#6f7a83", tracking=0.12)
    t1, a1 = tower(166, 97, 64, 1.0, "#8d979f", 0.3)
    t2, a2 = tower(191, 97, 40, 0.62, "#a9b1b8", 0.25)
    wires = ""
    for (x1, y1), (x2, y2) in zip(a1, a2):
        mx = (x1+x2)/2; wires += f'<path d="M{f(x1)},{f(y1)} Q{f(mx)},{f(max(y1,y2)+3)} {f(x2)},{f(y2)}" stroke="#a9b1b8" stroke-width="0.18" fill="none"/>'
    for i, (x1, y1) in enumerate(a1[0::2]):
        wires += (f'<path d="M{f(x1)},{f(y1)} Q{f(x1-60)},{f(y1+20+i*2)} {f(-2)},{f(y1+6+i*4)}" stroke="url(#{p}wg)" stroke-width="{0.32 if i==0 else 0.22}" fill="none"/>')
    pulse = (f'<path d="M14,58 H52 L54.5,54.5 L57.5,61 L60,56.5 L61.5,58 H96" fill="none" stroke="url(#{p}pl)" stroke-width="0.55" stroke-linejoin="round"/>'
             f'<circle cx="96" cy="58" r="0.9" fill="#3fae5a"/>')
    defs = (grad(f"{p}bg", [(0, "#ffffff"), (0.7, "#f7f9f8"), (1, "#e7ecea")], 0, 0, 0, 1) +
            grad(f"{p}tg", [(0, "#1f7a45"), (1, "#0c3f26")], 0, 0, 1, 0) +
            grad(f"{p}wg", [(0, "#3fae5a", 0), (0.4, "#3fae5a", 0.9), (1, "#9aa3ab", 0.9)], 0, 0, 1, 0) +
            grad(f"{p}pl", [(0, "#0f5a31"), (0.6, "#3fae5a"), (1, "#a6dc7e")], 0, 0, 1, 0) +
            f'<clipPath id="{p}c"><path d="{shape}"/></clipPath>')
    body = (f'<path d="{shape}" fill="url(#{p}bg)"/>'
            f'<g clip-path="url(#{p}c)">'
            f'<path d="M120,100 C150,92 176,80 200,58 V100Z" fill="#3fae5a" opacity="0.08"/>'
            f'<path d="M0,94 C60,90 140,92 200,76" stroke="#3fae5a" stroke-width="0.35" fill="none" opacity="0.7"/>'
            f'<path d="M0,97.5 C70,94 150,96 200,84" stroke="#9aa3ab" stroke-width="0.25" fill="none"/>'
            + wires + t2 + t1 + '</g>'
            f'<path d="{rrect(0.15,0.15,W-0.3,H-0.3,3.85)}" fill="none" stroke="#d5dcd9" stroke-width="0.3"/>'
            f'<rect x="0" y="12" width="4" height="22" fill="#3fae5a"/>'
            + logo(13, 10, 19) + t + pulse + co)
    return defs, body, shape, [], "Yashirin: 3M VHB lenta"

DESIGNS = [d01, d02, d03, d04, d05, d06, d07, d08, d09, d10, d11, d12, d13, d14, d15]

def sign_svg(n, title, p="s", standalone=True):
    defs, body, shape, holes, mount = DESIGNS[n-1](title, p)
    inner = f"<defs>{defs}</defs>{body}"
    if not standalone: return inner, shape, holes
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="100mm" viewBox="0 0 200 100">'
            f'<title>{title} — {CO}</title>{inner}</svg>')
