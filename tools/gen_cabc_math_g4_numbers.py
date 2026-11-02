# -*- coding: utf-8 -*-
"""
BC Grade 4 Math: Numbers to 10 000 (BC Mathematics Curriculum, Grade 4 Content: Number concepts to 10 000)
  python3 tools/gen_cabc_math_g4_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
BC number style: 4-digit numbers have no separator (4053); 5 or more digits use a no-break space
between groups of three (10 000). Never commas. Number words without "and" (four thousand fifty-three).
Wrong answers come from real mistakes: leaving out a zero (4053 -> 453), adding a zero or writing each
spoken part (4053 -> 40 053), reading the digit instead of its value (the 5 in 4053 is 5),
writing a regrouped number inside the numeral (2 thousands, 15 hundreds -> 21 530),
comparing the first digit only when the numbers have different lengths, and rounding to the wrong place.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
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

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand"]


# ------------------------------------------------------------ helpers
def c(n):
    """BC style: 4053 stays 4053; 10000 -> 10 000 with a no-break space."""
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
            (2, 3, 4, 5, [14, 5432, 2354]),             # counted pieces, read backwards, tens/ones swapped
            (1, 4, 0, 6, [146, 11, 10406]),            # left out the zero, counted pieces, extra zero
            (3, 0, 5, 2, [352, 3502, 10]),              # left out the zero, zero in the wrong place, counted pieces
            (2, 1, 6, 0, [216, 2106, 9]),
            (4, 0, 5, 3, [453, 40053, 4530]),           # 4053 -> 453 or 40 053
            (1, 3, 2, 7, [13, 7231, 1372]),
            (3, 2, 0, 0, [32, 3020, 5]),
            (2, 0, 0, 8, [28, 2080, 20008])]:
        n = 1000 * th + 100 * h + 10 * t + o
        e = blocks_e(th, h, t, o) + " Start with the big cubes, then the flats, rods and small cubes."
        what.append(mcq_n(fig(blocks_svg(th, h, t, o)) + "What number do the base ten blocks show?", n, wrong, e, rnd))
    how = [
        mcq_n(fig(blocks_svg(2, 4, 6, 1)) + "How many tens are there?", 6, [4, 1, 60],
              "Each rod is 1 ten. There are 6 rods, so there are 6 tens. The number is 2461.", rnd),
        mcq_n(fig(blocks_svg(1, 3, 0, 8)) + "How many hundreds are there?", 3, [1, 8, 300],
              "Each flat is 1 hundred. There are 3 flats, so there are 3 hundreds. The number is 1308.", rnd),
        mcq_n(fig(blocks_svg(2, 3, 5, 4)) + "How many thousands are there?", 2, [3, 5, 2000],
              "Each big cube is 1 thousand. There are 2 big cubes, so there are 2 thousands. "
              "Their value is 2000, but the question asks how many. The number is 2354.", rnd),
    ]
    match = []
    for th, h, t, o in [(2, 5, 3, 6), (3, 1, 4, 2)]:
        wrong = [thto(o, t, h, th), thto(th, t, h, o), thto(h, th, t, o)]
        match.append(mcq(fig(blocks_svg(th, h, t, o)) + "Which matches the blocks?", thto(th, h, t, o), wrong,
                         "Count each kind of block: %s. The number is %s." % (thto(th, h, t, o),
                                                                              c(1000 * th + 100 * h + 10 * t + o)), rnd))
    more = [
        mcq_n(fig(blocks_svg(2, 9, 4, 5)) + "Add 1 more flat. What number is it now?", 3045, [21045, 2955, 3945],
              "The blocks show 2945. Add 1 flat: now there are 10 flats. Trade 10 flats for 1 big cube. "
              "That is 3 thousands, 0 hundreds, 4 tens and 5 ones: 3045.", rnd),
        mcq_n(fig(blocks_svg(1, 4, 9, 6)) + "Add 1 more rod. What number is it now?", 1506, [14106, 1497, 2496],
              "The blocks show 1496. Add 1 rod: now there are 10 rods. Trade 10 rods for 1 flat. "
              "That is 1 thousand, 5 hundreds, 0 tens and 6 ones: 1506.", rnd),
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
        mcq_n("Write “seven thousand eight hundred six” as a number.", 7806, [786, 7860, 7086],
              "7 thousands, 8 hundreds, 0 tens and 6 ones: 7806. The 6 is ones, so it goes last. "
              "Write 0 for the empty tens place.", rnd),
    ]
    which = mcq_n("Which number has 3 thousands, 0 hundreds, 5 tens and 2 ones?", 3052, [352, 3502, 30052],
                  "Write the digits in order: thousands 3, hundreds 0, tens 5, ones 2. That is 3052.", rnd)
    for v, w in [(2945 + 100, 3045), (1496 + 10, 1506), (10 * 100, 1000), (10 * 1000, 10000)]:
        assert v == w
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
    for n, i in [(4728, 3), (6095, 1), (3517, 2), (2864, 1), (9302, 2)]:
        chart.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?",
                           digit(n, i) * 10 ** i, value_wrong(n, i), value_e(n, i, True), rnd))
    plain = []
    for n, i in [(3825, 2), (7409, 3), (5163, 1), (2071, 1), (6538, 2), (9246, 3)]:
        d = digit(n, i)
        plain.append(mcq_n("What is the value of the digit %d in %s?" % (d, c(n)), d * 10 ** i,
                           value_wrong(n, i), value_e(n, i), rnd))
    place = []
    for n, i in [(5381, 2), (8047, 3), (2609, 1)]:
        d = digit(n, i)
        others = [digit(n, x) for x in range(4) if x != i]
        place.append(mcq_n("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, others,
                           "%s has %s. The %s digit is %d." % (c(n), thto_n(n), PL[i], d), rnd))
    has = []
    for d, i, nums in [(7, 2, [3725, 7325, 3275, 3257]), (4, 1, [8143, 4813, 8413, 8134]),
                       (6, 3, [6950, 9650, 9506, 9560])]:
        good = [x for x in nums if digit(x, i) == d]
        assert len(good) == 1
        good = good[0]
        has.append(mcq_n("Which number has %s %d in the %s place?" % ("an" if d == 8 else "a", d, PL[i]),
                         good, [x for x in nums if x != good],
                         "In %s the %d is in the %s place, so it is worth %s."
                         % (c(good), d, PL[i], c(d * 10 ** i)), rnd))
    more = [
        mcq_n("What number is 1000 more than 4053?", 5053, [4153, 4063, 14053],
              "1000 more changes only the thousands digit: 4 thousands → 5 thousands. 4053 + 1000 = 5053.", rnd),
        mcq_n("What number is 100 less than 6025?", 5925, [6925, 6015, 5025],
              "There are 0 hundreds, so trade 1 thousand for 10 hundreds: 5 thousands, 10 hundreds. "
              "Take away 1 hundred: 5 thousands, 9 hundreds, 2 tens, 5 ones = 5925.", rnd),
        mcq_n("What number is 10 more than 3995?", 4005, [4095, 3996, 39105],
              "3995 has 9 tens. 10 more makes 10 tens, which is 1 hundred. That makes 10 hundreds, which is "
              "1 thousand. 3995 + 10 = 4005.", rnd),
    ]
    assert 4053 + 1000 == 5053 and 6025 - 100 == 5925 and 3995 + 10 == 4005
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
            (4053, [(4, 0, 5, 3), (4000, 500, 3), (400, 50, 3)]),
            (7208, [(7, 2, 0, 8), (7000, 200, 80), (700, 20, 8)]),
            (3640, [(3, 6, 4, 0), (3000, 600, 4), (300, 60, 40)]),
            (9015, [(9, 0, 1, 5), (9000, 100, 5), (900, 10, 5)]),
            (6372, [(6, 3, 7, 2), (6000, 300, 7, 2), (600, 30, 70, 2)])]:
        parts = [digit(n, i) * 10 ** i for i in range(3, -1, -1) if digit(n, i)]
        assert sum(parts) == n
        for w in wrong:
            assert sum(w) != n or len(w) == 4 and w[0] < 10
        std.append(mcq("What is %s in expanded form?" % c(n), exp_str(*parts), [exp_str(*w) for w in wrong],
                       "%s is %s. Write the value of each digit and skip the zeros: %s = %s."
                       % (c(n), thto_n(n), c(n), exp_str(*parts)), rnd))
    back = []
    for parts, wrong in [((4000, 300, 6), [436, 4360, 40306]), ((6000, 20, 5), [625, 6250, 60025]),
                         ((8000, 900, 4), [894, 8940, 80904]), ((5000, 7), [57, 5070, 5700]),
                         ((300, 2000, 40, 1), [3241, 2431, 2041])]:
        n = sum(parts)
        e = "%s = %s. That is %s." % (exp_str(*parts), c(n), thto_n(n))
        if 0 in [digit(n, i) for i in range(3)]:
            e += " Write 0 for each empty place, so the number has 4 digits."
        if parts[0] < parts[1]:
            e += " The parts are not in order, so put each digit in its own place."
        back.append(mcq_n("What number is %s?" % exp_str(*parts), n, wrong, e, rnd))
    regroup = [
        mcq_n("3452 = 3 thousands, 3 hundreds, ☐ tens and 2 ones. What number goes in the box?", 15, [5, 14, 6],
              "Only 3 hundreds are used, so 1 hundred becomes 10 tens. 10 + 5 = 15 tens. "
              "Check: 3000 + 300 + 150 + 2 = 3452.", rnd),
        mcq_n("2615 = 1 thousand, ☐ hundreds, 1 ten and 5 ones. What number goes in the box?", 16, [6, 2, 26],
              "Only 1 thousand is used, so 1 thousand becomes 10 hundreds. 10 + 6 = 16 hundreds. "
              "Check: 1000 + 1600 + 10 + 5 = 2615.", rnd),
        mcq("Which is another way to make 4270?", "3 thousands, 12 hundreds and 7 tens",
            ["4 thousands, 12 hundreds and 7 tens", "3 thousands, 2 hundreds and 17 tens",
             "3 thousands, 12 hundreds and 70 tens"],
            "Trade 1 thousand for 10 hundreds: 3000 + 1200 + 70 = 4270. "
            "(The others make 5270, 3370 and 4900.)", rnd),
        mcq("Which is the same as 5308?", "53 hundreds and 8 ones",
            ["53 hundreds and 8 tens", "5 hundreds, 3 tens and 8 ones", "530 hundreds and 8 ones"],
            "5 thousands = 50 hundreds, so 5308 has 50 + 3 = 53 hundreds and 8 ones. 5300 + 8 = 5308.", rnd),
    ]
    assert 3000 + 300 + 150 + 2 == 3452 and 1000 + 1600 + 15 == 2615
    assert (3000 + 1200 + 70, 4000 + 1200 + 70, 3000 + 200 + 170, 3000 + 1200 + 700) == (4270, 5270, 3370, 4900)
    assert (5300 + 8, 5300 + 80, 538, 53000 + 8) == (5308, 5380, 538, 53008)
    hund = [
        mcq_n("34 hundreds is the same as what number?", 3400, [340, 34, 34000],
              "1 hundred = 100, so 34 hundreds = 34 × 100 = 3400. That is 3 thousands and 4 hundreds.", rnd),
        mcq_n("How many hundreds are in 5200?", 52, [2, 5, 520],
              "5 thousands = 50 hundreds. 50 + 2 = 52 hundreds. Check: 52 × 100 = 5200. "
              "(2 is only the hundreds digit.)", rnd),
        mcq_n("How many tens are in 1250?", 125, [5, 12, 1250],
              "1250 = 1000 + 200 + 50 = 100 tens + 20 tens + 5 tens = 125 tens. Check: 125 × 10 = 1250.", rnd),
    ]
    comp = [
        mcq_n("What number is 2 thousands, 15 hundreds and 3 tens?", 3530, [21530, 2530, 3503],
              "15 hundreds = 1500. 2000 + 1500 + 30 = 3530. Do not write 15 inside the number.", rnd),
        mcq_n("What number is 4 thousands, 12 hundreds and 6 ones?", 5206, [41206, 4206, 4126],
              "12 hundreds = 1200 = 1 thousand and 2 hundreds. 4000 + 1200 + 6 = 5206.", rnd),
        mcq_n("What number is 6 thousands, 3 hundreds, 14 tens and 2 ones?", 6442, [63142, 6342, 6432],
              "14 tens = 140 = 1 hundred and 4 tens. 6000 + 300 + 140 + 2 = 6442.", rnd),
    ]
    assert 2000 + 1500 + 30 == 3530 and 4000 + 1200 + 6 == 5206 and 6000 + 300 + 140 + 2 == 6442
    order = (std[:2] + back[:2] + std[2:3] + back[2:3] + hund[:1] + std[3:4] + back[3:4] + regroup[:1]
             + hund[1:2] + std[4:] + back[4:] + regroup[1:2] + hund[2:] + comp[:1] + regroup[2:3]
             + comp[1:2] + regroup[3:] + comp[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Expanded form and decomposing in different ways", "items": order}


# ============================================================ set 4: compare and order
LT, GT = " &lt; ", " &gt; "


def first_diff(a, b):
    for i in range(3, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def set_compare(rnd):
    pick = []
    for kind, nums in [("greatest", [4053, 4503, 4350, 4305]), ("least", [7089, 7809, 7098, 7890]),
                       ("greatest", [9876, 10000, 9999, 999]), ("least", [3120, 312, 3012, 1302]),
                       ("greatest", [6060, 6606, 6600, 6066]), ("least", [5432, 5423, 5342, 5324])]:
        ans = max(nums) if kind == "greatest" else min(nums)
        rest = [x for x in nums if x != ans]
        if ans == 10000:
            e = ("10" + NB + "000 has 5 digits. All the others have 4 digits or fewer, so 10" + NB
                 + "000 is the greatest, even though 9999 starts with a 9.")
        elif ans == 312:
            e = "312 has only 3 digits. The others have 4 digits, so they are all greater. 312 is the least."
        else:
            srt = sorted(nums, reverse=(kind == "greatest"))
            i = first_diff(srt[0], srt[1])
            e = ("All four numbers have the same number of digits. Compare from the left. "
                 "%s and %s are the closest: they first differ in the %s place, %d %s %d. So %s is the %s."
                 % (c(srt[0]), c(srt[1]), PL[i], digit(srt[0], i), "&gt;" if kind == "greatest" else "&lt;",
                    digit(srt[1], i), c(ans), kind))
        pick.append(mcq_n("Which number is the %s?" % kind, ans, rest, e, rnd))
    true = [
        ("4503" + LT + "4530", ["6080" + GT + "6800", "9999" + GT + "10" + NB + "000", "7021" + LT + "7012"],
         "4503 and 4530 have the same thousands and hundreds. Tens: 0 tens &lt; 3 tens, so 4503 &lt; 4530. "
         "The others are false: 6080 &lt; 6800, 9999 &lt; 10" + NB + "000 and 7021 &gt; 7012."),
        ("3999" + LT + "4000", ["5100" + LT + "5010", "999" + GT + "1000", "2760" + LT + "2706"],
         "3999 has 3 thousands and 4000 has 4 thousands, so 3999 &lt; 4000. "
         "The others are false: 5100 &gt; 5010, 999 &lt; 1000 and 2760 &gt; 2706."),
        ("7600" + GT + "7060", ["1450" + GT + "1540", "8030" + LT + "830", "9008" + GT + "9080"],
         "Same thousands. Hundreds: 6 hundreds &gt; 0 hundreds, so 7600 &gt; 7060. "
         "The others are false: 1450 &lt; 1540, 8030 &gt; 830 and 9008 &lt; 9080."),
    ]
    assert 4503 < 4530 and not 6080 > 6800 and not 7021 < 7012 and 3999 < 4000 and not 5100 < 5010
    assert not 2760 < 2706 and 7600 > 7060 and not 1450 > 1540 and not 8030 < 830 and not 9008 > 9080
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
        order_q([4530, 4053, 4305], False, [[4530, 4305, 4053], [4305, 4053, 4530], [4053, 4530, 4305]],
                "All have 4 thousands. Hundreds: 0 &lt; 3 &lt; 5. Order: 4053, 4305, 4530."),
        order_q([9810, 10000, 9180, 9801], True,
                [[9810, 9801, 9180, 10000], [10000, 9801, 9810, 9180], [9180, 9801, 9810, 10000]],
                "10" + NB + "000 has 5 digits, so it is the greatest. 9180 has the fewest hundreds. "
                "9810 &gt; 9801 because 1 ten &gt; 0 tens. Order: 10" + NB + "000, 9810, 9801, 9180."),
        order_q([2706, 2076, 2670, 2607], False,
                [[2076, 2607, 2706, 2670], [2706, 2670, 2607, 2076], [2076, 2670, 2607, 2706]],
                "All have 2 thousands. Hundreds: 0 &lt; 6 &lt; 7, so 2076 is the least and 2706 is the greatest. "
                "2607 &lt; 2670 because 0 tens &lt; 7 tens. Order: 2076, 2607, 2670, 2706."),
        order_q([6450, 645, 6045, 6504], True,
                [[6504, 6450, 645, 6045], [645, 6045, 6450, 6504], [6450, 6504, 6045, 645]],
                "645 has only 3 digits, so it is the least. The others have 6 thousands. "
                "Hundreds: 5 &gt; 4 &gt; 0. Order: 6504, 6450, 6045, 645."),
    ]
    between = [
        mcq_n("Which number is between 3400 and 3500?", 3462, [3540, 3046, 4350],
              "A number between 3400 and 3500 has 3 thousands and 4 hundreds. 3462 fits. "
              "3540 is too big, 3046 is too small and 4350 is too big.", rnd),
        mcq_n("Which number is between 8900 and 9000?", 8950, [9800, 8090, 9005],
              "A number between 8900 and 9000 has 8 thousands and 9 hundreds. 8950 fits. "
              "9800 and 9005 are more than 9000, and 8090 is less than 8900.", rnd),
    ]
    dig = [
        mcq_n("Use the digits 7, 0, 4 and 9 once each. What is the greatest number you can make?", 9740,
              [9704, 7940, 9047],
              "Put the biggest digit in the thousands place, then the next biggest: 9, 7, 4, 0. That is 9740.", rnd),
        mcq_n("Use the digits 5, 0, 8 and 2 once each. What is the least 4-digit number you can make?", 2058,
              [258, 2085, 2508],
              "A 4-digit number cannot start with 0. Put the smallest other digit first: 2. Then 0, 5, 8: 2058. "
              "(0258 is just 258, which has only 3 digits.)", rnd),
    ]
    than = [
        mcq_n("Which number is greater than 7450?", 7504, [7405, 7045, 7449],
              "Same thousands. Hundreds: 7504 has 5 hundreds and 7450 has 4 hundreds. So 7504 &gt; 7450. "
              "The others are all less than 7450.", rnd),
        mcq_n("Which number is less than 5000?", 4999, [5001, 5010, 5100],
              "4999 has only 4 thousands. The others have 5 thousands and more, so they are greater than 5000.", rnd),
        mcq_n("Which number is greater than 9990?", 10000, [9909, 9099, 999],
              "10" + NB + "000 is 10 more than 9990. 9909 and 9099 have fewer hundreds or tens, and 999 has "
              "only 3 digits.", rnd),
    ]
    assert 3400 < 3462 < 3500 and 8900 < 8950 < 9000 and 9990 + 10 == 10000
    order = (pick[:2] + than[:1] + tr[:1] + between[:1] + orders[:1] + pick[2:3] + dig[:1] + than[1:2] + tr[1:2]
             + pick[3:4] + orders[1:2] + between[1:] + pick[4:5] + dig[1:] + orders[2:3] + tr[2:] + than[2:]
             + pick[5:] + orders[3:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers to 10" + NB + "000", "items": order}


# ============================================================ set 5: number lines, rounding, word problems
PN = {10: "10", 100: "100", 1000: "1000"}


def round_e(n, p):
    r = rnd_to(n, p)
    lo = n // p * p
    hi = lo + p
    i = {10: 0, 100: 1, 1000: 2}[p]
    d = digit(n, i)
    return ("%s is between %s and %s. Look at the %s digit: it is %d, so round %s. %s rounds to %s."
            % (c(n), c(lo), c(hi), PL[i], d, "up" if d >= 5 else "down", c(n), c(r)))


def set_round(rnd):
    nl = [
        mcq_n(fig(number_line_svg(0, 10000, 1000, [0, 5000, 10000], 7000)) + "What number does the arrow point to?",
              7000, [7, 6000, 8000],
              "From 0 to 10" + NB + "000 there are 10 jumps, so each mark is 1000. The arrow is 2 marks after 5000: "
              "6000, 7000.", rnd),
        mcq_n(fig(number_line_svg(3000, 4000, 100, [3000, 3500, 4000], 3600)) + "What number does the arrow point to?",
              3600, [3060, 3500, 3700],
              "From 3000 to 4000 there are 10 jumps, so each mark is 100. The arrow is 1 mark after 3500: 3600. "
              "(3060 counts each mark as 10.)", rnd),
        mcq_n(fig(number_line_svg(5200, 5300, 10, [5200, 5250, 5300], 5270)) + "What number does the arrow point to?",
              5270, [5207, 5700, 5280],
              "From 5200 to 5300 there are 10 jumps, so each mark is 10. The arrow is 2 marks after 5250: "
              "5260, 5270.", rnd),
        mcq_n(fig(number_line_svg(0, 10000, 500, [0, 5000, 10000], 7500)) + "What number does the arrow point to?",
              7500, [7050, 7000, 8500],
              "From 0 to 5000 there are 10 marks, so each mark is 500. The arrow is 5 marks after 5000: "
              "5500, 6000, 6500, 7000, 7500.", rnd),
    ]
    nlr = [
        mcq_n(fig(number_line_svg(4000, 5000, 100, [4000, 4500, 5000], 4380, show="4380"))
              + "Round 4380 to the nearest thousand.", 4000, [5000, 4400, 4300],
              "4380 is before the halfway mark, 4500, so it is closer to 4000. 4380 rounds to 4000. "
              "(4400 is rounding to the nearest hundred.)", rnd),
        mcq_n(fig(number_line_svg(2600, 2700, 10, [2600, 2650, 2700], 2650, show="2650"))
              + "Round 2650 to the nearest hundred.", 2700, [2600, 2650, 3000],
              "2650 is exactly halfway between 2600 and 2700. When a number is halfway, round up: 2700.", rnd),
        mcq_n(fig(number_line_svg(7300, 7400, 10, [7300, 7350, 7400], 7340, show="7340"))
              + "Round 7340 to the nearest hundred.", 7300, [7400, 7350, 7000],
              "7340 is before the halfway mark, 7350, so it is closer to 7300. 7340 rounds to 7300.", rnd),
    ]
    plain = []
    for n, p, wrong in [(4362, 10, [4370, 4400, 4300]), (4362, 100, [4300, 4360, 4000]),
                        (6845, 1000, [6000, 6800, 6900]), (2950, 100, [2900, 2000, 3950]),
                        (8095, 10, [8090, 8000, 8190]), (9600, 1000, [9000, 1000, 9700]),
                        (5555, 100, [5500, 5560, 6000])]:
        r = rnd_to(n, p)
        e = round_e(n, p)
        e += {2950: " 29 hundreds + 1 hundred = 30 hundreds = 3000.",
              8095: " 809 tens + 1 ten = 810 tens = 8100.",
              9600: " 9 thousands + 1 thousand = 10 thousands = 10" + NB + "000."}.get(n, "")
        plain.append(mcq_n("Round %s to the nearest %s." % (c(n), {10: "ten", 100: "hundred", 1000: "thousand"}[p]),
                           r, wrong, e, rnd))
    wp = [
        mcq_n("The Fraser River is about 1375 km long. What is 1375 rounded to the nearest hundred?", 1400,
              [1300, 1380, 1000],
              "1375 is between 1300 and 1400. The tens digit is 7, so round up: 1400 km. "
              "(1380 is rounding to the nearest ten.)", rnd),
        mcq_n("A BC Ferries boat carried 1468 passengers on one trip. About how many is that, to the nearest hundred?",
              1500, [1400, 1470, 2000],
              "1468 is between 1400 and 1500. The tens digit is 6, so round up: about 1500 passengers.", rnd),
        mcq_n("A school in Port Coquitlam raised $3275 in the Terry Fox Run. What is that to the nearest $1000?",
              3000, [4000, 3300, 3280],
              "3275 is between 3000 and 4000. The hundreds digit is 2, so round down: $3000. "
              "($3300 is rounding to the nearest hundred.)", rnd, pre="$"),
        mcq("Volunteers counted salmon in a river on Vancouver Island. They counted 6740 salmon in week 1 and 6470 "
            "salmon in week 2. Which week had more salmon?", "Week 1",
            ["Week 2", "Both weeks were the same", "You cannot tell"],
            "Both numbers have 6 thousands. Hundreds: 7 hundreds &gt; 4 hundreds, so 6740 &gt; 6470. "
            "Week 1 had more. The numbers use the same digits, but the places are different.", rnd),
        mcq_n("By 9 a.m., 9990 people had used a SkyTrain station. Then 10 more people came. "
              "How many people is that now?", 10000, [1000, 9100, 9991],
              "9990 is 999 tens. 10 more is 1 more ten: 999 tens + 1 ten = 1000 tens = 10" + NB + "000. "
              "The answer has 5 digits: 9990 + 10 = 10" + NB + "000.", rnd),
        mcq_n("A school in Surrey bought 2 boxes of 1000 pencils, 5 packs of 10 pencils and 7 more pencils. "
              "How many pencils is that?", 2057, [257, 2507, 20057],
              "2 thousands, 0 hundreds, 5 tens and 7 ones: 2000 + 50 + 7 = 2057. "
              "There are no hundreds, so write 0 in the hundreds place.", rnd),
    ]
    assert rnd_to(1375, 100) == 1400 and rnd_to(1468, 100) == 1500 and rnd_to(3275, 1000) == 3000
    assert 6740 > 6470 and 2000 + 50 + 7 == 2057 and rnd_to(2650, 100) == 2700 and rnd_to(4380, 1000) == 4000
    order = (nl[:2] + plain[:2] + nl[2:3] + nlr[:1] + plain[2:3] + nl[3:] + nlr[1:2] + plain[3:4] + plain[4:5]
             + nlr[2:] + plain[5:] + wp)
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Number lines, rounding and word problems", "items": order}


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
        "<figure class='sn-fig'>" + blocks_svg(2, 4, 0, 6, labels=True) +
        "<figcaption>Base ten blocks for 2406. A big cube is 1000, a flat is 100, a rod is 10 and a small cube is 1. "
        "There are no rods, so the tens digit is 0.</figcaption></figure>"
        "<h2>The value of a digit</h2>"
        "<p>The place tells you what a digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(4053, hi=1) +
        "<figcaption>In 4053 the 5 is in the tens place. Its value is 5 tens, or 50.</figcaption></figure>"
        "<p>If a place is empty, write <b>0</b> there. The 0 keeps the other digits in the right places.</p>" +
        ex("Write the number", "Write “four thousand fifty-three” as a number.",
           "4 thousands, 0 hundreds, 5 tens, 3 ones. Write 4, 0, 5, 3.", "4053 (not 453 or 40" + NB + "053)") +
        "<h2>Expanded form and decomposing</h2>"
        "<p><b>Expanded form</b> shows the value of each digit: 3452 = 3000 + 400 + 50 + 2. "
        "You can also decompose a number another way. Trade 1 hundred for 10 tens.</p>" +
        ex("Decompose", "Decompose 3452 in two ways.",
           "3 thousands, 4 hundreds, 5 tens and 2 ones. Or 3 thousands, 3 hundreds, 15 tens and 2 ones.",
           "3000 + 400 + 50 + 2 = 3000 + 300 + 150 + 2") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 5-digit number is greater than a 4-digit number. "
        "If both have 4 digits, compare the thousands, then the hundreds, then the tens, then the ones.</p>" +
        ex("Compare", "4503 ☐ 4530", "Thousands: 4 = 4. Hundreds: 5 = 5. Tens: 0 tens &lt; 3 tens.",
           "4503 &lt; 4530") +
        "<p>&gt; means “is greater than”. &lt; means “is less than”. The open side faces the greater number.</p>"
        "<h2>Number lines and rounding</h2>"
        "<p>To <b>round</b>, find the two round numbers the number is between. Then see which one is closer. "
        "Look at the digit just to the right of the place you round to. 0 to 4: round down. 5 to 9: round up.</p>"
        "<figure class='sn-fig'>" + number_line_svg(4000, 5000, 100, [4000, 4500, 5000], 4380, show="4380") +
        "<figcaption>4380 is closer to 4000 than to 5000. To the nearest thousand, 4380 rounds to 4000. "
        "To the nearest hundred, it rounds to 4400.</figcaption></figure>" +
        table(["Round 4362 to the nearest …", "Look at", "Answer"], [
            ["ten", "the ones digit, 2: round down", "4360"],
            ["hundred", "the tens digit, 6: round up", "4400"],
            ["thousand", "the hundreds digit, 3: round down", "4000"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Leaving out the zero (four thousand fifty-three = 453)", "Write 0 for the empty hundreds place: 4053"],
            ["Writing an extra zero (4053 = 40" + NB + "053)", "A number in the thousands has 4 digits"],
            ["Reading the digit, not its value (the 5 in 4053 is 5)", "The 5 is in the tens place: 50"],
            ["Writing 15 hundreds inside the number (2 thousands, 15 hundreds = 21" + NB + "500)",
             "15 hundreds = 1500, so 2000 + 1500 = 3500"],
            ["Comparing the first digits only (9876 &gt; " + tt + ")", "Count the digits first: " + tt + " &gt; 9876"],
            ["Rounding to the wrong place (4362 to the nearest hundred = 4360)",
             "Find the hundreds first: 4362 is between 4300 and 4400, so 4400"],
        ])
    )


FAQ = [
    {"q": "What number concepts are in the BC Grade 4 math curriculum?",
     "a": "Grade 4 students in BC work with number concepts to 10 000: reading and writing numbers, place value, "
          "decomposing numbers in different ways, comparing and ordering, and rounding to the nearest 10, 100 and 1000."},
    {"q": "How do you write 10 000 in Canada?",
     "a": "BC math resources write 4-digit numbers with no space (4053) and put a space between groups of three digits "
          "from 5 digits on (10 000). Commas are not used."},
    {"q": "How do you teach rounding to the nearest hundred?",
     "a": "Find the two hundreds the number is between, then look at the tens digit: 0 to 4 rounds down and 5 to 9 "
          "rounds up. A number line helps children see which hundred is closer."},
    {"q": "Is place value on the Grade 4 FSA?",
     "a": "The Grade 4 Foundation Skills Assessment includes numeracy, and number sense such as place value, comparing "
          "and rounding is part of the Grade 4 BC curriculum it is based on."},
]


def mark_large(u, pattern):
    """Tag wide pictures (base ten blocks, place value charts, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(34802)
    sets = [set_blocks(rnd), set_value(rnd), set_decompose(rnd), set_compare(rnd), set_round(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "numbers-to-10000", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 10 000: Place Value, Comparing and Rounding",
        "seo_title": "Grade 4 Numbers to 10 000 Math Worksheets: Free, with Answer Key (BC Curriculum)",
        "short_title": "Numbers to 10 000",
        "domain": "Number",
        "standard_code": "Grade 4: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Number concepts to 10 000",
        "meta_desc": "Free Grade 4 math worksheets on numbers to 10 000 for the BC curriculum: base ten blocks, the value "
                     "of each digit, expanded form, comparing and ordering, number lines and rounding. 100 questions "
                     "with an answer key, good FSA practice.",
        "key_big": "The place of a digit tells you its value. The 5 in 4053 is worth 50.",
        "key_sub": "Write 0 for an empty place: four thousand fifty-three is 4053, not 453 or 40 053. "
                   "To round, find the two round numbers it is between and choose the closer one.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    for k in ("title", "short_title", "key_sub", "seo_title"):
        u[k] = u[k].replace("10 000", "10" + NB + "000").replace("40 053", "40" + NB + "053")
    u["faq"] = [{"q": f["q"].replace("10 000", "10" + NB + "000"), "a": f["a"].replace("10 000", "10" + NB + "000")}
                for f in FAQ]
    u["meta_desc"] = u["meta_desc"].replace("10 000", "10" + NB + "000")
    return mark_large(u, "(base ten blocks|place value chart|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
