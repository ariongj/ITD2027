# Google Ads Submit lead form conversion — 24 September 2026

## Installation

Public pages use one shared `analytics-config.js`, then `consent.js`, then `analytics.min.js`, in that order in the document head. `scripts/sync-site.mjs` regenerates these references and the analytics bundle. The private stats admin is excluded. No AMP pages are present. App URLs now use the first 16 hexadecimal characters of each optimized file's SHA-256; tracking cache version remains `ads2` because those bytes are unchanged. Existing consent choices are preserved.

## Conversion fix report follow-up - 24 September 2026

The supplied `ITD_Google_Ads_Conversion_Fix_Developer_Report.pdf` reports a missing successful-submit hit in Tag Assistant. A fresh public download of the live contact page, analytics configuration, analytics bundle and both app bundles matched the local success-hook implementation. The live app URLs still used `perf23` and advertised `max-age=31536000, immutable`. Reusing that URL across the earlier form-controller update can strand returning visitors on pre-hook code. This is a verified release mechanism defect and a plausible explanation of the report, not proof of the reporting browser's exact cached state.

The build now derives each desktop/mobile controller URL from its actual normalized bytes. No new conversion action, extra event callback, page-load conversion, consent bypass, CSS change or backend change was introduced. `tests/cache-audit.mjs` exercises a private fixture: stable builds keep stable URLs and changing either controller automatically changes its URL without editing a version number. The tracking audit checks the exact fingerprint on every public page.

Create the upgrade-only archive in PowerShell with `& ./scripts/package-hostinger.ps1 -TrackingPatch -ReleaseName ITD-Hostinger-Conversion-Fix-2026-09-24-r2` (use a new release name if it already exists). This patch requires the existing ITD site; it is not a fresh-install archive. It contains public HTML plus the eight form/measurement scripts only. Extract over the existing site's `public_html`, preserving every other file. It excludes all PHP, `.env*`, statistics data and server configuration. Do not delete the existing site or replace its stats configuration. Previous full archives include server-side `stats/config.php` credentials; keep those archives private. Earlier marker-only scans did not prove that they were secret-free.

Verification: 73 tracking behavior scenarios, 28 public pages, 27 canonical pages, build idempotence and desktop/mobile content-hash assertions passed locally. Live Tag Assistant receipt is still required after deployment. Test with Ad measurement consent allowed and without browser privacy signals/blockers; deliberately denied measurement must continue to produce zero conversions. Do not count local mocked responses as live delivery evidence. A valid real enquiry must produce exactly one `conversion` for `AW-18460710310/_Dj_COrP6YIdEKar4OJE`, value 1, currency USD. Do not create or change any Google Ads account action.

Exact verified patch: `ITD-Hostinger-Conversion-Fix-2026-09-24-r2.zip`, 36 files, 259,054 bytes, SHA-256 `b677c8cb65c804ed16ef06ac9c2ee85effbf256ea5fde540040fde390ad6b5fa`. Reopened with CRC32 verification, safe allowlisted paths, Unix creator metadata and 0644 permissions; every entry matched the source and staged bytes. The 73 tracking scenarios passed against the staged patch. Site/SEO audits passed on the full source tree (the patch intentionally omits unchanged assets and sitemap). Browser QA: 390px mobile and 1440px desktop each emitted one correct queued conversion after mocked success; invalid fields, HTTP failure, network failure and refresh produced zero new conversions. Failure retained entered details, successful retry reset the form and displayed success. Google and Formspree requests were blocked during local QA. Neither a real lead nor a Google conversion was sent. Deployment is pending secure Hostinger access; live Tag Assistant proof remains unverified.

- GA4: `G-B0S3HLRPWD` (existing property retained).
- Google Ads: `AW-18460710310`.
- Submit lead form action: `AW-18460710310/_Dj_COrP6YIdEKar4OJE`, replacing the previous Contact action in the supplied developer brief. The site's code sends only the new action; this release does not change Google Ads account settings or historical data.
- Value/currency: `1.0` / `USD`, exactly as supplied. This is a nominal lead value, not revenue or a charge.

## What counts

Only the contact form counts. Both existing desktop and mobile controllers call `ITDAnalytics.reportLeadSuccess("contact-form", response)` immediately after confirming `response.ok`, before the existing reset/success UI. This adapts the brief's example to the site's consent-aware analytics module; there is no redirect and no extra Google tag. A WeakSet deduplicates repeated callbacks for the same response object, including responses accepted while consent was denied. A later separate successful submission can count again with a new random transaction ID.

Package enquiries, page views, button clicks, validation failures, unsuccessful network responses, WhatsApp clicks and booking-link clicks do not count as this conversion. Changing success text/classes cannot fire a conversion. Generic GA analytics remains separate and consent-gated. Calendly completion is not instrumented. Tracking errors cannot interrupt the form's existing reset or success feedback.

No names, emails, phone numbers, enquiry text or chat messages are added to the conversion payload. Only approved click IDs are retained in the measurement page URL; arbitrary query parameters and fragments are removed. Google may still process technical data such as IP address, device and ad-click identifiers. No enhanced-conversions user-data collection or personalized advertising is enabled by this implementation; check the Google account settings separately.

## Consent

Optional measurement starts denied. The Google library is not requested until at least one option is allowed. Analytics and ad measurement are separate unchecked choices. Reject, save selected choices, and allow all are available in Albanian, English and German. The preference lasts 180 days in this browser and can be changed in the footer. Do Not Track and Global Privacy Control keep measurement disabled. Forms remain usable without measurement.

On withdrawal, consent is updated, new application events are gated, and accessible first-party measurement cookies/IDs are cleared. A Google script already loaded is not unloaded; it may process the consent update. Previously collected data is not automatically erased. This is a technical implementation, not a legal compliance certification.

## Verification and release

Run `node scripts/sync-lead-tracking.mjs`, `node scripts/sync-site.mjs`, `node tests/tracking-audit.mjs`, `node tests/site-audit.mjs` and `node tests/seo-audit.mjs` before packaging. The scoped bundle synchronizer preserves unrelated optimized code and stops if its exact patch locations change. The tracking audit executes source and optimized form controllers with mocked responses: it never contacts Formspree or Google. Browser QA also blocks Google/Formspree requests and stubs form responses locally to avoid polluting production reports.

The Hostinger ZIP contains public files at its root, including `.htaccess`, consent assets and the shared tracking configuration. It excludes `.env.local`, private statistics, tests, backups, release notes and old ZIPs. Back up the live files before replacing them in the site's `public_html`; preserve the existing server secrets and `stats/storage` data. No hosting upload or Google Ads account changes are performed by packaging.

After upload, check the live homepage and contact pages, privacy choices and form delivery. Use Google Tag Assistant to verify the IDs and consent states. Check Google Ads conversion diagnostics after a genuine consented enquiry; ad attribution additionally depends on a valid ad interaction, browser restrictions and the Ads account setup. Do not treat local test events as evidence of Google receipt.

References: [Google tag setup](https://support.google.com/google-ads/answer/7548399?hl=en), [consent mode](https://developers.google.com/tag-platform/security/guides/consent), [CSP requirements](https://developers.google.com/tag-platform/security/guides/csp).

## Earlier lead-hook package verification — historical

- Tracking audit: 73 passing behavior scenarios across source and optimized desktop/mobile files, including missing/invalid fields, HTTP/network failure, successful contact versus package submissions, rapid duplicate submits, repeated callbacks, consent refusal/withdrawal and unavailable/throwing tracking.
- Site audit: 28 public HTML pages passed. SEO audit: 27 canonical pages passed.
- Actual browser, 390px mobile and 1440px desktop: optimized files loaded with the new cache version; successful locally simulated contact responses each produced exactly one event for the new label, value 1 USD; normal reset/success UI remained intact. Missing fields and a simulated API failure produced zero conversions. A reload produced zero conversions.
- Layout CSS, consent controls, chatbot and PHP backends were not changed. No live enquiries or Ads conversions were sent during testing.
- Release target: `ITD-Hostinger-Lead-Conversion-2026-09-24.zip`. Deployment and Google's receipt/attribution remain unverified until upload and live diagnostics. Confirm the new action's Primary setting in Google Ads; the PDF describes that setting, but it has not been independently verified in the account.
- Exact archive verified: 79 files, 879,469 bytes; SHA-256 `6c4de79c24f1f07c3a4a05598279d8a613bc3f4cc023bbd9916cdc6233e7e983`. Reopened with CRC32 verification; every entry matched source and staged bytes and had 0644 permissions. The marker-only secret scan was incomplete: the archive includes server-side stats credentials and must remain private. The retired conversion label was absent. The 73 tracking scenarios and SEO audit also passed against the staged release. CSS, chatbot, consent controls, `.htaccess` and PHP backend were byte-identical to the previous release.

## Previous release evidence — historical, not the current package

- `ITD-Hostinger-Google-Ads-2026-09-20.zip`: 79 public files, 878,769 bytes.
- SHA-256: `2bab0d1fcb9c090ff6da5ad2f3b6daa0396f810fef08650736e4ddeaaa7967e3`.
- Tracking audit: 37 passing behavior scenarios against source and the exact staged release; all 28 public HTML pages use the shared ordered installation.
- Site audit: 28 public pages passed. SEO audit: 27 canonical pages passed, including the staged release.
- Browser: English/German at 320px, Albanian at 390px and English at 1440px; no horizontal overflow from consent controls; buttons at least 44px high. Reject, selected advertising-only preference, reload persistence, footer reopening, Escape/focus restoration and mobile chat opening were exercised.
- ZIP reopened with CRC verification; all 79 entries matched source and staged bytes, had 0644 permissions and passed private-file/key-marker checks. Existing desktop/mobile app bundles, site styles and chatbot remained byte-identical to the September 8 release.
- Not deployed. Actual Google receipt/attribution, live Formspree delivery and Apache/Hostinger CSP execution still require post-upload verification. Local form-response tests were mocked and no test conversions or enquiries were sent externally.
