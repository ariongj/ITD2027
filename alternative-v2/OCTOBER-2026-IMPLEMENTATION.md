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
