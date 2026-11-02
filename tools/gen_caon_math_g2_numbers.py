# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Numbers to 200 (Ontario Mathematics Curriculum 2020, Grade 2: B1.1, also B1.2, B1.3)
  python3 tools/gen_caon_math_g2_numbers.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 2: whole numbers to 200, very short sentences for 7-8 year olds, base ten blocks, dot and craft stick pictures.
Number words are written the Canadian classroom way, without "and" (one hundred five).
Wrong answers come from real mistakes: writing each spoken part (one hundred five -> 1005),
leaving out a zero (105 -> 15), giving the digit instead of its value (the 4 in 145 is 4),
reading the blocks in the wrong order, counting pieces instead of values (1 + 4 + 5 = 10),
writing 14 tens as "14" next to the hundreds, sixteen / sixty, comparing 2- and 3-digit numbers
by the first digit only, and estimates that are far too big or too small.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#c9954c"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

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
    assert 0 <= correct <= 200, (q, correct)
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
    if n < 100:
        return "%s and %s" % (plural(digit(n, 1), 1), plural(digit(n, 0), 0))
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
    h, r = divmod(n, 100)
    if not h:
        return words99(r)
    return ONES[h] + " hundred" + (" " + words99(r) if r else "")


assert words(105) == "one hundred five" and words(152) == "one hundred fifty-two" and words(200) == "two hundred"


# ------------------------------------------------------------ figures
U = 8                      # base ten blocks: a cube = U, a rod = U x 10U, a flat = 10U x 10U (exact 1 : 10 : 100)
G = 8
GG = 22
MG = 8


def blocks_svg(h, t, o, labels=False):
    """Base ten blocks: h flats, t rods, o cubes (cubes in columns of 5)."""
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

    def flats(x, y):
        s = []
        for k in range(h):
            fx = x + k * (F + G)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (fx, y, F, F, FILL, GREEN))
            s += grid(fx, y, F, F, 10, 10)
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
        groups.append((h * F + (h - 1) * G, F, flats, plural(h, 2)))
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


def number_line_svg(lo, hi, step, labels, arrow=None, show=None):
    """Number line lo..hi with a tick every step, numbers under `labels`, a red arrow at `arrow`."""
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
            s.append(text(X(v), Y + 30, "%d" % v, 15, col=GREEN))
        v += step
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


DC = 16                    # dot pictures: one dot per cell of a DC x DC grid, jittered so they look scattered


def dot_field(n, cols, rows, x0, y0, rnd):
    cells = rnd.sample(range(cols * rows), n)
    s = []
    for c in sorted(cells):
        cx = x0 + (c % cols) * DC + DC / 2 + rnd.uniform(-3, 3)
        cy = y0 + (c // cols) * DC + DC / 2 + rnd.uniform(-3, 3)
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (cx, cy, GREEN))
    return s


def dots_svg(n, cols, rows, seed):
    """A box of 10 dots (to help estimate) next to a box of n scattered dots."""
    assert cols * rows >= n * 1.25, (n, cols, rows)
    r = random.Random(seed)
    s = []
    # reference box: 10 dots in a 4 x 4 grid of cells
    rw = 4 * DC + 8
    rh = 4 * DC + 8
    top = 24
    s.append("<rect x='6' y='%d' width='%d' height='%d' rx='6' fill='#fff' stroke='%s' stroke-width='1.6'/>"
             % (top, rw, rh, GREEN))
    s += dot_field(10, 4, 4, 10, top + 4, r)
    s.append(text(6 + rw / 2, 17, "10 dots", 14, col=GREEN))
    bx = 6 + rw + 18
    bw, bh = cols * DC + 8, rows * DC + 8
    s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#fff' stroke='%s' stroke-width='1.6'/>"
             % (bx, top, bw, bh, INK))
    s += dot_field(n, cols, rows, bx + 4, top + 4, r)
    W = bx + bw + 6
    H = top + max(rh, bh) + 6
    return svg_wrap(W, H, "".join(s), "dots to estimate")


def sticks_svg(b, loose):
    """b bundles of 10 craft sticks (with a red band) and loose single sticks."""
    SW, SG, SH = 2.6, 3.0, 64         # stick width, stick pitch, stick height
    BW = 9 * SG + SW                  # bundle width
    BG = 9
    y0 = 8
    s = []
    x = 8
    for k in range(b):
        for j in range(10):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='1' fill='%s' stroke='#8a6430' stroke-width='0.5'/>"
                     % (x + j * SG, y0, SW, SH, STICK))
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='7' fill='%s'/>" % (x - 1.5, y0 + SH / 2 - 3, BW + 3, RED))
        x += BW + BG
    if loose:
        x += 8
        for j in range(loose):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='1' fill='%s' stroke='#8a6430' stroke-width='0.5'/>"
                     % (x + j * 9, y0, SW, SH, STICK))
        x += (loose - 1) * 9 + SW
    else:
        x -= BG
    return svg_wrap(int(x + 9), SH + 2 * y0, "".join(s), "craft sticks in bundles of 10")


def blocks_e(h, t, o):
    n = 100 * h + 10 * t + o
    s = "A flat is 100, a rod is 10 and a small cube is 1. %s make %d." % (cap(hto_n(n)) if h else
                                                                          "%s and %s" % (plural(t, 1), plural(o, 0)), n)
    empty = [PL[i] for i, d in ((1, t), (0, o)) if d == 0]
    if empty:
        s += " There are no %s, so write 0 in the %s place%s." % (" or ".join(empty), " and ".join(empty),
                                                                 "s" if len(empty) > 1 else "")
    return s


# ============================================================ set 1: base ten blocks
def set_blocks(rnd):
    what = []
    for h, t, o, wrong in [(1, 2, 4, [421, 142, 7]), (1, 3, 5, [531, 153, 9]), (1, 5, 0, [15, 105, 6]),
                           (1, 6, 8, [861, 186, 15]), (1, 0, 7, [17, 1007, 170]), (1, 8, 2, [281, 128, 11]),
                           (0, 9, 3, [39, 903, 12]), (1, 1, 9, [911, 191, 11]), (2, 0, 0, [2, 20, 1000]),
                           (1, 4, 6, [641, 164, 11])]:
        n = 100 * h + 10 * t + o
        assert n not in wrong
        e = blocks_e(h, t, o)
        if h:
            e += " Start with the flats, then the rods, then the small cubes."
        what.append(mcq_n(fig(blocks_svg(h, t, o)) + "What number do the blocks show?", n, wrong, e, rnd))
    how = [
        mcq_n(fig(blocks_svg(1, 7, 3)) + "How many tens are there?", 7, [1, 3, 70],
              "Each rod is 1 ten. There are 7 rods, so there are 7 tens. The number is 173.", rnd),
        mcq_n(fig(blocks_svg(1, 4, 9)) + "How many ones are there?", 9, [1, 4, 14],
              "Each small cube is 1 one. There are 9 cubes, so there are 9 ones. The number is 149.", rnd),
        mcq_n(fig(blocks_svg(2, 0, 0)) + "How many hundreds are there?", 2, [20, 200, 0],
              "Each flat is 1 hundred. There are 2 flats, so there are 2 hundreds. The number is 200.", rnd),
    ]
    match = []
    for h, t, o in [(1, 6, 2), (1, 2, 7)]:
        wrong = [hto(o, t, h), hto(h, o, t), hto(t, h, o)]
        match.append(mcq(fig(blocks_svg(h, t, o)) + "Which matches the blocks?", hto(h, t, o), wrong,
                         "Count each kind: %s, %s, %s. That is %s: %d."
                         % (unit(h, "flat"), unit(t, "rod"), unit(o, "small cube"), hto(h, t, o),
                            100 * h + 10 * t + o), rnd))
    more = [
        mcq_n(fig(blocks_svg(1, 3, 6)) + "Add 1 more rod. What number is it now?", 146, [137, 236, 126],
              "The blocks show 136. A rod is 10. 136 + 10 = 146. Only the tens digit changes.", rnd),
        mcq_n(fig(blocks_svg(1, 2, 9)) + "Add 1 more small cube. What number is it now?", 130, [1210, 139, 120],
              "The blocks show 129. Add 1 cube: now there are 10 cubes. Trade 10 cubes for 1 rod. "
              "That is 1 hundred, 3 tens and 0 ones: 130.", rnd),
    ]
    ten_rods = mcq_n(fig(blocks_svg(0, 10, 0)) + "There are 10 rods. What number do they show?", 100,
                     [10, 110, 1000],
                     "Each rod is 10. Count by 10s: 10, 20, 30 … 100. 10 tens make 1 hundred.", rnd)
    which = [
        mcq_n("Which number has 1 hundred, 3 tens and 8 ones?", 138, [831, 183, 12],
              "Write the hundreds digit first, then the tens, then the ones: 1, 3, 8. That is 138.", rnd),
        mcq_n("Which number has 1 hundred, 0 tens and 6 ones?", 106, [16, 1006, 160],
              "Write 1 for the hundreds, 0 for the tens and 6 for the ones: 106. "
              "The 0 shows there are no tens.", rnd),
    ]
    order = (what[:2] + how[:1] + what[2:4] + match[:1] + how[1:2] + what[4:6] + [ten_rods] + what[6:7]
             + match[1:] + which[:1] + what[7:8] + how[2:] + what[8:9] + which[1:] + what[9:] + more)
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Base ten blocks: hundreds, tens and ones", "items": order}


# ============================================================ set 2: value of a digit
def value_wrong(n, i):
    d = digit(n, i)
    if i == 2:
        return [d, d * 10, d * 1000]
    if i == 1:
        return [d, d * 100, n % 100]
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
    return ("%s is %s: %d. Write 0 for the empty %s place."
            % (cap(words(n)), hto_n(n), n, " and ".join(empty)))


def set_value(rnd):
    chart = [mcq_n(fig(chart_svg(n, hi=i)) + "What is the red digit worth?", digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i, True), rnd)
             for n, i in [(146, 1), (173, 2), (158, 0), (192, 1), (127, 1)]]
    plain = [mcq_n("What is the value of the %d in %d?" % (digit(n, i), n), digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i), rnd)
             for n, i in [(164, 1), (135, 0), (187, 1), (152, 2)]]
    place = [
        mcq("In 147, which digit is in the tens place?", 4, [1, 7, 40],
            "147 is 1 hundred, 4 tens and 7 ones. The tens digit is 4. (Its value is 40.)", rnd),
        mcq("In 185, which digit is in the hundreds place?", 1, [8, 5, 100],
            "185 is 1 hundred, 8 tens and 5 ones. The hundreds digit is 1. (Its value is 100.)", rnd),
    ]
    has = []
    for d, i, ans, wrong, extra in [
            (6, 1, 162, [126, 106, 16], "126 has 6 ones, not 6 tens."),
            (9, 0, 139, [193, 91, 190], "193 has 9 tens, not 9 ones."),
            (1, 2, 108, [18, 81, 11], "18, 81 and 11 have only 2 digits, so they have no hundreds.")]:
        assert digit(ans, i) == d and all(digit(w, i) != d for w in wrong)
        has.append(mcq_n("Which number has %s %d in the %s place?" % ("a", d, PL[i]), ans, wrong,
                         "%d is %s. The %d is in the %s place. %s" % (ans, hto_n(ans), d, PL[i], extra), rnd))
    wr = []
    for n, wrong in [(105, [15, 1005, 150]), (120, [12, 102, 1020]), (116, [16, 160, 1016])]:
        e = zero_e(n) if (n % 10 == 0 or digit(n, 1) == 0) else ""
        if n == 116:
            e = "One hundred sixteen is 1 hundred, 1 ten and 6 ones: 116. Sixteen is 16, not sixty (60)."
        wr.append(mcq_n("Write “%s” as a number." % words(n), n, wrong, e, rnd))
    cnt = mcq_n(fig(chart_svg(107)) + "How many tens are in 107?", 0, [1, 7, 10],
                "107 is 1 hundred, 0 tens and 7 ones. The 0 shows there are no tens.", rnd)
    has0 = mcq_n("Which number has 0 tens?", 104, [140, 14, 41],
                 "104 is 1 hundred, 0 tens and 4 ones. 140 has 4 tens, 14 has 1 ten and 41 has 4 tens.", rnd)
    school = mcq_n("Our school has 168 students. What is the value of the 6?", 60, [6, 600, 68],
                   "168 is 1 hundred, 6 tens and 8 ones. The 6 is in the tens place, so it is worth 60.", rnd)
    order = (chart[:2] + plain[:1] + place[:1] + wr[:1] + chart[2:3] + has[:1] + plain[1:2] + [cnt] + chart[3:4]
             + wr[1:2] + place[1:] + has[1:2] + plain[2:3] + [has0] + chart[4:] + wr[2:] + has[2:] + plain[3:]
             + [school])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "The value of each digit", "items": order}


# ============================================================ set 3: decompose in different ways
def set_decompose(rnd):
    std = [
        mcq("What is 145 in expanded form?", "100 + 40 + 5", ["1 + 4 + 5", "100 + 4 + 5", "10 + 40 + 5"],
            "145 is 1 hundred, 4 tens and 5 ones. That is 100 + 40 + 5.", rnd),
        mcq("What is 172 in expanded form?", "100 + 70 + 2", ["1 + 7 + 2", "100 + 7 + 2", "100 + 70 + 20"],
            "172 is 1 hundred, 7 tens and 2 ones. That is 100 + 70 + 2.", rnd),
        mcq("What is 108 in expanded form?", "100 + 8", ["10 + 8", "100 + 80", "1 + 8"],
            "108 is 1 hundred, 0 tens and 8 ones. 0 tens adds nothing. So 108 = 100 + 8.", rnd),
        mcq("What is 160 in expanded form?", "100 + 60", ["100 + 6", "10 + 60", "1 + 6"],
            "160 is 1 hundred, 6 tens and 0 ones. 6 tens = 60. So 160 = 100 + 60.", rnd),
    ]
    miss = [
        mcq_n("100 + ☐ + 3 = 153. What number goes in the box?", 50, [5, 53, 150],
              "153 is 1 hundred, 5 tens and 3 ones. 5 tens = 50.", rnd),
        mcq_n("☐ + 30 + 4 = 134. What number goes in the box?", 100, [1, 10, 134],
              "134 is 1 hundred, 3 tens and 4 ones. 1 hundred = 100.", rnd),
        mcq_n("100 + ☐ = 109. What number goes in the box?", 9, [90, 19, 0],
              "109 is 1 hundred, 0 tens and 9 ones. 100 + 9 = 109.", rnd),
    ]
    exp = [
        mcq_n("What number is 100 + 9?", 109, [1009, 19, 190],
              "100 + 9 is 1 hundred, 0 tens and 9 ones: 109. Do not write 100 and then 9. "
              "The answer has only 3 digits.", rnd),
        mcq_n("What number is 100 + 70?", 170, [1070, 17, 107],
              "100 + 70 is 1 hundred, 7 tens and 0 ones: 170. The answer has only 3 digits.", rnd),
    ]
    tens = [
        mcq_n("145 = ☐ tens and 5 ones. What number goes in the box?", 14, [4, 40, 140],
              "1 hundred is 10 tens. 10 tens + 4 tens = 14 tens. Check: 140 + 5 = 145.", rnd),
        mcq_n("168 = ☐ tens and 8 ones. What number goes in the box?", 16, [6, 60, 160],
              "1 hundred is 10 tens. 10 tens + 6 tens = 16 tens. Check: 160 + 8 = 168.", rnd),
        mcq_n("130 = ☐ tens. What number goes in the box?", 13, [3, 1, 130],
              "130 is 1 hundred and 3 tens. 1 hundred = 10 tens. 10 + 3 = 13 tens.", rnd),
        mcq_n("200 = ☐ tens. What number goes in the box?", 20, [2, 10, 200],
              "1 hundred = 10 tens. 2 hundreds = 20 tens. Count by 10s 20 times to reach 200.", rnd),
        mcq_n("156 = 1 hundred, ☐ tens and 6 ones. What number goes in the box?", 5, [15, 50, 56],
              "156 is 1 hundred, 5 tens and 6 ones. The tens digit is 5.", rnd),
    ]
    other = [
        mcq("Which is another way to make 145?", "14 tens and 5 ones",
            ["4 tens and 5 ones", "14 tens and 15 ones", "1 hundred, 14 tens and 5 ones"],
            "14 tens = 140. 140 + 5 = 145. (The others make 45, 155 and 245.)", rnd),
        mcq("Which is <b>not</b> equal to 120?", "1 hundred and 2 ones",
            ["12 tens", "1 hundred and 2 tens", "120 ones"],
            "1 hundred and 2 ones = 102, not 120. 12 tens = 120, 100 + 20 = 120 and 120 ones = 120.", rnd),
        mcq("Which shows 145 a different way?", "100 + 30 + 15",
            ["100 + 30 + 5", "100 + 40 + 15", "10 + 40 + 5"],
            "Take 1 ten from 40 and make it 10 ones: 100 + 30 + 15. Check: 100 + 30 + 15 = 145.", rnd),
        mcq_n("157 = 100 + 40 + ☐. What number goes in the box?", 17, [7, 70, 57],
              "157 = 100 + 50 + 7. Only 40 is used, so 1 ten moves to the ones: 10 + 7 = 17. "
              "Check: 100 + 40 + 17 = 157.", rnd),
    ]
    blk = [
        mcq_n(fig(blocks_svg(1, 3, 15)) + "What number do the blocks show?", 145, [1315, 135, 19],
              "15 small cubes are 1 ten and 5 ones. 1 hundred + 3 tens + 1 ten + 5 ones = 145. "
              "Check: 100 + 30 + 15 = 145.", rnd),
        mcq_n(fig(blocks_svg(0, 12, 7)) + "What number do the blocks show?", 127, [19, 27, 1207],
              "12 rods are 12 tens = 120. 120 + 7 = 127. 10 rods make 1 hundred, so it is 1 hundred, "
              "2 tens and 7 ones.", rnd),
    ]
    for v, w in [(140 + 5, 145), (45, 40 + 5), (140 + 15, 155), (100 + 140 + 5, 245), (100 + 2, 102),
                 (12 * 10, 120), (100 + 30 + 15, 145), (100 + 30 + 5, 135), (100 + 40 + 15, 155),
                 (100 + 40 + 17, 157), (100 + 30 + 15, 145), (120 + 7, 127), (160 + 8, 168), (130, 13 * 10)]:
        assert v == w
    order = (std[:2] + miss[:2] + exp[:1] + std[2:] + miss[2:] + exp[1:] + tens[4:] + tens[:1] + other[:1]
             + blk[:1] + tens[1:3] + other[1:2] + blk[1:] + tens[3:4] + other[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Decompose numbers in different ways", "items": order}


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
    for x, y in [(142, 124), (109, 190), (98, 102), (170, 107), (200, 199)]:
        lt = "&lt;" if x < y else "&gt;"
        gt = "&gt;" if x < y else "&lt;"
        e = compare_e(max(x, y), min(x, y))
        if x == 98:
            e += " Do not just look at the first digit. Count the digits first."
        cmp_.append(mcq("Which is true?", "%d %s %d" % (x, lt, y),
                        ["%d %s %d" % (x, gt, y), "%d = %d" % (x, y), "%d %s %d" % (y, lt, x)], e, rnd))
    big = [
        mcq_n("Which number is the greatest?", 163, [136, 116, 113],
              "All have 1 hundred. Tens: 163 has 6 tens, the most. So 163 is the greatest.", rnd),
        mcq_n("Which number is the least?", 87, [108, 180, 178],
              "87 is the only number with 2 digits, so it is the least, even though 8 is a big digit.", rnd),
        mcq_n("Which number is the greatest?", 200, [199, 190, 109],
              "200 has 2 hundreds. The others have only 1 hundred. 200 is 1 more than 199.", rnd),
        mcq_n("Which number is the least?", 101, [110, 111, 119],
              "All have 1 hundred. Tens: 101 has 0 tens, the fewest. So 101 is the least.", rnd),
    ]
    order = [
        mcq("Put 156, 165 and 65 in order from least to greatest.", "65, 156, 165",
            ["156, 165, 65", "65, 165, 156", "165, 156, 65"],
            "65 has only 2 digits, so it is the least. 156 and 165 both have 1 hundred. "
            "Tens: 5 tens &lt; 6 tens, so 156 &lt; 165. Order: 65, 156, 165.", rnd),
        mcq("Put 120, 102 and 12 in order from least to greatest.", "12, 102, 120",
            ["102, 12, 120", "12, 120, 102", "120, 102, 12"],
            "12 has only 2 digits, so it is the least. 102 and 120 both have 1 hundred. "
            "Tens: 0 tens &lt; 2 tens, so 102 &lt; 120. Order: 12, 102, 120.", rnd),
        mcq("Put 189, 198 and 98 in order from greatest to least.", "198, 189, 98",
            ["98, 189, 198", "189, 198, 98", "98, 198, 189"],
            "98 has only 2 digits, so it is the least. 189 and 198 both have 1 hundred. "
            "Tens: 9 tens &gt; 8 tens, so 198 &gt; 189. Order: 198, 189, 98.", rnd),
        mcq("Put 147, 174, 74 and 117 in order from least to greatest.", "74, 117, 147, 174",
            ["74, 147, 117, 174", "174, 147, 117, 74", "117, 147, 174, 74"],
            "74 has only 2 digits, so it is the least. The others have 1 hundred. "
            "Tens: 1 &lt; 4 &lt; 7. Order: 74, 117, 147, 174.", rnd),
    ]
    between = [
        mcq_n("Which number is between 120 and 150?", 136, [115, 153, 160],
              "136 is more than 120 and less than 150. 115 is too small. 153 and 160 are too big.", rnd),
        mcq_n("Which number is between 170 and 180?", 175, [157, 185, 107],
              "175 has 1 hundred and 7 tens, so it is between 170 and 180. 157 and 107 are too small. "
              "185 is too big.", rnd),
    ]
    near = [
        mcq_n("What number is 10 more than 145?", 155, [146, 245, 135],
              "10 more: add 1 ten. The tens digit goes from 4 to 5: 155. (146 is 1 more. 245 is 100 more.)", rnd),
        mcq_n("What number is 10 less than 160?", 150, [159, 60, 170],
              "10 less: take away 1 ten. 16 tens − 1 ten = 15 tens = 150. (159 is 1 less.)", rnd),
        mcq_n("What number is 1 more than 129?", 130, [1210, 139, 128],
              "129 + 1: 9 ones and 1 more one make 10 ones = 1 ten. So 12 tens become 13 tens: 130.", rnd),
    ]
    nl = [
        mcq_n(fig(number_line_svg(100, 200, 10, [100, 150, 200], 130)) + "What number does the arrow point to?",
              130, [103, 120, 140],
              "Each mark is 10. Count by 10s from 100: 110, 120, 130. The arrow is at 130.", rnd),
        mcq_n(fig(number_line_svg(0, 200, 10, [0, 100, 200], 170)) + "What number does the arrow point to?",
              170, [17, 160, 180],
              "From 0 to 100 there are 10 marks, so each mark is 10. "
              "The arrow is 7 marks after 100: 110, 120 … 170.", rnd),
    ]
    for a, b in [(65, 156), (156, 165), (12, 102), (102, 120), (98, 189), (189, 198), (74, 117), (117, 147),
                 (147, 174), (120, 136), (136, 150), (170, 175), (175, 180)]:
        assert a < b
    order = (cmp_[:2] + big[:2] + near[:1] + nl[:1] + cmp_[2:3] + order[:1] + between[:1] + near[1:2]
             + cmp_[3:4] + big[2:3] + order[1:2] + nl[1:] + near[2:] + cmp_[4:] + big[3:] + between[1:]
             + order[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers to 200", "items": order}


# ============================================================ set 5: estimate, count and word problems
EST = [10, 20, 50, 100, 150, 200]


def set_estimate(rnd, P):
    est = []
    for n, cols, rows, best, choices, seed in [(21, 7, 4, 20, [20, 50, 100, 200], 2101),
                                               (48, 10, 6, 50, [10, 20, 50, 100], 4801),
                                               (97, 13, 10, 100, [20, 50, 100, 200], 9701),
                                               (152, 19, 10, 150, [50, 100, 150, 200], 15201)]:
        assert best in choices and min(choices, key=lambda c: abs(c - n)) == best
        assert sorted(abs(c - n) for c in choices)[1] >= 25
        e = ("The big box has about %d groups of 10 dots. So there are about %d. If you count them all, there are %d. "
             "%d is close to %d." % (round(n / 10), best, n, n, best))
        wrong = ["about %d" % c for c in choices if c != best]
        est.append(mcq(fig(dots_svg(n, cols, rows, seed)) + "The small box has 10 dots. "
                       "About how many dots are in the big box?", "about %d" % best, wrong, e, rnd))
    sticks = [
        mcq_n(fig(sticks_svg(13, 6)) + "Each bundle has 10 craft sticks. How many sticks are there?", 136,
              [19, 1306, 163],
              "Count the bundles by 10s: 13 bundles = 13 tens = 130. Then count on 6 loose sticks: "
              "131, 132 … 136.", rnd),
        mcq_n(fig(sticks_svg(7, 12)) + "Each bundle has 10 craft sticks. How many sticks are there?", 82,
              [712, 19, 72],
              "7 bundles = 70. There are 12 loose sticks: that is 1 more ten and 2 ones. 70 + 12 = 82.", rnd),
    ]
    sense = mcq("About how many students are in one Grade 2 class?", "about 20",
                ["about 2", "about 100", "about 200"],
                "A Grade 2 class has about 20 students. 2 is too few. 100 or 200 is a whole school, not one class.",
                rnd)
    wp = []
    name, he, his = P.next()
    wp.append(mcq_n("%s has 1 box of 100 hockey cards, 4 packs of 10 cards and 7 single cards. "
                    "How many cards does %s have?" % (name, he), 147, [12, 174, 741],
                    "1 box = 100. 4 packs of 10 = 40. 7 single cards = 7. 100 + 40 + 7 = 147.", rnd))
    wp.append(mcq("A farmer sees 160 Canada geese on Monday and 106 on Tuesday. On which day did she see more geese?",
                  "Monday", ["Tuesday", "Both days the same", "You cannot tell"],
                  "Both have 1 hundred. Tens: 160 has 6 tens and 106 has 0 tens. 160 &gt; 106, so Monday.", rnd))
    name, he, his = P.next()
    wp.append(mcq("%s has 13 dimes. A dime is 10¢. How much money is that?" % name, "130¢",
                  ["13¢", "23¢", "103¢"],
                  "Count by 10s 13 times: 10, 20, 30 … 130. 13 tens = 130, so 13 dimes = 130¢. That is the same as $1.30.", rnd))
    wp.append(mcq_n("Pencils come in boxes of 10. The class has 18 boxes. How many pencils is that?", 180,
                    [18, 108, 28],
                    "18 boxes of 10 = 18 tens = 180. (10 boxes = 100, 8 boxes = 80, 100 + 80 = 180.)", rnd))
    wp.append(mcq_n("For the food drive, Grade 2 collects “one hundred eight” cans. Write the number of cans.", 108,
                    [18, 1008, 180],
                    "One hundred eight is 1 hundred, 0 tens and 8 ones: 108. Write 0 for the empty tens place.", rnd))
    g = P.next()
    b = P.next()
    while g[1] == b[1]:
        b = P.next()
    wp.append(mcq("%s reads 145 pages. %s reads 154 pages. Who reads more pages?" % (g[0], b[0]), b[0],
                  [g[0], "They read the same", "You cannot tell"],
                  "Both have 1 hundred. Tens: 154 has 5 tens and 145 has 4 tens. 154 &gt; 145, so %s reads more."
                  % b[0], rnd))
    name, he, his = P.next()
    wp.append(mcq_n("%s’s mystery number is between 150 and 160. It has 7 ones. What is it?" % name, 157,
                    [175, 147, 167],
                    "Between 150 and 160 means 1 hundred and 5 tens. Then 7 ones: 157.", rnd))
    wp.append(mcq_n("120 students sit in the gym in rows of 10. How many rows are there?", 12, [120, 2, 20],
                    "120 = 12 tens. Each row is 10 students, so there are 12 rows. Count by 10s: 10, 20 … 120.", rnd))
    wp.append(mcq("Three classes raise money for the Terry Fox Run: $126, $162 and $116. "
                  "Which list goes from least to greatest?", "$116, $126, $162",
                  ["$126, $116, $162", "$162, $126, $116", "$116, $162, $126"],
                  "All have 1 hundred. Tens: 1 ten &lt; 2 tens &lt; 6 tens. Order: $116, $126, $162.", rnd))
    name, he, his = P.next()
    wp.append(mcq_n("%s has 100 stickers. %s gets 3 more packs of 10. How many stickers does %s have now?"
                    % (name, cap(he), he), 130, [103, 400, 113],
                    "3 packs of 10 = 30. 100 + 30 = 130. (103 adds 3, not 3 tens.)", rnd))
    name, he, his = P.next()
    wp.append(mcq_n("A book has 200 pages. %s is on page 190. How many pages are left to read?" % name, 10,
                    [1, 90, 100],
                    "From 190 to 200 is 1 more ten. 200 − 190 = 10 pages.", rnd))
    wp.append(mcq_n("Today is the 100th day of school. What day of school was it 10 days ago?", 90,
                    [99, 110, 10],
                    "10 days ago means 10 less. 100 − 10 = 90. (99 is 1 less. 110 is 10 more.)", rnd))
    name, he, his = P.next()
    wp.append(mcq_n("%s writes one hundred fifty-two as 1052. What should %s write?" % (name, he), 152,
                    [1052, 125, 102],
                    "One hundred fifty-two is 1 hundred, 5 tens and 2 ones: 152. "
                    "It has only 3 digits. Do not write 10 for the hundred.", rnd))
    for v, w in [(130 + 6, 136), (70 + 12, 82), (100 + 40 + 7, 147), (13 * 10, 130), (18 * 10, 180),
                 (12 * 10, 120), (100 + 30, 130), (200 - 190, 10), (100 - 10, 90)]:
        assert v == w
    order = est[:2] + sticks[:1] + est[2:3] + [sense] + sticks[1:] + est[3:] + wp
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Estimate, count and word problems", "items": order}


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
        "<p>10 ones make 1 ten. 10 tens make 1 hundred. "
        "A 3-digit number has a <b>hundreds</b>, a <b>tens</b> and a <b>ones</b> place.</p>"
        "<figure class='sn-fig'>" + blocks_svg(1, 4, 5, labels=True) +
        "<figcaption>Base ten blocks for 145. A flat is 100, a rod is 10 and a small cube is 1.</figcaption></figure>"
        "<h2>The value of a digit</h2>"
        "<p>The place tells you what a digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(145, hi=1) +
        "<figcaption>In 145 the 4 is in the tens place. Its value is 4 tens, or 40.</figcaption></figure>"
        "<p>If a place is empty, write <b>0</b> there.</p>" +
        ex("Write the number", "Write “one hundred five” as a number.",
           "1 hundred, 0 tens, 5 ones. Write 1, 0, 5.", "105 (not 15 or 1005)") +
        "<h2>Decompose in different ways</h2>"
        "<p>145 = 100 + 40 + 5. You can also trade 1 hundred for 10 tens. "
        "Then 145 is 14 tens and 5 ones.</p>"
        "<figure class='sn-fig'>" + blocks_svg(0, 14, 5, labels=True) +
        "<figcaption>14 tens and 5 ones is also 145: 140 + 5 = 145.</figcaption></figure>" +
        ex("Decompose", "Show 145 in two ways.",
           "1 hundred, 4 tens and 5 ones. Or 14 tens and 5 ones.", "100 + 40 + 5 = 140 + 5") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits. A 3-digit number is greater than a 2-digit number. "
        "If both have 3 digits, compare the hundreds, then the tens, then the ones.</p>" +
        ex("Compare", "142 ☐ 124", "Hundreds: 1 = 1. Tens: 4 tens &gt; 2 tens.", "142 &gt; 124") +
        "<p>&gt; means “is greater than”. &lt; means “is less than”. The open side faces the greater number.</p>"
        "<h2>Estimate, then count</h2>"
        "<p>To estimate, look at a group of 10. Think: how many groups of 10 fit? "
        "Then count to check. Count by 10s, then count on the ones.</p>"
        "<figure class='sn-fig'>" + dots_svg(48, 10, 6, 4801) +
        "<figcaption>About 5 groups of 10 fit, so there are about 50 dots. Count to check: 48.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing each part you hear (one hundred five = 1005)", "A number in the hundreds has 3 digits: 105"],
            ["Leaving out the zero (105 = 15)", "Write 0 for the empty tens place: 105"],
            ["Reading the digit, not its value (the 4 in 145 is 4)", "The 4 is in the tens place: 40"],
            ["Counting blocks, not their values (1 flat, 4 rods, 5 cubes = 10)", "Flats are 100, rods are 10: 145"],
            ["Comparing the first digits only (98 &gt; 102)", "Count the digits first: 102 &gt; 98"],
            ["Guessing a far-off estimate", "Use a group of 10 to help, then count to check"],
        ])
    )


FAQ = [
    {"q": "What number skills are in the Grade 2 Ontario math curriculum?",
     "a": "Grade 2 students read, represent, compose and decompose whole numbers up to 200 (B1.1), compare and order them (B1.2) and estimate the number of objects in collections of up to 200 and check by counting (B1.3)."},
    {"q": "How do I explain hundreds, tens and ones to a Grade 2 child?",
     "a": "Use base ten blocks or bundles of 10 craft sticks: 10 ones make a ten and 10 tens make a hundred. Then 145 is 1 hundred, 4 tens and 5 ones, or 100 + 40 + 5."},
    {"q": "Why does my child write 1005 for one hundred five?",
     "a": "Children often write each part they hear, 100 and then 5. Show that a number in the hundreds has only 3 digits and that 0 holds the empty tens place: 105."},
    {"q": "How can children practise estimating at home?",
     "a": "Fill a jar with pasta, buttons or LEGO bricks, show a group of 10, and ask for an estimate. Then count by 10s to check, and talk about how close the estimate was."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(42801)
    P = People(random.Random(428011))
    sets = [set_blocks(rnd), set_value(rnd), set_decompose(rnd), set_compare(rnd), set_estimate(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "numbers-to-200", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 200: Place Value, Comparing and Estimating",
        "seo_title": "Grade 2 Numbers to 200 Math Worksheets: Free, with Answer Key (Ontario)",
        "short_title": "Numbers to 200",
        "domain": "Number",
        "standard_code": "Grade 2: B1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compose, and decompose whole numbers up to and including 200, using a variety of tools and strategies, and describe various ways they are used in everyday life",
        "meta_desc": "Free Grade 2 math worksheets on numbers to 200 for the Ontario curriculum: base ten blocks, the value of each digit, decomposing numbers, comparing and ordering, and estimating then counting. 100 questions with an answer key.",
        "key_big": "The place of a digit tells you its value. The 4 in 145 is worth 40.",
        "key_sub": "Write 0 for an empty place: one hundred five is 105, not 15 or 1005. 145 is 100 + 40 + 5, or 14 tens and 5 ones.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(base ten blocks|place value chart|number line|dots to estimate|craft sticks)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
