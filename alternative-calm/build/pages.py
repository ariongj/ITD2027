# -*- coding: utf-8 -*-
"""Make a preview copy of the built site for GitHub Pages (or any sub-folder host).

    py -X utf8 build/pages.py <output folder>

The real site uses root-relative links ("/services-en", "/css/site.css") and
clean URLs that .htaccess maps on Hostinger. A project page such as
https://ariongj.github.io/ITD2027/calm/ has neither, so the preview copy:
  - rewrites every root-relative link to a relative one ("services-en.html",
    "css/site.css", "../assets/..." inside the stylesheet);
  - is marked noindex,nofollow (the live address stays itdks.tech);
  - leaves out consent + analytics, so preview visits never reach GA4/Ads;
  - leaves out server files (.htaccess, PHP, sitemap, deploy scripts, build/).
Forms still post to the real Formspree endpoint and the chat still opens the
Kraken assistant, exactly like the live site.

The copy is then checked the way scripts/check-pages.py checks the ITD2027
proposal: every local link and anchor must resolve, no root-relative URL may
remain, one <h1> per page, no non-public files. Exit code 1 on any problem.
"""
import os
import re
import shutil
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY_DIRS = ["css", "js", "assets"]
COPY_FILES = ["chatbot.js", "favicon.ico"]
HOME = {"/": "index.html", "/en": "index-en.html", "/de": "index-de.html"}
MEASUREMENT = re.compile(r'<!-- ITD measurement \(consent-gated\) -->\s*<link rel="stylesheet" href="/consent\.css[^"]*">\s*'
                         r'<script defer src="/analytics-config\.js[^"]*"></script>\s*<script defer src="/consent\.js[^"]*"></script>\s*'
                         r'<script defer src="/analytics\.min\.js[^"]*" data-itd-analytics="true"></script>\s*')


def rel(url, pages):
    """Root-relative URL -> relative URL for a page that sits in the site root."""
    if not url.startswith("/") or url.startswith("//"):
        return url
    parts = urlsplit(url)
    path = parts.path
    if path in HOME:
        new = HOME[path]
    elif "." not in path.rsplit("/", 1)[-1] and path.lstrip("/") + ".html" in pages:
        new = path.lstrip("/") + ".html"
    else:
        new = path.lstrip("/")
    return new + (f"?{parts.query}" if parts.query else "") + (f"#{parts.fragment}" if parts.fragment else "")


def rewrite_html(text, pages):
    text, n = MEASUREMENT.subn("", text)
    if n != 1:
        raise SystemExit("measurement block not found: templates changed? update build/pages.py")
    text = text.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex,nofollow">')
    text = text.replace('<meta name="robots" content="noindex, follow">', '<meta name="robots" content="noindex,nofollow">')
    text = re.sub(r'\b(href|src|data-contact-url)="([^"]*)"', lambda m: f'{m.group(1)}="{rel(m.group(2), pages)}"', text)
    text = re.sub(r'\bsrcset="([^"]*)"', lambda m: 'srcset="' + ", ".join(
        " ".join([rel(p.split()[0], pages)] + p.split()[1:]) for p in m.group(1).split(",")) + '"', text)
    return text


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs, self.ids, self.h1 = [], set(), 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])
        if a.get("srcset"):
            self.refs += [p.split()[0] for p in a["srcset"].split(",")]


def check(out):
    errors, checked = [], 0
    pages = {name: Page(open(os.path.join(out, name), encoding="utf-8").read())
             for name in os.listdir(out) if name.endswith(".html")}

    def target(source_dir, ref, where):
        nonlocal checked
        url = urlsplit(ref)
        if url.scheme or url.netloc or ref.startswith(("mailto:", "tel:", "data:")):
            return
        if url.path.startswith("/"):
            errors.append(f"{where}: root-relative URL left: {ref}")
            return
        path = os.path.normpath(os.path.join(source_dir, unquote(url.path))) if url.path else None
        checked += 1
        if path and os.path.isdir(path):
            path = os.path.join(path, "index.html")
        if path and (not os.path.isfile(path) or not os.path.abspath(path).startswith(os.path.abspath(out))):
            errors.append(f"{where}: missing target: {ref}")
            return
        name = os.path.basename(path) if path else where
        if url.fragment and name in pages and unquote(url.fragment) not in pages[name].ids:
            errors.append(f"{where}: missing anchor: {ref}")

    for name, page in pages.items():
        if page.h1 != 1:
            errors.append(f"{name}: expected one <h1>, found {page.h1}")
        for ref in page.refs:
            target(out, ref, name)
    for dirpath, _, files in os.walk(out):
        for f in files:
            p = os.path.join(dirpath, f)
            if f.endswith(".css"):
                for ref in re.findall(r"url\(\s*['\"]?([^'\"\)]+)['\"]?\s*\)", open(p, encoding="utf-8").read()):
                    target(dirpath, ref.strip(), f)
            if f.startswith((".env", ".ht")) or f.lower().endswith((".php", ".py", ".ps1", ".cmd", ".zip", ".pem", ".key", ".xlsx", ".csv")):
                errors.append(f"non-public file in preview: {os.path.relpath(p, out)}")
    return len(pages), checked, errors


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out = os.path.abspath(sys.argv[1])
    if os.path.abspath(SRC) == out or os.path.abspath(SRC).startswith(out + os.sep):
        raise SystemExit("output folder must not contain the source folder")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    pages = {f for f in os.listdir(SRC) if f.endswith(".html")}
    for name in sorted(pages):
        with open(os.path.join(SRC, name), encoding="utf-8") as fh:
            text = rewrite_html(fh.read(), pages)
        with open(os.path.join(out, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    for d in COPY_DIRS:
        shutil.copytree(os.path.join(SRC, d), os.path.join(out, d))
    for f in COPY_FILES:
        shutil.copy2(os.path.join(SRC, f), out)
    # The stylesheet lives in css/, so its root-relative font URLs become ../assets/...
    css = os.path.join(out, "css", "site.css")
    text = open(css, encoding="utf-8").read().replace('url("/assets/', 'url("../assets/')
    open(css, "w", encoding="utf-8", newline="\n").write(text)
    manifest = open(os.path.join(SRC, "site.webmanifest"), encoding="utf-8").read()
    manifest = manifest.replace('"start_url": "/"', '"start_url": "./"').replace('"src": "/assets/', '"src": "assets/')
    open(os.path.join(out, "site.webmanifest"), "w", encoding="utf-8", newline="\n").write(manifest)

    n, checked, errors = check(out)
    print(f"preview: {n} pages, {checked} local references checked, {len(errors)} problems -> {out}")
    for e in errors[:40]:
        print("  " + e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
