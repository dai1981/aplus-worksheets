# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Angles (MOE 2021 Primary Mathematics Syllabus, Standard – Geometry)
  python3 tools/gen_sg_maths_p4_angles.py
Naming angles (∠ABC with the vertex in the middle, ∠a), acute / right / obtuse, reading a protractor
(inner and outer scales), turns and the clock face, and adding or subtracting two marked angles.
Every angle is drawn exactly at its size (trig, 0° = pointing right, anticlockwise, SVG y goes down);
every marked angle is measured back from the drawing and checked against its value.
Labels are checked so that they do not touch a line, an arc or another label.
Protractor: inner scale has 0 on the right, outer scale has 0 on the left; marks every 5°, numbers every 10°.
Singapore style: British spelling, anticlockwise, Singapore names. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
LINE = "#1f4e79"
FILL = "#cfe0f1"
PFILL = "#eef4fa"
BLUE = "#2f6fb5"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


def D(v):
    """Angle in degrees as text: 65°."""
    assert abs(v - round(v)) < 1e-9 and 0 < v < 1000
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

    def line(self, p, q, col=LINE, sw=3):
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

def clock_svg(h, label=None):
    """Analogue clock at h o'clock with the smaller angle between the hands marked. Square picture."""
    c = (60.0, 60.0)
    R = 55
    s = ["<circle cx='60' cy='60' r='%d' fill='#ffffff' stroke='%s' stroke-width='3'/>" % (R, LINE)]
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
    arc = [pol(c, 11, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in arc), RED))
    hh, mh = pol(c, 16, hd), pol(c, 23, 90)
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='60' cy='60' r='4' fill='%s'/>" % INK)
    return svg_wrap(120, 120, "".join(s), label or "clock showing %d o’clock" % h)


PFILL = "#eef6f0"

class PPic:
    """Collects strokes (as sampled points, for collision checks and the bounding box) and labels (as boxes)."""

    def __init__(self):
        self.el = []          # (z, svg) z: 0 back, 1 strokes, 2 labels
        self.pts = []         # sampled points of every stroke
        self.boxes = []       # (x0, y0, x1, y1) of every label
        self.soft = []        # points that labels may cover (rays across a protractor scale)

    def line(self, p, q, col=LINE, sw=3, soft=False, cap_="round", dash=None):
        self.el.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='%s'%s/>"
                        % (p[0], p[1], q[0], q[1], col, sw, cap_, " stroke-dasharray='%s'" % dash if dash else "")))
        n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 2))
        pts = [(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)]
        (self.soft if soft else self.pts).extend(pts)

    def arc(self, V, r, a, b, col=LINE, sw=2.2, fill=None, z=1):
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

    def ray(self, V, deg, L, col=LINE, sw=3, soft=False):
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
                 % (R, R, R, -R, -R, R, PFILL, LINE)))
    P.pts += [pol(V, R, t) for t in range(0, 181)] + [(x, 14) for x in range(-R, R + 1, 2)]
    P.line((-R, 0), (R, 0), LINE, 1.6)
    for t in range(0, 181, 5):
        L = 11 if t % 10 == 0 else 6
        P.line(pol(V, R - L, t), pol(V, R, t), INK, 1.8 if t % 10 == 0 else 1.2, cap_="butt")
    # center mark
    P.line((0, -8), (0, 8), INK, 1.6)
    # labels: outer scale (0 at the left) and inner scale (0 at the right), turned like on a real protractor
    for t in range(0, 181, 10):
        for rr, val, col in [(R - PO, 180 - t, INK), (R - PI, t, BLUE)]:
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

def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

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



# ------------------------------------------------------------ Primary 4 figures
O = (0.0, 0.0)


def tri_pts(a, b, base=150, rot=0):
    """Triangle with angle a at the left end of the base, b at the right end, apex above."""
    c = 180 - a - b
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    pts = [O, (float(base), 0.0), pol(O, side, a)]
    return rot_all(pts, rot) if rot else pts


def I(ch):
    """Small letter angle name in HTML: ∠a."""
    return "∠<i>%s</i>" % ch


def put(P, p, d, nm, r0):
    """Point name just beyond p in direction d, as close as it fits without touching anything."""
    for r in range(r0, 34):
        c = pol(p, r, d)
        if P.clear(P.box_of(c[0], c[1], nm, 16)):
            P.label(c[0], c[1], nm)
            return
    raise AssertionError("no room for point name " + nm)


def named_svg(rays, vname, marks, label="angle with named points", L=88):
    """Rays from the vertex O. rays: [(direction, point name)]. vname: name of the vertex.
    marks: [(from_dir, to_dir, value, text, kind)] measured anticlockwise from from_dir to to_dir."""
    P = Pic()
    for d, nm in rays:
        P.line(O, pol(O, L, d))
    for a, b, val, t, kd in marks:
        P.mark(O, pol(O, L, a), pol(O, L, b), val, t, kind=kd, ccw=True)
    P.dot(O)
    for d, nm in rays:
        P.dot(pol(O, L, d), 3)
    for d, nm in rays:
        put(P, pol(O, L, d), d, nm, 12)
    sx = sum(math.cos(math.radians(d)) for d, n in rays)
    sy = sum(math.sin(math.radians(d)) for d, n in rays)
    vd = (math.degrees(math.atan2(sy, sx)) + 180) % 360 if math.hypot(sx, sy) > 0.2 else 270
    put(P, O, vd, vname, 12)
    return P.svg(label)


def tri_named(a, b, names, marks, rot=0, base=150, label="triangle with named corners"):
    """Triangle with angle a at the left end of the base and b at the right end.
    names: 3 corner letters (left, right, top). marks: {corner index: text or ''}."""
    pts = tri_pts(a, b, base, rot)
    A = poly_angles(pts)
    P = Pic()
    P.poly(pts)
    for i, t in marks.items():
        P.mark(pts[i], pts[i - 1], pts[(i + 1) % 3], A[i], t or None, inside=pts)
    g = (sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3)
    for i, nm in enumerate(names):
        put(P, pts[i], ang(g, pts[i]), nm, 11)
    return P.svg(label), A


def pair_svg(a1, L1, a2, L2, label="two angles to compare"):
    """Two angles side by side, captioned ∠p and ∠q."""
    s1 = angle_fig(a1, 0, "angle", L=L1)
    s2 = angle_fig(a2, 0, "angle", L=L2)
    return strip_svg([s1, s2], ["∠<tspan font-style='italic'>p</tspan>", "∠<tspan font-style='italic'>q</tspan>"],
                     label, cw=150, fs=18)


def model_svg(rows, total, label="bar model", width=230):
    """Bar model drawn to scale. rows: [(name, [(degrees, text)])]; total: text for the bracket
    (above a single bar, or to the right of two bars)."""
    mx = max(sum(s[0] for s in segs) for n, segs in rows)
    k = float(width) / mx
    fs = 15
    plain = [re.sub(r"<[^>]+>", "", n) for n, s in rows]
    x0 = max(tw(p, 16) for p in plain) + 22 if any(plain) else 0
    out = []
    top = 26 if len(rows) == 1 else 4
    rh, gap = 32, 14
    for r, (name, segs) in enumerate(rows):
        y = top + r * (rh + gap)
        if name:
            out.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                       % (x0 - 10, y + rh / 2 + 5.8, INK, name))
        x = x0
        for deg, t in segs:
            w = deg * k
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, y, w, rh, FILL, LINE))
            if t:
                assert tw(t, fs) + 6 <= w, ("segment too narrow", t, w)
                out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                           % (x + w / 2, y + rh / 2 + fs * 0.36, fs, RED if t == "?" else INK, t))
            x += w
    if len(rows) == 1:
        w = sum(s[0] for s in rows[0][1]) * k
        out.append("<polyline points='%.1f,22 %.1f,14 %.1f,14 %.1f,22' fill='none' stroke='%s' stroke-width='1.8'/>"
                   % (x0, x0, x0 + w, x0 + w, INK))
        out.append("<rect x='%.1f' y='2' width='%.1f' height='18' fill='#ffffff'/>" % (x0 + w / 2 - tw(total, 16) / 2 - 4, tw(total, 16) + 8))
        out.append("<text x='%.1f' y='17' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                   % (x0 + w / 2, RED if total == "?" else INK, total))
        W, H = x0 + w + 6, top + rh + 6
    else:
        xr = x0 + mx * k + 10
        y1, y2 = top, top + len(rows) * rh + (len(rows) - 1) * gap
        out.append("<polyline points='%.1f,%d %.1f,%d %.1f,%d %.1f,%d' fill='none' stroke='%s' stroke-width='1.8'/>"
                   % (xr - 6, y1, xr, y1, xr, y2, xr - 6, y2, INK))
        out.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='start'>%s</text>"
                   % (xr + 6, (y1 + y2) / 2 + 5.8, RED if total == "?" else INK, total))
        W, H = xr + 6 + tw(total, 16) + 6, y2 + 6
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(out), label)


# ------------------------------------------------------------ set 1: naming angles
def name_wrong(e1, v, e2):
    """Wrong names for ∠e1 v e2: vertex not in the middle (two ways) and only two letters."""
    return ["∠%s%s%s" % (v, e1, e2), "∠%s%s%s" % (e1, e2, v), "∠%s%s" % (e1, v)]


def set_names(rnd, P):
    its = []
    q = "Name the marked angle."
    for (e1, d1), v, (e2, d2) in [(("A", 0), "B", ("C", 55)), (("P", 20), "Q", ("R", 140)), (("X", 200), "Y", ("Z", 290))]:
        s = (d2 - d1) % 360
        svg = named_svg([(d1, e1), (d2, e2)], v, [(d1, d2, s, None, "right" if s == 90 else "arc")])
        its.append(mcq(fig(svg) + q, "∠%s%s%s" % (e1, v, e2), name_wrong(e1, v, e2),
                       "The vertex is %s, where the two arms meet. Put the vertex letter in the middle: ∠%s%s%s "
                       "(∠%s%s%s is also correct). An angle name needs three letters." % (v, e1, v, e2, e2, v, e1), rnd))
    # three rays from one vertex
    for rays, v, mk, ans, wrong in [
        ([(0, "A"), (40, "C"), (110, "D")], "B", (0, 40), "∠ABC", ["∠ABD", "∠CBD", "∠BAC"]),
        ([(10, "P"), (75, "S"), (160, "R")], "Q", (75, 160), "∠SQR", ["∠PQS", "∠PQR", "∠QSR"]),
        ([(-20, "K"), (50, "M"), (125, "N")], "L", (-20, 125), "∠KLN", ["∠KLM", "∠MLN", "∠LKN"]),
        ([(200, "E"), (260, "G"), (340, "H")], "F", (200, 260), "∠EFG", ["∠GFH", "∠EFH", "∠FEG"]),
    ]:
        s = (mk[1] - mk[0]) % 360
        svg = named_svg(rays, v, [(mk[0], mk[1], s, None, "arc")])
        e = ("Follow the arc. Its arms go to %s and %s, and the vertex is %s. So the angle is %s. "
             "With three arms at %s, a name like ∠%s alone would not say which angle you mean."
             % (ans[1], ans[3], v, ans, v, v))
        its.append(mcq(fig(svg) + q, ans, wrong, e, rnd))
    # triangles
    for a, b, names, i, ans, wrong in [
        (62, 48, "PQR", 2, "∠PRQ", ["∠PQR", "∠QPR", "∠PR"]),
        (40, 75, "DEF", 1, "∠DEF", ["∠EDF", "∠DFE", "∠DE"]),
    ]:
        svg, A = tri_named(a, b, names, {i: ""})
        v = names[i]
        o = [x for x in names if x != v]
        its.append(mcq(fig(svg) + "Name the marked angle in the triangle.", ans, wrong,
                       "The marked angle is at %s. Its arms are %s%s and %s%s, so its name is ∠%s%s%s, with %s in the middle."
                       % (v, v, o[0], v, o[1], o[0], v, o[1], v), rnd))
    # small letters
    rays = [(0, "A"), (50, "C"), (125, "D")]
    sv = named_svg(rays, "B", [(0, 50, 50, "a", "arc"), (50, 125, 75, "b", "arc")], label="two angles a and b")
    its.append(mcq(fig(sv) + "Which angle is " + I("a") + "?", "∠ABC", ["∠CBD", "∠ABD", "∠BAC"],
                   I("a") + " is between the arms BA and BC, so " + I("a") + " = ∠ABC. "
                   "∠CBD is " + I("b") + ", and ∠ABD is the whole angle, " + I("a") + " and " + I("b") + " together.", rnd))
    rays = [(10, "P"), (95, "R"), (150, "S")]
    sv = named_svg(rays, "Q", [(10, 95, 85, "x", "arc"), (95, 150, 55, "y", "arc")], label="two angles x and y")
    its.append(mcq(fig(sv) + "Which is another name for " + I("y") + "?", "∠RQS", ["∠PQR", "∠PQS", "∠QRS"],
                   I("y") + " is between the arms QR and QS. The vertex Q goes in the middle: ∠RQS. "
                   "∠PQR is " + I("x") + ", and ∠PQS is " + I("x") + " and " + I("y") + " together.", rnd))
    rays = [(-10, "X"), (45, "W"), (115, "V")]
    sv = named_svg(rays, "O", [(-10, 45, 55, "m", "arc"), (45, 115, 70, "n", "arc")], label="two angles m and n")
    its.append(mcq(fig(sv) + "∠XOV is made up of which angles?", I("m") + " and " + I("n"),
                   [I("m") + " only", I("n") + " only", "∠XOW and ∠XOV"],
                   "∠XOV goes from arm OX all the way to arm OV. It is " + I("m") + " (∠XOW) and " + I("n") + " (∠WOV) put together.", rnd))
    svg, A = tri_named(70, 50, "XZY", {0: "a", 1: "c", 2: "b"}, label="triangle with angles a, b and c")
    its.append(mcq(fig(svg) + "In triangle XYZ, which angle is ∠XYZ?", I("b"), [I("a"), I("c"), "It is not marked"],
                   "In ∠XYZ the middle letter is Y, so the vertex is Y. The angle at Y is marked " + I("b") + ".", rnd))
    sv = named_svg([(0, "A"), (90, "C"), (140, "D")], "B", [(0, 90, 90, None, "right")], label="right angle ABC")
    its.append(mcq(fig(sv) + "Which angle is a right angle?", "∠ABC", ["∠CBD", "∠ABD", "∠BCD"],
                   "The small square shows a right angle. It sits between the arms BA and BC, so ∠ABC = 90°. "
                   "∠ABD is bigger than a right angle and ∠CBD is smaller.", rnd))
    its.append(mcq("In ∠PQR, which point is the vertex?", "Q", ["P", "R", "the line PR"],
                   "The middle letter of an angle name is always the vertex. In ∠PQR it is Q.", rnd))
    its.append(mcq("Which angle has its vertex at M?", "∠LMN", ["∠MLN", "∠LNM", "∠MKL"],
                   "The vertex is the middle letter. Only ∠LMN has M in the middle.", rnd))
    its.append(mcq("What are the two arms of ∠DEF?", "ED and EF", ["DE and DF", "FD and FE", "DF and EF"],
                   "The vertex is E, the middle letter. Both arms start at E: one goes to D and one goes to F.", rnd))
    its.append(mcq("Which two names are for the same angle?", "∠XYZ and ∠ZYX",
                   ["∠XYZ and ∠YXZ", "∠XYZ and ∠XZY", "∠XYZ and ∠YZX"],
                   "Both names have Y in the middle, so both have the vertex at Y and the arms YX and YZ. "
                   "You may read the angle from either arm.", rnd))
    n, he, his = P.next()
    its.append(mcq("The vertex of an angle is B and its arms go to A and C. %s names it ∠BAC. What is wrong?" % n,
                   "B must be the middle letter",
                   ["The letters must be in ABC order", "Angle names use small letters", "Nothing is wrong"],
                   "∠BAC has A in the middle, so it means the angle at A. The angle at B is ∠ABC (or ∠CBA).", rnd))
    its.append(mcq("∠PQS is made up of ∠PQR and ∠RQS. Which of the three angles is the largest?", "∠PQS",
                   ["∠PQR", "∠RQS", "They are all equal"],
                   "∠PQS is the whole angle. ∠PQR and ∠RQS are its two parts, so each part is smaller than ∠PQS.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name angles: ∠ABC and ∠a", "items": its}


# ------------------------------------------------------------ set 2: acute, right, obtuse and estimates
KIND = {"acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle (180°)"}
KIND_E = {
    "acute": "An acute angle is smaller than a right angle: less than 90°.",
    "right": "A right angle is exactly 90°, a quarter turn. The small square shows it.",
    "obtuse": "An obtuse angle is bigger than a right angle but smaller than a straight line: between 90° and 180°.",
    "straight": "The two arms make a straight line: 180°, half a turn.",
}


def kind(d):
    return "acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight"


def set_estimate(rnd, P):
    its = []
    q = "Is the marked angle acute, right or obtuse?"
    for d, rot in [(35, 15), (125, 0), (90, 30), (160, 10), (70, 100), (100, 160), (55, 200), (180, 0)]:
        k = kind(d)
        e = KIND_E[k]
        if k in ("acute", "obtuse"):
            e += " This angle is %s." % D(d)
        if rot >= 90 or k == "right":
            e += " Turning an angle does not change its size."
        q2 = q if d != 180 else "What kind of angle is marked?"
        its.append(mcq(fig(angle_fig(d, rot)) + q2, KIND[k], [KIND[w] for w in KIND if w != k], e, rnd))
    q = "Which is the best estimate for the marked angle?"
    for d, rot, best, wrong in [
        (28, 0, 30, [150, 60, 90]),
        (62, 20, 60, [120, 30, 90]),
        (118, 5, 120, [60, 90, 170]),
        (147, 10, 150, [30, 100, 180]),
        (43, 70, 45, [135, 90, 15]),
        (172, 0, 170, [10, 120, 90]),
    ]:
        if d < 90:
            e = "The angle is smaller than a right angle (90°), so it is acute. About %s fits. (It is %s.)" % (D(best), D(d))
        else:
            e = ("The angle is bigger than a right angle (90°) but smaller than a straight line (180°), so it is obtuse. "
                 "About %s fits. (It is %s.)" % (D(best), D(d)))
        if (180 - best) in wrong:
            e += " %s is the number on the other scale of a protractor." % D(180 - best)
        its.append(mcq(fig(angle_fig(d, rot)) + q, "about " + D(best), ["about " + D(w) for w in wrong], e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(150, 0, 26), (80, 0, 56), (45, 0, 60), (110, 0, 42)], lab)) +
                        "Which angle is the largest?", "A",
                        "The size of an angle is the amount of turn, not the length of the arms. "
                        "A opens the widest (about 150°), so it is the largest, even though its arms are the shortest."))
    its.append(letter_q(fig(abcd_svg([(60, 0), (85, 0), (130, 0), (30, 0)], lab)) + "Which angle is obtuse?", "C",
                        "Obtuse means more than a right angle (90°) and less than 180°. Only C opens wider than a right angle. "
                        "B is close to a right angle, but a little smaller, so it is acute."))
    its.append(letter_q(fig(abcd_svg([(120, 0), (90, 0), (20, 0), (160, 0)], lab)) + "Which angle is 90°?", "B",
                        "The small square in B shows a right angle, 90°. A and D are obtuse and C is acute."))
    its.append(mcq(fig(pair_svg(40, 70, 70, 36)) + "Which angle is bigger?", "∠<i>q</i>",
                   ["∠<i>p</i>", "They are equal", "You cannot tell"],
                   "Look at how wide the arms open, not how long they are. " + I("q") + " opens wider (70°) than " +
                   I("p") + " (40°). Longer arms do not make a bigger angle.", rnd))
    its.append(mcq("An angle is a little smaller than a right angle. Which could it be?", "80°", ["100°", "180°", "8°"],
                   "A right angle is 90°. A little smaller than 90° is about 80°. 100° is a little bigger, and 8° is very small.", rnd))
    its.append(mcq("Which of these is an obtuse angle?", "135°", ["45°", "90°", "85°"],
                   "An obtuse angle is between 90° and 180°. Only 135° is. 90° is a right angle; 45° and 85° are acute.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Acute, right or obtuse? Estimate angles", "items": its}


# ------------------------------------------------------------ set 3: protractor
def read_cands(v):
    c = [D(180 - v)]
    if v % 10 == 5:
        c += [D(v - 5), D(v + 5), D(v + 10)]       # read the number before or after the 5° mark
    else:
        c += [D(v + 10), D(v - 10), D(v + 5)]
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
            e += " The marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " The outer scale says %d there, but it starts from the other side. The angle is %s, so %s makes sense." % (
            180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([0, v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for v in (30, 55, 120, 145, 70, 100):
        e = ("The bottom arm is on 0 on the left, so read the <b>outer</b> scale, which starts at 0 on the left. "
             "The other arm crosses it at %d." % v)
        if v % 10 == 5:
            e += " The marks go up in 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " (The inner scale says %d there.) The angle is %s, so %s makes sense." % (180 - v, size_word(v), D(v))
        its.append(mcq(fig(protractor_svg([180, 180 - v], "protractor measuring an angle")) + q, D(v), read_cands(v), e, rnd))
    for a, b in ((20, 95), (40, 150)):
        v = b - a
        its.append(mcq(fig(protractor_svg([a, b], "protractor measuring an angle with neither arm on 0")) +
                       "Neither arm is on 0. What is the size of the angle?", D(v), [D(b), D(180 - b), D(a + b)],
                       "On the inner scale one arm is at %d and the other is at %d. The angle is the difference: %d° − %d° = %d°."
                       % (a, b, b, a, v), rnd))
    its.append(mcq("Where do you put the centre of the protractor when you measure ∠ABC?", "on point B",
                   ["on point A", "on point C", "in the middle of the line AC"],
                   "The centre goes on the vertex, where the two arms meet. In ∠ABC the vertex is the middle letter, B. "
                   "Then line up one arm with 0.", rnd))
    its.append(mcq("One arm of an angle is on 0 of the outer scale. Which scale should you read?", "the outer scale",
                   ["the inner scale", "the scale with the bigger number", "the scale with the smaller number"],
                   "Read the scale that starts at 0 on your arm. Here that is the outer scale.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s measures an angle that is clearly smaller than a right angle. The other arm crosses the protractor "
                   "at 35 and 145. What is the angle?" % n, D(35), [D(145), D(110), D(180)],
                   "An angle smaller than a right angle is less than 90°, so it is 35°. 145 is on the other scale.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s wants to draw an angle of 65°. %s puts %s line on 0 of the inner scale. Where should %s make a dot?"
                   % (n, cap(he), his, he), "at 65 on the inner scale",
                   ["at 65 on the outer scale", "at 60 on the inner scale", "at 115 on the inner scale"],
                   "Use the scale that starts at 0 on your line: the inner scale. Count up to 65 (the mark between 60 and 70), "
                   "make a dot, then join it to the vertex. Using 65 on the outer scale would give 115°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s measures an angle that is clearly obtuse and writes 70°. What is the angle?" % n,
                   D(110), [D(70), D(20), D(160)],
                   "An obtuse angle is more than 90°, so 70° cannot be right. %s read the wrong scale. "
                   "The other scale shows 180 − 70 = 110 at the same place, so the angle is 110°." % n, rnd))
    its.append(mcq("On the inner scale, one arm of an angle is at 20 and the other arm is at 75. What is the angle?",
                   D(55), [D(75), D(95), D(105)],
                   "Neither arm is on 0, so find the difference: 75° − 20° = 55°. "
                   "(95° comes from adding, and 105° is what the outer scale shows for 75.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a protractor: inner and outer scales", "items": its}


# ------------------------------------------------------------ set 4: turns and the clock face
CLOCK_E = "The 12 numbers on a clock split a whole turn (360°) into 12 equal spaces: 360° ÷ 12 = 30° each."


def set_turns(rnd, P):
    its = []
    q = "What is the smaller angle between the two hands at %d o’clock?"
    for h, v, wrong, note in [
        (3, 90, [30, 180, 45], "At 3 o’clock the hands make a right angle (a quarter turn)."),
        (6, 180, [60, 90, 360], "At 6 o’clock the hands make a straight line: half a turn."),
        (2, 60, [20, 30, 120], ""),
        (4, 120, [40, 90, 240], ""),
        (1, 30, [10, 60, 90], ""),
        (5, 150, [50, 120, 30], ""),
        (10, 60, [300, 20, 120], "Count the short way, from 10 to 12: 2 spaces. (300° is the long way round.)"),
    ]:
        sp = min(h, 12 - h)
        e = CLOCK_E + " The hands are %d space%s apart: %d × 30° = %d°." % (sp, "" if sp == 1 else "s", sp, v)
        if note:
            e += " " + note
        its.append(dq(fig(clock_svg(h)) + q % h, v, wrong, e, rnd))
    its.append(dq("How many degrees are in a quarter turn?", 90, [25, 180, 45],
                  "A whole turn is 360°. A quarter of it is 360° ÷ 4 = 90°, a right angle.", rnd))
    its.append(dq("How many degrees are in a half turn?", 180, [90, 360, 50],
                  "A half turn is half of 360°: 360° ÷ 2 = 180°. The arms make a straight line.", rnd))
    its.append(dq("How many degrees are in a " + FR(3, 4) + "-turn?", 270, [75, 180, 300],
                  "A quarter turn is 90°, so three quarter turns are 3 × 90° = 270°. "
                  "(75° is three quarters of 100, but a whole turn is 360°.)", rnd))
    its.append(mcq("What fraction of a whole turn is 90°?", FR(1, 4), [FR(1, 2), FR(3, 4), FR(1, 9)],
                   "90° × 4 = 360°, so 90° is " + FR(1, 4) + " of a whole turn.", rnd))
    its.append(mcq("How many right angles make a whole turn?", "4", ["2", "3", "360"],
                   "4 × 90° = 360°, so 4 right angles make a whole turn. 2 right angles make a half turn.", rnd))
    its.append(mcq("How many right angles make a half turn?", "2", ["1", "4", "180"],
                   "A half turn is 180°, and 2 × 90° = 180°.", rnd))
    its.append(dq("The minute hand turns clockwise from 12 to 3. How many degrees does it turn?", 90, [3, 30, 180],
                  "From 12 to 3 is a quarter of the clock face: a quarter turn, 90°.", rnd))
    its.append(mcq("The minute hand turns for 30 minutes. How much of a turn is that?", "a half turn",
                   ["a quarter turn", "a " + FR(3, 4) + "-turn", "a whole turn"],
                   "The minute hand makes a whole turn in 60 minutes. 30 minutes is half of 60 minutes, so it is a half turn (180°).", rnd))
    its.append(dq("How many degrees does the minute hand turn in 45 minutes?", 270, [45, 90, 180],
                  "15 minutes is a quarter turn (90°). 45 minutes is 3 quarter turns: 3 × 90° = 270°.", rnd))
    its.append(mcq("The minute hand turns through 180°. How many minutes have passed?", "30 minutes",
                   ["15 minutes", "180 minutes", "45 minutes"],
                   "180° is a half turn. The minute hand makes a half turn in half an hour: 30 minutes.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces north. %s makes a quarter turn clockwise. Which way does %s face now?" % (n, cap(he), he),
                   "east", ["west", "south", "north"],
                   "Clockwise from north, a quarter turn (90°) takes you to east. (Anticlockwise would be west.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces south at East Coast Park. %s turns 180°. Which way does %s face now?" % (n, cap(he), he),
                   "north", ["east", "west", "south"],
                   "180° is a half turn. After a half turn you face the opposite way: south becomes north.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces east. %s turns 90° anticlockwise. Which way does %s face now?" % (n, cap(he), he),
                   "north", ["south", "west", "east"],
                   "Anticlockwise from east, a quarter turn takes you to north. (Clockwise would be south.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Turns and angles on a clock face", "items": its}


# ------------------------------------------------------------ set 5: two marked angles, word problems
def set_problems(rnd, P):
    its = []
    for rays, v, a, b, nm, wrong_extra in [
        ([(0, "A"), (35, "C"), (85, "D")], "B", 35, 50, ("ABC", "CBD", "ABD"), None),
        ([(15, "P"), (80, "R"), (160, "S")], "Q", 65, 80, ("PQR", "RQS", "PQS"), None),
        ([(-10, "K"), (30, "M"), (110, "N")], "L", 40, 80, ("KLM", "MLN", "KLN"), None),
        ([(190, "E"), (245, "G"), (290, "H")], "F", 55, 45, ("EFG", "GFH", "EFH"), None),
    ]:
        d0, d1, d2 = rays[0][0], rays[1][0], rays[2][0]
        assert (d1 - d0) % 360 == a and (d2 - d1) % 360 == b
        sv = named_svg(rays, v, [(d0, d1, a, D(a), "arc"), (d1, d2, b, D(b), "arc")], label="two marked angles")
        s = a + b
        its.append(dq(fig(sv) + "Find ∠%s." % nm[2], s, [abs(a - b), 180 - s, a, b],
                      "∠%s is made up of ∠%s and ∠%s. Add them: %d° + %d° = %d°." % (nm[2], nm[0], nm[1], a, b, s), rnd))
    for rays, v, a, whole, nm in [
        ([(0, "A"), (45, "C"), (110, "D")], "B", 45, 110, ("ABC", "CBD", "ABD")),
        ([(20, "X"), (90, "Z"), (155, "W")], "Y", 70, 135, ("XYZ", "ZYW", "XYW")),
        ([(-25, "P"), (40, "R"), (95, "S")], "Q", 65, 120, ("PQR", "RQS", "PQS")),
        ([(160, "D"), (190, "F"), (285, "G")], "E", 30, 125, ("DEF", "FEG", "DEG")),
    ]:
        d0, d1, d2 = rays[0][0], rays[1][0], rays[2][0]
        b = whole - a
        assert (d1 - d0) % 360 == a and (d2 - d1) % 360 == b
        sv = named_svg(rays, v, [(d0, d1, a, D(a), "arc"), (d1, d2, b, "?", "arc")], label="one marked angle and an unknown angle")
        its.append(dq(fig(sv) + "∠%s = %s. Find the unknown angle ∠%s." % (nm[2], D(whole), nm[1]), b,
                      [whole + a, a, 180 - b, whole],
                      "The whole angle ∠%s is %s. Take away the part you know: %d° − %d° = %d°. "
                      "Check: %d° + %d° = %d°." % (nm[2], D(whole), whole, a, b, a, b, whole), rnd))
    for rays, v, a, nm in [
        ([(0, "P"), (35, "S"), (90, "R")], "Q", 35, ("PQS", "SQR", "PQR")),
        ([(110, "A"), (170, "D"), (200, "C")], "B", 60, ("ABD", "DBC", "ABC")),
    ]:
        d0, d1, d2 = rays[0][0], rays[1][0], rays[2][0]
        b = 90 - a
        assert (d1 - d0) % 360 == a and (d2 - d1) % 360 == b
        sv = named_svg(rays, v, [(d0, d1, a, D(a), "arc"), (d1, d2, b, "?", "arc")], label="a right angle split into two angles")
        its.append(dq(fig(sv) + "∠%s is a right angle. Find ∠%s." % (nm[2], nm[1]), b, [180 - a, 90 + a, a],
                      "A right angle is 90°. ∠%s = 90° − %d° = %d°." % (nm[1], a, b), rnd))
    # bar models
    its.append(dq(fig(model_svg([("", [(40, "40°"), (75, "75°")])], "?")) +
                  "A door is open at 40°. Mr Tan pushes it open another 75°. How wide is the door open now?", 115,
                  [35, 75, 65],
                  "The model shows the two turns joined together. 40° + 75° = 115°.", rnd))
    its.append(dq(fig(model_svg([("", [(50, "50°"), (100, "?")])], "150°")) +
                  "Mdm Wong opens a paper fan to 150°. She first opened it to 50°. How many more degrees did she open it?", 100,
                  [200, 50, 150],
                  "The whole is 150° and one part is 50°. The other part is 150° − 50° = 100°.", rnd))
    its.append(dq(fig(model_svg([("∠<tspan font-style='italic'>p</tspan>", [(40, ""), (40, "")]),
                                 ("∠<tspan font-style='italic'>q</tspan>", [(40, "?")])], "120°")) +
                  "∠<i>p</i> and ∠<i>q</i> make 120° together. ∠<i>p</i> is twice as big as ∠<i>q</i>. Find ∠<i>q</i>.", 40,
                  [60, 80, 30],
                  "∠<i>p</i> is 2 units and ∠<i>q</i> is 1 unit, so 3 units = 120°. 1 unit = 120° ÷ 3 = 40°. "
                  "∠<i>q</i> = 40° (∠<i>p</i> = 80°). (60° comes from 120° ÷ 2.)", rnd))
    its.append(dq(fig(model_svg([("∠<tspan font-style='italic'>x</tspan>", [(35, ""), (20, "20°")]),
                                 ("∠<tspan font-style='italic'>y</tspan>", [(35, "?")])], "90°")) +
                  "∠<i>x</i> and ∠<i>y</i> make a right angle together. ∠<i>x</i> is 20° more than ∠<i>y</i>. Find ∠<i>y</i>.", 35,
                  [45, 55, 70],
                  "Take away the extra 20°: 90° − 20° = 70°. That is 2 equal units, so 1 unit = 70° ÷ 2 = 35°. "
                  "∠<i>y</i> = 35° (∠<i>x</i> = 55°). (45° comes from forgetting the extra 20°.)", rnd))
    n, he, his = P.next()
    its.append(dq("%s cuts a round cake for Children’s Day into 4 equal pieces from the centre. What angle does each piece make at the centre?" % n,
                  90, [45, 360, 180],
                  "The pieces go all the way round the centre: a whole turn, 360°. 360° ÷ 4 = 90°, a right angle. "
                  "(45° comes from using 180°, and 360° is the whole turn before dividing.)", rnd))
    n, he, his = P.next()
    its.append(dq("A robot at the Science Centre makes a quarter turn and then a half turn, both clockwise. "
                  "How many degrees does it turn altogether?", 270, [180, 360, 90],
                  "A quarter turn is 90° and a half turn is 180°. 90° + 180° = 270°, a " + FR(3, 4) + "-turn.", rnd))
    its.append(dq(fig(model_svg([("", [(70, "70°"), (55, "?")])], "125°")) +
                  "Two roads meet at an angle of 125°. A new footpath splits this angle into two parts. One part is 70°. "
                  "Find the other part.", 55, [195, 70, 65],
                  "The whole is 125° and one part is 70°. The other part is 125° − 70° = 55°. "
                  "(195° comes from adding instead of subtracting.)", rnd))
    n, he, his = P.next()
    its.append(dq("The blades of %s’s scissors are open at 25°. %s opens them 15° more. What is the angle between the blades now?"
                  % (n, cap(he)), 40, [10, 25, 15],
                  "%s opens the blades more, so add: 25° + 15° = 40°." % n, rnd))
    its.append(dq("The minute hand of a clock turns from 12 to 2, and then from 2 to 5. How many degrees does it turn altogether?",
                  150, [60, 90, 210],
                  "Each hour space is 30°. From 12 to 2 is 2 × 30° = 60°, and from 2 to 5 is 3 × 30° = 90°. "
                  "60° + 90° = 150°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures ∠ABC = 65° and ∠CBD = 40°. Together they make ∠ABD. Find ∠ABD." % n, 105,
                  [25, 75, 140],
                  "∠ABD is made up of ∠ABC and ∠CBD: 65° + 40° = 105°. (25° comes from subtracting.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angle problems: add and subtract marked angles", "items": its}


def FR(n, d):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, d)


# ------------------------------------------------------------ lesson
def body_html():
    names = named_svg([(0, "A"), (50, "C"), (125, "D")], "B", [(0, 50, 50, "a", "arc"), (50, 125, 75, "b", "arc")],
                      label="angles ABC and CBD at the vertex B")
    kinds = strip_svg([angle_fig(40, 0, L=55), angle_fig(90, 0, L=55), angle_fig(130, 0, L=55)],
                      ["acute", "right angle", "obtuse"], "acute, right and obtuse angles", cw=150)
    prot = protractor_svg([0, 50], "protractor measuring a 50 degree angle")
    clock = clock_svg(3, "clock at 3 o’clock showing a right angle")
    sumfig = named_svg([(0, "P"), (35, "R"), (95, "S")], "Q", [(0, 35, 35, "35°", "arc"), (35, 95, 60, "60°", "arc")],
                       label="angle PQS made of two angles")
    return (
        "<h2>Naming angles</h2>"
        "<p>An angle is made by two <b>arms</b> that meet at a point, the <b>vertex</b>. "
        "We name an angle with three letters, and the vertex is always the <b>middle</b> letter. "
        "We can also name an angle with one small letter, like ∠<i>a</i>.</p>"
        "<figure class='sn-fig'>" + names +
        "<figcaption>∠<i>a</i> = ∠ABC (or ∠CBA). ∠<i>b</i> = ∠CBD. The whole angle is ∠ABD. "
        "With three arms at B, “∠B” would not say which angle you mean.</figcaption></figure>"
        "<h2>Acute, right and obtuse</h2>"
        "<p>We measure angles in <b>degrees</b> (°). Compare an angle with a right angle (90°).</p>"
        "<figure class='sn-fig'>" + kinds +
        "<figcaption>Acute: less than 90°. Right angle: exactly 90°. Obtuse: more than 90° and less than 180°.</figcaption></figure>"
        "<p>The length of the arms does not change the size of an angle. Only the amount of turn matters.</p>"
        "<h2>Measure with a protractor</h2>"
        "<p>1. Put the centre of the protractor on the vertex. 2. Line up one arm with <b>0</b>. "
        "3. Read the scale that <b>starts at 0 on that arm</b>. 4. Check with your estimate: acute or obtuse?</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom arm is on 0 of the inner (blue) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same place, but the angle is acute, so 130° cannot be right.</figcaption></figure>" +
        ex("Draw ∠PQR = 65°", "Draw the line QR. Put the centre of the protractor on Q and the line QR on 0.",
           "Count along the scale that starts at 0 on QR up to 65 and make a dot P. Join Q to P.", "∠PQR = 65°") +
        "<h2>Turns and the clock face</h2>"
        "<figure class='sn-fig'>" + clock +
        "<figcaption>At 3 o’clock the hands make a quarter turn: 90°.</figcaption></figure>" +
        table(["Turn", "Degrees", "Right angles"], [
            [FR(1, 4) + "-turn", "90°", "1"],
            [FR(1, 2) + "-turn", "180°", "2"],
            [FR(3, 4) + "-turn", "270°", "3"],
            ["whole turn", "360°", "4"],
        ]) +
        "<p>Each hour space on a clock is 360° ÷ 12 = <b>30°</b>. At 2 o’clock the hands are 2 × 30° = 60° apart.</p>"
        "<h2>Adding and subtracting angles</h2>"
        "<figure class='sn-fig'>" + sumfig +
        "<figcaption>∠PQS is made up of ∠PQR and ∠RQS.</figcaption></figure>" +
        ex("Find the whole angle", "∠PQR = 35° and ∠RQS = 60°. Find ∠PQS.", "35° + 60° = 95°.", "∠PQS = 95°") +
        ex("Find a part", "∠PQS = 95° and ∠PQR = 35°. Find ∠RQS.", "95° − 35° = 60°. Check: 35° + 60° = 95°.", "∠RQS = 60°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (130° for a 50° angle)", "Read the scale that starts at 0 on your arm, then check your estimate"],
            ["Writing ∠BAC for the angle at B", "Put the vertex in the middle: ∠ABC"],
            ["Thinking longer arms make a bigger angle", "The size of an angle is the amount of turn, not the length of the arms"],
            ["Putting the protractor centre at the end of an arm", "Put the centre exactly on the vertex"],
        ])
    )


FAQ = [
    {"q": "What do P4 students learn about angles?",
     "a": "They name angles as ∠ABC or ∠a, tell acute, right and obtuse angles apart, measure and draw angles with a protractor, and link quarter, half and whole turns to 90°, 180° and 360°."},
    {"q": "How do you name an angle like ∠ABC?",
     "a": "Use three letters with the vertex in the middle: ∠ABC is the angle at B between the arms BA and BC. ∠CBA is the same angle."},
    {"q": "What is the most common mistake when using a protractor?",
     "a": "Reading the wrong scale, for example 130° instead of 50°. Read the scale that starts at 0 on one arm, and check that an acute angle gets a reading below 90°."},
    {"q": "Is this topic in the MOE syllabus for Primary 4?",
     "a": "Yes. Measuring and drawing angles in degrees and naming them with ∠ABC and ∠a are part of Geometry in the MOE 2021 Primary 4 syllabus. Angle facts such as angles on a straight line come in P5."},
]


def gen():
    rnd = random.Random(64813)
    P = People(rnd)
    sets = [set_names(rnd, P), set_estimate(rnd, P), set_protractor(rnd, P), set_turns(rnd, P), set_problems(rnd, P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "angles", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Angles: Naming, Measuring and Drawing Angles",
        "seo_title": "P4 Angles Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Angles",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 4: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Using notation such as ∠ABC and ∠a to name angles; measuring angles in degrees; drawing an angle of given size",
        "meta_desc": "Free P4 maths practice on angles: name ∠ABC, acute or obtuse, read a protractor, turns and clocks. "
                     "100 questions with answers.",
        "key_big": "In ∠ABC the vertex B is the middle letter, and you read the protractor scale that starts at 0.",
        "key_sub": "An acute angle that reads 50 on one scale and 130 on the other is 50°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(protractor|four angles labelled|bar model|two angles to compare)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
