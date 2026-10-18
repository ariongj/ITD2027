"""Change report 08 (18 October 2026): the round that makes the site ready for publication.

Texts from appendix A in SQ / EN / DE (here for the texts held in T and copy(), and in finalize() for the texts
that come from the original pages), banners in the visitor's language, the orbit on a 5 s JavaScript clock with
a countdown and dragging, the Outfit font, an orientation map on Contact and a WhatsApp button on every page.
Design pieces (orbit, font, map, WhatsApp) belong to the main version only; ITD2027/M keeps its look but shares
the corrected texts. Layout and motion: assets/report08.css, assets/orbit.js and assets/report08.js."""
import atexit, re
_r7_copy=copy
_r7_home=home
_r7_labs=labs
_r7_contact=contact
_r7_footer=footer
_r7_communications=communications
_r7_project_card=project_card

# ---------------------------------------------------------------- texts held in T and copy()
for _l,_v in {
 'sq':{'servicelead':'Zgjidh fushën që të duhet. E sqarojmë nevojën dhe propozojmë një zgjidhje me punë, afate dhe përgjegjësi të përcaktuara.',
  'projectsLead':'Një përzgjedhje e faqeve dhe zgjidhjeve tona. Hap secilin projekt për ta parë nga afër.',
  'examplesNote':'Ky shembull ilustron një rrjedhë të mundshme pune. Nuk paraqet rezultat të matur të një klienti.',
  'aboutLead':'Jemi IT Department, një ekip teknologjie në Prishtinë. Lidhim faqet e internetit, softuerin, kreativën dhe mbështetjen IT me nevojat e biznesit tënd.',
  'creativeLead':'Identitet vizual, përmbajtje dhe fushata digjitale, nga koncepti te materialet që marka jote përdor çdo ditë.',
  'aiLead':'Agjentë AI për kërkesa, mbështetje, dokumente dhe raporte. Të lidhur me proceset e tua, me rregulla të qarta dhe kontroll nga ekipi.',
  'endingbody':'Na trego çfarë dëshiron të përmirësosh. Hapim një bisedë dhe përcaktojmë hapin e parë.',
  'privacyTitle':'Privatësia'},
 'en':{'servicelead':'Choose the area you need. We’ll clarify the requirement and propose a solution with a defined scope, timeline and responsibilities.',
  'projectsLead':'A selection of our websites and solutions. Open each project to explore it.',
  'examplesNote':'This example illustrates a possible workflow. It does not present a measured client result.',
  'aboutLead':'We are IT Department, a technology team in Prishtina. We connect websites, software, creative work and IT support with your business needs.',
  'creativeLead':'Visual identity, content and digital campaigns, from the concept to the materials your brand uses every day.',
  'aiLead':'AI agents for enquiries, support, documents and reports, connected to your workflows with clear rules and team control.',
  'endingbody':'Tell us what you want to improve. We’ll discuss it and agree on a first step.',
  'privacyTitle':'Privacy'},
 'de':{'servicelead':'Wählen Sie den passenden Bereich. Wir klären Ihren Bedarf und schlagen eine Lösung mit festgelegtem Umfang, Zeitplan und Verantwortlichkeiten vor.',
  'projectsLead':'Eine Auswahl unserer Websites und Lösungen. Öffnen Sie das jeweilige Projekt, um es genauer anzusehen.',
  'examplesNote':'Dieses Beispiel veranschaulicht einen möglichen Arbeitsablauf. Es zeigt kein gemessenes Kundenergebnis.',
  'aboutLead':'Wir sind IT Department, ein Technologieteam in Prishtina. Wir verbinden Websites, Software, Kreativarbeit und IT-Support mit den Anforderungen Ihres Unternehmens.',
  'creativeLead':'Visuelle Identität, Inhalte und digitale Kampagnen, vom Konzept bis zu den Materialien, die Ihre Marke täglich nutzt.',
  'aiLead':'KI-Agenten für Anfragen, Support, Dokumente und Berichte, eingebunden in Ihre Abläufe, mit klaren Regeln und Kontrolle durch Ihr Team.',
  'endingbody':'Erzählen Sie uns, was Sie verbessern möchten. Gemeinsam legen wir den ersten Schritt fest.',
  'privacyTitle':'Datenschutz'}}.items(): T[_l].update(_v)

PRIVACY={
 'sq':['Të dhënat që dërgon në formular kalojnë përmes Formspree te IT Department. Drafti ruhet në këtë skedë deri kur kërkesa dërgohet me sukses ose skeda mbyllet.',
  'WhatsApp, Calendly dhe Google Maps kanë politikat e tyre. Harta mund të ngarkohet pas klikimit, duke hapur lidhje me shërbimin e Google Maps.',
  'Fontet shërbehen nga vetë faqja; ngarkimi i tyre nuk kërkon lidhje me Google Fonts.',
  'Matja e vizitave është e çaktivizuar në versionin e kontrolluar. Nëse aktivizohet në publikim, teksti dhe zgjedhja e përdoruesit përditësohen sipas konfigurimit real.',
  'Mos dërgo fjalëkalime ose të dhëna të ndjeshme. Për pyetje: info@itdks.tech.'],
 'en':['Details submitted through a form are sent via Formspree to IT Department. The draft stays in this tab until the enquiry is sent successfully or the tab is closed.',
  'WhatsApp, Calendly and Google Maps have their own policies. The map can load after a click, connecting to the Google Maps service.',
  'Fonts are served by this website; loading them does not require a connection to Google Fonts.',
  'Visit measurement is disabled in the reviewed version. If enabled at launch, the text and user choice must reflect the actual configuration.',
  'Do not send passwords or sensitive information. Questions: info@itdks.tech.'],
 'de':['Formularangaben werden über Formspree an IT Department übermittelt. Der Entwurf bleibt in diesem Tab, bis die Anfrage erfolgreich gesendet oder der Tab geschlossen wird.',
  'WhatsApp, Calendly und Google Maps haben eigene Richtlinien. Die Karte kann nach einem Klick geladen werden; dabei wird eine Verbindung zu Google Maps hergestellt.',
  'Die Schriftdateien werden von dieser Website bereitgestellt. Zum Laden ist keine Verbindung zu Google Fonts erforderlich.',
  'Die Besuchsmessung ist in der geprüften Version deaktiviert. Wird sie beim Start aktiviert, müssen Text und Auswahlmöglichkeit der tatsächlichen Konfiguration entsprechen.',
  'Senden Sie keine Passwörter oder sensiblen Daten. Fragen: info@itdks.tech.']}

COPY08={
 'sq':{'services':'Çfarë do të rregullojmë sot?','projects':'Projekte që kemi realizuar.','partners':'Partnerë me të cilët ndërtojmë.',
  'partnerlead':'Njih partnerët dhe teknologjitë që përdorim në projektet tona, nga infrastruktura te shërbimet digjitale.',
  'about':'Një ekip pranë biznesit tënd.','contact':'Nisemi nga ajo që të duhet.','casebadge':'Skenar demonstrues · Softuer',
  'familydesc':['Faqe interneti dhe mjete digjitale që lidhin klientët, dokumentet dhe punën e ekipit.','Mbështetje teknike, sisteme të mirëmbajtura dhe masa sigurie sipas nevojave të biznesit.','Agjentë për kërkesa, dokumente dhe detyra të përsëritura, me rregulla të qarta dhe miratim nga ekipi.','Identitet vizual, përmbajtje dhe fushata që e paraqesin markën me qartësi.'],
  'stepdesc':['Nisim nga pengesat që has sot në punë.','Përcaktojmë punën, afatet dhe përgjegjësitë.','Ndërtojmë, testojmë dhe ia dorëzojmë ekipit.','Mbledhim reagime, mësojmë dhe vazhdojmë përmirësimet.'],
  'success':'Kërkesa u dërgua. Faleminderit! Do të të kontaktojmë në emailin e dhënë.',
  'failure':'Dërgimi nuk u konfirmua. Teksti yt është ruajtur në këtë skedë. Provo përsëri ose na shkruaj me email.',
  'formnote':'Me dërgimin, të dhënat e kërkesës kalojnë përmes Formspree te IT Department.'},
 'en':{'services':'What can we improve today?','projects':'Projects we have delivered.','partners':'Partners we build with.',
  'partnerlead':'Meet the partners and technologies we work with, from infrastructure to digital services.',
  'about':'A team working alongside your business.','contact':'Let’s start with what you need.','casebadge':'Illustrative example · Software',
  'familydesc':['Websites and digital tools connecting customers, documents and your team’s work.','Technical support, maintained systems and security measures suited to your business.','Agents for enquiries, documents and recurring tasks, with clear rules and team approval.','Visual identity, content and campaigns that communicate your brand clearly.'],
  'stepdesc':['We start with what gets in the way of your work today.','We define the scope, timeline and responsibilities.','We build, test and hand over to your team.','We gather feedback, learn and continue improving.'],
  'success':'Your enquiry has been sent. Thank you. We’ll contact you at the email address provided.',
  'failure':'Delivery was not confirmed. Your text is saved in this tab. Try again or email us.',
  'invalid':'Complete this field.',
  'formnote':'When you submit, your enquiry details are sent through Formspree to IT Department.'},
 'de':{'services':'Was können wir für Sie verbessern?','projects':'Projekte, die wir umgesetzt haben.','partners':'Partner, mit denen wir Lösungen entwickeln.',
  'partnerlead':'Lernen Sie die Partner und Technologien kennen, mit denen wir arbeiten, von der Infrastruktur bis zu digitalen Diensten.',
  'about':'Ein Team an der Seite Ihres Unternehmens.','contact':'Sprechen wir über Ihr Vorhaben.','casebadge':'Beispielszenario · Software',
  'familydesc':['Websites und digitale Werkzeuge, die Kunden, Dokumente und die Arbeit Ihres Teams verbinden.','Technischer Support, gepflegte Systeme und Sicherheitsmaßnahmen passend zu Ihrem Unternehmen.','Agenten für Anfragen, Dokumente und wiederkehrende Aufgaben, mit klaren Regeln und Freigaben durch Ihr Team.','Visuelle Identität, Inhalte und Kampagnen, die Ihre Marke klar vermitteln.'],
  'stepdesc':['Wir beginnen mit den Hindernissen in Ihrem Arbeitsalltag.','Wir legen Umfang, Zeitplan und Zuständigkeiten fest.','Wir entwickeln, testen und übergeben die Lösung an Ihr Team.','Wir sammeln Rückmeldungen, lernen daraus und entwickeln die Lösung weiter.'],
  'success':'Ihre Anfrage wurde gesendet. Vielen Dank. Wir melden uns unter der angegebenen E-Mail-Adresse.',
  'failure':'Der Versand wurde nicht bestätigt. Ihr Text ist in diesem Tab gespeichert. Versuchen Sie es erneut oder schreiben Sie uns eine E-Mail.',
  'formnote':'Beim Senden werden die Angaben Ihrer Anfrage über Formspree an IT Department übermittelt.'}}
def copy(l):
 c=_r7_copy(l); c.update(COPY08[l])
 # The privacy page shows c["privacy"] in one paragraph: the four topics of appendix A as separate paragraphs.
 c['privacy']='</p><p>'.join(PRIVACY[l])
 return c

# ---------------------------------------------------------------- texts that come from the original pages
# Exact old text → new text per language, applied to every page of that language when it is written.
FIN={
 'sq':[
  ('Rezultat: klienti kupton më shpejt çfarë ofron dhe si të kontaktojë.','Rezultat: strukturë e qartë, përmbajtje e lexueshme dhe rrugë e thjeshtë drejt kontaktit.'),
  ('Rezultat: punë më e organizuar, më pak hapa manualë dhe raportim më i qartë.','Rezultat: kërkesa, dokumente dhe përgjegjësi të organizuara në një rrjedhë të përbashkët pune.'),
  ('Rezultat: aplikacion me funksione të qarta për klientët ose stafin.','Rezultat: funksione të përcaktuara sipas proceseve dhe përdoruesve të biznesit.'),
  ('Rezultat: pajisje, qasje dhe sisteme më të rregullta.','Rezultat: një pikë kontakti për pajisjet, përdoruesit dhe mirëmbajtjen e sistemeve.'),
  ('Rezultat: qasje më të kontrolluara dhe të dhëna më të mbrojtura.','Rezultat: masa për mbrojtjen e qasjes, të dhënave dhe vazhdimësisë së punës.'),
  ('Rezultat: plan i thjeshtë për çfarë duhet rregulluar së pari.','Rezultat: pamje e gjendjes aktuale dhe plan përmirësimi me prioritete të qarta.'),
  ('Rezultat: markë më e qartë dhe më e njëtrajtshme.','Rezultat: një identitet vizual i qëndrueshëm në materialet dhe kanalet e markës.'),
  ('Rezultat: marketing me mesazh, kanal dhe matje të qarta.','Rezultat: përmbajtje dhe fushata të organizuara sipas audiencës, kanaleve dhe objektivave.'),
  ('<h3>Data</h3>','<h3>Të dhëna</h3>'),
  ('Përgjigjet në interesime, mbledh detaje dhe përgatit hapat e radhës.','Përgjigjet në interesime, mbledh detajet dhe përgatit hapat e radhës për ekipin.'),
  ('Lexon tabela, CRM dhe dokumente, pastaj nxjerr përmbledhje të lehta për t&#x27;u kuptuar.','Lexon tabela, CRM dhe dokumente, pastaj përgatit përmbledhje të qarta për ekipin.'),
  ('Ndjek detyra, afate dhe aprovime, që puna të mbetet e organizuar.','Ndjek detyrat, afatet dhe miratimet, që puna të mbetet e organizuar.'),
  ('I kthen rregullat, procedurat dhe dokumentet në përgjigje që ekipi i gjen më lehtë.','I kthen dokumentet dhe procedurat në përgjigje që ekipi i gjen më lehtë.'),
  ('Mbledh shifra, pagesa dhe status projekte, pastaj përgatit raport të lexueshëm.','Mbledh shifrat, pagesat dhe gjendjen e projekteve në raporte të lexueshme.'),
  ('<li>Rendit kërkesat</li>','<li>Organizon kërkesat</li>'),('<li>Dërgon përgjigje të para</li>','<li>Përgatit përgjigje</li>'),('<li>Kujton ndjekjet pasuese</li>','<li>Kujton ndjekjen e tyre</li>'),
  ('A merreni vetëm me IT apo edhe me automatizim dhe AI?','A ofroni vetëm IT apo edhe automatizim dhe AI?'),
  ('Po. I lidhim IT-në, automatizimin, raportimin, sigurinë dhe AI-në kur kjo e bën punën më të lehtë.','Përveç IT-së, ofrojmë automatizim dhe AI kur i përshtaten nevojës së projektit. I lidhim me raportimin, sigurinë dhe proceset e ekipit.'),
  ('A mund të fillojmë me auditim përpara një projekti më të madh?','A mund të nisim me një audit para një projekti më të madh?'),
  ('Po. Auditim fillestar na ndihmon të kuptojmë gjendjen reale, rreziqet dhe prioritetet para zbatimit.','Po. Një audit fillestar na ndihmon të kuptojmë gjendjen aktuale, rreziqet dhe prioritetet para zbatimit.'),
  ('Varet nga fusha dhe kompleksiteti. Një faqe web mund të ecë më shpejt, ndërsa një sistem i brendshëm, auditim i plotë ose implementim sigurie kërkon analizë, testim dhe dorëzim më të kontrolluar.','Afati varet nga puna dhe kompleksiteti. E përcaktojmë pas analizës, bashkë me fazat e testimit dhe dorëzimit.'),
  ('Përmbajtja në faqe është për informim. Çmimet, afatet dhe zgjidhjet konfirmohen vetëm pas analizës së kërkesës.','Përmbajtja e faqes shërben për informim. Çmimet, afatet dhe zgjidhja përfundimtare konfirmohen pas shqyrtimit të kërkesës.'),
  ('Çdo bashkëpunim fillon me bisedë, analizë dhe marrëveshje të qartë mbi punën, afatet dhe përgjegjësitë.','Çdo bashkëpunim nis me një marrëveshje të qartë për punën, afatet dhe përgjegjësitë. Ndryshimet konfirmohen para zbatimit.'),
  ('Faqja duhet përdorur normalisht dhe pa veprime që dëmtojnë sigurinë, funksionimin ose përmbajtjen e saj.','Përdore faqen pa veprime që dëmtojnë sigurinë, funksionimin ose përmbajtjen e saj.'),
  ('Faqja mund të hapë WhatsApp, Calendly, Formspree ose Google Maps. Këto platforma kanë rregullat e tyre të përdorimit.','Linkat e jashtëm hapin shërbime me kushte dhe politika të veçanta. Na kontakto nëse një link nuk funksionon.')],
 'en':[
  ('Result: clearer communication and stronger trust.','Result: clear structure, readable content and a straightforward path to contact.'),
  ('Result: faster processes, fewer mistakes, and more accurate reporting.','Result: enquiries, documents and responsibilities organised in a shared workflow.'),
  ('Result: a solution that gets used every day, not a project that sits unused.','Result: functions defined around your business processes and users.'),
  ('Result: fewer work interruptions and more stable operations.','Result: one point of contact for devices, users and system maintenance.'),
  ('Result: lower risk, stronger continuity, and better reputation protection.','Result: measures to protect access, data and business continuity.'),
  ('Result: technical clarity and better-informed decisions.','Result: a review of the current setup and an improvement plan with clear priorities.'),
  ('Result: a clearer and more professional presence at every point of contact.','Result: a consistent visual identity across your brand’s materials and channels.'),
  ('Result: more disciplined communication, more controlled growth, and decisions based on performance.','Result: content and campaigns organised around your audience, channels and objectives.'),
  ('<h3>Sales</h3>','<h3>Enquiries</h3>'),
  ('Talks to new clients, collects details and keeps interest from getting lost.','Responds to enquiries, collects details and prepares the next steps for your team.'),
  ('Reads sheets, CRM and documents, then turns them into answers people understand fast.','Reads spreadsheets, CRM data and documents, then prepares clear summaries for your team.'),
  ('Answers common questions and prepares the cases your team needs to handle.','Answers common questions and passes cases requiring a decision to your team.'),
  ('Tracks tasks, deadlines and approvals so work does not stay buried in messages.','Tracks tasks, deadlines and approvals to keep work organised.'),
  ('Becomes the internal helper for rules, procedures, documents and company knowledge.','Turns documents and procedures into answers your team can find more easily.'),
  ('Collects numbers, payments and project status into readable management reports.','Brings figures, payments and project status together in readable reports.'),
  ('<li>Qualifies leads</li>','<li>Organises enquiries</li>'),('<li>Sends first replies</li>','<li>Drafts replies</li>'),('<li>Sends follow-up reminders</li>','<li>Reminds the team to follow up</li>'),
  ('Do you only handle IT, or also automation and AI?','Do you provide IT services only, or automation and AI as well?'),
  ('Yes. We connect IT, automation, reporting, security, and AI when that makes work easier.','Alongside IT services, we offer automation and AI where they fit the project. We connect them with reporting, security and team workflows.'),
  ('Yes. An initial audit helps us understand the real situation, the risks, and the priorities before implementation.','Yes. An initial audit helps us understand the current setup, risks and priorities before implementation.'),
  ('It depends on the area and complexity. A website may move faster, while an internal system, a full audit, or a security implementation requires analysis, testing, and a more controlled delivery.','The timeline depends on scope and complexity. We agree it after discovery, including testing and handover stages.'),
  ('The content on this site is for general information. Prices, timelines, and solutions are confirmed only after we review the request.','Website content is provided for information. Prices, timelines and the final solution are confirmed after we review the enquiry.'),
  ('Every collaboration starts with a conversation, analysis, and a clear agreement on scope, timelines, and responsibilities.','Each collaboration starts with a clear agreement on scope, timeline and responsibilities. Changes are confirmed before implementation.'),
  ('The site should be used normally and without actions that harm security, performance, or content.','Use the website without actions that harm its security, operation or content.'),
  ('The site may open WhatsApp, Calendly, Formspree, or Google Maps. These platforms have their own terms and privacy rules.','External links open services with their own terms and policies. Contact us if a link does not work.'),
  ('>Explore product<','>View product<')],
 'de':[
  ('Ergebnis: klarere Kommunikation und stärkeres Vertrauen.','Ergebnis: klare Struktur, gut lesbare Inhalte und ein einfacher Weg zur Kontaktaufnahme.'),
  ('Ergebnis: schnellere Prozesse, weniger Fehler und genaueres Reporting.','Ergebnis: Anfragen, Dokumente und Zuständigkeiten in einem gemeinsamen Arbeitsablauf.'),
  ('Ergebnis: eine Lösung, die täglich genutzt wird, nicht ein Projekt, das ungenutzt bleibt.','Ergebnis: Funktionen, die sich an Ihren Geschäftsprozessen und Nutzern orientieren.'),
  ('Ergebnis: weniger Arbeitsunterbrechungen und stabilerer Betrieb.','Ergebnis: eine Anlaufstelle für Geräte, Nutzer und die Wartung Ihrer Systeme.'),
  ('Ergebnis: geringeres Risiko, stärkere Kontinuität und besserer Reputationsschutz.','Ergebnis: Maßnahmen zum Schutz von Zugängen, Daten und der Betriebsfähigkeit.'),
  ('Ergebnis: technische Klarheit und besser informierte Entscheidungen.','Ergebnis: ein Überblick über den aktuellen Stand und ein Verbesserungsplan mit klaren Prioritäten.'),
  ('Ergebnis: ein klarerer und professionellerer Auftritt an jedem Kontaktpunkt.','Ergebnis: eine einheitliche visuelle Identität über die Materialien und Kanäle Ihrer Marke hinweg.'),
  ('Ergebnis: diszipliniertere Kommunikation, kontrollierteres Wachstum und Entscheidungen auf Basis von Performance.','Ergebnis: Inhalte und Kampagnen, abgestimmt auf Zielgruppen, Kanäle und Ziele.'),
  ('<h3>Vertrieb</h3>','<h3>Anfragen</h3>'),
  ('Spricht mit neuen Kunden, sammelt Details und verhindert, dass Interesse verloren geht.','Beantwortet Anfragen, sammelt Details und bereitet die nächsten Schritte für Ihr Team vor.'),
  ('Liest Tabellen, CRM und Dokumente und macht daraus verständliche Antworten.','Liest Tabellen, CRM-Daten und Dokumente und erstellt verständliche Zusammenfassungen für Ihr Team.'),
  ('Beantwortet häufige Fragen und bereitet Fälle für Ihr Team vor.','Beantwortet häufige Fragen und leitet Fälle, die eine Entscheidung erfordern, an Ihr Team weiter.'),
  ('Verfolgt Aufgaben, Fristen und Freigaben, damit Arbeit nicht in Chats liegen bleibt.','Verfolgt Aufgaben, Fristen und Freigaben, damit die Arbeit organisiert bleibt.'),
  ('Hilft intern bei Regeln, Abläufen, Dokumenten und Unternehmenswissen.','Macht Informationen aus Dokumenten und Abläufen für Ihr Team leichter zugänglich.'),
  ('Sammelt Zahlen, Zahlungen und Projektstatus in lesbare Managementberichte.','Fasst Kennzahlen, Zahlungen und Projektstände in übersichtlichen Berichten zusammen.'),
  ('<li>Qualifiziert Leads</li>','<li>Ordnet Anfragen</li>'),('<li>Sendet erste Antworten</li>','<li>Bereitet Antworten vor</li>'),('<li>Erinnert an Follow-ups</li>','<li>Erinnert an die Nachverfolgung</li>'),
  ('Machen Sie nur IT oder auch Automatisierung und KI?','Bieten Sie nur IT-Leistungen oder auch Automatisierung und KI an?'),
  ('Ja. Wir verbinden IT, Automatisierung, Reporting, Sicherheit und KI, wenn dadurch die Arbeit leichter wird.','Neben IT-Leistungen bieten wir Automatisierung und KI an, wenn sie zum Projekt passen. Wir verbinden sie mit Reporting, Sicherheit und den Abläufen Ihres Teams.'),
  ('Können wir vor einem größeren Projekt mit einem Audit starten?','Können wir vor einem größeren Projekt mit einem Audit beginnen?'),
  ('Ja. Ein erster Audit hilft, die echte Situation, Risiken und Prioritäten vor der Umsetzung zu verstehen.','Ja. Ein erstes Audit hilft uns, den aktuellen Stand, Risiken und Prioritäten vor der Umsetzung zu verstehen.'),
  ('Das hängt vom Bereich und der Komplexität ab. Eine Website kann schneller gehen, während ein internes System, ein vollständiger Audit oder eine Sicherheitsumsetzung Analyse, Tests und kontrollierte Lieferung braucht.','Der Zeitplan hängt von Umfang und Komplexität ab. Wir legen ihn nach der Analyse fest, einschließlich Tests und Übergabe.'),
  ('Die Inhalte dieser Website dienen allgemeinen Informationen. Preise, Zeitpläne und Lösungen werden erst nach Prüfung der Anfrage bestätigt.','Die Inhalte dieser Website dienen der Information. Preise, Zeitpläne und die endgültige Lösung werden nach Prüfung der Anfrage bestätigt.'),
  ('Jede Zusammenarbeit startet mit Gespräch, Analyse und klarer Vereinbarung zu Umfang, Zeitplan und Verantwortlichkeiten.','Jede Zusammenarbeit beginnt mit einer klaren Vereinbarung zu Umfang, Zeitplan und Verantwortlichkeiten. Änderungen werden vor der Umsetzung bestätigt.'),
  ('Die Website soll normal genutzt werden, ohne Handlungen, die Sicherheit, Performance oder Inhalte schädigen.','Nutzen Sie die Website ohne Handlungen, die Sicherheit, Betrieb oder Inhalte beeinträchtigen.'),
  ('Die Website kann WhatsApp, Calendly, Formspree oder Google Maps öffnen. Diese Plattformen haben eigene Bedingungen und Datenschutzregeln.','Externe Links führen zu Diensten mit eigenen Bedingungen und Richtlinien. Kontaktieren Sie uns, falls ein Link nicht funktioniert.')]}
FIN_HITS={(l,i):0 for l in FIN for i in range(len(FIN[l]))}
# Albanian: one terminology (miratim, mbështetje) everywhere, as on page 21.
SQ_TERMS=[(r'\bSuport prioritar\b','Mbështetje prioritare'),(r'\bSuport\b','Mbështetje'),(r'\bsuport\b','mbështetje'),(r'\bAprovim','Miratim'),(r'\baprovim','miratim')]
def finalize(html,page,l):
 for i,(old,new) in enumerate(FIN[l]):
  if old in html: FIN_HITS[(l,i)]+=1; html=html.replace(old,new)
 if l=='sq':
  for pat,new in SQ_TERMS: html=re.sub(pat,new,html)
 return html
@atexit.register
def _report_unused():
 unused=[f'{l}: {FIN[l][i][0][:70]}' for (l,i),n in FIN_HITS.items() if n==0]
 if unused: print('report08: texts not found:\n  '+'\n  '.join(unused))

# ---------------------------------------------------------------- home
# The four service banners in the visitor's language (the brand line "IT Department / Your Technology Partner"
# stays in English); the orbit turns on a 5 s JavaScript clock with a countdown under the card.
BANNER_ALT={
 'web':('Web & softuer. Ndërtuar për biznesin tënd. Webfaqe. Aplikacione. Softuer biznesi.','Web & Software. Built for your business. Websites. Apps. Business software.','Web & Software. Für Ihr Unternehmen. Websites. Apps. Unternehmenssoftware.'),
 'it':('IT & siguri. Puno i sigurt. Vazhdo përpara. Mbështetje IT. Siguri kibernetike. Auditime IT.','IT & Security. Stay secure. Keep moving. IT support. Cybersecurity. IT audits.','IT & Sicherheit. Sicher bleiben. Weiterkommen. IT-Support. Cybersicherheit. IT-Audits.'),
 'ai':('Agjentë AI. Më pak rutinë. Më shumë kontroll. Procese me AI. Kontroll njerëzor.','AI Agents. Less busywork. More control. AI workflows. Human oversight.','KI-Agenten. Weniger Routine. Mehr Kontrolle. KI-Workflows. Menschliche Kontrolle.'),
 'creative':('Kreativa. Jepi forcë markës tënde. Identitet marke. Përmbajtje. Fushata digjitale.','Creative. Make your brand matter. Brand identity. Content. Digital campaigns.','Kreativ. Stärken Sie Ihre Marke. Markenidentität. Content. Digitale Kampagnen.')}
def orbit(l):
 if THEME=='m': return ''
 cards=''; dots=''
 for i,(key,page,anchor,label,words) in enumerate(SERVICE_SLIDES):
  name=tr(l,*label); place=ORBIT_PLACES[i]
  hidden='' if i==0 else ' aria-hidden="true" tabindex="-1"'
  img=f'assets/home/service-{key}-{l}'
  cards+=(f'<a class="orbit-card {place}" href="{route(page,l)}{anchor}" data-slide data-label="0{i+1} / {name}" draggable="false"{hidden}>'
   f'<img src="{img}-1600.webp" srcset="{img}-800.webp 800w, {img}-1600.webp 1600w" sizes="(max-width:800px) 92vw, 700px" width="1600" height="900" alt="IT Department — {tr(l,*BANNER_ALT[key])}" draggable="false" decoding="async"{" loading=lazy" if place=="is-back" else ""}></a>')
  dots+=f'<button type="button" class="slider-dot" aria-controls="orbit-slides" aria-label="{tr(l,"Slajdi","Slide","Folie")} {i+1}: {name}"{" aria-current=true" if i==0 else ""}><span class="slider-bar"><span class="slider-fill"></span></span></button>'
 pause=tr(l,('Ndalo ndërrimin automatik','Nis ndërrimin automatik'),('Pause automatic rotation','Start automatic rotation'),('Automatischen Wechsel anhalten','Automatischen Wechsel starten'))
 return (f'<section class="r7-orbit" aria-roledescription="{tr(l,"prezantim me slajde","carousel","Karussell")}" aria-label="{tr(l,"Shërbimet tona","Our services","Unsere Leistungen")}" data-orbit>'
  f'<button type="button" class="orbit-pause" data-pause="{pause[0]}" data-play="{pause[1]}">{pause[0]}</button>'
  f'<div class="orbit-stage" id="orbit-slides" aria-live="off">{cards}</div>'
  f'<div class="orbit-controls" hidden><div class="slider-dots">{dots}</div><p class="orbit-countdown" aria-hidden="true" data-countdown>05 s</p>'
  f'<p class="orbit-caption" aria-hidden="true" data-caption>01 / {tr(l,*SERVICE_SLIDES[0][3])}</p></div></section>')

def home(l,t):
 html=_r7_home(l,t)
 if THEME=='m': return html
 c=copy(l)
 # Appendix A: an introduction for the four areas, the projects and the partners.
 areas=heading(labels(l)[1],tr(l,'Katër fusha. Një ekip që i lidh.','Four areas. One team to connect them.','Vier Bereiche. Ein Team, das sie verbindet.'))
 assert html.count('<section class="wrap pillars">')==1
 html=html.replace('<section class="wrap pillars">','<section class="wrap pillars r8-areas">'+areas,1)
 for title,desc in [(c['selected'],tr(l,'Shiko disa nga faqet dhe zgjidhjet që kemi realizuar.','Explore selected websites and solutions we have built.','Entdecken Sie ausgewählte Websites und Lösungen, die wir umgesetzt haben.')),
  (tr(l,'Njerëzit dhe platformat me të cilat ndërtojmë.','The people and platforms we build with.','Menschen und Plattformen, mit denen wir Lösungen entwickeln.'),tr(l,'Partnerë dhe teknologji që mbështesin punën tonë.','Partners and technologies that support our work.','Partner und Technologien, die unsere Arbeit unterstützen.'))]:
  old=f'<h2>{esc(title)}</h2>'; assert html.count(old)==1, title
  html=html.replace(old,old+f'<p>{esc(desc)}</p>',1)
 return html

# Projects: each card ends with "Shiko faqen" (the card itself remains the link to the live site).
def project_card(p,l,tag='h2',lazy=True):
 html=_r7_project_card(p,l,tag,lazy)
 if THEME=='m': return html
 return html.replace('<span class="sr-only">',f'<span class="project-cta">{tr(l,"Shiko faqen","Visit website","Website ansehen")}</span><span class="sr-only">',1)

# ---------------------------------------------------------------- ITD Labs and Kraken Assistant
LAB_BANNER_ALT={'kraken-card':('kraken-os-banner',('Biznesi yt. I ndërlidhur. Klientë, projekte dhe financa. Një platformë.','Your business. Connected. Clients, projects and finance. One platform.','Ihr Unternehmen. Vernetzt. Kunden, Projekte und Finanzen. Eine Plattform.'),(1200,510)),
 'communications-card':('kraken-assistant-banner',('Çdo bisedë. Një kuti hyrëse. Asistencë me AI. Ekipi yt në kontroll.','Every conversation. One inbox. AI assistance. Your team in control.','Jedes Gespräch. Ein Posteingang. KI-Unterstützung. Ihr Team behält die Kontrolle.'),(1200,509))}
def lab_image(img,name,l):
 if THEME=='m' or img not in LAB_BANNER_ALT: return _r6_lab_image(img,name,l)
 key,words,(w,h)=LAB_BANNER_ALT[img]; f=f'assets/labs/{key}-{l}'
 return f'src="{f}-1200.webp" srcset="{f}-600.webp 600w, {f}-1200.webp 1200w" sizes="(max-width:800px) 92vw, 420px" alt="{name} — {tr(l,*words)}" width="{w}" height="{h}" loading="lazy" decoding="async"'
def labs_stage(l):
 bar=lambda label:f'<span class="stage-bar"><i></i><i></i><i></i><b>{label}</b></span>'
 return ('<div class="labs-stage" aria-hidden="true">'
  f'<figure class="stage-win stage-kraken">{bar("KRAKEN OS / WORKSPACE")}<img src="assets/labs/kraken-os-banner-{l}-1200.webp" width="1200" height="510" alt="" decoding="async"></figure>'
  f'<figure class="stage-win stage-comms">{bar("KRAKEN ASSISTANT")}<img src="assets/labs/kraken-assistant-banner-{l}-1200.webp" width="1200" height="509" alt="" decoding="async"></figure>'
  '<figure class="stage-aura"><img src="assets/labs/aura-emblem.svg" width="200" height="200" alt=""><strong>AURA</strong><small>Say it. Consider it handled.</small></figure>'
  f'<span class="labs-badge">{LABS_FLASK}</span></div>')
def labs(l,t):
 html=_r7_labs(l,t)
 if THEME=='m': return html
 # AURA's status under its text (appendix A, ITD Labs).
 status=tr(l,'Pamje paraprake. Linku publik do të shtohet kur të jetë gati.','Preview. A public link will be added when available.','Vorschau. Ein öffentlicher Link wird ergänzt, sobald er verfügbar ist.')
 html,n=re.subn(r'(<div class="aura-showcase"><div>.*?</h2><p>.*?</p>)',lambda m:m.group(1)+f'<p class="r8-status">{status}</p>',html,count=1,flags=re.S)
 assert n==1
 return html
def communications(l,t):
 html=_r7_communications(l,t)
 if THEME=='m': return html
 # The product's own address as a clear action, and a title over the three points.
 old=f'<p class="official-row">{official("assistant.krakenos.cloud",l)}</p>'; assert old in html
 cta=(f'<p class="official-row"><a class="button r8-open" href="https://assistant.krakenos.cloud/" target="_blank" rel="noopener noreferrer">'
  f'{tr(l,"Hap Kraken Assistant","Open Kraken Assistant","Kraken Assistant öffnen")}<span class="sr-only"> ({tr(l,"hapet në një skedë të re","opens in a new tab","öffnet in einem neuen Tab")})</span></a></p>')
 html=html.replace(old,cta,1)
 grid='<section class="wrap section"><div class="grid three">'; assert grid in html
 return html.replace(grid,'<section class="wrap section">'+heading('KRAKEN ASSISTANT',tr(l,'Bisedat e ekipit, në një vend.','Your team’s conversations in one place.','Die Gespräche Ihres Teams an einem Ort.'))+'<div class="grid three">',1)

# ---------------------------------------------------------------- contact: title and orientation map
MAP_Q='42.655800066393724,21.151119141173435'
def contact(l,t):
 html=_r7_contact(l,t)
 if THEME=='m': return html
 c=copy(l); old=f'<h1>{esc(c["contact"])}</h1>'; assert html.count(old)==1
 html=html.replace(old,f'<h1>{tr(l,"Flasim për projektin tënd.","Let’s discuss your project.","Sprechen wir über Ihr Projekt.")}</h1>',1)
 link=f'https://www.google.com/maps?q={MAP_Q}'
 embed=f'https://www.google.com/maps?q={MAP_Q}&amp;z=15&amp;output=embed'
 return html+(f'<section class="wrap section r8-map" aria-labelledby="map-title"><h2 id="map-title">{tr(l,"Na gjen në Prishtinë.","Find us in Prishtina.","Sie finden uns in Prishtina.")}</h2>'
  f'<div class="r8-map-grid"><div class="r8-map-frame" data-map="{embed}" data-map-title="{tr(l,"Harta: vendndodhje orientuese në Prishtinë","Map: approximate location in Prishtina","Karte: ungefähre Lage in Prishtina")}">'
  f'<div class="r8-map-sketch"><span class="r8-pin" aria-hidden="true"></span><span class="r8-pin-label">{tr(l,"Prishtinë / orientuese","Prishtina / approximate","Prishtina / ungefähr")}</span>'
  f'<button type="button" class="button outline r8-map-load" data-map-load>{tr(l,"Shfaq hartën","Show map","Karte anzeigen")}</button>'
  f'<small>{tr(l,"Harta ngarkohet nga Google Maps pas klikimit.","The map loads from Google Maps after you click.","Die Karte wird nach dem Klick von Google Maps geladen.")}</small></div></div>'
  f'<div class="r8-map-copy"><h3>{t["location"]}</h3><p>{tr(l,"Vendndodhje orientuese në Prishtinë, Kosovë. Për vizitë, na kontakto që ta konfirmojmë adresën.","Approximate location in Prishtina, Kosovo. Contact us to confirm the address before visiting.","Ungefähre Lage in Prishtina, Kosovo. Bitte kontaktieren Sie uns vor einem Besuch, um die Adresse zu bestätigen.")}</p>'
  f'<div class="r8-map-actions"><a class="button" href="{link}" target="_blank" rel="noopener noreferrer">{tr(l,"Hap në Google Maps","Open in Google Maps","In Google Maps öffnen")}<span class="sr-only"> ({tr(l,"hapet në një skedë të re","opens in a new tab","öffnet in einem neuen Tab")})</span></a>'
  f'<a class="button r8-mail" href="mailto:{cfg["email"]}">{cfg["email"]}</a></div></div></div></section>')

# ---------------------------------------------------------------- WhatsApp on every page
WA_ICON=('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path d="M16 4.5A11.5 11.5 0 0 0 6.1 21.8L4.6 27.4l5.8-1.5A11.5 11.5 0 1 0 16 4.5Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
 '<path d="M12.2 10.4c.4-.3 1-.2 1.2.3l1.1 2.5c.2.4.1.8-.2 1.1l-.8.8c.8 1.6 2.1 2.9 3.7 3.7l.8-.8c.3-.3.7-.4 1.1-.2l2.5 1.1c.5.2.6.8.3 1.2-.7 1.4-2 2.1-3.5 1.7-3.9-1-6.9-4-7.9-7.9-.4-1.5.3-2.8 1.7-3.5Z" fill="currentColor"/></svg>')
def footer(l,t,page='index'):
 html=_r7_footer(l,t,page)
 if THEME=='m': return html
 name=tr(l,'Na shkruaj në WhatsApp','Message us on WhatsApp','Schreiben Sie uns auf WhatsApp')
 # Inside the footer landmark (it is fixed to the corner of the screen, so its place in the page does not show).
 assert html.endswith('</footer>')
 return html[:-len('</footer>')]+(f'<a class="wa-float" href="{wa(l)}" target="_blank" rel="noopener noreferrer" aria-label="{name}" data-wa-float>{WA_ICON}'
  f'<span class="wa-tip" aria-hidden="true">{name}</span></a></footer>')
