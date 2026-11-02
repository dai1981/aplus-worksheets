# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Place Value, Rounding and Negative Numbers
(National Curriculum in England, Year 6: Number and place value)
  python3 tools/gen_uk_maths_y6_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are written with commas. Negative numbers use the real minus sign − (U+2212).
Wrong answers come from real mistakes: giving the digit instead of its value, missing zero placeholders when
writing words as numerals (4,600,005 for 4,060,005), comparing the first digits only, rounding the wrong way or to
the wrong place, keeping the digits after the rounding place, forgetting to exchange a 9, rounding twice, and
working out an interval across zero as 7 − 5 = 2 instead of 7 + 5 = 12.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
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

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions", "ten millions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million", "ten million"]


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


def lg(p):
    return len(str(p)) - 1


def plural(d, i):
    if i == 6:
        return "%d million" % d
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def expanded(n):
    return " + ".join(c(digit(n, i) * 10 ** i) for i in range(ndig(n) - 1, -1, -1) if digit(n, i))


def zero_mistakes(n):
    """Numbers a pupil writes when a zero goes missing, moves, or is added."""
    s = str(n)
    out = []
    for i, ch in enumerate(s):
        if ch == "0":
            for j in (i - 1, i + 1):                            # zero swapped with a neighbour
                if 0 < j < len(s) and s[j] != "0":
                    l = list(s)
                    l[i], l[j] = l[j], l[i]
                    out.append(int("".join(l)))
            out.append(int(s[:i] + s[i + 1:]))                 # left out a zero
    for i in range(1, len(s)):                                  # an extra zero
        if s[i] == "0":
            out.append(int(s[:i] + "0" + s[i:]))
    return [v for v in out if v != n and 1000 <= v < 100000000]


def joined_digits(n):
    """Writing only the non-zero digits side by side (4,000,000 + 60,000 + 5 -> 465)."""
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
    """4,060,005 -> four million, sixty thousand and five."""
    assert 0 < n < 100000000
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


assert words(4060005) == "four million, sixty thousand and five"
assert words(3250412) == "three million, two hundred and fifty thousand, four hundred and twelve"
assert words(2305040) == "two million, three hundred and five thousand and forty"


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
GROUPS = [("Millions", 1), ("Thousands", 3), ("Ones", 3)]
SUB = ["O", "H", "T", "O", "H", "T", "O"]


def chart_svg(n, hi=None):
    """Millions | Thousands (H T O) | Ones (H T O) chart with a 7-digit n in it. hi = place index to colour red."""
    x0 = y0 = 6
    W, H = 2 * x0 + 7 * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, 7 * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 7 * CW, H1 + H2, FILL)]
    k = 0
    for name, span in GROUPS:
        x = x0 + k * CW
        s.append(text(x + span * CW / 2, y0 + 19, name, 14, bold=True))
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                     % (x, y0, x, y0 + H1 + H2 + ROW, GREEN))
        k += span
    for k in range(7):
        i = 6 - k
        x = x0 + k * CW
        if k not in (0, 1, 4):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (x, y0 + H1, x, y0 + H1 + H2 + ROW, GREEN))
        s.append(text(x + CW / 2, y0 + H1 + 19, SUB[k], 14, bold=True))
        s.append(text(x + CW / 2, y0 + H1 + H2 + 34, str(digit(n, i)), 28, bold=True, col=RED if hi == i else INK))
    for y in (y0 + H1, y0 + H1 + H2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + 7 * CW, y, GREEN, "1.2" if y == y0 + H1 else "2"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, 7 * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % c(n))


def number_line_svg(lo, hi, step, labels, arrow=None, dot=None, show=None):
    """Number line lo..hi, a tick every step, bold numbers at `labels`.
    arrow = red arrow (pupil reads the number); dot = red dot with its number written above (rounding)."""
    L, R, Y = 58, 422, 58
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
    if arrow is not None:
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
        if show:
            s.append(text(min(max(ax, 60), W - 60), Y - 44, show, 15, bold=True, col=RED))
    if dot is not None:
        dx = X(dot)
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (dx, Y, RED))
        s.append(text(min(max(dx, 60), W - 60), Y - 18, c(dot), 16, bold=True, col=RED))
    top = 14 if (arrow is not None and show) else 0
    if top:
        s = ["<g transform='translate(0 %d)'>" % top] + s + ["</g>"]
    return svg_wrap(W, H + top, "".join(s), "number line from %s to %s" % (c(lo), c(hi)))


def round_line(n, p):
    lo = n // p * p
    return fig(number_line_svg(lo, lo + p, p // 10, [lo, lo + p // 2, lo + p], dot=n))


def neg_line_svg(lo, hi, labels, g=19, arrow=None, dots=None, jumps=None):
    """Number line through zero, one tick for every whole number.
    dots = list of numbers marked with red dots; jumps = (a, b) draws a bracket above with its length."""
    pad = 30
    n = hi - lo
    W = 2 * pad + n * g
    Y = 52 if (jumps or arrow is not None) else 30
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
def distinct7(rnd, used):
    while True:
        d = rnd.sample(range(10), 7)
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
    for i in [5, 3, 6, 4, 2]:                                    # chart, red digit (5)
        while True:
            n = distinct7(rnd, used)
            if digit(n, i):
                break
        d = digit(n, i)
        A.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True), rnd))
    for i in [4, 5, 3, 6]:                                       # value, no chart (4)
        while True:
            n = distinct7(rnd, used)
            if digit(n, i):
                break
        d = digit(n, i)
        B.append(mcq_n("What is the value of the digit %d in %s?" % (d, c(n)), d * 10 ** i,
                       value_cands(d, i), value_e(d, i), rnd))
    for i in [5, 4]:                                             # which digit is in a place (2)
        n = distinct7(rnd, used)
        while not digit(n, i):
            n = distinct7(rnd, used)
        d = digit(n, i)
        cands = [digit(n, x) for x in sorted(range(7), key=lambda x: (abs(x - i), x)) if x != i]
        e = ("Read the places from the right: ones, tens, hundreds, thousands, ten thousands, hundred thousands, "
             "millions. In %s the %s digit is %d, worth %s." % (c(n), PL[i], d, c(d * 10 ** i)))
        C.append(mcq("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, cands, e, rnd))
    for n in [4060005, 2307080, 9004300]:                        # words -> numeral (3)
        used.add(n)
        cands = zero_mistakes(n) + [joined_digits(n)]
        m, t, o = n // 1000000, n // 1000 % 1000, n % 1000
        e = ("Write each part in its group of three digits: %s million → %d, %s thousand → %03d, then %03d. "
             "Fill every empty place with 0: %s." % (w1000(m), m, w1000(t), t, o, c(n)))
        D.append(mcq_n("Which number is <b>%s</b>?" % words(n), n, cands, e, rnd))
    for n in [5030700, 1406020]:                                 # numeral -> words (2)
        used.add(n)
        cands = [words(v) for v in zero_mistakes(n) if v >= 1000000]
        e = ("Split %s into groups: %s million, %s thousand, %s. Say each group, then its name: %s."
             % (c(n), n // 1000000, n // 1000 % 1000, n % 1000, words(n)))
        E.append(mcq("How do you write %s in words?" % c(n), words(n), cands, e, rnd))
    for n in [3407020, 6050300]:                                 # expanded -> number (2)
        used.add(n)
        cands = zero_mistakes(n) + [joined_digits(n)]
        e = "Put each digit in its place and write 0 in every empty place: %s = %s." % (expanded(n), c(n))
        F.append(mcq_n("What number is <b>%s</b>?" % expanded(n), n, cands, e, rnd))
    G.append(mcq_n("In 3,606,000, how many times greater is the value of the first 6 than the value of the second 6?",
                   100, [10, 1000, 594000],
                   "The first 6 is worth 600,000. The second 6 is worth 6,000. 600,000 ÷ 6,000 = 100. "
                   "Each place to the left is worth 10 times more, and the 6s are two places apart: 10 × 10 = 100. "
                   "(594,000 is the difference, not how many times greater.)", rnd))
    d, i = 5, 5
    others = [x for x in range(1, 10) if x != d]
    rnd.shuffle(others)
    base = others[:6]
    nums = {}
    for pos in [6, 5, 4, 3]:
        ds = base[:]
        ds.insert(6 - pos, d)
        nums[pos] = int("".join(map(str, ds)))
    assert digit(nums[i], i) == d
    H.append(mcq("Which number has a %d in the hundred thousands place?" % d, c(nums[i]),
                 [c(nums[x]) for x in nums if x != i],
                 "The hundred thousands place is the 6th digit from the right (the first digit after the millions). "
                 "In %s the %d is there, so it is worth %s." % (c(nums[i]), d, c(d * 10 ** i)), rnd))
    order = A[:3] + C + A[3:] + B + H + F + D + E + G
    assert len(order) == 20
    return {"title": "Value of each digit up to 10,000,000 and numbers in words", "items": order}


# ============================================================ set 2: compare and order
def first_diff(a, b):
    for i in range(7, -1, -1):
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
    """4 different 7-digit numbers made from the same digits, with the same millions digit."""
    while True:
        ds = rnd.sample(range(1, 10), 7)
        out = set()
        tries = 0
        while len(out) < 4 and tries < 80:
            tries += 1
            l = ds[:]
            a = rnd.randint(1, 4)
            b = a + rnd.choice([1, 2])
            l[a], l[b] = l[b], l[a]
            out.add(int("".join(map(str, l))))
        if len(out) == 4 and not (out & used):
            used.update(out)
            return sorted(out)


def set_compare(rnd, used):
    its = []
    for x, y in [(6089450, 6098450), (987654, 1002300), (5710200, 5701200), (3045600, 3405600)]:
        right = "%s %s %s" % (c(x), "&lt;" if x < y else "&gt;", c(y))
        wrong = ["%s %s %s" % (c(x), "&gt;" if x < y else "&lt;", c(y)), "%s = %s" % (c(x), c(y)),
                 "%s %s %s" % (c(y), "&lt;" if x < y else "&gt;", c(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 987654:
            e += " Big first digits do not matter when a number has fewer digits."
        its.append(mcq("Which is true?", right, wrong, e, rnd))
    for j in range(6):
        if j == 2:
            nums = [998750, 1089000, 1098000, 1009800]
        elif j == 5:
            nums = [2060400, 999999, 2006400, 2064000]
        else:
            nums = lookalikes(rnd, used)
        nums = sorted(nums)
        want_max = j < 3
        ans = nums[-1] if want_max else nums[0]
        nxt = nums[-2] if want_max else nums[1]
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % c(ans)
            if 998750 in nums:
                e = ("998,750 has only 6 digits, so it is the smallest, even though it starts with 9. "
                     "Of the 7-digit numbers: " + compare_expl(ans, nxt) + " %s is the greatest." % c(ans))
        else:
            e = compare_expl(nxt, ans) + " %s is the smallest." % c(ans)
            if 999999 in nums:
                e = ("999,999 has only 6 digits, so it is the smallest. Every 7-digit number is at least 1,000,000.")
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
    its.append(mcq_n("What is 10,000 more than 4,995,300?", 5005300, [4996300, 4005300, 5095300, 4105300],
                     "Add 1 to the ten thousands digit: 9 ten thousands + 1 = 10 ten thousands. Exchange them for "
                     "1 hundred thousand, then 9 + 1 = 10 hundred thousands, so exchange again for 1 million. "
                     "4,995,300 + 10,000 = 5,005,300.", rnd))
    its.append(mcq_n("What is 100,000 less than 2,034,500?", 1934500, [2024500, 1034500, 2933500, 2033500],
                     "There are 0 hundred thousands, so exchange 1 million for 10 hundred thousands. "
                     "10 − 1 = 9 hundred thousands and 1 million is left. 2,034,500 − 100,000 = 1,934,500.", rnd))
    for lo, v in [(2000000, 2700000), (5000000, 5400000)]:
        k = (v - lo) // 100000
        q = fig(number_line_svg(lo, lo + 1000000, 100000, [lo, lo + 500000, lo + 1000000], arrow=v)) + \
            "What number does the arrow point to?"
        e = ("From %s to %s there are 10 equal jumps, so each mark is 100,000, not 10,000. The arrow is %d marks "
             "after %s: %s + %s = %s." % (c(lo), c(lo + 1000000), k, c(lo), c(lo), c(k * 100000), c(v)))
        its.append(mcq_n(q, v, [lo + k * 10000, lo + 1000000 - k * 100000, v + 100000], e, rnd))
    its.append(mcq("5,2☐8,400 &gt; 5,276,000. Which digit could go in the box?", "8", ["4", "5", "6"],
                   "The millions and hundred thousands are the same. Compare the ten thousands: the box must be more "
                   "than 7, or equal to 7. 4, 5 and 6 are too small. 5,288,400 &gt; 5,276,000.", rnd))
    its.append(mcq("3,☐45,000 &lt; 3,412,900. Which digit could go in the box?", "3", ["4", "5", "9"],
                   "The millions are the same. Compare the hundred thousands: the box must be less than 4. "
                   "If it is 4, compare the ten thousands: 4 &gt; 1, so 3,445,000 would be too big. "
                   "3,345,000 &lt; 3,412,900.", rnd))
    its.append(mcq_n("Use each of the digits 4, 0, 8, 2, 6, 1 and 9 once. What is the greatest 7-digit number you can make?",
                     9864210, [9864201, 9846210, 1024689],
                     "Put the biggest digit in the millions place, then the next biggest, and so on: 9, 8, 6, 4, 2, 1, 0. "
                     "The greatest number is 9,864,210.", rnd))
    assert len(its) == 20
    order = its[:4] + its[13:15] + its[4:10] + its[15:17] + its[10:13] + its[17:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers up to 10,000,000", "items": order}


# ============================================================ set 3: rounding
def place(p):
    return c(p)


def round_to(n, p):
    return ((n + p // 2) // p) * p


def round_expl(n, p):
    lo = n // p * p
    r = round_to(n, p)
    k = lg(p)
    d = digit(n, k - 1)
    if n - lo == p // 2:
        s = ("%s is exactly halfway between %s and %s. A number that is exactly halfway rounds up."
             % (c(n), c(lo), c(lo + p)))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s."
             % (c(n), c(lo), c(lo + p), PL[k - 1], d,
                "5 or more" if d >= 5 else "4 or less", "up" if r > lo else "down"))
    if r > lo and digit(n, k) == 9:
        s += (" The %s digit is 9, so rounding up makes 10 %s. Exchange them for 1 %s."
              % (PL[k], PL[k], PL1[k + 1]))
    return s + " Answer: %s." % c(r)


def nine_mistakes(n, p):
    r = round_to(n, p)
    lo = n // p * p
    if r == lo or digit(n, lg(p)) != 9:
        return []
    pre = n // (p * 10)
    out = [pre * p * 10]                                       # 9 became 0, nothing exchanged
    if pre:
        out.insert(0, int(str(pre) + "10" + "0" * lg(p)))      # “10” written in the 9's place
    return out


def round_cands(n, p):
    r = round_to(n, p)
    lo = n // p * p
    other = lo + p if r == lo else lo                          # rounded the wrong way
    out = [other] + nine_mistakes(n, p)
    if r > lo:
        out.append(r + n % p)                                  # kept the digits after the place
    out.append(round_to(n, p // 10) if p >= 100 else None)     # rounded to the place on the right
    out.append(n // (p // 10) * (p // 10) if p >= 100 else None)   # cut off at the wrong place
    out.append(round_to(n, p * 10))                            # rounded to the place on the left
    out += [r + p, r - p]
    return out


class Picker:
    def __init__(self, rnd):
        self.rnd = rnd
        self.used = set()

    def take(self, n):
        assert n not in self.used, n
        self.used.add(n)
        return n

    def pick(self, lo, hi, p, ok=lambda n: True):
        while True:
            n = self.rnd.randint(lo, hi)
            if (n % p and n % 10 and n not in self.used and ok(n) and round_to(n, p) > 0
                    and digit(n, lg(p)) != 9 and n % p != p // 2 and n % (p // 10 if p > 10 else 10)):
                self.used.add(n)
                return n


def q_round(n, p, rnd, line=False):
    q = "Round %s to the nearest %s." % (c(n), place(p))
    if line:
        q = round_line(n, p) + q
    return mcq_n(q, round_to(n, p), round_cands(n, p), round_expl(n, p), rnd)


def which_rounds(target, p, right, wrong, rnd):
    assert round_to(right, p) == target
    for w in wrong:
        assert round_to(w, p) != target, (target, w)
    lo, hi = target - p // 2, target + p // 2 - 1
    e = ("Numbers from %s to %s round to %s. %s is in that range. %s rounds to %s."
         % (c(lo), c(hi), c(target), c(right), c(wrong[0]), c(round_to(wrong[0], p))))
    return mcq("Which number rounds to %s when you round to the nearest %s?" % (c(target), place(p)),
               c(right), [c(w) for w in wrong], e, rnd)


def set_round(rnd, pk):
    its = []
    for p, lo, hi in [(1000, 100000, 999999), (10000, 100000, 999999), (100000, 1000000, 9999999),
                      (1000000, 1000000, 8999999), (10000, 1000000, 9999999), (100000, 100000, 899999)]:
        its.append(q_round(pk.pick(lo, hi, p), p, rnd, True))
    for p, lo, hi in [(10, 1000000, 9999999), (100, 100000, 999999), (1000, 1000000, 9999999),
                      (10000, 1000000, 9999999), (100000, 1000000, 9999999), (1000000, 1000000, 8999999)]:
        its.append(q_round(pk.pick(lo, hi, p), p, rnd))
    for n, p in [(2450000, 100000), (3500000, 1000000), (4965300, 100000), (2397800, 10000)]:
        its.append(q_round(pk.take(n), p, rnd))
    its.append(which_rounds(4000000, 1000000, 3612000, [3450000, 4500000, 4612000], rnd))
    its.append(which_rounds(760000, 10000, 756300, [765000, 754999, 767100], rnd))
    its.append(mcq("What is the smallest whole number that rounds to 300,000 when you round to the nearest 100,000?",
                   "250,000", ["200,000", "249,999", "299,999"],
                   "Numbers from 250,000 to 349,999 round to 300,000. 249,999 has 4 ten thousands, so it rounds down "
                   "to 200,000. The smallest is 250,000.", rnd))
    n = 6348527
    assert (round_to(n, 1000), round_to(n, 100000), round_to(n, 1000000)) == (6349000, 6300000, 6000000)
    its.append(mcq("Round 6,348,527 to the nearest 1,000, the nearest 100,000 and the nearest 1,000,000. "
                   "Which list is correct?", "6,349,000; 6,300,000; 6,000,000",
                   ["6,348,000; 6,300,000; 6,000,000", "6,349,000; 6,400,000; 6,000,000",
                    "6,349,000; 6,300,000; 7,000,000"],
                   "Always round the number you started with. Nearest 1,000: the hundreds digit is 5, so 6,349,000. "
                   "Nearest 100,000: the ten thousands digit is 4, so 6,300,000. Nearest 1,000,000: the hundred "
                   "thousands digit is 3, so 6,000,000.", rnd))
    order = its[:2] + its[6:8] + its[2:4] + its[8:10] + its[12:14] + its[4:6] + its[10:12] + its[14:16] + its[16:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Round to the nearest 10, 100, 1,000, 10,000, 100,000 and 1,000,000", "items": order}


# ============================================================ set 4: negative numbers and intervals across zero
def interval_e(a, b, temp=False):
    lo, hi = min(a, b), max(a, b)
    f = deg if temp else c
    unit = " degrees" if temp else ""
    if lo < 0 < hi:
        return ("Count in two jumps through 0. From %s to %s is %d. From %s to %s is %d. %d + %d = %d%s. "
                "Do not work out %d − %d."
                % (f(lo), f(0), -lo, f(0), f(hi), hi, -lo, hi, hi - lo, unit, max(-lo, hi), min(-lo, hi)))
    return ("Both numbers are below 0. Count up from %s to %s: %d − %d = %d%s."
            % (c(lo), c(hi), -lo, -hi, hi - lo, unit))


def set_negative(rnd):
    its = []
    for v, mirror in [(-7, -3), (-13, -17), (-16, -14)]:
        q = fig(neg_line_svg(-20, 10, [-20, -15, -10, -5, 0, 5, 10], g=13, arrow=v)) + \
            "What number does the arrow point to?"
        base = -((-v) // 5 * 5)
        k = base - v
        e = ("The arrow is to the left of 0, so the number is negative. Start at %s and count %d mark%s to the left: "
             "%s. Numbers get smaller as you go left." % (c(base), k, "" if k == 1 else "s", c(v)))
        its.append(mcq_z(q, v, [-v, mirror, v - 1, v + 1], e, rnd))
    for v, cands in [(-9, [9, -11, -8]), (-4, [4, -6, -3])]:
        q = fig(thermo_svg(-15, 10, v)) + "What temperature does the thermometer show?"
        base = -((-v) // 5 * 5)
        e = ("The red line ends below 0, so the temperature is negative. Each mark is 1 degree. "
             "Start at %s and count down %d marks to the top of the red line: %s." % (deg(base), base - v, deg(v)))
        its.append(mcq_z(q, v, cands, e, rnd, fmt=deg))
    for a, b, f in [(-7, 5, True), (-4, 8, True), (-12, 6, False), (-15, -6, False), (9, -13, False)]:
        q = "What is the difference between %s and %s?" % (c(a), c(b))
        if f:
            q = fig(neg_line_svg(-10, 10, [-10, -5, 0, 5, 10], g=19, dots=[a, b])) + \
                "The dots show %s and %s. What is the difference between them?" % (c(a), c(b))
        d = abs(a - b)
        cands = [abs(abs(a) - abs(b)), -d, d + 1, d - 1]
        if a < 0 and b < 0:
            cands = [abs(a) + abs(b), -d, d + 1]
        its.append(mcq_z(q, d, cands, interval_e(a, b), rnd))
    for a, op, b in [(-4, "+", 9), (3, M, 8), (-6, M, 5), (-12, "+", 7)]:
        r = a + b if op == "+" else a - b
        if op == "+":
            e = "Start at %s and count up %d: %s. You pass 0 on the way." % (c(a), b, c(r)) if r > 0 else \
                "Start at %s and count up %d. You stay below 0: %s." % (c(a), b, c(r))
            cands = [-r, a - b, -(a - b) if a - b < 0 else None, abs(a) + b]
        else:
            e = ("Start at %s and count down %d. %s"
                 % (c(a), b, "Count down to 0 (%d), then %d more below 0: %s." % (a, b - a, c(r)) if a > 0
                    else "Going down from a negative number makes it more negative: %s." % c(r)))
            cands = [-r, a + b, -(a + b), abs(a) - b]
        its.append(mcq_z("Calculate %s %s %d." % (c(a), op, b), r, cands, e, rnd))
    temps = [-3, -8, 2, -1]
    o = sorted(temps)
    fmt = lambda l: ", ".join(deg(v) for v in l)
    its.append(mcq("Put these temperatures in order from coldest to warmest: %s." % fmt(temps), fmt(o),
                   [fmt(sorted(temps, key=abs)), fmt(o[::-1]), fmt([o[3], o[0], o[1], o[2]])],
                   "Below 0, the bigger the number after the minus sign, the colder it is. %s is the coldest and "
                   "%s is the only one above 0. Order: %s." % (deg(-8), deg(2), fmt(o)), rnd))
    its.append(mcq("Which temperature is the warmest?", deg(-2), [deg(-12), deg(-9), deg(-5)],
                   "All four are below 0. The warmest is the closest to 0: %s is only 2 degrees below 0." % deg(-2), rnd))
    for seq, s, ans, wrong in [([19, 12, 5], 7, -2, [2, -3, -1]), ([15, 9, 3], 6, -3, [3, -2, -4])]:
        assert seq[-1] - s == ans
        e = ("The numbers go down by %d each time. %d − %d: count down %d to 0, then %d more: %s."
             % (s, seq[-1], s, seq[-1], s - seq[-1], c(ans)))
        its.append(mcq_z("The numbers go down by %d each time: %s, ? What comes next?" % (s, ", ".join(map(str, seq))),
                         ans, wrong, e, rnd))
    its.append(mcq_z("What number is exactly halfway between %s and 10?" % c(-6), 2, [8, 4, -2],
                     "The difference between %s and 10 is 6 + 10 = 16. Half of 16 is 8. Count 8 up from %s: %s + 8 = 2. "
                     "(8 is the size of the half, not the number.)" % (c(-6), c(-6), c(-6)), rnd))
    its.append(mcq_z("%s − ☐ = %s. What number goes in the box?" % (c(-3), c(-10)), 7, [-7, 13, -13],
                     "From %s down to %s is 7 steps, so take away 7. Check: %s − 7 = %s." % (c(-3), c(-10), c(-3), c(-10)),
                     rnd))
    order = its[:3] + its[3:5] + its[16:17] + its[14:16] + its[5:7] + its[10:12] + its[17:19] + its[7:10] + \
        its[12:14] + its[19:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Negative numbers and intervals across zero", "items": order}


# ============================================================ set 5: word problems
def unit_fmt(pre="", post=""):
    return lambda v: pre + c(v) + post


def story(t, n, p, rnd, pre="", post=""):
    f = unit_fmt(pre, post)
    r = round_to(n, p)
    return mcq_n(t, r, round_cands(n, p), round_expl(n, p).replace("Answer: %s." % c(r), "Answer: %s." % f(r)), rnd, fmt=f)


def set_words(rnd, P):
    its = []
    its.append(mcq_n("At the 2021 census, Birmingham had a population of 1,144,919. What is the value of the first 4 "
                     "in this number?", 40000, [4000, 400000, 4],
                     "1,144,919 has 1 million, 1 hundred thousand, 4 ten thousands, 4 thousands, 9 hundreds, 1 ten "
                     "and 9 ones. The first 4 is in the ten thousands place, so it is worth 40,000.", rnd))
    its.append(story("At the 2021 census, Leeds had a population of 811,953. What is this rounded to the nearest 10,000?",
                     811953, 10000, rnd, post=" people"))
    cities = [("Sheffield", 556521), ("Bristol", 472465), ("Leeds", 811953), ("Manchester", 551938)]
    o = sorted(cities, key=lambda x: -x[1])
    nm = lambda l: ", ".join(x[0] for x in l)
    its.append(mcq("These are the populations of four cities at the 2021 census: %s. Which list orders the cities from "
                   "greatest to smallest population?" % "; ".join("%s %s" % (n, c(v)) for n, v in cities), nm(o),
                   [nm([o[0], o[2], o[1], o[3]]), nm(o[::-1]), nm([o[1], o[0], o[2], o[3]])],
                   "Leeds is the only one with 8 hundred thousands, and Bristol has only 4. Sheffield and Manchester "
                   "both have 5 hundred thousands and 5 ten thousands; compare the thousands: 6 &gt; 1. "
                   "Order: %s." % nm(o), rnd))
    its.append(mcq_n("A football club’s total attendance for the season was two million, forty thousand and fifty. "
                     "How is this written in digits?", 2040050, [2400050, 2040500, 240050, 2004050],
                     "2 million → 2, forty thousand → 040, fifty → 050. Fill every empty place with 0: 2,040,050.", rnd))
    its.append(story("A crowd of 74,310 fans watched a cup final. What is the crowd to the nearest 1,000?",
                     74310, 1000, rnd, post=" fans"))
    its.append(mcq_z("One winter day in Edinburgh the temperature was %s at 6 am and 7 °C at 2 pm. "
                     "By how many degrees did the temperature rise?" % deg(-6), 13, [1, 12, 14],
                     interval_e(-6, 7, True), rnd,
                     fmt=lambda v: "%d degree%s" % (v, "" if v == 1 else "s")))
    its.append(mcq_z("A freezer is at %s. A fridge is at 4 °C. How many degrees warmer is the fridge?" % deg(-18),
                     22, [14, 21, 23],
                     interval_e(-18, 4, True), rnd, fmt=lambda v: "%d degrees" % v))
    its.append(mcq_z("At 6 pm the temperature was 3 °C. During the night it fell by 9 degrees. "
                     "What was the temperature then?", -6, [6, -5, -12],
                     "Fell means count down. Count down 3 to reach 0, then 6 more: %s. (3 − 9 is not 6.)" % deg(-6),
                     rnd, fmt=deg))
    its.append(mcq_z("At midnight the temperature was %s. By 9 am it had risen by 5 degrees. "
                     "What was the temperature at 9 am?" % deg(-8), -3, [3, -13, 13],
                     "Risen means count up. From %s count up 5: %s, %s, %s, %s, %s. It is still below 0: %s."
                     % (deg(-8), c(-7), c(-6), c(-5), c(-4), c(-3), deg(-3)), rnd, fmt=deg))
    name, he, his = P.next()
    its.append(mcq("In a shopping centre, the ground floor is level 0 and the car park levels are %s and %s. "
                   "%s takes the lift from level 3 down to level %s. How many levels does %s go down?"
                   % (c(-1), c(-2), name, c(-2), he), "5 levels", ["1 level", "6 levels", "4 levels"],
                   "From level 3 down to 0 is 3 levels. From 0 down to %s is 2 levels. 3 + 2 = 5 levels." % c(-2), rnd))
    its.append(story("A house was sold for £348,750. What is the price to the nearest £10,000?", 348750, 10000, rnd,
                     pre="£"))
    its.append(story("A charity raised £2,495,600. What is this to the nearest £100,000?", 2495600, 100000, rnd, pre="£"))
    its.append(story("The average distance from the Earth to the Moon is 384,400 km. What is this to the nearest 10,000 km?",
                     384400, 10000, rnd, post=" km"))
    for w in [60512, 59412, 60500]:
        assert round_to(w, 1000) != 60000
    assert round_to(59612, 1000) == 60000
    its.append(mcq("A newspaper says “about 60,000 fans” went to a concert. The number was rounded to the nearest 1,000. "
                   "Which could be the real number of fans?", "59,612", ["60,512", "59,412", "60,500"],
                   "Numbers from 59,500 to 60,499 round to 60,000. 59,612 is in that range. 60,512 and 60,500 round up "
                   "to 61,000, and 59,412 rounds down to 59,000.", rnd))
    its.append(mcq("The population of a town, rounded to the nearest 10,000, is 250,000. "
                   "What is the smallest the population could be?", "245,000", ["240,000", "249,999", "254,999"],
                   "Numbers from 245,000 to 254,999 round to 250,000. 244,999 would round down to 240,000, "
                   "so the smallest is 245,000. (254,999 is the greatest.)", rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s has the digit cards 7, 0, 3, 9, 1, 5 and 2. %s uses each card once to make the smallest "
                     "7-digit number %s can. What number does %s make?" % (name, cap(she), she, she),
                     1023579, [123579, 1203579, 9753210],
                     "Put the smallest digits first, but a 7-digit number cannot start with 0. Start with 1, then 0, "
                     "then 2, 3, 5, 7, 9: 1,023,579. (0,123,579 is really 123,579, a 6-digit number.)", rnd))
    its.append(mcq_z("A submarine is at %s m (250 m below sea level). It rises 180 m. Where is it now?" % c(-250),
                     -70, [-430, 70, -130], "Rising means count up. %s + 180: it is still 70 m below sea level, so %s m."
                     % (c(-250), c(-70)), rnd, fmt=lambda v: c(v) + " m"))
    its.append(mcq_n("A diver is 12 m below sea level. A seagull is flying 15 m above sea level, straight above the diver. "
                     "How far apart are they?", 27, [3, 26, 28],
                     "From 12 m below sea level up to sea level is 12 m. From sea level up to the seagull is 15 m. "
                     "12 + 15 = 27 m. (15 − 12 = 3 is the mistake of not crossing 0.)", rnd, fmt=lambda v: c(v) + " m"))
    its.append(mcq_n("A theme park had 1,995,800 visitors last year. This year it had 10,000 more. "
                     "How many visitors did it have this year?", 2005800, [1996800, 2095800, 1905800],
                     "Add 1 to the ten thousands digit: 9 + 1 = 10, so exchange for 1 hundred thousand. Then 9 + 1 = 10 "
                     "hundred thousands, so exchange for 1 million. 1,995,800 + 10,000 = 2,005,800.", rnd))
    name, he, his = P.next()
    its.append(mcq_n("A museum had 1,463,000 visitors in a year. %s rounds this to the nearest 100,000 first, then "
                     "rounds %s answer to the nearest 1,000,000 and gets 2,000,000. What is 1,463,000 rounded to the "
                     "nearest 1,000,000?" % (name, his), 1000000, [2000000, 1500000, 1460000],
                     "Always round the original number. Look at the hundred thousands digit of 1,463,000: 4. "
                     "4 or less, so round down to 1,000,000. Rounding twice (1,463,000 → 1,500,000 → 2,000,000) gives "
                     "the wrong answer.", rnd))
    assert len(its) == 20
    tail = its[1:]
    rnd.shuffle(tail)
    return {"title": "Place value, rounding and negative number word problems", "items": its[:1] + tail}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    n = 3462718
    return (
        "<h2>Place value up to 10,000,000</h2>"
        "<p>Big numbers are split into groups of three digits: <b>millions</b>, <b>thousands</b> and <b>ones</b>. "
        "Each group has hundreds, tens and ones. Each place is worth 10 times the place to its right.</p>"
        "<figure class='sn-fig'>" + chart_svg(4060005, hi=4) +
        "<figcaption>4,060,005: the 6 is in the ten thousands place, so it is worth 60,000. "
        "The zeros hold the other places.</figcaption></figure>"
        "<h2>Reading and writing large numbers</h2>"
        "<p>Read each group of three digits, then say its name: million, thousand. "
        "In words we write “and” before the last tens and ones.</p>" +
        table(["Digits", "Words"], [
            ["4,060,005", words(4060005)],
            ["3,250,412", words(3250412)],
            ["10,000,000", "ten million"],
        ]) +
        ex("Words to digits", "Write two million, three hundred and five thousand and forty in digits.",
           "2 million → 2. Three hundred and five thousand → 305. Forty → 040 (no hundreds, so write 0).",
           "2,305,040") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 7-digit number is greater than any 6-digit number. If both have the same "
        "number of digits, compare place by place from the left until two digits are different.</p>" +
        ex("Compare", "5,710,200 ☐ 5,701,200",
           "Millions: 5 = 5. Hundred thousands: 7 = 7. Ten thousands: 1 &gt; 0.", "5,710,200 &gt; 5,701,200") +
        "<h2>Rounding to any place</h2>"
        "<ol class='rk-step'><li>Find the digit in the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to its right</b>.</li>"
        "<li><b>5 or more</b>: round up. <b>4 or less</b>: round down.</li>"
        "<li>Change every digit after the rounding place to 0.</li></ol>"
        "<figure class='sn-fig'>" + number_line_svg(3400000, 3500000, 10000, [3400000, 3450000, 3500000], dot=n) +
        "<figcaption>3,462,718 is past the halfway point, 3,450,000, so to the nearest 100,000 it rounds to "
        "3,500,000.</figcaption></figure>" +
        table(["Round 3,462,718 to the nearest", "Look at", "Answer"], [
            ["10", "the ones digit: 8", c(round_to(n, 10))],
            ["100", "the tens digit: 1", c(round_to(n, 100))],
            ["1,000", "the hundreds digit: 7", c(round_to(n, 1000))],
            ["10,000", "the thousands digit: 2", c(round_to(n, 10000))],
            ["100,000", "the ten thousands digit: 6", c(round_to(n, 100000))],
            ["1,000,000", "the hundred thousands digit: 4", c(round_to(n, 1000000))],
        ]) +
        ex("Watch the 9s", "Round 4,965,300 to the nearest 100,000.",
           "The hundred thousands digit is 9 and the ten thousands digit is 6, so round up. 9 + 1 = 10 hundred "
           "thousands. Exchange them for 1 million: 4,900,000 + 100,000 = 5,000,000.", "5,000,000") +
        "<h2>Negative numbers and intervals across zero</h2>"
        "<p>Numbers below 0 are negative. We meet them in temperatures, below sea level and in lifts. "
        "To find the difference between a negative and a positive number, <b>jump to 0 first</b>, then add the two jumps.</p>"
        "<figure class='sn-fig'>" + neg_line_svg(-8, 6, list(range(-8, 7)), g=30, jumps=(-7, 5)) +
        "<figcaption>From " + c(-7) + " to 0 is 7. From 0 to 5 is 5. The difference is 7 + 5 = 12.</figcaption></figure>" +
        ex("Temperature", "The temperature rose from " + deg(-7) + " to 5 °C. By how many degrees did it rise?",
           "7 degrees up to 0 °C, then 5 more degrees: 7 + 5 = 12.", "12 degrees") +
        ex("Calculate", c(-6) + " − 5",
           "Start at " + c(-6) + " and count down 5. Going down from a negative number makes it more negative.", c(-11)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Missing a zero placeholder (four million, sixty thousand and five → 4,600,005)",
             "Write each group as three digits: 4 | 060 | 005 → 4,060,005"],
            ["Giving the digit, not its value (the 6 in 4,060,005 is 6)", "It is in the ten thousands place: 60,000"],
            ["Rounding the wrong place (3,462,718 to the nearest 100,000 → 3,463,000)",
             "Find the hundred thousands digit first: 3,500,000"],
            ["Keeping the digits after rounding (3,462,718 to the nearest 100,000 → 3,562,718)", "Change every digit after the place to 0"],
            ["Interval across zero as 7 − 5 = 2 (" + deg(-7) + " to 5 °C)", "Jump to 0 and add: 7 + 5 = 12"],
        ])
    )


FAQ = [
    {"q": "What place value do Year 6 children need to know?",
     "a": "Year 6 pupils read, write, order and compare numbers up to 10,000,000 and know the value of every digit. "
          "They round any whole number to a required degree of accuracy and use negative numbers in context, "
          "including finding intervals across zero."},
    {"q": "How do you write a number in the millions in words?",
     "a": "Split it into groups of three digits and read each group with its name. 4,060,005 is “four million, "
          "sixty thousand and five”. Write 0 in every empty place when you turn words back into digits."},
    {"q": "How do you find the difference between a negative and a positive number?",
     "a": "Count to 0 and then on from 0, and add the two parts. From −7 °C to 5 °C is 7 + 5 = 12 degrees, not 7 − 5."},
    {"q": "Is place value tested in the Year 6 SATs?",
     "a": "Yes. The KS2 reasoning papers often ask pupils to round, order large numbers or find a difference "
          "across zero. A scaled score of 100 or more means a pupil has met the expected standard."},
]


def mark_large(u, pattern):
    """Tag wide pictures (charts, number lines, thermometers) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(6601)
    P = People(rnd)
    used = set()
    pk = Picker(rnd)
    sets = [set_value(rnd, used), set_compare(rnd, used), set_round(rnd, pk), set_negative(rnd), set_words(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "place-value-and-rounding", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value, Rounding and Negative Numbers up to 10,000,000",
        "seo_title": "Year 6 Place Value and Rounding Worksheets: Numbers to 10 Million and Negative Numbers (Free)",
        "short_title": "Place value and rounding",
        "domain": "Number and place value",
        "standard_code": "Year 6: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read, write, order and compare numbers up to 10,000,000 and determine the value of each digit; round any whole number to a required degree of accuracy; use negative numbers in context, and calculate intervals across zero; solve number and practical problems that involve all of the above.",
        "meta_desc": "Free Year 6 maths worksheets for the National Curriculum: place value up to 10,000,000, numbers in words, comparing and ordering, rounding to any place, and negative numbers with intervals across zero. 100 SATs-style questions with an answer key.",
        "key_big": "Split big numbers into groups of three: millions, thousands, ones. The place decides what each digit is worth.",
        "key_sub": "Write 0 in every empty place (4,060,005). To round, look one place to the right: 5 or more rounds up. Across zero, jump to 0 and add: −7 to 5 is 7 + 5 = 12.",
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
