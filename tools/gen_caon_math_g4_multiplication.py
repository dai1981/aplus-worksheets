# -*- coding: utf-8 -*-
"""
CA-ON Grade 4 Math: Multiplying by one-digit numbers
(Ontario Mathematics Curriculum 2020, Grade 4, B2.5 and B2.3: multiply two- or three-digit numbers
 by one-digit numbers and by 10, 100 and 1000, using tools including arrays; mental math)
x 10, 100, 1000; base ten blocks, area models and partial products; the standard method for
3-digit x 1-digit; estimate first; Ontario word problems.
  python3 tools/gen_caon_math_g4_multiplication.py
HTML attributes use single quotes (no backslashes in the JSON). Every answer is computed in code.
Ontario style: Canadian English, metric, $ (whole dollars here), 4-digit numbers without a separator.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
GREY = "#6b6259"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
NBSP = " "


# ------------------------------------------------------------ helpers
def f(n):
    """Ontario style: 4536, 10 000 (no-break space only from 5 digits)."""
    s = str(n)
    if abs(n) < 10000:
        return s
    return "{:,}".format(n).replace(",", NBSP)


def qr(q, r):
    return "%s R %d" % (f(q), r) if r else f(q)


def mcq(q, correct, cands, e, zero_ok=False):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or (lead == "0" and not zero_ok):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def tw(t, fs, bold=True):
    return len(str(t)) * fs * (0.6 if bold else 0.56)


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def parts(n):
    """236 -> [200, 30, 6] (zeros left out)."""
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


def unit_word(k, i):
    w = PLACE[i]
    return "%s %s" % (f(k), w[:-1] if k == 1 else w)


def carry_list(a, d):
    """Regrouped digit going INTO each column (index = column from the right)."""
    c, out = 0, {}
    for i, x in enumerate(digits(a)):
        p = x * d + c
        c = p // 10
        if c and i < len(digits(a)) - 1:
            out[i + 1] = c
    return out


# ------------------------------------------------------------ typical multiplication mistakes
def mult_wrong(a, d, skip=None, carry_first=False):
    """skip=None: forget every regrouped digit; skip=k: forget the one made in column k.
    carry_first: add the regrouped digit BEFORE multiplying."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        p = (x + c) * d if carry_first else x * d + c
        if i == len(ds) - 1:
            r += p * 10 ** i
        else:
            r += (p % 10) * 10 ** i
            c = p // 10
            if not carry_first and (skip is None or skip == i):
                c = 0
    return r


def only_ones(a, d):
    """Multiplying only the ones: 23 × 4 -> 20 + 12 = 32."""
    return a - a % 10 + (a % 10) * d


def concat(a, d):
    """Writing each column's product side by side: 23 × 4 -> 8 | 12 -> 812."""
    return int("".join(str(x * d) for x in reversed(digits(a))))


def tens_as_ones(a, d):
    """20 × 4 = 8: every part treated as ones."""
    return sum(x * d for x in digits(a))


def cands_mult(a, d):
    ds = digits(a)
    out = [mult_wrong(a, d), only_ones(a, d), mult_wrong(a, d, carry_first=True)]
    out += [mult_wrong(a, d, skip=k) for k in range(len(ds) - 1)]
    out += [concat(a, d), tens_as_ones(a, d), a * (d - 1), a + d, a * (d + 1)]
    return out


def steps_std(a, d):
    """The standard method, column by column."""
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d = %d" % (x, d, x * d) + (", plus %d = %d" % (c, p) if c else "")
        last = i == len(ds) - 1
        if last or p < 10:
            out.append("%s: %s. Write %d." % (cap(PLACE[i]), ex_, p))
        else:
            out.append("%s: %s. Write %d, regroup %s." % (cap(PLACE[i]), ex_, p % 10, unit_word(p // 10, i + 1)))
        c = p // 10
    return " ".join(out) + " Answer: %s." % f(a * d)


def steps_pp(a, d):
    ps = parts(a)
    return ("Split %s into %s. Multiply each part: %s. Add: %s = %s." %
            (f(a), " + ".join(f(p) for p in ps),
             ", ".join("%s × %d = %s" % (f(p), d, f(p * d)) for p in ps),
             " + ".join(f(p * d) for p in ps), f(a * d)))



# ------------------------------------------------------------ figures
S = 8                      # size of one unit cube


def blocks(h, t, o, x, y):
    """Base ten blocks: flats, rods, units (units in columns of 5). Returns (svg, width, height)."""
    s = []
    cx = x
    big = 10 * S
    for _ in range(h):
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, y, big, big, FILL, GREEN))
        for k in range(1, 10):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>" % (cx + k * S, y, cx + k * S, y + big, GREEN))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>" % (cx, y + k * S, cx + big, y + k * S, GREEN))
        cx += big + 5
    for _ in range(t):
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, y, S, big, FILL, GREEN))
        for k in range(1, 10):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>" % (cx, y + k * S, cx + S, y + k * S, GREEN))
        cx += S + 4
    hh = big if (h or t) else 0
    ncol = (o + 4) // 5
    for k in range(o):
        col, row = divmod(k, 5)
        uy = y + (hh - (row + 1) * (S + 2) if hh else row * (S + 2))
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx + col * (S + 3), uy, S, S, FILL, GREEN))
    w = cx - x + ncol * (S + 3) - (4 if ncol == 0 and (h or t) else 0)
    hgt = hh or min(o, 5) * (S + 2)
    return "".join(s), w, hgt


def groups_svg(a, d, label=None):
    """d equal groups of base ten blocks, each in a dashed box."""
    t, o = divmod(a, 10)
    pad = 7
    s = []
    x = 3
    H = 0
    for g in range(d):
        body, w, h = blocks(0, t, o, x + pad, 3 + pad)
        s.append("<rect x='%.1f' y='3' width='%.1f' height='%d' rx='8' fill='none' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                 % (x, w + 2 * pad, h + 2 * pad, GREY))
        s.append(body)
        x += w + 2 * pad + 8
        H = h + 2 * pad + 6
    return svg_wrap(int(x - 5), int(H), "".join(s), label or "%d groups of %d in base ten blocks" % (d, a))


def area_svg(side, tops, inside, label, wsum=250):
    """Area model: a rectangle split into parts. tops = labels above each part,
    inside = text inside each part ('?' = red), side = label on the left."""
    FS = 18
    vals = [int(t) if str(t).isdigit() else 1 for t in tops]
    tot = float(sum(vals))
    ws = [max(56, tw(tops[k], FS) + 18, tw(inside[k], FS) + 18, wsum * vals[k] / tot) for k in range(len(tops))]
    x0, y0, h = 34, 30, 62
    s = []
    x = x0
    for k, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y0, w, h, FILL, GREEN))
        t = inside[k]
        if t:
            s.append(text(x + w / 2, y0 + h / 2 + 6, t, FS, col=RED if t == "?" else INK))
        s.append(text(x + w / 2, y0 - 9, tops[k], FS, col=RED if tops[k] == "?" else GREEN))
        x += w
    s.append(text(x0 - 15, y0 + h / 2 + 6, str(side), FS, col=GREEN))
    return svg_wrap(int(x + 4), y0 + h + 4, "".join(s), label)


def std_svg(a, d, ans="", ex=None, label=None):
    """Standard method in columns. ans: ' ' = blank, '?' = red dashed box.
    ex: {column from the right: regrouped digit}, written small ABOVE the top number."""
    fs = 26
    cw = fs * 0.95
    a_s = str(a)
    nd = max(len(a_s), len(ans))
    slots = nd + 1
    W = int(cw * slots + 16)
    right = W - 8
    gap = fs * 1.22
    s = []

    def col_x(i):
        return right - cw * (i + 0.5)

    def row(t, y, col=INK):
        for i, ch in enumerate(reversed(t)):
            if ch == " ":
                continue
            if ch == "?":
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' "
                         "stroke-width='2' stroke-dasharray='4 3'/>" % (col_x(i) - cw * 0.42, y - fs * 0.98, cw * 0.84, fs * 1.14, RED))
                s.append(text(col_x(i), y - 2, "?", fs, col=RED))
            else:
                s.append(text(col_x(i), y - 2, ch, fs, col=col))

    y = 6
    if ex:
        y += 16
        for i, v in ex.items():
            s.append(text(col_x(i), y, str(v), 16, col=GREEN))
        y += 4
    y += fs
    row(a_s, y)
    y += gap
    row(str(d), y)
    s.append(text(col_x(nd), y - 2, "×", fs, col=GREEN))
    y += 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (right - cw * slots, y, right, y, INK))
    if ans:
        y += fs + 6
        row(ans, y)
    H = int(y + 10)
    return svg_wrap(W, H, "".join(s), label or "%d times %d written in columns" % (a, d), font="monospace")


def pp_svg(a, d, show=None, total=None, label=None):
    """Partial products in columns, with a note (in words) beside each row.
    show: list of texts for each partial product row (smallest place first); '?' = red box."""
    ps = list(reversed(parts(a)))                    # ones first
    show = show or [f(p * d) for p in ps]
    fs = 24
    cw = fs * 0.62
    nd = max(len(str(a * d)), len(str(a)) + 1)
    numw = cw * (nd + 1) + 8
    notes = ["%d × %s" % (d, f(p)) for p in ps]
    nfs = 15
    W = int(numw + 18 + max(tw(n, nfs, False) for n in notes) + 6)
    right = numw
    s = []

    def put(t, y, col=INK):
        if t == "?":
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' stroke-width='2' "
                     "stroke-dasharray='4 3'/>" % (right - cw * 3.4, y - fs * 0.95, cw * 3.4, fs * 1.15, RED))
            s.append(text(right - cw * 1.7, y - 2, "?", fs, col=RED))
        else:
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end' "
                     "font-family='monospace'>%s</text>" % (right, y - 2, fs, col, t))

    y = 6 + fs
    put(str(a), y)
    y += fs * 1.2
    put(str(d), y)
    s.append(text(right - cw * nd, y - 2, "×", fs, col=GREEN))
    y += 8
    s.append("<line x1='4' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (y, right + 4, y, INK))
    for t, n in zip(show, notes):
        y += fs * 1.2
        put(t, y, GREEN if t != "?" else RED)
        s.append(text(right + 18, y - 3, n, nfs, anchor="start", bold=False, col=GREY))
    if total is not None:
        y += 8
        s.append("<line x1='4' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (y, right + 4, y, INK))
        y += fs * 1.2
        put(total, y)
    return svg_wrap(W, int(y + 8), "".join(s), label or "%d times %d with partial products" % (a, d))



def pick_2x1(rnd, seen, lo=12, hi=98, regroup=True, dmax=9):
    while True:
        a, d = rnd.randint(lo, hi), rnd.randint(3, dmax)
        if a % 10 == 0 or (a, d) in seen or a // 10 == a % 10:
            continue
        if regroup and (a % 10) * d < 10:
            continue
        seen.add((a, d))
        return a, d


def area_1(a, d, inside=None, label=None):
    ps = parts(a)
    return area_svg(d, [f(p) for p in ps], inside or [""] * len(ps),
                    label or "area model with %d parts for %d times %d" % (len(ps), a, d))


def pv_svg(a, m, hide=True, label=None):
    """Place value chart (Th H T O): a on top, a × m below, arrows show each digit moving left."""
    k = len(str(m)) - 1
    p = a * m
    CW, L = 50, 74
    heads = ["Th", "H", "T", "O"]
    s = []
    y_h, y1, y2, rh = 4, 30, 30 + 40 + 18 + 26 * k, 40

    def cx(i):                     # i = column from the right (0 = ones)
        return L + CW * (3 - i) + CW / 2

    for j, hname in enumerate(heads):
        x = L + CW * j
        s.append("<rect x='%d' y='%d' width='%d' height='26' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y_h, CW, FILL, GREEN))
        s.append(text(x + CW / 2, y_h + 19, hname, 16, col=GREEN))
        for yy in (y1, y2):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='white' stroke='%s' stroke-width='1.5'/>" % (x, yy, CW, rh, GREEN))
    for i, dgt in enumerate(digits(a)):
        s.append(text(cx(i), y1 + 28, str(dgt), 22))
        x1, x2 = cx(i), cx(i + k)
        ya, yb = y1 + rh + 5, y2 - 5
        ang = math.atan2(yb - ya, x2 - x1)
        lx, ly = x2 - 9 * math.cos(ang), yb - 9 * math.sin(ang)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x1, ya, lx, ly, GREY))
        p1 = (x2 - 11 * math.cos(ang - 0.42), yb - 11 * math.sin(ang - 0.42))
        p2 = (x2 - 11 * math.cos(ang + 0.42), yb - 11 * math.sin(ang + 0.42))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x2, yb, p1[0], p1[1], p2[0], p2[1], GREY))
    for i, dgt in enumerate(digits(p)):
        if hide:
            s.append(text(cx(i), y2 + 28, "?", 22, col=RED))
        else:
            s.append(text(cx(i), y2 + 28, str(dgt), 22, col=GREEN if i < k else INK))
    s.append(text(L / 2, y1 + 28, f(a), 18, col=INK))
    s.append(text(L / 2, y2 + 28, "× %s" % f(m), 18, col=GREEN))
    return svg_wrap(L + 4 * CW + 4, y2 + rh + 4, "".join(s), label or "place value chart for %d times %d" % (a, m))


# ------------------------------------------------------------ set 1: x 10, 100, 1000
UNIT = {10: "tens", 100: "hundreds", 1000: "thousands"}
PLACES = {10: "one place", 100: "two places", 1000: "three places"}
ZEROS = {10: "one zero", 100: "two zeros", 1000: "three zeros"}


def cands_pow(a, m):
    p = a * m
    return [p * 10, p // 10, a + m, p * 100]


def e_pow(a, m):
    p = a * m
    e = ("%s × %s = %s %s = %s. Each digit moves %s to the left, so write %s after %s."
         % (f(a), f(m), f(a), UNIT[m], f(p), PLACES[m], ZEROS[m], f(a)))
    if a % 10 == 0:
        e += " The zero already in %s stays. Do not add extra zeros: the answer is %s, not %s." % (f(a), f(p), f(p * 10))
    return e


def set_pow(rnd):
    its, seen = [], set()

    def pick(lo, hi, m, nozero=True, endzero=False):
        while True:
            a = rnd.randint(lo, hi)
            if endzero != (a % 10 == 0) or (a, m) in seen or a * m > 9999:
                continue
            if nozero and not endzero and "0" in str(a):
                continue
            if len(set(str(a))) < len(str(a)):
                continue
            seen.add((a, m))
            return a

    # place value charts
    for lo, hi, m in [(12, 98, 10), (102, 987, 10), (12, 98, 100)]:
        a = pick(lo, hi, m)
        its.append(mcq(fig(pv_svg(a, m)) + "The chart shows how the digits of %s move when you multiply by %s. What is %s × %s?"
                       % (f(a), f(m), f(a), f(m)), f(a * m), [f(v) for v in cands_pow(a, m)], e_pow(a, m)))
    # plain
    for lo, hi, m in [(12, 98, 10), (12, 98, 10), (102, 987, 10), (102, 987, 10), (2, 9, 100), (12, 98, 100), (12, 98, 100),
                      (2, 9, 1000), (2, 9, 1000)]:
        a = pick(lo, hi, m)
        q = "What is %s × %s?" % (f(a), f(m)) if rnd.random() < 0.6 else "What is %s × %s?" % (f(m), f(a))
        its.append(mcq(q, f(a * m), [f(v) for v in cands_pow(a, m)], e_pow(a, m)))
    # numbers that already end in zero
    for lo, hi, m in [(20, 90, 10), (20, 90, 100), (110, 980, 10)]:
        a = pick(lo, hi, m, endzero=True)
        its.append(mcq("What is %s × %s?" % (f(a), f(m)), f(a * m), [f(v) for v in cands_pow(a, m)], e_pow(a, m)))
    # missing first factor
    for m in (10, 100):
        a = pick(12, 98, m)
        p = a * m
        its.append(mcq("What number goes in the box?  <b>☐ × %s = %s</b>" % (f(m), f(p)), f(a),
                       [f(p), f(p * 10), f(p - m), f(a * 10)],
                       "Think: which number has %s added to make %s? Take %s off the end of %s: %s. Check: %s × %s = %s."
                       % (ZEROS[m], f(p), ZEROS[m], f(p), f(a), f(a), f(m), f(p))))
    a = pick(2, 9, 1000)
    its.append(mcq("What number goes in the box?  <b>%d × ☐ = %s</b>" % (a, f(a * 1000)), "1000", ["10", "100", f(10000)],
                   "%s has three zeros after the %d. Multiplying by 1000 adds three zeros, so the box is 1000. Check: %d × 1000 = %s = %d thousands."
                   % (f(a * 1000), a, a, f(a * 1000), a)))
    # what it means
    its.append(mcq("Which is the same as 56 × 10?", "56 tens", ["56 hundreds", "56 ones", "66"],
                   "× 10 turns every one into a ten, so 56 × 10 = 56 tens = 560. (56 hundreds = 5600, and 66 is 56 + 10.)"))
    its.append(mcq("Which is the same as 8 × 100?", "8 hundreds", ["8 tens", "8 thousands", "108"],
                   "8 groups of 100 = 8 hundreds = 800. (8 thousands = 8000, and 108 is 8 + 100.)"))
    return {"title": "Multiply by 10, 100 and 1000", "items": its}


# ------------------------------------------------------------ set 2: 2-digit x 1-digit, area models and partial products
def set_models(rnd, seen):
    its = []
    # A: base ten groups
    for k in range(4):
        while True:
            a, d = rnd.randint(13, 39), rnd.randint(2, 4)
            t, o = divmod(a, 10)
            if o == 0 or (a, d) in seen or t == o or (o * d < 10 and k < 3) or (k == 3 and o * d >= 10):
                continue
            break
        seen.add((a, d))
        e = ("There are %d groups of %d. Tens: %d × %s = %s = %d. Ones: %d × %d = %d. "
             % (d, a, d, unit_word(t, 1), unit_word(t * d, 1), t * d * 10, d, o, o * d))
        if o * d >= 10:
            e += "%d ones = %s and %s. " % (o * d, unit_word(o * d // 10, 1), unit_word(o * d % 10, 0))
        e += "%d + %d = %d." % (t * d * 10, o * d, a * d)
        its.append(mcq(fig(groups_svg(a, d)) + "The blocks show %d groups of %d. What is %d × %d?" % (d, a, a, d),
                       f(a * d), [f(v) for v in cands_mult(a, d)], e))
    # B: one part of the area model is missing
    for k in range(4):
        a, d = pick_2x1(rnd, seen, 21, 89)
        t, o = divmod(a, 10)
        t *= 10
        if k % 2 == 0:
            show, ans = ["?", f(o * d)], t * d
            wrong = [t // 10 * d, t * d * 10, t + d, (t + 10) * d]
            e = "The ? part is %d × %d. %d × %d = %d, so %s × %d = %s = %d." % (
                t, d, t // 10, d, t // 10 * d, unit_word(t // 10, 1), d, unit_word(t // 10 * d, 1), t * d)
        else:
            show, ans = [f(t * d), "?"], o * d
            wrong = [o + d, (o - 1) * d, (o + 1) * d, o * 10 + d]
            e = "The ? part is %d × %d = %d." % (o, d, o * d)
        e += " The whole rectangle: %d × %d = %d + %d = %d." % (a, d, t * d, o * d, a * d)
        its.append(mcq(fig(area_1(a, d, show)) + "This area model shows %d × %d. What number goes in the part marked ?" % (a, d),
                       f(ans), [f(v) for v in wrong], e))
    # C: which expression is the same?
    for _ in range(3):
        a, d = pick_2x1(rnd, seen, 21, 89)
        t, o = divmod(a, 10)
        t *= 10
        right = "%d × %d + %d × %d" % (t, d, o, d)
        wrong = ["%d × %d + %d × %d" % (t // 10, d, o, d), "%d × %d + %d" % (t, d, o), "%d + %d × %d" % (t, o, d)]
        e = ("Split %d into %d + %d. Multiply <b>both</b> parts by %d, then add: %d × %d + %d × %d = %d + %d = %d."
             % (a, t, o, d, t, d, o, d, t * d, o * d, a * d))
        its.append(mcq("Which is the same as %d × %d?" % (a, d), right, wrong, e))
    # D: missing number
    for k in range(3):
        a, d = pick_2x1(rnd, seen, 21, 89)
        t, o = divmod(a, 10)
        t *= 10
        if k == 0:
            q = "%d × %d = %d × %d + ☐ × %d" % (a, d, t, d, d)
            ans, wrong = o, [t // 10, a, o * d]
            e = "%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is %d." % (a, t, o, a, d, t, d, o, d, o)
        elif k == 1:
            q = "%d × %d = ☐ × %d + %d × %d" % (a, d, d, o, d)
            ans, wrong = t, [t // 10, a, t * d]
            e = "%d = %d + %d, so the missing number is %d (%s, not %d). %d × %d + %d × %d = %d." % (
                a, t, o, t, unit_word(t // 10, 1), t // 10, t, d, o, d, a * d)
        else:
            q = "%d × %d = %d + ☐" % (a, d, t * d)
            ans, wrong = o * d, [o, o + d, (o + 1) * d]
            e = "%d × %d = %d × %d + %d × %d = %d + %d. The missing number is %d × %d = %d." % (
                a, d, t, d, o, d, t * d, o * d, o, d, o * d)
        its.append(mcq("What number goes in the box?  <b>%s</b>" % q, str(ans), [str(v) for v in wrong], e))
    # E: partial products with one row missing
    for _ in range(2):
        a, d = pick_2x1(rnd, seen, 23, 98)
        ps = list(reversed(parts(a)))
        show = [f(p * d) for p in ps]
        show[1] = "?"
        p = ps[1]
        lead = p // 10
        wrong = [lead * d, p * d * 10, p + d, (lead + 1) * d * 10]
        e = ("The ? row is %d × %d. %d × %d = %d, so %d × %s = %s = %d. "
             % (d, p, d, lead, lead * d, d, unit_word(lead, 1), unit_word(lead * d, 1), p * d))
        e += "Add the partial products: %d + %d = %d." % (ps[0] * d, p * d, a * d)
        its.append(mcq(fig(pp_svg(a, d, show)) + "What number goes in the box marked ?", f(p * d), [f(v) for v in wrong], e))
    # F: use the area model / partial products to find the product
    for k in range(4):
        a, d = pick_2x1(rnd, seen, 23, 98, dmax=9)
        q = (fig(area_1(a, d)) + "Use the area model to find %d × %d." % (a, d)) if k < 2 else \
            "Use partial products to find %d × %d." % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in cands_mult(a, d)], steps_pp(a, d)))
    return {"title": "Area models and partial products (23 × 4)", "items": its}


# ------------------------------------------------------------ set 3: 3-digit x 1-digit
def pick_3x1(rnd, seen, zero=None):
    while True:
        a, d = rnd.randint(112, 989), rnd.randint(3, 9)
        ds = digits(a)
        if a * d > 9999 or (a, d) in seen:
            continue
        if zero == "tens":
            if ds[1] != 0 or ds[0] == 0 or ds[0] * d < 10:
                continue
        elif zero == "ones":
            if ds[0] != 0 or ds[1] == 0 or ds[1] * d < 10:
                continue
        elif 0 in ds or len(carry_list(a, d)) < 2 or len(set(ds)) < 3:
            continue
        seen.add((a, d))
        return a, d


def set_three(rnd, seen, P):
    its = []
    # partial products with one row missing
    for k in range(3):
        a, d = pick_3x1(rnd, seen)
        ps = list(reversed(parts(a)))
        pos = [1, 2, 2][k]
        show = [f(p * d) for p in ps]
        show[pos] = "?"
        p = ps[pos]
        ans = p * d
        lead = p // 10 ** pos
        wrong = [lead * d, ans * 10, p + d, (lead + 1) * d * 10 ** pos]
        e = ("The ? row is %d × %s. %d × %d = %d, so %d × %s = %s = %s. "
             % (d, f(p), d, lead, lead * d, d, unit_word(lead, pos), unit_word(lead * d, pos), f(ans)))
        e += "Add all the partial products: %s = %s." % (" + ".join(f(x * d) for x in ps), f(a * d))
        its.append(mcq(fig(pp_svg(a, d, show)) + "What number goes in the box marked ?", f(ans), [f(v) for v in wrong], e))
    # which partial products
    for _ in range(2):
        a, d = pick_3x1(rnd, seen)
        ps = parts(a)
        right = " + ".join(f(p * d) for p in ps)
        opts = {
            right: a * d,
            " + ".join(str(x * d) for x in reversed(digits(a))): sum(x * d for x in digits(a)),
            " + ".join([f(ps[0]), f(ps[1]), f(ps[2] * d)]): ps[0] + ps[1] + ps[2] * d,
            " + ".join([f(ps[0] * d), f(ps[1] // 10 * d), f(ps[2] * d)]): ps[0] * d + ps[1] // 10 * d + ps[2] * d,
        }
        assert len(opts) == 4 and len(set(opts.values())) == 4, opts
        wrong = [k_ for k_ in opts if k_ != right]
        its.append(mcq("Which partial products add up to %d × %d?" % (a, d), right, wrong,
                       steps_pp(a, d) + " Keep the place value: %d × %d is %s, not %d." % (ps[1], d, f(ps[1] * d), ps[1] // 10 * d)))
    # area model, 3 parts
    for _ in range(2):
        a, d = pick_3x1(rnd, seen)
        its.append(mcq(fig(area_1(a, d)) + "Use the area model to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in cands_mult(a, d)], steps_pp(a, d)))
    # standard method
    for i in range(8):
        a, d = pick_3x1(rnd, seen)
        q = (fig(std_svg(a, d)) + "Multiply.") if i % 2 == 0 else "What is %d × %d?" % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in cands_mult(a, d)], steps_std(a, d)))
    # zeros
    a, d = pick_3x1(rnd, seen, zero="tens")
    c = (a % 10) * d // 10
    its.append(mcq(fig(std_svg(a, d)) + "Multiply.", f(a * d), [f(v) for v in cands_mult(a, d)],
                   steps_std(a, d) + " 0 × %d = 0, but you still add the regrouped %d." % (d, c)))
    a, d = pick_3x1(rnd, seen, zero="ones")
    its.append(mcq("What is %d × %d?" % (a, d), f(a * d), [f(v) for v in cands_mult(a, d)], steps_std(a, d)))
    # find the mistake
    LAB = {"reg": "Forgot to regroup", "ones": "Multiplied only the ones",
           "first": "Added the regrouped digit before multiplying", "none": "There is no mistake"}
    for kind in ("reg", "ones", "first"):
        while True:
            a, d = pick_3x1(rnd, seen)
            vals = {"reg": mult_wrong(a, d), "ones": only_ones(a, d), "first": mult_wrong(a, d, carry_first=True)}
            if len(set(vals.values()) | {a * d}) == 4:
                break
        name, he, his = P.next()
        w = vals[kind]
        why = {"reg": "%s wrote only the ones digit of each product and dropped the regrouped digits." % cap(he),
               "ones": "%s multiplied the %d ones by %d but left the tens and hundreds as they were (%s)." % (
                   cap(he), a % 10, d, " + ".join([f(a - a % 10), str(a % 10 * d)])),
               "first": "%s added the regrouped digit first and then multiplied. Multiply first, then add." % cap(he)}[kind]
        its.append(mcq("%s says %d × %d = %s. What mistake did %s make?" % (name, a, d, f(w), he), LAB[kind],
                       [LAB[k_] for k_ in ("reg", "ones", "first", "none") if k_ != kind], why + " " + steps_std(a, d)))
    return {"title": "Multiply 3-digit numbers by 1-digit numbers", "items": its}


# ------------------------------------------------------------ set 4: estimate first
def rounded(a):
    if a < 100:
        r = int(round(a / 10.0)) * 10
        return r, (a // 10 * 10 if r > a else a // 10 * 10 + 10), "to the nearest ten"
    r = int(round(a / 100.0)) * 100
    return r, (a // 100 * 100 if r > a else a // 100 * 100 + 100), "to the nearest hundred"


def pick_est(rnd, seen, lo, hi, up=None):
    while True:
        a, d = rnd.randint(lo, hi), rnd.randint(3, 9)
        if (a, d) in seen or a * d > 9999 or a % 10 == 0:
            continue
        mid = a % 10 if a < 100 else a // 10 % 10
        if mid == 5 or (a >= 100 and a % 100 < 10) or len(carry_list(a, d)) < 1:
            continue
        r, _, _ = rounded(a)
        if up is not None and (r > a) != up:
            continue
        seen.add((a, d))
        return a, d


def set_estimate(rnd, seen, P):
    its = []
    # A: round, then multiply
    for i in range(8):
        a, d = pick_est(rnd, seen, 23, 98) if i < 4 else pick_est(rnd, seen, 112, 989)
        r, other, what = rounded(a)
        cands = [f(other * d), f(r * d * 10), f(r + d), f(r * d // 10)]
        e = ("%d rounds to %s. %s × %d = %s. The exact answer is %s, which is close to %s."
             % (a, f(r), f(r), d, f(r * d), f(a * d), f(r * d)))
        its.append(mcq("Estimate %d × %d. Round %d %s first." % (a, d, a, what), f(r * d), cands, e))
    # B: best way to estimate
    for lo, hi in [(23, 98), (112, 989)]:
        a, d = pick_est(rnd, seen, lo, hi, up=True)
        r, other, what = rounded(a)
        its.append(mcq("Which is the best way to estimate %d × %d?" % (a, d), "%s × %d" % (f(r), d),
                       ["%s × %d" % (f(other), d), "%s × 10" % f(r), "%d × 10" % a],
                       "Round %d %s: %d is closer to %s than to %s. Keep %d as it is: it is already a one-digit number. "
                       "Estimate: %s × %d = %s." % (a, what, a, f(r), f(other), d, f(r), d, f(r * d))))
    # C: which answer is reasonable?
    for i in range(6):
        while True:
            a, d = pick_est(rnd, seen, 112, 989) if i < 4 else pick_est(rnd, seen, 34, 98)
            r = rounded(a)[0]
            est = r * d
            pool = [only_ones(a, d), a * d * 10, tens_as_ones(a, d), a + d, concat(a, d)]
            far = [v for v in pool if v != a * d and not 0.7 * est <= v <= 1.4 * est]
            far = list(dict.fromkeys(far))
            if len(far) >= 3:
                break
            seen.discard((a, d))
        e = ("Estimate: %d rounds to %s, and %s × %d = %s. Only %s is close to %s; the other answers are far too small or too big. "
             % (a, f(r), f(r), d, f(est), f(a * d), f(est))) + steps_std(a, d)
        its.append(mcq("Estimate first. Which answer to %d × %d is reasonable?" % (a, d), f(a * d), [f(v) for v in far], e))
    # D: is it reasonable?
    LAB = {"yes": "Yes, it is close to the estimate", "big": "No, it is much too big",
           "small": "No, it is much too small", "eq": "No, it must equal the estimate"}
    for kind in ("yes", "big", "small", "yes"):
        while True:
            a, d = pick_est(rnd, seen, 112, 989)
            r = rounded(a)[0]
            est = r * d
            w = {"yes": a * d, "big": a * d * 10, "small": only_ones(a, d)}[kind]
            if kind != "small" or w < 0.6 * est:
                break
            seen.discard((a, d))
        name, he, his = P.next()
        q = "%s works out %d × %d = %s. Use an estimate. Is %s answer reasonable?" % (name, a, d, f(w), his)
        if kind == "yes":
            e = "Estimate: %s × %d = %s. %s is close to %s, so it is reasonable. An exact answer does not have to equal the estimate." % (
                f(r), d, f(est), f(w), f(est))
        else:
            e = "Estimate: %s × %d = %s. %s is much %s than %s, so there is a mistake. " % (
                f(r), d, f(est), f(w), "bigger" if kind == "big" else "smaller", f(est)) + steps_std(a, d)
        its.append(mcq(q, LAB[kind], [LAB[k_] for k_ in ("yes", "big", "small", "eq") if k_ != kind], e))
    return {"title": "Estimate first, then check", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(P):
    its = []
    D = lambda v: "$" + f(v)

    def unit(fmt):
        return D if fmt == "$" else (lambda v, s=fmt: s.format(f(v)))

    # x 10, 100, 1000
    POW = [
        ("Hockey cards come in packs of 10. {n} has {a} packs. How many cards does {he} have?", 46, 10, "{} cards"),
        ("A roll of raffle tickets has 1000 tickets. The school uses {a} rolls at its winter carnival. How many tickets is that?", 4, 1000, "{} tickets"),
        ("A sugar bush sells maple taffy in boxes of 10 pieces. It sells {a} boxes on a Saturday in March. How many pieces of taffy is that?", 80, 10, "{} pieces"),
        ("A box holds 100 craft sticks. The art teacher orders {a} boxes. How many craft sticks is that?", 25, 100, "{} craft sticks"),
    ]
    for t, a, m, fmt in POW:
        n, he, his = P.next()
        fm = unit(fmt)
        its.append(mcq(t.format(n=n, he=he, his=his, a=a), fm(a * m), [fm(v) for v in cands_pow(a, m)],
                       "Multiply: %s × %s. " % (f(a), f(m)) + e_pow(a, m) + " So the answer is %s." % fm(a * m)))
    # equal groups: (text, a, d, format)
    M = [
        ("Tickets to a hockey game cost ${a} each. {n} buys {d} tickets for {his} family. How much does {he} pay?", 28, 4, "$"),
        ("On a canoe trip in Algonquin Park, a group paddles {a} km each day for {d} days. How far do they paddle?", 18, 6, "{} km"),
        ("A Grade 4 class reads for {a} minutes every school day. How many minutes is that in {d} school days?", 35, 5, "{} minutes"),
        ("{d} flocks of Canada geese land on a pond. Each flock has {a} geese. How many geese land on the pond?", 47, 3, "{} geese"),
        ("A skating rink keeps rental skates on racks. Each rack holds {a} pairs. There are {d} racks. How many pairs of skates is that?", 36, 7, "{} pairs"),
        ("For the Terry Fox Run, each of {d} classes at a school in Ottawa raises ${a}. How much do they raise in all?", 126, 8, "$"),
        ("A truck driver drives {a} km each day. How far does {he} drive in {d} days?", 386, 5, "{} km"),
        ("A school library has {d} shelves of chapter books. Each shelf holds {a} books. How many books is that?", 145, 7, "{} books"),
        ("An arena in Hamilton has {d} sections. Each section has {a} seats. How many seats are there?", 238, 6, "{} seats"),
        ("A store sells winter boots for ${a} a pair. It sells {d} pairs on a snowy Saturday. How much money is that?", 129, 7, "$"),
        ("An orchard fills {d} crates with apples. Each crate holds {a} apples. How many apples is that?", 124, 9, "{} apples"),
    ]
    for t, a, d, fmt in M:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=a, d=d)
        q = q[0].upper() + q[1:]
        fm = unit(fmt)
        e = "Equal groups, so multiply: %s × %d. " % (fm(a), d) + steps_std(a, d) + " So the answer is %s." % fm(a * d)
        its.append(mcq(q, fm(a * d), [fm(v) for v in cands_mult(a, d)], e))
    # two steps
    n, he, his = P.next()
    c = 3 * 45
    its.append(mcq("%s buys 3 hockey sticks at $45 each. %s pays with $200. How much change does %s get?" % (n, cap(he), he),
                   D(200 - c), [D(c), D(200 - mult_wrong(45, 3)), D(200 + c)],
                   "Step 1: cost: 3 × $45 = $%d (5 × 3 = 15, write 5, regroup 1; 4 × 3 = 12, plus 1 = 13). "
                   "Step 2: change: $200 − $%d = $%d." % (c, c, 200 - c)))
    c = 6 * 125
    its.append(mcq("A school has 6 boxes of pencils with 125 pencils in each box. It gives out 480 pencils. How many pencils are left?",
                   "%d pencils" % (c - 480), ["%d pencils" % c, "%d pencils" % (c + 480), "%d pencils" % (mult_wrong(125, 6) - 480)],
                   "Step 1: 6 × 125 = %d (5 × 6 = 30, write 0, regroup 3; 2 × 6 = 12, plus 3 = 15, write 5, regroup 1; "
                   "1 × 6 = 6, plus 1 = 7). Step 2: %d − 480 = %d." % (c, c, c - 480)))
    c = 4 * 48
    its.append(mcq("A school books 4 small buses for a field trip. Each bus has 48 seats. 175 people go on the trip. How many seats are empty?",
                   "%d seats" % (c - 175), ["%d seats" % c, "%d seats" % (c + 175), "23 seats"],
                   "Step 1: seats: 4 × 48 = %d (8 × 4 = 32, write 2, regroup 3; 4 × 4 = 16, plus 3 = 19). "
                   "Step 2: empty seats: %d − 175 = %d. (Regroup a ten to subtract the ones: 12 − 5 = 7.)" % (c, c, c - 175)))
    # estimate
    its.append(mcq("A school has 6 Grade 4 classes. Each class has 28 students. About how many Grade 4 students are there?",
                   "about 180", ["about 120", "about 1800", "about 36"],
                   "Round 28 to the nearest ten: 30. 30 × 6 = 180. (The exact answer is 28 × 6 = 168, close to 180.)"))
    its.append(mcq("A summer camp buys 7 tents. Each tent costs $289. About how much do the tents cost?",
                   "about $2100", ["about $1400", "about $21" + NBSP + "000", "about $307"],
                   "Round $289 to the nearest hundred: $300. $300 × 7 = $2100. (The exact cost is 289 × 7 = $2023, close to $2100.)"))
    return {"title": "Word problems: hockey, field trips and more", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Multiply by 10, 100 and 1000</h2>"
        "<p>When you multiply by 10, every digit moves <b>one place to the left</b>. A zero fills the empty ones place. "
        "× 100 moves the digits two places, and × 1000 moves them three places.</p>"
        "<figure class='sn-fig'>" + pv_svg(36, 10, hide=False, label="place value chart for 36 times 10") +
        "<figcaption>36 × 10: 3 tens become 3 hundreds and 6 ones become 6 tens. 36 × 10 = 36 tens = 360.</figcaption></figure>" +
        table(["Multiply", "Think", "Answer"], [
            ["36 × 10", "36 tens", "360"],
            ["36 × 100", "36 hundreds", "3600"],
            ["4 × 1000", "4 thousands", "4000"],
            ["40 × 10", "40 tens", "400 (not 4000)"],
        ]) +
        "<h2>Two digits: split into tens and ones</h2>"
        "<p>23 × 4 means 4 groups of 23. Each 23 is 2 tens and 3 ones. Multiply the tens, multiply the ones, then add.</p>"
        "<figure class='sn-fig'>" + groups_svg(23, 4, "4 groups of 23 in base ten blocks") +
        "<figcaption>4 groups of 23: 8 tens and 12 ones. 12 ones = 1 ten and 2 ones, so the total is 9 tens and 2 ones = 92.</figcaption></figure>"
        "<p>An <b>area model</b> shows the same thing. The rectangle is 23 long and 4 wide. Split 23 into 20 and 3.</p>"
        "<figure class='sn-fig'>" + area_1(23, 4, ["80", "12"], "area model for 23 times 4") +
        "<figcaption>20 × 4 = 80 and 3 × 4 = 12. These are the <b>partial products</b>. Add them: 80 + 12 = 92.</figcaption></figure>"
        "<h2>Three digits: partial products and the standard method</h2>"
        "<p><b>Partial products</b> write each part on its own row, then add the rows. "
        "The <b>standard method</b> is a short way to write the same steps. Start with the ones. "
        "If you get 10 or more, write the ones digit and <b>regroup</b>: write a small digit above the next place. "
        "Multiply first, then add the regrouped digit.</p>"
        "<figure class='sn-fig'>" + pp_svg(236, 4, total="944", label="236 times 4 with partial products") +
        "<figcaption>4 × 6 = 24, 4 × 30 = 120 and 4 × 200 = 800. Add: 24 + 120 + 800 = 944.</figcaption></figure>"
        "<figure class='sn-fig'>" + std_svg(236, 4, "944", {1: 2, 2: 1}, "236 times 4 with the standard method") +
        "<figcaption>Ones: 6 × 4 = 24, write 4, regroup 2 tens. Tens: 3 × 4 = 12, plus 2 = 14, write 4, regroup 1 hundred. "
        "Hundreds: 2 × 4 = 8, plus 1 = 9. Answer: 944.</figcaption></figure>"
        "<h2>Estimate first</h2>"
        "<p>Round the big number, then multiply. The estimate tells you about how big the answer should be.</p>" +
        ex("Estimate, then check", "389 × 6 = ?",
           "389 rounds to 400. 400 × 6 = 2400. Now multiply: 9 × 6 = 54, write 4, regroup 5. "
           "8 × 6 = 48, plus 5 = 53, write 3, regroup 5. 3 × 6 = 18, plus 5 = 23. "
           "2334 is close to 2400, so it makes sense.", "2334") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting to regroup (23 × 4 = 82)", "12 ones = 1 ten and 2 ones. Add the 1 ten to the tens: 92"],
            ["Multiplying only the ones (23 × 4 = 32)", "Multiply the tens too: 20 × 4 = 80, 3 × 4 = 12, 80 + 12 = 92"],
            ["Adding an extra zero (40 × 10 = 4000)", "40 is 4 tens. 40 tens = 400. × 10 adds only one zero"],
            ["Writing 20 × 4 as 8", "20 × 4 = 2 tens × 4 = 8 tens = 80"],
            ["Adding the regrouped digit first ((3 + 2) × 4)", "Multiply first: 3 × 4 = 12, then add 2: 14"],
        ])
    )


FAQ = [
    {"q": "What multiplication do Grade 4 students learn in Ontario?",
     "a": "The Ontario math curriculum asks Grade 4 students to multiply two- and three-digit numbers by one-digit numbers, and by 10, 100 and 1000, using tools such as arrays, base ten blocks and area models. They also use mental math to multiply by 10, 100 and 1000."},
    {"q": "What are partial products?",
     "a": "Partial products split a number by place value and multiply each part. For 23 × 4, multiply 20 × 4 = 80 and 3 × 4 = 12, then add: 80 + 12 = 92."},
    {"q": "How do you multiply by 10, 100 and 1000 in your head?",
     "a": "Each digit moves one, two or three places to the left, and zeros fill the empty places. So 36 × 10 = 360, 36 × 100 = 3600 and 4 × 1000 = 4000, while 40 × 10 is 400, not 4000."},
    {"q": "Why should students estimate before they multiply?",
     "a": "An estimate shows about how big the answer should be. For 389 × 6, 400 × 6 = 2400, so 2334 makes sense, but an answer like 258 or 23" + NBSP + "340 shows a mistake."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def gen():
    rnd = random.Random(44805)
    P = People(rnd)
    seen = set()
    sets = [set_pow(rnd), set_models(rnd, seen), set_three(rnd, seen, P), set_estimate(rnd, seen, P), set_story(P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0] * 4
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            pos[it["a"]] += 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
        assert pos == [5, 5, 5, 5], pos
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "multiplying-by-one-digit-numbers", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying by One-Digit Numbers",
        "seo_title": "Grade 4 Multiplying by One-Digit Numbers Worksheets: × 10, 100, 1000, Area Models, Partial Products (Free, Ontario)",
        "short_title": "Multiplying by one-digit numbers",
        "domain": "Number",
        "standard_code": "Grade 4: B2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the multiplication of two- or three-digit whole numbers by one-digit whole numbers and by 10, 100, and 1000, using appropriate tools, including arrays",
        "meta_desc": "Free Grade 4 math worksheets on multiplying by one-digit numbers for the Ontario curriculum: multiplying by 10, 100 and 1000, area models, partial products, 3-digit × 1-digit, estimating first and word problems. 100 questions with an answer key.",
        "key_big": "Split the number into hundreds, tens and ones. Multiply each part, then add the parts.",
        "key_sub": "23 × 4 = 20 × 4 + 3 × 4 = 80 + 12 = 92. To multiply by 10, 100 or 1000, the digits move 1, 2 or 3 places to the left: 40 × 10 = 400. Estimate first to check your answer.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(area model|[0-9]+ groups of|place value chart)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
