"""Generate brand/tokens.css from brand/tokens.json (the single source).

    uv run python brand/build_tokens.py

Pages link brand/tokens.css; fonts are self-hosted from brand/fonts/ (no Google requests).
"""

import json
from pathlib import Path

HERE = Path(__file__).parent
FONT_URL = "fonts/"  # relative to tokens.css


def main() -> None:
    t = json.loads((HERE / "tokens.json").read_text(encoding="utf-8"))
    themes = [th["id"] for th in t["color"]["themes"]]
    first = themes[0]

    def per_theme(tokens, theme):
        out = []
        for tok in tokens:
            v = tok["value"]
            v = v if isinstance(v, str) else v.get(theme, v[first])
            out.append(f"  --{tok['name']}: {v};")
        return out

    color, shadow = t["color"]["tokens"], t.get("shadow", {}).get("tokens", [])
    lines = [f"/* {t['name']} — generated from tokens.json by build_tokens.py; do not edit */", ""]
    for f in t["type"]["fonts"]:
        lines += [
            "@font-face {",
            f'  font-family: "{f["family"]}";',
            f'  src: url("{FONT_URL}{Path(f["file"]).name}") format("woff2");',
            f"  font-weight: {f['weight']};",
            "  font-display: swap;",
            "}",
        ]
    lines += ["", ":root {"]
    lines += per_theme(color, first) + per_theme(shadow, first)
    for fam in ("spacing", "radius"):
        lines += [f"  --{x['name']}: {x['value']};" for x in t[fam]["tokens"]]
    lines += [f"  --font-{k}: {v};" for k, v in t["type"]["families"].items()]
    first_scheme = "dark" if first == "dark" else "light"
    other = [th for th in themes if th != first][0]
    lines += [f"  color-scheme: {first_scheme};", "}", ""]
    other_scheme = "light" if first_scheme == "dark" else "dark"
    other_vars = per_theme(color, other) + per_theme(shadow, other) + [f"  color-scheme: {other_scheme};"]
    lines += [f"@media (prefers-color-scheme: {other_scheme}) {{", f'  :root:not([data-theme="{first}"]) {{']
    lines += ["  " + x for x in other_vars] + ["  }", "}", "", f':root[data-theme="{other}"] {{']
    lines += other_vars + ["}", ""]
    for g in t["type"]["groups"]:
        for s in g["styles"]:
            fam = s.get("family", g["family"])
            lines += [f".t-{s['name']} {{", f"  font-family: var(--font-{fam});",
                      f"  font-size: {s['fontSize']};", f"  line-height: {s['lineHeight']};",
                      f"  font-weight: {s['fontWeight']};"]
            if "letterSpacing" in s:
                lines.append(f"  letter-spacing: {s['letterSpacing']};")
            if fam == "mono":
                lines.append("  font-variant-numeric: tabular-nums;")
            lines.append("}")
    (HERE / "tokens.css").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote", HERE / "tokens.css")


if __name__ == "__main__":
    main()
