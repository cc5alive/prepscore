"""Render the LA renter checklist to src/la-renters-checklist.pdf (copied to dist by build.py).
Run after changing the handout: python3 build.py && python3 tools/make_handout_pdf.py && python3 build.py
Needs playwright. Serves dist/ on a local port so fonts and styles load as on the site."""
import functools, http.server, os, threading
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(HERE, "dist"))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f"http://127.0.0.1:{srv.server_port}/la-renters.html"); pg.wait_for_timeout(800)
    pg.pdf(path=os.path.join(HERE, "src", "la-renters-checklist.pdf"), format="Letter",
           margin={"top": "0.45in", "bottom": "0.45in", "left": "0.5in", "right": "0.5in"})
    b.close()
srv.shutdown()
print("wrote src/la-renters-checklist.pdf")
