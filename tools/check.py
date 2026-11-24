#!/usr/bin/env python3
"""Pre-publish checks for bhagyank-calculator.online. Run from the repo root after tools/build.py."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
errors = []


def exists(href):
    path = href.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return (PUB / "index.html").exists()
    return (PUB / (path.strip("/") + ".html")).exists() or (PUB / path.strip("/")).is_file()


# 1. every page: valid JSON-LD, tracking present, internal links resolve
for f in sorted(PUB.rglob("*.html")):
    s = f.read_text()
    rel = f.relative_to(PUB)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except Exception as ex:  # noqa: BLE001
            errors.append(f"{rel}: bad JSON-LD ({ex})")
    if s.count("GTM-WFC7XXW5") != 2:
        errors.append(f"{rel}: Google Tag Manager code missing")
    for href in re.findall(r'href="(/[^"]*)"', s):
        if not exists(href):
            errors.append(f"{rel}: broken internal link {href}")

# 2. sitemap.xml: every page listed once, matches canonicals, hreflang reciprocal, no leftover date tokens
import xml.etree.ElementTree as ET
SITE = "https://www.bhagyank-calculator.online"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
try:
    urls = ET.parse(PUB / "sitemap.xml").findall("s:url", NS)
    locs = [u.find("s:loc", NS).text for u in urls]
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml: duplicate URLs")
    pages = set()
    for f in PUB.rglob("*.html"):
        rel = f.relative_to(PUB).as_posix()[:-5]
        if rel != "404":
            pages.add(SITE + "/" if rel == "index" else SITE + "/" + rel)
    for missing in sorted(pages - set(locs)):
        errors.append(f"sitemap.xml: page missing {missing}")
    for extra in sorted(set(locs) - pages):
        errors.append(f"sitemap.xml: lists a page that does not exist {extra}")
    alts = {u.find("s:loc", NS).text: {a.get("hreflang"): a.get("href") for a in u.findall("x:link", NS)} for u in urls}
    for loc, a in alts.items():
        if a and loc not in alts.get(a.get("en"), {}).values():
            errors.append(f"sitemap.xml: hreflang not reciprocal for {loc}")
        path = loc.replace(SITE, "").strip("/") or "index"
        html = (PUB / (path + ".html")).read_text()
        m = re.search(r'rel="canonical" href="([^"]+)"', html)
        if not m or m.group(1) != loc:
            errors.append(f"{path}.html: canonical does not match sitemap URL {loc}")
except Exception as ex:  # noqa: BLE001
    errors.append(f"sitemap.xml: could not be read ({ex})")
for f in PUB.rglob("*.html"):
    if "__MODIFIED" in f.read_text() or "__PUBLISHED" in f.read_text():
        errors.append(f"{f.relative_to(PUB)}: date placeholder left in page")

# 3. every blog post: rules from CONTENT_GUIDE.md
for pf in sorted((ROOT / "tools" / "posts").glob("*.json")):
    try:
        p = json.loads(pf.read_text())
    except Exception as ex:  # noqa: BLE001
        errors.append(f"{pf.name}: invalid JSON ({ex})")
        continue
    for k in ["slug", "lang", "published", "title", "desc", "h1", "intro", "body", "faqs", "related"]:
        if k not in p:
            errors.append(f"{pf.name}: missing field {k}")
    body = p.get("body", "")
    text = " ".join([p.get("intro", ""), re.sub(r"<[^>]+>", " ", body)] + [q + " " + a for q, a in p.get("faqs", [])])
    if "—" in text or "—" in p.get("title", "") + p.get("desc", ""):
        errors.append(f"{pf.name}: contains an em dash - use a regular hyphen")
    words = len(text.split())
    if words < 900:
        errors.append(f"{pf.name}: only {words} words (aim for 1,000-1,500)")
    ext = re.findall(r'href="(https?://[^"]+|\{\{PEW_[A-Z]+_URL\}\})"', body)
    if len(ext) != 1:
        errors.append(f"{pf.name}: needs exactly 1 external statistic link, found {len(ext)}")
    internal = re.findall(r'href="(/[^"]*)"', body)
    if len(internal) < 4:
        errors.append(f"{pf.name}: only {len(internal)} internal links in the body (need 4-8)")
    if not re.search(r'<section id="[^"]+" class="content-section"><h2>', body):
        errors.append(f"{pf.name}: body must use <section id=.. class=\"content-section\"><h2> blocks")
    if not (3 <= len(p.get("faqs", [])) <= 6):
        errors.append(f"{pf.name}: needs 3-5 FAQs")
    if len(p.get("title", "")) > 70:
        errors.append(f"{pf.name}: title longer than 70 characters")
    out = PUB / (("hi/blog/" if p.get("lang") == "hi" else "blog/") + p.get("slug", "") + ".html")
    if not out.exists():
        errors.append(f"{pf.name}: page not built at {out.relative_to(ROOT)} - run tools/build.py")

if errors:
    print("\n".join(errors))
    print(f"\n{len(errors)} problem(s) found")
    sys.exit(1)
print("ALL CHECKS PASSED")
