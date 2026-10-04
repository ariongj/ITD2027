# -*- coding: utf-8 -*-
"""Generate the social share images (Open Graph, 1200x630) for each language.

    py build/og.py

Writes assets/brand/og-image.png (Albanian, the default), og-image-en.png and
og-image-de.png. The layout is plain HTML/CSS rendered by headless Chrome or
Edge, so it uses the site's own font, logo and colours. The text comes from
ui.ogTitle / ui.ogSub / ui.ogEyebrow in the content files; re-run after editing them.
"""
import html
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_sq import L as SQ  # noqa: E402
from content_en import L as EN  # noqa: E402
from content_de import L as DE  # noqa: E402
from templates import OG_FILES  # noqa: E402

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def find_browser():
    for b in BROWSERS:
        if os.path.isabs(b) and os.path.exists(b):
            return b
        found = shutil.which(b)
        if found:
            return found
    raise SystemExit("No Chrome/Edge found. Install one, or edit BROWSERS in build/og.py.")


def uri(rel):
    return pathlib.Path(ROOT, rel).resolve().as_uri()


def page(L):
    first, second = L["ui"]["ogTitle"], L["ui"]["ogSub"]
    chips = [label for label, _ in L["ui"]["footerServiceLinks"]][:4]
    chip_html = "".join(f"<li>{html.escape(c)}</li>" for c in chips)
    bars = "".join(f'<i style="height:{h}%"></i>' for h in (38, 52, 46, 64, 58, 74, 88))
    return f"""<!DOCTYPE html><html lang="{L['lang']}"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Instrument Sans";font-weight:400 700;src:url("{uri('assets/fonts/instrument-sans-latin-wght-normal.woff2')}") format("woff2")}}
@font-face{{font-family:"Instrument Sans";font-weight:400 700;src:url("{uri('assets/fonts/instrument-sans-latin-ext-wght-normal.woff2')}") format("woff2");unicode-range:U+0100-02BA}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{font-family:"Instrument Sans",system-ui,sans-serif;background:#f7f6f3;color:#141417;position:relative}}
.edge{{position:absolute;left:0;top:0;bottom:0;width:10px;background:#e00000}}
.copy{{position:absolute;left:84px;top:72px;width:640px}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:600;font-size:28px;letter-spacing:-.01em}}
.brand img{{width:52px;height:52px}}
.eyebrow{{margin:46px 0 18px;font:600 17px/1.2 Consolas,"SF Mono",Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;color:#d40000}}
h1{{margin:0;font-size:60px;line-height:1.04;letter-spacing:-.035em;font-weight:620;max-width:620px}}
.sub{{margin:16px 0 0;font-size:34px;line-height:1.2;letter-spacing:-.02em;font-weight:500;color:#55575f;max-width:620px}}
ul{{position:absolute;left:84px;bottom:64px;margin:0;padding:0;list-style:none;display:flex;gap:10px;flex-wrap:nowrap;width:760px}}
li{{padding:9px 16px;border:1.5px solid rgba(20,20,23,.14);border-radius:999px;background:#fff;font-size:18px;font-weight:500;color:#33353c}}
.url{{position:absolute;right:64px;bottom:72px;font:600 20px Consolas,"SF Mono",Menlo,monospace;color:#141417}}
.mock{{position:absolute;right:-60px;top:110px;width:420px;border:1.5px solid rgba(20,20,23,.1);border-radius:18px;background:#fff;box-shadow:0 30px 60px -28px rgba(20,20,23,.35);overflow:hidden}}
.bar{{display:flex;gap:7px;padding:13px 16px;background:#efede8;border-bottom:1.5px solid rgba(20,20,23,.08)}}
.bar i{{width:11px;height:11px;border-radius:50%;background:rgba(20,20,23,.18)}}
.body{{padding:24px 24px 28px;display:grid;gap:12px}}
.l{{height:14px;border-radius:7px;background:#141417;width:70%}}
.t{{height:8px;border-radius:4px;background:rgba(20,20,23,.16)}}
.cta{{width:110px;height:28px;border-radius:8px;background:#e00000;margin-top:8px}}
.panel{{position:absolute;right:250px;top:330px;width:230px;padding:18px 20px;border-radius:16px;background:#fff;border:1.5px solid rgba(20,20,23,.1);box-shadow:0 26px 50px -24px rgba(20,20,23,.35)}}
.bars{{display:flex;align-items:flex-end;gap:7px;height:62px}}
.bars i{{flex:1;border-radius:4px 4px 0 0;background:rgba(20,20,23,.16)}}
.bars i:last-child{{background:#e00000}}
</style></head><body>
<div class="edge"></div>
<div class="copy">
<div class="brand"><img src="{uri('assets/brand/logo-shield-108.png')}" alt="">IT Department</div>
<p class="eyebrow">{html.escape(L['ui']['ogEyebrow'])}</p>
<h1>{html.escape(first)}</h1>
<p class="sub">{html.escape(second)}</p>
</div>
<div class="mock"><div class="bar"><i></i><i></i><i></i></div><div class="body"><div class="l"></div><div class="t" style="width:88%"></div><div class="t" style="width:62%"></div><div class="cta"></div></div></div>
<div class="panel"><div class="bars">{bars}</div></div>
<ul>{chip_html}</ul>
<div class="url">itdks.tech</div>
</body></html>"""


def main():
    browser = find_browser()
    work = tempfile.mkdtemp(prefix="itd-og-")
    profile = os.path.join(work, "profile")
    try:
        for L in (SQ, EN, DE):
            src = os.path.join(work, f"og-{L['lang']}.html")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(page(L))
            out = os.path.join(ROOT, "assets", "brand", OG_FILES[L["lang"]])
            cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                   "--no-default-browser-check", "--allow-file-access-from-files", f"--user-data-dir={profile}",
                   "--force-device-scale-factor=1", "--window-size=1200,630", "--virtual-time-budget=4000",
                   f"--screenshot={out}", pathlib.Path(src).as_uri()]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            print(f"  {OG_FILES[L['lang']]:<18} {os.path.getsize(out):>8,} B")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
