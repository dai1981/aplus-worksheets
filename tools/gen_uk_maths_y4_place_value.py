# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Place Value (National Curriculum in England, Year 4: Number and place value)
  python tools/gen_uk_maths_y4_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are written with commas. Negative numbers use the real minus sign − (U+2212).
Rounding and Roman numerals are separate units.
Wrong answers come from real mistakes: giving the digit instead of its value (the 3 in 4,352 is 3),
leaving out a zero placeholder (4,000 + 60 + 2 = 462), changing the wrong digit for 1,000 more or less,
counting in the wrong multiple, comparing the first digits only, and skipping 0 when counting back.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

PL = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
PL1 = ["one", "ten", "hundred", "thousand", "ten thousand"]


# ------------------------------------------------------------ helpers
def c(n):
    """Number with commas and a real minus sign: 4536 -> 4,536, -3 -> −3."""
    return (M if n < 0 else "") + "{:,}".format(abs(n))


def deg(n):
    return c(n) + " °C"


def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        if x in seen or not x:
            continue
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_n(q, correct, cands, e, rnd):
    """Whole-number choices with commas. Wrong numbers that are 0 or less are dropped."""
    return mcq(q, c(correct), [c(v) for v in cands if v is not None and v > 0 and v != correct], e, rnd)


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


def ndig(n):
    return len(str(n))


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def expanded(n):
    return " + ".join(c(digit(n, i) * 10 ** i) for i in range(ndig(n) - 1, -1, -1) if digit(n, i))


def zero_mistakes(n):
    """Numbers a pupil writes when a zero goes missing, moves, or is added."""
    s = str(n)
    out = []
    for i, ch in enumerate(s):
        if ch == "0":
            out.append(int(s[:i] + s[i + 1:]))                 # left out a zero
            for j in (i - 1, i + 1):                            # zero swapped with a neighbour
                if 0 < j < len(s) and s[j] != "0":
                    l = list(s)
                    l[i], l[j] = l[j], l[i]
                    out.append(int("".join(l)))
    for i in range(1, len(s)):                                  # an extra zero
        if s[i] == "0":
            out.append(int(s[:i] + "0" + s[i:]))
    return [v for v in out if v != n and 10 <= v < 100000]


def joined_digits(n):
    """Writing only the non-zero digits side by side (4,000 + 60 + 2 -> 462)."""
    return int("".join(ch for ch in str(n) if ch != "0"))


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


# ------------------------------------------------------------ figures
CW, HEAD, ROW = 96, 34, 50


def chart_svg(n, hi=None):
    """Thousands / hundreds / tens / ones chart with n in it. hi = place index (3..0) to colour red."""
    x0 = y0 = 6
    W, H = 2 * x0 + 4 * CW, 2 * y0 + HEAD + ROW
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, 4 * CW, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, 4 * CW, HEAD, FILL)]
    for k in range(4):
        i = 3 - k
        x = x0 + k * CW
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (x, y0, x, y0 + HEAD + ROW, GREEN))
        cx = x + CW / 2
        s.append(text(cx, y0 + 23, cap(PL[i]), 15, bold=True))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, bold=True, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 4 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, H, "".join(s), "place value chart showing %s" % c(n))


CR = 23           # counter radius
CS = 50           # counter spacing
CGAP = 14         # gap between columns


def counters_svg(n):
    """Place value counters: one column for each place, up to 9 counters as a 3 x 3 grid.
    Empty places get an empty column so the zero can be seen."""
    x0, y0 = 8, 8
    colw = 3 * CS
    W = 2 * x0 + 4 * colw + 3 * CGAP
    H = 2 * y0 + 3 * CS
    s = []
    for k in range(4):
        i = 3 - k
        d = digit(n, i)
        x = x0 + k * (colw + CGAP)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.2' "
                 "stroke-dasharray='4 4'/>" % (x - 2, y0 - 2, colw + 4, 3 * CS + 4, GRAY))
        for j in range(d):
            cx = x + CS / 2 + (j % 3) * CS
            cy = y0 + CS / 2 + (j // 3) * CS
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.8'/>"
                     % (cx, cy, CR, FILL if i % 2 else "#ffffff", GREEN))
            s.append(text(cx, cy + 5, c(10 ** i), 14))
    return svg_wrap(W, H, "".join(s), "place value counters")


def number_line_svg(lo, hi, step, labels, arrow, show=None):
    """Number line lo..hi with a tick every step, numbers under `labels` and a red arrow at `arrow`.
    show = text above the arrow (lesson pictures only)."""
    L, R, Y = 40, 420, 58
    W, H = 460, 100
    span = hi - lo

    def X(v):
        return L + (v - lo) * (R - L) / span

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 30, c(v), 15, bold=True, col=GREEN))
        v += step
    ax = X(arrow)
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    if show:
        s.append(text(min(max(ax, 40), W - 40), Y - 44, show, 15, bold=True, col=RED))
    top = 0 if not show else 0
    return svg_wrap(W, H + top, "".join(s), "number line from %s to %s" % (c(lo), c(hi)))


def neg_line_svg(lo, hi, labels, arrow=None, jumps=None, g=19):
    """Number line through zero, one tick for every whole number. jumps = (start, end) draws hops."""
    pad = 28
    n = hi - lo
    W = 2 * pad + n * g
    Y = 46 if jumps else 36
    H = Y + 34

    def X(v):
        return pad + (v - lo) * g

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 16, Y, W - pad + 16, Y, INK),
         "<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (pad - 18, Y, W - pad + 18, Y, INK)]
    for v in range(lo, hi + 1):
        big = v in labels
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (9 if big else 6), X(v), Y + (9 if big else 6), INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 26, c(v), 14, bold=(v == 0)))
    if jumps:
        a, b = jumps
        st = -1 if b < a else 1
        for v in range(a, b, st):
            x1, x2 = X(v), X(v + st)
            s.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='1.6'/>"
                     % (x1, Y - 4, (x1 + x2) / 2, Y - 26, x2, Y - 4, RED))
        s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (X(b), Y, RED))
    if arrow is not None:
        ax = X(arrow)
        s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (ax - 6, Y - 20, ax + 6, Y - 20, ax, Y - 8, RED))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 34, ax, Y - 18, RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (c(lo), c(hi)))


def thermo_svg(lo, hi, val):
    """Celsius thermometer: a tick every degree, numbers every 5 degrees, red column up to val."""
    g = 10
    top = 16
    x = 70
    Yv = lambda v: top + (hi - v) * g
    bot = Yv(lo)
    s = ["<rect x='%d' y='%d' width='14' height='%d' rx='7' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
         % (x - 7, top - 8, bot - top + 16, INK)]
    s.append("<circle cx='%d' cy='%d' r='12' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, bot + 18, RED, INK))
    s.append("<rect x='%d' y='%d' width='6' height='%d' fill='%s'/>" % (x - 3, Yv(val), bot + 14 - Yv(val), RED))
    for v in range(lo, hi + 1):
        y = Yv(v)
        big = v % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x - 9 - (9 if big else 4), y, x - 9, y, INK, "1.6" if big else "1"))
        if big:
            s.append(text(x - 22, y + 5, c(v), 14, anchor="end", bold=(v == 0)))
    s.append(text(x + 14, top + 4, "°C", 14, anchor="start", bold=True))
    H = int(bot + 36)
    return svg_wrap(108, H, "".join(s), "thermometer from %s to %s degrees Celsius" % (c(lo), c(hi)))


# ============================================================ set 1: value of each digit
def distinct4(rnd, used):
    while True:
        d = rnd.sample(range(10), 4)
        if d[0] == 0:
            continue
        n = int("".join(map(str, d)))
        if n not in used:
            used.add(n)
            return n


def value_cands(d, i):
    out = [d, d * 10 ** (i - 1) if i >= 1 else None, d * 10 ** (i + 1)]
    if i >= 2:
        out.append(d * 10 ** (i - 2))
    return [v for v in out if v and v != d * 10 ** i] + [d * 10 ** (i + 2)]


def value_e(d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %s. The digit is %d, but its value is %s."
            % ("red " if red else "", d, PL[i], plural(d, i), c(v), d, c(v)))


def set_value(rnd, used):
    its = []
    # value of the red digit in a chart (5)
    for i in [3, 2, 1, 2, 3]:
        while True:
            n = distinct4(rnd, used)
            if digit(n, i):
                break
        d = digit(n, i)
        its.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                         value_cands(d, i), value_e(d, i, True), rnd))
    # value of a digit, no chart (5)
    for i in [2, 1, 3, 2, 1]:
        while True:
            n = distinct4(rnd, used)
            if digit(n, i):
                break
        d = digit(n, i)
        its.append(mcq_n("What is the value of the digit %d in %s?" % (d, c(n)), d * 10 ** i,
                         value_cands(d, i), value_e(d, i), rnd))
    # which digit is in a place (4)
    for i in [2, 1, 3, 2]:
        n = distinct4(rnd, used)
        d = digit(n, i)
        e = ("%s has %s." % (c(n), ", ".join(plural(digit(n, x), x) for x in range(3, -1, -1)))
             + " The %s digit is %d." % (PL[i], d))
        cands = [digit(n, x) for x in sorted(range(4), key=lambda x: (abs(x - i), x)) if x != i]
        its.append(mcq("In %s, which digit is in the %s place?" % (c(n), PL[i]), d, cands, e, rnd))
    # what the digit stands for (3)
    for i in [2, 1, 2]:
        while True:
            n = distinct4(rnd, used)
            if digit(n, i):
                break
        d = digit(n, i)
        ans = "%d %s" % (d, PL[i])
        wrong = ["%d %s" % (d, PL[x]) for x in range(4) if x != i]
        its.append(mcq("In %s, what does the digit %d stand for?" % (c(n), d), ans, wrong,
                       "Read the places from the left: thousands, hundreds, tens, ones. The %d is in the %s place, "
                       "so it stands for %d %s, or %s." % (d, PL[i], d, PL[i], c(d * 10 ** i)), rnd))
    # which number has a digit in a place (3)
    for d, i in [(7, 2), (4, 1), (5, 3)]:
        others = [x for x in range(1, 10) if x != d]
        rnd.shuffle(others)
        base = others[:3]
        nums = {}
        for pos in [3, 2, 1, 0]:
            ds = base[:]
            ds.insert(3 - pos, d)
            nums[pos] = int("".join(map(str, ds)))
        assert digit(nums[i], i) == d
        its.append(mcq("Which number has a %d in the %s place?" % (d, PL[i]), c(nums[i]),
                       [c(nums[x]) for x in nums if x != i],
                       "The %s place is the %s digit from the right. In %s the %d is there, so it is worth %s."
                       % (PL[i], ["1st", "2nd", "3rd", "4th"][i], c(nums[i]), d, c(d * 10 ** i)), rnd))
    order = its[:3] + its[10:12] + its[3:5] + its[5:8] + its[12:14] + its[14:16] + its[8:10] + its[16:]
    assert len(order) == 20
    return {"title": "Value of each digit in a 4-digit number", "items": order}


# ============================================================ set 2: partition and represent
def with_zero(rnd, used, zeros=(1, 2)):
    while True:
        ds = [rnd.randint(1, 9)] + [rnd.randint(0, 9) for _ in range(3)]
        z = sum(1 for x in ds[1:] if x == 0)
        n = int("".join(map(str, ds)))
        if z in zeros and n not in used and len(set(zero_mistakes(n))) >= 3:
            used.add(n)
            return n


def set_partition(rnd, used):
    its = []
    # counters (5)
    for j in range(5):
        if j in (1, 3):
            n = with_zero(rnd, used, zeros=(1,))
        else:
            n = distinct4(rnd, used)
            while 0 in [digit(n, x) for x in range(4)]:
                n = distinct4(rnd, used)
        cands = []
        if "0" in str(n):
            cands.append(joined_digits(n))
        cands += zero_mistakes(n)
        cands.append(int(str(n)[::-1]) if n % 10 else None)          # read the ones first
        cands += [n + 10 ** i for i in range(4) if digit(n, i) < 9]   # miscounted one group
        e = ("Count each kind of counter: %s. Write the digits in order: %s."
             % (", ".join(plural(digit(n, i), i) for i in range(3, -1, -1)), c(n)))
        if "0" in str(n):
            e += " There are no %s, so write 0 in that place." % " or ".join(PL[i] for i in range(4) if not digit(n, i))
        its.append(mcq_n(fig(counters_svg(n)) + "What number do the place value counters show?", n, cands, e, rnd))
    # expanded -> number (4)
    for j in range(4):
        n = with_zero(rnd, used)
        cands = [joined_digits(n)] + zero_mistakes(n)
        e = "Put each digit in its place and write 0 in any empty place: %s = %s." % (expanded(n), c(n))
        its.append(mcq_n("What number is <b>%s</b>?" % expanded(n), n, cands, e, rnd))
    # number -> partition (4)
    for j in range(4):
        n = with_zero(rnd, used)
        cands = [expanded(v) for v in zero_mistakes(n) if v >= 100]
        rnd.shuffle(cands)
        e = ("Write the value of each digit that is not 0: %s. A zero adds nothing, so it does not get its own part."
             % expanded(n))
        its.append(mcq("Which shows %s partitioned into thousands, hundreds, tens and ones?" % c(n), expanded(n),
                       cands, e, rnd))
    # missing part (3)
    for i in [2, 1, 3]:
        n = distinct4(rnd, used)
        while 0 in [digit(n, x) for x in range(4)]:
            n = distinct4(rnd, used)
        d = digit(n, i)
        parts = ["☐" if x == i else c(digit(n, x) * 10 ** x) for x in range(3, -1, -1)]
        e = "%s has %s in the %s place. %s = %s, so the missing part is %s." % (
            c(n), d, PL[i], plural(d, i), c(d * 10 ** i), c(d * 10 ** i))
        its.append(mcq_n("%s = %s. What number goes in the box?" % (" + ".join(parts), c(n)), d * 10 ** i,
                         value_cands(d, i), e, rnd))
    # estimate on 0 to 10,000 (2)
    for v in [2800, 6300]:
        cands = [v + 1000, 1000 * (v // 1000) + 1000 - v % 1000, v // 10]
        e = ("Each small mark is 1,000. The arrow is between %s and %s, %s %s. So it shows about %s."
             % (c(v // 1000 * 1000), c(v // 1000 * 1000 + 1000),
                "closer to",
                c(v // 1000 * 1000 + 1000) if v % 1000 > 500 else c(v // 1000 * 1000), c(v)))
        q = fig(number_line_svg(0, 10000, 1000, [0, 5000, 10000], v)) + "Estimate the number the arrow points to."
        its.append(mcq_n(q, v, cands, e, rnd))
    # read exactly between thousands (2)
    for lo, v in [(3000, 3700), (8000, 8400)]:
        k = (v - lo) // 100
        cands = [lo + 10 * k, lo + 1000 - k * 100, v + 100]
        e = ("From %s to %s there are 10 jumps, so each mark is 100, not 10. The arrow is %d marks after %s: %s + %s = %s."
             % (c(lo), c(lo + 1000), k, c(lo), c(lo), c(k * 100), c(v)))
        q = fig(number_line_svg(lo, lo + 1000, 100, [lo, lo + 500, lo + 1000], v)) + "What number does the arrow point to?"
        its.append(mcq_n(q, v, cands, e, rnd))
    order = its[:3] + its[5:7] + its[3:5] + its[9:11] + its[13:16] + its[7:9] + its[16:18] + its[11:13] + its[18:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Partition and represent 4-digit numbers", "items": order}


# ============================================================ set 3: 1,000 more or less, counting in multiples
STEP_SLIPS = {6: [7, 10, 12], 7: [6, 8, 10], 9: [10, 8, 18], 25: [5, 10, 50], 1000: [100, 10, 2000]}
SLIP_WHY = {7: "counted in 7s", 6: "counted in 6s", 8: "counted in 8s", 10: "counted in 10s", 5: "counted in 5s",
            100: "counted in 100s"}


def set_more_less_count(rnd, used):
    its = []
    # 1,000 more or less (6)
    for kind, n in [("more", 4352), ("less", 7068), ("more", 2097), ("less", 1236), ("more", 8905), ("less", 3004)]:
        sg = 1 if kind == "more" else -1
        ans = n + sg * 1000
        cands = [n + sg * 100, n + sg * 10, n - sg * 1000, n + sg * 1]
        e = ("Only the thousands digit changes: %d thousand%s → %d thousand%s. The hundreds, tens and ones stay the same. "
             "%s %s 1,000 = %s." % (digit(n, 3), "" if digit(n, 3) == 1 else "s", digit(ans, 3),
                                    "" if digit(ans, 3) == 1 else "s", c(n), "+" if sg > 0 else M, c(ans)))
        if ans < 1000:
            e = ("%s has 1 thousand. Take it away and the thousands digit becomes 0: %s %s 1,000 = %s."
                 % (c(n), c(n), M, c(ans)))
        its.append(mcq_n("What is 1,000 %s than %s?" % (kind, c(n)), ans, cands, e, rnd))
    # reverse (2)
    for kind, n in [("more", 6281), ("less", 3940)]:
        sg = 1 if kind == "more" else -1
        ans = n - sg * 1000
        cands = [n + sg * 1000, n - sg * 100, n - sg * 10]
        e = ("Work backwards. If 1,000 %s than the number is %s, the number is 1,000 %s than %s: %s."
             % (kind, c(n), "less" if sg > 0 else "more", c(n), c(ans)))
        its.append(mcq_n("1,000 %s than a number is %s. What is the number?" % (kind, c(n)), ans, cands, e, rnd))
    # sequences (9)
    specs = [(6, "next", [18, 24, 30, 36]),
             (7, "next", [35, 42, 49, 56]),
             (9, "next", [27, 36, 45, 54]),
             (25, "next", [125, 150, 175, 200]),
             (1000, "next", [2405, 3405, 4405, 5405]),
             (6, "missing", [42, 48, None, 60, 66]),
             (7, "back", [84, 77, 70, 63]),
             (25, "back", [300, 275, 250, 225]),
             (1000, "back", [9060, 8060, 7060, 6060])]
    for s, kind, seq in specs:
        if kind == "missing":
            k = seq.index(None)
            base = seq[k - 1]
            ans = base + s
            assert seq[k + 1] == ans + s
            cands = [base + s + 1, base + 10, base + s - 1]
            show = ", ".join("☐" if v is None else c(v) for v in seq)
            q = "Count in %ss: %s. What number goes in the box?" % (c(s), show)
            e = "The numbers go up by %s each time. %s + %s = %s. Check: %s + %s = %s." % (
                c(s), c(base), c(s), c(ans), c(ans), c(s), c(seq[k + 1]))
        else:
            sg = 1 if kind == "next" else -1
            for a, b in zip(seq, seq[1:]):
                assert b - a == sg * s
            ans = seq[-1] + sg * s
            cands = [seq[-1] + sg * w for w in STEP_SLIPS[s]]
            q = "%s: %s, ? What comes next?" % ("Count in %ss" % c(s) if sg > 0 else "Count back in %ss" % c(s),
                                                 ", ".join(c(v) for v in seq))
            e = "Each number is %s %s than the one before. %s %s %s = %s." % (
                c(s), "more" if sg > 0 else "less", c(seq[-1]), "+" if sg > 0 else M, c(s), c(ans))
            if s == 1000:
                e += " Only the thousands digit changes."
        its.append(mcq_n(q, ans, cands, e, rnd))
    # multiples (3)
    for s, ans, wrong, why in [
            (9, 63, [59, 56, 66], "7 × 9 = 63. 59 ends in 9 but is not in the 9 times table; 56 is 7 × 8 and 66 is 11 × 6."),
            (7, 49, [47, 54, 36], "7 × 7 = 49. 47 ends in 7 but is not in the 7 times table; 54 is 6 × 9 and 36 is 6 × 6."),
            (25, 175, [155, 205, 240], "Counting in 25s always ends in 00, 25, 50 or 75: 150, 175, 200. "
                                       "155 and 205 end in 5 but are not multiples of 25.")]:
        assert ans % s == 0 and all(w % s for w in wrong)
        its.append(mcq_n("Which number would you say when counting in %ss from 0?" % s, ans, wrong, why, rnd))
    order = its[:6] + its[8:13] + its[17:19] + its[6:8] + its[13:17] + its[19:]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "1,000 more or less and counting in 6s, 7s, 9s, 25s and 1,000s", "items": order}


# ============================================================ set 4: compare, order and count through zero
def first_diff(a, b):
    for i in range(3, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def compare_expl(big, small):
    if ndig(big) != ndig(small):
        return "%s has %d digits and %s has only %d, so %s is greater." % (c(big), ndig(big), c(small), ndig(small), c(big))
    i = first_diff(big, small)
    same = "The digits are the same until the %s place" % PL[i] if i < 3 else "Start with the thousands"
    return ("Compare from the left. %s: %s is more than %s. So %s &gt; %s."
            % (same, plural(digit(big, i), i), plural(digit(small, i), i), c(big), c(small)))


def lookalikes(rnd, used):
    """4 different 4-digit numbers with the same digits and the same thousands digit."""
    while True:
        ds = rnd.sample(range(1, 10), 4)
        out = set()
        tries = 0
        while len(out) < 4 and tries < 60:
            tries += 1
            l = ds[:]
            a, b = rnd.sample(range(1, 4), 2)
            l[a], l[b] = l[b], l[a]
            if rnd.random() < 0.5:
                a, b = rnd.sample(range(1, 4), 2)
                l[a], l[b] = l[b], l[a]
            out.add(int("".join(map(str, l))))
        if len(out) == 4 and not (out & used):
            used.update(out)
            return sorted(out)


def set_compare_zero(rnd, used, P):
    its = []
    # which comparison is true (4)
    pairs = [(4352, 4325), (6089, 6098), (987, 1023), (5710, 5701)]
    for j, (x, y) in enumerate(pairs):
        right = "%s %s %s" % (c(x), "&lt;" if x < y else "&gt;", c(y))
        wrong = ["%s %s %s" % (c(x), "&gt;" if x < y else "&lt;", c(y)), "%s = %s" % (c(x), c(y)),
                 "%s %s %s" % (c(y), "&lt;" if x < y else "&gt;", c(x))]
        e = compare_expl(max(x, y), min(x, y))
        if x == 987:
            e += " A bigger first digit (9) does not matter when there are fewer digits."
        its.append(mcq("Which is true?", right, wrong, e, rnd))
    # greatest (3) and smallest (3)
    for j in range(6):
        if j == 2:
            nums = [998, 1089, 1098, 1009]
        elif j == 5:
            nums = [1206, 999, 1062, 1026]
        else:
            nums = lookalikes(rnd, used)
        nums = sorted(nums)
        want_max = j < 3
        ans = nums[-1] if want_max else nums[0]
        nxt = nums[-2] if want_max else nums[1]
        if want_max:
            e = compare_expl(ans, nxt) + " %s is the greatest." % c(ans)
            if 998 in nums:
                e = ("998 has only 3 digits, so it is the smallest, even though 9 is a big digit. "
                     "Of the 4-digit numbers, " + compare_expl(ans, nxt)[0].lower() + compare_expl(ans, nxt)[1:]
                     + " %s is the greatest." % c(ans))
        else:
            e = compare_expl(nxt, ans) + " %s is the smallest." % c(ans)
        its.append(mcq("Which number is the %s?" % ("greatest" if want_max else "smallest"), c(ans),
                       [c(v) for v in nums if v != ans], e, rnd))
    # order smallest to greatest (2)
    for j in range(2):
        while True:
            nums = lookalikes(rnd, used)
            three = rnd.sample(nums, 3)
            if three != sorted(three):
                break
        o = sorted(three)
        perms = [[o[0], o[2], o[1]], [o[1], o[0], o[2]], o[::-1], [o[2], o[0], o[1]]]
        fmt = lambda l: ", ".join(c(v) for v in l)
        i1, i2 = first_diff(o[1], o[0]), first_diff(o[2], o[1])
        e = ("Compare from the left. %s &lt; %s (%s: %d &lt; %d). %s &lt; %s (%s: %d &lt; %d). So the order is %s."
             % (c(o[0]), c(o[1]), PL[i1], digit(o[0], i1), digit(o[1], i1),
                c(o[1]), c(o[2]), PL[i2], digit(o[1], i2), digit(o[2], i2), fmt(o)))
        its.append(mcq("Put %s in order from smallest to greatest." % fmt(three), fmt(o), [fmt(p) for p in perms], e, rnd))
    # read a number line through zero (3)
    for v in [-3, -7, -4]:
        q = fig(neg_line_svg(-10, 10, [-10, -5, 0, 5, 10], arrow=v)) + "What number does the arrow point to?"
        e = ("The arrow is to the left of 0, so the number is negative. Count back from 0: %s. The answer is %s."
             % (", ".join(c(-k) for k in range(1, -v + 1)), c(v)))
        if v < -5:
            e = ("The arrow is to the left of 0, so the number is negative. It is %d marks past %s: count %s. The answer is %s."
                 % (-5 - v, c(-5), ", ".join(c(-k) for k in range(6, -v + 1)), c(v)))
        its.append(mcq(q, c(v), [c(-v), c(v - 1), c(v + 1)], e, rnd))
    # thermometers (2)
    for v in [-6, -2]:
        q = fig(thermo_svg(-10, 10, v)) + "What temperature does the thermometer show?"
        e = ("The red line ends below 0, so the temperature is negative. Each mark is 1 degree. "
             "Count down from 0: %s. It shows %s." % (", ".join(c(-k) for k in range(1, -v + 1)), deg(v)))
        its.append(mcq(q, deg(v), [deg(-v), deg(v - 1) if v != -6 else deg(-4), deg(v + 1) if v != -6 else deg(-5)],
                       e, rnd))
    # count back through zero (3)
    for seq, s, ans, wrong in [([7, 4, 1], 3, -2, [2, -3, -1]),
                               ([30, 20, 10, 0], 10, -10, [10, -1, -20]),
                               ([5, 3, 1], 2, -1, [1, 0, -2])]:
        assert seq[-1] - s == ans
        steps = [seq[-1] - k for k in range(1, s + 1)]
        e = ("Count back %d from %s, one at a time: %s. Remember to count 0. The answer is %s."
             % (s, c(seq[-1]), ", ".join(c(v) for v in steps), c(ans)))
        if s == 10:
            e = ("10 less than 0 is 10 below zero, so it is %s. Do not forget the minus sign: 10 is above zero."
                 % c(ans))
        its.append(mcq("Count back in %ss: %s, ? What comes next?" % (s, ", ".join(c(v) for v in seq)), c(ans),
                       [c(w) for w in wrong], e, rnd))
    assert len(its) == 20
    return {"title": "Compare and order numbers, and count back through zero", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, used, P):
    its = []
    its.append(mcq_n("A football stadium has 4,068 seats. What is the value of the digit 6 in 4,068?", 60,
                     [6, 600, 6000], "The 6 is in the tens place, so it is worth 6 tens = 60.", rnd))
    its.append(mcq("The village of Ashby has 2,507 people. Which shows 2,507 partitioned?", "2,000 + 500 + 7",
                   ["2,000 + 50 + 7", "200 + 50 + 7", "2,000 + 500 + 70"],
                   "2,507 has 2 thousands, 5 hundreds, 0 tens and 7 ones: 2,000 + 500 + 7. The 0 tens adds nothing.", rnd))
    walkers = [(P.next(), v) for v in [6240, 6420, 6204, 6402]]
    best = max(walkers, key=lambda w: w[1])
    its.append(mcq("Four friends counted their steps on a school trip. %s. Who walked the most steps?"
                   % "; ".join("%s: %s" % (p[0], c(v)) for p, v in walkers), best[0][0],
                   [p[0] for p, v in walkers if v != best[1]],
                   "All four numbers have 6 thousands. Compare the hundreds: 6,420 and 6,402 have 4 hundreds. "
                   "Then the tens: 2 tens &gt; 0 tens, so 6,420 is the greatest. %s walked the most." % best[0][0], rnd))
    vill = [("Westbrook", 1064), ("Little Ashby", 1406), ("Millford", 1460), ("Oakley", 1046)]
    its.append(mcq("These villages have these populations: %s. Which village has the smallest population?"
                   % "; ".join("%s %s" % (n, c(v)) for n, v in vill), "Oakley",
                   ["Westbrook", "Little Ashby", "Millford"],
                   "All four have 1 thousand. 1,064 and 1,046 have 0 hundreds. Compare the tens: 4 tens &lt; 6 tens, "
                   "so 1,046 is the smallest. Oakley has the smallest population.", rnd))
    name, he, his = P.next()
    its.append(mcq_n("%s's dad is a lorry driver. He has driven 3,950 km this month. Next month he will drive 1,000 km more "
                     "than this. How far will he drive next month?" % name, 4950, [3960, 4050, 2950],
                     "1,000 more: only the thousands digit changes. 3 thousands → 4 thousands. 3,950 + 1,000 = 4,950 km.",
                     rnd))
    its[-1]["c"] = [x + " km" for x in its[-1]["c"]]
    its.append(mcq_n("Last year 5,083 people visited a castle. This year 1,000 fewer people visited. "
                     "How many people visited this year?", 4083, [4983, 5073, 6083],
                     "1,000 fewer: only the thousands digit changes. 5 thousands → 4 thousands. 5,083 − 1,000 = 4,083.",
                     rnd))
    its.append(mcq_n("The caretaker stacks chairs in piles of 25. How many chairs are in 6 piles?", 150, [125, 175, 31],
                     "Count in 25s six times: 25, 50, 75, 100, 125, 150. There are 150 chairs.", rnd))
    its.append(mcq_n("There are 7 days in a week. How many days are there in 8 weeks?", 56, [48, 63, 15],
                     "Count in 7s eight times: 7, 14, 21, 28, 35, 42, 49, 56. 8 × 7 = 56 days.", rnd))
    its.append(mcq_n("Eggs come in boxes of 6. How many eggs are in 9 boxes?", 54, [48, 60, 63],
                     "Count in 6s nine times: 6, 12, 18, 24, 30, 36, 42, 48, 54. 9 × 6 = 54 eggs.", rnd))
    its.append(mcq_n("Each bench in the school hall seats 9 children. How many children can sit on 7 benches?", 63,
                     [56, 72, 16], "Count in 9s seven times: 9, 18, 27, 36, 45, 54, 63. 7 × 9 = 63 children.", rnd))
    its.append(mcq("At 7:00 am the temperature was %s. By lunchtime it was 4 degrees warmer. What was the temperature "
                   "at lunchtime?" % deg(-3), deg(1), [deg(-7), deg(7), deg(2)],
                   "Warmer means count up. From %s count up 4: %s, %s, 0, 1. Do not skip 0. It was %s."
                   % (deg(-3), c(-2), c(-1), deg(1)), rnd))
    its.append(mcq("In the evening the temperature was 3 °C. During the night it fell by 5 degrees. "
                   "What was the temperature then?", deg(-2), [deg(2), deg(-3), deg(8)],
                   "Fell means count down. From 3 count down 5: 2, 1, 0, %s, %s. Do not skip 0. It was %s."
                   % (c(-1), c(-2), deg(-2)), rnd))
    cities = [("Edinburgh", -4), ("Belfast", -1), ("Cardiff", 2), ("Manchester", -2)]
    its.append(mcq("One winter morning the temperatures were: %s. Which city was the coldest?"
                   % "; ".join("%s %s" % (n, deg(v)) for n, v in cities), "Edinburgh",
                   ["Belfast", "Cardiff", "Manchester"],
                   "The coldest temperature is the one furthest below 0. %s is 4 degrees below 0, which is colder than "
                   "%s or %s. Edinburgh was the coldest." % (deg(-4), deg(-2), deg(-1)), rnd))
    its.append(mcq_n("A shop has 4 boxes of 1,000 stickers, 12 packs of 100 stickers and 6 single stickers. "
                     "How many stickers is that?", 5206, [4126, 5260, 4206],
                     "12 hundreds = 1 thousand and 2 hundreds. So there are 5 thousands, 2 hundreds, 0 tens and 6 ones: "
                     "4,000 + 1,200 + 6 = 5,206.", rnd))
    name, she, her = P.next()
    its.append(mcq_n("%s thinks of a number. It has 3 thousands, 0 hundreds, 8 tens and 6 ones. What is %s number?"
                     % (name, her), 3086, [386, 3806, 3860],
                     "Write the digits in order: 3 thousands, 0 hundreds, 8 tens, 6 ones → 3,086. "
                     "The 0 keeps the 3 in the thousands place.", rnd))
    name, he, his = P.next()
    its.append(mcq_n("%s counts on in 1,000s from 2,450: 2,450, 3,450, … What is the 5th number %s says?" % (name, he),
                     6450, [7450, 2950, 5450],
                     "Write the 5 numbers: 2,450, 3,450, 4,450, 5,450, 6,450. The 5th number is 6,450.", rnd))
    name, he, his = P.next()
    its.append(mcq("%s's family parks in a car park. The ground floor is level 0. The floors below ground are "
                   "level %s, level %s and so on. %s gets into the lift on level 2 and goes down 4 levels. "
                   "Which level is %s on now?" % (name, c(-1), c(-2), cap(he), he),
                   "level " + c(-2), ["level 2", "level " + c(-3), "level 6"],
                   "Count down 4 from level 2: 1, 0, %s, %s. Do not skip level 0. %s is on level %s."
                   % (c(-1), c(-2), cap(he), c(-2)), rnd))
    sch = [1253, 1325, 1235, 1352]
    o = sorted(sch[:3])
    fmt = lambda l: ", ".join(c(v) for v in l)
    its.append(mcq("Three secondary schools have %s pupils. Which list shows these numbers from smallest to greatest?"
                   % fmt(sch[:3]), fmt(o), [fmt([o[1], o[0], o[2]]), fmt([o[0], o[2], o[1]]), fmt(o[::-1])],
                   "All have 1 thousand. 1,235 and 1,253 have 2 hundreds, 1,325 has 3 hundreds. "
                   "1,235 &lt; 1,253 because 3 tens &lt; 5 tens. Order: %s." % fmt(o), rnd))
    name, she, her = P.next()
    its.append(mcq_n(fig(number_line_svg(0, 10000, 1000, [0, 5000, 10000], 7500)) +
                     "%s's step goal is 10,000 steps a day. The arrow shows how many steps %s has walked so far today. "
                     "About how many steps is that?" % (name, she), 7500, [8500, 2500, 750],
                     "Each mark is 1,000 steps. The arrow is halfway between 7,000 and 8,000, so it shows about 7,500 steps.",
                     rnd))
    its.append(mcq_n("Use each of the digits 3, 8, 0 and 5 once to make the greatest 4-digit number.", 8530,
                     [8503, 8350, 5830],
                     "Put the biggest digit in the thousands place, then the next biggest, and so on: 8, 5, 3, 0. "
                     "The greatest number is 8,530.", rnd))
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
        "<h2>Thousands, hundreds, tens and ones</h2>"
        "<p>A 4-digit number has a <b>thousands</b> digit, a <b>hundreds</b> digit, a <b>tens</b> digit and a "
        "<b>ones</b> digit. The place tells you what the digit is worth. 10 hundreds make 1 thousand.</p>"
        "<figure class='sn-fig'>" + chart_svg(4352, hi=2) +
        "<figcaption>In 4,352 the 3 is in the hundreds place. Its value is 3 hundreds, or 300.</figcaption></figure>"
        "<figure class='sn-fig'>" + counters_svg(3042) +
        "<figcaption>Place value counters for 3,042: 3 thousands, 0 hundreds, 4 tens and 2 ones. "
        "There are no hundreds, so the hundreds digit is 0.</figcaption></figure>" +
        ex("Partition", "Partition 7,305 into thousands, hundreds, tens and ones.",
           "7 thousands = 7,000. 3 hundreds = 300. 0 tens = nothing. 5 ones = 5.", "7,000 + 300 + 5") +
        "<h2>1,000 more and 1,000 less</h2>"
        "<p>To find 1,000 more or 1,000 less, change <b>only the thousands digit</b>. "
        "The hundreds, tens and ones stay the same.</p>" +
        table(["1,000 less", "Number", "1,000 more"], [
            ["3,352", "4,352", "5,352"],
            ["236", "1,236", "2,236"],
            ["7,905", "8,905", "9,905"],
        ]) +
        "<h2>Counting in 6s, 7s, 9s, 25s and 1,000s</h2>" +
        table(["Count in", "Numbers"], [
            ["6s", "6, 12, 18, 24, 30, 36, 42, 48, 54, 60"],
            ["7s", "7, 14, 21, 28, 35, 42, 49, 56, 63, 70"],
            ["9s", "9, 18, 27, 36, 45, 54, 63, 72, 81, 90"],
            ["25s", "25, 50, 75, 100, 125, 150, 175, 200"],
            ["1,000s", "2,405, 3,405, 4,405, 5,405, 6,405"],
        ]) +
        "<p>Counting in 9s: add 10, then take away 1 (36 → 46 → 45). Counting in 25s always ends in 00, 25, 50 or 75.</p>"
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 4-digit number is greater than any 3-digit number. If both have 4 digits, "
        "compare place by place from the left until two digits are different.</p>" +
        ex("Compare", "6,089 ☐ 6,098",
           "Thousands: 6 = 6. Hundreds: 0 = 0. Tens: 8 &lt; 9.", "6,089 &lt; 6,098") +
        "<h2>Estimate on a number line</h2>"
        "<figure class='sn-fig'>" + number_line_svg(0, 10000, 1000, [0, 5000, 10000], 2800, show="about 2,800") +
        "<figcaption>Each mark is 1,000. The arrow is between 2,000 and 3,000, closer to 3,000, so it shows about 2,800."
        "</figcaption></figure>"
        "<h2>Counting back through zero</h2>"
        "<p>Numbers below 0 are <b>negative numbers</b>. We write them with a minus sign: " + c(-1) + ", " + c(-2) + ", "
        + c(-3) + ". We use them for temperatures below 0 °C.</p>"
        "<figure class='sn-fig'>" + neg_line_svg(-5, 5, list(range(-5, 6)), jumps=(2, -3), g=34) +
        "<figcaption>Count back 5 from 2: 1, 0, " + c(-1) + ", " + c(-2) + ", " + c(-3) +
        ". The 0 counts as one step.</figcaption></figure>" +
        ex("Temperature", "It is 3 °C. The temperature falls by 5 degrees. What is it now?",
           "Count down 5: 2, 1, 0, " + c(-1) + ", " + c(-2) + ".", deg(-2)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Giving the digit, not its value (the 3 in 4,352 is 3)", "The 3 is in the hundreds place: 300"],
            ["Leaving out a zero (4,000 + 60 + 2 = 462)", "Write 0 in the empty hundreds place: 4,062"],
            ["Changing the wrong digit (1,000 more than 4,352 = 4,452)", "Change the thousands digit: 5,352"],
            ["Comparing the first digits only (998 &gt; 1,089)", "Count the digits first: 1,089 &gt; 998"],
            ["Skipping 0 when counting back (1, " + c(-1) + ", " + c(-2) + ")", "Say 0: 1, 0, " + c(-1)],
        ])
    )


FAQ = [
    {"q": "What place value should a Year 4 child know?",
     "a": "In Year 4 children work with numbers beyond 1,000. They know the value of each digit in a 4-digit number, find 1,000 more or less, count in 6s, 7s, 9s, 25s and 1,000s, compare and order numbers, and count back through zero."},
    {"q": "How do you find 1,000 more or less than a number?",
     "a": "Change only the thousands digit by 1 and keep the other digits the same. 1,000 more than 4,352 is 5,352, and 1,000 less is 3,352."},
    {"q": "What are place value counters?",
     "a": "Place value counters are round counters marked 1, 10, 100 or 1,000. Children build a number with them, for example 3 thousands, 4 tens and 2 ones make 3,042."},
    {"q": "Do Year 4 children learn negative numbers?",
     "a": "Yes. The National Curriculum asks Year 4 pupils to count backwards through zero to include negative numbers, often on a number line or a thermometer, for example 2, 1, 0, −1, −2."},
]


def mark_large(u, pattern):
    """Tag wide pictures (charts, counters, number lines, thermometers) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(4402)
    P = People(rnd)
    used = set()
    sets = [set_value(rnd, used), set_partition(rnd, used), set_more_less_count(rnd, used),
            set_compare_zero(rnd, used, P), set_words(rnd, used, P)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
    u = {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "place-value", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value: 4-Digit Numbers, 1,000 More or Less and Counting Through Zero",
        "seo_title": "Year 4 Place Value Worksheets: 4-Digit Numbers, Counting in Multiples and Negative Numbers",
        "short_title": "Place value",
        "domain": "Number and place value",
        "standard_code": "Year 4: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count in multiples of 6, 7, 9, 25 and 1,000; find 1,000 more or less than a given number; count backwards through zero to include negative numbers; recognise the place value of each digit in a four-digit number (thousands, hundreds, tens, and ones); order and compare numbers beyond 1,000; identify, represent and estimate numbers using different representations.",
        "meta_desc": "Free Year 4 place value maths worksheets for the National Curriculum: the value of each digit in 4-digit numbers, partitioning, place value counters, 1,000 more or less, counting in 6s, 7s, 9s, 25s and 1,000s, comparing and ordering, and counting back through zero. 100 questions with an answer key.",
        "key_big": "In a 4-digit number each digit is worth thousands, hundreds, tens or ones. The place decides the value.",
        "key_sub": "The 3 in 4,352 is worth 300. Write 0 in any empty place, change only the thousands digit for 1,000 more or less, and remember to say 0 when you count back past it.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(place value chart|place value counters|number line|thermometer)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
