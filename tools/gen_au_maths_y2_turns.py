# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Turns (Australian Curriculum v9.0, AC9M2M05)
  python3 tools/gen_au_maths_y2_turns.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 2 students identify, describe and demonstrate quarter, half, three-quarter and full turns,
clockwise and anticlockwise, in everyday situations. No right angles (Year 3) and no degrees.
Pictures are drawn exactly: every turn arrow sweeps the right amount, every turned shape is the
start shape rotated by whole quarter turns, and the four pictures in an A-D question are all
different (checked in code). Every label is checked against every line.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
RED = "#c8102e"
GOLD = "#f2b632"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D, turns, clock numbers, the four things around a child)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c >= 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


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


# ------------------------------------------------------------ geometry
def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dirv(deg):
    """Direction for an angle in degrees, anticlockwise on screen (SVG y goes down). 90 = up."""
    t = math.radians(deg)
    return (math.cos(t), -math.sin(t))


def rot_pt(p, deg):
    """Rotate anticlockwise on screen by deg (negative = clockwise)."""
    t = math.radians(deg)
    return (p[0] * math.cos(t) + p[1] * math.sin(t), -p[0] * math.sin(t) + p[1] * math.cos(t))


def seg_hits_box(p, q, box, m):
    x0, y0, x1, y1 = box[0] - m, box[1] - m, box[2] + m, box[3] + m
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return False
        else:
            r = qq / pp
            if pp < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return False
    return True


# ------------------------------------------------------------ drawing
class Fig:
    """Collects SVG elements, their strokes and label boxes; checks that no label touches a stroke."""

    def __init__(self):
        self.el, self.segs, self.boxes, self.ext = [], [], [], []

    def _seg(self, p, q, hw):
        self.segs.append((p, q, hw))
        for a in (p, q):
            self.ext += [(a[0] - hw, a[1] - hw), (a[0] + hw, a[1] + hw)]

    def line(self, p, q, w=3, col=GREEN, dash=None, cap="round"):
        d = " stroke-dasharray='%s'" % dash if dash else ""
        self.el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' "
                       "stroke-linecap='%s'%s/>" % (p[0], p[1], q[0], q[1], col, w, cap, d))
        self._seg(p, q, w / 2.0)

    def dot(self, p, r=4, col=INK):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (p[0], p[1], r, col))
        self._seg(p, p, r)

    def circle(self, p, r, fill=FILL, w=2.5, col=GREEN):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s' stroke='%s' stroke-width='%g'/>"
                       % (p[0], p[1], r, fill, col, w))
        self.ext += [(p[0] - r - w, p[1] - r - w), (p[0] + r + w, p[1] + r + w)]
        self.segs.append((p, p, r + w / 2.0))

    def label(self, p, t, d, off=7, fs=16):
        d = norm(d)
        w, h = len(t) * fs * 0.6, fs * 0.72
        k = off + abs(d[0]) * w / 2 + abs(d[1]) * h / 2
        c = add(p, d, k)
        box = (c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2)
        self.boxes.append(box)
        self.ext += [box[:2], box[2:]]
        self.el.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (c[0], c[1] + h / 2, fs, INK, t))

    def poly(self, pts, fill=FILL, w=3, col=GREEN):
        P = " ".join("%.1f,%.1f" % p for p in pts)
        self.el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                       % (P, fill, col, w))
        n = len(pts)
        for i in range(n):
            self._seg(pts[i], pts[(i + 1) % n], w / 2.0)

    def mark(self, pts, w=1.8, col=INK):
        self.el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round' "
                       "stroke-linecap='round'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col, w))
        for i in range(len(pts) - 1):
            self._seg(pts[i], pts[i + 1], w / 2.0)

    def head(self, tip, d, col=GREEN, L=9, W=6):
        d = norm(d)
        nr = (-d[1], d[0])
        b = add(tip, d, -L)
        pts = [tip, add(b, nr, W), add(b, nr, -W)]
        self.el.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col))
        for i in range(3):
            self._seg(pts[i], pts[(i + 1) % 3], 0.5)

    def render(self):
        for b in self.boxes:
            for p, q, hw in self.segs:
                assert not seg_hits_box(p, q, b, hw + 1.5), ("label touches a stroke", b, p, q)
        for i, b in enumerate(self.boxes):
            for c in self.boxes[i + 1:]:
                assert b[2] + 2 < c[0] or c[2] + 2 < b[0] or b[3] + 2 < c[1] or c[3] + 2 < b[1], "labels overlap"
        xs, ys = [p[0] for p in self.ext], [p[1] for p in self.ext]
        return "".join(self.el), (min(xs), min(ys), max(xs), max(ys))

    def svg(self, label, pad=5):
        body, bb = self.render()
        W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
        if W == H:
            W += 1                                     # keep figures out of the larger 'square' print size
        dx = pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2
        dy = pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2
        return svg_wrap(W, H, "<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body), label)


# ------------------------------------------------------------ turn arrows
TURNS = ["quarter turn", "half turn", "three-quarter turn", "full turn"]
FRAC = {1: "quarter turn", 2: "half turn", 3: "three-quarter turn", 4: "full turn"}


def turn_fig(q, cw=True, start=90, r=30):
    """Dashed start line (direction `start`), a curved arrow for q quarter turns and a solid end line."""
    F = Fig()
    c = (0.0, 0.0)
    F.line(c, add(c, dirv(start), r + 12), w=2.4, col=INK, dash="5 4", cap="butt")
    sweep = 90.0 * q
    sg = -1 if cw else 1
    draw = min(sweep - 20, 330.0)              # the arrowhead stops just before the end line
    n = max(8, int(draw / 5))
    end_a = start + sg * draw
    pts = [add(c, dirv(start + sg * draw * i / n), r) for i in range(n + 1)]
    F.mark(pts, w=3, col=GREEN)
    end = add(c, dirv(end_a), r)
    F.head(add(end, dirv(end_a + sg * 90), 8), dirv(end_a + sg * 90), L=11, W=7)
    if q < 4:
        F.line(c, add(c, dirv(start + sg * sweep), r + 12), w=3, col=INK)
    F.dot(c, 4)
    return F


def turn_svg(q, cw=True, start=90):
    return turn_fig(q, cw, start).svg("arrow showing a %s %s" % (FRAC[q], "clockwise" if cw else "anticlockwise"))


# ------------------------------------------------------------ a child facing one of 4 things (seen from above)
def facing_fig(names, face, fs=16, R=52):
    """names on the 4 sides (top, right, bottom, left); clockwise goes top, right, bottom, left."""
    F = Fig()
    c = (0.0, 0.0)
    for i, t in enumerate(names):
        d = dirv(90 - 90 * i)
        F.label(add(c, d, R), t, d, off=0, fs=fs)
    d = dirv(90 - 90 * face)
    F.circle(c, 11)
    F.line(add(c, d, 13), add(c, d, 30), w=3.4, col=INK, cap="butt")
    F.head(add(c, d, 39), d, col=INK, L=10, W=7)
    return F


def end_side(start, quarters, cw):
    return (start + (quarters if cw else -quarters)) % 4


CLASSROOM = ["board", "window", "door", "desk"]
PLAYGROUND = ["slide", "swings", "canteen", "sandpit"]
BACKYARD = ["house", "shed", "gate", "tree"]
BEACH = ["sea", "kiosk", "car park", "rocks"]


# ------------------------------------------------------------ clocks
def clock_face(s, c):
    s.append("<circle cx='56' cy='56' r='52' fill='#ffffff' stroke='%s' stroke-width='3'/>" % GREEN)
    for i in range(12):
        d = dirv(90 - 30 * i)
        a, b = add(c, d, 47), add(c, d, 41 if i % 3 == 0 else 44)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>"
                 % (a + b + (INK, 2.4 if i % 3 == 0 else 1.4)))
    for num, i in (("12", 0), ("3", 3), ("6", 6), ("9", 9)):
        p = add(c, dirv(90 - 30 * i), 33)
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (p[0], p[1] + 5.4, INK, num))


def hand_svg(pos):
    """Analog clock with one hand (an arrow) pointing at `pos` (12, 3, 6 or 9). Square: printed large."""
    c = (56.0, 56.0)
    s = []
    clock_face(s, c)
    d = dirv(90 - 30 * (pos % 12))
    tip = add(c, d, 25)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
             % (add(c, d, 17) + (RED,)))
    nr = (-d[1], d[0])
    b = add(tip, d, -10)
    s.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in (tip, add(b, nr, 6), add(b, nr, -6))), RED))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "clock with one hand pointing to %d" % pos)


def clock_turn_svg(start, quarters, cw=True):
    """Minute hand dashed where it started (at `start`), solid where it ends after `quarters`
    quarter turns, with a curved arrow for the turn."""
    c = (56.0, 56.0)
    s = []
    clock_face(s, c)
    sg = -1 if cw else 1
    a0 = 90 - 30 * start
    sweep = min(90 * quarters - 24, 330)
    n = max(8, int(sweep / 5))
    r = 15
    pts = [add(c, dirv(a0 + sg * sweep * i / n), r) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (" ".join("%.1f,%.1f" % p for p in pts), GREEN))
    ea = a0 + sg * sweep
    d = dirv(ea + sg * 90)
    tip = add(add(c, dirv(ea), r), d, 8)
    nr = (-d[1], d[0])
    b = add(tip, d, -10)
    s.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in (tip, add(b, nr, 6), add(b, nr, -6))), GREEN))
    p0 = add(c, dirv(a0), 24)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' stroke-dasharray='4 3'/>" % (p0 + (INK,)))
    if quarters < 4:
        p1 = add(c, dirv(a0 + sg * 90 * quarters), 24)
        s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (p1 + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "clock with the minute hand turning %s" % ("clockwise" if cw else "anticlockwise"))


# ------------------------------------------------------------ shapes that turn
SHAPES = {
    "flag": [("line", [(0, 30), (0, -30)], INK), ("poly", [(0, -30), (32, -19), (0, -8)], RED)],
    "L": [("poly", [(-20, -30), (-4, -30), (-4, 14), (24, 14), (24, 30), (-20, 30)], FILL)],
    "steps": [("poly", [(-30, 30), (30, 30), (30, 10), (10, 10), (10, -10), (-10, -10), (-10, -30), (-30, -30)], GOLD)],
    "arrow": [("poly", [(0, -30), (20, -6), (7, -6), (7, 30), (-7, 30), (-7, -6), (-20, -6)], FILL)],
}


def turned(kind, q_cw, flip=False):
    """Primitives of a shape after q_cw quarter turns clockwise (flip = mirror image first)."""
    out = []
    for typ, pts, col in SHAPES[kind]:
        P = [((-x if flip else x), y) for x, y in pts]
        out.append((typ, [rot_pt(p, -90 * q_cw) for p in P], col))
    return out


def canon(prims):
    return tuple(sorted((t, tuple(sorted((round(p[0], 3) + 0.0, round(p[1], 3) + 0.0) for p in pts))) for t, pts, _ in prims))


def shape_fig(kind, q_cw=0, flip=False):
    F = Fig()
    for typ, pts, col in turned(kind, q_cw, flip):
        if typ == "line":
            F.line(pts[0], pts[1], w=4, col=col)
        else:
            F.poly(pts, fill=col, w=2.6, col=GREEN if col != RED else "#8c0b20")
    return F


def place(s, F, cx, cy):
    body, bb = F.render()
    s.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (cx - (bb[0] + bb[2]) / 2, cy - (bb[1] + bb[3]) / 2, body))
    return bb


def row_svg(start, figs, label):
    """Start shape, then pictures A-D in one row. Wide: printed large."""
    cw, top = 84, 76
    s = []
    for k, (F, cap) in enumerate([(start, "Start")] + [(f, "ABCD"[i]) for i, f in enumerate(figs)]):
        x = k * cw + (12 if k else 0)
        bb = place(s, F, x + cw / 2.0, top / 2.0 + 2)
        assert bb[2] - bb[0] <= cw - 8 and bb[3] - bb[1] <= top - 4
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + cw / 2.0, top + 20, INK, cap))
    s.append("<line x1='%d' y1='6' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (cw + 6, cw + 6, top + 22, GRAY))
    return svg_wrap(5 * cw + 12, top + 28, "".join(s), label)


def before_after_svg(a, b, label="shape before and after a turn"):
    cw, top = 110, 76
    s = []
    for k, (F, cap) in enumerate([(a, "before"), (b, "after")]):
        x = k * (cw + 40)
        bb = place(s, F, x + cw / 2.0, top / 2.0 + 2)
        assert bb[2] - bb[0] <= cw - 8 and bb[3] - bb[1] <= top - 4
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + cw / 2.0, top + 20, INK, cap))
    y = top / 2.0 + 2
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cw + 4, y, cw + 26, y, INK))
    s.append("<polygon points='%d,%.1f %d,%.1f %d,%.1f' fill='%s'/>" % (cw + 36, y, cw + 25, y - 7, cw + 25, y + 7, INK))
    return svg_wrap(2 * cw + 40, top + 28, "".join(s), label)


def strip_svg(items, cw=128, label="figures", fs=15):
    rend = [F.render() for F, _ in items]
    top = max(bb[3] - bb[1] for _, bb in rend) + 8
    s = []
    for k, ((body, bb), (_, cap)) in enumerate(zip(rend, items)):
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        assert bw <= cw - 6, (cap, bw)
        dx = k * cw + (cw - bw) / 2 - bb[0]
        dy = (top - bh) / 2 - bb[1]
        s.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body))
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (k * cw + cw / 2.0, top + 16, fs, INK, cap))
    return svg_wrap(cw * len(items), int(top + 24), "".join(s), label)


def arrows_row_svg():
    """Four arrows pointing up, right, down and left, labelled A-D."""
    return row4_svg([shape_fig("arrow", q) for q in range(4)], "four arrows labelled A to D")


def row4_svg(figs, label):
    cw, top = 84, 70
    s = []
    for k, F in enumerate(figs):
        place(s, F, k * cw + cw / 2.0, top / 2.0 + 2)
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (k * cw + cw / 2.0, top + 20, INK, "ABCD"[k]))
    return svg_wrap(4 * cw, top + 28, "".join(s), label)


SHAPE_NAME = {"flag": "flag", "L": "L shape", "steps": "steps shape", "arrow": "arrow"}


def pick_turned(kind, q_cw, p, why):
    """Start shape and four pictures; the right one (q_cw quarter turns clockwise) is at position p.
    Wrong pictures are real mistakes: the other way, the wrong amount, or a flip."""
    right = turned(kind, q_cw)
    qs = [(4 - q_cw) % 4, 2, 1, 3]
    cands = [(q, False) for q in qs if q % 4 != q_cw % 4][:2] + [(q_cw, True), (0, True), (0, False)]
    seen = {canon(right)}
    wrong = []
    for q, fl in cands:
        k = canon(turned(kind, q, fl))
        if k in seen:
            continue
        seen.add(k)
        wrong.append(shape_fig(kind, q, fl))
        if len(wrong) == 3:
            break
    assert len(wrong) == 3
    figs = wrong[:]
    figs.insert(p, shape_fig(kind, q_cw))
    return figs


# ------------------------------------------------------------ set 1: quarter, half, three-quarter and full turns
def set_turns(rnd, P):
    its = []
    q = "What turn does the arrow show? It starts at the dashed line."
    E = {1: "The arrow goes a quarter of the way round. That is a quarter turn.",
         2: "The arrow goes halfway round. The end line points the opposite way. That is a half turn.",
         3: "The arrow goes three quarters of the way round. That is a three-quarter turn.",
         4: "The arrow goes all the way round, back to the dashed line. That is a full turn."}
    for k, cw, st in [(1, True, 90), (2, False, 0), (3, True, 180), (4, True, 90),
                      (1, False, 0), (2, True, 90), (3, False, 270), (4, False, 180)]:
        its.append(mcq_fixed(fig(turn_svg(k, cw, st)) + q, TURNS, FRAC[k], E[k]))
    for n, t, e in [(2, "a half turn", "A quarter and another quarter make a half. So 2 quarter turns make a half turn."),
                    (3, "a three-quarter turn", "Three quarters means 3 quarter turns."),
                    (4, "a full turn", "4 quarters make a whole. So 4 quarter turns make a full turn.")]:
        its.append(mcq_num("How many quarter turns make %s?" % t, n, [1, 2, 3, 4], e))
    its.append(mcq_num("How many half turns make a full turn?", 2, [1, 3, 4],
                       "A half and another half make a whole. So 2 half turns make a full turn."))
    its.append(mcq("Which turn takes you back to the start?", "a full turn",
                   ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "A full turn goes all the way round. You face the same way again.", rnd))
    its.append(mcq("Which turn makes you face the opposite way?", "a half turn",
                   ["a quarter turn", "a full turn", "a three-quarter turn"],
                   "A half turn goes halfway round. You face the opposite way.", rnd))
    its.append(mcq("Which is the smallest turn?", "a quarter turn",
                   ["a half turn", "a three-quarter turn", "a full turn"],
                   "A quarter turn is only 1 quarter of the way round. It is the smallest.", rnd))
    n, he, his = P.next()
    its.append(mcq_fixed("%s makes a quarter turn. Then %s makes another quarter turn the same way. What turn is that altogether?" % (n, he),
                         TURNS, "half turn", "1 quarter + 1 quarter = 2 quarters. That is a half turn."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s makes a half turn. Then %s makes another half turn the same way. What turn is that altogether?" % (n, he),
                         TURNS, "full turn", "A half + a half = a whole. That is a full turn."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s makes a half turn. Then %s makes a quarter turn the same way. What turn is that altogether?" % (n, he),
                         TURNS, "three-quarter turn", "2 quarters + 1 quarter = 3 quarters. That is a three-quarter turn."))
    n, he, his = P.next()
    its.append(mcq(fig(turn_svg(2, True, 90)) + "%s says this arrow shows a quarter turn. Is %s right?" % (n, he),
                   "No, it is a half turn", ["Yes, it is a quarter turn", "No, it is a full turn", "No, it is a three-quarter turn"],
                   "The end line points the opposite way to the dashed line. The arrow goes halfway round: a half turn.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(turn_svg(3, True, 0)) + "%s says this arrow shows a quarter turn. Is %s right?" % (n, he),
                   "No, it is a three-quarter turn", ["Yes, it is a quarter turn", "No, it is a half turn", "No, it is a full turn"],
                   "Follow the arrow, not just the end line. It goes 3 quarters of the way round: a three-quarter turn.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Quarter, half, three-quarter and full turns", "items": its}


# ------------------------------------------------------------ set 2: clockwise and anticlockwise
DIRS_H = ["quarter turn clockwise", "quarter turn anticlockwise", "half turn clockwise", "half turn anticlockwise"]
DIRS_T = ["quarter turn clockwise", "quarter turn anticlockwise", "three-quarter turn clockwise", "three-quarter turn anticlockwise"]


def dir_name(k, cw):
    return FRAC[k] + (" clockwise" if cw else " anticlockwise")


def set_clockwise(rnd, P):
    its = []
    q = "Which turn does the arrow show? It starts at the dashed line."
    CWE = "It goes the same way as clock hands: clockwise."
    ACE = "It goes the opposite way to clock hands: anticlockwise."
    for k, cw, st, opts in [(1, True, 180, DIRS_T), (1, False, 90, DIRS_T), (3, True, 90, DIRS_T), (3, False, 0, DIRS_T),
                            (1, True, 0, DIRS_H), (1, False, 270, DIRS_H), (2, True, 0, DIRS_H), (2, False, 90, DIRS_H)]:
        e = "The arrow goes %s round. %s" % ({1: "a quarter of the way", 2: "halfway", 3: "three quarters of the way"}[k], CWE if cw else ACE)
        its.append(mcq_fixed(fig(turn_svg(k, cw, st)) + q, opts, dir_name(k, cw), e))
    qc = "The minute hand turns from the dashed line to where it is now. Which turn does it make?"
    for st, k, cw, opts, e in [
            (12, 1, True, DIRS_H, "From 12 to 3 is a quarter of the way round, the same way clocks go: clockwise."),
            (12, 2, True, DIRS_H, "From 12 to 6 is halfway round, the same way clocks go: clockwise."),
            (12, 1, False, DIRS_H, "From 12 back to 9 is a quarter of the way round, the opposite way to clocks: anticlockwise."),
            (3, 2, False, DIRS_H, "From 3 back to 9 is halfway round, the opposite way to clocks: anticlockwise.")]:
        its.append(mcq_fixed(fig(clock_turn_svg(st % 12, k, cw)) + qc, opts, dir_name(k, cw), e))
    its.append(mcq("Which way do the hands on a clock turn?", "clockwise",
                   ["anticlockwise", "both ways", "up and down"],
                   "Clock hands always turn the same way. That way is called clockwise.", rnd))
    its.append(mcq("What does anticlockwise mean?", "the opposite way to clock hands",
                   ["the same way as clock hands", "a half turn", "a full turn"],
                   "Anticlockwise is the opposite way to the way clock hands go.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(turn_svg(1, False, 90)) + "%s says this arrow turns clockwise. Is %s right?" % (n, he),
                   "No, it turns anticlockwise", ["Yes, it turns clockwise", "No, it is a half turn", "Yes, all turns are clockwise"],
                   "Clock hands go from 12 to 3: to the right at the top. This arrow goes to the left at the top. It is anticlockwise.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(turn_svg(3, True, 90)) + "%s says this is a quarter turn anticlockwise. Is %s right?" % (n, he),
                   "No, it is a three-quarter turn clockwise",
                   ["Yes, it is a quarter turn anticlockwise", "No, it is a quarter turn clockwise", "No, it is a half turn clockwise"],
                   "Follow the arrow all the way. It goes 3 quarters of the way round, the same way as clock hands.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s makes a quarter turn clockwise. Then %s makes a quarter turn anticlockwise. Which way does %s face now?" % (n, he, he),
                   "the same way as at the start", ["the opposite way", "a quarter turn clockwise from the start", "a quarter turn anticlockwise from the start"],
                   "The second turn goes back the other way by the same amount. So %s faces the same way as at the start." % he, rnd))
    n, he, his = P.next()
    its.append(mcq("%s makes a half turn clockwise. %s friend makes a half turn anticlockwise. They both started facing the board. What is true now?"
                   % (n, his.capitalize()),
                   "They both face away from the board", ["They both face the board", "Only %s faces the board" % n, "They face opposite ways"],
                   "A half turn either way makes you face the opposite way. So they both face away from the board.", rnd))
    its.append(mcq("Which turn ends in the same place as a quarter turn clockwise?", "a three-quarter turn anticlockwise",
                   ["a quarter turn anticlockwise", "a half turn clockwise", "a three-quarter turn clockwise"],
                   "1 quarter one way ends where 3 quarters the other way ends. 1 + 3 = 4 quarters: a full turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s makes a quarter turn clockwise. Then %s makes another quarter turn clockwise. How far has %s turned?" % (n, he, he),
                   "a half turn clockwise", ["a quarter turn clockwise", "a half turn anticlockwise", "a full turn clockwise"],
                   "1 quarter + 1 quarter = a half. Both turns were clockwise, so it is a half turn clockwise.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Clockwise and anticlockwise", "items": its}


# ------------------------------------------------------------ set 3: what does it face after a turn?
def set_facing(rnd, P):
    its = []
    sc = [(CLASSROOM, 0, 1, True), (PLAYGROUND, 1, 1, True), (BACKYARD, 0, 2, True), (CLASSROOM, 2, 1, False),
          (PLAYGROUND, 3, 1, True), (BACKYARD, 1, 3, True), (CLASSROOM, 1, 1, False), (PLAYGROUND, 0, 3, False),
          (BACKYARD, 1, 2, True), (CLASSROOM, 3, 4, True)]
    for names, st, k, cw in sc:
        n, he, his = P.next()
        end = end_side(st, k, cw)
        turn = FRAC[k] if k in (2, 4) else dir_name(k, cw)
        if k == 4:
            e = "A full turn goes all the way round. %s faces the %s again." % (he.capitalize(), names[end])
        elif k == 2:
            e = "A half turn makes you face the opposite way. The %s is opposite the %s." % (names[end], names[st])
        else:
            path = [names[(st + (i if cw else -i)) % 4] for i in range(k + 1)]
            e = "Go %s, one quarter at a time: %s." % ("the way clock hands go" if cw else "the opposite way to clock hands",
                                                        ", then ".join(path))
        its.append(mcq_fixed(fig(facing_fig(names, st).svg("child facing the %s" % names[st])) +
                             "%s faces the %s. %s makes a %s. What does %s face now?" % (n, names[st], he.capitalize(), turn, he),
                             ["the " + t for t in names], "the " + names[end], e))
    CL = ["12", "3", "6", "9"]
    for st, k in [(12, 1), (3, 1), (12, 3), (6, 2)]:
        end = CL[(CL.index(str(st)) + k) % 4]
        e = "Go clockwise, a quarter at a time: %s." % ", then ".join(CL[(CL.index(str(st)) + i) % 4] for i in range(k + 1))
        its.append(mcq_fixed(fig(hand_svg(st)) + "The hand points to %d. It makes a %s clockwise. Where does it point now?" % (st, FRAC[k]),
                             CL, end, e))
    for k, cw, e in [(1, True, "A quarter turn clockwise turns the arrow from up to the right."),
                     (2, True, "A half turn makes the arrow point the opposite way: down."),
                     (1, False, "A quarter turn anticlockwise turns the arrow from up to the left.")]:
        q_cw = k if cw else 4 - k
        p = q_cw % 4
        its.append(mcq_fixed(fig(arrows_row_svg()) + "An arrow points up. It makes a %s. Which picture shows it now?" % dir_name(k, cw) if k != 2 else
                             fig(arrows_row_svg()) + "An arrow points up. It makes a half turn. Which picture shows it now?",
                             ["A", "B", "C", "D"], "ABCD"[p], "Picture %s. %s" % ("ABCD"[p], e)))
    n, he, his = P.next()
    its.append(mcq(fig(facing_fig(CLASSROOM, 2).svg("child facing the door")) +
                   "%s faces the door. %s makes a half turn. %s says %s faces the window. Is %s right?" % (n, he.capitalize(), he.capitalize(), he, he),
                   "No, %s faces the board" % he, ["Yes, %s faces the window" % he, "No, %s faces the desk" % he, "No, %s faces the door" % he],
                   "The window is only a quarter turn away. A half turn makes you face the opposite way. The board is opposite the door.", rnd))
    its.append(mcq("You make a full turn. What do you face now?", "the same thing as at the start",
                   ["the thing behind you", "the thing on your left", "the thing on your right"],
                   "A full turn goes all the way round. You end up facing the same way as at the start.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces the gate. %s makes a three-quarter turn clockwise. %s friend makes a quarter turn anticlockwise. What is true now?"
                   % (n, he.capitalize(), his.capitalize()),
                   "They face the same way", ["They face opposite ways", "Only %s faces the gate" % n, "They both face the gate"],
                   "3 quarters clockwise ends in the same place as 1 quarter anticlockwise. So they face the same way.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "What do you face after a turn?", "items": its}


# ------------------------------------------------------------ set 4: turning shapes
DIRS_S = ["quarter turn clockwise", "quarter turn anticlockwise", "half turn", "full turn"]


def set_shapes(rnd, P):
    its = []
    for kind, k, cw, p in [("flag", 1, True, 0), ("L", 2, True, 1), ("steps", 1, False, 2),
                           ("flag", 2, True, 3), ("L", 1, True, 1), ("flag", 1, False, 2)]:
        q_cw = k if cw else 4 - k
        figs = pick_turned(kind, q_cw, p, "")
        t = "a half turn" if k == 2 else "a " + dir_name(k, cw)
        e = {(1, True): "The top of the shape turns to the right, the way clock hands go.",
             (1, False): "The top of the shape turns to the left, the opposite way to clock hands.",
             (2, True): "After a half turn the shape is upside down. The top is now at the bottom."}[(k, cw)]
        its.append(mcq_fixed(fig(row_svg(shape_fig(kind), figs, "start %s and four pictures labelled A to D" % SHAPE_NAME[kind])) +
                             "Turn the start shape %s. Which picture shows it?" % t,
                             ["A", "B", "C", "D"], "ABCD"[p], "Picture %s. %s A flipped shape is not a turn." % ("ABCD"[p], e)))
    q = "What turn moves the shape from before to after?"
    for kind, q_cw, ans, e in [
            ("flag", 1, "quarter turn clockwise", "The top of the flag pole turns to the right, the way clock hands go: a quarter turn clockwise."),
            ("L", 3, "quarter turn anticlockwise", "The top of the shape turns to the left, the opposite way to clock hands: a quarter turn anticlockwise."),
            ("steps", 2, "half turn", "The shape is upside down now. That is a half turn."),
            ("arrow", 1, "quarter turn clockwise", "The arrow pointed up. Now it points right. That is a quarter turn clockwise."),
            ("flag", 3, "quarter turn anticlockwise", "The flag pole pointed up. Now it points left. That is a quarter turn anticlockwise."),
            ("L", 4, "full turn", "The shape looks the same as before. It went all the way round: a full turn.")]:
        its.append(mcq_fixed(fig(before_after_svg(shape_fig(kind), shape_fig(kind, q_cw), "%s before and after a turn" % SHAPE_NAME[kind])) + q,
                             DIRS_S, ans, e))
    its.append(mcq("Which capital letter looks the same after a half turn?", "N", ["L", "F", "E"],
                   "Turn the page upside down. N still looks like N. L, F and E do not.", rnd))
    its.append(mcq("Which capital letter looks the same after a half turn?", "S", ["J", "P", "R"],
                   "Turn the page upside down. S still looks like S. J, P and R do not.", rnd))
    its.append(mcq("When you turn a shape, what changes?", "the way it faces",
                   ["its size", "how many sides it has", "how many corners it has"],
                   "Turning does not change the shape or its size. Only the way it faces changes.", rnd))
    its.append(mcq("A square makes a quarter turn. What does it look like now?", "the same square",
                   ["a bigger square", "a rectangle", "a triangle"],
                   "All the sides of a square are the same. After a quarter turn it looks just the same.", rnd))
    its.append(mcq("Which shape looks different after a quarter turn?", "a long rectangle",
                   ["a square", "a circle", "a plus sign"],
                   "A long rectangle that lies flat stands up tall after a quarter turn. The others look the same.", rnd))
    n, he, his = P.next()
    its.append(mcq("A flag pole points up. %s turns the flag a quarter turn clockwise. %s says the pole points left now. Is %s right?" % (n, he.capitalize(), he),
                   "No, it points right", ["Yes, it points left", "No, it points down", "No, it still points up"],
                   "Clockwise is the way clock hands go. From 12 they go to 3, on the right. So the pole points right.", rnd))
    its.append(mcq_num("A triangle has 3 corners. It makes a half turn. How many corners does it have now?", 3, [2, 4, 6],
                       "Turning a shape does not change it. It still has 3 corners."))
    n, he, his = P.next()
    its.append(mcq("%s turns a puzzle piece a half turn. Then %s turns it another half turn. What does it look like now?" % (n, he),
                   "the same as at the start", ["upside down", "on its side", "flipped over"],
                   "A half turn and another half turn make a full turn. The piece is back the way it started.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Turning shapes", "items": its}


# ------------------------------------------------------------ set 5: turns in everyday life
def set_life(rnd, P):
    its = []
    its.append(mcq(fig(clock_turn_svg(0, 1)) + "It was 4 o’clock. The minute hand made this turn. What time is it now?",
                   "quarter past 4", ["quarter to 4", "half past 4", "5 o’clock"],
                   "A quarter turn of the minute hand is 15 minutes. 15 minutes after 4 o’clock is quarter past 4.", rnd))
    its.append(mcq(fig(clock_turn_svg(0, 2)) + "It was 7 o’clock. The minute hand made this turn. What time is it now?",
                   "half past 7", ["quarter past 7", "quarter to 8", "8 o’clock"],
                   "A half turn of the minute hand is 30 minutes. 30 minutes after 7 o’clock is half past 7.", rnd))
    its.append(mcq("How long does the minute hand take to make a full turn?", "1 hour",
                   ["30 minutes", "15 minutes", "1 day"],
                   "The minute hand goes all the way round the clock in 60 minutes. That is 1 hour.", rnd))
    its.append(mcq_fixed("From 2 o’clock to half past 2, what turn does the minute hand make?", TURNS, "half turn",
                         "The minute hand goes from 12 to 6. That is halfway round: a half turn."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s turns the garden tap a quarter turn. Then %s turns it another quarter turn the same way. How far has the tap turned?" % (n, he),
                         TURNS, "half turn", "1 quarter + 1 quarter = 2 quarters. That is a half turn."))
    its.append(mcq("You turn a jar lid anticlockwise to open it. Which way do you turn it to close it?", "clockwise",
                   ["anticlockwise", "upside down", "a full turn anticlockwise"],
                   "Closing is the opposite of opening. The opposite of anticlockwise is clockwise.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts a key in the front door lock. %s turns it a half turn. How does the key look now?" % (n, he.capitalize()),
                   "upside down", ["on its side", "the same as before", "flipped over"],
                   "A half turn turns the key upside down. A quarter turn would leave it on its side.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s rides %s skateboard to the end of the path. %s does a half turn. Which way does %s go now?" % (n, his, he.capitalize(), he),
                   "back the way %s came" % he, ["the same way as before", "to the side", "round in a circle"],
                   "A half turn makes you face the opposite way. So %s rides back the way %s came." % (he, he), rnd))
    n, he, his = P.next()
    its.append(mcq("%s spins on %s skateboard and makes a full turn. Which way does %s face now?" % (n, his, he),
                   "the same way as before", ["the opposite way", "to the side", "upside down"],
                   "A full turn goes all the way round, so %s faces the same way as before." % he, rnd))
    n, he, his = P.next()
    its.append(mcq("%s rides the merry-go-round. It makes 1 full turn and stops. Where is %s now?" % (n, he),
                   "where %s started" % he, ["on the other side", "a quarter of the way round", "halfway round"],
                   "A full turn goes all the way round, back to the start.", rnd))
    n, he, his = P.next()
    its.append(mcq("In netball, %s catches the ball facing the goal. %s pivots a half turn. What does %s face now?" % (n, he.capitalize(), he),
                   "away from the goal", ["the goal", "the left sideline", "the right sideline"],
                   "A half turn makes you face the opposite way. So %s faces away from the goal." % he, rnd))
    n, he, his = P.next()
    its.append(mcq("%s gets on the Ferris wheel at the bottom. The wheel makes a half turn. Where is %s seat now?" % (n, his),
                   "at the top", ["at the bottom", "on the side", "back at the start"],
                   "A half turn goes halfway round the wheel. The bottom goes to the top.", rnd))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(facing_fig(PLAYGROUND, 2).svg("child facing the canteen")) +
                         "At lunch, %s faces the canteen. %s makes a quarter turn clockwise. What does %s face now?" % (n, he.capitalize(), he),
                         ["the " + t for t in PLAYGROUND], "the sandpit",
                         "Go the way clock hands go: canteen, then sandpit."))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(facing_fig(BEACH, 0).svg("child facing the sea")) +
                         "%s faces the sea. %s turns to face the car park behind %s. What turn is that?" % (n, he.capitalize(), "her" if he == "she" else "him"),
                         TURNS, "half turn", "The car park is opposite the sea. Turning to face the opposite way is a half turn."))
    n, he, his = P.next()
    its.append(mcq_fixed("At the school concert, %s does 4 quarter turns the same way. What turn is that altogether?" % n,
                         TURNS, "full turn", "4 quarters make a whole. That is a full turn."))
    n, he, his = P.next()
    its.append(mcq_num("%s turns the music up. The knob makes a three-quarter turn clockwise. How many quarter turns is that?" % n,
                       3, [1, 2, 4], "A three-quarter turn is 3 quarter turns."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s opens a jar. %s turns the lid a quarter turn. Then %s turns it 2 more quarter turns. What turn is that altogether?" % (n, he.capitalize(), he),
                         TURNS, "three-quarter turn", "1 quarter + 2 quarters = 3 quarters. That is a three-quarter turn."))
    n, he, his = P.next()
    sib = "brother"
    its.append(mcq("The biggest slice of pizza points at %s. %s turns the plate a half turn. Who does the slice point at now?" % (n, he.capitalize()),
                   "%s %s, across the table" % (his, sib), [n, "%s mum, next to %s" % (his, "her" if he == "she" else "him"),
                                                             "%s dad, next to %s" % (his, "her" if he == "she" else "him")],
                   "A half turn makes the slice point the opposite way: across the table.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s turns a round door knob a quarter turn clockwise. %s lets go and it turns back. How does it turn back?" % (n, he.capitalize()),
                   "a quarter turn anticlockwise", ["a quarter turn clockwise", "a half turn anticlockwise", "a full turn clockwise"],
                   "It goes back the same amount the other way. The other way to clockwise is anticlockwise.", rnd))
    its.append(mcq_num("A bike wheel makes a full turn and then a half turn. How many quarter turns is that?", 6, [4, 5, 3],
                       "A full turn is 4 quarter turns. A half turn is 2 more. 4 + 2 = 6."))
    assert len(its) == 20, len(its)
    return {"title": "Turns in everyday life", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    turns = strip_svg([(turn_fig(k), t) for t, k in (("quarter", 1), ("half", 2), ("three-quarter", 3), ("full", 4))],
                      cw=124, label="quarter, half, three-quarter and full turns clockwise")
    dirs = strip_svg([(turn_fig(1, True), "clockwise"), (turn_fig(1, False), "anticlockwise")], cw=130,
                     label="a quarter turn clockwise and a quarter turn anticlockwise")
    face = facing_fig(CLASSROOM, 0).svg("child facing the board, with the window, door and desk around")
    shp = strip_svg([(shape_fig("flag", 0), "start"), (shape_fig("flag", 1), "quarter clockwise"),
                     (shape_fig("flag", 2), "half turn"), (shape_fig("flag", 3), "quarter anticlockwise")],
                    cw=150, label="a flag turned a quarter turn clockwise, a half turn and a quarter turn anticlockwise", fs=14)
    return (
        "<h2>What is a turn?</h2>"
        "<p>When something <b>turns</b>, it goes round. We say how far it goes round.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>Each turn starts at the dashed line.</figcaption></figure>" +
        table(["Turn", "How far round", "Quarter turns"], [
            ["Quarter turn", "a quarter of the way", "1"], ["Half turn", "halfway (face the opposite way)", "2"],
            ["Three-quarter turn", "three quarters of the way", "3"], ["Full turn", "all the way (back to the start)", "4"],
        ]) +
        "<h2>Clockwise and anticlockwise</h2>"
        "<p><b>Clockwise</b> is the way clock hands go. <b>Anticlockwise</b> is the opposite way.</p>"
        "<figure class='sn-fig'>" + dirs +
        "<figcaption>At the top, clockwise goes to the right. Anticlockwise goes to the left.</figcaption></figure>"
        "<h2>What do you face after a turn?</h2>"
        "<figure class='sn-fig'>" + face +
        "<figcaption>The arrow shows the way the child faces.</figcaption></figure>" +
        ex("Example", "Mia faces the board. She makes a quarter turn clockwise. What does she face now?",
           "Go the way clock hands go, one quarter: board, then window.", "the window") +
        ex("Example", "Jack faces the board. He makes a half turn. What does he face now?",
           "A half turn makes you face the opposite way. The door is opposite the board.", "the door") +
        "<h2>Turning shapes</h2>"
        "<p>A turned shape is the same shape. Only the way it faces changes.</p>"
        "<figure class='sn-fig'>" + shp + "</figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up clockwise and anticlockwise", "Clockwise is the way clock hands go: from 12 to 3"],
            ["Calling a three-quarter turn a quarter turn", "Follow the arrow all the way, not just the end"],
            ["Calling a half turn a quarter turn", "After a half turn you face the opposite way"],
            ["Thinking a turned shape is a new shape", "Turning only changes the way a shape faces"],
        ])
    )


FAQ = [
    {"q": "What is AC9M2M05 in the Australian Curriculum?",
     "a": "It is the Year 2 maths content description “identify, describe and demonstrate quarter, half, three-quarter and full measures of turn in everyday situations”. Students turn their bodies, objects and shapes and describe the turn."},
    {"q": "How do you teach clockwise and anticlockwise to a Year 2 child?",
     "a": "Show an analog clock: clockwise is the way the hands go, from 12 to 3. Anticlockwise is the opposite way. Let your child turn their body both ways and say the turn out loud."},
    {"q": "Do Year 2 students learn right angles?",
     "a": "Not yet. In Year 2 students describe turns as quarter, half, three-quarter and full turns. In Year 3 they learn that a quarter turn makes a right angle."},
    {"q": "What are some everyday examples of turns for Year 2?",
     "a": "Clock hands, taps, jar lids, keys, door knobs, a merry-go-round and a skateboard all turn. A half turn on a skateboard sends you back the way you came, and a full turn of a merry-go-round brings you back to the start."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5. Fixed-order questions stay; the others fill the gaps."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [5 - c for c in cnt]
        assert min(need) >= 0 and sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen():
    rnd = random.Random(2813)
    P = People(rnd)
    sets = [set_turns(rnd, P), set_clockwise(rnd, P), set_facing(rnd, P), set_shapes(rnd, P), set_life(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "turns", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Turns: Quarter, Half, Three-Quarter and Full Turns, Clockwise and Anticlockwise",
        "seo_title": "Year 2 Turns Worksheets: Quarter, Half and Full Turns, Clockwise and Anticlockwise (Free, Australian Curriculum)",
        "short_title": "Turns",
        "domain": "Measurement",
        "standard_code": "AC9M2M05",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify, describe and demonstrate quarter, half, three-quarter and full measures of turn in everyday situations",
        "meta_desc": "Free Year 2 maths worksheets on turns: quarter, half, three-quarter and full turns, clockwise and anticlockwise, what you face after a turn, turning shapes and turns in everyday life. 100 questions with pictures and an answer key, following the Australian Curriculum (AC9M2M05).",
        "key_big": "A turn tells how far something goes round: a quarter, a half, three quarters or all the way.",
        "key_sub": "2 quarter turns make a half turn and 4 make a full turn. Clockwise is the way clock hands go; anticlockwise is the opposite way. A half turn makes you face the opposite way, and a full turn brings you back to the start.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures (rows of shapes) so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(start [A-Za-z ]+ and four pictures labelled A to D|four arrows labelled A to D|[A-Za-z ]+ before and after a turn)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
