# -*- coding: utf-8 -*-
"""
BC Grade 2 Math: Change in quantity (BC Mathematics Curriculum, Grade 2: Patterning)
  python3 tools/gen_cabc_math_g2_change.py
Join and separate stories with pictures, writing the number sentence with a box (28 + □ = 45),
finding the change, finding the start, and BC word problems to 100. Canadian English.
Every answer and every wrong answer is computed and checked in code.
Wrong answers come from real mistakes: using the wrong operation, answering with the start
(or end) amount, not regrouping, and being off by a ten.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_caon_math_g1_word_problems.py and gen_caon_math_g2_add_sub.py.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
BOX = "□"
MINUS = "−"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", gold="#e8b21c", brown="#9a6a3a", black="#2b2b2b")


# ------------------------------------------------------------ helpers
def lead(c):
    m = re.match(r"(\d+)", c)
    return int(m.group(1)) if m else None


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (whole numbers 1 to 198, all different values)."""
    correct = str(correct)
    seen = {correct}
    num = "=" not in correct and lead(correct) is not None
    vals = {lead(correct)} if num else set()
    pick = []
    for c in cands:
        c = str(c)
        v = lead(c)
        if c in seen or not c:
            continue
        if num and (v is None or v < 1 or v > 198 or v in vals):
            continue
        seen.add(c)
        if num:
            vals.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def cap(s):
    return s[0].upper() + s[1:]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def one(self):
        n, he, his, him = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his), him=him)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def fmt(n, u):
    return "%d %s" % (n, u[0] if n == 1 else u[1])


def say(t, p, **k):
    d = dict(p)
    d.update(k)
    return t.format(**d)


def solve_box(eq):
    """Whole-number value of □ that makes the equation true (None if there is none)."""
    for v in range(0, 201):
        l, r = eq.replace(MINUS, "-").replace(BOX, str(v)).split(" = ")
        if eval(l) == eval(r):
            return v
    return None


# ------------------------------------------------------------ typical mistakes
def small_from_big(a, b):
    """52 − 17 = 45: took the smaller ones digit from the larger one (no regrouping)."""
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    return (ta - tb) * 10 + abs(oa - ob)


def carry(a, b):
    return a % 10 + b % 10 >= 10


def borrow(a, b):
    return b % 10 > a % 10


# ------------------------------------------------------------ explanations (short, Grade 2 words)
def tens_word(k):
    return "1 ten" if k == 1 else "%d tens" % k


def count_list(a, t):
    return ", ".join(str(x) for x in range(a + 1, t + 1))


def e_add(a, b):
    """a + b, bigger number first. Ends with '= <b>s</b>.'"""
    if b > a:
        a, b = b, a
    s = a + b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if s <= 20:
        if b <= 4:
            return "Count on from %d: %s. %d + %d = <b>%d</b>." % (a, count_list(a, s), a, b, s)
        return "%d + %d = <b>%d</b>." % (a, b, s)
    if b < 10:
        if oa + b < 10:
            return "Add the ones: %d + %d = %d. The tens stay the same. %d + %d = <b>%d</b>." % (oa, b, oa + b, a, b, s)
        need = 10 - oa
        return ("Make the next ten: %d + %d = %d. Then add the rest: %d + %d = <b>%d</b>."
                % (a, need, a + need, a + need, b - need, s))
    if ob == 0:
        return ("%d is %s. Add the tens. The ones stay the same. %d + %d = <b>%d</b>."
                % (b, tens_word(tb), a, b, s))
    e = "Tens: %d + %d = %d. Ones: %d + %d = %d. " % (10 * ta, 10 * tb, 10 * (ta + tb), oa, ob, oa + ob)
    if oa + ob == 10:
        e += "10 ones is 1 ten. "
    elif oa + ob > 10:
        e += "%d ones is 1 ten and %s. " % (oa + ob, "1 one" if oa + ob == 11 else "%d ones" % (oa + ob - 10))
    return e + "%d + %d = <b>%d</b>." % (10 * (ta + tb), oa + ob, s)


def e_sub(a, b):
    r = a - b
    ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
    if a <= 20:
        return "%d − %d = <b>%d</b>." % (a, b, r)
    if b >= 10 and ob == 0:
        return ("%d is %s. Take away the tens. The ones stay the same. %d − %d = <b>%d</b>."
                % (b, tens_word(tb), a, b, r))
    if ob <= oa:
        if b < 10:
            return "Ones: %d − %d = %d. The tens stay the same. %d − %d = <b>%d</b>." % (oa, ob, oa - ob, a, b, r)
        return ("Tens: %d − %d = %d. Ones: %d − %d = %d. %d + %d = <b>%d</b>."
                % (10 * ta, 10 * tb, 10 * (ta - tb), oa, ob, oa - ob, 10 * (ta - tb), oa - ob, r))
    has = "0 ones" if oa == 0 else ("only 1 one" if oa == 1 else "only %d ones" % oa)
    e = ("%d has %s, so regroup 1 ten as 10 ones. Ones: %d − %d = %d. "
         % (a, has, oa + 10, ob, oa + 10 - ob))
    e += "Tens: %d − %d = %d. " % (ta - 1, tb, ta - 1 - tb)
    return e + "%d − %d = <b>%d</b>." % (a, b, r)


def count_up(a, c):
    """How far from a up to c, with jumps on a number line. Ends with the answer in bold."""
    d = c - a
    nxt = (a // 10 + 1) * 10
    if d <= 9 and (a <= 20 or c <= nxt):
        if d <= 6:
            return "Count up from %d to %d: %s. That is <b>%d</b>." % (a, c, count_list(a, c), d)
        return "Count up from %d to %d. That is <b>%d</b>." % (a, c, d)
    if c < nxt:
        return "Same tens, so look at the ones: %d − %d = <b>%d</b>." % (c % 10, a % 10, d)
    if a % 10 == 0:
        t = c // 10 * 10
        if t == c:
            return "Count up by tens from %d to %d: %s. That is %s = <b>%d</b>." % (
                a, c, ", ".join(str(x) for x in range(a + 10, c + 1, 10)), tens_word(d // 10), d)
        return ("Count up from %d: %d + %d = %d. %d + %d = %d. Add the jumps: %d + %d = <b>%d</b>."
                % (a, a, t - a, t, t, c - t, c, t - a, c - t, d))
    return ("Count up from %d: %d + %d = %d. %d + %d = %d. Add the jumps: %d + %d = <b>%d</b>."
            % (a, a, nxt - a, nxt, nxt, c - nxt, c, nxt - a, c - nxt, d))


# ------------------------------------------------------------ objects (each fits in a 28 x 28 cell)
PITCH = 28


def obj(kind, cx, cy):
    s = "<g data-o='1'>"
    if kind == "apple":
        s += ("<path d='M%.1f %.1f q1 -4 3 -5' fill='none' stroke='#7a4a1e' stroke-width='2'/>" % (cx, cy - 7)
              + "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
              % (cx + 5, cy - 10, C["green"], cx + 5, cy - 10)
              + "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 1, C["red"], INK))
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 11 if k % 2 == 0 else 4.6
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
        s += "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), C["gold"], INK)
    elif kind == "card":
        s += ("<rect x='%.1f' y='%.1f' width='17' height='23' rx='2' fill='#ffffff' stroke='%s' stroke-width='1.3'/>"
              % (cx - 8.5, cy - 11.5, INK)
              + "<rect x='%.1f' y='%.1f' width='13' height='12' fill='%s'/>" % (cx - 6.5, cy - 9.5, C["blue"])
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='#f3d2b5' stroke='%s' stroke-width='0.8'/>" % (cx, cy - 4.5, INK)
              + "<rect x='%.1f' y='%.1f' width='11' height='2.4' fill='%s'/>" % (cx - 5.5, cy + 5, C["red"]))
    elif kind == "puck":
        s += ("<rect x='%.1f' y='%.1f' width='20' height='7' fill='%s'/>" % (cx - 10, cy - 3, C["black"])
              + "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4' fill='%s'/>" % (cx, cy + 4, C["black"])
              + "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4' fill='#555555' stroke='%s' stroke-width='1'/>" % (cx, cy - 3, C["black"]))
    elif kind == "child":
        s += ("<path d='M%.1f %.1f q0 -8 7 -8 q7 0 7 8 z' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 7, cy + 12, C["blue"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='5' fill='#f3d2b5' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 5, INK))
    elif kind == "fish":
        s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#c95a44' stroke='%s' stroke-width='1.1' "
              "stroke-linejoin='round'/>" % (cx + 5, cy, cx + 12, cy - 6, cx + 12, cy + 6, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='9.5' ry='5.5' fill='#e0735a' stroke='%s' stroke-width='1.2'/>"
              % (cx - 2, cy, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx - 7, cy - 1.2, INK))
    elif kind == "shell":
        base = cy + 8
        s += ("<path d='M%.1f %.1f A 10 10 0 0 1 %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='#f4c7a1' stroke='%s' "
              "stroke-width='1.2' stroke-linejoin='round'/>"
              % (cx - 10, cy + 1, cx + 10, cy + 1, cx + 3, base, cx - 3, base, INK))
        for ang in (150, 120, 90, 60, 30):
            r = math.radians(ang)
            s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#b0703a' stroke-width='1'/>"
                  % (cx, base - 1, cx + 9 * math.cos(r), cy + 1 - 9 * math.sin(r)))
    elif kind == "cone":
        s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#5a3a1a' stroke-width='2'/>" % (cx, cy - 13, cx, cy - 9)
              + "<ellipse cx='%.1f' cy='%.1f' rx='7' ry='10.5' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx, cy + 1, C["brown"], INK))
        for dy in (-5, 0, 5):
            s += ("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='#5a3a1a' "
                  "stroke-width='1'/>" % (cx - 5.5, cy + dy, cx - 2.7, cy + dy + 3, cx, cy + dy,
                                          cx + 2.7, cy + dy + 3, cx + 5.5, cy + dy))
    else:
        raise ValueError(kind)
    return s + "</g>"


def cross(cx, cy, r=10):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - r, cy - r, cx + r, cy + r, RED, cx - r, cy + r, cx + r, cy - r, RED))


def group_body(x0, y0, n, kind, cols=5, gap5=0):
    """n objects in rows of `cols`; an extra gap after every 5 in a row (like a ten frame)."""
    s, centers = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * PITCH + PITCH / 2 + (gap5 if c >= 5 else 0)
        cy = y0 + r * PITCH + PITCH / 2
        centers.append((cx, cy))
        s.append(obj(kind, cx, cy))
    ncol = min(n, cols)
    w = ncol * PITCH + (gap5 if ncol > 5 else 0)
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centers


def join_svg(a, b, kind):
    """Join: a objects, then b more inside a dashed box."""
    o, gap = 6, 22
    b1, w1, h1, _ = group_body(o, o + 4, a, kind, cols=10, gap5=8)
    b2, w2, h2, _ = group_body(o + w1 + gap + 6, o + 4, b, kind)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 12, h2 + 8, GREEN))
    W, H = o + w1 + gap + w2 + 12 + o, o + max(h1 + 4, h2 + 8) + o
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + box + b2, "picture: %d and %d more" % (a, b))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def take_svg(a, b, kind):
    """Separate: a objects in rows of 10; the last b are crossed out."""
    o = 6
    cols = 10 if a > 10 else 5
    body, w, h, cen = group_body(o, o, a, kind, cols=cols, gap5=8)
    xs = "".join(cross(cx, cy) for cx, cy in cen[a - b:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs, "picture: %d, %d crossed out" % (a, b))
    assert svg.count("<g data-o='1'>") == a and svg.count("<g data-x='1'>") == b
    return svg


# ------------------------------------------------------------ tens and ones blocks
CU = 12          # one cube
RG = 6           # gap between rods


def blocks_body(x0, y0, n, h=10 * CU):
    """n as tens rods and ones cubes, all on the same bottom line. Returns body, width, rod and cube centres."""
    t, o = divmod(n, 10)
    s, rods, cubes = [], [], []
    x = x0
    for i in range(t):
        for k in range(10):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                     % (x, y0 + h - (k + 1) * CU, CU, CU, FILL, GREEN))
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.8'/>"
                 % (x, y0 + h - 10 * CU, CU, 10 * CU, GREEN))
        rods.append((x + CU / 2.0, y0 + h - 5 * CU))
        x += CU + RG
    if t and o:
        x += 6
    for i in range(o):
        c, r = divmod(i, 5)
        cx, cy = x + c * (CU + 4), y0 + h - (r + 1) * (CU + 2) + 2
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#fbe3a6' stroke='#a07a12' stroke-width='1.2'/>"
                 % (cx, cy, CU, CU))
        cubes.append((cx + CU / 2.0, cy + CU / 2.0))
    w = t * (CU + RG) - (RG if t and not o else 0) + (6 if t and o else 0) + (((o + 4) // 5) * (CU + 4) - 4 if o else 0)
    return "".join(s), w, rods, cubes


def join_blocks_svg(a, b):
    o, gap = 8, 16
    H = 10 * CU
    b1, w1, _, _ = blocks_body(o, o + 6, a)
    b2, w2, _, _ = blocks_body(o + w1 + gap + 8, o + 6, b)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 16, H + 12, GREEN))
    W, HH = o + w1 + gap + w2 + 16 + o, o + H + 12 + o
    return svg_wrap(int(W + 0.99), int(HH + 0.99), b1 + box + b2,
                    "tens and ones blocks: %d and %d more" % (a, b))


def take_blocks_svg(a, b):
    """a as tens and ones; the last tens of b rods and ones of b cubes are crossed out (no regrouping)."""
    assert b % 10 <= a % 10 and b // 10 <= a // 10
    o = 8
    body, w, rods, cubes = blocks_body(o, o, a)
    xs = []
    for cx, cy in rods[len(rods) - b // 10:] if b >= 10 else []:
        xs.append("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.8' "
                  "stroke-linecap='round'/><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.8' "
                  "stroke-linecap='round'/></g>" % (cx - 8, cy - 56, cx + 8, cy + 56, RED, cx + 8, cy - 56, cx - 8, cy + 56, RED))
    if b % 10:
        xs += [cross(cx, cy, 5.5) for cx, cy in cubes[len(cubes) - b % 10:]]
    svg = svg_wrap(int(w + 2 * o + 0.99), 10 * CU + 2 * o, body + "".join(xs),
                   "tens and ones blocks: %d, %d crossed out" % (a, b))
    assert svg.count("<g data-x='1'>") == b // 10 + b % 10
    return svg


# ------------------------------------------------------------ bar models
def bar_svg(p1, p2, unknown=None):
    """Part-part-whole bar model: whole on top, the two parts below, drawn to scale (with a minimum width)."""
    whole = p1 + p2
    m, BW, bh, gap, minw = 8, 300, 38, 10, 52
    w1 = int(round(BW * p1 / float(whole)))
    w1 = max(minw, min(BW - minw, w1))
    W, H = BW + 2 * m, 2 * m + 2 * bh + gap
    lab = {"whole": whole, "p1": p1, "p2": p2}
    if unknown:
        lab[unknown] = "?"
    y2 = m + bh + gap

    def box(x, y, w, k):
        unk = lab[k] == "?"
        return ("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'%s/>"
                % (x, y, w, bh, PINK if unk else (FILL if k == "whole" else "#ffffff"), RED if unk else GREEN,
                   " stroke-dasharray='5 3'" if unk else ""))
    s = [box(m, m, BW, "whole"), box(m, y2, w1, "p1"), box(m + w1, y2, BW - w1, "p2")]
    for cx, cy, k in [(m + BW / 2.0, m + 26, "whole"), (m + w1 / 2.0, y2 + 26, "p1"), (m + w1 + (BW - w1) / 2.0, y2 + 26, "p2")]:
        v = lab[k]
        s.append(text(cx, cy, str(v), 20, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "bar model: whole %s, parts %s and %s" % (lab["whole"], lab["p1"], lab["p2"]))


# ------------------------------------------------------------ open number line
def nline_svg(ticks, jumps, jlabels, label):
    """Open number line. jumps: signed sizes (only the sign and size class matter). ticks: one label per point."""
    def jw(j):
        if len(jumps) == 1:
            return 150
        return 100 if abs(j) >= 10 else 64
    m, ry, ly = 30, 24, 52
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (jw(j) if j > 0 else -jw(j)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, 1 if x2 > x1 else 0, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 8, jlabels[k], 16, col=RED if "?" in jlabels[k] else GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "open number line: " + label)


def nl_change(a, c):
    """a + □ = c (c > a) or a − □ = c (c < a): one jump marked ?."""
    return nline_svg([str(a), str(c)], [c - a], ["?"],
                     "from %d %s to %d, the jump is unknown" % (a, "up" if c > a else "back", c))


def nl_start(b, c, op):
    """□ + b = c or □ − b = c: the start is marked ?."""
    j = b if op == "+" else -b
    return nline_svg(["?", str(c)], [j], [("+%d" if op == "+" else "−%d") % b],
                     "an unknown start, a jump of %s%d, ending at %d" % ("plus " if op == "+" else "minus ", b, c))


# ------------------------------------------------------------ story contexts
# s start, ss some at the start, ad add, ads add some, tk take, tks take some, now, qn now?,
# qa added?, qt taken?, qs start?  u units, k picture kind (None: no object picture), top biggest realistic number
CTX = [
    dict(s="{N} had {a} hockey cards.", ss="{N} had some hockey cards.",
         ad="{He} got {b} more.", ads="{He} got some more.",
         tk="{He} gave {b} cards to {his} friend.", tks="{He} gave some cards to {his} friend.",
         now="Now {he} has {c} hockey cards.", qn="How many hockey cards does {N} have now?",
         qa="How many cards did {N} get?", qt="How many cards did {N} give away?",
         qs="How many hockey cards did {N} have at the start?", u=("hockey card", "hockey cards"), k="card", top=100),
    dict(s="There were {a} salmon in the creek.", ss="There were some salmon in the creek.",
         ad="Then {b} more salmon swam in.", ads="Then some more salmon swam in.",
         tk="Then {b} salmon swam on up the river.", tks="Then some salmon swam on up the river.",
         now="Now there are {c} salmon in the creek.", qn="How many salmon are in the creek now?",
         qa="How many salmon swam in?", qt="How many salmon swam on up the river?",
         qs="How many salmon were in the creek at the start?", u=("salmon", "salmon"), k="fish", top=100),
    dict(s="There were {a} people on the SkyTrain.", ss="There were some people on the SkyTrain.",
         ad="At the next station, {b} more people got on.", ads="At the next station, some more people got on.",
         tk="At the next station, {b} people got off.", tks="At the next station, some people got off.",
         now="Now there are {c} people on the SkyTrain.", qn="How many people are on the SkyTrain now?",
         qa="How many people got on?", qt="How many people got off?",
         qs="How many people were on the SkyTrain at the start?", u=("person", "people"), k="child", top=100),
    dict(s="{N} had {a} shells from the beach.", ss="{N} had some shells from the beach.",
         ad="{He} found {b} more on Vancouver Island.", ads="{He} found some more on Vancouver Island.",
         tk="{He} gave {b} shells to {his} cousin.", tks="{He} gave some shells to {his} cousin.",
         now="Now {he} has {c} shells.", qn="How many shells does {N} have now?",
         qa="How many shells did {N} find?", qt="How many shells did {N} give away?",
         qs="How many shells did {N} have at the start?", u=("shell", "shells"), k="shell", top=100),
    dict(s="{N} collected {a} pinecones in Stanley Park.", ss="{N} collected some pinecones in Stanley Park.",
         ad="Then {he} found {b} more.", ads="Then {he} found some more.",
         tk="{He} used {b} pinecones for a craft.", tks="{He} used some pinecones for a craft.",
         now="Now {he} has {c} pinecones.", qn="How many pinecones does {N} have now?",
         qa="How many more pinecones did {N} find?", qt="How many pinecones did {N} use?",
         qs="How many pinecones did {N} collect at the start?", u=("pinecone", "pinecones"), k="cone", top=100),
    dict(s="{N} picked {a} apples at an orchard in the Okanagan.",
         ss="{N} picked some apples at an orchard in the Okanagan.",
         ad="Then {he} picked {b} more.", ads="Then {he} picked some more.",
         tk="{He} gave {b} apples to {his} class.", tks="{He} gave some apples to {his} class.",
         now="Now {he} has {c} apples.", qn="How many apples does {N} have now?",
         qa="How many more apples did {N} pick?", qt="How many apples did {N} give away?",
         qs="How many apples did {N} pick at the start?", u=("apple", "apples"), k="apple", top=100),
    dict(s="There were {a} pucks in the bucket.", ss="There were some pucks in the bucket.",
         ad="The coach put in {b} more.", ads="The coach put in some more.",
         tk="The coach took out {b} pucks.", tks="The coach took out some pucks.",
         now="Now there are {c} pucks in the bucket.", qn="How many pucks are in the bucket now?",
         qa="How many pucks did the coach put in?", qt="How many pucks did the coach take out?",
         qs="How many pucks were in the bucket at the start?", u=("puck", "pucks"), k="puck", top=100),
    dict(s="{N} had {a} stickers.", ss="{N} had some stickers.",
         ad="{His} teacher gave {him} {b} more.", ads="{His} teacher gave {him} some more.",
         tk="{He} used {b} stickers on a card.", tks="{He} used some stickers on a card.",
         now="Now {he} has {c} stickers.", qn="How many stickers does {N} have now?",
         qa="How many stickers did the teacher give {N}?", qt="How many stickers did {N} use?",
         qs="How many stickers did {N} have at the start?", u=("sticker", "stickers"), k="star", top=100),
    dict(s="At recess, {a} children were on the playground.", ss="At recess, some children were on the playground.",
         ad="Then {b} more children came out.", ads="Then some more children came out.",
         tk="Then {b} children went inside.", tks="Then some children went inside.",
         now="Now there are {c} children on the playground.", qn="How many children are on the playground now?",
         qa="How many children came out?", qt="How many children went inside?",
         qs="How many children were on the playground at the start?", u=("child", "children"), k="child", top=100),
    dict(s="There were {a} Canada geese on the pond.", ss="There were some Canada geese on the pond.",
         ad="Then {b} more geese landed.", ads="Then some more geese landed.",
         tk="Then {b} geese flew away.", tks="Then some geese flew away.",
         now="Now there are {c} geese on the pond.", qn="How many geese are on the pond now?",
         qa="How many geese landed?", qt="How many geese flew away?",
         qs="How many geese were on the pond at the start?", u=("goose", "geese"), k=None, top=100),
    dict(s="The class library had {a} books.", ss="The class library had some books.",
         ad="The teacher added {b} more.", ads="The teacher added some more.",
         tk="Students took {b} books home.", tks="Students took some books home.",
         now="Now there are {c} books in the class library.", qn="How many books are in the class library now?",
         qa="How many books did the teacher add?", qt="How many books did students take home?",
         qs="How many books were in the class library at the start?", u=("book", "books"), k=None, top=100),
    dict(s="There were {a} cars on the ferry.", ss="There were some cars on the ferry.",
         ad="Then {b} more cars drove on.", ads="Then some more cars drove on.",
         tk="At the first stop, {b} cars drove off.", tks="At the first stop, some cars drove off.",
         now="Now there are {c} cars on the ferry.", qn="How many cars are on the ferry now?",
         qa="How many cars drove on?", qt="How many cars drove off?",
         qs="How many cars were on the ferry at the start?", u=("car", "cars"), k=None, top=100),
    dict(s="There were {a} bald eagles by the Fraser River.", ss="There were some bald eagles by the Fraser River.",
         ad="Then {b} more eagles flew in.", ads="Then some more eagles flew in.",
         tk="Then {b} eagles flew away.", tks="Then some eagles flew away.",
         now="Now there are {c} eagles by the river.", qn="How many eagles are by the river now?",
         qa="How many eagles flew in?", qt="How many eagles flew away?",
         qs="How many eagles were by the river at the start?", u=("eagle", "eagles"), k=None, top=60),
    dict(s="{N} read {a} pages of a book.", ss="{N} read some pages of a book.",
         ad="The next day, {he} read {b} more pages.", ads="The next day, {he} read some more pages.",
         tk=None, tks=None,
         now="Now {he} has read {c} pages.", qn="How many pages has {N} read now?",
         qa="How many pages did {N} read the next day?", qt=None,
         qs="How many pages did {N} read on the first day?", u=("page", "pages"), k=None, top=100),
]


class Ctx:
    """Cycles through the contexts in a shuffled order; can ask for one with a picture or with take-away words."""
    def __init__(self, rnd, lst):
        self.rnd, self.lst = rnd, lst
        self.order = []
        self.last = None

    def get(self, pic=False, need=0, take=False):
        for _ in range(3):
            if not self.order:
                self.order = list(self.lst)
                self.rnd.shuffle(self.order)
            for strict in (True, False):
                for i, c in enumerate(self.order):
                    if ((not pic or c.get("k")) and c["top"] >= need and (not take or c["tk"])
                            and (not strict or c is not self.last)):
                        self.last = self.order.pop(i)
                        return self.last
            self.order = []
        raise RuntimeError("no context")


# ------------------------------------------------------------ stories
# AR join, end unknown        TR separate, end unknown
# CA join, change unknown     CT separate, change unknown
# SA join, start unknown      ST separate, start unknown
TAKE = {"TR", "CT", "ST"}


def build(kind, c, p, x, y):
    """x, y: the two known numbers. AR/TR: start, change. CA/CT: start, end. SA/ST: change, end."""
    U = lambda v: fmt(v, c["u"])
    if kind == "AR":
        a, b = x, y
        ans, st, en, ch = a + b, a, a + b, b
        q = say(c["s"] + " " + c["ad"] + " " + c["qn"], p, a=a, b=b)
        e = "Some more came, so add. " + e_add(a, b)
        wrong = [abs(a - b), a + b - 10 if carry(a, b) else None, a, ans + 10, ans - 10, ans + 1, ans - 1]
        eq = "%d + %d = %s" % (a, b, BOX)
    elif kind == "TR":
        a, b = x, y
        ans, st, en, ch = a - b, a, a - b, b
        q = say(c["s"] + " " + c["tk"] + " " + c["qn"], p, a=a, b=b)
        e = "Some went away, so subtract. Do not add. " + e_sub(a, b)
        wrong = [a + b, small_from_big(a, b) if borrow(a, b) else None, a, ans + 10, ans - 10, ans + 1, ans - 1]
        eq = "%d − %d = %s" % (a, b, BOX)
    elif kind == "CA":
        a, t = x, y
        ans, st, en, ch = t - a, a, t, t - a
        q = say(c["s"], p, a=a) + " " + say(c["ads"] + " " + c["now"] + " " + c["qa"], p, c=t)
        e = "The change is missing: %d + %s = %d. " % (a, BOX, t) + count_up(a, t) + \
            " Check: %d + %d = %d." % (a, ans, t)
        wrong = [a + t, a, t, small_from_big(t, a) if borrow(t, a) else None, ans + 10, ans - 10, ans + 1, ans - 1]
        eq = "%d + %s = %d" % (a, BOX, t)
    elif kind == "CT":
        a, t = x, y
        ans, st, en, ch = a - t, a, t, a - t
        q = say(c["s"], p, a=a) + " " + say(c["tks"] + " " + c["now"] + " " + c["qt"], p, c=t)
        e = ("The change is missing: %d − %s = %d. Find how far it is from %d up to %d. " % (a, BOX, t, t, a)
             + count_up(t, a) + " Check: %d − %d = %d." % (a, ans, t))
        wrong = [a + t, a, t, small_from_big(a, t) if borrow(a, t) else None, ans + 10, ans - 10, ans + 1, ans - 1]
        eq = "%d − %s = %d" % (a, BOX, t)
    elif kind == "SA":
        b, t = x, y
        ans, st, en, ch = t - b, t - b, t, b
        q = say(c["ss"] + " " + c["ad"] + " " + c["now"] + " " + c["qs"], p, b=b, c=t)
        e = ("The start is missing: %s + %d = %d. Work backward. Take away the %d that came. " % (BOX, b, t, b)
             + e_sub(t, b) + " Check: %d + %d = %d." % (ans, b, t))
        wrong = [t + b, t, b, small_from_big(t, b) if borrow(t, b) else None, ans + 10, ans - 10, ans + 1, ans - 1]
        eq = "%s + %d = %d" % (BOX, b, t)
    elif kind == "ST":
        b, t = x, y
        ans, st, en, ch = t + b, t + b, t, b
        q = say(c["ss"] + " " + c["tk"] + " " + c["now"] + " " + c["qs"], p, b=b, c=t)
        e = ("The start is missing: %s − %d = %d. Work backward. Put back the %d that went away. " % (BOX, b, t, b)
             + e_add(t, b) + " Check: %d − %d = %d." % (ans, b, t))
        wrong = [abs(t - b), t, b, ans - 10 if carry(t, b) else None, ans + 10, ans + 1, ans - 1]
        eq = "%s − %d = %d" % (BOX, b, t)
    else:
        raise ValueError(kind)
    wrong = [w for w in wrong if w is not None]
    if max(x, y, ans) <= 20:
        wrong = [w for w in wrong if w not in (ans + 10, ans - 10)] + [ans + 2, ans - 2]
    assert 2 <= ans <= 100 and solve_box(eq) == ans, (kind, eq, ans)
    assert max(x, y, ans) <= min(100, c["top"]) and ans not in (x, y), (kind, x, y, ans)
    assert st - (ch if kind in TAKE else -ch) == en
    assert "{" not in q, q
    return dict(q=q, ans=ans, wrong=wrong, e=e + " Answer: %s." % U(ans), eq=eq, U=U, nums=(x, y), kind=kind,
                st=st, ch=ch, en=en)


def item(b, rnd, pic=""):
    return mcq((fig(pic) if pic else "") + b["q"], b["U"](b["ans"]), [b["U"](v) for v in b["wrong"]], b["e"], rnd)


def bar_for(b):
    """The bar model for a story: the whole is the bigger amount (start for take-away, end for join)."""
    k, st, ch, en = b["kind"], b["st"], b["ch"], b["en"]
    if k == "AR":
        return bar_svg(st, ch, "whole")
    if k == "CA":
        return bar_svg(st, ch, "p2")
    if k == "SA":
        return bar_svg(st, ch, "p1")
    if k == "TR":
        return bar_svg(en, ch, "p1")
    if k == "CT":
        return bar_svg(en, ch, "p2")
    if k == "ST":
        return bar_svg(en, ch, "whole")
    raise ValueError(k)


# ------------------------------------------------------------ number pickers
def pick(rnd, used, gen, ok):
    for _ in range(50000):
        v = gen()
        if ok(*v) and v not in used:
            used.add(v)
            return v
    raise RuntimeError("no numbers")


def nums_for(kind, rnd, used, lo, hi, regroup=None):
    """Two known numbers for a story whose biggest amount is lo..hi. regroup: True/False/None (either)."""
    R = rnd.randint

    def big_small():
        big = R(lo, hi)
        return big, R(5, big - 5)

    def ok_rg(big, small):
        return regroup is None or borrow(big, small) == regroup

    def fine(big, small):
        d = big - small
        mn = 10 if lo >= 35 else 3
        return (d >= max(3, mn) and small >= mn and d != small and ok_rg(big, small)
                and not (big % 10 == 0 and small % 10 == 0 and big > 30))
    # big: the larger of start/end, small: the change or the smaller amount
    if kind == "AR":
        s, b = pick(rnd, used, big_small, fine)
        return (s - b, b)
    if kind == "TR":
        return pick(rnd, used, big_small, fine)
    if kind == "CA":
        t, a = pick(rnd, used, big_small, fine)
        return (a, t)
    if kind == "CT":
        a, t = pick(rnd, used, big_small, fine)
        return (a, t)
    if kind == "SA":
        t, b = pick(rnd, used, big_small, fine)
        return (b, t)
    if kind == "ST":
        w, b = pick(rnd, used, big_small, fine)
        return (b, w - b)
    raise ValueError(kind)


# ============================================================ set 1: join and separate stories with pictures
def set_pictures(rnd, P, X, used):
    its = []
    R = rnd.randint
    for i in range(8):
        if i % 2 == 0:
            a, b = pick(rnd, used, lambda: (R(5, 13), R(2, 5)), lambda a, b: 8 <= a + b <= 18 and a != b)
            c = X.get(pic=True)
            bb = build("AR", c, P.one(), a, b)
            its.append(item(bb, rnd, join_svg(a, b, c["k"])))
        else:
            a, b = pick(rnd, used, lambda: (R(9, 20), R(2, 7)), lambda a, b: a - b >= 3 and a - b != b)
            c = X.get(pic=True, take=True)
            bb = build("TR", c, P.one(), a, b)
            its.append(item(bb, rnd, take_svg(a, b, c["k"])))
    # which number sentence matches the picture?
    assert 9 + 4 == 13 and 15 - 6 == 9
    its.append(mcq(fig(join_svg(9, 4, "apple")) + "Which number sentence matches the picture?", "9 + 4 = 13",
                   ["9 − 4 = 5", "9 + 4 = 12", "9 + 5 = 14"],
                   "There are 9 apples. 4 more come. They are in the box. Some more come, so add: <b>9 + 4 = 13</b>. "
                   "9 − 4 = 5 uses the wrong sign.", rnd))
    its.append(mcq(fig(take_svg(15, 6, "shell")) + "Which number sentence matches the picture?", "15 − 6 = 9",
                   ["15 + 6 = 21", "15 − 6 = 8", "15 − 5 = 10"],
                   "There are 15 shells. 6 are crossed out, so they go away. Subtract: <b>15 − 6 = 9</b>. "
                   "15 + 6 = 21 uses the wrong sign.", rnd))
    # bigger numbers with tens and ones blocks
    plans = [("AR", 20, 0), ("TR", 0, 10), ("AR", 0, 0), ("TR", 0, 1), ("AR", 1, 0),
             ("TR", 0, 0), ("AR", 1, 0), ("TR", 0, 0), ("AR", 1, 0), ("TR", 0, 0)]
    for kind, rg, tens in plans:
        if kind == "AR":
            if rg == 20:
                a, b = pick(rnd, used, lambda: (R(21, 59), 10 * R(2, 3)), lambda a, b: a % 10 != 0)
            else:
                a, b = pick(rnd, used, lambda: (R(14, 58), R(12, 38)),
                            lambda a, b: a + b <= 95 and carry(a, b) == bool(rg) and a % 10 and b % 10 and a != b)
            c = X.get(need=a + b)
            bb = build("AR", c, P.one(), a, b)
            its.append(item(bb, rnd, join_blocks_svg(a, b)))
        else:
            if tens == 10:
                a, b = pick(rnd, used, lambda: (R(42, 89), 10 * R(2, 3)), lambda a, b: a % 10 != 0)
            elif tens == 1:
                a, b = pick(rnd, used, lambda: (R(26, 79), R(2, 6)), lambda a, b: b <= a % 10)
            else:
                a, b = pick(rnd, used, lambda: (R(35, 89), R(12, 34)),
                            lambda a, b: not borrow(a, b) and b % 10 and a - b >= 11 and a - b != b)
            c = X.get(need=a, take=True)
            bb = build("TR", c, P.one(), a, b)
            its.append(item(bb, rnd, take_blocks_svg(a, b)))
    assert len(its) == 20
    return {"title": "Join and separate stories with pictures", "items": its}


# ============================================================ set 2: write the number sentence
FORMS = ["{p} + {q} = □", "{p} − {q} = □", "{p} + □ = {q}", "{p} − □ = {q}",
         "□ + {p} = {q}", "□ − {p} = {q}", "□ − {q} = {p}", "{q} − □ = {p}"]
WHY = dict(AR="Some more came and the end is missing",
           TR="Some went away and the end is missing",
           CA="Some more came and the change is missing, so the □ goes in the middle",
           CT="Some went away and the change is missing, so the □ goes in the middle",
           SA="The start is missing and some more came, so the □ goes first",
           ST="The start is missing and some went away, so the □ goes first")


def trap_for(b):
    """The wrong-operation sentence a student often writes."""
    x, y = b["nums"]
    k = b["kind"]
    if k == "AR":
        return "%d − %d = □" % (max(x, y), min(x, y))
    if k == "TR":
        return "%d + %d = □" % (x, y)
    if k in ("CA", "CT"):
        return "%d + %d = □" % (x, y)
    if k == "SA":
        return "%d + %d = □" % (y, x)
    return "%d − %d = □" % (max(x, y), min(x, y))      # ST


def canon(x):
    m = re.match(r"^(\d+) \+ (\d+) = □$", x)
    return ("+",) + tuple(sorted(int(v) for v in m.groups())) if m else x


def eq_item(b, rnd, pic):
    p, q = b["nums"]
    ans = b["ans"]
    trap = trap_for(b)
    assert solve_box(trap) not in (None, ans)
    bad = []
    pool = [f.format(p=p, q=q) for f in FORMS] + [f.format(p=q, q=p) for f in FORMS]
    for x in [trap] + rnd.sample(pool, len(pool)):
        v = solve_box(x)
        if x == b["eq"] or v is None or v == ans or v < 1 or canon(x) in {canon(y) for y in bad + [b["eq"]]}:
            continue
        bad.append(x)
    assert bad[0] == trap and len(bad) >= 3, (b["kind"], trap, bad)
    qq = (fig(pic) if pic else "") + b["q"].rsplit(" How", 1)[0] + " Which number sentence matches the story?"
    why = "uses the wrong sign" if b["kind"] in ("AR", "TR", "ST") else "just adds the two numbers in the story"
    e = "%s: <b>%s</b>. The □ is %d. (%s %s.)" % (WHY[b["kind"]], b["eq"], ans, trap, why)
    return mcq(qq, b["eq"], bad[:3], e, rnd)


def set_sentence(rnd, P, X, used):
    kinds = []
    for _ in range(2):
        h = ["AR", "TR", "CA", "CT", "SA", "ST", "CA", "CT", "SA", "ST"]
        rnd.shuffle(h)
        kinds += h
    its = []
    for i, k in enumerate(kinds):
        lo, hi = (12, 40) if i < 10 else (35, 95)
        x, y = nums_for(k, rnd, used, lo, hi)
        c = X.get(need=hi, take=k in TAKE)
        bb = build(k, c, P.one(), x, y)
        pic = bar_for(bb) if i < 12 else ""
        its.append(eq_item(bb, rnd, pic))
    return {"title": "Write the number sentence with a box", "items": its}


# ============================================================ set 3: find the change
def bare_change(a, c, rnd):
    if c > a:
        eq = "%d + %s = %d" % (a, BOX, c)
        ans = c - a
        wrong = [a + c, a, c, small_from_big(c, a) if borrow(c, a) else None, ans + 10, ans - 10, ans + 1, ans - 1]
        e = "Start at %d and end at %d. " % (a, c) + count_up(a, c) + " Check: %d + %d = %d." % (a, ans, c)
    else:
        eq = "%d − %s = %d" % (a, BOX, c)
        ans = a - c
        wrong = [a + c, a, c, small_from_big(a, c) if borrow(a, c) else None, ans + 10, ans - 10, ans + 1, ans - 1]
        e = ("Jump back from %d to %d. The jump is how far apart they are. " % (a, c) + count_up(c, a)
             + " Check: %d − %d = %d." % (a, ans, c))
    assert solve_box(eq) == ans
    q = fig(nl_change(a, c)) + "What number goes in the box? %s" % eq
    return mcq(q, ans, [w for w in wrong if w is not None], e, rnd)


def set_change(rnd, P, X, used):
    its = []
    for a, c in [(30, 50), (24, 54), (36, 40), (28, 45), (60, 40), (52, 30)]:
        used.add((a, c))
        its.append(bare_change(a, c, rnd))
    assert 26 + 15 == 41 and 26 + 41 == 67
    its.append(mcq("Mei had 26 stickers. She got some more. Now she has 41. Ryan says she got 67. "
                   "What did Ryan do?", "He added 26 and 41",
                   ["He gave the start amount", "He gave the end amount", "He forgot to regroup"],
                   "26 + 41 = 67. But 67 is more than she has now. The change is the jump from 26 to 41: "
                   "26 + 4 = 30, 30 + 11 = 41, so she got 15. Ryan <b>added 26 and 41</b>.", rnd))
    kinds = ["CA", "CT", "CA", "CT", "CA", "CA", "CT"]
    for i, k in enumerate(kinds):
        x, y = nums_for(k, rnd, used, 20, 60)
        c = X.get(need=60, take=k in TAKE)
        bb = build(k, c, P.one(), x, y)
        pic = nl_change(x, y) if i % 2 == 0 else bar_for(bb)
        its.append(item(bb, rnd, pic))
    kinds = ["CA", "CT", "CA", "CT", "CA", "CT"]
    for k in kinds:
        x, y = nums_for(k, rnd, used, 45, 98, regroup=True)
        c = X.get(need=98, take=k in TAKE)
        its.append(item(build(k, c, P.one(), x, y), rnd))
    assert len(its) == 20
    return {"title": "Find the change: how many came or went?", "items": its}


# ============================================================ set 4: find the start
def bare_start(b, c, op, rnd):
    if op == "+":
        eq = "%s + %d = %d" % (BOX, b, c)
        ans = c - b
        wrong = [c + b, c, b, small_from_big(c, b) if borrow(c, b) else None, ans + 10, ans - 10, ans + 1, ans - 1]
        e = ("Work backward from %d. %d came, so take them away. " % (c, b) + e_sub(c, b)
             + " Check: %d + %d = %d." % (ans, b, c))
    else:
        eq = "%s − %d = %d" % (BOX, b, c)
        ans = c + b
        wrong = [abs(c - b), c, b, ans - 10 if carry(c, b) else None, ans + 10, ans + 1, ans - 1]
        e = ("Work backward from %d. %d went away, so put them back. " % (c, b) + e_add(c, b)
             + " Check: %d − %d = %d." % (ans, b, c))
    assert solve_box(eq) == ans
    q = fig(nl_start(b, c, op)) + "What number goes in the box? %s" % eq
    return mcq(q, ans, [w for w in wrong if w is not None], e, rnd)


def set_start(rnd, P, X, used):
    its = []
    for b, c, op in [(20, 50, "+"), (6, 39, "+"), (10, 25, "−"), (17, 45, "+"), (12, 30, "−"), (18, 35, "−")]:
        used.add((b, c))
        its.append(bare_start(b, c, op, rnd))
    assert 42 - 18 == 24 and 42 + 18 == 60
    its.append(mcq("Hana had some shells. She found 18 more. Now she has 42. Owen says she had 42 at the start. "
                   "What did Owen do?", "He gave the end amount",
                   ["He added 42 and 18", "He gave the change", "He forgot to regroup"],
                   "42 is how many she has <b>now</b>, at the end. Owen <b>gave the end amount</b>. Work backward: "
                   "42 − 18 = 24. She had 24 shells at the start.", rnd))
    kinds = ["SA", "ST", "SA", "ST", "SA", "ST", "SA"]
    for k in kinds:
        x, y = nums_for(k, rnd, used, 20, 60)
        c = X.get(need=60, take=k in TAKE)
        bb = build(k, c, P.one(), x, y)
        its.append(item(bb, rnd, bar_for(bb)))
    kinds = ["ST", "SA", "ST", "SA", "ST", "SA"]
    for k in kinds:
        x, y = nums_for(k, rnd, used, 45, 99, regroup=True)
        c = X.get(need=99, take=k in TAKE)
        its.append(item(build(k, c, P.one(), x, y), rnd))
    assert len(its) == 20
    return {"title": "Find the start: work backward", "items": its}


# ============================================================ set 5: word problems to 100
def set_words(rnd, P, X, used):
    kinds = []
    for _ in range(2):
        h = ["AR", "TR", "CA", "CT", "SA", "ST", "CA", "CT", "SA", "ST"]
        rnd.shuffle(h)
        kinds += h
    its = []
    for i, k in enumerate(kinds):
        x, y = nums_for(k, rnd, used, 40, 100, regroup=(i % 3 != 2))
        c = X.get(need=100, take=k in TAKE)
        bb = build(k, c, P.one(), x, y)
        its.append(item(bb, rnd, bar_for(bb) if i < 6 else ""))
    return {"title": "Word problems to 100: salmon, SkyTrain and the ferry", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 8 + 5 == 13 and 12 - 4 == 8 and 28 + 17 == 45 and 45 - 17 == 28 and 52 - 22 == 30 and 30 + 12 == 42
    return (
        "<h2>The idea: start, change, end</h2>"
        "<p>A change story has three parts. There is a <b>start</b>. Then there is a <b>change</b>: "
        "some come, or some go away. Then there is the <b>end</b>. "
        "Two parts are known. Find the one you do not know. Use a box □ for it.</p>"
        + table(["What is missing?", "Some come", "Some go away"], [
            ["The end", "28 + 17 = □", "52 − 22 = □"],
            ["The change", "28 + □ = 45", "52 − □ = 30"],
            ["The start", "□ + 17 = 45", "□ − 12 = 30"],
        ]) +
        "<h2>Join: some more come</h2>"
        "<p>Draw the start. Draw the ones that come. Count them all.</p>"
        "<figure class='sn-fig'>" + join_svg(8, 5, "fish") +
        "<figcaption>There were 8 salmon in the creek. 5 more swam in. 8 + 5 = 13 salmon.</figcaption></figure>"
        "<h2>Separate: some go away</h2>"
        "<p>Draw the start. Cross out the ones that go away. Count the ones that are left.</p>"
        "<figure class='sn-fig'>" + take_svg(12, 4, "apple") +
        "<figcaption>Wei had 12 apples. He gave 4 to his class. 12 − 4 = 8 apples.</figcaption></figure>"
        "<h2>Find the change</h2>"
        "<p>The start and the end are known. Count up from the start to the end. "
        "Jump to the next ten first.</p>"
        "<figure class='sn-fig'>" + nline_svg(["28", "30", "45"], [2, 15], ["+2", "+15"],
                                             "from 28 jump plus 2 to 30, then plus 15 to 45") +
        "<figcaption>28 + □ = 45. Jump +2 to 30, then +15 to 45. 2 + 15 = 17, so □ = 17.</figcaption></figure>"
        + ex("Find the change", "There were 52 people on the SkyTrain. At the next station, some people got off. "
             "Now there are 30. How many got off?",
             "52 − □ = 30. Count up from 30 to 52: 30 + 20 = 50, 50 + 2 = 52. 20 + 2 = 22. Check: 52 − 22 = 30.",
             "22 people") +
        "<h2>Find the start: work backward</h2>"
        "<p>The start is missing. Go back from the end. If some came, take them away. "
        "If some went away, put them back.</p>"
        "<figure class='sn-fig'>" + bar_svg(28, 17, "p1") +
        "<figcaption>□ + 17 = 45. The whole is 45 and one part is 17. 45 − 17 = 28, so □ = 28.</figcaption></figure>"
        + ex("Find the start", "Liam had some hockey cards. He gave 12 to his friend. Now he has 30. "
             "How many did he have at the start?",
             "□ − 12 = 30. Put back the 12 he gave away: 30 + 12 = 42. Check: 42 − 12 = 30.", "42 hockey cards") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the wrong operation: 28 + □ = 45, so 28 + 45 = 73",
             "The end is 45, so the change is less than 45. Count up from 28 to 45: 17."],
            ["Answering with the start amount: “28”", "28 is the start. The question asks for the change."],
            ["Answering with the end amount: □ + 17 = 45, so “45”", "45 is the end. Work backward: 45 − 17 = 28."],
            ["Not regrouping: 52 − 17 = 45", "2 − 7 cannot be done. Regroup 1 ten: 12 − 7 = 5. Answer: 35."],
        ]) +
        "<p>Always check: put your answer in the box and read the story again.</p>"
    )


FAQ = [
    {"q": "What does “change in quantity” mean in the BC Grade 2 math curriculum?",
     "a": "It means an amount that goes up or down: some come or some go away. Grade 2 students show the change with "
          "pictures and with number sentences like 28 + □ = 45, using numbers to 100."},
    {"q": "How do you find the missing number in 28 + □ = 45?",
     "a": "Count up from 28 to 45: 2 to get to 30, then 15 more, so □ = 17. You can also subtract: 45 − 28 = 17."},
    {"q": "How do you solve a story when the start is missing?",
     "a": "Work backward from the end. If 17 came and now there are 45, take them away: 45 − 17 = 28. "
          "If 12 went away and 30 are left, put them back: 30 + 12 = 42."},
    {"q": "Why is change in quantity in the Patterning part of BC math?",
     "a": "In BC, Patterning includes early algebra: seeing how an amount changes and using a symbol like □ for "
          "the unknown number. It builds toward solving equations in later grades."},
]


# ============================================================ checks
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    """Check every answer again from the question text and the picture labels."""
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            right = it["c"][it["a"]]
            plain = re.sub(r"<[^>]+>", " ", it["q"]).strip()
            key = plain + " ".join(re.findall(r"aria-label='([^']*)'", it["q"]))
            assert key not in seen, key
            seen.add(key)
            if BOX in right:
                v = solve_box(right)
                assert v is not None and all(solve_box(c) not in (None, v) for c in it["c"] if c != right), it
            elif "=" not in right and lead(right) is not None:
                assert len({lead(c) for c in it["c"]}) == 4, it
            m = re.search(r"What number goes in the box\? (.+)$", plain)
            if m:
                assert solve_box(m.group(1)) == int(right), it["q"]
            m = re.search(r"aria-label='bar model: whole (\S+), parts (\S+) and (\S+)'", it["q"])
            if m and BOX not in right:
                vals = [m.group(1), m.group(2), m.group(3)]
                k = vals.index("?")
                nn = [int(x) for x in vals if x != "?"]
                want = nn[0] + nn[1] if k == 0 else nn[0] - nn[1]
                assert lead(right) == want, it["q"]
            m = re.search(r"aria-label='(?:picture|tens and ones blocks): (\d+) and (\d+) more'", it["q"])
            if m and "number sentence" not in plain:
                assert lead(right) == int(m.group(1)) + int(m.group(2)), it["q"]
            m = re.search(r"aria-label='(?:picture|tens and ones blocks): (\d+), (\d+) crossed out'", it["q"])
            if m and "number sentence" not in plain:
                assert lead(right) == int(m.group(1)) - int(m.group(2)), it["q"]
            for t in [plain, it["e"]] + it["c"]:
                assert "\\" not in t and ".." not in t and "{" not in t, t
                assert not re.search(r"\b1 (apples|stickers|hockey cards|cards|pucks|shells|pinecones|children|geese|"
                                     r"books|people|cars|eagles|pages)\b", t), t
                assert not re.search(r"\b([2-9]|\d\d) (apple|sticker|card|puck|shell|pinecone|child|goose|"
                                     r"book|person|car|eagle|page)\b(?!s)", t), t


def gen():
    rnd = random.Random(52805)
    P = People(rnd)
    X = Ctx(rnd, CTX)
    used = set()
    sets = [set_pictures(rnd, P, X, used), set_sentence(rnd, P, X, used), set_change(rnd, P, X, used),
            set_start(rnd, P, X, used), set_words(rnd, P, X, used)]
    balance(sets, rnd)
    verify(sets)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "change-in-quantity", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Change in Quantity: Find the Change and the Start",
        "seo_title": "Grade 2 Math: Change in Quantity Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "Change in quantity",
        "domain": "Patterning",
        "standard_code": "Grade 2: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Change in quantity, using pictorial and symbolic representation",
        "meta_desc": "Free Grade 2 math worksheets on change in quantity for the BC curriculum: join and separate "
                     "stories with pictures, writing number sentences like 28 + □ = 45, finding the change, finding "
                     "the start and word problems to 100. 100 questions with an answer key.",
        "key_big": "Start, change, end: find the part you do not know.",
        "key_sub": "Some come: add. Some go away: subtract. For 28 + □ = 45, count up from 28 to 45: 2 + 15 = 17. "
                   "If the start is missing, work backward from the end. The start or end number is not the change.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "picture|tens and ones blocks|bar model|open number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
