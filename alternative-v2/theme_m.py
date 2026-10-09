"""ITD2027/M — the same site in the style of the SELCA site (build with ITD_THEME=m).

Only the home page and the header change in markup: a dark top bar, a full-bleed hero slideshow with
the headline over the picture, and a floating bar with four facts. Everything else is the same content,
restyled by assets/m/m.css (Fraunces and Manrope, cream and wine red)."""
_base_header=header
_base_home=home

M_ICONS={
 'calendar':'<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4m8-4v4M3 10h18"/>',
 'route':'<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5"/>',
 'shield':'<path d="m12 3 8 3v6c0 5-8 9-8 9S4 17 4 12V6Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/>',
 'phone':'<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'}
def micon(name): return '<svg class="m-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+M_ICONS[name]+'</svg>'
def accent(text,word):
 assert word in text,(text,word)
 return esc(text).replace(esc(word),f'<em>{esc(word)}</em>',1)

def topbar(l,t):
 return (f'<aside class="m-topbar" aria-label="{t["contact"]}"><div class="wrap m-topbar-inner"><a href="tel:+{cfg["phoneDigits"]}">{micon("phone")}{cfg["phoneDisplay"]}</a>'
  f'<p>{micon("clock")}{t["hours"]} · {t["location"]}</p><a href="mailto:{cfg["email"]}">{micon("mail")}{cfg["email"]}</a></div></aside>')

def header(page,l,t):
 h=_base_header(page,l,t)
 if THEME!='m': return h
 # Light header with dark letters; the home page keeps the white logo over the picture.
 if page not in ('index','creative','ai-agents'): h=h.replace('src="assets/brand/logo-original.png"','src="assets/m/logo-ink.png"',1)
 return h.replace('<header class="header">',topbar(l,t)+'<header class="header">',1)

def m_slides(l,t):
 c=copy(l); creative=tr(l,['Ide që duken.','Mesazhe që mbeten.'],['Ideas you see.','Messages that stay.'],['Ideen, die auffallen.','Botschaften, die bleiben.'])
 return [
  {'theme':'itd','image':'hero-itd.webp','eyebrow':'WEB / SOFTWARE / AI / IT','tag':'h1','lang':'','title':accent(c['home'],tr(l,'punën','work','Arbeit')),
   'text':tr(l,'Faqe interneti, softuer dhe automatizim me AI. Nga ideja te një zgjidhje që ekipi yt mund ta përdorë.','Websites, software and AI automation. From an idea to a solution your team can use.','Websites, Software und KI-Automatisierung. Von der Idee zu einer Lösung, die Ihr Team im Alltag nutzen kann.'),
   'buttons':[(c['see'],route('services',l),'',''),(c['book'],cfg['bookingUrl'],'outline-light','target="_blank" rel="noopener noreferrer"')]},
  {'theme':'kraken','image':'hero-kraken.webp','eyebrow':'ITD LABS · KRAKEN OS','tag':'h2','lang':en_attr(l),'title':'Many arms. <em>One brain.</em>',
   'text':tr(l,'Një platformë modulare për njerëzit, klientët, financat dhe punën e përditshme.','A modular platform for people, customers, finance and daily work.','Eine modulare Plattform für Menschen, Kunden, Finanzen und tägliche Arbeit.'),
   'buttons':[(tr(l,'Shiko produktin','Explore product','Produkt ansehen'),route('krakenos',l),'',''),(c['demo'],route('contact',l)+'?service=KrakenOS&intent=demo','outline-light','')]},
  {'theme':'creative','image':'hero-creative.webp','eyebrow':'IT DEPARTMENT / CREATIVE STUDIO','tag':'h2','lang':'','title':f'{esc(creative[0])} <em>{esc(creative[1])}</em>',
   'text':t['creativeLead'],
   'buttons':[(tr(l,'Shiko portofolin','View portfolio','Portfolio ansehen'),route('creative',l)+'#portfolio','',''),(t['talk'],route('contact',l),'outline-light','')]}]

def m_hero(l,t):
 slides=m_slides(l,t); n=len(slides); html=''; dots=''
 for i,s in enumerate(slides):
  buttons=''.join(button(label,href,extra,style) for label,href,style,extra in s['buttons'])
  html+=(f'<div class="slide m-slide m-slide-{s["theme"]}{" is-active" if i==0 else ""}" role="group" aria-roledescription="{tr(l,"slajd","slide","Folie")}" aria-label="{i+1} / {n}" data-slide>'
   f'<img class="m-slide-bg" src="assets/m/{s["image"]}" width="1920" height="1080" alt=""{"" if i==0 else " loading=lazy"} decoding="async">'
   f'<div class="wrap m-slide-copy"><p class="m-pill"><span></span>{s["eyebrow"]}</p><{s["tag"]} class="m-display"{s["lang"]}>{s["title"]}</{s["tag"]}><p class="m-lead">{s["text"]}</p><div class="actions">{buttons}</div></div></div>')
  dots+=f'<button type="button" class="slider-dot" aria-controls="hero-slides" aria-label="{tr(l,"Slajdi","Slide","Folie")} {i+1}"{" aria-current=true" if i==0 else ""}><span class="slider-bar"><span class="slider-fill"></span></span></button>'
 pause=tr(l,('Ndalo ndërrimin automatik','Nis ndërrimin automatik'),('Pause automatic rotation','Start automatic rotation'),('Automatischen Wechsel anhalten','Automatischen Wechsel starten'))
 arrows=(f'<button type="button" class="slider-pause" aria-label="{pause[0]}" data-pause="{pause[0]}" data-play="{pause[1]}"><span aria-hidden="true"></span></button>'
  f'<button type="button" class="slider-prev" aria-controls="hero-slides" aria-label="{tr(l,"Slajdi i mëparshëm","Previous slide","Vorherige Folie")}"><span aria-hidden="true">‹</span></button>'
  f'<button type="button" class="slider-next" aria-controls="hero-slides" aria-label="{tr(l,"Slajdi i radhës","Next slide","Nächste Folie")}"><span aria-hidden="true">›</span></button>')
 return (f'<section class="hero-slider m-hero" aria-roledescription="{tr(l,"prezantim me slajde","carousel","Karussell")}" aria-label="IT Department" data-slider>'
  f'<div class="slides" id="hero-slides" aria-live="off">{html}</div>'
  f'<div class="slider-controls m-controls" hidden><div class="wrap m-controls-inner"><span class="m-counter" aria-hidden="true"><b data-counter>01</b> / 0{n}</span>'
  f'<div class="slider-dots">{dots}</div><div class="slider-arrows">{arrows}</div></div></div></section>')

def m_features(l,t):
 items=tr(l,[('calendar','Takim 30-minutësh','Online, në kohën që të përshtatet.'),('route','Plan i qartë','Fillojmë me një bisedë, pastaj me një plan.'),('shield','Mbështetje IT nga €99','Paketa mujore për sistemet e biznesit.'),('globe','Shqip · English · Deutsch','Bashkëpunim në tri gjuhë.')],
  [('calendar','30-minute meeting','Online, at a time that suits you.'),('route','A clear plan','First a conversation, then a clear plan.'),('shield','IT support from €99','Monthly plans for your business systems.'),('globe','Shqip · English · Deutsch','Working together in three languages.')],
  [('calendar','30-Minuten-Gespräch','Online, zu einem passenden Termin.'),('route','Ein klarer Plan','Zuerst ein Gespräch, dann ein klarer Plan.'),('shield','IT-Support ab 99 €','Monatliche Pakete für Ihre Systeme.'),('globe','Shqip · English · Deutsch','Zusammenarbeit in drei Sprachen.')])
 links=[cfg['bookingUrl'],route('services',l)+'#process','#packages','']
 cells=''
 for (ic,title,text),href in zip(items,links):
  inner=f'<span class="m-feature-icon">{micon(ic)}</span><span><strong>{title}</strong><span>{text}</span></span>'
  extra=' target="_blank" rel="noopener noreferrer"' if href.startswith('https://') else ''
  cells+=f'<a class="m-feature" href="{esc(href)}"{extra}>{inner}</a>' if href else f'<div class="m-feature">{inner}</div>'
 return f'<div class="wrap m-features">{cells}</div>'

def home(l,t):
 if THEME!='m': return _base_home(l,t)
 old=_old_home(l,t); tail=old[old.index('</section>')+10:]
 return m_hero(l,t)+m_features(l,t)+priority_services(l,t)+tail
