# -*- coding: utf-8 -*-
"""Local preview server that mimics the Hostinger .htaccess clean URLs.

    py build/serve.py 8765          only this computer: http://localhost:8765
    py build/serve.py 8765 --lan    also phones/laptops on the same Wi-Fi
    py build/serve.py 8765 --prod-headers
                                    also send the security headers from .htaccess
                                    (Content-Security-Policy etc.), to test that
                                    nothing on the pages is blocked by them

/            -> index.html      /en -> index-en.html      /de -> index-de.html
/services-en -> services-en.html   unknown -> 404.html (status 404)

--lan makes the preview reachable by anyone on your local network while it
runs (Windows may ask to allow Python through the firewall). Stop it with
Ctrl+C when you are done.
"""
import os
import socket
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PORT = int(ARGS[0]) if ARGS else 8765
LAN = "--lan" in sys.argv
PROD_HEADERS = []
if "--prod-headers" in sys.argv:
    import re as _re
    with open(os.path.join(ROOT, ".htaccess"), encoding="utf-8") as _fh:
        for _line in _fh:
            _m = _re.match(r'\s*Header always set ([\w-]+) "(.*)"\s*$', _line)
            if _m and _m.group(1) != "Strict-Transport-Security":  # HSTS means nothing on http://localhost
                PROD_HEADERS.append((_m.group(1), _m.group(2).replace(" upgrade-insecure-requests", "")))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if clean in ("/", ""):
            clean = "/index.html"
        elif clean == "/en":
            clean = "/index-en.html"
        elif clean == "/de":
            clean = "/index-de.html"
        elif clean == "/stats/admin":
            clean = "/stats/admin.html"
        full = super().translate_path(clean)
        if not os.path.exists(full) and not clean.endswith(".html") and os.path.exists(full + ".html"):
            return full + ".html"
        return full

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = os.path.join(ROOT, "404.html")
            if os.path.exists(page):
                with open(page, "rb") as fh:
                    body = fh.read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        for name, value in PROD_HEADERS:
            self.send_header(name, value)
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


def lan_addresses():
    found = set()
    try:
        # The address the OS would use to reach the internet is the LAN one.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.0.2.1", 80))  # documentation address, no packet is sent for UDP connect
        found.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if not ip.startswith("127."):
                found.add(ip)
    except OSError:
        pass
    return sorted(found)


if __name__ == "__main__":
    Handler.extensions_map.update({".woff2": "font/woff2", ".webp": "image/webp", ".webmanifest": "application/manifest+json"})
    host = "0.0.0.0" if LAN else "127.0.0.1"
    print(f"Serving {ROOT}")
    print(f"  This computer:   http://localhost:{PORT}")
    if LAN:
        for ip in lan_addresses():
            print(f"  Same Wi-Fi:      http://{ip}:{PORT}   (open this on a phone)")
    if PROD_HEADERS:
        print("  Sending production headers: " + ", ".join(n for n, _ in PROD_HEADERS))
    sys.stdout.flush()
    ThreadingHTTPServer((host, PORT), Handler).serve_forever()
