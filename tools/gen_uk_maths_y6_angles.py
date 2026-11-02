# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Angles (National Curriculum in England, Geometry – properties of shapes)
  python tools/gen_uk_maths_y6_angles.py
HTML attributes use single quotes (no backslashes in the JSON).

Angle facts used:
  straight line 180°, around a point 360°, vertically opposite angles are equal,
  triangle 180°, quadrilateral 360°, polygon with n sides (n − 2) × 180°,
  regular polygon: exterior angle 360° ÷ n, interior angle 180° − exterior angle.
Every figure is drawn to its stated angles: each marked angle is measured from the drawing
and checked against its value (also the "?" and letter angles). Labels are checked so that
they do not touch a line, an arc or another label, and sit inside the angle they name.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


def D(v):
    """Angle in degrees as text: 65°, 22.5°, 1,080°."""
    if abs(v - round(v)) < 1e-9:
        return "{:,}°".format(int(round(v)))
    return ("%.1f°" % v)


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
    """Point at distance r from V in direction deg (anticlockwise on screen, 0 = right)."""
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
        """Mark the angle at V between rays VP and VQ (the smaller one unless ccw: from P anticlockwise to Q).
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
    each angle measured anticlockwise from from_dir to to_dir."""
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
    """Two straight lines crossing at O: angles a, 180 − a, a, 180 − a anticlockwise from rot.
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
    """Convex quadrilateral ABCD (anticlockwise) with angles a at A, b at B, c at C; D = 360 − a − b − c."""
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
    pts = [(0.0, h1 + h2), (w, h1), (0.0, 0.0), (-w, h1)]     # bottom, right, top, left (anticlockwise on screen)
    A = poly_angles(pts)
    side = (360 - top - bottom) / 2.0
    assert all(abs(x - y) < 1e-6 for x, y in zip(A, [bottom, side, top, side])), A
    return pts


def clock_svg(h, label=None):
    """Analogue clock at h o'clock with the smaller angle between the hands marked. Square picture."""
    c = (60.0, 60.0)
    R = 55
    s = ["<circle cx='60' cy='60' r='%d' fill='#ffffff' stroke='%s' stroke-width='3'/>" % (R, GREEN)]
    for i in range(12):
        d = 90 - 30 * i
        a, b = pol(c, R - 5, d), pol(c, R - (12 if i % 3 == 0 else 9), d)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>"
                 % (a + b + (INK, 2.4 if i % 3 == 0 else 1.4)))
    for num, i in (("12", 0), ("3", 3), ("6", 6), ("9", 9)):
        p = pol(c, R - 22, 90 - 30 * i)
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (p[0], p[1] + 5.4, INK, num))
    hd = 90 - 30 * (h % 12)
    sweep = (30 * h) % 360
    a0, a1 = (hd, 90) if sweep <= 180 else (90, 90 + 360 - sweep)
    n = 30
    arc = [pol(c, 15, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in arc), RED))
    hh, mh = pol(c, 19, hd), pol(c, 27, 90)
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='60' cy='60' r='4' fill='%s'/>" % INK)
    return svg_wrap(120, 120, "".join(s), label or "clock showing %d o’clock" % h)


# ------------------------------------------------------------ set 1: straight line and around a point
def set_line_point(rnd, P):
    its = []
    q_line = "The angles are on a straight line. Work out the missing angle."
    # (rot, parts, texts, wrong answers)
    lines = [
        (0, [50, 130], ["50°", "?"], 130, [310, 40, 50],
         "Angles on a straight line add up to 180°. 180° − 50° = 130°."),
        (0, [65, 115], ["?", "115°"], 65, [245, 25, 115],
         "Angles on a straight line add up to 180°. 180° − 115° = 65°. (360° − 115° = 245° would be for angles around a point.)"),
        (20, [142, 38], ["142°", "?"], 38, [218, 52, 142],
         "The line is tilted, but it is still straight: 180° − 142° = 38°."),
        (0, [45, 65, 70], ["45°", "?", "70°"], 65, [245, 115, 135],
         "First add the angles you know: 45° + 70° = 115°. Then 180° − 115° = 65°."),
        (0, [90, 55, 35], [None, "?", "35°"], 55, [145, 235, 125],
         "The small square is a right angle: 90°. 90° + 35° = 125°, and 180° − 125° = 55°."),
        (-15, [28, 55, 97], ["28°", "?", "97°"], 55, [235, 125, 83],
         "28° + 97° = 125°. Angles on a straight line add up to 180°, so 180° − 125° = 55°."),
    ]
    for rot, parts, texts, v, wrong, e in lines:
        lab = "angles on a straight line"
        its.append(dq(fig(line_svg(rot, parts, texts, label=lab)) + q_line, v, wrong, e, rnd))
    q_pt = "The angles are around a point. Work out the missing angle."
    pts = [
        (0, [110, 135, 115], ["110°", "135°", "?"], 115, [245, 225, 125],
         "Angles around a point add up to 360°. 110° + 135° = 245°, and 360° − 245° = 115°."),
        (30, [140, 85, 135], ["140°", "?", "135°"], 85, [275, 95, 225],
         "140° + 135° = 275°. Angles around a point add up to 360°: 360° − 275° = 85°."),
        (0, [90, 125, 60, 85], [None, "125°", "60°", "?"], 85, [275, 95, 235],
         "The small square is 90°. 90° + 125° + 60° = 275°, and 360° − 275° = 85°."),
        (15, [100, 120, 75, 65], ["100°", "120°", "?", "65°"], 75, [285, 105, 85],
         "100° + 120° + 65° = 285°. 360° − 285° = 75°."),
    ]
    for rot, parts, texts, v, wrong, e in pts:
        its.append(dq(fig(point_svg(rot, parts, texts)) + q_pt, v, wrong, e, rnd))
    its.append(dq(fig(rays_svg([0, 62, 90], [(0, 62, 62, "62°", "arc"), (62, 90, 28, "?", "arc"), (0, 90, 90, None, "right")],
                               "right angle split into two angles", L=96)) +
                  "The whole angle is a right angle. Work out the missing angle.", 28, [118, 298, 62],
                  "A right angle is 90°. 90° − 62° = 28°. (180° − 62° = 118° would be for a straight line.)", rnd))
    its.append(dq(fig(line_svg(0, [70, 70, 40], ["a", "a", "40°"], label="angles on a straight line, two marked a")) +
                  "The two angles marked <i>a</i> are equal. What is <i>a</i>?", 70, [140, 160, 320],
                  "Angles on a straight line add up to 180°. 180° − 40° = 140°, and the two equal angles share it: 140° ÷ 2 = 70°.", rnd))
    its.append(dq(fig(point_svg(90, [120, 120, 120], ["b", "b", "b"], label="three equal angles around a point")) +
                  "The three angles marked <i>b</i> are equal. What is <i>b</i>?", 120, [60, 90, 180],
                  "Angles around a point add up to 360°. 360° ÷ 3 = 120°. (180° ÷ 3 = 60° would be a straight line.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [130, 50], ["130°", "?"])) +
                   "%s says the missing angle is 230°, because 360° − 130° = 230°. Is %s right?" % (n, he),
                   "No, it is 50°", ["Yes, it is 230°", "No, it is 130°", "No, it is 40°"],
                   "The angles are on a straight line, so they add up to 180°, not 360°. 180° − 130° = 50°.", rnd))
    its.append(dq("Angles on a straight line add up to …", 180, [360, 90, 100],
                  "A straight line is a half turn: 180°. Two right angles make a straight line.", rnd))
    its.append(dq("Angles around a point add up to …", 360, [180, 270, 90],
                  "Angles around a point make a full turn: 360°.", rnd))
    its.append(dq("Three equal angles together make a straight line. How big is each angle?", 60, [120, 90, 45],
                  "The three angles add up to 180°. 180° ÷ 3 = 60°. (120° would come from using 360°.)", rnd))
    its.append(dq("Five equal angles fit exactly around a point. How big is each angle?", 72, [36, 90, 60],
                  "Around a point: 360°. 360° ÷ 5 = 72°. (36° comes from 180° ÷ 5.)", rnd))
    its.append(dq("Four angles are around a point. One is a right angle and the other three are equal. How big is each of the three equal angles?",
                  90, [30, 120, 270],
                  "360° − 90° = 270°. The three equal angles share it: 270° ÷ 3 = 90°.", rnd))
    its.append(mcq("Two angles are next to each other. One is 125° and the other is 65°. Can they make a straight line?",
                   "No, they add up to 190°", ["Yes, they add up to 180°", "Yes, one angle is obtuse", "No, they add up to 360°"],
                   "125° + 65° = 190°. Angles on a straight line must add up to exactly 180°, so they cannot.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles on a straight line and around a point", "items": its}


# ------------------------------------------------------------ set 2: vertically opposite angles
def set_vertical(rnd, P):
    its = []
    lab = "two straight lines crossing"
    # (rot, a, texts for the four angles a, 180−a, a, 180−a, answer, wrong, e)
    opp = [
        (0, 40, ["40°", None, "?", None], 40, [140, 320, 50]),
        (20, 115, [None, "?", None, "65°"], 65, [115, 295, 25]),
        (-30, 72, ["?", None, "72°", None], 72, [108, 288, 18]),
        (10, 35, [None, "145°", None, "?"], 145, [35, 215, 55]),
    ]
    for rot, a, texts, v, wrong in opp:
        its.append(dq(fig(cross_svg(rot, a, texts, label=lab)) + "Two straight lines cross. Work out the missing angle.", v, wrong,
                      "The missing angle is vertically opposite the %s angle, so they are equal: %s." % (D(v), D(v)), rnd))
    adj = [
        (0, 58, ["58°", "?", None, None], 122, [58, 302, 32]),
        (15, 130, [None, "?", "130°", None], 50, [130, 230, 40]),
        (-20, 75, [None, None, "75°", "?"], 105, [75, 285, 15]),
        (5, 34, ["?", "146°", None, None], 34, [146, 214, 56]),
    ]
    for rot, a, texts, v, wrong in adj:
        k = [t for t in texts if t and t != "?"][0]
        its.append(dq(fig(cross_svg(rot, a, texts, label=lab)) + "Two straight lines cross. Work out the missing angle.", v, wrong,
                      "The missing angle and %s are next to each other on a straight line, so they add up to 180°. 180° − %s = %s."
                      % (k, k, D(v)), rnd))
    its.append(mcq(fig(cross_svg(0, 64, ["64°", "a", "b", "c"], label=lab)) + "Two straight lines cross. Find <i>a</i>, <i>b</i> and <i>c</i>.",
                   "a = 116°, b = 64°, c = 116°",
                   ["a = 64°, b = 116°, c = 64°", "a = 116°, b = 116°, c = 116°", "a = 26°, b = 64°, c = 26°"],
                   "<i>a</i> is on a straight line with 64°: 180° − 64° = 116°. <i>b</i> is vertically opposite 64°, so it is 64°. "
                   "<i>c</i> is vertically opposite <i>a</i>, so it is 116°.", rnd))
    its.append(mcq(fig(cross_svg(30, 105, ["p", "q", "r", "105°"], label=lab)) + "Two straight lines cross. Find <i>p</i>, <i>q</i> and <i>r</i>.",
                   "p = 75°, q = 105°, r = 75°",
                   ["p = 105°, q = 75°, r = 105°", "p = 75°, q = 75°, r = 75°", "p = 255°, q = 105°, r = 255°"],
                   "<i>p</i> and 105° are on a straight line: 180° − 105° = 75°. <i>q</i> is vertically opposite 105°, so 105°. "
                   "<i>r</i> is vertically opposite <i>p</i>: 75°.", rnd))
    its.append(mcq(fig(cross_svg(10, 55, ["a", "b", "c", "d"], label=lab)) + "Which two angles are vertically opposite?",
                   "a and c", ["a and b", "c and d", "a and d"],
                   "Vertically opposite angles are across the crossing point from each other: <i>a</i> and <i>c</i> (also <i>b</i> and <i>d</i>). "
                   "Angles next to each other, like <i>a</i> and <i>b</i>, add up to 180°.", rnd))
    three = "three straight lines through a point"
    its.append(dq(fig(rays_svg([0, 50, 110, 180, 230, 290],
                               [(0, 50, 50, "50°", "arc"), (50, 110, 60, "60°", "arc"), (110, 180, 70, "?", "arc")], three, L=82)) +
                  "Three straight lines meet at a point. Work out the missing angle.", 70, [250, 130, 120],
                  "The three angles are on a straight line, so they add up to 180°. 50° + 60° = 110°, and 180° − 110° = 70°.", rnd))
    its.append(dq(fig(rays_svg([0, 45, 125, 180, 225, 305],
                               [(0, 45, 45, "45°", "arc"), (45, 125, 80, "80°", "arc"), (225, 305, 80, "?", "arc")], three, L=82)) +
                  "Three straight lines meet at a point. Work out the missing angle.", 80, [100, 55, 45],
                  "The missing angle is vertically opposite the 80° angle, so it is also 80°.", rnd))
    its.append(dq(fig(rays_svg([0, 35, 120, 180, 215, 300],
                               [(0, 35, 35, "35°", "arc"), (35, 120, 85, "85°", "arc"), (300, 360, 60, "?", "arc")], three, L=82)) +
                  "Three straight lines meet at a point. Work out the missing angle.", 60, [120, 85, 35],
                  "35° + 85° + the angle above them make a straight line: 180° − 120° = 60°. "
                  "The missing angle is vertically opposite that angle, so it is 60° too.", rnd))
    its.append(dq(fig(cross_svg(0, 80, ["2y", None, "80°", None], label=lab)) +
                  "Two straight lines cross. What is the value of <i>y</i>?", 40, [80, 50, 160],
                  "2<i>y</i> is vertically opposite 80°, so 2<i>y</i> = 80°. Then <i>y</i> = 80° ÷ 2 = 40°.", rnd))
    its.append(mcq("What is true about vertically opposite angles?", "They are equal",
                   ["They add up to 180°", "They add up to 90°", "They add up to 360°"],
                   "When two straight lines cross, the angles opposite each other are equal. Angles next to each other add up to 180°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says that vertically opposite angles add up to 180°. Is %s right?" % (n, he),
                   "No, they are equal", ["Yes, they are on a straight line", "Yes, they always do", "No, they add up to 360°"],
                   "Vertically opposite angles are equal. It is the angles next to each other (on a straight line) that add up to 180°.", rnd))
    its.append(mcq("Two straight lines cross. One of the angles is a right angle. What are the other three angles?",
                   "90°, 90° and 90°", ["90°, 180° and 90°", "45°, 90° and 45°", "270°, 90° and 270°"],
                   "The angle next to 90° is 180° − 90° = 90°, and the opposite angles are equal. So all four angles are 90°.", rnd))
    its.append(dq("Two straight lines cross. What do all four angles add up to?", 360, [180, 90, 720],
                  "The four angles go all the way around the crossing point, so they add up to 360°.", rnd))
    its.append(dq("Two straight lines cross. Two vertically opposite angles add up to 100°. How big is each of the other two angles?",
                  130, [50, 80, 260],
                  "The two equal opposite angles are 100° ÷ 2 = 50° each. The angles next to them are 180° − 50° = 130°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Vertically opposite angles", "items": its}


# ------------------------------------------------------------ set 3: triangles
def set_triangles(rnd, P):
    its = []
    q = "Work out the missing angle in this triangle."
    for a, b, rot, shown, v, wrong in [
        (50, 60, 0, {0: "50°", 1: "60°", 2: "?"}, 70, [250, 110, 130]),
        (35, 40, 0, {0: "35°", 1: "?", 2: "105°"}, 40, [220, 140, 145]),
        (28, 88, 180, {0: "28°", 1: "?", 2: "64°"}, 88, [272, 92, 152]),
        (72, 63, 15, {0: "?", 1: "63°", 2: "45°"}, 72, [252, 108, 117]),
        (24, 38, 0, {0: "24°", 1: "?", 2: "118°"}, 38, [218, 142, 156]),
    ]:
        pts = tri_pts(a, b, 190 if 180 - a - b > 100 else 140, rot)
        A = check_tri(pts, [a, b, 180 - a - b])
        known = [A[i] for i, t in shown.items() if t != "?"]
        e = "Angles in a triangle add up to 180°. %s + %s = %s, and 180° − %s = %s." % (
            D(known[0]), D(known[1]), D(sum(known)), D(sum(known)), D(v))
        its.append(dq(fig(shape_svg(pts, shown, "triangle")) + q, v, wrong, e, rnd))
    for a, v, rot in ((38, 52, 0), (61, 29, 90)):
        pts = tri_pts(90, a, 130, rot)       # right angle at corner 0, a at corner 1
        check_tri(pts, [90, a, 90 - a])
        its.append(dq(fig(shape_svg(pts, {1: "%d°" % a, 2: "?"}, "right-angled triangle", rights=(0,))) + q, v,
                      [180 - a, 90 + a, 270 - a],
                      "The small square is a right angle (90°). 90° + %d° = %d°, and 180° − %d° = %d°. "
                      "(Or: the other two angles add up to 90°, so 90° − %d° = %d°.)" % (a, 90 + a, 90 + a, v, a, v), rnd))
    q_iso = "This is an isosceles triangle. The marks show the two equal sides. Work out the missing angle."
    # apex given -> base angle
    for apex, rot in ((40, 0), (110, 0)):
        b = (180 - apex) / 2
        pts = tri_pts(b, b, 170 if apex > 90 else 100, rot)
        check_tri(pts, [b, b, apex])
        its.append(dq(fig(shape_svg(pts, {2: D(apex), 1: "?"}, "isosceles triangle", ticks=((1, 1), (2, 1)))) + q_iso, b,
                      [180 - apex, apex, (360 - apex) / 2],
                      "The two base angles are equal. 180° − %s = %s, and %s ÷ 2 = %s." % (D(apex), D(180 - apex), D(180 - apex), D(b)), rnd))
    # base given -> apex
    for b, rot, wrong in ((52, 0, [128, 52, 64]), (67, 180, [113, 67, 23])):
        apex = 180 - 2 * b
        pts = tri_pts(b, b, 150, rot)
        check_tri(pts, [b, b, apex])
        its.append(dq(fig(shape_svg(pts, {0: D(b), 2: "?"}, "isosceles triangle", ticks=((1, 1), (2, 1)))) + q_iso, apex,
                      wrong,
                      "The two base angles are equal, so both are %s. %s + %s = %s, and 180° − %s = %s."
                      % (D(b), D(b), D(b), D(2 * b), D(2 * b), D(apex)), rnd))
    pts = tri_pts(48, 48, 130)
    its.append(dq(fig(shape_svg(pts, {0: "48°", 2: "?"}, "triangle with two equal angles marked", eqs=((0, 1), (1, 1)))) +
                  "The two angles with a dash are equal. Work out the missing angle.", 84, [132, 48, 66],
                  "Both marked angles are 48°. 48° + 48° = 96°, and 180° − 96° = 84°.", rnd))
    pts = tri_pts(90, 45, 110)
    its.append(dq(fig(shape_svg(pts, {1: "?"}, "right-angled isosceles triangle", rights=(0,), ticks=((0, 1), (2, 1)))) +
                  "This right-angled triangle is isosceles. Work out the missing angle.", 45, [90, 135, 60],
                  "The other two angles share 180° − 90° = 90°. They are equal, so each is 90° ÷ 2 = 45°.", rnd))

    pts2 = tri_pts(55, 55, 120)

    def extend(P, A):
        E = (pts2[1][0] + 80, 0.0)
        P.line(pts2[1], E)
        P.mark(pts2[1], pts2[2], E, 125, "?")
    pts = pts2
    check_tri(pts, [55, 55, 70])
    its.append(dq(fig(shape_svg(pts, {0: "55°", 2: "70°"}, "triangle with one side made longer", extra=extend)) +
                  "One side of the triangle is made longer. Work out the angle marked ?", 125, [55, 70, 305],
                  "The angle inside the triangle at that corner is 180° − 55° − 70° = 55°. It is on a straight line with ?, so ? = 180° − 55° = 125°.", rnd))
    its.append(dq("Each angle of an equilateral triangle is …", 60, [90, 120, 180],
                  "An equilateral triangle has 3 equal angles that add up to 180°. 180° ÷ 3 = 60°.", rnd))
    its.append(mcq("Which three angles could be the angles of a triangle?", "50°, 60° and 70°",
                   ["50°, 60° and 80°", "90°, 90° and 20°", "100°, 100° and 160°"],
                   "The angles of a triangle add up to 180°. 50° + 60° + 70° = 180°. The others add up to 190°, 200° and 360°.", rnd))
    its.append(mcq("An isosceles triangle has one angle of 100°. What are the other two angles?", "40° and 40°",
                   ["80° and 80°", "130° and 130°", "100° and −20°"],
                   "100° is obtuse, so it must be the angle between the equal sides (two angles of 100° would be more than 180°). "
                   "180° − 100° = 80°, and 80° ÷ 2 = 40°.", rnd))
    its.append(mcq("A triangle has a right angle and an angle of 45°. What type of triangle is it?", "right-angled and isosceles",
                   ["right-angled and scalene", "equilateral", "obtuse-angled"],
                   "The third angle is 180° − 90° − 45° = 45°. Two equal angles mean two equal sides, so it is right-angled and isosceles.", rnd))
    its.append(dq("Two angles of a triangle are 37° and 98°. What is the third angle?", 45, [225, 55, 135],
                  "37° + 98° = 135°. 180° − 135° = 45°.", rnd))
    n, he, his = P.next()
    pts = tri_pts(65, 45, 140)
    its.append(mcq(fig(shape_svg(pts, {0: "65°", 1: "45°", 2: "?"}, "triangle")) +
                   "%s says the missing angle is 250°, because the angles in a triangle add up to 360°. Is %s right?" % (n, he),
                   "No, it is 70°", ["Yes, it is 250°", "No, it is 110°", "No, it is 20°"],
                   "The angles in a triangle add up to 180°, not 360°. 65° + 45° = 110°, and 180° − 110° = 70°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in triangles", "items": its}


# ------------------------------------------------------------ set 4: quadrilaterals and regular polygons
def set_polygons(rnd, P):
    its = []
    q = "Work out the missing angle in this quadrilateral."
    for (a, b, c), texts, v, wrong, rot in [
        ((80, 115, 70), {0: "80°", 1: "115°", 2: "70°", 3: "?"}, 95, [265, 85, 105], 0),
        ((70, 60, 120), {0: "70°", 1: "60°", 2: "120°", 3: "?"}, 110, [250, 70, 120], 0),
        ((100, 65, 120), {0: "100°", 1: "?", 2: "120°", 3: "75°"}, 65, [295, 115, 75], 0),
    ]:
        pts = quad_from(a, b, c, 150, 100, rot)
        known = [poly_angles(pts)[i] for i, t in texts.items() if t != "?"]
        e = "Angles in a quadrilateral add up to 360°. %s + %s + %s = %s, and 360° − %s = %s." % (
            D(known[0]), D(known[1]), D(known[2]), D(sum(known)), D(sum(known)), D(v))
        its.append(dq(fig(shape_svg(pts, texts, "quadrilateral")) + q, v, wrong, e, rnd))
    pts = quad_from(90, 90, 65, 150, 140)
    its.append(dq(fig(shape_svg(pts, {2: "65°", 3: "?"}, "quadrilateral with two right angles", rights=(0, 1))) + q, 115,
                  [205, 25, 65],
                  "The two small squares are 90° each. 90° + 90° + 65° = 245°, and 360° − 245° = 115°. "
                  "(Using 180° instead of 360° gives an impossible answer.)", rnd))
    pts = kite_pts(50, 90)
    its.append(dq(fig(shape_svg(pts, {2: "50°", 1: "?"}, "kite", rights=(0,), ticks=((0, 1), (3, 1), (1, 2), (2, 2)))) +
                  "This is a kite. Its two side angles are equal. Work out the missing angle.", 110, [220, 40, 130],
                  "50° + 90° = 140°. 360° − 140° = 220° is left for the two equal angles: 220° ÷ 2 = 110°.", rnd))
    A_ = O
    B_ = (140.0, 0.0)
    D_ = pol(O, 80, 70)
    C_ = (B_[0] + D_[0], B_[1] + D_[1])
    pts = [A_, B_, C_, D_]
    its.append(dq(fig(shape_svg(pts, {0: "70°", 1: "?"}, "parallelogram", ticks=((0, 1), (2, 1), (1, 2), (3, 2)))) +
                  "This is a parallelogram. Work out the missing angle.", 110, [70, 290, 20],
                  "In a parallelogram, angles next to each other add up to 180°: 180° − 70° = 110°. "
                  "Check: 70° + 110° + 70° + 110° = 360°.", rnd))
    its.append(dq("Three angles of a quadrilateral are 75°, 75° and 105°. What is the fourth angle?", 105, [255, 75, 165],
                  "75° + 75° + 105° = 255°. 360° − 255° = 105°.", rnd))
    its.append(dq("The angles inside any quadrilateral add up to …", 360, [180, 540, 400],
                  "A quadrilateral can be cut into 2 triangles from one corner: 2 × 180° = 360°.", rnd))
    # regular polygons
    n_, he, his = P.next()
    pent = regular_pts(5)
    its.append(dq(fig(shape_svg(pent, {0: "?"}, "regular pentagon", ticks=tuple((i, 1) for i in range(5)))) +
                  "This is a regular pentagon. What is the size of each angle inside it?", 108, [72, 540, 120],
                  "A pentagon makes 3 triangles from one corner: 3 × 180° = 540°. 540° ÷ 5 = 108°. "
                  "(360° ÷ 5 = 72° is the exterior angle, not the angle inside.)", rnd))
    hexa = regular_pts(6)
    its.append(dq(fig(shape_svg(hexa, {0: "?"}, "regular hexagon", ticks=tuple((i, 1) for i in range(6)))) +
                  "This is a regular hexagon. What is the size of each angle inside it?", 120, [60, 720, 108],
                  "A hexagon makes 4 triangles from one corner: 4 × 180° = 720°. 720° ÷ 6 = 120°. "
                  "(360° ÷ 6 = 60° is the exterior angle.)", rnd))

    def diags(P, A):
        for k in (2, 3):
            P.line(pent[0], pent[k], sw=2)
    its.append(dq(fig(shape_svg(pent, {}, "pentagon split into 3 triangles", extra=diags)) +
                  "The pentagon is split into triangles from one corner. What do the angles inside a pentagon add up to?", 540,
                  [360, 900, 108],
                  "There are 3 triangles, and each has angles adding up to 180°. 3 × 180° = 540°. "
                  "(5 × 180° = 900° counts 5 triangles, but there are only 3.)", rnd))
    its.append(dq("What do the angles inside a hexagon add up to?", 720, [1080, 360, 540],
                  "From one corner a hexagon splits into 6 − 2 = 4 triangles. 4 × 180° = 720°.", rnd))
    its.append(dq("What do the angles inside an octagon add up to?", 1080, [1440, 720, 135],
                  "From one corner an octagon splits into 8 − 2 = 6 triangles. 6 × 180° = 1,080°.", rnd))
    its.append(mcq_n("Lines are drawn from one corner of a hexagon to the other corners. How many triangles are made?", 4, [6, 3, 5],
                     "From one corner you can draw lines to 3 other corners (not to itself or its 2 neighbours). They make 6 − 2 = 4 triangles.", rnd))
    its.append(dq("What is the size of each angle inside a regular octagon?", 135, [45, 1080, 140],
                  "Each exterior angle is 360° ÷ 8 = 45°. Each angle inside is 180° − 45° = 135°. "
                  "(Or 1,080° ÷ 8 = 135°.)", rnd))
    its.append(dq("What is the size of each exterior angle of a regular pentagon?", 72, [108, 36, 60],
                  "The exterior angles of any polygon add up to 360°. 360° ÷ 5 = 72°. (108° is the angle inside.)", rnd))
    its.append(dq("What is the size of each angle inside a regular decagon (10 sides)?", 144, [36, 1440, 162],
                  "Each exterior angle is 360° ÷ 10 = 36°. Each angle inside is 180° − 36° = 144°.", rnd))
    its.append(mcq_n("Each exterior angle of a regular polygon is 45°. How many sides does it have?", 8, [4, 135, 9],
                     "The exterior angles add up to 360°. 360° ÷ 45° = 8, so it has 8 sides (an octagon).", rnd))
    its.append(mcq("Which regular polygon has angles of 90° inside it?", "a square",
                   ["an equilateral triangle", "a regular pentagon", "a regular hexagon"],
                   "A square has 4 right angles. An equilateral triangle has 60°, a regular pentagon 108° and a regular hexagon 120°.", rnd))
    its.append(mcq("%s says each angle inside a regular hexagon is 60°, because 360° ÷ 6 = 60°. Is %s right?" % (n_, he),
                   "No, it is 120°", ["Yes, it is 60°", "No, it is 720°", "No, it is 108°"],
                   "360° ÷ 6 = 60° is the exterior angle. The angle inside is 180° − 60° = 120°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in quadrilaterals and regular polygons", "items": its}


def mcq_n(q, v, wrong, e, rnd):
    return mcq(q, "{:,}".format(v), ["{:,}".format(w) for w in wrong], e, rnd)


# ------------------------------------------------------------ set 5: SATs-style problems
def set_problems(rnd, P):
    its = []
    # triangle sitting on a straight line, outside angles 130 and 115
    pts = tri_pts(50, 65, 130)

    def base_line(P_, A):
        L_, R_ = (-70.0, 0.0), (pts[1][0] + 70, 0.0)
        P_.line(pts[0], L_)
        P_.line(pts[1], R_)
        P_.mark(pts[0], pts[2], L_, 130, "130°")
        P_.mark(pts[1], pts[2], R_, 115, "115°")
    check_tri(pts, [50, 65, 65])
    its.append(dq(fig(shape_svg(pts, {2: "?"}, "triangle on a straight line", extra=base_line)) +
                  "A triangle sits on a straight line. Work out the missing angle.", 65, [245, 115, 50],
                  "Inside the triangle: 180° − 130° = 50° and 180° − 115° = 65°. Then 180° − 50° − 65° = 65°.", rnd))
    # isosceles with one base side made longer, outside angle 112
    ip = tri_pts(68, 68, 110)

    def ext(P_, A):
        E = (-70.0, 0.0)
        P_.line(ip[0], E)
        P_.mark(ip[0], ip[2], E, 112, "112°")
    its.append(dq(fig(shape_svg(ip, {2: "?"}, "isosceles triangle with one side made longer", ticks=((1, 1), (2, 1)), extra=ext)) +
                  "The triangle is isosceles. Work out the missing angle.", 44, [68, 56, 112],
                  "The base angle inside is 180° − 112° = 68°. Both base angles are 68°: 68° + 68° = 136°, and 180° − 136° = 44°.", rnd))
    # kite 70 top, 130 bottom
    kp = kite_pts(70, 130, w=54)
    kp = rot_all(kp, 0)
    its.append(dq(fig(shape_svg(kp, {2: "70°", 0: "130°", 1: "?"}, "kite", ticks=((0, 1), (3, 1), (1, 2), (2, 2)))) +
                  "This is a kite. Work out the missing angle.", 80, [160, 110, 50],
                  "The two side angles of a kite are equal. 70° + 130° = 200°, 360° − 200° = 160°, and 160° ÷ 2 = 80°.", rnd))
    # rectangle with a diagonal
    w = 150.0
    h = w * math.tan(math.radians(35))
    R = [(0.0, 0.0), (w, 0.0), (w, -h), (0.0, -h)]

    def diag(P_, A):
        P_.line(R[0], R[2], sw=2.5)
        P_.mark(R[0], R[1], R[2], 35, "35°")
        P_.mark(R[0], R[2], R[3], 55, "?")
    its.append(dq(fig(shape_svg(R, {}, "rectangle with a diagonal", rights=(1, 2, 3), extra=diag, split=(0,))) +
                  "A diagonal is drawn in a rectangle. Work out the missing angle.", 55, [145, 35, 125],
                  "The corner of a rectangle is a right angle. 90° − 35° = 55°.", rnd))
    # clock at 4 o'clock
    its.append(dq(fig(clock_svg(4)) + "What is the smaller angle between the hands of the clock at 4 o’clock?", 120, [240, 90, 40],
                  "The 12 hour spaces go around 360°, so each is 360° ÷ 12 = 30°. At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°.", rnd))
    # regular hexagon from 6 triangles
    hx = regular_pts(6, 70, start=0)

    def spokes(P_, A):
        for p in hx:
            P_.line(O, p, sw=2)
        P_.mark(O, hx[0], hx[1], 60, "a")
        P_.dot(O)
    its.append(dq(fig(shape_svg(hx, {}, "regular hexagon split into 6 triangles", extra=spokes)) +
                  "A regular hexagon is split into 6 equal triangles from its centre. What is angle <i>a</i>?", 60, [120, 30, 72],
                  "The 6 angles at the centre go all the way around: 360° ÷ 6 = 60°. (120° is the angle inside the hexagon at a corner.)", rnd))
    # x, x+20, 2x on a straight line
    its.append(dq(fig(line_svg(0, [40, 60, 80], ["x", "x + 20°", "2x"], L=110, label="angles on a straight line with x")) +
                  "The angles are on a straight line. What is the value of <i>x</i>?", 40, [85, 45, 80],
                  "<i>x</i> + <i>x</i> + 20° + 2<i>x</i> = 180°, so 4<i>x</i> + 20° = 180°. 4<i>x</i> = 160°, so <i>x</i> = 40°. "
                  "Check: 40° + 60° + 80° = 180°.", rnd))
    # isosceles x, x, 50
    tp = tri_pts(65, 65, 110)
    its.append(dq(fig(shape_svg(tp, {0: "x", 1: "x", 2: "50°"}, "isosceles triangle with angles x")) +
                  "The two angles marked <i>x</i> are equal. What is <i>x</i>?", 65, [130, 155, 50],
                  "180° − 50° = 130°. The two equal angles share it: 130° ÷ 2 = 65°.", rnd))
    # regular pentagon with a diagonal
    pe = regular_pts(5, 88)

    def pdiag(P_, A):
        P_.line(pe[0], pe[2], sw=2.5)
        P_.mark(pe[0], pe[1], pe[2], 36, "?")
    its.append(dq(fig(shape_svg(pe, {1: "108°"}, "regular pentagon with a diagonal", ticks=tuple((i, 1) for i in range(5)), extra=pdiag)) +
                  "This is a regular pentagon with one diagonal. Each angle inside the pentagon is 108°. Work out the missing angle.", 36,
                  [72, 108, 54],
                  "The diagonal makes an isosceles triangle with two sides of the pentagon. 180° − 108° = 72°, and the two equal angles are 72° ÷ 2 = 36°.", rnd))
    # two lines cross, a triangle on one side
    base = 120.0
    tA = O
    tB = pol(O, base, -20)
    tC = pol(O, base * math.sin(math.radians(75)) / math.sin(math.radians(65)), 20)
    tpts = [tA, tB, tC]
    check_tri(tpts, [40, 75, 65])

    def crossing(P_, A):
        P_.line(O, pol(O, 70, 160))
        P_.line(O, pol(O, 70, 200))
        P_.mark(O, pol(O, 70, 160), pol(O, 70, 200), 40, "40°")
    its.append(dq(fig(shape_svg(tpts, {1: "75°", 2: "?"}, "two crossing lines and a triangle", extra=crossing)) +
                  "Two straight lines cross. A triangle is drawn on one side. Work out the missing angle.", 65, [105, 140, 75],
                  "The angle inside the triangle at the crossing point is vertically opposite 40°, so it is 40°. "
                  "180° − 40° − 75° = 65°.", rnd))
    # word problems
    its.append(dq("What is the smaller angle between the hands of a clock at 5 o’clock?", 150, [210, 120, 180],
                  "Each hour space is 360° ÷ 12 = 30°. At 5 o’clock the hands are 5 spaces apart: 5 × 30° = 150°. "
                  "(210° is the larger angle, the other way round.)", rnd))
    n, he, his = P.next()
    its.append(dq("%s leans a ladder against a wall. The wall is upright and the ground is flat. The ladder makes an angle of 72° with the ground. "
                  "What angle does the ladder make with the wall?" % n, 18, [108, 288, 72],
                  "The wall, the ground and the ladder make a right-angled triangle. 180° − 90° − 72° = 18°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s cuts a round pizza into 8 equal slices from the centre. What angle does each slice make at the centre?" % n,
                  45, [22.5, 60, 135],
                  "The slices go all the way around the centre: 360°. 360° ÷ 8 = 45°. (22.5° comes from using 180°.)", rnd))
    its.append(dq("A pair of scissors is like two straight lines crossing at the screw. The handles are opened to an angle of 35°. "
                  "What is the angle between the blades?", 35, [145, 325, 55],
                  "The angle between the blades is vertically opposite the angle between the handles, so it is equal: 35°.", rnd))
    its.append(dq("The end of a roof is an isosceles triangle. The angle at the top is 110°. What angle does each sloping side make with the bottom beam?",
                  35, [70, 110, 55],
                  "180° − 110° = 70° is shared by the two equal angles: 70° ÷ 2 = 35°.", rnd))
    its.append(dq("The angles of a quadrilateral are <i>x</i>, <i>x</i>, 2<i>x</i> and 2<i>x</i>. What is <i>x</i>?", 60, [90, 30, 120],
                  "<i>x</i> + <i>x</i> + 2<i>x</i> + 2<i>x</i> = 6<i>x</i> = 360°, so <i>x</i> = 60°. (30° comes from using 180°.)", rnd))
    its.append(mcq("One angle of a triangle is 60°. Another angle is twice the size of the third angle. What are the other two angles?",
                   "40° and 80°", ["60° and 60°", "100° and 200°", "30° and 60°"],
                   "180° − 60° = 120° is left. If the smaller angle is 1 part, the larger is 2 parts: 3 parts = 120°, so 1 part = 40°. "
                   "The angles are 40° and 80°.", rnd))
    its.append(mcq_n("Each angle inside a regular polygon is 150°. How many sides does the polygon have?", 12, [30, 15, 6],
                     "Each exterior angle is 180° − 150° = 30°. The exterior angles add up to 360°: 360° ÷ 30° = 12 sides.", rnd))
    n, he, his = P.next()
    its.append(dq("%s turns from facing north to facing south-east, turning clockwise. How many degrees does %s turn?" % (n, he), 135,
                  [45, 225, 90],
                  "North to east is a right angle (90°). East to south-east is half a right angle (45°). 90° + 45° = 135°.", rnd))
    its.append(dq("In triangle ABC, angle A is 34° and angle B is 3 times the size of angle A. What is angle C?", 44,
                  [146, 112, 78],
                  "Angle B = 3 × 34° = 102°. 34° + 102° = 136°, and 180° − 136° = 44°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "SATs-style angle problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def strip_svg(svgs, caps, label, cw=None):
    """Several small figures side by side, each with a caption under it."""
    dims = []
    for s in svgs:
        m = re.search(r"viewBox='0 0 (\d+) (\d+)'", s)
        dims.append((int(m.group(1)), int(m.group(2))))
    cw = cw or max(max(w for w, h in dims), max(tw(c, 15) for c in caps) + 10)
    top = max(h for w, h in dims)
    out = []
    for k, (s, c) in enumerate(zip(svgs, caps)):
        w, h = dims[k]
        assert w <= cw, (c, w, cw)
        x, y = k * cw + (cw - w) / 2.0, (top - h) / 2.0
        out.append(re.sub(r"^<svg ", "<svg x='%.1f' y='%.1f' " % (x, y), s))
        out.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                   % (k * cw + cw / 2.0, top + 20, INK, c))
    return svg_wrap(int(cw * len(svgs)), top + 28, "".join(out), label)


def body_html():
    facts = strip_svg([line_svg(0, [60, 120], ["60°", "120°"], L=80), point_svg(0, [130, 100, 130], ["130°", "100°", "130°"], L=66),
                       cross_svg(0, 50, ["50°", "130°", "50°", "130°"], L=66)],
                      ["straight line: 180°", "around a point: 360°", "vertically opposite: equal"],
                      "angles on a straight line, around a point and vertically opposite", cw=210)
    tri = tri_pts(50, 70, 140)
    pent = regular_pts(5, 62)

    def diags(P, A):
        for k in (2, 3):
            P.line(pent[0], pent[k], sw=2)
    shapes = strip_svg([shape_svg(tri, {0: "50°", 1: "70°", 2: "60°"}, "triangle"),
                        shape_svg(quad_from(80, 115, 70, 130, 90), {0: "80°", 1: "115°", 2: "70°", 3: "95°"}, "quadrilateral"),
                        shape_svg(pent, {}, "pentagon split into 3 triangles", extra=diags)],
                       ["triangle: 180°", "quadrilateral: 360°", "pentagon: 3 × 180° = 540°"],
                       "angles in a triangle, a quadrilateral and a pentagon", cw=220)
    return (
        "<h2>Five angle facts</h2>"
        "<p>To find a missing angle, find the <b>fact</b> that fits the picture. Then add the angles you know and subtract from the total.</p>"
        "<figure class='sn-fig'>" + facts +
        "<figcaption>Angles on a straight line add up to 180°. Angles around a point add up to 360°. "
        "When two straight lines cross, the opposite angles are equal.</figcaption></figure>" +
        table(["Where the angles are", "Angle fact"], [
            ["On a straight line", "They add up to 180°"],
            ["Around a point", "They add up to 360°"],
            ["Vertically opposite (two lines cross)", "They are equal"],
            ["Inside a triangle", "They add up to 180°"],
            ["Inside a quadrilateral", "They add up to 360°"],
        ]) +
        ex("Example", "Two angles on a straight line are 47° and ?. Find ?.",
           "Straight line, so 180°. 180° − 47° = 133°. Check: 47° + 133° = 180°.", "133°") +
        "<h2>Triangles and quadrilaterals</h2>"
        "<p>The angles inside a triangle add up to <b>180°</b>. A quadrilateral splits into 2 triangles, so its angles add up to <b>360°</b>. "
        "In an isosceles triangle, the two base angles are equal. Marks on the sides show which two sides are equal.</p>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>From one corner, a shape with n sides splits into n − 2 triangles.</figcaption></figure>" +
        ex("Isosceles triangle", "The angle at the top of an isosceles triangle is 40°. Find each base angle.",
           "180° − 40° = 140°. The two base angles are equal: 140° ÷ 2 = 70°.", "70° each") +
        "<h2>Regular polygons</h2>"
        "<p>A regular polygon has equal sides and equal angles. Walk around it: you turn through the <b>exterior angles</b>, "
        "and they add up to 360°. So each exterior angle is 360° ÷ number of sides. The angle inside is 180° minus that.</p>" +
        table(["Regular polygon", "Exterior angle", "Angle inside"], [
            ["Equilateral triangle (3 sides)", "360° ÷ 3 = 120°", "60°"],
            ["Square (4 sides)", "360° ÷ 4 = 90°", "90°"],
            ["Pentagon (5 sides)", "360° ÷ 5 = 72°", "108°"],
            ["Hexagon (6 sides)", "360° ÷ 6 = 60°", "120°"],
            ["Octagon (8 sides)", "360° ÷ 8 = 45°", "135°"],
        ]) +
        ex("Regular pentagon", "Find each angle inside a regular pentagon.",
           "Triangles: 3 × 180° = 540°, and 540° ÷ 5 = 108°. Or exterior angles: 360° ÷ 5 = 72°, and 180° − 72° = 108°.", "108°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using 360° for a straight line, or 180° around a point", "Straight line: 180°. All the way round: 360°"],
            ["Using 180° for a quadrilateral", "A quadrilateral is 2 triangles: 360°"],
            ["Thinking vertically opposite angles add up to 180°", "Opposite angles are equal. Angles next to each other add up to 180°"],
            ["Not halving for the two equal angles of an isosceles triangle", "Subtract the top angle from 180°, then divide by 2"],
            ["Giving 360° ÷ n as the angle inside a regular polygon", "360° ÷ n is the exterior angle. Inside: 180° minus it"],
            ["Measuring a diagram marked “not drawn accurately”", "Calculate with angle facts. Do not measure"],
        ])
    )


FAQ = [
    {"q": "What angle facts do Year 6 pupils need to know?",
     "a": "Angles on a straight line add up to 180°, angles around a point add up to 360°, vertically opposite angles are equal, "
          "angles in a triangle add up to 180° and angles in a quadrilateral add up to 360°."},
    {"q": "How do you find a missing angle in a triangle?",
     "a": "Add the two angles you know and subtract the total from 180°. In an isosceles triangle the two base angles are equal, so you may need to halve."},
    {"q": "How do you work out the angles inside a regular polygon?",
     "a": "Divide 360° by the number of sides to get the exterior angle, then subtract it from 180°. For a regular pentagon: 360° ÷ 5 = 72°, so each angle inside is 108°."},
    {"q": "Are missing-angle questions in the Year 6 SATs?",
     "a": "Yes, angle questions often appear in the reasoning papers (Papers 2 and 3). Diagrams are usually marked “not drawn accurately”, so pupils must calculate with angle facts, not measure."},
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
    rnd = random.Random(6616)
    P = People(rnd)
    sets = [set_line_point(rnd, P), set_vertical(rnd, P), set_triangles(rnd, P), set_polygons(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "angles", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Angles: Missing Angles in Triangles, Quadrilaterals and Regular Polygons",
        "seo_title": "Year 6 Angles Worksheets: Missing Angles, Vertically Opposite, Triangles and Regular Polygons (Free, with Answers)",
        "short_title": "Angles",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 6: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Find unknown angles in any triangles, quadrilaterals, and regular polygons; recognise angles where they meet at a point, "
                         "are on a straight line, or are vertically opposite, and find missing angles.",
        "meta_desc": "Free Year 6 maths worksheets on angles: angles on a straight line and around a point, vertically opposite angles, "
                     "missing angles in triangles and quadrilaterals, and angles in regular polygons, plus SATs-style problems. "
                     "100 questions with an answer key, following the National Curriculum.",
        "key_big": "Straight line 180°, around a point 360°, triangle 180°, quadrilateral 360°, and vertically opposite angles are equal.",
        "key_sub": "Add the angles you know and subtract from the right total. In a regular polygon each exterior angle is 360° ÷ number of sides, "
                   "and the angle inside is 180° minus that.",
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
            if m:
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
        mark_large(u, "(angles on a straight line|three straight lines|two crossing lines and a triangle|triangle on a straight line)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
