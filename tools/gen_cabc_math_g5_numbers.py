# -*- coding: utf-8 -*-
"""
British Columbia Grade 5 Math: Numbers to 1 000 000
(BC Mathematics Curriculum, Grade 5 Content: Number concepts to 1 000 000)
  python3 tools/gen_cabc_math_g5_numbers.py
Read, write and represent whole numbers to 1 000 000, find the value of each digit, write expanded form and
decompose numbers, compare and order them, use number lines and rounding, and work with real BC numbers
(city populations from the 2021 Census, salmon counts, crowds, fundraising).
Numbers: 4-digit numbers have no separator (4503); 5 or more digits use a no-break space (405 030). Never commas.
Wrong answers come from real mistakes: leaving out a zero (forty thousand five hundred three -> 4503),
giving the digit instead of its value (the 7 in 471 250 is 7), counting place value disks instead of
adding their values, reading a number line as if every space were 1000, comparing by the first digit only,
writing 14 ten thousands inside the number, rounding the wrong place, cutting off instead of rounding,
and rounding twice.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]


# ------------------------------------------------------------ helpers
def n(x):
    """BC/SI style: 4503, 10 000, 405 030 (no-break spaces, never commas)."""
    s = str(x)
    if len(s) <= 4:
        return s
    g = []
    while s:
        g.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(g)


NUM = re.compile(r"^(\$)?(\d+)( .+)?$")


def val(c):
    """Value of a choice that is a single number (None otherwise)."""
    c = re.sub(r"(?<=\d)" + NB + r"(?=\d)", "", c)
    m = NUM.match(c)
    if not m:
        return None
    return (F(m.group(2)), "$" if m.group(1) else (m.group(3) or "").strip())


def xval(s):
    """Value of an expanded-form choice such as '400 000 + 500 + 3' or '9 × 100 000 + 5 × 1'."""
    s = s.replace(NB, "").replace(" ", "")
    tot = 0
    for term in s.split("+"):
        p = 1
        for f in term.split("×"):
            p *= int(f)
        tot += p
    return tot


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


def mcq_n(q, correct, wrong, e, pre=""):
    assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3, (q, correct, wrong)
    return mcq(q, pre + n(correct), [pre + n(v) for v in wrong], e)


def mcq_x(q, correct, wrong, e, value):
    """Expanded-form choices: the correct one equals value, the wrong ones all have different values."""
    vs = [xval(x) for x in [correct] + wrong]
    assert vs[0] == value and len(set(vs)) == 4, (q, vs)
    return mcq(q, correct, wrong, e)


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


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def digit(x, i):
    return (x // 10 ** i) % 10


def ndig(x):
    return len(str(x))


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def rnd_to(x, p):
    """Round half up to the nearest 10**p."""
    m = 10 ** p
    return (x + m // 2) // m * m


# ------------------------------------------------------------ numbers in words (no "and")
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
    if x == 1000000:
        return "one million"
    assert 0 < x < 1000000
    t, o = divmod(x, 1000)
    parts = []
    if t:
        parts.append(w1000(t) + " thousand")
    if o:
        parts.append(w1000(o))
    return " ".join(parts)


assert words(40503) == "forty thousand five hundred three"
assert words(306040) == "three hundred six thousand forty"
assert words(815400) == "eight hundred fifteen thousand four hundred"


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 64, 28, 28, 48
SUB = ["H", "T", "O", "H", "T", "O"]


def chart_svg(x, hi=None):
    """Thousands (H T O) | Ones (H T O) chart with a number below 1 000 000. hi = place index drawn in red."""
    assert x < 1000000
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


DISK_FILL = {5: "#e8d6f0", 4: "#f2d4cf", 3: "#d6e4f4", 2: "#cfe6d6", 1: "#fbe9c0", 0: "#e4e4e4"}
DR = 34          # disk radius (fits “100 000” at 14px)
DG = 4           # gap between disks
GG = 18          # gap between place groups


def disks_svg(counts):
    """Place value disks. counts = [hundred thousands, ten thousands, thousands, hundreds, tens, ones].
    Each place with disks is a group of up to 2 columns x 3 rows."""
    assert len(counts) == 6 and all(0 <= c <= 6 for c in counts)
    groups = [(5 - k, c) for k, c in enumerate(counts) if c]
    D = 2 * DR
    M = 6
    W = 2 * M + sum((min(c, 2) * D + (min(c, 2) - 1) * DG) for _, c in groups) + GG * (len(groups) - 1)
    rows = max((c + 1) // 2 for _, c in groups)
    H = 2 * M + rows * D + (rows - 1) * DG
    s = []
    x = M
    for i, c in groups:
        cols = min(c, 2)
        for k in range(c):
            cx = x + (k % cols) * (D + DG) + DR
            cy = M + (k // cols) * (D + DG) + DR
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (cx, cy, DR - 1, DISK_FILL[i], INK))
            s.append(text(cx, cy + 5, n(10 ** i), 14, bold=True))
        x += cols * D + (cols - 1) * DG + GG
    value = sum(c * 10 ** (5 - k) for k, c in enumerate(counts))
    return svg_wrap(W, H, "".join(s), "place value disks showing %s" % n(value))


def line_svg(lo, hi, step, labels, arrow=None, show=None):
    """Number line lo..hi, a tick every step, numbers at `labels`, red arrow at `arrow` (with its value if show)."""
    L, R = 62, 418
    W = 480
    top = 18 if show else 0
    Y = (58 if arrow is not None else 30) + top
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
    for v in labels:
        assert (v - lo) % step == 0 and lo <= v <= hi
    if arrow is not None:
        assert (arrow - lo) % step == 0
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
        if show:
            s.append(text(ax, Y - 46, n(arrow), 15, bold=True, col=RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (n(lo), n(hi)))


# ============================================================ set 1: place value to one million
def disks_e(counts):
    parts = [(c, 10 ** (5 - k)) for k, c in enumerate(counts)]
    value = sum(c * v for c, v in parts)
    used = ["%d × %s = %s" % (c, n(v), n(c * v)) for c, v in parts if c]
    empty = [PL[5 - k] for k, c in enumerate(counts) if c == 0]
    s = "Find the value of each group: %s. Add them: %s." % ("; ".join(used), n(value))
    if empty:
        s += " There are no %s, so write 0 in %s." % (" or ".join(empty), "those places" if len(empty) > 1 else "that place")
    return s


def words_e(x):
    t, o = divmod(x, 1000)
    return ("Say the thousands part first: %s thousand → %d. Then write the rest with three digits: %s → %03d. "
            "So the number is %s." % (w1000(t), t, w1000(o) if o else "nothing", o, n(x)))


def set_read():
    D_ = []
    for counts, wrong in [([3, 4, 0, 2, 0, 0], [34200, 9, 304200]),
                          ([2, 0, 5, 0, 1, 0], [25010, 8, 250010]),
                          ([1, 3, 0, 0, 4, 2], [13042, 10, 134200]),
                          ([4, 0, 0, 6, 0, 3], [463, 13, 40603])]:
        x = sum(c * 10 ** (5 - k) for k, c in enumerate(counts))
        e = disks_e(counts)
        if sum(counts) in wrong:
            e += " Do not just count the disks: each disk has its own value."
        D_.append(mcq_n(fig(disks_svg(counts)) + "What number do the place value disks show?", x, wrong, e))
    P_ = []
    for x, i in [(635274, 5), (428916, 4), (750382, 3)]:
        others = [PL[k] for k in sorted(range(6), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        P_.append(mcq(fig(chart_svg(x, hi=i)) + "Which place is the red digit in?", PL[i], others,
                      "Read the places from the right: ones, tens, hundreds, thousands, ten thousands, "
                      "hundred thousands. In %s the red %d is in the %s place." % (n(x), digit(x, i), PL[i])))
    G_ = []
    for x, i in [(743816, 4), (590264, 3)]:
        d = digit(x, i)
        assert len(set(str(x))) == 6
        cands = [str(digit(x, k)) for k in sorted(range(6), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        e = "In %s: %s. The %s digit is %d." % (
            n(x), ", ".join("%s %d" % (PL[k], digit(x, k)) for k in range(5, -1, -1)), PL[i], d)
        if d == 0:
            e += " The 0 shows there are no %s." % PL[i]
        G_.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    W_ = []
    for x, wrong in [(40503, [4503, 400503, 45003]), (306040, [36040, 306400, 360040]),
                     (520007, [52007, 520070, 527000]), (815400, [81540, 815040, 850400])]:
        e = words_e(x)
        if x == 40503:
            e += " 4503 leaves out the 0 in the thousands place."
        if x == 815400:
            e += " Fifteen is 15, not 50."
        W_.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, wrong, e))
    W_.append(mcq_n("Which number is <b>one million</b>?", 1000000, [100000, 10000000, 10000],
                    "One million is 1000 thousands. Write 1, then two groups of three zeros: 1 000 000. "
                    "It has 7 digits. (100 000 is one hundred thousand.)"))
    R_ = []
    for x, wx in [(604050, [64050, 604500, 640050]), (218070, [218700, 280070, 21870]),
                  (470012, [470120, 47012, 470021])]:
        e = ("Split %s into the thousands part and the rest: %d thousand and %d. Say each part: %s."
             % (n(x), x // 1000, x % 1000, words(x)))
        if x == 218070:
            e += " Eighteen is 18, eighty is 80."
        R_.append(mcq("How do you write %s in words?" % n(x), words(x), [words(v) for v in wx], e))
    C_ = [
        mcq_n("How many hundred thousands make 1" + NB + "000" + NB + "000?", 10, [100, 1000, 1],
              "Count by hundred thousands: 100 000, 200 000 … 1 000 000. That is 10 hundred thousands. "
              "Each place is worth 10 times the place to its right."),
        mcq_n("Ten groups of 100" + NB + "000 make what number?", 1000000, [100000, 10000000, 100010],
              "10 × 100 000 = 1 000 000. Count by hundred thousands: 100 000, 200 000 … 1 000 000. "
              "Ten hundred thousands make one million."),
        mcq_n("What number is 1 more than 999" + NB + "999?", 1000000, [100000, 10000000, 999998],
              "999 999 + 1: every 9 becomes 0 as you regroup, and a 1 goes in the millions place: 1 000 000. "
              "(999 998 is 1 less.)"),
    ]
    assert 10 * 100000 == 1000000 and 999999 + 1 == 1000000
    its = D_[:2] + P_[:2] + G_[:1] + W_[:2] + D_[2:3] + P_[2:] + R_[:1] + W_[2:3] + G_[1:] + C_[:1] \
        + D_[3:] + W_[3:4] + R_[1:2] + C_[1:2] + W_[4:] + R_[2:] + C_[2:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Place value to one million", "items": its}


# ============================================================ set 2: value of a digit
def value_cands(d, i):
    """The digit itself, the value one place up, and one place down (or two up for the tens)."""
    if i == 0:
        return [d * 10, d * 100, d * 1000]
    return [d * 10 ** (i + 1), d, d * 10 ** (i - 1) if i >= 2 else d * 10 ** (i + 2)]


def value_e(d, i, red=False):
    v = d * 10 ** i
    s = "The %s%d is in the %s place, so it is worth %s = %s." % ("red " if red else "", d, PL[i], plural(d, i), n(v))
    if i:
        s += " The digit is %d, but its value is %s." % (d, n(v))
    return s


def set_value():
    A = []
    for x, i in [(528461, 5), (374152, 4), (809627, 2), (641783, 1), (195530, 3)]:
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    B = []
    for x, d in [(471250, 7), (236091, 3), (702846, 8), (915384, 9), (468205, 2)]:
        assert str(x).count(str(d)) == 1
        i = ndig(x) - 1 - str(x).index(str(d))
        B.append(mcq_n("What is the value of the %d in %s?" % (d, n(x)), d * 10 ** i, value_cands(d, i), value_e(d, i)))
    H = []
    for d, i, ans, wrong in [(6, 5, 632054, [362054, 236054, 326540]), (4, 3, 274019, [247019, 270419, 427019]),
                             (0, 4, 508371, [580371, 538071, 853701])]:
        assert digit(ans, i) == d and all(digit(w, i) != d for w in wrong)
        e = "%s has %s." % (n(ans), ", ".join(plural(digit(ans, k), k) for k in range(5, -1, -1)))
        e += " The %s digit is %d." % (PL[i], d)
        H.append(mcq_n("Which number has a %d in the %s place?" % (d, PL[i]), ans, wrong, e))
    T = [
        mcq_n("The 3 in 300" + NB + "000 is worth how many times the 3 in 30" + NB + "000?", 10, [100, 3, 270000],
              "The first 3 is worth 300 000. The second 3 is worth 30 000. 300 000 ÷ 30 000 = 10. "
              "Each place is worth 10 times the place to its right. (270 000 is the difference, not how many times.)"),
        mcq_n("In 550" + NB + "000, the first 5 is worth how many times the second 5?", 10, [100, 5, 450000],
              "The first 5 is in the hundred thousands place: 500 000. The second 5 is in the ten thousands place: "
              "50 000. 500 000 ÷ 50 000 = 10."),
    ]
    assert 300000 // 30000 == 10 and 500000 // 50000 == 10
    Tot = [
        mcq_n("478" + NB + "300 = ☐ thousands and 3 hundreds. What number goes in the box?", 478, [8, 47, 4783],
              "478 300 = 478 000 + 300. 478 000 is 478 thousands. So 478 300 = 478 thousands and 3 hundreds. "
              "(8 is only the thousands digit.)"),
        mcq_n("260" + NB + "000 = ☐ ten thousands. What number goes in the box?", 26, [260, 2600, 6],
              "100 000 = 10 ten thousands, so 260 000 = 20 + 6 = 26 ten thousands. Check: 26 × 10 000 = 260 000."),
    ]
    assert 478 * 1000 + 300 == 478300 and 26 * 10000 == 260000
    Re = [mcq_n("In the 2021 Census, Kelowna had 144" + NB + "576 people. What is the value of the 5?", 500,
                [5, 50, 5000],
                "144 576 is 1 hundred thousand, 4 ten thousands, 4 thousands, 5 hundreds, 7 tens and 6 ones. "
                "The 5 is in the hundreds place, so it is worth 500.")]
    Z = [
        mcq_n("Which number has 0 ten thousands?", 708516, [780516, 875016, 78516],
              "708 516 is 7 hundred thousands, 0 ten thousands, 8 thousands, 5 hundreds, 1 ten and 6 ones. "
              "The other numbers have 8 or 7 ten thousands."),
        mcq("In 903" + NB + "407, which digit is in the tens place?", "0", ["4", "7", "9"],
            "903 407 is 9 hundred thousands, 0 ten thousands, 3 thousands, 4 hundreds, 0 tens and 7 ones. "
            "The tens digit is 0: there are no tens."),
    ]
    assert digit(708516, 4) == 0 and all(digit(w, 4) != 0 for w in [780516, 875016, 78516]) and digit(903407, 1) == 0
    its = A[:2] + B[:2] + Re + A[2:3] + B[2:3] + H[:1] + Z[:1] + A[3:4] + B[3:4] + H[1:2] + Tot[:1] + Z[1:] \
        + A[4:] + B[4:] + H[2:] + Tot[1:] + T
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "The value of each digit", "items": its}


# ============================================================ set 3: expanded form and decomposing
def expd(x):
    return " + ".join(n(digit(x, i) * 10 ** i) for i in range(ndig(x) - 1, -1, -1) if digit(x, i))


def mult_form(x):
    return " + ".join("%d × %s" % (digit(x, i), n(10 ** i)) for i in range(ndig(x) - 1, -1, -1) if digit(x, i))


def phrase(parts):
    """[(count, place index)] -> ('4 hundred thousands, 12 ten thousands and 7 thousands', value)."""
    ws = [plural(c, i) for c, i in parts]
    return ", ".join(ws[:-1]) + " and " + ws[-1], sum(c * 10 ** i for c, i in parts)


def set_expand():
    S = []
    for x, wrong in [(683725, ["6 + 8 + 3 + 7 + 2 + 5", "600 000 + 8000 + 3000 + 700 + 20 + 5",
                               "60 000 + 80 000 + 3000 + 700 + 20 + 5"]),
                     (453000, ["4 + 5 + 3", "400 000 + 50 000 + 300", "400 000 + 5000 + 300"]),
                     (405030, ["40 000 + 5000 + 30", "400 000 + 50 000 + 30", "400 000 + 5000 + 300"]),
                     (720080, ["700 000 + 2000 + 80", "700 000 + 20 000 + 800", "70 000 + 20 000 + 80"]),
                     (930016, ["900 000 + 30 000 + 100 + 6", "90 000 + 30 000 + 10 + 6", "900 000 + 3000 + 10 + 6"])]:
        wrong = [nbsp(w) for w in wrong]
        e = "Write the value of each digit that is not 0: %s. That is %s." % (
            ", ".join("%s %d = %s" % (PL[i], digit(x, i), n(digit(x, i) * 10 ** i))
                      for i in range(5, -1, -1) if digit(x, i)), expd(x))
        if "0" in str(x):
            e += " A 0 adds nothing, so it is left out."
        S.append(mcq_x("What is %s in expanded form?" % n(x), expd(x), wrong, e, x))
    X = []
    for terms, x, wrong in [(["800 000", "600", "4"], 800604, [8604, 860004, 800064]),
                            (["300 000", "70 000", "20"], 370020, [37020, 372000, 307020]),
                            (["500 000", "9"], 500009, [509, 50009, 500090]),
                            (["3000", "200 000", "1", "40 000", "60"], 243061, [321460, 243016, 24361])]:
        ex_ = " + ".join(t.replace(" ", NB) for t in terms)
        assert xval(ex_) == x
        e = ("Put each value in its place and write 0 in every empty place. %s → %s." % (ex_, n(x)))
        if x == 243061:
            e = ("The parts are not in order. Sort them from the greatest place: "
                 "200 000 + 40 000 + 3000 + 60 + 1 = 243 061. Do not write the digits in the order you see them.")
        X.append(mcq_n("What number is <b>%s</b>?" % ex_, x, wrong, e))
    for x, wrong in [(906050, [965, 906500, 960050]), (700029, [729, 70029, 700290])]:
        mf = mult_form(x)
        assert xval(mf) == x
        X.append(mcq_n("What number is <b>%s</b>?" % mf, x, wrong,
                       "Work out each part: %s. Add them: %s. Write 0 in every empty place." % (
                           ", ".join("%d × %s = %s" % (digit(x, i), n(10 ** i), n(digit(x, i) * 10 ** i))
                                     for i in range(5, -1, -1) if digit(x, i)), n(x))))
    B = []
    for q, x, ans, wrong in [("600 000 + ☐ + 7000 + 200 + 5 = 687 205", 687205, 80000, [8, 8000, 800000]),
                             ("☐ + 30 000 + 40 + 2 = 530 042", 530042, 500000, [5, 50000, 5000]),
                             ("700 000 + 4000 + ☐ = 704 009", 704009, 9, [90, 900, 9000]),
                             ("100 000 + 50 000 + ☐ + 6 = 150 086", 150086, 80, [8, 800, 86])]:
        q = re.sub(r"(?<=\d) (?=\d{3})", NB, q)
        lhs = q.split("=")[0].replace("☐", str(ans))
        assert xval(lhs) == x
        i = [k for k in range(6) if digit(x, k) * 10 ** k == ans][0]
        B.append(mcq_n(q + ". What number goes in the box?", ans, wrong,
                       "%s has %s in the %s place. That is worth %s." % (n(x), digit(x, i), PL[i], n(ans))))
    R = []
    R.append(mcq_n("453" + NB + "000 = ☐ thousands. What number goes in the box?", 453, [45, 4530, 3],
                   "453 000 = 453 groups of 1000, so it is 453 thousands. Check: 453 × 1000 = 453 000."))
    assert 453 * 1000 == 453000
    p, v = phrase([(3, 5), (14, 4), (2, 3)])
    assert v == 442000
    R.append(mcq_n("What number is %s?" % p, 442000, [3142000, 342000, 3142],
                   "3 hundred thousands = 300 000 and 14 ten thousands = 140 000. 300 000 + 140 000 + 2000 = 442 000. "
                   "Do not write 14 inside the number: 14 ten thousands is 1 hundred thousand and 4 ten thousands."))
    R.append(mcq_n("260" + NB + "400 = 1 hundred thousand, ☐ ten thousands and 4 hundreds. What number goes in the box?",
                   16, [6, 26, 160],
                   "260 400 = 2 hundred thousands, 6 ten thousands and 4 hundreds. Trade 1 hundred thousand for "
                   "10 ten thousands: 10 + 6 = 16 ten thousands. Check: 100 000 + 160 000 + 400 = 260 400."))
    assert 100000 + 160000 + 400 == 260400
    ok, vo = phrase([(4, 5), (12, 4), (7, 3)])
    ws = [phrase([(4, 5), (2, 4), (7, 3)]), phrase([(5, 5), (12, 4), (7, 3)]), phrase([(4, 5), (12, 4), (70, 3)])]
    assert vo == 527000 and len({vo} | {w[1] for w in ws}) == 4
    R.append(mcq("Which is another way to make 527" + NB + "000?", ok, [w[0] for w in ws],
                 "4 hundred thousands = 400 000 and 12 ten thousands = 120 000. 400 000 + 120 000 + 7000 = 527 000. "
                 "(The others make %s, %s and %s.)" % tuple(n(w[1]) for w in ws)))
    no, vn = phrase([(3, 5), (2, 3)])
    ys = ["32 ten thousands", "320 thousands", phrase([(2, 5), (12, 4)])[0]]
    assert vn == 302000 and 32 * 10000 == 320 * 1000 == 200000 + 120000 == 320000
    R.append(mcq("Which is <b>not</b> equal to 320" + NB + "000?", no, ys,
                 "3 hundred thousands and 2 thousands = 300 000 + 2000 = 302 000, not 320 000. "
                 "32 ten thousands = 320 000, 320 thousands = 320 000 and 200 000 + 120 000 = 320 000."))
    its = S[:2] + X[:2] + B[:2] + S[2:3] + X[2:3] + B[2:3] + S[3:4] + X[3:4] + B[3:] + S[4:] + X[4:5] \
        + R[:1] + X[5:] + R[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Expanded form and decomposing numbers", "items": its}


# ============================================================ set 4: compare and order
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


def set_compare():
    C = []
    for x, y in [(453000, 450300), (98765, 102345), (634050, 634500), (800091, 799999), (517284, 517824)]:
        lt, gt = "&lt;", "&gt;"
        right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
        wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
                 "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 98765:
            e += " A big first digit does not matter when a number has fewer digits."
        C.append(mcq("Which is true?", right, wrong, e))
    G = []
    for nums, want_max in [([365120, 361520, 356210, 362150], True), ([89999, 100001, 100010, 101000], False),
                           ([708090, 708900, 700980, 79890], True), ([426500, 425060, 426050, 425600], False)]:
        s = sorted(nums)
        ans, nxt = (s[-1], s[-2]) if want_max else (s[0], s[1])
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % n(ans)
            if 79890 in nums:
                e = ("79 890 has only 5 digits, so it is the least. For the 6-digit numbers, c" + e[1:])
        else:
            e = compare_expl(nxt, ans) + " %s is the least." % n(ans)
            if 89999 in nums:
                e = ("89 999 has only 5 digits, so it is the least, even though it starts with 8. "
                     "Every 6-digit number is at least 100 000.")
        G.append(mcq("Which number is the %s?" % ("greatest" if want_max else "least"), n(ans),
                     [n(v) for v in nums if v != ans], e))
    fmt = lambda l: ", ".join(n(v) for v in l)
    O = []
    for nums, up, perms, e in [
        ([453000, 435000, 450300], True, [[450300, 435000, 453000], [453000, 450300, 435000],
                                          [435000, 453000, 450300]],
         "All have 4 hundred thousands. Ten thousands: 3 &lt; 5, so 435 000 is the least. 453 000 and 450 300 both "
         "have 5 ten thousands. Thousands: 0 &lt; 3, so 450 300 &lt; 453 000."),
        ([612040, 164020, 621040], False, [[164020, 612040, 621040], [612040, 621040, 164020],
                                           [621040, 164020, 612040]],
         "Hundred thousands: 1 &lt; 6, so 164 020 is the least. 612 040 and 621 040 both have 6 hundred thousands. "
         "Ten thousands: 2 &gt; 1, so 621 040 &gt; 612 040."),
        ([99500, 105000, 100500, 95050], True, [[99500, 95050, 100500, 105000], [95050, 99500, 105000, 100500],
                                                [105000, 100500, 99500, 95050]],
         "The 5-digit numbers are less than the 6-digit numbers. 95 050 &lt; 99 500 (thousands: 5 &lt; 9). "
         "100 500 &lt; 105 000 (thousands: 0 &lt; 5)."),
        ([990000, 1000000, 909999, 999000], False, [[999000, 990000, 909999, 1000000],
                                                    [1000000, 990000, 999000, 909999],
                                                    [909999, 990000, 999000, 1000000]],
         "1 000 000 has 7 digits, so it is the greatest. Then compare the 6-digit numbers: 999 000 &gt; 990 000 "
         "(thousands: 9 &gt; 0) and 990 000 &gt; 909 999 (ten thousands: 9 &gt; 0)."),
    ]:
        o = sorted(nums) if up else sorted(nums)[::-1]
        assert all(p != o and sorted(p) == sorted(o) for p in perms)
        O.append(mcq("Put %s in order from %s." % (fmt(nums), "least to greatest" if up else "greatest to least"),
                     fmt(o), [fmt(p) for p in perms], e + " Order: %s." % fmt(o)))
    Dg = [
        mcq_n("Use each of the digits 7, 2, 9, 4, 1 and 6 once. What is the greatest number you can make?", 976421,
              [976412, 124679, 796421],
              "Put the biggest digit in the hundred thousands place, then the next biggest, and so on: "
              "9, 7, 6, 4, 2, 1. The greatest number is 976 421."),
        mcq_n("Use each of the digits 5, 0, 8, 3, 6 and 1 once. What is the least 6-digit number you can make?", 103568,
              [13568, 130568, 865310],
              "A 6-digit number cannot start with 0. Put the smallest other digit first: 1. Then 0, 3, 5, 6, 8: "
              "103 568. (013 568 is just 13 568, which has only 5 digits.)"),
        mcq_n("Use each of the digits 6, 0, 2, 0, 9 and 5 once. What is the greatest number you can make?", 965200,
              [965002, 952600, 200569],
              "Biggest digit first: 9, then 6, then 5, then 2. The two 0s go last, in the tens and ones places: 965 200."),
    ]
    assert int("".join(sorted("729416", reverse=True))) == 976421
    assert int("".join(sorted("602095", reverse=True))) == 965200
    Bx = [
        mcq("38☐" + NB + "400 &gt; 386" + NB + "500. Which digit could go in the box?", "8", ["2", "5", "6"],
            "The hundred thousands and ten thousands are the same. Compare the thousands: the box must be 6 or more. "
            "If it is 6, compare the hundreds: 4 &lt; 5, so 386 400 is too small. 388 400 &gt; 386 500."),
        mcq("625" + NB + "☐80 &lt; 625" + NB + "450. Which digit could go in the box?", "3", ["4", "5", "9"],
            "The first three digits are the same. Compare the hundreds: the box must be 4 or less. "
            "If it is 4, compare the tens: 8 &gt; 5, so 625 480 is too big. 625 380 &lt; 625 450."),
    ]
    assert 388400 > 386500 > 386400 and 625380 < 625450 < 625480
    Bt = [
        mcq_n("Which number is between 450" + NB + "000 and 460" + NB + "000?", 458700, [465000, 449900, 45870],
              "A number between 450 000 and 460 000 has 4 hundred thousands and 5 ten thousands. 458 700 fits. "
              "465 000 is too big, 449 900 is too small and 45 870 has only 5 digits."),
        mcq_n("Which number is between 799" + NB + "000 and 801" + NB + "000?", 800150, [801500, 790900, 80015],
              "800 150 is more than 800 000 and less than 801 000, so it is between 799 000 and 801 000. "
              "801 500 is too big, 790 900 is too small and 80 015 has only 5 digits."),
    ]
    assert 450000 < 458700 < 460000 and 799000 < 800150 < 801000 and 790900 < 799000 and 801500 > 801000
    its = C[:2] + G[:2] + O[:1] + C[2:3] + Bt[:1] + Dg[:1] + G[2:3] + O[1:2] + C[3:4] + Bt[1:] + Dg[1:2] \
        + G[3:] + O[2:3] + C[4:] + Bx[:1] + Dg[2:] + O[3:] + Bx[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Compare and order numbers to 1 000 000", "items": its}


# ============================================================ set 5: rounding and real-life numbers
PLACE_TO = {1: "ten", 2: "hundred", 3: "thousand", 4: "ten thousand", 5: "hundred thousand"}


def round_e(x, p):
    r = rnd_to(x, p)
    look = digit(x, p - 1)
    lo = x // 10 ** p * 10 ** p
    return ("Nearest %s: %s is between %s and %s. Look at the %s digit: %d. %s So %s rounds to %s."
            % (PLACE_TO[p], n(x), n(lo), n(lo + 10 ** p), PL[p - 1], look,
               "5 or more, so round up." if look >= 5 else "4 or less, so round down.", n(x), n(r)))


def set_life(P):
    L = [
        mcq_n(fig(line_svg(0, 1000000, 100000, [0, 500000, 1000000], arrow=700000))
              + "What number does the arrow point to?", 700000, [70000, 600000, 800000],
              "From 0 to 1 000 000 there are 10 equal spaces, so each space is 100 000. "
              "The arrow is 2 spaces after 500 000: 600 000, 700 000."),
        mcq_n(fig(line_svg(400000, 500000, 10000, [400000, 450000, 500000], arrow=430000))
              + "What number does the arrow point to?", 430000, [403000, 420000, 470000],
              "From 400 000 to 500 000 there are 10 equal spaces, so each space is 10 000, not 1000. "
              "The arrow is 3 spaces after 400 000: 430 000."),
        mcq_n(fig(line_svg(200000, 300000, 20000, [200000, 300000], arrow=260000))
              + "What number does the arrow point to?", 260000, [230000, 240000, 280000],
              "From 200 000 to 300 000 there are only 5 equal spaces, so each space is 100 000 ÷ 5 = 20 000. "
              "The arrow is 3 spaces after 200 000: 220 000, 240 000, 260 000. (230 000 counts each space as 10 000.)"),
    ]
    R = []
    for x, p, wrong, extra in [
        (453600, 4, [460000, 500000, 454000], ""),
        (678500, 3, [678000, 680000, 700000], " Do not just drop the hundreds: 678 000 is cutting off, not rounding."),
        (345120, 5, [350000, 400000, 340000],
         " Round the number you started with. Do not round to 350 000 first and then to 400 000."),
        (850960, 5, [800000, 850000, 851000], ""),
        (299610, 3, [299000, 299600, 290000],
         " 299 thousands + 1 thousand = 300 thousands, so the answer is 300 000."),
    ]:
        r = rnd_to(x, p)
        assert r not in wrong
        R.append(mcq_n("Round %s to the nearest %s." % (n(x), PLACE_TO[p]), r, wrong, round_e(x, p) + extra))
    W = []
    assert rnd_to(568322, 4) == 570000
    W.append(mcq_n("In the 2021 Census, Surrey had 568" + NB + "322 people. Round this number to the nearest "
                   "ten thousand.", 570000, [560000, 600000, 568000], round_e(568322, 4)))
    W.append(mcq("In the 2021 Census, Kamloops had 97" + NB + "902 people and Nanaimo had 99" + NB + "863 people. "
                 "Which city had more people?", "Nanaimo", ["Kamloops", "They had the same", "You cannot tell"],
                 compare_expl(99863, 97902) + " Nanaimo had more people."))
    W.append(mcq("In the 2021 Census, Kelowna had 144" + NB + "576 people, Abbotsford had 153" + NB + "524 and "
                 "Coquitlam had 148" + NB + "625. Which list goes from least to greatest?",
                 ", ".join(n(v) for v in [144576, 148625, 153524]),
                 [", ".join(n(v) for v in l) for l in [[148625, 144576, 153524], [153524, 148625, 144576],
                                                       [144576, 153524, 148625]]],
                 "Ten thousands: 4 &lt; 5, so 153 524 is the greatest. 144 576 and 148 625 both have 4 ten thousands. "
                 "Thousands: 4 &lt; 8, so 144 576 &lt; 148 625. Order: 144 576, 148 625, 153 524."))
    W.append(mcq_n("Volunteers counted three hundred forty thousand five hundred sockeye salmon swimming up a BC "
                   "river. Write the number in digits.", 340500, [34500, 340050, 3400500],
                   words_e(340500) + " 34 500 leaves out the 0 in the thousands place."))
    W.append(mcq_n("In the 2021 Census, Burnaby had 249" + NB + "125 people. What is the value of the 4?", 40000,
                   [4, 4000, 400000],
                   "249 125 is 2 hundred thousands, 4 ten thousands, 9 thousands, 1 hundred, 2 tens and 5 ones. "
                   "The 4 is in the ten thousands place, so it is worth 40 000, not 4."))
    W.append(mcq("Which is the best estimate for the number of people at a sold-out football game at BC Place "
                 "in Vancouver?", "about 54" + NB + "000", ["about 540", "about 5400", "about 540" + NB + "000"],
                 "BC Place is a stadium that holds about 54 000 people, so about 54 000 is a good estimate. About 540 "
                 "or 5400 is far too few, and 540 000 is almost as many people as live in Surrey."))
    assert rnd_to(209937, 5) == 200000 and rnd_to(250000, 5) == 300000 and rnd_to(149900, 5) == 100000
    W.append(mcq_n("A BC city’s population, rounded to the nearest hundred thousand, is 200" + NB + "000. "
                   "Which could be the real population?", 209937, [250000, 149900, 20990],
                   "Numbers from 150 000 up to 249 999 round to 200 000. 209 937 has 0 ten thousands, so it rounds "
                   "down to 200 000. 250 000 rounds up to 300 000, 149 900 rounds to 100 000, and 20 990 is far too "
                   "small. (209 937 was the population of Richmond in the 2021 Census.)"))
    assert rnd_to(386452, 3) == 386000
    W.append(mcq_n("A fish counter on a river counted 386" + NB + "452 pink salmon in one season. Round the count to "
                   "the nearest thousand.", 386000, [387000, 390000, 386500], round_e(386452, 3)))
    W.append(mcq_n("Schools in a BC school district raised one hundred five thousand three hundred dollars for the "
                   "Terry Fox Run. Write the amount in numbers.", 105300, [15300, 105030, 150300],
                   words_e(105300) + " The amount is $105 300.", pre="$"))
    assert 589650 + 100000 == 689650
    W.append(mcq_n("A region had 589" + NB + "650 people. Twenty years later it has 100" + NB + "000 more people. "
                   "How many people live there now?", 689650, [599650, 589750, 1589650],
                   "Adding 100 000 changes the hundred thousands digit: 5 + 1 = 6 hundred thousands. "
                   "589 650 + 100 000 = 689 650. (599 650 adds only 10 000.)"))
    name, he, his = P.next()
    W.append(mcq_n("%s’s mystery number has 7 hundred thousands, 0 ten thousands, 4 thousands, 0 hundreds, "
                   "2 tens and 0 ones. What is it?" % name, 704020, [742, 74020, 740020],
                   "Write one digit for each place, with 0 for the empty places: 7, 0, 4, 0, 2, 0. That is 704 020."))
    assert 6 * 100000 == 600000
    W.append(mcq_n("A salmon hatchery on Vancouver Island releases 100" + NB + "000 young coho salmon each spring. "
                   "How many does it release in 6 springs?", 600000, [60000, 500000, 6000000],
                   "Count by 100 000s: 100 000, 200 000, 300 000, 400 000, 500 000, 600 000. "
                   "6 × 100 000 = 600 000. (500 000 counts only 5 springs, and 60 000 leaves out a 0.)"))
    its = L[:2] + R[:2] + L[2:] + R[2:] + W
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Rounding and real-life BC numbers", "items": its}


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
        "<p>Each place is worth <b>10 times</b> the place to its right: ones, tens, hundreds, thousands, "
        "ten thousands, hundred thousands. Ten hundred thousands make <b>1 000 000</b> (one million). "
        "Big numbers are split into groups of three digits. In BC we leave a small space between the groups "
        "(405 030), not a comma. A 4-digit number has no space (4503).</p>"
        "<figure class='sn-fig'>" + chart_svg(453000, hi=5) +
        "<figcaption>453 000: the 4 is in the hundred thousands place, so it is worth 400 000.</figcaption></figure>"
        "<p>Place value disks show the same thing. Find the value of each group, then add.</p>"
        "<figure class='sn-fig'>" + disks_svg([2, 0, 5, 0, 1, 0]) +
        "<figcaption>200 000 + 5000 + 10 = 205 010. There are no ten thousands, hundreds or ones, "
        "so write 0 there.</figcaption></figure>"
        + ex("Words to digits", "Write forty thousand five hundred three in digits.",
             "Forty thousand → 40. Five hundred three → 503 (always three digits after the space).",
             "40 503 (not 4503)")
        + "<h2>The value of a digit</h2>"
        "<p>The <b>digit</b> is the symbol. Its <b>value</b> depends on its place. In 471 250 the digit 7 is in the "
        "ten thousands place, so its value is 70 000, not 7.</p>"
        "<h2>Expanded form and decomposing</h2>"
        "<p><b>Expanded form</b> shows the value of each digit: 683 725 = 600 000 + 80 000 + 3000 + 700 + 20 + 5. "
        "Leave out the zeros: 405 030 = 400 000 + 5000 + 30.</p>"
        + ex("Decompose", "Write 453 000 in three ways.",
             "Expanded form: 400 000 + 50 000 + 3000. It is also 45 ten thousands and 3 thousands, or 453 thousands.",
             "400 000 + 50 000 + 3000 = 45 ten thousands + 3 thousands = 453 thousands")
        + "<h2>Compare and order</h2>"
        "<p>First count the digits: a 6-digit number is greater than any 5-digit number. If both have the same "
        "number of digits, compare place by place from the left until two digits are different.</p>"
        + ex("Compare", "634 050 ☐ 634 500",
             "Hundred thousands: 6 = 6. Ten thousands: 3 = 3. Thousands: 4 = 4. Hundreds: 0 &lt; 5.",
             "634 050 &lt; 634 500")
        + "<h2>Number lines and rounding</h2>"
        "<p>On a number line, work out the size of each space first. To round, look at the digit "
        "<b>one place to the right</b>: 5 or more rounds up, 4 or less rounds down.</p>"
        "<figure class='sn-fig'>" + line_svg(400000, 500000, 10000, [400000, 450000, 500000], arrow=430000, show=True) +
        "<figcaption>Each space is 10 000. 430 000 is closer to 400 000 than to 500 000, so to the nearest "
        "hundred thousand it rounds to 400 000.</figcaption></figure>"
        + table(["Round 678 500 to the nearest …", "Look at", "Answer"], [
            ["hundred thousand", "the ten thousands digit: 7", "700 000"],
            ["ten thousand", "the thousands digit: 8", "680 000"],
            ["thousand", "the hundreds digit: 5", "679 000"],
        ])
        + "<h2>Big numbers in BC</h2>"
        "<p>We see numbers to 1 000 000 in the populations of BC cities, in salmon counts on our rivers, in crowds "
        "at BC Place and in money raised for the Terry Fox Run. News reports often round them: Surrey’s 568 322 "
        "people in the 2021 Census becomes “about 570 000 people”.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving out a zero (forty thousand five hundred three → 4503)",
             "Write three digits after the space: 40 | 503 → 40 503"],
            ["Giving the digit, not its value (the 7 in 471 250 is 7)", "It is in the ten thousands place: 70 000"],
            ["Counting the disks (3 + 4 + 2 = 9)", "Add the values: 300 000 + 40 000 + 200 = 340 200"],
            ["Comparing the first digits only (98 765 &gt; 102 345)", "Count the digits first: 102 345 &gt; 98 765"],
            ["Thinking every space on a number line is 1000", "Work out the space first: 400 000 to 500 000 in 10 spaces is 10 000 each"],
            ["Rounding twice (345 120 → 350 000 → 400 000)", "Round the number you started with: 300 000"],
        ])
    )


FAQ = [
    {"q": "What number concepts are in the BC Grade 5 math curriculum?",
     "a": "Grade 5 students in BC work with number concepts to 1 000 000: reading and writing numbers, place value, "
          "expanded form, comparing and ordering, and rounding. They also work with decimals to thousandths."},
    {"q": "How do you write one million in numbers?",
     "a": "One million is 1 000 000: a 1 followed by six zeros, with a space between each group of three digits. "
          "It is 10 hundred thousands, or 1000 thousands."},
    {"q": "How do you write forty thousand five hundred three in numbers?",
     "a": "Write 40 for the thousands part and 503 for the rest: 40 503. The part after the space always has three "
          "digits, so the number is not 4503."},
    {"q": "How do you round a 6-digit number to the nearest ten thousand?",
     "a": "Look at the thousands digit. If it is 5 or more, round up; if it is 4 or less, keep the ten thousands digit "
          "and change the rest to 0. So 568 322 rounds to 570 000 and 453 600 rounds to 450 000."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (405 030) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "body_html", "standard_text"):
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
    """Tag wide pictures (place value charts, disks, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(55801)
    P = People(random.Random(558011))
    sets = [set_read(), set_value(), set_expand(), set_compare(), set_life(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "numbers-to-1000000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 1 000 000: Place Value, Comparing and Rounding",
        "seo_title": "Grade 5 Numbers to 1 000 000 Math Worksheets: Free, with Answer Key (BC Curriculum)",
        "short_title": "Numbers to 1 000 000",
        "domain": "Number",
        "standard_code": "Grade 5: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Number concepts to 1 000 000",
        "meta_desc": "Free Grade 5 math worksheets on numbers to 1 000 000 for the BC curriculum: place value, the value of each digit, expanded form, comparing and ordering, and rounding with real BC numbers. 100 questions with an answer key.",
        "key_big": "The place of a digit tells you its value. The 4 in 453 000 is worth 400 000.",
        "key_sub": "Write three digits after each space: forty thousand five hundred three is 40 503, not 4503. To compare, count the digits first, then compare from the left.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "(number line|place value chart|place value disks)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
