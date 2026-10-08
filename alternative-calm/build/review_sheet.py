# -*- coding: utf-8 -*-
"""List every Albanian and German sentence that is NEW compared with the
previous site, next to the English, for a fluent reviewer.

    py build/review_sheet.py [path-to-previous-site-folder]

Writes build/translation-review.csv (opens in Excel). A sentence counts as
"reused" when it already appears word for word on the previous site in that
language; everything else is "new" and worth a native speaker's read.
Without a previous-site folder, every sentence is listed.
"""
import csv
import html
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from content_sq import L as SQ  # noqa: E402
from content_en import L as EN  # noqa: E402
from content_de import L as DE  # noqa: E402

SKIP_KEYS = {"icon", "href", "id", "num", "slug", "file", "price", "urls", "lang", "locale", "suffix",
             "value", "anchors", "featured", "langName", "title", "desc", "page"}
# Page titles/descriptions of these pages are the current site's (indexed) originals: not for review.
ORIGINAL_PAGES = ("home", "services", "ai", "projects", "creative", "about", "contact", "privacy", "terms", "notfound")
PAGE_NAMES = {"ui": "All pages (menu, footer, forms)", "home": "Home", "services": "Services", "web": "Web & software", "ai": "AI Agents",
              "projects": "Projects", "labs": "ITD Labs", "krakenos": "Kraken OS", "communications": "Kraken Communications", "aura": "AURA",
              "creative": "Creative", "about": "About", "contact": "Contact",
              "privacy": "Privacy", "terms": "Terms", "notfound": "404 page"}


def norm(s):
    s = html.unescape(s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("„", '"').replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def walk(node, path=()):
    """Yield (path, text) for every human-readable string."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in SKIP_KEYS and not (k in ("title", "desc") and path and path[-1] not in ORIGINAL_PAGES):
                continue
            yield from walk(v, path + (k,))
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            yield from walk(v, path + (str(i),))
    elif isinstance(node, str):
        s = node.strip()
        if not s or s.startswith(("/", "http", "#")) or re.fullmatch(r"[\w.-]+\.(webp|png|svg)", s):
            return
        if re.fullmatch(r"[a-z0-9-]+", s) and path and path[-1] in ("0", "1") and len(s) < 12:
            return  # icon names inside tuples
        yield path, s


def get(node, path):
    for p in path:
        node = node[int(p)] if isinstance(node, (list, tuple)) else node[p]
    return node


def corpus(folder, files):
    text = []
    for f in files:
        p = os.path.join(folder, f)
        if os.path.exists(p):
            raw = io.open(p, encoding="utf-8", errors="replace").read()
            raw = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", raw)
            raw = re.sub(r'(?s)<[^>]+?(?:content|aria-label|placeholder|alt|value|title)="([^"]*)"[^>]*>', r" \1 ", raw)
            text.append(re.sub(r"<[^>]+>", " ", raw))
    return norm(" ".join(text))


def main():
    prev = sys.argv[1] if len(sys.argv) > 1 else None
    pages = ["index", "services", "ai-agents", "projects", "creative", "about", "contact", "privacy", "terms", "404"]
    sq_old = corpus(prev, [f"{p}.html" for p in pages]) if prev else ""
    de_old = corpus(prev, [f"{p}-de.html" for p in pages] + ["404.html"]) if prev else ""

    rows, n_sq, n_de = [], 0, 0
    for path, en_text in walk(EN):
        try:
            sq_text, de_text = get(SQ, path), get(DE, path)
        except (KeyError, IndexError, TypeError):
            continue
        if not isinstance(sq_text, str) or not isinstance(de_text, str):
            continue
        sq_new = not (prev and norm(sq_text) in sq_old)
        de_new = not (prev and norm(de_text) in de_old)
        if not (sq_new or de_new):
            continue
        n_sq += sq_new
        n_de += de_new
        page = PAGE_NAMES.get(path[0], path[0])
        rows.append([f"R{len(rows) + 1:03d}", page, ".".join(path[1:]), en_text,
                     sq_text if sq_new else "", "new" if sq_new else "reused",
                     de_text if de_new else "", "new" if de_new else "reused", ""])

    # German-only texts (no English or Albanian counterpart), e.g. the note for the German market.
    for path, de_text in walk(DE):
        try:
            get(EN, path)
            continue
        except (KeyError, IndexError, TypeError):
            pass
        if prev and norm(de_text) in de_old:
            continue
        n_de += 1
        rows.append([f"R{len(rows) + 1:03d}", PAGE_NAMES.get(path[0], path[0]), ".".join(path[1:]), "(German only)",
                     "", "", de_text, "new", ""])

    out = os.path.join(HERE, "translation-review.csv")
    with io.open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ID", "Page", "Where", "English (reference)", "Albanian", "Albanian status",
                    "German", "German status", "Reviewer notes"])
        w.writerows(rows)
    print(f"{len(rows)} rows: {n_sq} new Albanian strings, {n_de} new German strings -> {out}")


if __name__ == "__main__":
    main()
