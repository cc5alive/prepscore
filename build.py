# -*- coding: utf-8 -*-
"""Static site generator for PrepScore. Run: python3 build.py"""
import html, json, os, shutil, sys, urllib.parse, datetime
from data import SITE, SCENARIOS, MATRIX, QUIZ_CATS, QUIZ, TIERS, LOCATIONS, GUIDES
from cities import CITIES, REGIONS, ALERTS_CHECKED

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dist")
TODAY = datetime.date.today().isoformat()
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


def shell(*, path, title, desc, body, root, og, canon, jsonld=(), active="", scripts=(), body_attr="", noindex=False):
    full_title = title if SITE["name"] in title else f"{title} | {SITE['name']}"
    nav = [("quiz", "quiz.html", "Get your score"), ("where", "where/index.html", "Where you live"),
           ("scenarios", "scenarios.html", "Emergencies"), ("guides", "guides/index.html", "Gear guides")]
    navhtml = ""
    for key, href, label in nav[1:]:
        cur = ' aria-current="page"' if key == active else ""
        navhtml += f'<a href="{root}{href}"{cur}>{label}</a>'
    navhtml += f'<a class="btn" href="{root}quiz.html">Get your PrepScore</a>'
    loc_links = "".join(f'<li><a href="{root}where/{l["slug"]}.html">{e(l["name"])}</a></li>' for l in LOCATIONS)
    guide_links = "".join(f'<li><a href="{root}guides/{g["slug"]}.html">{e(g["short"])}</a></li>' for g in GUIDES)
    head = f"""<title>{e(full_title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE['url']}{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE['url']}{canon}"><meta property="og:image" content="{SITE['url']}/og/{og}.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{f'<meta name="twitter:site" content="{SITE["twitter"]}">' if SITE['twitter'] else ''}
{'<meta name="robots" content="noindex">' if noindex else ''}
<meta name="theme-color" content="#ECEFE8">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}assets/site.css">
{''.join(ld(j) for j in jsonld)}"""
    page = f"""<a class="btn sm" href="#main" style="position:absolute;left:-999px" onfocus="this.style.left='16px'" onblur="this.style.left='-999px'">Skip to content</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="{root}index.html" aria-label="{SITE['name']} home">{BRAND_SVG}{SITE['name']}</a>
<nav class="nav" aria-label="Main">{navhtml}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div class="stack"><a class="brand" href="{root}index.html">{BRAND_SVG}{SITE['name']}</a>
<p class="muted">Practical emergency preparedness for normal people. Find your gaps, fix the important ones first.</p>
<p class="muted small">We earn commissions from links marked Affiliate. <a href="{root}disclosure.html">How we make money</a>. Guidance here is general information, not medical or legal advice. In an emergency, follow instructions from local officials.</p></div>
<div><h4>Where you live</h4><ul>{loc_links}</ul></div>
<div><h4>Gear guides</h4><ul>{guide_links}</ul></div>
<div><h4>Tools</h4><ul><li><a href="{root}quiz.html">How prepared am I?</a></li><li><a href="{root}city/index.html">City guides</a></li><li><a href="{root}scenarios.html">What matters in which emergency</a></li><li><a href="{root}guides/go-bag.html#checklist">Go-bag checklist</a></li><li><a href="{root}disclosure.html">Affiliate disclosure</a></li></ul></div>
</div></footer>
{''.join(f'<script src="{root}assets/{s}"></script>' for s in scripts)}"""
    return head, page, body_attr


def write(rel, parts, artifact=False):
    head, page, body_attr = parts
    out = os.path.join(OUT if not artifact else ART, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if artifact and rel == "index.html":
        doc = head + "\n" + page
    else:
        doc = f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body{body_attr}>\n{page}\n</body>\n</html>\n'
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)


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
<div class="tag-body"><div class="tag-days">11<small>days on your own</small></div>
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


DISCLOSE = lambda root: f'<p class="disclose">Some links on this page are affiliate links, marked <b>Affiliate</b>. If you buy through them we may earn a commission at no extra cost to you. It never decides what we recommend, and we include free options where they exist. <a href="{root}disclosure.html">How we pick and make money</a>.</p>'

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
<p class="lede">Check off what you already have. PrepScore weighs it against the risks where you live, tells you how long your supplies would carry you, and shows the few gaps worth fixing first.</p>
<div class="cta-row"><a class="btn" href="quiz.html">Get your PrepScore</a><span class="muted small">About 3 minutes. No sign-up. Answers stay on your device.</span></div></div>
<div>{tag_example(root)}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Where you live changes the plan</h2><p>An apartment on the 14th floor and a farmhouse on a well fail in completely different ways. Start with your situation.</p></div><a href="where/index.html">All locations</a></div>
<div class="loc-grid">{locs}</div>
<p class="city-strip"><span>City guides:</span> {city_links("")}</p>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>What matters in which emergency</h2><p>The three most critical items for each kind of event. A go-bag is everything in a wildfire and useless in a blizzard.</p></div><a href="scenarios.html">See the full matrix</a></div>
<div class="scen-grid">{scen}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Gear guides</h2><p>What to buy, how much you need and what to skip. Picks at three budgets, with the trade-offs spelled out.</p></div></div>
<ul class="guide-list">{guides}</ul>
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
                            body=body, root=root, og="default", canon="/", jsonld=j), "/", "1.0")


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
    body = f"""<div class="page-head"><div class="wrap">
{crumbs_html([("Home", "/"), ("How prepared am I?", "/quiz")], root)}
<h1>How prepared am I?</h1>
<p class="dek">Check off what you have right now, not what you plan to buy. Your score updates as you go and is weighted for where you live.</p>
</div></div>
<div class="wrap"><div class="quiz-layout">
<div>
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
<div class="tag-body" aria-live="polite"><div class="tag-days"><span data-out="days">0</span><small data-out="dayword">days on your own</small></div>
<div class="tag-score"><b data-out="score">0</b><span>PrepScore / 100</span></div>
<div class="tag-tier" data-out="tier">Sitting Duck</div><p class="tag-line" data-out="line"></p></div>
<ul class="manifest">{man}</ul><div class="hazard"></div>
</div>
<div style="margin-top:1.75rem"><h3>Your 2-week targets</h3>
<div class="targets" style="margin-top:.6rem"><div><b id="t-water">28 gal</b><span>water</span></div><div><b id="t-food">56k kcal</b><span>food</span></div><div><b id="t-bags">56</b><span>toilet bags</span></div></div></div>
<div style="margin-top:1.75rem"><h3>Fix these first</h3><ul class="gaps" id="gaps"></ul></div>
<div class="share-panel" style="margin-top:1.75rem" id="share">
<h3 style="margin-bottom:.75rem">Share your card</h3>
<canvas id="card" width="1200" height="630" aria-label="Your shareable PrepScore card"></canvas>
<div class="share-row"><button type="button" class="btn sm" id="btn-share">Share</button><button type="button" class="btn ghost sm" id="btn-save">Save image</button><button type="button" class="btn ghost sm" id="btn-copy">Copy link</button></div>
<div class="share-row small"><a id="s-x" href="#" target="_blank" rel="noopener">Post on X</a><a id="s-fb" href="#" target="_blank" rel="noopener">Facebook</a><a id="s-reddit" href="#" target="_blank" rel="noopener">Reddit</a><a id="s-wa" href="#" target="_blank" rel="noopener">WhatsApp</a></div>
<textarea id="copy-fallback" hidden rows="3" style="width:100%;margin-top:.5rem" aria-label="Link to copy"></textarea>
<p class="status" id="share-status" role="status"></p>
</div>
</aside>
</div></div>
<div class="mobile-bar"><span><b data-out="score">0</b> <span data-out="tier">Sitting Duck</span></span><a href="#result">See result</a></div>"""
    data = {"quiz": QUIZ, "cats": QUIZ_CATS, "tiers": TIERS,
            "locations": [{"slug": l["slug"], "name": l["name"], "mult": l["mult"], "item": l["item"]} for l in LOCATIONS],
            "site": {"url": SITE["url"], "host": HOST}}
    with open(os.path.join(HERE, "src", "data.js"), "w") as f:
        f.write("window.PREP=" + json.dumps(data, separators=(",", ":")) + ";")
    j = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "PrepScore preparedness quiz",
          "url": SITE["url"] + "/quiz", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "description": "A free checklist that scores your emergency preparedness and estimates how many days you could last on your own."},
         crumbs_ld([("Home", "/"), ("How prepared am I?", "/quiz")])]
    add("quiz.html", shell(path="/quiz", title="How Prepared Am I? Free Emergency Preparedness Quiz",
                           desc="Check off what you have and get your PrepScore: how many days you could last on your own, your biggest gaps, and a card to share. Weighted for where you live.",
                           body=body, root=root, og="quiz", canon="/quiz", jsonld=j,
                           scripts=("data.js", "quiz.js"), body_attr=' class="has-bar" data-root=""'), "/quiz", "0.9")


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
<div class="tag-body"><div class="tag-days"><span id="d">?</span><small>days on their own</small></div>
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
<script>(function(){{var m=(location.hash||"").match(/s(\\d+)-d(\\d+)/);if(!m)return;var s=+m[1],d=+m[2];document.getElementById("s").textContent=s;document.getElementById("d").textContent=d>=90?"90+":d;document.getElementById("who").textContent="Someone scored "+s+" and could last about "+(d>=90?"90+":d)+(d===1?" day":" days")+" on their own.";}})();</script>"""
        add(f"score/{t['slug']}.html", shell(path=f"/score/{t['slug']}", title=f"I'm {t['name']} on PrepScore. How long would you last?",
                                           desc=f"{t['line']} Take the free 3-minute preparedness quiz and see how many days you could last on your own.",
                                           body=body, root=root, og=f"tier-{t['slug']}", canon=f"/score/{t['slug']}"), f"/score/{t['slug']}", "0.4")


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
<p class="city-strip"><span>City guides:</span> {city_links(root)}</p></div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
    add("where/index.html", shell(path="/where/", title="Emergency Preparedness by Location: City, Suburbs, Rural and More",
                                  desc="Emergency prep guides for city apartments, suburbs, rural homes, hurricane coasts, wildfire country and earthquake zones.",
                                  body=body, root=root, og="default", canon="/where/", jsonld=[crumbs_ld(cr)], active="where"), "/where/", "0.8")


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
        same = [o for o in CITIES if o is not c and o["parent"] == c["parent"]]
        region = [o for o in CITIES if o is not c and o["region"] == c["region"] and o not in same]
        near = (same + region)[:5]
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
<div class="aside"><h3>More cities</h3><ul>{near_html}<li><a href="index.html">All city guides</a></li></ul></div></aside>
</div></section>
<section class="section"><div class="wrap"><div class="cta-box"><div><h2>How ready is your {e(c['name'])} home?</h2>
<p>The quiz weights every item for {e(parent['name'].lower())} risks and shows your top gaps. About 3 minutes, no sign-up.</p></div>
<a class="btn" href="{root}quiz.html#{parent['slug']}">Get your PrepScore</a></div></div></section>"""
        j = [{"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "description": c["meta"],
              "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["name"]},
              "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + f"/og/city-{c['slug']}.png",
              "mainEntityOfPage": SITE["url"] + f"/city/{c['slug']}",
              "about": {"@type": "City", "name": f"{c['name']}, {c['state']}"}},
             {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
             crumbs_ld(cr)]
        add(f"city/{c['slug']}.html", shell(path=f"/city/{c['slug']}", title=c["title"], desc=c["meta"], body=body, root=root,
                                           og=f"city-{c['slug']}", canon=f"/city/{c['slug']}", jsonld=j, active="where"), f"/city/{c['slug']}", "0.8")
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
    add("city/index.html", shell(path="/city/", title="Emergency Preparedness by City: Local Alerts, Zones and Risks",
                                 desc="City-by-city emergency prep guides with official alert sign-ups, evacuation zone lookups and local risks for Los Angeles, New York, Houston, Miami and more.",
                                 body=body, root=root, og="default", canon="/city/", jsonld=[crumbs_ld(cr)], active="where"), "/city/", "0.8")


# ---------------------------------------------------------------------------
# Guides
# ---------------------------------------------------------------------------
def build_guides():
    root = "../"
    for g in GUIDES:
        hm = "".join(f'<div><dt>{e(a)}</dt><dd><span class="v">{e(b)}</span>{e(c)}</dd></div>' for a, b, c in g["howmuch"])
        picks = ""
        for tier in ("start", "step", "deep"):
            ps = [p for p in g["picks"] if p["tier"] == tier]
            if not ps:
                continue
            lbl, sub = TIER_LABEL[tier]
            picks += f'<div class="tier-head" style="margin-top:2.5rem"><h2>{lbl}</h2><p>{sub}</p></div>'
            for p in ps:
                if p.get("q"):
                    buy = f'<a class="btn sm" href="{e(amazon(p["q"]))}" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a><span class="aff">Affiliate link</span>'
                else:
                    buy = f'<a class="btn sm" href="{e(p["url"])}" target="_blank" rel="noopener">Find a class</a><span class="aff">Free resource, not an affiliate link</span>'
                picks += f"""<article class="pick"><div><h3>{e(p['name'])}</h3>
<dl class="facts"><dt>What it is</dt><dd>{e(p['what'])}</dd><dt>Why</dt><dd>{e(p['why'])}</dd><dt>Watch out</dt><dd>{e(p['watch'])}</dd></dl></div>
<div class="buy"><span class="price">{e(p['price'])}</span><span class="bestfor">Best for: {e(p['best'])}</span>{buy}</div></article>"""
        choose = "".join(f"<li>{e(x)}</li>" for x in g["choose"])
        mistakes = "".join(f"<li>{e(x)}</li>" for x in g["mistakes"])
        faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faqs"])
        mx = [MX[i] for i in g["matrix"]]
        checklist = ""
        if g.get("checklist"):
            lis = "".join(f'<li><label class="qitem" for="ck-{i}"><input type="checkbox" id="ck-{i}" data-ck><span class="qbox">{CHECK_SVG}</span><span class="t">{e(x)}</span></label></li>' for i, x in enumerate(g["checklist"]))
            checklist = f'<section class="section" id="checklist"><div class="wrap"><div class="section-head"><div><h2>Go-bag checklist</h2><p>Tick items as you pack. Your progress stays in this browser.</p></div><span class="muted" id="ck-count"></span></div><ul class="check-grid">{lis}</ul></div></section>'
        whymx = "".join(f'<li><b>{e(m["name"])}</b>: {e(m["why"])}</li>' for m in mx)
        cr = [("Home", "/"), ("Gear guides", "/guides/"), (g["name"], f"/guides/{g['slug']}")]
        body = f"""<div class="page-head"><div class="wrap">{crumbs_html(cr, root)}
<h1>{e(g['h1'])}</h1><p class="dek">{e(g['dek'])}</p><p class="muted small" style="margin-top:1rem">Updated {datetime.date.today().strftime('%B %Y')}. Prices are typical ranges; check the live price before you buy.</p></div></div>
<section class="section"><div class="wrap stack-l">
{DISCLOSE(root)}
<h2>How much you need</h2><dl class="howmuch">{hm}</dl>
</div></section>
<section class="section"><div class="wrap stack-l">
<div class="section-head" style="margin:0"><div><h2>When it matters</h2><p>How important each item is in each kind of emergency.</p></div><a href="{root}scenarios.html">All items, all emergencies</a></div>
{matrix_table(mx, caption=g['name'] + ' importance by scenario')}
<ul class="plain-list read">{whymx}</ul>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">{picks}</div></section>
{checklist}
<section class="section"><div class="wrap two-col">
<div class="stack-l"><h2>How to choose</h2><ul class="plain-list read">{choose}</ul>
<h2 style="margin-top:2.5rem">Mistakes to avoid</h2><ul class="plain-list read">{mistakes}</ul>
<h2 style="margin-top:2.5rem">Questions</h2><div class="faq">{faqs}</div></div>
<aside class="stack-l"><div class="aside"><h3>Other guides</h3><ul>{''.join(f'<li><a href="{o["slug"]}.html">{e(o["short"])}</a></li>' for o in GUIDES if o is not g)}</ul></div>
<div class="aside"><h3>By location</h3><ul>{''.join(f'<li><a href="{root}where/{l["slug"]}.html">{e(l["name"])}</a></li>' for l in LOCATIONS)}</ul></div></aside>
</div></section>
<section class="section"><div class="wrap">{cta_quiz(root)}</div></section>"""
        j = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["meta"],
              "dateModified": TODAY, "author": {"@type": "Organization", "name": SITE["name"]},
              "publisher": {"@type": "Organization", "name": SITE["name"]}, "image": SITE["url"] + f"/og/guide-{g['slug']}.png",
              "mainEntityOfPage": SITE["url"] + f"/guides/{g['slug']}"},
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
<section class="section"><div class="wrap stack-l">{DISCLOSE(root)}<ul class="guide-list">{lst}</ul></div></section>"""
    add("guides/index.html", shell(path="/guides/", title="Emergency Preparedness Gear Guides", desc="Buyer's guides for emergency water, food, power, first aid, radios, lighting, go-bags and sanitation. Honest picks at three budgets.",
                                   body=body, root=root, og="default", canon="/guides/", jsonld=[crumbs_ld(cr)], active="guides"), "/guides/", "0.8")


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
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
<p>As an Amazon Associate we earn from qualifying purchases.</p>
<p>We don't accept paid placements, sponsored rankings or free products in exchange for coverage.</p>
<h2 style="margin-top:2rem">How we pick</h2>
<p>We start from what you need in a real emergency, then look for gear that does that job reliably at three budgets. We favor items with long track records, independent certifications where they exist (NIOSH for respirators, NSF/ANSI or EPA registration for water treatment), and makers who publish real specs.</p>
<p>Whenever a free or cheap option works, like a Stop the Bleed class or a bathtub full of water, we say so first.</p>
<h2 style="margin-top:2rem">Your quiz answers</h2>
<p>The PrepScore quiz runs entirely in your browser. Your answers are saved on your device so you can come back to them. We don't send them anywhere.</p>
<h2 style="margin-top:2rem">Not professional advice</h2>
<p>This site is general information. It isn't medical, legal or safety-engineering advice. Follow the instructions of local officials during an emergency, and follow every product's safety labels, especially for generators, heaters and stoves.</p>
</div></section>"""
    add("disclosure.html", shell(path="/disclosure", title="Affiliate Disclosure and How We Pick Gear", desc=f"How {SITE['name']} makes money, how we choose gear, and how we handle your quiz answers.",
                                 body=body, root=root, og="default", canon="/disclosure"), "/disclosure", "0.3")
    body = f"""<div class="page-head"><div class="wrap"><h1>Nothing here</h1><p class="dek">This page moved or never existed.</p>
<p style="margin-top:1.5rem"><a class="btn" href="/quiz">Get your PrepScore</a></p></div></div>"""
    PAGES.append(("404.html", shell(path="/404", title="Page not found", desc="Page not found.", body=body, root="/", og="default", canon="/404", noindex=True), None, None))


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
    card("quiz", "How prepared am I?", "Get your PrepScore", "Check off what you have. See how long you'd last, your top gaps, and a card to share.")
    card("scenarios", "Emergencies", "What matters when", "Outages, earthquakes, evacuations, bad water, sheltering in place and long grid-down events.", bigfont="display")
    for t in TIERS:
        card(f"tier-{t['slug']}", f"Tier {t['min']}–{t['max']}", t["name"], t["brag"] + " How long would you last?", color=t["color"])
    for l in LOCATIONS:
        card(f"loc-{l['slug']}", "Where you live", l["h1"], l["dek"], bigfont="display")
    for g in GUIDES:
        card(f"guide-{g['slug']}", "Buyer's guide", g["name"], g["dek"])
    for c in CITIES:
        card(f"city-{c['slug']}", f"City guide  ·  {c['state']}", f"Prepping in {c['name']}", "  ·  ".join(c["risks"]) + ". Local alerts, zones and what to do first.", bigfont="display")


def build_files():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel, _, canon, prio in PAGES:
        if canon is None:
            continue
        sm.append(f"  <url><loc>{SITE['url']}{canon}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    open(os.path.join(OUT, "_headers"), "w").write("/assets/*\n  Cache-Control: public, max-age=604800\n/og/*\n  Cache-Control: public, max-age=604800\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    open(os.path.join(OUT, "_redirects"), "w").write("/score /quiz 302\n/how-prepared-am-i /quiz 301\n")
    open(os.path.join(OUT, "assets", "favicon.svg"), "w").write(BRAND_SVG.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"').replace("currentColor", "#142019"))


if __name__ == "__main__":
    ART = os.path.join(HERE, "artifact")
    for d in (OUT, ART):
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "assets"))
    build_home(); build_quiz(); build_scores(); build_locations(); build_cities(); build_guides(); build_scenarios(); build_misc()
    for f in ("site.css", "quiz.js", "site.js", "data.js"):
        shutil.copy(os.path.join(HERE, "src", f), os.path.join(OUT, "assets", f))
    for rel, parts, _, _ in PAGES:
        write(rel, parts)
    build_og(); build_files()
    if "--preview" in sys.argv:  # optional copy for Claude artifact previews
        shutil.copytree(OUT, ART)
        write("index.html", [p for r, p, _, _ in PAGES if r == "index.html"][0], artifact=True)
    print(f"Built {len(PAGES)} pages into {OUT}")
