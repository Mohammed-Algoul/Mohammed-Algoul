"""Tiny SVG toolkit used to generate every visual in this profile.

Why text-to-path?  Images inside a GitHub README are rendered through <img>,
which cannot load web fonts reliably (and GitHub's raw-content CSP blocks
font loading).  So every string is shaped with HarfBuzz (proper kerning) and
converted to vector outlines with fontTools.  The result looks identical on
every OS, browser and in the GitHub mobile app.
"""
from __future__ import annotations

import io
from html import escape
import json
import random
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"

# ---------------------------------------------------------------- palette ---
BG = "#07080F"
PANEL = "#0A0C18"
INK = "#EEF0FF"
SOFT = "#C9CEEA"
MUTED = "#9AA2C6"
DIM = "#646C92"
CYAN = "#22D3EE"
BLUE = "#4F7DFF"
VIOLET = "#9B6BFF"
MAGENTA = "#E879F9"
SKY = "#38BDF8"
INDIGO = "#818CF8"
BRAND_STOPS = [(0, CYAN), (0.5, BLUE), (1, VIOLET)]

# light-theme counterparts (only used for transparent section headers)
L_INK = "#0B1020"
L_DIM = "#5A6386"
L_BRAND_STOPS = [(0, "#0891B2"), (0.5, "#2563EB"), (1, "#7C3AED")]


def num(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Font:
    def __init__(self, filename: str):
        tt = TTFont(FONTS / filename)
        tt.flavor = None  # woff2 -> plain sfnt for HarfBuzz
        buf = io.BytesIO()
        tt.save(buf)
        data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(data))
        self._cache: dict[str, list] = {}

    def shape(self, text: str):
        if text not in self._cache:
            buf = hb.Buffer()
            buf.add_str(text)
            buf.guess_segment_properties()
            hb.shape(self.hb, buf, {"kern": True, "liga": True})
            out = []
            for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
                if info.codepoint == 0:
                    raise ValueError(f"missing glyph in {text!r}")
                out.append((info.codepoint, pos.x_advance, pos.x_offset, pos.y_offset))
            self._cache[text] = out
        return self._cache[text]

    def width(self, text: str, size: float, tracking: float = 0) -> float:
        g = self.shape(text)
        return sum(a for _, a, _, _ in g) * size / self.upem + tracking * size * max(len(g) - 1, 0)

    def glyph_d(self, gid: int) -> str:
        """Outline of one glyph in a 1000-unit em, y pointing down."""
        k = 1000 / self.upem
        pen = SVGPathPen(self.glyphs, ntos=num)
        self.glyphs[self.order[gid]].draw(TransformPen(pen, (k, 0, 0, -k, 0, 0)))
        return pen.getCommands()

    def layout(self, text: str, size: float, tracking: float = 0):
        """Yield (gid, x_offset_in_em1000, y_offset_in_em1000)."""
        k = 1000 / self.upem
        cx = 0.0
        for gid, adv, xo, yo in self.shape(text):
            yield gid, cx + xo * k, -yo * k
            cx += adv * k + tracking * 1000


# glyph outlines referenced by the SVG currently being built
GLYPH_DEFS: dict[str, str] = {}


_fonts: dict[str, Font] = {}


def font(key: str) -> Font:
    files = {
        "sg4": "space-grotesk-latin-400-normal.woff2",
        "sg5": "space-grotesk-latin-500-normal.woff2",
        "sg6": "space-grotesk-latin-600-normal.woff2",
        "sg7": "space-grotesk-latin-700-normal.woff2",
        "jb4": "jetbrains-mono-latin-400-normal.woff2",
        "jb5": "jetbrains-mono-latin-500-normal.woff2",
    }
    if key not in _fonts:
        _fonts[key] = Font(files[key])
    return _fonts[key]


def text(s: str, x: float, y: float, size: float, fill: str, f: str = "sg4", tracking: float = 0,
         anchor: str = "start", opacity: float | None = None) -> str:
    fo = font(f)
    w = fo.width(s, size, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    uses = []
    for gid, gx, gy in fo.layout(s, size, tracking):
        key = f"{f}_{gid}"
        if key not in GLYPH_DEFS:
            d = fo.glyph_d(gid)
            if not d:
                continue  # whitespace
            GLYPH_DEFS[key] = d
        elif not GLYPH_DEFS[key]:
            continue
        ys = f' y="{num(gy)}"' if abs(gy) > 0.05 else ""
        uses.append(f'<use href="#{key}" x="{num(gx)}"{ys}/>')
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return (f'<g transform="translate({num(x)} {num(y)}) scale({size / 1000:.5f})" fill="{fill}"{op}>'
            + "".join(uses) + "</g>")


def tw(s: str, size: float, f: str = "sg4", tracking: float = 0) -> float:
    return font(f).width(s, size, tracking)


def wrap(s: str, size: float, maxw: float, f: str = "sg4") -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and tw(trial, size, f) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- pieces ----
ICONS = json.loads((ROOT / "scripts" / "icons.json").read_text())


def icon(name: str, x: float, y: float, size: float, fill: str, opacity: float | None = None) -> str:
    s = size / 24
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return f'<path transform="translate({num(x)} {num(y)}) scale({s:.4f})" d="{ICONS[name]}" fill="{fill}"{op}/>'


def lin_grad(gid: str, stops=BRAND_STOPS, x1=0, y1=0, x2=1, y2=0, user: tuple | None = None) -> str:
    units = ""
    if user:
        x1, y1, x2, y2 = user
        units = ' gradientUnits="userSpaceOnUse"'
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{units}>{st}</linearGradient>'


def glow(gid: str, color: str, opacity: float) -> str:
    return (f'<radialGradient id="{gid}"><stop offset="0" stop-color="{color}" stop-opacity="{opacity}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def arrow_ne(cx: float, cy: float, size: float, color: str, width: float = 1.8) -> str:
    h = size / 2
    return (f'<path d="M{num(cx-h)} {num(cy+h)}L{num(cx+h)} {num(cy-h)}M{num(cx-h*0.35)} {num(cy-h)}H{num(cx+h)}V{num(cy+h*0.35)}" '
            f'stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow_e(x: float, cy: float, size: float, color: str, width: float = 1.8) -> str:
    h = size / 2
    return (f'<path d="M{num(x)} {num(cy)}H{num(x+size)}M{num(x+size-h*0.8)} {num(cy-h*0.8)}L{num(x+size)} {num(cy)}L{num(x+size-h*0.8)} {num(cy+h*0.8)}" '
            f'stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}.pulse{opacity:0}}"


def svg(w: int, h: int, title: str, body: str, defs: str = "", style: str = "") -> str:
    title = escape(title)
    st = f"<style>{style}{REDUCED_MOTION}</style>" if style else ""
    glyphs = "".join(f'<path id="{k}" d="{d}"/>' for k, d in GLYPH_DEFS.items() if d)
    GLYPH_DEFS.clear()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'fill="none" role="img" aria-label="{title}"><title>{title}</title>{st}<defs>{glyphs}{defs}</defs>{body}</svg>\n')


def panel(gid: str, w: int, h: int, r: int = 22, glows: list[tuple] = (), grid: bool = False,
          border_stops=BRAND_STOPS) -> tuple[str, str, str]:
    """Return (defs, background, overlay) for a dark rounded panel.

    glows: list of (cx, cy, r, color, opacity)
    """
    defs = [f'<clipPath id="{gid}c"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>',
            lin_grad(f"{gid}b", border_stops, user=(0, 0, w, h))]
    bg = [f'<rect width="{w}" height="{h}" rx="{r}" fill="{PANEL}"/>', f'<g clip-path="url(#{gid}c)">']
    for i, (cx, cy, rr, col, op) in enumerate(glows):
        defs.append(glow(f"{gid}g{i}", col, op))
        bg.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="url(#{gid}g{i})"/>')
    if grid:
        defs.append(f'<pattern id="{gid}p" width="22" height="22" patternUnits="userSpaceOnUse">'
                    f'<circle cx="1" cy="1" r="1" fill="#fff" fill-opacity="0.07"/></pattern>')
        defs.append(f'<radialGradient id="{gid}m"><stop offset="0" stop-color="#fff"/>'
                    f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
        defs.append(f'<mask id="{gid}mk"><rect width="{w}" height="{h}" fill="url(#{gid}m)"/></mask>')
        bg.append(f'<rect width="{w}" height="{h}" fill="url(#{gid}p)" mask="url(#{gid}mk)"/>')
    bg.append("</g>")
    overlay = (f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="{r-0.75}" '
               f'stroke="url(#{gid}b)" stroke-opacity="0.38" stroke-width="1.5"/>')
    return "".join(defs), "".join(bg), overlay


def rng(seed: int) -> random.Random:
    return random.Random(seed)
