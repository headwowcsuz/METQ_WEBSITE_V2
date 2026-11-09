"""Matnni vektor konturga (SVG path) aylantirish: fontTools + HarfBuzz (kerning bilan).
Natijada SVG/PDF fayllarda shrift o'rnatish talab qilinmaydi."""
import io, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

FS = os.environ.get("FONTSRC", "")
def _fs(pkg, w):
    return f"{FS}/node_modules/@fontsource/{pkg}/files/{pkg}-latin-{w}-normal.woff"

FONTS = {
  "montserrat-600": _fs("montserrat", 600), "montserrat-500": _fs("montserrat", 500),
  "montserrat-700": _fs("montserrat", 700),
  "cormorant-600": _fs("cormorant-garamond", 600), "cormorant-500": _fs("cormorant-garamond", 500),
  "jost-500": _fs("jost", 500), "jost-400": _fs("jost", 400),
  "playfair-700": _fs("playfair-display", 700), "playfair-500": _fs("playfair-display", 500),
  "raleway-700": _fs("raleway", 700), "raleway-500": _fs("raleway", 500),
  "cinzel-700": _fs("cinzel", 700), "cinzel-500": _fs("cinzel", 500),
  "orbitron-700": _fs("orbitron", 700), "orbitron-500": _fs("orbitron", 500),
  "barlow-600": _fs("barlow", 600), "barlow-500": _fs("barlow", 500), "barlow-700": _fs("barlow", 700),
  "marcellus-400": _fs("marcellus", 400),
  "oswald-600": _fs("oswald", 600), "oswald-400": _fs("oswald", 400),
  "manrope-800": _fs("manrope", 800), "manrope-600": _fs("manrope", 600),
  "michroma-400": _fs("michroma", 400),
  "exo2-700": _fs("exo-2", 700), "exo2-500": _fs("exo-2", 500), "exo2-300": _fs("exo-2", 300),
  "archivo-800": _fs("archivo", 800), "archivo-500": _fs("archivo", 500),
  "inter-300": "/usr/share/fonts/opentype/inter/InterDisplay-Light.otf",
  "inter-400": "/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf",
  "inter-500": "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf",
  "inter-600": "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf",
  "inter-700": "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
}
# Katalog/spetsifikatsiya uchun shrift nomlari
FONT_NAMES = {
  "montserrat": "Montserrat", "cormorant": "Cormorant Garamond", "jost": "Jost",
  "playfair": "Playfair Display", "raleway": "Raleway", "cinzel": "Cinzel",
  "orbitron": "Orbitron", "barlow": "Barlow", "marcellus": "Marcellus", "oswald": "Oswald",
  "manrope": "Manrope", "michroma": "Michroma", "exo2": "Exo 2", "archivo": "Archivo",
  "inter": "Inter Display",
}
_cache = {}

def _load(key):
    if key in _cache: return _cache[key]
    tt = TTFont(FONTS[key]); tt.flavor = None
    buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
    tt = TTFont(io.BytesIO(data))
    face = hb.Face(data); f = hb.Font(face)
    upem = tt["head"].unitsPerEm
    os2 = tt["OS/2"]
    cap = getattr(os2, "sCapHeight", 0) or int(upem * 0.7)
    _cache[key] = (tt, f, upem, cap)
    return _cache[key]

def shape(text, key, size, tracking=0.0):
    """size = shrift o'lchami (em, mm). tracking = em ulushida harflar orasidagi qo'shimcha masofa."""
    tt, f, upem, cap = _load(key)
    cmap = tt.getBestCmap()
    missing = [c for c in text if ord(c) not in cmap]
    if missing: raise ValueError(f"{key} shriftida belgi yo'q: {missing!r}")
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(f, buf, {"kern": True, "liga": False})
    s = size / upem
    names = tt.getGlyphOrder()
    out, x = [], 0.0
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        out.append((names[info.codepoint], x + pos.x_offset * s, pos.y_offset * s))
        x += pos.x_advance * s
        if i < len(buf.glyph_infos) - 1: x += tracking * size
    return out, x, s, cap * s

def width(text, key, size, tracking=0.0):
    return shape(text, key, size, tracking)[1]

def cap_height(key, size):
    tt, f, upem, cap = _load(key); return cap * size / upem

def size_for_cap(key, cap_mm):
    tt, f, upem, cap = _load(key); return cap_mm * upem / cap

def path(text, key, size, x, y, anchor="start", tracking=0.0, max_w=None):
    """y = tayanch chiziq (baseline). Qaytaradi: (d, haqiqiy_kenglik, size)."""
    glyphs, w, s, capm = shape(text, key, size, tracking)
    if max_w and w > max_w:
        k = max_w / w; size *= k
        glyphs, w, s, capm = shape(text, key, size, tracking)
    tt = _load(key)[0]; gs = tt.getGlyphSet()
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    parts = []
    for name, gx, gy in glyphs:
        pen = SVGPathPen(gs, ntos=lambda v: ("%.3f" % v).rstrip("0").rstrip("."))
        tp = TransformPen(pen, (s, 0, 0, -s, x0 + gx, y - gy))
        gs[name].draw(tp)
        d = pen.getCommands()
        if d: parts.append(d)
    return " ".join(parts), w, size

def fit_size(texts, key, cap_mm, max_w, tracking=0.0):
    """Bir nechta matn uchun umumiy shrift o'lchami: cap balandlik maqsadi, lekin kenglikka sig'sin."""
    size = size_for_cap(key, cap_mm)
    for t in texts:
        w = width(t, key, size, tracking)
        if w > max_w: size *= max_w / w
    return size
