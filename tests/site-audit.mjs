import { access, readFile, readdir, stat } from "node:fs/promises";
import { dirname, extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const entries = await readdir(root, { withFileTypes: true });
const htmlFiles = entries.filter((entry) => entry.isFile() && entry.name.endsWith(".html")).map((entry) => entry.name);
const errors = [];
const currentDate = new Date().toISOString().slice(0, 10);
const siteConfig = JSON.parse(await readFile(join(root, "site.config.json"), "utf8"));

function check(condition, message) {
  if (!condition) errors.push(message);
}

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

function attributes(tag) {
  return Object.fromEntries(
    [...tag.matchAll(/([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)]
      .slice(1)
      .map((match) => [match[1].toLowerCase(), match[2] ?? match[3] ?? match[4] ?? ""])
  );
}

for (const file of htmlFiles) {
  const path = join(root, file);
  const html = await readFile(path, "utf8");
  const h1Count = (html.match(/<h1(?:\s|>)/gi) || []).length;
  check(h1Count === 1, `${file}: expected exactly one h1, found ${h1Count}`);
  check(/<meta name="description" content="[^"]{80,}"/i.test(html), `${file}: missing or too-short meta description`);
  if (file !== "404.html") {
    check(/<link rel="canonical" href="https:\/\/itdks\.tech\//i.test(html), `${file}: missing canonical`);
  }
  check(!html.includes("info@itdepartment.al"), `${file}: contains the retired email`);
  check(!html.includes("itdepartment.al"), `${file}: contains the retired domain`);
  check(!html.includes("2026-05-17"), `${file}: contains a stale modified date`);
  check(html.includes(`styles.min.css?v=${siteConfig.assetVersion}`), `${file}: stale stylesheet version`);
  check(html.includes(`chatbot.js?v=${siteConfig.chatVersion}`), `${file}: stale chatbot version`);

  const headings = [...html.matchAll(/<h([1-6])(?:\s[^>]*)?>/gi)].map((match) => Number(match[1]));
  for (let index = 1; index < headings.length; index += 1) {
    check(headings[index] <= headings[index - 1] + 1, `${file}: heading skips h${headings[index - 1]} to h${headings[index]}`);
  }

  const ids = [...html.matchAll(/\sid="([^"]+)"/gi)].map((match) => match[1]);
  const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
  check(duplicateIds.length === 0, `${file}: duplicate ids ${[...new Set(duplicateIds)].join(", ")}`);

  for (const image of html.match(/<img\b[^>]*>/gi) || []) {
    const attrs = attributes(image);
    check(Object.hasOwn(attrs, "alt"), `${file}: image without alt`);
    check(Boolean(attrs.width) && Boolean(attrs.height), `${file}: image without dimensions (${attrs.src || "unknown"})`);
  }

  for (const link of html.match(/<a\b[^>]*target="_blank"[^>]*>/gi) || []) {
    const attrs = attributes(link);
    check(/\bnoopener\b/.test(attrs.rel || ""), `${file}: target=_blank link missing noopener`);
  }

  for (const script of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try {
      const parsed = JSON.parse(script[1]);
      const encoded = JSON.stringify(parsed);
      check(!encoded.includes('"dateModified":"2026-05-17"'), `${file}: stale JSON-LD date`);
    } catch {
      errors.push(`${file}: invalid JSON-LD`);
    }
  }

  for (const reference of html.matchAll(/\s(?:href|src)="([^"]+)"/gi)) {
    const raw = reference[1];
    if (/^(?:https?:|mailto:|tel:|data:|javascript:|#)/i.test(raw)) continue;
    const clean = raw.split(/[?#]/)[0];
    if (!clean) continue;
    let relative = clean.replace(/^\/+/, "");
    if (relative === "") relative = "index.html";
    else if (relative === "en") relative = "index-en.html";
    else if (relative === "de") relative = "index-de.html";
    const direct = join(root, relative);
    let resolved = await exists(direct);
    if (!resolved && !extname(relative)) resolved = await exists(`${direct}.html`);
    check(resolved, `${file}: broken local reference ${raw}`);
  }

  if (/^contact(?:-en|-de)?\.html$/.test(file)) {
    check(/<body class="contact-page">/.test(html), `${file}: compact contact layout class missing`);
    check(/href="mailto:info@itdks\.tech"/.test(html), `${file}: direct email action missing`);
    const schedulePosition = html.indexOf('class="section contact-scheduling-section"');
    const writtenRequestPosition = html.indexOf('class="section contact-details-section"');
    const scheduleSection = html.match(/<section class="section contact-scheduling-section"[\s\S]*?<\/section>/)?.[0] || "";
    const writtenRequestSection = html.match(/<section class="section contact-details-section"[\s\S]*?<\/section>/)?.[0] || "";
    check(schedulePosition > 0 && writtenRequestPosition > schedulePosition, `${file}: scheduling is not separated before the written request`);
    check(/id="booking-call"/.test(scheduleSection) && /data-booking-link/.test(scheduleSection), `${file}: dedicated scheduling action missing`);
    check(!/data-booking-link/.test(writtenRequestSection), `${file}: booking action is mixed into the written request`);
  }
  if (/^projects(?:-en|-de)?\.html$/.test(file)) {
    const casePosition = html.indexOf('id="case-examples"');
    const statsPosition = html.indexOf('class="container grid-4 trust-grid"');
    check(casePosition > 0 && statsPosition > casePosition, `${file}: project examples are not positioned before stats`);
  }
}

const sitemap = await readFile(join(root, "sitemap.xml"), "utf8");
for (const match of sitemap.matchAll(/<lastmod>([^<]+)<\/lastmod>/g)) {
  check(/^\d{4}-\d{2}-\d{2}$/.test(match[1]) && match[1] <= currentDate, "sitemap.xml: invalid or future lastmod date");
}

const appSourceSize = (await stat(join(root, "app.js"))).size;
const appMinSize = (await stat(join(root, "app.min.js"))).size;
const liteSourceSize = (await stat(join(root, "app-lite.js"))).size;
const liteMinSize = (await stat(join(root, "app-lite.min.js"))).size;
const cssSourceSize = (await stat(join(root, "styles.css"))).size;
const cssMinSize = (await stat(join(root, "styles.min.css"))).size;
check(appMinSize < appSourceSize, "app.min.js is not smaller than its source");
check(liteMinSize < liteSourceSize, "app-lite.min.js is not smaller than its source");
check(cssMinSize < cssSourceSize, "styles.min.css is not smaller than its source");

if (errors.length) {
  console.error(`site-audit: FAIL (${errors.length})`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`site-audit: PASS (${htmlFiles.length} HTML files, links/assets/SEO/a11y checks clean)`);
