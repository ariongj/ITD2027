// Scoped, fail-closed updates to the existing optimized app bundles.
// Preserve all unrelated minified code; a changed source pattern requires review.
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
const root = resolve(import.meta.dirname, "..");
const patches = [
  ["app-lite.min.js", 'if(!u.ok)throw new Error("submit failed");e.reset()', 'if(!u.ok)throw new Error("submit failed");if(e.id==="contact-form"){try{window.ITDAnalytics?.reportLeadSuccess("contact-form",u)}catch(trackingError){}}e.reset()'],
  ["app.min.js", 'if(!(await fetch(FORM_ENDPOINT,{method:"POST",headers:{Accept:"application/json"},body:o})).ok)throw new Error("Submit failed");form.reset()', 'const leadResponse=await fetch(FORM_ENDPOINT,{method:"POST",headers:{Accept:"application/json"},body:o});if(!leadResponse.ok)throw new Error("Submit failed");try{window.ITDAnalytics?.reportLeadSuccess("contact-form",leadResponse)}catch(trackingError){}form.reset()']
];
for (const [file, before, after] of patches) {
  const path = resolve(root, file), original = await readFile(path, "utf8");
  if (original.includes(after)) continue;
  if (original.split(before).length !== 2) throw new Error(`Expected exactly one contact success path in ${file}`);
  await writeFile(path, original.replace(before, after), "utf8");
}
// Keep public disclosures aligned with the narrower, approved conversion action.
const path = resolve(root, "scripts/sync-site.mjs");
const original = await readFile(path, "utf8");
const updated = original.replaceAll('modified: "2026-09-20"', 'modified: "2026-09-24"')
  .replaceAll("një kërkesë kontakti ose pakete", "një kërkesë nga formulari i kontaktit")
  .replaceAll("a contact or package enquiry", "an enquiry from the contact form")
  .replaceAll("eine Kontakt- oder Paketanfrage", "eine Anfrage über das Kontaktformular")
  .replaceAll("20 shtator 2026", "24 shtator 2026")
  .replaceAll("September 20, 2026", "September 24, 2026")
  .replaceAll("20. September 2026", "24. September 2026");
if (updated !== original) await writeFile(path, updated, "utf8");
console.log("Contact success hooks synchronized; unrelated optimized code preserved.");
