# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Angles on a straight line and at a point
(Australian Curriculum v9.0, AC9M6M04)
  python3 tools/gen_au_maths_y6_angles.py
Angles on a straight line add to 180°, angles at a point add to 360°, vertically opposite angles are equal;
use these facts to find unknown angles and explain the reasoning. Australian English.
HTML attributes use single quotes (no backslashes in the JSON).

Every figure is drawn to its stated angles: each marked angle is measured from the drawing
and checked against its value (also the "?" and letter angles). Labels are checked so that
they do not touch a line, an arc or another label, and sit inside the angle they name.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


def D(v):
    """Angle in degrees as text: 65°, 270° (whole degrees only)."""
    assert abs(v - round(v)) < 1e-9 and 0 < v < 1000, v
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


def point_svg(rot, parts, texts, L=80, label="angles at a point"):
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
    """Analog clock at h o'clock with the smaller angle between the hands marked. Square picture."""
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
    return svg_wrap(120, 120, "".join(s), label or "analog clock showing %d o’clock" % h)



def mcq_n(q, v, wrong, e, rnd):
    return mcq(q, str(v), [str(w) for w in wrong], e, rnd)


THREE = "three straight lines through a point"
CROSS = "two straight lines crossing"


# ------------------------------------------------------------ set 1: angles on a straight line
def set_line(rnd, P):
    its = []
    q = "The angles are on a straight line. Work out the missing angle."
    for rot, parts, texts, v, wrong, e in [
        (0, [40, 140], ["40°", "?"], 140, [320, 220, 40],
         "Angles on a straight line add up to 180°. 180° − 40° = 140°."),
        (0, [115, 65], ["115°", "?"], 65, [245, 295, 115],
         "Angles on a straight line add up to 180°. 180° − 115° = 65°. (360° − 115° = 245° would be for angles at a point.)"),
        (25, [132, 48], ["?", "48°"], 132, [312, 228, 48],
         "The line is tilted, but it is still straight: 180° − 48° = 132°."),
        (-20, [73, 107], ["73°", "?"], 107, [287, 253, 73],
         "Angles on a straight line add up to 180°. 180° − 73° = 107°."),
        (0, [90, 35, 55], [None, "35°", "?"], 55, [235, 125, 145],
         "The small square is a right angle: 90°. 90° + 35° = 125°, and 180° − 125° = 55°."),
        (0, [48, 62, 70], ["48°", "?", "70°"], 62, [242, 118, 132],
         "First add the angles you know: 48° + 70° = 118°. Then subtract from 180°: 180° − 118° = 62°."),
        (10, [25, 95, 60], ["25°", "95°", "?"], 60, [240, 120, 155],
         "25° + 95° = 120°. Angles on a straight line add up to 180°, so 180° − 120° = 60°."),
        (-12, [37, 108, 35], ["37°", "108°", "?"], 35, [215, 145, 72],
         "37° + 108° = 145°, and 180° − 145° = 35°."),
    ]:
        its.append(dq(fig(line_svg(rot, parts, texts)) + q, v, wrong, e, rnd))
    its.append(dq(fig(line_svg(-10, [55, 55, 70], ["a", "a", "70°"], label="angles on a straight line, two marked a")) +
                  "The two angles marked <i>a</i> are equal. What is <i>a</i>?", 55, [110, 145, 70],
                  "180° − 70° = 110°. The two equal angles share it: 110° ÷ 2 = 55°.", rnd))
    its.append(dq(fig(line_svg(0, [30, 60, 90], ["x", "2x", "3x"], L=100, label="angles x, 2x and 3x on a straight line")) +
                  "The angles are on a straight line. What is the value of <i>x</i>?", 30, [60, 90, 36],
                  "<i>x</i> + 2<i>x</i> + 3<i>x</i> = 6<i>x</i>, and 6<i>x</i> = 180°. So <i>x</i> = 180° ÷ 6 = 30°. "
                  "(60° comes from using 360°.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [50, 54, 76], ["50°", "a", "76°"], label="angles on a straight line")) +
                   "%s says <i>a</i> = 50°, because it looks the same size as the 50° angle. Is %s right?" % (n, he),
                   "No, a = 54°", ["Yes, a = 50°", "No, a = 126°", "No, a = 234°"],
                   "Do not trust how an angle looks: work it out. 50° + 76° = 126°, and 180° − 126° = 54°.", rnd))
    its.append(dq(fig(rays_svg([0, 62, 90], [(0, 62, 62, "62°", "arc"), (62, 90, 28, "?", "arc"), (0, 90, 90, None, "right")],
                               "right angle split into two angles", L=96)) +
                  "The whole angle is a right angle. Work out the missing angle.", 28, [118, 298, 152],
                  "A right angle is 90°. 90° − 62° = 28°. (180° − 62° = 118° would be for a straight line.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [130, 50], ["130°", "?"])) +
                   "%s says the missing angle is 230°, because 360° − 130° = 230°. Is %s right?" % (n, he),
                   "No, it is 50°", ["Yes, it is 230°", "No, it is 130°", "No, it is 310°"],
                   "The angles are on a straight line, so they add up to 180°, not 360°. 180° − 130° = 50°.", rnd))
    its.append(dq("Angles on a straight line add up to …", 180, [360, 90, 100],
                  "A straight angle is a half turn: 180°. Two right angles make a straight line.", rnd))
    its.append(dq("Two angles sit on a straight line. One of them is 74°. How big is the other angle?", 106, [286, 254, 16],
                  "180° − 74° = 106°. Check: 74° + 106° = 180°.", rnd))
    its.append(dq("Three equal angles together make a straight line. How big is each angle?", 60, [120, 90, 45],
                  "The three angles add up to 180°. 180° ÷ 3 = 60°. (120° would come from using 360°.)", rnd))
    its.append(mcq("Two angles are next to each other. One is 125° and the other is 65°. Can they make a straight line?",
                   "No, they add up to 190°", ["Yes, they add up to 180°", "Yes, one angle is obtuse", "No, they add up to 360°"],
                   "125° + 65° = 190°. Angles on a straight line must add up to exactly 180°, so they cannot.", rnd))
    its.append(dq("Two angles on a straight line. One angle is 4 times as big as the other. How big is the smaller angle?",
                  36, [45, 72, 144],
                  "The angles are 1 part and 4 parts: 5 parts = 180°. 1 part = 180° ÷ 5 = 36°. (The larger angle is 4 × 36° = 144°.)", rnd))
    its.append(mcq("Two angles on a straight line. One is an acute angle of 38°. What is the other angle?",
                   "obtuse, 142°", ["acute, 52°", "reflex, 322°", "acute, 38°"],
                   "180° − 38° = 142°. It is between 90° and 180°, so it is obtuse. (52° is 90° − 38°, which is for a right angle.)", rnd))
    its.append(dq("A straight line is split into three angles. Two of them are 65° and 47°. What is the third angle?", 68, [112, 248, 115],
                  "65° + 47° = 112°. 180° − 112° = 68°. (112° is the two angles added, not the missing one.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles on a straight line", "items": its}


# ------------------------------------------------------------ set 2: angles at a point
def set_point(rnd, P):
    its = []
    q = "The angles are at a point. Work out the missing angle."
    for rot, parts, texts, v, wrong, e in [
        (0, [110, 135, 115], ["110°", "135°", "?"], 115, [245, 250, 225],
         "Angles at a point add up to 360°. 110° + 135° = 245°, and 360° − 245° = 115°."),
        (30, [140, 85, 135], ["140°", "?", "135°"], 85, [275, 220, 225],
         "140° + 135° = 275°. Angles at a point add up to 360°: 360° − 275° = 85°."),
        (0, [90, 125, 60, 85], [None, "125°", "60°", "?"], 85, [275, 175, 95],
         "The small square is 90°. 90° + 125° + 60° = 275°, and 360° − 275° = 85°. (175° comes from forgetting the right angle.)"),
        (15, [100, 120, 75, 65], ["100°", "120°", "?", "65°"], 75, [285, 140, 65],
         "100° + 120° + 65° = 285°. 360° − 285° = 75°."),
        (0, [200, 95, 65], ["200°", "95°", "?"], 65, [295, 160, 265],
         "One angle is reflex. 200° + 95° = 295°, and 360° − 295° = 65°."),
    ]:
        its.append(dq(fig(point_svg(rot, parts, texts)) + q, v, wrong, e, rnd))
    its.append(dq(fig(point_svg(90, [230, 130], ["?", "130°"], label="a reflex angle and an obtuse angle at a point")) +
                  "The two angles are at a point. Work out the reflex angle marked ?", 230, [50, 490, 310],
                  "Angles at a point add up to 360°. 360° − 130° = 230°. (50° comes from using 180°, and 490° from adding.)", rnd))
    its.append(dq(fig(point_svg(90, [120, 120, 120], ["b", "b", "b"], label="three equal angles at a point")) +
                  "The three angles marked <i>b</i> are equal. What is <i>b</i>?", 120, [60, 90, 180],
                  "Angles at a point add up to 360°. 360° ÷ 3 = 120°. (180° ÷ 3 = 60° would be a straight line.)", rnd))
    its.append(dq(fig(point_svg(20, [100, 130, 130], ["100°", "y", "y"], label="angles at a point, two marked y")) +
                  "The two angles marked <i>y</i> are equal. What is <i>y</i>?", 130, [260, 40, 100],
                  "360° − 100° = 260°. The two equal angles share it: 260° ÷ 2 = 130°.", rnd))
    its.append(dq(fig(point_svg(30, [120, 80, 160], ["120°", "x", "2x"], label="angles at a point with x and 2x")) +
                  "The angles are at a point. What is the value of <i>x</i>?", 80, [20, 160, 240],
                  "<i>x</i> + 2<i>x</i> = 3<i>x</i>, and 3<i>x</i> = 360° − 120° = 240°. So <i>x</i> = 240° ÷ 3 = 80°.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(point_svg(0, [150, 100, 110], ["150°", "100°", "?"])) +
                   "%s says the missing angle is 250°, because 150° + 100° = 250°. Is %s right?" % (n, he),
                   "No, it is 110°", ["Yes, it is 250°", "No, it is 150°", "No, it is 360°"],
                   "Add the angles you know, then subtract from 360°: 360° − 250° = 110°. "
                   "250° is the total of the two angles, not the missing angle.", rnd))
    its.append(dq("Angles at a point add up to …", 360, [180, 270, 90],
                  "Angles at a point make a full turn (a revolution): 360°.", rnd))
    its.append(dq("Five equal angles fit exactly around a point. How big is each angle?", 72, [36, 90, 60],
                  "At a point: 360°. 360° ÷ 5 = 72°. (36° comes from 180° ÷ 5.)", rnd))
    its.append(dq("Four angles are at a point. One is a right angle and the other three are equal. How big is each of the three equal angles?",
                  90, [30, 120, 270],
                  "360° − 90° = 270°. The three equal angles share it: 270° ÷ 3 = 90°.", rnd))
    its.append(dq("Four angles are at a point. Three of them are 95°, 120° and 85°. What is the fourth angle?", 60, [300, 145, 180],
                  "95° + 120° + 85° = 300°. 360° − 300° = 60°.", rnd))
    its.append(dq("A reflex angle of 250° and one other angle make a full turn. How big is the other angle?", 110, [70, 610, 250],
                  "A full turn is 360°. 360° − 250° = 110°. (70° comes from 250° − 180°, and 610° from adding.)", rnd))
    its.append(mcq_n("How many angles of 45° fit exactly around a point?", 8, [4, 6, 12],
                     "360° ÷ 45° = 8. (4 is how many fit on a straight line: 180° ÷ 45° = 4.)", rnd))
    its.append(dq("Three angles are at a point. Two of them are 140° each. What is the third angle?", 80, [280, 220, 40],
                  "140° + 140° = 280°. 360° − 280° = 80°. (220° comes from subtracting only one 140°.)", rnd))
    its.append(dq("Three angles at a point are <i>x</i>, 2<i>x</i> and 3<i>x</i>. What is <i>x</i>?", 60, [30, 180, 72],
                  "<i>x</i> + 2<i>x</i> + 3<i>x</i> = 6<i>x</i> = 360°, so <i>x</i> = 60°. (30° comes from using 180°.)", rnd))
    its.append(mcq("Can angles of 150°, 120° and 100° fit around a point with no gaps or overlaps?",
                   "No, they add up to 370°", ["Yes, they add up to 360°", "No, they add up to 180°", "Yes, two are obtuse"],
                   "150° + 120° + 100° = 370°. Angles at a point must add up to exactly 360°, so they would overlap by 10°.", rnd))
    its.append(dq("Two angles are at a point. One is 5 times as big as the other. How big is the larger angle?", 300, [60, 150, 288],
                  "1 part + 5 parts = 6 parts = 360°. 1 part = 60°, so the larger angle is 5 × 60° = 300° (a reflex angle). "
                  "(150° comes from using 180°.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles at a point", "items": its}


# ------------------------------------------------------------ set 3: vertically opposite angles
def set_vertical(rnd, P):
    its = []
    for rot, a, texts, v, wrong in [
        (0, 40, ["40°", None, "?", None], 40, [140, 320, 50]),
        (20, 115, [None, "?", None, "65°"], 65, [115, 295, 25]),
        (-30, 72, ["?", None, "72°", None], 72, [108, 288, 18]),
        (10, 35, [None, "145°", None, "?"], 145, [35, 215, 55]),
        (40, 25, [None, "?", None, "155°"], 155, [25, 205, 65]),
    ]:
        its.append(dq(fig(cross_svg(rot, a, texts, label=CROSS)) + "Two straight lines cross. Work out the missing angle.", v, wrong,
                      "The missing angle is vertically opposite the %s angle, so they are equal: %s." % (D(v), D(v)), rnd))
    for rot, a, texts, v, wrong in [
        (0, 58, ["58°", "?", None, None], 122, [58, 302, 32]),
        (15, 130, [None, "?", "130°", None], 50, [130, 230, 40]),
        (-20, 75, [None, None, "75°", "?"], 105, [75, 285, 15]),
        (5, 34, ["?", "146°", None, None], 34, [146, 214, 56]),
    ]:
        k = [t for t in texts if t and t != "?"][0]
        its.append(dq(fig(cross_svg(rot, a, texts, label=CROSS)) + "Two straight lines cross. Work out the missing angle.", v, wrong,
                      "The missing angle and %s are next to each other on a straight line, so they add up to 180°. 180° − %s = %s."
                      % (k, k, D(v)), rnd))
    its.append(mcq(fig(cross_svg(0, 64, ["64°", "a", "b", "c"], label=CROSS)) + "Two straight lines cross. Find <i>a</i>, <i>b</i> and <i>c</i>.",
                   "a = 116°, b = 64°, c = 116°",
                   ["a = 64°, b = 116°, c = 64°", "a = 116°, b = 116°, c = 116°", "a = 26°, b = 64°, c = 26°"],
                   "<i>a</i> is on a straight line with 64°: 180° − 64° = 116°. <i>b</i> is vertically opposite 64°, so it is 64°. "
                   "<i>c</i> is vertically opposite <i>a</i>, so it is 116°.", rnd))
    its.append(mcq(fig(cross_svg(30, 105, ["p", "q", "r", "105°"], label=CROSS)) + "Two straight lines cross. Find <i>p</i>, <i>q</i> and <i>r</i>.",
                   "p = 75°, q = 105°, r = 75°",
                   ["p = 105°, q = 75°, r = 105°", "p = 75°, q = 75°, r = 75°", "p = 255°, q = 105°, r = 255°"],
                   "<i>p</i> and 105° are on a straight line: 180° − 105° = 75°. <i>q</i> is vertically opposite 105°, so 105°. "
                   "<i>r</i> is vertically opposite <i>p</i>: 75°.", rnd))
    its.append(mcq(fig(cross_svg(10, 55, ["a", "b", "c", "d"], label=CROSS)) + "Which two angles are vertically opposite?",
                   "a and c", ["a and b", "c and d", "a and d"],
                   "Vertically opposite angles are across the crossing point from each other: <i>a</i> and <i>c</i> (also <i>b</i> and <i>d</i>). "
                   "Angles next to each other, like <i>a</i> and <i>b</i>, add up to 180°.", rnd))
    its.append(dq(fig(rays_svg([0, 45, 125, 180, 225, 305],
                               [(0, 45, 45, "45°", "arc"), (45, 125, 80, "80°", "arc"), (225, 305, 80, "?", "arc")], THREE, L=82)) +
                  "Three straight lines meet at a point. Work out the missing angle.", 80, [100, 55, 45],
                  "The missing angle is vertically opposite the 80° angle, so it is also 80°.", rnd))
    its.append(dq(fig(cross_svg(0, 80, ["2y", None, "80°", None], label=CROSS)) +
                  "Two straight lines cross. What is the value of <i>y</i>?", 40, [80, 50, 160],
                  "2<i>y</i> is vertically opposite 80°, so 2<i>y</i> = 80°. Then <i>y</i> = 80° ÷ 2 = 40°.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(cross_svg(0, 86, ["86°", "a", None, None], label=CROSS)) +
                   "%s says <i>a</i> = 86°, because the two angles look the same size. Is %s right?" % (n, he),
                   "No, a = 94°", ["Yes, a = 86°", "No, a = 274°", "No, a = 4°"],
                   "<i>a</i> is next to 86° on a straight line, not opposite it. 180° − 86° = 94°. "
                   "Angles can look equal and still be different, so use the angle facts.", rnd))
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
    its.append(dq("Two straight lines cross. One angle is 27°. How big is the angle vertically opposite it?", 27, [153, 333, 63],
                  "Vertically opposite angles are equal, so it is also 27°. (153° is the angle next to it.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Vertically opposite angles", "items": its}


# ------------------------------------------------------------ set 4: unknown angles in diagrams
def set_diagrams(rnd, P):
    its = []
    q3 = "Three straight lines meet at a point. Work out the missing angle."
    its.append(dq(fig(rays_svg([0, 40, 115, 180, 220, 295],
                               [(0, 40, 40, "40°", "arc"), (40, 115, 75, "75°", "arc"), (115, 180, 65, "?", "arc")], THREE, L=82)) + q3,
                  65, [245, 115, 75],
                  "The three angles above the flat line are on a straight line. 40° + 75° = 115°, and 180° − 115° = 65°.", rnd))
    its.append(dq(fig(rays_svg([0, 40, 115, 180, 220, 295],
                               [(0, 40, 40, "40°", "arc"), (115, 180, 65, "65°", "arc"), (220, 295, 75, "?", "arc")], THREE, L=82)) + q3,
                  75, [65, 40, 105],
                  "Step 1: the angle between 40° and 65° on the straight line is 180° − 40° − 65° = 75°. "
                  "Step 2: the missing angle is vertically opposite it, so it is 75°.", rnd))
    its.append(dq(fig(rays_svg([0, 55, 120, 180, 235, 300],
                               [(0, 55, 55, "55°", "arc"), (120, 180, 60, "?", "arc"), (235, 300, 65, "65°", "arc")], THREE, L=82)) + q3,
                  60, [120, 65, 300],
                  "The angle between 55° and ? is vertically opposite 65°, so it is 65°. "
                  "Then on the straight line: 180° − 55° − 65° = 60°.", rnd))
    its.append(mcq(fig(rays_svg([0, 50, 110, 180, 230, 290],
                                [(0, 50, 50, "50°", "arc"), (50, 110, 60, "60°", "arc"), (110, 180, 70, "a", "arc"),
                                 (180, 230, 50, "b", "arc"), (230, 290, 60, "c", "arc")], THREE, L=90)) +
                   "Three straight lines meet at a point. Find <i>a</i>, <i>b</i> and <i>c</i>.",
                   "a = 70°, b = 50°, c = 60°",
                   ["a = 70°, b = 60°, c = 50°", "a = 250°, b = 50°, c = 60°", "a = 70°, b = 130°, c = 120°"],
                   "<i>a</i>: 180° − 50° − 60° = 70° (straight line). <i>b</i> is vertically opposite 50°, and <i>c</i> is vertically opposite 60°.", rnd))
    lab5 = "two crossing lines and one more line from the point"
    its.append(dq(fig(rays_svg([0, 180, 70, 250, 125],
                               [(0, 70, 70, "70°", "arc"), (70, 125, 55, "55°", "arc"), (125, 180, 55, "?", "arc")], lab5, L=86)) +
                  "Two straight lines cross, and one more line starts at the crossing point. Work out the missing angle.",
                  55, [125, 110, 70],
                  "The three angles above the flat line are on a straight line. 70° + 55° = 125°, and 180° − 125° = 55°.", rnd))
    its.append(dq(fig(rays_svg([0, 180, 70, 250, 125],
                               [(70, 125, 55, "55°", "arc"), (125, 180, 55, "55°", "arc"), (180, 250, 70, "?", "arc")], lab5, L=86)) +
                  "Two straight lines cross, and one more line starts at the crossing point. Work out the missing angle.",
                  70, [110, 55, 250],
                  "Step 1: on the straight line, the angle at the right is 180° − 55° − 55° = 70°. "
                  "Step 2: the missing angle is vertically opposite it, so it is 70°.", rnd))
    its.append(dq(fig(rays_svg([0, 90, 180, 270, 310],
                               [(0, 90, 90, None, "right"), (270, 310, 40, "?", "arc"), (310, 360, 50, "50°", "arc")],
                               "two lines at right angles and one more line", L=80)) +
                  "Two straight lines cross at right angles. One more line starts at the crossing point. Work out the missing angle.",
                  40, [130, 310, 50],
                  "The lines cross at right angles, so all four angles they make are 90°. The angle between the downward line and the right-hand line is 90°, so ? = 90° − 50° = 40°.", rnd))
    its.append(dq(fig(point_svg(0, [60, 85, 215], ["60°", "?", "215°"])) + "The angles are at a point. Work out the missing angle.",
                  85, [275, 145, 300],
                  "60° + 215° = 275°. Angles at a point add up to 360°: 360° − 275° = 85°.", rnd))
    its.append(dq(fig(line_svg(0, [45, 135], ["x", "3x"], label="angles x and 3x on a straight line")) +
                  "The angles are on a straight line. What is the value of <i>x</i>?", 45, [90, 60, 135],
                  "<i>x</i> + 3<i>x</i> = 4<i>x</i> = 180°. So <i>x</i> = 180° ÷ 4 = 45°. (90° comes from using 360°.)", rnd))
    its.append(dq(fig(cross_svg(0, 40, ["a + 20°", None, "2a", None], L=110, label=CROSS)) +
                  "Two straight lines cross. What is the value of <i>a</i>?", 20, [40, 160, 80],
                  "The two angles are vertically opposite, so they are equal: 2<i>a</i> = <i>a</i> + 20°. Take <i>a</i> from both sides: "
                  "<i>a</i> = 20°. Check: 2 × 20° = 40° and 20° + 20° = 40°.", rnd))
    its.append(dq(fig(cross_svg(20, 60, ["2x", None, None, "4x"], L=90, label=CROSS)) +
                  "Two straight lines cross. What is the value of <i>x</i>?", 30, [60, 120, 15],
                  "2<i>x</i> and 4<i>x</i> are next to each other on a straight line: 6<i>x</i> = 180°, so <i>x</i> = 30°. "
                  "(60° comes from using 360°.)", rnd))
    its.append(dq(fig(rays_svg([0, 65, 180, 245, 290],
                               [(0, 65, 65, "65°", "arc"), (245, 290, 45, "?", "arc"), (290, 360, 70, "70°", "arc")], lab5, L=86)) +
                  "Two straight lines cross, and one more line starts at the crossing point. Work out the missing angle.",
                  45, [115, 110, 65],
                  "Step 1: next to 65° on the straight line is 180° − 65° = 115°. "
                  "Step 2: the angle below, between the sloping line and the flat line, is vertically opposite it, so it is 115°. "
                  "Step 3: 115° − 70° = 45°.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [61, 59, 60], ["61°", "?", "60°"], L=100, label="angles on a straight line")) +
                   "%s says the missing angle is 60°, because all three angles look equal. Is %s right?" % (n, he),
                   "No, it is 59°", ["Yes, it is 60°", "No, it is 61°", "No, it is 239°"],
                   "61° + 60° = 121°, and 180° − 121° = 59°. The angles look almost the same, but they are not equal.", rnd))
    its.append(dq(fig(point_svg(15, [50, 50, 50, 105, 105], ["50°", "50°", "50°", "q", "q"], L=84,
                                label="five angles at a point, two marked q")) +
                  "The angles are at a point. The two angles marked <i>q</i> are equal. What is <i>q</i>?", 105, [210, 15, 50],
                  "50° + 50° + 50° = 150°. 360° − 150° = 210°, and 210° ÷ 2 = 105°.", rnd))
    its.append(dq(fig(rays_svg([0, 40, 90, 180], [(0, 40, 40, "40°", "arc"), (40, 90, 50, "?", "arc"), (90, 180, 90, None, "right")],
                               "angles on a straight line with a right angle", L=92)) +
                  "The angles are on a straight line. Work out the missing angle.", 50, [140, 40, 230],
                  "The square shows a right angle (90°). 90° + 40° = 130°, and 180° − 130° = 50°. (Or: 90° − 40° = 50°.)", rnd))
    its.append(mcq(fig(cross_svg(25, 128, ["128°", "a", "b", None], label=CROSS)) +
                   "Two straight lines cross. Find <i>a</i> and <i>b</i>.",
                   "a = 52°, b = 128°", ["a = 128°, b = 52°", "a = 52°, b = 52°", "a = 232°, b = 128°"],
                   "<i>a</i> is on a straight line with 128°: 180° − 128° = 52°. <i>b</i> is vertically opposite 128°, so <i>b</i> = 128°.", rnd))
    its.append(dq(fig(point_svg(0, [60] * 6, ["x"] * 6, L=84, label="six equal angles made by three straight lines")) +
                  "Three straight lines cross at one point and make six equal angles. What is <i>x</i>?", 60, [30, 120, 45],
                  "Angles at a point add up to 360°. 360° ÷ 6 = 60°. (30° comes from 180° ÷ 6.)", rnd))
    its.append(dq(fig(rays_svg([0, 180, 50, 250],
                               [(0, 50, 50, "50°", "arc"), (180, 250, 70, "70°", "arc"), (250, 360, 110, "?", "arc")],
                               "a straight line and two lines from a point on it", L=86)) +
                  "The flat line is straight. Work out the missing angle.", 110, [130, 70, 240],
                  "The 70° angle and ? are on the straight line below it: 180° − 70° = 110°. The 50° angle does not help here.", rnd))
    its.append(mcq(fig(rays_svg([0, 50, 120, 180, 230, 300],
                                [(0, 50, 50, "a", "arc"), (50, 120, 70, "b", "arc"), (120, 180, 60, "c", "arc"),
                                 (180, 230, 50, "d", "arc"), (230, 300, 70, "e", "arc"), (300, 360, 60, "f", "arc")], THREE, L=82)) +
                   "Three straight lines meet at a point. Which angle is vertically opposite angle <i>b</i>?",
                   "e", ["c", "d", "f"],
                   "Follow the two lines that make angle <i>b</i> through the crossing point. The angle between them on the other side is <i>e</i>.", rnd))
    n, he, his = P.next()
    its.append(dq(fig(line_svg(15, [90, 48, 42], [None, "?", "42°"], label="angles on a straight line with a right angle")) +
                  "The angles are on a straight line. Work out the missing angle.", 48, [138, 228, 42],
                  "The square is 90°. 90° + 42° = 132°, and 180° − 132° = 48°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find unknown angles in diagrams", "items": its}


# ------------------------------------------------------------ set 5: reasoning and multi-step problems
def set_problems(rnd, P):
    its = []
    its.append(dq(fig(clock_svg(4)) + "What is the smaller angle between the hands of the analog clock at 4 o’clock?", 120, [240, 90, 40],
                  "The 12 hour spaces go around 360°, so each is 360° ÷ 12 = 30°. At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°.", rnd))
    its.append(dq(fig(clock_svg(10)) + "What is the smaller angle between the hands of the analog clock at 10 o’clock?", 60, [300, 30, 120],
                  "From 10 to 12 is 2 hour spaces. Each space is 30°, so 2 × 30° = 60°. (300° is the reflex angle the other way round.)", rnd))
    its.append(dq("What is the smaller angle between the hands of a clock at 5 o’clock?", 150, [210, 120, 180],
                  "Each hour space is 360° ÷ 12 = 30°. At 5 o’clock the hands are 5 spaces apart: 5 × 30° = 150°. "
                  "(210° is the larger angle, the other way round.)", rnd))
    its.append(dq("At 3 o’clock, what is the reflex angle between the hands of a clock?", 270, [90, 180, 360],
                  "The smaller angle is a right angle, 90°. The reflex angle goes the other way round: 360° − 90° = 270°.", rnd))
    its.append(dq("The minute hand turns for 20 minutes. Through how many degrees does it turn?", 120, [20, 60, 240],
                  "The minute hand turns 360° in 60 minutes, so 6° each minute. 20 × 6° = 120°. (240° is the other 40 minutes.)", rnd))
    its.append(mcq("At which time do the hands of a clock make a straight angle (180°)?", "6 o’clock",
                   ["3 o’clock", "9 o’clock", "12 o’clock"],
                   "At 6 o’clock the hands point to 12 and 6, in a straight line: 6 × 30° = 180°. At 3 and 9 o’clock they make a right angle.", rnd))
    n, he, his = P.next()
    its.append(dq("%s cuts a round pizza into 6 equal slices. Every cut goes through the centre. What angle does each slice make at the centre?" % n,
                  60, [30, 120, 300],
                  "The slices go all the way around the centre: 360°. 360° ÷ 6 = 60°. (30° comes from using 180°.)", rnd))
    n, he, his = P.next()
    its.append(dq("A pizza is cut into 8 equal slices from the centre. %s eats 3 slices. What angle at the centre do the slices that are left make?" % n,
                  225, [135, 45, 180],
                  "Each slice is 360° ÷ 8 = 45°. 5 slices are left: 5 × 45° = 225°. (135° is the 3 slices that were eaten.)", rnd))
    its.append(dq(fig(point_svg(10, [100, 80, 95, 85], ["100°", "80°", "95°", "?"], label="pizza cuts meeting at the centre")) +
                  "A pizza is cut into 4 slices of different sizes. The cuts meet at the centre. Work out the angle of the last slice.",
                  85, [275, 175, 95],
                  "The angles at the centre add up to 360°. 100° + 80° + 95° = 275°, and 360° − 275° = 85°.", rnd))
    its.append(dq("In a roof truss, a sloping strut meets the straight bottom beam. The angle on one side of the strut is 58°. "
                  "What is the angle on the other side?", 122, [302, 58, 32],
                  "The two angles are on a straight line (the beam), so they add up to 180°. 180° − 58° = 122°.", rnd))
    its.append(dq("At the top of a roof truss, the two sloping rafters meet the upright king post. Each rafter makes an angle of 62° with the post. "
                  "What is the angle between the two rafters?", 124, [62, 56, 236],
                  "The angle between the rafters is made of the two angles next to the post: 62° + 62° = 124°.", rnd))
    its.append(dq("In a roof truss, two struts meet the straight bottom beam at the same point. Above the beam they make three angles: 48°, 75° and one more. "
                  "What is the third angle?", 57, [237, 123, 75],
                  "The three angles are on the straight beam, so they add up to 180°. 48° + 75° = 123°, and 180° − 123° = 57°.", rnd))
    its.append(dq("A pair of scissors is like two straight lines crossing at the screw. The handles are opened to an angle of 35°. "
                  "What is the angle between the blades?", 35, [145, 325, 55],
                  "The angle between the blades is vertically opposite the angle between the handles, so it is equal: 35°.", rnd))
    its.append(dq("The legs of a folding beach chair cross like an X. The angle between the legs at the top is 50°. "
                  "What is the angle between the legs at the side of the X?", 130, [50, 310, 40],
                  "The side angle is next to the 50° angle on a straight leg, so 180° − 50° = 130°.", rnd))
    its.append(dq("Two straight roads cross. One angle between them is 72°. What do the two obtuse angles add up to?", 216, [108, 144, 288],
                  "Each obtuse angle is 180° − 72° = 108°. The two obtuse angles are vertically opposite, so they are equal: 108° + 108° = 216°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s faces north and turns clockwise until %s faces south-east. How many degrees does %s turn?" % (n, he, he), 135,
                  [45, 225, 90],
                  "North to east is a right angle (90°). East to south-east is half a right angle (45°). 90° + 45° = 135°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s faces east and turns clockwise until %s faces north. How many degrees does %s turn?" % (n, he, he), 270,
                  [90, 180, 360],
                  "Clockwise from east: to south is 90°, to west is 180°, to north is 270°. (90° would be turning anticlockwise.)", rnd))
    its.append(dq("A ceiling fan has 5 equal blades spaced evenly around the centre. What is the angle between two blades next to each other?",
                  72, [36, 60, 90],
                  "The blades share the full turn: 360° ÷ 5 = 72°. (36° comes from using 180°.)", rnd))
    its.append(dq("Three straight lines meet at a point. Five of the six angles are 40°, 60°, 80°, 40° and 60°. What is the sixth angle?",
                  80, [100, 280, 60],
                  "All six angles are at a point, so they add up to 360°. 40° + 60° + 80° + 40° + 60° = 280°, and 360° − 280° = 80°. "
                  "Check: it is vertically opposite the other 80° angle.", rnd))
    its.append(dq("A skateboard ramp starts on flat ground and rises at an angle of 25° to the ground. "
                  "What is the obtuse angle between the ramp and the ground on the other side of where it starts?", 155, [335, 65, 25],
                  "The two angles are on the straight ground, so they add up to 180°. 180° − 25° = 155°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reasoning and multi-step problems", "items": its}


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
                      ["straight line: 180°", "at a point: 360°", "vertically opposite: equal"],
                      "angles on a straight line, at a point and vertically opposite", cw=210)
    worked = rays_svg([0, 40, 115, 180, 220, 295],
                      [(0, 40, 40, "40°", "arc"), (115, 180, 65, "65°", "arc"), (220, 295, 75, "?", "arc")], THREE, L=82)
    return (
        "<h2>Three angle facts</h2>"
        "<p>To find an unknown angle, look for the <b>fact</b> that fits the picture. Add the angles you know, then subtract from the total.</p>"
        "<figure class='sn-fig'>" + facts +
        "<figcaption>Angles on a straight line add up to 180°. Angles at a point add up to 360°. "
        "When two straight lines cross, the vertically opposite angles are equal.</figcaption></figure>" +
        table(["Where the angles are", "Angle fact"], [
            ["On a straight line", "They add up to 180° (a straight angle)"],
            ["At a point (all the way round)", "They add up to 360° (a revolution)"],
            ["Vertically opposite (two straight lines cross)", "They are equal"],
            ["Next to each other where two lines cross", "They add up to 180°"],
        ]) +
        "<h2>Worked examples</h2>" +
        ex("Straight line", "Three angles on a straight line are 48°, 70° and ?. Find ?.",
           "Straight line, so the total is 180°. 48° + 70° = 118°. 180° − 118° = 62°. Check: 48° + 70° + 62° = 180°.", "62°") +
        ex("At a point", "Angles at a point are 200°, 95° and ?. Find ?.",
           "At a point, so the total is 360°. 200° + 95° = 295°. 360° − 295° = 65°.", "65°") +
        "<figure class='sn-fig'>" + worked +
        "<figcaption>Two steps: the angle between 40° and 65° is 180° − 40° − 65° = 75°. "
        "The ? is vertically opposite it, so ? = 75°.</figcaption></figure>" +
        ex("Explain your reasoning", "Three straight lines meet at a point (picture above). Find ?.",
           "Step 1: 40°, 65° and the angle between them are on a straight line, so that angle is 180° − 105° = 75°. "
           "Step 2: ? is vertically opposite that angle, and vertically opposite angles are equal.", "75°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using 360° for a straight line, or 180° at a point", "Straight line: 180°. All the way round: 360°"],
            ["Adding the known angles and giving that total as the answer", "Add the known angles, then subtract the total from 180° or 360°"],
            ["Thinking two angles are equal because they look the same", "Only use a fact: vertically opposite, or marked as equal. Then calculate"],
            ["Thinking vertically opposite angles add up to 180°", "Opposite angles are equal. Angles next to each other add up to 180°"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about angles in the Australian Curriculum?",
     "a": "They learn that angles on a straight line add up to 180°, angles at a point add up to 360° and vertically opposite angles are equal, "
          "and they use these facts to find unknown angles and explain their reasoning."},
    {"q": "How do you find a missing angle on a straight line?",
     "a": "Add the angles you know and subtract the total from 180°. For example, if the other angles are 48° and 70°, the missing angle is 180° − 118° = 62°."},
    {"q": "What are vertically opposite angles?",
     "a": "When two straight lines cross they make four angles. The angles opposite each other are vertically opposite and always equal; "
          "the angles next to each other add up to 180°."},
    {"q": "Should students measure missing angles with a protractor?",
     "a": "No, they should calculate them with the angle facts and show each step. Angles that look equal may not be, "
          "and diagrams in tests are often not drawn to scale."},
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
    rnd = random.Random(6815)
    P = People(rnd)
    sets = [set_line(rnd, P), set_point(rnd, P), set_vertical(rnd, P), set_diagrams(rnd, P), set_problems(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "angles-on-a-line-and-at-a-point", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Angles on a Straight Line and at a Point",
        "seo_title": "Year 6 Angles on a Straight Line and at a Point Worksheets: Vertically Opposite and Unknown Angles (Free, with Answers)",
        "short_title": "Angles on a line and at a point",
        "domain": "Measurement",
        "standard_code": "AC9M6M04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify the relationships between angles on a straight line, angles at a point and vertically opposite angles; "
                         "use these to determine unknown angles, communicating reasoning",
        "meta_desc": "Free Year 6 maths worksheets for the Australian Curriculum: angles on a straight line (180°), angles at a point (360°) "
                     "and vertically opposite angles, finding unknown angles in diagrams and explaining the reasoning, with clock, "
                     "pizza and roof truss problems. 100 questions with an answer key.",
        "key_big": "Angles on a straight line add up to 180°, angles at a point add up to 360°, and vertically opposite angles are equal.",
        "key_sub": "Add the angles you know, then subtract from 180° or 360°. Do not trust how an angle looks: use a fact and show each step.",
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
        mark_large(u, "(angles on a straight line|three straight lines|two crossing lines|a straight line and two lines|six equal angles)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
