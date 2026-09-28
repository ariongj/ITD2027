(function () {
  "use strict";

  var FORM_ENDPOINT = "https://formspree.io/f/xpqypezj";
  var WHATSAPP_NUMBER = "38349573570";
  var BOOKING_LINK = "https://calendly.com/arion-gjonbalaj/30min";
  var lang = (document.documentElement.lang || "").toLowerCase();
  var isDe = lang.indexOf("de") === 0;
  var isEn = lang.indexOf("en") === 0;
  var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var pageFile = (window.location.pathname.split("/").pop() || "index").toLowerCase();
  var pageVariant = pageFile.indexOf("services") === 0 ? "services" : pageFile.indexOf("ai-agents") === 0 ? "ai" : pageFile.indexOf("projects") === 0 ? "projects" : pageFile.indexOf("about") === 0 ? "about" : pageFile.indexOf("contact") === 0 ? "contact" : "home";
  var copy = isDe ? {
    bookingLabel: "Termin buchen",
    defaultWhatsappMessage: "Hallo! Ich möchte mit IT Department über eine Website, Software oder IT-Support sprechen.",
    scrollTopLabel: "Nach oben",
    selectPlan: "Paket wählen",
    selectedPackage: "Ausgewähltes Paket",
    packageRequired: "Bitte füllen Sie Paket, Name, E-Mail und Telefonnummer vor dem Senden aus.",
    contactRequired: "Bitte füllen Sie alle Pflichtfelder vor dem Senden aus.",
    validEmail: "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
    validPhone: "Bitte geben Sie eine gültige Telefonnummer ein.",
    packageSuccess: "Ihre Paket-Anfrage wurde erfolgreich gesendet.",
    packageError: "Senden fehlgeschlagen. Bitte versuchen Sie es erneut oder schreiben Sie uns auf WhatsApp.",
    contactSuccess: "Ihre Nachricht wurde erfolgreich gesendet.",
    contactError: "Senden fehlgeschlagen. Bitte versuchen Sie es erneut oder schreiben Sie uns auf WhatsApp.",
    packageTitle: function (title) { return "Sie haben " + title + " gewählt."; },
    packageSummary: function (label, title, price) { return price ? "Ausgewähltes Paket: " + title + " (" + price + "). Hinterlassen Sie Ihre Kontaktdaten und wir melden uns mit den nächsten Schritten." : "Ausgewähltes Paket: " + title + ". Hinterlassen Sie Ihre Kontaktdaten und wir melden uns mit den nächsten Schritten."; },
    packageSubject: function (label) { return "Paket-Anfrage - " + label; },
    packageWhatsappPreview: function (title) { return "WhatsApp öffnet sich mit einer vorbereiteten Nachricht für das Paket " + title + "."; },
    packageWhatsappMessage: function (title) { return "Hallo! Ich interessiere mich für das Paket " + title + ". Können Sie mich bitte anrufen?"; }
  } : isEn ? {
    bookingLabel: "Book a call",
    defaultWhatsappMessage: "Hello! I would like to talk about a website, software, or IT support with IT Department.",
    scrollTopLabel: "Back to top",
    selectPlan: "Select plan",
    selectedPackage: "Selected package",
    packageRequired: "Please fill in the package, name, email, and phone number before submitting.",
    contactRequired: "Please fill in all required fields before submitting.",
    validEmail: "Please enter a valid email address.",
    validPhone: "Please enter a valid phone number.",
    packageSuccess: "Your package inquiry was sent successfully.",
    packageError: "Sending failed. Please try again or message us on WhatsApp.",
    contactSuccess: "Your message was sent successfully.",
    contactError: "Sending failed. Please try again or message us on WhatsApp.",
    packageTitle: function (title) { return "You selected " + title + "."; },
    packageSummary: function (label, title, price) { return price ? "Selected package: " + title + " (" + price + "). Leave your details and we will reply with the next steps." : "Selected package: " + title + ". Leave your details and we will reply with the next steps."; },
    packageSubject: function (label) { return "Package inquiry - " + label; },
    packageWhatsappPreview: function (title) { return "WhatsApp will open with a prepared message for the " + title + " package."; },
    packageWhatsappMessage: function (title) { return "Hello! I am interested in your " + title + " package. Could you please call me?"; }
  } : {
    bookingLabel: "Cakto takim",
    defaultWhatsappMessage: "Përshëndetje! Dua të flas për një faqe web, softuer ose mbështetje IT me IT Department.",
    scrollTopLabel: "Kthehu në krye",
    selectPlan: "Zgjidh planin",
    selectedPackage: "Paketa e zgjedhur",
    packageRequired: "Plotëso paketën, emrin, emailin dhe telefonin përpara dërgimit.",
    contactRequired: "Plotëso të gjitha fushat përpara dërgimit.",
    validEmail: "Vendos një email të vlefshëm.",
    validPhone: "Vendos një numër telefoni të vlefshëm.",
    packageSuccess: "Kërkesa për paketën u dërgua me sukses.",
    packageError: "Dërgimi dështoi. Provo përsëri ose na shkruaj në WhatsApp.",
    contactSuccess: "Mesazhi u dërgua me sukses.",
    contactError: "Dërgimi dështoi. Provo përsëri ose na shkruaj në WhatsApp.",
    packageTitle: function (title) { return "Ke zgjedhur " + title + "."; },
    packageSummary: function (label, title, price) { return price ? "Paketa e zgjedhur: " + title + " (" + price + "). Lër kontaktin dhe ne të kthehemi me hapat e radhës." : "Paketa e zgjedhur: " + title + ". Lër kontaktin dhe ne të kthehemi me hapat e radhës."; },
    packageSubject: function (label) { return "Kërkesë për paketë - " + label; },
    packageWhatsappPreview: function (title) { return "WhatsApp hapet me mesazh të gatshëm për paketën " + title + "."; },
    packageWhatsappMessage: function (title) { return "Përshëndetje! Jam i interesuar për paketën " + title + ". A mund të më telefononi, ju lutem?"; }
  };

  var WHATSAPP_URL = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(copy.defaultWhatsappMessage);

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  }

  function setStatus(node, message, className) {
    if (!node) return;
    node.textContent = message;
    node.className = "form-status";
    if (className) node.classList.add(className);
  }

  function applyActionLinks(scope) {
    scope = scope || document;
    scope.querySelectorAll("[data-booking-link]").forEach(function (link) {
      link.setAttribute("href", BOOKING_LINK);
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noreferrer noopener");
    });
    scope.querySelectorAll("[data-whatsapp-link], .whatsapp-button").forEach(function (link) {
      var href = link.getAttribute("href") || "";
      var isDefault = href === "https://wa.me/" + WHATSAPP_NUMBER || href === "https://wa.me/" + WHATSAPP_NUMBER + "/";
      if (!href || href === "#" || isDefault) link.setAttribute("href", WHATSAPP_URL);
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noreferrer noopener");
      if (/(button|utility-button|creative-button|ai-button|whatsapp-button)/.test(link.className || "")) link.classList.add("button-whatsapp");
    });
  }

  function setupMenu() {
    var menuToggle = document.querySelector("[data-menu-toggle]");
    var mobileMenu = document.getElementById("mobile-menu");
    if (!menuToggle || !mobileMenu) return;
    function close() {
      menuToggle.setAttribute("aria-expanded", "false");
      mobileMenu.hidden = true;
      mobileMenu.classList.remove("is-open");
      document.body.classList.remove("menu-open");
    }
    function open() {
      menuToggle.setAttribute("aria-expanded", "true");
      mobileMenu.hidden = false;
      mobileMenu.classList.add("is-open");
      document.body.classList.add("menu-open");
    }
    close();
    menuToggle.addEventListener("click", function () {
      menuToggle.getAttribute("aria-expanded") === "true" ? close() : open();
    });
    mobileMenu.querySelectorAll("[data-menu-link]").forEach(function (link) { link.addEventListener("click", close); });
    document.addEventListener("click", function (event) {
      if (mobileMenu.hidden || event.target.closest(".mobile-menu") || event.target.closest("[data-menu-toggle]")) return;
      close();
    });
    document.addEventListener("keydown", function (event) { if (event.key === "Escape") close(); });
    window.addEventListener("resize", function () { if (window.innerWidth > 720) close(); }, { passive: true });
  }

  function setupHeader() {
    var header = document.querySelector(".site-header");
    var condensed = false;
    var raf = 0;
    function sync() {
      raf = 0;
      var y = window.scrollY || document.documentElement.scrollTop;
      var enter = window.innerWidth <= 560 ? 26 : window.innerWidth <= 720 ? 34 : 88;
      var exit = window.innerWidth <= 560 ? 8 : window.innerWidth <= 720 ? 14 : 52;
      if (header) {
        if (!condensed && y > enter) condensed = true;
        else if (condensed && y < exit) condensed = false;
        header.classList.toggle("is-condensed", condensed);
      }
      document.body.classList.toggle("has-floating-cta", y > 120);
    }
    function queue() { if (!raf) raf = window.requestAnimationFrame(sync); }
    sync();
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue, { passive: true });
  }

  function setupUtilityCtas() {
    if (document.querySelector(".sticky-cta") || document.querySelector(".floating-cta-stack") || document.querySelector(".mobile-cta-bar")) return;
    var floating = document.createElement("div");
    floating.className = "floating-cta-stack";
    floating.innerHTML = '<a href="' + BOOKING_LINK + '" class="utility-button utility-book sticky-book-button" data-booking-link>' + copy.bookingLabel + '</a><a href="' + WHATSAPP_URL + '" class="utility-button utility-whatsapp button-whatsapp sticky-whatsapp-button" data-whatsapp-link>WhatsApp</a>';
    var mobileBar = document.createElement("div");
    mobileBar.className = "mobile-cta-bar";
    mobileBar.innerHTML = '<div class="mobile-cta-inner"><a href="' + BOOKING_LINK + '" class="utility-button utility-book" data-booking-link>' + copy.bookingLabel + '</a><a href="' + WHATSAPP_URL + '" class="utility-button utility-whatsapp button-whatsapp" data-whatsapp-link>WhatsApp</a></div>';
    document.body.appendChild(floating);
    document.body.appendChild(mobileBar);
    applyActionLinks(floating);
    applyActionLinks(mobileBar);
  }

  function setupScrollProgress() {
    var isCreativePage = document.body.classList.contains("creative-page");
    var isAiPage = document.body.classList.contains("ai-page");
    var gradientId = isCreativePage ? "progress-gradient-creative-lite" : isAiPage ? "progress-gradient-ai-lite" : "progress-gradient-lite";
    var gradientStops = isCreativePage
      ? '<stop offset="0%" stop-color="#ff8a1f"></stop><stop offset="55%" stop-color="#ff3f91"></stop><stop offset="100%" stop-color="#24f6ff"></stop>'
      : isAiPage
        ? '<stop offset="0%" stop-color="#b9ff5f"></stop><stop offset="50%" stop-color="#37f5ff"></stop><stop offset="100%" stop-color="#6c7dff"></stop>'
        : '<stop offset="0%" stop-color="#ffffff"></stop><stop offset="55%" stop-color="#ff6262"></stop><stop offset="100%" stop-color="#e00000"></stop>';
    var progress = document.querySelector(".progress-wrap");
    var markup = '<svg viewBox="-1 -1 102 102" aria-hidden="true"><defs><linearGradient id="' + gradientId + '" x1="0%" y1="0%" x2="100%" y2="100%">' + gradientStops + '</linearGradient></defs><path class="progress-wrap__bg" d="M50,1 a49,49 0 1,1 0,98 a49,49 0 1,1 0,-98"></path><path class="active-progress" d="M50,1 a49,49 0 1,1 0,98 a49,49 0 1,1 0,-98" style="stroke:url(#' + gradientId + ')"></path></svg><span class="progress-wrap__arrow" aria-hidden="true">&#8593;</span>';
    if (!progress) {
      progress = document.createElement("button");
      progress.type = "button";
      progress.className = "progress-wrap";
      document.body.appendChild(progress);
    }
    if (!progress.querySelector(".active-progress")) progress.innerHTML = markup;
    if (progress.tagName !== "BUTTON") {
      progress.setAttribute("role", "button");
      progress.tabIndex = 0;
    }
    progress.setAttribute("aria-label", copy.scrollTopLabel);
    var path = progress.querySelector(".active-progress");
    var pathLength = path && path.getTotalLength ? path.getTotalLength() : 0;
    var raf = 0;
    if (pathLength) {
      path.style.strokeDasharray = pathLength + " " + pathLength;
      path.style.strokeDashoffset = pathLength;
    }
    function update() {
      raf = 0;
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (pathLength) {
        var draw = scrollHeight > 0 ? pathLength - (scrollTop * pathLength / scrollHeight) : pathLength;
        path.style.strokeDashoffset = Math.max(draw, 0);
      }
      progress.classList.toggle("is-visible", scrollTop > 140);
    }
    function queue() { if (!raf) raf = window.requestAnimationFrame(update); }
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue, { passive: true });
    window.addEventListener("hashchange", queue);
    queue();
    window.setTimeout(queue, 140);
  }

  function setupAiStickyGuard() {
    if (!document.body.classList.contains("ai-page")) return;
    var sticky = document.querySelector(".ai-sticky-cta");
    var progress = document.querySelector(".progress-wrap");
    var sections = Array.from(document.querySelectorAll("#ai-agent-brief, .ai-footer"));
    if (!sticky || !sections.length) return;
    var active = new Set();
    function sync() {
      var hidden = active.size > 0;
      sticky.classList.toggle("is-section-hidden", hidden);
      if (progress) progress.classList.remove("is-section-hidden-mobile");
    }
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) { entry.isIntersecting ? active.add(entry.target) : active.delete(entry.target); });
        sync();
      }, { rootMargin: "0px 0px -16% 0px", threshold: 0.02 });
      sections.forEach(function (section) { observer.observe(section); });
    }
  }

  function setupCreativeLightboxes() {
    var lightboxes = Array.from(document.querySelectorAll(".creative-lightbox"));
    if (!lightboxes.length) return;
    var active = null;
    lightboxes.forEach(function (box) {
      box.setAttribute("aria-hidden", "true");
      document.body.appendChild(box);
    });
    function close() {
      if (!active) return;
      active.classList.remove("is-open");
      active.setAttribute("aria-hidden", "true");
      document.body.classList.remove("creative-lightbox-open");
      active = null;
      history.replaceState(null, "", window.location.pathname + window.location.search + "#creative-showcase");
    }
    function open(box) {
      if (!box) return;
      if (active && active !== box) active.classList.remove("is-open");
      active = box;
      box.classList.add("is-open");
      box.setAttribute("aria-hidden", "false");
      document.body.classList.add("creative-lightbox-open");
      history.replaceState(null, "", window.location.pathname + window.location.search + "#" + box.id);
    }
    document.querySelectorAll('a[href^="#"][href$="-brandbook-preview"]').forEach(function (link) {
      link.addEventListener("click", function (event) {
        var target = document.querySelector(link.getAttribute("href"));
        if (!target) return;
        event.preventDefault();
        open(target);
      });
    });
    document.querySelectorAll(".creative-lightbox-backdrop, .creative-lightbox-close").forEach(function (control) {
      control.addEventListener("click", function (event) { event.preventDefault(); close(); });
    });
    document.addEventListener("keydown", function (event) { if (event.key === "Escape") close(); });
  }

  function setupPackageTools() {
    var buttons = Array.from(document.querySelectorAll("[data-package-select]"));
    var inquiry = document.getElementById("package-inquiry");
    var form = document.getElementById("package-inquiry-form");
    var status = document.getElementById("package-form-status");
    if (!buttons.length && !form) return;
    var homePath = isDe ? "/de" : isEn ? "/en" : "/";
    var isHome = ["/", "/en", "/de"].indexOf(window.location.pathname.toLowerCase()) !== -1;
    function dataFrom(button) {
      var label = button && button.dataset.packageLabel || "Package";
      return {
        label: label,
        title: button && button.dataset.packageTitle || label,
        price: button && button.dataset.packagePrice || "",
        button: button
      };
    }
    function packageWhatsappUrl(title) {
      return "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(copy.packageWhatsappMessage(title));
    }
    function selectPackage(data) {
      if (!isHome || !inquiry) {
        var url = new URL(homePath, window.location.origin);
        url.searchParams.set("package", data.label);
        url.searchParams.set("title", data.title);
        if (data.price) url.searchParams.set("price", data.price);
        url.hash = "package-inquiry";
        window.location.href = url.toString();
        return;
      }
      buttons.forEach(function (item) {
        var selected = item === data.button;
        item.classList.toggle("is-selected", selected);
        item.setAttribute("aria-pressed", selected ? "true" : "false");
        item.textContent = selected ? copy.selectedPackage : copy.selectPlan;
      });
      inquiry.hidden = false;
      inquiry.classList.add("has-selection");
      var title = document.getElementById("package-inquiry-title");
      var summary = document.getElementById("package-inquiry-summary");
      var tag = document.getElementById("package-inquiry-tag");
      var price = document.getElementById("package-inquiry-price");
      var hiddenPackage = document.getElementById("package-hidden-package");
      var hiddenSubject = document.getElementById("package-hidden-subject");
      var whatsapp = document.getElementById("package-whatsapp-link");
      var quick = document.getElementById("package-whatsapp-quick");
      var preview = document.getElementById("package-whatsapp-preview");
      if (title) title.textContent = copy.packageTitle(data.title);
      if (summary) summary.textContent = copy.packageSummary(data.label, data.title, data.price);
      if (tag) tag.textContent = data.label;
      if (price) price.textContent = data.price || data.title;
      if (hiddenPackage) hiddenPackage.value = data.label + " - " + data.title;
      if (hiddenSubject) hiddenSubject.value = copy.packageSubject(data.label);
      if (whatsapp) whatsapp.href = packageWhatsappUrl(data.title);
      if (quick) quick.href = packageWhatsappUrl(data.title);
      if (preview) preview.textContent = copy.packageWhatsappPreview(data.title);
      setStatus(status, "", "");
      inquiry.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "start" });
    }
    buttons.forEach(function (button) { button.addEventListener("click", function () { selectPackage(dataFrom(button)); }); });
    var finder = document.querySelector("[data-package-finder]");
    if (finder) {
      var answers = Array.from(finder.querySelectorAll("[data-package-answer]"));
      var result = finder.querySelector("[data-package-recommendation]");
      var labelNode = finder.querySelector("[data-package-recommendation-label]");
      var copyNode = finder.querySelector("[data-package-recommendation-copy]");
      var apply = finder.querySelector("[data-package-finder-apply]");
      var selected = new Map();
      var current = "Business";
      function updateFinder() {
        var scores = { Starter: 0, Business: 0, Enterprise: 0 };
        selected.forEach(function (target) { if (scores[target] !== undefined) scores[target] += 1; });
        current = ["Business", "Enterprise", "Starter"].sort(function (a, b) { return scores[b] - scores[a]; })[0];
        var matching = buttons.find(function (button) { return (button.dataset.packageLabel || "") === current; });
        if (result) result.hidden = false;
        if (labelNode) labelNode.textContent = current;
        if (copyNode) copyNode.textContent = finder.dataset["copy" + current] || "";
        if (apply) apply.textContent = isDe ? "Weiter mit " + current : isEn ? "Continue with " + current : "Vazhdo me " + current;
        if (matching && apply) apply.setAttribute("aria-label", (matching.dataset.packageTitle || current) + " " + (matching.dataset.packagePrice || ""));
      }
      answers.forEach(function (answer) {
        answer.addEventListener("click", function () {
          var question = answer.closest("[data-package-question]");
          var key = question && question.dataset.packageQuestion || answer.textContent.trim();
          if (question) question.querySelectorAll("[data-package-answer]").forEach(function (item) {
            item.classList.toggle("is-selected", item === answer);
            item.setAttribute("aria-pressed", item === answer ? "true" : "false");
          });
          selected.set(key, answer.dataset.packageTarget || "Business");
          updateFinder();
        });
      });
      if (apply) apply.addEventListener("click", function () {
        var matching = buttons.find(function (button) { return (button.dataset.packageLabel || "") === current; });
        if (matching) selectPackage(dataFrom(matching));
      });
    }
    if (form && status) setupPackageForm(form, status);
  }

  function setupPackageForm(form, status) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      if (!data.paketa || !data.emri || !data.email || !data.telefoni) return setStatus(status, copy.packageRequired, "error");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return setStatus(status, copy.validEmail, "error");
      if (String(data.telefoni).replace(/\D/g, "").length < 7) return setStatus(status, copy.validPhone, "error");
      submitForm(form, status, copy.packageSuccess, copy.packageError);
    });
  }

  function setupContactForm() {
    var form = document.getElementById("contact-form");
    var status = document.getElementById("form-status");
    if (!form || !status) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      if (!data.emri || !data.email || !data.kompania || !data.sherbimi) return setStatus(status, copy.contactRequired, "error");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return setStatus(status, copy.validEmail, "error");
      submitForm(form, status, copy.contactSuccess, copy.contactError);
    });
  }

  function submitForm(form, status, success, error) {
    if (form.dataset.submitting === "true") return;
    var submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    form.dataset.submitting = "true";
    form.setAttribute("aria-busy", "true");
    if (submitButton) submitButton.disabled = true;
    setStatus(status, "", "");
    fetch(FORM_ENDPOINT, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: new FormData(form)
    }).then(function (response) {
      if (!response.ok) throw new Error("submit failed");
      if (form.id === "contact-form") {
        try { window.ITDAnalytics?.reportLeadSuccess("contact-form", response); } catch (trackingError) { /* Tracking must not interrupt form success. */ }
      }
      form.reset();
      setStatus(status, success, "success");
    }).catch(function () {
      setStatus(status, error, "error");
    }).finally(function () {
      form.dataset.submitting = "false";
      form.removeAttribute("aria-busy");
      if (submitButton) submitButton.disabled = false;
    });
  }

  function setupButtons() {
    document.querySelectorAll(".button, .button-ghost, .utility-button, .nav-toggle, .creative-button, .ai-button").forEach(function (button) {
      button.addEventListener("pointerdown", function () { button.classList.add("is-pressed"); }, { passive: true });
      ["pointerup", "pointerleave", "blur"].forEach(function (name) {
        button.addEventListener(name, function () { button.classList.remove("is-pressed"); }, { passive: true });
      });
    });
    document.querySelectorAll(".progress-wrap").forEach(function (button) {
      button.setAttribute("aria-label", copy.scrollTopLabel);
      button.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
      });
      button.addEventListener("keydown", function (event) {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
      });
    });
  }

  onReady(function () {
    document.body.dataset.pageVariant = pageVariant;
    document.documentElement.classList.add("app-lite-ready");
    setupMenu();
    setupHeader();
    setupUtilityCtas();
    applyActionLinks(document);
    setupScrollProgress();
    setupAiStickyGuard();
    setupCreativeLightboxes();
    setupPackageTools();
    setupContactForm();
    setupButtons();
  });
})();
