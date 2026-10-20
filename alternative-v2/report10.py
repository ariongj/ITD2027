"""Change report 10 (21 October 2026): the round after going live, main version only.

Typography as on the approved phone view, Outfit at its real weights (assets/report10.css); the partners in the
new order; no decorative 01 / 02 / 03 on any page; four new icons for the home areas; a richer storyboard for the
AI character and a gesture of its own for each of the six agents, moving only while on screen (assets/report10.js);
Terms and Privacy as full pages in SQ, EN and DE, describing only what the site really does."""
import atexit

# ---------------------------------------------------------------- partners (page 4)
# The same order on the home page, /partners, mobile and in every language; the DOM follows the list.
PARTNER_ORDER=['cisco','hostinger','mikrotik','adobe','kobags','paysera','optika-miftari','raiffeisen','humanplus']
if THEME!='m': PARTNERS.sort(key=lambda p:PARTNER_ORDER.index(p[0]))

# ---------------------------------------------------------------- the four areas (page 6)
# One family: 26 px, the same 26-unit grid, 1.5 stroke, round ends, colour from currentColor; the soft tile behind
# each symbol is the same colour at low opacity (report10.css), so nothing white is baked in.
AREA_ICONS=['<rect x="5" y="6" width="16" height="12" rx="2.5"/><path d="M5 9.5h16M13 18v2.5M10 20.5h6M10.4 12.4 8.8 14l1.6 1.6M15.6 12.4l1.6 1.6-1.6 1.6M13.7 12.1l-1.4 3.8"/>',
 '<path d="M13 5.2 19.2 7.6v4.9c0 4-2.7 6.9-6.2 8.3-3.5-1.4-6.2-4.3-6.2-8.3V7.6Z"/><path d="m10.2 13.1 2 2 3.8-4.2"/>',
 '<rect x="7" y="10.25" width="12" height="10" rx="3.5"/><path d="M13 10.25V7.75M5.2 13.75v3.6M20.8 13.75v3.6M11.6 17.75h2.8"/><circle cx="13" cy="6.75" r="1"/><circle cx="10.6" cy="14.55" r=".95" fill="currentColor" stroke="none"/><circle cx="15.4" cy="14.55" r=".95" fill="currentColor" stroke="none"/>',
 '<path d="M13 5 18.6 13.8 13 21 7.4 13.8Z"/><path d="M13 5v6.3M9.4 17.2h7.2"/><circle cx="13" cy="12.7" r="1.4"/>']
def area_icon(i):
 return ('<svg class="icon r10-icon" viewBox="0 0 26 26" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
  f'<rect class="r10-tile" width="26" height="26" rx="8" fill="currentColor" stroke="none"/>{AREA_ICONS[i]}</svg>')

_r9_families=families
def families(l,t):
 html=_r9_families(l,t)
 if THEME=='m': return html
 for i in range(4):
  assert icon(i) in html, i
  html=html.replace(icon(i),area_icon(i),1)
 return html

# The services page shows the same four areas: the same icons there.
_r9_services=services
def services(l,t):
 html=_r9_services(l,t)
 if THEME=='m': return html
 for i in range(4):
  old=f'<div class="service-family-title">{icon(i)}'
  assert old in html, i
  html=html.replace(old,f'<div class="service-family-title">{area_icon(i)}',1)
 return html

# ---------------------------------------------------------------- characters (pages 7-10)
# The AI character: an outer frame floats, the rig inside tilts and nods, hands and eyes turn on their own joints
# (report10.css). data-motion: report10.js runs the loop only while the box is on screen and the tab is visible.
_r9_ai=ai
def ai(l,t):
 html=_r9_ai(l,t)
 if THEME=='m': return html
 layers=''.join(f'<img class="ac ac-{x}" src="assets/ai/character/{x}.webp" width="360" height="311" alt="" decoding="async">' for x in CHARACTER_LAYERS)
 old=f'<div class="agent-character">{layers}</div>'
 assert old in html and html.count('<div class="ai-flow-card">')==1
 html=html.replace(old,f'<div class="agent-character"><div class="ac-rig">{layers}</div></div>',1)
 return html.replace('<div class="ai-flow-card">','<div class="ai-flow-card" data-motion>',1)

# The six agents: the same frame and rig, each with its own gesture.
_r9_agent_bot=agent_bot
def agent_bot(name):
 html=_r9_agent_bot(name)
 if THEME=='m': return html
 head=f'<span class="agent-bot" data-agent-bot="{name}" aria-hidden="true">'
 assert html.startswith(head) and html.endswith('</span>')
 return f'<span class="agent-bot" data-agent-bot="{name}" data-motion aria-hidden="true"><span class="ab-rig">'+html[len(head):-len('</span>')]+'</span></span>'

# ---------------------------------------------------------------- decorative numbers (page 5)
# Removed from the finished pages of every language: numbers on their own, and "01 / " in front of a label (the label
# stays). Prices, phone numbers, dates and the slide positions read out to screen readers keep their numbers.
DECOR=[(r'<span class="(?:mini-number|agent-index|detail-number)">\d{1,2}</span>',''),
 (r'<div><small>\d{1,2}</small><strong>','<div><strong>'),
 (r'<div><span>\d{1,2}</span><(h3|strong)>',r'<div><\1>'),
 (r'<(p|span) class="eyebrow">\d{1,2}</\1>',''),
 (r'(<div class="service-family-title"><svg\b.*?</svg>)<span class="eyebrow">[^<]*</span>',r'\1'),
 (r'(<p class="(?:partner-index|about-step-label|eyebrow|slide-kicker|slide-tag)"[^>]*>)\d{1,2} / (?:\d{1,2} · )?',r'\1'),
 (r'(data-label=")\d{1,2} / ',r'\1'),
 (r'(<p class="orbit-caption"[^>]*>)\d{1,2} / ',r'\1')]
DECOR_USED=[0]*len(DECOR)
def _decor_check():
 unused=[DECOR[i][0] for i,n in enumerate(DECOR_USED) if not n]
 if unused and THEME!='m': print('report10: number patterns that matched nothing:',unused)
atexit.register(_decor_check)

# ---------------------------------------------------------------- Terms and Privacy (pages 11-13)
UPDATED=('2026-10-21','Përditësuar më 21 tetor 2026','Updated 21 October 2026','Aktualisiert am 21. Oktober 2026')
# Filled in once the company confirms them (page 12: legal name, registered address, business number); until then the
# pages state only the published identity: IT Department, Prishtina, email and phone.
LEGAL_ENTITY={'name':None,'address':None,'number':None}
def analytics(): return PRODUCTION and os.environ.get('ITD_ANALYTICS')=='1'
PROVIDERS={'Hostinger':'https://www.hostinger.com/legal/privacy-policy','Formspree':'https://formspree.io/legal/privacy-policy/',
 'Google':'https://policies.google.com/privacy','Calendly':'https://calendly.com/legal/privacy-notice','WhatsApp':'https://www.whatsapp.com/legal/privacy-policy'}

def _ext(name,url): return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'
def _page_link(page,l):
 # The pages are rewritten to clean URLs before finalize runs, so the links are written in their final form.
 return (public_path(page,l) or './') if PRODUCTION else route(page,l)

def tel(): return f'<a href="tel:+{cfg["phoneDigits"]}">{cfg["phoneDisplay"]}</a>'
def identity(l):
 e=LEGAL_ENTITY; phone=tel(); mail=f'<a href="mailto:{cfg["email"]}">{cfg["email"]}</a>'
 extra=''.join(f'<li>{label}: {esc(e[k])}</li>' for k,label in zip(['name','address','number'],tr(l,['Emri juridik','Adresa','Numri i biznesit'],['Legal name','Address','Business number'],['Firmenname','Anschrift','Unternehmensnummer'])) if e[k])
 base=tr(l,f'IT Department, me seli në Prishtinë, Kosovë · {mail} · {phone}',f'IT Department, based in Prishtina, Kosovo · {mail} · {phone}',f'IT Department mit Sitz in Prishtina, Kosovo · {mail} · {phone}')
 return f'<p>{base}</p>'+(f'<ul class="r10-facts">{extra}</ul>' if extra else '')

def flows(l):
 fields=tr(l,['Të dhënat','Qëllimi','Baza ligjore','Ruajtja'],['Data','Purpose','Legal basis','Retention'],['Daten','Zweck','Rechtsgrundlage','Speicherdauer'])
 items=[tr(l,('Formulari i kërkesës','Emri, emaili, kompania dhe telefoni nëse i jepni, shërbimi i zgjedhur, mesazhi, si dhe lloji i formularit dhe gjuha.','T’ju përgjigjemi dhe, nëse e kërkoni, të përgatisim një ofertë.','Hapat që ndërmarrim me kërkesën tuaj para një kontrate; interesi ynë i ligjshëm për t’iu përgjigjur.','Kërkesa kalon përmes Formspree dhe arrin në emailin tonë. E ruajmë sa duhet për kërkesën dhe për bashkëpunimin që mund të pasojë; më gjatë vetëm kur ligji e kërkon, p.sh. për kontratat dhe faturat.'),
   ('Enquiry form','Name, email, company and phone if provided, the selected service, your message, and the form type and language.','To reply and, if you ask for it, to prepare an offer.','Steps taken at your request before a contract; our legitimate interest in replying.','The enquiry passes through Formspree and reaches our inbox. We keep it as long as needed for the enquiry and any collaboration that follows; longer only where the law requires it, for example for contracts and invoices.'),
   ('Anfrageformular','Name, E-Mail, Unternehmen und Telefon, sofern angegeben, die gewählte Leistung, Ihre Nachricht sowie Formulartyp und Sprache.','Um Ihnen zu antworten und auf Wunsch ein Angebot zu erstellen.','Maßnahmen auf Ihre Anfrage vor einem Vertrag; unser berechtigtes Interesse, Ihnen zu antworten.','Die Anfrage wird über Formspree übermittelt und erreicht unser Postfach. Wir speichern sie, solange es für die Anfrage und eine mögliche Zusammenarbeit nötig ist; länger nur, wenn das Gesetz es verlangt, etwa für Verträge und Rechnungen.')),
  tr(l,('Drafti në shfletues','Teksti që shkruani në formular, para dërgimit.','Që teksti të mos humbasë nëse rifreskoni faqen ose ndërroni gjuhën.','Interesi i ligjshëm për një formular që funksionon; drafti nuk na dërgohet para se ta dërgoni ju.','Vetëm në këtë skedë të shfletuesit (sessionStorage), derisa kërkesa dërgohet me sukses ose skeda mbyllet.'),
   ('Draft in your browser','The text you type into the form, before sending.','So your text is not lost if you reload the page or switch language.','Legitimate interest in a working form; the draft is not sent to us until you submit it.','Only in this browser tab (sessionStorage), until the enquiry is sent successfully or the tab is closed.'),
   ('Entwurf im Browser','Der Text, den Sie vor dem Senden in das Formular eingeben.','Damit Ihr Text beim Neuladen oder beim Sprachwechsel nicht verloren geht.','Berechtigtes Interesse an einem funktionierenden Formular; der Entwurf wird uns erst übermittelt, wenn Sie ihn senden.','Nur in diesem Browser-Tab (sessionStorage), bis die Anfrage erfolgreich gesendet oder der Tab geschlossen wird.')),
  tr(l,('Email, telefon dhe WhatsApp','Adresa e emailit ose numri juaj dhe përmbajtja e mesazhit.','Komunikimi për kërkesën tuaj.','Hapat para një kontrate, me kërkesën tuaj; interesi i ligjshëm për t’iu përgjigjur.','Si te kërkesat me formular. WhatsApp hapet vetëm kur klikoni lidhjen dhe vepron sipas kushteve të veta.'),
   ('Email, phone and WhatsApp','Your email address or number and the content of your message.','Communicating about your enquiry.','Steps before a contract, at your request; legitimate interest in replying.','As for form enquiries. WhatsApp opens only when you click the link and operates under its own terms.'),
   ('E-Mail, Telefon und WhatsApp','Ihre E-Mail-Adresse oder Nummer und der Inhalt Ihrer Nachricht.','Kommunikation zu Ihrer Anfrage.','Vorvertragliche Maßnahmen auf Ihre Anfrage; berechtigtes Interesse, Ihnen zu antworten.','Wie bei Formularanfragen. WhatsApp wird erst geöffnet, wenn Sie auf den Link klicken, und unterliegt eigenen Bedingungen.')),
  tr(l,('Rezervimi i takimit','Emri, emaili, orari i zgjedhur dhe përgjigjet që jepni në Calendly.','Organizimi i takimit.','Hapat para një kontrate, me kërkesën tuaj.','Calendly ngarkohet vetëm kur hapni rezervimin dhe i ruan të dhënat sipas kushteve të veta; ne i përdorim sa duhet për takimin dhe për bashkëpunimin që mund të pasojë.'),
   ('Booking a meeting','Name, email, the selected time and the answers you give in Calendly.','Organising the meeting.','Steps before a contract, at your request.','Calendly loads only when you open the booking and keeps the data under its own terms; we use it as long as needed for the meeting and any collaboration that follows.'),
   ('Terminbuchung','Name, E-Mail, gewählter Termin und Ihre Angaben in Calendly.','Organisation des Termins.','Vorvertragliche Maßnahmen auf Ihre Anfrage.','Calendly wird erst geladen, wenn Sie die Buchung öffnen, und speichert die Daten nach eigenen Bedingungen; wir nutzen sie, solange es für den Termin und eine mögliche Zusammenarbeit nötig ist.'))]
 if analytics(): items.append(tr(l,('Matja e vizitave (Google Analytics)','Faqja, gjuha, kategoria e shërbimit ose produktit dhe veprimi i kontaktit (p.sh. klikim te emaili ose rezervim i konfirmuar), si dhe të dhëna teknike të pajisjes dhe një identifikues në cookie. Eventet tona nuk përmbajnë emër, email, telefon ose mesazh.','Të kuptojmë cilat faqe dhe shërbime përdoren, që ta përmirësojmë faqen. Nuk përdoret për reklama: ruajtja për reklama, sinjalet e Google dhe personalizimi i reklamave janë të çaktivizuara.','Pëlqimi juaj. Pa pëlqim, Google Analytics nuk ngarkohet; nëse shfletuesi dërgon “Do Not Track”, matja nuk ofrohet fare.','Cookies deri në 2 vjet; të dhënat e eventeve sipas afatit të caktuar në llogarinë tonë Google Analytics, jo më shumë se 14 muaj.'),
   ('Visit measurement (Google Analytics)','The page, language, service or product category and the contact action (for example an email click or a confirmed booking), plus technical device data and an identifier stored in a cookie. Our events contain no names, emails, phone numbers or messages.','To understand which pages and services are used, so we can improve the site. It is not used for advertising: ad storage, Google signals and ad personalisation are switched off.','Your consent. Without consent, Google Analytics is not loaded; if your browser sends “Do Not Track”, measurement is not offered at all.','Cookies up to 2 years; event data according to the setting of our Google Analytics property, no longer than 14 months.'),
   ('Besuchsmessung (Google Analytics)','Seite, Sprache, Leistungs- oder Produktkategorie und die Kontaktaktion (z. B. ein Klick auf die E-Mail-Adresse oder eine bestätigte Buchung) sowie technische Gerätedaten und eine in einem Cookie gespeicherte Kennung. Unsere Ereignisse enthalten keine Namen, E-Mail-Adressen, Telefonnummern oder Nachrichten.','Um zu verstehen, welche Seiten und Leistungen genutzt werden, und die Website zu verbessern. Keine Nutzung für Werbung: Werbespeicherung, Google-Signale und personalisierte Werbung sind deaktiviert.','Ihre Einwilligung. Ohne Einwilligung wird Google Analytics nicht geladen; sendet Ihr Browser „Do Not Track“, wird die Messung gar nicht angeboten.','Cookies bis zu 2 Jahre; Ereignisdaten gemäß der Einstellung unserer Google-Analytics-Property, höchstens 14 Monate.')))
 items+=[tr(l,('Të dhëna teknike të serverit','Adresa IP, data dhe ora, adresa e faqes së kërkuar, faqja nga vini dhe lloji i shfletuesit.','Shfaqja e faqes, funksionimi dhe mbrojtja nga keqpërdorimi.','Interesi ynë i ligjshëm për një faqe të sigurt dhe funksionale.','Për një kohë të kufizuar, sipas cilësimeve të ofruesit të hostimit (Hostinger).'),
   ('Technical server data','IP address, date and time, the requested address, the referring page and the browser type.','Delivering the site, operating it and protecting it against misuse.','Our legitimate interest in a secure, working website.','For a limited time, according to the settings of the hosting provider (Hostinger).'),
   ('Technische Serverdaten','IP-Adresse, Datum und Uhrzeit, aufgerufene Adresse, verweisende Seite und Browsertyp.','Bereitstellung, Betrieb und Schutz der Website vor Missbrauch.','Unser berechtigtes Interesse an einer sicheren, funktionierenden Website.','Für begrenzte Zeit, gemäß den Einstellungen des Hosting-Anbieters (Hostinger).')),
  tr(l,('Harta dhe shkronjat','Kur klikoni “Shfaq hartën”, Google Maps merr adresën IP dhe të dhëna teknike të pajisjes.','Shfaqja e vendndodhjes orientuese. Shkronjat (Outfit) shërbehen nga vetë faqja, pa lidhje me Google Fonts.','Kërkesa juaj me klikim; harta nuk ngarkohet para klikimit.','Sipas kushteve të Google.'),
   ('Map and fonts','When you click “Show map”, Google Maps receives your IP address and technical device data.','Showing the approximate location. The font (Outfit) is served by this website, with no connection to Google Fonts.','Your request by clicking; the map does not load before you click.','Under Google’s terms.'),
   ('Karte und Schriften','Wenn Sie auf „Karte anzeigen“ klicken, erhält Google Maps Ihre IP-Adresse und technische Gerätedaten.','Anzeige des ungefähren Standorts. Die Schrift (Outfit) wird von dieser Website bereitgestellt, ohne Verbindung zu Google Fonts.','Ihre Anfrage per Klick; vor dem Klick wird die Karte nicht geladen.','Nach den Bedingungen von Google.'))]
 out=''.join('<div class="r10-flow"><h3>'+name+'</h3><dl>'+''.join(f'<div><dt>{f}</dt><dd>{v}</dd></div>' for f,v in zip(fields,vals))+'</dl></div>' for name,*vals in items)
 if not analytics(): out+='<p>'+tr(l,'Në këtë version të faqes Google Analytics nuk është aktiv dhe nuk vendosen cookies matjeje.','In this version of the site Google Analytics is not active and no measurement cookies are set.','In dieser Version der Website ist Google Analytics nicht aktiv; es werden keine Mess-Cookies gesetzt.')+'</p>'
 return out+'<p>'+tr(l,'Mos na dërgoni fjalëkalime ose të dhëna të ndjeshme, p.sh. shëndetësore, përmes formularit ose mesazheve.','Please do not send passwords or sensitive data, such as health information, through the form or messages.','Bitte senden Sie keine Passwörter oder sensiblen Daten, etwa Gesundheitsdaten, über das Formular oder Nachrichten.')+'</p>'

def storage_table(l):
 head=tr(l,['Emri','Ofruesi','Qëllimi','Afati','Kategoria'],['Name','Provider','Purpose','Duration','Category'],['Name','Anbieter','Zweck','Dauer','Kategorie'])
 needed=tr(l,'E nevojshme','Necessary','Erforderlich'); measure=tr(l,'Matje, vetëm me pëlqim','Measurement, only with consent','Messung, nur mit Einwilligung')
 rows=[('itd-proposal-v1-…','IT Department',tr(l,'Drafti i formularit (sessionStorage)','Form draft (sessionStorage)','Formularentwurf (sessionStorage)'),tr(l,'Deri në dërgim ose mbylljen e skedës','Until sent or the tab is closed','Bis zum Senden oder Schließen des Tabs'),needed)]
 if analytics(): rows+=[('itd-analytics-consent-v1','IT Department',tr(l,'Ruan zgjedhjen tuaj për matjen (localStorage)','Stores your measurement choice (localStorage)','Speichert Ihre Wahl zur Messung (localStorage)'),tr(l,'Derisa ta ndryshoni ose t’i fshini të dhënat e shfletuesit','Until you change it or clear your browser data','Bis Sie sie ändern oder die Browserdaten löschen'),needed),
  ('_ga','Google',tr(l,'Dallon vizitat me një identifikues të rastësishëm','Distinguishes visits with a random identifier','Unterscheidet Besuche mit einer zufälligen Kennung'),tr(l,'2 vjet','2 years','2 Jahre'),measure),
  ('_ga_B0S3HLRPWD','Google',tr(l,'Ruan gjendjen e sesionit','Keeps the session state','Speichert den Sitzungsstatus'),tr(l,'2 vjet','2 years','2 Jahre'),measure)]
 caption=tr(l,'Çfarë ruhet në shfletuesin tuaj','What is stored in your browser','Was in Ihrem Browser gespeichert wird')
 body=''.join('<tr><th scope="row" data-label="'+head[0]+'"><code>'+r[0]+'</code></th>'+''.join(f'<td data-label="{h}">{v}</td>' for h,v in zip(head[1:],r[1:]))+'</tr>' for r in rows)
 return f'<div class="r10-table"><table><caption>{caption}</caption><thead><tr>'+''.join(f'<th scope="col">{h}</th>' for h in head)+f'</tr></thead><tbody>{body}</tbody></table></div>'

def privacy_sections(l):
 aip=_ext(tr(l,'Agjencia për Informim dhe Privatësi (AIP)','Information and Privacy Agency (AIP)','Agentur für Information und Datenschutz (AIP)'),tr(l,'https://aip.rks-gov.net/','https://aip.rks-gov.net/en/','https://aip.rks-gov.net/en/'))
 mail=f'<a href="mailto:{cfg["email"]}">{cfg["email"]}</a>'
 google=tr(l,'Analytics vetëm me pëlqim; Maps vetëm pas klikimit','Analytics only with consent; Maps only after a click','Analytics nur mit Einwilligung; Maps erst nach einem Klick') if analytics() else tr(l,'Maps vetëm pas klikimit','Maps only after a click','Maps erst nach einem Klick')
 roles=[('Hostinger',tr(l,'hostimi i faqes','website hosting','Hosting der Website')),('Formspree',tr(l,'dërgimi i formularëve','form delivery','Übermittlung der Formulare')),('Google',google),
  ('Calendly',tr(l,'rezervimi i takimeve, kur e hapni','booking meetings, when you open it','Terminbuchung, wenn Sie sie öffnen')),('WhatsApp',tr(l,'bisedat, kur klikoni lidhjen','conversations, when you click the link','Unterhaltungen, wenn Sie auf den Link klicken'))]
 withdraw=('<p>'+tr(l,'Pëlqimin për matjen mund ta tërhiqni në çdo kohë te “Cilësimet e privatësisë” në fund të faqes. Tërheqja nuk ndikon në përpunimin e bërë më parë.','You can withdraw your consent to measurement at any time under “Privacy settings” at the bottom of the page. Withdrawal does not affect processing carried out before.','Ihre Einwilligung zur Messung können Sie jederzeit unter „Datenschutzeinstellungen“ am Seitenende widerrufen. Der Widerruf berührt die bis dahin erfolgte Verarbeitung nicht.')+'</p>') if analytics() else ''
 cookies_intro=tr(l,'Matja opsionale bllokohet derisa të zgjidhni “Lejo matjen”. Me “Pa analytics” nuk vendosen cookies matjeje; kur e tërheqni pëlqimin, cookies _ga fshihen nga ky domen.','Optional measurement stays blocked until you choose “Allow analytics”. With “No analytics” no measurement cookies are set; when you withdraw consent, the _ga cookies are deleted from this domain.','Die optionale Messung bleibt blockiert, bis Sie „Analytics erlauben“ wählen. Mit „Ohne Analytics“ werden keine Mess-Cookies gesetzt; beim Widerruf werden die _ga-Cookies dieser Domain gelöscht.') if analytics() else tr(l,'Në këtë version të faqes nuk vendosen cookies matjeje.','This version of the site sets no measurement cookies.','Diese Version der Website setzt keine Mess-Cookies.')
 return [('who',tr(l,'Kush jemi','Who we are','Wer wir sind'),
   '<p>'+tr(l,'Kontrolluesi i të dhënave për këtë faqe është:','The controller of the data for this website is:','Verantwortlich für die Daten dieser Website ist:')+'</p>'+identity(l)
   +'<p>'+tr(l,'Kjo politikë vlen për faqen itdks.tech dhe për kërkesat që na dërgoni përmes saj. Baza ligjore është Ligji nr. 06/L-082 për mbrojtjen e të dhënave personale.','This policy applies to itdks.tech and to the enquiries you send us through it. The legal framework is Law No. 06/L-082 on the Protection of Personal Data.','Diese Erklärung gilt für itdks.tech und für Anfragen, die Sie uns darüber senden. Rechtsgrundlage ist das Gesetz Nr. 06/L-082 über den Schutz personenbezogener Daten.')+'</p>'),
  ('data',tr(l,'Të dhënat, qëllimet dhe ruajtja','Data, purposes and retention','Daten, Zwecke und Speicherdauer'),
   '<p>'+tr(l,'Përpunojmë vetëm të dhënat që duhen për qëllimin përkatës. Për secilën rrjedhë:','We process only the data needed for each purpose. For each flow:','Wir verarbeiten nur die Daten, die für den jeweiligen Zweck nötig sind. Für jeden Ablauf:')+'</p>'+flows(l)),
  ('recipients',tr(l,'Shërbimet e jashtme','External services','Externe Dienste'),
   '<p>'+tr(l,'Për disa funksione përdorim ofrues të jashtëm. Secili merr vetëm të dhënat që i duhen për shërbimin e vet dhe ka politikën e vet të privatësisë:','For some functions we use external providers. Each receives only the data its service needs and has its own privacy policy:','Für einige Funktionen nutzen wir externe Anbieter. Jeder erhält nur die Daten, die sein Dienst benötigt, und hat eine eigene Datenschutzerklärung:')+'</p><ul>'
   +''.join(f'<li>{_ext(n,PROVIDERS[n])}: {r}</li>' for n,r in roles)+'</ul><p>'
   +tr(l,'Rrjetet sociale në fund të faqes hapen vetëm kur i klikoni. Disa nga këta ofrues i përpunojnë të dhënat jashtë Kosovës, përfshirë Bashkimin Evropian dhe Shtetet e Bashkuara, sipas kushteve dhe masave të tyre mbrojtëse.','The social networks at the bottom of the page open only when you click them. Some of these providers process data outside Kosovo, including in the European Union and the United States, under their own terms and safeguards.','Die sozialen Netzwerke am Seitenende öffnen sich erst, wenn Sie sie anklicken. Einige dieser Anbieter verarbeiten Daten außerhalb des Kosovo, auch in der Europäischen Union und in den USA, nach ihren eigenen Bedingungen und Schutzmaßnahmen.')+'</p>'),
  ('rights',tr(l,'Të drejtat tuaja','Your rights','Ihre Rechte'),
   '<p>'+tr(l,'Sipas Ligjit nr. 06/L-082 mund të kërkoni qasje në të dhënat tuaja, korrigjimin ose fshirjen e tyre, kufizimin e përpunimit dhe, kur zbatohet, bartjen e tyre, si dhe të kundërshtoni përpunimin që bazohet në interes të ligjshëm.','Under Law No. 06/L-082 you can request access to your data, its correction or deletion, restriction of processing and, where applicable, data portability, and you can object to processing based on legitimate interest.','Nach dem Gesetz Nr. 06/L-082 können Sie Auskunft über Ihre Daten, deren Berichtigung oder Löschung, die Einschränkung der Verarbeitung und, soweit anwendbar, die Datenübertragbarkeit verlangen sowie einer Verarbeitung auf Grundlage berechtigter Interessen widersprechen.')+'</p>'+withdraw
   +'<p>'+tr(l,f'Për t’i ushtruar këto të drejta, na shkruani në {mail}. Nëse mendoni se të drejtat tuaja janë shkelur, mund të paraqisni ankesë te {aip}.',f'To exercise these rights, write to {mail}. If you believe your rights have been infringed, you can lodge a complaint with the {aip}.',f'Zur Ausübung dieser Rechte schreiben Sie an {mail}. Wenn Sie meinen, dass Ihre Rechte verletzt wurden, können Sie sich bei der {aip} beschweren.')+'</p>'),
  ('cookies',tr(l,'Cookies dhe matja','Cookies and measurement','Cookies und Messung'),
   f'<p>{cookies_intro}</p>'+storage_table(l)+'<p>'+tr(l,'Calendly dhe Google Maps mund të vendosin cookies të veta vetëm kur i hapni.','Calendly and Google Maps may set their own cookies only when you open them.','Calendly und Google Maps können erst dann eigene Cookies setzen, wenn Sie sie öffnen.')+'</p>'),
  ('contact',tr(l,'Kontakt dhe ndryshime','Contact and changes','Kontakt und Änderungen'),
   '<p>'+tr(l,f'Për pyetje rreth privatësisë: {mail} ose {tel()}. Kur e ndryshojmë këtë politikë, versionin e ri e publikojmë në këtë faqe me datën e përditësimit.',f'Privacy questions: {mail} or {tel()}. When we change this policy, we publish the new version on this page with its update date.',f'Fragen zum Datenschutz: {mail} oder {tel()}. Wenn wir diese Erklärung ändern, veröffentlichen wir die neue Fassung auf dieser Seite mit dem Aktualisierungsdatum.')+'</p>')]

def terms_sections(l):
 mail=f'<a href="mailto:{cfg["email"]}">{cfg["email"]}</a>'
 privacy=f'<a href="{_page_link("privacy",l)}">'+tr(l,'Politikën e privatësisë','Privacy policy','Datenschutzerklärung')+'</a>'
 return [('scope',tr(l,'Kush jemi dhe fusha','Who we are and scope','Wer wir sind und Geltungsbereich'),
   identity(l)+'<p>'+tr(l,'Faqja itdks.tech prezanton shërbimet tona për web, softuer, IT, siguri, AI dhe kreativë dhe ju mundëson të na kontaktoni. Këto kushte vlejnë për këdo që e përdor faqen; për shërbimet që porositni vlen oferta ose kontrata përkatëse. Përmbajtja e faqes shërben për informim.','itdks.tech presents our web, software, IT, security, AI and creative services and lets you contact us. These terms apply to everyone who uses the site; services you order are governed by the corresponding offer or contract. Website content is provided for information.','itdks.tech stellt unsere Leistungen in Web, Software, IT, Sicherheit, KI und Kreativ vor und ermöglicht Ihnen, uns zu kontaktieren. Diese Bedingungen gelten für alle, die die Website nutzen; für beauftragte Leistungen gilt das jeweilige Angebot oder der Vertrag. Die Inhalte der Website dienen der Information.')+'</p>'),
  ('offers',tr(l,'Ofertat dhe shërbimet','Offers and services','Angebote und Leistungen'),
   '<p>'+tr(l,'Bashkëpunimi nis me kërkesën tuaj: e shqyrtojmë nevojën, ju dërgojmë ofertë dhe puna fillon pas marrëveshjes. Çdo bashkëpunim nis me një marrëveshje të qartë për punën, afatet dhe përgjegjësitë.','Each collaboration starts with your enquiry: we review the need, send you an offer, and work begins once we agree. Every collaboration rests on a clear agreement on scope, timeline and responsibilities.','Jede Zusammenarbeit beginnt mit Ihrer Anfrage: Wir prüfen den Bedarf, senden Ihnen ein Angebot, und die Arbeit beginnt nach der Vereinbarung. Grundlage ist stets eine klare Absprache über Umfang, Zeitplan und Zuständigkeiten.')+'</p><p>'
   +tr(l,'Çmimi, afati, pagesa, dorëzimi dhe ndryshimet përcaktohen në ofertë ose kontratë. Çmimet dhe paketat në faqe janë orientuese; çmimet, afatet dhe zgjidhja përfundimtare konfirmohen pas shqyrtimit të kërkesës. Ndryshimet konfirmohen para zbatimit.','Price, timeline, payment, delivery and changes are set in the offer or contract. Prices and packages on the site are a guide; prices, timelines and the final solution are confirmed after we review the enquiry. Changes are confirmed before implementation.','Preis, Frist, Zahlung, Lieferung und Änderungen werden im Angebot oder Vertrag festgelegt. Preise und Pakete auf der Website dienen der Orientierung; Preise, Zeitplan und die endgültige Lösung werden nach Prüfung der Anfrage bestätigt. Änderungen werden vor der Umsetzung bestätigt.')+'</p>'),
  ('content',tr(l,'Përmbajtja dhe pronësia','Content and ownership','Inhalte und Rechte'),
   '<p>'+tr(l,'Përpiqemi që informacioni të jetë i saktë dhe i përditësuar dhe mund ta ndryshojmë kur është e nevojshme. Shembujt e shënuar si demonstrues janë ilustrime, jo projekte të realizuara.','We aim to keep the information accurate and up to date, and may update it when needed. Examples marked as illustrative are demonstrations, not delivered projects.','Wir bemühen uns um korrekte und aktuelle Informationen und können sie bei Bedarf anpassen. Als Beispiel gekennzeichnete Inhalte sind Illustrationen, keine umgesetzten Projekte.')+'</p><p>'
   +tr(l,'Tekstet, dizajni dhe materialet grafike të faqes janë të IT Department, përveç kur shënohet ndryshe; mos i kopjoni pa miratimin tonë. Logot dhe emrat e palëve të treta u përkasin pronarëve të tyre; listimi i partnerëve nuk nënkupton certifikim apo status zyrtar partneri.','Texts, design and graphics on this site belong to IT Department unless stated otherwise; do not copy them without our approval. Third-party logos and names belong to their owners; listing a partner does not imply certification or official partner status.','Texte, Design und Grafiken dieser Website gehören IT Department, sofern nicht anders angegeben; bitte kopieren Sie sie nicht ohne unsere Zustimmung. Logos und Namen Dritter gehören ihren Inhabern; die Nennung eines Partners bedeutet keine Zertifizierung und keinen offiziellen Partnerstatus.')+'</p>'),
  ('use',tr(l,'Përdorimi dhe lidhjet','Use and links','Nutzung und Links'),
   '<ul>'+''.join(f'<li>{x}</li>' for x in tr(l,['Përdoreni faqen pa veprime që dëmtojnë sigurinë, funksionimin ose përmbajtjen e saj.','Mos dërgoni të dhëna të rreme ose përmbajtje të paligjshme.','Mos provoni qasje të paautorizuar dhe mos testoni sigurinë pa leje.'],['Use the website without actions that harm its security, operation or content.','Do not submit false information or unlawful content.','Do not attempt unauthorised access or test security without permission.'],['Nutzen Sie die Website ohne Handlungen, die ihre Sicherheit, ihren Betrieb oder ihre Inhalte beeinträchtigen.','Senden Sie keine falschen Angaben oder rechtswidrigen Inhalte.','Versuchen Sie keinen unbefugten Zugriff und testen Sie die Sicherheit nicht ohne Erlaubnis.']))+'</ul><p>'
   +tr(l,f'Lidhjet e jashtme (p.sh. Calendly, WhatsApp, Google Maps dhe rrjetet sociale) hapin shërbime me kushte dhe politika të veçanta, të cilat ne nuk i kontrollojmë. Për të dhënat personale shihni {privacy}.',f'External links (such as Calendly, WhatsApp, Google Maps and social networks) open services with their own terms and policies, which we do not control. For personal data, see our {privacy}.',f'Externe Links (etwa Calendly, WhatsApp, Google Maps und soziale Netzwerke) öffnen Dienste mit eigenen Bedingungen und Richtlinien, auf die wir keinen Einfluss haben. Zu personenbezogenen Daten siehe unsere {privacy}.')+'</p>'),
  ('liability',tr(l,'Përgjegjësia','Liability','Haftung'),
   '<p>'+tr(l,'Informacioni në faqe është i përgjithshëm dhe nuk zëvendëson ofertën ose këshillën për rastin tuaj. Përgjegjësia për punën e porositur përcaktohet në ofertë ose kontratë.','Information on the site is general and does not replace an offer or advice for your case. Liability for ordered work is set out in the offer or contract.','Die Informationen auf der Website sind allgemein und ersetzen weder ein Angebot noch eine Beratung für Ihren Fall. Die Haftung für beauftragte Arbeiten regelt das Angebot oder der Vertrag.')+'</p><p>'
   +tr(l,'Bëjmë kujdes që faqja të funksionojë, por nuk mund të garantojmë qasje pa ndërprerje. Asgjë në këto kushte nuk e kufizon përgjegjësinë që ligji nuk lejon të kufizohet, as të drejtat tuaja të detyrueshme.','We take care to keep the site working but cannot guarantee uninterrupted access. Nothing in these terms limits liability that cannot be limited by law, or your mandatory rights.','Wir achten darauf, dass die Website funktioniert, können aber keinen unterbrechungsfreien Zugang garantieren. Nichts in diesen Bedingungen beschränkt eine Haftung, die gesetzlich nicht beschränkt werden kann, oder Ihre zwingenden Rechte.')+'</p>'),
  ('closing',tr(l,'Pyetje, ankesa dhe ndryshime','Questions, complaints and changes','Fragen, Beschwerden und Änderungen'),
   '<p>'+tr(l,f'Për pyetje ose ankesa na shkruani në {mail}; mosmarrëveshjet përpiqemi t’i zgjidhim fillimisht me marrëveshje.',f'For questions or complaints, write to {mail}; we aim to resolve any disagreement amicably first.',f'Für Fragen oder Beschwerden schreiben Sie an {mail}; Meinungsverschiedenheiten möchten wir zunächst einvernehmlich lösen.')+'</p><p>'
   +tr(l,'Kur i ndryshojmë këto kushte, versionin e ri e publikojmë në këtë faqe me datën e përditësimit.','When we change these terms, we publish the new version on this page with its update date.','Wenn wir diese Bedingungen ändern, veröffentlichen wir die neue Fassung auf dieser Seite mit dem Aktualisierungsdatum.')+'</p>')]

def legal_page(page,l):
 # Centred title, a short summary, the update date and a topic menu (beside the text on wide screens, above it on
 # phones); headings are real h2s with anchors, the text column stays at 65-75 characters (page 11).
 title,summary=(tr(l,('Politika e privatësisë','Si i përdorim dhe i mbrojmë të dhënat tuaja kur vizitoni itdks.tech dhe kur na kontaktoni.'),('Privacy policy','How we use and protect your data when you visit itdks.tech and contact us.'),('Datenschutzerklärung','Wie wir Ihre Daten verwenden und schützen, wenn Sie itdks.tech besuchen und uns kontaktieren.')) if page=='privacy'
  else tr(l,('Kushtet e përdorimit','Rregullat për përdorimin e faqes itdks.tech dhe si nisin shërbimet tona.'),('Terms of use','The rules for using itdks.tech and how our services begin.'),('Nutzungsbedingungen','Die Regeln für die Nutzung von itdks.tech und wie unsere Leistungen beginnen.')))
 sections=privacy_sections(l) if page=='privacy' else terms_sections(l)
 label=tr(l,'Në këtë faqe','On this page','Auf dieser Seite')
 toc=f'<nav class="r10-toc" aria-labelledby="toc-title" data-toc><h2 id="toc-title">{label}</h2><ul>'+''.join(f'<li><a href="#{k}">{h}</a></li>' for k,h,_ in sections)+'</ul></nav>'
 body=''.join(f'<section id="{k}" aria-labelledby="{k}-title"><h2 id="{k}-title">{h}</h2>{b}</section>' for k,h,b in sections)
 date=UPDATED[0]; when=tr(l,*UPDATED[1:])
 return (f'<section class="page-intro wrap r10-legal-intro"><p class="eyebrow">IT DEPARTMENT</p><h1>{title}</h1><p class="lead">{summary}</p><p class="r10-updated"><time datetime="{date}">{when}</time></p></section>'
  f'<div class="wrap r10-legal">{toc}<div class="r10-legal-text">{body}</div></div>')

def _clean_links(html):
 # The same clean URLs as the page loop in proposal.py writes for production.
 if not PRODUCTION: return html
 for linked_page in [*builders,'privacy','404']:
  for linked_lang in T:
   old=route(linked_page,linked_lang); new=public_path(linked_page,linked_lang) or './'
   for suffix in ['"','?','#']: html=html.replace('href="'+old+suffix,'href="'+new+suffix)
 return html

_r9_finalize=finalize
def finalize(html,page,l):
 html=_r9_finalize(html,page,l)
 if THEME=='m': return html
 for i,(pat,new) in enumerate(DECOR):
  html,n=re.subn(pat,new,html,flags=re.S); DECOR_USED[i]+=n
 if page in ('privacy','terms'):
  html,n=re.subn(r'<main id="main">.*?</main>',lambda m:'<main id="main">'+_clean_links(legal_page(page,l))+'</main>',html,count=1,flags=re.S)
  assert n==1
 return html
