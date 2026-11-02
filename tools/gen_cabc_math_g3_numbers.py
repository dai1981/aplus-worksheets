# -*- coding: utf-8 -*-
"""
BC Grade 3 Math: Numbers to 1000 (BC Mathematics Curriculum, Grade 3 Content: Number concepts to 1000)
  python3 tools/gen_cabc_math_g3_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 3: whole numbers to 1000 (no spaces needed), short sentences for 8-9 year olds, base ten block pictures.
Number words are written the Canadian classroom way, without "and" (three hundred five).
Wrong answers come from real mistakes: writing each spoken part (three hundred five -> 3005),
leaving out a zero (305 -> 35), giving the digit instead of its value (the 4 in 345 is 4),
reading the blocks in the wrong order (234 -> 432), counting pieces instead of values (2 + 3 + 4 = 9),
writing 14 tens as "14" inside the number (2 hundreds, 14 tens, 6 ones -> 2146), fifteen / fifty,
comparing 2- and 3-digit numbers by the first digit only, and skip counting (by 10s, 25s, 50s and 100s) with the wrong step size.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

PL = ["ones", "tens", "hundreds"]
PL1 = ["one", "ten", "hundred"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e, rnd):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    ch = wrong + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, wrong, e, rnd):
    assert 0 <= correct <= 1000, (q, correct)
    assert all(isinstance(w, int) and 0 <= w < 10000 and w != correct for w in wrong), (q, correct, wrong)
    return mcq(q, correct, wrong, e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


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


def digit(n, i):
    return (n // 10 ** i) % 10


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def unit(k, w):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


def hto(h, t, o):
    return "%s, %s and %s" % (plural(h, 2), plural(t, 1), plural(o, 0))


def hto_n(n):
    return hto(digit(n, 2), digit(n, 1), digit(n, 0))


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t
        assert [sum(1 for it in st["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


# ------------------------------------------------------------ number words (Canadian classroom style: no "and")
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words99(n):
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


def words(n):
    if n == 1000:
        return "one thousand"
    h, r = divmod(n, 100)
    if not h:
        return words99(r)
    return ONES[h] + " hundred" + (" " + words99(r) if r else "")


assert words(305) == "three hundred five" and words(640) == "six hundred forty" and words(900) == "nine hundred"


# ------------------------------------------------------------ figures
U = 8                      # base ten blocks: a cube = U, a rod = U x 10U, a flat = 10U x 10U (exact 1 : 10 : 100)
G = 8                      # gap between flats
GG = 22                    # gap between groups
MG = 8


def blocks_svg(h, t, o, labels=False):
    """Base ten blocks: h flats, t rods, o cubes. Flats in one row (up to 3) or two rows; cubes in columns of 5."""
    F = 10 * U
    groups = []

    def grid(x, y, w, hh, cols, rows):
        s = []
        for i in range(1, cols):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x + i * U, y, x + i * U, y + hh, GREEN))
        for i in range(1, rows):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + i * U, x + w, y + i * U, GREEN))
        return s

    fcols = h if h <= 3 else (h + 1) // 2
    frows = 1 if h <= 3 else 2

    def flats(x, y):
        s = []
        for k in range(h):
            fx = x + (k % fcols) * (F + G)
            fy = y + (k // fcols) * (F + G)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (fx, fy, F, F, FILL, GREEN))
            s += grid(fx, fy, F, F, 10, 10)
        return s

    def rods(x, y):
        s = []
        for k in range(t):
            lx = x + k * (U + 5)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (lx, y, U, F, FILL, GREEN))
            s += grid(lx, y, U, F, 1, 10)
        return s

    ccols = (o + 4) // 5

    def cubes(x, y):
        s = []
        for k in range(o):
            mx = x + (k // 5) * (U + 6)
            my = y + (k % 5) * (U + 7)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (mx, my, U, U, CUBE, GREEN))
        return s

    if h:
        groups.append((fcols * F + (fcols - 1) * G, frows * F + (frows - 1) * G, flats, plural(h, 2)))
    if t:
        groups.append((t * U + (t - 1) * 5, F, rods, plural(t, 1)))
    if o:
        groups.append((ccols * U + (ccols - 1) * 6, 5 * U + 4 * 7, cubes, plural(o, 0)))
    lab_w = lambda s: int(len(s) * 8.6) + 6
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * MG + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * MG + body_h + (26 if labels else 0)
    s = []
    x = MG
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, MG + body_h - gh)        # every group sits on the same base line
        if labels:
            s.append(text(x + w / 2, MG + body_h + 20, lab, 15))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base ten blocks")


CW, HEAD, ROW = 104, 34, 50


def chart_svg(n, hi=None):
    """Hundreds / tens / ones chart. hi = place index to colour red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 3 * CW, 2 * y0 + HEAD + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 3 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 3 * CW, HEAD, FILL)]
    for k in range(3):
        i = 2 - k
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append(text(cx, y0 + 23, cap(PL[i]), 15))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 3 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "place value chart showing %d" % n)


def number_line_svg(lo, hi, step, labels, arrow=None, show=None, unit="", jumps=None):
    """Number line lo..hi with a tick every step, numbers under `labels`, a red arrow at `arrow`
    and/or red jump arcs between the values in `jumps`."""
    L, R, Y = 36, 436, 58
    W, Hh = 472, 100

    def X(v):
        return L + (v - lo) * (R - L) / (hi - lo)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, "%d%s" % (v, unit), 15, col=GREEN))
        v += step
    if jumps:
        for a, b in zip(jumps, jumps[1:]):
            xa, xb = X(a), X(b)
            s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.2'/>"
                     % (xa, Y - 4, (xa + xb) / 2, Y - 44, xb, Y - 4, RED))
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>"
                     % (xb - 6, Y - 12, xb + 1, Y - 12, xb, Y - 3, RED))
        s.append("<circle cx='%.1f' cy='%d' r='4' fill='%s'/>" % (X(jumps[0]), Y, RED))
    if arrow is not None:
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    if show:
        s.append(text(min(max(X(arrow), 60), W - 60), Y - 44, show, 15, col=RED))
    top = 18 if show else 0
    body = "".join(s)
    if top:
        body = "<g transform='translate(0 %d)'>%s</g>" % (top, body)
    return svg_wrap(W, Hh + top, body, "number line from %d to %d" % (lo, hi))


def blocks_e(h, t, o):
    n = 100 * h + 10 * t + o
    s = "A flat is 100, a rod is 10 and a small cube is 1. %s make %d." % (cap(hto(h, t, o)), n)
    empty = [PL[i] for i, d in ((1, t), (0, o)) if d == 0]
    if empty:
        s += " There are no %s, so write 0 in the %s place%s." % (" or ".join(empty), " and ".join(empty),
                                                                  "s" if len(empty) > 1 else "")
    return s


# ============================================================ set 1: base ten blocks
def set_blocks(rnd):
    what = []
    for h, t, o in [(2, 3, 4), (1, 5, 2), (3, 2, 6), (2, 8, 5), (4, 1, 7), (1, 7, 9), (3, 4, 1), (5, 6, 3)]:
        n = 100 * h + 10 * t + o
        wrong = [100 * o + 10 * t + h, 100 * h + 10 * o + t, h + t + o]       # read backwards, tens/ones swapped, counted pieces
        e = blocks_e(h, t, o) + " Start with the flats, then the rods, then the small cubes."
        what.append(mcq_n(fig(blocks_svg(h, t, o)) + "What number do the base ten blocks show?", n, wrong, e, rnd))
    how = [
        mcq_n(fig(blocks_svg(3, 5, 2)) + "How many tens are there?", 5, [3, 2, 50],
              "Each rod is 1 ten. There are 5 rods, so there are 5 tens. The number is 352.", rnd),
        mcq_n(fig(blocks_svg(4, 2, 6)) + "How many hundreds are there?", 4, [2, 6, 400],
              "Each flat is 1 hundred. There are 4 flats, so there are 4 hundreds. The number is 426.", rnd),
        mcq_n(fig(blocks_svg(2, 7, 8)) + "How many ones are there?", 8, [2, 7, 17],
              "Each small cube is 1 one. There are 8 cubes, so there are 8 ones. The number is 278.", rnd),
    ]
    match = []
    for h, t, o in [(3, 6, 4), (2, 5, 7), (5, 1, 8)]:
        wrong = [hto(o, t, h), hto(h, o, t), hto(t, h, o)]
        match.append(mcq(fig(blocks_svg(h, t, o)) + "Which matches the blocks?", hto(h, t, o), wrong,
                         "Count each kind: %s, %s, %s. That is %s: %d."
                         % (unit(h, "flat"), unit(t, "rod"), unit(o, "small cube"), hto(h, t, o), 100 * h + 10 * t + o), rnd))
    more = [
        mcq_n(fig(blocks_svg(2, 4, 5)) + "Add 1 more rod. What number is it now?", 255, [246, 345, 235],
              "The blocks show 245. A rod is 10. 245 + 10 = 255. Only the tens digit changes.", rnd),
        mcq_n(fig(blocks_svg(1, 3, 6)) + "Add 1 more flat. What number is it now?", 236, [137, 146, 36],
              "The blocks show 136. A flat is 100. 136 + 100 = 236. Only the hundreds digit changes.", rnd),
        mcq_n(fig(blocks_svg(3, 5, 9)) + "Add 1 more small cube. What number is it now?", 360, [3510, 369, 459],
              "The blocks show 359. Add 1 cube: now there are 10 cubes. Trade 10 cubes for 1 rod. "
              "That is 3 hundreds, 6 tens and 0 ones: 360.", rnd),
    ]
    thousand = mcq_n(fig(blocks_svg(10, 0, 0)) + "There are 10 flats. What number do they show?", 1000,
                     [10, 100, 900],
                     "Each flat is 100. Count by 100s: 100, 200, 300 … 1000. 10 hundreds make 1000.", rnd)
    which = []
    for h, t, o in [(4, 2, 9), (7, 3, 1)]:
        n = 100 * h + 10 * t + o
        which.append(mcq_n("Which number has %s?" % hto(h, t, o), n,
                           [100 * o + 10 * t + h, 100 * h + 10 * o + t, h + t + o],
                           "Write the hundreds digit first, then the tens, then the ones: %d, %d, %d. That is %d."
                           % (h, t, o, n), rnd))
    order = (what[:3] + how[:2] + what[3:5] + match[:2] + how[2:] + what[5:7] + match[2:] + which[:1]
             + what[7:] + more + which[1:] + [thousand])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Base ten blocks: hundreds, tens and ones", "items": order}


# ============================================================ set 2: value of a digit
def value_wrong(n, i):
    d = digit(n, i)
    if i == 2:
        return [d, d * 10, d * 1000]
    if i == 1:
        return [d, d * 100, n % 100]                     # the digit, the wrong place, "read from the 4 on" (45)
    return [d * 10, d * 100, n % 100]


def value_e(n, i, red=False):
    d = digit(n, i)
    v = d * 10 ** i
    s = "The %s%d is in the %s place. It is worth %s = %d." % ("red " if red else "", d, PL[i], plural(d, i), v)
    if i:
        s += " The digit is %d, but its value is %d." % (d, v)
    return s


def zero_e(n):
    empty = [PL[i] for i in (1, 0) if digit(n, i) == 0]
    return ("%s is %s: %d. Write 0 for the empty %s place. The 0 keeps the other digits in the right places."
            % (cap(words(n)), hto_n(n), n, " and ".join(empty)))


def set_value(rnd):
    chart = [mcq_n(fig(chart_svg(n, hi=i)) + "What is the red digit worth?", digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i, True), rnd)
             for n, i in [(345, 1), (582, 2), (716, 0), (493, 1), (268, 2)]]
    plain = [mcq_n("What is the value of the %d in %d?" % (digit(n, i), n), digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i), rnd)
             for n, i in [(473, 1), (619, 2), (538, 0), (924, 1)]]
    place = []
    for n, i in [(736, 2), (418, 1)]:
        d = digit(n, i)
        wrong = [digit(n, x) for x in range(2, -1, -1) if x != i] + [d * 10 ** i]
        place.append(mcq("In %d, which digit is in the %s place?" % (n, PL[i]), d, wrong,
                         "%d is %s. The %s digit is %d. (Its value is %d.)" % (n, hto_n(n), PL[i], d, d * 10 ** i), rnd))
    has = []
    for d, i, ans, wrong in [(6, 1, 263, [623, 236, 632]), (8, 2, 815, [158, 581, 185]), (3, 0, 473, [437, 347, 734])]:
        assert digit(ans, i) == d and all(digit(w, i) != d for w in wrong)
        has.append(mcq_n("Which number has %s %d in the %s place?" % ("an" if d == 8 else "a", d, PL[i]), ans, wrong,
                         "%d is %s. The %d is in the %s place." % (ans, hto_n(ans), d, PL[i]), rnd))
    tower = mcq_n("A BC Ferries ship has room for 553 people. What is the value of the 5 in the tens place?", 50,
                  [5, 500, 53],
                  "553 is 5 hundreds, 5 tens and 3 ones. The 5 in the tens place is worth 50. "
                  "The other 5 is in the hundreds place and is worth 500.", rnd)
    wr = []
    for n, wrong in [(305, [35, 3005, 350]), (406, [46, 4006, 460]), (870, [87, 807, 8070])]:
        wr.append(mcq_n("Write “%s” as a number." % words(n), n, wrong, zero_e(n), rnd))
    cnt = mcq_n(fig(chart_svg(507)) + "How many tens are in 507?", 0, [5, 7, 50],
                "507 is 5 hundreds, 0 tens and 7 ones. The 0 shows there are no tens.", rnd)
    has0 = mcq_n("Which number has 0 tens?", 306, [360, 630, 36],
                 "306 is 3 hundreds, 0 tens and 6 ones. 360 and 630 have 0 ones, and 36 has 3 tens.", rnd)
    order = (chart[:2] + plain[:1] + place[:1] + wr[:1] + chart[2:3] + has[:1] + plain[1:2] + [cnt] + chart[3:4]
             + wr[1:2] + place[1:] + has[1:2] + plain[2:3] + [has0] + chart[4:] + wr[2:] + has[2:] + plain[3:]
             + [tower])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "The value of each digit", "items": order}


# ============================================================ set 3: expanded form and decomposing
def set_decompose(rnd):
    std = [
        mcq("What is 346 in expanded form?", "300 + 40 + 6",
            ["3 + 4 + 6", "300 + 4 + 6", "300 + 40 + 60"],
            "346 is 3 hundreds, 4 tens and 6 ones. That is 300 + 40 + 6.", rnd),
        mcq("What is 572 in expanded form?", "500 + 70 + 2",
            ["5 + 7 + 2", "500 + 7 + 2", "50 + 70 + 2"],
            "572 is 5 hundreds, 7 tens and 2 ones. That is 500 + 70 + 2.", rnd),
        mcq("What is 508 in expanded form?", "500 + 8", ["50 + 8", "500 + 80", "5 + 8"],
            "508 is 5 hundreds, 0 tens and 8 ones. 0 tens adds nothing. So 508 = 500 + 8.", rnd),
        mcq("What is 690 in expanded form?", "600 + 90", ["600 + 9", "60 + 90", "6 + 9"],
            "690 is 6 hundreds, 9 tens and 0 ones. 9 tens = 90. So 690 = 600 + 90.", rnd),
    ]
    miss = [
        mcq_n("300 + ☐ + 6 = 346. What number goes in the box?", 40, [4, 400, 46],
              "346 is 3 hundreds, 4 tens and 6 ones. 4 tens = 40.", rnd),
        mcq_n("☐ + 20 + 9 = 829. What number goes in the box?", 800, [8, 80, 829],
              "829 is 8 hundreds, 2 tens and 9 ones. 8 hundreds = 800.", rnd),
        mcq_n("400 + ☐ = 407. What number goes in the box?", 7, [70, 47, 0],
              "407 is 4 hundreds, 0 tens and 7 ones. 400 + 7 = 407.", rnd),
        mcq_n("600 + 30 + ☐ = 635. What number goes in the box?", 5, [50, 35, 500],
              "635 is 6 hundreds, 3 tens and 5 ones. The ones part is 5.", rnd),
    ]
    exp = []
    for a, b, wrong in [(600, 7, [67, 6007, 670]), (400, 90, [49, 409, 4090])]:
        n = a + b
        exp.append(mcq_n("What number is %d + %d?" % (a, b), n, wrong,
                         "%d + %d is %s: %d. Do not write %d and then %d. The answer has only 3 digits."
                         % (a, b, hto_n(n), n, a, b), rnd))
    rd = [
        mcq("How do you write 708 in words?", words(708), ["seventy-eight", words(780), words(807)],
            "708 is 7 hundreds, 0 tens and 8 ones. Say the hundreds, then the ones: seven hundred eight.", rnd),
        mcq("How do you write 350 in words?", words(350), ["thirty-five", words(305), words(315)],
            "350 is 3 hundreds, 5 tens and 0 ones. 5 tens is fifty, not fifteen: three hundred fifty.", rnd),
    ]
    blk = [
        mcq_n(fig(blocks_svg(2, 14, 6)) + "What number do the base ten blocks show?", 346, [2146, 246, 336],
              "There are 14 rods. 10 rods make 1 hundred, so 14 tens = 1 hundred and 4 tens. "
              "200 + 140 + 6 = 346.", rnd),
        mcq_n(fig(blocks_svg(3, 0, 15)) + "What number do the base ten blocks show?", 315, [3015, 305, 350],
              "15 small cubes are 1 ten and 5 ones. 300 + 15 = 315.", rnd),
    ]
    regroup = [
        mcq_n("346 = 2 hundreds, ☐ tens and 6 ones. What number goes in the box?", 14, [4, 34, 140],
              "Take 1 hundred from 3 hundreds and make it 10 tens. Now there are 2 hundreds and 10 + 4 = 14 tens. "
              "Check: 200 + 140 + 6 = 346.", rnd),
        mcq_n("523 = 4 hundreds, 12 tens and ☐ ones. What number goes in the box?", 3, [13, 23, 30],
              "4 hundreds = 400 and 12 tens = 120. 400 + 120 = 520. 523 − 520 = 3. So there are 3 ones.", rnd),
        mcq("Which is another way to make 346?", "2 hundreds, 14 tens and 6 ones",
            ["2 hundreds, 4 tens and 6 ones", "3 hundreds, 14 tens and 6 ones", "2 hundreds, 14 tens and 16 ones"],
            "2 hundreds = 200 and 14 tens = 140. 200 + 140 + 6 = 346. "
            "(The others make 246, 446 and 356.)", rnd),
        mcq("Which is <b>not</b> equal to 250?", "2 hundreds and 5 ones",
            ["25 tens", "1 hundred and 15 tens", "2 hundreds and 5 tens"],
            "2 hundreds and 5 ones = 205, not 250. 25 tens = 250, 100 + 150 = 250 and 200 + 50 = 250.", rnd),
        mcq_n("430 = ☐ tens. What number goes in the box?", 43, [3, 4, 430],
              "430 = 4 hundreds and 3 tens. 4 hundreds = 40 tens. 40 + 3 = 43 tens. Check: 43 × 10 = 430.", rnd),
        mcq_n("357 = 200 + ☐ + 7. What number goes in the box?", 150, [50, 100, 15],
              "357 = 300 + 50 + 7. Only 200 is used, so 100 moves to the tens part: 100 + 50 = 150. "
              "Check: 200 + 150 + 7 = 357.", rnd),
    ]
    for v, w in [(200 + 140 + 6, 346), (400 + 120 + 3, 523), (300 + 140 + 6, 446), (200 + 140 + 16, 356),
                 (200 + 5, 205), (100 + 150, 250), (43 * 10, 430), (200 + 150 + 7, 357), (300 + 15, 315)]:
        assert v == w
    order = (std[:2] + miss[:2] + rd[:1] + std[2:] + exp[:1] + miss[2:] + rd[1:] + exp[1:]
             + blk[:1] + regroup[:1] + blk[1:] + regroup[1:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Expanded form and decomposing numbers", "items": order}


# ============================================================ set 4: compare and order
def first_diff(a, b):
    for i in (2, 1, 0):
        if digit(a, i) != digit(b, i):
            return i


def compare_e(big, small):
    if len(str(big)) != len(str(small)):
        return ("%d has %d digits and %d has only %d. So %d &gt; %d."
                % (big, len(str(big)), small, len(str(small)), big, small))
    i = first_diff(big, small)
    lead = "Start with the hundreds" if i == 2 else "The %s are the same, so look at the %s" % (
        " and ".join(PL[x] for x in (2, 1) if x > i), PL[i])
    return ("Compare from the left. %s: %s is more than %s. So %d &gt; %d."
            % (lead, plural(digit(big, i), i), plural(digit(small, i), i), big, small))


def set_compare(rnd):
    cmp_ = []
    for x, y in [(452, 425), (309, 390), (98, 102), (670, 607), (1000, 999)]:
        lt = "&lt;" if x < y else "&gt;"
        gt = "&gt;" if x < y else "&lt;"
        e = compare_e(max(x, y), min(x, y))
        if x == 98:
            e += " Do not just look at the first digit: count the digits first."
        cmp_.append(mcq("Which is true?", "%d %s %d" % (x, lt, y),
                        ["%d %s %d" % (x, gt, y), "%d = %d" % (x, y), "%d %s %d" % (y, lt, x)], e, rnd))
    big = [
        mcq_n("Which number is the greatest?", 543, [534, 354, 435],
              compare_e(543, 534) + " 543 is the greatest.", rnd),
        mcq_n("Which number is the least?", 86, [608, 680, 806],
              "86 is the only number with 2 digits, so it is the least, even though 8 is a big digit.", rnd),
        mcq_n("Which number is the greatest?", 1000, [999, 990, 909],
              "1000 has 4 digits. 999, 990 and 909 have only 3. 1000 is 1 more than 999, so 1000 is the greatest.", rnd),
        mcq_n("Which number is the least?", 702, [720, 712, 727],
              "All have 7 hundreds. Tens: 702 has 0 tens, which is the fewest. So 702 is the least.", rnd),
    ]
    order = [
        mcq("Put 271, 217 and 712 in order from least to greatest.", "217, 271, 712",
            ["271, 217, 712", "712, 271, 217", "217, 712, 271"],
            "Hundreds first: 712 has 7 hundreds, so it is the greatest. 217 and 271 both have 2 hundreds. "
            "Tens: 1 ten &lt; 7 tens, so 217 &lt; 271. Order: 217, 271, 712.", rnd),
        mcq("Put 450, 405 and 45 in order from least to greatest.", "45, 405, 450",
            ["405, 45, 450", "45, 450, 405", "450, 405, 45"],
            "45 has only 2 digits, so it is the least. 405 and 450 both have 4 hundreds. "
            "Tens: 0 tens &lt; 5 tens, so 405 &lt; 450. Order: 45, 405, 450.", rnd),
        mcq("Put 836, 863 and 638 in order from greatest to least.", "863, 836, 638",
            ["638, 836, 863", "836, 863, 638", "863, 638, 836"],
            "638 has only 6 hundreds, so it is the least. 836 and 863 both have 8 hundreds. "
            "Tens: 6 tens &gt; 3 tens, so 863 &gt; 836. Order: 863, 836, 638.", rnd),
        mcq("Put 529, 592, 925 and 259 in order from least to greatest.", "259, 529, 592, 925",
            ["259, 592, 529, 925", "925, 592, 529, 259", "529, 592, 259, 925"],
            "Hundreds: 2 &lt; 5 &lt; 9, so 259 is the least and 925 is the greatest. "
            "529 and 592 both have 5 hundreds: 2 tens &lt; 9 tens. Order: 259, 529, 592, 925.", rnd),
        mcq("Put 1000, 100, 910 and 190 in order from greatest to least.", "1000, 910, 190, 100",
            ["910, 190, 1000, 100", "100, 190, 910, 1000", "1000, 190, 910, 100"],
            "1000 has 4 digits, so it is the greatest. Then compare the hundreds: 9 &gt; 1, so 910 comes next. "
            "190 &gt; 100 because 9 tens &gt; 0 tens. Order: 1000, 910, 190, 100.", rnd),
    ]
    dig = [
        mcq_n("Use the digits 4, 7 and 2 once each. What is the greatest number you can make?", 742,
              [724, 247, 472],
              "Put the biggest digit in the hundreds place, then the next biggest: 7, 4, 2. That is 742.", rnd),
        mcq_n("Use the digits 5, 0 and 3 once each. What is the least 3-digit number you can make?", 305,
              [35, 350, 503],
              "A 3-digit number cannot start with 0. Put the smallest other digit first: 3. Then 0, then 5: 305. "
              "(035 is just 35, which has only 2 digits.)", rnd),
        mcq_n("Use the digits 8, 0 and 6 once each. What is the greatest number you can make?", 860,
              [806, 680, 608],
              "Biggest digit first: 8. Then 6. The 0 goes last, in the ones place: 860.", rnd),
    ]
    between = [
        mcq_n("Which number is between 450 and 500?", 476, [445, 504, 540],
              "A number between 450 and 500 is greater than 450 and less than 500. 476 has 4 hundreds and 7 tens, "
              "so it fits. 445 is too small. 504 and 540 are too big.", rnd),
        mcq_n("Which number is between 700 and 750?", 728, [782, 770, 699],
              "728 has 7 hundreds and 2 tens, so it is between 700 and 750. 782 and 770 are more than 750. "
              "699 is less than 700.", rnd),
    ]
    less = mcq_n("What number is 10 less than 600?", 590, [500, 610, 690],
                 "10 less than 600: count back one ten. 600 is 60 tens, and 1 ten less is 59 tens = 590. "
                 "500 is 100 less, and 610 is 10 more.", rnd)
    for a, b in [(217, 271), (271, 712), (45, 405), (405, 450), (638, 836), (836, 863), (259, 529), (529, 592),
                 (592, 925), (100, 190), (190, 910), (910, 1000), (450, 476), (476, 500), (700, 728), (728, 750)]:
        assert a < b
    order = (cmp_[:2] + big[:2] + order[:1] + cmp_[2:3] + dig[:1] + between[:1] + order[1:2] + cmp_[3:4]
             + big[2:3] + dig[1:2] + order[2:3] + [less] + cmp_[4:] + big[3:] + between[1:] + order[3:4]
             + dig[2:] + order[4:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers to 1000", "items": order}


# ============================================================ set 5: count by 10s, 25s, 50s, 100s, number lines, word problems
def set_count(rnd, P):
    seq = [
        mcq_n("Count by 10s: 570, 580, 590, ☐. What comes next?", 600, [5100, 591, 690],
              "Count by 10s: each number is 10 more. 59 tens + 1 ten = 60 tens = 600. "
              "10 tens make a new hundred, so it is not 5100.", rnd),
        mcq_n("Count by 25s: 25, 50, 75, ☐. What comes next?", 100, [80, 85, 125],
              "Count by 25s, like counting quarters: 25, 50, 75, 100. 75 + 25 = 100. "
              "(80 is counting by 5s and 85 is counting by 10s.)", rnd),
        mcq_n("Count by 50s: 350, 400, 450, ☐. What comes next?", 500, [460, 550, 455],
              "Count by 50s: each number is 50 more. 450 + 50 = 500. (460 is counting by 10s.)", rnd),
        mcq_n("Count by 100s: 230, 330, 430, ☐. What comes next?", 530, [440, 431, 630],
              "Count by 100s: only the hundreds digit changes. 4 hundreds → 5 hundreds: 530.", rnd),
        mcq_n("Count back by 25s: 300, 275, 250, ☐. What comes next?", 225, [200, 240, 245],
              "Count back by 25s: each number is 25 less. 250 − 25 = 225. "
              "(200 is counting back by 50s and 240 is counting back by 10s.)", rnd),
    ]
    nl = [
        mcq_n(fig(number_line_svg(0, 1000, 100, [0, 500, 1000], 800)) + "What number does the arrow point to?",
              800, [80, 700, 900],
              "From 0 to 1000 there are 10 jumps, so each mark is 100. The arrow is 3 marks after 500: "
              "600, 700, 800.", rnd),
        mcq_n(fig(number_line_svg(0, 1000, 50, [0, 500, 1000], 650)) + "What number does the arrow point to?",
              650, [800, 530, 700],
              "From 0 to 500 there are 10 jumps, so each mark is 50, not 100. "
              "The arrow is 3 marks after 500: 550, 600, 650.", rnd),
    ]
    name, he, his = P.next()
    nl.append(mcq_n(fig(number_line_svg(0, 200, 25, [0, 100, 200], jumps=[0, 25, 50, 75, 100, 125]))
                    + "%s counts by 25s. %s starts at 0 and makes 5 jumps. Where does %s land?" % (name, cap(he), he),
                    125, [5, 100, 150],
                    "Each jump is 25: 25, 50, 75, 100, 125. After 5 jumps %s lands on 125." % name, rnd))
    nl.append(mcq_n(fig(number_line_svg(300, 600, 50, [300, 400, 500, 600], jumps=[300, 350, 400, 450, 500]))
                    + "The jumps start at 300. Each jump is 50. Where does the 4th jump land?",
                    500, [450, 340, 700],
                    "Count by 50s from 300: 350, 400, 450, 500. The 4th jump lands on 500.", rnd))
    nl.append(mcq_n(fig(number_line_svg(400, 500, 10, [400, 450, 500], 470)) + "What number does the arrow point to?",
                    470, [407, 460, 480],
                    "From 400 to 450 there are 5 jumps, so each mark is 10, not 1. "
                    "The arrow is 2 marks after 450: 460, 470.", rnd))

    wp = []
    name, she, her = P.next()
    wp.append(mcq_n("Canada geese fly in groups of 50. %s counts 6 groups. How many geese is that?" % name, 300,
                    [56, 600, 250],
                    "Count by 50s: 50, 100, 150, 200, 250, 300. 6 groups of 50 = 300 geese.", rnd))
    name, she, her = P.next()
    wp.append(mcq("%s counts money from the Terry Fox Run: seven $10 bills and four loonies. "
                  "How much money is that?" % name,
                  "$74", ["$11", "$47", "$704"],
                  "Seven $10 bills = $70. A loonie is $1, so four loonies = $4. $70 + $4 = $74. "
                  "(Do not add 7 + 4, and do not write $704.)", rnd))
    wp.append(mcq_n("The hockey arena has “eight hundred six” seats. Write the number of seats.", 806,
                    [86, 8006, 860],
                    "Eight hundred six is 8 hundreds, 0 tens and 6 ones: 806. Write 0 for the empty tens place.", rnd))
    wp.append(mcq("Two orchards in the Okanagan picked cherries. The Lee orchard picked 450 kg. "
                  "The Singh orchard picked 540 kg. Which orchard picked more?",
                  "The Singh orchard", ["The Lee orchard", "They picked the same", "You cannot tell"],
                  "Compare the hundreds: 5 hundreds &gt; 4 hundreds. So 540 &gt; 450. The Singh orchard picked more.", rnd))
    wp.append(mcq_n("Pencils come in boxes of 10. The school buys 36 boxes. How many pencils is that?", 360,
                    [36, 46, 306],
                    "36 tens = 3 hundreds and 6 tens = 360. 30 boxes is 300 pencils. "
                    "6 more boxes is 60. 300 + 60 = 360.", rnd))
    name, she, her = P.next()
    wp.append(mcq("%s has 6 quarters in %s piggy bank. How much money is that?" % (name, her), "$1.50",
                  ["$6.00", "$0.60", "$1.25"],
                  "A quarter is 25¢. Count by 25s: 25, 50, 75, 100, 125, 150. 150¢ = $1.50. "
                  "(Each quarter is not $1, and it is not 10¢ like a dime.)", rnd))
    wp.append(mcq("Three schools go on a field trip to Stanley Park. Cedar Hill sends 316 students, Lakeview "
                  "sends 361 and Eagle Ridge sends 136. Which list goes from least to greatest?", "136, 316, 361",
                  ["316, 136, 361", "361, 316, 136", "136, 361, 316"],
                  "136 has only 1 hundred, so it is the least. 316 and 361 both have 3 hundreds. "
                  "Tens: 1 ten &lt; 6 tens. Order: 136, 316, 361.", rnd))
    name, he, his = P.next()
    wp.append(mcq_n("%s’s mystery number is between 600 and 700. It has 5 tens and 0 ones. What is it?" % name,
                    650, [605, 560, 750],
                    "Between 600 and 700 means 6 hundreds. Then 5 tens and 0 ones: 650.", rnd))
    name, she, her = P.next()
    wp.append(mcq_n("For the food drive, %s stacks cans in groups of 50. There are 9 groups. "
                    "How many cans is that?" % name, 450, [59, 900, 400],
                    "Count by 50s: 50, 100, 150, 200, 250, 300, 350, 400, 450. 9 groups of 50 = 450 cans. "
                    "(Two groups of 50 make 100, so 8 groups make 400, and 1 more group makes 450.)", rnd))
    wp.append(mcq_n("For Canada Day, a town in the Okanagan buys flags in boxes of 100. It buys 10 boxes. "
                    "How many flags is that?",
                    1000, [110, 100, 10],
                    "Count by 100s: 100, 200, 300 … 1000. 10 hundreds make 1000 flags. "
                    "(110 is 100 + 10, but the town has 10 boxes of 100.)", rnd))
    for v, w in [(50 * 6, 300), (70 + 4, 74), (36 * 10, 360), (25 * 6, 150), (50 * 9, 450), (10 * 100, 1000),
                 (75 + 25, 100), (250 - 25, 225), (590 + 10, 600), (25 * 5, 125), (450 + 20, 470)]:
        assert v == w
    order = seq[:3] + nl[:2] + seq[3:] + nl[2:] + wp
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Count by 10s, 25s, 50s and 100s, number lines and word problems", "items": order}


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
        "<h2>Hundreds, tens and ones</h2>"
        "<p>A 3-digit number has three places: <b>hundreds</b>, <b>tens</b> and <b>ones</b>. "
        "10 ones make 1 ten. 10 tens make 1 hundred. 10 hundreds make 1000.</p>"
        "<figure class='sn-fig'>" + blocks_svg(3, 4, 6, labels=True) +
        "<figcaption>Base ten blocks for 346. A flat is 100, a rod is 10 and a small cube is 1.</figcaption></figure>"
        "<h2>The value of a digit</h2>"
        "<p>The place tells you what a digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(345, hi=1) +
        "<figcaption>In 345 the 4 is in the tens place. Its value is 4 tens, or 40.</figcaption></figure>"
        "<p>If a place is empty, write <b>0</b> there. The 0 keeps the other digits in the right places.</p>" +
        ex("Write the number", "Write “three hundred five” as a number.",
           "3 hundreds, 0 tens, 5 ones. Write 3, 0, 5.", "305 (not 35 or 3005)") +
        "<h2>Expanded form and decomposing</h2>"
        "<p><b>Expanded form</b> shows the value of each digit: 346 = 300 + 40 + 6. "
        "You can also decompose a number another way. Trade 1 hundred for 10 tens.</p>"
        "<figure class='sn-fig'>" + blocks_svg(2, 14, 6, labels=True) +
        "<figcaption>2 hundreds, 14 tens and 6 ones is also 346: 200 + 140 + 6 = 346.</figcaption></figure>" +
        ex("Decompose", "Decompose 346 in two ways.",
           "3 hundreds, 4 tens and 6 ones. Or 2 hundreds, 14 tens and 6 ones.",
           "300 + 40 + 6 = 200 + 140 + 6") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 3-digit number is greater than a 2-digit number. "
        "If both have 3 digits, compare the hundreds, then the tens, then the ones.</p>" +
        ex("Compare", "452 ☐ 425", "Hundreds: 4 = 4. Tens: 5 tens &gt; 2 tens.", "452 &gt; 425") +
        "<p>&gt; means “is greater than”. &lt; means “is less than”. The open side faces the greater number.</p>"
        "<h2>Count by 10s, 25s, 50s and 100s</h2>"
        "<p>Counting by 10s: 570, 580, 590, 600. After 9 tens comes a new hundred. "
        "Counting by 25s is like counting quarters: 25, 50, 75, 100. Four 25s make 100. "
        "Counting by 50s: 50, 100, 150, 200 … Two 50s make 100. "
        "Counting by 100s changes only the hundreds digit: 230, 330, 430.</p>"
        "<figure class='sn-fig'>" + number_line_svg(0, 1000, 50, [0, 500, 1000], 650, show="650") +
        "<figcaption>From 0 to 500 there are 10 marks, so each mark is 50. The arrow is 3 marks after 500: 650.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing each part you hear (three hundred five = 3005)", "A number in the hundreds has 3 digits: 305"],
            ["Leaving out the zero (305 = 35)", "Write 0 for the empty tens place: 305"],
            ["Reading the digit, not its value (the 4 in 345 is 4)", "The 4 is in the tens place: 40"],
            ["Writing 14 tens inside the number (2 hundreds, 14 tens, 6 ones = 2146)",
             "14 tens = 140, so 200 + 140 + 6 = 346"],
            ["Comparing the first digits only (98 &gt; 102)", "Count the digits first: 102 &gt; 98"],
            ["Thinking every mark on a number line is 1 or 100", "Work out the jump first: 0 to 500 in 10 jumps means 50 each"],
            ["Counting by 10s past a hundred (590, 5100)", "10 tens make a new hundred: 590, 600"],
        ])
    )


FAQ = [
    {"q": "What number skills are in the Grade 3 BC math curriculum?",
     "a": "Grade 3 students in BC work with number concepts to 1000: place value with hundreds, tens and ones, "
          "comparing and ordering numbers, and skip counting by 10s, 25s, 50s and 100s."},
    {"q": "What are base ten blocks?",
     "a": "Base ten blocks are place value materials used in many BC classrooms: a small cube is 1, a rod is 10 and a flat is 100. "
          "Ten flats make 1000, so children can see what each digit is worth."},
    {"q": "Why does my child write 35 for three hundred five?",
     "a": "Leaving out the zero is a common place value mistake. Ask how many hundreds, tens and ones there are, "
          "and remind them to write 0 when there are no tens: 305."},
    {"q": "Do Grade 3 students in BC write the FSA?",
     "a": "No. In BC the Foundation Skills Assessment (FSA) is written in Grades 4 and 7. "
          "Strong place value in Grade 3 is a good base for the numeracy part."},
]


def mark_large(u, pattern):
    """Tag wide pictures (base ten blocks, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(53801)
    P = People(random.Random(538011))
    sets = [set_blocks(rnd), set_value(rnd), set_decompose(rnd), set_compare(rnd), set_count(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "numbers-to-1000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 1000: Place Value, Comparing and Skip Counting",
        "seo_title": "Grade 3 Numbers to 1000 Math Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Numbers to 1000",
        "domain": "Number",
        "standard_code": "Grade 3: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Number concepts to 1000",
        "meta_desc": "Free Grade 3 math worksheets on numbers to 1000: base ten blocks, the value of each digit, expanded form, comparing and ordering, and counting by 10s, 25s, 50s and 100s on number lines. 100 questions with an answer key, following the BC curriculum.",
        "key_big": "The place of a digit tells you its value. The 4 in 345 is worth 40.",
        "key_sub": "Write 0 for an empty place: three hundred five is 305, not 35 or 3005. 346 is 300 + 40 + 6, or 2 hundreds, 14 tens and 6 ones.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(base ten blocks|place value chart|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
