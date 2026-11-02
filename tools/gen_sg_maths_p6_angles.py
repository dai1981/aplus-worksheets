# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Angles in Composite Figures (MOE 2021 Primary Mathematics Syllabus, Standard)
  python tools/gen_sg_maths_p6_angles.py
HTML attributes use single quotes (no backslashes in the JSON).

Angle facts used (no extra lines are ever constructed):
  straight line 180°, at a point 360°, vertically opposite angles are equal, triangle 180°,
  isosceles triangle: the angles opposite the equal sides are equal, equilateral triangle: 60° each,
  parallelogram / rhombus: opposite angles equal, angles next to each other add up to 180°,
  trapezium: the two angles between the parallel sides add up to 180°.
Every figure is drawn to its stated angles: each marked angle is measured from the drawing
and checked against its value. Labels are checked so that they do not touch a line, an arc or another label.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


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

def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5/5/5/5)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t

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


# ============================================================ Singapore unit
def D(v):
    """Angle in degrees as text: 65°."""
    if abs(v - round(v)) < 1e-9:
        return "%d°" % int(round(v))
    return "%.1f°" % v


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def meet(P, a, Q, b):
    """Where the line through P in direction a meets the line through Q in direction b."""
    d1, d2 = pol(O, 1, a), pol(O, 1, b)
    den = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((Q[0] - P[0]) * d2[1] - (Q[1] - P[1]) * d2[0]) / den
    return (P[0] + t * d1[0], P[1] + t * d1[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def subp(p, q):
    return (p[0] - q[0], p[1] - q[1])


class Fig(Pic):
    """Pic with vertex letters (placed outside, in the widest gap between the lines at that point)
    and arrow marks for parallel sides."""

    def __init__(self):
        Pic.__init__(self)
        self.vtodo = []
        self.arcs = []

    def arrow(self, p, q, n=1, at=0.5):
        d = ang(p, q)
        m = (p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at)
        for j in range(n):
            tip = pol(m, (j - (n - 1) / 2.0) * 7 + 4, d)
            self.polyline([pol(tip, 8, d + 150), tip, pol(tip, 8, d - 150)], INK, 2)

    def mark(self, V, P, Q, val, text=None, **kw):
        a, b = ang(V, P), ang(V, Q)
        s = (b - a) % 360
        if s > 180:
            a, s = b, 360 - s
        self.arcs.append((V, a + 0.5, s - 1))
        Pic.mark(self, V, P, Q, val, text, **kw)

    def vletter(self, V, t):
        self.vtodo.append((V, t))

    def _letter(self, V, t):
        dirs = []
        for p, q in self.segs:
            if dist(p, V) < 1e-6:
                dirs.append(ang(V, q))
            elif dist(q, V) < 1e-6:
                dirs.append(ang(V, p))
            elif abs(dist(p, V) + dist(V, q) - dist(p, q)) < 1e-6:
                dirs += [ang(V, p), ang(V, q)]
        dirs = sorted(set(round(d % 360, 6) for d in dirs))
        n = len(dirs)
        gaps = [(dirs[i], (dirs[(i + 1) % n] - dirs[i]) % 360 or 360) for i in range(n)] if n else [(0, 360)]
        def marked(g):
            return any(dist(V, W) < 1e-6 and ((a - g[0]) % 360 < g[1] - 1e-6 or (a + s - g[0]) % 360 < g[1] - 1e-6)
                       for W, a, s in self.arcs)
        gaps.sort(key=lambda g: (marked(g), -g[1]))
        for a0, s in gaps:
            for r in range(10, 36):
                for off in (0, 0.12, -0.12, 0.24, -0.24, 0.36, -0.36):
                    c = pol(V, r, a0 + s / 2 + off * s)
                    b = self.box_of(c[0], c[1], t, 16)
                    if self.clear(b, 2.5):
                        self.label(c[0], c[1], t, 16, INK, check=False)
                        return
        raise AssertionError("no room for letter " + t)

    def svg(self, label, pad=5):
        for item in sorted(self.todo, key=lambda t: -t[2]):
            self.place(*item)
        self.todo = []
        for V, t in self.vtodo:
            self._letter(V, t)
        self.vtodo = []
        return Pic.svg(self, label, pad)


def fg(pts, segs, marks=(), rights=(), ticks=(), arrows=(), fills=(), hide=(), label="figure", sw=3):
    """Lettered figure. pts: {letter: point}. segs: 'AB' strings. marks: (V, P, Q, value, text).
    rights: (V, P, Q) right-angle squares. ticks / arrows: ('AB', n). fills: 'ABCD' polygons."""
    F = Fig()
    for f in fills:
        F.el.append((0, "<polygon points='%s' fill='%s' stroke='none'/>" % (" ".join("%.1f,%.1f" % pts[k] for k in f), FILL)))
    for s in segs:
        p, q = pts[s[0]], pts[s[1]]
        # split at points lying on the segment, so that the line-of-sight check sees every vertex as an end point
        on = sorted([dist(p, v) for k, v in pts.items() if k not in s and dist(p, v) > 1e-6 and dist(q, v) > 1e-6
                     and abs(dist(p, v) + dist(v, q) - dist(p, q)) < 1e-6])
        cuts = [0.0] + on + [dist(p, q)]
        d = ang(p, q)
        for i in range(len(cuts) - 1):
            F.line(pol(p, cuts[i], d), pol(p, cuts[i + 1], d), sw=sw)
    for s, k in ticks:
        F.ticks(pts[s[0]], pts[s[1]], k)
    tk = [set(s) for s, k in ticks]
    for s, k in arrows:
        F.arrow(pts[s[0]], pts[s[1]], k, 0.3 if set(s) in tk else 0.5)
    for v, p, q in rights:
        F.mark(pts[v], pts[p], pts[q], 90, kind="right")
    for v, p, q, val, t in marks:
        F.mark(pts[v], pts[p], pts[q], val, t)
    for k in sorted(pts):
        if k not in hide:
            F.vletter(pts[k], k)
    try:
        return F.svg(label)
    except AssertionError as e:
        raise AssertionError("%s: %s" % (label, e))


def measure(pts, v, p, q):
    a, b = ang(pts[v], pts[p]), ang(pts[v], pts[q])
    s = (b - a) % 360
    return min(s, 360 - s)


def para(L, s, angA, rot=0):
    """Parallelogram ABCD: A bottom left, B bottom right, C top right, D top left; ∠DAB = angA."""
    A_, B_ = O, (float(L), 0.0)
    D_ = pol(O, s, angA)
    C_ = add(B_, D_)
    pts = [A_, B_, C_, D_]
    if rot:
        pts = rot_all(pts, rot)
    return dict(zip("ABCD", pts))


def trap(L, angA, angB, h, rot=0, names="ABCD"):
    """Trapezium ABCD with AB // DC (AB at the bottom): ∠DAB = angA, ∠ABC = angB, height h."""
    A_, B_ = O, (float(L), 0.0)
    D_ = pol(A_, h / math.sin(math.radians(angA)), angA)
    C_ = pol(B_, h / math.sin(math.radians(angB)), 180 - angB)
    assert C_[0] - D_[0] > 45, "top side too short"
    pts = [A_, B_, C_, D_]
    if rot:
        pts = rot_all(pts, rot)
    return dict(zip(names, pts))


def bar_svg(rows, total, k, label, ask=None):
    """Model method: one bar per angle, made of equal unit boxes (width = degrees × k).
    rows: (name, [(degrees, text in box)]). A brace on the right shows the total."""
    fs, rh, gap = 15, 26, 10
    nw = max(tw(n, fs) for n, _ in rows) + 12
    out = []
    ends = []
    for i, (name, segs) in enumerate(rows):
        y = i * (rh + gap)
        out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                   % (nw - 8, y + rh / 2 + 5.4, fs, RED if i == ask else INK, name))
        x = nw
        for deg, t in segs:
            w = deg * k
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, y, w, rh, "#ffffff" if t else FILL, GREEN))
            if t:
                assert tw(t, 14) + 4 < w, t
                out.append("<text x='%.1f' y='%.1f' font-size='14' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                           % (x + w / 2, y + rh / 2 + 5, INK, t))
            x += w
        ends.append(x)
        if i == ask:
            out.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s'>?</text>" % (x + 7, y + rh / 2 + 5.8, RED))
    bx = max(ends) + 24
    H = len(rows) * (rh + gap) - gap
    out.append("<polyline points='%.1f,1 %.1f,1 %.1f,%d %.1f,%d' fill='none' stroke='%s' stroke-width='2'/>"
               % (bx - 6, bx, bx, H - 1, bx - 6, H - 1, INK))
    out.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s'>%s</text>" % (bx + 7, H / 2 + 5.8, INK, total))
    W = int(bx + 10 + tw(total, 16))
    return svg_wrap(W, H + 2, "<g transform='translate(1 0)'>%s</g>" % "".join(out), label)


# ------------------------------------------------------------ set 1: angle facts review
def set_facts(rnd, P):
    its = []
    q_line = "The angles are on a straight line. Find the unknown angle."
    its.append(dq(fig(line_svg(0, [48, 132], ["48°", "?"])) + q_line, 132, [312, 42, 48],
                  "Angles on a straight line add up to 180°. 180° − 48° = 132°.", rnd))
    its.append(dq(fig(line_svg(10, [57, 85, 38], ["57°", "?", "38°"])) + q_line, 85, [265, 95, 123],
                  "57° + 38° = 95°. Angles on a straight line add up to 180°, so 180° − 95° = 85°.", rnd))
    its.append(dq(fig(point_svg(20, [105, 160, 95], ["105°", "?", "95°"])) +
                  "The angles are at a point. Find the unknown angle.", 160, [200, 255, 265],
                  "Angles at a point add up to 360°. 105° + 95° = 200°, and 360° − 200° = 160°.", rnd))
    its.append(dq(fig(cross_svg(15, 62, ["62°", None, "?", None])) + "Two straight lines cross. Find the unknown angle.", 62,
                  [118, 298, 28], "The unknown angle is vertically opposite 62°. Vertically opposite angles are equal, so it is 62°.", rnd))
    its.append(dq(fig(cross_svg(-10, 74, ["74°", "?", None, None])) + "Two straight lines cross. Find the unknown angle.", 106,
                  [74, 286, 16], "The unknown angle and 74° are on a straight line. 180° − 74° = 106°.", rnd))
    # triangle ABC
    t = tri_pts(52, 71, 150)
    pts = dict(A=t[0], B=t[1], C=t[2])
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("A", "B", "C", 52, "52°"), ("B", "A", "C", 71, "71°"), ("C", "A", "B", 57, "?")],
                         fills=["ABC"], label="triangle ABC")) + "Find ∠ACB.", 57, [237, 123, 128],
                  "Angles in a triangle add up to 180°. ∠ACB = 180° − 52° − 71° = 57°.", rnd))
    t = tri_pts(34, 90, 140)
    pts = dict(A=t[0], B=t[1], C=t[2])
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("A", "B", "C", 34, "34°"), ("C", "A", "B", 56, "?")], rights=[("B", "A", "C")],
                         fills=["ABC"], label="right-angled triangle ABC")) + "Find ∠ACB.", 56, [146, 236, 34],
                  "∠ABC is a right angle (90°). ∠ACB = 180° − 90° − 34° = 56°.", rnd))
    t = tri_pts(63, 69, 140)
    pts = dict(B=t[0], C=t[1], A=t[2], D=(t[1][0] + 80, 0.0))
    its.append(dq(fig(fg(pts, ["BD", "AB", "AC"], [("B", "C", "A", 63, "63°"), ("A", "B", "C", 48, "48°"), ("C", "A", "D", 111, "?")],
                         fills=["ABC"], label="triangle ABC with BC made longer to D")) + "BCD is a straight line. Find ∠ACD.", 111,
                  [69, 291, 48],
                  "∠ACB = 180° − 63° − 48° = 69°. ∠ACD and ∠ACB are on a straight line: 180° − 69° = 111°.", rnd))
    its.append(dq(fig(point_svg(30, [80, 80, 80, 120], ["x", "x", "x", "120°"], label="angles at a point, three marked x")) +
                  "The three angles marked <i>x</i> are equal. Find ∠<i>x</i>.", 80, [20, 120, 240],
                  "Angles at a point add up to 360°. 360° − 120° = 240°, and 240° ÷ 3 = 80°.", rnd))
    its.append(dq(fig(line_svg(0, [65, 65, 50], ["y", "y", "50°"], label="angles on a straight line, two marked y")) +
                  "The two angles marked <i>y</i> are equal. Find ∠<i>y</i>.", 65, [130, 155, 50],
                  "180° − 50° = 130°. The two equal angles share it: 130° ÷ 2 = 65°.", rnd))
    L = 80
    pts = dict(O=O, A=pol(O, L, 195), B=pol(O, L, 15), C=pol(O, L, 157), D=pol(O, L, 337))
    its.append(dq(fig(fg(pts, ["AB", "CD"], [("O", "A", "C", 38, "38°"), ("O", "B", "C", 142, "?")], label="lines AB and CD cross at O")) +
                  "AB and CD are straight lines. Find ∠BOC.", 142, [38, 322, 52],
                  "∠BOC and ∠AOC are on the straight line AB. ∠BOC = 180° − 38° = 142°.", rnd))
    pts = dict(O=O, A=pol(O, 95, 0), B=pol(O, 95, 90), C=pol(O, 95, 27))
    its.append(dq(fig(fg(pts, ["OA", "OB", "OC"], [("O", "A", "C", 27, "27°"), ("O", "C", "B", 63, "?")], rights=[("O", "A", "B")],
                         label="right angle AOB split by OC")) + "∠AOB is a right angle. Find ∠BOC.", 63, [153, 333, 27],
                  "A right angle is 90°. ∠BOC = 90° − 27° = 63°.", rnd))
    its.append(dq("The angles in a triangle add up to …", 180, [360, 90, 270],
                  "The three angles of any triangle add up to 180°. Angles at a point add up to 360°.", rnd))
    its.append(dq("Two angles of a triangle are 47° and 68°. Find the third angle.", 65, [245, 115, 133],
                  "47° + 68° = 115°. 180° − 115° = 65°.", rnd))
    its.append(dq("Three angles at a point are 140°, 95° and ∠<i>x</i>. Find ∠<i>x</i>.", 125, [235, 220, 265],
                  "Angles at a point add up to 360°. 140° + 95° = 235°, and 360° − 235° = 125°.", rnd))
    n, he, his = P.next()
    t = tri_pts(70, 48, 140)
    pts = dict(A=t[0], B=t[1], C=t[2])
    its.append(mcq(fig(fg(pts, ["AB", "BC", "CA"], [("A", "B", "C", 70, "70°"), ("B", "A", "C", 48, "48°"), ("C", "A", "B", 62, "x")],
                          fills=["ABC"], label="triangle ABC with angle x")) +
                   "%s says ∠<i>x</i> = 242°, because the angles in a triangle add up to 360°. Is %s right?" % (n, he),
                   "No, ∠<i>x</i> = 62°", ["Yes, ∠<i>x</i> = 242°", "No, ∠<i>x</i> = 118°", "No, ∠<i>x</i> = 22°"],
                   "The angles in a triangle add up to 180°, not 360°. ∠<i>x</i> = 180° − 70° − 48° = 62°.", rnd))
    its.append(dq("In triangle PQR, ∠PQR = 90° and ∠QPR is twice ∠QRP. Find ∠QRP.", 30, [60, 45, 90],
                  "∠QPR + ∠QRP = 180° − 90° = 90°. ∠QRP is 1 unit and ∠QPR is 2 units: 3 units = 90°, so 1 unit = 30°.", rnd))
    # bow-tie: AD and BE cross at C
    C_ = O
    pts = dict(C=C_, A=pol(C_, 120 * math.sin(math.radians(67)), 207.5), B=pol(C_, 120 * math.sin(math.radians(58)), 152.5),
               D=pol(C_, 100 * math.sin(math.radians(55)), 27.5), E=pol(C_, 100 * math.sin(math.radians(70)), 332.5))
    its.append(dq(fig(fg(pts, ["AD", "BE", "AB", "DE"], [("A", "B", "C", 58, "58°"), ("B", "A", "C", 67, "67°"), ("C", "D", "E", 55, "?")],
                         fills=["ABC", "CDE"], label="two triangles with lines AD and BE crossing at C")) +
                  "AD and BE are straight lines that cross at C. Find ∠DCE.", 55, [125, 58, 67],
                  "∠ACB = 180° − 58° − 67° = 55°. ∠DCE is vertically opposite ∠ACB, so ∠DCE = 55°.", rnd))
    pts = dict(O=O, A=pol(O, 92, 180), B=pol(O, 92, 0), C=pol(O, 92, 145), D=pol(O, 92, 88))
    its.append(dq(fig(fg(pts, ["AB", "OC", "OD"], [("O", "A", "C", 35, "35°"), ("O", "C", "D", 57, "?"), ("O", "D", "B", 88, "88°")],
                         label="straight line AOB with rays OC and OD")) + "AOB is a straight line. Find ∠COD.", 57,
                  [237, 92, 145],
                  "Angles on a straight line add up to 180°. 35° + 88° = 123°, and 180° − 123° = 57°.", rnd))
    its.append(dq("∠<i>p</i> and ∠<i>q</i> are on a straight line. ∠<i>p</i> is 40° more than ∠<i>q</i>. Find ∠<i>p</i>.", 110,
                  [70, 140, 90],
                  "∠<i>p</i> + ∠<i>q</i> = 180°. Take away the extra 40°: 180° − 40° = 140°, so ∠<i>q</i> = 140° ÷ 2 = 70°. "
                  "∠<i>p</i> = 70° + 40° = 110°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angle facts review", "items": its}


# ------------------------------------------------------------ set 2: isosceles and equilateral triangles
def set_iso(rnd, P):
    its = []
    t = tri_pts(70, 70, 100)
    pts = dict(B=t[0], C=t[1], A=t[2])
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("A", "B", "C", 40, "40°"), ("B", "C", "A", 70, "?")], ticks=[("AB", 1), ("AC", 1)],
                         fills=["ABC"], label="isosceles triangle ABC")) + "In triangle ABC, AB = AC. Find ∠ABC.", 70,
                  [140, 40, 160],
                  "AB = AC, so ∠ABC = ∠ACB. 180° − 40° = 140°, and 140° ÷ 2 = 70°.", rnd))
    t = tri_pts(64, 64, 120)
    pts = dict(P=t[0], R=t[1], Q=t[2])
    its.append(dq(fig(fg(pts, ["PQ", "QR", "RP"], [("P", "R", "Q", 64, "64°"), ("Q", "P", "R", 52, "?")], ticks=[("PQ", 1), ("QR", 1)],
                         fills=["PQR"], label="isosceles triangle PQR")) + "In triangle PQR, PQ = QR. Find ∠PQR.", 52,
                  [64, 116, 128],
                  "PQ = QR, so ∠QPR = ∠QRP = 64°. ∠PQR = 180° − 64° − 64° = 52°.", rnd))
    pts = dict(B=O, A=pol(O, 140, 0), C=pol(O, 140, 30))
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("B", "A", "C", 30, "30°"), ("A", "B", "C", 75, "?")], ticks=[("BA", 1), ("BC", 1)],
                         fills=["ABC"], label="isosceles triangle ABC with AB = BC")) + "In triangle ABC, AB = BC. Find ∠BAC.", 75,
                  [30, 150, 120],
                  "AB = BC, so the equal angles are ∠BAC and ∠BCA (opposite the equal sides), not ∠ABC. "
                  "180° − 30° = 150°, and 150° ÷ 2 = 75°.", rnd))
    t = tri_pts(60, 60, 100)
    pts = dict(B=t[0], C=t[1], A=t[2], D=(t[1][0] + 80, 0.0))
    its.append(dq(fig(fg(pts, ["BD", "AB", "AC"], [("C", "A", "D", 120, "?")], ticks=[("AB", 1), ("BC", 1), ("CA", 1)],
                         fills=["ABC"], label="equilateral triangle ABC with BC made longer to D")) +
                  "ABC is an equilateral triangle and BCD is a straight line. Find ∠ACD.", 120, [60, 300, 90],
                  "Each angle of an equilateral triangle is 60°, so ∠ACB = 60°. ∠ACD = 180° − 60° = 120°.", rnd))
    t = tri_pts(62, 62, 110)
    pts = dict(B=t[0], C=t[1], A=t[2], D=(t[1][0] + 80, 0.0))
    its.append(dq(fig(fg(pts, ["BD", "AB", "AC"], [("C", "A", "D", 118, "118°"), ("A", "B", "C", 56, "?")], ticks=[("AB", 1), ("AC", 1)],
                         fills=["ABC"], label="isosceles triangle ABC with BC made longer to D")) +
                  "In triangle ABC, AB = AC. BCD is a straight line. Find ∠BAC.", 56, [62, 118, 124],
                  "∠ACB = 180° − 118° = 62°. AB = AC, so ∠ABC = 62° too. ∠BAC = 180° − 62° − 62° = 56°.", rnd))
    t = tri_pts(70, 66, 140)
    pts = dict(B=t[0], C=t[1], A=t[2])
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("B", "C", "A", 70, "70°"), ("A", "B", "C", 44, "44°"), ("C", "A", "B", 66, "?")],
                         fills=["ABC"], label="triangle ABC")) + "Find ∠ACB.", 66, [70, 68, 110],
                  "No sides are marked equal, so do not assume the triangle is isosceles. ∠ACB = 180° − 70° − 44° = 66°.", rnd))
    D_ = O
    pts = dict(D=D_, B=(-90.0, 0.0), C=(100.0, 0.0), A=pol(D_, 100, 70))
    its.append(dq(fig(fg(pts, ["BC", "DA", "AC", "AB"], [("D", "A", "B", 110, "110°"), ("C", "D", "A", 55, "?")],
                         ticks=[("DA", 1), ("DC", 1)], fills=["ABC"], label="triangle ABC with AD drawn")) +
                  "BDC is a straight line and AD = DC. Find ∠ACD.", 55, [70, 110, 35],
                  "∠ADC = 180° − 110° = 70°. AD = DC, so ∠DAC = ∠DCA. 180° − 70° = 110°, and 110° ÷ 2 = 55°.", rnd))
    pts = dict(A=O, B=(100.0, 0.0), C=(100.0, -100.0), D=(0.0, -100.0))
    pts["E"] = pol(pts["D"], 100, 60)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "DE", "EC"], [("D", "A", "E", 150, "?")], rights=[("A", "B", "D"), ("B", "A", "C")],
                         ticks=[("DE", 1), ("EC", 1), ("DC", 1)], fills=["ABCD", "DCE"], label="square ABCD with triangle DCE on top")) +
                  "ABCD is a square and DCE is an equilateral triangle. Find ∠ADE.", 150, [60, 90, 210],
                  "∠ADC = 90° (square) and ∠CDE = 60° (equilateral triangle). ∠ADE = 90° + 60° = 150°.", rnd))
    t = tri_pts(50, 50, 120)
    pts = dict(A=t[0], B=t[1], C=t[2])
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("A", "B", "C", 50, "x"), ("B", "A", "C", 50, "x"), ("C", "A", "B", 80, "80°")],
                         ticks=[("CA", 1), ("CB", 1)], fills=["ABC"], label="isosceles triangle with base angles x")) +
                  "In triangle ABC, CA = CB. Find ∠<i>x</i>.", 50, [100, 80, 140],
                  "The two base angles are equal. 180° − 80° = 100°, and 100° ÷ 2 = 50°.", rnd))
    t = tri_pts(45, 90, 120)
    pts = dict(A=t[0], B=t[1], C=t[2])
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA"], [("A", "B", "C", 45, "?")], rights=[("B", "A", "C")], ticks=[("AB", 1), ("BC", 1)],
                         fills=["ABC"], label="right-angled isosceles triangle ABC")) +
                  "In triangle ABC, ∠ABC = 90° and AB = BC. Find ∠BAC.", 45, [90, 60, 135],
                  "∠BAC + ∠BCA = 180° − 90° = 90°. They are equal, so ∠BAC = 90° ÷ 2 = 45°.", rnd))
    t = tri_pts(60, 60, 160)
    pts = dict(B=t[0], C=t[1], A=t[2])
    pts["D"] = meet(pts["A"], ang(pts["A"], pts["B"]) + 45, pts["B"], 0)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA", "AD"], [("A", "B", "D", 45, "45°"), ("D", "A", "C", 105, "?")],
                         ticks=[("AB", 1), ("BC", 1), ("CA", 1)], fills=["ABC"], label="equilateral triangle ABC with AD drawn")) +
                  "ABC is an equilateral triangle. D is on BC. Find ∠ADC.", 105, [75, 15, 60],
                  "∠ABD = 60°. In triangle ABD, ∠ADB = 180° − 60° − 45° = 75°. BDC is a straight line, so ∠ADC = 180° − 75° = 105°.", rnd))
    its.append(mcq("An isosceles triangle has an angle of 110°. Find the other two angles.", "35° and 35°",
                   ["70° and 70°", "110° and 35°", "55° and 55°"],
                   "Two angles of 110° would be more than 180°, so 110° is the angle between the equal sides. "
                   "180° − 110° = 70°, and 70° ÷ 2 = 35°.", rnd))
    its.append(mcq("An isosceles triangle has an angle of 50°. What could the other two angles be?", "50° and 80°, or 65° and 65°",
                   ["65° and 65° only", "50° and 80° only", "130° and 130°"],
                   "If 50° is one of the two equal angles: 180° − 50° − 50° = 80°. If 50° is the other angle: (180° − 50°) ÷ 2 = 65°. "
                   "Both are possible.", rnd))
    pts = dict(B=O, D=(90.0, 0.0), C=(175.0, 0.0))
    pts["A"] = pol(O, 90 * math.sin(math.radians(110)) / math.sin(math.radians(35)), 35)
    its.append(dq(fig(fg(pts, ["BC", "AB", "AD", "AC"], [("B", "D", "A", 35, "35°"), ("D", "A", "C", 70, "?")],
                         ticks=[("AD", 1), ("BD", 1)], fills=["ABC"], label="triangle ABC with AD drawn, AD = BD")) +
                  "D is on BC and AD = BD. Find ∠ADC.", 70, [110, 35, 145],
                  "AD = BD, so ∠BAD = ∠ABD = 35°. ∠ADB = 180° − 35° − 35° = 110°. ∠ADC = 180° − 110° = 70°.", rnd))
    pts = dict(A=O, B=(110.0, 0.0), C=(110.0, -110.0), D=(0.0, -110.0))
    pts["E"] = pol(O, 110, 60)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "AE", "BE"], [("B", "E", "C", 30, "?")], rights=[("C", "B", "D"), ("D", "A", "C")],
                         ticks=[("AB", 1), ("AE", 1), ("BE", 1)], fills=["ABE"], label="square ABCD with triangle ABE inside")) +
                  "ABCD is a square and ABE is an equilateral triangle. Find ∠EBC.", 30, [60, 90, 150],
                  "∠ABC = 90° (square) and ∠ABE = 60° (equilateral triangle). ∠EBC = 90° − 60° = 30°.", rnd))
    n, he, his = P.next()
    t = tri_pts(68, 68, 110)
    pts = dict(B=t[0], C=t[1], A=t[2])
    its.append(mcq(fig(fg(pts, ["AB", "BC", "CA"], ticks=[("AB", 1), ("AC", 1)], fills=["ABC"], label="isosceles triangle ABC")) +
                   "In triangle ABC, AB = AC. %s says ∠BAC = ∠ABC. Is %s right?" % (n, he),
                   "No, ∠ABC = ∠ACB", ["Yes, ∠BAC = ∠ABC", "No, ∠BAC = ∠ACB", "No, all three are equal"],
                   "The equal angles are opposite the equal sides. AB and AC are equal, so ∠ACB (opposite AB) = ∠ABC (opposite AC).", rnd))
    t = tri_pts(55, 55, 110)
    pts = dict(B=t[0], C=t[1], A=t[2], D=(-75.0, 0.0), E=(t[1][0] + 75, 0.0))
    its.append(dq(fig(fg(pts, ["DE", "AB", "AC"], [("B", "A", "D", 125, "125°"), ("C", "A", "E", 125, "?")], ticks=[("AB", 1), ("AC", 1)],
                         fills=["ABC"], label="isosceles triangle ABC on the straight line DE")) +
                  "In triangle ABC, AB = AC. DBCE is a straight line. Find ∠ACE.", 125, [55, 70, 235],
                  "∠ABC = 180° − 125° = 55°. AB = AC, so ∠ACB = 55°. ∠ACE = 180° − 55° = 125°.", rnd))
    its.append(dq("In triangle XYZ, XY = XZ and ∠YXZ = 48°. Find ∠XYZ.", 66, [132, 48, 156],
                  "XY = XZ, so ∠XYZ = ∠XZY. 180° − 48° = 132°, and 132° ÷ 2 = 66°.", rnd))
    pts = dict(B=O, C=(100.0, 0.0), E=(180.0, 0.0))
    pts["A"] = pol(O, 100, 60)
    pts["D"] = pol(pts["C"], 80, 60)
    its.append(dq(fig(fg(pts, ["BE", "AB", "AC", "CD", "DE"], [("C", "A", "D", 60, "?")], fills=["ABC", "CED"],
                         ticks=[("AB", 1), ("BC", 1), ("CA", 1), ("CD", 2), ("DE", 2), ("CE", 2)],
                         label="two equilateral triangles on a straight line")) +
                  "ABC and CED are equilateral triangles. BCE is a straight line. Find ∠ACD.", 60, [120, 90, 300],
                  "∠ACB = 60° and ∠DCE = 60°. Angles on a straight line add up to 180°: ∠ACD = 180° − 60° − 60° = 60°.", rnd))
    its.append(dq("Triangle ABC is isosceles with AB = AC. ∠ABC = 72°. Find ∠BAC.", 36, [72, 108, 54],
                  "AB = AC, so ∠ACB = ∠ABC = 72°. ∠BAC = 180° − 72° − 72° = 36°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Isosceles and equilateral triangles", "items": its}


# ------------------------------------------------------------ set 3: parallelograms and rhombuses
PG = ["AB", "BC", "CD", "DA"]


def set_para(rnd, P):
    its = []
    pts = para(150, 90, 65)
    its.append(dq(fig(fg(pts, PG, [("A", "B", "D", 65, "65°"), ("B", "A", "C", 115, "?")], fills=["ABCD"], label="parallelogram ABCD")) +
                  "ABCD is a parallelogram. Find ∠ABC.", 115, [65, 295, 25],
                  "In a parallelogram, angles next to each other add up to 180°. ∠ABC = 180° − 65° = 115°.", rnd))
    pts = para(150, 90, 72)
    its.append(dq(fig(fg(pts, PG, [("A", "B", "D", 72, "72°"), ("C", "B", "D", 72, "?")], fills=["ABCD"], label="parallelogram ABCD")) +
                  "ABCD is a parallelogram. Find ∠BCD.", 72, [108, 288, 18],
                  "∠BCD is opposite ∠DAB. Opposite angles of a parallelogram are equal, so ∠BCD = 72°.", rnd))
    pts = para(150, 85, 52)
    its.append(dq(fig(fg(pts, PG, [("B", "A", "C", 128, "128°"), ("D", "A", "C", 128, "?")], fills=["ABCD"], label="parallelogram ABCD")) +
                  "ABCD is a parallelogram. Find ∠ADC.", 128, [52, 232, 104],
                  "∠ADC is opposite ∠ABC. Opposite angles of a parallelogram are equal, so ∠ADC = 128°.", rnd))
    tk = [("AB", 1), ("BC", 1), ("CD", 1), ("DA", 1)]
    pts = para(110, 110, 70)
    its.append(dq(fig(fg(pts, PG, [("B", "A", "C", 110, "110°"), ("C", "B", "D", 70, "?")], ticks=tk, fills=["ABCD"], label="rhombus ABCD")) +
                  "ABCD is a rhombus. Find ∠BCD.", 70, [110, 250, 20],
                  "A rhombus is a parallelogram with 4 equal sides. ∠ABC and ∠BCD are next to each other: 180° − 110° = 70°.", rnd))
    pts = para(110, 110, 80)
    its.append(dq(fig(fg(pts, PG + ["AC"], [("B", "A", "C", 100, "100°"), ("A", "B", "C", 40, "?")], ticks=tk, fills=["ABCD"],
                         label="rhombus ABCD with diagonal AC")) +
                  "ABCD is a rhombus. Find ∠BAC.", 40, [80, 50, 100],
                  "AB = BC, so triangle ABC is isosceles and ∠BAC = ∠BCA. 180° − 100° = 80°, and 80° ÷ 2 = 40°.", rnd))
    pts = para(110, 110, 64)
    its.append(dq(fig(fg(pts, PG + ["BD"], [("A", "B", "D", 64, "64°"), ("B", "A", "D", 58, "?")], ticks=tk, fills=["ABCD"],
                         label="rhombus ABCD with diagonal BD")) +
                  "ABCD is a rhombus. Find ∠ABD.", 58, [64, 116, 32],
                  "AB = AD, so triangle ABD is isosceles and ∠ABD = ∠ADB. 180° − 64° = 116°, and 116° ÷ 2 = 58°.", rnd))
    pts = para(100, 100 * math.sin(math.radians(38)) / math.sin(math.radians(30)), 68)
    its.append(dq(fig(fg(pts, PG + ["AC"], [("A", "B", "C", 38, "38°"), ("B", "A", "C", 112, "112°"), ("A", "C", "D", 30, "?")],
                         fills=["ABCD"], label="parallelogram ABCD with diagonal AC")) +
                  "ABCD is a parallelogram. Find ∠DAC.", 30, [74, 68, 142],
                  "∠DAB = 180° − 112° = 68° (angles next to each other). ∠DAC = 68° − 38° = 30°.", rnd))
    pts = para(140, 90, 70)
    pts["E"] = (pts["B"][0] + 75, 0.0)
    its.append(dq(fig(fg(pts, ["AE", "BC", "CD", "DA"], [("B", "C", "E", 70, "70°"), ("D", "A", "C", 110, "?")], fills=["ABCD"],
                         label="parallelogram ABCD with AB made longer to E")) +
                  "ABCD is a parallelogram and ABE is a straight line. Find ∠ADC.", 110, [70, 250, 290],
                  "∠ABC = 180° − 70° = 110° (straight line). ∠ADC is opposite ∠ABC, so ∠ADC = 110°.", rnd))
    pts = para(150, 95, 60)
    its.append(dq(fig(fg(pts, PG, [("A", "B", "D", 60, "x"), ("B", "A", "C", 120, "2x")], fills=["ABCD"], label="parallelogram ABCD with angles x and 2x")) +
                  "ABCD is a parallelogram. Find ∠<i>x</i>.", 60, [120, 90, 45],
                  "Angles next to each other add up to 180°: <i>x</i> + 2<i>x</i> = 3<i>x</i> = 180°. So <i>x</i> = 180° ÷ 3 = 60°.", rnd))
    its.append(dq("In parallelogram PQRS, ∠PQR = 74°. Find ∠QRS.", 106, [74, 286, 16],
                  "∠PQR and ∠QRS are next to each other, so they add up to 180°. 180° − 74° = 106°.", rnd))
    its.append(mcq("ABCD is a parallelogram. Which two angles are always equal?", "∠DAB and ∠BCD",
                   ["∠DAB and ∠ABC", "∠ABC and ∠BCD", "∠DAB and ∠CDA"],
                   "Opposite angles of a parallelogram are equal: ∠DAB = ∠BCD and ∠ABC = ∠CDA. Angles next to each other add up to 180°.", rnd))
    its.append(mcq("One angle of a rhombus is 48°. Find the other three angles.", "48°, 132° and 132°",
                   ["132°, 132° and 132°", "48°, 48° and 48°", "42°, 48° and 42°"],
                   "The opposite angle is also 48°. Each angle next to it is 180° − 48° = 132°. Check: 48° + 132° + 48° + 132° = 360°.", rnd))
    pts = para(170, 110, 110)
    pts["E"] = meet(pts["B"], 135, pts["D"], 0)
    its.append(dq(fig(fg(pts, PG + ["BE"], [("D", "A", "C", 70, "70°"), ("B", "A", "E", 45, "45°"), ("B", "E", "C", 25, "?")],
                         fills=["ABCD"], label="parallelogram ABCD with BE drawn")) +
                  "ABCD is a parallelogram. E is on DC. Find ∠EBC.", 25, [65, 45, 135],
                  "∠ABC is opposite ∠ADC, so ∠ABC = 70°. ∠EBC = 70° − 45° = 25°.", rnd))
    pts = para(110, 110, 56)
    its.append(dq(fig(fg(pts, PG + ["AC"], [("A", "B", "C", 28, "28°"), ("B", "A", "C", 124, "?")], ticks=tk, fills=["ABCD"],
                         label="rhombus ABCD with diagonal AC")) +
                  "ABCD is a rhombus. Find ∠ABC.", 124, [28, 152, 56],
                  "AB = BC, so ∠BCA = ∠BAC = 28°. ∠ABC = 180° − 28° − 28° = 124°.", rnd))
    n, he, his = P.next()
    pts = para(150, 90, 58)
    its.append(mcq(fig(fg(pts, PG, [("A", "B", "D", 58, "58°")], fills=["ABCD"], label="parallelogram ABCD")) +
                   "ABCD is a parallelogram. %s says ∠ABC = 58°, because opposite angles are equal. Is %s right?" % (n, he),
                   "No, ∠ABC = 122°", ["Yes, ∠ABC = 58°", "No, ∠ABC = 302°", "No, ∠ABC = 32°"],
                   "∠ABC is next to ∠DAB, not opposite it. Angles next to each other add up to 180°: 180° − 58° = 122°. "
                   "The angle opposite ∠DAB is ∠BCD.", rnd))
    pts = para(140, 85, 122)
    pts["E"] = (pts["C"][0] + 75, pts["C"][1])
    its.append(dq(fig(fg(pts, ["AB", "BC", "DE", "DA"], [("C", "B", "E", 58, "58°"), ("B", "A", "C", 58, "?")], fills=["ABCD"],
                         label="parallelogram ABCD with DC made longer to E")) +
                  "ABCD is a parallelogram and DCE is a straight line. Find ∠ABC.", 58, [122, 302, 32],
                  "∠BCD = 180° − 58° = 122° (straight line). ∠ABC and ∠BCD are next to each other: 180° − 122° = 58°.", rnd))
    pts = para(110, 110, 108)
    its.append(dq(fig(fg(pts, PG, [("A", "B", "D", 108, "3y"), ("B", "A", "C", 72, "2y")], ticks=tk, fills=["ABCD"],
                         label="rhombus ABCD with angles 3y and 2y")) +
                  "ABCD is a rhombus. Find ∠<i>y</i>.", 36, [72, 90, 108],
                  "Angles next to each other add up to 180°: 3<i>y</i> + 2<i>y</i> = 5<i>y</i> = 180°. So <i>y</i> = 180° ÷ 5 = 36°.", rnd))
    pts = para(140, 140 * math.sin(math.radians(35)) / math.sin(math.radians(40)), 105)
    its.append(dq(fig(fg(pts, PG + ["BD"], [("A", "B", "D", 105, "105°"), ("D", "A", "B", 40, "40°"), ("B", "A", "D", 35, "?")],
                         fills=["ABCD"], label="parallelogram ABCD with diagonal BD")) +
                  "ABCD is a parallelogram. Find ∠ABD.", 35, [145, 75, 40],
                  "In triangle ABD: ∠ABD = 180° − 105° − 40° = 35°.", rnd))
    its.append(dq("In parallelogram WXYZ, ∠WXY is 30° more than ∠XYZ. Find ∠WXY.", 105, [75, 150, 195],
                  "∠WXY + ∠XYZ = 180°. 180° − 30° = 150°, so ∠XYZ = 150° ÷ 2 = 75° and ∠WXY = 75° + 30° = 105°.", rnd))
    its.append(dq("What do the four angles of a parallelogram add up to?", 360, [180, 720, 270],
                  "A parallelogram is a 4-sided figure. Its two pairs of angles next to each other each add up to 180°: 2 × 180° = 360°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallelograms and rhombuses", "items": its}


# ------------------------------------------------------------ set 4: trapeziums
TR = ["AB", "BC", "CD", "DA"]
AR = [("AB", 1), ("DC", 1)]


def set_trap(rnd, P):
    its = []
    pts = trap(170, 70, 60, 85)
    its.append(dq(fig(fg(pts, TR, [("A", "B", "D", 70, "70°"), ("D", "A", "C", 110, "?")], arrows=AR, fills=["ABCD"], label="trapezium ABCD")) +
                  "ABCD is a trapezium with AB // DC. Find ∠ADC.", 110, [70, 290, 20],
                  "∠DAB and ∠ADC are between the parallel sides, so they add up to 180°. ∠ADC = 180° − 70° = 110°.", rnd))
    pts = trap(170, 80, 58, 85)
    its.append(dq(fig(fg(pts, TR, [("B", "A", "C", 58, "58°"), ("C", "B", "D", 122, "?")], arrows=AR, fills=["ABCD"], label="trapezium ABCD")) +
                  "ABCD is a trapezium with AB // DC. Find ∠BCD.", 122, [58, 302, 32],
                  "∠ABC and ∠BCD are between the parallel sides: ∠BCD = 180° − 58° = 122°.", rnd))
    pts = trap(170, 75, 65, 85)
    its.append(dq(fig(fg(pts, TR, [("A", "B", "D", 75, "75°"), ("B", "A", "C", 65, "65°"), ("C", "B", "D", 115, "?")], arrows=AR,
                         fills=["ABCD"], label="trapezium ABCD")) +
                  "ABCD is a trapezium with AB // DC. Find ∠BCD.", 115, [105, 140, 65],
                  "∠BCD pairs with ∠ABC (the two angles on side BC): 180° − 65° = 115°. ∠DAB pairs with ∠ADC, not with ∠BCD.", rnd))
    pts = trap(160, 90, 62, 90)
    its.append(dq(fig(fg(pts, TR, [("B", "A", "C", 62, "62°"), ("C", "B", "D", 118, "?")], rights=[("A", "B", "D"), ("D", "A", "C")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with two right angles")) +
                  "ABCD is a trapezium with AB // DC. Find ∠BCD.", 118, [62, 28, 298],
                  "∠ABC and ∠BCD are between the parallel sides, so they add up to 180°. ∠BCD = 180° − 62° = 118°.", rnd))
    its.append(dq("In trapezium PQRS, PQ // SR and ∠QPS = 64°. Find ∠PSR.", 116, [64, 296, 26],
                  "∠QPS and ∠PSR are on side PS, between the parallel sides. They add up to 180°: 180° − 64° = 116°.", rnd))
    h = 90.0
    pts = dict(A=O, D=pol(O, h / math.sin(math.radians(75)), 75), C=(h / math.tan(math.radians(40)), -h), B=(175.0, 0.0))
    its.append(dq(fig(fg(pts, TR + ["AC"], [("D", "A", "C", 105, "105°"), ("A", "B", "C", 40, "40°"), ("A", "C", "D", 35, "?")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with diagonal AC")) +
                  "ABCD is a trapezium with AB // DC. Find ∠DAC.", 35, [65, 75, 140],
                  "∠DAB = 180° − 105° = 75° (angles between the parallel sides). ∠DAC = 75° − 40° = 35°.", rnd))
    A_, B_ = O, (130.0, 0.0)
    C_ = pol(B_, 130 * math.sin(math.radians(30)) / math.sin(math.radians(40)), 70)
    D_ = (-C_[1] / math.tan(math.radians(80)), C_[1])
    pts = dict(A=A_, B=B_, C=C_, D=D_)
    its.append(dq(fig(fg(pts, TR + ["AC"], [("B", "A", "C", 110, "110°"), ("A", "B", "C", 30, "30°"), ("C", "A", "B", 40, "?")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with diagonal AC")) +
                  "ABCD is a trapezium with AB // DC. Find ∠ACB.", 40, [70, 140, 220],
                  "In triangle ABC: ∠ACB = 180° − 110° − 30° = 40°.", rnd))
    pts = trap(140, 72, 108, 80)
    pts["E"] = (pts["B"][0] + 75, 0.0)
    its.append(dq(fig(fg(pts, ["AE", "BC", "CD", "DA"], [("B", "C", "E", 72, "72°"), ("C", "B", "D", 72, "?")], arrows=AR, fills=["ABCD"],
                         label="trapezium ABCD with AB made longer to E")) +
                  "ABCD is a trapezium with AB // DC. ABE is a straight line. Find ∠BCD.", 72, [108, 252, 18],
                  "∠ABC = 180° − 72° = 108° (straight line). ∠ABC and ∠BCD are between the parallel sides: 180° − 108° = 72°.", rnd))
    pts = trap(170, 100, 65, 85)
    its.append(dq(fig(fg(pts, TR, [("A", "B", "D", 100, "x + 20°"), ("D", "A", "C", 80, "x")], arrows=AR, fills=["ABCD"],
                         label="trapezium ABCD with angles x and x + 20°")) +
                  "ABCD is a trapezium with AB // DC. Find ∠<i>x</i>.", 80, [100, 90, 170],
                  "<i>x</i> + <i>x</i> + 20° = 180°. 2<i>x</i> = 160°, so <i>x</i> = 80°. Check: 80° + 100° = 180°.", rnd))
    its.append(mcq("ABCD is a trapezium with AB // DC. Which two angles must add up to 180°?", "∠DAB and ∠ADC",
                   ["∠DAB and ∠ABC", "∠DAB and ∠BCD", "∠ADC and ∠BCD"],
                   "The two angles on a side that joins the parallel sides add up to 180°: ∠DAB + ∠ADC and ∠ABC + ∠BCD.", rnd))
    B_, h = (215.0, 0.0), 110.0
    D_ = add(B_, pol(O, h / math.sin(math.radians(145)), 145))
    A_ = (D_[0] - h / math.tan(math.radians(70)), 0.0)
    C_ = pol(B_, h / math.sin(math.radians(65)), 115)
    pts = dict(A=A_, B=B_, C=C_, D=D_)
    its.append(dq(fig(fg(pts, TR + ["BD"], [("B", "A", "D", 35, "35°"), ("C", "B", "D", 115, "115°"), ("B", "D", "C", 30, "?")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with diagonal BD")) +
                  "ABCD is a trapezium with AB // DC. Find ∠DBC.", 30, [80, 65, 145],
                  "∠ABC = 180° − 115° = 65° (angles between the parallel sides). ∠DBC = 65° − 35° = 30°.", rnd))
    base = trap(150, 118, 70, 80)
    pts = dict(A=base["A"], D=base["B"], C=base["C"], B=base["D"])
    pts = dict(zip(pts, rot_all(list(pts.values()), 90)))
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA"], [("A", "B", "D", 118, "118°"), ("B", "A", "C", 62, "?")],
                         arrows=[("AD", 1), ("BC", 1)], fills=["ABCD"], label="trapezium ABCD with AD parallel to BC")) +
                  "ABCD is a trapezium with AD // BC. Find ∠ABC.", 62, [118, 242, 28],
                  "Here the parallel sides are AD and BC. ∠BAD and ∠ABC are on side AB, between them, so they add up to 180°. "
                  "∠ABC = 180° − 118° = 62°.", rnd))
    h = 85.0
    pts = dict(A=O, B=(180.0, 0.0), D=(0.0, -h), C=(h / math.tan(math.radians(50)), -h))
    its.append(dq(fig(fg(pts, TR + ["AC"], [("A", "B", "C", 50, "50°"), ("C", "D", "A", 50, "?")], rights=[("D", "A", "C")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with a right angle and diagonal AC")) +
                  "ABCD is a trapezium with AB // DC and ∠ADC = 90°. Find ∠ACD.", 50, [40, 130, 140],
                  "∠DAB = 180° − 90° = 90°, so ∠DAC = 90° − 50° = 40°. In triangle ADC: ∠ACD = 180° − 90° − 40° = 50°.", rnd))
    n, he, his = P.next()
    pts = trap(170, 68, 75, 85)
    its.append(mcq(fig(fg(pts, TR, [("A", "B", "D", 68, "68°")], arrows=AR, fills=["ABCD"], label="trapezium ABCD")) +
                   "ABCD is a trapezium with AB // DC. %s says ∠ABC = 112°, because 180° − 68° = 112°. Is %s right?" % (n, he),
                   "No, 112° is ∠ADC", ["Yes, ∠ABC = 112°", "No, ∠ABC = 68°", "No, ∠ABC = 292°"],
                   "∠DAB pairs with ∠ADC (both on side AD). So ∠ADC = 180° − 68° = 112°. "
                   "∠ABC cannot be found from ∠DAB alone.", rnd))
    its.append(dq("In trapezium KLMN, KL // NM. ∠KLM is 3 times ∠LMN. Find ∠LMN.", 45, [135, 60, 90],
                  "∠KLM + ∠LMN = 180°. ∠LMN is 1 unit and ∠KLM is 3 units: 4 units = 180°, so 1 unit = 45°.", rnd))
    A_, B_ = O, (170.0, 0.0)
    E_ = meet(A_, 70, B_, 120)
    tdn = 0.5
    pts = dict(A=A_, B=B_, E=E_, D=(E_[0] * tdn, E_[1] * tdn), C=(B_[0] + (E_[0] - B_[0]) * tdn, E_[1] * tdn))
    its.append(dq(fig(fg(pts, ["AB", "BE", "EA", "DC"], [("A", "B", "E", 70, "70°"), ("B", "A", "E", 60, "60°"), ("D", "E", "C", 70, "?")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with AD and BC made longer to meet at E")) +
                  "ABCD is a trapezium with AB // DC. AD and BC are made longer to meet at E. Find ∠EDC.", 70, [110, 50, 60],
                  "∠ADC = 180° − 70° = 110° (angles between the parallel sides). ADE is a straight line, so ∠EDC = 180° − 110° = 70°.", rnd))
    its.append(dq("In trapezium ABCD, AB // DC, ∠DAB = 56° and ∠BCD = 104°. Find ∠ADC + ∠ABC.", 200, [160, 360, 180],
                  "∠ADC = 180° − 56° = 124° and ∠ABC = 180° − 104° = 76°. 124° + 76° = 200°.", rnd))
    s = 125.0
    D_ = pol(O, s, 60)
    C_ = (D_[0] + s, D_[1])
    pts = dict(A=O, D=D_, C=C_, B=(C_[0] - C_[1] / math.tan(math.radians(70)), 0.0))
    its.append(dq(fig(fg(pts, TR + ["AC"], [("D", "A", "C", 120, "120°"), ("A", "B", "C", 30, "?")], ticks=[("AD", 1), ("DC", 1)],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with diagonal AC and AD = DC")) +
                  "ABCD is a trapezium with AB // DC and AD = DC. Find ∠CAB.", 30, [60, 120, 90],
                  "AD = DC, so ∠DAC = ∠DCA = (180° − 120°) ÷ 2 = 30°. ∠DAB = 180° − 120° = 60°, so ∠CAB = 60° − 30° = 30°.", rnd))
    h = 85.0
    A_ = O
    D_ = pol(O, h / math.sin(math.radians(64)), 64)
    E_ = (D_[0] + h / math.tan(math.radians(66)), 0.0)
    pts = dict(A=A_, D=D_, E=E_, B=(190.0, 0.0))
    pts["C"] = (pts["B"][0] - h / math.tan(math.radians(72)), -h)
    its.append(dq(fig(fg(pts, TR + ["DE"], [("A", "B", "D", 64, "64°"), ("D", "A", "E", 50, "50°"), ("D", "E", "C", 66, "?")],
                         arrows=AR, fills=["ABCD"], label="trapezium ABCD with DE drawn")) +
                  "ABCD is a trapezium with AB // DC. E is on AB. Find ∠EDC.", 66, [116, 64, 130],
                  "∠ADC = 180° − 64° = 116° (angles between the parallel sides). ∠EDC = 116° − 50° = 66°.", rnd))
    base = trap(150, 65, 75, 80)
    pts = dict(P=base["A"], S=base["B"], R=base["C"], Q=base["D"])
    pts = dict(zip(pts, rot_all(list(pts.values()), -80)))
    its.append(dq(fig(fg(pts, ["PQ", "QR", "RS", "SP"], [("S", "P", "R", 75, "75°"), ("R", "Q", "S", 105, "?")],
                         arrows=[("PS", 1), ("QR", 1)], fills=["PQRS"], label="trapezium PQRS with PS parallel to QR")) +
                  "PQRS is a trapezium with PS // QR. Find ∠QRS.", 105, [75, 285, 15],
                  "∠PSR and ∠QRS are on side RS, between the parallel sides PS and QR. ∠QRS = 180° − 75° = 105°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Trapeziums", "items": its}


# ------------------------------------------------------------ set 5: PSLE-style problems
def set_psle(rnd, P):
    its = []
    pts = dict(A=O, B=(110.0, 0.0), C=(110.0, -110.0), D=(0.0, -110.0))
    pts["E"] = pol(O, 110, 60)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "AE", "BE", "CE"], [("E", "A", "C", 135, "?")],
                         rights=[("C", "B", "D"), ("D", "A", "C")], ticks=[("AB", 1), ("AE", 1), ("BE", 1)], fills=["ABE"],
                         label="square ABCD with triangle ABE inside and CE drawn")) +
                  "ABCD is a square and ABE is an equilateral triangle. Find ∠AEC.", 135, [75, 150, 120],
                  "∠EBC = 90° − 60° = 30°. BE = BA = BC, so triangle EBC is isosceles: ∠BEC = (180° − 30°) ÷ 2 = 75°. "
                  "∠AEC = ∠AEB + ∠BEC = 60° + 75° = 135°.", rnd))
    pts = dict(B=O, C=(110.0, 0.0))
    pts["A"] = pol(O, 110, 60)
    pts["D"] = pol(pts["C"], 110, 40)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA", "CD", "DA"], [("C", "A", "D", 80, "80°"), ("A", "B", "D", 110, "?")],
                         ticks=[("AB", 1), ("BC", 1), ("CA", 1), ("CD", 1)], fills=["ABC", "ACD"],
                         label="equilateral triangle ABC and isosceles triangle ACD")) +
                  "ABC is an equilateral triangle and CA = CD. Find ∠BAD.", 110, [50, 140, 120],
                  "CA = CD, so ∠CAD = ∠CDA = (180° − 80°) ÷ 2 = 50°. ∠BAC = 60°. ∠BAD = 60° + 50° = 110°.", rnd))
    t = tri_pts(72, 72, 90)
    pts = dict(B=t[0], C=t[1], A=t[2])
    pts["D"] = meet(pts["B"], 36, pts["C"], ang(pts["C"], pts["A"]))
    its.append(dq(fig(fg(pts, ["AB", "BC", "CA", "BD"], [("A", "B", "C", 36, "36°"), ("B", "C", "D", 36, "?")],
                         ticks=[("AB", 1), ("AC", 1), ("BD", 2), ("BC", 2)], fills=["ABC"], label="isosceles triangle ABC with BD drawn")) +
                  "In the figure, AB = AC and BD = BC. D is on AC. Find ∠DBC.", 36, [72, 108, 54],
                  "∠ACB = (180° − 36°) ÷ 2 = 72°. BD = BC, so ∠BDC = ∠BCD = 72°. ∠DBC = 180° − 72° − 72° = 36°.", rnd))
    B_ = (200.0, 0.0)
    C_ = pol(B_, 100, 110)
    E_ = (110.0, 0.0)
    D_ = (C_[0] - (B_[0] - E_[0]), C_[1])
    A_ = (D_[0] + D_[1] / math.tan(math.radians(48)), 0.0)
    pts = dict(A=A_, B=B_, C=C_, D=D_, E=E_)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "DE"], [("A", "B", "D", 48, "48°"), ("B", "A", "C", 70, "70°"), ("D", "A", "E", 62, "?")],
                         arrows=[("AB", 1), ("DC", 1), ("ED", 2), ("BC", 2)], fills=["ABCD"], label="trapezium ABCD with parallelogram EBCD")) +
                  "ABCD is a trapezium with AB // DC. E is on AB and EBCD is a parallelogram. Find ∠ADE.", 62, [70, 48, 118],
                  "In parallelogram EBCD, ∠DEB = 180° − 70° = 110°. AEB is a straight line, so ∠AED = 180° − 110° = 70°. "
                  "In triangle ADE: ∠ADE = 180° − 48° − 70° = 62°.", rnd))
    C_ = O
    pts = dict(C=C_, A=pol(C_, 120 * math.sin(math.radians(67)), 207.5), B=pol(C_, 120 * math.sin(math.radians(58)), 152.5),
               D=pol(C_, 100 * math.sin(math.radians(55)), 27.5), E=pol(C_, 100 * math.sin(math.radians(70)), 332.5))
    its.append(dq(fig(fg(pts, ["AD", "BE", "AB", "DE"], [("A", "B", "C", 58, "58°"), ("B", "A", "C", 67, "67°"), ("D", "C", "E", 70, "70°"),
                                                       ("E", "C", "D", 55, "?")],
                         fills=["ABC", "CDE"], label="two triangles with lines AD and BE crossing at C")) +
                  "AD and BE are straight lines that cross at C. Find ∠CED.", 55, [67, 125, 58],
                  "∠ACB = 180° − 58° − 67° = 55°. ∠DCE is vertically opposite, so ∠DCE = 55°. ∠CED = 180° − 55° − 70° = 55°.", rnd))
    pts = para(135, 135, 110)
    pts["E"] = pol(pts["B"], 135, 50)
    its.append(dq(fig(fg(pts, PG + ["BE", "CE", "AE"], [("B", "A", "C", 70, "70°"), ("A", "B", "E", 25, "?")],
                         ticks=[("AB", 1), ("BC", 1), ("CD", 1), ("DA", 1), ("BE", 1), ("CE", 1)], fills=["ABCD", "BEC"],
                         label="rhombus ABCD with equilateral triangle BCE")) +
                  "ABCD is a rhombus and BCE is an equilateral triangle. Find ∠BAE.", 25, [50, 130, 65],
                  "∠ABE = 70° + 60° = 130°. AB = BC = BE, so triangle ABE is isosceles: ∠BAE = (180° − 130°) ÷ 2 = 25°.", rnd))
    pts = para(150, 100, 112)
    pts["E"] = pol(O, 100, 68)
    its.append(dq(fig(fg(pts, PG + ["AE"], [("B", "A", "C", 68, "68°"), ("A", "D", "E", 44, "?")], ticks=[("AD", 1), ("AE", 1)],
                         fills=["ABCD"], label="parallelogram ABCD with AE drawn")) +
                  "ABCD is a parallelogram. E is on DC and AD = AE. Find ∠DAE.", 44, [112, 68, 22],
                  "∠ADC is opposite ∠ABC, so ∠ADC = 68°. AD = AE, so ∠AED = 68°. ∠DAE = 180° − 68° − 68° = 44°.", rnd))
    pts = dict(A=O, B=(110.0, 0.0), C=(110.0, -110.0), D=(0.0, -110.0))
    pts["E"] = (110.0, -110.0 + 110 * math.tan(math.radians(32)))
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "DE"], [("E", "D", "C", 58, "58°"), ("D", "A", "E", 58, "?")],
                         rights=[("A", "B", "D"), ("B", "A", "C"), ("C", "B", "D")], fills=["ABCD"], label="square ABCD with DE drawn")) +
                  "ABCD is a square. E is on BC. Find ∠ADE.", 58, [32, 122, 148],
                  "In triangle DEC: ∠EDC = 180° − 90° − 58° = 32°. ∠ADE = 90° − 32° = 58°.", rnd))
    t = tri_pts(70, 70, 100)
    pts = dict(B=t[0], C=t[1], A=t[2], D=(190.0, 0.0))
    pts["E"] = pol(pts["C"], 45 / math.cos(math.radians(50)), 50)
    its.append(dq(fig(fg(pts, ["BD", "AB", "AC", "CE", "ED"], [("A", "B", "C", 40, "40°"), ("E", "C", "D", 80, "80°"), ("C", "A", "E", 60, "?")],
                         ticks=[("AB", 1), ("AC", 1), ("CE", 2), ("ED", 2)], fills=["ABC", "CDE"],
                         label="two isosceles triangles on a straight line")) +
                  "BCD is a straight line. AB = AC and CE = DE. Find ∠ACE.", 60, [120, 70, 50],
                  "∠ACB = (180° − 40°) ÷ 2 = 70°. ∠ECD = (180° − 80°) ÷ 2 = 50°. "
                  "On the straight line: ∠ACE = 180° − 70° − 50° = 60°.", rnd))
    pts = para(140, 90, 75)
    pts["E"] = pol(pts["D"], 140, 60)
    its.append(dq(fig(fg(pts, PG + ["DE", "EC"], [("A", "B", "D", 75, "75°"), ("D", "A", "E", 165, "?")],
                         ticks=[("DE", 1), ("EC", 1), ("DC", 1)], fills=["ABCD", "DCE"],
                         label="parallelogram ABCD with equilateral triangle DCE")) +
                  "ABCD is a parallelogram and DCE is an equilateral triangle. Find ∠ADE.", 165, [135, 45, 195],
                  "∠ADC = 180° − 75° = 105° (angles next to each other). ∠CDE = 60°. ∠ADE = 105° + 60° = 165°.", rnd))
    its.append(dq(fig(bar_svg([("smaller", [(20, "")] * 2), ("larger", [(20, "")] * 7)], "180°", 1.25,
                              "bar model of two angles, 2 units and 7 units, total 180°", ask=0)) +
                  "Two angles next to each other in a parallelogram are in the ratio 2 : 7. Find the smaller angle.", 40,
                  [80, 140, 20],
                  "Angles next to each other add up to 180°. 2 + 7 = 9 units. 9 units = 180°, so 1 unit = 20°. "
                  "The smaller angle is 2 units = 40°.", rnd))
    its.append(dq(fig(bar_svg([("∠BAC", [(32, "")]), ("∠ABC", [(32, "")] * 3), ("∠ACB", [(32, ""), (20, "20°")])], "180°", 1.6,
                              "bar model: 1 unit, 3 units, 1 unit and 20°, total 180°", ask=1)) +
                  "In triangle ABC, ∠ABC is 3 times ∠BAC. ∠ACB is 20° more than ∠BAC. Find ∠ABC.", 96, [32, 52, 120],
                  "5 units + 20° = 180°. 5 units = 160°, so 1 unit = 32°. ∠ABC = 3 units = 96°.", rnd))
    its.append(dq(fig(bar_svg([("∠BAC", [(36, "")]), ("∠ABC", [(36, "")] * 2), ("∠ACB", [(36, "")] * 2)], "180°", 1.3,
                              "bar model: 1 unit, 2 units and 2 units, total 180°", ask=1)) +
                  "Triangle ABC is isosceles with AB = AC. ∠ABC is twice ∠BAC. Find ∠ABC.", 72, [36, 90, 144],
                  "∠ACB = ∠ABC, so both are 2 units. 1 + 2 + 2 = 5 units = 180°. 1 unit = 36°, so ∠ABC = 72°.", rnd))
    pts = dict(A=O, B=(110.0, 0.0), C=(110.0, -110.0), D=(0.0, -110.0))
    pts["E"] = pol(pts["D"], 110, 60)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "DE", "EC", "AE"], [("A", "B", "E", 75, "?")], rights=[("B", "A", "C"), ("C", "B", "D")],
                         ticks=[("DE", 1), ("EC", 1), ("DC", 1), ("DA", 1)], fills=["ABCD", "DCE"],
                         label="square ABCD with equilateral triangle DCE and AE drawn")) +
                  "ABCD is a square and DCE is an equilateral triangle. Find ∠BAE.", 75, [15, 60, 30],
                  "∠ADE = 90° + 60° = 150°. DA = DC = DE, so ∠DAE = (180° − 150°) ÷ 2 = 15°. ∠BAE = 90° − 15° = 75°.", rnd))
    t = tri_pts(55, 68, 130)
    pts = dict(B=t[0], C=t[1], A=t[2], D=(-75.0, 0.0), E=(t[1][0] + 75, 0.0))
    its.append(dq(fig(fg(pts, ["DE", "AB", "AC"], [("B", "A", "D", 125, "125°"), ("C", "A", "E", 112, "112°"), ("A", "B", "C", 57, "?")],
                         fills=["ABC"], label="triangle ABC on a straight line")) +
                  "DBCE is a straight line. Find ∠BAC.", 57, [123, 237, 68],
                  "∠ABC = 180° − 125° = 55° and ∠ACB = 180° − 112° = 68°. ∠BAC = 180° − 55° − 68° = 57°.", rnd))
    L = 130.0
    pts = para(L, 2 * L * math.cos(math.radians(70)), 70)
    its.append(dq(fig(fg(pts, PG + ["BD"], [("A", "B", "D", 70, "70°"), ("B", "D", "C", 70, "?")], ticks=[("AB", 1), ("BD", 1)],
                         fills=["ABCD"], label="parallelogram ABCD with diagonal BD, AB = BD")) +
                  "ABCD is a parallelogram and AB = BD. Find ∠DBC.", 70, [40, 110, 55],
                  "AB = BD, so ∠ADB = ∠DAB = 70° and ∠ABD = 180° − 70° − 70° = 40°. "
                  "∠ABC = 180° − 70° = 110°, so ∠DBC = 110° − 40° = 70°.", rnd))
    s = 100.0
    D_ = pol(O, s, 68)
    pts = dict(A=O, D=D_, E=(2 * D_[0], 0.0), C=(D_[0] + 130, D_[1]))
    pts["B"] = (pts["C"][0] - D_[1] / math.tan(math.radians(75)), 0.0)
    its.append(dq(fig(fg(pts, TR + ["DE"], [("D", "E", "C", 68, "?")], ticks=[("DA", 1), ("DE", 1)], arrows=AR, fills=["ABCD"],
                         label="trapezium ABCD with DE drawn, DA = DE")) +
                  "ABCD is a trapezium with AB // DC. E is on AB, DA = DE and ∠ADC = 112°. Find ∠EDC.", 68, [44, 112, 22],
                  "∠DAB = 180° − 112° = 68°. DA = DE, so ∠DEA = 68° and ∠ADE = 180° − 68° − 68° = 44°. ∠EDC = 112° − 44° = 68°.", rnd))
    pts = para(110, 110, 64)
    its.append(dq(fig(fg(pts, PG + ["AC"], [("B", "A", "C", 116, "116°"), ("C", "A", "D", 32, "?")],
                         ticks=[("AB", 1), ("BC", 1), ("CD", 1), ("DA", 1)], fills=["ABCD"], label="rhombus ABCD with diagonal AC")) +
                  "ABCD is a rhombus. Find ∠ACD.", 32, [64, 116, 58],
                  "∠ADC is opposite ∠ABC, so ∠ADC = 116°. CD = DA, so triangle ACD is isosceles: "
                  "∠ACD = (180° − 116°) ÷ 2 = 32°.", rnd))
    its.append(dq(fig(bar_svg([("∠p", [(40, "")] * 2), ("∠q", [(40, "")] * 3), ("∠r", [(40, "")] * 4)], "360°", 0.7,
                              "bar model: 2, 3 and 4 units, total 360°", ask=2)) +
                  "Three angles at a point, ∠<i>p</i>, ∠<i>q</i> and ∠<i>r</i>, are in the ratio 2 : 3 : 4. Find ∠<i>r</i>.", 160,
                  [80, 120, 90],
                  "Angles at a point add up to 360°. 2 + 3 + 4 = 9 units = 360°, so 1 unit = 40°. ∠<i>r</i> = 4 units = 160°.", rnd))
    h = 90.0
    pts = dict(A=O, B=(h + h / math.tan(math.radians(60)), 0.0), D=(0.0, -h), E=(h, -h))
    pts["C"] = (pts["B"][0], -h)
    its.append(dq(fig(fg(pts, ["AB", "BC", "CD", "DA", "AE", "BE"], [("E", "A", "B", 75, "75°"), ("B", "E", "C", 30, "?")],
                         rights=[("A", "B", "D"), ("D", "A", "C"), ("C", "B", "D")], ticks=[("DA", 1), ("DE", 1)], fills=["ABE"],
                         label="rectangle ABCD with triangle ABE")) +
                  "ABCD is a rectangle. E is on DC and DE = DA. Find ∠EBC.", 30, [60, 45, 15],
                  "DE = DA and ∠ADE = 90°, so ∠DEA = 45°. On the straight line DC: ∠CEB = 180° − 45° − 75° = 60°. "
                  "In triangle EBC: ∠EBC = 180° − 90° − 60° = 30°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style composite figures", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    pg = para(130, 80, 70)
    f_pg = fg(pg, PG, [("A", "B", "D", 70, "70°"), ("B", "A", "C", 110, "110°"), ("C", "B", "D", 70, "70°"), ("D", "A", "C", 110, "110°")],
              fills=["ABCD"], label="parallelogram ABCD")
    tp = trap(150, 65, 75, 75)
    f_tp = fg(tp, TR, [("A", "B", "D", 65, "65°"), ("D", "A", "C", 115, "115°"), ("B", "A", "C", 75, "75°"), ("C", "B", "D", 105, "105°")],
              arrows=AR, fills=["ABCD"], label="trapezium ABCD")
    t = tri_pts(70, 70, 90)
    f_iso = fg(dict(B=t[0], C=t[1], A=t[2]), ["AB", "BC", "CA"],
               [("A", "B", "C", 40, "40°"), ("B", "C", "A", 70, "70°"), ("C", "A", "B", 70, "70°")],
               ticks=[("AB", 1), ("AC", 1)], fills=["ABC"], label="isosceles triangle ABC")
    shapes = strip_svg([f_pg, f_tp, f_iso], ["parallelogram", "trapezium", "isosceles triangle"],
                       "parallelogram, trapezium and isosceles triangle with their angles")
    ex_pts = para(150, 95, 66)
    ex_pts["E"] = meet(ex_pts["B"], 66 + 48, ex_pts["D"], 0)
    f_ex = fg(ex_pts, PG + ["BE"], [("A", "B", "D", 66, "66°"), ("B", "E", "C", 48, "?")], ticks=[("BC", 1), ("BE", 1)],
              fills=["ABCD"], label="parallelogram ABCD with BE drawn, BE = BC")
    assert abs(measure(ex_pts, "C", "B", "E") - 66) < 1e-6 and abs(measure(ex_pts, "E", "B", "C") - 66) < 1e-6
    return (
        "<h2>Find one angle at a time</h2>"
        "<p>A composite figure is made of shapes you know: triangles, squares, rectangles, parallelograms, rhombuses and trapeziums. "
        "Do not draw extra lines. Find the angles you can, one at a time, until you reach the one you want.</p>" +
        table(["Shape or place", "Angle fact"], [
            ["Straight line", "Angles add up to 180°"],
            ["At a point", "Angles add up to 360°"],
            ["Two straight lines cross", "Vertically opposite angles are equal"],
            ["Triangle", "Angles add up to 180°"],
            ["Isosceles triangle", "The two angles opposite the equal sides are equal"],
            ["Equilateral triangle", "Each angle is 60°"],
            ["Square and rectangle", "Each angle is 90°"],
            ["Parallelogram and rhombus", "Opposite angles are equal. Angles next to each other add up to 180°"],
            ["Trapezium", "The two angles between the parallel sides add up to 180°"],
        ]) +
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>Arrows show parallel sides: AB // DC means AB is parallel to DC. Tick marks show equal sides. "
        "In the trapezium, 65° + 115° = 180° and 75° + 105° = 180°.</figcaption></figure>"
        "<h2>Worked example</h2>"
        "<figure class='sn-fig'>" + f_ex + "</figure>" +
        ex("Example 1", "ABCD is a parallelogram. E is on DC and BE = BC. ∠DAB = 66°. Find ∠EBC.",
           "Step 1: ∠BCD is opposite ∠DAB, so ∠BCD = 66°. "
           "Step 2: BE = BC, so triangle BCE is isosceles and ∠BEC = ∠BCE = 66°. "
           "Step 3: ∠EBC = 180° − 66° − 66° = 48°.", "48°") +
        ex("Example 2 (model method)", "Two angles of a rhombus next to each other are in the ratio 1 : 4. Find the larger angle.",
           "They add up to 180°. 1 + 4 = 5 units = 180°, so 1 unit = 36°. The larger angle is 4 units = 144°.", "144°") +
        "<p>Write a reason for each step, for example “opposite angles of a parallelogram” or “isosceles triangle”. "
        "In the PSLE, method marks are given for clear working.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking a triangle is isosceles because it looks like one", "Use equal sides only when tick marks or the question say so"],
            ["Choosing the wrong pair of equal angles", "The equal angles are opposite the equal sides"],
            ["Using 360° for the angles in a triangle", "A triangle is 180°. Use 360° for angles at a point or in a 4-sided figure"],
            ["Saying angles next to each other in a parallelogram are equal", "Opposite angles are equal. Angles next to each other add up to 180°"],
            ["Adding the wrong pair in a trapezium", "Only the two angles on a side between the parallel sides add up to 180°"],
            ["Measuring with a protractor", "Figures may not be drawn to scale in tests. Calculate"],
        ])
    )


FAQ = [
    {"q": "What are angles in composite figures in P6 maths?",
     "a": "They are questions where you find an unknown angle in a figure made of triangles, squares, rectangles, parallelograms, rhombuses and trapeziums. "
          "You use angle facts step by step, without drawing extra lines."},
    {"q": "How do I help my child find unknown angles in PSLE geometry questions?",
     "a": "Ask your child to name the shapes in the figure, mark every angle they can find, and write a reason for each step. "
          "Most PSLE angle questions need 2 or 3 steps."},
    {"q": "What is the most common mistake with angles in parallelograms?",
     "a": "Mixing up which angles are equal. Opposite angles are equal, but angles next to each other add up to 180°."},
    {"q": "Is this topic in the MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics Syllabus for Primary 6 includes finding unknown angles in composite figures, "
          "without additional construction of lines, under Measurement and Geometry."},
]


def gen():
    rnd = random.Random(66809)
    P = People(rnd)
    sets = [set_facts(rnd, P), set_iso(rnd, P), set_para(rnd, P), set_trap(rnd, P), set_psle(rnd, P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "angles-in-composite-figures", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Angles in Composite Figures",
        "seo_title": "P6 Angles in Composite Figures Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE)",
        "short_title": "Angles in Composite Figures",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 6: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Finding unknown angles, without additional construction of lines, in composite geometric figures involving squares, "
                         "rectangles, triangles, parallelograms, rhombuses and trapeziums",
        "meta_desc": "Free P6 maths practice: find unknown angles in figures made of triangles, parallelograms, rhombuses and trapeziums. "
                     "100 PSLE-style questions with answers.",
        "key_big": "Name the shapes in the figure, then find one angle at a time using an angle fact.",
        "key_sub": "Parallelogram ABCD with ∠DAB = 70°: ∠ABC = 180° − 70° = 110°, and ∠BCD = 70° (opposite angles are equal).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(angles on a straight line|bar model|two triangles with lines|two isosceles triangles on a straight line|"
                      "two equilateral triangles|triangle ABC on a straight line|isosceles triangle ABC on the straight line)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
