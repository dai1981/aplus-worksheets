# -*- coding: utf-8 -*-
"""
CA-BC Grade 5 Math: Division with remainders (BC Mathematics Curriculum, Computational fluency)
"Multiplication and division to three digits, including division with remainders."
Division facts, dividing 3-digit numbers by 1-digit numbers, remainders, what the remainder means
(round up, leave it out, share it as a fraction) and BC word problems with buses and boxes.
  python3 tools/gen_cabc_math_g5_division.py
HTML attributes use single quotes (no backslashes in the JSON). Every answer is computed in code.
BC style: Canadian English, metric, $ and ¢, no-break space from 5 digits (10 000).
"""
import json, os, random, re, math
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
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
NBSP = " "


# ------------------------------------------------------------ helpers
def f(n):
    """BC style: 4536, 10 000 (no-break space only from 5 digits)."""
    if abs(n) < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def qr(q, r):
    return "%s R %d" % (f(q), r) if r else f(q)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, num, den):
    if num == 0:
        return f(w)
    if w == 0:
        return fr(num, den)
    return "%s %s" % (f(w), fr(num, den))


def cval(c):
    """Value of a choice: '12 boxes' -> 12, '3 <fr 1/2> L' -> 7/2, '8 R 1' -> ('R', 8, 1), 'about 80' -> 80."""
    t = re.sub(r"<span class='fn'>(\d+)</span><span class='fd'>(\d+)</span>", r" \1/\2 ", c)
    t = re.sub(r"<[^>]+>", " ", t).replace("$", " ")
    m = re.match(r"^\s*(\d+) R (\d+)\s*$", t)
    if m:
        return ("R", int(m.group(1)), int(m.group(2)))
    v, found = Fraction(0), False
    for tok in t.split():
        if re.match(r"^\d+/\d+$", tok) or re.match(r"^\d+(\.\d+)?$", tok):
            v += Fraction(tok)
            found = True
    return v if found else c


def mcq(q, correct, cands, e, values=None):
    """4 choices: correct + the first 3 usable distractors (no zero or negative leads, no equal values)."""
    correct = str(correct)
    seen = {correct}
    vals = {values(correct)} if values else set()
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        if values:
            v = values(c)
            if v in vals:
                continue
            vals.add(v)
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcqv(q, correct, cands, e):
    return mcq(q, correct, cands, e, values=cval)


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


def units(k, one, many):
    return "%s %s" % (f(k), one if k == 1 else many)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def text(x, y, t, fs=18, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %s × %d + %d = %s." % (f(q), d, r, f(n))
    return "Check: %s × %d = %s." % (f(q), d, f(n))


# ------------------------------------------------------------ short division in words
def short_rows(n, d):
    """Short division: list of (digit index, number divided, quotient digit or None, amount carried)."""
    ds = [int(c) for c in str(n)]
    cur, rows, started = 0, [], False
    for i, x in enumerate(ds):
        cur = cur * 10 + x
        if not started and cur < d and i < len(ds) - 1:
            rows.append((i, cur, None, cur))
            continue
        started = True
        q, r = divmod(cur, d)
        rows.append((i, cur, q, r))
        cur = r
    return rows


def short_steps(n, d, end=True):
    """Divide each digit from the left; carry what is left to the next digit."""
    rows = short_rows(n, d)
    out = []
    for k, (i, cur, q, r) in enumerate(rows):
        last = k == len(rows) - 1
        nxt = None if last else rows[k + 1][1]
        if q is None:
            out.append("%d is less than %d, so carry it: %d." % (cur, d, nxt))
        elif last:
            out.append("%d ÷ %d = %s." % (cur, d, qr(q, r)))
        elif q == 0:
            out.append("%d is less than %d: write 0, carry %d to make %d." % (cur, d, r, nxt))
        elif r:
            out.append("%d ÷ %d = %d R %d: write %d, carry %d to make %d." % (cur, d, q, r, q, r, nxt))
        else:
            out.append("%d ÷ %d = %d: write %d." % (cur, d, q, q))
    q, r = divmod(n, d)
    if end:
        return " ".join(out) + " Answer: %s. %s" % (qr(q, r), check_txt(n, d))
    return " ".join(out)


# ------------------------------------------------------------ typical mistakes
def digitwise(n, d):
    """Each digit divided on its own, nothing carried (468 ÷ 4 -> 112)."""
    return int("".join(str(int(c) // d) for c in str(n)))


def no_zero(q):
    """The 0 inside the quotient left out (104 -> 14)."""
    s = str(q)
    return int(s.replace("0", "")) if "0" in s[1:] and s.replace("0", "") else None


def cands_div(n, d):
    q = n // d
    c = []
    z = no_zero(q)
    if z:
        c.append(z)
    dw = digitwise(n, d)
    if dw != q and dw * 2 > q:
        c.append(dw)
    c += [q * 10, q + 1, q - 1, q + 10, q - 10, q + 2]
    return [f(x) for x in c]


def cands_rem(n, d):
    q, r = divmod(n, d)
    return [qr(q - 1, r + d),          # remainder bigger than the divisor
            f(q),                      # remainder ignored
            qr(q, d - r),              # wrote how many more are needed
            qr(q + 1, r), qr(q - 1, r), qr(q * 10, r)]


# ------------------------------------------------------------ figures
def short_svg(n, d, work=False, label=None):
    """Short division: divisor, bracket and dividend. With work=True the quotient and carries are shown."""
    fs = 26
    cw = fs * 1.05
    ds = str(n)
    L = len(ds)
    x0 = 12 + fs * 0.62 + 18
    rh = fs * 1.25
    top = (rh + 8) if work else 10
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    by = top + rh - fs * 0.18
    for j, ch in enumerate(ds):
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                 "font-family='monospace'>%s</text>" % (col(j), by, fs, INK, ch))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end' "
             "font-family='monospace'>%d</text>" % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * L + 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))
    H = top + bh + 6
    if work:
        rows = short_rows(n, d)
        for k, (i, cur, q, r) in enumerate(rows):
            if q is not None:
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                         "font-family='monospace'>%d</text>" % (col(i), top - 8, fs, GREEN, q))
            if k < len(rows) - 1 and r:
                s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                         % (col(i + 1) - cw * 0.42, by - fs * 0.45, RED, r))
        q, r = divmod(n, d)
        if r:
            rt = "R %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' font-family='monospace'>%s</text>"
                     % (x0 + cw * L + 10, top - 8, fs, GREEN, rt))
            W = max(W, x0 + cw * L + 10 + len(rt) * fs * 0.62 + 6)
    lab = label or ("%d divided by %d worked out with short division" if work else "%d divided by %d written as short division") % (n, d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), lab)


def area_svg(side, tops, inside, label):
    """Area model: divisor on the left, the dividend split into parts. tops = partial quotients ('?' red)."""
    FS = 18
    ws = [max(64, len(str(tops[k])) * FS * 0.6 + 20, len(str(inside[k])) * FS * 0.6 + 20) for k in range(len(tops))]
    x0, y0, h = 34, 30, 58
    s = []
    x = x0
    for k, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y0, w, h, FILL, GREEN))
        s.append(text(x + w / 2, y0 + h / 2 + 6, inside[k], FS))
        s.append(text(x + w / 2, y0 - 9, tops[k], FS, col=RED if tops[k] == "?" else GREEN))
        x += w
    s.append(text(x0 - 15, y0 + h / 2 + 6, str(side), FS, col=GREEN))
    return svg_wrap(int(x + 4), y0 + h + 4, "".join(s), label)


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
    return svg_wrap(int(x), int(d * gap + 8), "".join(s), label or "%d counters in groups of %d" % (n, d))


def array_svg(rows, cols, label=None):
    R, gap = 7, 20
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (6 + R + j * gap, 6 + R + i * gap, R, GREEN))
    return svg_wrap(int(12 + 2 * R + (cols - 1) * gap), int(12 + 2 * R + (rows - 1) * gap), "".join(s),
                    label or "array of %d rows of %d dots" % (rows, cols))


def pizza_svg(n, d, label=None):
    """n round pizzas; the leftover ones (n mod d) are cut into d equal slices."""
    q, r = divmod(n, d)
    R = 19
    s = []
    for k in range(n):
        cx, cy = 6 + R + k * (2 * R + 8), 6 + R
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, FILL, GREEN))
        if k >= n - r:
            for j in range(d):
                a = -math.pi / 2 + 2 * math.pi * j / d
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
                         % (cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), RED))
    W = 12 + n * (2 * R) + (n - 1) * 8
    return svg_wrap(int(W), 2 * R + 12, "".join(s), label or "%d pizzas, the last %d cut into %d equal slices" % (n, r, d))


# ------------------------------------------------------------ set 1: division facts
def set_facts():
    its = []
    for n, d in [(63, 9), (48, 6), (56, 8), (42, 7), (72, 8), (54, 9), (36, 4), (81, 9)]:
        q = n // d
        its.append(mcq("What is %d ÷ %d?" % (n, d), str(q), [str(q + 1), str(q - 1), str(q + 2), str(d), str(n - d)],
                       "Think multiplication: %d × ? = %d. %d × %d = %d, so %d ÷ %d = %d." % (d, n, d, q, n, n, d, q)))
    for d, q in [(6, 8), (7, 9)]:
        n = d * q
        its.append(mcq("Find the missing number: ? ÷ %d = %d" % (d, q), str(n),
                       [str(d + q), str(n - d), str(n + d), str(q - d) if q > d else None],
                       "The missing number is the total. Multiply: %d × %d = %d. Check: %d ÷ %d = %d. "
                       "Adding %d + %d = %d is a common mistake." % (q, d, n, n, d, q, d, q, d + q)))
    for n, q in [(72, 9), (48, 8)]:
        d = n // q
        its.append(mcq("Find the missing number: %d ÷ ? = %d" % (n, q), str(d),
                       [str(d + 1), str(d - 1), str(n - q), str(q)],
                       "Ask: what number times %d makes %d? %d × %d = %d, so %d ÷ %d = %d." % (q, n, d, q, n, n, d, q)))
    for n, d in [(64, 8), (49, 7)]:
        q = n // d
        its.append(mcq("Which multiplication fact helps you find %d ÷ %d?" % (n, d), "%d × %d = %d" % (q, d, n),
                       ["%d × %d = %d" % (q - 1, d, (q - 1) * d), "%d × %d = %d" % (q + 1, d, (q + 1) * d),
                        "%d + %d = %d" % (n, d, n + d)],
                       "Division undoes multiplication. %d × %d = %d, so %d ÷ %d = %d." % (q, d, n, n, d, q)))
    its.append(mcq("Which is NOT in the fact family for 6, 7 and 42?", "6 ÷ 42 = 7",
                   ["42 ÷ 6 = 7", "7 × 6 = 42", "42 ÷ 7 = 6"],
                   "In a division fact the total, 42, comes first: 42 ÷ 6 = 7 and 42 ÷ 7 = 6. "
                   "6 ÷ 42 divides the wrong way, so it is not in the fact family."))
    for n, d in [(420, 7), (360, 4), (240, 3), (280, 7)]:
        q = n // d
        its.append(mcq("Use a fact to find %d ÷ %d." % (n, d), str(q), [str(q // 10), str(q * 10), str(q + 10), str(q - 10)],
                       "%d is %d tens. %d tens ÷ %d = %d tens, which is %d. Check: %d × %d = %d."
                       % (n, n // 10, n // 10, d, q // 10, q, q, d, n)))
    rows, cols = 6, 9
    its.append(mcq(fig(array_svg(rows, cols)) + "These 54 chairs are set out in 6 equal rows. How many chairs are in each row?",
                   "9", ["6", "8", "48"],
                   "The array has 6 equal rows. 54 ÷ 6 = 9, so each row has 9 chairs. Check: 6 × 9 = 54."))
    return {"title": "Division facts", "items": its}


# ------------------------------------------------------------ set 2: 3-digit by 1-digit, no remainder
def set_three_digit():
    its = []
    for n, d in [(468, 4), (735, 5), (852, 6), (296, 8), (581, 7), (912, 3)]:
        assert n % d == 0
        its.append(mcq(fig(short_svg(n, d)) + "Divide.", f(n // d), cands_div(n, d), short_steps(n, d)))
    for n, d in [(624, 6), (945, 9), (384, 8), (672, 4)]:
        assert n % d == 0
        its.append(mcq("What is %d ÷ %d?" % (n, d), f(n // d), cands_div(n, d), short_steps(n, d)))
    for n, d in [(552, 4), (738, 6), (847, 7)]:
        ps, rest = [], n
        for scale in (100, 10):
            k = (rest // scale) // d * d * scale
            if k:
                ps.append(k)
                rest -= k
        if rest:
            ps.append(rest)
        assert sum(ps) == n and all(p % d == 0 for p in ps)
        pq = [p // d for p in ps]
        q = n // d
        svg = area_svg(d, ["?"] * len(ps), [f(p) for p in ps], "area model for %d divided by %d" % (n, d))
        e = ("The model splits %d into %s. Divide each part by %d: %s. Add: %s = %d. %s"
             % (n, " + ".join(f(p) for p in ps), d, ", ".join("%d ÷ %d = %d" % (p, d, x) for p, x in zip(ps, pq)),
                " + ".join(str(x) for x in pq), q, check_txt(n, d)))
        its.append(mcq(fig(svg) + "Use the area model to find %d ÷ %d." % (n, d), f(q),
                       [f(q - pq[-1]), f(q * 10), f(q + 10), f(q + 1)], e))
    for n, d, near in [(487, 6, 480), (358, 9, 360)]:
        est = near // d
        e = ("Find a number close to %d that is easy to divide by %d: %d. %d ÷ %d = %d (think %d ÷ %d = %d). "
             "So %d ÷ %d is about %d." % (n, d, near, near, d, est, near // 10, d, est // 10, n, d, est))
        its.append(mcqv("Which is the best estimate for %d ÷ %d?" % (n, d), "about %d" % est,
                        ["about %d" % (est // 10), "about %d" % (est * 10), "about %d" % (est + 10)], e))
    for n, d in [(816, 4), (648, 3)]:
        q = n // d
        its.append(mcq("Which multiplication checks that %d ÷ %d = %d?" % (n, d, q), "%d × %d = %d" % (q, d, n),
                       ["%d × %d = %d" % (n, d, n * d), "%d × %d = %d" % (d, d, d * d), "%d + %d = %d" % (q, d, q + d)],
                       "Multiply the answer by the number you divided by: %d × %d = %d. That is the number you started with, "
                       "so the answer is right." % (q, d, n)))
    its.append(mcq("Owen says 618 ÷ 6 = 13. What mistake did he make?", "He left out the 0 in the tens place",
                   ["He divided the wrong way", "He ignored a remainder", "There is no mistake"],
                   "6 ÷ 6 = 1. Then 1 is less than 6, so write 0 in the tens place and carry 1 to make 18. "
                   "18 ÷ 6 = 3. The answer is 103, not 13. Check: 103 × 6 = 618."))
    its.append(mcq("How many digits does the answer to 256 ÷ 8 have?", "2 digits", ["3 digits", "1 digit", "4 digits"],
                   "2 is less than 8, so there are no hundreds in the answer. Start with 25: 25 ÷ 8 = 3 R 1, carry 1 to make 16. "
                   "16 ÷ 8 = 2. 256 ÷ 8 = 32, which has 2 digits."))
    opts = [(312, 4), (314, 4), (310, 4), (315, 4)]
    e = "Divide each one: " + "; ".join("%d ÷ 4 = %s" % (n, qr(*divmod(n, 4))) for n, _ in opts) + \
        ". Only 312 ÷ 4 = 78 has no remainder. Check: 78 × 4 = 312."
    its.append(mcq("Which division has no remainder?", "312 ÷ 4", ["314 ÷ 4", "310 ÷ 4", "315 ÷ 4"], e))
    return {"title": "Divide 3-digit numbers by 1-digit numbers", "items": its}


# ------------------------------------------------------------ set 3: remainders
def pick_rem(rnd, used, lo, hi, dlo=3, dhi=9):
    while True:
        d = rnd.randint(dlo, dhi)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if r == 0 or n in used or q < 10 or "0" in str(q) or r == q % 10 or q % 10 == d - r:
            continue
        used.add(n)
        return n, d


def set_remainders(rnd, used, P):
    its = []
    for n, d in [(26, 4), (31, 6), (29, 5)]:
        used.add(n)
        q, r = divmod(n, d)
        e = ("There are %d full groups of %d and %s left over (in red). %d is less than %d, so it cannot make another group. "
             "%d ÷ %d = %s. %s" % (q, d, units(r, "counter", "counters"), r, d, n, d, qr(q, r), check_txt(n, d)))
        its.append(mcq(fig(dots_svg(n, d)) + "The picture shows %d counters in groups of %d. What is %d ÷ %d?" % (n, d, n, d),
                       qr(q, r), cands_rem(n, d), e))
    for i in range(8):
        n, d = pick_rem(rnd, used, 41, 98) if i < 2 else pick_rem(rnd, used, 112, 989)
        q, r = divmod(n, d)
        qq = (fig(short_svg(n, d)) + "Divide.") if i % 2 == 1 else "What is %d ÷ %d?" % (n, d)
        cands = cands_rem(n, d)
        dw = digitwise(n, d)
        if dw != q and int(str(n)[0]) >= d:
            cands.insert(1, qr(dw, r))
        its.append(mcq(qq, qr(q, r), cands, short_steps(n, d)))
    for _ in range(2):
        n, d = pick_rem(rnd, used, 120, 980, 4)
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), str(r),
                       [f(q), str(d - r), str(r + d), str(d)],
                       "The question asks for the remainder, not the quotient. " + short_steps(n, d)))
    for _ in range(2):
        n, d = pick_rem(rnd, used, 120, 980)
        q, r = divmod(n, d)
        its.append(mcq("%d ÷ %d = %s. Which expression checks this answer? It should equal %d." % (n, d, qr(q, r), n),
                       "%d × %d + %d" % (q, d, r),
                       ["%d × %d − %d" % (q, d, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (q, d, r)],
                       "Multiply the quotient by the divisor, then add the remainder: %d × %d = %d, %d + %d = %d. "
                       "It matches, so the answer is right." % (q, d, q * d, q * d, r, n)))
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick_rem(rnd, used, 50, 99, 4, 8)
        q, r = divmod(n, d)
        its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he),
                       "The remainder is too big",
                       ["%s ignored the remainder" % cap(he), "%s divided the wrong way" % cap(he), "There is no mistake"],
                       "The remainder must be less than the divisor. %d is not less than %d, so one more group of %d fits: "
                       "%d − %d = %d. The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    name, he, his = P.next()
    its.append(mcq("%s says 47 ÷ 5 = 9. What mistake did %s make?" % (name, he),
                   "%s ignored the remainder" % cap(he),
                   ["The remainder is too big", "%s divided the wrong way" % cap(he), "There is no mistake"],
                   "9 × 5 = 45, and 47 − 45 = 2. The 2 left over is part of the answer: 47 ÷ 5 = 9 R 2."))
    its.append(mcq("You divide a number by 6. Which of these could be the remainder?", "5", ["6", "7", "9"],
                   "A remainder is always less than the divisor. When you divide by 6, the remainder can only be 0 to 5. "
                   "So 5 is the only possible one."))
    q, d, r = 47, 5, 3
    n = q * d + r
    its.append(mcq("In a division, the quotient is 47, the divisor is 5 and the remainder is 3. What number was divided?",
                   str(n), [str(q * d), str(q * d - r), str(q + d + r), str(q * d + d)],
                   "Work backwards: multiply, then add the remainder. 47 × 5 = 235, and 235 + 3 = 238. "
                   "Check: 238 ÷ 5 = 47 R 3."))
    return {"title": "Division with remainders", "items": its}


# ------------------------------------------------------------ set 4: what the remainder means
def frac_item(t, n, d, one, many, figure=False, measure=False):
    """Share n things among d; the leftovers are cut. Answer as a mixed number."""
    q, r = divmod(n, d)
    assert r and q >= 1 and gcd(r, d) == 1
    if measure:
        U = lambda s: s + " " + many
    else:
        U = lambda s: s + " " + (one if s == "1" else many)
    ans = U(mixed(q, r, d))
    cands = [U("%d.%d" % (q, r)), U(f(q)), U(mixed(q, r, n)) if r < n else None, U(mixed(q, 1, d)) if r > 1 else None,
             U(mixed(q, d - r, d)) if d - r != r else None, U(f(q + 1)), U(mixed(q, 1, r)) if r > 1 else None]
    word = one if not measure else ("metre" if many == "m" else "litre")
    if r == 1:
        how = ("%d ÷ %d = %d R 1. Each gets %s. The 1 %s left over is cut into %d equal parts, so each gets %s more. "
               % (n, d, q, U(f(q)), word, d, fr(1, d)))
    else:
        how = ("%d ÷ %d = %d R %d. Each gets %s. The %d %ss left over are shared too: %d ÷ %d = %s more each. "
               % (n, d, q, r, U(f(q)), r, word, r, d, fr(r, d)))
    e = how + "Answer: %s. (The remainder is not a decimal: %d R %d is not %d.%d.)" % (ans, q, r, q, r)
    return mcqv((fig(pizza_svg(n, d)) if figure else "") + t, ans, cands, e)


def up_item(t, n, d, one, many, who, who1):
    q, r = divmod(n, d)
    ans = units(q + 1, one, many)
    e = ("%d ÷ %d = %s. %s are not enough: %s still %s room. Round up to %s."
         % (n, d, qr(q, r), cap(units(q, one, many)), units(r, who1, who), "needs" if r == 1 else "need", ans))
    return mcqv(t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e)


def down_item(t, n, d, one, many, why):
    q, r = divmod(n, d)
    ans = units(q, one, many)
    e = "%d ÷ %d = %s. %s Leave the remainder out: the answer is %s." % (n, d, qr(q, r), why, ans)
    return mcqv(t, ans, [units(q + 1, one, many), qr(q, r), units(r, one, many), units(q - 1, one, many)], e)


def left_item(t, n, d, one, many):
    q, r = divmod(n, d)
    ans = units(r, one, many)
    e = ("%d ÷ %d = %s (%d × %d = %d, %d − %d = %d). The question asks how many are left over, so the answer is the remainder: %s."
         % (n, d, qr(q, r), q, d, q * d, n, q * d, r, ans))
    return mcqv(t, ans, [units(q, one, many), units(d - r, one, many), qr(q, r), units(d, one, many)], e)


def set_meaning():
    its = []
    its.append(up_item("61 campers sleep in tents on Vancouver Island. Each tent sleeps 4 campers. How many tents are needed?",
                       61, 4, "tent", "tents", "campers", "camper"))
    its.append(up_item("A class of 27 students goes kayaking. Each kayak holds 2 students. How many kayaks are needed?",
                       27, 2, "kayak", "kayaks", "students", "student"))
    its.append(up_item("Hana has 75 photos for an album. Each page holds 6 photos. How many pages does she need for all of them?",
                       75, 6, "page", "pages", "photos", "photo"))
    its.append(up_item("A library is moving 130 books. Each box holds 8 books. How many boxes are needed to move all the books?",
                       130, 8, "box", "boxes", "books", "book"))
    its.append(up_item("209 people come to a school concert. Each row has 9 chairs. How many rows are needed so everyone has a seat?",
                       209, 9, "row", "rows", "people", "person"))
    its.append(down_item("Ava has 50 cookies. She packs them in boxes of 8. How many boxes can she fill?",
                         50, 8, "box", "boxes", "The 2 cookies left over cannot fill another box."))
    its.append(down_item("Ethan has $45. A movie ticket costs $7. How many tickets can he buy?",
                         45, 7, "ticket", "tickets", "6 tickets cost $42. The $3 left over is not enough for another ticket."))
    its.append(down_item("44 players come to a lacrosse day. The coach puts them in teams of 6. How many full teams can she make?",
                         44, 6, "team", "teams", "The 2 players left over are not enough for another team."))
    its.append(down_item("Wei cuts a 100 cm ribbon into pieces that are each 8 cm long. How many 8 cm pieces can he cut?",
                         100, 8, "piece", "pieces", "The 4 cm left over is too short for another piece."))
    its.append(down_item("A gardener plants 157 tulip bulbs in rows of 9. How many full rows can she plant?",
                         157, 9, "row", "rows", "The 4 bulbs left over cannot make a full row."))
    its.append(frac_item("5 pizzas are shared equally by 2 friends. The leftover pizza is cut in half. How many pizzas does each friend get?",
                         5, 2, "pizza", "pizzas", figure=True))
    its.append(frac_item("9 muffins are shared equally by 4 students. How many muffins does each student get?",
                         9, 4, "muffin", "muffins"))
    its.append(frac_item("11 granola bars are shared equally by 3 hikers. How many granola bars does each hiker get?",
                         11, 3, "granola bar", "granola bars"))
    its.append(left_item("Zara has 67 beads. She puts 8 beads on each bracelet and makes as many bracelets as she can. "
                         "How many beads are left over?", 67, 8, "bead", "beads"))
    its.append(left_item("A teacher shares 94 pencil crayons equally among 6 tables. Each table gets as many as possible. "
                         "How many pencil crayons are left over?", 94, 6, "pencil crayon", "pencil crayons"))
    pool = ["7 pizzas shared by 4", "30 people, 4 per canoe", "Full packs of 6 from 40", "Cards left when 50 go to 6"]
    for ask, k, e in [
        ("In which story should you round up to the next whole number?", 1,
         "30 ÷ 4 = 7 R 2. With 7 canoes, 2 people still need a seat, so you need 8 canoes. Round up when everyone must fit."),
        ("In which story does it make sense to write the remainder as a fraction?", 0,
         "7 ÷ 4 = 1 R 3. A pizza can be cut, so the 3 leftover pizzas are shared too: each person gets 1 " + fr(3, 4) +
         " pizzas. People, packs and cards cannot be cut."),
        ("In which story should you leave the remainder out?", 2,
         "40 ÷ 6 = 6 R 4. The 4 left over cannot make a full pack, so the answer is 6 packs. The remainder is left out."),
    ]:
        its.append(mcq(ask, pool[k], [p for i, p in enumerate(pool) if i != k], e))
    its.append(mcq("Liam packs 38 muffins in boxes of 6: 38 ÷ 6 = 6 R 2. What does the 2 mean?",
                   "2 muffins are not in a box",
                   ["2 boxes are not full", "Each box gets 2 more", "He needs 2 more boxes"],
                   "6 boxes hold 6 × 6 = 36 muffins. 38 − 36 = 2, so the R 2 means 2 muffins are left without a box."))
    its.append(mcq("45 students ride in vans that hold 7 students each: 45 ÷ 7 = 6 R 3. What does the 3 mean?",
                   "3 students still need a seat",
                   ["3 vans are needed", "3 seats are empty in each van", "Each van holds 3 more"],
                   "6 vans hold 6 × 7 = 42 students. 45 − 42 = 3 students do not fit, so a 7th van is needed."))
    return {"title": "What the remainder means", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(P):
    its = []
    D = lambda v: "$" + f(v)
    nm, he, his = P.next()
    for t, n_, d, fm in [
        ("4 Grade 5 classes in Surrey raise $456 for the Terry Fox Run. Each class raises the same amount. How much does each class raise?",
         456, 4, D),
        ("An orchard in Kelowna packs 864 apples into 8 crates, with the same number in each crate. How many apples are in each crate?",
         864, 8, lambda v: "%s apples" % f(v)),
        ("A theatre in Vancouver has 675 seats in 5 equal sections. How many seats are in each section?",
         675, 5, lambda v: "%s seats" % f(v)),
        ("%s reads a 312-page book in 8 days. %s reads the same number of pages each day. How many pages does %s read each day?"
         % (nm, cap(he), he), 312, 8, lambda v: "%s pages" % f(v)),
        ("A cedar fence is 448 cm long. It is made of 7 panels that are all the same length. How long is each panel?",
         448, 7, lambda v: "%s cm" % f(v)),
    ]:
        assert n_ % d == 0
        e = "Share equally, so divide: %d ÷ %d. " % (n_, d) + short_steps(n_, d) + " So the answer is %s." % fm(n_ // d)
        cands = [fm(int(x)) for x in cands_div(n_, d)]
        its.append(mcq(t, fm(n_ // d), cands, e))
    for t, n, d, one, many, who, who1 in [
        ("93 students and adults go on a field trip to Grouse Mountain. Each van holds 8 people. How many vans are needed?",
         93, 8, "van", "vans", "people", "person"),
        ("29 students go canoeing on the Fraser River. Each canoe holds 3 students. How many canoes are needed?",
         29, 3, "canoe", "canoes", "students", "student"),
        ("125 hockey players travel to a tournament in Kamloops. Each minibus holds 9 players. How many minibuses are needed?",
         125, 9, "minibus", "minibuses", "players", "player"),
        ("155 skiers wait for the gondola at Whistler. Each gondola cabin carries 8 skiers. How many cabins are needed to take everyone up?",
         155, 8, "cabin", "cabins", "skiers", "skier"),
    ]:
        its.append(up_item(t, n, d, one, many, who, who1))
    its.append(down_item("A bakery in Nanaimo makes 154 Nanaimo bars. It packs them in boxes of 6. How many boxes can it fill?",
                         154, 6, "box", "boxes", "The 4 bars left over cannot fill another box."))
    nm, he, his = P.next()
    its.append(down_item("%s has 230 hockey cards. Each page of %s binder holds 9 cards. How many pages can %s fill?" % (nm, his, he),
                         230, 9, "page", "pages", "The 5 cards left over cannot fill another page."))
    its.append(down_item("A farm in the Fraser Valley packs 427 jars of honey in boxes of 8. How many boxes can it fill?",
                         427, 8, "box", "boxes", "The 3 jars left over cannot fill another box."))
    its.append(left_item("A teacher shares 250 stickers equally among 7 groups. Each group gets as many as possible. "
                         "How many stickers are left over?", 250, 7, "sticker", "stickers"))
    nm, he, his = P.next()
    its.append(left_item("%s puts 185 photos in an album, 4 on each page. How many photos are on the last page, which is not full?" % nm,
                         185, 4, "photo", "photos"))
    its.append(frac_item("At a class party, 11 pizzas are shared equally by 4 tables. How many pizzas does each table get?",
                         11, 4, "pizza", "pizzas"))
    its.append(frac_item("A 13 m rope is cut into 4 equal pieces for a climbing class. How long is each piece?",
                         13, 4, "metre", "m", measure=True))
    its.append(mcq("A school buys 4 boxes of 36 freezies. The freezies are shared equally among 6 classes. How many freezies does each class get?",
                   "24 freezies", ["144 freezies", "6 freezies", "36 freezies"],
                   "Step 1: 4 × 36 = 144 freezies. Step 2: 144 ÷ 6 = 24 (14 ÷ 6 = 2 R 2, carry 2 to make 24; 24 ÷ 6 = 4). "
                   "Each class gets 24 freezies."))
    nm, he, his = P.next()
    its.append(mcq("%s has $120. %s spends $36 on a Canucks T-shirt, then shares the rest equally among 4 charities. How much does each charity get?"
                   % (nm, cap(he)), "$21", ["$84", "$30", "$39"],
                   "Step 1: $120 − $36 = $84. Step 2: $84 ÷ 4 = $21. Each charity gets $21. "
                   "($120 ÷ 4 = $30 forgets to take away the $36 first.)"))
    its.append(mcqv("Two Grade 5 classes have 28 and 31 students. They go to Stanley Park in vans that hold 8 students each. How many vans are needed?",
                    "8 vans", ["7 vans", "7 R 3", "4 vans"],
                    "Step 1: 28 + 31 = 59 students. Step 2: 59 ÷ 8 = 7 R 3. 7 vans hold 56 students, and 3 students still need a seat, "
                    "so round up to 8 vans."))
    its.append(mcq("315 students are put into 9 equal teams for Sports Day. Which number sentence finds the number of students on each team?",
                   "315 ÷ 9 = 35", ["9 ÷ 315 = 35", "315 × 9 = 2835", "315 − 9 = 306"],
                   "You know the total (315) and the number of teams (9), so divide: 315 ÷ 9 = 35. "
                   "9 ÷ 315 divides the wrong way. Check: 35 × 9 = 315."))
    return {"title": "Word problems: buses, boxes and more", "items": its}


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
        "<h2>Division facts</h2>"
        "<p>Division splits a total into equal groups. Every division fact has a multiplication fact behind it. "
        "To find 54 ÷ 6, ask: 6 times what makes 54? 6 × 9 = 54, so 54 ÷ 6 = 9.</p>"
        "<p>Facts also help with tens: 420 ÷ 7 is 42 tens ÷ 7 = 6 tens = 60.</p>"
        "<h2>Divide a 3-digit number by a 1-digit number</h2>"
        "<p>Divide one digit at a time, starting on the left. Write each answer digit on top. "
        "If something is left, carry it to the next digit.</p>"
        "<figure class='sn-fig'>" + short_svg(157, 4, True, "157 divided by 4 worked out with short division") +
        "<figcaption>1 is less than 4, so carry it: 15. 15 ÷ 4 = 3 R 3: write 3, carry 3 to make 37. "
        "37 ÷ 4 = 9 R 1. Answer: 39 R 1. Check: 39 × 4 + 1 = 157.</figcaption></figure>" +
        ex("A 0 in the answer", "What is 618 ÷ 6?",
           "6 ÷ 6 = 1. Next, 1 is less than 6: write 0 and carry 1 to make 18. 18 ÷ 6 = 3.", "103 (not 13)") +
        "<h2>Remainders</h2>"
        "<p>The <b>remainder</b> is what is left when no more full groups can be made. We write it with R. "
        "The remainder is always <b>less than the number you divide by</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg(23, 5, "23 counters in groups of 5") +
        "<figcaption>23 ÷ 5 = 4 R 3: 4 full groups of 5, and 3 left over (red). Check: 4 × 5 + 3 = 23.</figcaption></figure>"
        "<h2>What the remainder means</h2>"
        "<p>In a word problem, the answer is not always “4 R 3”. Read the question and decide what to do with the remainder.</p>" +
        table(["The question asks", "Do this", "Example"], [
            ["Everyone or everything must fit", "Round up: add 1", "45 students, 7 per van: 7 vans"],
            ["How many full groups?", "Leave the remainder out", "50 cookies, boxes of 8: 6 boxes"],
            ["The leftovers can be shared", "Write a fraction", "5 pizzas, 2 friends: 2 " + fr(1, 2) + " each"],
            ["How many are left over?", "The remainder is the answer", "67 beads, 8 per bracelet: 3 left"],
        ]) +
        "<figure class='sn-fig'>" + pizza_svg(5, 2, "5 pizzas, the last one cut in half") +
        "<figcaption>5 pizzas shared by 2 friends: 5 ÷ 2 = 2 R 1. Cut the last pizza in half. "
        "Each friend gets 2 " + fr(1, 2) + " pizzas.</figcaption></figure>" +
        ex("Field trip", "93 people go to Grouse Mountain. Each van holds 8 people. How many vans are needed?",
           "93 ÷ 8 = 11 R 5. 11 vans hold 88 people, and 5 people still need a seat. Add 1 more van.", "12 vans") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Ignoring the remainder (47 ÷ 5 = 9)", "Write what is left: 47 ÷ 5 = 9 R 2"],
            ["A remainder bigger than the divisor (29 ÷ 4 = 6 R 5)", "If the remainder is 4 or more, make one more group: 7 R 1"],
            ["Leaving out a 0 (618 ÷ 6 = 13)", "When a digit is too small, write 0 and carry: 103"],
            ["Not carrying (468 ÷ 4 = 112)", "Carry what is left to the next digit: 117"],
            ["Writing R as a decimal (5 ÷ 2 = 2.1)", "2 R 1 means 1 left of 2: 2 " + fr(1, 2)],
            ["45 students need 6 vans", "3 students are still waiting, so 7 vans are needed"],
        ])
    )


FAQ = [
    {"q": "What division do Grade 5 students learn in BC?",
     "a": "The BC Grade 5 curriculum includes multiplication and division to three digits, including division with remainders. Students divide numbers like 745 ÷ 6 and decide what the remainder means in a word problem."},
    {"q": "What does R mean in a division answer?",
     "a": "R stands for remainder: the amount left over after making equal groups. 23 ÷ 5 = 4 R 3 means 4 groups of 5 with 3 left over, and the remainder is always less than the divisor."},
    {"q": "When do you round up in a division word problem?",
     "a": "Round up when everyone or everything must fit, such as students on buses or books in boxes. 45 students in vans of 7 is 6 R 3, so 7 vans are needed."},
    {"q": "How can my child check a division answer?",
     "a": "Multiply the answer by the divisor, then add the remainder. For 157 ÷ 4 = 39 R 1, 39 × 4 + 1 = 157, so the answer is right."},
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
    rnd = random.Random(55807)
    P = People(rnd)
    used = set()
    sets = [set_facts(), set_three_digit(), set_remainders(rnd, used, P), set_meaning(), set_story(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "division-with-remainders", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Division with Remainders",
        "seo_title": "Grade 5 Division with Remainders Worksheets: Facts, 3-Digit Division, Word Problems (Free, BC Curriculum)",
        "short_title": "Division with remainders",
        "domain": "Computational fluency",
        "standard_code": "Grade 5: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Multiplication and division to three digits, including division with remainders",
        "meta_desc": "Free Grade 5 math worksheets on division with remainders for the BC curriculum: division facts, dividing 3-digit numbers by 1-digit numbers, remainders, what the remainder means and word problems with buses and boxes. 100 questions with an answer key.",
        "key_big": "Divide one digit at a time and carry what is left. The remainder is always less than the number you divide by.",
        "key_sub": "157 ÷ 4 = 39 R 1. Check: 39 × 4 + 1 = 157. In a word problem, decide what the remainder means: round up (one more bus), leave it out (full boxes only) or share it as a fraction.",
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
    mark_large(u, "(area model|[0-9]+ counters|[0-9]+ pizzas|array of)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
