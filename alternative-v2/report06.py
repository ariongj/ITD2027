"""Change report 06 (13 October 2026), the main version only — ITD2027/M keeps its own look.

One axis for every title on the base pages and ITD Labs, the home title above the slideshow, a quiet
background, nine partners in 3 × 3, a black Services hero with centred filters, ITD Labs in green,
bigger Creative boxes, the approved AI character in the existing box and a black contact form.
Layout and colour are in assets/report06.css, which only this version loads."""
_r5_home=home
_r5_services=services
_r5_contact=contact
_r5_ai=ai
_r5_labs=labs
_r5_header=header
_r5_footer=footer

# Base pages and ITD Labs: titles, descriptions, filters and card names on one centred axis
# (<body data-axis="center">). Creative and AI Agents keep their layout; only pages 13-15 of the report apply there.
CENTER_PAGES=['index','services','projects','partners','itd-labs','about','contact']

# Home: the title on top, the slideshow below it. On wide screens the previous and next slides show
# beside the active one; clicking them turns the slideshow (the arrows and dots do the same for everyone).
def peek_card(s):
 if s.get('banner'): media,theme=f'<img src="{s["banner"]}-768.webp" width="768" height="512" alt="" decoding="async">','banner'
 else:
  w,h=s['size']; media,theme=f'<img src="{s["image"]}" width="{w}" height="{h}" alt="" decoding="async">',s['theme']
 return f'<div class="peek-card peek-{theme}"><span class="peek-media">{media}</span><span class="peek-name">{s["title"]}</span></div>'
def peeks(side):
 n=len(SLIDES); shown=n-1 if side=='prev' else 1
 return f'<div class="peek-col peek-{side}" data-peeks="{side}" aria-hidden="true">'+''.join(f'<div class="peek{" is-shown" if i==shown else ""}">{peek_card(s)}</div>' for i,s in enumerate(SLIDES))+'</div>'

def home(l,t):
 c=copy(l)
 lead=tr(l,"Faqe interneti, softuer dhe automatizim me AI. Nga ideja te një zgjidhje që ekipi yt mund ta përdorë.","Websites, software and AI automation. From an idea to a solution your team can use.","Websites, Software und KI-Automatisierung. Von der Idee zu einer Lösung, die Ihr Team im Alltag nutzen kann.")
 hero=(f'<div class="r6-hero-band"><section class="hero r6-hero wrap"><div class="hero-copy"><p class="eyebrow">WEB / SOFTWARE / AI / IT</p><h1>{c["home"]}</h1><p class="lead">{lead}</p>'
  f'<div class="actions">{button(c["see"],route("services",l))}{button(c["book"],cfg["bookingUrl"],"target=\"_blank\" rel=\"noopener noreferrer\"","dark")}</div></div>'
  f'<div class="r6-stage">{peeks("prev")}{slider(l)}{peeks("next")}</div></section></div>')
 # The service areas, projects, partners and support plans follow as before.
 old=_old_home(l,t); tail=old[old.index('</section>')+10:]
 return hero+priority_services(l,t)+tail

# Services: the title in its own black box.
def services(l,t):
 html=_r5_services(l,t)
 if THEME=='m': return html
 c=copy(l); old=intro(c['services'],t['servicelead'],t,labels(l)[1])
 assert html.startswith(old)
 return f'<section class="wrap r6-dark-hero"><div class="r6-dark-box"><p class="eyebrow">{esc(labels(l)[1])}</p><h1>{esc(c["services"])}</h1><p class="lead">{esc(t["servicelead"])}</p></div></section>'+html[len(old):]

# ITD Labs badge: a drawn flask with a narrow neck and a wide base. Two or three small bubbles rise and fade
# and the flask floats 2-3 px (report06.css); with reduced motion it stays still.
LABS_FLASK=('<svg class="labs-flask" viewBox="0 0 64 80" aria-hidden="true" focusable="false"><defs><linearGradient id="labs-liquid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a6f2bd"/><stop offset="1" stop-color="#2fae63"/></linearGradient></defs>'
 '<g class="flask-body"><path d="M24.5 12V29L11 57.2C8.2 63.1 12.5 70 19 70H45C51.5 70 55.8 63.1 53 57.2L39.5 29V12" fill="#f3fff6" fill-opacity=".14"/>'
 '<path d="M15.6 47.5Q32 43.5 48.4 47.5L53 57.2C55.8 63.1 51.5 70 45 70H19C12.5 70 8.2 63.1 11 57.2Z" fill="url(#labs-liquid)"/>'
 '<path d="M24.5 12V29L11 57.2C8.2 63.1 12.5 70 19 70H45C51.5 70 55.8 63.1 53 57.2L39.5 29V12" fill="none" stroke="#b9f5cb" stroke-width="3" stroke-linejoin="round"/>'
 '<rect x="20" y="6" width="24" height="7" rx="3.5" fill="#1b4a30" stroke="#b9f5cb" stroke-width="2.5"/>'
 '<circle cx="29" cy="60" r="3.2" fill="none" stroke="#f2fff6" stroke-width="2"/><circle cx="38.5" cy="55" r="2" fill="none" stroke="#f2fff6" stroke-width="1.8"/></g>'
 '<circle class="bubble b1" cx="33" cy="36" r="2.4" fill="#b9f5cb"/><circle class="bubble b2" cx="29" cy="41" r="1.7" fill="#b9f5cb"/><circle class="bubble b3" cx="36" cy="44" r="1.4" fill="#b9f5cb"/>'
 '<path d="M5 30h8M9 26v8" stroke="#9fe8b6" stroke-width="2" stroke-linecap="round"/></svg>')

def labs_stage(l):
 # The products layered in the hero; the same views are in the catalogue below, so this is decorative.
 bar=lambda label:f'<span class="stage-bar"><i></i><i></i><i></i><b>{label}</b></span>'
 return ('<div class="labs-stage" aria-hidden="true">'
  f'<figure class="stage-win stage-kraken">{bar("KRAKEN OS / WORKSPACE")}<img src="assets/labs/slide-kraken-os.webp" width="760" height="396" alt="" decoding="async"></figure>'
  f'<figure class="stage-win stage-comms">{bar("COMMUNICATIONS")}<img src="assets/labs/slide-communications.webp" width="760" height="396" alt="" decoding="async"></figure>'
  '<figure class="stage-aura"><img src="assets/labs/aura-emblem.svg" width="200" height="200" alt=""><strong>AURA</strong><small>Say it. Consider it handled.</small></figure>'
  f'<span class="labs-badge">{LABS_FLASK}</span></div>')

def labs(l,t):
 if THEME=='m': return _r5_labs(l,t)
 title=tr(l,('Ide që bëhen','produkte.'),('Ideas become','products.'),('Aus Ideen werden','Produkte.'))
 lead=tr(l,'Produkte dhe eksperimente të zhvilluara brenda IT Department. Secili me një qëllim të qartë dhe identitetin e vet.','Products and experiments developed within IT Department. Each with a clear purpose and its own identity.','Produkte und Experimente, entwickelt bei IT Department. Jedes mit einem klaren Zweck und eigener Identität.')
 chips=tr(l,['NDËRTUAR NGA ITD','PRODUKTE & EKSPERIMENTE'],['BUILT BY ITD','PRODUCTS & EXPERIMENTS'],['ENTWICKELT VON ITD','PRODUKTE & EXPERIMENTE'])
 hero=(f'<section class="labs-hero wrap"><p class="eyebrow">{tr(l,"ITD LABS / PRODUKTET TONA","ITD LABS / OUR PRODUCTS","ITD LABS / UNSERE PRODUKTE")}</p><h1>{title[0]} <span>{title[1]}</span></h1><p class="lead">{lead}</p>'
  f'<div class="actions">{button(tr(l,"Eksploro produktet","Explore the products","Produkte entdecken"),"#products",style="mint")}{button(t["talk"],route("contact",l),style="ghost")}</div>'
  f'{labs_stage(l)}<ul class="labs-chips">'+''.join(f'<li>{x}</li>' for x in chips)+'</ul></section>')
 cards=''
 for i,(p,name,img,kind,body,tags) in enumerate(lab_items(l)):
  cards+=(f'<article class="lab-card card" data-product="{p}"><div class="lab-art lab-art-{i}"><img {lab_image(img,name,l)}></div><div class="lab-card-copy">'
   f'<p class="eyebrow">0{i+1} / {lab_kinds(l)[i]}</p><h3>{name}</h3><p>{body}</p><ul class="lab-tags">'+''.join(f'<li>{x}</li>' for x in tags)+'</ul>'
   f'{button(tr(l,"Shiko produktin","Explore product","Produkt ansehen"),route(p,l),style="mint")}</div></article>')
 catalog=('<section class="wrap section labs-catalog" id="products">'+heading(tr(l,'NJË EKIP / TRE PRODUKTE','ONE TEAM / THREE PRODUCTS','EIN TEAM / DREI PRODUKTE'),tr(l,'Produktet tona.','Our products.','Unsere Produkte.'),
  tr(l,'Platforma, komunikimi dhe asistenti me zë. Gjej produktin që lidhet me mënyrën si punon.','A platform, communication and a voice assistant. Find the product that fits the way you work.','Plattform, Kommunikation und Sprachassistent. Finden Sie das Produkt, das zu Ihrer Arbeitsweise passt.'))
  +f'<div class="grid three">{cards}</div><p class="section-note">{product_note(l)}</p></section>')
 return hero+catalog+aura_showcase(l)+ending(l,t)

# ITD Labs page: the original logo with its red turned into #008000 (assets/brand/logo-labs.png).
def labs_logo(html,page):
 return html.replace('src="assets/brand/logo-original.png"','src="assets/brand/logo-labs.png"') if THEME!='m' and page=='itd-labs' else html
def header(page,l,t): return labs_logo(_r5_header(page,l,t),page)
def footer(l,t,page='index'): return labs_logo(_r5_footer(l,t,page),page)

# AI Agents: the approved character inside the existing Request → Agent → Approval → Action box.
def ai(l,t):
 html=_r5_ai(l,t)
 if THEME=='m': return html
 old=f'<div class="agent-orbit">{icon(2)}<span>AI</span></div>'
 assert old in html
 character=('<div class="agent-character"><img src="assets/ai/agent-character-200.webp" srcset="assets/ai/agent-character-200.webp 200w, assets/ai/agent-character-400.webp 400w" sizes="170px" width="200" height="152" alt="" decoding="async">'
  '<i class="lid lid-l"></i><i class="lid lid-r"></i></div>')
 return html.replace(old,f'<div class="agent-orbit r6-orbit">{character}<span>AI</span></div>',1)

# Contact: the enquiry form in black with a red title and a short line under it; fields and sending unchanged.
def contact(l,t):
 html=_r5_contact(l,t)
 if THEME=='m': return html
 title=tr(l,"Na trego pak për projektin.","Tell us about your project.","Erzählen Sie uns von Ihrem Projekt.")
 old=f'<div class="form-card"><h2>{title}</h2>'
 assert old in html
 lead=tr(l,'Pak kontekst na ndihmon të nisim nga pika e duhur.','A little context helps us start in the right place.','Etwas Kontext hilft uns, an der richtigen Stelle zu beginnen.')
 return html.replace(old,f'<div class="form-card r6-form-dark"><h2>{title}</h2><p class="form-lead">{lead}</p>',1)
