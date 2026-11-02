# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Comparing angles (Australian Curriculum v9.0, AC9M4M04)
  python3 tools/gen_au_maths_y4_angles.py
Name and compare angles with a right angle: acute, right, obtuse, straight, reflex and revolution.
No degrees (that is Year 5). Every angle is drawn exactly (trig, 0 = pointing right, anticlockwise,
SVG y goes down); every marked angle is measured back from the drawing and checked. Angles in pictures
that are not right, straight or a revolution are at least 20 degrees away from those, so students can judge them.
Australian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]




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

    def line(self, p, q, col=GREEN, sw=3, dash=None):
        d = " stroke-dasharray='%s'" % dash if dash else ""
        self.el.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='%s'%s/>"
                        % (p[0], p[1], q[0], q[1], col, sw, "butt" if dash else "round", d)))
        self.segs.append((p, q))
        n = max(2, int(dist(p, q) / 2))
        self.pts.extend([(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)])

    def poly(self, pts, fill=FILL, sw=3, col=GREEN):
        self.el.append((0, "<polygon points='%s' fill='%s' stroke='none'/>" % (" ".join("%.1f,%.1f" % p for p in pts), fill)))
        n = len(pts)
        for i in range(n):
            self.line(pts[i], pts[(i + 1) % n], col=col, sw=sw)

    def circle(self, c, r, fill="none", col=INK, sw=3):
        self.el.append((1, "<circle cx='%.1f' cy='%.1f' r='%g' fill='%s' stroke='%s' stroke-width='%g'/>" % (c[0], c[1], r, fill, col, sw)))
        R = r + sw / 2.0
        self.pts.extend([(c[0] + R * math.cos(t / 8.0), c[1] + R * math.sin(t / 8.0)) for t in range(51)])

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



def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D, turns, compass points, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fix": True}


def mcq_num(q, correct, e):
    return mcq_fixed(q, ["1", "2", "3", "4"], str(correct), e)


# ------------------------------------------------------------ Year 4 figures (no degrees shown)
def judgeable(d):
    """Without a protractor, a picture must be clearly one kind: right, straight and revolution exactly,
    anything else at least 20° away from them."""
    assert d in (90, 180, 360) or (abs(d - 90) >= 20 and abs(d - 180) >= 20 and 0 < d <= 340), d


def angle_fig(d, rot=0, L=70, L2=None, label="marked angle"):
    """Two arms from O: one at rot, the other at rot + d (anticlockwise). The arc marks the angle d
    (round the outside when d is reflex); a right angle gets the small square."""
    judgeable(d)
    if d == 360:
        return rev_fig(rot, L=L, label=label)
    P = Pic()
    A, B = pol(O, L, rot), pol(O, L2 or L, rot + d)
    P.line(O, A)
    P.line(O, B)
    if d == 90:
        P.mark(O, A, B, 90, kind="right", ccw=True)
    else:
        P.mark(O, A, B, d, r=(22 if d < 40 else 17 if d > 180 else 16), ccw=True)
    P.dot(O)
    return P.svg(label)


def rev_fig(rot, label="revolution", L=70, r=18):
    """A revolution: one arm, and an arrow that turns all the way round back to it."""
    P = Pic()
    P.line(O, pol(O, L, rot))
    a0, a1 = rot + 12, rot + 348
    P.arc(O, r, a0, a1)
    E = pol(O, r, a1)
    t = a1 + 90
    P.polyline([pol(E, 7, t + 180 - 35), E, pol(E, 7, t + 180 + 35)], INK, 1.8)
    P.dot(O)
    return P.svg(label)


def turn_fig(frac, cw=True, L=50, r=22, label=None):
    """Dashed start arm pointing up, a curved arrow for the turn and the solid end arm."""
    P = Pic()
    P.line(O, pol(O, L, 90), col=INK, sw=2.4, dash="5 4")
    sg = -1 if cw else 1
    sweep = 360.0 * frac
    a0, a1 = 90 + sg * 8, 90 + sg * (min(sweep, 352) - 12)
    n = max(8, int(abs(a1 - a0) / 4))
    P.polyline([pol(O, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)], GREEN, 2.6)
    E = pol(O, r, a1)
    t = a1 + sg * 90                       # direction of travel at the end of the arrow
    P.polyline([pol(E, 8, t + 180 - 35), E, pol(E, 8, t + 180 + 35)], GREEN, 2.6)
    if frac < 1:
        P.line(O, pol(O, L, 90 + sg * sweep), col=GREEN, sw=3.4)
    P.dot(O, 4)
    return P.svg(label or "%s turn %s" % ({0.25: "quarter", 0.5: "half", 0.75: "three-quarter", 1.0: "full"}[frac],
                                         "clockwise" if cw else "anticlockwise"))


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
        assert w <= cw and tw(c, fs) <= cw, (c, w, cw)
        x, y = k * cw + (cw - w) / 2.0, (top - h) / 2.0
        inner = re.sub(r"^<svg [^>]*>", "", s)
        assert inner.endswith("</svg>")
        out.append("<g transform='translate(%.1f %.1f)'>%s</g>" % (x, y, inner[:-6]))
        out.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                   % (k * cw + cw / 2.0, top + fs + 6, fs, INK, c))
    return svg_wrap(int(math.ceil(cw * len(svgs))), top + fs + 12, "".join(out), label)


def abcd_svg(angles, label="four angles labelled A to D"):
    """angles: (size, rot, arm length)."""
    return strip_svg([angle_fig(d, rot, L) for d, rot, L in angles], ["A", "B", "C", "D"], label, fs=18)


def pair_svg(a, b, names=("P", "Q"), label=None):
    return strip_svg([angle_fig(*a), angle_fig(*b)], list(names),
                     label or "angle %s and angle %s" % names, fs=18)


def clock_svg(h, label=None):
    """Analog clock at h o'clock. The red arc marks the angle from the minute hand (on 12) clockwise to the
    hour hand: 30° for every hour mark. Square picture."""
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
    sweep = 30 * h
    n = max(6, sweep // 6)
    arc = [pol(c, 13, 90 - sweep * i / n) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in arc), RED))
    hh, mh = pol(c, 19, 90 - sweep), pol(c, 27, 90)
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='60' cy='60' r='4' fill='%s'/>" % INK)
    return svg_wrap(120, 120, "".join(s), label or "analog clock showing %d o’clock" % h)


WALL = "#9a948b"
WOODD = "#8b5a2b"


def door_svg(d, label=None):
    """A door seen from above. It turns about the hinge (dot) from the closed position (dashed) to d."""
    judgeable(d)
    P = Pic()
    Ld = 64
    P.line(pol(O, 34, 180), O, col=WALL, sw=7)
    P.line((Ld, 0.0), (Ld + 34, 0.0), col=WALL, sw=7)
    P.line(O, (Ld, 0.0), col=INK, sw=2, dash="5 4")
    D2 = pol(O, Ld, d)
    P.line(O, D2, col=WOODD, sw=5)
    P.mark(O, (Ld, 0.0), D2, d, r=18, ccw=True)
    P.dot(O, 4)
    return P.svg(label or "open door seen from above")


def scissors_svg(d, blade=70, handle=26, label=None):
    """Open scissors: two straight arms crossing at the pivot; blades to the right, finger rings to the left."""
    judgeable(d)
    P = Pic()
    for s_ in (1, -1):
        P.line(O, pol(O, blade, s_ * d / 2.0), col=INK, sw=3.4)
        e = pol(O, handle, 180 + s_ * d / 2.0)
        P.line(O, e, col=RED, sw=4)
        P.circle(pol(e, 9, 180 + s_ * d / 2.0), 9, col=RED, sw=3.4)
    P.mark(O, pol(O, blade, -d / 2.0), pol(O, blade, d / 2.0), d, r=20, ccw=True)
    P.dot(O, 3.5)
    return P.svg(label or "open scissors")


def laptop_svg(d, label=None):
    """A laptop seen from the side: keyboard flat, screen turned up to angle d."""
    judgeable(d)
    P = Pic()
    P.line(O, (92.0, 0.0), col=INK, sw=6)
    S = pol(O, 70, d)
    P.line(O, S, col=GREEN, sw=5)
    P.mark(O, (92.0, 0.0), S, d, r=20, ccw=True)
    return P.svg(label or "laptop seen from the side")


def interior(pts):
    """Interior angles of a simple polygon (y down), convex or not."""
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    out = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u = ((a[0] - b[0]) / dist(a, b), (a[1] - b[1]) / dist(a, b))
        v = ((c[0] - b[0]) / dist(c, b), (c[1] - b[1]) / dist(c, b))
        base = math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1]))))
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out.append(base if cr * area > 0 else 360 - base)
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, "not a simple polygon"
    return out


def mark_inside(P, pts, i, A, text=None):
    """Mark the inside angle at corner i (it may be reflex)."""
    n = len(pts)
    V, p, q = pts[i], pts[i - 1], pts[(i + 1) % n]
    if abs((ang(V, q) - ang(V, p)) % 360 - A[i]) < 1e-6:
        p, q = p, q
    else:
        p, q = q, p
    assert abs((ang(V, q) - ang(V, p)) % 360 - A[i]) < 1e-6
    if abs(A[i] - 90) < 1e-6 and not text:
        P.mark(V, p, q, 90, kind="right", ccw=True)
    else:
        P.mark(V, p, q, A[i], text, r=(16 if A[i] > 180 else None), ccw=True)


def concave_svg(pts, marks, label, texts=None):
    """Polygon (convex or not) with the inside angle marked at the corners in `marks`."""
    P = Pic()
    P.poly(pts)
    A = interior(pts)
    for i in marks:
        judgeable(round(A[i], 9))
        mark_inside(P, pts, i, A, (texts or {}).get(i))
    return P.svg(label)


LSHAPE = [(0.0, 0.0), (50.0, 0.0), (50.0, 60.0), (110.0, 60.0), (110.0, 100.0), (0.0, 100.0)]
DART = [(0.0, 0.0), (120.0, 45.0), (0.0, 90.0), (34.0, 45.0)]
HEX = [pol(O, 50, 60 * i) for i in range(6)]
OBT = tri_pts(25, 35, base=150)            # angle C at the top is 120°
PIZ = "#f3d27a"
CRUST = "#b8862e"


def pizza_svg(eaten, label=None):
    """A round pizza cut into 8 equal slices with `eaten` slices gone (taken from the right-hand side).
    The angle of what is left is marked at the centre."""
    P = Pic()
    R = 50
    a0 = 45 * eaten / 2.0
    a1 = 360 - a0
    n = int((a1 - a0) / 5)
    rim = [pol(O, R, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    P.poly([O] + rim, fill=PIZ, sw=3, col=CRUST)
    for k in range(1, 8 - eaten):
        P.line(O, pol(O, R, a0 + 45 * k), col=CRUST, sw=1.6)
    for k in range(8 - eaten):
        P.dot(pol(O, 34, a0 + 45 * k + 22.5), 4)
    P.mark(O, pol(O, R, a0), pol(O, R, a1), a1 - a0, r=15, ccw=True)
    return P.svg(label or "pizza cut into 8 slices with %d eaten" % eaten)


POINTS = ["north", "east", "south", "west"]
TURNS = ["quarter turn", "half turn", "three-quarter turn", "full turn"]


def compass_svg(face, label=None):
    """A student (circle) in the middle with an arrow showing the way they face; N E S W around."""
    P = Pic()
    R = 48
    for i, t in enumerate("NESW"):
        c = pol(O, R, 90 - 90 * i)
        P.label(c[0], c[1], t, fs=18)
    P.circle(O, 11, fill=FILL, col=GREEN, sw=2.5)
    d = 90 - 90 * face
    P.line(pol(O, 13, d), pol(O, 28, d), col=INK, sw=3.4)
    tip = pol(O, 36, d)
    P.el.append((1, "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in
                 (tip, pol(tip, 11, d + 180 - 32), pol(tip, 11, d + 180 + 32))), INK)))
    P.pts.extend([tip, pol(tip, 11, d + 180 - 32), pol(tip, 11, d + 180 + 32)])
    return P.svg(label or "student facing %s" % POINTS[face])


# ------------------------------------------------------------ angle names
NAMES = {"acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle",
         "reflex": "reflex angle", "revolution": "revolution"}
WRONG = {"acute": ["obtuse", "right", "reflex"], "right": ["acute", "obtuse", "straight"],
         "obtuse": ["acute", "reflex", "straight"], "straight": ["obtuse", "reflex", "revolution"],
         "reflex": ["obtuse", "straight", "revolution"], "revolution": ["straight", "reflex", "right"]}
KIND_E = {
    "acute": "An acute angle is less than a right angle: narrower than a square corner.",
    "right": "A right angle is a square corner: a quarter turn. The small square shows it.",
    "obtuse": "An obtuse angle is greater than a right angle but less than a straight angle.",
    "straight": "A straight angle is 2 right angles: a half turn. The two arms make a straight line.",
    "reflex": "A reflex angle is greater than a straight angle but less than a revolution. The arc goes round the outside.",
    "revolution": "A revolution is one whole turn: 4 right angles. The arm goes all the way round and ends where it started.",
}


def kind(d):
    return ("acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight" if d == 180
            else "reflex" if d < 360 else "revolution")


def name_q(q, k, e, rnd, wrong=None):
    return mcq(q, NAMES[k], [NAMES[w] for w in (wrong or WRONG[k])], e, rnd)


SAME = ["angle P", "angle Q", "They are the same size", "You cannot tell"]


# ------------------------------------------------------------ set 1: name the angle
def set_names(rnd, P):
    its = []
    q = "What is the name of the marked angle?"
    for d, rot, L in [(40, 10, 70), (90, 30, 64), (130, 0, 60), (180, 0, 60), (240, 0, 56), (360, 0, 60),
                      (60, 110, 74), (150, 200, 58), (300, 20, 54), (180, 60, 60), (115, 40, 66)]:
        k = kind(d)
        e = KIND_E[k]
        if k == "reflex":
            e += " The gap between the arms is small, but the marked angle is the big one."
        if rot and d in (90, 180):
            e += " Turning the angle does not change its name."
        its.append(name_q(fig(angle_fig(d, rot, L)) + q, k, e, rnd))
    its.append(name_q("An angle is less than a right angle. What is it called?", "acute",
                      "An acute angle is less than a right angle. An obtuse angle is greater than a right angle.", rnd))
    its.append(name_q("An angle is greater than a right angle but less than a straight angle. What is it called?", "obtuse",
                      "Between a right angle and a straight angle is an obtuse angle.", rnd, ["acute", "reflex", "right"]))
    its.append(name_q("An angle is greater than a straight angle but less than a revolution. What is it called?", "reflex",
                      "Between a straight angle (a half turn) and a revolution (a full turn) is a reflex angle. "
                      "An obtuse angle is less than a straight angle.", rnd))
    its.append(name_q("Which angle is one whole turn?", "revolution",
                      "A revolution is one whole turn: the arm turns all the way round. A straight angle is only half a turn.", rnd))
    its.append(mcq_num("How many right angles make a straight angle?", 2,
                       "A straight angle is a half turn. A half turn is 2 quarter turns, so it is 2 right angles."))
    its.append(mcq_num("How many right angles make a revolution?", 4,
                       "A revolution is a full turn. A full turn is 4 quarter turns, so it is 4 right angles."))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(180, 15, 62)) + "%s says there is no angle here because the arms make a straight line. "
                   "Is %s right?" % (n, he),
                   "No, it is a straight angle", ["Yes, a straight line is not an angle", "No, it is a right angle",
                                                  "No, it is a reflex angle"],
                   "The arm has turned a half turn from the other arm. That turn is an angle: a straight angle (2 right angles).", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(230, 10, 60)) + "%s says the marked angle is obtuse. Is %s right?" % (n, he),
                   "No, it is a reflex angle", ["Yes, it is an obtuse angle", "No, it is an acute angle",
                                                "No, it is a straight angle"],
                   "The arc goes round the outside. The gap between the arms looks obtuse, but the marked angle is greater "
                   "than a straight angle, so it is reflex.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?",
                   "acute, right, obtuse, straight, reflex, revolution",
                   ["acute, obtuse, right, straight, reflex, revolution",
                    "acute, right, obtuse, reflex, straight, revolution",
                    "right, acute, obtuse, straight, revolution, reflex"],
                   "Acute is less than a right angle. Obtuse is between a right angle and a straight angle. "
                   "Reflex is between a straight angle and a revolution, which is the largest.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name the angle: acute, right, obtuse, straight, reflex, revolution", "items": its}


# ------------------------------------------------------------ set 2: compare two angles
def set_compare(rnd, P):
    its = []
    q = "Which marked angle is larger?"
    for a, b, ans, e in [
        ((50, 15, 80), (120, 10, 34), "angle Q",
         "Angle Q is obtuse and angle P is acute. Q is larger, even though its arms are shorter."),
        ((140, 0, 34), (70, 20, 82), "angle P",
         "Angle P is obtuse and angle Q is acute. Long arms do not make an angle larger."),
        ((60, 10, 82), (60, 10, 34), "They are the same size",
         "Both angles open the same amount. Only the arms are different lengths, and arm length does not change an angle."),
        ((130, 0, 66), (230, 0, 50), "angle Q",
         "Angle Q is reflex: its arc goes round the outside, past a straight angle. Angle P is obtuse, less than a straight angle."),
        ((90, 0, 36), (90, 40, 76), "They are the same size",
         "Both are right angles (the small squares show it). Tilting an angle or making its arms longer does not change it."),
        ((300, 20, 40), (160, 0, 78), "angle P",
         "Angle P is reflex, so it is greater than a straight angle. Angle Q is obtuse, less than a straight angle."),
        ((35, 0, 60), (65, 0, 60), "angle Q",
         "Both are acute, but angle Q opens wider. Put one on top of the other to check."),
        ((180, 0, 44), (150, 10, 80), "angle P",
         "Angle P is a straight angle. Angle Q is obtuse: it is less than a straight angle, even with longer arms."),
    ]:
        its.append(mcq_fixed(fig(pair_svg(a, b)) + q, SAME, ans, e))
    lab = "four angles labelled A to D"
    its.append(mcq_fixed(fig(abcd_svg([(50, 10, 66), (140, 0, 30), (90, 0, 52), (25, 10, 70)], lab)) +
                         "Which angle is the largest?", ["A", "B", "C", "D"], "B",
                         "B is obtuse, so it is greater than a right angle. A and D are acute and C is a right angle. "
                         "B has the shortest arms, but arm length does not matter."))
    its.append(mcq_fixed(fig(abcd_svg([(130, 0, 66), (90, 0, 52), (35, 0, 30), (210, 0, 52)], lab)) +
                         "Which angle is the smallest?", ["A", "B", "C", "D"], "C",
                         "C is acute: less than a right angle. A is obtuse, B is a right angle and D is reflex."))
    its.append(mcq_fixed(fig(abcd_svg([(160, 0, 54), (90, 0, 52), (45, 0, 60), (250, 0, 46)], lab)) +
                         "Which angle is reflex?", ["A", "B", "C", "D"], "D",
                         "Only the arc in D goes round more than a straight angle. A is obtuse: close to a straight angle, but less."))
    its.append(mcq_fixed(fig(abcd_svg([(125, 0, 52), (250, 0, 46), (60, 0, 60), (180, 0, 44)], lab)) +
                         "Which angle is obtuse?", ["A", "B", "C", "D"], "A",
                         "A is greater than a right angle but less than a straight angle. In B the gap looks obtuse, but the "
                         "arc marks the reflex angle round the outside."))
    trio = strip_svg([angle_fig(120, 10, 34), angle_fig(40, 10, 80), angle_fig(230, 0, 46)], ["X", "Y", "Z"],
                     "angles X, Y and Z", fs=18)
    its.append(mcq(fig(trio) + "Put the angles in order from smallest to largest.", "Y, X, Z",
                   ["X, Y, Z", "Z, X, Y", "Y, Z, X"],
                   "Y is acute, X is obtuse and Z is reflex. Look at the turn and the arc, not the arm length.", rnd))
    its.append(mcq("Which is always larger: an obtuse angle or an acute angle?", "the obtuse angle",
                   ["the acute angle", "They are the same size", "You cannot tell"],
                   "An acute angle is less than a right angle. An obtuse angle is greater than a right angle. "
                   "So the obtuse angle is always larger.", rnd))
    its.append(mcq("Which is always larger: a straight angle or a reflex angle?", "the reflex angle",
                   ["the straight angle", "They are the same size", "You cannot tell"],
                   "A reflex angle is greater than a straight angle, by definition.", rnd))
    its.append(mcq_fixed("Angle P is a right angle. Angle Q is a little less than a right angle. Which angle is larger?",
                         SAME, "angle P", "Angle Q is less than a right angle, so the right angle P is larger."))
    n, he, his = P.next()
    its.append(mcq("%s draws two angles. Angle P has arms 10 cm long and angle Q has arms 3 cm long. %s says P must be "
                   "the larger angle. Is %s right?" % (n, cap(he), he),
                   "No, arm length does not change the size of an angle",
                   ["Yes, longer arms make a larger angle", "Yes, P is 7 cm larger", "No, Q is always larger"],
                   "The size of an angle is the amount of turn between the arms. You cannot tell which is larger "
                   "from the arm lengths.", rnd))
    its.append(name_q("Which of these angles is smaller than a right angle?", "acute",
                      "Only an acute angle is less than a right angle. Obtuse, straight and reflex angles are all larger.",
                      rnd, ["obtuse", "straight", "reflex"]))
    its.append(mcq("Two angles are both obtuse. What do you know for sure?", "Both are larger than a right angle",
                   ["They are the same size", "Both are larger than a straight angle", "Both have long arms"],
                   "Every obtuse angle is greater than a right angle and less than a straight angle. "
                   "Two obtuse angles can still be different sizes.", rnd))
    its.append(mcq("An angle is larger than 2 right angles but smaller than 4 right angles. What kind of angle is it?",
                   "reflex angle", ["obtuse angle", "straight angle", "revolution"],
                   "2 right angles make a straight angle and 4 make a revolution. Between them is a reflex angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare angles (arm length does not matter)", "items": its}


# ------------------------------------------------------------ set 3: angles in shapes and objects
def set_objects(rnd, P):
    its = []
    for h, e in [(2, "The hands are 2 hour marks apart. A right angle is 3 hour marks (3 o’clock), so this is less: acute."),
                 (3, "At 3 o’clock the hands make a square corner: a right angle."),
                 (4, "The hands are 4 hour marks apart. That is more than 3 (a right angle) and less than 6 (a straight angle): obtuse."),
                 (6, "At 6 o’clock the hands point in opposite directions. They make a straight angle.")]:
        its.append(name_q(fig(clock_svg(h)) + "What kind of angle is marked between the clock hands?", kind(30 * h), e, rnd))
    its.append(name_q(fig(clock_svg(8, "analog clock at 8 o’clock with the angle from 12 to 8 marked")) +
                      "The red arc goes clockwise from the minute hand to the hour hand. What kind of angle does it mark?",
                      "reflex", "From 12 to 8 is 8 hour marks, more than 6 (a straight angle). So the marked angle is reflex. "
                      "The gap on the other side is obtuse, but that is not the marked angle.", rnd))
    q = "This door is seen from above. It opened from the dashed line. What kind of angle has it opened?"
    its.append(name_q(fig(door_svg(60)) + q, "acute",
                      "The door has opened less than a square corner, so the angle is acute.", rnd))
    its.append(name_q(fig(door_svg(130)) + q, "obtuse",
                      "The door has opened past a square corner but not to a straight line, so the angle is obtuse.", rnd))
    its.append(name_q(fig(scissors_svg(40)) + "What kind of angle do the blades of these scissors make?", "acute",
                      "The blades open less than a square corner, so the angle is acute.", rnd))
    its.append(name_q(fig(laptop_svg(115)) + "This laptop is seen from the side. What kind of angle does the screen make with the keyboard?",
                      "obtuse", "The screen leans back past a square corner, but not flat. That is an obtuse angle.", rnd))
    sc = strip_svg([scissors_svg(30, 74, 28), scissors_svg(60, 40, 18)], ["P", "Q"], "scissors P and Q", fs=18)
    its.append(mcq_fixed(fig(sc) + "Which scissors are open wider?",
                         ["scissors P", "scissors Q", "They are open the same amount", "You cannot tell"], "scissors Q",
                         "The angle between the blades of Q is larger. P has longer blades, but long blades do not make "
                         "a larger angle."))
    its.append(mcq_fixed(fig(shape_svg(OBT, {0: "A", 1: "B", 2: "C"}, "triangle with angles A, B and C")) +
                         "Which angle in this triangle is obtuse?", ["angle A", "angle B", "angle C", "none of them"], "angle C",
                         "Angle C at the top opens wider than a right angle, so it is obtuse. A and B are acute."))
    hx = concave_svg(HEX, [0], "regular hexagon with one angle marked")
    its.append(name_q(fig(hx) + "What kind of angle is marked inside this hexagon?", "obtuse",
                      "Each corner of a regular hexagon is wider than a square corner but less than a straight line: obtuse.", rnd))
    its.append(name_q(fig(concave_svg(LSHAPE, [2], "L-shape with the inside corner marked")) +
                      "What kind of angle is marked inside this L-shape?", "reflex",
                      "The marked corner points inwards. Inside the shape it is 3 right angles, more than a straight angle: reflex.", rnd,
                      ["right", "obtuse", "straight"]))
    n, he, his = P.next()
    its.append(mcq(fig(concave_svg(DART, [3], "arrowhead shape with the inside corner marked")) +
                   "%s says the marked angle inside this arrowhead is obtuse. Is %s right?" % (n, he),
                   "No, it is a reflex angle", ["Yes, it is an obtuse angle", "No, it is an acute angle", "No, it is a straight angle"],
                   "The corner points into the shape, so the angle inside is greater than a straight angle: reflex. "
                   "The gap outside the shape is the obtuse one.", rnd))
    its.append(name_q(fig(pizza_svg(1)) + "A pizza was cut into 8 equal slices and 1 slice was eaten. "
                      "What kind of angle does the rest of the pizza make at the centre?", "reflex",
                      "7 of the 8 slices are left. That is more than half the pizza (a straight angle) but less than a whole "
                      "(a revolution), so the angle is reflex.", rnd))
    its.append(name_q("A pizza is cut into 8 equal slices. What kind of angle is at the tip of one slice?", "acute",
                      "2 slices make a quarter of the pizza: a right angle. One slice is half of that, so it is acute.", rnd))
    its.append(name_q("A pizza is cut into 2 equal halves. What kind of angle is at the centre of one half?", "straight",
                      "Half a pizza has a straight cut edge through the centre. Half a turn is a straight angle.", rnd))
    its.append(name_q("A right-angled triangle has 1 right angle. What kind of angles are the other 2?", "acute",
                      "The other 2 angles of a right-angled triangle together make 1 right angle, so each one is "
                      "less than a right angle: acute.", rnd))
    its.append(name_q("What kind of angle is at each corner of a give way sign (a triangle with equal sides)?", "acute",
                      "Each corner of an equilateral triangle is narrower than a square corner, so it is acute.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s opens a book and lays it flat on the table. What angle do the two covers make?" % n, "straight",
                      "When the book lies flat, the covers make a straight line: a straight angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in shapes and everyday objects", "items": its}


# ------------------------------------------------------------ set 4: turns and right angles
def set_turns(rnd, P):
    its = []
    q = "The arm turns from the dashed line in the direction of the arrow. What angle does the turn make?"
    for frac, cw, k, e in [
        (0.25, True, "right", "A quarter turn makes a right angle: a square corner."),
        (0.5, False, "straight", "A half turn makes the arm point the opposite way. That is a straight angle: 2 right angles."),
        (0.75, True, "reflex", "A three-quarter turn is 3 right angles. That is more than a straight angle, so it is reflex."),
        (1.0, False, "revolution", "The arm turns all the way round, back to the dashed line. A full turn is a revolution."),
    ]:
        its.append(name_q(fig(turn_fig(frac, cw)) + q, k, e, rnd))
    its.append(mcq_num("How many right angles make a three-quarter turn?", 3,
                       "Each right angle is a quarter turn. 3 quarter turns make a three-quarter turn."))
    its.append(mcq_fixed("Which turn makes a straight angle?", TURNS, "half turn",
                         "A straight angle is 2 right angles, and 2 quarter turns make a half turn."))
    its.append(mcq_fixed("Which turn makes a revolution?", TURNS, "full turn",
                         "A revolution is one whole turn: a full turn, or 4 right angles."))
    its.append(mcq_fixed("Which turn makes a right angle?", TURNS, "quarter turn",
                         "A right angle is a quarter turn: a square corner."))
    its.append(name_q("An arm turns less than a quarter turn. What kind of angle does it make?", "acute",
                      "A quarter turn is a right angle. Less than that is an acute angle.", rnd))
    its.append(name_q("An arm turns more than a quarter turn but less than a half turn. What kind of angle does it make?", "obtuse",
                      "More than a right angle but less than a straight angle is obtuse.", rnd))
    its.append(name_q("An arm turns more than a half turn but less than a full turn. What kind of angle does it make?", "reflex",
                      "More than a straight angle but less than a revolution is reflex.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s faces north. %s turns clockwise until %s faces south. What angle has %s turned through?"
                      % (n, cap(he), he, he), "straight",
                      "North to south is a half turn: 2 right angles. That is a straight angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s faces east. %s turns clockwise until %s faces north. What angle has %s turned through?"
                      % (n, cap(he), he, he), "reflex",
                      "Clockwise from east: south (1), west (2), north (3). 3 right angles is a reflex angle.", rnd))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(compass_svg(3)) + "%s faces west. %s turns clockwise through 1 right angle. Which way does %s face now?"
                         % (n, cap(he), he), POINTS, "north",
                         "Clockwise goes north, east, south, west, then back to north. 1 right angle clockwise from west is north."))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(compass_svg(0)) + "%s faces north. %s turns anticlockwise through 3 right angles. Which way does %s face now?"
                         % (n, cap(he), he), POINTS, "east",
                         "Anticlockwise from north: west (1), south (2), east (3). So %s faces east." % he))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(compass_svg(2)) + "%s faces south. %s turns through a straight angle. Which way does %s face now?"
                         % (n, cap(he), he), POINTS, "north",
                         "A straight angle is a half turn, so %s faces the opposite way. North is opposite south." % he))
    n, he, his = P.next()
    its.append(mcq("%s turns from facing north to facing south. %s says that makes no angle, because %s is still on the same "
                   "straight line. Is %s right?" % (n, cap(he), he, he),
                   "No, it is a straight angle", ["Yes, it makes no angle", "No, it is a right angle", "No, it is a revolution"],
                   "%s turned a half turn. A half turn is an angle: a straight angle, 2 right angles." % n, rnd))
    its.append(mcq("Which of these is a reflex angle?", "3 right angles",
                   ["1 right angle", "2 right angles", "4 right angles"],
                   "1 right angle is a right angle, 2 make a straight angle and 4 make a revolution. "
                   "3 right angles is between a straight angle and a revolution: reflex.", rnd))
    its.append(name_q("Two quarter turns make which angle?", "straight",
                      "2 quarter turns make a half turn. A half turn is a straight angle.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(turn_fig(0.75, False)) + "%s says this is a quarter turn because the end arm makes a right angle "
                   "with the dashed line. Is %s right?" % (n, he),
                   "No, it is a three-quarter turn: a reflex angle",
                   ["Yes, it is a quarter turn", "No, it is a half turn", "No, it is a full turn"],
                   "Follow the arrow: it goes three quarters of the way round. The small gap is a right angle, but the "
                   "turn is 3 right angles: a reflex angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Turns and right angles", "items": its}


# ------------------------------------------------------------ set 5: problems
def set_problems(rnd, P):
    its = []
    its.append(name_q("At 9 o’clock, what angle do the hands of an analog clock make?", "right",
                      "The minute hand points to 12 and the hour hand to 9. That is 3 hour marks apart: a square corner, "
                      "a right angle.", rnd))
    its.append(name_q("The minute hand turns from 12 to 6. What angle has it turned through?", "straight",
                      "From 12 to 6 is halfway round the clock: a half turn. That is a straight angle.", rnd))
    its.append(name_q("A spelling test starts at 9:00 am and ends at 9:45 am. The minute hand turns from 12 to 9. "
                      "What angle has it turned through?", "reflex",
                      "12 to 3, 3 to 6 and 6 to 9 is 3 right angles: a three-quarter turn. That is a reflex angle.", rnd))
    its.append(name_q("Recess starts at 11:00 am and ends at 11:20 am. The minute hand turns from 12 to 4. "
                      "What angle has it turned through?", "obtuse",
                      "12 to 3 is a right angle. 12 to 4 is a bit more, but less than 12 to 6 (a straight angle). So it is obtuse.", rnd))
    its.append(name_q("A class plays a 10-minute game. The minute hand turns from 12 to 2. What angle has it turned through?",
                      "acute", "12 to 2 is less than 12 to 3 (a right angle), so the angle is acute.", rnd))
    its.append(name_q("The minute hand turns for exactly one hour. What angle has it turned through?", "revolution",
                      "In one hour the minute hand goes all the way round once: a full turn, a revolution.", rnd))
    its.append(mcq("At which time do the hands of an analog clock make an obtuse angle?", "4 o’clock",
                   ["3 o’clock", "1 o’clock", "6 o’clock"],
                   "At 4 o’clock the hands are 4 hour marks apart: more than a right angle (3) and less than a straight "
                   "angle (6). 3 o’clock is a right angle, 1 o’clock is acute and 6 o’clock is straight.", rnd))
    its.append(mcq("At which time do the hands of an analog clock make an acute angle?", "2 o’clock",
                   ["3 o’clock", "5 o’clock", "6 o’clock"],
                   "At 2 o’clock the hands are 2 hour marks apart, less than a right angle (3). 5 o’clock is obtuse.", rnd))
    n, he, his = P.next()
    its.append(name_q("At the skate park, %s spins %s skateboard all the way round once, a “360”. "
                      "What angle has the board turned through?" % (n, his), "revolution",
                      "All the way round once is a full turn: a revolution.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s opens %s laptop until the screen stands straight up from the keyboard. "
                      "What angle do the screen and keyboard make?" % (n, his), "right",
                      "Straight up from a flat keyboard is a square corner: a right angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("At the beach, %s leans the back of %s deckchair back. It is wider than a square corner but not flat. "
                      "What angle do the seat and back make?" % (n, his), "obtuse",
                      "Wider than a right angle but less than a straight angle is obtuse.", rnd))
    n, he, his = P.next()
    its.append(name_q("On a school excursion, %s walks north, then turns right to walk east. What angle did %s turn through?"
                      % (n, he), "right", "North to east is a quarter turn clockwise: a right angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s faces the beach to the east. %s turns anticlockwise until %s faces south. What angle has %s turned through?"
                      % (n, cap(he), he, he), "reflex",
                      "Anticlockwise from east: north, west, south. That is 3 right angles, a reflex angle. "
                      "(Turning clockwise would only be 1 right angle.)", rnd))
    n, he, his = P.next()
    its.append(name_q("%s opens %s scissors a little to cut a ribbon. What kind of angle do the blades make?" % (n, his), "acute",
                      "A little open is less than a square corner, so the blades make an acute angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s’s family cuts a pizza into 4 equal slices. What kind of angle is at the tip of each slice?" % n,
                      "right", "4 equal slices are 4 quarter turns round the centre. A quarter turn is a right angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("A pizza is cut into 4 equal slices and %s eats 1. What kind of angle do the 3 slices left make at the centre?"
                      % n, "reflex", "3 quarter slices make 3 right angles. That is more than a straight angle: reflex.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s turns the garden tap on with a half turn. What angle does the handle turn through?" % n, "straight",
                      "A half turn is a straight angle: 2 right angles.", rnd))
    a, b = P.next(), P.next()
    its.append(mcq("%s and %s each cut a round pizza into 8 equal slices. %s’s pizza is much bigger, so %s slices have "
                   "longer sides. %s says the tip of %s slice is a bigger angle. Is %s right?"
                   % (a[0], b[0], b[0], b[2], b[0], b[2], b[1]),
                   "No, the tips are the same size", ["Yes, longer sides make a bigger angle",
                                                      "No, the smaller pizza’s slice has a bigger angle", "You cannot tell"],
                   "Both pizzas are cut into 8 equal slices, so each tip turns the same amount: half a right angle. "
                   "Longer sides do not change the angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s faces north. %s makes a quarter turn clockwise, then a half turn clockwise. "
                      "What angle has %s turned through altogether?" % (n, cap(he), he), "reflex",
                      "1 quarter turn + 2 quarter turns = 3 quarter turns: 3 right angles. That is a reflex angle.", rnd))
    n, he, his = P.next()
    n, he, his = P.next()
    its.append(name_q("%s opens the classroom door just a little, less than a square corner, to peek out. "
                      "What angle has the door opened?" % n, "acute",
                      "Less than a square corner (a right angle) is an acute angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angle problems in everyday life", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    kinds = strip_svg([angle_fig(40, 0, 55), angle_fig(90, 0, 55), angle_fig(130, 0, 55)],
                      ["acute", "right", "obtuse"], "acute, right and obtuse angles", cw=150)
    kinds2 = strip_svg([angle_fig(180, 0, 55), angle_fig(240, 0, 55), rev_fig(0, L=55)],
                       ["straight", "reflex", "revolution"], "straight angle, reflex angle and revolution", cw=150)
    turns = strip_svg([turn_fig(f) for f in (0.25, 0.5, 0.75, 1.0)], ["quarter", "half", "three-quarter", "full"],
                      "quarter, half, three-quarter and full turns clockwise", cw=124)
    same = strip_svg([angle_fig(55, 10, 86), angle_fig(55, 10, 34)], ["long arms", "short arms"],
                     "two angles of the same size with long and short arms", cw=130)
    return (
        "<h2>Compare every angle with a right angle</h2>"
        "<p>An angle is the amount of <b>turn</b> between two arms. A <b>right angle</b> is a square corner: a quarter turn. "
        "Use it to name every other angle. The arc shows which angle is meant.</p>"
        "<figure class='sn-fig'>" + kinds + "</figure>"
        "<figure class='sn-fig'>" + kinds2 +
        "<figcaption>A reflex angle goes round the outside. A revolution goes all the way round.</figcaption></figure>" +
        table(["Name", "Compared with a right angle"], [
            ["Acute angle", "less than 1 right angle"],
            ["Right angle", "exactly 1 right angle (a quarter turn)"],
            ["Obtuse angle", "between 1 and 2 right angles"],
            ["Straight angle", "exactly 2 right angles (a half turn)"],
            ["Reflex angle", "between 2 and 4 right angles"],
            ["Revolution", "exactly 4 right angles (a full turn)"],
        ]) +
        "<h2>Turns make angles</h2>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>Each turn starts at the dashed arm.</figcaption></figure>" +
        ex("Example", "Mia faces north. She turns clockwise until she faces west. What angle has she turned through?",
           "North to east, east to south, south to west: 3 right angles. That is more than a straight angle.", "a reflex angle") +
        ex("Example", "At 4 o’clock, what kind of angle do the clock hands make?",
           "A right angle is 3 hour marks (3 o’clock) and a straight angle is 6 (6 o’clock). 4 is between them.", "an obtuse angle") +
        "<h2>Compare two angles</h2>"
        "<p>Look at how far each angle turns. Is it less than, equal to or more than a right angle? A straight angle? "
        "The length of the arms does not matter.</p>"
        "<figure class='sn-fig'>" + same +
        "<figcaption>These two angles are the same size.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking longer arms make a bigger angle", "Look at the turn between the arms, not the arm length"],
            ["Calling a reflex angle obtuse", "Check the arc. If it goes round the outside, past a straight line, it is reflex"],
            ["Saying a straight line is “no angle”", "A half turn is an angle: a straight angle, 2 right angles"],
            ["Thinking a tilted right angle is not a right angle", "Turning an angle does not change its size or name"],
        ])
    )


FAQ = [
    {"q": "What are the angle names in Year 4 maths in Australia?",
     "a": "Acute (less than a right angle), right, obtuse (between a right angle and a straight angle), straight (2 right angles), reflex (between a straight angle and a revolution) and revolution (a full turn)."},
    {"q": "Do Year 4 students measure angles in degrees?",
     "a": "No. In Year 4 students estimate and compare angles with a right angle. Measuring in degrees with a protractor starts in Year 5."},
    {"q": "What is a reflex angle?",
     "a": "A reflex angle is greater than a straight angle (a half turn) but less than a revolution (a full turn). It is the angle on the outside of the arms."},
    {"q": "Why is a longer-armed angle not a bigger angle?",
     "a": "The size of an angle is the amount of turn between its arms. Making the arms longer or shorter does not change the turn."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) in every set. Fixed-order questions keep their order."""
    for s in sets:
        fixed = [it["a"] for it in s["items"] if it.get("fix")]
        targets = []
        for p in range(4):
            assert fixed.count(p) <= 5, (s["title"], fixed)
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
    rnd = random.Random(4815)
    P = People(rnd)
    sets = [set_names(rnd, P), set_compare(rnd, P), set_objects(rnd, P), set_turns(rnd, P), set_problems(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "comparing-angles", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Comparing Angles: Acute, Right, Obtuse, Straight, Reflex and Revolution",
        "seo_title": "Year 4 Angles Worksheets: Acute, Obtuse, Reflex and Straight Angles (Free, Australian Curriculum)",
        "short_title": "Comparing angles",
        "domain": "Measurement",
        "standard_code": "AC9M4M04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Estimate and compare angles using angle names including acute, obtuse, straight angle, reflex and "
                         "revolution, and recognise their relationship to a right angle",
        "meta_desc": "Free Year 4 maths worksheets on comparing angles: name acute, right, obtuse, straight and reflex angles "
                     "and a revolution, compare angles with a right angle, find angles in clocks, doors and shapes, and link "
                     "turns to right angles. 100 questions with an answer key, following the Australian Curriculum (AC9M4M04).",
        "key_big": "Compare every angle with a right angle: less is acute, more is obtuse, 2 right angles is straight.",
        "key_sub": "More than a straight angle is reflex, and a full turn (4 right angles) is a revolution. "
                   "The size of an angle is the turn between its arms, not the length of the arms.",
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
        mark_large(u, "(four angles labelled|angle P and angle Q|angles X, Y and Z|scissors P and Q)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
