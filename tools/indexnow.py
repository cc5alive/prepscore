# -*- coding: utf-8 -*-
"""Submit URLs to IndexNow by hand. The Worker already pings changed pages once a day;
use this for a one-off full submission (after the key file is live on prepscore.org).

  python3 tools/indexnow.py --all          every URL in the live sitemap
  python3 tools/indexnow.py /guides/water  specific pages
"""
import json, re, sys, urllib.request

HOST = "prepscore.org"
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))


def main(args):
    key = re.search(r'"INDEXNOW_KEY"\s*:\s*"([^"]+)"', open(f"{ROOT}/wrangler.jsonc").read()).group(1)
    if args == ["--all"]:
        xml = urllib.request.urlopen(f"https://{HOST}/sitemap.xml", timeout=30).read().decode()
        urls = re.findall(r"<loc>([^<]+)</loc>", xml)
    elif args:
        urls = [u if u.startswith("http") else f"https://{HOST}{u}" for u in args]
    else:
        sys.exit(__doc__)
    body = json.dumps({"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow answered {r.status} for {len(urls)} URLs (200 or 202 means accepted)")


if __name__ == "__main__":
    main(sys.argv[1:])
