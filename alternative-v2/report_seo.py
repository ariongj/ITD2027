"""SEO report of 23 October 2026 (ITD_SEO_Raporti_Final_Ekipi_23-10-2026.pdf, pages 2-5).

The <title> of every page in SQ / EN / DE as the report gives it (the visible headings stay); "Find us on Google
Maps" on the contact page opens the business profile; the stable Facebook address in the footer and in schema.org;
the "Review us on Google" link appears in the contact page and the footer once cfg["reviewUrl"] holds the direct
review link from Google Business (Ask for reviews), never the general profile link."""

# Facebook: the profile's stable address instead of the share link, everywhere it is used (links and sameAs).
SOCIAL[:]=[(n,'https://www.facebook.com/people/ITDepartment/61589358992650/' if n=='Facebook' else u) for n,u in SOCIAL]
MAPS_PROFILE='https://share.google/EnL0Qbs1GCVTKIfoY'

SEO_TITLES={
 'index':('Zhvillim Web, Softuer & Automatizim AI | IT Department','Web Development, Software & AI Automation | IT Department','Webentwicklung, Software & KI-Automatisierung | IT Department'),
 'services':('Shërbime Web, AI, IT & Dizajn | IT Department','Web, AI, IT & Design Services | IT Department','Web-, KI-, IT- & Designleistungen | IT Department'),
 'web-software':('Zhvillim Faqesh Web & Softueri | IT Department','Website & Software Development | IT Department','Website- & Softwareentwicklung | IT Department'),
 'ai-automation':('Automatizim me AI për Biznese | IT Department','AI Automation for Business | IT Department','KI-Automatisierung für Unternehmen | IT Department'),
 'projects':('Projekte Web, Softuer & Dizajn | IT Department','Web, Software & Design Projects | IT Department','Web-, Software- & Designprojekte | IT Department'),
 'partners':('Partnerët Tanë | IT Department','Our Partners | IT Department','Unsere Partner | IT Department'),
 'creative':('Branding, Dizajn Grafik & Përmbajtje | IT Department','Branding, Graphic Design & Content | IT Department','Branding, Grafikdesign & Content | IT Department'),
 'ai-agents':('Agjentë AI për Automatizimin e Biznesit | IT Department','AI Agents for Business Automation | IT Department','KI-Agenten für die Geschäftsautomatisierung | IT Department'),
 'about':('Rreth Nesh | IT Department','About Us | IT Department','Über uns | IT Department'),
 'contact':('Kontakt për Web, Softuer & AI | IT Department','Contact Us for Web, Software & AI | IT Department','Kontakt für Web, Software & KI | IT Department'),
 'itd-labs':('ITD Labs | Produkte Softuerike & Inovacion','ITD Labs | Software Products & Innovation','ITD Labs | Softwareprodukte & Innovation'),
 'krakenos':('Kraken OS | Menaxhimi i Biznesit në Një Platformë','Kraken OS | Business Management in One Platform','Kraken OS | Unternehmensverwaltung auf einer Plattform'),
 'kraken-communications':('Kraken Assistant | Komunikimi me Klientët & AI','Kraken Assistant | Customer Communication & AI','Kraken Assistant | Kundenkommunikation & KI'),
 'aura':('AURA | Asistenti Digjital nga ITD Labs','AURA | Digital Assistant by ITD Labs','AURA | Digitaler Assistent von ITD Labs'),
 'terms':('Kushtet e Përdorimit | IT Department','Terms of Use | IT Department','Nutzungsbedingungen | IT Department'),
 'privacy':('Politika e Privatësisë | IT Department','Privacy Policy | IT Department','Datenschutzerklärung | IT Department')}

def seo_title(page,l,html):
 if page=='project-detail':
  # The detail page carries its project's own name, as its heading shows it.
  name=html_unescape(re.sub(r'<[^>]+>','',re.search(r'<h1>(.*?)</h1>',html,re.S).group(1))).strip().rstrip('.')
  return tr(l,f'{name} | Projekte nga IT Department',f'{name} | Projects by IT Department',f'{name} | Projekte von IT Department')
 return tr(l,*SEO_TITLES[page]) if page in SEO_TITLES else None
from html import unescape as html_unescape

def review_link(l,cls):
 url=cfg.get('reviewUrl','')
 if not url: return ''
 return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'+tr(l,'Na vlerëso në Google','Review us on Google','Bewerten Sie uns auf Google')+'<span class="sr-only"> ('+tr(l,'hapet në një skedë të re','opens in a new tab','öffnet in einem neuen Tab')+')</span></a>'

_seo_contact=contact
def contact(l,t):
 html=_seo_contact(l,t)
 if THEME=='m': return html
 old=f'<a class="button" href="https://www.google.com/maps?q=42.655800066393724,21.151119141173435" target="_blank" rel="noopener noreferrer">'+tr(l,'Hap në Google Maps','Open in Google Maps','In Google Maps öffnen')
 assert html.count(old)==1
 return html.replace(old,f'<a class="button" href="{MAPS_PROFILE}" target="_blank" rel="noopener noreferrer">'+tr(l,'Na gjej në Google Maps','Find us on Google Maps','Finden Sie uns auf Google Maps'),1).replace('<a class="button r8-mail"',review_link(l,'button outline')+'<a class="button r8-mail"',1)

_seo_footer=footer
def footer(l,t,page='index'):
 html=_seo_footer(l,t,page)
 if THEME=='m' or not cfg.get('reviewUrl'): return html
 return html.replace('<div class="r7-legal">','<div class="r7-legal">'+review_link(l,'r7-review'),1)

_seo_finalize=finalize
def finalize(html,page,l):
 html=_seo_finalize(html,page,l)
 if THEME=='m': return html
 title=seo_title(page,l,html)
 if not title: return html
 html,n=re.subn(r'<title>.*?</title>',f'<title>{esc(title)}</title>',html,count=1)
 assert n==1
 return re.sub(r'(<meta property="og:title" content=")[^"]*"',lambda m:m.group(1)+esc(title)+'"',html,count=1)
