# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Measuring angles
(Australian Curriculum v9.0, AC9M5M04)
  python3 tools/gen_au_maths_y5_angles.py
Name angles (acute, right, obtuse, straight, reflex, revolution), estimate, measure with a protractor
(inner and outer scales), construct angles, and relate angle sizes to names and everyday angles.
Australian English. HTML attributes use single quotes (no backslashes in the JSON).

Every angle is drawn exactly at its size (trig, 0° = pointing right, anticlockwise, SVG y goes down);
every marked angle is measured back from the drawing and checked against its value.
Labels are checked so that they do not touch a line, an arc or another label.
Protractor: inner scale has 0 on the right, outer scale has 0 on the left; marks every 5°, numbers every 10°.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


def D(v):
    """Angle in degrees as text: 65°, 1080° (Australian style: no separator in 4-digit numbers)."""
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


# ------------------------------------------------------------ angle names
NAMES = {"acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle",
         "reflex": "reflex angle", "revolution": "revolution"}
WRONG = {"acute": ["obtuse", "right", "reflex"], "right": ["acute", "obtuse", "straight"],
         "obtuse": ["acute", "reflex", "straight"], "straight": ["obtuse", "reflex", "revolution"],
         "reflex": ["obtuse", "straight", "revolution"], "revolution": ["straight", "reflex", "right"]}
KIND_E = {
    "acute": "An acute angle is smaller than a right angle: less than 90°.",
    "right": "A right angle is exactly 90°, a quarter turn. The small square shows it.",
    "obtuse": "An obtuse angle is bigger than a right angle but smaller than a straight angle: between 90° and 180°.",
    "straight": "A straight angle is exactly 180°, half a turn. The two arms make a straight line.",
    "reflex": "A reflex angle is bigger than a straight angle but smaller than a revolution: between 180° and 360°. "
              "Look at the arc: it goes round the outside.",
    "revolution": "A revolution is one whole turn: exactly 360°. The arm turns all the way round and ends where it started.",
}


def kind(d):
    return ("acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight" if d == 180
            else "reflex" if d < 360 else "revolution")


def name_q(q, k, wrong, e, rnd):
    return mcq(q, NAMES[k], [NAMES[w] for w in wrong], e, rnd)


def set_names(rnd, P):
    its = []
    q = "What is the name of the marked angle?"
    for d, rot in [(35, 15), (125, 0), (230, 0), (90, 30), (320, 20), (160, 10), (70, 100), (180, 0),
                   (200, 200), (360, 0), (100, 160), (180, 35)]:
        k = kind(d)
        e = KIND_E[k]
        if d not in (90, 180, 360):
            e += " This angle is %s." % D(d)
        if k == "reflex":
            e += " (The gap between the arms is %s, but the arc marks the big angle round the outside.)" % D(360 - d)
        if d == 90 or (d == 180 and rot):
            e += " Turning the angle does not change its size or its name."
        its.append(name_q(fig(name_fig(d, rot)) + q, k, WRONG[k], e, rnd))
    for d, wrong in [(175, ["straight", "reflex", "acute"]), (185, ["obtuse", "straight", "revolution"]),
                     (89, ["right", "obtuse", "reflex"]), (270, ["obtuse", "straight", "right"]),
                     (360, ["straight", "reflex", "right"])]:
        k = kind(d)
        e = {175: "175° is more than 90° but less than 180°, so it is obtuse. It is close to a straight angle, but not 180°.",
             185: "185° is more than 180° but less than 360°, so it is reflex, even though it is close to a straight angle.",
             89: "89° is less than 90°, so it is acute (only just). A right angle is exactly 90°.",
             270: "270° is more than 180° but less than 360°, so it is reflex. It is three right angles: 3 × 90° = 270°.",
             360: "360° is one whole turn: a revolution. A straight angle is only half a turn (180°)."}[d]
        its.append(name_q("An angle measures %s. What is its name?" % D(d), k, wrong, e, rnd))
    its.append(dq("How many degrees are in a revolution?", 360, [180, 90, 100],
                  "A revolution is one whole turn: 360°. It is 4 right angles: 4 × 90° = 360°. "
                  "180° is a straight angle, only half a turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says an angle of 190° is obtuse because it is bigger than 90°. Is %s right?" % (n, he),
                   "No, it is reflex", ["Yes, it is obtuse", "No, it is acute", "No, it is a revolution"],
                   "Obtuse angles are bigger than 90° but smaller than 180°. 190° is more than 180°, so it is reflex.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?",
                   "acute, right, obtuse, straight, reflex, revolution",
                   ["acute, obtuse, right, straight, reflex, revolution",
                    "acute, right, obtuse, reflex, straight, revolution",
                    "right, acute, obtuse, straight, revolution, reflex"],
                   "Acute is less than 90°, right is 90°, obtuse is between 90° and 180°, straight is 180°, "
                   "reflex is between 180° and 360°, and a revolution is 360°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name the angle", "items": its}


# ------------------------------------------------------------ estimate
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
            e = ("The angle is bigger than a right angle (90°) but smaller than a straight angle (180°), so it is obtuse. "
                 "About %s fits. (It is %s.)" % (D(best), D(d)))
        else:
            e = ("The arc goes round the outside, so the angle is reflex: more than 180°. The gap on the other side is about %s, "
                 "so the marked angle is about 360° − %s = %s. (It is %s.)" % (D(360 - best), D(360 - best), D(best), D(d)))
        if d < 180 and (180 - best) in wrong:
            e += " About %s would be a %s angle." % (D(180 - best), "much wider" if best < 90 else "much smaller")
        its.append(mcq(fig(angle_fig(d, rot)) + q, "about " + D(best), ["about " + D(w) for w in wrong], e, rnd))
    lab = "four angles labelled A to D"
    its.append(letter_q(fig(abcd_svg([(60, 0), (240, 0), (125, 0), (165, 0)], lab)) + "Which angle is closest to 120°?", "C",
                        "C is a bit more than a right angle: about 120°. A is about 60°. B is reflex (about 240°): its gap "
                        "looks like 120°, but the arc marks the big angle. D is nearly a straight angle."))
    its.append(letter_q(fig(abcd_svg([(170, 0), (95, 0), (30, 0), (215, 0)], lab)) + "Which angle is reflex?", "D",
                        "A reflex angle is more than 180°. Only the arc in D goes round more than a straight angle. "
                        "A is obtuse: nearly 180°, but not more."))
    its.append(letter_q(fig(abcd_svg([(250, 0, 30), (170, 0, 46), (100, 0, 50), (60, 0, 56)], lab)) +
                        "Which angle is the largest?", "A",
                        "The size of an angle is the amount of turn, not the length of the arms. A is reflex (about 250°), "
                        "so it is the largest, even though its arms are the shortest."))
    its.append(letter_q(fig(abcd_svg([(85, 0), (40, 0), (15, 0), (135, 0)], lab)) + "Which angle is closest to 45°?", "B",
                        "45° is half a right angle. B is about half of a right angle. A is nearly a right angle, "
                        "C is very small and D is obtuse."))
    its.append(letter_q(fig(abcd_svg([(80, 0), (260, 0), (30, 0), (145, 0)], lab)) + "Which angle is obtuse?", "D",
                        "Obtuse means between 90° and 180°. D is about 145°. B is reflex: the gap between its arms looks obtuse, "
                        "but the arc marks the angle round the outside."))
    its.append(mcq("An angle is a little smaller than a right angle. Which could it be?", "80°", ["100°", "180°", "170°"],
                   "A right angle is 90°. A little smaller than 90° is about 80°. 100° is a little bigger.", rnd))
    its.append(mcq("An angle is a little bigger than a straight angle. Which could it be?", "195°", ["165°", "95°", "360°"],
                   "A straight angle is 180°, so a little bigger is about 195°. 165° is a little smaller than a straight angle, "
                   "and 95° is a little bigger than a right angle.", rnd))
    its.append(mcq("An angle is about half a right angle. Which is the best estimate?", "45°", ["90°", "180°", "25°"],
                   "A right angle is 90°, and half of 90° is 45°.", rnd))
    its.append(mcq("Which is larger: three right angles or 250°?", "three right angles", ["250°", "they are equal", "you cannot tell"],
                   "Three right angles are 3 × 90° = 270°, and 270° is more than 250°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s estimates a reflex angle as about 70°. Why must %s be wrong?" % (n, he),
                   "A reflex angle is more than 180°", ["70° is too big for any angle", "A reflex angle is less than 90°",
                                                        "A reflex angle is exactly 180°"],
                   "Every reflex angle is more than 180°, so its estimate must be more than 180°. 70° may be the gap on the other "
                   "side: then the reflex angle is about 360° − 70° = 290°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Estimate angles", "items": its}


# ------------------------------------------------------------ measure with a protractor
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
    its.append(dq(fig(protractor_svg([0, 75], "protractor measuring an angle")) +
                  "The protractor measures the angle between the two arms. What is the <b>reflex</b> angle between the same arms?",
                  285, [75, 105, 255],
                  "On the inner scale the angle is 75°. The reflex angle goes the other way round. Together they make a revolution: "
                  "360° − 75° = 285°. (105° is the reading on the wrong scale.)", rnd))
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
    its.append(dq("To find a reflex angle, %s measures the angle on the other side. It is 130°. What is the reflex angle?" % n,
                  230, [130, 50, 310],
                  "The two angles go all the way round the vertex, so they make a revolution: 360°. 360° − 130° = 230°. "
                  "(50° comes from using 180° instead of 360°.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Measure with a protractor", "items": its}


# ------------------------------------------------------------ construct angles
def set_construct(rnd, P):
    its = []
    lab = "four angles labelled A to D"
    for size, angs, ans, e in [
        (40, [140, 40, 90, 220], "B",
         "B is acute, a bit less than half a right angle: 40°. A is 140°, what you get from the wrong protractor scale. "
         "C is a right angle and D is reflex."),
        (120, [60, 150, 240, 120], "D",
         "D is a bit more than a right angle: 120°. A is 60° (the wrong scale). C is reflex: its gap is 120°, "
         "but the arc marks 240°. B is 150°, wider than 120°."),
        (75, [75, 105, 285, 45], "A",
         "A is a bit less than a right angle: 75°. B is 105° (the wrong scale). C is reflex: its gap is 75°, but the arc marks 285°. "
         "D is only 45°."),
        (210, [150, 30, 210, 330], "C",
         "210° is reflex: a bit more than a straight angle. C fits. A is 150°, obtuse: its arc goes the short way. "
         "D is 330°, nearly a revolution."),
        (300, [60, 300, 240, 120], "B",
         "300° is reflex: a revolution (360°) minus 60°. In B the gap is 60° and the arc goes round the outside. "
         "A marks only the 60° gap."),
        (135, [45, 160, 225, 135], "D",
         "135° is a right angle and half a right angle more: D. A is 45° (the wrong scale). C is reflex (225°). B is 160°, nearly a straight angle."),
    ]:
        its.append(letter_q(fig(abcd_svg([(a, 0) for a in angs], lab)) +
                            "Which drawing shows an angle of %s?" % D(size), ans, e))
    its.append(letter_q(fig(abcd_svg([(80, 0), (100, 0), (90, 0), (45, 0)], lab)) + "Which drawing shows a right angle?", "C",
                        "A right angle is exactly 90°. C has the small square that shows 90°. A is a little less (80°) and B is a little more (100°)."))
    its.append(letter_q(fig(abcd_svg([(180, 0), (170, 0), (190, 0), (160, 0)], lab)) + "Which drawing shows a straight angle?", "A",
                        "A straight angle is 180°: the two arms make one straight line. B and D bend a little (170° and 160°). "
                        "C is reflex (190°): its arc goes past the straight line."))
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
    n, he, his = P.next()
    its.append(mcq("%s is constructing an angle of 65°. What should %s do first?" % (n, he), "Draw a straight arm with a ruler",
                   ["Mark a dot at 65", "Draw a curved arc", "Draw a dot at 65 on both scales"],
                   "First draw one straight arm with a ruler. Then put the centre of the protractor on one end, "
                   "line the arm up with 0 and mark 65.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s has drawn one arm. %s puts the centre of the protractor on its end, with the arm on 0 of the inner scale. "
                   "Where should %s mark a dot for 65°?" % (n, cap(he), he), "at 65 on the inner scale",
                   ["at 65 on the outer scale", "at 115 on the inner scale", "at 60 on the inner scale"],
                   "Use the scale that starts at 0 on your arm: the inner scale. Count up to 65 (the small mark between 60 and 70) "
                   "and mark a dot there. 65 on the outer scale would give 115°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s has marked a dot at 35 on the correct scale. What should %s do next?" % (n, he),
                   "Join the dot to the vertex with a ruler",
                   ["Join the dot to the end of the other arm", "Draw a circle through the dot", "Mark another dot at 145"],
                   "The second arm starts at the vertex and goes through the dot. Join them with a ruler, "
                   "then mark the angle with an arc.", rnd))
    its.append(mcq("A protractor only goes to 180°. How can you construct a reflex angle of 250°?",
                   "Draw 110°, then mark the angle outside it",
                   ["Draw 70°, then mark the angle outside it", "Draw 250 on the outer scale", "You cannot construct it"],
                   "360° − 250° = 110°. Construct an angle of 110°. The angle round the outside is then 250°. "
                   "(70° comes from 250° − 180°, but the two angles must make a revolution, 360°.)", rnd))
    its.append(dq("To construct a reflex angle of 300°, which angle should you draw first with the protractor?", 60,
                  [120, 30, 240],
                  "The two angles round the vertex make a revolution: 360°. 360° − 300° = 60°. Draw 60°, "
                  "then mark the big angle round the outside. (120° comes from 300° − 180°.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s constructs an angle of 145°, but it looks acute. What went wrong?" % n,
                   "%s read the wrong scale" % cap(he),
                   ["%s arms are too short" % cap(his), "145° is an acute angle", "%s should have used 360°" % cap(he)],
                   "145° is obtuse, so the angle should look wider than a right angle. On the other scale, 145 is in the same place as 35, "
                   "so %s drew 35°." % he, rnd))
    its.append(mcq("Which number is in the same place on both scales of a protractor?", "90", ["0", "180", "45"],
                   "90 is at the top, halfway round. It is 90 on the inner scale and 90 on the outer scale, so a right angle "
                   "is the same on both scales.", rnd))
    its.append(mcq("How do you construct a straight angle (180°)?",
                   "Draw one arm, then carry it on in a straight line past the vertex",
                   ["Draw two arms at a right angle", "Draw two arms on top of each other", "Draw an arm that turns all the way round"],
                   "A straight angle is half a turn: the two arms point in opposite directions and make one straight line. "
                   "Two arms at a right angle make only 90°.", rnd))
    its.append(mcq("What does a revolution look like when you draw it?",
                   "One arm, with an arc that goes all the way round back to it",
                   ["Two arms that make a straight line", "Two arms that make a right angle", "Two arms with an arc round the outside of a gap"],
                   "A revolution is a whole turn, 360°: the arm turns all the way round and ends where it started. "
                   "Two arms in a straight line make only 180°, a straight angle.", rnd))
    a, b = P.next(), P.next()
    its.append(mcq("%s constructs a 40° angle with arms 10 cm long. %s constructs a 40° angle with arms 5 cm long. "
                   "Which angle is bigger?" % (a[0], b[0]), "They are the same size",
                   ["%s’s angle" % a[0], "%s’s angle" % b[0], "You cannot tell"],
                   "The size of an angle is the amount of turn between the arms, not the length of the arms. Both are 40°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Construct angles", "items": its}


# ------------------------------------------------------------ everyday angles
def roof_svg():
    return shape_svg(tri_pts(25, 25, base=170), {0: "25°", 1: "25°"}, "roof with a pitch of 25 degrees")


def ramp_svg():
    return shape_svg(tri_pts(20, 90, base=160), {0: "20°"}, "skateboard ramp at 20 degrees to the ground", rights=(1,))


def set_everyday(rnd, P):
    its = []
    N = NAMES
    its.append(dq(fig(clock_svg(4)) + "What is the size of the marked angle between the hands at 4 o’clock?", 120,
                  [240, 90, 40],
                  "The 12 spaces between the numbers go round a revolution, 360°, so each space is 360° ÷ 12 = 30°. "
                  "At 4 o’clock the hands are 4 spaces apart: 4 × 30° = 120°.", rnd))
    its.append(name_q(fig(clock_svg(3)) + "What is the name of the marked angle between the hands at 3 o’clock?", "right",
                      ["acute", "obtuse", "straight"],
                      "At 3 o’clock the hands are 3 spaces apart: 3 × 30° = 90°. That is a right angle, a quarter turn.", rnd))
    its.append(name_q(fig(clock_svg(5)) + "What is the name of the marked angle between the hands at 5 o’clock?", "obtuse",
                      ["acute", "reflex", "straight"],
                      "At 5 o’clock the hands are 5 spaces apart: 5 × 30° = 150°. That is between 90° and 180°, so it is obtuse.", rnd))
    its.append(name_q("At 6 o’clock the hands of an analog clock point in opposite directions. What angle do they make?", "straight",
                      ["revolution", "reflex", "obtuse"],
                      "6 spaces × 30° = 180°. The hands make one straight line: a straight angle, half a turn. "
                      "(A revolution would be a whole turn, 360°.)", rnd))
    its.append(dq("At 8 o’clock the smaller angle between the hands is 120°. What is the reflex angle between the hands?", 240,
                  [120, 60, 300],
                  "The two angles between the hands make a revolution: 360°. 360° − 120° = 240°. "
                  "(60° comes from using 180° instead of 360°.)", rnd))
    its.append(dq("In one hour the minute hand turns all the way round once. How many degrees does it turn?", 360,
                  [180, 60, 12],
                  "All the way round once is a revolution: 360°. (180° is only half a turn, from 12 to 6.)", rnd))
    its.append(dq("How many degrees does the minute hand turn in 15 minutes?", 90, [15, 180, 45],
                  "60 minutes is a revolution (360°). 15 minutes is a quarter of an hour, so a quarter turn: 90°.", rnd))
    its.append(dq("The minute hand turns clockwise from 12 to 9. How many degrees does it turn?", 270, [90, 180, 45],
                  "12 to 3, 3 to 6 and 6 to 9 are three quarter turns: 3 × 90° = 270°, a reflex angle. "
                  "(90° is the short way, from 9 to 12.)", rnd))
    its.append(name_q(fig(roof_svg()) + "The pitch of this roof is the angle between the roof and the flat ceiling. It is 25°. "
                      "What is the name of this angle?", "acute", ["obtuse", "right", "reflex"],
                      "25° is less than 90°, so the roof pitch is an acute angle.", rnd))
    its.append(mcq("Four houses have roof pitches of 15°, 22°, 30° and 40°. Which roof is the steepest?", "the 40° roof",
                   ["the 15° roof", "the 22° roof", "the 30° roof"],
                   "The bigger the angle between the roof and the flat ceiling, the steeper the roof. 40° is the largest.", rnd))
    its.append(name_q(fig(ramp_svg()) + "This skateboard ramp makes an angle of 20° with the ground. What is the name of this angle?",
                      "acute", ["obtuse", "right", "straight"],
                      "20° is less than 90°, so it is acute. The small square shows the right angle at the back of the ramp.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s’s skateboard ramp makes 20° with the ground. %s rebuilds it at 35°. How is the new ramp different?" % (n, cap(he)),
                   "It is steeper", ["It is less steep", "It is the same", "It is a reflex angle"],
                   "A bigger angle with the ground makes a steeper ramp. 35° is bigger than 20°, but both are still acute.", rnd))
    its.append(mcq("In skateboarding, a “180” is a jump where the rider turns 180°. How much of a turn is that?",
                   "half a turn (a straight angle)",
                   ["a whole turn (a revolution)", "a quarter turn (a right angle)", "three-quarters of a turn"],
                   "180° is half of a revolution (360°): half a turn, a straight angle. The rider ends up facing the other way.", rnd))
    its.append(mcq("A skateboarder does a “360”. How much of a turn is that?", "a whole turn (a revolution)",
                   ["half a turn (a straight angle)", "a quarter turn (a right angle)", "three-quarters of a turn"],
                   "360° is one whole turn, a revolution: the rider ends up facing the same way again. "
                   "Half a turn would be a “180”.", rnd))
    n, he, his = P.next()
    its.append(dq("%s faces north on the school oval. %s turns until %s faces south. How many degrees has %s turned?"
                  % (n, cap(he), he, he), 180, [90, 360, 270],
                  "North to south is half a turn, whichever way you go: 180°, a straight angle. "
                  "(360° would bring %s back to face north.)" % n, rnd))
    n, he, his = P.next()
    its.append(name_q("%s opens %s laptop so the screen makes an angle of 110° with the keyboard. What is the name of this angle?"
                      % (n, his), "obtuse", ["right", "acute", "reflex"],
                      "110° is more than 90° but less than 180°, so it is obtuse.", rnd))
    n, he, his = P.next()
    its.append(dq("%s measures the angle between a playground slide and the ground. %s writes 140°, but the angle is clearly acute. "
                  "What is the angle?" % (n, cap(he)), 40, [140, 220, 50],
                  "An acute angle is less than 90°. %s read the wrong scale: 180° − 140° = 40°." % n, rnd))
    n, he, his = P.next()
    its.append(dq("%s cuts a round birthday cake into 6 equal slices from the centre. What angle does each slice make at the centre?" % n,
                  60, [30, 90, 120],
                  "The slices go all the way round the centre: a revolution, 360°. 360° ÷ 6 = 60°. "
                  "(30° comes from using 180° instead of 360°.)", rnd))
    its.append(dq("A ceiling fan blade turns 3 revolutions. How many degrees does it turn?", 1080, [540, 360, 900],
                  "One revolution is 360°. 3 × 360° = 1080°. (540° comes from using 180° for a revolution.)", rnd))
    its.append(dq("A steering wheel is turned three-quarters of a revolution. How many degrees is that?", 270, [135, 75, 90],
                  "A quarter of a revolution is 360° ÷ 4 = 90°. Three quarters is 3 × 90° = 270°. "
                  "(135° comes from using 180° for a revolution.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in everyday life", "items": its}


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
    kinds2 = strip_svg([angle_fig(180, 0, L=55), angle_fig(240, 0, L=55), rev_fig(0, L=55)],
                       ["straight", "reflex", "revolution"], "straight angle, reflex angle and revolution", cw=150)
    prot = protractor_svg([0, 50], "protractor measuring a 50 degree angle")
    return (
        "<h2>Angle names</h2>"
        "<p>An angle is an amount of <b>turn</b> between two arms. We measure it in <b>degrees</b> (°). "
        "A revolution (one whole turn) is <b>360°</b>, a straight angle (half a turn) is <b>180°</b> and a right angle "
        "(a quarter turn) is <b>90°</b>.</p>"
        "<figure class='sn-fig'>" + kinds + "</figure>"
        "<figure class='sn-fig'>" + kinds2 +
        "<figcaption>The arc shows which angle is meant. A reflex angle goes round the outside.</figcaption></figure>" +
        table(["Name", "Size"], [
            ["Acute angle", "less than 90°"],
            ["Right angle", "exactly 90°"],
            ["Obtuse angle", "more than 90°, less than 180°"],
            ["Straight angle", "exactly 180°"],
            ["Reflex angle", "more than 180°, less than 360°"],
            ["Revolution", "exactly 360°"],
        ]) +
        "<h2>Estimate first</h2>"
        "<p>Compare the angle with a right angle (90°) and a straight angle (180°). Is it smaller, between them or bigger? "
        "The length of the arms does not change the size of the angle.</p>" +
        ex("Estimate", "An angle is a bit wider than a right angle. About how big is it?",
           "It is more than 90° but much less than 180°, so it is obtuse.", "about 110° to 120°") +
        "<h2>Measure with a protractor</h2>"
        "<p>1. Put the centre of the protractor on the vertex. 2. Line up one arm with <b>0</b>. "
        "3. Read the scale that <b>starts at 0 on that arm</b>. 4. Check with your estimate: acute or obtuse?</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom arm is on 0 of the inner (green) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same place, but the angle is acute, so 130° cannot be right. "
        "The small marks go up in 5s.</figcaption></figure>" +
        ex("Reflex angle", "The gap on the other side of a reflex angle measures 130°. Find the reflex angle.",
           "The two angles make a revolution: 360° − 130° = 230°.", "230°") +
        "<h2>Construct an angle</h2>"
        "<p>To construct 65°: draw one arm with a ruler. Put the centre of the protractor on its end and line the arm up with 0. "
        "Mark a dot at 65 on the scale that starts at that 0. Join the dot to the vertex with a ruler.</p>" +
        ex("Construct a reflex angle", "Construct an angle of 250°.",
           "A protractor only goes to 180°. 360° − 250° = 110°. Construct 110°, then mark the angle round the outside.",
           "the outside of a 110° angle") +
        "<h2>Angles around us</h2>" +
        table(["Example", "Angle", "Name"], [
            ["Clock hands at 3 o’clock", "90°", "right angle"],
            ["Clock hands at 6 o’clock", "180°", "straight angle"],
            ["A house roof pitch", "often 15° to 30°", "acute angle"],
            ["A skateboarder’s “180”", "180°", "straight angle (half a turn)"],
            ["A skateboarder’s “360”", "360°", "revolution (a whole turn)"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (140° for a 40° angle)", "Read the scale that starts at 0 on your arm, then check your estimate"],
            ["Calling 190° obtuse", "Obtuse is between 90° and 180°. More than 180° is reflex"],
            ["Saying a revolution is 180°", "A straight angle is 180° (half a turn). A revolution is 360° (a whole turn)"],
            ["Thinking longer arms make a bigger angle", "The size of an angle is the amount of turn, not the length of the arms"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about angles in the Australian Curriculum?",
     "a": "They estimate, construct and measure angles in degrees with a protractor, and connect the sizes to the angle names: acute, right, obtuse, straight, reflex and revolution."},
    {"q": "How do you measure an angle with a protractor?",
     "a": "Estimate first. Put the centre on the vertex, line up one arm with 0 and read the scale that starts at that 0, then check the reading against your estimate."},
    {"q": "What are the angle names and their sizes?",
     "a": "Acute is less than 90°, right is 90°, obtuse is between 90° and 180°, straight is 180°, reflex is between 180° and 360°, and a revolution is 360°."},
    {"q": "Why do protractors have two scales?",
     "a": "So you can measure from an arm on either side: one scale starts at 0 on the right and the other at 0 on the left. Always read the scale that starts at 0 on your arm."},
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
    rnd = random.Random(5813)
    P = People(rnd)
    sets = [set_names(rnd, P), set_estimate(rnd, P), set_protractor(rnd, P), set_construct(rnd, P), set_everyday(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "measuring-angles", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Angles",
        "seo_title": "Year 5 Measuring Angles Worksheets: Protractor, Estimating and Angle Names",
        "short_title": "Measuring angles",
        "domain": "Measurement",
        "standard_code": "AC9M5M04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Estimate, construct and measure angles in degrees, using appropriate tools including a protractor, "
                         "and relate these measures to angle names",
        "meta_desc": "Free Year 5 measuring angles worksheets for the Australian Curriculum: name acute, right, obtuse, straight "
                     "and reflex angles and a revolution, estimate angles, read both protractor scales, construct angles and "
                     "find angles in everyday life. 100 maths questions with an answer key, great for NAPLAN practice.",
        "key_big": "Right angle 90°, straight angle 180°, revolution 360°. Measure with a protractor and read the scale that starts at 0 on your arm.",
        "key_sub": "Estimate first: acute is less than 90°, obtuse is between 90° and 180°, reflex is between 180° and 360°. "
                   "If the reading does not match your estimate, you read the wrong scale (40° and 140° sit at the same place).",
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
