// Hanax landing page v2: hero reveal video (if present), scroll reveals, film dialog, proof-video slot,
// theme toggle, and the "Sammuta kaikki" panel demo. No dependencies; no requests
// beyond this site's own static files (never /api: it needs the demo login).
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  /* ---- Theme toggle (system default; ?tema=light|dark or the button overrides) ---- */
  var themeBtn = $("#theme");
  if (themeBtn) {
    var systemDark = window.matchMedia("(prefers-color-scheme: dark)");
    var current = function () { return root.dataset.theme || (systemDark.matches ? "dark" : "light"); };
    var label = function () {
      var next = current() === "dark" ? "vaalea" : "tumma";
      themeBtn.setAttribute("aria-label", "Vaihda " + next + " teema");
      themeBtn.title = "Vaihda " + next + " teema";
    };
    themeBtn.hidden = false;
    label();
    themeBtn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("hanax.theme", next); } catch (e) { /* storage unavailable */ }
      label();
    });
    if (systemDark.addEventListener) systemDark.addEventListener("change", label);
  }

  /* ---- Hero: play the reveal once, hold the lit last frame. Falls back to the still. ---- */
  var heroVideo = $(".hero-video");
  if (heroVideo && root.classList.contains("motion")) {
    var settled = false;
    var toStill = function () {
      if (settled) return;
      settled = true;
      root.classList.remove("motion");
    };
    var timer = setTimeout(toStill, 4000);
    heroVideo.addEventListener("playing", function () { settled = true; clearTimeout(timer); }, { once: true });
    heroVideo.addEventListener("error", toStill);
    heroVideo.src = heroVideo.dataset.src;
    var p = heroVideo.play();
    if (p && p.catch) p.catch(toStill);
  }

  /* ---- Turntable loop: plays only while visible and motion is welcome ---- */
  var loops = $$(".loop-video");
  if (loops.length && "IntersectionObserver" in window) {
    var loopIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting && !reduceMotion.matches) {
          if (!v.src) v.src = v.dataset.src;
          var q = v.play();
          if (q && q.catch) q.catch(function () {});
        } else if (!v.paused) {
          v.pause();
        }
      });
    }, { threshold: 0.35 });
    loops.forEach(function (v) { loopIO.observe(v); });
  }

  /* ---- Scroll reveals: only hide what is below the fold, so nothing flashes ---- */
  var rv = $$(".rv");
  if (rv.length && "IntersectionObserver" in window && !reduceMotion.matches) {
    var vh = window.innerHeight;
    rv.forEach(function (el) { if (el.getBoundingClientRect().top < vh * 0.92) el.classList.add("in"); });
    var rvIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); rvIO.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rv.forEach(function (el) { if (!el.classList.contains("in")) rvIO.observe(el); });
    root.classList.add("rv-ready");
  }

  /* ---- Film dialog (60 s video). Without JS the link opens the MP4 directly. ---- */
  var film = $("#film");
  if (film && typeof film.showModal === "function") {
    var fv = $("video", film);
    var missing = $(".film-missing", film);
    var fail = function () { if (missing) missing.hidden = false; };
    var src = $("source", fv);
    if (src) src.addEventListener("error", fail);
    fv.addEventListener("error", fail);
    var opener = null;
    $$("[data-film]").forEach(function (a) {
      a.addEventListener("click", function (ev) {
        ev.preventDefault();
        opener = a;
        film.showModal();
        var q = fv.play();
        if (q && q.catch) q.catch(function () { fv.focus(); });
      });
    });
    var closeFilm = function () { film.close(); };
    $("#film-close").addEventListener("click", closeFilm);
    film.addEventListener("click", function (ev) { if (ev.target === film) closeFilm(); });
    film.addEventListener("close", function () { fv.pause(); if (opener) opener.focus(); });
  }

  /* ---- Proof video slot: appears only once /media/proof-kitchen.mp4 really loads ---- */
  var proof = $("#proof-video");
  if (proof) {
    var pv = $("video", proof);
    pv.preload = "metadata";
    pv.addEventListener("loadedmetadata", function () {
      if (pv.dataset.poster) {
        var img = new Image();
        img.onload = function () { pv.poster = pv.dataset.poster; };
        img.src = pv.dataset.poster;
      }
      proof.hidden = false;
      proof.classList.add("in");
    }, { once: true });
    pv.addEventListener("error", function () { proof.remove(); }, { once: true });
    pv.src = pv.dataset.src;
  }

  /* ---- Freshness readouts tick like the real app (text only; paused off-screen) ---- */
  function ticker(scope) {
    var ages = $$("[data-age]", scope);
    var visible = false;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; }).observe(scope);
    }
    setInterval(function () {
      if (!visible || document.hidden) return;
      ages.forEach(function (el) {
        var n = (parseInt(el.dataset.age, 10) || 0) + 1;
        if (n > 15 + (el.textContent.length % 3) * 7) n = 1;
        el.dataset.age = String(n);
        el.textContent = String(n);
      });
    }, 1000);
  }
  var readout = $(".readout");
  if (readout) ticker(readout);

  /* ---- Panel demo: the knob turns everything off, one row at a time ---- */
  var panel = $("#panel");
  if (!panel) return;
  ticker(panel);
  var knob = $("#all-off");
  if (!knob) return; // phone view: monitoring only, no knob
  var resetBtn = $("#reset");
  var hint = $("#knob-hint");
  var n = $(".sum-n", panel);
  var devices = $$(".dev", panel);
  var initial = devices.map(function (d) { return d.dataset.on; });
  var timers = [];
  var clearTimers = function () { timers.forEach(clearTimeout); timers = []; };
  knob.disabled = false;
  var countOn = function () { return devices.filter(function (d) { return d.dataset.on === "true"; }).length; };

  knob.addEventListener("click", function () {
    clearTimers();
    knob.disabled = true;
    var on = devices.filter(function (d) { return d.dataset.on === "true"; });
    var step = reduceMotion.matches ? 0 : 420;
    on.forEach(function (d, i) {
      timers.push(setTimeout(function () {
        d.dataset.on = "false";
        var age = $("[data-age]", d);
        if (age) { age.dataset.age = "0"; age.textContent = "0"; }
        if (n) n.textContent = String(countOn());
      }, step * (i + 1)));
    });
    timers.push(setTimeout(function () {
      panel.dataset.state = "off";
      hint.textContent = "Kaikki pois";
      resetBtn.hidden = false;
      resetBtn.focus({ preventScroll: true });
    }, step * (on.length + 1)));
  });

  resetBtn.addEventListener("click", function () {
    clearTimers();
    devices.forEach(function (d, i) { d.dataset.on = initial[i]; });
    if (n) n.textContent = String(countOn());
    panel.dataset.state = "on";
    hint.textContent = "Paina: kaikki pois";
    knob.disabled = false;
    resetBtn.hidden = true;
    knob.focus({ preventScroll: true });
  });
})();
