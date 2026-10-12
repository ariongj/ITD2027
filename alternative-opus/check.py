# -*- coding: utf-8 -*-
"""Check the built ITD2027 · opus pages: 18 pages, one h1 each, canonical and SQ/EN/DE alternates,
and every local link, picture and #anchor resolves. Links into the main version (../privacy.html etc.)
are checked against alternative-v2/site, where they are published next to /opus/.

    python alternative-opus/check.py"""
import json, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
SITE, MAIN = HERE / "site", HERE.parent / "alternative-v2" / "site"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs, self.ids, self.h1, self.canonical, self.alts = [], set(), 0, [], set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a["href"])
        if tag == "link" and a.get("rel") == "alternate":
            self.alts.add(a.get("hreflang"))
        for k in ("href", "src"):
            if a.get(k):
                self.refs.append(a[k])
        if a.get("srcset"):
            self.refs += [part.strip().split()[0] for part in a["srcset"].split(",")]


pages = {p.name: Page(p.read_text(encoding="utf-8")) for p in sorted(SITE.glob("*.html"))}
errors, checked = [], 0
if len(pages) != 18:
    errors.append(f"expected 18 pages, found {len(pages)}")
for name, page in pages.items():
    if page.h1 != 1:
        errors.append(f"{name}: {page.h1} h1")
    if len(page.canonical) != 1 or not page.canonical[0].endswith("/" + name):
        errors.append(f"{name}: canonical {page.canonical}")
    if page.alts != {"sq", "en", "de", "x-default"}:
        errors.append(f"{name}: alternates {sorted(x or '' for x in page.alts)}")
    for ref in page.refs:
        u = urlsplit(ref)
        if u.scheme or u.netloc or ref.startswith("mailto:") or ref.startswith("tel:"):
            continue
        checked += 1
        path = unquote(u.path)
        if path.startswith("../"):
            target = MAIN / path[3:]
            ids = Page(target.read_text(encoding="utf-8")).ids if target.suffix == ".html" and target.is_file() else set()
        elif path:
            target = SITE / path
            ids = pages[path].ids if path in pages else set()
        else:
            target, ids = SITE / name, page.ids
        if not target.is_file():
            errors.append(f"{name}: missing {ref}")
        elif u.fragment and target.suffix == ".html" and u.fragment not in ids:
            errors.append(f"{name}: missing anchor {ref}")
print(json.dumps({"pages": len(pages), "local_references": checked, "errors": errors[:30]}, ensure_ascii=False))
sys.exit(1 if errors else 0)
