// PrepScore Worker: serves the static site, plus one endpoint that counts clicks on retailer links.
// The count is anonymous: no cookies, no IP address, no user agent. Only the page, the tracking ID,
// the product (ASIN), the button label and the section of the page are stored, with the date.
const ASIN = /^[A-Z0-9]{10}$/;
const TAG = /^[a-z0-9-]{1,40}-20$/;
const clip = (v, n) => (typeof v === "string" ? v.slice(0, n) : "");

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/click") return env.ASSETS.fetch(request);

    if (request.method !== "POST") return new Response(null, { status: 405 });
    const origin = request.headers.get("Origin");
    if (origin && origin !== "https://prepscore.org") return new Response(null, { status: 403 });

    let d;
    try { d = await request.json(); } catch { return new Response(null, { status: 400 }); }
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
  },
};
