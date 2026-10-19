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
