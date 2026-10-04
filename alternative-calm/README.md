# itdks.tech — "calm" version

A rebuilt version of the IT Department website: same pages, same URLs, same
languages (SQ default, EN, DE), same integrations (Formspree, Calendly,
WhatsApp, Kraken chat, consent + analytics), but a much lighter, calmer
design and a fraction of the code. Since 3 October 2026 it also has the
**ITD Labs** product section (Kraken OS, Kraken Communications, AURA) that the
October design and SEO reports ask for; see "ITD Labs" below.

A side-by-side with the current site is in `build/screens/compare-home-en.png`.

## What changed

| | Current site | This version |
|---|---|---|
| Look | Dark, red glow, animated frames on every card, 3D background | Light, warm off-white, black + one red accent; dark when the visitor's device is dark (toggle in the header) |
| Home page | 7 dense sections, package quiz, inline package form, 21 buttons | 6 sections: hero, services, process, numbers, packages, contact; 8 buttons |
| Motion | 35 animated elements, many looping | 9, play once and stop; off entirely with "reduce motion" |
| CSS + JS (home, uncompressed) | 465 KB, incl. 163 KB three.js from a CDN | 82 KB, no libraries |
| Fonts | Manrope/Sora named in CSS but never loaded | Instrument Sans, 30 KB, self-hosted (no Google Fonts request) |
| Packages | Select → inline form on the home page | "Ask about Business" → contact page with the package prefilled |
| Phones | Cards and prices in sideways-swipe rows | Everything stacked; language switch inside the menu |
| Share images | One dark image | One light image per language (`og-image*.png`) |
| Speed, simulated slow phone | Main content after 2.7 s, 331 KB | Main content after 1.2 s, 159 KB |
| Accessibility | — | axe-core: 0 violations on every page type, light and dark |
| Keyboard | — | Visible focus ring on every link, button and field; the phone menu keeps focus inside it |
| Forms | Formspree | Same endpoint and field names, plus a spam honeypot, messages in the page's language, error fields announced to screen readers, and a working fallback if JavaScript fails |
| Chat | Kraken assistant, button bottom left | Same assistant; button bottom right, clear of the text, icon only on phones |
| Products | Not on the site | ITD Labs page, a page each for Kraken OS and Kraken Communications, AURA as a preview; "Request a demo" opens the contact form with the product filled in |

## Kept from the current site on purpose

- **Search:** every page keeps its current `<title>` and meta description, so
  what Google has indexed does not change. The home headline still names
  Prishtina, Kosovo.
- **URLs:** all 27 page addresses are unchanged, including /en and /de. The
  ITD Labs section adds 9 new ones (listed below); nothing was renamed.
- **Legal pages:** the privacy and terms text is word for word the current
  site's, in all three languages, including the "Updated on" dates.
- **Deep links:** the section anchors used by the current site still exist
  (for example `#ai-agent-brief`, `#creative-showcase`, `#booking-call`,
  `#choose-package`). `build/check.py` fails if one goes missing.
- **Old package links:** links like `/?package=Business&price=299…` from the
  current site forward to the contact form with that package filled in.
- **Measurement:** `consent.js`, `analytics-config.js` and `analytics.min.js`
  are the original files, and the contact-form conversion still fires through
  `ITDAnalytics.reportLeadSuccess`.

## ITD Labs

Added on 3 October 2026, following "Raporti i Ndryshimeve 01" (ITD Labs: Kraken
OS → Kraken Communications → AURA, AURA without a link) and the SEO report of
2 October (a page per product with a demo request, products kept apart from
client projects). The look stays this version's own; only the product pages
carry a hint of their product's colour (Kraken blue, AURA violet).

| Page | Albanian | English | German |
|---|---|---|---|
| ITD Labs (all products) | /itd-labs | /itd-labs-en | /itd-labs-de |
| Kraken OS | /krakenos | /krakenos-en | /krakenos-de |
| Kraken Communications | /kraken-communications | /kraken-communications-en | /kraken-communications-de |

The page names match the ones the ITD2027 proposal uses at the time of writing
(`itd-labs`, `krakenos`, `kraken-communications`), so either version can go
live without changing links. "ITD Labs" is in the main menu (the
product pages highlight it) and in the footer.

- **Where the words come from.** Kraken OS: the official presentation
  (`KRAKEN-OS-Prezantimi-Zyrtar_v2`), page 1 (what it is, the three layers,
  "start with a few modules") and page 29 (the client-to-report flow, the eight
  implementation steps, "licence, configuration and AI services are set out in
  the offer"). Kraken Communications: the slide headlines of
  `Kraken-Communications-SQ-v4`. ITD Labs and AURA: the design report. Prices,
  the credits offer, the Viber add-on and client or demo names were left out
  on purpose.
- **Images** (`assets/labs/`, WebP, two sizes each so phones load the small
  one): the Kraken OS dashboard and the Communications overview from the
  report's product visuals, and the AURA emblem. They show demo data. The
  server caches images for a year, so give a replaced image a new file name.
- **Request a demo.** Every product page links to
  `/contact?product=krakenos` (or `kraken-communications`, `itd-labs`). The
  form then shows "Demo request: Kraken OS", selects "ITD Labs product demo"
  and sends the product in an extra field, `produkti`. Unknown values are
  ignored, and old `?package=` links still work as before.
- **Measurement.** A delivered demo request also sends `request_demo` (with
  consent, no form values), next to the existing lead conversion. Clicks on
  WhatsApp, phone, email and Calendly were already measured by the original
  `analytics.min.js` as `whatsapp_click`, `phone_click`, `email_click` and
  `booking_click`; those names were kept so existing GA4 reports keep working.
  In GA4, mark `request_demo` as a key event.
- **Try the chat.** The chat on this site runs on Kraken, so the Kraken
  Communications page has an "Open the chat" button. It only appears once the
  chat button has loaded.
- **Menu.** With six items the menu needs about 1,090 px, so below 1,100 px it
  folds into the Menu button (a side panel on tablets). Checked from 320 px to
  1,440 px in all three languages: no wrapping, no sideways scrolling.

## Folder layout

```
index.html, index-en.html, index-de.html   home pages (generated)
services*.html, ai-agents*.html, ...       inner pages (generated)
404.html, sitemap.xml                      generated
css/site.css                               the only stylesheet
js/site.js                                 nav, theme, forms, lightbox, prefill
assets/brand, assets/creative, assets/partners, assets/fonts, assets/labs (product images)
build/                                     source + tools (not deployed, blocked by .htaccess)
  content_sq.py / content_en.py / content_de.py   all copy, per language
  templates.py                             HTML for every page
  build.py                                 writes the HTML files and sitemap
  check.py                                 link / anchor / placeholder / markup QA
  og.py                                    regenerates the share images (needs Chrome or Edge)
  serve.py                                 local preview with clean URLs
  pages.py                                 preview copy for GitHub Pages (see "On GitHub")
  screens/                                 comparison screenshot
stats/, chat.php, consent.*, analytics*    unchanged from the current site
```

## Editing text

### In Excel (easiest)

All 881 pieces of text are in `build/texts.xlsx`: one row each, with English,
Albanian and German side by side, grouped by page (ITD Labs, Kraken OS and
Kraken Communications have their own groups).

1. Refresh the workbook so it matches the site:
   `py -X utf8 build/texts.py export`
   (add `--compare <folder with the current site's files>` to get
   "Albanian new?" / "German new?" columns for a translation review).
2. Edit the English, Albanian or German cells in Excel and save as .xlsx.
   Leave the Key column alone; it tells the import where each text belongs.
   Keep placeholders such as `{plan}`, `{price}` or `{link}` in the text.
   An empty cell is ignored, it never deletes text.
3. Apply and rebuild:

```powershell
py -X utf8 build/texts.py import --dry
py -X utf8 build/texts.py import
py -X utf8 build/build.py
py -X utf8 build/check.py
```

`--dry` lists what would change without writing anything. Edits that remove a
placeholder are refused and listed.

### In the source files

All copy lives in `build/content_<lang>.py`. Change the text, then rebuild:

```powershell
py -X utf8 build/build.py
py -X utf8 build/check.py
```

If you change the home-page headline, also run `py -X utf8 build/og.py` so the
share images match. Never edit the generated `*.html` files by hand; the next
build overwrites them.

## Preview locally

```powershell
py -X utf8 build/serve.py 8765
```

Then open http://localhost:8765/ (SQ), /en, /de. The server maps clean URLs
the same way `.htaccess` does on Hostinger.

To look at it on real phones, connect them to the same Wi-Fi and run:

```powershell
py -X utf8 build/serve.py 8765 --lan
```

It prints an address like `http://192.168.0.101:8765` to open on the phone.
Windows may ask to allow Python through the firewall; allow it for private
networks. Anyone on that Wi-Fi can open the preview while it runs, so stop it
with Ctrl+C afterwards.

To preview with the same security headers the live server sends (from
`.htaccess`), add `--prod-headers`. Every page was checked this way: nothing is
blocked by the Content-Security-Policy, including the chat window.

## On GitHub

This folder is also kept in the ITD2027 repository
(https://github.com/ariongj/ITD2027) as `alternative-calm/`, and GitHub Pages
shows it at https://ariongj.github.io/ITD2027/calm/. The ITD2027 proposal stays
at https://ariongj.github.io/ITD2027/.

- The preview is made by `build/pages.py`: relative links (GitHub Pages serves
  the site from a sub-folder), `noindex`, and no consent or analytics scripts,
  so preview visits never reach GA4 or Google Ads. Forms and the chat work as
  on the live site: a form sent from the preview reaches the real inbox.
- The Pages workflow rebuilds this folder, runs `build/check.py`, makes the
  preview and checks every link in it before publishing.
- `stats/` is not in the repository, because the local copy holds the
  analytics secret. The repository root has the same files with the secret
  removed. `.claude/` is left out too.
- To update the preview, copy this folder over `alternative-calm/` in a clone
  of the repository (again without `stats/` and `.claude/`), commit, and push
  to `main`.

## Deploy

Same as before: `deploy-hostinger.cmd` (see `DEPLOY.md`). The `build/` folder,
`.claude/`, `README.md` and `.env*` files are excluded from upload.

Remember to place `.env` with `OPENAI_API_KEY` on the server if `chat.php`
is still in use; it is not part of this folder.

## Going live checklist

1. **Keep a backup of the current site.** The `_public_html (2).zip` this
   version was built from is a full copy of the current files. Keep it; if
   anything goes wrong, uploading those files again restores the old site.
2. **Rebuild and check:** `py -X utf8 build/build.py` then
   `py -X utf8 build/check.py` must say "No problems found."
3. **See what will upload:** `.\deploy-hostinger.cmd -DryRun` (88 files at
   the time of writing; `build/`, `README.md`, `.claude/` and `.env*` are
   left out).
4. **Upload:** `.\deploy-hostinger.cmd` as described in `DEPLOY.md`.
5. **Test on the live site** in a private window, on a computer and a phone:
   - `/`, `/en`, `/de` load, the language switch and the phone menu work;
   - send one real enquiry from `/contact-en` and confirm the email arrives;
   - "Ask about Business" on the home page opens the contact form with the
     package filled in;
   - "Book a 30-min call" opens Calendly, WhatsApp buttons open WhatsApp;
   - the chat button opens the assistant;
   - `/itd-labs` shows the three products; "Request a demo" on `/krakenos`
     opens the contact form with Kraken OS filled in; "Open the chat" on
     `/kraken-communications` opens the assistant;
   - "Privacy settings" in the footer reopens the consent choices;
   - a wrong address such as `/xyz` shows the 404 page.
6. **Search Console:** submit `https://itdks.tech/sitemap.xml` again and
   watch the Pages report for new 404 errors for two weeks. Page addresses,
   titles and descriptions did not change, so rankings should not move.
7. **Optional clean-up, a week later:** the upload does not delete files the
   new site no longer uses. They are harmless, but can be removed in the
   Hostinger File Manager: `styles.css`, `styles.min.css`, `app.js`,
   `app.min.js`, `app-lite.js`, `app-lite.min.js`, and the
   `logo-lockup-*.png` / `.webp` files.

## Things to review before going live

- Albanian and German wording of the *new* sentences. In `build/texts.xlsx`,
  filter "Albanian new?" or "German new?" to "yes": those are the sentences
  written for this version; everything else is word for word from the current
  site. The reviewer can correct them right there and you import the file as
  described under "Editing text". (`build/translation-review.csv` is the same
  list as a plain CSV.) `build/translation-review-notes.csv` logs the corrections an automated
  language review already applied, and the suggestions it left for a person.
  Regenerate the sheet after edits with
  `py -X utf8 build/review_sheet.py <folder with the current site's files>`.
- The numbers (140+ projects, 40+ clients, 12+ platforms, 96% satisfaction,
  8 sectors) are copied from the current site; confirm they are still right.
- Form confirmation messages now use the current site's wording. No reply-time
  promise was added; add one only if the team can keep it.
- ITD Labs: confirm the product catalogue (the SEO report says it still needs
  confirming), that AURA should appear as a preview without a link, and the
  module list on the Kraken OS page (taken from the presentation, which says
  availability depends on each implementation; the page says so too).
- The new ITD Labs texts went through the same automated language review
  (German: 18 changes, Albanian: 11 applied, 1 kept). Each decision is in
  `build/translation-review-notes.csv` under "ITD Labs". They still need a
  person's read like the rest.
- From the SEO report: the projects page still uses the current site's
  anonymous examples. The report asks for real, publishable projects
  (problem, screenshots, result) and for any illustrative example to be
  labelled as one. That needs material only the team has.
- From the SEO report: Search Console lists `/teams/`, which is not part of
  this site. Check on the server what it is before going live. If it is a
  folder that should stay, keep it (the upload does not delete it). If it is
  gone, point it to the closest page with a 301, not to the home page. Old
  `.html` addresses such as `/index-en.html` and `/creative.html` already
  redirect to their clean addresses through `.htaccess`.
