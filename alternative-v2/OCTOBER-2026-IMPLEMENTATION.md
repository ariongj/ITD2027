# October 2026 reports — implementation and verification

The ITD2027 site has been revised against both supplied reports. The local preview is http://127.0.0.1:8791/. The original WebSite ITD preview keeps port 8790.

## Source and scope

- Authoritative repository: `C:/Users/A/Documents/ITD2027`, baseline `e1bf8f86d9620aea725df3c2e74af8c40cf68932`. Remote main was checked before editing and matched this revision.
- Briefs: `ITDKS_SEO_dhe_Ridizajn_Raport_2026-10-02.pdf` (8 pages) and `ITD2027_Raporti_i_Ndryshimeve_01.pdf` (13 pages). Both were read completely and visually inspected.
- Original root static/PHP site is preserved. Work is confined to the alternative website and its validation script. No commit, push or production deployment was performed.
- GitHub Pages automatically publishes on pushes to main. The current working changes have not been pushed.

## Implemented and locally verified

| Requirement | Evidence / outcome |
| --- | --- |
| Original ITD logos | All three original logo files match their source SHA-256 byte for byte. |
| Shared design | Locally hosted Plus Jakarta Sans with OFL licence; #0B0D10 header, #E00000 red, #B90E22 hover, #F4F4F2 background, #111318 text. 56px desktop / 36px mobile primary headings. Original Creative and AI Agents palettes retained; Kraken product uses navy/blue. |
| Interaction | Keyboard focus, 200ms hover transitions, pressed feedback, reduced motion and mobile touch handling. |
| ITD Labs | Header dropdown and footer catalogue; Kraken OS, Kraken Communications, AURA in that order. AURA has no active product link or button. |
| Product pages | Existing Kraken OS route retained; original presentation images, CRM/workspace/finance/documents/inventory scope. Separate Kraken Communications detail page with inbox, human handoff, contacts and offers. |
| Service architecture | Dedicated web-software and ai-automation pages in SQ/EN/DE, linked prominently from home and service overview. Audiences, deliverables, process, illustrative example, oversight/integration boundaries and meeting/enquiry actions. German collaboration copy explains project-specific communication, handover and support arrangements without invented service guarantees. |
| Existing depth | Services, illustrative projects, Creative portfolio, AI Agents, partners, FAQs, contact, privacy and terms remain reachable. |
| SEO | 51 translated pages with unique titles/canonicals, descriptions, one H1 and reciprocal absolute SQ/EN/DE/x-default alternates. Sitemap contains 48 non-404 pages. Separate preview/noindex and isolated production/indexable builds. |
| URL continuity | `seo-url-map.csv` inventories 31 existing/report-mentioned URLs. Current clean production URLs are retained. Existing index-en.html and creative.html redirect destinations are preserved. `/teams/` was confirmed 404 and remains 404; no unsupported homepage redirect. Obsolete standalone optech_footer parameter has a prepared targeted 301. |
| Forms | Existing Formspree provider retained. Required/email/whitespace validation, draft persistence, pending state, duplicate prevention, success confirmation, malformed response/network failure and retry verified using intercepted responses. |
| Measurement | generate_lead requires Formspree ok=true. request_demo additionally requires an explicit Kraken demo intent/product. Phone, email and WhatsApp are click events only. Event parameters whitelist page/language/service/product and exclude entered text and personal data. |
| Booking | Existing Calendly scheduling link now opens an accessible dialog, loading the provider only on user action. Confirmed booking event checks Calendly origin, active iframe source, scheduled-event URI and duplicate delivery. Direct-link fallback remains available. Public calendar reached the real Select a Date & Time screen; no time was selected or booking submitted. |
| Consent | Production GA4 is opt-in, respects Do Not Track, supports denial/revocation/re-consent and sanitizes page URLs. Local/GitHub previews send no analytics. Provider tag calls were intercepted for verification. |

## Verification record

- 51 routes; 204 layouts at 1440, 768, 390 and 320 pixels: no horizontal overflow, broken local images or JavaScript errors.
- 12 additional header breakpoint checks: 1121, 1180, 1280 and 1366 pixels in all three languages.
- 308 existing interaction checks, 113 October navigation/measurement checks, 67 booking checks: 488 total.
- 2,625 local links/assets validated by `scripts/check-pages.py`.
- Both preview and production builds: 51 canonical URLs, 48 sitemap URLs, complete language alternates and original logo integrity.
- Desktop and mobile screenshots of all 13 main page types inspected. QA JSON and PNG evidence is local under `qa/proposal/` and excluded from publishing.
- Forms, Google tag transport and booking confirmations were intercepted in tests; these tests do not prove actual email receipt, real booking creation or GA4 ingestion.

## Independent review, 5 October 2026

Five reviewers read this revision (JavaScript, content claims, SEO/accessibility, the production `.htaccess`, publication safety). Each finding was then checked by three skeptics; 20 of 24 were confirmed and fixed here, except one (below).

- `production.htaccess` now matches the live root's protections: `.env`/`.ht*` files are denied (the live root keeps the chat API key in `.env`), `/stats` routes to the admin page, `/stats/storage/` is forbidden, `/index`, `/index-en`, `/index-de` keep their 301s, HSTS and Permissions-Policy are back, and the strict CSP applies to the new pages while `/stats/` keeps a policy that allows its inline code. The clean-URL rule now checks `%{DOCUMENT_ROOT}/$1.html` for paths without a dot: the `%{REQUEST_FILENAME}.html` form makes `/services/x` loop and answer 500, which the live site still does today. The `.html` redirect is anchored to the request path, and the `optech_footer` rule drops the query with a trailing `?` instead of `QSD`.
- The 404 pages use absolute links (`PUBLIC_BASE`), so they keep their styles and links at any depth: `/a/b` in production, `/ITD2027/calm/x` on GitHub Pages.
- `measurement.js`: leads from catalogue CTAs, Kraken OS sector chips and the AI Agents form now carry their service or product (exact lists, then keywords in SQ/EN/DE, then the page; `ai-agents` maps to `ai-automation`).
- `booking.js`: browsers without `<dialog>` keep the plain Calendly link; reopening the dialog while `widget.js` loads no longer embeds two calendars; a later Calendly message no longer replaces the confirmation.
- `qa-seo.py` reads the tracked public sitemap snapshot `seo-live-sitemap.xml`, stops before writing if it is missing (it used to shrink `seo-url-map.csv` to 4 rows), writes the CSV only after its checks pass, and records the `/index` redirects (34 URLs).
- English brand lines on Albanian and German pages carry `lang="en"`; the ITD Labs menu marks the current product page with `aria-current`; the Kraken Communications screenshot description is translated.
- Not changed: the meta descriptions of contact, terms and privacy still repeat the page title (privacy says "in this version"). The fix was prepared but not applied in this session; the live site's descriptions are a ready replacement.

Accessibility audit, 7 October 2026 (axe-core 4.10, WCAG 2.1 A/AA + best practice, all 51 pages at 1280 and 390 px): the agent numbers on the AI Agents cards (3.8:1) and the Kraken OS image caption (4.2:1) now pass contrast; the project-detail case title is an `h2` (same look, see `revision.css`) and the projects grid has a visually hidden `h2`, so headings no longer skip a level; the contact details block is a `div` instead of an `aside` inside `main`. Result: 0 violations.

Verified after the fixes: `check-pages.py` 51 pages, 0 errors; `qa-seo.py` preview and production, 0 errors; lead classification for 17 labels, the booking reopen case and the no-`<dialog>` fallback in a browser with Calendly stubbed.

## Change report 02, 8 October 2026

`ITD2027_Raporti_i_Ndryshimeve_02` (15 pages) applied:

- **Home banner:** the "Built for what's next." box is now a slideshow of three slides (Kraken OS, Kraken Communications, AURA), changing every 10 seconds with a thin progress bar, arrows, dots, swipe and a pause button. It pauses while the mouse is over it, while keyboard focus is inside it and during a touch. With reduced motion it never turns by itself. Without JavaScript it shows the first slide. Slides are edited in `SLIDES` in `revision.py`: order, title, text, link, and a desktop and optional mobile image. The code is `site/assets/slider.js`, loaded on the home pages only. The 10 s timer is the CSS progress animation, so pausing the bar pauses the slideshow.
- **Partners:** no categories. Nine cards with black and white logos, a name and a short description (report p. 6): Cisco, MikroTik, Hostinger, Paysera, Raiffeisen Bank, Adobe, Optika Miftari, KoBags Group, Human+ Qendra Diagnostike. Home shows the first six and "Shiko të gjithë partnerët". eConnect, iMatrix and Comtrade are removed, including their logo files. The descriptions are still to be approved (report p. 15).
- **"Le të flasim":** the same black box (#0B0D10, red label, white text, red Contact button, white-outline WhatsApp) wherever it is used. The label is #ff4d4d, because #E00000 on black is 3.85:1, too low for small text.
- **ITD Labs green #008000:** labels, buttons, card lines and the menu indicator. Small text on light backgrounds uses #006600. Product art, the Kraken logo and the AURA emblem keep their own colours.
- **Kraken:** the official, transparent Kraken logo (the file used on krakenos.cloud and assistant.krakenos.cloud) in both product heroes, plus a separate link to each official site.
- **AURA:** its own page (`aura`, `aura-en`, `aura-de`), reached from "Shiko produktin" on the Labs card, the ITD Labs menu, the footer and the home slide. It has the vector emblem, the short description and only the confirmed functions (voice, tasks, meetings). The app link is added when the app is ready.
- **AI Agents:** one robot head with six expressions (open smile, analytical look, soft eyes, determined focus, curious eyes, precise), using the existing palette.
- **About:** the four steps are a graphic panel (Discovery, Planning, Delivery, Improvement); "Për njerëzit pas çdo procesi" is a black box. Text unchanged.
- **Projects:** unchanged. The examples stay labelled as illustrative until real projects are supplied.

Checks: `check-pages.py` 54 pages, 0 errors; `qa-seo.py` preview and production 54 pages, 51 sitemap URLs, 0 errors; axe (WCAG 2.1 AA + best practice) at 1280 and 390 px and overflow at 320 and 390 px on all 54 pages; slideshow behaviour (autoplay order, pause, hover, keyboard focus, swipe, reduced motion, no JavaScript) in Chrome.

## Link previews, structured data and lighter pages, 9 October 2026

- **Link previews:** every page except the 404 has Open Graph and X (Twitter) tags: title, description, canonical URL, locale and a 1200×630 share image per language (`assets/brand/og-sq.jpg`, `-en`, `-de`, made in the site's style, about 50 KB each). Shared links on WhatsApp, Facebook, LinkedIn or X show a proper card. The page title and description are the same as in search results.
- **Structured data (schema.org JSON-LD):** Organization (name, logo, email, phone, Prishtina, social profiles), WebSite, WebPage and, below the home page, a BreadcrumbList (for example Home › ITD Labs › AURA). Built by `share_tags()` in `proposal.py`; `apple-touch-icon` uses the 512 px shield.
- **Lighter images:** the product screenshots and the About texture are WebP instead of PNG (1.7 MB → 0.19 MB). The ITD Labs cards use the slide images: the Labs page loads 37 KB of screenshots instead of 521 KB, Kraken OS 133 KB instead of 959 KB, Kraken Communications 42 KB instead of 298 KB, and About 10 KB instead of 441 KB. The unused PNGs were removed.

## Design audit, 9 October 2026

Every page type was reviewed at 1440 and 390 px against change report 02. Fixed:

- **Process everywhere:** Services, Websites & software and AI automation showed the four steps as plain text; they now use the same graphic cards (phase, number, title, line) as About, four across on desktop, two on tablets, one on phones (`steps()` in `proposal.py`).
- **Project tiles:** the illustrative examples had abstract icon-and-dots placeholders. They are now small screen mock-ups in the same language as the featured case: connected sites, approvals in a table, a distributed team, and reporting with a conversation (`project_art()`, shapes only, no text, hidden from screen readers). They stay labelled illustrative until real projects are supplied.
- **Font:** Plus Jakarta Sans is served as a subset WOFF2 (`assets/fonts/plus-jakarta.woff2`, 38 KB instead of the 176 KB TTF; Latin, Latin-1, Latin Extended-A, the punctuation, arrows and € the site uses; weight axis 200–800 kept). The unused Manrope and Sora files are removed. The ⌄ in the ITD Labs menu was never in the font and keeps its system fallback.
- **Web app manifest** (`site.webmanifest`, written by the build) with the site name, colours and the 512 px shield; `production.htaccess` declares the WOFF2 and manifest types and caches fonts and images for 30 days (HTML, CSS and JS keep 5 minutes).
- `preview.mjs` serves `.woff2`, `.jpg` and `.webmanifest`; `qa-signature.mjs` checks the WOFF2 instead of Manrope.

Not changed on purpose: the hero carries no "140+ projects / 40+ clients" numbers (report 01's hero concept has none). Still needed from the client: real projects, approved partner descriptions, the AURA app link.

## Change report 03, 10 October 2026

`ITD2027_Raporti_i_Ndryshimeve_03` (12 pages) applied:

- **Real projects:** the illustrative project tiles and brandbooks are gone from Projects, and the illustrative case is gone from the home page. Both now show the five published sites: verkaufeimmobilie.de, RATA Solar, KoBags Group, Paketoje and Optika Miftari. Each card has a screenshot from the live site (from the report), a category, a short description and a link that opens the project in a new tab. Every project is one record in `PROJECTS` in `proposal.py`: name, category, description, screenshot, today's `url` and `final`. When a client moves to its own domain, only `final` changes. Public text does not mention subdomains or GitHub. The Projects description in search results now describes the published work. The illustrative case page (`project-detail`) remains, linked as an example from the service pages.
- **Manrope everywhere:** self-hosted variable WOFF2 (Latin and Latin Extended, `assets/fonts/manrope-*.woff2`, OFL), with only the real weights 400/500/600/700 (650/750/800 were mapped). Headings are 700 with a more open rhythm (H1 56–60 px, H2 up to 42 px, mobile H1 36–42 px), text is 16–18 px, and content labels are at least 12 px. Hover no longer scales button text (only a 2 px lift). Plus Jakarta Sans is removed. The share images were redrawn in Manrope. ITD2027/M uses the same Manrope file.
- **The IT Department banner opens the slideshow:** slide 1 is the team's 1536 × 1024 banner, shown whole (`object-fit: contain`) on a dark ground, with its words as the alt text and no second title over it. Then Kraken OS, Communications and AURA follow. It is still 10 seconds per slide, with manual controls, pause and reduced motion. A `banner` slide type in `SLIDES` takes a finished picture.
- **ITD Labs:** "ITD Labs" in the menu is a plain link to the Labs page, on desktop and in the phone menu. There is no product dropdown, and the link stays underlined in green on the product pages. The Labs page has a pale green hero ("ITD LABS / PRODUKTET TONA", "Ndërtuar nga IT Department për punë më të qartë."). Each card has a green strip, the product view on top in its own colours, a green "01 / PLATFORMË" label, the name and description, and a filled green "Shiko produktin" button.
- QA scripts updated for the direct link and Manrope.

## Change report 06, 13 October 2026

Source: `ITD2027_Raporti_i_Ndryshimeve_06.pdf` (17 pages, the only document for this round). The changes are in `report06.py` (executed after `revision.py`) and `site/assets/report06.css`. Only the main version loads that stylesheet; ITD2027/M keeps its look and only shares the partner list.

- **One axis for titles:** on Home, Services, Projects, Partners, ITD Labs, About and Contact (`<body data-axis="center">`), the page and section titles, descriptions, filters and card names are centred. Descriptions have a limited width and a line height of 1.5–1.6. H1 is 56–62 px on desktop and 36–40 px on phones. Long text, FAQ answers and form labels keep normal alignment. The closing black box and the About introduction are centred too.
- **Home:** the title, text and both actions are centred at the top, with the slideshow below them. Slide 1 is still the IT Department banner, and each slide still shows for 10 s with arrows, indicators and a pause button below the slide. On wide screens the previous and next slides show beside it. Clicking one turns the slideshow, and they are hidden from assistive technology because the arrows and dots do the same job. The background is warm white with a very light grid and thin red lines only at the edge. A light band separates the partners.
- **Partners:** all nine are on the home page in 3 × 3 (two columns on tablets, one on phones). The logo sits above the name and a short description, in the report's order and wording: KoBags Group, Human+, Optika Miftari, Cisco, MikroTik, Hostinger, Paysera, Raiffeisen Bank, Adobe. The Partners page uses the same list.
- **Services:** the title sits in a black box with thin red lines at both edges. The filters are centred (the active one red, the others light), and the card titles are centred with a red "Shiko detajet" button.
- **ITD Labs:** a green gradient covers the whole page, header and footer included. The logo is the original file with its red turned into #008000 (`assets/brand/logo-labs.png`). The hero is centred ("Ide që bëhen produkte.", new description, "Eksploro produktet" and "Le të flasim"). Below it, Kraken OS, Communications and AURA are layered, with a small drawn flask badge: an SVG whose bubbles rise and fade over 7 s while the flask floats 2–3 px, and which stays still with reduced motion. The catalogue ("Një ekip / tre produkte", "Produktet tona.") has cards with depth, a centred name, tags and "Shiko produktin". AURA keeps its own tones, and the contact box and footer are green.
- **Creative:** Branding, Social, Video & Motion and Fushata are bigger boxes (16 px, 46 px high, 12 px apart) that wrap naturally on phones.
- **AI Agents:** the approved character from the report sits in the existing orbit with the AI mark and fits inside it.
  - It is animated as a character, without a Lottie or Rive player. The report's picture is split into six layers on one 360 × 311 canvas in `assets/ai/character/` (about 27 KB in total): both feet, the body with the left hand, each eye, and the raised right hand. Each eye is separated from the visor as colour plus transparency and the visor under it is filled in. Stacked without movement, the layers rebuild the original picture (mean difference 0.05 of 255); that is also what visitors who prefer reduced motion see.
  - `report06.css` moves each part along the storyboard on page 15, on one 7 s loop shared with the four phases:
    - **Request, 0–1.5 s:** the eyes look towards the request.
    - **Agent, 1.5–3 s:** a blink of about 150 ms, and the hand lifts to prepare the step.
    - **Approval, 3–4.5 s:** a small gesture down towards approval while the body leans.
    - **Action, 4.5–6 s:** the eyes turn to the action and brighten, then everything returns softly.
    - Then one second of rest.
  - The character floats 5 px and the feet follow slightly later. The active phase lights up in sync.
- **Contact:** the title is centred. As in the report, the form runs the full width under the three ways to start, with the privacy line and the send button on one row. The address, phone and map follow below it. The form card is black, with a red title, a short line under it ("Pak kontekst na ndihmon të nisim nga pika e duhur."), white labels, light fields and a red button. The success and error messages have light colours on the black. The fields and Formspree sending are unchanged.
- **Smaller points from pages 3–5:** titles are at least 56 px on desktop. The banner slide has no label over it, as in the mock-up. The menu lines on the black header are red.
- **Translations:** the English and German pages were scanned for Albanian, and the German pages for English (product names and fixed brand lines excepted). No untranslated text was found.
- Verified: 54 pages pass check-pages.py and qa-seo.py, ITD2027/M passes its check, axe finds 0 violations on all pages, and there is no sideways overflow at 320 or 390 px. The slideshow test passes 72/72, and the previews, character layers and blink, contact order, Labs logo and bubbles pass 12/12.

## Change report 07, 16 October 2026

Source: `ITD2027_Raporti_i_Ndryshimeve_07_v2.pdf` (17 pages). The changes are in `report07.py` (executed after `report06.py`), `site/assets/report07.css` and `site/assets/orbit.js`. Only the main version loads them; ITD2027/M keeps its look. The images come from the report itself, because no separate package was supplied.

- **Home slideshow:** the four service banners replace the IT Department, Kraken and AURA slides, in the banners' own order 01–04:
  - Web & Software → `services.html#web`
  - IT & Security → `services.html#it`
  - AI Agents → `ai-agents.html`
  - Creative → `creative.html`
  
  They are shown whole at 16:9 (`assets/home/service-*-800|1600.webp`). The text in each picture is the alt text.
  - **Motion:** the cards sit on an orbit, as on pages 3–4. Every 6 s the right card comes forward to the centre and grows, the centre card moves to the left and shrinks, the left card goes to the back, and the back card comes in on the right. Position, size and depth change in one 900 ms transition, so a full cycle is 24 s.
  - **Controls:** there is no visible pause button. The indicators choose a card and the 6 s rhythm continues from there, and a click on a side card turns the orbit.
  - **Pausing:** the orbit holds while a mouse is over it, while keyboard focus is inside it, and during a touch. Keyboard users meet a pause button when they tab into it (required by WCAG 2.2.2). With reduced motion it never turns by itself.
  - **Phones:** the centre banner fills the width and the cards cross-fade, with "01 / Web & Software" under the indicators.
- **Buttons:** the diagonal arrow is removed from every button and text link on all pages and in all languages, including the Calendly fallback link. The corner marks on clickable cards and the "opens in a new tab" mark on project names stay.
- **ITD Labs:** the supplied Kraken OS and Kraken Assistant banners replace the two pictures in the hero composition and on the catalogue cards. They are shown whole, and positions, sizes and angles are unchanged. AURA keeps its own view. The cards follow page 8: a larger name, the tags as plain text and a wide "Shiko produktin".
- **Kraken Assistant:** the new name replaces Kraken Communications in the website interface: the slide, the catalogue, the product page, the footer, the form options, the page titles and descriptions, EN/DE, and the opus version. Page addresses (`kraken-communications.html`) stay the same, so existing links keep working.
- **About:** the red "Punë më e qartë. Sisteme më të sigurta." box is removed with its space. The three values follow the introduction directly, numbered in red.
- **Contact:** the form is unchanged. Under it, "Preferon të shkruash?" now has a short line and two red buttons: `mailto:info@itdks.tech` and `tel:+38349573570`, followed by the address and hours.
- **Footer (every page):**
  - **Brand column:** the shield with "IT Department", the line, and `info@itdks.tech` as a red outlined button.
  - **Link columns:** Kompania, Njësitë and ITD Labs (with Kraken Assistant).
  - **Bottom row:** copyright, Privatësia/Kushtet, and Instagram, LinkedIn and Facebook as white mono icons in circles, each with an accessible name.
  - **Phones:** the name, the email button and the icons are centred, as on page 16.
  - **Sub-brand colours:** ITD Labs uses the green shield, and Creative and AI Agents their own.
- **AI Agents cards:** the six character variants from page 14 replace the icons. Each card shows its own character next to its name and role, in the agent's colour (#7EDDE6, #B7A8FB, #8BBDE6, #E1A1D2, #91DCB7, #E6C890).
  - **Layers:** every variant is scaled to the same body size on one canvas and split into feet, body, eyes and hands, in `assets/ai/agents/<name>/` (about 90 KB for all six).
  - **Motion:** each character floats 3 px and blinks, and makes the gesture of its role:
    - Ari waves.
    - Dita tilts her head.
    - Nora opens both hands.
    - Leo points ahead.
    - Mira explains.
    - Fin balances both hands.
  - **Timing:** the cycles are shifted by one second per card, so the cards never move together.
  - **Size:** 104 px on desktop and 84 px on phones.
  - **Links:** the card ends with "Shiko detajet +", as in the report; the separate "Diskuto këtë agjent" link is gone, and the form below still offers the agent choice.
  - The AI Agents hero keeps the approved animated character.
- Verified: the orbit test passes 40/40. It covers order, links, whole banners, 6 s and 900 ms, indicators, side-card clicks, focus, the pause button, reduced motion, phone, no JavaScript, and the other report 07 points. The report 06 checks still pass 6/6. 54 pages pass check-pages.py and qa-seo.py, M and opus pass their checks, axe finds 0 violations, and there is no sideways overflow.

## Change report 08, 18 October 2026

Source: `ITD2027_Raporti_i_Ndryshimeve_08.pdf` (55 pages, the only reference for this round). The changes are in `report08.py` (executed after `report07.py`), `site/assets/report08.css`, `site/assets/report08.js` and a rewritten `site/assets/orbit.js`. Text changes that live as literals in the older layers were made in place (`proposal.py`, `revision.py`, `report06.py`, `report07.py`). The corrected texts reach ITD2027/M as well; the font, orbit, map and WhatsApp button are on the main version only.

- **Orbit (pages 4–5):**
  - **Timing:** JavaScript times the orbit; the CSS animation no longer drives it. Each step lasts 5 s: the centre card is read for 4 s, then the cards change place, size and depth in 1 s. A new card arrives at 5, 10, 15 and 20 s.
  - **Countdown:** the progress bar and a countdown under the card ("05 s" … "01 s") follow the same clock.
  - **Manual control:** the indicators, a click on a side card, dragging with the mouse (Pointer Events, about 40 px) and a horizontal swipe on phones (`touch-action: pan-y` keeps vertical scrolling) all start a new 5 s cycle. A drag never opens a card; a click on the centre card opens its service.
  - **Movement (follow-up, 19 October):** the cards now travel on one continuous ellipse that the script draws every frame. Place, size, depth and turn change together; the left card passes behind to the right, and the text is never turned round. While dragging, the cards follow the pointer and settle on the nearest card when released. On phones the banner glides out to one side as the next comes in from the other. The earlier version moved each card in a straight CSS transition between fixed places.
  - **Cache:** every stylesheet and script link carries a content fingerprint (`?v=…`, added in `finalize`), so a browser never combines a new page with a script cached from an earlier version. GitHub Pages caches files for 10 minutes, and that combination could stop the slideshow from moving.
  - **Pausing:** hovering no longer stops the orbit. It waits while the visitor drags or has keyboard focus inside it, and a hidden tab does not pile up changes. Keyboard users still meet the pause button when they tab in. With reduced motion it never turns by itself and the countdown is hidden.
- **Banners in three languages (pages 6–12):** the four service banners and the two Kraken banners are in SQ, EN and DE, 18 files in `assets/home/service-*-{sq,en,de}-{800,1600}.webp` and `assets/labs/kraken-*-banner-{sq,en,de}-{600,1200}.webp`. They are taken from the report's own images, because the package of originals was not supplied. The alt texts are in the page language. The "IT Department / Your Technology Partner" line, the logos, the product names and the domains stay as they are.
- **Font (pages 13–14):**
  - **Source:** Outfit from Google's official repository (`ofl/outfit/Outfit[wght].ttf`, downloaded with the owner's permission), served by the site as a 45 KB WOFF2 with its OFL licence (`assets/fonts/outfit/`). Only that file is preloaded, the old Manrope preload is gone, and it covers every character the pages use.
  - **Where it applies:** Outfit is set on `html, body, button, input, select, textarea`, so titles, menu, buttons, forms and footer all use it.
  - **Type scale:** H1 48–56 px on desktop and 32–38 px on phones; section H2 32–40 px; text 17 px (16 px on phones); menu and buttons 14–15 px at weight 600; notes 13–14 px.
  - **Header fit:** at 1121–1340 px the header gaps are tightened so the 14 px menu fits.
- **Contact (pages 15–16):**
  - **Title:** the page title is "Flasim për projektin tënd.".
  - **Map section:** "Na gjen në Prishtinë." now follows the form and the direct contacts. It shows a sketch with the pin and a "Shfaq hartën" button: the Google Maps embed (approved pin 42.655800066393724, 21.151119141173435; lazy; localised title) loads only after that click. Beside it are "Prishtinë, Kosovë", the note that the location is approximate, "Hap në Google Maps" (https://www.google.com/maps?q=42.655800066393724,21.151119141173435) and the email. On phones the order is ways to start, form, email/phone, map, footer.
- **WhatsApp (page 17):** a 56 px button sits fixed 24 px from the bottom-right corner on every page; on phones it is 52 px, 16 px from the edge plus the safe area.
  - **Look:** the outline follows the section (red; ITD Labs and its products green; Creative pink; AI Agents teal). It has no arrow and no constant animation, plus a localised accessible name and tooltip.
  - **Link:** wa.me/38349573570 with the localised opening message.
  - **Getting out of the way:** it sits inside the footer landmark. It is hidden while the phone menu or a dialog is open, it rises above a cookie panel, and it steps aside while the form's send row or the footer's bottom row is on screen.
- **Texts (appendix A, all 17 page types in SQ/EN/DE):**
  - **Home and services:** home introduction; headings for the four areas, projects and partners; services title (EN/DE), introduction, the four area descriptions and the eight described results.
  - **Projects and the illustrative case:** projects title, introduction and a "Shiko faqen" button on each project; case label "Skenar demonstrues", its explanation and flows.
  - **Partners:** title and introduction.
  - **ITD Labs:** title (EN/DE), introduction, catalogue title, the three card texts, localised tags, and the AURA status line.
  - **Product pages:** Kraken OS hero ("Shumë procese. Një sistem."), introduction and module texts. Kraken Assistant title, introduction, section title and an "Hap Kraken Assistant" button to assistant.krakenos.cloud. AURA hero ("Thuaje. Ktheje në veprim."), introduction, voice label, meetings and status.
  - **Creative:** English title, introduction, and the four box names.
  - **AI Agents:** introduction, flow, roles, the six descriptions, Ari's actions, the shared human-approval text, "Nis një projekt pilot" and the "Agjenti AI" form label.
  - **About:** title, introduction and the four process steps.
  - **Contact and service pages:** contact texts, the web and AI introductions, the German web title, and "Skenar demonstrues".
  - **Forms, FAQ and legal pages:** form messages, success, failure and note (in the site-copy JSON too); the corrected FAQ answers; the privacy page as four technical paragraphs; the four terms paragraphs (language only); and the closing box text.
  - **Global:** "View product" in English. In Albanian, one terminology (miratim, mbështetje, Të dhëna) throughout.
- Verified:
  - **Report 08 checks:** a new acceptance test (`test08.py`) passes 47/47 against the criteria on page 23. It covers the clock (center changes at 5/10/15/20 s, 1 s move, countdown and progress), drag, swipe, short drag, indicators, side clicks, hover, focus, the hidden tab and reduced motion. It also covers banners per language, Outfit loaded and used everywhere, no sideways scroll at 375, 390, 768 and 1440 px, and the map, mailto, tel and WhatsApp details and behaviour on all 51 pages.
  - **Texts:** `verify_texts.py` confirms every appendix text on its page in the three languages, and the language scan finds 0 untranslated strings.
  - **Regression:** 54 pages pass check-pages.py and qa-seo.py (preview and production); M and opus pass their checks; axe finds 0 violations and there is no sideways overflow.
- **Still for the team before the final launch (page 22):**
  - **Indexing and domain:** the production build already removes noindex and points canonical, hreflang, Open Graph, schema and the sitemap to the final domain (`ITD_PRODUCTION=1`, `ITD_SITE_URL`). The GitHub preview stays noindex.
  - **Real-world tests:** a real Formspree delivery, email receipt and Calendly confirmation; the HTTPS, cache and error-page check on the final domain; real-device tests.
  - **Replace the banners:** swap in the originals from the source files once they are supplied.

## Change report 09, 19 October 2026

Source: `ITD2027_Raporti09_Vetem_Ndryshimet_e_Fundit.pdf` (7 pages, the last changes before going live). Only the main version is affected; ITD2027/M is unchanged.

- **Slideshow:** a new card every 2.5 s (`STEP=2500`, `MOVE=1000`, `READ=1500` in `orbit.js`). The cards arrive in the centre at 2.5, 5, 7.5 and 10 s, and the approved orbit movement is unchanged. The numeric countdown is gone: the `[data-countdown]` element, its CSS and the code that wrote the seconds, with no empty line left. The indicators and the service name ("01 / Web & Software") remain, now on every width. Clicking, dragging and swiping are kept.
- **AURA box on ITD Labs (`report09.py`, `assets/aura-live.js`, `assets/report09.css`):** only the emblem and the phrase on the right move. The title, text, button and the box layout stay, and the Labs hero and catalogue are unchanged.
  - **Emblem:** inline SVG built from the original ribbon geometry (`assets/labs/aura-emblem.svg`, itself rebuilt from the AURA app's drawing code). It uses the AURA app's active state, read from the app's own build: the three ribbons turn on their own (4.8 s, 6 s in reverse, 4.8 s), the emblem breathes (`orb-breathe` 4.4 s) and the halo pulses (2.8 s). The glow sits behind the lines.
  - **Phrase:** "Say it." is static. "Consider it handled." is typed as HTML text: a short wait with a cursor, about 60 ms per letter, the full phrase held for 3 s, a 300 ms fade, then again. It is set in Outfit 400 at 12 px (11 px on phones). The phrase's box always holds the full phrase, so nothing jumps.
  - **Behaviour:** it runs only while the box is on screen and the tab is active. Screen readers get the phrase once (the typed copy is hidden from them, no aria-live). There are no new controls, no sound and no microphone. With reduced motion the emblem stands still and the full phrase shows without a cursor. The brand phrase stays in English on SQ/EN/DE pages.
- **Cache:** the version fingerprints on CSS/JS links make browsers load the new orbit and AURA files right after publication.
- **Going live on itdks.tech (19 October):** the owner chose the main domain, indexable, with Google Analytics after consent.
  - **Package:** the production build (`ITD_PRODUCTION=1`, `ITD_SITE_URL=https://itdks.tech`, `ITD_ANALYTICS=1`, `ITD_INDEXABLE=1`) is packaged as `qa/release/ITD-itdks.tech-2026-10-19.zip` (206 files, mode 0644). Next to it are a manifest, an upload guide and a list of 34 current-site files the new site no longer uses, among them the old chatbot `chat.php`; `stats/` and `.env` stay.
  - **Fixes for the server's security policy:**
    - The Google map is added to `frame-src`, and `data:` to `img-src` for the decorative SVG lines.
    - The agent characters' pivot points moved from style attributes into `report09.css`, since `style-src 'self'` blocks inline styles.
    - The WhatsApp button now really rises above the cookie panel: the check used `offsetParent`, which is always null for a fixed element.
  - **Privacy page:** in that build it describes Google Analytics with consent, together with the report 08 paragraphs on forms, external services and fonts.
  - **Tests:** the production build, served with the same CSP and clean URLs, shows no policy violations on the key pages. The orbit, map, AURA, agents, Outfit and consent panel all work, and Google Analytics does not load before consent. axe finds 0 violations and there is no overflow.
- Verified: `test09.py` passes 63/63 (the 2.5 s rhythm and 1 s turn, no countdown on desktop and phones, the service name, all earlier orbit, language, font, width, contact and WhatsApp checks, and the AURA checks of page 7). The audit was rebuilt after the scratchpad was cleaned: axe finds 0 violations on 54 pages and there is no sideways overflow. check-pages.py, qa-seo.py (preview and production), M, opus and the language scan pass.

## Change report 10, 21 October 2026

Source: `ITD_Raporti10_Final_v2.pdf` (14 pages; the round after going live). Only the main version is affected; ITD2027/M and opus are unchanged. The work is a new layer, `report10.py`, with `assets/report10.css` and `assets/report10.js`.

- **Typography (pages 2-3):**
  - Outfit at its real weights only, with `font-synthesis: none`: 700 for titles, 600 for the menu and buttons, 400 for text.
  - Desktop: H1 48-56 px, text 18 px at 1.6, buttons 16 px. Phones: H1 36-40 px, text 17 px. Titles stay centred.
  - The phone and desktop now share the same H1 weight and letter-spacing.
  - Two text boxes no longer sit under a transform, so their text stays sharp: the WhatsApp label (it was centred with a half-pixel offset) and the KrakenOS screenshot caption (a 3D tilt).
- **Partners (page 4):** Cisco, Hostinger, MikroTik, Adobe, KoBags Group, Paysera, Optika Miftari, Raiffeisen Bank, Human+. The order is the same on the home page and /partners, in SQ/EN/DE, and on desktop and phone; the DOM follows the same order.
- **Decorative numbers (page 5):** removed from the finished pages of every language, together with the space they used.
  - Standalone numbers on cards, process steps, the AI flow and agent cards, about values, contact paths and service details.
  - "01 / " in front of labels: Labs eyebrows, process phases, "PARTNER", and the slideshow caption, which now shows only the service name.
  - The "0N / 04" counter drawn inside the four home banners (SQ/EN/DE), retouched from the original report 08 artwork; "IT DEPARTMENT" stays.
  - Prices, phone numbers, dates and the slide positions read out to screen readers keep their numbers.
- **Icons (page 6):** four new SVGs for the home areas and the matching service families: window + code, shield + check, assistant with eyes and antenna, pen nib + shape.
  - One 26-unit grid, 1.5 stroke, round ends, `currentColor`, on a soft red tile.
  - 26 px at every width, `aria-hidden`; hover and focus lift them 2 px in 0.2 s.
- **Characters (pages 7-10):**
  - **AI character, 7 s storyboard:** listens (looks at the request), thinks (tilts up to 3°, eyes pulse), waves (hand 12-18° at the shoulder, the ring glows), then settles with a short nod. Float is 7 px.
  - **Six agents, each with its own gesture:** Ari waves and looks back; Dita reads and nods; Nora opens both hands; Leo points twice and nods; Mira explains with her eyes following the hand; Fin balances and confirms. Float is 5 px, the body moves up to 3°, hands 10-18°, blinks last about 150 ms, and loops run 6.6-7.6 s.
  - **How the motion is built:** an outer frame floats, a rig inside it tilts and nods, and hands and eyes turn on their own joints. Separate properties are used, so no two loops write the same transform.
  - **When it plays:** each figure moves only while on screen. It starts from the beginning when it appears; figures that appear together gesture 1.1 s apart. A hidden tab pauses everything. Hover or focus gives a short hop. With reduced motion the figures are still and complete.
- **Terms and Privacy (pages 11-13):** two full pages in SQ/EN/DE.
  - **Layout:** a centred title, summary and update date (21.10.2026). A topic menu sits beside the text on wide screens and above it on phones, and marks the section being read. Text is 18 px at 1.65 in a column of about 70 characters (17 px on phones).
  - **Privacy:**
    - Identity.
    - Each data flow with its data, purpose, legal basis and retention: form, browser draft, email/phone/WhatsApp, Calendly, Google Analytics with consent (production only), server logs, map and fonts.
    - External providers with links to their policies, and transfers outside Kosovo.
    - Rights under Law 06/L-082, with the AIP link.
    - A table of what is stored in the browser, and how to refuse and withdraw.
  - **Terms:** identity and scope, offers and services, content and ownership, use and links, liability (no absolute exclusions), complaints and changes.
  - **What the pages describe:** only what the site really does, read from its code and security policy. The legal name, address and business number appear once they are entered in `LEGAL_ENTITY`; until then the pages show the published identity (IT Department, Prishtina, email, phone).
- **Verified:**
  - Report 10 test: 61/61. It covers partners, numbers on 51 pages, icons, typography at 360-1920 px, the seven characters sampled for 11 s (float, tilt, hand, blink and the gesture order), in view and off screen, hidden tab, hover, reduced motion, both legal pages in three languages and two widths, keyboard, and widths 360/390/768/1440/1920 plus 200 % zoom.
  - `test09` passes 63/63, updated for the caption without "01 /" and 18 px desktop text.
  - Production with its CSP and clean URLs: 25/25, including a real consent test with Google blocked at the network level. The first visit loads nothing; "No analytics" holds across pages; "Allow" loads GA; withdrawal deletes the `_ga` cookies.
  - axe finds 0 violations and there is no overflow. check-pages, qa-seo, M (54 pages), opus (18) and the language scan pass.
- **Open for the company (pages 12-13):**
  - The legal name, registered address and business number.
  - Real retention periods for enquiries and emails, and the GA4 data-retention setting (the page says "no more than 14 months").
  - Confirmation of the jurisdiction wording.
  - Legal approval of the final texts.

## Change report 11, 21 October 2026

Source: `ITD_Raporti11_Profesional_SQ_EN_DE_v3.pdf` (18 pages): the AI Agents scenes in three languages, and the remaining font and legal items. Only the main version is affected; ITD2027/M and opus are unchanged. The work is a new layer, `report11.py`, with `assets/report11.css` and `assets/report11.js`.

- **Six scenes (pages 5-12):** each agent card now opens with a scene, then the name, role and text.
  - **Each scene has:**
    - the status at the top;
    - three phase marks;
    - the character beside its work object;
    - the sentence below the scene (13 px, two lines reserved);
    - a three-part progress bar.
  - **Scene size:** 150 px on desktop and 136 px on phones.
  - **The task:** each agent does one 9 s task (start 0-2 s, work 2-6 s, result 6-9 s).
    - Ari lifts a phone with the arm, voice waves pulse and the request is noted.
    - Dita types (hand 2-4 px, keys light at irregular moments) while the table rows fill.
    - Nora receives a question, three typing dots appear while she points to the answer, then the reply is sent and she opens her hands.
    - Leo moves a task card across three columns (0.63 s each, ease-in-out), points to approval and nods.
    - Mira opens a document, a lens follows her hand along the lines, and the found section lights up.
    - Fin takes a calculator, three keys light, the chart grows from the base and he presents it.
  - **How it is drawn:** all objects are inline SVG in one family (thin outlines, soft corners, the agent's colour). Hand-held objects sit in the arm's group and turn around the shoulder. Text inside the scene is replaced by shapes; real sentences are HTML outside the scene.
- **AI character (page 6):** the box now shows the character beside the vertical flow Request / Agent / Approval / Action, with a demo caption and a three-part bar.
  - **9 s loop:** listens (0-2 s, Request lit), works with the hand (2-5 s, Agent), points to Approval (5-7 s), then nods and returns (7-9 s, Action).
  - **Movement:** float 6 px, body up to 2.8°, hand up to 21°.
- **Languages (pages 13-17):** one dictionary in SQ/EN/DE (`r11-copy`, keys like `ari.state_work`, `nora.message_done`), with the report's texts.
  - `report11.js` reads each scene's CSS clock, so texts and gestures stay in step. It types the work sentence at 45-85 ms per letter with a cursor.
  - If the page language changes, every scene restarts cleanly in the new language.
  - The scenes are `aria-hidden`; a full sentence per scene stays in HTML for screen readers, with no aria-live typing.
- **Behaviour:**
  - Scenes start when they come into view, also on phones. Scenes that appear together start 1.1 s apart.
  - A scene rests off screen and pauses in a hidden tab.
  - With reduced motion the scenes are still and show the readable result.
  - No audio, microphone or real data.
- **Font (page 4):** a proof was run in Chrome and Edge at 100 / 125 / 200 % and on a phone. The site's Outfit file paints every letter, including Ë ç Ä ö Ü ß and digits, at its real instances: Bold titles, SemiBold buttons, Regular text. Synthesis is off, the WOFF2 answers 200, and Outfit is loaded before the first paint, so no fallback is shown. Only the client's confirmation on their own computer remains.
- **Legal (pages 2-3):** the GitHub preview states that Analytics is off; the itdks.tech build states Analytics with consent, as tested. The other items need the company's confirmed data, and the report says not to publish assumed values:
  - legal name and address;
  - retention periods for enquiries, client files and invoices;
  - the hosting log period;
  - each provider's role, processing location and transfer safeguard under the agreements actually signed;
  - the competent law and forum.
- **Verified:**
  - Report 11 test: 50/50. It covers the texts at start, work and result in all three languages, letter-by-letter typing, every work object, the hero steps in time, amplitudes, scene sizes at 360-1920 px with the German texts, a stable height, start order, off screen, hidden tab, a language change while typing, and reduced motion.
  - Report 10 test: 44/44, without its character section, which report 11 replaces.
  - `test09` 63/63; production with CSP 26/26, with the scenes typing under the policy.
  - axe finds 0 violations and there is no overflow. check-pages, qa-seo, M, opus and the language scan pass.

## SEO report, 23 October 2026

Source: `ITD_SEO_Raporti_Final_Ekipi_23-10-2026.pdf` (6 pages). Google Search Console and Google Business were already set up by the SEO team; the website changes are in `report_seo.py`.

- **Titles (pages 3-5):** every page's `<title>` and `og:title` in SQ/EN/DE as the report gives them. The titles have no geographic suffix, and the product names are kept. The project detail page uses its project's name ("… | Projekte nga IT Department"). The visible headings are unchanged. This applies to the main version only.
- **Google Maps (page 2):** the contact page's map button now reads "Na gjej në Google Maps" / "Find us on Google Maps" / "Finden Sie uns auf Google Maps". It opens the business profile, `share.google/EnL0Qbs1GCVTKIfoY`, which resolves to Google's "IT Department" panel.
- **Facebook (page 2):** the stable address `facebook.com/people/ITDepartment/61589358992650/` replaces the share link in every footer and in schema.org `sameAs`.
- **Waiting for the company:**
  - **Review link:** "Na vlerëso në Google" appears on the contact page and in the footer as soon as `reviewUrl` in `site.config.json` holds the direct link from Google Business → Ask for reviews. The report asks for that link, not the profile link.
  - **Projects:** the client request, the work done and the solution for each real project need the company's texts and approval in SQ/EN/DE.
- **Verified:** all 54 titles match the report; check-pages, qa-seo (preview and production), M, opus and axe (0 violations, no overflow) pass.

## Security and bug audit, 25 October 2026

Source: `itdks_security_and_bug_audit.pdf` (5 pages). Each finding was checked against the code and the live site before it was fixed.

- **BUG-01 / BUG-02 (www):** these do not reproduce live. `www.itdks.tech` answers every address, missing pages included, with a 301 to `itdks.tech` (the rule in `production.htaccess`), so no page is served on www. Both points were hardened anyway:
  - The 404 pages link their files root-relative (`/assets/…`, or `/ITD2027/assets/…` on GitHub) instead of `https://itdks.tech/…`.
  - `measurement.js` treats `www.itdks.tech` and `itdks.tech` as the same site, and nothing else.
- **BUG-03 (orbit drag):**
  - **Bug:** a drag released outside the carousel stayed active.
  - **Fix:** the stage now captures the pointer once the cards follow it. A mouse that comes back with no button pressed ends any pending drag. Touch swipes are unaffected: only the stage's own `lostpointercapture` counts.
- **BUG-04 (Calendly):** the "if the calendar does not open" warning appeared over a working calendar. Now it appears only if the calendar fails to load or answers nothing within 15 s; Calendly's own messages clear the status, and reopening shows no warning. With the production CSP, opening the calendar raised no policy report in the test.
- **BUG-05 (Creative form):** the form now offers the same six services as the cards in each language (`report_audit.py`), so a card selects its own option instead of adding a near-duplicate.
- **BUG-06 (drafts):** the draft records its language.
  - **Text** still carries over between languages.
  - **Service:** comes back only in its own language, or when the list there has the same option, so no Albanian option lands in the English form.
  - **The `[data-agent]` listener stays:** ITD2027/M still uses it.
- **BUG-07 (illustrative project page):** `noindex`, out of the sitemap (48 URLs), and its link to itself and its filter attributes are removed.
- **BUG-08 (AI Agents):** scenes off screen are no longer read; `getAnimations()` runs only for scenes on screen.
- **SEC-02:** the production build writes `/.well-known/security.txt` (RFC 9116), with contact info@itdks.tech, languages sq/en/de, the canonical URL and an expiry 360 days after the build.
- **SEC-03:** `Cross-Origin-Opener-Policy: same-origin-allow-popups` and `Cross-Origin-Resource-Policy: same-site` are in `production.htaccess`. The `platform`, `panel` and `Server` headers are added by Hostinger's edge and cannot be removed from `.htaccess`.
- **SEC-01 (DMARC):** a DNS record for the company to add in Hostinger. SPF and the Google DKIM key are already published and mail goes through Google, so `_dmarc.itdks.tech TXT "v=DMARC1; p=quarantine; rua=mailto:info@itdks.tech; adkim=r; aspf=r"` can be added. Starting with `p=none` for two weeks is the cautious option.
- **Checkers:** `scripts/check-pages.py` and `qa-seo.py` accept root-relative links only under the site's base path (from the canonical URL) and check that they resolve.
- **Verified:**
  - Audit checks 12/12 on the production build with its CSP:
    - drag released outside, and a press released outside;
    - creative options;
    - draft languages;
    - no polling off screen;
    - the www check;
    - Calendly without the warning, also when reopened;
    - `security.txt`;
    - noindex and sitemap;
    - the 404 page on a missing nested URL.
  - Report 11 50/50, Report 10 44/44, Report 09 63/63 (phone swipe and the Maps profile link), production 26/26.
  - axe finds 0 violations and there is no overflow. check-pages, qa-seo (preview and production), M and opus pass.

## Calendly link and llms.txt, developer report of 24 October 2026

Source: `ITD_Calendly_llms_SQ_EN_DE_Developer_24-10-2026.pdf` (6 pages, two notes from the user's audit screenshots).

- **Calendly fallback:** the booking dialog's link ("Hap në Calendly" / "Open in Calendly" / "In Calendly öffnen") now has the real booking address from the moment it exists, so Lighthouse no longer reports "Links are not crawlable".
  - The address comes from `bookingUrl` in `site.config.json`, through the page's `site-copy` data block.
  - It keeps that `href` while the calendar is open and after it closes.
  - Without JavaScript, the page's booking buttons are already plain links to the same page.
- **llms.txt:** every build writes `llms.txt` to the site root.
  - **Format:** `# IT Department`, a one-line summary, then `## Shqip (sq)`, `## English (en)` and `## Deutsch (de)`. Each section has 14 Markdown links to the main pages, with the page names and URLs of its own language.
  - **What it isn't:** it does not replace the sitemap, robots.txt or hreflang.
  - **Old files:** the old site's `llms.txt` on the server (plain URLs, the removed chatbot) is replaced. The old `llms-full.txt` is listed for deletion in the package.
- **Verified:** 13/13 checks.
  - On eight pages in three languages, the fallback has its `href` before any click, the report's text, and no link anywhere lacks an `href`.
  - Keyboard opening and closing work, and so does the no-JavaScript case.
  - `llms.txt` has its structure; each of the 42 links goes to a page in its section's language and already answers 200 on itdks.tech.
  - Audit checks 12/12, production 26/26, axe 0 violations, check-pages, qa-seo and M pass.

## Project pages, report of 25 October 2026

Source: `ITD_Projektet_Faqet_e_Brendshme_SEO_25-10-2026.pdf` (14 pages). Only the main version is affected; M and opus are unchanged. The work is in `report_projects.py` and `assets/projects.css`, with the routes in `proposal.py`.

- **Six projects, 18 pages:** verkaufeimmobilie.de, RATA Solar, KoBags Group, Paketoje, Optika Miftari and the new Kalkulatori, each in SQ/EN/DE.
  - **Addresses:** `/project/<slug>`, `/project/<slug>-en` and `/project/<slug>-de`. The report proposed `/projects/<slug>`, but a folder named `projects` would make the server answer `/projects` as a folder (a 301 to `/projects/`, then 403), so the detail pages live in `project/`.
  - **Folder links:** the pages in that folder link everything root-relative, including `srcset`, as the 404 pages do.
- **Template (page 3):**
  - **Hero:** the project name and short type in the centre, "Vizito website-in" to the live site (new tab), and "All projects".
  - **Story:** a large view of the website, then the introduction, goal and solution in a readable column, what it includes as four cards (one per row on phones) and the visual direction.
  - **Gallery:** two or three further views (desktop pages and the phone view, opening in the lightbox).
  - **Links and CTA:** the related service (Websites & software), three similar projects, and "Have a similar project?" with contact.
- **Texts (pages 4-13):**
  - **SQ:** in full, as given.
  - **EN/DE:** the introductions, titles and meta descriptions as given. The goal, solution, features, visual direction, card texts and labels were translated from the SQ base.
  - **Titles and meta:** set through `NEW_META`, for example "RATA Solar | Website për Energji Solare | IT Department".
  - **Demo notes:** Paketoje says its orders and payments are simulated. verkaufeimmobilie.de says the website shows a customer preview with illustrative example valuations and properties (page 14).
- **Project data (page 14):**
  - RATA Solar's address is now `https://ratasolar.com/`.
  - KoBags is described as a catalogue with quotations; the old "design studio" text is gone.
  - Kalkulatori is presented as a services website.
  - Each project's external address is kept in one field (`url`).
- **Views:** captured from the public websites on 25 October 2026 (desktop 1440 × 900, phone 390 × 844 at 2×), as WebP in `assets/projects/`. Cookie banners were closed with their "reject" choice, and the card images were replaced with the same fresh views.
- **Cards and links:** the cards on Home and Projects open the internal page in the same language ("Shiko projektin" / "View project" / "Projekt ansehen"; card and button share one URL). On wide screens the six cards sit three per row. The "Websites & software" page lists the six projects.
- **SEO:** the 18 pages answer 200 and each has its own title and meta, one H1, a self-canonical, reciprocal hreflang sq/en/de with x-default, a breadcrumb (Home → Projects → project), and an entry in the sitemap (66 URLs). The illustrative `/project-detail` stays `noindex` (no equivalent page to redirect it to).
- **Checkers:** `check-pages.py` (72 pages, base path from the home page's canonical URL) and `qa-seo.py` (72 pages, 66 sitemap URLs, rglob) cover the folder.
- **Verified:**
  - Projects test: 32/32, on the production build with the server's CSP and clean URLs. In three languages it covers the cards, Home, the service page and each of the 18 pages:
    - title and meta, H1, canonical and hreflang, the sections;
    - four features, the gallery (images load, with descriptions), the visit button;
    - language switch to the same project, similar projects, the service link, the CTA;
    - no policy violations.
  - Also the lightbox, phones at 360/390 (one card per row, no sideways scroll) and the sitemap.
  - axe finds 0 violations and there is no overflow on all 72 pages.
  - Report 09 63/63, Report 11 50/50, Report 10 44/44, audit 12/12, Calendly/llms 13/13, production 26/26. check-pages, qa-seo, M and opus pass.

## Update of 27 October 2026: Google review, KoBags domain, Paketoje phone view

Source: `ITD_Update_Google_Review_KoBags_Paketoje_27-10-2026.pdf` (3 pages). Main version only; M and opus are unchanged.

- **Google review (page 1):**
  - `reviewUrl` in `site.config.json` holds the direct link `https://g.page/r/CYds9oGJiyl6EAI/review` (not the Maps profile).
  - **Texts:** "Na vlerëso në Google" / "Leave us a Google review" / "Bewerten Sie uns auf Google".
  - **Where:** on `/contact`, `/contact-en` and `/contact-de` (between "Find us on Google Maps" and the email button, `.r8-review`), and in the shared footer of every page, under the email button (`.footer-cta.r7-review`, the same red outline).
  - **Link behaviour:** a real `a href`, `target="_blank"`, `rel="noopener noreferrer"`, a translated screen-reader note "(opens in a new tab)", no arrow, at least 52 px high.
  - **Testing:** no review was submitted while testing.
- **KoBags (page 2):** the project's `url` (and the M card) is `https://kobags-group.com/`, so the "Visit website" button opens it in all three languages. The internal `/project/kobags-group` pages and their canonicals stay. No page links to `kobags.itdks.tech` any more. The views captured on 25.10 show the same website and stay.
- **Paketoje phone view (pages 2-3):**
  - **The new capture:** `paketoje-mobile-780/-390.webp`, taken again from the live demo at 390 × 844 at 2× on 28.10.2026.
    - It is the cup slide ("Pije të ftohta…"), taken after fonts, photos and its entrance animations had finished.
    - The demo/CMS button is hidden and there is no cookie banner.
    - It is scrolled so the photo with the cup sits right under the site header, with the product card (text and button) below it. No empty green area.
  - **Display:** the gallery shows it whole with natural proportions (no crop). Its `sizes` hint now says 300 px on phones, so phones at 2× load the 780 px file.
  - **Other uses:** no card uses this image. The lightbox opens the 780 px file.
- **Verified:** on the production build with the server's CSP and clean URLs.
  - The update test passes 28/28:
    - the review button on all 72 pages and on contact, checked at 1440, 390 and 360 px in three languages (visible, at least 44 px, no sideways scroll, no policy violations);
    - KoBags in three languages;
    - Paketoje at 360, 390, 430 and 1440 px in three languages (whole, undistorted, sharp at 2×, demo note visible), plus the lightbox.
  - Earlier tests: projects 32/32, audit 12/12, Calendly/llms 13/13, production 26/26, Report 09 63/63, Report 11 50/50, Report 10 44/44.
  - axe finds 0 violations and nothing overflows on all 72 pages. check-pages (72, and M 54) and qa-seo (72 pages, 66 sitemap URLs, preview and production) pass.
- **After publishing (page 3, for the team):** check the links, images and pages on phones, and confirm the sitemap and indexing of the new pages in Search Console. Search Console was not opened here.

## Deferred, missing or not live-verified

1. **Real client case studies — user deferred to the next update.** Bring this up at the next ITD website update: request approved public client names/projects, screenshots, problem/solution and verified results. Current examples remain labelled illustrative. This is recorded in the project and as a requested context reminder, not a scheduled notification.
2. **AURA vector source — resolved 5 October 2026.** The emblem is drawn in code in the AURA web app itself (the built app in `Documents/Jaris P/tmp/aura-site-stage-*`, function `Me` and component `J`: three ribbons, radius + amplitude × sin(frequency × angle + phase), 121 points, with the pink/teal/ice gradients and glow from its CSS). `site/assets/labs/aura-emblem.svg` is a static rebuild from that code with the same parameters (no tracing), 6.5 KB; it replaces the 559 × 563 raster taken from the PDF.
3. **Production migration:** `.htaccess` is prepared, not executed on Apache. Source URL continuity and outputs are checked locally; server redirect behavior, deployed cache and live routes require the authorized deployment.
4. **Search Console / GA4:** no account settings or sitemap submission were changed. Configure key events for confirmed leads/bookings/demo requests; keep contact clicks secondary. Disable overlapping enhanced-measurement form conversions and verify DebugView/event receipt before relying on reporting. The supplied GSC data is internal evidence and is not presented as public marketing claims.
5. **Real delivery:** complete an explicitly authorized Formspree receipt test and booking-confirmation/GA4 ingestion test before claiming the providers are live-verified.
6. **Postlaunch monitoring:** no automation was created. The report’s 30–90 day monitoring begins after an actual launch, with Search Console/GA4 access and the approved baseline.

## Build and review

Run `python alternative-v2/build.py` for the GitHub/local preview. It stays noindex and analytics-disabled. `start-preview.ps1` and `stop-preview.ps1` manage only this project's registered port 8791.

Run `python alternative-v2/qa-seo.py` to validate preview and production variants. Production output is isolated under `alternative-v2/qa/production/`, so it cannot accidentally replace the GitHub publish directory. The validator sets `ITD_PRODUCTION=1`, `ITD_SITE_URL=https://itdks.tech`, `ITD_ANALYTICS=1` only for that separate build. Do not upload it over the live root without a deployment backup and verification of the existing PHP/statistics runtime.

Main implementation: `revision.py` (new content/components), `proposal.py` (generator/metadata), `site/assets/revision.css`, `site/assets/site.js`, `measurement.js`, and `booking.js`. Original component source remains in `proposal.py`. The generated site remains the GitHub Pages artifact.

External technical references: [Google URL-move guidance](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes), [GA4 recommended events](https://developers.google.com/analytics/devguides/collection/ga4/reference/events), [Calendly embed event documentation](https://developer.calendly.com/api-docs/overview/embedding/notifying-the-parent-window), [Plus Jakarta Sans source/licence](https://github.com/google/fonts/tree/main/ofl/plusjakartasans).
- Follow-up check against the PDF, 17 October 2026: the header now shows the shield beside "IT Department" in one row on every page, as in all of the report's mock-ups (desktop and phone), in each sub-brand's colour. The AI Agents section heading is centred on phones (page 16). The analytics map treats the "Kraken Assistant" form option as the same product. The orbit test passes 40/40 and the report 06 checks pass 6/6; axe finds 0 violations and there is no sideways overflow.
