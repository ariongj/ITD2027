"""SEO checklist for the developer (SEO_Teknik_Checklist_per_Developer.pdf, 20 November 2026), main version only.

Item 07: the contact, privacy and terms pages had the page name as their meta description ("Privacy", "Terms") or a
single short line. Each now summarises what the page holds, built from the page's own intro and section headings; the
same text goes to og:description and to the WebPage description in the structured data. The legal texts are unchanged.
Item 14: phones no longer download images bigger than they show. The sizes of the project cards, project pages and
galleries now describe the width each image really takes (measured from 360 to 1920 px), and the brandbook covers, the
two Labs stage banners and the two Kraken dashboards get smaller WebP variants (made from the same files) with
srcset/sizes. The image on screen is the same picture at the same size; the lightbox still opens the full file.
Item 12: the brandbook covers on the creative pages no longer move while they load between 541 and 800 px (CLS 0.11 -> 0),
see report11.css. The other items were already in place or are handled outside the pages (.htaccess for the one-hop
redirects)."""

SEO_DESCRIPTIONS={
 'contact':('Kontakto IT Department në Prishtinë për web, softuer, IT & siguri, AI ose kreativë: takim 30-minutësh, WhatsApp, kërkesë me shkrim ose email.',
  'Contact IT Department in Prishtina about web, software, IT & security, AI or creative work: a 30-minute meeting, WhatsApp, a written enquiry or email.',
  'Kontaktieren Sie IT Department in Prishtina zu Web, Software, IT-Sicherheit, KI oder Kreativleistungen: 30-Minuten-Gespräch, WhatsApp, schriftliche Anfrage oder E-Mail.'),
 'privacy':('Si i përdorim dhe i mbrojmë të dhënat tuaja në itdks.tech: formulari, rezervimet, Google Analytics e Google Ads, statistikat e faqes, cookies dhe të drejtat tuaja.',
  'How we use and protect your data on itdks.tech: the enquiry form, meeting bookings, Google Analytics and Google Ads, site statistics, cookies and your rights.',
  'Wie wir Ihre Daten auf itdks.tech verwenden und schützen: Anfrageformular, Terminbuchung, Google Analytics und Google Ads, Website-Statistik, Cookies und Ihre Rechte.'),
 'terms':('Rregullat për përdorimin e itdks.tech dhe si nisin shërbimet tona: ofertat dhe kontratat, përmbajtja dhe pronësia, lidhjet, përgjegjësia, pyetjet dhe ankesat.',
  'The rules for using itdks.tech and how our services begin: offers and contracts, content and ownership, links, liability, questions and complaints.',
  'Die Regeln für die Nutzung von itdks.tech und wie unsere Leistungen beginnen: Angebote und Verträge, Inhalte und Rechte, Links, Haftung, Fragen und Beschwerden.')}


_checklist_finalize=finalize
def finalize(html,page,l):
 html=_checklist_finalize(html,page,l)
 if THEME=='m' or page not in SEO_DESCRIPTIONS: return html
 new=tr(l,*SEO_DESCRIPTIONS[page])
 old=html_unescape(re.search(r'<meta name="description" content="([^"]*)">',html).group(1))
 html,n=re.subn(r'<meta name="description" content="[^"]*">',lambda m:f'<meta name="description" content="{esc(new)}">',html,count=1)
 assert n==1
 html,n=re.subn(r'(<meta property="og:description" content=")[^"]*"',lambda m:m.group(1)+esc(new)+'"',html,count=1)
 assert n==1
 # the WebPage node of the JSON-LD, written by share_tags() with json.dumps(..., ensure_ascii=False)
 key='"description": '+json.dumps(old,ensure_ascii=False).replace('</','<\\/')
 assert html.count(key)==1,(page,l,key)
 return html.replace(key,'"description": '+json.dumps(new,ensure_ascii=False).replace('</','<\\/'),1)


# Item 14. Each slot is at least the width the image takes at that viewport (seo checklist audit, 360-1920 px).
SEO_SIZES={
 'card':'(max-width:800px) calc(100vw - 32px), (max-width:1120px) 48vw, 440px',
 'card-wide':'(max-width:1120px) calc(100vw - 32px), 440px',  # third card of the home grid: full width from 801 to 1120 px
 'hero':'(max-width:1100px) calc(100vw - 32px), 1040px',
 'gallery':'(max-width:702px) calc(100vw - 32px), (max-width:976px) 50vw, (max-width:1270px) 38vw, 530px',
 'gallery-second':'(max-width:640px) calc(100vw - 32px), (max-width:702px) calc(100vw - 290px), (max-width:976px) 50vw, (max-width:1270px) 38vw, 530px',
 'gallery-one':'(max-width:640px) calc(100vw - 32px), (max-width:800px) calc(100vw - 290px), (max-width:1270px) calc(100vw - 310px), (max-width:1416px) calc(100vw - 340px), 1072px',
 'brandbook':'(max-width:540px) 50vw, (max-width:800px) 280px, (max-width:1279px) 23vw, 330px',
 'brandbook-card':'(max-width:540px) 54vw, (max-width:800px) 30vw, 290px',  # the same covers in the portfolio grid (lazy)
 'kraken-os-banner':'(max-width:800px) 68vw, (max-width:1150px) 54vw, 605px',
 'kraken-assistant-banner':'(max-width:800px) 46vw, (max-width:1150px) 36vw, 400px',
 'lab-card':'(max-width:800px) 92vw, (max-width:1440px) 28vw, 400px',  # the two Labs cards; was 420px from 801 px, they are 243-399 px
 'theme-first':'(max-width:640px) 92vw, (max-width:1400px) 29vw, 410px',  # ITD Themes on the home page: three in a row from 641 px
 'theme':'(max-width:640px) 46vw, (max-width:1400px) 29vw, 410px',
 'communications-dashboard':'(max-width:1416px) calc(100vw - 32px), 1320px',
 'kraken-dashboard':'(max-width:800px) 86vw, (max-width:1416px) 46vw, 650px'}
SEO_VARIANTS={'brandbook':(480,720),'communications-dashboard':(720,1280),'kraken-dashboard':(720,)}

def _seo_resized(src,name,full):
 base=src[:-5]
 return ', '.join([f'{base}-{w}.webp {w}w' for w in SEO_VARIANTS[name]]+[f'{src} {full}w'])

def _seo_images(html,page,l):
 # project cards (home, projects, the related projects on every project page)
 card='sizes="(max-width:800px) 100vw, 50vw"'
 home=html.find('class="project-grid project-grid-home"')
 parts=html.split(card); out=parts[0]
 for k,rest in enumerate(parts[1:]):
  wide=home>=0 and k==2
  out+=f'sizes="{SEO_SIZES["card-wide" if wide else "card"]}"'+rest
 if home>=0: assert len(parts)==4,(page,l,len(parts))
 html=out
 # the first card of the projects page and the big image of a project page are the largest paint
 if '<body data-page="projects"' in html:
  html,n=re.subn(r'<div class="project-shot"><img src=',lambda m:'<div class="project-shot"><img fetchpriority="high" src=',html,count=1); assert n==1,(page,l)
 html,n=re.subn(r'sizes="\(max-width:1100px\) 100vw, 1040px"( width="\d+" height="\d+" alt="[^"]*") decoding="async"',
  lambda m:f'sizes="{SEO_SIZES["hero"]}"{m.group(1)} decoding="async" fetchpriority="high"',html)
 assert n==(1 if 'pj-gallery' in html else 0),(page,l,n)
 # project galleries: two screenshots and a phone, or one screenshot beside the phone
 i=html.find('<div class="pj-gallery-grid">')
 if i>=0:
  j=html.find('</section>',i); g=html[i:j]; one=g.count('<figure class="pj-fig">')==1
  k=iter(['gallery-one'] if one else ['gallery','gallery-second'])
  g,n=re.subn(r'sizes="\(max-width:800px\) 100vw, 520px"',lambda m:f'sizes="{SEO_SIZES[next(k)]}"',g)
  assert n==g.count('<figure class="pj-fig">') and n in (1,2),(page,l,n)
  html=html[:i]+g+html[j:]
 assert 'sizes="(max-width:800px) 100vw, 520px"' not in html,(page,l)
 # brandbook covers, Labs stage banners, Kraken dashboards
 def add(m,name,srcset):
  return f'<img src="{m.group(1)}" srcset="{srcset}" sizes="{SEO_SIZES[name]}" width="{m.group(2)}"'
 html,nb=re.subn(r'<img src="((?:/?)assets/creative/(?:nexus|hyperlink)-brandbook\.webp)" width="(1024)"(?= height="1536"( loading="lazy")?)',
  lambda m:add(m,'brandbook-card' if m.group(3) else 'brandbook',_seo_resized(m.group(1),'brandbook',1024)),html)
 assert nb==(4 if 'class="creative-books"' in html else 0),(page,l,nb)
 html,ns=re.subn(r'<img src="((?:/?)assets/labs/(kraken-os-banner|kraken-assistant-banner)-(?:sq|en|de)-1200\.webp)" width="(1200)"',
  lambda m:f'<img src="{m.group(1)}" srcset="{m.group(1)[:-10]}-600.webp 600w, {m.group(1)} 1200w" sizes="{SEO_SIZES[m.group(2)]}" width="{m.group(3)}"',html)
 assert ns==(2 if 'stage-win stage-kraken' in html else 0),(page,l,ns)
 html,n=re.subn(r'sizes="\(max-width:800px\) 92vw, 420px"',lambda m:f'sizes="{SEO_SIZES["lab-card"]}"',html)
 assert n==(2 if 'stage-win stage-kraken' in html else 0),(page,l,n)
 for name,full in (('communications-dashboard',2033),('kraken-dashboard',1359)):
  html,n=re.subn(r'<img src="((?:/?)assets/labs/'+name+r'\.webp)" width="('+str(full)+')"',lambda m:add(m,name,_seo_resized(m.group(1),name,full)),html)
  assert n<=1,(page,l,name,n)
 # ITD Themes previews on the home page (the four service images above them turn in the orbit, so they keep their sizes)
 html,n1=re.subn(r'sizes="\(max-width:640px\) 92vw, 380px"',lambda m:f'sizes="{SEO_SIZES["theme-first"]}"',html)
 html,n2=re.subn(r'sizes="\(max-width:640px\) 46vw, 380px"',lambda m:f'sizes="{SEO_SIZES["theme"]}"',html)
 assert (n1,n2) in ((0,0),(1,2)),(page,l,n1,n2)
 return html

_checklist_finalize_images=finalize
def finalize(html,page,l):
 html=_checklist_finalize_images(html,page,l)
 return html if THEME=='m' else _seo_images(html,page,l)
