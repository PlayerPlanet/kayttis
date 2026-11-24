/* Hanax print kit: renders the panel UI mock, indicator-light grids and state chips.
   Usage: <div data-panel="on|safe" data-variant="phone"></div>, <div data-lights="5"></div>,
   <span data-chip="on|off|safe"></span> */
(function () {
  var ICON = {
    hana: '<path d="M5 9h9a4 4 0 0 1 4 4v1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M9 9V6M6 6h6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M18 17.5c0 1.2-.7 2-1.5 2s-1.5-.8-1.5-2 1.5-3 1.5-3 1.5 1.8 1.5 3z" FILL/>',
    liesi: '<rect x="3.5" y="3.5" width="17" height="17" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="9" cy="9" r="2.2" FILL/><circle cx="15" cy="9" r="2.2" FILL/><circle cx="9" cy="15" r="2.2" FILL/><circle cx="15" cy="15" r="2.2" FILL/>',
    valo: '<path d="M12 3.5a5.5 5.5 0 0 0-3.2 10c.7.5 1.2 1.3 1.2 2.1V17h4v-1.4c0-.8.5-1.6 1.2-2.1A5.5 5.5 0 0 0 12 3.5z" FILL stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M10 20.5h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    kahvi: '<path d="M5 8h11v6a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5z" FILL stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M16 10h1.5a2.5 2.5 0 0 1 0 5H16" fill="none" stroke="currentColor" stroke-width="2"/>',
    pesu: '<rect x="4" y="3.5" width="16" height="17" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="13" r="4" FILL stroke="currentColor" stroke-width="2"/><path d="M7.5 7h2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    pois: '<circle cx="12" cy="12" r="7.5" fill="none" stroke="currentColor" stroke-width="2"/>',
    paalla: '<circle cx="12" cy="12" r="8" fill="currentColor"/>',
    kysymys: '<path d="M9 9a3 3 0 1 1 4 2.8c-.7.3-1 .9-1 1.6V14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="18" r="1.3" fill="currentColor"/>'
  };
  function icon(name, filled) {
    var body = ICON[name].replace(/FILL/g, filled ? 'fill="currentColor"' : 'fill="none" stroke="currentColor" stroke-width="2"');
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + body + '</svg>';
  }
  function chip(state) {
    if (state === 'on') return '<span class="chip on">' + icon('paalla') + 'Päällä</span>';
    if (state === 'safe') return '<span class="chip safe">' + icon('check') + 'Kaikki kiinni</span>';
    if (state === 'unknown') return '<span class="chip unknown">' + icon('kysymys') + 'Ei tietoa · 5 min</span>';
    return '<span class="chip off">' + icon('pois') + 'Pois</span>';
  }
  function dev(ic, name, on, fresh) {
    return '<div class="dev' + (on ? ' is-on' : '') + '"><div class="ico">' + icon(ic, on) + '</div>' +
      '<div><div class="nm">' + name + '</div><div class="fr">' + fresh.replace(/(\d+) s sitten/, '<span class="nb">$1 s sitten</span>') + '</div></div>' + chip(on ? 'on' : 'off') + '</div>';
  }
  function panel(state, compact) {
    var on = state === 'on';
    var h = '<div class="screen">';
    h += '<div class="scr-top"><div class="home"><img src="../../../brand/logo/hanax-mark.svg" alt="">Koti</div><div class="clock">13.56</div></div>';
    if (on) {
      h += '<div class="summary on"><div><div class="big">2 laitetta päällä</div><div class="sub">tarkistettu 12 s sitten</div></div><span class="okbadge onbadge">' + icon('paalla') + '</span></div>';
    } else {
      h += '<div class="summary safe"><div><div class="big">Kaikki kiinni</div><div class="sub">tarkistettu 4 s sitten</div></div><span class="okbadge">' + icon('check') + '</span></div>';
    }
    h += '<div class="room"><div class="room-name">Keittiö</div>';
    h += dev('hana', 'Keittiön hana', on, on ? 'tarkistettu 12 s sitten' : 'tarkistettu 4 s sitten');
    h += dev('liesi', 'Liesi', on, on ? 'tarkistettu 12 s sitten' : 'tarkistettu 4 s sitten');
    if (!compact) h += dev('kahvi', 'Kahvinkeitin', false, 'tarkistettu 12 s sitten');
    h += '</div>';
    if (!compact) {
      h += '<div class="room"><div class="room-name">Kodinhoitohuone</div>';
      h += dev('pesu', 'Pesukoneen hana', false, 'tarkistettu 12 s sitten') + '</div>';
      h += '<div class="room"><div class="room-name">Olohuone</div>';
      h += dev('valo', 'Valot', false, 'tarkistettu 12 s sitten') + '</div>';
    }
    h += on ? '<div class="allbtn"><span class="knob"></span>Sammuta kaikki</div>'
            : '<div class="allbtn done">Ei mitään sammutettavaa</div>';
    return h + '</div>';
  }
  document.querySelectorAll('[data-panel]').forEach(function (el) {
    var phone = el.getAttribute('data-variant') === 'phone';
    el.classList.add('device');
    if (phone) el.classList.add('phone');
    el.innerHTML = (phone ? '' : '<span class="cam"></span>') + panel(el.getAttribute('data-panel'), el.hasAttribute('data-compact'));
  });
  document.querySelectorAll('[data-lights]').forEach(function (el) {
    var lit = (el.getAttribute('data-lights') || '').split(',').filter(function (x) { return x !== ''; }).map(Number);
    var safe = el.hasAttribute('data-safe');
    el.classList.add('lights');
    var h = '';
    for (var i = 0; i < 12; i++) h += '<span class="dot' + (lit.indexOf(i) >= 0 ? (safe ? ' safe' : ' lit') : '') + '"></span>';
    el.innerHTML = h;
  });
  document.querySelectorAll('[data-chip]').forEach(function (el) { el.outerHTML = chip(el.getAttribute('data-chip')); });
  document.querySelectorAll('[data-icon]').forEach(function (el) {
    el.innerHTML = icon(el.getAttribute('data-icon'), el.hasAttribute('data-filled'));
  });
})();
