# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Place Value to 1,000 (National Curriculum in England, Year 3: Number and place value)
  python tools/gen_uk_maths_y3_place_value.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers below 1,000 have no comma; 1,000 and above are written with commas.
Number words follow British English: "three hundred and six", "two hundred and forty-three".
Wrong answers come from real mistakes: writing "three hundred and six" as 3006 or 36, giving the digit
instead of its value (the 4 in 349 is 4), mixing up tens and ones, fifteen/fifty, changing the wrong digit
for 10 or 100 more or less (295 + 10 = 395), counting in the wrong multiple, and comparing by the last digit.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

PL = ["ones", "tens", "hundreds"]
PL1 = ["one", "ten", "hundred"]


# ------------------------------------------------------------ helpers
def c(n):
    """Number with a comma from 1,000: 1000 -> 1,000, 306 -> 306."""
    return "{:,}".format(n)


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


def mcq_n(q, correct, cands, e, rnd, unit=""):
    """Whole-number choices with commas. Wrong numbers that are 0 or less are dropped."""
    it = mcq(q, c(correct), [c(v) for v in cands if v is not None and v > 0 and v != correct], e, rnd)
    if unit:
        it["c"] = [x + unit for x in it["c"]]
    return it


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


def hto(n):
    return n // 100, n // 10 % 10, n % 10


def plural(d, i):
    return "%d %s" % (d, PL[i] if d != 1 else PL1[i])


def hto_text(h, t, o):
    return "%s, %s, %s" % (plural(h, 2), plural(t, 1), plural(o, 0))


def expanded(n):
    h, t, o = hto(n)
    return " + ".join(str(v) for v in (h * 100, t * 10, o) if v)


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


# ------------------------------------------------------------ number words (British: "and" after hundred)
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words99(n):
    if n < 20:
        return ONES[n]
    return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")


def words(n):
    assert 0 < n < 10000
    out = []
    th, r = divmod(n, 1000)
    h, r = divmod(r, 100)
    if th:
        out.append(ONES[th] + " thousand")
    if h:
        out.append(ONES[h] + " hundred")
    s = " ".join(out)
    if r:
        s = (s + " and " if s else "") + words99(r)
    return s


# ------------------------------------------------------------ typical mistakes
def swap_to(n):
    """Tens and ones mixed up: 427 -> 472."""
    h, t, o = hto(n)
    return h * 100 + o * 10 + t


def drop_zero(n):
    """306 -> 36, 450 -> 45 (a zero place left out)."""
    s = str(n)
    return int(s[0] + s[1:].replace("0", "")) if "0" in s[1:] and s[1:] != "00" else None


def as_heard(n):
    """Writing each spoken part: three hundred and six -> 3006."""
    h, r = divmod(n, 100)
    return int(str(h * 100) + str(r)) if 0 < r < 10 else None


def teen_mix(n):
    """fifteen / fifty and thirty / thirteen mixed up."""
    h, t, o = hto(n)
    if t == 1 and o >= 3:
        return h * 100 + o * 10
    if o == 0 and t >= 3:
        return h * 100 + 10 + t
    return None


def write_cands(n):
    h, t, o = hto(n)
    out = [as_heard(n), drop_zero(n), teen_mix(n)]
    if t != o:
        out.append(swap_to(n))
    if o and o != h:
        out.append(o * 100 + t * 10 + h)
    out += [n + 10 if t < 9 else n - 10, n + 100 if h < 9 else n - 100]
    return out


# ------------------------------------------------------------ figures
U = 8                      # one small cube = U x U, a rod = U x 10U, a flat = 10U x 10U
FG, RG, CG, GG, MG = 8, 6, 4, 20, 6


def blocks_svg(h, t, o, labels=False):
    """Base-ten blocks: h hundred squares, t ten rods, o ones cubes. Sizes are exact (1 : 10 : 100)."""
    F = 10 * U
    fcols = h if h <= 2 else (h + 1) // 2
    frows = 1 if h <= 2 else 2
    groups = []

    def flats(x, y):
        s = []
        for k in range(h):
            fx = x + (k % fcols) * (F + FG)
            fy = y + (k // fcols) * (F + FG)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (fx, fy, F, F, FILL, GREEN))
            for i in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (fx + i * U, fy, fx + i * U, fy + F, GREEN))
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                         % (fx, fy + i * U, fx + F, fy + i * U, GREEN))
        return s

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

    if h:
        groups.append((fcols * F + (fcols - 1) * FG, frows * F + (frows - 1) * FG, flats, plural(h, 2)))
    if t:
        groups.append((t * U + (t - 1) * RG, F, rods, plural(t, 1)))
    if o:
        groups.append((ccols * U + (ccols - 1) * (CG + 2), 5 * U + 4 * (CG + 4), cubes, plural(o, 0)))
    lab_w = lambda s: int(len(s) * 8.6) + 4
    widths = [max(g[0], lab_w(g[3])) if labels else g[0] for g in groups]
    body_h = max(g[1] for g in groups)
    W = 2 * MG + sum(widths) + GG * (len(groups) - 1)
    Hh = 2 * MG + body_h + (26 if labels else 0)
    s = []
    x = MG
    for (gw, gh, draw, lab), w in zip(groups, widths):
        s += draw(x + (w - gw) // 2, MG)
        if labels:
            s.append(text(x + w / 2, MG + body_h + 20, lab, 15, bold=True))
        x += w + GG
    return svg_wrap(W, Hh, "".join(s), "base-ten blocks")


CW, HEAD, ROW = 96, 34, 50


def chart_svg(n, hi=None):
    """Hundreds / tens / ones chart with n in it. hi = place (2, 1, 0) to colour red."""
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
        s.append(text(cx, y0 + 23, cap(PL[i]), 15, bold=True))
        s.append(text(cx, y0 + HEAD + 36, str(digit(n, i)), 30, bold=True, col=RED if hi == i else INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, x0 + 3 * CW, y0 + HEAD, GREEN))
    return svg_wrap(W, Hh, "".join(s), "place value chart showing %d" % n)


CR, CS, CGAP = 23, 50, 14


def counters_svg(n):
    """Place value counters 100 / 10 / 1, up to 9 of each as a 3 x 3 grid. Empty places keep an empty box."""
    x0, y0 = 8, 8
    colw = 3 * CS
    W = 2 * x0 + 3 * colw + 2 * CGAP
    Hh = 2 * y0 + 3 * CS
    s = []
    for k in range(3):
        i = 2 - k
        d = digit(n, i)
        x = x0 + k * (colw + CGAP)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.2' "
                 "stroke-dasharray='4 4'/>" % (x - 2, y0 - 2, colw + 4, 3 * CS + 4, GRAY))
        for j in range(d):
            cx = x + CS / 2 + (j % 3) * CS
            cy = y0 + CS / 2 + (j // 3) * CS
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.8'/>"
                     % (cx, cy, CR, FILL if i != 1 else "#ffffff", GREEN))
            s.append(text(cx, cy + 5, str(10 ** i), 15, bold=True))
    return svg_wrap(W, Hh, "".join(s), "place value counters")


def number_line_svg(lo, hi, step, labels, arrow, show=None):
    """Number line lo..hi with a tick every step, numbers under `labels` and a red arrow at `arrow`."""
    L, R, Y = 34, 426, 58
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
            s.append(text(X(v), Y + 30, c(v), 15, bold=True, col=GREEN))
        v += step
    ax = X(arrow)
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (ax - 7, Y - 22, ax + 7, Y - 22, ax, Y - 9, RED))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (ax, Y - 40, ax, Y - 20, RED))
    if show:
        s.append(text(min(max(ax, 60), W - 60), Y - 44, show, 15, bold=True, col=RED))
    top = 18 if show else 0
    body = "".join(s)
    if top:
        body = "<g transform='translate(0 %d)'>%s</g>" % (top, body)
    return svg_wrap(W, Hh + top, body, "number line from %s to %s" % (c(lo), c(hi)))


# ============================================================ set 1: hundreds, tens and ones
def block_cands(h, t, o):
    n = 100 * h + 10 * t + o
    out = [swap_to(n), drop_zero(n), h + t + o, n + 10 if t < 9 else n - 10]
    if o:
        out.append(o * 100 + t * 10 + h)
    out += [n - 10 if t else n + 1, n + 100]
    return out


def count_e(h, t, o, what="blocks"):
    n = 100 * h + 10 * t + o
    if what == "blocks":
        s = "A big square is 100, a rod is 10 and a small cube is 1. "
    else:
        s = "Count the counters in each box. "
    s += "%s, %s and %s: %s = %d." % (plural(h, 2), plural(t, 1), plural(o, 0), expanded(n), n)
    if t == 0:
        s += " There are no tens, so write 0 in the tens place."
    elif o == 0:
        s += " There are no ones, so write 0 in the ones place."
    return s


def value_cands(d, i):
    out = [d, d * 10 ** (i + 1) if i < 2 else None, d * 10 ** (i - 1) if i >= 1 else None, d * 10 ** (i - 2) if i == 2 else None]
    return [v for v in out if v and v != d * 10 ** i] + [d * 1000, d * 10 + d]


def value_e(n, d, i, red=False):
    v = d * 10 ** i
    return ("The %s%d is in the %s place, so it is worth %s = %d. The digit is %d, but its value is %d."
            % ("red " if red else "", d, PL[i], plural(d, i), v, d, v))


def distinct3(rnd, used):
    while True:
        h, t, o = rnd.randint(1, 9), rnd.randint(1, 9), rnd.randint(1, 9)
        n = 100 * h + 10 * t + o
        if len({h, t, o}) == 3 and n not in used:
            used.add(n)
            return n


def set_hto(rnd, used):
    its = []
    # base-ten blocks: what number? (6)
    specs = []
    while len(specs) < 3:
        h, t, o = rnd.randint(1, 5), rnd.randint(1, 7), rnd.randint(1, 9)
        if len({h, t, o}) == 3 and (h, t, o) not in specs:
            specs.append((h, t, o))
    specs = specs[:2] + [(rnd.randint(2, 5), 0, rnd.randint(2, 8)), specs[2],
                         (rnd.randint(1, 4), rnd.randint(2, 7), 0), (rnd.randint(2, 5), 0, rnd.randint(2, 8))]
    blocks = []
    for h, t, o in specs:
        n = 100 * h + 10 * t + o
        assert n not in used
        used.add(n)
        blocks.append(mcq_n(fig(blocks_svg(h, t, o)) + "What number do the blocks show?", n,
                            block_cands(h, t, o), count_e(h, t, o), rnd))
    # which matches the blocks (2)
    match = []
    for _ in range(2):
        while True:
            h, t, o = rnd.randint(1, 4), rnd.randint(1, 7), rnd.randint(1, 9)
            n = 100 * h + 10 * t + o
            if len({h, t, o}) == 3 and n not in used:
                used.add(n)
                break
        wrong = [hto_text(h, o, t), hto_text(t, h, o), hto_text(o, t, h), hto_text(h, t + 1, o)]
        match.append(mcq(fig(blocks_svg(h, t, o)) + "Which matches the blocks?", hto_text(h, t, o), wrong,
                         "A big square is 1 hundred. A rod is 1 ten. A small cube is 1 one. "
                         "Count each kind: %s. The number is %d." % (hto_text(h, t, o), n), rnd))
    # place value counters (3)
    counters = []
    for z in (None, "t", "o"):
        while True:
            h, t, o = rnd.randint(1, 9), rnd.randint(1, 9), rnd.randint(1, 9)
            if z == "t":
                t = 0
            if z == "o":
                o = 0
            n = 100 * h + 10 * t + o
            if len({h, t, o}) == 3 and n not in used:
                used.add(n)
                break
        cands = [drop_zero(n), swap_to(n), as_heard(n)] + block_cands(h, t, o)
        counters.append(mcq_n(fig(counters_svg(n)) + "What number do the place value counters show?", n,
                              cands, count_e(h, t, o, "counters"), rnd))
    # value of the red digit (4)
    red = []
    for i in [1, 2, 1, 2]:
        n = distinct3(rnd, used)
        while digit(n, i) == 1:
            used.discard(n)
            n = distinct3(rnd, used)
        d = digit(n, i)
        red.append(mcq_n(fig(chart_svg(n, hi=i)) + "What is the value of the red digit?", d * 10 ** i,
                         value_cands(d, i), value_e(n, d, i, True), rnd))
    # value of a digit, no chart (3) — includes the 4 in 349
    val = []
    for n, i in [(349, 1), (None, 2), (None, 1)]:
        if n is None:
            n = distinct3(rnd, used)
        else:
            used.add(n)
        d = digit(n, i)
        val.append(mcq_n("What is the value of the digit %d in %d?" % (d, n), d * 10 ** i,
                         value_cands(d, i) + [n % (10 ** (i + 1))], value_e(n, d, i), rnd))
    # which digit is in a place (2)
    which = []
    for i in [1, 2]:
        n = distinct3(rnd, used)
        d = digit(n, i)
        e = ("%d has %s. The %s digit is %d."
             % (n, ", ".join(plural(digit(n, x), x) for x in (2, 1, 0)), PL[i], d))
        cands = [digit(n, x) for x in (0, 1, 2) if x != i] + [d * 10 ** i]
        which.append(mcq("In %d, which digit is in the %s place?" % (n, PL[i]), d, cands, e, rnd))
    order = (blocks[:2] + match[:1] + red[:2] + blocks[2:3] + counters[:1] + val[:1] + which[:1] + blocks[3:4]
             + match[1:] + counters[1:2] + red[2:3] + val[1:2] + blocks[4:5] + which[1:] + counters[2:]
             + red[3:] + blocks[5:] + val[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Hundreds, tens and ones", "items": order}


# ============================================================ set 2: numerals and words
def word_cands(n):
    return [words(v) for v in write_cands(n) if v and v != n]


def word_e(n):
    h, t, o = hto(n)
    parts = "%s, %s, %s" % (plural(h, 2), plural(t, 1), plural(o, 0))
    e = "%s is %s. Say the hundreds, then “and”, then the tens and ones: %s." % (n, parts, words(n))
    if t == 0 and o:
        e += " There are 0 tens, so we say nothing for the tens."
    if t == 1:
        e += " %d is “%s”, not “%s”." % (n % 100, ONES[n % 100], TENS[o]) if o >= 3 else ""
    return e


def set_words(rnd, used):
    its = []
    # words -> numerals (7): 3 with 0 tens, 1 with 0 ones, 1 teen, 2 others
    kinds = ["zt", "gen", "teen", "zt", "zo", "gen", "zt"]
    nums = []
    for k in kinds:
        while True:
            h = rnd.randint(1, 9)
            t = 0 if k == "zt" else (1 if k == "teen" else rnd.randint(2, 9))
            o = rnd.randint(1, 9) if k != "zo" else 0
            if k == "teen":
                o = rnd.randint(3, 9)
            if k == "zo":
                t = rnd.randint(3, 9)
            n = 100 * h + 10 * t + o
            if n not in used and len({h, t, o}) == 3:
                used.add(n)
                nums.append(n)
                break
    w2n = []
    for n in nums:
        h, t, o = hto(n)
        e = ("%s means %s: %s = %d." % (cap(words(n)), hto_text(h, t, o), expanded(n), n))
        if t == 0:
            e += " Write 0 in the tens place. 3-digit numbers have only 3 digits, so it is not %s." % c(as_heard(n))
        if o == 0:
            e += " Write 0 in the ones place."
        w2n.append(mcq_n("Write <b>%s</b> in numerals." % words(n), n, write_cands(n), e, rnd))
    # numerals -> words (7)
    kinds = ["gen", "zt", "teen", "zo", "gen", "zt", "teen"]
    nums = []
    for k in kinds:
        while True:
            h = rnd.randint(1, 9)
            t = 0 if k == "zt" else (1 if k == "teen" else rnd.randint(2, 9))
            o = rnd.randint(1, 9)
            if k == "teen":
                o = rnd.randint(3, 9)
            if k == "zo":
                t, o = rnd.randint(3, 9), 0
            n = 100 * h + 10 * t + o
            if n not in used and len({h, t, o}) == 3:
                used.add(n)
                nums.append(n)
                break
    n2w = [mcq("How do you write %d in words?" % n, words(n), word_cands(n), word_e(n), rnd) for n in nums]
    # expanded -> number (3)
    exp = []
    for q, n, wrong, e in [
            ("400 + 7", 407, [47, 470, 4007],
             "400 + 7 is 4 hundreds, 0 tens and 7 ones. Write 0 in the tens place: 407."),
            ("600 + 30", 630, [63, 603, 6030],
             "600 + 30 is 6 hundreds, 3 tens and 0 ones. Write 0 in the ones place: 630."),
            ("5 + 40 + 900", 945, [549, 954, 594],
             "The parts are not in order. Find the hundreds first: 900. Then the tens: 40. Then the ones: 5. "
             "900 + 40 + 5 = 945.")]:
        used.add(n)
        exp.append(mcq_n("What number is <b>%s</b>?" % q, n, wrong, e, rnd))
    # number -> partition (3)
    part = []
    for n, wrong in [(704, ["700 + 40", "70 + 4", "7 + 0 + 4"]),
                     (582, ["500 + 28", "5 + 8 + 2", "500 + 800 + 2"]),
                     (360, ["300 + 6", "3 + 6 + 0", "300 + 600"])]:
        used.add(n)
        h, t, o = hto(n)
        e = "%d has %s. Write the value of each digit that is not 0: %s." % (n, hto_text(h, t, o), expanded(n))
        part.append(mcq("Which shows %d partitioned into hundreds, tens and ones?" % n, expanded(n), wrong, e, rnd))
    order = (w2n[:2] + n2w[:2] + exp[:1] + w2n[2:3] + part[:1] + n2w[2:4] + w2n[3:4] + exp[1:2] + n2w[4:5]
             + w2n[4:5] + part[1:2] + n2w[5:6] + w2n[5:6] + exp[2:] + part[2:] + n2w[6:] + w2n[6:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Read and write numbers to 1,000 in numerals and words", "items": order}


# ============================================================ set 3: 10 or 100 more or less, counting in multiples
def set_more_less(rnd, used):
    its = []
    specs = [  # (step, kind, n, wrong, extra explanation)
        (10, "more", 347, [447, 348, 337], ""),
        (100, "more", 462, [472, 463, 362], ""),
        (10, "less", 586, [486, 585, 596], ""),
        (100, "less", 618, [608, 718, 617], ""),
        (10, "more", 295, [395, 296, 285],
         " 9 tens and 1 more ten make 10 tens = 1 hundred, so the hundreds digit goes up too."),
        (10, "less", 503, [403, 513, 502],
         " There are 0 tens, so take 1 ten from the hundreds: 5 hundreds → 4 hundreds and 9 tens."),
        (100, "less", 140, [130, 240, 41],
         " 1 hundred take away 1 hundred leaves 0 hundreds, so the answer has only 2 digits."),
        (100, "more", 900, [910, 800, 901],
         " 9 hundreds and 1 more hundred make 10 hundreds = 1 thousand."),
    ]
    ml = []
    for step, kind, n, wrong, extra in specs:
        sg = 1 if kind == "more" else -1
        ans = n + sg * step
        assert all(w != ans for w in wrong)
        place = "tens" if step == 10 else "hundreds"
        e = ("%d %s than %d: change the %s digit. %d %s %d = %s.%s"
             % (step, kind, n, place, n, "+" if sg > 0 else "−", step, c(ans), extra))
        if not extra:
            e = ("%d %s than %d: only the %s digit changes. %d %s %d = %s."
                 % (step, kind, n, place, n, "+" if sg > 0 else "−", step, c(ans)))
        ml.append(mcq_n("What is %d %s than %d?" % (step, kind, n), ans, wrong, e, rnd))
    rev = mcq_n("10 more than a number is 400. What is the number?", 390, [410, 300, 399],
                "Work backwards. The number is 10 less than 400. 400 − 10 = 390. Check: 390 + 10 = 400.", rnd)
    # sequences (8)
    seqs = [
        (4, "next", [20, 24, 28, 32], [34, 40, 33]),
        (50, "next", [150, 200, 250, 300], [310, 400, 305]),
        (8, "next", [24, 32, 40, 48], [52, 58, 54]),
        (100, "next", [340, 440, 540, 640], [650, 641, 840]),
        (4, "missing", [12, 16, None, 24, 28], [18, 22, 30]),
        (50, "back", [500, 450, 400, 350], [340, 250, 400]),
        (8, "missing", [40, 48, None, 64, 72], [52, 54, 58]),
        (100, "back", [920, 820, 720, 620], [610, 420, 619]),
    ]
    sq = []
    for s, kind, seq, wrong in seqs:
        if kind == "missing":
            k = seq.index(None)
            ans = seq[k - 1] + s
            assert seq[k + 1] == ans + s
            q = "Count in %ds: %s. What number goes in the box?" % (s, ", ".join("☐" if v is None else str(v) for v in seq))
            e = "The numbers go up by %d each time. %d + %d = %d. Check: %d + %d = %d." % (
                s, seq[k - 1], s, ans, ans, s, seq[k + 1])
        else:
            sg = 1 if kind == "next" else -1
            for a, b in zip(seq, seq[1:]):
                assert b - a == sg * s
            ans = seq[-1] + sg * s
            q = "%s: %s, ? What comes next?" % ("Count in %ds" % s if sg > 0 else "Count back in %ds" % s,
                                                 ", ".join(str(v) for v in seq))
            e = "Each number is %d %s than the one before. %d %s %d = %d." % (
                s, "more" if sg > 0 else "less", seq[-1], "+" if sg > 0 else "−", s, ans)
            if s == 100:
                e += " Only the hundreds digit changes."
        assert ans not in wrong
        sq.append(mcq_n(q, ans, wrong, e, rnd))
    # multiples (3)
    mult = []
    for s, ans, wrong, why in [
            (4, 28, [26, 18, 34], "7 × 4 = 28, so you say 28 when counting in 4s: 4, 8, 12, 16, 20, 24, 28. "
                                  "26, 18 and 34 are in the 2 times table, but not the 4 times table."),
            (8, 64, [54, 68, 58], "8 × 8 = 64. 68 is in the 4 times table but not the 8 times table. "
                                  "54 and 58 end in 4 and 8 but are not multiples of 8."),
            (50, 650, [605, 520, 675], "Counting in 50s always ends in 00 or 50: 550, 600, 650, 700. "
                                       "605, 520 and 675 do not end in 00 or 50.")]:
        assert ans % s == 0 and all(w % s for w in wrong)
        mult.append(mcq_n("Which number would you say when counting in %ds from 0?" % s, ans, wrong, why, rnd))
    order = (ml[:2] + sq[:2] + ml[2:4] + sq[2:4] + mult[:1] + ml[4:5] + sq[4:5] + ml[5:6] + sq[5:6]
             + mult[1:2] + ml[6:7] + sq[6:7] + [rev] + ml[7:] + sq[7:] + mult[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "10 or 100 more or less, and counting in 4s, 8s, 50s and 100s", "items": order}


# ============================================================ set 4: compare, order and estimate
def first_diff(a, b):
    for i in range(2, -1, -1):
        if digit(a, i) != digit(b, i):
            return i


def compare_expl(big, small):
    if len(str(big)) != len(str(small)):
        return "%s has %d digits and %s has only %d, so %s is greater." % (
            c(big), len(str(big)), c(small), len(str(small)), c(big))
    i = first_diff(big, small)
    same = "The digits are the same until the %s" % PL[i] if i < 2 else "Start with the hundreds"
    return ("Compare from the left. %s: %s is more than %s. So %d &gt; %d."
            % (same, plural(digit(big, i), i), plural(digit(small, i), i), big, small))


def set_compare(rnd, used):
    its = []
    # which is true (4)
    tru = []
    for x, y in [(352, 325), (419, 501), (99, 120), (735, 753)]:
        sym = "&lt;" if x < y else "&gt;"
        anti = "&gt;" if x < y else "&lt;"
        right = "%d %s %d" % (x, sym, y)
        wrong = ["%d %s %d" % (x, anti, y), "%d = %d" % (x, y), "%d %s %d" % (y, sym, x)]
        e = compare_expl(max(x, y), min(x, y))
        if x == 419:
            e += " Do not look at the last digit first: 9 ones is less than 1 hundred."
        if x == 99:
            e += " Big digits (9 and 9) do not matter when there are fewer digits."
        tru.append(mcq("Which is true?", right, wrong, e, rnd))
    # greatest / smallest (6)
    gs = []
    for want, nums, extra in [
            ("greatest", [472, 427, 742, 724], ""),
            ("smallest", [563, 536, 356, 365], ""),
            ("greatest", [99, 101, 110, 100], " 99 has big digits, but it has only 2 digits, so it is the smallest."),
            ("smallest", [807, 870, 780, 708], ""),
            ("greatest", [608, 680, 806, 860], ""),
            ("smallest", [401, 389, 410, 398], " Do not compare the last digits: 401 ends in 1, but it has 4 hundreds."),
    ]:
        o = sorted(nums)
        ans, nxt = (o[-1], o[-2]) if want == "greatest" else (o[0], o[1])
        e = (compare_expl(ans, nxt) if want == "greatest" else compare_expl(nxt, ans)) + \
            " %d is the %s.%s" % (ans, want, extra)
        gs.append(mcq("Which number is the %s?" % want, str(ans), [str(v) for v in nums if v != ans], e, rnd))
    # order (3)
    od = []
    fmt = lambda l: ", ".join(str(v) for v in l)
    for three, up in [([504, 450, 540], True), ([263, 326, 236], True), ([718, 178, 781], False)]:
        o = sorted(three) if up else sorted(three, reverse=True)
        perms = [[o[0], o[2], o[1]], [o[1], o[0], o[2]], o[::-1], [o[2], o[0], o[1]]]
        s = sorted(three)
        i1, i2 = first_diff(s[1], s[0]), first_diff(s[2], s[1])
        e = ("Compare from the left. %d &lt; %d (%s: %d &lt; %d). %d &lt; %d (%s: %d &lt; %d). So the order is %s."
             % (s[0], s[1], PL[i1], digit(s[0], i1), digit(s[1], i1),
                s[1], s[2], PL[i2], digit(s[1], i2), digit(s[2], i2), fmt(o)))
        od.append(mcq("Put %s in order from %s." % (fmt(three), "smallest to greatest" if up else "greatest to smallest"),
                      fmt(o), [fmt(p) for p in perms], e, rnd))
    # number between (2)
    btw = []
    for lo, hi, ans, wrong in [(450, 500, 486, [405, 540, 504]), (700, 800, 790, [690, 870, 807])]:
        assert lo < ans < hi and all(not lo < w < hi for w in wrong)
        e = "A number between %d and %d is greater than %d and less than %d. %d &gt; %d and %d &lt; %d, so %d is between them." % (
            lo, hi, lo, hi, ans, lo, ans, hi, ans)
        btw.append(mcq_n("Which number is between %d and %d?" % (lo, hi), ans, wrong, e, rnd))
    # number lines 0 to 1,000 (3)
    nl = []
    for v, kind, wrong in [(300, "read", [400, 700, 30]), (700, "read", [600, 300, 70]), (850, "est", [750, 150, 805])]:
        if kind == "read":
            q = fig(number_line_svg(0, 1000, 100, [0, 500, 1000], v)) + "What number does the arrow point to?"
            e = ("From 0 to 1,000 there are 10 jumps, so each mark is 100. Count the marks from 0: %s. The arrow shows %d."
                 % (", ".join(str(100 * k) for k in range(1, v // 100 + 1)), v))
        else:
            q = fig(number_line_svg(0, 1000, 100, [0, 500, 1000], v)) + "Estimate the number the arrow points to."
            e = ("Each mark is 100. The arrow is halfway between 800 and 900. Halfway between them is 850.")
        nl.append(mcq_n(q, v, wrong, e, rnd))
    # number lines with tens (2)
    nt = []
    for lo, v in [(400, 430), (700, 760)]:
        k = (v - lo) // 10
        wrong = [lo + k, lo + 100 - k * 10, v + 10]
        e = ("From %d to %d there are 10 jumps, so each mark is 10, not 1. The arrow is %d marks after %d: %d + %d = %d."
             % (lo, lo + 100, k, lo, lo, k * 10, v))
        q = fig(number_line_svg(lo, lo + 100, 10, [lo, lo + 50, lo + 100], v)) + "What number does the arrow point to?"
        nt.append(mcq_n(q, v, wrong, e, rnd))
    order = (tru[:2] + gs[:2] + nl[:1] + tru[2:3] + gs[2:3] + od[:1] + nl[1:2] + btw[:1] + gs[3:4] + tru[3:]
             + nt[:1] + od[1:2] + gs[4:5] + nl[2:] + btw[1:] + nt[1:] + gs[5:] + od[2:])
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare, order and estimate numbers to 1,000", "items": order}


# ============================================================ set 5: word problems
def set_problems(rnd, P):
    its = []
    name, she, her = P.next()
    its.append(mcq_n("%s's book has three hundred and eight pages. How do you write this number in numerals?" % name,
                     308, [3008, 38, 380],
                     "Three hundred and eight is 3 hundreds, 0 tens and 8 ones. Write 0 in the tens place: 308.", rnd))
    name, he, his = P.next()
    its.append(mcq_n("Stickers come in packs of 100, strips of 10 and single stickers. %s has 4 packs, 6 strips and "
                     "3 single stickers. How many stickers does %s have?" % (name, he), 463, [436, 643, 13],
                     "4 packs = 400. 6 strips = 60. 3 singles = 3. 400 + 60 + 3 = 463.", rnd))
    its.append(mcq_n("The school kitchen cooked 245 school dinners on Monday. On Tuesday it cooked 10 more. "
                     "How many dinners did it cook on Tuesday?", 255, [345, 246, 235],
                     "10 more: only the tens digit changes. 4 tens → 5 tens. 245 + 10 = 255.", rnd))
    its.append(mcq_n("Pencils come in boxes of 100. The school has 7 full boxes and 5 more pencils. "
                     "How many pencils is that?", 705, [75, 7005, 750],
                     "7 boxes of 100 = 700. Add 5: 700 + 5 = 705. There are 0 tens, so write 0 in the tens place.", rnd))
    its.append(mcq_n("The school library has 590 books. It buys 10 new books. How many books does it have now?", 600,
                     [690, 591, 580],
                     "9 tens + 1 ten = 10 tens = 1 hundred. So 5 hundreds become 6 hundreds and there are 0 tens: "
                     "590 + 10 = 600.", rnd))
    its.append(mcq_n("A farmer has 832 sheep. She sells 100 of them. How many sheep are left?", 732, [822, 932, 831],
                     "100 less: only the hundreds digit changes. 8 hundreds → 7 hundreds. 832 − 100 = 732.", rnd))
    rd = [(P.next(), v) for v in [389, 398, 419, 401]]
    best = max(rd, key=lambda w: w[1])
    its.append(mcq("Four children counted the pages they read this term. %s. Who read the most pages?"
                   % "; ".join("%s: %d" % (p[0], v) for p, v in rd), best[0][0],
                   [p[0] for p, v in rd if v != best[1]],
                   "Compare the hundreds first. 419 and 401 have 4 hundreds; 389 and 398 have only 3. "
                   "Then the tens: 1 ten &gt; 0 tens, so 419 is the greatest. %s read the most. "
                   "Do not just look at the last digit." % best[0][0], rnd))
    cls = [("Class 3A", 506), ("Class 3B", 560), ("Class 3C", 650), ("Class 3D", 605)]
    its.append(mcq("Four classes collected bottle tops for recycling. %s. Which class collected the fewest?"
                   % "; ".join("%s: %d" % (n, v) for n, v in cls), "Class 3A", ["Class 3B", "Class 3C", "Class 3D"],
                   "Compare the hundreds: 506 and 560 have 5 hundreds. Then the tens: 0 tens &lt; 6 tens, "
                   "so 506 is the smallest. Class 3A collected the fewest.", rnd))
    its.append(mcq_n("A train has 8 carriages. Each carriage has 50 seats. How many seats are there?", 400,
                     [350, 450, 58],
                     "Count in 50s eight times: 50, 100, 150, 200, 250, 300, 350, 400. There are 400 seats.", rnd))
    its.append(mcq_n("Each table in the classroom has 4 chairs. There are 9 tables. How many chairs are there?", 36,
                     [32, 40, 13], "Count in 4s nine times: 4, 8, 12, 16, 20, 24, 28, 32, 36. 9 × 4 = 36 chairs.", rnd))
    its.append(mcq_n("A spider has 8 legs. How many legs do 6 spiders have?", 48, [40, 56, 14],
                     "Count in 8s six times: 8, 16, 24, 32, 40, 48. 6 × 8 = 48 legs.", rnd))
    name, she, her = P.next()
    its.append(mcq_n("Raffle tickets for the school fair come in books of 100. %s sells 6 books. "
                     "How many tickets does %s sell?" % (name, she), 600, [60, 700, 106],
                     "Count in 100s six times: 100, 200, 300, 400, 500, 600. %s sells 600 tickets." % name, rnd))
    name, he, his = P.next()
    its.append(mcq_n(fig(number_line_svg(0, 1000, 100, [0, 500, 1000], 600)) +
                     "A sponsored walk is 1,000 m long. The arrow shows where %s is. How far has %s walked?" % (name, he),
                     600, [400, 700, 60],
                     "Each mark is 100 m. The arrow is 1 mark after 500: 500 + 100 = 600 m.", rnd, unit=" m"))
    name, she, her = P.next()
    its.append(mcq_n("%s thinks of a number. It has 5 hundreds, 0 tens and 9 ones. What is %s number?" % (name, her),
                     509, [59, 590, 5009],
                     "Write the digits in order: 5 hundreds, 0 tens, 9 ones → 509. The 0 keeps the 5 in the hundreds place.",
                     rnd))
    its.append(mcq_n("There are 486 children at Oak Tree Primary School. What is the value of the 8 in 486?", 80,
                     [8, 800, 86], "The 8 is in the tens place, so it is worth 8 tens = 80.", rnd))
    its.append(mcq_n("Use the digits 7, 2 and 5 once each. What is the greatest number you can make?", 752,
                     [725, 572, 257],
                     "Put the biggest digit in the hundreds place, then the next biggest: 7, 5, 2. The greatest number is 752.",
                     rnd))
    its.append(mcq("Use the digits 0, 4 and 9 once each. What is the smallest 3-digit number you can make?", "409",
                   ["49", "490", "904"],
                   "0 cannot go in the hundreds place, or it would be a 2-digit number. Use the next smallest digit, 4. "
                   "Then put 0 in the tens and 9 in the ones: 409.", rnd))
    name, she, her = P.next()
    name2, he2, his2 = P.next()
    its.append(mcq_n("%s scores 380 points in a game. %s scores 100 points fewer. How many points does %s score?"
                     % (name, name2, name2), 280, [370, 480, 290],
                     "100 fewer: only the hundreds digit changes. 3 hundreds → 2 hundreds. 380 − 100 = 280.", rnd))
    its.append(mcq_n("There are 310 chairs in the school hall. 10 chairs are taken away to be mended. "
                     "How many chairs are left?", 300, [210, 309, 320],
                     "10 less: 1 ten → 0 tens. 310 − 10 = 300. The hundreds stay the same.", rnd))
    name, he, his = P.next()
    its.append(mcq_n("%s counts in 4s from 0: 4, 8, 12, … What is the 10th number %s says?" % (name, he), 40,
                     [36, 44, 14],
                     "The 10th number is 10 × 4 = 40. Count: 4, 8, 12, 16, 20, 24, 28, 32, 36, 40.", rnd))
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
        "<h2>Hundreds, tens and ones</h2>"
        "<p>A 3-digit number has a <b>hundreds</b> digit, a <b>tens</b> digit and a <b>ones</b> digit. "
        "The place tells you what the digit is worth. 10 ones make 1 ten. <b>10 tens make 1 hundred.</b></p>"
        "<figure class='sn-fig'>" + blocks_svg(2, 4, 3, labels=True) +
        "<figcaption>A big square is 1 hundred. A rod is 1 ten. A small cube is 1 one. "
        "2 hundreds, 4 tens and 3 ones make 243.</figcaption></figure>"
        "<figure class='sn-fig'>" + chart_svg(349, hi=1) +
        "<figcaption>In 349 the 4 is in the tens place. Its value is 4 tens, or 40.</figcaption></figure>"
        "<figure class='sn-fig'>" + counters_svg(306) +
        "<figcaption>Place value counters for 306: 3 hundreds, 0 tens and 6 ones. "
        "There are no tens, so the tens digit is 0.</figcaption></figure>"
        "<h2>Numerals and words</h2>" +
        table(["Numeral", "Words", "Partitioned"], [
            ["243", "two hundred and forty-three", "200 + 40 + 3"],
            ["306", "three hundred and six", "300 + 6"],
            ["415", "four hundred and fifteen", "400 + 10 + 5"],
            ["750", "seven hundred and fifty", "700 + 50"],
            ["1,000", "one thousand", "10 hundreds"],
        ]) +
        "<p>Say “and” after the hundreds. Use a hyphen for numbers like forty-three.</p>" +
        ex("Write in numerals", "Write “three hundred and six” in numerals.",
           "3 hundreds, 0 tens, 6 ones. Write 3, 0, 6.", "306 (not 3006 or 36)") +
        "<h2>10 or 100 more or less</h2>"
        "<p>For 10 more or less, change the <b>tens</b> digit. For 100 more or less, change the <b>hundreds</b> digit.</p>" +
        table(["100 less", "10 less", "Number", "10 more", "100 more"], [
            ["247", "337", "347", "357", "447"],
            ["195", "285", "295", "305", "395"],
        ]) +
        "<p>Watch out at 9 tens: 295 + 10 = 305, because 10 tens make 1 hundred.</p>"
        "<h2>Counting in 4s, 8s, 50s and 100s</h2>" +
        table(["Count in", "Numbers"], [
            ["4s", "4, 8, 12, 16, 20, 24, 28, 32, 36, 40"],
            ["8s", "8, 16, 24, 32, 40, 48, 56, 64, 72, 80"],
            ["50s", "50, 100, 150, 200, 250, 300, 350, 400"],
            ["100s", "100, 200, 300, 400, 500, 600, 700"],
        ]) +
        "<p>The 8s are double the 4s. Counting in 50s always ends in 00 or 50.</p>"
        "<h2>Compare and order</h2>"
        "<p>First count the digits: a 3-digit number is greater than any 2-digit number. If both have 3 digits, "
        "compare the hundreds, then the tens, then the ones.</p>" +
        ex("Compare", "419 ☐ 501",
           "Hundreds: 4 &lt; 5. You can stop here. The 9 ones do not matter.", "419 &lt; 501") +
        "<p>&lt; means “is less than”. &gt; means “is greater than”. The open side faces the bigger number.</p>"
        "<h2>Estimate on a number line</h2>"
        "<figure class='sn-fig'>" + number_line_svg(0, 1000, 100, [0, 500, 1000], 850, show="about 850") +
        "<figcaption>Each mark is 100. The arrow is halfway between 800 and 900, so it shows about 850.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing “three hundred and six” as 3006 or 36", "Use 3 digits with 0 tens: 306"],
            ["Giving the digit, not its value (the 4 in 349 is 4)", "The 4 is in the tens place: 40"],
            ["Changing the wrong digit (295 + 10 = 395)", "10 more changes the tens: 305"],
            ["Comparing the last digits (419 &gt; 501 because 9 &gt; 1)", "Compare the hundreds first: 419 &lt; 501"],
            ["Mixing up fifteen and fifty (415 and 450)", "Fifteen is 1 ten, 5 ones: 415"],
        ])
    )


FAQ = [
    {"q": "What place value should a Year 3 child know?",
     "a": "Year 3 children work with numbers up to 1,000. They know the value of each digit in a 3-digit number, read and write numbers in numerals and words, find 10 or 100 more or less, count in 4s, 8s, 50s and 100s, and compare and order numbers."},
    {"q": "How do you write numbers in words in Year 3?",
     "a": "Say the hundreds, then “and”, then the tens and ones, for example 243 is two hundred and forty-three and 306 is three hundred and six. Numbers from 21 to 99 use a hyphen, like forty-three."},
    {"q": "How do you find 10 or 100 more or less than a number?",
     "a": "For 10 more or less, change the tens digit by 1; for 100 more or less, change the hundreds digit by 1. Take care at 9 tens: 10 more than 295 is 305."},
    {"q": "Why does my child write 3006 for three hundred and six?",
     "a": "They write each part they hear: 300 and then 6. Show that three hundred and six is 3 hundreds, 0 tens and 6 ones, so it has only 3 digits: 306."},
]


def mark_large(u, pattern):
    """Tag wide pictures (blocks, counters, charts, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(3301)
    P = People(rnd)
    used = set()
    sets = [set_hto(rnd, used), set_words(rnd, used), set_more_less(rnd, used),
            set_compare(rnd, used), set_problems(rnd, P)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
    u = {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "place-value", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Place Value to 1,000: Hundreds, Tens and Ones, 10 or 100 More or Less",
        "seo_title": "Year 3 Place Value Worksheets: Hundreds, Tens and Ones, Numbers to 1,000 in Words",
        "short_title": "Place value",
        "domain": "Number and place value",
        "standard_code": "Year 3: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count from 0 in multiples of 4, 8, 50 and 100; find 10 or 100 more or less than a given number; recognise the place value of each digit in a three-digit number (hundreds, tens, ones); compare and order numbers up to 1,000; identify, represent and estimate numbers using different representations; read and write numbers up to 1,000 in numerals and in words.",
        "meta_desc": "Free Year 3 place value maths worksheets for the National Curriculum: hundreds, tens and ones with base-ten blocks and place value counters, numbers to 1,000 in numerals and words, 10 or 100 more or less, counting in 4s, 8s, 50s and 100s, and comparing and ordering. 100 questions with an answer key.",
        "key_big": "A 3-digit number is hundreds, tens and ones. The place of a digit decides its value.",
        "key_sub": "The 4 in 349 is worth 40. Three hundred and six is 306: write 0 when there are no tens. For 10 more or less change the tens digit; for 100 more or less change the hundreds digit.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(base-ten blocks|place value chart|place value counters|number line)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
