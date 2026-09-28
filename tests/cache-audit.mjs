// Regression test for the missing-conversion release failure: changed form
// controllers must never keep the same immutable browser URL.
import assert from "node:assert/strict";
import { mkdtemp, copyFile, mkdir, readFile, writeFile, rm } from "node:fs/promises";
import { resolve, join } from "node:path";
import { tmpdir } from "node:os";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";

const root = resolve(".");
const fixture = await mkdtemp(join(tmpdir(), "itd-cache-audit-"));
const files = ["site.config.json", "contact-en.html", "sitemap.xml", "styles.css", "styles.min.css", "analytics.js", "app.js", "app-lite.js", "app.min.js", "app-lite.min.js", "scripts/sync-site.mjs", "scripts/local-seo.mjs"];
try {
  await mkdir(join(fixture, "scripts"));
  for (const file of files) await copyFile(join(root, file), join(fixture, file));
  const build = () => execFileSync(process.execPath, [join(fixture, "scripts/sync-site.mjs")]);
  const page = () => readFile(join(fixture, "contact-en.html"), "utf8");
  const version = (html, name) => html.match(new RegExp(name.replaceAll(".", "\\.") + '\\?v=([^"\\s]+)'))?.[1];
  build();
  const first = await page();
  build();
  assert.equal(await page(), first, "Identical builds must preserve asset URLs");
  for (const name of ["app.min.js", "app-lite.min.js"]) {
    const before = await page();
    const changed = (await readFile(join(fixture, name), "utf8")) + "\n/* isolated cache regression fixture */\n";
    await writeFile(join(fixture, name), changed);
    build();
    const after = await page();
    assert.notEqual(version(after, name), version(before, name), `${name}: changed bytes must change URL without a manual version bump`);
    assert.equal(version(after, name), createHash("sha256").update(changed).digest("hex").slice(0, 16));
  }
  console.log("cache-audit: PASS (stable rebuild and automatic desktop/mobile cache invalidation)");
} finally {
  // mkdtemp returned this exact test-owned path; never remove the workspace.
  assert(fixture.startsWith(join(tmpdir(), "itd-cache-audit-")) && fixture !== root);
  await rm(fixture, { recursive: true, force: true });
}
