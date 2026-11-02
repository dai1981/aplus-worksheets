# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Numbers to 1000
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 2: Whole Numbers —
 numbers up to 1000: counting in tens/hundreds, place values, reading and writing, comparing and ordering, patterns)
  python3 tools/gen_sg_maths_p2_numbers.py
Hundreds, tens and ones (base ten blocks, place value discs and charts), reading and writing numbers in numerals
and in words, comparing and ordering, counting on and back in tens and hundreds (number lines), and number
patterns with simple Singapore word problems and bar models. Short sentences for 7-8 year olds.
Numbers stay at 1000 or below, so there are no digit-group spaces.
Words follow Singapore textbooks: "four hundred and seven".
Wrong answers come from real mistakes: leaving out a zero (407 written 47), writing each spoken part
(four hundred and seven -> 4007), mixing up 407 and 470, giving the digit instead of its value (the 4 in 345 is 4),
counting the blocks instead of adding their values (2 + 3 + 4 = 9), reading the blocks backwards (234 -> 432),
fifteen / fifty and nineteen / ninety, the spellings "fourty" and "ninty", comparing the first digit only
(99 > 189), and forgetting to rename 10 tens as 1 hundred when counting on in tens (590, 5100).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"

PL = ["ones", "tens", "hundreds"]
PL1 = ["one", "ten", "hundred"]


# ------------------------------------------------------------ helpers
NUM = re.compile(r"^(\d+)$")


def val(c):
    """Value of a choice that is a single number (None otherwise)."""
    m = NUM.match(c)
    return int(m.group(1)) if m else None


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong. No two choices may be equal in value."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    known = [v for v in (val(x) for x in ch) if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_n(q, correct, wrong, e):
    assert isinstance(correct, int) and 0 <= correct <= 1000, (q, correct)
    assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3, (q, correct, wrong)
    assert all(isinstance(w, int) and 0 <= w < 10000 for w in wrong), (q, wrong)
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


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def cap(s):
    return s[0].upper() + s[1:]


def digit(x, i):
    return (x // 10 ** i) % 10


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def hto(h, t, o):
    return "%s, %s and %s" % (plural(h, 2), plural(t, 1), plural(o, 0))


def hto_n(x):
    return hto(digit(x, 2), digit(x, 1), digit(x, 0))


def unit(k, w):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


# ------------------------------------------------------------ numbers in words (Singapore / British style)
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def w100(x):
    if x < 20:
        return ONES[x]
    return TENS[x // 10] + ("-" + ONES[x % 10] if x % 10 else "")


def words(x):
    """407 -> four hundred and seven."""
    assert 0 < x <= 1000
    if x == 1000:
        return "one thousand"
    h, r = divmod(x, 100)
    out = []
    if h:
        out.append(ONES[h] + " hundred")
    if r:
        out.append(w100(r))
    return " and ".join(out)


assert words(407) == "four hundred and seven" and words(470) == "four hundred and seventy"
assert words(300) == "three hundred" and words(864) == "eight hundred and sixty-four" and words(47) == "forty-seven"


def empty_places(x):
    return [PL[i] for i in (1, 0) if digit(x, i) == 0 and x >= 100]


def write_e(x):
    s = "%s is %s: %d." % (cap(words(x)), hto_n(x), x)
    emp = empty_places(x)
    if emp:
        s += " Write 0 for the empty %s place%s." % (" and ".join(emp), "s" if len(emp) > 1 else "")
    return s


# ------------------------------------------------------------ figures
U = 8                      # base ten blocks: a cube = U, a rod = U x 10U, a flat = 10U x 10U (exact 1 : 10 : 100)
G = 8                      # gap between flats
GG = 22                    # gap between groups
MG = 8


def blocks_svg(h, t, o, labels=False):
    """Base ten blocks: h flats, t rods, o cubes. Flats in one row (up to 3) or two rows; cubes in columns of 5."""
    F = 10 * U
    groups = []

    def grid(x, y, w, hh, cols, rows):
        s = []
        for i in range(1, cols):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x + i * U, y, x + i * U, y + hh, GREEN))
        for i in range(1, rows):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + i * U, x + w, y + i * U, GREEN))
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

    def rods(x, y):
        s = []
        for k in range(t):
            lx = x + k * (U + 5)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (lx, y, U, F, FILL, GREEN))
            s += grid(lx, y, U, F, 1, 10)
        return s

    ccols = (o + 4) // 5

    def cubes(x, y):
        s = []
        for k in range(o):
            mx = x + (k // 5) * (U + 6)
            my = y + (k % 5) * (U + 7)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                     % (mx, my, U, U, CUBE, GREEN))
        return s

    if h:
        groups.append((fcols * F + (fcols - 1) * G, frows * F + (frows - 1) * G, flats, plural(h, 2)))
    if t:
        groups.append((t * U + (t - 1) * 5, F, rods, plural(t, 1)))
    if o:
        groups.append((ccols * U + (ccols - 1) * 6, 5 * U + 4 * 7, cubes, plural(o, 0)))
    lab_w = lambda s: int(len(s) * 8.6) + 6
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * MG + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * MG + body_h + (26 if labels else 0)
    s = []
    x = MG
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, MG + body_h - gh)        # every group sits on the same base line
        if labels:
            s.append(text(x + w / 2, MG + body_h + 20, lab, 15))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base ten blocks")


CW, HEAD, ROW = 104, 34, 50


def chart_svg(x, hi=None):
    """Place value chart Hundreds | Tens | Ones. hi = place index drawn in red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 3 * CW, 2 * y0 + HEAD + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 3 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 3 * CW, HEAD, FILL)]
    for k in range(3):
        i = 2 - k
        xx = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (xx, y0, xx, y0 + HEAD + ROW, GREEN))
        cx = xx + CW / 2
        s.append(text(cx, y0 + 23, cap(PL[i]), 15))
        s.append(text(cx, y0 + HEAD + 36, str(digit(x, i)), 30, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 3 * CW, y0 + HEAD, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0, 3 * CW, HEAD + ROW, GREEN))
    return svg_wrap(W, Hh, "".join(s), "place value chart showing %d" % x)


DISC_FILL = {2: "#d6e4f4", 1: "#cfe6d6", 0: "#fbe9c0"}
DR = 19          # disc radius (fits “100” at 14px)
DG = 4           # gap between discs
DGG = 18         # gap between place groups


def discs_svg(counts):
    """Place value discs. counts = [H, T, O], each 0 to 9, drawn in groups of up to 3 columns x 3 rows."""
    assert len(counts) == 3 and all(0 <= c <= 9 for c in counts)
    groups = [(2 - k, c) for k, c in enumerate(counts) if c]
    D = 2 * DR
    M = 6
    W = 2 * M + sum(min(c, 3) * D + (min(c, 3) - 1) * DG for _, c in groups) + DGG * (len(groups) - 1)
    rows = max((c + 2) // 3 for _, c in groups)
    H = 2 * M + rows * D + (rows - 1) * DG
    s = []
    x = M
    for i, c in groups:
        cols = min(c, 3)
        for k in range(c):
            cx = x + (k % cols) * (D + DG) + DR
            cy = M + (k // cols) * (D + DG) + DR
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (cx, cy, DR - 1, DISC_FILL[i], INK))
            s.append(text(cx, cy + 5, str(10 ** i), 14))
        x += cols * D + (cols - 1) * DG + DGG
    value = sum(c * 10 ** (2 - k) for k, c in enumerate(counts))
    return svg_wrap(W, H, "".join(s), "place value discs showing %d" % value)


def line_svg(lo, hi, step, labels, arrow=None):
    """Number line lo..hi, a tick every step, numbers at `labels`, red arrow at `arrow`."""
    L, R = 40, 440
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
            s.append(text(X(v), Y + 30, str(v), 15, col=GREEN))
        v += step
    for v in labels:
        assert (v - lo) % step == 0 and lo <= v <= hi
    if arrow is not None:
        assert (arrow - lo) % step == 0 and arrow not in labels
        ax = X(arrow)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    return svg_wrap(W, H, "".join(s), "number line from %d to %d" % (lo, hi))


def bar_svg(rows, total=None, label="bar model"):
    """Singapore bar model, drawn to scale.
    rows = [(name, [(value, dashed)], [(first seg, last seg, text)], right text (optional))];
    total = text for a brace on the right spanning all the rows."""
    LW, BW, BH = 96, 300, 30
    big = max(sum(v for v, _ in r[1]) for r in rows)
    sc = BW / float(big)
    side = max([len(r[3]) for r in rows if len(r) > 3] or [0])
    W = LW + BW + (70 if total else 14) + (int(side * 9.5) + 16 if side else 0)
    y = 6
    s = []
    tops = []
    for row in rows:
        name, segs, over = row[:3]
        y += 24
        tops.append(y)
        s.append(text(LW - 10, y + BH / 2.0 + 5, name, 14, anchor="end"))
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
            s.append(text((x1 + x2) / 2.0, y - 11, t, 14, col=RED if t == "?" else INK))
        if len(row) > 3:
            s.append(text(xs[-1] + 10, y + BH / 2.0 + 6, row[3], 16, anchor="start", col=RED))
        y += BH + 12
    H = y
    if total:
        xb = LW + BW + 10
        y1, y2 = tops[0], tops[-1] + BH
        ym = (y1 + y2) / 2.0
        s.append("<path d='M%d %d q6 0 6 6 L%d %.1f q0 3 4 3 q-4 0 -4 3 L%d %d q0 6 -6 6' fill='none' "
                 "stroke='%s' stroke-width='1.6'/>" % (xb, y1, xb + 6, ym - 3, xb + 6, y2 - 6, INK))
        s.append(text(xb + 16, ym + 5, total, 14, anchor="start", col=RED if total == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def blocks_e(h, t, o):
    x = 100 * h + 10 * t + o
    s = "A flat is 100, a rod is 10 and a small cube is 1. %s make %d." % (cap(hto(h, t, o)), x)
    emp = [PL[i] for i, d in ((1, t), (0, o)) if d == 0]
    if emp:
        s += " There are no %s, so write 0 in the %s place." % (" or ".join(emp), " and ".join(emp))
    return s


def discs_e(h, t, o):
    x = 100 * h + 10 * t + o
    parts = ["%s of %d = %d" % (unit(c, "disc"), 10 ** i, c * 10 ** i) for i, c in ((2, h), (1, t), (0, o)) if c]
    s = "Find the value of each group of discs: %s. Then put them together: %d." % (", ".join(parts), x)
    emp = [PL[i] for i, d in ((1, t), (0, o)) if d == 0]
    if emp:
        s += " There are no %d discs, so write 0 in the %s place." % (10 ** (1 if emp[0] == "tens" else 0), emp[0])
    return s


# ============================================================ set 1: hundreds, tens and ones
def set_place():
    S = {}
    for key, (h, t, o), wrong, extra in [
            ("b1", (2, 3, 4), [432, 9, 243], "Start with the flats: 200. Then the rods: 230. Then the cubes: 234."),
            ("b2", (1, 5, 2), [251, 8, 125], "Count the flats, then the rods, then the small cubes."),
            ("b3", (3, 0, 6), [36, 360, 9], ""),
            ("b4", (4, 2, 0), [42, 402, 6], ""),
            ("b5", (2, 6, 5), [562, 13, 256], "Count the rods in tens: 10, 20, 30, 40, 50, 60."),
            ("b6", (6, 1, 3), [316, 10, 631], "Count the flats in hundreds: 100, 200 … 600.")]:
        x = 100 * h + 10 * t + o
        S[key] = mcq_n(fig(blocks_svg(h, t, o)) + "What number do the blocks show?", x, wrong,
                       (blocks_e(h, t, o) + " " + extra).strip())
    for key, (h, t, o), wrong in [("d1", (3, 4, 2), [243, 9, 324]),
                                  ("d2", (5, 0, 8), [58, 580, 13]),
                                  ("d3", (2, 7, 0), [27, 207, 9])]:
        x = 100 * h + 10 * t + o
        S[key] = mcq_n(fig(discs_svg([h, t, o])) + "What number do the place value discs show?", x, wrong,
                       discs_e(h, t, o))
    S["ht"] = mcq_n(fig(blocks_svg(3, 5, 2)) + "How many tens are there?", 5, [3, 2, 50],
                    "Each rod is 1 ten. There are 5 rods, so there are 5 tens. The number is 352.")
    S["hh"] = mcq_n(fig(blocks_svg(4, 2, 6)) + "How many hundreds are there?", 4, [2, 6, 400],
                    "Each flat is 1 hundred. There are 4 flats, so there are 4 hundreds. The number is 426.")
    S["h0"] = mcq_n(fig(chart_svg(709)) + "How many tens are in 709?", 0, [7, 9, 70],
                    "709 is 7 hundreds, 0 tens and 9 ones. The 0 shows that there are no tens.")
    S["same1"] = mcq("Which is the same as 604?", "6 hundreds and 4 ones",
                     ["6 hundreds and 4 tens", "6 tens and 4 ones", "4 hundreds and 6 ones"],
                     "604 is 6 hundreds, 0 tens and 4 ones. That is 6 hundreds and 4 ones. "
                     "(6 hundreds and 4 tens is 640.)")
    S["same2"] = mcq("Which is the same as 851?", "8 hundreds, 5 tens and 1 one",
                     ["8 hundreds, 1 ten and 5 ones", "5 hundreds, 8 tens and 1 one", "1 hundred, 5 tens and 8 ones"],
                     "Read the digits from the left: 8 is in the hundreds place, 5 is in the tens place and 1 is in "
                     "the ones place. 851 = 8 hundreds, 5 tens and 1 one.")
    S["w1"] = mcq_n("Which number has 5 hundreds, 3 tens and 8 ones?", 538, [835, 16, 583],
                    "Write the hundreds digit first, then the tens, then the ones: 5, 3, 8. That is 538.")
    S["w2"] = mcq_n("Which number has 7 hundreds and 4 ones?", 704, [74, 740, 7004],
                    "There are no tens, so write 0 in the tens place: 7, 0, 4. That is 704.")
    S["w3"] = mcq_n("Which number has 2 hundreds and 9 tens?", 290, [29, 209, 2090],
                    "2 hundreds and 9 tens is 200 + 90 = 290. There are no ones, so the ones digit is 0.")
    S["k"] = mcq_n("How many hundreds make 1000?", 10, [100, 1, 1000],
                   "Count in hundreds: 100, 200, 300 … 1000. That is 10 hundreds. 10 hundreds make 1000.")
    S["ren"] = mcq_n(fig(blocks_svg(2, 12, 5)) + "What number do the blocks show?", 325, [2125, 225, 19],
                     "There are 12 rods. 10 tens make 1 hundred, so 12 tens = 1 hundred and 2 tens. "
                     "200 + 120 + 5 = 325.")
    S["th"] = mcq_n(fig(blocks_svg(10, 0, 0)) + "There are 10 flats. What number do they show?", 1000,
                    [10, 100, 900],
                    "Each flat is 100. Count in hundreds: 100, 200, 300 … 1000. 10 hundreds make 1000.")
    for v, w in [(200 + 120 + 5, 325), (10 * 100, 1000), (600 + 4, 604)]:
        assert v == w
    order = ["b1", "b2", "ht", "d1", "b3", "hh", "w1", "b4", "same1", "d2", "b5", "w2", "h0",
             "d3", "same2", "b6", "w3", "k", "ren", "th"]
    assert sorted(order) == sorted(S)
    return {"title": "Hundreds, tens and ones", "items": [S[k] for k in order]}


# ============================================================ set 2: read and write numbers in words
def set_words():
    S = {}
    for key, x, wrong in [("n1", 407, [47, 4007, 470]),
                          ("n2", 630, [6030, 603, 63]),
                          ("n3", 215, [250, 2015, 205]),
                          ("n4", 864, [8064, 846, 468]),
                          ("n5", 300, [3, 30, 3000]),
                          ("n6", 750, [715, 7050, 705]),
                          ("n7", 519, [590, 5019, 509]),
                          ("n8", 902, [92, 920, 9002])]:
        e = write_e(x)
        if x == 750:
            e += " Fifty is 5 tens. Fifteen is 15."
        if x == 519:
            e += " Nineteen is 19. Ninety is 9 tens."
        if x == 300:
            e += " Three thousand is 3000."
        S[key] = mcq_n("Write <b>%s</b> in numerals." % words(x), x, wrong, e)
    for key, x, wrong in [("t1", 407, [47, 470, 417]),
                          ("t2", 560, [506, 56, 516]),
                          ("t3", 318, [380, 308, 38]),
                          ("t4", 740, [704, 714, 74]),
                          ("t5", 913, [930, 903, 93]),
                          ("t6", 605, [65, 650, 615])]:
        e = "%d is %s. Say the hundreds, then the rest: %s." % (x, hto_n(x), words(x))
        if digit(x, 1) == 1:
            e += " 1 ten and %d ones is %s." % (digit(x, 0), w100(x % 100))
        S[key] = mcq("Which is %d in words?" % x, words(x), [words(w) for w in wrong], e)
    S["sp1"] = mcq("Which is the correct way to write 340 in words?", "three hundred and forty",
                   ["three hundred and fourty", "three hundred and four", "thirty-four"],
                   "340 is 3 hundreds and 4 tens. 4 tens is forty. Forty has no u: f-o-r-t-y.")
    S["sp2"] = mcq("Which is the correct way to write 290 in words?", "two hundred and ninety",
                   ["two hundred and ninty", "two hundred and nine", "twenty-nine"],
                   "290 is 2 hundreds and 9 tens. 9 tens is ninety. Ninety keeps the e: n-i-n-e-t-y.")
    S["c1"] = mcq(fig(chart_svg(806)) + "Write this number in words.", words(806),
                  [words(86), words(860), words(816)],
                  "The chart shows 8 hundreds, 0 tens and 6 ones: 806. In words: eight hundred and six.")
    S["c2"] = mcq(fig(chart_svg(470)) + "Write this number in words.", words(470),
                  [words(407), words(47), words(417)],
                  "The chart shows 4 hundreds, 7 tens and 0 ones: 470. 7 tens is seventy. "
                  "In words: four hundred and seventy.")
    S["siti"] = mcq_n("Siti writes “three hundred and nine” as 3009. What is the correct numeral?", 309,
                      [39, 390, 3009],
                      "Three hundred and nine is 3 hundreds, 0 tens and 9 ones: 309. "
                      "A number in the hundreds has only 3 digits, so do not write 300 and then 9.")
    S["k"] = mcq("Write <b>one thousand</b> in numerals.", "1000", ["100", "10" + NB + "000", "10"],
                 "One thousand is 10 hundreds: 1000. It has 1 and three zeros.")
    order = ["n1", "t1", "n2", "sp1", "c1", "n3", "t2", "n5", "t3", "k", "n4", "c2", "t4",
             "n6", "sp2", "t5", "n7", "t6", "n8", "siti"]
    assert sorted(order) == sorted(S)
    return {"title": "Read and write numbers in words", "items": [S[k] for k in order]}


# ============================================================ set 3: compare and order
def first_diff(a, b):
    for i in (2, 1, 0):
        if digit(a, i) != digit(b, i):
            return i


def compare_e(big, small):
    if len(str(big)) != len(str(small)):
        return ("%d has %d digits and %d has only %d. So %d is greater."
                % (big, len(str(big)), small, len(str(small)), big))
    i = first_diff(big, small)
    lead = "Compare the hundreds" if i == 2 else "The %s are the same, so compare the %s" % (
        " and ".join(PL[x] for x in (2, 1) if x > i), PL[i])
    return "%s: %s is more than %s. So %d is greater than %d." % (
        lead, plural(digit(big, i), i), plural(digit(small, i), i), big, small)


def set_compare():
    S = {}
    for key, nums, kind in [("g1", [470, 407, 74, 447], "greatest"),
                            ("s1", [289, 298, 829, 892], "smallest"),
                            ("g2", [530, 503, 350, 305], "greatest"),
                            ("s2", [99, 909, 990, 199], "smallest"),
                            ("g3", [1000, 999, 990, 100], "greatest"),
                            ("s3", [602, 612, 621, 620], "smallest")]:
        ans = max(nums) if kind == "greatest" else min(nums)
        assert nums[0] == ans
        rest = sorted(nums[1:], reverse=(kind == "greatest"))
        if kind == "greatest":
            e = compare_e(ans, rest[0]) + " %d is the greatest." % ans
        else:
            e = compare_e(rest[0], ans) + " %d is the smallest." % ans
        if key == "s2":
            e = "99 has only 2 digits. The others have 3 digits. So 99 is the smallest, even though 9 is a big digit."
        if key == "g3":
            e = "1000 has 4 digits. The others have only 3 digits. 1000 is 1 more than 999, so 1000 is the greatest."
        S[key] = mcq_n("Which number is the %s?" % kind, ans, nums[1:], e)
    for key, x, y in [("c1", 407, 470), ("c2", 352, 325), ("c3", 98, 189), ("c4", 760, 706), ("c5", 999, 1000)]:
        lt = "&lt;" if x < y else "&gt;"
        gt = "&gt;" if x < y else "&lt;"
        e = compare_e(max(x, y), min(x, y))
        e += " So %d %s %d." % (x, lt, y)
        if key == "c3":
            e += " Do not look only at the first digit. Count the digits first."
        S[key] = mcq("Which is correct?", "%d %s %d" % (x, lt, y),
                     ["%d %s %d" % (x, gt, y), "%d = %d" % (x, y), "%d %s %d" % (y, lt, x)], e)
    S["o1"] = mcq("Arrange the numbers in order, beginning with the smallest: 371, 317, 731", "317, 371, 731",
                  ["371, 317, 731", "731, 371, 317", "317, 731, 371"],
                  "731 has 7 hundreds, so it is the greatest. 317 and 371 both have 3 hundreds. "
                  "Tens: 1 ten &lt; 7 tens, so 317 &lt; 371. Order: 317, 371, 731.")
    S["o2"] = mcq("Arrange the numbers in order, beginning with the smallest: 560, 506, 56", "56, 506, 560",
                  ["506, 56, 560", "56, 560, 506", "560, 506, 56"],
                  "56 has only 2 digits, so it is the smallest. 506 and 560 both have 5 hundreds. "
                  "Tens: 0 tens &lt; 6 tens, so 506 &lt; 560. Order: 56, 506, 560.")
    S["o3"] = mcq("Arrange the numbers in order, beginning with the greatest: 849, 894, 489", "894, 849, 489",
                  ["489, 849, 894", "849, 894, 489", "894, 489, 849"],
                  "489 has only 4 hundreds, so it is the smallest. 849 and 894 both have 8 hundreds. "
                  "Tens: 9 tens &gt; 4 tens, so 894 &gt; 849. Order: 894, 849, 489.")
    S["o4"] = mcq("Arrange the numbers in order, beginning with the smallest: 625, 652, 256, 265", "256, 265, 625, 652",
                  ["265, 256, 652, 625", "652, 625, 265, 256", "256, 625, 265, 652"],
                  "256 and 265 have 2 hundreds, so they come first: 5 tens &lt; 6 tens, so 256 &lt; 265. "
                  "625 and 652 have 6 hundreds: 2 tens &lt; 5 tens. Order: 256, 265, 625, 652.")
    S["dg1"] = mcq_n("Use the digits 3, 8 and 5 once each. What is the greatest 3-digit number you can make?",
                     853, [835, 358, 583],
                     "Put the biggest digit in the hundreds place, then the next biggest: 8, 5, 3. That is 853.")
    S["dg2"] = mcq_n("Use the digits 6, 0 and 2 once each. What is the smallest 3-digit number you can make?",
                     206, [26, 260, 602],
                     "A 3-digit number cannot start with 0. Put the smaller of 2 and 6 first: 2. Then 0, then 6: 206. "
                     "(026 is just 26, which has only 2 digits.)")
    S["dg3"] = mcq_n("Use the digits 7, 0 and 4 once each. What is the greatest 3-digit number you can make?",
                     740, [704, 470, 407],
                     "Biggest digit first: 7. Then 4. The 0 goes last, in the ones place: 740.")
    S["bt1"] = mcq_n("Which number is between 600 and 650?", 628, [682, 599, 660],
                     "628 has 6 hundreds and 2 tens, so it is more than 600 and less than 650. "
                     "682 and 660 are more than 650. 599 is less than 600.")
    S["bt2"] = mcq_n("Which number is greater than 509 but smaller than 590?", 550, [505, 595, 509],
                     "550 is greater than 509 (5 tens &gt; 0 tens) and smaller than 590 (5 tens &lt; 9 tens). "
                     "505 is smaller than 509, 595 is greater than 590, and 509 is not greater than itself.")
    for a, b in [(317, 371), (371, 731), (56, 506), (506, 560), (489, 849), (849, 894), (256, 265), (265, 625),
                 (625, 652), (600, 628), (628, 650), (509, 550), (550, 590)]:
        assert a < b
    order = ["g1", "c1", "s1", "dg1", "c2", "g2", "o1", "s2", "bt1", "c3", "o2", "dg2", "g3",
             "c4", "s3", "o3", "bt2", "dg3", "c5", "o4"]
    assert sorted(order) == sorted(S)
    return {"title": "Compare and order numbers", "items": [S[k] for k in order]}


# ============================================================ set 4: count in tens and hundreds
def set_count():
    S = {}
    for key, seq, ans, wrong, e in [
            ("s1", [230, 240, 250], 260, [251, 350, 270],
             "Count on in tens: each number is 10 more. Only the tens digit goes up. 250 + 10 = 260."),
            ("s2", [200, 300, 400], 500, [410, 401, 600],
             "Count on in hundreds: each number is 100 more. 400 + 100 = 500."),
            ("s3", [145, 245, 345], 445, [355, 346, 545],
             "Count on in hundreds: only the hundreds digit goes up. 3 hundreds → 4 hundreds: 445."),
            ("s4", [480, 470, 460], 450, [360, 459, 440],
             "Count back in tens: each number is 10 less. 460 − 10 = 450."),
            ("s5", [906, 806, 706], 606, [696, 705, 506],
             "Count back in hundreds: only the hundreds digit goes down. 706 − 100 = 606."),
            ("s6", [570, 580, 590], 600, [5100, 591, 690],
             "590 + 10: 9 tens + 1 ten = 10 tens. Rename 10 tens as 1 hundred: 5 hundreds become 6 hundreds. "
             "The answer is 600, not 5100."),
            ("s7", [720, 710, 700], 690, [600, 699, 680],
             "Count back in tens: 700 − 10 = 690. 700 is 70 tens, and 1 ten less is 69 tens = 690.")]:
        q = "What comes next?<br><b>%s, ☐</b>" % ", ".join(map(str, seq))
        step = seq[1] - seq[0]
        assert seq[2] - seq[1] == step and seq[2] + step == ans
        S[key] = mcq_n(q, ans, wrong, e)
    S["mis"] = mcq_n("What is the missing number?<br><b>610, 620, ☐, 640</b>", 630, [621, 720, 650],
                     "Count on in tens: 610, 620, 630, 640. 620 + 10 = 630.")
    S["b1"] = mcq_n(fig(blocks_svg(2, 4, 5)) + "Add 1 more ten. What number is it now?", 255, [246, 345, 265],
                    "The blocks show 245. 1 more ten is 10 more: 245 + 10 = 255. Only the tens digit changes.")
    S["b2"] = mcq_n(fig(blocks_svg(1, 3, 6)) + "Add 1 more hundred. What number is it now?", 236, [137, 146, 336],
                    "The blocks show 136. 1 more hundred is 100 more: 136 + 100 = 236. "
                    "Only the hundreds digit changes.")
    S["b3"] = mcq_n(fig(blocks_svg(3, 9, 2)) + "Add 1 more ten. What number is it now?", 402, [3102, 393, 492],
                    "The blocks show 392. Add 1 rod: now there are 10 rods. Rename 10 tens as 1 hundred. "
                    "That is 4 hundreds, 0 tens and 2 ones: 402.")
    S["l1"] = mcq_n(fig(line_svg(0, 1000, 100, [0, 500, 1000], arrow=800)) + "What number does the arrow point to?",
                    800, [80, 700, 900],
                    "From 0 to 1000 there are 10 equal jumps, so each jump is 100. "
                    "The arrow is 3 jumps after 500: 600, 700, 800.")
    S["l2"] = mcq_n(fig(line_svg(300, 400, 10, [300, 350, 400], arrow=370)) + "What number does the arrow point to?",
                    370, [307, 360, 380],
                    "From 300 to 400 there are 10 equal jumps, so each jump is 10, not 1. "
                    "The arrow is 2 jumps after 350: 360, 370.")
    S["l3"] = mcq_n(fig(line_svg(200, 300, 10, [200, 250, 300], arrow=230)) + "What number does the arrow point to?",
                    230, [203, 220, 240],
                    "Each jump is 10. Count on in tens from 200: 210, 220, 230. (203 counts each jump as 1.)")
    S["m1"] = mcq_n("What number is 10 more than 695?", 705, [696, 795, 605],
                    "695 + 10: 9 tens + 1 ten = 10 tens = 1 hundred. So 6 hundreds become 7 hundreds and the tens "
                    "digit becomes 0: 705. (795 is 100 more. 696 is 1 more.)")
    S["m2"] = mcq_n("What number is 100 less than 1000?", 900, [990, 999, 800],
                    "1000 is 10 hundreds. 1 hundred less is 9 hundreds = 900. (990 is 10 less. 999 is 1 less.)")
    S["m3"] = mcq_n("What number is 100 more than 856?", 956, [866, 857, 846],
                    "100 more: the hundreds digit goes up by 1. 8 hundreds → 9 hundreds: 956. (866 is 10 more.)")
    S["m4"] = mcq_n("What number is 10 less than 403?", 393, [402, 303, 413],
                    "403 has 0 tens. Take 1 hundred and rename it as 10 tens: 3 hundreds and 10 tens. "
                    "Take away 1 ten: 3 hundreds, 9 tens and 3 ones = 393. (303 is 100 less.)")
    S["t1"] = mcq_n("How many tens are there in 300?", 30, [3, 300, 10],
                    "1 hundred is 10 tens. So 3 hundreds are 10 + 10 + 10 = 30 tens.")
    S["t2"] = mcq_n("40 tens = ☐. What number goes in the box?", 400, [40, 4000, 140],
                    "10 tens make 1 hundred. 40 tens are 4 groups of 10 tens: 4 hundreds = 400.")
    for v, w in [(245 + 10, 255), (136 + 100, 236), (392 + 10, 402), (695 + 10, 705), (1000 - 100, 900),
                 (856 + 100, 956), (403 - 10, 393), (30 * 10, 300), (40 * 10, 400)]:
        assert v == w
    order = ["s1", "s2", "l1", "b1", "s3", "mis", "s4", "b2", "l3", "s5", "t1", "m3", "l2",
             "s6", "b3", "m1", "s7", "t2", "m4", "m2"]
    assert sorted(order) == sorted(S)
    return {"title": "Count in tens and hundreds", "items": [S[k] for k in order]}


# ============================================================ set 5: number patterns and word problems
def set_patterns():
    S = {}
    S["r1"] = mcq("What is the rule for this pattern?<br><b>312, 322, 332, 342</b>", "Add 10",
                  ["Add 1", "Add 100", "Subtract 10"],
                  "The numbers get bigger. 322 − 312 = 10. The tens digit goes up by 1 each time. The rule is “add 10”.")
    S["r2"] = mcq("What is the rule for this pattern?<br><b>865, 765, 665, 565</b>", "Subtract 100",
                  ["Add 100", "Subtract 10", "Subtract 1"],
                  "The numbers get smaller. 865 − 765 = 100. The hundreds digit goes down by 1 each time. "
                  "The rule is “subtract 100”.")
    S["p1"] = mcq_n("What is the missing number?<br><b>455, 465, ☐, 485, 495</b>", 475, [466, 565, 470],
                    "Each number is 10 more: 455, 465, 475, 485, 495. 465 + 10 = 475.")
    S["p2"] = mcq_n("What is the missing number?<br><b>980, ☐, 780, 680</b>", 880, [970, 890, 800],
                    "Each number is 100 less: 980, 880, 780, 680. 980 − 100 = 880. (970 is 10 less.)")
    S["p3"] = mcq_n("Count on in fives. What comes next?<br><b>735, 740, 745, ☐</b>", 750, [746, 755, 845],
                    "Each number is 5 more. 745 + 5 = 750. (755 adds 10. 845 adds 100.)")
    S["p4"] = mcq_n("What is the 5th number in this pattern?<br><b>120, 220, 320, …</b>", 520, [420, 160, 620],
                    "Each number is 100 more. 120 (1st), 220 (2nd), 320 (3rd), 420 (4th), 520 (5th).")
    S["p5"] = mcq_n("What comes next?<br><b>1000, 900, 800, ☐</b>", 700, [790, 600, 810],
                    "Each number is 100 less. 800 − 100 = 700. (790 is only 10 less. 600 is 200 less. 810 adds 10.)")
    # ---- word problems
    S["ali"] = mcq_n("Ali has 3 boxes of 100 stickers, 4 packets of 10 stickers and 5 loose stickers. "
                     "How many stickers does he have?", 345, [12, 543, 3045],
                     "3 boxes of 100 = 300. 4 packets of 10 = 40. 300 + 40 + 5 = 345. "
                     "(Do not just add 3 + 4 + 5.)")
    S["cups"] = mcq_n("Mrs Lim buys 6 packs of paper cups for Children’s Day. Each pack has 100 cups. "
                      "How many cups does she buy?", 600, [6, 106, 60],
                      "Count in hundreds 6 times: 100, 200, 300, 400, 500, 600. 6 hundreds = 600.")
    S["stamps"] = mcq_n(fig(bar_svg([("Mei Ling", [(356, False)], [(0, 0, "356")]),
                                     ("Jun Jie", [(356, False), (100, False)], [(1, 1, "100")], "?")],
                                    label="bar model: Mei Ling and Jun Jie"))
                        + "Mei Ling has 356 stamps. Jun Jie has 100 more stamps than Mei Ling. "
                          "How many stamps does Jun Jie have?", 456, [256, 366, 1356],
                        "Jun Jie’s bar is Mei Ling’s bar and 100 more. 356 + 100 = 456. "
                        "Only the hundreds digit changes. (366 is 10 more. 256 is 100 fewer.)")
    S["pages"] = mcq_n(fig(bar_svg([("Raju", [(285, False)], [(0, 0, "285")]),
                                    ("Priya", [(275, False), (10, True)], [(0, 0, "?")], "10 fewer")],
                                   label="bar model: Raju and Priya"))
                       + "Raju reads 285 pages. Priya reads 10 fewer pages than Raju. "
                         "How many pages does Priya read?", 275, [295, 185, 284],
                       "Priya’s bar is 10 shorter than Raju’s. 285 − 10 = 275. "
                       "(295 is 10 more. 185 is 100 fewer.)")
    S["hawker"] = mcq("A hawker centre sells 638 plates of chicken rice and 683 bowls of laksa on Saturday. "
                      "Which does it sell more of?", "Laksa",
                      ["Chicken rice", "They are the same", "You cannot tell"],
                      "Both numbers have 6 hundreds. Compare the tens: 8 tens &gt; 3 tens. So 683 &gt; 638. "
                      "It sells more laksa.")
    S["lib"] = mcq_n("The school library has “seven hundred and eight” story books. Write the number of books "
                     "in numerals.", 708, [78, 780, 7008],
                     "Seven hundred and eight is 7 hundreds, 0 tens and 8 ones: 708. "
                     "Write 0 for the empty tens place.")
    S["hafiz"] = mcq_n("Hafiz thinks of a 3-digit number. It has 6 hundreds, 5 ones and no tens. "
                       "What is his number?", 605, [65, 650, 6005],
                       "6 hundreds, 0 tens and 5 ones: 605. The 0 holds the tens place.")
    S["cans"] = mcq("For a recycling drive, Class 2A collects 246 cans, Class 2B collects 264 cans and "
                    "Class 2C collects 226 cans. Which class collects the most cans?", "Class 2B",
                    ["Class 2A", "Class 2C", "They collect the same"],
                    "All three numbers have 2 hundreds. Compare the tens: 6 tens is the most. "
                    "264 is the greatest, so Class 2B collects the most.")
    S["ryan"] = mcq_n("Ryan has 470 points in a game. He gets 10 points for each star. He gets 3 more stars. "
                      "How many points does he have now?", 500, [473, 770, 490],
                      "Count on in tens 3 times: 480, 490, 500. (473 adds 3 ones. 770 adds 3 hundreds.)")
    S["xinyi"] = mcq_n("Xin Yi’s number is 10 less than 600. What is her number?", 590, [500, 610, 599],
                       "600 is 60 tens. 1 ten less is 59 tens = 590. (500 is 100 less. 599 is 1 less.)")
    S["beads"] = mcq_n(fig(bar_svg([("Box A", [(300, False)], [(0, 0, "300")]),
                                    ("Box B", [(200, False)], [(0, 0, "200")])], total="?",
                                   label="bar model: Box A and Box B"))
                       + "Box A has 300 beads. Box B has 200 beads. How many beads are there in all?", 500,
                       [100, 5, 400],
                       "3 hundreds and 2 hundreds make 5 hundreds. Count on in hundreds from 300: 400, 500. "
                       "There are 500 beads.")
    S["paper"] = mcq_n(fig(bar_svg([("Paper", [(900, False), (100, False)], [(0, 0, "?"), (1, 1, "100")])],
                                   total="1000", label="bar model: 1000 sheets of paper"))
                       + "Mr Tan has 1000 sheets of paper. He gives away 100 sheets. How many sheets does he have "
                         "left?", 900, [990, 800, 999],
                       "1000 is 10 hundreds. Take away 1 hundred: 9 hundreds = 900. "
                       "(990 takes away only 10.)")
    S["ethan"] = mcq_n("Ethan counts on in tens from 340: 350, 360, … He stops at 400. "
                       "How many numbers does he say after 340?", 6, [60, 4, 5],
                       "He says 350, 360, 370, 380, 390, 400. That is 6 numbers. "
                       "(400 − 340 = 60, and 60 is 6 tens.)")
    for v, w in [(300 + 40 + 5, 345), (6 * 100, 600), (356 + 100, 456), (285 - 10, 275), (470 + 30, 500),
                 (600 - 10, 590), (300 + 200, 500), (1000 - 100, 900), ((400 - 340) // 10, 6), (120 + 400, 520)]:
        assert v == w
    order = ["r1", "p1", "p3", "r2", "p2", "p4", "p5", "ali", "cups", "stamps", "lib", "hawker", "hafiz",
             "pages", "ryan", "cans", "xinyi", "beads", "paper", "ethan"]
    assert sorted(order) == sorted(S)
    return {"title": "Number patterns and word problems", "items": [S[k] for k in order]}


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
        "<h2>Hundreds, tens and ones</h2>"
        "<p>A 3-digit number has three places: <b>hundreds</b>, <b>tens</b> and <b>ones</b>. "
        "10 ones make 1 ten. 10 tens make 1 hundred. 10 hundreds make 1000.</p>"
        "<figure class='sn-fig'>" + blocks_svg(3, 4, 6, labels=True) +
        "<figcaption>346 is 3 hundreds, 4 tens and 6 ones. A flat is 100, a rod is 10 and a small cube is 1."
        "</figcaption></figure>"
        "<p>A place value chart shows the digit in each place. The place tells you what the digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(345, hi=1) +
        "<figcaption>In 345 the digit 4 is in the tens place. Its value is 4 tens, or 40.</figcaption></figure>"
        "<h2>Reading and writing numbers</h2>"
        "<p>Say the hundreds first, then “and”, then the tens and ones. "
        "If a place is empty, write <b>0</b> there. The 0 keeps the other digits in the right places.</p>"
        + table(["Numeral", "Words"], [[str(x), words(x)] for x in (407, 470, 515, 300, 1000)])
        + ex("Words to numerals", "Write four hundred and seven in numerals.",
             "4 hundreds, 0 tens and 7 ones. Write 4, 0, 7.", "407 (not 47 or 4007)")
        + "<h2>Comparing and ordering</h2>"
        "<p>First count the digits: a 3-digit number is greater than a 2-digit number. "
        "If both have 3 digits, compare the hundreds, then the tens, then the ones.</p>"
        + ex("Compare", "Which is greater, 407 or 470?",
             "Hundreds: 4 = 4. Tens: 0 tens &lt; 7 tens.", "470 is greater. 407 &lt; 470")
        + "<p>&gt; means “is greater than”. &lt; means “is smaller than”. The open side faces the greater number.</p>"
        "<h2>Counting in tens and hundreds</h2>"
        "<p>Counting on in tens changes the tens digit: 230, 240, 250. "
        "Counting on in hundreds changes the hundreds digit: 145, 245, 345. "
        "When there are 10 tens, rename them as 1 hundred: 580, 590, 600.</p>"
        "<figure class='sn-fig'>" + line_svg(300, 400, 10, [300, 350, 400], arrow=370) +
        "<figcaption>From 300 to 400 there are 10 jumps, so each jump is 10. The arrow is at 370.</figcaption></figure>"
        "<h2>Patterns and word problems</h2>"
        "<p>To find the rule of a pattern, find how much each number goes up or down. "
        "In a word problem, draw a bar model to see what to find.</p>"
        "<figure class='sn-fig'>" + bar_svg([("Mei Ling", [(356, False)], [(0, 0, "356")]),
                                            ("Jun Jie", [(356, False), (100, False)], [(1, 1, "100")], "?")],
                                           label="bar model: Mei Ling and Jun Jie") +
        "<figcaption>Jun Jie has 100 more stamps than Mei Ling. 356 + 100 = 456.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving out the zero (four hundred and seven → 47)", "Write 0 for the empty tens place: 407"],
            ["Writing each part you hear (four hundred and seven → 4007)", "A number in the hundreds has 3 digits: 407"],
            ["Mixing up 407 and 470", "407 has 0 tens and 7 ones. 470 has 7 tens and 0 ones"],
            ["Giving the digit, not its value (the 4 in 345 is 4)", "The 4 is in the tens place: 40"],
            ["Comparing the first digits only (99 &gt; 189)", "Count the digits first: 189 &gt; 99"],
            ["Not renaming when counting in tens (590, 5100)", "10 tens make 1 hundred: 590, 600"],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 numbers to 1000?",
     "a": "Primary 2 students count in tens and hundreds, read and write numbers up to 1000 in numerals and in words, "
          "find the value of each digit, compare and order numbers, and continue number patterns."},
    {"q": "How do I explain place value to my child?",
     "a": "Use bundles or blocks: 10 ones make a ten and 10 tens make a hundred. Then 346 is 3 hundreds, 4 tens and "
          "6 ones, so the 4 is worth 40."},
    {"q": "What is the most common mistake with numbers to 1000?",
     "a": "The most common mistake is leaving out a zero, such as writing four hundred and seven as 47. "
          "Children also mix up 407 and 470, or give the digit instead of its value."},
    {"q": "Is numbers to 1000 in the MOE syllabus?",
     "a": "Yes. Numbers up to 1000, including counting in tens and hundreds, place values, reading and writing, "
          "comparing and ordering, and patterns, are part of Whole Numbers in the MOE 2021 Primary 2 Mathematics "
          "syllabus."},
]


def mark_large(u, pattern):
    """Tag wide pictures (blocks, discs, place value charts, number lines, bar models) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(62801)
    sets = [set_place(), set_words(), set_compare(), set_count(), set_patterns()]
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
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "numbers-to-1000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Numbers to 1000",
        "seo_title": "P2 Numbers to 1000 Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Numbers to 1000",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Numbers up to 1000: counting in tens/hundreds, place values, reading and writing, "
                         "comparing and ordering, patterns",
        "meta_desc": "Free P2 maths practice on numbers to 1000: place value, numerals and words, comparing, ordering, "
                     "counting in tens and hundreds. 100 questions with answers.",
        "key_big": "Write 0 for an empty place: four hundred and seven is 407, not 47.",
        "key_sub": "In 345 the digit 4 is in the tens place, so its value is 40.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(base ten blocks|place value chart|place value discs|number line|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
