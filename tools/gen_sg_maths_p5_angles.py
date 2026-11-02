# -*- coding: utf-8 -*-
"""
SG Primary 5 Maths: Angles (MOE 2021 Primary Mathematics Syllabus, Standard, Primary 5: Geometry)
  python3 tools/gen_sg_maths_p5_angles.py
Angles on a straight line add to 180°, angles at a point add to 360°, vertically opposite angles are equal;
find unknown angles (∠a, ∠AOC), equal angles marked, ratio of angles with bar models. Singapore English.
HTML attributes use single quotes (no backslashes in the JSON).

Every figure is drawn to its stated angles: each marked angle is measured from the drawing
and checked against its value (also the "?" and letter angles). Labels are checked so that
they do not touch a line, an arc or another label, and sit inside the angle they name.
Bar models are drawn to scale (cell width = degrees × scale).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
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


def place_centre(P, t, d):
    """Point name at the crossing point, in direction d, as close as it fits without touching a stroke."""
    for r in range(12, 40):
        c = pol(O, r, d)
        if P.clear(P.box_of(c[0], c[1], t, 16), 2.5):
            P.label(c[0], c[1], t)
            return
    raise AssertionError("no room for " + t)


def rays_svg(rays, marks, label, L=80, dot=True, names=None, centre=None):
    """Lines from one point O. rays: directions (deg). marks: (from_dir, to_dir, val, text, kind[, eq]),
    each angle measured anticlockwise from from_dir to to_dir. eq: dashes across the arc (equal angles).
    names: {direction: point letter} at the ends of the lines; centre: (letter, direction) for the point O."""
    P = Pic()
    for d in rays:
        P.line(O, pol(O, L, d))
    for m in marks:
        a, b, val, t, kind = m[:5]
        eq = m[5] if len(m) > 5 else 0
        P.mark(O, pol(O, L, a), pol(O, L, b), val, t, kind=kind, ccw=True, eq=eq, r=(30 if eq else None))
    if dot:
        P.dot(O)
    for d, n in sorted((names or {}).items()):
        assert any(abs((d - r) % 360) < 1e-9 for r in rays), "name on a line end"
        c = pol(O, L + 14, d)
        P.label(c[0], c[1], n)
    if centre:
        place_centre(P, *centre)
    return P.svg(label)


def line_svg(rot, parts, texts, L=92, label="angles on a straight line", **kw):
    """Straight line through O at direction rot, with rays splitting the top half into parts (deg)."""
    assert abs(sum(parts) - 180) < 1e-9
    rays, marks, d = [rot, rot + 180], [], rot
    for p, t in zip(parts, texts):
        if d != rot:
            rays.append(d)
        marks.append((d, d + p, p, t, "right" if (p == 90 and t is None) else "arc"))
        d += p
    return rays_svg(rays, marks, label, L, **kw)


def point_svg(rot, parts, texts, L=80, label="angles at a point", eqs=None):
    assert abs(sum(parts) - 360) < 1e-9
    rays, marks, d = [], [], rot
    for i, (p, t) in enumerate(zip(parts, texts)):
        rays.append(d)
        marks.append((d, d + p, p, t, "right" if (p == 90 and t is None) else "arc", (eqs or {}).get(i, 0)))
        d += p
    return rays_svg(rays, marks, label, L)


def cross_svg(rot, a, texts, L=78, label="two straight lines crossing", **kw):
    """Two straight lines crossing at O: angles a, 180 − a, a, 180 − a anticlockwise from rot.
    texts: 4 labels (None = no mark). Rays: rot, rot + a, rot + 180, rot + 180 + a."""
    parts = [a, 180 - a, a, 180 - a]
    rays, marks, d = [], [], rot
    for p, t in zip(parts, texts):
        rays.append(d)
        if t is not None:
            marks.append((d, d + p, p, t, "arc"))
        d += p
    return rays_svg(rays, marks, label, L, **kw)


def bar_svg(rows, total, scale, label):
    """Bar model drawn to scale. rows: (angle letter, [(degrees, cell text)], right text).
    Every cell is exactly degrees × scale wide. A bracket on the right shows the total."""
    fs = 15
    lw = max(tw(r[0], fs) + 0.8 * fs for r in rows) + 12        # ∠ is about 0.8 em wide
    x0, bh, gap, y0 = 4 + lw, 30, 12, 4
    s, ends = [], []
    for i, (nm, segs, right) in enumerate(rows):
        y = y0 + i * (bh + gap)
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>∠<tspan font-style='italic'>%s</tspan></text>"
                 % (x0 - 8, y + bh / 2 + 5.5, fs, INK, nm))
        x = x0
        for deg, cell in segs:
            w = deg * scale
            col = "#fde7bd" if cell and cell != "?" else FILL
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y, w, bh, col, INK))
            if cell:
                assert tw(cell, fs) + 8 < w, ("cell too small", cell)
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x + w / 2, y + bh / 2 + 5.5, fs, RED if cell == "?" else INK, cell))
            x += w
        if right:
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='start'>%s</text>"
                     % (x + 8, y + bh / 2 + 5.5, fs, RED if right == "?" else INK, right))
            x += 8 + tw(right, fs)
        ends.append(x)
    ybot = y0 + len(rows) * (bh + gap) - gap
    xb = max(ends) + 10
    s.append("<path d='M%.1f %d h8 V%d h-8' fill='none' stroke='%s' stroke-width='2'/>" % (xb, y0, ybot, INK))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='start'>%s</text>"
             % (xb + 14, (y0 + ybot) / 2 + 5.5, fs, INK, total))
    W = int(math.ceil(xb + 14 + tw(total, fs) + 6))
    return svg_wrap(W, ybot + 5, "".join(s), "bar model: " + label)


def ratio_bars(names, parts, unit, ask, total):
    """Bar model for angles in a ratio: each unit cell is the same width (unit degrees)."""
    rows = [(n, [(unit, "")] * p, "?" if i == ask else "") for i, (n, p) in enumerate(zip(names, parts))]
    return bar_svg(rows, total, 230.0 / (max(parts) * unit), "%s in the ratio %s" % (" and ".join("angle " + n for n in names),
                                                                                    " : ".join(str(p) for p in parts)))


def mcq_n(q, v, wrong, e, rnd):
    return mcq(q, str(v), [str(w) for w in wrong], e, rnd)


def A(t):
    """∠ with an italic letter, for question HTML."""
    return "∠<i>%s</i>" % t


THREE = "three straight lines through a point"
CROSS = "two straight lines crossing"
NAMED = "straight lines with named points"
LINE_Q = "The angles are on a straight line. Find %s."
POINT_Q = "The angles are at a point. Find %s."
CROSS_Q = "Two straight lines cross. Find %s."


# ------------------------------------------------------------ set 1: angles on a straight line
def set_line(rnd, P):
    its = []
    for rot, parts, texts, k, v, wrong, e in [
        (0, [40, 140], ["40°", "a"], "a", 140, [320, 220, 40],
         "Angles on a straight line add up to 180°. 180° − 40° = 140°."),
        (0, [115, 65], ["115°", "b"], "b", 65, [245, 295, 115],
         "Angles on a straight line add up to 180°. 180° − 115° = 65°. (360° − 115° = 245° is for angles at a point.)"),
        (25, [132, 48], ["c", "48°"], "c", 132, [312, 228, 48],
         "The line is tilted, but it is still straight: 180° − 48° = 132°."),
        (-20, [73, 107], ["73°", "d"], "d", 107, [287, 253, 73],
         "Angles on a straight line add up to 180°. 180° − 73° = 107°."),
        (0, [90, 35, 55], [None, "35°", "e"], "e", 55, [235, 125, 145],
         "The small square shows a right angle: 90°. 90° + 35° = 125°, and 180° − 125° = 55°."),
        (0, [48, 62, 70], ["48°", "f", "70°"], "f", 62, [242, 118, 132],
         "First add the angles you know: 48° + 70° = 118°. Then subtract from 180°: 180° − 118° = 62°."),
        (10, [25, 95, 60], ["25°", "95°", "g"], "g", 60, [240, 120, 155],
         "25° + 95° = 120°. Angles on a straight line add up to 180°, so 180° − 120° = 60°."),
        (-12, [37, 108, 35], ["37°", "108°", "h"], "h", 35, [215, 145, 72],
         "37° + 108° = 145°, and 180° − 145° = 35°."),
    ]:
        its.append(dq(fig(line_svg(rot, parts, texts)) + LINE_Q % A(k), v, wrong, e, rnd))
    its.append(dq(fig(line_svg(-10, [55, 55, 70], ["m", "m", "70°"], label="angles on a straight line, two marked m")) +
                  "The two angles marked <i>m</i> are equal. Find %s." % A("m"), 55, [110, 145, 70],
                  "180° − 70° = 110°. The two equal angles share it: 110° ÷ 2 = 55°.", rnd))
    its.append(dq(fig(line_svg(0, [52, 128], ["?", "128°"], label=NAMED, names={0: "B", 52: "C", 180: "A"}, centre=("O", 270))) +
                  "AOB is a straight line. ∠AOC = 128°. Find ∠BOC.", 52, [232, 128, 38],
                  "∠AOC and ∠BOC are on the straight line AOB, so they add up to 180°. ∠BOC = 180° − 128° = 52°.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [50, 54, 76], ["50°", "k", "76°"])) +
                   "%s says %s = 50°, because it looks the same size as the 50° angle. Is %s right?" % (n, A("k"), he),
                   "No, ∠k = 54°", ["Yes, ∠k = 50°", "No, ∠k = 126°", "No, ∠k = 234°"],
                   "Do not trust how an angle looks: work it out. 50° + 76° = 126°, and 180° − 126° = 54°.", rnd))
    its.append(dq(fig(rays_svg([0, 62, 90], [(0, 62, 62, "62°", "arc"), (62, 90, 28, "n", "arc"), (0, 90, 90, None, "right")],
                               "right angle split into two angles", L=96)) +
                  "The whole angle is a right angle. Find %s." % A("n"), 28, [118, 298, 152],
                  "A right angle is 90°. 90° − 62° = 28°. (180° − 62° = 118° is for a straight line.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [130, 50], ["130°", "p"])) +
                   "%s says %s = 230°, because 360° − 130° = 230°. Is %s right?" % (n, A("p"), he),
                   "No, ∠p = 50°", ["Yes, ∠p = 230°", "No, ∠p = 130°", "No, ∠p = 310°"],
                   "The angles are on a straight line, so they add up to 180°, not 360°. 180° − 130° = 50°.", rnd))
    its.append(dq("Angles on a straight line add up to …", 180, [360, 90, 100],
                  "A straight line makes a half turn: 180°. Two right angles make a straight line.", rnd))
    its.append(dq("Two angles are on a straight line. One of them is 74°. Find the other angle.", 106, [286, 254, 16],
                  "180° − 74° = 106°. Check: 74° + 106° = 180°.", rnd))
    its.append(dq("Three equal angles together make a straight line. Find the size of each angle.", 60, [120, 90, 45],
                  "The three angles add up to 180°. 180° ÷ 3 = 60°. (120° comes from using 360°.)", rnd))
    its.append(mcq("Two angles are next to each other. One is 125° and the other is 65°. Can they make a straight line?",
                   "No, they add up to 190°", ["Yes, they add up to 180°", "Yes, one angle is obtuse", "No, they add up to 360°"],
                   "125° + 65° = 190°. Angles on a straight line must add up to exactly 180°, so they cannot.", rnd))
    its.append(dq("Two angles are on a straight line. One angle is 4 times as big as the other. Find the smaller angle.",
                  36, [45, 72, 144],
                  "The angles are 1 unit and 4 units: 5 units = 180°. 1 unit = 180° ÷ 5 = 36°. (The larger angle is 4 × 36° = 144°.)", rnd))
    its.append(mcq("Two angles are on a straight line. One is an acute angle of 38°. What is the other angle?",
                   "obtuse, 142°", ["acute, 52°", "reflex, 322°", "acute, 38°"],
                   "180° − 38° = 142°. It is between 90° and 180°, so it is obtuse. (52° is 90° − 38°, which is for a right angle.)", rnd))
    its.append(dq("A straight line is split into three angles. Two of them are 65° and 47°. Find the third angle.", 68, [112, 248, 115],
                  "65° + 47° = 112°. 180° − 112° = 68°. (112° is the two angles added, not the unknown angle.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles on a straight line (180°)", "items": its}


# ------------------------------------------------------------ set 2: angles at a point
def set_point(rnd, P):
    its = []
    for rot, parts, texts, k, v, wrong, e in [
        (0, [110, 135, 115], ["110°", "135°", "a"], "a", 115, [245, 250, 225],
         "Angles at a point add up to 360°. 110° + 135° = 245°, and 360° − 245° = 115°."),
        (30, [140, 85, 135], ["140°", "b", "135°"], "b", 85, [275, 220, 225],
         "140° + 135° = 275°. Angles at a point add up to 360°: 360° − 275° = 85°."),
        (0, [90, 125, 60, 85], [None, "125°", "60°", "c"], "c", 85, [275, 175, 95],
         "The small square is 90°. 90° + 125° + 60° = 275°, and 360° − 275° = 85°. (175° comes from forgetting the right angle.)"),
        (15, [100, 120, 75, 65], ["100°", "120°", "d", "65°"], "d", 75, [285, 140, 65],
         "100° + 120° + 65° = 285°. 360° − 285° = 75°."),
        (0, [200, 95, 65], ["200°", "95°", "e"], "e", 65, [295, 160, 265],
         "One angle is a reflex angle. 200° + 95° = 295°, and 360° − 295° = 65°."),
    ]:
        its.append(dq(fig(point_svg(rot, parts, texts)) + POINT_Q % A(k), v, wrong, e, rnd))
    its.append(dq(fig(point_svg(90, [230, 130], ["r", "130°"], label="a reflex angle and an obtuse angle at a point")) +
                  "The two angles are at a point. Find the reflex angle %s." % A("r"), 230, [50, 490, 310],
                  "Angles at a point add up to 360°. 360° − 130° = 230°. (50° comes from using 180°, and 490° from adding.)", rnd))
    its.append(dq(fig(point_svg(90, [120, 120, 120], ["f", "f", "f"], label="three equal angles at a point")) +
                  "The three angles marked <i>f</i> are equal. Find %s." % A("f"), 120, [60, 90, 180],
                  "Angles at a point add up to 360°. 360° ÷ 3 = 120°. (180° ÷ 3 = 60° is for a straight line.)", rnd))
    its.append(dq(fig(point_svg(20, [100, 130, 130], ["100°", "g", "g"], label="angles at a point, two marked g")) +
                  "The two angles marked <i>g</i> are equal. Find %s." % A("g"), 130, [260, 40, 100],
                  "360° − 100° = 260°. The two equal angles share it: 260° ÷ 2 = 130°.", rnd))
    its.append(dq(fig(point_svg(30, [120, 80, 160], ["120°", "p", "q"], label="angles at a point, p and q")) +
                  "The angles are at a point. %s is twice as big as %s. Find %s." % (A("q"), A("p"), A("p")), 80, [120, 160, 240],
                  "360° − 120° = 240°. ∠<i>p</i> is 1 unit and ∠<i>q</i> is 2 units: 3 units = 240°, so 1 unit = 80°. "
                  "(120° comes from treating the two angles as equal.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(point_svg(0, [150, 100, 110], ["150°", "100°", "h"])) +
                   "%s says %s = 250°, because 150° + 100° = 250°. Is %s right?" % (n, A("h"), he),
                   "No, ∠h = 110°", ["Yes, ∠h = 250°", "No, ∠h = 150°", "No, ∠h = 360°"],
                   "Add the angles you know, then subtract from 360°: 360° − 250° = 110°. "
                   "250° is the total of the two angles, not the unknown angle.", rnd))
    its.append(dq("Angles at a point add up to …", 360, [180, 270, 90],
                  "Angles at a point make a complete turn: 360°.", rnd))
    its.append(dq("Five equal angles fit exactly around a point. Find the size of each angle.", 72, [36, 90, 60],
                  "At a point: 360°. 360° ÷ 5 = 72°. (36° comes from 180° ÷ 5.)", rnd))
    its.append(dq("Four angles are at a point. One is a right angle and the other three are equal. Find the size of each of the three equal angles.",
                  90, [30, 120, 270],
                  "360° − 90° = 270°. The three equal angles share it: 270° ÷ 3 = 90°.", rnd))
    its.append(dq("Four angles are at a point. Three of them are 95°, 120° and 85°. Find the fourth angle.", 60, [300, 145, 180],
                  "95° + 120° + 85° = 300°. 360° − 300° = 60°.", rnd))
    its.append(dq("A reflex angle of 250° and one other angle make a complete turn. Find the other angle.", 110, [70, 610, 250],
                  "A complete turn is 360°. 360° − 250° = 110°. (70° comes from 250° − 180°, and 610° from adding.)", rnd))
    its.append(mcq_n("How many angles of 45° fit exactly around a point?", 8, [4, 6, 12],
                     "360° ÷ 45° = 8. (4 is how many fit on a straight line: 180° ÷ 45° = 4.)", rnd))
    its.append(dq("Three angles are at a point. Two of them are 140° each. Find the third angle.", 80, [280, 220, 40],
                  "140° + 140° = 280°. 360° − 280° = 80°. (220° comes from subtracting only one 140°.)", rnd))
    its.append(dq("Three angles at a point are in the ratio 2 : 3 : 4. Find the largest angle.", 160, [80, 120, 90],
                  "2 + 3 + 4 = 9 units = 360°. 1 unit = 360° ÷ 9 = 40°. The largest angle is 4 units: 4 × 40° = 160°. "
                  "(80° comes from using 180°.)", rnd))
    its.append(mcq("Can angles of 150°, 120° and 100° fit around a point with no gaps or overlaps?",
                   "No, they add up to 370°", ["Yes, they add up to 360°", "No, they add up to 180°", "Yes, two are obtuse"],
                   "150° + 120° + 100° = 370°. Angles at a point must add up to exactly 360°, so they would overlap by 10°.", rnd))
    its.append(dq("Two angles are at a point. One is 5 times as big as the other. Find the larger angle.", 300, [60, 150, 288],
                  "1 unit + 5 units = 6 units = 360°. 1 unit = 60°, so the larger angle is 5 × 60° = 300° (a reflex angle). "
                  "(150° comes from using 180°.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles at a point (360°)", "items": its}


# ------------------------------------------------------------ set 3: vertically opposite angles
def set_vertical(rnd, P):
    its = []
    for rot, a, texts, k, v, wrong in [
        (0, 40, ["40°", None, "a", None], "a", 40, [140, 320, 50]),
        (20, 115, [None, "b", None, "65°"], "b", 65, [115, 295, 25]),
        (-30, 72, ["c", None, "72°", None], "c", 72, [108, 288, 18]),
        (10, 35, [None, "145°", None, "d"], "d", 145, [35, 215, 55]),
        (40, 25, [None, "e", None, "155°"], "e", 155, [25, 205, 65]),
    ]:
        its.append(dq(fig(cross_svg(rot, a, texts, label=CROSS)) + CROSS_Q % A(k), v, wrong,
                      "%s is vertically opposite the %s angle. Vertically opposite angles are equal, so %s = %s." % (A(k), D(v), A(k), D(v)), rnd))
    for rot, a, texts, k, v, wrong in [
        (0, 58, ["58°", "f", None, None], "f", 122, [58, 302, 32]),
        (15, 130, [None, "g", "130°", None], "g", 50, [130, 230, 40]),
        (-20, 75, [None, None, "75°", "h"], "h", 105, [75, 285, 15]),
        (5, 34, ["m", "146°", None, None], "m", 34, [146, 214, 56]),
    ]:
        kn = [t for t in texts if t and t.endswith("°")][0]
        its.append(dq(fig(cross_svg(rot, a, texts, label=CROSS)) + CROSS_Q % A(k), v, wrong,
                      "%s and %s are next to each other on a straight line, so they add up to 180°. 180° − %s = %s. "
                      "(They are not vertically opposite.)" % (A(k), kn, kn, D(v)), rnd))
    its.append(mcq(fig(cross_svg(0, 64, ["64°", "p", "q", "r"], label=CROSS)) + "Two straight lines cross. Find ∠<i>p</i>, ∠<i>q</i> and ∠<i>r</i>.",
                   "p = 116°, q = 64°, r = 116°",
                   ["p = 64°, q = 116°, r = 64°", "p = 116°, q = 116°, r = 116°", "p = 26°, q = 64°, r = 26°"],
                   "∠<i>p</i> is on a straight line with 64°: 180° − 64° = 116°. ∠<i>q</i> is vertically opposite 64°, so it is 64°. "
                   "∠<i>r</i> is vertically opposite ∠<i>p</i>, so it is 116°.", rnd))
    its.append(mcq(fig(cross_svg(30, 105, ["s", "t", "u", "105°"], label=CROSS)) + "Two straight lines cross. Find ∠<i>s</i>, ∠<i>t</i> and ∠<i>u</i>.",
                   "s = 75°, t = 105°, u = 75°",
                   ["s = 105°, t = 75°, u = 105°", "s = 75°, t = 75°, u = 75°", "s = 255°, t = 105°, u = 255°"],
                   "∠<i>s</i> and 105° are on a straight line: 180° − 105° = 75°. ∠<i>t</i> is vertically opposite 105°, so it is 105°. "
                   "∠<i>u</i> is vertically opposite ∠<i>s</i>: 75°.", rnd))
    its.append(mcq(fig(cross_svg(10, 55, ["a", "b", "c", "d"], label=CROSS)) + "Two straight lines cross. Which two angles are vertically opposite?",
                   "∠a and ∠c", ["∠a and ∠b", "∠c and ∠d", "∠a and ∠d"],
                   "Vertically opposite angles are across the crossing point from each other: ∠<i>a</i> and ∠<i>c</i> (also ∠<i>b</i> and ∠<i>d</i>). "
                   "Angles next to each other, like ∠<i>a</i> and ∠<i>b</i>, add up to 180°.", rnd))
    its.append(dq(fig(rays_svg([0, 45, 125, 180, 225, 305],
                               [(0, 45, 45, "45°", "arc"), (45, 125, 80, "80°", "arc"), (225, 305, 80, "w", "arc")], THREE, L=82)) +
                  "Three straight lines meet at a point. Find %s." % A("w"), 80, [100, 55, 45],
                  "∠<i>w</i> is vertically opposite the 80° angle, so it is also 80°.", rnd))
    its.append(dq(fig(cross_svg(0, 70, ["?", None, "70°", None], label=NAMED,
                                names={0: "B", 70: "D", 180: "A", 250: "C"}, centre=("O", 125))) +
                  "AB and CD are straight lines that cross at O. ∠AOC = 70°. Find ∠BOD.", 70, [110, 290, 20],
                  "∠BOD and ∠AOC are vertically opposite, so they are equal: ∠BOD = 70°.", rnd))
    its.append(dq(fig(cross_svg(0, 48, [None, "132°", "?", None], label=NAMED,
                                names={0: "B", 48: "D", 180: "A", 228: "C"}, centre=("O", 294))) +
                  "AB and CD are straight lines that cross at O. ∠AOD = 132°. Find ∠AOC.", 48, [132, 228, 42],
                  "∠AOC is next to ∠AOD on the straight line CD, so they add up to 180°: 180° − 132° = 48°. "
                  "(∠AOC is not vertically opposite ∠AOD. ∠BOC is.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(cross_svg(0, 86, ["86°", "k", None, None], label=CROSS)) +
                   "%s says %s = 86°, because the two angles look the same size. Is %s right?" % (n, A("k"), he),
                   "No, ∠k = 94°", ["Yes, ∠k = 86°", "No, ∠k = 274°", "No, ∠k = 4°"],
                   "∠<i>k</i> is next to 86° on a straight line, not opposite it. 180° − 86° = 94°. "
                   "Angles can look equal and still be different, so use the angle facts.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says that vertically opposite angles add up to 180°. Is %s right?" % (n, he),
                   "No, they are equal", ["Yes, they are on a straight line", "Yes, they always do", "No, they add up to 360°"],
                   "Vertically opposite angles are equal. It is the angles next to each other (on a straight line) that add up to 180°.", rnd))
    its.append(mcq("Two straight lines cross. One of the angles is a right angle. What are the other three angles?",
                   "90°, 90° and 90°", ["90°, 180° and 90°", "45°, 90° and 45°", "270°, 90° and 270°"],
                   "The angle next to 90° is 180° − 90° = 90°, and vertically opposite angles are equal. So all four angles are 90°.", rnd))
    its.append(dq("Two straight lines cross. Two vertically opposite angles add up to 100°. Find the size of each of the other two angles.",
                  130, [50, 80, 260],
                  "The two equal opposite angles are 100° ÷ 2 = 50° each. The angles next to them are 180° − 50° = 130°.", rnd))
    its.append(dq("Two straight lines cross. One angle is 27°. Find the angle vertically opposite it.", 27, [153, 333, 63],
                  "Vertically opposite angles are equal, so it is also 27°. (153° is the angle next to it.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Vertically opposite angles", "items": its}


# ------------------------------------------------------------ set 4: unknown angles in figures
def set_figures(rnd, P):
    its = []
    q3 = "Three straight lines meet at a point. Find %s."
    its.append(dq(fig(rays_svg([0, 40, 115, 180, 220, 295],
                               [(0, 40, 40, "40°", "arc"), (40, 115, 75, "75°", "arc"), (115, 180, 65, "a", "arc")], THREE, L=82)) + q3 % A("a"),
                  65, [245, 115, 75],
                  "The three angles above the flat line are on a straight line. 40° + 75° = 115°, and 180° − 115° = 65°.", rnd))
    its.append(dq(fig(rays_svg([0, 40, 115, 180, 220, 295],
                               [(0, 40, 40, "40°", "arc"), (115, 180, 65, "65°", "arc"), (220, 295, 75, "b", "arc")], THREE, L=82)) + q3 % A("b"),
                  75, [65, 40, 105],
                  "Step 1: the angle between 40° and 65° on the straight line is 180° − 40° − 65° = 75°. "
                  "Step 2: ∠<i>b</i> is vertically opposite it, so ∠<i>b</i> = 75°.", rnd))
    its.append(dq(fig(rays_svg([0, 55, 120, 180, 235, 300],
                               [(0, 55, 55, "55°", "arc"), (120, 180, 60, "c", "arc"), (235, 300, 65, "65°", "arc")], THREE, L=82)) + q3 % A("c"),
                  60, [120, 65, 300],
                  "The angle between 55° and ∠<i>c</i> is vertically opposite 65°, so it is 65°. "
                  "Then on the straight line: 180° − 55° − 65° = 60°.", rnd))
    its.append(mcq(fig(rays_svg([0, 50, 110, 180, 230, 290],
                                [(0, 50, 50, "50°", "arc"), (50, 110, 60, "60°", "arc"), (110, 180, 70, "p", "arc"),
                                 (180, 230, 50, "q", "arc"), (230, 290, 60, "r", "arc")], THREE, L=90)) +
                   "Three straight lines meet at a point. Find ∠<i>p</i>, ∠<i>q</i> and ∠<i>r</i>.",
                   "p = 70°, q = 50°, r = 60°",
                   ["p = 70°, q = 60°, r = 50°", "p = 250°, q = 50°, r = 60°", "p = 70°, q = 130°, r = 120°"],
                   "∠<i>p</i>: 180° − 50° − 60° = 70° (straight line). ∠<i>q</i> is vertically opposite 50°, and ∠<i>r</i> is vertically opposite 60°.", rnd))
    lab5 = "two crossing lines and one more line from the point"
    qx = "Two straight lines cross, and one more line starts at the crossing point. Find %s."
    its.append(dq(fig(rays_svg([0, 180, 70, 250, 125],
                               [(0, 70, 70, "70°", "arc"), (70, 125, 55, "55°", "arc"), (125, 180, 55, "d", "arc")], lab5, L=86)) + qx % A("d"),
                  55, [125, 110, 70],
                  "The three angles above the flat line are on a straight line. 70° + 55° = 125°, and 180° − 125° = 55°.", rnd))
    its.append(dq(fig(rays_svg([0, 180, 70, 250, 125],
                               [(70, 125, 55, "55°", "arc"), (125, 180, 55, "55°", "arc"), (180, 250, 70, "e", "arc")], lab5, L=86)) + qx % A("e"),
                  70, [110, 55, 250],
                  "Step 1: on the straight line, the angle at the right is 180° − 55° − 55° = 70°. "
                  "Step 2: ∠<i>e</i> is vertically opposite it, so ∠<i>e</i> = 70°.", rnd))
    its.append(dq(fig(rays_svg([0, 90, 180, 270, 310],
                               [(0, 90, 90, None, "right"), (270, 310, 40, "f", "arc"), (310, 360, 50, "50°", "arc")],
                               "two lines at right angles and one more line", L=80)) +
                  "Two straight lines cross at right angles. One more line starts at the crossing point. Find %s." % A("f"),
                  40, [130, 310, 50],
                  "The lines cross at right angles, so all four angles they make are 90°. "
                  "So ∠<i>f</i> + 50° = 90°, and ∠<i>f</i> = 90° − 50° = 40°.", rnd))
    its.append(dq(fig(point_svg(0, [60, 85, 215], ["60°", "g", "215°"])) + POINT_Q % A("g"),
                  85, [275, 145, 300],
                  "60° + 215° = 275°. Angles at a point add up to 360°: 360° − 275° = 85°.", rnd))
    its.append(dq(fig(rays_svg([0, 50, 180, 230, 300],
                               [(0, 50, 50, "50°", "arc"), (230, 300, 70, "?", "arc"), (300, 360, 60, "60°", "arc")], NAMED, L=86,
                               names={0: "B", 50: "C", 180: "A", 230: "D", 300: "E"}, centre=("O", 115))) +
                  "AB and CD are straight lines that cross at O. ∠BOC = 50° and ∠BOE = 60°. Find ∠DOE.", 70, [130, 50, 120],
                  "Step 1: ∠BOD is next to ∠BOC on the straight line CD: 180° − 50° = 130°. "
                  "Step 2: ∠DOE = ∠BOD − ∠BOE = 130° − 60° = 70°.", rnd))
    its.append(dq(fig(cross_svg(15, 90, ["h", "h", None, None], label=CROSS)) +
                  "Two straight lines cross. The two angles marked <i>h</i> are equal. Find %s." % A("h"), 90, [180, 45, 60],
                  "The two angles are next to each other on a straight line: 2 × ∠<i>h</i> = 180°, so ∠<i>h</i> = 90°. "
                  "(45° comes from 180° ÷ 4, and 60° from 180° ÷ 3.)", rnd))
    its.append(dq(fig(point_svg(0, [90, 150, 60, 60], [None, "150°", "k", "k"], label="angles at a point, two marked k")) +
                  "The angles are at a point. The two angles marked <i>k</i> are equal. Find %s." % A("k"), 60, [120, 105, 15],
                  "The square is 90°. 90° + 150° = 240°. 360° − 240° = 120°, and 120° ÷ 2 = 60°. "
                  "(105° comes from forgetting the right angle.)", rnd))
    its.append(dq(fig(rays_svg([0, 65, 180, 245, 290],
                               [(0, 65, 65, "65°", "arc"), (245, 290, 45, "m", "arc"), (290, 360, 70, "70°", "arc")], lab5, L=86)) + qx % A("m"),
                  45, [115, 110, 65],
                  "Step 1: next to 65° on the straight line is 180° − 65° = 115°. "
                  "Step 2: the angle below, between the sloping line and the flat line, is vertically opposite it, so it is 115°. "
                  "Step 3: ∠<i>m</i> = 115° − 70° = 45°.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(line_svg(0, [61, 59, 60], ["61°", "n", "60°"], L=100)) +
                   "%s says %s = 60°, because all three angles look equal. Is %s right?" % (n, A("n"), he),
                   "No, ∠n = 59°", ["Yes, ∠n = 60°", "No, ∠n = 61°", "No, ∠n = 239°"],
                   "61° + 60° = 121°, and 180° − 121° = 59°. The angles look almost the same, but they are not equal.", rnd))
    its.append(dq(fig(point_svg(15, [50, 50, 50, 105, 105], ["50°", "50°", "50°", "s", "s"], L=84,
                                label="five angles at a point, two marked s")) +
                  "The angles are at a point. The two angles marked <i>s</i> are equal. Find %s." % A("s"), 105, [210, 15, 50],
                  "50° + 50° + 50° = 150°. 360° − 150° = 210°, and 210° ÷ 2 = 105°.", rnd))
    its.append(dq(fig(rays_svg([0, 40, 90, 180], [(0, 40, 40, "40°", "arc"), (40, 90, 50, "t", "arc"), (90, 180, 90, None, "right")],
                               "angles on a straight line with a right angle", L=92)) +
                  LINE_Q % A("t"), 50, [140, 40, 230],
                  "The square shows a right angle (90°). 90° + 40° = 130°, and 180° − 130° = 50°. (Or: 90° − 40° = 50°.)", rnd))
    its.append(mcq(fig(cross_svg(25, 128, ["128°", "u", "v", None], label=CROSS)) +
                   "Two straight lines cross. Find ∠<i>u</i> and ∠<i>v</i>.",
                   "u = 52°, v = 128°", ["u = 128°, v = 52°", "u = 52°, v = 52°", "u = 232°, v = 128°"],
                   "∠<i>u</i> is on a straight line with 128°: 180° − 128° = 52°. ∠<i>v</i> is vertically opposite 128°, so ∠<i>v</i> = 128°.", rnd))
    its.append(dq(fig(point_svg(0, [60] * 6, ["w"] * 6, L=84, label="six equal angles made by three straight lines")) +
                  "Three straight lines cross at one point and make six equal angles. Find %s." % A("w"), 60, [30, 120, 45],
                  "Angles at a point add up to 360°. 360° ÷ 6 = 60°. (30° comes from 180° ÷ 6.)", rnd))
    its.append(dq(fig(rays_svg([0, 180, 50, 250],
                               [(0, 50, 50, "50°", "arc"), (180, 250, 70, "70°", "arc"), (250, 360, 110, "x", "arc")],
                               "a straight line and two lines from a point on it", L=86)) +
                  "The flat line is straight. Find %s." % A("x"), 110, [130, 70, 240],
                  "The 70° angle and ∠<i>x</i> are on the straight line below it: 180° − 70° = 110°. The 50° angle does not help here.", rnd))
    its.append(mcq(fig(rays_svg([0, 50, 120, 180, 230, 300],
                                [(0, 50, 50, "a", "arc"), (50, 120, 70, "b", "arc"), (120, 180, 60, "c", "arc"),
                                 (180, 230, 50, "d", "arc"), (230, 300, 70, "e", "arc"), (300, 360, 60, "f", "arc")], THREE, L=82)) +
                   "Three straight lines meet at a point. Which angle is vertically opposite %s?" % A("b"),
                   "∠e", ["∠c", "∠d", "∠f"],
                   "Follow the two lines that make ∠<i>b</i> through the crossing point. The angle between them on the other side is ∠<i>e</i>.", rnd))
    its.append(dq(fig(line_svg(15, [90, 48, 42], [None, "y", "42°"])) +
                  LINE_Q % A("y"), 48, [138, 228, 42],
                  "The square is 90°. 90° + 42° = 132°, and 180° − 132° = 48°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find unknown angles in figures", "items": its}


# ------------------------------------------------------------ set 5: multi-step and word problems
def set_problems(rnd, P):
    its = []
    its.append(dq(fig(ratio_bars(["a", "b"], [2, 3], 36, 1, "180°")) +
                  "%s and %s are on a straight line. %s : %s = 2 : 3. Find %s." % (A("a"), A("b"), A("a"), A("b"), A("b")),
                  108, [72, 216, 144],
                  "5 units = 180°. 1 unit = 180° ÷ 5 = 36°. ∠<i>b</i> = 3 units = 3 × 36° = 108°. "
                  "(72° is ∠<i>a</i>. 216° comes from using 360°.)", rnd))
    its.append(dq(fig(ratio_bars(["p", "q", "r"], [3, 4, 5], 30, 2, "360°")) +
                  "%s, %s and %s are at a point. %s : %s : %s = 3 : 4 : 5. Find %s." % (A("p"), A("q"), A("r"), A("p"), A("q"), A("r"), A("r")),
                  150, [75, 120, 90],
                  "12 units = 360°. 1 unit = 360° ÷ 12 = 30°. ∠<i>r</i> = 5 units = 5 × 30° = 150°. (75° comes from using 180°.)", rnd))
    its.append(dq(fig(bar_svg([("m", [(70, ""), (40, "40°")], "?"), ("n", [(70, "")], "")], "180°", 2.1,
                              "angle m is 40 degrees more than angle n, total 180 degrees")) +
                  "%s and %s are on a straight line. %s is 40° more than %s. Find %s." % (A("m"), A("n"), A("m"), A("n"), A("m")),
                  110, [70, 90, 200],
                  "Take away the extra 40°: 180° − 40° = 140°. That is 2 equal units, so 1 unit = 70°. "
                  "∠<i>m</i> = 70° + 40° = 110°. (90° comes from making the angles equal; 200° from using 360°.)", rnd))
    its.append(dq(fig(ratio_bars(["c", "d"], [1, 5], 30, None, "180°")) +
                  "%s and %s are on a straight line. %s : %s = 1 : 5. How much bigger is %s than %s?" % (A("c"), A("d"), A("c"), A("d"), A("d"), A("c")),
                  120, [150, 240, 30],
                  "6 units = 180°, so 1 unit = 30°. ∠<i>d</i> is 4 units more than ∠<i>c</i>: 4 × 30° = 120°. "
                  "(150° is ∠<i>d</i> itself; 240° comes from using 360°.)", rnd))
    its.append(dq(fig(line_svg(0, [45, 135], ["e", "f"], label="angles e and f on a straight line")) +
                  "The angles are on a straight line. %s is 3 times as big as %s. Find %s." % (A("f"), A("e"), A("f")), 135, [45, 270, 60],
                  "∠<i>e</i> is 1 unit and ∠<i>f</i> is 3 units: 4 units = 180°, so 1 unit = 45°. ∠<i>f</i> = 3 × 45° = 135°. "
                  "(60° comes from 180° ÷ 3.)", rnd))
    its.append(dq(fig(point_svg(90, [105, 85, 85, 85], ["105°", None, None, "g"], label="angles at a point, three marked equal",
                                eqs={1: 1, 2: 1, 3: 1})) +
                  "The angles are at a point. The angles with the same mark are equal. Find %s." % A("g"), 85, [255, 90, 25],
                  "360° − 105° = 255°. The three equal angles share it: 255° ÷ 3 = 85°. (90° comes from 360° ÷ 4; the four angles are not all equal. 25° comes from using 180°.)", rnd))
    its.append(dq(fig(rays_svg([0, 35, 70, 125, 180],
                               [(0, 35, 35, "35°", "arc", 1), (35, 70, 35, None, "arc", 1), (70, 125, 55, "h", "arc", 2),
                                (125, 180, 55, None, "arc", 2)], "angles on a straight line, two pairs marked equal", L=100)) +
                  "The angles are on a straight line. Angles with the same mark are equal. Find %s." % A("h"), 55, [110, 145, 90],
                  "The two angles with one dash are 35° each: 35° + 35° = 70°. 180° − 70° = 110°. "
                  "The two angles with two dashes share it: 110° ÷ 2 = 55°. (90° comes from 180° ÷ 2, which leaves out the 35° angles.)", rnd))
    its.append(dq(fig(rays_svg([0, 64, 122, 180, 244],
                               [(0, 64, 64, "64°", "arc"), (64, 122, 58, "k", "arc", 1), (122, 180, 58, None, "arc", 1)],
                               "two crossing lines and a line splitting one angle into two equal angles", L=90)) +
                  "Two straight lines cross. A third line splits one angle into two equal angles. Find %s." % A("k"), 58, [116, 64, 148],
                  "Next to 64° on the straight line: 180° − 64° = 116°. The two equal angles share it: 116° ÷ 2 = 58°. "
                  "(148° comes from using 360°.)", rnd))
    its.append(dq(fig(rays_svg([0, 40, 110, 180],
                               [(0, 40, 40, "40°", "arc"), (40, 110, 70, None, "arc", 1), (110, 180, 70, "?", "arc", 1)],
                               NAMED, L=92, names={0: "B", 40: "D", 110: "C", 180: "A"}, centre=("O", 270))) +
                  "AOB is a straight line. ∠AOC = ∠COD and ∠BOD = 40°. Find ∠AOC.", 70, [140, 160, 40],
                  "180° − 40° = 140°. ∠AOC and ∠COD are equal, so each is 140° ÷ 2 = 70°. (160° comes from using 360°.)", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(point_svg(20, [118, 120, 122], ["118°", "120°", "v"])) +
                   "%s says %s = 120°, because it looks the same as the 120° angle. Is %s right?" % (n, A("v"), he),
                   "No, ∠v = 122°", ["Yes, ∠v = 120°", "No, ∠v = 118°", "No, ∠v = 238°"],
                   "118° + 120° = 238°, and 360° − 238° = 122°. Angles that look equal are not always equal: calculate.", rnd))
    its.append(dq("A pair of scissors is like two straight lines crossing at the screw. The handles are opened to an angle of 35°. "
                  "Find the angle between the blades.", 35, [145, 325, 55],
                  "The angle between the blades is vertically opposite the angle between the handles, so it is equal: 35°.", rnd))
    its.append(dq("The legs of a folding chair at a void deck event cross like an X. The angle between the legs at the top is 50°. "
                  "Find the angle between the legs at the side of the X.", 130, [50, 310, 40],
                  "The side angle is next to the 50° angle on a straight leg, so it is 180° − 50° = 130°. (50° is the vertically opposite angle at the bottom.)", rnd))
    n, he, his = P.next()
    its.append(dq("Mdm Wong cuts a round pandan cake into 8 equal slices. Every cut goes through the centre. %s eats 3 slices. "
                  "Find the angle at the centre made by the slices that are left." % n,
                  225, [135, 45, 180],
                  "Each slice is 360° ÷ 8 = 45°. 5 slices are left: 5 × 45° = 225°. (135° is the 3 slices that were eaten.)", rnd))
    its.append(dq("The ceiling fan in an HDB flat has 3 blades spaced equally around the centre. Find the angle between two blades next to each other.",
                  120, [60, 90, 180],
                  "The blades share a complete turn: 360° ÷ 3 = 120°. (60° comes from using 180°.)", rnd))
    its.append(dq("Two straight roads cross at a junction. One angle between them is 72°. Find the sum of the two obtuse angles.", 216, [108, 144, 288],
                  "Each obtuse angle is 180° − 72° = 108°. The two obtuse angles are vertically opposite, so they are equal: 108° + 108° = 216°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s faces north. %s turns clockwise until %s faces south-east. Find the angle %s turns through." % (n, cap(he), he, he), 135,
                  [45, 225, 90],
                  "North to east is a right angle (90°). East to south-east is half a right angle (45°). 90° + 45° = 135°.", rnd))
    its.append(dq("A ladder stands on a flat floor and leans against a wall. The angle between the ladder and the floor on the wall side is 68°. "
                  "Find the angle between the ladder and the floor on the other side.", 112, [292, 68, 22],
                  "The two angles are on the straight floor, so they add up to 180°. 180° − 68° = 112°.", rnd))
    n, he, his = P.next()
    its.append(dq("%s opens a paper fan until its two outer edges make a straight line. The fan has 6 equal sections. Find the angle of each section." % n,
                  30, [60, 36, 150],
                  "The sections share a straight angle: 180° ÷ 6 = 30°. (60° comes from using 360°.)", rnd))
    its.append(dq("A bicycle wheel has 10 spokes spaced equally around the centre. Find the angle between two spokes next to each other.",
                  36, [18, 72, 30],
                  "The spokes share a complete turn: 360° ÷ 10 = 36°. (18° comes from using 180°.)", rnd))
    its.append(dq("Two straight paths at East Coast Park cross. One of the four angles is 58°. Find the sum of the other three angles.",
                  302, [122, 244, 180],
                  "The four angles are at a point, so they add up to 360°. 360° − 58° = 302°. "
                  "Check: 122° + 58° + 122° = 302°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Multi-step and word problems: equal angles and ratio", "items": its}


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
    named = cross_svg(0, 70, ["70°", "110°", "70°", None], L=80, label=NAMED,
                      names={0: "B", 70: "D", 180: "A", 250: "C"}, centre=("O", 305))
    model = ratio_bars(["a", "b"], [2, 3], 36, 1, "180°")
    return (
        "<h2>Three angle facts</h2>"
        "<p>To find an unknown angle, look for the <b>fact</b> that fits the figure. Add the angles you know, then subtract from the total.</p>"
        "<figure class='sn-fig'>" + facts +
        "<figcaption>Angles on a straight line add up to 180°. Angles at a point add up to 360°. "
        "When two straight lines cross, the vertically opposite angles are equal.</figcaption></figure>" +
        table(["Where the angles are", "Angle fact"], [
            ["On a straight line", "They add up to 180°"],
            ["At a point (all the way round)", "They add up to 360°"],
            ["Vertically opposite (two straight lines cross)", "They are equal"],
            ["Next to each other where two lines cross", "They add up to 180°"],
        ]) +
        "<h2>Worked examples</h2>" +
        ex("Straight line", "Three angles on a straight line are 48°, 70° and ∠<i>a</i>. Find ∠<i>a</i>.",
           "Straight line, so the total is 180°. 48° + 70° = 118°. 180° − 118° = 62°. Check: 48° + 70° + 62° = 180°.", "62°") +
        ex("At a point", "Angles at a point are 200°, 95° and ∠<i>b</i>. Find ∠<i>b</i>.",
           "At a point, so the total is 360°. 200° + 95° = 295°. 360° − 295° = 65°.", "65°") +
        "<figure class='sn-fig'>" + named +
        "<figcaption>∠AOC is vertically opposite ∠BOD. ∠AOD is next to ∠BOD on the straight line AB.</figcaption></figure>" +
        ex("Named angles", "AB and CD are straight lines that cross at O. ∠BOD = 70°. Find ∠AOC and ∠AOD.",
           "∠AOC is vertically opposite ∠BOD, so ∠AOC = 70°. ∠AOD is on the straight line AB with ∠BOD: 180° − 70° = 110°.",
           "∠AOC = 70°, ∠AOD = 110°") +
        "<figure class='sn-fig'>" + model +
        "<figcaption>∠<i>a</i> : ∠<i>b</i> = 2 : 3 on a straight line. 5 units = 180°.</figcaption></figure>" +
        ex("Ratio of angles", "∠<i>a</i> and ∠<i>b</i> are on a straight line. ∠<i>a</i> : ∠<i>b</i> = 2 : 3. Find ∠<i>b</i>.",
           "Draw a model: ∠<i>a</i> is 2 units and ∠<i>b</i> is 3 units. 5 units = 180°, so 1 unit = 36°. ∠<i>b</i> = 3 × 36° = 108°.", "108°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using 360° for a straight line, or 180° at a point", "Straight line: 180°. All the way round: 360°"],
            ["Thinking two angles are equal because they look the same", "Angles are equal only if a fact says so: vertically opposite, or marked equal. Then calculate"],
            ["Taking angles next to each other as vertically opposite", "Vertically opposite angles are across the crossing point. Angles next to each other add up to 180°"],
            ["Giving the total of the known angles as the answer", "Add the known angles, then subtract the total from 180° or 360°"],
        ])
    )


FAQ = [
    {"q": "What is taught about angles in P5 maths?",
     "a": "Primary 5 students learn that angles on a straight line add up to 180°, angles at a point add up to 360° and vertically opposite angles are equal. "
          "They use these facts to find unknown angles in figures."},
    {"q": "How do I help my child find an unknown angle?",
     "a": "Ask which fact fits the figure first: straight line (180°), at a point (360°) or vertically opposite (equal). "
          "Then add the known angles and subtract from the total, for example 180° − 48° − 70° = 62°."},
    {"q": "What is the most common mistake with angles?",
     "a": "Using 360° for angles on a straight line, and thinking two angles are equal just because they look the same. "
          "Angles are equal only when a fact or a mark shows it, so always calculate."},
    {"q": "Is this in the MOE syllabus for Primary 5?",
     "a": "Yes. Angles on a straight line, angles at a point and vertically opposite angles are in the Primary 5 Geometry content of the MOE 2021 Primary Mathematics Syllabus. "
          "Primary 6 builds on them in geometry questions for the PSLE."},
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
    rnd = random.Random(65813)
    P = People(rnd)
    sets = [set_line(rnd, P), set_point(rnd, P), set_vertical(rnd, P), set_figures(rnd, P), set_problems(rnd, P)]
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
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "angles", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Angles: Straight Lines, Angles at a Point and Vertically Opposite Angles",
        "seo_title": "P5 Angles Worksheets: Free Primary 5 Maths Practice on Unknown Angles with Answers (MOE Syllabus)",
        "short_title": "Angles",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 5: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Angles on a straight line; angles at a point; vertically opposite angles; finding unknown angles",
        "meta_desc": "Free P5 angles practice: angles on a straight line (180°), at a point (360°), vertically opposite angles and unknown angles. 100 questions with answers.",
        "key_big": "Angles on a straight line add up to 180°, angles at a point add up to 360°, and vertically opposite angles are equal.",
        "key_sub": "Example: on a straight line with 48° and 70°, the unknown angle is 180° − 48° − 70° = 62°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return u


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
        mark_large(u, "(bar model|angles on a straight line|three straight lines|two crossing lines|a straight line and two lines|six equal angles|straight lines with named)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
