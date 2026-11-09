# Manba (generator)

Barcha tablichkalar shu skriptlar bilan yaratilgan — o'zgartirish kiritib, qayta yaratish mumkin.

- `designs.py` — 15 dizayn (mm koordinatalarda, 200 × 100).
- `textpath.py` — matnni vektor konturga aylantirish (fontTools + HarfBuzz, kerning bilan).
- `meta.py` — material, o'rnatish, ranglar.
- `build.py` — SVG, texnik chizma, mockup, PDF/PNG uchun HTML, poster.
- `render.cjs` — Chromium (Playwright) orqali PNG / JPG / PDF.
- `catalog.py` — `index.html` va WebP previewlar.

Qayta yaratish:
```
npm i @fontsource/{montserrat,cormorant-garamond,jost,playfair-display,raleway,cinzel,orbitron,barlow,marcellus,oswald,manrope,michroma,exo-2,archivo}  # FONTSRC papkasida
pip install fonttools uharfbuzz pillow
FONTSRC=<papka> BUILD_TMP=/tmp/metq python3 build.py && node render.cjs /tmp/metq/jobs.json && python3 catalog.py
```
Shriftlar: Google Fonts (SIL Open Font License) va Inter (OFL).
