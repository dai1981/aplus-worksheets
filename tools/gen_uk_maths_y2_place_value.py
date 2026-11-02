# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Place Value to 100 (National Curriculum in England, Year 2: Number and place value)
  python tools/gen_uk_maths_y2_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Year 2: numbers up to 100, very short sentences for 6-7 year olds, many pictures.
Wrong answers come from real mistakes: 47 written as 74 or 407, giving the digit instead of its value
(the 4 in 47 is 4), adding the digits (4 + 7 = 11), comparing by the ones digit, fourteen / forty,
and spelling slips (fourty, ninty, forteen).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#c98a3d"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e, rnd):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    ch = wrong + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, wrong, e, rnd, unit=""):
    assert all(isinstance(w, int) and w >= 0 and w != correct for w in wrong), (q, correct, wrong)
    it = mcq(q, correct, wrong, e, rnd)
    if unit:
        it["c"] = [x + unit for x in it["c"]]
    return it


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def unit(k, one, many):
    return "%d %s" % (k, one if k == 1 else many)


def T(k):
    return unit(k, "ten", "tens")


def O(k):
    return unit(k, "one", "ones")


def TO(t, o):
    return "%s and %s" % (T(t), O(o))


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


# ------------------------------------------------------------ number words
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    if n == 100:
        return "one hundred"
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


# ------------------------------------------------------------ figures
U = 8                      # one small cube = U x U, a rod = U x 10U
RG, CG, GG, M = 6, 4, 22, 6


def blocks_svg(t, o, labels=False):
    """Base-ten blocks: t ten rods, o ones cubes (columns of 5). Sizes are exact (1 : 10)."""
    F = 10 * U
    groups = []

    def rods(x, y):
        s = []
        for k in range(t):
            rx = x + k * (U + RG)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (rx, y, U, F, FILL, GREEN))
            for i in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (rx, y + i * U, rx + U, y + i * U, GREEN))
        return s

    ccols = (o + 4) // 5

    def cubes(x, y):
        s = []
        for k in range(o):
            cx = x + (k // 5) * (U + CG + 2)
            cy = y + (k % 5) * (U + CG + 4)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, U, U, CUBE, GREEN))
        return s

    if t:
        groups.append((t * U + (t - 1) * RG, F, rods, T(t)))
    if o:
        groups.append((ccols * U + (ccols - 1) * (CG + 2), 5 * U + 4 * (CG + 4), cubes, O(o)))
    lab_w = lambda s: int(len(s) * 8.6) + 4
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * M + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * M + body_h + (26 if labels else 0)
    s = []
    x = M
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, M)
        if labels:
            s.append(text(x + w / 2, M + body_h + 20, lab))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base-ten blocks")


SW, SH = 4, 56             # straw spacing in a bundle, straw height


def straws_svg(b, loose):
    """b bundles of 10 straws (with a band) and some loose straws."""
    bw = 9 * SW + 4
    LS = 9
    W = 2 * M + b * bw + (b - 1) * 12 + (GG + (loose - 1) * LS + 4 if loose else 0)
    Hh = 2 * M + SH
    s = []
    x = M
    for k in range(b):
        for i in range(10):
            sx = x + 2 + i * SW
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (sx, M + 2, sx, M + SH - 2, WOOD))
        s.append("<rect x='%d' y='%d' width='%d' height='7' rx='2' fill='%s'/>" % (x - 1, M + SH // 2 - 3, bw + 2, RED))
        x += bw + 12
    if loose:
        x += GG - 12
        for i in range(loose):
            sx = x + 2 + i * LS
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (sx, M + 2, sx, M + SH - 2, WOOD))
    return svg_wrap(W, Hh, "".join(s), "bundles of straws")


CW, HEAD, ROW = 80, 32, 48


def chart_svg(n, hi=None):
    """Tens / ones chart with n in it. hi = 1 (tens) or 0 (ones) to colour red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 2 * CW, 2 * y0 + HEAD + ROW
    t, o = divmod(n, 10)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 2 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 2 * CW, HEAD, FILL)]
    for k, (lab, d, place) in enumerate([("Tens", t, 1), ("Ones", o, 0)]):
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append(text(cx, y0 + 22, lab, 16))
        s.append(text(cx, y0 + HEAD + 35, str(d), 30, col=RED if hi == place else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 2 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "tens and ones chart showing %d" % n)


def number_line_svg(lo, hi, step, labels, arrow, show=None):
    """Number line lo..hi with a tick every step, numbers under `labels` and a red arrow at `arrow`."""
    L, R, Y = 30, 430, 58
    W, Hh = 460, 100

    def X(v):
        return L + (v - lo) * (R - L) / (hi - lo)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, R + 10, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, str(v), 15, col=GREEN))
        v += step
    ax = X(arrow)
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    if show:
        s.append(text(min(max(ax, 60), W - 60), Y - 44, show, 15, col=RED))
    top = 18 if show else 0
    body = "".join(s)
    if top:
        body = "<g transform='translate(0 %d)'>%s</g>" % (top, body)
    return svg_wrap(W, Hh + top, body, "number line from %d to %d" % (lo, hi))


# ============================================================ set 1: tens and ones
def count_e(t, o, what="blocks"):
    n = 10 * t + o
    if what == "blocks":
        s = "A rod is 10. A small cube is 1. "
        s += "Count the rods in tens: %s. " % ", ".join(str(10 * i) for i in range(1, t + 1))
    else:
        s = "A bundle is 10 straws. Count the bundles in tens: %s. " % ", ".join(str(10 * i) for i in range(1, t + 1))
    if o:
        s += "Then add %s: %d + %d = %d." % (O(o), 10 * t, o, n)
    else:
        s += "There are no ones, so write 0 in the ones place: %d." % n
    return s


def set_tens_ones(rnd):
    blocks = []
    for t, o, wrong in [(2, 5, [52, 205, 7]), (3, 8, [83, 308, 11]), (6, 0, [6, 16, 600]),
                        (5, 2, [25, 502, 62]), (7, 4, [47, 704, 64])]:
        n = 10 * t + o
        e = count_e(t, o)
        if n == 25:
            e += " Each rod is 10, not 1."
        blocks.append(mcq_n(fig(blocks_svg(t, o)) + "What number do the blocks show?", n, wrong, e, rnd))
    straws = []
    for t, o, wrong in [(4, 6, [64, 406, 10]), (1, 9, [91, 109, 10]), (8, 3, [38, 803, 11])]:
        n = 10 * t + o
        straws.append(mcq_n(fig(straws_svg(t, o)) + "How many straws are there?", n, wrong, count_e(t, o, "straws"), rnd))
    match = []
    for t, o in [(3, 6), (5, 9)]:
        wrong = [TO(o, t), TO(t, o + 1), TO(t + 1, o)]
        match.append(mcq(fig(blocks_svg(t, o)) + "Which matches the blocks?", TO(t, o), wrong,
                         "Count the rods: %s. Count the small cubes: %s. The number is %d."
                         % (T(t), O(o), 10 * t + o), rnd))
    red = []
    for n, place, wrong in [(63, 1, [6, 3, 63]), (28, 0, [80, 2, 28]), (91, 1, [9, 1, 91])]:
        d = n // 10 if place else n % 10
        v = d * 10 if place else d
        e = ("The red %d is in the %s place. It is worth %s = %d."
             % (d, "tens" if place else "ones", T(d) if place else O(d), v))
        if place:
            e += " The digit is %d, but its value is %d." % (d, v)
        red.append(mcq_n(fig(chart_svg(n, place)) + "What is the red digit worth?", v, wrong, e, rnd))
    val = []
    for n, d, wrong in [(47, 4, [4, 7, 47]), (85, 5, [50, 8, 85]), (72, 7, [7, 2, 72])]:
        place = 1 if n // 10 == d else 0
        v = d * 10 if place else d
        e = "In %d the %d is in the %s place, so it is worth %d." % (n, d, "tens" if place else "ones", v)
        if place:
            e += " %d is %s." % (n, TO(n // 10, n % 10))
        val.append(mcq_n("What is the %d in %d worth?" % (d, n), v, wrong, e, rnd))
    how = [
        mcq_n("How many tens are in 58?", 5, [8, 50, 58], "58 is 5 tens and 8 ones. There are 5 tens.", rnd),
        mcq_n("How many ones are in 36?", 6, [3, 60, 36], "36 is 3 tens and 6 ones. There are 6 ones.", rnd),
        mcq_n("How many tens are in 90?", 9, [0, 90, 10], "90 is 9 tens and 0 ones. There are 9 tens.", rnd),
    ]
    which = [mcq_n("Which number has 3 ones and 8 tens?", 83, [38, 803, 11],
                   "Write the tens first, then the ones. 8 tens and 3 ones make 83.", rnd)]
    order = (blocks[:2] + straws[:1] + match[:1] + how[:2] + blocks[2:3] + red[:1] + val[:1] + straws[1:2]
             + blocks[3:4] + red[1:2] + match[1:] + how[2:] + val[1:2] + straws[2:] + blocks[4:] + red[2:]
             + which + val[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Tens and ones", "items": order}


# ============================================================ set 2: partition
def set_partition(rnd):
    miss = [
        mcq_n("47 = 40 + ☐", 7, [4, 70, 47], "47 is 4 tens and 7 ones. 4 tens = 40. So 47 = 40 + 7.", rnd),
        mcq_n("63 = ☐ + 3", 60, [6, 3, 30], "63 is 6 tens and 3 ones. 6 tens = 60, not 6. So 63 = 60 + 3.", rnd),
        mcq_n("85 = 80 + ☐", 5, [8, 50, 85], "85 is 8 tens and 5 ones. 85 = 80 + 5.", rnd),
        mcq_n("☐ + 9 = 29", 20, [2, 90, 29], "29 is 2 tens and 9 ones. 2 tens = 20. So 20 + 9 = 29.", rnd),
        mcq_n("26 = 10 + ☐", 16, [6, 2, 36],
              "26 can be 1 ten and 16 ones. 10 + 16 = 26. (6 is wrong: 10 + 6 = 16.)", rnd),
    ]
    make = [
        mcq_n("What is 60 + 4?", 64, [604, 10, 46], "60 is 6 tens. 4 is 4 ones. 6 tens and 4 ones = 64. Not 604.", rnd),
        mcq_n("What is 7 + 50?", 57, [75, 507, 12],
              "50 is 5 tens and 7 is 7 ones. Tens come first: 57. The order you add them does not matter.", rnd),
        mcq_n("What is 4 tens and 9 ones?", 49, [94, 409, 13], "4 tens = 40. 40 + 9 = 49.", rnd),
        mcq_n("What is 8 tens and 0 ones?", 80, [8, 18, 800], "8 tens = 80. There are 0 ones, so the number is 80.", rnd),
    ]
    part = []
    for n, wrong in [(72, ["7 + 2", "20 + 7", "70 + 20"]), (38, ["3 + 8", "80 + 3", "30 + 80"]),
                     (56, ["5 + 6", "60 + 5", "50 + 60"])]:
        t, o = divmod(n, 10)
        part.append(mcq("Which shows %d split into tens and ones?" % n, "%d + %d" % (10 * t, o), wrong,
                        "%d is %s. %s = %d. So %d = %d + %d." % (n, TO(t, o), T(t), 10 * t, n, 10 * t, o), rnd))
    odd = []
    for t, o, wrong in [(3, 17, [317, 37, 20]), (2, 15, [215, 25, 17]), (5, 12, [512, 52, 17])]:
        n = 10 * t + o
        q = "What is %s?" % TO(t, o)
        if t == 3:
            q = fig(blocks_svg(t, o)) + "There are %s. What number is it?" % TO(t, o)
        odd.append(mcq_n(q, n, wrong,
                         "%s = %d. %s = 1 ten and %s. So %d + %d = %d." % (T(t), 10 * t, O(o), O(o - 10), 10 * t, o, n),
                         rnd))
    fill = [
        mcq_n("47 is 3 tens and ☐ ones.", 17, [7, 4, 10],
              "47 is 4 tens and 7 ones. Take 1 ten and make it 10 ones. Now there are 3 tens and 10 + 7 = 17 ones. "
              "Check: 30 + 17 = 47.", rnd),
        mcq_n("64 is 5 tens and ☐ ones.", 14, [4, 6, 10],
              "64 is 6 tens and 4 ones. Take 1 ten and make it 10 ones: 5 tens and 14 ones. Check: 50 + 14 = 64.", rnd),
    ]
    same = [
        mcq("Which is another way to make 52?", "4 tens and 12 ones",
            ["4 tens and 2 ones", "5 tens and 12 ones", "2 tens and 5 ones"],
            "52 is 5 tens and 2 ones. Take 1 ten and make it 10 ones: 4 tens and 12 ones. 40 + 12 = 52.", rnd),
        mcq("Which is the same as 36?", "2 tens and 16 ones",
            ["2 tens and 6 ones", "3 tens and 16 ones", "6 tens and 3 ones"],
            "36 is 3 tens and 6 ones. Take 1 ten and make it 10 ones: 2 tens and 16 ones. 20 + 16 = 36.", rnd),
        mcq("Which is NOT the same as 45?", "3 tens and 5 ones",
            ["4 tens and 5 ones", "3 tens and 15 ones", "40 + 5"],
            "3 tens and 5 ones is 30 + 5 = 35, not 45. The others all make 45: 40 + 5 and 30 + 15.", rnd),
    ]
    order = (make[:1] + miss[:2] + part[:1] + make[1:2] + miss[2:3] + part[1:2] + make[2:3] + miss[3:4]
             + part[2:] + make[3:] + odd[:1] + miss[4:] + fill[:1] + odd[1:2] + same[:1] + fill[1:]
             + odd[2:] + same[1:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Partition numbers into tens and ones", "items": order}


# ============================================================ set 3: numbers in words
def set_words(rnd):
    w2n = []
    for n, wrong, extra in [
            (14, [40, 41, 104], " Do not mix it up with forty, which is 40."),
            (40, [14, 4, 400], " Numbers ending in “ty” are tens. Fourteen is 14."),
            (63, [36, 603, 53], ""),
            (18, [80, 81, 108], " Do not mix it up with eighty, which is 80."),
            (91, [19, 901, 81], ""),
            (70, [17, 7, 700], " Numbers ending in “ty” are tens. Seventeen is 17."),
            (35, [53, 305, 25], ""),
            (59, [95, 509, 49], "")]:
        t, o = divmod(n, 10)
        e = "%s is %s, so write %d." % (words(n)[0].upper() + words(n)[1:], TO(t, o), n) + extra
        if n >= 20 and o:
            e += " Do not write %d0%d: a 2-digit number has only 2 digits." % (t, o)
        w2n.append(mcq_n("Write <b>%s</b> in numerals." % words(n), n, wrong, e, rnd))
    n2w = []
    for n, wrong, extra in [
            (64, ["forty-six", "sixty", "six-four"], ""),
            (14, ["forty", "fourty", "forteen"], " Spell it four + teen. Forty is 40."),
            (40, ["fourty", "fourteen", "four"], " Forty has no “u”, but four and fourteen do."),
            (17, ["seventy", "seventy-one", "seven"], ""),
            (82, ["twenty-eight", "eighty", "eight-two"], ""),
            (90, ["nineteen", "ninty", "nine"], " Ninety keeps the “e” from nine."),
            (55, ["fifteen", "fifty", "five-five"], ""),
            (73, ["thirty-seven", "seventy", "seven-three"], "")]:
        t, o = divmod(n, 10)
        if n < 20:
            e = "%d is 1 ten and %s. Numbers from 13 to 19 end in “teen”: %s." % (n, O(o), words(n))
        elif o:
            e = "%d is %s. Say the tens, then the ones, with a hyphen: %s." % (n, TO(t, o), words(n))
        else:
            e = "%d is %s. Tens end in “ty”: %s." % (n, T(t), words(n))
        n2w.append(mcq("How do you write %d in words?" % n, words(n), wrong, e + extra, rnd))
    other = [
        mcq_n("How many tens are in seventy-two?", 7, [2, 70, 72],
              "Seventy-two is 72: 7 tens and 2 ones. There are 7 tens.", rnd),
        mcq_n("How many ones are in forty-eight?", 8, [4, 80, 48],
              "Forty-eight is 48: 4 tens and 8 ones. There are 8 ones.", rnd),
        mcq(fig(blocks_svg(2, 7)) + "Which shows the number in words?", "twenty-seven",
            ["seventy-two", "twenty", "twenty-six"],
            "2 rods and 7 cubes: 2 tens and 7 ones = 27. In words: twenty-seven.", rnd),
        mcq(fig(blocks_svg(5, 0)) + "Which shows the number in words?", "fifty",
            ["fifteen", "five", "fifty-one"],
            "5 rods and no cubes: 5 tens = 50. In words: fifty. Fifteen is 15.", rnd),
    ]
    order = (w2n[:2] + n2w[:2] + other[:1] + w2n[2:3] + n2w[2:3] + other[2:3] + w2n[3:4] + n2w[3:4]
             + w2n[4:5] + n2w[4:5] + other[1:2] + w2n[5:6] + n2w[5:6] + other[3:] + w2n[6:7] + n2w[6:7]
             + w2n[7:] + n2w[7:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Numbers to 100 in numerals and words", "items": order}


# ============================================================ set 4: compare, order and estimate
def cmp_e(a, b):
    big, small = max(a, b), min(a, b)
    if big // 10 != small // 10:
        return ("Look at the tens first. %d has %s and %d has %s. So %d &gt; %d."
                % (big, T(big // 10), small, T(small // 10), big, small))
    return ("The tens are the same, so look at the ones. %s &gt; %s. So %d &gt; %d."
            % (O(big % 10), O(small % 10), big, small))


def set_compare(rnd):
    tru = []
    for x, y, extra in [(47, 74, ""), (52, 49, " Do not look at the ones first: 9 ones is less than 1 ten."),
                        (38, 83, ""), (61, 16, "")]:
        sym = "&lt;" if x < y else "&gt;"
        anti = "&gt;" if x < y else "&lt;"
        wrong = ["%d %s %d" % (x, anti, y), "%d = %d" % (x, y), "%d %s %d" % (y, sym, x)]
        tru.append(mcq("Which is true?", "%d %s %d" % (x, sym, y), wrong,
                       cmp_e(x, y) + extra + " The open side of the sign faces the bigger number.", rnd))
    tru.append(mcq("Which is true?", "30 + 6 = 36", ["30 + 6 &gt; 36", "30 + 6 &lt; 36", "30 + 6 = 63"],
                   "30 + 6 is 3 tens and 6 ones, which is 36. Both sides are the same, so use =.", rnd))
    tru.append(mcq("Which is true?", "fourteen &lt; forty",
                   ["fourteen &gt; forty", "fourteen = forty", "forty &lt; fourteen"],
                   "Fourteen is 14 (1 ten). Forty is 40 (4 tens). 14 &lt; 40.", rnd))
    gs = []
    for want, nums, extra in [
            ("greatest", [29, 71, 68, 45], " 29 has the biggest ones digit, but only 2 tens."),
            ("smallest", [53, 35, 50, 39], ""),
            ("greatest", [89, 98, 90, 80], ""),
            ("smallest", [19, 91, 21, 12], " 19 and 12 both have 1 ten. 2 ones &lt; 9 ones.")]:
        o = sorted(nums)
        ans = o[-1] if want == "greatest" else o[0]
        e = "Compare the tens first, then the ones. In order: %s. The %s is %d.%s" % (
            ", ".join(str(v) for v in o), want, ans, extra)
        gs.append(mcq("Which number is the %s?" % want, ans, [v for v in nums if v != ans], e, rnd))
    od = []
    fmt = lambda l: ", ".join(str(v) for v in l)
    for three, up in [([56, 65, 46], True), ([73, 37, 70], False), ([18, 81, 80], True)]:
        o = sorted(three) if up else sorted(three, reverse=True)
        perms = [[o[0], o[2], o[1]], [o[1], o[0], o[2]], o[::-1]]
        e = "Compare the tens first. If the tens are the same, compare the ones. From %s: %s." % (
            "smallest to greatest" if up else "greatest to smallest", fmt(o))
        od.append(mcq("Put %s in order from %s." % (fmt(three), "smallest to greatest" if up else "greatest to smallest"),
                      fmt(o), [fmt(p) for p in perms], e, rnd))
    btw = []
    for lo, hi, ans, wrong in [(30, 40, 34, [43, 29, 41]), (60, 70, 67, [76, 57, 71])]:
        assert lo < ans < hi and all(not lo < w < hi for w in wrong)
        btw.append(mcq_n("Which number is between %d and %d?" % (lo, hi), ans, wrong,
                         "Numbers between %d and %d have %s: %d, %d, … %d. %d has %s, so it fits."
                         % (lo, hi, T(lo // 10), lo + 1, lo + 2, hi - 1, ans, T(ans // 10)), rnd))
    nl = []
    for v, wrong in [(30, [3, 70, 40]), (80, [8, 20, 70])]:
        k = v // 10
        nl.append(mcq_n(fig(number_line_svg(0, 100, 10, [0, 50, 100], v)) + "What number does the arrow point to?",
                        v, wrong, "From 0 to 100 there are 10 jumps, so each mark is 10. Count in tens from 0: %s."
                        % ", ".join(str(10 * i) for i in range(1, k + 1)), rnd))
    est = [
        mcq_n(fig(number_line_svg(0, 100, 10, [0, 50, 100], 45)) + "Estimate the number the arrow points to.",
              45, [54, 35, 55], "Each mark is 10. The arrow is halfway between 40 and 50. Halfway is 45.", rnd),
        mcq_n(fig(number_line_svg(0, 100, 10, [0, 50, 100], 25)) + "Estimate the number the arrow points to.",
              25, [52, 75, 35],
              "The arrow is halfway between 0 and 50, so it is about 25. 75 is halfway between 50 and 100.", rnd),
        mcq_n(fig(number_line_svg(40, 50, 1, [40, 45, 50], 47)) + "What number does the arrow point to?",
              47, [74, 43, 57], "Each mark is 1. Count on from 45: 46, 47. The arrow shows 47.", rnd),
    ]
    order = (tru[:2] + nl[:1] + gs[:1] + tru[2:3] + btw[:1] + nl[1:2] + gs[1:2] + od[:1] + tru[3:4] + est[:1]
             + gs[2:3] + tru[4:5] + od[1:2] + btw[1:] + est[1:2] + gs[3:] + tru[5:] + est[2:] + od[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare, order and estimate with <, > and =",
            "items": order}


# ============================================================ set 5: word problems
def set_problems(rnd):
    its = [
        mcq_n("Pencils come in packs of 10. Amelia has 3 packs and 4 more pencils. How many pencils does she have?",
              34, [43, 304, 7], "3 packs = 3 tens = 30. 30 + 4 = 34.", rnd),
        mcq_n("Noah keeps marbles in bags of 10. He has 6 bags and 2 more marbles. How many marbles does he have?",
              62, [26, 602, 8], "6 bags = 6 tens = 60. 60 + 2 = 62.", rnd),
        mcq_n("Isla has 47 stickers. She puts them on sheets of 10. How many full sheets can she make?",
              4, [7, 40, 47], "47 is 4 tens and 7 ones. She can fill 4 sheets of 10.", rnd),
        mcq_n("George has 53 stickers. He fills as many sheets of 10 as he can. How many stickers are left over?",
              3, [5, 30, 50], "53 is 5 tens and 3 ones. 5 sheets use 50. 3 stickers are left over.", rnd),
        mcq_n("Biscuits come in packs of 10. The class needs 50 biscuits. How many packs do they need?",
              5, [50, 10, 15], "50 is 5 tens. Each pack is 1 ten. They need 5 packs.", rnd),
        mcq_n("Freya writes seventy-one on her card. Which number does she write?",
              71, [17, 701, 61], "Seventy-one is 7 tens and 1 one: 71. Seventeen is 17.", rnd),
        mcq_n("Harry gets on the number 46 bus. What is the 4 worth?",
              40, [4, 6, 46], "The 4 is in the tens place. It is worth 4 tens = 40.", rnd),
        mcq("Four children play a game. Jack scores 39, Poppy scores 52, Leo scores 48 and Grace scores 25. "
            "Who scores the most?", "Poppy", ["Jack", "Leo", "Grace"],
            "Look at the tens. 52 has 5 tens. The others have fewer tens. Poppy scores the most. "
            "Jack has 9 ones, but only 3 tens.", rnd),
        mcq("Class 1 has 31 children. Class 2 has 28 children. Which is true?", "28 &lt; 31",
            ["28 &gt; 31", "28 = 31", "31 &lt; 28"],
            "Look at the tens. 31 has 3 tens. 28 has 2 tens. So 28 &lt; 31. Class 1 has more children.", rnd),
        mcq_n("Oliver has 2 tens and 13 ones in cubes. How many cubes is that?",
              33, [213, 23, 15], "2 tens = 20. 13 ones = 1 ten and 3 ones. 20 + 13 = 33.", rnd),
        mcq_n("Ruby needs 60 beads. Beads come on strings of 10. How many strings does she need?",
              6, [60, 16, 10], "60 is 6 tens. Each string is 1 ten. She needs 6 strings.", rnd),
        mcq_n("A teacher has 100 pencils. She puts them in pots of 10. How many pots does she fill?",
              10, [1, 100, 9], "Count in tens to 100: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100. That is 10 pots. "
                               "10 tens = 100.", rnd),
        mcq_n(fig(number_line_svg(0, 100, 10, [0, 50, 100], 70)) +
              "Kai runs a 100 m race. The arrow shows where he is. How far has he run?",
              70, [7, 30, 60], "Each mark is 10 m. Count in tens: 10, 20, 30, 40, 50, 60, 70. He has run 70 m.",
              rnd, unit=" m"),
        mcq_n("Zara thinks of a number. It has 8 tens and 5 ones. What is her number?",
              85, [58, 805, 13], "8 tens = 80. 80 + 5 = 85.", rnd),
        mcq_n("Arjun thinks of a number between 40 and 50. It has 6 ones. What is his number?",
              46, [64, 406, 56], "Between 40 and 50 means 4 tens. 4 tens and 6 ones = 46.", rnd),
        mcq_n("Use the digits 3 and 8 once each. What is the biggest 2-digit number you can make?",
              83, [38, 88, 11], "Put the bigger digit in the tens place: 8 tens and 3 ones = 83. "
                                "You cannot use 8 twice.", rnd),
        mcq_n("Use the digits 5 and 2 once each. What is the smallest 2-digit number you can make?",
              25, [52, 22, 7], "Put the smaller digit in the tens place: 2 tens and 5 ones = 25.", rnd),
        mcq_n("A shop has 7 bags of 10 apples and 9 loose apples. How many apples is that?",
              79, [97, 709, 16], "7 bags = 7 tens = 70. 70 + 9 = 79.", rnd),
        mcq_n("Evie counts her toy cars. She has 3 tens and 0 ones. How many toy cars does she have?",
              30, [3, 300, 13], "3 tens = 30. There are 0 ones, so the number is 30.", rnd),
        mcq("Maya writes 47 = 4 + 7. That is wrong. Which is right?", "47 = 40 + 7",
            ["47 = 4 + 7", "47 = 70 + 4", "47 = 40 + 70"],
            "The 4 in 47 is 4 tens, so it is worth 40. 47 = 40 + 7. (4 + 7 is only 11.)", rnd),
    ]
    assert len(its) == 20
    tail = its[1:]
    rnd.shuffle(tail)
    return {"title": "Place value word problems", "items": its[:1] + tail}


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
        "<h2>Tens and ones</h2>"
        "<p>A 2-digit number has a <b>tens</b> digit and a <b>ones</b> digit. "
        "The place tells you what the digit is worth. <b>10 ones make 1 ten.</b></p>"
        "<figure class='sn-fig'>" + blocks_svg(4, 7, labels=True) +
        "<figcaption>A rod is 1 ten. A small cube is 1 one. 4 tens and 7 ones make 47.</figcaption></figure>"
        "<figure class='sn-fig'>" + chart_svg(47, 1) +
        "<figcaption>In 47 the 4 is in the tens place. It is worth 4 tens, or 40.</figcaption></figure>"
        "<h2>Partition</h2>"
        "<p>Split a number into tens and ones: <b>47 = 40 + 7</b>. "
        "You can also swap 1 ten for 10 ones: 47 is 3 tens and 17 ones, because 30 + 17 = 47.</p>" +
        ex("Partition", "Split 63 into tens and ones.", "63 is 6 tens and 3 ones. 6 tens = 60.", "63 = 60 + 3") +
        "<h2>Numbers in words</h2>" +
        table(["Numeral", "Words", "Tens and ones"], [
            ["14", "fourteen", "1 ten and 4 ones"],
            ["40", "forty", "4 tens and 0 ones"],
            ["64", "sixty-four", "6 tens and 4 ones"],
            ["90", "ninety", "9 tens and 0 ones"],
            ["100", "one hundred", "10 tens"],
        ]) +
        "<p>“Teen” numbers have 1 ten. “Ty” numbers have lots of tens. Use a hyphen in sixty-four.</p>"
        "<h2>Compare with &lt; &gt; =</h2>"
        "<p>Look at the tens first. If the tens are the same, look at the ones.</p>" +
        ex("Compare", "52 ☐ 49", "Tens: 5 tens &gt; 4 tens. Stop here. The 9 ones do not matter.", "52 &gt; 49") +
        "<p>&lt; means “is less than”. &gt; means “is greater than”. = means “is the same as”. "
        "The open side faces the bigger number.</p>"
        "<h2>Estimate on a number line</h2>"
        "<figure class='sn-fig'>" + number_line_svg(0, 100, 10, [0, 50, 100], 45, show="about 45") +
        "<figcaption>Each mark is 10. The arrow is halfway between 40 and 50, so it shows about 45.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing forty-seven as 74 or 407", "Tens first, then ones: 47"],
            ["Saying the 4 in 47 is worth 4", "It is in the tens place: 40"],
            ["Comparing the ones first (49 &gt; 52)", "Compare the tens first: 52 &gt; 49"],
            ["Mixing up fourteen and forty", "Fourteen is 14, forty is 40"],
            ["Spelling fourty or ninty", "forty, ninety"],
        ])
    )


FAQ = [
    {"q": "What place value should a Year 2 child know?",
     "a": "Year 2 children work with numbers up to 100. They know the tens and ones in a 2-digit number, read and write numbers in numerals and words, compare and order numbers with <, > and =, and find numbers on a number line."},
    {"q": "What does partitioning mean in Year 2 maths?",
     "a": "Partitioning means splitting a number into parts, usually tens and ones: 47 = 40 + 7. Children also learn other ways, such as 47 = 30 + 17."},
    {"q": "Why does my child write 407 for forty-seven?",
     "a": "They write each part they hear: 40 and then 7. Show 4 tens and 7 ones with blocks or straws, then write the tens digit and the ones digit: 47."},
    {"q": "How do you teach < and > signs in Year 2?",
     "a": "Compare the tens first, then the ones, and say “is less than” or “is greater than”. The open side of the sign always faces the bigger number, as in 52 > 49."},
]


def mark_large(u, pattern):
    """Tag wide pictures (blocks, straws, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(2201)
    sets = [set_tens_ones(rnd), set_partition(rnd), set_words(rnd), set_compare(rnd), set_problems(rnd)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "place-value-to-100", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value to 100: Tens and Ones, Partitioning and Comparing",
        "seo_title": "Year 2 Place Value Worksheets: Tens and Ones, Numbers to 100 in Words",
        "short_title": "Place value to 100",
        "domain": "Number and place value",
        "standard_code": "Year 2: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise the place value of each digit in a two-digit number (tens, ones); identify, represent and estimate numbers using different representations, including the number line; compare and order numbers from 0 up to 100; use <, > and = signs; read and write numbers to at least 100 in numerals and in words; use place value and number facts to solve problems.",
        "meta_desc": "Free Year 2 place value maths worksheets for the National Curriculum: tens and ones with blocks and straws, partitioning (47 = 40 + 7), numbers to 100 in words, comparing with <, > and =, and number lines. 100 questions with an answer key.",
        "key_big": "A 2-digit number is tens and ones. The 4 in 47 is worth 40.",
        "key_sub": "47 = 40 + 7, and it is also 3 tens and 17 ones. To compare numbers, look at the tens first, then the ones.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(base-ten blocks|bundles of straws|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
