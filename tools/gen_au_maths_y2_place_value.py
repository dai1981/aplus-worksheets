# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Place value to 1000 (Australian Curriculum v9.0, AC9M2N02, also AC9M2N01)
  python3 tools/gen_au_maths_y2_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Year 2: numbers to 1000 (no 4-digit answers), very short sentences for 7-8 year olds, MAB pictures.
Wrong answers come from real mistakes: writing each spoken part (three hundred and five -> 3005),
leaving out a zero (305 -> 35), giving the digit instead of its value (the 4 in 345 is 4),
reading the blocks in the wrong order (234 -> 432), counting pieces instead of values (2 + 3 + 4 = 9),
writing 14 tens as "14" inside the number (2 hundreds, 14 tens, 6 ones -> 2146),
fifteen / fifty, and comparing 2- and 3-digit numbers by the first digit only.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

PL = ["ones", "tens", "hundreds"]
PL1 = ["one", "ten", "hundred"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e, rnd):
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    ch = wrong + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, wrong, e, rnd):
    assert 0 <= correct <= 1000, (q, correct)
    assert all(isinstance(w, int) and w >= 0 and w != correct for w in wrong), (q, correct, wrong)
    return mcq(q, correct, wrong, e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
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


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def unit(k, w):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


def hto(h, t, o):
    return "%s, %s and %s" % (plural(h, 2), plural(t, 1), plural(o, 0))


def hto_n(n):
    return hto(digit(n, 2), digit(n, 1), digit(n, 0))


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


def words(n):
    h, r = divmod(n, 100)
    if not h:
        return words99(r)
    return ONES[h] + " hundred" + (" and " + words99(r) if r else "")


assert words(305) == "three hundred and five" and words(640) == "six hundred and forty" and words(900) == "nine hundred"


# ------------------------------------------------------------ figures
U = 8                      # MAB: a mini = U, a long = U x 10U, a flat = 10U x 10U (exact 1 : 10 : 100)
G = 8                      # gap between flats
GG = 22                    # gap between groups
MG = 8


def mab_svg(h, t, o, labels=False):
    """MAB: h flats, t longs, o minis. Flats in one row (up to 3) or two rows; minis in columns of 5."""
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
        s += draw(x + (w - gw) // 2, MG + body_h - gh)        # every group sits on the same base line
        if labels:
            s.append(text(x + w / 2, MG + body_h + 20, lab, 15))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "MAB blocks")


CW, HEAD, ROW = 104, 34, 50


def chart_svg(n, hi=None):
    """Hundreds / tens / ones chart. hi = place index to colour red."""
    x0 = y0 = 6
    W, Hh = 2 * x0 + 3 * CW, 2 * y0 + HEAD + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 3 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 3 * CW, HEAD, FILL)]
    for k in range(3):
        i = 2 - k
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append(text(cx, y0 + 23, cap(PL[i]), 15))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 3 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "place value chart showing %d" % n)


def number_line_svg(lo, hi, step, labels, arrow, show=None, unit=""):
    """Number line lo..hi with a tick every step, numbers under `labels` and a red arrow at `arrow`."""
    L, R, Y = 36, 436, 58
    W, Hh = 472, 100

    def X(v):
        return L + (v - lo) * (R - L) / (hi - lo)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, "%d%s" % (v, unit), 15, col=GREEN))
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


def mab_e(h, t, o):
    n = 100 * h + 10 * t + o
    s = "A flat is 100, a long is 10 and a mini is 1. %s make %d." % (cap(hto(h, t, o)), n)
    empty = [PL[i] for i, d in ((1, t), (0, o)) if d == 0]
    if empty:
        s += " There are no %s, so write 0 in the %s place%s." % (" or ".join(empty), " and ".join(empty),
                                                                  "s" if len(empty) > 1 else "")
    return s


# ============================================================ set 1: hundreds, tens and ones with MAB
def set_mab(rnd):
    what = []
    for h, t, o in [(2, 3, 4), (1, 5, 2), (3, 2, 6), (2, 8, 5), (4, 1, 7), (1, 7, 9), (3, 4, 1), (5, 6, 3)]:
        n = 100 * h + 10 * t + o
        wrong = [100 * o + 10 * t + h, 100 * h + 10 * o + t, h + t + o]       # read backwards, tens/ones swapped, counted pieces
        e = mab_e(h, t, o) + " Start with the flats, then the longs, then the minis."
        what.append(mcq_n(fig(mab_svg(h, t, o)) + "What number do the MAB show?", n, wrong, e, rnd))
    how = [
        mcq_n(fig(mab_svg(3, 5, 2)) + "How many tens are there?", 5, [3, 2, 50],
              "Each long is 1 ten. There are 5 longs, so there are 5 tens. The number is 352.", rnd),
        mcq_n(fig(mab_svg(4, 2, 6)) + "How many hundreds are there?", 4, [2, 6, 400],
              "Each flat is 1 hundred. There are 4 flats, so there are 4 hundreds. The number is 426.", rnd),
        mcq_n(fig(mab_svg(2, 7, 8)) + "How many ones are there?", 8, [2, 7, 17],
              "Each mini is 1 one. There are 8 minis, so there are 8 ones. The number is 278.", rnd),
    ]
    match = []
    for h, t, o in [(3, 6, 4), (2, 5, 7), (5, 1, 8)]:
        wrong = [hto(o, t, h), hto(h, o, t), hto(t, h, o)]
        match.append(mcq(fig(mab_svg(h, t, o)) + "Which matches the MAB?", hto(h, t, o), wrong,
                         "Count each kind: %s, %s, %s. That is %s: %d."
                         % (unit(h, "flat"), unit(t, "long"), unit(o, "mini"), hto(h, t, o), 100 * h + 10 * t + o), rnd))
    more = [
        mcq_n(fig(mab_svg(2, 4, 5)) + "Add 1 more long. What number is it now?", 255, [246, 345, 235],
              "The MAB show 245. A long is 10. 245 + 10 = 255. Only the tens digit changes.", rnd),
        mcq_n(fig(mab_svg(1, 3, 6)) + "Add 1 more flat. What number is it now?", 236, [137, 146, 36],
              "The MAB show 136. A flat is 100. 136 + 100 = 236. Only the hundreds digit changes.", rnd),
        mcq_n(fig(mab_svg(3, 5, 9)) + "Add 1 more mini. What number is it now?", 360, [3510, 369, 459],
              "The MAB show 359. Add 1 mini: now there are 10 minis. Trade 10 minis for 1 long. "
              "That is 3 hundreds, 6 tens and 0 ones: 360.", rnd),
    ]
    which = []
    for h, t, o in [(4, 2, 9), (7, 3, 1), (6, 8, 2)]:
        n = 100 * h + 10 * t + o
        which.append(mcq_n("Which number has %s?" % hto(h, t, o), n,
                           [100 * o + 10 * t + h, 100 * h + 10 * o + t, h + t + o],
                           "Write the hundreds digit first, then the tens, then the ones: %d, %d, %d. That is %d."
                           % (h, t, o, n), rnd))
    order = (what[:3] + how[:2] + what[3:5] + match[:2] + how[2:] + what[5:7] + match[2:] + which[:2]
             + what[7:] + more + which[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Hundreds, tens and ones with MAB", "items": order}


# ============================================================ set 2: value of a digit
def value_wrong(n, i):
    d = digit(n, i)
    if i == 2:
        return [d, d * 10, d * 1000]
    if i == 1:
        return [d, d * 100, n % 100]                     # the digit, the wrong place, "read from the 4 on" (45)
    return [d * 10, d * 100, n % 100]


def value_e(n, i, red=False):
    d = digit(n, i)
    v = d * 10 ** i
    s = "The %s%d is in the %s place. It is worth %s = %d." % ("red " if red else "", d, PL[i], plural(d, i), v)
    if i:
        s += " The digit is %d, but its value is %d." % (d, v)
    return s


def set_value(rnd):
    chart = [mcq_n(fig(chart_svg(n, hi=i)) + "What is the red digit worth?", digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i, True), rnd)
             for n, i in [(345, 1), (582, 2), (716, 0), (493, 1), (268, 2), (857, 1)]]
    plain = [mcq_n("What is the %d in %d worth?" % (digit(n, i), n), digit(n, i) * 10 ** i,
                   value_wrong(n, i), value_e(n, i), rnd)
             for n, i in [(473, 1), (619, 2), (538, 0), (924, 1), (751, 2)]]
    place = []
    for n, i in [(736, 2), (418, 1), (695, 1)]:
        d = digit(n, i)
        wrong = [digit(n, x) for x in range(2, -1, -1) if x != i] + [d * 10 ** i]
        place.append(mcq("In %d, which digit is in the %s place?" % (n, PL[i]), d, wrong,
                         "%d is %s. The %s digit is %d. (Its value is %d.)" % (n, hto_n(n), PL[i], d, d * 10 ** i), rnd))
    has = []
    for d, i, ans, wrong in [(6, 1, 263, [623, 236, 632]), (8, 2, 815, [158, 581, 185]), (3, 0, 473, [437, 347, 734])]:
        assert digit(ans, i) == d and all(digit(w, i) != d for w in wrong)
        has.append(mcq_n("Which number has %s %d in the %s place?" % ("an" if d == 8 else "a", d, PL[i]), ans, wrong,
                         "%d is %s. The %d is in the %s place." % (ans, hto_n(ans), d, PL[i]), rnd))
    groups = [
        mcq_n(fig(mab_svg(0, 6, 0)) + "What are 6 tens worth?", 60, [6, 600, 16],
              "Count the longs in tens: 10, 20, 30, 40, 50, 60. 6 tens = 60.", rnd),
        mcq_n(fig(mab_svg(8, 0, 0)) + "What are 8 hundreds worth?", 800, [8, 80, 108],
              "Count the flats in hundreds: 100, 200, 300 … 800. 8 hundreds = 800.", rnd),
        mcq_n(fig(mab_svg(0, 5, 0)) + "What are 5 tens worth?", 50, [5, 500, 15],
              "Count the longs in tens: 10, 20, 30, 40, 50. 5 tens = 50.", rnd),
    ]
    order = (groups[:1] + chart[:2] + plain[:1] + place[:1] + groups[1:2] + chart[2:4] + has[:1] + plain[1:3]
             + place[1:2] + groups[2:] + chart[4:] + has[1:2] + plain[3:] + place[2:] + has[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "The value of each digit", "items": order}


# ============================================================ set 3: zero as a place holder
def zero_e(n):
    empty = [PL[i] for i in (1, 0) if digit(n, i) == 0]
    return ("%s is %s: %d. Write 0 for the empty %s place. The 0 keeps the other digits in the right places."
            % (cap(words(n)), hto_n(n), n, " and ".join(empty)))


def set_zero(rnd, P):
    mab = []
    for h, t, o, wrong in [(3, 0, 5, [35, 3005, 350]), (4, 6, 0, [46, 406, 4600]),
                           (2, 0, 8, [28, 2008, 280]), (7, 0, 0, [7, 70, 7000])]:
        mab.append(mcq_n(fig(mab_svg(h, t, o)) + "What number do the MAB show?", 100 * h + 10 * t + o, wrong,
                         mab_e(h, t, o), rnd))
    wr = []
    for n, wrong in [(406, [46, 4006, 460]), (203, [23, 2003, 230]), (570, [57, 507, 5070]),
                     (809, [89, 8009, 890]), (640, [64, 604, 6040])]:
        wr.append(mcq_n("Write “%s” in numerals." % words(n), n, wrong, zero_e(n), rnd))
    rd = [
        mcq("How do you write 708 in words?", words(708), ["seventy-eight", words(780), words(807)],
            "708 is 7 hundreds, 0 tens and 8 ones. Say the hundreds, then the ones: seven hundred and eight.", rnd),
        mcq("How do you write 350 in words?", words(350), ["thirty-five", words(305), words(315)],
            "350 is 3 hundreds, 5 tens and 0 ones. 5 tens is fifty, not fifteen: three hundred and fifty.", rnd),
    ]
    cnt = [
        mcq_n(fig(chart_svg(507)) + "How many tens are in 507?", 0, [5, 7, 50],
              "507 is 5 hundreds, 0 tens and 7 ones. The 0 shows there are no tens.", rnd),
        mcq_n(fig(chart_svg(380)) + "How many ones are in 380?", 0, [8, 3, 80],
              "380 is 3 hundreds, 8 tens and 0 ones. The 0 shows there are no ones.", rnd),
    ]
    has0 = [
        mcq_n("Which number has 0 tens?", 306, [360, 630, 36],
              "306 is 3 hundreds, 0 tens and 6 ones. 360 and 630 have 0 ones, and 36 has 3 tens.", rnd),
        mcq_n("Which number has 0 ones?", 470, [407, 704, 47],
              "470 is 4 hundreds, 7 tens and 0 ones. 407 and 704 have 0 tens, and 47 has 7 ones.", rnd),
    ]
    exp = []
    for a, b, wrong in [(600, 7, [67, 6007, 670]), (400, 90, [49, 409, 4090]), (800, 3, [83, 8003, 830])]:
        n = a + b
        exp.append(mcq_n("What is %d + %d?" % (a, b), n, wrong,
                         "%d + %d is %s: %d. Do not write %d then %d. The answer has only 3 digits."
                         % (a, b, hto_n(n), n, a, b), rnd))
    name, she, her = P.next()
    fix = [
        mcq_n("%s writes 3005 for “three hundred and five”. What should %s write?" % (name, she), 305,
              [35, 350, 3050],
              "Three hundred and five is 3 hundreds, 0 tens and 5 ones: 305. "
              "3005 has 4 digits. It is far too big.", rnd),
        mcq("Which is true?", "305 &gt; 35", ["305 = 35", "305 &lt; 35", "35 &gt; 305"],
            "305 has 3 digits and 35 has only 2. 305 is 3 hundreds and 5 ones. 35 is 3 tens and 5 ones. "
            "So 305 &gt; 35. The 0 matters.", rnd),
    ]
    order = (mab[:2] + wr[:2] + cnt[:1] + mab[2:3] + exp[:1] + has0[:1] + wr[2:3] + cnt[1:] + mab[3:] + rd[:1]
             + exp[1:2] + has0[1:] + wr[3:4] + fix[:1] + rd[1:] + exp[2:] + wr[4:] + fix[1:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Zero as a place holder", "items": order}


# ============================================================ set 4: partition
def set_partition(rnd):
    std = [
        mcq("Which shows 346 split into hundreds, tens and ones?", "300 + 40 + 6",
            ["3 + 4 + 6", "300 + 4 + 6", "300 + 40 + 60"],
            "346 is 3 hundreds, 4 tens and 6 ones. That is 300 + 40 + 6.", rnd),
        mcq("Which shows 572 split into hundreds, tens and ones?", "500 + 70 + 2",
            ["5 + 7 + 2", "500 + 7 + 2", "50 + 70 + 2"],
            "572 is 5 hundreds, 7 tens and 2 ones. That is 500 + 70 + 2.", rnd),
        mcq("Which shows 508 split into parts?", "500 + 8", ["50 + 8", "500 + 80", "5 + 8"],
            "508 is 5 hundreds, 0 tens and 8 ones. 0 tens adds nothing. So 508 = 500 + 8.", rnd),
        mcq("Which shows 690 split into parts?", "600 + 90", ["600 + 9", "60 + 90", "6 + 9"],
            "690 is 6 hundreds, 9 tens and 0 ones. 9 tens = 90. So 690 = 600 + 90.", rnd),
    ]
    miss = [
        mcq_n("300 + ☐ + 6 = 346. What number goes in the box?", 40, [4, 400, 46],
              "346 is 3 hundreds, 4 tens and 6 ones. 4 tens = 40.", rnd),
        mcq_n("☐ + 20 + 9 = 829. What number goes in the box?", 800, [8, 80, 829],
              "829 is 8 hundreds, 2 tens and 9 ones. 8 hundreds = 800.", rnd),
        mcq_n("400 + ☐ = 407. What number goes in the box?", 7, [70, 47, 0],
              "407 is 4 hundreds, 0 tens and 7 ones. 400 + 7 = 407.", rnd),
        mcq_n("600 + 30 + ☐ = 635. What number goes in the box?", 5, [50, 35, 500],
              "635 is 6 hundreds, 3 tens and 5 ones. The ones part is 5.", rnd),
    ]
    mab = [
        mcq_n(fig(mab_svg(2, 14, 6)) + "What number do the MAB show?", 346, [2146, 246, 336],
              "There are 14 longs. 10 longs make 1 hundred, so 14 tens = 1 hundred and 4 tens. "
              "200 + 140 + 6 = 346.", rnd),
        mcq_n(fig(mab_svg(1, 12, 5)) + "What number do the MAB show?", 225, [1125, 125, 215],
              "12 longs are 12 tens = 120. 100 + 120 + 5 = 225. "
              "That is the same as 2 hundreds, 2 tens and 5 ones.", rnd),
        mcq_n(fig(mab_svg(3, 0, 15)) + "What number do the MAB show?", 315, [3015, 305, 350],
              "15 minis are 1 ten and 5 ones. 300 + 15 = 315.", rnd),
    ]
    regroup = [
        mcq_n("346 = 2 hundreds, ☐ tens and 6 ones. What number goes in the box?", 14, [4, 34, 140],
              "Take 1 hundred from 3 hundreds and make it 10 tens. Now there are 2 hundreds and 10 + 4 = 14 tens. "
              "Check: 200 + 140 + 6 = 346.", rnd),
        mcq_n("523 = 4 hundreds, 12 tens and ☐ ones. What number goes in the box?", 3, [13, 23, 30],
              "4 hundreds = 400 and 12 tens = 120. 400 + 120 = 520. 523 − 520 = 3. So there are 3 ones.", rnd),
        mcq("Which is another way to make 346?", "2 hundreds, 14 tens and 6 ones",
            ["2 hundreds, 4 tens and 6 ones", "3 hundreds, 14 tens and 6 ones", "2 hundreds, 14 tens and 16 ones"],
            "2 hundreds = 200 and 14 tens = 140. 200 + 140 + 6 = 346. "
            "(The others make 246, 446 and 356.)", rnd),
        mcq("Which is <b>not</b> equal to 250?", "2 hundreds and 5 ones",
            ["25 tens", "1 hundred and 15 tens", "2 hundreds and 5 tens"],
            "2 hundreds and 5 ones = 205, not 250. 25 tens = 250, 100 + 150 = 250 and 200 + 50 = 250.", rnd),
        mcq_n("How many tens are in 250 altogether?", 25, [5, 2, 250],
              "250 = 2 hundreds and 5 tens. 2 hundreds = 20 tens. 20 tens + 5 tens = 25 tens.", rnd),
        mcq_n("430 = ☐ tens. What number goes in the box?", 43, [3, 4, 430],
              "430 = 4 hundreds and 3 tens. 4 hundreds = 40 tens. 40 + 3 = 43 tens. Check: 43 × 10 = 430.", rnd),
        mcq_n("600 = ☐ tens. What number goes in the box?", 60, [6, 600, 10],
              "1 hundred = 10 tens. 6 hundreds = 60 tens. Check: 60 × 10 = 600.", rnd),
        mcq_n("357 = 200 + ☐ + 7. What number goes in the box?", 150, [50, 100, 15],
              "357 = 300 + 50 + 7. Only 200 is used, so 100 moves to the tens part: 100 + 50 = 150. "
              "Check: 200 + 150 + 7 = 357.", rnd),
        mcq_n("418 = 400 + ☐ ones. What number goes in the box?", 18, [8, 10, 1],
              "418 = 400 + 10 + 8. The 1 ten and 8 ones together make 18 ones. 400 + 18 = 418.", rnd),
    ]
    for v, w in [(200 + 140 + 6, 346), (400 + 120 + 3, 523), (300 + 140 + 6, 446), (200 + 140 + 16, 356),
                 (200 + 5, 205), (100 + 150, 250), (43 * 10, 430), (200 + 150 + 7, 357), (100 + 120 + 5, 225),
                 (300 + 15, 315)]:
        assert v == w
    order = std[:2] + miss[:2] + std[2:] + miss[2:] + mab[:1] + regroup[:1] + mab[1:2] + regroup[1:3] + mab[2:] + regroup[3:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Partition in standard and non-standard ways", "items": order}


# ============================================================ set 5: compare, order and word problems
def first_diff(a, b):
    for i in (2, 1, 0):
        if digit(a, i) != digit(b, i):
            return i


def compare_e(big, small):
    if len(str(big)) != len(str(small)):
        return ("%d has %d digits and %d has only %d. So %d &gt; %d."
                % (big, len(str(big)), small, len(str(small)), big, small))
    i = first_diff(big, small)
    lead = "Start with the hundreds" if i == 2 else "The %s are the same, so look at the %s" % (
        " and ".join(PL[x] for x in (2, 1) if x > i), PL[i])
    return ("Compare from the left. %s: %s is more than %s. So %d &gt; %d."
            % (lead, plural(digit(big, i), i), plural(digit(small, i), i), big, small))


def set_problems(rnd, P):
    cmp_ = []
    for x, y in [(452, 425), (309, 390), (98, 102)]:
        lt = "&lt;" if x < y else "&gt;"
        gt = "&gt;" if x < y else "&lt;"
        e = compare_e(max(x, y), min(x, y))
        if x == 98:
            e += " Do not just look at the first digit: count the digits first."
        cmp_.append(mcq("Which is true?", "%d %s %d" % (x, lt, y),
                        ["%d %s %d" % (x, gt, y), "%d = %d" % (x, y), "%d %s %d" % (y, lt, x)], e, rnd))
    big = [
        mcq_n("Which number is the greatest?", 543, [534, 354, 435],
              compare_e(543, 534) + " 543 is the greatest.", rnd),
        mcq_n("Which number is the smallest?", 86, [608, 680, 806],
              "86 is the only number with 2 digits, so it is the smallest, even though 8 is a big digit.", rnd),
    ]
    order = [mcq("Put 271, 217 and 712 in order from smallest to largest.", "217, 271, 712",
                 ["271, 217, 712", "712, 271, 217", "217, 712, 271"],
                 "Hundreds first: 712 has 7 hundreds, so it is the largest. 217 and 271 both have 2 hundreds. "
                 "Tens: 1 ten &lt; 7 tens, so 217 &lt; 271. Order: 217, 271, 712.", rnd)]
    lines = [
        mcq_n(fig(number_line_svg(0, 1000, 100, [0, 500, 1000], 600)) + "What number does the arrow point to?",
              600, [60, 500, 700],
              "From 0 to 1000 there are 10 jumps, so each mark is 100. The arrow is 1 mark after 500: 600.", rnd),
        mcq_n(fig(number_line_svg(300, 400, 10, [300, 350, 400], 360)) + "What number does the arrow point to?",
              360, [306, 370, 600],
              "From 300 to 400 there are 10 jumps, so each mark is 10, not 1. "
              "The arrow is 1 mark after 350: 350 + 10 = 360.", rnd),
    ]
    wp = []
    a, _, _ = P.next()
    b, _, _ = P.next()
    wp.append(mcq("%s’s class collected 245 bottle tops. %s’s class collected 254. Which class collected more?"
                  % (a, b), "%s’s class" % b, ["%s’s class" % a, "They are the same", "You cannot tell"],
                  "Both have 2 hundreds. Tens: 5 tens &gt; 4 tens. So 254 &gt; 245. %s’s class collected more." % b, rnd))
    wp.append(mcq_n("Pencils come in boxes of 10. The school buys 36 boxes. How many pencils is that?", 360,
                    [36, 46, 306],
                    "36 tens = 3 hundreds and 6 tens = 360. Count: 10 boxes is 100 pencils, so 30 boxes is 300. "
                    "6 more boxes is 60. 300 + 60 = 360.", rnd))
    name, she, her = P.next()
    wp.append(mcq_n("%s has 2 packs of 100 stickers, 5 sheets of 10 stickers and 3 single stickers. "
                    "How many stickers does %s have?" % (name, she), 253, [235, 10, 352],
                    "2 packs of 100 = 200. 5 sheets of 10 = 50. 3 singles = 3. 200 + 50 + 3 = 253.", rnd))
    name, he, his = P.next()
    while he != "he":
        name, he, his = P.next()
    wp.append(mcq_n("There are “five hundred and seven” students at %s’s school. %s writes 5007. "
                    "What is the right number?" % (name, cap(he)), 507, [57, 570, 750],
                    "Five hundred and seven is 5 hundreds, 0 tens and 7 ones: 507. "
                    "5007 has 4 digits, so it is far too big.", rnd))
    name, she, her = P.next()
    wp.append(mcq(fig(number_line_svg(0, 1000, 100, [0, 500, 1000], 700, unit=" m")) +
                    "A bushwalk is 1000 m long. The arrow shows where %s is. How far has %s walked?" % (name, she),
                    "700 m", ["70 m", "600 m", "800 m"],
                    "Each mark is 100 m. The arrow is 2 marks after 500 m: 500, 600, 700. %s has walked 700 m."
                    % name, rnd))
    wp.append(mcq("Three classes read books. 2A read 136, 2B read 163 and 2C read 116. "
                  "Which list goes from smallest to largest?", "116, 136, 163",
                  ["136, 116, 163", "163, 136, 116", "116, 163, 136"],
                  "All have 1 hundred. Compare the tens: 1 ten &lt; 3 tens &lt; 6 tens. Order: 116, 136, 163.", rnd))
    name, she, her = P.next()
    wp.append(mcq_n("%s’s number has 6 hundreds, 0 tens and 9 ones. What is %s number?" % (name, her), 609,
                    [69, 690, 6009],
                    "Write the digits in order: 6, 0, 9. That is 609. The 0 keeps the 6 in the hundreds place.", rnd))
    wp.append(mcq_n("Use the digits 4, 7 and 2 once each. What is the greatest number you can make?", 742,
                    [724, 247, 472],
                    "Put the biggest digit in the hundreds place, then the next biggest: 7, 4, 2. That is 742.", rnd))
    wp.append(mcq_n("Use the digits 5, 0 and 3 once each. What is the smallest 3-digit number you can make?", 305,
                    [35, 350, 503],
                    "A 3-digit number cannot start with 0. Put the smallest other digit first: 3. Then 0, then 5: 305. "
                    "(035 is just 35, which has only 2 digits.)", rnd))
    name, he, his = P.next()
    while he != "he":
        name, he, his = P.next()
    wp.append(mcq("%s has three $100 notes, four $10 notes and two $1 coins. How much money is that?" % name,
                  "$342", ["$9", "$324", "$432"],
                  "Three $100 notes = $300. Four $10 notes = $40. Two $1 coins = $2. $300 + $40 + $2 = $342.", rnd))
    wp.append(mcq_n("The cricket club has 170 members. Then 10 more people join. How many members are there now?", 180,
                    [171, 270, 160],
                    "10 more changes only the tens digit: 7 tens → 8 tens. 170 + 10 = 180.", rnd))
    wp.append(mcq_n("Icy poles come in boxes of 10. The school canteen has 10 boxes. How many icy poles is that?",
                    100, [10, 1000, 20],
                    "10 tens = 1 hundred. So 10 boxes of 10 is 100 icy poles.", rnd))
    for v, w in [(200 + 50 + 3, 253), (300 + 40 + 2, 342), (36 * 10, 360), (170 + 10, 180), (10 * 10, 100)]:
        assert v == w
    assert 254 > 245 and 116 < 136 < 163 and 217 < 271 < 712 and 98 < 102 and 309 < 390
    order = cmp_[:2] + lines[:1] + big + order + cmp_[2:] + lines[1:] + wp
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare, order and word problems", "items": order}


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
        "<h2>Hundreds, tens and ones</h2>"
        "<p>A 3-digit number has three places: <b>hundreds</b>, <b>tens</b> and <b>ones</b>. "
        "10 ones make 1 ten. 10 tens make 1 hundred. 10 hundreds make 1000.</p>"
        "<figure class='sn-fig'>" + mab_svg(3, 4, 6, labels=True) +
        "<figcaption>MAB for 346. A flat is 100, a long is 10 and a mini is 1.</figcaption></figure>"
        "<h2>The value of a digit</h2>"
        "<p>The place tells you what a digit is worth.</p>"
        "<figure class='sn-fig'>" + chart_svg(345, hi=1) +
        "<figcaption>In 345 the 4 is in the tens place. It is worth 4 tens, or 40.</figcaption></figure>"
        "<h2>Zero holds a place</h2>"
        "<p>If a place is empty, write <b>0</b> there. The 0 keeps the other digits in the right places.</p>" +
        ex("Write in numerals", "Write “three hundred and five” in numerals.",
           "3 hundreds, 0 tens, 5 ones. Write 3, 0, 5.", "305 (not 35 or 3005)") +
        "<h2>Partition in different ways</h2>"
        "<p>The <b>standard</b> way uses each digit: 346 = 300 + 40 + 6. "
        "A <b>non-standard</b> way trades 1 hundred for 10 tens.</p>"
        "<figure class='sn-fig'>" + mab_svg(2, 14, 6, labels=True) +
        "<figcaption>2 hundreds, 14 tens and 6 ones is also 346: 200 + 140 + 6 = 346.</figcaption></figure>" +
        ex("Partition", "Partition 346 in two ways.",
           "Standard: 3 hundreds, 4 tens and 6 ones. Non-standard: 2 hundreds, 14 tens and 6 ones.",
           "300 + 40 + 6 = 200 + 140 + 6") +
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 3-digit number is bigger than a 2-digit number. "
        "If both have 3 digits, compare the hundreds, then the tens, then the ones.</p>" +
        ex("Compare", "452 ☐ 425", "Hundreds: 4 = 4. Tens: 5 tens &gt; 2 tens.", "452 &gt; 425") +
        "<p>&gt; means “is greater than”. &lt; means “is less than”. The open side faces the bigger number.</p>"
        "<figure class='sn-fig'>" + number_line_svg(0, 1000, 100, [0, 500, 1000], 600, show="600") +
        "<figcaption>Each mark is 100. The arrow is 1 mark after 500, so it shows 600.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing each part you hear (three hundred and five = 3005)", "A hundreds number has 3 digits: 305"],
            ["Leaving out the zero (305 = 35)", "Write 0 for the empty tens place: 305"],
            ["Giving the digit, not its value (the 4 in 345 is 4)", "The 4 is in the tens place: 40"],
            ["Writing 14 tens inside the number (2 hundreds, 14 tens, 6 ones = 2146)",
             "14 tens = 140, so 200 + 140 + 6 = 346"],
            ["Comparing the first digits only (98 &gt; 102)", "Count the digits first: 102 &gt; 98"],
        ])
    )


FAQ = [
    {"q": "What place value does a Year 2 student learn in Australia?",
     "a": "The Australian Curriculum (AC9M2N02) asks Year 2 students to partition, rearrange, regroup and rename two- and three-digit numbers and to understand the role of zero. They also order numbers to at least 1000 (AC9M2N01)."},
    {"q": "What are MAB blocks?",
     "a": "MAB (multi-base arithmetic blocks) are the base-ten blocks used in Australian classrooms: a mini is 1, a long is 10 and a flat is 100. Children build numbers with them to see what each digit is worth."},
    {"q": "Why is zero important in place value?",
     "a": "Zero holds an empty place so the other digits keep their value. Without it, 305 would become 35, so children learn to write 0 when there are no tens or no ones."},
    {"q": "What is non-standard partitioning?",
     "a": "It means splitting a number in a way other than hundreds, tens and ones digits. For example, 346 can be 2 hundreds, 14 tens and 6 ones, which helps children trade and regroup when they add and subtract."},
]


def mark_large(u, pattern):
    """Tag wide pictures (MAB, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(2801)
    P = People(random.Random(28011))
    sets = [set_mab(rnd), set_value(rnd), set_zero(rnd, P), set_partition(rnd), set_problems(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "place-value-to-1000", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value to 1000: Hundreds, Tens and Ones",
        "seo_title": "Year 2 Place Value Worksheets: Numbers to 1000, Free with Answer Key",
        "short_title": "Place value to 1000",
        "domain": "Number",
        "standard_code": "AC9M2N02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Partition, rearrange, regroup and rename two- and three-digit numbers using standard and non-standard groupings; recognise the role of zero in place value notation",
        "meta_desc": "Free Year 2 place value maths worksheets for the Australian Curriculum: hundreds, tens and ones with MAB, the value of each digit, zero as a place holder, standard and non-standard partitioning, and comparing and ordering numbers to 1000. 100 questions with an answer key.",
        "key_big": "The place of a digit tells you its value. The 4 in 345 is worth 40.",
        "key_sub": "Write 0 for an empty place: three hundred and five is 305, not 35 or 3005. 346 is 3 hundreds, 4 tens and 6 ones, or 2 hundreds, 14 tens and 6 ones.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(MAB blocks|place value chart|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
