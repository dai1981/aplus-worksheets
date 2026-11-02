# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Measuring angles (National Curriculum in England, Geometry – properties of shapes)
  python tools/gen_uk_maths_y5_angles.py
HTML attributes use single quotes (no backslashes in the JSON).

Every angle is drawn exactly at its size (trig, 0° = pointing right, anticlockwise, SVG y goes down);
every marked angle is measured back from the drawing and checked against its value.
Labels are checked so that they do not touch a line, an arc or another label.
Protractor: inner scale has 0 on the right, outer scale has 0 on the left; marks every 5°, numbers every 10°.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
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


FILL2 = "#eef6f0"

class PPic:
    """Collects strokes (as sampled points, for collision checks and the bounding box) and labels (as boxes)."""

    def __init__(self):
        self.el = []          # (z, svg) z: 0 back, 1 strokes, 2 labels
        self.pts = []         # sampled points of every stroke
        self.boxes = []       # (x0, y0, x1, y1) of every label
        self.soft = []        # points that labels may cover (rays across a protractor scale)

    def line(self, p, q, col=GREEN, sw=3, soft=False, cap_="round", dash=None):
        self.el.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='%s'%s/>"
                        % (p[0], p[1], q[0], q[1], col, sw, cap_, " stroke-dasharray='%s'" % dash if dash else "")))
        n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 2))
        pts = [(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)]
        (self.soft if soft else self.pts).extend(pts)

    def arc(self, V, r, a, b, col=GREEN, sw=2.2, fill=None, z=1):
        """Arc around V from math angle a to b (counterclockwise, b > a)."""
        assert b > a
        n = max(4, int((b - a) / 2))
        pts = [pol(V, r, a + (b - a) * i / n) for i in range(n + 1)]
        big = 1 if b - a > 180 else 0
        p, q = pts[0], pts[-1]
        if b - a >= 359.9:
            d = "M%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f" % (
                p + (r, r) + pol(V, r, a + 180) + (r, r) + p)
        else:
            d = "M%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f" % (p + (r, r, big) + q)
        if fill:
            d2 = d if b - a >= 359.9 else "M%.1f,%.1f L" % V + d[1:] + " Z"
            self.el.append((0, "<path d='%s' fill='%s' stroke='none'/>" % (d2, fill)))
        if col:
            self.el.append((z, "<path d='%s' fill='none' stroke='%s' stroke-width='%g'/>" % (d, col, sw)))
            self.pts.extend(pts)
        else:
            self.soft.extend(pts)
        return pts

    def ray(self, V, deg, L, col=GREEN, sw=3, soft=False):
        E = pol(V, L, deg)
        self.line(V, pol(V, L - 4, deg), col, sw, soft)
        # arrowhead
        a1, a2 = pol(E, 11, deg + 180 - 24), pol(E, 11, deg + 180 + 24)
        self.el.append((1, "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (E + a1 + a2 + (col,))))
        (self.soft if soft else self.pts).extend([E, a1, a2])

    def dot(self, V, r=4, col=INK):
        self.el.append((1, "<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (V[0], V[1], r, col)))
        self.pts.extend([(V[0] + r * math.cos(t / 4.0), V[1] + r * math.sin(t / 4.0)) for t in range(26)])

    def square_mark(self, V, d1, s=12):
        q1, q3 = pol(V, s, d1), pol(V, s, d1 + 90)
        q2 = (q1[0] + q3[0] - V[0], q1[1] + q3[1] - V[1])
        self.el.append((1, "<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                        % (q1 + q2 + q3 + (INK,))))
        self.line(q1, q2, INK, 0.01)
        self.line(q2, q3, INK, 0.01)
        self.el.pop(); self.el.pop()

    def box_of(self, cx, cy, t, fs, bold=True):
        w, h = tw(t, fs, bold), fs * 0.74
        return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

    def clear(self, b, gap=2.5, soft_ok=True):
        x0, y0, x1, y1 = b[0] - gap, b[1] - gap, b[2] + gap, b[3] + gap
        for p in self.pts:
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                return False
        for o in self.boxes:
            if not (o[2] + gap <= b[0] or b[2] + gap <= o[0] or o[3] + gap <= b[1] or b[3] + gap <= o[1]):
                return False
        return True

    def label(self, cx, cy, t, fs=16, col=INK, bold=True, halo=False, check=True):
        b = self.box_of(cx, cy, t, fs, bold)
        if check:
            assert self.clear(b), ("label collides", t, cx, cy)
        self.boxes.append(b)
        self.el.append((2, "<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='middle'%s>%s</text>"
                        % (cx, cy + fs * 0.36, fs, " font-weight='700'" if bold else "", col,
                           " stroke='#fff' stroke-width='3.5' paint-order='stroke'" if halo else "", t)))

    def rlabel(self, cx, cy, t, fs, col, rot, gap=1.5):
        """Label turned by rot degrees (clockwise), like the numbers on a real protractor.
        Checked in its own turned frame against strokes and other labels."""
        w, h = tw(t, fs, False), fs * 0.74
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

        def to_local(p, L):
            dx, dy = p[0] - L[0], p[1] - L[1]
            return (dx * L[5] + dy * L[6], -dx * L[6] + dy * L[5])

        def outline(L, n=6):
            out = []
            for i in range(n + 1):
                for u, v in ((-L[2] / 2 + L[2] * i / n, -L[3] / 2), (-L[2] / 2 + L[2] * i / n, L[3] / 2),
                             (-L[2] / 2, -L[3] / 2 + L[3] * i / n), (L[2] / 2, -L[3] / 2 + L[3] * i / n)):
                    out.append((L[0] + u * L[5] - v * L[6], L[1] + u * L[6] + v * L[5]))
            return out

        def inside(p, L, g):
            u, v = to_local(p, L)
            return abs(u) <= L[2] / 2 + g and abs(v) <= L[3] / 2 + g
        me = (cx, cy, w, h, rot, c, s)
        others = getattr(self, "rl", [])
        assert not any(inside(p, me, gap) for p in self.pts), ("label collides with a stroke", t)
        for o in others:
            assert not any(inside(p, me, gap) for p in outline(o)), ("label collides with label", t)
            assert not any(inside(p, o, gap) for p in outline(me)), ("label collides with label", t)
        self.rl = others + [me]
        self.soft.extend(outline(me, 1))
        self.el.append((2, "<text x='%.1f' y='%.1f' font-size='%d' fill='%s' text-anchor='middle' "
                           "transform='rotate(%.1f %.1f %.1f)'>%s</text>"
                        % (cx, cy + fs * 0.36, fs, col, rot, cx, cy, t)))

    def svg(self, label, pad=5, square=False, min_w=0):
        allp = self.pts + self.soft + [(b[0], b[1]) for b in self.boxes] + [(b[2], b[3]) for b in self.boxes]
        x0 = min(p[0] for p in allp) - pad
        y0 = min(p[1] for p in allp) - pad
        x1 = max(p[0] for p in allp) + pad
        y1 = max(p[1] for p in allp) + pad
        W, H = int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))
        W = max(W, min_w)
        if square:
            W = H = max(W, H)
        elif W == H:
            W += 1                                     # keep out of the larger 'square' print size
        dx, dy = (W - (x1 - x0)) / 2 - x0, (H - (y1 - y0)) / 2 - y0
        body = "".join(s for z, s in sorted(self.el, key=lambda t: t[0]))
        return svg_wrap(W, H, "<g transform='translate(%.1f %.1f)'>%s</g>" % (dx, dy, body), label), W, H


PR = 185          # protractor radius
PO, PI = 18, 31   # outer and inner label radius, measured in from the edge


def protractor_svg(rays, label=None, mark=True):
    """Protractor centered on the vertex. rays: directions in deg (0 = right). Rays are red and cross the scales."""
    P = PPic()
    V = (0.0, 0.0)
    R = PR
    # body
    P.el.append((0, "<path d='M%.1f,0 A%d,%d 0 0 0 %.1f,0 L%.1f,14 L%.1f,14 Z' fill='%s' stroke='%s' stroke-width='2.4'/>"
                 % (R, R, R, -R, -R, R, FILL2, GREEN)))
    P.pts += [pol(V, R, t) for t in range(0, 181)] + [(x, 14) for x in range(-R, R + 1, 2)]
    P.line((-R, 0), (R, 0), GREEN, 1.6)
    for t in range(0, 181, 5):
        L = 11 if t % 10 == 0 else 6
        P.line(pol(V, R - L, t), pol(V, R, t), INK, 1.8 if t % 10 == 0 else 1.2, cap_="butt")
    # center mark
    P.line((0, -8), (0, 8), INK, 1.6)
    # labels: outer scale (0 at the left) and inner scale (0 at the right), turned like on a real protractor
    for t in range(0, 181, 10):
        for rr, val, col in [(R - PO, 180 - t, INK), (R - PI, t, GREEN)]:
            c = pol(V, rr, t)
            if t in (0, 180):              # the end numbers sit upright, just above the base line
                x = math.copysign(min(abs(c[0]), R - PO - 17.5), c[0]) if rr == R - PI else c[0]
                P.rlabel(x, -7.0, str(val), 14, col, 0)
            else:
                P.rlabel(c[0], c[1], str(val), 14, col, 90 - t)
    for i, d in enumerate(rays):
        P.ray(V, d, R + 20, col=RED, sw=2.6, soft=True)
    P.dot(V, 4.5, INK)
    # labels go on top of the rays with a white halo
    P.el = [(z, s.replace("<text ", "<text stroke='#fff' stroke-width='3' paint-order='stroke' "))
            for z, s in P.el]
    return P.svg(label or "protractor measuring an angle", pad=4)[0]


# ------------------------------------------------------------ Year 5 figures
def angle_fig(d, rot, label="marked angle", L=80, text=None, r=None):
    """Two arms from O: one at rot, one at rot + d (anticlockwise). The marked angle is d (it may be reflex)."""
    P = Pic()
    P.line(O, pol(O, L, rot))
    P.line(O, pol(O, L, rot + d))
    if d == 90 and not text:
        P.mark(O, pol(O, L, rot), pol(O, L, rot + d), 90, kind="right", ccw=True)
    else:
        rr = r or (24 if d < 40 else 20 if d > 180 else 18)
        P.mark(O, pol(O, L, rot), pol(O, L, rot + d), d, text, r=rr, ccw=True)
    P.dot(O)
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
        assert w <= cw, (c, w, cw)
        x, y = k * cw + (cw - w) / 2.0, (top - h) / 2.0
        inner = re.sub(r"^<svg [^>]*>", "", s)
        assert inner.endswith("</svg>")
        out.append("<g transform='translate(%.1f %.1f)'>%s</g>" % (x, y, inner[:-6]))
        out.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                   % (k * cw + cw / 2.0, top + fs + 6, fs, INK, c))
    return svg_wrap(int(math.ceil(cw * len(svgs))), top + fs + 12, "".join(out), label)


def abcd_svg(angles, label, L=42):
    """Four marked angles labelled A, B, C, D. angles: (size, rot) or (size, rot, arm length)."""
    svgs = []
    for a in angles:
        d, rot = a[0], a[1]
        svgs.append(angle_fig(d, rot, "angle", L=a[2] if len(a) > 2 else L))
    return strip_svg(svgs, ["A", "B", "C", "D"], label, fs=18)


def letter_q(q, ans, e):
    """Choices A–D in order (the quiz keeps that order)."""
    ch = ["A", "B", "C", "D"]
    return {"q": q, "c": ch, "a": ch.index(ans), "e": e, "fix": True}


def mc(q, correct, wrong, e, rnd):
    return mcq(q, correct, wrong, e, rnd)


# ------------------------------------------------------------ set 1: acute, obtuse, reflex
KIND_E = {
    "acute": "An acute angle is smaller than a right angle: less than 90°.",
    "right angle": "A right angle is exactly 90°, a quarter turn. The small square shows it.",
    "obtuse": "An obtuse angle is bigger than a right angle but smaller than a straight line: between 90° and 180°.",
    "straight line": "Two arms that make a straight line make an angle of 180°, half a turn.",
    "reflex": "A reflex angle is bigger than a straight line: between 180° and 360°. Look at the arc: it goes round the outside.",
}


def kind(d):
    return "acute" if d < 90 else "right angle" if d == 90 else "obtuse" if d < 180 else "straight line" if d == 180 else "reflex"


def set_types(rnd, P):
    its = []
    q = "What type of angle is marked?"
    for d, rot, wrong in [
        (35, 15, ["obtuse", "reflex", "right angle"]),
        (125, 0, ["acute", "reflex", "right angle"]),
        (230, 0, ["obtuse", "acute", "straight line"]),
        (90, 30, ["acute", "obtuse", "reflex"]),
        (320, 20, ["acute", "obtuse", "right angle"]),
        (160, 10, ["reflex", "acute", "straight line"]),
        (70, 100, ["obtuse", "right angle", "reflex"]),
        (200, 200, ["obtuse", "straight line", "acute"]),
        (180, 0, ["obtuse", "reflex", "right angle"]),
        (100, 160, ["acute", "right angle", "reflex"]),
    ]:
        k = kind(d)
        e = KIND_E[k] + " This angle is %s." % D(d)
        if k == "reflex":
            e += " (The angle on the other side is %s, but the arc marks the big angle.)" % D(360 - d)
        if d == 90:
            e += " Turning the angle does not change its size."
        its.append(mcq(fig(angle_fig(d, rot)) + q, k, wrong, e, rnd))
    for d, wrong in [(175, ["reflex", "straight line", "acute"]), (185, ["obtuse", "straight line", "acute"]),
                     (89, ["right angle", "obtuse", "reflex"]), (270, ["obtuse", "straight line", "right angle"])]:
        k = kind(d)
        e = KIND_E[k].split(":")[0] + ". %s is %s." % (D(d), {
            "obtuse": "more than 90° but less than 180°", "reflex": "more than 180° but less than 360°",
            "acute": "less than 90° (only just!)"}[k])
        its.append(mcq("An angle measures %s. What type of angle is it?" % D(d), k, wrong, e, rnd))
    its.append(mcq("Which of these angles is reflex?", "210°", ["120°", "175°", "90°"],
                   "A reflex angle is more than 180°. Only 210° is more than 180°. 175° is close to 180°, but it is still obtuse.", rnd))
    its.append(mcq("Which of these angles is obtuse?", "135°", ["45°", "90°", "225°"],
                   "An obtuse angle is between 90° and 180°. 135° is the only one. 225° is more than 180°, so it is reflex.", rnd))
    its.append(mcq("A reflex angle is …", "more than 180° and less than 360°",
                   ["more than 90° and less than 180°", "less than 90°", "exactly 180°"],
                   "Reflex angles are bigger than a half turn (180°) but smaller than a whole turn (360°).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says an angle of 190° is obtuse because it is bigger than 90°. Is %s right?" % (n, he),
                   "No, it is reflex", ["Yes, it is obtuse", "No, it is acute", "No, it is a right angle"],
                   "Obtuse angles are bigger than 90° but smaller than 180°. 190° is more than 180°, so it is reflex.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?", "acute, right angle, obtuse, reflex",
                   ["acute, obtuse, right angle, reflex", "reflex, obtuse, right angle, acute", "right angle, acute, obtuse, reflex"],
                   "Acute is less than 90°, a right angle is 90°, obtuse is between 90° and 180°, and reflex is more than 180°.", rnd))
    its.append(mcq("At which time is the smaller angle between the hands of a clock acute?", "1 o’clock",
                   ["4 o’clock", "6 o’clock", "3 o’clock"],
                   "At 1 o’clock the hands are 1 hour space apart: 30°, which is acute. 3 o’clock is a right angle (90°), "
                   "4 o’clock is obtuse (120°) and 6 o’clock is a straight line (180°).", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Acute, obtuse and reflex angles", "items": its}


# ------------------------------------------------------------ set 2: estimate and compare
def set_estimate(rnd, P):
    its = []
    q = "Which is the best estimate for the marked angle?"
    for d, rot, best, wrong in [
        (28, 0, 30, [150, 60, 90]),
        (62, 20, 60, [120, 30, 90]),
        (118, 5, 120, [60, 90, 180]),
        (147, 10, 150, [30, 210, 120]),
        (43, 70, 45, [135, 90, 15]),
        (172, 0, 170, [10, 190, 120]),
        (235, 0, 240, [120, 60, 300]),
        (300, 30, 300, [60, 240, 120]),
        (205, 10, 200, [160, 20, 270]),
        (275, 15, 270, [90, 180, 330]),
    ]:
        if d < 90:
            e = "The angle is smaller than a right angle (90°), so it is acute. About %s fits. (It is %s.)" % (D(best), D(d))
        elif d < 180:
            e = ("The angle is bigger than a right angle (90°) but smaller than a straight line (180°), so it is obtuse. "
                 "About %s fits. (It is %s.)" % (D(best), D(d)))
        else:
            e = ("The arc goes round the outside, so the angle is reflex: more than 180°. The angle on the other side is about %s, "
                 "so the marked angle is about 360° − %s = %s. (It is %s.)" % (D(360 - best), D(360 - best), D(best), D(d)))
        if d < 180 and (180 - best) in wrong:
            e += " About %s would be a %s angle." % (D(180 - best), "much wider" if best < 90 else "much smaller")
        its.append(mcq(fig(angle_fig(d, rot)) + q, "about " + D(best), ["about " + D(w) for w in wrong], e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(60, 0), (240, 0), (125, 0), (165, 0)], lab)) + "Which angle is closest to 120°?", "C",
                        "C is a bit more than a right angle: about 120°. A is about 60°. B is reflex (about 240°): its inside gap "
                        "looks like 120°, but the arc marks the big angle. D is nearly a straight line."))
    its.append(letter_q(fig(abcd_svg([(170, 0), (95, 0), (30, 0), (215, 0)], lab)) + "Which angle is reflex?", "D",
                        "A reflex angle is more than 180°. Only the arc in D goes round more than a straight line. A is obtuse, nearly 180°."))
    its.append(letter_q(fig(abcd_svg([(250, 0, 30), (170, 0, 46), (100, 0, 50), (60, 0, 56)], lab)) +
                        "Which angle is the largest?", "A",
                        "The size of an angle is the amount of turn, not the length of the arms. A is reflex (about 250°), so it is the largest, "
                        "even though its arms are the shortest."))
    its.append(letter_q(fig(abcd_svg([(85, 0), (40, 0), (15, 0), (135, 0)], lab)) + "Which angle is closest to 45°?", "B",
                        "45° is half a right angle. B is about half of a right angle. A is nearly a right angle, C is very small and D is obtuse."))
    its.append(letter_q(fig(abcd_svg([(80, 0), (260, 0), (30, 0), (145, 0)], lab)) + "Which angle is obtuse?", "D",
                        "Obtuse means between 90° and 180°. D is about 145°. B is reflex: the gap between its arms looks obtuse, "
                        "but the arc marks the angle round the outside."))
    its.append(mcq("An angle is a little smaller than a right angle. Which could it be?", "80°", ["100°", "180°", "170°"],
                   "A right angle is 90°. A little smaller than 90° is about 80°. 100° is a little bigger.", rnd))
    its.append(mcq("An angle is a little more than half a turn. Which could it be?", "195°", ["165°", "95°", "360°"],
                   "Half a turn is 180°, so a little more is about 195°. 165° is a little less than half a turn, and 95° is a little more than a quarter turn.", rnd))
    its.append(mcq("Which is larger: three right angles or 250°?", "three right angles", ["250°", "they are equal", "you cannot tell"],
                   "Three right angles are 3 × 90° = 270°, and 270° is more than 250°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s estimates a reflex angle as about 70°. Why must %s be wrong?" % (n, he),
                   "A reflex angle is more than 180°", ["70° is too big for any angle", "A reflex angle is less than 90°",
                                                        "A reflex angle is exactly 180°"],
                   "Every reflex angle is more than 180°, so its estimate must be more than 180°. 70° may be the angle on the other side: "
                   "then the reflex angle is about 360° − 70° = 290°.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?", "59°, 95°, 185°, 205°",
                   ["95°, 59°, 185°, 205°", "59°, 95°, 205°, 185°", "205°, 185°, 95°, 59°"],
                   "Compare the hundreds, then the tens: 59° &lt; 95° &lt; 185° &lt; 205°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Estimate and compare angles", "items": its}


# ------------------------------------------------------------ set 3: protractor
def read_cands(v):
    c = [D(180 - v)]
    if v % 10 == 5:
        c += [D(v - 4), D(v + 5), D(v - 5)]       # counted a 5-degree mark as 1 degree; read the next number
    else:
        c += [D(v + 10), D(v - 10), D(v + 1)]
    return c


def size_word(v):
    return "smaller than a right angle" if v < 90 else "bigger than a right angle"


def set_protractor(rnd, P):
    its = []
    q = "What is the size of the angle?"
    for v in (40, 65, 110, 155, 80, 135):
        e = ("The bottom arm is on 0 on the right, so read the <b>inner</b> scale, which starts at 0 on the right. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The small marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " The outer scale says %d there, but it starts from the other side. The angle is %s, so %s makes sense." % (
            180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([0, v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for v in (30, 55, 120, 145, 70, 100):
        e = ("The bottom arm is on 0 on the left, so read the <b>outer</b> scale, which starts at 0 on the left. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The small marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " (The inner scale says %d there.) The angle is %s, so %s makes sense." % (180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([180, 180 - v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for a, b in ((20, 95), (40, 150)):
        v = b - a
        its.append(mcq(fig(protractor_svg([a, b], "protractor measuring an angle with neither arm on 0")) +
                       "Neither arm is on 0. What is the size of the angle?", D(v), [D(b), D(180 - b), D(a), D(a + b)],
                       "On the inner scale one arm is at %d and the other is at %d. The angle is the difference: %d° − %d° = %d°."
                       % (a, b, b, a, v), rnd))
    its.append(mcq("Where do you put the centre of the protractor when you measure an angle?", "on the vertex",
                   ["at the end of an arm", "on the 90 mark", "in the middle of an arm"],
                   "The centre goes on the vertex, where the two arms meet. Then line up one arm with 0.", rnd))
    its.append(mcq("One arm of an angle is on 0 of the outer scale. Which scale should you read?", "the outer scale",
                   ["the inner scale", "the scale with the bigger number", "the scale with the smaller number"],
                   "Read the scale that starts at 0 on your arm. Here that is the outer scale.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s measures an angle that is clearly smaller than a right angle. The arm crosses the protractor at 35 and 145. "
                   "What is the angle?" % n, D(35), [D(145), D(110), D(180)],
                   "An angle smaller than a right angle is less than 90°, so it is 35°. 145 is on the other scale.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s wants to draw an angle of 65°. %s puts %s line on 0 of the inner scale. Where should %s make a mark?"
                   % (n, cap(he), his, he), "at 65 on the inner scale",
                   ["at 65 on the outer scale", "5 small marks after 60", "at 115 on the inner scale"],
                   "Use the scale that starts at 0 on your line: the inner scale. Count up to 65 (the small mark between 60 and 70), "
                   "make a dot, then join it to the vertex. The small marks go up in 5s, so 5 marks after 60 would be 85. On the outer scale, 65 would give 115°.", rnd))
    n, he, his = P.next()
    its.append(mcq("To find a reflex angle, %s measures the angle on the other side. It is 130°. What is the reflex angle?" % n,
                   D(230), [D(130), D(50), D(310)],
                   "The two angles go all the way round the vertex, so they add up to 360°. 360° − 130° = 230°. "
                   "(50° comes from using 180° instead of 360°.)", rnd))
    its.append(mcq("A protractor only goes to 180°. How can you draw a reflex angle of 250°?",
                   "Draw 110°, then mark the angle outside it",
                   ["Draw 70°, then mark the angle outside it", "Draw 250° on the outer scale", "You cannot draw it"],
                   "360° − 250° = 110°. Draw an angle of 110°. The angle round the outside is then 250°. "
                   "(250° − 180° = 70° is a different angle.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Measure and draw angles with a protractor", "items": its}


# ------------------------------------------------------------ set 4: straight line, point, turns
def set_facts(rnd, P):
    its = []
    q_line = "The angles are on a straight line. Work out the missing angle."
    q_pt = "The angles are around a point. Work out the missing angle."
    for rot, parts, texts, v, wrong, e in [
        (0, [55, 125], ["55°", "?"], 125, [305, 35, 55],
         "Angles on a straight line add up to 180°. 180° − 55° = 125°."),
        (15, [40, 140], ["?", "140°"], 40, [220, 50, 140],
         "The line is tilted, but it is still straight: 180° − 140° = 40°. (220° would be for angles around a point.)"),
        (0, [40, 85, 55], ["40°", "?", "55°"], 85, [265, 140, 95],
         "First add the angles you know: 40° + 55° = 95°. Then 180° − 95° = 85°."),
        (0, [90, 62, 28], [None, "62°", "?"], 28, [118, 298, 62],
         "The small square is a right angle: 90°. 90° + 62° = 152°, and 180° − 152° = 28°."),
    ]:
        its.append(dq(fig(line_svg(rot, parts, texts)) + q_line, v, wrong, e, rnd))
    for rot, parts, texts, v, wrong, e in [
        (0, [120, 140, 100], ["120°", "140°", "?"], 100, [260, 240, 220],
         "Angles around a point add up to 360°. 120° + 140° = 260°, and 360° − 260° = 100°."),
        (30, [90, 130, 55, 85], [None, "130°", "?", "85°"], 55, [305, 145, 140],
         "The small square is 90°. 90° + 130° + 85° = 305°, and 360° − 305° = 55°."),
        (20, [70, 290], ["70°", "?"], 290, [110, 20, 70],
         "The two angles go all the way around the point: 360°. 360° − 70° = 290°, a reflex angle. "
         "(110° comes from using 180°.)"),
        (90, [120, 120, 120], ["b", "b", "b"], 120, [60, 90, 180],
         "Angles around a point add up to 360°. The three angles are equal: 360° ÷ 3 = 120°. (60° comes from 180° ÷ 3.)"),
        (0, [90, 135, 135], [None, "a", "a"], 135, [45, 270, 90],
         "360° − 90° = 270° is left for the two equal angles. 270° ÷ 2 = 135°. (45° comes from using 180°.)"),
    ]:
        qq = q_pt if "a" not in texts and "b" not in texts else (
            "The three angles marked <i>b</i> are equal. What is <i>b</i>?" if "b" in texts else
            "The two angles marked <i>a</i> are equal. What is <i>a</i>?")
        its.append(dq(fig(point_svg(rot, parts, texts)) + qq, v, wrong, e, rnd))
    its.append(dq("Angles on a straight line add up to …", 180, [360, 90, 100],
                  "A straight line is half a turn: 180°. Two right angles make a straight line.", rnd))
    its.append(dq("One whole turn is …", 360, [180, 100, 90],
                  "A whole turn goes all the way round: 360°. It is 4 right angles: 4 × 90° = 360°.", rnd))
    its.append(dq("How many degrees are in a half turn?", 180, [90, 360, 120],
                  "A whole turn is 360°, and half of 360° is 180°.", rnd))
    its.append(dq("How many degrees are in a three-quarter turn?", 270, [180, 300, 75],
                  "A quarter turn is 90°. Three quarter turns are 3 × 90° = 270°. (75° is three quarters of 100, but a turn is 360°.)", rnd))
    its.append(mcq("How many right angles make a whole turn?", "4", ["2", "3", "360"],
                   "4 × 90° = 360°, so 4 right angles make a whole turn. 2 right angles make a straight line.", rnd))
    its.append(mcq("Which angle is a multiple of 90°?", "270°", ["100°", "300°", "190°"],
                   "The multiples of 90° are 90°, 180°, 270° and 360°. 270° = 3 × 90°.", rnd))
    its.append(mcq("What do two right angles make?", "a straight line (180°)",
                   ["a whole turn (360°)", "a reflex angle (270°)", "an obtuse angle (100°)"],
                   "2 × 90° = 180°, half a turn. The arms make a straight line. 4 right angles make a whole turn.", rnd))
    its.append(mcq("How many right angles are there in 270°?", "3", ["2", "4", "27"],
                   "270° ÷ 90° = 3. Three right angles make a three-quarter turn.", rnd))
    n, he, his = P.next()
    its.append(dq("%s faces north and turns clockwise to face east. How many degrees does %s turn?" % (n, he), 90,
                  [180, 270, 45], "North to east clockwise is a quarter turn: 90°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s faces north and turns anticlockwise until %s faces east. How many degrees does %s turn?" % (n, he, he), 270,
                  [90, 180, 360],
                  "Anticlockwise from north: west (90°), south (180°), then east (270°). It is the long way round. "
                  "(90° would be clockwise.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces south and turns 270° clockwise. Which way does %s face now?" % (n, he), "east",
                   ["west", "north", "south"],
                   "270° is 3 right angles. Clockwise from south: west (90°), north (180°), east (270°). "
                   "(West would be a quarter turn clockwise, or 270° anticlockwise.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles on a straight line, around a point and turns", "items": its}


# ------------------------------------------------------------ set 5: regular polygons and problems
REG = ["Regular: all sides and all angles are equal", "Irregular: the sides are not all equal",
       "Irregular: the angles are not all equal", "Irregular: the sides and the angles are not all equal"]


def set_polygons(rnd, P):
    its = []
    q = "The marks show which sides and angles are equal. Is this polygon regular or irregular?"
    hexa = regular_pts(6, 52)
    its.append(mcq(fig(shape_svg(hexa, {}, "hexagon", ticks=tuple((i, 1) for i in range(6)), eqs=tuple((i, 1) for i in range(6)))) + q,
                   REG[0], REG[1:], "All 6 sides have the same mark and all 6 angles have the same mark. Equal sides and equal angles: regular.", rnd))
    s = 90.0
    rh = [O, (s, 0.0), pol((s, 0.0), s, 60), pol(O, s, 60)]
    its.append(mcq(fig(shape_svg(rh, {0: "60°", 1: "120°", 2: "60°", 3: "120°"}, "rhombus", ticks=tuple((i, 1) for i in range(4)))) + q,
                   REG[2], [REG[0], REG[1], REG[3]],
                   "All 4 sides are equal, but the angles are 60° and 120°. A regular polygon needs equal sides <b>and</b> equal angles, "
                   "so this rhombus is irregular.", rnd))
    re_ = [O, (130.0, 0.0), (130.0, -70.0), (0.0, -70.0)]
    its.append(mcq(fig(shape_svg(re_, {}, "rectangle", rights=(0, 1, 2, 3), ticks=((0, 1), (2, 1), (1, 2), (3, 2)))) + q,
                   REG[1], [REG[0], REG[2], REG[3]],
                   "All 4 angles are right angles, but the long sides and the short sides are different. "
                   "Equal angles are not enough, so this rectangle is irregular.", rnd))
    pe = [O, (120.0, 0.0), (150.0, -60.0), (70.0, -105.0), (-20.0, -55.0)]
    its.append(mcq(fig(shape_svg(pe, {}, "pentagon")) + "Is this pentagon regular or irregular?",
                   REG[3], REG[:3],
                   "There are no equal marks. The sides are clearly different lengths and the angles are different sizes, so it is irregular.", rnd))
    its.append(mcq("A shape has 4 equal sides. Must it be a regular polygon?", "No, its angles must be equal too",
                   ["Yes, all its sides are equal", "Yes, every 4-sided shape is regular", "No, it must have 5 sides"],
                   "A regular polygon has all sides equal <b>and</b> all angles equal. A rhombus has 4 equal sides but its angles can be different.", rnd))
    its.append(mcq("Which shape is always a regular polygon?", "an equilateral triangle", ["a rectangle", "a rhombus", "a hexagon"],
                   "An equilateral triangle always has 3 equal sides and 3 equal angles (60° each). A rectangle, a rhombus or a hexagon can be irregular.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a hexagon. All its angles are 120°, but some sides are 3 cm and some are 5 cm. Is it regular?" % n,
                   "No, the sides are not all equal", ["Yes, the angles are all equal", "Yes, it has 6 sides", "No, the angles are not all equal"],
                   "Regular needs equal angles <b>and</b> equal sides. The sides are 3 cm and 5 cm, so the hexagon is irregular.", rnd))
    its.append(mcq("A regular octagon has a perimeter of 48 cm. How long is each side?", "6 cm", ["8 cm", "40 cm", "384 cm"],
                   "A regular octagon has 8 equal sides. 48 ÷ 8 = 6 cm.", rnd))
    its.append(dq("A regular pentagon has one angle of 108°. What is the size of each of its other angles?", 108, [72, 90, 540],
                  "In a regular polygon all the angles are equal, so every angle is 108°.", rnd))
    its.append(dq(fig(clock_svg(4)) + "What is the smaller angle between the hands of the clock at 4 o’clock?", 120, [240, 90, 40],
                  "The 12 hour spaces go around 360°, so each is 360° ÷ 12 = 30°. At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°.", rnd))
    its.append(dq("At 4 o’clock the smaller angle between the hands of a clock is 120°. What is the reflex angle between the hands?",
                  240, [60, 120, 300],
                  "The two angles between the hands go all the way round: 360°. 360° − 120° = 240°. (60° comes from using 180°.)", rnd))
    its.append(dq("The minute hand turns clockwise from 12 to 9. How many degrees does it turn?", 270, [90, 180, 45],
                  "12 to 3, 3 to 6 and 6 to 9 are three quarter turns: 3 × 90° = 270°. (90° is the short way, from 9 to 12.)", rnd))
    its.append(dq("How many degrees does the minute hand of a clock turn in 15 minutes?", 90, [15, 180, 45],
                  "60 minutes is a whole turn (360°). 15 minutes is a quarter of an hour, so a quarter turn: 90°.", rnd))
    its.append(dq("A reflex angle and an angle of 85° fit together to make a whole turn. What is the reflex angle?", 275, [95, 5, 85],
                  "A whole turn is 360°. 360° − 85° = 275°. (95° comes from using 180°.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces east in the playground. %s turns 90° anticlockwise. Which way does %s face now?" % (n, cap(he), he),
                   "north", ["south", "west", "east"],
                   "Anticlockwise from east, a quarter turn takes you to north. (Clockwise would be south.)", rnd))
    its.append(mcq("A robot faces north. It turns through 3 right angles clockwise. Which way does it face now?", "west",
                   ["east", "south", "north"],
                   "Clockwise from north: east (1 right angle), south (2), west (3). (East would be 3 right angles anticlockwise.)", rnd))
    its.append(dq("A windmill sail turns a half turn and then a quarter turn more. How many degrees does it turn altogether?", 270,
                  [180, 360, 90], "A half turn is 180° and a quarter turn is 90°. 180° + 90° = 270°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures an angle and writes 40°. The angle is clearly bigger than a right angle. What should %s have written?" % (n, he),
                  140, [40, 220, 320],
                  "An angle bigger than a right angle is more than 90°. %s read the wrong scale: the other scale gives 180° − 40° = 140°." % n, rnd))
    its.append(dq("Three paths meet at a point. Two of the angles between them are 90° and 150°. What is the third angle?", 120,
                  [240, 210, 270],
                  "The three angles go all the way around the point: 360°. 90° + 150° = 240°, and 360° − 240° = 120°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s cuts a round cake into 4 equal slices from the centre. What angle does each slice make at the centre?" % n, 90,
                  [45, 25, 360],
                  "The slices go all the way round the centre: 360°. 360° ÷ 4 = 90°, a right angle. (45° comes from using 180°.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Regular polygons and angle problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    kinds = strip_svg([angle_fig(40, 0, L=55), angle_fig(90, 0, L=55), angle_fig(130, 0, L=55), angle_fig(180, 0, L=55),
                       angle_fig(240, 0, L=55)],
                      ["acute", "right angle", "obtuse", "straight line", "reflex"], "acute, right, obtuse, straight and reflex angles", cw=150)
    prot = protractor_svg([0, 50], "protractor measuring a 50 degree angle")
    facts = strip_svg([line_svg(0, [60, 120], ["60°", "120°"], L=80), point_svg(20, [70, 290], ["70°", "290°"], L=66)],
                      ["straight line: 180°", "around a point: 360°"], "angles on a straight line and around a point", cw=210)
    s = 82.0
    shapes = strip_svg([shape_svg(regular_pts(6, 44), {}, "regular hexagon", ticks=tuple((i, 1) for i in range(6)),
                                  eqs=tuple((i, 1) for i in range(6))),
                        shape_svg([O, (s, 0.0), pol((s, 0.0), s, 60), pol(O, s, 60)], {}, "rhombus",
                                  ticks=tuple((i, 1) for i in range(4)), eqs=((0, 1), (2, 1), (1, 2), (3, 2))),
                        shape_svg([O, (110.0, 0.0), (110.0, -55.0), (0.0, -55.0)], {}, "rectangle", rights=(0, 1, 2, 3),
                                  ticks=((0, 1), (2, 1), (1, 2), (3, 2)))],
                       ["regular", "irregular: angles differ", "irregular: sides differ"], "regular and irregular polygons", cw=210)
    return (
        "<h2>Types of angle</h2>"
        "<p>An angle is an amount of <b>turn</b>. We measure it in <b>degrees</b> (°). A whole turn is <b>360°</b>, "
        "half a turn is <b>180°</b> and a quarter turn is <b>90°</b>, a right angle.</p>"
        "<figure class='sn-fig'>" + kinds +
        "<figcaption>The arc shows which angle is meant. A reflex angle goes round the outside.</figcaption></figure>" +
        table(["Type", "Size"], [
            ["Acute", "less than 90°"],
            ["Right angle", "exactly 90°"],
            ["Obtuse", "more than 90°, less than 180°"],
            ["Reflex", "more than 180°, less than 360°"],
        ]) +
        "<p>To <b>estimate</b>, compare with a right angle (90°) and a straight line (180°). "
        "The length of the arms does not change the size of the angle.</p>"
        "<h2>Measure with a protractor</h2>"
        "<p>1. Put the centre of the protractor on the vertex. 2. Line up one arm with <b>0</b>. "
        "3. Read the scale that <b>starts at 0 on that arm</b>. 4. Check with your estimate: acute or obtuse?</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom arm is on 0 of the inner (green) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same place, but the angle is acute, so 130° cannot be right. The small marks go up in 5s.</figcaption></figure>" +
        ex("Draw an angle of 65°", "Draw a line. Put the centre on one end and the line on 0.",
           "Count along the scale that starts at 0 on your line to 65, make a dot, and join it to the end of the line.", "an angle of 65°") +
        ex("Reflex angle", "The angle on the other side measures 130°. Find the reflex angle.",
           "The two angles make a whole turn: 360° − 130° = 230°.", "230°") +
        "<h2>Straight lines, points and turns</h2>"
        "<figure class='sn-fig'>" + facts +
        "<figcaption>Angles on a straight line add up to 180° (half a turn). Angles around a point add up to 360° (one whole turn).</figcaption></figure>" +
        ex("Missing angle", "Two angles on a straight line are 55° and ?. Find ?.", "180° − 55° = 125°. Check: 55° + 125° = 180°.", "125°") +
        "<h2>Regular and irregular polygons</h2>"
        "<p>A polygon is <b>regular</b> if all its sides are equal <b>and</b> all its angles are equal. "
        "If either is not true, it is <b>irregular</b>. Small marks show which sides and angles are equal.</p>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>A rhombus has equal sides but not equal angles. A rectangle has equal angles but not equal sides. Both are irregular.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (140° for a 40° angle)", "Read the scale that starts at 0 on your arm, then check your estimate"],
            ["Calling 190° obtuse", "Obtuse is between 90° and 180°. More than 180° is reflex"],
            ["Using 180° for a whole turn", "Straight line: 180°. All the way round: 360°"],
            ["Thinking longer arms make a bigger angle", "The size of an angle is the amount of turn, not the length of the arms"],
            ["Saying a shape is regular because its sides are equal", "Regular needs equal sides and equal angles"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 children learn about angles?",
     "a": "They learn to name acute, obtuse and reflex angles, estimate and measure angles with a protractor, draw angles, use angles on a straight line (180°) and around a point (360°), and tell regular from irregular polygons."},
    {"q": "How do you teach measuring angles with a protractor in Year 5?",
     "a": "Estimate first. Then put the centre on the vertex, line up one arm with 0 and read the scale that starts at that 0. Check the reading against the estimate."},
    {"q": "What is a reflex angle?",
     "a": "A reflex angle is more than 180° and less than 360°. To measure one, measure the angle on the other side and subtract it from 360°."},
    {"q": "What is the difference between a regular and an irregular polygon?",
     "a": "A regular polygon has all sides equal and all angles equal, like a square. A rectangle and a rhombus are irregular, because only their angles or only their sides are equal."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) in every set. Picture-letter questions keep A–D order."""
    for s in sets:
        fixed = [it["a"] for it in s["items"] if it.get("fix")]
        targets = []
        for p in range(4):
            targets += [p] * (5 - fixed.count(p))
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fix")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        for it in s["items"]:
            it.pop("fix", None)


def gen():
    rnd = random.Random(5515)
    P = People(rnd)
    sets = [set_types(rnd, P), set_estimate(rnd, P), set_protractor(rnd, P), set_facts(rnd, P), set_polygons(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "measuring-angles", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Angles: Acute, Obtuse and Reflex Angles, Protractors and Regular Polygons",
        "seo_title": "Year 5 Measuring Angles Worksheets: Protractor, Reflex Angles, 180° and 360° (Free, with Answers)",
        "short_title": "Measuring angles",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 5: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Know angles are measured in degrees: estimate and compare acute, obtuse and reflex angles; draw given angles, "
                         "and measure them in degrees (°); identify: angles at a point and one whole turn (total 360°), angles at a point "
                         "on a straight line and ½ a turn (total 180°), other multiples of 90°; distinguish between regular and irregular "
                         "polygons based on reasoning about equal sides and angles.",
        "meta_desc": "Free Year 5 maths worksheets on measuring angles: acute, obtuse and reflex angles, estimating, reading a protractor, "
                     "angles on a straight line and around a point, turns, and regular and irregular polygons. "
                     "100 questions with an answer key, following the National Curriculum.",
        "key_big": "A whole turn is 360°, a straight line is 180° and a right angle is 90°. Reflex angles are more than 180°.",
        "key_sub": "On a protractor, put the centre on the vertex, line up one arm with 0 and read the scale that starts at that 0. "
                   "Estimate first so you can spot a reading from the wrong scale.",
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
        mark_large(u, "(angles on a straight line|protractor|four angles labelled)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
