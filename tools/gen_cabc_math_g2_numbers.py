# -*- coding: utf-8 -*-
"""
BC Grade 2 Math: Numbers to 100 (BC Mathematics Curriculum, Grade 2 Content: Number concepts to 100)
  python3 tools/gen_cabc_math_g2_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 2: whole numbers to 100, very short sentences for 7-8 year olds, base ten blocks, ten frames,
coins (nickels and dimes), hundred chart pieces and number lines.
Wrong answers come from real mistakes: reversing the digits (47 / 74), giving the digit instead of its value
(the 4 in 47 is 4), counting the pieces instead of their values (4 rods and 7 cubes = 11),
writing each spoken part (sixty-three -> 603), sixteen / sixty, comparing by the ones digit,
counting by 1s instead of skipping, counting the marks on a number line instead of their value,
and moving across instead of down on a hundred chart.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
NICKEL = "#d5d8dc"
FONT = "Arial, Helvetica, sans-serif"

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
    assert 0 <= correct <= 100, (q, correct)
    assert all(isinstance(w, int) and 0 <= w < 1000 and w != correct for w in wrong), (q, correct, wrong)
    return mcq(q, correct, wrong, e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def cap(s):
    return s[0].upper() + s[1:]


def digit(n, i):
    return (n // 10 ** i) % 10


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def to_n(n):
    return "%s and %s" % (plural(digit(n, 1), 1), plural(digit(n, 0), 0))


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


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    if n == 100:
        return "one hundred"
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


assert words(63) == "sixty-three" and words(70) == "seventy" and words(16) == "sixteen"


# ------------------------------------------------------------ figures
U = 8                      # base ten blocks: a cube = U, a rod = U x 10U (exact 1 : 10)
GG = 22
MG = 8


def blocks_svg(t, o, labels=False):
    """Base ten blocks: t rods and o small cubes (cubes in columns of 5)."""
    F = 10 * U
    groups = []

    def rods(x, y):
        s = []
        for k in range(t):
            lx = x + k * (U + 5)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (lx, y, U, F, FILL, GREEN))
            for i in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                         % (lx, y + i * U, lx + U, y + i * U, GREEN))
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
        s += draw(x + (w - gw) // 2, MG + body_h - gh)
        if labels:
            s.append(text(x + w / 2, MG + body_h + 20, lab, 15))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base ten blocks")


CW, HEAD, ROW = 96, 34, 50


def chart_svg(n, hi=None):
    """Tens / ones chart. hi = place index to colour red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 2 * CW, 2 * y0 + HEAD + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 2 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 2 * CW, HEAD, FILL)]
    for k in range(2):
        i = 1 - k
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append(text(cx, y0 + 23, cap(PL[i]), 15))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 2 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "tens and ones chart showing %d" % n)


def number_line_svg(lo, hi, step, labels, arrow=None):
    """Number line lo..hi with a tick every step, numbers under `labels`, a red arrow at `arrow`."""
    L, R, Y = 30, 430, 46
    W, Hh = 460, 86

    def X(v):
        return L + (v - lo) * (R - L) / (hi - lo)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, "%d" % v, 15, col=GREEN))
        v += step
    if arrow is not None:
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    return svg_wrap(W, Hh, "".join(s), "number line from %d to %d" % (lo, hi))


CWID, CHT = 48, 34


def hchart_svg(tl, nrows, ncols, target, hide=()):
    """A piece of the hundred chart. tl = top-left number. target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the hundred chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 100
    m = 4
    W, H = 2 * m + ncols * CWID, 2 * m + nrows * CHT
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CWID, m + r * CHT
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CWID, CHT, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CWID / 2, y + 23, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CWID / 2, y + 23, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "hundred chart piece")


def groups_svg(k, size):
    """k boxes, each holding `size` dots (size 2, 5 or 10). Size 10 is drawn as a full ten frame."""
    R = 5.5
    P = 15                                    # dot pitch
    cols = {2: 1, 5: 1, 10: 2}[size]
    rows = {2: 2, 5: 5, 10: 5}[size]
    if size == 10:
        cols, rows = 5, 2
    bw, bh = cols * P + 8, rows * P + 8
    gap = 8
    W = 12 + k * bw + (k - 1) * gap
    H = bh + 12
    s = []
    for g in range(k):
        bx = 6 + g * (bw + gap)
        s.append("<rect x='%d' y='6' width='%d' height='%d' rx='4' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                 % (bx, bw, bh, GREEN))
        if size == 10:
            for c in range(1, cols):
                s.append("<line x1='%.1f' y1='6' x2='%.1f' y2='%d' stroke='%s' stroke-width='0.8'/>"
                         % (bx + 4 + c * P, bx + 4 + c * P, 6 + bh, GREEN))
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='0.8'/>"
                     % (bx, 10 + P, bx + bw, 10 + P, GREEN))
        for d in range(size):
            c, r = (d % cols, d // cols)
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                     % (bx + 4 + c * P + P / 2, 10 + r * P + P / 2, R, RED if size == 10 else GREEN))
    return svg_wrap(W, H, "".join(s), "groups of %d dots" % size)


def coins_svg(k, value):
    """A row of k coins (5 = nickel, 10 = dime)."""
    r = 17 if value == 5 else 15
    gap = 6
    W = 12 + k * 2 * r + (k - 1) * gap
    H = 2 * r + 12
    s = []
    for i in range(k):
        cx = 6 + r + i * (2 * r + gap)
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='#7f8c8d' stroke-width='1.6'/>"
                 % (cx, 6 + r, r, NICKEL))
        s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#95a5a6' stroke-width='0.8'/>"
                 % (cx, 6 + r, r - 3))
        s.append(text(cx, 6 + r + 5, "%d¢" % value, 14))
    return svg_wrap(W, H, "".join(s), "coins %d cents each" % value)


def blocks_e(t, o):
    n = 10 * t + o
    s = "A rod is 10 and a small cube is 1. %s make %d." % (cap(to_n(n)), n)
    return s


# ============================================================ set 1: base ten blocks
def set_blocks(rnd):
    what = []
    for t, o, wrong, extra in [
            (4, 7, [74, 11, 407], "Write the tens digit first: 47, not 74."),
            (3, 5, [53, 8, 305], "Count the rods by 10s: 10, 20, 30. Then count on 5: 35."),
            (6, 0, [6, 600, 70], "Count the rods by 10s: 10, 20, 30, 40, 50, 60. No cubes means 0 ones."),
            (2, 9, [92, 11, 209], "Count the rods by 10s: 10, 20. Then count on 9 ones: 29."),
            (5, 3, [35, 8, 503], "Count the rods by 10s to 50. Then count on 3: 51, 52, 53."),
            (7, 6, [67, 13, 706], "Count the rods by 10s to 70. Then count on 6 ones: 76."),
            (8, 1, [18, 9, 801], "8 tens is eighty. 81 is eighty-one, not eighteen (18)."),
            (9, 4, [49, 13, 904], "Count the rods by 10s to 90. Then count on 4 ones: 94."),
            (1, 6, [61, 7, 106], "This is sixteen. Sixty-one (61) is 6 tens and 1 one.")]:
        n = 10 * t + o
        assert n not in wrong and digit(n, 1) == t and digit(n, 0) == o
        what.append(mcq_n(fig(blocks_svg(t, o)) + "What number do the blocks show?", n, wrong,
                          blocks_e(t, o) + " " + extra, rnd))
    how = [
        mcq_n(fig(blocks_svg(5, 8)) + "How many tens are there?", 5, [8, 50, 58],
              "Each rod is 1 ten. There are 5 rods, so there are 5 tens. The number is 58.", rnd),
        mcq_n(fig(blocks_svg(3, 9)) + "How many ones are there?", 9, [3, 90, 39],
              "Each small cube is 1 one. There are 9 cubes, so there are 9 ones. The number is 39.", rnd),
        mcq_n(fig(blocks_svg(7, 0)) + "How many ones are there?", 0, [7, 70, 1],
              "There are no small cubes, so there are 0 ones. The number is 70.", rnd),
    ]
    match = [
        mcq(fig(blocks_svg(4, 2)) + "Which matches the blocks?", "4 tens and 2 ones",
            ["2 tens and 4 ones", "4 tens and 4 ones", "6 ones"],
            "There are 4 rods and 2 small cubes. That is 4 tens and 2 ones: 42.", rnd),
        mcq(fig(blocks_svg(2, 5)) + "Which matches the blocks?", "2 tens and 5 ones",
            ["5 tens and 2 ones", "2 tens and 2 ones", "7 ones"],
            "There are 2 rods and 5 small cubes. That is 2 tens and 5 ones: 25.", rnd),
    ]
    more = [
        mcq_n(fig(blocks_svg(3, 6)) + "Add 1 more rod. What number is it now?", 46, [37, 26, 56],
              "The blocks show 36. A rod is 10. 36 + 10 = 46. Only the tens digit changes.", rnd),
        mcq_n(fig(blocks_svg(5, 9)) + "Add 1 more small cube. What number is it now?", 60, [510, 69, 50],
              "The blocks show 59. Add 1 cube: now there are 10 cubes. Trade 10 cubes for 1 rod. "
              "That is 6 tens and 0 ones: 60.", rnd),
    ]
    trade = [
        mcq_n(fig(blocks_svg(3, 14)) + "What number do the blocks show?", 44, [314, 17, 34],
              "14 small cubes are 1 ten and 4 ones. 3 tens + 1 ten = 4 tens. So the number is 44. "
              "Check: 30 + 14 = 44.", rnd),
        mcq_n(fig(blocks_svg(10, 0)) + "There are 10 rods. What number do they show?", 100, [10, 90, 110],
              "Each rod is 10. Count by 10s: 10, 20, 30 … 100. 10 tens make 1 hundred.", rnd),
    ]
    which = [
        mcq_n("Which number has 6 tens and 3 ones?", 63, [36, 9, 603],
              "Write the tens digit first, then the ones: 6, 3. That is 63.", rnd),
        mcq_n("Which number has 5 tens and 0 ones?", 50, [5, 500, 15],
              "5 tens is 50. There are no ones, so write 0 in the ones place: 50 (fifty, not fifteen).", rnd),
    ]
    order = (what[:2] + how[:1] + what[2:3] + match[:1] + what[3:4] + how[1:2] + which[:1] + what[4:5]
             + more[:1] + match[1:] + what[5:6] + how[2:] + which[1:] + what[6:7] + trade[:1] + what[7:8]
             + more[1:] + what[8:] + trade[1:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Tens and ones with base ten blocks", "items": order}


# ============================================================ set 2: value of a digit
def value_wrong(n, i):
    d, other = digit(n, i), digit(n, 1 - i)
    if i == 1:
        return [d, n, d * 100]
    return [d * 10, n, other]


def value_e(n, i, red=False):
    d = digit(n, i)
    v = d * 10 ** i
    s = "%s is %s. The %s%d is in the %s place, so it is worth %d." % (n, to_n(n), "red " if red else "", d, PL[i], v)
    if i:
        s += " The digit is %d, but its value is %d." % (d, v)
    return s


def set_value(rnd):
    chart = [mcq_n(fig(chart_svg(n, hi=i)) + "What is the red digit worth?", digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i, True), rnd)
             for n, i in [(47, 1), (74, 0), (38, 1), (91, 1), (56, 0)]]
    plain = [mcq_n("What is the value of the %d in %d?" % (digit(n, i), n), digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i), rnd)
             for n, i in [(62, 1), (83, 0), (95, 1), (25, 1)]]
    place = [
        mcq("In 58, which digit is in the tens place?", 5, [8, 50, 58],
            "58 is 5 tens and 8 ones. The tens digit is 5. (Its value is 50.)", rnd),
        mcq("In 71, which digit is in the ones place?", 1, [7, 70, 71],
            "71 is 7 tens and 1 one. The ones digit is 1. It is the digit on the right.", rnd),
    ]
    has = [
        mcq_n("Which number has a 6 in the tens place?", 62, [26, 16, 6],
              "62 is 6 tens and 2 ones. 26 and 16 have 6 ones, not 6 tens. 6 has no tens.", rnd),
        mcq_n("Which number has a 3 in the ones place?", 43, [34, 30, 38],
              "43 is 4 tens and 3 ones. 34, 30 and 38 have 3 tens, not 3 ones.", rnd),
        mcq_n("Which number has 0 ones?", 70, [7, 17, 71],
              "70 is 7 tens and 0 ones. 7 and 17 have 7 ones, and 71 has 1 one.", rnd),
    ]
    wr = [
        mcq_n("Write “sixteen” as a number.", 16, [60, 61, 106],
              "Sixteen is 1 ten and 6 ones: 16. Sixty is 60. Listen for “teen”.", rnd),
        mcq_n("Write “seventy” as a number.", 70, [17, 7, 700],
              "Seventy is 7 tens and 0 ones: 70. Seventeen is 17.", rnd),
        mcq_n("Write “eighty-five” as a number.", 85, [58, 805, 80],
              "Eighty-five is 8 tens and 5 ones: 85. Do not write 80 and then 5. It has only 2 digits.", rnd),
    ]
    exp = [
        mcq("What is 47 in expanded form?", "40 + 7", ["4 + 7", "70 + 4", "4 + 70"],
            "47 is 4 tens and 7 ones. 4 tens = 40. So 47 = 40 + 7.", rnd),
        mcq_n("What number is 90 + 2?", 92, [902, 29, 11],
              "90 + 2 is 9 tens and 2 ones: 92. Do not write 90 and then 2. The answer has only 2 digits.", rnd),
    ]
    hund = mcq_n("100 = ☐ tens. What number goes in the box?", 10, [1, 100, 0],
                 "Count by 10s: 10, 20, 30 … 100. That is 10 tens. 10 tens make 1 hundred.", rnd)
    order = (chart[:2] + plain[:1] + place[:1] + wr[:1] + chart[2:3] + has[:1] + plain[1:2] + exp[:1]
             + chart[3:4] + wr[1:2] + place[1:] + has[1:2] + plain[2:3] + exp[1:] + chart[4:] + wr[2:]
             + has[2:] + plain[3:] + [hund])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "The value of each digit", "items": order}


# ============================================================ set 3: compare and order
def compare_e(big, small):
    if len(str(big)) != len(str(small)):
        return ("%d has %d digits and %d has only %d. So %d &gt; %d."
                % (big, len(str(big)), small, len(str(small)), big, small))
    if digit(big, 1) != digit(small, 1):
        return ("Compare the tens first: %s is more than %s. So %d &gt; %d."
                % (plural(digit(big, 1), 1), plural(digit(small, 1), 1), big, small))
    return ("The tens are the same, so compare the ones: %s is more than %s. So %d &gt; %d."
            % (plural(digit(big, 0), 0), plural(digit(small, 0), 0), big, small))


def set_compare(rnd):
    cmp_ = []
    for x, y in [(47, 74), (93, 39), (60, 58), (100, 99), (25, 52), (81, 18)]:
        lt = "&lt;" if x < y else "&gt;"
        gt = "&gt;" if x < y else "&lt;"
        e = compare_e(max(x, y), min(x, y))
        if (x, y) == (60, 58):
            e += " Do not compare the ones first: 8 ones is more than 0 ones, but 58 is less."
        cmp_.append(mcq("Which is true?", "%d %s %d" % (x, lt, y),
                        ["%d %s %d" % (x, gt, y), "%d = %d" % (x, y), "%d %s %d" % (y, lt, x)], e, rnd))
    big = [
        mcq_n("Which number is the greatest?", 86, [68, 66, 58],
              "Compare the tens. 86 has 8 tens, the most. So 86 is the greatest.", rnd),
        mcq_n("Which number is the least?", 13, [31, 33, 30],
              "Compare the tens. 13 has 1 ten. The others have 3 tens. So 13 is the least.", rnd),
        mcq_n("Which number is the greatest?", 97, [79, 90, 77],
              "97 and 90 both have 9 tens. Ones: 7 ones &gt; 0 ones. So 97 is the greatest.", rnd),
        mcq_n("Which number is the least?", 40, [45, 54, 44],
              "40, 45 and 44 have 4 tens. Ones: 0 is the fewest. So 40 is the least.", rnd),
    ]
    order = [
        mcq("Put 47, 74 and 44 in order from least to greatest.", "44, 47, 74",
            ["47, 44, 74", "74, 47, 44", "47, 74, 44"],
            "74 has 7 tens, so it is the greatest. 44 and 47 have 4 tens. Ones: 4 &lt; 7, so 44 &lt; 47. "
            "Order: 44, 47, 74.", rnd),
        mcq("Put 29, 92 and 9 in order from least to greatest.", "9, 29, 92",
            ["92, 29, 9", "29, 9, 92", "29, 92, 9"],
            "9 has only 1 digit, so it is the least. 29 has 2 tens and 92 has 9 tens. Order: 9, 29, 92.", rnd),
        mcq("Put 65, 56 and 60 in order from greatest to least.", "65, 60, 56",
            ["56, 60, 65", "65, 56, 60", "60, 65, 56"],
            "56 has 5 tens, so it is the least. 65 and 60 have 6 tens. Ones: 5 &gt; 0, so 65 &gt; 60. "
            "Order: 65, 60, 56.", rnd),
    ]
    between = [
        mcq_n("Which number is between 40 and 50?", 46, [64, 54, 39],
              "46 has 4 tens, so it is between 40 and 50. 64 and 54 are too big. 39 is too small.", rnd),
        mcq_n("Which number is between 70 and 80?", 73, [37, 83, 67],
              "73 has 7 tens, so it is between 70 and 80. 37 and 67 are too small. 83 is too big.", rnd),
    ]
    near = [
        mcq_n("What number is 10 more than 36?", 46, [37, 26, 56],
              "10 more: add 1 ten. The tens digit goes from 3 to 4: 46. (37 is 1 more. 26 is 10 less.)", rnd),
        mcq_n("What number is 1 less than 70?", 69, [60, 71, 68],
              "1 less: count back 1. 70, 69. (60 is 10 less. 71 is 1 more.)", rnd),
        mcq_n("What number is 10 less than 100?", 90, [99, 0, 110],
              "10 less: take away 1 ten. 10 tens − 1 ten = 9 tens = 90. (99 is 1 less.)", rnd),
    ]
    gl = [
        mcq_n("Which number is greater than 63?", 71, [36, 59, 60],
              "71 has 7 tens and 63 has 6 tens. So 71 &gt; 63. The others are less than 63.", rnd),
        mcq_n("Which number is less than 45?", 39, [54, 50, 46],
              "39 has 3 tens and 45 has 4 tens. So 39 &lt; 45. The others are greater than 45.", rnd),
    ]
    for a, b in [(44, 47), (47, 74), (9, 29), (29, 92), (56, 60), (60, 65), (40, 46), (46, 50), (70, 73),
                 (73, 80), (63, 71), (39, 45)]:
        assert a < b
    order = (cmp_[:2] + big[:2] + near[:1] + gl[:1] + cmp_[2:3] + order[:1] + between[:1] + near[1:2]
             + cmp_[3:4] + big[2:3] + order[1:2] + gl[1:] + cmp_[4:5] + near[2:] + big[3:] + between[1:]
             + cmp_[5:] + order[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers to 100", "items": order}


# ============================================================ set 4: count by 2s, 5s and 10s
def set_skip(rnd):
    pat = []
    for seq, ans, wrong, e in [
            ([2, 4, 6, 8], 10, [9, 12, 11], "Count by 2s: add 2 each time. 8 + 2 = 10."),
            ([5, 10, 15, 20], 25, [21, 30, 35], "Count by 5s: add 5 each time. 20 + 5 = 25."),
            ([10, 20, 30, 40], 50, [41, 60, 45], "Count by 10s: add 10 each time. 40 + 10 = 50."),
            ([35, 40, 45], 50, [46, 55, 60], "Count by 5s: add 5 each time. 45 + 5 = 50."),
            ([7, 17, 27, 37], 47, [38, 40, 57], "Count by 10s from 7: add 1 ten each time. "
                                                "The ones digit stays 7. 37 + 10 = 47."),
            ([1, 3, 5, 7], 9, [8, 10, 11], "Count by 2s from 1: add 2 each time. 7 + 2 = 9."),
            ([50, 48, 46, 44], 42, [43, 40, 46], "Count back by 2s: take away 2 each time. 44 − 2 = 42."),
            ([90, 80, 70], 60, [69, 50, 80], "Count back by 10s: take away 10 each time. 70 − 10 = 60."),
            ([100, 95, 90], 85, [89, 80, 75], "Count back by 5s: take away 5 each time. 90 − 5 = 85.")]:
        step = seq[1] - seq[0]
        assert all(seq[k + 1] - seq[k] == step for k in range(len(seq) - 1)) and seq[-1] + step == ans
        pat.append(mcq_n("What comes next? " + ", ".join(map(str, seq)) + ", ☐", ans, wrong, e, rnd))
    miss = mcq_n("What number is missing? 65, 70, 75, ☐, 85", 80, [76, 85, 90],
                 "Count by 5s: 65, 70, 75, 80, 85. 75 + 5 = 80.", rnd)
    not_say = mcq_n("You count by 5s from 0. Which number do you <b>not</b> say?", 32, [35, 40, 25],
                    "Counting by 5s from 0, every number ends in 0 or 5: 25, 30, 35, 40. 32 ends in 2.", rnd)
    say = mcq_n("You count by 2s from 0. Which number do you say?", 46, [45, 33, 51],
                "Counting by 2s from 0, every number ends in 0, 2, 4, 6 or 8. 46 ends in 6.", rnd)
    pics = [
        mcq_n(fig(groups_svg(7, 2)) + "Count by 2s. How many dots are there?", 14, [7, 13, 16],
              "There are 7 groups of 2. Count by 2s: 2, 4, 6, 8, 10, 12, 14.", rnd),
        mcq_n(fig(groups_svg(6, 5)) + "Count by 5s. How many dots are there?", 30, [6, 11, 25],
              "There are 6 groups of 5. Count by 5s: 5, 10, 15, 20, 25, 30.", rnd),
        mcq_n(fig(groups_svg(5, 10)) + "Each ten frame is full. How many dots are there?", 50, [5, 15, 40],
              "A full ten frame has 10 dots. Count by 10s: 10, 20, 30, 40, 50.", rnd),
        mcq(fig(coins_svg(8, 5)) + "Count the nickels by 5s. How much money is it?", "40¢",
            ["8¢", "13¢", "45¢"],
            "A nickel is 5¢. Count by 5s 8 times: 5, 10, 15, 20, 25, 30, 35, 40. That is 40¢.", rnd),
        mcq(fig(coins_svg(7, 10)) + "Count the dimes by 10s. How much money is it?", "70¢",
            ["7¢", "17¢", "60¢"],
            "A dime is 10¢. Count by 10s 7 times: 10, 20, 30, 40, 50, 60, 70. That is 70¢.", rnd),
    ]
    color = mcq("On a hundred chart, you count by 10s from 3. Which numbers do you colour?",
                "3, 13, 23, 33", ["3, 4, 5, 6", "10, 20, 30, 40", "3, 8, 13, 18"],
                "Counting by 10s from 3, add 10 each time: 3, 13, 23, 33. The ones digit stays 3. "
                "On the chart, you move straight down the column.", rnd)
    howmany = mcq_n("You count by 5s from 5 to 50. How many numbers do you say?", 10, [5, 50, 9],
                    "5, 10, 15, 20, 25, 30, 35, 40, 45, 50. That is 10 numbers. 10 fives make 50.", rnd)
    mitt = mcq_n("There are 9 pairs of mittens. Count by 2s. How many mittens are there?", 18, [9, 11, 20],
                 "A pair is 2. Count by 2s 9 times: 2, 4, 6, 8, 10, 12, 14, 16, 18.", rnd)
    order = (pat[:3] + pics[:1] + pat[3:4] + pics[1:2] + pat[5:6] + pics[2:3] + [say] + pat[4:5]
             + pics[3:4] + [miss] + pat[6:7] + [mitt] + pics[4:] + pat[7:8] + [not_say] + pat[8:]
             + [color, howmany])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Count by 2s, 5s and 10s", "items": order}


# ============================================================ set 5: hundred chart, number lines and word problems
def set_chart_line(rnd):
    items = []
    # piece 1: 3 x 3 from 34, ? at the centre = 45
    items.append(mcq_n(fig(hchart_svg(34, 3, 3, (1, 1), hide=((1, 0), (1, 2)))) +
                       "This is part of a hundred chart. What number is the ?", 45, [36, 55, 44],
                       "Each step right is 1 more. Each step down is 10 more. 35 is above the ?, "
                       "so the ? is 35 + 10 = 45.", rnd))
    # piece 2: 3 x 3 from 56, ? at bottom middle = 77
    items.append(mcq_n(fig(hchart_svg(56, 3, 3, (2, 1), hide=((2, 0), (2, 2)))) +
                       "This is part of a hundred chart. What number is the ?", 77, [68, 87, 76],
                       "Look up: 67 is above the ?. One step down is 10 more: 67 + 10 = 77.", rnd))
    # piece 3: 3 x 3 from 12, ? at bottom right = 34, with the middle hidden
    items.append(mcq_n(fig(hchart_svg(12, 3, 3, (2, 2), hide=((1, 1),))) +
                       "This is part of a hundred chart. What number is the ?", 34, [43, 44, 25],
                       "Look up: 24 is above the ?. 24 + 10 = 34. It is also 1 more than 33.", rnd))
    items.append(mcq_n("On a hundred chart, which number is just below 47?", 57, [48, 37, 46],
                       "One row down is 10 more. 47 + 10 = 57. (48 is just to the right. 37 is just above.)", rnd))
    items.append(mcq_n("On a hundred chart, which number is just above 82?", 72, [92, 81, 83],
                       "One row up is 10 less. 82 − 10 = 72. (92 is just below.)", rnd))
    nl = [
        mcq_n(fig(number_line_svg(0, 100, 10, [0, 50, 100], 70)) + "What number does the arrow point to?",
              70, [7, 60, 80],
              "From 0 to 50 there are 5 jumps, so each mark is 10. Count by 10s: 10, 20 … 70.", rnd),
        mcq_n(fig(number_line_svg(40, 50, 1, [40, 45, 50], 47)) + "What number does the arrow point to?",
              47, [74, 46, 48],
              "Each mark is 1. Count on from 45: 46, 47. The arrow is at 47.", rnd),
        mcq_n(fig(number_line_svg(60, 80, 1, [60, 70, 80], 76)) + "What number does the arrow point to?",
              76, [67, 75, 86],
              "Each mark is 1. Start at 70 and count on 6 marks: 71, 72 … 76.", rnd),
        mcq_n(fig(number_line_svg(0, 100, 5, [0, 50, 100], 35)) + "What number does the arrow point to?",
              35, [7, 70, 30],
              "From 0 to 50 there are 10 jumps, so each mark is 5. Count by 5s: 5, 10 … 35. "
              "(7 is the number of marks, not the number.)", rnd),
        mcq_n(fig(number_line_svg(20, 30, 1, [20, 30], 25)) + "The arrow is halfway between 20 and 30. "
              "What number is it?", 25, [15, 50, 22],
              "From 20 to 30 there are 10 small jumps. Halfway is 5 jumps: 20 + 5 = 25.", rnd),
    ]
    wp = [
        mcq_n("Kai has 4 packs of 10 hockey cards and 6 single cards. How many cards does he have?", 46,
              [64, 10, 406],
              "4 packs of 10 = 40. 40 + 6 = 46. (4 tens and 6 ones.)", rnd),
        mcq("On a field trip to a salmon hatchery, Ava counts 63 salmon. Liam counts 36. Who counts more?",
            "Ava", ["Liam", "They count the same", "You cannot tell"],
            "Compare the tens: 63 has 6 tens and 36 has 3 tens. 63 &gt; 36, so Ava counts more.", rnd),
        mcq("For the Terry Fox Run, Simran gives 7 toonies. A toonie is $2. How much money is that?",
            "$14", ["$7", "$9", "$16"],
            "Count by 2s 7 times: 2, 4, 6, 8, 10, 12, 14. 7 toonies are $14.", rnd),
        mcq_n("On a BC Ferries boat, the cars park in 9 lanes. Each lane has 10 cars. How many cars are there?", 90,
              [19, 9, 900],
              "Count by 10s 9 times: 10, 20 … 90. 9 tens = 90.", rnd),
        mcq_n("Hana’s mystery number is between 60 and 70. It has 4 ones. What is it?", 64,
              [46, 74, 54],
              "Between 60 and 70 means 6 tens. Then 4 ones: 64.", rnd),
        mcq("Owen reads 47 pages. Zara reads 74 pages. Who reads more pages?", "Zara",
            ["Owen", "They read the same", "You cannot tell"],
            "Compare the tens: 74 has 7 tens and 47 has 4 tens. 74 &gt; 47, so Zara reads more.", rnd),
        mcq("Arjun has 9 nickels. A nickel is 5¢. How much money does he have?", "45¢",
            ["9¢", "14¢", "50¢"],
            "Count by 5s 9 times: 5, 10, 15, 20, 25, 30, 35, 40, 45. 9 nickels are 45¢.", rnd),
        mcq_n("12 students put on skates at the rink. Each student wears 2 skates. How many skates is that?", 24,
              [12, 14, 22],
              "Count by 2s 12 times: 2, 4, 6 … 22, 24. 12 students wear 24 skates.", rnd),
        mcq_n("Today is day 87 of school. What day of school will it be in 10 days?", 97,
              [88, 77, 98],
              "10 days later is 10 more. 87 + 10 = 97. Only the tens digit changes. (88 is 1 more.)", rnd),
        mcq_n("Leah writes seventy-four as 704. What should she write?", 74, [704, 47, 70],
              "Seventy-four is 7 tens and 4 ones: 74. It has only 2 digits. Do not write 70 and then 4.", rnd),
    ]
    for v, w in [(40 + 6, 46), (7 * 2, 14), (9 * 10, 90), (9 * 5, 45), (12 * 2, 24), (87 + 10, 97),
                 (35 + 10, 45), (67 + 10, 77), (24 + 10, 34), (47 + 10, 57), (82 - 10, 72)]:
        assert v == w
    order = items[:1] + nl[:1] + items[3:4] + nl[1:2] + items[1:2] + nl[2:3] + items[4:5] + nl[3:4] \
        + items[2:3] + nl[4:] + wp
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Hundred chart, number lines and word problems", "items": order}


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
        "<h2>Tens and ones</h2>"
        "<p>10 ones make 1 ten. 10 tens make 1 hundred. "
        "A 2-digit number has a <b>tens</b> place and a <b>ones</b> place.</p>"
        "<figure class='sn-fig'>" + blocks_svg(4, 7, labels=True) +
        "<figcaption>Base ten blocks for 47. A rod is 10 and a small cube is 1.</figcaption></figure>"
        "<h2>The value of a digit</h2>"
        "<p>The place tells you what a digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(47, hi=1) +
        "<figcaption>In 47 the 4 is in the tens place. Its value is 4 tens, or 40.</figcaption></figure>"
        "<p>47 = 40 + 7. If a place is empty, write <b>0</b> there: seventy is 70.</p>" +
        ex("Write the number", "Write “sixty-three” as a number.",
           "6 tens and 3 ones. Write the tens digit first: 6, 3.", "63 (not 36 or 603)") +
        "<h2>Compare and order</h2>"
        "<p>Compare the tens first. If the tens are the same, compare the ones.</p>" +
        ex("Compare", "47 ☐ 74", "Tens: 4 tens &lt; 7 tens.", "47 &lt; 74") +
        "<p>&gt; means “is greater than”. &lt; means “is less than”. The open side faces the greater number.</p>"
        "<h2>Count by 2s, 5s and 10s</h2>"
        "<p>Skip counting is fast counting. By 2s: 2, 4, 6, 8. By 5s: 5, 10, 15, 20. By 10s: 10, 20, 30, 40.</p>"
        "<figure class='sn-fig'>" + coins_svg(6, 5) +
        "<figcaption>6 nickels. Count by 5s: 5, 10, 15, 20, 25, 30. That is 30¢.</figcaption></figure>"
        "<h2>Hundred chart and number lines</h2>"
        "<p>On a hundred chart, one step right is 1 more. One step down is 10 more.</p>"
        "<figure class='sn-fig'>" + hchart_svg(34, 3, 3, (1, 1)) +
        "<figcaption>The ? is below 35, so it is 35 + 10 = 45.</figcaption></figure>"
        "<p>On a number line, find what each mark is worth before you count.</p>"
        "<figure class='sn-fig'>" + number_line_svg(0, 100, 10, [0, 50, 100], 70) +
        "<figcaption>Each mark is 10. The arrow is at 70.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up the digits (47 and 74)", "Write the tens first, then the ones"],
            ["Reading the digit, not its value (the 4 in 47 is 4)", "The 4 is in the tens place: 40"],
            ["Counting blocks, not their values (4 rods and 7 cubes = 11)", "Count rods by 10s, then add the ones: 47"],
            ["Writing each part you hear (sixty-three = 603)", "A number less than 100 has 2 digits: 63"],
            ["Comparing the ones first (58 &gt; 60)", "Compare the tens first: 60 &gt; 58"],
            ["Counting the marks on a number line", "Find what each mark is worth, then count"],
        ])
    )


FAQ = [
    {"q": "What number skills are in the Grade 2 BC math curriculum?",
     "a": "Grade 2 students in BC work with number concepts to 100: counting, skip counting by 2s, 5s and 10s, "
          "place value with tens and ones, and comparing and ordering numbers."},
    {"q": "How do I explain tens and ones to a Grade 2 child?",
     "a": "Use base ten blocks or bundles of 10 straws: 10 ones make a ten. Then 47 is 4 tens and 7 ones, or 40 + 7."},
    {"q": "Why does my child write 74 for 47?",
     "a": "Mixing up the digits is a common place value mistake. Ask how many tens and how many ones, and remind them that the tens digit is written first."},
    {"q": "How can children practise skip counting at home?",
     "a": "Count pairs of socks by 2s, nickels by 5s and dimes by 10s. A hundred chart helps too: counting by 10s moves straight down a column."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(52801)
    sets = [set_blocks(rnd), set_value(rnd), set_compare(rnd), set_skip(rnd), set_chart_line(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "numbers-to-100", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 100: Tens and Ones, Comparing and Skip Counting",
        "seo_title": "Grade 2 Numbers to 100 Math Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Numbers to 100",
        "domain": "Number",
        "standard_code": "Grade 2: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Number concepts to 100",
        "meta_desc": "Free Grade 2 math worksheets on numbers to 100: tens and ones with base ten blocks, the value of each digit, comparing and ordering, counting by 2s, 5s and 10s, the hundred chart and number lines. 100 questions with an answer key, following the BC curriculum.",
        "key_big": "The place of a digit tells you its value. The 4 in 47 is worth 40.",
        "key_sub": "47 is 4 tens and 7 ones: 40 + 7. To compare, look at the tens first: 47 < 74.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(base ten blocks|number line|groups of|coins)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
