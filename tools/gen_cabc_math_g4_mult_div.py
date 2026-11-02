# -*- coding: utf-8 -*-
"""
CA-BC Grade 4 Math: Multiplying and dividing by one-digit numbers
(BC Mathematics Curriculum, Grade 4, Computational fluency:
 multiplication and division of two- or three-digit numbers by one-digit numbers)
Base ten blocks and area models, partial products and the standard method, dividing by sharing
with base ten (trading), remainders and what they mean, BC word problems.
  python3 tools/gen_cabc_math_g4_mult_div.py
HTML attributes use single quotes (no backslashes in the JSON). Every answer is computed in code.
BC style: Canadian English, metric, $ (whole dollars here), 4-digit numbers without a separator.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
GREY = "#6b6259"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
NBSP = " "


# ------------------------------------------------------------ helpers
def f(n):
    """BC style: 4536, 10 000 (no-break space only from 5 digits)."""
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


# ------------------------------------------------------------ division helpers
def div_share(n, d, who="group"):
    """Share n into d equal groups, one place at a time, trading what is left over."""
    ds = [int(c) for c in str(n)]
    L = len(ds)
    carry, out, started = 0, [], False
    for k, x in enumerate(ds):
        i = L - 1 - k
        amt = carry * 10 + x
        if not started and amt < d and k < L - 1:
            if amt:
                out.append("%s %s not enough for %d %ss. Trade %s for %s." % (
                    cap(unit_word(amt, i)), "is" if amt == 1 else "are", d, who, "it" if amt == 1 else "them", unit_word(amt * 10, i - 1)))
            carry = amt
            continue
        started = True
        each, left = divmod(amt, d)
        lead = ("Now there are %s. " % unit_word(amt, i)) if carry else ""
        s = lead + "Share %s: each %s gets %s" % (unit_word(amt, i), who, unit_word(each, i))
        if left and i > 0:
            s += ", %s left. Trade %s for %s." % (unit_word(left, i), "it" if left == 1 else "them", unit_word(left * 10, i - 1))
        elif left:
            s += ", %s left over." % unit_word(left, i)
        else:
            s += "."
        out.append(s)
        carry = left
    q, r = divmod(n, d)
    out.append("Each %s gets %s%s." % (who, f(q), (" and %d %s left over: %s" % (r, "is" if r == 1 else "are", qr(q, r))) if r else ""))
    chk = ("Check: %s × %d + %d = %s." % (f(q), d, r, f(n))) if r else ("Check: %s × %d = %s." % (f(q), d, f(n)))
    return " ".join(out) + " " + chk


def digitwise(n, d):
    """Dividing each digit on its own and dropping what is left (52 ÷ 4 -> 1 | 0 -> 10)."""
    return int("".join(str(int(c) // d) for c in str(n)))


def cands_div(n, d):
    q = n // d
    c = ([digitwise(n, d)] if digitwise(n, d) * 2 > q else []) + [q * 10, q + 1, q - 1, q + 10, q - 10, q + 2]
    return [f(x) for x in c]


def cands_rem(n, d):
    q, r = divmod(n, d)
    return [qr(q - 1, r + d), f(q), qr(q, d - r), qr(q + 1, r), qr(q - 1, r), f(q + 1)]


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


def pile_svg(n, label=None):
    """The base ten blocks for one number."""
    h, rest = divmod(n, 100)
    t, o = divmod(rest, 10)
    body, w, hgt = blocks(h, t, o, 4, 4)
    return svg_wrap(int(w + 8), int(hgt + 8), body, label or "base ten blocks showing %d" % n)


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


def dots_svg(n, d, label=None):
    """n counters put in groups of d: each group is a column; leftovers in red at the end."""
    q, r = divmod(n, d)
    R, gap = 7, 19
    s = []
    x = 6
    for g in range(q + (1 if r else 0)):
        k = d if g < q else r
        col = GREEN if g < q else RED
        if g < q:
            s.append("<rect x='%.1f' y='3' width='%d' height='%d' rx='9' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (x - 3, 2 * R + 6, d * gap + 2, GREY))
        for j in range(k):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (x + R, 4 + gap / 2 + 1 + j * gap, R, col))
        x += 2 * R + 6 + (8 if g == q - 1 else 5)
    return svg_wrap(int(x), int(d * gap + 8), "".join(s), label or "%d counters put in groups of %d" % (n, d))


# ------------------------------------------------------------ set 1: base ten blocks and area models
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


def set_models(rnd, seen):
    its = []
    # A: base ten groups
    for k in range(5):
        while True:
            a, d = rnd.randint(13, 39), rnd.randint(2, 4)
            t, o = divmod(a, 10)
            if o == 0 or (a, d) in seen or t == o or (o * d < 10 and k < 4) or (k == 4 and o * d >= 10):
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
    for k in range(5):
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
    for _ in range(4):
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
    # E: 3-digit area models (hardest, last)
    for _ in range(3):
        while True:
            a, d = rnd.randint(112, 489), rnd.randint(3, 6)
            if 0 in digits(a) or (a, d) in seen or len(carry_list(a, d)) < 2:
                continue
            break
        seen.add((a, d))
        its.append(mcq(fig(area_1(a, d)) + "Use the area model to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in cands_mult(a, d)], steps_pp(a, d)))
    return {"title": "Multiply with base ten blocks and area models", "items": its}


# ------------------------------------------------------------ set 2: partial products and the standard method
def pick_3x1(rnd, seen, zero=False):
    while True:
        a, d = rnd.randint(112, 989), rnd.randint(3, 9)
        ds = digits(a)
        if a * d > 9999:
            continue
        if zero:
            if ds[1] != 0 or ds[0] == 0 or ds[0] * d < 10:
                continue
        elif 0 in ds or len(carry_list(a, d)) < 2:
            continue
        if (a, d) in seen:
            continue
        seen.add((a, d))
        return a, d


def set_methods(rnd, seen):
    its = []
    # partial products with one row missing
    for k in range(4):
        if k < 2:
            a, d = pick_2x1(rnd, seen, 23, 98)
        else:
            a, d = pick_3x1(rnd, seen)
        ps = list(reversed(parts(a)))
        pos = 1 if k != 3 else 2
        show = [f(p * d) for p in ps]
        show[pos] = "?"
        p = ps[pos]
        ans = p * d
        lead = p // 10 ** pos
        wrong = [lead * d, ans * 10, p + d, (lead + 1) * d * 10 ** pos]
        e = ("The ? row is %d × %s. %d × %d = %d, so %d × %s = %s = %s. "
             % (d, f(p), d, lead, lead * d, d, unit_word(lead, pos), unit_word(lead * d, pos), f(ans)))
        e += "All the partial products: %s = %s." % (" + ".join(f(x * d) for x in ps), f(a * d))
        its.append(mcq(fig(pp_svg(a, d, show)) + "What number goes in the box marked ?", f(ans), [f(v) for v in wrong], e))
    # standard method: 2-digit (4) and 3-digit (5) and a zero in the tens (1)
    for i in range(4):
        a, d = pick_2x1(rnd, seen, 23, 98)
        q = (fig(std_svg(a, d)) + "Multiply.") if i % 2 == 0 else "What is %d × %d?" % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in cands_mult(a, d)], steps_std(a, d)))
    for i in range(5):
        a, d = pick_3x1(rnd, seen)
        q = (fig(std_svg(a, d)) + "Multiply.") if i % 2 == 1 else "What is %d × %d?" % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in cands_mult(a, d)], steps_std(a, d)))
    a, d = pick_3x1(rnd, seen, zero=True)
    c = (a % 10) * d // 10
    its.append(mcq(fig(std_svg(a, d)) + "Multiply.", f(a * d), [f(v) for v in cands_mult(a, d)],
                   steps_std(a, d) + " 0 × %d = 0, but you still add the regrouped %d." % (d, c)))
    # what is the next step?
    for k in range(3):
        while True:
            a, d = pick_2x1(rnd, seen, 23, 98)
            t, o = divmod(a, 10)
            p0 = o * d
            p1 = t * d + p0 // 10
            if p0 % 10 != p0 // 10 and p1 >= 10 and p1 % 10 and p0 % 10 and (t + p0 // 10) * d != p1:
                break
            seen.discard((a, d))
        c = p0 // 10
        if k != 1:
            q = fig(std_svg(a, d)) + "Start with the ones: %d × %d = %d. What do you do?" % (o, d, p0)
            right = "write %d, regroup %d" % (p0 % 10, c)
            wrong = ["write %d, regroup %d" % (c, p0 % 10), "write %d" % p0, "write %d only" % (p0 % 10)]
            e = ("%d ones = %s and %s. Write %d in the ones place. Regroup %s: write a small %d above the tens. "
                 % (p0, unit_word(c, 1), unit_word(p0 % 10, 0), p0 % 10, unit_word(c, 1), c) + steps_std(a, d))
        else:
            q = (fig(std_svg(a, d, " " + str(p0 % 10), {1: c})) +
                 "The ones are done. Now the tens: %d × %d, then add the regrouped %d. What is the full answer?" % (t, d, c))
            right = f(a * d)
            wrong = [f(t * d * 10 + p0 % 10), f((t + c) * d * 10 + p0 % 10), f((p1 % 10) * 10 + p0 % 10)]
            e = ("Multiply first, then add: %d × %d = %d, plus %d = %d. The tens are the last place, so write all of %d. "
                 % (t, d, t * d, c, p1, p1) + "Answer: %s." % f(a * d))
        its.append(mcq(q, right, wrong, e))
    # estimate first
    for a, d in [(48, 7), (82, 6), (296, 4)]:
        seen.add((a, d))
        if a < 100:
            r10 = int(round(a / 10.0)) * 10
            other = a // 10 * 10 if r10 > a else a // 10 * 10 + 10
            what = "to the nearest ten"
        else:
            r10 = int(round(a / 100.0)) * 100
            other = a // 100 * 100 if r10 > a else a // 100 * 100 + 100
            what = "to the nearest hundred"
        q = "Estimate %d × %d. Round %d %s first." % (a, d, a, what)
        e = ("%d rounds to %d. %d × %d = %d. The exact answer is %s, which is close to %d."
             % (a, r10, r10, d, r10 * d, f(a * d), r10 * d))
        its.append(mcq(q, f(r10 * d), [f(other * d), f(r10 * d * 10), f(r10 + d)], e))
    return {"title": "Partial products and the standard method", "items": its}


# ------------------------------------------------------------ set 3: divide by sharing and with base ten
def set_share(rnd, used):
    its = []
    # sharing pictures: (n, d)
    for n, d in [(69, 3), (48, 4), (52, 4), (72, 3), (246, 2), (132, 4)]:
        used.add(n)
        q = n // d
        e = div_share(n, d)
        its.append(mcq(fig(pile_svg(n)) + "Share these blocks equally into %d groups. How many are in each group?" % d,
                       f(q), cands_div(n, d), e))
    # trading ideas
    its.append(mcq("You share 5 tens equally into 4 groups. Each group gets 1 ten. What do you do with the 1 ten that is left?",
                   "Trade it for 10 ones", ["Leave it out", "Trade it for 1 one", "Give it to one group"],
                   "Every group must get the same amount, so do not leave it out or give it to one group. "
                   "Trade 1 ten for 10 ones and keep sharing. For 52 ÷ 4: 10 + 2 = 12 ones, so each group gets 3 more ones. 52 ÷ 4 = 13."))
    its.append(mcq("You share 1 hundred, 3 tens and 2 ones equally into 4 groups. There are not enough hundreds. What do you do first?",
                   "Trade 1 hundred for 10 tens", ["Trade 1 hundred for 10 ones", "Leave the hundred out", "Give the hundred to one group"],
                   "Every group needs the same amount, so trade 1 hundred for 10 tens. " + div_share(132, 4)))
    its.append(mcq("To find 75 ÷ 5, you share 7 tens: each group gets 1 ten and 2 tens are left. "
                   "You trade the 2 tens for ones. How many ones are there to share now?",
                   "25 ones", ["5 ones", "20 ones", "7 ones"],
                   "2 tens = 20 ones. Add the 5 ones you already had: 20 + 5 = 25 ones. 25 ÷ 5 = 5, so 75 ÷ 5 = 15."))
    # area models (partial quotients)
    for n, d in [(96, 4), (162, 3), (378, 6), (185, 5)]:
        used.add(n)
        ps, rest = [], n
        for scale in (100, 10):
            k = (rest // scale) // d * d * scale
            if k:
                ps.append(k)
                rest -= k
        if rest:
            ps.append(rest)
        pq = [p // d for p in ps]
        q = n // d
        tops = ["?"] * len(ps)
        svg = area_svg(d, tops, [f(p) for p in ps], "area model for %d divided by %d" % (n, d), wsum=200)
        e = ("The model splits %d into %s. Divide each part by %d: %s. Add: %s = %d. Check: %d × %d = %d."
             % (n, " + ".join(f(p) for p in ps), d, ", ".join("%d ÷ %d = %d" % (p, d, x) for p, x in zip(ps, pq)),
                " + ".join(str(x) for x in pq), q, q, d, n))
        cands = [f(q - pq[0] + pq[0] // 10) if pq[0] >= 10 else f(q * 10), f(q - pq[-1]), f(q * 10), f(q + 10), f(q + 1)]
        its.append(mcq(fig(svg) + "Use the area model to find %d ÷ %d." % (n, d), f(q), cands, e))
    # plain divisions
    for n, d in [(84, 6), (91, 7), (256, 8), (138, 3)]:
        used.add(n)
        its.append(mcq("What is %d ÷ %d?" % (n, d), f(n // d), cands_div(n, d), div_share(n, d)))
    # think multiplication
    for n, d in [(96, 8), (115, 5), (234, 9)]:
        used.add(n)
        q = n // d
        e = "Think: %d times what number is %d? That is %d ÷ %d. " % (d, n, n, d) + div_share(n, d)
        its.append(mcq("What number goes in the box?  <b>☐ × %d = %d</b>" % (d, n), f(q), cands_div(n, d), e))
    return {"title": "Divide by sharing and with base ten", "items": its}


# ------------------------------------------------------------ set 4: remainders
def pick_rem(rnd, used, lo, hi, dlo=3, dhi=9):
    while True:
        d = rnd.randint(dlo, dhi)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if r == 0 or n in used or q < 10 or "0" in str(q) or r == q % 10:
            continue
        used.add(n)
        return n, d


def set_rem(rnd, used, P):
    its = []
    # counters
    for n, d in [(38, 5), (27, 4), (44, 6), (31, 3)]:
        used.add(n)
        q, r = divmod(n, d)
        e = ("Make groups of %d. There are %d full groups and %d %s left over (in red). "
             "%d is less than %d, so it cannot make another group. %d ÷ %d = %s. Check: %d × %d + %d = %d."
             % (d, q, r, "counter" if r == 1 else "counters", r, d, n, d, qr(q, r), q, d, r, n))
        its.append(mcq(fig(dots_svg(n, d)) + "The picture shows %d counters in groups of %d. What is %d ÷ %d?" % (n, d, n, d),
                       qr(q, r), cands_rem(n, d), e))
    # compute
    for i in range(6):
        n, d = pick_rem(rnd, used, 41, 98) if i < 3 else pick_rem(rnd, used, 112, 989)
        q, r = divmod(n, d)
        its.append(mcq("What is %d ÷ %d?" % (n, d), qr(q, r), cands_rem(n, d), div_share(n, d)))
    # the remainder only
    for _ in range(2):
        n, d = pick_rem(rnd, used, 120, 980, 4)
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), str(r),
                       [f(q), str(d - r), str(r + d), str(d)],
                       "The question asks for the remainder, not the quotient. " + div_share(n, d)))
    # check by multiplying
    for _ in range(2):
        n, d = pick_rem(rnd, used, 120, 980)
        q, r = divmod(n, d)
        good = "%d × %d + %d" % (q, d, r)
        its.append(mcq("%d ÷ %d = %s. Which expression checks this answer? It should equal %d." % (n, d, qr(q, r), n), good,
                       ["%d × %d − %d" % (q, d, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (q, d, r)],
                       "Multiply the quotient by the divisor, then add the remainder: %d × %d = %d, %d + %d = %d. "
                       "It matches, so the answer is right." % (q, d, q * d, q * d, r, n)))
    # remainder too big
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick_rem(rnd, used, 50, 99, 4, 8)
        q, r = divmod(n, d)
        its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he),
                       "The remainder is too big",
                       ["%s forgot the remainder" % cap(he), "There should be no remainder", "There is no mistake"],
                       "The remainder must be less than the divisor. %d is more than %d, so one more group of %d fits: "
                       "%d − %d = %d. The answer is %s. Check: %d × %d + %d = %d." % (r + d, d, d, r + d, d, r, qr(q, r), q, d, r, n)))
    # which remainder is possible
    for d, right, wrong in [(6, "5", ["6", "7", "9"]), (4, "3", ["4", "5", "8"])]:
        its.append(mcq("You divide a number by %d. Which of these could be the remainder?" % d, right, wrong,
                       "A remainder is always less than the divisor. When you divide by %d, the remainder can only be 0 to %d. "
                       "So %s is the only possible one." % (d, d - 1, right)))
    # what the remainder means
    its.append(mcq("27 ÷ 4 = 6 R 3. There are 27 cookies and 4 cookies go in each bag. What does the 3 mean?",
                   "3 cookies are left over", ["3 bags are full", "Each bag has 3 cookies", "3 more bags are needed"],
                   "6 bags are full (6 × 4 = 24 cookies). 27 − 24 = 3 cookies do not fill another bag. The remainder 3 is the cookies left over."))
    its.append(mcq("50 ÷ 8 = 6 R 2. There are 50 students and 8 students fit in each van. What does the 2 mean?",
                   "2 students still need a seat", ["2 vans are full", "Each van has 2 empty seats", "2 vans are needed"],
                   "6 vans carry 6 × 8 = 48 students. 50 − 48 = 2 students are still waiting, so they need a 7th van."))
    return {"title": "Division with remainders and what the remainder means", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(P):
    its = []
    D = lambda v: "$" + f(v)

    # multiplication (equal groups): (text, a, d, format)
    M = [
        ("A box of Okanagan apples holds {a} apples. A fruit stand in Kelowna sells {d} boxes. How many apples is that?", 88, 6, "{} apples"),
        ("Tickets to a hockey game cost ${a} each. {n} buys {d} tickets for {his} family. How much does {he} pay?", 27, 5, "$"),
        ("For the Terry Fox Run, each of {d} classes at a Surrey school raises ${a}. How much do they raise in all?", 135, 8, "$"),
        ("A trail loop in Stanley Park is {a} m long. {n} walks the loop {d} times. How far does {he} walk?", 875, 4, "{} m"),
        ("A salmon hatchery has {d} tanks. Each tank holds {a} young salmon. How many young salmon are there?", 245, 6, "{} salmon"),
        ("A small ferry to an island carries {a} cars on each trip. It makes {d} trips in a day. How many cars is that?", 48, 7, "{} cars"),
        ("A Grade 4 class reads for {a} minutes every school day. How many minutes is that in {d} school days?", 25, 9, "{} minutes"),
    ]
    for t, a, d, fmt in M:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=a, d=d)
        fm = D if fmt == "$" else (lambda v, s=fmt: s.format(f(v)))
        e = "Equal groups, so multiply: %s × %d. " % (fm(a), d) + steps_std(a, d) + " So the answer is %s." % fm(a * d)
        its.append(mcq(q, fm(a * d), [fm(v) for v in cands_mult(a, d)], e))
    # two steps
    n, he, his = P.next()
    its.append(mcq("%s buys 6 swim passes at $14 each. %s pays with $100. How much change does %s get?" % (n, cap(he), he),
                   "$16", ["$84", "$26", "$94"],
                   "Step 1: cost: 6 × $14 = $84 (4 × 6 = 24, write 4, regroup 2; 1 × 6 = 6, plus 2 = 8). "
                   "Step 2: change: $100 − $84 = $16."))
    its.append(mcq("A school books 4 small buses for a trip to Whistler. Each bus has 36 seats. 129 people go on the trip. How many seats are empty?",
                   "15 seats", ["144 seats", "25 seats", "273 seats"],
                   "Step 1: seats: 4 × 36 = 144 (6 × 4 = 24, write 4, regroup 2; 3 × 4 = 12, plus 2 = 14). "
                   "Step 2: empty seats: 144 − 129 = 15."))
    # division, no remainder
    nm, he, his = P.next()
    DIV = [
        ("96 students come to a soccer day in Burnaby. They make 4 equal teams. How many students are on each team?", 96, 4, "{} students"),
        ("%s reads a 168-page book in 7 days. %s reads the same number of pages each day. How many pages does %s read each day?"
         % (nm, cap(he), he), 168, 7, "{} pages"),
        ("A cedar board is 192 cm long. It is cut into 8 equal pieces. How long is each piece?", 192, 8, "{} cm"),
    ]
    for t, n_, d, fmt in DIV:
        fm = lambda v, s=fmt: s.format(f(v))
        e = "Share equally, so divide: %d ÷ %d. " % (n_, d) + div_share(n_, d) + " So the answer is %s." % fm(n_ // d)
        its.append(mcq(t, fm(n_ // d), [fm(int(x)) for x in cands_div(n_, d)], e))

    def rem_item(t, n_, d, kind, one, many, why):
        q, r = divmod(n_, d)
        U = lambda k: "%s %s" % (f(k), one if k == 1 else many)
        base = "Divide: %d ÷ %d = %s (%d × %d = %d, %d − %d = %d). " % (n_, d, qr(q, r), q, d, q * d, n_, q * d, r)
        if kind == "up":
            ans = U(q + 1)
            e = base + "%s hold only %d. The %s left over %s, so add 1 more. The answer is %s." % (
                cap(U(q)), q * d, why[0] % r, why[1], ans)
            cands = [U(q), qr(q, r), U(r), U(q + 2)]
        elif kind == "down":
            ans = U(q)
            e = base + "The %s left over %s not enough %s, so leave the remainder out. The answer is %s." % (
                why[0] % r, "is" if (r == 1 or why[0].startswith("$")) else "are", why[1], ans)
            cands = [U(q + 1), qr(q, r), U(r), U(q - 1)]
        else:
            ans = U(r)
            e = base + "The question asks how many are left over. That is the remainder: %s." % ans
            cands = [U(q), U(d - r), qr(q, r), U(r + d)]
        its.append(mcq(t, ans, cands, e))

    # round up
    rem_item("75 students and adults go on a field trip to the aquarium. Each shuttle bus holds 9 people. "
             "How many shuttle buses are needed to take everyone?", 75, 9, "up", "bus", "buses",
             ("%d people", "still need a seat"))
    rem_item("52 campers go canoeing on a lake near Kamloops. Each canoe holds 3 campers. How many canoes do they need?",
             52, 3, "up", "canoe", "canoes", ("%d camper" if 52 % 3 == 1 else "%d campers", "still needs a canoe" if 52 % 3 == 1 else "still need a canoe"))
    rem_item("118 students go on an overnight trip on Vancouver Island. Each tent sleeps 4 students. How many tents are needed?",
             118, 4, "up", "tent", "tents", ("%d students", "still need a tent"))
    rem_item("A class of 29 students goes to a soccer game. Each van holds 6 students. How many vans are needed?",
             29, 6, "up", "van", "vans", ("%d students" if 29 % 6 != 1 else "%d student", "still need a seat"))
    # round down
    rem_item("An orchard in the Okanagan picked 467 apples. It packs them in gift boxes of 8. How many boxes can it fill completely?",
             467, 8, "down", "box", "boxes", ("%d apples", "to fill another box"))
    nm, he, his = P.next()
    rem_item("%s has $40. A swim pass costs $6. How many swim passes can %s buy?" % (nm, he),
             40, 6, "down", "pass", "passes", ("$%d", "to buy another pass"))
    # left over
    rem_item("A farm stand in Penticton has 230 peaches. It packs them in boxes of 4 and fills as many boxes as it can. "
             "How many peaches are not in a box?", 230, 4, "rem", "peach", "peaches", None)
    rem_item("A teacher shares 75 pencil crayons equally among 9 tables. Each table gets as many as possible. "
             "How many pencil crayons are left over?", 75, 9, "rem", "pencil crayon", "pencil crayons", None)
    return {"title": "Word problems: buses, apples and more", "items": its}


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
        "<h2>Multiply: split the number into tens and ones</h2>"
        "<p>23 × 4 means 4 groups of 23. Each 23 is 2 tens and 3 ones. Multiply the tens, multiply the ones, then add.</p>"
        "<figure class='sn-fig'>" + groups_svg(23, 4, "4 groups of 23 in base ten blocks") +
        "<figcaption>4 groups of 23: 8 tens and 12 ones. 12 ones = 1 ten and 2 ones, so the total is 9 tens and 2 ones = 92.</figcaption></figure>"
        "<p>An <b>area model</b> shows the same thing. The rectangle is 23 long and 4 wide. Split 23 into 20 and 3.</p>"
        "<figure class='sn-fig'>" + area_1(23, 4, ["80", "12"], "area model for 23 times 4") +
        "<figcaption>20 × 4 = 80 and 3 × 4 = 12. Add the parts: 80 + 12 = 92.</figcaption></figure>"
        "<h2>Partial products and the standard method</h2>"
        "<p><b>Partial products</b> write each part on its own row, then add the rows. "
        "The <b>standard method</b> is a short way to write the same steps. Start with the ones. "
        "If you get 10 or more, write the ones digit and <b>regroup</b> the tens: write a small digit above the next place. "
        "Multiply first, then add the regrouped digit.</p>"
        "<figure class='sn-fig'>" + pp_svg(47, 6, total="282", label="47 times 6 with partial products") +
        "<figcaption>Partial products: 6 × 7 = 42 and 6 × 40 = 240. Add: 42 + 240 = 282.</figcaption></figure>"
        "<figure class='sn-fig'>" + std_svg(47, 6, "282", {1: 4}, "47 times 6 with the standard method") +
        "<figcaption>Standard method: 7 × 6 = 42, write 2, regroup 4 tens. 4 × 6 = 24, plus 4 = 28. Write 28. Answer: 282.</figcaption></figure>" +
        ex("Three digits", "236 × 4 = ?",
           "Ones: 6 × 4 = 24. Write 4, regroup 2 tens. Tens: 3 × 4 = 12, plus 2 = 14. Write 4, regroup 1 hundred. "
           "Hundreds: 2 × 4 = 8, plus 1 = 9.", "944") +
        "<p>Check with an estimate: 236 is close to 200, and 200 × 4 = 800. 944 is a bit more, so it makes sense.</p>"
        "<h2>Divide by sharing</h2>"
        "<p>52 ÷ 4 means share 52 into 4 equal groups. Share the biggest blocks first. "
        "When some are left, <b>trade</b> them for 10 of the next smaller block and keep sharing.</p>"
        "<figure class='sn-fig'>" + pile_svg(52, "base ten blocks showing 52") +
        "<figcaption>Share 5 tens: each group gets 1 ten, 1 ten is left. Trade it for 10 ones: now there are 12 ones. "
        "Share 12 ones: each group gets 3. Each group gets 1 ten and 3 ones = 13.</figcaption></figure>"
        "<p>You can also split the number into parts that divide easily. "
        "156 ÷ 4: 120 ÷ 4 = 30 and 36 ÷ 4 = 9, so 156 ÷ 4 = 39. Check by multiplying: 39 × 4 = 156.</p>"
        "<h2>Remainders</h2>"
        "<p>Sometimes there is some left that cannot make another full group. That is the <b>remainder</b>. "
        "We write it with R. The remainder is always <b>less than the number you divide by</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg(38, 5, "38 counters in groups of 5") +
        "<figcaption>38 ÷ 5 = 7 R 3: 7 full groups of 5, and 3 left over (red). Check: 7 × 5 + 3 = 38.</figcaption></figure>"
        "<h2>What does the remainder mean?</h2>" +
        table(["The question asks", "Use the remainder like this", "75 people, 9 in each shuttle bus: 75 ÷ 9 = 8 R 3"], [
            ["How many are needed for everyone?", "Add 1 to the answer", "9 buses"],
            ["How many full groups?", "Leave the remainder out", "8 full buses"],
            ["How many are left over?", "The remainder is the answer", "3 people"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting to regroup (23 × 4 = 82)", "12 ones = 1 ten and 2 ones. Add the 1 ten to the tens: 92"],
            ["Multiplying only the ones (23 × 4 = 32)", "Multiply the tens too: 20 × 4 = 80, 3 × 4 = 12, 80 + 12 = 92"],
            ["Writing 20 × 4 as 8", "20 × 4 = 2 tens × 4 = 8 tens = 80"],
            ["Ignoring the remainder (75 people need 8 buses)", "3 people are still waiting, so 9 buses are needed"],
            ["A remainder that is too big (38 ÷ 5 = 6 R 8)", "If the remainder is 5 or more, make one more group: 7 R 3"],
        ])
    )


FAQ = [
    {"q": "How do Grade 4 students in BC multiply and divide by one-digit numbers?",
     "a": "The BC curriculum asks Grade 4 students to multiply and divide two- and three-digit numbers by one-digit numbers using strategies that make sense, such as base ten blocks, area models and partial products. Many students then move on to a shorter written method."},
    {"q": "What is the area model for multiplication?",
     "a": "It is a rectangle split into parts by place value. For 23 × 4, one part is 20 × 4 = 80 and the other is 3 × 4 = 12, and the whole rectangle is 80 + 12 = 92."},
    {"q": "What does R mean in a division answer?",
     "a": "R stands for remainder, the amount left over after making equal groups. In a word problem, decide what it means: sometimes you need one more bus or box, and sometimes you leave the leftovers out."},
    {"q": "Is multiplication and division on the Grade 4 FSA?",
     "a": "The Grade 4 FSA numeracy section asks students to solve problems with numbers, so multiplying, dividing and explaining what a remainder means are useful practice. These worksheets give that practice with an answer key."},
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
    rnd = random.Random(34804)
    P = People(rnd)
    seen, used = set(), set()
    sets = [set_models(rnd, seen), set_methods(rnd, seen), set_share(rnd, used), set_rem(rnd, used, P), set_story(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "multiplying-and-dividing-by-one-digit-numbers", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing by One-Digit Numbers",
        "seo_title": "Grade 4 Multiplying and Dividing by One-Digit Numbers Worksheets: Area Models, Remainders (Free, BC Curriculum)",
        "short_title": "Multiplying and dividing by one-digit numbers",
        "domain": "Computational fluency",
        "standard_code": "Grade 4: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Multiplication and division of two- or three-digit numbers by one-digit numbers",
        "meta_desc": "Free Grade 4 math worksheets on multiplying and dividing by one-digit numbers for the BC curriculum: base ten blocks, area models, partial products, the standard method, sharing with trading, remainders and BC word problems. 100 questions with an answer key, great FSA practice.",
        "key_big": "Split the number into hundreds, tens and ones. Multiply or share each part, then put the parts together.",
        "key_sub": "23 × 4 = 20 × 4 + 3 × 4 = 80 + 12 = 92. To divide, share the biggest blocks first and trade what is left. A remainder is always less than the divisor; in a word problem, decide if you need one more.",
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
    mark_large(u, "(area model|[0-9]+ groups of|[0-9]+ counters|base ten blocks showing [0-9]{3})")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
