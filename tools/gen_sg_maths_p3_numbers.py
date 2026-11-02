# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Numbers to 10 000
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 3: Whole Numbers —
 numbers up to 10 000: counting in hundreds/thousands, place values, reading and writing,
 comparing and ordering, patterns)
  python3 tools/gen_sg_maths_p3_numbers.py
Place value with base ten blocks, place value discs and a place value chart, reading and writing numbers in
numerals and words (zeros as placeholders), the value of a digit and expanded form, comparing and ordering,
and number patterns (counting on and back in 100s and 1000s) with Singapore word problems and bar models.
Numbers: 4-digit numbers have no separator (4053); 10 000 uses a no-break space. Never commas.
Words follow Singapore textbooks: "four thousand and fifty-three", "two thousand, six hundred and five".
Wrong answers come from real mistakes: leaving out zeros (4053 written 453), giving the digit instead of
its value, counting the blocks or discs instead of adding their values, saying "zero hundred", reading
fifteen as fifty, comparing the first digits only, and forgetting to rename when a pattern crosses a thousand.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
SIDE = "#a9d3b5"
TOP = "#e3f1e7"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand"]
HEAD = ["Ones", "Tens", "Hundreds", "Thousands"]


# ------------------------------------------------------------ helpers
def n(x):
    """MOE style: 4053, 10 000 (no-break space, never commas)."""
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
    """Value of '3000 + 400 + 5' or '2 × 1000 + 6 × 100 + 4 × 1'."""
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
    """4053 -> four thousand and fifty-three; 2605 -> two thousand, six hundred and five."""
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


assert words(4053) == "four thousand and fifty-three"
assert words(2605) == "two thousand, six hundred and five"
assert words(7008) == "seven thousand and eight"
assert words(2600) == "two thousand, six hundred"
assert words(10000) == "ten thousand"
assert words(453) == "four hundred and fifty-three"


def read_e(x):
    """Numeral -> words explanation."""
    t, o = divmod(x, 1000)
    if not t:
        return "%s is “%s”." % (n(x), words(x))
    if o == 0:
        return "%s is %d thousands, so we say “%s”." % (n(x), t, words(x))
    h, r = divmod(o, 100)
    parts = ["%s → %s thousand" % (plural(t, 3), w1000(t))]
    if h:
        parts.append("%s → %s hundred" % (plural(h, 2), ONES[h]))
    else:
        parts.append("0 hundreds → say nothing")
    if r:
        parts.append("%d → %s" % (r, w100(r)))
    return "Read place by place: %s. So %s is “%s”." % ("; ".join(parts), n(x), words(x))


def write_e(x):
    """Words -> numeral explanation."""
    t, o = divmod(x, 1000)
    return ("Write the thousands digit, then always three more digits for hundreds, tens and ones: "
            "%s → %d; %s → %03d. So the number is %s."
            % (plural(t, 3), t, w1000(o) if o else "nothing more", o, n(x)))


# ------------------------------------------------------------ figures
def digits_svg(x, hi):
    """A 4-digit number in boxes, the digit in place `hi` in red (no place names, so the student must work it out)."""
    BW, BH, G, M = 52, 60, 6, 6
    k = ndig(x)
    W = 2 * M + k * BW + (k - 1) * G
    H = 2 * M + BH
    s = []
    for j, ch in enumerate(str(x)):
        i = k - 1 - j
        xx = M + j * (BW + G)
        red = i == hi
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (xx, M, BW, BH, "#fbe3df" if red else "#fff", RED if red else GREEN))
        s.append(text(xx + BW / 2.0, M + 43, ch, 36, bold=True, col=RED if red else INK))
    return svg_wrap(W, H, "".join(s), "the number %s with one digit in red" % n(x))


CW, H1, ROW = 100, 32, 50


def chart_svg(x, hi=None):
    """Place value chart Thousands | Hundreds | Tens | Ones for a number below 10 000."""
    assert x < 10000
    x0 = y0 = 6
    K = 4
    W, H = 2 * x0 + K * CW, 2 * y0 + H1 + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (x0, y0, K * CW, H1 + ROW),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, K * CW, H1, FILL)]
    nd = ndig(x)
    for k in range(K):
        i = K - 1 - k
        xx = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>"
                     % (xx, y0, xx, y0 + H1 + ROW, GREEN))
        s.append(text(xx + CW / 2.0, y0 + 21, HEAD[i], 14, bold=True))
        if i < nd:
            s.append(text(xx + CW / 2.0, y0 + H1 + 36, str(digit(x, i)), 28, bold=True,
                          col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + H1, x0 + K * CW, y0 + H1, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, K * CW, H1 + ROW, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % n(x))


DISC_FILL = {3: "#f2d4cf", 2: "#d6e4f4", 1: "#cfe6d6", 0: "#fbe9c0"}
DR = 26          # disc radius (fits “1000” at 14px bold)
DG = 4           # gap between discs
GG = 16          # gap between place groups


def discs_svg(counts):
    """Place value discs. counts = [Th, H, T, O]. Each place is a group of up to 2 columns x 3 rows."""
    assert len(counts) == 4 and all(0 <= c <= 6 for c in counts)
    groups = [(3 - k, c) for k, c in enumerate(counts) if c]
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
    value = sum(c * 10 ** (3 - k) for k, c in enumerate(counts))
    return svg_wrap(W, H, "".join(s), "place value discs showing %s" % n(value))


U = 8                      # base ten blocks: a one = U, a ten = 10U, a hundred = 10U x 10U, a thousand = 10U cube
DEP = 26                   # depth offset for the drawn thousand cube
BG = 8                     # gap between pieces
BGG = 22                   # gap between groups
BM = 8


def blocks_svg(th, h, t, o, labels=False):
    """Base ten blocks: th thousand cubes, h hundred flats, t ten rods, o one cubes (faces drawn 1 : 10 : 100)."""
    assert th <= 4 and h <= 6 and t <= 9 and o <= 9
    FS = 10 * U

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
            cx = x + k * (FS + DEP + BG)
            cy = y + DEP
            s.append("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (cx, cy, cx + DEP, cy - DEP, cx + DEP + FS, cy - DEP, cx + FS, cy, TOP, GREEN))
            s.append("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (cx + FS, cy, cx + FS + DEP, cy - DEP, cx + FS + DEP, cy - DEP + FS, cx + FS, cy + FS,
                        SIDE, GREEN))
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (cx, cy, FS, FS, FILL, GREEN))
            s += grid(cx, cy, FS, FS, 10, 10)
        return s

    fcols = h if h <= 3 else (h + 1) // 2
    frows = 1 if h <= 3 else 2

    def flats(x, y):
        s = []
        for k in range(h):
            fx = x + (k % fcols) * (FS + BG)
            fy = y + (k // fcols) * (FS + BG)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (fx, fy, FS, FS, FILL, GREEN))
            s += grid(fx, fy, FS, FS, 10, 10)
        return s

    def rods(x, y):
        s = []
        for k in range(t):
            lx = x + k * (U + 5)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (lx, y, U, FS, FILL, GREEN))
            s += grid(lx, y, U, FS, 1, 10)
        return s

    ccols = (o + 4) // 5

    def ones(x, y):
        s = []
        for k in range(o):
            mx = x + (k // 5) * (U + 6)
            my = y + (k % 5) * (U + 7)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (mx, my, U, U, CUBE, GREEN))
        return s

    groups = []
    if th:
        groups.append((th * (FS + DEP) + (th - 1) * BG, FS + DEP, cubes, plural(th, 3)))
    if h:
        groups.append((fcols * FS + (fcols - 1) * BG, frows * FS + (frows - 1) * BG, flats, plural(h, 2)))
    if t:
        groups.append((t * U + (t - 1) * 5, FS, rods, plural(t, 1)))
    if o:
        groups.append((ccols * U + (ccols - 1) * 6, min(o, 5) * U + (min(o, 5) - 1) * 7, ones, plural(o, 0)))
    lab_w = lambda s: int(len(s) * 8.6) + 6
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * BM + sum(widths) + BGG * (len(groups) - 1)
    Hh = 2 * BM + body_h + (26 if labels else 0)
    s = []
    x = BM
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, BM + body_h - gh)        # every group sits on the same base line
        if labels:
            s.append(text(x + w / 2.0, BM + body_h + 20, lab, 15, bold=True))
        x += w + BGG
    value = th * 1000 + h * 100 + t * 10 + o
    return svg_wrap(W, Hh, "".join(s), "base ten blocks showing %s" % n(value))


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


# ============================================================ set 1: place value with blocks and discs
def zero_e(counts):
    empty = [PL[3 - k] for k, c in enumerate(counts) if not c]
    if not empty:
        return ""
    return " There %s no %s, so write 0 in %s." % ("are", " or ".join(empty),
                                                  "that place" if len(empty) == 1 else "those places")


def sum_e(counts, what):
    parts = [(c, 10 ** (3 - k)) for k, c in enumerate(counts)]
    value = sum(c * v for c, v in parts)
    used = ["%d × %s = %s" % (c, n(v), n(c * v)) for c, v in parts if c]
    return "Find the value of each group of %s: %s. Add them: %s.%s" % (what, "; ".join(used), n(value),
                                                                        zero_e(counts))


def place_e(x, i):
    return ("Read the places from the right: ones, tens, hundreds, thousands. "
            "In %s the red %d is in the %s place." % (n(x), digit(x, i), PL[i]))


def set_place():
    B = []
    for counts, wrong in [([2, 3, 4, 5], [14, 5432, 2354]),
                          ([1, 4, 0, 0], [5, 14, 1040]),
                          ([3, 0, 2, 6], [11, 326, 3260]),
                          ([2, 0, 0, 7], [9, 27, 2070]),
                          ([1, 5, 6, 0], [12, 156, 1506])]:
        x = sum(c * 10 ** (3 - k) for k, c in enumerate(counts))
        e = sum_e(counts, "blocks")
        if sum(counts) in wrong:
            e += " Do not just count the blocks: a thousand cube is worth 1000."
        B.append(mcq_n(fig(blocks_svg(*counts)) + "What number do the base ten blocks show?", x, wrong, e))
    D = []
    for counts, wrong in [([3, 2, 0, 0], [5, 32, 3020]),
                          ([2, 0, 4, 1], [7, 241, 2410]),
                          ([1, 0, 0, 3], [4, 13, 1030]),
                          ([4, 1, 0, 3], [8, 413, 4130])]:
        x = sum(c * 10 ** (3 - k) for k, c in enumerate(counts))
        e = sum_e(counts, "discs")
        if sum(counts) in wrong:
            e += " Do not just count the discs: each disc has its own value."
        D.append(mcq_n(fig(discs_svg(counts)) + "What number do the place value discs show?", x, wrong, e))
    P_ = []
    for x, i in [(5824, 3), (7391, 2), (4567, 1)]:
        others = [PL[k] for k in range(4) if k != i]
        P_.append(mcq(fig(digits_svg(x, i)) + "Which place is the red digit in?", PL[i], others, place_e(x, i)))
    C_ = []
    for x, wrong in [(4053, [453, 4530, 4503]), (7008, [78, 7800, 7080])]:
        C_.append(mcq_n(fig(chart_svg(x)) + "What number does the place value chart show?", x, wrong,
                        "Read the digits from the thousands to the ones: %s. Keep every 0: it holds an empty "
                        "place. The number is %s." % (", ".join(str(digit(x, i)) for i in range(3, -1, -1)), n(x))))
    G_ = []
    for x, i in [(3816, 2), (9274, 1)]:
        d = digit(x, i)
        assert len(set(str(x))) == 4
        cands = [str(digit(x, k)) for k in range(4) if k != i]
        e = "In %s: %s. The %s digit is %d." % (
            n(x), ", ".join("%s %d" % (PL[k], digit(x, k)) for k in range(3, -1, -1)), PL[i], d)
        G_.append(mcq("In %s, which digit is in the %s place?" % (n(x), PL[i]), str(d), cands, e))
    K_ = [
        mcq_n("How many hundreds make 1000?", 10, [100, 1, 1000],
              "Count in hundreds: 100, 200, 300 … 1000. That is 10 hundreds. "
              "Each place is worth 10 times the place to its right."),
        mcq_n("What number is 1 more than 9999?", 10000, [1000, 9998, 100000],
              "9999 + 1: every 9 becomes 0 as you rename, and a 1 goes in the ten thousands place: "
              "10 000 (ten thousand). (9998 is 1 less, and 100 000 has too many zeros.)"),
        mcq_n("What is the greatest 4-digit number?", 9999, [10000, 9000, 999],
              "Put the greatest digit, 9, in all 4 places: 9999. 10 000 has 5 digits and 999 has only 3."),
        mcq_n("What is the smallest 4-digit number?", 1000, [999, 1111, 100],
              "A 4-digit number cannot start with 0, so put 1 in the thousands place and 0 in the other places: "
              "1000. 999 has only 3 digits."),
    ]
    assert 10 * 100 == 1000 and 9999 + 1 == 10000
    its = B[:1] + P_[:1] + D[:1] + K_[:1] + C_[:1] + B[1:2] + G_[:1] + D[1:2] + P_[1:2] + K_[2:3] \
        + B[2:3] + C_[1:2] + D[2:3] + G_[1:2] + K_[3:4] + B[3:4] + P_[2:] + D[3:] + B[4:] + K_[1:2]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Place value with base ten blocks and discs", "items": its}


# ============================================================ set 2: numerals and words
def set_words():
    R = []
    for x, wrong, extra in [
        (3000, [300, 13000, 30000], " Three thousand is 3000; thirty thousand would be 30 000."),
        (6705, [675, 6750, 6075], " The 0 tens are not said, but the 0 is still written."),
        (2410, [2401, 2041, 2140], ""),
        (8090, [8009, 890, 8900], " The 9 is in the tens place, so we say “ninety”."),
        (1515, [1550, 1505, 5115], " The last two digits are 15: fifteen, not fifty."),
        (9006, [906, 9060, 9600], ""),
        (10000, [1000, 100000, 100], " It is 1 more than 9999."),
    ]:
        R.append(mcq_w("How do you write %s in words?" % n(x), x, wrong, read_e(x) + extra))
    R.insert(1, mcq("How do you write 4053 in words?", words(4053),
                    [words(453), "four thousand, zero hundred and fifty-three", words(4503)],
                    read_e(4053) + " We never say “zero hundred”. Just leave the hundreds out."))
    assert words(4503) == "four thousand, five hundred and three"
    W = []
    for x, wrong, extra in [
        (4053, [453, 40053, 4530], " 453 leaves out the 0 that holds the hundreds place."),
        (7008, [78, 708, 7080], " 78 and 708 leave out zeros that hold empty places."),
        (2600, [260, 2060, 20600], ""),
        (5040, [540, 5400, 50040], ""),
        (3912, [39012, 3902, 30912], " Do not write “thousand” as 000 before the 912: the number has only 4 digits."),
        (8818, [8880, 8808, 88018], " Eighteen is 18; eighty is 80."),
        (6019, [6090, 619, 6190], " Nineteen is 19; ninety is 90."),
    ]:
        W.append(mcq_n("Which number is <b>%s</b>?" % words(x), x, wrong, write_e(x) + extra))
    M = []
    for x, q, ans, wrong in [
        (5300, "five thousand, ☐ hundred", "three", ["thirty", "thirteen", "zero"]),
        (2050, "two thousand and ☐", "fifty", ["five", "fifteen", "five hundred"]),
    ]:
        assert words(x) == q.replace("☐", ans)
        M.append(mcq("%s = %s. Which word goes in the box?" % (n(x), q), ans, wrong, read_e(x)))
    nums = [3045, 3450, 3504, 3405]
    Z = [mcq("Which number is read <b>without</b> the word “hundred”?", n(3045), [n(v) for v in nums[1:]],
             "%s has 0 in the hundreds place, so we do not say “hundred”: %s. The others: %s."
             % (n(3045), words(3045), "; ".join("%s is %s" % (n(v), words(v)) for v in nums[1:])))]
    assert all("hundred" in words(v) for v in nums[1:]) and "hundred" not in words(3045)
    Ch = [mcq_n("Siti writes “six thousand and seven” as 607. What should she write?", 6007,
                [607, 6070, 67],
                "Six thousand → 6. Then three more digits: no hundreds, no tens, 7 ones → 007. "
                "6 | 007 = 6007. 607 is only six hundred and seven: Siti left out a zero.")]
    assert words(6007) == "six thousand and seven" and words(607) == "six hundred and seven"
    Zc = [mcq_n("Write <b>nine thousand and nine</b> in numerals. How many zeros does it have?", 2, [1, 3, 0],
                "Nine thousand and nine is 9009: 9 thousands, 0 hundreds, 0 tens, 9 ones. It has 2 zeros. "
                "(909 has only 1 zero and is nine hundred and nine.)")]
    assert words(9009) == "nine thousand and nine"
    its = R[:2] + W[:2] + R[2:3] + M[:1] + W[2:3] + R[3:4] + W[3:4] + Z + R[4:5] + W[4:5] + Ch \
        + R[5:6] + M[1:] + W[5:6] + R[6:7] + Zc + W[6:] + R[7:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Reading and writing numbers in words", "items": its}


# ============================================================ set 3: value of a digit and expanded form
def value_cands(d, i):
    """The digit itself and its value in the two nearest other places (tens or more)."""
    near = [k for k in sorted(range(1, 4), key=lambda k: (abs(k - i), -k)) if k != i][:2]
    return [d] + [d * 10 ** k for k in near]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), n(v), d, n(v)))


def expand(x):
    return " + ".join(n(digit(x, i) * 10 ** i) for i in range(3, -1, -1) if digit(x, i))


def set_value():
    A = []
    for x, i in [(4836, 3), (2594, 2), (7162, 1), (6283, 2)]:
        d = digit(x, i)
        A.append(mcq_n(fig(digits_svg(x, i)) + "What is the value of the red digit?", d * 10 ** i,
                       value_cands(d, i), value_e(d, i, True)))
    B = []
    for x, d in [(3785, 7), (5246, 5), (9431, 3), (6812, 8)]:
        assert str(x).count(str(d)) == 1
        i = ndig(x) - 1 - str(x).index(str(d))
        B.append(mcq_n("What is the value of the %d in %s?" % (d, n(x)), d * 10 ** i, value_cands(d, i),
                       value_e(d, i)))
    S = []
    for x, d in [(2837, 3), (6452, 6)]:
        i = ndig(x) - 1 - str(x).index(str(d))
        others = [plural(d, k) for k in range(4) if k != i]
        S.append(mcq("In %s, the digit %d stands for ☐." % (n(x), d), plural(d, i), others,
                     "Count the places from the right: ones, tens, hundreds, thousands. "
                     "The %d is in the %s place, so it stands for %s = %s." % (d, PL[i], plural(d, i), n(d * 10 ** i))))
    Wh = [mcq("In which number is the digit 6 worth 600?", "4632", ["6432", "4362", "4326"],
              "The 6 must be in the hundreds place (the 3rd digit from the right). In 4632 the 6 is worth 600. "
              "In 6432 it is worth 6000, in 4362 it is worth 60 and in 4326 it is worth 6.")]
    E = []
    x = 6208
    E.append(mcq("Which shows 6208 in expanded form?", expand(x),
                 ["6000 + 200 + 80", "600 + 20 + 8", "6000 + 2000 + 8"],
                 "Write the value of each digit: 6 thousands = 6000, 2 hundreds = 200, 0 tens, 8 ones = 8. "
                 "So 6208 = %s. The 0 tens is left out." % expand(x)))
    assert xval(expand(x)) == x and all(xval(v) != x for v in ["6000 + 200 + 80", "600 + 20 + 8", "6000 + 2000 + 8"])
    E.append(mcq_n("4503 = 4000 + ☐ + 3. What number goes in the box?", 500, [5, 50, 5000],
                   "4503 = 4000 + 500 + 3. The 5 is in the hundreds place, so its value is 500."))
    E.append(mcq_n("7024 = 7000 + ☐ + 4. What number goes in the box?", 20, [2, 200, 24],
                   "The 2 is in the tens place, so its value is 20. 7000 + 20 + 4 = 7024."))
    E.append(mcq_n("What number is <b>3000 + 400 + 5</b>?", 3405, [345, 3450, 30405],
                   "Put each value in its place: 3 thousands, 4 hundreds, 0 tens, 5 ones → 3405."))
    E.append(mcq_n("What number is <b>9000 + 80 + 1</b>?", 9081, [981, 9801, 9810],
                   "9 thousands, 0 hundreds, 8 tens, 1 one → 9081. Write 0 in the empty hundreds place."))
    E.append(mcq_n("What number is <b>2 × 1000 + 6 × 100 + 4 × 1</b>?", 2604, [264, 2640, 2064],
                   "2 × 1000 = 2000, 6 × 100 = 600, 4 × 1 = 4. Add them: 2604. There are no tens, so the tens "
                   "digit is 0."))
    assert 4000 + 500 + 3 == 4503 and 7000 + 20 + 4 == 7024
    assert xval("3000 + 400 + 5") == 3405 and xval("9000+80+1") == 9081
    assert xval("2 × 1000 + 6 × 100 + 4 × 1") == 2604
    Rn = [
        mcq_n("3400 = ☐ hundreds. What number goes in the box?", 34, [340, 3, 304],
              "3400 = 34 × 100, so it is 34 hundreds. (3000 is 30 hundreds, plus 4 hundreds.)"),
        mcq_n("How many tens are there in 2500?", 250, [25, 2500, 205],
              "2500 = 250 × 10, so there are 250 tens. (25 is the number of hundreds.)"),
        mcq_n("What number is 12 hundreds?", 1200, [12, 120, 12000],
              "12 hundreds = 10 hundreds + 2 hundreds = 1000 + 200 = 1200. Rename 10 hundreds as 1 thousand."),
    ]
    assert 34 * 100 == 3400 and 250 * 10 == 2500 and 12 * 100 == 1200
    its = B[:2] + A[:1] + E[1:2] + B[2:3] + A[1:2] + S[:1] + E[3:4] + B[3:] + A[2:3] + E[:1] + E[4:5] + S[1:] \
        + A[3:] + E[2:3] + Rn[:1] + E[5:] + Wh + Rn[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Value of a digit and expanded form", "items": its}


# ============================================================ set 4: compare and order
def first_diff(a, b):
    for i in range(4, -1, -1):
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
    for x, y in [(5430, 5403), (999, 1002), (3056, 3065), (7999, 8001), (6060, 6600), (4587, 4578)]:
        lt, gt = "&lt;", "&gt;"
        right = "%s %s %s" % (n(x), lt if x < y else gt, n(y))
        wrong = ["%s %s %s" % (n(x), gt if x < y else lt, n(y)), "%s = %s" % (n(x), n(y)),
                 "%s %s %s" % (n(y), lt if x < y else gt, n(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 999:
            e += " A big first digit does not matter when a number has fewer digits."
        C.append(mcq("Which is true?", right, wrong, e))
    G = []
    for nums, want_max in [([2465, 2456, 2645, 2546], True),
                           ([999, 1001, 1010, 1100], False),
                           ([6089, 6809, 6890, 689], True),
                           ([3512, 3521, 3152, 3215], False)]:
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
        ([4530, 4350, 4503], True, [[4503, 4350, 4530], [4530, 4503, 4350], [4350, 4530, 4503]],
         "All have 4 thousands. Hundreds: 3 &lt; 5, so 4350 is the least. 4530 and 4503 both have 5 hundreds. "
         "Tens: 0 &lt; 3, so 4503 &lt; 4530."),
        ([1201, 1210, 1120], False, [[1120, 1201, 1210], [1201, 1210, 1120], [1210, 1120, 1201]],
         "All have 1 thousand. Hundreds: 1 &lt; 2, so 1120 is the least. 1210 and 1201 both have 2 hundreds. "
         "Tens: 1 &gt; 0, so 1210 &gt; 1201."),
        ([9900, 10000, 9090, 990], True, [[990, 9900, 9090, 10000], [10000, 9900, 9090, 990],
                                           [9090, 990, 9900, 10000]],
         "990 has only 3 digits, so it is the least. 10 000 has 5 digits, so it is the greatest. "
         "9090 &lt; 9900 (hundreds: 0 &lt; 9)."),
        ([6066, 6606, 6660, 6006], False, [[6006, 6066, 6606, 6660], [6660, 6066, 6606, 6006],
                                           [6606, 6660, 6006, 6066]],
         "All have 6 thousands. Hundreds: 6660 and 6606 have 6 hundreds; the others have 0. "
         "6660 and 6606: tens 6 &gt; 0, so 6660 &gt; 6606. 6066 and 6006: tens 6 &gt; 0, so 6066 &gt; 6006."),
    ]:
        o = sorted(nums) if up else sorted(nums)[::-1]
        assert all(p != o and sorted(p) == sorted(o) for p in perms)
        assert len({tuple(p) for p in perms}) == 3
        O.append(mcq("Put %s in order from %s." % (fmt(nums), "least to greatest" if up else "greatest to least"),
                     fmt(o), [fmt(p) for p in perms], e + " Order: %s." % fmt(o)))
    Dg = [
        mcq_n("Use each of the digits 3, 8, 1 and 6 once. What is the greatest number you can make?", 8631,
              [8613, 1368, 6831],
              "Put the greatest digit in the thousands place, then the next greatest, and so on: "
              "8, 6, 3, 1. The greatest number is 8631."),
        mcq_n("Use each of the digits 5, 0, 7 and 2 once. What is the smallest 4-digit number you can make?",
              2057, [257, 2075, 2507],
              "A 4-digit number cannot start with 0. Put the smallest other digit first: 2. Then 0, 5, 7: 2057. "
              "(0257 is just 257, which has only 3 digits.)"),
        mcq_n("Use each of the digits 4, 0, 9 and 0 once. What is the greatest number you can make?", 9400,
              [9040, 4900, 9004],
              "Put the greatest digits first: 9 in the thousands place, 4 in the hundreds place, then the two 0s: "
              "9400."),
    ]
    assert int("".join(sorted("3816", reverse=True))) == 8631 and int("".join(sorted("4090", reverse=True))) == 9400
    Bt = [
        mcq_n("Which number is between 4590 and 4610?", 4600, [4509, 4690, 460],
              "4590 &lt; 4600 &lt; 4610. 4509 is less than 4590, 4690 is more than 4610, "
              "and 460 has only 3 digits."),
        mcq_n("Which number is greater than 8900 but less than 9000?", 8950, [9850, 895, 9050],
              "8950 has 8 thousands and 9 hundreds, so it is between 8900 and 9000. "
              "9850 and 9050 are more than 9000; 895 is less than 8900."),
        mcq_n("What is the greatest 4-digit number that is less than 5000?", 4999, [5001, 4000, 499],
              "Go back 1 from 5000: 4999. 5001 is more than 5000, 4000 is not the greatest, "
              "and 499 has only 3 digits."),
    ]
    assert 4590 < 4600 < 4610 and 8900 < 8950 < 9000 and 5000 - 1 == 4999
    its = C[:2] + G[:1] + C[2:3] + Bt[:1] + G[1:2] + C[3:4] + O[:1] + C[4:5] + Dg[:1] + G[2:3] + Bt[1:2] \
        + O[1:2] + C[5:] + Dg[1:2] + G[3:] + O[2:3] + Bt[2:] + Dg[2:] + O[3:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Comparing and ordering numbers", "items": its}


# ============================================================ set 5: number patterns and word problems
def seq(a, step, k=4):
    return [a + j * step for j in range(k)]


def set_patterns():
    S = {}
    for key, a, step, wrong, e in [
        ("p1", 2400, 1000, [4500, 6400, 4410],
         "Each number is 1000 more: the thousands digit goes up by 1. 4400 + 1000 = 5400. "
         "(4500 adds only 100.)"),
        ("p2", 1570, 100, [2770, 1780, 1970],
         "Each number is 100 more: the hundreds digit goes up by 1. 1770 + 100 = 1870. "
         "(2770 adds 1000, and 1780 adds 10.)"),
        ("p3", 8360, -1000, [6260, 4360, 6350],
         "Each number is 1000 less: the thousands digit goes down by 1. 6360 − 1000 = 5360. "
         "(6260 takes away only 100.)"),
        ("p4", 3200, -100, [2000, 2990, 2800],
         "Each number is 100 less. 3000 − 100 = 2900: rename 1 thousand as 10 hundreds, then take away "
         "1 hundred. (2000 takes away 1000.)"),
        ("p5", 4700, 100, [4000, 4910, 5900],
         "Each number is 100 more. 4900 + 100 = 5000: 10 hundreds are renamed as 1 thousand. "
         "(4000 forgets to rename.)"),
    ]:
        s = seq(a, step)
        q = "What is the next number in the pattern?<br><b>%s, %s, %s, ☐</b>" % (n(s[0]), n(s[1]), n(s[2]))
        S[key] = mcq_n(q, s[3], wrong, e)
    s = seq(6180, 1000)
    S["mid1"] = mcq_n("What is the missing number?<br><b>%s, ☐, %s, %s</b>" % (n(s[0]), n(s[2]), n(s[3])), s[1],
                      [6190, 6280, 7190],
                      "From 8180 to 9180 is 1000 more, so the rule is “add 1000”. 6180 + 1000 = 7180.")
    s = seq(9450, -100)
    S["mid2"] = mcq_n("What is the missing number?<br><b>%s, %s, ☐, %s</b>" % (n(s[0]), n(s[1]), n(s[3])), s[2],
                      [8250, 9240, 9200],
                      "Each number is 100 less: 9450, 9350, 9250, 9150. Only the hundreds digit changes. "
                      "(8250 takes away 1000 instead of 100.)")
    S["more"] = mcq_n("What number is 100 more than 3960?", 4060, [3060, 3970, 4960],
                      "3960 + 100: 9 hundreds + 1 hundred = 10 hundreds. Rename them as 1 thousand: "
                      "3 thousands become 4. 3960 + 100 = 4060. (4960 adds 1000, and 3970 adds 10.)")
    S["less"] = mcq_n("What number is 1000 less than 10" + NB + "000?", 9000, [9900, 1000, 8000],
                      "10 000 is 10 thousands. Take away 1 thousand: 9 thousands = 9000. "
                      "(9900 takes away only 100.)")
    S["rule"] = mcq("What is the rule for this pattern?<br><b>5630, 5430, 5230, 5030</b>", "Subtract 200",
                    ["Add 200", "Subtract 2000", "Subtract 20"],
                    "The numbers get smaller, so we subtract. 5630 − 5430 = 200. The hundreds digit goes down by 2 "
                    "each time. The rule is “subtract 200”.")
    assert 5630 - 5430 == 200 and 5230 - 200 == 5030
    S["line1"] = mcq_n(fig(line_svg(3000, 4000, 100, [3000, 3500, 4000], arrow=3700))
                       + "What number does the arrow point to?", 3700, [3070, 3600, 3800],
                       "From 3000 to 4000 there are 10 equal spaces, so each space is 100. The arrow is "
                       "2 spaces after 3500: 3600, 3700. (3070 counts each space as 10.)")
    S["line2"] = mcq_n(fig(line_svg(0, 10000, 1000, [0, 5000, 10000], arrow=7000))
                       + "What number does the arrow point to?", 7000, [700, 6000, 8000],
                       "From 0 to 10 000 there are 10 equal spaces, so each space is 1000. The arrow is 2 spaces "
                       "after 5000: 6000, 7000. (700 counts each space as 100.)")
    # ---- word problems
    S["hafiz"] = mcq_n("Hafiz counts back in thousands: 9200, 8200, … What is the 4th number he says?", 6200,
                       [7200, 5200, 8900],
                       "9200 (1st), 8200 (2nd), 7200 (3rd), 6200 (4th). Each time the thousands digit goes down "
                       "by 1. (8900 counts back in hundreds.)")
    S["library"] = mcq_n("The school library has 4680 books. It gets 100 new books every month. How many "
                         "books will it have after 3 months?", 4980, [4780, 4683, 7680],
                         "Count on in hundreds 3 times: 4780, 4880, 4980. (4780 is after only 1 month, "
                         "and 7680 adds 3 thousands.)")
    assert 4680 + 3 * 100 == 4980
    S["compare"] = mcq("Ali’s school has 1245 students. Mei Ling’s school has 1254 students. Which is true?",
                       "Mei Ling’s school has more students",
                       ["Ali’s school has more students", "Both schools have the same number of students",
                        "You cannot tell which school has more"],
                       compare_expl(1254, 1245) + " Mei Ling’s school has more students.")
    S["bakery"] = mcq_n("A bakery sold 900 buns on Monday. Each day after that, it sold 100 more buns than the "
                        "day before. How many buns did it sell on Friday?", 1300, [1400, 1200, 905],
                        "Monday 900, Tuesday 1000, Wednesday 1100, Thursday 1200, Friday 1300. From Monday to "
                        "Friday there are only 4 jumps of 100. (1400 adds 5 jumps.)")
    assert 900 + 4 * 100 == 1300
    S["savings"] = mcq_n("Mrs Lim had $5000 in the bank. She took out $1000 every month for 3 months. "
                         "How much money did she have left?", 2000, [4000, 8000, 4997],
                         "Count back in thousands 3 times: $4000, $3000, $2000. "
                         "($4997 takes away $3 instead of $3000.)", pre="$")
    assert 5000 - 3 * 1000 == 2000
    # ---- bar models
    S["cans"] = mcq_n(fig(bar_svg([("Class A", [(3850, False)], [(0, 0, n(3850))]),
                                   ("Class B", [(3850, False), (1000, False)], [(1, 1, n(1000))], "?")],
                                  label="bar model: Class A and Class B"))
                      + "For a recycling drive, Class A collected 3850 cans. Class B collected 1000 more cans "
                        "than Class A. How many cans did Class B collect?",
                      4850, [2850, 3950, 3851],
                      "Class B’s bar is Class A’s bar plus 1000. 3850 + 1000 = 4850: the thousands digit goes up "
                      "by 1. (2850 subtracts, and 3950 adds only 100.)")
    assert 3850 + 1000 == 4850
    S["zoo"] = mcq_n(fig(bar_svg([("Saturday", [(6430, False)], [(0, 0, n(6430))]),
                                  ("Friday", [(5430, False), (1000, True)], [(0, 0, n(5430)), (1, 1, "?")])],
                                 label="bar model comparing Saturday and Friday"))
                     + "The zoo had 6430 visitors on Saturday and 5430 visitors on Friday. How many more visitors "
                       "were there on Saturday?", 1000, [100, 11860, 10],
                     "The difference is the part marked ?. 6430 − 5430 = 1000: only the thousands digit is "
                     "different (6 and 5). (11 860 adds the numbers.)")
    assert 6430 - 5430 == 1000 and 6430 + 5430 == 11860
    S["oranges"] = mcq_n(fig(bar_svg([("Oranges", [(2000, False), (5000, True)], [(0, 0, n(2000)), (1, 1, "?")])],
                                     total=n(7000), label="bar model: 7000 oranges, 2000 sold"))
                         + "A shop had 7000 mandarin oranges for Chinese New Year. It sold 2000 of them. "
                           "How many mandarin oranges were left?", 5000, [9000, 6800, 500],
                         "The whole bar is 7000 and one part is 2000. 7000 − 2000 = 5000 (7 thousands − "
                         "2 thousands = 5 thousands). (9000 adds, and 6800 takes away only 200.)")
    assert 7000 - 2000 == 5000
    order = ["p1", "p2", "more", "p3", "line1", "p4", "less", "mid1", "line2", "p5", "rule", "mid2",
             "compare", "library", "hafiz", "cans", "savings", "zoo", "oranges", "bakery"]
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
        "<h2>Place value to 10 000</h2>"
        "<p>A 4-digit number has <b>thousands, hundreds, tens and ones</b>. Each place is worth <b>10 times</b> "
        "the place to its right. 10 ones make 1 ten, 10 tens make 1 hundred, 10 hundreds make 1 thousand, "
        "and 10 thousands make 10 000 (ten thousand).</p>"
        "<p>Base ten blocks show the value of each place. Count each kind of block and write a digit for it.</p>"
        "<figure class='sn-fig'>" + blocks_svg(2, 3, 0, 4, labels=True) +
        "<figcaption>2 thousands, 3 hundreds, 0 tens and 4 ones make 2304. "
        "There are no tens, so the tens digit is 0.</figcaption></figure>"
        "<p>Place value discs show the same idea. Find the value of each group of discs, then add.</p>"
        "<figure class='sn-fig'>" + discs_svg([3, 0, 2, 1]) +
        "<figcaption>3000 + 20 + 1 = 3021. Do not just count the discs (3 + 2 + 1 = 6).</figcaption></figure>"
        "<figure class='sn-fig'>" + chart_svg(4053, hi=1) +
        "<figcaption>4053: the 5 is in the tens place, so it is worth 50. "
        "The 0 holds the empty hundreds place.</figcaption></figure>"
        "<h2>Reading and writing numbers in words</h2>"
        "<p>Read the thousands first and say “thousand”. Then read the hundreds, tens and ones. "
        "If a place has 0, do not say it, but always <b>write</b> the 0.</p>"
        + table(["Numerals", "Words"], [
            [n(4053), words(4053)],
            [n(2605), words(2605)],
            [n(7008), words(7008)],
            [n(10000), words(10000)],
        ])
        + ex("Words to numerals", "Write six thousand and seven in numerals.",
             "six thousand → 6; then three more digits for hundreds, tens and ones: 007.",
             "6007 (not 607)")
        + "<h2>Value of a digit and expanded form</h2>"
        "<p>The <b>digit</b> is the symbol. Its <b>value</b> depends on its place. In 3785 the digit 7 is in "
        "the hundreds place, so its value is 700, not 7.</p>"
        "<p>Expanded form shows the value of every digit: 6208 = 6000 + 200 + 8.</p>"
        "<h2>Comparing and ordering</h2>"
        "<p>First count the digits: a 4-digit number is greater than any 3-digit number. If the numbers have the "
        "same number of digits, compare place by place from the left until two digits are different.</p>"
        + ex("Compare", "3056 ☐ 3065",
             "Thousands: 3 = 3. Hundreds: 0 = 0. Tens: 5 &lt; 6.",
             "3056 &lt; 3065")
        + "<h2>Number patterns</h2>"
        "<p>To count on in hundreds, add 1 to the hundreds digit. To count on in thousands, add 1 to the "
        "thousands digit. When the hundreds go past 9, rename 10 hundreds as 1 thousand.</p>"
        + ex("Count on in hundreds", "4700, 4800, 4900, ☐",
             "4900 + 100: 9 hundreds + 1 hundred = 10 hundreds = 1 thousand.",
             "5000")
        + "<p>In word problems, draw a bar model to see what to find.</p>"
        "<figure class='sn-fig'>" + bar_svg([("Class A", [(3850, False)], [(0, 0, n(3850))]),
                                            ("Class B", [(3850, False), (1000, False)], [(1, 1, n(1000))], "?")],
                                           label="bar model: Class A and Class B") +
        "<figcaption>Class B collected 1000 more cans than Class A. "
        "3850 + 1000 = 4850.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving out zeros (four thousand and fifty-three → 453)",
             "Write three digits after the thousands: 4 | 053 → 4053"],
            ["Saying “zero hundred” (four thousand, zero hundred and fifty-three)",
             "Leave out places with 0: four thousand and fifty-three"],
            ["Giving the digit, not its value (the 7 in 3785 is 7)",
             "It is in the hundreds place: 700"],
            ["Counting the blocks or discs (3 + 2 + 1 = 6)", "Add the values: 3000 + 20 + 1 = 3021"],
            ["Comparing the first digits only (999 &gt; 1002)",
             "Count the digits first: 1002 &gt; 999"],
            ["Forgetting to rename in a pattern (4900 + 100 → 4000)",
             "10 hundreds make 1 thousand: 5000"],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 whole numbers?",
     "a": "Primary 3 students count in hundreds and thousands, read and write numbers up to 10 000 in numerals "
          "and in words, find the value of each digit, compare and order numbers, and continue number patterns."},
    {"q": "How do you write four thousand and fifty-three in numerals?",
     "a": "Write 4 for the thousands, then three more digits for hundreds, tens and ones: 4053. "
          "The 0 holds the empty hundreds place, so it is not 453."},
    {"q": "What is the most common mistake with numbers to 10 000?",
     "a": "The most common mistake is leaving out zeros, such as writing 4053 as 453. Another is giving the "
          "digit instead of its value: the 7 in 3785 is worth 700."},
    {"q": "Is numbers to 10 000 in the MOE syllabus?",
     "a": "Yes. Numbers up to 10 000, including place value, reading and writing, comparing and ordering, and "
          "number patterns, are part of Whole Numbers in the MOE 2021 Primary 3 Mathematics syllabus."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (10 000) everywhere outside SVG markup."""
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
    """Tag wide pictures (blocks, discs, charts, number lines, bar models) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(63801)
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
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "numbers-to-10000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Numbers to 10 000",
        "seo_title": "P3 Numbers to 10 000 Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Numbers to 10 000",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Numbers up to 10 000: counting in hundreds/thousands, place values, reading and writing, "
                         "comparing and ordering, patterns",
        "meta_desc": "Free P3 maths practice on numbers to 10 000: place value, numerals and words, value of a digit, "
                     "comparing, ordering and patterns. 100 questions with answers.",
        "key_big": "After the thousands, always write three digits: four thousand and fifty-three is 4053.",
        "key_sub": "In 3785 the digit 7 is in the hundreds place, so its value is 700.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(fix_spaces(u),
                      "(number line|place value chart|place value discs|base ten blocks|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
