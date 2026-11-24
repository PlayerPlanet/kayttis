// Inline SVG icons. Each device type has an "on" and an "off" variant: the on variant is
// filled and emits something (light rays, water, a spark); the off variant is an outline.
// Icons use currentColor so the toggle button decides the colour.

const svg = (body) =>
  `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;

const BULB = "M12 5.2a5 5 0 0 0-3 9c.5.4.8 1 .8 1.6v.4h4.4v-.4c0-.6.3-1.2.8-1.6a5 5 0 0 0-3-9z";
const BULB_BASE = '<path d="M10 18.6h4M10.6 21h2.8"/>';

const FAUCET =
  '<path d="M3.5 7.5v6"/><path d="M3.5 10.5h9a3.5 3.5 0 0 1 3.5 3.5v1" stroke-width="2.6"/><path d="M8.5 10.5V7M6 7h5"/>';

const PLUG_PRONGS = '<path d="M9.5 3v4M14.5 3v4"/>';
const PLUG_BODY = "M7 7h10v3a5 5 0 0 1-10 0z";

export const ICONS = {
  lamp: {
    on: svg(
      `<path d="${BULB}" fill="currentColor"/>${BULB_BASE}` +
        '<path d="M12 1.6v1.2M4.6 4.4l.9.9M19.4 4.4l-.9.9M2.6 10.2h1.3M20.1 10.2h1.3"/>',
    ),
    off: svg(`<path d="${BULB}"/>${BULB_BASE}`),
  },
  faucet: {
    on: svg(
      FAUCET +
        '<path d="M16 17.2c-.9 1.3-1.4 2.1-1.4 2.8a1.4 1.4 0 0 0 2.8 0c0-.7-.5-1.5-1.4-2.8z" fill="currentColor"/>' +
        '<path d="M19.6 16.6v1.4M12.4 16.6v1.4"/>',
    ),
    off: svg(FAUCET),
  },
  electric: {
    on: svg(
      `${PLUG_PRONGS}<path d="${PLUG_BODY}" fill="currentColor"/><path d="M12 15v6"/>` +
        '<path d="M3.2 9.5h1.6M19.2 9.5h1.6M4.3 4.8l1.1 1.1M19.7 4.8l-1.1 1.1"/>',
    ),
    off: svg(`${PLUG_PRONGS}<path d="${PLUG_BODY}"/><path d="M12 15v6"/>`),
  },
};

export const TYPE_LABELS = {
  lamp: "Valaisin",
  faucet: "Hana",
  electric: "Muu sähkölaite",
};

export const CHEVRON = svg('<path d="M6 9l6 6 6-6" stroke-width="2.2"/>');
export const CAMERA = svg(
  '<path d="M4 7.5h3l1.6-2h6.8l1.6 2h3v11H4z"/><circle cx="12" cy="13" r="3.2"/>',
);
