# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Place value to 10 000 (Australian Curriculum v9.0, AC9M3N01)
  python3 tools/gen_au_maths_y3_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Australian number style: 4-digit numbers have no separator (4536); 5 or more digits use a
no-break space between groups of three (10 000, 45 307). Never commas.
Wrong answers come from real mistakes: leaving out zero placeholders (four thousand and six -> 46 or 406),
writing each spoken part (4000 and 6 -> 40 006), giving the digit instead of its value,
comparing the first digit only when the numbers have different lengths, and misreading 10 000 as 1000.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
SIDE = "#a9d3b5"
TOP = "#e3f1e7"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand"]


# ------------------------------------------------------------ helpers
def c(n):
    """Australian style: 4536 stays 4536; 45307 -> 45 307 with a no-break space."""
    s = str(n)
    if n < 10000:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


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


def mcq_n(q, correct, cands, e, rnd, unit=""):
    """Whole-number choices. Wrong numbers that are 0 or less, or too big to be sensible, are dropped."""
    it = mcq(q, c(correct), [c(v) for v in cands if v is not None and 0 < v < 1000000 and v != correct], e, rnd)
    if unit:
        it["c"] = [x + unit for x in it["c"]]
    return it


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
    """Numbers a student writes when a zero goes missing, moves, or is added."""
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
    return [v for v in out if v != n and 10 <= v < 1000000]


def joined_digits(n):
    """Writing only the non-zero digits side by side (4000 + 6 -> 46)."""
    return int("".join(ch for ch in str(n) if ch != "0"))


def as_heard(n):
    """Writing each spoken part: four thousand and six -> 4000 then 6 -> 40006."""
    th, r = divmod(n, 1000)
    if th and r:
        return int(str(th * 1000) + str(r))
    return None


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


# ------------------------------------------------------------ number words (Australian: "and" after hundred)
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words99(n):
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


def words999(n):
    h, r = divmod(n, 100)
    if not h:
        return words99(r)
    return ONES[h] + " hundred" + (" and " + words99(r) if r else "")


def words(n):
    """4006 -> four thousand and six; 12305 -> twelve thousand, three hundred and five."""
    assert 0 < n < 1000000
    th, r = divmod(n, 1000)
    if not th:
        return words999(r)
    s = words999(th) + " thousand"
    if r >= 100:
        s += ", " + words999(r)
    elif r:
        s += " and " + words99(r)
    return s


assert words(4006) == "four thousand and six"
assert words(12305) == "twelve thousand, three hundred and five"
assert words(10000) == "ten thousand"
assert words(25050) == "twenty-five thousand and fifty"


# ------------------------------------------------------------ figures
U = 8                      # MAB: a mini = U, a long = 10U, a flat = 10U x 10U, a big cube = 10U with depth
D = 26                     # depth offset for the drawn thousand cube
G = 8                      # gap between pieces
GG = 22                    # gap between groups
MG = 8


def mab_svg(th, h, t, o, labels=False):
    """MAB (base-ten blocks): th thousand cubes, h flats, t longs, o minis. Sizes are 1 : 10 : 100 on the faces."""
    F = 10 * U
    groups = []

    def grid(x, y, w, hh, cols, rows):
        s = []
        for i in range(1, cols):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>"
                     % (x + i * U, y, x + i * U, y + hh, GREEN))
        for i in range(1, rows):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + i * U, x + w, y + i * U, GREEN))
        return s

    def cubes(x, y):
        s = []
        for k in range(th):
            cx = x + k * (F + D + G)
            cy = y + D
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

    def longs(x, y):
        s = []
        for k in range(t):
            lx = x + k * (U + 5)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (lx, y, U, F, FILL, GREEN))
            s += grid(lx, y, U, F, 1, 10)
        return s

    ccols = (o + 4) // 5

    def minis(x, y):
        s = []
        for k in range(o):
            mx = x + (k // 5) * (U + 6)
            my = y + (k % 5) * (U + 7)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (mx, my, U, U, CUBE, GREEN))
        return s

    if th:
        groups.append((th * (F + D) + (th - 1) * G, F + D, cubes, plural(th, 3)))
    if h:
        groups.append((fcols * F + (fcols - 1) * G, frows * F + (frows - 1) * G, flats, plural(h, 2)))
    if t:
        groups.append((t * U + (t - 1) * 5, F, longs, plural(t, 1)))
    if o:
        groups.append((ccols * U + (ccols - 1) * 6, 5 * U + 4 * 7, minis, plural(o, 0)))
    lab_w = lambda s: int(len(s) * 8.6) + 6
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * MG + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * MG + body_h + (26 if labels else 0)
    s = []
    x = MG
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, MG + body_h - gh)        # sit every group on the same base line
        if labels:
            s.append(text(x + w / 2, MG + body_h + 20, lab, 15, bold=True))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "MAB blocks")


CW, HEAD, ROW = 112, 34, 50


def chart_svg(n, hi=None, places=None):
    """Place value chart with 3, 4 or 5 columns. hi = place index to colour red."""
    k_n = places or max(ndig(n), 3)
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
        s.append(text(cx, y0 + 23, cap(PL[i]), 14, bold=True))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, bold=True, col=RED if hi == i else INK))
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
            s.append(text(X(v), Y + 30, c(v), 15, bold=True, col=GREEN))
        v += step
    ax = X(arrow)
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    if show:
        s.append(text(min(max(ax, 60), W - 60), Y - 44, show, 15, bold=True, col=RED))
    top = 18 if show else 0
    body = "".join(s)
    if top:
        body = "<g transform='translate(0 %d)'>%s</g>" % (top, body)
    return svg_wrap(W, Hh + top, body, "number line from %s to %s" % (c(lo), c(hi)))


# ============================================================ set 1: value of each digit
def value_cands(d, i):
    out = [d, d * 10 ** (i - 1) if i >= 1 else None, d * 10 ** (i + 1)]
    if i >= 2:
        out.append(d * 10 ** (i - 2))
    return [v for v in out if v and v != d * 10 ** i] + [d * 10 ** (i + 2)]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), c(v), d, c(v)))


def mab_e(th, h, t, o):
    n = 1000 * th + 100 * h + 10 * t + o
    s = ("A big cube is 1000, a flat is 100, a long is 10 and a mini is 1. "
         "%s, %s, %s and %s: %s." % (plural(th, 3), plural(h, 2), plural(t, 1), plural(o, 0), c(n)))
    empty = [PL[i] for i, d in ((2, h), (1, t), (0, o)) if d == 0]
    if empty:
        s += " There are no %s, so write 0 in that place." % " or ".join(empty)
    return s


def set_value(rnd):
    its = []
    # MAB (4)
    for th, h, t, o in [(2, 3, 4, 5), (1, 4, 0, 6), (3, 0, 5, 2), (2, 1, 6, 0)]:
        n = 1000 * th + 100 * h + 10 * t + o
        cands = []
        if "0" in str(n):
            cands.append(joined_digits(n))
        cands += zero_mistakes(n)
        cands += [th + h + t + o, n + 100, n + 10, n + 1000]
        its.append(mcq_n(fig(mab_svg(th, h, t, o)) + "What number do the MAB show?", n, cands,
                         mab_e(th, h, t, o), rnd))
    # value of the red digit in a chart (5)
    for n, i in [(4728, 3), (586, 1), (36154, 4), (52918, 3), (61473, 2)]:
        d = digit(n, i)
        its.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                         value_cands(d, i), value_e(d, i, True), rnd))
    # value of a digit, no chart (5)
    for n, i in [(3825, 2), (7409, 3), (24617, 4), (58371, 3), (90264, 1)]:
        d = digit(n, i)
        its.append(mcq_n("What is the value of the digit %d in %s?" % (d, c(n)), d * 10 ** i,
                         value_cands(d, i), value_e(d, i), rnd))
    # which digit is in a place (3)
    for n, i in [(47285, 3), (63914, 4), (28571, 2)]:
        d = digit(n, i)
        e = ("%s has %s." % (c(n), ", ".join(plural(digit(n, x), x) for x in range(4, -1, -1)))
             + " The %s digit is %d." % (PL[i], d))
        cands = [digit(n, x) for x in sorted(range(5), key=lambda x: (abs(x - i), x)) if x != i]
        its.append(mcq("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, cands, e, rnd))
    # which number has a digit in a place (3)
    for d, i, base in [(6, 2, [3, 8, 1]), (4, 3, [7, 2, 9]), (8, 4, [1, 5, 3, 2])]:
        nums = {}
        for pos in range(len(base) + 1)[::-1]:
            ds = base[:]
            ds.insert(len(base) - pos, d)
            nums[pos] = int("".join(map(str, ds)))
        assert digit(nums[i], i) == d
        alts = [nums[x] for x in nums if x != i][-3:]
        its.append(mcq("Which number has %s %d in the %s place?" % ("an" if d == 8 else "a", d, PL[i]), c(nums[i]),
                       [c(v) for v in alts],
                       "In %s the %d is in the %s place, so it is worth %s = %s."
                       % (c(nums[i]), d, PL[i], plural(d, i), c(d * 10 ** i)), rnd))
    assert len(its) == 20
    return {"title": "Value of each digit in 3-, 4- and 5-digit numbers", "items": its}


# ============================================================ set 2: numbers in words and numerals
def word_num_e(n):
    parts = [plural(digit(n, i), i) for i in range(ndig(n) - 1, -1, -1)]
    s = "%s is %s: %s." % (cap(words(n)), ", ".join(parts), c(n))
    if "0" in str(n):
        empty = [PL[i] for i in range(ndig(n) - 1, -1, -1) if digit(n, i) == 0]
        lst = empty[0] if len(empty) == 1 else ", ".join(empty[:-1]) + " and " + empty[-1]
        s += " Write 0 for the empty %s place%s." % (lst, "s" if len(empty) > 1 else "")
    return s


def set_words(rnd):
    its = []
    # words -> numerals (10)
    for n in [4006, 3020, 7408, 8011, 5090, 12305, 20040, 16007, 30500, 25050]:
        cands = [joined_digits(n), as_heard(n)] + zero_mistakes(n)
        its.append(mcq_n("Write “%s” in numerals." % words(n), n, cands, word_num_e(n), rnd))
    # numerals -> words (6)
    for n in [2604, 9017, 4500, 15080, 40300, 11011]:
        wrong = [v for v in zero_mistakes(n) if v >= 100]
        if n == 9017:
            wrong = [9070, 917, 90017]
        if n == 11011:
            wrong = [11110, 1111, 11101]
        e = "%s has %s. Say it: %s." % (c(n), ", ".join(plural(digit(n, i), i) for i in range(ndig(n) - 1, -1, -1)
                                                         if digit(n, i)), words(n))
        if n == 9017:
            e += " 17 is seventeen, not seventy."
        its.append(mcq("How do you write %s in words?" % c(n), words(n), [words(v) for v in wrong], e, rnd))
    # ten thousand (4)
    its.append(mcq_n("Which number is ten thousand?", 10000, [1000, 100000, 100],
                     "Ten thousand is 10 thousands. It has 5 digits: 1 and four zeros, written 10 000. "
                     "1000 is only one thousand.", rnd))
    its.append(mcq_n("How many thousands make 10 000?", 10, [100, 1000, 1],
                     "10 000 is 1 ten thousand, and 1 ten thousand = 10 thousands. "
                     "Count in thousands: 1000, 2000, … 9000, 10 000. That is 10 thousands.", rnd))
    its.append(mcq_n("Write “forty thousand” in numerals.", 40000, [4000, 400000, 400],
                     "Forty thousand is 4 ten thousands, 0 thousands, 0 hundreds, 0 tens and 0 ones: 40 000. "
                     "4000 is only four thousand.", rnd))
    its.append(mcq_n("Write “nineteen thousand” in numerals.", 19000, [1900, 9000, 190000],
                     "Nineteen thousand is 1 ten thousand and 9 thousands, then 0 hundreds, 0 tens and 0 ones: 19 000. "
                     "1900 is one thousand, nine hundred.", rnd))
    order = its[:5] + its[10:13] + its[16:18] + its[5:10] + its[13:16] + its[18:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Read and write numbers in words and numerals", "items": order}


# ============================================================ set 3: partition
def set_partition(rnd):
    its = []
    # expanded -> number (5)
    for n in [6243, 5063, 9708, 24007, 81450]:
        cands = [joined_digits(n)] + zero_mistakes(n) + [int(str(n)[::-1])]
        if "0" not in str(n):
            cands = [n - n % 100 + (n % 10) * 10 + n // 10 % 10, n - n % 1000 + (n // 10 % 10) * 100 + (n // 100 % 10) * 10 + n % 10, int(str(n)[::-1])]
        e = "Put each digit in its place and write 0 in any empty place: %s = %s." % (expanded(n), c(n))
        if "0" not in str(n):
            e = "%s = %s. Each part gives one digit." % (expanded(n), c(n))
        its.append(mcq_n("What number is <b>%s</b>?" % expanded(n), n, cands, e, rnd))
    # number -> standard partition (4)
    for n in [3462, 4085, 30619, 52070]:
        k = ndig(n)
        if "0" not in str(n):
            low = " + ".join(c(digit(n, i) * 10 ** max(i - 1, 0)) for i in range(k - 1, -1, -1))
            dig = " + ".join(c(digit(n, i) * (10 ** i if i >= 2 else 1)) for i in range(k - 1, -1, -1))
            wrong = [dig, low, " + ".join(str(digit(n, i)) for i in range(k - 1, -1, -1))]
        else:
            wrong = [expanded(v) for v in zero_mistakes(n) if v >= 100]
        e = ("Write the value of each digit that is not 0: %s. A zero adds nothing, so it does not get its own part."
             % expanded(n)) if "0" in str(n) else "Write the value of each digit: %s." % expanded(n)
        its.append(mcq("Which shows %s partitioned into place values?" % c(n), expanded(n), wrong, e, rnd))
    # missing part (3)
    for n, i in [(7354, 2), (46028, 1), (32901, 4)]:
        d = digit(n, i)
        parts = ["☐" if x == i else c(digit(n, x) * 10 ** x) for x in range(ndig(n) - 1, -1, -1) if digit(n, x) or x == i]
        e = "%s has %d in the %s place. %s = %s, so the missing part is %s." % (
            c(n), d, PL[i], plural(d, i), c(d * 10 ** i), c(d * 10 ** i))
        its.append(mcq_n("%s = %s. What number goes in the box?" % (" + ".join(parts), c(n)), d * 10 ** i,
                         value_cands(d, i), e, rnd))
    # how many hundreds / tens / thousands altogether (4)
    for n, i, ans, wrong in [(3462, 2, 34, [4, 3, 346]), (4570, 1, 457, [7, 45, 57]),
                             (26300, 3, 26, [6, 2, 263]), (12800, 2, 128, [8, 12, 1280])]:
        assert n // 10 ** i == ans
        rest = n - ans * 10 ** i
        e = ("Cover the digits to the right of the %s place: %s → %s. So %s has %d %s altogether: "
             "%d %s = %s%s. The %s digit is only %d."
             % (PL[i], c(n), ans, c(n), ans, PL[i], ans, PL[i], c(ans * 10 ** i),
                (", with %d left over" % rest) if rest else "", PL[i], digit(n, i)))
        its.append(mcq_n("How many %s are there in %s altogether?" % (PL[i], c(n)), ans, wrong, e, rnd))
    # non-standard partitions (4)
    its.append(mcq_n("3462 = 34 hundreds and ☐ ones. What number goes in the box?", 62, [2, 6, 462],
                     "34 hundreds = 3400. 3462 − 3400 = 62. So 3462 = 34 hundreds and 62 ones.", rnd))
    its.append(mcq_n("5306 = 4000 + ☐ + 6. What number goes in the box?", 1300, [300, 1000, 130],
                     "5306 is 5000 + 300 + 6. Here only 4000 is used, so 1000 moves to the hundreds part: "
                     "1000 + 300 = 1300. Check: 4000 + 1300 + 6 = 5306.", rnd))
    its.append(mcq("Which is another way to make 2750?", "27 hundreds and 5 tens",
                   ["27 hundreds and 50 tens", "2 hundreds and 75 tens", "275 hundreds"],
                   "27 hundreds = 2700 and 5 tens = 50. 2700 + 50 = 2750. "
                   "(50 tens is 500, and 275 hundreds is 27 500.)", rnd))
    its.append(mcq("Which is <b>not</b> equal to 4800?", "4 thousands and 8 tens",
                   ["48 hundreds", "4 thousands and 8 hundreds", "480 tens"],
                   "4 thousands and 8 tens = 4000 + 80 = 4080, not 4800. "
                   "48 hundreds = 4800, 4000 + 800 = 4800 and 480 tens = 4800.", rnd))
    assert len(its) == 20
    for v, w in [(2700 + 50, 2750), (4000 + 80, 4080), (4800, 48 * 100), (4800, 480 * 10)]:
        assert v == w
    return {"title": "Partition numbers in standard and non-standard ways", "items": its}


# ============================================================ set 4: compare and order
def first_diff(a, b):
    for i in range(ndig(a) - 1, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def compare_expl(big, small):
    if ndig(big) != ndig(small):
        return "%s has %d digits and %s has only %d, so %s is greater." % (c(big), ndig(big), c(small), ndig(small), c(big))
    i = first_diff(big, small)
    top = ndig(big) - 1
    same = "The digits are the same until the %s place" % PL[i] if i < top else "Start with the %s" % PL[top]
    return ("Compare from the left. %s: %s is more than %s. So %s &gt; %s."
            % (same, plural(digit(big, i), i), plural(digit(small, i), i), c(big), c(small)))


def set_compare(rnd):
    its = []
    # which is true (5)
    for x, y in [(4352, 4325), (9870, 10200), (23504, 23540), (6089, 6098), (12001, 9999)]:
        lt = "&lt;" if x < y else "&gt;"
        gt = "&gt;" if x < y else "&lt;"
        right = "%s %s %s" % (c(x), lt, c(y))
        wrong = ["%s %s %s" % (c(x), gt, c(y)), "%s = %s" % (c(x), c(y)), "%s %s %s" % (c(y), lt, c(x))]
        e = compare_expl(max(x, y), min(x, y))
        if ndig(x) != ndig(y):
            e += " Do not just look at the first digit: count the digits first."
        its.append(mcq("Which is true?", right, wrong, e, rnd))
    # greatest (3) / smallest (2)
    for want_max, nums in [(True, [7065, 7605, 7560, 7506]), (True, [9899, 10001, 10010, 9989]),
                           (True, [35210, 35120, 32510, 35201]), (False, [4087, 4807, 4078, 4708]),
                           (False, [10300, 9870, 10030, 13000])]:
        o = sorted(nums)
        ans = o[-1] if want_max else o[0]
        nxt = o[-2] if want_max else o[1]
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % c(ans)
        else:
            e = compare_expl(nxt, ans) + " %s is the smallest." % c(ans)
        if 9870 in nums:
            e = "9870 is the only number with 4 digits, so it is the smallest, even though 9 is a big digit."
        if 9899 in nums:
            e = ("9899 and 9989 have only 4 digits, so they are smaller. " + compare_expl(ans, nxt)
                 + " %s is the greatest." % c(ans))
        its.append(mcq("Which number is the %s?" % ("greatest" if want_max else "smallest"), c(ans),
                       [c(v) for v in nums if v != ans], e, rnd))
    # order (4)
    fmt = lambda l: ", ".join(c(v) for v in l)
    for nums, up in [([5260, 5026, 5602], True), ([12450, 9980, 12405], True),
                     ([30060, 30600, 3600], True), ([8150, 8510, 8015], False)]:
        o = sorted(nums) if up else sorted(nums, reverse=True)
        perms = [[o[0], o[2], o[1]], [o[1], o[0], o[2]], o[::-1]]
        a = sorted(nums)
        steps = []
        for p, q in zip(a, a[1:]):
            if ndig(p) != ndig(q):
                steps.append("%s &lt; %s (fewer digits)" % (c(p), c(q)))
            else:
                i = first_diff(q, p)
                steps.append("%s &lt; %s (%s: %d &lt; %d)" % (c(p), c(q), PL[i], digit(p, i), digit(q, i)))
        e = "Compare from the left. %s. So the order is %s." % (". ".join(steps), fmt(o))
        its.append(mcq("Put %s in order from %s." % (fmt(nums), "smallest to largest" if up else "largest to smallest"),
                       fmt(o), [fmt(p) for p in perms], e, rnd))
    # number lines (4)
    its.append(mcq_n(fig(number_line_svg(0, 10000, 1000, [0, 5000, 10000], 7000)) +
                     "What number does the arrow point to?", 7000, [700, 6000, 8000],
                     "From 0 to 10 000 there are 10 jumps, so each mark is 1000. The arrow is 2 marks after 5000: "
                     "5000, 6000, 7000.", rnd))
    its.append(mcq_n(fig(number_line_svg(20000, 30000, 1000, [20000, 25000, 30000], 26000)) +
                     "What number does the arrow point to?", 26000, [2600, 27000, 6000],
                     "Each mark is 1000. The arrow is 1 mark after 25 000: 25 000 + 1000 = 26 000.", rnd))
    its.append(mcq_n(fig(number_line_svg(4000, 5000, 100, [4000, 4500, 5000], 4300)) +
                     "What number does the arrow point to?", 4300, [4030, 4700, 4400],
                     "From 4000 to 5000 there are 10 jumps, so each mark is 100, not 10. "
                     "The arrow is 3 marks after 4000: 4000 + 300 = 4300.", rnd))
    its.append(mcq_n(fig(number_line_svg(0, 10000, 1000, [0, 5000, 10000], 3500)) +
                     "Estimate the number the arrow points to.", 3500, [4500, 350, 6500],
                     "Each mark is 1000. The arrow is halfway between 3000 and 4000, so it shows about 3500.", rnd))
    # between (2)
    its.append(mcq_n("Which number is between 6400 and 6500?", 6450, [6540, 6045, 6390],
                     "Numbers between 6400 and 6500 have 6 thousands and 4 hundreds. 6450 has 6 thousands, "
                     "4 hundreds and 5 tens. 6045 has 0 hundreds, and 6540 has 5 hundreds.", rnd))
    its.append(mcq_n("Which number is between 19 000 and 20 000?", 19500, [1950, 20100, 18999],
                     "Numbers between 19 000 and 20 000 start with 19 thousand. 19 500 is 19 thousands and 5 hundreds. "
                     "1950 has only 4 digits, so it is much smaller.", rnd))
    assert len(its) == 20
    order = its[:5] + its[14:17] + its[5:10] + its[18:] + its[10:14] + its[17:18]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers", "items": order}


# ============================================================ set 5: word problems
def set_problems(rnd, P):
    its = []
    its.append(mcq_n("At the footy, %s people watched the game. What is the value of the digit 5 in %s?"
                     % (c(45307), c(45307)), 5000, [5, 500, 50000],
                     "The 5 is in the thousands place, so it is worth 5 thousands = 5000.", rnd))
    its.append(mcq("The school library has 4060 books. Which shows 4060 partitioned?", "4000 + 60",
                   ["4000 + 600", "400 + 60", "4000 + 6"],
                   "4060 has 4 thousands, 0 hundreds, 6 tens and 0 ones: 4000 + 60.", rnd))
    its.append(mcq("Mum’s car has travelled %s km. Which digit is in the thousands place?" % c(23406), "3",
                   ["2", "4", "6"],
                   "%s has 2 ten thousands, 3 thousands, 4 hundreds, 0 tens and 6 ones. The thousands digit is 3."
                   % c(23406), rnd))
    walkers = [(P.next(), v) for v in [8350, 8503, 8035, 8530]]
    best = max(walkers, key=lambda w: w[1])
    its.append(mcq("Four friends counted their steps on a school excursion. %s. Who walked the most steps?"
                   % "; ".join("%s: %s" % (p[0], c(v)) for p, v in walkers), best[0][0],
                   [p[0] for p, v in walkers if v != best[1]],
                   "All four numbers have 8 thousands. Compare the hundreds: 8503 and 8530 have 5 hundreds. "
                   "Then the tens: 3 tens &gt; 0 tens, so 8530 is the greatest. %s walked the most." % best[0][0], rnd))
    crowds = [32410, 32140, 31999, 32401]
    its.append(mcq("The crowds at four footy games were %s. Which crowd was the smallest?"
                   % ", ".join(c(v) for v in crowds), c(31999), [c(v) for v in crowds if v != 31999],
                   "All four have 3 ten thousands. Compare the thousands: %s has only 1 thousand, the others have 2. "
                   "So %s is the smallest." % (c(31999), c(31999)), rnd))
    its.append(mcq_n("Raffle tickets come in books of 100. How many books make 3400 tickets?", 34, [4, 3, 340],
                     "3400 = 34 hundreds, because 34 × 100 = 3400. So there are 34 books.", rnd))
    its.append(mcq_n("Pencils come in boxes of 10. The school buys 2350 pencils. How many boxes is that?", 235,
                     [23, 35, 350],
                     "2350 = 235 tens, because 235 × 10 = 2350. So there are 235 boxes.", rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s writes “ten thousand, four hundred” in numerals. What should %s write?" % (name, she), 10400,
                     [1400, 100400, 10004],
                     "Ten thousand, four hundred is 1 ten thousand, 0 thousands, 4 hundreds, 0 tens and 0 ones: %s."
                     % c(10400), rnd))
    its.append(mcq_n("A sign says a country town has a population of “seventeen thousand and forty”. "
                     "What is this in numerals?", 17040, [17400, 1740, 170040],
                     "1 ten thousand, 7 thousands, 0 hundreds, 4 tens and 0 ones: %s." % c(17040), rnd))
    name, he, his = P.next()
    its.append(mcq("A truck driver drove %s km in March. How do you write %s in words?" % (c(12450), c(12450)),
                   words(12450), [words(1245), words(12045), words(120450)],
                   "%s is 12 thousands, 4 hundreds and 5 tens: %s." % (c(12450), words(12450)), rnd))
    name, she, her = P.next()
    its.append(mcq_n(fig(number_line_svg(0, 10000, 1000, [0, 5000, 10000], 6500)) +
                     "%s’s step goal is %s steps a day. The arrow shows how many steps %s has walked so far. "
                     "About how many steps is that?" % (name, c(10000), she), 6500, [7500, 5500, 650],
                     "Each mark is 1000 steps. The arrow is halfway between 6000 and 7000, so it shows about 6500 steps.",
                     rnd))
    its.append(mcq_n("Use each of the digits 4, 0, 7, 2 and 9 once to make the greatest 5-digit number.", 97420,
                     [97402, 97240, 9742],
                     "Put the biggest digit in the ten thousands place, then the next biggest, and so on: "
                     "9, 7, 4, 2, 0. The greatest number is %s." % c(97420), rnd))
    its.append(mcq_n("Use each of the digits 3, 0, 8 and 5 once to make the smallest 4-digit number.", 3058,
                     [358, 3085, 3508],
                     "A 4-digit number cannot start with 0, so put the smallest non-zero digit first: 3. "
                     "Then 0, 5, 8. The smallest number is 3058.", rnd))
    its.append(mcq_n("There are %s people at the cricket. Then 1000 more people arrive. How many people are there now?"
                     % c(10000), 11000, [20000, 10100, 10001],
                     "1000 more changes only the thousands digit: 0 thousands → 1 thousand. %s + 1000 = %s."
                     % (c(10000), c(11000)), rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s’s number has 4 ten thousands, 2 thousands, 0 hundreds, 6 tens and 0 ones. What is %s number?"
                     % (name, her), 42060, [4206, 42600, 42006],
                     "Write the digits in order: 4, 2, 0, 6, 0 → %s. The zeros keep the other digits in their places."
                     % c(42060), rnd))
    name, he, his = P.next()
    its.append(mcq_n("A farm has 2307 sheep. %s says the 3 is worth 3. What is the 3 really worth?" % name, 300,
                     [3, 30, 3000],
                     "In 2307 the 3 is in the hundreds place. Its value is 3 hundreds = 300.", rnd))
    its.append(mcq_n("Footy tickets are printed in packs of 1000. How many packs are needed for %s tickets?" % c(25000),
                     25, [250, 2500, 2],
                     "%s = 25 thousands, because 25 × 1000 = %s. So 25 packs are needed." % (c(25000), c(25000)), rnd))
    towns = [14205, 14520, 14052]
    o = sorted(towns, reverse=True)
    its.append(mcq("Three country towns have populations of %s. Which list shows them from largest to smallest?"
                   % fmt_list(towns), fmt_list(o),
                   [fmt_list([o[1], o[0], o[2]]), fmt_list([o[0], o[2], o[1]]), fmt_list(o[::-1])],
                   "All have 14 thousands. Compare the hundreds: 5 hundreds &gt; 2 hundreds &gt; 0 hundreds. "
                   "Order: %s." % fmt_list(o), rnd))
    its.append(mcq("The school canteen sold 1098 icy poles last term and 1089 this term. Which is true?",
                   "1098 &gt; 1089", ["1098 &lt; 1089", "1098 = 1089", "1089 &gt; 1098"],
                   "Both have 1 thousand and 0 hundreds. Compare the tens: 9 tens &gt; 8 tens. So 1098 &gt; 1089.", rnd))
    its.append(mcq_n("A class collects bottle tops. They have 3 bags of 1000, 14 bags of 100 and 5 single bottle tops. "
                     "How many bottle tops is that?", 4405, [31405, 3145, 3405],
                     "14 hundreds = 1 thousand and 4 hundreds. So there are 4 thousands, 4 hundreds, 0 tens and 5 ones: "
                     "3000 + 1400 + 5 = 4405.", rnd))
    assert 3000 + 1400 + 5 == 4405 and 1098 > 1089 and 34 * 100 == 3400 and 235 * 10 == 2350
    assert len(its) == 20
    return {"title": "Place value word problems", "items": its}


def fmt_list(l):
    return ", ".join(c(v) for v in l)


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
        "<h2>Each place is worth 10 times more</h2>"
        "<p>Every digit sits in a <b>place</b>: ones, tens, hundreds, thousands or ten thousands. "
        "The place tells you what the digit is worth. 10 ones make 1 ten, 10 tens make 1 hundred, "
        "10 hundreds make 1 thousand and <b>10 thousands make 10 000</b>.</p>"
        "<figure class='sn-fig'>" + mab_svg(1, 4, 0, 6, labels=True) +
        "<figcaption>MAB for 1406. A big cube is 1000, a flat is 100, a long is 10 and a mini is 1. "
        "There are no longs, so the tens digit is 0.</figcaption></figure>"
        "<figure class='sn-fig'>" + chart_svg(45307, hi=3) +
        "<figcaption>In " + c(45307) + " the 5 is in the thousands place. Its value is 5 thousands, or 5000."
        "</figcaption></figure>"
        "<h2>Reading and writing numbers</h2>"
        "<p>Say the thousands first, then the rest. Write 4-digit numbers with no space (4536). "
        "Put a small space in numbers with 5 or more digits (" + c(10000) + ", " + c(45307) + ").</p>" +
        table(["Numeral", "Words"], [
            ["4006", "four thousand and six"],
            ["3020", "three thousand and twenty"],
            [c(10000), "ten thousand"],
            [c(12305), "twelve thousand, three hundred and five"],
        ]) +
        ex("Write in numerals", "Write “four thousand and six” in numerals.",
           "4 thousands, 0 hundreds, 0 tens, 6 ones. Write 4, 0, 0, 6.", "4006 (not 46, 406 or " + c(40006) + ")") +
        "<h2>Partition in different ways</h2>"
        "<p>The <b>standard</b> way uses the value of each digit. A <b>non-standard</b> way regroups the places.</p>" +
        ex("Partition", "Partition 3462 in two ways.",
           "Standard: 3000 + 400 + 60 + 2. Non-standard: 34 hundreds = 3400, so 3462 = 34 hundreds and 62 ones.",
           "3000 + 400 + 60 + 2 = 34 hundreds and 62 ones") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 5-digit number is greater than any 4-digit number. "
        "If both have the same number of digits, compare place by place from the left.</p>" +
        ex("Compare", "23 504 ☐ 23 540".replace(" ", NB),
           "Ten thousands: 2 = 2. Thousands: 3 = 3. Hundreds: 5 = 5. Tens: 0 &lt; 4.",
           c(23504) + " &lt; " + c(23540)) +
        "<p>&lt; means “is less than”. &gt; means “is greater than”. The open side faces the bigger number.</p>"
        "<figure class='sn-fig'>" + number_line_svg(0, 10000, 1000, [0, 5000, 10000], 3500, show="about 3500") +
        "<figcaption>Each mark is 1000. The arrow is halfway between 3000 and 4000, so it shows about 3500."
        "</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Leaving out zeros (four thousand and six = 46 or 406)", "Write 0 for each empty place: 4006"],
            ["Writing each part you hear (four thousand and six = " + c(40006) + ")", "A thousands number has 4 digits: 4006"],
            ["Giving the digit, not its value (the 5 in " + c(45307) + " is 5)", "The 5 is in the thousands place: 5000"],
            ["Comparing the first digits only (9870 &gt; " + c(10200) + ")", "Count the digits first: " + c(10200) + " &gt; 9870"],
            ["Reading " + c(10000) + " as 1000", c(10000) + " has 5 digits: ten thousand"],
        ])
    )


FAQ = [
    {"q": "What place value does a Year 3 student learn in Australia?",
     "a": "The Australian Curriculum (AC9M3N01) asks Year 3 students to recognise, represent and order numbers beyond 10 000. They name the value of each digit, read and write numbers in words and numerals, partition numbers in different ways and compare and order them."},
    {"q": "What are MAB blocks?",
     "a": "MAB (multi-base arithmetic blocks) are the base-ten blocks used in Australian classrooms: a mini is 1, a long is 10, a flat is 100 and a big cube is 1000. Children build numbers with them to see what each digit is worth."},
    {"q": "How do you write 10 000 in Australia?",
     "a": "Numbers with 5 or more digits are written with a small space between groups of three digits, such as 10 000 and 45 307. Four-digit numbers like 4536 are written with no space, and commas are not used."},
    {"q": "Is place value tested in NAPLAN?",
     "a": "Yes. The Year 3 NAPLAN numeracy test often asks students to read, write, partition and order numbers, so regular practice with place value helps them answer these questions quickly and accurately."},
]


GROUP = re.compile(r"(?<![\d.])(\d{1,3}) (\d{3})(?!\d)")


def nb(t):
    """Use a no-break space inside numbers like 10 000 that were typed with an ordinary space (not inside SVG)."""
    parts = re.split(r"(<svg.*?</svg>)", t, flags=re.S)
    return "".join(x if x.startswith("<svg") else GROUP.sub(lambda m: m.group(1) + NB + m.group(2), x) for x in parts)


def nb_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "standard_text", "body_html"):
        u[k] = nb(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nb(f["q"]), nb(f["a"])
    for st in u["sets"]:
        for it in st["items"]:
            it["q"], it["e"] = nb(it["q"]), nb(it["e"])
            it["c"] = [nb(x) for x in it["c"]]


def mark_large(u, pattern):
    """Tag wide pictures (MAB, charts, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(3801)
    P = People(rnd)
    sets = [set_value(rnd), set_words(rnd), set_partition(rnd), set_compare(rnd), set_problems(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "place-value-to-10000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value to 10 000 and Beyond: Read, Write, Partition and Order Numbers",
        "seo_title": "Year 3 Place Value Worksheets: Numbers to 10 000 and Beyond, Free with Answer Key",
        "short_title": "Place value to 10 000",
        "domain": "Number",
        "standard_code": "AC9M3N01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise, represent and order natural numbers using naming and writing conventions for numerals beyond 10 000",
        "meta_desc": "Free Year 3 place value maths worksheets for the Australian Curriculum: the value of each digit with MAB and place value charts, numbers beyond 10 000 in words and numerals, standard and non-standard partitioning, and comparing and ordering. 100 NAPLAN-style questions with an answer key.",
        "key_big": "The place of a digit decides its value. Each place is worth 10 times the place to its right.",
        "key_sub": "The 5 in 45 307 is worth 5000. Write 0 for an empty place: four thousand and six is 4006. Count the digits before you compare: 10 200 is greater than 9870.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    u["key_sub"] = u["key_sub"].replace("45 307", c(45307)).replace("10 200", c(10200))
    u["title"] = u["title"].replace("10 000", c(10000))
    u["seo_title"] = u["seo_title"].replace("10 000", c(10000))
    u["short_title"] = u["short_title"].replace("10 000", c(10000))
    u["standard_text"] = u["standard_text"].replace("10 000", c(10000))
    for f in u["faq"]:
        for k in ("q", "a"):
            for n in (10000, 45307):
                f[k] = f[k].replace(c(n).replace(NB, " "), c(n))
    u["meta_desc"] = u["meta_desc"].replace("10 000", c(10000))
    nb_spaces(u)
    return mark_large(u, "(MAB blocks|place value chart|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
