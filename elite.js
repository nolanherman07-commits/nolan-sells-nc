/* Nestlewood Realty: Elite */

/* ===== SETTINGS ===== */
// Background videos live in the videos/ folder. Each section picks its clip in _build/build.py.
// If a video is missing, the animated mountain scene shows instead.
const LEAD_EMAIL = "nolan@nestlewoodrealty.com";
// Forms are delivered to LEAD_EMAIL by FormSubmit (formsubmit.co, free, no account).
// The very first submission sends an "Activate form" email to LEAD_EMAIL; click it once.
const FORM_ENDPOINT = "https://formsubmit.co/ajax/" + LEAD_EMAIL;
// Per-video tuning: "start" skips that many seconds at the beginning, "rate" is playback speed (1 = normal).
const VIDEO_TUNING = { "videos/sell.mp4": { start: 3, rate: 1.5 } };

/* Always start each page at the top (unless the link points to a section, like sell.html#value) */
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
const toTop = () => { if (!location.hash) window.scrollTo(0, 0); };
toTop();
addEventListener("DOMContentLoaded", toTop);
addEventListener("load", toTop);
addEventListener("pageshow", toTop);

/* ===== Animated Blue Ridge mountain scenes (drawn in code) ===== */
const PALETTES = {
  sunset: { sky: ["#1e2140", "#4e4170", "#b8687b", "#f19a62", "#fcd49a"], sun: "#ffe0a8", sunY: 600, ridges: ["#c18ea0", "#946f94", "#694f7c", "#46385e", "#2a2341", "#141220"] },
  golden: { sky: ["#36597d", "#86a3be", "#e9c495", "#f6a65a"], sun: "#fff0c8", sunY: 560, ridges: ["#b3a9bd", "#8a83a1", "#64627f", "#43445e", "#282a3e", "#14151f"] },
  dusk:   { sky: ["#121833", "#36305e", "#85507d", "#e17a68"], sun: "#ffb58a", sunY: 640, ridges: ["#8a6589", "#634a77", "#45375e", "#2d2645", "#1c182d", "#0f0d18"] },
  mist:   { sky: ["#8ea6ba", "#c3d0da", "#ece5d8"], sun: "#ffffff", sunY: 520, ridges: ["#bcc7d0", "#98a8b7", "#76899d", "#566b82", "#3a4d64", "#223040"] },
  night:  { sky: ["#04060e", "#0b1230", "#1b2452"], sun: "#e9ecff", sunY: 300, moon: true, ridges: ["#2c3463", "#232a53", "#1b2043", "#141832", "#0d1023", "#07091a"] },
  dawn:   { sky: ["#2b3a5a", "#7a83a6", "#e6b0a0", "#f5d2a7"], sun: "#fff1d0", sunY: 600, ridges: ["#b5a8bb", "#8b80a0", "#655e80", "#45425f", "#2a2a40", "#161622"] },
};
function rng(seed) { return () => (seed = (seed * 16807) % 2147483647) / 2147483647; }
function mountainSVG(name, seed = 7) {
  const P = PALETTES[name] || PALETTES.sunset, r = rng(seed), W = 1600, n = P.ridges.length, id = name + seed;
  const stops = P.sky.map((c, i) => `<stop offset="${(i / (P.sky.length - 1)) * 100}%" stop-color="${c}"/>`).join("");
  let layers = "";
  P.ridges.forEach((color, i) => {
    const base = 470 + i * 78, amp = 60 + i * 12;
    const waves = [1, 2, 3, 5, 7, 11].map((k) => ({ k, a: (r() * amp) / (k * .55 + .6), p: r() * 6.28 }));
    const y = (x) => base - waves.reduce((s, w) => s + w.a * Math.sin((2 * Math.PI * w.k * x) / W + w.p), 0);
    let d = `M0 900 L0 ${y(0).toFixed(1)}`;
    for (let x = 12; x <= W * 2; x += 12) d += ` L${x} ${y(x).toFixed(1)}`;
    d += ` L${W * 2} 900 Z`;
    let trees = "";
    if (i >= n - 2) { // pine trees along the closest ridges
      for (let t = 0; t < 70; t++) {
        const x = r() * W, h = 14 + r() * (i === n - 1 ? 34 : 18), w = h * .38;
        [x, x + W].forEach((xx) => { const yy = y(xx) + 4; trees += `M${(xx - w).toFixed(1)} ${yy.toFixed(1)} L${xx.toFixed(1)} ${(yy - h).toFixed(1)} L${(xx + w).toFixed(1)} ${yy.toFixed(1)} Z `; });
      }
    }
    const dur = 260 - i * 38;
    layers += `<g class="layer" style="animation-duration:${dur}s"><path d="${d}" fill="${color}"/>${trees ? `<path d="${trees}" fill="${color}"/>` : ""}</g>`;
    if (i < n - 1) layers += `<rect x="0" y="${base - 40}" width="${W}" height="${900 - base + 40}" fill="url(#haze${id})" opacity=".35"/>`;
  });
  const birds = name === "night" ? "" : [0, 1, 2].map((b) => `<path class="bird" style="animation-delay:-${b * 6 + r() * 4}s" d="M${b * 26} ${210 + b * 18} q8 -8 16 0 q8 -8 16 0" fill="none" stroke="rgba(30,20,30,.55)" stroke-width="2"/>`).join("");
  return `<svg viewBox="0 0 ${W} 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs><linearGradient id="sky${id}" x1="0" y1="0" x2="0" y2="1">${stops}</linearGradient>
      <radialGradient id="sun${id}"><stop offset="0%" stop-color="${P.sun}" stop-opacity="1"/><stop offset="18%" stop-color="${P.sun}" stop-opacity=".9"/><stop offset="100%" stop-color="${P.sun}" stop-opacity="0"/></radialGradient>
      <linearGradient id="haze${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${P.sky[P.sky.length - 1]}" stop-opacity="0"/><stop offset="100%" stop-color="${P.sky[P.sky.length - 1]}" stop-opacity=".9"/></linearGradient></defs>
    <rect width="${W}" height="900" fill="url(#sky${id})"/>
    <circle class="sun" cx="${P.moon ? 1180 : 1040}" cy="${P.sunY}" r="${P.moon ? 140 : 300}" fill="url(#sun${id})"/>
    ${P.moon ? `<circle cx="1180" cy="${P.sunY}" r="34" fill="#f4f1e8"/>` : ""}
    ${birds}${layers}</svg>`;
}

document.addEventListener("DOMContentLoaded", () => {
  const $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  $$(".scene").forEach((el, i) => {
    el.innerHTML = mountainSVG(el.dataset.scene, 11 + i * 17);
    // Only the top section of each page moves; scenes further down stay still so the site stays smooth
    if (!el.closest(".hero, .page-hero, .tools")) el.classList.add("still");
  });

  // Optional hero video
  $$(".hero-video[data-src]").forEach((v) => {
    const tune = VIDEO_TUNING[v.dataset.src] || {}, start = tune.start || 0, rate = tune.rate || 1;
    const setRate = () => { v.defaultPlaybackRate = rate; v.playbackRate = rate; };
    if (start) {
      // Skip the opening seconds, including every time the clip loops
      v.loop = false;
      v.addEventListener("loadedmetadata", () => { v.currentTime = start; }, { once: true });
      v.addEventListener("ended", () => { v.currentTime = start; setRate(); v.play().catch(() => {}); });
    }
    v.addEventListener("loadeddata", () => { v.hidden = false; v.classList.add("ready"); setRate(); v.play().catch(() => {}); }, { once: true });
    v.src = v.dataset.src;
  });

  // Headlines: words slide up one by one
  const isHome = !!$(".curtain");
  $$(".split-words").forEach((h) => {
    const parts = h.innerHTML.split(/(<em>.*?<\/em>|\s+)/).filter((p) => p && p.trim());
    const start = isHome ? 1.5 : 0.3;
    h.innerHTML = parts.map((p, i) => `<span class="w"><span style="animation-delay:${start + i * 0.14}s">${p}</span></span>`).join(" ");
  });
  [".hero-copy .kicker", ".hero-sub", ".hero-btns", ".trace-line", ".hero-stats", ".glass-card"].forEach((q, i) => {
    const el = $(q);
    if (el) el.style.animationDelay = `${1.4 + i * 0.18}s`;
  });

  // Words light up as you scroll
  $$(".words").forEach((words) => {
    words.innerHTML = words.innerHTML.split(/(<em>.*?<\/em>|\s+)/).filter((w) => w && w.trim()).map((w) => `<span class="wd">${w}</span>`).join(" ");
    const spans = $$(".wd", words);
    const lightUp = () => {
      const r = words.getBoundingClientRect(), vh = innerHeight;
      const prog = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      spans.forEach((sp, i) => sp.classList.toggle("lit", i / spans.length < prog));
    };
    addEventListener("scroll", lightUp, { passive: true });
    lightUp();
  });

  // Count-up numbers
  const countUp = (el) => {
    if (el.dataset.done) return;
    el.dataset.done = 1;
    const end = +el.dataset.count, pre = el.dataset.prefix || "", suf = el.dataset.suffix || "", t0 = performance.now();
    const step = (t) => {
      const p = Math.min(1, (t - t0) / 1800), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + Math.round(end * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  // Reveal on scroll (+ start counters)
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    e.target.classList.add("in");
    $$("[data-count]", e.target).forEach(countUp);
    io.unobserve(e.target);
  }), { threshold: 0.15 });
  $$(".reveal").forEach((el) => io.observe(el));
  setTimeout(() => $$(".hero-stats [data-count]").forEach(countUp), 2200);

  // Listing rails: arrows, progress bar, gentle auto-glide
  $$(".listings").forEach((sec) => {
    const rail = $(".rail", sec), bar = $(".progress span", sec);
    if (!rail) return;
    const card = () => (($(".home-card", rail) || {}).offsetWidth || 400) + 24;
    const next = $(".arr.next", sec), prev = $(".arr.prev", sec);
    if (next) next.addEventListener("click", () => rail.scrollBy({ left: card() }));
    if (prev) prev.addEventListener("click", () => rail.scrollBy({ left: -card() }));
    const upd = () => {
      const max = rail.scrollWidth - rail.clientWidth;
      if (bar) bar.style.width = `${25 + 75 * (max ? rail.scrollLeft / max : 0)}%`;
    };
    rail.addEventListener("scroll", upd, { passive: true });
    upd();
    if (rail.scrollWidth > rail.clientWidth + 10) {
      const auto = setInterval(() => {
        if (rail.scrollLeft >= rail.scrollWidth - rail.clientWidth - 4) rail.scrollTo({ left: 0 });
        else rail.scrollBy({ left: card() });
      }, 4500);
      ["pointerdown", "wheel", "touchstart"].forEach((ev) => rail.addEventListener(ev, () => clearInterval(auto), { once: true, passive: true }));
    }
  });

  // Area panels: expand on hover; tap an open panel to visit that area
  $$(".panels").forEach((group) => {
    const ps = $$(".panel", group);
    ps.forEach((p) => {
      p.addEventListener("mouseenter", () => ps.forEach((q) => q.classList.toggle("open", q === p)));
      p.addEventListener("click", (e) => {
        if (e.target.closest("a")) return;
        if (p.classList.contains("open") && p.dataset.href) location.href = p.dataset.href;
        else ps.forEach((q) => q.classList.toggle("open", q === p));
      });
    });
  });

  // One-line reviews: fast, shuffled, never repeats until every line has been shown
  $$(".quote-strip").forEach((strip) => {
    const items = $$(".qs", strip);
    if (!items.length) return;
    let bag = [], cur = -1;
    const next = () => {
      if (!bag.length) { bag = items.map((_, i) => i).sort(() => Math.random() - .5); if (bag[0] === cur && bag.length > 1) bag.push(bag.shift()); }
      const n = bag.shift();
      if (cur >= 0) items[cur].classList.remove("on");
      items[n].classList.add("on"); cur = n;
    };
    next(); setInterval(next, 4000);
  });

  // Reviews rotate
  const qs = $$(".q"), bars = $$(".q-bars i");
  if (qs.length > 1) {
    let qi = 0;
    setInterval(() => {
      qs[qi].classList.remove("on");
      if (bars[qi]) bars[qi].classList.remove("on");
      qi = (qi + 1) % qs.length;
      qs[qi].classList.add("on");
      if (bars[qi]) { void bars[qi].offsetWidth; bars[qi].classList.add("on"); }
    }, 7000);
  }

  // Mortgage calculator
  if ($("#c-price")) {
    const money = (n) => "$" + Math.round(n).toLocaleString("en-US");
    const calc = () => {
      const price = +$("#c-price").value || 0, down = (+$("#c-down").value || 0) / 100;
      const r = (+$("#c-rate").value || 0) / 100 / 12, n = (+$("#c-term").value || 30) * 12, extra = +$("#c-extra").value || 0;
      const loan = price * (1 - down), pi = r ? loan * r / (1 - Math.pow(1 + r, -n)) : loan / n;
      $("#c-pay").textContent = money(pi + extra);
      $("#c-pi").textContent = money(pi);
      $("#c-ti").textContent = money(extra);
      $("#c-loan").textContent = money(loan);
    };
    $$(".calc input").forEach((el) => el.addEventListener("input", calc));
    calc();
  }

  // Nav darkens after scrolling; cursor glow follows the mouse
  const nav = $(".nav-wrap"), glow = $(".cursor-glow");
  addEventListener("scroll", () => { if (nav) nav.classList.toggle("scrolled", scrollY > 80); }, { passive: true });
  if (glow) addEventListener("pointermove", (e) => { glow.style.left = e.clientX + "px"; glow.style.top = e.clientY + "px"; }, { passive: true });

  // Cover text drifts as you scroll
  const copy = $(".hero-copy") || $(".ph-copy");
  if (copy) addEventListener("scroll", () => { if (scrollY < innerHeight) copy.style.transform = `translateY(${scrollY * 0.25}px)`; }, { passive: true });

  // Lead forms
  $$(".lead-form").forEach((f) => f.addEventListener("submit", async (e) => {
    e.preventDefault();
    // Forms marked data-need-contact accept a phone number OR an email
    if (f.hasAttribute("data-need-contact")) {
      const ph = f.querySelector('[name="phone"]'), em = f.querySelector('[name="email"]'), note = f.querySelector(".form-note");
      if (!ph.value.trim() && !em.value.trim()) {
        if (note) { note.textContent = "Please add a phone number or an email so Nolan can reach you."; note.classList.add("err"); }
        ph.focus(); return;
      }
      if (note) { note.textContent = "Phone or email, whichever you prefer."; note.classList.remove("err"); }
    }
    const data = new FormData(f), btn = $("button", f);
    const showGuide = () => {
      if (f.dataset.guide && !f.parentElement.querySelector(".guide-dl"))
        f.insertAdjacentHTML("afterend", `<a class="pill light guide-dl" style="margin-top:1.2rem" href="${f.dataset.guide}" download>Download your guide</a>`);
    };
    if (FORM_ENDPOINT) {
      const label = btn.textContent;
      btn.textContent = "Sending..."; btn.disabled = true;
      const payload = Object.fromEntries(data);
      payload._subject = "Website lead: " + (f.dataset.subject || "message");
      payload._template = "table"; payload._captcha = "false";
      payload.page = location.href;
      try {
        const r = await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) });
        const res = await r.json().catch(() => ({}));
        // FormSubmit answers HTTP 200 even when it did not deliver (e.g. form not activated yet)
        if (!r.ok || String(res.success) !== "true") throw new Error(res.message || "not delivered");
        f.reset(); btn.textContent = "Sent! Nolan will be in touch."; showGuide();
        setTimeout(() => { btn.textContent = label; btn.disabled = false; }, 6000);
      } catch (err) {
        btn.disabled = false; btn.textContent = "Couldn't send. Call or text 828-404-5335";
      }
      return;
    }
    showGuide();
    const body = [...data].map(([k, val]) => `${k}: ${val}`).join("\n");
    location.href = `mailto:${LEAD_EMAIL}?subject=${encodeURIComponent(f.dataset.subject)}&body=${encodeURIComponent(body)}`;
  }));
});

/* Mobile menu */
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".menu-btn"), menu = document.getElementById("mobile-menu");
  if (!btn || !menu) return;
  const set = (open) => {
    document.body.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", open); btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.setAttribute("aria-hidden", !open);
    btn.querySelector(".menu-word").textContent = open ? "Close" : "Menu";
  };
  btn.addEventListener("click", () => set(!document.body.classList.contains("menu-open")));
  menu.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
  addEventListener("keydown", (e) => { if (e.key === "Escape") set(false); });
  addEventListener("pageshow", () => set(false));
});
