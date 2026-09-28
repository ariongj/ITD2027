# IT Department — local SEO and mobile polish

Release: 2026-09-08. Target: the existing PHP/static Hostinger site at https://itdks.tech.
Status: implemented and locally checked; this release has not been uploaded or live-verified.

Final archive: `ITD-Hostinger-2026-09-08.zip` — 77 files, 881,576 bytes.

SHA-256: `d4ed2c38f8d1e68174603247bd25b08eb3a5ea317e78dd012f4240b70487bbe8`.

## Search coverage

The Albanian, English and German versions now describe the same six business areas, with Prishtina and Kosovo as the local focus:

| Area | Existing public destination |
| --- | --- |
| Website design and development | `/services#websites` |
| Administration/business management systems | `/services#business-systems` |
| IT support and infrastructure | `/services#it-support` |
| Cybersecurity | `/services#cybersecurity` |
| Creative work, branding and graphic design | `/creative` and `/services#branding` |
| Digital marketing | `/creative` and `/services#marketing` |

AI, applications and IT audits remain available. No unsupported rankings, certifications, ratings, street address or guarantees were added.

Unique titles, descriptions, social previews and visible introductions were updated on the home, services, creative, about and contact pages in all three languages. Service structured data matches the rendered service descriptions. Existing canonical URLs and reciprocal language links are retained. Privacy-page structured types were corrected. Sitemap modification dates describe actual editorial changes; rerunning the generator no longer changes every date or legal-policy update date. The public www host is redirected to the existing HTTPS canonical host in `.htaccess`.

## Mobile polish

The compact design is retained. Headings use the available phone width; long German headings wrap. Service cards are wider and six short links jump directly to the relevant card. Service CTAs take two rows rather than three. Mobile buttons have clearer labels, the menu toggle and chat close control have 44px targets, and chat inputs use 16px text to avoid iOS input zoom. Opening chat does not automatically open a phone keyboard. Focus wraps within mobile chat and returns to its launcher on close. Open mobile navigation stays attached to the viewport after scrolling. CSS now loads as a regular stylesheet to prevent unstyled flashes.

## Deploy safely

1. Back up the current Hostinger `public_html` files and private configuration.
2. Upload the release ZIP and extract its contents directly inside `public_html` — `index.html` and `.htaccess` must be at that root, not in another folder.
3. Overwrite matching public website files. Preserve the existing server `.env`/environment variables, authentication files and `stats/storage` data. The archive contains no keys or visitor logs and does not configure external services.
4. Clear Hostinger/CDN cache. Verify `/`, `/services`, `/creative`, `/contact`, `/en`, `/de`, `/robots.txt`, `/sitemap.xml`, a missing URL, mobile navigation and chat on the real domain. Confirm the www host redirects without a loop.
5. Recheck real contact delivery and AI responses using the existing server configuration. PHP/provider behavior is not exercised by the local static preview.

The existing domain responded successfully during read-only checks before these edits. That does not verify the new release on Hostinger. The www redirect requires post-upload Apache/Hostinger verification. Browser checks emulate phone sizes, not a physical iOS/Android keyboard or device.

## Search visibility outside the code

No ranking or indexing result is guaranteed. Submit the existing sitemap in the domain's Google Search Console account and inspect the updated URLs after deployment. Verify the owner's Google Business Profile separately; its real address/service area, category, reviews and account verification cannot be inferred or completed from these files. No external account was changed.

References: [Google SEO guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), [accurate sitemap dates](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [local search factors](https://support.google.com/business/answer/7091?hl=en).

## Repeatable checks

`node scripts/sync-site.mjs` updates generated files; a second run should report zero changes. Editorial content and dates live in `scripts/local-seo.mjs`.

`node tests/site-audit.mjs` checks all 28 HTML files, local assets, headings and preserved contact/project flows.

`node tests/seo-audit.mjs` checks 27 public canonical pages, reciprocal translations, social metadata, 21 visible Service definitions, anchors and sitemap dates. It also accepts an extracted release folder as its first argument.

`node scripts/preview.mjs` starts the fixed local UI preview on `127.0.0.1:8787`; it can also preview an extracted release folder. PHP endpoints deliberately return an unavailable response and private paths are not served.

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/package-hostinger.ps1` runs this local packaging script in a single process and creates a new release without overwriting previous archives. It does not change the machine's execution policy. `-ReleaseName` can identify a later release.

## Verification evidence

- Static site audit: passed for 28 HTML files.
- SEO audit: passed for 27 public pages, all reciprocal SQ/EN/DE alternates, all local fragment links, matching metadata and 21 service definitions.
- Browser layout checks: all 27 public pages at 320px; all nine Albanian page types at 768px and 1440px. The German legal-heading overflow found at 320px was corrected and visually rechecked. Home, services, creative, contact/chat and menu states were visually inspected.
- Chat bounds: passed at 320×450, 390×844, 560×740, 720×740 and 1440×900. Mobile input is 16px, the transformed-parent collapse is absent, Shift+Tab wraps, Escape closes and restores focus, and the local unavailable response re-enables sending.
- Mobile menu after scrolling: reproduced the offscreen-menu problem, corrected it, and verified it stays at 6px from the viewport top with the previous scroll position retained on close. Language navigation from services to English completed.
- All six service shortcuts were exercised against the final packaged English page and reached the expected section URLs, including keyboard activation. Final mobile typography was visually rechecked.
- Archive checks: 77 public files; CRC32 validated, contents byte-for-byte matched to source, safe relative paths, 0644 file modes, no environment files, visitor logs, nested archives or private-key markers. SEO audit passed against the staged release.

External provider success, actual mobile keyboards, search indexing/rankings and the new Hostinger deployment are not covered by these local checks.
