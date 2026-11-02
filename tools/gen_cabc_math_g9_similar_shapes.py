# -*- coding: utf-8 -*-
"""
BC Grade 9 Math: Similar Shapes and Scale Diagrams (BC Mathematics Curriculum, Geometry and measurement:
spatial proportional reasoning)
  python3 tools/gen_cabc_math_g9_similar_shapes.py
Helpers adapted from gen_caon_math_g8_scale_drawings.py; all wording written for BC.
Sets: similar figures and scale factor, missing sides in similar triangles, scale diagrams
(enlargements and reductions), maps and plans, word problems (shadows and heights).
Wrong answers come from real mistakes: adding instead of multiplying, matching the wrong sides,
dividing by the scale factor instead of multiplying, and unit slips (cm, m, km).
Every answer is checked with fractions.Fraction (never float). Every figure is drawn to its numbers.
Canadian English, metric units, SI number spacing (no-break space). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
SLUG = "similar-shapes-and-scale-diagrams"
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#cfe6d6"
FILL2 = "#dbe7f6"
LINE = "#2b2b2b"
THIN = "#a0a0a0"
RED = "#c0392b"
BLUE = "#2f6fc0"
GREEN = "#2e7d4f"
BROWN = "#8a5a2b"
FONT = "Arial, Helvetica, sans-serif"
SQ = "²"
X = "<i>x</i>"
XS = "<tspan font-style='italic'>x</tspan>"  # inside SVG (an <i> tag would break the SVG)


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 18000 -> '18 000' (no-break space)."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def nice(x, places=2):
    """True when x is positive and has at most `places` decimal places."""
    x = F(x)
    return x > 0 and (x * 10 ** places).denominator == 1


def kt(x):
    """A scale factor as text: a decimal when it ends, otherwise a fraction."""
    x = F(x)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return num(x) if d == 1 else fr(x.numerator, x.denominator)


def L(x, u):
    return "%s %s" % (num(x), u)


def A(x, u):
    return "%s %s%s" % (num(x), u, SQ)


def R(a, b):
    return "%s:%s" % (num(a), num(b))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")
RAT = re.compile(r"^(\d[\d" + NBSP + r"]*(?:\.\d+)?):(\d[\d" + NBSP + r"]*(?:\.\d+)?)$")
NUM = re.compile(r"^(\d[\d" + NBSP + r"]*(?:\.\d+)?)( .+)?$")
UNIT = {"mm": F(1, 10), "cm": F(1), "m": F(100), "km": F(100000),
        "mm²": F(1, 100), "cm²": F(1), "m²": F(10000)}


def val(c):
    """(number, unit) of a choice, or None when it is not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "")
    m = RAT.match(c)
    if m:
        return (F(m.group(1).replace(NBSP, "")) / F(m.group(2).replace(NBSP, "")), "ratio")
    m = NUM.match(c)
    if not m:
        return None
    return (F(m.group(1).replace(NBSP, "")), (m.group(2) or "").strip())


def norm(c):
    """Value in base units, so that 300 m and 0.3 km count as the same value."""
    v = val(c)
    if v is None:
        return None
    if v[1] in UNIT:
        return (v[0] * UNIT[v[1]], "area" if SQ in v[1] else "len")
    return v


def mcq(q, right, wrong, e, value=None):
    """Correct answer first + 3 wrong; balance() moves it. No two choices equal in value.
    value: the exact answer (number before its unit), checked against the correct choice."""
    right = str(right)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [right] + wrong
    assert len(set(plain(x) for x in ch)) == 4, (q, ch)
    if value is not None:
        v = val(right)
        assert v is not None and v[0] == F(value), (q, right, value)
    known = [n for n in (norm(x) for x in ch) if n is not None]
    assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ svg helpers
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def tw(t, fs):
    """Rough width of bold Arial text."""
    return len(plain(t)) * fs * 0.62


class Canvas:
    """Collects SVG parts with their bounding boxes; wrap() shifts everything to a 0 0 W H viewBox."""

    def __init__(self):
        self.parts = []
        self.box = [1e9, 1e9, -1e9, -1e9]

    def grow(self, x0, y0, x1, y1):
        b = self.box
        self.box = [min(b[0], x0), min(b[1], y0), max(b[2], x1), max(b[3], y1)]

    def add(self, svg, pts):
        self.parts.append(svg)
        for (x, y) in pts:
            self.grow(x, y, x, y)

    def line(self, x1, y1, x2, y2, col=LINE, w=2.0, dash=None):
        d = " stroke-dasharray='%s'" % dash if dash else ""
        self.add("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f'%s stroke-linecap='round'/>"
                 % (x1, y1, x2, y2, col, w, d), [(x1 - w, y1 - w), (x2 + w, y2 + w), (x1 + w, y1 + w), (x2 - w, y2 - w)])

    def poly(self, pts, fill, col=LINE, w=2.2):
        self.add("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%.1f' stroke-linejoin='round'/>"
                 % (" ".join("%.1f,%.1f" % p for p in pts), fill, col, w),
                 [(x + dx, y + dy) for (x, y) in pts for dx in (-w, w) for dy in (-w, w)])

    def rect(self, x, y, w, h, fill, col=LINE, sw=2.2):
        self.add("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                 % (x, y, w, h, fill, col, sw), [(x - sw, y - sw), (x + w + sw, y + h + sw)])

    def text(self, x, y, t, fs=15, anchor="middle", col=LINE, weight=700):
        """y is the baseline."""
        w = tw(t, fs)
        x0 = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
        t = t.replace(X, XS)
        self.add("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
                 % (x, y, fs, weight, col, anchor, t), [(x0, y - fs * 0.78), (x0 + w, y + fs * 0.22)])

    def ctext(self, cx, cy, t, fs=15, col=LINE, weight=700):
        """Text centred on (cx, cy)."""
        self.text(cx, cy + fs * 0.35, t, fs, "middle", col, weight)

    def wrap(self, label, pad=4):
        x0, y0, x1, y1 = self.box
        W, H = int(math.ceil(x1 - x0 + 2 * pad)), int(math.ceil(y1 - y0 + 2 * pad))
        return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
                "aria-label='%s'><g font-family='%s' transform='translate(%.1f %.1f)'>%s</g></svg>"
                % (W, H, W, H, label, FONT, pad - x0, pad - y0, "".join(self.parts)))


def side_label(cv, U, V, G, t, col=BLUE, fs=15):
    """Label the segment UV on the side away from the point G."""
    mx, my = (U[0] + V[0]) / 2, (U[1] + V[1]) / 2
    dx, dy = V[0] - U[0], V[1] - U[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    if (mx - G[0]) * nx + (my - G[1]) * ny < 0:
        nx, ny = -nx, -ny
    w = tw(t, fs)
    off = 5 + abs(nx) * w / 2 + abs(ny) * fs * 0.55
    cv.ctext(mx + nx * off, my + ny * off, t, fs, col)


def vertex_label(cv, P, G, t, fs=15):
    dx, dy = P[0] - G[0], P[1] - G[1]
    n = math.hypot(dx, dy)
    cv.ctext(P[0] + dx / n * 14, P[1] + dy / n * 14, t, fs, LINE)


def tri_points(s):
    """Sides (base AB, right BC, left CA) -> A, B, C with A at the origin, y up."""
    c, a, b = [float(v) for v in s]
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(b * b - x * x)
    return [(0.0, 0.0), (c, 0.0), (x, y)]


def draw_tri(cv, s, px, ox, oy, labels, verts=None, flip=False, fill=FILL):
    """Draw triangle with sides s at px pixels per unit; base on y = oy, left end at ox."""
    pts = tri_points(s)
    base = pts[1][0]
    xs = [p[0] for p in pts]
    lo = min(xs)
    sc = []
    for (x, y) in pts:
        xx = (base - x) if flip else x
        lo2 = (base - max(xs)) if flip else lo
        sc.append((ox + (xx - lo2) * px, oy - y * px))
    cv.poly(sc, fill)
    G = (sum(p[0] for p in sc) / 3, sum(p[1] for p in sc) / 3)
    A_, B_, C_ = sc
    for (U, V), t in zip(((A_, B_), (B_, C_), (C_, A_)), labels):
        if t:
            side_label(cv, U, V, G, t)
    if verts:
        for P, t in zip(sc, verts):
            vertex_label(cv, P, G, t)
    return max(p[0] for p in sc)


def tri_pair_svg(p, q, labP, labQ, vP=None, vQ=None, flipQ=False, label="similar triangles"):
    big = max(max(tri_points(p)[2][1], 0), max(tri_points(q)[2][1], 0))
    wide = max(max(p), max(q))
    px = min(118.0 / big, 150.0 / wide)
    cv = Canvas()
    right = draw_tri(cv, p, px, 0, 0, labP, vP)
    draw_tri(cv, q, px, right + 64, 0, labQ, vQ, flip=flipQ, fill=FILL2)
    return cv.wrap(label)


def lab(v, u):
    return "%s %s" % (num(v), u)


def nested_svg(AB, AC, BC, t, labs, show_vertices=True):
    """Triangle ABC (A at the top) with DE parallel to BC, AD = t × AB.
    labs: dict with keys AD, DB, DE, BC (text or None)."""
    # B at origin, C on the base; A from AB and AC
    c = float(BC)
    x = (AB * AB + c * c - AC * AC) / (2 * c)
    y = math.sqrt(AB * AB - x * x)
    px = min(150.0 / y, 210.0 / c)
    Bp = (0.0, 0.0)
    Cp = (c * px, 0.0)
    Ap = (x * px, -y * px)
    Dp = (Ap[0] + t * (Bp[0] - Ap[0]), Ap[1] + t * (Bp[1] - Ap[1]))
    Ep = (Ap[0] + t * (Cp[0] - Ap[0]), Ap[1] + t * (Cp[1] - Ap[1]))
    cv = Canvas()
    cv.poly([Ap, Bp, Cp], FILL2)
    cv.poly([Ap, Dp, Ep], FILL)
    G = ((Ap[0] + Bp[0] + Cp[0]) / 3, (Ap[1] + Bp[1] + Cp[1]) / 3)
    # parallel marks (arrowheads) on DE and BC
    for (U, V) in ((Dp, Ep), (Bp, Cp)):
        mx = U[0] + 0.68 * (V[0] - U[0])
        my = U[1]
        cv.add("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>"
               % (mx - 6, my - 5, mx, my, mx - 6, my + 5, RED), [(mx - 6, my - 5), (mx, my + 5)])
    if labs.get("AD"):
        side_label(cv, Ap, Dp, G, labs["AD"])
    if labs.get("DB"):
        side_label(cv, Dp, Bp, G, labs["DB"])
    if labs.get("BC"):
        side_label(cv, Bp, Cp, G, labs["BC"])
    if labs.get("DE"):
        # label just under DE, inside the trapezoid
        cv.ctext(Dp[0] + 0.38 * (Ep[0] - Dp[0]), Dp[1] + 14, labs["DE"], 15, BLUE)
    if show_vertices:
        for P, nm in ((Ap, "A"), (Bp, "B"), (Cp, "C")):
            vertex_label(cv, P, G, nm)
        cv.ctext(Dp[0] - 12, Dp[1] - 10, "D", 15)
        cv.ctext(Ep[0] + 12, Ep[1] - 10, "E", 15)
    return cv.wrap("triangle with a line parallel to its base")


def rect_pair_svg(w1, h1, w2, h2, u="cm", labs1=None, labs2=None, label="two rectangles"):
    big = max(h1, h2)
    px = min(100.0 / big, 140.0 / max(w1, w2))
    cv = Canvas()
    labs1 = labs1 or (lab(w1, u), lab(h1, u))
    labs2 = labs2 or (lab(w2, u), lab(h2, u))
    x = 0
    for (w, h, (lw, lh), fill) in ((w1, h1, labs1, FILL), (w2, h2, labs2, FILL2)):
        W, H = w * px, h * px
        cv.rect(x, -H, W, H, fill)
        if lw:
            cv.ctext(x + W / 2, 14, lw, 15, BLUE)
        if lh:
            cv.text(x + W + 6, -H / 2 + 5, lh, 15, "start", BLUE)
        x += W + 6 + (tw(lh, 15) if lh else 0) + 36
    return cv.wrap(label)


def grid_pair_svg(w1, h1, w2, h2):
    """Original and image rectangles on one grid of squares."""
    sq = 18
    cols = w1 + w2 + 3
    rows = max(h1, h2) + 2
    cv = Canvas()
    for i in range(cols + 1):
        cv.line(i * sq, 0, i * sq, rows * sq, THIN, 1)
    for j in range(rows + 1):
        cv.line(0, j * sq, cols * sq, j * sq, THIN, 1)
    x1, x2 = sq, (w1 + 2) * sq
    yb = (rows - 1) * sq
    cv.rect(x1, yb - h1 * sq, w1 * sq, h1 * sq, FILL, LINE, 2.6)
    cv.rect(x2, yb - h2 * sq, w2 * sq, h2 * sq, FILL2, LINE, 2.6)
    cv.ctext(x1 + w1 * sq / 2, rows * sq + 14, "original", 14)
    cv.ctext(x2 + w2 * sq / 2, rows * sq + 14, "image", 14)
    return cv.wrap("grid with an original rectangle and its image")


def scale_bar_svg(cm, amt, unit, parts):
    """Scale bar: `parts` alternating blocks; the whole bar is `cm` cm on the map and stands for `amt` `unit`."""
    labs = [num(F(amt) * i / parts) for i in range(parts + 1)]
    seg = max(44.0 * cm / parts, max(tw(t, 14) for t in labs) + 10)
    cv = Canvas()
    for i in range(parts):
        cv.rect(i * seg, 30, seg, 14, LINE if i % 2 == 0 else "#ffffff", LINE, 1.6)
    for i in range(parts + 1):
        cv.text(i * seg, 22, labs[i], 14, weight=400)
    bw = seg * parts
    cv.text(bw + 8, 42, unit, 15, "start")
    cv.line(0, 58, bw, 58, BLUE, 1.6)
    cv.line(0, 52, 0, 64, BLUE, 1.6)
    cv.line(bw, 52, bw, 64, BLUE, 1.6)
    cv.text(bw / 2, 80, "%s cm" % num(cm), 14, col=BLUE)
    return cv.wrap("scale bar: %s cm stands for %s %s" % (num(cm), num(amt), unit))


def plan_svg(w, h, name):
    """A rectangle on a plan, drawn in proportion, sides labelled in cm."""
    px = 26
    cv = Canvas()
    W, H = w * px, h * px
    cv.rect(0, 0, W, H, FILL)
    cv.ctext(W / 2, H / 2, name, 14, LINE, 400)
    cv.ctext(W / 2, H + 14, "%s cm" % num(w), 15, BLUE)
    cv.text(W + 6, H / 2 + 5, "%s cm" % num(h), 15, "start", BLUE)
    return cv.wrap("plan: rectangle %s cm by %s cm" % (num(w), num(h)))


def shadow_svg(h1, s1, n1, h2, s2, n2, labs, u="m"):
    """Two upright objects and their shadows at the same time of day, drawn at one scale.
    labs: (height1, shadow1, height2, shadow2) texts (None to hide)."""
    px = min(120.0 / max(h1, h2), 210.0 / max(s1, s2))
    cv = Canvas()
    hl1, sl1, hl2, sl2 = labs
    x1 = max(tw(hl1 or "", 15), 8) + 10
    x2 = x1 + s1 * px + max(tw(hl2 or "", 15), 8) + 46
    end = x2 + s2 * px
    cv.line(0, 0, end + 14, 0, LINE, 2)
    for (x, h, s, nm, hl, sl, col) in ((x1, h1, s1, n1, hl1, sl1, BROWN), (x2, h2, s2, n2, hl2, sl2, GREEN)):
        H, S = h * px, s * px
        cv.add("<rect x='%.1f' y='0' width='%.1f' height='5' fill='#7d7d7d'/>" % (x, S), [(x, 0), (x + S, 5)])
        cv.line(x, 0, x + S, 0, "#555555", 5)
        cv.line(x, 0, x, -H, col, 6)
        cv.line(x, -H, x + S, 0, "#c99a00", 1.8, "6 4")
        cv.ctext(x, min(-H - 14, -32), nm, 14, LINE, 400)
        if hl:
            cv.text(x - 8, min(-H / 2 + 5, -6), hl, 15, "end", BLUE)
        if sl:
            cv.ctext(x + S / 2, 20, sl, 15, BLUE)
    return cv.wrap("shadows of %s and %s" % (n1, n2))


# ============================================================ set 1: similar figures and scale factor
def set_factor():
    its = []
    its.append(mcq("Two figures are <b>similar</b>. Which statement is always true?",
                   "Angles are equal; sides are in proportion",
                   ["Sides are equal; angles are in proportion", "Angles and sides are all equal",
                    "Every side is longer by the same amount"],
                   "Similar figures have the same shape: matching angles are <b>equal</b>, and every side is multiplied by the "
                   "<b>same scale factor</b>. Equal sides would make the figures congruent, and adding the same amount changes the shape."))
    its.append(mcq(fig(rect_pair_svg(2, 3, 6, 9)) + "The small rectangle is enlarged to make the large one. What is the scale factor?",
                   "3", ["4", fr(1, 3), "9"],
                   "Scale factor = new length ÷ original length = 6 ÷ 2 = <b>3</b> (check: 9 ÷ 3 = 3). "
                   "4 is the difference 6 − 2, and " + fr(1, 3) + " divides the wrong way.", value=3))
    its.append(mcq(fig(tri_pair_svg((4, 5, 6), (8, 10, 12), ("4 cm", "5 cm", "6 cm"), ("8 cm", "10 cm", "12 cm"))) +
                   "The triangles are similar. What scale factor takes the green triangle to the blue triangle?",
                   "2", ["4", fr(1, 2), "8"],
                   "Matching sides: 8 ÷ 4 = 2, 10 ÷ 5 = 2, 12 ÷ 6 = 2. The scale factor is <b>2</b>. "
                   "4 is the difference 8 − 4, and " + fr(1, 2) + " takes the blue triangle back to the green one.", value=2))
    its.append(mcq(fig(tri_pair_svg((16, 12, 10), (8, 6, 5), ("16 cm", "12 cm", "10 cm"), ("8 cm", "6 cm", "5 cm"))) +
                   "The green triangle is reduced to make the blue triangle. What is the scale factor?",
                   "0.5", ["2", "8", "6"],
                   "Scale factor = new ÷ original = 8 ÷ 16 = <b>0.5</b>. A reduction always has a scale factor less than 1. "
                   "2 divides the wrong way, and 8 and 6 are differences (16 − 8 and 12 − 6), not a factor.", value=F(1, 2)))
    its.append(mcq("A side of a figure is 6 cm long. The figure is enlarged by a scale factor of 3. How long is the new side?",
                   L(18, "cm"), [L(9, "cm"), L(2, "cm"), L(3, "cm")],
                   "Multiply by the scale factor: 6 × 3 = <b>18 cm</b>. 9 cm adds 3, 2 cm divides by 3, and 3 cm subtracts 3.",
                   value=18))
    its.append(mcq("A side is 14 cm long. The figure is reduced by a scale factor of 0.5. How long is the new side?",
                   L(7, "cm"), [L(28, "cm"), L(F(29, 2), "cm"), L(F(27, 2), "cm")],
                   "14 × 0.5 = <b>7 cm</b>. 28 cm divides by 0.5, and 14.5 cm and 13.5 cm add or subtract 0.5.", value=7))
    its.append(mcq("A triangle has angles 50°, 60° and 70°. It is enlarged by a scale factor of 2. "
                   "What is the angle that matches the 60° angle?",
                   "60°", ["120°", "62°", "30°"],
                   "Enlarging changes the side lengths, not the angles. Matching angles are equal, so it is still <b>60°</b>. "
                   "120° doubles the angle, which would make the angle sum 360°, not 180°."))
    its.append(mcq(fig(rect_pair_svg(4, 6, 6, 8)) + "Are these two rectangles similar?",
                   "No: 6 ÷ 4 ≠ 8 ÷ 6", ["Yes: both sides grow by 2 cm", "Yes: the scale factor is 1.5",
                                         "Yes: the scale factor is 2"],
                   "Check the ratios of matching sides: 6 ÷ 4 = 1.5 but 8 ÷ 6 ≈ 1.33. They are not equal, so the rectangles are "
                   "<b>not similar</b>. Adding 2 cm to each side keeps the same difference, not the same shape."))
    its.append(mcq(fig(rect_pair_svg(4, 6, 10, 15)) + "Are these two rectangles similar?",
                   "Yes: the scale factor is 2.5", ["No: the sides grow by different amounts",
                                                    "Yes: the scale factor is 6", "Yes: the scale factor is 9"],
                   "10 ÷ 4 = 2.5 and 15 ÷ 6 = 2.5. The ratios are equal, so the rectangles are <b>similar</b> with scale factor 2.5. "
                   "The sides grow by 6 cm and 9 cm, but similar figures multiply; they do not add."))
    its.append(mcq("Which rectangle is similar to a 3 cm by 5 cm rectangle?",
                   "9 cm by 15 cm", ["5 cm by 7 cm", "6 cm by 8 cm", "6 cm by 15 cm"],
                   "9 ÷ 3 = 3 and 15 ÷ 5 = 3, so <b>9 cm by 15 cm</b> is similar. 5 by 7 and 6 by 8 add to both sides, "
                   "and 6 by 15 multiplies the sides by different numbers (2 and 3)."))
    its.append(mcq("Which triangle is similar to a triangle with sides 3 cm, 4 cm and 5 cm?",
                   "6 cm, 8 cm, 10 cm", ["4 cm, 5 cm, 6 cm", "6 cm, 8 cm, 12 cm", "9 cm, 12 cm, 13 cm"],
                   "Every side must be multiplied by the same number: 3 × 2 = 6, 4 × 2 = 8, 5 × 2 = 10, so "
                   "<b>6 cm, 8 cm, 10 cm</b>. 4, 5, 6 adds 1 to each side; the other two multiply only some sides."))
    its.append(mcq(fig(tri_pair_svg((5, 6, 4), (10, 12, 8), (None, None, None), (None, None, None),
                                    ("A", "B", "C"), ("D", "E", "F"), flipQ=True)) +
                   "△ABC ~ △DEF. Which side matches side AB?",
                   "DE", ["EF", "DF", "BC"],
                   "The order of the letters tells you the match: A ↔ D, B ↔ E, C ↔ F. So AB matches <b>DE</b>. "
                   "The blue triangle is flipped, so do not match sides by where they sit on the page."))
    its.append(mcq("△ABC ~ △DEF. Which angle is equal to ∠B?",
                   "∠E", ["∠D", "∠F", "∠A"],
                   "In △ABC ~ △DEF, the second letters match: B ↔ E. So <b>∠B = ∠E</b>."))
    its.append(mcq("△PQR ~ △STU. Which ratio is equal to " + fr("PQ", "ST") + "?",
                   fr("QR", "TU"), [fr("QR", "SU"), fr("PR", "TU"), fr("PQ", "TU")],
                   "Match the letters in order: P ↔ S, Q ↔ T, R ↔ U. So PQ/ST = QR/TU = PR/SU, and the answer is "
                   "<b>QR/TU</b>. The other ratios pair sides that do not match."))
    its.append(mcq("An original side is 15 cm. The matching side of the image is 6 cm. What is the scale factor?",
                   "0.4", ["2.5", "9", "0.6"],
                   "Scale factor = image ÷ original = 6 ÷ 15 = <b>0.4</b>. 2.5 divides the wrong way, 9 is the difference, "
                   "and 0.6 is 9 ÷ 15 (the difference divided by the original).", value=F(2, 5)))
    its.append(mcq("A side is 9 cm long. The figure is enlarged by a scale factor of 1.5. How long is the new side?",
                   L(F(27, 2), "cm"), [L(F(21, 2), "cm"), L(F(15, 2), "cm"), L(6, "cm")],
                   "9 × 1.5 = <b>13.5 cm</b>. 10.5 cm adds 1.5, 7.5 cm subtracts 1.5, and 6 cm divides by 1.5.",
                   value=F(27, 2)))
    its.append(mcq("A side is 12 cm long. The figure is reduced by a scale factor of " + fr(2, 3) + ". How long is the new side?",
                   L(8, "cm"), [L(18, "cm"), L(4, "cm"), L(36, "cm")],
                   "12 × " + fr(2, 3) + " = 24 ÷ 3 = <b>8 cm</b>. 18 cm divides by " + fr(2, 3) +
                   ", 4 cm finds only " + fr(1, 3) + " of 12, and 36 cm multiplies by 3.", value=8))
    its.append(mcq("A figure is changed with a scale factor of 0.75. What is the new figure?",
                   "A reduction", ["An enlargement", "A congruent copy", "A figure 0.75 cm longer"],
                   "A scale factor between 0 and 1 makes every side shorter, so the image is a <b>reduction</b>. "
                   "A scale factor greater than 1 enlarges, and a scale factor of 1 gives a congruent copy."))
    its.append(mcq("Two triangles are similar with a scale factor of 3. The small triangle has a perimeter of 15 cm. "
                   "What is the perimeter of the large triangle?",
                   L(45, "cm"), [L(18, "cm"), L(24, "cm"), L(135, "cm")],
                   "Every side is multiplied by 3, so the perimeter is too: 15 × 3 = <b>45 cm</b>. "
                   "18 cm adds 3, 24 cm adds 3 to each of the 3 sides, and 135 cm multiplies by 9 (that is for area).",
                   value=45))
    its.append(mcq("A 4 cm by 10 cm rectangle is similar to a 6 cm by " + X + " cm rectangle. The 4 cm side matches the 6 cm side. "
                   "What is " + X + "?",
                   "15", ["12", "2.4", "16"],
                   "Scale factor: 6 ÷ 4 = 1.5. " + X + " = 10 × 1.5 = <b>15</b>. 12 adds 2, 2.4 is 6 × 4 ÷ 10 (sides matched the "
                   "wrong way), and 16 adds 6.", value=15))
    assert len(its) == 20, len(its)
    return {"title": "Similar figures and scale factor", "items": its}


# ============================================================ set 2: missing side in similar triangles
def tri_item(p, k, i, j, flip=False, swap=False, u="cm"):
    """Left triangle P shows all three sides; Q = k × P shows side i and the unknown side j."""
    k = F(k)
    q = [k * F(v) for v in p]
    right = q[j]
    m = 3 - i - j
    labP = [lab(v, u) for v in p]
    labQ = [None, None, None]
    labQ[i] = lab(q[i], u)
    labQ[j] = X
    pool = []
    pool.append((F(p[j]) + q[i] - F(p[i]), "adds %s (the difference %s − %s) instead of multiplying"
                 % (num(abs(q[i] - F(p[i]))), num(max(q[i], F(p[i]))), num(min(q[i], F(p[i]))))
                 if q[i] > p[i] else
                 "subtracts %s (the difference %s − %s) instead of multiplying" % (num(F(p[i]) - q[i]), num(p[i]), num(q[i]))))
    pool.append((k * F(p[m]), "scales the wrong side (%s)" % lab(p[m], u)))
    pool.append((F(p[j]) / k, "divides by the scale factor instead of multiplying"))
    if flip:
        mir = {0: 0, 1: 2, 2: 1}
        pool.append((F(p[mir[j]]) * q[i] / F(p[mir[i]]), "matches sides by their place on the page, not by shape"))
    wrong, why, seen = [], [], {right}
    for v, w in pool:
        if nice(v) and v not in seen and len(wrong) < 3:
            seen.add(v)
            wrong.append(L(v, u))
            why.append("%s %s" % (L(v, u), w))
    assert len(wrong) == 3, (p, k, i, j, pool)
    if swap:
        svg = tri_pair_svg([float(v) for v in q], p, labQ, labP, flipQ=flip)
    else:
        svg = tri_pair_svg(p, [float(v) for v in q], labP, labQ, flipQ=flip)
    q_text = "The triangles are similar. Find " + X + "."
    e = ("Matching sides: %s and %s. Scale factor: %s ÷ %s = %s. %s = %s × %s = <b>%s</b>. "
         % (lab(p[i], u), lab(q[i], u), num(q[i]), num(p[i]), kt(k), X, num(p[j]), kt(k), L(right, u)))
    e += "; ".join(why[:1]) + ", " + why[1] + ", and " + why[2] + "."
    return mcq(fig(svg) + q_text, L(right, u), wrong, e, value=right)


def nested_item(AD, DB, AC, known, kval, u="cm"):
    """Triangle ABC with DE ∥ BC. known = 'DE' (find BC) or 'BC' (find DE)."""
    AD, DB, kval = F(AD), F(DB), F(kval)
    AB = AD + DB
    t = AD / AB
    if known == "DE":
        DE, BC = kval, kval * AB / AD
        right = BC
        pool = [(DE * DB / AD, "matches DE with DB instead of using the whole side AB"),
                (DE + DB, "adds DB instead of multiplying"),
                (DE * AB / DB, "uses DB in place of AD"),
                (DE * AD / AB, "divides by the scale factor")]
        labs = {"AD": lab(AD, u), "DB": lab(DB, u), "DE": lab(DE, u), "BC": X}
        step = "AB = %s + %s = %s. Scale factor: AB ÷ AD = %s ÷ %s. %s = %s × %s ÷ %s = <b>%s</b>." % (
            num(AD), num(DB), num(AB), num(AB), num(AD), X, num(DE), num(AB), num(AD), L(right, u))
    else:
        BC, DE = kval, kval * AD / AB
        right = DE
        pool = [(BC * AD / DB, "matches DE with DB instead of using the whole side AB"),
                (BC - DB, "subtracts DB instead of multiplying"),
                (BC * DB / AB, "uses DB in place of AD"),
                (BC * AB / AD, "multiplies by the wrong ratio")]
        labs = {"AD": lab(AD, u), "DB": lab(DB, u), "DE": X, "BC": lab(BC, u)}
        step = "AB = %s + %s = %s. Scale factor: AD ÷ AB = %s ÷ %s. %s = %s × %s ÷ %s = <b>%s</b>." % (
            num(AD), num(DB), num(AB), num(AD), num(AB), X, num(BC), num(AD), num(AB), L(right, u))
    wrong, why, seen = [], [], {right}
    for v, w in pool:
        if nice(v) and v not in seen and len(wrong) < 3:
            seen.add(v)
            wrong.append(L(v, u))
            why.append("%s %s" % (L(v, u), w))
    assert len(wrong) == 3, (AD, DB, known, pool)
    svg = nested_svg(float(AB), float(AC), float(BC), float(t), labs)
    q = fig(svg) + "DE is parallel to BC, so △ADE ~ △ABC. Find " + X + "."
    e = step + " " + why[0] + ", " + why[1] + ", and " + why[2] + "."
    return mcq(q, L(right, u), wrong, e, value=right)


def set_missing():
    its = []
    its.append(tri_item((6, 5, 4), 2, 0, 1))
    its.append(tri_item((5, 4, 3), 2, 1, 0))
    its.append(tri_item((12, 10, 8), F(1, 2), 0, 2, flip=True))
    its.append(tri_item((4, 6, 5), F(5, 2), 0, 2))
    its.append(tri_item((4, 3, 2), 3, 2, 1, u="m"))
    its.append(tri_item((7, 6, 5), 2, 1, 0, swap=True))
    its.append(mcq("△ABC ~ △DEF. AB = 4 cm, BC = 6 cm and DE = 10 cm. How long is EF?",
                   L(15, "cm"), [L(12, "cm"), L(25, "cm"), L(F(12, 5), "cm")],
                   "AB matches DE, and BC matches EF. Scale factor: 10 ÷ 4 = 2.5. EF = 6 × 2.5 = <b>15 cm</b>. "
                   "12 cm adds 6, 25 cm scales DE instead of BC, and 2.4 cm divides by 2.5.", value=15))
    its.append(tri_item((12, 9, 6), F(2, 3), 0, 1, flip=True))
    its.append(tri_item((10, 8, 6), 2, 2, 1, flip=True))
    its.append(tri_item((6, 4, 3), F(5, 2), 1, 2))
    its.append(nested_item(6, 3, 10, "DE", 8))
    its.append(tri_item((8, 10, 6), F(5, 4), 0, 1, flip=True))
    its.append(tri_item((15, 9, 12), F(2, 3), 0, 2, swap=True))
    its.append(nested_item(5, 10, 13, "DE", 4))
    its.append(mcq("△PQR ~ △STU. PQ = 12 cm, QR = 9 cm and ST = 8 cm. How long is TU?",
                   L(6, "cm"), [L(5, "cm"), L(F(27, 2), "cm"), L(4, "cm")],
                   "PQ matches ST, and QR matches TU. Scale factor: 8 ÷ 12 = " + fr(2, 3) + ". TU = 9 × " + fr(2, 3) +
                   " = <b>6 cm</b>. 5 cm subtracts 4, 13.5 cm multiplies by 1.5 (the wrong way), and 4 cm is 12 − 8.",
                   value=6))
    its.append(tri_item((5, 7, 6), F(7, 5), 0, 1))
    its.append(nested_item(6, 4, 12, "BC", 15))
    its.append(tri_item((16, 12, 8), F(3, 4), 1, 0, flip=True))
    its.append(nested_item(3, 6, 10, "BC", 12))
    its.append(tri_item((10, 7, 5), F(8, 5), 2, 0))
    assert len(its) == 20, len(its)
    return {"title": "Missing sides in similar triangles", "items": its}


# ============================================================ set 3: scale diagrams
def set_diagram():
    its = []
    its.append(mcq("A scale diagram of a ladybug uses a scale factor of 5. The real ladybug is 8 mm long. "
                   "How long is the ladybug in the diagram?",
                   L(40, "mm"), [L(13, "mm"), L(F(8, 5), "mm"), L(3, "mm")],
                   "Diagram length = scale factor × real length = 5 × 8 = <b>40 mm</b>. 13 mm adds 5, 1.6 mm divides by 5, "
                   "and 3 mm subtracts 5.", value=40))
    its.append(mcq(fig(grid_pair_svg(2, 3, 4, 6)) + "What scale factor takes the original to the image?",
                   "2", ["3", fr(1, 2), "4"],
                   "Count squares: the width goes from 2 to 4 and the height from 3 to 6. 4 ÷ 2 = 6 ÷ 3 = <b>2</b>. "
                   "3 is the change in height (6 − 3), " + fr(1, 2) + " divides the wrong way, and 4 is the image width.",
                   value=2))
    its.append(mcq("A scale factor of 2.5 is used to make a scale diagram. What kind of diagram is it?",
                   "An enlargement", ["A reduction", "A congruent copy", "Not similar to the object"],
                   "2.5 is greater than 1, so every length is multiplied by more than 1: the diagram is an <b>enlargement</b>."))
    its.append(mcq("A real feather is 30 cm long. In a scale diagram it is 6 cm long. What is the scale factor?",
                   "0.2", ["5", "24", "0.8"],
                   "Scale factor = diagram length ÷ real length = 6 ÷ 30 = <b>0.2</b>. 5 divides the wrong way, "
                   "24 is the difference, and 0.8 is 24 ÷ 30.", value=F(1, 5)))
    its.append(mcq("A scale diagram of an ant uses a scale factor of 4. The ant is 6 cm long in the diagram. "
                   "How long is the real ant?",
                   L(F(3, 2), "cm"), [L(24, "cm"), L(2, "cm"), L(10, "cm")],
                   "Real length = diagram length ÷ scale factor = 6 ÷ 4 = <b>1.5 cm</b>. 24 cm multiplies, which would make the "
                   "real ant bigger than the enlarged drawing. 2 cm subtracts 4, and 10 cm adds 4.", value=F(3, 2)))
    its.append(mcq("Which scale factor gives a <b>reduction</b>?",
                   "0.8", ["1.2", "8", "1"],
                   "A reduction needs a scale factor between 0 and 1, so <b>0.8</b>. 1.2 and 8 enlarge, and 1 keeps the same size."))
    its.append(mcq("A scale diagram of a hummingbird is 24 cm long. The real bird is 8 cm long. What is the scale factor?",
                   "3", [fr(1, 3), "16", "32"],
                   "Scale factor = 24 ÷ 8 = <b>3</b>. " + fr(1, 3) + " divides the wrong way, 16 is the difference, "
                   "and 32 adds the two lengths.", value=3))
    its.append(mcq("A 9 cm by 12 cm photo is enlarged by a scale factor of 3. What size is the new photo?",
                   "27 cm by 36 cm", ["12 cm by 15 cm", "27 cm by 12 cm", "3 cm by 4 cm"],
                   "Multiply both sides by 3: 9 × 3 = 27 and 12 × 3 = 36, so <b>27 cm by 36 cm</b>. 12 by 15 adds 3, "
                   "27 by 12 enlarges only one side, and 3 by 4 divides by 3."))
    its.append(mcq("To enlarge a 4 cm line to 10 cm, what scale factor is needed?",
                   "2.5", ["6", "0.4", "40"],
                   "Scale factor = 10 ÷ 4 = <b>2.5</b>. 6 is the difference, 0.4 divides the wrong way, and 40 multiplies the lengths.",
                   value=F(5, 2)))
    its.append(mcq(fig(grid_pair_svg(6, 4, 3, 2)) + "What scale factor takes the original to the image?",
                   "0.5", ["2", "3", "0.25"],
                   "Width 6 → 3 and height 4 → 2. 3 ÷ 6 = 2 ÷ 4 = <b>0.5</b>. 2 divides the wrong way, 3 is the change in width, "
                   "and 0.25 multiplies 0.5 by itself.", value=F(1, 2)))
    its.append(mcq("A 20 cm by 30 cm picture is reduced so that the 20 cm side becomes 8 cm. How long does the 30 cm side become?",
                   L(12, "cm"), [L(18, "cm"), L(75, "cm"), L(F(16, 5), "cm")],
                   "Scale factor: 8 ÷ 20 = 0.4. 30 × 0.4 = <b>12 cm</b>. 18 cm subtracts 12 from both sides, 75 cm divides by 0.4, "
                   "and 3.2 cm uses 0.4 twice (8 × 0.4).", value=12))
    its.append(mcq(fig(grid_pair_svg(4, 6, 6, 9)) + "What scale factor takes the original to the image?",
                   "1.5", ["2", fr(2, 3), "3"],
                   "Width 4 → 6 and height 6 → 9: 6 ÷ 4 = 9 ÷ 6 = <b>1.5</b>. 2 and 3 are the changes in width and height, "
                   "and " + fr(2, 3) + " divides the wrong way.", value=F(3, 2)))
    its.append(mcq("A scale diagram of a bee uses a scale factor of 6. The real bee is 1.5 cm long. "
                   "How long is the bee in the diagram?",
                   L(9, "cm"), [L(F(15, 2), "cm"), L(F(1, 4), "cm"), L(90, "cm")],
                   "6 × 1.5 = <b>9 cm</b>. 7.5 cm adds 6, 0.25 cm divides by 6, and 90 cm puts the decimal point in the wrong place.",
                   value=9))
    its.append(mcq("Each 1 cm in a scale diagram stands for 4 cm in real life. What is the scale factor?",
                   "0.25", ["4", "3", "5"],
                   "Scale factor = diagram ÷ real = 1 ÷ 4 = <b>0.25</b>. The diagram is a reduction. 4 divides the wrong way, "
                   "3 is the difference, and 5 adds.", value=F(1, 4)))
    its.append(mcq("A 1.2 m long poster is reduced by a scale factor of " + fr(3, 4) + ". How long is the new poster?",
                   L(F(9, 10), "m"), [L(F(8, 5), "m"), L(F(39, 20), "m"), L(F(9, 20), "m")],
                   "1.2 × " + fr(3, 4) + " = 3.6 ÷ 4 = <b>0.9 m</b>. 1.6 m divides by " + fr(3, 4) + ", 1.95 m adds 0.75, "
                   "and 0.45 m subtracts 0.75.", value=F(9, 10)))
    its.append(mcq("A figure is enlarged by a scale factor of 2. The image is then enlarged by a scale factor of 3. "
                   "What single scale factor takes the original to the final image?",
                   "6", ["5", "1.5", "3"],
                   "Each step multiplies the lengths: 2 × 3 = <b>6</b>. 5 adds the scale factors, 1.5 divides them, "
                   "and 3 uses only the last step.", value=6))
    its.append(mcq("A scale diagram of a plant cell uses a scale factor of 200. The real cell is 0.05 mm across. "
                   "How wide is the cell in the diagram?",
                   L(10, "mm"), [L(F(4001, 20), "mm"), L(F(1, 4000), "mm"), L(100, "mm")],
                   "200 × 0.05 = <b>10 mm</b>. 200.05 mm adds, 0.00025 mm divides by 200, and 100 mm puts the decimal point "
                   "in the wrong place.", value=10))
    its.append(mcq("A scale diagram of a canoe uses a scale factor of 0.02. The canoe is 10 cm long in the diagram. "
                   "How long is the real canoe?",
                   L(5, "m"), [L(F(1, 500), "m"), L(F(1, 2), "m"), L(50, "m")],
                   "Real length = 10 ÷ 0.02 = 500 cm = <b>5 m</b>. 0.002 m multiplies by 0.02 (0.2 cm), "
                   "and 0.5 m and 50 m slip when changing cm to m.", value=5))
    its.append(mcq("A model of a ferry uses a scale factor of " + fr(1, 200) + ". The real ferry is 160 m long. "
                   "How long is the model?",
                   L(80, "cm"), [L(F(4, 5), "cm"), L(8, "cm"), L(32000, "cm")],
                   "160 m = 16" + NBSP + "000 cm. 16" + NBSP + "000 ÷ 200 = <b>80 cm</b>. 0.8 cm and 8 cm slip when changing units, "
                   "and 32" + NBSP + "000 cm multiplies by 200.", value=80))
    its.append(mcq("A 4 cm by 6 cm drawing of a salmon is enlarged so that the 6 cm side becomes 15 cm. "
                   "How long does the 4 cm side become?",
                   L(10, "cm"), [L(13, "cm"), L(F(8, 5), "cm"), L(F(45, 2), "cm")],
                   "Scale factor: 15 ÷ 6 = 2.5. 4 × 2.5 = <b>10 cm</b>. 13 cm adds 9, 1.6 cm divides by 2.5, "
                   "and 22.5 cm matches the sides the wrong way (15 × 6 ÷ 4).", value=10))
    assert len(its) == 20, len(its)
    return {"title": "Scale diagrams: enlargements and reductions", "items": its}


# ============================================================ set 4: maps and plans
def set_maps():
    its = []
    its.append(mcq("A map has the scale 1 cm : 5 km. Two towns are 3 cm apart on the map. How far apart are they?",
                   L(15, "km"), [L(8, "km"), L(F(3, 5), "km"), L(150, "km")],
                   "Each 1 cm stands for 5 km: 3 × 5 = <b>15 km</b>. 8 km adds, 0.6 km divides, and 150 km multiplies by 10 too.",
                   value=15))
    its.append(mcq("A map has the scale 1:50" + NBSP + "000. Two lakes are 4 cm apart on the map. How far apart are they?",
                   L(2, "km"), [L(200, "km"), L(20, "km"), L(F(1, 5), "km")],
                   "4 × 50" + NBSP + "000 = 200" + NBSP + "000 cm = 2000 m = <b>2 km</b>. 200 km reads the centimetres as metres; "
                   "20 km and 0.2 km slip by a factor of 10.", value=2))
    its.append(mcq(fig(scale_bar_svg(4, 20, "km", 4)) + "A road on this map is 6 cm long. How long is the real road?",
                   L(30, "km"), [L(120, "km"), L(24, "km"), L(10, "km")],
                   "The bar shows 4 cm for 20 km, so 1 cm stands for 5 km. 6 × 5 = <b>30 km</b>. 120 km multiplies 6 by the whole "
                   "bar, 24 km multiplies 6 by 4, and 10 km adds 6 and 4.", value=30))
    its.append(mcq("A floor plan has the scale 1:100. A wall is 4.5 cm long on the plan. How long is the real wall?",
                   L(F(9, 2), "m"), [L(450, "m"), L(45, "m"), L(F(9, 20), "m")],
                   "4.5 × 100 = 450 cm = <b>4.5 m</b>. 450 m forgets that the 450 is in centimetres; 45 m and 0.45 m slip by 10.",
                   value=F(9, 2)))
    its.append(mcq("A plan has the scale 1:50. A bed is 4 cm long on the plan. How long is the real bed?",
                   L(2, "m"), [L(200, "m"), L(20, "m"), L(54, "cm")],
                   "4 × 50 = 200 cm = <b>2 m</b>. 200 m forgets to change cm to m, 20 m slips by 10, and 54 cm adds 50.",
                   value=2))
    its.append(mcq("A map has the scale 1 cm : 3 km. Two towns are 18 km apart. How far apart are they on the map?",
                   L(6, "cm"), [L(54, "cm"), L(15, "cm"), L(21, "cm")],
                   "Real to map: divide. 18 ÷ 3 = <b>6 cm</b>. 54 cm multiplies, 15 cm subtracts, and 21 cm adds.", value=6))
    its.append(mcq("Write the scale 1 cm : 2 m as a ratio with no units.",
                   "1:200", ["1:2", "1:20", "1:2000"],
                   "Use the same unit for both parts: 2 m = 200 cm, so the scale is <b>1:200</b>. "
                   "1:2 ignores the units, and 1:20 and 1:2000 change the units by the wrong amount."))
    its.append(mcq("Write the scale 1 cm : 1 km as a ratio with no units.",
                   "1:100" + NBSP + "000", ["1:1000", "1:10" + NBSP + "000", "1:1" + NBSP + "000" + NBSP + "000"],
                   "1 km = 1000 m = 100" + NBSP + "000 cm, so 1 cm : 1 km is <b>1:100" + NBSP + "000</b>. "
                   "1:1000 changes km to m but stops there."))
    its.append(mcq(fig(plan_svg(5, 3, "garage")) + "The scale of this plan is 1:200. How long is the longer side of the real garage?",
                   L(10, "m"), [L(1000, "m"), L(100, "m"), L(1, "m")],
                   "5 × 200 = 1000 cm = <b>10 m</b>. 1000 m forgets the cm, and 100 m and 1 m divide by the wrong power of 10.",
                   value=10))
    its.append(mcq(fig(plan_svg(4, 3, "patio")) + "The scale of this plan is 1 cm : 1.5 m. What is the area of the real patio?",
                   A(27, "m"), [A(18, "m"), A(21, "m"), A(12, "m")],
                   "Real sides: 4 × 1.5 = 6 m and 3 × 1.5 = 4.5 m. Area: 6 × 4.5 = <b>27 m²</b>. 18 m² multiplies the plan area "
                   "by 1.5 only once, 21 is the perimeter, and 12 m² is the area on the plan.", value=27))
    its.append(mcq("A city map has the scale 1:20" + NBSP + "000. Two SkyTrain stations are 6 cm apart on the map. "
                   "How far apart are they?",
                   L(F(6, 5), "km"), [L(120, "km"), L(12, "km"), L(F(3, 25), "km")],
                   "6 × 20" + NBSP + "000 = 120" + NBSP + "000 cm = 1200 m = <b>1.2 km</b>. 120 km reads the cm as m; "
                   "12 km and 0.12 km slip by 10.", value=F(6, 5)))
    its.append(mcq("A trail in a park is 750 m long. How long is it on a map with the scale 1:25" + NBSP + "000?",
                   L(3, "cm"), [L(F(3, 10), "cm"), L(30, "cm"), L(300, "cm")],
                   "750 m = 75" + NBSP + "000 cm. 75" + NBSP + "000 ÷ 25" + NBSP + "000 = <b>3 cm</b>. "
                   "The other choices slip by powers of 10 when changing m to cm.", value=3))
    its.append(mcq("A 12 m wall is 6 cm long on a plan. What is the scale of the plan?",
                   "1:200", ["1:2", "1:20", "1:2000"],
                   "12 m = 1200 cm. 6 cm stands for 1200 cm, so 1 cm stands for 1200 ÷ 6 = 200 cm. The scale is <b>1:200</b>. "
                   "1:2 forgets to change m to cm."))
    its.append(mcq("Two towns 15 km apart are 5 cm apart on a map. What is the scale of the map?",
                   "1:300" + NBSP + "000", ["1:3", "1:3000", "1:30" + NBSP + "000"],
                   "15 km = 1" + NBSP + "500" + NBSP + "000 cm. 1" + NBSP + "500" + NBSP + "000 ÷ 5 = 300" + NBSP + "000, "
                   "so the scale is <b>1:300" + NBSP + "000</b>. 1:3 forgets to change km to cm."))
    its.append(mcq(fig(scale_bar_svg(5, 10, "km", 5)) + "A lake on this map is 3.5 cm long. How long is the real lake?",
                   L(7, "km"), [L(35, "km"), L(F(35, 2), "km"), L(F(27, 2), "km")],
                   "The bar shows 5 cm for 10 km, so 1 cm stands for 2 km. 3.5 × 2 = <b>7 km</b>. 35 km multiplies by 10, "
                   "17.5 km multiplies by 5, and 13.5 km adds 3.5 and 10.", value=7))
    its.append(mcq("Two towns are 8 cm apart on a road map with the scale 1:250" + NBSP + "000. How far apart are they?",
                   L(20, "km"), [L(2, "km"), L(200, "km"), L(2000, "km")],
                   "8 × 250" + NBSP + "000 = 2" + NBSP + "000" + NBSP + "000 cm = 20" + NBSP + "000 m = <b>20 km</b>. "
                   "The other choices slip by powers of 10.", value=20))
    its.append(mcq("A house is drawn at four different scales. Which scale makes the <b>largest</b> drawing?",
                   "1:50", ["1:100", "1:200", "1:500"],
                   "At 1:50, 1 cm stands for only 50 cm, so it takes more centimetres to draw the house. "
                   "<b>1:50</b> is the largest drawing; 1:500 is the smallest."))
    its.append(mcq("A wall is 6 cm long on a 1:100 plan. How long is it on a 1:200 plan of the same house?",
                   L(3, "cm"), [L(12, "cm"), L(600, "cm"), L(F(3, 2), "cm")],
                   "Real wall: 6 × 100 = 600 cm. At 1:200: 600 ÷ 200 = <b>3 cm</b>. 12 cm multiplies by 2, "
                   "600 cm is the real length, and 1.5 cm halves twice.", value=3))
    its.append(mcq("A classroom is 9 m long. A student draws it 18 cm long on a plan. What is the scale?",
                   "1:50", ["1:2", "2:1", "1:500"],
                   "9 m = 900 cm. 900 ÷ 18 = 50, so 1 cm stands for 50 cm: <b>1:50</b>. 1:2 ignores the units, "
                   "2:1 divides 18 by 9, and 1:500 slips by 10."))
    its.append(mcq("A hiking map has the scale 1:50" + NBSP + "000. A trail is 4 km long. How long is it on the map?",
                   L(8, "cm"), [L(F(4, 5), "cm"), L(80, "cm"), L(F(25, 2), "cm")],
                   "4 km = 400" + NBSP + "000 cm. 400" + NBSP + "000 ÷ 50" + NBSP + "000 = <b>8 cm</b>. 0.8 cm and 80 cm slip by 10, "
                   "and 12.5 cm divides 50 by 4.", value=8))
    assert len(its) == 20, len(its)
    return {"title": "Maps and plans", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    its.append(mcq(fig(shadow_svg(F(3, 2), 2, "Olivia", 9, 12, "tree", ("1.5 m", "2 m", X, "12 m"))) +
                   "At the same time of day, Olivia (1.5 m tall) casts a 2 m shadow and a tree casts a 12 m shadow. "
                   "How tall is the tree?",
                   L(9, "m"), [L(F(23, 2), "m"), L(16, "m"), L(F(27, 2), "m")],
                   "The sun makes similar triangles. The tree’s shadow is 12 ÷ 2 = 6 times as long, so the tree is "
                   "1.5 × 6 = <b>9 m</b> tall. 11.5 m subtracts 0.5 instead of multiplying, 16 m matches height with shadow "
                   "the wrong way (12 × 2 ÷ 1.5), and 13.5 m adds 1.5 to the shadow.", value=9))
    its.append(mcq(fig(shadow_svg(1, F(8, 5), "metre stick", 8, F(64, 5), "flagpole", ("1 m", "1.6 m", X, "12.8 m"))) +
                   "A metre stick casts a 1.6 m shadow. At the same time, a flagpole casts a 12.8 m shadow. How tall is the flagpole?",
                   L(8, "m"), [L(F(61, 5), "m"), L(F(512, 25), "m"), L(F(69, 5), "m")],
                   "Height ÷ shadow is the same for both: 1 ÷ 1.6. Flagpole: 12.8 ÷ 1.6 = <b>8 m</b>. 12.2 m subtracts 0.6, "
                   "20.48 m multiplies by 1.6 instead of dividing, and 13.8 m adds 1.", value=8))
    its.append(mcq("A 2 m pole casts a 3 m shadow. At the same time, a western red cedar casts a 45 m shadow. "
                   "How tall is the cedar?",
                   L(30, "m"), [L(44, "m"), L(F(135, 2), "m"), L(47, "m")],
                   "Shadow scale factor: 45 ÷ 3 = 15. Height: 2 × 15 = <b>30 m</b>. 44 m subtracts 1, "
                   "67.5 m matches the sides the wrong way (45 × 3 ÷ 2), and 47 m adds 2.", value=30))
    its.append(mcq(fig(shadow_svg(F(9, 5), F(6, 5), "Ryan", 24, 16, "building", ("1.8 m", "1.2 m", "24 m", X))) +
                   "Ryan is 1.8 m tall and casts a 1.2 m shadow. A 24 m building is beside him. "
                   "How long is the building’s shadow?",
                   L(16, "m"), [L(F(117, 5), "m"), L(36, "m"), L(F(126, 5), "m")],
                   "Shadow ÷ height = 1.2 ÷ 1.8 = " + fr(2, 3) + ". Building’s shadow: 24 × " + fr(2, 3) + " = <b>16 m</b>. "
                   "23.4 m subtracts 0.6, 36 m uses height ÷ shadow (the wrong way), and 25.2 m adds 1.2.", value=16))
    its.append(mcq("Ethan’s shadow is 1.2 m long. At the same time, a 3 m pole casts a 2 m shadow. How tall is Ethan?",
                   L(F(9, 5), "m"), [L(F(11, 5), "m"), L(F(4, 5), "m"), L(F(5, 2), "m")],
                   "Height ÷ shadow = 3 ÷ 2 = 1.5. Ethan: 1.2 × 1.5 = <b>1.8 m</b>. 2.2 m adds 1, "
                   "0.8 m divides by 1.5, and 2.5 m is 3 − 0.5.", value=F(9, 5)))
    its.append(mcq(fig(shadow_svg(F(3, 2), F(9, 10), "Liam", 10, 6, "Douglas fir", ("150 cm", "90 cm", X, "6 m"))) +
                   "Liam is 150 cm tall and his shadow is 90 cm long. At the same time, a Douglas fir casts a 6 m shadow. "
                   "How tall is the tree?",
                   L(10, "m"), [L(F(18, 5), "m"), L(F(33, 5), "m"), L(1000, "m")],
                   "Change to one unit: 1.5 m and 0.9 m. Height ÷ shadow = 1.5 ÷ 0.9 = " + fr(5, 3) + ". Tree: 6 × " + fr(5, 3) +
                   " = <b>10 m</b>. 3.6 m uses the ratio upside down, 6.6 m adds 0.6, and 1000 m mixes cm and m.", value=10))
    its.append(mcq("Students make two similar triangles on the bank of the Fraser River to estimate its width. "
                   "In the small triangle, 8 m along the bank matches 40 m in the large triangle. The small triangle’s side "
                   "across is 6 m. How wide is the river (the large triangle’s side across)?",
                   L(30, "m"), [L(38, "m"), L(F(6, 5), "m"), L(48, "m")],
                   "Scale factor: 40 ÷ 8 = 5. Width: 6 × 5 = <b>30 m</b>. 38 m adds 32, 1.2 m divides by 5, "
                   "and 48 m multiplies 6 by 8.", value=30))
    its.append(mcq("A 10 cm by 15 cm photo of an orca is enlarged so the 10 cm side becomes 25 cm. How long is the other side?",
                   L(F(75, 2), "cm"), [L(30, "cm"), L(6, "cm"), L(40, "cm")],
                   "Scale factor: 25 ÷ 10 = 2.5. 15 × 2.5 = <b>37.5 cm</b>. 30 cm adds 15, 6 cm divides by 2.5, "
                   "and 40 cm adds 25 and 15.", value=F(75, 2)))
    its.append(mcq("A model of a BC Ferries ship uses a scale factor of " + fr(1, 250) + ". The model is 64 cm long. "
                   "How long is the real ship?",
                   L(160, "m"), [L(16, "m"), L(F(8, 5), "m"), L(1600, "m")],
                   "Real length = 64 × 250 = 16" + NBSP + "000 cm = <b>160 m</b>. The other choices slip by powers of 10 "
                   "when changing cm to m.", value=160))
    its.append(mcq(fig(shadow_svg(F(8, 5), 2, "Simran", 12, 15, "light pole", ("1.6 m", "2 m", X, "15 m"))) +
                   "Simran is 1.6 m tall and casts a 2 m shadow. A light pole at the soccer field casts a 15 m shadow. "
                   "How tall is the light pole?",
                   L(12, "m"), [L(F(73, 5), "m"), L(F(75, 4), "m"), L(F(83, 5), "m")],
                   "Scale factor: 15 ÷ 2 = 7.5. Height: 1.6 × 7.5 = <b>12 m</b>. 14.6 m subtracts 0.4, 18.75 m matches "
                   "the sides the wrong way (15 × 2 ÷ 1.6), and 16.6 m adds 1.6.", value=12))
    its.append(mcq("A model car is built at a scale of 1:24. The model is 18 cm long. How long is the real car?",
                   L(F(108, 25), "m"), [L(F(3, 4), "cm"), L(42, "cm"), L(F(216, 5), "m")],
                   "18 × 24 = 432 cm = <b>4.32 m</b>. 0.75 cm divides by 24, 42 cm adds 24, and 43.2 m slips by 10.",
                   value=F(108, 25)))
    its.append(mcq("A drawing of a salmon is 12 cm long. It is enlarged for a school mural with a scale factor of 15. "
                   "How long is the salmon on the mural?",
                   L(F(9, 5), "m"), [L(27, "cm"), L(F(4, 5), "cm"), L(18, "m")],
                   "12 × 15 = 180 cm = <b>1.8 m</b>. 27 cm adds 15, 0.8 cm divides by 15, and 18 m slips when changing cm to m.",
                   value=F(9, 5)))
    its.append(mcq("A scale diagram of a snowboard uses a scale factor of " + fr(1, 8) + ". The real snowboard is 152 cm long. "
                   "How long is it in the diagram?",
                   L(19, "cm"), [L(1216, "cm"), L(144, "cm"), L(160, "cm")],
                   "152 × " + fr(1, 8) + " = 152 ÷ 8 = <b>19 cm</b>. 1216 cm multiplies by 8, and 144 cm and 160 cm "
                   "subtract or add 8.", value=19))
    its.append(mcq("On a trail map with the scale 1:50" + NBSP + "000, Owen’s hike near Whistler is 9 cm long. "
                   "He hikes at 3 km per hour. How long does the hike take?",
                   "1.5 hours", ["3 hours", "15 hours", "4.5 hours"],
                   "Distance: 9 × 50" + NBSP + "000 = 450" + NBSP + "000 cm = 4.5 km. Time: 4.5 ÷ 3 = <b>1.5 hours</b>. "
                   "3 hours uses 9 km, 15 hours uses 45 km, and 4.5 is the distance, not the time.", value=F(3, 2)))
    its.append(mcq(fig(shadow_svg(F(6, 5), F(4, 5), "stick", F(9, 5), F(6, 5), "Kai", ("1.2 m", "0.8 m", X, "1.2 m"))) +
                   "A 1.2 m stick casts a 0.8 m shadow. At the same time, Kai’s shadow is 1.2 m long. How tall is Kai?",
                   L(F(9, 5), "m"), [L(F(8, 5), "m"), L(F(4, 5), "m"), L(2, "m")],
                   "Height ÷ shadow = 1.2 ÷ 0.8 = 1.5. Kai: 1.2 × 1.5 = <b>1.8 m</b>. 1.6 m adds 0.4, 0.8 m uses the ratio "
                   "upside down, and 2 m adds 1.2 and 0.8.", value=F(9, 5)))
    its.append(mcq("A wheelchair ramp rises 0.6 m over a horizontal distance of 4.8 m. How high is the ramp 1.6 m from its bottom end?",
                   L(F(1, 5), "m"), [L(F(9, 5), "m"), L(F(3, 5), "m"), L(F(4, 5), "m")],
                   "The small triangle is similar to the whole ramp. Scale factor: 1.6 ÷ 4.8 = " + fr(1, 3) +
                   ". Height: 0.6 × " + fr(1, 3) + " = <b>0.2 m</b>. 1.8 m multiplies by 3, 0.6 m is the full height, "
                   "and 0.8 m halves 1.6 instead of using the scale factor.", value=F(1, 5)))
    its.append(mcq("Nadia is 1.6 m tall and casts a 2 m shadow. At the same time, a tree casts an 8 m shadow. "
                   "How much taller than Nadia is the tree?",
                   L(F(24, 5), "m"), [L(F(32, 5), "m"), L(6, "m"), L(8, "m")],
                   "Tree: 1.6 × (8 ÷ 2) = 6.4 m. Difference: 6.4 − 1.6 = <b>4.8 m</b>. 6.4 m is the tree’s full height, "
                   "6 m is 8 − 2 (shadows subtracted), and 8 m is the tree’s shadow.", value=F(24, 5)))
    its.append(mcq("A 1:100 plan of a school garden shows a vegetable bed 3.5 cm by 2 cm. Wooden edging costs $6 per metre. "
                   "How much does edging for the whole bed cost?",
                   "$66", ["$33", "$42", "$6600"],
                   "Real sides: 3.5 m and 2 m. Perimeter: 2 × (3.5 + 2) = 11 m. Cost: 11 × $6 = <b>$66</b>. "
                   "$33 uses only two sides, $42 multiplies the area 7 m² by $6, and $6600 forgets to change cm to m."))
    its.append(mcq("A photo of Grouse Mountain is 12 cm wide. It is reduced so that it fits a 9 cm wide space. "
                   "The photo was 8 cm tall. How tall is it now?",
                   L(6, "cm"), [L(5, "cm"), L(F(27, 2), "cm"), L(F(27, 4), "cm")],
                   "Scale factor: 9 ÷ 12 = 0.75. 8 × 0.75 = <b>6 cm</b>. 5 cm subtracts 3, 13.5 cm is 9 × 12 ÷ 8 (sides matched "
                   "the wrong way), and 6.75 cm multiplies 9 by 0.75.", value=6))
    its.append(mcq("Two similar triangular sails have matching sides of 2 m and 5 m. The small sail’s longest side is 3.2 m. "
                   "How long is the large sail’s longest side?",
                   L(8, "m"), [L(F(31, 5), "m"), L(F(32, 25), "m"), L(16, "m")],
                   "Scale factor: 5 ÷ 2 = 2.5. 3.2 × 2.5 = <b>8 m</b>. 6.2 m adds 3, 1.28 m divides by 2.5, "
                   "and 16 m multiplies by 5 only.", value=8))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: shadows, heights and models", "items": its}


# ============================================================ lesson
def body_html():
    f_tri = tri_pair_svg((6, 5, 4), (9, 7.5, 6), ("6 cm", "5 cm", "4 cm"), ("9 cm", X, "6 cm"))
    f_sh = shadow_svg(F(3, 2), 2, "student", 9, 12, "tree", ("1.5 m", "2 m", X, "12 m"))
    f_bar = scale_bar_svg(4, 20, "km", 4)
    return (
        "<h2>What makes shapes similar</h2>"
        "<p>Two shapes are <b>similar</b> when they have the same shape but maybe a different size. "
        "Matching angles are <b>equal</b>. Matching sides are in <b>proportion</b>: every side is multiplied by the same number.</p>"
        "<p>That number is the <b>scale factor</b>. Scale factor = new length ÷ original length. "
        "A scale factor greater than 1 is an <b>enlargement</b>. A scale factor between 0 and 1 is a <b>reduction</b>.</p>"
        + ex("Find the scale factor", "A 4 cm side becomes 10 cm. What is the scale factor?",
             "10 ÷ 4 = 2.5. Every other side is also multiplied by 2.5.", "2.5")
        + "<h2>Missing sides in similar triangles</h2>"
        "<p>First match the sides. In △ABC ~ △DEF, the letters match in order: A ↔ D, B ↔ E, C ↔ F. "
        "Then find the scale factor from one known pair, and multiply.</p>"
        "<figure class='sn-fig'>" + f_tri +
        "<figcaption>The 6 cm and 9 cm sides match, so the scale factor is 9 ÷ 6 = 1.5. "
        "<i>x</i> matches the 5 cm side: <i>x</i> = 5 × 1.5 = 7.5 cm.</figcaption></figure>"
        + ex("Use a proportion", "△ABC ~ △DEF. AB = 4 cm, BC = 6 cm and DE = 10 cm. Find EF.",
             "EF ÷ BC = DE ÷ AB, so EF ÷ 6 = 10 ÷ 4. EF = 6 × 2.5.", "15 cm")
        + "<h2>Scale diagrams, maps and plans</h2>"
        "<p>A scale diagram is similar to the real object. Diagram length = scale factor × real length. "
        "To go back to the real length, divide. On a map, 1:50" + NBSP + "000 means 1 cm stands for 50" + NBSP +
        "000 cm, which is 500 m.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>The bar is 4 cm long and stands for 20 km, so 1 cm stands for 5 km. A 6 cm road is 6 × 5 = 30 km.</figcaption></figure>"
        + "<h2>Shadows and heights</h2>"
        "<p>At the same time of day, the sun’s rays make similar right triangles. Height ÷ shadow is the same for every object.</p>"
        "<figure class='sn-fig'>" + f_sh +
        "<figcaption>The tree’s shadow is 12 ÷ 2 = 6 times as long, so the tree is 1.5 × 6 = 9 m tall.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4 cm → 6 cm, so 10 cm → 12 cm (adding 2)", "Multiply: 6 ÷ 4 = 1.5, and 10 × 1.5 = 15 cm"],
            ["Matching sides by where they sit on the page", "Match by the letters (AB ↔ DE) or by the angles"],
            ["Using DB instead of the whole side AB", "In nested triangles, AB = AD + DB"],
            ["Dividing by the scale factor to find the new side", "New side = original × scale factor"],
            ["1:50" + NBSP + "000, so 4 cm is 200" + NBSP + "000 m", "200" + NBSP + "000 cm = 2000 m = 2 km"],
        ])
    )


FAQ = [
    {"q": "What do Grade 9 students learn about similar shapes in BC?",
     "a": "Mathematics 9 in BC includes spatial proportional reasoning: students use scale factors, similar triangles and scale diagrams to find missing lengths, and solve problems with maps, plans and shadows."},
    {"q": "How can you tell if two shapes are similar?",
     "a": "Their matching angles are equal and the ratios of their matching sides are all the same. For rectangles, check that length ÷ length equals width ÷ width."},
    {"q": "How do you find a missing side in similar triangles?",
     "a": "Match the sides, find the scale factor from one known pair (new ÷ original), then multiply the matching side by it. Do not add the difference."},
    {"q": "How do you find the height of a tree with shadows?",
     "a": "Measure a person or stick and its shadow at the same time as the tree’s shadow. Height ÷ shadow is the same for both, so tree height = tree shadow × (person’s height ÷ person’s shadow)."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(59807)
    sets = [set_factor(), set_missing(), set_diagram(), set_maps(), set_problems()]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": SLUG, "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Similar Shapes and Scale Diagrams: Scale Factors, Missing Sides, Maps and Shadows",
        "seo_title": "Grade 9 Similar Shapes and Scale Diagrams Worksheets (BC Math): Free with Answer Key",
        "short_title": "Similar shapes and scale diagrams",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 9: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Spatial proportional reasoning",
        "meta_desc": "Free Grade 9 math worksheets on similar shapes and scale diagrams for the BC curriculum: scale factors, missing sides in similar triangles, enlargements and reductions, maps and plans, and shadow problems. 100 questions with an answer key.",
        "key_big": "Similar shapes have equal angles and proportional sides: multiply every length by the same scale factor. Never add.",
        "key_sub": "Scale factor = new length ÷ original length. Match the sides first: in △ABC ~ △DEF, AB matches DE.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(similar triangles|two rectangles|grid with|shadows|scale bar|triangle with a line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
