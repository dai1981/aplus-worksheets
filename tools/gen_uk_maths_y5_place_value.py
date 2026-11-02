# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Place Value to a Million and Negative Numbers
(National Curriculum in England, Year 5: Number and place value)
  python3 tools/gen_uk_maths_y5_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are written with commas. Negative numbers use the real minus sign − (U+2212).
Rounding and Roman numerals are separate units.
Wrong answers come from real mistakes: giving the digit instead of its value, missing zero placeholders when
writing words as numerals (three hundred and four thousand and twenty → 34,020), changing the wrong digit for
10,000 more or less, forgetting to exchange when a 9 becomes 10 (or a 0 has to give), comparing the first digits
only instead of counting the digits, skipping 0 when counting through zero, and ignoring the minus sign.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRAY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]


# ------------------------------------------------------------ helpers
def c(n):
    """Number with commas and a real minus sign: 4536 -> 4,536, -3 -> −3."""
    return (M if n < 0 else "") + "{:,}".format(abs(n))


def deg(n):
    return c(n) + " °C"


def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        if x in seen or not x:
            continue
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, cands, e, rnd, fmt=c):
    """Whole-number choices with commas. Wrong numbers that are 0 or less are dropped."""
    return mcq(q, fmt(correct), [fmt(v) for v in cands if v is not None and v > 0 and v != correct], e, rnd)


def mcq_z(q, correct, cands, e, rnd, fmt=c):
    """Integer choices that may be negative or zero."""
    return mcq(q, fmt(correct), [fmt(v) for v in cands if v is not None and v != correct], e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
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


def ndig(n):
    return len(str(n))


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def expanded(n):
    return " + ".join(c(digit(n, i) * 10 ** i) for i in range(ndig(n) - 1, -1, -1) if digit(n, i))


def zero_mistakes(n):
    """Numbers a pupil writes when a zero goes missing, moves, or is added."""
    s = str(n)
    out = []
    for i, ch in enumerate(s):
        if ch == "0":
            out.append(int(s[:i] + s[i + 1:]))                 # left out a zero
            for j in (i - 1, i + 1):                            # zero swapped with a neighbour
                if 0 < j < len(s) and s[j] != "0":
                    l = list(s)
                    l[i], l[j] = l[j], l[i]
                    out.append(int("".join(l)))
    for i in range(1, len(s)):                                  # an extra zero
        if s[i] == "0":
            out.append(int(s[:i] + "0" + s[i:]))
    return [v for v in out if v != n and 1000 <= v < 10000000]


def joined_digits(n):
    """Writing only the non-zero digits side by side (300,000 + 4,000 + 20 -> 342)."""
    return int("".join(ch for ch in str(n) if ch != "0"))


# ------------------------------------------------------------ numbers in words (British: "and" before tens/ones)
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def w100(n):
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


def w1000(n):
    h, r = divmod(n, 100)
    out = []
    if h:
        out.append(ONES[h] + " hundred")
    if r:
        out.append(w100(r))
    return " and ".join(out)


def words(n):
    """304,020 -> three hundred and four thousand and twenty."""
    assert 0 < n < 10000000
    m, rest = divmod(n, 1000000)
    t, o = divmod(rest, 1000)
    parts = []
    if m:
        parts.append(w1000(m) + " million")
    if t:
        parts.append(w1000(t) + " thousand")
    s = ", ".join(parts)
    if o:
        if not s:
            s = w1000(o)
        elif o < 100:
            s += " and " + w100(o)
        else:
            s += ", " + w1000(o)
    return s


assert words(304020) == "three hundred and four thousand and twenty"
assert words(406050) == "four hundred and six thousand and fifty"
assert words(811953) == "eight hundred and eleven thousand, nine hundred and fifty-three"
assert words(1000000) == "one million"


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


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 64, 28, 28, 48
SUB = ["H", "T", "O", "H", "T", "O"]


def chart_svg(n, hi=None):
    """Thousands (H T O) | Ones (H T O) chart with a 5- or 6-digit n. hi = place index to colour red.
    Places in front of the first digit are left empty."""
    x0 = y0 = 6
    W, H = 2 * x0 + 6 * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, 6 * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 6 * CW, H1 + H2, FILL)]
    s.append(text(x0 + 1.5 * CW, y0 + 19, "Thousands", 14, bold=True))
    s.append(text(x0 + 4.5 * CW, y0 + 19, "Ones", 14, bold=True))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0 + 3 * CW, y0, x0 + 3 * CW, y0 + H1 + H2 + ROW, GREEN))
    for k in range(6):
        i = 5 - k
        x = x0 + k * CW
        if k not in (0, 3):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (x, y0 + H1, x, y0 + H1 + H2 + ROW, GREEN))
        s.append(text(x + CW / 2, y0 + H1 + 19, SUB[k], 14, bold=True))
        if i < ndig(n):
            s.append(text(x + CW / 2, y0 + H1 + H2 + 34, str(digit(n, i)), 28, bold=True,
                          col=RED if hi == i else INK))
    for y in (y0 + H1, y0 + H1 + H2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + 6 * CW, y, GREEN, "1.2" if y == y0 + H1 else "2"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, 6 * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % c(n))


def number_line_svg(lo, hi, step, labels, arrow):
    """Number line lo..hi, a tick every step, bold numbers at `labels`, red arrow at `arrow`."""
    L, R, Y = 50, 430, 58
    W, H = 480, 100
    span = hi - lo

    def X(v):
        return L + (v - lo) * (R - L) / span

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, c(v), 15, bold=True, col=GREEN))
        v += step
    ax = X(arrow)
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (c(lo), c(hi)))


def neg_line_svg(lo, hi, labels, g=19, arrow=None, dots=None, jumps=None, hops=None):
    """Number line through zero, one tick for every whole number.
    dots = numbers marked with red dots; jumps = (a, b) with a < 0 < b draws two brackets through 0;
    hops = (start, end) draws a hop for every step."""
    pad = 30
    n = hi - lo
    W = 2 * pad + n * g
    Y = 52 if (jumps or hops or arrow is not None) else 30
    H = Y + 34

    def X(v):
        return pad + (v - lo) * g

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 16, Y, W - pad + 16, Y, INK),
         "<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (pad - 18, Y, W - pad + 18, Y, INK)]
    for v in range(lo, hi + 1):
        big = v in labels
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (9 if big else 6), X(v), Y + (9 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 26, c(v), 14, bold=(v == 0)))
    if jumps:
        a, b = jumps
        for (u, w, col) in [(a, 0, BLUE), (0, b, RED)]:
            x1, x2 = X(u), X(w)
            s.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x1, Y - 4, (x1 + x2) / 2, Y - 40, x2, Y - 4, col))
            s.append(text((x1 + x2) / 2, Y - 26, str(abs(w - u)), 15, bold=True, col=col))
    if hops:
        a, b = hops
        st = -1 if b < a else 1
        for v in range(a, b, st):
            x1, x2 = X(v), X(v + st)
            s.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='1.6'/>"
                     % (x1, Y - 4, (x1 + x2) / 2, Y - 26, x2, Y - 4, RED))
        s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (X(b), Y, RED))
    if dots:
        for v in dots:
            s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (X(v), Y, RED))
    if arrow is not None:
        ax = X(arrow)
        s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (ax - 6, Y - 20, ax + 6, Y - 20, ax, Y - 8, RED))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 36, ax, Y - 18, RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (c(lo), c(hi)))


def thermo_svg(lo, hi, val):
    """Celsius thermometer: a tick every degree, numbers every 5 degrees, red column up to val."""
    g = 9
    top = 16
    x = 70
    Yv = lambda v: top + (hi - v) * g
    bot = Yv(lo)
    s = ["<rect x='%d' y='%d' width='14' height='%d' rx='7' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
         % (x - 7, top - 8, bot - top + 16, INK)]
    s.append("<circle cx='%d' cy='%d' r='12' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, bot + 18, RED, INK))
    s.append("<rect x='%d' y='%d' width='6' height='%d' fill='%s'/>" % (x - 3, Yv(val), bot + 14 - Yv(val), RED))
    for v in range(lo, hi + 1):
        y = Yv(v)
        big = v % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x - 9 - (9 if big else 4), y, x - 9, y, INK, "1.6" if big else "1"))
        if big:
            s.append(text(x - 22, y + 5, c(v), 14, anchor="end", bold=(v == 0)))
    s.append(text(x + 14, top + 4, "°C", 14, anchor="start", bold=True))
    H = int(bot + 36)
    return svg_wrap(108, H, "".join(s), "thermometer from %s to %s degrees Celsius" % (c(lo), c(hi)))


# ============================================================ set 1: value of each digit, numbers in words
def distinct(rnd, used, nd):
    while True:
        d = rnd.sample(range(10), nd)
        if d[0] == 0:
            continue
        n = int("".join(map(str, d)))
        if n not in used:
            used.add(n)
            return n


def value_cands(d, i):
    out = [d * 10 ** (i - 1) if i >= 1 else None, d * 10 ** (i + 1), d]
    if i >= 2:
        out.append(d * 10 ** (i - 2))
    return [v for v in out if v and v != d * 10 ** i] + [d * 10 ** (i + 2)]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), c(v), d, c(v)))


def set_value(rnd, used):
    A, B, C, D, E, F, G, H = [], [], [], [], [], [], [], []
    for nd, i in [(5, 3), (6, 4), (6, 5), (5, 4), (6, 2)]:      # chart, red digit (5)
        while True:
            n = distinct(rnd, used, nd)
            if digit(n, i):
                break
        d = digit(n, i)
        A.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True), rnd))
    for nd, i in [(6, 3), (5, 4), (6, 5), (6, 4)]:              # value, no chart (4)
        while True:
            n = distinct(rnd, used, nd)
            if digit(n, i):
                break
        d = digit(n, i)
        B.append(mcq_n("What is the value of the digit %d in %s?" % (d, c(n)), d * 10 ** i,
                       value_cands(d, i), value_e(d, i), rnd))
    for i in [4, 5]:                                             # which digit is in a place (2)
        n = distinct(rnd, used, 6)
        while not digit(n, i):
            n = distinct(rnd, used, 6)
        d = digit(n, i)
        cands = [digit(n, x) for x in sorted(range(6), key=lambda x: (abs(x - i), x)) if x != i]
        e = ("Read the places from the right: ones, tens, hundreds, thousands, ten thousands, hundred thousands. "
             "In %s the %s digit is %d, worth %s." % (c(n), PL[i], d, c(d * 10 ** i)))
        C.append(mcq("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, cands, e, rnd))
    for n in [304020, 70605, 250009]:                            # words -> numeral (3)
        used.add(n)
        cands = zero_mistakes(n) + [joined_digits(n)]
        t, o = n // 1000, n % 1000
        e = ("Write the thousands part first: %s thousand → %d. Then the last three digits: %s → %03d. "
             "Fill every empty place with 0: %s." % (w1000(t), t, w1000(o), o, c(n)))
        D.append(mcq_n("Which number is <b>%s</b>?" % words(n), n, cands, e, rnd))
    for n in [406050, 90712]:                                    # numeral -> words (2)
        used.add(n)
        cands = [words(v) for v in zero_mistakes(n)]
        e = ("Split %s at the comma: %s thousand, then %s. Say the thousands part and the word “thousand”, "
             "then the rest: %s." % (c(n), n // 1000, n % 1000, words(n)))
        E.append(mcq("How do you write %s in words?" % c(n), words(n), cands, e, rnd))
    for n in [503082, 60704]:                                    # expanded -> number (2)
        used.add(n)
        cands = zero_mistakes(n) + [joined_digits(n)]
        e = "Put each digit in its place and write 0 in every empty place: %s = %s." % (expanded(n), c(n))
        F.append(mcq_n("What number is <b>%s</b>?" % expanded(n), n, cands, e, rnd))
    G.append(mcq_n("In 330,000, how many times greater is the value of the first 3 than the value of the second 3?",
                   10, [100, 3, 270000],
                   "The first 3 is worth 300,000. The second 3 is worth 30,000. 300,000 ÷ 30,000 = 10. "
                   "Each place to the left is worth 10 times more. (270,000 is the difference, not how many times "
                   "greater.)", rnd))
    d, i = 7, 4
    others = [x for x in range(1, 10) if x != d]
    rnd.shuffle(others)
    base = others[:5]
    nums = {}
    for pos in [5, 4, 3, 2]:
        ds = base[:]
        ds.insert(5 - pos, d)
        nums[pos] = int("".join(map(str, ds)))
    assert digit(nums[i], i) == d
    H.append(mcq("Which number has a %d in the ten thousands place?" % d, c(nums[i]),
                 [c(nums[x]) for x in nums if x != i],
                 "In a 6-digit number the ten thousands place is the 2nd digit from the left (5th from the right). "
                 "In %s the %d is there, so it is worth %s." % (c(nums[i]), d, c(d * 10 ** i)), rnd))
    order = A[:3] + C + A[3:] + B + H + F + D + E + G
    assert len(order) == 20
    return {"title": "Value of each digit up to 1,000,000 and numbers in words", "items": order}


# ============================================================ set 2: counting in powers of 10
def set_count(rnd):
    its = []
    # more / less (8): (amount, sign, n, wrongs, explanation)
    specs = [
        (10000, 1, 245318, [246318, 345318, 235318],
         "Only the ten thousands digit changes: 4 → 5. The other digits stay the same. 245,318 + 10,000 = 255,318."),
        (100000, -1, 708452, [698452, 808452, 707452],
         "Only the hundred thousands digit changes: 7 → 6. The other digits stay the same. "
         "708,452 − 100,000 = 608,452."),
        (1000, 1, 39600, [30600, 39700, 49600],
         "9 thousands + 1 thousand = 10 thousands. Exchange them for 1 ten thousand: the 3 becomes 4 and the "
         "thousands digit becomes 0. 39,600 + 1,000 = 40,600."),
        (10000, -1, 503214, [403214, 513214, 502214],
         "There are 0 ten thousands, so exchange 1 hundred thousand for 10 ten thousands. 10 − 1 = 9 ten "
         "thousands and 4 hundred thousands are left. 503,214 − 10,000 = 493,214."),
        (100, 1, 64950, [64050, 64960, 65950],
         "9 hundreds + 1 hundred = 10 hundreds. Exchange them for 1 thousand: 4 thousands become 5 and the "
         "hundreds digit becomes 0. 64,950 + 100 = 65,050."),
        (10000, 1, 896000, [806000, 897000, 996000],
         "9 ten thousands + 1 ten thousand = 10 ten thousands. Exchange them for 1 hundred thousand: "
         "8 becomes 9 and the ten thousands digit becomes 0. 896,000 + 10,000 = 906,000."),
        (1000, -1, 100500, [101500, 90500, 100400],
         "There are 0 thousands and 0 ten thousands, so exchange 1 hundred thousand for 9 ten thousands and "
         "10 thousands. Take 1 thousand away: 100,500 − 1,000 = 99,500."),
        (100000, 1, 900000, [910000, 800000, 901000],
         "9 hundred thousands + 1 hundred thousand = 10 hundred thousands = 1 million. "
         "900,000 + 100,000 = 1,000,000."),
    ]
    for amt, sg, n, wrong, e in specs:
        ans = n + sg * amt
        assert ans not in wrong and len(set(wrong)) == 3
        assert c(ans) in e
        its.append(mcq_n("What is %s %s than %s?" % (c(amt), "more" if sg > 0 else "less", c(n)), ans, wrong, e, rnd))
    # reverse (2)
    for amt, kind, n, wrong in [(10000, "more", 482150, [492150, 481150, 382150]),
                                (100000, "less", 360400, [260400, 370400, 361400])]:
        sg = 1 if kind == "more" else -1
        ans = n - sg * amt
        e = ("Work backwards. If %s %s than the number is %s, the number is %s %s than %s: %s."
             % (c(amt), kind, c(n), c(amt), "less" if sg > 0 else "more", c(n), c(ans)))
        its.append(mcq_n("%s %s than a number is %s. What is the number?" % (c(amt), kind, c(n)), ans, wrong, e, rnd))
    # sequences (8): (step, seq with None for the box, wrongs, extra explanation)
    seqs = [
        (10, [5970, 5980, 5990, "?"], [5000, 5991, 6090],
         "9 tens + 1 ten = 10 tens: exchange them for 1 hundred. Now there are 10 hundreds: exchange them for 1 thousand."),
        (100, [46800, 46900, 47000, "?"], [47010, 48000, 46900], ""),
        (1000, [128500, 129500, 130500, "?"], [130600, 140500, 129500], ""),
        (10000, [27450, 37450, 47450, 57450, "?"], [58450, 157450, 47450], ""),
        (100000, [150000, 250000, 350000, "?"], [360000, 351000, 250000], ""),
        (-10000, [135200, 125200, 115200, 105200, "?"], [104200, 5200, 115200],
         "105,200 has 0 ten thousands, so exchange 1 hundred thousand for 10 ten thousands: 10 − 1 = 9."),
        (-1000, [13050, 12050, 11050, 10050, "?"], [9950, 11050, 10040],
         "10,050 has 0 thousands, so exchange 1 ten thousand for 10 thousands: 10 − 1 = 9."),
        (10000, [482000, 492000, None, 512000], [493000, 592000, 402000],
         "9 ten thousands + 1 ten thousand = 10 ten thousands: exchange them for 1 hundred thousand. Check: 502,000 + 10,000 = 512,000."),
    ]
    for s, seq, wrong, extra in seqs:
        if None in seq:
            k = seq.index(None)
            ans = seq[k - 1] + s
            assert seq[k + 1] == ans + s
            show = ", ".join("☐" if v is None else c(v) for v in seq)
            q = "Count in %ss: %s. What number goes in the box?" % (c(s), show)
            e = "The numbers go up by %s each time. %s + %s = %s. %s" % (c(s), c(seq[k - 1]), c(s), c(ans), extra)
        else:
            nums = seq[:-1]
            for a, b in zip(nums, nums[1:]):
                assert b - a == s
            ans = nums[-1] + s
            q = "%s: %s, ? What comes next?" % ("Count in %ss" % c(s) if s > 0 else "Count back in %ss" % c(-s),
                                                 ", ".join(c(v) for v in nums))
            e = ("Each number is %s %s than the one before. %s %s %s = %s. %s"
                 % (c(abs(s)), "more" if s > 0 else "less", c(nums[-1]), "+" if s > 0 else M, c(abs(s)), c(ans), extra))
            if not extra:
                e += "Only the %s digit changes." % PL[len(str(abs(s))) - 1]
        assert ans not in wrong
        its.append(mcq_n(q, ans, wrong, e.strip(), rnd))
    # find the rule (2)
    its.append(mcq("What is the rule? 34,615, 44,615, 54,615, 64,615", "add 10,000",
                   ["add 1,000", "add 100,000", "add 10"],
                   "Only the ten thousands digit changes: 3, 4, 5, 6. So each number is 10,000 more than the one before.",
                   rnd))
    its.append(mcq("What is the rule? 608,300, 607,300, 606,300, 605,300", "take away 1,000",
                   ["take away 100", "take away 10,000", "add 1,000"],
                   "Only the thousands digit changes and it gets smaller: 8, 7, 6, 5. So the rule is take away 1,000.",
                   rnd))
    assert len(its) == 20
    # easy -> hard: plain more/less, sequences without exchange, rules, then exchanges and reverse
    order = [its[0], its[1], its[11], its[12], its[13], its[14], its[18], its[19], its[8], its[9],
             its[2], its[4], its[10], its[3], its[5], its[15], its[16], its[17], its[6], its[7]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Count in steps of 10, 100, 1,000, 10,000 and 100,000", "items": order}


# ============================================================ set 3: compare and order
def first_diff(a, b):
    for i in range(6, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def compare_expl(big, small):
    if ndig(big) != ndig(small):
        return "%s has %d digits and %s has only %d, so %s is greater." % (c(big), ndig(big), c(small), ndig(small), c(big))
    i = first_diff(big, small)
    same = ("The digits are the same until the %s place" % PL[i]) if i < ndig(big) - 1 else "Start with the %s" % PL[i]
    return ("Compare from the left. %s: %s is more than %s. So %s &gt; %s."
            % (same, plural(digit(big, i), i), plural(digit(small, i), i), c(big), c(small)))


def lookalikes(rnd, used):
    """4 different 6-digit numbers made from the same digits, with the same hundred thousands digit."""
    while True:
        ds = rnd.sample(range(1, 10), 6)
        out = set()
        tries = 0
        while len(out) < 4 and tries < 80:
            tries += 1
            l = ds[:]
            a = rnd.randint(1, 3)
            b = a + rnd.choice([1, 2])
            l[a], l[b] = l[b], l[a]
            out.add(int("".join(map(str, l))))
        if len(out) == 4 and not (out & used):
            used.update(out)
            return sorted(out)


def set_compare(rnd, used):
    its = []
    for x, y in [(45672, 45762), (99850, 100400), (306500, 360050), (781240, 781204)]:
        right = "%s %s %s" % (c(x), "&lt;" if x < y else "&gt;", c(y))
        wrong = ["%s %s %s" % (c(x), "&gt;" if x < y else "&lt;", c(y)), "%s = %s" % (c(x), c(y)),
                 "%s %s %s" % (c(y), "&lt;" if x < y else "&gt;", c(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 99850:
            e += " Big first digits do not matter when a number has fewer digits."
        its.append(mcq("Which is true?", right, wrong, e, rnd))
    for j in range(6):
        if j == 2:
            nums = [98760, 102300, 120300, 103200]
        elif j == 5:
            nums = [100100, 99999, 100010, 101000]
        else:
            nums = lookalikes(rnd, used)
        nums = sorted(nums)
        want_max = j < 3
        ans = nums[-1] if want_max else nums[0]
        nxt = nums[-2] if want_max else nums[1]
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % c(ans)
            if 98760 in nums:
                e = ("98,760 has only 5 digits, so it is the smallest, even though it starts with 9. "
                     "Of the 6-digit numbers, c" + compare_expl(ans, nxt)[1:] + " %s is the greatest." % c(ans))
        else:
            e = compare_expl(nxt, ans) + " %s is the smallest." % c(ans)
            if 99999 in nums:
                e = "99,999 has only 5 digits, so it is the smallest. Every 6-digit number is at least 100,000."
        its.append(mcq("Which number is the %s?" % ("greatest" if want_max else "smallest"), c(ans),
                       [c(v) for v in nums if v != ans], e, rnd))
    fmt = lambda l: ", ".join(c(v) for v in l)
    for j in range(3):
        while True:
            nums = lookalikes(rnd, used)
            three = rnd.sample(nums, 3)
            if three != sorted(three) and three != sorted(three)[::-1]:
                break
        up = j < 2
        o = sorted(three) if up else sorted(three)[::-1]
        perms = [[o[0], o[2], o[1]], [o[1], o[0], o[2]], o[::-1], [o[2], o[0], o[1]]]
        a, b, cc = sorted(three)
        i1, i2 = first_diff(b, a), first_diff(cc, b)
        e = ("Compare from the left. %s &lt; %s (%s: %d &lt; %d). %s &lt; %s (%s: %d &lt; %d). So the order is %s."
             % (c(a), c(b), PL[i1], digit(a, i1), digit(b, i1), c(b), c(cc), PL[i2], digit(b, i2), digit(cc, i2), fmt(o)))
        its.append(mcq("Put %s in order from %s." % (fmt(three), "smallest to greatest" if up else "greatest to smallest"),
                       fmt(o), [fmt(p) for p in perms], e, rnd))
    its.append(mcq_n(fig(number_line_svg(0, 1000000, 100000, [0, 500000, 1000000], 700000)) +
                     "What number does the arrow point to?", 700000, [70000, 300000, 800000],
                     "From 0 to 1,000,000 there are 10 equal jumps, so each mark is 100,000. The arrow is 7 marks "
                     "after 0: 700,000.", rnd))
    its.append(mcq_n(fig(number_line_svg(300000, 400000, 10000, [300000, 350000, 400000], 360000)) +
                     "What number does the arrow point to?", 360000, [306000, 340000, 370000],
                     "From 300,000 to 400,000 there are 10 equal jumps, so each mark is 10,000, not 1,000. "
                     "The arrow is 6 marks after 300,000: 300,000 + 60,000 = 360,000.", rnd))
    for v, w in [(455800, [445800, 45980, 540500])]:
        assert 450000 < v < 460000 and all(not 450000 < x < 460000 for x in w)
        its.append(mcq_n("Which number is between 450,000 and 460,000?", v, w,
                         "Numbers between 450,000 and 460,000 have 4 hundred thousands and 5 ten thousands. "
                         "455,800 fits. 45,980 has only 5 digits, so it is much smaller.", rnd))
    its.append(mcq("6☐4,500 &gt; 674,000. Which digit could go in the box?", "8", ["4", "5", "6"],
                   "The hundred thousands are the same (6). Compare the ten thousands: the box must be 7 or more. "
                   "4, 5 and 6 are too small. 684,500 &gt; 674,000.", rnd))
    its.append(mcq("3☐,850 &lt; 34,100. Which digit could go in the box?", "3", ["4", "5", "9"],
                   "The ten thousands are the same (3). Compare the thousands: the box must be 4 or less. "
                   "If it is 4, compare the hundreds: 8 &gt; 1, so 34,850 would be too big. 33,850 &lt; 34,100.", rnd))
    its.append(mcq_n("Use each of the digits 4, 0, 7, 2, 9 and 5 once. What is the greatest 6-digit number you can make?",
                     975420, [975402, 957420, 204579],
                     "Put the biggest digit in the hundred thousands place, then the next biggest, and so on: "
                     "9, 7, 5, 4, 2, 0. The greatest number is 975,420.", rnd))
    its.append(mcq_n("Use each of the digits 3, 0, 8, 1, 6 and 5 once. What is the smallest 6-digit number you can make?",
                     103568, [13568, 130568, 865310],
                     "Put the smallest digits first, but a 6-digit number cannot start with 0. Start with 1, then 0, "
                     "then 3, 5, 6, 8: 103,568. (013,568 is really 13,568, a 5-digit number.)", rnd))
    assert len(its) == 20
    order = its[:4] + its[13:15] + its[4:10] + its[15:16] + its[10:13] + its[16:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers up to 1,000,000", "items": order}


# ============================================================ set 4: negative numbers and counting through zero
def set_negative(rnd):
    its = []
    for v in [-3, -7, -6]:                                       # number line (3)
        q = fig(neg_line_svg(-10, 10, [-10, -5, 0, 5, 10], arrow=v)) + "What number does the arrow point to?"
        if v > -5:
            e = ("The arrow is to the left of 0, so the number is negative. Count back from 0: %s. The answer is %s."
                 % (", ".join(c(-k) for k in range(1, -v + 1)), c(v)))
        else:
            e = ("The arrow is to the left of 0, so the number is negative. It is %d mark%s past %s: count %s. "
                 "The answer is %s." % (-5 - v, "" if v == -6 else "s", c(-5),
                                        ", ".join(c(-k) for k in range(6, -v + 1)), c(v)))
        its.append(mcq_z(q, v, [-v, v - 1, v + 1], e, rnd))
    for v, cands in [(-4, [4, -3, -5]), (-7, [7, -6, -8]), (6, [-6, 5, 7])]:   # thermometer (3)
        q = fig(thermo_svg(-10, 10, v)) + "What temperature does the thermometer show?"
        if v < 0:
            e = ("The red line ends below 0, so the temperature is negative. Each mark is 1 degree. "
                 "Count down from 0: %s. It shows %s." % (", ".join(c(-k) for k in range(1, -v + 1)), deg(v)))
        else:
            e = ("The red line ends above 0, so the temperature is positive. Each mark is 1 degree. "
                 "It is 1 mark above 5: %s." % deg(v))
        its.append(mcq_z(q, v, cands, e, rnd, fmt=deg))
    # sequences through zero (4): (seq, step, wrongs)
    for seq, s, wrong in [([8, 5, 2], -3, [1, -2, 0]),
                          ([15, 10, 5, 0], -5, [5, -10, -1]),
                          ([-11, -8, -5], 3, [2, -1, -3]),
                          ([-7, -4, -1], 3, [1, 3, -4])]:
        ans = seq[-1] + s
        for a, b in zip(seq, seq[1:]):
            assert b - a == s
        assert ans != 0 and ans not in wrong
        steps = [seq[-1] + (k if s > 0 else -k) for k in range(1, abs(s) + 1)]
        e = ("The numbers go %s by %d each time. Count %s %d from %s, one at a time: %s. "
             % ("up" if s > 0 else "down", abs(s), "on" if s > 0 else "back", abs(s), c(seq[-1]),
                ", ".join(c(v) for v in steps)))
        e += ("Remember to count 0. " if 0 in steps[:-1] else "") + "The answer is %s." % c(ans)
        if s == -5:
            e = "5 less than 0 is 5 below zero, so it is %s. Do not forget the minus sign: 5 is above zero." % c(ans)
        its.append(mcq_z("%s: %s, ? What comes next?" % ("Count on in %ss" % s if s > 0 else "Count back in %ss" % -s,
                                                         ", ".join(c(v) for v in seq)), ans, wrong, e, rnd))
    # count on / back (4): (start, step, wrongs) wrongs = skipped 0, ignored the sign, went the wrong way
    for a, s, wrong in [(-3, 7, [5, 3, -10]), (2, -6, [-5, 4, 8]), (5, -8, [-4, 3, 13]), (-8, 5, [3, -13, -2])]:
        ans = a + s
        steps = [a + (k if s > 0 else -k) for k in range(1, abs(s) + 1)]
        e = "Count %s %d from %s: %s." % ("on" if s > 0 else "back", abs(s), c(a), ", ".join(c(v) for v in steps))
        e += (" Do not skip 0." if 0 in steps else " You stay below 0.") + " The answer is %s." % c(ans)
        its.append(mcq_z("Count %s %d from %s. Where do you land?" % ("on" if s > 0 else "back", abs(s), c(a)),
                         ans, wrong, e, rnd))
    # compare and order (3)
    its.append(mcq("Which is true?", "%s &lt; %s" % (c(-6), c(-2)),
                   ["%s &gt; %s" % (c(-6), c(-2)), "%s &lt; %s" % (c(-2), c(-6)), "%s = %s" % (c(-6), c(-2))],
                   "On a number line %s is further left than %s, so it is smaller: %s &lt; %s. "
                   "Below 0, the bigger the number after the minus sign, the smaller the number."
                   % (c(-6), c(-2), c(-6), c(-2)), rnd))
    temps = [-3, 4, -8, 1]
    o = sorted(temps)
    fmt = lambda l: ", ".join(deg(v) for v in l)
    its.append(mcq("Put these temperatures in order from coldest to warmest: %s." % fmt(temps), fmt(o),
                   [fmt(sorted(temps, key=abs)), fmt(o[::-1]), fmt([o[1], o[0], o[2], o[3]])],
                   "The coldest is the furthest below 0: %s, then %s. Then the temperatures above 0: %s, %s. "
                   "Order: %s." % (deg(-8), deg(-3), deg(1), deg(4), fmt(o)), rnd))
    its.append(mcq("Which temperature is the warmest?", deg(-1), [deg(-9), deg(-4), deg(-6)],
                   "All four are below 0. The warmest is the closest to 0: %s is only 1 degree below 0." % deg(-1), rnd))
    # difference across zero (3)
    for a, b, f in [(-4, 6, True), (-5, 3, True), (-7, -2, False)]:
        d = b - a
        if f:
            q = fig(neg_line_svg(-10, 10, [-10, -5, 0, 5, 10], dots=[a, b])) + \
                "The dots show %s and %s. How many steps apart are they?" % (c(a), c(b))
            e = ("Count in two jumps through 0. From %s to 0 is %d. From 0 to %d is %d. %d + %d = %d. "
                 "Do not work out %d − %d." % (c(a), -a, b, b, -a, b, d, max(-a, b), min(-a, b)))
            wrong = [abs(-a - b), d - 1, d + 1]
        else:
            q = "How many steps is it from %s up to %s on a number line?" % (c(a), c(b))
            e = ("Both numbers are below 0. Count up from %s: %s. That is %d steps."
                 % (c(a), ", ".join(c(v) for v in range(a + 1, b + 1)), d))
            wrong = [-a - b, d + 1, d - 1]
        its.append(mcq_z(q, d, wrong, e, rnd))
    assert len(its) == 20
    order = its[0:3] + its[3:6] + its[14:17] + its[6:10] + its[10:14] + its[17:20]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Negative numbers in context and counting through zero", "items": order}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    pound = lambda v: "£" + c(v)
    its.append(mcq_n("A house is for sale for £385,450. What is the value of the digit 8 in the price?", 80000,
                     [8000, 800000, 8],
                     "385,450 has 3 hundred thousands, 8 ten thousands, 5 thousands, 4 hundreds, 5 tens and 0 ones. "
                     "The 8 is in the ten thousands place, so it is worth £80,000.", rnd, fmt=pound))
    its.append(mcq("At the 2021 census, Leeds had a population of 811,953. How is this number written in words?",
                   words(811953), [words(811593), words(81953), words(811935)],
                   "Split at the comma: 811 thousand, then 953. Say “eight hundred and eleven thousand”, then "
                   "“nine hundred and fifty-three”.", rnd))
    cities = [("Sheffield", 556521), ("Bristol", 472465), ("Leeds", 811953), ("Manchester", 551938)]
    o = sorted(cities, key=lambda x: -x[1])
    nm = lambda l: ", ".join(x[0] for x in l)
    its.append(mcq("These are the populations of four cities at the 2021 census: %s. Which list orders the cities from "
                   "greatest to smallest population?" % "; ".join("%s %s" % (n, c(v)) for n, v in cities), nm(o),
                   [nm([o[0], o[2], o[1], o[3]]), nm(o[::-1]), nm([o[1], o[0], o[2], o[3]])],
                   "Leeds is the only one with 8 hundred thousands, and Bristol has only 4. Sheffield and Manchester "
                   "both have 5 hundred thousands and 5 ten thousands; compare the thousands: 6 &gt; 1. "
                   "Order: %s." % nm(o), rnd))
    its.append(mcq_n("A football club’s total attendance for the season was two hundred and six thousand and forty. "
                     "How is this written in digits?", 206040, [260040, 206400, 26040],
                     "Two hundred and six thousand → 206. Forty → 040 (no hundreds, so write 0). "
                     "Fill every empty place with 0: 206,040.", rnd))
    its.append(mcq_n("A stadium had 58,900 fans at one match. At the next match there were 10,000 more fans. "
                     "How many fans were at the next match?", 68900, [59900, 158900, 48900],
                     "10,000 more: only the ten thousands digit changes. 5 ten thousands → 6 ten thousands. "
                     "58,900 + 10,000 = 68,900 fans.", rnd))
    its.append(mcq_n("A town had a population of 99,400. Five years later it had grown by 1,000 people. "
                     "What is the population now?", 100400, [90400, 109400, 99500],
                     "9 thousands + 1 thousand = 10 thousands, so exchange for 1 ten thousand. Then 9 + 1 = 10 ten "
                     "thousands, so exchange again for 1 hundred thousand. 99,400 + 1,000 = 100,400.", rnd))
    its.append(mcq("Which of these house prices is the highest?", "£490,500", ["£409,950", "£490,050", "£94,995"],
                   "£94,995 has only 5 digits, so it is the lowest. The others all have 4 hundred thousands. "
                   "£490,500 and £490,050 have 9 ten thousands; compare the hundreds: 5 &gt; 0. "
                   "£490,500 is the highest.", rnd))
    its.append(mcq_z("One winter morning in Aberdeen the temperature was %s at 6 am. By noon it was 4 °C. "
                     "By how many degrees did the temperature rise?" % deg(-5), 9, [1, 8, 10],
                     "Count up in two jumps through 0. From %s to 0 °C is 5 degrees. From 0 °C to 4 °C is 4 degrees. "
                     "5 + 4 = 9 degrees. (5 − 4 = 1 is the mistake of not crossing 0.)" % deg(-5), rnd,
                     fmt=lambda v: "%d degree%s" % (v, "" if v == 1 else "s")))
    its.append(mcq_z("At 4 pm the temperature was 2 °C. By midnight it had fallen by 6 degrees. "
                     "What was the temperature at midnight?", -4, [4, -5, -8],
                     "Fallen means count down. From 2 count down 6: 1, 0, %s, %s, %s, %s. Do not skip 0. It was %s."
                     % (c(-1), c(-2), c(-3), c(-4), deg(-4)), rnd, fmt=deg))
    its.append(mcq("A shop has four freezers. Their temperatures are %s. Which is the coldest?"
                   % ", ".join(deg(v) for v in [-18, -21, -15, -19]), deg(-21), [deg(-15), deg(-18), deg(-19)],
                   "The coldest temperature is the one furthest below 0. %s is 21 degrees below 0, more than any of "
                   "the others." % deg(-21), rnd))
    name, he, his = P.next()
    its.append(mcq("In a shopping centre the ground floor is level 0. The car park levels below it are level %s, "
                   "level %s and level %s. %s gets into the lift on level 2 and goes down 4 levels. "
                   "Which level is %s on now?" % (c(-1), c(-2), c(-3), name, he),
                   "level " + c(-2), ["level 2", "level " + c(-3), "level 6"],
                   "Count down 4 from level 2: 1, 0, %s, %s. Do not skip level 0. %s is on level %s."
                   % (c(-1), c(-2), cap(he), c(-2)), rnd))
    its.append(mcq("A theme park had 300,000 visitors by the end of May, 400,000 by the end of June and 500,000 by the "
                   "end of July. The total goes up by 100,000 each month. By the end of which month will it reach "
                   "900,000?", "November", ["October", "December", "September"],
                   "Count on in 100,000s: August 600,000, September 700,000, October 800,000, November 900,000.", rnd))
    its.append(mcq_n("A school website had 245,000 visits last year. This year it had 100,000 more. "
                     "How many visits did it have this year?", 345000, [255000, 246000, 145000],
                     "100,000 more: only the hundred thousands digit changes. 2 → 3. 245,000 + 100,000 = 345,000.", rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s has the digit cards 0, 4, 7, 2, 9 and 6. %s uses each card once to make the smallest "
                     "6-digit number %s can. What number does %s make?" % (name, cap(she), she, she),
                     204679, [24679, 240679, 976420],
                     "Put the smallest digits first, but a 6-digit number cannot start with 0. Start with 2, then 0, "
                     "then 4, 6, 7, 9: 204,679. (024,679 is really 24,679, a 5-digit number.)", rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s thinks of a number. It has 4 hundred thousands, 0 ten thousands, 7 thousands, 0 hundreds, "
                     "3 tens and 5 ones. What is %s number?" % (name, her), 407035, [470035, 407350, 47035],
                     "Write the digits in order: 4, 0, 7, 0, 3, 5 → 407,035. The zeros keep every digit in the right "
                     "place.", rnd))
    its.append(mcq_n("The average distance from the Earth to the Moon is 384,400 km. What is the value of the digit 3?",
                     300000, [30000, 3000, 3], "The 3 is in the hundred thousands place, so it is worth 300,000 km.", rnd,
                     fmt=lambda v: c(v) + " km"))
    name, she, her = P.next()
    its.append(mcq_z("%s is diving. %s is 8 m below sea level (%s m). %s swims up 5 m. Where is %s now?"
                     % (name, cap(she), c(-8), cap(she), she), -3, [3, -13, 13],
                     "Swimming up means count up. From %s count up 5: %s, %s, %s, %s, %s. %s is still below sea "
                     "level: %s m." % (c(-8), c(-7), c(-6), c(-5), c(-4), c(-3), cap(she), c(-3)), rnd,
                     fmt=lambda v: c(v) + " m"))
    tk = [65407, 65740, 65074]
    ot = sorted(tk)
    fmt = lambda l: ", ".join(c(v) for v in l)
    its.append(mcq("Three concerts sold %s tickets. Which list shows these numbers from smallest to greatest?" % fmt(tk),
                   fmt(ot), [fmt([ot[1], ot[0], ot[2]]), fmt([ot[0], ot[2], ot[1]]), fmt(ot[::-1])],
                   "All three have 65 thousand. Compare the hundreds: 0 &lt; 4 &lt; 7. "
                   "Order: %s." % fmt(ot), rnd))
    its.append(mcq_n("A charity wants to raise £1,000,000. It has raised £960,000 so far. It raises £10,000 each week. "
                     "How many more weeks will it take to reach £1,000,000?", 4, [40, 3, 5],
                     "Count on in 10,000s from £960,000: £970,000, £980,000, £990,000, £1,000,000. That is 4 jumps, "
                     "so 4 weeks.", rnd, fmt=lambda v: "%d week%s" % (v, "" if v == 1 else "s")))
    its.append(mcq("At the 2021 census, Cardiff had a population of 362,400. Which digit is in the ten thousands place?",
                   "6", ["3", "2", "4"],
                   "Read the places from the left: 3 hundred thousands, 6 ten thousands, 2 thousands, 4 hundreds. "
                   "The ten thousands digit is 6.", rnd))
    assert len(its) == 20
    tail = its[1:]
    rnd.shuffle(tail)
    return {"title": "Place value and negative number word problems", "items": its[:1] + tail}


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
        "<h2>Place value up to 1,000,000</h2>"
        "<p>A 6-digit number has two groups of three digits: <b>thousands</b> and <b>ones</b>. "
        "Each group has hundreds, tens and ones. Each place is worth 10 times the place to its right. "
        "10 hundred thousands make <b>1,000,000</b> (one million).</p>"
        "<figure class='sn-fig'>" + chart_svg(304020, hi=3) +
        "<figcaption>304,020: the 4 is in the thousands place, so it is worth 4,000. "
        "The zeros hold the empty places.</figcaption></figure>"
        "<h2>Reading and writing big numbers</h2>"
        "<p>Read the thousands group and say “thousand”, then read the last three digits. "
        "In words we write “and” before the last tens and ones.</p>" +
        table(["Digits", "Words"], [
            ["304,020", words(304020)],
            ["90,712", words(90712)],
            ["1,000,000", "one million"],
        ]) +
        ex("Words to digits", "Write two hundred and fifty thousand and nine in digits.",
           "Two hundred and fifty thousand → 250. Nine → 009 (no hundreds or tens, so write 0s).",
           "250,009") +
        "<h2>Counting in powers of 10</h2>"
        "<p>To count on or back in 10s, 100s, 1,000s, 10,000s or 100,000s, change the digit in that place. "
        "When a 9 goes up, exchange: 10 of one place make 1 of the next place.</p>" +
        table(["Number", "10,000 more", "100,000 less"], [
            ["245,318", "255,318", "145,318"],
            ["896,000", "906,000", "796,000"],
            ["503,214", "513,214", "403,214"],
        ]) +
        ex("Exchange", "What is 1,000 more than 39,600?",
           "9 thousands + 1 thousand = 10 thousands. Exchange them for 1 ten thousand: 3 ten thousands become 4.",
           "40,600") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 6-digit number is greater than any 5-digit number. If both have the same "
        "number of digits, compare place by place from the left until two digits are different.</p>" +
        ex("Compare", "306,500 ☐ 360,050",
           "Hundred thousands: 3 = 3. Ten thousands: 0 &lt; 6.", "306,500 &lt; 360,050") +
        "<figure class='sn-fig'>" + number_line_svg(300000, 400000, 10000, [300000, 350000, 400000], 360000) +
        "<figcaption>From 300,000 to 400,000 there are 10 jumps, so each mark is 10,000. "
        "The arrow points to 360,000.</figcaption></figure>"
        "<h2>Negative numbers and counting through zero</h2>"
        "<p>Numbers below 0 are <b>negative</b>. We meet them in temperatures, below sea level and in lifts. "
        "When you count through zero, 0 is one of the steps.</p>"
        "<figure class='sn-fig'>" + neg_line_svg(-5, 5, list(range(-5, 6)), g=34, hops=(2, -4)) +
        "<figcaption>Count back 6 from 2: 1, 0, " + ", ".join(c(-k) for k in range(1, 5)) +
        ". You land on " + c(-4) + ".</figcaption></figure>" +
        ex("Temperature", "The temperature was " + deg(-4) + ". It rose to 6 °C. By how many degrees did it rise?",
           "4 degrees up to 0 °C, then 6 more degrees: 4 + 6 = 10.", "10 degrees") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Missing a zero placeholder (three hundred and four thousand and twenty → 34,020)",
             "Write each group as three digits: 304 | 020 → 304,020"],
            ["Giving the digit, not its value (the 4 in 304,020 is 4)", "It is in the thousands place: 4,000"],
            ["Changing the wrong digit (10,000 more than 245,318 → 246,318)",
             "Find the ten thousands digit: 255,318"],
            ["Comparing the first digits only (99,850 &gt; 100,400)", "Count the digits first: 100,400 &gt; 99,850"],
            ["Skipping 0 when counting through zero (2, 1, " + c(-1) + ")", "Say 0: 2, 1, 0, " + c(-1)],
        ])
    )


FAQ = [
    {"q": "What place value do Year 5 children need to know?",
     "a": "Year 5 pupils read, write, order and compare numbers up to 1,000,000 and know the value of each digit. "
          "They count on and back in steps of 10, 100, 1,000, 10,000 and 100,000, and use negative numbers in "
          "context, counting through zero."},
    {"q": "How do you write 304,020 in words?",
     "a": "Read the thousands group, then the rest: three hundred and four thousand and twenty. When you write it "
          "back in digits, put 0 in every empty place."},
    {"q": "How do you find 10,000 more or less than a number?",
     "a": "Change the ten thousands digit by 1 and keep the other digits the same: 10,000 more than 245,318 is "
          "255,318. If the digit is 9, exchange 10 ten thousands for 1 hundred thousand: 896,000 + 10,000 = 906,000."},
    {"q": "Do Year 5 children learn negative numbers?",
     "a": "Yes. The National Curriculum asks Year 5 pupils to interpret negative numbers in context, such as "
          "temperatures, and to count forwards and backwards through zero, for example 2, 1, 0, −1, −2."},
]


def mark_large(u, pattern):
    """Tag wide pictures (charts, number lines, thermometers) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(5501)
    P = People(rnd)
    used = set()
    sets = [set_value(rnd, used), set_count(rnd), set_compare(rnd, used), set_negative(rnd), set_words(rnd, P)]
    balance(sets, rnd)
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [x.replace(",", "") for x in it["c"]]
            assert len(set(vals)) == 4, it
            assert it["q"].count("<svg") <= 1
            key = (it["q"], tuple(sorted(it["c"])))
            assert key not in allq, it["q"]
            allq.add(key)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "place-value-to-a-million", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value to 1,000,000, Counting in Powers of 10 and Negative Numbers",
        "seo_title": "Year 5 Place Value Worksheets: Numbers to a Million and Negative Numbers (Free)",
        "short_title": "Place value to a million",
        "domain": "Number and place value",
        "standard_code": "Year 5: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read, write, order and compare numbers to at least 1,000,000 and determine the value of each digit; count forwards or backwards in steps of powers of 10 for any given number up to 1,000,000; interpret negative numbers in context, count forwards and backwards with positive and negative whole numbers, including through zero.",
        "meta_desc": "Free Year 5 maths worksheets for the National Curriculum: place value up to 1,000,000, numbers in words, counting in steps of 10, 100, 1,000, 10,000 and 100,000, comparing and ordering, and negative numbers through zero. 100 questions with an answer key.",
        "key_big": "In a 6-digit number, each digit is worth hundreds, tens or ones of thousands, or hundreds, tens or ones. The place decides the value.",
        "key_sub": "The 4 in 304,020 is worth 4,000. Write 0 in every empty place, change only one digit when you count in powers of 10 (exchange when a 9 goes up), and say 0 when you count through zero.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(place value chart|number line|thermometer)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
