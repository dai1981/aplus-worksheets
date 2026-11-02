# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Numbers to 10 Million
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 5: Whole Numbers —
 reading and writing numbers up to 10 million in numerals and in words)
  python3 tools/gen_sg_maths_p5_numbers.py
Place value to millions (place value charts and discs), reading numbers in words, writing numerals from words
(zeros as placeholders), the value of a digit, comparing and ordering, and numbers in Singapore life with bar models.
Numbers: 4-digit numbers have no separator (4503); 5 or more digits use a no-break space (2 040 006). Never commas.
Words follow Singapore textbooks: "two million, forty thousand and six".
Wrong answers come from real mistakes: leaving out zeros (2 040 006 written 246 or 2 400 006), giving the digit
instead of its value, counting the discs instead of adding their values, reading fifteen as fifty, saying a
"thousand" when the thousands group is 000, comparing the first digits only, and the classic subtraction slips.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions", "ten millions"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million", "ten million"]
AB = ["O", "T", "H", "Th", "TTh", "HTh", "M"]


# ------------------------------------------------------------ helpers
def n(x):
    """MOE style: 4503, 10 000, 2 040 006 (no-break spaces, never commas)."""
    s = str(x)
    if len(s) <= 4:
        return s
    g = []
    while s:
        g.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(g)


def d_(x):
    return "$" + n(x)


NUM = re.compile(r"^(\$)?(\d+)( .+)?$")


def val(c):
    """Value of a choice that is a single number (None otherwise)."""
    c = re.sub(r"(?<=\d)" + NB + r"(?=\d)", "", c)
    m = NUM.match(c)
    if not m:
        return None
    return (F(m.group(2)), "$" if m.group(1) else (m.group(3) or "").strip())


def xval(s):
    """Value of '5 000 000 + 30 000 + 2' or '8 × 1 000 000 + 6 × 10'."""
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
    """2 040 006 -> two million, forty thousand and six."""
    assert 0 < x < 1000000000
    m, rest = divmod(x, 1000000)
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


assert words(2040006) == "two million, forty thousand and six"
assert words(5000300) == "five million, three hundred"
assert words(7000045) == "seven million and forty-five"
assert words(9205060) == "nine million, two hundred and five thousand and sixty"
assert words(3470512) == "three million, four hundred and seventy thousand, five hundred and twelve"
assert words(10000000) == "ten million"


def grp(x):
    """'2 | 040 | 006' (groups of three from the right)."""
    s = str(x)
    g = []
    while s:
        g.insert(0, s[-3:])
        s = s[:-3]
    return " | ".join(g)


def read_e(x):
    """Numeral -> words explanation."""
    m, rest = divmod(x, 1000000)
    t, o = divmod(rest, 1000)
    steps = []
    if m:
        steps.append("%d → %s million" % (m, w1000(m)))
    if m or t:
        steps.append("%03d → %s" % (t, (w1000(t) + " thousand") if t else "no thousands, so do not say “thousand”"))
    steps.append("%03d → %s" % (o, w1000(o) if o else "nothing"))
    return ("Split the number into groups of three from the right: %s. Read each group with its name: %s. "
            "So %s is “%s”." % (grp(x), "; ".join(steps), n(x), words(x)))


def write_e(x):
    """Words -> numeral explanation."""
    m, rest = divmod(x, 1000000)
    t, o = divmod(rest, 1000)
    steps = []
    if m:
        steps.append("%s million → %d" % (w1000(m), m))
    steps.append(("%s thousand → %03d" % (w1000(t), t)) if t else "no thousands → 000")
    steps.append(("%s → %03d" % (w1000(o), o)) if o else "nothing more → 000")
    return ("Write every group after the millions with three digits: %s. So the number is %s."
            % ("; ".join(steps), n(x)))


# ------------------------------------------------------------ figures
CW, H1, H2, ROW = 70, 28, 28, 48


def chart_svg(x, hi=None):
    """Place value chart M | HTh TTh Th | H T O with a number below 10 000 000. hi = place drawn in red."""
    assert x < 10000000
    x0 = y0 = 6
    W, H = 2 * x0 + 7 * CW, 2 * y0 + H1 + H2 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, 7 * CW, H1 + H2 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 7 * CW, H1 + H2, FILL)]
    for k, w, name in [(0, 1, "Millions"), (1, 3, "Thousands"), (4, 3, "Ones")]:
        s.append(text(x0 + k * CW + w * CW / 2.0, y0 + 19, name, 14, bold=True))
    for k in (1, 4):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + k * CW, y0, x0 + k * CW, y0 + H1 + H2 + ROW, GREEN))
    nd = ndig(x)
    for k in range(7):
        i = 6 - k
        xx = x0 + k * CW
        if k not in (0, 1, 4):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (xx, y0 + H1, xx, y0 + H1 + H2 + ROW, GREEN))
        s.append(text(xx + CW / 2.0, y0 + H1 + 19, AB[i], 14, bold=True))
        if i < nd:
            s.append(text(xx + CW / 2.0, y0 + H1 + H2 + 34, str(digit(x, i)), 28, bold=True,
                          col=RED if hi == i else INK))
    for y in (y0 + H1, y0 + H1 + H2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x0 + CW if y == y0 + H1 else x0, y, x0 + 7 * CW, y, GREEN, "1.2" if y == y0 + H1 else "2"))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, 7 * CW, H1 + H2 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % n(x))


DISC_FILL = {6: "#f6dcc0", 5: "#e8d6f0", 4: "#f2d4cf", 3: "#d6e4f4", 2: "#cfe6d6", 1: "#fbe9c0", 0: "#e4e4e4"}
DR = 45          # disc radius (fits “1 000 000” at 14px)
DG = 4           # gap between discs
GG = 18          # gap between place groups


def discs_svg(counts):
    """Place value discs. counts = [M, HTh, TTh, Th, H, T, O]. Each place is a group of up to 2 columns x 2 rows."""
    assert len(counts) == 7 and all(0 <= c <= 4 for c in counts)
    groups = [(6 - k, c) for k, c in enumerate(counts) if c]
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
    value = sum(c * 10 ** (6 - k) for k, c in enumerate(counts))
    return svg_wrap(W, H, "".join(s), "place value discs showing %s" % n(value))


def line_svg(lo, hi, step, labels, arrow=None, show=None):
    """Number line lo..hi, a tick every step, numbers at `labels`, red arrow at `arrow`."""
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


def bar_svg(rows, total=None, label="bar model"):
    """Singapore bar model, drawn to scale.
    rows = [(name, [(value, dashed)], [(first seg, last seg, text)], right text (optional))];
    total = text for a brace on the right spanning all the rows."""
    LW, BW, BH = 104, 300, 30
    big = max(sum(v for v, _ in r[1]) for r in rows)
    sc = BW / float(big)
    W = LW + BW + (112 if total else 14) + (24 if any(len(r) > 3 for r in rows) else 0)
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
        s.append("<path d='M%d %d q8 0 8 8 L%d %.1f q0 6 6 6 q-6 0 -6 6 L%d %d q0 8 -8 8' fill='none' "
                 "stroke='%s' stroke-width='1.6'/>" % (xb, y1, xb + 8, ym - 6, xb + 8, y2 - 8, INK))
        s.append(text(xb + 20, ym + 5, total, 14, anchor="start", bold=True, col=RED if total == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


# ============================================================ set 1: place value to millions
def discs_e(counts):
    parts = [(c, 10 ** (6 - k)) for k, c in enumerate(counts)]
    value = sum(c * v for c, v in parts)
    used = ["%d × %s = %s" % (c, n(v), n(c * v)) for c, v in parts if c]
    s = "Find the value of each group: %s. Add them: %s. Write 0 in every empty place." % ("; ".join(used), n(value))
    return s


def place_e(x, i):
    return ("Read the places from the right: ones, tens, hundreds, thousands, ten thousands, hundred thousands, "
            "millions. In %s the red %d is in the %s place." % (n(x), digit(x, i), PL[i]))


def set_place():
    P_ = []
    for x, i in [(5243816, 6), (7395024, 5), (4152708, 4), (9316485, 3)]:
        others = [PL[k] for k in sorted(range(7), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        P_.append(mcq(fig(chart_svg(x, hi=i)) + "Which place is the red digit in?", PL[i], others, place_e(x, i)))
    C_ = []
    for x, wrong in [(3060405, [3600405, 3060450, 360405]), (8007090, [879, 8070090, 8700090])]:
        C_.append(mcq_n(fig(chart_svg(x)) + "What number does the place value chart show?", x, wrong,
                        "Read the digits from the millions to the ones: %s. Keep every 0: it holds an empty place. "
                        "The number is %s." % (", ".join(str(digit(x, i)) for i in range(6, -1, -1)), n(x))))
    D_ = []
    for counts, wrong in [([3, 2, 0, 0, 0, 0, 0], [5, 320000, 3020000]),
                          ([2, 0, 4, 0, 0, 1, 0], [7, 2400010, 240010]),
                          ([1, 0, 0, 3, 0, 0, 2], [6, 132, 1300002]),
                          ([4, 1, 0, 0, 3, 0, 0], [8, 4010300, 4100030])]:
        x = sum(c * 10 ** (6 - k) for k, c in enumerate(counts))
        e = discs_e(counts)
        if sum(counts) in wrong:
            e += " Do not just count the discs: each disc has its own value."
        D_.append(mcq_n(fig(discs_svg(counts)) + "What number do the place value discs show?", x, wrong, e))
    G_ = []
    for x, i in [(4753218, 5), (6029517, 4), (3860742, 3)]:
        d = digit(x, i)
        assert len(set(str(x))) == 7
        cands = [str(digit(x, k)) for k in sorted(range(7), key=lambda k: (abs(k - i), -k)) if k != i][:3]
        e = "In %s: %s. The %s digit is %d." % (
            n(x), ", ".join("%s %d" % (PL[k], digit(x, k)) for k in range(6, -1, -1)), PL[i], d)
        if d == 0:
            e += " The 0 shows there are no %s." % PL[i]
        G_.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    K_ = [
        mcq_n("How many hundred thousands make 1" + NB + "000" + NB + "000?", 10, [100, 1000, 1],
              "Count in hundred thousands: 100 000, 200 000 … 1 000 000. That is 10 hundred thousands. "
              "Each place is worth 10 times the place to its right."),
        mcq_n("How many thousands make 1 million?", 1000, [100, 10000, 10],
              "1 000 000 = 1000 × 1000. So 1000 thousands make 1 million."),
        mcq_n("How many millions make 10" + NB + "000" + NB + "000?", 10, [100, 1, 1000],
              "10 000 000 = 10 × 1 000 000. Ten millions make ten million."),
        mcq_n("What number is 1 more than 9" + NB + "999" + NB + "999?", 10000000, [1000000, 9999998, 100000000],
              "9 999 999 + 1: every 9 becomes 0 as you rename, and a 1 goes in the ten millions place: 10 000 000. "
              "(9 999 998 is 1 less.)"),
        mcq_n("What is the greatest 7-digit number?", 9999999, [10000000, 9000000, 999999],
              "Put the greatest digit, 9, in all 7 places: 9 999 999. 10 000 000 has 8 digits and "
              "999 999 has only 6."),
    ]
    assert 10 * 100000 == 1000000 and 1000 * 1000 == 1000000 and 9999999 + 1 == 10000000
    Ph = [
        mcq_n("What number is 3 millions, 4 hundred thousands and 5 tens?", 3400050, [345, 3400500, 340050],
              "3 000 000 + 400 000 + 50 = 3 400 050. Write a digit for every place: 3, 4, 0, 0, 0, 5, 0."),
        mcq_n("What number is 6 millions, 7 thousands and 2 hundreds?", 6007200, [672, 6700200, 6070200],
              "6 000 000 + 7000 + 200 = 6 007 200. There are no hundred thousands or ten thousands, "
              "so write 0 in those places."),
    ]
    assert 3000000 + 400000 + 50 == 3400050 and 6000000 + 7000 + 200 == 6007200
    its = P_[:2] + C_[:1] + K_[:1] + D_[:1] + G_[:1] + P_[2:3] + K_[1:2] + D_[1:2] + C_[1:] + G_[1:2] \
        + K_[2:3] + P_[3:] + D_[2:3] + Ph[:1] + G_[2:] + K_[3:4] + D_[3:] + Ph[1:] + K_[4:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Place value to millions", "items": its}


# ============================================================ set 2: read numbers in words
def set_read():
    R = []
    for x, wrong, extra in [
        (3000000, [300000, 30000000, 3000], " 3 000 000 has six zeros after the 3."),
        (5400000, [5040000, 540000, 5000400], ""),
        (2040006, [2400006, 2040060, 2004006], " The 0s hold empty places, so the 4 is in the ten thousands place."),
        (7000045, [7000450, 7045000, 745], ""),
        (6250000, [6025000, 6205000, 625000], ""),
        (4506000, [4560000, 4050600, 4006000], ""),
        (1300090, [1300900, 1390000, 1030090], ""),
        (8017300, [8170300, 8017030, 8070300], " Seventeen is 17, not 70."),
        (9205060, [9250060, 9205600, 9025060], ""),
        (3470512, [3407512, 3047512, 3470520], " Twelve is 12, not 20."),
        (5015015, [5050015, 5015050, 5150015], " Fifteen is 15; fifty is 50."),
        (6080708, [6800708, 6080780, 6008708], ""),
        (2909090, [2990090, 2909900, 2099090], ""),
        (7777007, [7707007, 7777070, 7770007], ""),
    ]:
        R.append(mcq_w("How do you write %s in words?" % n(x), x, wrong, read_e(x) + extra))
    R.append(mcq("How do you write 10" + NB + "000" + NB + "000 in words?", "ten million",
                 ["one million", "one hundred million", "one hundred thousand"],
                 "10 000 000 is 10 millions, so we say “ten million”. One million is 1 000 000 and one hundred "
                 "thousand is 100 000."))
    M = []
    for x, q, ans, wrong in [
        (8030400, "eight million, ☐ thousand, four hundred", "thirty", ["three", "three hundred", "thirteen"]),
        (2600050, "two million, six hundred thousand and ☐", "fifty", ["five", "five hundred", "fifteen"]),
        (9004700, "nine million, ☐ thousand, seven hundred", "four", ["forty", "four hundred", "fourteen"]),
    ]:
        assert words(x) == q.replace("☐", ans)
        M.append(mcq("%s = %s. Which word goes in the box?" % (n(x), q), ans, wrong, read_e(x)))
    nums = [5000300, 5003000, 5300000, 5030000]
    Z = [mcq("Which number is read <b>without</b> the word “thousand”?", n(5000300), [n(v) for v in nums[1:]],
             "%s has 000 in the thousands group, so we do not say “thousand”: %s. The others: %s."
             % (n(5000300), words(5000300), "; ".join("%s is %s" % (n(v), words(v)) for v in nums[1:])))]
    assert all("thousand" in words(v) for v in nums[1:]) and "thousand" not in words(5000300)
    Ch = [mcq_n("Chloe reads 4" + NB + "060" + NB + "000 as “four million and sixty”. What number did she really say?",
                4000060, [4060000, 460, 4600000],
                "“Four million and sixty” is 4 000 060: the 60 is in the tens place. 4 060 000 has 060 in the "
                "thousands group, so it is “four million, sixty thousand”. She left out the word “thousand”.")]
    assert words(4000060) == "four million and sixty" and words(4060000) == "four million, sixty thousand"
    its = R[:3] + M[:1] + R[3:6] + R[14:] + M[1:2] + R[6:9] + Z + M[2:] + R[9:11] + Ch + R[11:14]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Reading numbers in words", "items": its}


# ============================================================ set 3: write numerals from words
def set_write():
    W = []
    for x, wrong, extra in [
        (4000000, [400000, 40000000, 4000], " Four million has six zeros after the 4."),
        (6200000, [6000200, 620000, 6020000], ""),
        (2040006, [246, 2400006, 240006], " 246 and 2 400 006 leave out zeros that hold empty places."),
        (5308000, [5380000, 5003008, 5308], ""),
        (7000025, [7025, 7025000, 700025], ""),
        (1950000, [1905000, 1000950, 195000], ""),
        (3070401, [3700401, 3070041, 37401], ""),
        (8008080, [8800080, 8008800, 8080080], ""),
        (9604300, [9640300, 9604030, 9064300], ""),
        (4012009, [4120009, 412009, 4012090], " Twelve thousand is 012 in the thousands group."),
        (6113030, [6130030, 6113300, 6103030], ""),
        (10000000, [1000000, 100000000, 10000], " Ten million is 10 millions: a 1, a 0 and six more zeros."),
        (2000202, [2202000, 2200002, 222], " There are no thousands, so the thousands group is 000."),
        (5050015, [5500015, 5050150, 5015015], " Fifty is 50, fifteen is 15."),
    ]:
        e = write_e(x) + extra if x != 10000000 else "Ten million = 10 × 1 000 000 = 10 000 000." + extra
        W.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, wrong, e))
    O = [
        mcq_n("Which number is 4 million and 25 thousand?", 4025000, [4250000, 425000, 4000025],
              "4 million = 4 000 000. 25 thousand = 25 000. 4 000 000 + 25 000 = 4 025 000. "
              "The thousands group needs three digits: 025."),
        mcq_n("Which number is 3 millions, 2 ten thousands and 8 ones?", 3020008, [328, 3200008, 3002008],
              "3 000 000 + 20 000 + 8 = 3 020 008. Write 0 for the hundred thousands, thousands, hundreds and tens."),
        mcq_n("6" + NB + "380" + NB + "000 = 6 million and ☐ thousand. What number goes in the box?", 380, [38, 3800, 3],
              "6 380 000 = 6 000 000 + 380 000, and 380 000 is 380 thousands. So the box is 380."),
        mcq_n("2" + NB + "070" + NB + "000 = ☐ thousands. What number goes in the box?", 2070, [207, 20700, 27],
              "2 070 000 = 2070 × 1000, so it is 2070 thousands. (2 million is 2000 thousands, plus 70 thousands.)"),
        mcq_n("What number is <b>5" + NB + "000" + NB + "000 + 30" + NB + "000 + 400 + 2</b>?", 5030402,
              [5300402, 5003402, 53402],
              "Put each value in its place and write 0 in every empty place: 5 millions, 0 hundred thousands, "
              "3 ten thousands, 0 thousands, 4 hundreds, 0 tens, 2 ones → 5 030 402."),
        mcq_n("What number is <b>8 × 1" + NB + "000" + NB + "000 + 6 × 10" + NB + "000 + 9 × 10</b>?", 8060090,
              [869, 8600090, 8060900],
              "8 × 1 000 000 = 8 000 000, 6 × 10 000 = 60 000, 9 × 10 = 90. Add them: 8 060 090."),
    ]
    assert 4000000 + 25000 == 4025000 and 3000000 + 20000 + 8 == 3020008 and 6000000 + 380 * 1000 == 6380000
    assert 2070 * 1000 == 2070000
    assert xval("5 000 000 + 30 000 + 400 + 2") == 5030402 and xval("8 × 1000000 + 6 × 10000 + 9 × 10") == 8060090
    its = W[:3] + O[:1] + W[3:6] + W[11:12] + O[1:2] + W[6:8] + O[2:3] + W[8:10] + O[3:4] + W[12:13] + O[4:5] \
        + W[10:11] + O[5:] + W[13:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Writing numbers in numerals", "items": its}


# ============================================================ set 4: value of a digit, compare and order
def value_cands(d, i):
    """The digit itself, the value one place up, and one place down."""
    return [d * 10 ** (i + 1), d, d * 10 ** (i - 1)]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), n(v), d, n(v)))


def first_diff(a, b):
    for i in range(7, -1, -1):
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
    A = []
    for x, i in [(4836175, 6), (2594381, 5), (7162849, 3)]:
        d = digit(x, i)
        A.append(mcq_n(fig(chart_svg(x, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    B = []
    for x, d in [(3708452, 7), (5246913, 4), (9413680, 6), (8351207, 8)]:
        assert str(x).count(str(d)) == 1
        i = ndig(x) - 1 - str(x).index(str(d))
        B.append(mcq_n("What is the value of the %d in %s?" % (d, n(x)), d * 10 ** i, value_cands(d, i),
                       value_e(d, i)))
    T = [mcq_n("In 4" + NB + "400" + NB + "000, the first 4 is worth how many times the second 4?", 10,
               [100, 4, 3600000],
               "The first 4 is in the millions place: 4 000 000. The second 4 is in the hundred thousands place: "
               "400 000. 4 000 000 ÷ 400 000 = 10. (3 600 000 is the difference, not how many times.)")]
    assert 4000000 // 400000 == 10
    C = []
    for x, y in [(5430000, 5403000), (987654, 1023456), (3060500, 3065000), (7999999, 8000001)]:
        lt, gt = "&lt;", "&gt;"
        right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
        wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
                 "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 987654:
            e += " A big first digit does not matter when a number has fewer digits."
        C.append(mcq("Which is true?", right, wrong, e))
    G = []
    for nums, want_max in [([2465300, 2456300, 2465030, 2456030], True),
                           ([999999, 1000100, 1001000, 1000010], False),
                           ([6080900, 6008900, 6800090, 680900], True)]:
        s = sorted(nums)
        ans, nxt = (s[-1], s[-2]) if want_max else (s[0], s[1])
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % n(ans)
        else:
            e = ("%s has only %d digits. The other numbers have %d digits, so %s is the least, even though it "
                 "starts with 9." % (n(ans), ndig(ans), ndig(nxt), n(ans)))
        G.append(mcq("Which number is the %s?" % ("greatest" if want_max else "least"), n(ans),
                     [n(v) for v in nums if v != ans], e))
    fmt = lambda l: ", ".join(n(v) for v in l)
    O = []
    for nums, up, perms, e in [
        ([4530000, 4350000, 4503000], True, [[4503000, 4350000, 4530000], [4530000, 4503000, 4350000],
                                             [4350000, 4530000, 4503000]],
         "All have 4 millions. Hundred thousands: 3 &lt; 5, so 4 350 000 is the least. 4 530 000 and 4 503 000 both "
         "have 5 hundred thousands. Ten thousands: 0 &lt; 3, so 4 503 000 &lt; 4 530 000."),
        ([1210000, 1201000, 1120000], False, [[1120000, 1201000, 1210000], [1201000, 1210000, 1120000],
                                              [1210000, 1120000, 1201000]],
         "All have 1 million. Hundred thousands: 1 &lt; 2, so 1 120 000 is the least. 1 210 000 and 1 201 000 both "
         "have 2 hundred thousands. Ten thousands: 1 &gt; 0, so 1 210 000 &gt; 1 201 000."),
        ([9900000, 10000000, 9090000, 909000], True, [[909000, 9900000, 9090000, 10000000],
                                                      [10000000, 9900000, 9090000, 909000],
                                                      [9090000, 909000, 9900000, 10000000]],
         "909 000 has only 6 digits, so it is the least. 10 000 000 has 8 digits, so it is the greatest. "
         "9 090 000 &lt; 9 900 000 (hundred thousands: 0 &lt; 9)."),
    ]:
        o = sorted(nums) if up else sorted(nums)[::-1]
        assert all(p != o and sorted(p) == sorted(o) for p in perms)
        O.append(mcq("Put %s in order from %s." % (fmt(nums), "least to greatest" if up else "greatest to least"),
                     fmt(o), [fmt(p) for p in perms], e + " Order: %s." % fmt(o)))
    Dg = [
        mcq_n("Use each of the digits 3, 8, 1, 6, 0, 5 and 7 once. What is the greatest number you can make?", 8765310,
              [8765301, 1035678, 7865310],
              "Put the greatest digit in the millions place, then the next greatest, and so on: "
              "8, 7, 6, 5, 3, 1, 0. The greatest number is 8 765 310."),
        mcq_n("Use each of the digits 3, 8, 1, 6, 0, 5 and 7 once. What is the least 7-digit number you can make?",
              1035678, [135678, 1305678, 8765310],
              "A 7-digit number cannot start with 0. Put the least other digit first: 1. Then 0, 3, 5, 6, 7, 8: "
              "1 035 678. (0 135 678 is just 135 678, which has only 6 digits.)"),
    ]
    assert int("".join(sorted("3816057", reverse=True))) == 8765310
    its = B[:2] + A[:1] + C[:2] + B[2:3] + A[1:2] + G[:1] + C[2:3] + O[:1] + B[3:] + A[2:] + G[1:2] + C[3:] \
        + O[1:2] + T + Dg[:1] + G[2:] + Dg[1:] + O[2:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20
    return {"title": "Value of a digit, comparing and ordering", "items": its}


# ============================================================ set 5: numbers in real life
def set_life():
    S = {}
    S["pop"] = mcq_n("About six million people live in Singapore. Write six million in numerals.", 6000000,
                     [600000, 60000000, 6000],
                     "Six million = 6 × 1 000 000 = 6 000 000: a 6 followed by six zeros. (600 000 is six hundred "
                     "thousand.)")
    S["hdb"] = mcq("There are more than one million HDB flats in Singapore. Which number is more than one million?",
                   n(1100000), [n(110000), n(999999), n(100000)],
                   "One million is 1 000 000. Only 1 100 000 has 7 digits, so it is the only number greater than "
                   "1 000 000. 999 999 is 1 less than one million.")
    assert 1100000 > 1000000 > 999999
    S["line6"] = mcq_n(fig(line_svg(0, 10000000, 1000000, [0, 5000000, 10000000], arrow=6000000))
                       + "The arrow shows about how many people live in Singapore. What number does it point to?",
                       6000000, [600000, 7000000, 1000000],
                       "From 0 to 10 000 000 there are 10 equal spaces, so each space is 1 000 000. "
                       "The arrow is 1 space after 5 000 000: 6 000 000. (600 000 counts each space as 100 000.)")
    x = 1605040
    S["bus"] = mcq_n("A bus company counted %s rides paid with EZ-Link cards in one week. Write the number in "
                     "numerals." % words(x), x, [1650040, 165040, 1605400], write_e(x))
    S["lift"] = mcq_w("A town council spent $2" + NB + "608" + NB + "000 to upgrade lifts in HDB blocks. "
                      "How do you read the amount?", 2608000, [2680000, 2006800, 268000],
                      read_e(2608000) + " So the amount is “%s dollars”." % words(2608000))
    S["lift"]["c"] = [c + " dollars" for c in S["lift"]["c"]]
    S["charity"] = mcq_n("A charity raised $3" + NB + "482" + NB + "560 at its yearly show. "
                         "What is the value of the 8 in this amount?", 80000, [8, 8000, 800000],
                         "3 482 560 is 3 millions, 4 hundred thousands, 8 ten thousands, 2 thousands, 5 hundreds, "
                         "6 tens and 0 ones. The 8 is in the ten thousands place, so it is worth $80 000.", pre="$")
    S["library"] = mcq("Library A has 1" + NB + "245" + NB + "000 books. Library B has 1" + NB + "254" + NB + "000 "
                       "books. Which library has more books?", "Library B",
                       ["Library A", "They have the same number", "You cannot tell"],
                       compare_expl(1254000, 1245000) + " Library B has more books.")
    S["mystery"] = mcq_n("Jun Jie’s mystery number has 5 millions, 0 hundred thousands, 3 ten thousands, "
                         "0 thousands, 9 hundreds, 0 tens and 4 ones. What is his number?", 5030904,
                         [5394, 5300904, 5030940],
                         "Write one digit for each place, with 0 for the empty places: 5, 0, 3, 0, 9, 0, 4. "
                         "That is 5 030 904.")
    S["kumar"] = mcq_n("Kumar reads a number aloud: “seven million, seven thousand and seventy”. Which number "
                       "should he write?", 7007070, [7700070, 7007700, 7070070],
                       write_e(7007070))
    assert words(7007070) == "seven million, seven thousand and seventy"
    pq = [("City P", 1085000), ("City Q", 1058000), ("City R", 1580000)]
    o = sorted(pq, key=lambda t: -t[1])
    fm = lambda l: ", ".join(t[0] for t in l)
    S["cities"] = mcq("City P has 1" + NB + "085" + NB + "000 people, City Q has 1" + NB + "058" + NB + "000 people "
                      "and City R has 1" + NB + "580" + NB + "000 people. Which list goes from the most people "
                      "to the fewest?", fm(o),
                      [fm(l) for l in [[pq[0], pq[1], pq[2]], [pq[1], pq[0], pq[2]], [pq[2], pq[1], pq[0]]]],
                      "All have 1 million. Hundred thousands: 5 &gt; 0, so City R has the most. City P and City Q "
                      "both have 0 hundred thousands. Ten thousands: 8 &gt; 5, so City P has more than City Q. "
                      "Order: City R, City P, City Q.")
    assert fm(o) == "City R, City P, City Q"
    S["fund"] = mcq_n("A school building fund had $4" + NB + "950" + NB + "000. It then received $100" + NB + "000 "
                      "more. How much money is in the fund now?", 5050000, [4960000, 5950000, 4050000],
                      "Add 1 hundred thousand: 9 hundred thousands + 1 hundred thousand = 10 hundred thousands. "
                      "Rename them as 1 million: 4 millions become 5 millions. 4 950 000 + 100 000 = 5 050 000. "
                      "(4 050 000 forgets to add the 1 million.)",
                      pre="$")
    assert 4950000 + 100000 == 5050000
    S["line37"] = mcq_n(fig(line_svg(3000000, 4000000, 100000, [3000000, 3500000, 4000000], arrow=3700000))
                        + "The number line shows how many dollars a charity has raised so far. "
                          "How much has it raised?", 3700000, [3070000, 3600000, 3800000],
                        "From 3 000 000 to 4 000 000 there are 10 equal spaces, so each space is 100 000. "
                        "The arrow is 2 spaces after 3 500 000: 3 600 000, 3 700 000. The charity has raised "
                        "$3 700 000. (3 070 000 counts each space as 10 000.)", pre="$")
    S["cans"] = mcq_n("A factory makes 45" + NB + "000 drink cans a day. How many cans does it make in 100 days?",
                      4500000, [450000, 45000000, 145000],
                      "45 000 × 100: multiplying by 100 moves each digit two places to the left. "
                      "45 000 × 100 = 4 500 000. (450 000 is × 10 and 45 000 000 is × 1000.)")
    assert 45000 * 100 == 4500000
    S["share"] = mcq_n("A fund of $3" + NB + "600" + NB + "000 is shared equally among 100 schools. "
                       "How much does each school get?", 36000, [360000, 3600, 360],
                       "3 600 000 ÷ 100: dividing by 100 moves each digit two places to the right. "
                       "3 600 000 ÷ 100 = 36 000. Each school gets $36 000. (360 000 is ÷ 10.)", pre="$")
    assert 3600000 // 100 == 36000
    S["diff7"] = mcq_n("Siti makes the greatest 7-digit number that has 7 different digits. What is her number?",
                       9876543, [9999999, 1023456, 987654],
                       "Use the greatest digits, each only once, from the millions place down: 9, 8, 7, 6, 5, 4, 3. "
                       "Her number is 9 876 543. (9 999 999 uses the same digit 7 times.)")
    # ---- bar models
    S["park"] = mcq_n(fig(bar_svg([("Last year", [(2500000, False)], [(0, 0, n(2500000))]),
                                   ("This year", [(2500000, False), (400000, False)], [(1, 1, n(400000))], "?")],
                                  total=None, label="bar model: last year and this year"))
                      + "A theme park had 2" + NB + "500" + NB + "000 visitors last year. This year it had "
                        "400" + NB + "000 more visitors than last year. How many visitors did it have this year?",
                      2900000, [2100000, 2540000, 6500000],
                      "This year’s bar is last year’s bar plus 400 000. 2 500 000 + 400 000 = 2 900 000. "
                      "(2 100 000 subtracts instead of adding.)")
    assert 2500000 + 400000 == 2900000
    S["expo"] = mcq_n(fig(bar_svg([("Fair A", [(1350000, False), (750000, True)], [(0, 0, n(1350000)), (1, 1, "?")]),
                                   ("Fair B", [(2100000, False)], [(0, 0, n(2100000))])],
                                  label="bar model comparing two fairs"))
                      + "Book Fair A had 1" + NB + "350" + NB + "000 visitors. Book Fair B had 2" + NB + "100" + NB
                      + "000 visitors. How many more visitors did Fair B have than Fair A?",
                      750000, [1250000, 3450000, 850000],
                      "The difference is the part marked ?. 2 100 000 − 1 350 000 = 750 000. Rename 1 million as "
                      "10 hundred thousands first. (1 250 000 takes the smaller digit from the bigger one in each "
                      "place.)")
    assert 2100000 - 1350000 == 750000
    S["twice"] = mcq_n(fig(bar_svg([("1st year", [(600000, False)], [(0, 0, "?")]),
                                    ("2nd year", [(600000, False), (600000, False)], [])],
                                   total=n(1800000), label="bar model: 1 unit and 2 units, total 1 800 000"))
                       + "A museum had 1" + NB + "800" + NB + "000 visitors in two years. In the 2nd year it had twice "
                         "as many visitors as in the 1st year. How many visitors did it have in the 1st year?",
                       600000, [900000, 1200000, 3600000],
                       "1st year = 1 unit, 2nd year = 2 units. 3 units = 1 800 000. 1 unit = 1 800 000 ÷ 3 = 600 000. "
                       "(900 000 splits the total into 2 parts, and 1 200 000 is the 2nd year.)")
    assert 1800000 // 3 == 600000 and 600000 * 3 == 1800000
    S["bottles"] = mcq_n(fig(bar_svg([("March", [(1600000, False)], [(0, 0, "?")]),
                                      ("April", [(1600000, False), (400000, False)], [(1, 1, n(400000))])],
                                     total=n(3600000), label="bar model: March and April, total 3 600 000"))
                         + "A factory made 3" + NB + "600" + NB + "000 bottles of water in March and April. It made "
                           "400" + NB + "000 more bottles in April than in March. How many bottles did it make "
                           "in March?",
                         1600000, [2000000, 1800000, 3200000],
                         "Take away the extra 400 000: 3 600 000 − 400 000 = 3 200 000. Now the two bars are equal: "
                         "2 units = 3 200 000, so 1 unit = 1 600 000. March: 1 600 000. (2 000 000 is April.)")
    assert (3600000 - 400000) // 2 == 1600000 and 1600000 + 2000000 == 3600000
    S["app"] = mcq_n(fig(bar_svg([("Website", [(1280000, False)], [(0, 0, "?")]),
                                  ("App", [(1280000, False)] * 4, [])],
                                 total=n(6400000), label="bar model: 1 unit and 4 units, total 6 400 000"))
                     + "An online shop had 6" + NB + "400" + NB + "000 visits in a year. It had 4 times as many visits "
                       "on its app as on its website. How many visits were on its website?",
                     1280000, [1600000, 5120000, 128000],
                     "Website = 1 unit, app = 4 units. 5 units = 6 400 000. 1 unit = 6 400 000 ÷ 5 = 1 280 000. "
                     "(1 600 000 divides by 4 instead of 5, and 128 000 leaves out a zero.)")
    assert 6400000 // 5 == 1280000 and 1280000 * 5 == 6400000
    order = ["pop", "hdb", "line6", "bus", "lift", "charity", "library", "mystery", "kumar", "cities", "fund",
             "line37", "cans", "share", "diff7", "park", "expo", "twice", "bottles", "app"]
    assert sorted(order) == sorted(S)
    its = [S[k] for k in order]
    return {"title": "Big numbers in real life", "items": its}


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
        "<h2>Place value to 10 million</h2>"
        "<p>Each place is worth <b>10 times</b> the place to its right. After the hundred thousands comes the "
        "<b>millions</b> place. 10 hundred thousands make 1 000 000 (one million), and 10 millions make "
        "10 000 000 (ten million).</p>"
        "<p>In a place value chart, M = millions, HTh = hundred thousands, TTh = ten thousands, Th = thousands, "
        "H = hundreds, T = tens and O = ones.</p>"
        "<figure class='sn-fig'>" + chart_svg(2040006, hi=4) +
        "<figcaption>2 040 006: the 4 is in the ten thousands place, so it is worth 40 000. "
        "The zeros hold the empty places.</figcaption></figure>"
        "<p>Place value discs show the same idea. Find the value of each group of discs, then add.</p>"
        "<figure class='sn-fig'>" + discs_svg([3, 0, 2, 0, 0, 0, 1]) +
        "<figcaption>3 000 000 + 20 000 + 1 = 3 020 001.</figcaption></figure>"
        "<h2>Reading numbers in words</h2>"
        "<p>Split the number into groups of three digits from the right. Read each group and say its name: "
        "“million”, then “thousand”. If a group is 000, skip its name.</p>"
        + table(["Numerals", "Words"], [
            [n(2040006), words(2040006)],
            [n(5000300), words(5000300)],
            [n(3470512), words(3470512)],
            [n(10000000), words(10000000)],
        ])
        + "<h2>Writing numbers in numerals</h2>"
        "<p>After the millions, every group must have <b>three digits</b>. Use 0 to hold an empty place.</p>"
        + ex("Words to numerals", "Write two million, forty thousand and six in numerals.",
             "two million → 2; forty thousand → 040; six → 006.",
             "2 040 006 (not 246 or 2 400 006)")
        + "<h2>Value of a digit</h2>"
        "<p>The <b>digit</b> is the symbol. Its <b>value</b> depends on its place. In 3 708 452 the digit 7 is in "
        "the hundred thousands place, so its value is 700 000, not 7.</p>"
        "<h2>Comparing and ordering</h2>"
        "<p>First count the digits: a 7-digit number is greater than any 6-digit number. If the numbers have the "
        "same number of digits, compare place by place from the left until two digits are different.</p>"
        + ex("Compare", "3 060 500 ☐ 3 065 000",
             "Millions: 3 = 3. Hundred thousands: 0 = 0. Ten thousands: 6 = 6. Thousands: 0 &lt; 5.",
             "3 060 500 &lt; 3 065 000")
        + "<h2>Big numbers in real life</h2>"
        "<p>About 6 000 000 people live in Singapore, and there are more than 1 000 000 HDB flats. "
        "In word problems with big numbers, draw a bar model to see what to find.</p>"
        "<figure class='sn-fig'>" + bar_svg([("1st year", [(600000, False)], [(0, 0, "?")]),
                                            ("2nd year", [(600000, False), (600000, False)], [])],
                                           total=n(1800000), label="bar model: 1 unit and 2 units, total 1 800 000") +
        "<figcaption>A museum had 1 800 000 visitors in two years, with twice as many in the 2nd year. "
        "3 units = 1 800 000, so 1 unit = 600 000.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving out zeros (two million, forty thousand and six → 246 or 2 400 006)",
             "Write three digits in each group: 2 | 040 | 006 → 2 040 006"],
            ["Giving the digit, not its value (the 7 in 3 708 452 is 7)",
             "It is in the hundred thousands place: 700 000"],
            ["Counting the discs (3 + 2 + 1 = 6)", "Add the values: 3 000 000 + 20 000 + 1 = 3 020 001"],
            ["Saying “thousand” for a 000 group (5 000 300 → five million, three thousand)",
             "Skip the empty group: five million, three hundred"],
            ["Comparing the first digits only (987 654 &gt; 1 023 456)",
             "Count the digits first: 1 023 456 &gt; 987 654"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 whole numbers?",
     "a": "Primary 5 students read and write numbers up to 10 million in numerals and in words, find the value of "
          "each digit, and compare and order big numbers. They also multiply and divide by 10, 100 and 1000."},
    {"q": "How do you write two million, forty thousand and six in numerals?",
     "a": "Write 2 for the millions, 040 for the thousands and 006 for the ones: 2 040 006. Each group after the "
          "millions needs three digits, so zeros hold the empty places."},
    {"q": "What is the most common mistake with numbers to 10 million?",
     "a": "The most common mistake is leaving out zeros, such as writing 2 040 006 as 246 or 2 400 006. Another is "
          "giving the digit instead of its value: the 7 in 3 708 452 is worth 700 000."},
    {"q": "Is numbers to 10 million in the MOE syllabus?",
     "a": "Yes. Reading and writing numbers up to 10 million in numerals and in words is part of Whole Numbers in "
          "the MOE 2021 Primary 5 Mathematics syllabus."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (2 040 006) everywhere outside SVG markup."""
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
    rnd = random.Random(65801)
    sets = [set_place(), set_read(), set_write(), set_compare(), set_life()]
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
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "numbers-to-10-million", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Numbers to 10 Million",
        "seo_title": "P5 Numbers to 10 Million Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Numbers to 10 Million",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Reading and writing numbers up to 10 million in numerals and in words",
        "meta_desc": "Free P5 maths practice on numbers to 10 million: place value, words and numerals, "
                     "the value of a digit, comparing and ordering. 100 questions, answers included.",
        "key_big": "After the millions, every group has three digits: two million, forty thousand and six is 2 040 006.",
        "key_sub": "In 3 708 452 the digit 7 is in the hundred thousands place, so its value is 700 000.",
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
