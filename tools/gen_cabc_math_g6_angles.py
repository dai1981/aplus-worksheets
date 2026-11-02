# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Angles
(BC Mathematics Curriculum, Grade 6: Geometry and measurement, angle measurement and classification)
  python3 tools/gen_cabc_math_g6_angles.py
Classify angles (acute, right, obtuse, straight, reflex), estimate with benchmark angles, read both protractor
scales, angles on a straight line (180°) and around a point (360°), and angles in BC life.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).

Every angle is drawn exactly at its size (trig, 0° = pointing right, counterclockwise, SVG y goes down);
every marked angle is measured back from the drawing and checked against its value.
Labels are checked so that they do not touch a line, an arc or another label.
Protractor: inner scale has 0 on the right (counts counterclockwise), outer scale has 0 on the left
(counts clockwise); marks every 5°, numbers every 10°.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


def D(v):
    """Angle in degrees as text: 65°, 1080° (BC style: no separator in 4-digit numbers)."""
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
    """Protractor centred on the vertex. rays: directions in deg (0 = right). Rays are red and cross the scales."""
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
    """Two arms from O: one at rot, one at rot + d (counterclockwise). The marked angle is d (it may be reflex)."""
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



def rev_fig(rot, label="marked angle", L=80, r=20):
    """A revolution: one arm, and an arrow that turns all the way round (360°) back to it."""
    P = Pic()
    P.line(O, pol(O, L, rot))
    a0, a1 = rot + 12, rot + 348
    P.arc(O, r, a0, a1)
    E = pol(O, r, a1)
    t = a1 + 90                        # direction of travel at the end of the arc
    P.polyline([pol(E, 7, t + 180 - 35), E, pol(E, 7, t + 180 + 35)], INK, 1.8)
    P.dot(O)
    return P.svg(label)


def name_fig(d, rot, L=80):
    return rev_fig(rot, L=L) if d == 360 else angle_fig(d, rot, L=L)


# ------------------------------------------------------------ angles on a straight line and around a point
def rays_svg(rays, marks, label, L=80, dot=True):
    """Lines from one point O. rays: directions (deg). marks: (from_dir, to_dir, val, text, kind),
    each angle measured counterclockwise from from_dir to to_dir."""
    P = Pic()
    for d in rays:
        P.line(O, pol(O, L, d))
    for a, b, val, t, kind_ in marks:
        P.mark(O, pol(O, L, a), pol(O, L, b), val, t, kind=kind_, ccw=True)
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
    """Rays from O splitting a full turn into parts (deg), counterclockwise from rot."""
    assert abs(sum(parts) - 360) < 1e-9
    rays, marks, d = [], [], rot
    for p, t in zip(parts, texts):
        rays.append(d)
        marks.append((d, d + p, p, t, "right" if (p == 90 and t is None) else "arc"))
        d += p
    return rays_svg(rays, marks, label, L)


# ------------------------------------------------------------ angle names
NAMES = {"acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle",
         "reflex": "reflex angle"}
WRONG = {"acute": ["obtuse", "right", "reflex"], "right": ["acute", "obtuse", "straight"],
         "obtuse": ["acute", "reflex", "straight"], "straight": ["obtuse", "reflex", "right"],
         "reflex": ["obtuse", "straight", "acute"]}
KIND_E = {
    "acute": "An acute angle is smaller than a right angle: less than 90°.",
    "right": "A right angle is exactly 90°, a quarter turn. The small square shows it.",
    "obtuse": "An obtuse angle is bigger than a right angle but smaller than a straight angle: between 90° and 180°.",
    "straight": "A straight angle is exactly 180°, half a turn. The two arms make a straight line.",
    "reflex": "A reflex angle is bigger than a straight angle but smaller than a full turn: between 180° and 360°. "
              "Look at the arc: it goes around the outside.",
}


def kind(d):
    return "acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight" if d == 180 else "reflex"


def name_q(q, k, wrong, e, rnd):
    return mcq(q, NAMES[k], [NAMES[w] for w in wrong], e, rnd)


def set_classify(rnd, P):
    its = []
    q = "Classify the marked angle."
    for d, rot in [(35, 15), (125, 0), (90, 30), (160, 10), (230, 0), (70, 100), (180, 0),
                   (320, 20), (100, 160), (265, 45), (180, 35)]:
        k = kind(d)
        e = KIND_E[k]
        if d not in (90, 180):
            e += " This angle is %s." % D(d)
        if k == "reflex":
            e += " (The gap between the arms is %s, but the arc marks the big angle around the outside.)" % D(360 - d)
        if d == 90 or (d == 180 and rot) or rot >= 90:
            e += " Turning the angle does not change its size or its name."
        its.append(name_q(fig(angle_fig(d, rot)) + q, k, WRONG[k], e, rnd))
    for d, wrong in [(175, ["straight", "reflex", "acute"]), (185, ["obtuse", "straight", "acute"]),
                     (89, ["right", "obtuse", "reflex"]), (91, ["right", "acute", "straight"])]:
        k = kind(d)
        e = {175: "175° is more than 90° but less than 180°, so it is obtuse. It is close to a straight angle, but not 180°.",
             185: "185° is more than 180° but less than 360°, so it is reflex, even though it is close to a straight angle.",
             89: "89° is less than 90°, so it is acute (only just). A right angle is exactly 90°.",
             91: "91° is more than 90° but less than 180°, so it is obtuse (only just). A right angle is exactly 90°."}[d]
        its.append(name_q("An angle measures %s. How do you classify it?" % D(d), k, wrong, e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(130, 0), (60, 0), (250, 0), (90, 0)], lab)) + "Which angle is reflex?", "C",
                        "A reflex angle is more than 180°: its arc goes around the outside. C is about 250°. "
                        "A is obtuse, B is acute and D is a right angle."))
    n, he, his = P.next()
    its.append(mcq("%s says an angle of 190° is obtuse because it is bigger than 90°. Is %s right?" % (n, he),
                   "No, it is reflex", ["Yes, it is obtuse", "No, it is acute", "No, it is straight"],
                   "Obtuse angles are bigger than 90° but smaller than 180°. 190° is more than 180°, so it is reflex.", rnd))
    its.append(mcq("Which list has only reflex angles?", "200°, 270°, 345°",
                   ["100°, 150°, 175°", "95°, 180°, 270°", "45°, 190°, 300°"],
                   "Reflex angles are more than 180° and less than 360°. 200°, 270° and 345° all fit. "
                   "100°, 150° and 175° are obtuse, 180° is straight and 45° is acute.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?",
                   "acute, right, obtuse, straight, reflex",
                   ["acute, obtuse, right, straight, reflex", "acute, right, obtuse, reflex, straight",
                    "right, acute, obtuse, straight, reflex"],
                   "Acute is less than 90°, right is 90°, obtuse is between 90° and 180°, straight is 180° "
                   "and reflex is between 180° and 360°.", rnd))
    its.append(dq("How many degrees are in a full turn?", 360, [180, 90, 100],
                  "A full turn is 360°. It is 4 right angles: 4 × 90° = 360°. "
                  "180° is a straight angle, only half a turn.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Classify angles: acute, right, obtuse, straight, reflex", "items": its}


# ------------------------------------------------------------ estimate with benchmark angles
def set_estimate(rnd, P):
    its = []
    q = "Use benchmark angles (45°, 90°, 135°, 180°, 270°). Which is the best estimate for the marked angle?"
    for d, rot, best, wrong, e in [
        (28, 0, 30, [150, 60, 90],
         "The angle is less than half a right angle (45°). About 30° fits. (150° is what the other scale of a protractor would say.)"),
        (43, 70, 45, [135, 90, 15],
         "The angle is about half of a right angle, so it is about 45°."),
        (88, 30, 90, [45, 180, 270],
         "The angle looks like a square corner, so it is about 90°. (It is 88°.)"),
        (118, 5, 120, [60, 90, 240],
         "The angle is a bit more than a right angle (90°), but less than 135°. About 120° fits. (60° would be acute.)"),
        (137, 10, 135, [45, 90, 225],
         "The angle is about halfway between a right angle (90°) and a straight angle (180°), so it is about 135°."),
        (172, 0, 170, [10, 190, 90],
         "The arms almost make a straight line (180°), so the angle is about 170°. "
         "(10° is the small gap left to make a straight line, and 190° would be reflex.)"),
        (205, 0, 200, [160, 20, 300],
         "The arc goes around the outside and is a little more than a straight angle (180°), so it is about 200°. "
         "(160° is the gap between the arms, the angle on the other side.)"),
        (268, 20, 270, [90, 180, 360],
         "The arc goes around the outside and leaves a gap of about a right angle. 360° − 90° = 270°. "
         "(90° is the gap, not the marked angle.)"),
        (313, 0, 315, [45, 225, 135],
         "The gap between the arms is about 45°, half a right angle. The marked angle goes around the outside: "
         "360° − 45° = 315°. (45° is only the gap.)"),
        (228, 30, 225, [135, 45, 315],
         "The marked angle is more than a straight angle (180°) but less than three right angles (270°). "
         "Halfway between is 225°. (135° is the gap on the other side: 360° − 225° = 135°.)"),
    ]:
        its.append(mcq(fig(angle_fig(d, rot)) + q, "about " + D(best), ["about " + D(w) for w in wrong], e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(85, 0), (45, 0), (15, 0), (135, 0)], lab)) + "Which angle is closest to 45°?", "B",
                        "45° is half a right angle. B is about half of a square corner. A is nearly a right angle, C is very small and D is obtuse."))
    its.append(letter_q(fig(abcd_svg([(200, 0), (300, 0), (270, 0), (330, 0)], lab)) + "Which angle is closest to 270°?", "C",
                        "270° is three right angles, so the gap between the arms is a right angle. C leaves a square-corner gap. "
                        "A is about 200°, B is about 300° and D is about 330°."))
    its.append(letter_q(fig(abcd_svg([(150, 0, 28), (100, 0, 40), (60, 0, 50), (30, 0, 58)], lab)) +
                        "Which angle is the largest?", "A",
                        "The size of an angle is the amount of turn between the arms, not the length of the arms. "
                        "A opens the widest (about 150°), even though its arms are the shortest."))
    its.append(mcq("An angle is a little smaller than a right angle. Which could it be?", "80°", ["100°", "45°", "170°"],
                   "A right angle is 90°. A little smaller than 90° is about 80°. 100° is a little bigger.", rnd))
    its.append(mcq("An angle is a little bigger than a straight angle. Which could it be?", "190°", ["170°", "100°", "290°"],
                   "A straight angle is 180°. A little bigger is about 190°, a reflex angle. 170° is a little smaller.", rnd))
    its.append(mcq("Which angle is closer to a straight angle: 165° or 200°?", "165°",
                   ["200°", "they are equally close", "you cannot tell"],
                   "165° is 15° away from 180°: 180° − 165° = 15°. 200° is 20° away: 200° − 180° = 20°. So 165° is closer.", rnd))
    its.append(dq("What angle is halfway between a right angle and a straight angle?", 135, [270, 100, 45],
                  "Halfway between 90° and 180° is 135°, because 90° + 45° = 135°. (270° comes from adding 90° + 180°.)", rnd))
    its.append(dq("How many degrees are in three quarters of a full turn?", 270, [75, 180, 90],
                  "A full turn is 360°. One quarter is 90°, so three quarters is 3 × 90° = 270°. "
                  "(75° comes from mixing up three quarters with 75%.)", rnd))
    its.append(mcq("An angle is bigger than a straight angle but smaller than three right angles. Which could it be?", "230°",
                   ["130°", "290°", "170°"],
                   "It must be between 180° and 270°. Only 230° fits. 130° and 170° are less than 180°, and 290° is more than 270°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s estimates an angle as about 135°. Then %s measures it with a protractor and reads 45°. What should %s do?"
                   % (n, he, he), "Check the other scale: 135°",
                   ["Keep 45°", "Write 90°, between the two", "Add them: 180°"],
                   "45° is far from the estimate of 135°, so %s probably read the wrong scale. "
                   "The other scale gives 180° − 45° = 135°, which matches the estimate." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Estimate with benchmark angles", "items": its}


# ------------------------------------------------------------ read a protractor
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
        e = ("The bottom arm is on 0 at the right, so read the <b>inner</b> scale. It counts counterclockwise from 0 on the right. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The small marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " The outer scale says %d there, but it counts from the other side. The angle is %s, so %s makes sense." % (
            180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([0, v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for v in (30, 55, 120, 145, 70, 100):
        e = ("The bottom arm is on 0 at the left, so read the <b>outer</b> scale. It counts clockwise from 0 on the left. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The small marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " (The inner scale says %d there.) The angle is %s, so %s makes sense." % (180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([180, 180 - v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for a, b in ((20, 95), (40, 150)):
        v = b - a
        its.append(mcq(fig(protractor_svg([a, b], "protractor measuring an angle with neither arm on 0")) +
                       "Neither arm is on 0. What is the size of the angle?", D(v), [D(b), D(180 - b), D(a), D(a + b)],
                       "On the inner scale one arm is at %d and the other is at %d. The angle is the difference: %d° − %d° = %d°. "
                       "(%s comes from reading only one arm.)" % (a, b, b, a, v, D(b)), rnd))
    its.append(mcq("Where do you put the centre of the protractor when you measure an angle?", "on the vertex",
                   ["at the end of an arm", "on the 90 mark", "in the middle of an arm"],
                   "The centre goes on the vertex, where the two arms meet. Then line up one arm with 0.", rnd))
    its.append(mcq("One arm of an angle is on 0 of the outer scale. Which scale should you read?", "the outer scale",
                   ["the inner scale", "the scale with the bigger number", "the scale with the smaller number"],
                   "Read the scale that starts at 0 on your arm. Here that is the outer scale.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s measures an angle that is clearly smaller than a right angle. The arm crosses the protractor at 35 and 145. "
                   "What is the angle?" % n, D(35), [D(145), D(110), D(180)],
                   "An angle smaller than a right angle is acute, less than 90°, so it is 35°. 145 is on the other scale.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures an angle and writes 40°. The angle is clearly obtuse. What should %s have written?" % (n, he),
                  140, [40, 220, 320],
                  "An obtuse angle is more than 90°. %s read the wrong scale: the other scale gives 180° − 40° = 140°." % n, rnd))
    n, he, his = P.next()
    its.append(dq(fig(protractor_svg([0, 130], "protractor with an angle drawn on it")) +
                  "%s wanted to draw an angle of 50°. %s base arm is on 0 of the inner scale. "
                  "The picture shows what %s drew. What angle did %s actually draw?" % (n, cap(his), he, he),
                  130, [50, 230, 310],
                  "Read the inner scale, because the base arm is on its 0: the second arm is at 130, so the angle is 130°. "
                  "%s used 50 on the outer scale by mistake. 180° − 50° = 130°." % n, rnd))
    n, he, his = P.next()
    its.append(dq(fig(protractor_svg([180, 70], "protractor with an angle drawn on it")) +
                  "%s wanted to draw an angle of 70°. %s base arm is on 0 of the outer scale. "
                  "The picture shows what %s drew. What angle did %s actually draw?" % (n, cap(his), he, he),
                  110, [70, 250, 290],
                  "The base arm is on 0 of the outer scale, so read the outer scale: the second arm is at 110, so the angle is 110°. "
                  "%s used 70 on the inner scale by mistake. 180° − 70° = 110°." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a protractor (both scales)", "items": its}


# ------------------------------------------------------------ angles on a line and around a point
def set_line_point(rnd, P):
    its = []
    q_line = "The angles make a straight line. What is the missing angle?"
    for rot, parts, texts, v, wrong, e in [
        (0, [55, 125], ["55°", "?"], 125, [305, 35, 55],
         "Angles on a straight line add up to 180°. 180° − 55° = 125°. (305° comes from using 360° instead of 180°.)"),
        (15, [40, 140], ["?", "140°"], 40, [220, 50, 140],
         "The line is tilted, but it is still straight: 180° − 140° = 40°. (50° is 90° − 40°: the line is not a right angle.)"),
        (0, [90, 90], [None, "?"], 90, [270, 180, 45],
         "The small square shows a right angle, 90°. 180° − 90° = 90°, so the other angle is a right angle too."),
        (-10, [35, 145], ["35°", "?"], 145, [55, 325, 135],
         "180° − 35° = 145°. (55° is 90° − 35°: the line is not a right angle.)"),
        (0, [40, 85, 55], ["40°", "?", "55°"], 85, [265, 140, 95],
         "First add the angles you know: 40° + 55° = 95°. Then 180° − 95° = 85°. (265° comes from using 360°.)"),
        (0, [48, 90, 42], ["48°", None, "?"], 42, [132, 312, 48],
         "The small square is 90°. 48° + 90° = 138°, and 180° − 138° = 42°."),
        (0, [90, 62, 28], [None, "62°", "?"], 28, [118, 298, 62],
         "The small square is a right angle: 90°. 90° + 62° = 152°, and 180° − 152° = 28°. (118° comes from 180° − 62°, forgetting the right angle.)"),
    ]:
        its.append(dq(fig(line_svg(rot, parts, texts)) + q_line, v, wrong, e, rnd))
    q_pt = "The angles go all the way around a point. What is the missing angle?"
    for rot, parts, texts, v, wrong, e in [
        (30, [110, 250], ["110°", "?"], 250, [70, 110, 290],
         "Angles around a point add up to 360°. 360° − 110° = 250°, a reflex angle. (70° comes from using 180° instead of 360°.)"),
        (10, [100, 130, 130], ["100°", "130°", "?"], 130, [230, 260, 50],
         "Add the angles you know: 100° + 130° = 230°. Angles around a point add up to 360°: 360° − 230° = 130°. "
         "(260° comes from subtracting only 100°.)"),
        (0, [90, 150, 120], [None, "150°", "?"], 120, [30, 210, 270],
         "The small square is 90°. 90° + 150° = 240°, and 360° − 240° = 120°. "
         "(30° comes from using 180°: 180° − 150°.)"),
        (20, [70, 80, 95, 115], ["70°", "80°", "95°", "?"], 115, [245, 185, 125],
         "Add the three angles you know: 70° + 80° + 95° = 245°. 360° − 245° = 115°. "
         "(185° comes from forgetting the 70° angle.)"),
    ]:
        its.append(dq(fig(point_svg(rot, parts, texts)) + q_pt, v, wrong, e, rnd))
    its.append(dq(fig(point_svg(0, [60] * 6, ["a"] * 6)) +
                  "The six angles marked <i>a</i> are equal and go all the way around a point. What is <i>a</i>?",
                  60, [30, 90, 120],
                  "The six equal angles add up to 360°. 360° ÷ 6 = 60°. (30° comes from 180° ÷ 6.)", rnd))
    its.append(dq(fig(point_svg(15, [80, 140, 140], ["80°", "b", "b"])) +
                  "The two angles marked <i>b</i> are equal. The angles go all the way around a point. What is <i>b</i>?",
                  140, [50, 280, 100],
                  "360° − 80° = 280° is left for the two equal angles. 280° ÷ 2 = 140°. "
                  "(50° comes from using 180°: (180° − 80°) ÷ 2.)", rnd))
    its.append(dq("Four equal angles go all the way around a point. How big is each one?", 90, [45, 180, 60],
                  "360° ÷ 4 = 90°. Each one is a right angle. (45° comes from 180° ÷ 4.)", rnd))
    its.append(mcq("Angles on a straight line add up to 180°. Angles around a point add up to …", "360°",
                   ["180°", "90°", "270°"],
                   "Around a point is a full turn: 360°. A straight line is only half a turn: 180°.", rnd))
    its.append(dq("Three angles go around a point. Two of them are 90° and 120°. What is the third angle?", 150,
                  [210, 60, 240],
                  "90° + 120° = 210°. 360° − 210° = 150°. (210° is the sum of the two angles, not the missing one, "
                  "and 60° comes from 180° − 120°.)", rnd))
    its.append(dq("Two angles make a straight line. One angle is 72°. What is the other angle?", 108, [112, 18, 288],
                  "180° − 72° = 108°. Check: 108° + 72° = 180°. (112° comes from a subtraction slip, 18° from 90° − 72° "
                  "and 288° from 360° − 72°.)", rnd))
    its.append(name_q("Two angles make a straight line. One of them is obtuse. How do you classify the other one?", "acute",
                      ["obtuse", "right", "straight"],
                      "The two angles add up to 180°. The obtuse one is more than 90°, so less than 90° is left: the other one is acute. "
                      "(For example, 120° + 60° = 180°.)", rnd))
    n, he, his = P.next()
    its.append(mcq("Three angles go around a point: 100°, 120° and 140°. %s says they are correct because they add up to 180°. "
                   "What is wrong?" % n, "They add up to 360°, not 180°",
                   ["Nothing, they add up to 180°", "They should add up to 270°", "One angle must be a right angle"],
                   "100° + 120° + 140° = 360°. Angles around a point make a full turn, so 360° is correct. "
                   "180° is for angles on a straight line.", rnd))
    its.append(dq("Two angles make a straight line. One angle is 4 times as big as the other. How big is the smaller angle?",
                  36, [45, 72, 144],
                  "The smaller angle is 1 part and the bigger one is 4 parts: 5 parts make 180°. 180° ÷ 5 = 36°. "
                  "The bigger angle is 4 × 36° = 144°. (45° comes from 180° ÷ 4, and 72° from 360° ÷ 5.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles on a line and around a point", "items": its}


# ------------------------------------------------------------ angles in real life
def ramp_svg(a, label="a ramp on flat ground"):
    """Flat ground (a straight line) and a ramp rising from a point on it at angle a. The other angle is marked “?”."""
    return line_svg(0, [a, 180 - a], [D(a), "?"], L=100, label=label)


def set_real(rnd, P):
    its = []
    its.append(dq(fig(clock_svg(4)) + "What is the size of the marked angle between the hands at 4 o’clock?", 120,
                  [240, 90, 40],
                  "The 12 spaces between the numbers go around a full turn, 360°, so each space is 360° ÷ 12 = 30°. "
                  "At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°.", rnd))
    its.append(dq(fig(clock_svg(10)) + "What is the size of the marked angle between the hands at 10 o’clock?", 60, [300, 30, 120],
                  "From 10 to 12 is 2 hour spaces. Each space is 30°, so 2 × 30° = 60°. (300° is the reflex angle the other way around.)", rnd))
    its.append(dq("How many degrees does the minute hand turn in 20 minutes?", 120, [20, 60, 240],
                  "The minute hand turns 360° in 60 minutes, so 6° each minute. 20 × 6° = 120°. (240° is the other 40 minutes.)", rnd))
    its.append(dq("Soccer practice in Surrey runs from 3:00 p.m. to 3:45 p.m. How many degrees does the minute hand turn?",
                  270, [45, 90, 180],
                  "45 minutes is three quarters of an hour, so three quarter turns: 3 × 90° = 270°, a reflex angle. "
                  "(45° mixes up minutes and degrees.)", rnd))
    n, he, his = P.next()
    its.append(dq("After a hockey game, a round pizza is cut into 8 equal slices from the centre. %s’s team eats 3 slices. "
                  "What angle at the centre do the slices that are left make?" % n,
                  225, [135, 45, 180],
                  "Each slice is 360° ÷ 8 = 45°. 5 slices are left: 5 × 45° = 225°, a reflex angle. (135° is the 3 slices that were eaten.)", rnd))
    its.append(dq("A snowboarder at Whistler spins one and a half full turns in the air. How many degrees is that?", 540,
                  [360, 450, 180],
                  "One full turn is 360°, and half a turn is 180°. 360° + 180° = 540°. (450° is 360° + 90°, a turn and a quarter.)", rnd))
    its.append(dq(fig(ramp_svg(25)) + "A skateboard ramp at a skatepark in Burnaby rises from flat ground at 25°. "
                  "What is the angle on the other side of the ramp?", 155, [65, 335, 25],
                  "The flat ground is a straight line, so the two angles add up to 180°. 180° − 25° = 155°. "
                  "(65° is 90° − 25°, and 335° is 360° − 25°.)", rnd))
    its.append(name_q("A classroom door is opened so that it makes an angle of 100° with the wall. How do you classify this angle?",
                      "obtuse", ["acute", "right", "reflex"],
                      "100° is more than 90° but less than 180°, so it is obtuse.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s is kayaking near Nanaimo, facing west. %s turns the kayak 90° counterclockwise. Which way is %s facing now?"
                   % (n, cap(he), he), "south", ["north", "east", "west"],
                   "Counterclockwise goes north → west → south → east. A quarter turn counterclockwise from west is south. "
                   "North would be 90° clockwise.", rnd))
    n, he, his = P.next()
    its.append(dq("On Grouse Mountain, %s measures the slope of a ski run with a protractor and writes 155°, but the slope is clearly acute. "
                  "What is the angle?" % n, 25, [155, 205, 65],
                  "An acute angle is less than 90°. %s read the wrong scale: 180° − 155° = 25°." % n, rnd))
    its.append(dq("In a circle graph of favourite sports, the section for hockey is one quarter of the circle. "
                  "What angle does it make at the centre?", 90, [25, 45, 180],
                  "A full circle is 360°. One quarter of 360° is 360° ÷ 4 = 90°. (25° confuses a quarter with 25%.)", rnd))
    its.append(mcq("In a circle graph of favourite sports, the section for soccer makes an angle of 120° at the centre. What fraction of the circle is it?",
                   "one third", ["one quarter", "one half", "one sixth"],
                   "120° out of 360°: 360° ÷ 120° = 3, so it is one third. (One half would be 180°, and one quarter 90°.)", rnd))
    its.append(dq("A garden sprinkler in Kelowna waters while it turns through 150°. What angle around the sprinkler does it not water?",
                  210, [30, 150, 510],
                  "The watered angle and the dry angle make a full turn: 360° − 150° = 210°. (30° comes from 180° − 150°.)", rnd))
    its.append(dq("A wind turbine has 3 blades spaced equally around the centre. What is the angle between two blades next to each other?",
                  120, [60, 90, 180],
                  "The 3 equal angles go all the way around: 360° ÷ 3 = 120°. (60° comes from 180° ÷ 3.)", rnd))
    its.append(mcq("A BC Ferries boat leaves the dock sailing east. It turns 45° counterclockwise. Which way is it sailing now?",
                   "northeast", ["southeast", "north", "northwest"],
                   "Counterclockwise from east turns toward north. 45° is half of a right angle, so the boat points halfway between "
                   "east and north: northeast. (Southeast would be 45° clockwise.)", rnd))
    its.append(dq("A cedar tree leans after a storm. It makes an angle of 80° with the flat ground on one side. "
                  "What angle does it make with the ground on the other side?", 100, [10, 280, 80],
                  "The flat ground is a straight line, so the two angles add up to 180°. 180° − 80° = 100°. "
                  "(10° comes from 90° − 80°.)", rnd))
    its.append(dq("A Ferris wheel has 10 cars spaced equally around its centre. What angle at the centre is between two cars next to each other?",
                  36, [18, 10, 72],
                  "The 10 equal angles go all the way around: 360° ÷ 10 = 36°. (18° comes from 180° ÷ 10.)", rnd))
    n, he, his = P.next()
    its.append(dq("At a skating club in Kamloops, %s spins two and a half full turns. How many degrees does %s turn?" % (n, he),
                  900, [720, 450, 1080],
                  "Two full turns are 2 × 360° = 720°, and half a turn is 180°. 720° + 180° = 900°. "
                  "(450° comes from using 180° for a full turn.)", rnd))
    n, he, his = P.next()
    its.append(dq("In coding class, %s’s robot faces north and turns 90° clockwise three times. "
                  "What single counterclockwise turn would get it to the same direction?" % n, 90, [270, 180, 360],
                  "3 × 90° = 270° clockwise. A clockwise turn and a counterclockwise turn that end in the same place add up to 360°: "
                  "360° − 270° = 90° counterclockwise.", rnd))
    n, he, his = P.next()
    its.append(dq("%s hikes a trail in Stanley Park. At a bend, the angle between the two straight parts of the trail is 150°. "
                  "How many degrees did %s turn at the bend?" % (n, he), 30, [150, 210, 60],
                  "Walking straight on would be 180°. The trail bends to 150°, so %s turned 180° − 150° = 30°. "
                  "(150° is the angle between the paths, not the turn.)" % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in BC life", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    kinds = strip_svg([angle_fig(40, 0, L=55), angle_fig(90, 0, L=55), angle_fig(130, 0, L=55)],
                      ["acute", "right", "obtuse"], "acute, right and obtuse angles", cw=150)
    kinds2 = strip_svg([angle_fig(180, 0, L=55), angle_fig(240, 0, L=55)],
                       ["straight", "reflex"], "straight angle and reflex angle", cw=150)
    prot = protractor_svg([0, 50], "protractor measuring a 50 degree angle")
    line = line_svg(0, [65, 115], ["65°", "115°"])
    point = point_svg(0, [100, 120, 140], ["100°", "120°", "140°"])
    return (
        "<h2>Classify angles</h2>"
        "<p>An angle is an amount of <b>turn</b> between two arms. We measure it in <b>degrees</b> (°). "
        "A full turn is <b>360°</b>, a straight angle (half a turn) is <b>180°</b> and a right angle "
        "(a quarter turn) is <b>90°</b>.</p>"
        "<figure class='sn-fig'>" + kinds + "</figure>"
        "<figure class='sn-fig'>" + kinds2 +
        "<figcaption>The arc shows which angle is meant. A reflex angle goes around the outside.</figcaption></figure>" +
        table(["Name", "Size"], [
            ["Acute angle", "less than 90°"],
            ["Right angle", "exactly 90°"],
            ["Obtuse angle", "more than 90°, less than 180°"],
            ["Straight angle", "exactly 180°"],
            ["Reflex angle", "more than 180°, less than 360°"],
        ]) +
        "<h2>Estimate with benchmarks</h2>"
        "<p>Compare the angle with angles you know: <b>45°</b> (half a right angle), <b>90°</b>, <b>135°</b>, "
        "<b>180°</b> and <b>270°</b> (three right angles). Estimate first, then measure. "
        "If the measurement is far from your estimate, check it.</p>" +
        ex("Estimate", "An angle opens a little wider than a square corner. Estimate it.",
           "It is more than 90° but less than 135°.", "about 110° to 120°") +
        "<h2>Read a protractor</h2>"
        "<p>1. Put the centre of the protractor on the vertex. 2. Line up one arm with <b>0</b>. "
        "3. Read the scale that <b>starts at 0 on that arm</b>. 4. Check the reading against your estimate.</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom arm is on 0 of the inner (green) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same place, but the angle is acute, so 130° cannot be right. "
        "The small marks go up in 5s.</figcaption></figure>" +
        "<p>A protractor only goes to 180°. To find a reflex angle, measure the angle on the other side, "
        "then subtract from 360°.</p>" +
        ex("Reflex angle", "The gap on the other side of a reflex angle measures 130°. Find the reflex angle.",
           "The two angles make a full turn: 360° − 130° = 230°.", "230°") +
        "<h2>Angles on a line and around a point</h2>"
        "<p>Angles on a straight line add up to <b>180°</b>. Angles that go all the way around a point add up to <b>360°</b>.</p>"
        "<figure class='sn-fig'>" + line +
        "<figcaption>65° + 115° = 180°</figcaption></figure>"
        "<figure class='sn-fig'>" + point +
        "<figcaption>100° + 120° + 140° = 360°</figcaption></figure>" +
        ex("Missing angle around a point", "Three angles go around a point. Two are 90° and 150°. Find the third.",
           "90° + 150° = 240°. 360° − 240° = 120°.", "120°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (140° for a 40° angle)", "Read the scale that starts at 0 on your arm, then check your estimate"],
            ["Calling 190° obtuse", "Obtuse is between 90° and 180°. More than 180° is reflex"],
            ["Thinking long arms make a big angle", "The size is the turn between the arms, not their length"],
            ["Using 180° for angles around a point", "Around a point is a full turn: 360°. A straight line is 180°"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about angles in the BC math curriculum?",
     "a": "In Grade 6, BC students measure and classify angles as acute, right, obtuse, straight or reflex. They estimate with benchmark angles such as 45°, 90° and 180° and use a protractor to measure and draw angles."},
    {"q": "Why does a protractor have two scales?",
     "a": "So you can measure from an arm on either side: the inner scale starts at 0 on the right, and the outer scale starts at 0 on the left. Always read the scale that starts at 0 on your arm, then check the answer against your estimate."},
    {"q": "How do you measure a reflex angle with a protractor?",
     "a": "A protractor only goes to 180°, so measure the angle on the other side of the arms and subtract it from 360°. For example, if the other side is 70°, the reflex angle is 290°."},
    {"q": "Do angles on a straight line always add up to 180°?",
     "a": "Yes. A straight line is half a turn, so the angles on it add up to 180°. Angles that go all the way around a point add up to 360°."},
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
    rnd = random.Random(56812)
    P = People(rnd)
    sets = [set_classify(rnd, P), set_estimate(rnd, P), set_protractor(rnd, P), set_line_point(rnd, P), set_real(rnd, P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "angles", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Angles: Classify, Estimate and Measure",
        "seo_title": "Grade 6 Angles Worksheets: Classify, Estimate and Measure (Free Math with Answer Key, BC Curriculum)",
        "short_title": "Angles",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 6: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Angle measurement and classification",
        "meta_desc": "Free Grade 6 math worksheets on angles for the BC curriculum: classify acute, right, obtuse, straight and "
                     "reflex angles, estimate with benchmark angles, read both protractor scales and find missing angles on a "
                     "straight line and around a point. 100 questions with an answer key.",
        "key_big": "Estimate first, then read the protractor scale that starts at 0 on your arm.",
        "key_sub": "Acute is less than 90°, obtuse is between 90° and 180°, and reflex is between 180° and 360°. "
                   "Angles on a straight line add up to 180°; angles around a point add up to 360°.",
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
        mark_large(u, "(protractor|four angles labelled)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
