# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Place Value, Tens and Ones (1.NBT.B.2 a-c)
  python tools/gen_us_math_g1_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 1: numbers up to 120, no commas. Very short sentences for 6-7 year olds.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#c98a3d"
BAND = "#c0392b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, allow0=False):
    correct = str(correct)
    seen = {correct}
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        if x in seen or not x or x.startswith("-") or (x == "0" and not allow0):
            continue
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, cands, e, rnd, allow0=False):
    """Number choices. Wrong numbers below 0 (and 0 unless allow0) are dropped."""
    lo = 0 if allow0 else 1
    return mcq(q, correct, [v for v in cands if v is not None and v >= lo and v != correct], e, rnd, allow0)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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


def unit(k, one, many):
    return "%d %s" % (k, one if k == 1 else many)


def T(k):
    return unit(k, "ten", "tens")


def O(k):
    return unit(k, "one", "ones")


def TO(t, o):
    return "%s and %s" % (T(t), O(o))


def by_tens(t):
    return ", ".join(str(10 * i) for i in range(1, t + 1))


def by_ones(o):
    return ", ".join(str(i) for i in range(1, o + 1))


def joined(t, o):
    """The “407” mistake: writing the tens value and then the ones."""
    return int(str(10 * t) + str(o))


def rev(n):
    t, o = divmod(n, 10)
    return o * 10 + t if o else None


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


# ------------------------------------------------------------ figures
U = 8                      # one small cube = U x U, a rod = U x 10U
RG, CG, GG, M = 6, 4, 20, 6


def blocks_svg(t, o, labels=False):
    """Base-ten blocks: t ten rods, o ones cubes (columns of 5). Sizes are exact (1 : 10)."""
    F = 10 * U
    groups = []

    def rods(x, y):
        s = []
        for k in range(t):
            rx = x + k * (U + RG)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (rx, y, U, F, FILL, GREEN))
            for i in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (rx, y + i * U, rx + U, y + i * U, GREEN))
        return s

    ccols = (o + 4) // 5

    def cubes(x, y):
        s = []
        for k in range(o):
            cx = x + (k // 5) * (U + CG + 2)
            cy = y + (k % 5) * (U + CG + 4)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, U, U, CUBE, GREEN))
        return s

    if t:
        groups.append((t * U + (t - 1) * RG, F, rods, T(t)))
    if o:
        groups.append((ccols * U + (ccols - 1) * (CG + 2), 5 * U + 4 * (CG + 4), cubes, O(o)))
    lab_w = lambda s: int(len(s) * 8.6) + 4
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * M + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * M + body_h + (26 if labels else 0)
    s = []
    x = M
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, M)
        if labels:
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + w / 2, M + body_h + 20, INK, lab))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base-ten blocks")


C = 22                     # ten-frame cell


def tenframes_svg(n):
    """Ten-frames, one above the other. Dots fill each frame row by row, left to right."""
    frames = (n + 9) // 10
    gap = 10
    W = 2 * M + 5 * C
    Hh = 2 * M + frames * 2 * C + (frames - 1) * gap
    s = []
    for f in range(frames):
        y0 = M + f * (2 * C + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
                 % (M, y0, 5 * C, 2 * C, GREEN))
        for i in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (M + i * C, y0, M + i * C, y0 + 2 * C, GREEN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (M, y0 + C, M + 5 * C, y0 + C, GREEN))
        k = min(10, n - 10 * f)
        for d in range(k):
            cx = M + (d % 5) * C + C / 2
            cy = y0 + (d // 5) * C + C / 2
            s.append("<circle cx='%.1f' cy='%.1f' r='7.5' fill='%s'/>" % (cx, cy, RED))
    return svg_wrap(W, Hh, "".join(s), "ten-frames")


SW, SH = 4, 56             # stick spacing in a bundle, stick height


def sticks_svg(b, loose):
    """b bundles of 10 sticks (with a band) and some loose sticks."""
    bw = 9 * SW + 4
    LS = 9
    W = 2 * M + b * bw + (b - 1) * 12 + (GG + (loose - 1) * LS + 4 if loose else 0)
    Hh = 2 * M + SH
    s = []
    x = M
    for k in range(b):
        for i in range(10):
            sx = x + 2 + i * SW
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (sx, M + 2, sx, M + SH - 2, WOOD))
        s.append("<rect x='%d' y='%d' width='%d' height='7' rx='2' fill='%s'/>" % (x - 1, M + SH // 2 - 3, bw + 2, BAND))
        x += bw + 12
    if loose:
        x += GG - 12
        for i in range(loose):
            sx = x + 2 + i * LS
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (sx, M + 2, sx, M + SH - 2, WOOD))
    return svg_wrap(W, Hh, "".join(s), "bundles of sticks")


CW, HEAD, ROW = 80, 32, 48


def chart_svg(n, hi=None):
    """Tens / ones chart with n in it. hi = 1 (tens) or 0 (ones) to color red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 2 * CW, 2 * y0 + HEAD + ROW
    t, o = divmod(n, 10)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 2 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 2 * CW, HEAD, FILL)]
    for k, (lab, d, place) in enumerate([("Tens", t, 1), ("Ones", o, 0)]):
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx, y0 + 22, INK, lab))
        s.append("<text x='%.1f' y='%d' font-size='30' font-weight='800' fill='%s' text-anchor='middle'>%d</text>"
                 % (cx, y0 + HEAD + 35, RED if hi == place else INK, d))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 2 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "tens and ones chart")


def count_e(t, o):
    n = 10 * t + o
    s = "Count the rods by tens: %s. " % by_tens(t)
    if o:
        s += "Count the cubes: %s. " % by_ones(o)
    s += "%s is %d." % (cap(TO(t, o)), n)
    return s


# ============================================================ set 1: base-ten blocks
def two_digit(rnd, used, tlo=1, thi=9, olo=1, ohi=9, distinct=True):
    while True:
        t, o = rnd.randint(tlo, thi), rnd.randint(olo, ohi)
        n = 10 * t + o
        if distinct and t == o:
            continue
        if n not in used:
            used.add(n)
            return t, o


def set_blocks(rnd, used):
    its = []
    # blocks -> number (12), small tens first
    ranges = [(1, 3)] * 4 + [(2, 6)] * 4 + [(5, 9)] * 4
    for j, (lo, hi) in enumerate(ranges):
        t, o = two_digit(rnd, used, lo, hi, 1, 9)
        n = 10 * t + o
        miss = [n + 1, n - 1, n + 10, n - 10][j % 4]
        if j % 3 == 0:
            cands = [rev(n), t + o, joined(t, o), miss]
        elif j % 3 == 1:
            cands = [rev(n), joined(t, o), miss, t + o]
        else:
            cands = [rev(n), t + o, miss, joined(t, o)]
        e = count_e(t, o)
        if j < 2:
            e += " Each rod is 10, not 1."
        its.append(mcq_n(fig(blocks_svg(t, o)) + "What number do the blocks show?", n, cands, e, rnd))
    # how many tens / ones (4)
    for kind in ["tens", "ones", "tens", "ones"]:
        t, o = two_digit(rnd, used, 2, 7, 2, 9)
        n = 10 * t + o
        if kind == "tens":
            its.append(mcq_n(fig(blocks_svg(t, o)) + "How many tens are there?", t, [o, t * 10, n],
                             "Each rod is 1 ten. Count the rods: there are %s." % T(t), rnd))
        else:
            its.append(mcq_n(fig(blocks_svg(t, o)) + "How many ones are there?", o, [t, n, t + o],
                             "Each small cube is 1 one. Count the cubes: there are %s." % O(o), rnd))
    # which matches (4)
    for _ in range(4):
        t, o = two_digit(rnd, used, 2, 8, 2, 8)
        wrong = [TO(o, t), TO(t, o + 1), TO(t + 1, o)]
        its.append(mcq(fig(blocks_svg(t, o)) + "Which matches the blocks?", TO(t, o), wrong,
                       "A rod is 1 ten. A small cube is 1 one. There are %d rods and %d cubes: %s." % (t, o, TO(t, o)),
                       rnd))
    order = its[0:4] + its[12:14] + its[4:7] + its[16:18] + its[7:9] + its[14:16] + its[9:12] + its[18:]
    assert len(order) == 20
    return {"title": "Count tens and ones in blocks", "items": order}


# ============================================================ set 2: teen numbers
def teen_cands(n):
    o = n - 10
    return [rev(n), 1 + o, 100 + o, o, n + 1]


def set_teens(rnd, used):
    its = []
    teens = list(range(11, 20))
    rnd.shuffle(teens)
    # ten-frames -> number (7)
    for n in sorted(teens[:7], key=lambda v: (v % 3, v)):
        o = n - 10
        e = "The full frame is 1 ten. The other frame has %s. %s is %d." % (
            unit(o, "dot", "dots"), cap(TO(1, o)), n)
        its.append(mcq_n(fig(tenframes_svg(n)) + "What number do the ten-frames show?", n, teen_cands(n), e, rnd))
    # 1 ten and o ones = ? (5)
    rnd.shuffle(teens)
    for n in teens[:5]:
        o = n - 10
        e = "1 ten is 10. 10 and %d more is %d. Do not add 1 + %d." % (o, n, o)
        its.append(mcq_n("%s is ☐." % cap(TO(1, o)), n, [1 + o, rev(n), joined(1, o), n + 1], e, rnd))
    # n is 1 ten and ☐ ones (4)
    rest = [v for v in teens[5:] if v != 11] + [v for v in teens[:5] if v != 11]
    for n in rest[:4]:
        o = n - 10
        e = "%d is 10 and %d more. So %d is 1 ten and %s." % (n, o, n, O(o))
        its.append(mcq_n("%d is 1 ten and ☐ ones." % n, o, [1, 10, n, o + 1], e, rnd))
    # which shows (2)
    for n in [13, 17]:
        o = n - 10
        its.append(mcq("Which is the same as %d?" % n, TO(1, o), [TO(o, 1), TO(1, n), T(n)],
                       "%d is 10 and %d more. That is %s." % (n, o, TO(1, o)), rnd))
    # ten (2)
    its.append(mcq("Which is the same as 10 ones?", "1 ten", ["10 tens", "1 one", "0 tens"],
                   "10 ones make a bundle called a ten. 10 ones = 1 ten.", rnd))
    its.append(mcq_n("1 ten and 0 ones is ☐.", 10, [1, 100, 11],
                     "1 ten is 10. There are no more ones, so the number is 10. The 0 shows 0 ones.", rnd))
    order = its[18:19] + its[0:3] + its[7:9] + its[19:20] + its[3:5] + its[12:14] + its[9:11] + its[5:7] \
        + its[14:16] + its[11:12] + its[16:18]
    assert len(order) == 20, len(order)
    return {"title": "Teen numbers: 1 ten and some ones", "items": order}


# ============================================================ set 3: tens and ones in a number
def set_digits(rnd, used):
    its = []
    # chart -> number (2)
    for _ in range(2):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        its.append(mcq_n(fig(chart_svg(n)) + "What number is in the chart?", n, [rev(n), joined(t, o), t + o],
                         "The chart shows %s. Write the tens digit first: %d." % (TO(t, o), n), rnd))
    # n is ☐ tens and o ones (4)
    for o in rnd.sample(range(1, 10), 4):
        t, o = two_digit(rnd, used, 2, 9, o, o)
        n = 10 * t + o
        its.append(mcq_n("%d is ☐ tens and %s." % (n, O(o)), t, [o, t * 10, n],
                         "In %d the %d is in the tens place. %d is %s." % (n, t, n, TO(t, o)), rnd))
    # n is t tens and ☐ ones (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 9, 2, 9)
        n = 10 * t + o
        its.append(mcq_n("%d is %s and ☐ ones." % (n, T(t)), o, [t, n, o * 10],
                         "In %d the %d is in the ones place. %d is %s." % (n, o, n, TO(t, o)), rnd))
    # what does the tens digit mean (4)
    for t in rnd.sample(range(2, 10), 4):
        t, o = two_digit(rnd, used, t, t, 1, 9)
        n = 10 * t + o
        its.append(mcq("What does the %d in %d mean?" % (t, n), T(t), [O(t), T(o), T(n)],
                       "The %d is first, in the tens place. It means %s. That is %d." % (t, T(t), t * 10), rnd))
    # what does the ones digit mean (2)
    for _ in range(2):
        t, o = two_digit(rnd, used, 2, 9, 2, 9)
        n = 10 * t + o
        its.append(mcq("What does the %d in %d mean?" % (o, n), O(o), [T(o), O(t), O(n)],
                       "The %d is last, in the ones place. It means %s." % (o, O(o)), rnd))
    # tens and ones -> number (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        its.append(mcq_n("Which number has %s?" % TO(t, o), n, [rev(n), joined(t, o), t + o],
                         "Write the tens first, then the ones: %d, %d. The number is %d." % (t, o, n), rnd))
    # in which number is the d worth d tens (2)
    for d, others in [(5, [35, 15, 75]), (3, [43, 93, 63])]:
        o = rnd.choice([x for x in range(1, 10) if x != d])
        n = 10 * d + o
        its.append(mcq_n("In which number does the %d mean %s?" % (d, T(d)), n, others,
                         "The tens digit is the first digit. In %d the %d is first, so it means %s. "
                         "In the other numbers the %d is in the ones place." % (n, d, T(d), d), rnd))
    order = its[0:2] + its[2:4] + its[6:8] + its[15:17] + its[9:11] + its[4:6] + its[8:9] + its[13:15] \
        + its[17:18] + its[11:13] + its[18:]
    assert len(order) == 20, len(order)
    return {"title": "Tens and ones in a number", "items": order}


# ============================================================ set 4: decades and other ways
def set_decades(rnd, used):
    its = []
    tens = list(range(2, 10))
    rnd.shuffle(tens)
    # rods only (4)
    for t in tens[:4]:
        n = 10 * t
        its.append(mcq_n(fig(blocks_svg(t, 0)) + "What number do the blocks show?", n, [t, t * 100, n + 10],
                         "Count the rods by tens: %s. There are no cubes, so there are 0 ones. The number is %d."
                         % (by_tens(t), n), rnd))
    # t tens = ? (4)
    for k, t in enumerate(tens[4:8]):
        n = 10 * t
        its.append(mcq_n("%s is ☐." % T(t) if k % 2 == 0 else "%s and 0 ones is ☐." % T(t), n,
                         [t, t * 100, n - 10 if k % 2 else n + 10],
                         "Count by tens: %s. %s is %d. Write 0 for 0 ones." % (by_tens(t), cap(T(t)), n), rnd))
    # how many tens in a decade (3)
    for k, t in enumerate(rnd.sample([3, 4, 6, 7, 8, 9], 3)):
        n = 10 * t
        its.append(mcq_n("%d is ☐ tens and 0 ones." % n, t, [n, 10, t + 1 if t < 9 else t - 1], (
            "%d has %s %d in the tens place and a 0 in the ones place. %d is %s and 0 ones." % (n, "an" if t == 8 else "a", t, n, T(t))),
            rnd))
    # which is the same as 90 (2)
    for n in [90, 60]:
        t = n // 10
        its.append(mcq("Which is the same as %d?" % n, T(t), [O(t), T(n), TO(t, 1)],
                       "%d is %s and 0 ones. Count by tens to check: %s." % (n, T(t), by_tens(t)), rnd))
    # more than 9 ones (3)
    for t, o in [(2, 13), (3, 15), (4, 11)]:
        n = 10 * t + o
        its.append(mcq_n("%s is ☐." % TO(t, o), n, [int("%d%d" % (t, o)), t + o, 10 * t + o % 10],
                         "%s is 1 ten and %s. So you have %s. That is %d." % (cap(O(o)), O(o - 10),
                                                                              TO(t + 1, o - 10), n), rnd))
    # blocks with more than 9 cubes (2)
    for t, o in [(2, 12), (1, 14)]:
        n = 10 * t + o
        its.append(mcq_n(fig(blocks_svg(t, o)) + "What number do the blocks show?", n,
                         [int("%d%d" % (t, o)), t + o, 10 * t + o % 10],
                         "Count the rods: %s. Count the cubes: %d. 10 cubes make 1 more ten. "
                         "So it is %s. That is %d." % (by_tens(t), o, TO(t + 1, o - 10), n), rnd))
    # another way (2)
    for n in [25, 34]:
        t, o = divmod(n, 10)
        its.append(mcq("Which is another way to show %d?" % n, TO(t - 1, o + 10),
                       [TO(t, o + 10), TO(t - 1, o), TO(o, t)],
                       "Break 1 ten into 10 ones. %s becomes %s. It is still %d." % (TO(t, o), TO(t - 1, o + 10), n),
                       rnd))
    order = its[0:2] + its[4:6] + its[11:13] + its[2:4] + its[6:8] + its[8:11] + its[13:16] + its[16:18] + its[18:]
    assert len(order) == 20, len(order)
    return {"title": "Tens with 0 ones, and more than 9 ones", "items": order}


# ============================================================ set 5: story problems
THINGS = [  # (thing, group noun, loose word)
    ("sticks", "bundles", "loose sticks"),
    ("crayons", "boxes", "loose crayons"),
    ("beads", "strings", "loose beads"),
    ("pencils", "packs", "loose pencils"),
    ("stickers", "sheets", "loose stickers"),
    ("straws", "bundles", "loose straws"),
    ("markers", "boxes", "loose markers"),
]


def set_story(rnd, used):
    its = []
    things = THINGS[:]
    rnd.shuffle(things)
    ti = [0]

    def nxt():
        th = things[ti[0] % len(things)]
        ti[0] += 1
        return th

    # bundles + loose -> total (6), the first 3 with a picture
    for j in range(6):
        if j < 3:
            th = THINGS[0]
            b, l = [(2, 4), (3, 7), (4, 5)][j]
        else:
            th = nxt()
            while th[0] == "sticks":
                th = nxt()
            b, l = two_digit(rnd, used, 2, 8, 2, 9)
        n = 10 * b + l
        name, she, her = P.next()
        thing, grp, loose = th
        if j < 3:
            q = fig(sticks_svg(b, l)) + "%s has %d bundles of 10 sticks. %s has %d loose sticks. How many sticks does %s have?" % (
                name, b, cap(she), l, she)
        else:
            q = "%s has %d %s of 10 %s. %s also has %d %s. How many %s does %s have?" % (
                name, b, grp, thing, cap(she), l, loose, thing, she)
        e = "%d %s of 10 is %s, or %d. %d %s is %s. %d and %d is %d." % (
            b, grp, T(b), 10 * b, l, loose, O(l), 10 * b, l, n)
        its.append(mcq_n(q, n, [rev(n), b + l, joined(b, l)], e, rnd))
    # total -> full groups (3) and leftovers (3)
    for j in range(6):
        th = nxt()
        thing, grp, loose = th
        b, l = two_digit(rnd, used, 2, 8, 2, 9)
        n = 10 * b + l
        name, she, her = P.next()
        head = "%s has %d %s. %s puts them in %s of 10. " % (name, n, thing, cap(she), grp)
        if j % 2 == 0:
            q = head + "How many full %s does %s make?" % (grp, she)
            its.append(mcq_n(q, b, [l, 10 * b, n],
                             "%d is %s. Each ten fills 1 %s. So %s makes %d full %s." % (
                                 n, TO(b, l), grp[:-2] if grp.endswith("xes") else grp[:-1], she, b, grp), rnd))
        else:
            q = head + "How many %s are left over?" % thing
            its.append(mcq_n(q, l, [b, 10 * b, n],
                             "%d is %s. The tens go in %d %s. The %s are left over: %d %s." % (
                                 n, TO(b, l), b, grp, O(l), l, thing), rnd))
    # full groups only -> total (3)
    for t, (thing, grp, word) in zip(rnd.sample(range(3, 10), 3), [("eggs", "cartons", "carton"),
                                                                   ("crayons", "boxes", "box"),
                                                                   ("apples", "bags", "bag")]):
        name, she, her = P.next()
        n = 10 * t
        q = "Each %s has 10 %s. %s has %d full %s. How many %s does %s have?" % (word, thing, name, t, grp, thing, she)
        its.append(mcq_n(q, n, [t, t * 100, t + 10],
                         "%d %s of 10 is %s. Count by tens: %s. %s has %d %s." % (
                             t, grp, T(t), by_tens(t), name, n, thing), rnd))
    # make a ten (2)
    name, she, her = P.next()
    its.append(mcq_n("%s has 13 cubes. %s snaps 10 of them into a rod. How many loose cubes are left?" % (name, cap(she)),
                     3, [13, 10, 1],
                     "13 is 1 ten and 3 ones. The rod uses 10 cubes. 3 cubes are left.", rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s has 1 rod and 9 cubes. %s gets 1 more cube. What number does %s have now?" % (
        name, cap(she), she), 20, [110, 19, 11],
        "1 rod and 9 cubes is 19. 1 more is 20. Now there are 10 cubes. They make 1 more ten: 2 tens and 0 ones = 20.", rnd))
    # compare (2)
    g, b_ = P.next(), P.next()
    its.append(mcq("%s has 7 tens. %s has 70 ones. Who has more?" % (g[0], b_[0]), "They have the same",
                   [g[0], b_[0], "We cannot tell"],
                   "7 tens is 70. 70 ones is also 70. They have the same.", rnd))
    g, b_ = P.next(), P.next()
    its.append(mcq("%s has 4 bundles of 10 straws. %s has 9 loose straws. Who has more straws?" % (g[0], b_[0]),
                   g[0], [b_[0], "They have the same", "We cannot tell"],
                   "4 bundles of 10 is 40 straws. 40 is more than 9. %s has more." % g[0], rnd))
    # more than 9 loose (1)
    name, she, her = P.next()
    its.append(mcq_n("%s has 2 bundles of 10 straws and 14 loose straws. How many straws does %s have?" % (name, she),
                     34, [214, 16, 24],
                     "14 loose straws make 1 more bundle and 4 left. So it is 3 tens and 4 ones. That is 34.", rnd))
    order = its[0:3] + its[12:15] + its[3:6] + its[6:8] + its[15:16] + its[8:10] + its[18:19] \
        + its[10:12] + its[16:18] + its[19:]
    assert len(order) == 20, len(order)
    return {"title": "Story problems with tens", "items": order}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>10 ones make 1 ten</h2>"
        "<p>Put 10 ones together. Now you have a bundle. We call it a <b>ten</b>.</p>"
        "<figure class='sn-fig'>" + sticks_svg(1, 3) +
        "<figcaption>1 bundle of 10 sticks and 3 loose sticks. That is 1 ten and 3 ones, or 13.</figcaption></figure>"
        "<h2>Teen numbers</h2>"
        "<p>The numbers 11 to 19 are <b>1 ten and some ones</b>. 16 is 1 ten and 6 ones.</p>"
        "<figure class='sn-fig'>" + tenframes_svg(16) +
        "<figcaption>A full ten-frame is 1 ten. 6 more dots are 6 ones. 10 and 6 is 16.</figcaption></figure>"
        "<h2>Two digits: tens and ones</h2>"
        "<p>A 2-digit number has two places. The <b>first digit tells the tens</b>. "
        "The <b>last digit tells the ones</b>.</p>"
        "<figure class='sn-fig'>" + blocks_svg(4, 7, labels=True) +
        "<figcaption>A rod is 1 ten. A small cube is 1 one. 4 tens and 7 ones make 47.</figcaption></figure>"
        "<figure class='sn-fig'>" + chart_svg(47, hi=1) +
        "<figcaption>In 47 the 4 means 4 tens, or 40. The 7 means 7 ones.</figcaption></figure>" +
        ex("Count the blocks", "There are 3 rods and 5 cubes. What number is it?",
           "Count the rods by tens: 10, 20, 30. Count on the cubes: 31, 32, 33, 34, 35.", "35") +
        ex("What does the digit mean?", "What does the 6 in 62 mean?",
           "The 6 is first. It is in the tens place.", "6 tens, or 60") +
        "<h2>Tens with 0 ones</h2>"
        "<p>10, 20, 30, 40, 50, 60, 70, 80 and 90 have <b>0 ones</b>. 50 is 5 tens and 0 ones. "
        "The 0 shows there are no ones.</p>" +
        ex("More than 9 ones", "2 tens and 13 ones is ☐.",
           "13 ones is 1 ten and 3 ones. So you have 3 tens and 3 ones.", "33") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up the digits (4 tens and 7 ones as 74)", "Tens come first: 47"],
            ["Writing 4 tens and 7 ones as 407", "Use only 2 digits: 47"],
            ["Counting a rod as 1 (4 rods and 7 cubes as 11)", "Each rod is 10: 10, 20, 30, 40, then 41 to 47"],
            ["Adding 1 + 6 for 1 ten and 6 ones (7)", "1 ten is 10. 10 and 6 is 16"],
            ["Writing 5 tens as 5", "Write 0 for 0 ones: 50"],
        ])
    )


FAQ = [
    {"q": "What is place value in 1st grade math?",
     "a": "In Grade 1, place value means a 2-digit number is made of tens and ones. In 47, the 4 means 4 tens (40) and the 7 means 7 ones."},
    {"q": "How do you explain teen numbers to a first grader?",
     "a": "Show a full ten-frame or a bundle of 10 sticks, then some extra ones. 16 is 1 ten and 6 ones, so the 1 in 16 means 10, not 1."},
    {"q": "Why does my child write 74 for 47?",
     "a": "They mix up which digit is the tens. Have them build the number with 4 rods and 7 cubes, then say “4 tens first, then 7 ones” as they write 47."},
    {"q": "How do you teach tens and ones at home?",
     "a": "Bundle straws, sticks or pencils in groups of 10 with a rubber band. Ask your child to make a number with bundles and loose ones, then count by tens and count on the ones."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so the small cubes, dots and sticks stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


P = None


def gen_place_value():
    global P
    rnd = random.Random(104)
    P = People(rnd)
    used = set()
    sets = [set_blocks(rnd, used), set_teens(rnd, used), set_digits(rnd, used),
            set_decades(rnd, used), set_story(rnd, used)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "place-value-tens-ones", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value: Tens and Ones",
        "seo_title": "Grade 1 Place Value Worksheets: Tens and Ones, Teen Numbers and Base-Ten Blocks",
        "short_title": "Tens and ones",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "1.NBT.B.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/NBT/B/2/",
        "standard_text": "Understand that the two digits of a two-digit number represent amounts of tens and ones.",
        "meta_desc": "Free Grade 1 place value worksheets: count tens and ones in base-ten blocks, teen numbers on ten-frames, what each digit means, 10, 20 … 90 as tens, and bundle story problems. 100 questions with an answer key.",
        "key_big": "10 ones make 1 ten. In a 2-digit number, the first digit is tens and the last digit is ones.",
        "key_sub": "47 is 4 tens and 7 ones. 16 is 1 ten and 6 ones. 50 is 5 tens and 0 ones.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base-ten blocks|ten-frames|bundles of sticks")


if __name__ == "__main__":
    u = gen_place_value()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
