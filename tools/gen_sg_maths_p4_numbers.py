# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Numbers to 100 000
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 4: Whole Numbers —
 numbers up to 100 000: place values, reading and writing, comparing and ordering, patterns)
  python3 tools/gen_sg_maths_p4_numbers.py
Place value to ten thousands (place value charts and discs), reading and writing numbers in numerals and words
(zeros as placeholders), the value of a digit and expanded form, comparing and ordering, and number patterns
(counting on and back in 1000s and 10 000s) with Singapore word problems and bar models.
Numbers: 4-digit numbers have no separator (4503); 5 or more digits use a no-break space (40 503). Never commas.
Words follow Singapore textbooks: "forty thousand, five hundred and three".
Wrong answers come from real mistakes: leaving out zeros (40 503 written 4053 or 4503), giving the digit instead
of its value, counting the discs instead of adding their values, reading fifteen as fifty, comparing the first
digits only, and forgetting to rename when a pattern crosses a ten thousand.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand"]
AB = ["O", "T", "H", "Th", "TTh"]


# ------------------------------------------------------------ helpers
def n(x):
    """MOE style: 4503, 10 000, 40 503 (no-break spaces, never commas)."""
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
    """Value of '30 000 + 4000 + 50 + 2' or '7 × 10 000 + 3 × 100'."""
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


def mcq_w(q, x, wrong, e):
    """Choices in words; every wrong value must differ from x."""
    assert x not in wrong and len(set(wrong)) == 3, (x, wrong)
    return mcq(q, words(x), [words(v) for v in wrong], e)


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


def digit(x, i):
    return (x // 10 ** i) % 10


def ndig(x):
    return len(str(x))


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


# ------------------------------------------------------------ numbers in words (Singapore / British style)
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
    return " and ".join(out)


def words(x):
    """40 503 -> forty thousand, five hundred and three."""
    assert 0 < x <= 100000
    t, o = divmod(x, 1000)
    s = (w1000(t) + " thousand") if t else ""
    if o:
        if not s:
            s = w1000(o)
        elif o < 100:
            s += " and " + w100(o)
        else:
            s += ", " + w1000(o)
    return s


assert words(40503) == "forty thousand, five hundred and three"
assert words(40053) == "forty thousand and fifty-three"
assert words(70045) == "seventy thousand and forty-five"
assert words(62500) == "sixty-two thousand, five hundred"
assert words(100000) == "one hundred thousand"
assert words(4503) == "four thousand, five hundred and three"


def read_e(x):
    """Numeral -> words explanation."""
    t, o = divmod(x, 1000)
    if not t:
        return "%s is “%s”." % (n(x), words(x))
    steps = ["%d → %s thousand" % (t, w1000(t)),
             "%03d → %s" % (o, w1000(o) if o else "nothing more")]
    return ("Split off the last three digits: %d | %03d. Read the thousands, then the rest: %s. "
            "So %s is “%s”." % (t, o, "; ".join(steps), n(x), words(x)))


def write_e(x):
    """Words -> numeral explanation."""
    t, o = divmod(x, 1000)
    steps = ["%s thousand → %d" % (w1000(t), t),
             ("%s → %03d" % (w1000(o), o)) if o else "nothing more → 000"]
    return ("After the thousands, always write three digits: %s. So the number is %s."
            % ("; ".join(steps), n(x)))


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 70, 28, 28, 48


def chart_svg(x, hi=None):
    """Place value chart Thousands (TTh Th) | Ones (H T O) for a number below 100 000. hi = place drawn in red."""
    assert x < 100000
    x0 = y0 = 6
    K = 5
    W, H = 2 * x0 + K * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, K * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, K * CW, H1 + H2, FILL)]
    for k, w, name in [(0, 2, "Thousands"), (2, 3, "Ones")]:
        s.append(text(x0 + k * CW + w * CW / 2.0, y0 + 19, name, 14, bold=True))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0 + 2 * CW, y0, x0 + 2 * CW, y0 + H1 + H2 + ROW, GREEN))
    nd = ndig(x)
    for k in range(K):
        i = K - 1 - k
        xx = x0 + k * CW
        if k not in (0, 2):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (xx, y0 + H1, xx, y0 + H1 + H2 + ROW, GREEN))
        s.append(text(xx + CW / 2.0, y0 + H1 + 19, AB[i], 14, bold=True))
        if i < nd:
            s.append(text(xx + CW / 2.0, y0 + H1 + H2 + 34, str(digit(x, i)), 28, bold=True,
                          col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
             % (x0, y0 + H1, x0 + K * CW, y0 + H1, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + H1 + H2, x0 + K * CW, y0 + H1 + H2, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, K * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % n(x))


DISC_FILL = {4: "#f2d4cf", 3: "#d6e4f4", 2: "#cfe6d6", 1: "#fbe9c0", 0: "#e4e4e4"}
DR = 32          # disc radius (fits “10 000” at 14px)
DG = 4           # gap between discs
GG = 16          # gap between place groups


def discs_svg(counts):
    """Place value discs. counts = [TTh, Th, H, T, O]. Each place is a group of up to 2 columns x 2 rows."""
    assert len(counts) == 5 and all(0 <= c <= 4 for c in counts)
    groups = [(4 - k, c) for k, c in enumerate(counts) if c]
    assert len(groups) <= 4
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
                     % (cx, cy, DR - 1, DISC_FILL[i], INK))
            s.append(text(cx, cy + 5, n(10 ** i), 14, bold=True))
        x += cols * D + (cols - 1) * DG + GG
    value = sum(c * 10 ** (4 - k) for k, c in enumerate(counts))
    return svg_wrap(W, H, "".join(s), "place value discs showing %s" % n(value))


def line_svg(lo, hi, step, labels, arrow=None):
    """Number line lo..hi, a tick every step, numbers at `labels`, red arrow at `arrow`."""
    L, R = 52, 428
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
    for v in labels:
        assert (v - lo) % step == 0 and lo <= v <= hi
    if arrow is not None:
        assert (arrow - lo) % step == 0
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (n(lo), n(hi)))


def bar_svg(rows, total=None, label="bar model"):
    """Singapore bar model, drawn to scale.
    rows = [(name, [(value, dashed)], [(first seg, last seg, text)], right text (optional))];
    total = text for a brace on the right spanning all the rows."""
    LW, BW, BH = 104, 300, 30
    big = max(sum(v for v, _ in r[1]) for r in rows)
    sc = BW / float(big)
    W = LW + BW + (80 if total else 14) + (24 if any(len(r) > 3 for r in rows) else 0)
    y = 6
    s = []
    tops = []
    for row in rows:
        name, segs, over = row[:3]
        y += 24
        tops.append(y)
        s.append(text(LW - 10, y + BH / 2.0 + 5, name, 14, anchor="end", bold=True))
        xs = [LW]
        for v, dashed in segs:
            xs.append(xs[-1] + v * sc)
        for k, (v, dashed) in enumerate(segs):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'%s/>"
                     % (xs[k], y, xs[k + 1] - xs[k], BH, "#fff" if dashed else FILL, INK if not dashed else RED,
                        " stroke-dasharray='5 4'" if dashed else ""))
        for a, b, t in over:
            x1, x2 = xs[a] + 1, xs[b + 1] - 1
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='1.4'/>"
                     % (x1, y - 2, x1, y - 7, x2, y - 7, x2, y - 2, INK))
            s.append(text((x1 + x2) / 2.0, y - 11, t, 14, bold=True, col=RED if t == "?" else INK))
        if len(row) > 3:
            s.append(text(xs[-1] + 10, y + BH / 2.0 + 6, row[3], 16, anchor="start", bold=True, col=RED))
        y += BH + 12
    H = y
    if total:
        xb = LW + BW + 10
        y1, y2 = tops[0], tops[-1] + BH
        ym = (y1 + y2) / 2.0
        s.append("<path d='M%d %d q6 0 6 6 L%d %.1f q0 3 4 3 q-4 0 -4 3 L%d %d q0 6 -6 6' fill='none' "
                 "stroke='%s' stroke-width='1.6'/>" % (xb, y1, xb + 6, ym - 3, xb + 6, y2 - 6, INK))
        s.append(text(xb + 16, ym + 5, total, 14, anchor="start", bold=True, col=RED if total == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


# ============================================================ set 1: place value
def discs_e(counts):
    parts = [(c, 10 ** (4 - k)) for k, c in enumerate(counts)]
    value = sum(c * v for c, v in parts)
    used = ["%d × %s = %s" % (c, n(v), n(c * v)) for c, v in parts if c]
    return "Find the value of each group: %s. Add them: %s. Write 0 in every empty place." % ("; ".join(used), n(value))


def place_e(x, i):
    return ("Read the places from the right: ones, tens, hundreds, thousands, ten thousands. "
            "In %s the red %d is in the %s place." % (n(x), digit(x, i), PL[i]))


def set_place():
    P_ = []
    for x, i in [(52438, 4), (73951, 3), (41527, 2), (93164, 1)]:
        others = [PL[k] for k in sorted(range(5), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        P_.append(mcq(fig(chart_svg(x, hi=i)) + "Which place is the red digit in?", PL[i], others, place_e(x, i)))
    C_ = []
    for x, wrong in [(40503, [4053, 45003, 40530]), (70080, [78, 70800, 7080]), (30604, [3064, 36004, 30640])]:
        C_.append(mcq_n(fig(chart_svg(x)) + "What number does the place value chart show?", x, wrong,
                        "Read the digits from the ten thousands to the ones: %s. Keep every 0: it holds an empty "
                        "place. The number is %s." % (", ".join(str(digit(x, i)) for i in range(4, -1, -1)), n(x))))
    D_ = []
    for counts, wrong in [([3, 2, 0, 0, 0], [5, 3200, 30200]),
                          ([2, 0, 4, 0, 1], [7, 2401, 24001]),
                          ([1, 0, 0, 3, 2], [6, 132, 13002]),
                          ([4, 1, 0, 3, 0], [8, 4130, 41300])]:
        x = sum(c * 10 ** (4 - k) for k, c in enumerate(counts))
        e = discs_e(counts)
        if sum(counts) in wrong:
            e += " Do not just count the discs: each disc has its own value."
        D_.append(mcq_n(fig(discs_svg(counts)) + "What number do the place value discs show?", x, wrong, e))
    G_ = []
    for x, i in [(47532, 3), (60295, 2), (38614, 1)]:
        d = digit(x, i)
        assert len(set(str(x))) == 5
        cands = [str(digit(x, k)) for k in sorted(range(5), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        e = "In %s: %s. The %s digit is %d." % (
            n(x), ", ".join("%s %d" % (PL[k], digit(x, k)) for k in range(4, -1, -1)), PL[i], d)
        G_.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    K_ = [
        mcq_n("How many thousands make 10" + NB + "000?", 10, [100, 1000, 1],
              "Count in thousands: 1000, 2000 … 10 000. That is 10 thousands. "
              "Each place is worth 10 times the place to its right."),
        mcq_n("What number is 1 more than 99" + NB + "999?", 100000, [10000, 99998, 1000000],
              "99 999 + 1: every 9 becomes 0 as you rename, and a 1 goes in the hundred thousands place: "
              "100 000 (one hundred thousand). (99 998 is 1 less.)"),
        mcq_n("What is the greatest 5-digit number?", 99999, [100000, 90000, 9999],
              "Put the greatest digit, 9, in all 5 places: 99 999. 100 000 has 6 digits and 9999 has only 4."),
        mcq_n("What is the smallest 5-digit number?", 10000, [9999, 1000, 11111],
              "A 5-digit number cannot start with 0, so put 1 in the ten thousands place and 0 in all the other "
              "places: 10 000. 9999 has only 4 digits."),
    ]
    assert 10 * 1000 == 10000 and 100 * 100 == 10000 and 99999 + 1 == 100000
    Ph = [
        mcq_n("What number is 3 ten thousands, 4 thousands and 5 tens?", 34050, [345, 34500, 3450],
              "30 000 + 4000 + 50 = 34 050. Write a digit for every place: 3, 4, 0, 5, 0."),
        mcq_n("What number is 6 ten thousands, 7 hundreds and 2 ones?", 60702, [672, 67002, 6702],
              "60 000 + 700 + 2 = 60 702. There are no thousands or tens, so write 0 in those places."),
    ]
    assert 30000 + 4000 + 50 == 34050 and 60000 + 700 + 2 == 60702
    its = P_[:2] + C_[:1] + K_[:1] + D_[:1] + G_[:1] + P_[2:3] + D_[1:2] + C_[1:2] + G_[1:2] \
        + K_[2:3] + P_[3:] + D_[2:3] + Ph[:1] + G_[2:] + K_[3:4] + D_[3:] + C_[2:] + Ph[1:] + K_[1:2]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Place value to 100 000", "items": its}


# ============================================================ set 2: numerals and words
def set_words():
    R = []
    for x, wrong, extra in [
        (30000, [3000, 13000, 300], " 30 000 is 30 thousands. Thirty is 30; thirteen is 13."),
        (45000, [4500, 40500, 40005], ""),
        (40503, [4503, 45003, 40530], " The 0s hold empty places: 40 thousands, then 503."),
        (70045, [7045, 70450, 70405], ""),
        (62500, [6250, 62050, 60250], ""),
        (18300, [80300, 18030, 1830], " Eighteen is 18, not 80."),
        (15015, [50015, 15050, 15150], " Fifteen is 15; fifty is 50."),
        (90909, [99009, 90990, 9909], ""),
    ]:
        R.append(mcq_w("How do you write %s in words?" % n(x), x, wrong, read_e(x) + extra))
    W = []
    for x, wrong, extra in [
        (40000, [4000, 400000, 400], " Forty thousand is 40 thousands: 40 followed by 000."),
        (40503, [4053, 45003, 4503], " 4053 and 4503 leave out a zero that holds an empty place."),
        (70025, [7025, 70250, 725], ""),
        (19500, [90500, 1950, 10950], " Nineteen is 19; ninety is 90."),
        (30401, [3401, 34001, 30410], ""),
        (80080, [8080, 88000, 80800], ""),
        (12012, [1212, 12120, 120012], " Twelve thousand is 12 | 000, and twelve is 012 after it."),
    ]:
        W.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, wrong, write_e(x) + extra))
    W.append(mcq_n("Which number is <b>one hundred thousand</b>?", 100000, [10000, 1000000, 1000],
                   "One hundred thousand is 100 thousands: 100 | 000 = 100 000. It is 1 more than 99 999. "
                   "(10 000 is ten thousand.)"))
    M = []
    for x, q, ans, wrong in [
        (60300, "sixty thousand, ☐ hundred", "three", ["thirty", "thirteen", "zero"]),
        (24050, "twenty-four thousand and ☐", "fifty", ["five", "five hundred", "fifteen"]),
    ]:
        assert words(x) == q.replace("☐", ans)
        M.append(mcq("%s = %s. Which word goes in the box?" % (n(x), q), ans, wrong, read_e(x)))
    nums = [30045, 30450, 34500, 30405]
    Z = [mcq("Which number is read <b>without</b> the word “hundred”?", n(30045), [n(v) for v in nums[1:]],
             "%s has 0 in the hundreds place, so we do not say “hundred”: %s. The others: %s."
             % (n(30045), words(30045), "; ".join("%s is %s" % (n(v), words(v)) for v in nums[1:])))]
    assert all("hundred" in words(v) for v in nums[1:]) and "hundred" not in words(30045)
    Ch = [mcq_n("Chloe writes “fifty thousand and six” as 5006. What should she write?", 50006,
                [5006, 50060, 56],
                "Fifty thousand is 50 | 000. Six goes in the ones place: 50 | 006 = 50 006. "
                "5006 is only five thousand and six: Chloe left out a zero.")]
    assert words(50006) == "fifty thousand and six" and words(5006) == "five thousand and six"
    its = R[:2] + W[:2] + R[2:3] + W[2:3] + M[:1] + R[3:4] + W[3:4] + W[7:8] + R[4:5] + W[4:5] + Z \
        + R[5:6] + W[5:6] + M[1:] + R[6:7] + Ch + W[6:7] + R[7:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Reading and writing numbers in words", "items": its}


# ============================================================ set 3: value of a digit and expanded form
def value_cands(d, i):
    """The digit itself and its value in the two nearest other places (tens or more)."""
    near = [k for k in sorted(range(1, 5), key=lambda k: (abs(k - i), -k)) if k != i][:2]
    return [d] + [d * 10 ** k for k in near]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), n(v), d, n(v)))


def expand(x):
    return " + ".join(n(digit(x, i) * 10 ** i) for i in range(4, -1, -1) if digit(x, i))


def set_value():
    A = []
    for x, i in [(48361, 4), (25943, 3), (71628, 2), (39574, 1)]:
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    B = []
    for x, d in [(37845, 7), (52469, 4), (94136, 9), (61287, 8)]:
        assert str(x).count(str(d)) == 1
        i = ndig(x) - 1 - str(x).index(str(d))
        B.append(mcq_n("What is the value of the %d in %s?" % (d, n(x)), d * 10 ** i, value_cands(d, i),
                       value_e(d, i)))
    S = []
    for x, d in [(28307, 3), (65432, 6)]:
        i = ndig(x) - 1 - str(x).index(str(d))
        others = [plural(d, k) for k in sorted(range(5), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        S.append(mcq("In %s, the digit %d stands for ☐." % (n(x), d), plural(d, i), others,
                     "Count the places from the right: ones, tens, hundreds, thousands, ten thousands. "
                     "The %d is in the %s place, so it stands for %s = %s." % (d, PL[i], plural(d, i), n(d * 10 ** i))))
    T = [mcq_n("In 44" + NB + "000, the first 4 is worth how many times the second 4?", 10, [100, 4, 36000],
               "The first 4 is in the ten thousands place: 40 000. The second 4 is in the thousands place: 4000. "
               "40 000 ÷ 4000 = 10. (36 000 is the difference, not how many times.)")]
    assert 40000 // 4000 == 10
    E = []
    x = 62708
    E.append(mcq("Which shows 62" + NB + "708 in expanded form?", expand(x),
                 ["60" + NB + "000 + 2000 + 70 + 8", "6000 + 200 + 70 + 8", "60" + NB + "000 + 2000 + 700 + 80"],
                 "Write the value of each digit: 6 ten thousands = 60 000, 2 thousands = 2000, 7 hundreds = 700, "
                 "0 tens, 8 ones = 8. So 62 708 = %s. The 0 tens is left out." % expand(x)))
    assert xval(expand(x)) == x and xval("60000+2000+70+8") != x
    E.append(mcq_n("40" + NB + "503 = 40" + NB + "000 + ☐ + 3. What number goes in the box?", 500, [5, 50, 5000],
                   "40 503 = 40 000 + 500 + 3. The 5 is in the hundreds place, so its value is 500."))
    E.append(mcq_n("56" + NB + "024 = 50" + NB + "000 + 6000 + ☐ + 4. What number goes in the box?", 20,
                   [2, 200, 24],
                   "The 2 is in the tens place, so its value is 20. 50 000 + 6000 + 20 + 4 = 56 024."))
    E.append(mcq_n("What number is <b>30" + NB + "000 + 4000 + 50 + 2</b>?", 34052, [3452, 34502, 30452],
                   "Put each value in its place: 3 ten thousands, 4 thousands, 0 hundreds, 5 tens, 2 ones → 34 052."))
    E.append(mcq_n("What number is <b>90" + NB + "000 + 800 + 1</b>?", 90801, [981, 98001, 90810],
                   "9 ten thousands, 0 thousands, 8 hundreds, 0 tens, 1 one → 90 801. "
                   "Write 0 in every empty place."))
    E.append(mcq_n("What number is <b>7 × 10" + NB + "000 + 3 × 100 + 6 × 1</b>?", 70306, [736, 73006, 70360],
                   "7 × 10 000 = 70 000, 3 × 100 = 300, 6 × 1 = 6. Add them: 70 306."))
    assert 40000 + 500 + 3 == 40503 and 50000 + 6000 + 20 + 4 == 56024
    assert xval("30000 + 4000 + 50 + 2") == 34052 and xval("90000+800+1") == 90801
    assert xval("7 × 10000 + 3 × 100 + 6 × 1") == 70306
    Rn = [
        mcq_n("52" + NB + "000 = ☐ thousands. What number goes in the box?", 52, [520, 5200, 5],
              "52 000 = 52 × 1000, so it is 52 thousands."),
        mcq_n("30" + NB + "400 = ☐ hundreds. What number goes in the box?", 304, [34, 3040, 3004],
              "30 400 = 304 × 100, so it is 304 hundreds. (30 000 is 300 hundreds, plus 4 hundreds.)"),
        mcq_n("How many tens are there in 4500?", 450, [45, 4500, 405],
              "4500 = 450 × 10, so there are 450 tens. (45 is the number of hundreds.)"),
    ]
    assert 52 * 1000 == 52000 and 304 * 100 == 30400 and 450 * 10 == 4500
    its = B[:2] + A[:1] + E[1:2] + B[2:3] + A[1:2] + S[:1] + E[3:4] + B[3:] + A[2:3] + E[:1] + E[4:5] + S[1:] \
        + A[3:] + E[2:3] + Rn[:1] + E[5:] + T + Rn[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Value of a digit and expanded form", "items": its}


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
    C = []
    for x, y in [(54300, 54030), (9876, 10234), (30605, 30650), (79999, 80001), (60060, 60600), (45678, 45687)]:
        lt, gt = "&lt;", "&gt;"
        right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
        wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
                 "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 9876:
            e += " A big first digit does not matter when a number has fewer digits."
        C.append(mcq("Which is true?", right, wrong, e))
    G = []
    for nums, want_max in [([24653, 24563, 24635, 24536], True),
                           ([9999, 10001, 10010, 10100], False),
                           ([60809, 60089, 68009, 6809], True),
                           ([35120, 35210, 32510, 35102], False)]:
        s = sorted(nums)
        ans, nxt = (s[-1], s[-2]) if want_max else (s[0], s[1])
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % n(ans)
        elif ndig(ans) != ndig(nxt):
            e = ("%s has only %d digits. The other numbers have %d digits, so %s is the least, even though it "
                 "starts with 9." % (n(ans), ndig(ans), ndig(nxt), n(ans)))
        else:
            e = compare_expl(nxt, ans).replace("So %s &gt; %s." % (n(nxt), n(ans)),
                                               "So %s &lt; %s." % (n(ans), n(nxt))) + " %s is the least." % n(ans)
        G.append(mcq("Which number is the %s?" % ("greatest" if want_max else "least"), n(ans),
                     [n(v) for v in nums if v != ans], e))
    fmt = lambda l: ", ".join(n(v) for v in l)
    O = []
    for nums, up, perms, e in [
        ([45300, 43500, 45030], True, [[45030, 43500, 45300], [45300, 45030, 43500], [43500, 45300, 45030]],
         "All have 4 ten thousands. Thousands: 3 &lt; 5, so 43 500 is the least. 45 300 and 45 030 both have "
         "5 thousands. Hundreds: 0 &lt; 3, so 45 030 &lt; 45 300."),
        ([12100, 12010, 11200], False, [[11200, 12010, 12100], [12010, 12100, 11200], [12100, 11200, 12010]],
         "All have 1 ten thousand. Thousands: 1 &lt; 2, so 11 200 is the least. 12 100 and 12 010 both have "
         "2 thousands. Hundreds: 1 &gt; 0, so 12 100 &gt; 12 010."),
        ([99000, 100000, 90900, 9900], True, [[9900, 99000, 90900, 100000], [100000, 99000, 90900, 9900],
                                              [90900, 9900, 99000, 100000]],
         "9900 has only 4 digits, so it is the least. 100 000 has 6 digits, so it is the greatest. "
         "90 900 &lt; 99 000 (thousands: 0 &lt; 9)."),
        ([60606, 66060, 60660, 66006], False, [[66006, 66060, 60660, 60606], [60606, 60660, 66006, 66060],
                                               [66060, 66006, 60606, 60660]],
         "Thousands: 66 060 and 66 006 have 6 thousands; the others have 0. 66 060 and 66 006: hundreds 0 = 0, "
         "tens 6 &gt; 0, so 66 060 &gt; 66 006. 60 660 and 60 606: hundreds 6 = 6, tens 6 &gt; 0, "
         "so 60 660 &gt; 60 606."),
    ]:
        o = sorted(nums) if up else sorted(nums)[::-1]
        assert all(p != o and sorted(p) == sorted(o) for p in perms)
        assert len({tuple(p) for p in perms}) == 3
        O.append(mcq("Put %s in order from %s." % (fmt(nums), "least to greatest" if up else "greatest to least"),
                     fmt(o), [fmt(p) for p in perms], e + " Order: %s." % fmt(o)))
    Dg = [
        mcq_n("Use each of the digits 3, 8, 1, 6 and 0 once. What is the greatest number you can make?", 86310,
              [86301, 10368, 68310],
              "Put the greatest digit in the ten thousands place, then the next greatest, and so on: "
              "8, 6, 3, 1, 0. The greatest number is 86 310."),
        mcq_n("Use each of the digits 3, 8, 1, 6 and 0 once. What is the smallest 5-digit number you can make?",
              10368, [1368, 13068, 86310],
              "A 5-digit number cannot start with 0. Put the smallest other digit first: 1. Then 0, 3, 6, 8: "
              "10 368. (01 368 is just 1368, which has only 4 digits.)"),
        mcq_n("Use each of the digits 5, 0, 7, 0 and 2 once. What is the smallest 5-digit number you can make?",
              20057, [257, 20075, 25007],
              "The first digit cannot be 0, so start with the smallest other digit: 2. Then put both 0s, then "
              "5 and 7: 20 057."),
    ]
    assert int("".join(sorted("38160", reverse=True))) == 86310
    Bt = [
        mcq_n("Which number is between 45" + NB + "900 and 46" + NB + "100?", 46000, [45090, 46900, 4600],
              "45 900 &lt; 46 000 &lt; 46 100. 45 090 is less than 45 900, 46 900 is more than 46 100, "
              "and 4600 has only 4 digits."),
        mcq_n("Which number is greater than 89" + NB + "000 but less than 90" + NB + "000?", 89500,
              [98000, 8950, 90500],
              "89 500 has 8 ten thousands and 9 thousands, so it is between 89 000 and 90 000. "
              "98 000 and 90 500 are more than 90 000; 8950 is less than 89 000."),
        mcq_n("What is the greatest 5-digit number that is less than 50" + NB + "000?", 49999,
              [50001, 49000, 4999],
              "Go back 1 from 50 000: 49 999. 50 001 is more than 50 000, 49 000 is not the greatest, "
              "and 4999 has only 4 digits."),
    ]
    assert 45900 < 46000 < 46100 and 89000 < 89500 < 90000 and 50000 - 1 == 49999
    its = C[:2] + G[:1] + C[2:3] + Bt[:1] + G[1:2] + C[3:4] + O[:1] + C[4:5] + Dg[:1] + G[2:3] + Bt[1:2] \
        + O[1:2] + C[5:] + Dg[1:2] + G[3:] + O[2:3] + Bt[2:] + Dg[2:] + O[3:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Comparing and ordering numbers", "items": its}


# ============================================================ set 5: number patterns and word problems
def seq(a, step, k=4):
    return [a + j * step for j in range(k)]


def set_patterns():
    S = {}
    # next number in a pattern
    for key, a, step, wrong, e in [
        ("p1", 23400, 1000, [25500, 35400, 27400],
         "Each number is 1000 more: the thousands digit goes up by 1. 25 400 + 1000 = 26 400."),
        ("p2", 15070, 10000, [36070, 45170, 55070],
         "Each number is 10 000 more: the ten thousands digit goes up by 1. 35 070 + 10 000 = 45 070."),
        ("p3", 82360, -10000, [42360, 62260, 61360],
         "Each number is 10 000 less: the ten thousands digit goes down by 1. 62 360 − 10 000 = 52 360."),
        ("p4", 30200, -1000, [28100, 18200, 26200],
         "Each number is 1000 less: the thousands digit goes down by 1. 28 200 − 1000 = 27 200. "
         "(28 100 takes away 100, and 18 200 takes away 10 000.)"),
        ("p5", 47500, 1000, [40500, 49600, 59500],
         "Each number is 1000 more. 49 500 + 1000 = 50 500: 10 thousands are renamed as 1 ten thousand. "
         "(40 500 forgets to rename.)"),
    ]:
        s = seq(a, step)
        q = "What is the next number in the pattern?<br><b>%s, %s, %s, ☐</b>" % (n(s[0]), n(s[1]), n(s[2]))
        S[key] = mcq_n(q, s[3], wrong, e)
    s = seq(61800, 1000)
    S["mid1"] = mcq_n("What is the missing number?<br><b>%s, ☐, %s, %s</b>" % (n(s[0]), n(s[2]), n(s[3])), s[1],
                      [61900, 71800, 62900],
                      "From 63 800 to 64 800 is 1000 more, so the rule is “add 1000”. 61 800 + 1000 = 62 800.")
    s = seq(90450, -10000)
    S["mid2"] = mcq_n("What is the missing number?<br><b>%s, %s, ☐, %s</b>" % (n(s[0]), n(s[1]), n(s[3])), s[2],
                      [7450, 79450, 70350],
                      "Each number is 10 000 less: 90 450, 80 450, 70 450, 60 450. Only the ten thousands digit "
                      "changes. (79 450 takes away 1000.)")
    S["more"] = mcq_n("What number is 1000 more than 39" + NB + "650?", 40650, [30650, 39750, 49650],
                      "39 650 + 1000: 9 thousands + 1 thousand = 10 thousands. Rename them as 1 ten thousand: "
                      "3 ten thousands become 4. 39 650 + 1000 = 40 650. (49 650 adds 10 000.)")
    S["less"] = mcq_n("What number is 10" + NB + "000 less than 100" + NB + "000?", 90000, [99000, 9000, 80000],
                      "100 000 is 10 ten thousands. Take away 1 ten thousand: 9 ten thousands = 90 000. "
                      "(99 000 takes away only 1000.)")
    S["rule"] = mcq("What is the rule for this pattern?<br><b>56" + NB + "300, 54" + NB + "300, 52" + NB + "300, 50"
                    + NB + "300</b>", "Subtract 2000", ["Add 2000", "Subtract 200", "Subtract 20" + NB + "000"],
                    "The numbers get smaller, so we subtract. 56 300 − 54 300 = 2000. The thousands digit goes "
                    "down by 2 each time. The rule is “subtract 2000”.")
    assert 56300 - 54300 == 2000 and 52300 - 2000 == 50300
    S["line1"] = mcq_n(fig(line_svg(40000, 50000, 1000, [40000, 45000, 50000], arrow=47000))
                       + "What number does the arrow point to?", 47000, [40700, 46000, 48000],
                       "From 40 000 to 50 000 there are 10 equal spaces, so each space is 1000. The arrow is "
                       "2 spaces after 45 000: 46 000, 47 000. (40 700 counts each space as 100.)")
    S["line2"] = mcq_n(fig(line_svg(0, 100000, 10000, [0, 50000, 100000], arrow=70000))
                       + "What number does the arrow point to?", 70000, [7000, 60000, 80000],
                       "From 0 to 100 000 there are 10 equal spaces, so each space is 10 000. The arrow is 2 spaces "
                       "after 50 000: 60 000, 70 000. (7000 counts each space as 1000.)")
    # ---- word problems
    S["hafiz"] = mcq_n("Hafiz counts back in ten thousands: 95" + NB + "200, 85" + NB + "200, … "
                       "What is the 4th number he says?", 65200, [75200, 55200, 92200],
                       "95 200 (1st), 85 200 (2nd), 75 200 (3rd), 65 200 (4th). Each time the ten thousands digit "
                       "goes down by 1. (92 200 counts back in thousands.)")
    S["library"] = mcq_n("A library has 46" + NB + "800 books. It buys 1000 new books every month. How many "
                         "books will it have after 3 months?", 49800, [47800, 46803, 76800],
                         "Count on in thousands 3 times: 47 800, 48 800, 49 800. (47 800 is after only 1 month, "
                         "and 76 800 adds 3 ten thousands.)")
    assert 46800 + 3 * 1000 == 49800
    S["compare"] = mcq("Ali’s school library has 12" + NB + "450 books. Wei Ming’s school library has 12" + NB
                       + "540 books. Which is true?", "Wei Ming’s library has more books",
                       ["Ali’s library has more books", "They have the same number of books",
                        "You cannot tell which has more"],
                       compare_expl(12540, 12450) + " Wei Ming’s library has more books.")
    S["run"] = mcq_n("A charity run had 9000 runners in its 1st year. Each year after that, it had 1000 more "
                     "runners than the year before. How many runners were there in the 5th year?", 13000,
                     [14000, 12000, 9005],
                     "1st year 9000, 2nd 10 000, 3rd 11 000, 4th 12 000, 5th 13 000. From the 1st year to the "
                     "5th year there are only 4 jumps of 1000. (14 000 adds 5 jumps.)")
    assert 9000 + 4 * 1000 == 13000
    S["savings"] = mcq_n("Mr Tan had $25" + NB + "000 in the bank. He took out $1000 every month for 4 months. "
                         "How much money did he have left?", 21000, [24000, 29000, 24996],
                         "Count back in thousands 4 times: $24 000, $23 000, $22 000, $21 000. "
                         "($24 996 takes away $4 instead of $4000.)", pre="$")
    assert 25000 - 4 * 1000 == 21000
    # ---- bar models
    S["cans"] = mcq_n(fig(bar_svg([("School A", [(38500, False)], [(0, 0, n(38500))]),
                                   ("School B", [(38500, False), (10000, False)], [(1, 1, n(10000))], "?")],
                                  label="bar model: School A and School B"))
                      + "For a recycling drive, School A collected 38" + NB + "500 cans. School B collected "
                        "10" + NB + "000 more cans than School A. How many cans did School B collect?",
                      48500, [28500, 39500, 38510],
                      "School B’s bar is School A’s bar plus 10 000. 38 500 + 10 000 = 48 500: the ten thousands "
                      "digit goes up by 1. (28 500 subtracts, and 39 500 adds only 1000.)")
    assert 38500 + 10000 == 48500
    S["gardens"] = mcq_n(fig(bar_svg([("Saturday", [(64300, False)], [(0, 0, n(64300))]),
                                      ("Friday", [(54300, False), (10000, True)], [(0, 0, n(54300)), (1, 1, "?")])],
                                     label="bar model comparing Saturday and Friday"))
                         + "A park had 64" + NB + "300 visitors on Saturday and 54" + NB + "300 visitors on Friday. "
                           "How many more visitors were there on Saturday?", 10000, [1000, 118600, 100],
                         "The difference is the part marked ?. 64 300 − 54 300 = 10 000: only the ten thousands "
                         "digit is different (6 and 5). (118 600 adds the numbers.)")
    assert 64300 - 54300 == 10000
    S["masks"] = mcq_n(fig(bar_svg([("Masks", [(20000, False), (50000, True)], [(0, 0, n(20000)), (1, 1, "?")])],
                                   total=n(70000), label="bar model: 70 000 masks, 20 000 given out"))
                       + "A community centre had 70" + NB + "000 face masks. It gave out 20" + NB + "000 masks "
                         "to residents. How many masks were left?", 50000, [90000, 68000, 5000],
                       "The whole bar is 70 000 and one part is 20 000. 70 000 − 20 000 = 50 000 (7 ten thousands − "
                       "2 ten thousands = 5 ten thousands). (90 000 adds, and 68 000 takes away only 2000.)")
    assert 70000 - 20000 == 50000
    order = ["p1", "p2", "more", "p3", "line1", "p4", "less", "mid1", "line2", "p5", "rule", "mid2",
             "compare", "library", "hafiz", "cans", "savings", "gardens", "masks", "run"]
    assert sorted(order) == sorted(S) and len(order) == 20
    its = [S[k] for k in order]
    return {"title": "Number patterns and word problems", "items": its}


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
        "<h2>Place value to 100 000</h2>"
        "<p>Each place is worth <b>10 times</b> the place to its right. After the thousands comes the "
        "<b>ten thousands</b> place. 10 thousands make 10 000, and 10 ten thousands make 100 000 "
        "(one hundred thousand).</p>"
        "<p>In a place value chart, TTh = ten thousands, Th = thousands, H = hundreds, T = tens and O = ones.</p>"
        "<figure class='sn-fig'>" + chart_svg(40503, hi=2) +
        "<figcaption>40 503: the 5 is in the hundreds place, so it is worth 500. "
        "The zeros hold the empty places.</figcaption></figure>"
        "<p>Place value discs show the same idea. Find the value of each group of discs, then add.</p>"
        "<figure class='sn-fig'>" + discs_svg([3, 0, 2, 0, 1]) +
        "<figcaption>30 000 + 200 + 1 = 30 201.</figcaption></figure>"
        "<h2>Reading and writing numbers in words</h2>"
        "<p>Split off the last three digits. Read the thousands first and say “thousand”. "
        "Then read the last three digits. After the thousands, a numeral always has <b>three more digits</b>, "
        "so use 0 to hold an empty place.</p>"
        + table(["Numerals", "Words"], [
            [n(40503), words(40503)],
            [n(70045), words(70045)],
            [n(62500), words(62500)],
            [n(100000), words(100000)],
        ])
        + ex("Words to numerals", "Write fifty thousand and six in numerals.",
             "fifty thousand → 50; six → 006.",
             "50 006 (not 5006)")
        + "<h2>Value of a digit and expanded form</h2>"
        "<p>The <b>digit</b> is the symbol. Its <b>value</b> depends on its place. In 37 845 the digit 7 is in "
        "the thousands place, so its value is 7000, not 7.</p>"
        "<p>Expanded form shows the value of every digit: 62 708 = 60 000 + 2000 + 700 + 8.</p>"
        "<h2>Comparing and ordering</h2>"
        "<p>First count the digits: a 5-digit number is greater than any 4-digit number. If the numbers have the "
        "same number of digits, compare place by place from the left until two digits are different.</p>"
        + ex("Compare", "30 605 ☐ 30 650",
             "Ten thousands: 3 = 3. Thousands: 0 = 0. Hundreds: 6 = 6. Tens: 0 &lt; 5.",
             "30 605 &lt; 30 650")
        + "<h2>Number patterns</h2>"
        "<p>To count on in thousands, add 1 to the thousands digit. To count on in ten thousands, add 1 to the "
        "ten thousands digit. When the thousands go past 9, rename 10 thousands as 1 ten thousand.</p>"
        + ex("Count on in thousands", "47 500, 48 500, 49 500, ☐",
             "49 500 + 1000: 9 thousands + 1 thousand = 10 thousands = 1 ten thousand.",
             "50 500")
        + "<p>In word problems, draw a bar model to see what to find.</p>"
        "<figure class='sn-fig'>" + bar_svg([("School A", [(38500, False)], [(0, 0, n(38500))]),
                                            ("School B", [(38500, False), (10000, False)], [(1, 1, n(10000))], "?")],
                                           label="bar model: School A and School B") +
        "<figcaption>School B collected 10 000 more cans than School A. "
        "38 500 + 10 000 = 48 500.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving out zeros (forty thousand, five hundred and three → 4053 or 4503)",
             "Write three digits after the thousands: 40 | 503 → 40 503"],
            ["Giving the digit, not its value (the 7 in 37 845 is 7)",
             "It is in the thousands place: 7000"],
            ["Counting the discs (3 + 2 + 1 = 6)", "Add the values: 30 000 + 200 + 1 = 30 201"],
            ["Comparing the first digits only (9876 &gt; 10 234)",
             "Count the digits first: 10 234 &gt; 9876"],
            ["Forgetting to rename in a pattern (49 500 + 1000 → 40 500)",
             "10 thousands make 1 ten thousand: 50 500"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 whole numbers?",
     "a": "Primary 4 students read and write numbers up to 100 000 in numerals and in words, find the value of "
          "each digit, compare and order numbers, and continue number patterns. They also round numbers and learn "
          "factors and multiples."},
    {"q": "How do you write forty thousand, five hundred and three in numerals?",
     "a": "Write 40 for the thousands and 503 for the rest: 40 503. After the thousands there must always be three "
          "digits, so zeros hold the empty places."},
    {"q": "What is the most common mistake with numbers to 100 000?",
     "a": "The most common mistake is leaving out zeros, such as writing 40 503 as 4053. Another is giving the "
          "digit instead of its value: the 7 in 37 845 is worth 7000."},
    {"q": "Is numbers to 100 000 in the MOE syllabus?",
     "a": "Yes. Numbers up to 100 000, including place value, reading and writing, comparing and ordering, and "
          "number patterns, are part of Whole Numbers in the MOE 2021 Primary 4 Mathematics syllabus."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (40 503) everywhere outside SVG markup."""
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
    """Tag wide pictures (place value charts, discs, number lines, bar models) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64801)
    sets = [set_place(), set_words(), set_value(), set_compare(), set_patterns()]
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
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "numbers-to-100000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Numbers to 100 000",
        "seo_title": "P4 Numbers to 100 000 Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Numbers to 100 000",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Numbers up to 100 000: place values, reading and writing, comparing and ordering, patterns",
        "meta_desc": "Free P4 maths practice on numbers to 100 000: place value, numerals and words, expanded form, "
                     "comparing, ordering and patterns. 100 questions with answers.",
        "key_big": "After the thousands, always write three digits: forty thousand and six is 40 006.",
        "key_sub": "In 37 845 the digit 7 is in the thousands place, so its value is 7000.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(fix_spaces(u), "(number line|place value chart|place value discs|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
