#!/usr/bin/env python3
"""Generate the dark-dashboard SVG panels for the GitHub profile README.

Produces (relative to repo root):
  assets/header.svg      – editor-style banner: greeting, roles code-line, tech-stack pills
  assets/skills.svg      – "What I Can Do" skills & services card grid
  assets/stats.svg       – GitHub Stats + Most Used Languages panels
  assets/activity.svg    – Activity Contribution Graph (waveform)
  assets/summary.svg     – Profile Summary trophies + Language Pie Chart + Project Status
  assets/snake/github-contribution-grid-snake.svg        – static contribution grid + snake
  assets/snake/github-contribution-grid-snake-dark.svg   – same (dark palette)

Run:  python3 assets/scripts/generate_profile_svgs.py
"""
import math
import os
import random

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

W = 860

# ---- palette (GitHub-dark inspired) ---------------------------------------
BG          = "#0d1117"
PANEL       = "#0e1524"
PANEL_EDGE  = "#1c2740"
BAR         = "#0b101c"
CARD        = "#101a2c"
CARD_EDGE   = "#22304c"
PILL        = "#131c2e"
PILL_EDGE   = "#24304a"
TEXT        = "#e8edf4"
MUTED       = "#8b949e"
DIM         = "#6e7681"
BLUE        = "#58a6ff"
PURPLE      = "#bc8cff"
GREEN       = "#3fb950"
YELLOW      = "#e3b341"
PINK        = "#f778ba"
RED         = "#ff7b72"
STR_GREEN   = "#7ee787"

SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'Cascadia Code','JetBrains Mono',Consolas,monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=12, fill=TEXT, weight=400, mono=False, anchor="start",
        spacing=None):
    fam = MONO if mono else SANS
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{ls}>'
            f'{esc(s)}</text>')


def rect(x, y, w, h, fill, stroke=None, rx=10, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}"{st}/>')


def panel(w, h):
    """Full-width rounded panel with border."""
    return rect(0.5, 0.5, w - 1, h - 1, PANEL, PANEL_EDGE, rx=12)


def header_svg() -> str:
    H = 252
    tech = [
        ("React", "#61dafb"), ("TypeScript", "#3178c6"), ("Node.js", "#43a047"),
        ("Python", "#4584b6"), ("AWS", "#ff9900"), ("Docker", "#2496ed"),
        ("Tailwind CSS", "#38bdf8"), ("PostgreSQL", "#4169e1"),
        ("GraphQL", "#e10098"), ("Firebase", "#ffb300"),
        ("GitHub Actions", "#2088ff"),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">']
    out.append(f'<defs><clipPath id="c"><rect x="0.5" y="0.5" width="{W-1}" '
               f'height="{H-1}" rx="12"/></clipPath></defs>')
    out.append(panel(W, H))
    out.append(f'<g clip-path="url(#c)">')
    out.append(rect(0, 0, W, 36, BAR, rx=0))
    out.append(f'<line x1="0" y1="36.5" x2="{W}" y2="36.5" stroke="{PANEL_EDGE}"/>')
    out.append('</g>')
    out.append(txt(18, 23, "MRK92-Dev / README.md", 12, MUTED, mono=True))
    out.append(txt(W - 18, 23, "✎", 13, MUTED, anchor="end"))
    # greeting
    out.append(txt(20, 86, "👋 Hi, I'm Muhammad Arshad Khan", 21, TEXT, 700))
    # roles code line (syntax highlighted)
    code = (f'<text x="20" y="118" font-family="{MONO}" font-size="12.5" '
            f'xml:space="preserve">'
            f'<tspan fill="{PURPLE}">const </tspan>'
            f'<tspan fill="#79c0ff">roles</tspan>'
            f'<tspan fill="{TEXT}"> = [</tspan>'
            f"<tspan fill=\"{STR_GREEN}\">'Fullstack Developer'</tspan>"
            f'<tspan fill="{DIM}">, </tspan>'
            f"<tspan fill=\"{STR_GREEN}\">'Node.js Expert'</tspan>"
            f'<tspan fill="{DIM}">, </tspan>'
            f"<tspan fill=\"{STR_GREEN}\">'Cloud Enthusiast'</tspan>"
            f'<tspan fill="{DIM}">, </tspan>'
            f"<tspan fill=\"{STR_GREEN}\">'Open Source Contributor'</tspan>"
            f'<tspan fill="{TEXT}">];</tspan></text>')
    out.append(code)
    out.append(txt(20, 152, "Tech stack", 12.5, TEXT, 600))
    # pills, two rows
    rows = [tech[:7], tech[7:]]
    y = 166
    for row in rows:
        x = 18.0
        for label, color in row:
            w = 36 + 6.15 * len(label)
            out.append(rect(x, y, w, 26, PILL, PILL_EDGE, rx=13))
            out.append(f'<circle cx="{x+13}" cy="{y+13}" r="4" fill="{color}"/>')
            out.append(txt(x + 24, y + 17, label, 11, TEXT, 500))
            x += w + 10
        y += 34
    out.append('</svg>')
    return "\n".join(out)


def skills_svg() -> str:
    H = 436
    cards = [
        ("🛡️", "Cyber Security", "Pen-testing · Network hardening",
         "OWASP top-10 · CTF playbooks"),
        ("🐍", "Python Coding", "Automation · Scripting · APIs",
         "Scraping · Data pipelines · Bots"),
        ("🤖", "AI Agents", "LLM agents · Tool-calling workflows",
         "Prompt engineering · RAG pipelines"),
        ("📡", "ESP32 Projects", "IoT firmware · Wi-Fi / BLE",
         "Sensors · Live dashboards"),
        ("🔌", "Arduino Uno", "Embedded C/C++ · Robotics",
         "Circuits · Motors · Prototyping"),
        ("🌐", "Full-Stack Web", "React · Node.js · REST / GraphQL",
         "PostgreSQL · Firebase · Tailwind"),
        ("☁️", "Cloud & DevOps", "AWS · Docker · Linux",
         "CI/CD with GitHub Actions"),
        ("📊", "Data & ML", "Pandas · NumPy · Visualization",
         "Model serving · Quick ML demos"),
        ("🤝", "Open Source", "Clean PRs · Code reviews",
         "Docs people actually read"),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">']
    out.append(panel(W, H))
    out.append(txt(20, 34, "⚡ What I Can Do", 15, TEXT, 700))
    out.append(txt(W - 20, 34, "// skills & services", 11, DIM, mono=True,
                   anchor="end"))
    cw, ch, gx, gy = 265, 110, 14.5, 14
    xs = [18, 18 + cw + gx, 18 + 2 * (cw + gx)]
    ys = [52, 52 + ch + gy, 52 + 2 * (ch + gy)]
    for i, (icon, title, l1, l2) in enumerate(cards):
        x, y = xs[i % 3], ys[i // 3]
        out.append(rect(x, y, cw, ch, CARD, CARD_EDGE, rx=10))
        out.append(txt(x + 16, y + 37, icon, 19))
        out.append(txt(x + 46, y + 35, title, 13, TEXT, 700))
        out.append(txt(x + 16, y + 64, l1, 10.5, MUTED))
        out.append(txt(x + 16, y + 81, l2, 10.5, MUTED))
    out.append('</svg>')
    return "\n".join(out)


def stats_svg() -> str:
    H = 214
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">']
    # ---- left: GitHub Stats
    out.append(rect(0.5, 8.5, 413, 197, PANEL, PANEL_EDGE, rx=12))
    out.append(txt(20, 38, "📊 GitHub Stats", 13, TEXT, 700))
    # rows: label at y, value at y+24
    layout = [
        (20, 64, "Grade", "B+", GREEN, 20),
        (20, 122, "Commits", "3,412", TEXT, 16),
        (220, 64, "Stars", "112", TEXT, 16),
        (220, 122, "PRs", "86", TEXT, 16),
        (220, 168, "Contribs", "2.4k", TEXT, 16),
    ]
    for x, y, label, value, vcol, vsize in layout:
        out.append(txt(x, y, label, 10.5, MUTED))
        out.append(txt(x, y + 24, value, vsize, vcol, 700))
    # ---- right: Most Used Languages
    out.append(rect(428.5, 8.5, 431, 197, PANEL, PANEL_EDGE, rx=12))
    # mini bar icon before title
    out.append(f'<rect x="448" y="26" width="4" height="12" rx="1" fill="{BLUE}"/>')
    out.append(f'<rect x="454" y="30" width="4" height="8" rx="1" fill="{PURPLE}"/>')
    out.append(f'<rect x="460" y="23" width="4" height="15" rx="1" fill="{YELLOW}"/>')
    out.append(txt(472, 38, "Most Used Languages", 13, TEXT, 700))
    segs = [(35.2, BLUE), (28.1, PURPLE), (18.7, YELLOW), (8.3, PINK),
            (9.7, "#263042")]
    bx, by, bw, bh = 448, 58, 391, 10
    out.append(f'<defs><clipPath id="barclip"><rect x="{bx}" y="{by}" '
               f'width="{bw}" height="{bh}" rx="5"/></clipPath></defs>')
    out.append(f'<g clip-path="url(#barclip)">')
    x = bx
    for pct, color in segs:
        wseg = bw * pct / 100.0
        out.append(f'<rect x="{x:.1f}" y="{by}" width="{wseg:.1f}" height="{bh}" '
                   f'fill="{color}"/>')
        x += wseg
    out.append('</g>')
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5" '
               f'fill="none" stroke="{PANEL_EDGE}"/>')
    legend = [
        (448, 100, "Python", "35.2%", BLUE),
        (650, 100, "JavaScript", "18.7%", YELLOW),
        (448, 130, "TypeScript", "28.1%", PURPLE),
        (650, 130, "CSS", "8.3%", PINK),
        (448, 160, "Other", "9.7%", "#263042"),
    ]
    for x, y, name, pct, color in legend:
        out.append(f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{color}"/>')
        out.append(txt(x + 14, y, name, 11, TEXT))
        out.append(txt(x + 150, y, pct, 11, MUTED, anchor="end"))
    out.append('</svg>')
    return "\n".join(out)


def activity_svg() -> str:
    H = 208
    rnd = random.Random(42)
    cx0, cx1, mid = 20, 840, 122
    tops, bots = [], []
    n = (cx1 - cx0) // 5
    for i in range(n + 1):
        x = cx0 + i * 5
        t = i
        a = abs(math.sin(t * 0.32) * 0.45 + math.sin(t * 0.11 + 1.7) * 0.30 +
                (rnd.random() - 0.5) * 0.55)
        a = min(1.0, a)
        tops.append((x, mid - 10 - a * 56))
        bots.append((x, mid + 8 + a * 50))
    poly = "M " + " L ".join(f"{x},{y:.1f}" for x, y in tops)
    poly += " L " + " L ".join(f"{x},{y:.1f}" for x, y in reversed(bots)) + " Z"
    line = "M " + " L ".join(f"{x},{y:.1f}" for x, y in tops)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">']
    out.append('<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
               f'<stop offset="0" stop-color="{BLUE}"/>'
               f'<stop offset="1" stop-color="{PURPLE}"/></linearGradient>'
               f'<linearGradient id="g2" x1="0" y1="0" x2="1" y2="0">'
               f'<stop offset="0" stop-color="{BLUE}" stop-opacity="0.55"/>'
               f'<stop offset="1" stop-color="{PURPLE}" stop-opacity="0.55"/>'
               '</linearGradient></defs>')
    out.append(panel(W, H))
    out.append(txt(20, 32, "📈 Activity Analyzer — Contribution Graph", 13, TEXT, 700))
    out.append(f'<circle cx="{W-150}" cy="28" r="4" fill="{BLUE}"/>')
    out.append(txt(W - 140, 32, "contributions", 10.5, MUTED))
    out.append(f'<circle cx="{W-60}" cy="28" r="4" fill="{PURPLE}"/>')
    out.append(txt(W - 50, 32, "2.4k", 10.5, MUTED))
    out.append(f'<path d="{poly}" fill="url(#g2)"/>')
    out.append(f'<path d="{line}" fill="none" stroke="url(#g)" '
               f'stroke-width="1.6"/>')
    out.append('</svg>')
    return "\n".join(out)


def arc_path(cx, cy, r0, r1, a0, a1):
    large = 1 if (a1 - a0) > math.pi else 0
    p = []
    p.append(f"M {cx + r1*math.cos(a0):.1f} {cy + r1*math.sin(a0):.1f}")
    p.append(f"A {r1} {r1} 0 {large} 1 {cx + r1*math.cos(a1):.1f} "
             f"{cy + r1*math.sin(a1):.1f}")
    p.append(f"L {cx + r0*math.cos(a1):.1f} {cy + r0*math.sin(a1):.1f}")
    p.append(f"A {r0} {r0} 0 {large} 0 {cx + r0*math.cos(a0):.1f} "
             f"{cy + r0*math.sin(a0):.1f}")
    p.append("Z")
    return " ".join(p)


def summary_svg() -> str:
    H = 236
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">']
    # ---- A: profile summary trophies
    out.append(rect(0.5, 8.5, 440, 219, PANEL, PANEL_EDGE, rx=12))
    out.append(txt(20, 38, "🏆 Profile Summary", 13, TEXT, 700))
    row1 = ["Stars", "Commits", "Followers", "Issues", "PRs", "Repos", "Languages"]
    row2 = ["Security", "AI Agents", "IoT", "Arduino", "Python", "Cloud", "OSS"]
    for r, labels, ey, ly in [(0, row1, 78, 100), (1, row2, 140, 162)]:
        for i, lab in enumerate(labels):
            cx = 16 + i * 61 + 30
            out.append(txt(cx, ey, "🏆", 16, anchor="middle"))
            out.append(txt(cx, ly, lab, 7.5, MUTED, anchor="middle"))
    # ---- B: language pie chart
    out.append(rect(454.5, 8.5, 240, 219, PANEL, PANEL_EDGE, rx=12))
    out.append(txt(470, 38, "🧿 Language Pie Chart", 12.5, TEXT, 700))
    segs = [(35.2, BLUE), (28.1, PURPLE), (18.7, YELLOW), (8.3, PINK),
            (9.7, "#263042")]
    a = -math.pi / 2
    cx, cy = 522, 132
    for pct, color in segs:
        a1 = a + 2 * math.pi * pct / 100.0
        out.append(f'<path d="{arc_path(cx, cy, 26, 46, a, a1 - 0.02)}" '
                   f'fill="{color}"/>')
        a = a1
    legend = [("Python", BLUE), ("TypeScript", PURPLE), ("JavaScript", YELLOW),
              ("CSS", PINK), ("Other", "#263042")]
    y = 96
    for name, color in legend:
        out.append(f'<circle cx="584" cy="{y-3}" r="4" fill="{color}"/>')
        out.append(txt(594, y, name, 10, TEXT))
        y += 21
    # ---- C: project status
    out.append(rect(708.5, 8.5, 151, 219, PANEL, PANEL_EDGE, rx=12))
    out.append(txt(724, 38, "🚀 Project Status", 12, TEXT, 700))
    lx, ly = 784, 110
    for j, (dy, col) in enumerate([(34, "#1f4fbf"), (17, "#2f6feb"),
                                   (0, "#58a6ff")]):
        y = ly + dy
        out.append(f'<path d="M {lx} {y} L {lx+38} {y+13} L {lx} {y+26} '
                   f'L {lx-38} {y+13} Z" fill="{col}" opacity="{1 - j*0.12}"/>')
    out.append(f'<circle cx="{lx}" cy="{ly+72}" r="3.5" fill="{GREEN}"/>')
    out.append(txt(lx, ly + 92, "all systems building", 9, MUTED, anchor="middle"))
    out.append('</svg>')
    return "\n".join(out)


def snake_svg() -> str:
    H = 246
    rnd = random.Random(7)
    levels = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    weights = [0.16, 0.20, 0.28, 0.22, 0.14]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">']
    out.append(panel(W, H))
    out.append(txt(20, 30, "GitHub contribution grid", 11, MUTED))
    out.append(txt(W - 20, 30, "MRK92-Dev", 11, MUTED, 600, mono=True,
                   anchor="end"))
    cell, gap = 16, 3.5
    cols, rows = 42, 7
    x0 = (W - (cols * (cell + gap) - gap)) / 2
    y0 = 52
    for r in range(rows):
        for c in range(cols):
            lv = rnd.choices(range(5), weights=weights)[0]
            out.append(f'<rect x="{x0 + c*(cell+gap):.1f}" '
                       f'y="{y0 + r*(cell+gap):.1f}" width="{cell}" '
                       f'height="{cell}" rx="3" fill="{levels[lv]}"/>')
    out.append(txt(W / 2, y0 + 3.5 * (cell + gap) + 12, "🐍", 26, anchor="middle"))
    out.append('</svg>')
    return "\n".join(out)


def main():
    files = {
        "designs/dashboard/assets/header.svg": header_svg(),
        "designs/dashboard/assets/skills.svg": skills_svg(),
        "designs/dashboard/assets/stats.svg": stats_svg(),
        "designs/dashboard/assets/activity.svg": activity_svg(),
        "designs/dashboard/assets/summary.svg": summary_svg(),
        "assets/snake/github-contribution-grid-snake.svg": snake_svg(),
        "assets/snake/github-contribution-grid-snake-dark.svg": snake_svg(),
    }
    for rel, content in files.items():
        path = os.path.join(REPO, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(content + "\n")
        print("wrote", rel)


if __name__ == "__main__":
    main()
