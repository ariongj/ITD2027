/* IT Department — site.js (Claude's version)
   Small, dependency-free. Everything degrades gracefully without JS. */
(function () {
  "use strict";

  // Tells the inline <head> failsafe that this script loaded, so it keeps
  // the fade-in effect instead of revealing everything at once.
  window.__itdReady = true;

  var doc = document;
  var root = doc.documentElement;
  var body = doc.body;
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Header shadow on scroll -------------------------------------------- */
  var header = doc.querySelector("[data-header]");
  function syncHeader() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", syncHeader, { passive: true });
  syncHeader();

  /* ---- Mobile navigation -------------------------------------------------- */
  var toggle = doc.querySelector("[data-nav-toggle]");
  var nav = doc.getElementById("site-nav");
  var toggleLabel = toggle ? toggle.querySelector(".nav-toggle-label") : null;
  function setNav(open, focusToggle) {
    if (!toggle || !nav) return;
    body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    // Keep keyboard focus inside the open menu: the page behind it (and the
    // skip link and chat button around it) is inert.
    [doc.getElementById("main"), doc.querySelector(".site-footer"), doc.querySelector(".skip-link"),
      doc.getElementById("itd-kraken-chat")].forEach(function (el) {
      if (!el) return;
      if (open) el.setAttribute("inert", "");
      else el.removeAttribute("inert");
    });
    if (toggleLabel) toggleLabel.textContent = open ? toggle.dataset.labelClose : toggle.dataset.labelOpen;
    if (open) {
      var first = nav.querySelector("a");
      if (first) first.focus({ preventScroll: true });
    } else if (focusToggle) {
      toggle.focus();
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(!body.classList.contains("nav-open"));
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setNav(false);
    });
    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && body.classList.contains("nav-open")) setNav(false, true);
    });
    var desktop = window.matchMedia("(min-width: 1101px)"); // matches the menu breakpoint in site.css
    if (desktop.addEventListener) desktop.addEventListener("change", function (m) { if (m.matches) setNav(false); });
  }

  /* ---- Theme toggle (light / dark) --------------------------------------- */
  var themeBtn = doc.querySelector("[data-theme-toggle]");
  function currentTheme() {
    var t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") return t;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    try { localStorage.setItem("itd-theme", theme); } catch (error) { /* private mode */ }
    if (themeBtn) themeBtn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }
  if (themeBtn) {
    themeBtn.setAttribute("aria-pressed", currentTheme() === "dark" ? "true" : "false");
    themeBtn.addEventListener("click", function () {
      applyTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  }

  /* ---- Reveal on scroll --------------------------------------------------- */
  var reveals = doc.querySelectorAll(".reveal");
  // Anything already in the first viewport shows immediately; only content
  // further down fades in as the visitor scrolls to it.
  Array.prototype.forEach.call(reveals, function (el) {
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.9) el.classList.add("reveal--instant", "is-visible");
  });
  if (reveals.length && "IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
    // Safety net: anything still hidden after 2s becomes visible.
    setTimeout(function () {
      reveals.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("is-visible");
      });
    }, 2000);
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---- Forms (Formspree via fetch) --------------------------------------- */
  function setupForm(form) {
    var status = form.querySelector(".form-status");
    var msg = form.dataset;
    // Without this script the browser's own required-field check applies;
    // with it, we show messages in the page's language instead.
    form.noValidate = true;
    function setStatus(text, kind) {
      if (!status) return;
      status.textContent = text || "";
      status.className = "form-status" + (kind ? " " + kind : "");
    }
    function markInvalid(field) {
      field.setAttribute("aria-invalid", "true");
      if (status && status.id) field.setAttribute("aria-describedby", status.id);
      field.focus();
    }
    form.addEventListener("input", function (event) {
      var field = event.target;
      if (field && field.getAttribute && field.getAttribute("aria-invalid") === "true") {
        field.removeAttribute("aria-invalid");
        field.removeAttribute("aria-describedby");
      }
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (form.dataset.submitting === "true") return;

      var missing = null;
      Array.prototype.forEach.call(form.querySelectorAll("[required]"), function (field) {
        if (!missing && !String(field.value || "").trim()) missing = field;
      });
      if (missing) {
        setStatus(msg.msgRequired, "error");
        markInvalid(missing);
        return;
      }
      var email = form.querySelector("input[type=email]");
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
        setStatus(msg.msgEmail, "error");
        markInvalid(email);
        return;
      }

      var button = form.querySelector("button[type=submit]");
      form.dataset.submitting = "true";
      form.setAttribute("aria-busy", "true");
      if (button) button.disabled = true;
      setStatus(msg.msgSending, "pending");

      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form)
      }).then(function (response) {
        if (!response.ok) throw new Error("submit failed");
        try {
          if (form.id === "contact-form" && window.ITDAnalytics && window.ITDAnalytics.reportLeadSuccess) {
            window.ITDAnalytics.reportLeadSuccess("contact-form", response);
          }
          // A delivered demo request for an ITD Labs product (no form values are sent).
          var demoField = form.querySelector("input[name=produkti]");
          if (demoField && demoField.value && window.ITDAnalytics && window.ITDAnalytics.track) {
            window.ITDAnalytics.track("request_demo", { form_id: form.id });
          }
        } catch (error) { /* tracking must never break the form */ }
        form.reset();
        setStatus(msg.msgSuccess, "success");
      }).catch(function () {
        setStatus(msg.msgError, "error");
      }).finally(function () {
        form.dataset.submitting = "false";
        form.removeAttribute("aria-busy");
        if (button) button.disabled = false;
      });
    });
  }
  Array.prototype.forEach.call(doc.querySelectorAll("form[data-ajax]"), setupForm);

  /* ---- Old package links -------------------------------------------------
     The previous site sent package choices to the home page, e.g.
     /?package=Business&price=299+EUR+/+month#package-inquiry. Forward those
     to the contact form so bookmarked or advertised links keep working. */
  if (body.classList.contains("page-home") && window.URLSearchParams) {
    var oldParams = new URLSearchParams(window.location.search);
    var oldPlan = oldParams.get("package");
    if (oldPlan && body.dataset.contactUrl) {
      var digits = (oldParams.get("price") || "").match(/\d+/);
      var target = body.dataset.contactUrl + "?package=" + encodeURIComponent(oldPlan) +
        (digits ? "&price=" + digits[0] : "") + "#contact-form";
      window.location.replace(target);
      return;
    }
  }

  /* ---- Contact page: prefill from ?package=Business&price=299 ----------- */
  var packageForm = doc.querySelector("[data-package-form]");
  if (packageForm && window.URLSearchParams) {
    var params = new URLSearchParams(window.location.search);
    var plan = params.get("package");
    var price = params.get("price") || "";
    if (plan) {
      var tpl = packageForm.dataset;
      var fill = function (s) { return (s || "").split("{plan}").join(plan).split("{price}").join(price); };
      var notice = packageForm.querySelector("p[data-package-notice]");
      if (notice) { notice.textContent = fill(tpl.pkgNotice); notice.hidden = false; }
      var hidden = packageForm.querySelector("input[name=paketa]");
      if (hidden) hidden.value = fill(tpl.pkgHidden) || plan;
      var subject = packageForm.querySelector("input[name=_subject]");
      if (subject) subject.value = fill(tpl.pkgSubject);
      var select = packageForm.querySelector("select[name=sherbimi]");
      if (select && tpl.pkgOption) {
        Array.prototype.forEach.call(select.options, function (option) {
          if (option.value === tpl.pkgOption || option.textContent === tpl.pkgOption) select.value = option.value;
        });
      }
      var textarea = packageForm.querySelector("textarea");
      if (textarea && !textarea.value) textarea.value = fill(tpl.pkgMessage);
    }

    /* ---- ...or a product demo from ?product=krakenos (ITD Labs pages) ---- */
    var productKey = params.get("product");
    var products = {};
    try { products = JSON.parse(packageForm.dataset.demoProducts || "{}"); } catch (error) { products = {}; }
    if (!plan && productKey && Object.prototype.hasOwnProperty.call(products, productKey)) {
      var d = packageForm.dataset;
      var product = products[productKey];
      var fillDemo = function (s) { return (s || "").split("{product}").join(product); };
      var demoNotice = packageForm.querySelector("p[data-package-notice]");
      if (demoNotice) { demoNotice.textContent = fillDemo(d.demoNotice); demoNotice.hidden = false; }
      var demoHidden = packageForm.querySelector("input[name=produkti]");
      if (demoHidden) demoHidden.value = product;
      var demoSubject = packageForm.querySelector("input[name=_subject]");
      if (demoSubject) demoSubject.value = fillDemo(d.demoSubject);
      var demoSelect = packageForm.querySelector("select[name=sherbimi]");
      if (demoSelect && d.demoOption) {
        Array.prototype.forEach.call(demoSelect.options, function (option) {
          if (option.value === d.demoOption) demoSelect.value = option.value;
        });
      }
      var demoText = packageForm.querySelector("textarea");
      if (demoText && !demoText.value) demoText.value = fillDemo(d.demoMessage);
    }
  }

  /* ---- "Open the chat" buttons (Kraken Communications page) -------------
     Shown only once the chat launcher exists, so the button never does nothing. */
  var chatButtons = doc.querySelectorAll("[data-open-chat]");
  if (chatButtons.length) {
    var findLauncher = function () { return doc.querySelector("#itd-kraken-chat button"); };
    var wireChat = function () {
      if (!findLauncher()) return false;
      Array.prototype.forEach.call(chatButtons, function (button) {
        button.hidden = false;
        button.addEventListener("click", function () {
          var launcher = findLauncher();
          if (!launcher) return;
          // The launcher toggles; never close a chat that is already open.
          if (launcher.getAttribute("aria-expanded") === "true") {
            var frame = doc.getElementById("itd-kraken-frame");
            if (frame) frame.focus();
          } else {
            launcher.click();
          }
        });
      });
      return true;
    };
    if (!wireChat()) window.addEventListener("load", wireChat, { once: true });
  }

  /* ---- Lightbox (native <dialog>) --------------------------------------- */
  Array.prototype.forEach.call(doc.querySelectorAll("[data-lightbox]"), function (button) {
    var dialog = doc.getElementById("lightbox-" + button.getAttribute("data-lightbox"));
    if (!dialog || typeof dialog.showModal !== "function") return;
    button.addEventListener("click", function () { dialog.showModal(); });
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog || event.target.closest("[data-lightbox-close]")) dialog.close();
    });
  });

  /* ---- Footer year -------------------------------------------------------- */
  Array.prototype.forEach.call(doc.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
