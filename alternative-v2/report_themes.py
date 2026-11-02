"""ITD Themes in the main site (ITD_Themes_Integrimi_ne_Webfaqe_SQ_EN_DE_01-11-2026.pdf), main version only.

The catalogue itself lives at themes.itdks.tech; this layer only leads to it:
- Home: a section after the four service areas and before the projects (three models; on phones one large, two compact).
- Web & software: a dark block after the three benefits and before "Nga nevoja reale". Services: a text link at the web service.
- Footer: "Modele website" in the Company column, on every page and language. The main menu stays as it is.

Cards and buttons are plain links that open in the same tab, in the visitor's language. The three screenshots are the
ones the report uses, taken from the catalogue's demos (assets/themes). 220 models and 20 industries were checked against
the catalogue's own data on 2 November 2026. All three demos are English only, hence "Demo EN" in every language. The texts follow the
report; the EN/DE of "Një drejtim për çdo biznes." and of the note under the dark block are not in it and were translated from SQ."""

THEMES_HOME={'sq':'https://themes.itdks.tech/','en':'https://themes.itdks.tech/en/','de':'https://themes.itdks.tech/de/'}
THEMES_MODEL={'sq':'https://themes.itdks.tech/modeli/{}.html','en':'https://themes.itdks.tech/en/model/{}.html','de':'https://themes.itdks.tech/de/modell/{}.html'}
THEMES_MODELS=[dict(id='t021',name='Monolith House',img='monolith-house',industry=('Arkitekturë','Architecture','Architektur')),
 dict(id='t041',name='Altura Five',img='altura-five',industry=('Hotelieri','Hospitality','Hotellerie')),
 dict(id='t111',name='Lumen Eyewear',img='lumen-eyewear',industry=('Dyqan online','Online shop','Onlineshop'))]
THEMES_FOOTER=('Modele website','Website models','Website-Vorlagen')


def theme_card(m,l,sizes):
 name,industry=m['name'],tr(l,*m['industry'])
 view=tr(l,'Shiko modelin','View model','Vorlage ansehen')
 label=f'{view} {name}, {industry} '+tr(l,'(demo në anglisht)','(demo in English)','(Demo auf Englisch)')
 alt=tr(l,f'Pamje e demos së modelit {name}',f'Screenshot of the {name} demo',f'Screenshot der Demo {name}')
 src=f'assets/themes/{m["img"]}'
 return (f'<a class="th-card" href="{THEMES_MODEL[l].format(m["id"])}" aria-label="{esc(label)}"><span class="th-frame"><span class="th-bar"><i></i><i></i><i></i><b>Demo EN</b></span>'
  f'<img src="{src}-480.webp" srcset="{src}-480.webp 480w, {src}-960.webp 960w" sizes="{sizes}" width="960" height="615" alt="{esc(alt)}" loading="lazy" decoding="async"></span>'
  f'<span class="th-industry">{esc(industry)}</span><strong class="th-name">{esc(name)}</strong><span class="th-view">{esc(view)}</span></a>')


def themes_section(l):
 first,*others=THEMES_MODELS
 cards=lambda items,sizes,cls:''.join(f'<div class="{cls}">{theme_card(m,l,sizes)}</div>' for m in items)
 phone=(f'<div class="th-phone"><p class="th-count">{tr(l,"220 modele · 20 industri","220 models · 20 industries","220 Vorlagen · 20 Branchen")}</p>'
  f'<p class="th-hint">{tr(l,"Vazhdo poshtë për dy pamje të tjera","Scroll for two more ideas","Weitere Ideen beim Scrollen entdecken")}</p>'
  f'<p class="eyebrow">ITD THEMES</p><h3>{tr(l,"Një drejtim për çdo biznes.","A direction for every business.","Eine Richtung für jedes Unternehmen.")}</h3></div>')
 return ('<section class="wrap section th-section">'
  +heading('ITD THEMES',tr(l,'Website-i yt fillon me një ide.','Your website starts with an idea.','Ihre Website beginnt mit einer Idee.'),
   tr(l,'Eksploro 220 modele nga 20 industri. Zgjidh një drejtim dhe ne e përshtatim sipas biznesit tënd.','Explore 220 website models across 20 industries. Choose a direction and we tailor it to your business.','Entdecken Sie 220 Website-Vorlagen für 20 Branchen. Wählen Sie eine Richtung, die wir an Ihr Unternehmen anpassen.'))
  +'<div class="th-grid">'+cards([first],'(max-width:640px) 92vw, 380px','th-main')+phone+cards(others,'(max-width:640px) 46vw, 380px','th-other')+'</div>'
  +'<div class="th-foot">'+button(tr(l,'Eksploro modelet','Explore the models','Vorlagen entdecken'),THEMES_HOME[l],style='th-cta')
  +f'<p class="th-note">{tr(l,"Modele demonstrimi, të personalizueshme për biznesin tënd.","Demo models, ready to be tailored to your business.","Demo-Vorlagen, individuell an Ihr Unternehmen anpassbar.")}</p></div></section>')


def themes_panel(l):
 return ('<section class="wrap section th-service"><div class="th-panel"><p class="eyebrow">ITD THEMES</p>'
  f'<h2>{tr(l,"Gjej një model për biznesin tënd.","Find a model for your business.","Finden Sie eine Vorlage für Ihr Unternehmen.")}</h2>'
  f'<p>{tr(l,"Zgjidh një pikënisje nga koleksioni ynë. Ne përshtatim markën, përmbajtjen dhe funksionet sipas projektit.","Choose a starting point from our collection. We adapt the branding, content and features to your project.","Wählen Sie einen Ausgangspunkt aus unserer Kollektion. Wir passen Design, Inhalte und Funktionen an Ihr Projekt an.")}</p>'
  +button(themes_link_text(l),THEMES_HOME[l],style='th-cta')
  +f'<p class="th-panel-note">{tr(l,"220 modele · 20 industri · Personalizim sipas projektit","220 models · 20 industries · Tailored to your project","220 Vorlagen · 20 Branchen · Anpassung an Ihr Projekt")}</p></div></section>')


def themes_link_text(l): return tr(l,'Gjej një model për biznesin tënd','Find a model for your business','Passende Vorlage finden')


_themes_home=home
def home(l,t):
 html=_themes_home(l,t)
 if THEME=='m': return html
 start=html.index('<section class="wrap pillars r8-areas">')
 end=html.index('</section>',start)+len('</section>')
 assert 'NGA STUDIOJA' in html[end:end+200] or 'FROM THE STUDIO' in html[end:end+200] or 'AUS DEM STUDIO' in html[end:end+200], html[end:end+200]
 return html[:end]+themes_section(l)+html[end:]


_themes_web_software=web_software
def web_software(l,t):
 html=_themes_web_software(l,t)
 if THEME=='m': return html
 marker='<section class="wrap section service-context">'
 assert html.count(marker)==1
 return html.replace(marker,themes_panel(l)+marker,1)


_themes_services=services
def services(l,t):
 html=_themes_services(l,t)
 if THEME=='m': return html
 start=html.index('<details class="service-detail" id="websites">')
 end=html.index('</div></details>',start)
 return html[:end]+f'<a class="text-link th-service-link" href="{THEMES_HOME[l]}">{themes_link_text(l)}</a>'+html[end:]


_themes_footer=footer
def footer(l,t,page='index'):
 html=_themes_footer(l,t,page)
 if THEME=='m': return html
 partners=f'<li><a href="{route("partners",l)}">{dict(zip(PAGES,labels(l)))["partners"]}</a></li>'
 assert html.count(partners)==1
 return html.replace(partners,partners+f'<li class="th-footer-link"><a href="{THEMES_HOME[l]}">{tr(l,*THEMES_FOOTER)}<small>ITD Themes</small></a></li>',1)
