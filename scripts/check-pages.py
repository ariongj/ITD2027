"""Validate the exact static directory published to GitHub Pages.

    python scripts/check-pages.py [folder]   (default alternative-v2/site; ITD2027/M is alternative-v2/site-m)"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "alternative-v2" / "site"

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs, self.ids, self.headings, self.canonical = [], set(), 0, ""
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        for key in ("href", "src"):
            if attrs.get(key):
                self.refs.append(attrs[key])

pages = {path.resolve(): Page(path.read_text(encoding="utf-8-sig"))
         for path in ROOT.rglob("*.html")}
errors, checked = [], 0
# 54 pages, plus the 18 project pages in project/ on the main version.
EXPECTED = 72 if (ROOT / "project").is_dir() else 54
if len(pages) != EXPECTED or not (ROOT / "index.html").is_file():
    errors.append(f"Expected the complete newer website with {EXPECTED} HTML pages.")
# The site's base path from the home page's canonical URL (/ITD2027/ on GitHub, / on the domain).
home = pages.get((ROOT / "index.html").resolve())
BASE = urlsplit(home.canonical).path.rsplit("/", 1)[0] + "/" if home and home.canonical else ""

def check_reference(source, reference):
    global checked
    url = urlsplit(reference)
    if url.scheme or url.netloc:
        return
    path = url.path
    if path.startswith("/"):
        # Root-relative is fine only under the site's own base path: the 404 pages (missing URLs at any depth)
        # and the pages in project/ use it. It resolves from the site root.
        if not BASE or not path.startswith(BASE):
            errors.append(f"{source.name}: root-relative URL breaks project hosting: {reference}")
            return
        target = (ROOT / unquote(path[len(BASE):])).resolve()
    else:
        target = (source.parent / unquote(path)).resolve() if path else source.resolve()
    if target.is_dir():
        target /= "index.html"
    checked += 1
    if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
        errors.append(f"{source.name}: missing or outside-site target: {reference}")
    elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
        errors.append(f"{source.name}: missing anchor: {reference}")

for source, page in pages.items():
    if page.headings != 1:
        errors.append(f"{source.name}: expected one main heading.")
    for reference in page.refs:
        check_reference(source, reference)

for source in ROOT.rglob("*.css"):
    for reference in re.findall(r"url\(\s*['\"]?([^'\"\)]+)['\"]?\s*\)", source.read_text(encoding="utf-8")):
        check_reference(source, reference.strip())

for source in ROOT.rglob("*"):
    if source.is_symlink():
        errors.append(f"Symlink in publish directory: {source.relative_to(ROOT)}")
    if source.is_file() and (source.name.startswith(".env") or source.suffix.lower() in {
        ".php", ".py", ".ps1", ".sqlite", ".db", ".pem", ".key", ".zip"
    }):
        errors.append(f"Non-public file in publish directory: {source.relative_to(ROOT)}")

print(json.dumps({"pages": len(pages), "local_references": checked, "errors": errors}))
raise SystemExit(1 if errors else 0)
