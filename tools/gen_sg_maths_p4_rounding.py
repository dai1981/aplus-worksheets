# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Rounding and Estimation
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 4: Whole Numbers —
 rounding numbers to the nearest 10, 100 or 1000; use of ≈)
  python3 tools/gen_sg_maths_p4_rounding.py
Numbers up to 100 000. 4-digit numbers have no separator (4536); 5 digits use a no-break space (54 728).
Round half up (4500 -> 5000). Estimate sums, differences and products with ≈, and word problems with bar models.
Wrong answers come from real mistakes: rounding the wrong way (4500 rounded down to 4000), rounding to the wrong
place, rounding in two steps (3449 -> 3450 -> 3500), always rounding down, keeping the digits after the rounding
place, and losing or mis-writing the renamed 1 when a 9 rounds up (2965 -> 2000 or 21 000).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
NB = " "

LOOK = {10: "ones", 100: "tens", 1000: "hundreds"}          # digit to look at
OWN = {10: "tens", 100: "hundreds", 1000: "thousands"}      # digit that is rounded
NEXT1 = {10: "hundred", 100: "thousand", 1000: "ten thousand"}


# ------------------------------------------------------------ helpers
def n(x):
    """MOE style: 4536, 10 000, 54 728 (no-break spaces, never commas)."""
    assert x == int(x) and x >= 0, x
    s = str(int(x))
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


def unit(pre="", post=""):
    return lambda v: pre + n(v) + post


def mcq_r(q, correct, cands, e, fmt=n):
    """Number choices: the first 3 different wrong values from cands (most likely mistake first)."""
    pick = []
    for v in cands:
        if v is None or v <= 0 or v > 100000 or v == correct or v in pick:
            continue
        pick.append(v)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return mcq(q, fmt(correct), [fmt(v) for v in pick], e)


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


def lg(p):
    return len(str(p)) - 1


# ------------------------------------------------------------ figures
def number_line_svg(lo, hi, x, step):
    """Number line lo..hi, a tick every step, labels at both ends and the halfway point, red dot on x."""
    L, R, Y = 50, 390, 50
    W, H = 440, 92
    span = hi - lo
    mid = lo + span // 2

    def X(v):
        return L + (v - lo) * (R - L) / float(span)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in (lo, mid, hi)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (11 if big else 6), X(v), Y + (11 if big else 6), INK, "2" if big else "1.2"))
        if big:
            s.append(text(X(v), Y + 32, n(v), 15, bold=True, col=GREEN if v != mid else GREY))
        v += step
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(x), Y, RED))
    tx = min(max(X(x), 40), W - 40)
    s.append(text(tx, Y - 19, n(x), 16, bold=True, col=RED))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (n(lo), n(hi)))


def line_for(x, p):
    lo = x // p * p
    return fig(number_line_svg(lo, lo + p, x, p // 10))


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


# ------------------------------------------------------------ rounding
def round_to(x, p):
    return ((x + p // 2) // p) * p


assert round_to(4500, 1000) == 5000 and round_to(4499, 1000) == 4000 and round_to(85, 10) == 90
assert round_to(2965, 100) == 3000 and round_to(3449, 100) == 3400


def two_step(x, p):
    """Rounding in steps: 3449 -> 3450 -> 3500 (nearest 100)."""
    v = x
    q = 10
    while q <= p:
        v = round_to(v, q)
        q *= 10
    return v


def round_expl(x, p, fmt=n):
    """Short explanation of rounding x to the nearest p (10, 100 or 1000)."""
    lo = x // p * p
    r = round_to(x, p)
    d = digit(x, lg(p) - 1)
    if x - lo == p // 2:
        s = ("%s is exactly halfway between %s and %s. A number exactly halfway rounds up."
             % (n(x), n(lo), n(lo + p)))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. It is %s, so round %s."
             % (n(x), n(lo), n(lo + p), LOOK[p], d,
                "5 or more" if d >= 5 else "4 or less", "up" if r > lo else "down"))
    if r > lo and digit(x, lg(p)) == 9:
        s += (" The %s digit is 9, so rounding up makes 10 %s. Rename 10 %s as 1 %s: %s + %s = %s."
              % (OWN[p], OWN[p], OWN[p], NEXT1[p], n(lo), n(p), n(r)))
    ts = two_step(x, p)
    if ts != r:
        s += (" Do not round in two steps (%s → %s → %s). Round the number you started with."
              % (n(x), n(round_to(x, p // 10 if p > 10 else 10)), n(ts)))
    return s + " So %s ≈ %s." % (n(x), fmt(r)) if fmt is n else s + " Answer: %s." % fmt(r)


def nine_mistakes(x, p):
    """When a 9 rounds up: writing “10” in one place (2965 -> 21 000) or forgetting to rename (2965 -> 2000)."""
    r = round_to(x, p)
    lo = x // p * p
    if r == lo or digit(x, lg(p)) != 9:
        return []
    pre = x // (p * 10)
    out = [pre * p * 10]
    if pre:
        out.insert(0, int(str(pre) + "10" + "0" * lg(p)))
    return out


def round_cands(x, p):
    """Wrong answers from real mistakes, most likely first."""
    r = round_to(x, p)
    lo = x // p * p
    other = lo + p if r == lo else lo                 # rounded the wrong way (4500 -> 4000)
    out = [two_step(x, p), other] + nine_mistakes(x, p)
    if r > lo:
        out.append(r + x % p)                         # kept the digits after the place (3462 -> 3562)
    if p >= 100:
        out.append(round_to(x, p // 10))              # rounded to the place on the right (3460)
        out.append(x // (p // 10) * (p // 10))        # cut off at the wrong place (3400)
    out.append(round_to(x, p * 10))                   # rounded to the place on the left
    out.append(x // (p * 10) * (p * 10))
    out += [r + p, r - p, x]
    return out


class Picker:
    def __init__(self, rnd):
        self.rnd = rnd
        self.used = set()

    def take(self, x):
        assert x not in self.used, x
        self.used.add(x)
        return x

    def pick(self, lo, hi, p):
        """A number in [lo, hi]: not a multiple of 10, not halfway, no 9 in the rounding place, not used."""
        while True:
            x = self.rnd.randint(lo, hi)
            if (x % 10 and x % p != p // 2 and digit(x, lg(p)) != 9 and two_step(x, p) == round_to(x, p)
                    and x not in self.used and round_to(x, p) > 0):
                self.used.add(x)
                return x


def q_round(x, p, line=False, box=False):
    if box:
        q = "%s ≈ ☐ when it is rounded to the nearest %s. What number goes in the box?" % (n(x), n(p))
    else:
        q = "Round %s to the nearest %s." % (n(x), n(p))
    if line:
        q = line_for(x, p) + q
    return mcq_r(q, round_to(x, p), round_cands(x, p), round_expl(x, p))


def which_rounds(target, p, right, wrong):
    assert round_to(right, p) == target
    for w in wrong:
        assert round_to(w, p) != target, (target, w)
    lo, hi = target - p // 2, target + p // 2 - 1
    e = ("Numbers from %s to %s round to %s. %s is in that range. %s rounds to %s."
         % (n(lo), n(hi), n(target), n(right), n(wrong[0]), n(round_to(wrong[0], p))))
    return mcq("Which number rounds to %s when you round it to the nearest %s?" % (n(target), n(p)),
               n(right), [n(w) for w in wrong], e)


def least_most(target, p, least):
    lo, hi = target - p // 2, target + p // 2 - 1
    if least:
        ans, wrong = lo, [target - p, lo - 1, hi]
        e = ("Numbers from %s to %s round to %s. %s rounds down to %s, so the smallest is %s."
             % (n(lo), n(hi), n(target), n(lo - 1), n(target - p), n(lo)))
    else:
        ans, wrong = hi, [hi + 1, target + p - 1, lo]
        e = ("Numbers from %s to %s round to %s. %s is exactly halfway, so it rounds up to %s. The greatest is %s."
             % (n(lo), n(hi), n(target), n(hi + 1), n(target + p), n(hi)))
    for w in wrong:
        assert (round_to(w, p) != target) or (w == (hi if least else lo))
    assert round_to(ans, p) == target and round_to(lo - 1, p) != target and round_to(hi + 1, p) != target
    return mcq("What is the %s whole number that rounds to %s when you round it to the nearest %s?"
               % ("smallest" if least else "greatest", n(target), n(p)), n(ans), [n(w) for w in wrong], e)


# ============================================================ set 1: nearest 10
def set_ten(pk):
    L, P = [], []
    for lo, hi in [(11, 89), (11, 89), (101, 989), (101, 989), (101, 989), (1001, 9989), (1001, 9989),
                   (10001, 99989)]:
        L.append(q_round(pk.pick(lo, hi, 10), 10, line=True))
    L.append(q_round(pk.take(85), 10, line=True))
    for k, (lo, hi) in enumerate([(101, 989), (1001, 9989), (1001, 9989), (10001, 99989), (10001, 99989)]):
        P.append(q_round(pk.pick(lo, hi, 10), 10, box=k % 2 == 1))
    S = [q_round(pk.take(4396), 10), q_round(pk.take(2997), 10, box=True), q_round(pk.take(35055), 10)]
    R = [which_rounds(450, 10, 447, [455, 441, 458]), least_most(60, 10, True), least_most(70, 10, False)]
    its = L[:3] + P[:1] + L[3:5] + L[8:9] + P[1:2] + L[5:7] + S[:1] + P[2:3] + L[7:8] + R[:1] + P[3:4] + S[1:2] \
        + S[2:] + P[4:] + R[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Round to the nearest 10", "items": its}


# ============================================================ set 2: nearest 100
def set_hundred(pk):
    L, P = [], []
    for lo, hi in [(110, 890), (110, 890), (110, 890), (1010, 8890), (1010, 8890), (1010, 8890), (10010, 98890)]:
        L.append(q_round(pk.pick(lo, hi, 100), 100, line=True))
    L.append(q_round(pk.take(4450), 100, line=True))
    for k, (lo, hi) in enumerate([(1010, 8890), (1010, 8890), (1010, 8890), (10010, 98890), (10010, 98890)]):
        P.append(q_round(pk.pick(lo, hi, 100), 100, box=k % 2 == 1))
    S = [q_round(pk.take(2965), 100), q_round(pk.take(3449), 100, line=True), q_round(pk.take(7050), 100, box=True),
         q_round(pk.take(39960), 100), q_round(pk.take(1049), 100)]
    R = [which_rounds(800, 100, 763, [850, 742, 871]), least_most(600, 100, False)]
    its = L[:3] + P[:1] + L[3:5] + L[7:8] + P[1:2] + L[5:7] + S[1:2] + P[2:3] + S[:1] + R[:1] + S[2:3] + P[3:4] \
        + S[4:5] + S[3:4] + P[4:] + R[1:]
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Round to the nearest 100", "items": its}


# ============================================================ set 3: nearest 1000
def set_thousand(pk):
    L, P = [], []
    for lo, hi in [(1010, 8990), (1010, 8990), (1010, 8990), (10100, 98990), (10100, 98990)]:
        L.append(q_round(pk.pick(lo, hi, 1000), 1000, line=True))
    L.append(q_round(pk.take(4500), 1000, line=True))
    for k, (lo, hi) in enumerate([(1010, 8990), (1010, 8990), (10100, 98990), (10100, 98990)]):
        P.append(q_round(pk.pick(lo, hi, 1000), 1000, box=k % 2 == 1))
    S = [q_round(pk.take(6457), 1000, line=True), q_round(pk.take(9615), 1000), q_round(pk.take(39600), 1000),
         q_round(pk.take(2499), 1000, box=True), q_round(pk.take(72500), 1000), q_round(pk.take(48451), 1000),
         q_round(pk.take(99600), 1000, box=True)]
    R = [which_rounds(3000, 1000, 2684, [3500, 2450, 3812]), least_most(8000, 1000, True)]
    assert round_to(6348, 10) == 6350 and round_to(6348, 100) == 6300 and round_to(6348, 1000) == 6000
    T = [mcq("Round 6348 to the nearest 10, the nearest 100 and the nearest 1000. Which list is correct?",
             "6350; 6300; 6000", ["6350; 6400; 7000", "6340; 6300; 6000", "6350; 6300; 7000"],
             "Always round the number you started with, 6348. Nearest 10: the ones digit is 8, so 6350. "
             "Nearest 100: the tens digit is 4, so 6300. Nearest 1000: the hundreds digit is 3, so 6000. "
             "Do not round 6350 again to get 6400 and then 7000.")]
    its = L[:2] + P[:1] + L[2:3] + L[5:6] + P[1:2] + L[3:5] + S[:1] + P[2:3] + S[1:2] + R[:1] + S[3:4] + S[2:3] \
        + P[3:4] + S[4:5] + S[5:6] + S[6:] + R[1:] + T
    assert len(its) == 20 and len({id(x) for x in its}) == 20, len(its)
    return {"title": "Round to the nearest 1000", "items": its}


# ============================================================ set 4: estimating with ≈
SYM = {"+": "+", "-": "−"}


def estimate(a, b, op, p, story=None, fmt=n, lead="", money=False):
    """Estimate a + b or a − b by rounding both numbers to the nearest p."""
    ra, rb = round_to(a, p), round_to(b, p)
    f = (lambda u, v: u + v) if op == "+" else (lambda u, v: u - v)
    exact, est = f(a, b), f(ra, rb)
    trunc = f(a // p * p, b // p * p)
    small = f(round_to(a, p // 10), round_to(b, p // 10)) if p > 10 else None
    assert est != exact and est > 0
    sym = SYM[op]
    m = (lambda v: "$" + n(v)) if money else n
    e = ("%s%s ≈ %s and %s ≈ %s. %s %s %s = %s. (The exact answer is %s, so the estimate is close.)"
         % (lead, m(a), m(ra), m(b), m(rb), m(ra), sym, m(rb), m(est), m(exact)))
    if fmt is not n:
        e += " Answer: about %s." % fmt(est)
    assert abs(est - exact) <= p
    q = story or ("Round each number to the nearest %s to estimate. %s %s %s ≈ ☐" % (n(p), n(a), sym, n(b)))
    return mcq_r(q, est, [trunc, exact, small, est + p, est - p], e, fmt)


def estimate_mul(a, k, p, story=None, fmt=n):
    """Estimate a × k by rounding a to the nearest p."""
    ra = round_to(a, p)
    exact, est = a * k, ra * k
    lo = a // p * p
    other = (lo + p if ra == lo else lo) * k
    small = round_to(a, p // 10) * k if p > 10 else None
    assert est != exact
    e = ("%s ≈ %s. %s × %d = %s. (The exact answer is %s.)" % (n(a), n(ra), n(ra), k, n(est), n(exact)))
    if fmt is not n:
        e += " Answer: about %s." % fmt(est)
    q = story or ("Round %s to the nearest %s to estimate. %s × %d ≈ ☐" % (n(a), n(p), n(a), k))
    return mcq_r(q, est, [other, exact, small, ra * (k + 1), est * 10], e, fmt)


def set_estimate():
    its = []
    its.append(estimate(58, 37, "+", 10))
    its.append(estimate(378, 452, "+", 100))
    its.append(estimate_mul(52, 8, 10))
    its.append(estimate(912, 387, "-", 100))
    its.append(estimate(4812, 3275, "+", 1000))
    its.append(estimate_mul(68, 7, 10))
    its.append(estimate(8730, 3214, "-", 1000))
    its.append(estimate_mul(387, 6, 100))
    its.append(estimate(2648, 1173, "+", 100))
    # the ≈ sign
    assert round_to(3468, 100) == 3500 and round_to(3468, 10) == 3470
    its.append(mcq("3468 is rounded to the nearest 100. Which is correct?", "3468 ≈ 3500",
                   ["3468 = 3500", "3468 ≈ 3400", "3468 ≈ 3470"],
                   "The tens digit is 6, so 3468 rounds up to 3500. ≈ means “is approximately equal to”, so we write "
                   "3468 ≈ 3500. 3468 = 3500 is wrong because the numbers are not equal. (3470 is the nearest 10.)"))
    its.append(estimate(6812, 2395, "-", 100))
    its.append(estimate_mul(712, 9, 100))
    its.append(estimate(23487, 41260, "+", 1000))
    its.append(estimate_mul(2985, 4, 1000))
    its.append(estimate(45280, 17630, "-", 1000))
    its.append(estimate(7023, 4987, "-", 1000))
    its.append(estimate_mul(1980, 5, 1000))
    its.append(estimate_mul(3046, 7, 1000))
    # is the answer reasonable?
    assert 4987 + 2036 == 7023
    its.append(mcq("Ali worked out 4987 + 2036 = 6023. Use rounding to the nearest 1000 to check. "
                   "Is his answer reasonable?", "No, it should be about 7000",
                   ["Yes, it is about 6000", "No, it should be about 8000", "Yes, it is about 7000"],
                   "4987 ≈ 5000 and 2036 ≈ 2000. 5000 + 2000 = 7000. 6023 is far from 7000, so Ali made a mistake. "
                   "(The exact answer is 7023: he forgot to add the renamed 1 thousand.)"))
    assert 498 * 4 == 1992
    its.append(mcq("Mei Ling worked out 498 × 4 = 1192. Round 498 to the nearest 100 to check. "
                   "Is her answer reasonable?", "No, it should be about 2000",
                   ["Yes, it is about 1200", "No, it should be about 1600", "Yes, it is about 2000"],
                   "498 ≈ 500. 500 × 4 = 2000. 1192 is far from 2000, so the answer is not reasonable. "
                   "(The exact answer is 1992.)"))
    assert len(its) == 20
    return {"title": "Estimating with ≈", "items": its}


# ============================================================ set 5: word problems
def story(t, x, p, pre="", post=""):
    f = unit(pre, post)
    return mcq_r(t, round_to(x, p), round_cands(x, p), round_expl(x, p, fmt=f), f)


def set_words():
    S = {}
    S["stadium"] = story("A crowd of 54" + NB + "728 people watched a match at the National Stadium. "
                         "About how many people is that, to the nearest 1000?", 54728, 1000, post=" people")
    S["flyer"] = story("The Singapore Flyer is 165 m tall. What is its height to the nearest 10 m?", 165, 10,
                       post=" m")
    S["school"] = story("A primary school has 1346 students. How many students is that to the nearest 100?",
                        1346, 100, post=" students")
    S["library"] = story("A library has 6752 storybooks. About how many storybooks is that, to the nearest 1000?",
                         6752, 1000, post=" storybooks")
    S["mrt"] = story("An MRT train carried 1485 passengers in the morning. Round the number of passengers to "
                     "the nearest 100.", 1485, 100, post=" passengers")
    S["hawker"] = story("A hawker stall sold 2965 plates of chicken rice in a month. About how many plates is "
                        "that, to the nearest 100?", 2965, 100, post=" plates")
    S["plane"] = story("A plane flew 4675 km from Changi Airport. How far is that to the nearest 1000 km?",
                       4675, 1000, post=" km")
    S["car"] = story("Mr Tan’s car has travelled 25" + NB + "961 km. How far is that to the nearest 100 km?",
                     25961, 100, post=" km")
    S["fair"] = story("A Children’s Day fun fair raised $3450. How much is that to the nearest $100?", 3450, 100,
                      pre="$")
    S["sports"] = story("2486 students took part in Sports Day. About how many students is that, to the "
                        "nearest 1000?", 2486, 1000, post=" students")
    S["durian"] = story("A fruit seller sold 1996 durians in June. Round this number to the nearest 10.",
                        1996, 10, post=" durians")
    S["zoo"] = story("The Singapore Zoo had 18" + NB + "463 visitors in one week. Round the number of visitors to "
                     "the nearest 100.", 18463, 100, post=" visitors")
    # reasoning about a rounded number
    real = [54610, 54480, 55500, 55820]
    assert round_to(real[0], 1000) == 55000 and all(round_to(w, 1000) != 55000 for w in real[1:])
    S["real"] = mcq("A newspaper said “about 55" + NB + "000 fans” were at the National Stadium. The number was "
                    "rounded to the nearest 1000. Which could be the real number of fans?",
                    n(54610), [n(v) for v in real[1:]],
                    "Numbers from 54 500 to 55 499 round to 55 000. 54 610 is in that range. 54 480 rounds down to "
                    "54 000, and 55 500 and 55 820 round up to 56 000.")
    S["greatest"] = mcq("The number of seats in a concert hall is 5000 when it is rounded to the nearest 1000. "
                        "What is the greatest number of seats the hall could have?",
                        n(5499), [n(5500), n(5999), n(4999)],
                        "Numbers from 4500 to 5499 round to 5000. 5500 is exactly halfway, so it rounds up to 6000. "
                        "The greatest is 5499.")
    assert round_to(5499, 1000) == 5000 and round_to(5500, 1000) == 6000
    S["smallest"] = mcq("A school has about 800 students, rounded to the nearest 100. What is the smallest number "
                        "of students it could have?", n(750), [n(700), n(749), n(849)],
                        "Numbers from 750 to 849 round to 800. 749 rounds down to 700, so the smallest is 750.")
    assert round_to(750, 100) == 800 and round_to(749, 100) == 700
    # estimating with bar models
    S["gardens"] = estimate(4870, 5240, "+", 1000, fmt=unit(post=" visitors"),
                            story=fig(bar_svg([("Saturday", [(4870, False)], [(0, 0, n(4870))]),
                                               ("Sunday", [(5240, False)], [(0, 0, n(5240))])],
                                              total="?", label="bar model: Saturday and Sunday, total unknown"))
                            + "A flower show at Gardens by the Bay had 4870 visitors on Saturday and 5240 visitors "
                              "on Sunday. Round each number to the nearest 1000 to estimate the total number of "
                              "visitors.")
    S["oranges"] = estimate(8730, 6125, "-", 1000, fmt=unit(post=" oranges"),
                            story=fig(bar_svg([("Oranges", [(6125, False), (8730 - 6125, True)],
                                                [(0, 0, "sold " + n(6125)), (1, 1, "?")], )],
                                              total=n(8730), label="bar model: oranges sold and left"))
                            + "Before Chinese New Year, a shop had 8730 mandarin oranges. It sold 6125 of them. "
                              "Round each number to the nearest 1000 to estimate how many oranges were left.")
    S["bubble"] = estimate_mul(198, 7, 100, fmt=unit(post=" cups"),
                               story=fig(bar_svg([("Cups sold", [(198, False)] * 7, [(0, 0, "198")])],
                                                 total="?", label="bar model: 7 equal units of 198"))
                               + "A bubble tea shop sold 198 cups a day for 7 days. Round 198 to the nearest 100 "
                                 "to estimate the number of cups sold.")
    S["holiday"] = estimate(2985, 1190, "-", 100, fmt=unit(pre="$"), money=True,
                            story=fig(bar_svg([("Holiday", [(2985, False)], [(0, 0, "$2985")]),
                                               ("Television", [(1190, False), (2985 - 1190, True)],
                                                [(0, 0, "$1190"), (1, 1, "?")])],
                                              label="bar model comparing the holiday and the television"))
                            + "Hui Min’s family spent $2985 on a holiday and $1190 on a television. Round each "
                              "amount to the nearest $100 to estimate how much more they spent on the holiday.")
    order = ["flyer", "school", "stadium", "library", "mrt", "fair", "durian", "plane", "hawker", "sports", "zoo",
             "car", "gardens", "oranges", "real", "bubble", "holiday", "smallest", "greatest"]
    # tickets: an estimate to decide
    assert 48 * 6 == 288 and 50 * 6 == 300
    S["tickets"] = mcq("Each ticket to a show costs $48. Mrs Lim wants to buy 6 tickets. She has $200. "
                       "Round $48 to the nearest $10 to estimate. Does she have enough money?",
                       "No, she needs about $300", ["Yes, she needs about $200", "Yes, she needs about $240",
                                                    "No, she needs about $480"],
                       "$48 ≈ $50. $50 × 6 = $300. $200 is much less than $300, so she does not have enough. "
                       "(The exact cost is $288.)")
    order.insert(17, "tickets")
    assert sorted(order) == sorted(S) and len(order) == 20
    return {"title": "Rounding and estimation word problems", "items": [S[k] for k in order]}


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
        "<h2>What rounding means</h2>"
        "<p>Rounding finds the <b>nearest</b> 10, 100 or 1000. A rounded number is easy to work with, "
        "and it helps you check if an answer makes sense.</p>"
        "<p>We use the sign <b>≈</b>. It means “is approximately equal to”. We write 47 ≈ 50.</p>"
        "<figure class='sn-fig'>" + number_line_svg(40, 50, 47, 1) +
        "<figcaption>47 is nearer to 50 than to 40. So 47 ≈ 50 (to the nearest 10).</figcaption></figure>"
        "<h2>The rounding rule</h2>"
        "<ol class='rk-step'><li>Find the digit in the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to its right</b>.</li>"
        "<li><b>5 or more</b>: round up. <b>4 or less</b>: round down.</li>"
        "<li>Change every digit after the rounding place to 0.</li></ol>"
        "<figure class='sn-fig'>" + number_line_svg(3400, 3500, 3462, 10) +
        "<figcaption>3462 is between 3400 and 3500. It is past the halfway point, 3450, so it rounds to 3500."
        "</figcaption></figure>" +
        table(["Round 3462 to the nearest", "Look at", "Answer"], [
            ["10", "the ones digit: 2", "3462 ≈ 3460"],
            ["100", "the tens digit: 6", "3462 ≈ 3500"],
            ["1000", "the hundreds digit: 4", "3462 ≈ 3000"],
        ]) +
        ex("Exactly halfway", "Round 4500 to the nearest 1000.",
           "4500 is exactly halfway between 4000 and 5000. A number exactly halfway rounds up.", "4500 ≈ 5000") +
        ex("Watch the 9s", "Round 2965 to the nearest 100.",
           "The tens digit is 6, so round up. 9 hundreds + 1 hundred = 10 hundreds. "
           "Rename 10 hundreds as 1 thousand: 2900 + 100 = 3000.", "2965 ≈ 3000") +
        "<h2>Estimating with ≈</h2>"
        "<p>Round each number first. Then add, subtract or multiply the rounded numbers. "
        "Compare the estimate with your exact answer to spot a mistake.</p>" +
        ex("Estimate a sum", "Round each number to the nearest 1000. 4812 + 3275 ≈ ☐",
           "4812 ≈ 5000 and 3275 ≈ 3000. 5000 + 3000 = 8000. The exact answer, 8087, is close.", "8000") +
        ex("Estimate a product", "Round 387 to the nearest 100. 387 × 6 ≈ ☐",
           "387 ≈ 400. 400 × 6 = 2400. The exact answer is 2322.", "2400") +
        "<p>In word problems, draw a bar model first. Then round the numbers in the model.</p>"
        "<figure class='sn-fig'>" + bar_svg([("Saturday", [(4870, False)], [(0, 0, n(4870))]),
                                            ("Sunday", [(5240, False)], [(0, 0, n(5240))])],
                                           total="?", label="bar model: Saturday and Sunday, total unknown") +
        "<figcaption>4870 visitors on Saturday and 5240 on Sunday. 4870 ≈ 5000 and 5240 ≈ 5000, "
        "so the total ≈ 10 000.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Rounding 4500 down to 4000", "Exactly halfway rounds up: 5000"],
            ["Rounding the wrong place (3462 to the nearest 100 = 3460)", "Find the hundreds digit first: 3500"],
            ["Rounding in two steps (3449 → 3450 → 3500)", "Round the number you started with: 3400"],
            ["Keeping the digits after the place (3462 → 3562)", "Change them to 0: 3500"],
            ["Losing the renamed 1 (2965 → 2000)", "10 hundreds = 1 thousand: 3000"],
        ])
    )


FAQ = [
    {"q": "What rounding is taught in P4 maths?",
     "a": "Primary 4 students round whole numbers to the nearest 10, 100 or 1000 and use the sign ≈. "
          "They use rounding to estimate answers to sums, differences and products."},
    {"q": "How do I explain rounding to my child?",
     "a": "Draw a number line and ask which round number is nearer. Then teach the rule: look at the digit to the "
          "right of the rounding place; 5 or more rounds up, 4 or less rounds down."},
    {"q": "What is the most common rounding mistake?",
     "a": "The most common mistake is rounding in two steps, such as 3449 → 3450 → 3500, when the answer to the "
          "nearest 100 is 3400. Another is rounding 4500 down to 4000; a number exactly halfway rounds up."},
    {"q": "Is rounding in the MOE syllabus?",
     "a": "Yes. Rounding numbers to the nearest 10, 100 or 1000 and the use of ≈ are part of Whole Numbers in the "
          "MOE 2021 Primary 4 Mathematics syllabus. Estimation skills are also useful later for the PSLE."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (54 728) everywhere outside SVG markup."""
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
    """Tag wide pictures (number lines, bar models) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64802)
    pk = Picker(rnd)
    sets = [set_ten(pk), set_hundred(pk), set_thousand(pk), set_estimate(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "rounding-and-estimation", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Rounding and Estimation",
        "seo_title": "P4 Rounding and Estimation Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Rounding and Estimation",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Rounding numbers to the nearest 10, 100 or 1000; use of ≈",
        "meta_desc": "Free P4 maths practice: round to the nearest 10, 100 and 1000 with number lines, estimate "
                     "with ≈ and solve word problems. 100 questions with answers.",
        "key_big": "Look one place to the right: 5 or more rounds up, 4 or less rounds down.",
        "key_sub": "3462 ≈ 3500 to the nearest 100, because the tens digit 6 is 5 or more.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(fix_spaces(u), "(number line|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
