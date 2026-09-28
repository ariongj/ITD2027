import { readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { localSeo, focusedServices } from "./local-seo.mjs";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const root = dirname(scriptDir);
const config = JSON.parse(await readFile(join(root, "site.config.json"), "utf8"));

// Normalize before hashing: immutable browser URLs must change with the actual
// form-controller bytes, even when a release's manual assetVersion is unchanged.
const appVersions = {};
for (const name of ["app.js", "app-lite.js", "app.min.js", "app-lite.min.js"]) {
  const path = join(root, name);
  const before = await readFile(path, "utf8");
  const after = before
    .replace(/https:\/\/formspree\.io\/f\/[A-Za-z0-9_-]+/g, config.formEndpoint)
    .replace(/https:\/\/calendly\.com\/[^"'`\s]+/g, config.bookingUrl)
    .replace(/38349573570/g, config.phoneDigits)
    .replaceAll("itdepartment.al", "itdks.tech");
  if (after !== before) await writeFile(path, after, "utf8");
  appVersions[name] = createHash("sha256").update(after).digest("hex").slice(0, 16);
}

const seo = {
  "404.html": {
    description: "Faqja nuk u gjet. Kthehu te IT Department për shërbime web, softuer, AI, automatizim, IT support dhe siguri për biznesin."
  },
  "contact.html": {
    description: "Kontakto IT Department në Prishtinë për faqe web, softuer, AI, automatizim, IT support, infrastrukturë dhe auditim sigurie për biznesin."
  },
  "contact-en.html": {
    description: "Contact IT Department in Prishtina for websites, software, AI automation, IT support, infrastructure and cybersecurity audits for your business."
  },
  "contact-de.html": {
    description: "Kontaktieren Sie IT Department in Prishtina für Websites, Software, KI-Automatisierung, IT-Support, Infrastruktur und Cybersicherheitsaudits."
  },
  "creative.html": {
    description: "Kreativë, branding, identitet vizual dhe marketing digjital nga IT Department për biznese që duan komunikim të qartë dhe prezencë profesionale."
  },
  "creative-en.html": {
    description: "Creative work, branding, visual identity and digital marketing from IT Department for businesses that want clear communication and a professional presence."
  },
  "privacy.html": {
    modified: "2026-09-24",
    description: "Politika e privatësisë e IT Department shpjegon të dhënat që përpunohen nga formularët, chat-i AI, analiza e faqes dhe shërbimet e jashtme."
  },
  "privacy-en.html": {
    modified: "2026-09-24",
    description: "The IT Department privacy policy explains data processed through forms, AI chat, website analytics and external services, including retention and deletion."
  },
  "privacy-de.html": {
    modified: "2026-09-24",
    description: "Die Datenschutzerklärung von IT Department erläutert Datenverarbeitung über Formulare, AI-Chat, Website-Analyse und externe Dienste."
  },
  "projects.html": {
    description: "Shiko shembuj projektesh nga IT Department për faqe web, softuer, automatizim, AI, infrastrukturë IT, siguri dhe raportim biznesi."
  },
  "projects-en.html": {
    description: "Explore IT Department project examples across websites, software, automation, AI, IT infrastructure, cybersecurity and business reporting."
  },
  "projects-de.html": {
    description: "Entdecken Sie Projektbeispiele von IT Department für Websites, Software, Automatisierung, KI, IT-Infrastruktur, Cybersicherheit und Reporting."
  },
  "terms.html": {
    description: "Kushtet e përdorimit të faqes IT Department shpjegojnë informacionin, kërkesat për shërbime, platformat e jashtme dhe përdorimin e lejuar."
  },
  "terms-en.html": {
    description: "The IT Department website terms explain site information, service inquiries, external platforms, acceptable use and communication responsibilities."
  },
  "terms-de.html": {
    description: "Die Nutzungsbedingungen der IT-Department-Website erklären Website-Informationen, Leistungsanfragen, externe Plattformen und zulässige Nutzung."
  },
  "index-en.html": {
    title: "IT Department Kosovo | Web, Software, AI & IT Support"
  },
  "index-de.html": {
    title: "IT Department Kosovo | Web, Software, KI & IT-Support"
  }
};
Object.assign(seo, localSeo);

const localeCopy = {
  sq: {
    ecosystem: "Teknologjit&euml; dhe platformat",
    ecosystemAria: "Teknologjitë dhe platformat që përdorim",
    hiddenHeading: "P&euml;rmbajtja kryesore"
  },
  en: {
    ecosystem: "Technologies and platforms",
    ecosystemAria: "Technologies and platforms we use",
    hiddenHeading: "Main page content"
  },
  de: {
    ecosystem: "Technologien und Plattformen",
    ecosystemAria: "Technologien und Plattformen, die wir nutzen",
    hiddenHeading: "Hauptinhalt der Seite"
  }
};

function documentLocale(html) {
  const match = html.match(/<html[^>]*\blang="([^"]+)"/i);
  const lang = (match?.[1] || "sq").toLowerCase();
  return lang.startsWith("de") ? "de" : lang.startsWith("en") ? "en" : "sq";
}

function escapeAttribute(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function replaceMeta(html, key, value) {
  const escaped = escapeAttribute(value);
  const pattern = new RegExp(`(<meta\\s+(?:name|property)="${key}"\\s+content=")[^"]*(")`, "i");
  return pattern.test(html) ? html.replace(pattern, `$1${escaped}$2`) : html;
}

function updateStructuredData(html, pageSeo, fileName, locale) {
  return html.replace(
    /(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g,
    (full, open, raw, close) => {
      try {
        const data = JSON.parse(raw);
        const visit = (value) => {
          if (!value || typeof value !== "object") return;
          if (Array.isArray(value)) {
            value.forEach(visit);
            return;
          }

          if (Object.hasOwn(value, "dateModified") && pageSeo?.modified) {
            value.dateModified = pageSeo.modified;
          }

          // PrivacyPolicy is not a Schema.org page type.
          if (value["@type"] === "PrivacyPolicy") value["@type"] = "WebPage";
          const types = Array.isArray(value["@type"]) ? value["@type"] : [value["@type"]];
          const isPage = types.some((type) => typeof type === "string" && /Page$/.test(type));
          if (isPage && pageSeo?.description) value.description = pageSeo.description;
          if (isPage && pageSeo?.title) value.name = pageSeo.title;
          if (isPage && pageSeo?.modified && value.url) value["@id"] = `${value.url}#webpage`;

          if (types.includes("BreadcrumbList") && pageSeo?.breadcrumb && Array.isArray(value.itemListElement)) {
            const last = value.itemListElement.at(-1);
            if (last && typeof last === "object") last.name = pageSeo.breadcrumb;
          }

          Object.values(value).forEach(visit);
        };
        visit(data);
        if (/^services(?:-en|-de)?\.html$/.test(fileName)) {
          const canonical = html.match(/<link rel="canonical" href="([^"]+)"/)[1];
          const services = focusedServices[locale].map(service => ({
            "@type": "Service", "@id": `${canonical}#${service.id}-service`,
            name: service.name, description: service.description,
            url: `${canonical}#${service.id}`,
            provider: { "@id": `${config.siteUrl}/#organization` },
            areaServed: [{ "@type": "Country", name: "Kosovo" }, { "@type": "City", name: "Prishtina" }]
          }));
          data["@graph"] = data["@graph"].filter(item => item["@type"] !== "Service");
          data["@graph"].push(...services);
          const page = data["@graph"].find(item => /Page$/.test(item["@type"]));
          page.mainEntity = services.map(service => ({ "@id": service["@id"] }));
        }
        return `${open}${JSON.stringify(data)}${close}`;
      } catch (error) {
        throw new Error(`Cannot update structured data in ${fileName}: ${error.message}`);
      }
    }
  );
}

function ensureHeadingHierarchy(html, locale) {
  if (html.includes('class="visually-hidden"')) return html;
  const h1End = html.search(/<\/h1>/i);
  if (h1End < 0) return html;
  const tail = html.slice(h1End + 5);
  const next = tail.match(/<h([2-6])(?:\s[^>]*)?>/i);
  if (!next || Number(next[1]) <= 2 || next.index == null) return html;
  const position = h1End + 5 + next.index;
  const heading = `<h2 class="visually-hidden">${localeCopy[locale].hiddenHeading}</h2>`;
  return `${html.slice(0, position)}${heading}${html.slice(position)}`;
}

function moveProjectExamplesForward(html) {
  const casePattern = /<section class="section(?: case-examples-section)?"(?: id="case-examples")?>\s*<div class="container page-copy">\s*<p class="eyebrow">(?:Raste pune|Case examples|Fallbeispiele)<\/p>[\s\S]*?<\/section>/i;
  const caseMatch = html.match(casePattern);
  const heroMatch = html.match(/<section class="section hero">[\s\S]*?<\/section>/i);
  if (!caseMatch || !heroMatch) return html;

  let caseSection = caseMatch[0]
    .replace(
      /<section class="section(?: case-examples-section)?"(?: id="case-examples")?>/,
      '<section class="section case-examples-section" id="case-examples">'
    );
  const heroEnd = heroMatch.index + heroMatch[0].length;
  if (caseMatch.index > heroMatch.index && html.slice(heroEnd, caseMatch.index).trim() === "") {
    const currentBlockEnd = caseMatch.index + caseMatch[0].length;
    const normalized = `${heroMatch[0]}\n\n    ${caseSection}`;
    const current = html.slice(heroMatch.index, currentBlockEnd);
    if (current === normalized) return html;
    return `${html.slice(0, heroMatch.index)}${normalized}${html.slice(currentBlockEnd)}`;
  }
  html = html.replace(caseMatch[0], "");
  return html.replace(heroMatch[0], `${heroMatch[0]}\n\n    ${caseSection}`);
}

function updateHtml(fileName, html) {
  const locale = documentLocale(html);
  const pageSeo = seo[fileName];

  // One shared configuration, consent defaults before any Google tag, no duplicate loaders.
  const tracking = `<!-- ITD measurement -->\n  <link rel="stylesheet" href="/consent.css?v=${config.trackingVersion}" />\n  <script defer src="/analytics-config.js?v=${config.trackingVersion}"></script>\n  <script defer src="/consent.js?v=${config.trackingVersion}"></script>\n  <script defer src="/analytics.min.js?v=${config.trackingVersion}" data-itd-analytics="true"></script>\n  <!-- /ITD measurement -->`;
  html = html.replace(/<script>\s*window\.ITD_ANALYTICS_CONFIG\s*=[\s\S]*?<\/script>/g, "");
  if (html.includes("<!-- ITD measurement -->")) {
    html = html.replace(/<!-- ITD measurement -->[\s\S]*?<!-- \/ITD measurement -->/, tracking);
  } else html = html.replace(/<\/head>/i, `  ${tracking}\n</head>`);

  html = html
    // A regular stylesheet avoids unstyled layout and blue-link flashes on phones.
    .replace(/<link rel="preload" href="(styles\.min\.css[^\"]*)" as="style" onload="[^"]*"\s*\/>\s*<noscript><link rel="stylesheet" href="[^"]+"\s*\/><\/noscript>/g, '<link rel="stylesheet" href="$1" />')
    .replaceAll("info@itdepartment.al", config.email)
    .replaceAll("info@itdks.tech", config.email)
    .replaceAll("https://formspree.io/f/xpqypezj", config.formEndpoint)
    .replaceAll("https://calendly.com/arion-gjonbalaj/30min", config.bookingUrl)
    .replaceAll("38349573570", config.phoneDigits)
    .replaceAll("itdepartment.al", "itdks.tech")
    .replace(/styles\.min\.css\?v=[^"']+/g, `styles.min.css?v=${config.assetVersion}`)
    .replace(/app-lite\.min\.js\?v=[^"']+/g, `app-lite.min.js?v=${appVersions["app-lite.min.js"]}`)
    .replace(/app\.min\.js\?v=[^"']+/g, `app.min.js?v=${appVersions["app.min.js"]}`)
    .replace(/chatbot\.js\?v=[^"']+/g, `chatbot.js?v=${config.chatVersion}`)
    .replace(/<button class="nav-toggle"(?![^>]*\baria-label=)/g, '<button class="nav-toggle" aria-label="Menu"')
    .replace(
      /(<div class="partner-tail">\s*<p class="eyebrow">)[^<]*(<\/p>\s*<div class="partner-logo-marquee[^"]*" aria-label=")[^"]*(")/g,
      `$1${localeCopy[locale].ecosystem}$2${localeCopy[locale].ecosystemAria}$3`
    );

  if (pageSeo?.title) {
    html = html.replace(/<title>[\s\S]*?<\/title>/i, `<title>${escapeAttribute(pageSeo.title)}</title>`);
    html = replaceMeta(html, "og:title", pageSeo.title);
    html = replaceMeta(html, "twitter:title", pageSeo.title);
  }
  if (pageSeo?.description) {
    html = replaceMeta(html, "description", pageSeo.description);
    html = replaceMeta(html, "og:description", pageSeo.description);
    html = replaceMeta(html, "twitter:description", pageSeo.description);
  }

  if (pageSeo?.h1) html = html.replace(/<h1>[\s\S]*?<\/h1>/, `<h1>${escapeAttribute(pageSeo.h1)}</h1>`);
  if (/^privacy(?:-en|-de)?\.html$/.test(fileName)) {
    const privacyCopy = {
      sq: ["Analiza dhe matja e reklamave", "Analiza e vizitave në serverin tonë dhe Google Analytics aktivizohen vetëm nëse i lejoni. Google Ads aktivizohet veçmas për matjen e reklamave. Google mund të marrë identifikues teknikë, adresën IP, informacione për pajisjen, faqen dhe klikimin e reklamës. Cookies mund të përdoren për të lidhur një vizitë me një reklamë.", "Një konvertim dërgohet vetëm pasi shërbimi i formularit pranon me sukses një kërkesë nga formulari i kontaktit, dhe vetëm kur matja e reklamave është e lejuar. Emri, emaili, telefoni dhe teksti i kërkesës nuk përfshihen në këtë ngjarje. Vlera fikse 1 USD është vlerë matjeje, jo pagesë apo të ardhura. Ky instalim nuk aktivizon reklama të personalizuara.", "Zgjedhja ruhet në këtë shfletues për 180 ditë. Mund ta ndryshoni ose të tërhiqni lejen te “Cilësimet e privatësisë” në fund të çdo faqeje. Pas tërheqjes ndalohen ngjarjet e reja; të dhënat e dërguara më parë nuk fshihen automatikisht. Respektojmë sinjalet Do Not Track dhe Global Privacy Control. Formularët punojnë edhe kur i refuzoni të dyja.", "Politika e privatësisë e Google", "Përditësuar më 24 shtator 2026."],
      en: ["Analytics and ad measurement", "Visit analytics on our server and Google Analytics are enabled only if you allow them. Google Ads is enabled separately for ad measurement. Google may receive technical identifiers, your IP address, device information, the page and ad-click information. Cookies may be used to connect a visit to an ad.", "A conversion is sent only after the form service successfully accepts an enquiry from the contact form, and only when ad measurement is allowed. Your name, email, phone number and enquiry text are not included in this event. The fixed value of 1 USD is a measurement value, not a payment or revenue. This installation does not enable personalized ads.", "Your choice is stored in this browser for 180 days. You can change it or withdraw permission using “Privacy settings” at the bottom of every page. Withdrawal stops new events; previously sent data is not automatically deleted. We respect Do Not Track and Global Privacy Control signals. Forms work when you reject both options.", "Google privacy policy", "Updated on September 24, 2026."],
      de: ["Analyse und Anzeigenmessung", "Besuchsanalysen auf unserem Server und Google Analytics werden nur mit Ihrer Erlaubnis aktiviert. Google Ads wird separat zur Anzeigenmessung aktiviert. Google kann technische Kennungen, Ihre IP-Adresse, Geräteinformationen sowie Angaben zur Seite und zum Anzeigenklick erhalten. Cookies können einen Besuch einer Anzeige zuordnen.", "Eine Conversion wird nur gesendet, wenn der Formulardienst eine Anfrage über das Kontaktformular erfolgreich angenommen hat und die Anzeigenmessung erlaubt ist. Name, E-Mail, Telefonnummer und Anfragetext sind nicht Teil dieses Ereignisses. Der feste Wert von 1 USD dient nur der Messung und ist weder Zahlung noch Umsatz. Diese Installation aktiviert keine personalisierte Werbung.", "Ihre Auswahl wird 180 Tage in diesem Browser gespeichert. Unter „Datenschutzeinstellungen“ am Ende jeder Seite können Sie sie ändern oder widerrufen. Ein Widerruf stoppt neue Ereignisse; bereits gesendete Daten werden nicht automatisch gelöscht. Do Not Track und Global Privacy Control werden berücksichtigt. Formulare funktionieren auch, wenn Sie beide Optionen ablehnen.", "Google-Datenschutzerklärung", "Aktualisiert am 24. September 2026."]
    }[locale];
    const disclosure = `<article class="service-card reactive-panel" id="measurement-privacy"><h3>${privacyCopy[0]}</h3>${privacyCopy.slice(1, 4).map(text => `<p>${text}</p>`).join("\n")}<p><a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">${privacyCopy[4]}</a></p></article>`;
    if (html.includes('id="measurement-privacy"')) html = html.replace(/<article[^>]*id="measurement-privacy"[\s\S]*?<\/article>/, disclosure);
    else html = html.replace('</div><div class="highlight-card reactive-panel legal-contact-card">', `${disclosure}\n</div><div class="highlight-card reactive-panel legal-contact-card">`);
    html = html.replace(/(<p class="legal-updated">)[\s\S]*?(<\/p>)/, `$1${privacyCopy[5]}$2`);
  }
  if (pageSeo?.lead) html = html.replace(/<p class="lead">[\s\S]*?<\/p>/, `<p class="lead">${escapeAttribute(pageSeo.lead)}</p>`);
  if (/^services(?:-en|-de)?\.html$/.test(fileName)) {
    html = html.replace('class="container grid-2" style="margin-top: 22px;"', 'class="container grid-2 service-catalogue" style="margin-top: 22px;"');
    let card = 0;
    html = html.replace(/<article class="service-card reactive-panel"(?: id="[^"]+")?>[\s\S]*?<\/article>/g, block => {
      const index = card++;
      const service = focusedServices[locale].find(service => service.card === index);
      if (!service) return block;
      return block.replace(/^<article[^>]+>/, `<article class="service-card reactive-panel" id="${service.id}">`)
        .replace(/<h3>[\s\S]*?<\/h3>\s*<p>[\s\S]*?<\/p>/,
          `<h3>${escapeAttribute(service.name)}</h3>\n          <p>${escapeAttribute(service.description)}</p>`);
    });
    const label = { sq: "Shko te shërbimi", en: "Jump to a service", de: "Direkt zur Leistung" }[locale];
    const shortcuts = `<nav class="service-shortcuts" aria-label="${label}">${focusedServices[locale].filter(service => service.id !== "it-audit").map(service => `<a href="#${service.id}">${service.label}</a>`).join("")}</nav>`;
    if (html.includes('class="service-shortcuts"')) html = html.replace(/<nav class="service-shortcuts"[\s\S]*?<\/nav>/, shortcuts);
    else html = html.replace(/(<p class="lead">[\s\S]*?<\/p>)/, `$1\n        ${shortcuts}`);
  }
  html = updateStructuredData(html, pageSeo, fileName, locale);
  html = ensureHeadingHierarchy(html, locale);
  if (/^projects(?:-en|-de)?\.html$/.test(fileName)) {
    html = moveProjectExamplesForward(html);
  }
  return html;
}

const files = await readdir(root, { withFileTypes: true });
// Whitespace-only compaction retains line boundaries (including line comments).
const analyticsSource = await readFile(join(root, "analytics.js"), "utf8");
await writeFile(join(root, "analytics.min.js"), analyticsSource.split(/\r?\n/).map(line => line.trim()).filter(Boolean).join("\n") + "\n", "utf8");
// Preserve the existing minified bundle and regenerate only the scoped polish.
const polishMarker = "/* ITD polish 2026-09: scoped service navigation and mobile input comfort. */";
const styleSource = await readFile(join(root, "styles.css"), "utf8");
if (!styleSource.includes(polishMarker)) throw new Error("Missing scoped CSS marker");
const minPath = join(root, "styles.min.css");
const minBefore = await readFile(minPath, "utf8");
const polish = styleSource.slice(styleSource.indexOf(polishMarker) + polishMarker.length).trim().replace(/\s+/g, " ");
const minAfter = `${minBefore.split(polishMarker)[0].trimEnd()}\n${polishMarker}\n${polish}\n`;
if (minAfter !== minBefore) await writeFile(minPath, minAfter, "utf8");
let changed = 0;
const changedFiles = [];
for (const entry of files) {
  if (!entry.isFile() || !entry.name.endsWith(".html")) continue;
  const path = join(root, entry.name);
  const before = await readFile(path, "utf8");
  const after = updateHtml(entry.name, before);
  if (after !== before) {
    await writeFile(path, after, "utf8");
    changed += 1;
    changedFiles.push(entry.name);
  }
}

const sitemapPath = join(root, "sitemap.xml");
const sitemapBefore = await readFile(sitemapPath, "utf8");
const sitemapAfter = sitemapBefore.replace(/<url>[\s\S]*?<\/url>/g, block => {
  const route = new URL(block.match(/<loc>([^<]+)<\/loc>/)[1]).pathname;
  const file = route === "/" ? "index.html" : route === "/en" || route === "/de" ? `index-${route.slice(1)}.html` : `${route.slice(1)}.html`;
  return seo[file]?.modified ? block.replace(/<lastmod>[^<]+<\/lastmod>/, `<lastmod>${seo[file].modified}</lastmod>`) : block;
});
if (sitemapAfter !== sitemapBefore) {
  await writeFile(sitemapPath, sitemapAfter, "utf8");
  changed += 1;
  changedFiles.push("sitemap.xml");
}

console.log(`Synchronized ${changed} generated site files; editorial modification dates preserved.`);
if (changedFiles.length) console.log(changedFiles.join(", "));
