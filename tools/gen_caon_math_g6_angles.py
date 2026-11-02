# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Measuring angles
(Ontario Curriculum 2020, Grade 6: Spatial Sense, E2)
  python3 tools/gen_ca_math_g6_angles.py
Name angles (acute, right, obtuse, straight, reflex), read both protractor scales, find reflex angles
(360° − x), relate clockwise and counterclockwise angles between the same arms (they add up to 360°),
and angles in real life. Canadian English. HTML attributes use single quotes (no backslashes in the JSON).

Every angle is drawn exactly at its size (trig, 0° = pointing right, counterclockwise, SVG y goes down);
every marked angle is measured back from the drawing and checked against its value.
Labels are checked so that they do not touch a line, an arc or another label.
Protractor: inner scale has 0 on the right (counts counterclockwise), outer scale has 0 on the left
(counts clockwise); marks every 5°, numbers every 10°.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
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
# ------------------------------------------------------------ Grade 6 figures: clockwise and counterclockwise
def turn_fig(rot, d, t_ccw=None, t_cw=None, arrows=True, ccw=True, cw=True, L=82, label="two angles between the same arms"):
    """Two arms from O: one at rot, one at rot + d (counterclockwise).
    The counterclockwise angle (d) has an arc of radius 20 from the first arm; the clockwise angle (360 − d) has an
    arc of radius 30 going the other way from the same arm. With arrows, each arc ends in an arrowhead at the other arm."""
    assert 0 < d < 360
    P = Pic()
    P.line(O, pol(O, L, rot))
    P.line(O, pol(O, L, rot + d))
    if ccw:
        r = 20
        P.arc(O, r, rot, rot + d)
        if arrows:
            E = pol(O, r, rot + d)
            t = rot + d + 90
            P.polyline([pol(E, 7, t + 180 - 35), E, pol(E, 7, t + 180 + 35)], INK, 1.8)
        if t_ccw:
            P.todo.append((O, rot, d, r + (4 if arrows else 0), t_ccw, L, None))
    if cw:
        r = 32 if ccw else 22
        e = 360 - d
        P.arc(O, r, rot + d, rot + 360, col=RED if (ccw and arrows) else INK)
        if arrows:
            E = pol(O, r, rot + d)
            t = rot + d - 90
            P.polyline([pol(E, 7, t + 180 - 35), E, pol(E, 7, t + 180 + 35)], RED if ccw else INK, 1.8)
        if t_cw:
            P.todo.append((O, rot + d, e, r + (4 if arrows else 0), t_cw, L, None))
    P.dot(O)
    return P.svg(label)


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


def set_names(rnd, P):
    its = []
    q = "What is the name of the marked angle?"
    for d, rot in [(35, 15), (125, 0), (230, 0), (90, 30), (320, 20), (160, 10), (70, 100), (180, 0),
                   (200, 200), (100, 160), (180, 35), (265, 45)]:
        k = kind(d)
        e = KIND_E[k]
        if d not in (90, 180):
            e += " This angle is %s." % D(d)
        if k == "reflex":
            e += " (The gap between the arms is %s, but the arc marks the big angle around the outside.)" % D(360 - d)
        if d == 90 or (d == 180 and rot):
            e += " Turning the angle does not change its size or its name."
        its.append(name_q(fig(angle_fig(d, rot)) + q, k, WRONG[k], e, rnd))
    for d, wrong in [(175, ["straight", "reflex", "acute"]), (185, ["obtuse", "straight", "acute"]),
                     (89, ["right", "obtuse", "reflex"]), (270, ["obtuse", "straight", "right"])]:
        k = kind(d)
        e = {175: "175° is more than 90° but less than 180°, so it is obtuse. It is close to a straight angle, but not 180°.",
             185: "185° is more than 180° but less than 360°, so it is reflex, even though it is close to a straight angle.",
             89: "89° is less than 90°, so it is acute (only just). A right angle is exactly 90°.",
             270: "270° is more than 180° but less than 360°, so it is reflex. It is three right angles: 3 × 90° = 270°."}[d]
        its.append(name_q("An angle measures %s. What is its name?" % D(d), k, wrong, e, rnd))
    n, he, his = P.next()
    its.append(mcq("%s says an angle of 190° is obtuse because it is bigger than 90°. Is %s right?" % (n, he),
                   "No, it is reflex", ["Yes, it is obtuse", "No, it is acute", "No, it is straight"],
                   "Obtuse angles are bigger than 90° but smaller than 180°. 190° is more than 180°, so it is reflex.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?",
                   "acute, right, obtuse, straight, reflex",
                   ["acute, obtuse, right, straight, reflex", "acute, right, obtuse, reflex, straight",
                    "right, acute, obtuse, straight, reflex"],
                   "Acute is less than 90°, right is 90°, obtuse is between 90° and 180°, straight is 180° "
                   "and reflex is between 180° and 360°.", rnd))
    its.append(mcq("Which list has only reflex angles?", "200°, 270°, 345°",
                   ["100°, 150°, 175°", "95°, 180°, 270°", "45°, 190°, 300°"],
                   "Reflex angles are more than 180° and less than 360°. 200°, 270° and 345° all fit. "
                   "100°, 150° and 175° are obtuse, 180° is straight and 45° is acute.", rnd))
    its.append(dq("How many degrees are in a full turn?", 360, [180, 90, 100],
                  "A full turn is 360°. It is 4 right angles: 4 × 90° = 360°. "
                  "180° is a straight angle, only half a turn.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name the angle", "items": its}


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
                   "An angle smaller than a right angle is acute, less than 90°, so it is 35°. 145 is on the other scale.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures an angle and writes 40°. The angle is clearly obtuse. What should %s have written?" % (n, he),
                  140, [40, 220, 320],
                  "An obtuse angle is more than 90°. %s read the wrong scale: the other scale gives 180° − 40° = 140°." % n, rnd))
    n, he, his = P.next()
    its.append(dq(fig(protractor_svg([0, 130], "protractor with an angle drawn on it")) +
                  "%s wanted to construct an angle of 50°. %s base arm is on 0 of the inner scale. "
                  "The picture shows what %s drew. What angle did %s actually draw?" % (n, cap(his), he, he),
                  130, [50, 230, 310],
                  "Read the inner scale, because the base arm is on its 0: the second arm is at 130, so the angle is 130°. "
                  "%s used 50 on the outer scale by mistake. 180° − 50° = 130°." % n, rnd))
    n, he, his = P.next()
    its.append(dq(fig(protractor_svg([180, 70], "protractor with an angle drawn on it")) +
                  "%s wanted to construct an angle of 70°. %s base arm is on 0 of the outer scale. "
                  "The picture shows what %s drew. What angle did %s actually draw?" % (n, cap(his), he, he),
                  110, [70, 250, 290],
                  "The base arm is on 0 of the outer scale, so read the outer scale: the second arm is at 110, so the angle is 110°. "
                  "%s used 70 on the inner scale by mistake. 180° − 70° = 110°." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a protractor (both scales)", "items": its}


# ------------------------------------------------------------ reflex angles
REFL = "reflex angle and the angle on the other side"


def set_reflex(rnd, P):
    its = []
    q = "Work out the reflex angle marked “?”."
    for rot, x, wrong in [(0, 70, [110, 70, 250]), (20, 125, [55, 125, 305]), (10, 40, [140, 40, 220]),
                          (0, 155, [25, 155, 335])]:
        its.append(dq(fig(turn_fig(rot, x, D(x), "?", arrows=False, label=REFL)) + q, 360 - x, wrong,
                      "The two angles go all the way around the vertex, so they add up to 360°. 360° − %s = %s. "
                      "(%s comes from using 180° instead of 360°.)" % (D(x), D(360 - x), D(180 - x)), rnd))
    for rot, x, wrong in [(0, 110, [70, 610, 250]), (30, 60, [120, 660, 300])]:
        its.append(dq(fig(turn_fig(rot, x, "?", D(360 - x), arrows=False, label=REFL)) +
                      "The reflex angle is %s. Work out the angle marked “?”." % D(360 - x), x, wrong,
                      "The two angles add up to 360°. 360° − %s = %s. (%s comes from %s − 180°, and %s from adding.)"
                      % (D(360 - x), D(x), D(180 - x), D(360 - x), D(720 - x)), rnd))
    its.append(dq(fig(protractor_svg([0, 75], "protractor measuring an angle")) +
                  "The protractor measures the angle between the two arms. What is the <b>reflex</b> angle between the same arms?",
                  285, [75, 105, 255],
                  "On the inner scale the angle is 75°. The reflex angle goes the other way around. Together they make a full turn: "
                  "360° − 75° = 285°. (105° is the reading on the wrong scale.)", rnd))
    its.append(dq(fig(protractor_svg([180, 130], "protractor measuring an angle")) +
                  "The protractor measures the angle between the two arms. What is the <b>reflex</b> angle between the same arms?",
                  310, [50, 130, 230],
                  "The left arm is on 0 of the outer scale, so the angle is 50°. The reflex angle is 360° − 50° = 310°. "
                  "(230° comes from reading 130 on the wrong scale: 360° − 130° = 230°.)", rnd))
    n, he, his = P.next()
    its.append(dq("To find a reflex angle, %s measures the angle on the other side. It is 130°. What is the reflex angle?" % n,
                  230, [130, 50, 310],
                  "The two angles go all the way around the vertex, so they make a full turn: 360°. 360° − 130° = 230°. "
                  "(50° comes from using 180° instead of 360°.)", rnd))
    its.append(dq("The gap between the arms of a reflex angle is 45°. How big is the reflex angle?", 315, [135, 225, 405],
                  "360° − 45° = 315°. (135° comes from 180° − 45°, and 225° from 180° + 45°.)", rnd))
    its.append(dq("A reflex angle is 200°. How big is the angle on the other side of its arms?", 160, [20, 200, 560],
                  "The two angles make a full turn: 360° − 200° = 160°. (20° comes from 200° − 180°.)", rnd))
    its.append(mcq("A protractor only goes to 180°. How can you construct a reflex angle of 250°?",
                   "Draw 110°, then mark the angle outside it",
                   ["Draw 70°, then mark the angle outside it", "Draw 250 on the outer scale", "You cannot construct it"],
                   "360° − 250° = 110°. Construct an angle of 110°. The angle around the outside is then 250°. "
                   "(70° comes from 250° − 180°, but the two angles must make a full turn, 360°.)", rnd))
    its.append(dq("To construct a reflex angle of 300°, which angle should you draw first with the protractor?", 60,
                  [120, 30, 240],
                  "The two angles around the vertex make a full turn: 360°. 360° − 300° = 60°. Draw 60°, "
                  "then mark the big angle around the outside. (120° comes from 300° − 180°.)", rnd))
    its.append(mcq("Another way to construct 215°: draw a straight angle (180°), then add more. How much more?", "35°",
                   ["145°", "125°", "215°"],
                   "215° − 180° = 35°. Draw a straight line through the vertex, then measure 35° more past it. "
                   "(145° is 360° − 215°, the angle on the other side.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says the reflex angle is 120° when the gap between the arms is 60°, because 180° − 60° = 120°. Is %s right?"
                   % (n, he), "No, it is 300°", ["Yes, it is 120°", "No, it is 240°", "No, it is 60°"],
                   "A reflex angle is more than 180°, so 120° cannot be right. The two angles make a full turn: 360° − 60° = 300°.", rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(120, 0), (240, 0), (300, 0), (200, 0)], lab)) + "Which drawing shows an angle of 240°?", "B",
                        "240° is reflex: 360° − 240° = 120° is left for the gap. In B the arc goes around the outside of a 120° gap. "
                        "A marks only the 120° gap. C is 300° and D is 200°."))
    its.append(letter_q(fig(abcd_svg([(60, 0), (120, 0), (210, 0), (300, 0)], lab)) + "Which drawing shows an angle of 300°?", "D",
                        "300° is reflex: the gap is 360° − 300° = 60°, and the arc goes around the outside. "
                        "A marks only the 60° gap. C is 210°."))
    its.append(dq(fig(clock_svg(4)) + "The marked angle between the hands at 4 o’clock is 120°. What is the reflex angle between the hands?",
                  240, [60, 120, 480],
                  "The two angles between the hands make a full turn: 360° − 120° = 240°. (60° comes from 180° − 120°.)", rnd))
    its.append(dq("An angle is three right angles plus 20°. How big is it?", 290, [110, 200, 250],
                  "Three right angles are 3 × 90° = 270°. 270° + 20° = 290°, a reflex angle. (110° is 90° + 20°.)", rnd))
    its.append(dq("A reflex angle is 3 times as big as the angle on the other side of its arms. How big is the reflex angle?",
                  270, [135, 90, 120],
                  "The two angles make 4 equal parts of 360°: 360° ÷ 4 = 90°. The reflex angle is 3 × 90° = 270°. "
                  "(135° comes from sharing 180° instead of 360°.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflex angles: 360° − x", "items": its}


# ------------------------------------------------------------ clockwise and counterclockwise
TURN = "counterclockwise and clockwise angles between the same arms"


def set_turns(rnd, P):
    its = []
    for rot, x, known, wrong in [(0, 70, "ccw", [110, 70, 250]), (10, 260, "cw", [80, 100, 280]),
                                 (-20, 145, "ccw", [35, 145, 325]), (30, 325, "cw", [145, 35, 215]),
                                 (0, 230, "ccw", [50, 230, 590]), (90, 90, "cw", [270, 630, 180])]:
        # x is the counterclockwise angle; the clockwise angle is 360 − x
        if known == "ccw":
            v, k = 360 - x, x
            q = ("The black arrow turns <b>counterclockwise</b> through %s. The red arrow turns <b>clockwise</b> "
                 "from the same arm to the same arm. How big is the clockwise angle?" % D(x))
            f = turn_fig(rot, x, D(x), "?", label=TURN)
        else:
            v, k = x, 360 - x
            q = ("The red arrow turns <b>clockwise</b> through %s. The black arrow turns <b>counterclockwise</b> "
                 "from the same arm to the same arm. How big is the counterclockwise angle?" % D(360 - x))
            f = turn_fig(rot, x, "?", D(360 - x), label=TURN)
        e = ("The clockwise and counterclockwise angles between the same two arms add up to a full turn, 360°. "
             "360° − %s = %s." % (D(k), D(v)))
        if 180 - k > 0:
            e += " (%s comes from using 180° instead of 360°.)" % D(180 - k)
        its.append(dq(fig(f) + q, v, wrong, e, rnd))
    its.append(mcq(fig(turn_fig(15, 300, ccw=False, label="an arrow turning from one arm to another")) +
                   "The arrow shows a turn from one arm to the other. Which describes the turn?",
                   "about 60° clockwise", ["about 60° counterclockwise", "about 300° clockwise", "about 120° clockwise"],
                   "The arrow turns the same way as the hands of a clock, so it is clockwise. It turns less than a right angle: about 60°. "
                   "The counterclockwise angle between the same arms would be about 300°.", rnd))
    its.append(mcq(fig(turn_fig(0, 250, cw=False, label="an arrow turning from one arm to another")) +
                   "The arrow shows a turn from one arm to the other. Which describes the turn?",
                   "about 250° counterclockwise", ["about 110° counterclockwise", "about 250° clockwise", "about 110° clockwise"],
                   "The arrow turns the opposite way to the hands of a clock, so it is counterclockwise. It goes past a straight angle, "
                   "so it is reflex: about 250°. The clockwise angle between the same arms is about 110°.", rnd))
    its.append(dq("The clockwise angle and the counterclockwise angle between the same two arms always add up to …", 360,
                  [180, 90, 270],
                  "Turning one way and then the other way between the same two arms makes one full turn: 360°.", rnd))
    n, he, his = P.next()
    its.append(mcq("The counterclockwise angle between two arms is 80°. %s says the clockwise angle is 100°, because they add up to 180°. "
                   "Is %s right?" % (n, he), "No, it is 280°", ["Yes, it is 100°", "No, it is 80°", "No, it is 260°"],
                   "Clockwise and counterclockwise angles between the same arms add up to 360°, not 180°. 360° − 80° = 280°.", rnd))
    its.append(dq(fig(protractor_svg([0, 60], "protractor measuring an angle")) +
                  "The inner scale counts counterclockwise from the right arm, so the counterclockwise angle is 60°. "
                  "What is the clockwise angle from the right arm to the other arm?", 300, [120, 60, 240],
                  "The two angles add up to 360°: 360° − 60° = 300°. (120° is the outer scale reading, which is a different angle.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces north. %s turns 90° clockwise. Which way is %s facing now?" % (n, cap(he), he), "east",
                   ["west", "south", "north"],
                   "Clockwise goes north → east → south → west. A quarter turn (90°) clockwise from north is east. "
                   "West would be a quarter turn counterclockwise.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces east. %s turns 270° counterclockwise. Which way is %s facing now?" % (n, cap(he), he), "south",
                   ["north", "west", "east"],
                   "Counterclockwise goes east → north → west → south. 270° is three quarter turns, so %s ends up facing south. "
                   "(It is the same as 90° clockwise.)" % n, rnd))
    its.append(dq("A turn of 90° clockwise ends in the same place as a counterclockwise turn of …", 270, [90, 180, 450],
                  "The two turns add up to 360°. 360° − 90° = 270° counterclockwise.", rnd))
    its.append(dq("A turn of 120° counterclockwise ends in the same place as a clockwise turn of …", 240, [120, 60, 480],
                  "The two turns add up to 360°. 360° − 120° = 240° clockwise. (60° comes from using 180°.)", rnd))
    its.append(dq("A clock hand points at 12. If it turned <b>counterclockwise</b> to 4, how many degrees would it turn?", 240,
                  [120, 60, 270],
                  "Each hour space is 360° ÷ 12 = 30°. Clockwise from 12 to 4 is 4 × 30° = 120°. "
                  "Counterclockwise is the other way around: 360° − 120° = 240°.", rnd))
    its.append(dq("The minute hand turns clockwise from 12 to 9. How many degrees does it turn?", 270, [90, 180, 45],
                  "12 to 3, 3 to 6 and 6 to 9 are three quarter turns: 3 × 90° = 270°, a reflex angle. "
                  "(90° is the counterclockwise turn from 12 to 9.)", rnd))
    its.append(mcq("The clockwise angle between two arms is 185°. What is the counterclockwise angle between the same arms?",
                   "175°, an obtuse angle", ["175°, a reflex angle", "5°, an acute angle", "185°, an obtuse angle"],
                   "360° − 185° = 175°. It is between 90° and 180°, so it is obtuse. (5° comes from 185° − 180°.)", rnd))
    its.append(dq("The clockwise and counterclockwise angles between two arms are equal. How big is each one?", 180, [90, 360, 120],
                  "They add up to 360°, and they are equal: 360° ÷ 2 = 180°. The two arms make a straight line.", rnd))
    its.append(dq("A turn of <i>x</i> counterclockwise and a turn of 3<i>x</i> clockwise go from the same arm to the same arm. "
                  "What is <i>x</i>?", 90, [45, 120, 270],
                  "The two turns add up to 360°: <i>x</i> + 3<i>x</i> = 4<i>x</i> = 360°, so <i>x</i> = 90°. "
                  "(45° comes from using 180°.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Clockwise and counterclockwise angles", "items": its}


# ------------------------------------------------------------ angles in real life
def set_real(rnd, P):
    its = []
    its.append(dq(fig(clock_svg(4)) + "What is the size of the marked angle between the hands at 4 o’clock?", 120,
                  [240, 90, 40],
                  "The 12 spaces between the numbers go around a full turn, 360°, so each space is 360° ÷ 12 = 30°. "
                  "At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°.", rnd))
    its.append(dq(fig(clock_svg(10)) + "What is the size of the marked angle between the hands at 10 o’clock?", 60, [300, 30, 120],
                  "From 10 to 12 is 2 hour spaces. Each space is 30°, so 2 × 30° = 60°. (300° is the reflex angle the other way around.)", rnd))
    its.append(dq("What is the reflex angle between the hands of a clock at 2 o’clock?", 300, [60, 120, 240],
                  "The smaller angle is 2 × 30° = 60°. The reflex angle goes the other way around: 360° − 60° = 300°.", rnd))
    its.append(dq("How many degrees does the minute hand turn in 20 minutes?", 120, [20, 60, 240],
                  "The minute hand turns 360° in 60 minutes, so 6° each minute. 20 × 6° = 120°. (240° is the other 40 minutes.)", rnd))
    its.append(dq("How many degrees does the minute hand turn from 3:00 p.m. to 3:45 p.m.?", 270, [45, 90, 180],
                  "45 minutes is three quarters of an hour, so three quarter turns: 3 × 90° = 270°, a reflex angle.", rnd))
    n, he, his = P.next()
    its.append(dq("On pizza day, a round pizza is cut into 8 equal slices from the centre. %s eats 3 slices. "
                  "What angle at the centre do the slices that are left make?" % n,
                  225, [135, 45, 180],
                  "Each slice is 360° ÷ 8 = 45°. 5 slices are left: 5 × 45° = 225°, a reflex angle. (135° is the 3 slices that were eaten.)", rnd))
    n, he, his = P.next()
    its.append(dq("At the skating rink, %s spins 3 full turns. How many degrees does %s turn?" % (n, he), 1080, [540, 360, 900],
                  "One full turn is 360°. 3 × 360° = 1080°. (540° comes from using 180° for a full turn.)", rnd))
    its.append(name_q("A classroom door is opened so that it makes an angle of 100° with the wall. What is the name of this angle?",
                      "obtuse", ["acute", "right", "reflex"],
                      "100° is more than 90° but less than 180°, so it is obtuse.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s is canoeing at the cottage, facing west. %s turns the canoe 90° counterclockwise. Which way is %s facing now?"
                   % (n, cap(he), he), "south", ["north", "east", "west"],
                   "Counterclockwise from west goes to south (north → west → south → east). "
                   "North would be 90° clockwise.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures the slope of a ski hill with a protractor and writes 155°, but the slope is clearly acute. "
                  "What is the angle?" % n, 25, [155, 205, 65],
                  "An acute angle is less than 90°. %s read the wrong scale: 180° − 155° = 25°." % n, rnd))
    its.append(dq("In a circle graph, the section for “hockey” is one quarter of the circle. What angle does it make at the centre?",
                  90, [25, 45, 180],
                  "A full circle is 360°. One quarter of 360° is 360° ÷ 4 = 90°. (25° confuses a quarter with 25%.)", rnd))
    its.append(mcq("In a circle graph, the section for “soccer” makes an angle of 120° at the centre. What fraction of the circle is it?",
                   "one third", ["one quarter", "one half", "one sixth"],
                   "120° out of 360°: 360° ÷ 120° = 3, so it is one third. (One half would be 180°, and one quarter 90°.)", rnd))
    its.append(dq("A lawn sprinkler waters while it turns 150° counterclockwise. What angle around the sprinkler does it not water?",
                  210, [30, 150, 510],
                  "The watered angle and the dry angle make a full turn: 360° − 150° = 210°. (30° comes from 180° − 150°.)", rnd))
    its.append(dq("A wind turbine has 3 blades spaced equally around the centre. What is the angle between two blades next to each other?",
                  120, [60, 90, 180],
                  "The 3 equal angles go all the way around: 360° ÷ 3 = 120°. (60° comes from 180° ÷ 3.)", rnd))
    its.append(dq("How many degrees does the minute hand turn from 7:15 a.m. to 7:45 a.m.?", 180, [30, 90, 360],
                  "30 minutes is half an hour, so half a turn: 360° ÷ 2 = 180°, a straight angle.", rnd))
    n, he, his = P.next()
    its.append(dq("In coding class, %s’s robot faces north and turns 90° clockwise three times. "
                  "What counterclockwise turn would get it to the same direction?" % n, 90, [270, 180, 360],
                  "3 × 90° = 270° clockwise. Clockwise and counterclockwise turns that end in the same place add up to 360°: "
                  "360° − 270° = 90° counterclockwise.", rnd))
    n, he, his = P.next()
    its.append(dq("%s writes code for a sprite that turns left (counterclockwise) 60°. What right (clockwise) turn would end in the same direction?"
                  % n, 300, [60, 120, 240],
                  "The two turns add up to 360°: 360° − 60° = 300° clockwise. (120° comes from 180° − 60°.)", rnd))
    its.append(name_q("At the skatepark, a skateboarder does a “180”: the board turns 180°. What angle is that?",
                      "straight", ["reflex", "right", "obtuse"],
                      "180° is half of a full turn (360°): a straight angle. The skateboarder ends up facing the other way.", rnd))
    n, he, his = P.next()
    its.append(dq("%s spins one and a half full turns on the ice. How many degrees is that?" % n, 540, [360, 450, 180],
                  "One full turn is 360°, and half a turn is 180°. 360° + 180° = 540°. (450° is 360° + 90°, a turn and a quarter.)", rnd))
    its.append(mcq("A ship sails east. It turns 45° counterclockwise. Which way is it sailing now?", "northeast",
                   ["southeast", "north", "northwest"],
                   "Counterclockwise from east turns toward north. 45° is half of a right angle, so the ship points halfway between "
                   "east and north: northeast. (Southeast would be 45° clockwise.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in real life", "items": its}


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
    turns = turn_fig(0, 70, "70°", "290°", label=TURN)
    return (
        "<h2>Angle names</h2>"
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
        "<h2>Read a protractor</h2>"
        "<p>1. Estimate first: acute or obtuse? 2. Put the centre of the protractor on the vertex. 3. Line up one arm with <b>0</b>. "
        "4. Read the scale that <b>starts at 0 on that arm</b>. 5. Check the reading against your estimate.</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom arm is on 0 of the inner (green) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same place, but the angle is acute, so 130° cannot be right. "
        "The small marks go up in 5s.</figcaption></figure>" +
        "<h2>Reflex angles</h2>"
        "<p>A protractor only goes to 180°. To measure a reflex angle, measure the angle on the other side of the arms, "
        "then subtract from 360°.</p>" +
        ex("Measure a reflex angle", "The gap on the other side of a reflex angle measures 130°. Find the reflex angle.",
           "The two angles make a full turn: 360° − 130° = 230°.", "230°") +
        ex("Construct a reflex angle", "Construct an angle of 250°.",
           "360° − 250° = 110°. Construct 110° with the protractor, then mark the angle around the outside.",
           "the outside of a 110° angle") +
        "<h2>Clockwise and counterclockwise</h2>"
        "<p>From one arm you can turn to the other arm two ways: <b>clockwise</b> (the way clock hands move) or "
        "<b>counterclockwise</b> (the other way). Together the two turns make a full turn, so they <b>add up to 360°</b>.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>Counterclockwise 70° (black arrow) and clockwise 290° (red arrow): 70° + 290° = 360°.</figcaption></figure>" +
        ex("Find the other turn", "A robot turns 120° counterclockwise. What clockwise turn ends in the same direction?",
           "The two turns add up to 360°: 360° − 120° = 240°.", "240° clockwise") +
        "<p>On a protractor, the inner scale counts counterclockwise from 0 on the right, and the outer scale counts clockwise "
        "from 0 on the left.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (140° for a 40° angle)", "Read the scale that starts at 0 on your arm, then check your estimate"],
            ["Calling 190° obtuse", "Obtuse is between 90° and 180°. More than 180° is reflex"],
            ["Subtracting from 180° to find a reflex angle", "A reflex angle and the angle on the other side add up to 360°"],
            ["Thinking clockwise and counterclockwise angles add up to 180°", "Between the same two arms they make a full turn: 360°"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about angles in the Ontario math curriculum?",
     "a": "They use a protractor to measure and construct angles up to 360°, including reflex angles, and learn that the clockwise and counterclockwise angles between the same two arms add up to 360°."},
    {"q": "How do you measure a reflex angle with a protractor?",
     "a": "A protractor only goes to 180°, so measure the angle on the other side of the arms and subtract it from 360°. For example, if the other side is 70°, the reflex angle is 290°."},
    {"q": "Why do protractors have two scales?",
     "a": "So you can measure from an arm on either side: the inner scale counts counterclockwise from 0 on the right, and the outer scale counts clockwise from 0 on the left. Always read the scale that starts at 0 on your arm."},
    {"q": "Are angles on the Grade 6 EQAO math assessment?",
     "a": "Yes, spatial sense, including angles, is part of the Grade 6 Ontario math curriculum that EQAO assesses. Practise estimating first, reading the correct protractor scale and finding reflex angles."},
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
    rnd = random.Random(36813)
    P = People(rnd)
    sets = [set_names(rnd, P), set_protractor(rnd, P), set_reflex(rnd, P), set_turns(rnd, P), set_real(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "measuring-angles", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Angles: Protractors, Reflex Angles, Clockwise and Counterclockwise",
        "seo_title": "Grade 6 Measuring Angles Worksheets: Protractor and Reflex Angles (Free, Answer Key)",
        "short_title": "Measuring angles",
        "domain": "Spatial Sense",
        "standard_code": "Grade 6: Spatial Sense, E2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use a protractor to measure and construct angles up to 360°, and state the relationship between angles "
                         "that are measured clockwise and those that are measured counterclockwise",
        "meta_desc": "Free Grade 6 math worksheets on measuring angles for the Ontario curriculum: name acute, right, obtuse, "
                     "straight and reflex angles, read both protractor scales, find reflex angles and see why clockwise and "
                     "counterclockwise angles add up to 360°. 100 questions with an answer key, good EQAO practice.",
        "key_big": "The clockwise and counterclockwise angles between the same two arms add up to 360°.",
        "key_sub": "Read the protractor scale that starts at 0 on your arm, then check your estimate: acute is less than 90°, "
                   "obtuse is between 90° and 180°, reflex is between 180° and 360°. For a reflex angle, measure the other side "
                   "and subtract from 360°.",
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
