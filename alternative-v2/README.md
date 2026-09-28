# IT Department — supplied design proposal applied

Local preview: http://127.0.0.1:8790/

Version: 27 September 2026. Implemented and locally verified; not deployed to itdks.tech. User acceptance and production verification remain separate.

## Design source and implementation

The source is the complete 33-page IT_Department_Propozim_i_Plote_i_Dizajnit.pdf supplied by Arion. All pages were extracted and visually reviewed. Its nine-page architecture, light main-page system, Sora/Manrope typography, restrained red/black banner, distinct Creative and AI palettes, partner rows, product imagery and mobile composition are implemented.

The nine primary pages are Home, Services, Projects, Partners, Creative, AI Agents, About, Contact and KrakenOS. Albanian, English and German are available throughout. An illustrative project detail, privacy, terms and 404 complete the 39 generated HTML pages.

Original source content remains available: eight detailed services, all three IT package prices and inclusions, six creative offerings, six AI agents and their tasks, four original illustrative cases, two concept brandbooks and twelve FAQs. Nine platform profiles explain the relevant technology without asserting unverified official partnership status. KrakenOS uses the supplied product-presentation images and links demo requests to the contact form.

## Brand preservation

The three IT Department logo variants are exact byte copies of the supplied originals. The original main logo appears on the main pages; the Creative and AI variants appear in both the header and footer of their respective pages. No logo was redrawn, recolored or replaced.

The nine original platform SVG files are also retained. Their neutral display color and transparent canvas are handled in CSS; their source geometry is unchanged. The brand texture and KrakenOS images were extracted directly from the supplied PDF. The NEXUS and HYPERLINK assets remain identified as concepts.

## Authoritative files

- build.py: original content extraction, source helpers and build entry point.
- proposal.py: proposal components, page assembly and SQ/EN/DE copy.
- site/assets/site.css: shared design system and responsive rules.
- site/assets/site.js: navigation, filters, disclosures, image viewer and enquiry forms.
- site/: generated static website and its self-contained assets.
- site/assets/fonts/: Sora and Manrope fonts with OFL licenses.
- preview.mjs: loopback-only preview on the fixed project port 8790.
- start-preview.ps1 / stop-preview.ps1: start or stop only this preview.

Run build.py with Python 3. The builder uses only the standard library and reads the parent website plus its public site.config.json. Node runs the preview server. No application database or new dependency installation is required.

The previous white studio direction is preserved in history/studio-direction-20260927. Earlier iterations remain in history. The initial source-manifest.json is retained; proposal-source-manifest.json records the source immediately before this implementation. The old manifest's unrelated chat.php change is not reverted. The current proposal-source comparison shows no original-root file changes during this work.

## Contact behavior

The Contact, Creative and AI forms submit to the existing public Formspree endpoint configured by the original website. Required fields, whitespace validation, email validation, pending feedback, duplicate prevention, a 20-second timeout, success confirmation, failure recovery and retry are implemented. Success is shown only after an HTTP success and an explicit provider JSON response with ok=true.

Drafts stay in sessionStorage for the current browser tab, survive refresh/language changes, and are removed after a confirmed successful submission. Errors preserve the entered text. Email and WhatsApp remain available as alternative contact routes. Calendly is the existing meeting-booking link.

All 21 submission requests in automated QA were intercepted locally. No test message was sent to Formspree, email or WhatsApp. Actual provider acceptance and inbox delivery remain unverified. Production deployment and a real authorized delivery test are separate steps.

## Verification evidence

| Acceptance item | Status | Evidence |
| --- | --- | --- |
| Nine proposal pages in all three languages | verified | 39 generated routes including supporting pages; qa/proposal/route-report.json |
| Original three ITD logos | verified | SHA-256 equality with supplied PNG files |
| Root website preserved during this implementation | verified | No differences against proposal-source-manifest.json |
| Desktop, tablet, standard and small phone widths | verified | 156 layout checks at 1440, 768, 390 and 320 px; zero horizontal overflow |
| Desktop navigation near breakpoints | verified | SQ/EN/DE at 1121, 1180, 1280 and 1366 px; qa/proposal/breakpoint-report.json |
| Local links, assets and anchors | verified | All collected local targets resolve; no missing images |
| Filters and service disclosures | verified | All service/project/portfolio/FAQ filters and eight service details exercised |
| Platform profiles and AI agent selection | verified | Nine profiles and six agents exercised in all languages |
| Mobile menu and language switching | verified | All nine navigation destinations; Escape and draft continuity exercised |
| Image viewer accessibility | verified | Open, Escape, keyboard focus containment, scroll lock and focus restoration |
| Enquiry UX and recovery | verified locally | Required/whitespace/email validation, pending/duplicate protection, preserved drafts, retry, network error, malformed and unconfirmed responses |
| Reduced motion | verified | Transitions and smooth scrolling disabled under the reduced-motion preference |
| Preview privacy and route protection | verified | No external page-load requests; noindex, robots disallow, 404 and private-file denial |
| Visual review | verified | Desktop and mobile screenshots for all nine pages in qa/proposal |
| Real provider delivery | unverified | No external submission sent |
| Production deployment | not performed | Local preview only |
| User design acceptance | pending | Requires Arion's review of this applied version |

The interaction report records 308 passing assertions and no JavaScript errors. Reproduction scripts are qa-proposal.mjs, qa-proposal-interactions.mjs, qa-proposal-breakpoints.mjs and qa-proposal-visual.mjs. They use the bundled Playwright package and installed Chrome; paths reflect this Windows workspace. Form tests always intercept the provider endpoint.

The asset and generated-file hashes are saved in qa/proposal/site-manifest.json. Screenshots correspond to the final applied design. The PDF renderings and extracted text are kept privately in reference/proposal and are not served by the preview.

## Publication boundaries

The PDF identifies the existing 140+ projects, 40+ clients and package prices as requiring confirmation before publication. These source-provided values are retained in this local preview; no new metrics or client claims were added. Illustrative cases remain labeled. Platform listings do not claim certifications or official partner status. KrakenOS imagery presents the product; it does not establish current production readiness of any module.

This work applies the website design. It does not create a Figma account/file, deploy the website, alter the live site's analytics/chat systems, activate an AI provider, complete a Calendly booking or send communications. Production SEO canonicals, sitemap/domain configuration, tracking consent and live submission receipt should be verified as part of an explicitly scoped publication.
