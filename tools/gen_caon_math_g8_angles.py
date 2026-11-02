# -*- coding: utf-8 -*-
"""
CA Grade 8 Math: Angle properties
(Ontario Curriculum 2020, Grade 8: Spatial Sense, E2.2)
  python3 tools/gen_caon_math_g8_angles.py
Supplementary and complementary angles, vertically opposite angles, parallel lines cut by a transversal
(corresponding, alternate and co-interior angles), angles in triangles and quadrilaterals (with the exterior
angle of a triangle), and interior angles of polygons: (n − 2) × 180°. Canadian English.
HTML attributes use single quotes (no backslashes in the JSON).

Every figure is drawn to its stated angles: each marked angle is measured from the drawing and checked
against its value (also the "?" and letter angles). Labels are checked so that they do not touch a line,
an arc or another label, and sit inside the angle they name.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


def D(v):
    """Angle in degrees as text: 65°, 1080° (Ontario style: no separator in 4-digit numbers)."""
    assert abs(v - round(v)) < 1e-9 and v < 10000
    return "%d°" % int(round(v))


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c is None or c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q[-80:], correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def dq(q, v, wrong, e, rnd):
    """Degree answer; wrong answers are numbers (mistakes). Negative or zero ones are skipped."""
    return mcq(q, D(v), [D(w) for w in wrong if w > 0 and abs(w - v) > 1e-9], e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


def tw(t, fs, bold=True):
    """Approximate text width (Arial)."""
    w = 0
    for ch in str(t):
        w += 0.4 if ch == "°" else (0.72 if ch.isupper() else 0.6 if ch == "?" else 0.5 if ch.isalpha() else 0.556)
    return w * fs * (1.04 if bold else 1)


# ------------------------------------------------------------ geometry (screen coordinates, y down)
def pol(V, r, deg):
    """Point at distance r from V in direction deg (counterclockwise on screen, 0 = right)."""
    t = math.radians(deg)
    return (V[0] + r * math.cos(t), V[1] - r * math.sin(t))


def ang(V, P):
    return math.degrees(math.atan2(-(P[1] - V[1]), P[0] - V[0])) % 360


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def rot_all(pts, deg, c=(0.0, 0.0)):
    out = []
    for p in pts:
        r, a = dist(c, p), ang(c, p) if dist(c, p) > 1e-12 else 0
        out.append(pol(c, r, a + deg))
    return out


def poly_angles(pts):
    n = len(pts)
    out = []
    for i in range(n):
        a, b = ang(pts[i], pts[i - 1]), ang(pts[i], pts[(i + 1) % n])
        s = (b - a) % 360
        out.append(min(s, 360 - s))
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, "shape must be convex"
    return out


def cross(a, b, c, d):
    """Do segments ab and cd cross?"""
    def o(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def in_poly(p, pts, m=0):
    """Is p inside the convex polygon pts, at least m from every side?"""
    n = len(pts)
    sg = None
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        cr = ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) / dist(a, b)
        if sg is None:
            sg = 1 if sum((pts[(j + 1) % n][0] - pts[j][0]) * (pts[(j + 1) % n][1] + pts[j][1]) for j in range(n)) < 0 else -1
        if cr * sg < m:
            return False
    return True


# ------------------------------------------------------------ drawing kit with checks
class Pic:
    """Strokes are kept as sampled points (for collision checks and the bounding box), labels as boxes.
    Angle marks are measured from the drawing and must equal their stated values."""

    def __init__(self):
        self.el = []          # (z, svg) z: 0 fill, 1 strokes, 2 labels
        self.pts = []
        self.boxes = []
        self.todo = []        # labels to place after every stroke is drawn
        self.segs = []        # straight strokes, for the line-of-sight check

    def line(self, p, q, col=GREEN, sw=3):
        self.el.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                        % (p[0], p[1], q[0], q[1], col, sw)))
        self.segs.append((p, q))
        n = max(2, int(dist(p, q) / 2))
        self.pts.extend([(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)])

    def poly(self, pts, fill=FILL, sw=3):
        self.el.append((0, "<polygon points='%s' fill='%s' stroke='none'/>" % (" ".join("%.1f,%.1f" % p for p in pts), fill)))
        n = len(pts)
        for i in range(n):
            self.line(pts[i], pts[(i + 1) % n], sw=sw)

    def polyline(self, pts, col=INK, sw=1.8):
        self.el.append((1, "<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round' stroke-linecap='round'/>"
                        % (" ".join("%.1f,%.1f" % p for p in pts), col, sw)))
        for i in range(len(pts) - 1):
            p, q = pts[i], pts[i + 1]
            n = max(2, int(dist(p, q) / 2))
            self.pts.extend([(p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n) for k in range(n + 1)])

    def arc(self, V, r, a, b, col=INK, sw=1.8):
        n = max(4, int((b - a) / 3))
        self.polyline([pol(V, r, a + (b - a) * i / n) for i in range(n + 1)], col, sw)

    def dot(self, V, r=3.5):
        self.el.append((1, "<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (V[0], V[1], r, INK)))
        self.pts.extend([(V[0] + r * math.cos(t / 4.0), V[1] + r * math.sin(t / 4.0)) for t in range(26)])

    def ticks(self, p, q, n=1):
        """Equal-side marks across the middle of side pq."""
        d = ang(p, q)
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        for j in range(n):
            c = pol(m, (j - (n - 1) / 2.0) * 5, d)
            self.polyline([pol(c, 6, d + 90), pol(c, 6, d - 90)], INK, 2)

    def mark(self, V, P, Q, val, text=None, kind="arc", r=None, ccw=False, eq=0, inside=None):
        """Mark the angle at V between rays VP and VQ (the smaller one unless ccw: from P counterclockwise to Q).
        val: its true size (checked against the drawing). kind: 'arc' or 'right' (small square).
        eq: number of small dashes across the arc (equal-angle marks)."""
        a, b = ang(V, P), ang(V, Q)
        s = (b - a) % 360
        if not ccw and s > 180:
            a, s = b, 360 - s
        assert abs(s - val) < 1e-6, ("drawing does not match", val, s)
        if kind == "right":
            assert abs(val - 90) < 1e-9
            k = 12
            q1, q3 = pol(V, k, a), pol(V, k, a + 90)
            q2 = (q1[0] + q3[0] - V[0], q1[1] + q3[1] - V[1])
            self.polyline([q1, q2, q3], INK, 1.8)
            r = k * 1.42
        else:
            assert abs(val - 90) > 1e-9 or text, "a right angle needs its square or a label"
            r = r or (15 if val >= 75 else 19 if val >= 40 else 24)
            self.arc(V, r, a, a + s)
            for j in range(eq):
                m = a + s / 2 + (j - (eq - 1) / 2.0) * 7
                self.polyline([pol(V, r - 5, m), pol(V, r + 5, m)], INK, 1.8)
            if eq:
                r += 5
        if text:
            self.todo.append((V, a, s, r, text, min(dist(V, P), dist(V, Q)), inside))

    def box_of(self, cx, cy, t, fs):
        w, h = tw(t, fs), fs * 0.74
        return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

    def clear(self, b, gap=2.5):
        x0, y0, x1, y1 = b[0] - gap, b[1] - gap, b[2] + gap, b[3] + gap
        for p in self.pts:
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                return False
        for o in self.boxes:
            if not (o[2] + gap <= b[0] or b[2] + gap <= o[0] or o[3] + gap <= b[1] or b[3] + gap <= o[1]):
                return False
        return True

    def label(self, cx, cy, t, fs=16, col=INK, check=True, italic=False):
        b = self.box_of(cx, cy, t, fs)
        if check:
            assert self.clear(b), ("label collides", t)
        self.boxes.append(b)
        self.el.append((2, "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700'%s fill='%s' text-anchor='middle'>%s</text>"
                        % (cx, cy + fs * 0.36, fs, " font-style='italic'" if italic else "", col, t)))

    def place(self, V, a, s, r, t, arm, inside=None):
        """Label inside the angle (all four corners in the wedge), just outside its arc, clear of strokes.
        Tries the bisector first, then directions a little to each side."""
        mid = a + s / 2.0
        fs = 16
        rl = r + 5
        while rl < arm:
            for f in (0, 0.12, -0.12, 0.24, -0.24):
                c = pol(V, rl, mid + f * s)
                bx = self.box_of(c[0], c[1], t, fs)
                corners = [(bx[0], bx[1]), (bx[2], bx[1]), (bx[0], bx[3]), (bx[2], bx[3])]
                ok = all(dist(V, p) >= r + 3 and (ang(V, p) - a) % 360 <= s for p in corners)
                if ok and inside:
                    ok = all(in_poly(p, inside, 3) for p in corners)
                if ok:
                    ok = not any(cross(V, cc, p, q) for p, q in self.segs if dist(p, V) > 1 and dist(q, V) > 1 for cc in [c] + corners)
                if ok and self.clear(bx, 3):
                    half = math.hypot(bx[2] - bx[0], bx[3] - bx[1]) / 2
                    assert rl + half <= arm + 6, ("label outside the arms", t, rl, arm)
                    letter = any(ch.isalpha() for ch in t)
                    self.label(c[0], c[1], t, fs, RED if t == "?" else INK, italic=letter)
                    return
            rl += 1
        raise AssertionError("no room for label " + t)

    def svg(self, label, pad=5):
        for item in sorted(self.todo, key=lambda t: -t[2]):
            self.place(*item)
        self.todo = []
        allp = self.pts + [(b[0], b[1]) for b in self.boxes] + [(b[2], b[3]) for b in self.boxes]
        x0 = min(p[0] for p in allp) - pad
        y0 = min(p[1] for p in allp) - pad
        x1 = max(p[0] for p in allp) + pad
        y1 = max(p[1] for p in allp) + pad
        W, H = int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))
        if W == H:
            W += 1                                     # keep out of the larger 'square' print size
        dx, dy = (W - (x1 - x0)) / 2 - x0, (H - (y1 - y0)) / 2 - y0
        body = "".join(s for z, s in sorted(self.el, key=lambda t: t[0]))
        return svg_wrap(W, H, "<g transform='translate(%.1f %.1f)'>%s</g>" % (dx, dy, body), label)


# ------------------------------------------------------------ figures
O = (0.0, 0.0)

def rays_svg(rays, marks, label, L=80, dot=True):
    """Lines from one point O. rays: directions (deg). marks: (from_dir, to_dir, val, text, kind),
    each angle measured counterclockwise from from_dir to to_dir."""
    P = Pic()
    for d in rays:
        P.line(O, pol(O, L, d))
    for a, b, val, t, kind in marks:
        P.mark(O, pol(O, L, a), pol(O, L, b), val, t, kind=kind, ccw=True)
    if dot:
        P.dot(O)
    return P.svg(label)


def line_svg(rot, parts, texts, L=92, label="angles on a straight line"):
    """Straight line through O at direction rot, with rays splitting the top half into parts (deg)."""
    assert abs(sum(parts) - 180) < 1e-9
    rays, marks, d = [rot, rot + 180], [], rot
    for p, t in zip(parts, texts):
        if d != rot:
            rays.append(d)
        marks.append((d, d + p, p, t, "right" if (p == 90 and t is None) else "arc"))
        d += p
    return rays_svg(rays, marks, label, L)


def point_svg(rot, parts, texts, L=80, label="angles around a point"):
    assert abs(sum(parts) - 360) < 1e-9
    rays, marks, d = [], [], rot
    for p, t in zip(parts, texts):
        rays.append(d)
        marks.append((d, d + p, p, t, "right" if (p == 90 and t is None) else "arc"))
        d += p
    return rays_svg(rays, marks, label, L)


def cross_svg(rot, a, texts, L=78, label="two straight lines crossing"):
    """Two straight lines crossing at O: angles a, 180 − a, a, 180 − a counterclockwise from rot.
    texts: 4 labels (None = no mark)."""
    parts = [a, 180 - a, a, 180 - a]
    rays, marks, d = [], [], rot
    for p, t in zip(parts, texts):
        rays.append(d)
        if t is not None:
            marks.append((d, d + p, p, t, "arc"))
        d += p
    return rays_svg(rays, marks, label, L)


def tri_pts(a, b, base=150, rot=0):
    """Triangle with angle a at the left end of the base, b at the right end, apex above."""
    c = 180 - a - b
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    pts = [O, (float(base), 0.0), pol(O, side, a)]
    return rot_all(pts, rot) if rot else pts


def shape_svg(pts, texts, label, rights=(), ticks=(), eqs=(), extra=None, sw=3, split=()):
    """Polygon with angle marks. texts: {corner index: text}. rights: corners with a small square.
    ticks: (side index, number of ticks). eqs: (corner, number of dashes) equal-angle marks without text."""
    P = Pic()
    P.poly(pts, sw=sw)
    A = poly_angles(pts)
    n = len(pts)
    for i in range(n):
        if abs(A[i] - 90) < 1e-6:
            assert i in rights or i in texts or i in split, "unmarked right angle"
    for i, k in ticks:
        P.ticks(pts[i], pts[(i + 1) % n], k)
    for i in rights:
        P.mark(pts[i], pts[i - 1], pts[(i + 1) % n], A[i], kind="right")
    for i, k in eqs:
        P.mark(pts[i], pts[i - 1], pts[(i + 1) % n], A[i], texts.get(i), eq=k, inside=pts)
    for i, t in texts.items():
        if i in [e[0] for e in eqs]:
            continue
        P.mark(pts[i], pts[i - 1], pts[(i + 1) % n], A[i], t, inside=pts)
    if extra:
        extra(P, A)
    return P.svg(label)


def check_tri(pts, want):
    A = poly_angles(pts)
    assert all(abs(x - y) < 1e-6 for x, y in zip(A, want)), (A, want)
    return A


def regular_pts(n, r=62, start=None):
    start = 270 - 180.0 / n if start is None else start          # flat bottom side
    return [pol(O, r, start + 360.0 * i / n) for i in range(n)]


def quad_from(a, b, c, AB=150, BC=90, rot=0):
    """Convex quadrilateral ABCD (counterclockwise) with angles a at A, b at B, c at C; D = 360 − a − b − c."""
    A_ = O
    B_ = (float(AB), 0.0)
    C_ = pol(B_, BC, 180 - b)
    h = 360 - b - c
    # intersect A + t*dir(a) with C + u*dir(h)
    da, dh = pol(O, 1, a), pol(O, 1, h)
    den = da[0] * dh[1] - da[1] * dh[0]
    t = ((C_[0]) * dh[1] - (C_[1]) * dh[0]) / den
    u = ((C_[0]) * da[1] - (C_[1]) * da[0]) / den
    assert t > 0 and u > 0
    D_ = (da[0] * t, da[1] * t)
    pts = [A_, B_, C_, D_]
    if rot:
        pts = rot_all(pts, rot)
    A = poly_angles(pts)
    assert all(abs(x - y) < 1e-6 for x, y in zip(A, [a, b, c, 360 - a - b - c])), A
    for i in range(4):
        assert dist(pts[i], pts[(i + 1) % 4]) > 50, "side too short"
    return pts


def kite_pts(top, bottom, w=58):
    """Kite with its line of symmetry upright: angle top at the top, bottom at the bottom."""
    h1 = w / math.tan(math.radians(top / 2.0))
    h2 = w / math.tan(math.radians(bottom / 2.0))
    pts = [(0.0, h1 + h2), (w, h1), (0.0, 0.0), (-w, h1)]     # bottom, right, top, left (counterclockwise on screen)
    A = poly_angles(pts)
    side = (360 - top - bottom) / 2.0
    assert all(abs(x - y) < 1e-6 for x, y in zip(A, [bottom, side, top, side])), A
    return pts



# ------------------------------------------------------------ Grade 8 figures: parallel lines and a transversal
def chevron(P, at, d, col=INK):
    """Small arrowhead on a line at point at, pointing in direction d (marks parallel lines)."""
    P.polyline([pol(at, 8, d + 180 - 40), at, pol(at, 8, d + 180 + 40)], col, 2.2)


def par_svg(t, texts, gap=80, ext=56, label="two parallel lines cut by a transversal", arrows=True):
    """Two horizontal parallel lines cut by a transversal at angle t (0 < t < 180) to the right-hand side.
    Lower crossing point L = (0, 0), upper crossing point U is gap above it.
    Regions at each point, counterclockwise from the right: 0 = [0, t], 1 = [t, 180], 2 = [180, 180 + t],
    3 = [180 + t, 360]. Sizes: t, 180 − t, t, 180 − t.
    texts: {("U" or "L", region): text}. Each marked angle is checked against the drawing."""
    assert 20 < t < 160 and t != 90
    Lp = (0.0, 0.0)
    Up = (gap / math.tan(math.radians(t)), -float(gap))
    x0 = min(Lp[0], Up[0]) - ext
    x1 = max(Lp[0], Up[0]) + ext
    P = Pic()
    # every line is drawn in pieces that end at the crossing points (the label checks skip strokes through the vertex)
    P.line((x0, 0.0), Lp)
    P.line(Lp, (x1, 0.0))
    P.line((x0, -float(gap)), Up)
    P.line(Up, (x1, -float(gap)))
    P.line(pol(Lp, ext, t + 180), Lp)
    P.line(Lp, Up)
    P.line(Up, pol(Up, ext, t))
    if arrows:
        for y in (0.0, -float(gap)):
            chevron(P, (x1 - 16, y), 0)
    between = dist(Lp, Up)
    dirs = [0, t, 180, 180 + t, 360]
    for (which, k), txt in texts.items():
        V = Up if which == "U" else Lp

        def arm(d):
            d = d % 360
            if abs(d) < 1e-9:
                return x1 - V[0]
            if abs(d - 180) < 1e-9:
                return V[0] - x0
            toward_other = (abs(d - t) < 1e-9) if which == "L" else (abs(d - (t + 180) % 360) < 1e-9)
            return between if toward_other else ext
        a, b = dirs[k], dirs[k + 1]
        val = b - a
        P.mark(V, pol(V, arm(a), a), pol(V, arm(b), b), val, txt, ccw=True)
    return P.svg(label)


def strip_svg(svgs, caps, label, cw=None, fs=15):
    """Several small figures side by side, each with a caption under it."""
    dims = []
    for s in svgs:
        m = re.search(r"viewBox='0 0 (\d+) (\d+)'", s)
        dims.append((int(m.group(1)), int(m.group(2))))
    cw = cw or max(max(w for w, h in dims) + 10, max(tw(c, fs) for c in caps) + 10)
    top = max(h for w, h in dims)
    out = []
    for k, (s, c) in enumerate(zip(svgs, caps)):
        w, h = dims[k]
        assert w <= cw and tw(c, fs) <= cw - 4, (c, w, cw)
        x, y = k * cw + (cw - w) / 2.0, (top - h) / 2.0
        inner = re.sub(r"^<svg [^>]*>", "", s)
        assert inner.endswith("</svg>")
        out.append("<g transform='translate(%.1f %.1f)'>%s</g>" % (x, y, inner[:-6]))
        out.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                   % (k * cw + cw / 2.0, top + fs + 6, fs, INK, c))
    return svg_wrap(int(math.ceil(cw * len(svgs))), top + fs + 12, "".join(out), label)


def mc(q, correct, wrong, e, rnd):
    return mcq(q, correct, wrong, e, rnd)


def mcq_n(q, v, wrong, e, rnd):
    return mcq(q, str(v), [str(w) for w in wrong], e, rnd)


def V(s):
    """The variable x in italics inside HTML text (also in 2x, 3x)."""
    return re.sub(r"(?<![A-Za-z])x(?![A-Za-z])", "<i>x</i>", s)


# ------------------------------------------------------------ set 1: supplementary and complementary angles
def set_supp_comp(rnd, P):
    its = []
    ql = "The angles are on a straight line. Find the missing angle."
    for rot, parts, texts, v, wrong, e in [
        (0, [48, 132], ["48°", "?"], 132, [42, 312, 48],
         "Angles on a straight line are supplementary: they add up to 180°. 180° − 48° = 132°. "
         "(42° comes from using 90°, the rule for complementary angles.)"),
        (15, [115, 65], ["?", "65°"], 115, [25, 295, 65],
         "The line is tilted, but it is still straight, so the angles add up to 180°. 180° − 65° = 115°."),
        (0, [38, 85, 57], ["38°", "?", "57°"], 85, [265, 95, 142],
         "The three angles make a straight line: 180°. 38° + 57° = 95°, and 180° − 95° = 85°. "
         "(95° is the sum of the known angles, not the missing one.)"),
    ]:
        its.append(dq(fig(line_svg(rot, parts, texts)) + ql, v, wrong, e, rnd))
    qr = "The whole angle is a right angle. Find the missing angle."
    for rot, a, first, v, wrong in [(0, 37, True, 53, [143, 323, 37]), (20, 26, False, 26, [116, 64, 296])]:
        b = 90 - a
        marks = [(rot, rot + a, a, "%d°" % a if first else "?", "arc"),
                 (rot + a, rot + 90, b, "?" if first else "%d°" % b, "arc"),
                 (rot, rot + 90, 90, None, "right")]
        known = a if first else b
        its.append(dq(fig(rays_svg([rot, rot + a, rot + 90], marks, "right angle split into two angles", L=96)) + qr,
                      v, wrong,
                      "The two angles are complementary: they add up to 90°. 90° − %s = %s. "
                      "(%s comes from using 180°.)" % (D(known), D(v), D(180 - known)), rnd))
    its.append(dq(fig(line_svg(0, [60, 120], ["x", "2x"], L=100, label="angles x and 2x on a straight line")) +
                  V("The angles are on a straight line. What is the value of x?"), 60, [90, 120, 30],
                  V("x + 2x = 180°, so 3x = 180° and x = 60°. Check: 60° + 120° = 180°. "
                    "(30° comes from 3x = 90°.)"), rnd))
    its.append(dq(fig(rays_svg([0, 35, 90], [(0, 35, 35, "x", "arc"), (35, 90, 55, "x + 20°", "arc"), (0, 90, 90, None, "right")],
                               "right angle split into x and x + 20°", L=112)) +
                  V("The whole angle is a right angle. What is the value of x?"), 35, [80, 45, 55],
                  V("x + x + 20° = 90°, so 2x = 70° and x = 35°. Check: 35° + 55° = 90°. "
                    "(80° comes from using 180°: 2x = 160°.)"), rnd))
    its.append(dq(fig(line_svg(0, [36, 36, 108], ["x", "x", "3x"], L=104, label="angles x, x and 3x on a straight line")) +
                  V("The angles are on a straight line. What is the value of x?"), 36, [60, 45, 72],
                  V("x + x + 3x = 5x = 180°, so x = 180° ÷ 5 = 36°. Check: 36° + 36° + 108° = 180°. "
                    "(60° comes from dividing by 3, the number of angles, not by 5.)"), rnd))
    its.append(dq("What is the complement of 34°?", 56, [146, 34, 326],
                  "Complementary angles add up to 90°. 90° − 34° = 56°. (146° is the supplement: 180° − 34°.)", rnd))
    its.append(dq("What is the supplement of 112°?", 68, [22, 248, 78],
                  "Supplementary angles add up to 180°. 180° − 112° = 68°. "
                  "(22° comes from 112° − 90°, and 248° from 360° − 112°.)", rnd))
    its.append(dq("Two angles are complementary. One is 4 times the other. What is the smaller angle?", 18, [36, 72, 30],
                  "The angles are 1 part and 4 parts: 5 parts = 90°, so 1 part = 18°. The angles are 18° and 72°. "
                  "(36° comes from using 180°.)", rnd))
    its.append(dq("Two angles are supplementary. One is 30° more than the other. What is the larger angle?", 105,
                  [75, 60, 150],
                  "Take away the extra 30°: 180° − 30° = 150°, and 150° ÷ 2 = 75° for the smaller angle. "
                  "The larger angle is 75° + 30° = 105°. Check: 75° + 105° = 180°.", rnd))
    its.append(mc("Which pair of angles is complementary?", "27° and 63°",
                  ["27° and 153°", "45° and 55°", "63° and 117°"],
                  "Complementary angles add up to 90°: 27° + 63° = 90°. 27° and 153° (and 63° and 117°) add up to 180°, "
                  "so they are supplementary.", rnd))
    its.append(mc("Which pair of angles is supplementary?", "104° and 76°",
                  ["14° and 76°", "104° and 86°", "76° and 284°"],
                  "Supplementary angles add up to 180°: 104° + 76° = 180°. 14° + 76° = 90° (complementary), "
                  "104° + 86° = 190° and 76° + 284° = 360°.", rnd))
    n, he, his = P.next()
    its.append(mc("%s says the complement of 40° is 140°. Is %s right?" % (n, he), "No, it is 50°",
                  ["Yes, it is 140°", "No, it is 320°", "No, it is 40°"],
                  "Complementary angles add up to 90°, so the complement is 90° − 40° = 50°. "
                  "140° is the supplement (180° − 40°).", rnd))
    its.append(mc("Can an obtuse angle have a complement?", "No, it is already more than 90°",
                  ["Yes, subtract it from 180°", "Yes, subtract 90° from it", "Only if it is less than 180°"],
                  "Complementary angles add up to 90°. An obtuse angle is more than 90° on its own, so no angle can be added to it to make 90°.", rnd))
    its.append(dq(V("Angles A and B are supplementary. Angle A = 3x and angle B = x + 40°. What is the value of x?"), 35,
                  [45, 140, 55],
                  V("3x + x + 40° = 180°, so 4x + 40° = 180°. 4x = 140°, so x = 35°. "
                    "Check: A = 105° and B = 75°, and 105° + 75° = 180°. (140° is 4x, not x.)"), rnd))
    its.append(dq("An angle and its complement differ by 18°. What is the larger angle?", 54, [36, 99, 72],
                  "The two angles add up to 90°. 90° − 18° = 72°, and 72° ÷ 2 = 36° is the smaller angle. "
                  "The larger is 36° + 18° = 54°. (99° comes from using 180°.)", rnd))
    its.append(dq("An angle is 5 times as big as its supplement. How big is the angle?", 150, [30, 75, 36],
                  "The angle is 5 parts and its supplement is 1 part: 6 parts = 180°, so 1 part = 30°. "
                  "The angle is 5 × 30° = 150°. (30° is the supplement.)", rnd))
    its.append(dq("What is the supplement of the complement of 25°?", 115, [155, 65, 245],
                  "First the complement: 90° − 25° = 65°. Then its supplement: 180° − 65° = 115°. "
                  "(155° is the supplement of 25° itself.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Supplementary and complementary angles", "items": its}


# ------------------------------------------------------------ set 2: vertically opposite angles
def set_vertical(rnd, P):
    its = []
    lab = "two straight lines crossing"
    qx = "Two straight lines cross. Find the missing angle."
    for rot, a, texts, v, wrong in [
        (0, 40, ["40°", None, "?", None], 40, [140, 320, 50]),
        (20, 115, [None, "?", None, "65°"], 65, [115, 295, 25]),
        (-30, 72, ["?", None, "72°", None], 72, [108, 288, 18]),
        (10, 35, [None, "145°", None, "?"], 145, [35, 215, 55]),
    ]:
        its.append(dq(fig(cross_svg(rot, a, texts, label=lab)) + qx, v, wrong,
                      "The missing angle is vertically opposite the %s angle, so the two are equal: %s." % (D(v), D(v)), rnd))
    for rot, a, texts, v, wrong in [
        (0, 58, ["58°", "?", None, None], 122, [58, 302, 32]),
        (15, 130, [None, "?", "130°", None], 50, [130, 230, 40]),
    ]:
        k = [t for t in texts if t and t != "?"][0]
        its.append(dq(fig(cross_svg(rot, a, texts, label=lab)) + qx, v, wrong,
                      "The missing angle and %s are next to each other on a straight line, so they are supplementary: "
                      "180° − %s = %s. (%s would be the vertically opposite angle.)" % (k, k, D(v), k), rnd))
    its.append(mc(fig(cross_svg(0, 64, ["64°", "a", "b", "c"], label=lab)) + "Two straight lines cross. Find <i>a</i>, <i>b</i> and <i>c</i>.",
                  "a = 116°, b = 64°, c = 116°",
                  ["a = 64°, b = 116°, c = 64°", "a = 116°, b = 116°, c = 116°", "a = 26°, b = 64°, c = 26°"],
                  "<i>a</i> is on a straight line with 64°: 180° − 64° = 116°. <i>b</i> is vertically opposite 64°, so <i>b</i> = 64°. "
                  "<i>c</i> is vertically opposite <i>a</i>, so <i>c</i> = 116°.", rnd))
    its.append(dq(fig(cross_svg(0, 70, ["2x + 10°", None, "70°", None], L=92, label=lab)) +
                  V("Two straight lines cross. What is the value of x?"), 30, [40, 60, 70],
                  V("Vertically opposite angles are equal: 2x + 10° = 70°. 2x = 60°, so x = 30°. "
                    "(40° comes from adding 10° instead of subtracting it.)"), rnd))
    its.append(dq(fig(cross_svg(0, 120, ["3x", "x + 20°", None, None], L=92, label=lab)) +
                  V("Two straight lines cross. What is the value of x?"), 40, [50, 160, 10],
                  V("The two angles are next to each other on a straight line, so 3x + x + 20° = 180°. "
                    "4x = 160°, so x = 40°. Check: 120° + 60° = 180°. "
                    "(10° comes from making them equal, but only vertically opposite angles are equal.)"), rnd))
    its.append(dq(fig(cross_svg(10, 80, ["4x − 20°", None, "2x + 30°", None], L=96, label=lab)) +
                  V("Two straight lines cross. What is the value of x?"), 25, [5, 80, 50],
                  V("Vertically opposite angles are equal: 4x − 20° = 2x + 30°. Take 2x from both sides: 2x − 20° = 30°. "
                    "2x = 50°, so x = 25°. Check: 4 × 25° − 20° = 80° and 2 × 25° + 30° = 80°. (80° is the angle, not x.)"), rnd))
    three = "three straight lines through a point"
    its.append(dq(fig(rays_svg([0, 50, 110, 180, 230, 290],
                               [(0, 50, 50, "50°", "arc"), (50, 110, 60, "60°", "arc"), (110, 180, 70, "?", "arc")], three, L=82)) +
                  "Three straight lines meet at a point. Find the missing angle.", 70, [250, 130, 120],
                  "The three angles are on a straight line, so they add up to 180°. 50° + 60° = 110°, and 180° − 110° = 70°.", rnd))
    its.append(dq(fig(rays_svg([0, 45, 125, 180, 225, 305],
                               [(0, 45, 45, "45°", "arc"), (45, 125, 80, "80°", "arc"), (225, 305, 80, "?", "arc")], three, L=82)) +
                  "Three straight lines meet at a point. Find the missing angle.", 80, [100, 55, 45],
                  "The missing angle is vertically opposite the 80° angle, so it is also 80°.", rnd))
    its.append(dq(fig(rays_svg([0, 35, 120, 180, 215, 300],
                               [(0, 35, 35, "35°", "arc"), (35, 120, 85, "85°", "arc"), (300, 360, 60, "?", "arc")], three, L=82)) +
                  "Three straight lines meet at a point. Find the missing angle.", 60, [120, 85, 35],
                  "35° + 85° + the angle above them make a straight line: 180° − 120° = 60°. "
                  "The missing angle is vertically opposite that angle, so it is 60° too.", rnd))
    its.append(mc(fig(cross_svg(10, 55, ["a", "b", "c", "d"], label=lab)) + "Which two angles are vertically opposite?",
                  "a and c", ["a and b", "c and d", "a and d"],
                  "Vertically opposite angles are across the crossing point from each other: <i>a</i> and <i>c</i> (also <i>b</i> and <i>d</i>). "
                  "Angles next to each other, like <i>a</i> and <i>b</i>, are supplementary.", rnd))
    its.append(mc("What is true about vertically opposite angles?", "They are equal",
                  ["They add up to 180°", "They add up to 90°", "They add up to 360°"],
                  "When two straight lines cross, the angles opposite each other are equal. Angles next to each other add up to 180°.", rnd))
    n, he, his = P.next()
    its.append(mc("%s says that vertically opposite angles are supplementary. Is %s right?" % (n, he),
                  "No, they are equal", ["Yes, they add up to 180°", "Yes, they are on a straight line", "No, they add up to 360°"],
                  "Vertically opposite angles are equal. The angles next to each other (on a straight line) are the supplementary ones.", rnd))
    its.append(mc("Two straight lines cross. One of the angles is a right angle. What are the other three angles?",
                  "90°, 90° and 90°", ["90°, 180° and 90°", "45°, 90° and 45°", "270°, 90° and 270°"],
                  "The angle next to 90° is 180° − 90° = 90°, and opposite angles are equal. So all four angles are 90°: "
                  "the lines are perpendicular.", rnd))
    its.append(dq("Two straight lines cross. Two vertically opposite angles add up to 100°. How big is each of the other two angles?",
                  130, [50, 80, 260],
                  "The two equal opposite angles are 100° ÷ 2 = 50° each. The angles next to them are 180° − 50° = 130°.", rnd))
    its.append(dq("Two straight lines cross. One angle is 4 times the angle next to it. What is the smaller angle?",
                  36, [45, 72, 18],
                  "Angles next to each other add up to 180°. 1 part + 4 parts = 5 parts = 180°, so the smaller angle is 36°. "
                  "(72° comes from sharing 360° instead of 180°.)", rnd))
    its.append(dq("Two straight lines cross. One of the angles is 47°. What do the two obtuse angles add up to?",
                  266, [133, 313, 86],
                  "Each obtuse angle is next to a 47° angle: 180° − 47° = 133°. The two obtuse angles are equal: "
                  "133° + 133° = 266°. Check: 47° + 47° + 266° = 360°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Vertically opposite angles", "items": its}


# ------------------------------------------------------------ set 3: parallel lines and a transversal
PAR = "two parallel lines cut by a transversal"
PAIR_NAMES = ["corresponding angles", "alternate angles", "co-interior angles", "vertically opposite angles"]


def set_parallel(rnd, P):
    its = []
    q = "The arrows show that the two lines are parallel. Find the missing angle."
    for t, texts, v, wrong, e in [
        (65, {("U", 0): "65°", ("L", 0): "?"}, 65, [115, 295, 25],
         "The two angles are in the same position at each crossing point (above the line, right of the transversal). "
         "They are corresponding angles, so they are equal: 65°."),
        (110, {("U", 1): "70°", ("L", 1): "?"}, 70, [110, 20, 290],
         "The two angles are in the same position at each crossing point, so they are corresponding angles. "
         "Corresponding angles are equal: 70°."),
        (55, {("U", 3): "125°", ("L", 1): "?"}, 125, [55, 235, 35],
         "The angles are between the parallel lines, on opposite sides of the transversal (a Z shape). "
         "They are alternate angles, so they are equal: 125°. (55° would be co-interior angles.)"),
        (70, {("U", 2): "70°", ("L", 0): "?"}, 70, [110, 20, 290],
         "The angles are between the parallel lines, on opposite sides of the transversal. "
         "Alternate angles are equal: 70°."),
        (60, {("U", 3): "120°", ("L", 0): "?"}, 60, [120, 240, 30],
         "The angles are between the parallel lines, on the same side of the transversal (a C shape). "
         "They are co-interior angles, so they add up to 180°: 180° − 120° = 60°. (120° mixes them up with alternate angles.)"),
        (125, {("U", 2): "125°", ("L", 1): "?"}, 55, [125, 235, 35],
         "The angles are between the parallel lines, on the same side of the transversal. "
         "Co-interior angles add up to 180°: 180° − 125° = 55°."),
        (48, {("U", 0): "48°", ("L", 2): "?"}, 48, [132, 312, 42],
         "The angles are outside the parallel lines, on opposite sides of the transversal. "
         "The angle vertically opposite 48° and the missing angle are corresponding, so the missing angle is 48°."),
        (75, {("U", 1): "105°", ("L", 0): "?"}, 75, [105, 255, 15],
         "Two steps. The angle in the same place at the lower point is corresponding, so it is 105°. "
         "The missing angle is next to it on a straight line: 180° − 105° = 75°."),
        (40, {("U", 0): "40°", ("L", 3): "?"}, 140, [40, 320, 50],
         "The corresponding angle at the lower point is 40°. The missing angle is on a straight line with it: "
         "180° − 40° = 140°."),
    ]:
        its.append(dq(fig(par_svg(t, texts)) + q, v, wrong, e, rnd))
    qn = "The arrows show that the two lines are parallel. What kind of angles are <i>a</i> and <i>b</i>?"
    for t, texts, ans, e in [
        (62, {("U", 3): "a", ("L", 1): "b"}, "alternate angles",
         "They are between the parallel lines, on opposite sides of the transversal (a Z shape): alternate angles. They are equal."),
        (118, {("U", 0): "a", ("L", 0): "b"}, "corresponding angles",
         "They are in the same position at each crossing point (an F shape): corresponding angles. They are equal."),
        (58, {("U", 3): "a", ("L", 0): "b"}, "co-interior angles",
         "They are between the parallel lines, on the same side of the transversal (a C shape): co-interior angles. "
         "They add up to 180°."),
    ]:
        its.append(mc(fig(par_svg(t, texts)) + qn, ans, [x for x in PAIR_NAMES if x != ans], e, rnd))
    qv = V("The arrows show that the two lines are parallel. What is the value of x?")
    its.append(dq(fig(par_svg(105, {("U", 0): "3x", ("L", 0): "105°"})) + qv, 35, [25, 105, 315],
                  V("The angles are corresponding, so they are equal: 3x = 105°, and x = 105° ÷ 3 = 35°. "
                    "(25° comes from 3x = 75°, as if they added up to 180°.)"), rnd))
    its.append(dq(fig(par_svg(80, {("U", 3): "2x", ("L", 0): "x + 30°"}, gap=120, ext=60)) + qv, 50, [30, 70, 150],
                  V("The angles are co-interior, so they add up to 180°: 2x + x + 30° = 180°. 3x = 150°, so x = 50°. "
                    "Check: 100° + 80° = 180°. (30° comes from making them equal, as if they were alternate.)"), rnd))
    its.append(dq(fig(par_svg(70, {("U", 2): "4x − 10°", ("L", 0): "70°"}, gap=120, ext=60)) + qv, 20, [15, 30, 80],
                  V("The angles are alternate, so they are equal: 4x − 10° = 70°. 4x = 80°, so x = 20°. "
                    "(15° comes from subtracting 10° instead of adding it, and 30° from using 180° − 70° = 110°.)"), rnd))
    its.append(mc("When a transversal crosses two parallel lines, corresponding angles are …", "equal",
                  ["supplementary", "complementary", "always 90°"],
                  "Corresponding angles sit in the same position at each crossing point, so they are equal. "
                  "Co-interior angles are the ones that are supplementary.", rnd))
    its.append(mc("When a transversal crosses two parallel lines, co-interior angles …", "add up to 180°",
                  ["are equal", "add up to 90°", "add up to 360°"],
                  "Co-interior angles are between the parallel lines on the same side of the transversal. They add up to 180°.", rnd))
    n, he, his = P.next()
    its.append(mc("%s says that alternate angles on parallel lines add up to 180°. Is %s right?" % (n, he),
                  "No, alternate angles are equal",
                  ["Yes, they are between the lines", "Yes, they make a Z shape", "No, they add up to 90°"],
                  "Alternate angles (Z shape) are equal. Co-interior angles (C shape) are the ones that add up to 180°.", rnd))
    its.append(mc("A transversal crosses two lines. Two co-interior angles are 72° and 110°. Are the lines parallel?",
                  "No, 72° + 110° = 182°",
                  ["Yes, the angles are close", "Yes, one angle is obtuse", "No, co-interior angles must be equal"],
                  "If the lines were parallel, the co-interior angles would add up to exactly 180°. 72° + 110° = 182°, so the lines are not parallel.", rnd))
    its.append(mc("A transversal crosses two lines. Two corresponding angles are both 64°. Are the lines parallel?",
                  "Yes, corresponding angles are equal",
                  ["No, they must add up to 180°", "No, they must add up to 90°", "You cannot tell"],
                  "When corresponding angles are equal, the lines are parallel. This is how you can check that two lines are parallel.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallel lines: corresponding, alternate and co-interior angles", "items": its}


# ------------------------------------------------------------ set 4: triangles and quadrilaterals
def arrows_on(P, p, q):
    """Parallel-side arrow at the middle of side pq, pointing from p to q."""
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    chevron(P, pol(m, 4, ang(p, q)), ang(p, q))


def set_tri_quad(rnd, P):
    its = []
    q = "Find the missing angle in this triangle."
    for a, b, rot, shown, v, wrong in [
        (50, 60, 0, {0: "50°", 1: "60°", 2: "?"}, 70, [250, 110, 130]),
        (35, 40, 0, {0: "35°", 1: "?", 2: "105°"}, 40, [220, 140, 145]),
        (72, 63, 15, {0: "?", 1: "63°", 2: "45°"}, 72, [252, 108, 117]),
    ]:
        pts = tri_pts(a, b, 190 if 180 - a - b > 100 else 140, rot)
        A = check_tri(pts, [a, b, 180 - a - b])
        known = [A[i] for i, t in shown.items() if t != "?"]
        e = "The angles in a triangle add up to 180°. %s + %s = %s, and 180° − %s = %s. (%s comes from using 360°.)" % (
            D(known[0]), D(known[1]), D(sum(known)), D(sum(known)), D(v), D(360 - sum(known)))
        its.append(dq(fig(shape_svg(pts, shown, "triangle")) + q, v, wrong, e, rnd))
    pts = tri_pts(90, 38, 130)
    check_tri(pts, [90, 38, 52])
    its.append(dq(fig(shape_svg(pts, {1: "38°", 2: "?"}, "right triangle", rights=(0,))) + q, 52, [142, 128, 232],
                  "The small square is a right angle (90°). The other two angles add up to 180° − 90° = 90°, so 90° − 38° = 52°.", rnd))
    q_iso = "This is an isosceles triangle. The marks show the two equal sides. Find the missing angle."
    pts = tri_pts(70, 70, 100)
    check_tri(pts, [70, 70, 40])
    its.append(dq(fig(shape_svg(pts, {2: "40°", 1: "?"}, "isosceles triangle", ticks=((1, 1), (2, 1)))) + q_iso, 70,
                  [140, 40, 160],
                  "The two base angles are equal. 180° − 40° = 140°, and 140° ÷ 2 = 70°. (140° is both base angles together.)", rnd))
    pts = tri_pts(67, 67, 150, 180)
    check_tri(pts, [67, 67, 46])
    its.append(dq(fig(shape_svg(pts, {0: "67°", 2: "?"}, "isosceles triangle", ticks=((1, 1), (2, 1)))) + q_iso, 46,
                  [113, 67, 23],
                  "The two base angles are equal, so both are 67°. 67° + 67° = 134°, and 180° − 134° = 46°. "
                  "(113° comes from 180° − 67°, forgetting the second base angle.)", rnd))
    # exterior angles
    tp = tri_pts(45, 75, 130)
    check_tri(tp, [45, 75, 60])

    def ext1(P_, A):
        E = (tp[1][0] + 75, 0.0)
        P_.line(tp[1], E)
        P_.mark(tp[1], tp[2], E, 105, "?")
    its.append(dq(fig(shape_svg(tp, {0: "45°", 2: "60°"}, "triangle with one side extended", extra=ext1)) +
                  "One side of the triangle is extended. Find the exterior angle marked “?”.", 105, [75, 255, 15],
                  "The exterior angle equals the sum of the two interior angles that are not next to it: 45° + 60° = 105°. "
                  "(Or: the interior angle is 180° − 105° = 75°, and 75° + 105° = 180°.)", rnd))
    tq = tri_pts(70, 50, 140)
    check_tri(tq, [70, 50, 60])

    def ext2(P_, A):
        E = (tq[1][0] + 75, 0.0)
        P_.line(tq[1], E)
        P_.mark(tq[1], tq[2], E, 130, "130°")
    its.append(dq(fig(shape_svg(tq, {0: "70°", 2: "?"}, "triangle with one side extended", extra=ext2)) +
                  "One side of the triangle is extended. Find the missing angle.", 60, [50, 110, 200],
                  "The exterior angle 130° equals the sum of the two interior angles that are not next to it: "
                  "70° + ? = 130°, so ? = 60°. (50° is the interior angle next to the 130° angle.)", rnd))
    its.append(dq(V("The angles of a triangle are x, 2x and 3x. What is the value of x?"), 30, [60, 36, 90],
                  V("x + 2x + 3x = 6x = 180°, so x = 30°. The angles are 30°, 60° and 90°. (60° comes from 6x = 360°.)"), rnd))
    n, he, his = P.next()
    pts = tri_pts(65, 45, 140)
    its.append(mc(fig(shape_svg(pts, {0: "65°", 1: "45°", 2: "?"}, "triangle")) +
                  "%s says the missing angle is 250°, because the angles in a triangle add up to 360°. Is %s right?" % (n, he),
                  "No, it is 70°", ["Yes, it is 250°", "No, it is 110°", "No, it is 20°"],
                  "The angles in a triangle add up to 180°, not 360°. 65° + 45° = 110°, and 180° − 110° = 70°.", rnd))
    its.append(mc("Which three angles could be the angles of a triangle?", "50°, 60° and 70°",
                  ["50°, 60° and 80°", "90°, 90° and 20°", "100°, 100° and 160°"],
                  "The angles of a triangle add up to 180°. 50° + 60° + 70° = 180°. The others add up to 190°, 200° and 360°.", rnd))
    its.append(mc("An isosceles triangle has one angle of 100°. What are the other two angles?", "40° and 40°",
                  ["80° and 80°", "100° and −20°", "50° and 30°"],
                  "100° is obtuse, so it must be the angle between the equal sides (two angles of 100° would be more than 180°). "
                  "180° − 100° = 80°, and 80° ÷ 2 = 40°.", rnd))
    its.append(dq("Two angles of a triangle are 37° and 98°. What is the third angle?", 45, [225, 55, 135],
                  "37° + 98° = 135°, and 180° − 135° = 45°. (225° comes from using 360°.)", rnd))
    # quadrilaterals
    q4 = "Find the missing angle in this quadrilateral."
    for (a, b, c), texts, v, wrong in [
        ((80, 115, 70), {0: "80°", 1: "115°", 2: "70°", 3: "?"}, 95, [265, 85, 105]),
        ((100, 65, 120), {0: "100°", 1: "?", 2: "120°", 3: "75°"}, 65, [295, 115, 245]),
    ]:
        pts = quad_from(a, b, c, 150, 100)
        known = [poly_angles(pts)[i] for i, t in texts.items() if t != "?"]
        e = "The angles in a quadrilateral add up to 360°. %s + %s + %s = %s, and 360° − %s = %s." % (
            D(known[0]), D(known[1]), D(known[2]), D(sum(known)), D(sum(known)), D(v))
        its.append(dq(fig(shape_svg(pts, texts, "quadrilateral")) + q4, v, wrong, e, rnd))
    pts = quad_from(90, 90, 65, 150, 140)
    its.append(dq(fig(shape_svg(pts, {2: "65°", 3: "?"}, "quadrilateral with two right angles", rights=(0, 1))) + q4, 115,
                  [205, 25, 65],
                  "The two small squares are 90° each. 90° + 90° + 65° = 245°, and 360° − 245° = 115°. "
                  "(25° comes from using 180°: 180° − 90° − 65°.)", rnd))
    A_, B_ = O, (140.0, 0.0)
    D_ = pol(O, 80, 70)
    C_ = (B_[0] + D_[0], B_[1] + D_[1])
    pg = [A_, B_, C_, D_]

    def pg_arrows(P_, A):
        arrows_on(P_, pg[0], pg[1])
        arrows_on(P_, pg[3], pg[2])
    its.append(dq(fig(shape_svg(pg, {0: "70°", 1: "?"}, "parallelogram", ticks=((1, 2), (3, 2)), extra=pg_arrows)) +
                  "This is a parallelogram. Find the missing angle.", 110, [70, 290, 20],
                  "The bottom and top sides are parallel, so the angles at the two ends of a slanted side are co-interior: "
                  "they add up to 180°. 180° − 70° = 110°. Check: 70° + 110° + 70° + 110° = 360°.", rnd))
    tz = quad_from(64, 72, 108, 170, 90)

    def tz_arrows(P_, A):
        arrows_on(P_, tz[0], tz[1])
        arrows_on(P_, tz[3], tz[2])
    its.append(dq(fig(shape_svg(tz, {0: "64°", 1: "72°", 3: "?"}, "trapezoid with parallel sides marked", extra=tz_arrows)) +
                  "This is a trapezoid. The arrows show the parallel sides. Find the missing angle.", 116, [64, 296, 26],
                  "The left side crosses the two parallel sides, so the angles at its ends are co-interior: they add up to 180°. "
                  "180° − 64° = 116°. (64° would only be right for alternate angles.)", rnd))
    kp = kite_pts(50, 90)
    its.append(dq(fig(shape_svg(kp, {2: "50°", 1: "?"}, "kite", rights=(0,), ticks=((0, 1), (3, 1), (1, 2), (2, 2)))) +
                  "This is a kite. Its two side angles are equal. Find the missing angle.", 110, [220, 40, 130],
                  "50° + 90° = 140°. 360° − 140° = 220° is left for the two equal angles: 220° ÷ 2 = 110°.", rnd))
    its.append(dq(V("The angles of a quadrilateral are x, x, 2x and 2x. What is the value of x?"), 60, [30, 90, 120],
                  V("x + x + 2x + 2x = 6x = 360°, so x = 60°. The angles are 60°, 60°, 120° and 120°. (30° comes from using 180°.)"), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in triangles and quadrilaterals", "items": its}


# ------------------------------------------------------------ set 5: interior angles of polygons, and problems
def set_polygons(rnd, P):
    its = []
    pent = regular_pts(5)

    def diags(P_, A):
        for k in (2, 3):
            P_.line(pent[0], pent[k], sw=2)
    its.append(dq(fig(shape_svg(pent, {}, "pentagon split into 3 triangles", extra=diags)) +
                  "The pentagon is split into triangles from one vertex. What is the sum of its interior angles?", 540,
                  [360, 900, 108],
                  "There are 5 − 2 = 3 triangles, and the angles in each add up to 180°. 3 × 180° = 540°. "
                  "(900° counts 5 triangles, but there are only 3.)", rnd))
    its.append(dq("What is the sum of the interior angles of a hexagon?", 720, [1080, 360, 900],
                  "Use (n − 2) × 180°: (6 − 2) × 180° = 4 × 180° = 720°. (1080° comes from 6 × 180°.)", rnd))
    its.append(dq("What is the sum of the interior angles of an octagon?", 1080, [1440, 720, 1260],
                  "(n − 2) × 180° = (8 − 2) × 180° = 6 × 180° = 1080°. (1440° comes from 8 × 180°, and 1260° from (8 − 1) × 180°.)", rnd))
    its.append(dq("What is the sum of the interior angles of a decagon (10 sides)?", 1440, [1800, 1620, 360],
                  "(10 − 2) × 180° = 8 × 180° = 1440°. (1800° comes from 10 × 180°.)", rnd))
    hexa = regular_pts(6)
    its.append(dq(fig(shape_svg(pent, {0: "?"}, "regular pentagon", ticks=tuple((i, 1) for i in range(5)))) +
                  "This is a regular pentagon. What is the size of each interior angle?", 108, [72, 540, 120],
                  "Sum: (5 − 2) × 180° = 540°. The 5 angles are equal: 540° ÷ 5 = 108°. "
                  "(72° is 360° ÷ 5, the exterior angle.)", rnd))
    its.append(dq(fig(shape_svg(hexa, {0: "?"}, "regular hexagon", ticks=tuple((i, 1) for i in range(6)))) +
                  "This is a regular hexagon. What is the size of each interior angle?", 120, [60, 720, 108],
                  "Sum: (6 − 2) × 180° = 720°. 720° ÷ 6 = 120°. (60° is 360° ÷ 6, the exterior angle.)", rnd))
    its.append(dq("A stop sign is a regular octagon. What is the size of each interior angle?", 135, [45, 1080, 180],
                  "Sum: (8 − 2) × 180° = 1080°. The 8 angles are equal: 1080° ÷ 8 = 135°. (45° is 360° ÷ 8, the exterior angle.)", rnd))
    n, he, his = P.next()
    its.append(mcq_n("%s draws lines from one vertex of a stop sign (a regular octagon) to all the other vertices. "
                     "How many triangles does %s make?" % (n, he), 6, [8, 7, 5],
                     "From one vertex you can draw lines to every vertex except itself and its 2 neighbours. "
                     "An octagon splits into 8 − 2 = 6 triangles.", rnd))
    its.append(mcq_n("The interior angles of a polygon add up to 1260°. How many sides does it have?", 9, [7, 8, 10],
                     "(n − 2) × 180° = 1260°, so n − 2 = 1260 ÷ 180 = 7, and n = 9. (7 forgets to add the 2 back.)", rnd))
    its.append(mcq_n("Each interior angle of a regular polygon is 140°. How many sides does it have?", 9, [40, 7, 8],
                     "Each exterior angle is 180° − 140° = 40°. The exterior angles add up to 360°: 360° ÷ 40° = 9 sides. "
                     "Check: (9 − 2) × 180° = 1260°, and 1260° ÷ 9 = 140°.", rnd))
    its.append(dq("Four interior angles of a pentagon are 100°, 110°, 95° and 120°. What is the fifth angle?", 115,
                  [295, 108, 425],
                  "The sum for a pentagon is (5 − 2) × 180° = 540°. 100° + 110° + 95° + 120° = 425°, and 540° − 425° = 115°. "
                  "(108° is the angle of a regular pentagon, but this one is not regular.)", rnd))
    its.append(dq("Five interior angles of a hexagon are 120°, 115°, 130°, 125° and 110°. What is the sixth angle?", 120,
                  [300, 480, 600],
                  "The sum for a hexagon is (6 − 2) × 180° = 720°. The five angles add up to 600°, and 720° − 600° = 120°. "
                  "(300° comes from using (6 − 1) × 180° = 900°.)", rnd))
    its.append(dq(V("The interior angles of a hexagon are x, x, x, 2x, 2x and 2x. What is the value of x?"), 80,
                  [40, 120, 160],
                  V("The sum is (6 − 2) × 180° = 720°. x + x + x + 2x + 2x + 2x = 9x, so 9x = 720° and x = 80°. "
                    "(40° comes from 9x = 360°.)"), rnd))
    its.append(dq("The loonie, Canada’s $1 coin, has 11 sides. What is the sum of the interior angles of an 11-sided polygon?",
                  1620, [1980, 1800, 360],
                  "(11 − 2) × 180° = 9 × 180° = 1620°. (1980° comes from 11 × 180°.)", rnd))
    its.append(dq("A floor is tiled with regular octagons and squares. At each corner, two octagons and one square meet. "
                  "What do the three angles at that corner add up to?", 360, [315, 270, 405],
                  "Each octagon angle is 135° and each square angle is 90°. 135° + 135° + 90° = 360°, a full turn, "
                  "so the tiles fit with no gaps.", rnd))
    its.append(dq("A soccer ball is made of regular pentagons and regular hexagons. At each corner, one pentagon and two hexagons meet. "
                  "What do the three angles at that corner add up to?", 348, [360, 324, 336],
                  "Each pentagon angle is 108° and each hexagon angle is 120°. 108° + 120° + 120° = 348°. "
                  "That is less than 360°, so the pieces do not lie flat: the ball curves.", rnd))
    its.append(dq("A straight road crosses two parallel railway tracks near Winnipeg. The road makes a 58° angle with the first track. "
                  "What is the corresponding angle at the second track?", 58, [122, 32, 302],
                  "The tracks are parallel, so corresponding angles are equal: 58°. (122° is the angle on the other side of the road.)", rnd))
    n, he, his = P.next()
    its.append(dq("%s leans a ladder against the wall of a cottage to clean the eavestroughs. The wall is vertical and the ground is flat. "
                  "The ladder makes a 72° angle with the ground. What angle does it make with the wall?" % n, 18, [108, 288, 72],
                  "The wall, the ground and the ladder make a right triangle. 180° − 90° − 72° = 18°. "
                  "The two acute angles are complementary: 90° − 72° = 18°.", rnd))
    its.append(dq("The front of an A-frame cabin is an isosceles triangle. The angle at the top is 50°. "
                  "What angle does each sloping side make with the floor?", 65, [130, 50, 155],
                  "The two base angles are equal. 180° − 50° = 130°, and 130° ÷ 2 = 65°.", rnd))
    its.append(dq("The parking lines at a mall are parallel. Each line meets the curb at a 65° angle. "
                  "What is the angle on the other side of the line, along the same curb?", 115, [65, 25, 295],
                  "The two angles are on a straight line (the curb), so they are supplementary: 180° − 65° = 115°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Interior angles of polygons: (n − 2) × 180°", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    pairs = strip_svg([line_svg(0, [60, 120], ["60°", "120°"], L=76),
                       rays_svg([0, 35, 90], [(0, 35, 35, "35°", "arc"), (35, 90, 55, "55°", "arc"), (0, 90, 90, None, "right")],
                                "complementary angles", L=86),
                       cross_svg(0, 50, ["50°", "130°", "50°", "130°"], L=66)],
                      ["supplementary: 180°", "complementary: 90°", "vertically opposite: equal"],
                      "supplementary, complementary and vertically opposite angles", cw=215)
    par = strip_svg([par_svg(70, {("U", 0): "70°", ("L", 0): "70°"}, gap=70, ext=48),
                     par_svg(70, {("U", 2): "70°", ("L", 0): "70°"}, gap=70, ext=48),
                     par_svg(70, {("U", 3): "110°", ("L", 0): "70°"}, gap=70, ext=48)],
                    ["corresponding: equal", "alternate: equal", "co-interior: 180°"],
                    "corresponding, alternate and co-interior angles on parallel lines", cw=200)
    tri = tri_pts(50, 70, 140)
    pent = regular_pts(5, 62)

    def diags(P, A):
        for k in (2, 3):
            P.line(pent[0], pent[k], sw=2)
    shapes = strip_svg([shape_svg(tri, {0: "50°", 1: "70°", 2: "60°"}, "triangle"),
                        shape_svg(quad_from(80, 115, 70, 130, 90), {0: "80°", 1: "115°", 2: "70°", 3: "95°"}, "quadrilateral"),
                        shape_svg(pent, {}, "pentagon split into 3 triangles", extra=diags)],
                       ["triangle: 180°", "quadrilateral: 360°", "pentagon: 540°"],
                       "angles in a triangle, a quadrilateral and a pentagon", cw=220)
    return (
        "<h2>Pairs of angles</h2>"
        "<p><b>Supplementary</b> angles add up to <b>180°</b>, like angles on a straight line. "
        "<b>Complementary</b> angles add up to <b>90°</b>, like the two parts of a right angle. "
        "When two lines cross, the <b>vertically opposite</b> angles are <b>equal</b>.</p>"
        "<figure class='sn-fig'>" + pairs + "</figure>" +
        ex("Supplement and complement", "Find the supplement and the complement of 38°.",
           "Supplement: 180° − 38° = 142°. Complement: 90° − 38° = 52°.", "142° and 52°") +
        "<h2>Parallel lines and a transversal</h2>"
        "<p>A <b>transversal</b> is a line that crosses two other lines. Arrows on the lines show they are parallel. "
        "Then three pairs of angles follow a rule.</p>"
        "<figure class='sn-fig'>" + par +
        "<figcaption>Corresponding angles (F shape) and alternate angles (Z shape) are equal. "
        "Co-interior angles (C shape) add up to 180°.</figcaption></figure>" +
        table(["Pair", "Where they are", "Rule"], [
            ["Corresponding", "Same position at each crossing point", "Equal"],
            ["Alternate", "Between the lines, opposite sides of the transversal", "Equal"],
            ["Co-interior", "Between the lines, same side of the transversal", "Add up to 180°"],
        ]) +
        ex("Use algebra", "Two co-interior angles are 2<i>x</i> and <i>x</i> + 30°. Find <i>x</i>.",
           "Co-interior angles add up to 180°: 3<i>x</i> + 30° = 180°. 3<i>x</i> = 150°, so <i>x</i> = 50°.",
           "<i>x</i> = 50°") +
        "<h2>Triangles, quadrilaterals and polygons</h2>"
        "<p>The angles in a triangle add up to <b>180°</b>. The <b>exterior angle</b> of a triangle equals the sum of the two "
        "interior angles that are not next to it. A polygon with <i>n</i> sides splits into <i>n</i> − 2 triangles from one vertex, "
        "so its interior angles add up to <b>(<i>n</i> − 2) × 180°</b>.</p>"
        "<figure class='sn-fig'>" + shapes + "</figure>" +
        table(["Polygon", "Sides", "Sum of interior angles", "Each angle if regular"], [
            ["Triangle", "3", "1 × 180° = 180°", "60°"],
            ["Quadrilateral", "4", "2 × 180° = 360°", "90°"],
            ["Pentagon", "5", "3 × 180° = 540°", "108°"],
            ["Hexagon", "6", "4 × 180° = 720°", "120°"],
            ["Octagon", "8", "6 × 180° = 1080°", "135°"],
        ]) +
        ex("Regular octagon", "A stop sign is a regular octagon. Find each interior angle.",
           "Sum: (8 − 2) × 180° = 1080°. The 8 angles are equal: 1080° ÷ 8 = 135°.", "135°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up alternate and co-interior angles", "Z shape: equal. C shape (same side, between the lines): add up to 180°"],
            ["Using 360° for the angles in a triangle", "A triangle is 180°. A quadrilateral is 360°"],
            ["Mixing up supplementary and complementary", "Supplementary: 180°. Complementary: 90°"],
            ["Using <i>n</i> × 180° for a polygon", "Use (<i>n</i> − 2) × 180°: a hexagon is 4 × 180° = 720°"],
            ["Using the angle rules when the lines are not parallel", "Look for the arrows. Without them, corresponding angles need not be equal"],
        ])
    )


FAQ = [
    {"q": "What angle properties do Grade 8 students learn in Ontario?",
     "a": "In Spatial Sense (E2.2), they solve problems with the angle properties of intersecting lines, parallel lines cut by a transversal "
          "(corresponding, alternate and co-interior angles) and polygons, including the sum of interior angles, (n − 2) × 180°."},
    {"q": "What is the difference between alternate and co-interior angles?",
     "a": "Both pairs are between the parallel lines. Alternate angles are on opposite sides of the transversal (a Z shape) and are equal; "
          "co-interior angles are on the same side (a C shape) and add up to 180°."},
    {"q": "How do you find the sum of the interior angles of a polygon?",
     "a": "Use (n − 2) × 180°, where n is the number of sides. A hexagon has (6 − 2) × 180° = 720°, so each angle of a regular hexagon is 720° ÷ 6 = 120°."},
    {"q": "What is the difference between supplementary and complementary angles?",
     "a": "Supplementary angles add up to 180°, like angles on a straight line. Complementary angles add up to 90°, like the two parts of a right angle."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5/5/5/5)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen():
    rnd = random.Random(48816)
    P = People(rnd)
    sets = [set_supp_comp(rnd, P), set_vertical(rnd, P), set_parallel(rnd, P), set_tri_quad(rnd, P), set_polygons(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "angle-properties", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Angle Properties: Parallel Lines, Transversals and Polygons",
        "seo_title": "Grade 8 Angle Properties Worksheets: Parallel Lines and Polygons, Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Angle properties",
        "domain": "Spatial Sense",
        "standard_code": "Grade 8: E2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve problems involving angle properties, including the properties of intersecting and parallel lines and of polygons",
        "meta_desc": "Free Grade 8 math worksheets on angle properties for the Ontario curriculum: supplementary and complementary angles, "
                     "vertically opposite angles, corresponding, alternate and co-interior angles on parallel lines, triangles and "
                     "quadrilaterals, and interior angles of polygons with (n − 2) × 180°. 100 questions with an answer key.",
        "key_big": "On parallel lines, corresponding and alternate angles are equal, and co-interior angles add up to 180°.",
        "key_sub": "Supplementary angles add up to 180° and complementary angles to 90°. Vertically opposite angles are equal. "
                   "A triangle’s angles add up to 180°, a quadrilateral’s to 360°, and any polygon’s to (n − 2) × 180°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable: wide pictures (by name), and any
    picture whose 16px labels would print smaller than 3 mm at the normal size (27 mm × 52 mm, square 34 mm)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
            m = re.search(r"<svg (?!data-pf)[^>]*viewBox='0 0 (\d+) (\d+)'", it["q"])
            if m and "<text" in it["q"]:
                W, H = int(m.group(1)), int(m.group(2))
                k = 34.0 / W if W == H else min(52.0 / W, 27.0 / H)
                if 16 * k < 3.0:
                    it["q"] = it["q"].replace("<svg ", "<svg data-pf='lg' ", 1)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(two parallel lines|three straight lines)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
