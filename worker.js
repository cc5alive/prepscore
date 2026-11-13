// PrepScore Worker: serves the static site, plus two small endpoints that count anonymous events.
// No cookies, no IP address, no user agent are stored.
// /api/click: clicks on retailer links (page, tracking ID, product ASIN, button label, page section, date).
// /api/event: use of the site's free tools (page, event name, short detail, date).
const ASIN = /^[A-Z0-9]{10}$/;
const TAG = /^[a-z0-9-]{1,40}-20$/;
const EVENTS = new Set(["use", "print", "share", "tool"]);
const clip = (v, n) => (typeof v === "string" ? v.slice(0, n) : "");

async function readJson(request) {
  if (request.method !== "POST") return [null, new Response(null, { status: 405 })];
  const origin = request.headers.get("Origin");
  if (origin && origin !== "https://prepscore.org") return [null, new Response(null, { status: 403 })];
  try { return [await request.json(), null]; } catch { return [null, new Response(null, { status: 400 })]; }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/click") {
      const [d, err] = await readJson(request);
      if (err) return err;
      const page = clip(d.p, 120);
      if (!page.startsWith("/")) return new Response(null, { status: 400 });
      const tag = TAG.test(clip(d.t, 44)) ? d.t : "";
      const asin = ASIN.test(clip(d.a, 10)) ? d.a : (d.a === "search" ? "search" : "");
      const label = clip(d.l, 60);
      const place = clip(d.s, 60).replace(/[^a-z0-9-]/gi, "");
      try {
        await env.CLICKS.prepare(
          "INSERT INTO clicks (day, page, tag, asin, label, place) VALUES (date('now'), ?, ?, ?, ?, ?)"
        ).bind(page, tag, asin, label, place).run();
      } catch (e) {
        return new Response(null, { status: 500 });
      }
      return new Response(null, { status: 204 });
    }

    if (url.pathname === "/api/event") {
      const [d, err] = await readJson(request);
      if (err) return err;
      const page = clip(d.p, 120);
      const name = clip(d.n, 10);
      if (!page.startsWith("/") || !EVENTS.has(name)) return new Response(null, { status: 400 });
      const detail = clip(d.d, 60).replace(/[^a-z0-9/-]/gi, "");
      try {
        await env.CLICKS.prepare(
          "INSERT INTO events (day, page, name, detail) VALUES (date('now'), ?, ?, ?)"
        ).bind(page, name, detail).run();
      } catch (e) {
        return new Response(null, { status: 500 });
      }
      return new Response(null, { status: 204 });
    }

    return env.ASSETS.fetch(request);
  },
};
