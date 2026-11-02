# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 5 Math: Numbers to 100 000
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 5: B1.1, also B1.2)
  python3 tools/gen_caon_math_g5_numbers.py
Read, write, represent, compose and decompose whole numbers to 100 000, compare and order them,
use number lines and rounding, and work with numbers from everyday life (crowds, populations, money).
Numbers: 4-digit numbers have no separator (4503); 5 or more digits use a no-break space (45 300). Never commas.
Wrong answers come from real mistakes: leaving out a zero (forty thousand five hundred three -> 4503),
giving the digit instead of its value (the 7 in 47 125 is 7), counting place value disks instead of
adding their values, reading a number line as if every space were 1000, comparing by the first digit only,
writing 14 thousands inside the number, rounding the wrong place, cutting off instead of rounding,
and rounding twice.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand"]


# ------------------------------------------------------------ helpers
def n(x):
    """Ontario/SI style: 4503, 10 000, 45 300 (no-break spaces, never commas)."""
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
    """Value of an expanded-form choice such as '40 000 + 500 + 3' or '9 × 10 000 + 5 × 1'."""
    s = s.replace(NB, "")
    tot = 0
    for term in s.split("+"):
        p = 1
        for f in term.split("×"):
            p *= int(f.strip())
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


def cap(s):
    return s[0].upper() + s[1:]


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
    assert 0 < x < 1000000
    t, o = divmod(x, 1000)
    parts = []
    if t:
        parts.append(w1000(t) + " thousand")
    if o:
        parts.append(w1000(o))
    return " ".join(parts)


assert words(40503) == "forty thousand five hundred three"
assert words(72080) == "seventy-two thousand eighty"
assert words(100000) == "one hundred thousand"


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 64, 28, 28, 48
SUB = ["H", "T", "O", "H", "T", "O"]


def chart_svg(x, hi=None):
    """Thousands (H T O) | Ones (H T O) chart with a number up to 100 000. hi = place index drawn in red."""
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


DISK_FILL = {4: "#f2d4cf", 3: "#d6e4f4", 2: "#cfe6d6", 1: "#fbe9c0", 0: "#e4e4e4"}
DR = 30          # disk radius (fits “10 000” at 14px)
DG = 4           # gap between disks
GG = 18          # gap between place groups


def disks_svg(counts):
    """Place value disks. counts = [ten thousands, thousands, hundreds, tens, ones].
    Each place with disks is a group of up to 2 columns x 3 rows."""
    assert all(0 <= c <= 6 for c in counts)
    groups = [(4 - k, c) for k, c in enumerate(counts) if c]
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
    value = sum(c * 10 ** (4 - k) for k, c in enumerate(counts))
    return svg_wrap(W, H, "".join(s), "place value disks showing %s" % n(value))


def line_svg(lo, hi, step, labels, arrow=None, show=None):
    """Number line lo..hi, a tick every step, numbers at `labels`, red arrow at `arrow` (with its value if show)."""
    L, R = 58, 422
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


# ============================================================ set 1: read and write numbers to 100 000
def disks_e(counts):
    parts = [(c, 10 ** (4 - k)) for k, c in enumerate(counts)]
    value = sum(c * v for c, v in parts)
    used = ["%d × %s = %s" % (c, n(v), n(c * v)) for c, v in parts if c]
    empty = [PL[4 - k] for k, c in enumerate(counts) if c == 0]
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
    for counts, wrong in [([4, 5, 3, 0, 0], [453, 4530, 12]),
                          ([3, 0, 2, 1, 6], [3216, 32160, 12]),
                          ([1, 2, 0, 4, 0], [124, 1240, 12400]),
                          ([2, 0, 0, 5, 1], [251, 2051, 20510])]:
        x = sum(c * 10 ** (4 - k) for k, c in enumerate(counts))
        e = disks_e(counts)
        if sum(counts) in wrong:
            e += " Do not just count the disks: each disk has its own value."
        D_.append(mcq_n(fig(disks_svg(counts)) + "What number do the place value disks show?", x, wrong, e))
    P_ = []
    for x, i in [(63527, 4), (28914, 3), (50762, 2)]:
        others = [PL[k] for k in sorted(range(5), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        P_.append(mcq(fig(chart_svg(x, hi=i)) + "Which place is the red digit in?", PL[i], others,
                      "Read the places from the right: ones, tens, hundreds, thousands, ten thousands. "
                      "In %s the red %d is in the %s place." % (n(x), digit(x, i), PL[i])))
    G_ = []
    for x, i in [(74381, 3), (59026, 2)]:
        d = digit(x, i)
        cands = [str(digit(x, k)) for k in sorted(range(5), key=lambda k: (abs(k - i), -k)) if k != i]
        cands = [c for c in cands if c != str(d)][:3]
        e = "In %s: %s. The %s digit is %d." % (
            n(x), ", ".join("%s %d" % (PL[k], digit(x, k)) for k in range(4, -1, -1)), PL[i], d)
        if d == 0:
            e += " The 0 shows there are no %s." % PL[i]
        G_.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    W_ = []
    for x, wrong in [(40503, [4503, 400503, 45003]), (72080, [7280, 72800, 72008]),
                     (30006, [3006, 30060, 30600]), (15400, [1540, 15040, 50400])]:
        e = words_e(x)
        if x == 15400:
            e += " Fifteen is 15, not 50."
        W_.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, wrong, e))
    W_.append(mcq_n("Which number is <b>one hundred thousand</b>?", 100000, [10000, 1000000, 1000],
                    "One hundred thousand is 100 groups of 1000. Write 100 for the thousands part and 000 for the rest: "
                    "100 000. It has 6 digits. (10 000 is ten thousand.)"))
    R_ = []
    for x, wx in [(60405, [6405, 60045, 64005]), (18070, [18700, 80070, 1870]), (47012, [47120, 4712, 47021])]:
        e = ("Split %s into the thousands part and the rest: %d thousand and %d. Say each part: %s."
             % (n(x), x // 1000, x % 1000, words(x)))
        if x == 18070:
            e += " Eighteen is 18, eighty is 80."
        R_.append(mcq("How do you write %s in words?" % n(x), words(x), [words(v) for v in wx], e))
    C_ = [
        mcq_n("How many thousands make 10" + NB + "000?", 10, [100, 1000, 1],
              "Count by thousands: 1000, 2000, 3000 … 10 000. That is 10 thousands. Each place is worth "
              "10 times the place to its right."),
        mcq_n("Ten groups of 10" + NB + "000 make what number?", 100000, [10000, 1000000, 10010],
              "10 × 10 000 = 100 000. Count by ten thousands: 10 000, 20 000 … 100 000. "
              "Ten ten thousands make one hundred thousand."),
        mcq_n("What number is 1 more than 99" + NB + "999?", 100000, [10000, 1000000, 99998],
              "99 999 + 1: every 9 becomes 0 as you regroup, and a 1 goes in the hundred thousands place: 100 000. "
              "(99 998 is 1 less.)"),
    ]
    assert 10 * 10000 == 100000 and 99999 + 1 == 100000
    its = D_[:2] + P_[:2] + G_[:1] + W_[:2] + D_[2:3] + P_[2:] + R_[:1] + W_[2:3] + G_[1:] + C_[:1] \
        + D_[3:] + W_[3:4] + R_[1:2] + C_[1:2] + W_[4:] + R_[2:] + C_[2:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Read and write numbers to 100 000", "items": its}


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
    for x, i in [(52846, 3), (37415, 4), (80962, 2), (64178, 1), (19553, 3)]:
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    B = []
    for x, d in [(47125, 7), (23609, 3), (70284, 7), (91538, 5), (46820, 2)]:
        assert str(x).count(str(d)) == 1
        i = ndig(x) - 1 - str(x).index(str(d))
        B.append(mcq_n("What is the value of the %d in %s?" % (d, n(x)), d * 10 ** i, value_cands(d, i), value_e(d, i)))
    H = []
    for d, i, ans, wrong in [(6, 4, 63205, [36205, 6205, 23650]), (4, 3, 74019, [47019, 70419, 40719]),
                             (0, 2, 58037, [58307, 50837, 58370])]:
        assert digit(ans, i) == d and all(digit(w, i) != d for w in wrong)
        e = "%s has %s." % (n(ans), ", ".join(plural(digit(ans, k), k) for k in range(4, -1, -1)))
        e += " The %s digit is %d." % (PL[i], d)
        H.append(mcq_n("Which number has %s %d in the %s place?" % ("an" if d == 8 else "a", d, PL[i]), ans, wrong, e))
    T = [
        mcq_n("The 4 in 40" + NB + "000 is worth how many times the 4 in 4000?", 10, [100, 4, 36000],
              "The first 4 is worth 40 000. The second 4 is worth 4000. 40 000 ÷ 4000 = 10. "
              "Each place is worth 10 times the place to its right. (36 000 is the difference, not how many times.)"),
        mcq_n("In 55" + NB + "500, the first 5 is worth how many times the second 5?", 10, [100, 5, 45000],
              "The first 5 is in the ten thousands place: 50 000. The second 5 is in the thousands place: 5000. "
              "50 000 ÷ 5000 = 10."),
    ]
    assert 40000 // 4000 == 10 and 50000 // 5000 == 10
    Tot = [
        mcq_n("37" + NB + "800 = ☐ thousands and 8 hundreds. What number goes in the box?", 37, [7, 3, 378],
              "37 800 = 37 000 + 800. 37 000 is 37 thousands. So 37 800 = 37 thousands and 8 hundreds. "
              "(7 is only the thousands digit.)"),
        mcq_n("26" + NB + "000 = ☐ hundreds. What number goes in the box?", 260, [26, 2600, 6],
              "1000 = 10 hundreds, so 26 thousands = 26 × 10 = 260 hundreds. Check: 260 × 100 = 26 000."),
    ]
    assert 37 * 1000 + 800 == 37800 and 260 * 100 == 26000
    Re = [mcq_n("The town of Lakeview has 28" + NB + "460 people. What is the value of the 8?", 8000, [8, 800, 80000],
                "28 460 is 2 ten thousands, 8 thousands, 4 hundreds, 6 tens and 0 ones. "
                "The 8 is in the thousands place, so it is worth 8000.")]
    Z = [
        mcq_n("Which number has 0 thousands?", 40516, [45016, 45160, 4516],
              "40 516 is 4 ten thousands, 0 thousands, 5 hundreds, 1 ten and 6 ones. "
              "The other numbers all have 4 or 5 thousands."),
        mcq("In 90" + NB + "407, which digit is in the tens place?", "0", ["4", "7", "9"],
            "90 407 is 9 ten thousands, 0 thousands, 4 hundreds, 0 tens and 7 ones. "
            "The tens digit is 0: there are no tens."),
    ]
    for w, k in [(45016, 3), (45160, 3), (4516, 3)]:
        assert digit(w, k) != 0
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
    """[(count, place index)] -> ('4 ten thousands, 12 thousands and 7 hundreds', value)."""
    ws = [plural(c, i) for c, i in parts]
    return ", ".join(ws[:-1]) + " and " + ws[-1], sum(c * 10 ** i for c, i in parts)


def set_expand():
    S = []
    for x, wrong in [(68725, ["6 + 8 + 7 + 2 + 5", "60 000 + 800 + 700 + 20 + 5", "6000 + 8000 + 700 + 20 + 5"]),
                     (45300, ["4 + 5 + 3", "40 000 + 5000 + 30", "40 000 + 500 + 300"]),
                     (40503, ["4000 + 500 + 3", "40 000 + 5000 + 3", "40 000 + 500 + 30"]),
                     (72080, ["70 000 + 2000 + 8", "70 000 + 200 + 80", "7000 + 2000 + 80"]),
                     (93016, ["90 000 + 3000 + 100 + 6", "9000 + 3000 + 10 + 6", "90 000 + 300 + 10 + 6"])]:
        wrong = [nbsp(w) for w in wrong]
        e = "Write the value of each digit that is not 0: %s. That is %s." % (
            ", ".join("%s %d = %s" % (PL[i], digit(x, i), n(digit(x, i) * 10 ** i))
                      for i in range(4, -1, -1) if digit(x, i)), expd(x))
        if "0" in str(x):
            e += " A 0 adds nothing, so it is left out."
        S.append(mcq_x("What is %s in expanded form?" % n(x), expd(x), wrong, e, x))
    X = []
    for terms, x, wrong in [(["80 000", "600", "4"], 80604, [8604, 86004, 80064]),
                            (["30 000", "7000", "20"], 37020, [3720, 37200, 30720]),
                            (["50 000", "9"], 50009, [509, 5009, 50090]),
                            (["300", "20 000", "1", "4000", "60"], 24361, [32146, 24316, 2436])]:
        ex_ = " + ".join(t.replace(" ", NB) for t in terms)
        assert xval(ex_) == x
        e = ("Put each value in its place and write 0 in every empty place. %s → %s." % (ex_, n(x)))
        if x == 24361:
            e = ("The parts are not in order. Sort them from the greatest place: 20 000 + 4000 + 300 + 60 + 1 = 24 361. "
                 "Do not write the digits in the order you see them.")
        X.append(mcq_n("What number is <b>%s</b>?" % ex_, x, wrong, e))
    for x, wrong in [(90605, [965, 9605, 90650]), (70029, [729, 7029, 70290])]:
        mf = mult_form(x)
        assert xval(mf) == x
        X.append(mcq_n("What number is <b>%s</b>?" % mf, x, wrong,
                       "Work out each part: %s. Add them: %s. Write 0 in every empty place." % (
                           ", ".join("%d × %s = %s" % (digit(x, i), n(10 ** i), n(digit(x, i) * 10 ** i))
                                     for i in range(4, -1, -1) if digit(x, i)), n(x))))
    B = []
    for q, x, ans, wrong in [("60 000 + ☐ + 700 + 20 + 5 = 68 725", 68725, 8000, [8, 800, 80000]),
                             ("☐ + 3000 + 40 + 2 = 53 042", 53042, 50000, [5, 5000, 500]),
                             ("70 000 + 400 + ☐ = 70 409", 70409, 9, [90, 900, 9000]),
                             ("10 000 + 5000 + ☐ + 6 = 15 086", 15086, 80, [8, 800, 86])]:
        q = re.sub(r"(?<=\d) (?=\d{3})", NB, q)
        lhs = q.split("=")[0].replace("☐", str(ans))
        assert xval(lhs) == x
        i = [k for k in range(5) if digit(x, k) * 10 ** k == ans][0]
        B.append(mcq_n(q + ". What number goes in the box?", ans, wrong,
                       "%s has %s in the %s place. That is worth %s." % (n(x), digit(x, i), PL[i], n(ans))))
    R = []
    R.append(mcq_n("45" + NB + "300 = ☐ hundreds. What number goes in the box?", 453, [45, 4530, 3],
                   "45 300 = 45 thousands and 3 hundreds. 45 thousands = 450 hundreds. 450 + 3 = 453 hundreds. "
                   "Check: 453 × 100 = 45 300."))
    assert 453 * 100 == 45300
    p, v = phrase([(3, 4), (14, 3), (2, 2)])
    assert v == 44200
    R.append(mcq_n("What number is %s?" % p, 44200, [314200, 34200, 3142],
                   "3 ten thousands = 30 000 and 14 thousands = 14 000. 30 000 + 14 000 + 200 = 44 200. "
                   "Do not write 14 inside the number: 14 thousands is 1 ten thousand and 4 thousands."))
    R.append(mcq_n("26" + NB + "400 = 1 ten thousand, ☐ thousands and 4 hundreds. What number goes in the box?",
                   16, [6, 26, 160],
                   "26 400 = 2 ten thousands, 6 thousands and 4 hundreds. Trade 1 ten thousand for 10 thousands: "
                   "10 + 6 = 16 thousands. Check: 10 000 + 16 000 + 400 = 26 400."))
    assert 10000 + 16000 + 400 == 26400
    ok, vo = phrase([(4, 4), (12, 3), (7, 2)])
    ws = [phrase([(4, 4), (2, 3), (7, 2)]), phrase([(5, 4), (12, 3), (7, 2)]), phrase([(4, 4), (12, 3), (70, 2)])]
    assert vo == 52700 and len({vo} | {w[1] for w in ws}) == 4
    R.append(mcq("Which is another way to make 52" + NB + "700?", ok, [w[0] for w in ws],
                 "4 ten thousands = 40 000 and 12 thousands = 12 000. 40 000 + 12 000 + 700 = 52 700. "
                 "(The others make %s, %s and %s.)" % tuple(n(w[1]) for w in ws)))
    no, vn = phrase([(3, 4), (2, 2)])
    ys = ["32 thousands", "320 hundreds", phrase([(2, 4), (12, 3)])[0]]
    assert vn == 30200 and 32 * 1000 == 320 * 100 == 20000 + 12000 == 32000
    R.append(mcq("Which is <b>not</b> equal to 32" + NB + "000?", no, ys,
                 "3 ten thousands and 2 hundreds = 30 000 + 200 = 30 200, not 32 000. "
                 "32 thousands = 32 000, 320 hundreds = 32 000 and 20 000 + 12 000 = 32 000."))
    its = S[:2] + X[:2] + B[:2] + S[2:3] + X[2:3] + B[2:3] + S[3:4] + X[3:4] + B[3:] + S[4:] + X[4:5] \
        + R[:1] + X[5:] + R[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Expanded form and decomposing numbers", "items": its}


# ============================================================ set 4: compare and order
def first_diff(a, b):
    for i in range(5, -1, -1):
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
    its = []
    C = []
    for x, y in [(45300, 45030), (9876, 10234), (63405, 63450), (80091, 79999), (51728, 51782)]:
        lt, gt = "&lt;", "&gt;"
        right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
        wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
                 "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 9876:
            e += " A big first digit does not matter when a number has fewer digits."
        C.append(mcq("Which is true?", right, wrong, e))
    G = []
    for nums, want_max in [([36512, 36152, 35621, 36215], True), ([8999, 10001, 10010, 10100], False),
                           ([70809, 70890, 70098, 7989], True), ([42650, 42506, 42605, 42560], False)]:
        s = sorted(nums)
        ans, nxt = (s[-1], s[-2]) if want_max else (s[0], s[1])
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % n(ans)
            if 7989 in nums:
                e = ("7989 has only 4 digits, so it is the least. For the 5-digit numbers, c" + e[1:])
        else:
            e = compare_expl(nxt, ans) + " %s is the least." % n(ans)
            if 8999 in nums:
                e = ("8999 has only 4 digits, so it is the least, even though it starts with 8. "
                     "Every 5-digit number is at least 10 000.")
        G.append(mcq("Which number is the %s?" % ("greatest" if want_max else "least"), n(ans),
                     [n(v) for v in nums if v != ans], e))
    fmt = lambda l: ", ".join(n(v) for v in l)
    O = []
    for nums, up, perms, e in [
        ([45300, 43500, 45030], True, [[45030, 43500, 45300], [45300, 45030, 43500], [43500, 45300, 45030]],
         "All have 4 ten thousands. Thousands: 3 &lt; 5, so 43 500 is the least. 45 300 and 45 030 both have "
         "5 thousands. Hundreds: 0 &lt; 3, so 45 030 &lt; 45 300."),
        ([61204, 16402, 62104], False, [[16402, 61204, 62104], [61204, 62104, 16402], [62104, 16402, 61204]],
         "Ten thousands: 1 &lt; 6, so 16 402 is the least. 61 204 and 62 104 both have 6 ten thousands. "
         "Thousands: 2 &gt; 1, so 62 104 &gt; 61 204."),
        ([9950, 10500, 10050, 9505], True, [[9950, 9505, 10050, 10500], [9505, 9950, 10500, 10050],
                                            [10500, 10050, 9950, 9505]],
         "The 4-digit numbers are less than the 5-digit numbers. 9505 &lt; 9950 (hundreds: 5 &lt; 9). "
         "10 050 &lt; 10 500 (hundreds: 0 &lt; 5)."),
        ([99000, 100000, 90999, 99900], False, [[99900, 99000, 90999, 100000], [100000, 99000, 99900, 90999],
                                               [90999, 99000, 99900, 100000]],
         "100 000 has 6 digits, so it is the greatest. Then compare the 5-digit numbers: 99 900 &gt; 99 000 "
         "(hundreds: 9 &gt; 0) and 99 000 &gt; 90 999 (thousands: 9 &gt; 0)."),
    ]:
        o = sorted(nums) if up else sorted(nums)[::-1]
        assert all(p != o and sorted(p) == sorted(o) for p in perms)
        O.append(mcq("Put %s in order from %s." % (fmt(nums), "least to greatest" if up else "greatest to least"),
                     fmt(o), [fmt(p) for p in perms], e + " Order: %s." % fmt(o)))
    Dg = [
        mcq_n("Use each of the digits 7, 2, 9, 4 and 1 once. What is the greatest number you can make?", 97421,
              [97412, 14279, 79421],
              "Put the biggest digit in the ten thousands place, then the next biggest, and so on: 9, 7, 4, 2, 1. "
              "The greatest number is 97 421."),
        mcq_n("Use each of the digits 5, 0, 8, 3 and 6 once. What is the least 5-digit number you can make?", 30568,
              [3568, 35068, 86530],
              "A 5-digit number cannot start with 0. Put the smallest other digit first: 3. Then 0, 5, 6, 8: 30 568. "
              "(03 568 is just 3568, which has only 4 digits.)"),
        mcq_n("Use each of the digits 6, 0, 2, 0 and 9 once. What is the greatest number you can make?", 96200,
              [96002, 92600, 20069],
              "Biggest digit first: 9, then 6, then 2. The two 0s go last, in the tens and ones places: 96 200."),
    ]
    assert int("".join(sorted("72941", reverse=True))) == 97421
    Bx = [
        mcq("4☐" + NB + "215 &gt; 47" + NB + "300. Which digit could go in the box?", "8", ["3", "6", "7"],
            "The ten thousands are the same. Compare the thousands: the box must be 7 or more. If it is 7, compare "
            "the hundreds: 2 &lt; 3, so 47 215 is too small. 48 215 &gt; 47 300."),
        mcq("62" + NB + "☐80 &lt; 62" + NB + "450. Which digit could go in the box?", "3", ["4", "5", "9"],
            "The ten thousands and thousands are the same. Compare the hundreds: the box must be 4 or less. "
            "If it is 4, compare the tens: 8 &gt; 5, so 62 480 is too big. 62 380 &lt; 62 450."),
    ]
    assert 48215 > 47300 and 47215 < 47300 and 62380 < 62450 and 62480 > 62450
    Bt = [
        mcq_n("Which number is between 45" + NB + "000 and 46" + NB + "000?", 45870, [46500, 44990, 4580],
              "A number between 45 000 and 46 000 has 4 ten thousands and 5 thousands. 45 870 fits. "
              "46 500 is too big, 44 990 is too small and 4580 has only 4 digits."),
        mcq_n("Which number is between 79" + NB + "900 and 80" + NB + "100?", 80015, [80150, 79090, 8010],
              "80 015 is more than 80 000 and less than 80 100, so it is between 79 900 and 80 100. "
              "80 150 is too big, 79 090 is too small and 8010 has only 4 digits."),
    ]
    assert 45000 < 45870 < 46000 and 79900 < 80015 < 80100 and not 79900 < 79090
    its = C[:2] + G[:2] + O[:1] + C[2:3] + Bt[:1] + Dg[:1] + G[2:3] + O[1:2] + C[3:4] + Bt[1:] + Dg[1:2] \
        + G[3:] + O[2:3] + C[4:] + Bx[:1] + Dg[2:] + O[3:] + Bx[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Compare and order numbers to 100 000", "items": its}


# ============================================================ set 5: number lines, rounding and real-life numbers
PLACE_TO = {1: "ten", 2: "hundred", 3: "thousand", 4: "ten thousand"}


def round_e(x, p):
    r = rnd_to(x, p)
    look = digit(x, p - 1)
    lo = x // 10 ** p * 10 ** p
    return ("Nearest %s: %s is between %s and %s. Look at the %s digit: %d. %s So %s rounds to %s."
            % (PLACE_TO[p], n(x), n(lo), n(lo + 10 ** p), PL[p - 1], look,
               "5 or more, so round up." if look >= 5 else "4 or less, so round down.", n(x), n(r)))


def set_life(P):
    L = [
        mcq_n(fig(line_svg(0, 100000, 10000, [0, 50000, 100000], arrow=70000)) + "What number does the arrow point to?",
              70000, [7000, 60000, 80000],
              "From 0 to 100 000 there are 10 equal spaces, so each space is 10 000. "
              "The arrow is 2 spaces after 50 000: 60 000, 70 000."),
        mcq_n(fig(line_svg(40000, 50000, 1000, [40000, 45000, 50000], arrow=43000))
              + "What number does the arrow point to?", 43000, [40300, 42000, 47000],
              "From 40 000 to 50 000 there are 10 equal spaces, so each space is 1000, not 100. "
              "The arrow is 3 spaces after 40 000: 43 000."),
        mcq_n(fig(line_svg(45000, 46000, 100, [45000, 45500, 46000], arrow=45300))
              + "What number does the arrow point to?", 45300, [45030, 48000, 45700],
              "From 45 000 to 46 000 there are 10 equal spaces, so each space is 100, not 1000. "
              "The arrow is 3 spaces after 45 000: 45 300."),
        mcq_n(fig(line_svg(20000, 30000, 2000, [20000, 30000], arrow=26000)) + "What number does the arrow point to?",
              26000, [23000, 24000, 28000],
              "From 20 000 to 30 000 there are only 5 equal spaces, so each space is 10 000 ÷ 5 = 2000. "
              "The arrow is 3 spaces after 20 000: 22 000, 24 000, 26 000. (23 000 counts each space as 1000.)"),
    ]
    R = []
    for x, p, wrong, extra in [
        (45300, 3, [46000, 50000, 40000], ""),
        (67850, 3, [67000, 70000, 67900], " Do not just drop the hundreds: 67 000 is cutting off, not rounding."),
        (34512, 4, [35000, 40000, 34000], " Round the number you started with. Do not round to 35 000 first."),
        (85096, 4, [80000, 85000, 86000], ""),
        (29961, 2, [29900, 29960, 29000],
         " 9 hundreds + 1 hundred = 10 hundreds = 1 thousand, so 29 900 becomes 30 000."),
    ]:
        r = rnd_to(x, p)
        assert r not in wrong
        R.append(mcq_n("Round %s to the nearest %s." % (n(x), PLACE_TO[p]), r, wrong, round_e(x, p) + extra))
    W = []
    assert rnd_to(34862, 3) == 35000
    W.append(mcq_n("There were 34" + NB + "862 fans at a football game. A news report rounds the crowd to the "
                   "nearest thousand. What number does it report?", 35000, [34000, 30000, 34900],
                   round_e(34862, 3)))
    W.append(mcq("Maple Creek has 18" + NB + "406 people. Pine Bay has 18" + NB + "460 people. "
                 "Which town has more people?", "Pine Bay", ["Maple Creek", "They have the same", "You cannot tell"],
                 compare_expl(18460, 18406) + " Pine Bay has more people."))
    W.append(mcq("Three towns have 27" + NB + "095, 29" + NB + "750 and 27" + NB + "509 people. "
                 "Which list goes from least to greatest?",
                 ", ".join(n(v) for v in [27095, 27509, 29750]),
                 [", ".join(n(v) for v in l) for l in [[27509, 27095, 29750], [29750, 27509, 27095],
                                                       [27095, 29750, 27509]]],
                 "Thousands: 7 &lt; 9, so 29 750 is the greatest. 27 095 and 27 509 both have 7 thousands. "
                 "Hundreds: 0 &lt; 5, so 27 095 &lt; 27 509. Order: 27 095, 27 509, 29 750."))
    W.append(mcq_n("Schools in one city raised forty-five thousand three hundred dollars for the Terry Fox Run. "
                   "Write the amount in numbers.", 45300, [4530, 45030, 450300],
                   words_e(45300) + " The amount is $45 300.", pre="$"))
    name, he, his = P.next()
    W.append(mcq_n("%s’s mystery number has 7 ten thousands, 0 thousands, 4 hundreds, 0 tens and 2 ones. "
                   "What is it?" % name, 70402, [7042, 742, 70420],
                   "Write one digit for each place, with 0 for the empty places: 7, 0, 4, 0, 2. That is 70 402."))
    W.append(mcq("Which is the best estimate for the number of people at a sold-out NHL hockey game?",
                 "about 19" + NB + "000", ["about 190", "about 1900", "about 190" + NB + "000"],
                 "NHL arenas hold about 15 000 to 21 000 people, so about 19 000 is a good estimate. About 190 or 1900 "
                 "is far too few, and 190 000 is more people than live in many Canadian cities."))
    assert rnd_to(56780, 4) == 60000 and rnd_to(54990, 4) == 50000 and rnd_to(65000, 4) == 70000
    W.append(mcq_n("A city’s population, rounded to the nearest ten thousand, is 60" + NB + "000. "
                   "Which could be the real population?", 56780, [54990, 65000, 6500],
                   "Numbers from 55 000 up to 64 999 round to 60 000. 56 780 has 6 thousands, so it rounds up to 60 000. "
                   "54 990 rounds to 50 000, 65 000 rounds up to 70 000, and 6500 is far too small."))
    W.append(mcq_n("A sugar bush has 15" + NB + "000 maple trees. The workers tap them in groups of 1000. "
                   "How many groups is that?", 15, [150, 1500, 5],
                   "15 000 = 15 thousands. So there are 15 groups of 1000. Check: 15 × 1000 = 15 000."))
    assert 15 * 1000 == 15000 and rnd_to(24680, 2) == 24700
    W.append(mcq_n("Volunteers counted 24" + NB + "680 Canada geese at a wetland. Round the count to the nearest "
                   "hundred.", 24700, [24600, 25000, 24000], round_e(24680, 2)))
    assert 89650 + 10000 == 99650
    W.append(mcq_n("A city had 89" + NB + "650 people. Ten years later it has 10" + NB + "000 more people. "
                   "How many people live there now?", 99650, [90650, 89750, 189650],
                   "Adding 10 000 changes the ten thousands digit: 8 ten thousands + 1 = 9 ten thousands. "
                   "89 650 + 10 000 = 99 650. (90 650 adds only 1000.)"))
    name, he, his = P.next()
    assert 25000 + 3 * 10000 == 55000
    W.append(mcq_n("%s’s town has planted 25 000 trees. It plants 10 000 more each year. "
                   "How many trees will it have planted after 3 more years?" % name, 55000, [28000, 35000, 45000],
                   "Count on by 10 000s: 35 000, 45 000, 55 000. After 3 more years the town will have planted "
                   "55 000 trees. (28 000 adds only 3000.)"))
    its = L[:2] + R[:2] + L[2:] + R[2:] + W
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Number lines, rounding and real-life numbers", "items": its}


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
        "<h2>Place value to 100 000</h2>"
        "<p>Each place is worth <b>10 times</b> the place to its right: ones, tens, hundreds, thousands, "
        "ten thousands. Ten ten thousands make <b>100 000</b> (one hundred thousand). "
        "Big numbers are split into groups of three digits. In Canada we leave a small space between the groups "
        "(45 300), not a comma. A 4-digit number has no space (4503).</p>"
        "<figure class='sn-fig'>" + chart_svg(45300, hi=4) +
        "<figcaption>45 300: the 4 is in the ten thousands place, so it is worth 40 000.</figcaption></figure>"
        "<p>Place value disks show the same thing. Find the value of each group, then add.</p>"
        "<figure class='sn-fig'>" + disks_svg([3, 0, 2, 1, 6]) +
        "<figcaption>30 000 + 200 + 10 + 6 = 30 216. There are no thousands, so write 0 there.</figcaption></figure>"
        + ex("Words to digits", "Write forty thousand five hundred three in digits.",
             "Forty thousand → 40. Five hundred three → 503 (always three digits after the space).",
             "40 503 (not 4503)")
        + "<h2>The value of a digit</h2>"
        "<p>The <b>digit</b> is the symbol. Its <b>value</b> depends on its place. In 47 125 the digit 7 is in the "
        "thousands place, so its value is 7000.</p>"
        "<h2>Expanded form and decomposing</h2>"
        "<p><b>Expanded form</b> shows the value of each digit: 68 725 = 60 000 + 8000 + 700 + 20 + 5. "
        "Leave out the zeros: 40 503 = 40 000 + 500 + 3.</p>"
        + ex("Decompose", "Write 45 300 in three ways.",
             "Expanded form: 40 000 + 5000 + 300. It is also 45 thousands and 3 hundreds, or 453 hundreds.",
             "40 000 + 5000 + 300 = 45 thousands + 3 hundreds = 453 hundreds")
        + "<h2>Compare and order</h2>"
        "<p>First count the digits: a 5-digit number is greater than any 4-digit number. If both have the same "
        "number of digits, compare place by place from the left until two digits are different.</p>"
        + ex("Compare", "63 405 ☐ 63 450",
             "Ten thousands: 6 = 6. Thousands: 3 = 3. Hundreds: 4 = 4. Tens: 0 &lt; 5.", "63 405 &lt; 63 450")
        + "<h2>Number lines and rounding</h2>"
        "<p>On a number line, work out the size of each space first. To round, look at the digit "
        "<b>one place to the right</b>: 5 or more rounds up, 4 or less rounds down.</p>"
        "<figure class='sn-fig'>" + line_svg(45000, 46000, 100, [45000, 45500, 46000], arrow=45300, show=True) +
        "<figcaption>Each space is 100. 45 300 is closer to 45 000 than to 46 000, so to the nearest thousand "
        "it rounds to 45 000.</figcaption></figure>"
        + table(["Round 67 850 to the nearest …", "Look at", "Answer"], [
            ["ten thousand", "the thousands digit: 7", "70 000"],
            ["thousand", "the hundreds digit: 8", "68 000"],
            ["hundred", "the tens digit: 5", "67 900"],
        ])
        + "<h2>Big numbers in everyday life</h2>"
        "<p>We see numbers to 100 000 in crowds at hockey and football games, in the populations of towns and "
        "cities, and in money raised for events like the Terry Fox Run. News reports often round them: "
        "34 862 fans becomes “about 35 000 fans”.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving out a zero (forty thousand five hundred three → 4503)",
             "Write three digits after the space: 40 | 503 → 40 503"],
            ["Giving the digit, not its value (the 7 in 47 125 is 7)", "It is in the thousands place: 7000"],
            ["Counting the disks (4 + 5 + 3 = 12)", "Add the values: 40 000 + 5000 + 300 = 45 300"],
            ["Comparing the first digits only (9876 &gt; 10 234)", "Count the digits first: 10 234 &gt; 9876"],
            ["Thinking every space on a number line is 1000", "Work out the space first: 45 000 to 46 000 in 10 spaces is 100 each"],
            ["Rounding twice (34 512 → 35 000 → 40 000)", "Round the number you started with: 30 000"],
        ])
    )


FAQ = [
    {"q": "What number skills are in the Grade 5 Ontario math curriculum?",
     "a": "In Grade 5 students read, represent, compose and decompose whole numbers up to 100 000 (B1.1) and "
          "compare and order them (B1.2). They also describe how big numbers are used in everyday life, "
          "such as crowds, populations and money."},
    {"q": "Why do Canadian students write 45 300 with a space instead of a comma?",
     "a": "Canada follows the SI style: numbers with 5 or more digits are split into groups of three with a small "
          "space, and 4-digit numbers have no space (4503). This avoids mix-ups with the decimal comma used in French."},
    {"q": "How do you write forty thousand five hundred three in numbers?",
     "a": "Write 40 for the thousands part and 503 for the rest: 40 503. The part after the space always has three "
          "digits, so the number is not 4503."},
    {"q": "How do you round a 5-digit number to the nearest thousand?",
     "a": "Look at the hundreds digit. If it is 5 or more, round up; if it is 4 or less, keep the thousands digit "
          "and change the rest to 0. So 67 850 rounds to 68 000 and 45 300 rounds to 45 000."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (45 300) everywhere outside SVG markup."""
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
    """Tag wide pictures (place value charts, disks, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(45802)
    P = People(random.Random(458021))
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "numbers-to-100000", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 100 000: Place Value, Comparing and Rounding",
        "seo_title": "Grade 5 Numbers to 100 000 Math Worksheets: Place Value, Comparing and Rounding (Free, Answer Key)",
        "short_title": "Numbers to 100 000",
        "domain": "Number",
        "standard_code": "Grade 5: B1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compose, and decompose whole numbers up to and including 100" + NB + "000, using appropriate tools and strategies, and describe various ways they are used in everyday life",
        "meta_desc": "Free Grade 5 math worksheets on numbers to 100 000 for the Ontario curriculum: place value, the value of each digit, expanded form, comparing and ordering, number lines and rounding with real-life numbers. 100 questions with an answer key.",
        "key_big": "The place of a digit tells you its value. The 4 in 45 300 is worth 40 000.",
        "key_sub": "Write three digits after the space: forty thousand five hundred three is 40 503, not 4503. To compare, count the digits first, then compare from the left.",
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
