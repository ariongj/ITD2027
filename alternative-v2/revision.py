"""October reports: shared identity, two service landing pages and ITD Labs."""
_old_home=home
_old_services=services
_old_footer=footer
_old_kraken=krakenos
NAV_ORDER=['index','services','projects','partners','itd-labs','creative','ai-agents','about','contact']
PAGES=['index','services','projects','partners','creative','ai-agents','about','contact','itd-labs']
_old_labels=labels
def labels(l): return _old_labels(l)[:-1]+['ITD Labs']
# Fixed English brand lines on Albanian/German pages are marked so screen readers pronounce them in English.
def en_attr(l): return '' if l=='en' else ' lang="en"'
def current(page,target): return ' aria-current="page"' if page==target else ''
# The ITD Labs catalogue and its product pages (menu highlight in ITD Labs green).
LABS_PAGES=['itd-labs','krakenos','kraken-communications','aura']
KRAKEN_LOGO='<img class="product-logo" src="assets/labs/kraken-logo.png" width="505" height="136" alt="{}">'
def official(url,l): return f'<a class="official-link" href="https://{url}/" target="_blank" rel="noopener noreferrer"><span class="sr-only">{tr(l,"Faqja zyrtare:","Official website:","Offizielle Website:")} </span>{url}{A}</a>'

def header(page,l,t):
 nav=''
 for p in NAV_ORDER:
  if p=='itd-labs':
   active=page in LABS_PAGES
   nav+=f'<div class="labs-nav"><button class="labs-toggle" aria-expanded="false" aria-controls="labs-menu" {"data-current=true" if active else ""}>ITD Labs <span aria-hidden="true">⌄</span></button><div id="labs-menu" hidden><a href="{route(p,l)}"{current(page,"itd-labs")}>{tr(l,"Të gjitha produktet","All products","Alle Produkte")}{A}</a><a href="{route("krakenos",l)}"{current(page,"krakenos")}>Kraken OS</a><a href="{route("kraken-communications",l)}"{current(page,"kraken-communications")}>Kraken Communications</a><a href="{route("aura",l)}"{current(page,"aura")}>AURA</a></div></div>'
  else:
   label=dict(zip(PAGES,labels(l)))[p]
   nav+=f'<a href="{route(p,l)}" '+('aria-current="page"' if p==page else '')+f'>{label}</a>'
 langs=''.join(f'<a href="{route(page,x)}" lang="{x}" aria-label="{name}" '+('aria-current="true"' if x==l else '')+f'>{x.upper()}</a>' for x,name in [('sq','Shqip'),('en','English'),('de','Deutsch')])
 variant={'creative':'creative','ai-agents':'ai'}.get(page,'original')
 return f'<a class="skip" href="#main">{t["skip"]}</a><header class="header"><div class="header-inner wrap"><a class="brand" href="{route("index",l)}" aria-label="IT Department"><img src="assets/brand/logo-{variant}.png" width="480" height="232" alt="IT Department"></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="{t["menu"]}"><span></span><span></span><span></span></button><nav id="main-nav" aria-label="{t["menu"]}"><div class="nav-links">{nav}</div><div class="languages" aria-label="{t["lang"]}">{langs}</div><a class="button nav-cta" href="{route("contact",l)}">{t["talk"]}{A}</a></nav></div></header>'

def footer(l,t,page='index'):
 html=_old_footer(l,t,page)
 extra=f'<div class="footer-products"><span>ITD LABS</span><a href="{route("krakenos",l)}">Kraken OS</a><a href="{route("kraken-communications",l)}">Kraken Communications</a><a href="{route("aura",l)}">AURA</a></div>'
 return html.replace('<div class="footer-bottom">',extra+'<div class="footer-bottom">')

def priority_services(l,t):
 items=[('web-software',tr(l,'Faqe interneti & softuer','Websites & software','Websites & Software'),tr(l,'Një faqe që shpjegon ofertën. Një sistem që lidh punën.','A website that explains your offer. A system that connects your work.','Eine Website, die Ihr Angebot erklärt. Software, die Ihre Abläufe verbindet.')),
 ('ai-automation',tr(l,'Automatizim me AI','AI automation','KI-Automatisierung'),tr(l,'Nga kërkesa te ndjekja, me rregulla dhe kontroll njerëzor.','From enquiry to follow-up, with clear rules and human oversight.','Von der Anfrage bis zur Nachverfolgung – mit klaren Regeln und menschlicher Kontrolle.'))]
 return '<section class="wrap section priority-services">'+heading(tr(l,'DY PIKA NISJEJE','TWO WAYS TO START','ZWEI AUSGANGSPUNKTE'),tr(l,'Çfarë e çon biznesin përpara?','What moves your business forward?','Was bringt Ihr Unternehmen weiter?'))+'<div class="grid two">'+''.join(f'<a class="priority-card card padded" href="{route(p,l)}"><span class="mini-number">0{i+1}</span><h2>{title}</h2><p>{desc}</p><span class="text-link">{copy(l)["details"]}{A}</span></a>' for i,(p,title,desc) in enumerate(items))+'</div></section>'

# Home banner (Report 02): 2–3 published slides, changing every 10 seconds (assets/slider.js).
# To change a slide, edit it here: order, title, line, text, link (a page of this site) and image.
# 'mobile' is an optional separate image for phones; 'alt' empty means the image is decorative.
SLIDES=[
 {'theme':'kraken','page':'krakenos','title':'Kraken OS','tagline':'Many arms. One brain.',
  'text':('Një platformë për punën e përditshme.','One platform for everyday work.','Eine Plattform für die tägliche Arbeit.'),
  'image':'assets/labs/slide-kraken-os.webp','mobile':'','size':(760,396),'alt':('Kraken OS — pamje e panelit','Kraken OS — dashboard view','Kraken OS — Dashboard-Ansicht')},
 {'theme':'communications','page':'kraken-communications','title':'Kraken Communications','tagline':'',
  'text':('Bisedat dhe ekipi në një vend.','Conversations and your team in one place.','Gespräche und Team an einem Ort.'),
  'image':'assets/labs/slide-communications.webp','mobile':'','size':(760,396),'alt':('Kraken Communications — pamje e përgjithshme','Kraken Communications — overview','Kraken Communications — Übersicht')},
 {'theme':'aura','page':'aura','title':'AURA','tagline':'Say it. Consider it handled.',
  'text':('Asistent privat me zë që i kthen kërkesat në detyra dhe takime.','A private voice assistant that turns requests into tasks and meetings.','Privater Sprachassistent, der Anfragen in Aufgaben und Termine verwandelt.'),
  'image':'assets/labs/aura-emblem.svg','mobile':'','size':(200,200),'alt':('','','')}]

def slider(l):
 n=len(SLIDES); slides=''; dots=''
 for i,s in enumerate(SLIDES):
  w,h=s['size']; alt=tr(l,*s['alt'])
  source=f'<source media="(max-width:540px)" srcset="{s["mobile"]}">' if s['mobile'] else ''
  media=f'<picture class="slide-media">{source}<img src="{s["image"]}" width="{w}" height="{h}" alt="{alt}" decoding="async"{"" if i==0 else " loading=lazy"}></picture>'
  tagline=f'<p class="slide-tagline"{en_attr(l)}>{s["tagline"]}</p>' if s['tagline'] else ''
  slides+=f'<div class="slide slide-{s["theme"]}{" is-active" if i==0 else ""}" role="group" aria-roledescription="{tr(l,"slajd","slide","Folie")}" aria-label="{i+1} / {n}: {s["title"]}" data-slide><div class="slide-copy"><p class="slide-kicker">0{i+1} / 0{n} · ITD LABS</p><h2>{s["title"]}</h2>{tagline}<p class="slide-text">{tr(l,*s["text"])}</p><a class="slide-link" href="{route(s["page"],l)}">{tr(l,"Shiko produktin","Explore product","Produkt ansehen")}{A}</a></div>{media}</div>'
  dots+=f'<button type="button" class="slider-dot" aria-controls="hero-slides" aria-label="{tr(l,"Slajdi","Slide","Folie")} {i+1}: {s["title"]}"{" aria-current=true" if i==0 else ""}><span class="slider-bar"><span class="slider-fill"></span></span></button>'
 pause=tr(l,('Ndalo ndërrimin automatik','Nis ndërrimin automatik'),('Pause automatic rotation','Start automatic rotation'),('Automatischen Wechsel anhalten','Automatischen Wechsel starten'))
 arrows=f'<button type="button" class="slider-pause" aria-label="{pause[0]}" data-pause="{pause[0]}" data-play="{pause[1]}"><span aria-hidden="true"></span></button><button type="button" class="slider-prev" aria-controls="hero-slides" aria-label="{tr(l,"Slajdi i mëparshëm","Previous slide","Vorherige Folie")}"><span aria-hidden="true">‹</span></button><button type="button" class="slider-next" aria-controls="hero-slides" aria-label="{tr(l,"Slajdi i radhës","Next slide","Nächste Folie")}"><span aria-hidden="true">›</span></button>'
 return f'<section class="hero-slider" aria-roledescription="{tr(l,"prezantim me slajde","carousel","Karussell")}" aria-label="ITD Labs" data-slider><div class="slides" id="hero-slides" aria-live="off">{slides}</div><div class="slider-controls" hidden><div class="slider-dots">{dots}</div><div class="slider-arrows">{arrows}</div></div></section>'

def home(l,t):
 c=copy(l)
 hero=f'<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="red-dot"></span>WEB / SOFTWARE / AI / IT</p><h1>{c["home"]}</h1><p class="lead">{tr(l,"Faqe interneti, softuer dhe automatizim me AI. Nga ideja te një zgjidhje që ekipi yt mund ta përdorë.","Websites, software and AI automation. From an idea to a solution your team can use.","Websites, Software und KI-Automatisierung. Von der Idee zu einer Lösung, die Ihr Team im Alltag nutzen kann.")}</p><div class="actions">{button(c["see"],route("services",l))}{button(c["book"],cfg["bookingUrl"],"target=\"_blank\" rel=\"noopener noreferrer\"","dark")}</div><p class="hero-location">Prishtina, Kosovo · SQ / EN / DE</p></div>{slider(l)}</section>'
 # Preserve the existing service depth, portfolio, process and support sections.
 old=_old_home(l,t); tail=old[old.index('</section>')+10:]
 return hero+priority_services(l,t)+tail

def services(l,t):
 old=_old_services(l,t); pos=old.index('</section>')+10
 return old[:pos]+priority_services(l,t)+old[pos:]

def product_note(l): return tr(l,'Pamje nga prezantimi i produktit. Modulet dhe kanalet e disponueshme varen nga konfigurimi, lejet dhe integrimet e miratuara.','Images from the product presentation. Available modules and channels depend on configuration, permissions and approved integrations.','Ansichten aus der Produktpräsentation. Verfügbare Module und Kanäle hängen von Konfiguration, Berechtigungen und freigegebenen Integrationen ab.')

SLIDE_IMAGE={'kraken-card':'slide-kraken-os.webp','communications-card':'slide-communications.webp'}

def aura_phone(l):
 # The AURA product view: its vector emblem on the app's dark screen (colours from the AURA app).
 return f'<figure class="aura-phone"><img src="assets/labs/aura-emblem.svg" width="200" height="200" alt=""><figcaption>AURA</figcaption><p{en_attr(l)}>Say it. Consider it handled.</p></figure>'

def labs(l,t):
 desc=tr(l,'Produkte dhe eksperimente të zhvilluara brenda IT Department. Secili me një qëllim të qartë dhe identitetin e vet.','Products and experiments developed within IT Department. Each with a clear purpose and its own identity.','Produkte und Experimente aus IT Department. Jedes mit einem klaren Zweck und einer eigenen Identität.')
 cards=''
 items=[('krakenos','Kraken OS','kraken-card',tr(l,'Platformë modulare','Modular platform','Modulare Plattform'),tr(l,'Klientët, puna dhe vendimet lidhen në një platformë të përbashkët.','Customers, work and decisions come together in one platform.','Kunden, Arbeit und Entscheidungen in einer gemeinsamen Plattform.'),['CRM',tr(l,'Projekte','Projects','Projekte'),'Accounting','Workspace']),('kraken-communications','Kraken Communications','communications-card',tr(l,'Komunikim me klientët','Customer communication','Kundenkommunikation'),tr(l,'Kanalet, kontaktet, bisedat e ekipit dhe ofertat në një platformë.','Channels, contacts, team conversations and offers in one platform.','Kanäle, Kontakte, Teamgespräche und Angebote in einer Plattform.'),['Inbox',tr(l,'Kontakte','Contacts','Kontakte'),tr(l,'Oferta','Offers','Angebote')]),('aura','AURA','aura-emblem',tr(l,'Asistent privat me zë','Private voice assistant','Privater Sprachassistent'),tr(l,'Një asistent i menduar për mënyrën si punon: nga kërkesat te detyrat dhe takimet.','An assistant designed around how you work: from requests to tasks and meetings.','Ein Assistent für Ihre Arbeitsweise: von Anfragen zu Aufgaben und Terminen.'),['Voice-first',tr(l,'Detyra','Tasks','Aufgaben'),tr(l,'Takime','Meetings','Termine')])]
 for i,(p,name,img,kind,body,tags) in enumerate(items):
  # AURA: vector emblem rebuilt from the AURA app's own drawing code (replaces the raster from the PDF).
  image='src="assets/labs/aura-emblem.svg" alt="AURA" width="200" height="200"' if img=='aura-emblem' else f'src="assets/labs/{SLIDE_IMAGE[img]}" alt="{name} — {copy(l)["screenshot"]}" width="760" height="396"'
  visual=f'<div class="lab-art lab-art-{i}"><span>0{i+1} / ITD LABS</span><img {image}><strong{en_attr(l)}>{["KRAKEN:OS","COMMUNICATIONS","SAY IT. CONSIDER IT HANDLED."][i]}</strong></div>'
  # Report 02: every card has "Shiko produktin", in ITD Labs green; the art keeps each product's colours.
  link=button(tr(l,'Shiko produktin','Explore product','Produkt ansehen'),route(p,l),style='outline labs')
  cards+=f'<article class="lab-card card" data-product="{p}">{visual}<div class="lab-card-copy"><p class="eyebrow">{kind}</p><h2>{name}</h2><p>{body}</p><div class="chips">'+''.join(f'<span>{x}</span>' for x in tags)+f'</div>{link}</div></article>'
 aura=f'<section class="wrap section"><div class="aura-showcase"><div><p class="eyebrow">AURA / ITD LABS</p><h2{en_attr(l)}>Say it.<br>Consider it<br>handled.</h2><p>{tr(l,"Një asistent privat me zë që i kthen kërkesat në detyra dhe takime.","A private voice assistant that turns requests into tasks and meetings.","Ein privater Sprachassistent, der Anfragen in Aufgaben und Termine verwandelt.")}</p>{button(tr(l,"Shiko produktin","Explore product","Produkt ansehen"),route("aura",l),style="light")}</div>{aura_phone(l)}</div></section>'
 return intro(tr(l,'Ide që bëhen produkte.','Ideas become products.','Aus Ideen werden Produkte.'),desc,t,'ITD LABS')+f'<section class="wrap labs-catalog"><div class="grid three">{cards}</div><p class="section-note">{product_note(l)}</p></section>'+aura+ending(l,t)

def communications(l,t):
 title=tr(l,'Komunikimi, i bashkuar në një vend.','Communication, together in one place.','Kommunikation an einem Ort.')
 lead=tr(l,'Bisedat, kontaktet dhe hapi i radhës — me kontekst të përbashkët për ekipin.','Conversations, contacts and the next step — with shared context for your team.','Gespräche, Kontakte und der nächste Schritt – mit gemeinsamem Kontext für Ihr Team.')
 hero=intro(title,lead,t,'ITD LABS / KRAKEN COMMUNICATIONS')
 # Report 02: the Kraken family logo (transparent, original blue) and the product's official site.
 hero=hero.replace('<section class="page-intro wrap">','<section class="page-intro wrap">'+KRAKEN_LOGO.format('Kraken Communications'),1).removesuffix('</section>')+f'<p class="official-row">{official("assistant.krakenos.cloud",l)}</p></section>'
 shot=f'<section class="wrap communications-screen"><a href="assets/labs/communications-dashboard.webp" data-lightbox="Kraken Communications"><img src="assets/labs/communications-dashboard.webp" width="2033" height="730" alt="{tr(l,"Kraken Communications — pamja e përgjithshme","Kraken Communications — overview","Kraken Communications — Übersicht")}"><span>{copy(l)["screenshot"]}{A}</span></a></section>'
 items=tr(l,[('Inbox i përbashkët','Website chat, Instagram dhe Messenger në një rrjedhë, me kanalet e lidhura për demonstrimin tuaj.'),('Kalimi te ekipi','AI dhe ekipi punojnë me të njëjtën histori. Përcaktohen pronësia, miratimet dhe momenti i ndërhyrjes.'),('Kontakte dhe oferta','Kontakti, ndjekja dhe oferta qëndrojnë pranë bisedës, pa humbur kontekstin.')],[('Shared inbox','Website chat, Instagram and Messenger in one flow, with channels connected for your demonstration.'),('Handoff to the team','AI and your team share the same history. Ownership, approvals and intervention points are defined.'),('Contacts and offers','Contacts, follow-up and offers stay close to the conversation, without losing context.')],[('Gemeinsamer Posteingang','Website-Chat, Instagram und Messenger in einem Ablauf, mit den für Ihre Demo verbundenen Kanälen.'),('Übergabe an das Team','KI und Team nutzen denselben Verlauf. Zuständigkeit, Freigaben und Übergabepunkte werden festgelegt.'),('Kontakte und Angebote','Kontakte, Nachverfolgung und Angebote bleiben direkt beim Gespräch – der Kontext bleibt erhalten.')])
 return hero+shot+'<section class="wrap section"><div class="grid three">'+''.join(f'<article class="card padded"><span class="mini-number">0{i+1}</span><h2>{a}</h2><p>{b}</p></article>' for i,(a,b) in enumerate(items))+'</div><p class="section-note product-note">'+product_note(l)+'</p><div class="actions">'+button(copy(l)['demo'],route('contact',l)+'?service=Kraken%20Communications&intent=demo')+button('ITD Labs',route('itd-labs',l),style='outline')+'</div></section>'

def krakenos(l,t):
 html=_old_kraken(l,t).replace('?service=KrakenOS"','?service=KrakenOS&amp;intent=demo"')
 inventory=f'<article class="card padded module-card">{icon(1)}<h3>{tr(l,"Inventari","Inventory","Inventar")}</h3><p>{tr(l,"Pamje e inventarit pranë proceseve të kompanisë. Fushat, qasjet dhe lidhjet me modulet e tjera përcaktohen në konfigurim.","Inventory alongside your company processes. Fields, access and connections to other modules are defined during configuration.","Inventar im Zusammenhang mit Ihren Unternehmensabläufen. Felder, Zugänge und Verbindungen zu weiteren Modulen werden bei der Einrichtung festgelegt.")}</p></article>'
 html=html.replace('</div></section><section class="wrap section"><div class="kraken-special">',inventory+'</div></section><section class="wrap section"><div class="kraken-special">',1)
 html=html.replace('<h1>Many arms.','<h1'+en_attr(l)+'>Many arms.',1)
 # Report 02: Kraken logo in the hero and the official product site as a separate link.
 html=html.replace('<div><p class="eyebrow">IT DEPARTMENT / KRAKENOS</p>','<div>'+KRAKEN_LOGO.format('Kraken OS')+'<p class="eyebrow">ITD LABS / KRAKEN OS</p>',1)
 hero_end=html.index('<a class="product-hero-image"')
 html=html[:hero_end].removesuffix('</div>')+f'<p class="official-row">{official("krakenos.cloud",l)}</p></div>'+html[hero_end:]
 return html.replace('<section class="kraken-hero wrap">','<section class="kraken-hero wrap">').replace('assets/krakenos/dashboard.png','assets/labs/kraken-dashboard.webp').replace('width="894" height="513"','width="1359" height="488"')+f'<p class="wrap section-note product-note">{product_note(l)}</p>'

def aura(l,t):
 # Report 02: AURA's own presentation page. Only the confirmed functions (voice, tasks, meetings);
 # the link to the app is added as a separate action once it is ready.
 lead=tr(l,'Një asistent privat me zë që i kthen kërkesat në detyra dhe takime.','A private voice assistant that turns requests into tasks and meetings.','Ein privater Sprachassistent, der Anfragen in Aufgaben und Termine verwandelt.')
 hero=f'<section class="aura-hero wrap"><div class="aura-hero-copy"><p class="eyebrow">ITD LABS / AURA</p><h1{en_attr(l)}>Say it.<br>Consider it handled.</h1><p class="lead">{lead}</p><div class="actions">{button(tr(l,"Pyet për AURA","Ask about AURA","Nach AURA fragen"),route("contact",l)+"?service=AURA",style="light")}{button("ITD Labs",route("itd-labs",l),style="outline")}</div></div>{aura_phone(l)}</section>'
 items=tr(l,[('Me zë','E thua kërkesën me zë, ashtu siç do t’ia thoje dikujt nga ekipi.'),('Detyra','Kërkesat kthehen në detyra konkrete.'),('Takime','Kërkesat për takime kthehen në takime.')],[('Voice-first','You say the request out loud, the way you would tell someone on your team.'),('Tasks','Requests become concrete tasks.'),('Meetings','Meeting requests become meetings.')],[('Sprache zuerst','Sie sprechen die Anfrage aus, so wie Sie es jemandem aus dem Team sagen würden.'),('Aufgaben','Anfragen werden zu konkreten Aufgaben.'),('Termine','Terminanfragen werden zu Terminen.')])
 functions='<section class="wrap section aura-functions">'+heading('AURA',tr(l,'Nga kërkesa te veprimi.','From request to action.','Von der Anfrage zur Umsetzung.'))+'<div class="grid three">'+''.join(f'<article class="card padded"><span class="mini-number">0{i+1}</span><h3>{a}</h3><p>{b}</p></article>' for i,(a,b) in enumerate(items))+'</div><p class="section-note product-note">'+tr(l,'Pamje paraprake e produktit. Lidhja me aplikacionin do të shtohet kur të jetë gati.','Product preview. The link to the app will be added when it is ready.','Produktvorschau. Der Link zur App folgt, sobald sie bereit ist.')+'</p></section>'
 return hero+functions+ending(l,t)

def service_landing(l,t,ai_service=False):
 if ai_service:
  title=tr(l,'Më pak rutinë. Më shumë kontroll.','Less routine. More control.','Weniger Routine. Mehr Kontrolle.')
  lead=tr(l,'Automatizim me AI për kërkesa, dokumente dhe ndjekje. Zgjedhim një proces të qartë, e provojmë me ekipin dhe përcaktojmë kufijtë përpara përdorimit.','AI automation for enquiries, documents and follow-up. We choose one clear process, test it with your team and define the boundaries before use.','KI-Automatisierung für Anfragen, Dokumente und Nachverfolgung. Wir wählen einen klaren Prozess, testen ihn mit Ihrem Team und legen vor dem Einsatz die Grenzen fest.')
  service=tr(l,'Automatizim me AI','AI automation','KI-Automatisierung'); key='ai-automation'
  items=tr(l,[('Kërkesat e klientëve','Klasifikim i kërkesave dhe përgatitje e përgjigjeve nga burime të miratuara. Ekipi kontrollon dërgimin.'),('Dokumentet dhe raportet','Nxjerrje dhe përmbledhje informacioni, me dokumentin burimor pranë rezultatit për verifikim.'),('Ndjekja e punës','Përgatitje detyrash dhe kujtesash. Ndryshimet me ndikim kalojnë përmes miratimit të përcaktuar.')],[('Customer enquiries','Classify enquiries and draft answers from approved sources. Your team controls sending.'),('Documents and reports','Extract and summarise information, keeping the source document alongside the result for verification.'),('Work follow-up','Prepare tasks and reminders. Consequential changes pass through the agreed approval step.')],[('Kundenanfragen','Anfragen einordnen und Antworten aus freigegebenen Quellen vorbereiten. Ihr Team kontrolliert den Versand.'),('Dokumente und Berichte','Informationen extrahieren und zusammenfassen. Das Original bleibt zur Prüfung beim Ergebnis.'),('Nachverfolgung','Aufgaben und Erinnerungen vorbereiten. Änderungen mit Auswirkungen durchlaufen die vereinbarte Freigabe.')])
  audience=tr(l,'Për ekipe që përsërisin të njëjtat hapa në email, CRM, tabela ose dokumente dhe duan t’i lehtësojnë pa humbur mbikëqyrjen.','For teams repeating the same steps across email, CRM, spreadsheets or documents who want to reduce that work while retaining oversight.','Für Teams, die dieselben Schritte in E-Mail, CRM, Tabellen oder Dokumenten wiederholen und ihren Aufwand reduzieren möchten, ohne die Kontrolle abzugeben.')
  example=tr(l,'Shembull ilustrues: një kërkesë hyn nga formulari. Agjenti propozon kategorinë dhe një draft përgjigjeje nga dokumentet e miratuara. Një person e kontrollon dhe miraton përpara dërgimit. Pa burim të qartë, kërkesa kalon te ekipi.','Illustrative example: an enquiry arrives through a form. The agent suggests a category and drafts a response from approved documents. A person checks and approves it before sending. Without a clear source, the enquiry goes to the team.','Beispielszenario: Eine Anfrage trifft über das Formular ein. Der Agent schlägt eine Kategorie vor und entwirft eine Antwort aus freigegebenen Dokumenten. Eine Person prüft und genehmigt sie vor dem Versand. Ohne eindeutige Quelle übernimmt das Team.')
  assurance=tr(l,'Burimet, qasjet dhe aprovimet caktohen për çdo projekt. Integrimet me CRM, email dhe kanale të tjera kërkojnë qasjet përkatëse. Fillojmë me një pilot të kontrolluar dhe testojmë edhe përgjigjet e pasakta, mungesën e të dhënave dhe kalimin te njeriu.','Sources, access and approvals are defined per project. Connections to CRM, email and other channels need the corresponding permissions. We begin with a controlled pilot and also test incorrect answers, missing data and handoff to a person.','Quellen, Zugänge und Freigaben werden je Projekt festgelegt. CRM-, E-Mail- und weitere Anbindungen benötigen entsprechende Berechtigungen. Wir beginnen mit einem kontrollierten Pilotprojekt und testen auch falsche Antworten, fehlende Daten und die Übergabe an Menschen.')
 else:
  title=tr(l,'Një faqe për klientët. Një sistem për ekipin.','A website for customers. A system for your team.','Eine Website für Ihre Kunden. Software für Ihr Team.')
  lead=tr(l,'Ndërtojmë faqe interneti dhe softuer rreth ofertës, klientëve dhe mënyrës si punon biznesi yt — nga struktura e parë te dorëzimi dhe mirëmbajtja.','We build websites and software around your offer, customers and the way your business works — from the first structure to handover and maintenance.','Wir entwickeln Websites und Software passend zu Ihrem Angebot, Ihren Kunden und Ihren Abläufen – von der ersten Struktur bis zur Übergabe und Wartung.')
  service=tr(l,'Faqe interneti & softuer','Websites & software','Websites & Software'); key='web-software'
  items=tr(l,[('Faqe që shpjegojnë ofertën','Strukturë e qartë, përmbajtje në gjuhët e projektit, përvojë në telefon dhe rrugë e drejtpërdrejtë drejt kontaktit.'),('Softuer për procesin tënd','Portale, aplikacione dhe mjete që lidhin kërkesat, detyrat, dokumentet dhe rolet e ekipit.'),('Dorëzim dhe mbështetje','Testim i rrjedhave kryesore, udhëzime për ekipin dhe plan mirëmbajtjeje i përcaktuar në ofertë.')],[('Websites that explain your offer','Clear structure, content in the project’s languages, a considered mobile experience and a direct path to contact.'),('Software for your process','Portals, applications and tools connecting enquiries, tasks, documents and team roles.'),('Handover and support','Testing of key journeys, guidance for your team and a maintenance plan defined in the proposal.')],[('Websites, die Ihr Angebot erklären','Klare Struktur, Inhalte in den Projektsprachen, eine durchdachte mobile Nutzung und ein direkter Kontaktweg.'),('Software für Ihre Abläufe','Portale, Anwendungen und Werkzeuge verbinden Anfragen, Aufgaben, Dokumente und Teamrollen.'),('Übergabe und Betreuung','Prüfung der zentralen Abläufe, Anleitung für Ihr Team und ein im Angebot festgelegter Wartungsplan.')])
  audience=tr(l,'Për biznese që duan prezencë më të qartë në internet ose që puna e tyre ka kaluar kufijtë e tabelave, emailit dhe sistemeve të shkëputura.','For businesses that need a clearer online presence or whose work has outgrown spreadsheets, email and disconnected systems.','Für Unternehmen, die online klarer auftreten möchten oder deren Abläufe über Tabellen, E-Mails und voneinander getrennte Systeme hinausgewachsen sind.')
  example=tr(l,'Shembull ilustrues: një portal i lidh kërkesat, dokumentet dhe aprovimet në një rrjedhë. Stafi sheh hapin e radhës dhe përgjegjësin. Ky është skenar demonstrues, jo rezultat i verifikuar i një klienti.','Illustrative example: a portal connects requests, documents and approvals in one flow. Staff can see the next step and its owner. This is a demonstration scenario, not a verified client result.','Beispielszenario: Ein Portal verbindet Anfragen, Dokumente und Freigaben. Mitarbeitende sehen den nächsten Schritt und die zuständige Person. Dies ist ein Demonstrationsszenario, kein belegtes Kundenergebnis.')
  assurance=tr(l,'Para zhvillimit përcaktojmë përmbajtjen, gjuhët, funksionet, pronësinë dhe afatet. Integrimet dhe mirëmbajtja përfshihen vetëm sipas marrëveshjes. Dorëzimi përfshin shpjegimin e zgjidhjes dhe kontrollin e përdorimit në telefon e desktop.','Before development, we agree content, languages, functions, ownership and timing. Integrations and maintenance follow the agreed scope. Handover includes an explanation of the solution and checks on mobile and desktop.','Vor der Entwicklung stimmen wir Inhalte, Sprachen, Funktionen, Zuständigkeiten und Termine ab. Integrationen und Wartung richten sich nach dem vereinbarten Umfang. Zur Übergabe gehören eine Erklärung der Lösung sowie Prüfungen auf Mobilgeräten und Desktop.')
 hero=intro(title,lead,t,service)+f'<div class="wrap actions service-actions">{button(copy(l)["book"],cfg["bookingUrl"],"target=\"_blank\" rel=\"noopener noreferrer\"")}{button(t["talk"],route("contact",l)+"?service="+quote(service),style="outline")}</div>'
 features='<section class="wrap section"><div class="grid three">'+''.join(f'<article class="card padded"><span class="mini-number">0{i+1}</span><h2>{a}</h2><p>{b}</p></article>' for i,(a,b) in enumerate(items))+'</div></section>'
 context='<section class="wrap section service-context"><div><p class="eyebrow">'+tr(l,'PËR KË','WHO IT IS FOR','FÜR WEN')+'</p><h2>'+tr(l,'Nga nevoja reale.','Start with a real need.','Vom tatsächlichen Bedarf ausgehen.')+'</h2><p>'+audience+'</p></div><div><p class="eyebrow">'+tr(l,'SI PUNOJMË','HOW WE WORK','SO ARBEITEN WIR')+'</p><p>'+assurance+'</p></div></section>'
 example_html='<section class="wrap section"><div class="service-example card padded"><p class="eyebrow">'+tr(l,'SHEMBULL ILUSTRUES','ILLUSTRATIVE EXAMPLE','BEISPIELSZENARIO')+'</p><h2>'+tr(l,'Nga kërkesa te hapi i radhës.','From an enquiry to the next step.','Von der Anfrage zum nächsten Schritt.')+'</h2><p>'+example+'</p>'+button(tr(l,'Shiko agjentët','Explore agents','Agenten ansehen') if ai_service else copy(l)['details'],route('ai-agents' if ai_service else 'project-detail',l),style='outline')+'</div></section>'
 germany=''
 if l=='de': germany='<section class="wrap section"><div class="card padded"><p class="eyebrow">PRISHTINA → DEUTSCHLAND</p><h2>Zusammenarbeit mit klarer Übergabe.</h2><p>Unser Team sitzt in Prishtina, Kosovo. Für Ihr Projekt vereinbaren wir Kommunikationssprache, Ansprechperson, Besprechungen und schriftliche Meilensteine. Zugänge, Dokumentation, Übergabe und der Umfang des anschließenden Supports werden vorab festgelegt. So ist klar, wer wofür verantwortlich ist.</p></div></section>'
 return hero+features+context+process(l,t)+example_html+germany+ending(l,t)

def web_software(l,t): return service_landing(l,t)
def ai_automation(l,t): return service_landing(l,t,True)

NEW_META={
 'itd-labs':(['ITD Labs · Produkte & eksperimente','ITD Labs · Products & experiments','ITD Labs · Produkte & Experimente'],['Kraken OS, Kraken Communications dhe AURA: produktet e IT Department, secili me faqen e vet.','Kraken OS, Kraken Communications and AURA: products by IT Department, each with its own page.','Kraken OS, Kraken Communications und AURA: Produkte von IT Department, jeweils mit eigener Seite.']),
 'aura':(['AURA · Asistent privat me zë','AURA · Private voice assistant','AURA · Privater Sprachassistent'],['AURA nga ITD Labs: asistent privat me zë që i kthen kërkesat në detyra dhe takime.','AURA by ITD Labs: a private voice assistant that turns requests into tasks and meetings.','AURA von ITD Labs: ein privater Sprachassistent, der Anfragen in Aufgaben und Termine verwandelt.']),
 'kraken-communications':(['Kraken Communications · Biseda, kontakte & oferta','Kraken Communications · Conversations, contacts & offers','Kraken Communications · Gespräche, Kontakte & Angebote'],['Inbox i përbashkët, kalim nga AI te ekipi dhe ndjekje e kontakteve. Kërko demonstrim sipas kanaleve të tua.','A shared inbox, AI-to-team handoff and contact follow-up. Request a demonstration around your channels.','Gemeinsamer Posteingang, KI-Übergabe an das Team und Kontaktnachverfolgung. Demo für Ihre Kanäle anfragen.']),
 'web-software':(['Faqe interneti & softuer në Kosovë','Websites & software from Kosovo','Websites & Software · Entwicklung aus Kosovo'],['Faqe interneti dhe softuer për biznesin: strukturë, zhvillim, testim dhe dorëzim nga IT Department në Prishtinë.','Business websites and software: structure, development, testing and handover by IT Department in Prishtina.','Websites und individuelle Software für Unternehmen in Deutschland und Kosovo: Entwicklung, Tests und Übergabe aus Prishtina.']),
 'ai-automation':(['Automatizim me AI për biznesin','AI automation for business','KI-Automatisierung für Unternehmen'],['Automatizim për kërkesa, dokumente dhe ndjekje me burime të miratuara, rregulla dhe kontroll njerëzor.','Automation for enquiries, documents and follow-up with approved sources, clear rules and human oversight.','Automatisierung für Anfragen, Dokumente und Nachverfolgung mit freigegebenen Quellen und menschlicher Kontrolle.']),
 'krakenos':(['Kraken OS · Platformë modulare','Kraken OS · Modular business platform','Kraken OS · Modulare Unternehmensplattform'],['CRM, projekte, detyra dhe financa në një platformë modulare. Kërko demonstrim për biznesin tënd.','CRM, projects, tasks and finance in a modular platform. Request a demonstration for your business.','CRM, Projekte, Aufgaben und Finanzen in einer modularen Plattform. Demo für Ihr Unternehmen anfragen.'])}
