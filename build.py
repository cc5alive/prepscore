# -*- coding: utf-8 -*-
"""Static site generator for PrepScore. Run: python3 build.py"""
import hashlib, html, json, os, posixpath, re, shutil, sys, urllib.parse, datetime
from data import SITE, SCENARIOS, MATRIX, QUIZ_CATS, QUIZ, TIERS, LOCATIONS, GUIDES, QUICK, SOURCES, QUIZ_BUY, KIT, KIT_PREMADE, KIT_EXTRAS, KIT_SOURCES, QUIZ_ACTIONS, PICK_SKIP
from cities import CITIES, REGIONS, ALERTS_CHECKED
from pool import POOL_CITIES
POOL_ASIDE = lambda root: (f'<div class="aside"><h3>Have a backyard pool?</h3><p class="muted small">It can back up your water supply, but not through a filter alone. '
                            f'<a href="{root}guides/pool-water.html">What it takes to drink pool water</a>.</p></div>')

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dist")
# Content date, not build date: drives sitemap lastmod, dateModified and "Reviewed" labels.
TODAY = SITE.get("updated") or datetime.date.today().isoformat()
REVIEWED = datetime.date.fromisoformat(TODAY).strftime("%B %Y")
AMAZON_LINE = "As an Amazon Associate, PrepScore earns from qualifying purchases."
HOST = SITE["url"].split("//", 1)[1].rstrip("/")
e = html.escape

# tier text color for chips (dark text on light tier colors)
for t in TIERS:
    t["text"] = "#142019" if t["slug"] in ("weekend-ready", "squared-away") else "#FFFFFF"

SCN = {s["id"]: s for s in SCENARIOS}
MX = {m["id"]: m for m in MATRIX}
GD = {g["slug"]: g for g in GUIDES}
LVL = {3: "Critical", 2: "Important", 1: "Useful", 0: "Not needed"}
TIER_LABEL = {"start": ("Start here", "Cheap, high-impact basics everyone should own."),
              "step": ("Step up", "Where most prepared households land."),
              "deep": ("Go deep", "For long outages, big households and rural homes.")}

FONTS = ("https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800;900"
         "&family=Big+Shoulders+Stencil+Display:wght@900&family=Public+Sans:wght@400;500;600;700&display=swap")

BRAND_SVG = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="3" '
             'fill="none" stroke="currentColor" stroke-width="3"/><rect x="3.5" y="3.5" width="25" height="7" fill="#F2B705"/>'
             '<path d="M2 10.5h28" stroke="currentColor" stroke-width="2.5"/><path d="M10 16v10M16 16v10M22 16v10" '
             'stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>')
CHECK_SVG = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def amazon(q):
    return "https://www.amazon.com/s?k=" + urllib.parse.quote_plus(q) + "&tag=" + SITE["amazon_tag"]


def buy_url(p):
    """Best link for a pick: a specific Amazon product (asin), a direct affiliate url, or an Amazon search."""
    if p.get("asin"):
        return f"https://www.amazon.com/dp/{p['asin']}?tag={SITE['amazon_tag']}"
    if p.get("aff_url"):
        return p["aff_url"]
    return amazon(p["q"])


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def dots(n):
    i = "".join('<i class="on"></i>' if k < n else "<i></i>" for k in range(3))
    return f'<span class="lv lv-{n}" role="img" aria-label="{LVL[n]}">{i}</span>'


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + p}
                                for i, (n, p) in enumerate(items)]}


def crumbs_html(items, root):
    parts = []
    for i, (n, p) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{e(n)}</span>')
        else:
            if p == "/":
                href = root + "index.html"
            elif p.endswith("/"):
                href = root + p.strip("/") + "/index.html"
            else:
                href = root + p.strip("/") + ".html"
            parts.append(f'<a href="{href}">{e(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "".join(parts) + "</nav>"


def asset(name):
    """Versioned asset URL: the ?v= hash changes whenever the file changes, so browsers
    that cached an older copy (assets are cached for a week) fetch the new one."""
    import hashlib
    with open(os.path.join(HERE, "src", name), "rb") as f:
        return f"assets/{name}?v={hashlib.sha1(f.read()).hexdigest()[:10]}"


def shell(*, path, title, desc, body, root, og, canon, jsonld=(), active="", scripts=(), body_attr="", noindex=False):
    # Only add the brand when it still fits in ~60 characters, so search results don't cut titles off.
    full_title = title if (SITE["name"] in title or len(title) + len(SITE["name"]) + 3 > 60) else f"{title} | {SITE['name']}"
    nav = [("quiz", "quiz.html", "Get your score"), ("where", "where/index.html", "Where you live"),
           ("cities", "city/index.html", "Cities"),
           ("scenarios", "scenarios.html", "Emergencies"), ("guides", "guides/index.html", "Gear guides")]
    navhtml = ""
    for key, href, label in nav[1:]:
        cur = ' aria-current="page"' if key == active else ""
        navhtml += f'<a href="{root}{href}"{cur}>{label}</a>'
    navhtml += f'<a class="btn" href="{root}quiz.html">Get your PrepScore</a>'
    loc_links = "".join(f'<li><a href="{root}where/{l["slug"]}.html">{e(l["name"])}</a></li>' for l in LOCATIONS)
    guide_links = "".join(f'<li><a href="{root}guides/{g["slug"]}.html">{e(g["short"])}</a></li>' for g in GUIDES) + f'<li><a href="{root}guides/pool-water.html">Drinking pool water</a></li>'
    head = f"""<title>{e(full_title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE['url']}{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE['url']}{canon}"><meta property="og:image" content="{SITE['url']}/og/{og}.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{f'<meta name="twitter:site" content="{SITE["twitter"]}">' if SITE['twitter'] else ''}
{'<meta name="robots" content="noindex, follow">' if noindex else ''}
<meta name="theme-color" content="#ECEFE8">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}{asset('site.css')}">
{''.join(ld(j) for j in jsonld)}"""
    page = f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="{root}index.html" aria-label="{SITE['name']} home">{BRAND_SVG}{SITE['name']}</a>
{'' if active == 'quiz' else f'<a class="btn head-cta" href="{root}quiz.html">Get your PrepScore</a>'}
<nav class="nav" aria-label="Main">{navhtml}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div class="stack"><a class="brand" href="{root}index.html">{BRAND_SVG}{SITE['name']}</a>
<p class="muted">Practical emergency preparedness for normal people. Find your gaps, fix the important ones first.</p>
<p class="muted small">{AMAZON_LINE} We also earn commissions from other links marked Affiliate. <a href="{root}disclosure.html">How we make money</a>.</p>
<p class="muted small">Guidance here is general information, not medical or legal advice. In an emergency, follow instructions from local officials.</p>
<p class="muted small">Questions or corrections: <a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div>
<div><h2 class="foot-h">Where you live</h2><ul>{loc_links}</ul></div>
<div><h2 class="foot-h">Gear guides</h2><ul>{guide_links}</ul></div>
<div><h2 class="foot-h">Tools</h2><ul><li><a href="{root}quiz.html">How prepared am I?</a></li><li><a href="{root}72-hour-kit.html">Simple 3-day kit</a></li><li><a href="{root}water-calculator.html">Water storage calculator</a></li><li><a href="{root}power-calculator.html">Power station calculator</a></li><li><a href="{root}food-calculator.html">Food storage calculator</a></li><li><a href="{root}city/index.html">City guides</a></li><li><a href="{root}scenarios.html">What matters in which emergency</a></li><li><a href="{root}guides/go-bag.html#checklist">Go-bag checklist</a></li><li><a href="{root}black-friday.html">Black Friday prep picks</a></li><li><a href="{root}preparedness-gifts.html">Preparedness gift guide</a></li><li><a href="{root}library.html">Printable guides and books</a></li><li><a href="{root}resources.html">Other great prep resources</a></li><li><a href="{root}about.html">About and editorial standards</a></li><li><a href="{root}disclosure.html">Affiliate disclosure</a></li><li><a href="{root}privacy.html">Privacy policy</a></li></ul></div>
</div></footer>
{''.join(f'<script src="{root}{asset(s)}"></script>' for s in scripts)}<script defer src="{root}{asset("track.js")}"></script>{BEACON}"""
    return head, page, body_attr


LINK_RE = re.compile(r'(href|src)="([^"]+)"')


def clean_links(doc, rel):
    """Rewrite relative links to root-absolute, clean URLs (/guides/water, /where/) so every
    internal click lands directly on the canonical address instead of going through a redirect."""
    base = posixpath.dirname("/" + rel)

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http:", "https:", "mailto:", "tel:", "data:", "#", "javascript:")):
            return m.group(0)
        path, frag = (url.split("#", 1) + [""])[:2]
        if not path:
            return m.group(0)
        if not path.startswith("/"):
            path = posixpath.normpath(posixpath.join(base, path))
        if path.endswith("/index.html"):
            path = path[: -len("index.html")]
        elif path.endswith(".html"):
            path = path[: -len(".html")]
        return f'{attr}="{path}{"#" + frag if frag else ""}"'

    return LINK_RE.sub(fix, doc)


PAGE_LANG = {"la-renters-es.html": "es"}
_LA_ALT = [("en", "/la-renters"), ("es", "/la-renters-es"), ("x-default", "/la-renters")]
HREFLANG = {"la-renters.html": _LA_ALT, "la-renters-es.html": _LA_ALT}


def write(rel, parts, artifact=False):
    head, page, body_attr = parts
    out = os.path.join(OUT if not artifact else ART, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if artifact and rel == "index.html":
        doc = head + "\n" + page
    else:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE["url"]}{u}">\n' for l, u in HREFLANG.get(rel, []))
        doc = f'<!doctype html>\n<html lang="{PAGE_LANG.get(rel, "en")}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{alt}{head}\n</head>\n<body{body_attr}>\n{page}\n</body>\n</html>\n'
        doc = clean_links(doc, rel)
        doc = section_tag(doc, rel)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    if not artifact:
        m = re.search(r'<main id="main">(.*)</main>', doc, re.S)
        HASHES[rel] = content_hash(m.group(1) if m else doc)


# Separate Amazon tracking IDs per section, so Associates reports show which part of the site earns.
SECTION_TAGS = [("quiz.html", "prepscorequiz-20"), ("guides/", "prepscoreguides-20"),
                ("black-friday.html", "prepscorebf-20"), ("72-hour-kit.html", "prepscorekit-20"), ("preparedness-gifts.html", "prepscoregifts-20")]


def tag_for(rel):
    for prefix, tag in SECTION_TAGS:
        if rel == prefix or (prefix.endswith("/") and rel.startswith(prefix)):
            return tag
    return SITE["amazon_tag"]


def section_tag(doc, rel):
    t = tag_for(rel)
    return doc if t == SITE["amazon_tag"] else doc.replace("tag=" + SITE["amazon_tag"], "tag=" + t)


def content_hash(main_html):
    """Hash a page's main content, ignoring "Month YYYY" review stamps and asset version strings."""
    t = re.sub(r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}", "", main_html)
    t = re.sub(r"\?v=[0-9a-f]+", "", t)
    t = re.sub(r"tag=[a-z0-9-]+-20", "tag=", t)
    return hashlib.sha1(t.encode()).hexdigest()[:16]


HASHES = {}  # rel -> hash of the page's main content, for real sitemap lastmod dates
PAGES = []  # (rel, parts, sitemap_path, priority)


def add(rel, parts, canon, prio="0.7"):
    PAGES.append((rel, parts, canon, prio))


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def tag_example(root):
    rows = [("Water", 62), ("Food", 70), ("Power", 40), ("Medical", 55), ("Comms", 35), ("Evacuation", 48)]
    man = "".join(f'<li><span>{n}</span><span class="bar"><i style="width:{v}%"></i></span></li>' for n, v in rows)
    t = TIERS[2]
    return f"""<figure class="tag" aria-label="Example PrepScore result" style="margin:0">
<div class="tag-top"><span>PrepScore manifest</span><span class="tier-chip" style="--tier:{t['color']};color:{t['text']}">{t['name']}</span></div>
<div class="tag-body"><div class="tag-days">11<small>days of supplies</small></div>
<div class="tag-score"><b>58</b><span>PrepScore / 100</span></div>
<div class="tag-tier">{t['name']}</div><p class="tag-line">{t['line']}</p></div>
<ul class="manifest">{man}</ul><div class="hazard"></div>
</figure><p class="example-note">Example result. Yours takes about 3 minutes.</p>"""


def matrix_table(items, highlight=None, caption=""):
    head = "".join(f'<th scope="col" data-col="{s["id"]}"{" class=\"col-on\"" if s["id"] == highlight else ""}>{e(s["short"])}</th>' for s in SCENARIOS)
    rows = ""
    for m in items:
        cells = "".join(f'<td data-col="{s["id"]}"{" class=\"col-on\"" if s["id"] == highlight else ""}>{dots(m["lv"][s["id"]])}</td>' for s in SCENARIOS)
        rows += f'<tr><th scope="row">{e(m["name"])}</th>{cells}</tr>'
    cap = f"<caption class=\"sr-only\" style=\"position:absolute;left:-9999px\">{e(caption)}</caption>" if caption else ""
    legend = '<div class="legend">' + "".join(f"<span>{dots(n)} {LVL[n]}</span>" for n in (3, 2, 1)) + "</div>"
    return f'<div class="table-wrap"><table class="matrix">{cap}<thead><tr><th scope="col">Item</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>{legend}'


def cta_quiz(root, loc=None):
    if loc:
        return f"""<div class="cta-box"><div><h2>How ready is your {e(loc['name'].lower())} home?</h2>
<p>The quiz weights every item for {e(loc['name'].lower())} risks and shows your top gaps. About 3 minutes, no sign-up.</p></div>
<a class="btn" href="{root}quiz.html#{loc['slug']}">Get your PrepScore</a></div>"""
    return f"""<div class="cta-box"><div><h2>How many days could you last?</h2>
<p>Check off what you have. Get a score, your top gaps and a card to share. About 3 minutes, no sign-up.</p></div>
<a class="btn" href="{root}quiz.html">Get your PrepScore</a></div>"""


LA_ASIDE = lambda root: (f'<div class="aside"><h3>Renting in LA?</h3><p class="muted small" style="margin-bottom:.5rem">A free one-page checklist with alert sign-ups, a building drill and what to ask your landlord. No product links.</p>'
                         f'<ul><li><a href="{root}../la-renters.html">LA renter emergency checklist</a></li></ul></div>')

# Cloudflare Web Analytics: cookieless, no consent banner needed. Set SITE["cf_beacon"] to the site token to turn it on.
BEACON = (f'\n<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{SITE["cf_beacon"]}"}}\'></script>'
          if SITE.get("cf_beacon") else "")
PRIVACY_UPDATED = "November 12, 2026"

DISCLOSE = lambda root: f'<p class="disclose">Some links on this page are affiliate links, marked <b>Affiliate</b>. If you buy through them we may earn a commission at no extra cost to you. {AMAZON_LINE} Commissions never decide what we recommend, and we include free options where they exist. <a href="{root}disclosure.html">How we pick and make money</a>.</p>'


def city_picker(root):
    groups = ""
    for r in REGIONS:
        cs = [c for c in CITIES if c["region"] == r]
        if cs:
            groups += f'<optgroup label="{e(r)}">' + "".join(f'<option value="/city/{c["slug"]}">{e(c["name"])}</option>' for c in cs) + "</optgroup>"
    return f"""<form class="city-pick" action="/city/" data-city-pick>
<label for="city-select">Find your city</label>
<div class="city-pick-row"><select id="city-select" name="city"><option value="">Choose a city…</option>{groups}</select>
<button class="btn sm" type="submit">Go</button></div>
<a class="small" href="{root}city/index.html">See all {len(CITIES)} city guides</a></form>"""

# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def build_home():
    root = ""
    locs = "".join(f'<a href="where/{l["slug"]}.html"><h3>{e(l["name"])}</h3><p>{e(l["threats"][0][0])}, {e(l["threats"][1][0].lower())} and more.</p></a>' for l in LOCATIONS)
    scen = ""
    for s in SCENARIOS:
        top = sorted([m for m in MATRIX if m["lv"][s["id"]] == 3], key=lambda m: -sum(m["lv"].values()))[:3]
        lis = "".join(f'<li><a href="guides/{m["guide"]}.html">{e(m["name"])}</a></li>' for m in top)
        scen += f'<article><h3>{e(s["name"])}</h3><p class="span">{e(s["span"])}</p><ol>{lis}</ol></article>'
    guides = "".join(f'<li><a href="guides/{g["slug"]}.html"><b>{e(g["name"])}</b><span>{e(g["short"])}</span></a></li>' for g in GUIDES)
    body = f"""<section class="hero"><div class="wrap">
<div><h1>How many days could you last on your own?</h1>
<p class="lede">PrepScore is a free emergency preparedness check. Tick off what you already have, and it weighs your supplies against the risks where you live, tells you how long they'd carry you, and shows the few gaps worth fixing first.</p>
<div class="cta-row"><a class="btn" href="quiz.html">Get your PrepScore</a><span class="muted small">About 3 minutes. No sign-up. Answers stay on your device.</span></div>
<p class="hero-alt">Just want the basics? <a href="72-hour-kit.html">Build the simple 3-day kit</a></p>{BF_PROMO(root) if bf_active() else ""}</div>
<div>{tag_example(root)}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Where you live changes the plan</h2><p>An apartment on the 14th floor and a farmhouse on a well fail in completely different ways. Start with your situation.</p></div><a href="where/index.html">All locations</a></div>
<div class="loc-grid">{locs}</div>
{city_picker(root)}
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>What matters in which emergency</h2><p>The three most critical items for each kind of event. A go-bag is everything in a wildfire and useless in a blizzard.</p></div><a href="scenarios.html">See the full matrix</a></div>
<div class="scen-grid">{scen}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Gear guides</h2><p>What to buy, how much you need and what to skip. Picks at three budgets, with the trade-offs spelled out.</p></div></div>
<ul class="guide-list">{guides}</ul>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Free calculators</h2><p>Your household's numbers in a minute. No sign-up, no product links.</p></div></div>
<ul class="guide-list"><li><a href="water-calculator.html"><b>Water storage calculator</b><span>How much water to store for 3 days, a week and two weeks, and the space and weight it takes.</span></a></li>
<li><a href="food-calculator.html"><b>Food storage calculator</b><span>Calories for 3 days, 2 weeks and a month, and an example pantry list sized for your household.</span></a></li>
<li><a href="power-calculator.html"><b>Power station calculator</b><span>Pick your fridge, CPAP, router and phones; get the battery size and output to buy.</span></a></li></ul>
</div></section>

<section class="section"><div class="wrap stack-l">
{cta_quiz(root)}
<p class="muted small read">We make money through affiliate links, clearly marked on every guide. We don't take paid placements or sell rankings. <a href="disclosure.html">Read how we pick gear</a>.</p>
</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": SITE["url"] + "/",
          "description": "Emergency preparedness score, location guides and gear buyer's guides."},
         {"@context": "https://schema.org", "@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/",
          "logo": SITE["url"] + "/og/default.png"}]
    add("index.html", shell(path="/", title=f"{SITE['name']}: How Prepared Are You for an Emergency?",
                            desc="Find out how many days you could last on your own. A free emergency preparedness score, location-specific prep guides and honest gear buyer's guides.",
                            body=body, root=root, og="default", canon="/", jsonld=j, scripts=("site.js",)), "/", "1.0")


# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------
def build_quiz():
    root = ""
    chips = "".join(f'<button type="button" class="chip" data-loc="{l["slug"]}" aria-pressed="false">{e(l["name"])}</button>' for l in LOCATIONS)
    cats_html = ""
    for c in QUIZ_CATS:
        items = ""
        for q in [q for q in QUIZ if q["cat"] == c["id"]]:
            if q.get("type") == "choice":
                opts = "".join(f'<label><input type="radio" name="{q["id"]}" id="{q["id"]}-{i}" value="{i}" data-q><span>{e(ch[0])}</span></label>' for i, ch in enumerate(q["choices"]))
                items += f'<div class="qchoice"><fieldset><legend>{e(q["label"])}</legend><div class="seg">{opts}</div></fieldset><p class="tip">{e(q["tip"])}</p></div>'
            else:
                items += f'<label class="qitem" for="{q["id"]}"><input type="checkbox" id="{q["id"]}" data-q><span class="qbox">{CHECK_SVG}</span><span><span class="t">{e(q["label"])}</span><span class="tip">{e(q["tip"])}</span></span></label>'
        guide = f' <a class="small" href="guides/{c["guide"]}.html">Guide</a>' if c["guide"] else ""
        cats_html += f'<section class="qcat" aria-labelledby="h-{c["id"]}"><div class="qcat-head"><h2 id="h-{c["id"]}">{e(c["name"])}{guide}</h2><span class="pct" data-cat-pct="{c["id"]}">0%</span></div>{items}</section>'
    man = "".join(f'<li><span>{e(c["short"])}</span><span class="bar"><i data-cat-bar="{c["id"]}"></i></span></li>' for c in QUIZ_CATS)
    body = f"""<div class="page-head quiz-head"><div class="wrap">
{crumbs_html([("Home", "/"), ("How prepared am I?", "/quiz")], root)}
<h1>How prepared am I?</h1>
<p class="dek">Check off what you have right now, not what you plan to buy. Your score updates as you go and is weighted for where you live.</p>
<p class="quiz-promise">About 3 minutes · No sign-up · Answers stay on your device</p>
</div></div>
<div class="wrap"><div class="quiz-layout">
<div>
<p class="city-note" id="city-note" hidden></p>
<div class="setup" style="margin-top:2rem">
<div><span class="lbl" style="font-weight:700;display:block;margin-bottom:.55rem">Where do you live?</span><div class="chips" role="group" aria-label="Where do you live">{chips}</div></div>
<div><span style="font-weight:700;display:block;margin-bottom:.55rem" id="people-label">People in your household</span>
<div class="stepper" role="group" aria-labelledby="people-label"><button type="button" id="people-minus" aria-label="Fewer people">&minus;</button><output id="people-out" aria-live="polite">2</output><button type="button" id="people-plus" aria-label="More people">+</button></div></div>
</div>
{cats_html}
<p style="margin-top:2rem"><button type="button" class="btn ghost sm" id="btn-reset">Clear my answers</button></p>
</div>
<aside class="quiz-side" aria-label="Your result" id="result">
<div class="tag" style="margin-top:2rem">
<div class="tag-top"><span data-out="loc">Suburbs</span><span class="tier-chip">Sitting Duck</span></div>
<div class="tag-body" aria-live="polite"><div class="tag-days"><span data-out="days">?</span><small data-out="dayword">days of supplies</small></div>
<div class="tag-score"><b data-out="score">0</b><span>PrepScore / 100</span></div>
<div class="tag-tier" data-out="tier">Sitting Duck</div><p class="tag-line" data-out="line"></p>
<p class="tag-limits" data-out="limits">Answer the water and food questions to see how long your supplies last.</p></div>
<ul class="manifest">{man}</ul><div class="hazard"></div>
</div>
<details class="how-scored"><summary>How this is calculated</summary><p><b>Days of supplies</b> is the shorter of your stored drinking water and your no-cook food. Water you can drain from a water heater counts; a filter doesn't, because it needs a water source. <b>The PrepScore</b> is the share of the checklist you have, with each item weighted for where you live (water and earthquake prep count more in earthquake country, for example). Your answers stay in your browser.</p></details>
<div style="margin-top:1.75rem"><h3>Your 2-week targets</h3>
<div class="targets" style="margin-top:.6rem"><div><b id="t-water">28 gal</b><span>water</span></div><div><b id="t-food">56k kcal</b><span>food</span></div><div><b id="t-bags">56</b><span>toilet bags</span></div></div></div>
<div style="margin-top:1.75rem" id="plan"><h3>Your plan for this week</h3><p style="margin:.2rem 0 .6rem;color:var(--muted);font-size:.92rem">Your three biggest gaps, weighted for where you live, each with a free or use-what-you-have option where there is one. Tick each one off above once it's handled.</p><ol class="gaps" id="gaps"></ol>
<div id="next-wrap" hidden><h4 class="next-h">After that</h4><ul class="next-list" id="next"></ul></div>
<div class="print-box"><button type="button" class="btn" id="btn-print">Print my plan</button><p>One page with your three actions, supply targets, local alert links and space to write down your household plan. No product links, so it's easy to share.</p></div>
<p class="aff" style="margin-top:.6rem">Buy links are affiliate links. {AMAZON_LINE}</p></div>
<div class="share-panel" style="margin-top:1.75rem" id="share">
<h3 style="margin-bottom:.75rem">Share your score</h3>
<canvas id="card" width="1200" height="630" aria-label="Your shareable PrepScore card"></canvas>
<div class="share-row"><button type="button" class="btn sm" id="btn-share">Share</button><button type="button" class="btn ghost sm" id="btn-save">Save image</button><button type="button" class="btn ghost sm" id="btn-copy">Copy link</button></div>
<div class="share-row small"><a id="s-x" href="#" target="_blank" rel="noopener">Post on X</a><a id="s-fb" href="#" target="_blank" rel="noopener">Facebook</a><a id="s-reddit" href="#" target="_blank" rel="noopener">Reddit</a><a id="s-wa" href="#" target="_blank" rel="noopener">WhatsApp</a></div>
<textarea id="copy-fallback" hidden rows="3" style="width:100%;margin-top:.5rem" aria-label="Link to copy"></textarea>
<p class="status" id="share-status" role="status"></p>
</div>
</aside>
</div></div>
<div class="mobile-bar empty"><span class="mb-score"><b data-out="score">0</b> <span data-out="tier">Sitting Duck</span></span><span class="mb-empty">Check items to see your score</span><a href="#result">See result</a></div>
<section class="plan-print" id="plan-print" aria-hidden="true"></section>"""
    buy = {}
    for qid, spec in QUIZ_BUY.items():
        if spec[0] == "q":
            buy[qid] = {"name": spec[2], "url": amazon(spec[1]), "aff": True}
        elif spec[0] == "asin":
            buy[qid] = {"name": spec[2], "url": buy_url({"asin": spec[1]}), "aff": True}
        else:
            pk = next(p for p in GD[spec[0]]["picks"] if p["name"] == spec[1])
            buy[qid] = {"name": pk["name"], "url": buy_url(pk) if pk.get("q") or pk.get("asin") else pk.get("url"), "aff": bool(pk.get("q") or pk.get("asin"))}
    cities = {c["slug"]: {"name": c["name"], "state": c["state"], "loc": c["parent"],
                          "alerts": [[a["label"], a["url"]] for a in c["alerts"][:2]] + ([[c["zone"]["label"], c["zone"]["url"]]] if c.get("zone") else []),
                          "pri": [[p[1], p[2]] for p in c["priorities"] if p[2]]} for c in CITIES}
    data = {"quiz": QUIZ, "cats": QUIZ_CATS, "tiers": TIERS, "buy": buy, "act": QUIZ_ACTIONS, "cities": cities,
            "locations": [{"slug": l["slug"], "name": l["name"], "mult": l["mult"], "item": l["item"]} for l in LOCATIONS],
            "site": {"url": SITE["url"], "host": HOST}}
    with open(os.path.join(HERE, "src", "data.js"), "w") as f:
        f.write(("window.PREP=" + json.dumps(data, separators=(",", ":")) + ";").replace("tag=" + SITE["amazon_tag"], "tag=" + tag_for("quiz.html")))
    j = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "PrepScore preparedness quiz",
          "url": SITE["url"] + "/quiz", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "description": "A free checklist that scores your emergency preparedness and estimates how many days you could last on your own."},
         crumbs_ld([("Home", "/"), ("How prepared am I?", "/quiz")])]
    add("quiz.html", shell(path="/quiz", title="How Prepared Am I? Free Emergency Preparedness Quiz",
                           desc="Check off what you have and get your PrepScore: how many days you could last on your own, your biggest gaps, and a card to share. Weighted for where you live.",
                           body=body, root=root, og="quiz", canon="/quiz", jsonld=j,
                           scripts=("data.js", "quiz.js"), body_attr=' class="has-bar" data-root=""', active="quiz"), "/quiz", "0.9")


# ---------------------------------------------------------------------------
# Score share pages
# ---------------------------------------------------------------------------
def build_scores():
    root = "../"
    for t in TIERS:
        ladder = "".join(f'<li{" aria-current=\"true\"" if x is t else ""}><span class="rng">{x["min"]}–{x["max"]}</span><span><span class="swatch" style="background:{x["color"]}"></span><b>{e(x["name"])}</b><br><span class="muted">{e(x["line"])}</span></span></li>' for x in TIERS)
        body = f"""<div class="page-head"><div class="wrap score-hero">
<div><p class="muted" id="who">Someone shared their PrepScore.</p>
<h1 style="font-family:var(--f-stencil);font-weight:900;font-size:clamp(3rem,8vw,5.5rem);line-height:.9">{e(t['name'])}</h1>
<p class="dek">{e(t['line'])}</p>
<p style="margin-top:1.75rem"><a class="btn" href="{root}quiz.html">How long would you last?</a></p></div>
<figure class="tag" style="margin:0">
<div class="tag-top"><span>PrepScore manifest</span><span class="tier-chip" style="--tier:{t['color']};color:{t['text']}">{e(t['name'])}</span></div>
<div class="tag-body"><div class="tag-days"><span id="d">?</span><small>days of supplies</small></div>
<div class="tag-score"><b id="s">{t['min']}+</b><span>PrepScore / 100</span></div>
<div class="tag-tier">{e(t['name'])}</div><p class="tag-line">Score range {t['min']} to {t['max']}</p></div><div class="hazard"></div></figure>
</div></div>
<section class="section"><div class="wrap two-col">
<div class="stack-l"><h2>Every tier</h2><ul class="tier-ladder">{ladder}</ul></div>
<div class="aside"><h3>Fix the basics first</h3><ul>
<li><a href="{root}guides/water.html">Two weeks of water</a></li><li><a href="{root}guides/radios.html">An emergency radio</a></li>
<li><a href="{root}guides/power.html">Power banks and a CO alarm</a></li><li><a href="{root}guides/go-bag.html">A packed go-bag</a></li>
<li><a href="{root}guides/sanitation.html">An emergency toilet</a></li></ul></div>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>
<script>(function(){{var m=(location.hash||"").match(/s(\\d+)(?:-d(\\d+))?/);if(!m)return;var s=+m[1];document.getElementById("s").textContent=s;if(m[2]==null){{document.getElementById("who").textContent="Someone scored "+s+".";return;}}var d=+m[2];document.getElementById("d").textContent=d>=90?"90+":d;document.getElementById("who").textContent="Someone scored "+s+" and has about "+(d>=90?"90+":d)+(d===1?" day":" days")+" of water and food stored.";}})();</script>"""
        add(f"score/{t['slug']}.html", shell(path=f"/score/{t['slug']}", title=f"I'm {t['name']} on PrepScore. How long would you last?",
                                           desc=f"{t['line']} Take the free 3-minute preparedness quiz and see how many days you could last on your own.",
                                           body=body, root=root, og=f"tier-{t['slug']}", canon=f"/score/{t['slug']}", noindex=True), None, None)


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------
def build_locations():
    root = "../"
    for l in LOCATIONS:
        threats = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in l["threats"])
        diff = "".join(f"<p>{e(p)}</p>" for p in l["different"])
        pri = ""
        for name, why, g in l["priorities"]:
            more = f'<a class="more" href="{root}guides/{g}.html">{e(GD[g]["short"])} guide</a>' if g else ""
            pri += f"<li><div><b>{e(name)}</b><p>{e(why)}</p>{more}</div></li>"
        skip = "".join(f"<li>{e(s)}</li>" for s in l["skip"])
        others = "".join(f'<li><a href="{o["slug"]}.html">{e(o["name"])}</a></li>' for o in LOCATIONS if o is not l)
        mine = [c for c in CITIES if c["parent"] == l["slug"]]
        city_aside = ('<div class="aside"><h3>City guides</h3><ul>' + "".join(f'<li><a href="{root}city/{c["slug"]}.html">{e(c["name"])}</a></li>' for c in mine) + "</ul></div>") if mine else ""
        gl = sorted({g for _, _, g in l["priorities"] if g})
        guides = "".join(f'<li><a href="{root}guides/{g}.html">{e(GD[g]["short"])}</a></li>' for g in gl)
        cr = [("Home", "/"), ("Where you live", "/where/"), (l["name"], f"/where/{l['slug']}")]
        body = f"""<div class="page-head"><div class="wrap">
{crumbs_html(cr, root)}<h1>{e(l['h1'])}</h1><p class="dek">{e(l['dek'])}</p></div></div>
<section class="section"><div class="wrap two-col">
<div class="stack-l">
<h2>What goes wrong here</h2><dl class="threats">{threats}</dl>
<h2 style="margin-top:3rem">What's different about your plan</h2><div class="stack read">{diff}</div>
<h2 style="margin-top:3rem">Do these first, in this order</h2><ol class="priority">{pri}</ol>
<h2 style="margin-top:3rem">Skip or put off</h2><ul class="skip read">{skip}</ul>
</div>
<aside class="stack-l">{city_aside}<div class="aside"><h3>Gear guides for you</h3><ul>{guides}</ul></div>
<div class="aside"><h3>Other places</h3><ul>{others}</ul></div></aside>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root, l)}</div></section>"""
        j = [{"@context": "https://schema.org", "@type": "Article", "headline": l["title"], "description": l["meta"],
              "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["name"]},
              "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + f"/og/loc-{l['slug']}.png",
              "mainEntityOfPage": SITE["url"] + f"/where/{l['slug']}"}, crumbs_ld(cr)]
        add(f"where/{l['slug']}.html", shell(path=f"/where/{l['slug']}", title=l["title"], desc=l["meta"], body=body, root=root,
                                            og=f"loc-{l['slug']}", canon=f"/where/{l['slug']}", jsonld=j, active="where"), f"/where/{l['slug']}", "0.8")
    # index
    items = "".join(f'<a href="{l["slug"]}.html"><h3>{e(l["name"])}</h3><p>{e(l["dek"])}</p></a>' for l in LOCATIONS)
    cr = [("Home", "/"), ("Where you live", "/where/")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}<h1>Prep for where you actually live</h1>
<p class="dek">Generic checklists treat every household the same. These guides start from what tends to fail in your kind of place, then put the fixes in order.</p></div></div>
<section class="section"><div class="wrap"><div class="loc-grid">{items}</div>
{city_picker(root)}</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    add("where/index.html", shell(path="/where/", title="Emergency Prep by Location: City, Suburbs, Rural and More",
                                  desc="Emergency prep guides for city apartments, suburbs, rural homes, hurricane coasts, wildfire country and earthquake zones.",
                                  body=body, root=root, og="default", canon="/where/", jsonld=[crumbs_ld(cr)], active="where", scripts=("site.js",)), "/where/", "0.8")


# ---------------------------------------------------------------------------
# Cities
# ---------------------------------------------------------------------------
LOC = {l["slug"]: l for l in LOCATIONS}


def city_links(root):
    return ", ".join(f'<a href="{root}city/{c["slug"]}.html">{e(c["name"])}</a>' for c in CITIES)


EXT = '<svg class="ext" viewBox="0 0 12 12" aria-hidden="true"><path d="M4.5 2.5h5v5M9.5 2.5 3 9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'


def alert_item(a, kind="alert"):
    return (f'<li class="signup"><div><b>{e(a["name"])}</b><p>{e(a["how"])}</p></div>'
            f'<a class="btn sm ghost" href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["label"])}{EXT}</a></li>')


def build_cities():
    root = "../"
    for c in CITIES:
        parent = LOC[c["parent"]]
        risks = "".join(f'<li>{e(r)}</li>' for r in c["risks"])
        alerts = "".join(alert_item(a) for a in c["alerts"])
        if c.get("zone"):
            alerts += alert_item(c["zone"])
        hazards = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in c["hazards"])
        notes = "".join(f"<p>{e(p)}</p>" for p in c["notes"])
        pri = ""
        for name, why, g in c["priorities"]:
            more = f'<a class="more" href="{root}guides/{g}.html">{e(GD[g]["short"])} guide</a>' if g else ""
            pri += f"<li><div><b>{e(name)}</b><p>{e(why)}</p>{more}</div></li>"
        faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in c["faqs"])
        region = sorted([o for o in CITIES if o is not c and o["region"] == c["region"]], key=lambda o: o["state"] != c["state"])
        same = [o for o in CITIES if o is not c and o["parent"] == c["parent"] and o not in region]
        near = (region + same)[:5]
        near_html = "".join(f'<li><a href="{o["slug"]}.html">{e(o["name"])}</a></li>' for o in near)
        gl = sorted({g for _, _, g in c["priorities"] if g})
        guides = "".join(f'<li><a href="{root}guides/{g}.html">{e(GD[g]["short"])}</a></li>' for g in gl)
        cr = [("Home", "/"), ("City guides", "/city/"), (c["name"], f"/city/{c['slug']}")]
        body = f"""<div class="page-head"><div class="wrap">
{crumbs_html(cr, root)}<h1>Prepping in {e(c['name'])}</h1><p class="dek">{e(c['dek'])}</p>
<ul class="risk-chips" aria-label="Main risks">{risks}</ul></div></div>
<section class="section"><div class="wrap two-col">
<div class="stack-l">
<div class="signups"><h2>Sign up today</h2><p class="muted">The official {e(c['name'])} alert and lookup tools. Each takes a few minutes and works even if you do nothing else on this page.</p>
<ul>{alerts}</ul><p class="muted small">Links checked {ALERTS_CHECKED}. Wireless Emergency Alerts reach most phones automatically; these add local detail.</p></div>
<h2 style="margin-top:3rem">What can go wrong in {e(c['name'])}</h2><dl class="threats">{hazards}</dl>
<h2 style="margin-top:3rem">What that means for your plan</h2><div class="stack read">{notes}</div>
<h2 style="margin-top:3rem">Do these first, in this order</h2><ol class="priority">{pri}</ol>
<h2 style="margin-top:3rem">Questions</h2><div class="faq">{faqs}</div>
</div>
<aside class="stack-l"><div class="aside"><h3>The full {e(parent['name'].lower())} guide</h3><p class="muted small" style="margin-bottom:.5rem">{e(c['name'])} follows the same playbook, with local details above.</p><ul><li><a href="{root}where/{parent['slug']}.html">{e(parent['h1'])}</a></li></ul></div>
<div class="aside"><h3>Gear guides</h3><ul>{guides}</ul></div>
{POOL_ASIDE(root) if c["slug"] in POOL_CITIES else ""}{LA_ASIDE(root) if c["slug"] == "los-angeles" else ""}<div class="aside"><h3>More cities</h3><ul>{near_html}<li><a href="index.html">All city guides</a></li></ul></div></aside>
</div></section>
<section class="section"><div class="wrap"><div class="cta-box"><div><h2>How ready is your {e(c['name'])} home?</h2>
<p>The quiz weights every item for {e(parent['name'].lower())} risks and shows your top gaps. About 3 minutes, no sign-up.</p></div>
<a class="btn" href="{root}quiz.html#{parent['slug']},{c['slug']}">Get your PrepScore</a></div></div></section>"""
        j = [{"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["meta"],
              "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["name"]},
              "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + f"/og/city-{c['slug']}.png",
              "mainEntityOfPage": SITE["url"] + f"/city/{c['slug']}",
              "about": {"@type": "City", "name": f"{c['name']}, {c['state']}"}},
             {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
             crumbs_ld(cr)]
        add(f"city/{c['slug']}.html", shell(path=f"/city/{c['slug']}", title=c["title"], desc=c["meta"], body=body, root=root,
                                           og=f"city-{c['slug']}", canon=f"/city/{c['slug']}", jsonld=j, active="cities"), f"/city/{c['slug']}", "0.8")
    # index
    groups = ""
    for r in REGIONS:
        cs = [c for c in CITIES if c["region"] == r]
        if not cs:
            continue
        items = "".join(f'<a href="{c["slug"]}.html"><h3>{e(c["name"])}</h3><p>{e(", ".join(c["risks"]))}</p></a>' for c in cs)
        groups += f'<h2 class="region-h">{e(r)}</h2><div class="loc-grid">{items}</div>'
    cr = [("Home", "/"), ("City guides", "/city/")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}<h1>City prep guides</h1>
<p class="dek">The local version: each city's official alert sign-ups, how to find your evacuation zone, what tends to go wrong there and what to do first.</p></div></div>
<section class="section"><div class="wrap stack-l">{groups}</div></section>
<section class="section"><div class="wrap stack-l"><p class="muted read">Don't see your city? Start with the guide for <a href="{root}where/index.html">your kind of place</a>, then search your county's name plus "emergency alerts" to find your local sign-up.</p>{cta_quiz(root)}</div></section>"""
    add("city/index.html", shell(path="/city/", title="Emergency Prep by City: Local Alerts, Zones and Risks",
                                 desc="City-by-city emergency prep guides with official alert sign-ups, evacuation zone lookups and local risks for Los Angeles, New York, Houston, Miami and more.",
                                 body=body, root=root, og="default", canon="/city/", jsonld=[crumbs_ld(cr)], active="cities"), "/city/", "0.8")


# ---------------------------------------------------------------------------
# Guides
# ---------------------------------------------------------------------------
POOL_CALLOUT = ('<div class="cta-box"><div><h2>Have a pool?</h2><p>It can hold years of water, but a filter alone won\'t make it drinkable, '
                'especially a saltwater pool. Here\'s what it takes.</p></div><a class="btn" href="pool-water.html">Read the pool water guide</a></div>')


def build_guides():
    root = "../"
    for g in GUIDES:
        hm = "".join(f'<div><dt>{e(a)}</dt><dd><span class="v">{e(b)}</span>{e(c)}</dd></div>' for a, b, c in g["howmuch"])
        PK = {p["name"]: p for p in g["picks"]}

        def buy_btn(p, compact=False):
            if p.get("q") or p.get("asin") or p.get("aff_url"):
                label = "Check price" if compact else ("Check price on Amazon" if not p.get("aff_url") else "Check price")
                target = p.get("asin_name") or (p["name"] if p.get("asin") else "Amazon search results")
                # Name the exact product only when the heading doesn't already (generic or "or similar" headings, search links)
                note = (f'<span class="link-to"><b>Our pick:</b> {e(target)}</span>'
                        if target != p["name"] or "or similar" in p["name"] else "")
                return (f'{note}<a class="btn sm" href="{e(buy_url(p))}" target="_blank" rel="sponsored nofollow noopener">{label}</a>'
                        f'<span class="aff">Affiliate link</span>')
            return (f'<a class="btn sm" href="{e(p["url"])}" target="_blank" rel="noopener">{"Find a class" if not compact else "Free"}</a>'
                    f'<span class="aff">Free, not an affiliate link</span>')

        quick = ""
        for label, name in QUICK.get(g["slug"], []):
            p = PK[name]
            quick += (f'<li><span class="qp-label">{e(label)}</span><div class="qp-main"><a class="qp-name" href="#pick-{slugify(name)}">{e(name)}</a>'
                      f'<span class="qp-why">{e(p["why"])}</span></div><div class="qp-buy"><span class="price">{band(p["price"])}</span>{buy_btn(p, True)}</div></li>')
        quick_html = (f'<section class="quickpicks" id="quick-picks" aria-labelledby="qp-h"><h2 id="qp-h">Quick picks</h2>'
                      f'<ul>{quick}</ul><p class="aff">{BAND_NOTE} Buy links are affiliate links; {AMAZON_LINE[0].lower() + AMAZON_LINE[1:]} '
                      f'<a href="{root}disclosure.html">Disclosure</a></p></section>') if quick else ""
        picks = ""
        for tier in ("start", "step", "deep"):
            ps = [p for p in g["picks"] if p["tier"] == tier]
            if not ps:
                continue
            lbl, sub = TIER_LABEL[tier]
            picks += f'<div class="tier-head" id="{tier}" style="margin-top:2.5rem"><h2>{lbl}</h2><p>{sub}</p></div>'
            for p in ps:
                picks += f"""<article class="pick" id="pick-{slugify(p['name'])}"><div><h3>{e(p['name'])}</h3>
<dl class="facts"><dt>What it is</dt><dd>{e(p['what'])}</dd><dt>Why</dt><dd>{e(p['why'])}</dd><dt>Watch out</dt><dd>{e(p['watch'])}</dd><dt>Skip it if</dt><dd>{e(PICK_SKIP[p['name']])}</dd></dl></div>
<div class="buy"><span class="price">{band(p['price'])}</span><span class="bestfor">Best for: {e(p['best'])}</span>{buy_btn(p)}</div></article>"""
        choose = "".join(f"<li>{e(x)}</li>" for x in g["choose"])
        mistakes = "".join(f"<li>{e(x)}</li>" for x in g["mistakes"])
        faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faqs"])
        srcs = SOURCES.get(g["slug"], [])
        sources = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in srcs)
        mx = [MX[i] for i in g["matrix"]]
        checklist = ""
        if g.get("checklist"):
            pfx = "ck" if g["slug"] == "go-bag" else f"ck-{g['slug']}"  # keep go-bag ids stable for saved progress
            lis = "".join(f'<li><label class="qitem" for="{pfx}-{i}"><input type="checkbox" id="{pfx}-{i}" data-ck><span class="qbox">{CHECK_SVG}</span><span class="t">{e(x)}</span></label></li>' for i, x in enumerate(g["checklist"]))
            checklist = (f'<section class="section printable" id="checklist"><div class="wrap"><div class="section-head"><div><h2>{e(g["name"])} checklist</h2>'
                         f'<p>Tick items as you pack. Your progress stays in this browser.</p></div>'
                         f'<div class="ck-tools"><span class="muted" id="ck-count"></span><button type="button" class="btn ghost sm" data-print>Print checklist</button></div></div>'
                         f'<ul class="check-grid">{lis}</ul></div></section>')
        whymx = "".join(f'<li><b>{e(m["name"])}</b>: {e(m["why"])}</li>' for m in mx)
        toc = [("quick-picks", "Quick picks")] if quick else []
        toc += [("how-much", "How much you need"), ("when", "When it matters"), ("start", "All picks")]
        if g.get("checklist"):
            toc.append(("checklist", "Checklist"))
        toc += [("choose", "How to choose"), ("faq", "Questions"), ("sources", "Sources")]
        toc_html = '<nav class="toc" aria-label="On this page"><span>On this page</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
        cr = [("Home", "/"), ("Gear guides", "/guides/"), (g["name"], f"/guides/{g['slug']}")]
        body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(g['h1'])}</h1><p class="dek">{e(g['dek'])}</p><p class="muted small" style="margin-top:1rem">Reviewed {REVIEWED} against guidance from {e(", ".join(sorted({t.split(":")[0] for t, _ in srcs})))}. Picks are researched from published specs, certifications and safety guidance, not hands-on tested by PrepScore. <a href="{root}disclosure.html">How we pick</a>.</p>
<p class="hero-alt">New to prepping? Start with <a href="{root}72-hour-kit.html">the simple 3-day kit</a>.</p></div></div>
<section class="section"><div class="wrap stack-l">
{quick_html}
{toc_html}
<h2 id="how-much">How much you need</h2><dl class="howmuch">{hm}</dl>
{f'<p class="read">For your household\'s exact amounts, space and weight, use the <a href="{root}water-calculator.html">water storage calculator</a>. Short on space? See <a href="apartment-water-storage.html">how to store water in an apartment</a>.</p>' if g["slug"] == "water" else ""}
{f'<p class="read">Power out in a winter storm? See the <a href="winter-storm-power-outage.html">winter outage checklist</a>: heating one room safely, protecting pipes and knowing when to leave.</p>' if g["slug"] in ("light-heat", "power") else ""}
{f'<p class="read">Driving in snow country? See <a href="stranded-in-car-winter.html">what to do if you\'re stuck in your car in a snowstorm</a>, with a printable winter checklist.</p>' if g["slug"] == "car" else ""}
{f'<p class="read">For your household\'s calories and an example pantry list, use the <a href="{root}food-calculator.html">food storage calculator</a>.</p>' if g["slug"] == "food" else ""}
{POOL_CALLOUT if g["slug"] == "water" else ""}
{f'<p class="read">To size a station for your own devices, use the <a href="{root}power-calculator.html">power station calculator</a>. Using a CPAP? See <a href="cpap-power-outage.html">nights per charge by setting and station size</a>.</p>' if g["slug"] == "power" else ""}
</div></section>
<section class="section" id="when"><div class="wrap stack-l">
<div class="section-head" style="margin:0"><div><h2>When it matters</h2><p>How important each item is in each kind of emergency.</p></div><a href="{root}scenarios.html">All items, all emergencies</a></div>
{matrix_table(mx, caption=g['name'] + ' importance by scenario')}
<ul class="plain-list read">{whymx}</ul>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">{DISCLOSE(root)}{picks}</div></section>
{checklist}
<section class="section"><div class="wrap two-col">
<div class="stack-l"><h2 id="choose">How to choose</h2><ul class="plain-list read">{choose}</ul>
<h2 style="margin-top:2.5rem">Mistakes to avoid</h2><ul class="plain-list read">{mistakes}</ul>
<h2 id="faq" style="margin-top:2.5rem">Questions</h2><div class="faq">{faqs}</div>
<h2 id="sources" style="margin-top:2.5rem">Sources</h2><ul class="plain-list read sources">{sources}</ul>
<p class="muted small read">We check this guide against these sources when we review it. Read <a href="{root}about.html">how we research and review</a>.</p></div>
<aside class="stack-l"><div class="aside"><h3>Other guides</h3><ul>{''.join(f'<li><a href="{o["slug"]}.html">{e(o["short"])}</a></li>' for o in GUIDES if o is not g)}</ul></div>
<div class="aside"><h3>By location</h3><ul>{''.join(f'<li><a href="{root}where/{l["slug"]}.html">{e(l["name"])}</a></li>' for l in LOCATIONS)}</ul></div></aside>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
        j = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["meta"],
              "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/about"},
              "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + f"/og/guide-{g['slug']}.png",
              "mainEntityOfPage": SITE["url"] + f"/guides/{g['slug']}",
              "citation": [{"@type": "CreativeWork", "name": t, "url": u} for t, u in srcs]},
             {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faqs"]]},
             {"@context": "https://schema.org", "@type": "ItemList", "name": g["h1"],
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["name"]} for i, p in enumerate(g["picks"])]},
             crumbs_ld(cr)]
        add(f"guides/{g['slug']}.html", shell(path=f"/guides/{g['slug']}", title=g["title"], desc=g["meta"], body=body, root=root,
                                             og=f"guide-{g['slug']}", canon=f"/guides/{g['slug']}", jsonld=j, active="guides",
                                             scripts=("site.js",)), f"/guides/{g['slug']}", "0.9")
    cr = [("Home", "/"), ("Gear guides", "/guides/")]
    lst = "".join(f'<li><a href="{g["slug"]}.html"><b>{e(g["name"])}</b><span>{e(g["dek"])}</span></a></li>' for g in GUIDES)
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}<h1>Emergency gear guides</h1>
<p class="dek">What to buy, how much of it, and what to skip. Every guide has picks at three budgets and shows which emergencies each item matters for.</p></div></div>
<section class="section"><div class="wrap stack-l"><div class="cta-box"><div><h2>New to this? Start here.</h2><p>The simple 3-day kit: eleven essentials, how much you need, and one product for each.</p></div><a class="btn" href="{root}72-hour-kit.html">See the 3-day kit</a></div>{DISCLOSE(root)}<ul class="guide-list">{lst}</ul>
<h2 style="margin-top:1rem">Deep dives</h2><ul class="guide-list"><li><a href="pool-water.html"><b>Drinking pool water</b><span>Chlorine and saltwater pools: why a filter isn't enough, and the gear that makes pool water drinkable as a last resort.</span></a></li>
<li><a href="apartment-water-storage.html"><b>Water storage for apartments</b><span>How much you need, which containers fit small spaces, and where to put 200+ pounds of water.</span></a></li>
<li><a href="winter-storm-power-outage.html"><b>Losing power in a winter storm</b><span>Heat one room safely, avoid carbon monoxide, keep pipes from freezing and know when to leave. Printable checklist.</span></a></li>
<li><a href="stranded-in-car-winter.html"><b>Stuck in your car in a snowstorm</b><span>What to do from the first minute, how much gas idling uses, and the winter extras for your car kit.</span></a></li>
<li><a href="cpap-power-outage.html"><b>CPAP in a power outage</b><span>How many nights a power station runs your CPAP by setting and size, what to buy, and how to set it up before an outage.</span></a></li></ul>
<p class="muted">Looking beyond PrepScore? See <a href="{root}resources.html">the best outside prep resources</a>, or <a href="{root}library.html">free printable guides and the best prepper books</a>.</p></div></section>"""
    add("guides/index.html", shell(path="/guides/", title="Emergency Preparedness Gear Guides", desc="Buyer's guides for emergency water, food, power, first aid, radios, lighting, go-bags and sanitation. Honest picks at three budgets.",
                                   body=body, root=root, og="default", canon="/guides/", jsonld=[crumbs_ld(cr)], active="guides"), "/guides/", "0.8")



# ---------------------------------------------------------------------------
# Simple 3-day kit
# ---------------------------------------------------------------------------

# Price bands instead of prices: Amazon only allows prices pulled live from its API, so next to
# retailer links we show a rough band, never a specific or recorded price.
BAND_RANGES = ["under $25", "$25 to $100", "$100 to $300", "over $300"]
BAND_NOTE = ("Price bands: $ under $25, $$ $25 to $100, $$$ $100 to $300, $$$$ over $300. "
             "They're a rough guide, not current prices. Check the retailer for today's price.")


def band(text):
    """'$90 to $120 for 4' -> $$$ band markup. Text with no dollar amount (Free, Varies) passes through."""
    nums = [float(x.replace(",", "")) for x in re.findall(r"\$\s?([\d,]+(?:\.\d+)?)", text)]
    if not nums:
        return e(text)
    v = (nums[0] + nums[1]) / 2 if len(nums) > 1 else nums[0]
    n = 4 if v >= 300 else 3 if v >= 100 else 2 if v >= 25 else 1
    return (f'<span class="band"><span aria-hidden="true"><b>{"$" * n}</b><i>{"$" * (4 - n)}</i></span>'
            f'<span class="sr">Price band: {BAND_RANGES[n - 1]}</span></span>')


def kit_buy(prod, label="Check price"):
    name, asin, price = prod[0], prod[1], prod[2]
    url = f"https://www.amazon.com/dp/{asin}?tag={SITE['amazon_tag']}"
    return (f'<div class="kit-prod"><div><span class="kit-pick">Our pick</span><b>{e(name)}</b>'
            f'{f"<span class=kit-note>{e(prod[3])}</span>" if len(prod) > 3 and prod[3] else ""}</div>'
            f'<div class="kit-buy"><span class="price">{band(price)}</span>'
            f'<a class="btn sm" href="{e(url)}" target="_blank" rel="sponsored nofollow noopener">{label}</a></div></div>')


KIT_TOOLS = {
    "water": '<a class="kit-more kit-tool" href="water-calculator.html">Work out your household\'s water</a>',
    "food": '<a class="kit-more kit-tool" href="food-calculator.html">Work out your household\'s food</a>',
    "power": '<a class="kit-more kit-tool" href="power-calculator.html">Need more than phones? Size a power station</a>',
}


def build_kit():
    root = ""
    items = ""
    for i, k in enumerate(KIT):
        prod = kit_buy(k["product"]) if k.get("product") else '<p class="kit-free">Nothing to buy. Gather what you already have.</p>'
        also = ""
        if k.get("also"):
            a = k["also"]
            url = f"https://www.amazon.com/dp/{a[1]}?tag={SITE['amazon_tag']}"
            also = f'<p class="kit-also">Plus: <a href="{e(url)}" target="_blank" rel="sponsored nofollow noopener">{e(a[0])}</a> ({band(a[2])})</p>'
        items += f"""<li class="kit-item" id="kit-{k['id']}"><div class="kit-head"><h3>{e(k['name'])}</h3><span class="kit-amt">{e(k['amount'])}</span></div>
<p>{e(k['why'])}</p><p class="kit-tip">{e(k['tip'])}</p>{prod}{also}
{KIT_TOOLS.get(k['id'], '')}<a class="kit-more" href="guides/{k['guide']}.html">More on {e(GD[k['guide']]['short'].lower())}</a></li>"""
    checklist = "".join(f'<li><label class="qitem" for="k3-{i}"><input type="checkbox" id="k3-{i}" data-ck><span class="qbox">{CHECK_SVG}</span><span class="t">{e(k["name"])}: {e(k["amount"].lower())}</span></label></li>' for i, k in enumerate(KIT))
    checklist += "".join(f'<li><label class="qitem" for="k3-x{i}"><input type="checkbox" id="k3-x{i}" data-ck><span class="qbox">{CHECK_SVG}</span><span class="t">{e(x)}</span></label></li>' for i, x in enumerate(KIT_EXTRAS))
    pm = KIT_PREMADE
    pm_url = f"https://www.amazon.com/dp/{pm[1]}?tag={SITE['amazon_tag']}"
    faqs = [
        ["What should be in a 72-hour emergency kit?", "At minimum: 3 gallons of water per person, 3 days of food that needs no cooking, a manual can opener, a headlamp or flashlight and a warm blanket per person, an emergency radio, a charged power bank, a first-aid kit, at least a week of medications, copies of important documents with some cash, N95 masks, and toilet bags with hygiene basics."],
        ["How much water do I need for 3 days?", "Plan on at least one gallon per person per day, so 3 gallons per person for 3 days. Add more for pets, nursing mothers, sick family members and hot weather."],
        ["How much food do I need for 3 days?", "Plan about 2,000 calories per adult per day, or roughly 6,000 per person for three days. Kids, nursing parents and anyone with dietary restrictions need their own food. Mix ration bars with familiar no-cook food like peanut butter, crackers, canned food and dried fruit."],
        ["Is a 3-day kit enough?", "It's the classic starting point and covers most power outages and short emergencies. Many local emergency agencies, especially in earthquake and hurricane regions, recommend building toward two weeks of supplies, especially water. Our guides for earthquake country and the hurricane coast cover what to add."],
        ["Should I just buy a pre-made kit?", "A pre-made kit is a fine way to start today. Most include some water, food bars and basic first aid, but they usually skimp on water, food and medications, and their flashlights, radios and first-aid kits are minimal. Use one as a base and add the items above."],
    ]
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in KIT_SOURCES)
    cr = [("Home", "/"), ("3-day kit", "/72-hour-kit")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>The simple 3-day emergency kit</h1>
<p class="dek">Eleven things that get your household through the first 72 hours of most emergencies. One shopping trip, one afternoon, and you're ahead of most of your neighbors.</p>
<p class="muted small" style="margin-top:1rem">Reviewed {REVIEWED} against Ready.gov, CDC and FDA guidance. Latest update: added warmth, and clarified food, water and medication amounts. {BAND_NOTE}</p>
<dl class="howmuch kit-stats" style="margin-top:1.75rem">
<div><dt>Water</dt><dd><span class="v">3 gal</span>per person, minimum</dd></div>
<div><dt>Food</dt><dd><span class="v">6,000 cal</span>per adult, no cooking needed</dd></div>
<div><dt>Time</dt><dd><span class="v">1 afternoon</span>to gather and pack</dd></div>
<div><dt>Cost if buying new</dt><dd><span class="v">$500+</span>for two people, less if you own some of it</dd></div>
</dl></div></div>
<section class="section"><div class="wrap two-col">
<div class="stack-l">
<p class="disclose">Product links on this page are affiliate links. {AMAZON_LINE} Commissions never decide what we recommend. <a href="{root}disclosure.html">How we pick</a>. {BAND_NOTE}</p>
<h2>The 11 essentials</h2>
<ol class="kit-list">{items}</ol>
<div class="kit-premade"><h3>Short on time? Start with a pre-made kit</h3>
<p>A ready-made backpack gets you water pouches, a food bar, a light stick and a small first-aid kit in one click. Pre-made kits are a fast start but usually skimp on water, food and medications, so use one as a base and add the items above, starting with a real headlamp, radio and power bank.</p>
<div class="kit-buy"><b>{e(pm[0])}</b><span class="price">{band(pm[2])}</span><a class="btn sm" href="{e(pm_url)}" target="_blank" rel="sponsored nofollow noopener">Check price</a></div></div>
</div>
<aside class="stack-l"><div class="aside"><h3>Keep it working</h3><ul class="plain-list small">
<li>Store it all in one bin or bag by the door or in a hall closet.</li>
<li>Check it twice a year, when the clocks change. Swap expired food, meds and batteries.</li>
<li>Tell everyone at home where it is.</li></ul></div>
<div class="aside"><h3>Ready for more?</h3><ul>
<li><a href="{root}quiz.html">See how prepared you are</a></li>
<li><a href="{root}guides/go-bag.html">Build a go-bag to evacuate</a></li>
<li><a href="{root}guides/water.html">Store two weeks of water</a></li>
<li><a href="{root}city/index.html">Find your city's alert sign-ups</a></li></ul></div></aside>
</div></section>
<section class="section printable" id="checklist"><div class="wrap">
<div class="section-head"><div><h2>Your 3-day kit checklist</h2><p>Tick things off as you gather them. Your progress stays in this browser.</p></div>
<div class="ck-tools"><span class="muted" id="ck-count"></span><button type="button" class="btn ghost sm" data-print>Print checklist</button></div></div>
<ul class="check-grid">{checklist}</ul></div></section>
<section class="section"><div class="wrap"><div class="section-head"><div><h2>Next step: plan for where you live</h2><p>How much to store, and what fails first, depends on your situation. Pick yours.</p></div><a href="city/index.html">Or find your city</a></div>
<div class="loc-grid">{"".join(f'<a href="where/{l["slug"]}.html"><h3>{e(l["name"])}</h3><p>{e(l["threats"][0][0])}, {e(l["threats"][1][0].lower())} and more.</p></a>' for l in LOCATIONS)}</div></div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2>Questions</h2><div class="faq">{faq_html}</div>
<h2 style="margin-top:2.5rem">Sources</h2><ul class="plain-list read sources">{srcs}</ul></div><div></div></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    prods = [k["product"] for k in KIT if k.get("product")]
    j = [{"@context": "https://schema.org", "@type": "Article", "headline": "The Simple 3-Day (72-Hour) Emergency Kit", "description": "Eleven essentials for a 72-hour emergency kit, with how much you need and one recommended product for each.",
          "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/about"},
          "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + "/og/kit.png", "mainEntityOfPage": SITE["url"] + "/72-hour-kit",
          "citation": [{"@type": "CreativeWork", "name": t, "url": u} for t, u in KIT_SOURCES]},
         {"@context": "https://schema.org", "@type": "ItemList", "name": "72-hour emergency kit essentials",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": k["name"]} for i, k in enumerate(KIT)]},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
         crumbs_ld(cr)]
    add("72-hour-kit.html", shell(path="/72-hour-kit", title="72-Hour Emergency Kit: The Simple 3-Day Checklist",
                                  desc="The simplest 72-hour emergency kit: 11 essentials for 3 days, how much water and food you need, and one recommended product for each. Printable checklist included.",
                                  body=body, root=root, og="kit", canon="/72-hour-kit", jsonld=j, scripts=("site.js",)), "/72-hour-kit", "0.9")

# ---------------------------------------------------------------------------
# Pool water deep dive
# ---------------------------------------------------------------------------
def aff_btn(asin, label="Check price"):
    url = f"https://www.amazon.com/dp/{asin}?tag={SITE['amazon_tag']}"
    return f'<a class="btn sm" href="{e(url)}" target="_blank" rel="sponsored nofollow noopener">{label}</a>'


def build_pool():
    import pool as P
    root = "../"
    hm = "".join(f'<div><dt>{e(a)}</dt><dd><span class="v">{e(b)}</span>{e(c)}</dd></div>' for a, b, c in P.HOWMUCH)
    verdict = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in P.VERDICT)
    crow = "".join(f'<tr><th scope="row">{e(a)}</th><td data-l="Typical in a pool">{e(b)}</td><td data-l="Guideline">{e(c)}</td><td data-l="What removes it">{e(d)}</td></tr>' for a, b, c, d in P.CONTAMINANTS)
    before = "".join(f"<li>{e(x)}</li>" for x in P.BEFORE)
    steps = lambda lst: "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in lst)
    salt_facts = "".join(f"<li>{e(x)}</li>" for x in P.SALT_FACTS)
    nopower = "".join(f"<li>{e(x)}</li>" for x in P.NO_POWER)
    cc = P.CC_PICK
    stages = "".join(f"<li><b>{e(a)}</b>{e(b)}</li>" for a, b in cc["stages"])
    yn = lambda v: f'<span class="yn {"y" if v.lower().startswith("yes") else "n"}">{e(v)}</span>'
    frow = "".join(f'<tr><th scope="row">{e(n)}<span class="pw-kind">{e(k)}</span></th><td data-l="Germs">{e(g)}</td><td data-l="Chlorine and taste">{yn(c)}</td><td data-l="Salt and stabilizer">{yn(s)}</td>'
                   f'<td class="pw-buy" data-l="Price band"><span class="price">{band(pr)}</span>{aff_btn(a)}</td></tr>' for n, a, pr, k, g, c, s, _ in P.FILTERS)
    fnotes = "".join(f"<li><b>{e(n.replace(' (CC' + chr(39) + 's pick)', ''))}:</b> {e(note)}</li>" for n, _, _, _, _, _, _, note in P.FILTERS)
    gear = "".join(f"""<article class="pick"><div><h3>{e(n)}</h3><dl class="facts"><dt>What it is</dt><dd>{e(w)}</dd><dt>Why</dt><dd>{e(y)}</dd></dl></div>
<div class="buy"><span class="price">{band(pr)}</span>{aff_btn(a, "Check price on Amazon")}<span class="aff">Affiliate link</span></div></article>""" for n, a, pr, w, y in P.GEAR)
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in P.FAQS)
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in P.SOURCES)
    toc = [("short-answer", "Short answer"), ("whats-in-it", "What's in pool water"), ("chlorine", "Chlorine pools"), ("salt", "Saltwater pools"),
           ("filters", "Filters compared"), ("gear", "Gear that removes salt"), ("faq", "Questions"), ("sources", "Sources")]
    toc_html = '<nav class="toc" aria-label="On this page"><span>On this page</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
    cr = [("Home", "/"), ("Gear guides", "/guides/"), ("Water", "/guides/water"), ("Pool water", "/guides/pool-water")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(P.H1)}</h1><p class="dek">{e(P.DEK)}</p>
<p class="muted small" style="margin-top:1rem">Reviewed {REVIEWED} against guidance from the CDC, FEMA, EPA and WHO. {BAND_NOTE}</p>
{toc_html}</div></div>
<section class="section"><div class="wrap stack-l">
<div class="pw-verdict" id="short-answer"><h2>The short answer</h2><ol>{verdict}</ol></div>
<dl class="howmuch">{hm}</dl>
</div></section>
<section class="section" id="whats-in-it"><div class="wrap stack-l">
<div class="section-head" style="margin:0"><div><h2>What's in pool water</h2><p>Germs are the easy part. The hard part is what's dissolved in the water, because filters can't catch it.</p></div></div>
<div class="table-wrap"><table class="matrix pw-table"><thead><tr><th scope="col">What</th><th scope="col">Typical in a pool</th><th scope="col">Drinking-water guideline</th><th scope="col">What removes it</th></tr></thead><tbody>{crow}</tbody></table></div>
</div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2>Before an emergency</h2><ul class="plain-list read">{before}</ul>
<h2 id="chlorine" style="margin-top:2.5rem">Chlorinated pools, step by step</h2>
<ol class="pw-steps">{steps(P.CHLORINE_STEPS)}</ol>
<div class="disclose"><b>If you can't distill or run RO.</b> {e(P.LAST_RESORT)}</div>
<h2 id="salt" style="margin-top:2.5rem">Saltwater pools, step by step</h2>
<ul class="plain-list read">{salt_facts}</ul>
<ol class="pw-steps">{steps(P.SALT_STEPS)}</ol>
<h2 style="margin-top:2.5rem">No power? Distill it on a stove</h2>
<ul class="plain-list read">{nopower}</ul>
</div>
<aside class="stack-l"><div class="aside"><h3>Use pool water for</h3><ul class="plain-list small"><li>Flushing toilets (pour a bucket into the bowl)</li><li>Washing hands, bodies and dishes</li><li>Cleaning</li><li>Putting out small fires</li><li>Drinking only after distilling or RO</li></ul></div>
<div class="aside"><h3>Related guides</h3><ul><li><a href="water.html">Emergency water storage</a></li><li><a href="power.html">Power for a distiller</a></li><li><a href="sanitation.html">Sanitation without running water</a></li><li><a href="{root}72-hour-kit.html">The simple 3-day kit</a></li></ul></div></aside>
</div></section>
<section class="section" id="filters"><div class="wrap stack-l">
<div class="section-head" style="margin:0"><div><h2>Filters compared</h2><p>Every one of these is a good final step after distilling or RO. None of them removes salt or stabilizer on its own.</p></div></div>
{DISCLOSE(root)}
<div class="pw-cc"><div><span class="kit-pick">What I bought</span><h3>{e(cc['name'])}</h3>
<p class="pw-quote">“{e(P.CC_NOTE)}” <span class="muted">CC Pearce, site creator</span></p>
<ul class="pw-stages">{stages}</ul><p class="muted small">{e(cc['limits'])}</p></div>
<div class="kit-buy"><span class="price">{band(cc['price'])}</span>{aff_btn(cc['asin'])}</div></div>
<div class="table-wrap"><table class="matrix pw-table"><thead><tr><th scope="col">Filter</th><th scope="col">Germs</th><th scope="col">Chlorine and taste</th><th scope="col">Salt and stabilizer</th><th scope="col">Price band</th></tr></thead><tbody>{frow}</tbody></table></div>
<ul class="plain-list read small pw-notes">{fnotes}</ul>
</div></section>
<section class="section" id="gear"><div class="wrap"><h2>Gear that removes salt and stabilizer</h2>
<p class="muted read" style="margin-top:.5rem">These are the pieces that make pool water drinkable, plus the cheap tools that tell you it worked.</p>{gear}</div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2 id="faq">Questions</h2><div class="faq">{faq_html}</div>
<h2 id="sources" style="margin-top:2.5rem">Sources</h2><ul class="plain-list read sources">{srcs}</ul>
<p class="muted small read">This guide is general information, not medical advice. If someone gets sick after drinking treated water, call a doctor or poison control (1-800-222-1222).</p></div><div></div></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "Article", "headline": P.TITLE, "description": P.META, "dateModified": TODAY,
          "author": {"@type": "Person", "name": "CC Pearce", "url": "https://ccpearce.com"},
          "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + "/og/guide-pool-water.png",
          "mainEntityOfPage": SITE["url"] + "/guides/pool-water",
          "citation": [{"@type": "CreativeWork", "name": t, "url": u} for t, u in P.SOURCES]},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P.FAQS]},
         {"@context": "https://schema.org", "@type": "HowTo", "name": "How to make chlorinated pool water drinkable in an emergency",
          "step": [{"@type": "HowToStep", "name": a, "text": b} for a, b in P.CHLORINE_STEPS]},
         crumbs_ld(cr)]
    add("guides/pool-water.html", shell(path="/guides/pool-water", title=P.TITLE, desc=P.META, body=body, root=root, og="guide-pool-water",
                                       canon="/guides/pool-water", jsonld=j, active="guides"), "/guides/pool-water", "0.8")


# ---------------------------------------------------------------------------
# Outside resources
# ---------------------------------------------------------------------------
def build_resources():
    import resources as R
    root = ""
    secs = ""
    allres = []
    for sid, title, sub, items in R.SECTIONS:
        cards = ""
        for name, url, by, kind, best, about, watch in items:
            allres.append((name, url))
            w = f'<p class="rs-watch"><b>Keep in mind:</b> {e(watch)}</p>' if watch else ""
            cards += f"""<article class="rs-card"><div class="rs-top"><span class="rs-kind rs-{kind.lower()}">{e(kind)}</span><span class="rs-by">{e(by)}</span></div>
<h3><a href="{e(url)}" target="_blank" rel="noopener">{e(name)}</a></h3>
<p class="rs-best"><b>Best for:</b> {e(best)}</p><p class="rs-about">{e(about)}</p>{w}
<a class="rs-go" href="{e(url)}" target="_blank" rel="noopener">Visit {e(url.split("//")[1].split("/")[0].replace("www.", ""))}<span aria-hidden="true"> ↗</span></a></article>"""
        secs += f"""<section class="section" id="{sid}"><div class="wrap"><div class="section-head"><div><h2>{e(title)}</h2><p>{e(sub)}</p></div></div>
<div class="rs-grid">{cards}</div></div></section>"""
    toc_html = '<nav class="toc" aria-label="On this page"><span>On this page</span>' + "".join(f'<a href="#{s[0]}">{e(s[1])}</a>' for s in R.SECTIONS) + "</nav>"
    cr = [("Home", "/"), ("Resources", "/resources")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(R.H1)}</h1><p class="dek">{e(R.DEK)}</p>
<p class="muted small" style="margin-top:1rem">Checked {REVIEWED}. None of these are affiliate links, and nobody paid to be listed.</p>
{toc_html}</div></div>
{secs}
<section class="section"><div class="wrap two-col"><div class="stack-l read">
<h2>How we chose these</h2>
<ul class="plain-list"><li>Official and nonprofit sources first, because they're accountable and free.</li>
<li>Independent sites only when they add something the official ones don't, like tested gear or a deeper explanation.</li>
<li>Each one is here for a specific job. If a site is weak on something, we say so.</li>
<li>Know a resource that belongs here? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a> or tell us on X at <a href="https://x.com/cc5alive" target="_blank" rel="noopener">@cc5alive</a>.</li></ul></div>
<aside class="stack-l"><div class="aside"><h3>On PrepScore</h3><ul><li><a href="library.html">Printable guides and books</a></li><li><a href="quiz.html">How prepared am I?</a></li><li><a href="72-hour-kit.html">The simple 3-day kit</a></li><li><a href="guides/index.html">Gear guides</a></li><li><a href="city/index.html">City guides</a></li></ul></div></aside></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": R.TITLE, "description": R.META, "url": SITE["url"] + "/resources",
          "dateModified": TODAY, "publisher": {"@type": "Organization", "name": SITE["name"]},
          "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": u} for i, (n, u) in enumerate(allres)]}},
         crumbs_ld(cr)]
    add("resources.html", shell(path="/resources", title=R.TITLE, desc=R.META, body=body, root=root, og="resources",
                                canon="/resources", jsonld=j), "/resources", "0.7")


# ---------------------------------------------------------------------------
# Library: printable PDFs and books
# ---------------------------------------------------------------------------
def build_library():
    import library as L
    root = ""
    pdf_html = ""
    for sid, title, sub, items in L.PDF_SECTIONS:
        cards = ""
        for name, url, by, kind, best, about in items:
            lbl = "Download PDF" if kind == "PDF" else "Go to download page"
            cards += f"""<article class="rs-card"><div class="rs-top"><span class="rs-kind rs-free">Free</span><span class="rs-kind">{e(kind)}</span><span class="rs-by">{e(by)}</span></div>
<h3><a href="{e(url)}" target="_blank" rel="noopener">{e(name)}</a></h3>
<p class="rs-best"><b>Best for:</b> {e(best)}</p><p class="rs-about">{e(about)}</p>
<a class="btn ghost sm lb-dl" href="{e(url)}" target="_blank" rel="noopener">{lbl}</a></article>"""
        pdf_html += f"""<div class="lb-sub" id="{sid}"><h3 class="lb-h">{e(title)}</h3><p class="muted">{e(sub)}</p><div class="rs-grid">{cards}</div></div>"""
    books_html = ""
    allbooks = []
    for sid, title, items in L.BOOK_SECTIONS:
        rows = ""
        for name, author, asin, price, best, why in items:
            allbooks.append((name, author))
            rows += f"""<article class="pick"><div><h3>{e(name)}</h3><p class="muted" style="margin-top:.2rem">{e(author)}</p>
<dl class="facts"><dt>Best for</dt><dd>{e(best)}</dd><dt>Why</dt><dd>{e(why)}</dd></dl></div>
<div class="buy"><span class="price">{band(price)}</span>{aff_btn(asin, "See it on Amazon")}<span class="aff">Affiliate link</span></div></article>"""
        books_html += f'<div class="lb-sub" id="{sid}"><h3 class="lb-h">{e(title)}</h3>{rows}</div>'
    tips = "".join(f"<li>{e(t)}</li>" for t in L.PRINT_TIPS)
    toc = [("free-guides", "Free printable guides")] + [(s[0], s[1]) for s in L.PDF_SECTIONS] + [("books", "Books")]
    toc_html = '<nav class="toc" aria-label="On this page"><span>On this page</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
    cr = [("Home", "/"), ("Library", "/library")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(L.H1)}</h1><p class="dek">{e(L.DEK)}</p>
<p class="muted small" style="margin-top:1rem">Links checked {REVIEWED}. The guides are free from their publishers; book links are affiliate links.</p>
{toc_html}</div></div>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<div class="pw-verdict"><h2>How to build your binder</h2><ol>{tips}</ol></div></div>
<aside class="stack-l"><div class="aside"><h3>Also print</h3><ul><li><a href="72-hour-kit.html#checklist">The PrepScore 3-day kit checklist</a></li><li><a href="guides/go-bag.html#checklist">The go-bag checklist</a></li><li><a href="city/index.html">Your city's alert sign-ups</a></li></ul></div></aside></div></section>
<section class="section" id="free-guides"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>Free printable guides</h2><p>Official and nonprofit guides, free from the people who wrote them. We link to the source, not to copies.</p></div></div>
{pdf_html}</div></section>
<section class="section" id="books"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>The best prepper and survival books</h2><p>Books for the skills and judgment that checklists can't teach. {BAND_NOTE}</p></div></div>
{DISCLOSE(root)}{books_html}</div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l read"><h2>More to read online</h2>
<p>For websites, apps and classes, see <a href="resources.html">the best prep resources beyond PrepScore</a>.</p></div><div></div></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    items = [{"@type": "ListItem", "position": i + 1, "item": {"@type": "DigitalDocument", "name": n, "url": u, "publisher": {"@type": "Organization", "name": by}}}
             for i, (n, u, by, *_rest) in enumerate(x for s in L.PDF_SECTIONS for x in s[3])]
    n0 = len(items)
    items += [{"@type": "ListItem", "position": n0 + i + 1, "item": {"@type": "Book", "name": n, "author": {"@type": "Person", "name": a}}} for i, (n, a) in enumerate(allbooks)]
    j = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": L.TITLE, "description": L.META, "url": SITE["url"] + "/library",
          "dateModified": TODAY, "publisher": {"@type": "Organization", "name": SITE["name"]},
          "mainEntity": {"@type": "ItemList", "itemListElement": items}}, crumbs_ld(cr)]
    add("library.html", shell(path="/library", title=L.TITLE, desc=L.META, body=body, root=root, og="library",
                              canon="/library", jsonld=j), "/library", "0.8")


# ---------------------------------------------------------------------------
# Black Friday
# ---------------------------------------------------------------------------
BF_UNTIL = datetime.date(2026, 12, 15)   # hide the homepage promo after this date (page itself stays up)
bf_active = lambda: datetime.date.today() <= BF_UNTIL
BF_PROMO = lambda root: f'<p class="hero-alt bf-promo">Shopping the sales? <a href="{root}black-friday.html">See the Black Friday prep gear worth buying</a>, or <a href="{root}preparedness-gifts.html">gifts people will actually use</a></p>'


def build_blackfriday():
    import blackfriday as B
    root = ""

    def card(p, num=None):
        name, asin, price, why, best, guide = p
        more = f' · <a href="guides/{guide}.html">{e(GD[guide]["short"])} guide</a>' if guide else ""
        badge = f'<span class="bf-num">{num}</span>' if num else ""
        return (f'<article class="bf-card">{badge}<h3>{e(name)}</h3><p class="bf-why">{e(why)}</p>'
                f'<p class="bf-best">Best for: {e(best)}{more}</p>'
                f'<div class="bf-buy"><div class="bf-price"><span class="bf-plabel">Price band</span><b>{band(price)}</b></div>'
                f'<div class="bf-cta">{aff_btn(asin, "See today\'s price")}<span class="aff">Affiliate link</span></div></div></article>')

    ess = "".join(card(p, i + 1) for i, p in enumerate(B.ESSENTIALS))
    big = "".join(card(p) for p in B.BIG_TICKET)
    gifts = "".join(card(p) for p in B.GIFTS)
    sale = lambda sid: f'<p class="bf-sale"><b>Sale pattern:</b> {e(B.SALE_NOTES[sid])}</p>' if sid in getattr(B, "SALE_NOTES", {}) else ""
    cats = "".join(f'<div class="bf-cat" id="{sid}"><h3 class="lb-h">{e(t)}</h3>{sale(sid)}<div class="bf-grid">{"".join(card(p) for p in items)}</div></div>' for sid, t, items in B.CATEGORIES)
    tips = "".join(f"<li><b>{e(a)}</b> {e(c)}</li>" for a, c in B.TIPS)
    dates = "".join(f'<div><dt>{e(a)}</dt><dd>{e(c)}</dd></div>' for a, c in B.DATES)
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in B.FAQS)
    toc = [("essentials", "Essentials"), ("big-ticket", "Worth waiting for"), ("gifts", "Small gifts")] + [(s[0], s[1]) for s in B.CATEGORIES] + [("faq", "Questions")]
    toc_html = '<nav class="toc" aria-label="On this page"><span>Jump to</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
    cr = [("Home", "/"), ("Black Friday", "/black-friday")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(B.H1)}</h1><p class="dek">{e(B.DEK)}</p>
<dl class="bf-dates">{dates}</dl>
{toc_html}</div></div>
<section class="section"><div class="wrap two-col"><div class="stack-l">
{DISCLOSE(root)}
<div class="pw-verdict"><h2>How to shop the sales</h2><ol>{tips}</ol></div></div>
<aside class="stack-l"><div class="aside"><h3>Not sure what you're missing?</h3><p class="muted small" style="margin-bottom:.5rem">The free quiz shows your biggest gaps in about 3 minutes, so you buy what you actually need.</p><ul><li><a href="quiz.html">Get your PrepScore</a></li><li><a href="72-hour-kit.html">The simple 3-day kit</a></li><li><a href="preparedness-gifts.html">Preparedness gift guide</a></li><li><a href="power-calculator.html">What size power station?</a></li></ul></div></aside></div></section>
<section class="section" id="essentials"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>The essentials, in order</h2><p>If you buy nothing else this season, buy these. Together they cover water, power, light, news, first aid and food for the most common emergencies.</p></div></div>
<div class="bf-grid">{ess}</div></div></section>
<section class="section" id="big-ticket"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>Big-ticket gear worth waiting for</h2><p>Expensive items where a sale saves real money. Buy these after the essentials.</p>{sale("big-ticket")}</div></div>
<div class="bf-grid">{big}</div></div></section>
<section class="section" id="gifts"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>Small prep gifts</h2><p>Inexpensive, useful gifts for the person who has everything except a plan. More ideas at every budget in the <a href="preparedness-gifts.html">preparedness gift guide</a>.</p></div></div>
<div class="bf-grid">{gifts}</div></div></section>
<section class="section"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>More picks by category</h2><p>The rest of our recommended gear, each from one of our free guides.</p></div></div>
{cats}</div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2 id="faq">Questions</h2><div class="faq">{faq_html}</div>
<p class="muted small read">{BAND_NOTE} {AMAZON_LINE}</p></div><div></div></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    allp = [p for p in B.ESSENTIALS + B.BIG_TICKET + B.GIFTS] + [p for _, _, items in B.CATEGORIES for p in items]
    j = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": B.TITLE, "description": B.META, "url": SITE["url"] + "/black-friday",
          "dateModified": TODAY, "publisher": {"@type": "Organization", "name": SITE["name"]},
          "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[0]} for i, p in enumerate(allp)]}},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in B.FAQS]},
         crumbs_ld(cr)]
    add("black-friday.html", shell(path="/black-friday", title=B.TITLE, desc=B.META, body=body, root=root, og="black-friday",
                                   canon="/black-friday", jsonld=j), "/black-friday", "0.8")


# ---------------------------------------------------------------------------
# Water storage calculator
# ---------------------------------------------------------------------------
WATER_CALC_FAQ = [
    ("How much water should I store per person?",
     "Plan on at least 1 gallon per person per day, for drinking and basic hygiene. That's the CDC and Ready.gov guideline. Store at least 3 days, and build toward two weeks if you can."),
    ("Why two weeks?",
     "After a major earthquake, hurricane or water main failure, tap water can be out or unsafe for days to weeks, and stores sell out fast. Many local emergency agencies recommend two weeks for that reason."),
    ("Do I need more in hot weather?",
     "Yes. Ready.gov notes that in very hot temperatures, water needs can double. Children, nursing mothers and people who are sick may need more too."),
    ("How much water do pets need?",
     "Store at least three days of water for each pet, separate from your own. A common rule of thumb is about an ounce of water per pound of body weight per day; ask your vet if your pet has special needs."),
    ("Does the water in my water heater count?",
     "It can. A typical tank holds 40 to 50 gallons. Shut off the cold water supply first so the tank isn't contaminated, let the water cool, and drain it from the valve at the bottom. The calculator counts 40 gallons if you tick the box."),
    ("How do I store water safely?",
     "Use food-grade containers with tight lids, or unopened commercially bottled water. Keep it somewhere cool and dark, away from chemicals. Replace water you bottled yourself every six months, and follow the date on store-bought water."),
    ("Where do I put it in a small apartment?",
     "Stackable 5-gallon containers take about two square feet of floor per 20 gallons. Spread heavy water around the apartment rather than in one spot, and use closets, under beds and behind the couch. Fill collapsible jugs or a bathtub when a storm is forecast for extra washing and flushing water."),
]


def build_water_calc():
    root = ""
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in WATER_CALC_FAQ)
    cr = [("Home", "/"), ("Water storage calculator", "/water-calculator")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>How much emergency water should you store?</h1>
<p class="dek">Enter your household and what you already have. You'll get the 3-day, 1-week and 2-week amounts, what's left to store, and how much room and weight it takes.</p></div></div>
<section class="section"><div class="wrap wc">
<form class="wc-in" onsubmit="return false" aria-label="Your household">
<div><span class="wc-l" id="wc-people-l">People in your household</span>
<div class="stepper" role="group" aria-labelledby="wc-people-l"><button type="button" id="wc-minus" aria-label="Fewer people">&minus;</button><output id="wc-people" aria-live="polite">2</output><button type="button" id="wc-plus" aria-label="More people">+</button></div></div>
<label class="wc-field"><span class="wc-l">Total weight of your pets, in pounds</span><input type="number" id="wc-petlb" inputmode="decimal" min="0" step="1" placeholder="0"><span class="wc-h">Leave blank if you have none.</span></label>
<label class="wc-check"><input type="checkbox" id="wc-hot"><span>We live somewhere very hot, or plan for summer heat <span class="wc-h">Doubles each person's water.</span></span></label>
<label class="wc-field"><span class="wc-l">Drinking water you already have, in gallons</span><input type="number" id="wc-have" inputmode="decimal" min="0" step="1" placeholder="0"><span class="wc-h">A 24-pack of half-liter bottles is about 3 gallons.</span></label>
<label class="wc-check"><input type="checkbox" id="wc-heater"><span>Count my water heater (40 gallons) <span class="wc-h">Only if you know how to drain it safely.</span></span></label>
</form>
<div class="wc-out" aria-live="polite">
<div class="wc-stats"><div><span>You need each day</span><b id="wc-daily">2 gal</b></div><div><span>Your water lasts</span><b id="wc-lasts">0 days</b></div></div>
<p class="wc-note" id="wc-lasts-note"></p>
<div class="table-wrap"><table class="wc-table"><thead><tr><th scope="col">Goal</th><th scope="col">You need</th><th scope="col">Left to store</th><th scope="col">5-gal containers</th><th scope="col">Weight</th><th scope="col">Floor space</th></tr></thead><tbody id="wc-rows"></tbody></table></div>
<p class="wc-note">In an apartment, two weeks of water for your household weighs about <b id="wc-weight">0 lb</b>. Spread it around rather than stacking it all in one spot.</p>
<p class="wc-assume"><b>How this is calculated:</b> 1 gallon per person per day (CDC and Ready.gov), doubled in very hot weather (Ready.gov). Pets at about 1 ounce per pound per day. Water weighs 8.34 pounds a gallon; stacked 5-gallon containers take roughly 2 square feet per 20 gallons. Your entries stay in your browser.</p>
</div>
</div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2>Next steps</h2>
<ul class="plain-list read"><li><a href="{root}guides/water.html">Water storage and filters guide</a>: containers that fit your space, filters and purification for when storage runs out.</li>
<li><a href="{root}guides/apartment-water-storage.html">Storing water in an apartment</a>: which containers fit and where to put them.</li>
<li><a href="{root}quiz.html">Get your PrepScore</a>: see where water ranks among your gaps and print a one-page plan.</li>
<li><a href="{root}72-hour-kit.html">The simple 3-day kit</a>: the other ten essentials.</li></ul>
<h2 id="faq" style="margin-top:2rem">Questions</h2><div class="faq">{faq_html}</div>
<h2 style="margin-top:2rem">Sources</h2><ul class="sources plain-list small">
<li><a href="https://www.ready.gov/water" target="_blank" rel="noopener">Ready.gov: Water</a></li>
<li><a href="https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html" target="_blank" rel="noopener">CDC: Creating and storing an emergency water supply</a></li>
<li><a href="https://www.caloes.ca.gov/wp-content/uploads/Preparedness/Documents/Pet-Fact-Sheet.pdf" target="_blank" rel="noopener">Cal OES: Pet preparedness fact sheet</a></li></ul>
</div><div></div></div></section>"""
    j = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "Emergency water storage calculator",
          "url": SITE["url"] + "/water-calculator", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "description": "Calculate how much emergency drinking water to store for 3 days, 1 week and 2 weeks, how much you still need, and how much space and weight it takes."},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in WATER_CALC_FAQ]},
         crumbs_ld(cr)]
    add("water-calculator.html", shell(path="/water-calculator", title="Emergency Water Storage Calculator: How Much Water to Store",
                                       desc="How much emergency water should you store? Enter your household to get 3-day, 1-week and 2-week amounts, what you still need, and the space and weight it takes.",
                                       body=body, root=root, og="water-calc", canon="/water-calculator", jsonld=j, scripts=("calc.js",)),
        "/water-calculator", "0.9")


# ---------------------------------------------------------------------------
# LA renter checklist: a free, product-link-free handout for neighborhood groups
# ---------------------------------------------------------------------------
LA_HOME = [
    ("Water", "At least 3 gallons per person to start, then build to two weeks: about 14 gallons each. A major quake can break water mains for weeks."),
    ("Food", "Two weeks of food you can eat without cooking, and a manual can opener."),
    ("By every bed", "Sturdy shoes and a flashlight or headlamp. Broken glass is the most common earthquake injury."),
    ("Emergency toilet", "A bucket, heavy trash bags and cat litter. After a quake, don't flush until you know the sewer lines are OK."),
    ("Smoke", "N95 masks for everyone, for wildfire smoke and quake dust."),
    ("Medicine and papers", "A week or more of prescriptions, spare glasses, and copies of IDs, your lease and insurance."),
    ("Power and cash", "A charged power bank for each phone, and some cash in small bills."),
    ("Go-bag", "A packed bag by the door in case you have to leave fast for a fire."),
]
LA_DRILL = [
    "At night, with the lights off, walk from your bed to the nearest stairwell using a flashlight. Count the doors. Elevators won't run after a quake or in a fire.",
    "Practice drop, cover and hold on next to your bed, desk and couch.",
    "Find your unit's water shutoff, and ask where the building's gas shutoff and wrench are. Only shut off gas if you smell it or hear hissing.",
    "Pick a meeting spot outside your building and one outside the neighborhood.",
    "Swap numbers with two neighbors, and note who might need help: older neighbors, people with disabilities, families with babies.",
]
LA_ASK = [
    "Is our building on the city's soft-story or concrete retrofit list, and is the work done? You can also look up the building's address on the LA Department of Building and Safety website.",
    "Is the water heater strapped? A falling water heater can start a fire or flood the unit.",
    "Where are the gas and water shutoffs, and who has the tools?",
    "Does every unit have working smoke alarms, and carbon monoxide alarms where there are gas appliances?",
]


def build_la_renters():
    root = ""
    la = next(c for c in CITIES if c["slug"] == "los-angeles")
    signups = la["alerts"] + ([la["zone"]] if la.get("zone") else [])
    qr = open(os.path.join(HERE, "src", "qr-la-renters.svg")).read()
    qr = re.sub(r"<\?xml[^>]*>", "", qr).replace('width="33mm" height="33mm"', 'width="100%" height="100%" role="img" aria-label="QR code for prepscore.org/la-renters"')
    box = '<span class="lr-box" aria-hidden="true"></span>'
    sign_html = "".join(f'<li>{box}<div><b><a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["label"])}</a></b> <span class="lr-url">{e(a["url"].replace("https://", "").rstrip("/"))}</span><p>{e(a["how"])}</p></div></li>' for a in signups)
    home_html = "".join(f"<li>{box}<div><b>{e(t)}.</b> {e(d)}</div></li>" for t, d in LA_HOME)
    drill_html = "".join(f"<li>{box}<div>{e(d)}</div></li>" for d in LA_DRILL)
    ask_html = "".join(f"<li>{box}<div>{e(d)}</div></li>" for d in LA_ASK)
    cr = [("Home", "/"), ("Cities", "/city/"), ("Los Angeles", "/city/los-angeles"), ("Renter checklist", "/la-renters")]
    body = f"""<div class="page-head no-print"><div class="wrap">{crumbs_html(cr, root)}
<h1>Los Angeles renter emergency checklist</h1>
<p class="dek">A free one-page checklist for LA apartment renters: the official alert sign-ups, what to keep at home, a 10-minute building drill, and what to ask your landlord.</p>
<div class="lr-actions"><button type="button" class="btn" onclick="window.print()">Print the checklist</button><a class="btn ghost" href="{root}la-renters-checklist.pdf">Download the PDF</a><a class="btn ghost" href="{root}la-renters-es.html" hreflang="es" lang="es">En español</a></div>
<p class="muted small" style="margin-top:1rem">This page has no product or affiliate links. Neighborhood councils, tenant groups, libraries and building managers are welcome to print and share it. Corrections or requests: <a href="mailto:{SITE['email']}">{SITE['email']}</a>. Checked {e(ALERTS_CHECKED)}.</p></div></div>
<section class="section"><div class="wrap">
<article class="lr" id="handout">
<header class="lr-head"><div><p class="lr-kicker">Free · No sign-up · No product links</p><h2>LA renter emergency checklist</h2>
<p>Earthquakes come without warning, fires can move in minutes, and heat waves strain the grid. Ten minutes today makes the first days much easier.</p></div>
<div class="lr-qr">{qr}<span>Scan for the full list and a free plan for your household</span></div></header>
<div class="lr-cols">
<section><h3>1. Sign up for alerts today</h3><ul class="lr-list">{sign_html}</ul>
<h3>2. Keep at home, for each person</h3><ul class="lr-list">{home_html}</ul></section>
<section><h3>3. Run a 10-minute building drill</h3><ul class="lr-list">{drill_html}</ul>
<h3>4. Ask your landlord</h3><ul class="lr-list">{ask_html}</ul>
<h3>5. Check your insurance</h3><p class="lr-p">Standard renters insurance usually doesn't cover earthquake damage. The California Earthquake Authority sells renters earthquake policies through participating insurers; ask your agent.</p>
<h3>6. Write it down</h3>
<div class="lr-line"><span>Our evacuation zone</span><i></i></div><div class="lr-line"><span>Meeting spot near home</span><i></i></div>
<div class="lr-line"><span>Out-of-area contact</span><i></i></div><div class="lr-line"><span>Neighbor's phone</span><i></i></div></section>
</div>
<footer class="lr-foot">From PrepScore, a free emergency preparedness site · prepscore.org/la-renters · {SITE['email']} · General information, not professional advice. In an emergency, follow local officials and call 911 for life-threatening situations.</footer>
</article>
</div></section>
<section class="section no-print"><div class="wrap two-col"><div class="stack-l">
<h2>Go further</h2>
<ul class="plain-list read"><li><a href="{root}quiz.html#earthquake-country,los-angeles">Get your PrepScore</a>: a free 3-minute check that gives your household a one-page plan with these LA alert links built in.</li>
<li><a href="{root}water-calculator.html">Water storage calculator</a>: exactly how much water your household needs, and the space it takes.</li>
<li><a href="{root}city/los-angeles.html">The full Los Angeles guide</a>: earthquakes, wildfire, heat and power shutoffs in more detail.</li>
<li><a href="{root}where/city-apartment.html">Prepping in a city apartment</a>: what's different when you rent and live up high.</li></ul>
<h2 style="margin-top:2rem">Sources</h2><ul class="sources plain-list small">
<li><a href="https://emergency.lacity.gov/notifyla" target="_blank" rel="noopener">City of Los Angeles Emergency Management: NotifyLA</a></li>
<li><a href="https://lacounty.gov/emergency/" target="_blank" rel="noopener">LA County: Alert LA County</a></li>
<li><a href="https://www.earthquakecountry.org/" target="_blank" rel="noopener">Earthquake Country Alliance: Seven Steps to Earthquake Safety</a></li>
<li><a href="https://www.earthquakeauthority.com/California-Earthquake-Insurance-Policies/Renters" target="_blank" rel="noopener">California Earthquake Authority: Renters policies</a></li>
<li><a href="https://www.ready.gov/kit" target="_blank" rel="noopener">Ready.gov: Build a kit</a></li></ul>
</div><div></div></div></section>"""
    j = [{"@context": "https://schema.org", "@type": "Article", "headline": "Los Angeles renter emergency checklist",
          "description": "A free printable emergency checklist for Los Angeles apartment renters.", "dateModified": TODAY,
          "author": {"@type": "Person", "name": "CC Pearce", "url": "https://ccpearce.com"},
          "publisher": {"@type": "Organization", "name": SITE["name"]}, "mainEntityOfPage": SITE["url"] + "/la-renters"},
         crumbs_ld(cr)]
    add("la-renters.html", shell(path="/la-renters", title="Los Angeles Renter Emergency Checklist (Free Printable)",
                                 desc="A free one-page emergency checklist for LA apartment renters: NotifyLA and Alert LA County sign-ups, what to keep at home, a 10-minute building drill and what to ask your landlord.",
                                 body=body, root=root, og="la-renters", canon="/la-renters", jsonld=j, body_attr=' class="print-handout"'),
        "/la-renters", "0.8")


def build_la_renters_es():
    import la_es as S
    root = ""
    qr = open(os.path.join(HERE, "src", "qr-la-renters-es.svg")).read()
    qr = re.sub(r"<\?xml[^>]*>", "", qr).replace('width="33mm" height="33mm"', 'width="100%" height="100%" role="img" aria-label="Código QR de prepscore.org/la-renters-es"')
    box = '<span class="lr-box" aria-hidden="true"></span>'
    sign_html = "".join(f'<li>{box}<div><b><a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a></b> <span class="lr-url">{e(u.replace("https://", "").rstrip("/"))}</span><p>{e(h)}</p></div></li>' for l, u, h in S.SIGNUPS)
    home_html = "".join(f"<li>{box}<div><b>{e(t)}.</b> {e(d)}</div></li>" for t, d in S.HOME)
    drill_html = "".join(f"<li>{box}<div>{e(d)}</div></li>" for d in S.DRILL)
    ask_html = "".join(f"<li>{box}<div>{e(d)}</div></li>" for d in S.ASK)
    lines = "".join(f'<div class="lr-line"><span>{e(x)}</span><i></i></div>' for x in S.LINES)
    cr = [("Inicio", "/"), ("Ciudades", "/city/"), ("Los Ángeles", "/city/los-angeles"), ("Lista para inquilinos", "/la-renters-es")]
    body = f"""<div class="page-head no-print"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(S.H1)}</h1>
<p class="dek">{e(S.DEK)}</p>
<div class="lr-actions"><button type="button" class="btn" onclick="window.print()">Imprimir la lista</button><a class="btn ghost" href="{root}la-renters-checklist-es.pdf">Descargar el PDF</a><a class="btn ghost" href="{root}la-renters.html" hreflang="en" lang="en">In English</a></div>
<p class="muted small" style="margin-top:1rem">{e(S.NOTE)} Escríbanos a <a href="mailto:{SITE['email']}">{SITE['email']}</a>. {e(S.CHECKED)}</p></div></div>
<section class="section"><div class="wrap">
<article class="lr" id="handout">
<header class="lr-head"><div><p class="lr-kicker">Gratis · Sin registro · Sin enlaces a productos</p><h2>Lista de emergencia para inquilinos de LA</h2>
<p>Los terremotos llegan sin aviso, los incendios avanzan en minutos y las olas de calor sobrecargan la red eléctrica. Diez minutos hoy facilitan mucho los primeros días.</p></div>
<div class="lr-qr">{qr}<span>Escanee para ver esta lista en línea</span></div></header>
<div class="lr-cols">
<section><h3>1. Regístrese hoy para recibir alertas</h3><ul class="lr-list">{sign_html}</ul>
<h3>2. Tenga en casa, por persona</h3><ul class="lr-list">{home_html}</ul></section>
<section><h3>3. Haga un simulacro de 10 minutos en su edificio</h3><ul class="lr-list">{drill_html}</ul>
<h3>4. Pregúntele al dueño o administrador</h3><ul class="lr-list">{ask_html}</ul>
<h3>5. Revise su seguro</h3><p class="lr-p">{e(S.INSURANCE)}</p>
<h3>6. Anótelo</h3>{lines}</section>
</div>
<footer class="lr-foot">{e(S.FOOT)}</footer>
</article>
</div></section>
<section class="section no-print"><div class="wrap two-col"><div class="stack-l">
<h2>Más recursos (en inglés)</h2>
<ul class="plain-list read"><li><a href="{root}quiz.html#earthquake-country,los-angeles" hreflang="en">PrepScore</a>: una evaluación gratuita de 3 minutos que le da a su hogar un plan de una página.</li>
<li><a href="{root}water-calculator.html" hreflang="en">Calculadora de agua</a>: cuánta agua necesita su hogar y cuánto espacio ocupa.</li>
<li><a href="{root}city/los-angeles.html" hreflang="en">Guía completa de Los Ángeles</a>: terremotos, incendios, calor y cortes de luz.</li></ul>
<h2 style="margin-top:2rem">Fuentes</h2><ul class="sources plain-list small">
<li><a href="https://emergency.lacity.gov/notifyla" target="_blank" rel="noopener">Ciudad de Los Ángeles: NotifyLA</a></li>
<li><a href="https://lacounty.gov/emergency/" target="_blank" rel="noopener">Condado de Los Ángeles: Alert LA County</a></li>
<li><a href="https://www.earthquakecountry.org/" target="_blank" rel="noopener">Earthquake Country Alliance: Siete pasos para la seguridad en terremotos</a></li>
<li><a href="https://www.earthquakeauthority.com/California-Earthquake-Insurance-Policies/Renters" target="_blank" rel="noopener">California Earthquake Authority: Pólizas para inquilinos</a></li>
<li><a href="https://www.ready.gov/es/kit" target="_blank" rel="noopener">Ready.gov en español: Prepare un kit</a></li></ul>
</div><div></div></div></section>"""
    j = [{"@context": "https://schema.org", "@type": "Article", "headline": S.H1, "inLanguage": "es",
          "description": S.META, "dateModified": TODAY,
          "author": {"@type": "Person", "name": "CC Pearce", "url": "https://ccpearce.com"},
          "publisher": {"@type": "Organization", "name": SITE["name"]}, "mainEntityOfPage": SITE["url"] + "/la-renters-es"},
         crumbs_ld(cr)]
    add("la-renters-es.html", shell(path="/la-renters-es", title=S.TITLE, desc=S.META, body=body, root=root, og="la-renters-es",
                                    canon="/la-renters-es", jsonld=j, body_attr=' class="print-handout"'), "/la-renters-es", "0.7")


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Power station size calculator (no product links on the tool itself)
# ---------------------------------------------------------------------------
def build_power_calc():
    import powercalc as PC
    root = ""

    def dev_row(d):
        did, name, hint, run, per, unit, use, qty, surge = d
        if unit in ("h", "chg"):
            use_html = (f'<label class="pc-use"><input type="number" class="pc-use-in" inputmode="decimal" min="0" max="24" step="{1 if unit == "chg" else 0.5}" value="{use:g}" '
                        f'aria-label="{e(name)}: {PC.UNIT_LABEL[unit]}"><span>{PC.UNIT_LABEL[unit]}</span></label>')
        else:
            use_html = f'<span class="pc-use pc-fixed">{PC.UNIT_LABEL[unit]}</span>'
        return (f'<li class="pc-dev{" on" if qty else ""}" data-id="{did}"><div class="pc-name"><b>{e(name)}</b><span class="wc-h">{e(hint)}</span></div>'
                f'<div class="stepper sm" role="group" aria-label="How many: {e(name)}"><button type="button" data-dir="-1" aria-label="One fewer {e(name.lower())}">&minus;</button>'
                f'<output aria-live="polite">{qty}</output><button type="button" data-dir="1" aria-label="One more {e(name.lower())}">+</button></div>{use_html}</li>')

    rows = "".join(dev_row(d) for d in PC.DEVICES)
    rows += ('<li class="pc-dev" data-id="custom"><div class="pc-name"><b>Something else</b><span class="wc-h">Watts from the label or adapter</span>'
             '<label class="pc-w"><input type="number" class="pc-w-in" inputmode="decimal" min="0" step="1" placeholder="0" aria-label="Watts for something else"><span>watts</span></label></div>'
             '<div class="stepper sm" role="group" aria-label="How many: something else"><button type="button" data-dir="-1" aria-label="One fewer">&minus;</button><output aria-live="polite">0</output>'
             '<button type="button" data-dir="1" aria-label="One more">+</button></div>'
             '<label class="pc-use"><input type="number" class="pc-use-in" inputmode="decimal" min="0" max="24" step="0.5" value="1" aria-label="Something else: hours a day"><span>hours a day</span></label></li>')
    payload = json.dumps({"devices": PC.DEVICES}, separators=(",", ":")).replace("</", "<\\/")
    table = "".join(f'<tr><th scope="row">{e(n)}</th><td>{e(h)}</td><td>{(per * use):,.0f} Wh{f" ({use:g} {PC.UNIT_LABEL[u]})" if u in ("h", "chg") else ""}</td></tr>'
                    for _, n, h, _, per, u, use, _, _ in PC.DEVICES)
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in PC.FAQ)
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in PC.SOURCES)
    cr = [("Home", "/"), ("Power station calculator", "/power-calculator")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>What size power station do you need?</h1>
<p class="dek">Pick what you want to keep running in an outage. You'll get how much energy that takes a day, the battery size to buy for one day, three days or a week, and the output it needs.</p></div></div>
<section class="section"><div class="wrap wc pc">
<form class="wc-in pc-in" onsubmit="return false" aria-label="Your devices">
<div class="pc-top"><span class="wc-l">What do you need to power?</span><button type="button" class="btn ghost sm" id="pc-reset">Clear all</button></div>
<ul class="pc-list">{rows}</ul>
</form>
<div class="wc-out pc-out" id="pc-results" aria-live="polite">
<div class="wc-stats"><div><span>Energy you use a day</span><b id="pc-daily">0 Wh</b></div><div><span>Power if all run at once</span><b id="pc-run">0 W</b></div></div>
<p class="pc-class" id="pc-class"></p>
<div class="table-wrap"><table class="wc-table pc-table"><thead><tr><th scope="col">Cover without recharging</th><th scope="col">Buy at least</th><th scope="col">Size class</th></tr></thead><tbody id="pc-rows"></tbody></table></div>
<p class="wc-note" id="pc-out"></p>
<ul class="pc-notes" id="pc-notes"></ul>
<p class="pc-next">Ready to compare models? <a href="{root}guides/power.html#step">See our power station picks</a> in the backup power guide{" "}(affiliate links are on that page, not this one).</p>
<p class="wc-assume"><b>How this is calculated:</b> each device's watts × hours a day, using typical figures you can change. Power stations deliver about 85% of their rated capacity through the AC outlets, and we add 20% so you aren't running the battery to empty. Real use varies with your devices and settings; check their labels. Your entries stay in your browser.</p>
</div>
</div>
<script type="application/json" id="pc-data">{payload}</script>
<div class="pc-sticky" id="pc-sticky"><span id="pc-sticky-txt">Add a device to start</span><a href="#pc-results">See results</a></div>
</section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2>How much power common devices use</h2>
<p class="read">Typical figures, used as the starting values above. Your own devices may use more or less.</p>
<div class="table-wrap"><table class="wc-table"><thead><tr><th scope="col">Device</th><th scope="col">Typical</th><th scope="col">A day, as set above</th></tr></thead><tbody>{table}</tbody></table></div>
<h2 id="faq" style="margin-top:2rem">Questions</h2><div class="faq">{faq_html}</div>
<h2 style="margin-top:2rem">Sources</h2><ul class="sources plain-list small">{srcs}</ul>
</div>
<aside class="stack-l"><div class="aside"><h3>Next steps</h3><ul>
<li><a href="{root}guides/power.html">Backup power guide</a>: power stations, solar and generators</li>
<li><a href="{root}guides/cpap-power-outage.html">Keeping a CPAP running in an outage</a></li>
<li><a href="{root}water-calculator.html">Water storage calculator</a></li>
<li><a href="{root}quiz.html">Get your PrepScore</a></li></ul></div></aside>
</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "Power station size calculator",
          "url": SITE["url"] + "/power-calculator", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "description": "Calculate the power station capacity and output you need to run a fridge, CPAP, router, phones and lights through a power outage."},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PC.FAQ]},
         crumbs_ld(cr)]
    add("power-calculator.html", shell(path="/power-calculator", title="Power Station Size Calculator: What Size Do You Need?",
                                       desc="What size power station do you need for an outage? Pick your fridge, CPAP, router, phones and lights to get the watt-hours, size class and output to buy.",
                                       body=body, root=root, og="power-calc", canon="/power-calculator", jsonld=j, scripts=("power.js",)),
        "/power-calculator", "0.9")


# ---------------------------------------------------------------------------
# CPAP in a power outage (buyer page under guides/)
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Food storage calculator (no product links on the tool itself)
# ---------------------------------------------------------------------------
def build_food_calc():
    import foodcalc as FC
    root = ""
    payload = json.dumps({"kcal": FC.KCAL, "pantry": FC.PANTRY}, separators=(",", ":")).replace("</", "<\\/")
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FC.FAQ)
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in FC.SOURCES)
    ptable = "".join(f'<tr><th scope="row">{e(n)}</th><td>{e(u)}</td><td>{k:,}</td></tr>' for _, n, u, k, _, _, _ in FC.PANTRY)
    stepper = lambda i, label, val: (f'<div><span class="wc-l" id="fc-{i}-l">{label}</span><div class="stepper" role="group" aria-labelledby="fc-{i}-l">'
                                     f'<button type="button" id="fc-{i}-minus" aria-label="Fewer">&minus;</button><output id="fc-{i}" aria-live="polite">{val}</output>'
                                     f'<button type="button" id="fc-{i}-plus" aria-label="More">+</button></div></div>')
    cr = [("Home", "/"), ("Food storage calculator", "/food-calculator")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>How much emergency food should you store?</h1>
<p class="dek">Enter your household. You'll get the calories you need for 3 days, 2 weeks and a month, and an example pantry list sized for you, with or without a stove.</p></div></div>
<section class="section"><div class="wrap wc">
<form class="wc-in" onsubmit="return false" aria-label="Your household">
{stepper("adults", "Adults and teens", 2)}
{stepper("kids", "Children under 12", 0)}
<label class="wc-check"><input type="checkbox" id="fc-active"><span>We do hard physical work, or plan for it <span class="wc-h">Clearing debris, walking out, staying warm in a cold house. Plans 2,500 calories per adult.</span></span></label>
<label class="wc-check"><input type="checkbox" id="fc-stove"><span>We can cook (camp stove, grill or gas range) <span class="wc-h">Adds rice, oats and pasta to the list. Never cook with a grill or camp stove indoors.</span></span></label>
<div><span class="wc-l" id="fc-goal-h">Show a pantry list for</span><div class="seg" role="group" aria-labelledby="fc-goal-h">
<button type="button" data-goal="3" aria-pressed="false">3 days</button><button type="button" data-goal="14" aria-pressed="true">2 weeks</button><button type="button" data-goal="30" aria-pressed="false">1 month</button></div></div>
</form>
<div class="wc-out fc-out" aria-live="polite">
<div class="wc-stats"><div><span>Calories a day</span><b id="fc-daily">4,000</b></div><div><span>Total for <span id="fc-goal-l">2 weeks</span></span><b id="fc-total">56,000</b></div></div>
<div class="table-wrap"><table class="wc-table fc-table"><thead><tr><th scope="col">Goal</th><th scope="col">Calories</th><th scope="col">As 3,600-calorie ration packs</th></tr></thead><tbody id="fc-rows"></tbody></table></div>
<h2 class="fc-h">An example pantry for your household</h2>
<p class="wc-note">One way to reach your total with food that keeps for months and needs no fridge. Swap in what your family actually eats; aim for the same calories.</p>
<ol class="fc-list" id="fc-list"></ol>
<p class="wc-note" id="fc-stove-note" hidden>Cooking takes water too: about 2 cups per cup of rice, more for pasta. The <a href="{root}water-calculator.html">water calculator</a> covers drinking water only, so store a little extra.</p>
<p class="pc-next">Want longer shelf life or a go-bag option? <a href="{root}guides/food.html#step">See our emergency food picks</a> in the food guide (affiliate links are on that page, not this one).</p>
<p class="wc-assume"><b>How this is calculated:</b> about 2,000 calories per adult or teen a day (2,500 if you plan for hard physical work) and 1,400 per child under 12, within the ranges in the Dietary Guidelines for Americans. The pantry list splits your total across food groups using typical label calories; brands vary, so check labels. Your entries stay in your browser.</p>
</div>
</div>
<script type="application/json" id="fc-data">{payload}</script>
</section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2>Tips for storing it</h2>
<ul class="plain-list read">
<li><b>Store what you eat.</b> Buy a few extra of your usual groceries each trip and eat from the front, putting new cans at the back.</li>
<li><b>Keep a manual can opener with it.</b> It's the most-forgotten item in emergency pantries.</li>
<li><b>Cool, dry and dark.</b> Heat shortens shelf life; a closet beats a hot garage.</li>
<li><b>Eat the fridge first.</b> In an outage, use refrigerated food first, then the freezer, and only then the pantry. A closed fridge stays safe for about 4 hours; a full freezer about 48.</li>
<li><b>Write the month on the can.</b> Check everything twice a year, when the clocks change.</li></ul>
<h2 style="margin-top:2rem">Calories in common pantry foods</h2>
<p class="read">Typical label figures, used for the list above.</p>
<div class="table-wrap"><table class="wc-table"><thead><tr><th scope="col">Food</th><th scope="col">Size</th><th scope="col">Calories</th></tr></thead><tbody>{ptable}</tbody></table></div>
<h2 id="faq" style="margin-top:2rem">Questions</h2><div class="faq">{faq_html}</div>
<h2 style="margin-top:2rem">Sources</h2><ul class="sources plain-list small">{srcs}</ul>
</div>
<aside class="stack-l"><div class="aside"><h3>Next steps</h3><ul>
<li><a href="{root}guides/food.html">Emergency food and cooking guide</a></li>
<li><a href="{root}water-calculator.html">Water storage calculator</a></li>
<li><a href="{root}power-calculator.html">Power station calculator</a></li>
<li><a href="{root}72-hour-kit.html">The simple 3-day kit</a></li>
<li><a href="{root}quiz.html">Get your PrepScore</a></li></ul></div></aside>
</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "Emergency food storage calculator",
          "url": SITE["url"] + "/food-calculator", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "description": "Calculate how many calories of emergency food your household needs for 3 days, 2 weeks or a month, with an example pantry list."},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FC.FAQ]},
         crumbs_ld(cr)]
    add("food-calculator.html", shell(path="/food-calculator", title="Emergency Food Storage Calculator: How Much Food to Store",
                                      desc="How much emergency food should you store? Enter your household to get calories for 3 days, 2 weeks and a month, plus an example pantry list sized for you.",
                                      body=body, root=root, og="food-calc", canon="/food-calculator", jsonld=j, scripts=("food.js",)),
        "/food-calculator", "0.9")


# ---------------------------------------------------------------------------
# Buyer pages under guides/ built from a content module (apartment water, stranded in winter)
# ---------------------------------------------------------------------------
def build_buyer(M):
    root = "../"
    verdict = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in M.VERDICT)

    def pick(p):
        url = buy_url(dict(p, q=p.get("q", "")))
        target = p.get("asin_name") or (p["name"] if p.get("asin") else "Amazon search results")
        note = f'<span class="link-to"><b>Our pick:</b> {e(target)}</span>' if target != p["name"] else ""
        return f"""<article class="pick" id="pick-{slugify(p['name'])}"><div><h3>{e(p['name'])}</h3><dl class="facts"><dt>What it is</dt><dd>{e(p['what'])}</dd><dt>Why</dt><dd>{e(p['why'])}</dd><dt>Watch out</dt><dd>{e(p['watch'])}</dd></dl></div>
<div class="buy"><span class="price">{band(p['price'])}</span><span class="bestfor">Best for: {e(p['best'])}</span>{note}
<a class="btn sm" href="{e(url)}" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a><span class="aff">Affiliate link</span></div></article>"""
    picks = "".join(pick(p) for p in M.PICKS)
    toc = [("short-answer", "Short answer")]
    table = ""
    if getattr(M, "TABLE_TITLE", None):  # space and weight by household size (apartment water)
        trs = ""
        for n in (1, 2, 3, 4):
            gal = 14 * n
            trs += (f'<tr><th scope="row">{n} {"person" if n == 1 else "people"}</th><td data-l="3 days">{3 * n} gal</td><td data-l="2 weeks">{gal} gal</td>'
                    f'<td data-l="Weight">{round(gal * 8.34):,} lb</td><td data-l="5-gal containers">{-(-gal // 5)}</td><td data-l="Floor space">~{max(1, round(gal * 0.1))} sq ft</td></tr>')
        table = (f'<section class="section" id="space"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>{e(M.TABLE_TITLE)}</h2><p>{e(M.TABLE_NOTE)}</p></div>'
                 f'<a href="{M.CALC_LINK[1]}">Your household in the calculator</a></div>'
                 f'<div class="table-wrap"><table class="matrix pw-table cp-table"><thead><tr><th scope="col">Household</th><th scope="col">3 days</th><th scope="col">2 weeks</th><th scope="col">Weight (2 weeks)</th><th scope="col">5-gal containers</th><th scope="col">Floor space</th></tr></thead><tbody>{trs}</tbody></table></div></div></section>')
        toc.append(("space", "Space and weight"))
    steps = ""
    if getattr(M, "STEPS", None):
        steps = (f'<section class="section" id="steps"><div class="wrap two-col"><div class="stack-l"><h2>{e(M.STEPS_TITLE)}</h2>'
                 f'<ol class="pw-steps">{"".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in M.STEPS)}</ol></div><div></div></div></section>')
        toc.append(("steps", "What to do"))
    toc.append(("picks", "What to buy"))
    sections = ""
    for title, items in getattr(M, "SECTIONS", []):
        sid = slugify(title)
        sections += (f'<h2 id="{sid}" style="margin-top:2.5rem">{e(title)}</h2><ul class="plain-list read">'
                     + "".join(f"<li><b>{e(a)}.</b> {e(b)}</li>" for a, b in items) + "</ul>")
    checklist = ""
    if getattr(M, "CHECKLIST", None):
        pfx = "ck-" + M.SLUG[:12]
        lis = "".join(f'<li><label class="qitem" for="{pfx}-{i}"><input type="checkbox" id="{pfx}-{i}" data-ck><span class="qbox">{CHECK_SVG}</span><span class="t">{e(x)}</span></label></li>' for i, x in enumerate(M.CHECKLIST))
        checklist = (f'<section class="section printable" id="checklist"><div class="wrap"><div class="section-head"><div><h2>{e(M.CHECKLIST_TITLE)}</h2>'
                     f'<p>{e(M.CHECKLIST_NOTE)} <a href="{getattr(M, "CHECKLIST_LINK", ("", ""))[1] or M.PARENT + ".html"}">{e(getattr(M, "CHECKLIST_LINK", ("", ""))[0] or GD[M.PARENT]["short"] + " guide")}</a>.</p></div>'
                     f'<div class="ck-tools"><span class="muted" id="ck-count"></span><button type="button" class="btn ghost sm" data-print>Print checklist</button></div></div>'
                     f'<ul class="check-grid">{lis}</ul></div></section>')
        toc.append(("checklist", "Checklist"))
    toc += [("faq", "Questions"), ("sources", "Sources")]
    toc_html = '<nav class="toc" aria-label="On this page"><span>On this page</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in M.FAQS)
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in M.SOURCES)
    related = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in M.RELATED)
    parent = GD[M.PARENT]
    cr = [("Home", "/"), ("Gear guides", "/guides/"), (parent["name"], f"/guides/{M.PARENT}"), (M.CRUMB, f"/guides/{M.SLUG}")]
    calc = f'<p class="read">{e(M.CALC_LINK[0])} <a href="{M.CALC_LINK[1]}">{e(M.CALC_LINK[2])}</a>.</p>' if getattr(M, "CALC_LINK", None) else ""
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(M.H1)}</h1><p class="dek">{e(M.DEK)}</p>
<p class="muted small" style="margin-top:1rem">Reviewed {REVIEWED} against {e(M.REVIEWED)}. Picks are researched from published specs and safety guidance, not hands-on tested by PrepScore. <a href="{root}disclosure.html">How we pick</a>. {BAND_NOTE}</p>
{toc_html}</div></div>
<section class="section"><div class="wrap stack-l">
<div class="pw-verdict" id="short-answer"><h2>The short answer</h2><ol>{verdict}</ol></div>
{calc}
</div></section>
{table}{steps}
<section class="section" id="picks" style="padding-top:2rem"><div class="wrap">{DISCLOSE(root)}
<h2 style="margin-top:2rem">What to buy</h2>{picks}</div></section>
{checklist}
<section class="section"><div class="wrap two-col"><div class="stack-l">
{sections}
<h2 id="faq" style="margin-top:2.5rem">Questions</h2><div class="faq">{faq_html}</div>
<h2 id="sources" style="margin-top:2.5rem">Sources</h2><ul class="plain-list read sources">{srcs}</ul>
<p class="muted small read">General information, not medical or safety advice for your situation. In an emergency, call 911 and follow instructions from local officials.</p></div>
<aside class="stack-l"><div class="aside"><h3>Related</h3><ul>{related}</ul></div></aside>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    howto = [{"@context": "https://schema.org", "@type": "HowTo", "name": M.H1, "step": [{"@type": "HowToStep", "name": a, "text": b} for a, b in M.STEPS]}] if getattr(M, "STEPS", None) else []
    j = [{"@context": "https://schema.org", "@type": "Article", "headline": M.TITLE, "description": M.META, "dateModified": TODAY,
          "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/about"},
          "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + f"/og/{M.OG}.png",
          "mainEntityOfPage": SITE["url"] + f"/guides/{M.SLUG}",
          "citation": [{"@type": "CreativeWork", "name": t, "url": u} for t, u in M.SOURCES]},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in M.FAQS]}] + howto + [crumbs_ld(cr)]
    add(f"guides/{M.SLUG}.html", shell(path=f"/guides/{M.SLUG}", title=M.TITLE, desc=M.META, body=body, root=root, og=M.OG,
                                       canon=f"/guides/{M.SLUG}", jsonld=j, active="guides", scripts=("site.js",) if getattr(M, "CHECKLIST", None) else ()),
        f"/guides/{M.SLUG}", "0.8")


def build_cpap():
    import cpap as C
    root = "../"
    verdict = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in C.VERDICT)

    def nights(lo_wh, hi_wh, station):
        usable = station * 0.85
        lo, hi = usable / hi_wh, usable / lo_wh
        if hi < 1:
            return "Less than 1"
        a, b = int(lo), int(hi)
        if lo < 1:
            return "About 1"
        return f"About {a}" if a == b else f"{a} to {b}"

    head = "".join(f'<th scope="col">{s:,} Wh station</th>' for s in C.STATIONS)
    trs = "".join(f'<tr><th scope="row">{e(n)}<span class="pw-kind">{lo} to {hi} Wh a night</span></th>'
                  + "".join(f'<td data-l="{s:,} Wh">{nights(lo, hi, s)}</td>' for s in C.STATIONS) + "</tr>" for n, lo, hi in C.SETTINGS)

    def pick(p):
        url = buy_url(dict(p, q=p.get("q", "")))
        target = p.get("asin_name") or "Amazon search results"
        return f"""<article class="pick"><div><h3>{e(p['name'])}</h3><dl class="facts"><dt>What it is</dt><dd>{e(p['what'])}</dd><dt>Why</dt><dd>{e(p['why'])}</dd><dt>Watch out</dt><dd>{e(p['watch'])}</dd></dl></div>
<div class="buy"><span class="price">{band(p['price'])}</span><span class="bestfor">Best for: {e(p['best'])}</span><span class="link-to"><b>Our pick:</b> {e(target)}</span>
<a class="btn sm" href="{e(url)}" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a><span class="aff">Affiliate link</span></div></article>"""
    picks = "".join(pick(p) for p in C.PICKS)
    steps = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in C.SETUP)
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in C.FAQS)
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in C.SOURCES)
    toc = [("short-answer", "Short answer"), ("runtime", "Runtime table"), ("picks", "What to buy"), ("setup", "Set it up"), ("faq", "Questions"), ("sources", "Sources")]
    toc_html = '<nav class="toc" aria-label="On this page"><span>On this page</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
    cr = [("Home", "/"), ("Gear guides", "/guides/"), ("Power", "/guides/power"), ("CPAP in an outage", "/guides/cpap-power-outage")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(C.H1)}</h1><p class="dek">{e(C.DEK)}</p>
<p class="muted small" style="margin-top:1rem">Reviewed {REVIEWED} against ResMed's published battery figures and FDA and ASPR guidance. Picks are researched from published specs, not hands-on tested by PrepScore. <a href="{root}disclosure.html">How we pick</a>. {BAND_NOTE}</p>
{toc_html}</div></div>
<section class="section"><div class="wrap stack-l">
<div class="pw-verdict" id="short-answer"><h2>The short answer</h2><ol>{verdict}</ol></div>
</div></section>
<section class="section" id="runtime"><div class="wrap stack-l">
<div class="section-head" style="margin:0"><div><h2>How many nights you'll get</h2><p>Nights per full charge, by machine setting and station size. Based on about 85% of a station's rated capacity being usable.</p></div><a href="{root}power-calculator.html">Add other devices in the calculator</a></div>
<div class="table-wrap"><table class="matrix pw-table cp-table"><thead><tr><th scope="col">Your CPAP setting</th>{head}</tr></thead><tbody>{trs}</tbody></table></div>
<p class="muted small read">Nightly use is from ResMed's battery guide for the AirSense 10 at 8 to 10 cmH2O over 8 hours, measured at 12 V DC (current × 12 V × 8 hours, without the guide's 50% safety margin). Higher pressures, longer nights, the AirSense 11 and other brands will differ. The best number is your own: run the CPAP from the station for one night and check the battery level in the morning.</p>
</div></section>
<section class="section" id="picks" style="padding-top:2rem"><div class="wrap">{DISCLOSE(root)}
<h2 style="margin-top:2rem">What to buy</h2>{picks}
<article class="pick"><div><h3>DC power cord or converter for your CPAP</h3><p class="read" style="margin-top:.6rem">{e(C.DC_NOTE)}</p></div>
<div class="buy"><span class="price">Varies</span><span class="bestfor">Best for: Anyone running a CPAP from a battery</span><span class="aff">No link: buy from your CPAP maker or supplier</span></div></article>
</div></section>
<section class="section"><div class="wrap two-col"><div class="stack-l">
<h2 id="setup">Set it up before the outage</h2>
<ol class="pw-steps">{steps}</ol>
<h2 id="faq" style="margin-top:2.5rem">Questions</h2><div class="faq">{faq_html}</div>
<h2 id="sources" style="margin-top:2.5rem">Sources</h2><ul class="plain-list read sources">{srcs}</ul>
<p class="muted small read">This page is general information, not medical advice. If you rely on a powered medical device, ask your doctor and equipment supplier what to do in an outage.</p></div>
<aside class="stack-l"><div class="aside"><h3>Related</h3><ul><li><a href="{root}power-calculator.html">Power station size calculator</a></li><li><a href="power.html">Backup power guide</a></li><li><a href="first-aid.html">First aid, medications and insulin in an outage</a></li><li><a href="light-heat.html">Staying warm without power</a></li></ul></div></aside>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "Article", "headline": C.TITLE, "description": C.META, "dateModified": TODAY,
          "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/about"},
          "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + "/og/guide-cpap.png",
          "mainEntityOfPage": SITE["url"] + "/guides/cpap-power-outage",
          "citation": [{"@type": "CreativeWork", "name": t, "url": u} for t, u in C.SOURCES]},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in C.FAQS]},
         crumbs_ld(cr)]
    add("guides/cpap-power-outage.html", shell(path="/guides/cpap-power-outage", title=C.TITLE, desc=C.META, body=body, root=root, og="guide-cpap",
                                               canon="/guides/cpap-power-outage", jsonld=j, active="guides"), "/guides/cpap-power-outage", "0.8")


# ---------------------------------------------------------------------------
# Preparedness gift guide
# ---------------------------------------------------------------------------
def build_gifts():
    import gifts as G
    root = ""
    by_id = {g[0]: g for g in G.GIFTS}

    def level(price):
        nums = [float(x.replace(",", "")) for x in re.findall(r"\$\s?([\d,]+(?:\.\d+)?)", price)]
        v = (nums[0] + nums[1]) / 2 if len(nums) > 1 else nums[0]
        return 4 if v >= 300 else 3 if v >= 100 else 2 if v >= 25 else 1

    def card(g):
        gid, name, asin, price, why, who, guide = g
        more = f' · <a href="guides/{guide}.html">{e(GD[guide]["short"])} guide</a>' if guide else ""
        return (f'<article class="bf-card" id="gift-{gid}"><h3>{e(name)}</h3><p class="bf-why">{e(why)}</p>'
                f'<p class="bf-best">Good for: {e(who)}{more}</p>'
                f'<div class="bf-buy"><div class="bf-price"><span class="bf-plabel">Price band</span><b>{band(price)}</b></div>'
                f'<div class="bf-cta">{aff_btn(asin, "See today's price")}<span class="aff">Affiliate link</span></div></div></article>')

    tiers = [(1, "under-25", "Under $25", "Stocking stuffers and small thank-yous."),
             (2, "25-100", "$25 to $100", "The sweet spot: everyday gear that's ready for an emergency."),
             (3, "100-300", "$100 to $300", "Bigger gifts that people rarely buy for themselves."),
             (4, "over-300", "Over $300", "For someone who gets long outages, uses a CPAP or heads into the backcountry.")]
    sections = ""
    for n, sid, title, sub in tiers:
        items = [g for g in G.GIFTS if level(g[3]) == n]
        if items:
            sections += (f'<section class="section" id="{sid}"><div class="wrap stack-l"><div class="section-head" style="margin:0"><div><h2>{e(title)}</h2><p>{e(sub)}</p></div></div>'
                         f'<div class="bf-grid">{"".join(card(g) for g in items)}</div></div></section>')
    people = "".join(f'<div><dt>{e(t)}</dt><dd>' + ", ".join(f'<a href="#gift-{i}">{e(by_id[i][1].split(" (")[0])}</a>' for i in ids) + "</dd></div>" for t, ids in G.PEOPLE)
    free = "".join(f"<li>{e(x)}</li>" for x in G.FREE_GIFT)
    skip = "".join(f"<li><b>{e(a)}.</b> {e(b)}</li>" for a, b in G.SKIP)
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in G.FAQS)
    toc = [(t[1], t[2]) for t in tiers] + [("free", "The free gift"), ("skip", "What to skip"), ("faq", "Questions")]
    toc_html = '<nav class="toc" aria-label="On this page"><span>Jump to</span>' + "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</nav>"
    cr = [("Home", "/"), ("Preparedness gifts", "/preparedness-gifts")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(G.H1)}</h1><p class="dek">{e(G.DEK)}</p>
<p class="muted small" style="margin-top:1rem">Updated {REVIEWED}. Every gift here is also a pick in one of our guides, researched from published specs and safety guidance, not hands-on tested by PrepScore. {BAND_NOTE}</p>
{toc_html}</div></div>
<section class="section"><div class="wrap two-col"><div class="stack-l">
{DISCLOSE(root)}
<div class="pw-verdict"><h2>Gifts by person</h2><dl class="gift-people">{people}</dl></div></div>
<aside class="stack-l"><div class="aside"><h3>Shopping the sales?</h3><p class="muted small" style="margin-bottom:.5rem">See which prep gear usually goes on sale, and the essentials to buy first.</p><ul><li><a href="black-friday.html">Black Friday prep picks</a></li><li><a href="power-calculator.html">Power station size calculator</a></li></ul></div></aside></div></section>
{sections}
<section class="section" id="free"><div class="wrap two-col"><div class="stack-l">
<h2>The best gift is free: 20 minutes together</h2>
<p class="read">Gear helps, but a plan matters more. Spend part of a visit doing these with someone you love:</p>
<ul class="plain-list read">{free}</ul>
<p class="read"><a href="quiz.html">Take the PrepScore quiz</a> · <a href="city/index.html">Find their city's alert sign-ups</a></p>
<h2 id="skip" style="margin-top:2.5rem">What to skip</h2>
<ul class="plain-list read">{skip}</ul>
<h2 id="faq" style="margin-top:2.5rem">Questions</h2><div class="faq">{faq_html}</div>
<p class="muted small read">{AMAZON_LINE} Prices change often, especially around the holidays, so check the retailer for today's price.</p>
</div><div></div></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    j = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": G.TITLE, "description": G.META, "url": SITE["url"] + "/preparedness-gifts",
          "dateModified": TODAY, "publisher": {"@type": "Organization", "name": SITE["name"]},
          "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": g[1]} for i, g in enumerate(G.GIFTS)]}},
         {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in G.FAQS]},
         crumbs_ld(cr)]
    add("preparedness-gifts.html", shell(path="/preparedness-gifts", title=G.TITLE, desc=G.META, body=body, root=root, og="gifts",
                                         canon="/preparedness-gifts", jsonld=j), "/preparedness-gifts", "0.8")


def build_scenarios():
    root = ""
    chips = "".join(f'<button type="button" class="chip" data-scn="{s["id"]}" aria-pressed="{"true" if i == 0 else "false"}">{e(s["name"])}</button>' for i, s in enumerate(SCENARIOS))
    panels = ""
    for i, s in enumerate(SCENARIOS):
        cols = ""
        for lv in (3, 2, 1):
            items = [m for m in MATRIX if m["lv"][s["id"]] == lv]
            lis = "".join(f'<li><b>{e(m["name"])}</b><span>{e(m["why"])}</span><a href="guides/{m["guide"]}.html">{e(GD[m["guide"]]["short"])}</a></li>' for m in items) or '<li><span>Nothing in this group.</span></li>'
            cols += f"<div><h3>{dots(lv)} {LVL[lv]}</h3><ul>{lis}</ul></div>"
        panels += f'<div class="scn-panel" data-panel="{s["id"]}"{"" if i == 0 else " hidden"}><p class="dek" style="margin:0 0 1.5rem"><b>{e(s["name"])}, {e(s["span"])}.</b> {e(s["desc"])}</p><div class="ranked">{cols}</div></div>'
    cr = [("Home", "/"), ("Emergencies", "/scenarios")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>What matters in which emergency</h1><p class="dek">Prep isn't one list. Pick an emergency to see what's critical, what helps and what can wait.</p></div></div>
<section class="section"><div class="wrap stack-l">
<div class="chips" role="group" aria-label="Choose an emergency">{chips}</div>
{panels}
</div></section>
<section class="section"><div class="wrap stack-l">
<h2>The full matrix</h2><p class="muted read">Every item against every emergency. Scroll sideways on a phone.</p>
{matrix_table(MATRIX, highlight=SCENARIOS[0]['id'], caption='Importance of each item by emergency')}
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    add("scenarios.html", shell(path="/scenarios", title="Emergency Preparedness by Scenario: What Matters Most",
                                desc="Which emergency supplies matter for power outages, earthquakes, evacuations, unsafe water, sheltering in place and long grid-down events.",
                                body=body, root=root, og="scenarios", canon="/scenarios", jsonld=[crumbs_ld(cr)], active="scenarios",
                                scripts=("site.js",)), "/scenarios", "0.8")


def build_misc():
    root = ""
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html([("Home", "/"), ("How we make money", "/disclosure")], root)}
<h1>How we pick gear and make money</h1><p class="dek">Short version: affiliate commissions, clearly labeled, and they don't decide what we recommend.</p></div></div>
<section class="section"><div class="wrap stack read">
<h2>How we make money</h2>
<p>Some links on {SITE['name']} are affiliate links. They're labeled <b>Affiliate</b> next to the button. If you buy through one, the retailer pays us a commission. Your price is the same.</p>
<p>{AMAZON_LINE}</p>
<p>We don't accept paid placements, sponsored rankings or free products in exchange for coverage. Questions about how we make money? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
<h2 style="margin-top:2rem">How we pick</h2>
<p>We start from what you need in a real emergency, then look for gear that does that job reliably at three budgets. We favor items with long track records, independent certifications where they exist (NIOSH for respirators, NSF/ANSI or EPA registration for water treatment), and makers who publish real specs.</p>
<p>We don't run a test lab. Picks are researched from published specifications, certifications, safety guidance and long-term owner feedback, not hands-on tested by PrepScore, and we say so on every guide. Each pick also says who can skip it, because the best purchase is often none.</p>
<p>Whenever a free or cheap option works, like a Stop the Bleed class or a bathtub full of water, we say so first.</p>
<h2 style="margin-top:2rem">Your quiz answers</h2>
<p>The PrepScore quiz runs entirely in your browser. Your answers are saved on your device so you can come back to them. We don't send them anywhere. See our <a href="{root}privacy.html">privacy policy</a>.</p>
<h2 style="margin-top:2rem">Not professional advice</h2>
<p>This site is general information. It isn't medical, legal or safety-engineering advice. Follow the instructions of local officials during an emergency, and follow every product's safety labels, especially for generators, heaters and stoves.</p>
</div></section>"""
    add("disclosure.html", shell(path="/disclosure", title="Affiliate Disclosure and How We Pick Gear", desc=f"How {SITE['name']} makes money, how we choose gear, and how we handle your quiz answers.",
                                 body=body, root=root, og="default", canon="/disclosure"), "/disclosure", "0.3")

    # Privacy policy
    analytics_on = bool(SITE.get("cf_beacon") or SITE.get("cf_analytics_auto"))
    analytics_html = ("""<h2 style="margin-top:2rem">Analytics</h2>
<p>We use <a href="https://www.cloudflare.com/web-analytics/" target="_blank" rel="noopener">Cloudflare Web Analytics</a> to count visits. It doesn't use cookies, doesn't fingerprint your device and doesn't track you across sites. We see totals: which pages were viewed, where visitors came from (the referring site), country, browser and device type, and how fast pages loaded. We can't see who you are.</p>"""
        if analytics_on else
        """<h2 style="margin-top:2rem">Analytics</h2>
<p>We don't run analytics or tracking scripts. If we add analytics, we'll use a cookieless, privacy-focused tool and update this page first.</p>""")
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html([("Home", "/"), ("Privacy", "/privacy")], root)}
<h1>Privacy policy</h1><p class="dek">Short version: no accounts, no forms, no ads, no cookies of our own. Your quiz answers never leave your device.</p>
<p class="muted small" style="margin-top:1rem">Last updated {PRIVACY_UPDATED}</p></div></div>
<section class="section"><div class="wrap stack read">
<h2>What we collect</h2>
<p>Very little. {SITE['name']} has no sign-up, no email list, no comment forms and no ads. We don't ask for your name, email or address, and we don't set cookies of our own.</p>
<h2 style="margin-top:2rem">Your quiz answers stay on your device</h2>
<p>The PrepScore quiz runs entirely in your browser. Your answers, household size and location type are saved in your browser's local storage so they're there when you come back. They're never sent to us or anyone else. Use <b>Clear my answers</b> on the quiz, or clear your browser's site data, to delete them.</p>
<p>The share card is drawn in your browser too. Nothing is shared unless you choose a share button, and then only your score, tier and days of supplies go to the service you picked (X, Facebook, Reddit or WhatsApp), under that service's privacy policy.</p>
{analytics_html}
<h2 style="margin-top:2rem">Counting clicks and tool use</h2>
<p>When you click a link to a retailer such as Amazon, the site records which page you were on, which product and which button, with the date. It also counts, by page and date, when someone uses the quiz or a calculator, prints a page, uses a share button, or follows a link to one of our calculators. It doesn't record your answers, your IP address, your browser or anything that identifies you, and it uses no cookies. We use the totals to learn which guides and tools are useful.</p>
<h2 style="margin-top:2rem">Hosting and fonts</h2>
<p>The site is hosted by Cloudflare. Like any web host, Cloudflare processes basic request data, such as your IP address and browser, to deliver pages and protect the site from attacks, under <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">Cloudflare's privacy policy</a>.</p>
<p>Our fonts load from Google Fonts, so Google receives your IP address and browser details when a page loads, under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's privacy policy</a>.</p>
<h2 style="margin-top:2rem">Affiliate links</h2>
<p>Links marked <b>Affiliate</b> go to retailers such as Amazon. When you click one, the retailer may set cookies on its own site to credit us for the referral. Their privacy policies apply once you're there. We never learn who you are or what you bought; retailers only report total sales and commissions to us. More on how we make money is on our <a href="{root}disclosure.html">disclosure page</a>.</p>
<h2 style="margin-top:2rem">Links to other sites</h2>
<p>We link to government agencies, nonprofits and other sites we trust. We're not responsible for their privacy practices, so check their policies too.</p>
<h2 style="margin-top:2rem">Children</h2>
<p>{SITE['name']} is for a general audience and isn't directed at children under 13. We don't knowingly collect information from children.</p>
<h2 style="margin-top:2rem">Your choices and rights</h2>
<p>Because we don't keep personal information tied to you, there's nothing for us to look up, correct or delete. We don't sell or share personal information. You can block cookies in your browser, clear your quiz answers at any time, and use a content blocker if you prefer.</p>
<h2 style="margin-top:2rem">Changes and contact</h2>
<p>If we change how the site handles data, we'll update this page and the date at the top before the change takes effect. Questions? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>, or reach {SITE['name']}'s creator, CC Pearce, on X at <a href="https://x.com/cc5alive" target="_blank" rel="noopener">@cc5alive</a>.</p>
</div></section>"""
    add("privacy.html", shell(path="/privacy", title="Privacy Policy", desc=f"How {SITE['name']} handles your data: no accounts, no cookies of our own, and quiz answers that never leave your device.",
                              body=body, root=root, og="default", canon="/privacy"), "/privacy", "0.3")
    # About and editorial standards
    allsrc = {}
    for lst in SOURCES.values():
        for t, u in lst:
            allsrc[t.split(":")[0]] = allsrc.get(t.split(":")[0]) or u
    agencies = ", ".join(sorted(allsrc))
    cr = [("Home", "/"), ("About", "/about")]
    body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>About PrepScore</h1><p class="dek">Practical emergency preparedness for ordinary households: what actually matters where you live, in the order you should do it.</p></div></div>
<section class="section"><div class="wrap stack read">
<h2>Who's behind it</h2>
<p>PrepScore was started by CC Pearce, a writer and entrepreneur based in Los Angeles.</p>
<p>I'm new to prepping myself. But the time has never felt more uncertain, and I want good, practical resources to be available to everyone, for free. So I built the site I wished existed when I started: begin with what actually matters, check it against official sources, and be upfront about how the site makes money.</p>
<p>Email me at <a href="mailto:{SITE['email']}">{SITE['email']}</a> with questions, corrections or ideas. You can also find me on X at <a href="https://x.com/cc5alive" rel="me noopener" target="_blank">@cc5alive</a> and at <a href="https://ccpearce.com" rel="me noopener" target="_blank">ccpearce.com</a>.</p>
<h2 style="margin-top:2rem">What the site does</h2>
<p>{SITE['name']} is an independent site. We built it because most prep advice is either a 300-item shopping list or a doomsday fantasy. We'd rather help you get the first two weeks right: water, power, light, first aid, a way to get alerts, and a plan to leave.</p>
<p>The free quiz shows where you stand. The location and city guides show what tends to fail where you live. The gear guides show what to buy, how much you need and what to skip.</p>
<h2 style="margin-top:2rem">Where our guidance comes from</h2>
<p>Safety guidance on this site follows official public-health and emergency-management sources, including {e(agencies)}. Every gear guide lists the specific sources it was checked against. City guides link only to official city, county and state alert systems and evacuation-zone tools. For other sites we trust, see <a href="{root}resources.html">our list of the best prep resources</a>.</p>
<p>When official guidance and common prepper advice disagree, we go with the official guidance. Examples: storing two weeks of water rather than three days in earthquake country, never running a generator in a garage, and not taping windows before a hurricane.</p>
<h2 style="margin-top:2rem">How we review</h2>
<ul class="plain-list">
<li>Each guide shows the month it was last reviewed. We re-check guides at least once a year and after major changes in official guidance.</li>
<li>City alert links are re-checked at least yearly, because cities change their notification systems.</li>
<li>Next to retailer links we show a price band ($ to $$$$), not a price. Bands are a rough guide; check the retailer for today's price.</li>
<li>When we find a mistake, we fix it and update the review date. Spotted one? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</li>
</ul>
<h2 style="margin-top:2rem">How we make money</h2>
<p>We earn commissions from affiliate links, which are always labeled. They never decide what we recommend, and we point to free options first when they exist. {AMAZON_LINE} <a href="{root}disclosure.html">Full disclosure</a>.</p>
<h2 style="margin-top:2rem">Not professional advice</h2>
<p>This site is general information, not medical, legal or engineering advice. In an emergency, follow instructions from local officials and call 911 when lives are at risk.</p>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    founder = {"@type": "Person", "name": "CC Pearce", "url": "https://ccpearce.com", "email": "mailto:" + SITE["email"],
               "sameAs": ["https://x.com/cc5alive", "https://ccpearce.com"]}
    j = [{"@context": "https://schema.org", "@type": "AboutPage", "name": "About PrepScore", "url": SITE["url"] + "/about",
          "dateModified": TODAY, "mainEntity": founder,
          "about": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/", "founder": founder}}, crumbs_ld(cr)]
    add("about.html", shell(path="/about", title="About PrepScore and Our Editorial Standards", desc="PrepScore was started by CC Pearce to make practical emergency preparedness free for everyone. Where our guidance comes from, how we review it and how we make money.",
                            body=body, root=root, og="default", canon="/about", jsonld=j), "/about", "0.4")

    body = f"""<div class="page-head"><div class="wrap"><h1>Nothing here</h1><p class="dek">This page moved or never existed. Try one of these instead.</p>
<p style="margin-top:1.5rem"><a class="btn" href="/quiz">Get your PrepScore</a></p></div></div>
<section class="section"><div class="wrap two-col"><div class="stack">{city_picker("/")}</div>
<div class="aside"><h3>Gear guides</h3><ul>{''.join(f'<li><a href="/guides/{g["slug"]}">{e(g["short"])}</a></li>' for g in GUIDES)}</ul></div></div></section>"""
    PAGES.append(("404.html", shell(path="/404", title="Page not found", desc="Page not found.", body=body, root="/", og="default", canon="/404", noindex=True, scripts=("site.js",)), None, None))


# ---------------------------------------------------------------------------
# OG images
# ---------------------------------------------------------------------------
def build_og():
    from PIL import Image, ImageDraw, ImageFont
    F = os.path.join(HERE, "fonts")
    st = lambda s: ImageFont.truetype(f"{F}/fontsource-big-shoulders-stencil-display-5.3.0/files/big-shoulders-stencil-display-latin-900-normal.woff", s)
    dp = lambda s: ImageFont.truetype(f"{F}/fontsource-big-shoulders-display-5.3.0/files/big-shoulders-display-latin-800-normal.woff", s)
    bd = lambda s, w=600: ImageFont.truetype(f"{F}/fontsource-public-sans-5.3.0/files/public-sans-latin-{w}-normal.woff", s)
    INK, PAPER, SURF, MUTED, SIG = "#142019", "#ECEFE8", "#F7F8F3", "#55625A", "#F2B705"
    od = os.path.join(OUT, "og"); os.makedirs(od, exist_ok=True)

    def fit(draw, text, maker, size, maxw):
        while size > 30 and draw.textlength(text, font=maker(size)) > maxw:
            size -= 4
        return maker(size)

    def wrap(draw, text, font, maxw):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        return lines

    def card(name, kicker, big, sub, color=None, bigfont="stencil"):
        W, H = 1200, 630
        im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
        d.rectangle([48, 48, W - 36, H - 36], fill=INK)
        d.rectangle([36, 36, W - 48, H - 48], fill=SURF, outline=INK, width=5)
        d.line([36, 106, W - 48, 106], fill=INK, width=5)
        d.text((64, 71), f"{SITE['name'].upper()}  ·  {kicker.upper()}", font=bd(24, 700), fill=INK, anchor="lm")
        d.text((W - 76, 71), HOST, font=bd(22, 600), fill=MUTED, anchor="rm")
        x = 64
        if color:
            d.rectangle([64, 150, 84, 360], fill=color); x = 108
        maker = st if bigfont == "stencil" else dp
        lines = [big] if len(big) < 18 else wrap(d, big, maker(110), W - x - 90)
        size = 170 if len(lines) == 1 else 108
        y = 140
        for ln in lines[:3]:
            f = fit(d, ln, maker, size, W - x - 90)
            d.text((x, y), ln, font=f, fill=INK)
            y += int(f.size * 0.95)
        sf = bd(32, 500)
        y = max(y + 24, 400)
        for ln in wrap(d, sub, sf, W - 180)[:2]:
            d.text((66, y), ln, font=sf, fill=MUTED); y += 44
        # hazard band
        band = Image.new("RGB", (W - 84, 14), INK); bdraw = ImageDraw.Draw(band)
        for s in range(-40, W, 28):
            bdraw.polygon([(s, 14), (s + 14, 14), (s + 26, 0), (s + 12, 0)], fill=SIG)
        im.paste(band, (36, H - 62))
        im.save(os.path.join(od, name + ".png"), optimize=True)

    card("default", "Emergency preparedness", "How many days could you last?", "Free 3-minute preparedness score, location guides and honest gear guides.")
    card("la-renters-es", "Gratis para imprimir", "Lista para inquilinos de LA", "Alertas oficiales, qué tener en casa, un simulacro de 10 minutos y qué preguntarle al dueño.", bigfont="display")
    card("la-renters", "Free printable", "LA renter checklist", "Alert sign-ups, what to keep at home, a 10-minute building drill and what to ask your landlord.", bigfont="display")
    card("power-calc", "Free calculator", "What size power station?", "Pick your fridge, CPAP, router, phones and lights. Get the battery size and output to buy.", bigfont="display")
    card("food-calc", "Free calculator", "How much food to store", "Enter your household: calories for 3 days, 2 weeks and a month, and a pantry list sized for you.", bigfont="display")
    import aptwater, wintercar, winterstorm
    for M in (aptwater, wintercar, winterstorm):
        card(M.OG, M.OG_CARD[0], M.OG_CARD[1], M.OG_CARD[2], bigfont="display")
    card("guide-cpap", "Backup power", "CPAP in a power outage", "Nights per charge by setting and station size, what to buy, and how to set it up first.", bigfont="display")
    card("gifts", "Gift guide 2026", "Prep gifts people use", "Headlamps, power banks, weather radios, car kits and more, by price band. Plus what to skip.", bigfont="display")
    card("water-calc", "Free calculator", "How much water to store", "Enter your household: 3-day, 1-week and 2-week amounts, what you still need, and the space it takes.", bigfont="display")
    card("kit", "The simple 3-day kit", "Your 72-hour kit", "Eleven essentials, one afternoon. How much you need and what to buy for each.")
    card("quiz", "How prepared am I?", "Get your PrepScore", "Check off what you have. See how long you'd last, your top gaps, and a card to share.")
    card("scenarios", "Emergencies", "What matters when", "Outages, earthquakes, evacuations, bad water, sheltering in place and long grid-down events.", bigfont="display")
    for t in TIERS:
        card(f"tier-{t['slug']}", f"Tier {t['min']}–{t['max']}", t["name"], t["brag"] + " How long would you last?", color=t["color"])
    for l in LOCATIONS:
        card(f"loc-{l['slug']}", "Where you live", l["h1"], l["dek"], bigfont="display")
    for g in GUIDES:
        card(f"guide-{g['slug']}", "Buyer's guide", g["name"], g["dek"])
    card("black-friday", "Black Friday 2026", "Prep gear worth buying", "The essentials to get first, big-ticket items worth waiting for, and how to spot a real deal.", bigfont="display")
    card("library", "The prepper's library", "Print it before you need it", "Free survival guides from FEMA, the CDC, the Army and Hesperian, plus the best prepper books.", bigfont="display")
    card("resources", "Beyond PrepScore", "The best prep resources", "Ready.gov, Wirecutter, Watch Duty, Stop the Bleed and more, with what each one is best for.", bigfont="display")
    card("guide-pool-water", "Water deep dive", "Drinking pool water", "Chlorine and saltwater pools: why a filter isn't enough, and what makes it drinkable.", bigfont="display")
    for c in CITIES:
        card(f"city-{c['slug']}", f"City guide  ·  {c['state']}", f"Prepping in {c['name']}", "  ·  ".join(c["risks"]) + ". Local alerts, zones and what to do first.", bigfont="display")


def build_files():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    # lastmod = the day a page's main content last changed (tracked in lastmod.json, committed with the source)
    lm_path = os.path.join(HERE, "lastmod.json")
    try:
        lm = json.load(open(lm_path))
    except (OSError, ValueError):
        lm = {}
    today = datetime.date.today().isoformat()
    new_lm = {}
    for rel, _, canon, prio in PAGES:
        h = HASHES.get(rel)
        prev = lm.get(rel)
        new_lm[rel] = {"hash": h, "date": prev["date"] if prev and prev.get("hash") == h else today}
        if canon is None:
            continue
        sm.append(f"  <url><loc>{SITE['url']}{canon}</loc><lastmod>{new_lm[rel]['date']}</lastmod><priority>{prio}</priority></url>")
    try:
        with open(lm_path, "w") as f:
            json.dump(dict(sorted(new_lm.items())), f, indent=1)
            f.write("\n")
    except OSError:
        pass
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    open(os.path.join(OUT, "_headers"), "w").write("/assets/*\n  Cache-Control: public, max-age=604800\n/og/*\n  Cache-Control: public, max-age=604800\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    open(os.path.join(OUT, "_redirects"), "w").write("/score /quiz 302\n/how-prepared-am-i /quiz 301\n")
    open(os.path.join(OUT, "assets", "favicon.svg"), "w").write(BRAND_SVG.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"')
                                                              .replace('fill="none" stroke="currentColor"', 'fill="#F7F8F3" stroke="currentColor"').replace("currentColor", "#142019"))
    # LA renter checklist PDF (rendered by tools/make_handout_pdf.py from the built page)
    if os.path.exists(os.path.join(HERE, "src", "la-renters-checklist.pdf")):
        shutil.copy(os.path.join(HERE, "src", "la-renters-checklist.pdf"), os.path.join(OUT, "la-renters-checklist.pdf"))
    if os.path.exists(os.path.join(HERE, "src", "la-renters-checklist-es.pdf")):
        shutil.copy(os.path.join(HERE, "src", "la-renters-checklist-es.pdf"), os.path.join(OUT, "la-renters-checklist-es.pdf"))
    # Favicon set (rendered by tools/make_icons.py): /favicon.ico and /apple-touch-icon.png at the root, where browsers look for them
    ICONS = os.path.join(HERE, "src", "icons")
    os.makedirs(os.path.join(OUT, "assets", "icons"), exist_ok=True)
    for f in os.listdir(ICONS):
        shutil.copy(os.path.join(ICONS, f), os.path.join(OUT, f if f in ("favicon.ico", "apple-touch-icon.png") else os.path.join("assets", "icons", f)))
    manifest = {"name": SITE["name"], "short_name": SITE["name"], "description": SITE["tagline"], "start_url": "/", "display": "standalone",
                "background_color": "#ECEFE8", "theme_color": "#ECEFE8",
                "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                          {"src": "/assets/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    with open(os.path.join(OUT, "site.webmanifest"), "w") as f:
        json.dump(manifest, f, indent=1)


if __name__ == "__main__":
    ART = os.path.join(HERE, "artifact")
    for d in (OUT, ART):
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "assets"))
    build_home(); build_quiz(); build_scores(); build_locations(); build_cities(); build_guides(); build_pool(); build_resources(); build_library(); build_blackfriday(); build_kit(); build_water_calc(); build_power_calc(); build_food_calc(); build_cpap(); import aptwater, wintercar, winterstorm; build_buyer(aptwater); build_buyer(wintercar); build_buyer(winterstorm); build_gifts(); build_la_renters(); build_la_renters_es(); build_scenarios(); build_misc()
    for f in ("site.css", "quiz.js", "site.js", "data.js", "calc.js", "power.js", "food.js", "track.js"):
        shutil.copy(os.path.join(HERE, "src", f), os.path.join(OUT, "assets", f))
    for rel, parts, _, _ in PAGES:
        write(rel, parts)
    build_og(); build_files()
    if "--preview" in sys.argv:  # optional copy for Claude artifact previews
        shutil.copytree(OUT, ART)
        write("index.html", [p for r, p, _, _ in PAGES if r == "index.html"][0], artifact=True)
    print(f"Built {len(PAGES)} pages into {OUT}")
