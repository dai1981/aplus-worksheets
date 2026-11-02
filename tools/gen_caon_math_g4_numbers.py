# -*- coding: utf-8 -*-
"""
Ontario Grade 4 Math: Numbers to 10 000 (Ontario Mathematics Curriculum 2020, Grade 4: B1.1, also B1.2)
  python3 tools/gen_caon_math_g4_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
Ontario number style: 4-digit numbers have no separator (4053); 5 or more digits use a no-break space
between groups of three (10 000). Never commas. Number words without "and" (four thousand fifty-three).
Wrong answers come from real mistakes: leaving out a zero (4053 -> 453), adding a zero or writing each
spoken part (4053 -> 40 053), reading the digit instead of its value (the 5 in 4053 is 5),
writing a regrouped number inside the numeral (3 thousands, 14 hundreds -> 31 450),
comparing the first digit only when the numbers have different lengths, and reading every
mark on a number line as 1, 10 or 100 without working out the jump.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
SIDE = "#a9d3b5"
TOP = "#e3f1e7"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand"]


# ------------------------------------------------------------ helpers
class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

def c(n):
    """Ontario style: 4053 stays 4053; 10000 -> 10 000 with a no-break space."""
    s = str(n)
    if n < 10000:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


def mcq(q, correct, wrong, e, rnd):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    ch = wrong + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, wrong, e, rnd, pre=""):
    """Whole-number choices, all different values."""
    assert all(isinstance(w, int) and w >= 0 for w in wrong + [correct]), (q, correct, wrong)
    assert len(set(wrong + [correct])) == 4, (q, correct, wrong)
    return mcq(q, pre + c(correct), [pre + c(w) for w in wrong], e, rnd)


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


def thto(th, h, t, o):
    return "%s, %s, %s and %s" % (plural(th, 3), plural(h, 2), plural(t, 1), plural(o, 0))


def thto_n(n):
    return thto(digit(n, 3), digit(n, 2), digit(n, 1), digit(n, 0))


def rnd_to(n, p):
    return (n + p // 2) // p * p


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
    th, r = divmod(n, 1000)
    h, r = divmod(r, 100)
    parts = []
    if th:
        parts.append(ONES[th] + " thousand")
    if h:
        parts.append(ONES[h] + " hundred")
    if r:
        parts.append(words99(r))
    return " ".join(parts)


assert words(4053) == "four thousand fifty-three" and words(7806) == "seven thousand eight hundred six"


# ------------------------------------------------------------ figures
U = 8                      # base ten blocks: a small cube = U, a rod = 10U, a flat = 10U x 10U, a big cube with depth
D = 26                     # depth offset for the drawn big cube (1000)
G = 8                      # gap between pieces
GG = 22                    # gap between groups
MG = 8


def blocks_svg(th, h, t, o, labels=False):
    """Base ten blocks: th big cubes, h flats, t rods, o small cubes. Faces are exact 1 : 10 : 100."""
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

    tcols = th if th <= 2 else 2
    trows = (th + tcols - 1) // tcols if th else 0

    def bigs(x, y):
        s = []
        for k in range(th):
            cx = x + (k % tcols) * (F + D + G)
            cy = y + (k // tcols) * (F + D + G) + D
            s.append("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (cx, cy, cx + D, cy - D, cx + D + F, cy - D, cx + F, cy, TOP, GREEN))
            s.append("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (cx + F, cy, cx + F + D, cy - D, cx + F + D, cy - D + F, cx + F, cy + F, SIDE, GREEN))
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (cx, cy, F, F, FILL, GREEN))
            s += grid(cx, cy, F, F, 10, 10)
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

    if th:
        groups.append((tcols * (F + D) + (tcols - 1) * G, trows * (F + D) + (trows - 1) * G, bigs, plural(th, 3)))
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


CW, HEAD, ROW = 112, 34, 50


def chart_svg(n, hi=None):
    """Thousands / hundreds / tens / ones chart. hi = place index to colour red."""
    k_n = 4
    x0 = y0 = 6
    W, Hh = 2 * x0 + k_n * CW, 2 * y0 + HEAD + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, k_n * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, k_n * CW, HEAD, FILL)]
    for k in range(k_n):
        i = k_n - 1 - k
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append(text(cx, y0 + 23, cap(PL[i]), 15))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + k_n * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "place value chart showing %s" % c(n))


def number_line_svg(lo, hi, step, labels, arrow, show=None):
    """Number line lo..hi with a tick every step, numbers under `labels` and a red arrow at `arrow`."""
    L, R, Y = 40, 440, 58
    W, Hh = 480, 100

    def X(v):
        return L + (v - lo) * (R - L) / (hi - lo)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, c(v), 15, col=GREEN))
        v += step
    ax = X(arrow)
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    if show:
        s.append(text(min(max(ax, 60), W - 60), Y - 44, show, 15, col=RED))
    top = 18 if show else 0
    body = "".join(s)
    if top:
        body = "<g transform='translate(0 %d)'>%s</g>" % (top, body)
    return svg_wrap(W, Hh + top, body, "number line from %s to %s" % (c(lo), c(hi)))


def blocks_e(th, h, t, o):
    n = 1000 * th + 100 * h + 10 * t + o
    s = ("A big cube is 1000, a flat is 100, a rod is 10 and a small cube is 1. %s make %s."
         % (cap(thto(th, h, t, o)), c(n)))
    empty = [PL[i] for i, d in ((2, h), (1, t), (0, o)) if d == 0]
    if empty:
        s += " There are no %s, so write 0 in %s." % (" or ".join(empty),
                                                     "that place" if len(empty) == 1 else "those places")
    return s


# ============================================================ set 1: base ten blocks
def set_blocks(rnd):
    what = []
    for th, h, t, o, wrong in [
            (3, 4, 2, 6, [15, 6243, 3462]),             # counted pieces, read backwards, tens/ones swapped
            (2, 5, 0, 7, [257, 14, 20507]),             # left out the zero, counted pieces, extra zero
            (4, 0, 3, 8, [438, 4308, 15]),              # left out the zero, zero in the wrong place, counted pieces
            (1, 2, 7, 0, [127, 1207, 10]),
            (5, 0, 6, 1, [561, 50061, 5610]),           # 5061 -> 561 or 50 061
            (2, 4, 1, 8, [15, 8142, 2481]),
            (4, 1, 0, 0, [41, 4010, 5]),
            (3, 0, 0, 9, [39, 3090, 30009])]:
        n = 1000 * th + 100 * h + 10 * t + o
        e = blocks_e(th, h, t, o) + " Start with the big cubes, then the flats, rods and small cubes."
        what.append(mcq_n(fig(blocks_svg(th, h, t, o)) + "What number do the base ten blocks show?", n, wrong, e, rnd))
    how = [
        mcq_n(fig(blocks_svg(3, 5, 2, 4)) + "How many tens are there?", 2, [5, 4, 20],
              "Each rod is 1 ten. There are 2 rods, so there are 2 tens. The number is 3524.", rnd),
        mcq_n(fig(blocks_svg(2, 6, 0, 3)) + "How many hundreds are there?", 6, [2, 3, 600],
              "Each flat is 1 hundred. There are 6 flats, so there are 6 hundreds. The number is 2603.", rnd),
        mcq_n(fig(blocks_svg(4, 2, 6, 1)) + "How many thousands are there?", 4, [2, 6, 4000],
              "Each big cube is 1 thousand. There are 4 big cubes, so there are 4 thousands. "
              "Their value is 4000, but the question asks how many. The number is 4261.", rnd),
    ]
    match = []
    for th, h, t, o in [(3, 6, 2, 5), (2, 1, 5, 4)]:
        wrong = [thto(o, t, h, th), thto(th, t, h, o), thto(h, th, t, o)]
        match.append(mcq(fig(blocks_svg(th, h, t, o)) + "Which matches the blocks?", thto(th, h, t, o), wrong,
                         "Count each kind of block: %s. The number is %s." % (thto(th, h, t, o),
                                                                              c(1000 * th + 100 * h + 10 * t + o)), rnd))
    more = [
        mcq_n(fig(blocks_svg(3, 9, 6, 2)) + "Add 1 more flat. What number is it now?", 4062, [31062, 3862, 4962],
              "The blocks show 3962. Add 1 flat: now there are 10 flats. Trade 10 flats for 1 big cube. "
              "That is 4 thousands, 0 hundreds, 6 tens and 2 ones: 4062.", rnd),
        mcq_n(fig(blocks_svg(2, 7, 9, 3)) + "Add 1 more rod. What number is it now?", 2803, [27103, 2783, 3793],
              "The blocks show 2793. Add 1 rod: now there are 10 rods. Trade 10 rods for 1 flat. "
              "That is 2 thousands, 8 hundreds, 0 tens and 3 ones: 2803.", rnd),
    ]
    ten_flats = mcq_n(fig(blocks_svg(0, 10, 0, 0)) + "There are 10 flats. What number do they show?", 1000,
                      [10, 100, 10000],
                      "Each flat is 100. Count by 100s: 100, 200, 300 … 1000. "
                      "10 hundreds make 1 thousand, the same as 1 big cube.", rnd)
    ten_cubes = mcq_n("Each big cube is 1000. What number do 10 big cubes make?", 10000, [1000, 100000, 10],
                      "Count by 1000s: 1000, 2000, 3000 … 10" + NB + "000. 10 thousands make 10" + NB + "000. "
                      "Ten thousand has 5 digits: 1 and four zeros.", rnd)
    wd = [
        mcq_n("Write “four thousand fifty-three” as a number.", 4053, [453, 40053, 4530],
              "4 thousands, 0 hundreds, 5 tens and 3 ones. There are no hundreds, so write 0 there: 4053. "
              "It has 4 digits, not 3 (453) or 5 (40" + NB + "053).", rnd),
        mcq_n("Write “six thousand nine hundred four” as a number.", 6904, [694, 6940, 6094],
              "6 thousands, 9 hundreds, 0 tens and 4 ones: 6904. The 4 is ones, so it goes last. "
              "Write 0 for the empty tens place.", rnd),
    ]
    which = mcq_n("Which number has 5 thousands, 0 hundreds, 7 tens and 1 one?", 5071, [571, 5701, 50071],
                  "Write the digits in order: thousands 5, hundreds 0, tens 7, ones 1. That is 5071.", rnd)
    assert 3962 + 100 == 4062 and 2793 + 10 == 2803
    order = (what[:3] + how[:2] + what[3:5] + match[:1] + wd[:1] + what[5:6] + how[2:] + [which]
             + what[6:] + match[1:] + wd[1:] + [ten_flats] + more + [ten_cubes])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Base ten blocks: thousands, hundreds, tens and ones", "items": order}


# ============================================================ set 2: value of a digit
def value_wrong(n, i):
    d = digit(n, i)
    out = [d]                                    # the digit, not its value
    out += [d * 10 ** (i + 1)]                   # one place too far left
    out += [d * 10 ** (i - 1)] if i >= 2 else [d * 10 ** (i + 2)]
    return out


def value_e(n, i, red=False):
    d = digit(n, i)
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), c(d * 10 ** i), d, c(d * 10 ** i)))


def set_value(rnd):
    chart = []
    for n, i in [(5839, 3), (7064, 1), (2486, 2), (9352, 1), (6207, 2)]:
        chart.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?",
                           digit(n, i) * 10 ** i, value_wrong(n, i), value_e(n, i, True), rnd))
    plain = []
    for n, i in [(4916, 2), (8305, 3), (1672, 1), (3058, 1), (7493, 2), (2741, 3)]:
        d = digit(n, i)
        plain.append(mcq_n("What is the value of the digit %d in %s?" % (d, c(n)), d * 10 ** i,
                           value_wrong(n, i), value_e(n, i), rnd))
    place = []
    for n, i in [(6492, 2), (9083, 3), (3715, 1)]:
        d = digit(n, i)
        others = [digit(n, x) for x in range(4) if x != i]
        place.append(mcq_n("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, others,
                           "%s has %s. The %s digit is %d." % (c(n), thto_n(n), PL[i], d), rnd))
    has = []
    for d, i, nums in [(5, 2, [4538, 5438, 4385, 4358]), (8, 1, [2781, 8271, 2871, 2817]),
                       (3, 3, [3740, 7340, 7403, 7430])]:
        good = [x for x in nums if digit(x, i) == d]
        assert len(good) == 1
        good = good[0]
        has.append(mcq_n("Which number has %s %d in the %s place?" % ("an" if d == 8 else "a", d, PL[i]),
                         good, [x for x in nums if x != good],
                         "In %s the %d is in the %s place, so it is worth %s."
                         % (c(good), d, PL[i], c(d * 10 ** i)), rnd))
    more = [
        mcq_n("What number is 1000 more than 5062?", 6062, [5162, 5072, 15062],
              "1000 more changes only the thousands digit: 5 thousands → 6 thousands. 5062 + 1000 = 6062.", rnd),
        mcq_n("What number is 100 less than 8034?", 7934, [8934, 8024, 7034],
              "There are 0 hundreds, so trade 1 thousand for 10 hundreds: 7 thousands, 10 hundreds. "
              "Take away 1 hundred: 7 thousands, 9 hundreds, 3 tens, 4 ones = 7934.", rnd),
        mcq_n("What number is 10 more than 6995?", 7005, [7095, 6996, 6905],
              "6995 has 9 tens. 10 more makes 10 tens, which is 1 hundred. That makes 10 hundreds, which is "
              "1 thousand. 6995 + 10 = 7005.", rnd),
    ]
    assert 5062 + 1000 == 6062 and 8034 - 100 == 7934 and 6995 + 10 == 7005
    order = (chart[:2] + plain[:2] + place[:1] + chart[2:3] + plain[2:3] + has[:1] + place[1:2] + plain[3:4]
             + chart[3:4] + has[1:2] + more[:1] + plain[4:5] + place[2:] + chart[4:] + has[2:] + plain[5:]
             + more[1:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "The value of each digit", "items": order}


# ============================================================ set 3: expanded form and decomposing
def exp_str(*parts):
    return " + ".join(c(p) for p in parts)


def set_decompose(rnd):
    std = []
    for n, wrong in [
            (5062, [(5, 0, 6, 2), (5000, 600, 2), (500, 60, 2)]),
            (8401, [(8, 4, 0, 1), (8000, 400, 10), (800, 40, 1)]),
            (2970, [(2, 9, 7, 0), (2000, 900, 7), (200, 90, 70)]),
            (6038, [(6, 0, 3, 8), (6000, 300, 8), (600, 30, 8)]),
            (4527, [(4, 5, 2, 7), (4000, 500, 2, 7), (400, 50, 20, 7)])]:
        parts = [digit(n, i) * 10 ** i for i in range(3, -1, -1) if digit(n, i)]
        assert sum(parts) == n
        for w in wrong:
            assert sum(w) != n
        std.append(mcq("What is %s in expanded form?" % c(n), exp_str(*parts), [exp_str(*w) for w in wrong],
                       "%s is %s. Write the value of each digit and skip the zeros: %s = %s."
                       % (c(n), thto_n(n), c(n), exp_str(*parts)), rnd))
    back = []
    for parts, wrong in [((5000, 200, 9), [529, 5290, 50209]), ((7000, 30, 4), [734, 7340, 70034]),
                         ((3000, 800, 6), [386, 3860, 30806]), ((9000, 5), [95, 9050, 9500]),
                         ((400, 6000, 70, 2), [4672, 6742, 6072])]:
        n = sum(parts)
        e = "%s = %s. That is %s." % (exp_str(*parts), c(n), thto_n(n))
        if 0 in [digit(n, i) for i in range(3)]:
            e += " Write 0 for each empty place, so the number has 4 digits."
        if parts[0] < parts[1]:
            e += " The parts are not in order, so put each digit in its own place."
        back.append(mcq_n("What number is %s?" % exp_str(*parts), n, wrong, e, rnd))
    regroup = [
        mcq_n("4361 = 4 thousands, 2 hundreds, ☐ tens and 1 one. What number goes in the box?", 16, [6, 15, 60],
              "Only 2 hundreds are used, so 1 hundred becomes 10 tens. 10 + 6 = 16 tens. "
              "Check: 4000 + 200 + 160 + 1 = 4361.", rnd),
        mcq_n("3728 = 2 thousands, ☐ hundreds, 2 tens and 8 ones. What number goes in the box?", 17, [7, 3, 27],
              "Only 2 thousands are used, so 1 thousand becomes 10 hundreds. 10 + 7 = 17 hundreds. "
              "Check: 2000 + 1700 + 20 + 8 = 3728.", rnd),
        mcq("Which is another way to make 5380?", "4 thousands, 13 hundreds and 8 tens",
            ["5 thousands, 13 hundreds and 8 tens", "4 thousands, 3 hundreds and 18 tens",
             "4 thousands, 13 hundreds and 80 tens"],
            "Trade 1 thousand for 10 hundreds: 4000 + 1300 + 80 = 5380. "
            "(The others make 6380, 4480 and 6100.)", rnd),
        mcq("Which is the same as 6407?", "64 hundreds and 7 ones",
            ["64 hundreds and 7 tens", "6 hundreds, 4 tens and 7 ones", "640 hundreds and 7 ones"],
            "6 thousands = 60 hundreds, so 6407 has 60 + 4 = 64 hundreds and 7 ones. 6400 + 7 = 6407.", rnd),
    ]
    assert 4000 + 200 + 160 + 1 == 4361 and 2000 + 1700 + 28 == 3728
    assert (4000 + 1300 + 80, 5000 + 1300 + 80, 4000 + 300 + 180, 4000 + 1300 + 800) == (5380, 6380, 4480, 6100)
    assert (6400 + 7, 6400 + 70, 647, 64000 + 7) == (6407, 6470, 647, 64007)
    hund = [
        mcq_n("47 hundreds is the same as what number?", 4700, [470, 47, 47000],
              "1 hundred = 100, so 47 hundreds = 47 × 100 = 4700. That is 4 thousands and 7 hundreds.", rnd),
        mcq_n("How many hundreds are in 3600?", 36, [6, 3, 360],
              "3 thousands = 30 hundreds. 30 + 6 = 36 hundreds. Check: 36 × 100 = 3600. "
              "(6 is only the hundreds digit.)", rnd),
        mcq_n("How many tens are in 2480?", 248, [8, 24, 2480],
              "2480 = 2000 + 400 + 80 = 200 tens + 40 tens + 8 tens = 248 tens. Check: 248 × 10 = 2480.", rnd),
    ]
    assert 47 * 100 == 4700 and 36 * 100 == 3600 and 248 * 10 == 2480
    comp = [
        mcq_n("What number is 3 thousands, 14 hundreds and 5 tens?", 4450, [31450, 3450, 4405],
              "14 hundreds = 1400. 3000 + 1400 + 50 = 4450. Do not write 14 inside the number.", rnd),
        mcq_n("What number is 5 thousands, 11 hundreds and 9 ones?", 6109, [51109, 5109, 5119],
              "11 hundreds = 1100 = 1 thousand and 1 hundred. 5000 + 1100 + 9 = 6109.", rnd),
        mcq_n("What number is 2 thousands, 6 hundreds, 13 tens and 4 ones?", 2734, [26134, 2634, 2644],
              "13 tens = 130 = 1 hundred and 3 tens. 2000 + 600 + 130 + 4 = 2734.", rnd),
    ]
    assert 3000 + 1400 + 50 == 4450 and 5000 + 1100 + 9 == 6109 and 2000 + 600 + 130 + 4 == 2734
    order = (std[:2] + back[:2] + std[2:3] + back[2:3] + hund[:1] + std[3:4] + back[3:4] + regroup[:1]
             + hund[1:2] + std[4:] + back[4:] + regroup[1:2] + hund[2:] + comp[:1] + regroup[2:3]
             + comp[1:2] + regroup[3:] + comp[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Expanded form and decomposing in different ways", "items": order}


# ============================================================ set 4: compare and order
LT, GT = " &lt; ", " &gt; "
TT = "10" + NB + "000"


def first_diff(a, b):
    for i in range(3, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def set_compare(rnd):
    pick = []
    for kind, nums in [("greatest", [6072, 6702, 6270, 6207]), ("least", [8019, 8901, 8091, 8910]),
                       ("greatest", [9989, 10000, 9899, 998]), ("least", [4230, 423, 4023, 2304]),
                       ("greatest", [5050, 5505, 5500, 5055]), ("least", [7654, 7645, 7564, 7546])]:
        ans = max(nums) if kind == "greatest" else min(nums)
        rest = [x for x in nums if x != ans]
        lens = [len(str(x)) for x in nums]
        if ans == 10000:
            e = (TT + " has 5 digits. All the others have 4 digits or fewer, so " + TT
                 + " is the greatest, even though 9989 starts with a 9.")
        elif len(str(ans)) == 3:
            e = ("%s has only 3 digits. The others have 4 digits, so they are all greater. %s is the least."
                 % (c(ans), c(ans)))
        else:
            assert len(set(lens)) == 1
            srt = sorted(nums, reverse=(kind == "greatest"))
            i = first_diff(srt[0], srt[1])
            e = ("All four numbers have the same number of digits. Compare from the left. "
                 "%s and %s are the closest: they first differ in the %s place, %d %s %d. So %s is the %s."
                 % (c(srt[0]), c(srt[1]), PL[i], digit(srt[0], i), "&gt;" if kind == "greatest" else "&lt;",
                    digit(srt[1], i), c(ans), kind))
        pick.append(mcq_n("Which number is the %s?" % kind, ans, rest, e, rnd))
    true = [
        ("5602" + LT + "5620", ["3070" + GT + "3700", "9999" + GT + TT, "8143" + LT + "8134"],
         "5602 and 5620 have the same thousands and hundreds. Tens: 0 tens &lt; 2 tens, so 5602 &lt; 5620. "
         "The others are false: 3070 &lt; 3700, 9999 &lt; " + TT + " and 8143 &gt; 8134."),
        ("6999" + LT + "7000", ["4200" + LT + "4020", "999" + GT + "1000", "3850" + LT + "3805"],
         "6999 has 6 thousands and 7000 has 7 thousands, so 6999 &lt; 7000. "
         "The others are false: 4200 &gt; 4020, 999 &lt; 1000 and 3850 &gt; 3805."),
        ("8500" + GT + "8050", ["2360" + GT + "2630", "6040" + LT + "640", "1007" + GT + "1070"],
         "Same thousands. Hundreds: 5 hundreds &gt; 0 hundreds, so 8500 &gt; 8050. "
         "The others are false: 2360 &lt; 2630, 6040 &gt; 640 and 1007 &lt; 1070."),
    ]
    assert 5602 < 5620 and not 3070 > 3700 and not 8143 < 8134 and 6999 < 7000 and not 4200 < 4020
    assert not 3850 < 3805 and 8500 > 8050 and not 2360 > 2630 and not 6040 < 640 and not 1007 > 1070
    tr = [mcq("Which is true?", a, w, e, rnd) for a, w, e in true]

    def order_q(nums, desc, wrong, e):
        ans = sorted(nums, reverse=desc)
        js = lambda l: ", ".join(c(x) for x in l)
        for w in wrong:
            assert sorted(w) == sorted(nums) and w != ans
        return mcq("Put %s in order from %s." % (js(nums[:-1]) + " and " + c(nums[-1]),
                                                 "greatest to least" if desc else "least to greatest"),
                   js(ans), [js(w) for w in wrong], e, rnd)

    orders = [
        order_q([5620, 5062, 5206], False, [[5620, 5206, 5062], [5206, 5062, 5620], [5062, 5620, 5206]],
                "All have 5 thousands. Hundreds: 0 &lt; 2 &lt; 6. Order: 5062, 5206, 5620."),
        order_q([8710, 10000, 8170, 8701], True,
                [[8710, 8701, 8170, 10000], [10000, 8701, 8710, 8170], [8170, 8701, 8710, 10000]],
                TT + " has 5 digits, so it is the greatest. 8170 has the fewest hundreds. "
                "8710 &gt; 8701 because 1 ten &gt; 0 tens. Order: " + TT + ", 8710, 8701, 8170."),
        order_q([3805, 3085, 3580, 3508], False,
                [[3085, 3508, 3805, 3580], [3805, 3580, 3508, 3085], [3085, 3580, 3508, 3805]],
                "All have 3 thousands. Hundreds: 0 &lt; 5 &lt; 8, so 3085 is the least and 3805 is the greatest. "
                "3508 &lt; 3580 because 0 tens &lt; 8 tens. Order: 3085, 3508, 3580, 3805."),
        order_q([7340, 734, 7034, 7403], True,
                [[7403, 7340, 734, 7034], [734, 7034, 7340, 7403], [7340, 7403, 7034, 734]],
                "734 has only 3 digits, so it is the least. The others have 7 thousands. "
                "Hundreds: 4 &gt; 3 &gt; 0. Order: 7403, 7340, 7034, 734."),
    ]
    between = [
        mcq_n("Which number is between 6200 and 6300?", 6248, [6320, 6028, 2648],
              "A number between 6200 and 6300 has 6 thousands and 2 hundreds. 6248 fits. "
              "6320 is too big, 6028 is too small and 2648 is too small.", rnd),
        mcq_n("Which number is between 4900 and 5000?", 4960, [5960, 4096, 5004],
              "A number between 4900 and 5000 has 4 thousands and 9 hundreds. 4960 fits. "
              "5960 and 5004 are more than 5000, and 4096 is less than 4900.", rnd),
    ]
    assert 6200 < 6248 < 6300 and not 6200 < 2648 and 4900 < 4960 < 5000
    dig = [
        mcq_n("Use the digits 6, 0, 3 and 8 once each. What is the greatest number you can make?", 8630,
              [8603, 6830, 8036],
              "Put the biggest digit in the thousands place, then the next biggest: 8, 6, 3, 0. That is 8630.", rnd),
        mcq_n("Use the digits 7, 0, 4 and 1 once each. What is the least 4-digit number you can make?", 1047,
              [147, 1074, 1407],
              "A 4-digit number cannot start with 0. Put the smallest other digit first: 1. Then 0, 4, 7: 1047. "
              "(0147 is just 147, which has only 3 digits.)", rnd),
    ]
    than = [
        mcq_n("Which number is greater than 6380?", 6803, [6308, 6038, 6379],
              "Same thousands. Hundreds: 6803 has 8 hundreds and 6380 has 3 hundreds. So 6803 &gt; 6380. "
              "The others are all less than 6380.", rnd),
        mcq_n("Which number is less than 8000?", 7999, [8001, 8010, 8100],
              "7999 has only 7 thousands. The others have 8 thousands and more, so they are greater than 8000.", rnd),
        mcq_n("Which number is greater than 9980?", 10000, [9908, 9089, 998],
              TT + " is 20 more than 9980. 9908 and 9089 have fewer tens or hundreds, and 998 has "
              "only 3 digits.", rnd),
    ]
    assert 6803 > 6380 > 6379 and 9980 + 20 == 10000
    order = (pick[:2] + than[:1] + tr[:1] + between[:1] + orders[:1] + pick[2:3] + dig[:1] + than[1:2] + tr[1:2]
             + pick[3:4] + orders[1:2] + between[1:] + pick[4:5] + dig[1:] + orders[2:3] + tr[2:] + than[2:]
             + pick[5:] + orders[3:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers to 10" + NB + "000", "items": order}


# ============================================================ set 5: number lines and numbers in everyday life
def set_lines(rnd, P):
    def nl_q(lo, hi, step, labels, arrow, ans_wrong, e):
        assert arrow not in ans_wrong
        return mcq_n(fig(number_line_svg(lo, hi, step, labels, arrow)) + "What number does the arrow point to?",
                     arrow, ans_wrong, e, rnd)

    nl = [
        nl_q(0, 10000, 1000, [0, 5000, 10000], 3000, [3, 2000, 4000],
             "From 0 to " + TT + " there are 10 jumps, so each mark is 1000. The arrow is 3 marks after 0: "
             "1000, 2000, 3000."),
        nl_q(6000, 7000, 100, [6000, 6500, 7000], 6800, [6080, 6500, 6900],
             "From 6000 to 7000 there are 10 jumps, so each mark is 100. The arrow is 3 marks after 6500: "
             "6600, 6700, 6800. (6080 counts each mark as 10.)"),
        nl_q(2400, 2500, 10, [2400, 2450, 2500], 2430, [2403, 2300, 2440],
             "From 2400 to 2500 there are 10 jumps, so each mark is 10. The arrow is 3 marks after 2400: "
             "2410, 2420, 2430."),
        nl_q(0, 10000, 500, [0, 5000, 10000], 2500, [5000, 500, 2050],
             "From 0 to 5000 there are 10 marks, so each mark is 500. The arrow is 5 marks after 0: "
             "500, 1000, 1500, 2000, 2500. (5000 counts each mark as 1000.)"),
        nl_q(9000, 10000, 100, [9000, 9500, 10000], 9900, [9090, 9800, 10000],
             "Each mark is 100. The arrow is 1 mark before " + TT + ", so it points to "
             + TT + " − 100 = 9900."),
        nl_q(3000, 5000, 200, [3000, 4000, 5000], 4600, [4300, 3600, 4800],
             "From 3000 to 4000 there are 5 jumps, so each mark is 200. The arrow is 3 marks after 4000: "
             "4200, 4400, 4600. (4300 counts each mark as 100.)"),
    ]
    assert 10000 - 100 == 9900
    closer = [
        mcq(fig(number_line_svg(7000, 8000, 100, [7000, 7500, 8000], 7820, show="7820"))
            + "Is 7820 closer to 7000 or to 8000?", "8000", ["7000", "7800", "It is exactly halfway"],
            "Halfway between 7000 and 8000 is 7500. 7820 is after 7500, so it is closer to 8000. "
            "(7820 has 7 thousands, but it is only 180 away from 8000.)", rnd),
        mcq(fig(number_line_svg(2300, 2400, 10, [2300, 2350, 2400], 2340, show="2340"))
            + "Is 2340 closer to 2300 or to 2400?", "2300", ["2400", "2350", "It is exactly halfway"],
            "Halfway between 2300 and 2400 is 2350. 2340 is before 2350, so it is closer to 2300: "
            "it is 40 away from 2300 and 60 away from 2400.", rnd),
    ]
    assert 8000 - 7820 < 7820 - 7000 and 2340 - 2300 < 2400 - 2340
    count = [
        mcq_n("Count on by 1000s: 2350, 3350, 4350, ☐. What number comes next?", 5350, [4450, 4360, 6350],
              "Counting by 1000s changes only the thousands digit: 2, 3, 4, then 5. The next number is 5350.", rnd),
        mcq_n("Count back by 100s: 6230, 6130, 6030, ☐. What number comes next?", 5930, [6020, 5030, 6930],
              "Each number is 100 less. 6030 has 0 hundreds, so trade 1 thousand for 10 hundreds: "
              "6030 − 100 = 5930.", rnd),
    ]
    assert 6030 - 100 == 5930
    a, _, _ = P.next()
    b, _, _ = P.next()
    c1, s1, h1 = P.next()
    wp = [
        mcq_n("A hockey arena in Kingston has 6248 seats. What is the value of the 2 in 6248?", 200, [2, 20, 2000],
              "The 2 is in the hundreds place, so it is worth 2 hundreds = 200.", rnd),
        mcq_n("A school library in Ottawa has four thousand six hundred eight books. Which number is that?",
              4608, [468, 4680, 40608],
              "4 thousands, 6 hundreds, 0 tens and 8 ones: 4608. Write 0 for the empty tens place.", rnd),
        mcq("Volunteers counted 1209 loons on lakes in Muskoka. How do you write 1209 in words?",
            "one thousand two hundred nine",
            ["one thousand two hundred ninety", "one hundred twenty-nine", "twelve thousand nine"],
            "1209 is 1 thousand, 2 hundreds, 0 tens and 9 ones: one thousand two hundred nine. "
            "The 9 is in the ones place, so it is nine, not ninety.", rnd),
        mcq("A sugar bush made 3460 L of maple syrup this spring. Which shows 3460 in expanded form?",
            "3000 + 400 + 60", ["3000 + 400 + 6", "300 + 40 + 6", "3 + 4 + 6 + 0"],
            "3460 is 3 thousands, 4 hundreds, 6 tens and 0 ones: 3000 + 400 + 60. "
            "The 6 is in the tens place, so it is worth 60.", rnd),
        mcq_n("Students at a school in Hamilton raised $2700 for the Terry Fox Run. The money is all in $100 bills. "
              "How many $100 bills is that?", 27, [7, 2, 270],
              "2700 = 27 hundreds, because 27 × 100 = 2700. So there are 27 bills of $100. "
              "(7 is only the hundreds digit.)", rnd),
        mcq("%s's family drove 2085 km on a summer road trip. %s's family drove 2058 km. Who drove farther?"
            % (a, b), "%s's family" % a, ["%s's family" % b, "They drove the same distance", "You cannot tell"],
            "Both numbers have 2 thousands and 0 hundreds. Tens: 8 tens &gt; 5 tens, so 2085 &gt; 2058. "
            "The numbers use the same digits, but the places are different.", rnd),
        mcq_n("A school in Mississauga bought 3 boxes of 1000 stickers, 6 packs of 10 stickers and 4 single stickers. "
              "How many stickers is that?", 3064, [364, 3604, 30064],
              "3 thousands, 0 hundreds, 6 tens and 4 ones: 3000 + 60 + 4 = 3064. "
              "There are no hundreds, so write 0 in the hundreds place.", rnd),
        mcq("Four schools collected cans for a food drive: Maple School 1305, Pine School 1530, "
            "Birch School 1350 and Cedar School 1053. Which school collected the most cans?",
            "Pine School", ["Maple School", "Birch School", "Cedar School"],
            "All four numbers have 1 thousand. Compare the hundreds: 1530 has 5 hundreds, 1350 and 1305 have 3, "
            "and 1053 has 0. So 1530 is the greatest. Pine School collected the most.", rnd),
        mcq_n("%s's town had a Canada Day fireworks show. More than 4500 people came, but fewer than 4600. "
              "Which number could be how many people came?" % c1, 4562, [4652, 4056, 5462],
              "The number must be between 4500 and 4600, so it has 4 thousands and 5 hundreds. 4562 fits. "
              "4652 and 5462 are too big, and 4056 is too small.", rnd),
        mcq_n("A ski hill sold 9995 lift tickets this winter. On the last day it sold 5 more. "
              "How many lift tickets did it sell in all?", 10000, [1000, 9990, 9996],
              "9995 + 5 = 10" + NB + "000. 10 ones make 1 ten, 10 tens make 1 hundred, 10 hundreds make "
              "1 thousand and 10 thousands make 10" + NB + "000. The answer has 5 digits.", rnd),
    ]
    assert 3000 + 60 + 4 == 3064 and 2085 > 2058 and 27 * 100 == 2700 and 9995 + 5 == 10000
    assert max([1305, 1530, 1350, 1053]) == 1530 and 4500 < 4562 < 4600 and 4000 + 600 + 8 == 4608
    order = (nl[:2] + count[:1] + nl[2:3] + closer[:1] + nl[3:4] + count[1:] + nl[4:5] + closer[1:] + nl[5:] + wp)
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Number lines and numbers in everyday life", "items": order}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)



def body_html():
    tt = "10" + NB + "000"
    return (
        "<h2>Thousands, hundreds, tens and ones</h2>"
        "<p>A 4-digit number has four places: <b>thousands</b>, <b>hundreds</b>, <b>tens</b> and <b>ones</b>. "
        "10 ones make 1 ten. 10 tens make 1 hundred. 10 hundreds make 1 thousand. "
        "10 thousands make " + tt + ".</p>"
        "<figure class='sn-fig'>" + blocks_svg(3, 2, 0, 5, labels=True) +
        "<figcaption>Base ten blocks for 3205. A big cube is 1000, a flat is 100, a rod is 10 and a small cube is 1. "
        "There are no rods, so the tens digit is 0.</figcaption></figure>"
        "<h2>The value of a digit</h2>"
        "<p>The place tells you what a digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(4053, hi=1) +
        "<figcaption>In 4053 the 5 is in the tens place. Its value is 5 tens, or 50.</figcaption></figure>"
        "<p>If a place is empty, write <b>0</b> there. The 0 keeps the other digits in the right places.</p>" +
        ex("Write the number", "Write “four thousand fifty-three” as a number.",
           "4 thousands, 0 hundreds, 5 tens, 3 ones. Write 4, 0, 5, 3.", "4053 (not 453 or 40" + NB + "053)") +
        "<h2>Expanded form and decomposing</h2>"
        "<p><b>Expanded form</b> shows the value of each digit: 4361 = 4000 + 300 + 60 + 1. "
        "You can also decompose a number another way. Trade 1 hundred for 10 tens.</p>" +
        ex("Decompose", "Decompose 4361 in two ways.",
           "4 thousands, 3 hundreds, 6 tens and 1 one. Or 4 thousands, 2 hundreds, 16 tens and 1 one.",
           "4000 + 300 + 60 + 1 = 4000 + 200 + 160 + 1") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 5-digit number is greater than a 4-digit number. "
        "If both have 4 digits, compare the thousands, then the hundreds, then the tens, then the ones.</p>" +
        ex("Compare", "5602 ☐ 5620", "Thousands: 5 = 5. Hundreds: 6 = 6. Tens: 0 tens &lt; 2 tens.",
           "5602 &lt; 5620") +
        "<p>&gt; means “is greater than”. &lt; means “is less than”. The open side faces the greater number.</p>"
        "<h2>Number lines</h2>"
        "<p>Before you read a number line, work out the size of each jump. "
        "Count the jumps between two labelled numbers.</p>"
        "<figure class='sn-fig'>" + number_line_svg(6000, 7000, 100, [6000, 6500, 7000], 6800, show="6800") +
        "<figcaption>From 6000 to 7000 there are 10 jumps, so each mark is 100. The arrow is 3 marks after 6500: "
        "6800.</figcaption></figure>"
        "<h2>Numbers in everyday life</h2>"
        "<p>We use numbers to " + tt + " to count seats in a hockey arena, books in a library, "
        "kilometres on a road trip and dollars raised for the Terry Fox Run. "
        "Read the number first, then think about what each digit means.</p>" +
        table(["Number", "Where you might see it", "In words"], [
            ["6248", "seats in a hockey arena", "six thousand two hundred forty-eight"],
            ["2085", "kilometres on a road trip", "two thousand eighty-five"],
            ["$2700", "money raised for a charity run", "two thousand seven hundred dollars"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Leaving out the zero (four thousand fifty-three = 453)", "Write 0 for the empty hundreds place: 4053"],
            ["Writing an extra zero (4053 = 40" + NB + "053)", "A number in the thousands has 4 digits"],
            ["Reading the digit, not its value (the 5 in 4053 is 5)", "The 5 is in the tens place: 50"],
            ["Writing 14 hundreds inside the number (3 thousands, 14 hundreds = 31" + NB + "400)",
             "14 hundreds = 1400, so 3000 + 1400 = 4400"],
            ["Comparing the first digits only (9989 &gt; " + tt + ")", "Count the digits first: " + tt + " &gt; 9989"],
            ["Thinking every mark on a number line is 1, 10 or 100",
             "Work out the jump first: 0 to 5000 in 10 jumps means 500 each"],
        ])
    )


FAQ = [
    {"q": "What number skills are in the Grade 4 Ontario math curriculum?",
     "a": "Grade 4 students read, represent, compose and decompose whole numbers up to and including 10 000 (B1.1) "
          "and compare and order them (B1.2). They also describe how these numbers are used in everyday life."},
    {"q": "How do you write 10 000 in Canada?",
     "a": "Ontario math resources write 4-digit numbers with no space (4053) and put a space between groups of three "
          "digits from 5 digits on (10 000). Commas are not used."},
    {"q": "How can I help my child with place value to 10 000 at home?",
     "a": "Point out big numbers in daily life, such as arena seats, kilometres on a trip or prices, and ask what each "
          "digit is worth. Ask your child to say the number in two ways, for example 4361 as 43 hundreds and 61 ones."},
    {"q": "Do Grade 4 students write EQAO?",
     "a": "No. In Ontario, the EQAO math assessment is written in Grade 3 and Grade 6. Grade 4 place value builds on "
          "Grade 3 and prepares students for Grade 6."},
]


def mark_large(u, pattern):
    """Tag wide pictures (base ten blocks, place value charts, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(44802)
    P = People(random.Random(448021))
    sets = [set_blocks(rnd), set_value(rnd), set_decompose(rnd), set_compare(rnd), set_lines(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "numbers-to-10000", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 10 000: Place Value, Comparing and Number Lines",
        "seo_title": "Grade 4 Numbers to 10 000 Math Worksheets: Free, with Answer Key (Ontario)",
        "short_title": "Numbers to 10 000",
        "domain": "Number",
        "standard_code": "Grade 4: B1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compose, and decompose whole numbers up to and including 10 000, using "
                         "appropriate tools and strategies, and describe various ways they are used in everyday life",
        "meta_desc": "Free Grade 4 math worksheets on numbers to 10 000 for the Ontario curriculum: base ten blocks, "
                     "the value of each digit, expanded form, comparing and ordering, and number lines. "
                     "100 questions with an answer key.",
        "key_big": "The place of a digit tells you its value. The 5 in 4053 is worth 50.",
        "key_sub": "Write 0 for an empty place: four thousand fifty-three is 4053, not 453 or 40 053. "
                   "To compare, count the digits first, then compare from the left.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    sp = lambda t: t.replace("10 000", "10" + NB + "000").replace("40 053", "40" + NB + "053")
    for k in ("title", "short_title", "key_sub", "seo_title", "meta_desc", "standard_text"):
        u[k] = sp(u[k])
    u["faq"] = [{"q": sp(f["q"]), "a": sp(f["a"])} for f in FAQ]
    return mark_large(u, "(base ten blocks|place value chart|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
