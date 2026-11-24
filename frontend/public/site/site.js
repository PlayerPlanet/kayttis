// Hanax landing page: theme toggle, video fallback, and the "Sammuta kaikki" panel demo.
// No dependencies, no network requests beyond this site's own files.
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---- Theme toggle (system default; choice remembered per browser) ---- */
  var themeBtn = document.getElementById("theme");
  if (themeBtn) {
    var systemDark = window.matchMedia("(prefers-color-scheme: dark)");
    var current = function () {
      return root.dataset.theme || (systemDark.matches ? "dark" : "light");
    };
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
    systemDark.addEventListener && systemDark.addEventListener("change", label);
  }

  /* ---- Video: degrade gracefully if the file is not there yet ---- */
  var device = document.querySelector(".device");
  var video = device && device.querySelector("video");
  if (video) {
    var missing = device.querySelector(".video-missing");
    var fail = function () {
      device.classList.add("is-missing");
      if (missing) missing.hidden = false;
      var c = device.querySelector(".video-fallback");
      if (c) c.hidden = false;
    };
    var source = video.querySelector("source");
    if (source) source.addEventListener("error", fail);
    video.addEventListener("error", fail);
    // Until the poster is known to exist, cover the empty frame with a designed
    // fallback that doubles as the play button. A real poster replaces it.
    var cover = device.querySelector(".video-fallback");
    var poster = video.getAttribute("poster");
    var showCover = function () {
      video.removeAttribute("poster");
      if (cover && !video.currentTime) cover.hidden = false;
    };
    if (poster) {
      var probe = new Image();
      probe.onerror = showCover;
      probe.src = poster;
    } else {
      showCover();
    }
    if (cover) {
      cover.addEventListener("click", function () {
        cover.hidden = true;
        var p = video.play();
        if (p && p.catch) p.catch(function () { video.focus(); });
      });
      video.addEventListener("play", function () { cover.hidden = true; });
    }
  }

  /* ---- Panel demo ---- */
  var panel = document.getElementById("panel");
  if (!panel) return;
  var offBtn = document.getElementById("all-off");
  var resetBtn = document.getElementById("reset");
  var devices = Array.prototype.slice.call(panel.querySelectorAll(".dev"));
  var initial = devices.map(function (d) { return d.dataset.on; });
  var ages = Array.prototype.slice.call(panel.querySelectorAll("[data-age]"));
  var timers = [];

  function clearTimers() { timers.forEach(clearTimeout); timers = []; }

  function allOff() {
    clearTimers();
    offBtn.disabled = true;
    var on = devices.filter(function (d) { return d.dataset.on === "true"; });
    var step = reduceMotion.matches ? 0 : 450;
    on.forEach(function (d, i) {
      timers.push(setTimeout(function () {
        d.dataset.on = "false";
        var age = d.querySelector("[data-age]");
        if (age) { age.dataset.age = "0"; age.textContent = "0"; }
      }, step * (i + 1)));
    });
    timers.push(setTimeout(function () {
      panel.dataset.state = "off";
      offBtn.hidden = true;
      resetBtn.hidden = false;
      resetBtn.focus({ preventScroll: true });
    }, step * (on.length + 1)));
  }

  function reset() {
    clearTimers();
    devices.forEach(function (d, i) { d.dataset.on = initial[i]; });
    panel.dataset.state = "on";
    offBtn.disabled = false;
    offBtn.hidden = false;
    resetBtn.hidden = true;
    offBtn.focus({ preventScroll: true });
  }

  offBtn.hidden = false;
  offBtn.addEventListener("click", allOff);
  resetBtn.addEventListener("click", reset);

  // Freshness readouts tick like the real panel: sensors report every ~15 s.
  // Text-only change, so it also runs with reduced motion; paused when off-screen.
  var visible = false;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
    }).observe(panel);
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
})();
