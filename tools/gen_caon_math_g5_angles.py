# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Measuring angles
(Ontario Curriculum 2020, Grade 5: Spatial Sense, E2.3 and E2.4)
  python3 tools/gen_caon_math_g5_angles.py
Benchmark angles (45°, 90°, 180°) to estimate and compare, read both protractor scales and construct angles up to 180°,
name acute, right, obtuse and straight angles, angles that make a straight line, and angles in real life.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).

Every angle is drawn exactly at its size (trig, 0° = pointing right, counterclockwise, SVG y goes down);
every marked angle is measured back from the drawing and checked against its value.
Labels are checked so that they do not touch a line, an arc or another label.
Protractor: inner scale has 0 on the right, outer scale has 0 on the left; marks every 5°, numbers every 10°.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
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


# ------------------------------------------------------------ figures
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


# ------------------------------------------------------------ angle names (Grade 5: up to 180°)
NAMES = {"acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle"}
WRONG = {"acute": ["obtuse", "right", "straight"], "right": ["acute", "obtuse", "straight"],
         "obtuse": ["acute", "straight", "right"], "straight": ["obtuse", "right", "acute"]}
KIND_E = {
    "acute": "An acute angle is smaller than a right angle: less than 90°.",
    "right": "A right angle is exactly 90°, a square corner. The small square shows it.",
    "obtuse": "An obtuse angle is bigger than a right angle but smaller than a straight angle: between 90° and 180°.",
    "straight": "A straight angle is exactly 180°. The two arms make a straight line.",
}


def kind(d):
    assert 0 < d <= 180
    return "acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight"


def name_q(q, k, wrong, e, rnd):
    return mcq(q, NAMES[k], [NAMES[w] for w in wrong], e, rnd)


def set_names(rnd, P):
    its = []
    q = "What is the name of the marked angle?"
    for d, rot in [(35, 15), (125, 0), (90, 30), (160, 10), (70, 100), (180, 0),
                   (100, 160), (180, 35), (20, 40), (90, 120), (145, 200)]:
        k = kind(d)
        e = KIND_E[k]
        if d not in (90, 180):
            e += " This angle is %s." % D(d)
        if rot >= 90 or (d in (90, 180) and rot):
            e += " The angle is turned, but turning it does not change its size or its name."
        its.append(name_q(fig(angle_fig(d, rot)) + q, k, WRONG[k], e, rnd))
    for d, wrong in [(89, ["right", "obtuse", "straight"]), (91, ["right", "acute", "straight"]),
                     (175, ["straight", "acute", "right"])]:
        k = kind(d)
        e = {89: "89° is less than 90°, so it is acute (only just). A right angle is exactly 90°.",
             91: "91° is more than 90°, so it is obtuse (only just). A right angle is exactly 90°.",
             175: "175° is more than 90° but less than 180°, so it is obtuse. It is close to a straight angle, but not 180°."}[d]
        its.append(name_q("An angle measures %s. What is its name?" % D(d), k, wrong, e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(45, 0), (90, 0), (60, 30), (120, 0)], lab)) + "Which angle is obtuse?", "D",
                        "Obtuse means bigger than a right angle. D opens wider than the square corner in B. A and C are acute."))
    its.append(letter_q(fig(abcd_svg([(150, 0), (180, 0), (30, 0), (90, 0)], lab)) + "Which angle is a straight angle?", "B",
                        "A straight angle is 180°: the two arms make one straight line. A is obtuse, nearly straight, but it still has a bend."))
    its.append(mcq("Which list has only obtuse angles?", "95°, 130°, 175°",
                   ["45°, 100°, 160°", "90°, 120°, 150°", "100°, 180°, 140°"],
                   "Obtuse angles are more than 90° and less than 180°. 95°, 130° and 175° all fit. "
                   "45° is acute, 90° is right and 180° is straight.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?", "acute, right, obtuse, straight",
                   ["acute, obtuse, right, straight", "right, acute, obtuse, straight", "straight, obtuse, right, acute"],
                   "Acute is less than 90°, right is 90°, obtuse is between 90° and 180°, and straight is 180°.", rnd))
    its.append(mcq("How many right angles make one straight angle?", "2", ["3", "4", "1"],
                   "90° + 90° = 180°. Two right angles side by side make a straight line.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says an angle of 90° is obtuse because it is a big angle. Is %s right?" % (n, he),
                   "No, it is a right angle", ["Yes, it is obtuse", "No, it is acute", "No, it is straight"],
                   "An angle of exactly 90° is a right angle. Obtuse angles are more than 90°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Acute, right, obtuse and straight angles", "items": its}


# ------------------------------------------------------------ benchmark angles, estimating and comparing
BENCH = {45: "half a right angle (45°)", 90: "a right angle (90°)", 135: "halfway between a right angle and a straight angle (135°)",
         180: "a straight angle (180°)"}


def set_estimate(rnd, P):
    its = []
    q = "Use benchmark angles. Which is the best estimate for the marked angle?"
    for d, rot, best, wrong, e in [
        (28, 0, 30, [150, 60, 90],
         "The angle is less than half a right angle (45°). About 30° fits. (150° is what the outer scale of a protractor would say.)"),
        (43, 70, 45, [135, 90, 15],
         "The angle is about half of a right angle, so it is about 45°."),
        (62, 20, 60, [120, 30, 90],
         "The angle is more than half a right angle (45°) but less than a right angle (90°). About 60° fits."),
        (88, 30, 90, [45, 180, 135],
         "The angle looks like a square corner, so it is about 90°. (It is 88°.)"),
        (118, 5, 120, [60, 90, 180],
         "The angle is a bit more than a right angle (90°), but less than 135°. About 120° fits. (60° would be acute.)"),
        (137, 10, 135, [45, 90, 180],
         "The angle is about halfway between a right angle (90°) and a straight angle (180°), so it is about 135°."),
        (147, 0, 150, [30, 120, 90],
         "The angle is more than 135° but less than a straight angle (180°). About 150° fits. (30° is the acute angle on the other side.)"),
        (172, 0, 170, [10, 120, 90],
         "The arms almost make a straight line (180°), so the angle is about 170°. (10° is the small gap left to make a straight line.)"),
    ]:
        its.append(mcq(fig(angle_fig(d, rot)) + q, "about " + D(best), ["about " + D(w) for w in wrong], e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(85, 0), (45, 0), (15, 0), (135, 0)], lab)) + "Which angle is closest to 45°?", "B",
                        "45° is half a right angle. B is about half of a square corner. A is nearly a right angle, C is very small and D is obtuse."))
    its.append(letter_q(fig(abcd_svg([(60, 0), (165, 0), (120, 0), (95, 0)], lab)) + "Which angle is closest to 120°?", "C",
                        "120° is a bit more than a right angle, but less than 135°. C fits. A is acute, B is nearly straight and D is only just more than a right angle."))
    its.append(letter_q(fig(abcd_svg([(150, 0, 28), (100, 0, 40), (60, 0, 50), (30, 0, 58)], lab)) +
                        "Which angle is the largest?", "A",
                        "The size of an angle is the amount of turn between the arms, not the length of the arms. "
                        "A opens the widest (about 150°), even though its arms are the shortest."))
    its.append(letter_q(fig(abcd_svg([(70, 0, 30), (110, 0, 36), (25, 0, 58), (50, 0, 44)], lab)) +
                        "Which angle is the smallest?", "C",
                        "Look at how far the arms open, not how long they are. C opens the least (about 25°), "
                        "even though its arms are the longest."))
    its.append(mcq("An angle is a little smaller than a right angle. Which could it be?", "80°", ["100°", "45°", "170°"],
                   "A right angle is 90°. A little smaller than 90° is about 80°. 100° is a little bigger.", rnd))
    its.append(mcq("An angle is bigger than 45° but smaller than a right angle. Which could it be?", "60°", ["30°", "100°", "140°"],
                   "It must be between 45° and 90°. Only 60° fits. 30° is smaller than 45°, and 100° and 140° are bigger than 90°.", rnd))
    its.append(mcq("Which angle is closer to a right angle: 80° or 105°?", "80°", ["105°", "they are equally close", "you cannot tell"],
                   "80° is 10° away from 90°, because 90° − 80° = 10°. 105° is 15° away, because 105° − 90° = 15°. So 80° is closer.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?", "59°, 95°, 105°, 150°",
                   ["95°, 59°, 105°, 150°", "59°, 105°, 95°, 150°", "150°, 105°, 95°, 59°"],
                   "Compare the hundreds first, then the tens: 59° &lt; 95° &lt; 105° &lt; 150°.", rnd))
    its.append(dq("How many degrees is half of a right angle?", 45, [50, 90, 30],
                  "A right angle is 90°. Half of 90° is 90° ÷ 2 = 45°. (50° comes from thinking a right angle is 100°.)", rnd))
    n, he, his = P.next()
    its.append(mcq("Angle P has long arms. Angle Q has short arms but opens wider. %s says angle P is bigger because its arms are longer. "
                   "Is %s right?" % (n, he),
                   "No, Q is bigger", ["Yes, P is bigger", "No, they are equal", "Yes, long arms make big angles"],
                   "The size of an angle is how far the arms turn apart. The length of the arms does not matter. Q opens wider, so Q is bigger.", rnd))
    its.append(mcq("Leah’s angle is about halfway between a right angle and a straight angle. What is a good estimate?", "about 135°",
                   ["about 270°", "about 100°", "about 45°"],
                   "Halfway between 90° and 180° is 135°, because 90° + 45° = 135°. (270° comes from adding 90° + 180°.)", rnd))
    its.append(mcq("An angle is a little smaller than a straight angle. Which could it be?", "170°", ["190°", "100°", "80°"],
                   "A straight angle is 180°. A little smaller is about 170°. 190° is bigger than 180°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Benchmark angles: estimate and compare", "items": its}


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
    for v in (40, 65, 110, 155, 135):
        e = ("The bottom arm is on 0 at the right, so read the <b>inner</b> scale. It starts at 0 on the right. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The small marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " The outer scale says %d there, but it starts from the other side. The angle is %s, so %s makes sense." % (
            180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([0, v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for v in (30, 55, 120, 145, 70, 100):
        e = ("The bottom arm is on 0 at the left, so read the <b>outer</b> scale. It starts at 0 on the left. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The small marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " (The inner scale says %d there.) The angle is %s, so %s makes sense." % (180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([180, 180 - v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    its.append(mcq(fig(protractor_svg([20, 95], "protractor measuring an angle with neither arm on 0")) +
                   "Neither arm is on 0. What is the size of the angle?", D(75), [D(95), D(85), D(115)],
                   "On the inner scale one arm is at 20 and the other is at 95. The angle is the difference: 95° − 20° = 75°. "
                   "(95° comes from reading only one arm.)", rnd))
    its.append(mcq("Where do you put the centre of the protractor when you measure an angle?", "on the vertex",
                   ["at the end of an arm", "on the 90 mark", "in the middle of an arm"],
                   "The centre goes on the vertex, where the two arms meet. Then line up one arm with 0.", rnd))
    its.append(mcq("Why does a protractor have two scales?", "So you can start at 0 on either side",
                   ["One is for big angles only", "One is in centimetres", "So you can add the two numbers"],
                   "The inner scale starts at 0 on the right, and the outer scale starts at 0 on the left. "
                   "Read the scale that starts at 0 on your arm.", rnd))
    its.append(mcq("One arm of an angle is on 0 of the outer scale. Which scale should you read?", "the outer scale",
                   ["the inner scale", "the scale with the bigger number", "the scale with the smaller number"],
                   "Read the scale that starts at 0 on your arm. Here that is the outer scale.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s measures an angle that is clearly smaller than a right angle. The arm crosses the protractor at 35 and 145. "
                   "What is the angle?" % n, D(35), [D(145), D(110), D(180)],
                   "An angle smaller than a right angle is acute, less than 90°, so it is 35°. 145 is on the other scale.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures an angle and writes 40°. The angle is clearly obtuse. What should %s have written?" % (n, he),
                  140, [40, 50, 130],
                  "An obtuse angle is more than 90°. %s read the wrong scale: the other scale gives 180° − 40° = 140°." % n, rnd))
    n, he, his = P.next()
    its.append(mcq("%s wants to construct an angle of 65°. %s puts %s base line on 0 of the inner scale. Where should %s make a dot?"
                   % (n, cap(he), his, he), "at 65 on the inner scale",
                   ["at 65 on the outer scale", "5 small marks after 60", "at 115 on the inner scale"],
                   "Use the scale that starts at 0 on your base line: the inner scale. Count up to 65 (the small mark between 60 and 70), "
                   "make a dot, then join it to the vertex. The small marks go up in 5s, so 5 marks after 60 would be 85. "
                   "Using 65 on the outer scale would give 115°.", rnd))
    n, he, his = P.next()
    its.append(dq(fig(protractor_svg([0, 130], "protractor with an angle drawn on it")) +
                  "%s wanted to construct an angle of 50°. %s base arm is on 0 of the inner scale. "
                  "The picture shows what %s drew. What angle did %s actually draw?" % (n, cap(his), he, he),
                  130, [50, 120, 140],
                  "Read the inner scale, because the base arm is on its 0: the second arm is at 130, so the angle is 130°. "
                  "%s used 50 on the outer scale by mistake. 180° − 50° = 130°." % n, rnd))
    n, he, his = P.next()
    its.append(dq(fig(protractor_svg([180, 70], "protractor with an angle drawn on it")) +
                  "%s wanted to construct an angle of 70°. %s base arm is on 0 of the outer scale. "
                  "The picture shows what %s drew. What angle did %s actually draw?" % (n, cap(his), he, he),
                  110, [70, 100, 120],
                  "The base arm is on 0 of the outer scale, so read the outer scale: the second arm is at 110, so the angle is 110°. "
                  "%s used 70 on the inner scale by mistake. 180° − 70° = 110°." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a protractor: inner and outer scales", "items": its}


# ------------------------------------------------------------ angles that make a straight line
def set_line(rnd, P):
    its = []
    q_line = "The angles make a straight line. What is the missing angle?"
    for rot, parts, texts, v, wrong, e in [
        (0, [55, 125], ["55°", "?"], 125, [305, 35, 55],
         "Angles that make a straight line add up to 180°. 180° − 55° = 125°."),
        (15, [40, 140], ["?", "140°"], 40, [220, 50, 140],
         "The line is tilted, but it is still straight: 180° − 140° = 40°. (50° is 90° − 40°: the line is not a right angle.)"),
        (0, [110, 70], ["110°", "?"], 70, [250, 20, 110],
         "Angles that make a straight line add up to 180°. 180° − 110° = 70°. (20° comes from 110° − 90°.)"),
        (0, [90, 90], [None, "?"], 90, [270, 180, 45],
         "The small square shows a right angle, 90°. 180° − 90° = 90°, so the other angle is a right angle too."),
        (-10, [35, 145], ["35°", "?"], 145, [55, 325, 135],
         "180° − 35° = 145°. (55° is 90° − 35°: the line is not a right angle.)"),
        (0, [40, 85, 55], ["40°", "?", "55°"], 85, [265, 140, 95],
         "First add the angles you know: 40° + 55° = 95°. Then 180° − 95° = 85°."),
        (0, [90, 62, 28], [None, "62°", "?"], 28, [118, 298, 62],
         "The small square is a right angle: 90°. 90° + 62° = 152°, and 180° − 152° = 28°."),
        (0, [48, 90, 42], ["48°", None, "?"], 42, [132, 312, 48],
         "The small square is 90°. 48° + 90° = 138°, and 180° − 138° = 42°."),
    ]:
        its.append(dq(fig(line_svg(rot, parts, texts)) + q_line, v, wrong, e, rnd))
    its.append(dq(fig(line_svg(0, [60, 60, 60], ["a", "a", "a"])) +
                  "The three angles marked <i>a</i> are equal and make a straight line. What is <i>a</i>?", 60, [120, 90, 45],
                  "The three equal angles add up to 180°. 180° ÷ 3 = 60°. (120° comes from 360° ÷ 3.)", rnd))
    its.append(dq("Angles that make a straight line add up to …", 180, [360, 90, 100],
                  "A straight angle is 180°. Two right angles make a straight line: 90° + 90° = 180°.", rnd))
    its.append(dq("Two angles make a straight line. One angle is 72°. What is the other angle?", 108, [112, 18, 288],
                  "180° − 72° = 108°. Check: 108° + 72° = 180°. (112° comes from taking 0 − 2 the wrong way round, and 18° from 90° − 72°.)", rnd))
    its.append(dq("Two angles make a straight line. One angle is 135°. What is the other angle?", 45, [55, 225, 135],
                  "180° − 135° = 45°. Check: 135° + 45° = 180°. (55° comes from taking 0 − 5 the wrong way round, and 225° from 360° − 135°.)", rnd))
    its.append(dq("Two <b>equal</b> angles make a straight line. How big is each one?", 90, [180, 45, 60],
                  "180° ÷ 2 = 90°. Each one is a right angle.", rnd))
    its.append(name_q("Two angles make a straight line. One of them is obtuse. What kind of angle is the other one?", "acute",
                      ["obtuse", "right", "straight"],
                      "The two angles add up to 180°. The obtuse one is more than 90°, so less than 90° is left: the other one is acute. "
                      "(For example, 120° + 60° = 180°.)", rnd))
    its.append(mcq("Which pair of angles makes a straight line?", "65° and 115°",
                   ["65° and 125°", "45° and 45°", "90° and 100°"],
                   "Angles that make a straight line add up to 180°. 65° + 115° = 180°. "
                   "65° + 125° = 190°, 45° + 45° = 90° and 90° + 100° = 190°.", rnd))
    n, he, his = P.next()
    its.append(mcq("Two angles are 100° and 70°. %s says they make a straight line. Is %s right?" % (n, he),
                   "No, they add up to 170°", ["Yes, they add up to 180°", "No, they add up to 190°", "Yes, both are obtuse"],
                   "100° + 70° = 170°. A straight line needs 180°, so they do not make a straight line.", rnd))
    n, he, his = P.next()
    its.append(mcq("Two angles make a straight line. One is 50°. %s says the other is 310° because 360° − 50° = 310°. Is %s right?"
                   % (n, he), "No, it is 130°", ["Yes, it is 310°", "No, it is 40°", "No, it is 50°"],
                   "A straight line is 180°, not 360°. 180° − 50° = 130°.", rnd))
    its.append(dq("Three angles make a straight line. Two of them are 30° and 70°. What is the third angle?", 80, [100, 260, 10],
                  "30° + 70° = 100°. 180° − 100° = 80°. (100° is the sum of the two angles, not the missing one.)", rnd))
    its.append(dq("A straight line is split into a right angle and two equal angles. How big is each equal angle?", 45, [90, 135, 30],
                  "180° − 90° = 90° is left for the two equal angles. 90° ÷ 2 = 45°.", rnd))
    its.append(dq("Two angles make a straight line. One angle is twice as big as the other. How big is the smaller angle?", 60,
                  [90, 120, 45],
                  "The smaller angle is 1 part and the bigger angle is 2 parts: 3 parts make 180°. 180° ÷ 3 = 60°. "
                  "The bigger angle is 120°. (90° comes from sharing 180° into 2 equal parts.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles that make a straight line", "items": its}


# ------------------------------------------------------------ angles in real life
def ramp_svg(a, label="a ramp on flat ground"):
    """Flat ground (a straight line) and a ramp rising from a point on it at angle a. The other angle is marked “?”."""
    return line_svg(0, [a, 180 - a], [D(a), "?"], L=100, label=label)


def set_real(rnd, P):
    its = []
    for h, v, wrong, e in [
        (3, 90, [30, 15, 60],
         "The 12 spaces between the numbers go around the clock, and each space is 30°. "
         "At 3 o’clock the hands are 3 spaces apart: 3 × 30° = 90°, a right angle. (15° counts 3 × 5 minutes.)"),
        (2, 60, [20, 10, 120],
         "Each space between two numbers is 30°. At 2 o’clock the hands are 2 spaces apart: 2 × 30° = 60°. "
         "(10° counts 2 × 5 minutes.)"),
        (5, 150, [50, 25, 120],
         "Each space between two numbers is 30°. At 5 o’clock the hands are 5 spaces apart: 5 × 30° = 150°. "
         "(25° counts 5 × 5 minutes.)"),
        (6, 180, [60, 30, 90],
         "At 6 o’clock the hands point in opposite directions. They make a straight line: 180°. (6 × 30° = 180°.)"),
    ]:
        its.append(dq(fig(clock_svg(h)) + "What is the size of the marked angle between the hands at %d o’clock?" % h,
                      v, wrong, e, rnd))
    its.append(name_q(fig(clock_svg(4)) + "What kind of angle do the hands make at 4 o’clock?", "obtuse",
                      ["acute", "right", "straight"],
                      "At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°. That is more than 90° but less than 180°, so it is obtuse.", rnd))
    its.append(mcq("At which time do the hands of a clock make a right angle?", "3:00", ["6:00", "12:00", "4:00"],
                   "At 3:00 the minute hand points to 12 and the hour hand points to 3: a quarter turn, 90°. "
                   "At 6:00 they make a straight line, and at 12:00 they are on top of each other.", rnd))
    its.append(dq("How many degrees does the minute hand turn in 15 minutes?", 90, [15, 45, 180],
                  "In 15 minutes the minute hand goes from 12 to 3, a quarter of the way around: a right angle, 90°.", rnd))
    its.append(dq("How many degrees does the minute hand turn from 7:15 a.m. to 7:45 a.m.?", 180, [30, 90, 45],
                  "In 30 minutes the minute hand goes from 3 to 9, halfway around. The start and end make a straight line: 180°.", rnd))
    its.append(dq(fig(ramp_svg(20)) + "A ramp makes an angle of 20° with the flat ground. What is the angle marked “?”?",
                  160, [70, 340, 20],
                  "The ground is a straight line, so the two angles add up to 180°. 180° − 20° = 160°. (70° comes from 90° − 20°.)", rnd))
    its.append(dq(fig(ramp_svg(35, "a ladder leaning on flat ground")) +
                  "A ladder rests on flat ground and makes an angle of 35° with it. What is the angle marked “?”?",
                  145, [55, 325, 155],
                  "The ground is a straight line: 180° − 35° = 145°. (55° comes from 90° − 35°.)", rnd))
    its.append(mcq("A wheelchair ramp makes an angle of 5° with the ground. A skateboard ramp makes 30°. Which is steeper?",
                   "the skateboard ramp", ["the wheelchair ramp", "they are the same", "you cannot tell"],
                   "The bigger the angle with the ground, the steeper the ramp. 30° is bigger than 5°, so the skateboard ramp is steeper.", rnd))
    its.append(name_q("At the skatepark, a ramp makes an angle of 25° with the ground. What kind of angle is that?", "acute",
                      ["obtuse", "right", "straight"],
                      "25° is less than 90°, so it is acute. Ramps are usually acute angles.", rnd))
    its.append(name_q("A classroom door is opened so that it makes an angle of 100° with the wall. What kind of angle is this?",
                      "obtuse", ["acute", "right", "straight"],
                      "100° is more than 90° but less than 180°, so it is obtuse.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s opens a book and lays it flat on the desk. The two covers make one straight line. What kind of angle is that?" % n,
                      "straight", ["obtuse", "right", "acute"],
                      "The covers make a straight line, so the angle is a straight angle: 180°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures the slope of a ski hill with a protractor and writes 155°, but the slope is clearly acute. "
                  "What is the angle?" % n, 25, [155, 65, 35],
                  "An acute angle is less than 90°. %s read the wrong scale: 180° − 155° = 25°." % n, rnd))
    n, he, his = P.next()
    its.append(dq("%s opens a laptop so the screen makes 110° with the keyboard. Then %s opens it until it is flat (a straight line). "
                  "How many more degrees did the screen turn?" % (n, he), 70, [250, 110, 180],
                  "Flat is 180°. 180° − 110° = 70° more. (250° comes from using 360° instead of 180°.)", rnd))
    n, he, his = P.next()
    its.append(dq("%s’s scissors are open 40°. %s opens them twice as wide. What is the angle now?" % (n, cap(he)), 80,
                  [20, 60, 140],
                  "Twice as wide means 2 × 40° = 80°. (20° is half as wide, and 60° only adds 20°.)", rnd))
    its.append(dq("A hockey stick’s blade lies flat on the ice. The shaft and the blade make an angle of 135°. "
                  "What angle does the shaft make with the ice on the other side?", 45, [135, 55, 225],
                  "The blade lies flat on the ice, so the two angles make a straight line: 180° − 135° = 45°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s’s canoe paddle and the water make an angle of about 45°. Which benchmark is that?" % n,
                   "half a right angle", ["a right angle", "a straight angle", "more than a right angle"],
                   "45° is half of 90°, so it is half a right angle.", rnd))
    n, he, his = P.next()
    its.append(dq("In coding class, %s’s robot faces north and turns 90° clockwise. Then it turns 90° clockwise again. "
                  "How many degrees has it turned in all?" % n, 180, [90, 360, 270],
                  "90° + 90° = 180°. The robot made a half turn and now faces south.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in real life: clocks, ramps and more", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    bench = strip_svg([angle_fig(45, 0, L=55), angle_fig(90, 0, L=55), angle_fig(180, 0, L=55)],
                      ["45°", "90°", "180°"], "benchmark angles of 45, 90 and 180 degrees", cw=150)
    kinds = strip_svg([angle_fig(40, 0, L=55), angle_fig(90, 0, L=55), angle_fig(130, 0, L=55), angle_fig(180, 0, L=55)],
                      ["acute", "right", "obtuse", "straight"], "acute, right, obtuse and straight angles", cw=140)
    prot = protractor_svg([0, 50], "protractor measuring a 50 degree angle")
    line = line_svg(0, [55, 125], ["55°", "?"])
    return (
        "<h2>Benchmark angles</h2>"
        "<p>An angle is the amount of <b>turn</b> between two arms. We measure it in <b>degrees</b> (°). "
        "Three benchmark angles help you estimate: <b>45°</b> (half a right angle), <b>90°</b> (a right angle, a square corner) "
        "and <b>180°</b> (a straight angle).</p>"
        "<figure class='sn-fig'>" + bench +
        "<figcaption>Compare an angle with these three before you measure it.</figcaption></figure>" +
        ex("Estimate", "An angle opens a bit wider than a square corner, but not halfway to a straight line. Estimate it.",
           "It is more than 90° and less than 135° (halfway between 90° and 180°).", "about 110°") +
        "<p>The length of the arms does not change the size of an angle. Only the turn matters.</p>"
        "<h2>Angle names</h2>"
        "<figure class='sn-fig'>" + kinds + "</figure>" +
        table(["Name", "Size"], [
            ["Acute angle", "less than 90°"],
            ["Right angle", "exactly 90°"],
            ["Obtuse angle", "more than 90°, less than 180°"],
            ["Straight angle", "exactly 180°"],
        ]) +
        "<h2>How a protractor works</h2>"
        "<p>A protractor is half a circle split into 180 small turns of 1°. It has <b>two scales</b>, so you can start at 0 on "
        "either side. The inner scale starts at 0 on the right. The outer scale starts at 0 on the left.</p>"
        "<p>1. Estimate first: acute or obtuse? 2. Put the centre of the protractor on the vertex. 3. Line up one arm with <b>0</b>. "
        "4. Read the scale that <b>starts at 0 on that arm</b>. 5. Check the reading against your estimate.</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom arm is on 0 of the inner (green) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same place, but the angle is acute, so 130° cannot be right.</figcaption></figure>" +
        ex("Construct an angle of 70°", "Draw a base line and mark the vertex. How do you draw 70°?",
           "Put the centre on the vertex and the base line on 0. Use the scale that starts at 0 on your line, "
           "make a dot at 70, then join the dot to the vertex.", "a dot at 70 on the scale that starts at 0") +
        "<h2>Angles that make a straight line</h2>"
        "<p>Angles that make a straight line add up to <b>180°</b>. To find a missing angle, subtract from 180°.</p>"
        "<figure class='sn-fig'>" + line + "</figure>" +
        ex("Find the missing angle", "Two angles make a straight line. One is 55°. Find the other.",
           "180° − 55° = 125°. Check: 125° + 55° = 180°.", "125°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (140° for a 40° angle)", "Read the scale that starts at 0 on your arm, then check your estimate"],
            ["Thinking longer arms make a bigger angle", "Compare how far the arms open, not how long they are"],
            ["Calling 90° obtuse", "Exactly 90° is a right angle. Obtuse is more than 90°"],
            ["Subtracting from 360° on a straight line", "Angles that make a straight line add up to 180°"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about angles in the Ontario math curriculum?",
     "a": "They use benchmark angles like 45°, 90° and 180° to estimate and compare angles, and they learn how a protractor works so they can measure and construct angles up to 180°."},
    {"q": "How do you use a protractor to measure an angle?",
     "a": "Put the centre of the protractor on the vertex, line up one arm with 0, then read the scale that starts at 0 on that arm. Check the reading against your estimate: acute angles are less than 90°."},
    {"q": "Why does a protractor have two scales?",
     "a": "So you can measure from an arm on either side: the inner scale starts at 0 on the right and the outer scale starts at 0 on the left. Reading the wrong scale is the most common mistake."},
    {"q": "What are benchmark angles?",
     "a": "Benchmark angles are angles you know well, such as 45° (half a right angle), 90° (a right angle) and 180° (a straight angle). Comparing with them gives a quick estimate before you measure."},
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
    rnd = random.Random(45817)
    P = People(rnd)
    sets = [set_names(rnd, P), set_estimate(rnd, P), set_protractor(rnd, P), set_line(rnd, P), set_real(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "measuring-angles", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Angles: Benchmark Angles, Protractors and Angles on a Straight Line",
        "seo_title": "Grade 5 Measuring Angles Worksheets: Protractor and Benchmark Angles (Free, Answer Key)",
        "short_title": "Measuring angles",
        "domain": "Spatial Sense",
        "standard_code": "Grade 5: E2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Explain how protractors work, use a protractor to measure and construct angles up to 180°, "
                         "and use benchmark angles to estimate the size of other angles",
        "meta_desc": "Free Grade 5 math worksheets on measuring angles for the Ontario curriculum: estimate with benchmark angles "
                     "(45°, 90°, 180°), compare angles, read the inner and outer protractor scales, name acute, right, obtuse and "
                     "straight angles, and find angles on a straight line. 100 questions with an answer key.",
        "key_big": "Estimate first, then read the protractor scale that starts at 0 on your arm.",
        "key_sub": "Benchmarks: 45° is half a right angle, 90° is a right angle and 180° is a straight angle. "
                   "Acute is less than 90°, obtuse is between 90° and 180°. Angles that make a straight line add up to 180°.",
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
