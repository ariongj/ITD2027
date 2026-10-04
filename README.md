# IT Department — ITD2027

Source repository for the IT Department website and the starting point for its 2027 edition.

## Start here

The newer design is in alternative-v2/site/: 39 static HTML pages in Albanian, English and German, with the original branding and shared assets. Its editable generator is alternative-v2/build.py plus alternative-v2/proposal.py; shared CSS and JavaScript live in alternative-v2/site/assets/.

The existing website remains at the repository root because the newer design's generator reads its content, images and public site.config.json. Keep this layout when rebuilding.

    python alternative-v2/build.py
    node alternative-v2/preview.mjs

Open http://127.0.0.1:8790/ for the newer design. Use Python 3 and Node.js. The static preview uses no application database. It does not execute the older site's PHP endpoints.

A second, calmer alternative is in alternative-calm/: the complete site as ready-to-upload files (36 pages and a 404 page in Albanian, English and German, including the ITD Labs pages for Kraken OS, Kraken Communications and AURA), with its generator in alternative-calm/build/. It does not depend on the files above and needs only Python 3:

    python alternative-calm/build/build.py
    python alternative-calm/build/check.py
    python alternative-calm/build/serve.py 8765

alternative-calm/README.md describes it. Its stats/ folder is not in the repository because the original copy holds the analytics secret; the root stats/ folder is the same code with the secret removed.

## Scope and status

This import provides the existing site and newer design as the base for 2027 work. It does not implement a further redesign, change existing dates or commercial claims, deploy hosting, or alter itdks.tech. The newer proposal remains marked noindex. Read alternative-v2/README.md for its design context and prior local verification; referenced private histories, PDF materials and QA screenshots are retained only in the original workspace.

The older root site requires a PHP-capable server for chat and analytics. The newer static proposal uses the existing public Formspree endpoint for enquiries; do not submit test messages without authorization. Production deployment, real form delivery and design acceptance are separate from this GitHub upload.

## Configuration and privacy

Local .env files, analytics visitor records, private source PDFs, old releases, backups and generated QA files are excluded. No API keys or existing analytics credentials belong in Git.

In this repository copy, the older analytics backend reads ITD_STATS_ADMIN_KEY and ITD_STATS_SECRET from the PHP server environment. Set fresh independent random values there before using it. When either value is absent, the analytics endpoints return HTTP 503 with configuration_required. A local .env file alone does not configure these PHP constants.

The chat endpoint uses its existing server-side OpenAI configuration; no credentials are provisioned by this import. The existing Hostinger scripts and deployment notes describe the older live site and must not be treated as an instruction to deploy the 2027 proposal.

## Checks

    node tests/site-audit.mjs
    node tests/seo-audit.mjs
    node tests/tracking-audit.mjs
    node tests/cache-audit.mjs

These cover the older source site. The alternative-v2/qa-proposal*.mjs scripts cover the newer proposal and include intercepted form tests. Their Playwright import currently points to the original Windows runtime; configure that path and create alternative-v2/qa/proposal/ before running them on another machine.

## Verification of this import

- The newer proposal regenerated all 39 pages from this repository.
- Its 1,833 local page, asset and anchor references resolve.
- JavaScript syntax checks passed for its controller and preview server.
- Existing root-site SEO checks passed for 27 canonical pages.
- Existing tracking checks passed 73 scenarios across 28 pages, without external requests.
- The cache-invalidation regression check passed.
- The existing general site audit fails on 27 root pages: site.config.json expects chatbot version bot5, while the supplied HTML uses kraken-20260925. The original folder has the same mismatch. This import preserves those source files.
- The 185 unchanged source files match the original folder byte-for-byte. The only modified supplied files are .gitignore and stats/config.php, for publication exclusions and removal of embedded credentials.
- Exact original secret values and common credential patterns were checked against the publication copy, with no matches.
- PHP runtime behavior, browser workflows and external providers were not newly exercised for this source import. Earlier browser results in alternative-v2/README.md remain historical evidence.

## GitHub Pages hosting

The publishing workflow in .github/workflows/pages.yml builds the newer design and the calm alternative and uploads only their static pages. Successful pushes to main publish automatically at:

https://ariongj.github.io/ITD2027/ (newer design)
https://ariongj.github.io/ITD2027/calm/ (calm alternative)

The workflow validates all 39 HTML pages and their local links and CSS assets before publishing. For the calm alternative, alternative-calm/build/pages.py makes a sub-folder copy with relative links, noindex and no analytics scripts, then checks its 37 pages and every local link and anchor the same way. The source files, legacy PHP endpoints and operational configuration are not part of the Pages website.

The newer design retains its preview noindex setting. The itdks.tech domain and its existing hosting are unchanged. Forms retain the existing Formspree connection; actual inbox delivery requires a separately authorized submission test.

Check the repository's Actions tab for each deployment result. Revert an unwanted source commit and push main to publish the prior version again.
