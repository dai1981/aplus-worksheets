# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Measuring Angles (4.MD.C.5-7)
  python tools/gen_us_math_g4_angles.py
HTML attributes use single quotes (no backslashes in the JSON).

Every angle is drawn exactly at its degree value (computed with trig; math angles,
0 deg = pointing right, counterclockwise, SVG y goes down).
Every figure is checked: no label may touch a ray, an arc, a tick mark or another label,
and the viewBox is computed from everything that is drawn.
Protractor: inner scale has 0 on the right, outer scale has 0 on the left.
Tick marks every 5 deg, labels every 10 deg on both scales.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#9a9187"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def D(v):
    return "%d°" % v


def num_of(c):
    m = re.match(r"(?:about )?(-?\d+)°", c)
    return int(m.group(1)) if m else None


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no degree values of 0 or less, or above 360)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        n = num_of(c)
        if c in seen or not c or (n is not None and not 0 < n <= 360):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=True):
    """Approximate text width (Arial): digits 0.556 em, degree sign 0.4 em, capitals 0.72 em."""
    w = 0
    for ch in str(t):
        w += 0.4 if ch == "°" else (0.72 if ch.isupper() else 0.6 if ch == "?" else 0.556)
    return w * fs * (1.04 if bold else 1)


# ------------------------------------------------------------ drawing kit with collision checks
class Pic:
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


def pol(V, r, deg):
    t = math.radians(deg)
    return (V[0] + r * math.cos(t), V[1] - r * math.sin(t))


def place_label(P, V, a, b, r, t, fs=16, col=INK):
    """Put a label for the angle from a to b outside its arc (radius r), as close as it fits."""
    mid = (a + b) / 2.0
    rl = r + 6
    while rl < 400:
        c = pol(V, rl, mid)
        bx = P.box_of(c[0], c[1], t, fs)
        corners = [(bx[0], bx[1]), (bx[2], bx[1]), (bx[0], bx[3]), (bx[2], bx[3])]
        if min(math.hypot(p[0] - V[0], p[1] - V[1]) for p in corners) >= r + 4 and P.clear(bx, 3):
            P.label(c[0], c[1], t, fs, col)
            return rl + math.hypot(bx[2] - bx[0], bx[3] - bx[1]) / 2
        rl += 1
    raise AssertionError("no room for label " + t)


def angle_svg(rays, arcs, label, letters=None, squares=(), L=None, line_ends=(), square=False):
    """rays: directions (deg). arcs: (a, b, r, text or '', colour). letters: {direction: letter, 'V': letter}.
    The rays are drawn long enough that every label sits inside the angle it names."""
    V = (0.0, 0.0)
    need = 0
    for _ in range(2):            # first pass: find how long the rays must be
        P = Pic()
        RL = max(L or 78, need)
        for d in rays:
            P.ray(V, d, RL)
        for s in squares:
            P.square_mark(V, s)
        for a, b, r, t, col in arcs:
            P.arc(V, r, a, b, col=col)
        P.dot(V)
        for a, b, r, t, col in arcs:
            if t:
                need = max(need, place_label(P, V, a, b, r, t, 16, RED if t == "?" else INK) + 14)
        if RL >= need:
            break
    if letters:
        for d, ch in letters.items():
            if d == "V":
                # vertex letter: opposite the middle of all rays
                sx = sum(math.cos(math.radians(x)) for x in rays)
                sy = sum(math.sin(math.radians(x)) for x in rays)
                op = math.degrees(math.atan2(-sy, -sx))
                c = pol(V, 16, op)
            else:
                c = pol(V, RL + 14, d)
            P.label(c[0], c[1], ch, 16, INK)
    return P.svg(label, square=square)[0]


# ------------------------------------------------------------ figures
def turn_svg(n4, size=130, label=None):
    """A turn of n4 quarter turns (1..4) starting from the ray pointing right, counterclockwise."""
    P = Pic()
    c = size / 2.0
    V = (c, c)
    R = c - 14
    P.arc(V, R, 0, 360, col=GRAY, sw=1.4)
    P.el[-1] = (1, P.el[-1][1].replace("stroke-width='1.4'", "stroke-width='1.4' stroke-dasharray='4 4'"))
    deg = 90 * n4
    P.arc(V, R - 2, 0, deg, col=None, fill=FILL)
    P.ray(V, 0, R + 8)
    if deg < 360:
        P.ray(V, deg, R + 8, col=RED)
    # turning arrow
    end = min(deg, 345) if deg == 360 else deg
    ra = 24
    P.arc(V, ra, 8, end - 6, col=INK, sw=2.2)
    tip = pol(V, ra, end - 2)
    a1, a2 = pol(tip, 9, end - 2 - 90 - 25 + 0), pol(tip, 9, end - 2 - 90 + 25)
    P.el.append((1, "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (tip + a1 + a2 + (INK,))))
    P.dot(V)
    s, W, H = P.svg(label or "turn of %d degrees" % deg, pad=0, square=True)
    return s


def clock_svg(h, size=150):
    """Clock at h:00. The angle from the minute hand (12) clockwise to the hour hand is shaded."""
    P = Pic()
    c = size / 2.0
    V = (c, c)
    R = c - 4
    P.el.append((0, "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='4'/>" % (c, c, R, GREEN)))
    P.pts += [pol(V, R + 2, t) for t in range(0, 360, 3)]
    deg = 30 * h
    P.arc(V, R - 16, 90 - deg, 90, col=None, fill=FILL)
    P.arc(V, 22, 90 - deg, 90, col=RED, sw=2.4)
    for i in range(60):
        a = 90 - i * 6
        r1 = R - (10 if i % 5 == 0 else 5)
        P.line(pol(V, r1, a), pol(V, R - 2, a), INK, 2.4 if i % 5 == 0 else 1, cap_="butt")
    for n in range(1, 13):
        p = pol(V, R - 22, 90 - 30 * n)
        P.label(p[0], p[1], str(n), 15, INK, check=False)
    P.line(V, pol(V, R - 43, 90 - deg), INK, 7)
    P.line(V, pol(V, R - 34, 90), RED, 4)
    P.dot(V, 5)
    s, W, H = P.svg("clock showing %d:00 with the angle between the hands" % h, pad=0, square=True)
    return s


PR = 185          # protractor radius
PO, PI = 18, 31   # outer and inner label radius, measured in from the edge


def protractor_svg(rays, label=None, mark=True):
    """Protractor centered on the vertex. rays: directions in deg (0 = right). Rays are red and cross the scales."""
    P = Pic()
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


# ------------------------------------------------------------ set 1: angles as turns
def turn_cands(deg):
    return {90: [D(25), D(180), D(360)], 180: [D(50), D(90), D(360)], 270: [D(75), D(180), D(90)],
            360: [D(100), D(180), D(270)]}[deg]


def set_turns(rnd):
    its = []
    names = {1: "a 1/4 turn", 2: "a 1/2 turn", 3: "a 3/4 turn", 4: "a full turn"}
    whys = {
        1: "A full turn is 360°. A 1/4 turn is one of 4 equal parts: 90°. It makes a right angle. (25° would be true only if a circle had 100 degrees.)",
        2: "A 1/2 turn is half of 360°: 180°. The two rays point in opposite directions and make a straight line.",
        3: "A 3/4 turn is 3 quarter turns: 90° + 90° + 90° = 270°.",
        4: "A full turn goes all the way around and comes back to the start: 360°.",
    }
    qs = {1: "The red ray turned from the green ray. How many degrees is this turn?",
          2: "How many degrees is the turn shown?",
          3: "The ray turned 3 quarter turns. How many degrees is that?",
          4: "The ray turned all the way around. How many degrees is that?"}
    for n4 in (1, 2, 3, 4):
        its.append(mcq(fig(turn_svg(n4)) + qs[n4], D(90 * n4), turn_cands(90 * n4), whys[n4], rnd))
    its.append(mcq("How many degrees are in a full turn (a whole circle)?", D(360), [D(100), D(180), D(90)],
                   "A full turn is 360°. Half a turn is 180° and a quarter turn is 90°.", rnd))
    its.append(mcq("An angle that turns through " + fr(1, 360) + " of a circle measures ___.", "1 degree",
                   ["1 right angle", "360 degrees", "1 full turn"],
                   "A circle is cut into 360 tiny equal turns. Each one is 1 degree (1°).", rnd))
    its.append(mcq("What fraction of a full turn is 1°?", fr(1, 360), [fr(1, 100), fr(1, 180), fr(1, 90)],
                   "A full turn is 360 one-degree angles, so 1° is " + fr(1, 360) + " of a turn.", rnd))
    its.append(mcq("An angle turns through 75 one-degree angles. What is its measure?", D(75), [D(76), D(285), D(105)],
                   "75 one-degree angles make 75°. (76° comes from counting the marks instead of the spaces between them.)", rnd))
    its.append(mcq("An angle turns through 140 one-degree angles. What is its measure?", D(140), [D(141), D(220), D(40)],
                   "Each one-degree angle adds 1°: 140 of them make 140°.", rnd))
    its.append(mcq("How many 1/4 turns make a full turn?", "4", ["2", "3", "90"],
                   "4 quarter turns of 90° make 360°: 90° + 90° + 90° + 90° = 360°.", rnd))
    its.append(mcq("What fraction of a full turn is 180°?", fr(1, 2), [fr(1, 4), fr(3, 4), fr(1, 180)],
                   "180° is half of 360°, so it is a 1/2 turn.", rnd))
    its.append(mcq("What fraction of a full turn is 90°?", fr(1, 4), [fr(1, 2), fr(3, 4), fr(1, 90)],
                   "90° + 90° + 90° + 90° = 360°, so 90° is 1 of 4 equal parts: a 1/4 turn.", rnd))
    for h in (3, 6, 1, 2, 4, 5):
        deg = 30 * h
        wrong = [D(5 * h), D(360 - deg), D(30 * (h + 1)), D(h)]
        if h == 1:
            e = "Each hour space is 30° (360° ÷ 12). From 12 to 1 is 1 hour space: 30°."
        else:
            e = ("Each hour space is 30° (360° ÷ 12). From 12 to %d is %d hour spaces: %s = %d°."
                 % (h, h, " + ".join(["30°"] * h) if h <= 3 else "%d × 30°" % h, deg))
        if h == 3:
            e += " That is a 1/4 turn, a right angle."
        if h == 6:
            e += " That is a 1/2 turn, a straight angle."
        its.append(mcq(fig(clock_svg(h)) + "What is the measure of the shaded angle between the clock hands?",
                       D(deg), wrong, e, rnd))
    its.append(mcq("A clock face is a full turn split into 12 equal hour spaces. How many degrees is each hour space?", D(30),
                   [D(12), D(5), D(60)],
                   "360° ÷ 12 = 30°. (5 is the number of minutes in each hour space, not the degrees.)", rnd))
    its.append(mcq("The minute hand moves from 12 to 9, the long way round (clockwise). How many degrees does it turn?", D(270),
                   [D(90), D(45), D(180)],
                   "12 to 3, 3 to 6 and 6 to 9 are three quarter turns: 3 × 90° = 270°. (90° is the short way back from 9 to 12.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles as turns: degrees, quarter turns and clocks", "items": its}


# ------------------------------------------------------------ set 2: read a protractor
def read_cands(v):
    c = [D(180 - v)]
    if v % 10 == 5:
        c += [D(v - 4), D(v + 5), D(v - 5)]       # counted the 5-degree mark as 1 degree; read the next number
    else:
        c += [D(v + 10), D(v - 10), D(v + 1)]
    return c


def set_protractor(rnd):
    its = []
    # one ray on 0 of the inner scale (right side)
    for v in (50, 30, 65, 120, 145, 80, 160):
        e = ("The bottom ray points to 0 on the right, so read the <b>inner</b> scale, which starts at 0 on the right. "
             "The other ray crosses it at %d°." % v)
        if v % 10 == 5:
            e += " The marks go by 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " The outer scale says %d there, but that scale starts from the other side." % (180 - v)
        e += " The angle is %s, so %d° makes sense." % ("smaller than a right angle" if v < 90 else "bigger than a right angle", v)
        its.append(mcq(fig(protractor_svg([0, v], "protractor angle %d degrees" % v)) + "What is the measure of the angle?",
                       D(v), read_cands(v), e, rnd))
    # one ray on 0 of the outer scale (left side)
    for v in (50, 40, 115, 135, 75, 100, 25):
        d = 180 - v
        e = ("The bottom ray points to 0 on the left, so read the <b>outer</b> scale, which starts at 0 on the left. "
             "The other ray crosses it at %d°." % v)
        if v % 10 == 5:
            e += " The marks go by 5s, so the mark between %d and %d is %d." % (v - 5, v + 5, v)
        e += " (The inner scale says %d there.)" % (180 - v)
        e += " The angle is %s, so %d° makes sense." % ("smaller than a right angle" if v < 90 else "bigger than a right angle", v)
        its.append(mcq(fig(protractor_svg([180, d], "protractor angle %d degrees" % v)) + "What is the measure of the angle?",
                       D(v), read_cands(v), e, rnd))
    # neither ray on 0
    for a, b in ((30, 110), (20, 75), (60, 150)):
        v = b - a
        its.append(mcq(fig(protractor_svg([a, b], "protractor angle between %d and %d" % (a, b))) +
                       "Neither ray is on 0. What is the measure of the angle?", D(v),
                       [D(b), D(a + b), D(180 - b), D(a)],
                       "On the inner scale one ray is at %d and the other is at %d. The angle is the difference: %d° − %d° = %d°."
                       % (a, b, b, a, v), rnd))
    its.append(mcq("Where do you put the center mark of a protractor when you measure an angle?", "on the vertex",
                   ["at the end of a ray", "on the 90 mark", "in the middle of a ray"],
                   "The center mark goes on the vertex, the point where the two rays meet. Then line up one ray with 0.", rnd))
    its.append(mcq("One ray of an angle is on the 0 of the outer scale. Which numbers should you read?", "the outer scale",
                   ["the inner scale", "the bigger number", "the smaller number"],
                   "Read the scale that starts at 0 on your ray. Here that is the outer scale.", rnd))
    its.append(mcq("Ana measures an angle that is clearly wider than a right angle. Her protractor shows 55 and 125 where the ray crosses. "
                   "What is the angle?", D(125), [D(55), D(180), D(70)],
                   "An angle wider than a right angle is more than 90°, so it is 125°. 55° is the reading on the wrong scale.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a protractor: inner and outer scales", "items": its}


# ------------------------------------------------------------ set 3: kinds of angles and estimates
KIND_E = {
    "acute": "An acute angle is smaller than a right angle: less than 90°.",
    "right": "A right angle is exactly 90°, a square corner. The small square shows it.",
    "obtuse": "An obtuse angle is bigger than a right angle but smaller than a straight angle: between 90° and 180°.",
    "straight": "A straight angle is 180°. The two rays point in opposite directions and make a straight line.",
}
KINDS = ["acute", "right", "obtuse", "straight"]


def kind(d):
    return "acute" if d < 90 else "right" if d == 90 else "obtuse" if d < 180 else "straight"


def simple_angle(d, rot, label, r=26):
    sq = (rot,) if d == 90 else ()
    arcs = [] if d == 90 else [(rot, rot + d, r, "", GREEN)]
    return angle_svg([rot, rot + d], arcs, label, squares=sq, L=82)


def set_kinds(rnd):
    its = []
    for d, rot in ((30, 10), (90, 0), (120, 15), (180, 0), (60, 100), (145, 200), (90, 35), (20, 120)):
        e = KIND_E[kind(d)] + " This angle is %d°." % d
        if d == 90 and rot % 90:
            e += " Turning an angle does not change its size."
        its.append(mcq(fig(simple_angle(d, rot, "%s angle" % kind(d))) + "What kind of angle is this?",
                       kind(d), [k for k in KINDS if k != kind(d)], e, rnd))
    est = [(28, 0, [30, 90, 150, 60]), (62, 20, [60, 120, 30, 90]), (122, 5, [120, 60, 90, 180]),
           (148, 10, [150, 30, 90, 120]), (47, 70, [45, 135, 90, 15]), (170, 5, [180, 10, 90, 135])]
    for d, rot, ch in est:
        best = min(ch, key=lambda x: abs(x - d))
        other = 180 - best
        wrong = ["about %s" % D(x) for x in ([other] + ch) if x != best]
        e = ("Compare with a right angle (90°). This angle is %s a right angle%s, so about %d° fits. (It is %d°.) "
             "About %d° is %s a right angle, so it cannot be the answer."
             % ("smaller than" if d < 90 else "bigger than", "" if d < 90 or d > 135 else " but not close to a straight line",
                best, d, other, "wider than" if other > 90 else "smaller than"))
        if best == 180:
            e = ("The rays almost make a straight line (180°), so it is about 180°. (It is %d°.) About 10° is a tiny angle, almost closed." % d)
        its.append(mcq(fig(simple_angle(d, rot, "angle to estimate")) + "Which is the best estimate for this angle?",
                       "about %s" % D(best), wrong, e, rnd))
    its.append(mcq("An angle measures 135°. What kind of angle is it?", "obtuse", ["acute", "right", "straight"],
                   "135° is more than 90° and less than 180°, so it is obtuse.", rnd))
    its.append(mcq("Which angle measure is acute?", D(75), [D(95), D(90), D(180)],
                   "Acute means less than 90°. Only 75° is less than 90°.", rnd))
    its.append(mcq("Which could be the measure of an obtuse angle?", D(140), [D(40), D(90), D(180)],
                   "An obtuse angle is between 90° and 180°. 140° is the only one in that range.", rnd))
    its.append(mcq("How many right angles make a straight angle?", "2", ["4", "1", "3"],
                   "90° + 90° = 180°, so 2 right angles make a straight angle. (4 right angles make a full turn.)", rnd))
    its.append(mcq("Omar says a 100° angle is acute because 100 is a small number. Is he right?", "No, it is obtuse",
                   ["Yes, it is acute", "No, it is right", "No, it is straight"],
                   "100° is more than 90°, so the angle is wider than a right angle. That makes it obtuse.", rnd))
    its.append(mcq("An angle measures 180°. What kind of angle is it?", "straight", ["obtuse", "right", "acute"],
                   "180° is a half turn. The rays make a straight line, so it is a straight angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Acute, right, obtuse and straight: name and estimate", "items": its}


# ------------------------------------------------------------ set 4: adding angles
def add_cands(a, b):
    s = a + b
    c = []
    if a % 10 + b % 10 >= 10:
        c.append(D(s - 10))                 # forgot to regroup
    c += [D(abs(a - b)), D(180 - s), D(s + 10), D(max(a, b))]
    return c


def part_cands(w, a):
    v = w - a
    c = [D(w + a)]
    if a % 10 > w % 10:
        c.append(D(v + 10))                 # regrouping mistake in the subtraction
    c += [D(180 - a) if w != 180 else D(90 - a), D(a), D(v - 10)]
    return c


def split_svg(rot, a, b, show_a, show_b, label):
    rays = [rot, rot + a, rot + a + b]
    arcs = [(rot, rot + a, 30, show_a, GREEN), (rot + a, rot + a + b, 40, show_b, RED if show_b == "?" else GREEN)]
    return angle_svg(rays, arcs, label, letters={rot: "A", "V": "B", rot + a: "D", rot + a + b: "C"}, L=86)


def set_add(rnd):
    its = []
    for a, b, rot in ((40, 35, 10), (25, 60, 0), (55, 45, 20), (70, 50, 5), (35, 85, 15), (90, 45, 0), (65, 75, 10), (110, 30, 0)):
        s = a + b
        e = "Angle measures add: %d° + %d° = %d°. The two parts share ray BD and do not overlap, so together they make angle ABC." % (a, b, s)
        if a % 10 + b % 10 >= 10:
            e += " Remember to regroup: %d + %d = %d." % (a % 10, b % 10, a % 10 + b % 10)
        its.append(mcq(fig(split_svg(rot, a, b, D(a), D(b), "angle ABC split into two parts")) +
                       "Angle ABC is split into two angles by ray BD. What is the measure of angle ABC?",
                       D(s), add_cands(a, b), e, rnd))
    for w, a, rot in ((80, 35, 15), (125, 50, 0), (150, 65, 10), (100, 45, 20), (135, 90, 0), (115, 70, 5), (160, 25, 0), (95, 40, 25)):
        v = w - a
        e = "The two parts add up to the whole: %d° + ? = %d°. Subtract: %d° − %d° = %d°." % (a, w, w, a, v)
        e += " Check: %d° + %d° = %d°." % (a, v, w)
        its.append(mcq(fig(split_svg(rot, a, v, D(a), "?", "angle ABC with one unknown part")) +
                       "Angle ABC measures %d°. What is the measure of angle DBC?" % w,
                       D(v), part_cands(w, a), e, rnd))
    for k, p, rot in ((3, 25, 15), (4, 30, 0)):
        rays = [rot + i * p for i in range(k + 1)]
        arcs = [(rot + i * p, rot + (i + 1) * p, 34, D(p) if i == 0 else "", GREEN) for i in range(k)]
        tot = k * p
        its.append(mcq(fig(angle_svg(rays, arcs, "angle split into %d equal parts" % k, L=90)) +
                       "The angle is split into %d equal parts. One part is %d°. What is the whole angle?" % (k, p),
                       D(tot), [D(p), D((k - 1) * p), D((k + 1) * p)],
                       "There are %d equal parts (count the spaces between the rays, not the rays). %d × %d° = %d°." % (k, k, p, tot), rnd))
    its.append(mcq("Two angles of 45° are put side by side with no gap and no overlap. What angle do they make together?", D(90),
                   [D(45), D(80), D(180)],
                   "Angle measures add: 45° + 45° = 90°. Together they make a right angle.", rnd))
    its.append(mcq("Angle PQR is 120°. Ray QS splits it into two angles. One of them is 75°. What is the other?", D(45),
                   [D(195), D(55), D(105)],
                   "The two parts add up to 120°. 120° − 75° = 45°. Check: 75° + 45° = 120°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angle measures add up", "items": its}


# ------------------------------------------------------------ set 5: unknown angles and word problems
def set_unknown(rnd, P):
    its = []
    # straight line
    for x, known_right, rot in ((40, True, 0), (125, True, 0), (70, False, 0)):
        v = 180 - x
        if known_right:
            arcs = [(rot, rot + x, 28, D(x), GREEN), (rot + x, rot + 180, 36, "?", RED)]
        else:
            arcs = [(rot, rot + v, 36, "?", RED), (rot + v, rot + 180, 28, D(x), GREEN)]
        ray = rot + (x if known_right else v)
        svg = angle_svg([rot, rot + 180, ray], arcs, "angles on a straight line", L=96)
        its.append(mcq(fig(svg) + "The two angles sit on a straight line. What is the unknown angle?", D(v),
                       [D(360 - x), D(abs(90 - x)), D(x), D(v + 10)],
                       "Angles on a straight line add up to 180°. 180° − %d° = %d°. Check: %d° + %d° = 180°." % (x, v, x, v), rnd))
    # right angle split
    for x, rot in ((35, 0), (60, 20), (25, 10)):
        v = 90 - x
        arcs = [(rot, rot + x, 34, D(x), GREEN), (rot + x, rot + 90, 44, "?", RED)]
        svg = angle_svg([rot, rot + x, rot + 90], arcs, "right angle split into two parts", squares=(rot,), L=96)
        its.append(mcq(fig(svg) + "The whole angle is a right angle. What is the unknown angle?", D(v),
                       [D(180 - x), D(90 + x), D(x), D(v + 10)],
                       "A right angle is 90°. 90° − %d° = %d°. (Using 180° would give %d°, but this is a right angle, not a straight line.)"
                       % (x, v, 180 - x), rnd))
    # around a point
    for a, b, rot in ((120, 150, 0), (100, 135, 30), (90, 160, 0)):
        v = 360 - a - b
        arcs = [(rot, rot + a, 20, D(a), GREEN), (rot + a, rot + a + b, 27, D(b), GREEN), (rot + a + b, rot + 360, 34, "?", RED)]
        svg = angle_svg([rot, rot + a, rot + a + b], arcs, "angles around a point", L=80)
        cands = [D(a + b), D(180 - a) if a < 180 else None, D(360 - a), D(v + 10)]
        its.append(mcq(fig(svg) + "Three angles go all the way around a point. What is the unknown angle?", D(v),
                       [c for c in cands if c], "Angles all the way around a point add up to 360°, a full turn. "
                       "%d° + %d° = %d°, and 360° − %d° = %d°." % (a, b, a + b, a + b, v), rnd))
    # word problems
    n, he, his = P.next()
    its.append(mcq("%s opens a door until it makes a right angle with the wall. Then %s closes it by 35°. "
                   "What angle does the door make with the wall now?" % (n, he), D(55), [D(125), D(145), D(35)],
                   "A right angle is 90°. Closing the door makes the angle smaller: 90° − 35° = 55°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s rides a skateboard. %s turns 90°, then turns 180° more in the same direction. "
                   "How many degrees does %s turn in all?" % (n, cap(he), he), D(270), [D(90), D(180), D(360)],
                   "Turns in the same direction add: 90° + 180° = 270°. That is a 3/4 turn.", rnd))
    its.append(mcq("A round pizza is cut into 4 equal slices from the center. What angle does each slice make at the center?",
                   D(90), [D(45), D(25), D(360)],
                   "The slices go all the way around the center: 360°. 360° ÷ 4 = 90°. (Using 180° would give 45°.)", rnd))
    n, he, his = P.next()
    its.append(mcq("A pie is cut into 6 equal slices. Each slice makes a 60° angle at the center. %s eats 2 slices. "
                   "What angle do the slices that are left make?" % n, D(240), [D(120), D(300), D(60)],
                   "The whole pie is 360°. 2 slices are 2 × 60° = 120°. 360° − 120° = 240°. (Or 4 slices are left: 4 × 60° = 240°.)", rnd))
    its.append(mcq("The minute hand of a clock moves for 20 minutes. How many degrees does it turn?", D(120),
                   [D(20), D(100), D(240)],
                   "Every 5 minutes is one hour space, which is 30°. 20 minutes is 4 spaces: 4 × 30° = 120°.", rnd))
    its.append(mcq("A skate ramp meets the flat ground at a 25° angle. What is the angle between the ramp and the ground on the other side?",
                   D(155), [D(65), D(335), D(25)],
                   "The ground is a straight line, so the two angles add up to 180°. 180° − 25° = 155°.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s opens a pair of scissors to 45°. Then %s opens them 35° more. What is the angle now?" % (n, he),
                   D(80), [D(10), D(70), D(100)],
                   "Opening more makes the angle bigger: 45° + 35° = 80°. (Remember to regroup: 5 + 5 = 10.)", rnd))
    n, he, his = P.next()
    its.append(mcq("A laptop screen is open at 110°. %s pushes it back 15° more. What angle is the screen open at now?" % n,
                   D(125), [D(95), D(165), D(70)],
                   "Pushing the screen back opens it more: 110° + 15° = 125°.", rnd))
    its.append(mcq("A lawn sprinkler sprays water through 60°, then through 70° more. How many more degrees must it turn to make a full turn?",
                   D(230), [D(130), D(50), D(290)],
                   "So far: 60° + 70° = 130°. A full turn is 360°: 360° − 130° = 230°. (Using 180° would give 50°.)", rnd))
    its.append(mcq("Three roads meet at one point. Two of the angles between them are 120° and 135°. What is the third angle?",
                   D(105), [D(255), D(115), D(225)],
                   "The three angles go all the way around the point: 360°. 120° + 135° = 255°, and 360° − 255° = 105°.", rnd))
    its.append(mcq("At 3:00 the hands of a clock make a right angle. What angle do they make at 4:00?",
                   D(120), [D(90), D(30), D(20)],
                   "Each hour space is 30°. At 4:00 the hour hand is 4 spaces from 12: 4 × 30° = 120°. That is 90° + 30°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Unknown angles and word problems", "items": its}


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
        x, y = k * cw + (cw - w) / 2.0, top - h
        inner = re.sub(r"^<svg ", "<svg x='%.1f' y='%.1f' " % (x, y), s)
        out.append(inner)
        out.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                   % (k * cw + cw / 2.0, top + 20, INK, c))
    W, H = int(cw * len(svgs)), top + 28
    return svg_wrap(W, H, "".join(out), label)


def body_html():
    turns = strip_svg([turn_svg(k, 110) for k in (1, 2, 3, 4)], ["1/4 turn = 90°", "1/2 turn = 180°", "3/4 turn = 270°", "full turn = 360°"],
                      "quarter, half, three-quarter and full turns", cw=140)
    prot = protractor_svg([0, 50], "protractor measuring a 50 degree angle")
    kinds = strip_svg([simple_angle(40, 0, "acute angle"), simple_angle(90, 0, "right angle"),
                       simple_angle(130, 0, "obtuse angle"), simple_angle(180, 0, "straight angle")],
                      ["acute: less than 90°", "right: 90°", "obtuse: 90° to 180°", "straight: 180°"],
                      "acute, right, obtuse and straight angles", cw=170)
    split = split_svg(10, 40, 35, D(40), D(35), "angle ABC made of a 40 degree and a 35 degree angle")
    line = angle_svg([0, 180, 50], [(0, 50, 28, D(50), GREEN), (50, 180, 36, D(130), GREEN)], "50 and 130 degrees on a straight line", L=96)
    return (
        "<h2>An angle is a turn</h2>"
        "<p>An <b>angle</b> is made by two <b>rays</b> that start at the same point, the <b>vertex</b>. "
        "Its size is how far one ray turns to reach the other. We measure that turn in <b>degrees</b> (°). "
        "A full turn is <b>360°</b>, so 1° is " + fr(1, 360) + " of a circle.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>A quarter turn is 90°, a right angle. A half turn is 180°, a straight line. "
        "On a clock, each hour space is 360° ÷ 12 = 30°, so the hands make 90° at 3:00.</figcaption></figure>"
        "<h2>Measure with a protractor</h2>"
        "<p>1. Put the center mark on the vertex. 2. Line up one ray with <b>0</b>. "
        "3. Read the scale that <b>starts at 0 on that ray</b>, where the other ray crosses it. "
        "4. Check: is the angle smaller or bigger than a right angle?</p>"
        "<figure class='sn-fig'>" + prot +
        "<figcaption>The bottom ray is on the 0 of the inner (green) scale, so read the inner scale: 50°. "
        "The outer scale says 130 at the same spot, but the angle is smaller than a right angle, so 130° cannot be right. "
        "The small marks go by 5s.</figcaption></figure>"
        "<h2>Kinds of angles</h2>"
        "<figure class='sn-fig'>" + kinds + "</figure>" +
        table(["Kind", "Size", "Example"], [
            ["Acute", "less than 90°", "30°, 75°"],
            ["Right", "exactly 90° (square corner)", "corner of a book"],
            ["Obtuse", "more than 90°, less than 180°", "120°, 145°"],
            ["Straight", "exactly 180°", "a straight line"],
        ]) +
        "<h2>Angle measures add</h2>"
        "<p>When an angle is split into parts that do not overlap, the parts add up to the whole angle. "
        "So you can add to find the whole, or subtract to find a missing part.</p>"
        "<figure class='sn-fig'>" + split +
        "<figcaption>Angle ABC = 40° + 35° = 75°.</figcaption></figure>" +
        ex("Missing part", "Angle ABC is 120°. One part is 75°. What is the other part?",
           "The parts add up to 120°: 75° + ? = 120°. Subtract: 120° − 75° = 45°.", "45°") +
        "<figure class='sn-fig'>" + line +
        "<figcaption>Angles on a straight line add up to 180°: 50° + 130° = 180°.</figcaption></figure>" +
        table(["The angles make…", "They add up to"], [
            ["a right angle", "90°"],
            ["a straight line", "180°"],
            ["a full turn around a point", "360°"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the wrong scale (130° for a 50° angle)", "Read the scale that starts at 0 on your ray, then check: small or big angle?"],
            ["Counting each small mark as 1° (61° instead of 65°)", "Check what the marks count by. On this protractor they go by 5s"],
            ["Not putting the center mark on the vertex", "Put the center mark exactly on the vertex before you read"],
            ["Using 180° when the angles make a right angle or a full turn", "Right angle: 90°. Straight line: 180°. All the way around: 360°"],
            ["Adding when a part is missing", "If you know the whole, subtract the known part"],
        ])
    )


FAQ = [
    {"q": "How do you teach measuring angles in 4th grade?",
     "a": "Start with turns: a quarter turn is 90° and a full turn is 360°. Then use a protractor: center mark on the vertex, one ray on 0, and read the scale that starts at that 0."},
    {"q": "Which number do you read on a protractor, the inner or the outer?",
     "a": "Read the scale that has 0 on the ray you lined up. Then check: if the angle is smaller than a right angle, the answer must be less than 90°."},
    {"q": "What does it mean that angle measure is additive?",
     "a": "If an angle is split into parts that do not overlap, the parts add up to the whole. For example, 40° + 35° = 75°, so a missing part can be found by subtracting."},
    {"q": "What does 4.MD.C.5–7 mean?",
     "a": "They are the Common Core Grade 4 standards on angles: understand degrees as parts of a 360° turn, measure and sketch angles with a protractor, and add and subtract angle measures to find unknown angles."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_angles():
    rnd = random.Random(114)
    P = People(rnd)
    sets = [set_turns(rnd), set_protractor(rnd), set_kinds(rnd), set_add(rnd), set_unknown(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "measuring-angles", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Angles: Degrees, Protractors and Unknown Angles",
        "seo_title": "Grade 4 Measuring Angles Worksheets: Protractor, Degrees, Acute and Obtuse, Unknown Angles",
        "short_title": "Measuring angles",
        "domain": "Measurement and Data",
        "standard_code": "4.MD.C.5–7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/MD/C/",
        "standard_text": "Recognize angles as geometric shapes that are formed wherever two rays share a common endpoint, and understand concepts of angle measurement: an angle that turns through 1/360 of a circle is a one-degree angle. Measure angles in whole-number degrees using a protractor. Sketch angles of specified measure. Recognize angle measure as additive. Solve addition and subtraction problems to find unknown angles on a diagram in real world and mathematical problems.",
        "meta_desc": "Free Grade 4 angle worksheets: angles as turns and degrees, reading the inner and outer scales of a protractor, acute, right, obtuse and straight angles, adding angles, and finding unknown angles in word problems. 100 practice questions with answers.",
        "key_big": "An angle measures a turn. A full turn is 360°, a quarter turn is 90°.",
        "key_sub": "On a protractor, put the center on the vertex, line up one ray with 0, and read the scale that starts at that 0. Angle parts add up: on a straight line to 180°, around a point to 360°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_angles()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "protractor")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
