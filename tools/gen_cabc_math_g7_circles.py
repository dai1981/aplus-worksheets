# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Circumference and area of circles (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g7_circles.py
pi is always 3.14 (every question says so). Every answer and every wrong choice is worked out with decimal.Decimal
from a named student mistake (r for d, C = pi r, C = 2 pi d, d in pi r squared, squaring pi, C / 2, C x pi ...).
Rounding is ROUND_HALF_UP to the place the question states.
Canadian English, metric units, SI number style (no-break space in numbers of 5 or more digits).
Pictures: labels never touch each other, and no line runs through a label (checked in Canvas).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
SQFILL = "#f6dcb4"
RED = "#c0392b"
BLUE = "#2f6fb5"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
PI = Dm("3.14")
USE = " Use π ≈ 3.14."


# ------------------------------------------------------------ numbers
def rnd(x, places):
    """Round half up to 0, 1 or 2 decimal places."""
    return x.quantize(Dm(1).scaleb(-places), rounding=ROUND_HALF_UP)


def N(x, places=None):
    """Number text. places=None: exact, no trailing zeros. Integer part of 5+ digits gets no-break spaces."""
    x = Dm(x)
    if places is None:
        s = format(x.normalize(), "f")
    else:
        s = format(rnd(x, places), "f")
    neg = s.startswith("-")
    s = s.lstrip("-")
    ip, _, fp = s.partition(".")
    if len(ip) >= 5:
        g = []
        while len(ip) > 3:
            g.insert(0, ip[-3:])
            ip = ip[:-3]
        g.insert(0, ip)
        ip = NB.join(g)
    s = ip + ("." + fp if fp else "")
    return ("−" if neg else "") + s


NUMRX = re.compile(r"^(\$)?([\d ]*\.?\d+)( .+)?$")


def val(c):
    m = NUMRX.match(c)
    if not m:
        return None
    return (Dm(m.group(2).replace(NB, "")), (m.group(1) or "") + (m.group(3) or "").strip())


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong. No two choices may have the same value and unit."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(ch)) == 4, (q, ch)
    vs = [val(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    for v in known:
        assert v[0] > 0, (q, ch)
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


def circle_pts(c, r, n=72):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


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

    def poly(self, pts, fill, sw=2, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=3, col=GREEN):
        self.el.append(("c", c, r, fill, sw, col))
        self.polys.append(circle_pts(c, r))
        self.grow(c[0] - r - sw, c[1] - r - sw, c[0] + r + sw, c[1] + r + sw)

    def dot(self, c, r=4, col=INK):
        self.el.append(("c", c, r, col, 0, col))
        self.segs.append((c, c))
        self.grow(c[0] - r, c[1] - r, c[0] + r, c[1] + r)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

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
        """Each label is inside one shape or outside all shapes, and no line runs through it."""
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
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                st = " stroke='%s' stroke-width='%g'" % (col, sw) if sw else ""
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'%s/>" % (c[0] - ox, c[1] - oy, r, fill, st))
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


def part_fig(part, deg=0, r=56):
    """Circle with one part in red: radius, diameter, circumference or centre."""
    cv = Canvas()
    if part == "circumference":
        cv.circle((0, 0), r, sw=6, col=RED)
    else:
        cv.circle((0, 0), r)
    if part == "radius":
        cv.line((0, 0), pol(r, deg), sw=4, col=RED)
    elif part == "diameter":
        cv.line(pol(r, deg), pol(r, deg + 180), sw=4, col=RED)
    if part == "centre":
        cv.dot((0, 0), 7, RED)
    else:
        cv.dot((0, 0), 4)
    return cv.svg("circle with its %s shown in red" % part)


def len_fig(lab, kind="radius", r=72):
    """Circle with its radius or diameter drawn and labelled; the label sits above the line."""
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.dot((0, 0), 4)
    if kind == "radius":
        cv.line((0, 0), (r, 0), sw=3, col=INK)
        cv.text(r / 2 + 2, -14, lab)
    else:
        cv.line((-r, 0), (r, 0), sw=3, col=INK)
        cv.text(-r / 2, -14, lab)
    return cv.svg("circle with its %s labelled %s" % (kind, lab))


# ------------------------------------------------------------ wording
def cm(x, u="cm", places=None):
    return "%s %s" % (N(x, places), u)


def cmz(x, u="cm", places=2):
    """Rounded to places, then without trailing zeros (for wrong choices of exact questions)."""
    return cm(rnd(Dm(x), places).normalize(), u)


def nearest(places):
    return {0: "the nearest whole number", 1: "the nearest tenth", 2: "the nearest hundredth"}[places]


# ============================================================ set 1: vocabulary
def set_parts():
    its = []
    asks = [("radius", 35, "What is the red line called?"),
            ("diameter", 20, "The red line goes through the centre. What is it called?"),
            ("circumference", 0, "What is the red edge of this circle called?"),
            ("centre", 0, "What is the red point called?")]
    exp = {"radius": "It goes from the centre to the edge, so it is a <b>radius</b>.",
           "diameter": "It goes all the way across the circle through the centre, so it is a <b>diameter</b>.",
           "circumference": "The distance all the way around a circle is its <b>circumference</b>. It is the perimeter of the circle.",
           "centre": "The point in the middle, the same distance from every point on the edge, is the <b>centre</b>."}
    for part, deg, q in asks:
        others = [p for p in ["radius", "diameter", "circumference", "centre"] if p != part]
        its.append(mcq(q + fig(part_fig(part, deg)), part, others, exp[part]))
    # radius -> diameter
    for r, f in [(Dm(6), True), (Dm(9), False), (Dm(15), False), (Dm("4.5"), True), (Dm("12.5"), False)]:
        u = "cm" if r < 10 else "m"
        if f:
            q = "What is the diameter of this circle?" + fig(len_fig(cm(r, u), "radius"))
        else:
            q = "A circle has a radius of %s. What is its diameter?" % cm(r, u)
        its.append(mcq(q, cm(2 * r, u), [cm(r / 2, u), cm(r * r, u), cm(r, u)],
                       "The diameter is 2 radii: d = 2r = 2 × %s = <b>%s</b>." % (N(r), cm(2 * r, u))))
    # diameter -> radius
    for d, f in [(Dm(14), True), (Dm(30), False), (Dm(9), True), (Dm(50), False), (Dm("7.6"), False)]:
        u = "mm" if d == 50 else ("cm" if d != 30 else "m")
        if f:
            q = "What is the radius of this circle?" + fig(len_fig(cm(d, u), "diameter"))
        else:
            q = "A circle has a diameter of %s. What is its radius?" % cm(d, u)
        its.append(mcq(q, cm(d / 2, u), [cm(2 * d, u), cm(d, u), cmz(PI * d, u)],
                       "The radius is half the diameter: r = d ÷ 2 = %s ÷ 2 = <b>%s</b>." % (N(d), cm(d / 2, u))))
    its.append(mcq("How does the diameter of a circle compare with its radius?",
                   "It is 2 times as long", ["It is half as long", "It is the same length", "It is π times as long"],
                   "A diameter is made of two radii end to end, so d = 2r. It is <b>2 times as long</b>."))
    its.append(mcq("For every circle, the circumference divided by the diameter is the same number. What is it called?",
                   "π (pi)", ["the radius", "the area", "the centre"],
                   "C ÷ d is always the same for every circle. This number is <b>π</b>, about 3.14."))
    its.append(mcq("About how many diameters fit around the circumference of a circle?",
                   "a little more than 3", ["exactly 2", "exactly 4", "about 6"],
                   "C = π × d and π ≈ 3.14, so the circumference is <b>a little more than 3</b> diameters. "
                   "About 6 is the number of <b>radii</b> that fit around (2π ≈ 6.28)."))
    its.append(mcq("A circle has a radius of 5 cm. Which is the longest?", "the circumference",
                   ["the diameter", "the radius", "they are all the same"],
                   "r = 5 cm, d = 10 cm and C ≈ 3.14 × 10 = 31.4 cm. <b>The circumference</b> is the longest."))
    its.append(mcq("Kai draws a circle with a compass. He opens the compass to 4 cm. What is the diameter of his circle?",
                   "8 cm", ["4 cm", "2 cm", "16 cm"],
                   "The compass opening is the radius: r = 4 cm. d = 2 × 4 = <b>8 cm</b>."))
    its.append(mcq("Every radius of the same circle is…", "the same length",
                   ["a different length", "longer than the diameter", "half the circumference"],
                   "Every point on the circle is the same distance from the centre, so all radii are <b>the same length</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Radius, diameter and circumference", "items": its}


# ============================================================ set 2: circumference
def set_circumference():
    its = []
    its.append(mcq("Which formula gives the circumference of a circle with diameter d?", "C = πd",
                   ["C = πr²", "C = 2πd", "C = d ÷ π"],
                   "The circumference is π times the diameter: <b>C = πd</b>. πr² is the area."))
    its.append(mcq("Which formula gives the circumference of a circle with radius r?", "C = 2πr",
                   ["C = πr", "C = πr²", "C = 2r"],
                   "d = 2r, so C = πd = π × 2r = <b>2πr</b>. Do not forget the 2."))
    # diameter given -> C = pi d
    for d, u, f in [(10, "cm", True), (6, "cm", False), (20, "m", False), (14, "m", True), (18, "mm", False), (12, "cm", False)]:
        d = Dm(d)
        c = PI * d
        if f:
            q = "Find the circumference." + USE + fig(len_fig(cm(d, u), "diameter"))
        else:
            q = "A circle has a diameter of %s. Find its circumference.%s" % (cm(d, u), USE)
        its.append(mcq(q, cm(c, u), [cm(PI * d / 2, u), cm(2 * PI * d, u), cm(PI * (d / 2) ** 2, u)],
                       "C = πd ≈ 3.14 × %s = <b>%s</b>. Using 2πd would double it." % (N(d), cm(c, u))))
    # radius given -> C = 2 pi r
    for r, u, f in [(5, "cm", True), (3, "m", False), (7, "cm", True), (10, "m", False), (4, "cm", False), (15, "mm", False)]:
        r = Dm(r)
        c = 2 * PI * r
        if f:
            q = "Find the circumference." + USE + fig(len_fig(cm(r, u), "radius"))
        else:
            q = "A circle has a radius of %s. Find its circumference.%s" % (cm(r, u), USE)
        w = [cm(PI * r, u), cm(PI * r * r, u), cm(4 * PI * r, u)]
        if r == 4:                                # 2 pi r = pi r squared when r = 2 only; r = 4 gives 4 pi r = pi r squared
            w[2] = cm(2 * r, u)
        its.append(mcq(q, cm(c, u), w,
                       "d = 2 × %s = %s. C = πd ≈ 3.14 × %s = <b>%s</b>. C = πr would give only half."
                       % (N(r), N(2 * r), N(2 * r), cm(c, u))))
    # decimals, rounded
    for kind, x, u, p in [("diameter", "4.5", "cm", 1), ("radius", "2.6", "m", 1), ("diameter", "13.5", "cm", 1),
                          ("radius", "8.35", "cm", 2)]:
        x = Dm(x)
        d = x if kind == "diameter" else 2 * x
        c = PI * d
        alt_half = PI * d / 2
        alt_dbl = 2 * PI * d
        alt_area = PI * (d / 2) ** 2
        w = [cm(alt_half, u, p), cm(alt_dbl, u, p), cm(alt_area, u, p)]
        its.append(mcq("A circle has a %s of %s. Find its circumference to %s.%s" % (kind, cm(x, u), nearest(p), USE),
                       cm(c, u, p), w,
                       ("" if kind == "diameter" else "d = 2 × %s = %s. " % (N(x), N(d))) +
                       "C = πd ≈ 3.14 × %s = %s ≈ <b>%s</b>." % (N(d), N(c), cm(c, u, p))))
    assert len(its) == 18, len(its)
    its.append(mcq("Circle A has a diameter of 10 cm. Circle B has a radius of 6 cm. Which has the longer circumference?",
                   "Circle B", ["Circle A", "They are the same", "You can’t tell"],
                   "Circle B has d = 2 × 6 = 12 cm, which is more than 10 cm. A bigger diameter means a longer circumference: "
                   "31.4 cm for A and 37.68 cm for B. <b>Circle B</b>."))
    its.append(mcq("The diameter of a circle doubles from 5 cm to 10 cm. What happens to the circumference?",
                   "It doubles", ["It stays the same", "It goes up by 5 cm", "It is 4 times as long"],
                   "C = πd: 3.14 × 5 = 15.7 cm and 3.14 × 10 = 31.4 cm. Double the diameter, and the circumference "
                   "<b>doubles</b> too."))
    return {"title": "Circumference: C = πd = 2πr", "items": its}


# ============================================================ set 3: area
def area_wrong(r, u, p=None):
    """Mistakes: C = 2 pi r instead of area, d in pi r squared, forgot to square (pi r), squared pi ((pi r) squared)."""
    d = 2 * r
    f = (lambda x, uu: cmz(x, uu, 2)) if p is None else (lambda x, uu: cm(x, uu, p))
    return {"circ": f(2 * PI * r, u), "pid2": f(PI * d * d, u + "²"), "pir": f(PI * r, u + "²"),
            "sqpi": f((PI * r) ** 2, u + "²")}


def set_area():
    its = []
    its.append(mcq("Which formula gives the area of a circle?", "A = πr²", ["A = πd", "A = 2πr", "A = (πr)²"],
                   "<b>A = πr²</b>: square the radius, then multiply by π. Only r is squared, not π."))
    its.append(mcq("A circle has a radius of 3 cm. In which unit is its area measured?", "cm²", ["cm", "cm³", "m"],
                   "Area counts squares, so it is in square units: <b>cm²</b>. Circumference is a length, in cm."))
    # integer radius, text and figure
    plan = [(5, "cm", False, ["pid2", "circ", "pir"]), (3, "m", True, ["pid2", "circ", "sqpi"]),
            (7, "cm", False, ["circ", "pir", "sqpi"]), (10, "m", True, ["pid2", "circ", "pir"]),
            (4, "cm", False, ["pid2", "pir", "sqpi"]), (6, "mm", True, ["pid2", "circ", "sqpi"]),
            (9, "cm", False, ["circ", "pid2", "pir"]), (12, "m", False, ["pid2", "circ", "sqpi"])]
    for r, u, f, keys in plan:
        r = Dm(r)
        a = PI * r * r
        w = area_wrong(r, u)
        if f:
            q = "Find the area of this circle." + USE + fig(len_fig(cm(r, u), "radius"))
        else:
            q = "A circle has a radius of %s. Find its area.%s" % (cm(r, u), USE)
        its.append(mcq(q, cm(a, u + "²"), [w[k] for k in keys],
                       "A = πr² ≈ 3.14 × %s × %s = 3.14 × %s = <b>%s</b>. Square the radius, not π."
                       % (N(r), N(r), N(r * r), cm(a, u + "²"))))
    # diameter given
    for d, u, f in [(10, "cm", True), (8, "m", False), (14, "cm", True), (20, "m", False), (30, "cm", False)]:
        d = Dm(d)
        r = d / 2
        a = PI * r * r
        w = area_wrong(r, u)
        if f:
            q = "Find the area of this circle." + USE + fig(len_fig(cm(d, u), "diameter"))
        else:
            q = "A circle has a diameter of %s. Find its area.%s" % (cm(d, u), USE)
        its.append(mcq(q, cm(a, u + "²"), [w["pid2"], w["circ"], w["pir"]],
                       "First halve the diameter: r = %s ÷ 2 = %s. A = πr² ≈ 3.14 × %s = <b>%s</b>. "
                       "Using d in πr² gives 4 times too much." % (N(d), N(r), N(r * r), cm(a, u + "²"))))
    # decimal radius, rounded to the nearest tenth
    for r, u in [("2.5", "cm"), ("1.5", "m"), ("4.2", "cm"), ("0.8", "m"), ("6.5", "cm")]:
        r = Dm(r)
        a = PI * r * r
        w = area_wrong(r, u, 1)
        its.append(mcq("A circle has a radius of %s. Find its area to the nearest tenth.%s" % (cm(r, u), USE),
                       cm(a, u + "²", 1), [w["pid2"], w["circ"], w["pir"]],
                       "r² = %s × %s = %s. A ≈ 3.14 × %s = %s ≈ <b>%s</b>."
                       % (N(r), N(r), N(r * r), N(r * r), N(a), cm(a, u + "²", 1))))
    assert len(its) == 20, len(its)
    return {"title": "Area: A = πr²", "items": its}


# ============================================================ set 4: r or d from C
def set_from_c():
    its = []
    its.append(mcq("You know the circumference of a circle. How do you find its diameter?", "divide C by π",
                   ["multiply C by π", "divide C by 2", "multiply C by 2"],
                   "C = πd, so d = C ÷ π. <b>Divide C by π</b> (about 3.14)."))
    its.append(mcq("You know the circumference of a circle. How do you find its radius?", "divide C by 2π",
                   ["divide C by π", "multiply C by 2π", "divide C by 2"],
                   "C = 2πr, so r = C ÷ 2π. <b>Divide C by 2π</b> (about 6.28). Dividing by π gives the diameter."))
    # exact diameter
    for d, u in [(10, "cm"), (5, "m"), (12, "cm"), (30, "mm"), (7, "m"), (25, "cm")]:
        d = Dm(d)
        c = PI * d
        its.append(mcq("A circle has a circumference of %s. Find its diameter.%s" % (cm(c, u), USE), cm(d, u),
                       [cm(d / 2, u), cmz(c / 2, u), cmz(c * PI, u)],
                       "d = C ÷ π ≈ %s ÷ 3.14 = <b>%s</b>. Check: 3.14 × %s = %s." % (N(c), cm(d, u), N(d), N(c))))
    # exact radius
    for r, u in [(4, "cm"), (10, "m"), (6, "cm"), (15, "m"), (8, "mm"), (20, "cm")]:
        r = Dm(r)
        c = 2 * PI * r
        its.append(mcq("A circle has a circumference of %s. Find its radius.%s" % (cm(c, u), USE), cm(r, u),
                       [cm(2 * r, u), cmz(c / 2, u), cmz(c * PI, u)],
                       "d = C ÷ π ≈ %s ÷ 3.14 = %s. r = %s ÷ 2 = <b>%s</b>. Or r = C ÷ 6.28 in one step."
                       % (N(c), N(2 * r), N(2 * r), cm(r, u))))
    # rounded
    for c, u, want, p in [(40, "cm", "d", 1), (100, "m", "d", 1), (25, "cm", "r", 1), (60, "cm", "r", 2),
                          (18, "m", "d", 2), (75, "cm", "r", 1)]:
        c = Dm(c)
        d = c / PI
        r = c / (2 * PI)
        if want == "d":
            right, w = d, [r, c / 2, c * PI]
            s = "d = C ÷ π ≈ %s ÷ 3.14 = %s… ≈ <b>%s</b>." % (N(c), N(rnd(d, 3)), cm(d, u, p))
            name = "diameter"
        else:
            right, w = r, [d, c / 2, c * PI]
            s = "r = C ÷ 2π ≈ %s ÷ 6.28 = %s… ≈ <b>%s</b>." % (N(c), N(rnd(r, 3)), cm(r, u, p))
            name = "radius"
        its.append(mcq("A circle has a circumference of %s. Find its %s to %s.%s" % (cm(c, u), name, nearest(p), USE),
                       cm(right, u, p), [cm(x, u, p) for x in w], s))
    assert len(its) == 20, len(its)
    return {"title": "Finding r or d from the circumference", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    # 1 bike wheel, one turn
    d = Dm(66)
    its.append(mcq("Liam’s bike wheel has a diameter of 66 cm. How far does the bike move in one full turn of the wheel?" + USE,
                   cm(PI * d), [cm(PI * d / 2), cm(2 * PI * d), cm(PI * 33 * 33)],
                   "One turn rolls out the circumference. C = πd ≈ 3.14 × 66 = <b>207.24 cm</b>."))
    # 2 bike wheel, 100 turns in metres
    its.append(mcq("The wheel on Liam’s bike goes 207.24 cm in one turn. How many metres does the bike go in 100 turns?",
                   "207.24 m", ["20.724 m", "2072.4 m", "2.0724 m"],
                   "100 × 207.24 cm = 20" + NB + "724 cm. 100 cm = 1 m, so 20" + NB + "724 cm ÷ 100 = <b>207.24 m</b>."))
    # 3 bike wheel, turns for 1 km
    d = Dm(64)
    c = PI * d
    n = 100000 / c
    assert rnd(n, 0) == 498
    its.append(mcq("Ava rides her bike 1 km along the Seawall in Stanley Park. Her wheels have a diameter of 64 cm. "
                   "About how many full turns does each wheel make? (1 km = 100" + NB + "000 cm)" + USE,
                   "about 498", ["about 995", "about 1563", "about 249"],
                   "C = πd ≈ 3.14 × 64 = 200.96 cm. 100" + NB + "000 ÷ 200.96 ≈ 497.6, so <b>about 498</b> turns. "
                   "Dividing by 64 forgets π."))
    assert rnd(100000 / (PI * 32), 0) == 995 and rnd(Dm(100000) / 64, 0) == 1563 and rnd(100000 / (2 * PI * 64), 0) == 249
    # 4 round table, tablecloth area
    its.append(mcq("A round table in the library is 1.2 m across. What is the area of the tabletop, to the nearest hundredth?" + USE,
                   cm(PI * Dm("0.36"), "m²", 2), [cm(PI * Dm("1.44"), "m²", 2), cm(PI * Dm("1.2"), "m²", 2),
                                                   cm(PI * Dm("0.6"), "m²", 2)],
                   "1.2 m across is the diameter, so r = 0.6 m. A = πr² ≈ 3.14 × 0.36 = 1.1304 ≈ <b>1.13 m²</b>."))
    # 5 round table, trim
    its.append(mcq("Simran glues ribbon around the edge of a round table with a diameter of 1.2 m. "
                   "How much ribbon does she need, to the nearest tenth of a metre?" + USE,
                   cm(PI * Dm("1.2"), "m", 1), [cm(PI * Dm("0.6"), "m", 1), cm(2 * PI * Dm("1.2"), "m", 1),
                                                cm(PI * Dm("0.36"), "m", 1)],
                   "The edge is the circumference. C = πd ≈ 3.14 × 1.2 = 3.768 ≈ <b>3.8 m</b>."))
    # 6 garden fence
    r = Dm(3)
    its.append(mcq("A circular garden in Kelowna has a radius of 3 m. How long is a fence that goes all the way around it?" + USE,
                   cm(2 * PI * r, "m"), [cm(PI * r, "m"), cm(PI * r * r, "m"), cm(4 * PI * r, "m")],
                   "The fence is the circumference. d = 6 m, so C = πd ≈ 3.14 × 6 = <b>18.84 m</b>."))
    # 7 garden area
    its.append(mcq("The same circular garden has a radius of 3 m. What area does it cover?" + USE,
                   cm(PI * 9, "m²"), [cm(2 * PI * 3, "m²"), cm(PI * 36, "m²"), cmz((PI * 3) ** 2, "m²")],
                   "A = πr² ≈ 3.14 × 3 × 3 = 3.14 × 9 = <b>28.26 m²</b>."))
    # 8 fencing cost
    c = 2 * PI * 2
    assert c * 12 == Dm("150.72")
    its.append(mcq("Mateo puts a fence around a circular garden with a radius of 2 m. The fencing costs $12 per metre. "
                   "How much does the fencing cost?" + USE,
                   "$150.72", ["$75.36", "$301.44", "$24.56"],
                   "C = 2πr ≈ 2 × 3.14 × 2 = 12.56 m. Cost = 12.56 × $12 = <b>$150.72</b>."))
    assert PI * 2 * 12 == Dm("75.36") and 2 * PI * 4 * 12 == Dm("301.44") and c + 12 == Dm("24.56")
    # 9 mulch bags
    a = PI * 16
    assert a == Dm("50.24")
    its.append(mcq("A circular flower bed has a diameter of 8 m. One bag of mulch covers 5 m². "
                   "How many bags does Jasleen need to cover the whole bed?" + USE,
                   "11 bags", ["10 bags", "6 bags", "41 bags"],
                   "r = 4 m. A = πr² ≈ 3.14 × 16 = 50.24 m². 50.24 ÷ 5 = 10.048, so 10 bags are not quite enough. "
                   "She needs <b>11 bags</b>."))
    assert 2 * PI * 4 / 5 > 5 and PI * 64 / 5 > 40
    # 10 cedar trunk
    c = Dm("4.71")
    its.append(mcq("Owen wraps a rope around a cedar trunk in Pacific Spirit Park. The rope measures 4.71 m. "
                   "What is the diameter of the trunk?" + USE,
                   cm(c / PI, "m"), [cm(c / PI / 2, "m"), cmz(c * PI, "m"), cmz(c / 2, "m")],
                   "The rope measures the circumference. d = C ÷ π ≈ 4.71 ÷ 3.14 = <b>1.5 m</b>."))
    # 11 sprinkler
    r = Dm(5)
    its.append(mcq("A lawn sprinkler waters a circle with a radius of 5 m. What area of grass does it water?" + USE,
                   cm(PI * 25, "m²"), [cm(2 * PI * 5, "m²"), cm(PI * 100, "m²"), cm(PI * 5, "m²")],
                   "A = πr² ≈ 3.14 × 25 = <b>78.5 m²</b>. 31.4 is the circumference, not the area."))
    # 12 trampoline net
    d = Dm("3.6")
    its.append(mcq("A round trampoline has a diameter of 3.6 m. A safety net goes all the way around the edge. "
                   "How long is the net, to the nearest tenth of a metre?" + USE,
                   cm(PI * d, "m", 1), [cm(PI * d / 2, "m", 1), cm(PI * Dm("1.8") ** 2, "m", 1), cm(2 * PI * d, "m", 1)],
                   "C = πd ≈ 3.14 × 3.6 = 11.304 ≈ <b>11.3 m</b>."))
    # 13 pizza
    assert PI * 225 > 2 * PI * 100
    its.append(mcq("Which gives more pizza: one round pizza 30 cm across, or two round pizzas 20 cm across?" + USE,
                   "one 30 cm pizza", ["two 20 cm pizzas", "they are the same", "you can’t tell"],
                   "30 cm pizza: r = 15, A ≈ 3.14 × 225 = 706.5 cm². Two 20 cm pizzas: r = 10, A ≈ 2 × 314 = 628 cm². "
                   "So <b>one 30 cm pizza</b> gives more, even though 20 + 20 &gt; 30."))
    # 14 path around a pond
    c = 2 * PI * 50
    its.append(mcq("A circular path around a pond in a Surrey park has a radius of 50 m. Mei walks around it 3 times. "
                   "How far does she walk?" + USE,
                   cm(3 * c, "m"), [cm(3 * PI * 50, "m"), cm(c, "m"), cm(3 * PI * 2500, "m")],
                   "One lap: C = 2πr ≈ 2 × 3.14 × 50 = 314 m. Three laps: 3 × 314 = <b>942 m</b>."))
    # 15 clock
    r = Dm(15)
    its.append(mcq("The classroom clock has a round face with a radius of 15 cm. What is the area of the clock face?" + USE,
                   cm(PI * 225, "cm²"), [cm(2 * PI * 15, "cm²"), cm(PI * 900, "cm²"), cm(PI * 15, "cm²")],
                   "A = πr² ≈ 3.14 × 15 × 15 = 3.14 × 225 = <b>706.5 cm²</b>."))
    # 16 stump radius
    c = Dm("2.512")
    its.append(mcq("The edge of a round tree stump measures 2.512 m around. What is the radius of the stump?" + USE,
                   cm(c / (2 * PI), "m"), [cm(c / PI, "m"), cm(c / 2, "m"), cmz(c * PI, "m")],
                   "d = C ÷ π ≈ 2.512 ÷ 3.14 = 0.8 m. r = 0.8 ÷ 2 = <b>0.4 m</b>."))
    # 17 circle on the ice
    r = Dm("4.5")
    its.append(mcq("A circle painted on a hockey rink has a radius of 4.5 m. How long is the painted line around it?" + USE,
                   cm(2 * PI * r, "m"), [cm(PI * r, "m"), cmz(PI * r * r, "m"), cm(4 * PI * r, "m")],
                   "d = 9 m. C = πd ≈ 3.14 × 9 = <b>28.26 m</b>."))
    # 18 hand drum
    r = Dm(20)
    its.append(mcq("Harjot’s hand drum has a round top 40 cm across. What is the area of the drum’s top?" + USE,
                   cm(PI * 400, "cm²"), [cm(2 * PI * 20, "cm²"), cm(PI * 1600, "cm²"), cm(PI * 20, "cm²")],
                   "40 cm across is the diameter, so r = 20 cm. A = πr² ≈ 3.14 × 400 = <b>1256 cm²</b>."))
    # 19 circle vs square
    assert PI * 10 < 32
    its.append(mcq("Which is longer: the circumference of a circle with a diameter of 10 cm, or the perimeter of a square "
                   "with 8 cm sides?" + USE,
                   "the square’s perimeter", ["the circle’s circumference", "they are the same", "you can’t tell"],
                   "Circle: C ≈ 3.14 × 10 = 31.4 cm. Square: P = 4 × 8 = 32 cm. <b>The square’s perimeter</b> is longer by 0.6 cm."))
    # 20 Ferris wheel
    d = Dm(20)
    its.append(mcq("A Ferris wheel at a summer fair in Abbotsford has a diameter of 20 m. "
                   "How far does a seat travel in one full turn?" + USE,
                   cm(PI * d, "m"), [cm(PI * 10, "m"), cm(2 * PI * d, "m"), cm(PI * 100, "m")],
                   "The seat travels the circumference. C = πd ≈ 3.14 × 20 = <b>62.8 m</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: wheels, tables and gardens", "items": its}


# ============================================================ lesson
def parts_lesson_svg():
    r = 80
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.line((-r, 0), (r, 0), sw=3, col=BLUE)
    cv.line((0, 0), pol(r, 60), sw=3, col=RED)
    cv.dot((0, 0), 4)
    cv.text(0, 16, "centre", 15)
    cv.text(-40, -14, "diameter", 15, col=BLUE)
    cv.text(r + 8, -48, "radius", 15, "start", RED)
    cv.text(r + 8, 50, "circumference", 15, "start", GREEN)
    cv.line(pol(r * 0.8, 60), (r + 4, -48), sw=1.5, col=RED)
    cv.line((r * math.cos(math.radians(35)), r * math.sin(math.radians(35))), (r + 4, 50), sw=1.5, col=GREEN)
    return cv.svg("circle with its centre, a radius, a diameter and the circumference labelled")


def unroll_svg():
    """A circle of diameter 1 unit rolled out: the circumference is a little more than 3 diameters."""
    u = 60
    s = []
    cx, cy, r = 40, 46, u / 2
    s.append("<circle cx='%g' cy='%g' r='%g' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r, FILL, GREEN))
    s.append("<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='%s' stroke-width='3'/>" % (cx - r, cy, cx + r, cy, BLUE))
    s.append("<text x='%g' y='%g' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>d</text>" % (cx, cy - 6, BLUE))
    x0, y0 = 100, 76
    L = float(PI) * u
    s.append("<line x1='%g' y1='%g' x2='%.1f' y2='%g' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
             % (x0, y0, x0 + L, y0, GREEN))
    for k in range(4):
        x = x0 + k * u
        s.append("<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='%s' stroke-width='2'/>" % (x, y0 - 12, x, y0 + 12, INK))
    s.append("<line x1='%.1f' y1='%g' x2='%.1f' y2='%g' stroke='%s' stroke-width='2'/>" % (x0 + L, y0 - 12, x0 + L, y0 + 12, INK))
    for k in range(3):
        x = x0 + k * u
        s.append("<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='%s' stroke-width='3'/>" % (x + 3, y0 - 22, x + u - 3, y0 - 22, BLUE))
        s.append("<text x='%g' y='%g' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>d</text>"
                 % (x + u / 2, y0 - 28, BLUE))
    s.append("<text x='%.1f' y='%g' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>C = 3.14 × d</text>"
             % (x0 + L / 2, y0 + 32, GREEN))
    W = int(math.ceil(x0 + L + 10))
    return svg_wrap(W, 116, "".join(s), "a circle rolled out flat: its circumference is a little more than 3 diameters")


def area_lesson_svg():
    r = 70
    cv = Canvas()
    cv.poly([(0, 0), (r, 0), (r, -r), (0, -r)], SQFILL, 2, INK)
    cv.circle((0, 0), r, fill="none")
    cv.dot((0, 0), 4)
    cv.line((0, 0), (-r, 0), sw=3, col=RED)
    cv.text(-r / 2, -14, "r", 16, col=RED)
    cv.text(r / 2, -r / 2, "r²", 17)
    return cv.svg("circle with a square of side r on its radius; the area of the circle is about 3.14 of these squares")


def body_html():
    return (
        "<h2>Parts of a circle</h2>"
        "<p>The <b>centre</b> is the middle point. A <b>radius</b> (r) goes from the centre to the edge. "
        "A <b>diameter</b> (d) goes all the way across through the centre. "
        "The <b>circumference</b> (C) is the distance all the way around: the perimeter of the circle.</p>"
        "<figure class='sn-fig'>" + parts_lesson_svg() +
        "<figcaption>A diameter is two radii: d = 2r and r = d ÷ 2.</figcaption></figure>"
        "<h2>Circumference: C = πd = 2πr</h2>"
        "<p>For every circle, C ÷ d is the same number. It is called <b>π</b> (pi). π = 3.14159…, "
        "and in these worksheets we use <b>π ≈ 3.14</b>. So the circumference is a little more than 3 diameters.</p>"
        "<figure class='sn-fig'>" + unroll_svg() +
        "<figcaption>Roll a circle out flat: its edge is 3 diameters and a little more.</figcaption></figure>"
        + ex("Example 1", "A bike wheel has a diameter of 60 cm. How far does it roll in one turn?",
             "C = πd ≈ 3.14 × 60 = 188.4", "188.4 cm")
        + ex("Example 2", "A circle has a radius of 5 m. Find its circumference.",
             "d = 2 × 5 = 10 m. C = πd ≈ 3.14 × 10 = 31.4", "31.4 m")
        + "<h2>Area: A = πr²</h2>"
        "<p>Square the radius, then multiply by π. The circle covers about 3.14 squares of side r. "
        "Area is in square units, such as cm² or m².</p>"
        "<figure class='sn-fig'>" + area_lesson_svg() +
        "<figcaption>The square on the radius has area r². The circle is about 3.14 of these squares.</figcaption></figure>"
        + ex("Example 3", "A round table has a diameter of 2 m. Find the area of its top.",
             "r = 2 ÷ 2 = 1 m. A = πr² ≈ 3.14 × 1 × 1 = 3.14", "3.14 m²")
        + "<h2>Working backwards</h2>"
        "<p>If you know the circumference, divide by π to get the diameter: d = C ÷ π. "
        "Then halve it for the radius.</p>"
        + ex("Example 4", "A tree trunk is 1.57 m around. Find its diameter.",
             "d = C ÷ π ≈ 1.57 ÷ 3.14 = 0.5", "0.5 m")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the diameter in A = πr²", "Halve d first: r = d ÷ 2"],
            ["C = πr", "C = 2πr (or C = πd)"],
            ["Squaring π: (3.14 × 5)²", "Square only r: 3.14 × 5²"],
            ["Mixing up C and A", "C is a length (cm); A is an area (cm²)"],
            ["Multiplying C by π to find d", "Divide: d = C ÷ π"],
        ])
    )


FAQ = [
    {"q": "Do Grade 7 students in BC learn circumference and area of circles?",
     "a": "Yes. Circumference and area of circles are part of Geometry and measurement in the BC Grade 7 math curriculum. Students find C = πd and A = πr² and use them to solve problems."},
    {"q": "What is the difference between circumference and area?",
     "a": "Circumference is the distance around a circle, measured in units like cm. Area is the space inside the circle, measured in square units like cm²."},
    {"q": "What value of π should Grade 7 students use?",
     "a": "Most Grade 7 work uses π ≈ 3.14, or the π key on a calculator. These worksheets use 3.14 so answers can be checked by hand."},
    {"q": "Do these circle worksheets help with the Grade 7 FSA?",
     "a": "Yes. The Grade 7 FSA includes numeracy, where students solve problems with measurement and decimals. Wheel, table and garden problems like these are good practice."},
]


def gen():
    r = random.Random(37810)
    sets = [set_parts(), set_circumference(), set_area(), set_from_c(), set_problems()]
    balance(sets, r)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "circumference-and-area-of-circles", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Circumference and Area of Circles",
        "seo_title": "Grade 7 Circumference and Area of Circles Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Circumference and area of circles",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 7: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Circumference and area of circles",
        "meta_desc": "Free Grade 7 math worksheets on circumference and area of circles for the BC curriculum: radius and diameter, C = πd = 2πr, A = πr² and finding the diameter from the circumference, with bike wheel, table and garden problems. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "Circumference C = πd = 2πr. Area A = πr². Use π ≈ 3.14.",
        "key_sub": "The diameter is 2 radii, so halve d before you use A = πr². Square only r, not π. C is a length (cm); A is in square units (cm²).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
