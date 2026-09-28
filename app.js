const FORM_ENDPOINT = "https://formspree.io/f/xpqypezj";
const WHATSAPP_NUMBER = "38349573570";
const BOOKING_LINK = "https://calendly.com/arion-gjonbalaj/30min";
const pageLanguage = document.documentElement.lang.toLowerCase();
const isGermanPage = pageLanguage.startsWith("de");
const isEnglishPage = pageLanguage.startsWith("en");
const copy = isGermanPage
  ? {
      bookingLabel: "Termin buchen",
      defaultWhatsappMessage: "Hallo! Ich möchte mit IT Department über eine Website, Software oder IT-Support sprechen.",
      scrollTopLabel: "Nach oben",
      selectPlan: "Paket wählen",
      selectedPackage: "Ausgewähltes Paket",
      packageTitle: (title) => `Sie haben ${title} gewählt.`,
      packageSummary: (label, title, price) =>
        price
          ? `Ausgewähltes Paket: ${title} (${price}). Hinterlassen Sie Ihre Kontaktdaten und wir melden uns mit den nächsten Schritten.`
          : `Ausgewähltes Paket: ${title}. Hinterlassen Sie Ihre Kontaktdaten und wir melden uns mit den nächsten Schritten.`,
      packageSubject: (label) => `Paket-Anfrage - ${label}`,
      packageWhatsappPreview: (title) => `WhatsApp öffnet sich mit einer vorbereiteten Nachricht für das Paket ${title}.`,
      packageWhatsappMessage: (title) => `Hallo! Ich interessiere mich für das Paket ${title}. Können Sie mich bitte anrufen?`,
      packageRequired: "Bitte füllen Sie Paket, Name, E-Mail und Telefonnummer vor dem Senden aus.",
      validEmail: "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
      validPhone: "Bitte geben Sie eine gültige Telefonnummer ein.",
      packageSuccess: "Ihre Paket-Anfrage wurde erfolgreich gesendet. Wir melden uns so schnell wie möglich.",
      packageError: "Senden fehlgeschlagen. Bitte versuchen Sie es erneut oder schreiben Sie uns auf WhatsApp zu diesem Paket.",
      contactRequired: "Bitte füllen Sie alle Pflichtfelder vor dem Senden aus.",
      contactSuccess: "Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns so schnell wie möglich.",
      contactError: "Senden fehlgeschlagen. Bitte versuchen Sie es erneut oder schreiben Sie uns auf WhatsApp."
    }
  : isEnglishPage
    ? {
      bookingLabel: "Book a call",
      defaultWhatsappMessage: "Hello! I would like to talk about a website, software, or IT support with IT Department.",
      scrollTopLabel: "Back to top",
      selectPlan: "Select plan",
      selectedPackage: "Selected package",
      packageTitle: (title) => `You selected ${title}.`,
      packageSummary: (label, title, price) =>
        price
          ? `Selected package: ${title} (${price}). Leave your details and we will reply with the next steps.`
          : `Selected package: ${title}. Leave your details and we will reply with the next steps.`,
      packageSubject: (label) => `Package inquiry - ${label}`,
      packageWhatsappPreview: (title) => `WhatsApp will open with a prepared message for the ${title} package.`,
      packageWhatsappMessage: (title) => `Hello! I am interested in your ${title} package. Could you please call me?`,
      packageRequired: "Please fill in the package, name, email, and phone number before submitting.",
      validEmail: "Please enter a valid email address.",
      validPhone: "Please enter a valid phone number.",
      packageSuccess: "Your package inquiry was sent successfully. We will contact you as soon as possible.",
      packageError: "Sending failed. Please try again or message us on WhatsApp for this package.",
      contactRequired: "Please fill in all required fields before submitting.",
      contactSuccess: "Your message was sent successfully. We will contact you as soon as possible.",
      contactError: "Sending failed. Please try again or message us on WhatsApp."
    }
  : {
      bookingLabel: "Cakto takim",
      defaultWhatsappMessage: "Përshëndetje! Dua të flas për një faqe web, softuer ose mbështetje IT me IT Department.",
      scrollTopLabel: "Kthehu në krye",
      selectPlan: "Zgjidh planin",
      selectedPackage: "Paketa e zgjedhur",
      packageTitle: (title) => `Ke zgjedhur ${title}.`,
      packageSummary: (label, title, price) =>
        price
          ? `Paketa e zgjedhur: ${title} (${price}). Lër kontaktin dhe ne të kthehemi me hapat e radhës.`
          : `Paketa e zgjedhur: ${title}. Lër kontaktin dhe ne të kthehemi me hapat e radhës.`,
      packageSubject: (label) => `Kërkesë për paketë - ${label}`,
      packageWhatsappPreview: (title) => `WhatsApp-i hapet me mesazh të gatshëm për paketën ${title}.`,
      packageWhatsappMessage: (title) => `Përshëndetje! Jam i interesuar për paketën ${title}. A mund të më telefononi, ju lutem?`,
      packageRequired: "Plotëso paketën, emrin, emailin dhe telefonin përpara dërgimit.",
      validEmail: "Vendos një email të vlefshëm.",
      validPhone: "Vendos një numër telefoni të vlefshëm.",
      packageSuccess: "Kërkesa për paketën u dërgua me sukses. Do të të kontaktojmë sa më shpejt.",
      packageError: "Dërgimi dështoi. Provo përsëri ose na shkruaj në WhatsApp për këtë paketë.",
      contactRequired: "Plotëso të gjitha fushat përpara dërgimit.",
      contactSuccess: "Mesazhi u dërgua me sukses. Do t'ju kontaktojmë sa më shpejt.",
      contactError: "Dërgimi dështoi. Provo përsëri ose na shkruaj në WhatsApp."
    };
const WHATSAPP_MESSAGE = encodeURIComponent(copy.defaultWhatsappMessage);
const WHATSAPP_URL = `https://wa.me/${WHATSAPP_NUMBER}?text=${WHATSAPP_MESSAGE}`;
const BOOKING_LABEL = copy.bookingLabel;
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const pageFile = (window.location.pathname.split("/").pop() || "index").toLowerCase();
const pageVariant = pageFile.startsWith("services")
  ? "services"
  : pageFile.startsWith("ai-agents")
    ? "ai"
    : pageFile.startsWith("projects")
      ? "projects"
      : pageFile.startsWith("about")
        ? "about"
        : pageFile.startsWith("contact")
          ? "contact"
          : "home";

document.body.dataset.pageVariant = pageVariant;

const creativeLightboxes = [...document.querySelectorAll(".creative-lightbox")];
if (creativeLightboxes.length) {
  const showcaseHash = "#creative-showcase";
  let activeCreativeLightbox = null;

  creativeLightboxes.forEach((lightbox) => {
    lightbox.setAttribute("aria-hidden", "true");
    document.body.appendChild(lightbox);
  });

  function setCreativeHash(hash) {
    const nextUrl = `${window.location.pathname}${window.location.search}${hash}`;
    window.history.replaceState(null, "", nextUrl);
  }

  function closeCreativeLightbox() {
    if (!activeCreativeLightbox) return;
    activeCreativeLightbox.classList.remove("is-open");
    activeCreativeLightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("creative-lightbox-open");
    activeCreativeLightbox = null;
    setCreativeHash(showcaseHash);
  }

  function openCreativeLightbox(lightbox) {
    if (!lightbox) return;
    if (activeCreativeLightbox && activeCreativeLightbox !== lightbox) {
      activeCreativeLightbox.classList.remove("is-open");
      activeCreativeLightbox.setAttribute("aria-hidden", "true");
    }
    activeCreativeLightbox = lightbox;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("creative-lightbox-open");
    setCreativeHash(`#${lightbox.id}`);
  }

  document.querySelectorAll('a[href^="#"][href$="-brandbook-preview"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.querySelector(link.getAttribute("href"));
      if (!target) return;
      event.preventDefault();
      openCreativeLightbox(target);
    });
  });

  document.querySelectorAll(".creative-lightbox-backdrop, .creative-lightbox-close").forEach((control) => {
    control.addEventListener("click", (event) => {
      event.preventDefault();
      closeCreativeLightbox();
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeCreativeLightbox();
    }
  });

  if (window.location.hash.length > 1) {
    const initialLightbox = document.querySelector(window.location.hash);
    if (initialLightbox?.classList.contains("creative-lightbox")) {
      openCreativeLightbox(initialLightbox);
    }
  }
}

const reactivePanels = [...document.querySelectorAll(".reactive-panel")];
let activeReactivePanel = null;
let reactivePointerEvent = null;
let reactivePointerRaf = 0;

function clearHotPanels() {
  if (!activeReactivePanel) return;
  activeReactivePanel.classList.remove("is-hot");
  activeReactivePanel.style.setProperty("--panel-tilt-x", "0px");
  activeReactivePanel.style.setProperty("--panel-tilt-y", "0px");
  activeReactivePanel = null;
}

function applyReactivePointer() {
  reactivePointerRaf = 0;
  const event = reactivePointerEvent;
  if (!event) return;

  const hovered = event.target instanceof Element ? event.target.closest(".reactive-panel") : null;
  const previousPanel = activeReactivePanel;
  const nextPanel = hovered;
  const rect = nextPanel ? nextPanel.getBoundingClientRect() : null;

  if (previousPanel !== nextPanel) {
    if (previousPanel) {
      previousPanel.classList.remove("is-hot");
      previousPanel.style.setProperty("--panel-tilt-x", "0px");
      previousPanel.style.setProperty("--panel-tilt-y", "0px");
    }
    activeReactivePanel = nextPanel;
    if (activeReactivePanel) activeReactivePanel.classList.add("is-hot");
  }

  if (activeReactivePanel && rect) {
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    activeReactivePanel.style.setProperty("--local-glow-x", x + "%");
    activeReactivePanel.style.setProperty("--local-glow-y", y + "%");
    activeReactivePanel.style.setProperty("--panel-tilt-x", ((x - 50) / 24) + "px");
    activeReactivePanel.style.setProperty("--panel-tilt-y", ((y - 50) / 24) + "px");
  }

  document.documentElement.style.setProperty("--page-glow-x", (event.clientX / window.innerWidth * 100) + "%");
}

document.addEventListener("pointermove", (event) => {
  reactivePointerEvent = event;
  if (!reactivePointerRaf) {
    reactivePointerRaf = window.requestAnimationFrame(applyReactivePointer);
  }
}, { passive: true });

document.addEventListener("pointerleave", clearHotPanels);

const menuToggle = document.querySelector("[data-menu-toggle]");
const mobileMenu = document.getElementById("mobile-menu");
const siteHeader = document.querySelector(".site-header");
let headerCondensed = false;

function syncHeaderCondensed() {
  const enterThreshold = window.innerWidth <= 560 ? 26 : window.innerWidth <= 720 ? 34 : 88;
  const exitThreshold = window.innerWidth <= 560 ? 8 : window.innerWidth <= 720 ? 14 : 52;
  const y = window.scrollY || document.documentElement.scrollTop;

  if (siteHeader) {
    if (!headerCondensed && y > enterThreshold) {
      headerCondensed = true;
    } else if (headerCondensed && y < exitThreshold) {
      headerCondensed = false;
    }

    siteHeader.classList.toggle("is-condensed", headerCondensed);
  }

  document.body.classList.toggle("has-floating-cta", y > 120);
}

syncHeaderCondensed();
window.addEventListener("scroll", syncHeaderCondensed, { passive: true });

function closeMobileMenu() {
  if (!menuToggle || !mobileMenu) return;
  menuToggle.setAttribute("aria-expanded", "false");
  mobileMenu.hidden = true;
  mobileMenu.classList.remove("is-open");
  document.body.classList.remove("menu-open");
}

function openMobileMenu() {
  if (!menuToggle || !mobileMenu) return;
  menuToggle.setAttribute("aria-expanded", "true");
  mobileMenu.hidden = false;
  mobileMenu.classList.add("is-open");
  document.body.classList.add("menu-open");
}

if (menuToggle && mobileMenu) {
  closeMobileMenu();

  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    if (isOpen) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  });

  mobileMenu.querySelectorAll("[data-menu-link]").forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });

  document.addEventListener("click", (event) => {
    if (mobileMenu.hidden) return;
    if (event.target.closest(".mobile-menu") || event.target.closest("[data-menu-toggle]")) return;
    closeMobileMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMobileMenu();
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 720) closeMobileMenu();
    syncHeaderCondensed();
  });
}

function applyActionLinks(scope = document) {
  scope.querySelectorAll("[data-booking-link]").forEach((link) => {
    link.setAttribute("href", BOOKING_LINK);
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noreferrer noopener");
  });

  scope.querySelectorAll("[data-whatsapp-link], .whatsapp-button").forEach((link) => {
    if (link.classList.contains("button") || link.classList.contains("button-ghost") || link.classList.contains("utility-button") || link.classList.contains("creative-button") || link.classList.contains("ai-button") || link.classList.contains("whatsapp-button")) {
      link.classList.add("button-whatsapp");
    }
    const currentHref = link.getAttribute("href") || "";
    const isDefaultWhatsapp = currentHref === `https://wa.me/${WHATSAPP_NUMBER}` || currentHref === `https://wa.me/${WHATSAPP_NUMBER}/`;
    if (!currentHref || currentHref === "#" || isDefaultWhatsapp) {
      link.setAttribute("href", WHATSAPP_URL);
    }
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noreferrer noopener");
  });
}

function mountUtilityCtas() {
  if (!document.body) return;
  if (document.querySelector(".sticky-cta") || document.querySelector(".floating-cta-stack") || document.querySelector(".mobile-cta-bar")) return;

  const floating = document.createElement("div");
  floating.className = "floating-cta-stack";
  floating.innerHTML = `
    <a href="${BOOKING_LINK}" class="utility-button utility-book sticky-book-button" data-booking-link>${BOOKING_LABEL}</a>
    <a href="${WHATSAPP_URL}" class="utility-button utility-whatsapp button-whatsapp sticky-whatsapp-button" data-whatsapp-link>WhatsApp</a>
  `;

  const mobileBar = document.createElement("div");
  mobileBar.className = "mobile-cta-bar";
  mobileBar.innerHTML = `
    <div class="mobile-cta-inner">
      <a href="${BOOKING_LINK}" class="utility-button utility-book" data-booking-link>${BOOKING_LABEL}</a>
      <a href="${WHATSAPP_URL}" class="utility-button utility-whatsapp button-whatsapp" data-whatsapp-link>WhatsApp</a>
    </div>
  `;

  document.body.appendChild(floating);
  document.body.appendChild(mobileBar);
  applyActionLinks(floating);
  applyActionLinks(mobileBar);
}

mountUtilityCtas();
applyActionLinks();

function mountScrollProgress() {
  if (!document.body) return;
  const isCreativePage = document.body.classList.contains("creative-page");
  const isAiPage = document.body.classList.contains("ai-page");
  const gradientId = isCreativePage ? "progress-gradient-creative" : isAiPage ? "progress-gradient-ai" : "progress-gradient";
  const gradientStops = isCreativePage
    ? `
          <stop offset="0%" stop-color="#ffb000"></stop>
          <stop offset="50%" stop-color="#ff3f91"></stop>
          <stop offset="100%" stop-color="#24f6ff"></stop>
        `
    : isAiPage
      ? `
          <stop offset="0%" stop-color="#b9ff5f"></stop>
          <stop offset="50%" stop-color="#37f5ff"></stop>
          <stop offset="100%" stop-color="#6c7dff"></stop>
        `
    : `
          <stop offset="0%" stop-color="#ffffff"></stop>
          <stop offset="55%" stop-color="#ff6262"></stop>
          <stop offset="100%" stop-color="#e00000"></stop>
        `;

  let progressWrap = document.querySelector(".progress-wrap");
  const progressMarkup = `
    <svg viewBox="-1 -1 102 102" aria-hidden="true">
      <defs>
        <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="100%">
          ${gradientStops}
        </linearGradient>
      </defs>
      <path class="progress-wrap__bg" d="M50,1 a49,49 0 1,1 0,98 a49,49 0 1,1 0,-98"></path>
      <path class="active-progress" d="M50,1 a49,49 0 1,1 0,98 a49,49 0 1,1 0,-98" style="stroke:url(#${gradientId})"></path>
    </svg>
    <span class="progress-wrap__arrow" aria-hidden="true">&#8593;</span>
  `;

  if (!progressWrap) {
    progressWrap = document.createElement("button");
    progressWrap.type = "button";
    progressWrap.className = "progress-wrap";
    progressWrap.innerHTML = progressMarkup;
    document.body.appendChild(progressWrap);
  } else if (!progressWrap.querySelector(".active-progress")) {
    progressWrap.innerHTML = progressMarkup;
  }

  if (progressWrap.tagName !== "BUTTON") {
    progressWrap.setAttribute("role", "button");
    progressWrap.tabIndex = 0;
  }

  progressWrap.setAttribute("aria-label", copy.scrollTopLabel);

  const progressPath = progressWrap.querySelector(".active-progress");
  if (!progressPath) return;
  const pathLength = progressPath.getTotalLength();
  let rafId = 0;

  progressPath.style.strokeDasharray = `${pathLength} ${pathLength}`;
  progressPath.style.strokeDashoffset = `${pathLength}`;

  const updateProgress = () => {
    rafId = 0;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const draw = scrollHeight > 0 ? pathLength - (scrollTop * pathLength / scrollHeight) : pathLength;

    progressPath.style.strokeDashoffset = `${Math.max(draw, 0)}`;
    progressWrap.classList.toggle("is-visible", scrollTop > 140);
  };

  const queueUpdate = () => {
    if (rafId) return;
    rafId = window.requestAnimationFrame(updateProgress);
  };

  progressWrap.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
  });
  progressWrap.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
  });

  window.addEventListener("scroll", queueUpdate, { passive: true });
  window.addEventListener("resize", queueUpdate);
  window.addEventListener("hashchange", queueUpdate);
  queueUpdate();
  window.setTimeout(queueUpdate, 120);
  window.setTimeout(queueUpdate, 420);
}

mountScrollProgress();

function mountAiStickyGuard() {
  if (!document.body.classList.contains("ai-page")) return;
  const sticky = document.querySelector(".ai-sticky-cta");
  const progressWrap = document.querySelector(".progress-wrap");
  const guardedSections = [...document.querySelectorAll("#ai-agent-brief, .ai-footer")];
  if (!sticky || !guardedSections.length) return;

  const activeSections = new Set();
  const syncSticky = () => {
    const shouldHide = activeSections.size > 0;
    sticky.classList.toggle("is-section-hidden", shouldHide);
    progressWrap?.classList.remove("is-section-hidden-mobile");
  };

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeSections.add(entry.target);
        } else {
          activeSections.delete(entry.target);
        }
      });
      syncSticky();
    }, { rootMargin: "0px 0px -16% 0px", threshold: 0.02 });

    guardedSections.forEach((section) => observer.observe(section));
    return;
  }

  let rafId = 0;
  const queueSync = () => {
    if (rafId) return;
    rafId = window.requestAnimationFrame(() => {
      rafId = 0;
      activeSections.clear();
      guardedSections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.84 && rect.bottom > 0) {
          activeSections.add(section);
        }
      });
      syncSticky();
    });
  };

  window.addEventListener("scroll", queueSync, { passive: true });
  window.addEventListener("resize", queueSync);
  queueSync();
  window.setTimeout(queueSync, 400);
}

mountAiStickyGuard();

function mountPageHeroMotion() {
  if (pageVariant === "home") return;

  const heroSection = document.querySelector(".section.hero");
  if (!heroSection || heroSection.querySelector(".page-hero-motion")) return;

  const panel = document.createElement("div");
  panel.className = `page-hero-motion page-hero-motion--${pageVariant}`;
  panel.setAttribute("aria-hidden", "true");

  const sharedMotion = `
    <span class="hero-motion-data-rain hero-motion-data-rain--one"></span>
    <span class="hero-motion-data-rain hero-motion-data-rain--two"></span>
    <span class="hero-motion-signal-orbit hero-motion-signal-orbit--one"></span>
    <span class="hero-motion-signal-orbit hero-motion-signal-orbit--two"></span>
    <span class="hero-motion-spark hero-motion-spark--one"></span>
    <span class="hero-motion-spark hero-motion-spark--two"></span>
  `;

  const variants = {
    services: `
      ${sharedMotion}
      <span class="hero-motion-grid"></span>
      <span class="hero-motion-gear hero-motion-gear--lg"></span>
      <span class="hero-motion-gear hero-motion-gear--sm"></span>
      <span class="hero-motion-service-bar hero-motion-service-bar--1"></span>
      <span class="hero-motion-service-bar hero-motion-service-bar--2"></span>
      <span class="hero-motion-service-bar hero-motion-service-bar--3"></span>
      <span class="hero-motion-service-route"></span>
      <span class="hero-motion-service-node hero-motion-service-node--1"></span>
      <span class="hero-motion-service-node hero-motion-service-node--2"></span>
      <span class="hero-motion-service-node hero-motion-service-node--3"></span>
      <div class="hero-motion-console hero-motion-console--services">
        <span class="hero-motion-console-title">Flow</span>
        <span class="hero-motion-console-bar hero-motion-console-bar--1"></span>
        <span class="hero-motion-console-bar hero-motion-console-bar--2"></span>
        <span class="hero-motion-console-bar hero-motion-console-bar--3"></span>
      </div>
    `,
    projects: `
      ${sharedMotion}
      <span class="hero-motion-grid"></span>
      <span class="hero-motion-radar-ring hero-motion-radar-ring--1"></span>
      <span class="hero-motion-radar-ring hero-motion-radar-ring--2"></span>
      <span class="hero-motion-radar-ring hero-motion-radar-ring--3"></span>
      <span class="hero-motion-radar-sweep"></span>
      <span class="hero-motion-radar-target hero-motion-radar-target--1"></span>
      <span class="hero-motion-radar-target hero-motion-radar-target--2"></span>
      <span class="hero-motion-radar-target hero-motion-radar-target--3"></span>
      <span class="hero-motion-radar-line"></span>
      <div class="hero-motion-console hero-motion-console--projects">
        <span class="hero-motion-console-title">Track</span>
        <span class="hero-motion-console-line hero-motion-console-line--1"></span>
        <span class="hero-motion-console-line hero-motion-console-line--2"></span>
        <span class="hero-motion-console-line hero-motion-console-line--3"></span>
      </div>
    `,
    about: `
      ${sharedMotion}
      <span class="hero-motion-grid"></span>
      <span class="hero-motion-about-orbit hero-motion-about-orbit--1"></span>
      <span class="hero-motion-about-orbit hero-motion-about-orbit--2"></span>
      <span class="hero-motion-about-link"></span>
      <span class="hero-motion-gear hero-motion-gear--lg"></span>
      <span class="hero-motion-gear hero-motion-gear--sm"></span>
      <span class="hero-motion-about-node hero-motion-about-node--1"></span>
      <span class="hero-motion-about-node hero-motion-about-node--2"></span>
      <span class="hero-motion-about-node hero-motion-about-node--3"></span>
      <div class="hero-motion-console hero-motion-console--about">
        <span class="hero-motion-console-title">Team</span>
        <span class="hero-motion-console-link"></span>
        <span class="hero-motion-console-node hero-motion-console-node--1"></span>
        <span class="hero-motion-console-node hero-motion-console-node--2"></span>
        <span class="hero-motion-console-node hero-motion-console-node--3"></span>
      </div>
    `,
    contact: `
      ${sharedMotion}
      <span class="hero-motion-grid"></span>
      <span class="hero-motion-contact-core"></span>
      <span class="hero-motion-contact-ring hero-motion-contact-ring--1"></span>
      <span class="hero-motion-contact-ring hero-motion-contact-ring--2"></span>
      <span class="hero-motion-contact-ring hero-motion-contact-ring--3"></span>
      <span class="hero-motion-contact-rail"></span>
      <span class="hero-motion-contact-packet hero-motion-contact-packet--1"></span>
      <span class="hero-motion-contact-packet hero-motion-contact-packet--2"></span>
      <span class="hero-motion-contact-packet hero-motion-contact-packet--3"></span>
      <div class="hero-motion-console hero-motion-console--contact">
        <span class="hero-motion-console-title">Link</span>
        <span class="hero-motion-console-wave hero-motion-console-wave--1"></span>
        <span class="hero-motion-console-wave hero-motion-console-wave--2"></span>
        <span class="hero-motion-console-wave hero-motion-console-wave--3"></span>
        <span class="hero-motion-console-wave hero-motion-console-wave--4"></span>
      </div>
    `
  };

  panel.innerHTML = variants[pageVariant] || "";
  heroSection.appendChild(panel);
  document.body.classList.add("has-hero-motion");
}

mountPageHeroMotion();

function mountBuildMachineStage(buildLab) {
  const browserLayout = buildLab.querySelector(".build-browser-layout");
  if (!browserLayout || browserLayout.querySelector(".build-machine-stage")) return;

  const stage = document.createElement("div");
  stage.className = "build-machine-stage";
  stage.setAttribute("aria-hidden", "true");
  stage.innerHTML = `
    <span class="machine-stage-grid"></span>
    <span class="machine-core-ring machine-core-ring--one"></span>
    <span class="machine-core-ring machine-core-ring--two"></span>
    <span class="machine-gear machine-gear--lg"></span>
    <span class="machine-gear machine-gear--sm"></span>
    <span class="machine-gear machine-gear--micro"></span>
    <span class="machine-pulse machine-pulse--one"></span>
    <span class="machine-pulse machine-pulse--two"></span>
    <span class="machine-lane machine-lane--one"></span>
    <span class="machine-lane machine-lane--two"></span>
    <span class="machine-packet machine-packet--one"></span>
    <span class="machine-packet machine-packet--two"></span>
    <span class="machine-packet machine-packet--three"></span>
    <span class="machine-spark machine-spark--one"></span>
    <span class="machine-spark machine-spark--two"></span>
    <span class="machine-spark machine-spark--three"></span>
    <span class="machine-part machine-part--one"></span>
    <span class="machine-part machine-part--two"></span>
    <span class="machine-part machine-part--three"></span>
    <span class="machine-belt"></span>
    <div class="machine-arm">
      <span class="machine-arm-joint"></span>
      <span class="machine-arm-tip"></span>
    </div>
    <div class="machine-ledger">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="machine-rail">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
  `;

  browserLayout.appendChild(stage);
}

function mountBuildLab() {
  const buildLab = document.querySelector("[data-build-lab]");
  if (!buildLab) return;

  mountBuildMachineStage(buildLab);

  const tabs = [...buildLab.querySelectorAll("[data-build-tab]")];
  const flowCards = [...document.querySelectorAll("[data-build-flow-card]")];
  const statusEl = buildLab.querySelector("[data-build-status]");
  const urlEl = buildLab.querySelector("[data-build-url]");
  const codeModeEl = buildLab.querySelector("[data-build-code-mode]");
  const terminalTitleEl = buildLab.querySelector("[data-build-terminal-title]");
  const terminalPillEl = buildLab.querySelector("[data-build-terminal-pill]");
  const terminalLineEls = [...buildLab.querySelectorAll("[data-build-terminal-line]")];
  const statLabelEls = [...buildLab.querySelectorAll("[data-build-stat-label]")];
  const statValueEls = [...buildLab.querySelectorAll("[data-build-stat-value]")];

  const states = isGermanPage
    ? [
        {
          key: "website",
          tab: "Website",
          status: "Website bereit",
          url: "itdks.tech / unternehmen / launch",
          card: 0,
          codeMode: "Web",
          terminalTitle: "Website-Launch",
          terminalPill: "Bereit",
          terminalLines: [
            "Design freigegeben",
            "Texte und Formulare geprüft",
            "Website ist bereit für Besucher"
          ],
          stats: [
            { label: "Status", value: "Bereit" },
            { label: "Typ", value: "Unternehmensseite" },
            { label: "Tempo", value: "Schnell" }
          ]
        },
        {
          key: "software",
          tab: "Software",
          status: "Software aktiv",
          url: "app.itdks.tech / team / workflow",
          card: 1,
          codeMode: "App",
          terminalTitle: "System-Rollout",
          terminalPill: "Aktiv",
          terminalLines: [
            "Rollen und Workflow gesetzt",
            "Teamzugriffe verbunden",
            "Berichte aktualisieren live"
          ],
          stats: [
            { label: "Status", value: "Aktiv" },
            { label: "Typ", value: "Internes System" },
            { label: "Automatisierung", value: "Läuft" }
          ]
        },
        {
          key: "infrastructure",
          tab: "Infrastruktur",
          status: "Infrastruktur geschützt",
          url: "ops.itdks.tech / netzwerk / kontrolle",
          card: 2,
          codeMode: "IT",
          terminalTitle: "System-Monitoring",
          terminalPill: "Sicher",
          terminalLines: [
            "Zugriff und Firewall gesetzt",
            "Backups und Alarme aktiv",
            "Netzwerk wird überwacht"
          ],
          stats: [
            { label: "Sicherheit", value: "Geschützt" },
            { label: "Uptime", value: "24/7" },
            { label: "Support", value: "Aktiv" }
          ]
        }
      ]
    : isEnglishPage
      ? [
        {
          key: "website",
          tab: "Website",
          status: "Website ready",
          url: "itdks.tech / company / launch",
          card: 0,
          codeMode: "Web",
          terminalTitle: "Website launch",
          terminalPill: "Ready",
          terminalLines: [
            "Design approved",
            "Copy and forms checked",
            "Website is ready for visitors"
          ],
          stats: [
            { label: "Status", value: "Ready" },
            { label: "Type", value: "Company site" },
            { label: "Speed", value: "Fast" }
          ]
        },
        {
          key: "software",
          tab: "Software",
          status: "Software active",
          url: "app.itdks.tech / team / workflow",
          card: 1,
          codeMode: "App",
          terminalTitle: "System rollout",
          terminalPill: "Active",
          terminalLines: [
            "Roles and workflow set",
            "Team access connected",
            "Reports updating live"
          ],
          stats: [
            { label: "Status", value: "Active" },
            { label: "Type", value: "Internal system" },
            { label: "Automation", value: "Running" }
          ]
        },
        {
          key: "infrastructure",
          tab: "Infrastructure",
          status: "Infrastructure protected",
          url: "ops.itdks.tech / network / control",
          card: 2,
          codeMode: "IT",
          terminalTitle: "System monitoring",
          terminalPill: "Secure",
          terminalLines: [
            "Access and firewall set",
            "Backups and alerts active",
            "Network under monitoring"
          ],
          stats: [
            { label: "Security", value: "Protected" },
            { label: "Uptime", value: "24/7" },
            { label: "Support", value: "Active" }
          ]
        }
      ]
    : [
        {
          key: "website",
          tab: "Faqe web",
          status: "Faqja gati",
          url: "itdks.tech / kompani / publikim",
          card: 0,
          codeMode: "Web",
          terminalTitle: "Publikim i faqes",
          terminalPill: "Gati",
          terminalLines: [
            "Dizajni u miratua",
            "Teksti dhe formularët u kontrolluan",
            "Faqja është gati për vizitorë"
          ],
          stats: [
            { label: "Gjendja", value: "Gati" },
            { label: "Lloji", value: "Faqe kompanie" },
            { label: "Shpejtësia", value: "E shpejtë" }
          ]
        },
        {
          key: "software",
          tab: "Softuer",
          status: "Sistemi aktiv",
          url: "app.itdks.tech / ekip / rrjedhë",
          card: 1,
          codeMode: "App",
          terminalTitle: "Vendosje e sistemit",
          terminalPill: "Aktiv",
          terminalLines: [
            "Rolet dhe rrjedha u vendosën",
            "Qasjet e ekipit u lidhën",
            "Raportet po përditësohen live"
          ],
          stats: [
            { label: "Gjendja", value: "Aktiv" },
            { label: "Lloji", value: "Sistem i brendshëm" },
            { label: "Automatizim", value: "Në punë" }
          ]
        },
        {
          key: "infrastructure",
          tab: "Infrastrukturë",
          status: "Infrastruktura e mbrojtur",
          url: "ops.itdks.tech / rrjet / kontroll",
          card: 2,
          codeMode: "IT",
          terminalTitle: "Monitorim i sistemit",
          terminalPill: "Sigurt",
          terminalLines: [
            "Qasja dhe firewall-i u vendosën",
            "Backup-et dhe alarmet janë aktive",
            "Rrjeti po monitorohet"
          ],
          stats: [
            { label: "Siguri", value: "E mbrojtur" },
            { label: "Uptime", value: "24/7" },
            { label: "Mbështetje", value: "Aktive" }
          ]
        }
      ];

  let activeIndex = 0;
  let intervalId = 0;

  function applyState(index) {
    const state = states[index];
    if (!state) return;

    buildLab.dataset.buildState = state.key;
    if (statusEl) statusEl.textContent = state.status;
    if (urlEl) urlEl.textContent = state.url;
    if (codeModeEl) codeModeEl.textContent = state.codeMode;
    if (terminalTitleEl) terminalTitleEl.textContent = state.terminalTitle;
    if (terminalPillEl) terminalPillEl.textContent = state.terminalPill;

    tabs.forEach((tab, tabIndex) => {
      const isActive = tabIndex === index;
      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-pressed", isActive ? "true" : "false");
    });

    flowCards.forEach((card, cardIndex) => {
      card.classList.toggle("is-current", cardIndex === state.card);
    });

    terminalLineEls.forEach((line, lineIndex) => {
      line.textContent = state.terminalLines[lineIndex] || "";
    });

    statLabelEls.forEach((label, statIndex) => {
      label.textContent = state.stats[statIndex]?.label || "";
    });

    statValueEls.forEach((value, statIndex) => {
      value.textContent = state.stats[statIndex]?.value || "";
    });
  }

  function clearCycle() {
    if (!intervalId) return;
    window.clearInterval(intervalId);
    intervalId = 0;
  }

  function startCycle() {
    if (prefersReducedMotion || intervalId) return;
    intervalId = window.setInterval(() => {
      activeIndex = (activeIndex + 1) % states.length;
      applyState(activeIndex);
    }, 2600);
  }

  tabs.forEach((tab, tabIndex) => {
    tab.setAttribute("role", "button");
    tab.tabIndex = 0;

    const activate = () => {
      activeIndex = tabIndex;
      applyState(activeIndex);
      clearCycle();
      startCycle();
    };

    tab.addEventListener("click", activate);
    tab.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        activate();
      }
    });
  });

  buildLab.addEventListener("pointerenter", clearCycle);
  buildLab.addEventListener("pointerleave", startCycle);

  applyState(activeIndex);
  startCycle();
}

mountBuildLab();

const packageButtons = [...document.querySelectorAll("[data-package-select]")];
const packageInquiry = document.getElementById("package-inquiry");
const packageInquiryTitle = document.getElementById("package-inquiry-title");
const packageInquirySummary = document.getElementById("package-inquiry-summary");
const packageInquiryTag = document.getElementById("package-inquiry-tag");
const packageInquiryPrice = document.getElementById("package-inquiry-price");
const packageHiddenPackage = document.getElementById("package-hidden-package");
const packageHiddenSubject = document.getElementById("package-hidden-subject");
const packageWhatsappLink = document.getElementById("package-whatsapp-link");
const packageWhatsappQuick = document.getElementById("package-whatsapp-quick");
const packageWhatsappPreview = document.getElementById("package-whatsapp-preview");
const packageForm = document.getElementById("package-inquiry-form");
const packageFormStatus = document.getElementById("package-form-status");
const packageCards = [...document.querySelectorAll(".pricing-card")];
const PACKAGE_INQUIRY_HASH = "#package-inquiry";
const currentPath = window.location.pathname.toLowerCase();
const HOME_PAGE_PATH = isGermanPage ? "/de" : isEnglishPage ? "/en" : "/";
const isHomePage =
  currentPath === "/" ||
  currentPath.endsWith("/en") ||
  currentPath.endsWith("/de");

function buildPackageWhatsappUrl(packageLabel) {
  const message = copy.packageWhatsappMessage(packageLabel);
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

function getPackageData(button) {
  const packageLabel = button?.dataset.packageLabel || "Package";
  const packageTitle = button?.dataset.packageTitle || packageLabel;
  const packagePrice = button?.dataset.packagePrice || "";
  return { packageLabel, packageTitle, packagePrice, button };
}

function buildPackageInquiryUrl(packageData) {
  const url = new URL(HOME_PAGE_PATH, window.location.origin);
  url.searchParams.set("package", packageData.packageLabel);
  url.searchParams.set("title", packageData.packageTitle);
  if (packageData.packagePrice) {
    url.searchParams.set("price", packageData.packagePrice);
  }
  url.hash = "package-inquiry";
  return url.toString();
}

function syncPackageState(packageData) {
  const activeButton = packageData.button || packageButtons.find((item) => (item.dataset.packageLabel || "") === packageData.packageLabel);
  const activeCard = activeButton?.closest(".pricing-card") || null;

  packageButtons.forEach((item) => {
    const isActive = item === activeButton;
    item.classList.toggle("is-selected", isActive);
    item.setAttribute("aria-pressed", isActive ? "true" : "false");
    item.textContent = isActive ? copy.selectedPackage : copy.selectPlan;
  });

  packageCards.forEach((item) => {
    const isActive = item === activeCard;
    item.classList.toggle("is-selected-package", isActive);
    item.setAttribute("data-selected-state", isActive ? "true" : "false");
  });

  if (!packageInquiry) return;

  packageInquiry.hidden = false;
  packageInquiry.classList.add("is-hot");
  packageInquiry.classList.add("has-selection");
  packageInquiry.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "start" });

  if (packageInquiryTitle) {
    packageInquiryTitle.textContent = copy.packageTitle(packageData.packageTitle);
  }

  if (packageInquirySummary) {
    packageInquirySummary.textContent = copy.packageSummary(
      packageData.packageLabel,
      packageData.packageTitle,
      packageData.packagePrice
    );
  }

  if (packageInquiryTag) {
    packageInquiryTag.textContent = packageData.packageLabel;
  }

  if (packageInquiryPrice) {
    packageInquiryPrice.textContent = packageData.packagePrice || packageData.packageTitle;
  }

  if (packageHiddenPackage) {
    packageHiddenPackage.value = `${packageData.packageLabel} - ${packageData.packageTitle}`;
  }

  if (packageHiddenSubject) {
    packageHiddenSubject.value = copy.packageSubject(packageData.packageLabel);
  }

  const whatsappUrl = buildPackageWhatsappUrl(packageData.packageTitle);
  if (packageWhatsappLink) {
    packageWhatsappLink.href = whatsappUrl;
  }
  if (packageWhatsappQuick) {
    packageWhatsappQuick.href = whatsappUrl;
  }
  if (packageWhatsappPreview) {
    packageWhatsappPreview.textContent = copy.packageWhatsappPreview(packageData.packageTitle);
  }
  if (packageFormStatus) {
    packageFormStatus.textContent = "";
    packageFormStatus.className = "form-status";
  }

  const nextUrl = new URL(window.location.href);
  nextUrl.searchParams.set("package", packageData.packageLabel);
  nextUrl.searchParams.set("title", packageData.packageTitle);
  if (packageData.packagePrice) {
    nextUrl.searchParams.set("price", packageData.packagePrice);
  } else {
    nextUrl.searchParams.delete("price");
  }
  nextUrl.hash = "package-inquiry";
  window.history.replaceState({}, "", nextUrl.toString());

  if (packageForm) {
    const firstInput = packageForm.querySelector('input[type="text"], input[type="email"], input[type="tel"]');
    window.setTimeout(() => firstInput?.focus(), prefersReducedMotion ? 0 : 220);
  }
}

function setPackageSelection(button) {
  const packageData = getPackageData(button);

  if (!isHomePage || !packageInquiry) {
    window.location.href = buildPackageInquiryUrl(packageData);
    return;
  }

  syncPackageState(packageData);
}

if (packageButtons.length) {
  packageButtons.forEach((button) => {
    button.addEventListener("click", () => setPackageSelection(button));
  });
}

const packageFinder = document.querySelector("[data-package-finder]");

if (packageFinder) {
  const finderAnswers = [...packageFinder.querySelectorAll("[data-package-answer]")];
  const finderResult = packageFinder.querySelector("[data-package-recommendation]");
  const finderLabel = packageFinder.querySelector("[data-package-recommendation-label]");
  const finderCopy = packageFinder.querySelector("[data-package-recommendation-copy]");
  const finderApply = packageFinder.querySelector("[data-package-finder-apply]");
  const selectedAnswers = new Map();
  let currentFinderPackage = "Business";

  function getFinderCopy(packageLabel) {
    const key = `copy${packageLabel}`;
    return packageFinder.dataset[key] || "";
  }

  function chooseFinderPackage() {
    const scores = { Starter: 0, Business: 0, Enterprise: 0 };
    selectedAnswers.forEach((packageLabel) => {
      if (scores[packageLabel] !== undefined) scores[packageLabel] += 1;
    });

    return ["Business", "Enterprise", "Starter"].sort((a, b) => scores[b] - scores[a])[0];
  }

  function updateFinderResult() {
    if (!selectedAnswers.size) return;

    currentFinderPackage = chooseFinderPackage();
    const matchingButton = packageButtons.find((button) => (button.dataset.packageLabel || "") === currentFinderPackage);
    const title = matchingButton?.dataset.packageTitle || currentFinderPackage;
    const price = matchingButton?.dataset.packagePrice || "";

    if (finderResult) finderResult.hidden = false;
    if (finderLabel) finderLabel.textContent = currentFinderPackage;
    if (finderCopy) {
      finderCopy.textContent = `${getFinderCopy(currentFinderPackage)}${price ? ` ${price}.` : ""}`;
    }
    if (finderApply) {
      finderApply.textContent = isGermanPage
        ? `Weiter mit ${currentFinderPackage}`
        : isEnglishPage
          ? `Continue with ${currentFinderPackage}`
          : `Vazhdo me ${currentFinderPackage}`;
      finderApply.setAttribute("aria-label", `${title} ${price}`.trim());
    }
  }

  finderAnswers.forEach((answer) => {
    answer.addEventListener("click", () => {
      const question = answer.closest("[data-package-question]");
      const questionKey = question?.dataset.packageQuestion || answer.textContent.trim();
      const packageTarget = answer.dataset.packageTarget || "Business";

      question?.querySelectorAll("[data-package-answer]").forEach((item) => {
        item.classList.toggle("is-selected", item === answer);
        item.setAttribute("aria-pressed", item === answer ? "true" : "false");
      });

      selectedAnswers.set(questionKey, packageTarget);
      updateFinderResult();
    });
  });

  finderApply?.addEventListener("click", () => {
    const matchingButton = packageButtons.find((button) => (button.dataset.packageLabel || "") === currentFinderPackage);
    if (matchingButton) {
      setPackageSelection(matchingButton);
    }
  });
}

if (isHomePage && packageInquiry) {
  const packageParams = new URLSearchParams(window.location.search);
  const selectedPackage = packageParams.get("package");
  if (selectedPackage) {
    const matchingButton = packageButtons.find((button) => (button.dataset.packageLabel || "").toLowerCase() === selectedPackage.toLowerCase());
    const packageData = matchingButton
      ? getPackageData(matchingButton)
      : {
          packageLabel: selectedPackage,
          packageTitle: packageParams.get("title") || selectedPackage,
          packagePrice: packageParams.get("price") || "",
          button: null
        };

    syncPackageState(packageData);

    if (window.location.hash !== PACKAGE_INQUIRY_HASH) {
      const nextUrl = new URL(window.location.href);
      nextUrl.hash = "package-inquiry";
      window.history.replaceState({}, "", nextUrl.toString());
    }
  }
}

if (packageForm && packageFormStatus) {
  packageForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (packageForm.dataset.submitting === "true") return;
    packageFormStatus.className = "form-status";

    const data = Object.fromEntries(new FormData(packageForm).entries());
    if (!data.paketa || !data.emri || !data.email || !data.telefoni) {
      packageFormStatus.textContent = copy.packageRequired;
      packageFormStatus.classList.add("error");
      return;
    }

    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email);
    if (!emailOk) {
      packageFormStatus.textContent = copy.validEmail;
      packageFormStatus.classList.add("error");
      return;
    }

    const phoneDigits = String(data.telefoni).replace(/\D/g, "");
    if (phoneDigits.length < 7) {
      packageFormStatus.textContent = copy.validPhone;
      packageFormStatus.classList.add("error");
      return;
    }

    const packageSubmitButton = packageForm.querySelector('button[type="submit"], input[type="submit"]');
    packageForm.dataset.submitting = "true";
    packageForm.setAttribute("aria-busy", "true");
    if (packageSubmitButton) packageSubmitButton.disabled = true;

    try {
      const formData = new FormData(packageForm);
      const response = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: formData
      });

      if (!response.ok) {
        throw new Error("Package submit failed");
      }

      const selectedPackage = packageHiddenPackage?.value || "";
      const selectedSubject = packageHiddenSubject?.value || copy.packageSubject(isGermanPage ? "Ausgewähltes Paket" : isEnglishPage ? "Selected package" : "Paketa e zgjedhur");
      packageForm.reset();

      if (packageHiddenPackage) {
        packageHiddenPackage.value = selectedPackage;
      }

      if (packageHiddenSubject) {
        packageHiddenSubject.value = selectedSubject;
      }

      packageFormStatus.textContent = copy.packageSuccess;
      packageFormStatus.classList.add("success");
    } catch {
      packageFormStatus.textContent = copy.packageError;
      packageFormStatus.classList.add("error");
    } finally {
      packageForm.dataset.submitting = "false";
      packageForm.removeAttribute("aria-busy");
      if (packageSubmitButton) packageSubmitButton.disabled = false;
    }
  });
}

const form = document.getElementById("contact-form");
const statusEl = document.getElementById("form-status");
if (form && statusEl) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (form.dataset.submitting === "true") return;
    statusEl.className = "form-status";
    const data = Object.fromEntries(new FormData(form).entries());

    if (!data.emri || !data.email || !data.kompania || !data.sherbimi) {
      statusEl.textContent = copy.contactRequired;
      statusEl.classList.add("error");
      return;
    }

    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email);
    if (!emailOk) {
      statusEl.textContent = copy.validEmail;
      statusEl.classList.add("error");
      return;
    }

    const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    form.dataset.submitting = "true";
    form.setAttribute("aria-busy", "true");
    if (submitButton) submitButton.disabled = true;

    try {
      const formData = new FormData(form);
      const response = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: formData
      });

      if (!response.ok) {
        throw new Error("Submit failed");
      }

      try { window.ITDAnalytics?.reportLeadSuccess("contact-form", response); } catch (trackingError) { /* Tracking must not interrupt form success. */ }
      form.reset();
      statusEl.textContent = copy.contactSuccess;
      statusEl.classList.add("success");
    } catch {
      statusEl.textContent = copy.contactError;
      statusEl.classList.add("error");
    } finally {
      form.dataset.submitting = "false";
      form.removeAttribute("aria-busy");
      if (submitButton) submitButton.disabled = false;
    }
  });
}

document.querySelectorAll(".button, .button-ghost, .utility-button, .nav-toggle").forEach((button) => {
  button.addEventListener("pointerdown", () => {
    button.classList.add("is-pressed");
  });

  const clearPress = () => button.classList.remove("is-pressed");
  button.addEventListener("pointerup", clearPress);
  button.addEventListener("pointerleave", clearPress);
  button.addEventListener("blur", clearPress);
});

function initVisualScene() {
  const container = document.getElementById("visual");
  if (!container || !window.THREE || container.dataset.visualReady === "true") return;
  container.dataset.visualReady = "true";

  try {
    const isSmall = window.innerWidth < 768;
    const coarsePointer = window.matchMedia("(hover: none), (pointer: coarse)").matches;
    const lowPowerDevice = prefersReducedMotion || coarsePointer || isSmall || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);
    const mobileFactor = isSmall ? 0.68 : 1;
    const nodeCount = lowPowerDevice ? (isSmall ? 38 : 68) : 104;
    const shapeCount = lowPowerDevice ? (isSmall ? 10 : 18) : 26;
    const shieldCount = lowPowerDevice ? (isSmall ? 7 : 13) : 20;
    const streamCount = lowPowerDevice ? (isSmall ? 30 : 58) : 92;
    const particleCount = lowPowerDevice ? (isSmall ? 220 : 400) : 760;
    const sceneMotion = lowPowerDevice ? 0.74 : 0.84;
    const targetFrameMs = prefersReducedMotion ? 1000 / 12 : lowPowerDevice ? 1000 / 24 : 1000 / 42;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050505, 0.024);

    const camera = new THREE.PerspectiveCamera(54, window.innerWidth / window.innerHeight, 0.1, 220);
    camera.position.set(0, 0.4, 22);

    const renderer = new THREE.WebGLRenderer({ antialias: !lowPowerDevice, alpha: true, powerPreference: lowPowerDevice ? "default" : "high-performance" });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, lowPowerDevice ? 1 : 1.35));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    container.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0xffffff, 0.4));

  const redLight = new THREE.PointLight(0xe00000, 18, 130);
  redLight.position.set(10, 8, 12);
  scene.add(redLight);

  const redSoftLight = new THREE.PointLight(0xff3b3b, 8, 100);
  redSoftLight.position.set(-9, -7, 10);
  scene.add(redSoftLight);

  const whiteLight = new THREE.PointLight(0xffffff, 3.6, 80);
  whiteLight.position.set(0, 12, 8);
  scene.add(whiteLight);

  const world = new THREE.Group();
  scene.add(world);

  const ringA = new THREE.Mesh(
    new THREE.TorusGeometry(6.3, 0.08, 18, 220),
    new THREE.MeshBasicMaterial({ color: 0xe00000, transparent: true, opacity: 0.2 })
  );
  ringA.rotation.x = Math.PI * 0.4;
  world.add(ringA);

  const ringB = new THREE.Mesh(
    new THREE.TorusGeometry(9.2, 0.05, 12, 200),
    new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.09 })
  );
  ringB.rotation.set(Math.PI * 0.16, Math.PI * 0.28, 0);
  world.add(ringB);

  const pulseGroup = new THREE.Group();
  world.add(pulseGroup);
  const pulseRings = [];
  for (let i = 0; i < 3; i++) {
    const pulse = new THREE.Mesh(
      new THREE.RingGeometry(1.68, 1.9, 72),
      new THREE.MeshBasicMaterial({
        color: i === 1 ? 0xffffff : 0xff3b3b,
        transparent: true,
        opacity: i === 1 ? 0.1 : 0.16,
        side: THREE.DoubleSide,
        depthWrite: false
      })
    );
    pulse.rotation.x = Math.PI * 0.5;
    pulse.position.set(i === 0 ? -4.6 : i === 1 ? 0 : 4.8, -1.1 + i * 0.45, -2.8 - i * 0.6);
    pulse.userData = {
      offset: i * 1.6,
      baseX: pulse.position.x,
      baseY: pulse.position.y,
      baseZ: pulse.position.z
    };
    pulseGroup.add(pulse);
    pulseRings.push(pulse);
  }

  const coreGroup = new THREE.Group();
  coreGroup.position.set(0, -0.35, -1.8);
  world.add(coreGroup);

  const coreShellAMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.12 });
  const coreShellBMat = new THREE.LineBasicMaterial({ color: 0xe00000, transparent: true, opacity: 0.18 });
  const coreShellA = new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.OctahedronGeometry(2.2, 0)),
    coreShellAMat
  );
  const coreShellB = new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(1.5, 0)),
    coreShellBMat
  );
  coreShellA.rotation.set(0.42, 0.2, 0.14);
  coreShellB.rotation.set(-0.34, 0.46, 0.18);
  coreGroup.add(coreShellA);
  coreGroup.add(coreShellB);

  const coreNode = new THREE.Mesh(
    new THREE.SphereGeometry(0.18, 12, 12),
    new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.82 })
  );
  coreGroup.add(coreNode);

  const nodeGeo = new THREE.SphereGeometry(0.13, 14, 14);
  const nodeMaterials = [
    new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.84, roughness: 0.24, emissive: 0x111111, emissiveIntensity: 0.08 }),
    new THREE.MeshStandardMaterial({ color: 0xe00000, metalness: 0.82, roughness: 0.22, emissive: 0x580000, emissiveIntensity: 0.12 }),
    new THREE.MeshStandardMaterial({ color: 0xff3b3b, metalness: 0.8, roughness: 0.24, emissive: 0x600000, emissiveIntensity: 0.1 }),
    new THREE.MeshStandardMaterial({ color: 0x2a2a2a, metalness: 0.62, roughness: 0.38, emissive: 0x090909, emissiveIntensity: 0.06 })
  ];

  const nodeGroup = new THREE.Group();
  world.add(nodeGroup);
  const nodes = [];
  for (let i = 0; i < nodeCount; i++) {
    const mesh = new THREE.Mesh(nodeGeo, nodeMaterials[i % nodeMaterials.length]);
    const radius = 4.8 + Math.random() * 8.2;
    const angle = Math.random() * Math.PI * 2;
    mesh.position.set(
      Math.cos(angle) * radius + (Math.random() - 0.5) * 2.2,
      (Math.random() - 0.5) * 10,
      Math.sin(angle) * radius + (Math.random() - 0.5) * 7.2
    );
    mesh.userData = {
      baseX: mesh.position.x,
      baseY: mesh.position.y,
      baseZ: mesh.position.z,
      speed: 0.14 + Math.random() * 0.3,
      drift: Math.random() * Math.PI * 2,
      depth: Math.random() * 0.45 + 0.8
    };
    nodeGroup.add(mesh);
    nodes.push(mesh);
  }

  const polyGroup = new THREE.Group();
  world.add(polyGroup);
  const polyGeometries = [
    new THREE.IcosahedronGeometry(0.24, 0),
    new THREE.OctahedronGeometry(0.28, 0),
    new THREE.TetrahedronGeometry(0.3, 0),
    new THREE.BoxGeometry(0.28, 0.28, 0.28)
  ];
  const polyMaterials = [
    new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.72, roughness: 0.24, transparent: true, opacity: 0.76 }),
    new THREE.MeshStandardMaterial({ color: 0xe00000, metalness: 0.76, roughness: 0.24, transparent: true, opacity: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0xff3b3b, metalness: 0.74, roughness: 0.26, transparent: true, opacity: 0.76 })
  ];
  const shapes = [];
  for (let i = 0; i < shapeCount; i++) {
    const shape = new THREE.Mesh(polyGeometries[i % polyGeometries.length], polyMaterials[i % polyMaterials.length]);
    shape.position.set((Math.random() - 0.5) * 18, (Math.random() - 0.5) * 12, (Math.random() - 0.5) * 16);
    shape.userData = {
      rx: 0.001 + Math.random() * 0.003,
      ry: 0.001 + Math.random() * 0.0035,
      rz: 0.0008 + Math.random() * 0.002,
      wave: Math.random() * Math.PI * 2,
      baseY: shape.position.y,
      depth: Math.random() * 0.6 + 0.5
    };
    polyGroup.add(shape);
    shapes.push(shape);
  }

  const shieldSvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ffffff"/><stop offset="55%" stop-color="#ff3b3b"/><stop offset="100%" stop-color="#e00000"/></linearGradient></defs><path fill="url(#g)" d="M32 4l21 8v15c0 14.2-9.3 27-21 33C20.3 54 11 41.2 11 27V12l21-8z"/></svg>';
  const shieldTexture = new THREE.TextureLoader().load('data:image/svg+xml;charset=utf-8,' + encodeURIComponent(shieldSvg));
  const shieldGroup = new THREE.Group();
  world.add(shieldGroup);
  const shields = [];
  for (let i = 0; i < shieldCount; i++) {
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: shieldTexture, transparent: true, opacity: 0.72, depthWrite: false }));
    const radius = 3.4 + Math.random() * 10;
    const scale = 0.72 + Math.random() * 0.7;
    sprite.scale.set(scale, scale, scale);
    sprite.userData = {
      radius,
      angle: Math.random() * Math.PI * 2,
      speed: 0.001 + Math.random() * 0.002,
      height: 2 + Math.random() * 5,
      wave: Math.random() * Math.PI * 2,
      depth: Math.random() * 0.5 + 0.8
    };
    shieldGroup.add(sprite);
    shields.push(sprite);
  }

  const linePositions = new Float32Array(2200 * 6);
  const lineGeometry = new THREE.BufferGeometry();
  lineGeometry.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));
  const lines = new THREE.LineSegments(lineGeometry, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.08 }));
  world.add(lines);

  function updateLines() {
    let ptr = 0;
    let segments = 0;
    for (let i = 0; i < nodes.length; i++) {
      let linked = 0;
      const a = nodes[i].position;
      for (let j = i + 1; j < nodes.length && linked < 3; j++) {
        const b = nodes[j].position;
        if (a.distanceToSquared(b) < 7.2) {
          linePositions[ptr++] = a.x;
          linePositions[ptr++] = a.y;
          linePositions[ptr++] = a.z;
          linePositions[ptr++] = b.x;
          linePositions[ptr++] = b.y;
          linePositions[ptr++] = b.z;
          segments += 2;
          linked++;
        }
      }
    }
    lineGeometry.setDrawRange(0, segments);
    lineGeometry.attributes.position.needsUpdate = true;
  }

  const particlePositions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particlePositions.length; i += 3) {
    particlePositions[i] = (Math.random() - 0.5) * 86;
    particlePositions[i + 1] = (Math.random() - 0.5) * 56;
    particlePositions[i + 2] = (Math.random() - 0.5) * 52;
  }
  const particleGeometry = new THREE.BufferGeometry();
  particleGeometry.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
  const particles = new THREE.Points(particleGeometry, new THREE.PointsMaterial({ color: 0xffffff, size: 0.045, transparent: true, opacity: 0.38, depthWrite: false }));
  scene.add(particles);

  const streamGroup = new THREE.Group();
  world.add(streamGroup);
  const streamGeo = new THREE.SphereGeometry(0.06, 10, 10);
  const streamMaterials = [
    new THREE.MeshBasicMaterial({ color: 0xe00000, transparent: true, opacity: 0.82 }),
    new THREE.MeshBasicMaterial({ color: 0xff3b3b, transparent: true, opacity: 0.78 }),
    new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.56 })
  ];
  const streams = [];
  for (let i = 0; i < streamCount; i++) {
    const stream = new THREE.Mesh(streamGeo, streamMaterials[i % streamMaterials.length]);
    stream.userData = {
      radius: 2.6 + Math.random() * 10,
      angle: Math.random() * Math.PI * 2,
      speed: 0.002 + Math.random() * 0.003,
      vertical: 2 + Math.random() * 6,
      offset: Math.random() * Math.PI * 2,
      depth: Math.random() * 0.5 + 0.8
    };
    streamGroup.add(stream);
    streams.push(stream);
  }

  const beamGroup = new THREE.Group();
  world.add(beamGroup);
  const beamGeo = new THREE.BoxGeometry(0.045, 5.4, 0.045);
  const beamCoreMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.08 });
  const beamAccentMat = new THREE.MeshBasicMaterial({ color: 0xe00000, transparent: true, opacity: 0.12 });
  const beamDotGeo = new THREE.SphereGeometry(0.085, 10, 10);
  const beamDotMat = new THREE.MeshBasicMaterial({ color: 0xff3b3b, transparent: true, opacity: 0.88 });
  const beams = [];
  for (let i = 0; i < (isSmall ? 4 : 6); i++) {
    const beam = new THREE.Group();
    const beamLine = new THREE.Mesh(beamGeo, i % 2 === 0 ? beamCoreMat : beamAccentMat);
    const beamDot = new THREE.Mesh(beamDotGeo, beamDotMat);
    const x = -8.5 + i * 3.4;
    const z = -6.8 + (i % 2) * 1.8;
    beam.position.set(x, 0.2 + (i % 3) * 0.4, z);
    beamLine.position.y = 0;
    beamDot.position.y = -2.2;
    beam.userData = {
      baseX: x,
      baseY: beam.position.y,
      baseZ: z,
      floatOffset: i * 0.9 + Math.random() * Math.PI,
      phase: Math.random() * Math.PI * 2,
      depth: 0.6 + Math.random() * 0.5
    };
    beam.add(beamLine);
    beam.add(beamDot);
    beamGroup.add(beam);
    beams.push({ beam, beamLine, beamDot });
  }

  function makeGlow(r, g, b, size, opacity) {
    const canvas = document.createElement("canvas");
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext("2d");
    const gradient = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    gradient.addColorStop(0, "rgba(" + r + "," + g + "," + b + "," + opacity + ")");
    gradient.addColorStop(0.3, "rgba(" + r + "," + g + "," + b + "," + (opacity * 0.4) + ")");
    gradient.addColorStop(1, "rgba(" + r + "," + g + "," + b + ",0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 256, 256);
    const texture = new THREE.CanvasTexture(canvas);
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false }));
    sprite.scale.set(size, size, 1);
    return sprite;
  }

  const glowA = makeGlow(224, 0, 0, 18, 0.22);
  glowA.position.set(-5, 2, -6);
  scene.add(glowA);

  const glowB = makeGlow(255, 59, 59, 14, 0.16);
  glowB.position.set(6, -3, -5.4);
  scene.add(glowB);

  const glowC = makeGlow(255, 255, 255, 10, 0.08);
  glowC.position.set(0.4, 4, -8);
  scene.add(glowC);

  const targetMouse = { x: 0, y: 0 };
  const mouse = { x: 0, y: 0 };
  const scrollState = { y: 0, target: 0 };

  window.addEventListener("pointermove", (event) => {
    targetMouse.x = (event.clientX / window.innerWidth - 0.5) * 2;
    targetMouse.y = (event.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  window.addEventListener("scroll", () => {
    const maxScroll = Math.max(document.body.scrollHeight - window.innerHeight, 1);
    scrollState.target = window.scrollY / maxScroll;
  }, { passive: true });

  let last = performance.now();
  let lineFrame = 0;
  function animate(now) {
    requestAnimationFrame(animate);
    if (document.hidden || now - last < targetFrameMs) return;

    const dt = Math.min((now - last) / 16.666, 2.6);
    last = now;
    const t = now * 0.00024 * sceneMotion;

    mouse.x += (targetMouse.x - mouse.x) * 0.05;
    mouse.y += (targetMouse.y - mouse.y) * 0.05;
    scrollState.y += (scrollState.target - scrollState.y) * 0.05;

    world.rotation.y = Math.sin(t * 0.62) * 0.035 + mouse.x * 0.16 * mobileFactor;
    world.rotation.x = Math.cos(t * 0.48) * 0.025 + mouse.y * 0.12 * mobileFactor - scrollState.y * 0.06;
    world.position.x = mouse.x * 0.7 * mobileFactor;
    world.position.y = -scrollState.y * 2.2 + mouse.y * 0.45 * mobileFactor;
    world.position.z = Math.sin(t * 0.45) * 0.32;

    ringA.rotation.z += 0.0008 * dt * sceneMotion;
    ringB.rotation.z -= 0.00065 * dt * sceneMotion;
    pulseGroup.rotation.y += 0.00022 * dt * sceneMotion;
    nodeGroup.rotation.y += 0.00028 * dt * sceneMotion;
    coreGroup.rotation.y += 0.00038 * dt * sceneMotion;
    coreGroup.rotation.z += 0.00008 * dt * sceneMotion;
    streamGroup.rotation.y -= 0.00055 * dt * sceneMotion;
    streamGroup.rotation.x += 0.0001 * dt * sceneMotion;
    beamGroup.rotation.y += 0.00008 * dt * sceneMotion;

    if (!prefersReducedMotion) {
      pulseRings.forEach((pulse, index) => {
        const pulseTime = (t * 1.8 + pulse.userData.offset) % (Math.PI * 2);
        const wave = (Math.sin(pulseTime) + 1) * 0.5;
        const scale = 0.8 + wave * 1.5;
        pulse.scale.setScalar(scale);
        pulse.material.opacity = (index === 1 ? 0.05 : 0.08) + wave * (index === 1 ? 0.08 : 0.14);
        pulse.position.x = pulse.userData.baseX + mouse.x * (0.18 + index * 0.05) * mobileFactor;
        pulse.position.y = pulse.userData.baseY - scrollState.y * 0.55;
        pulse.position.z = pulse.userData.baseZ + Math.cos(t * 1.3 + index) * 0.24;
      });

      coreGroup.position.x = mouse.x * 0.62 * mobileFactor;
      coreGroup.position.y = -0.35 - scrollState.y * 0.42 - mouse.y * 0.26 * mobileFactor;
      coreGroup.position.z = -1.8 + Math.sin(t * 2.4) * 0.16;
      coreShellA.rotation.x += 0.0012 * dt * sceneMotion;
      coreShellA.rotation.y += 0.0018 * dt * sceneMotion;
      coreShellB.rotation.x -= 0.0015 * dt * sceneMotion;
      coreShellB.rotation.z += 0.0012 * dt * sceneMotion;
      coreShellAMat.opacity = 0.09 + (Math.sin(t * 3.6) + 1) * 0.025;
      coreShellBMat.opacity = 0.12 + (Math.cos(t * 4.2) + 1) * 0.04;
      coreNode.scale.setScalar(0.92 + Math.sin(t * 7.4) * 0.08);

      nodes.forEach((node, index) => {
        node.position.x = node.userData.baseX + Math.sin(t * 5.6 * node.userData.speed + node.userData.drift) * 0.11 + mouse.x * node.userData.depth * 0.22 * mobileFactor;
        node.position.y = node.userData.baseY + Math.cos(t * 4.8 * node.userData.speed + node.userData.drift) * 0.12 - mouse.y * node.userData.depth * 0.18 * mobileFactor;
        node.position.z = node.userData.baseZ + Math.sin(t * 4.2 * node.userData.speed + node.userData.drift) * 0.1;
        node.scale.setScalar(0.96 + Math.sin(t * 9 + index * 0.36) * 0.07);
      });

      shapes.forEach((shape, index) => {
        shape.rotation.x += shape.userData.rx * dt * 0.65 * sceneMotion + mouse.y * 0.00035 * mobileFactor;
        shape.rotation.y += shape.userData.ry * dt * 0.65 * sceneMotion + mouse.x * 0.00045 * mobileFactor;
        shape.rotation.z += shape.userData.rz * dt * 0.65 * sceneMotion;
        shape.position.y = shape.userData.baseY + Math.sin(t * 3.2 + shape.userData.wave + index * 0.12) * 0.14 - mouse.y * shape.userData.depth * 0.12 * mobileFactor;
      });

      shields.forEach((shield, index) => {
        shield.userData.angle += shield.userData.speed * dt * 4.2 * sceneMotion;
        shield.position.x = Math.cos(shield.userData.angle) * shield.userData.radius + mouse.x * shield.userData.depth * 0.24 * mobileFactor;
        shield.position.z = Math.sin(shield.userData.angle) * shield.userData.radius;
        shield.position.y = Math.sin(t * 4.2 + shield.userData.wave + index * 0.16) * shield.userData.height - mouse.y * shield.userData.depth * 0.16 * mobileFactor;
        shield.material.rotation += 0.0011 * dt * sceneMotion;
      });

      streams.forEach((stream, index) => {
        stream.userData.angle += stream.userData.speed * dt * 3.8 * sceneMotion;
        stream.position.x = Math.cos(stream.userData.angle) * stream.userData.radius + mouse.x * stream.userData.depth * 0.3 * mobileFactor;
        stream.position.z = Math.sin(stream.userData.angle) * stream.userData.radius;
        stream.position.y = Math.sin(stream.userData.angle * 1.8 + stream.userData.offset) * stream.userData.vertical - mouse.y * stream.userData.depth * 0.2 * mobileFactor;
        stream.scale.setScalar(0.9 + Math.sin(t * 10 + index * 0.34) * 0.12);
      });

      beams.forEach(({ beam, beamLine, beamDot }, index) => {
        const phase = t * 2.8 + beam.userData.phase;
        beam.position.x = beam.userData.baseX + mouse.x * beam.userData.depth * 0.38 * mobileFactor;
        beam.position.y = beam.userData.baseY + Math.sin(t * 1.2 + beam.userData.floatOffset) * 0.18 - scrollState.y * 0.36;
        beam.position.z = beam.userData.baseZ + Math.cos(t * 0.95 + index) * 0.14;
        beamLine.scale.y = 0.9 + Math.sin(t * 1.4 + index * 0.5) * 0.08;
        beamDot.position.y = -2.2 + ((Math.sin(phase) + 1) * 0.5) * 4.4;
        beamDot.scale.setScalar(0.84 + Math.sin(t * 4.4 + index) * 0.08);
        beamLine.material.opacity = 0.05 + ((Math.sin(phase * 0.6) + 1) * 0.5) * 0.08;
      });
    }

    particles.rotation.y += 0.00008 * dt * sceneMotion;
    particles.rotation.x += 0.000025 * dt * sceneMotion;
    particles.position.x = mouse.x * 1.1 * mobileFactor;
    particles.position.y = -scrollState.y * 1.6;
    lines.material.opacity = 0.06 + (Math.sin(t * 2.1) + 1) * 0.015 + scrollState.y * 0.012;

    glowA.position.x = -5 + mouse.x * 0.8 * mobileFactor;
    glowA.position.y = 2 - mouse.y * 0.45 * mobileFactor;
    glowA.material.opacity = 0.22 + Math.sin(t * 5.2) * 0.03;

    glowB.position.x = 6 + mouse.x * 0.65 * mobileFactor;
    glowB.position.y = -3 - mouse.y * 0.5 * mobileFactor;
    glowB.material.opacity = 0.15 + Math.cos(t * 4.8) * 0.02;

    glowC.position.x = 0.4 + mouse.x * 0.35 * mobileFactor;
    glowC.position.y = 4 - mouse.y * 0.32 * mobileFactor;
    glowC.material.opacity = 0.08 + Math.sin(t * 3.8 + 1.4) * 0.015;

    redLight.position.x = 10 + mouse.x * 3 * mobileFactor;
    redLight.position.y = 8 - mouse.y * 2.2 * mobileFactor;
    redLight.intensity = 17 + Math.sin(t * 2.2) * 1.6;
    redSoftLight.position.x = -9 - mouse.x * 2.4 * mobileFactor;
    redSoftLight.position.y = -7 + mouse.y * 2.2 * mobileFactor;
    redSoftLight.intensity = 7.5 + Math.cos(t * 2.6) * 1.1;
    whiteLight.position.x = mouse.x * 1.2 * mobileFactor;
    whiteLight.position.y = 12 - mouse.y * 1.6 * mobileFactor;
    whiteLight.intensity = 3.2 + Math.sin(t * 1.8 + 0.8) * 0.4;

    camera.position.x += ((mouse.x * 1.2 * mobileFactor) - camera.position.x) * 0.03;
    camera.position.y += (((-mouse.y * 0.9 * mobileFactor) + 0.4 + scrollState.y * 0.7) - camera.position.y) * 0.03;
    camera.position.z += ((22 - scrollState.y * 1.1) - camera.position.z) * 0.025;
    camera.lookAt(0, -scrollState.y * 1.2, 0);

    lineFrame++;
    if (lineFrame % (lowPowerDevice ? 5 : 3) === 0) updateLines();
    renderer.render(scene, camera);
  }

  updateLines();
  animate(performance.now());

    window.addEventListener("resize", () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, lowPowerDevice ? 1 : 1.35));
    });
  } catch (error) {
    console.error("IT Department background scene failed to initialize.", error);
    container.innerHTML = "";
    document.documentElement.classList.add("no-visual-scene");
  }
}

function shouldSkipVisualScene() {
  const smallViewport = window.innerWidth < 860;
  const coarsePointer = window.matchMedia("(hover: none), (pointer: coarse)").matches;
  const lowThreadCount = navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4;
  return prefersReducedMotion || smallViewport || coarsePointer || lowThreadCount;
}

function loadVisualSceneWhenIdle() {
  const container = document.getElementById("visual");
  if (!container || container.dataset.visualReady === "true") return;

  if (shouldSkipVisualScene()) {
    document.documentElement.classList.add("no-visual-scene");
    return;
  }

  if (window.THREE) {
    initVisualScene();
    return;
  }

  const threeModuleSrc = "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js";
  window.__itdThreeModulePromise = window.__itdThreeModulePromise || import(threeModuleSrc);
  window.__itdThreeModulePromise
    .then((three) => {
      window.THREE = three;
      initVisualScene();
    })
    .catch(() => document.documentElement.classList.add("no-visual-scene"));
}

function scheduleVisualScene() {
  if (!document.getElementById("visual")) return;

  let queued = false;
  const queueLoad = () => {
    if (queued) return;
    queued = true;
    window.removeEventListener("pointermove", queueLoad);
    window.removeEventListener("scroll", queueLoad);

    const load = () => {
      if ("requestIdleCallback" in window) {
        window.requestIdleCallback(loadVisualSceneWhenIdle, { timeout: 1200 });
      } else {
        loadVisualSceneWhenIdle();
      }
    };

    window.setTimeout(load, 120);
  };

  const start = () => {
    window.addEventListener("pointermove", queueLoad, { once: true, passive: true });
    window.addEventListener("scroll", queueLoad, { once: true, passive: true });
    window.setTimeout(queueLoad, 900);
  };

  if (document.readyState === "complete") {
    start();
  } else {
    window.addEventListener("load", start, { once: true });
  }
}

scheduleVisualScene();
































