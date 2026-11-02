# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Angles and rectangles
(Ontario Curriculum 2020, Grade 4: Spatial Sense, E2.4 and E1.1)
  python3 tools/gen_caon_math_g4_angles.py
Compare angles with a right angle (the corner of a sheet of paper), classify right, straight, acute and
obtuse angles, angles in shapes and real life (clock hands), parallel and perpendicular sides, and the
properties of rectangles and squares (right angles, parallel and perpendicular sides, lines of symmetry).
No degrees (that is Grade 5). Every angle is drawn exactly (trig, 0 = pointing right, counterclockwise,
SVG y goes down); every marked angle is measured back from the drawing and checked. Angles in pictures
that are not right or straight are at least 20 degrees away from them, so students can judge them.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]




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



def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D, turns, compass points, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fix": True}


def mcq_num(q, correct, e):
    return mcq_fixed(q, ["1", "2", "3", "4"], str(correct), e)


# ------------------------------------------------------------ Grade 4 figures (no degrees shown)
def judgeable(d):
    """Without a protractor, a picture must be clearly one kind: right and straight exactly,
    anything else at least 20° away from them (and at least 20°)."""
    assert d in (90, 180) or (20 <= d < 180 and abs(d - 90) >= 20 and abs(d - 180) >= 20), d


def angle_fig(d, rot=0, L=70, L2=None, label="marked angle"):
    """Two arms from O: one at rot, the other at rot + d (counterclockwise). The arc marks the angle d;
    a right angle gets the small square."""
    judgeable(d)
    P = Pic()
    A, B = pol(O, L, rot), pol(O, L2 or L, rot + d)
    P.line(O, A)
    P.line(O, B)
    if d == 90:
        P.mark(O, A, B, 90, kind="right", ccw=True)
    else:
        P.mark(O, A, B, d, r=(22 if d < 40 else 16), ccw=True)
    P.dot(O)
    return P.svg(label)


O = (0.0, 0.0)
PAPER = "#fbf3d0"
PAPER_EDGE = "#a8925a"


def paper_fig(d, rot=0, L=74, label="angle with the corner of a sheet of paper placed on it"):
    """The corner of a sheet of paper (a right angle) placed on the angle: one paper edge along the first arm."""
    judgeable(d)
    P = Pic()
    a, b = 50, 38
    c1 = pol(O, a, rot)
    paper = [O, c1, pol(c1, b, rot + 90), pol(O, b, rot + 90)]
    P.poly(paper, fill=PAPER, sw=1.6, col=PAPER_EDGE)
    A, B = pol(O, L, rot), pol(O, L, rot + d)
    P.line(O, A)
    P.line(O, B)
    if d == 90:
        P.mark(O, A, B, 90, kind="right", ccw=True)
    else:
        P.mark(O, A, B, d, r=(22 if d < 40 else 16), ccw=True)
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
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


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


def clock_svg(h, label=None):
    """Analog clock at h o’clock. The red arc marks the smaller angle between the minute hand (on 12)
    and the hour hand: 30° for every hour mark. Square picture."""
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
    sweep = 30 * min(h, 12 - h)
    sg = -1 if h <= 6 else 1
    n = max(6, sweep // 6)
    arc = [pol(c, 13, 90 + sg * sweep * i / n) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in arc), RED))
    hh, mh = pol(c, 19, 90 - 30 * h), pol(c, 27, 90)
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='60' y1='60' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='60' cy='60' r='4' fill='%s'/>" % INK)
    return svg_wrap(120, 120, "".join(s), label or "analog clock showing %d o’clock" % h)


def lines_pic(kind, rot=0, L=76, mark=False):
    """A pair of lines. 'par' parallel, 'meet' getting closer (they would meet), 'perp' crossing at a right
    angle, 'perpT' a T shape, 'perpL' a corner, 'cross' crossing at 55°."""
    P = Pic()
    if kind == "par":
        for k in (-15, 15):
            c = pol(O, k, rot + 90)
            P.line(pol(c, L / 2, rot + 180), pol(c, L / 2, rot))
    elif kind == "meet":
        for sg in (-1, 1):
            c = pol(O, sg * 18, rot + 90)
            dd = rot - sg * 10                     # the upper line slopes down, the lower line up: they close in
            P.line(pol(c, L / 2, dd + 180), pol(c, L / 2, dd))
    elif kind == "perp":
        P.line(pol(O, L / 2, rot + 180), pol(O, L / 2, rot))
        P.line(pol(O, L / 2, rot + 270), pol(O, L / 2, rot + 90))
        if mark:
            P.mark(O, pol(O, L / 2, rot), pol(O, L / 2, rot + 90), 90, kind="right", ccw=True)
    elif kind == "perpT":
        P.line(pol(O, L / 2, rot + 180), pol(O, L / 2, rot))
        P.line(O, pol(O, L * 0.6, rot + 90))
        if mark:
            P.mark(O, pol(O, L / 2, rot), pol(O, L / 2, rot + 90), 90, kind="right", ccw=True)
    elif kind == "perpL":
        P.line(O, pol(O, L * 0.75, rot))
        P.line(O, pol(O, L * 0.6, rot + 90))
        if mark:
            P.mark(O, pol(O, L / 2, rot), pol(O, L / 2, rot + 90), 90, kind="right", ccw=True)
    elif kind == "cross":
        P.line(pol(O, L / 2, rot + 180), pol(O, L / 2, rot))
        P.line(pol(O, L / 2, rot + 235), pol(O, L / 2, rot + 55))
    return P


def lines_svg(kind, rot=0, L=76, mark=False, label=None):
    return lines_pic(kind, rot, L, mark).svg(label or "two lines")


def lines_abcd(specs, label="four pairs of lines labelled A to D"):
    return strip_svg([lines_svg(k, r) for k, r in specs], ["A", "B", "C", "D"], label, fs=18)


def quad_svg(pts, label, letters=None, rights=None, dash=None, extra_dash=None, sw=3):
    """Polygon (screen coordinates). letters: vertex names placed outside each corner. rights: corners
    with a small square (default: every right-angled corner). dash: (p, q) a dashed red line, drawn a
    little past both ends."""
    P = Pic()
    P.poly(pts, sw=sw)
    A = poly_angles(pts)
    n = len(pts)
    if rights is None:
        rights = [i for i in range(n) if abs(A[i] - 90) < 1e-6]
    for i in rights:
        assert abs(A[i] - 90) < 1e-6
        P.mark(pts[i], pts[i - 1], pts[(i + 1) % n], 90, kind="right")
    for dl in [d for d in (dash, extra_dash) if d] if not isinstance(dash, list) else dash:
        p, q = dl
        dd = ang(p, q)
        P.line(pol(p, 10, dd + 180), pol(q, 10, dd), col=RED, sw=2.4, dash="6 4")
    if letters:
        cx = sum(p[0] for p in pts) / n
        cy = sum(p[1] for p in pts) / n
        for i, t in enumerate(letters):
            d = ang((cx, cy), pts[i])
            c = pol(pts[i], 14, d)
            P.label(c[0], c[1], t, fs=16)
    return P.svg(label)


def plain_svg(pts, label):
    P = Pic()
    P.poly(pts)
    return P.svg(label)


def rect(w, h):
    """Rectangle, corners from the top left going clockwise on screen: A B C D."""
    return [(0.0, 0.0), (float(w), 0.0), (float(w), float(h)), (0.0, float(h))]


RTRAP = [(0.0, 0.0), (80.0, 0.0), (130.0, 70.0), (0.0, 70.0)]
HOUSE = [(0.0, 26.0), (45.0, 0.0), (90.0, 26.0), (90.0, 86.0), (0.0, 86.0)]
PARA = [(26.0, 0.0), (116.0, 0.0), (90.0, 56.0), (0.0, 56.0)]
ITRAP = [(25.0, 0.0), (75.0, 0.0), (100.0, 56.0), (0.0, 56.0)]
KITE = [(36.0, 0.0), (72.0, 24.0), (36.0, 72.0), (0.0, 24.0)]
HEX = [pol(O, 50, 60 * i) for i in range(6)]
OBT = tri_pts(25, 35, base=150)            # angle C at the top is 120°
RTRI = tri_pts(90, 35, base=130)           # angle A at the bottom left is a right angle


# ------------------------------------------------------------ angle names
KINDS = ["acute", "right", "obtuse", "straight"]
NAMES = {"acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle"}
KIND_E = {
    "acute": "An acute angle is less than a right angle: narrower than the corner of a sheet of paper.",
    "right": "A right angle is a square corner, like the corner of a sheet of paper. The small square shows it.",
    "obtuse": "An obtuse angle is greater than a right angle but less than a straight angle.",
    "straight": "A straight angle is 2 right angles. The two arms make a straight line.",
}


def kind(d):
    return "acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight"


def name_q(q, k, e, rnd):
    return mcq(q, NAMES[k], [NAMES[w] for w in KINDS if w != k], e, rnd)


CMP = {"less": "less than a right angle", "equal": "equal to a right angle", "greater": "greater than a right angle"}


def cmp_q(q, d, e, rnd):
    k = "less" if d < 90 else "equal" if d == 90 else "greater"
    return mcq(q, CMP[k], [CMP[w] for w in ("less", "equal", "greater") if w != k] + ["equal to a straight angle"], e, rnd)


SAME = ["angle P", "angle Q", "They are the same size", "You cannot tell"]
NUMS = ["0", "1", "2", "4"]


# ------------------------------------------------------------ set 1: compare with a right angle
def set_compare(rnd, P):
    its = []
    q = "The corner of a sheet of paper is placed on the angle. How does the angle compare with a right angle?"
    for d, rot, e in [
        (45, 0, "The second arm is inside the paper corner. The angle is smaller than the corner, so it is less than a right angle."),
        (90, 0, "The second arm lies exactly along the edge of the paper. The angle fits the corner, so it is equal to a right angle."),
        (125, 0, "The second arm is outside the paper corner. The angle opens wider than the corner, so it is greater than a right angle."),
        (30, 20, "The second arm is well inside the paper corner, so the angle is less than a right angle."),
        (150, 10, "The second arm is far outside the paper corner, but the arms do not make a straight line. "
                  "The angle is greater than a right angle."),
        (90, 35, "The second arm lies along the edge of the paper. A tilted angle can still be a right angle."),
        (65, 200, "The second arm is inside the paper corner, so the angle is less than a right angle."),
        (110, 160, "The second arm is outside the paper corner, so the angle is greater than a right angle."),
    ]:
        its.append(cmp_q(fig(paper_fig(d, rot)) + q, d, e, rnd))
    q = "Which marked angle is larger?"
    for a, b, ans, e in [
        ((50, 15, 80), (120, 10, 34), "angle Q",
         "Angle Q is greater than a right angle and angle P is less. Q is larger, even though its arms are shorter."),
        ((140, 0, 34), (70, 20, 82), "angle P",
         "Angle P is greater than a right angle and angle Q is less. Long arms do not make an angle larger."),
        ((60, 10, 82), (60, 10, 34), "They are the same size",
         "Both angles open the same amount. Only the arms are different lengths, and arm length does not change an angle."),
        ((90, 0, 36), (90, 40, 76), "They are the same size",
         "Both are right angles (the small squares show it). Tilting an angle or making its arms longer does not change it."),
    ]:
        its.append(mcq_fixed(fig(pair_svg(a, b)) + q, SAME, ans, e))
    lab = "four angles labelled A to D"
    its.append(mcq_fixed(fig(abcd_svg([(50, 10, 66), (140, 0, 30), (90, 0, 52), (25, 10, 70)], lab)) +
                         "Which angle is greater than a right angle?", ["A", "B", "C", "D"], "B",
                         "B opens wider than a square corner. A and D are less than a right angle and C is a right angle. "
                         "B has the shortest arms, but arm length does not matter."))
    its.append(mcq_fixed(fig(abcd_svg([(130, 0, 66), (90, 0, 52), (35, 0, 30), (180, 0, 44)], lab)) +
                         "Which angle is less than a right angle?", ["A", "B", "C", "D"], "C",
                         "C is narrower than a square corner. A is greater than a right angle, B is a right angle and D is a "
                         "straight angle."))
    its.append(mcq_fixed(fig(abcd_svg([(70, 0, 60), (115, 0, 40), (90, 20, 30), (45, 0, 66)], lab)) +
                         "Which angle is equal to a right angle?", ["A", "B", "C", "D"], "C",
                         "C is a square corner: the small square shows it. It is tilted and has short arms, but it is still "
                         "a right angle. A and D are less, and B is greater."))
    trio = strip_svg([angle_fig(120, 10, 34), angle_fig(40, 10, 80), angle_fig(90, 0, 52)], ["X", "Y", "Z"],
                     "angles X, Y and Z", fs=18)
    its.append(mcq(fig(trio) + "Put the angles in order from smallest to largest.", "Y, Z, X",
                   ["X, Y, Z", "Y, X, Z", "Z, Y, X"],
                   "Y is less than a right angle, Z is a right angle and X is greater than a right angle. "
                   "Look at the opening, not the arm length.", rnd))
    its.append(mcq("Which of these has a corner that is a right angle?", "a page of your notebook",
                   ["the tip of a sharp pencil", "the point of a slice of pizza cut into 8", "a book lying open and flat"],
                   "The corner of a page is a square corner: a right angle. A pencil tip and a pizza slice tip are narrower "
                   "(acute), and a book lying flat makes a straight angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws two angles. Angle P has arms 10 cm long and angle Q has arms 3 cm long. %s says angle P "
                   "must be larger. Is %s right?" % (n, cap(he), he),
                   "No, arm length does not change the size of an angle",
                   ["Yes, longer arms make a larger angle", "Yes, angle P is 7 cm larger", "No, angle Q is always larger"],
                   "The size of an angle is how wide it opens between the arms. You cannot tell which is larger "
                   "from the arm lengths.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts the corner of a sheet of paper on an angle. The angle fits inside the corner and there is "
                   "space left over. How does the angle compare with a right angle?" % n,
                   CMP["less"], [CMP["equal"], CMP["greater"], "equal to a straight angle"],
                   "The angle is smaller than the paper corner, so it is less than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds a scrap of paper in half. Then %s folds it in half again, so the folded edge lies on top "
                   "of itself. What angle does the new folded corner make?" % (n, he),
                   NAMES["right"], [NAMES["acute"], NAMES["obtuse"], NAMES["straight"]],
                   "The first fold makes a straight edge: a straight angle. Folding it in half splits the straight angle "
                   "into 2 equal parts. Half of a straight angle is a right angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare angles with a right angle", "items": its}


# ------------------------------------------------------------ set 2: classify angles
def set_classify(rnd, P):
    its = []
    q = "What kind of angle is marked?"
    for d, rot, L in [(40, 10, 70), (90, 30, 64), (130, 0, 60), (180, 0, 60), (60, 110, 74), (150, 200, 58),
                      (180, 60, 60), (115, 40, 66), (25, 0, 72), (90, 200, 60)]:
        k = kind(d)
        e = KIND_E[k]
        if rot and d in (90, 180):
            e += " Turning the angle does not change its name."
        its.append(name_q(fig(angle_fig(d, rot, L)) + q, k, e, rnd))
    its.append(name_q("An angle is less than a right angle. What kind of angle is it?", "acute",
                      "An acute angle is less than a right angle. An obtuse angle is greater than a right angle.", rnd))
    its.append(name_q("An angle is greater than a right angle but less than a straight angle. What kind of angle is it?",
                      "obtuse", "Between a right angle and a straight angle is an obtuse angle.", rnd))
    its.append(name_q("The two arms of an angle make a straight line. What kind of angle is it?", "straight",
                      "When the arms point in opposite directions and make a straight line, the angle is a straight angle.", rnd))
    its.append(name_q("Which angle is a square corner, exactly a quarter turn?", "right",
                      "A right angle is a square corner. It is a quarter of a full turn.", rnd))
    its.append(mcq_fixed("How many right angles make a straight angle?", ["1", "2", "3", "4"], "2",
                         "Put 2 square corners side by side. Together their outside arms make a straight line."))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(180, 15, 62)) + "%s says there is no angle here because the arms make a straight line. "
                   "Is %s right?" % (n, he),
                   "No, it is a straight angle", ["Yes, a straight line is not an angle", "No, it is a right angle",
                                                  "No, it is an obtuse angle"],
                   "The two arms meet at the dot and point in opposite directions. That is an angle: a straight angle "
                   "(2 right angles).", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(90, 45, 62)) + "%s says this is not a right angle because it is tilted. Is %s right?" % (n, he),
                   "No, it is a right angle", ["Yes, it is an acute angle", "Yes, it is an obtuse angle",
                                               "Yes, right angles must have a flat arm"],
                   "The small square shows a square corner. Turning an angle does not change its size or its name.", rnd))
    its.append(mcq("Which list goes from the smallest angle to the largest?", "acute, right, obtuse, straight",
                   ["acute, obtuse, right, straight", "right, acute, obtuse, straight", "acute, right, straight, obtuse"],
                   "Acute is less than a right angle. Obtuse is between a right angle and a straight angle, "
                   "and a straight angle is 2 right angles.", rnd))
    lab = "four angles labelled A to D"
    its.append(mcq_fixed(fig(abcd_svg([(160, 0, 52), (90, 0, 52), (45, 0, 60), (125, 0, 30)], lab)) +
                         "Which angle is acute?", ["A", "B", "C", "D"], "C",
                         "C is the only angle less than a right angle. A and D are obtuse and B is a right angle."))
    its.append(mcq_fixed(fig(abcd_svg([(150, 0, 52), (90, 0, 52), (40, 0, 60), (180, 20, 44)], lab)) +
                         "Which angle is a straight angle?", ["A", "B", "C", "D"], "D",
                         "In D the two arms make a straight line. A is obtuse: close to a straight angle, but less."))
    assert len(its) == 20, len(its)
    return {"title": "Right, straight, acute and obtuse angles", "items": its}


# ------------------------------------------------------------ set 3: angles in shapes and real life
def set_real(rnd, P):
    its = []
    q = "What kind of angle do the clock hands make?"
    for h, e in [(3, "At 3 o’clock the hands make a square corner: a right angle."),
                 (2, "The hands are 2 hour marks apart. A right angle is 3 hour marks (like 3 o’clock), so this is less: acute."),
                 (4, "The hands are 4 hour marks apart. That is more than 3 (a right angle) and less than 6 "
                     "(a straight angle): obtuse."),
                 (6, "At 6 o’clock the hands point in opposite directions. They make a straight line: a straight angle."),
                 (9, "From 9 to 12 is 3 hour marks, the same as 12 to 3. The hands make a square corner: a right angle."),
                 (10, "From 10 to 12 is only 2 hour marks, less than 3. The angle is acute."),
                 (5, "From 12 to 5 is 5 hour marks: more than 3 (a right angle) but less than 6 (a straight angle). "
                     "The angle is obtuse.")]:
        its.append(name_q(fig(clock_svg(h)) + q, kind(30 * min(h, 12 - h)), e, rnd))
    q = "This door is seen from above. It opened from the dashed line. What kind of angle has it opened?"
    its.append(name_q(fig(door_svg(60)) + q, "acute",
                      "The door has opened less than a square corner, so the angle is acute.", rnd))
    its.append(name_q(fig(door_svg(130)) + q, "obtuse",
                      "The door has opened past a square corner but not to a straight line, so the angle is obtuse.", rnd))
    its.append(name_q(fig(scissors_svg(40)) + "What kind of angle do the blades of these scissors make?", "acute",
                      "The blades open less than a square corner, so the angle is acute.", rnd))
    its.append(name_q(fig(laptop_svg(115)) + "This laptop is seen from the side. What kind of angle does the screen make "
                      "with the keyboard?", "obtuse",
                      "The screen leans back past a square corner, but it is not flat. That is an obtuse angle.", rnd))
    its.append(mcq_fixed(fig(shape_svg(OBT, {0: "A", 1: "B", 2: "C"}, "triangle with angles A, B and C")) +
                         "Which angle in this triangle is obtuse?", ["angle A", "angle B", "angle C", "none of them"],
                         "angle C", "Angle C at the top opens wider than a right angle, so it is obtuse. A and B are acute."))
    its.append(mcq_fixed(fig(shape_svg(RTRI, {0: "A", 1: "B", 2: "C"}, "triangle with angles A, B and C")) +
                         "Which angle in this triangle is a right angle?", ["angle A", "angle B", "angle C", "none of them"],
                         "angle A", "Angle A is a square corner: one arm goes straight across and the other goes straight up. "
                         "B and C are acute."))
    hx = concave_svg(HEX, [0], "hexagon with equal sides and one angle marked")
    its.append(name_q(fig(hx) + "What kind of angle is marked inside this hexagon?", "obtuse",
                      "Each corner of this hexagon is wider than a square corner but less than a straight line: obtuse.", rnd))
    its.append(mcq_fixed(fig(plain_svg(RTRAP, "four-sided shape")) + "How many right angles does this shape have?",
                         ["0", "1", "2", "3"], "2",
                         "The two corners on the left side are square corners. The top right corner is obtuse and the "
                         "bottom right corner is acute."))
    its.append(mcq_fixed(fig(plain_svg(HOUSE, "house shape with 5 sides")) + "How many right angles does this house shape have?",
                         ["0", "1", "2", "3"], "2",
                         "The 2 corners at the bottom, where the walls meet the floor, are right angles. "
                         "The 3 corners of the roof are obtuse."))
    its.append(mcq("At which time do the hands of an analog clock make a straight angle?", "6 o’clock",
                   ["3 o’clock", "9 o’clock", "5 o’clock"],
                   "At 6 o’clock the minute hand points to 12 and the hour hand points to 6, the opposite way. "
                   "At 3 o’clock and 9 o’clock the hands make right angles.", rnd))
    its.append(name_q("A pizza is cut into 8 equal slices. What kind of angle is at the tip of one slice?", "acute",
                      "2 slices make a quarter of the pizza: a right angle. One slice is half of that, so it is acute.", rnd))
    its.append(name_q("A pizza is cut into 4 equal slices. What kind of angle is at the tip of each slice?", "right",
                      "4 equal slices fit round the centre. Each one is a quarter turn: a right angle.", rnd))
    n, he, his = P.next()
    its.append(name_q("%s opens a book and lays it flat on the table. What angle do the two covers make?" % n, "straight",
                      "When the book lies flat, the covers make a straight line: a straight angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in shapes and real life (clock hands)", "items": its}


# ------------------------------------------------------------ set 4: parallel and perpendicular
def set_lines(rnd, P):
    its = []
    its.append(mcq_fixed(fig(lines_abcd([("cross", 10), ("par", 0), ("perp", 0), ("meet", 0)])) +
                         "Which pair of lines is parallel?", ["A", "B", "C", "D"], "B",
                         "In B the lines stay the same distance apart and never meet. The lines in D get closer and would meet."))
    its.append(mcq_fixed(fig(lines_abcd([("perpT", 0), ("meet", 90), ("cross", 0), ("par", 60)])) +
                         "Which pair of lines is parallel?", ["A", "B", "C", "D"], "D",
                         "In D the slanted lines stay the same distance apart: they are parallel. Parallel lines do not "
                         "have to be flat."))
    its.append(mcq_fixed(fig(lines_abcd([("perp", 0), ("cross", 20), ("par", 90), ("meet", 30)])) +
                         "Which pair of lines is perpendicular?", ["A", "B", "C", "D"], "A",
                         "In A the lines cross and make 4 square corners. In B they cross, but not at a right angle."))
    its.append(mcq_fixed(fig(lines_abcd([("par", 0), ("cross", 0), ("perpL", 25), ("meet", 0)])) +
                         "Which pair of lines is perpendicular?", ["A", "B", "C", "D"], "C",
                         "In C the lines meet at a square corner, so they are perpendicular. A tilted corner can still be "
                         "a right angle."))
    its.append(mcq("What are parallel lines?", "lines that stay the same distance apart and never meet",
                   ["lines that meet at a right angle", "lines that are both horizontal", "lines that cross each other"],
                   "Parallel lines always stay the same distance apart, like the two rails of a train track.", rnd))
    its.append(mcq("What are perpendicular lines?", "lines that meet at a right angle",
                   ["lines that never meet", "lines that meet at any angle", "lines that are the same length"],
                   "Perpendicular lines meet or cross at a right angle, like the two edges at the corner of a page.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(lines_svg("meet", 0, 120, label="two lines that get closer")) +
                   "%s says these lines are parallel because they do not touch. Is %s right?" % (n, he),
                   "No, they get closer and would meet",
                   ["Yes, lines that do not touch are parallel", "No, they are perpendicular", "Yes, they are both flat"],
                   "Parallel lines stay the same distance apart. These lines get closer to the right, so they would meet "
                   "if they were longer.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(lines_svg("par", 40, 90, label="two slanted lines")) +
                   "%s says these lines cannot be parallel because they are slanted. Is %s right?" % (n, he),
                   "No, they are parallel", ["Yes, parallel lines must be flat", "No, they are perpendicular",
                                             "Yes, slanted lines always meet"],
                   "The lines stay the same distance apart all the way along, so they are parallel. "
                   "Parallel lines can point in any direction.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(lines_svg("perp", 30, 90, mark=True, label="two lines crossing at a right angle")) +
                   "%s says these lines are not perpendicular because neither line is straight up and down. Is %s right?"
                   % (n, he),
                   "No, they meet at a right angle, so they are perpendicular",
                   ["Yes, one line must be straight up and down", "No, they are parallel", "Yes, they are not touching"],
                   "Any two lines that meet at a right angle are perpendicular, even when both are tilted.", rnd))
    its.append(name_q("Two perpendicular lines cross. What kind of angles do they make?", "right",
                      "Perpendicular lines meet at right angles. When they cross, they make 4 right angles.", rnd))
    sq = rect(130, 76)
    its.append(mcq_fixed(fig(quad_svg(sq, "rectangle ABCD", letters="ABCD")) +
                         "In rectangle ABCD, which side is parallel to side AB?", ["side BC", "side CD", "side AD", "no side"],
                         "side CD", "Side AB is the top and side CD is the bottom. They stay the same distance apart, "
                         "so they are parallel. BC and AD meet AB at right angles."))
    its.append(mcq_fixed(fig(quad_svg(sq, "rectangle ABCD", letters="ABCD", rights=[])) +
                         "In rectangle ABCD, how many sides are perpendicular to side AB?", ["0", "1", "2", "3"], "2",
                         "Sides AD and BC each meet side AB at a right angle, so 2 sides are perpendicular to it. "
                         "Side CD is parallel to AB."))
    its.append(mcq_fixed(fig(quad_svg(RTRAP, "trapezoid ABCD", letters="ABCD")) +
                         "Which side of this trapezoid is parallel to side AB?", ["side BC", "side CD", "side AD", "no side"],
                         "side CD", "The top AB and the bottom CD stay the same distance apart. Side BC is slanted and "
                         "side AD is perpendicular to AB."))
    its.append(mcq_fixed(fig(quad_svg(ITRAP, "trapezoid", rights=[])) + "How many pairs of parallel sides does this trapezoid have?",
                         ["0", "1", "2", "4"], "1",
                         "Only the top and the bottom are parallel. The two slanted sides get closer at the top, so they "
                         "would meet."))
    its.append(mcq_fixed("How many pairs of parallel sides does a rectangle have?", ["0", "1", "2", "4"], "2",
                         "The top and bottom are one pair. The left and right sides are another pair. That is 2 pairs."))
    its.append(mcq("Which capital letter has a pair of parallel lines?", "H", ["V", "T", "L"],
                   "The two upright lines of H stay the same distance apart. T and L have lines that meet, and the lines "
                   "of V meet at the bottom.", rnd))
    its.append(mcq("Which capital letter is made of 2 perpendicular lines?", "L", ["V", "X", "H"],
                   "The two lines of L meet at a square corner. The lines of V and X meet at angles that are not right "
                   "angles, and H has 3 lines.", rnd))
    its.append(mcq("Which pair is parallel?", "the two rails of a train track",
                   ["the two hands of a clock at 3 o’clock", "the two blades of open scissors",
                    "a flagpole and the flat ground"],
                   "Train rails stay the same distance apart so the wheels fit. The clock hands at 3 o’clock and the "
                   "flagpole and ground are perpendicular.", rnd))
    its.append(mcq("Which pair is perpendicular?", "a flagpole and the flat ground",
                   ["the two rails of a train track", "the lines on lined paper", "the top and bottom edges of a door"],
                   "A flagpole stands straight up, so it meets the flat ground at a right angle. The other pairs are parallel.", rnd))
    its.append(mcq("The two blue lines on a hockey rink go straight across the ice from one side to the other. They are "
                   "always the same distance apart. How are the blue lines?", "parallel",
                   ["perpendicular", "they would meet", "they make a right angle"],
                   "Lines that stay the same distance apart and never meet are parallel.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallel and perpendicular sides", "items": its}


# ------------------------------------------------------------ set 5: rectangles and squares
def set_rects(rnd, P):
    its = []
    R = rect(124, 66)
    S = rect(76, 76)
    q = "Is the dashed line a line of symmetry?"
    its.append(mcq(fig(quad_svg(R, "rectangle with a dashed line across the middle", dash=((0.0, 33.0), (124.0, 33.0)))) + q,
                   "Yes, the two halves match when you fold on it",
                   ["No, the halves are different sizes", "No, only slanted lines can be lines of symmetry",
                    "No, a rectangle has no lines of symmetry"],
                   "Fold the rectangle on the dashed line. The top half lands exactly on the bottom half.", rnd))
    its.append(mcq(fig(quad_svg(R, "rectangle with a dashed diagonal line", dash=((0.0, 0.0), (124.0, 66.0)))) + q,
                   "No, the halves do not match when you fold on it",
                   ["Yes, it cuts the rectangle into 2 equal triangles", "Yes, every diagonal is a line of symmetry",
                    "Yes, it goes from corner to corner"],
                   "The 2 triangles are the same size, but if you fold on the diagonal, the corners stick out and do not "
                   "match. A diagonal of a rectangle that is not a square is not a line of symmetry.", rnd))
    its.append(mcq(fig(quad_svg(S, "square with a dashed diagonal line", dash=((0.0, 0.0), (76.0, 76.0)))) + q,
                   "Yes, the two halves match when you fold on it",
                   ["No, diagonals are never lines of symmetry", "No, the halves are different sizes",
                    "No, a square has only 2 lines of symmetry"],
                   "All 4 sides of a square are equal, so folding on a diagonal makes the two halves match exactly.", rnd))
    its.append(mcq_fixed("How many lines of symmetry does a rectangle that is not a square have?", NUMS, "2",
                         "One line goes across the middle and one goes up and down the middle. The diagonals are not "
                         "lines of symmetry."))
    its.append(mcq_fixed("How many lines of symmetry does a square have?", NUMS, "4",
                         "A square has 2 lines through the middles of the sides and 2 diagonals: 4 lines of symmetry."))
    its.append(mcq_fixed("How many right angles does a rectangle have?", ["1", "2", "3", "4"], "4",
                         "Every corner of a rectangle is a square corner, so a rectangle has 4 right angles."))
    its.append(mcq("Which is true for every rectangle?", "It has 4 right angles and 2 pairs of parallel sides",
                   ["All 4 sides are the same length", "It has 4 lines of symmetry", "It has only 1 pair of parallel sides"],
                   "Every rectangle has 4 right angles, and its opposite sides are parallel. Only squares have 4 equal sides "
                   "and 4 lines of symmetry.", rnd))
    its.append(mcq("Is a square a rectangle?", "Yes, it has 4 right angles and opposite sides parallel",
                   ["No, a rectangle must have 2 long sides and 2 short sides", "No, a square has no right angles",
                    "No, a square has no parallel sides"],
                   "A rectangle is a shape with 4 sides and 4 right angles. A square has all of that, so it is a special "
                   "rectangle with 4 equal sides.", rnd))
    pos = [1, 3]
    shapes = [quad_svg(PARA, "parallelogram", rights=[]), quad_svg(rect(96, 56), "rectangle"),
              quad_svg(ITRAP, "trapezoid", rights=[]), quad_svg(KITE, "kite", rights=[])]
    p = pos[0]
    order = [shapes[0], shapes[2], shapes[3]]
    order.insert(p, shapes[1])
    its.append(mcq_fixed(fig(strip_svg(order, ["A", "B", "C", "D"], "four shapes labelled A to D", fs=18)) +
                         "Which shape is a rectangle?", ["A", "B", "C", "D"], "ABCD"[p],
                         "Shape %s has 4 right angles (the small squares show them). Shape A leans over like a pushed "
                         "box: its sides are parallel, but its corners are not right angles." % "ABCD"[p]))
    cand = [quad_svg(S, "square", dash=((0.0, 0.0), (76.0, 76.0))),
            quad_svg(rect(110, 58), "rectangle", dash=((0.0, 0.0), (110.0, 58.0))),
            quad_svg(rect(110, 58), "rectangle", dash=((40.0, 0.0), (40.0, 58.0))),
            quad_svg(PARA, "parallelogram", rights=[], dash=((58.0, 0.0), (58.0, 56.0)))]
    p = pos[1]
    order = cand[1:]
    order.insert(p, cand[0])
    its.append(mcq_fixed(fig(strip_svg(order, ["A", "B", "C", "D"], "four shapes with dashed lines labelled A to D", fs=18)) +
                         "In which shape is the dashed line a line of symmetry?", ["A", "B", "C", "D"], "ABCD"[p],
                         "Only the square folds exactly onto itself along its diagonal. The rectangle’s diagonal does not "
                         "work, the line that is not in the middle makes 2 different parts, and the slanted shape does not "
                         "match when folded."))
    its.append(mcq_fixed("The flag of Canada is a rectangle. It has a red band on each side and a red maple leaf in the "
                         "middle. How many lines of symmetry does the flag have?", NUMS, "1",
                         "Fold the flag down the middle from top to bottom: the left and right halves match. Folding across "
                         "the middle does not work, because the maple leaf is not the same at the top and the bottom."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s folds a sheet of Letter paper (about 28 cm by 22 cm). In how many different ways can %s fold it "
                         "so the two halves match exactly?" % (n, he), NUMS, "2",
                         "Letter paper is a rectangle that is not a square. It folds in half across the middle and "
                         "up and down the middle. Folding on a diagonal does not work."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s cuts out a square of paper to make an origami card. In how many different ways can %s fold it "
                         "so the two halves match exactly?" % (n, he), NUMS, "4",
                         "A square has 4 lines of symmetry: across the middle, up and down the middle, and the 2 diagonals."))
    n, he, his = P.next()
    its.append(mcq("%s checks that a picture frame is a rectangle. What should %s check at each corner?" % (n, he),
                   "that it is a right angle", ["that it is an acute angle", "that it is an obtuse angle",
                                                "that it is a straight angle"],
                   "A rectangle has 4 right angles. %s can check each corner with the corner of a sheet of paper." % n, rnd))
    n, he, his = P.next()
    its.append(mcq("%s builds a garden bed with 2 sides 2 m long and 2 sides 1 m long. The corners are not right angles. "
                   "Is the garden bed a rectangle?" % n, "No, a rectangle needs 4 right angles",
                   ["Yes, opposite sides are the same length", "Yes, it has 4 sides", "No, a rectangle needs 4 equal sides"],
                   "Equal opposite sides are not enough. A rectangle must have 4 right angles.", rnd))
    n, he, his = P.next()
    its.append(name_q("A soccer field is a rectangle. %s runs along the side of the field, then turns at the corner flag to "
                      "run along the goal line. What angle do the side line and the goal line make?" % n, "right",
                      "The corners of a rectangle are right angles, so the side line and the goal line meet at a right angle.", rnd))
    its.append(mcq("A classroom window is a rectangle 120 cm wide and 80 cm tall. Which of its sides are parallel?",
                   "the top and bottom, and the left and right sides",
                   ["only the top and bottom", "the top and the left side", "no sides are parallel"],
                   "A rectangle has 2 pairs of parallel sides: the top and bottom, and the left and right sides.", rnd))
    its.append(mcq("A door is a rectangle. How do the side edge and the bottom edge of the door meet?",
                   "They are perpendicular: they make a right angle",
                   ["They are parallel", "They make an acute angle", "They make a straight angle"],
                   "Sides of a rectangle that meet at a corner make a right angle, so they are perpendicular.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a shape with 4 sides. Every corner is a right angle and all 4 sides are 5 cm long. "
                   "What is the best name for the shape?" % n, "a square",
                   ["a trapezoid", "a kite with slanted sides", "a triangle"],
                   "4 right angles and 4 equal sides make a square.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says a rectangle has 4 lines of symmetry because it has 4 sides. Is %s right?" % (n, he),
                   "No, a rectangle that is not a square has 2 lines of symmetry",
                   ["Yes, every shape with 4 sides has 4", "No, a rectangle has no lines of symmetry",
                    "No, a rectangle has 1 line of symmetry"],
                   "Only the lines across the middle and up and down the middle fold a rectangle into matching halves. "
                   "The diagonals do not.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rectangles and squares: right angles and symmetry", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    paper = strip_svg([paper_fig(50), paper_fig(90), paper_fig(130)],
                      ["less", "equal", "greater"], "angles compared with the corner of a sheet of paper", cw=140)
    kinds = strip_svg([angle_fig(40, 0, 55), angle_fig(90, 0, 55), angle_fig(130, 0, 55), angle_fig(180, 0, 50)],
                      ["acute", "right", "obtuse", "straight"], "acute, right, obtuse and straight angles", cw=124)
    lines = strip_svg([lines_svg("par", 0, 80), lines_svg("perp", 0, 80, mark=True), lines_svg("meet", 0, 80)],
                      ["parallel", "perpendicular", "neither"], "parallel lines, perpendicular lines and lines that would meet",
                      cw=130)
    rects = strip_svg([quad_svg(rect(110, 62), "rectangle", dash=[((55.0, 0.0), (55.0, 62.0)), ((0.0, 31.0), (110.0, 31.0))]),
                       quad_svg(rect(72, 72), "square", dash=[((36.0, 0.0), (36.0, 72.0)), ((0.0, 36.0), (72.0, 36.0)),
                                                              ((0.0, 0.0), (72.0, 72.0)), ((72.0, 0.0), (0.0, 72.0))])],
                      ["rectangle: 2 lines", "square: 4 lines"], "lines of symmetry of a rectangle and a square", cw=190)
    same = strip_svg([angle_fig(55, 10, 86), angle_fig(55, 10, 34)], ["long arms", "short arms"],
                     "two angles of the same size with long and short arms", cw=130)
    return (
        "<h2>Compare every angle with a right angle</h2>"
        "<p>An angle is made by two arms that meet at a point. A <b>right angle</b> is a square corner, like the corner "
        "of a sheet of paper. Put the corner of the paper on the angle to compare.</p>"
        "<figure class='sn-fig'>" + paper +
        "<figcaption>Inside the corner: less. Along the edge: equal. Outside the corner: greater.</figcaption></figure>"
        "<h2>Four kinds of angles</h2>"
        "<figure class='sn-fig'>" + kinds + "</figure>" +
        table(["Name", "Compared with a right angle"], [
            ["Acute angle", "less than a right angle"],
            ["Right angle", "exactly a square corner (the small square shows it)"],
            ["Obtuse angle", "greater than a right angle, less than a straight angle"],
            ["Straight angle", "2 right angles: the arms make a straight line"],
        ]) +
        ex("Example", "At 4 o’clock, what kind of angle do the clock hands make?",
           "A right angle is 3 hour marks (3 o’clock) and a straight angle is 6 (6 o’clock). 4 is between them.",
           "an obtuse angle") +
        "<p>The length of the arms does not matter. These two angles are the same size.</p>"
        "<figure class='sn-fig'>" + same + "</figure>"
        "<h2>Parallel and perpendicular</h2>"
        "<p><b>Parallel</b> lines stay the same distance apart and never meet, like train rails. "
        "<b>Perpendicular</b> lines meet at a right angle, like the edges at the corner of a page.</p>"
        "<figure class='sn-fig'>" + lines + "</figure>"
        "<h2>Rectangles and squares</h2>"
        "<p>A <b>rectangle</b> has 4 right angles. Its opposite sides are parallel, and sides that meet at a corner are "
        "perpendicular. A <b>square</b> is a rectangle with 4 equal sides.</p>"
        "<figure class='sn-fig'>" + rects +
        "<figcaption>A line of symmetry folds the shape into 2 matching halves.</figcaption></figure>" +
        ex("Example", "Is the diagonal of a rectangle 12 cm long and 6 cm wide a line of symmetry?",
           "Fold on the diagonal: the corners stick out past each other, so the halves do not match.",
           "no (only a square’s diagonals are lines of symmetry)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking longer arms make a bigger angle", "Look at how wide the angle opens, not the arm length"],
            ["Thinking a tilted right angle is not a right angle", "Turning an angle does not change its size or name"],
            ["Saying a straight line is “no angle”", "Two arms in a straight line make a straight angle: 2 right angles"],
            ["Calling lines parallel because they do not touch yet", "Parallel lines stay the same distance apart all the way"],
            ["Counting the diagonals of a rectangle as lines of symmetry", "Fold to check: a rectangle has 2 lines, a square has 4"],
        ])
    )


FAQ = [
    {"q": "What angles do Grade 4 students learn in the Ontario math curriculum?",
     "a": "Grade 4 students identify right, straight, acute and obtuse angles by comparing them with a right angle. "
          "Measuring angles in degrees with a protractor comes in Grade 5."},
    {"q": "How can my child check if an angle is a right angle at home?",
     "a": "Use the corner of a sheet of paper or a book. If the angle fits the corner exactly, it is a right angle; "
          "if it fits inside, it is acute; if it opens wider, it is obtuse."},
    {"q": "What is the difference between parallel and perpendicular lines?",
     "a": "Parallel lines stay the same distance apart and never meet. Perpendicular lines meet or cross at a right angle."},
    {"q": "How many lines of symmetry does a rectangle have?",
     "a": "A rectangle that is not a square has 2 lines of symmetry, through the middles of opposite sides. "
          "A square has 4, because its diagonals are lines of symmetry too."},
]


def gen():
    rnd = random.Random(44813)
    P = People(rnd)
    sets = [set_compare(rnd, P), set_classify(rnd, P), set_real(rnd, P), set_lines(rnd, P), set_rects(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "angles-and-rectangles", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Angles and Rectangles: Right, Acute, Obtuse and Straight Angles, Parallel and Perpendicular Sides",
        "seo_title": "Grade 4 Angles Worksheets: Acute, Obtuse, Parallel and Perpendicular (Free, Ontario Math)",
        "short_title": "Angles and rectangles",
        "domain": "Spatial Sense",
        "standard_code": "Grade 4: E2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify angles and classify them as right, straight, acute, or obtuse",
        "meta_desc": "Free Grade 4 math worksheets on angles and rectangles for the Ontario curriculum: compare angles with "
                     "a right angle, classify right, straight, acute and obtuse angles, find angles in clocks and shapes, "
                     "spot parallel and perpendicular sides, and find lines of symmetry. 100 questions with an answer key.",
        "key_big": "Compare every angle with a right angle: less is acute, more is obtuse, 2 right angles is straight.",
        "key_sub": "A rectangle has 4 right angles, 2 pairs of parallel sides and 2 lines of symmetry (a square has 4). "
                   "The size of an angle is how wide it opens, not the length of its arms.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(four angles labelled|angle P and angle Q|angles X, Y and Z|four pairs of lines|four shapes)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
