# -*- coding: utf-8 -*-
"""ITD2027 · opus — the IT Department site, designed in the editorial style of the SELCA site.

    python alternative-opus/build.py            -> alternative-opus/site/ (18 pages, SQ / EN / DE)

Content comes from the approved sources, so it never drifts from the other versions:
  - services, monthly plans and FAQ: the original site pages at the repository root;
  - page texts and form labels: T in alternative-v2/build.py;
  - projects, partners, social links: PROJECTS, PARTNERS, SOCIAL in alternative-v2/proposal.py;
  - the words that are new in this design: content.py.
Pictures and fonts are copied from alternative-v2 at build time (nothing duplicated in git). The pages are a
preview (noindex), link to each other relatively, and use the privacy and terms pages of the main version."""
import ast, json, os, re, shutil, sys
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V2 = ROOT / "alternative-v2"
OUT = HERE / "site"
BASE_URL = os.environ.get("OPUS_SITE_URL", "https://ariongj.github.io/ITD2027/opus").rstrip("/")
sys.path.insert(0, str(HERE))
from content import C, LANGS, SUFFIX, LANG_NAMES, tr  # noqa: E402

cfg = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8-sig"))


def literal(path, name):
    """A literal assignment (dict/list) from another generator file, read without running that file."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            tgt = node.targets[0]
            if getattr(tgt, "id", "") == name:
                return ast.literal_eval(node.value)
    raise KeyError(name)


def texts():
    tree = ast.parse((V2 / "build.py").read_text(encoding="utf-8-sig"))
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Subscript) and getattr(node.targets[0].value, "id", "") == "T":
            out[node.targets[0].slice.value] = ast.literal_eval(node.value)
    return out


T = texts()
PROJECTS = literal(V2 / "proposal.py", "PROJECTS")
PARTNERS = literal(V2 / "proposal.py", "PARTNERS")
SOCIAL = literal(V2 / "proposal.py", "SOCIAL")


# ---------------------------------------------------------------- original pages (approved services, plans, FAQ)
class Node:
    def __init__(self, tag="", attrs=()):
        self.tag = tag; self.attrs = dict(attrs); self.children = []

    def find(self, tag=None, cls=None):
        out = []
        for n in self.children:
            if isinstance(n, Node):
                if (not tag or n.tag == tag) and (not cls or cls in n.attrs.get("class", "").split()):
                    out.append(n)
                out += n.find(tag, cls)
        return out

    def text(self):
        return " ".join(" ".join(c.text() if isinstance(c, Node) else c for c in self.children).split())


class Parser(HTMLParser):
    VOID = {"img", "input", "br", "hr", "meta", "link", "source", "wbr", "area", "base", "embed", "param", "track", "col"}

    def __init__(self, t):
        super().__init__(convert_charrefs=True); self.root = Node(); self.stack = [self.root]; self.feed(t)

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs); self.stack[-1].children.append(n)
        if tag not in self.VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]; break

    def handle_data(self, d):
        self.stack[-1].children.append(d)


def source(page, l):
    return Parser((ROOT / f"{page}{SUFFIX[l]}.html").read_text(encoding="utf-8-sig")).root


def services(l):
    out = []
    for n in source("services", l).find("article", "service-card"):
        ps = [p.text() for p in n.find("p")]
        ps = [p for p in ps if not re.fullmatch(r"\d\d", p)]
        out.append({"title": n.find("h3")[0].text(), "text": ps[0] if ps else "", "result": ps[-1] if len(ps) > 1 else "",
                    "items": [x.text() for x in n.find("li")]})
    assert len(out) == 8, len(out)
    return out


def plans(l):
    out = []
    for n, price in zip(source("index", l).find("article", "pricing-card"), [99, 299, 779]):
        ps = [p.text() for p in n.find("p")]
        out.append({"name": ps[0], "fit": ps[1] if len(ps) > 1 else "", "title": n.find("h3")[0].text(), "price": price, "items": [x.text() for x in n.find("li")]})
    assert len(out) == 3
    return out


def faqs(l):
    out = []
    for n in source("about", l).find("details", "faq-card"):
        q, a = n.find(cls="faq-question"), n.find(cls="faq-answer")
        if q and a:
            out.append((q[0].text(), a[0].text()))
    assert len(out) >= 8, len(out)
    return out


# ---------------------------------------------------------------- helpers
def esc(s):
    return escape(str(s), quote=True)


def rich(s):
    """Escape, then turn *word* into the italic accent."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", esc(s))


def href(page, l, anchor=""):
    return f"{page}{SUFFIX[l]}.html" + (f"#{anchor}" if anchor else "")


A = '<span class="arrow" aria-hidden="true">↗</span>'
ICONS = {
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4m8-4v4M3 10h18"/>',
    "browser": '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    "shield": '<path d="m12 3 8 3v6c0 5-8 9-8 9S4 17 4 12V6Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4Z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "left": '<path d="m14 6-6 6 6 6"/>',
    "right": '<path d="m10 6 6 6-6 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def button(label, url, style="", extra=""):
    return f'<a class="btn {style}" href="{esc(url)}"{extra}>{esc(label)}{A}</a>'


def wa(l):
    return "https://wa.me/" + cfg["phoneDigits"] + "?text=" + quote(tr(l, "Përshëndetje IT Department, dëshiroj të flasim për një projekt.",
                                                                       "Hello IT Department, I would like to discuss a project.", "Hallo IT Department, ich möchte ein Projekt besprechen."))


EXT = ' target="_blank" rel="noopener noreferrer"'


def head(eyebrow, title, lead="", action="", cls=""):
    return (f'<div class="sec-head {cls}"><div><p class="eyebrow">{esc(eyebrow)}</p><h2>{rich(title)}</h2>'
            + (f'<p class="sec-lead">{esc(lead)}</p>' if lead else "") + f"</div>{action}</div>")


def link(label, url, extra=""):
    return f'<a class="link" href="{esc(url)}"{extra}>{esc(label)}{A}</a>'


# ---------------------------------------------------------------- shared blocks
def topbar(l, t):
    langs = "".join(f'<a href="{{lang_{x}}}" lang="{x}" hreflang="{x}"{" aria-current=true" if x == l else ""} aria-label="{LANG_NAMES[x]}">{x.upper()}</a>' for x in LANGS)
    return (f'<aside class="topbar" aria-label="{esc(t["contact"])}"><div class="wrap topbar-in"><div class="topbar-contact">'
            f'<a href="tel:+{cfg["phoneDigits"]}">{icon("phone")}{cfg["phoneDisplay"]}</a><a class="hide-sm" href="mailto:{cfg["email"]}">{icon("mail")}{cfg["email"]}</a></div>'
            f'<p class="hide-md">{icon("clock")}{esc(t["hours"])} · {esc(t["location"])}</p><nav class="langs" aria-label="{esc(t["lang"])}">{langs}</nav></div></aside>')


def header(page, l, t, c):
    items = "".join(f'<a href="{href(p, l)}"{" aria-current=page" if p == page else ""}>{esc(name)}</a>' for p, name in c["nav"])
    return (f'<a class="skip" href="#main">{esc(t["skip"])}</a>{topbar(l, t)}'
            f'<header class="header" data-header><div class="wrap header-in"><a class="brand" href="{href("index", l)}" aria-label="IT Department · {esc(c["home_nav"])}">'
            f'<img src="assets/logo-ink.png" width="480" height="232" alt="IT Department"></a>'
            f'<nav class="nav" id="nav" aria-label="{esc(t["menu"])}">{items}<a class="btn btn-sm nav-book" href="{esc(cfg["bookingUrl"])}"{EXT}>{esc(c["book"])}{A}</a></nav>'
            f'<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" data-menu><span class="sr">{esc(t["menu"])}</span>{icon("menu", "icon i-open")}{icon("close", "icon i-close")}</button>'
            f"</div></header>")


def footer(l, t, c):
    fam = "".join(f'<li><a href="{href("services", l, k)}">{esc(n)}</a></li>' for k, n, _ in c["families"])
    pages = "".join(f'<li><a href="{href(p, l)}">{esc(n)}</a></li>' for p, n in [("index", c["home_nav"])] + c["nav"])
    labs = "".join(f'<li><a href="{href("labs", l, p["key"])}">{esc(p["name"])}</a></li>' for p in c["products"])
    social = "".join(f'<a class="chip" href="{esc(u)}"{EXT}>{esc(n)}</a>' for n, u in SOCIAL)
    legal = f'<a href="../privacy{SUFFIX[l]}.html">{esc(t["privacy"])}</a><a href="../terms{SUFFIX[l]}.html">{esc(t["terms"])}</a>'
    return (f'<footer class="footer"><div class="wrap"><div class="foot-top"><p class="foot-claim">{esc(t["footer"])}</p>'
            f'<div class="foot-cta">{button(c["book"], cfg["bookingUrl"], "btn-light", EXT)}<a class="foot-mail" href="mailto:{cfg["email"]}">{cfg["email"]}{A}</a></div></div>'
            f'<div class="foot-grid"><div class="foot-brand"><img src="assets/brand/logo-original.png" width="480" height="232" alt="IT Department" loading="lazy">'
            f'<p class="foot-follow">{esc(c["follow"])}</p><div class="foot-social">{social}</div></div>'
            f'<div><p class="foot-title">IT Department</p><ul>{pages}</ul></div><div><p class="foot-title">{esc(c["nav"][0][1])}</p><ul>{fam}</ul></div>'
            f'<div><p class="foot-title">ITD Labs</p><ul>{labs}</ul></div>'
            f'<div><p class="foot-title">{esc(t["contact"])}</p><ul class="foot-contact"><li>{icon("mail")}<a href="mailto:{cfg["email"]}">{cfg["email"]}</a></li>'
            f'<li>{icon("phone")}<a href="tel:+{cfg["phoneDigits"]}">{cfg["phoneDisplay"]}</a></li><li>{icon("chat")}<a href="{esc(wa(l))}"{EXT}>WhatsApp</a></li>'
            f'<li>{icon("clock")}<span>{esc(t["hours"])}</span></li><li>{icon("pin")}<span>{esc(t["location"])}</span></li></ul></div></div>'
            f'<div class="foot-bottom"><p>© 2026 IT Department · {esc(t["location"])}</p><div class="foot-legal">{legal}<a href="../index{SUFFIX[l]}.html">{esc(c["versions"])}</a></div></div>'
            f"</div></footer>")


def cta(l, t, c):
    return (f'<section class="cta wrap" aria-labelledby="cta-title"><div class="cta-in"><div><p class="eyebrow">{esc(t["talk"])}</p><h2 id="cta-title">{rich(c["cta_title"])}</h2>'
            f'<p>{esc(t["endingbody"])}</p></div><div class="cta-actions">{button(c["contact_btn"], href("contact", l))}'
            f'{button("WhatsApp", wa(l), "btn-ghost-light", EXT)}{button(c["book"], cfg["bookingUrl"], "btn-ghost-light", EXT)}</div></div></section>')


def project_card(p, l, c, tag="h3", lazy=True):
    url = p["final"] or p["url"]
    return (f'<a class="proj" href="{esc(url)}"{EXT} data-project="{p["key"]}"><div class="proj-shot">'
            f'<img src="assets/projects/{p["key"]}-720.webp" srcset="assets/projects/{p["key"]}-720.webp 720w, assets/projects/{p["key"]}-1440.webp 1440w" sizes="(max-width:800px) 86vw, 34vw" width="720" height="450" alt=""{" loading=lazy" if lazy else ""} decoding="async"></div>'
            f'<div class="proj-copy"><p class="proj-cat">{esc(tr(l, *p["category"]))}</p><{tag}>{esc(p["name"])}{A}</{tag}><p>{esc(tr(l, *p["text"]))}</p>'
            f'<span class="sr"> ({esc(c["new_tab"])})</span></div></a>')


def steps_block(c):
    return '<ol class="steps">' + "".join(
        f'<li><p class="step-n">0{i + 1} / {esc(c["phases"][i])}</p><h3>{esc(n)}</h3><p>{esc(d)}</p></li>' for i, (n, d) in enumerate(c["steps"])) + "</ol>"


def partner_marquee(l, c):
    logos = "".join(f'<li><img src="assets/partners/{f}" alt="{esc(n)}" width="{w}" height="{h}" loading="lazy"{" class=tone" if tone else ""}></li>'
                    for _, n, f, (w, h), _, tone in PARTNERS)
    dup = "".join(f'<li><img src="assets/partners/{f}" alt="" width="{w}" height="{h}" loading="lazy"{" class=tone" if tone else ""}></li>'
                  for _, n, f, (w, h), _, tone in PARTNERS)
    return f'<div class="marquee" data-marquee><ul class="marquee-track">{logos}</ul><ul class="marquee-track" aria-hidden="true">{dup}</ul></div>'


def pricing_block(l, t, c, plist):
    cards = ""
    for i, p in enumerate(plist):
        items = "".join(f"<li>{esc(x)}</li>" for x in p["items"])
        cards += (f'<article class="plan{" plan-featured" if i == 1 else ""}"><p class="eyebrow">{esc(p["name"])}</p><h3>{esc(p["title"])}</h3><p class="plan-fit">{esc(p["fit"])}</p>'
                  f'<p class="price">€{p["price"]}<span>{esc(t["month"])}</span></p><details class="plan-more"><summary>{esc(c["included"])}{icon("plus")}</summary><ul>{items}</ul></details>'
                  f'{button(t["enquire"], href("contact", l) + "?service=" + quote(p["name"] + " €" + str(p["price"])), "btn-outline" if i != 1 else "")}</article>')
    return cards


# ---------------------------------------------------------------- pages
def page_home(l, t, c):
    shots = [p["key"] for p in PROJECTS]
    wall = "".join(f'<div class="wall-col wall-col-{k}">' + "".join(
        f'<img src="assets/projects/{shots[(i + k * 2) % 5]}-720.webp" width="720" height="450" alt=""{" loading=lazy" if k else ""} decoding="async">' for i in range(6)) + "</div>" for k in range(3))
    facts = ""
    for ic, title, text, target in c["facts"]:
        inner = f'<span class="fact-icon">{icon(ic)}</span><span><strong>{esc(title)}</strong><span>{esc(text)}</span></span>'
        url = {"book": cfg["bookingUrl"], "projects": href("projects", l), "pricing": "#pricing", "": ""}[target]
        facts += (f'<a class="fact" href="{esc(url)}"{EXT if url.startswith("http") else ""}>{inner}</a>' if url else f'<div class="fact">{inner}</div>')
    pics = {"web": ("projects/kobags-720.webp", 720, 450), "it": ("brand/banner-texture.webp", 738, 453), "ai": ("labs/slide-communications.webp", 760, 396), "creative": ("creative/nexus-brandbook.webp", 1024, 1536)}
    areas = "".join(
        f'<a class="area area-{k}" href="{href("services", l, k)}"><img src="assets/{pics[k][0]}" width="{pics[k][1]}" height="{pics[k][2]}" alt="" loading="lazy">'
        + (f'<span class="area-badge">{icon("shield")}</span>' if k == "it" else "")
        + f'<span class="area-copy"><span class="area-n">0{i + 1}</span><h3>{esc(n)}</h3><span class="area-text">{esc(d)}</span></span><span class="area-go" aria-hidden="true">↗</span></a>'
        for i, (k, n, d) in enumerate(c["families"]))
    work = "".join(project_card(p, l, c) for p in PROJECTS)
    products = "".join(
        f'<a class="product product-{p["key"]}" href="{href("labs", l, p["key"])}"><span class="product-shot"><img src="assets/{p["image"]}" width="{p["size"][0]}" height="{p["size"][1]}" alt="" loading="lazy"></span>'
        f'<span class="product-copy"><span class="product-kind">0{i + 1} / {esc(p["kind"])}</span><h3>{esc(p["name"])}</h3><span>{esc(p["text"])}</span></span></a>'
        for i, p in enumerate(c["products"]))
    faq = "".join(f'<details class="qa"><summary>{esc(q)}{icon("plus")}</summary><p>{esc(a)}</p></details>' for q, a in faqs(l)[:5])
    return (
        f'<section class="hero" aria-labelledby="hero-title"><div class="hero-wall" aria-hidden="true"><div class="wall">{wall}</div></div>'
        f'<div class="wrap hero-in"><p class="pill"><span></span>WEB · SOFTWARE · AI · IT</p><h1 id="hero-title">{rich(c["home_title"])}</h1>'
        f'<p class="hero-lead">{esc(c["home_lead"])}</p><div class="actions">{button(c["see_projects"], href("projects", l))}{button(c["book"], cfg["bookingUrl"], "btn-ghost-light", EXT)}</div>'
        f'<p class="hero-note">{esc(c["hero_wall"])}</p></div></section>'
        f'<div class="wrap facts">{facts}</div>'
        f'<section class="section wrap" aria-labelledby="what">{head(c["what"][0], c["what"][1], c["what"][2], link(c["see_services"], href("services", l))).replace("<h2>", "<h2 id=what>", 1)}<div class="areas">{areas}</div></section>'
        f'<section class="band" aria-labelledby="work"><div class="wrap">{head(c["work"][0], c["work"][1], action=link(c["work"][2], href("projects", l)), cls="on-dark").replace("<h2>", "<h2 id=work>", 1)}'
        f'<div class="rail" data-rail><div class="rail-track" data-rail-track>{work}</div><div class="rail-nav"><button type="button" class="rail-btn" data-rail-prev aria-label="{esc(c["prev"])}">{icon("left")}</button>'
        f'<button type="button" class="rail-btn" data-rail-next aria-label="{esc(c["next"])}">{icon("right")}</button></div></div></div></section>'
        f'<section class="section wrap labs-sec" aria-labelledby="labs">{head(c["labs"][0], c["labs"][1], c["labs"][2], link(c["labs_link"], href("labs", l)), cls="labs-head").replace("<h2>", "<h2 id=labs>", 1)}<div class="products">{products}</div></section>'
        f'<section class="section wrap" aria-labelledby="process">{head(t["process"], c["process_title"]).replace("<h2>", "<h2 id=process>", 1)}{steps_block(c)}</section>'
        f'<section class="section partners-sec" aria-labelledby="partners"><div class="wrap">{head(c["partners"][0], c["partners"][1]).replace("<h2>", "<h2 id=partners>", 1)}</div>{partner_marquee(l, c)}<p class="wrap fine">{esc(c["partners"][2])}</p></section>'
        f'<section class="section wrap" id="pricing" aria-labelledby="pricing-title">{head("IT SUPPORT", c["pricing_title"], t["packagenote"]).replace("<h2>", "<h2 id=pricing-title>", 1)}<div class="plans">{pricing_block(l, t, c, plans(l))}</div></section>'
        f'<section class="section wrap faq-sec" aria-labelledby="faq"><div>{head(c["faq"][0], c["faq"][1], action=link(c["faq"][2], href("about", l, "faq"))).replace("<h2>", "<h2 id=faq>", 1)}</div><div class="qas">{faq}</div></section>'
        + cta(l, t, c))


def intro(kicker, title, lead, l, c, crumb, aside=""):
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{href("index", l)}">{esc(c["home_nav"])}</a><span aria-hidden="true">/</span><span aria-current="page">{esc(crumb)}</span></nav>'
    return (f'<section class="intro wrap{" intro-split" if aside else ""}"><div class="intro-copy">{crumbs}<p class="eyebrow">{esc(kicker)}</p><h1>{rich(title)}</h1>'
            f'<p class="lead">{esc(lead)}</p></div>{aside}</section>')


def page_services(l, t, c):
    svc = services(l)
    groups = {"web": svc[0:3], "it": svc[3:6], "creative": svc[6:8]}
    blocks = ""
    for i, (k, name, desc) in enumerate(c["families"]):
        if k == "ai":
            body = (f'<div class="svc-ai"><p>{esc(t["aiLead"])}</p><p class="svc-agents">{esc(c["ai_agents"])}</p><div class="svc-guard">{icon("shield")}<div><strong>{esc(t["aiguard"])}</strong>'
                    f'<p>{esc(t["aiguardbody"])}</p></div></div>{button(c["discuss"], href("contact", l) + "?service=" + quote(name), "btn-outline")}</div>')
        else:
            body = "".join(
                f'<details class="svc"><summary><span class="svc-n">{svc.index(s) + 1:02d}</span><span class="svc-t">{esc(s["title"])}</span>{icon("plus")}</summary>'
                f'<div class="svc-body"><p>{esc(s["text"])}</p><ul>' + "".join(f"<li>{esc(x)}</li>" for x in s["items"]) + "</ul>"
                + (f'<p class="svc-result">{esc(s["result"])}</p>' if s["result"] else "")
                + f'{link(c["discuss"], href("contact", l) + "?service=" + quote(s["title"]))}</div></details>' for s in groups[k])
        blocks += (f'<section class="family" id="{k}" aria-labelledby="fam-{k}"><div class="family-head"><p class="family-n">0{i + 1}</p><h2 id="fam-{k}">{esc(name)}</h2><p>{esc(desc)}</p></div>'
                   f'<div class="family-body">{body}</div></section>')
    aside = '<figure class="intro-art art-stack" aria-hidden="true"><img src="assets/projects/rata-solar-720.webp" width="720" height="450" alt=""><img src="assets/labs/slide-kraken-os.webp" width="760" height="396" alt=""></figure>'
    return (intro(c["nav"][0][1].upper(), c["services_title"], t["servicelead"], l, c, c["nav"][0][1], aside) + f'<div class="wrap families">{blocks}</div>'
            f'<section class="section wrap" id="pricing" aria-labelledby="pricing-title">{head("IT SUPPORT", c["pricing_title"], t["packagenote"]).replace("<h2>", "<h2 id=pricing-title>", 1)}<div class="plans">{pricing_block(l, t, c, plans(l))}</div></section>'
            f'<section class="section wrap" aria-labelledby="process">{head(t["process"], c["process_title"]).replace("<h2>", "<h2 id=process>", 1)}{steps_block(c)}</section>' + cta(l, t, c))


def page_projects(l, t, c):
    rows = ""
    for i, p in enumerate(PROJECTS):
        url = p["final"] or p["url"]
        rows += (f'<article class="case{" case-flip" if i % 2 else ""}"><a class="case-shot" href="{esc(url)}"{EXT} tabindex="-1" aria-hidden="true">'
                 f'<img src="assets/projects/{p["key"]}-1440.webp" srcset="assets/projects/{p["key"]}-720.webp 720w, assets/projects/{p["key"]}-1440.webp 1440w" sizes="(max-width:800px) 100vw, 58vw" width="1440" height="900" alt=""{" loading=lazy" if i else ""} decoding="async"></a>'
                 f'<div class="case-copy"><p class="case-n">0{i + 1} / 0{len(PROJECTS)}</p><p class="proj-cat">{esc(tr(l, *p["category"]))}</p><h2>{esc(p["name"])}</h2><p>{esc(tr(l, *p["text"]))}</p>'
                 f'<a class="btn btn-outline" href="{esc(url)}"{EXT}>{esc(c["open_project"])}{A}<span class="sr"> — {esc(p["name"])} ({esc(c["new_tab"])})</span></a></div></article>')
    chips = ["Web", "Web App", "Windows", "Android", "iOS", "Dashboard", "AI", "E-commerce", "Booking", "CRM", "POS", "Inventory", "API", "Portal"]
    return (intro(c["projects_kicker"], c["work"][1], t["projectsLead"], l, c, c["nav"][1][1]) + f'<div class="wrap cases">{rows}</div>'
            f'<section class="section wrap" aria-labelledby="caps">{head(c["capabilities"][0], c["capabilities"][1]).replace("<h2>", "<h2 id=caps>", 1)}<div class="chips">'
            + "".join(f'<a class="chip" href="{href("contact", l)}?service={quote(x)}">{esc(x)}{A}</a>' for x in chips) + "</div></section>" + cta(l, t, c))


def page_labs(l, t, c):
    rows = ""
    for i, p in enumerate(c["products"]):
        actions = ""
        if p["site"]:
            actions += f'<a class="btn btn-green" href="https://{p["site"]}/"{EXT}><span class="sr">{esc(c["official"])}: </span>{p["site"]}{A}</a>'
        actions += button(c["demo"] if p["site"] else c["ask"], href("contact", l) + "?service=" + quote(p["service"]), "btn-outline")
        note = f'<p class="fine">{esc(c["aura_preview"])}</p>' if not p["site"] else ""
        tagline = f'<p class="product-tag" lang="en">{esc(p["tagline"])}</p>' if p["tagline"] else ""
        logo = '<img class="kraken-logo" src="assets/labs/kraken-logo.png" width="505" height="136" alt="">' if p["site"] else ""
        rows += (f'<article class="lab{" lab-flip" if i % 2 else ""} lab-{p["key"]}" id="{p["key"]}"><div class="lab-shot">{logo}<img src="assets/{p["image"]}" width="{p["size"][0]}" height="{p["size"][1]}" alt="{esc(p["name"])}"{" loading=lazy" if i else ""}></div>'
                 f'<div class="lab-copy"><p class="lab-kind">0{i + 1} / {esc(p["kind"])}</p><h2>{esc(p["name"])}</h2>{tagline}<p>{esc(p["text"])}</p>'
                 f'<ul class="ticks">' + "".join(f"<li>{esc(x)}</li>" for x in p["points"]) + f'</ul><div class="actions">{actions}</div>{note}</div></article>')
    return (f'<div class="labs-page">' + intro(c["labs_kicker"], c["labs"][1], c["labs"][2], l, c, c["nav"][2][1]) + f'</div><div class="wrap labs-rows">{rows}<p class="fine">{esc(c["product_note"])}</p></div>' + cta(l, t, c))


def page_about(l, t, c):
    aside = (f'<figure class="quote"><span class="quote-mark" aria-hidden="true">“</span><blockquote>{rich(c["quote"])}</blockquote>'
             f'<figcaption>IT Department · {esc(t["location"])}</figcaption></figure>')
    values = "".join(f'<article class="value"><p class="value-n">0{i + 1}</p><h3>{esc(a)}</h3><p>{esc(b)}</p></article>' for i, (a, b) in enumerate(c["values"]))
    people = (f'<div class="people"><p class="eyebrow">IT DEPARTMENT</p><h2>{rich(c["people"][0])}</h2><p>{esc(c["people"][1])}</p>'
              f'<ul class="people-chips">' + "".join(f"<li>{esc(x)}</li>" for x in c["people"][2]) + "</ul></div>")
    faq = "".join(f'<details class="qa"><summary>{esc(q)}{icon("plus")}</summary><p>{esc(a)}</p></details>' for q, a in faqs(l))
    return (intro(c["about_kicker"], c["about_title"], t["aboutLead"], l, c, c["nav"][3][1], aside)
            + f'<section class="section wrap" aria-labelledby="values">{head("IT DEPARTMENT", c["values_title"]).replace("<h2>", "<h2 id=values>", 1)}<div class="values">{values}</div></section>'
            + f'<section class="section wrap about-process"><div>{head(t["process"], c["process_title"])}{steps_block(c)}</div>{people}</section>'
            + f'<section class="section wrap faq-sec" id="faq" aria-labelledby="faq-title"><div>{head(c["faq"][0], c["faq"][1]).replace("<h2>", "<h2 id=faq-title>", 1)}</div><div class="qas">{faq}</div></section>' + cta(l, t, c))


def page_contact(l, t, c):
    urls = [cfg["bookingUrl"], wa(l), "mailto:" + cfg["email"]]
    channels = "".join(f'<a class="channel" href="{esc(u)}"{EXT if u.startswith("http") else ""}><span class="fact-icon">{icon(ic)}</span><h2>{esc(a)}</h2><p>{esc(b)}</p>{A}</a>'
                       for (ic, a, b), u in zip(c["channels"], urls))
    fams = [n for _, n, _ in c["families"]] + ["Kraken OS", "Kraken Communications", "AURA"]
    opts = "".join(f"<option>{esc(x)}</option>" for x in fams)
    form = (f'<form class="form" action="{esc(cfg["formEndpoint"])}" method="post" data-form data-sending="{esc(c["sending"])}" data-success="{esc(c["success"])}" data-failure="{esc(c["failure"])}">'
            f'<input type="hidden" name="source" value="IT Department / opus / {l}"><input type="text" name="_gotcha" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">'
            f'<div class="form-row"><label>{esc(t["name"])}<input name="name" autocomplete="name" required maxlength="100"></label><label>{esc(t["email"])}<input name="email" type="email" autocomplete="email" required maxlength="180"></label></div>'
            f'<div class="form-row"><label>{esc(c["company"])}<input name="company" autocomplete="organization" maxlength="150"></label><label>{esc(c["phone"])}<input name="phone" type="tel" autocomplete="tel" maxlength="60"></label></div>'
            f'<label>{esc(t["interest"])}<select name="service" data-service><option value="">{esc(t["choose"])}</option>{opts}</select></label>'
            f'<label>{esc(t["message"])}<textarea name="message" rows="5" required maxlength="3000" placeholder="{esc(t["placeholder"])}"></textarea></label>'
            f'<p class="fine">{esc(c["formnote"])} <a href="../privacy{SUFFIX[l]}.html">{esc(t["privacy"])}{A}</a></p>'
            f'<div class="form-end"><button class="btn" type="submit">{esc(c["send"])}{A}</button><p class="form-status" role="status" aria-live="polite"></p></div></form>')
    side = (f'<div class="contact-side"><p class="eyebrow">IT DEPARTMENT</p><h2>{esc(t["write"])}</h2><ul class="foot-contact on-light"><li>{icon("mail")}<a href="mailto:{cfg["email"]}">{cfg["email"]}</a></li>'
            f'<li>{icon("phone")}<a href="tel:+{cfg["phoneDigits"]}">{cfg["phoneDisplay"]}</a></li><li>{icon("clock")}<span>{esc(t["hours"])}</span></li><li>{icon("pin")}<span>{esc(t["location"])}</span></li></ul>'
            f'<a class="map" href="https://www.google.com/maps/search/?api=1&amp;query=42.655800066393724%2C21.151119141173435"{EXT}>{icon("pin")}<strong>{esc(t["location"])}</strong><span>{esc(c["map"])}{A}</span></a></div>')
    return (intro(c["nav"][4][1].upper(), c["contact_title"], t["contactLead"], l, c, c["nav"][4][1]) + f'<div class="wrap channels">{channels}</div>'
            f'<section class="section wrap contact-grid" id="write">{side}<div class="form-card"><h2>{rich(c["form_title"])}</h2>{form}</div></section>')


PAGES = {"index": page_home, "services": page_services, "projects": page_projects, "labs": page_labs, "about": page_about, "contact": page_contact}
DESC = {
    "index": lambda l, t, c: c["home_lead"], "services": lambda l, t, c: t["servicelead"], "projects": lambda l, t, c: t["projectsLead"],
    "labs": lambda l, t, c: c["labs"][2] + " Kraken OS, Kraken Communications, AURA.", "about": lambda l, t, c: t["aboutLead"], "contact": lambda l, t, c: t["contactLead"]}
OG = {"sq": "sq_AL", "en": "en_US", "de": "de_DE"}


def document(page, l):
    t, c = T[l], C(l)
    body = PAGES[page](l, t, c)
    title = f'{c["titles"][page]} | IT Department'
    desc = DESC[page](l, t, c)
    url = f"{BASE_URL}/{href(page, l)}"
    alts = "".join(f'<link rel="alternate" hreflang="{x}" href="{BASE_URL}/{href(page, x)}">' for x in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/{href(page, "sq")}">'
    og = (f'<meta property="og:type" content="website"><meta property="og:site_name" content="IT Department"><meta property="og:title" content="{esc(title)}">'
          f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{OG[l]}">'
          f'<meta property="og:image" content="{BASE_URL}/assets/brand/og-{l}.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">')
    html = (f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>'
            f'<meta name="description" content="{esc(desc)}"><meta name="robots" content="noindex,follow"><meta name="theme-color" content="#1c1a17"><link rel="canonical" href="{url}">{alts}{og}'
            f'<link rel="icon" href="assets/brand/favicon.png"><link rel="apple-touch-icon" href="assets/brand/logo-shield.png">'
            f'<link rel="preload" href="assets/fonts/fraunces-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>'
            f'<link rel="preload" href="assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>'
            f'<link rel="stylesheet" href="assets/opus.css"><script src="assets/opus.js" defer></script></head>'
            f'<body data-page="{page}">{header(page, l, t, c)}<main id="main">{body}</main>{footer(l, t, c)}</body></html>')
    for x in LANGS:
        html = html.replace("{lang_" + x + "}", href(page, x))
    return html


def copy_assets():
    a = OUT / "assets"
    shutil.rmtree(OUT, ignore_errors=True)
    (a / "fonts").mkdir(parents=True)
    s = V2 / "site" / "assets"
    for sub in ["projects", "partners"]:
        shutil.copytree(s / sub, a / sub)
    for f in ["labs/slide-kraken-os.webp", "labs/slide-communications.webp", "labs/aura-emblem.svg", "labs/kraken-logo.png", "brand/favicon.png", "brand/logo-shield.png",
              "brand/logo-original.png", "brand/banner-texture.webp", "brand/og-sq.jpg", "brand/og-en.jpg", "brand/og-de.jpg", "creative/nexus-brandbook.webp"]:
        (a / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s / f, a / f)
    for f in ["manrope-latin-wght-normal.woff2", "manrope-latin-ext-wght-normal.woff2", "manrope-OFL.txt"]:
        shutil.copy2(s / "fonts" / f, a / "fonts" / f)
    for f in (V2 / "theme-m" / "fonts").iterdir():
        shutil.copy2(f, a / "fonts" / f.name)
    shutil.copy2(V2 / "theme-m" / "logo-ink.png", a / "logo-ink.png")
    for f in ["opus.css", "opus.js"]:
        shutil.copy2(HERE / "assets" / f, a / f)


def main():
    copy_assets()
    n = 0
    for l in LANGS:
        for page in PAGES:
            (OUT / href(page, l)).write_text(document(page, l), encoding="utf-8")
            n += 1
    print(f"Built {n} pages into {OUT}")


if __name__ == "__main__":
    main()
