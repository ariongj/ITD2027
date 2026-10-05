# -*- coding: utf-8 -*-
"""Edit all website text in Excel: export to texts.xlsx, edit, import back.

    py -X utf8 build/texts.py export [--compare <folder with the previous site>]
    py -X utf8 build/texts.py import [build/texts.xlsx] [--dry]

export  writes build/texts.xlsx: one row per piece of text, with the English,
        Albanian and German side by side. With --compare, two extra columns mark
        the sentences that are new compared with the previous site (for review).
import  reads the workbook and writes every changed cell back into
        content_en.py / content_sq.py / content_de.py. Empty cells are ignored.
        Placeholders such as {plan} or {price} must stay in the text.
        Then run build.py to regenerate the pages.

Only the Albanian, English and German columns are read back; the other columns
are for orientation. Uses only the Python standard library.
"""
import ast
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
XLSX = os.path.join(HERE, "texts.xlsx")
LANGS = [("en", "English"), ("sq", "Albanian"), ("de", "German")]
SKIP_KEYS = {"icon", "href", "id", "slug", "file", "urls", "lang", "locale", "suffix", "anchors", "featured", "langName", "num", "page"}
PAGE_NAMES = {"ui": "All pages", "home": "Home", "services": "Services", "web": "Web & software", "ai": "AI Agents", "projects": "Projects",
              "labs": "ITD Labs", "krakenos": "Kraken OS", "communications": "Kraken Communications",
              "creative": "Creative", "about": "About", "contact": "Contact", "privacy": "Privacy",
              "terms": "Terms", "notfound": "404 page"}
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


# ----------------------------------------------------------- content files
def locate(lang):
    """Return (file bytes, {key: ast.Constant}) for every string in content_<lang>.py."""
    path = os.path.join(HERE, f"content_{lang}.py")
    data = open(path, "rb").read()
    tree = ast.parse(data)
    root = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "L" for t in n.targets))
    found = {}

    def walk(node, path):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    walk(v, path + (k.value,))
        elif isinstance(node, (ast.List, ast.Tuple)):
            for i, v in enumerate(node.elts):
                walk(v, path + (str(i),))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            found[".".join(path)] = node

    walk(root, ())
    return path, data, found


def is_text(key, value):
    parts = key.split(".")
    if any(p in SKIP_KEYS for p in parts):
        return False
    v = value.strip()
    if not v or v.startswith(("/", "http", "#")) or re.fullmatch(r"[\w.-]+\.(webp|png|svg)", v):
        return False
    if re.fullmatch(r"[a-z0-9-]+", v) and parts[-1] in ("0", "1") and len(v) < 12:
        return False  # icon names / page keys inside tuples
    return True


def all_texts():
    langs = {code: locate(code) for code, _ in LANGS}
    keys = [k for k, node in langs["en"][2].items() if is_text(k, node.value)]
    # Texts that exist in one language only (e.g. the German-market note) go right after
    # the key before them in that language, so they sit with their page.
    for code, _ in LANGS[1:]:
        prev = None
        for k, node in langs[code][2].items():
            if not is_text(k, node.value):
                continue
            if k not in keys:
                keys.insert(keys.index(prev) + 1 if prev in keys else len(keys), k)
            prev = k
    rows = []
    for k in keys:
        rows.append({"key": k, **{code: (langs[code][2][k].value if k in langs[code][2] else "") for code, _ in LANGS}})
    return rows, langs


# ------------------------------------------------------------------ export
def norm(s):
    import html as _h
    s = _h.unescape(s).replace("’", "'").replace("“", '"').replace("”", '"').replace("„", '"')
    return re.sub(r"\s+", " ", s.replace("–", "-").replace(" ", " ")).strip().lower()


def corpus(folder, suffix):
    pages = ["index", "services", "ai-agents", "projects", "creative", "about", "contact", "privacy", "terms"]
    text = []
    for p in pages + (["404"] if suffix == "" else []):
        f = os.path.join(folder, f"{p}{suffix}.html")
        if os.path.exists(f):
            raw = io.open(f, encoding="utf-8", errors="replace").read()
            raw = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", raw)
            raw = re.sub(r'(?s)<[^>]+?(?:content|aria-label|placeholder|alt|value|title)="([^"]*)"[^>]*>', r" \1 ", raw)
            text.append(re.sub(r"<[^>]+>", " ", raw))
    return norm(" ".join(text))


def col(i):
    s, i = "", i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path, header, rows, widths):
    def c(ref, text, style):
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(text))
        return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{escape(text)}</t></is></c>'

    last = f"{col(len(header) - 1)}{len(rows) + 1}"
    lines = ['<row r="1">' + "".join(c(f"{col(i)}1", h, 1) for i, h in enumerate(header)) + "</row>"]
    for r, row in enumerate(rows, start=2):
        cells = []
        for i, v in enumerate(row):
            style = 3 if header[i] in ("English", "Albanian", "German") else 2
            cells.append(c(f"{col(i)}{r}", v, style))
        lines.append(f'<row r="{r}">' + "".join(cells) + "</row>")
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             f'<worksheet xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
             '<sheetViews><sheetView workbookViewId="0"><pane xSplit="2" ySplit="1" topLeftCell="C2" activePane="bottomRight" state="frozen"/></sheetView></sheetViews>'
             f'<sheetFormatPr defaultRowHeight="15"/><cols>{cols}</cols><sheetData>{"".join(lines)}</sheetData>'
             f'<autoFilter ref="A1:{last}"/></worksheet>')
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<sheets><sheet name="Texts" sheetId="1" r:id="rId1"/></sheets>'
                f'<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">Texts!$A$1:${col(len(header) - 1)}${len(rows) + 1}</definedName></definedNames>'
                '</workbook>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              f'<styleSheet xmlns="{NS}">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FFEFEDE8"/><bgColor indexed="64"/></patternFill></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="4">'
              '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
              '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
              '<xf numFmtId="49" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
              '</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                     '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                     '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                     '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>')
    wb_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
               '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
               '</Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", styles)
        z.writestr("xl/worksheets/sheet1.xml", sheet)


def export(argv):
    compare = argv[argv.index("--compare") + 1] if "--compare" in argv else None
    rows, _ = all_texts()
    header = ["Page", "Key", "English", "Albanian", "German"]
    widths = [14, 30, 55, 55, 55]
    old = {}
    if compare:
        header += ["Albanian new?", "German new?"]
        widths += [13, 13]
        old = {"sq": corpus(compare, ""), "de": corpus(compare, "-de")}
    out = []
    for r in rows:
        line = [PAGE_NAMES.get(r["key"].split(".")[0], r["key"].split(".")[0]), r["key"], r["en"], r["sq"], r["de"]]
        if compare:
            line += ["" if norm(r["sq"]) in old["sq"] else "yes", "" if norm(r["de"]) in old["de"] else "yes"]
        out.append(line)
    write_xlsx(XLSX, header, out, widths)
    print(f"Wrote {len(out)} texts to {XLSX}")
    if compare:
        print(f"  new vs previous site: {sum(1 for l in out if l[5])} Albanian, {sum(1 for l in out if l[6])} German")


# ------------------------------------------------------------------ import
def read_xlsx(path):
    z = zipfile.ZipFile(path)
    q = lambda tag: f"{{{NS}}}{tag}"  # noqa: E731
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(q("si")):
            parts = []
            for child in si:
                if child.tag == q("t"):
                    parts.append(child.text or "")
                elif child.tag == q("r"):
                    parts.extend(t.text or "" for t in child.findall(q("t")))
            shared.append("".join(parts))
    sheet_path = "xl/worksheets/sheet1.xml"
    try:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rid = wb.find(q("sheets")).find(q("sheet")).get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        for rel in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")):
            if rel.get("Id") == rid:
                target = rel.get("Target").lstrip("/")
                sheet_path = target if target.startswith("xl/") else "xl/" + target
    except (KeyError, AttributeError):
        pass
    table = []
    for row in ET.fromstring(z.read(sheet_path)).find(q("sheetData")).findall(q("row")):
        values = {}
        for c in row.findall(q("c")):
            ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
            idx = 0
            for ch in ref:
                idx = idx * 26 + (ord(ch) - 64)
            t, v = c.get("t"), c.find(q("v"))
            if t == "s":
                val = shared[int(v.text)] if v is not None else ""
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(q("t")))
            elif v is not None and v.text is not None:
                val = v.text
                if t in (None, "n"):
                    try:
                        f = float(val)
                        val = str(int(f)) if f.is_integer() else val
                    except ValueError:
                        pass
            else:
                val = ""
            values[idx - 1] = val
        if values:
            table.append([values.get(i, "") for i in range(max(values) + 1)])
    return table


def do_import(argv):
    args = [a for a in argv if not a.startswith("--")]
    path = args[0] if args else XLSX
    dry = "--dry" in argv
    table = read_xlsx(path)
    header = [h.strip() for h in table[0]]
    if "Key" not in header:
        raise SystemExit("The first row must contain a 'Key' column (use a workbook made by 'texts.py export').")
    key_col = header.index("Key")
    lang_cols = {code: header.index(name) for code, name in LANGS if name in header}
    rows, langs = all_texts()
    current = {r["key"]: r for r in rows}
    edits = {code: [] for code in lang_cols}
    problems = []
    for line in table[1:]:
        key = line[key_col].strip() if key_col < len(line) else ""
        if not key:
            continue
        if key not in current:
            problems.append(f"unknown key {key!r} (row skipped)")
            continue
        for code, ci in lang_cols.items():
            new = line[ci] if ci < len(line) else ""
            old = current[key][code]
            if not new.strip() or new.strip() == old.strip():
                continue
            if sorted(re.findall(r"\{[a-z]+\}", new)) != sorted(re.findall(r"\{[a-z]+\}", old)):
                problems.append(f"{code} {key}: placeholders changed, skipped ({old!r} -> {new!r})")
                continue
            edits[code].append((key, old, new))
    total = 0
    for code, changes in edits.items():
        if not changes:
            continue
        path_py, data, found = langs[code]
        starts = [0]
        for line in data.splitlines(keepends=True):
            starts.append(starts[-1] + len(line))
        spans = []
        for key, old, new in changes:
            node = found[key]
            a = starts[node.lineno - 1] + node.col_offset
            b = starts[node.end_lineno - 1] + node.end_col_offset
            spans.append((a, b, json.dumps(new, ensure_ascii=False).encode("utf-8"), key, old, new))
        for a, b, lit, key, old, new in sorted(spans, reverse=True):
            data = data[:a] + lit + data[b:]
        ast.parse(data)  # never write a file that no longer parses
        if not dry:
            open(path_py, "wb").write(data)
        for _, _, _, key, old, new in spans:
            print(f"  {code.upper()} {key}\n     was: {old}\n     now: {new}")
        total += len(changes)
    for p in problems:
        print("  ! " + p)
    verb = "Would change" if dry else "Changed"
    print(f"{verb} {total} text(s)." + ("" if dry or not total else " Now run: py -X utf8 build/build.py"))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("export", "import"):
        print(__doc__)
        sys.exit(1)
    (export if sys.argv[1] == "export" else do_import)(sys.argv[2:])
