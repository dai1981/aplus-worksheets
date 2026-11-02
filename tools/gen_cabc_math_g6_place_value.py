# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: Place value from thousandths to billions
(BC Mathematics Curriculum, Grade 6, Number — small to large numbers (thousandths to billions))
  python3 tools/gen_cabc_math_g6_place_value.py
Place value to billions, reading and writing large numbers (BC and Canada census populations),
decimals to thousandths, comparing and ordering large numbers and decimals, and rounding in BC contexts.
Numbers: 4-digit numbers have no separator; 5 or more digits use a no-break space (5 000 879). Never commas.
Every answer is checked with decimal.Decimal / fractions.Fraction (never float).
Wrong answers come from real mistakes: mixing up millions and billions, giving the digit instead of its value,
missing zero placeholders, grouping digits from the left, "longer decimal is bigger" (0.45 > 0.5),
rounding the wrong place, cutting off instead of rounding, writing "10" in the place of a 9, rounding twice.
Census figures are Statistics Canada 2021 Census populations.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#1d5e8c"
FILL = "#d3e5f2"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands",
      "millions", "ten millions", "hundred millions", "billions", "ten billions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand",
       "million", "ten million", "hundred million", "billion", "ten billion"]
MAXV = 10 ** 11


# ------------------------------------------------------------ helpers
def n(x):
    """SI style: 4536, 10 000, 5 000 879 (no-break spaces, never commas)."""
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
    c = re.sub(r"(?<=\d)[ " + NB + r"](?=\d{3}(?!\d))", "", c)
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
PERIOD = ["", " thousand", " million", " billion"]


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
    assert 0 < x < 10 ** 12
    parts, k = [], 0
    while x:
        x, g = divmod(x, 1000)
        if g:
            parts.insert(0, w1000(g) + PERIOD[k])
        k += 1
    return " ".join(parts)


assert words(5000879) == "five million eight hundred seventy-nine"
assert words(2040000000) == "two billion forty million"
assert words(36991981) == "thirty-six million nine hundred ninety-one thousand nine hundred eighty-one"

DEN = {1: "tenths", 2: "hundredths", 3: "thousandths"}


def dec_words(s):
    w, _, f = s.partition(".")
    k = int(f)
    tail = w1000(k) + " " + (DEN[len(f)] if k != 1 else DEN[len(f)][:-1])
    return (w1000(int(w)) + " and " + tail) if int(w) else tail


assert dec_words("6.034") == "six and thirty-four thousandths"
assert dec_words("0.508") == "five hundred eight thousandths"


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
    return [v for v in out if v != x and 1000 <= v < MAXV]


def joined_digits(x):
    return int("".join(ch for ch in str(x) if ch != "0"))


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 42, 28, 26, 44
PNAME = ["Ones", "Thousands", "Millions", "Billions"]


def chart_svg(x, hi=None):
    """Place value chart with periods (Billions | Millions | Thousands | Ones), each H T O.
    Shows as many periods as the number needs (at least 3). hi = place index drawn in red."""
    nd = ndig(x)
    per = max(3, (nd + 2) // 3)
    cols = 3 * per
    x0 = y0 = 6
    W, H = 2 * x0 + cols * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, cols * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, cols * CW, H1 + H2, FILL)]
    for p in range(per):
        k = (per - 1 - p) * 3
        s.append(text(x0 + k * CW + 1.5 * CW, y0 + 19, PNAME[p], 14, bold=True))
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                     % (x0 + k * CW, y0, x0 + k * CW, y0 + H1 + H2 + ROW, GREEN))
    for k in range(cols):
        i = cols - 1 - k
        xx = x0 + k * CW
        if k % 3:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (xx, y0 + H1, xx, y0 + H1 + H2 + ROW, GREEN))
        s.append(text(xx + CW / 2, y0 + H1 + 18, "HTO"[k % 3], 14, bold=True))
        if i < nd:
            s.append(text(xx + CW / 2, y0 + H1 + H2 + 32, str(digit(x, i)), 26, bold=True,
                          col=RED if hi == i else INK))
    for y in (y0 + H1, y0 + H1 + H2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + cols * CW, y, GREEN, "1.2" if y == y0 + H1 else "2"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, cols * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % n(x))


def big_line_svg(lo, hi, step, labels, arrow=None):
    """Number line lo..hi for whole numbers, a tick every step, numbers at `labels`, red arrow at `arrow`."""
    L, R = 72, 448
    W = 520
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


# ============================================================ set 1: place value to billions
def value_cands(d, i):
    return [d * 10 ** (i + 3) if i + 3 <= 10 else None, d * 10 ** (i + 1) if i + 1 <= 10 else None,
            d * 10 ** (i - 1) if i >= 1 else None, d * 10 ** (i - 3) if i >= 3 else None, d,
            d * 10 ** (i - 2) if i >= 2 else None]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), n(v), d, n(v)))


def distinct(rnd, used, k):
    while True:
        ds = rnd.sample(range(10), k)
        if ds[0] == 0:
            continue
        x = int("".join(map(str, ds)))
        if x not in used:
            used.add(x)
            return x


def with_digit(rnd, used, k, i):
    while True:
        x = distinct(rnd, used, k)
        if digit(x, i):
            return x


def set_whole(rnd, used):
    A, B, C = [], [], []
    for k, i in [(9, 6), (10, 9), (9, 8), (10, 7), (10, 5)]:          # chart, red digit (5)
        x = with_digit(rnd, used, k, i)
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    for k, i in [(10, 8), (9, 7), (10, 6), (10, 9)]:                  # value, no chart (4)
        x = with_digit(rnd, used, k, i)
        d = digit(x, i)
        B.append(mcq_n("What is the value of the digit %d in %s?" % (d, n(x)), d * 10 ** i,
                       value_cands(d, i), value_e(d, i)))
    for k, i in [(10, 6), (10, 7)]:                                    # which digit is in a place (2)
        x = with_digit(rnd, used, k, i)
        d = digit(x, i)
        cands = [str(digit(x, j)) for j in sorted(range(k), key=lambda j: (abs(j - i), j)) if j != i][:3]
        e = ("Split the number into groups of three from the right: ones, thousands, millions, billions. "
             "In %s the %s digit is %d, worth %s." % (n(x), PL[i], d, n(d * 10 ** i)))
        C.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    Fx = []
    for x in [3040500207, 806009030]:                                  # expanded -> number (2)
        used.add(x)
        exp = " + ".join(n(digit(x, i) * 10 ** i) for i in range(ndig(x) - 1, -1, -1) if digit(x, i))
        e = "Put each digit in its place and write 0 in every empty place: %s = %s." % (exp, n(x))
        Fx.append(mcq_n("What number is <b>%s</b>?" % exp, x, zero_mistakes(x) + [joined_digits(x)], e))
    G = [mcq("How many millions are there in one billion?", "1000", ["100", "10", n(1000000)],
             "1 000 000 000 ÷ 1 000 000 = 1000. Each period is 1000 times the period before it: "
             "1000 thousands make a million, and 1000 millions make a billion."),
         mcq("Which number is <b>one billion</b>?", n(10 ** 9), [n(10 ** 6), n(10 ** 8), n(10 ** 10)],
             "One billion is 1000 millions. It has 9 zeros in three groups: 1 000 000 000. "
             "1 000 000 is only one million."),
         mcq("How many zeros does one billion have when you write it in digits?", "9", ["6", "12", "10"],
             "One billion = 1 000 000 000: three groups of three zeros, so 9 zeros. One million has 6 zeros."),
         mcq("In 770 000 000, the first 7 is worth how many times the second 7?", "10", ["100", "7", "1000"],
             "The first 7 is worth 700 000 000. The second 7 is worth 70 000 000. 700 000 000 ÷ 70 000 000 = 10. "
             "Each place is worth 10 times the place to its right."),
         mcq_n("What is 10 times 50 000 000?", 500000000, [5000000000, 5000000, 50000010],
               "Multiplying by 10 moves every digit one place to the left: 5 ten millions become 5 hundred millions. "
               "10 × 50 000 000 = 500 000 000."),
         mcq("Which number has a 4 in the hundred millions place?", n(2408135769),
             [n(2048135769), n(2084135769), n(4208135769)],
             "Count the places from the right: ones, tens, hundreds, thousands, …, millions, ten millions, "
             "hundred millions. In 2 408 135 769 the 4 is the first digit of the millions group, worth 400 000 000."),
         mcq("What is the value of the 6 in 6 027 450 000?", "6 billion", ["6 million", "60 million", "600 million"],
             "6 027 450 000 has 10 digits. The 6 is in the fourth group from the right, the billions group. "
             "It is worth 6 billion = 6 000 000 000.")]
    for v in [2408135769, 2048135769, 2084135769, 4208135769]:
        assert (digit(v, 8) == 4) == (v == 2408135769)
    its = A[:2] + C + A[2:] + B + Fx + G
    assert len(its) == 20, len(its)
    order = [14, 15, 13, 0, 1, 4, 5, 6, 2, 3, 18, 7, 8, 9, 10, 19, 16, 17, 11, 12]
    return {"title": "Place value to billions", "items": reorder(its, order)}


# ============================================================ set 2: read and write large numbers
def set_read():
    its = []
    # 0 BC population, words -> digits (zeros)
    x = 5000879
    its.append(mcq_n("At the 2021 census, British Columbia had <b>five million eight hundred seventy-nine</b> people. "
                     "Which number is this?", x, [5879, 5800079, 50000879, 5000000879],
                     "Write each group as three digits. Five million → 5. No thousands → 000. "
                     "Eight hundred seventy-nine → 879. So 5 | 000 | 879 = 5 000 879. The empty thousands group "
                     "still needs three zeros."))
    # 1 Vancouver words -> digits
    x = 662248
    its.append(mcq_n("At the 2021 census, the city of Vancouver had <b>six hundred sixty-two thousand two hundred "
                     "forty-eight</b> people. Which number is this?", x, [66248, 6622480, 662000248],
                     "Six hundred sixty-two thousand → 662 in the thousands group. Two hundred forty-eight → 248. "
                     "So 662 | 248 = 662 248."))
    # 2 Kamloops words -> digits
    x = 97902
    its.append(mcq_n("At the 2021 census, Kamloops had <b>ninety-seven thousand nine hundred two</b> people. "
                     "Which number is this?", x, [97920, 9792, 970902],
                     "Ninety-seven thousand → 97. Nine hundred two → 902 (no tens, so write 0). "
                     "So 97 | 902 = 97 902."))
    # 3 Surrey digits -> words
    its.append(mcq("At the 2021 census, Surrey had 568 322 people. How do you read this number?",
                   words(568322), ["five hundred sixty-eight million three hundred twenty-two",
                                   "fifty-six thousand eight hundred thirty-two", "five hundred sixty-eight three hundred twenty-two"],
                   "Split 568 322 into groups of three: 568 | 322. Read the first group and say “thousand”, then read "
                   "the second group: five hundred sixty-eight thousand three hundred twenty-two."))
    # 4 Prince George digits -> words (zero)
    its.append(mcq("At the 2021 census, Prince George had 76 708 people. How do you read this number?",
                   words(76708), [words(76780), words(760708), words(7678)],
                   "76 708 = 76 | 708. Seventy-six thousand, then seven hundred eight. The 0 means there are no tens, "
                   "so you do not say a tens word."))
    # 5 Canada digits -> words
    its.append(mcq("At the 2021 census, Canada had 36 991 981 people. How do you read this number?",
                   words(36991981), [words(36991981000), words(369919081), words(36000991)],
                   "Split 36 991 981 into groups from the right: 36 | 991 | 981. That is 36 million, "
                   "991 thousand and 981: thirty-six million nine hundred ninety-one thousand nine hundred eighty-one."))
    # 6 Canada area words -> digits
    x = 9984670
    its.append(mcq_n("Canada’s area is <b>nine million nine hundred eighty-four thousand six hundred seventy</b> square "
                     "kilometres. Which number is this?", x, [998467, 9984607, 9000984670],
                     "Nine million → 9. Nine hundred eighty-four thousand → 984. Six hundred seventy → 670. "
                     "So 9 | 984 | 670 = 9 984 670 km².", " km²"))
    # 7 Metro Vancouver decimal millions
    its.append(mcq_n("A news story says that Metro Vancouver has about <b>2.6 million</b> people. "
                     "Which number is 2.6 million?", 2600000, [260000, 2060000, 26000000],
                     "2.6 million = 2 millions and 6 tenths of a million. One tenth of a million is 100 000, "
                     "so 6 tenths is 600 000. 2 000 000 + 600 000 = 2 600 000."))
    # 8 Canada passed 40 million
    its.append(mcq_n("In 2023, Canada’s population passed <b>40 million</b>. Which number is 40 million?",
                     40000000, [40000000000, 4000000, 400000000],
                     "40 million = 40 × 1 000 000 = 40 000 000. Write 40 in the millions group, then two groups of "
                     "000. 40 000 000 000 would be 40 billion."))
    # 9 world population 8 billion
    its.append(mcq_n("There are about <b>8 billion</b> people in the world. Which number is 8 billion?",
                     8000000000, [8000000, 800000000, 80000000000],
                     "One billion is 1000 millions: 1 000 000 000. So 8 billion = 8 000 000 000, with 8 in the "
                     "billions group and three groups of 000 after it. 8 000 000 is only 8 million."))
    # 10 1.5 billion
    its.append(mcq_n("A music video has been watched <b>1.5 billion</b> times. Which number is 1.5 billion?",
                     1500000000, [1500000, 15000000000, 1050000000],
                     "1.5 billion = 1 billion and 5 tenths of a billion. 5 tenths of a billion is 500 million. "
                     "1 000 000 000 + 500 000 000 = 1 500 000 000."))
    # 11 standard -> millions
    its.append(mcq("Write 4 300 000 as a number of millions.", "4.3 million",
                   ["43 million", "0.43 million", "4.03 million"],
                   "4 300 000 = 4 000 000 + 300 000. 300 000 is 3 tenths of a million (1 000 000 ÷ 10 = 100 000). "
                   "So 4 300 000 = 4.3 million."))
    # 12 billions words -> digits
    its.append(mcq_n("Which number is <b>two billion forty million</b>?", 2040000000,
                     [2400000000, 2000040000, 240000000],
                     "Two billion → 2. Forty million → 040 (write the 0 to fill the hundred millions place). "
                     "No thousands and no ones → 000 | 000. So 2 | 040 | 000 | 000 = 2 040 000 000."))
    # 13 three billion
    its.append(mcq_n("Which number is <b>three billion</b>?", 3000000000, [3000000, 300000000, 30000000000],
                     "A billion has 9 zeros. 3 billion = 3 000 000 000 (10 digits). 3 000 000 is 3 million: "
                     "a million is 1000 times smaller than a billion."))
    # 14 twelve million five thousand
    its.append(mcq_n("Which number is <b>twelve million five thousand</b>?", 12005000,
                     [12500000, 12050000, 12000005],
                     "Twelve million → 12. Five thousand → 005 in the thousands group. No ones → 000. "
                     "So 12 | 005 | 000 = 12 005 000."))
    # 15 billions digits -> words
    x = 4050300000
    its.append(mcq("How do you read 4 050 300 000?", words(x),
                   [words(4500300000), words(4050300), words(4050003000)],
                   "Groups: 4 | 050 | 300 | 000. That is 4 billion, 50 million and 300 thousand: "
                   "four billion fifty million three hundred thousand."))
    # 16 number -> expanded (BC)
    its.append(mcq("Which shows 5 000 879 in expanded form?", "5 000 000 + 800 + 70 + 9",
                   ["5 000 000 + 8000 + 700 + 90", "5 000 000 + 879 000", "500 000 + 800 + 70 + 9"],
                   "5 000 879 has 5 millions, 0 hundred thousands, 0 ten thousands, 0 thousands, 8 hundreds, 7 tens "
                   "and 9 ones: 5 000 000 + 800 + 70 + 9."))
    assert 5000000 + 800 + 70 + 9 == 5000879
    # 17 value of a digit in the Canada number
    its.append(mcq_n("In 36 991 981 (Canada’s population in 2021), what is the value of the digit 3?", 30000000,
                     [3000000, 300000000, 30000],
                     "36 | 991 | 981: the 3 is in the ten millions place, so it is worth 3 ten millions = 30 000 000."))
    # 18 one billion in words
    its.append(mcq("How do you read 1 000 000 000?", "one billion",
                   ["one million", "one hundred million", "ten billion"],
                   "1 000 000 000 has four groups: 1 | 000 | 000 | 000. The fourth group from the right is billions, "
                   "so it is one billion."))
    # 19 Port Coquitlam
    x = 61498
    its.append(mcq_n("Terry Fox grew up in Port Coquitlam, BC. At the 2021 census, Port Coquitlam had "
                     "<b>sixty-one thousand four hundred ninety-eight</b> people. Which number is this?", x,
                     [6149800, 614098, 6198],
                     "Sixty-one thousand → 61. Four hundred ninety-eight → 498. So 61 | 498 = 61 498."))
    order = [1, 2, 0, 3, 4, 19, 13, 18, 8, 9, 14, 12, 15, 5, 6, 17, 16, 7, 10, 11]
    return {"title": "Read and write large numbers", "items": reorder(its, order)}


# ============================================================ set 3: decimals to thousandths
def set_decimals():
    its = []
    its.append(mcq(fig(dchart_svg("5.208", hi=-3)) + "What is the value of the red digit in 5.208?",
                   "8 thousandths", ["8 hundredths", "8 tenths", "8 ones"],
                   "The red 8 is the <b>third</b> digit after the decimal point, in the thousandths place. "
                   "Its value is 8 thousandths = 0.008. The 0 holds the hundredths place."))
    its.append(mcq(fig(dchart_svg("7.063", hi=-2)) + "What is the value of the red digit in 7.063?",
                   "6 hundredths", ["6 tenths", "6 thousandths", "6 ones"],
                   "The red 6 is the <b>second</b> digit after the decimal point, in the hundredths place. "
                   "Its value is 6 hundredths = 0.06."))
    its.append(mcq(fig(dchart_svg("24.719", hi=-1)) + "What is the value of the red digit in 24.719?",
                   "7 tenths", ["7 hundredths", "7 ones", "7 tens"],
                   "The red 7 is the <b>first</b> digit after the decimal point, in the tenths place. "
                   "Its value is 7 tenths = 0.7."))
    its.append(mcq("What is the value of the digit 4 in 9.142?", "0.04", ["0.4", "0.004", "4"],
                   "9 . 1 <b>4</b> 2: the 4 is the second digit after the decimal point, in the hundredths place. "
                   "It is worth 4 hundredths = 0.04."))
    its.append(mcq("In which place is the digit 9 in 0.059?", "thousandths", ["hundredths", "tenths", "ones"],
                   "0 . 0 5 <b>9</b>: tenths, hundredths, thousandths. The 9 is in the thousandths place."))
    its.append(mcq("In 6.381, which digit is in the hundredths place?", "8", ["3", "1", "6"],
                   "After the decimal point the places are tenths (3), hundredths (8) and thousandths (1). "
                   "So the hundredths digit is 8."))
    its.append(mcq("In 32.604, which digit is in the thousandths place?", "4", ["0", "6", "2"],
                   "After the decimal point: tenths 6, hundredths 0, thousandths 4. The thousandths digit is 4."))
    its.append(mcq("How many thousandths are there in 0.6?", "600", ["6", "60", "6000"],
                   "1 tenth = 100 thousandths, so 6 tenths = 600 thousandths. 0.6 = 0.600."))
    its.append(mcq("Write 7 ones, 3 hundredths and 2 thousandths as a decimal.", "7.032", ["7.32", "7.302", "7.0032"],
                   "There are 0 tenths, so write a 0 in the tenths place: 7 . 0 3 2 = 7.032. "
                   "7.32 would have 3 tenths."))
    assert D("2") + D("0.6") + D("0.05") + D("0.009") == D("2.659")
    its.append(mcq("2 + 0.6 + 0.05 + 0.009 = ?", "2.659", ["2.956", "26.59", "2.0659"],
                   "2 ones, 6 tenths, 5 hundredths and 9 thousandths: 2 . 6 5 9 = 2.659."))
    assert D("8") + D("0.2") + D("0.04") + D("0.007") == D("8.247")
    its.append(mcq("Which shows 8.247 in expanded form?", "8 + 0.2 + 0.04 + 0.007",
                   ["8 + 0.2 + 0.4 + 0.07", "8 + 2 + 4 + 7", "8 + 0.02 + 0.004 + 0.7"],
                   "8 ones, 2 tenths, 4 hundredths and 7 thousandths: 8 + 0.2 + 0.04 + 0.007."))
    its.append(mcq("Which number is equal to 0.3?", "0.300", ["0.03", "0.003", "3.00"],
                   "A 0 at the <b>end</b> of a decimal does not change its value: 0.3 = 0.30 = 0.300. "
                   "0.03 and 0.003 have the 3 in a different place."))
    assert F(D("0.087")) == F(87, 1000)
    its.append(mcq("Write 0.087 as a fraction.", fr(87, 1000), [fr(87, 100), fr(87, 10), fr(7, 1000)],
                   "0.087 has <b>three</b> decimal places, so it is thousandths: 87 thousandths = %s. "
                   "%s would be 0.87." % (fr(87, 1000), fr(87, 100))))
    its.append(mcq("Which number is <b>six and thirty-four thousandths</b>?", "6.034", ["6.34", "6.304", "6.0034"],
                   "“And” stands for the decimal point. Thirty-four thousandths must end in the <b>third</b> place "
                   "after the point: 6.034. 6.34 would be thirty-four hundredths."))
    its.append(mcq("How do you read 0.508 in words?", dec_words("0.508"),
                   ["five hundred eight hundredths", "fifty-eight thousandths", "five and eight thousandths"],
                   "0.508 has three decimal places, so read the digits as a whole number and say “thousandths”: "
                   "five hundred eight thousandths."))
    its.append(mcq("In 4.44, the 4 in the tenths place is worth how many times the 4 in the hundredths place?",
                   "10", ["100", "1000", "4"],
                   "Each place is worth 10 times the place to its right. 0.4 = 10 × 0.04. So the answer is 10."))
    assert D("2.709") + D("0.001") == D("2.71")
    its.append(mcq("What number is 0.001 more than 2.709?", "2.71", ["2.719", "2.7010", "2.809"],
                   "9 thousandths + 1 thousandth = 10 thousandths = 1 hundredth. So 2.709 + 0.001 = 2.710 = 2.71. "
                   "2.719 adds 1 hundredth, not 1 thousandth."))
    assert D("3.395") + D("0.01") == D("3.405")
    its.append(mcq("What number is 0.01 more than 3.395?", "3.405", ["3.396", "3.495", "3.3105"],
                   "Add 1 hundredth: 9 hundredths + 1 hundredth = 10 hundredths = 1 tenth. "
                   "So 3.395 + 0.01 = 3.405. 3.396 adds only 1 thousandth."))
    assert D("6.07") - D("0.1") == D("5.97")
    its.append(mcq("What number is 0.1 less than 6.07?", "5.97", ["6.06", "6.17", "5.07"],
                   "Take away 1 tenth. 6.07 has 0 tenths, so regroup 1 one as 10 tenths: 6.07 − 0.1 = 5.97. "
                   "6.06 takes away 1 hundredth."))
    its.append(mcq("Use each of the digits 3, 8, 1 and 6 once to make the <b>greatest</b> number with "
                   "1 digit before the decimal point and 3 digits after it.", "8.631", ["8.613", "1.368", "6.831"],
                   "Put the largest digit in the ones place, then the next largest in the tenths, hundredths and "
                   "thousandths places: 8.631. 1.368 is the least number you can make."))
    its = reorder(its, [0, 1, 2, 3, 4, 5, 6, 11, 8, 9, 10, 7, 12, 13, 14, 15, 16, 17, 18, 19])
    return {"title": "Decimals to thousandths", "items": its}


# ============================================================ set 4: compare and order
def first_diff(a, b):
    for i in range(11, -1, -1):
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


def cmp_whole(x, y, extra=""):
    lt, gt = "&lt;", "&gt;"
    right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
    wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
             "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
    return mcq("Which is true?", right, wrong, compare_expl(max(x, y), min(x, y)) + extra)


def cmp_item(x, y, e):
    a, b = Dm(x), Dm(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare <b>%s</b> and <b>%s</b>." % (x, y), right, wrong, e)


def order_q(q, nums, asc, wrongs, e):
    right = ", ".join(sorted(nums, key=lambda s: Dm(s.replace(NB, "").replace(" ", "")), reverse=not asc))
    ws = [", ".join(w) for w in wrongs]
    assert right not in ws and len(set(ws)) == 3
    for w in wrongs:
        assert sorted(w) == sorted(nums)
    assert right in e, (right, e)
    return mcq(q, right, ws, e)


def set_compare():
    its = []
    # whole numbers (8)
    its.append(cmp_whole(980000000, 2040000000, " A big first digit does not matter when a number has fewer digits."))
    its.append(cmp_whole(36991981, 36919981))
    its.append(mcq("Which is greater: 2 billion or 900 million?", "2 billion &gt; 900 million",
                   ["2 billion &lt; 900 million", "2 billion = 900 million", "You can’t tell"],
                   "2 billion = 2 000 000 000 (10 digits). 900 million = 900 000 000 (9 digits). "
                   "A billion is 1000 millions, so 2 billion is much greater, even though 900 &gt; 2."))
    nums = [987654321, 1002000000, 1020000000, 1000200000]
    its.append(mcq("Which number is the <b>greatest</b>?", n(1020000000), [n(v) for v in nums if v != 1020000000],
                   "987 654 321 has only 9 digits, so it is the least, even though it starts with 9. "
                   "The other three have 10 digits and the same billions digit. Compare the hundred millions: all 0. "
                   "Compare the ten millions: 1 020 000 000 has 2, the others have 0. So 1 020 000 000 is the greatest."))
    nums = [5000879, 5008790, 5000978, 5080790]
    its.append(mcq("Which number is the <b>least</b>?", n(5000879), [n(v) for v in nums if v != 5000879],
                   "All have 7 digits. Millions, hundred thousands and ten thousands are the same in "
                   "5 000 879 and 5 000 978, and both have 0 thousands. Compare the hundreds: 8 &lt; 9. "
                   "5 008 790 and 5 080 790 have more thousands. So 5 000 879 is the least."))
    vals = {"Vancouver": 662248, "Surrey": 568322, "Burnaby": 249125}
    o = sorted(vals.values())
    fmt = lambda l: ", ".join(n(v) for v in l)
    its.append(order_q("At the 2021 census, Vancouver had 662 248 people, Surrey had 568 322 and Burnaby had 249 125. "
                       "Order the populations from <b>least to greatest</b>.",
                       [n(v) for v in vals.values()], True,
                       [[n(662248), n(568322), n(249125)], [n(568322), n(249125), n(662248)],
                        [n(249125), n(662248), n(568322)]],
                       "All three have 6 digits. Compare the hundred thousands: 2 &lt; 5 &lt; 6. "
                       "So the order is " + fmt(o) + "."))
    its.append(mcq_n(fig(big_line_svg(0, 1000000000, 100000000, [0, 500000000, 1000000000], arrow=600000000))
                     + "What number does the arrow point to?", 600000000, [60000000, 400000000, 700000000],
                     "From 0 to 1 000 000 000 there are 10 equal spaces, so each space is 100 000 000 (one hundred "
                     "million), not 10 000 000. The arrow is 1 space after 500 000 000: 600 000 000."))
    for b in range(10):
        assert (int("4%d3000000" % b) > 457000000) == (b >= 6)
    its.append(mcq("4☐3" + NB + "000" + NB + "000 &gt; 457" + NB + "000" + NB + "000. Which digit could go in the box?",
                   "6", ["5", "4", "3"],
                   "The hundred millions are the same (4). Compare the ten millions: the box must be 5 or more. "
                   "If it is 5, compare the millions: 3 &lt; 7, so 453 000 000 is too small. 463 000 000 &gt; 457 000 000."))
    # decimals (12)
    its.append(cmp_item("0.45", "0.5", "0.5 = 0.50. Compare the tenths: 4 tenths &lt; 5 tenths. So 0.45 &lt; 0.5. "
                        "More digits does not mean a greater number."))
    its.append(cmp_item("0.7", "0.69", "0.7 = 0.70. Compare the tenths: 7 &gt; 6. So 0.7 &gt; 0.69."))
    its.append(cmp_item("5.06", "5.060", "A 0 at the end does not change the value. 5.06 = 5.060."))
    its.append(cmp_item("0.004", "0.04", "0.04 = 0.040. Compare the hundredths: 0 &lt; 4. So 0.004 &lt; 0.04. "
                        "4 thousandths is less than 4 hundredths."))
    its.append(cmp_item("0.215", "0.22", "Write both with 3 places: 0.215 and 0.220. The tenths are the same. "
                        "Compare the hundredths: 1 &lt; 2. So 0.215 &lt; 0.22. Do not compare 215 with 22."))
    its.append(cmp_item("3.9", "3.899", "3.9 = 3.900. The ones are the same. Compare the tenths: 9 &gt; 8. "
                        "So 3.9 &gt; 3.899."))
    its.append(mcq("Which number is the <b>greatest</b>?", "0.8", ["0.79", "0.799", "0.087"],
                   "Write them with 3 places: 0.800, 0.790, 0.799, 0.087. Compare the tenths first: only 0.8 has "
                   "8 tenths. So 0.8 is the greatest."))
    its.append(mcq("Which number is the <b>least</b>?", "0.506", ["0.56", "0.6", "0.65"],
                   "Write them with 3 places: 0.506, 0.560, 0.600, 0.650. The least is 0.506, "
                   "even though it has the most digits."))
    its.append(order_q("Order from <b>least to greatest</b>: 0.5, 0.45, 0.405", ["0.5", "0.45", "0.405"], True,
                       [["0.5", "0.45", "0.405"], ["0.45", "0.405", "0.5"], ["0.405", "0.5", "0.45"]],
                       "Write them with 3 places: 0.500, 0.450, 0.405. Compare 500, 450 and 405 thousandths. "
                       "So 0.405, 0.45, 0.5."))
    its.append(order_q("Order from <b>greatest to least</b>: 6.4, 6.38, 6.405, 6.04", ["6.4", "6.38", "6.405", "6.04"],
                       False, [["6.405", "6.38", "6.4", "6.04"], ["6.04", "6.38", "6.4", "6.405"],
                               ["6.4", "6.405", "6.38", "6.04"]],
                       "Write them with 3 places: 6.400, 6.380, 6.405, 6.040. Greatest first: 6.405, 6.4, 6.38, 6.04."))
    its.append(mcq(fig(dline_svg(2300, 2310, 10, [2300, 2305, 2310], 2306)) + "What number is at the red dot?",
                   "2.306", ["2.36", "2.307", "2.316"],
                   "From 2.3 to 2.31 there are 10 equal spaces. 2.31 − 2.30 = 0.01, so each space is 1 thousandth, "
                   "not 1 hundredth. Count 6 spaces on from 2.300: 2.306."))
    assert D("0.4") < D("0.409") < D("0.5")
    its.append(mcq("Which number is between 0.4 and 0.5?", "0.409", ["0.049", "0.51", "0.399"],
                   "0.4 = 0.400 and 0.5 = 0.500. 0.409 is between them. 0.049 and 0.399 are less than 0.4, "
                   "and 0.51 is more than 0.5."))
    its = reorder(its, [0, 2, 8, 9, 1, 10, 11, 3, 4, 12, 13, 14, 15, 5, 16, 17, 6, 18, 7, 19])
    return {"title": "Compare and order large numbers and decimals", "items": its}


# ============================================================ set 5: rounding in context
def rint(x, p):
    return ((x + p // 2) // p) * p


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


DPL = {0: "ones", 1: "tenths", 2: "hundredths", 3: "thousandths"}


def rdec_e(x, places):
    q = Dm(1).scaleb(-places)
    lo = Dm(x).quantize(q, rounding="ROUND_FLOOR")
    hi = lo + q
    r = Dm(rd(x, places))
    nxt = int(x.partition(".")[2][places])
    return ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s to %s."
            % (x, lo, hi, DPL[places + 1], nxt, "5 or more" if nxt >= 5 else "4 or less",
               "up" if r > lo else "down", r))


def set_round():
    its = []
    # 0 Vancouver nearest thousand
    x = 662248
    assert rint(x, 1000) == 662000
    its.append(mcq_n("At the 2021 census, the city of Vancouver had 662 248 people. "
                     "What is this rounded to the nearest thousand?", 662000, [663000, 660000, 662200],
                     rint_e(x, 1000) + " Answer: 662 000 people.", " people"))
    # 1 Surrey nearest ten thousand
    x = 568322
    assert rint(x, 10000) == 570000
    its.append(mcq_n("At the 2021 census, Surrey had 568 322 people. "
                     "What is this rounded to the nearest ten thousand?", 570000, [560000, 568000, 600000],
                     rint_e(x, 10000) + " Answer: 570 000 people.", " people"))
    # 2 BC nearest hundred thousand
    x = 5000879
    assert rint(x, 100000) == 5000000
    its.append(mcq_n("At the 2021 census, British Columbia had 5 000 879 people. "
                     "What is this rounded to the nearest hundred thousand?", 5000000, [5100000, 5001000, 5000900],
                     rint_e(x, 100000) + " Answer: 5 000 000 people.", " people"))
    # 3 Canada nearest million (9 regroup)
    x = 36991981
    assert rint(x, 1000000) == 37000000
    its.append(mcq_n("At the 2021 census, Canada had 36 991 981 people. "
                     "What is this rounded to the nearest million?", 37000000, [36000000, 36990000, 40000000],
                     rint_e(x, 1000000) + " Answer: 37 000 000 people (37 million).", " people"))
    # 4 Metro Vancouver
    x = 2642825
    assert rint(x, 100000) == 2600000
    its.append(mcq_n("At the 2021 census, Metro Vancouver had 2 642 825 people. "
                     "What is this rounded to the nearest hundred thousand?", 2600000, [2700000, 2640000, 3000000],
                     rint_e(x, 100000) + " Keep the 6 in the hundred thousands place and write zeros after it. "
                     "Answer: 2 600 000 people.", " people"))
    # 5 Kelowna nearest thousand
    x = 144576
    assert rint(x, 1000) == 145000
    its.append(mcq_n("At the 2021 census, Kelowna had 144 576 people. "
                     "What is this rounded to the nearest thousand?", 145000, [144000, 140000, 144600],
                     rint_e(x, 1000) + " Answer: 145 000 people.", " people"))
    # 6 Sun distance nearest million (9 regroup)
    x = 149597871
    assert rint(x, 1000000) == 150000000
    its.append(mcq_n("On average, Earth is 149 597 871 km from the Sun. What is this distance rounded to the nearest "
                     "million kilometres?", 150000000, [149000000, 149600000, 100000000],
                     rint_e(x, 1000000) + " Answer: 150 000 000 km (150 million km).", " km"))
    # 7 Nanaimo nearest thousand (regroup)
    x = 99863
    assert rint(x, 1000) == 100000
    its.append(mcq_n("At the 2021 census, Nanaimo had 99 863 people. "
                     "What is this rounded to the nearest thousand?", 100000, [99000, 99900, 90000],
                     rint_e(x, 1000) + " 99 thousands + 1 thousand = 100 thousands. Answer: 100 000 people.",
                     " people"))
    # 8 Burnaby reverse
    for w, r in [(249125, 250000), (255000, 260000), (244800, 240000), (258300, 260000)]:
        assert rint(w, 10000) == r
    its.append(mcq("A news report says that about 250 000 people lived in Burnaby in 2021. The number was "
                   "rounded to the nearest ten thousand. Which could be the real population?",
                   n(249125), [n(255000), n(244800), n(258300)],
                   "Numbers from 245 000 to 254 999 round to 250 000. 249 125 is in that range. 255 000 and 258 300 "
                   "round up to 260 000, and 244 800 rounds down to 240 000."))
    # 9 salmon nearest tenth
    assert rd("4.68", 1) == "4.7"
    its.append(mcq("A coho salmon caught on the Fraser River has a mass of 4.68 kg. What is its mass to the nearest "
                   "tenth of a kilogram?", "4.7 kg", ["4.6 kg", "5 kg", "4.8 kg"],
                   rdec_e("4.68", 1) + " 4.6 kg just cuts off the 8. Answer: 4.7 kg."))
    # 10 Terry Fox Run nearest whole
    assert rd("5.38", 0) == "5"
    its.append(mcq("Arjun ran 5.38 km in the Terry Fox Run. What is this distance to the nearest whole kilometre?",
                   "5 km", ["6 km", "5.4 km", "5.3 km"],
                   "5.38 is between 5 and 6. Look at the tenths digit: 3. 4 or less, so round down to 5. "
                   "5.4 km is the nearest tenth, not the nearest whole number. Answer: 5 km."))
    # 11 gas price nearest cent
    assert rd("1.879", 2) == "1.88"
    its.append(mcq("Gas in Kamloops costs $1.879 per litre. What is this price to the nearest cent (hundredth of a "
                   "dollar)?", "$1.88", ["$1.87", "$1.90", "$1.80"],
                   rdec_e("1.879", 2) + " A cent is a hundredth of a dollar, so keep two decimal places. Answer: $1.88."))
    # 12 rain 9 regroup
    assert rd("12.95", 1) == "13.0"
    its.append(mcq("On a rainy day in Vancouver, 12.95 mm of rain fell. What is this to the nearest tenth of a "
                   "millimetre?", "13.0 mm", ["12.9 mm", "12.10 mm", "12.0 mm"],
                   "12.95 is between 12.9 and 13.0. Look at the hundredths digit: 5. 5 or more, so round up. "
                   "9 tenths + 1 tenth = 10 tenths = 1 one, so 12.9 becomes 13.0. Do not write 12.10. Answer: 13.0 mm."))
    # 13 cherries 9 regroup hundredths
    assert rd("2.496", 2) == "2.50"
    its.append(mcq("A box of Okanagan cherries has a mass of 2.496 kg. What is this to the nearest hundredth of a "
                   "kilogram?", "2.50 kg", ["2.49 kg", "2.410 kg", "2.40 kg"],
                   "2.496 is between 2.49 and 2.50. Look at the thousandths digit: 6. 5 or more, so round up. "
                   "9 hundredths + 1 hundredth = 10 hundredths = 1 tenth, so 2.49 becomes 2.50. Answer: 2.50 kg."))
    # 14 long jump halfway
    assert rd("3.475", 2) == "3.48"
    its.append(mcq("Simran jumped 3.475 m in the long jump at a track meet in Burnaby. What is this to the nearest "
                   "hundredth of a metre?", "3.48 m", ["3.47 m", "3.5 m", "3.4 m"],
                   "3.475 is exactly halfway between 3.47 and 3.48. A number that is exactly halfway rounds up. "
                   "Answer: 3.48 m."))
    # 15 which swim time does NOT round to 36.5
    ts = ["36.44", "36.48", "36.53", "36.46"]
    assert [rd(t, 1) for t in ts] == ["36.4", "36.5", "36.5", "36.5"]
    its.append(mcq("Four swimmers raced 50 m at a swim meet in Victoria. Which time does <b>not</b> round to 36.5 s "
                   "to the nearest tenth?", "36.44 s", ["36.48 s", "36.53 s", "36.46 s"],
                   "Times from 36.45 s up to (but not including) 36.55 s round to 36.5 s. 36.44 has 4 hundredths, "
                   "so it rounds down to 36.4 s."))
    # 16 snowboard time rounds to 52.3
    ts = ["52.26", "52.36", "52.21", "52.35"]
    assert [rd(t, 1) for t in ts] == ["52.3", "52.4", "52.2", "52.4"]
    its.append(mcq("Chloe’s snowboard race time at Whistler, rounded to the nearest tenth, is 52.3 seconds. "
                   "Which could be her real time?", "52.26 s", ["52.36 s", "52.21 s", "52.35 s"],
                   "Times from 52.25 s to 52.34 s round to 52.3 s. 52.26 s is in that range. 52.36 s and 52.35 s "
                   "round up to 52.4 s, and 52.21 s rounds down to 52.2 s."))
    # 17 least that rounds, large
    assert rint(1450000, 100000) == 1500000 and rint(1449999, 100000) == 1400000 and rint(1549999, 100000) == 1500000
    its.append(mcq("The number of people who rode a ferry route in one year, rounded to the nearest hundred thousand, "
                   "is 1 500 000. What is the <b>least</b> the real number could be?", n(1450000),
                   [n(1400000), n(1499999), n(1549999)],
                   "Numbers from 1 450 000 to 1 549 999 round to 1 500 000. 1 449 999 would round down to 1 400 000, "
                   "so the least is 1 450 000. (1 549 999 is the greatest.)"))
    # 18 least race time that rounds to 12.7
    assert rd("12.65", 1) == "12.7" and rd("12.64", 1) == "12.6" and rd("12.74", 1) == "12.7"
    its.append(mcq("Owen’s 100 m time, rounded to the nearest tenth, is 12.7 s. The real time was measured to the "
                   "hundredth. What is the <b>least</b> it could be?", "12.65 s", ["12.60 s", "12.70 s", "12.74 s"],
                   "Times from 12.65 s to 12.74 s round to 12.7 s. 12.64 s would round down to 12.6 s, "
                   "so the least is 12.65 s. (12.74 s is the greatest.)"))
    # 19 rounding twice, decimals
    assert rd("48.346", 1) == "48.3" and rd(rd("48.346", 2), 1) == "48.4"
    its.append(mcq("Kai’s ski race time on Grouse Mountain was 48.346 s. He rounded it to the nearest hundredth "
                   "(48.35 s), then rounded that to the nearest tenth and got 48.4 s. What is 48.346 s rounded to the "
                   "nearest tenth?", "48.3 s", ["48.4 s", "48.35 s", "48 s"],
                   "Always round the number you started with. 48.346 is between 48.3 and 48.4. Look at the "
                   "hundredths digit: 4. 4 or less, so round down to 48.3 s. Rounding twice gives the wrong answer."))
    its = reorder(its, [9, 0, 10, 1, 5, 11, 2, 7, 12, 3, 13, 6, 4, 14, 8, 15, 16, 17, 18, 19])
    return {"title": "Rounding in real life", "items": its}


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
        "<h2>Place value to billions</h2>"
        "<p>Each place is worth <b>10 times</b> the place to its right. Big numbers are split into groups of three "
        "digits called periods: <b>billions</b>, <b>millions</b>, <b>thousands</b> and <b>ones</b>. "
        "In Canada we leave a small space between the groups (5 000 879), not a comma. "
        "A 4-digit number has no space (4536).</p>"
        "<figure class='sn-fig'>" + chart_svg(3040500207, hi=9) +
        "<figcaption>3 040 500 207: the 3 is in the billions place, so it is worth 3 000 000 000. "
        "The zeros hold the empty places.</figcaption></figure>"
        + table(["Name", "Digits", "Zeros"], [
            ["one thousand", "1000", "3"],
            ["one million = 1000 thousands", "1 000 000", "6"],
            ["one billion = 1000 millions", "1 000 000 000", "9"],
        ])
        + "<h2>Read and write large numbers</h2>"
        "<p>Read one group at a time, from the left, and say the group’s name. Write every group with "
        "<b>three digits</b>, using 0 for empty places.</p>"
        + ex("Words to digits", "At the 2021 census, British Columbia had five million eight hundred seventy-nine "
             "people. Write the number in digits.",
             "Five million → 5. No thousands → 000. Eight hundred seventy-nine → 879.", "5 000 879")
        + ex("Millions with a decimal", "Write 2.6 million in digits.",
             "0.1 million = 100 000, so 0.6 million = 600 000. 2 000 000 + 600 000.", "2 600 000")
        + "<h2>Decimals to thousandths</h2>"
        "<p>After the decimal point come <b>tenths</b>, <b>hundredths</b> and <b>thousandths</b>. "
        "1 hundredth split into 10 equal parts makes 10 thousandths. Read the word “and” as the decimal point.</p>"
        "<figure class='sn-fig'>" + dchart_svg("5.208", hi=-3) +
        "<figcaption>5.208 is “five and two hundred eight thousandths”. The 8 is worth 8 thousandths = 0.008.</figcaption></figure>"
        "<h2>Compare and order</h2>"
        "<p><b>Whole numbers:</b> count the digits first. A 10-digit number is greater than any 9-digit number. "
        "If they have the same number of digits, compare place by place from the left.</p>"
        "<p><b>Decimals:</b> compare the whole numbers first. Then give the decimals the same number of places by "
        "adding zeros at the end, and compare tenths, hundredths, thousandths.</p>"
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
            ["36 991 981 to the nearest million", "the hundred thousands digit: 9", "37 000 000"],
            ["2 642 825 to the nearest hundred thousand", "the ten thousands digit: 4", "2 600 000"],
            ["4.68 to the nearest tenth", "the hundredths digit: 8", "4.7"],
            ["1.879 to the nearest hundredth", "the thousandths digit: 9", "1.88"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up millions and billions (8 billion → 8 000 000)",
             "A billion is 1000 millions: 8 billion = 8 000 000 000"],
            ["0.45 &gt; 0.5 because it has more digits", "Use the same number of places: 0.45 &lt; 0.50"],
            ["Missing a zero group (five million eight hundred seventy-nine → 5879)",
             "Write each group as three digits: 5 | 000 | 879"],
            ["Giving the digit, not its value (the 3 in 36 991 981 is 3)", "It is in the ten millions place: 30 000 000"],
            ["Cutting off instead of rounding (4.68 → 4.6)", "Look at the next digit: 8, so round up to 4.7"],
            ["Rounding twice (48.346 → 48.35 → 48.4)", "Round the number you started with: 48.3"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about numbers in the BC math curriculum?",
     "a": "The Grade 6 Number standard is “small to large numbers (thousandths to billions)”. Students read, write, "
          "compare, order and round whole numbers up to billions and decimals to thousandths."},
    {"q": "How many millions are in a billion?",
     "a": "There are 1000 millions in one billion. One million is 1 000 000 (6 zeros) and one billion is "
          "1 000 000 000 (9 zeros)."},
    {"q": "Which is bigger, 0.45 or 0.5?",
     "a": "0.5 is bigger. Write both with the same number of places, 0.45 and 0.50, and compare the tenths: "
          "5 tenths is more than 4 tenths."},
    {"q": "Why do BC students write 5 000 879 with spaces instead of commas?",
     "a": "Canada uses the SI style in math: numbers with 5 or more digits are split into groups of three with a "
          "small space, and 4-digit numbers have no space (4536). This avoids mix-ups with the decimal comma used in French."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (5 000 879) everywhere outside SVG markup."""
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
    rnd = random.Random(56801)
    used = set()
    sets = [set_whole(rnd, used), set_read(), set_decimals(), set_compare(), set_round()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "thousandths-to-billions", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Place Value: Thousandths to Billions",
        "seo_title": "Grade 6 Place Value Worksheets: Thousandths to Billions, Free Math with Answer Key (BC Curriculum)",
        "short_title": "Thousandths to Billions",
        "domain": "Number",
        "standard_code": "Grade 6: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Small to large numbers (thousandths to billions)",
        "meta_desc": "Free Grade 6 math worksheets on place value from thousandths to billions for the BC curriculum: "
                     "millions and billions, reading and writing BC and Canada populations, decimals to thousandths, "
                     "comparing and ordering, and rounding in real life. 100 questions with an answer key.",
        "key_big": "Every place is worth 10 times the place to its right, from thousandths all the way up to billions.",
        "key_sub": "A billion is 1000 millions (1 000 000 000). Compare decimals place by place, not by length: "
                   "0.5 = 0.50 > 0.45. To round, look one place to the right: 5 or more rounds up.",
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
