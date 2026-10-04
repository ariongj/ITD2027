# -*- coding: utf-8 -*-
"""Build the static site into the parent folder.

    py build/build.py

Reads content_sq.py / content_en.py / content_de.py and templates.py, writes
37 HTML files (12 pages x 3 languages + 404) plus sitemap.xml next to this
folder. Safe to run repeatedly.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_sq import L as SQ  # noqa: E402
from content_en import L as EN  # noqa: E402
from content_de import L as DE  # noqa: E402
import templates as T  # noqa: E402

ALL = {"sq": SQ, "en": EN, "de": DE}


def write(name, text):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return len(text.encode("utf-8"))


def main():
    total = 0
    count = 0
    for lang, L in ALL.items():
        for key in T.PAGE_ORDER:
            name = T.filename(L, key)
            size = write(name, T.render(L, ALL, key))
            total += size
            count += 1
            print(f"  {name:<22} {size:>7,} B")
    size = write("404.html", T.render_404(ALL))
    print(f"  {'404.html':<22} {size:>7,} B")
    size = write("sitemap.xml", T.sitemap(ALL))
    print(f"  {'sitemap.xml':<22} {size:>7,} B")
    print(f"Built {count + 1} pages ({total / 1024:.0f} KB of HTML) into {OUT}")


if __name__ == "__main__":
    main()
