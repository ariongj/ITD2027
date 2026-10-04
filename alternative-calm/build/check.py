# -*- coding: utf-8 -*-
"""Quick QA over the built site: broken internal links/anchors, leftover
template placeholders, invalid JSON-LD, and a rough tag-balance check.

    py build/check.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [f for f in os.listdir(ROOT) if f.endswith(".html")]
CLEAN = {"/": "index.html", "/en": "index-en.html", "/de": "index-de.html"}
PLACEHOLDERS = ["{plan}", "{price}", "{product}", "{link}", "{email}", "{phone}", ">None<", "&amp;amp;", "Ã", "â€"]
problems = []


def target_file(path):
    if path in CLEAN:
        return CLEAN[path]
    name = path.strip("/")
    if os.path.exists(os.path.join(ROOT, name)):
        return name
    if os.path.exists(os.path.join(ROOT, name + ".html")):
        return name + ".html"
    return None


ids = {}
for page in PAGES:
    with open(os.path.join(ROOT, page), encoding="utf-8") as fh:
        html = fh.read()
    ids[page] = set(re.findall(r'\sid="([^"]+)"', html))

for page in sorted(PAGES):
    with open(os.path.join(ROOT, page), encoding="utf-8") as fh:
        html = fh.read()
    # data-pkg-* / data-demo-* attributes carry templates on purpose; check everything else.
    visible = re.sub(r'\sdata-(?:pkg|demo)-[a-z]+="[^"]*"', "", html)
    for ph in PLACEHOLDERS:
        if ph in visible:
            problems.append(f"{page}: leftover placeholder {ph!r}")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(m.group(1).replace("<\\/", "</"))
        except ValueError as exc:
            problems.append(f"{page}: invalid JSON-LD ({exc})")
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', html):
        if url.startswith(("http", "mailto:", "tel:", "data:", "javascript:")):
            continue
        if url.startswith("#"):
            if url[1:] and url[1:] not in ids[page]:
                problems.append(f"{page}: missing anchor {url}")
            continue
        path, _, frag = url.partition("#")
        path = path.split("?", 1)[0]
        if not path.startswith("/"):
            problems.append(f"{page}: relative url {url}")
            continue
        tf = target_file(path)
        if tf is None:
            problems.append(f"{page}: broken link {url}")
        elif frag and tf.endswith(".html") and frag not in ids.get(tf, set()):
            problems.append(f"{page}: missing anchor #{frag} in {tf}")
    for tag in ("div", "section", "article", "ul", "ol", "li", "form", "a", "p", "h1", "h2", "h3", "span", "label", "figure", "dialog", "nav", "header", "footer", "main", "button", "details", "summary"):
        opens = len(re.findall(rf"<{tag}\b[^>]*(?<!/)>", html))
        closes = len(re.findall(rf"</{tag}>", html))
        if opens != closes:
            problems.append(f"{page}: <{tag}> opens {opens} vs closes {closes}")
    all_ids = re.findall(r'\sid="([^"]+)"', html)
    dup = sorted({i for i in all_ids if all_ids.count(i) > 1})
    if dup:
        problems.append(f"{page}: duplicate id(s) {dup}")
    if html.count("<h1") != 1:
        problems.append(f"{page}: {html.count('<h1')} <h1> tags")
    if 'lang="' not in html[:200]:
        problems.append(f"{page}: missing lang attribute")

# Section anchors that existed on the previous site. Links in ads, posts and
# bookmarks may point at them, so every one must still exist.
LEGACY = {
    "index": ["package-inquiry"],
    "services": ["websites", "business-systems", "it-support", "cybersecurity", "it-audit", "branding", "marketing"],
    "ai-agents": ["ai-build", "ai-agent-brief", "contact-form"],
    "projects": ["case-examples"],
    "creative": ["creative-services", "creative-showcase", "creative-contact", "contact-form"],
    "about": ["faq"],
    "contact": ["booking-call", "contact-form"],
    "privacy": ["measurement-privacy"],
}
for base, anchors in LEGACY.items():
    for suffix in ("", "-en", "-de"):
        page = f"{base}{suffix}.html"
        extra = []
        if base == "index":
            extra = ["zgjidh-paketen"] if suffix == "" else ["choose-package"]
        for a in anchors + extra:
            if a not in ids.get(page, set()):
                problems.append(f"{page}: legacy anchor #{a} missing")

print(f"Checked {len(PAGES)} pages.")
if problems:
    print("\n".join(problems))
    sys.exit(1)
print("No problems found.")
