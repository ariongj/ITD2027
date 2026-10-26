"""Projects report of 25 October 2026 (ITD_Projektet_Faqet_e_Brendshme_SEO_25-10-2026.pdf): a page inside the site for
each of the six projects, in SQ / EN / DE (18 pages), main version only.

The cards on the home and projects pages open these pages ("Shiko projektin"); each page has the project's title and
introduction in the centre, a "Visit website" button, the goal, the solution, what it includes, a gallery of views of
the public website (taken 25 October 2026), the related ITD service, similar projects and "Have a similar project?".
The texts follow the report: SQ in full, EN/DE introductions and metadata as given, the rest translated from the SQ
base. Pages live under /project/<slug>: a folder named "projects" would collide with the /projects page on the
server (Apache answers a folder before the clean-URL rule)."""

PROJECT_DATA=[
 dict(key='verkaufeimmobilie',slug='verkaufeimmobilie',name='verkaufeimmobilie.de',url='https://verkaufeimmobilie.de/',similar=['rata-solar','kalkulatori','kobags'],
  cat=('Pasuri të paluajtshme · Platformë pronash','Real estate · Property platform','Immobilien · Immobilienplattform'),
  title=('verkaufeimmobilie.de | Platformë Pronash','verkaufeimmobilie.de | Property Platform','verkaufeimmobilie.de | Immobilienplattform'),
  meta=('Projekt web për vlerësim orientues prone, formularë dhe kërkesa për ekspert. Shiko prezantimin e platformës verkaufeimmobilie.de nga IT Department.',
   'A property website with indicative valuation, property forms and expert enquiries. Explore the verkaufeimmobilie.de project by IT Department.',
   'Immobilienwebsite mit orientierender Bewertung, Objektformularen und Expertenanfragen. Das Projekt verkaufeimmobilie.de von IT Department.'),
  card=('Platformë për vlerësim orientues të pronës dhe kërkesë për konsultë me ekspert.','A platform for an indicative property valuation and a request for an expert consultation.','Plattform für eine orientierende Immobilienbewertung und die Anfrage einer Expertenberatung.'),
  intro=('verkaufeimmobilie.de është një platformë për pronarët që duan të nisin shitjen e një prone në Gjermani. Ajo lidh një vlerësim fillestar orientues me mbledhjen e të dhënave të pronës dhe një kërkesë për konsultë personale.',
   'A property platform for owners in Germany, combining an indicative valuation, property information and a clear route to an expert enquiry.',
   'Eine Immobilienplattform für Eigentümer in Deutschland: mit orientierender Bewertung, strukturierten Objektdaten und einem klaren Weg zur Expertenanfrage.'),
  goal=('Qëllimi është ta bëjë të kuptueshëm hapin e parë: çfarë prone ka përdoruesi, çfarë informacioni duhet të japë dhe si mund të kërkojë ndihmë nga një ekspert.',
   'The aim is to make the first step easy to understand: what kind of property the user has, what information to provide and how to ask an expert for help.',
   'Ziel ist ein verständlicher erster Schritt: welche Immobilie der Nutzer hat, welche Angaben er machen sollte und wie er einen Experten um Hilfe bitten kann.'),
  solution=('Ndërfaqja organizon udhëtimin nga zgjedhja e llojit të pronës te formulari i detajuar dhe kërkesa për takim. Informacioni shpjegues, pyetjet e shpeshta dhe navigimi DE/EN e mbështesin këtë proces.',
   'The interface guides the journey from choosing the property type to the detailed form and the appointment request. Explanatory content, FAQs and DE/EN navigation support the process.',
   'Die Oberfläche führt von der Wahl der Immobilienart über das ausführliche Formular bis zur Terminanfrage. Erklärende Inhalte, häufige Fragen und die Navigation auf Deutsch und Englisch unterstützen den Ablauf.'),
  features=[('Kontroll orientues i vlerës me të dhëna të pronës.','Indicative value check with property data.','Orientierender Wertcheck mit Objektdaten.'),
   ('Formular për llojin, sipërfaqen, gjendjen dhe kontaktin.','Form for type, size, condition and contact.','Formular für Art, Fläche, Zustand und Kontakt.'),
   ('Prezantim pronash dhe përmbajtje orientuese.','Property listings and guidance content.','Objektpräsentation und Ratgeberinhalte.'),
   ('Kërkesë për ekspert, FAQ dhe kalim DE/EN.','Expert enquiry, FAQ and DE/EN switch.','Expertenanfrage, FAQ und Wechsel DE/EN.')],
  visual=('Pamje të pronave, ngjyra të qeta dhe formularë me hapa të qartë.','Property photography, calm colours and forms with clear steps.','Immobilienbilder, ruhige Farben und Formulare mit klaren Schritten.'),
  note=('Website-i shfaq një parapamje për klientin (Kundenvorschau): shembujt e vlerësimeve dhe pronave janë ilustrues, jo të dhëna reale.',
   'The website shows a customer preview (Kundenvorschau): the example valuations and properties are illustrative, not real data.',
   'Die Website zeigt eine Kundenvorschau: Die Beispielbewertungen und -objekte dienen der Veranschaulichung und sind keine echten Daten.'),
  home=('faqja kryesore me vlerësimin e pronës','home page with the property valuation','Startseite mit der Immobilienbewertung'),
  gallery=[('wertcheck',('formulari për të dhënat e pronës','the property data form','Formular für die Objektdaten')),
   ('objekte',('lista e pronave në parapamje','property listings in the preview','Objektliste in der Vorschau')),('mobile',None)]),
 dict(key='rata-solar',slug='rata-solar',name='RATA Solar',url='https://ratasolar.com/',similar=['verkaufeimmobilie','kobags','kalkulatori'],
  cat=('Energji solare · Website & mjet llogaritjeje','Solar energy · Website & calculation tool','Solarenergie · Website & Rechentool'),
  title=('RATA Solar | Website për Energji Solare','RATA Solar | Solar Energy Website','RATA Solar | Website für Solarenergie'),
  meta=('Website për zgjidhje solare, pajisje, projekte dhe kërkesa për ofertë, me kalkulator orientues të konsumit. Projekt nga IT Department.',
   'A solar energy website with systems, equipment, projects and quotation enquiries, supported by an indicative calculator. A project by IT Department.',
   'Website für Solarsysteme, Geräte, Projekte und Angebotsanfragen mit orientierendem Rechner. Ein Webprojekt von IT Department.'),
  card=('Website për energji solare me zgjidhje, projekte, pajisje dhe kalkulator orientues.','A solar energy website with systems, projects, equipment and an indicative calculator.','Website für Solarenergie mit Lösungen, Projekten, Geräten und orientierendem Rechner.'),
  intro=('RATA Solar prezanton zgjidhje fotovoltaike për shtëpi, biznese dhe industri. Website-i ndërthur shpjegimin e sistemeve solare me projektet, pajisjet dhe një mjet orientues që nis nga konsumi ose fatura e energjisë.',
   'A solar energy website connecting system information, equipment and completed installations with an indicative calculator and quotation enquiries.',
   'Eine Website für Solarenergie, die Systeminformationen, Geräte und realisierte Anlagen mit einem orientierenden Rechner und Angebotsanfragen verbindet.'),
  goal=('Oferta teknike duhet të kuptohet edhe nga vizitori pa njohuri të specializuara. Qëllimi është ta ndihmojë të krahasojë zgjidhjet dhe të përgatitet për një kërkesë të përshtatshme për objektin e tij.',
   'A technical offer has to make sense to visitors without specialist knowledge. The aim is to help them compare solutions and prepare a request that fits their building.',
   'Ein technisches Angebot muss auch ohne Fachwissen verständlich sein. Ziel ist es, Besuchern beim Vergleich der Lösungen zu helfen und eine passende Anfrage für ihr Objekt vorzubereiten.'),
  solution=('Faqja i ndan sistemet në on-grid, hybrid dhe off-grid, paraqet punët e realizuara dhe shpjegon lidhjen mes paneleve, inverterit, baterisë dhe objektit. Kalkulatori e kthen konsumin në një pikënisje për bisedën me ekipin.',
   'The site separates on-grid, hybrid and off-grid systems, presents completed installations and explains how panels, inverter, battery and building fit together. The calculator turns consumption into a starting point for the conversation with the team.',
   'Die Website unterscheidet On-Grid-, Hybrid- und Off-Grid-Systeme, zeigt realisierte Anlagen und erklärt das Zusammenspiel von Modulen, Wechselrichter, Batterie und Gebäude. Der Rechner macht aus dem Verbrauch einen Ausgangspunkt für das Gespräch mit dem Team.'),
  features=[('Kalkulator orientues sipas konsumit ose faturës.','Indicative calculator based on consumption or the energy bill.','Orientierender Rechner nach Verbrauch oder Stromrechnung.'),
   ('Faqe për sistemet dhe katalog pajisjesh.','Pages for each system and an equipment catalogue.','Seiten zu den Systemen und Gerätekatalog.'),
   ('Projekte me kategori dhe kapacitete të prezantuara.','Projects presented with categories and capacities.','Projekte mit Kategorien und Leistungsangaben.'),
   ('Ilustrime teknike, FAQ dhe kërkesë për ofertë.','Technical illustrations, FAQ and quotation requests.','Technische Illustrationen, FAQ und Angebotsanfrage.')],
  visual=('Fotografi solare, kontrast i errët me të verdhë dhe skema shpjeguese.','Solar photography, dark contrast with yellow, and explanatory diagrams.','Solarfotografie, dunkler Kontrast mit Gelb und erklärende Schemata.'),
  home=('faqja kryesore','home page','Startseite'),
  gallery=[('kalkulator',('kalkulatori i sistemit sipas konsumit','the system calculator based on consumption','Anlagenrechner nach Verbrauch')),
   ('projektet',('faqja e projekteve të realizuara','the completed projects page','Seite mit realisierten Projekten')),('mobile',None)]),
 dict(key='kobags',slug='kobags-group',name='KoBags Group',url='https://kobags.itdks.tech/',similar=['paketoje','rata-solar','optika-miftari'],
  cat=('Prodhim & ambalazh B2B · Website B2B & katalog','B2B manufacturing & packaging · B2B website & catalogue','B2B-Produktion & Verpackung · B2B-Website & Katalog'),
  title=('KoBags Group | Website B2B','KoBags Group | B2B Website','KoBags Group | B2B-Website'),
  meta=('Website B2B për qese të personalizuara: katalog, madhësi, specifikime, prodhim dhe kërkesë për ofertë. Projekti KoBags Group nga IT Department.',
   'A B2B website for custom bags with product families, sizes, specifications and quotation enquiries. The KoBags Group project by IT Department.',
   'B2B-Website für individuelle Taschen mit Produktfamilien, Größen, Spezifikationen und Angebotsanfragen. KoBags Group von IT Department.'),
  card=('Katalog B2B për qese të personalizuara, me specifikime dhe rrugë drejt ofertës.','A B2B catalogue for custom bags, with specifications and a route to a quotation.','B2B-Katalog für individuelle Taschen mit Spezifikationen und Weg zum Angebot.'),
  intro=('KoBags Group prezanton prodhimin e qeseve non-woven për biznese. Website-i e organizon ofertën sipas formës së qeses, përdorimit dhe specifikimeve, duke e udhëhequr blerësin drejt kërkesës për ofertë ose mostrës.',
   'A B2B website for custom non-woven bags, bringing product families, specifications and manufacturing information into a clear quotation journey.',
   'Eine B2B-Website für individuell bedruckte Non-Woven-Taschen, die Produktfamilien, Spezifikationen und Fertigungsinformationen mit Angebotsanfragen verbindet.'),
  goal=('Blerësi duhet të kuptojë produktin përpara se të diskutojë porosinë: materialin, madhësinë, printimin dhe përdorimin. Kërkesa duhet të nisë me informacion të strukturuar, jo vetëm me një mesazh të përgjithshëm.',
   'Buyers need to understand the product before discussing an order: material, size, printing and use. An enquiry should start with structured information, not just a general message.',
   'Einkäufer sollen das Produkt verstehen, bevor sie über eine Bestellung sprechen: Material, Größe, Druck und Einsatz. Eine Anfrage soll mit strukturierten Angaben beginnen, nicht nur mit einer allgemeinen Nachricht.'),
  solution=('Katalogu ndan familjet e produkteve dhe paraqet dimensionet, peshën e materialit dhe mundësitë e printimit. Përmbajtja mbi prodhimin, përgjegjësinë dhe dokumentet e kompanisë e plotëson prezantimin komercial në SQ/EN.',
   'The catalogue separates the product families and shows dimensions, fabric weight and printing options. Content on manufacturing, responsibility and company documents completes the commercial presentation in Albanian and English.',
   'Der Katalog gliedert die Produktfamilien und zeigt Abmessungen, Materialgewicht und Druckmöglichkeiten. Inhalte zu Fertigung, Verantwortung und Unternehmensdokumenten ergänzen die Präsentation auf Albanisch und Englisch.'),
  features=[('Familje qesesh dhe faqe të veçanta produktesh.','Bag families and individual product pages.','Taschenfamilien und eigene Produktseiten.'),
   ('Përzgjedhje madhësie dhe specifikime të produktit.','Size selection and product specifications.','Größenauswahl und Produktspezifikationen.'),
   ('Kërkesë për ofertë dhe kërkesë për mostër.','Quotation requests and sample requests.','Angebotsanfrage und Musteranfrage.'),
   ('Informacion për prodhimin, materialin dhe dokumentet.','Information on manufacturing, material and documents.','Informationen zu Fertigung, Material und Dokumenten.')],
  visual=('Pamje të prodhimit dhe produkteve, me identitet industrial të pastër.','Production and product imagery with a clean industrial identity.','Bilder aus Produktion und Sortiment mit klarer industrieller Identität.'),
  home=('faqja kryesore','home page','Startseite'),
  gallery=[('products',('katalogu i qeseve','the bag catalogue','Taschenkatalog')),
   ('product',('faqja e produktit me madhësitë dhe specifikimet','product page with sizes and specifications','Produktseite mit Größen und Spezifikationen')),('mobile',None)]),
 dict(key='paketoje',slug='paketoje',name='Paketoje',url='https://ariongj.github.io/paketa/',similar=['kobags','optika-miftari','rata-solar'],
  cat=('Ambalazh për ushqim & pije · Ndërfaqe e-commerce','Food & beverage packaging · E-commerce interface','Lebensmittel- & Getränkeverpackungen · E-Commerce-Oberfläche'),
  title=('Paketoje | E-commerce për Ambalazh','Paketoje | Packaging E-commerce','Paketoje | E-Commerce für Verpackungen'),
  meta=('Ndërfaqe e-commerce për ambalazh ushqimi: kategori, kërkim, shportë, sasi dhe personalizim. Shiko projektin Paketoje nga IT Department.',
   'A packaging e-commerce interface with categories, search, cart, quantities and custom branding enquiries. Explore Paketoje by IT Department.',
   'E-Commerce-Oberfläche für Lebensmittelverpackungen mit Kategorien, Suche, Warenkorb und Personalisierungsanfragen. Paketoje von IT Department.'),
  card=('Përvojë dyqani online për ambalazh ushqimi, me katalog, shportë dhe oferta për biznese.','An online shop experience for food packaging, with catalogue, cart and offers for businesses.','Onlineshop-Erlebnis für Lebensmittelverpackungen mit Katalog, Warenkorb und Angeboten für Unternehmen.'),
  intro=('Paketoje është një përvojë e-commerce për bizneset e ushqimit dhe pijeve. Katalogu organizon gota, kapakë, enë dhe materiale paketimi, ndërsa faqja lidh zgjedhjen e produktit me sasitë, çmimet dhe kërkesat për personalizim.',
   'An e-commerce interface for food and beverage packaging, combining a product catalogue, quantity selection, cart and custom branding enquiries.',
   'Eine E-Commerce-Oberfläche für Lebensmittel- und Getränkeverpackungen mit Produktkatalog, Mengenauswahl, Warenkorb und Anfragen zur Personalisierung.'),
  goal=('Biznesi duhet ta gjejë shpejt produktin që i përshtatet porosisë: kategorinë, madhësinë, përputhjen me kapakun dhe sasinë për pako ose karton. Personalizimi kërkon një rrugë të veçantë komunikimi.',
   'A business has to find the right product quickly: category, size, the matching lid and the quantity per pack or carton. Custom branding needs its own line of communication.',
   'Ein Unternehmen soll schnell das passende Produkt finden: Kategorie, Größe, passender Deckel und Menge pro Packung oder Karton. Die Personalisierung braucht einen eigenen Kommunikationsweg.'),
  solution=('Ndërfaqja bashkon kategori produktesh, kërkim, të preferuara dhe shportë. Seksionet për printim me logo, oferta shumice dhe mostra e bëjnë të qartë dallimin mes blerjes së produkteve dhe kërkesës për zgjidhje të personalizuar.',
   'The interface brings together product categories, search, favourites and a cart. Sections on logo printing, wholesale offers and samples make the difference between buying products and asking for a custom solution clear.',
   'Die Oberfläche verbindet Produktkategorien, Suche, Favoriten und Warenkorb. Bereiche für Logodruck, Großhandelsangebote und Muster trennen klar zwischen dem Kauf von Produkten und der Anfrage nach einer individuellen Lösung.'),
  features=[('Katalog produktesh me kategori dhe kërkim.','Product catalogue with categories and search.','Produktkatalog mit Kategorien und Suche.'),
   ('Çmime për pako/copë dhe përzgjedhje sasish.','Prices per pack or piece and quantity selection.','Preise pro Packung oder Stück und Mengenauswahl.'),
   ('Të preferuara, shportë dhe përvojë porosie demo.','Favourites, cart and a demo ordering experience.','Favoriten, Warenkorb und ein Demo-Bestellablauf.'),
   ('Printim me logo, mostra, FAQ dhe përmbajtje blogu.','Logo printing, samples, FAQ and blog content.','Logodruck, Muster, FAQ und Bloginhalte.')],
  visual=('Ngjyra të gjalla, fotografi produktesh dhe kompozim i qartë komercial.','Vivid colours, product photography and a clear commercial layout.','Kräftige Farben, Produktfotos und ein klarer kommerzieller Aufbau.'),
  note=('Projekt demonstrues: porositë dhe pagesat në këtë website janë të simuluara.','Demo project: orders and payments on this website are simulated.','Demoprojekt: Bestellungen und Zahlungen auf dieser Website sind simuliert.'),
  home=('faqja kryesore','home page','Startseite'),
  gallery=[('katalog',('katalogu me kategori produktesh','the catalogue with product categories','Katalog mit Produktkategorien')),
   ('produkt',('faqja e produktit me çmimin dhe sasinë','product page with price and quantity','Produktseite mit Preis und Menge')),('mobile',None)]),
 dict(key='optika-miftari',slug='optika-miftari',name='Optika Miftari',url='https://optika.itdks.tech/',similar=['paketoje','kalkulatori','kobags'],
  cat=('Optikë, laborator & klinikë · Katalog & shërbime optike','Optician, laboratory & clinic · Catalogue & optical services','Optik, Labor & Klinik · Katalog & Optikleistungen'),
  title=('Optika Miftari | Platformë Optike','Optika Miftari | Optical Website','Optika Miftari | Optik-Website'),
  meta=('Website optik me koleksione, provë virtuale, informacion lentesh dhe hyrje drejt laboratorit e rezervimit. Projekti Optika Miftari nga IT Department.',
   'An optical website with collections, virtual try-on, lens information and routes to laboratory services and bookings. Optika Miftari by IT Department.',
   'Optik-Website mit Kollektionen, virtueller Anprobe, Linseninformationen und Wegen zu Labor und Terminbuchung. Optika Miftari von IT Department.'),
  card=('Prezantim optik me koleksione, provë virtuale dhe rrugë drejt laboratorit e rezervimit.','An optical presentation with collections, virtual try-on and routes to the lab and booking.','Optik-Auftritt mit Kollektionen, virtueller Anprobe und Wegen zu Labor und Terminbuchung.'),
  intro=('Optika Miftari bashkon koleksionet e syzeve me shërbimet e laboratorit dhe klinikës. Përvoja digjitale e ndihmon vizitorin të eksplorojë stilin, të gjejë informacion për lentet dhe të vazhdojë drejt kontaktit ose rezervimit.',
   'An optical website connecting eyewear collections, virtual try-on and lens information with laboratory services, clinical information and booking routes.',
   'Eine Optik-Website, die Brillenkollektionen, virtuelle Anprobe und Linseninformationen mit Laborleistungen, Klinikangebot und Terminwegen verbindet.'),
  goal=('Një ofertë me disa specializime kërkon navigim të qartë: produktet për konsumatorin, informacioni i lenteve dhe bashkëpunimi profesional nuk duhet të përzihen në të njëjtën rrugë.',
   'An offer with several specialisations needs clear navigation: consumer products, lens information and professional partnerships should not share the same path.',
   'Ein Angebot mit mehreren Schwerpunkten braucht eine klare Navigation: Produkte für Endkunden, Linseninformationen und professionelle Zusammenarbeit dürfen sich nicht auf demselben Weg vermischen.'),
  solution=('Platforma i ndan koleksionet, Optical Lab dhe klinikën në hyrje të dallueshme. Prova virtuale dhe Lens Focus e pasurojnë eksplorimin e produktit, ndërsa faqet e kontaktit dhe partneritetit B2B ofrojnë hapa të qartë të mëtejshëm.',
   'The platform gives the collections, the Optical Lab and the clinic their own entry points. Virtual try-on and Lens Focus enrich product exploration, while the contact and B2B partnership pages offer clear next steps.',
   'Die Plattform gibt Kollektionen, Optical Lab und Klinik jeweils einen eigenen Einstieg. Virtuelle Anprobe und Lens Focus bereichern die Produktsuche, während Kontakt- und B2B-Partnerseiten klare nächste Schritte bieten.'),
  features=[('Koleksione syzesh dhe shfletim produktesh.','Eyewear collections and product browsing.','Brillenkollektionen und Produktsuche.'),
   ('Hyrje te prova virtuale 3D dhe Lens Focus.','Entry to the 3D virtual try-on and Lens Focus.','Zugang zur virtuellen 3D-Anprobe und zu Lens Focus.'),
   ('Prezantim i Optical Lab dhe bashkëpunimit B2B.','Presentation of the Optical Lab and B2B partnership.','Vorstellung des Optical Lab und der B2B-Zusammenarbeit.'),
   ('Klinika, kontakti dhe rruga drejt rezervimit.','The clinic, contact and the route to booking.','Klinik, Kontakt und Weg zur Terminbuchung.')],
  visual=('Fotografi editoriale, hapësirë e bollshme dhe identitet i përmbajtur.','Editorial photography, generous space and a restrained identity.','Redaktionelle Fotografie, viel Raum und eine zurückhaltende Identität.'),
  home=('faqja kryesore me koleksionet','home page with the collections','Startseite mit den Kollektionen'),
  gallery=[('lab',('faqja e Optical Lab','the Optical Lab page','Seite des Optical Lab')),('mobile',None)]),
 dict(key='kalkulatori',slug='kalkulatori',name='Kalkulatori',url='https://www.kalkulatori.info/',similar=['verkaufeimmobilie','rata-solar','optika-miftari'],
  cat=('Shërbime profesionale & financa · Website & kalkulator page','Professional services & finance · Website & salary calculator','Fachdienstleistungen & Finanzen · Website & Gehaltsrechner'),
  title=('Kalkulatori | Website Kontabiliteti','Kalkulatori | Accounting Services Website','Kalkulatori | Website für Buchhaltungsleistungen'),
  meta=('Website për kontabilitet, regjistrim biznesi dhe prokurim publik, me artikuj, formular kontakti dhe kalkulator page. Projekt nga IT Department.',
   'An accounting services website with business registration, public procurement, articles, contact forms and a salary calculator. Built by IT Department.',
   'Website für Buchhaltung, Unternehmensgründung und öffentliche Beschaffung mit Artikeln, Kontaktformular und Gehaltsrechner. Von IT Department.'),
  card=('Website për kontabilitet, regjistrim biznesi dhe prokurim publik, me kalkulator page.','A website for accounting, business registration and public procurement, with a salary calculator.','Website für Buchhaltung, Unternehmensgründung und öffentliche Beschaffung mit Gehaltsrechner.'),
  intro=('Kalkulatori prezanton shërbime për regjistrimin e biznesit, kontabilitetin, financat dhe prokurimin publik. Website-i i lidh këto fusha me përmbajtje këshilluese, partnerë profesionalë dhe një mënyrë të drejtpërdrejtë për të kërkuar konsultë.',
   'A professional services website for accounting, business registration and public procurement, supported by articles, consultation enquiries and a salary calculator.',
   'Eine Website für Buchhaltung, Unternehmensgründung und öffentliche Beschaffung mit Fachartikeln, Beratungsanfragen und einem Gehaltsrechner.'),
  goal=('Vizitori duhet të kuptojë cilin shërbim kërkon dhe si të kontaktojë ekipin, pa humbur mes termave profesionalë. Qëllimi është një prezantim i organizuar dhe një kërkesë që nis me kontekstin e duhur.',
   'Visitors should understand which service they need and how to contact the team without getting lost in professional terms. The aim is an organised presentation and an enquiry that starts with the right context.',
   'Besucher sollen verstehen, welche Leistung sie brauchen und wie sie das Team erreichen, ohne sich in Fachbegriffen zu verlieren. Ziel ist eine geordnete Präsentation und eine Anfrage, die mit dem richtigen Kontext beginnt.'),
  solution=('Faqja ndërtohet rreth tri shtyllave të shërbimit dhe faqeve të tyre shpjeguese. Formulari ndan lokacionin dhe shërbimin e kërkuar; artikujt, rrjeti i partnerëve dhe kalkulatori i pagës i japin vizitorit pika të tjera hyrjeje.',
   'The site is built around three service pillars and their explanatory pages. The form separates location and the requested service; articles, the partner network and the salary calculator give visitors further ways in.',
   'Die Website gliedert sich in drei Leistungsbereiche mit erklärenden Seiten. Das Formular trennt Standort und gewünschte Leistung; Artikel, das Partnernetz und der Gehaltsrechner bieten weitere Einstiege.'),
  features=[('Tri faqe shërbimesh dhe prezantim i procesit.','Three service pages and a presentation of the process.','Drei Leistungsseiten und Darstellung des Ablaufs.'),
   ('Artikuj me kategori dhe kërkesë për konsultë.','Articles with categories and consultation requests.','Artikel mit Kategorien und Beratungsanfrage.'),
   ('Kalkulator page neto/bruto, me një ose dy paga.','Net/gross salary calculator for one or two salaries.','Netto-/Brutto-Gehaltsrechner für ein oder zwei Gehälter.'),
   ('Formular sipas lokacionit/shërbimit dhe zgjedhje SQ/EN.','Form by location and service, with SQ/EN choice.','Formular nach Standort und Leistung, Auswahl SQ/EN.')],
  visual=('Identitet blu e gjelbër, ilustrime të qarta dhe hierarki profesionale.','A blue and green identity, clear illustrations and a professional hierarchy.','Blau-grüne Identität, klare Illustrationen und eine professionelle Hierarchie.'),
  home=('faqja kryesore','home page','Startseite'),
  gallery=[('paga',('kalkulatori i pagës neto dhe bruto','the net and gross salary calculator','Netto- und Bruttogehaltsrechner')),
   ('sherbim',('faqja e shërbimit Kontabilitet dhe financa','the Accounting and finance service page','Leistungsseite Buchhaltung und Finanzen')),('mobile',None)])]
PROJECT_BY_KEY={p['key']:p for p in PROJECT_DATA}
PHONE=('faqja kryesore në telefon','the home page on a phone','Startseite auf dem Smartphone')
LABELS=dict(intro=('Hyrja','Overview','Überblick'),goal=('Qëllimi','Goal','Ziel'),solution=('Zgjidhja','Solution','Lösung'),features=('Çfarë përfshin','What it includes','Was es umfasst'),
 visual=('Drejtimi vizual','Visual direction','Visuelle Richtung'),gallery=('Pamje nga projekti','Views of the project','Ansichten des Projekts'),visit=('Vizito website-in','Visit website','Website besuchen'),
 all=('Të gjitha projektet','All projects','Alle Projekte'),view=('Shiko projektin','View project','Projekt ansehen'),similar=('Projekte të ngjashme','Similar projects','Ähnliche Projekte'),
 service=('Shërbimi përkatës','Related service','Passende Leistung'),servicename=('Faqe interneti & softuer','Websites & software','Websites & Software'),
 servicetext=('Faqe interneti, platforma dhe softuer biznesi, të ndërtuara rreth punës reale.','Websites, platforms and business software, built around real work.','Websites, Plattformen und Unternehmenssoftware, gebaut für die tatsächliche Arbeit.'),
 cta=('Ke një projekt të ngjashëm?','Have a similar project?','Haben Sie ein ähnliches Projekt?'),ctatext=('Na trego për idenë tënde dhe e përcaktojmë bashkë hapin e parë.','Tell us about your idea and we’ll work out the first step together.','Erzählen Sie uns von Ihrer Idee, und wir planen gemeinsam den ersten Schritt.'),
 contact=('Na kontakto','Contact us','Kontakt aufnehmen'),caption=('Pamje nga website-i publik, tetor 2026','View of the public website, October 2026','Ansicht der öffentlichen Website, Oktober 2026'),
 newtab=('hapet në një skedë të re','opens in a new tab','öffnet in einem neuen Tab'),done=('Projekte të realizuara','Completed projects','Realisierte Projekte'))
L10=lambda l,k:tr(l,*LABELS[k])

def project_page_key(p): return 'project/'+p['slug']

# The project list: cards open the project's page; name, short text and "View project" on each card.
if THEME!='m':
 PROJECTS[:]=[{'key':p['key'],'name':p['name'],'url':p['url'],'final':'','category':tuple(x.upper() for x in p['cat']),'text':p['card'],'slug':p['slug']} for p in PROJECT_DATA]
 for p in PROJECT_DATA: NEW_META[project_page_key(p)]=(p['title'],p['meta'])
# Added to the page builders and, with "projects" as their parent for the breadcrumb, to PARENTS in proposal.py.
PROJECT_BUILDERS={} if THEME=='m' else {project_page_key(p):(lambda l,t,p=p:project_page(p,l,t)) for p in PROJECT_DATA}

_projects_card=project_card
def project_card(p,l,tag='h2',lazy=True):
 if THEME=='m' or 'slug' not in p: return _projects_card(p,l,tag,lazy)
 return (f'<a class="project-card card" href="{route("project/"+p["slug"],l)}" data-project="{p["key"]}">'
  f'<div class="project-shot"><img src="assets/projects/{p["key"]}-720.webp" srcset="assets/projects/{p["key"]}-720.webp 720w, assets/projects/{p["key"]}-1440.webp 1440w" sizes="(max-width:800px) 100vw, 50vw" width="720" height="450" alt=""{" loading=lazy" if lazy else ""} decoding="async"></div>'
  f'<div class="project-copy"><span class="project-category">{tr(l,*p["category"])}</span><{tag}>{esc(p["name"])}</{tag}><span class="project-text">{tr(l,*p["text"])}</span><span class="project-cta">{L10(l,"view")}</span></div></a>')

def figure(src_base,alt,mobile,caption,l):
 w,h=(780,1688) if mobile else (1440,900)
 small=f'{src_base}-390.webp 390w, {src_base}-780.webp 780w' if mobile else f'{src_base}-720.webp 720w, {src_base}-1440.webp 1440w'
 big=f'{src_base}-780.webp' if mobile else f'{src_base}-1440.webp'
 return (f'<figure class="pj-fig{" pj-fig-phone" if mobile else ""}"><a href="{big}" data-lightbox="{esc(alt)}"><img src="{big}" srcset="{small}" sizes="{"(max-width:800px) 60vw, 240px" if mobile else "(max-width:800px) 100vw, 520px"}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>'
  f'<figcaption>{caption}</figcaption></figure>')

def project_page(p,l,t):
 name=p['name']; T3=lambda k:tr(l,*p[k]); new=L10(l,'newtab')
 head,sub=T3('cat').split(' · ',1)
 # On phones the long domain name may break after "verkaufe" (soft hyphen) instead of running off the screen.
 h1=esc(name).replace('verkaufeimmobilie','verkaufe&shy;immobilie')
 hero=(f'<section class="pj-hero wrap"><p class="eyebrow">{esc(head)}</p><h1>{h1}</h1><p class="lead">{esc(sub)}</p>'
  f'<div class="actions"><a class="button" href="{esc(p["url"])}" target="_blank" rel="noopener noreferrer">{L10(l,"visit")}<span class="sr-only"> ({new})</span></a>{button(L10(l,"all"),route("projects",l),style="outline")}</div>'
  f'<figure class="pj-shot"><img src="assets/projects/{p["key"]}-1440.webp" srcset="assets/projects/{p["key"]}-720.webp 720w, assets/projects/{p["key"]}-1440.webp 1440w" sizes="(max-width:1100px) 100vw, 1040px" width="1440" height="900" alt="{esc(name)} — {esc(T3("home"))}" decoding="async">'
  f'<figcaption>{L10(l,"caption")}</figcaption></figure></section>')
 note=f'<p class="pj-note">{esc(T3("note"))}</p>' if p.get('note') else ''
 body=(f'<section class="wrap pj-body"><h2>{L10(l,"intro")}</h2><p>{esc(T3("intro"))}</p><h2>{L10(l,"goal")}</h2><p>{esc(T3("goal"))}</p><h2>{L10(l,"solution")}</h2><p>{esc(T3("solution"))}</p>'
  f'<h2>{L10(l,"features")}</h2><ul class="pj-features">'+''.join(f'<li>{esc(tr(l,*f))}</li>' for f in p['features'])+'</ul>'
  f'<p class="pj-visual"><strong>{L10(l,"visual")}:</strong> {esc(T3("visual"))}</p>{note}</section>')
 shots=''.join(figure(f'assets/projects/{p["key"]}-{g}',f'{name} — {tr(l,*(alt or PHONE))}',g=='mobile',L10(l,'caption'),l) for g,alt in p['gallery'])
 gallery=f'<section class="wrap section pj-gallery"><h2>{L10(l,"gallery")}</h2><div class="pj-gallery-grid">{shots}</div></section>'
 service=(f'<section class="wrap pj-service"><a class="card pj-service-card" href="{route("web-software",l)}"><span class="eyebrow">{L10(l,"service")}</span><strong>{L10(l,"servicename")}</strong>'
  f'<span>{L10(l,"servicetext")}</span><span class="pj-arrow" aria-hidden="true">→</span></a></section>')
 similar=('<section class="wrap section pj-similar">'+heading(L10(l,'all').upper(),L10(l,'similar'))+'<div class="project-grid">'
  +''.join(project_card(next(x for x in PROJECTS if x['key']==k),l,'h3') for k in p['similar'])+'</div></section>')
 cta=(f'<section class="wrap pj-cta"><h2>{L10(l,"cta")}</h2><p>{L10(l,"ctatext")}</p><div class="actions">{button(L10(l,"contact"),route("contact",l))}'
  f'{button(L10(l,"servicename"),route("web-software",l),style="outline")}</div></section>')
 return hero+body+gallery+service+similar+cta

# The service page for websites and software lists the projects too.
_projects_web_software=web_software
def web_software(l,t):
 html=_projects_web_software(l,t)
 if THEME=='m': return html
 links=''.join(f'<li><a href="{route("project/"+p["slug"],l)}"><strong>{esc(p["name"])}</strong><span>{tr(l,*p["card"])}</span></a></li>' for p in PROJECT_DATA)
 block=f'<section class="wrap section pj-done">'+heading(tr(l,'PROJEKTET','PROJECTS','PROJEKTE'),L10(l,'done'))+f'<ul class="pj-done-list">{links}</ul></section>'
 marker='<section class="wrap end-section"'
 assert html.count(marker)==1
 return html.replace(marker,block+marker,1)
