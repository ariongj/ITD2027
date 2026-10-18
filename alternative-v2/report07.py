"""Change report 07 (16 October 2026), the main version only — ITD2027/M keeps its own look.

The home slideshow shows the four service banners on an orbit (6 s per step, 900 ms transition, no visible
pause button, the indicators choose a card). Buttons and text links lose the diagonal arrow. ITD Labs uses
the new Kraken OS and Kraken Assistant banners (Kraken Communications is now Kraken Assistant everywhere).
About loses the red quote box, Contact gets email and phone as red buttons, the footer gets columns, an
outlined email button and mono social icons, and each AI agent card shows its own character.
Layout and motion are in assets/report07.css and assets/orbit.js, which only this version loads."""
_r6_home=home
_r6_about=about
_r6_contact=contact
_r6_ai=ai
_r6_footer=footer
_r6_lab_image=lab_image
_r6_krakenos=krakenos

# Header: as in every mock-up of the report (desktop and phone), the shield beside "IT Department" in one
# row instead of the stacked logo; ITD Labs, Creative and AI Agents keep their own shield colours.
_r6_header=header
def header(page,l,t):
 html=_r6_header(page,l,t)
 if THEME=='m': return html
 import re
 variant={'creative':'creative','ai-agents':'ai','itd-labs':'labs'}.get(page,'original')
 html,n=re.subn(r'(<a class="brand" href="[^"]*" aria-label="IT Department">)<img src="assets/brand/logo-[a-z]+\.png" width="480" height="232" alt="IT Department"></a>',
  lambda m:m.group(1).replace('class="brand"','class="brand r7-head-brand"')+f'<img src="assets/brand/shield-{variant}.png" width="122" height="146" alt=""><span>IT Department</span></a>',html,count=1)
 assert n==1
 return html

# Buttons, text links and the footer email carry no diagonal arrow any more (cards keep their corner mark,
# project names keep the "opens a new tab" mark).
if THEME!='m': A=''

# Home: the four service banners (16:9, the logo and words are in the picture, so they are the alt text).
# Order and links as in the report: 01 Web & Software, 02 IT & Security, 03 AI Agents, 04 Creative.
SERVICE_SLIDES=[
 ('web','services','#web',('Web & Software','Web & Software','Web & Software'),'Web & Software. Built for your business. Websites. Apps. Business software.'),
 ('it','services','#it',('IT & Siguri','IT & Security','IT & Sicherheit'),'IT & Security. Stay secure. Keep moving. IT support. Cybersecurity. IT audits.'),
 ('ai','ai-agents','',('AI Agents','AI Agents','KI-Agenten'),'AI Agents. Less busywork. More control. AI workflows. Human oversight.'),
 ('creative','creative','',('Kreativa','Creative','Kreativ'),'Creative. Make your brand matter. Brand identity. Content. Digital campaigns.')]
ORBIT_PLACES=['is-center','is-right','is-back','is-left']

def orbit(l):
 cards=''; dots=''
 for i,(key,page,anchor,label,words) in enumerate(SERVICE_SLIDES):
  name=tr(l,*label); place=ORBIT_PLACES[i]
  hidden='' if i==0 else ' aria-hidden="true" tabindex="-1"'
  cards+=(f'<a class="orbit-card {place}" href="{route(page,l)}{anchor}" data-slide data-label="0{i+1} / {name}"{hidden}>'
   f'<img src="assets/home/service-{key}-1600.webp" srcset="assets/home/service-{key}-800.webp 800w, assets/home/service-{key}-1600.webp 1600w" sizes="(max-width:800px) 92vw, 700px" width="1600" height="900" alt="IT Department — {words}"{en_attr(l)} decoding="async"{" loading=lazy" if place=="is-back" else ""}></a>')
  dots+=f'<button type="button" class="slider-dot" aria-controls="orbit-slides" aria-label="{tr(l,"Slajdi","Slide","Folie")} {i+1}: {name}"{" aria-current=true" if i==0 else ""}><span class="slider-bar"><span class="slider-fill"></span></span></button>'
 pause=tr(l,('Ndalo ndërrimin automatik','Nis ndërrimin automatik'),('Pause automatic rotation','Start automatic rotation'),('Automatischen Wechsel anhalten','Automatischen Wechsel starten'))
 first=f'01 / {tr(l,*SERVICE_SLIDES[0][3])}'
 return (f'<section class="r7-orbit" aria-roledescription="{tr(l,"prezantim me slajde","carousel","Karussell")}" aria-label="{tr(l,"Shërbimet tona","Our services","Unsere Leistungen")}" data-orbit>'
  f'<button type="button" class="orbit-pause" data-pause="{pause[0]}" data-play="{pause[1]}">{pause[0]}</button>'
  f'<div class="orbit-stage" id="orbit-slides" aria-live="off">{cards}</div>'
  f'<div class="orbit-controls" hidden><div class="slider-dots">{dots}</div><p class="orbit-caption" aria-hidden="true" data-caption>{first}</p></div></section>')

def home(l,t):
 c=copy(l)
 lead=tr(l,"Faqe interneti, softuer dhe automatizim me AI, të ndërtuara rreth nevojave të biznesit dhe mënyrës si punon ekipi yt.","Websites, software and AI automation built around your business needs and the way your team works.","Websites, Software und KI-Automatisierung, abgestimmt auf Ihr Unternehmen und die Arbeitsweise Ihres Teams.")
 hero=(f'<div class="r6-hero-band"><section class="hero r6-hero wrap"><div class="hero-copy"><p class="eyebrow">WEB / SOFTWARE / AI / IT</p><h1>{c["home"]}</h1><p class="lead">{lead}</p>'
  f'<div class="actions">{button(c["see"],route("services",l))}{button(c["book"],cfg["bookingUrl"],"target=\"_blank\" rel=\"noopener noreferrer\"","dark")}</div></div>{orbit(l)}</section></div>')
 old=_old_home(l,t); tail=old[old.index('</section>')+10:]
 return hero+priority_services(l,t)+tail

# ITD Labs: the supplied Kraken OS and Kraken Assistant banners in the hero composition and on the cards,
# shown whole. The composition, AURA and the other content stay as they are.
LAB_BANNERS={'kraken-card':('kraken-os-banner','Your business. Connected. Clients, projects and finance. One platform.',(1200,510)),
 'communications-card':('kraken-assistant-banner','Every conversation. One inbox. AI assistance. Your team in control.',(1200,509))}
def lab_image(img,name,l):
 if THEME=='m' or img not in LAB_BANNERS: return _r6_lab_image(img,name,l)
 key,words,(w,h)=LAB_BANNERS[img]
 return f'src="assets/labs/{key}-1200.webp" srcset="assets/labs/{key}-600.webp 600w, assets/labs/{key}-1200.webp 1200w" sizes="(max-width:800px) 92vw, 420px" alt="{name} — {words}"{en_attr(l)} width="{w}" height="{h}" loading="lazy" decoding="async"'

def labs_stage(l):
 bar=lambda label:f'<span class="stage-bar"><i></i><i></i><i></i><b>{label}</b></span>'
 return ('<div class="labs-stage" aria-hidden="true">'
  f'<figure class="stage-win stage-kraken">{bar("KRAKEN OS / WORKSPACE")}<img src="assets/labs/kraken-os-banner-1200.webp" width="1200" height="510" alt="" decoding="async"></figure>'
  f'<figure class="stage-win stage-comms">{bar("KRAKEN ASSISTANT")}<img src="assets/labs/kraken-assistant-banner-1200.webp" width="1200" height="509" alt="" decoding="async"></figure>'
  '<figure class="stage-aura"><img src="assets/labs/aura-emblem.svg" width="200" height="200" alt=""><strong>AURA</strong><small>Say it. Consider it handled.</small></figure>'
  f'<span class="labs-badge">{LABS_FLASK}</span></div>')

def krakenos(l,t):
 html=_r6_krakenos(l,t)
 return html if THEME=='m' else html.replace(' ↗</a>','</a>')

# About: the red quote box goes, with its space; the three values follow the introduction directly.
def about(l,t):
 html=_r6_about(l,t)
 if THEME=='m': return html
 s=html.index('<div class="quote-card">'); e=html.index('</div>',s)+6
 return html[:s]+html[e:]

# Contact: under the form, "Preferon të shkruash?" with email and phone as two red buttons.
def contact(l,t):
 html=_r6_contact(l,t)
 if THEME=='m': return html
 s=html.index('<div class="contact-aside">'); e=html.index('</section>',s)
 lead=tr(l,'Na kontakto drejtpërdrejt me email ose telefon.','Contact us directly by email or phone.','Kontaktieren Sie uns direkt per E-Mail oder Telefon.')
 direct=(f'<div class="contact-aside r7-direct"><h2>{t["write"]}</h2><p class="r7-direct-lead">{lead}</p><div class="r7-direct-actions">'
  f'<a class="button" href="mailto:{cfg["email"]}">{cfg["email"]}</a><a class="button" href="tel:+{cfg["phoneDigits"]}">{cfg["phoneDisplay"]}</a></div>'
  f'<p class="r7-direct-meta">{t["location"]} / {t["hours"]}</p></div>')
 return html[:s]+direct+html[e:]

# Footer: brand, line and the email as a red outlined button; Company, Units and ITD Labs columns;
# copyright, legal links and the three networks as mono icons with accessible names.
SOCIAL_ICONS={
 'Instagram':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5"/><circle cx="12" cy="12" r="4.1"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg>',
 'LinkedIn':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6.6 10v8M6.6 6.2v.3M10.8 18v-8M10.8 13.6c0-2.3 1.4-3.8 3.3-3.8 2 0 3.1 1.4 3.1 3.8V18"/></svg>',
 'Facebook':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M13.4 21v-7.6h2.6l.4-3.1h-3V8.4c0-.9.3-1.5 1.6-1.5h1.6V4.2c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.3H7.8v3.1h2.6V21z"/></svg>'}
def footer(l,t,page='index'):
 if THEME=='m': return _r6_footer(l,t,page)
 names=dict(zip(PAGES,labels(l)))
 col=lambda title,items:f'<div class="r7-footer-col"><p class="r7-footer-label">{title}</p><ul>'+''.join(f'<li><a href="{route(p,l)}">{n}</a></li>' for p,n in items)+'</ul></div>'
 company=[(p,names[p]) for p in ['index','services','projects','partners']]
 units=[('itd-labs','ITD Labs')]+[(p,names[p]) for p in ['creative','ai-agents','about','contact']]
 lab=[('krakenos','Kraken OS'),('kraken-communications','Kraken Assistant'),('aura','AURA')]
 # The shield beside the name, as in the report (ITD Labs green, Creative and AI in their own colours).
 variant={'creative':'creative','ai-agents':'ai','itd-labs':'labs'}.get(page,'original')
 social=''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{name}">{SOCIAL_ICONS[name]}</a>' for name,url in SOCIAL)
 # On phones the icons follow the email button (report page 16); the copy in the bottom row is for wider screens.
 return (f'<footer class="footer r7-footer"><div class="wrap"><div class="r7-footer-grid"><div class="r7-footer-brand"><a class="brand r7-brand" href="{route("index",l)}"><img src="assets/brand/shield-{variant}.png" width="122" height="146" alt=""><span>IT Department</span></a>'
  f'<p>{t["footer"]}</p><a class="button footer-cta" href="mailto:{cfg["email"]}">{cfg["email"]}</a><div class="r7-social r7-social-phone">{social}</div></div>'
  f'<nav class="r7-footer-nav" aria-label="{tr(l,"Lidhjet në fund të faqes","Footer links","Links im Fußbereich")}">'
  +col(tr(l,'KOMPANIA','COMPANY','UNTERNEHMEN'),company)+col(tr(l,'NJËSITË','UNITS','BEREICHE'),units)+col('ITD LABS',lab)+'</nav></div>'
  f'<div class="footer-bottom"><span>© 2026 IT Department · {t["location"]}</span><div class="r7-legal"><a href="{route("privacy",l)}">{t["privacy"]}</a><a href="{route("terms",l)}">{t["terms"]}</a></div>'
  f'<div class="r7-social r7-social-wide">{social}</div></div></div></footer>')

# AI Agents: each card shows its own character (the report's six variants), split into layers on one canvas
# (assets/ai/agents/<name>/) so it can blink, float 2-4 px and make its own hand gesture.
# Eye centres and hand joints in % of the canvas, measured when the layers were made.
AGENT_NAMES=['ari','dita','nora','leo','mira','fin']
AGENT_RIG={"ari": {"layers": ["foot-l", "foot-r", "body", "eye-l", "eye-r", "hand-l", "hand-r"], "eyes": [{"layer": "eye-l", "x": 49.0, "y": 34.6}, {"layer": "eye-r", "x": 66.5, "y": 29.6}], "hands": [{"layer": "hand-l", "pivot": [23.0, 55.5]}, {"layer": "hand-r", "pivot": [78.9, 40.5]}]},
 "dita": {"layers": ["foot-l", "foot-r", "body", "eye-l", "eye-r", "hand-l"], "eyes": [{"layer": "eye-l", "x": 49.9, "y": 34.3}, {"layer": "eye-r", "x": 66.5, "y": 27.1}], "hands": [{"layer": "hand-l", "pivot": [26.7, 65.3]}]},
 "nora": {"layers": ["foot-l", "foot-r", "body", "eye-l", "eye-r", "hand-l", "hand-r"], "eyes": [{"layer": "eye-l", "x": 48.7, "y": 33.2}, {"layer": "eye-r", "x": 66.3, "y": 29.4}], "hands": [{"layer": "hand-l", "pivot": [23.0, 55.5]}, {"layer": "hand-r", "pivot": [78.9, 45.6]}]},
 "leo": {"layers": ["foot-l", "foot-r", "body", "eye-l", "eye-r", "hand-l", "hand-r"], "eyes": [{"layer": "eye-l", "x": 49.1, "y": 34.2}, {"layer": "eye-r", "x": 66.7, "y": 30.1}], "hands": [{"layer": "hand-l", "pivot": [23.0, 55.5]}, {"layer": "hand-r", "pivot": [78.9, 40.5]}]},
 "mira": {"layers": ["foot-l", "foot-r", "body", "eye-l", "eye-r", "hand-l", "hand-r"], "eyes": [{"layer": "eye-l", "x": 46.9, "y": 33.3}, {"layer": "eye-r", "x": 63.1, "y": 24.1}], "hands": [{"layer": "hand-l", "pivot": [26.7, 65.3]}, {"layer": "hand-r", "pivot": [79.1, 44.3]}]},
 "fin": {"layers": ["foot-l", "foot-r", "body", "eye-l", "eye-r", "hand-l", "hand-r"], "eyes": [{"layer": "eye-l", "x": 49.0, "y": 34.3}, {"layer": "eye-r", "x": 66.3, "y": 30.6}], "hands": [{"layer": "hand-l", "pivot": [23.0, 55.5]}, {"layer": "hand-r", "pivot": [77.0, 55.5]}]}}
def agent_bot(name):
 rig=AGENT_RIG[name]; pivot={e['layer']:(e['x'],e['y']) for e in rig['eyes']}; pivot.update({h['layer']:tuple(h['pivot']) for h in rig['hands']})
 imgs=''.join(f'<img class="ab ab-{x}" src="assets/ai/agents/{name}/{x}.webp" width="216" height="150" alt="" loading="lazy" decoding="async"'+(f' style="transform-origin:{pivot[x][0]}% {pivot[x][1]}%"' if x in pivot else '')+'>' for x in rig['layers'])
 return f'<span class="agent-bot" data-agent-bot="{name}" aria-hidden="true">{imgs}</span>'
def ai(l,t):
 html=_r6_ai(l,t)
 if THEME=='m': return html
 for i,name in enumerate(AGENT_NAMES):
  old=f'<span class="robot robot-{i}">{face(i)}</span>'
  assert old in html, name
  html=html.replace(old,agent_bot(name),1)
 # As on page 14 the card ends with "Shiko detajet +": the separate "Diskuto këtë agjent" link goes
 # (the form further down still lets the visitor choose the agent).
 import re
 html,n=re.subn(r'<a class="text-link" data-agent="[^"]+" href="#brief">[^<]*</a>','',html)
 assert n==6, n
 return html
