"""Generate every SVG used by the profile README.

    python scripts/build.py            # all assets
    python scripts/build.py stats      # only the GitHub activity card (used by CI)
"""
from __future__ import annotations

import json
import os
import math
import sys
from datetime import datetime
from pathlib import Path

import content as C
from svgkit import (BG, BLUE, CYAN, DIM, INDIGO, INK, L_BRAND_STOPS, L_DIM, L_INK, MAGENTA, MUTED, PANEL,
                    ROOT, SKY, SOFT, VIOLET, arrow_e, arrow_ne, icon, lin_grad, num, panel, rng, svg, text,
                    tw, wrap)

ASSETS = ROOT / "assets"
ACCENT = {"cyan": CYAN, "blue": BLUE, "violet": VIOLET, "magenta": MAGENTA, "sky": SKY, "indigo": INDIGO}


def write(name: str, data: str) -> None:
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")
    print(f"  {name:<34} {len(data.encode()) / 1024:6.1f} KB")


# =================================================================== hero ===
def hero() -> None:
    W, H = 1000, 440
    pdefs, bg, border = panel("h", W, H, r=26, grid=True, glows=[
        (840, 40, 460, VIOLET, 0.30), (90, 470, 420, BLUE, 0.22), (640, 250, 260, CYAN, 0.08)])
    defs = [pdefs,
            lin_grad("brand", user=(56, 0, 420, 0)),
            lin_grad("ink", [(0, "#FFFFFF"), (1, "#BFC6F2")], 0, 0, 0, 1),
            lin_grad("edge", [(0, CYAN), (1, VIOLET)], user=(660, 0, 950, 0))]
    b = [bg]

    # --- status label with a pulsing dot
    b.append(f'<circle class="ring" cx="62" cy="73" r="5" fill="none" stroke="{CYAN}" stroke-width="1.5"/>')
    b.append(f'<circle cx="62" cy="73" r="4" fill="{CYAN}"/>')
    b.append(text(C.HERO_LABEL, 78, 78, 13.5, "#8BE3F5", "jb5", tracking=0.14))

    # --- name
    b.append(text(C.NAME_FIRST, 52, 172, 86, "url(#ink)", "sg7", tracking=-0.02))
    b.append(text(C.NAME_LAST, 52, 258, 86, "url(#brand)", "sg7", tracking=-0.02))

    # --- headline: "Machine learning · Data analytics · Intelligent systems"
    x, y = 56, 306
    for i, part in enumerate(C.HERO_HEADLINE):
        if i:
            b.append(f'<circle cx="{num(x + 9)}" cy="{y - 6}" r="2.6" fill="{CYAN}"/>')
            x += 18
        b.append(text(part, x, y, 20, INK, "sg5"))
        x += tw(part, 20, "sg5")
    for i, line in enumerate(C.HERO_SUB):
        b.append(text(line, 56, 340 + i * 27, 18.5, MUTED, "sg4"))
    end = 56 + tw(C.HERO_SUB[-1], 18.5, "sg4")
    b.append(f'<rect class="cur" x="{num(end + 6)}" y="{340 + 27 - 15}" width="9" height="19" rx="1.5" fill="{CYAN}" fill-opacity="0.85"/>')

    # --- meta row
    x = 56
    for i, m in enumerate(C.HERO_META):
        if i:
            b.append(f'<rect x="{num(x + 10)}" y="401" width="12" height="1.4" fill="{DIM}"/>')
            x += 32
        b.append(text(m, x, 406, 12, DIM, "jb5", tracking=0.16))
        x += tw(m, 12, "jb5", 0.16)

    # --- neural network
    layers_x = [672, 766, 860, 946]
    counts = [4, 6, 5, 2]
    cy = 214
    nodes = [[(lx, cy + (i - (n - 1) / 2) * 50) for i in range(n)] for lx, n in zip(layers_x, counts)]
    edges = []
    for a, bb in zip(nodes, nodes[1:]):
        for p in a:
            for q in bb:
                edges.append(f"M{num(p[0])} {num(p[1])}L{num(q[0])} {num(q[1])}")
    b.append(f'<path d="{"".join(edges)}" stroke="#93A4FF" stroke-opacity="0.13" stroke-width="1"/>')

    r = rng(7)
    routes = [(0, 1, 2, 0), (3, 4, 1, 1), (1, 3, 3, 0), (2, 0, 4, 1), (0, 5, 0, 0), (3, 2, 2, 1)]
    for k, (i, j, m, o) in enumerate(routes):
        pts = [nodes[0][i], nodes[1][j], nodes[2][m], nodes[3][o]]
        d = "M" + "L".join(f"{num(px)} {num(py)}" for px, py in pts)
        delay = k * 1.15 + r.random() * 0.3
        b.append(f'<path class="pulse" d="{d}" pathLength="100" stroke="url(#edge)" stroke-width="5" '
                 f'stroke-opacity="0.22" stroke-linecap="round" style="animation-delay:{delay:.2f}s"/>')
        b.append(f'<path class="pulse" d="{d}" pathLength="100" stroke="url(#edge)" stroke-width="2" '
                 f'stroke-linecap="round" style="animation-delay:{delay:.2f}s"/>')

    for li, layer in enumerate(nodes):
        for ni, (px, py) in enumerate(layer):
            out = li == len(nodes) - 1
            rr = 10 if out else 7.5
            col = VIOLET if li >= 2 else (CYAN if li == 0 else BLUE)
            if out or (li + ni) % 3 == 0:
                b.append(f'<circle class="breathe" cx="{num(px)}" cy="{num(py)}" r="{rr + 7}" fill="{col}" '
                         f'fill-opacity="0.16" style="animation-delay:{(li * 0.7 + ni * 0.45):.2f}s"/>')
            b.append(f'<circle cx="{num(px)}" cy="{num(py)}" r="{rr}" fill="#0B0E22" stroke="{col}" stroke-opacity="0.8" stroke-width="1.5"/>')
            b.append(f'<circle cx="{num(px)}" cy="{num(py)}" r="{2.6 if not out else 3.4}" fill="{col}"/>')
    b.append(text("y = relu(Wx + b)", 946, 406, 12.5, DIM, "jb4", anchor="end"))
    b.append(border)

    style = (".ring{transform-box:fill-box;transform-origin:center;animation:ring 2.8s ease-out infinite}"
             "@keyframes ring{0%{transform:scale(.7);opacity:.9}100%{transform:scale(2.6);opacity:0}}"
             ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
             ".pulse{stroke-dasharray:9 400;stroke-dashoffset:9;animation:flow 7s cubic-bezier(.45,.05,.55,.95) infinite}"
             "@keyframes flow{0%{stroke-dashoffset:9}45%{stroke-dashoffset:-100}100%{stroke-dashoffset:-100}}"
             ".breathe{animation:breathe 4.2s ease-in-out infinite}@keyframes breathe{0%,100%{opacity:.25}50%{opacity:1}}")
    write("hero.svg", svg(W, H, "Mohammed Algoul — Intelligent Systems & Computer Engineering. "
                                 "Machine learning, data analytics and intelligent systems.",
                          "".join(b), "".join(defs), style))


# ======================================================== section headers ===
def sections() -> None:
    W, H = 1000, 72
    for num_, title, tag in C.SECTIONS:
        slug = title.lower().split()[0]
        for theme in ("dark", "light"):
            ink, dim, stops = (INK, DIM, None) if theme == "dark" else (L_INK, L_DIM, L_BRAND_STOPS)
            defs = lin_grad("g", stops or [(0, CYAN), (0.5, BLUE), (1, VIOLET)], user=(0, 0, 1000, 0))
            defs += lin_grad("n", stops or [(0, CYAN), (1, VIOLET)], user=(0, 0, 26, 0))
            tx = 42
            lx1 = tx + tw(title, 30, "sg6") + 24
            lx2 = 998 - tw(tag, 14, "jb4") - 22
            defs += (f'<linearGradient id="f" x1="{num(lx1)}" x2="{num(lx2)}" gradientUnits="userSpaceOnUse">'
                     f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0.12"/></linearGradient>'
                     f'<mask id="m"><rect x="{num(lx1)}" y="30" width="{num(lx2 - lx1)}" height="14" fill="url(#f)"/></mask>')
            body = [text(num_, 2, 46, 17, "url(#n)", "jb5"),
                    text(title, tx, 47, 30, ink, "sg6"),
                    f'<g mask="url(#m)"><rect x="{num(lx1)}" y="36.4" width="{num(lx2 - lx1)}" height="1.6" fill="url(#g)"/></g>',
                    f'<rect x="{num(lx1 - 4)}" y="33.2" width="8" height="8" transform="rotate(45 {num(lx1)} 37.2)" fill="url(#g)"/>',
                    text(tag, 998, 46, 14, dim, "jb4", anchor="end")]
            write(f"sections/{num_}-{slug}-{theme}.svg", svg(W, H, f"{num_} {title}", "".join(body), defs))


# ================================================================== stack ===
def stack() -> None:
    W = 1000
    PAD, LX, CX, CX2 = 44, 44, 300, 956
    CH, GAP, FS, IS = 40, 10, 16, 18
    rows, y = [], 34
    body = []
    for ai, (accent, code, title, items) in enumerate(C.STACK):
        col = ACCENT[accent]
        chips, x, cy = [], CX, 0
        for label, ic in items:
            w = 15 + (IS + 9 if ic else 17) + tw(label, FS, "sg5") + 16
            if x + w > CX2:
                x, cy = CX, cy + CH + GAP
            chips.append((x, cy, w, label, ic))
            x += w + GAP
        row_h = max(cy + CH, 50)
        rows.append((y, row_h, col, code, title, chips))
        y += row_h + 44
    H = int(y - 44 + 34)

    pdefs, bg, border = panel("s", W, H, glows=[(980, 0, 420, VIOLET, 0.16), (0, H, 420, BLUE, 0.14)])
    body.append(bg)
    for i, (ry, rh, col, code, title, chips) in enumerate(rows):
        if i:
            body.append(f'<rect x="{PAD}" y="{num(ry - 22)}" width="{W - 2 * PAD}" height="1" fill="#fff" fill-opacity="0.06"/>')
        ly = ry + (rh - 50) / 2
        body.append(f'<rect x="{LX}" y="{num(ly + 4)}" width="3" height="42" rx="1.5" fill="{col}"/>')
        body.append(text(code, LX + 16, ly + 18, 11.5, col, "jb5", tracking=0.16))
        body.append(text(title, LX + 16, ly + 43, 20, INK, "sg6"))
        for x, cy, w, label, ic in chips:
            yy = ry + cy
            body.append(f'<rect x="{num(x)}" y="{num(yy)}" width="{num(w)}" height="{CH}" rx="{CH / 2}" '
                        f'fill="{col}" fill-opacity="0.07" stroke="{col}" stroke-opacity="0.26"/>')
            tx = x + 15
            if ic:
                body.append(icon(ic, tx, yy + (CH - IS) / 2, IS, col))
                tx += IS + 9
            else:
                body.append(f'<circle cx="{num(tx + 4)}" cy="{num(yy + CH / 2)}" r="4" stroke="{col}" stroke-width="1.4"/>'
                            f'<circle cx="{num(tx + 4)}" cy="{num(yy + CH / 2)}" r="1.4" fill="{col}"/>')
                tx += 17
            body.append(text(label, tx, yy + CH / 2 + 5.6, FS, "#DCE1FA", "sg5"))
    body.append(border)
    write("stack.svg", svg(W, H, "Tech stack — Languages: Python, JavaScript, HTML5, CSS. AI and ML: TensorFlow, Keras, "
                                 "scikit-learn. Data: pandas, NumPy, Matplotlib, Seaborn, Jupyter. Mobile: Flutter, Dart. "
                                 "Tools: FastAPI, web scraping, Google Colab, Kaggle, Git, GitHub, WPLSoft.",
                           "".join(body), pdefs))


# =============================================================== projects ===
def visual(kind: str, col: str, x0: float, y0: float, w: float, h: float) -> tuple[str, str]:
    """Abstract, data-free illustration for a project card. Returns (defs, body)."""
    r = rng(len(kind) * 31)
    out, defs = [], ""
    # faint grid
    for i in range(1, 4):
        gy = y0 + h * i / 4
        out.append(f'<path d="M{num(x0)} {num(gy)}H{num(x0 + w)}" stroke="#fff" stroke-opacity="0.05" stroke-dasharray="2 5"/>')
    if kind == "scan":
        cx, cy = x0 + 70, y0 + h / 2
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="64" ry="52" stroke="{col}" stroke-opacity="0.45" stroke-width="1.5"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="52" ry="41" stroke="{col}" stroke-opacity="0.15"/>')
        for dx, rot in ((-21, 8), (21, -8)):
            out.append(f'<ellipse cx="{cx + dx}" cy="{cy}" rx="16" ry="30" transform="rotate({rot} {cx + dx} {cy})" '
                       f'fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-opacity="0.55" stroke-width="1.2"/>')
        out.append(f'<circle cx="{cx + 25}" cy="{cy - 9}" r="4" fill="{MAGENTA}"/>'
                   f'<circle cx="{cx + 25}" cy="{cy - 9}" r="9" stroke="{MAGENTA}" stroke-opacity="0.6" stroke-dasharray="2 2.5"/>')
        defs = (f'<clipPath id="sc"><ellipse cx="{cx}" cy="{cy}" rx="64" ry="52"/></clipPath>'
                f'<linearGradient id="sl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
                f'<stop offset="1" stop-color="{col}" stop-opacity="0.45"/></linearGradient>')
        out.append(f'<g clip-path="url(#sc)"><g class="scan"><rect x="{cx - 66}" y="{cy - 74}" width="132" height="22" fill="url(#sl)"/>'
                   f'<rect x="{cx - 66}" y="{cy - 52.5}" width="132" height="1.5" fill="{col}"/></g></g>')
        lx = x0 + 160
        for i, lab in enumerate(("NORMAL", "BENIGN", "MALIGNANT")):
            ly = cy - 26 + i * 26
            c = MAGENTA if i == 2 else col
            out.append(f'<rect x="{lx}" y="{ly - 9}" width="10" height="10" rx="2.5" fill="{c}" fill-opacity="{0.9 if i == 2 else 0.35}"/>')
            out.append(text(lab, lx + 18, ly, 11.5, SOFT if i == 2 else MUTED, "jb5", tracking=0.1))
    elif kind == "curve":
        pts = []
        for i in range(12):
            t = i / 11
            pts.append((x0 + 8 + t * (w - 16), y0 + 18 + (h - 36) * (1 - math.exp(-2.6 * t)) * 0.95 + r.uniform(-4, 4)))
        line = "M" + "L".join(f"{num(a)} {num(b_)}" for a, b_ in pts)
        defs = (f'<linearGradient id="ca" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0.35"/>'
                f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>')
        out.append(f'<path d="{line}L{num(pts[-1][0])} {num(y0 + h)}L{num(pts[0][0])} {num(y0 + h)}Z" fill="url(#ca)"/>')
        out.append(f'<path d="{line}" stroke="{col}" stroke-width="2.2" stroke-linejoin="round"/>')
        for i, (a, b_) in enumerate(pts):
            if i % 2 == 0:
                out.append(f'<circle cx="{num(a)}" cy="{num(b_)}" r="3.2" fill="{PANEL}" stroke="{col}" stroke-width="1.6"/>')
        out.append(text("RETENTION", x0 + 10, y0 + 12, 10.5, MUTED, "jb5", tracking=0.12))
    elif kind == "clusters":
        centers = [(x0 + 60, y0 + 40, CYAN), (x0 + 150, y0 + 82, VIOLET), (x0 + 236, y0 + 38, BLUE)]
        for cx, cy, c in centers:
            out.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="30" stroke="{c}" stroke-opacity="0.45" stroke-dasharray="3 4"/>')
            for _ in range(11):
                a, d = r.uniform(0, 6.283), abs(r.gauss(0, 12))
                out.append(f'<circle cx="{num(cx + math.cos(a) * d)}" cy="{num(cy + math.sin(a) * d * 0.85)}" r="2.8" fill="{c}" fill-opacity="0.8"/>')
            out.append(f'<path d="M{num(cx - 5)} {num(cy)}H{num(cx + 5)}M{num(cx)} {num(cy - 5)}V{num(cy + 5)}" stroke="#fff" stroke-width="1.6"/>')
    elif kind == "pca":
        cx, cy, ang = x0 + 118, y0 + h / 2 + 6, math.radians(-18)
        for _ in range(46):
            u, v = r.gauss(0, 46), r.gauss(0, 12)
            px = cx + u * math.cos(ang) - v * math.sin(ang)
            py = cy + u * math.sin(ang) + v * math.cos(ang)
            out.append(f'<circle cx="{num(px)}" cy="{num(py)}" r="2.6" fill="{col}" fill-opacity="0.75"/>')
        for length, a, lab in ((104, ang, "PC1"), (38, ang - math.pi / 2, "PC2")):
            ex, ey = cx + length * math.cos(a), cy + length * math.sin(a)
            ah = 7
            l1 = (ex - ah * math.cos(a - 0.45), ey - ah * math.sin(a - 0.45))
            l2 = (ex - ah * math.cos(a + 0.45), ey - ah * math.sin(a + 0.45))
            out.append(f'<path d="M{num(cx)} {num(cy)}L{num(ex)} {num(ey)}M{num(l1[0])} {num(l1[1])}L{num(ex)} {num(ey)}L{num(l2[0])} {num(l2[1])}" '
                       f'stroke="#fff" stroke-opacity="0.9" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
            out.append(text(lab, ex + 8 * math.cos(a) + (4 if lab == "PC1" else -10), ey + 10 * math.sin(a) + 4, 11, SOFT, "jb5"))
    return defs, "".join(out)


def projects() -> None:
    W, H = 1000, 266
    for idx, p in enumerate(C.PROJECTS, 1):
        col = ACCENT[p["accent"]]
        pdefs, bg, border = panel("p", W, H, glows=[(900, 30, 360, col, 0.20), (40, 260, 300, BLUE, 0.10)],
                                  border_stops=[(0, col), (1, VIOLET if col != VIOLET else BLUE)])
        defs = [pdefs, lin_grad("st", [(0, "#FFFFFF"), (1, col)], user=(620, 0, 760, 0))]
        b = [bg]
        b.append(text(f"{idx:02d}", 44, 58, 12.5, col, "jb5", tracking=0.14))
        b.append(f'<rect x="72" y="52" width="14" height="1.4" fill="{DIM}"/>')
        b.append(text(p["label"].upper(), 96, 58, 12.5, col, "jb5", tracking=0.14))
        b.append(text(p["title"], 42, 102, 33, INK, "sg7", tracking=-0.01))
        for i, line in enumerate(wrap(p["desc"], 17.5, 520)[:3]):
            b.append(text(line, 44, 136 + i * 25, 17.5, MUTED, "sg4"))
        x = 44
        for t in p["tags"]:
            w = tw(t, 12.5, "jb4") + 24
            b.append(f'<rect x="{num(x)}" y="214" width="{num(w)}" height="28" rx="8" fill="#fff" fill-opacity="0.04" stroke="#fff" stroke-opacity="0.10"/>')
            b.append(text(t, x + 12, 232.5, 12.5, SOFT, "jb4"))
            x += w + 8
        vdefs, vbody = visual(p["visual"], col, 620, 40, 280, 124)
        defs.append(vdefs)
        b.append(vbody)
        # stat row
        b.append(f'<rect x="620" y="184" width="336" height="1" fill="#fff" fill-opacity="0.07"/>')
        b.append(text(p["stat"], 618, 238, 40, "url(#st)", "sg7", tracking=-0.02))
        sx = 620 + tw(p["stat"], 40, "sg7", -0.02) + 16
        b.append(text(p["stat_label"], sx, 215, 10.5, col, "jb5", tracking=0.14))
        b.append(text(p["stat_sub"], sx, 236, 14, SOFT, "sg4"))
        # link affordance
        b.append(f'<circle cx="934" cy="52" r="18" fill="#fff" fill-opacity="0.04" stroke="#fff" stroke-opacity="0.14"/>')
        b.append(arrow_ne(934, 52, 11, INK))
        b.append(border)
        style = (".scan{animation:scan 6s ease-in-out infinite}"
                 "@keyframes scan{0%,100%{transform:translateY(0)}50%{transform:translateY(104px)}}")
        alt = f"Project {idx:02d}: {p['title']} — {p['desc']} Stack: {', '.join(p['tags'])}."
        write(f"projects/{idx:02d}-{p['slug']}.svg", svg(W, H, alt, "".join(b), "".join(defs), style))


# ================================================================ connect ===
def connect() -> None:
    W, H = 1000, 196
    pdefs, bg, border = panel("c", W, H, glows=[(860, 100, 340, VIOLET, 0.24), (620, 0, 240, CYAN, 0.10)])
    b = [bg, text(C.CONNECT_TITLE, 46, 88, 32, INK, "sg6", tracking=-0.01)]
    for i, line in enumerate(wrap(C.CONNECT_SUB, 18, 560)):
        b.append(text(line, 48, 124 + i * 26, 18, MUTED, "sg4"))
    # orbit decoration
    cx, cy = 850, 98
    b.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{CYAN}"/><circle cx="{cx}" cy="{cy}" r="22" fill="{CYAN}" fill-opacity="0.12"/>')
    for i, (rad, n, col, dur) in enumerate(((46, 3, BLUE, 38), (74, 5, VIOLET, 60), (102, 7, INDIGO, 90))):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" stroke="#fff" stroke-opacity="0.08"/>')
        dots = "".join(f'<circle cx="{num(cx + rad * math.cos(2 * math.pi * k / n + i))}" '
                       f'cy="{num(cy + rad * math.sin(2 * math.pi * k / n + i))}" r="{3.6 - i * 0.5}" fill="{col}"/>'
                       for k in range(n))
        b.append(f'<g class="orbit" style="animation-duration:{dur}s;animation-direction:{"normal" if i % 2 == 0 else "reverse"}">{dots}</g>')
    b.append(border)
    style = f".orbit{{transform-origin:{cx}px {cy}px;animation:spin 60s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}"
    write("connect.svg", svg(W, H, f"{C.CONNECT_TITLE} {C.CONNECT_SUB}", "".join(b), pdefs, style))

    # buttons
    BW, BH = 300, 64
    for key, label, _url in C.BUTTONS:
        pdefs, bg, border = panel("b", BW, BH, r=32, glows=[(40, 32, 120, BLUE, 0.18)])
        b = [bg, f'<circle cx="34" cy="32" r="20" fill="#fff" fill-opacity="0.06" stroke="#fff" stroke-opacity="0.12"/>']
        if key == "linkedin":
            b.append(f'<rect x="23" y="21" width="22" height="22" rx="5" fill="{BLUE}"/>')
            b.append(text("in", 34, 37.5, 14.5, "#fff", "sg7", anchor="middle"))
        elif key == "github":
            b.append(icon("github", 23, 21, 22, INK))
        else:
            for dx, dy in ((0, 0), (12, 0), (0, 12), (12, 12)):
                b.append(f'<rect x="{23 + dx}" y="{21 + dy}" width="9" height="9" rx="2.2" '
                         f'fill="{[CYAN, BLUE, VIOLET, INDIGO][(dx + dy * 2) // 12 % 4]}"/>')
        b.append(text(label, 68, 38.5, 18.5, INK, "sg5"))
        b.append(arrow_e(258, 32, 16, MUTED))
        b.append(border)
        write(f"buttons/{key}.svg", svg(BW, BH, label, "".join(b), pdefs))


# ================================================================= footer ===
def footer() -> None:
    W, H = 1000, 76
    defs = (lin_grad("g", user=(250, 0, 750, 0)) +
            '<linearGradient id="f" x1="250" x2="750" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<mask id="m"><rect x="250" y="14" width="500" height="10" fill="url(#f)"/></mask>')
    b = ['<g mask="url(#m)"><rect x="250" y="18.4" width="500" height="1.4" fill="url(#g)"/></g>',
         f'<rect x="496" y="15" width="8" height="8" transform="rotate(45 500 19)" fill="url(#g)"/>',
         text("MOHAMMED ALGOUL  ·  GAZA, PALESTINE  ·  GENERATED WITH PYTHON + SVG", 500, 56, 11.5, "#7A82A8", "jb5",
              tracking=0.14, anchor="middle")]
    write("footer.svg", svg(W, H, "Mohammed Algoul — Gaza, Palestine", "".join(b), defs))


# ================================================================== stats ===
def stats() -> None:
    data_path = Path(os.environ.get("STATS_FILE", ROOT / "data" / "stats.json"))
    data = json.loads(data_path.read_text()) if data_path.exists() else None
    W, H = 1000, 452
    pdefs, bg, border = panel("a", W, H, glows=[(960, 0, 420, VIOLET, 0.16), (0, 452, 380, CYAN, 0.10)])
    defs = [pdefs, lin_grad("lb", user=(44, 0, 956, 0))]
    b = [bg]
    synced = data["generated_at"][:10] if data else "pending first sync"
    b.append(text("PUBLIC ACTIVITY  ·  AUTO-UPDATED DAILY", 44, 52, 11.5, DIM, "jb5", tracking=0.16))
    b.append(text(f"SYNCED {synced.upper()}", 956, 52, 11.5, DIM, "jb5", tracking=0.16, anchor="end"))

    kpis = [("PUBLIC PROJECTS", data and data["public_repos"]),
            ("CONTRIBUTIONS · 12 MO", data and data["contributions"]),
            ("ACTIVE DAYS · 12 MO", data and data["active_days"]),
            ("LONGEST STREAK", data and f'{data["longest_streak"]}d')]
    tw_ = (W - 88 - 3 * 14) / 4
    for i, (lab, val) in enumerate(kpis):
        x = 44 + i * (tw_ + 14)
        b.append(f'<rect x="{num(x)}" y="74" width="{num(tw_)}" height="92" rx="14" fill="#fff" fill-opacity="0.035" stroke="#fff" stroke-opacity="0.08"/>')
        b.append(text(str(val) if val is not None else "—", x + 20, 126, 36, INK, "sg7", tracking=-0.02))
        b.append(text(lab, x + 20, 150, 10.5, MUTED, "jb5", tracking=0.12))

    # contribution heatmap
    weeks = data["weeks"] if data else [[None] * 7 for _ in range(53)]
    weeks = weeks[-53:]
    cell, gap = 13.2, 3.6
    gx = (W - (len(weeks) * (cell + gap) - gap)) / 2
    gy = 212
    levels = ["#FFFFFF", "#1E2A78", "#3B4FD8", "#7C5CF6", CYAN]
    mx = max([c for w in weeks for c in w if c] or [1])
    last_month = None
    for wi, week in enumerate(weeks):
        x = gx + wi * (cell + gap)
        if data:
            first = data["week_starts"][-len(weeks):][wi]
            m = datetime.strptime(first, "%Y-%m-%d").strftime("%b").upper()
            if m != last_month and wi < len(weeks) - 2:
                if last_month is not None:
                    b.append(text(m, x, gy - 12, 10, DIM, "jb5", tracking=0.08))
                last_month = m
        for di, c in enumerate(week):
            y = gy + di * (cell + gap)
            if c is None:
                if data:  # day outside the calendar window
                    continue
                b.append(f'<rect x="{num(x)}" y="{num(y)}" width="{cell}" height="{cell}" rx="3" fill="#fff" fill-opacity="0.045"/>')
                continue
            if c == 0:
                b.append(f'<rect x="{num(x)}" y="{num(y)}" width="{cell}" height="{cell}" rx="3" fill="#fff" fill-opacity="0.045"/>')
            else:
                lvl = min(4, 1 + int(3 * (c - 1) / max(mx - 1, 1) + 0.5)) if mx > 1 else 2
                b.append(f'<rect x="{num(x)}" y="{num(y)}" width="{cell}" height="{cell}" rx="3" fill="{levels[lvl]}"/>')
    ly = gy + 7 * (cell + gap) + 14
    # legend, right-aligned to the grid edge: LESS ▢▢▢▢▢ MORE
    right = W - gx
    more_w = tw("MORE", 10, "jb5", 0.08)
    sq_x0 = right - more_w - 8 - 5 * 15 + 4
    b.append(text("MORE", right, ly + 10, 10, DIM, "jb5", tracking=0.08, anchor="end"))
    b.append(text("LESS", sq_x0 - 8, ly + 10, 10, DIM, "jb5", tracking=0.08, anchor="end"))
    for i, c in enumerate(["#FFFFFF"] + levels[1:]):
        op = ' fill-opacity="0.045"' if i == 0 else ""
        b.append(f'<rect x="{num(sq_x0 + i * 15)}" y="{ly}" width="11" height="11" rx="2.5" fill="{c}"{op}/>')
    if not data:
        b.append(f'<rect x="{num(W / 2 - 260)}" y="{gy + 40}" width="520" height="36" rx="18" fill="{PANEL}" stroke="#fff" stroke-opacity="0.1"/>')
        b.append(text("Contribution calendar syncs from the GitHub API daily", W / 2, gy + 63, 12.5, MUTED, "jb4", anchor="middle"))

    # language bar
    by = 382
    b.append(text("PRIMARY LANGUAGE ACROSS PUBLIC PROJECTS", 44, by - 14, 10.5, MUTED, "jb5", tracking=0.12))
    langs = data["languages"] if data else []
    palette = [CYAN, BLUE, VIOLET, MAGENTA, INDIGO, "#5EEAD4"]
    defs.append(f'<clipPath id="bar"><rect x="44" y="{by}" width="912" height="10" rx="5"/></clipPath>')
    b.append(f'<rect x="44" y="{by}" width="912" height="10" rx="5" fill="#fff" fill-opacity="0.06"/>')
    if langs:
        total = sum(v for _, v in langs)
        shown = langs[:5]
        other = total - sum(v for _, v in shown)
        if other > 0:
            shown = shown + [("Other", other)]
        x, segs, lx = 44, [], 44
        for i, (name, v) in enumerate(shown):
            w = 912 * v / total
            segs.append(f'<rect x="{num(x)}" y="{by}" width="{num(w + 0.5)}" height="10" fill="{palette[i]}"/>')
            x += w
            label = f"{name} · {v} {'repo' if v == 1 else 'repos'}"
            b.append(f'<circle cx="{num(lx + 4)}" cy="{by + 30}" r="4" fill="{palette[i]}"/>')
            b.append(text(label, lx + 14, by + 34.5, 12, SOFT, "jb4"))
            lx += 14 + tw(label, 12, "jb4") + 26
        b.append(f'<g clip-path="url(#bar)">{"".join(segs)}</g>')
    b.append(border)
    alt = "GitHub activity — " + (f"{data['public_repos']} public projects, {data['contributions']} contributions "
                                  f"in the last 12 months, {data['active_days']} active days." if data else "syncing.")
    write("stats.svg", svg(W, H, alt, "".join(b), "".join(defs)))


if __name__ == "__main__":
    targets = sys.argv[1:] or ["hero", "sections", "stack", "projects", "connect", "footer", "stats"]
    for t in targets:
        globals()[t]()
