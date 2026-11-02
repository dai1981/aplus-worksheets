# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Circles (Ontario Curriculum 2020, Spatial Sense E2.3 and E2.5)
  python3 tools/gen_caon_math_g7_circles.py
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
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
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
    asks = [("radius", 125, "The red segment joins the centre to the edge. What is it called?"),
            ("diameter", 150, "What is the red segment called?"),
            ("circumference", 0, "The red line goes all the way around the circle. What is it called?"),
            ("centre", 0, "The red point is the same distance from every point on the edge. What is it called?")]
    exp = {"radius": "A segment from the centre to the edge is a <b>radius</b>.",
           "diameter": "It crosses the whole circle and passes through the centre, so it is a <b>diameter</b>.",
           "circumference": "The distance around a circle is its <b>circumference</b>: the perimeter of the circle.",
           "centre": "The middle point, the same distance from every point on the edge, is the <b>centre</b>."}
    for part, deg, q in asks:
        others = [p for p in ["radius", "diameter", "circumference", "centre"] if p != part]
        its.append(mcq(q + fig(part_fig(part, deg)), part, others, exp[part]))
    # radius -> diameter
    for r, u, f in [(Dm(8), "cm", True), (Dm(11), "m", False), (Dm(25), "mm", False), (Dm("3.5"), "cm", True),
                    (Dm("7.5"), "m", False)]:
        if f:
            q = "What is the diameter of this circle?" + fig(len_fig(cm(r, u), "radius"))
        else:
            q = "A circle has a radius of %s. What is its diameter?" % cm(r, u)
        its.append(mcq(q, cm(2 * r, u), [cm(r / 2, u), cm(r * r, u), cm(r, u)],
                       "A diameter is 2 radii: d = 2r = 2 × %s = <b>%s</b>." % (N(r), cm(2 * r, u))))
    # diameter -> radius
    for d, u, f in [(Dm(16), "cm", True), (Dm(40), "m", False), (Dm(7), "cm", True), (Dm(24), "mm", False),
                    (Dm("9.4"), "cm", False)]:
        if f:
            q = "What is the radius of this circle?" + fig(len_fig(cm(d, u), "diameter"))
        else:
            q = "A circle has a diameter of %s. What is its radius?" % cm(d, u)
        its.append(mcq(q, cm(d / 2, u), [cm(2 * d, u), cm(d, u), cmz(PI * d, u)],
                       "The radius is half the diameter: r = d ÷ 2 = %s ÷ 2 = <b>%s</b>." % (N(d), cm(d / 2, u))))
    its.append(mcq("A diameter of a circle is always 2 times as long as…", "a radius",
                   ["the circumference", "the centre", "the area"],
                   "A diameter is two radii end to end, so d = 2r. It is 2 times as long as <b>a radius</b>."))
    its.append(mcq("The number π is the ratio of which two measures of a circle?", "circumference to diameter",
                   ["diameter to radius", "circumference to radius", "area to radius"],
                   "For every circle, C ÷ d is the same number, π ≈ 3.14. So π is <b>circumference to diameter</b>. "
                   "C ÷ r is 2π and d ÷ r is 2."))
    its.append(mcq("About how many radii fit around the circumference of a circle?",
                   "a little more than 6", ["a little more than 3", "exactly 2", "exactly 4"],
                   "C = 2πr ≈ 6.28 × r, so <b>a little more than 6</b> radii fit around. "
                   "A little more than 3 is the number of diameters."))
    its.append(mcq("A circle has a diameter of 12 cm. Which is the shortest?", "the radius",
                   ["the diameter", "the circumference", "they are all the same"],
                   "r = 6 cm, d = 12 cm and C ≈ 3.14 × 12 = 37.68 cm. <b>The radius</b> is the shortest."))
    its.append(mcq("Priya opens her compass to 6 cm and draws a circle. What is the diameter of the circle?",
                   "12 cm", ["6 cm", "3 cm", "36 cm"],
                   "The compass opening is the radius: r = 6 cm. d = 2 × 6 = <b>12 cm</b>."))
    its.append(mcq("All the radii of one circle are…", "the same length",
                   ["different lengths", "longer than the diameter", "half the circumference"],
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
                   "d = 2r, so C = πd = π × 2r = <b>2πr</b>. C = πr forgets the 2 and gives half the answer."))
    for d, u, f in [(22, "cm", True), (15, "cm", False), (30, "m", False), (12, "m", True), (25, "mm", False), (9, "cm", False)]:
        d = Dm(d)
        c = PI * d
        if f:
            q = "Find the circumference." + USE + fig(len_fig(cm(d, u), "diameter"))
        else:
            q = "A circle has a diameter of %s. Find its circumference.%s" % (cm(d, u), USE)
        its.append(mcq(q, cm(c, u), [cm(PI * d / 2, u), cm(2 * PI * d, u), cmz(PI * (d / 2) ** 2, u)],
                       "C = πd ≈ 3.14 × %s = <b>%s</b>. Do not double it: 2π goes with the radius, not the diameter."
                       % (N(d), cm(c, u))))
    for r, u, f in [(6, "cm", True), (8, "m", False), (9, "cm", True), (20, "m", False), (11, "cm", False), (35, "mm", False)]:
        r = Dm(r)
        c = 2 * PI * r
        if f:
            q = "Find the circumference." + USE + fig(len_fig(cm(r, u), "radius"))
        else:
            q = "A circle has a radius of %s. Find its circumference.%s" % (cm(r, u), USE)
        its.append(mcq(q, cm(c, u), [cm(PI * r, u), cm(PI * r * r, u), cm(4 * PI * r, u)],
                       "d = 2 × %s = %s. C = πd ≈ 3.14 × %s = <b>%s</b>. C = πr would give only half."
                       % (N(r), N(2 * r), N(2 * r), cm(c, u))))
    for kind, x, u, p in [("diameter", "5.5", "cm", 1), ("radius", "3.4", "m", 1), ("diameter", "10.5", "cm", 1),
                          ("radius", "6.35", "cm", 2)]:
        x = Dm(x)
        d = x if kind == "diameter" else 2 * x
        c = PI * d
        w = [cm(PI * d / 2, u, p), cm(2 * PI * d, u, p), cm(PI * (d / 2) ** 2, u, p)]
        its.append(mcq("A circle has a %s of %s. Find its circumference to %s.%s" % (kind, cm(x, u), nearest(p), USE),
                       cm(c, u, p), w,
                       ("" if kind == "diameter" else "d = 2 × %s = %s. " % (N(x), N(d))) +
                       "C = πd ≈ 3.14 × %s = %s ≈ <b>%s</b>." % (N(d), N(c), cm(c, u, p))))
    assert len(its) == 18, len(its)
    its.append(mcq("Circle A has a diameter of 14 cm. Circle B has a radius of 8 cm. Which has the longer circumference?",
                   "Circle B", ["Circle A", "They are the same", "You can’t tell"],
                   "Circle B has d = 2 × 8 = 16 cm, which is more than 14 cm. C ≈ 3.14 × 14 = 43.96 cm for A and "
                   "3.14 × 16 = 50.24 cm for B. <b>Circle B</b>."))
    its.append(mcq("The radius of a circle triples from 2 cm to 6 cm. What happens to the circumference?",
                   "It triples", ["It stays the same", "It goes up by 4 cm", "It is 9 times as long"],
                   "C = 2πr: 2 × 3.14 × 2 = 12.56 cm and 2 × 3.14 × 6 = 37.68 cm. 37.68 ÷ 12.56 = 3, "
                   "so the circumference <b>triples</b>."))
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
    its.append(mcq("Which formula gives the area of a circle?", "A = πr²", ["A = πd", "A = 2πr", "A = πd²"],
                   "<b>A = πr²</b>: square the radius, then multiply by π. πd² uses the diameter and gives 4 times too much."))
    its.append(mcq("A circle has a diameter of 8 m. In which unit is its area measured?", "m²", ["m", "m³", "cm²"],
                   "Area counts squares, so it is in square units of the same length unit: <b>m²</b>. "
                   "The circumference is a length, in m."))
    plan = [(6, "cm", False, ["pid2", "circ", "pir"]), (5, "m", True, ["pid2", "circ", "sqpi"]),
            (8, "cm", False, ["circ", "pir", "sqpi"]), (10, "mm", True, ["pid2", "circ", "pir"]),
            (3, "cm", False, ["pid2", "pir", "sqpi"]), (11, "m", True, ["pid2", "circ", "sqpi"]),
            (7, "m", False, ["circ", "pid2", "pir"]), (15, "cm", False, ["pid2", "circ", "sqpi"])]
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
    for d, u, f in [(12, "cm", True), (6, "m", False), (18, "cm", True), (16, "m", False), (40, "cm", False)]:
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
    for r, u in [("3.5", "cm"), ("2.5", "m"), ("1.2", "m"), ("5.4", "cm"), ("0.9", "m")]:
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
    for d, u in [(8, "cm"), (15, "m"), (20, "cm"), (40, "mm"), (3, "m"), (50, "cm")]:
        d = Dm(d)
        c = PI * d
        its.append(mcq("A circle has a circumference of %s. Find its diameter.%s" % (cm(c, u), USE), cm(d, u),
                       [cm(d / 2, u), cmz(c / 2, u), cmz(c * PI, u)],
                       "d = C ÷ π ≈ %s ÷ 3.14 = <b>%s</b>. Check: 3.14 × %s = %s." % (N(c), cm(d, u), N(d), N(c))))
    for r, u in [(3, "cm"), (12, "m"), (5, "cm"), (25, "m"), (9, "mm"), (30, "cm")]:
        r = Dm(r)
        c = 2 * PI * r
        its.append(mcq("A circle has a circumference of %s. Find its radius.%s" % (cm(c, u), USE), cm(r, u),
                       [cm(2 * r, u), cmz(c / 2, u), cmz(c * PI, u)],
                       "d = C ÷ π ≈ %s ÷ 3.14 = %s. r = %s ÷ 2 = <b>%s</b>. Or r = C ÷ 6.28 in one step."
                       % (N(c), N(2 * r), N(2 * r), cm(r, u))))
    for c, u, want, p in [(50, "cm", "d", 1), (80, "m", "d", 1), (30, "cm", "r", 1), (45, "cm", "r", 2),
                          (22, "m", "d", 2), (120, "cm", "r", 1)]:
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
def money(x):
    return "$" + format(rnd(Dm(x), 2), "f")


def set_problems():
    its = []
    # 1 bike wheel, one turn
    d = Dm(62)
    its.append(mcq("Noah’s bike wheel has a diameter of 62 cm. How far does the bike move in one full turn of the wheel?" + USE,
                   cm(PI * d), [cm(PI * d / 2), cm(2 * PI * d), cm(PI * 31 * 31)],
                   "One turn rolls out the circumference. C = πd ≈ 3.14 × 62 = <b>194.68 cm</b>."))
    # 2 500 turns in metres
    assert 500 * Dm("194.68") == Dm("97340")
    its.append(mcq("Noah’s wheel moves 194.68 cm in one turn. How many metres does the bike move in 500 turns?",
                   "973.4 m", ["97.34 m", "9734 m", "9.734 m"],
                   "500 × 194.68 cm = 97" + NB + "340 cm. 100 cm = 1 m, so 97" + NB + "340 ÷ 100 = <b>973.4 m</b>."))
    # 3 turns for 2 km
    c = PI * 50
    assert rnd(200000 / c, 0) == 1274 and Dm(200000) / 50 == 4000
    assert rnd(200000 / (PI * 25), 0) == 2548 and rnd(200000 / (2 * PI * 50), 0) == 637
    its.append(mcq("Ethan rides 2 km on the Martin Goodman Trail in Toronto. His wheels have a diameter of 50 cm. "
                   "About how many full turns does each wheel make? (2 km = 200" + NB + "000 cm)" + USE,
                   "about 1274", ["about 4000", "about 2548", "about 637"],
                   "C = πd ≈ 3.14 × 50 = 157 cm. 200" + NB + "000 ÷ 157 ≈ 1273.9, so <b>about 1274</b> turns. "
                   "Dividing by 50 forgets π."))
    # 4 round table area
    its.append(mcq("A round table in the school library is 1.5 m across. What is the area of the tabletop, "
                   "to the nearest hundredth?" + USE,
                   cm(PI * Dm("0.5625"), "m²", 2), [cm(PI * Dm("2.25"), "m²", 2), cm(PI * Dm("1.5"), "m²", 2),
                                                     cm(PI * Dm("0.75"), "m²", 2)],
                   "1.5 m across is the diameter, so r = 0.75 m. r² = 0.5625. "
                   "A = πr² ≈ 3.14 × 0.5625 = 1.76625 ≈ <b>1.77 m²</b>."))
    # 5 round table trim
    its.append(mcq("Olivia glues ribbon around the edge of the same round table, 1.5 m across. "
                   "How much ribbon does she need, to the nearest tenth of a metre?" + USE,
                   cm(PI * Dm("1.5"), "m", 1), [cm(PI * Dm("0.75"), "m", 1), cm(2 * PI * Dm("1.5"), "m", 1),
                                                cm(PI * Dm("0.5625"), "m", 1)],
                   "The edge is the circumference. C = πd ≈ 3.14 × 1.5 = 4.71 ≈ <b>4.7 m</b>."))
    # 6 garden fence
    r = Dm("2.5")
    its.append(mcq("A circular garden at a school in Hamilton has a radius of 2.5 m. "
                   "How long is a fence that goes all the way around it?" + USE,
                   cm(2 * PI * r, "m"), [cm(PI * r, "m"), cmz(PI * r * r, "m"), cm(4 * PI * r, "m")],
                   "The fence is the circumference. d = 5 m, so C = πd ≈ 3.14 × 5 = <b>15.7 m</b>."))
    # 7 garden area
    its.append(mcq("The same circular garden has a radius of 2.5 m. What area does it cover, to the nearest hundredth?" + USE,
                   cm(PI * r * r, "m²", 2), [cm(2 * PI * r, "m²", 2), cm(PI * 25, "m²", 2), cm((PI * r) ** 2, "m²", 2)],
                   "r² = 2.5 × 2.5 = 6.25. A = πr² ≈ 3.14 × 6.25 = 19.625 ≈ <b>19.63 m²</b>."))
    # 8 fencing cost
    c = 2 * PI * 3
    assert c == Dm("18.84")
    its.append(mcq("Aiden puts a fence around a circular garden with a radius of 3 m. The fencing costs $15 per metre. "
                   "How much does the fencing cost?" + USE,
                   money(c * 15), [money(PI * 3 * 15), money(2 * PI * 6 * 15), money(c + 15)],
                   "C = 2πr ≈ 2 × 3.14 × 3 = 18.84 m. Cost = 18.84 × $15 = <b>%s</b>." % money(c * 15)))
    # 9 mulch bags
    a = PI * 9
    assert a == Dm("28.26") and a / 3 > 9 and a / 3 < 10
    assert 9 > (2 * PI * 3) / 3 > 6 and 37 < PI * 36 / 3 < 38
    its.append(mcq("A circular flower bed has a diameter of 6 m. One bag of mulch covers 3 m². "
                   "How many bags does Amira need to cover the whole bed?" + USE,
                   "10 bags", ["9 bags", "7 bags", "38 bags"],
                   "r = 3 m. A = πr² ≈ 3.14 × 9 = 28.26 m². 28.26 ÷ 3 = 9.42, so 9 bags are not quite enough. "
                   "She needs <b>10 bags</b>."))
    # 10 tree trunk
    c = Dm("2.826")
    its.append(mcq("Owen wraps a rope around a white pine trunk in Algonquin Park. The rope measures 2.826 m. "
                   "What is the diameter of the trunk?" + USE,
                   cm(c / PI, "m"), [cm(c / PI / 2, "m"), cmz(c * PI, "m"), cm(c / 2, "m")],
                   "The rope measures the circumference. d = C ÷ π ≈ 2.826 ÷ 3.14 = <b>0.9 m</b>."))
    # 11 sprinkler
    its.append(mcq("A lawn sprinkler waters a circle with a radius of 6 m. What area of grass does it water?" + USE,
                   cm(PI * 36, "m²"), [cm(2 * PI * 6, "m²"), cm(PI * 144, "m²"), cm(PI * 6, "m²")],
                   "A = πr² ≈ 3.14 × 36 = <b>113.04 m²</b>. 37.68 is the circumference, not the area."))
    # 12 trampoline net
    d = Dm("4.2")
    its.append(mcq("A round trampoline has a diameter of 4.2 m. A safety net goes all the way around the edge. "
                   "How long is the net, to the nearest tenth of a metre?" + USE,
                   cm(PI * d, "m", 1), [cm(PI * d / 2, "m", 1), cm(PI * Dm("2.1") ** 2, "m", 1), cm(2 * PI * d, "m", 1)],
                   "C = πd ≈ 3.14 × 4.2 = 13.188 ≈ <b>13.2 m</b>."))
    # 13 pizza
    assert PI * 324 > 2 * PI * 144
    its.append(mcq("Which gives more pizza: one round pizza 36 cm across, or two round pizzas 24 cm across?" + USE,
                   "one 36 cm pizza", ["two 24 cm pizzas", "they are the same", "you can’t tell"],
                   "36 cm pizza: r = 18, A ≈ 3.14 × 324 = 1017.36 cm². Two 24 cm pizzas: r = 12, "
                   "A ≈ 2 × 452.16 = 904.32 cm². So <b>one 36 cm pizza</b> gives more, even though 24 + 24 &gt; 36."))
    # 14 face-off circle line
    r = Dm("4.5")
    its.append(mcq("A face-off circle on the ice at an arena in Sudbury has a radius of 4.5 m. "
                   "How long is the painted red line around it?" + USE,
                   cm(2 * PI * r, "m"), [cm(PI * r, "m"), cmz(PI * r * r, "m"), cm(4 * PI * r, "m")],
                   "d = 2 × 4.5 = 9 m. C = πd ≈ 3.14 × 9 = <b>28.26 m</b>."))
    # 15 face-off circle area
    its.append(mcq("The face-off circle has a radius of 4.5 m. What area of ice is inside it, to the nearest tenth?" + USE,
                   cm(PI * r * r, "m²", 1), [cm(PI * 81, "m²", 1), cm(2 * PI * r, "m²", 1), cm((PI * r) ** 2, "m²", 1)],
                   "r² = 4.5 × 4.5 = 20.25. A = πr² ≈ 3.14 × 20.25 = 63.585 ≈ <b>63.6 m²</b>. "
                   "Using d = 9 m in πr² gives 254.3 m², 4 times too much."))
    # 16 pond path
    c = 2 * PI * 40
    assert c == Dm("251.2")
    its.append(mcq("A circular path around a pond in an Ottawa park has a radius of 40 m. Chloe walks around it 4 times. "
                   "How far does she walk?" + USE,
                   cm(4 * c, "m"), [cm(4 * PI * 40, "m"), cm(c, "m"), cm(4 * PI * 1600, "m")],
                   "One lap: C = 2πr ≈ 2 × 3.14 × 40 = 251.2 m. Four laps: 4 × 251.2 = <b>1004.8 m</b>."))
    # 17 stump radius
    c = Dm("1.884")
    its.append(mcq("The edge of a round tree stump at the cottage measures 1.884 m around. What is the radius of the stump?" + USE,
                   cm(c / (2 * PI), "m"), [cm(c / PI, "m"), cm(c / 2, "m"), cmz(c * PI, "m")],
                   "d = C ÷ π ≈ 1.884 ÷ 3.14 = 0.6 m. r = 0.6 ÷ 2 = <b>0.3 m</b>."))
    # 18 drum
    its.append(mcq("Maya’s hand drum has a round top 50 cm across. What is the area of the drum’s top?" + USE,
                   cm(PI * 625, "cm²"), [cm(2 * PI * 25, "cm²"), cm(PI * 2500, "cm²"), cm(PI * 25, "cm²")],
                   "50 cm across is the diameter, so r = 25 cm. A = πr² ≈ 3.14 × 625 = <b>1962.5 cm²</b>."))
    # 19 circle vs square
    assert PI * 12 > 36
    its.append(mcq("Which is longer: the circumference of a circle with a diameter of 12 cm, or the perimeter of a square "
                   "with 9 cm sides?" + USE,
                   "the circle’s circumference", ["the square’s perimeter", "they are the same", "you can’t tell"],
                   "Circle: C ≈ 3.14 × 12 = 37.68 cm. Square: P = 4 × 9 = 36 cm. "
                   "<b>The circle’s circumference</b> is longer by 1.68 cm."))
    # 20 Ferris wheel
    d = Dm(24)
    its.append(mcq("A Ferris wheel at the Canadian National Exhibition (CNE) in Toronto has a diameter of 24 m. "
                   "How far does a seat travel in one full turn?" + USE,
                   cm(PI * d, "m"), [cm(PI * 12, "m"), cm(2 * PI * d, "m"), cm(PI * 144, "m")],
                   "The seat travels the circumference. C = πd ≈ 3.14 × 24 = <b>75.36 m</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: wheels, tables, gardens and rinks", "items": its}


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
        "<p>The <b>centre</b> is the middle point. A <b>radius</b> (r) joins the centre to the edge. "
        "A <b>diameter</b> (d) goes all the way across through the centre. "
        "The <b>circumference</b> (C) is the distance around the circle: its perimeter.</p>"
        "<figure class='sn-fig'>" + parts_lesson_svg() +
        "<figcaption>A diameter is two radii: d = 2r and r = d ÷ 2.</figcaption></figure>"
        "<h2>Circumference: C = πd = 2πr</h2>"
        "<p>Measure any circle: C ÷ d is always the same number. It is called <b>π</b> (pi). π = 3.14159…, "
        "and in these worksheets we use <b>π ≈ 3.14</b>. So the circumference is a little more than 3 diameters, "
        "or a little more than 6 radii.</p>"
        "<figure class='sn-fig'>" + unroll_svg() +
        "<figcaption>Roll a circle out flat: its edge is 3 diameters and a little more.</figcaption></figure>"
        + ex("Example 1", "A bike wheel has a diameter of 70 cm. How far does it roll in one turn?",
             "C = πd ≈ 3.14 × 70 = 219.8", "219.8 cm")
        + ex("Example 2", "A circle has a radius of 4 m. Find its circumference.",
             "d = 2 × 4 = 8 m. C = πd ≈ 3.14 × 8 = 25.12", "25.12 m")
        + "<h2>Area: A = πr²</h2>"
        "<p>Square the radius, then multiply by π. The circle covers about 3.14 squares of side r. "
        "Area is in square units, such as cm² or m².</p>"
        "<figure class='sn-fig'>" + area_lesson_svg() +
        "<figcaption>The square on the radius has area r². The circle is about 3.14 of these squares.</figcaption></figure>"
        + ex("Example 3", "A round table has a diameter of 1.6 m. Find the area of its top.",
             "r = 1.6 ÷ 2 = 0.8 m. r² = 0.64. A = πr² ≈ 3.14 × 0.64 = 2.0096", "about 2.01 m²")
        + "<h2>Working backwards</h2>"
        "<p>If you know the circumference, divide by π to get the diameter: d = C ÷ π. "
        "Then halve it for the radius, or divide C by 2π (about 6.28) in one step.</p>"
        + ex("Example 4", "A tree trunk is 2.198 m around. Find its radius.",
             "d = C ÷ π ≈ 2.198 ÷ 3.14 = 0.7 m. r = 0.7 ÷ 2 = 0.35", "0.35 m")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the diameter in A = πr²", "Halve d first: r = d ÷ 2"],
            ["C = πr", "C = 2πr (or C = πd)"],
            ["Squaring π: (3.14 × 5)²", "Square only r: 3.14 × 5²"],
            ["Mixing up C and A", "C is a length (m); A is an area (m²)"],
            ["Multiplying C by π to find d", "Divide: d = C ÷ π"],
        ])
    )


FAQ = [
    {"q": "When do Ontario students learn the area of a circle?",
     "a": "In Grade 7. The Ontario math curriculum (Spatial Sense, E2.3 and E2.5) has students find the circumference with C = πd and develop and use A = πr²."},
    {"q": "What is the difference between circumference and area?",
     "a": "Circumference is the distance around a circle, measured in units like cm or m. Area is the space inside it, measured in square units like cm² or m²."},
    {"q": "What value of π should Grade 7 students use?",
     "a": "Most Grade 7 work uses π ≈ 3.14 or the π key on a calculator. These worksheets use 3.14, so every answer can be checked by hand."},
    {"q": "How do you find the radius if you know the circumference?",
     "a": "Divide the circumference by π to get the diameter, then halve it. For example, C = 31.4 cm gives d = 31.4 ÷ 3.14 = 10 cm and r = 5 cm."},
]


def gen():
    r = random.Random(47818)
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "circles", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Circles: Circumference and Area",
        "seo_title": "Grade 7 Circles Worksheets: Circumference and Area, Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Circles",
        "domain": "Spatial Sense",
        "standard_code": "Grade 7: E2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Demonstrate an understanding of the inter-relationships between the radius, diameter, and area of a circle, and use the relationships to develop the formula for the area of a circle, and solve related problems",
        "meta_desc": "Free Grade 7 math worksheets on circles for the Ontario curriculum: radius and diameter, circumference C = πd = 2πr, area A = πr² and finding the radius or diameter from the circumference, with wheel, table, garden and hockey rink problems. 100 questions with an answer key.",
        "key_big": "Circumference C = πd = 2πr. Area A = πr². Use π ≈ 3.14.",
        "key_sub": "The diameter is 2 radii, so halve d before you use A = πr². C = πr is missing the 2. C is a length (cm); A is in square units (cm²).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
