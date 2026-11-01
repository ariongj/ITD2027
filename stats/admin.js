(function () {
  "use strict";
  // The admin key goes to the server in a request header (X-ITD-Stats-Key), never in an address, so it does not
  // end up in server logs or the browser history. It is kept for this browser tab only (sessionStorage).
  var adminKeyStorage = "itd_stats_admin_key";
  var summaryEndpoint = "/stats/summary.php";
  var exportEndpoint = "/stats/export.php";
  var config = window.ITD_MEASUREMENT || {};

  // Earlier versions kept the key, and a debug copy of events, in localStorage; both are removed.
  try {
    localStorage.removeItem(adminKeyStorage);
    localStorage.removeItem("itd_analytics_debug_events");
  } catch (error) {}
  // An old bookmark with the key in the address is not used any more; the key is taken out of the address bar.
  if (new URLSearchParams(window.location.search).has("key")) {
    window.history.replaceState({}, document.title, window.location.pathname);
  }

  function providerStatus(key, text, active) {
    var label = document.querySelector("[data-provider='" + key + "']");
    var dot = document.querySelector("[data-provider-dot='" + key + "']");
    if (!label || !dot) return;
    label.textContent = text;
    dot.className = "dot " + (active ? "live" : "off");
  }

  function number(value) {
    return new Intl.NumberFormat("en").format(Number(value || 0));
  }

  function status(message) {
    var node = document.querySelector("[data-summary-status]");
    if (node) node.textContent = message;
  }

  function storedKey() {
    try {
      return sessionStorage.getItem(adminKeyStorage) || "";
    } catch (error) {
      return "";
    }
  }

  function adminKey(force) {
    var existing = storedKey();
    if (existing && !force) return existing;
    var next = window.prompt("Enter ITD stats admin key", "");
    if (next === null) return existing;
    next = next.trim();
    try {
      if (next) sessionStorage.setItem(adminKeyStorage, next);
    } catch (error) {}
    return next;
  }

  function forgetKey() {
    try {
      sessionStorage.removeItem(adminKeyStorage);
    } catch (error) {}
  }

  function request(url, key) {
    return fetch(url, {
      cache: "no-store",
      credentials: "same-origin",
      headers: { "X-ITD-Stats-Key": key }
    }).then(function (response) {
      if (response.status === 401) {
        forgetKey();
        throw new Error("Wrong admin key.");
      }
      if (!response.ok) throw new Error("Stats endpoint returned " + response.status + ".");
      return response;
    });
  }

  function renderTop(target, values) {
    var node = document.querySelector("[data-top='" + target + "']");
    if (!node) return;
    var entries = Object.entries(values || {});
    if (!entries.length) {
      node.textContent = "No data yet.";
      return;
    }
    node.textContent = "";
    entries.forEach(function (entry, index) {
      if (index) node.appendChild(document.createElement("br"));
      var code = document.createElement("code");
      code.textContent = entry[0];
      node.appendChild(code);
      node.appendChild(document.createTextNode(" " + number(entry[1])));
    });
  }

  function renderHourly(values) {
    var node = document.querySelector("[data-hourly]");
    if (!node) return;
    node.textContent = "";
    var entries = Object.entries(values || {});
    if (!entries.length) {
      empty(node, "No hourly activity yet.");
      return;
    }
    var max = entries.reduce(function (top, entry) {
      return Math.max(top, Number(entry[1] || 0));
    }, 1);
    entries.forEach(function (entry) {
      var bar = document.createElement("div");
      bar.className = "hour-bar";
      bar.style.height = Math.max(8, Math.round((Number(entry[1] || 0) / max) * 120)) + "px";
      bar.title = entry[0] + " - " + number(entry[1]) + " events";
      var label = document.createElement("span");
      label.textContent = entry[0];
      bar.appendChild(label);
      node.appendChild(bar);
    });
  }

  function empty(node, message) {
    var box = document.createElement("div");
    box.className = "empty";
    box.textContent = message;
    node.appendChild(box);
  }

  function renderSummary(summary) {
    var totals = summary.totals || {};
    var top = summary.top || {};
    var ctas = top.cta_24h || {};
    document.querySelector("[data-metric='visitors']").textContent = number(totals.visitors_24h);
    document.querySelector("[data-metric='pageviews']").textContent = number(totals.pageviews_24h);
    document.querySelector("[data-metric='sessions']").textContent = number(totals.sessions_24h);
    document.querySelector("[data-metric='ctas']").textContent = number(totals.cta_24h);
    document.querySelector("[data-metric='leads']").textContent = number(ctas.form_submit_success);
    document.querySelector("[data-metric='conversion']").textContent = number(totals.conversion_rate_24h) + "%";
    document.querySelector("[data-metric='bounce']").textContent = number(totals.bounce_rate_24h) + "%";
    document.querySelector("[data-metric='events-all']").textContent = number(totals.events_all);

    renderTop("pages", top.pages_24h);
    renderTop("events", top.events_24h);
    renderTop("countries", top.countries_7d);
    renderTop("timezones", top.timezones_7d);
    renderTop("devices", top.devices_7d);
    renderTop("browsers", top.browsers_7d);
    renderTop("languages", top.languages_7d);
    renderTop("referrers", top.referrers_7d);
    renderTop("sources", top.utm_sources_7d);
    renderTop("campaigns", top.utm_campaigns_7d);
    renderHourly(summary.hourly_24h);

    var generated = summary.generated_at ? new Date(summary.generated_at).toLocaleString() : "";
    status("Live server stats loaded" + (generated ? " at " + generated : "") + ".");

    var container = document.querySelector("[data-events]");
    container.textContent = "";
    var list = summary.latest || [];
    if (!list.length) {
      empty(container, "The collector is ready. Visits with “Statistics” consent will appear here.");
      return;
    }
    list.forEach(function (event) {
      var row = document.createElement("div");
      row.className = "event-row";
      var label = event.label || event.service || event.title || event.path || "";
      var location = event.country || event.timezone || "";
      var small = [location, event.device, event.browser, event.browser_language].filter(Boolean).join(" / ");
      var time = event.time ? new Date(event.time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "";
      var parts = [document.createElement("strong"), document.createElement("span"), document.createElement("small")];
      parts[0].textContent = event.event || "event";
      parts[1].textContent = label;
      parts[2].textContent = (time ? time + " " : "") + small;
      parts.forEach(function (part) { row.appendChild(part); });
      container.appendChild(row);
    });
  }

  function renderEmpty(message) {
    ["visitors", "pageviews", "sessions", "ctas", "leads", "events-all"].forEach(function (name) {
      document.querySelector("[data-metric='" + name + "']").textContent = "0";
    });
    ["conversion", "bounce"].forEach(function (name) {
      document.querySelector("[data-metric='" + name + "']").textContent = "0%";
    });
    ["pages", "events", "countries", "timezones", "devices", "browsers", "languages", "referrers", "sources", "campaigns"].forEach(function (name) {
      renderTop(name, {});
    });
    renderHourly({});
    var container = document.querySelector("[data-events]");
    container.textContent = "";
    empty(container, "No server data loaded. Use “Admin Key” to sign in to the statistics.");
    status(message);
  }

  function refreshSummary(forceKey) {
    var key = adminKey(Boolean(forceKey));
    if (!key) {
      renderEmpty("Admin key needed for the server statistics.");
      return;
    }
    status("Loading live server stats...");
    request(summaryEndpoint + "?t=" + Date.now(), key)
      .then(function (response) { return response.json(); })
      .then(function (summary) {
        if (!summary.ok) throw new Error(summary.error || "Stats endpoint error.");
        renderSummary(summary);
      })
      .catch(function (error) {
        renderEmpty(error.message || "Could not load the server statistics.");
      });
  }

  function exportCsv() {
    var key = adminKey(false);
    if (!key) {
      status("Admin key needed before export.");
      return;
    }
    status("Preparing the CSV export...");
    request(exportEndpoint, key)
      .then(function (response) { return response.blob(); })
      .then(function (blob) {
        var link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "itd-stats-export-" + new Date().toISOString().slice(0, 10) + ".csv";
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(function () { URL.revokeObjectURL(link.href); }, 1000);
        status("CSV export downloaded.");
      })
      .catch(function (error) {
        status(error.message || "Could not export the statistics.");
      });
  }

  var gaOn = config.enabled === true && /^G-[A-Z0-9]+$/i.test(config.id || "");
  providerStatus("ga", gaOn ? config.id + " on every page, consent mode" : "Not active on this build", gaOn);
  providerStatus("ads", gaOn && config.conversion ? "Enquiry conversion " + String(config.conversion).split("/")[0] : "Not active on this build", gaOn && Boolean(config.conversion));
  providerStatus("site", gaOn ? "Recorded with “Statistics” consent" : "Not active on this build", gaOn);
  refreshSummary(false);

  document.querySelector("[data-action='admin-key']").addEventListener("click", function () {
    refreshSummary(true);
  });
  document.querySelector("[data-action='export']").addEventListener("click", exportCsv);
  document.querySelector("[data-action='refresh']").addEventListener("click", function () {
    refreshSummary(false);
  });
})();
