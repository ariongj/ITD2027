from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import quote
import json, shutil, hashlib
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
OUT=BASE/"site"
class Node:
 def __init__(self,tag="",attrs=()):
  self.tag=tag; self.attrs=dict(attrs); self.children=[]
 def find(self,tag=None,cls=None):
  out=[]
  for n in self.children:
   if isinstance(n,Node):
    if (not tag or n.tag==tag) and (not cls or cls in n.attrs.get("class","").split()): out.append(n)
    out+=n.find(tag,cls)
  return out
 def text(self): return " ".join(" ".join(c.text() if isinstance(c,Node) else c for c in self.children).split())
class Parser(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True); self.root=Node(); self.stack=[self.root]; self.feed(text)
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs); self.stack[-1].children.append(n)
  if tag not in {"img","input","br","hr","meta","link","source","wbr","area","base","embed","param","track","col"}: self.stack.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag: self.stack=self.stack[:i]; break
 def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs); self.handle_endtag(tag)
 def handle_data(self,data): self.stack[-1].children.append(data)
def esc(s): return escape(str(s),quote=True)
def route(p,l): return p+("" if l=="sq" else "-"+l)+".html"
def source(p,l): return Parser((ROOT/route(p,l)).read_text(encoding="utf-8-sig")).root
def first(n,tag=None,cls=None):
 a=n.find(tag,cls); return a[0].text() if a else ""
def paragraphs(n): return [p.text() for p in n.find("p") if not set(p.attrs.get("class","").split())&{"kicker","eyebrow","ai-kicker","ai-agent-tag"}]
A='<span aria-hidden="true">↗</span>'
cfg=json.loads((ROOT/"site.config.json").read_text(encoding="utf-8-sig"))
T={}
T["sq"]={
"nav":["Shërbimet","Projektet","Rreth nesh"],"talk":"Le të flasim","skip":"Kalo te përmbajtja","menu":"Menyja","close":"Mbyll","location":"Prishtinë, Kosovë","eyebrow":"PARTNERI YT NË TEKNOLOGJI",
"hero":["Teknologji që","e bën punën","më të lehtë."],"intro":"Faqe web, softuer dhe mbështetje IT. I lidhim pjesët që biznesi yt të ecë më qartë, çdo ditë.","cta":"Flasim për biznesin tënd","explore":"Shiko si të ndihmojmë","note":"Fillojmë me një bisedë. Pastaj, me një plan të qartë.",
"art":["PREZENCA JOTE","Faqe që të përfaqëson.","PUNA JOTE","Sisteme që të lidhin.","MBËSHTETJA JOTE","IT që të qëndron pranë."],"artbase":"NJË PARTNER. PJESËT TË LIDHURA.",
"services":"ÇFARË TË DUHET SOT?","serviceHeading":"Nisim nga nevoja jote.","serviceIntro":"Një projekt i ri apo një sistem që kërkon kujdes. Zgjidh pikën nga do të fillojmë.",
"groups":[["Të prezantohem më mirë.","Faqe web, identitet vizual dhe marketing që e bëjnë ofertën tënde të qartë.","Web · Branding · Marketing"],["Ta organizoj punën.","Softuer, aplikacione dhe AI që lidhin ekipin, klientët dhe proceset.","Softuer · Aplikacione · AI"],["Ta kem IT-në në rregull.","Mbështetje, siguri dhe mirëmbajtje për sistemet ku mbështetet biznesi.","IT · Siguri · Mirëmbajtje"]],
"work":"NGA STUDIOJA","workHeading":"Ide me identitet.","workIntro":"Një vështrim në konceptet tona të identitetit vizual. Nga ideja te një gjuhë e plotë e markës.","allwork":"Shiko projektet","concept":"Koncept vizual","view":"Hap brandbook-un",
"process":"SI PUNOJMË","processHeading":"Qartë, nga biseda e parë.","steps":[["Dëgjojmë.","Kuptojmë biznesin, ekipin dhe çfarë të pengon sot."],["Ndërtojmë.","Përcaktojmë prioritetet dhe e kthejmë planin në punë konkrete."],["Qëndrojmë pranë.","Dorëzojmë, shpjegojmë dhe vazhdojmë me mbështetjen që të duhet."]],
"aboutlink":"Njihu me IT Department","ending":"Nuk ke nevojë t’i kesh të gjitha përgjigjet.","endingbody":"Na trego çfarë dëshiron të përmirësosh. Hap pas hapi, e gjejmë pikën e duhur për të filluar.","footer":"Teknologji e menduar për punën tënde.","contact":"Kontakt","privacy":"Privatësia","terms":"Kushtet",
"allservices":"Shërbimet, me një plan të qartë.","servicelead":"Mund të fillojmë me një faqe, një sistem, një auditim apo mbështetje mujore. Hap detajet që të interesojnë.","packages":"Mbështetje mujore IT","packagenote":"Oferta përfundimtare dhe përfshirjet konfirmohen pas analizës së nevojës.","month":"/ muaj","enquire":"Diskuto këtë paketë",
"projectsTitle":"Nga nevoja, te zgjidhja.","projectsLead":"Koncepte vizuale dhe shembuj të llojeve të zgjidhjeve që ndërtojmë.","examples":"Shembuj zgjidhjesh","examplesNote":"Shembuj ilustrues të zgjidhjeve tona, pa të dhëna apo emra klientësh.",
"aboutTitle":"Departamenti yt i teknologjisë.","aboutLead":"Jemi IT Department, ekip teknologjie në Prishtinë. Lidhim faqen web, softuerin, kreativën dhe mbështetjen IT me mënyrën si punon biznesi yt.","faq":"Pyetje të shpeshta",
"aiTitle":"Më pak punë të përsëritur.","aiLead":"Agjentë AI për kërkesa, suport, dokumente dhe raporte. Të lidhur me proceset e tua, me rregulla dhe kontroll njerëzor.","aiguard":"Kontrolli mbetet te ekipi yt.","aiguardbody":"Përcaktojmë burimet e të dhënave, qasjet, aprovimet dhe historikun e veprimeve. Fillojmë me një pilot të kontrolluar.",
"creativeTitle":"Një markë që flet qartë.","creativeLead":"Branding, dizajn, social media dhe marketing. Një drejtim i qëndrueshëm, nga identiteti te materiali i gatshëm për publikim.",
"contactTitle":"Biseda e parë është e thjeshtë.","contactLead":"Na trego për biznesin dhe çfarë dëshiron të përmirësosh. Mund të rezervosh një bisedë ose të përgatitësh një mesazh.",
"book":"Rezervo një bisedë","booknote":"30 minuta · Online · Hap Calendly","write":"Preferon të shkruash?","name":"Emri yt","email":"Emaili yt","interest":"Çfarë të duhet?","choose":"Ende nuk jam i sigurt","message":"Na trego pak më shumë","placeholder":"Çfarë dëshiron të ndërtosh ose të përmirësosh?","prepare":"Përgatit mesazhin","draftnote":"Ky formular përgatit një mesazh. Ti zgjedh ta dërgosh me email ose WhatsApp.","ready":"Mesazhi yt është gati për ta kontrolluar.","sendemail":"Hape në email","sendwa":"Hape në WhatsApp","copy":"Kopjo mesazhin","copied":"Mesazhi u kopjua.","copyfailed":"Kopjimi nuk u lejua. Përzgjidhe dhe kopjoje tekstin më sipër.","edit":"Ndrysho mesazhin","draftstatus":"Asgjë nuk është dërguar automatikisht.","hours":"E hënë–E premte, 09:00–18:00",
"privacyTitle":"Privatësia në këtë version.","privacyBody":"Ky version lokal nuk përdor analytics, reklamim, chat AI apo cookies. Drafti i formularit ruhet në këtë skedë të shfletuesit (sessionStorage), që të mos humbasë gjatë rifreskimit ose ndërrimit të gjuhës. Fshihet kur mbyllet skeda dhe nuk dërgohet te një server. Butoni i përgatitjes shfaq mesazhin për kontroll. Vetëm kur zgjedh email ose WhatsApp, mesazhi kalon te aplikacioni i zgjedhur; dërgimin e konfirmon atje. Calendly, WhatsApp dhe ofruesi i emailit kanë politikat e tyre. Mos shkruaj fjalëkalime ose të dhëna të ndjeshme. Për pyetje: info@itdks.tech.",
"back":"Kthehu në krye","notfound":"Kjo faqe nuk u gjet.","notfoundbody":"Mund të kthehesh në faqen kryesore ose të na kontaktosh.","lang":"Gjuha","more":"Çfarë përfshihet"}
T["en"]={
"nav":["Services","Work","About us"],"talk":"Let’s talk","skip":"Skip to content","menu":"Menu","close":"Close","location":"Prishtina, Kosovo","eyebrow":"YOUR TECHNOLOGY PARTNER",
"hero":["Technology that","makes work","feel simpler."],"intro":"Websites, software and IT support. We connect the pieces so your business can work better, every day.","cta":"Let’s talk about your business","explore":"See how we can help","note":"First, a conversation. Then, a clear plan.",
"art":["YOUR PRESENCE","A website that represents you.","YOUR WORK","Systems that connect you.","YOUR SUPPORT","IT that stays by your side."],"artbase":"ONE PARTNER. ALL THE PIECES CONNECTED.",
"services":"WHAT DO YOU NEED TODAY?","serviceHeading":"Your needs come first.","serviceIntro":"A new project or a system that needs attention. Choose where we begin.",
"groups":[["Make a better impression.","Websites, visual identity and marketing that make your offer clear.","Web · Branding · Marketing"],["Organize the way we work.","Software, apps and AI that connect your team, customers and processes.","Software · Applications · AI"],["Keep our IT in good hands.","Support, security and maintenance for the systems your business relies on.","IT · Security · Maintenance"]],
"work":"FROM THE STUDIO","workHeading":"Ideas with identity.","workIntro":"A look at our visual identity concepts. From an idea to a complete brand language.","allwork":"Explore our work","concept":"Visual concept","view":"Open brandbook",
"process":"HOW WE WORK","processHeading":"Clear, from the first conversation.","steps":[["We listen.","We understand your business, your team and what gets in the way."],["We build.","We agree on priorities and turn the plan into practical work."],["We stay close.","We hand over, explain and continue with the support you need."]],
"aboutlink":"Meet IT Department","ending":"You don’t need to have all the answers.","endingbody":"Tell us what you want to improve. Together, we’ll find the right place to start.","footer":"Technology built around your work.","contact":"Contact","privacy":"Privacy","terms":"Terms",
"allservices":"The right services. A clear plan.","servicelead":"Start with a website, a system, an audit or monthly support. Open the details that matter to you.","packages":"Monthly IT support","packagenote":"The final offer and inclusions are confirmed after assessing your needs.","month":"/ month","enquire":"Discuss this plan",
"projectsTitle":"From a need to a solution.","projectsLead":"Visual concepts and examples of the kinds of solutions we build.","examples":"Solution examples","examplesNote":"Illustrative solution examples, without client names or private information.",
"aboutTitle":"Your technology department.","aboutLead":"We are IT Department, a technology team in Prishtina. We connect websites, software, creative work and IT support with the way your business operates.","faq":"Frequently asked questions",
"aiTitle":"Less repetitive work.","aiLead":"AI agents for enquiries, support, documents and reporting. Connected to your processes, with clear rules and human oversight.","aiguard":"Your team stays in control.","aiguardbody":"We define data sources, permissions, approvals and activity history. We start with a controlled pilot.",
"creativeTitle":"A brand that speaks clearly.","creativeLead":"Branding, design, social media and marketing. A consistent direction, from identity to material ready to publish.",
"contactTitle":"It starts with a conversation.","contactLead":"Tell us about your business and what you want to improve. Book a conversation or prepare a message.",
"book":"Book a conversation","booknote":"30 minutes · Online · Opens Calendly","write":"Prefer to write?","name":"Your name","email":"Your email","interest":"What do you need?","choose":"I’m not sure yet","message":"Tell us a little more","placeholder":"What would you like to build or improve?","prepare":"Prepare your message","draftnote":"This form prepares a message. You choose whether to send it by email or WhatsApp.","ready":"Your message is ready to review.","sendemail":"Open in email","sendwa":"Open in WhatsApp","copy":"Copy message","copied":"Message copied.","copyfailed":"Copy was not allowed. Select and copy the text above.","edit":"Edit message","draftstatus":"Nothing has been sent automatically.","hours":"Monday–Friday, 09:00–18:00",
"privacyTitle":"Privacy in this version.","privacyBody":"This local version uses no analytics, advertising, AI chat or cookies. Your form draft stays in this browser tab (sessionStorage), so refreshing or changing language does not lose your text. It is removed when the tab closes and is not sent to a server. Preparing a message displays it for review. Only when you choose email or WhatsApp is the message passed to that application; you confirm sending there. Calendly, WhatsApp and your email provider have their own policies. Do not enter passwords or sensitive data. Questions: info@itdks.tech.",
"back":"Back to home","notfound":"We couldn’t find that page.","notfoundbody":"Return to the homepage or get in touch.","lang":"Language","more":"What’s included"}
T["de"]={
"nav":["Leistungen","Projekte","Über uns"],"talk":"Kontakt aufnehmen","skip":"Zum Inhalt springen","menu":"Menü","close":"Schließen","location":"Prishtina, Kosovo","eyebrow":"IHR PARTNER FÜR TECHNOLOGIE",
"hero":["Technologie, die","Ihre Arbeit","leichter macht."],"intro":"Websites, Software und IT-Support. Wir verbinden die Bausteine, damit Ihr Unternehmen jeden Tag besser arbeiten kann.","cta":"Sprechen wir über Ihr Unternehmen","explore":"So können wir helfen","note":"Zuerst ein Gespräch. Dann ein klarer Plan.",
"art":["IHR AUFTRITT","Eine Website, die Sie zeigt.","IHRE ARBEIT","Systeme, die Sie verbinden.","IHR SUPPORT","IT, die an Ihrer Seite bleibt."],"artbase":"EIN PARTNER. ALLES VERBUNDEN.",
"services":"WAS BRAUCHEN SIE HEUTE?","serviceHeading":"Ihr Bedarf steht am Anfang.","serviceIntro":"Ein neues Projekt oder ein System, das Aufmerksamkeit braucht. Entscheiden Sie, wo wir anfangen.",
"groups":[["Überzeugender auftreten.","Websites, visuelle Identität und Marketing, die Ihr Angebot verständlich machen.","Web · Branding · Marketing"],["Die Arbeit organisieren.","Software, Apps und KI, die Team, Kunden und Prozesse verbinden.","Software · Anwendungen · KI"],["Die IT in guten Händen.","Support, Sicherheit und Wartung für die Systeme Ihres Unternehmens.","IT · Sicherheit · Wartung"]],
"work":"AUS DEM STUDIO","workHeading":"Ideen mit Identität.","workIntro":"Ein Einblick in unsere visuellen Markenkonzepte. Von der Idee zu einer vollständigen Markensprache.","allwork":"Projekte ansehen","concept":"Visuelles Konzept","view":"Brandbook öffnen",
"process":"SO ARBEITEN WIR","processHeading":"Klar, vom ersten Gespräch an.","steps":[["Wir hören zu.","Wir verstehen Ihr Unternehmen, Ihr Team und die heutigen Hindernisse."],["Wir entwickeln.","Wir legen Prioritäten fest und setzen den Plan Schritt für Schritt um."],["Wir bleiben an Ihrer Seite.","Wir übergeben, erklären und unterstützen Sie auch danach."]],
"aboutlink":"IT Department kennenlernen","ending":"Sie müssen noch nicht alle Antworten haben.","endingbody":"Erzählen Sie uns, was Sie verbessern möchten. Gemeinsam finden wir den richtigen Anfang.","footer":"Technologie für Ihren Arbeitsalltag.","contact":"Kontakt","privacy":"Datenschutz","terms":"Nutzungsbedingungen",
"allservices":"Passende Leistungen. Ein klarer Plan.","servicelead":"Beginnen Sie mit einer Website, einem System, einem Audit oder monatlichem Support. Öffnen Sie die Details, die Sie interessieren.","packages":"Monatlicher IT-Support","packagenote":"Das endgültige Angebot und der Leistungsumfang werden nach der Bedarfsanalyse bestätigt.","month":"/ Monat","enquire":"Paket besprechen",
"projectsTitle":"Vom Bedarf zur Lösung.","projectsLead":"Visuelle Konzepte und Beispiele für die Lösungen, die wir entwickeln.","examples":"Lösungsbeispiele","examplesNote":"Veranschaulichende Lösungsbeispiele ohne Kundennamen oder vertrauliche Informationen.",
"aboutTitle":"Ihre Technologieabteilung.","aboutLead":"Wir sind IT Department, ein Technologieteam in Prishtina. Wir verbinden Websites, Software, Kreativarbeit und IT-Support mit den Abläufen Ihres Unternehmens.","faq":"Häufige Fragen",
"aiTitle":"Weniger Routinearbeit.","aiLead":"KI-Agenten für Anfragen, Support, Dokumente und Berichte. Mit Ihren Prozessen verbunden, mit klaren Regeln und menschlicher Kontrolle.","aiguard":"Ihr Team behält die Kontrolle.","aiguardbody":"Wir definieren Datenquellen, Berechtigungen, Freigaben und Aktivitätsprotokolle. Wir beginnen mit einem kontrollierten Pilotprojekt.",
"creativeTitle":"Eine Marke, die klar spricht.","creativeLead":"Branding, Design, Social Media und Marketing. Eine einheitliche Richtung, von der Identität bis zum fertigen Material.",
"contactTitle":"Es beginnt mit einem Gespräch.","contactLead":"Erzählen Sie uns von Ihrem Unternehmen und Ihren Zielen. Buchen Sie ein Gespräch oder bereiten Sie eine Nachricht vor.",
"book":"Gespräch buchen","booknote":"30 Minuten · Online · Öffnet Calendly","write":"Lieber schriftlich?","name":"Ihr Name","email":"Ihre E-Mail","interest":"Was benötigen Sie?","choose":"Ich bin noch nicht sicher","message":"Erzählen Sie uns mehr","placeholder":"Was möchten Sie entwickeln oder verbessern?","prepare":"Nachricht vorbereiten","draftnote":"Dieses Formular bereitet eine Nachricht vor. Sie entscheiden, ob Sie sie per E-Mail oder WhatsApp senden.","ready":"Ihre Nachricht ist zur Prüfung bereit.","sendemail":"In E-Mail öffnen","sendwa":"In WhatsApp öffnen","copy":"Nachricht kopieren","copied":"Nachricht kopiert.","copyfailed":"Kopieren nicht erlaubt. Markieren und kopieren Sie den Text oben.","edit":"Nachricht bearbeiten","draftstatus":"Es wurde nichts automatisch gesendet.","hours":"Montag–Freitag, 09:00–18:00",
"privacyTitle":"Datenschutz in dieser Version.","privacyBody":"Diese lokale Version verwendet keine Analyse, Werbung, KI-Chats oder Cookies. Ihr Formularentwurf bleibt in diesem Browser-Tab (sessionStorage) erhalten, auch beim Neuladen oder Sprachwechsel. Er wird beim Schließen des Tabs gelöscht und nicht an einen Server gesendet. Die vorbereitete Nachricht wird zur Prüfung angezeigt. Erst wenn Sie E-Mail oder WhatsApp wählen, wird der Text an diese Anwendung übergeben; dort bestätigen Sie das Senden. Calendly, WhatsApp und Ihr E-Mail-Anbieter haben eigene Richtlinien. Geben Sie keine Passwörter oder sensiblen Daten ein. Fragen: info@itdks.tech.",
"back":"Zur Startseite","notfound":"Diese Seite wurde nicht gefunden.","notfoundbody":"Zurück zur Startseite oder nehmen Sie Kontakt auf.","lang":"Sprache","more":"Enthaltene Leistungen"}

for asset in ["assets/brand/logo-shield.png","assets/brand/favicon.png","assets/creative/nexus-brandbook.webp","assets/creative/hyperlink-brandbook.webp"]:
 dest=OUT/asset; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/asset,dest)
shutil.copy2(ROOT/"logo-lockup-tight-480.png",OUT/"assets/brand/logo-original.png")
baseline=BASE/"source-manifest.json"
if not baseline.exists():
 baseline.write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob("*") if p.is_file() and p.suffix in [".html",".css",".js",".php",".json"]},indent=2),encoding="utf-8")

def detail(n,i,l,t):
 title=first(n,"h3") or first(n,"h2"); ps=paragraphs(n); lis=n.find("li")
 body="".join(f'<p>{esc(p)}</p>' for p in ps[:1])
 if lis: body+="<ul>"+''.join(f'<li>{esc(x.text())}</li>' for x in lis)+"</ul>"
 if len(ps)>1: body+=f'<p>{esc(ps[-1])}</p>'
 href=route("contact",l)+"?service="+quote(title)
 return f'<details class="service-detail" id="{esc(n.attrs.get("id","service-"+str(i)))}"><summary><span class="detail-number">{i:02d}</span><h3>{esc(title)}</h3><span class="plus" aria-hidden="true">+</span></summary><div class="detail-body">{body}<a class="text-link" href="{href}">{t["talk"]}{A}</a></div></details>'

def terms(l,t):
 body=""
 for n in source("terms",l).find("article"):
  title=first(n,"h3")
  if title: body+=f'<section><h2>{esc(title)}</h2>'+''.join(f'<p>{esc(p)}</p>' for p in paragraphs(n))+('<ul>'+''.join(f'<li>{esc(x.text())}</li>' for x in n.find("li"))+'</ul>' if n.find("li") else '')+'</section>'
 return intro(t["terms"],"",t)+f'<div class="wrap legal">{body}</div>'

exec(compile((BASE/"proposal.py").read_text(encoding="utf-8-sig"),str(BASE/"proposal.py"),"exec"))
