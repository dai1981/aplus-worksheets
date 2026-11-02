# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Area and circumference of circles (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p6_circles.py
Every question says which value of pi to use (Take π = 3.14 or Take π = 22/7), as in the PSLE.
Every answer and every wrong choice is worked out with fractions.Fraction from a named student mistake
(diameter used as the radius, straight edges forgotten, r × 2 instead of r², C and A mixed up ...).
Singapore style: British spelling, ℓ/ml, no-break space in numbers of 5 or more digits, $ and ¢.
Pictures: labels never touch each other, and no line runs through a label (checked in Canvas).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F
from decimal import Decimal as Dm, ROUND_HALF_UP, getcontext

getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
LINE = "#1f4e79"
FILL = "#cfe0f1"
SHADE = "#f2b8a2"
RED = "#c0392b"
BLUE = "#2f6fb5"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
P314 = F(314, 100)
P227 = F(22, 7)


def FR(n, d):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, d)


T314 = " Take π = 3.14."
T227 = " Take π = " + FR(22, 7) + "."
PI_E = {P314: "3.14", P227: FR(22, 7)}


# ------------------------------------------------------------ numbers
def dec(x):
    x = F(x)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    assert d == 1, ("not a finite decimal", x)
    return Dm(x.numerator) / Dm(x.denominator)


def N(x, places=None):
    """Number text. places=None: exact, no trailing zeros. Integer part of 5+ digits gets no-break spaces."""
    if places is None:
        s = format(dec(x).normalize(), "f")
    else:
        q = Dm(x.numerator) / Dm(x.denominator) if isinstance(x, F) else Dm(x)
        s = format(q.quantize(Dm(1).scaleb(-places), rounding=ROUND_HALF_UP), "f")
    ip, _, fp = s.partition(".")
    if len(ip) >= 5:
        g = []
        while len(ip) > 3:
            g.insert(0, ip[-3:])
            ip = ip[:-3]
        g.insert(0, ip)
        ip = NB.join(g)
    return ip + ("." + fp if fp else "")


def U(x, u="cm", places=None):
    return "%s %s" % (N(x, places), u)


NUMRX = re.compile("^(\\$)?([\\d" + NB + "]*\\.?\\d+)( [^\\d×÷+−]+)?$")


def val(c):
    m = NUMRX.match(c)
    if not m:
        return None
    return Dm(m.group(2).replace(NB, ""))


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong. No two choices may have the same value."""
    ch = [str(correct)] + [str(x) for x in wrong]
    assert len(ch) == 4 and len(set(ch)) == 4, (q, ch)
    vs = [val(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    for v in known:
        assert v > 0, (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, r):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        r.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            r.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ drawing
def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count(".") * 0.6) * fs * 0.6


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def arc(c, r, a0, a1, n=48):
    """Points on a circle (y down), angles in degrees measured anticlockwise as seen on the page."""
    out = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        out.append((c[0] + r * math.cos(t), c[1] - r * math.sin(t)))
    return out


def pol(r, deg):
    t = math.radians(deg)
    return (r * math.cos(t), -r * math.sin(t))


class Canvas:
    """Shapes and text (y down); tracks the bounding box and writes a tight SVG."""

    def __init__(self):
        self.el, self.boxes, self.polys, self.segs = [], [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.5, col=LINE, track=True):
        self.el.append(("p", pts, fill, sw, col))
        if track:
            self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=2.5, col=LINE):
        self.poly(arc(c, r, 0, 360, 96)[:-1], fill, sw, col)

    def dot(self, c, r=3.5, col=INK):
        self.el.append(("c", c, r, col))
        self.segs.append((c, c))
        self.grow(c[0] - r, c[1] - r, c[0] + r, c[1] + r)

    def line(self, a, b, dashed=False, sw=2.4, col=INK):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, sw=4, col=RED):
        """Open path drawn over a shape edge (for highlighting); not checked against labels."""
        self.el.append(("o", pts, sw, col))

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def check(self):
        """Each label is inside one shape (or nested shapes) or outside all shapes, and no line runs through it."""
        for (x0, y0, x1, y1) in self.boxes:
            pts = [(x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 3) for i in range(7) for j in range(4)]
            hit = [sum(inside(p, poly) for p in pts) for poly in self.polys]
            hit = [h for h in hit if h]
            assert all(h == len(pts) for h in hit), ("label crosses an edge", (x0, y0, x1, y1), hit)
            for a, b in self.segs:
                for i in range(41):
                    x, y = a[0] + (b[0] - a[0]) * i / 40, a[1] + (b[1] - a[1]) * i / 40
                    assert not (x0 - 2 < x < x1 + 2 and y0 - 2 < y < y1 + 2), ("line through a label", (x0, y0))

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "o":
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linecap='round' "
                         "stroke-linejoin='round'/>" % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[3], e[2]))
            elif e[0] == "c":
                _, c, r, col = e
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (c[0] - ox, c[1] - oy, r, col))
            elif e[0] == "l":
                _, a, b, dashed, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return "".join(s)

    def svg(self, label, pad=5):
        self.check()
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        return svg_wrap(W, H, self.body(ox, oy), label)


def right_mark(cv, c, dx, dy, k=10):
    """Small right-angle mark at corner c; (dx, dy) point into the angle."""
    cv.line((c[0] + dx * k, c[1]), (c[0] + dx * k, c[1] + dy * k), sw=1.5)
    cv.line((c[0], c[1] + dy * k), (c[0] + dx * k, c[1] + dy * k), sw=1.5)


def part_fig(part, r=56):
    cv = Canvas()
    cv.circle((0, 0), r)
    if part == "circumference":
        cv.pline(arc((0, 0), r, 0, 360, 96), 6, RED)
    elif part == "radius":
        cv.line((0, 0), pol(r, 35), sw=4, col=RED)
    elif part == "diameter":
        cv.line(pol(r, 20), pol(r, 200), sw=4, col=RED)
    cv.dot((0, 0))
    return cv.svg("circle with its %s shown in red" % part)


def len_fig(lab, kind="radius", r=64):
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.dot((0, 0))
    if kind == "radius":
        cv.line((0, 0), (r, 0), sw=3)
        cv.text(r / 2 + 2, -14, lab)
    else:
        cv.line((-r, 0), (r, 0), sw=3)
        cv.text(-r / 2 + 4, -14, lab)
    return cv.svg("circle with its %s labelled %s" % (kind, lab))


def semi_fig(lab, kind="diameter", r=70):
    cv = Canvas()
    cv.poly(arc((0, 0), r, 0, 180), FILL)
    cv.dot((0, 0))
    if kind == "diameter":
        cv.text(0, 18, lab)
    else:
        cv.line((0, 0), (r, 0), sw=4, col=INK)
        cv.text(r / 2, 18, lab)
    return cv.svg("semicircle with its %s labelled %s" % (kind, lab))


def quarter_fig(lab, r=80):
    cv = Canvas()
    cv.poly([(0, 0)] + arc((0, 0), r, 0, 90), FILL)
    right_mark(cv, (0, 0), 1, -1)
    cv.text(r / 2, 16, lab)
    return cv.svg("quarter circle with radius %s" % lab)


def sq_quarter_fig(lab, S=110, shade="outside"):
    """Square with a quarter circle centred at its bottom-left corner, radius = side."""
    cv = Canvas()
    sq = [(0, 0), (S, 0), (S, -S), (0, -S)]
    q = [(0, 0)] + arc((0, 0), S, 0, 90)
    if shade == "outside":
        cv.poly(sq, SHADE)
        cv.poly(q, "#ffffff")
    else:
        cv.poly(sq, "#ffffff")
        cv.poly(q, SHADE)
    cv.text(S / 2, 16, lab)
    return cv.svg("square of side %s with a quarter circle drawn from one corner, part shaded" % lab)


def circle_in_square_fig(lab, S=110):
    cv = Canvas()
    cv.poly([(0, 0), (S, 0), (S, -S), (0, -S)], SHADE)
    cv.circle((S / 2, -S / 2), S / 2, fill="#ffffff")
    cv.text(S / 2, 16, lab)
    return cv.svg("circle that just fits inside a square of side %s, corners shaded" % lab)


def four_quarters_fig(lab, S=120):
    cv = Canvas()
    cv.poly([(0, 0), (S, 0), (S, -S), (0, -S)], SHADE)
    h = S / 2
    for (cx, cy), a0 in [((0, 0), 0), ((S, 0), 90), ((S, -S), 180), ((0, -S), 270)]:
        cv.poly([(cx, cy)] + arc((cx, cy), h, a0, a0 + 90), "#ffffff")
    cv.text(S / 2, 16, lab)
    return cv.svg("square of side %s with a quarter circle at each corner, middle part shaded" % lab)


def leaf_fig(lab, S=110):
    cv = Canvas()
    cv.poly([(0, 0), (S, 0), (S, -S), (0, -S)], "#ffffff")
    leaf = arc((0, 0), S, 0, 90) + arc((S, -S), S, 180, 270)[1:-1]
    cv.poly(leaf, SHADE)
    cv.text(S / 2, 16, lab)
    return cv.svg("square of side %s with two quarter circles from opposite corners, the overlap shaded" % lab)


def track_fig(Ltxt, Dtxt, L=150, R=48):
    cv = Canvas()
    pts = [(0, 0), (L, 0)] + arc((L, -R), R, -90, 90)[1:] + [(0, -2 * R)] + arc((0, -R), R, 90, 270)[1:-1]
    cv.poly(pts, FILL)
    cv.line((L, 0), (L, -2 * R), dashed=True, sw=1.8)
    cv.line((0, 0), (0, -2 * R), dashed=True, sw=1.8)
    cv.text(L / 2, -2 * R - 14, Ltxt)
    cv.text(L - tw(Dtxt, 16) / 2 - 10, -R, Dtxt)
    return cv.svg("running track: two straight sides of %s and two semicircular ends of diameter %s" % (Ltxt, Dtxt))


def window_fig(wtxt, htxt, W=110, H=80):
    cv = Canvas()
    R = W / 2
    pts = [(0, 0), (W, 0), (W, -H)] + arc((R, -H), R, 0, 180)[1:-1] + [(0, -H)]
    cv.poly(pts, FILL)
    cv.line((0, -H), (W, -H), dashed=True, sw=1.8)
    cv.text(W / 2, 16, wtxt)
    cv.text(W + 8, -H / 2, htxt, anchor="start")
    return cv.svg("rectangle %s wide and %s tall with a semicircle on top" % (wtxt, htxt))


def ring_fig(Rtxt, rtxt, R=84, r=44):
    cv = Canvas()
    cv.circle((0, 0), R, fill=SHADE)
    cv.circle((0, 0), r, fill="#ffffff")
    cv.dot((0, 0))
    cv.line((0, 0), (R, 0), sw=2.2)
    cv.text(R + 8, 0, Rtxt, anchor="start")
    cv.line((0, 0), pol(r, 125), sw=2.2)
    cv.text(-20, 13, rtxt, fs=15)
    return cv.svg("shaded ring between two circles with the same centre, radii %s and %s" % (Rtxt, rtxt))


def rect_semi_fig(wtxt, htxt, R=60):
    cv = Canvas()
    W = 2 * R
    cv.poly([(0, 0), (W, 0), (W, -R), (0, -R)], SHADE)
    cv.poly(arc((R, 0), R, 0, 180), "#ffffff")
    cv.text(R, 16, wtxt)
    cv.text(W + 8, -R / 2, htxt, anchor="start")
    return cv.svg("rectangle %s by %s with a semicircle cut out of it, the rest shaded" % (wtxt, htxt))


def sq_semis_fig(lab, S=90):
    cv = Canvas()
    h = S / 2
    pts = [(0, 0), (S, 0)] + arc((S, -h), h, -90, 90)[1:] + [(0, -S)] + arc((0, -h), h, 90, 270)[1:-1]
    cv.poly(pts, FILL)
    cv.line((0, 0), (0, -S), dashed=True, sw=1.8)
    cv.line((S, 0), (S, -S), dashed=True, sw=1.8)
    cv.text(S / 2, 16, lab)
    return cv.svg("square of side %s with a semicircle on the left side and on the right side" % lab)


def three_semis_fig(lab, R=84):
    cv = Canvas()
    cv.poly(arc((0, 0), R, 0, 180, 72), SHADE)
    h = R / 2
    cv.poly(arc((-h, 0), h, 0, 180), "#ffffff")
    cv.poly(arc((h, 0), h, 0, 180), "#ffffff")
    cv.text(0, 16, lab)
    return cv.svg("large semicircle with two small semicircles cut out along its diameter %s, the rest shaded" % lab)


def three_quarter_fig(lab, r=66):
    cv = Canvas()
    cv.poly([(0, 0)] + arc((0, 0), r, 90, 360), FILL)
    cv.dot((0, 0))
    cv.text(r / 2 + 6, -14, lab)
    return cv.svg("three-quarter circle with radius %s" % lab)


# ------------------------------------------------------------ bar models
def bar_svg(rows, spans, label, unit=38, right=None):
    """rows: [(name, n_units, n_shaded)]; spans: [(row, u0, u1, text, 'top'|'bot')]; right: text for a brace on the right."""
    s = []
    name_w = max(tw(r[0], 15) for r in rows) + 12 if any(r[0] for r in rows) else 0
    x0 = name_w + 4
    bh, gap = 28, 48
    top = 30
    maxn = max(r[1] for r in rows)
    for i, (name, n, k) in enumerate(rows):
        y = top + i * gap
        if name:
            s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                     % (x0 - 8, y + bh / 2 + 5, INK, name))
        for j in range(n):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x0 + j * unit, y, unit, bh, SHADE if j < k else FILL, LINE))
    for (ri, u0, u1, t, side) in spans:
        y = top + ri * gap
        xa, xb = x0 + u0 * unit + 2, x0 + u1 * unit - 2
        yy = y - 8 if side == "top" else y + bh + 8
        tick = 6 if side == "top" else -6
        s.append("<path d='M%.1f %.1f V%.1f H%.1f V%.1f' fill='none' stroke='%s' stroke-width='1.6'/>"
                 % (xa, yy + tick, yy, xb, yy + tick, INK))
        ty = yy - 6 if side == "top" else yy + 17
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % ((xa + xb) / 2, ty, INK, t))
    W = x0 + maxn * unit
    H = top + (len(rows) - 1) * gap + bh
    if right:
        bx = W + 10
        s.append("<path d='M%.1f %.1f H%.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='1.6'/>"
                 % (bx - 6, top, bx, H, bx - 6, INK))
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s'>%s</text>"
                 % (bx + 6, (top + H) / 2 + 5, INK, right))
        W = bx + 6 + tw(right, 15) + 4
    if any(sp[4] == "bot" and sp[0] == len(rows) - 1 for sp in spans):
        H += 30
    return svg_wrap(int(math.ceil(W + 6)), int(math.ceil(H + 6)), "".join(s), label)


# ============================================================ set 1
def circ_wrong_d(d, P, u):
    return [U(P * d / 2, u), U(2 * P * d, u), U(P * (d / 2) ** 2, u)]


def set_circumference():
    its = []
    its.append(mcq("What is the red line called?" + fig(part_fig("radius")), "radius",
                   ["diameter", "circumference", "centre"],
                   "It goes from the centre to the edge of the circle, so it is a <b>radius</b>."))
    its.append(mcq("What is the red curve all the way round this circle called?" + fig(part_fig("circumference")),
                   "circumference", ["radius", "diameter", "area"],
                   "The distance all the way round a circle is its <b>circumference</b>. It is the perimeter of the circle."))
    its.append(mcq("Which of these gives the circumference of a circle with radius r?", "2 × π × r",
                   ["π × r × r", "π × r", "2 × r"],
                   "The diameter is 2 × r, and circumference = π × diameter, so C = <b>2 × π × r</b>. π × r × r is the area."))
    its.append(mcq("A circle has a radius of 8 cm. What is its diameter?", "16 cm", ["4 cm", "64 cm", "25.12 cm"],
                   "The diameter is 2 radii: 2 × 8 = <b>16 cm</b>. 8 × 8 = 64 is not the diameter."))
    its.append(mcq("What is the radius of this circle?" + fig(len_fig("18 cm", "diameter")), "9 cm",
                   ["18 cm", "36 cm", "56.52 cm"],
                   "The line goes across the circle through the centre, so 18 cm is the diameter. "
                   "Radius = 18 ÷ 2 = <b>9 cm</b>."))
    its.append(mcq("A circle has a diameter of 25 cm. What is its radius?", "12.5 cm", ["50 cm", "25 cm", "5 cm"],
                   "Radius = diameter ÷ 2 = 25 ÷ 2 = <b>12.5 cm</b>."))
    plan = [("d", 10, "cm", P314, True), ("r", 5, "m", P314, False), ("d", 12, "m", P314, False),
            ("r", 15, "cm", P314, False), ("d", F(5, 2), "m", P314, False),
            ("d", 14, "cm", P227, True), ("r", 21, "cm", P227, False), ("d", 35, "m", P227, False),
            ("r", F(7, 2), "cm", P227, False)]
    for kind, x, u, P, f in plan:
        x = F(x)
        d = x if kind == "d" else 2 * x
        tk = T314 if P == P314 else T227
        name = "diameter" if kind == "d" else "radius"
        if f:
            q = "Find the circumference of this circle." + tk + fig(len_fig(U(x, u), name))
        else:
            q = "A circle has a %s of %s. Find its circumference.%s" % (name, U(x, u), tk)
        c = P * d
        if kind == "d":
            wr = circ_wrong_d(d, P, u)
            if d.denominator != 1:                  # pi + d: added instead of multiplied
                wr[2] = U(P + d, u)
            e = "C = π × d = %s × %s = <b>%s</b>." % (PI_E[P], N(d), U(c, u))
        else:
            wr = [U(P * x, u), U(4 * P * x, u), U(P * x * x, u)]
            e = ("d = 2 × %s = %s %s. C = π × d = %s × %s = <b>%s</b>. π × %s alone gives only half the circumference."
                 % (N(x), N(d), u, PI_E[P], N(d), U(c, u), N(x)))
        its.append(mcq(q, U(c, u), wr, e))
    r = F(36, 10)
    c = 2 * P314 * r
    its.append(mcq("A circle has a radius of 3.6 cm. Find its circumference, correct to 1 decimal place." + T314,
                   U(c, "cm", 1), [U(P314 * r, "cm", 1), U(4 * P314 * r, "cm", 1), U(P314 * r * r, "cm", 1)],
                   "d = 2 × 3.6 = 7.2 cm. C = 3.14 × 7.2 = %s ≈ <b>%s</b>." % (N(c), U(c, "cm", 1))))
    its.append(mcq("The circumference of a circle is 62.8 cm. Find its diameter." + T314, "20 cm",
                   ["10 cm", "31.4 cm", "197.192 cm"],
                   "C = π × d, so d = C ÷ π = 62.8 ÷ 3.14 = <b>20 cm</b>. Check: 3.14 × 20 = 62.8."))
    assert P314 * 20 == F(628, 10) and F(628, 10) * P314 == F("197.192")
    its.append(mcq("The circumference of a circle is 88 cm. Find its radius." + T227, "14 cm",
                   ["28 cm", "44 cm", "7 cm"],
                   "d = C ÷ π = 88 ÷ " + FR(22, 7) + " = 88 × " + FR(7, 22) + " = 28 cm. Radius = 28 ÷ 2 = <b>14 cm</b>."))
    assert 88 / P227 == 28
    its.append(mcq("The circumference of a circle is 132 m. Find its diameter." + T227, "42 m",
                   ["21 m", "66 m", "84 m"],
                   "d = C ÷ π = 132 × " + FR(7, 22) + " = <b>42 m</b>. 21 m is the radius."))
    assert 132 / P227 == 42
    its.append(mcq("Circle A has a radius of 6 cm. Circle B has a diameter of 10 cm. Which circle has the longer circumference?",
                   "Circle A", ["Circle B", "They are the same", "You cannot tell"],
                   "Circle A has a diameter of 2 × 6 = 12 cm, which is more than 10 cm. "
                   "The bigger the diameter, the longer the circumference. <b>Circle A</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Radius, diameter and circumference", "items": its}


# ============================================================ set 2
def set_area():
    its = []
    its.append(mcq("Which of these gives the area of a circle with radius r?", "π × r × r",
                   ["π × r × 2", "2 × π × r", "π × d × d"],
                   "Area = π × r × r (πr²). r² means r × r, <b>not</b> r × 2. 2 × π × r is the circumference."))
    its.append(mcq("The radius of a circle is given in cm. In which unit is its area?", "cm²", ["cm", "cm³", "m"],
                   "Area counts squares, so it is in square units: <b>cm²</b>. The circumference is a length, in cm."))
    plan = [(10, "cm", P314, False), (5, "m", P314, False), (8, "cm", P314, True), (3, "cm", P314, False),
            (9, "cm", P314, True), (20, "cm", P314, False), (F(3, 2), "m", P314, False),
            (7, "cm", P227, True), (14, "m", P227, False), (21, "cm", P227, False), (F(7, 2), "cm", P227, False),
            (35, "cm", P227, False)]
    for r, u, P, f in plan:
        r = F(r)
        tk = T314 if P == P314 else T227
        if f:
            q = "Find the area of this circle." + tk + fig(len_fig(U(r, u), "radius"))
        else:
            q = "A circle has a radius of %s. Find its area.%s" % (U(r, u), tk)
        a = P * r * r
        wr = [U(P * r * 2, u + "²"), U(P * (2 * r) ** 2, u + "²"), U(P * r, u + "²")]
        its.append(mcq(q, U(a, u + "²"), wr,
                       "A = π × r × r = %s × %s × %s = <b>%s</b>. Do not work out r × 2 instead of r × r."
                       % (PI_E[P], N(r), N(r), U(a, u + "²"))))
    for d, u, P, f in [(20, "cm", P314, True), (12, "m", P314, False), (56, "cm", P227, True)]:
        d = F(d)
        r = d / 2
        tk = T314 if P == P314 else T227
        if f:
            q = "Find the area of this circle." + tk + fig(len_fig(U(d, u), "diameter"))
        else:
            q = "A circle has a diameter of %s. Find its area.%s" % (U(d, u), tk)
        a = P * r * r
        wr = [U(P * d * d, u + "²"), U(P * d, u + "²"), U(P * r, u + "²")]
        its.append(mcq(q, U(a, u + "²"), wr,
                       "First find the radius: %s ÷ 2 = %s %s. A = %s × %s × %s = <b>%s</b>. "
                       "Using the diameter as the radius gives 4 times too much."
                       % (N(d), N(r), u, PI_E[P], N(r), N(r), U(a, u + "²"))))
    its.append(mcq("The area of a circle is 154 cm². Find its radius." + T227, "7 cm", ["14 cm", "49 cm", "24.5 cm"],
                   "r × r = 154 ÷ " + FR(22, 7) + " = 154 × " + FR(7, 22) + " = 49. 7 × 7 = 49, so r = <b>7 cm</b>."))
    assert 154 / P227 == 49 and 154 / (2 * P227) == F("24.5")
    its.append(mcq("The area of a circle is 314 cm². Find its diameter." + T314, "20 cm", ["10 cm", "100 cm", "50 cm"],
                   "r × r = 314 ÷ 3.14 = 100. 10 × 10 = 100, so r = 10 cm. Diameter = 2 × 10 = <b>20 cm</b>."))
    r = F(45, 10)
    a = P314 * r * r
    its.append(mcq("A circle has a radius of 4.5 cm. Find its area, correct to 1 decimal place." + T314,
                   U(a, "cm²", 1), [U(P314 * 81, "cm²", 1), U(2 * P314 * r, "cm²", 1), U(P314 * r, "cm²", 1)],
                   "r × r = 4.5 × 4.5 = 20.25. A = 3.14 × 20.25 = %s ≈ <b>%s</b>." % (N(a), U(a, "cm²", 1))))
    assert len(its) == 20, len(its)
    return {"title": "Area of circles", "items": its}


# ============================================================ set 3
def set_parts_of_circles():
    its = []
    its.append(mcq("What makes up the perimeter of a semicircle?", "the curved edge and the diameter",
                   ["the curved edge only", "the diameter only", "the curved edge and the radius"],
                   "Go all the way round the semicircle: along the curved edge, then back along the straight edge. "
                   "The perimeter is <b>the curved edge and the diameter</b>."))
    its.append(mcq("What makes up the perimeter of a quarter circle?", "the curved edge and 2 radii",
                   ["the curved edge only", "the curved edge and 1 radius", "the curved edge and the diameter"],
                   "A quarter circle has one curved edge and two straight edges. Each straight edge is a radius, so the "
                   "perimeter is <b>the curved edge and 2 radii</b>."))
    # semicircle area
    for x, kind, u, P, f in [(20, "d", "cm", P314, True), (14, "r", "cm", P227, False), (7, "d", "m", P227, False)]:
        x = F(x)
        r = x / 2 if kind == "d" else x
        tk = T314 if P == P314 else T227
        name = "diameter" if kind == "d" else "radius"
        if f:
            q = "Find the area of this semicircle." + tk + fig(semi_fig(U(x, u)))
        else:
            q = "A semicircle has a %s of %s. Find its area.%s" % (name, U(x, u), tk)
        a = P * r * r / 2
        wr = [U(P * r * r, u + "²"), U(P * (2 * r) ** 2 / 2, u + "²"), U(P * r, u + "²")]
        st = "" if kind == "r" else "r = %s ÷ 2 = %s %s. " % (N(x), N(r), u)
        its.append(mcq(q, U(a, u + "²"), wr,
                       st + "Area of the whole circle = %s × %s × %s = %s. Half of it: %s ÷ 2 = <b>%s</b>."
                       % (PI_E[P], N(r), N(r), N(P * r * r), N(P * r * r), U(a, u + "²"))))
    # quarter circle area
    for r, u, P, f in [(10, "cm", P314, True), (28, "cm", P227, False), (6, "m", P314, False)]:
        r = F(r)
        tk = T314 if P == P314 else T227
        q = ("Find the area of this quarter circle." + tk + fig(quarter_fig(U(r, u)))) if f else \
            "A quarter circle has a radius of %s. Find its area.%s" % (U(r, u), tk)
        a = P * r * r / 4
        its.append(mcq(q, U(a, u + "²"), [U(P * r * r, u + "²"), U(P * r * r / 2, u + "²"), U(P * r / 2, u + "²")],
                       "Area of the whole circle = %s × %s × %s = %s. A quarter: %s ÷ 4 = <b>%s</b>."
                       % (PI_E[P], N(r), N(r), N(P * r * r), N(P * r * r), U(a, u + "²"))))
    # semicircle perimeter
    for x, kind, u, P, f in [(20, "d", "cm", P314, True), (7, "r", "cm", P227, False), (42, "d", "m", P227, False),
                             (5, "r", "cm", P314, True)]:
        x = F(x)
        d = x if kind == "d" else 2 * x
        tk = T314 if P == P314 else T227
        name = "diameter" if kind == "d" else "radius"
        if f:
            q = "Find the perimeter of this semicircle." + tk + fig(semi_fig(U(x, u), name))
        else:
            q = "A semicircle has a %s of %s. Find its perimeter.%s" % (name, U(x, u), tk)
        cur = P * d / 2
        st = "" if kind == "d" else "d = 2 × %s = %s %s. " % (N(x), N(d), u)
        its.append(mcq(q, U(cur + d, u), [U(cur, u), U(cur + d / 2, u), U(P * d, u)],
                       st + "Curved edge = %s × %s ÷ 2 = %s %s. Perimeter = %s + %s = <b>%s</b>. "
                       "Do not forget the straight edge." % (PI_E[P], N(d), N(cur), u, N(cur), N(d), U(cur + d, u))))
    # quarter perimeter
    for r, u, P, f in [(14, "cm", P227, True), (10, "m", P314, False), (21, "cm", P227, False), (8, "cm", P314, False)]:
        r = F(r)
        tk = T314 if P == P314 else T227
        q = ("Find the perimeter of this quarter circle." + tk + fig(quarter_fig(U(r, u)))) if f else \
            "A quarter circle has a radius of %s. Find its perimeter.%s" % (U(r, u), tk)
        cur = P * 2 * r / 4
        third = U(cur * 2 + 2 * r, u) if P == P314 else U(P * 2 * r, u)
        its.append(mcq(q, U(cur + 2 * r, u), [U(cur, u), U(cur + r, u), third],
                       "Curved edge = %s × %s ÷ 4 = %s %s. Add the 2 radii: %s + %s + %s = <b>%s</b>."
                       % (PI_E[P], N(2 * r), N(cur), u, N(cur), N(r), N(r), U(cur + 2 * r, u))))
    its.append(mcq("Find the length of the curved edge of a semicircle with a diameter of 14 cm." + T227, "22 cm",
                   ["36 cm", "44 cm", "77 cm"],
                   "Curved edge = half the circumference = " + FR(22, 7) + " × 14 ÷ 2 = <b>22 cm</b>. "
                   "Only the curved edge is asked for, so do not add the diameter."))
    its.append(mcq("Find the area of this three-quarter circle." + T227 + fig(three_quarter_fig("14 cm")), "462 cm²",
                   ["616 cm²", "154 cm²", "308 cm²"],
                   "Whole circle = " + FR(22, 7) + " × 14 × 14 = 616 cm². Three quarters: 616 ÷ 4 × 3 = <b>462 cm²</b>."))
    assert P227 * 196 * 3 / 4 == 462
    its.append(mcq("A three-quarter circle has a radius of 7 cm. Find its perimeter." + T227, "47 cm",
                   ["33 cm", "40 cm", "44 cm"],
                   "Curved edge = " + FR(3, 4) + " of the circumference = " + FR(3, 4) + " × 44 = 33 cm. "
                   "Add the 2 radii: 33 + 7 + 7 = <b>47 cm</b>."))
    assert P227 * 14 * F(3, 4) == 33
    its.append(mcq("A semicircle and a quarter circle both have a radius of 10 cm. How much greater is the area of the semicircle?"
                   + T314, "78.5 cm²", ["157 cm²", "235.5 cm²", "15.7 cm²"],
                   "Semicircle = 314 ÷ 2 = 157 cm². Quarter circle = 314 ÷ 4 = 78.5 cm². "
                   "Difference = 157 − 78.5 = <b>78.5 cm²</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Semicircles and quarter circles", "items": its}


# ============================================================ set 4
def set_composite():
    its = []
    its.append(mcq("The figure is made of a square of side 10 cm and a quarter circle. Find the area of the shaded part."
                   + T314 + fig(sq_quarter_fig("10 cm")), "21.5 cm²", ["78.5 cm²", "84.3 cm²", "178.5 cm²"],
                   "Square = 10 × 10 = 100 cm². Quarter circle = 3.14 × 10 × 10 ÷ 4 = 78.5 cm². "
                   "Shaded = 100 − 78.5 = <b>21.5 cm²</b>."))
    its.append(mcq("The figure is made of a square of side 10 cm and a quarter circle. Find the perimeter of the shaded part."
                   + T314 + fig(sq_quarter_fig("10 cm")), "35.7 cm", ["55.7 cm", "20 cm", "25.7 cm"],
                   "The shaded part has 2 sides of the square and the curved edge. Curved edge = 3.14 × 20 ÷ 4 = 15.7 cm. "
                   "Perimeter = 10 + 10 + 15.7 = <b>35.7 cm</b>."))
    its.append(mcq("A circle just fits inside a square of side 14 cm. Find the area of the shaded part." + T227
                   + fig(circle_in_square_fig("14 cm")), "42 cm²", ["154 cm²", "152 cm²", "350 cm²"],
                   "The diameter of the circle is 14 cm, so r = 7 cm. Circle = " + FR(22, 7) + " × 7 × 7 = 154 cm². "
                   "Square = 14 × 14 = 196 cm². Shaded = 196 − 154 = <b>42 cm²</b>."))
    its.append(mcq("Four equal quarter circles are drawn at the corners of a square of side 20 cm. Find the area of the shaded part."
                   + T314 + fig(four_quarters_fig("20 cm")), "86 cm²", ["314 cm²", "321.5 cm²", "714 cm²"],
                   "Each quarter circle has radius 20 ÷ 2 = 10 cm. 4 quarters make 1 whole circle: 3.14 × 10 × 10 = 314 cm². "
                   "Shaded = 400 − 314 = <b>86 cm²</b>."))
    its.append(mcq("Four equal quarter circles are drawn at the corners of a square of side 20 cm. Find the perimeter of the shaded part."
                   + T314 + fig(four_quarters_fig("20 cm")), "62.8 cm", ["31.4 cm", "80 cm", "142.8 cm"],
                   "The shaded part is bounded by 4 curved edges only. 4 quarter circles of radius 10 cm make the "
                   "circumference of one circle: 3.14 × 20 = <b>62.8 cm</b>."))
    its.append(mcq("Two quarter circles are drawn inside a square of side 10 cm. Find the area of the shaded part."
                   + T314 + fig(leaf_fig("10 cm")), "57 cm²", ["157 cm²", "43 cm²", "78.5 cm²"],
                   "Each quarter circle = 78.5 cm². Two quarter circles = 157 cm², which covers the shaded part twice and "
                   "the rest of the square once. Shaded = 157 − 100 = <b>57 cm²</b>."))
    its.append(mcq("Two quarter circles are drawn inside a square of side 10 cm. Find the perimeter of the shaded part."
                   + T314 + fig(leaf_fig("10 cm")), "31.4 cm", ["15.7 cm", "51.4 cm", "71.4 cm"],
                   "The shaded part is bounded by 2 curved edges. Each = 3.14 × 20 ÷ 4 = 15.7 cm. "
                   "Perimeter = 15.7 + 15.7 = <b>31.4 cm</b>."))
    its.append(mcq("A running track has 2 straight sides of 100 m and 2 semicircular ends of diameter 70 m. "
                   "Find the perimeter of the track." + T227 + fig(track_fig("100 m", "70 m")), "420 m",
                   ["320 m", "640 m", "560 m"],
                   "The 2 semicircular ends make 1 whole circle: " + FR(22, 7) + " × 70 = 220 m. "
                   "Perimeter = 100 + 100 + 220 = <b>420 m</b>. The dashed lines are not part of the perimeter."))
    its.append(mcq("A running track has 2 straight sides of 100 m and 2 semicircular ends of diameter 70 m. "
                   "Find the area enclosed by the track." + T227 + fig(track_fig("100 m", "70 m")), "10" + NB + "850 m²",
                   ["22" + NB + "400 m²", "3850 m²", "14" + NB + "700 m²"],
                   "Rectangle = 100 × 70 = 7000 m². The 2 semicircles make 1 circle of radius 35 m: "
                   + FR(22, 7) + " × 35 × 35 = 3850 m². Total = 7000 + 3850 = <b>10" + NB + "850 m²</b>."))
    assert 7000 + P227 * 35 * 35 == 10850 and 7000 + P227 * 4900 == 22400
    its.append(mcq("A window is a rectangle 40 cm wide and 30 cm tall with a semicircle on top. Find the perimeter of the window."
                   + T314 + fig(window_fig("40 cm", "30 cm")), "162.8 cm", ["202.8 cm", "225.6 cm", "122.8 cm"],
                   "Curved edge = 3.14 × 40 ÷ 2 = 62.8 cm. Straight edges = 30 + 40 + 30 = 100 cm. "
                   "Perimeter = 62.8 + 100 = <b>162.8 cm</b>. The dashed line is inside the window, so do not count it."))
    its.append(mcq("A window is a rectangle 40 cm wide and 30 cm tall with a semicircle on top. Find the area of the window."
                   + T314 + fig(window_fig("40 cm", "30 cm")), "1828 cm²", ["2456 cm²", "3712 cm²", "1514 cm²"],
                   "Rectangle = 40 × 30 = 1200 cm². Semicircle: r = 20 cm, 3.14 × 20 × 20 ÷ 2 = 628 cm². "
                   "Total = 1200 + 628 = <b>1828 cm²</b>."))
    its.append(mcq("The figure shows two circles with the same centre. Their radii are 14 cm and 7 cm. "
                   "Find the area of the shaded ring." + T227 + fig(ring_fig("14 cm", "7 cm")), "462 cm²",
                   ["154 cm²", "770 cm²", "616 cm²"],
                   "Big circle = " + FR(22, 7) + " × 14 × 14 = 616 cm². Small circle = " + FR(22, 7)
                   + " × 7 × 7 = 154 cm². Ring = 616 − 154 = <b>462 cm²</b>. Do not subtract the radii first."))
    its.append(mcq("The figure shows two circles with the same centre. Their radii are 10 cm and 6 cm. "
                   "Find the area of the shaded ring." + T314 + fig(ring_fig("10 cm", "6 cm")), "200.96 cm²",
                   ["50.24 cm²", "427.04 cm²", "314 cm²"],
                   "Big circle = 3.14 × 10 × 10 = 314 cm². Small circle = 3.14 × 6 × 6 = 113.04 cm². "
                   "Ring = 314 − 113.04 = <b>200.96 cm²</b>."))
    assert P314 * 100 - P314 * 36 == F("200.96") and P314 * 16 == F("50.24")
    its.append(mcq("The shaded ring is between two circles with the same centre, of radii 14 cm and 7 cm. "
                   "Find the total length of both curved edges of the ring." + T227, "132 cm",
                   ["88 cm", "44 cm", "462 cm"],
                   "Outer edge = " + FR(22, 7) + " × 28 = 88 cm. Inner edge = " + FR(22, 7) + " × 14 = 44 cm. "
                   "Total = 88 + 44 = <b>132 cm</b>."))
    its.append(mcq("A semicircle is cut out of a rectangle 28 cm by 14 cm. Find the area of the shaded part." + T227
                   + fig(rect_semi_fig("28 cm", "14 cm")), "84 cm²", ["308 cm²", "348 cm²", "700 cm²"],
                   "Rectangle = 28 × 14 = 392 cm². Semicircle: r = 14 cm, " + FR(22, 7) + " × 14 × 14 ÷ 2 = 308 cm². "
                   "Shaded = 392 − 308 = <b>84 cm²</b>."))
    its.append(mcq("The figure is made of a square of side 14 cm and 2 semicircles. Find the perimeter of the figure."
                   + T227 + fig(sq_semis_fig("14 cm")), "72 cm", ["100 cm", "116 cm", "50 cm"],
                   "Each semicircle has a curved edge of " + FR(22, 7) + " × 14 ÷ 2 = 22 cm. "
                   "Perimeter = 14 + 14 + 22 + 22 = <b>72 cm</b>. The dashed sides are inside the figure."))
    its.append(mcq("The figure is made of a square of side 14 cm and 2 semicircles. Find the area of the figure."
                   + T227 + fig(sq_semis_fig("14 cm")), "350 cm²", ["504 cm²", "812 cm²", "273 cm²"],
                   "Square = 14 × 14 = 196 cm². 2 semicircles of radius 7 cm make 1 circle: " + FR(22, 7)
                   + " × 7 × 7 = 154 cm². Total = 196 + 154 = <b>350 cm²</b>."))
    its.append(mcq("Two small semicircles are cut out of a big semicircle with a diameter of 28 cm. Find the area of the shaded part."
                   + T227 + fig(three_semis_fig("28 cm")), "154 cm²", ["308 cm²", "231 cm²", "462 cm²"],
                   "Big semicircle: r = 14 cm, " + FR(22, 7) + " × 14 × 14 ÷ 2 = 308 cm². Each small semicircle: r = 7 cm, "
                   + FR(22, 7) + " × 7 × 7 ÷ 2 = 77 cm². Shaded = 308 − 77 − 77 = <b>154 cm²</b>."))
    its.append(mcq("Two small semicircles are cut out of a big semicircle with a diameter of 28 cm. Find the perimeter of the shaded part."
                   + T227 + fig(three_semis_fig("28 cm")), "88 cm", ["116 cm", "44 cm", "66 cm"],
                   "The shaded part has 3 curved edges and no straight edges. Big curved edge = " + FR(22, 7)
                   + " × 28 ÷ 2 = 44 cm. Each small one = " + FR(22, 7) + " × 14 ÷ 2 = 22 cm. "
                   "Perimeter = 44 + 22 + 22 = <b>88 cm</b>."))
    its.append(mcq("A running track has 2 straight sides of 80 m and 2 semicircular ends of diameter 50 m. "
                   "Find the perimeter of the track." + T314 + fig(track_fig("80 m", "50 m")), "317 m",
                   ["237 m", "474 m", "417 m"],
                   "The 2 ends make 1 whole circle: 3.14 × 50 = 157 m. Perimeter = 80 + 80 + 157 = <b>317 m</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Composite figures: squares, tracks and rings", "items": its}


# ============================================================ set 5
def set_psle():
    its = []
    its.append(mcq("The wheel of Ahmad’s bicycle has a diameter of 70 cm. How far does the bicycle move when the wheel makes "
                   "1 complete turn?" + T227, "220 cm", ["110 cm", "440 cm", "3850 cm"],
                   "In 1 turn, the bicycle moves the circumference of the wheel. C = " + FR(22, 7) + " × 70 = <b>220 cm</b>."))
    its.append(mcq("The wheel of Mei Ling’s scooter has a diameter of 70 cm. How many metres does the scooter move when the wheel "
                   "makes 50 complete turns?" + T227, "110 m", ["11 m", "1100 m", "55 m"],
                   "1 turn = " + FR(22, 7) + " × 70 = 220 cm. 50 turns = 50 × 220 = 11" + NB + "000 cm. "
                   "11" + NB + "000 cm ÷ 100 = <b>110 m</b>."))
    its.append(mcq("The wheels of Hafiz’s bicycle have a radius of 35 cm. He cycles 440 m along East Coast Park. "
                   "How many complete turns does each wheel make?" + T227, "200", ["400", "2", "20"],
                   "d = 70 cm, so 1 turn = " + FR(22, 7) + " × 70 = 220 cm. 440 m = 44" + NB + "000 cm. "
                   "44" + NB + "000 ÷ 220 = <b>200</b> turns. Change m to cm before you divide."))
    its.append(mcq("A round table top has a diameter of 1.4 m. Find the area of the table top." + T227, "1.54 m²",
                   ["6.16 m²", "4.4 m²", "2.2 m²"],
                   "r = 1.4 ÷ 2 = 0.7 m. A = " + FR(22, 7) + " × 0.7 × 0.7 = <b>1.54 m²</b>."))
    assert P227 * F(49, 100) == F("1.54") and P227 * F(196, 100) == F("6.16")
    its.append(mcq("Ali used " + FR(2, 5) + " of a roll of ribbon to go round the edge of a round table with a diameter of 70 cm. "
                   "How long was the roll of ribbon at first?" + T227
                   + fig(bar_svg([("", 5, 2)], [(0, 0, 2, "220 cm", "top"), (0, 0, 5, "?", "bot")],
                                 "bar model: 5 units, 2 units used for the table")),
                   "550 cm", ["88 cm", "330 cm", "1100 cm"],
                   "Edge of the table = " + FR(22, 7) + " × 70 = 220 cm. 2 units = 220 cm, 1 unit = 110 cm. "
                   "5 units = 5 × 110 = <b>550 cm</b>."))
    its.append(mcq("A wire 132 cm long is cut into 2 pieces. The longer piece is twice as long as the shorter piece. "
                   "The longer piece is bent to form a circle. Find the radius of the circle." + T227
                   + fig(bar_svg([("Longer", 2, 2), ("Shorter", 1, 0)], [], "bar model: longer piece 2 units, "
                                 "shorter piece 1 unit, total 132 cm", right="132 cm")),
                   "14 cm", ["28 cm", "7 cm", "21 cm"],
                   "3 units = 132 cm, 1 unit = 44 cm. Longer piece = 2 × 44 = 88 cm = circumference. "
                   "d = 88 ÷ " + FR(22, 7) + " = 28 cm, so r = 28 ÷ 2 = <b>14 cm</b>."))
    its.append(mcq("A circular pond has a radius of 14 m. A path 7 m wide goes round the pond. Find the area of the path." + T227,
                   "770 m²", ["154 m²", "1386 m²", "2002 m²"],
                   "Outer radius = 14 + 7 = 21 m. Big circle = " + FR(22, 7) + " × 21 × 21 = 1386 m². Pond = "
                   + FR(22, 7) + " × 14 × 14 = 616 m². Path = 1386 − 616 = <b>770 m²</b>."))
    its.append(mcq("Mr Tan puts a fence round a circular garden with a diameter of 21 m. The fencing costs $15 per metre. "
                   "How much does the fencing cost?" + T227, "$990", ["$495", "$1980", "$315"],
                   "Length of fence = " + FR(22, 7) + " × 21 = 66 m. Cost = 66 × $15 = <b>$990</b>."))
    its.append(mcq("A semicircular lawn has a diameter of 28 m. One packet of grass seed covers 50 m². "
                   "How many packets does Mrs Lim need to cover the whole lawn?" + T227, "7", ["6", "13", "25"],
                   "r = 14 m. Area = " + FR(22, 7) + " × 14 × 14 ÷ 2 = 308 m². 308 ÷ 50 = 6.16, so 6 packets are not "
                   "enough. She needs <b>7</b> packets."))
    its.append(mcq("A running track has 2 straight sides of 85 m and 2 semicircular ends of diameter 63 m. "
                   "Jun Jie runs 3 rounds of the track. How far does he run?" + T227 + fig(track_fig("85 m", "63 m")),
                   "1104 m", ["849 m", "1698 m", "1482 m"],
                   "The 2 ends make 1 circle: " + FR(22, 7) + " × 63 = 198 m. 1 round = 85 + 85 + 198 = 368 m. "
                   "3 rounds = 3 × 368 = <b>1104 m</b>."))
    its.append(mcq("Mdm Wong cuts the biggest possible circle from a square piece of cloth of side 42 cm. "
                   "What area of cloth is left?" + T227, "378 cm²", ["1386 cm²", "1632 cm²", "3150 cm²"],
                   "The diameter of the circle is 42 cm, so r = 21 cm. Circle = " + FR(22, 7) + " × 21 × 21 = 1386 cm². "
                   "Square = 42 × 42 = 1764 cm². Left = 1764 − 1386 = <b>378 cm²</b>."))
    its.append(mcq("Two equal circles, as big as possible, are cut from a rectangular card 28 cm by 14 cm. "
                   "What area of card is left?" + T227, "84 cm²", ["238 cm²", "308 cm²", "304 cm²"],
                   "Each circle has a diameter of 14 cm, so r = 7 cm. 1 circle = " + FR(22, 7) + " × 7 × 7 = 154 cm². "
                   "Card = 28 × 14 = 392 cm². Left = 392 − 154 − 154 = <b>84 cm²</b>."))
    its.append(mcq("The minute hand of the school hall clock is 14 cm long. How far does its tip move from 7.00 am to 7.45 am?"
                   + T227, "66 cm", ["88 cm", "44 cm", "462 cm"],
                   "In 1 hour, the tip goes round once: " + FR(22, 7) + " × 28 = 88 cm. 45 min is " + FR(3, 4)
                   + " of an hour: " + FR(3, 4) + " × 88 = <b>66 cm</b>."))
    its.append(mcq("Siti cuts a round cake with a diameter of 20 cm into 4 equal pieces. Find the perimeter of the top of one piece."
                   + T314, "35.7 cm", ["15.7 cm", "25.7 cm", "55.7 cm"],
                   "Each piece is a quarter circle with radius 10 cm. Curved edge = 3.14 × 20 ÷ 4 = 15.7 cm. "
                   "Perimeter = 15.7 + 10 + 10 = <b>35.7 cm</b>."))
    its.append(mcq("The radius of Circle A is 3 times the radius of Circle B. The area of Circle B is 154 cm². "
                   "Find the area of Circle A.", "1386 cm²", ["462 cm²", "924 cm²", "4158 cm²"],
                   "Area uses r × r. If the radius is 3 times as long, the area is 3 × 3 = 9 times as big. "
                   "9 × 154 = <b>1386 cm²</b>, not 3 × 154."))
    its.append(mcq("A wire 72 cm long is bent to form a semicircle, with no wire left over. Find the diameter of the semicircle."
                   + T227, "28 cm", ["14 cm", "36 cm", "18 cm"],
                   "Let the diameter be 7 units. Curved edge = " + FR(22, 7) + " × 7 units ÷ 2 = 11 units. "
                   "Perimeter = 11 + 7 = 18 units = 72 cm, so 1 unit = 4 cm. Diameter = 7 × 4 = <b>28 cm</b>."))
    its.append(mcq("Mr Rahman’s rectangular garden is 20 m by 14 m. A semicircular flower bed with a diameter of 14 m is along "
                   "one short side. The rest of the garden is grass. Find the area of the grass." + T227, "203 m²",
                   ["126 m²", "258 m²", "357 m²"],
                   "Garden = 20 × 14 = 280 m². Flower bed: r = 7 m, " + FR(22, 7) + " × 7 × 7 ÷ 2 = 77 m². "
                   "Grass = 280 − 77 = <b>203 m²</b>."))
    its.append(mcq("Priya used " + FR(2, 7) + " of her ribbon to go round the edge of a circular photo frame with a diameter of 21 cm. "
                   "She used half of the remaining ribbon for a card. How much ribbon did she have left?" + T227
                   + fig(bar_svg([("", 7, 2)], [(0, 0, 2, "66 cm", "top"), (0, 2, 7, "remainder", "bot")],
                                 "bar model: 7 units, 2 units used for the frame")),
                   "82.5 cm", ["165 cm", "231 cm", "33 cm"],
                   "Frame = " + FR(22, 7) + " × 21 = 66 cm = 2 units, so 1 unit = 33 cm. Remainder = 5 units = 165 cm. "
                   "Half of it is left: 165 ÷ 2 = <b>82.5 cm</b>."))
    its.append(mcq("A hawker centre has 12 round tables. Each table top has a diameter of 1 m. Find the total area of the 12 table tops."
                   + T314, "9.42 m²", ["18.84 m²", "37.68 m²", "0.785 m²"],
                   "r = 0.5 m. 1 table top = 3.14 × 0.5 × 0.5 = 0.785 m². 12 table tops = 12 × 0.785 = <b>9.42 m²</b>."))
    assert 12 * P314 * F(1, 4) == F("9.42")
    n = F(100000) / (P227 * 56)
    assert int(n) == 568
    its.append(mcq("The wheels of Kumar’s bicycle have a diameter of 56 cm. How many complete turns does each wheel make when he "
                   "cycles 1 km?" + T227, "568", ["569", "284", "1786"],
                   "1 turn = " + FR(22, 7) + " × 56 = 176 cm. 1 km = 100" + NB + "000 cm. 100" + NB + "000 ÷ 176 = 568.18…, "
                   "so each wheel makes <b>568</b> complete turns."))
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style word problems", "items": its}


# ============================================================ lesson
def parts_lesson_svg():
    r = 86
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.line((-r, 0), (r, 0), sw=3, col=BLUE)
    cv.line((0, 0), pol(r, 60), sw=3, col=RED)
    cv.dot((0, 0))
    cv.text(0, 16, "centre", 15)
    cv.text(-40, -14, "diameter", 15, col=BLUE)
    cv.text(r + 10, -46, "radius", 15, "start", RED)
    cv.text(r + 10, 50, "circumference", 15, "start", LINE)
    cv.line(pol(r * 0.8, 60), (r + 6, -46), sw=1.5, col=RED)
    cv.line(pol(r, -35), (r + 6, 50), sw=1.5, col=LINE)
    return cv.svg("circle with its centre, a radius, a diameter and the circumference labelled")


def semi_lesson_svg():
    r = 70
    cv = Canvas()
    cv.poly(arc((0, 0), r, 0, 180), FILL)
    cv.pline(arc((0, 0), r, 0, 180), 5, RED)
    cv.pline([(-r, 0), (r, 0)], 5, BLUE)
    cv.text(0, 18, "diameter", 15, col=BLUE)
    cv.text(0, -r - 14, "curved edge", 15, col=RED)
    cv2 = Canvas()
    R = 80
    cv2.poly([(0, 0)] + arc((0, 0), R, 0, 90), FILL)
    cv2.pline(arc((0, 0), R, 0, 90), 5, RED)
    cv2.pline([(0, -R), (0, 0), (R, 0)], 5, BLUE)
    cv2.text(R / 2, 16, "radius", 15, col=BLUE)
    cv2.text(-8, -R / 2, "radius", 15, "end", BLUE)
    cv2.text(R * 0.72 + 8, -R * 0.72 - 14, "curved edge", 15, "start", RED)
    a = cv.svg("semicircle")
    b = cv2.svg("quarter circle")
    # put the two side by side in one SVG
    wa, ha = [int(x) for x in re.search(r"viewBox='0 0 (\d+) (\d+)'", a).groups()]
    wb, hb = [int(x) for x in re.search(r"viewBox='0 0 (\d+) (\d+)'", b).groups()]
    ia = re.search(r"<g font-family='[^']+'>(.*)</g></svg>", a).group(1)
    ib = re.search(r"<g font-family='[^']+'>(.*)</g></svg>", b).group(1)
    H = max(ha, hb)
    body = ("<g transform='translate(0,%d)'>%s</g><g transform='translate(%d,%d)'>%s</g>"
            % (H - ha, ia, wa + 30, H - hb, ib))
    return svg_wrap(wa + 30 + wb, H, body, "perimeter of a semicircle and of a quarter circle: the curved edge in red "
                    "and the straight edges in blue")


def body_html():
    return (
        "<h2>Circumference: the distance round a circle</h2>"
        "<p>The <b>radius</b> (r) goes from the centre to the edge. The <b>diameter</b> (d) goes across through the centre, "
        "so d = 2 × r. The <b>circumference</b> is the distance all the way round.</p>"
        "<figure class='sn-fig'>" + parts_lesson_svg() +
        "<figcaption>A diameter is 2 radii: d = 2 × r and r = d ÷ 2.</figcaption></figure>"
        "<p>Circumference = π × d = 2 × π × r. The question tells you which value of π to use: "
        "<b>3.14</b> or <b>" + FR(22, 7) + "</b>. Use " + FR(22, 7) + " when the radius or diameter is a multiple of 7.</p>"
        + ex("Example 1", "A circle has a diameter of 14 cm. Find its circumference. Take π = " + FR(22, 7) + ".",
             FR(22, 7) + " × 14 = 44", "44 cm")
        + "<h2>Area: π × r × r</h2>"
        "<p>Area of a circle = π × r × r (written πr²). Always use the <b>radius</b>. "
        "Area is in square units, such as cm² or m².</p>"
        + ex("Example 2", "A circle has a diameter of 20 cm. Find its area. Take π = 3.14.",
             "r = 20 ÷ 2 = 10 cm. Area = 3.14 × 10 × 10 = 314", "314 cm²")
        + "<h2>Semicircles and quarter circles</h2>"
        "<p>A semicircle is half a circle. A quarter circle is a quarter of a circle. "
        "For the area, find the area of the whole circle, then halve it or divide it by 4. "
        "For the <b>perimeter</b>, add the curved edge <b>and</b> the straight edges.</p>"
        "<figure class='sn-fig'>" + semi_lesson_svg() +
        "<figcaption>Semicircle: curved edge + diameter. Quarter circle: curved edge + 2 radii.</figcaption></figure>"
        + ex("Example 3", "Find the perimeter of a semicircle with a diameter of 14 cm. Take π = " + FR(22, 7) + ".",
             "Curved edge = " + FR(22, 7) + " × 14 ÷ 2 = 22 cm. Perimeter = 22 + 14 = 36", "36 cm")
        + "<h2>Composite figures</h2>"
        "<p>Split the figure into shapes you know: squares, rectangles, circles, semicircles and quarter circles. "
        "For a shaded area, <b>add</b> the parts or <b>subtract</b> the part that is cut out. "
        "For a perimeter, trace the outline and add only the edges on the outside.</p>"
        "<figure class='sn-fig'>" + track_fig("100 m", "70 m") +
        "<figcaption>A running track: 2 straight sides and 2 semicircles, which make 1 whole circle.</figcaption></figure>"
        + ex("Example 4", "Find the perimeter of the track above. Take π = " + FR(22, 7) + ".",
             "2 semicircles = 1 circle: " + FR(22, 7) + " × 70 = 220 m. Perimeter = 100 + 100 + 220 = 420", "420 m")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the diameter as the radius", "Halve the diameter first: r = d ÷ 2"],
            ["Working out r × 2 for r²", "r² means r × r: 5² = 25, not 10"],
            ["Leaving out the straight edges of a semicircle", "Perimeter = curved edge + diameter"],
            ["Writing cm for an area", "Area is in cm² or m²; length is in cm or m"],
            ["Using the wrong value of π", "Use the value the question gives: 3.14 or " + FR(22, 7)],
        ])
    )


FAQ = [
    {"q": "Are area and circumference of circles in the PSLE?",
     "a": "Yes. Circles are part of Measurement and Geometry in the P6 MOE syllabus, and PSLE papers often ask for the "
          "area and perimeter of figures made of circles, semicircles and quarter circles."},
    {"q": "Should my child use π = 3.14 or 22/7?",
     "a": "Use the value the question gives. PSLE questions say “Take π = 3.14” or “Take π = 22/7”; 22/7 makes the working "
          "easier when the radius or diameter is a multiple of 7."},
    {"q": "What is the most common mistake with circles in P6?",
     "a": "Using the diameter in place of the radius in π × r × r. Another common mistake is leaving out the straight "
          "edges when finding the perimeter of a semicircle or quarter circle."},
    {"q": "How do I find the perimeter of a semicircle?",
     "a": "Add the curved edge and the diameter. The curved edge is half the circumference: π × d ÷ 2."},
]


def mark_large(u, pattern):
    """Tag wide pictures (bar models, tracks) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    r = random.Random(66807)
    sets = [set_circumference(), set_area(), set_parts_of_circles(), set_composite(), set_psle()]
    balance(sets, r)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "area-and-circumference-of-circles", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Area and Circumference of Circles",
        "seo_title": "P6 Area and Circumference of Circles Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE)",
        "short_title": "Area and circumference of circles",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 6: Area and Volume",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Area and circumference of circle; area and perimeter of semicircle, quarter circle and composite figures",
        "meta_desc": "P6 circles practice for the PSLE: circumference, area, semicircles, quarter circles and composite figures. 100 questions with answers.",
        "key_big": "Circumference = π × d. Area = π × r × r. Use the radius, not the diameter, for the area.",
        "key_sub": "Diameter 14 cm, π = 22/7: circumference = 22/7 × 14 = 44 cm; area = 22/7 × 7 × 7 = 154 cm².",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(bar model|running track)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
