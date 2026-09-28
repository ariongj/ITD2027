// Isolated runtime tests. No requests are sent to Google, Formspree or the live site.
import assert from "node:assert/strict";
import vm from "node:vm";
import { readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import { createHash } from "node:crypto";

const root = resolve(process.argv[2] || ".");
const source = Object.fromEntries(await Promise.all(["analytics-config.js", "consent.js", "analytics.js", "analytics.min.js", "app-lite.js", "app.js", "app-lite.min.js", "app.min.js"].map(async name => [name, await readFile(resolve(root, name), "utf8")])));
const preferenceKey = "itd_measurement_consent_v1";
const adsDestination = "AW-18460710310/_Dj_COrP6YIdEKar4OJE";
const flush = async () => { for (let i = 0; i < 5; i++) await new Promise(setImmediate); };

function harness({ saved, dnt, gpc, lang = "en", pathname = "/contact-en", bundle = "analytics.js", storageBlocked = false } = {}) {
  const scripts = [], beacons = [], elements = [], observers = new Map();
  const eventTarget = object => Object.assign(object, { events: {}, addEventListener(name, fn) { (this.events[name] ||= []).push(fn); }, dispatchEvent(event) { for (const fn of this.events[event.type] || []) fn(event); } });
  function node(id = "") {
    let classes = "", content = "";
    const children = new Map();
    const change = () => { if (observers.has(result)) queueMicrotask(observers.get(result)); };
    const result = eventTarget({ id, dataset: {}, tagName: "DIV", hidden: false, checked: false, disabled: false,
      setAttribute(name, value) { this[name] = value; }, removeAttribute(name) { delete this[name]; },
      getAttribute(name) { return this[name] || ""; }, hasAttribute(name) { return name in this; },
      appendChild(child) { elements.push(child); }, focus() { doc.activeElement = this; },
      querySelector(selector) { if (!children.has(selector)) children.set(selector, node(selector)); return children.get(selector); },
      get className() { return classes; }, set className(value) { classes = value; change(); },
      get textContent() { return content; }, set textContent(value) { content = value; change(); }
    });
    result.classList = { contains: value => classes.split(" ").includes(value), add(value) { result.className = classes + " " + value; }, remove(value) { result.className = classes.split(" ").filter(c => c !== value).join(" "); } };
    return result;
  }
  const storage = data => ({ data: new Map(data), getItem(key) { if (storageBlocked) throw Error("blocked"); return this.data.get(key) ?? null; }, setItem(key, value) { if (storageBlocked) throw Error("blocked"); this.data.set(key, value); }, removeItem(key) { if (storageBlocked) throw Error("blocked"); this.data.delete(key); } });
  const localStorage = storage(saved ? [[preferenceKey, JSON.stringify(saved)]] : []), sessionStorage = storage([]);
  const statuses = [node("form-status"), node("package-form-status"), node("other-status")];
  const forms = [node("contact-form"), node("package-form")];
  forms.forEach(form => {
    form.fields = { emri: "QA Test", email: "test@example.invalid", kompania: "Test", sherbimi: "Web", paketa: "Web", telefoni: "000000000" };
    form.reset = () => { form.resetCount = (form.resetCount || 0) + 1; };
  });
  const footer = node("footer"), body = node("body");
  const doc = eventTarget({ readyState: "complete", title: "Contact", cookie: "", documentElement: { lang, dataset: {}, scrollHeight: 1000 }, body,
    head: { appendChild(script) { scripts.push(script); } },
    createElement(tag) { const result = node(); result.tagName = tag.toUpperCase(); return result; },
    querySelector(selector) { if (selector.includes("googletagmanager")) return scripts.find(s => s.src?.includes("googletagmanager")) || null; if (selector === ".footer-legal-links" || selector === "footer") return footer; return null; },
    querySelectorAll(selector) { if (selector === ".form-status") return statuses; if (selector === "form") return forms; return []; },
    getElementById(id) { return [...statuses, ...forms].find(n => n.id === id) || null; }, contains: () => true
  });
  const location = new URL("https://itdks.tech" + pathname + "?email=private@example.invalid&gclid=TEST-click_id#private-text");
  const context = eventTarget({ document: doc, location, navigator: { language: lang, doNotTrack: dnt, globalPrivacyControl: gpc, sendBeacon(url, body) { beacons.push({ url, body }); return true; } },
    localStorage, sessionStorage, URL, Blob, Intl, console, queueMicrotask, innerWidth: 390, innerHeight: 844, scrollY: 0,
    matchMedia: () => ({ matches: false }), requestAnimationFrame: fn => { fn(); return 1; },
    fetch: async () => ({ ok: true }),
    MutationObserver: class { constructor(fn) { this.fn = fn; } observe(target) { observers.set(target, this.fn); } },
    CustomEvent: class { constructor(type, props = {}) { this.type = type; Object.assign(this, props); } },
    FormData: class { constructor(form) { this.fields = form.fields; } entries() { return Object.entries(this.fields); } }
  });
  context.window = context;
  vm.createContext(context);
  vm.runInContext(source["analytics-config.js"], context);
  vm.runInContext(source["consent.js"], context);
  vm.runInContext(source[bundle], context);
  const panel = elements.find(n => n.className === "itd-consent");
  const calls = () => (context.dataLayer || []).map(args => Array.from(args));
  const conversions = () => calls().filter(args => args[0] === "event" && args[1] === "conversion");
  const choose = action => panel.querySelector(`[data-consent-action="${action}"]`).dispatchEvent({ type: "click" });
  return { context, doc, panel, scripts, beacons, statuses, forms, calls, conversions, choose, localStorage, sessionStorage, observers, footer };
}

let scenarios = 0;
for (const bundle of ["analytics.js", "analytics.min.js"]) {
  const h = harness({ bundle });
  assert.equal(h.scripts.length, 0, "No Google request before a choice");
  assert.equal(h.beacons.length, 0, "No local collection before a choice");
  assert.equal(h.localStorage.data.size, 0, "No persistent tracking IDs before consent");
  assert.equal(h.panel.hidden, false);
  assert.equal(h.calls()[0][1], "default", "Consent defaults precede configuration");
  assert(Object.values(h.calls()[0][2]).every(v => v === "denied"));
  h.context.ITDAnalytics.track("form_submit_attempt", { email: "private@example.invalid" });
  h.choose("reject");
  assert.equal(h.panel.hidden, true);
  const deniedResponse = { ok: true };
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", deniedResponse);
  h.statuses[0].textContent = "Accepted"; h.statuses[0].classList.add("success");
  await flush();
  assert.equal(h.conversions().length, 0, "Denied enquiries do not convert");
  h.context.ITDConsent.open(); h.choose("accept");
  assert.equal(h.scripts.length, 1);
  assert.equal(h.conversions().length, 0, "Granting consent does not replay earlier enquiries");
  assert.equal(h.calls().filter(c => c[0] === "config").length, 2);
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", deniedResponse);
  assert.equal(h.conversions().length, 0, "Denied success cannot be replayed after consent");
  h.statuses[0].className = "form-status"; await flush();
  h.statuses[0].textContent = "Accepted again"; h.statuses[0].classList.add("success"); await flush();
  assert.equal(h.conversions().length, 0, "Success-message changes alone do not convert");
  for (const response of [undefined, null, {}, { ok: false }]) h.context.ITDAnalytics.reportLeadSuccess("contact-form", response);
  assert.equal(h.conversions().length, 0, "Missing/failed responses do not convert");
  const acceptedResponse = { ok: true };
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", acceptedResponse);
  assert.equal(h.conversions().length, 1);
  const event = h.conversions()[0][2];
  assert.equal(event.send_to, adsDestination); assert.equal(event.value, 1); assert.equal(event.currency, "USD");
  assert.deepEqual(Object.keys(event).sort(), ["currency", "send_to", "transaction_id", "value"]);
  h.statuses[0].textContent = "Accepted again"; h.observers.get(h.statuses[0])(); await flush();
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", acceptedResponse);
  assert.equal(h.conversions().length, 1, "Repeated DOM mutations do not duplicate conversions");
  h.statuses[1].textContent = "Accepted package"; h.statuses[1].classList.add("success"); await flush();
  h.context.ITDAnalytics.reportLeadSuccess("package-form", { ok: true });
  assert.equal(h.conversions().length, 1, "Package enquiries are excluded");
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", { ok: true });
  assert.equal(h.conversions().length, 2);
  assert.notEqual(h.conversions()[0][2].transaction_id, h.conversions()[1][2].transaction_id);
  h.statuses[2].textContent = "Unrelated success"; h.statuses[2].classList.add("success"); await flush();
  assert.equal(h.conversions().length, 2, "Unrelated statuses never count");
  h.context.ITDAnalytics.track("email_click", { href: "mailto:private@example.invalid", label: "Private", message: "Secret" });
  const ga = h.calls().filter(c => c[0] === "event" && c[1] !== "conversion");
  assert(ga.every(c => c[2].send_to === "G-B0S3HLRPWD"));
  assert(!JSON.stringify(ga).includes("private@example.invalid"));
  assert(!JSON.stringify(ga).includes("Secret"));
  assert(ga.every(c => c[2].page_location === "https://itdks.tech/contact-en?gclid=TEST-click_id"));
  const before = h.calls().filter(c => c[0] === "event").length, localBefore = h.beacons.length;
  h.context.ITDConsent.open(); h.choose("reject");
  h.context.ITDAnalytics.track("page_view");
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", { ok: true });
  h.statuses[0].className = "form-status"; await flush(); h.statuses[0].classList.add("success"); await flush();
  assert.equal(h.calls().filter(c => c[0] === "event").length, before);
  assert.equal(h.beacons.length, localBefore);
  assert(!h.localStorage.data.has("itd_visitor_id")); assert(!h.sessionStorage.data.has("itd_session_id"));
  vm.runInContext(source[bundle], h.context);
  assert.equal(h.scripts.length, 1, "Repeated initialization keeps one loader");
  scenarios += 14;
}

for (const category of ["analytics", "advertising"]) {
  const h = harness();
  h.panel.querySelector(`[name="itd-${category}"]`).checked = true; h.choose("save");
  assert.equal(h.calls().filter(c => c[0] === "config").length, 1);
  assert.equal(h.calls().find(c => c[0] === "config")[1], category === "analytics" ? "G-B0S3HLRPWD" : "AW-18460710310");
  h.statuses[0].textContent = "Accepted"; h.statuses[0].classList.add("success"); await flush();
  h.context.ITDAnalytics.reportLeadSuccess("contact-form", { ok: true });
  assert.equal(h.conversions().length, category === "advertising" ? 1 : 0);
  assert.equal(h.beacons.length > 0, category === "analytics");
  scenarios++;
}

const granted = { version: 1, updatedAt: Date.now(), analytics: true, advertising: true };
for (const options of [{ dnt: "1" }, { gpc: true }]) {
  const h = harness({ ...options, saved: granted });
  assert.equal(h.scripts.length, 0); assert.equal(h.beacons.length, 0);
  h.context.ITDConsent.open(); h.choose("accept");
  assert.equal(h.context.ITDConsent.get().advertising, false); scenarios++;
}
assert.equal(harness({ saved: granted }).scripts.length, 1);
assert.equal(harness({ saved: { ...granted, updatedAt: Date.now() - 181 * 86400000 } }).scripts.length, 0);
assert.equal(harness({ saved: { ...granted, updatedAt: Date.now() + 86400000 } }).scripts.length, 0);
assert.equal(harness({ pathname: "/stats/admin.html" }).scripts.length, 0);
const blockedStorage = harness({ storageBlocked: true }); blockedStorage.choose("accept"); assert.equal(blockedStorage.scripts.length, 1);
scenarios += 5;

// Exercise the actual current desktop and mobile form controllers with isolated responses.
for (const mode of ["mobile", "desktop", "mobile-min", "desktop-min"]) {
  for (const result of ["validation", "validation-empty", "http-error", "network-error", "success", "success-denied", "success-no-tracking", "success-broken-tracking", "success-double-click"]) {
    const h = harness({ saved: result === "success-denied" ? { ...granted, analytics: false, advertising: false } : granted, bundle: mode.endsWith("-min") ? "analytics.min.js" : "analytics.js" });
    const ctx = h.context;
    Object.assign(ctx, { FORM_ENDPOINT: "https://example.invalid/form", copy: new Proxy({}, { get: (_, key) => key }), packageForm: h.forms[1], packageFormStatus: h.statuses[1], packageHiddenPackage: null, packageHiddenSubject: { value: "Test" }, isGermanPage: false, isEnglishPage: true });
    if (mode === "mobile-min") {
      const code = source["app-lite.min.js"].split("function Z(e,t){")[1].split("function ee(){")[0];
      assert(code, "Optimized mobile controller extraction");
      vm.runInContext('var F=FORM_ENDPOINT,s=copy; function f(el, message, kind) { el.className = "form-status" + (kind ? " " + kind : ""); el.textContent = message; }\nfunction Z(e,t){' + code + '\nX(); Z(packageForm,packageFormStatus);', ctx);
    } else if (mode === "desktop-min") {
      const code = source["app.min.js"].split('packageForm&&packageFormStatus&&packageForm.addEventListener("submit",')[1].split('document.querySelectorAll(".button, .button-ghost, .utility-button, .nav-toggle")')[0];
      assert(code, "Optimized desktop controller extraction");
      vm.runInContext('packageForm&&packageFormStatus&&packageForm.addEventListener("submit",' + code.replace(/,$/, ";"), ctx);
    } else if (mode === "mobile") {
      const code = source["app-lite.js"].split("  function setupPackageForm(")[1].split("  function setupButtons(")[0];
      vm.runInContext('function setStatus(el, message, kind) { el.className = "form-status" + (kind ? " " + kind : ""); el.textContent = message; }\nfunction setupPackageForm(' + code + '\nsetupContactForm(); setupPackageForm(packageForm, packageFormStatus);', ctx);
    } else {
      const code = source["app.js"].split("if (packageForm && packageFormStatus) {")[1].split('document.querySelectorAll(".button, .button-ghost, .utility-button, .nav-toggle")')[0];
      vm.runInContext("if (packageForm && packageFormStatus) {" + code, ctx);
    }
    if (result === "success-no-tracking") ctx.ITDAnalytics = undefined;
    if (result === "success-broken-tracking") ctx.ITDAnalytics = { reportLeadSuccess() { throw Error("blocked tag"); } };
    let requests = 0;
    ctx.fetch = async () => { requests++; if (result === "network-error") throw Error("network unavailable"); return { ok: result.startsWith("success") }; };
    for (const form of h.forms) {
      if (result === "validation") form.fields.email = "invalid";
      if (result === "validation-empty") form.fields.emri = "";
      form.dispatchEvent({ type: "submit", preventDefault() {} });
      if (result === "success-double-click") form.dispatchEvent({ type: "submit", preventDefault() {} });
      await flush();
      assert.equal(form.resetCount || 0, result.startsWith("success") ? 1 : 0, `${mode}: reset preserved for ${result}`);
      if (result.startsWith("success")) assert(h.statuses[h.forms.indexOf(form)].classList.contains("success"), `${mode}: existing success UI preserved`);
    }
    assert.equal(requests, result.startsWith("validation") ? 0 : 2, `${mode}: request count for ${result}`);
    assert.equal(h.conversions().length, ["success", "success-double-click"].includes(result) ? 1 : 0, `${mode}: ${result}`);
    scenarios++;
  }
}

let pages = 0;
for (const file of await readdir(root)) {
  if (!file.endsWith(".html")) continue;
  const html = await readFile(resolve(root, file), "utf8");
  const head = html.split("</head>")[0];
  for (const name of ["analytics-config.js", "consent.js", "analytics.min.js"]) assert.equal((head.match(new RegExp(`src="/${name.replaceAll(".", "\\.")}\\?v=ads2"`, "g")) || []).length, 1, `${file}: shared ${name} in head`);
  assert(head.indexOf("/analytics-config.js") < head.indexOf("/consent.js")); assert(head.indexOf("/consent.js") < head.indexOf("/analytics.min.js"));
  for (const name of ["app.min.js", "app-lite.min.js"]) {
    const version = createHash("sha256").update(source[name]).digest("hex").slice(0, 16);
    assert(html.includes(`${name}?v=${version}"`), `${file}: ${name} must use its current content hash, not a reused immutable URL`);
    assert(source[name].includes('reportLeadSuccess("contact-form",'), `${name}: accepted contact response hook missing`);
  }
  assert(!html.includes("window.ITD_ANALYTICS_CONFIG=")); assert(!html.includes("gtag('event', 'conversion'"));
  assert(!html.includes("0VFlCISB6P0cEKar4OJE"));
  assert(!/<html[^>]*(?:\samp|⚡)/i.test(html));
  if (file.startsWith("privacy")) {
    assert(html.includes('id="measurement-privacy"'));
    assert(!/contact or package enquiry|kontakti ose pakete|Kontakt- oder Paketanfrage/.test(html));
  }
  pages++;
}
console.log(`tracking-audit: PASS (${scenarios} behavior scenarios, ${pages} public pages; no external requests)`);
