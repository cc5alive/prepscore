# PrepScore (prepscore.org)

Static emergency-preparedness site: a "How prepared am I?" quiz with shareable score cards, location prep guides, a scenario matrix and buyer's guides with Amazon affiliate links.

## How it works
- **All content lives in `data.py`**: site settings (domain, Amazon tag), scenarios, quiz items and weights, score tiers, locations and buyer's guides.
- **City guides live in `cities.py`**: one entry per city with its official alert sign-ups, evacuation zone lookup, hazards, priorities and FAQs. Re-check the alert links once a year and update `ALERTS_CHECKED`.
- `build.py` turns `data.py` and `cities.py` into the finished site in `dist/`: every page, sitemap.xml, robots.txt, structured data and share images.
- Every push to `main` makes Cloudflare run the build and deploy it to prepscore.org in about a minute.

## Adding or changing pages
1. Edit `data.py` (or `cities.py` for a new city). Copy an existing entry and keep the same keys. Only link to official government or utility sites for alerts and zones.
2. Optional local check: `pip install -r requirements.txt && python3 build.py`, then open `dist/index.html`.
3. Commit and push. Cloudflare deploys it.

## Keeping it fresh
- Bump `SITE["updated"]` in `data.py` when you change content. It drives the sitemap dates, the "Reviewed" line on guides and structured data.
- To link a pick to a specific Amazon product instead of a search, add `"asin": "B0XXXXXXX"` to that pick (copy the ASIN from Amazon's SiteStripe). For a direct brand affiliate link, add `"aff_url"` instead.
- Quick picks (`QUICK`), cited sources (`SOURCES`) and the quiz shopping list (`QUIZ_BUY`) are at the bottom of `data.py`.
- Internal links are written as clean URLs (`/guides/water`). To preview locally, serve `dist/` with something that maps `/page` to `page.html`, or open `wrangler dev`.

## Indexing safeguards
- `build.py` ends by running `tools/check_seo.py`. If a change adds an accidental `noindex`, breaks an internal link, drops a page from the sitemap, mismatches a canonical, duplicates a title or description, or writes structured data that doesn't parse, the build fails and Cloudflare keeps the last good version live. The log lists each problem.
- Structured data `dateModified` uses the same per-page date as the sitemap (from `lastmod.json`).
- IndexNow: the key is `vars.INDEXNOW_KEY` in `wrangler.jsonc`; the build publishes it as `/<key>.txt`. A daily Worker cron (15:17 UTC) pings IndexNow with pages whose sitemap date is today or yesterday. See results in the dashboard: Workers > prepscore > Logs. For a one-off full submission: `python3 tools/indexnow.py --all`.

## Rules
- Never edit `dist/` by hand; it is rebuilt every time.
- Every affiliate button keeps `rel="sponsored nofollow noopener"` and its visible "Affiliate link" label. The disclosure box stays on every guide.
- No invented ratings, reviews or exact prices. Keep safety guidance accurate (FEMA, CDC, Red Cross).

## Cloudflare build settings (Workers Builds)
- Build command: `pip install -r requirements.txt && python3 build.py`
- Deploy command: `npx wrangler deploy`
- Root directory: `/`
