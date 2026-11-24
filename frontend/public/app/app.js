// käyttis smart-home prototype.
//
// Switching is SIMULATED in the browser (kept in localStorage). The backend is read-only:
// a device may be "connected" to a backend device id, and then its live state is shown
// as a secondary line, but nothing here ever asks the backend to switch anything.

import { ICONS, TYPE_LABELS, CHEVRON, CAMERA } from "./icons.js";

const STORAGE_KEY = "kayttis.home.v1";
const API = "/api";
const CAMERAS = {
  main: { label: "Guild room camera", url: `${API}/camera/latest.jpg` },
};
const CAMERA_REFRESH_MS = 3000;
const POLL_OFFLINE_MS = 15000; // API unreachable: retry now and then
const POLL_NO_STREAM_MS = 5000; // API up but the event stream is not: poll instead
const POLL_WITH_STREAM_MS = 30000; // safety net while the stream is open
const TOAST_MS = 6000;

const collator = new Intl.Collator("fi", { sensitivity: "base", numeric: true });
const $ = (sel) => document.querySelector(sel);
const esc = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const uid = (prefix) => `${prefix}-${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;

// ---------------------------------------------------------------- state & storage

function seed() {
  const rooms = [
    { id: "kitchen", name: "Keittiö" },
    { id: "living", name: "Olohuone" },
    { id: "bath", name: "Kylpyhuone" },
  ];
  const d = (id, room, name, type, on, connection = null) => ({ id, room, name, type, on, connection, camera: "main" });
  const devices = [
    d("d-coffee-left", "kitchen", "Vasen kahvinkeitin", "electric", true, "coffee_machine_left"),
    d("d-coffee-right", "kitchen", "Oikea kahvinkeitin", "electric", false, "coffee_machine_right"),
    d("d-dish-tap", "kitchen", "Astianpesukoneen hana", "faucet", false, "dishwasher_tap"),
    d("d-kitchen-ceiling", "kitchen", "Kattovalo", "lamp", true, "lights"),
    d("d-oven", "kitchen", "Uuni", "electric", false),
    d("d-floor-lamp", "living", "Lattiavalo", "lamp", true),
    d("d-reading-lamp", "living", "Lukuvalo", "lamp", false),
    d("d-tv", "living", "Televisio", "electric", false),
    d("d-bath-tap", "bath", "Lavuaarin hana", "faucet", false),
    d("d-mirror-lamp", "bath", "Peilivalo", "lamp", false),
  ];
  return { version: 1, house: "My home", rooms, devices, collapsed: {} };
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const s = JSON.parse(raw);
      if (s && s.version === 1 && Array.isArray(s.rooms) && Array.isArray(s.devices)) {
        s.collapsed ??= {};
        return s;
      }
    }
  } catch {
    /* storage unavailable or corrupt: start from the seed */
  }
  return seed();
}

function save() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    /* private mode / storage blocked: the page keeps working for this visit */
  }
}

let state = load();

const live = {
  status: "connecting", // connecting | online | offline
  devices: new Map(), // backend id -> DeviceState
  stream: null,
  streamFailedAt: 0,
};

// ---------------------------------------------------------------- helpers

const roomName = (id) => state.rooms.find((r) => r.id === id)?.name ?? "";
const deviceById = (id) => state.devices.find((d) => d.id === id);

function sortDevices(list) {
  // on before off; alphabetical within each group
  return [...list].sort((a, b) => Number(b.on) - Number(a.on) || collator.compare(a.name, b.name));
}

function fmtNumber(v) {
  if (typeof v !== "number" || !Number.isFinite(v)) return null;
  return Math.abs(v) >= 10 ? String(Math.round(v)) : String(Math.round(v * 10) / 10);
}

/** "Live: brewing · 1400 W", or null if the device is not connected. */
function liveLine(dev) {
  if (!dev.connection) return null;
  if (live.status !== "online") return { text: "Live: offline", ok: false };
  const s = live.devices.get(dev.connection);
  if (!s) return { text: "Live: no data", ok: false };
  const parts = [s.state ?? "unknown"];
  const n = fmtNumber(s.value);
  if (n !== null) parts.push(s.unit ? `${n} ${s.unit}` : n);
  let text = `Live: ${parts.join(" · ")}`;
  if (s.stale) text += " (stale)";
  return { text, ok: !s.stale && s.state !== "unknown" };
}

function typeForKind(kind) {
  if (kind === "light") return "lamp";
  if (kind === "valve") return "faucet";
  return "electric";
}

function announce(msg) {
  const el = $("#announce");
  el.textContent = "";
  // a fresh text node makes screen readers re-announce identical messages
  requestAnimationFrame(() => (el.textContent = msg));
}

// ---------------------------------------------------------------- rendering

function deviceHTML(dev) {
  const icon = ICONS[dev.type]?.[dev.on ? "on" : "off"] ?? ICONS.electric[dev.on ? "on" : "off"];
  const ll = liveLine(dev);
  const stateText = dev.on ? "On" : "Off";
  return `
    <li class="device ${dev.on ? "is-on" : "is-off"}" data-id="${esc(dev.id)}">
      <button type="button" class="toggle" data-action="toggle" data-focus="t:${esc(dev.id)}"
        aria-pressed="${dev.on}" aria-label="Power: ${esc(dev.name)}"
        title="${dev.on ? "Turn off" : "Turn on"}">${icon}</button>
      <button type="button" class="row-main" data-action="camera" data-focus="c:${esc(dev.id)}">
        <span class="row-text">
          <span class="dev-name">${esc(dev.name)}</span>
          <span class="dev-meta"><span class="dev-state">${stateText}</span> · ${esc(TYPE_LABELS[dev.type] ?? "Device")}</span>
          ${ll ? `<span class="dev-live ${ll.ok ? "is-live" : ""}">${esc(ll.text)}</span>` : ""}
          <span class="sr-only">. Show camera</span>
        </span>
        <span class="cam-hint" aria-hidden="true">${CAMERA}</span>
      </button>
    </li>`;
}

function roomHTML(room) {
  const devs = sortDevices(state.devices.filter((d) => d.room === room.id));
  const on = devs.filter((d) => d.on).length;
  const expanded = !state.collapsed[room.id];
  const listId = `list-${room.id}`;
  return `
    <section class="room" aria-labelledby="h-${esc(room.id)}">
      <h2 id="h-${esc(room.id)}">
        <button type="button" class="room-head" data-action="collapse" data-room="${esc(room.id)}"
          data-focus="r:${esc(room.id)}" aria-expanded="${expanded}" aria-controls="${esc(listId)}">
          <span class="room-name">${esc(room.name)}</span>
          <span class="room-count">${on} of ${devs.length} on</span>
          <span class="chev" aria-hidden="true">${CHEVRON}</span>
        </button>
      </h2>
      <ul class="devices" id="${esc(listId)}" ${expanded ? "" : "hidden"}>
        ${devs.length ? devs.map(deviceHTML).join("") : '<li class="empty">No devices yet.</li>'}
      </ul>
    </section>`;
}

function render() {
  const focusKey = document.activeElement?.dataset?.focus;
  $("#rooms").innerHTML = state.rooms.map(roomHTML).join("");
  const total = state.devices.length;
  const on = state.devices.filter((d) => d.on).length;
  $("#summary").textContent = total
    ? on === 0
      ? `All ${total} devices are off`
      : `${on} of ${total} devices on`
    : "No devices yet";
  if (focusKey) document.querySelector(`[data-focus="${CSS.escape(focusKey)}"]`)?.focus();
  if (camera.deviceId) renderCameraMeta();
}

function renderLiveBadge() {
  const el = $("#live");
  el.dataset.state = live.status;
  $("#live-text").textContent =
    live.status === "online" ? "Live data" : live.status === "offline" ? "Live data offline" : "Connecting…";
  el.title =
    live.status === "offline"
      ? "Sensor data from the guild room is not reachable right now. Everything else works as usual."
      : "Live data from the guild room sensors";
}

// ---------------------------------------------------------------- actions

function setOn(dev, on) {
  dev.on = on;
  save();
  render();
  announce(`${dev.name} turned ${on ? "on" : "off"}`);
}

let toastTimer = 0;
let toastUndo = null;
function toast(text, undo = null) {
  $("#toast-text").textContent = text;
  toastUndo = undo;
  $("#toast-undo").hidden = !undo;
  $("#toast").hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(hideToast, undo ? TOAST_MS + 2000 : TOAST_MS);
}
function hideToast() {
  $("#toast").hidden = true;
  toastUndo = null;
}
$("#toast-undo").addEventListener("click", () => {
  const fn = toastUndo;
  hideToast();
  fn?.();
});

function goAway() {
  const wasOn = state.devices.filter((d) => d.on).map((d) => d.id);
  if (!wasOn.length) {
    toast("Away mode: everything is already off.");
    return;
  }
  for (const d of state.devices) d.on = false;
  save();
  render();
  toast(`Away mode: turned off ${wasOn.length} device${wasOn.length === 1 ? "" : "s"}.`, () => {
    for (const id of wasOn) {
      const d = deviceById(id);
      if (d) d.on = true;
    }
    save();
    render();
    toast("Restored the devices that were on.");
  });
}

$("#away").addEventListener("click", goAway);

$("#rooms").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-action]");
  if (!btn) return;
  const action = btn.dataset.action;
  if (action === "collapse") {
    const id = btn.dataset.room;
    state.collapsed[id] = !state.collapsed[id];
    save();
    render();
    return;
  }
  const dev = deviceById(btn.closest(".device")?.dataset.id);
  if (!dev) return;
  if (action === "toggle") setOn(dev, !dev.on);
  else if (action === "camera") openCamera(dev.id);
});

$("#reset").addEventListener("click", () => {
  if (!confirm("Reset the demo? Added devices are removed and every device returns to its starting state.")) return;
  state = seed();
  save();
  render();
  toast("Demo data reset.");
});

// ---------------------------------------------------------------- dialogs (shared)

for (const dlg of document.querySelectorAll("dialog")) {
  dlg.addEventListener("click", (e) => {
    if (e.target.closest("[data-close]")) dlg.close();
    else if (e.target === dlg) dlg.close(); // click on the backdrop
  });
}

function focusRow(devId, cls = "row-main") {
  const el = document.querySelector(`.device[data-id="${CSS.escape(devId)}"] .${cls}`);
  el?.focus();
  return el;
}

// ---------------------------------------------------------------- camera view

const camera = { deviceId: null, timer: 0, token: 0, objectUrl: null };
const camDlg = $("#camera");

function renderCameraMeta() {
  const dev = deviceById(camera.deviceId);
  if (!dev) return;
  $("#cam-title").textContent = dev.name;
  const ll = liveLine(dev);
  const parts = [
    `<strong>${dev.on ? "On" : "Off"}</strong> (simulated)`,
    esc(roomName(dev.room)),
    esc(TYPE_LABELS[dev.type] ?? "Device"),
  ];
  $("#cam-meta").innerHTML =
    parts.join(" · ") + `<br>${ll ? esc(ll.text) : "Not connected to live data"}`;
  const t = $("#cam-toggle");
  t.textContent = dev.on ? `Turn off` : `Turn on`;
  t.setAttribute("aria-label", `${dev.on ? "Turn off" : "Turn on"} ${dev.name}`);
}

async function loadFrame() {
  const dev = deviceById(camera.deviceId);
  if (!dev) return;
  const cam = CAMERAS[dev.camera] ?? CAMERAS.main;
  const token = ++camera.token;
  let blob = null;
  let capturedAt = null;
  try {
    const r = await fetch(`${cam.url}?t=${Date.now()}`, { cache: "no-store" });
    if (r.ok && (r.headers.get("content-type") ?? "").startsWith("image/")) {
      blob = await r.blob();
      const ts = Number(r.headers.get("X-Captured-At"));
      if (Number.isFinite(ts) && ts > 0) capturedAt = new Date(ts * 1000);
    }
  } catch {
    /* network error: treated as unavailable */
  }
  if (token !== camera.token) return; // closed or superseded meanwhile
  const img = $("#cam-img");
  if (blob) {
    const url = URL.createObjectURL(blob);
    img.onload = () => {
      if (camera.objectUrl && camera.objectUrl !== url) URL.revokeObjectURL(camera.objectUrl);
      camera.objectUrl = url;
    };
    img.src = url;
    img.alt = `${cam.label}, latest frame`;
    img.hidden = false;
    $("#cam-empty").hidden = true;
    const when = (capturedAt ?? new Date()).toLocaleTimeString("en-GB");
    $("#cam-caption").textContent = `${cam.label} · frame from ${when}`;
  } else {
    img.hidden = true;
    $("#cam-empty").hidden = false;
    $("#cam-empty-sub").textContent =
      live.status === "offline" ? "Live data is offline. Trying again every few seconds." : "Trying again every few seconds.";
    $("#cam-caption").textContent = cam.label;
  }
}

function openCamera(devId) {
  camera.deviceId = devId;
  $("#cam-img").hidden = true;
  $("#cam-img").removeAttribute("src");
  $("#cam-empty").hidden = false;
  $("#cam-empty-sub").textContent = "Loading…";
  $("#cam-caption").textContent = "";
  renderCameraMeta();
  camDlg.showModal();
  loadFrame();
  clearInterval(camera.timer);
  camera.timer = setInterval(loadFrame, CAMERA_REFRESH_MS);
}

camDlg.addEventListener("close", () => {
  clearInterval(camera.timer);
  camera.token++;
  const id = camera.deviceId;
  camera.deviceId = null;
  if (id && deviceById(id)) focusRow(id);
  else $("#add").focus();
});

$("#cam-toggle").addEventListener("click", () => {
  const dev = deviceById(camera.deviceId);
  if (dev) setOn(dev, !dev.on);
});

$("#cam-remove").addEventListener("click", () => {
  const dev = deviceById(camera.deviceId);
  if (!dev) return;
  const idx = state.devices.indexOf(dev);
  state.devices.splice(idx, 1);
  save();
  camDlg.close();
  render();
  toast(`Removed ${dev.name}.`, () => {
    state.devices.splice(Math.min(idx, state.devices.length), 0, dev);
    save();
    render();
  });
});

// ---------------------------------------------------------------- add device

const addDlg = $("#adder");
const form = $("#add-form");
const NEW_ROOM = "__new__";
let lastRoom = null;

function buildTypeOptions() {
  $("#f-types").innerHTML = Object.entries(TYPE_LABELS)
    .map(
      ([value, label], i) => `
      <label class="type-opt">
        <input type="radio" name="type" value="${value}" ${i === 0 ? "checked" : ""}>
        <span>${ICONS[value].on}${esc(label)}</span>
      </label>`,
    )
    .join("");
}

function buildConnectionOptions() {
  const sel = $("#f-conn");
  const keep = sel.value;
  const opts = ['<option value="">Not connected</option>'];
  const backend = [...live.devices.values()].sort((a, b) => collator.compare(a.name ?? a.id, b.name ?? b.id));
  for (const s of backend) {
    const used = state.devices.filter((d) => d.connection === s.id).map((d) => d.name);
    const note = used.length ? ` (used by ${used.join(", ")})` : "";
    opts.push(`<option value="${esc(s.id)}">${esc(s.name ?? s.id)} · ${esc(s.state ?? "unknown")}${esc(note)}</option>`);
  }
  sel.innerHTML = opts.join("");
  if ([...sel.options].some((o) => o.value === keep)) sel.value = keep;
  $("#f-conn-hint").textContent =
    live.status === "online"
      ? backend.length
        ? "Pick a sensor to show its live status under the device. Switching stays simulated."
        : "No live devices found."
      : "Live data is offline, so only “Not connected” is available right now.";
}

function buildRoomOptions(selected) {
  const sel = $("#f-room");
  sel.innerHTML =
    state.rooms.map((r) => `<option value="${esc(r.id)}">${esc(r.name)}</option>`).join("") +
    `<option value="${NEW_ROOM}">+ New room…</option>`;
  sel.value = selected && state.rooms.some((r) => r.id === selected) ? selected : (state.rooms[0]?.id ?? NEW_ROOM);
  syncNewRoom();
}

function syncNewRoom() {
  const isNew = $("#f-room").value === NEW_ROOM;
  $("#new-room-wrap").hidden = !isNew;
  if (!isNew) setError("f-newroom", false);
}

function setError(id, show) {
  $(`#${id}-err`).hidden = !show;
  $(`#${id}`).setAttribute("aria-invalid", show ? "true" : "false");
}

function openAdd() {
  form.reset();
  buildTypeOptions();
  buildConnectionOptions();
  buildRoomOptions(lastRoom);
  $("#f-name").dataset.auto = "";
  setError("f-name", false);
  setError("f-newroom", false);
  addDlg.showModal();
  $("#f-name").focus();
}

$("#add").addEventListener("click", openAdd);
$("#f-room").addEventListener("change", () => {
  syncNewRoom();
  if ($("#f-room").value === NEW_ROOM) $("#f-newroom").focus();
});

$("#f-conn").addEventListener("change", () => {
  const s = live.devices.get($("#f-conn").value);
  if (!s) return;
  // pre-fill from the backend device, but never overwrite a name the user typed
  const name = $("#f-name");
  if (!name.value.trim() || name.dataset.auto) {
    name.value = s.name ?? s.id;
    name.dataset.auto = "1";
    setError("f-name", false);
  }
  const type = typeForKind(s.kind);
  form.querySelector(`input[name="type"][value="${type}"]`).checked = true;
});
$("#f-name").addEventListener("input", (e) => {
  e.target.dataset.auto = "";
  if (e.target.value.trim()) setError("f-name", false);
});
$("#f-newroom").addEventListener("input", (e) => {
  if (e.target.value.trim()) setError("f-newroom", false);
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = $("#f-name").value.trim();
  const roomSel = $("#f-room").value;
  const newRoom = $("#f-newroom").value.trim();
  const nameBad = !name;
  const roomBad = roomSel === NEW_ROOM && !newRoom;
  setError("f-name", nameBad);
  setError("f-newroom", roomBad);
  if (nameBad || roomBad) {
    $(nameBad ? "#f-name" : "#f-newroom").focus();
    return;
  }

  let roomId = roomSel;
  if (roomSel === NEW_ROOM) {
    const existing = state.rooms.find((r) => collator.compare(r.name, newRoom) === 0);
    if (existing) roomId = existing.id;
    else {
      roomId = uid("room");
      state.rooms.push({ id: roomId, name: newRoom });
    }
  }
  const dev = {
    id: uid("d"),
    room: roomId,
    name,
    type: form.querySelector('input[name="type"]:checked')?.value ?? "electric",
    on: false,
    connection: $("#f-conn").value || null,
    camera: "main",
  };
  state.devices.push(dev);
  state.collapsed[roomId] = false; // make sure the new device is visible
  lastRoom = roomId;
  save();
  addDlg.close();
  render();
  const row = focusRow(dev.id);
  row?.closest(".device")?.classList.add("flash");
  row?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  toast(`Added ${dev.name} to ${roomName(roomId)}.`);
});

// ---------------------------------------------------------------- live data (read-only)

let pollTimer = 0;

function setLive(status) {
  if (live.status === status) return;
  live.status = status;
  renderLiveBadge();
  render();
  if (addDlg.open) buildConnectionOptions();
}

function applyDevice(s) {
  if (!s || typeof s.id !== "string") return;
  live.devices.set(s.id, s);
}

function openStream() {
  if (live.stream || typeof EventSource === "undefined") return;
  if (Date.now() - live.streamFailedAt < 30000) return; // stream broke recently: keep polling
  const es = new EventSource(`${API}/stream`);
  live.stream = es;
  let pending = false;
  es.addEventListener("device", (e) => {
    try {
      applyDevice(JSON.parse(e.data));
    } catch {
      return;
    }
    // batch the initial burst (every device once) into one render
    if (!pending) {
      pending = true;
      requestAnimationFrame(() => {
        pending = false;
        setLive("online");
        render();
      });
    }
  });
  es.onerror = () => {
    // Let polling decide whether the API is up; reopen on the next successful poll.
    es.close();
    if (live.stream === es) live.stream = null;
    live.streamFailedAt = Date.now();
    schedulePoll(1000);
  };
}

async function poll() {
  try {
    const r = await fetch(`${API}/devices`, { cache: "no-store", headers: { Accept: "application/json" } });
    if (!r.ok) throw new Error(String(r.status));
    const list = await r.json();
    if (!Array.isArray(list)) throw new Error("bad payload");
    live.devices = new Map();
    list.forEach(applyDevice);
    if (live.status === "online") render();
    setLive("online");
    openStream();
  } catch {
    if (live.stream) {
      live.stream.close();
      live.stream = null;
    }
    setLive("offline");
  }
  schedulePoll();
}

function schedulePoll(ms) {
  clearTimeout(pollTimer);
  const next =
    ms ?? (live.status !== "online" ? POLL_OFFLINE_MS : live.stream ? POLL_WITH_STREAM_MS : POLL_NO_STREAM_MS);
  pollTimer = setTimeout(poll, next);
}

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") schedulePoll(0);
});

// ---------------------------------------------------------------- start

renderLiveBadge();
render();
poll();
