#!/usr/bin/env python3
"""Build the profile README's generated parts.

Writes the banner, the Gaudi chart and the cluster-activity card into assets/,
and refreshes the releases list between the markers in README.md.
Only needs the standard library. Token: GITHUB_TOKEN, or `gh auth token` locally.
"""

import datetime as dt
import json
import os
import random
import re
import subprocess
import urllib.request
from pathlib import Path

LOGIN = "thediymaker"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Node-state colours from the Slurm dashboard.
FULL, PARTIAL, IDLE, DRAINED, MAINT = "#a3212b", "#bd4f16", "#1a7f37", "#3b82f6", "#6e7681"

THEMES = {
    "dark": dict(bg="#0d1117", card="#11161d", border="#262c36", text="#e6edf3",
                 muted="#8b949e", faint="#30363d", empty="#1b2028", empty_stroke="#262c36"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", faint="#d0d7de", empty="#eaeef2", empty_stroke="#d8dee4"),
}


def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()


def graphql(query):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {token()}", "User-Agent": LOGIN},
    )
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]


def fetch():
    return graphql("""{
      user(login: "%s") {
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
        }
        repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
          nodes {
            name stargazerCount
            releases(first: 3, orderBy: {field: CREATED_AT, direction: DESC}) {
              nodes { tagName publishedAt url isDraft isPrerelease }
            }
          }
        }
      }
    }""" % LOGIN)["user"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(n):
    return f"{n:,}"


# --- banner ------------------------------------------------------------------

def tile(x, y, w, h, name, rng, extra=""):
    """One animated node card: colour cycles through states, bars breathe."""
    states = [FULL, PARTIAL, FULL, PARTIAL, IDLE, FULL]
    rng.shuffle(states)
    dur = rng.uniform(9, 16)
    begin = -rng.uniform(0, dur)
    fills = ";".join(states + states[:1])
    out = [f'<g transform="translate({x},{y})">',
           f'<rect width="{w}" height="{h}" rx="6" fill="{states[0]}">'
           f'<animate attributeName="fill" values="{fills}" dur="{dur:.1f}s" begin="{begin:.1f}s" '
           f'calcMode="discrete" repeatCount="indefinite"/></rect>',
           f'<text x="7" y="14" font-family="{FONT}" font-size="9.5" font-weight="700" fill="#fff">{name}</text>']
    for i in range(3):
        by = 22 + i * 7
        vals = [rng.uniform(0.15, 1.0) for _ in range(4)]
        widths = ";".join(f"{v * (w - 14):.1f}" for v in vals + vals[:1])
        out.append(f'<rect x="7" y="{by}" width="{w - 14}" height="2.5" rx="1.2" fill="#fff" opacity=".22"/>')
        out.append(f'<rect x="7" y="{by}" width="{vals[0] * (w - 14):.1f}" height="2.5" rx="1.2" fill="#fff" opacity=".9">'
                   f'<animate attributeName="width" values="{widths}" dur="{rng.uniform(6, 11):.1f}s" '
                   f'begin="{-rng.uniform(0, 6):.1f}s" repeatCount="indefinite"/></rect>')
    out.append(extra)
    out.append("</g>")
    return "".join(out)


def static_tile(x, y, w, h, name, fill, pattern=None, icon=""):
    bars = "".join(f'<rect x="7" y="{22 + i * 7}" width="{w - 14}" height="2.5" rx="1.2" fill="#fff" opacity=".22"/>'
                   for i in range(3))
    stripes = f'<rect width="{w}" height="{h}" rx="6" fill="url(#{pattern})"/>' if pattern else ""
    return (f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="6" fill="{fill}"/>{stripes}'
            f'<text x="7" y="14" font-family="{FONT}" font-size="9.5" font-weight="700" fill="#fff">{name}</text>'
            f'{bars}{icon}</g>')


def interests(t, x, y):
    """Pills under the title, coloured like node states."""
    out = []
    # Text widths are pinned with textLength so padding stays even whatever font the viewer has.
    for label, tw in [("HPC", 28), ("AI", 13), ("3D printing", 70), ("IoT", 20), ("Tinkering", 60)]:
        w = tw + 38
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="5" fill="{t["faint"]}" fill-opacity=".45" '
                   f'stroke="{t["border"]}"/>'
                   f'<rect x="{x + 11}" y="{y + 10.5}" width="7" height="7" rx="1.5" fill="{t["muted"]}"/>'
                   f'<text x="{x + 25}" y="{y + 18.5}" textLength="{tw}" lengthAdjust="spacingAndGlyphs" '
                   f'font-family="{FONT}" font-size="13" font-weight="600" fill="{t["text"]}">{label}</text>')
        x += w + 8
    return "".join(out)


def banner(theme):
    t = THEMES[theme]
    rng = random.Random(7)
    W, H = 1000, 290
    cols, rows, tw, th, gap = 7, 4, 52, 44, 6
    gx = W - 36 - (cols * tw + (cols - 1) * gap)
    gy = 34
    tiles = []
    n = 0
    for r in range(rows):
        for c in range(cols):
            n += 1
            x, y = gx + c * (tw + gap), gy + r * (th + gap)
            name = f"GN{n - 21:02d}" if r == 3 else f"CN{n:03d}"
            if (r, c) == (1, 4):
                tiles.append(static_tile(x, y, tw, th, name, DRAINED, pattern="drain"))
            elif (r, c) == (2, 1):
                wrench = (f'<circle cx="{tw - 9}" cy="10" r="3" fill="none" stroke="#fff" stroke-width="1.4"/>')
                tiles.append(static_tile(x, y, tw, th, name, MAINT, icon=wrench))
            else:
                tiles.append(tile(x, y, tw, th, name, rng))

    footer_y = 266
    chips = [("RUNNING", "since 2019"), ("PENDING", "too many ideas")]
    chip_svg, cx = [], 160
    for label, value in chips:
        chip_svg.append(
            f'<circle cx="{cx}" cy="{footer_y - 4}" r="3" fill="{t["muted"]}"/>'
            f'<text x="{cx + 9}" y="{footer_y}" font-family="{MONO}" font-size="11" fill="{t["muted"]}" '
            f'letter-spacing=".5">{label} <tspan fill="{t["text"]}">{value}</tspan></text>')
        cx += 170

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Johnathan Lee: HPC and AI infrastructure">
<defs>
  <pattern id="drain" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="3.5" height="8" fill="#000" opacity=".22"/>
  </pattern>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>
<text x="40" y="58" font-family="{MONO}" font-size="13" fill="{t["muted"]}" letter-spacing="1">~/thediymaker</text>
<text x="38" y="112" font-family="{FONT}" font-size="46" font-weight="700" fill="{t["text"]}" letter-spacing="-1">Johnathan Lee</text>
<text x="40" y="146" font-family="{FONT}" font-size="18" fill="{t["muted"]}">Sr. HPC System Architect · Arizona State University</text>
{interests(t, 40, 168)}
<line x1="24" y1="{footer_y - 22}" x2="{W - 24}" y2="{footer_y - 22}" stroke="{t["faint"]}"/>
<circle cx="44" cy="{footer_y - 4}" r="4" fill="#2da44e"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="56" y="{footer_y}" font-family="{MONO}" font-size="11" font-weight="700" fill="#2da44e" letter-spacing="1">HEALTHY</text>
{"".join(chip_svg)}
<text x="{W - 36}" y="{footer_y}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["muted"]}">slurmdash.com · obleth.com</text>
{"".join(tiles)}
</svg>
'''


# --- Gaudi chart -------------------------------------------------------------

def gaudi_chart(theme):
    """Static: numbers from gaudi-cookbook's MXFP4 MoE kernel write-up."""
    t = THEMES[theme]
    W, H = 800, 480
    rows = [("GLM-5.3", 23.3, 59.1), ("Kimi-K2.7", 17.9, 44.5)]
    x0, scale = 150, 420 / 60
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-label="MXFP4 MoE decode on Gaudi 2: GLM-5.3 23.3 to 59.1 tokens/s, Kimi-K2.7 17.9 to 44.5 tokens/s">',
           f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>',
           f'<text x="40" y="62" font-family="{MONO}" font-size="14" fill="{t["muted"]}" letter-spacing="1">MXFP4 MoE DECODE · ONE 8-CARD GAUDI 2 NODE</text>',
           f'<text x="38" y="128" font-family="{FONT}" font-size="64" font-weight="700" fill="{t["text"]}" letter-spacing="-2">2.5×</text>',
           f'<text x="40" y="160" font-family="{FONT}" font-size="20" fill="{t["muted"]}">faster single-stream decode</text>']
    for i, (name, before, after) in enumerate(rows):
        y = 210 + i * 115
        out.append(f'<text x="40" y="{y + 38}" font-family="{FONT}" font-size="18" font-weight="600" fill="{t["text"]}">{name}</text>')
        for j, (val, fill, label) in enumerate([(before, t["faint"], "stock op"), (after, PARTIAL, "new kernel")]):
            by = y + j * 40
            w = val * scale
            out.append(f'<rect x="{x0}" y="{by}" width="{w:.1f}" height="30" rx="5" fill="{fill}"/>')
            tx = x0 + w + 12
            out.append(f'<text x="{tx:.1f}" y="{by + 21}" font-family="{MONO}" font-size="15" fill="{t["text"]}">{val} '
                       f'<tspan fill="{t["muted"]}">tok/s · {label}</tspan></text>')
    out.append(f'<text x="40" y="{H - 30}" font-family="{FONT}" font-size="14" fill="{t["muted"]}">vLLM + vllm-gaudi · public images and checkpoints</text>')
    out.append("</svg>\n")
    return "".join(out)


# --- cluster activity --------------------------------------------------------

def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if d["contributionCount"]:
            current += 1
        elif current or d is not days[-1]:  # today may still be empty
            break
    return longest, current


def cluster(theme, user):
    t = THEMES[theme]
    cc = user["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    counts = sorted(d["contributionCount"] for d in days if d["contributionCount"])
    q1 = counts[len(counts) // 3] if counts else 1
    q2 = counts[2 * len(counts) // 3] if counts else 1
    longest, current = streaks(days)
    stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])

    def level(n):
        if not n:
            return t["empty"], "idle"
        return (IDLE, "light") if n < q1 else (PARTIAL, "busy") if n < q2 else (FULL, "full")

    W, pad = 1000, 24
    tile, gap = 15, 3
    pitch = tile + gap
    gx = (W - (len(weeks) * pitch - gap)) / 2

    stats = [("Contributions", fmt(cc["contributionCalendar"]["totalContributions"]), "last 12 months"),
             ("Commits", fmt(cc["totalCommitContributions"]), "public and private"),
             ("Pull requests", fmt(cc["totalPullRequestContributions"]), "opened"),
             ("Longest streak", f"{longest} days", f"current {current}"),
             ("Stars", fmt(stars), "across my projects")]
    out = []
    sw = (W - 2 * pad) / len(stats)
    for i, (label, value, sub) in enumerate(stats):
        x = pad + 16 + i * sw
        if i:
            out.append(f'<line x1="{x - 16}" y1="34" x2="{x - 16}" y2="104" stroke="{t["faint"]}"/>')
        out.append(f'<text x="{x}" y="48" font-family="{FONT}" font-size="13" fill="{t["muted"]}">{label}</text>'
                   f'<text x="{x}" y="80" font-family="{FONT}" font-size="26" font-weight="600" fill="{t["text"]}">{value}</text>'
                   f'<text x="{x}" y="100" font-family="{FONT}" font-size="12" fill="{t["muted"]}">{sub}</text>')

    gy = 160
    month = None
    for wi, w in enumerate(weeks):
        first = dt.date.fromisoformat(w["contributionDays"][0]["date"])
        if first.month != month and first.day <= 7 and wi < len(weeks) - 1:
            month = first.month
            out.append(f'<text x="{gx + wi * pitch:.1f}" y="{gy - 10}" font-family="{FONT}" font-size="11" '
                       f'fill="{t["muted"]}">{first.strftime("%b")}</text>')
        for d in w["contributionDays"]:
            dow = (dt.date.fromisoformat(d["date"]).weekday() + 1) % 7  # Sunday first, like GitHub
            fill, state = level(d["contributionCount"])
            x, y = gx + wi * pitch, gy + dow * pitch
            stroke = f' stroke="{t["empty_stroke"]}"' if state == "idle" else ""
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{tile}" height="{tile}" rx="3" fill="{fill}"{stroke}>'
                       f'<title>{d["date"]}: {d["contributionCount"]}</title></rect>')
    # today: pulsing ring
    tx, ty = gx + (len(weeks) - 1) * pitch, gy + ((dt.date.fromisoformat(days[-1]["date"]).weekday() + 1) % 7) * pitch
    out.append(f'<rect x="{tx - 2:.1f}" y="{ty - 2}" width="{tile + 4}" height="{tile + 4}" rx="4" fill="none" '
               f'stroke="{t["text"]}" stroke-width="1.5"><animate attributeName="opacity" values="1;.2;1" dur="2s" '
               f'repeatCount="indefinite"/></rect>')

    ly = gy + 7 * pitch + 28
    lx = gx
    for fill, label in [(t["empty"], "Idle"), (IDLE, "Light"), (PARTIAL, "Busy"), (FULL, "Full")]:
        stroke = f' stroke="{t["empty_stroke"]}"' if label == "Idle" else ""
        out.append(f'<rect x="{lx:.1f}" y="{ly - 10}" width="11" height="11" rx="2.5" fill="{fill}"{stroke}/>'
                   f'<text x="{lx + 17:.1f}" y="{ly}" font-family="{FONT}" font-size="12" fill="{t["muted"]}">{label}</text>')
        lx += 70
    updated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    out.append(f'<text x="{W - gx:.1f}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="11" '
               f'fill="{t["muted"]}">one tile per day · updated {updated}</text>')

    H = ly + 26
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Contribution activity for the last 12 months, drawn as Slurm node tiles">'
            f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<line x1="{pad}" y1="126" x2="{W - pad}" y2="126" stroke="{t["faint"]}"/>'
            + "".join(out) + "</svg>\n")


# --- README releases ---------------------------------------------------------

def releases_md(user, limit=6):
    rel = []
    for repo in user["repositories"]["nodes"]:
        for r in repo["releases"]["nodes"]:
            if not (r["isDraft"] or r["isPrerelease"]):
                rel.append((r["publishedAt"], repo["name"], r["tagName"], r["url"]))
                break  # newest per repo only
    rel.sort(reverse=True)
    lines = ["| Project | Release | Date |", "|---|---|---|"]
    for published, name, tag, url in rel[:limit]:
        lines.append(f"| [{name}](https://github.com/{LOGIN}/{name}) | [`{tag}`]({url}) | {published[:10]} |")
    return "\n".join(lines)


def update_readme(user):
    path = ROOT / "README.md"
    text = path.read_text()
    new = re.sub(r"(<!-- releases:start -->\n).*?(<!-- releases:end -->)",
                 lambda m: m.group(1) + releases_md(user) + "\n" + m.group(2), text, flags=re.S)
    path.write_text(new)


def main():
    user = fetch()
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        (ASSETS / f"banner-{theme}.svg").write_text(banner(theme))
        (ASSETS / f"gaudi-{theme}.svg").write_text(gaudi_chart(theme))
        (ASSETS / f"cluster-{theme}.svg").write_text(cluster(theme, user))
    update_readme(user)


if __name__ == "__main__":
    main()
