import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import { localSeo, focusedServices } from "../scripts/local-seo.mjs";
const root = resolve(process.argv[2] || ".");
const origin = "https://itdks.tech";
const entities = { amp: "&", quot: '"', lt: "<", gt: ">", auml: "ä", Auml: "Ä", ouml: "ö", uuml: "ü", Uuml: "Ü", euml: "ë", ccedil: "ç", Ccedil: "Ç", szlig: "ß", rsquo: "’" };
const decode = text => text.replace(/&(#x[\da-f]+|#\d+|\w+);/gi, (raw, code) => code[0] === "#" ? String.fromCodePoint(code[1].toLowerCase() === "x" ? parseInt(code.slice(2),16) : Number(code.slice(1))) : entities[code] ?? raw);
const pages = new Map();
for (const file of await readdir(root)) {
  if (!file.endsWith(".html") || file === "404.html") continue;
  const html = await readFile(resolve(root, file), "utf8");
  const canonical = html.match(/<link rel="canonical" href="([^"]+)"/)[1];
  assert(!pages.has(canonical), `Duplicate canonical: ${canonical}`);
  const title = decode(html.match(/<title>(.*?)<\/title>/s)[1]);
  const meta = key => decode(html.match(new RegExp(`<meta (?:name|property)="${key}" content="([^"]+)"`))[1]);
  assert.equal(meta("og:title"), title, `${file}: Open Graph title mismatch`);
  assert.equal(meta("twitter:title"), title, `${file}: Twitter title mismatch`);
  assert.equal(meta("og:description"), meta("description"), `${file}: description mismatch`);
  assert.equal(meta("twitter:description"), meta("description"), `${file}: Twitter description mismatch`);
  assert.equal(meta("og:url"), canonical, `${file}: social URL mismatch`);
  const alternate = [...html.matchAll(/<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"/g)].map(m => [m[1],m[2]]);
  assert.deepEqual(alternate.map(a=>a[0]).sort(), ["de","en","sq","x-default"]);
  const graph = JSON.parse(html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s)[1])["@graph"];
  const page = graph.find(item => /Page$/.test(item["@type"]));
  assert.equal(page.url, canonical, `${file}: structured URL mismatch`);
  assert.equal(page.name, title, `${file}: structured title mismatch`);
  assert.equal(page.description, meta("description"), `${file}: structured description mismatch`);
  if (localSeo[file]) {
    assert.equal(title, localSeo[file].title);
    assert.equal(page.dateModified, localSeo[file].modified);
    assert(html.includes(localSeo[file].lead.replaceAll("&", "&amp;")), `${file}: local service introduction missing`);
  }
  pages.set(canonical, { file, html, alternate, page, graph });
}
for (const [url, page] of pages) {
  for (const [lang, target] of page.alternate) {
    assert(pages.has(target), `${page.file}: missing alternate ${target}`);
    assert.deepEqual(pages.get(target).alternate, page.alternate, `${page.file}: non-reciprocal ${lang} alternate`);
  }
  for (const match of page.html.matchAll(/href="([^"]*#[^"]+)"/g)) {
    const target = new URL(decode(match[1]), url);
    if (target.origin !== origin) continue;
    const hash = decodeURIComponent(target.hash.slice(1));
    if (!hash) continue;
    const targetPage = pages.get(`${target.origin}${target.pathname}`);
    assert(targetPage?.html.includes(`id="${hash}"`), `${page.file}: broken anchor ${match[1]}`);
  }
}
for (const locale of ["sq","en","de"]) {
  const url = `${origin}/services${locale === "sq" ? "" : `-${locale}`}`;
  const { html, graph } = pages.get(url);
  const services = graph.filter(item => item["@type"] === "Service");
  assert.equal(services.length, 7, `${locale}: expected all six focus areas plus IT audit`);
  for (const expected of focusedServices[locale]) {
    const actual = services.find(s => s.url === `${url}#${expected.id}`);
    assert(actual, `${locale}: service ${expected.id} missing`);
    const card = html.match(new RegExp(`<article[^>]+id="${expected.id}">([\\s\\S]*?)<\\/article>`))[1];
    assert.equal(decode(card.match(/<h3>(.*?)<\/h3>/s)[1]), actual.name);
    assert.equal(decode(card.match(/<h3>.*?<\/h3>\s*<p>(.*?)<\/p>/s)[1]), actual.description);
    assert.equal(actual.provider["@id"], `${origin}/#organization`);
    assert(!actual.aggregateRating && !actual.review, "Unsupported reviews");
  }
}
const sitemap = await readFile(resolve(root,"sitemap.xml"),"utf8");
const sitemapUrls = [...sitemap.matchAll(/<url>(.*?)<\/url>/gs)];
assert.equal(sitemapUrls.length, pages.size);
for (const match of sitemapUrls) {
  const url = match[1].match(/<loc>(.*?)<\/loc>/)[1];
  assert(pages.has(url), `Sitemap URL missing: ${url}`);
  assert.equal(match[1].match(/<lastmod>(.*?)<\/lastmod>/)[1], pages.get(url).page.dateModified, `${url}: lastmod mismatch`);
}
assert((await readFile(resolve(root,"robots.txt"),"utf8")).includes(`Sitemap: ${origin}/sitemap.xml`));
console.log(`seo-audit: PASS (${pages.size} canonical pages, reciprocal language links, 21 visible Service definitions, metadata and sitemap dates)`);
