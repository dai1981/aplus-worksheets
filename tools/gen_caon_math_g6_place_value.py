# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 6 Math: Large Numbers and Decimals
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 6, Number, B1)
  python3 tools/gen_ca_math_g6_place_value.py
Place value to one million, comparing and ordering large numbers, decimals to thousandths,
comparing and ordering decimals, and rounding decimals and large numbers in real Canadian contexts.
Numbers: 4-digit numbers have no separator; 5 or more digits use a no-break space (245 300). Never commas.
Every answer is checked with decimal.Decimal / fractions.Fraction (never float).
Wrong answers come from real mistakes: giving the digit instead of its value, missing zero placeholders,
comparing first digits only, "longer decimal is bigger" (0.45 > 0.5), rounding the wrong place or the wrong
way, cutting off instead of rounding, writing "10" in the place of a 9, and rounding twice.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]


# ------------------------------------------------------------ helpers
def n(x):
    """Ontario/SI style: 4536, 10 000, 245 300 (no-break spaces, never commas)."""
    s = str(x)
    if len(s) <= 4:
        return s
    g = []
    while s:
        g.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(g)


def D(s):
    return Dm(s)


def rd(x, places):
    """Round a decimal string half up to `places` decimal places; returns text with exactly that many places."""
    q = Dm(1).scaleb(-places)
    return str(Dm(x).quantize(q, rounding=ROUND_HALF_UP))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)( .+)?$")


def val(c):
    """Value of a choice with its unit; None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    c = re.sub(r"(?<=\d)" + NB + r"(?=\d)", "", c)
    m = NUM.match(c)
    if not m:
        return None
    return (F(m.group(2)), "$" if m.group(1) else (m.group(3) or "").strip())


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong. No two choices may be equal in value."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    vs = [val(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def pick3(correct, cands):
    """First 3 different wrong values from a list of mistakes (ints)."""
    out = []
    for v in cands:
        if v is None or v <= 0 or v == correct or v in out:
            continue
        out.append(v)
        if len(out) == 3:
            break
    assert len(out) == 3, (correct, cands)
    return out


def mcq_n(q, correct, cands, e, unit=""):
    return mcq(q, n(correct) + unit, [n(v) + unit for v in pick3(correct, cands)], e)


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


def digit(x, i):
    return (x // 10 ** i) % 10


def ndig(x):
    return len(str(x))


def cap(s):
    return s[0].upper() + s[1:]


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


# ------------------------------------------------------------ numbers in words (no "and" in whole numbers;
# "and" is said only for the decimal point)
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def w100(x):
    if x < 20:
        return ONES[x]
    return TENS[x // 10] + ("-" + ONES[x % 10] if x % 10 else "")


def w1000(x):
    h, r = divmod(x, 100)
    out = []
    if h:
        out.append(ONES[h] + " hundred")
    if r:
        out.append(w100(r))
    return " ".join(out)


def words(x):
    assert 0 < x <= 1000000
    if x == 1000000:
        return "one million"
    t, o = divmod(x, 1000)
    parts = []
    if t:
        parts.append(w1000(t) + " thousand")
    if o:
        parts.append(w1000(o))
    return " ".join(parts)


assert words(406005) == "four hundred six thousand five"
assert words(230708) == "two hundred thirty thousand seven hundred eight"

DEN = {1: "tenths", 2: "hundredths", 3: "thousandths"}


def dec_words(s):
    w, _, f = s.partition(".")
    k = int(f)
    tail = w1000(k) + " " + (DEN[len(f)] if k != 1 else DEN[len(f)][:-1])
    return (w1000(int(w)) + " and " + tail) if int(w) else tail


assert dec_words("4.026") == "four and twenty-six thousandths"
assert dec_words("0.305") == "three hundred five thousandths"


def zero_mistakes(x):
    """Numbers a student writes when a zero goes missing, moves, or is added."""
    s = str(x)
    out = []
    for i, ch in enumerate(s):
        if ch == "0":
            for j in (i - 1, i + 1):
                if 0 < j < len(s) and s[j] != "0":
                    l = list(s)
                    l[i], l[j] = l[j], l[i]
                    out.append(int("".join(l)))
            out.append(int(s[:i] + s[i + 1:]))
    for i in range(1, len(s)):
        if s[i] == "0":
            out.append(int(s[:i] + "0" + s[i:]))
    return [v for v in out if v != x and 1000 <= v < 10000000]


def joined_digits(x):
    return int("".join(ch for ch in str(x) if ch != "0"))


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 64, 28, 28, 48
SUB = ["H", "T", "O", "H", "T", "O"]


def chart_svg(x, hi=None):
    """Thousands (H T O) | Ones (H T O) chart with a number up to 999 999. hi = place index drawn in red."""
    x0 = y0 = 6
    W, H = 2 * x0 + 6 * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, 6 * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 6 * CW, H1 + H2, FILL)]
    for k, name in [(0, "Thousands"), (3, "Ones")]:
        s.append(text(x0 + k * CW + 1.5 * CW, y0 + 19, name, 14, bold=True))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0 + 3 * CW, y0, x0 + 3 * CW, y0 + H1 + H2 + ROW, GREEN))
    nd = ndig(x)
    for k in range(6):
        i = 5 - k
        xx = x0 + k * CW
        if k not in (0, 3):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (xx, y0 + H1, xx, y0 + H1 + H2 + ROW, GREEN))
        s.append(text(xx + CW / 2, y0 + H1 + 19, SUB[k], 14, bold=True))
        if i < nd:
            s.append(text(xx + CW / 2, y0 + H1 + H2 + 34, str(digit(x, i)), 28, bold=True,
                          col=RED if hi == i else INK))
    for y in (y0 + H1, y0 + H1 + H2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + 6 * CW, y, GREEN, "1.2" if y == y0 + H1 else "2"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, 6 * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % n(x))


def big_line_svg(lo, hi, step, labels, arrow=None):
    """Number line lo..hi for whole numbers, a tick every step, numbers at `labels`, red arrow at `arrow`."""
    L, R = 58, 422
    W = 480
    Y = 58 if arrow is not None else 30
    H = Y + 42
    span = hi - lo

    def X(v):
        return L + (v - lo) * (R - L) / float(span)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, n(v), 15, bold=True, col=GREEN))
        v += step
    if arrow is not None:
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (n(lo), n(hi)))


PV_ALL = [(1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths"), (-3, "Thousandths")]


def dchart_svg(s_, hi=None):
    """Decimal place value chart: (Tens) | Ones | . | Tenths | Hundredths | Thousandths. hi = place drawn in red."""
    w, _, f = s_.partition(".")
    cols = PV_ALL if len(w) > 1 else PV_ALL[1:]
    DW, PW, HEAD, DROW = 108, 16, 30, 44
    x0, y0 = 6, 6
    W = 2 * x0 + len(cols) * DW + PW
    H = 2 * y0 + HEAD + DROW
    xs, x = {}, x0
    for p, _ in cols:
        xs[p] = x
        x += DW + (PW if p == 0 else 0)
    px = xs[0] + DW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, W - 2 * x0, HEAD + DROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, W - 2 * x0, HEAD, FILL)]
    for p, name in cols:
        if p != cols[0][0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + DROW, GREEN))
        o.append(text(xs[p] + DW / 2.0, y0 + 20, name, 14, bold=True))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + DROW, GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    digits = {}
    for j, ch in enumerate(w):
        digits[len(w) - 1 - j] = ch
    for j, ch in enumerate(f):
        digits[-(j + 1)] = ch
    for p, ch in digits.items():
        o.append(text(xs[p] + DW / 2.0, y0 + HEAD + 32, ch, 28, bold=True, col=RED if hi == p else INK))
    o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, y0 + HEAD + 31, INK))
    return svg_wrap(W, H, "".join(o), "place value chart showing %s" % s_)


def dec(v):
    """Thousandths integer -> decimal text without trailing zeros."""
    d = Dm(v) / Dm(1000)
    return format(d.normalize(), "f")


def dline_svg(a, b, spaces, labels, dot=None, dot_label=False, W=420):
    """Decimal number line from a to b (in thousandths) with `spaces` equal spaces; red dot at `dot`."""
    L, R = 30, W - 30
    Y = 44 if dot_label else 30
    assert (b - a) % spaces == 0
    step = (b - a) // spaces

    def X(v):
        return L + (R - L) * (v - a) / float(b - a)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, INK)]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), INK, "2.5" if big else "1.6"))
    for v in labels:
        assert (v - a) % step == 0
        s.append(text(X(v), Y + 36, dec(v), 17, bold=True, col=GREEN))
    if dot is not None:
        assert a <= dot <= b
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(dot), Y, RED))
        if dot_label:
            s.append(text(X(dot), Y - 18, dec(dot), 17, bold=True, col=RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from %s to %s split into %d equal spaces"
                    % (dec(a), dec(b), spaces))


# ============================================================ set 1: place value to one million
def value_cands(d, i):
    return [d * 10 ** (i + 1) if i + 1 <= 5 else None, d * 10 ** (i - 1) if i >= 1 else None, d,
            d * 10 ** (i - 2) if i >= 2 else None, d * 10 ** (i + 2) if i + 2 <= 5 else None]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), n(v), d, n(v)))


def distinct6(rnd, used):
    while True:
        ds = rnd.sample(range(10), 6)
        if ds[0] == 0:
            continue
        x = int("".join(map(str, ds)))
        if x not in used:
            used.add(x)
            return x


def set_whole(rnd, used):
    A, B, C = [], [], []
    for i in [3, 4, 2, 5, 1]:                                   # chart, red digit (5)
        while True:
            x = distinct6(rnd, used)
            if digit(x, i):
                break
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    for i in [4, 5, 3, 2]:                                      # value, no chart (4)
        while True:
            x = distinct6(rnd, used)
            if digit(x, i):
                break
        d = digit(x, i)
        B.append(mcq_n("What is the value of the digit %d in %s?" % (d, n(x)), d * 10 ** i,
                       value_cands(d, i), value_e(d, i)))
    for i in [4, 3]:                                            # which digit is in a place (2)
        while True:
            x = distinct6(rnd, used)
            if digit(x, i):
                break
        d = digit(x, i)
        cands = [str(digit(x, k)) for k in sorted(range(6), key=lambda k: (abs(k - i), k)) if k != i][:3]
        e = ("Read the places from the right: ones, tens, hundreds, thousands, ten thousands, hundred thousands. "
             "In %s the %s digit is %d, worth %s." % (n(x), PL[i], d, n(d * 10 ** i)))
        C.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    Dw = []
    for x in [406005, 230708, 900430]:                         # words -> numeral (3)
        used.add(x)
        t, o = divmod(x, 1000)
        e = ("Write each group as three digits. %s thousand → %03d. Then %s → %03d. "
             "Fill every empty place with 0: %s." % (cap(w1000(t)), t, w1000(o), o, n(x)))
        Dw.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, zero_mistakes(x) + [joined_digits(x)], e))
    Ew = []
    for x in [305070, 140602]:                                 # numeral -> words (2)
        used.add(x)
        wr = [words(v) for v in zero_mistakes(x) if 100000 <= v < 1000000][:3]
        e = ("Split %s into two groups: %d thousand and %d. Say each group, then its name: %s."
             % (n(x), x // 1000, x % 1000, words(x)))
        Ew.append(mcq("How do you write %s in words?" % n(x), words(x), wr, e))
    Fx = []
    for x in [340702, 605030]:                                 # expanded -> number (2)
        used.add(x)
        exp = " + ".join(n(digit(x, i) * 10 ** i) for i in range(5, -1, -1) if digit(x, i))
        e = "Put each digit in its place and write 0 in every empty place: %s = %s." % (exp, n(x))
        Fx.append(mcq_n("What number is <b>%s</b>?" % exp, x, zero_mistakes(x) + [joined_digits(x)], e))
    G = [mcq("How many thousands are there in one million?", "1000", ["100", n(10000), n(1000000)],
             "1 000 000 ÷ 1000 = 1000. Ten hundred thousands make one million, and each hundred thousand is "
             "100 thousands: 10 × 100 = 1000 thousands."),
         mcq("In 550 000, the first 5 is worth how many times the second 5?", "10", ["100", "5", n(450000)],
             "The first 5 is worth 500 000. The second 5 is worth 50 000. 500 000 ÷ 50 000 = 10. "
             "Each place is worth 10 times the place to its right. (450 000 is the difference, not how many times.)")]
    its = A[:3] + C + A[3:] + B + Fx + Dw + Ew + G
    assert len(its) == 20
    return {"title": "Place value to one million", "items": its}


# ============================================================ set 2: compare and order large numbers
def first_diff(a, b):
    for i in range(6, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def compare_expl(big, small):
    if ndig(big) != ndig(small):
        return ("%s has %d digits and %s has only %d, so %s is greater."
                % (n(big), ndig(big), n(small), ndig(small), n(big)))
    i = first_diff(big, small)
    same = ("The digits are the same until the %s place" % PL[i]) if i < ndig(big) - 1 else "Start with the %s" % PL[i]
    return ("Compare from the left. %s: %s is more than %s. So %s &gt; %s."
            % (same, plural(digit(big, i), i), plural(digit(small, i), i), n(big), n(small)))


def lookalikes(rnd, used):
    """4 different 6-digit numbers made from the same digits, with the same first digit."""
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
    for x, y in [(608945, 609845), (98765, 102300), (571020, 570120), (304560, 340560)]:
        lt, gt = "&lt;", "&gt;"
        right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
        wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
                 "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 98765:
            e += " A big first digit does not matter when a number has fewer digits."
        its.append(mcq("Which is true?", right, wrong, e))
    for j in range(6):
        if j == 2:
            nums = [99875, 108900, 109800, 100980]
        elif j == 5:
            nums = [206040, 99999, 200640, 206400]
        else:
            nums = lookalikes(rnd, used)
        nums = sorted(nums)
        want_max = j < 3
        ans = nums[-1] if want_max else nums[0]
        nxt = nums[-2] if want_max else nums[1]
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % n(ans)
            if 99875 in nums:
                e = ("99 875 has only 5 digits, so it is the least, even though it starts with 9. "
                     "Of the 6-digit numbers: " + compare_expl(ans, nxt) + " %s is the greatest." % n(ans))
        else:
            e = compare_expl(nxt, ans) + " %s is the least." % n(ans)
            if 99999 in nums:
                e = "99 999 has only 5 digits, so it is the least. Every 6-digit number is at least 100 000."
        its.append(mcq("Which number is the %s?" % ("greatest" if want_max else "least"), n(ans),
                       [n(v) for v in nums if v != ans], e))
    fmt = lambda l: ", ".join(n(v) for v in l)
    for j in range(3):
        while True:
            nums = lookalikes(rnd, used)
            three = rnd.sample(nums, 3)
            if three != sorted(three) and three != sorted(three)[::-1]:
                break
        up = j < 2
        o = sorted(three) if up else sorted(three)[::-1]
        perms = [[o[0], o[2], o[1]], [o[1], o[0], o[2]], o[::-1]]
        a, b, cc = sorted(three)
        i1, i2 = first_diff(b, a), first_diff(cc, b)
        e = ("Compare from the left. %s &lt; %s (%s: %d &lt; %d). %s &lt; %s (%s: %d &lt; %d). So the order is %s."
             % (n(a), n(b), PL[i1], digit(a, i1), digit(b, i1), n(b), n(cc), PL[i2], digit(b, i2), digit(cc, i2), fmt(o)))
        its.append(mcq("Put %s in order from %s." % (fmt(three), "least to greatest" if up else "greatest to least"),
                       fmt(o), [fmt(p) for p in perms], e))
    assert 495300 + 10000 == 505300 and 203450 - 10000 == 193450
    its.append(mcq_n("What is 10 000 more than 495 300?", 505300, [496300, 405300, 595300],
                     "Add 1 to the ten thousands digit: 9 ten thousands + 1 = 10 ten thousands. Regroup them as "
                     "1 hundred thousand: 4 + 1 = 5 hundred thousands. 495 300 + 10 000 = 505 300."))
    its.append(mcq_n("What is 10 000 less than 203 450?", 193450, [202450, 103450, 213450],
                     "There are 0 ten thousands, so regroup 1 hundred thousand as 10 ten thousands. "
                     "10 − 1 = 9 ten thousands and 1 hundred thousand is left. 203 450 − 10 000 = 193 450."))
    for lo, hi, step, labels, v, wrongs, e in [
        (300000, 400000, 10000, [300000, 350000, 400000], 370000, [307000, 330000, 380000],
         "From 300 000 to 400 000 there are 10 equal spaces, so each space is 10 000, not 1000. "
         "The arrow is 7 spaces after 300 000: 300 000 + 70 000 = 370 000."),
        (0, 1000000, 100000, [0, 500000, 1000000], 600000, [60000, 400000, 700000],
         "From 0 to 1 000 000 there are 10 equal spaces, so each space is 100 000. "
         "The arrow is 1 space after 500 000: 500 000 + 100 000 = 600 000."),
    ]:
        its.append(mcq_n(fig(big_line_svg(lo, hi, step, labels, arrow=v)) + "What number does the arrow point to?",
                         v, wrongs, e))
    assert 528400 > 527600 and 527400 < 527600 and 304500 < 312900 < 314500
    its.append(mcq("52☐" + NB + "400 &gt; 527" + NB + "600. Which digit could go in the box?", "8", ["4", "6", "7"],
                   "The hundred thousands and ten thousands are the same. Compare the thousands: the box must be 7 or "
                   "more. If it is 7, compare the hundreds: 4 &lt; 6, so 527 400 is too small. 528 400 &gt; 527 600."))
    its.append(mcq("3☐4" + NB + "500 &lt; 312" + NB + "900. Which digit could go in the box?", "0", ["1", "2", "5"],
                   "The hundred thousands are the same. Compare the ten thousands: the box must be 1 or less. "
                   "If it is 1, compare the thousands: 4 &gt; 2, so 314 500 is too big. 304 500 &lt; 312 900."))
    its.append(mcq_n("Use each of the digits 4, 0, 8, 2, 6 and 9 once. What is the greatest 6-digit number you can make?",
                     986420, [986402, 968420, 204689],
                     "Put the biggest digit in the hundred thousands place, then the next biggest, and so on: "
                     "9, 8, 6, 4, 2, 0. The greatest number is 986 420."))
    assert len(its) == 20
    order = its[:4] + its[13:15] + its[4:10] + its[15:17] + its[10:13] + its[17:]
    assert len({id(x) for x in order}) == 20
    return {"title": "Compare and order numbers to one million", "items": order}


# ============================================================ set 3: decimals to thousandths
def set_decimals():
    its = []
    its.append(mcq(fig(dchart_svg("4.307", hi=-3)) + "What is the value of the red digit in 4.307?",
                   "7 thousandths", ["7 hundredths", "7 tenths", "7 ones"],
                   "The red 7 is the <b>third</b> digit after the decimal point, in the thousandths place. "
                   "Its value is 7 thousandths = 0.007. The 0 holds the hundredths place."))
    its.append(mcq(fig(dchart_svg("6.054", hi=-2)) + "What is the value of the red digit in 6.054?",
                   "5 hundredths", ["5 tenths", "5 thousandths", "5 ones"],
                   "The red 5 is the <b>second</b> digit after the decimal point, in the hundredths place. "
                   "Its value is 5 hundredths = 0.05."))
    its.append(mcq(fig(dchart_svg("13.582", hi=-1)) + "What is the value of the red digit in 13.582?",
                   "5 tenths", ["5 hundredths", "5 ones", "5 tens"],
                   "The red 5 is the <b>first</b> digit after the decimal point, in the tenths place. "
                   "Its value is 5 tenths = 0.5."))
    its.append(mcq("What is the value of the digit 8 in 7.286?", "0.08", ["0.8", "0.008", "8"],
                   "7 . 2 <b>8</b> 6: the 8 is the second digit after the decimal point, in the hundredths place. "
                   "It is worth 8 hundredths = 0.08."))
    its.append(mcq("In which place is the digit 6 in 0.036?", "thousandths", ["hundredths", "tenths", "ones"],
                   "0 . 0 3 <b>6</b>: tenths, hundredths, thousandths. The 6 is in the thousandths place."))
    its.append(mcq("In 9.473, which digit is in the hundredths place?", "7", ["4", "3", "9"],
                   "After the decimal point the places are tenths (4), hundredths (7) and thousandths (3). "
                   "So the hundredths digit is 7."))
    its.append(mcq("In 21.509, which digit is in the thousandths place?", "9", ["0", "5", "1"],
                   "After the decimal point: tenths 5, hundredths 0, thousandths 9. The thousandths digit is 9."))
    its.append(mcq("Write 5 ones, 4 hundredths and 1 thousandth as a decimal.", "5.041", ["5.41", "5.401", "5.0041"],
                   "There are 0 tenths, so write a 0 in the tenths place: 5 . 0 4 1 = 5.041. "
                   "5.41 would have 4 tenths."))
    assert D("3") + D("0.8") + D("0.02") + D("0.007") == D("3.827")
    its.append(mcq("3 + 0.8 + 0.02 + 0.007 = ?", "3.827", ["3.728", "38.27", "3.0827"],
                   "3 ones, 8 tenths, 2 hundredths and 7 thousandths: 3 . 8 2 7 = 3.827."))
    its.append(mcq("Which shows 6.135 in expanded form?", "6 + 0.1 + 0.03 + 0.005",
                   ["6 + 0.1 + 0.3 + 0.05", "6 + 1 + 3 + 5", "6 + 0.01 + 0.003 + 0.5"],
                   "6 ones, 1 tenth, 3 hundredths and 5 thousandths: 6 + 0.1 + 0.03 + 0.005."))
    assert D("6") + D("0.1") + D("0.03") + D("0.005") == D("6.135")
    its.append(mcq("Which number is <b>four and twenty-six thousandths</b>?", "4.026", ["4.26", "4.206", "4.0026"],
                   "“And” stands for the decimal point. Twenty-six thousandths must end in the <b>third</b> place "
                   "after the point: 4.026. 4.26 would be twenty-six hundredths."))
    its.append(mcq("How do you read 0.305 in words?", dec_words("0.305"),
                   ["three hundred five hundredths", "thirty-five thousandths", "three and five thousandths"],
                   "0.305 has three decimal places, so read the digits as a whole number and say “thousandths”: "
                   "three hundred five thousandths."))
    its.append(mcq("Write 0.045 as a fraction.", fr(45, 1000), [fr(45, 100), fr(45, 10), fr(5, 1000)],
                   "0.045 has <b>three</b> decimal places, so it is thousandths: 45 thousandths = %s. "
                   "%s would be 0.45." % (fr(45, 1000), fr(45, 100))))
    assert F(D("0.045")) == F(45, 1000)
    its.append(mcq("How many thousandths are there in 0.4?", "400", ["4", "40", "4000"],
                   "1 tenth = 100 thousandths, so 4 tenths = 400 thousandths. 0.4 = 0.400."))
    its.append(mcq("Which number is equal to 0.7?", "0.700", ["0.07", "0.007", "7.00"],
                   "A 0 at the <b>end</b> of a decimal does not change its value: 0.7 = 0.70 = 0.700. "
                   "0.07 and 0.007 have the 7 in a different place."))
    its.append(mcq("In 3.33, the 3 in the tenths place is worth how many times the 3 in the hundredths place?",
                   "10", ["100", "1000", "3"],
                   "Each place is worth 10 times the place to its right. 0.3 = 10 × 0.03. So the answer is 10."))
    assert D("5.309") + D("0.001") == D("5.31")
    its.append(mcq("What number is 0.001 more than 5.309?", "5.31", ["5.319", "5.3010", "5.409"],
                   "9 thousandths + 1 thousandth = 10 thousandths = 1 hundredth. So 5.309 + 0.001 = 5.310 = 5.31. "
                   "5.319 adds 1 hundredth, not 1 thousandth."))
    assert D("1.495") + D("0.01") == D("1.505")
    its.append(mcq("What number is 0.01 more than 1.495?", "1.505", ["1.496", "1.595", "1.4105"],
                   "Add 1 hundredth: 9 hundredths + 1 hundredth = 10 hundredths = 1 tenth. "
                   "So 1.495 + 0.01 = 1.505. 1.496 adds only 1 thousandth."))
    assert D("8.04") - D("0.1") == D("7.94")
    its.append(mcq("What number is 0.1 less than 8.04?", "7.94", ["8.03", "8.14", "7.04"],
                   "Take away 1 tenth. 8.04 has 0 tenths, so regroup 1 one as 10 tenths: 8.04 − 0.1 = 7.94. "
                   "8.03 takes away 1 hundredth."))
    its.append(mcq("Use each of the digits 2, 7, 4 and 9 once to make the <b>greatest</b> number with "
                   "1 digit before the decimal point and 3 digits after it.", "9.742", ["9.724", "2.479", "7.942"],
                   "Put the largest digit in the ones place, then the next largest in the tenths, hundredths and "
                   "thousandths places: 9.742. 2.479 is the least number you can make."))
    its = reorder(its, [0, 1, 2, 3, 4, 5, 6, 14, 7, 8, 9, 13, 12, 10, 11, 15, 16, 17, 18, 19])
    return {"title": "Decimals to thousandths", "items": its}


# ============================================================ set 4: compare and order decimals
def cmp_item(x, y, e):
    a, b = Dm(x), Dm(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare <b>%s</b> and <b>%s</b>." % (x, y), right, wrong, e)


def order_q(q, nums, asc, wrongs, e):
    right = ", ".join(sorted(nums, key=Dm, reverse=not asc))
    ws = [", ".join(w) for w in wrongs]
    assert right not in ws and len(set(ws)) == 3
    for w in wrongs:
        assert sorted(w) == sorted(nums)
    assert right in e
    return mcq(q, right, ws, e)


def dot_q(a, b, spaces, labels, dot, wrong, e):
    return mcq(fig(dline_svg(a, b, spaces, labels, dot)) + "What number is at the red dot?", dec(dot), wrong, e)


def set_dcompare():
    its = []
    its.append(cmp_item("0.45", "0.5", "0.5 = 0.50. Compare the tenths: 4 tenths &lt; 5 tenths. So 0.45 &lt; 0.5. "
                        "More digits does not mean a greater number."))
    its.append(cmp_item("0.6", "0.58", "0.6 = 0.60. Compare the tenths: 6 &gt; 5. So 0.6 &gt; 0.58."))
    its.append(cmp_item("3.08", "3.080", "A 0 at the end does not change the value. 3.08 = 3.080, so 3.08 = 3.080."))
    its.append(cmp_item("0.007", "0.07", "0.07 = 0.070. Compare the hundredths: 0 &lt; 7. So 0.007 &lt; 0.07. "
                        "7 thousandths is less than 7 hundredths."))
    its.append(cmp_item("0.99", "1.01", "Compare the ones first: 0 &lt; 1. So 0.99 &lt; 1.01. "
                        "Any number less than 1 is less than any number greater than 1."))
    its.append(cmp_item("0.125", "0.13", "Write both with 3 places: 0.125 and 0.130. The tenths are the same. "
                        "Compare the hundredths: 2 &lt; 3. So 0.125 &lt; 0.13. Do not compare 125 with 13."))
    its.append(cmp_item("4.216", "4.21", "4.21 = 4.210. Ones, tenths and hundredths are the same. "
                        "Compare the thousandths: 6 &gt; 0. So 4.216 &gt; 4.21."))
    its.append(cmp_item("2.8", "2.799", "2.8 = 2.800. The ones are the same. Compare the tenths: 8 &gt; 7. "
                        "So 2.8 &gt; 2.799."))
    its.append(mcq("Which number is the <b>greatest</b>?", "0.6", ["0.59", "0.599", "0.065"],
                   "Write them with 3 places: 0.600, 0.590, 0.599, 0.065. Compare the tenths first: only 0.6 has "
                   "6 tenths. So 0.6 is the greatest."))
    its.append(mcq("Which number is the <b>least</b>?", "0.304", ["0.34", "0.4", "0.43"],
                   "Write them with 3 places: 0.304, 0.340, 0.400, 0.430. The least is 0.304, "
                   "even though it has the most digits."))
    its.append(mcq("Which number is the <b>greatest</b>?", "7.2", ["6.998", "7.19", "7.199"],
                   "Compare the ones first: 6.998 has only 6 ones. Then 7.200, 7.190, 7.199: 2 tenths is more than "
                   "1 tenth. So 7.2 is the greatest."))
    its.append(order_q("Order from <b>least to greatest</b>: 0.5, 0.45, 0.405", ["0.5", "0.45", "0.405"], True,
                       [["0.5", "0.45", "0.405"], ["0.45", "0.405", "0.5"], ["0.405", "0.5", "0.45"]],
                       "Write them with 3 places: 0.500, 0.450, 0.405. Compare 500, 450 and 405 thousandths. "
                       "So 0.405, 0.45, 0.5."))
    its.append(order_q("Order from <b>least to greatest</b>: 2.7, 2.07, 1.97, 2.069", ["2.7", "2.07", "1.97", "2.069"],
                       True, [["2.07", "2.069", "2.7", "1.97"], ["1.97", "2.7", "2.07", "2.069"],
                              ["2.069", "2.07", "2.7", "1.97"]],
                       "1.97 has only 1 one, so it is the least. Then write the rest with 3 places: 2.700, 2.070, "
                       "2.069. So 1.97, 2.069, 2.07, 2.7."))
    its.append(order_q("Order from <b>greatest to least</b>: 5.3, 5.28, 5.305, 5.03", ["5.3", "5.28", "5.305", "5.03"],
                       False, [["5.305", "5.28", "5.3", "5.03"], ["5.03", "5.28", "5.3", "5.305"],
                               ["5.3", "5.305", "5.28", "5.03"]],
                       "Write them with 3 places: 5.300, 5.280, 5.305, 5.030. Greatest first: 5.305, 5.3, 5.28, 5.03."))
    its.append(order_q("Order from <b>least to greatest</b>: 0.8, 0.08, 0.808, 0.088", ["0.8", "0.08", "0.808", "0.088"],
                       True, [["0.08", "0.8", "0.088", "0.808"], ["0.8", "0.08", "0.088", "0.808"],
                              ["0.088", "0.08", "0.808", "0.8"]],
                       "Write them with 3 places: 0.800, 0.080, 0.808, 0.088. Compare 800, 80, 808 and 88 thousandths. "
                       "So 0.08, 0.088, 0.8, 0.808."))
    its.append(dot_q(300, 400, 10, [300, 400], 370, ["0.307", "0.7", "0.47"],
                     "From 0.3 to 0.4 there are 10 equal spaces, so each space is 1 hundredth (0.01). "
                     "Count 7 spaces on from 0.30: 0.37."))
    its.append(dot_q(5200, 5210, 10, [5200, 5205, 5210], 5204, ["5.24", "5.214", "5.206"],
                     "From 5.2 to 5.21 there are 10 equal spaces. 5.21 − 5.20 = 0.01, so each space is 1 thousandth. "
                     "Count 4 spaces on from 5.200: 5.204."))
    its.append(dot_q(680, 690, 10, [680, 690], 683, ["0.71", "0.6803", "0.638"],
                     "From 0.68 to 0.69 there are 10 equal spaces, so each space is 1 thousandth, not 1 hundredth. "
                     "Count 3 spaces on from 0.680: 0.683."))
    assert D("0.6") < D("0.608") < D("0.7")
    its.append(mcq("Which number is between 0.6 and 0.7?", "0.608", ["0.068", "0.71", "0.599"],
                   "0.6 = 0.600 and 0.7 = 0.700. 0.608 is between them. 0.068 and 0.599 are less than 0.6, "
                   "and 0.71 is more than 0.7."))
    assert D("0.737") < D("0.74") < D("0.747")
    its.append(mcq("0.7☐7 &lt; 0.74. What is the <b>greatest</b> digit that can go in the box?", "3", ["4", "9", "2"],
                   "0.74 = 0.740. With 3 in the box: 0.737 &lt; 0.740. With 4: 0.747 &gt; 0.740. "
                   "So the greatest digit is 3."))
    its = reorder(its, [0, 1, 2, 3, 4, 8, 9, 15, 5, 6, 7, 10, 16, 11, 12, 17, 13, 14, 18, 19])
    return {"title": "Compare and order decimals", "items": its}


# ============================================================ set 5: rounding in context
def rint(x, p):
    return ((x + p // 2) // p) * p


NAME_P = {1000: "thousand", 10000: "ten thousand", 100000: "hundred thousand", 100: "hundred"}
NAME_D = {0: "whole number", 1: "tenth", 2: "hundredth"}
DPL = {0: "ones", 1: "tenths", 2: "hundredths", 3: "thousandths"}


def rint_e(x, p):
    lo = x // p * p
    r = rint(x, p)
    k = len(str(p)) - 1
    d = digit(x, k - 1)
    s = ("%s is between %s and %s. Look at the %s digit, one place to the right of the %s: %d. %s, so round %s."
         % (n(x), n(lo), n(lo + p), PL[k - 1], PL[k], d, "5 or more" if d >= 5 else "4 or less",
            "up" if r > lo else "down"))
    if r > lo and digit(x, k) == 9:
        s += " The %s digit is 9, so rounding up makes 10 %s. Regroup them as 1 %s." % (PL[k], PL[k], PL1[k + 1])
    return s


def rdec_e(x, places):
    """Explanation for rounding the decimal string x to `places` places."""
    q = Dm(1).scaleb(-places)
    lo = Dm(x).quantize(q, rounding="ROUND_FLOOR")
    hi = lo + q
    r = Dm(rd(x, places))
    nxt = int(x.partition(".")[2][places])
    s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s to %s."
         % (x, lo, hi, DPL[places + 1], nxt, "5 or more" if nxt >= 5 else "4 or less",
            "up" if r > lo else "down", r))
    return s


def set_round(rnd):
    its = []
    # 0 Winnipeg nearest thousand (9 regroup)
    x = 749607
    assert rint(x, 1000) == 750000
    its.append(mcq_n("At the 2021 census, Winnipeg had a population of 749 607. "
                     "What is this rounded to the nearest thousand?", 750000, [749000, 740000, 749600],
                     rint_e(x, 1000) + " Answer: 750 000 people.", " people"))
    # 1 Hamilton nearest ten thousand
    x = 569353
    assert rint(x, 10000) == 570000
    its.append(mcq_n("At the 2021 census, Hamilton had a population of 569 353. "
                     "What is this rounded to the nearest ten thousand?", 570000, [560000, 569000, 600000],
                     rint_e(x, 10000) + " Answer: 570 000 people.", " people"))
    # 2 Quebec City nearest hundred thousand (rounding twice)
    x = 549459
    assert rint(x, 100000) == 500000 and rint(rint(x, 10000), 100000) == 600000
    its.append(mcq_n("At the 2021 census, Québec City had a population of 549 459. "
                     "What is this rounded to the nearest hundred thousand?", 500000, [600000, 550000, 549000],
                     rint_e(x, 100000) + " Do not round twice (549 459 → 550 000 → 600 000). Answer: 500 000 people.",
                     " people"))
    # 3 Victoria nearest ten thousand
    x = 91867
    assert rint(x, 10000) == 90000
    its.append(mcq_n("At the 2021 census, the city of Victoria had a population of 91 867. "
                     "What is this rounded to the nearest ten thousand?", 90000, [92000, 100000, 91000],
                     rint_e(x, 10000) + " Answer: 90 000 people.", " people"))
    # 4 hockey tickets nearest thousand
    x = 148652
    assert rint(x, 1000) == 149000
    its.append(mcq_n("A junior hockey team sold 148 652 tickets in one season. "
                     "What is this rounded to the nearest thousand?", 149000, [148000, 150000, 148700],
                     rint_e(x, 1000) + " Answer: 149 000 tickets.", " tickets"))
    # 5 pumpkin nearest tenth
    assert rd("4.68", 1) == "4.7"
    its.append(mcq("A pumpkin at the fall fair has a mass of 4.68 kg. What is its mass to the nearest tenth "
                   "of a kilogram?", "4.7 kg", ["4.6 kg", "5 kg", "4.8 kg"],
                   rdec_e("4.68", 1) + " 4.6 kg just cuts off the 8. Answer: 4.7 kg."))
    # 6 100 m nearest tenth
    assert rd("14.37", 1) == "14.4"
    its.append(mcq("In gym class, Ethan ran 100 m in 14.37 seconds. What is his time to the nearest tenth "
                   "of a second?", "14.4 s", ["14.3 s", "14 s", "15 s"],
                   rdec_e("14.37", 1) + " Answer: 14.4 s."))
    # 7 Terry Fox Run nearest whole
    assert rd("4.65", 0) == "5"
    its.append(mcq("Owen walked 4.65 km in the Terry Fox Run. What is this distance to the nearest whole kilometre?",
                   "5 km", ["4 km", "4.7 km", "4.6 km"],
                   "4.65 is between 4 and 5. Look at the tenths digit: 6. 5 or more, so round up to 5. "
                   "4.7 km is the nearest tenth, not the nearest whole number. Answer: 5 km."))
    # 8 field trip nearest dollar
    assert rd("18.65", 0) == "19"
    its.append(mcq("A field trip to the science centre costs $18.65 per student. What is this to the nearest dollar?",
                   "$19", ["$18", "$18.70", "$20"],
                   "$18.65 is between $18 and $19. Look at the tenths (dimes) digit: 6. 5 or more, so round up. "
                   "$18.70 is the nearest ten cents, and $20 is the nearest ten dollars. Answer: $19."))
    # 9 speed skating nearest hundredth
    assert rd("41.358", 2) == "41.36"
    its.append(mcq("Mei skated 500 m at the speed skating oval in 41.358 seconds. What is her time to the nearest "
                   "hundredth of a second?", "41.36 s", ["41.35 s", "41.4 s", "41.3 s"],
                   rdec_e("41.358", 2) + " 41.35 s just cuts off the 8, and 41.4 s rounds to the tenths. "
                   "Answer: 41.36 s."))
    # 10 gas price nearest cent
    assert rd("1.479", 2) == "1.48"
    its.append(mcq("Gas costs $1.479 per litre. What is this price to the nearest cent (hundredth of a dollar)?",
                   "$1.48", ["$1.47", "$1.50", "$1.40"],
                   rdec_e("1.479", 2) + " A cent is a hundredth of a dollar, so keep two decimal places. Answer: $1.48."))
    # 11 snowfall 9 regroup
    assert rd("12.95", 1) == "13.0"
    its.append(mcq("On a snow day, 12.95 cm of snow fell. What is this to the nearest tenth of a centimetre?",
                   "13.0 cm", ["12.9 cm", "12.10 cm", "12.0 cm"],
                   "12.95 is between 12.9 and 13.0. Look at the hundredths digit: 5. 5 or more, so round up. "
                   "9 tenths + 1 tenth = 10 tenths = 1 one, so 12.9 becomes 13.0. Do not write 12.10. Answer: 13.0 cm."))
    # 12 apples 9 regroup hundredths
    assert rd("2.496", 2) == "2.50"
    its.append(mcq("A bag of Ontario apples has a mass of 2.496 kg. What is this to the nearest hundredth of a kilogram?",
                   "2.50 kg", ["2.49 kg", "2.410 kg", "2.40 kg"],
                   "2.496 is between 2.49 and 2.50. Look at the thousandths digit: 6. 5 or more, so round up. "
                   "9 hundredths + 1 hundredth = 10 hundredths = 1 tenth, so 2.49 becomes 2.50. Answer: 2.50 kg."))
    # 13 long jump nearest hundredth, half up
    assert rd("3.475", 2) == "3.48"
    its.append(mcq("Priya jumped 3.475 m in the long jump at the track meet. What is this to the nearest hundredth "
                   "of a metre?", "3.48 m", ["3.47 m", "3.5 m", "3.4 m"],
                   "3.475 is exactly halfway between 3.47 and 3.48. A number that is exactly halfway rounds up. "
                   "Answer: 3.48 m."))
    # 14 which time does NOT round to 36.5
    ts = ["36.44", "36.48", "36.53", "36.46"]
    assert [rd(t, 1) for t in ts] == ["36.4", "36.5", "36.5", "36.5"]
    its.append(mcq("Four swimmers raced 50 m. Which time does <b>not</b> round to 36.5 s to the nearest tenth?",
                   "36.44 s", ["36.48 s", "36.53 s", "36.46 s"],
                   "Times from 36.45 s up to (but not including) 36.55 s round to 36.5 s. 36.44 has 4 hundredths, "
                   "so it rounds down to 36.4 s."))
    # 15 which time rounds to 52.3
    ts = ["52.26", "52.36", "52.21", "52.35"]
    assert [rd(t, 1) for t in ts] == ["52.3", "52.4", "52.2", "52.4"]
    its.append(mcq("Hana’s 400 m time, rounded to the nearest tenth, is 52.3 seconds. Which could be her real time?",
                   "52.26 s", ["52.36 s", "52.21 s", "52.35 s"],
                   "Times from 52.25 s to 52.34 s round to 52.3 s. 52.26 s is in that range. 52.36 s and 52.35 s "
                   "round up to 52.4 s, and 52.21 s rounds down to 52.2 s."))
    # 16 Windsor reverse
    for w, r in [(229660, 230000), (235000, 240000), (224800, 220000), (239000, 240000)]:
        assert rint(w, 10000) == r
    its.append(mcq("A news report says that about 230 000 people lived in Windsor, Ontario, in 2021. The number was "
                   "rounded to the nearest ten thousand. Which could be the real population?",
                   n(229660), [n(235000), n(224800), n(239000)],
                   "Numbers from 225 000 to 234 999 round to 230 000. 229 660 is in that range. 235 000 and 239 000 "
                   "round up to 240 000, and 224 800 rounds down to 220 000."))
    # 17 smallest that rounds
    assert rint(245000, 10000) == 250000 and rint(244999, 10000) == 240000 and rint(254999, 10000) == 250000
    its.append(mcq("The population of a town, rounded to the nearest ten thousand, is 250 000. "
                   "What is the least the population could be?", n(245000), [n(240000), n(249999), n(254999)],
                   "Numbers from 245 000 to 254 999 round to 250 000. 244 999 would round down to 240 000, "
                   "so the least is 245 000. (254 999 is the greatest.)"))
    # 18 least race time that rounds to 12.7
    assert rd("12.65", 1) == "12.7" and rd("12.64", 1) == "12.6" and rd("12.74", 1) == "12.7"
    its.append(mcq("A race time rounded to the nearest tenth is 12.7 s. The real time was measured to the hundredth. "
                   "What is the <b>least</b> it could be?", "12.65 s", ["12.60 s", "12.70 s", "12.74 s"],
                   "Times from 12.65 s to 12.74 s round to 12.7 s. 12.64 s would round down to 12.6 s, "
                   "so the least is 12.65 s. (12.74 s is the greatest.)"))
    # 19 rounding twice, decimals
    assert rd("48.346", 1) == "48.3" and rd(rd("48.346", 2), 1) == "48.4"
    its.append(mcq("Kai’s ski race time was 48.346 s. He rounded it to the nearest hundredth (48.35 s), then rounded "
                   "that to the nearest tenth and got 48.4 s. What is 48.346 s rounded to the nearest tenth?",
                   "48.3 s", ["48.4 s", "48.35 s", "48 s"],
                   "Always round the number you started with. 48.346 is between 48.3 and 48.4. Look at the "
                   "hundredths digit: 4. 4 or less, so round down to 48.3 s. Rounding twice gives the wrong answer."))
    its = reorder(its, [5, 0, 6, 1, 7, 3, 8, 4, 10, 9, 2, 13, 11, 12, 14, 16, 15, 17, 18, 19])
    return {"title": "Rounding decimals and large numbers in real life", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Place value to one million</h2>"
        "<p>Each place is worth <b>10 times</b> the place to its right. Big numbers are split into groups of three "
        "digits: <b>thousands</b> and <b>ones</b>. In Canada we leave a small space between the groups "
        "(245 300), not a comma. A 4-digit number has no space (4536).</p>"
        "<figure class='sn-fig'>" + chart_svg(406005, hi=5) +
        "<figcaption>406 005: the 4 is in the hundred thousands place, so it is worth 400 000. "
        "The zeros hold the empty places.</figcaption></figure>"
        + ex("Words to digits", "Write four hundred six thousand five in digits.",
             "Four hundred six thousand → 406. Five → 005 (no hundreds and no tens, so write 0s).", "406 005")
        + "<p>Ten hundred thousands make <b>one million</b>: 1 000 000.</p>"
        "<h2>Compare and order large numbers</h2>"
        "<p>First count the digits: a 6-digit number is greater than any 5-digit number. If both have the same "
        "number of digits, compare place by place from the left until two digits are different.</p>"
        + ex("Compare", "571 020 ☐ 570 120",
             "Hundred thousands: 5 = 5. Ten thousands: 7 = 7. Thousands: 1 &gt; 0.", "571 020 &gt; 570 120")
        + "<h2>Decimals to thousandths</h2>"
        "<p>After the decimal point come <b>tenths</b>, <b>hundredths</b> and <b>thousandths</b>. "
        "1 hundredth split into 10 equal parts makes 10 thousandths. Read the word “and” as the decimal point.</p>"
        "<figure class='sn-fig'>" + dchart_svg("4.307", hi=-3) +
        "<figcaption>4.307 is “four and three hundred seven thousandths”. The 7 is worth 7 thousandths = 0.007.</figcaption></figure>"
        "<h2>Compare and order decimals</h2>"
        "<p>Compare the <b>whole numbers</b> first. Then give the decimals the same number of places by adding zeros "
        "at the end, and compare from the left: tenths, hundredths, thousandths.</p>"
        + ex("Example", "Order 0.5, 0.45 and 0.405 from least to greatest.",
             "Write 0.500, 0.450 and 0.405. Compare 500, 450 and 405 thousandths.", "0.405, 0.45, 0.5")
        + "<h2>Rounding</h2>"
        "<ol class='rk-step'><li>Find the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to its right</b>.</li>"
        "<li><b>5 or more</b>: round up. <b>4 or less</b>: round down.</li>"
        "<li>Whole numbers: change the digits after that place to 0. Decimals: drop the digits after that place.</li></ol>"
        "<figure class='sn-fig'>" + dline_svg(4600, 4700, 10, [4600, 4650, 4700], dot=4680, dot_label=True) +
        "<figcaption>4.68 is past the halfway point, 4.65, so to the nearest tenth it rounds to 4.7.</figcaption></figure>"
        + table(["Round", "Look at", "Answer"], [
            ["749 607 to the nearest thousand", "the hundreds digit: 6", "750 000"],
            ["549 459 to the nearest hundred thousand", "the ten thousands digit: 4", "500 000"],
            ["4.68 to the nearest whole number", "the tenths digit: 6", "5"],
            ["4.68 to the nearest tenth", "the hundredths digit: 8", "4.7"],
            ["41.358 to the nearest hundredth", "the thousandths digit: 8", "41.36"],
        ])
        + ex("Watch the 9s", "Round 12.95 to the nearest tenth.",
             "The hundredths digit is 5, so round up. 9 tenths + 1 tenth = 10 tenths = 1 one. 12.9 becomes 13.0.", "13.0")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.45 &gt; 0.5 because it has more digits", "Use the same number of places: 0.45 &lt; 0.50"],
            ["Missing a zero (four hundred six thousand five → 46 005)", "Write each group as three digits: 406 | 005"],
            ["Giving the digit, not its value (the 4 in 406 005 is 4)", "It is in the hundred thousands place: 400 000"],
            ["Rounding the wrong place (4.68 to the nearest tenth → 5)", "Find the tenths digit first: 4.7"],
            ["Cutting off instead of rounding (41.358 → 41.35)", "Look at the next digit: 8, so round up to 41.36"],
            ["Rounding twice (549 459 → 550 000 → 600 000)", "Round the number you started with: 500 000"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about place value in the Ontario math curriculum?",
     "a": "In Grade 6 (Number, B1) students read, represent, compare and order whole numbers up to one million "
          "and decimals to thousandths. They also round decimals to the nearest tenth, hundredth or whole number."},
    {"q": "Why do Canadian students write 245 300 with a space instead of a comma?",
     "a": "Canada follows the SI style: numbers with 5 or more digits are split into groups of three with a small "
          "space, and 4-digit numbers have no space (4536). This avoids mix-ups with the decimal comma used in French."},
    {"q": "Which is bigger, 0.45 or 0.5?",
     "a": "0.5 is bigger. Write both with the same number of places, 0.45 and 0.50, and compare the tenths: "
          "5 tenths is more than 4 tenths."},
    {"q": "How do you round a decimal to the nearest tenth?",
     "a": "Look at the hundredths digit. If it is 5 or more, round up; if it is 4 or less, keep the tenths digit. "
          "So 4.68 rounds to 4.7 and 4.63 rounds to 4.6."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (245 300) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "body_html"):
        u[k] = nbsp(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nbsp(f["q"]), nbsp(f["a"])
    for s in u["sets"]:
        s["title"] = nbsp(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = nbsp(it["q"]), nbsp(it["e"])
            it["c"] = [nbsp(c) for c in it["c"]]
    return u


def mark_large(u, pattern):
    """Tag wide pictures (place value charts, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(36803)
    used = set()
    sets = [set_whole(rnd, used), set_compare(rnd, used), set_decimals(), set_dcompare(), set_round(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "large-numbers-and-decimals", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Large Numbers and Decimals: Place Value to One Million and Thousandths",
        "seo_title": "Grade 6 Large Numbers and Decimals Worksheets: Place Value, Comparing and Rounding (Free, Answer Key)",
        "short_title": "Large numbers and decimals",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compare, and order whole numbers up to and including one million and decimal numbers up to thousandths, and round decimal numbers to the nearest tenth, hundredth, or whole number",
        "meta_desc": "Free Grade 6 math worksheets for the Ontario curriculum: place value to one million, comparing and ordering large numbers, decimals to thousandths, and rounding to the nearest tenth, hundredth or whole number. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Every place is worth 10 times the place to its right, from thousandths all the way up to one million.",
        "key_sub": "Compare decimals place by place, not by length: 0.5 = 0.50 > 0.45. To round, look one place to the right: 5 or more rounds up.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "(number line|place value chart)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
