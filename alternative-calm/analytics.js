(function () {
  "use strict";
  if (window.ITDAnalytics) return;

  var config = window.ITD_ANALYTICS_CONFIG || {};
  var path = window.location.pathname || "/";

  if (path.indexOf("/stats/") === 0 || document.documentElement.dataset.analytics === "off") {
    return;
  }

  if ((config.respectDoNotTrack && (navigator.doNotTrack === "1" || window.doNotTrack === "1")) || navigator.globalPrivacyControl) {
    return;
  }

  var storageKey = "itd_analytics_debug_events";
  var visitorKey = "itd_visitor_id";
  var sessionKey = "itd_session_id";
  var startedAt = Date.now();
  var maxEvents = 250;
  var sentScroll = {};
  var scrollFrame = 0;
  var maxScroll = 1;
  var providersLoaded = false;
  var googleConfigured = {};
  var sentConsentPageView = false;

  function allowed(category) {
    return Boolean(window.ITDConsent && window.ITDConsent.get()[category]);
  }

  function randomId(prefix) {
    if (window.crypto && window.crypto.randomUUID) {
      return prefix + "-" + window.crypto.randomUUID();
    }
    return prefix + "-" + Math.random().toString(36).slice(2) + Date.now().toString(36);
  }

  function getStored(key, storage, prefix) {
    try {
      var existing = storage.getItem(key);
      if (existing) return existing;
      var next = randomId(prefix);
      storage.setItem(key, next);
      return next;
    } catch (error) {
      return randomId(prefix);
    }
  }

  var visitorId = "";
  var sessionId = "";

  function readEvents() {
    try {
      return JSON.parse(window.localStorage.getItem(storageKey) || "[]");
    } catch (error) {
      return [];
    }
  }

  function writeDebugEvent(payload) {
    if (!config.enableLocalDebug) return;
    try {
      var events = readEvents();
      events.push(payload);
      window.localStorage.setItem(storageKey, JSON.stringify(events.slice(-maxEvents)));
    } catch (error) {
      // Ignore storage limits/private browsing.
    }
  }

  function pageMeta() {
    var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
    var localeParts = String(navigator.language || "").split("-");
    return {
      path: window.location.pathname || "/",
      url: measurementUrl(),
      title: document.title || "",
      language: document.documentElement.lang || "",
      browser_language: navigator.language || "",
      browser_languages: navigator.languages ? navigator.languages.slice(0, 3).join(",") : "",
      locale_country_hint: localeParts.length > 1 ? localeParts.pop().toUpperCase() : "",
      timezone: Intl.DateTimeFormat ? Intl.DateTimeFormat().resolvedOptions().timeZone || "" : "",
      timezone_offset: new Date().getTimezoneOffset(),
      platform: navigator.userAgentData && navigator.userAgentData.platform ? navigator.userAgentData.platform : navigator.platform || "",
      connection_type: connection.effectiveType || "",
      save_data: Boolean(connection.saveData),
      color_scheme: window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark",
      page_type: document.body ? document.body.dataset.pageVariant || "unknown" : "unknown",
      referrer: "",
      session_id: sessionId,
      visitor_id: visitorId
    };
  }

  function cleanLabel(value) {
    return String(value || "").replace(/\s+/g, " ").trim().slice(0, 140);
  }

  function sendToProviders(name, data) {
    if (!allowed("analytics")) return;
    loadProviders();
    if (window.gtag && googleConfigured[config.gaMeasurementId] && !(name === "page_view" && config.gaSendCustomPageView === false)) {
      // Never forward form values, chat text, clicked labels or prefilled URLs.
      var safe = { send_to: config.gaMeasurementId, page_location: measurementUrl(), page_title: document.title, language: document.documentElement.lang };
      ["depth", "form_id", "status_id", "destination_host"].forEach(function (key) { if (data[key] !== undefined) safe[key] = data[key]; });
      window.gtag("event", name, safe);
    }
    if (window.clarity) {
      window.clarity("event", name);
    }
    if (window.plausible) {
      window.plausible(name, { props: { path: path } });
    }
  }

  function measurementUrl() {
    var url = new URL(window.location.href);
    var safe = new URL(url.origin + url.pathname);
    ["gclid", "gbraid", "wbraid"].forEach(function (key) {
      var value = url.searchParams.get(key);
      if (value && /^[A-Za-z0-9_.~-]{1,256}$/.test(value)) safe.searchParams.set(key, value);
    });
    return safe.href;
  }

  function sendToCollector(payload) {
    if (!config.collectorEndpoint) return;
    try {
      var body = JSON.stringify(payload);
      if (navigator.sendBeacon) {
        var blob = new Blob([body], { type: "application/json" });
        if (navigator.sendBeacon(config.collectorEndpoint, blob)) return;
      }
      window.fetch(config.collectorEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
        credentials: "same-origin",
        keepalive: true
      }).catch(function () {});
    } catch (error) {
      // Analytics collection must never break the page.
    }
  }

  function track(name, data) {
    if (!allowed("analytics")) return;
    if (!visitorId) visitorId = getStored(visitorKey, window.localStorage, "visitor");
    if (!sessionId) sessionId = getStored(sessionKey, window.sessionStorage, "session");
    var payload = Object.assign({}, pageMeta(), data || {}, {
      event: name,
      timestamp: new Date().toISOString(),
      seconds_on_page: Math.round((Date.now() - startedAt) / 1000)
    });
    writeDebugEvent(payload);
    sendToProviders(name, payload);
    sendToCollector(payload);
  }

  function loadGoogleTag() {
    var analytics = allowed("analytics") && /^G-[A-Z0-9]+$/i.test(config.gaMeasurementId || "");
    var advertising = allowed("advertising") && /^AW-\d+$/.test(config.googleAdsId || "");
    if (!analytics && !advertising) return;
    var id = analytics ? config.gaMeasurementId : config.googleAdsId;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () {
      window.dataLayer.push(arguments);
    };
    if (!document.querySelector("script[src*='googletagmanager.com/gtag/js']")) {
      var script = document.createElement("script");
      script.async = true;
      script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
      document.head.appendChild(script);
      window.gtag("js", new Date());
    }
    if (analytics && !googleConfigured[config.gaMeasurementId]) {
      window.gtag("config", config.gaMeasurementId, { send_page_view: false, page_location: measurementUrl(), page_referrer: "", allow_google_signals: false, allow_ad_personalization_signals: false });
      googleConfigured[config.gaMeasurementId] = true;
    }
    if (advertising && !googleConfigured[config.googleAdsId]) {
      window.gtag("config", config.googleAdsId, { page_location: measurementUrl(), page_referrer: "", allow_ad_personalization_signals: false });
      googleConfigured[config.googleAdsId] = true;
    }
  }

  var handledLeadResponses = new WeakSet();
  function reportLeadSuccess(formId, response) {
    // Called only from the contact form's accepted fetch response, never from UI mutations.
    if (formId !== "contact-form" || !response || typeof response !== "object" || response.ok !== true || handledLeadResponses.has(response)) return false;
    // Remember denied successes too: later consent must not replay an earlier enquiry.
    handledLeadResponses.add(response);
    if (!allowed("advertising") || !/^AW-\d+$/.test(config.googleAdsId || "") || !/^[A-Za-z0-9_-]+$/.test(config.googleAdsContactLabel || "")) return false;
    try {
      loadGoogleTag();
      window.gtag("event", "conversion", {
        send_to: config.googleAdsId + "/" + config.googleAdsContactLabel,
        value: config.googleAdsContactValue,
        currency: config.googleAdsContactCurrency,
        transaction_id: randomId("enquiry")
      });
      return true;
    } catch (error) {
      // A blocked or unavailable tag must never turn a delivered enquiry into an error.
      return false;
    }
  }

  function loadClarity(id) {
    if (!/^[a-z0-9]{5,}$/i.test(id || "")) return false;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () {
        (c[a].q = c[a].q || []).push(arguments);
      };
      t = l.createElement(r);
      t.async = 1;
      t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", id);
    return true;
  }

  function loadPlausible(domain, src) {
    if (!domain) return false;
    var script = document.createElement("script");
    script.defer = true;
    script.dataset.domain = domain;
    script.src = src || "https://plausible.io/js/script.js";
    document.head.appendChild(script);
    window.plausible = window.plausible || function () {
      (window.plausible.q = window.plausible.q || []).push(arguments);
    };
    return true;
  }

  function loadProviders() {
    loadGoogleTag();
    if (providersLoaded || !allowed("analytics")) return;
    providersLoaded = true;
    loadClarity(config.clarityProjectId);
    loadPlausible(config.plausibleDomain, config.plausibleScript);
  }

  function refreshScrollMetrics() {
    var doc = document.documentElement;
    maxScroll = Math.max(doc.scrollHeight - window.innerHeight, 1);
  }

  function handleScrollDepth() {
    scrollFrame = 0;
    var depth = Math.round((window.scrollY / maxScroll) * 100);
    [25, 50, 75, 90].forEach(function (threshold) {
      if (depth >= threshold && !sentScroll[threshold]) {
        sentScroll[threshold] = true;
        track("scroll_depth", {
          depth: threshold
        });
      }
    });
  }

  function queueScrollDepth() {
    if (!scrollFrame) scrollFrame = window.requestAnimationFrame(handleScrollDepth);
  }

  function initPageTracking() {
    refreshScrollMetrics();
    function consentChanged() {
      loadProviders();
      if (allowed("analytics") && !sentConsentPageView) {
        sentConsentPageView = true;
        track("page_view", { viewport: window.innerWidth + "x" + window.innerHeight });
      }
      if (!allowed("analytics")) {
        try { localStorage.removeItem(visitorKey); localStorage.removeItem(storageKey); sessionStorage.removeItem(sessionKey); } catch (error) {}
        visitorId = sessionId = "";
      }
    }
    window.addEventListener("itd:consent-change", consentChanged);
    consentChanged();

    document.addEventListener("click", function (event) {
      var target = event.target && event.target.closest ? event.target.closest("a, button, [data-package-select]") : null;
      if (!target) return;
      if (target.closest("[data-itd-consent]")) return;
      var href = target.getAttribute("href") || "";
      var label = cleanLabel(target.innerText || target.getAttribute("aria-label") || href || target.tagName);
      var eventName = "ui_click";
      var details = {
        label: label,
        href: href,
        element: target.tagName.toLowerCase()
      };

      if (href.indexOf("wa.me/") !== -1) eventName = "whatsapp_click";
      else if (href.indexOf("calendly.com") !== -1) eventName = "booking_click";
      else if (href.indexOf("mailto:") === 0) eventName = "email_click";
      else if (href.indexOf("tel:") === 0) eventName = "phone_click";
      else if (target.classList && target.classList.contains("lang-option")) eventName = "language_switch";
      else if (target.hasAttribute("data-package-select")) {
        eventName = "package_select";
        details.package = target.dataset.packageLabel || "";
      } else if (href) {
        try {
          var url = new URL(href, window.location.href);
          if (url.hostname && url.hostname !== window.location.hostname) {
            eventName = "outbound_click";
            details.destination_host = url.hostname;
          }
        } catch (error) {
          // Keep the base ui_click event.
        }
      }
      track(eventName, details);
    }, { passive: true });

    document.querySelectorAll("form").forEach(function (form) {
      var started = false;
      form.addEventListener("input", function () {
        if (started) return;
        started = true;
        track("form_start", {
          form_id: form.id || "",
          form_action: form.getAttribute("action") || ""
        });
      }, { passive: true });
      form.addEventListener("submit", function () {
        track("form_submit_attempt", {
          form_id: form.id || "",
          form_action: form.getAttribute("action") || ""
        });
      });
    });

    document.querySelectorAll(".form-status").forEach(function (status) {
      var wasSuccess = status.classList.contains("success");
      var observer = new MutationObserver(function () {
        var text = cleanLabel(status.textContent);
        var success = Boolean(text && status.classList.contains("success"));
        var newSuccess = success && !wasSuccess;
        wasSuccess = success;
        if (!text || (success && !newSuccess)) return;
        track(success ? "form_submit_success" : "form_submit_message", {
          message: text,
          status_id: status.id || ""
        });
      });
      observer.observe(status, { childList: true, characterData: true, subtree: true, attributes: true });
    });

    document.querySelectorAll("select[name='sherbimi']").forEach(function (select) {
      select.addEventListener("change", function () {
        track("service_select", {
          service: cleanLabel(select.value)
        });
      });
    });

    window.addEventListener("load", refreshScrollMetrics, { once: true });
    window.addEventListener("resize", refreshScrollMetrics, { passive: true });
    window.addEventListener("scroll", queueScrollDepth, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPageTracking, { once: true });
  } else {
    initPageTracking();
  }

  window.ITDAnalytics = {
    reportLeadSuccess: reportLeadSuccess,
    track: track,
    readDebugEvents: readEvents,
    clearDebugEvents: function () {
      window.localStorage.removeItem(storageKey);
    }
  };
})();
