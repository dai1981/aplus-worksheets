# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Tens and Ones (AC9M1N02, Australian Curriculum v9.0)
  python tools/gen_au_maths_y1_tens_ones.py
HTML attributes use single quotes (no backslashes in the JSON).
Year 1: two-digit numbers, very short sentences for 6-7 year olds, a picture in almost every question.
Australian English: MAB longs and minis, maths, colour.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#c98a3d"
BAND = "#c0392b"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


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


def joined(t, o):
    """The “406” mistake: writing the tens value and then the ones."""
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


ONES_W = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TENS_W = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    t, o = divmod(n, 10)
    assert 20 <= n <= 99
    return TENS_W[t] + ("-" + ONES_W[o] if o else "")


# ------------------------------------------------------------ figures
U = 8                      # MAB: a mini = U x U, a long = U x 10U (exactly 10 minis)
RG, CG, GG, M = 6, 4, 20, 6


def mab_svg(t, o, labels=False):
    """MAB: t longs and o minis (columns of 5). Sizes are exact (1 : 10)."""
    F = 10 * U
    groups = []

    def longs(x, y):
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

    def minis(x, y):
        s = []
        for k in range(o):
            cx = x + (k // 5) * (U + CG + 2)
            cy = y + (k % 5) * (U + CG + 4)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, U, U, CUBE, GREEN))
        return s

    if t:
        groups.append((t * U + (t - 1) * RG, F, longs, unit(t, "long", "longs")))
    if o:
        groups.append((ccols * U + (ccols - 1) * (CG + 2), 5 * U + 4 * (CG + 4), minis, unit(o, "mini", "minis")))
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
    return svg_wrap(W, Hh, "".join(s), "MAB blocks")


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
    """b bundles of 10 sticks (with a rubber band) and some loose sticks."""
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
    """Tens / ones chart with n in it. hi = 1 (tens) or 0 (ones) to colour red."""
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


def card_svg(n, hi):
    """A number card. hi = 1 colours the tens digit red and underlines it, hi = 0 the ones digit."""
    W, Hh = 120, 80
    t, o = divmod(n, 10)
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='10' fill='#fff' stroke='%s' stroke-width='2.5'/>"
         % (W - 6, Hh - 6, GREEN)]
    for k, (d, place) in enumerate([(t, 1), (o, 0)]):
        cx = 38 + k * 44
        col = RED if hi == place else INK
        s.append("<text x='%d' y='56' font-size='48' font-weight='800' fill='%s' text-anchor='middle'>%d</text>"
                 % (cx, col, d))
        if hi == place:
            s.append("<line x1='%d' y1='66' x2='%d' y2='66' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
                     % (cx - 14, cx + 14, RED))
    return svg_wrap(W, Hh, "".join(s), "number card")


def ppw_svg(whole, a, b):
    """Part-part-whole: whole on top, parts below. A part given as None shows a red ?."""
    W, Hh = 200, 128
    bw, bh = 72, 44
    s = []
    boxes = [(W / 2, 6, whole), (6 + bw / 2, Hh - 6 - bh, a), (W - 6 - bw / 2, Hh - 6 - bh, b)]
    for cx, y in [(boxes[1][0], boxes[1][1]), (boxes[2][0], boxes[2][1])]:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>"
                 % (W / 2, 6 + bh, cx, y, GREEN))
    for k, (cx, y, v) in enumerate(boxes):
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx - bw / 2, y, bw, bh, FILL if k == 0 else "#fff", GREEN))
        txt, col = ("?", RED) if v is None else (str(v), INK)
        s.append("<text x='%.1f' y='%d' font-size='26' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx, y + 32, col, txt))
    return svg_wrap(W, Hh, "".join(s), "part-part-whole")


def table_svg(rows, head):
    """Small table: name and number."""
    c1, c2, rh = 110, 80, 30
    x0 = y0 = 4
    W, Hh = 2 * x0 + c1 + c2, 2 * y0 + rh * (len(rows) + 1)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, c1 + c2, rh, FILL),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
         % (x0, y0, c1 + c2, rh * (len(rows) + 1), GREEN),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
         % (x0 + c1, y0, x0 + c1, y0 + rh * (len(rows) + 1), GREEN)]
    for i, (a, b) in enumerate([head] + rows):
        y = y0 + i * rh
        if i:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (x0, y, x0 + c1 + c2, y, GREEN))
        wt = "700" if i == 0 else "400"
        s.append("<text x='%d' y='%d' font-size='16' font-weight='%s' fill='%s'>%s</text>" % (x0 + 10, y + 21, wt, INK, a))
        s.append("<text x='%.1f' y='%d' font-size='16' font-weight='%s' fill='%s' text-anchor='middle'>%s</text>"
                 % (x0 + c1 + c2 / 2, y + 21, "700", INK, b))
    return svg_wrap(W, Hh, "".join(s), "table")


def count_e(t, o, thing="longs", one="minis"):
    n = 10 * t + o
    s = "Count the %s by tens: %s. " % (thing, by_tens(t))
    if o:
        s += "Count on the %s: %s. " % (one, ", ".join(str(10 * t + i) for i in range(1, o + 1)))
    s += "%s is %d." % (cap(TO(t, o)), n)
    return s


def two_digit(rnd, used, tlo=1, thi=9, olo=1, ohi=9, distinct=True):
    while True:
        t, o = rnd.randint(tlo, thi), rnd.randint(olo, ohi)
        n = 10 * t + o
        if distinct and t == o:
            continue
        if n not in used:
            used.add(n)
            return t, o


# ============================================================ set 1: MAB and bundles
def set_count(rnd, used):
    its = []
    # MAB -> number (6), small tens first
    for j, (lo, hi) in enumerate([(1, 2), (2, 3), (2, 4), (3, 6), (4, 7), (5, 9)]):
        t, o = two_digit(rnd, used, lo, hi, 1, 9)
        n = 10 * t + o
        miss = [n + 1, n - 1, n + 10, n - 10][j % 4]
        cands = [rev(n), t + o, joined(t, o), miss] if j % 2 == 0 else [t + o, rev(n), miss, joined(t, o)]
        e = count_e(t, o)
        if j < 2:
            e += " A long is 10, not 1."
        its.append(mcq_n(fig(mab_svg(t, o)) + "What number do the MAB show?", n, cands, e, rnd))
    # sticks -> number (4)
    for j, (lo, hi) in enumerate([(1, 3), (2, 4), (3, 5), (4, 6)]):
        t, o = two_digit(rnd, used, lo, hi, 1, 9)
        n = 10 * t + o
        e = count_e(t, o, "bundles", "loose sticks")
        its.append(mcq_n(fig(sticks_svg(t, o)) + "How many sticks are there?", n,
                         [t + o, rev(n), n + 10 if j % 2 else n - 1, joined(t, o)], e, rnd))
    # how many tens / ones (4)
    for kind, pic in [("tens", "mab"), ("ones", "mab"), ("tens", "sticks"), ("ones", "sticks")]:
        t, o = two_digit(rnd, used, 2, 6, 2, 9)
        n = 10 * t + o
        f = fig(mab_svg(t, o)) if pic == "mab" else fig(sticks_svg(t, o))
        if kind == "tens":
            e = ("Each long is 1 ten. Count the longs: %s." if pic == "mab" else
                 "Each bundle is 1 ten. Count the bundles: %s.") % T(t)
            its.append(mcq_n(f + "How many tens are there?", t, [o, t * 10, n], e, rnd))
        else:
            e = ("Each mini is 1 one. Count the minis: %s." if pic == "mab" else
                 "Each loose stick is 1 one. Count them: %s.") % O(o)
            its.append(mcq_n(f + "How many ones are there?", o, [t, n, t + o], e, rnd))
    # which matches (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 8, 2, 8)
        its.append(mcq(fig(mab_svg(t, o)) + "Which matches the MAB?", TO(t, o), [TO(o, t), TO(t, o + 1), TO(t + 1, o)],
                       "A long is 1 ten. A mini is 1 one. There are %d longs and %d minis: %s." % (t, o, TO(t, o)), rnd))
    # longs only (3)
    for t in rnd.sample([3, 5, 6, 8], 3):
        n = 10 * t
        used.add(n)
        its.append(mcq_n(fig(mab_svg(t, 0)) + "What number do the MAB show?", n, [t, n + 10, n - 10],
                         "Count the longs by tens: %s. There are no minis, so there are 0 ones. The number is %d."
                         % (by_tens(t), n), rnd))
    order = its[0:3] + its[10:12] + its[6:8] + its[3:4] + its[12:14] + its[8:10] + its[17:19] + its[4:6] \
        + its[14:17] + its[19:20]
    assert len(order) == 20, len(order)
    return {"title": "Count tens and ones with MAB and bundles", "items": order}


# ============================================================ set 2: write the number
def set_write(rnd, used):
    its = []
    # teen numbers on ten-frames (4)
    teens = rnd.sample(range(11, 20), 4)
    for n in teens:
        o = n - 10
        its.append(mcq_n(fig(tenframes_svg(n)) + "What number do the ten-frames show?", n,
                         [rev(n), 1 + o, joined(1, o), n + 1],
                         "The full frame is 1 ten. The other frame has %s. 10 and %d is %d." % (
                             unit(o, "dot", "dots"), o, n), rnd))
    # chart -> number (4)
    for _ in range(4):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        its.append(mcq_n(fig(chart_svg(n)) + "What number is in the chart?", n, [rev(n), joined(t, o), t + o],
                         "The chart shows %s. Write the tens digit first, then the ones: %d." % (TO(t, o), n), rnd))
    # t tens and o ones is ? (4), text only
    for _ in range(4):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        its.append(mcq_n("%s is ☐." % cap(TO(t, o)), n, [rev(n), t + o, joined(t, o)],
                         "%s is %d. Then add %s: %d." % (cap(T(t)), 10 * t, O(o), n), rnd))
    # tens with 0 ones (2)
    for t in rnd.sample([2, 4, 7, 9], 2):
        n = 10 * t
        its.append(mcq_n(fig(sticks_svg(t, 0)) + "%s is ☐." % cap(T(t)), n, [t, n + 1, 10 + t],
                         "Count by tens: %s. %s is %d. Write 0 for 0 ones." % (by_tens(t), cap(T(t)), n), rnd))
    # number words (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        its.append(mcq_n("Write “%s” as a number." % words(n), n, [joined(t, o), rev(n), 10 * t],
                         "“%s” is %d and %d. That is %s: %d. Do not write %d." % (
                             words(n), 10 * t, o, TO(t, o), n, joined(t, o)), rnd))
    # more than 9 ones (3)
    for t, o in [(2, 13), (3, 12), (4, 15)]:
        n = 10 * t + o
        its.append(mcq_n(fig(mab_svg(t, o)) + "What number do the MAB show?", n,
                         [int("%d%d" % (t, o)), t + o, 10 * t + o % 10],
                         "Count the longs: %s. There are %d minis. 10 minis make 1 more ten. "
                         "So it is %s. That is %d." % (by_tens(t), o, TO(t + 1, o - 10), n), rnd))
    order = its[0:2] + its[4:6] + its[12:14] + its[2:4] + its[8:10] + its[6:8] + its[14:16] + its[10:12] \
        + its[16:17] + its[17:20]
    assert len(order) == 20, len(order)
    return {"title": "Write the number", "items": order}


# ============================================================ set 3: tens and ones in a number
def set_digits(rnd, used):
    its = []
    # what does the tens digit mean (5)
    for t in rnd.sample(range(2, 10), 5):
        t, o = two_digit(rnd, used, t, t, 1, 9)
        n = 10 * t + o
        its.append(mcq(fig(card_svg(n, 1)) + "What does the red %d in %d mean?" % (t, n), T(t), [O(t), T(o), T(n)],
                       "The %d is first, in the tens place. It means %s. That is %d." % (t, T(t), t * 10), rnd))
    # what does the ones digit mean (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 9, 2, 9)
        n = 10 * t + o
        its.append(mcq(fig(card_svg(n, 0)) + "What does the red %d in %d mean?" % (o, n), O(o), [T(o), O(t), O(n)],
                       "The %d is last, in the ones place. It means %s." % (o, O(o)), rnd))
    # n is ? tens and o ones (4)
    for o in rnd.sample(range(1, 10), 4):
        t, o = two_digit(rnd, used, 2, 9, o, o)
        n = 10 * t + o
        its.append(mcq_n(fig(card_svg(n, None)) + "%d is ☐ tens and %s." % (n, O(o)), t, [o, t * 10, n],
                         "In %d the %d is in the tens place. %d is %s." % (n, t, n, TO(t, o)), rnd))
    # n is t tens and ? ones (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 9, 2, 9)
        n = 10 * t + o
        its.append(mcq_n(fig(card_svg(n, None)) + "%d is %s and ☐ ones." % (n, T(t)), o, [t, n, o * 10],
                         "In %d the %d is in the ones place. %d is %s." % (n, o, n, TO(t, o)), rnd))
    # value of the tens digit (3)
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        its.append(mcq_n(fig(card_svg(n, 1)) + "How much is the red %d in %d worth?" % (t, n), 10 * t, [t, n, 10 * o],
                         "The %d is in the tens place. %s is %d." % (t, cap(T(t)), 10 * t), rnd))
    # in which number does d mean d tens (2)
    for d, others in [(5, [35, 15, 75]), (3, [43, 93, 63])]:
        o = rnd.choice([x for x in range(1, 10) if x != d and 10 * d + x not in used])
        n = 10 * d + o
        used.add(n)
        its.append(mcq_n("In which number does the %d mean %s?" % (d, T(d)), n, others,
                         "The tens digit is the first digit. In %d the %d is first, so it means %s. "
                         "In the other numbers the %d is in the ones place." % (n, d, T(d), d), rnd))
    order = its[8:10] + its[0:2] + its[12:14] + its[5:7] + its[10:12] + its[2:4] + its[14:15] + its[7:8] \
        + its[15:18] + its[4:5] + its[18:20]
    assert len(order) == 20, len(order)
    return {"title": "Tens and ones in a number", "items": order}


# ============================================================ set 4: partition in different ways
def set_partition(rnd, used):
    its = []
    # which shows n (standard) (4), MAB picture
    for _ in range(4):
        t, o = two_digit(rnd, used, 2, 8, 2, 9)
        n = 10 * t + o
        its.append(mcq(fig(mab_svg(t, o)) + "Which shows %d?" % n, "%d + %d" % (10 * t, o),
                       ["%d + %d" % (t, o), "%d + %d" % (10 * o, t), "%d + %d" % (10 * t, 10 + o)],
                       "%d is %s. That is %d + %d." % (n, TO(t, o), 10 * t, o), rnd))
        assert 10 * t + o == n and 10 * o + t != n and 10 * t + 10 + o != n
    # standard part-part-whole, missing ones or tens (5)
    for j in range(5):
        t, o = two_digit(rnd, used, 2, 9, 1, 9)
        n = 10 * t + o
        if j % 2 == 0:
            its.append(mcq_n(fig(ppw_svg(n, 10 * t, None)) + "%d = %d + ☐" % (n, 10 * t), o, [t, n + 10 * t, 10 * o],
                             "%d is %s. The tens make %d. The ones make %d. So %d = %d + %d." % (
                                 n, TO(t, o), 10 * t, o, n, 10 * t, o), rnd))
        else:
            its.append(mcq_n(fig(ppw_svg(n, None, o)) + "%d = ☐ + %d" % (n, o), 10 * t, [t, n, n + o],
                             "%d is %s. %s is %d. So %d = %d + %d." % (n, TO(t, o), cap(T(t)), 10 * t, n, 10 * t, o), rnd))
    # non-standard, picture shows the regrouped MAB (2)
    for t, o in [(3, 4), (4, 6)]:
        n = 10 * t + o
        used.add(n)
        its.append(mcq_n(fig(mab_svg(t - 1, o + 10)) + "%d = %d + ☐" % (n, 10 * (t - 1)), o + 10,
                         [o, n + 10 * (t - 1), o + 9],
                         "Break 1 ten into 10 ones. %s becomes %s. So %d = %d + %d." % (
                             TO(t, o), TO(t - 1, o + 10), n, 10 * (t - 1), o + 10), rnd))
    # non-standard, part-part-whole only (4)
    for j in range(4):
        t, o = two_digit(rnd, used, 3, 9, 1, 9)
        n = 10 * t + o
        k = 1 if j < 2 else 2                     # take away 1 or 2 tens from the tens part
        part = 10 * (t - k)
        ans = n - part
        assert part + ans == n
        its.append(mcq_n(fig(ppw_svg(n, part, None)) + "%d = %d + ☐" % (n, part), ans,
                         [o, n + part, ans - 10 if ans - 10 != o else ans + 10],
                         "%d is %d + %d. Move %s from the tens to the ones: %d + %d = %d." % (
                             n, 10 * t, o, T(k), part, ans, n), rnd))
    # another way to make n (3), MAB
    for _ in range(3):
        t, o = two_digit(rnd, used, 2, 8, 1, 8)
        n = 10 * t + o
        its.append(mcq(fig(mab_svg(t, o)) + "Which is another way to make %d?" % n, "%d + %d" % (10 * (t - 1), o + 10),
                       ["%d + %d" % (10 * (t - 1), o), "%d + %d" % (10 * t, o + 10), "%d + %d" % (t, o)],
                       "Break 1 ten into 10 ones. %d + %d = %d. It is still %d." % (10 * (t - 1), o + 10, n, n), rnd))
    # regrouped MAB -> number (2)
    for t, o in [(3, 14), (5, 11)]:
        n = 10 * t + o
        used.add(n)
        its.append(mcq_n(fig(mab_svg(t, o)) + "What number do the MAB show?", n,
                         [int("%d%d" % (t, o)), t + o, 10 * t + o % 10],
                         "%d longs is %d. %d minis is 1 ten and %s. %d + %d = %d." % (
                             t, 10 * t, o, O(o - 10), 10 * t, o, n), rnd))
    order = its[0:4] + its[4:9] + its[16:18] + its[9:11] + its[18:20] + its[11:13] + its[13:16]
    assert len(order) == 20, len(order)
    return {"title": "Partition numbers in different ways", "items": order}


# ============================================================ set 5: compare (last 8 are word problems)
def more_than_q(rnd, n, used):
    t, o = divmod(n, 10)
    # wrong: smaller numbers with a bigger ones digit (the “look at the ones” mistake)
    big = [10 * (t - 1) + d for d in range(9, o, -1)]
    rnd.shuffle(big)
    wrong = big[:2] + [n - 1, n - 10]
    ans = 10 * (t + rnd.randint(1, 9 - t)) + rnd.randint(0, o - 1) if o > 0 else n + 10
    ans = ans if ans != n else n + 10
    assert ans > n and all(w < n for w in wrong)
    return mcq_n(fig(mab_svg(t, o)) + "The MAB show %d. Which number is more than %d?" % (n, n), ans, wrong,
                 "Look at the tens first. %d has %s. %d has %s. So %d is more than %d." % (
                     ans, T(ans // 10), n, T(t), ans, n), rnd)


def less_than_q(rnd, n, used):
    t, o = divmod(n, 10)
    small = [10 * (t + 1) + d for d in range(0, o)]
    rnd.shuffle(small)
    wrong = small[:2] + [n + 1, n + 10]
    ans = 10 * rnd.randint(1, t - 1) + rnd.randint(o + 1, 9)
    assert ans < n and all(w > n for w in wrong)
    return mcq_n(fig(mab_svg(t, o)) + "The MAB show %d. Which number is less than %d?" % (n, n), ans, wrong,
                 "Look at the tens first. %d has %s. %d has %s. So %d is less than %d." % (
                     ans, T(ans // 10), n, T(t), ans, n), rnd)


def set_compare(rnd, used):
    its = []
    for n in [24, 37, 58]:
        its.append(more_than_q(rnd, n, used))
    for n in [62, 75, 83]:
        its.append(less_than_q(rnd, n, used))
    # greatest / smallest (4)
    for nums, most in [([46, 64, 59, 38], True), ([27, 72, 45, 51], True),
                       ([53, 35, 41, 49], False), ([81, 18, 29, 36], False)]:
        ans = max(nums) if most else min(nums)
        word = "greatest" if most else "smallest"
        trap = max(nums, key=lambda v: v % 10) if most else min(nums, key=lambda v: v % 10)
        e = "Look at the tens first. %d has %s. %s. So %d is the %s." % (
            ans, T(ans // 10), "No other number has that many tens" if most else "No other number has so few tens",
            ans, word)
        if trap != ans:
            e += " Do not look at the ones first: %d is not the %s." % (trap, word)
        its.append(mcq_n("Which number is the %s?" % word, ans, [v for v in nums if v != ans], e, rnd))
    # true statement (2)
    for a, b in [(46, 64), (39, 93)]:
        its.append(mcq("Which is true?", "%d is more than %d" % (b, a),
                       ["%d is more than %d" % (a, b), "%d is less than %d" % (b, a), "%d is the same as %d" % (a, b)],
                       "%d has %s. %d has %s. %s is more than %s, so %d is more than %d." % (
                           b, T(b // 10), a, T(a // 10), cap(T(b // 10)), T(a // 10), b, a), rnd))
    # word problems (8)
    things = [("Four friends collected shells at the beach. Who collected the most?", "Shells"),
              ("Four friends collected cans for recycling. Who collected the fewest?", "Cans"),
              ("Four friends did skips with a skipping rope. Who did the most skips?", "Skips"),
              ("Four friends counted their stickers. Who has the fewest stickers?", "Stickers")]
    sets_ = [[46, 64, 59, 37], [28, 82, 71, 49], [53, 35, 44, 29], [67, 76, 81, 59]]
    for j, ((thing, head), nums) in enumerate(zip(things, sets_)):
        ppl = [P.next()[0] for _ in range(4)]
        most = j % 2 == 0
        ans_i = nums.index(max(nums) if most else min(nums))
        q = (fig(table_svg([[p, str(v)] for p, v in zip(ppl, nums)], ["Name", head])) +
             thing)
        e = "Look at the tens first. %d is %s. No one else has %s tens. So the answer is %s." % (
            nums[ans_i], TO(nums[ans_i] // 10, nums[ans_i] % 10), "so many" if most else "so few", ppl[ans_i])
        assert len({v // 10 for v in nums}) == 4
        its.append(mcq(q, ppl[ans_i], [p for k, p in enumerate(ppl) if k != ans_i], e, rnd))
    g, b_ = P.next(), P.next()
    its.append(mcq(fig(sticks_svg(5, 2)) + "%s has 5 bundles of 10 sticks and 2 loose sticks. %s has 25 sticks. "
                   "Who has more?" % (g[0], b_[0]), g[0], [b_[0], "They have the same", "We cannot tell"],
                   "5 bundles and 2 loose sticks is 52. %d is more than 25. %s has more." % (52, g[0]), rnd))
    g, b_ = P.next(), P.next()
    its.append(mcq(fig(mab_svg(4, 7)) + "%s made 47 with MAB. %s made 3 longs and 17 minis. Who made more?" % (
        g[0], b_[0]), "They have the same", [g[0], b_[0], "We cannot tell"],
        "17 minis is 1 ten and 7 ones. So 3 longs and 17 minis is 4 tens and 7 ones: 47. They have the same.", rnd))
    assert 30 + 17 == 47
    g, b_ = P.next(), P.next()
    its.append(mcq("%s’s class read 74 books. %s’s class read 47 books. Which class read more books?" % (g[0], b_[0]),
                   "%s’s class" % g[0], ["%s’s class" % b_[0], "They read the same", "We cannot tell"],
                   "74 has 7 tens. 47 has 4 tens. 7 tens is more than 4 tens. %s’s class read more." % g[0], rnd))
    g, b_ = P.next(), P.next()
    its.append(mcq("The Koalas scored 58 points in a footy game. The Wombats scored 85 points. Who won?",
                   "The Wombats", ["The Koalas", "It was a draw", "We cannot tell"],
                   "85 has 8 tens. 58 has 5 tens. 85 is more than 58, so the Wombats won.", rnd))
    order = its[0:2] + its[3:5] + its[2:3] + its[5:6] + its[6:8] + its[10:11] + its[8:10] + its[11:12] \
        + its[12:14] + its[16:18] + its[14:16] + its[18:20]
    assert len(order) == 20, len(order)
    return {"title": "Compare two-digit numbers", "items": order}


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
        "<h2>MAB: longs and minis</h2>"
        "<p>In class you use <b>MAB</b>. A <b>long</b> is 1 ten. A <b>mini</b> is 1 one. "
        "Count the longs by tens. Then count on the minis.</p>"
        "<figure class='sn-fig'>" + mab_svg(4, 6, labels=True) +
        "<figcaption>4 longs and 6 minis. Count 10, 20, 30, 40, then 41, 42, 43, 44, 45, 46. That is 46."
        "</figcaption></figure>"
        "<h2>Tens and ones in a number</h2>"
        "<p>A two-digit number has two places. The <b>first digit tells the tens</b>. "
        "The <b>last digit tells the ones</b>.</p>"
        "<figure class='sn-fig'>" + chart_svg(46, hi=1) +
        "<figcaption>In 46 the 4 means 4 tens, or 40. The 6 means 6 ones.</figcaption></figure>" +
        ex("What does the digit mean?", "What does the 4 in 46 mean?",
           "The 4 is first. It is in the tens place.", "4 tens, or 40") +
        "<h2>Partition in different ways</h2>"
        "<p>To <b>partition</b> means to split a number into parts. "
        "You can break 1 ten into 10 ones. The number stays the same.</p>"
        "<figure class='sn-fig'>" + ppw_svg(34, 30, 4) +
        "<figcaption>34 is 3 tens and 4 ones. 34 = 30 + 4.</figcaption></figure>" +
        ex("Another way", "34 = 20 + ☐",
           "Break 1 ten into 10 ones. 3 tens and 4 ones becomes 2 tens and 14 ones.", "14, so 34 = 20 + 14") +
        "<h2>Compare two-digit numbers</h2>"
        "<p>Look at the <b>tens first</b>. More tens means a bigger number. "
        "If the tens are the same, look at the ones.</p>" +
        ex("Which is more?", "Which is more, 46 or 64?",
           "46 has 4 tens. 64 has 6 tens. 6 tens is more than 4 tens.", "64") +
        ex("Same tens", "Which is more, 52 or 57?",
           "Both have 5 tens. Look at the ones: 7 ones is more than 2 ones.", "57") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the digits (46 = 4 + 6 = 10)", "The 4 is 4 tens: 46 = 40 + 6"],
            ["Swapping tens and ones (4 tens and 6 ones as 64)", "Tens come first: 46"],
            ["Writing “forty-six” as 406", "Use only 2 digits: 46"],
            ["Counting a long as 1 (4 longs and 6 minis as 10)", "Each long is 10: 10, 20, 30, 40, then 41 to 46"],
            ["Looking at the ones first (39 is more than 41)", "Look at the tens first: 41 is more than 39"],
        ])
    )


FAQ = [
    {"q": "What do Year 1 students learn about tens and ones in Australia?",
     "a": "The Australian Curriculum (AC9M1N02) asks Year 1 students to partition one- and two-digit numbers in different ways, including into tens and ones. For example, 34 is 3 tens and 4 ones, 30 + 4, or 20 + 14."},
    {"q": "What are MAB in Year 1 maths?",
     "a": "MAB (multi-base arithmetic blocks) are the base-ten blocks used in Australian classrooms. A long is 10 and a mini is 1, so 4 longs and 6 minis make 46."},
    {"q": "What does partition mean in Year 1 maths?",
     "a": "To partition is to split a number into parts. 46 can be split into 40 and 6, or into 30 and 16, and it is still 46."},
    {"q": "Why does my child write 64 for 46?",
     "a": "They mix up which digit shows the tens. Build the number with 4 bundles of 10 and 6 loose sticks, then say “4 tens first, then 6 ones” as they write 46."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so the minis, dots and sticks stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


P = None


def gen():
    global P
    rnd = random.Random(1802)
    P = People(rnd)
    sets = [set_count(rnd, set()), set_write(rnd, set()), set_digits(rnd, set()),
            set_partition(rnd, set()), set_compare(rnd, set())]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in keys, it["q"]
            keys.add(key)
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "tens-and-ones", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Tens and Ones: Partition Two-Digit Numbers",
        "seo_title": "Year 1 Tens and Ones Worksheets: MAB, Partitioning and Comparing, Free with Answer Key",
        "short_title": "Tens and ones",
        "domain": "Number",
        "standard_code": "AC9M1N02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Partition one- and two-digit numbers in different ways using physical and virtual materials, including partitioning two-digit numbers into tens and ones",
        "meta_desc": "Free Year 1 tens and ones maths worksheets for the Australian Curriculum: count MAB longs and minis and bundles of sticks, write the number, what each digit means, partition numbers in different ways (34 = 30 + 4 = 20 + 14) and compare two-digit numbers. 100 questions with an answer key.",
        "key_big": "10 ones make 1 ten. In a two-digit number, the first digit is the tens and the last digit is the ones.",
        "key_sub": "46 is 4 tens and 6 ones, so 46 = 40 + 6, not 4 + 6. You can also break a ten: 34 = 30 + 4 = 20 + 14.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "MAB blocks|ten-frames|bundles of sticks")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
