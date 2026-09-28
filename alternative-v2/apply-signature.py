from pathlib import Path
p=Path(r"C:\Users\A\Documents\WebSite ITD\alternative-v2\build.py")
s=p.read_text(encoding="utf-8")
start=s.index("def home(l,t):")
end=s.index("def detail(",start)
new=Path(r"C:\Users\A\Documents\WebSite ITD\alternative-v2\signature-home.py").read_text(encoding="utf-8-sig")
s=s[:start]+new+"\n"+s[end:]
old='def ending(l,t): return f\'<section class="ending wrap">'
s=s.replace(old,'def ending(l,t): return f\'<div class="ending-band"><section class="ending wrap">')
s=s.replace('{button(t["talk"],route("contact",l))}</div></section>\'','{button(t["talk"],route("contact",l))}</div></section></div>\'')
p.write_text(s,encoding="utf-8")

