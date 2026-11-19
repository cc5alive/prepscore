// PrepScore Worker: serves the static site, plus two small endpoints that count anonymous events.
// No cookies, no IP address, no user agent are stored.
// /api/click: clicks on retailer links (page, tracking ID, product ASIN, button label, page section, date).
// /api/event: use of the site's free tools (page, event name, short detail, date).
// Daily cron: pings IndexNow with pages whose sitemap lastmod is today or yesterday (UTC).
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

// IndexNow: tell participating search engines (Bing, Yandex, Seznam, Naver...) which URLs changed.
// Google doesn't use IndexNow; it reads the sitemap.
async function pingIndexNow(env) {
  const key = env.INDEXNOW_KEY;
  if (!key) return;
  const res = await env.ASSETS.fetch(new Request("https://prepscore.org/sitemap.xml"));
  if (!res.ok) return console.log("indexnow: sitemap fetch failed", res.status);
  const xml = await res.text();
  const day = (d) => d.toISOString().slice(0, 10);
  const now = Date.now();
  const recent = new Set([day(new Date(now)), day(new Date(now - 864e5))]);
  const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc><lastmod>([^<]+)<\/lastmod>/g)]
    .filter((m) => recent.has(m[2])).map((m) => m[1]).slice(0, 10000);
  if (!urlList.length) return console.log("indexnow: nothing changed");
  const r = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host: "prepscore.org", key, keyLocation: `https://prepscore.org/${key}.txt`, urlList }),
  });
  console.log("indexnow:", r.status, urlList.length, "urls");
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(pingIndexNow(env));
  },

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
