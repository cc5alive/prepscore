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

## Rules
- Never edit `dist/` by hand; it is rebuilt every time.
- Every affiliate button keeps `rel="sponsored nofollow noopener"` and its visible "Affiliate link" label. The disclosure box stays on every guide.
- No invented ratings, reviews or exact prices. Keep safety guidance accurate (FEMA, CDC, Red Cross).

## Cloudflare build settings (Workers Builds)
- Build command: `pip install -r requirements.txt && python3 build.py`
- Deploy command: `npx wrangler deploy`
- Root directory: `/`
