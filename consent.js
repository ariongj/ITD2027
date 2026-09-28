(function () {
  "use strict";
  if (window.ITDConsent || location.pathname.indexOf("/stats/") === 0 || document.documentElement.dataset.analytics === "off") return;
  var key = "itd_measurement_consent_v1";
  var maxAge = 180 * 24 * 60 * 60 * 1000;
  var config = window.ITD_ANALYTICS_CONFIG || {};
  var privacySignal = Boolean((config.respectDoNotTrack && (navigator.doNotTrack === "1" || window.doNotTrack === "1")) || navigator.globalPrivacyControl);
  var choice = { analytics: false, advertising: false };
  var hasChoice = false;
  var panel, analyticsInput, advertisingInput, reopen, previousFocus;
  var lang = document.documentElement.lang || "sq";
  var locale = lang.indexOf("de") === 0 ? "de" : lang.indexOf("en") === 0 ? "en" : "sq";
  var copy = {
    sq: { title: "Zgjedhjet e privatësisë", text: "Ti zgjedh nëse lejon matjen e vizitave dhe të kërkesave nga reklamat. Formularët funksionojnë edhe pa to.", analytics: "Analiza e vizitave", advertising: "Matja e reklamave", reject: "Refuzo opsionalet", save: "Ruaj zgjedhjet", accept: "Lejo të gjitha", privacy: "Privatësia", settings: "Cilësimet e privatësisë", signal: "Sinjali i privatësisë i shfletuesit e mban matjen opsionale të çaktivizuar." },
    en: { title: "Privacy choices", text: "Choose whether to allow visit analytics and measurement of enquiries from ads. Forms work without either.", analytics: "Visit analytics", advertising: "Ad measurement", reject: "Reject optional", save: "Save choices", accept: "Allow all", privacy: "Privacy policy", settings: "Privacy settings", signal: "Your browser privacy signal keeps optional measurement disabled." },
    de: { title: "Datenschutzauswahl", text: "Sie entscheiden über Besuchsanalysen und die Messung von Anfragen aus Anzeigen. Formulare funktionieren auch ohne beides.", analytics: "Besuchsanalyse", advertising: "Anzeigenmessung", reject: "Optionales ablehnen", save: "Auswahl speichern", accept: "Alle erlauben", privacy: "Datenschutz", settings: "Datenschutzeinstellungen", signal: "Das Datenschutzsignal Ihres Browsers deaktiviert optionale Messungen." }
  }[locale];

  try {
    var saved = JSON.parse(localStorage.getItem(key) || "null");
    if (saved && saved.version === 1 && Date.now() >= saved.updatedAt && Date.now() - saved.updatedAt < maxAge) {
      choice = { analytics: saved.analytics === true, advertising: saved.advertising === true };
      hasChoice = true;
    }
  } catch (error) { /* Private browsing can block preference storage. */ }
  if (privacySignal) choice = { analytics: false, advertising: false };

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag("consent", "default", {
    analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied"
  });
  window.gtag("set", "ads_data_redaction", true);

  function state() { return { analytics: choice.analytics, advertising: choice.advertising }; }
  function updateGoogle() {
    window["ga-disable-" + config.gaMeasurementId] = !choice.analytics;
    window.gtag("consent", "update", {
      analytics_storage: choice.analytics ? "granted" : "denied",
      ad_storage: choice.advertising ? "granted" : "denied",
      ad_user_data: choice.advertising ? "granted" : "denied",
      // This installation measures enquiries; it does not enable personalized ads.
      ad_personalization: "denied"
    });
  }
  function clearMeasurementCookies() {
    if (!choice.analytics) {
      try { localStorage.removeItem("itd_visitor_id"); localStorage.removeItem("itd_analytics_debug_events"); sessionStorage.removeItem("itd_session_id"); } catch (error) {}
    }
    document.cookie.split(";").forEach(function (part) {
      var name = part.split("=")[0].trim();
      var shouldClear = (!choice.analytics && /^_ga(?:_|$)|^_gid$|^_gat(?:_|$)/.test(name)) || (!choice.advertising && /^_gcl_/.test(name));
      if (!shouldClear) return;
      var hostname = location.hostname;
      var domains = ["", hostname, "." + hostname];
      if (hostname === "itdks.tech" || hostname.endsWith(".itdks.tech")) domains.push(".itdks.tech");
      domains.forEach(function (domain) {
        document.cookie = name + "=; Max-Age=0; path=/; SameSite=Lax" + (domain ? "; domain=" + domain : "");
      });
    });
  }
  function closePanel() {
    panel.hidden = true;
    document.body.classList.remove("itd-consent-visible");
    if (previousFocus && document.contains(previousFocus)) previousFocus.focus({ preventScroll: true });
  }
  function save(next) {
    choice = privacySignal ? { analytics: false, advertising: false } : { analytics: next.analytics === true, advertising: next.advertising === true };
    hasChoice = true;
    try { localStorage.setItem(key, JSON.stringify({ version: 1, updatedAt: Date.now(), analytics: choice.analytics, advertising: choice.advertising })); } catch (error) {}
    updateGoogle();
    clearMeasurementCookies();
    window.dispatchEvent(new CustomEvent("itd:consent-change", { detail: state() }));
    closePanel();
  }
  function show() {
    if (!panel) return;
    previousFocus = document.activeElement;
    analyticsInput.checked = choice.analytics;
    advertisingInput.checked = choice.advertising;
    panel.hidden = false;
    document.body.classList.add("itd-consent-visible");
    panel.querySelector("button").focus({ preventScroll: true });
  }
  window.ITDConsent = { get: state, open: show, privacySignal: privacySignal };
  if (hasChoice || privacySignal) updateGoogle();
  clearMeasurementCookies();

  function init() {
    panel = document.createElement("section");
    panel.className = "itd-consent";
    panel.dataset.itdConsent = "true";
    panel.setAttribute("aria-labelledby", "itd-consent-title");
    panel.hidden = hasChoice || privacySignal;
    panel.innerHTML = '<h2 id="itd-consent-title">' + copy.title + '</h2><p>' + copy.text + '</p>' +
      '<div class="itd-consent-options"><label><input type="checkbox" name="itd-analytics">' + copy.analytics + '</label><label><input type="checkbox" name="itd-advertising">' + copy.advertising + '</label></div>' +
      '<div class="itd-consent-actions"><button type="button" data-consent-action="reject">' + copy.reject + '</button><button type="button" data-consent-action="save">' + copy.save + '</button><button type="button" data-consent-action="accept">' + copy.accept + '</button></div>' +
      '<a href="/privacy' + (locale === "sq" ? "" : "-" + locale) + '">' + copy.privacy + '</a>' + (privacySignal ? '<p class="itd-consent-signal">' + copy.signal + '</p>' : '');
    document.body.appendChild(panel);
    analyticsInput = panel.querySelector('[name="itd-analytics"]');
    advertisingInput = panel.querySelector('[name="itd-advertising"]');
    analyticsInput.disabled = advertisingInput.disabled = privacySignal;
    analyticsInput.checked = choice.analytics;
    advertisingInput.checked = choice.advertising;
    panel.querySelector('[data-consent-action="reject"]').addEventListener("click", function () { save({ analytics: false, advertising: false }); });
    panel.querySelector('[data-consent-action="save"]').addEventListener("click", function () { save({ analytics: analyticsInput.checked, advertising: advertisingInput.checked }); });
    panel.querySelector('[data-consent-action="accept"]').addEventListener("click", function () { save({ analytics: true, advertising: true }); });
    panel.querySelector('[data-consent-action="accept"]').disabled = privacySignal;
    panel.addEventListener("keydown", function (event) { if (event.key === "Escape" && hasChoice) closePanel(); });
    reopen = document.createElement("button");
    reopen.type = "button";
    reopen.className = "itd-consent-settings";
    reopen.dataset.itdConsent = "true";
    reopen.textContent = copy.settings;
    reopen.addEventListener("click", show);
    var footer = document.querySelector(".footer-legal-links") || document.querySelector("footer");
    if (footer) footer.appendChild(reopen);
    if (!panel.hidden) document.body.classList.add("itd-consent-visible");
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();
})();
