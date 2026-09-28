from pathlib import Path
import ast
base=Path(__file__).resolve().parent
path=base/"build.py"
src=path.read_text(encoding="utf-8-sig")
overrides=(base/"studio-components.py").read_text(encoding="utf-8-sig")
replacement={n.name:ast.get_source_segment(overrides,n) for n in ast.parse(overrides).body if isinstance(n,ast.FunctionDef)}
lines=src.splitlines(keepends=True)
for n in reversed(ast.parse(src).body):
 if isinstance(n,ast.FunctionDef) and n.name in replacement:
  lines[n.lineno-1:n.end_lineno]=[replacement[n.name]+"\n"]
src="".join(lines)
src=src.replace('"sq":"Biznesi yt. I lidhur. I mbështetur.","en":"Your business. Connected. Supported.","de":"Ihr Unternehmen. Vernetzt. Unterstützt."','"sq":"Ide të mëdha. Zgjidhje reale.","en":"Big ideas. Real solutions.","de":"Große Ideen. Echte Lösungen."')
src=src.replace('content="#0a0b0e"','content="#ffffff"')
ast.parse(src)
path.write_text(src,encoding="utf-8")
js=base/"site/assets/site.js"
text=js.read_text(encoding="utf-8-sig")
text=text.replace("mobile.matches?'horizontal':'vertical'","'horizontal'")
js.write_text(text,encoding="utf-8")

