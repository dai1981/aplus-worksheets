# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Volume with Fractional Edge Lengths (6.G.A.2)
  python tools/gen_us_math_g6_volume.py
Answers are in simplest form (mixed numbers when more than 1). Every answer is computed with
fractions.Fraction (or decimal.Decimal), never typed by hand.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 6 style: numbers 1,000 and above are written with commas; units are in³, ft², and so on.

Pictures (checked in code):
  packed boxes   every small cube is drawn (back to front), so the hidden cubes really are there;
                 the drawn cubes equal (edge ÷ small edge) along each edge
  plain prisms   oblique view, 3 hidden edges dashed, edge labels outside the box (fractions stacked)
  base prisms    a 'glass' box with its base shaded, B and h labeled
"""
import json, math, os, random, re
from decimal import Decimal as D
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
FILL2, TOP2, SIDE2 = "#f6dcb4", "#fbecd3", "#e8c48f"       # the one highlighted small cube
BASE = "#4fae74"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
UNITS = ["in", "ft", "cm", "m"]
DZX, DZY = 0.55, 0.40          # one unit of depth goes this far right and up (oblique view)


# ------------------------------------------------------------ numbers
def f(n):
    return "{:,}".format(n)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return f(q)
    if q == 0:
        return fr(r, v.denominator)
    return "%s %s" % (f(q), fr(r, v.denominator))


def raw(v):
    v = F(v)
    return f(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


# an edge is (w, n, d): whole part w and fraction part n/d. 3 = (3, 0, 1); 1/2 = (0, 1, 2)
def val(t):
    return F(t[0]) + F(t[1], t[2])


def fx(t):
    return show(val(t))


def tb(t):
    """(top, bottom) used when multiplying: a whole number is n/1, 2 1/2 is 5/2."""
    return (t[0], 1) if t[1] == 0 else (t[0] * t[2] + t[1], t[2])


def imp(t):
    a, b = tb(t)
    return f(a) if b == 1 else fr(a, b)


def T(v):
    """Fraction -> edge tuple."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    return (q, r, v.denominator) if r else (q, 0, 1)


def dz(x):
    """Decimal without trailing zeros, with commas: 20500 -> 20,500; 12.50 -> 12.5."""
    s = format(x, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, p = s.partition(".")
    return "{:,}".format(int(i)) + ("." + p if p else "")


def cub(u):
    return u + "³"


def sqr(u):
    return u + "²"


def q3(v, u):
    """A volume: '3 3/4 in³'."""
    return "%s %s" % (show(v), cub(u))


def word_unit(v, one, many):
    return one if v <= 1 else many


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """correct and cands are (html, key). A distractor whose key equals the answer or an earlier
    distractor is skipped, so no two choices are worth the same. Positions are set by balance()."""
    ch, keys = [correct[0]], [correct[1]]
    for h, k in cands:
        if not h or h in ch or k in keys:
            continue
        num = k[1] if isinstance(k, tuple) else k
        if num is not None and num <= 0:
            continue
        ch.append(h)
        keys.append(k)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3 - t.count(".") * 0.5) * fs * 0.6


# ------------------------------------------------------------ drawing
class Canvas:
    """Collects shapes and labels, tracks the bounding box, then writes a tight SVG."""
    def __init__(self):
        self.el, self.boxes = [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN, op=None):
        self.el.append(("p", pts, fill, sw, col, op))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def _t(self, x, y, t, fs, anchor="middle", col=INK, weight="700"):
        self.el.append(("t", x, y, t, fs, anchor, col, weight))

    def label(self, x, y, parts, anchor="middle", col=INK):
        """parts: list of ('w', text) whole/plain text, ('f', n, d) stacked fraction, ('u', text) unit.
        (x, y) is the middle of the label. Labels never touch each other."""
        FW, FF, FU, gap = 17, 15, 16, 3
        ws = []
        for p in parts:
            if p[0] == "w":
                ws.append(tw(p[1], FW))
            elif p[0] == "f":
                ws.append(max(tw(p[1], FF), tw(p[2], FF)) + 5)
            else:
                ws.append(tw(p[1], FU) * 0.95)
        total = sum(ws) + gap * (len(ws) - 1)
        hh = 18 if any(p[0] == "f" for p in parts) else 9
        x0 = x - total / 2 if anchor == "middle" else (x if anchor == "start" else x - total)
        box = (x0, y - hh, x0 + total, y + hh)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (parts, box, b)
        self.boxes.append(box)
        self.grow(*box)
        cx = x0
        for p, wd in zip(parts, ws):
            if p[0] == "w":
                self._t(cx + wd / 2, y + 6, p[1], FW, col=col)
            elif p[0] == "f":
                m = cx + wd / 2
                self._t(m, y - 4, p[1], FF, col=col)
                self.el.append(("l", (cx + 1, y + 0.5), (cx + wd - 1, y + 0.5), False, 1.6, col))
                self._t(m, y + 16, p[2], FF, col=col)
            else:
                self._t(cx, y + 6, p[1], FU, "start", col, "400")
            cx += wd + gap
        return box

    def svg(self, label, pad=5):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1                                  # keep these pictures out of the 'square' print size
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3],
                            " fill-opacity='%g'" % e[5] if e[5] else ""))
            elif e[0] == "l":
                a, b = e[1], e[2]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, e[5], e[4],
                            " stroke-dasharray='5 4'" if e[3] else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col, wt = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, wt, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def parts_of(v, u=None):
    """Label parts for a length: 2 1/2 in -> [('w','2'), ('f',1,2), ('u','in')]."""
    if v is None:
        p = [("w", "?")]
    else:
        v = F(v)
        q, r = divmod(v.numerator, v.denominator)
        p = []
        if q or not r:
            p.append(("w", f(q)))
        if r:
            p.append(("f", r, v.denominator))
    if u:
        p.append(("u", u))
    return p


def proj(X, Y, Z, k):
    """x to the right, y up, z (depth) to the back."""
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def visible_cubes(l, w, h):
    """Cubes that show at least one face: front, top or right side."""
    return l * w * h - (l - 1) * (w - 1) * (h - 1)


def packed_svg(a, b, c, e=None, u="", label="box packed with small cubes", hi=False, px=None):
    """a cubes long, b cubes deep, c cubes tall; each small cube has edge e (a Fraction) in unit u.
    hi = color the front top right cube. Edge labels show a·e, b·e, c·e."""
    cubes = [(x, y, z) for x in range(a) for y in range(c) for z in range(b)]
    keys = set(cubes)
    assert len(keys) == a * b * c
    if px is None:
        px = min(150.0 / (a + b * DZX), 105.0 / (c + b * DZY), 26)
    cv = Canvas()
    for x, y, z in sorted(cubes, key=lambda q: (-q[2], q[1], q[0])):
        p = lambda i, j, m: proj(x + i, y + j, z + m, px)
        on = hi and (x, y, z) == (a - 1, c - 1, 0)
        fr_, tp, sd = (FILL2, TOP2, SIDE2) if on else (FILL, TOP, SIDE)
        if (x, y, z - 1) not in keys:
            cv.poly([p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)], fr_)
        if (x, y + 1, z) not in keys:
            cv.poly([p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)], tp)
        if (x + 1, y, z) not in keys:
            cv.poly([p(1, 0, 0), p(1, 0, 1), p(1, 1, 1), p(1, 1, 0)], sd)
    P = lambda i, j, m: proj(i, j, m, px)
    for q1, q2 in [((0, 0, 0), (a, 0, 0)), ((a, 0, 0), (a, 0, b)), ((a, 0, b), (a, c, b)), ((0, c, b), (a, c, b)),
                   ((0, c, 0), (0, c, b)), ((0, 0, 0), (0, c, 0)), ((0, c, 0), (a, c, 0)), ((a, 0, 0), (a, c, 0)),
                   ((a, c, 0), (a, c, b))]:
        cv.line(P(*q1), P(*q2), sw=2.4)                     # outline of the whole box
    if e is not None:
        x, y = P(a / 2, 0, 0)
        cv.label(x, y + 22, parts_of(a * e, u))
        x, y = P(0, c / 2, 0)
        cv.label(x - 8, y, parts_of(c * e, u), "end")
        x, y = P(a, 0, b / 2)
        cv.label(x + 8, y + 14, parts_of(b * e, u), "start")
    return cv.svg(label)


def disp(L, W, H):
    """Draw very different sizes a little closer together so the box stays readable."""
    L, W, H = float(L), float(W), float(H)
    m = max(L, W, H)
    return tuple(max(v, m / 3.0) for v in (L, W, H))


def box_faces(cv, L, W, H, k, op=None):
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(L, 0, 0), p(L, H, 0), p(0, H, 0)], FILL, 2.4, op=op)
    cv.poly([p(0, H, 0), p(L, H, 0), p(L, H, W), p(0, H, W)], TOP, 2.4, op=op)
    cv.poly([p(L, 0, 0), p(L, 0, W), p(L, H, W), p(L, H, 0)], SIDE, 2.4, op=op)
    return p


def prism_svg(L, W, H, u, miss=None, label="rectangular prism"):
    """Box with fractional edge labels. miss = 'l', 'w' or 'h' is shown as a red '?'."""
    dL, dW, dH = disp(L, W, H)
    k = min(150 / (dL + dW * DZX), 95 / (dH + dW * DZY))
    cv = Canvas()
    p = box_faces(cv, dL, dW, dH, k)
    for a, b in [((0, 0, dW), (dL, 0, dW)), ((0, 0, dW), (0, dH, dW)), ((0, 0, dW), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True, sw=1.6)
    lab = lambda key, v: (parts_of(None, u), RED) if miss == key else (parts_of(v, u), INK)
    x, y = p(dL / 2, 0, 0)
    t, c = lab("l", L)
    cv.label(x, y + 22, t, col=c)
    x, y = p(0, dH / 2, 0)
    t, c = lab("h", H)
    cv.label(x - 8, y, t, "end", c)
    x, y = p(dL, 0, dW / 2)
    t, c = lab("w", W)
    cv.label(x + 8, y + 14, t, "start", c)
    return cv.svg(label)


def base_svg(B, H, u, shape=(3.0, 2.0), label="rectangular prism with its base shaded"):
    """A see-through box with its base shaded. Labels: 'B = …' below the box, h on the left."""
    dL, dW = shape
    dH = max(float(H) / 2.2 * 1.0, 1.2) if H else 2.0
    dH = min(dH, 3.2)
    k = min(150 / (dL + dW * DZX), 90 / (dH + dW * DZY))
    cv = Canvas()
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(dL, 0, 0), p(dL, 0, dW), p(0, 0, dW)], BASE, 0.1, op=0.8)   # the base, seen through the box
    box_faces(cv, dL, dW, dH, k, op=0.4)
    for a, b in [((0, 0, dW), (dL, 0, dW)), ((0, 0, dW), (0, dH, dW)), ((0, 0, dW), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True, sw=1.6)
    x, y = p(0, dH / 2, 0)
    cv.label(x - 8, y, [("w", "h =")] + parts_of(H, u), "end")
    x, y = p(dL / 2 + dW * 0.5 * DZX / 1.0 * 0, 0, 0)
    cv.label(x, y + 24, [("w", "B =")] + parts_of(B, sqr(u)))
    return cv.svg(label)


# ------------------------------------------------------------ explanations
def prod_e(ts, u, pre="V = l × w × h = "):
    """V = 2 1/2 × 1 1/3 × 3 = 5/2 × 4/3 × 3 = 60/6 = 10 in³."""
    v = F(1)
    for t in ts:
        v *= val(t)
    s = pre + " × ".join(fx(t) for t in ts)
    if any(t[0] and t[1] for t in ts):
        s += " = " + " × ".join(imp(t) for t in ts)
    num = den = 1
    for t in ts:
        a, b = tb(t)
        num, den = num * a, den * b
    if den > 1:
        s += " = " + fr(num, den)
        if (num, den) != (v.numerator, v.denominator) or v > 1:
            s += " = " + show(v)
    else:
        s += " = " + f(num)
    return s + " %s." % cub(u)


def div_e(V, B, u):
    """h = V ÷ B with the steps."""
    h = V / B
    s = "%s ÷ %s = %s × %s" % (show(V), show(B), raw(V), raw(1 / B))
    num, den = V.numerator * B.denominator, V.denominator * B.numerator
    s += " = %s" % (fr(num, den) if den > 1 else f(num))
    if (num, den) != (h.numerator, h.denominator):
        s += " = %s" % show(h)
    return s + " %s" % u


# ------------------------------------------------------------ typical wrong answers for l × w × h
def wrongs(ts, u, order):
    """(html, key) pairs from real mistakes, in the order given."""
    vs = [val(t) for t in ts]
    V = vs[0] * vs[1] * vs[2]
    out = []
    for kd in order:
        v, sq = None, False
        if kd == "add":                                         # added the edges
            v = sum(vs)
        elif kd == "two":                                       # multiplied only two edges
            v = vs[0] * vs[1]
        elif kd == "two2":
            v = vs[1] * vs[2]
        elif kd == "parts":                                     # whole parts and fraction parts separately
            if all(t[0] for t in ts) and any(t[1] for t in ts):
                fp = [F(t[1], t[2]) for t in ts if t[1]]
                v = F(ts[0][0] * ts[1][0] * ts[2][0]) + (fp[0] if len(fp) == 1 else math.prod(fp))
        elif kd == "whole":                                     # dropped the fraction parts
            if all(t[0] for t in ts) and any(t[1] for t in ts):
                v = F(ts[0][0] * ts[1][0] * ts[2][0])
        elif kd == "badimp":                                    # 2 1/2 -> 3/2
            if any(t[0] and t[1] for t in ts):
                v = math.prod(F(t[0] + t[1], t[2]) if t[0] and t[1] else val(t) for t in ts)
        elif kd == "sq":                                        # right number, square units
            v, sq = V, True
        elif kd == "x3":                                        # cube: 3 × edge
            v = 3 * vs[0]
        elif kd == "x2":                                        # cube: edge × edge
            v = vs[0] * vs[0]
        else:
            raise ValueError(kd)
        if v is not None and v > 0:
            out.append(("%s %s" % (show(v), sqr(u) if sq else cub(u)), ("sq" if sq else "cu", v)))
    return out


def edge_txt(t, u):
    return "%s %s" % (fx(t), u)


# ------------------------------------------------------------ set 1: pack with small cubes
def set_pack(rnd):
    its = []
    # volume of one small cube
    its.append(mcq(fig(packed_svg(2, 2, 2, None, hi=True, label="a unit cube cut into 8 small cubes", px=34)) +
                   "A cube with 1-unit edges is cut into small cubes. Each small cube has edges of %s unit. "
                   "What is the volume of one small cube?" % fr(1, 2),
                   ("%s cubic unit" % fr(1, 8), F(1, 8)),
                   [("%s cubic unit" % fr(1, 2), F(1, 2)), ("%s cubic unit" % fr(1, 4), F(1, 4)),
                    ("%s cubic units" % show(F(3, 2)), F(3, 2))],
                   "8 small cubes fill 1 cubic unit, so each one is %s cubic unit. "
                   "The formula agrees: %s × %s × %s = %s." % (fr(1, 8), fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 8))))
    its.append(mcq(fig(packed_svg(3, 3, 3, None, hi=True, label="a unit cube cut into 27 small cubes", px=24)) +
                   "A cube with 1-unit edges is cut into small cubes with edges of %s unit. "
                   "What is the volume of one small cube?" % fr(1, 3),
                   ("%s cubic unit" % fr(1, 27), F(1, 27)),
                   [("%s cubic unit" % fr(1, 3), F(1, 3)), ("%s cubic unit" % fr(1, 9), F(1, 9)), ("1 cubic unit", F(1))],
                   "3 × 3 × 3 = 27 small cubes fill 1 cubic unit, so each is %s cubic unit: "
                   "%s × %s × %s = %s. (Adding %s + %s + %s = 1 is not volume.)"
                   % (fr(1, 27), fr(1, 3), fr(1, 3), fr(1, 3), fr(1, 27), fr(1, 3), fr(1, 3), fr(1, 3))))
    its.append(mcq("A small cube has edges that are %s inch long. What is its volume?" % fr(1, 4),
                   (q3(F(1, 64), "in"), F(1, 64)),
                   [(q3(F(3, 4), "in"), F(3, 4)), (q3(F(1, 16), "in"), F(1, 16)), (q3(F(1, 12), "in"), F(1, 12))],
                   "V = %s × %s × %s = %s in³. Multiply the edge by itself 3 times, not by 3 (3 × %s = %s)."
                   % (fr(1, 4), fr(1, 4), fr(1, 4), fr(1, 64), fr(1, 4), fr(3, 4))))
    its.append(mcq("A wooden block is a cube with edges of %s foot. What is its volume?" % fr(1, 2),
                   (q3(F(1, 8), "ft"), F(1, 8)),
                   [(q3(F(3, 2), "ft"), F(3, 2)), (q3(F(1, 4), "ft"), F(1, 4)), ("%s ft²" % fr(1, 8), ("sq", F(1, 8)))],
                   "V = %s × %s × %s = %s ft³. Volume uses cubic units (ft³), not square units." % (fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 8))))
    # how many small cubes make 1 cubic unit
    its.append(mcq("How many cubes with %s-inch edges fill a cube with 1-inch edges?" % fr(1, 2), ("8", 8),
                   [("2", 2), ("4", 4), ("6", 6)],
                   "2 small cubes fit along each edge: 2 × 2 × 2 = 8. So each small cube is %s in³." % fr(1, 8)))
    its.append(mcq("How many cubes with %s-centimeter edges fill a cube with 1-centimeter edges?" % fr(1, 4), ("64", 64),
                   [("4", 4), ("16", 16), ("12", 12)],
                   "4 small cubes fit along each edge: 4 × 4 × 4 = 64. (16 is only one layer.)"))
    # packed boxes with a picture
    seen = set()
    pics = []
    for i in range(8):
        k = 2 if i < 6 else 3
        while True:
            a, b, c = rnd.randint(3, 6), rnd.randint(2, 3), rnd.randint(2, 4)
            if (a, b, c) in seen or a <= b or a % k == 0 and b % k == 0 and c % k == 0:
                continue
            if k == 3 and a * b * c > 72:
                continue
            break
        seen.add((a, b, c))
        pics.append((a, b, c, k))
    for i, (a, b, c, k) in enumerate(pics):
        u = UNITS[i % 3]
        e = F(1, k)
        n = a * b * c
        V = F(n, k ** 3)
        word = {"in": "inch", "ft": "foot", "cm": "centimeter"}[u]
        sv = packed_svg(a, b, c, e, u)
        how = ("Along the edges: %s ÷ %s = %d, %s ÷ %s = %d, %s ÷ %s = %d cubes. %d × %d × %d = %d cubes."
               % (show(a * e), fr(1, k), a, show(b * e), fr(1, k), b, show(c * e), fr(1, k), c, a, b, c, n))
        if i % 2 == 0:
            q = fig(sv) + "The box is packed with cubes that have %s-%s edges. How many cubes fill the box?" % (fr(1, k), word)
            cands = [(f(visible_cubes(a, b, c)), visible_cubes(a, b, c)), (f(a * c), a * c), (f(a + b + c), a + b + c),
                     (show(V), V)]
            its.append(mcq(q, (f(n), n), cands, how + " Count the hidden cubes, too."))
        else:
            q = (fig(sv) + "The box is packed with cubes that have %s-%s edges. What is the volume of the box?"
                 % (fr(1, k), word))
            ee = (how + " Each cube is %s %s³, so V = %d × %s = %s %s³. Check: %s × %s × %s = %s."
                  % (fr(1, k ** 3), u, n, fr(1, k ** 3), show(V), u, show(a * e), show(b * e), show(c * e), show(V)))
            cands = [(q3(F(n), u), F(n)), (q3(F(n, k), u), F(n, k)), (q3(F(n, k * k), u), F(n, k * k)),
                     (q3(F(visible_cubes(a, b, c), k ** 3), u), F(visible_cubes(a, b, c), k ** 3))]
            its.append(mcq(q, (q3(V, u), V), cands, ee))
    # how many half-unit cubes fill a box (no picture)
    for (L, W, H), u in [((F(2), F(1), F(3, 2)), "in"), ((F(5, 2), F(2), F(1)), "ft"), ((F(3), F(3, 2), F(2)), "cm")]:
        n = int(L * W * H * 8)
        V = L * W * H
        word = {"in": "inch", "ft": "foot", "cm": "centimeter"}[u]
        q = ("How many cubes with %s-%s edges fill a box that is %s %s long, %s %s wide and %s %s tall?"
             % (fr(1, 2), word, show(L), u, show(W), u, show(H), u))
        cnt = [int(x * 2) for x in (L, W, H)]
        e = ("Along the edges: %d, %d and %d cubes (2 cubes for each %s). %d × %d × %d = %d cubes. "
             "Check: V = %s %s³, and each cube is %s %s³: %s × 8 = %d."
             % (cnt[0], cnt[1], cnt[2], word, cnt[0], cnt[1], cnt[2], n, show(V), u, fr(1, 8), u, show(V), n))
        its.append(mcq(q, (f(n), n), [(show(V), V), (show(V * 2), V * 2), (f(sum(cnt)), sum(cnt)),
                                      (f(cnt[0] * cnt[1]), cnt[0] * cnt[1])], e))
    # N small cubes -> volume
    for n, k, u in [(30, 2, "in"), (54, 3, "ft"), (96, 4, "cm")]:
        V = F(n, k ** 3)
        word = {"in": "inch", "ft": "foot", "cm": "centimeter"}[u]
        q = "A box is packed with %d cubes that have %s-%s edges, with no gaps. What is the volume of the box?" % (n, fr(1, k), word)
        e = ("One cube is %s × %s × %s = %s %s³. %d cubes: %d × %s = %s = <b>%s</b>."
             % (fr(1, k), fr(1, k), fr(1, k), fr(1, k ** 3), u, n, n, fr(1, k ** 3), fr(n, k ** 3), q3(V, u)))
        its.append(mcq(q, (q3(V, u), V), [(q3(F(n), u), F(n)), (q3(F(n, k), u), F(n, k)), (q3(F(n, k * k), u), F(n, k * k))], e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Pack a box with small cubes", "items": its}


# ------------------------------------------------------------ set 2: V = l × w × h
def rand_edge(rnd, kind):
    if kind == "frac":
        d = rnd.choice([2, 3, 4])
        n = rnd.randint(1, d - 1)
        while math.gcd(n, d) > 1:
            n = rnd.randint(1, d - 1)
        return (0, n, d)
    if kind == "mixed":
        d = rnd.choice([2, 2, 3, 4])
        n = rnd.randint(1, d - 1)
        while math.gcd(n, d) > 1:
            n = rnd.randint(1, d - 1)
        return (rnd.randint(1, 5), n, d)
    return (rnd.randint(2, 8), 0, 1)


def set_formula(rnd, seen):
    its = []
    kinds = [("mixed", "whole", "whole"), ("mixed", "mixed", "whole"), ("whole", "frac", "whole"), ("mixed", "whole", "mixed"),
             ("whole", "whole", "frac"), ("mixed", "mixed", "whole"), ("mixed", "frac", "whole"), ("whole", "mixed", "mixed"),
             ("mixed", "whole", "whole"), ("mixed", "mixed", "mixed")]
    orders = [["add", "parts", "two", "sq"], ["parts", "add", "badimp", "sq"], ["add", "two", "sq", "two2"],
              ["parts", "whole", "add", "sq"]]
    for i, kd in enumerate(kinds):
        while True:
            ts = [rand_edge(rnd, x) for x in kd]
            vs = [val(t) for t in ts]
            V = vs[0] * vs[1] * vs[2]
            key = tuple(sorted(vs))
            if key in seen or len(set(vs)) < 3 or V > 60 or vs[0] < vs[1] and kd[0] == "mixed" and kd[1] == "whole":
                continue
            break
        seen.add(key)
        u = UNITS[i % 4]
        L, W, H = vs
        q = fig(prism_svg(L, W, H, u, label="rectangular prism with fractional edges")) + "What is the volume of this rectangular prism?"
        its.append(mcq(q, (q3(V, u), ("cu", V)), wrongs(ts, u, orders[i % 4] + ["add", "two", "sq", "two2", "whole"]),
                       prod_e(ts, u) + (" Change mixed numbers to fractions before you multiply."
                                        if any(t[0] and t[1] for t in ts) else "")))
    for t, u in [((1, 1, 2), "in"), ((0, 2, 3), "m"), ((2, 1, 2), "cm")]:
        ts = [t, t, t]
        V = val(t) ** 3
        q = "A cube has edges that are %s %s long. What is its volume?" % (fx(t), u)
        its.append(mcq(q, (q3(V, u), ("cu", V)), wrongs(ts, u, ["x3", "x2", "parts", "sq"]),
                       prod_e(ts, u, "Every edge is the same, so V = ")))
    words = [((3, 1, 2), (2, 0, 1), (0, 3, 4), "ft"), ((5, 0, 1), (1, 1, 3), (2, 1, 4), "in"),
             ((4, 1, 2), (0, 2, 3), (6, 0, 1), "cm"), ((2, 3, 4), (1, 1, 2), (4, 0, 1), "m"),
             ((6, 1, 4), (2, 2, 5), (1, 1, 2), "in")]
    for i, (a, b, c, u) in enumerate(words):
        ts = [a, b, c]
        V = val(a) * val(b) * val(c)
        q = "A rectangular prism is %s long, %s wide and %s tall. What is its volume?" % (edge_txt(a, u), edge_txt(b, u), edge_txt(c, u))
        its.append(mcq(q, (q3(V, u), ("cu", V)), wrongs(ts, u, orders[(i + 1) % 4] + ["add", "two", "sq", "badimp"]), prod_e(ts, u)))
    for a, b, c, u in [((3, 1, 2), (2, 0, 1), (0, 1, 2), "in"), ((2, 1, 4), (1, 1, 2), (3, 0, 1), "ft")]:
        q = "A box is %s long, %s wide and %s tall. Which expression gives its volume?" % (edge_txt(a, u), edge_txt(b, u), edge_txt(c, u))
        right = "%s × %s × %s" % (fx(a), fx(b), fx(c))
        V = val(a) * val(b) * val(c)
        e = "Volume = length × width × height = %s = %s %s³." % (right, show(V), u)
        its.append(mcq(q, (right, 1), [("%s + %s + %s" % (fx(a), fx(b), fx(c)), 2), ("%s × %s" % (fx(a), fx(b)), 3),
                                       ("%s × %s × %s" % (f(a[0]), f(b[0]), f(c[0]) if c[0] else fx(c)), 4)],
                       e + " Keep the fraction parts: using only the whole numbers changes the edges."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Use V = l × w × h with fractions", "items": its}


# ------------------------------------------------------------ set 3: V = B × h
def bh_wrongs(B, h, u, order):
    out = []
    for kd in order:
        v, sq = None, False
        if kd == "add":
            v = B + h
        elif kd == "sq":
            v, sq = B * h, True
        elif kd == "half":                                       # B × h ÷ 2 (triangle formula)
            v = B * h / 2
        elif kd == "whole":                                      # dropped the fraction parts
            wb, wh = B.numerator // B.denominator, h.numerator // h.denominator
            if wb and wh and (B.denominator > 1 or h.denominator > 1):
                v = F(wb * wh)
        elif kd == "parts":
            wb, wh = B.numerator // B.denominator, h.numerator // h.denominator
            if wb and wh and B.denominator > 1 and h.denominator > 1:
                v = F(wb * wh) + (B - wb) * (h - wh)
        elif kd == "B":
            v = B
        elif kd == "2h":                                         # B × 2h
            v = B * h * 2
        if v is not None and v > 0:
            out.append(("%s %s" % (show(v), sqr(u) if sq else cub(u)), ("sq" if sq else "cu", v)))
    return out


def bh_e(B, h, u):
    s = "V = B × h = %s × %s" % (show(B), show(h))
    if (B.denominator > 1 and B > 1) or (h.denominator > 1 and h > 1):
        s += " = %s × %s" % (raw(B), raw(h))
    num, den = B.numerator * h.numerator, B.denominator * h.denominator
    s += " = %s" % (fr(num, den) if den > 1 else f(num))
    V = B * h
    if (num, den) != (V.numerator, V.denominator) or V.denominator > 1 and V > 1:
        s += " = %s" % show(V)
    return s + " %s³." % u


def set_base(rnd):
    its = []
    figs = [(F(15, 2), F(3, 2), "in", (3.0, 2.0)), (F(12), F(5, 4), "ft", (3.2, 1.8)), (F(9, 4), F(4), "cm", (2.2, 1.6)),
            (F(20, 3), F(3, 4), "m", (3.4, 2.2)), (F(21, 2), F(7, 3), "in", (3.0, 2.0)), (F(18), F(5, 6), "ft", (3.4, 2.4))]
    orders = [["add", "sq", "parts", "half"], ["add", "whole", "sq", "half"], ["sq", "add", "half", "B"],
              ["add", "half", "sq", "B"], ["parts", "add", "sq", "whole"], ["add", "sq", "half", "B"]]
    for (B, h, u, shp), od in zip(figs, orders):
        q = (fig(base_svg(B, h, u, shp)) + "The shaded base of this prism has area B. What is the volume of the prism?")
        its.append(mcq(q, (q3(B * h, u), ("cu", B * h)), bh_wrongs(B, h, u, od + ["add", "sq", "half", "B", "2h"]),
                       bh_e(B, h, u) + " B is already length × width, so multiply it by the height only."))
    texts = [(F(6), F(5, 2), "in"), (F(27, 4), F(2), "ft"), (F(10), F(3, 5), "cm"), (F(35, 2), F(4, 3), "in"),
             (F(16, 3), F(9, 4), "m"), (F(14), F(15, 4), "ft")]
    for i, (B, h, u) in enumerate(texts):
        q = ("The base of a rectangular prism has an area of %s %s. The prism is %s %s tall. What is its volume?"
             % (show(B), sqr(u), show(h), u))
        its.append(mcq(q, (q3(B * h, u), ("cu", B * h)), bh_wrongs(B, h, u, orders[i] + ["add", "sq", "half", "B", "2h"]), bh_e(B, h, u)))
    # find B first
    for i, (l, w, h, u) in enumerate([(F(5, 2), F(2), F(3, 2), "ft"), (F(4), F(9, 4), F(2, 3), "in"),
                                      (F(7, 2), F(3, 2), F(2), "cm"), (F(6), F(4, 3), F(5, 2), "m")]):
        B = l * w
        if i < 2:
            q = ("A prism has a base that is %s %s long and %s %s wide. It is %s %s tall. What is B, the area of the base?"
                 % (show(l), u, show(w), u, show(h), u))
            e = "B = length × width = %s × %s = %s %s. The height is not part of the base." % (show(l), show(w), show(B), sqr(u))
            its.append(mcq(q, ("%s %s" % (show(B), sqr(u)), ("sq", B)),
                           [("%s %s" % (show(B * h), sqr(u)), ("sq", B * h)), ("%s %s" % (show(l + w), sqr(u)), ("sq", l + w)),
                            ("%s %s" % (show(B), cub(u)), ("cu", B)), ("%s %s" % (show(2 * (l + w)), sqr(u)), ("sq", 2 * (l + w)))], e))
        else:
            q = ("A prism has a base that is %s %s long and %s %s wide. It is %s %s tall. Use B × h to find its volume."
                 % (show(l), u, show(w), u, show(h), u))
            e = "B = %s × %s = %s %s. " % (show(l), show(w), show(B), sqr(u)) + bh_e(B, h, u)
            its.append(mcq(q, (q3(B * h, u), ("cu", B * h)), bh_wrongs(B, h, u, ["B", "add", "sq", "half"]), e))
    # layers of half-inch cubes
    for per, layers, k, u in [(12, 5, 2, "in"), (20, 3, 2, "cm"), (18, 4, 3, "ft"), (24, 6, 2, "in")]:
        n = per * layers
        V = F(n, k ** 3)
        word = {"in": "inch", "ft": "foot", "cm": "centimeter"}[u]
        q = ("A box is filled with cubes that have %s-%s edges. Each layer has %d cubes, and there are %d layers. "
             "What is the volume of the box?" % (fr(1, k), word, per, layers))
        e = ("Cubes: %d × %d = %d. Each cube is %s %s³, so V = %d × %s = %s %s³. "
             "(B × h works too: B = %d × %s %s², h = %d × %s %s.)"
             % (per, layers, n, fr(1, k ** 3), u, n, fr(1, k ** 3), show(V), u, per, fr(1, k * k), u, layers, fr(1, k), u))
        its.append(mcq(q, (q3(V, u), V), [(q3(F(n), u), F(n)), (q3(F(n, k), u), F(n, k)), (q3(F(n, k * k), u), F(n, k * k)),
                                         (q3(F(per + layers), u), F(per + layers))], e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Use V = B × h", "items": its}


# ------------------------------------------------------------ set 4: decimals and missing edges
MISSING = [(F(5, 2), F(3, 2), F(3, 2), "ft", "h"), (F(4), F(5, 2), F(3, 4), "in", "h"), (F(3), F(4, 3), F(7, 2), "cm", "w"),
           (F(9, 2), F(2), F(5, 3), "m", "l"), (F(6), F(3, 2), F(5, 4), "in", "h"), (F(7, 2), F(5, 2), F(2), "ft", "w"),
           (F(8), F(3, 4), F(5, 2), "cm", "h"), (F(10, 3), F(3), F(3, 2), "in", "l")]


def dec_q(its, a, b, c, u, ctx=None):
    a, b, c = D(a), D(b), D(c)
    V = a * b * c
    q = ctx or ("A rectangular prism is %s %s long, %s %s wide and %s %s tall. What is its volume?"
                % (dz(a), u, dz(b), u, dz(c), u))
    e = "V = %s × %s × %s = %s × %s = <b>%s %s³</b>." % (dz(a), dz(b), dz(c), dz(a * b), dz(c), dz(V), u)
    cands = [("%s %s" % (dz(a + b + c), cub(u)), ("cu", a + b + c)), ("%s %s" % (dz(V * 10), cub(u)), ("cu", V * 10)),
             ("%s %s" % (dz(V), sqr(u)), ("sq", V)), ("%s %s" % (dz(V / 10), cub(u)), ("cu", V / 10)),
             ("%s %s" % (dz(a * b), cub(u)), ("cu", a * b))]
    its.append(mcq(q, ("%s %s" % (dz(V), cub(u)), ("cu", V)), cands, e + " Count the decimal places to place the point."))


def set_missing(rnd):
    its = []
    for a, b, c, u in [("2.5", "1.2", "4", "m"), ("1.5", "3", "2.4", "ft"), ("6", "2.5", "0.8", "cm"),
                       ("12", "4.5", "2", "in"), ("0.5", "0.4", "3", "m"), ("4.2", "2.5", "3", "in")]:
        dec_q(its, a, b, c, u)
    # missing edge with fractions
    cases = MISSING
    for i, (L, W, H, u, miss) in enumerate(cases):
        V = L * W * H
        known = {"h": (L, W), "l": (W, H), "w": (L, H)}[miss]
        ans = {"h": H, "l": L, "w": W}[miss]
        a, b = known
        B = a * b
        assert V / B == ans
        e = ("%s × %s = %s, so %s × ? = %s. ? = %s. Check: %s × %s × %s = %s."
             % (show(a), show(b), show(B), show(B), show(V), div_e(V, B, u), show(L), show(W), show(H), show(V)))
        cands = [("%s %s" % (show(V / a), u), V / a), ("%s %s" % (show(V - B), u), V - B), ("%s %s" % (show(B / V), u), B / V),
                 ("%s %s" % (show(V * B), u), V * B), ("%s %s" % (show(V / (a + b)), u), V / (a + b))]
        if i < 4:
            q = (fig(prism_svg(L, W, H, u, miss, "rectangular prism with one unknown edge")) +
                 "The volume of this prism is %s. What is the length of the edge marked ?" % q3(V, u))
        else:
            word = {"h": "How tall is it?", "l": "How long is it?", "w": "How wide is it?"}[miss]
            given = {"h": "%s %s long and %s %s wide" % (show(L), u, show(W), u),
                     "l": "%s %s wide and %s %s tall" % (show(W), u, show(H), u),
                     "w": "%s %s long and %s %s tall" % (show(L), u, show(H), u)}[miss]
            q = "A rectangular prism has a volume of %s. It is %s. %s" % (q3(V, u), given, word)
        its.append(mcq(q, ("%s %s" % (show(ans), u), ans), cands, e))
    # B and V known
    for V, B, u in [(F(45, 4), F(9, 2), "ft"), (F(20), F(15, 2), "in"), (F(35, 3), F(14), "cm")]:
        h = V / B
        q = "A prism has a volume of %s. The area of its base is %s %s. What is its height?" % (q3(V, u), show(B), sqr(u))
        e = "V = B × h, so %s × h = %s. h = %s." % (show(B), show(V), div_e(V, B, u))
        its.append(mcq(q, ("%s %s" % (show(h), u), h),
                       [("%s %s" % (show(V - B), u), V - B), ("%s %s" % (show(B / V), u), B / V),
                        ("%s %s" % (show(V * B), u), V * B), ("%s %s" % (show(h), cub(u)), ("cu", h))], e))
    # decimal missing edge
    V, a, b = D("18"), D("2.5"), D("1.2")
    q = "A rectangular prism has a volume of 18 m³. It is 2.5 m long and 1.2 m wide. How tall is it?"
    e = "2.5 × 1.2 = 3 m², so 3 × h = 18. h = 18 ÷ 3 = <b>6 m</b>. Check: 2.5 × 1.2 × 6 = 18."
    its.append(mcq(q, ("6 m", D(6)), [("7.2 m", D("7.2")), ("14.3 m", D("14.3")), ("15 m", D(15)), ("54 m", D(54))], e))
    # cube edge from its volume
    for V, s, u in [(F(27, 8), F(3, 2), "in"), (F(125, 8), F(5, 2), "ft")]:
        q = "A cube has a volume of %s. How long is each edge?" % q3(V, u)
        e = ("All 3 edges of a cube are equal. Find a number you multiply 3 times to get %s: "
             "%s × %s × %s = %s. Each edge is <b>%s %s</b>." % (raw(V), raw(s), raw(s), raw(s), raw(V), show(s), u))
        its.append(mcq(q, ("%s %s" % (show(s), u), s),
                       [("%s %s" % (show(V / 3), u), V / 3), ("%s %s" % (show(V / 2), u), V / 2),
                        ("%s %s" % (show(s.numerator), u), F(s.numerator))], e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Decimals and missing edges", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def lwh(story, ts, u, order, extra=""):
        V = math.prod(val(t) for t in ts)
        its.append(mcq(story, (q3(V, u), ("cu", V)), wrongs(ts, u, order + ["add", "two", "sq", "two2"]), prod_e(ts, u) + extra))

    n, he, his = P.next()
    lwh("%s's fish tank is %s ft long, 1 ft wide and %s ft tall. What is the volume of the tank?" % (n, fx((2, 1, 2)), fx((1, 1, 2))),
        [(2, 1, 2), (1, 0, 1), (1, 1, 2)], "ft", ["add", "parts", "two", "sq"])
    n, he, his = P.next()
    lwh("%s fills a sandbox that is 6 ft long and %s ft wide with sand %s ft deep. How many cubic feet of sand does %s need?"
        % (n, fx((4, 1, 2)), fr(3, 4), he), [(6, 0, 1), (4, 1, 2), (0, 3, 4)], "ft", ["two", "add", "sq"],
        " The depth of the sand is the height.")
    lwh("A cereal box is %s in wide, %s in deep and 11 in tall. What is its volume?" % (fx((7, 1, 2)), fx((2, 1, 2))),
        [(7, 1, 2), (2, 1, 2), (11, 0, 1)], "in", ["parts", "add", "two", "sq"])
    lwh("A raised garden bed is %s ft long, 3 ft wide and %s ft deep. How much soil fills it?" % (fx((8, 1, 3)), fx((1, 1, 4))),
        [(8, 1, 3), (3, 0, 1), (1, 1, 4)], "ft", ["parts", "whole", "add", "sq"])
    lwh("A brick is %s in long, %s in wide and %s in tall. What is its volume?" % (fx((7, 1, 2)), fx((3, 1, 2)), fx((2, 1, 4))),
        [(7, 1, 2), (3, 1, 2), (2, 1, 4)], "in", ["parts", "add", "badimp", "two"])
    lwh("The inside of a refrigerator is %s ft wide, 2 ft deep and %s ft tall. How much space is inside?" % (fx((2, 1, 2)), fx((5, 1, 2))),
        [(2, 1, 2), (2, 0, 1), (5, 1, 2)], "ft", ["parts", "add", "two", "sq"])
    n, he, his = P.next()
    lwh("%s keeps %s cards in a cube-shaped box with %s-inch edges. What is the volume of the box?" % (n, his, fx((4, 1, 2))),
        [(4, 1, 2)] * 3, "in", ["x3", "x2", "parts", "sq"])
    # half-inch and quarter-inch cubes
    n, he, his = P.next()
    its.append(mcq("%s fills a gift box that is 3 in long, 2 in wide and %s in tall with cubes that have %s-inch edges. "
                   "How many cubes fit?" % (n, fx((1, 1, 2)), fr(1, 2)), ("72", 72), [("9", 9), ("18", 18), ("13", 13)],
                   "Along the edges: 6, 4 and 3 cubes (2 for each inch). 6 × 4 × 3 = 72 cubes. "
                   "Check: V = 3 × 2 × %s = 9 in³, and 9 × 8 = 72." % fx((1, 1, 2))))
    assert F(3) * 2 * F(3, 2) * 8 == 72
    n, he, his = P.next()
    its.append(mcq("%s cuts a block of cheese that is 4 in long, %s in wide and %s in tall into cubes with %s-inch edges. "
                   "How many cubes does %s get?" % (n, fx((2, 1, 2)), fx((1, 1, 2)), fr(1, 2), he), ("120", 120),
                   [("15", 15), ("30", 30), ("16", 16)],
                   "Along the edges: 8, 5 and 3 cubes. 8 × 5 × 3 = 120 cubes. "
                   "Check: V = 4 × %s × %s = 15 in³, and 15 × 8 = 120." % (fx((2, 1, 2)), fx((1, 1, 2)))))
    assert F(4) * F(5, 2) * F(3, 2) * 8 == 120
    its.append(mcq("A jewelry box is 2 in long, %s in wide and 1 in tall. How many cubes with %s-inch edges fill it?"
                   % (fx((1, 1, 2)), fr(1, 4)), ("192", 192), [("3", 3), ("12", 12), ("18", 18)],
                   "4 cubes fit along each inch. Along the edges: 8, 6 and 4 cubes. 8 × 6 × 4 = 192. "
                   "Check: V = 3 in³, and each cube is %s in³: 3 × 64 = 192." % fr(1, 64)))
    assert F(2) * F(3, 2) * 1 * 64 == 192
    its.append(mcq("A box holds 120 sugar cubes with no gaps. Each sugar cube has %s-inch edges. What is the volume of the sugar?"
                   % fr(1, 2), (q3(F(15), "in"), F(15)), [(q3(F(120), "in"), F(120)), (q3(F(60), "in"), F(60)), (q3(F(30), "in"), F(30))],
                   "One sugar cube is %s in³. 120 × %s = %s = <b>15 in³</b>. (60 forgets that each cube is %s, not %s.)"
                   % (fr(1, 8), fr(1, 8), fr(120, 8), fr(1, 8), fr(1, 2))))
    # water partly filling a tank
    its.append(mcq("A tank is 3 ft long, %s ft wide and 2 ft tall. Water fills it to a depth of %s ft. What is the volume of the water?"
                   % (fx((1, 1, 2)), fx((1, 1, 4))), (q3(F(45, 8), "ft"), F(45, 8)),
                   [(q3(F(9), "ft"), F(9)), (q3(F(9, 2), "ft"), F(9, 2)), (q3(F(27, 8), "ft"), F(27, 8))],
                   "Use the depth of the water, not the height of the tank: 3 × %s × %s = 3 × %s × %s = %s = <b>%s ft³</b>. "
                   "(9 ft³ is the whole tank.)" % (fx((1, 1, 2)), fx((1, 1, 4)), fr(3, 2), fr(5, 4), fr(45, 8), show(F(45, 8)))))
    # missing height
    n, he, his = P.next()
    its.append(mcq("%s has 30 ft³ of sand for a sandbox that is 6 ft long and 4 ft wide. How deep will the sand be?" % n,
                   ("%s ft" % fx((1, 1, 4)), F(5, 4)), [("5 ft", F(5)), ("6 ft", F(6)), ("%s ft" % fr(4, 5), F(4, 5))],
                   "B = 6 × 4 = 24 ft². 24 × h = 30, so h = 30 ÷ 24 = %s = <b>%s ft</b>." % (fr(30, 24), fx((1, 1, 4)))))
    its.append(mcq("A moving box has a volume of %s. Its base is %s ft long and %s ft wide. How tall is it?"
                   % (q3(F(45, 8), "ft"), fx((2, 1, 2)), fx((1, 1, 2))), ("%s ft" % fx((1, 1, 2)), F(3, 2)),
                   [("%s ft" % show(F(9, 4)), F(9, 4)), ("%s ft" % show(F(15, 8)), F(15, 8)), ("%s ft" % fr(2, 3), F(2, 3))],
                   "B = %s × %s = %s ft². h = %s." % (fx((2, 1, 2)), fx((1, 1, 2)), show(F(15, 4)), div_e(F(45, 8), F(15, 4), "ft"))))
    assert F(5, 2) * F(3, 2) * F(3, 2) == F(45, 8)
    # decimals
    dec_q(its, "40", "25", "20.5", "cm", "An aquarium is 40 cm long and 25 cm wide. The water in it is 20.5 cm deep. What is the volume of the water?")
    dec_q(its, "10", "4.5", "1.2", "m", "A wading pool is 10 m long and 4.5 m wide. The water is 1.2 m deep. How much water is in the pool?")
    # compare two boxes
    its.append(mcq("Box A is 3 in by %s in by 2 in. Box B is a cube with %s-inch edges. Which box has the greater volume, and by how much?"
                   % (fx((2, 1, 2)), fx((2, 1, 2))), ("B, by %s in³" % fr(5, 8), 1),
                   [("A, by %s in³" % fr(5, 8), 2), ("Same volume", 3), ("A, by %s in³" % show(F(31, 8)), 4)],
                   "A: 3 × %s × 2 = 15 in³. B: %s × %s × %s = %s = %s in³. %s − 15 = %s, so B is greater by <b>%s in³</b>. "
                   "(Adding the edges gives %s for both, but that is not volume.)"
                   % (fx((2, 1, 2)), fr(5, 2), fr(5, 2), fr(5, 2), fr(125, 8), show(F(125, 8)), show(F(125, 8)), fr(5, 8), fr(5, 8),
                      show(F(15, 2)))))
    assert F(125, 8) - 15 == F(5, 8) and 3 + F(5, 2) + 2 == 3 * F(5, 2) and 12 - (8 + F(1, 8)) == F(31, 8)
    # many boxes, and B × h
    n, he, his = P.next()
    its.append(mcq("%s stacks 10 hay bales. Each bale is 3 ft long, %s ft wide and %s ft tall. What is the total volume of the bales?"
                   % (n, fx((1, 1, 2)), fx((1, 1, 3))), (q3(F(60), "ft"), F(60)),
                   [(q3(F(6), "ft"), F(6)), (q3(F(45), "ft"), F(45)), (q3(F(175, 3), "ft"), F(175, 3))],
                   "One bale: 3 × %s × %s = 3 × %s × %s = 6 ft³. Ten bales: 10 × 6 = <b>60 ft³</b>."
                   % (fx((1, 1, 2)), fx((1, 1, 3)), fr(3, 2), fr(4, 3))))
    assert 3 * F(3, 2) * F(4, 3) == 6 and 10 * (3 + F(3, 2) + F(4, 3)) == F(175, 3) and 10 * 3 * F(3, 2) == 45
    its.append(mcq("The bottom of a shoebox has an area of 72 in². The box is %s in tall. What is its volume?" % fx((4, 1, 2)),
                   (q3(F(324), "in"), ("cu", F(324))),
                   [(q3(F(153, 2), "in"), ("cu", F(153, 2))), (q3(F(288), "in"), ("cu", F(288))), ("324 in²", ("sq", F(324)))],
                   "V = B × h = 72 × %s = 72 × %s = %s = <b>324 in³</b>. (288 drops the %s.)"
                   % (fx((4, 1, 2)), fr(9, 2), fr(648, 2), fr(1, 2))))
    assert 72 * F(9, 2) == 324
    its.append(mcq("A moving company charges for the space a load takes up in a truck. Which unit fits that measure best?",
                   ("cubic feet (ft³)", 1), [("square feet (ft²)", 2), ("feet (ft)", 3), ("pounds (lb)", 4)],
                   "Space inside is volume, so it is measured in cubic units like ft³. "
                   "Square feet measure area, feet measure length, and pounds measure weight."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Volume word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    h = fr(1, 2)
    return (
        "<h2>The big idea</h2>"
        "<p>Volume counts how many cubes fill a box. When an edge is a fraction, use <b>small cubes</b> "
        "that fit the fraction. A cube with " + h + "-inch edges is " + h + " × " + h + " × " + h + " = "
        + fr(1, 8) + " in³, because 8 of them fill a 1-inch cube.</p>"
        "<figure class='sn-fig'>" + packed_svg(2, 2, 2, None, hi=True, label="a unit cube cut into 8 small cubes", px=34) +
        "<figcaption>A 1-inch cube cut into 8 cubes with " + h + "-inch edges. One small cube is " + fr(1, 8)
        + " in³.</figcaption></figure>"
        "<h2>Pack the box, then check with the formula</h2>"
        "<p>Count how many small cubes fit along each edge. Multiply to get the number of cubes. "
        "Then multiply by the volume of one small cube.</p>"
        "<figure class='sn-fig'>" + packed_svg(4, 2, 3, F(1, 2), "in") +
        "<figcaption>A box 2 in × 1 in × " + show(F(3, 2)) + " in holds 4 × 2 × 3 = 24 cubes. 24 × "
        + fr(1, 8) + " = 3 in³. The formula gives the same: 2 × 1 × " + show(F(3, 2)) + " = 3 in³.</figcaption></figure>"
        "<h2>The formulas</h2>"
        "<p><b>V = l × w × h</b> and <b>V = B × h</b>, where B is the area of the base. They work for fractions, too. "
        "Change mixed numbers to fractions, multiply the tops and the bottoms, then simplify.</p>"
        "<figure class='sn-fig'>" + prism_svg(F(5, 2), F(4, 3), F(3), "ft", label="rectangular prism with fractional edges") +
        "<figcaption>V = " + show(F(5, 2)) + " × " + show(F(4, 3)) + " × 3 = " + fr(5, 2) + " × " + fr(4, 3)
        + " × 3 = " + fr(60, 6) + " = 10 ft³.</figcaption></figure>"
        + ex("Use V = B × h", "The base of a box has an area of " + show(F(15, 2)) + " in². The box is " + show(F(3, 2))
             + " in tall. What is its volume?",
             fr(15, 2) + " × " + fr(3, 2) + " = " + fr(45, 4) + " = " + show(F(45, 4)) + ".", show(F(45, 4)) + " in³")
        + ex("Find a missing edge", "A box has a volume of " + show(F(45, 8)) + " ft³. It is " + show(F(5, 2)) + " ft long and "
             + show(F(3, 2)) + " ft wide. How tall is it?",
             "B = " + fr(5, 2) + " × " + fr(3, 2) + " = " + fr(15, 4) + " ft². h = " + fr(45, 8) + " ÷ " + fr(15, 4) + " = "
             + fr(45, 8) + " × " + fr(4, 15) + " = " + fr(180, 120) + " = " + show(F(3, 2)) + ".", show(F(3, 2)) + " ft")
        + "<h2>Units</h2>"
        + table(["Measure", "Unit", "Example"], [
            ["Length (1 edge)", "in, ft, cm, m", show(F(5, 2)) + " ft"],
            ["Area (a flat face, like the base)", "in², ft², cm², m²", show(F(15, 2)) + " in²"],
            ["Volume (space inside)", "in³, ft³, cm³, m³ (cubic inches, cubic feet …)", "10 ft³"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the small cubes and stopping: 24 in³", "Each " + h + "-inch cube is " + fr(1, 8) + " in³: 24 × "
             + fr(1, 8) + " = 3 in³"],
            ["Adding the edges: 2 + 1 + " + show(F(3, 2)) + " = " + show(F(9, 2)), "Multiply all three: 2 × 1 × " + show(F(3, 2)) + " = 3"],
            [show(F(5, 2)) + " × " + show(F(7, 2)) + " = " + show(F(25, 4)) + " (2 × 3, then " + h + " × " + h + ")",
             "Change to " + fr(5, 2) + " × " + fr(7, 2) + " first: " + fr(35, 4) + " = " + show(F(35, 4))],
            ["Multiplying only two edges", "That is the area of the base. Multiply by the height, too"],
            ["Writing in² for a volume", "Volume is in cubic units: in³"],
        ])
    )


FAQ = [
    {"q": "How do you find the volume of a rectangular prism with fractional edge lengths?",
     "a": "Multiply length × width × height. Change mixed numbers to fractions first: 2 1/2 × 1 1/3 × 3 = 5/2 × 4/3 × 3 = 10 cubic units."},
    {"q": "Why is a cube with 1/2-inch edges equal to 1/8 cubic inch?",
     "a": "Two of them fit along each edge of a 1-inch cube, so 2 × 2 × 2 = 8 of them fill it. Each one is 1/2 × 1/2 × 1/2 = 1/8 cubic inch."},
    {"q": "What is the difference between V = l × w × h and V = B × h?",
     "a": "They are the same formula. B is the area of the base (l × w), so B × h = l × w × h."},
    {"q": "How do you find a missing edge when you know the volume?",
     "a": "Multiply the two known edges, then divide the volume by that product. For V = 5 5/8 ft³ with a 2 1/2 ft by 1 1/2 ft base, h = 5 5/8 ÷ 3 3/4 = 1 1/2 ft."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(618)
    P = People(rnd)
    seen = {tuple(sorted(c[:3])) for c in MISSING}         # set 2 never repeats a prism from set 4
    seen |= {tuple(sorted(x)) for x in [(F(5, 2), 1, F(3, 2)), (F(15, 2), F(5, 2), 11), (F(25, 3), 3, F(5, 4)),
                                         (F(15, 2), F(7, 2), F(9, 4)), (F(5, 2), 2, F(11, 2)), (F(5, 2), F(4, 3), 3)]}
    sets = [set_pack(rnd), set_formula(rnd, seen), set_base(rnd), set_missing(rnd), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "volume-fractional-edges", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Volume with Fractional Edge Lengths",
        "seo_title": "Grade 6 Volume Worksheets: Fractional Edge Lengths, V = l × w × h and V = B × h",
        "short_title": "Volume with fractions",
        "domain": "Geometry",
        "standard_code": "6.G.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/G/A/2/",
        "standard_text": "Find the volume of a right rectangular prism with fractional edge lengths by packing it with unit cubes of the appropriate unit fraction edge lengths, and show that the volume is the same as would be found by multiplying the edge lengths of the prism. Apply the formulas V = l w h and V = b h to find volumes of right rectangular prisms with fractional edge lengths in the context of solving real-world and mathematical problems.",
        "meta_desc": "Free Grade 6 volume worksheets with fractional edge lengths: pack boxes with 1/2-inch cubes, use V = l × w × h and V = B × h with fractions and mixed numbers, find a missing edge, and solve real-world word problems in cubic units. 100 practice questions with an answer key.",
        "key_big": "V = l × w × h works for fractions, too.",
        "key_sub": "A cube with 1/2-unit edges is 1/2 × 1/2 × 1/2 = 1/8 cubic unit, so 8 of them fill 1 cubic unit. Change mixed numbers to fractions before you multiply: 2 1/2 × 1 1/2 × 2 = 5/2 × 3/2 × 2 = 7 1/2.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(box packed with small cubes|a unit cube cut)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
