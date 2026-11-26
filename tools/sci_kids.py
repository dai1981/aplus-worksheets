# -*- coding: utf-8 -*-
"""
Simple pictures for the K-2 science units (gen_us_science_gk_*, g1_*, g2_*).
Big, clear shapes that young children can name. Every function returns SVG pieces or a whole inline SVG
(viewBox set, single-quoted attributes, no backslashes).

icon(kind, cx, cy, s=1)   one picture about 80*s px wide, centred at (cx, cy)
card(kind)                one picture in its own small SVG
row(kinds, letters=True)  pictures side by side, labeled A, B, C ... (or with words)
"""
import math
from ws_common import svg_wrap, text, INK
import k_pics

YEL, ORG, SKYB, BLUEW, GRN, DKG, BRN, GRY, WHT, RED, PNK, PUR = (
    "#f6c431", "#e8893a", "#cfe8fb", "#3f8fd2", "#58a85a", "#2f7a3a", "#8a5a2b", "#9aa0a6", "#ffffff", "#d9534f", "#e78fb3", "#8e6bbf")

NAMES = {"sun": "sun", "cloud": "cloud", "rain": "rain", "snow": "snow", "wind": "wind", "storm": "thunderstorm", "rainbow": "rainbow",
         "sprout": "seedling", "plant": "plant in a pot", "tree": "tree", "cactus": "cactus", "seed": "seed", "leaf": "leaf",
         "bee": "bee", "butterfly": "butterfly", "bird": "bird", "frog": "frog", "fish": "fish", "duck": "duck", "bug": "ladybug",
         "flower": "flower", "apple": "apple", "ball": "ball", "cup": "cup",
         "ice": "ice cube", "drop": "drop of water", "puddle": "puddle", "rock": "rock", "block": "wooden block", "spoon": "metal spoon",
         "hot": "hot thermometer", "cold": "cold thermometer", "mountain": "mountain", "house": "house", "umbrella": "umbrella",
         "coat": "coat", "hat": "sun hat", "moon": "moon", "star": "star", "drum": "drum", "bell": "bell", "flashlight": "flashlight",
         "nest": "nest with eggs", "egg": "egg", "worm": "worm", "squirrel": "squirrel", "cat": "cat", "dog": "dog", "bear": "bear",
         "rabbit": "rabbit", "mirror": "mirror", "glass": "glass window", "paper": "paper", "sock": "sock", "crayon": "crayon"}


def P(d, fill, stroke=INK, sw=1.6, extra=""):
    return "<path d='%s' fill='%s' stroke='%s' stroke-width='%s'%s/>" % (d, fill, stroke, sw, extra)


def C(x, y, r, fill, stroke=INK, sw=1.6):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%s'/>" % (x, y, r, fill, stroke, sw)


def E(x, y, rx, ry, fill, stroke=INK, sw=1.6, rot=0):
    t = " transform='rotate(%g %.1f %.1f)'" % (rot, x, y) if rot else ""
    return "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='%s'%s/>" % (x, y, rx, ry, fill, stroke, sw, t)


def L(x1, y1, x2, y2, col=INK, w=2):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s' stroke-linecap='round'/>" % (x1, y1, x2, y2, col, w)


def Rr(x, y, w, h, fill, stroke=INK, sw=1.6, rx=0):
    return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%g' fill='%s' stroke='%s' stroke-width='%s'/>" % (x, y, w, h, rx, fill, stroke, sw)


def _cloud(x, y, k, fill=WHT):
    parts = [(x - 18 * k, y + 4 * k, 13 * k), (x + 16 * k, y + 4 * k, 14 * k), (x, y - 6 * k, 18 * k)]
    s = "".join(C(a, b, r + 1.6, INK, INK, 0) for a, b, r in parts) + Rr(x - 19 * k, y + 2 * k, 36 * k, 17.6 * k, INK, INK, 0)
    s += "".join(C(a, b, r, fill, fill, 0) for a, b, r in parts) + Rr(x - 18 * k, y + 2 * k, 34 * k, 16 * k, fill, fill, 0)
    return s


def _draw(kind, x, y, k):
    if kind in k_pics.NAMES and kind not in ("star",):
        return k_pics.obj(kind, x, y, 34 * k)
    if kind == "sun":
        s = "".join(L(x + 26 * k * math.cos(a), y + 26 * k * math.sin(a), x + 38 * k * math.cos(a), y + 38 * k * math.sin(a), ORG, 3 * k)
                    for a in [i * math.pi / 4 for i in range(8)])
        return s + C(x, y, 20 * k, YEL, ORG, 2)
    if kind == "moon":
        return P("M%.1f %.1f A%.1f %.1f 0 1 0 %.1f %.1f A%.1f %.1f 0 1 1 %.1f %.1f Z" % (x + 8 * k, y - 28 * k, 30 * k, 30 * k, x + 8 * k, y + 28 * k, 22 * k, 22 * k, x + 8 * k, y - 28 * k), "#f3e9a8", "#a08a2a")
    if kind == "star":
        pts = " ".join("%.1f,%.1f" % (x + (30 if i % 2 == 0 else 12) * k * math.cos(-math.pi / 2 + i * math.pi / 5),
                                        y + (30 if i % 2 == 0 else 12) * k * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10))
        return "<polygon points='%s' fill='%s' stroke='#a57c00' stroke-width='1.6'/>" % (pts, YEL)
    if kind == "cloud":
        return _cloud(x, y, k * 1.2)
    if kind == "rain":
        return _cloud(x, y - 12 * k, k, "#dde3ea") + "".join(L(x + dx * k, y + 14 * k, x + (dx - 4) * k, y + 26 * k, BLUEW, 3 * k) for dx in (-16, -4, 8, 20))
    if kind == "snow":
        s = _cloud(x, y - 12 * k, k, "#eef2f6")
        for dx, dy in ((-16, 18), (2, 26), (18, 16)):
            cx, cy = x + dx * k, y + dy * k
            s += "".join(L(cx - 5 * k * math.cos(a), cy - 5 * k * math.sin(a), cx + 5 * k * math.cos(a), cy + 5 * k * math.sin(a), BLUEW, 1.8 * k) for a in (0, 1.05, 2.1))
        return s
    if kind == "storm":
        return _cloud(x, y - 12 * k, k, "#9aa3ad") + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x + 2 * k, y + 6 * k, x - 8 * k, y + 22 * k, x + 2 * k, y + 20 * k, x - 4 * k, y + 36 * k), YEL, "#a57c00")
    if kind == "wind":
        s = ""
        for dy, w in ((-14, 50), (0, 62), (14, 44)):
            s += "<path d='M%.1f %.1f H%.1f q10 0 10 -8 q0 -8 -8 -8' fill='none' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>" % (
                x - 32 * k, y + dy * k, x - 32 * k + w * k, "#6a8caf", 3.2 * k)
        return s
    if kind == "rainbow":
        cols = ["#d9534f", "#e8893a", "#f6c431", "#58a85a", "#3f8fd2", "#8e6bbf"]
        return "".join("<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f' fill='none' stroke='%s' stroke-width='%.1f'/>" % (
            x - (36 - 5 * i) * k, y + 16 * k, (36 - 5 * i) * k, (36 - 5 * i) * k, x + (36 - 5 * i) * k, y + 16 * k, c, 5 * k) for i, c in enumerate(cols))
    if kind == "seed":
        return E(x, y, 16 * k, 24 * k, "#c9a26b", BRN, 1.6, 20) + L(x - 4 * k, y - 12 * k, x + 4 * k, y + 12 * k, BRN, 1.2)
    if kind == "leaf":
        return P("M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x - 26 * k, y + 20 * k, x - 24 * k, y - 26 * k, x + 26 * k, y - 22 * k, x + 22 * k, y + 22 * k, x - 26 * k, y + 20 * k), GRN, DKG) + L(x - 26 * k, y + 20 * k, x + 18 * k, y - 16 * k, DKG, 1.6)
    if kind == "sprout":
        return (Rr(x - 30 * k, y + 18 * k, 60 * k, 10 * k, BRN, BRN, 0) + L(x, y + 18 * k, x, y - 8 * k, DKG, 3 * k)
                + E(x - 12 * k, y - 12 * k, 12 * k, 6 * k, GRN, DKG, 1.4, -30) + E(x + 12 * k, y - 14 * k, 12 * k, 6 * k, GRN, DKG, 1.4, 30))
    if kind == "plant":
        return (P("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 18 * k, y + 8 * k, x + 18 * k, y + 8 * k, x + 13 * k, y + 34 * k, x - 13 * k, y + 34 * k), "#c8693b", "#7a3b1c")
                + L(x, y + 8 * k, x, y - 24 * k, DKG, 3 * k) + E(x - 13 * k, y - 8 * k, 13 * k, 6 * k, GRN, DKG, 1.4, -25)
                + E(x + 13 * k, y - 14 * k, 13 * k, 6 * k, GRN, DKG, 1.4, 25) + E(x - 9 * k, y - 28 * k, 11 * k, 5 * k, GRN, DKG, 1.4, -40))
    if kind == "tree":
        return Rr(x - 6 * k, y + 4 * k, 12 * k, 34 * k, BRN, "#5b3a1a") + C(x, y - 12 * k, 26 * k, GRN, DKG) + C(x - 16 * k, y + 2 * k, 14 * k, GRN, DKG) + C(x + 16 * k, y + 2 * k, 14 * k, GRN, DKG)
    if kind == "cactus":
        return (Rr(x - 9 * k, y - 34 * k, 18 * k, 70 * k, GRN, DKG, 1.6, 9 * k) + Rr(x - 28 * k, y - 14 * k, 12 * k, 26 * k, GRN, DKG, 1.6, 6 * k)
                + Rr(x - 20 * k, y + 4 * k, 14 * k, 8 * k, GRN, GRN, 0) + Rr(x + 16 * k, y - 22 * k, 12 * k, 24 * k, GRN, DKG, 1.6, 6 * k)
                + Rr(x + 6 * k, y - 4 * k, 14 * k, 8 * k, GRN, GRN, 0))
    if kind == "bee":
        return (E(x - 4 * k, y - 16 * k, 10 * k, 7 * k, "#e8f4fb", GRY, 1.2, -20) + E(x + 8 * k, y - 16 * k, 10 * k, 7 * k, "#e8f4fb", GRY, 1.2, 20)
                + E(x, y, 22 * k, 14 * k, YEL, INK) + Rr(x - 8 * k, y - 13 * k, 5 * k, 26 * k, INK, INK, 0) + Rr(x + 4 * k, y - 13 * k, 5 * k, 26 * k, INK, INK, 0)
                + C(x + 22 * k, y - 2 * k, 7 * k, INK, INK))
    if kind == "butterfly":
        return (E(x - 16 * k, y - 10 * k, 16 * k, 14 * k, ORG, INK, 1.4, -20) + E(x + 16 * k, y - 10 * k, 16 * k, 14 * k, ORG, INK, 1.4, 20)
                + E(x - 12 * k, y + 12 * k, 11 * k, 9 * k, YEL, INK, 1.4, 20) + E(x + 12 * k, y + 12 * k, 11 * k, 9 * k, YEL, INK, 1.4, -20)
                + E(x, y, 3.5 * k, 22 * k, INK, INK) + L(x, y - 20 * k, x - 7 * k, y - 32 * k, INK, 1.4) + L(x, y - 20 * k, x + 7 * k, y - 32 * k, INK, 1.4))
    if kind == "bird":
        return (E(x, y, 24 * k, 16 * k, "#5b9bd5", "#2e5f8a") + C(x + 20 * k, y - 12 * k, 11 * k, "#5b9bd5", "#2e5f8a")
                + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x + 29 * k, y - 14 * k, x + 40 * k, y - 10 * k, x + 29 * k, y - 7 * k), ORG, ORG, 1)
                + C(x + 23 * k, y - 14 * k, 2 * k, INK, INK) + P("M%.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x - 12 * k, y - 2 * k, x - 4 * k, y - 22 * k, x + 8 * k, y - 4 * k), "#3d7ab8", "#2e5f8a", 1.2)
                + L(x - 4 * k, y + 15 * k, x - 6 * k, y + 26 * k, ORG, 2 * k) + L(x + 6 * k, y + 15 * k, x + 6 * k, y + 26 * k, ORG, 2 * k))
    if kind == "frog":
        return (E(x, y + 8 * k, 28 * k, 18 * k, GRN, DKG) + C(x - 13 * k, y - 10 * k, 9 * k, GRN, DKG) + C(x + 13 * k, y - 10 * k, 9 * k, GRN, DKG)
                + C(x - 13 * k, y - 11 * k, 4 * k, WHT, INK, 1) + C(x + 13 * k, y - 11 * k, 4 * k, WHT, INK, 1) + C(x - 13 * k, y - 11 * k, 2 * k, INK, INK, 0)
                + C(x + 13 * k, y - 11 * k, 2 * k, INK, INK, 0) + "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (x - 10 * k, y + 6 * k, x, y + 12 * k, x + 10 * k, y + 6 * k, DKG))
    if kind == "worm":
        return "<path d='M%.1f %.1f q10 -14 20 0 t20 0 t20 0' fill='none' stroke='#d98c8c' stroke-width='%.1f' stroke-linecap='round'/>" % (x - 30 * k, y, 9 * k) + C(x + 30 * k, y, 2 * k, INK, INK, 0)
    if kind in ("cat", "dog", "bear", "rabbit", "squirrel"):
        col = {"cat": "#f0a35e", "dog": "#c98f56", "bear": "#7a5232", "rabbit": "#d9d4cc", "squirrel": "#b06a32"}[kind]
        s = E(x, y + 12 * k, 22 * k, 18 * k, col)
        if kind == "squirrel":
            s = P("M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x - 14 * k, y + 26 * k, x - 44 * k, y + 10 * k, x - 30 * k, y - 22 * k, x - 20 * k, y, x - 10 * k, y + 14 * k), col) + s
        head = C(x, y - 14 * k, 15 * k, col)
        ears = ""
        if kind == "cat":
            ears = P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 13 * k, y - 20 * k, x - 12 * k, y - 36 * k, x - 3 * k, y - 27 * k), col) + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x + 13 * k, y - 20 * k, x + 12 * k, y - 36 * k, x + 3 * k, y - 27 * k), col)
        elif kind == "dog":
            ears = E(x - 15 * k, y - 10 * k, 6 * k, 12 * k, "#8a5a2b", INK, 1.4, 20) + E(x + 15 * k, y - 10 * k, 6 * k, 12 * k, "#8a5a2b", INK, 1.4, -20)
        elif kind == "bear":
            ears = C(x - 12 * k, y - 27 * k, 6 * k, col) + C(x + 12 * k, y - 27 * k, 6 * k, col)
        elif kind == "rabbit":
            ears = E(x - 7 * k, y - 36 * k, 5 * k, 15 * k, col) + E(x + 7 * k, y - 36 * k, 5 * k, 15 * k, col)
        elif kind == "squirrel":
            ears = C(x - 9 * k, y - 27 * k, 4 * k, col) + C(x + 9 * k, y - 27 * k, 4 * k, col)
        face = C(x - 5 * k, y - 16 * k, 2 * k, INK, INK, 0) + C(x + 5 * k, y - 16 * k, 2 * k, INK, INK, 0) + C(x, y - 10 * k, 2.4 * k, INK, INK, 0)
        return s + ears + head + face
    if kind == "nest":
        return (E(x - 8 * k, y - 4 * k, 9 * k, 11 * k, "#cfe3f3", GRY) + E(x + 8 * k, y - 4 * k, 9 * k, 11 * k, "#cfe3f3", GRY)
                + P("M%.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x - 32 * k, y + 2 * k, x, y + 34 * k, x + 32 * k, y + 2 * k), "#b98a52", "#6b4423"))
    if kind == "egg":
        return E(x, y, 18 * k, 24 * k, "#f6efe0", GRY)
    if kind == "ice":
        return P("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 22 * k, y - 10 * k, x + 8 * k, y - 22 * k, x + 24 * k, y + 6 * k, x - 6 * k, y + 20 * k), "#dff1fb", "#6aa7cf") + L(x - 10 * k, y - 6 * k, x + 4 * k, y - 12 * k, WHT, 3 * k)
    if kind == "drop":
        return P("M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z" % (x, y - 32 * k, x + 24 * k, y - 4 * k, x + 22 * k, y + 26 * k, x, y + 26 * k,
                                                                                    x - 22 * k, y + 26 * k, x - 24 * k, y - 4 * k, x, y - 32 * k), "#8cc3ec", "#3f8fd2")
    if kind == "puddle":
        return E(x, y + 10 * k, 36 * k, 12 * k, "#8cc3ec", "#3f8fd2")
    if kind == "rock":
        return P("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 30 * k, y + 18 * k, x - 20 * k, y - 10 * k, x + 4 * k, y - 18 * k, x + 28 * k, y - 2 * k, x + 32 * k, y + 18 * k), "#a9a39a", "#5f5a52")
    if kind == "block":
        return Rr(x - 22 * k, y - 22 * k, 44 * k, 44 * k, "#e2b77a", "#8a5a2b") + L(x - 14 * k, y - 8 * k, x + 14 * k, y - 8 * k, "#b98a52", 1.4) + L(x - 14 * k, y + 8 * k, x + 14 * k, y + 8 * k, "#b98a52", 1.4)
    if kind == "spoon":
        return E(x - 14 * k, y - 14 * k, 11 * k, 16 * k, "#d7dbe0", "#6b7280", 1.6, 45) + L(x - 6 * k, y - 6 * k, x + 26 * k, y + 26 * k, "#9aa0a6", 6 * k)
    if kind == "hot" or kind == "cold":
        lvl = 30 if kind == "hot" else 6
        col = RED if kind == "hot" else BLUEW
        return (Rr(x - 6 * k, y - 34 * k, 12 * k, 58 * k, WHT, INK, 1.6, 6 * k) + C(x, y + 28 * k, 10 * k, col, INK)
                + Rr(x - 3 * k, y + 22 * k - lvl * k * 1.6, 6 * k, lvl * k * 1.6, col, col, 0))
    if kind == "mountain":
        return P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 38 * k, y + 26 * k, x, y - 30 * k, x + 38 * k, y + 26 * k), "#9a8f80", "#5f5a52") + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 12 * k, y - 12 * k, x, y - 30 * k, x + 12 * k, y - 12 * k), WHT, "#5f5a52", 1.2)
    if kind == "house":
        return Rr(x - 26 * k, y - 6 * k, 52 * k, 36 * k, "#f4e3c1", BRN) + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x - 32 * k, y - 4 * k, x, y - 32 * k, x + 32 * k, y - 4 * k), "#c0504d", "#7a2f2d") + Rr(x - 6 * k, y + 10 * k, 12 * k, 20 * k, BRN, BRN)
    if kind == "umbrella":
        return P("M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z" % (x - 34 * k, y - 4 * k, 34 * k, 28 * k, x + 34 * k, y - 4 * k), "#d9534f", "#8e2a27") + L(x, y - 4 * k, x, y + 28 * k, INK, 2.4) + "<path d='M%.1f %.1f q0 6 -6 6 q-6 0 -6 -6' fill='none' stroke='%s' stroke-width='2.4'/>" % (x, y + 28 * k, INK)
    if kind == "coat":
        pts = [(-10, -30), (-30, -22), (-38, 10), (-27, 13), (-22, -2), (-22, 32), (22, 32), (22, -2), (27, 13), (38, 10), (30, -22), (10, -30), (0, -18)]
        return ("<polygon points='%s' fill='#3f6fb5' stroke='#1f3f73' stroke-width='1.6'/>" % " ".join("%.1f,%.1f" % (x + a * k, y + b * k) for a, b in pts)
                + L(x, y - 18 * k, x, y + 32 * k, "#1f3f73", 1.6) + "".join(C(x + 4 * k, y + d * k, 2 * k, WHT, WHT, 0) for d in (-6, 6, 18)))
    if kind == "hat":
        return E(x, y + 10 * k, 38 * k, 9 * k, "#e8c872", "#9b7a1d") + P("M%.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x - 18 * k, y + 8 * k, x, y - 30 * k, x + 18 * k, y + 8 * k), "#e8c872", "#9b7a1d") + Rr(x - 17 * k, y - 2 * k, 34 * k, 6 * k, RED, RED, 0)
    if kind == "drum":
        return Rr(x - 26 * k, y - 12 * k, 52 * k, 34 * k, RED, "#8e2a27") + E(x, y - 12 * k, 26 * k, 8 * k, "#f6efe0", INK) + L(x + 20 * k, y - 34 * k, x + 6 * k, y - 16 * k, BRN, 3 * k) + C(x + 21 * k, y - 35 * k, 4 * k, "#e2b77a", BRN)
    if kind == "bell":
        return P("M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x - 26 * k, y + 18 * k, x - 20 * k, y - 32 * k, x, y - 30 * k, x + 20 * k, y - 32 * k, x + 26 * k, y + 18 * k), YEL, "#a57c00") + C(x, y + 22 * k, 6 * k, "#a57c00", "#a57c00")
    if kind == "flashlight":
        return (Rr(x - 34 * k, y - 8 * k, 40 * k, 16 * k, "#5a6270", INK, 1.6, 3) + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x + 6 * k, y - 8 * k, x + 18 * k, y - 14 * k, x + 18 * k, y + 14 * k, x + 6 * k, y + 8 * k), "#7a8290")
                + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x + 18 * k, y - 14 * k, x + 40 * k, y - 26 * k, x + 40 * k, y + 26 * k, x + 18 * k, y + 14 * k), "#fdf0a6", "none", 0))
    if kind == "mirror":
        return E(x, y - 6 * k, 22 * k, 28 * k, "#e4f1f8", "#8a5a2b", 3) + L(x - 8 * k, y - 18 * k, x + 2 * k, y - 26 * k, WHT, 3) + L(x, y + 22 * k, x, y + 34 * k, "#8a5a2b", 4 * k)
    if kind == "glass":
        return Rr(x - 26 * k, y - 26 * k, 52 * k, 52 * k, "#e9f5fb", "#6aa7cf", 3) + L(x - 14 * k, y + 6 * k, x + 6 * k, y - 14 * k, WHT, 3) + L(x, y - 26 * k, x, y + 26 * k, "#6aa7cf", 2) + L(x - 26 * k, y, x + 26 * k, y, "#6aa7cf", 2)
    if kind == "paper":
        return Rr(x - 20 * k, y - 26 * k, 40 * k, 52 * k, WHT, GRY) + "".join(L(x - 12 * k, y + d * k, x + 12 * k, y + d * k, "#b9c4cf", 1.4) for d in (-14, -6, 2, 10))
    if kind == "sock":
        return P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Z" % (x - 6 * k, y - 32 * k, x + 12 * k, y - 32 * k, x + 12 * k, y + 8 * k, x + 34 * k, y + 14 * k, x + 22 * k, y + 28 * k, x - 6 * k, y + 22 * k), PUR, "#5a3f80")
    if kind == "crayon":
        return Rr(x - 30 * k, y - 7 * k, 46 * k, 14 * k, "#3f8fd2", "#1f5f99", 1.6, 2) + P("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x + 16 * k, y - 7 * k, x + 32 * k, y, x + 16 * k, y + 7 * k), "#f2d6a2", "#1f5f99")
    raise ValueError(kind)


def icon(kind, cx, cy, s=1.0):
    return _draw(kind, cx, cy, s)


def name(kind):
    return NAMES.get(kind, kind)


def card(kind, size=110, label=None):
    return svg_wrap(size, size, icon(kind, size / 2, size / 2, size / 110.0), label or "a picture of a %s" % name(kind))


def row(kinds, letters=True, words=None, size=100, label=None):
    """Pictures side by side; letters A-D below each (or words)."""
    s = ""
    lab = words or (["ABCDEFGH"[i] for i in range(len(kinds))] if letters else None)
    h = size + (30 if lab else 0)
    cw = max(size, max(len(w) for w in words) * 7.4 + 12) if words else size
    for i, k in enumerate(kinds):
        x = cw / 2 + i * cw
        s += icon(k, x, size / 2, size / 115.0)
        if lab:
            s += text(x, size + 20, lab[i], 16 if letters and not words else 13)
    return svg_wrap(cw * len(kinds), h, s, label or "pictures: " + ", ".join(name(k) for k in kinds))


def scene(items, w=360, h=180, sky=True, ground=True, label="a picture"):
    """items: [(kind, x, y, s)] on a sky and ground background."""
    s = ""
    if sky:
        s += "<rect x='0' y='0' width='%d' height='%d' fill='#e6f3fc'/>" % (w, h)
    if ground:
        s += "<rect x='0' y='%d' width='%d' height='%d' fill='#cfe7b8'/>" % (h - 40, w, 40)
    for k, x, y, sc in items:
        s += icon(k, x, y, sc)
    return svg_wrap(w, h, s, label)
