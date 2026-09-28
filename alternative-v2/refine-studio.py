from pathlib import Path
base=Path(__file__).resolve().parent
p=base/"build.py"
s=p.read_text(encoding="utf-8-sig")
s=s.replace('cards=""\n for i,(key,label)', 'cards=""\n caption={"sq":"Identitet / Drejtim artistik","en":"Branding / Art direction","de":"Markenidentität / Gestaltung"}[l]\n for i,(key,label)')
s=s.replace('<p>Branding / Art direction</p>','<p>{caption}</p>')
s=s.replace('"names":["Websites.\\nIdentitet.', '"names":["Faqe web.\\nIdentitet.')
p.write_text(s,encoding="utf-8")
p=base/"site/assets/site.css"
s=p.read_text(encoding="utf-8-sig")
s=s.replace('--red:#ef292f','--red:#e5232b')
s=s.replace('letter-spacing:-.075em','letter-spacing:-.06em;word-spacing:.035em')
s=s.replace('letter-spacing:-.065em','letter-spacing:-.05em')
s=s.replace('.ending-band{background:var(--red)', '.ending-band{background:#dc2028')
s=s.replace('color:#ffe5e5','color:#fff').replace('color:#ffbcbf','color:#fff0f0').replace('color:#ffe1e2','color:#fff')
s += '\n@media(max-width:700px){.hero-services a{min-height:36px;display:flex;align-items:center}.work-section .section-heading{display:flex}.work-caption p{font-size:10px}.work-tag{font-size:9px}.footer-mid nav a,.footer-mid>div a,.footer-bottom nav a{display:inline-flex;align-items:center;min-height:36px}.footer-mid nav{gap:7px 22px}.footer-mid>div{margin-top:13px}.footer-bottom nav{margin-top:9px}}\n'
p.write_text(s,encoding="utf-8")

