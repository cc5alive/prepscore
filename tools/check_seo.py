# -*- coding: utf-8 -*-
"""Indexing safety checks on the built site. build.py runs this last and fails the build
(so Cloudflare doesn't deploy) if anything here breaks. Run on its own: python3 tools/check_seo.py"""
import glob, json, os, re, sys

# Pages that are meant to stay out of Google: the 404 page and the shareable score cards.
NOINDEX_OK = re.compile(r"^(404\.html|score/[a-z-]+\.html)$")


def url_for(rel):
    """dist path -> clean public path, the same way the site links to it."""
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def file_for(out, path):
    """Clean public path -> built file, or None."""
    p = path.split("#", 1)[0].split("?", 1)[0]
    cands = ["index.html"] if p == "/" else [p.strip("/") + ".html", p.strip("/") + "/index.html", p.lstrip("/")]
    for c in cands:
        if os.path.isfile(os.path.join(out, c)):
            return c
    return None


def run(out, site_url, indexnow_key=""):
    errors = []
    err = errors.append

    # robots.txt and sitemap
    robots = open(os.path.join(out, "robots.txt")).read()
    if re.search(r"(?mi)^Disallow:\s*/\s*$", robots):
        err("robots.txt blocks the whole site")
    if f"Sitemap: {site_url}/sitemap.xml" not in robots:
        err("robots.txt doesn't point to the sitemap")
    sitemap = open(os.path.join(out, "sitemap.xml")).read()
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    if len(locs) != len(set(locs)):
        err("sitemap lists a URL more than once")
    in_sitemap = set()
    for loc in locs:
        if not loc.startswith(site_url + "/"):
            err(f"sitemap URL on the wrong host: {loc}")
            continue
        path = loc[len(site_url):]
        in_sitemap.add(path)
        if not file_for(out, path):
            err(f"sitemap URL has no page: {path}")

    titles, descs = {}, {}
    for f in sorted(glob.glob(os.path.join(out, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(f, out).replace(os.sep, "/")
        doc = open(f, encoding="utf-8").read()
        noindex = re.search(r'<meta name="robots" content="[^"]*noindex', doc)
        if noindex and not NOINDEX_OK.match(rel):
            err(f"{rel}: noindex on a page that should be in Google")
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
        title = re.search(r"<title>(.*?)</title>", doc, re.S)
        desc = re.search(r'<meta name="description" content="([^"]*)"', doc)
        if not canon:
            err(f"{rel}: no canonical link")
        if not title or not title.group(1).strip():
            err(f"{rel}: no title")
        if not desc or not desc.group(1).strip():
            err(f"{rel}: no meta description")
        # JSON-LD must parse, or Google ignores it
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
            try:
                json.loads(block)
            except ValueError as ex:
                err(f"{rel}: structured data doesn't parse ({ex})")
        # Internal links must land on a real page
        for href in set(re.findall(r'href="(/[^"]*)"', doc)):
            if href.startswith(("/api/", "//")):
                continue
            if not file_for(out, href):
                err(f"{rel}: broken internal link {href}")
        if noindex:
            continue
        expected = url_for(rel)
        if canon and canon.group(1) != site_url + expected:
            err(f"{rel}: canonical {canon.group(1)} doesn't match its URL {site_url + expected}")
        if expected not in in_sitemap:
            err(f"{rel}: indexable page missing from sitemap")
        if title:
            titles.setdefault(title.group(1).strip(), []).append(rel)
        if desc:
            descs.setdefault(desc.group(1).strip(), []).append(rel)

    for t, rels in titles.items():
        if len(rels) > 1:
            err(f"duplicate title on {', '.join(rels)}: {t}")
    for d, rels in descs.items():
        if len(rels) > 1:
            err(f"duplicate description on {', '.join(rels)}")

    if indexnow_key:
        kf = os.path.join(out, f"{indexnow_key}.txt")
        if not os.path.isfile(kf) or open(kf).read().strip() != indexnow_key:
            err("IndexNow key file missing or wrong")

    if errors:
        print(f"SEO check failed ({len(errors)} problem{'s' if len(errors) != 1 else ''}):")
        for x in errors:
            print("  - " + x)
        return False
    print(f"SEO check passed: {len(locs)} sitemap URLs, {len(titles)} indexable pages.")
    return True


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, here)
    from data import SITE
    sys.path.insert(0, os.path.join(here, "tools"))
    key = ""
    m = re.search(r'"INDEXNOW_KEY"\s*:\s*"([A-Za-z0-9-]{8,128})"', open(os.path.join(here, "wrangler.jsonc")).read())
    if m:
        key = m.group(1)
    sys.exit(0 if run(os.path.join(here, "dist"), SITE["url"], key) else 1)
