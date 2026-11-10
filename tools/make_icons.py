"""Render the PrepScore icon to PNG/ICO sizes for the favicon set. Run when the logo changes:
python3 tools/make_icons.py  (needs playwright + Pillow; writes src/icons/, which build.py copies to dist/)."""
import io, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from build import BRAND_SVG
OUT = os.path.join(HERE, "src", "icons")
INK, PAPER, SURF = "#142019", "#ECEFE8", "#F7F8F3"
# Solid fill inside the crate so the icon reads on dark browser tabs too.
icon = (BRAND_SVG.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"')
        .replace('fill="none" stroke="currentColor"', f'fill="{SURF}" stroke="currentColor"').replace("currentColor", INK))

def render(px, pad=0.0, bg=None):
    inner = round(px * (1 - 2 * pad))
    html = (f'<html><body style="margin:0;background:{bg or "transparent"};width:{px}px;height:{px}px;display:grid;place-items:center">'
            f'<div style="width:{inner}px;height:{inner}px">{icon.replace("<svg ", "<svg width=\'100%\' height=\'100%\' ")}</div></body></html>')
    pg.set_viewport_size({"width": px, "height": px}); pg.set_content(html)
    return Image.open(io.BytesIO(pg.screenshot(omit_background=bg is None))).convert("RGBA")

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for px in (16, 32, 48, 192, 512):
        render(px).save(os.path.join(OUT, f"icon-{px}.png"))
    render(180, pad=0.12, bg=PAPER).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
    render(512, pad=0.18, bg=PAPER).save(os.path.join(OUT, "icon-maskable-512.png"))
    b.close()
Image.open(os.path.join(OUT, "icon-48.png")).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote", sorted(os.listdir(OUT)))
