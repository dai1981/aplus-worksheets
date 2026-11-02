# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Dividing by two-digit numbers (Ontario Mathematics Curriculum 2020, B2.7)
Three-digit whole numbers divided by two-digit whole numbers: multiples of 10, the area model,
long division without and with remainders (whole number, fraction, rounded up), Ontario word problems.
  python3 tools/gen_caon_math_g5_division.py
HTML attributes use single quotes (no backslashes in the JSON). Every answer is computed in code.
Canadian style: Canadian English, metric, $, numbers under 10 000 (no separators needed).
"""
import json, os, random, re
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
NBSP = " "


# ------------------------------------------------------------ helpers
def f(n):
    """Ontario style: 4536, 10 000 (no-break space only from 5 digits)."""
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


def r10(x):
    return (x + 5) // 10 * 10


def cval(c):
    """Value of a choice: '12 boxes' -> 12, '3 <fr 1/2> L' -> 7/2, '8 R 10' -> ('R', 8, 10), 'about 8' -> 8."""
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


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %d × %d + %d = %d." % (q, d, r, n)
    return "Check: %d × %d = %d." % (q, d, n)


# ------------------------------------------------------------ long division in words
def ld_rows(n, d):
    """Steps of long division: list of (index of digit, partial dividend, quotient digit), remainder."""
    ds = [int(c) for c in str(n)]
    cur, steps, started = 0, [], False
    for i, x in enumerate(ds):
        cur = cur * 10 + x
        if not started and cur < d and i < len(ds) - 1:
            continue
        started = True
        q = cur // d
        steps.append((i, cur, q))
        cur -= q * d
    return steps, cur


def first_try(cur, d):
    """Round the divisor to the nearest ten and estimate one quotient digit."""
    D = r10(d)
    return D, max(1, min(9, cur // D))


def digit_words(cur, d):
    """Estimate one quotient digit and fix it if needed (in words). Returns (text, digit)."""
    q = cur // d
    D, e = first_try(cur, d)
    if q == 0:
        if cur == 0:
            return "Nothing is left to divide, so write 0.", 0
        return "%d is less than %d, so write 0." % (cur, d), 0
    parts = []
    if abs(e - q) > 1:
        # rounding is too far off (for example 15 -> 20): find the digit by multiplying
        parts.append("%d × %d = %d and %d × %d = %d is more than %d, so use %d."
                     % (q, d, q * d, q + 1, d, (q + 1) * d, cur, q))
        parts.append("%d − %d = %d." % (cur, q * d, cur - q * d))
        return " ".join(parts), q
    if D != d:
        parts.append("%d ÷ %d is about %d ÷ %d, so try %d." % (cur, d, cur, D, e))
    else:
        parts.append("Try %d." % e)
    while e * d > cur:
        parts.append("%d × %d = %d is more than %d, so try %d." % (e, d, e * d, cur, e - 1))
        e -= 1
    while cur - e * d >= d:
        parts.append("%d × %d = %d leaves %d, which is not less than %d, so try %d." % (e, d, e * d, cur - e * d, d, e + 1))
        e += 1
    assert e == q
    parts.append("%d × %d = %d, %d − %d = %d." % (q, d, q * d, cur, q * d, cur - q * d))
    return " ".join(parts), q


def ld_steps(n, d, end=True):
    """Divide, multiply, subtract, bring down — in words, with the estimate for each digit."""
    ds = str(n)
    steps, r = ld_rows(n, d)
    q = n // d
    parts = []
    for k, (i, cur, qd) in enumerate(steps):
        w, _ = digit_words(cur, d)
        if k == 0:
            head = ("%d is less than %d, so start with %d. " % (int(ds[:i]), d, cur)) if i > 0 else ""
            parts.append(head + w)
        else:
            parts.append(("Bring down %s. " % ds[i] if cur == 0 else "Bring down %s to make %d. " % (ds[i], cur)) + w)
    if end:
        parts.append("Answer: %s. %s" % (qr(q, r), check_txt(n, d)))
    else:
        parts.append("So %d ÷ %d = %s." % (n, d, qr(q, r)))
    return " ".join(parts)


# ------------------------------------------------------------ typical mistakes
def no_rem_cands(n, d):
    q = n // d
    c = []
    if q % 10 == 0:
        c.append(f(q // 10))                       # left out the 0 in the ones place
    c += [f(q * 10),                               # first digit written in the wrong place
          qr(q - 1, d),                            # estimate not fixed: "remainder" equals the divisor
          f(q + 1), f(q - 1), f(q + 10), f(q - 10)]
    return c


def rem_cands(n, d):
    q, r = divmod(n, d)
    return [qr(q - 1, r + d),                      # remainder bigger than the divisor
            f(q),                                  # left the remainder out
            qr(q * 10, r),                         # first digit in the wrong place
            qr(q, d - r),                          # wrote how many more are needed
            qr(q + 1, r), qr(q - 1, r)]


# ------------------------------------------------------------ figures
def bracket_svg(n, d, fs=24, work=False):
    """Long division layout. With work=True, the full worked example is drawn."""
    cw = fs * 0.85
    ds = str(n)
    L = len(ds)
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18
    steps, r = ld_rows(n, d)
    q = n // d
    rh = fs * 1.25
    top = (rh + 6) if work else 10
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def digits_at(txt, last, y, colr=INK):
        for k, ch in enumerate(reversed(txt)):
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (col(last - k), y, fs, colr, ch))

    by = top + rh - fs * 0.18
    digits_at(ds, L - 1, by)
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * L + 8
    H = top + bh + 8
    if work:
        digits_at(str(q), L - 1, top - 8, GREEN)
        if r:
            rt = "R %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>"
                     % (x0 + cw * L + 10, top - 8, fs, GREEN, rt))
            W = max(W, x0 + cw * L + 10 + len(rt) * fs * 0.62 + 8)
        y = by
        for k, (i, cur, qd) in enumerate(steps):
            p = qd * d
            y += rh
            digits_at(str(p), i, y)
            left = i - len(str(max(p, cur))) + 1
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>−</text>"
                     % (col(i - len(str(p)) + 1) - cw * 0.85, y, fs, RED))
            ly = y + fs * 0.3
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (col(left) - cw * 1.2, ly, col(i) + cw * 0.5, ly, INK))
            y += rh
            diff = cur - p
            if k + 1 < len(steps):
                nxt = steps[k + 1][1]
                digits_at(str(nxt), i + 1, y)
                s.append("<path d='M%.1f %.1f V%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='3 3' "
                         "marker-end='url(#ah)'/>" % (col(i + 1), by + fs * 0.3, y - fs * 0.95, GREEN))
            else:
                digits_at(str(diff), i, y, GREEN if diff else INK)
        H = y + 12
        s.insert(0, "<defs><marker id='ah' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='6' markerHeight='6' "
                    "orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + cw * L + 4, top, INK))
    label = ("%d divided by %d worked out with long division" if work else "%d divided by %d written as long division") % (n, d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


def area_svg(d, inside, tops, label):
    """Area model: divisor on the left side, a rectangle split into parts. inside = area in each part,
    tops = partial quotient above each part. '?' is drawn in red."""
    fs = 18
    xs = 42
    ws = [max(72, len(str(p)) * fs * 0.62 + 26, len(str(t)) * fs * 0.62 + 20) for p, t in zip(inside, tops)]
    y0, h = 34, 58
    s = []
    x = xs
    for p, t, w in zip(inside, tops, ws):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y0, w, h, FILL, GREEN))
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + w / 2, y0 + h / 2 + 6, fs, RED if p == "?" else INK, p))
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + w / 2, y0 - 10, fs, RED if t == "?" else GREEN, t))
        x += w
    s.append("<text x='%d' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (xs - 20, y0 + h / 2 + 6, fs, GREEN, d))
    return svg_wrap(int(x + 8), y0 + h + 8, "".join(s), label)


def area_parts(q, split_tens=False):
    """Partial quotients from the digits of q: 23 -> 20, 3 (or 10, 10, 3 when split_tens)."""
    t, o = q // 10 * 10, q % 10
    pq = [10] * (t // 10) if split_tens else [t]
    if o:
        pq.append(o)
    return pq


# ============================================================ set 1: multiples of 10
def set_tens(rnd, used):
    its = []
    facts = [(a, b) for a in range(2, 10) for b in range(2, 10) if 10 <= a * b <= 99]
    rnd.shuffle(facts)

    def take(cond):
        for k, (dd, qq) in enumerate(facts):
            if cond(dd, qq):
                facts.pop(k)
                return dd, qq
        raise AssertionError("no fact")

    # A) fact × 10 ÷ tens: 240 ÷ 30 = 8
    for i in range(7):
        dd, qq = take(lambda a, b: a * b * 10 not in used and a * b % 10 != 0)
        n, d = dd * qq * 10, dd * 10
        used.add(n)
        e = ("Think of the fact: %d ÷ %d = %d. Cross out one 0 in each number: %d ÷ %d = %d ÷ %d = %d. "
             "Check: %d × %d = %d." % (dd * qq, dd, qq, n, d, n // 10, dd, qq, qq, d, n))
        its.append(mcqv("What is %d ÷ %d?" % (n, d), f(qq), [f(qq * 10), f(qq + 1), f(qq - 1), f(qq * 100)], e))
    # B) hundreds ÷ tens: 600 ÷ 20 = 30
    for dd, qq in [(2, 3), (4, 2), (3, 3)]:
        n, d = dd * qq * 100, dd * 10
        q = n // d
        used.add(n)
        e = ("Cross out one 0 in each number: %d ÷ %d = %d ÷ %d. %d ÷ %d = %d, so %d ÷ %d = %d. "
             "Do not lose the 0 in the answer: %d × %d = %d." % (n, d, n // 10, dd, dd * qq, dd, qq, n // 10, dd, q, q, d, n))
        its.append(mcqv("What is %d ÷ %d?" % (n, d), f(q), [f(qq), f(q * 10), f(q + 10), f(q - 10)], e))
    # C) missing factor
    for _ in range(3):
        dd, qq = take(lambda a, b: a * b * 10 not in used and a * b % 10 != 0)
        n, d = dd * qq * 10, dd * 10
        used.add(n)
        e = ("Think: what number times %d is %d? That is %d ÷ %d = %d ÷ %d = %d. Check: %d × %d = %d."
             % (d, n, n, d, n // 10, dd, qq, qq, d, n))
        its.append(mcqv("What number goes in the box?  <b>☐ × %d = %d</b>" % (d, n), f(qq),
                        [f(qq * 10), f(n - d), f(qq + 1), f(qq - 1)], e))
    # D) remainders with multiples of 10: 250 ÷ 30 = 8 R 10
    k = 0
    while k < 3:
        dd = rnd.randint(3, 9)
        qq = rnd.randint(2, 9)
        rr = rnd.randint(1, dd - 1)
        n, d = (dd * qq + rr) * 10, dd * 10
        if n in used or n > 999 or rr == qq or qq * 10 == rr * 10 + d:
            continue
        used.add(n)
        q, r = divmod(n, d)
        e = ("%d × %d = %d and %d × %d = %d, which is too big. So %d groups of %d fit, and %d − %d = %d is left. "
             "%d ÷ %d = %s. The remainder is %d, not %d: crossing out zeros does not change what is left over. %s"
             % (q, d, q * d, q + 1, d, (q + 1) * d, q, d, n, q * d, r, n, d, qr(q, r), r, r // 10, check_txt(n, d)))
        its.append(mcqv("What is %d ÷ %d?" % (n, d), qr(q, r), [qr(q, r // 10), f(q), qr(q, d - r), qr(q - 1, r + d)], e))
        k += 1
    # E) estimate by rounding the divisor
    k = 0
    while k < 4:
        D = rnd.choice([20, 30, 40, 50, 60, 70, 80, 90])
        d = D + rnd.choice([-2, -1, 1, 2])
        e_ = rnd.randint(3, 9)
        m = e_ * D
        n = m + rnd.choice([-1, 1]) * rnd.randint(2, 8)
        if not (100 <= n <= 999) or n in used or m // 10 == e_ * 10 // 10 or abs(n // d - e_) > 1:
            continue
        used.add(n)
        q, r = divmod(n, d)
        expl = ("Round %d to %d. %d is close to %d, and %d ÷ %d = %d, so %d ÷ %d = %d. "
                "%d ÷ %d is about %d. (The exact answer is %s.)" % (d, D, n, m, m // 10, D // 10, e_, m, D, e_, n, d, e_, qr(q, r)))
        its.append(mcqv("Round the divisor to the nearest ten to estimate %d ÷ %d." % (n, d), "about %d" % e_,
                        ["about %d" % (e_ * 10), "about %d" % (m // 10), "about %d" % (e_ * 100)], expl))
        k += 1
    assert len(its) == 20, len(its)
    return {"title": "Divide by multiples of 10", "items": its}


# ============================================================ set 2: area model
def set_area(rnd, used):
    its = []
    k = 0
    # A) use the area model to find the quotient (all tops unknown)
    while k < 8:
        d = rnd.randint(12, 45)
        q = rnd.randint(11, 39)
        n = q * d
        if d % 10 == 0 or n in used or n > 999 or n < 200 or q % 10 == 0:
            continue
        used.add(n)
        pq = area_parts(q, split_tens=(k in (2, 6) and q >= 20))
        parts = [p * d for p in pq]
        e = ("Each part is %d × something. Divide each part by %d: %s. Add the partial quotients: %s = %d. %s"
             % (d, d, ", ".join("%d ÷ %d = %d" % (p, d, x) for p, x in zip(parts, pq)),
                " + ".join(str(x) for x in pq), q, check_txt(n, d)))
        cands = [f(sum(x // 10 if x % 10 == 0 else x for x in pq)),   # wrote 20 as 2 (place value)
                 f(q - pq[-1]),                                        # forgot the last part
                 f(q + 10), f(q * 10), f(q + 1)]
        svg = area_svg(d, [str(p) for p in parts], ["?"] * len(parts), "area model for %d divided by %d" % (n, d))
        its.append(mcqv(fig(svg) + "Use the area model to find %d ÷ %d." % (n, d), f(q), cands, e))
        k += 1
    # B) missing partial quotient
    k = 0
    while k < 4:
        d = rnd.randint(13, 39)
        a = rnd.choice([10, 20]) if d < 25 else 10
        b = rnd.randint(2, 9)
        n = (a + b) * d
        if d % 10 == 0 or n in used or n > 999 or b * d == d * 10:
            continue
        used.add(n)
        svg = area_svg(d, [str(a * d), str(b * d)], [str(a), "?"], "area model for %d divided by %d" % (n, d))
        e = ("The part has area %d and side %d. %d ÷ %d = %d, because %d × %d = %d. So %d ÷ %d = %d + %d = %d."
             % (b * d, d, b * d, d, b, b, d, b * d, n, d, a, b, a + b))
        its.append(mcqv(fig(svg) + "The area model shows %d ÷ %d. What number goes in place of the red question mark?" % (n, d), f(b),
                        [f(b * 10), f(b * d - d), f(a + b), f(b + 1)], e))
        k += 1
    # C) missing area
    k = 0
    while k < 3:
        d = rnd.randint(12, 32)
        a = rnd.choice([10, 20])
        b = rnd.randint(2, 9)
        n = (a + b) * d
        if d % 10 == 0 or n in used or n > 999:
            continue
        used.add(n)
        svg = area_svg(d, ["?", str(b * d)], [str(a), str(b)], "area model for %d divided by %d" % (n, d))
        e = ("The area of a part is side × top: %d × %d = %d. Check: %d + %d = %d, and %d ÷ %d = %d."
             % (d, a, a * d, a * d, b * d, n, n, d, a + b))
        its.append(mcqv(fig(svg) + "The area model shows %d ÷ %d. What is the missing area (the red question mark)?" % (n, d),
                        f(a * d), [f(a * d // 10), f(a + d), f(b * d), f(a * d + d)], e))
        k += 1
    # D) which split works
    k = 0
    while k < 3:
        d = rnd.randint(13, 29)
        b = rnd.randint(2, 9)
        n = (10 + b) * d
        h = n // 100 * 100
        if d % 10 == 0 or n in used or n > 999 or n % 100 == 0 or n < 200 or h % d == 0:
            continue
        used.add(n)
        good = "%d + %d" % (10 * d, b * d)
        badp = [(h, n - h), (h - 100, n - h + 100), (10 * d + 10, b * d - 10)]
        if any(x % d == 0 or y <= 0 for x, y in badp):
            used.discard(n)
            continue
        bad = ["%d + %d" % xy for xy in badp]
        e = ("Each part must be a multiple of %d, so it divides with no remainder. %d = %d × 10 and %d = %d × %d. "
             "So %d ÷ %d = 10 + %d = %d. Splitting by place value (%d + %d) does not work: %d ÷ %d is not a whole number."
             % (d, 10 * d, d, b * d, d, b, n, d, b, 10 + b, h, n - h, h, d))
        assert h % d != 0
        its.append(mcq("You want to find %d ÷ %d with an area model. Which way to split %d works best?" % (n, d, n), good, bad, e))
        k += 1
    # E) area model with a remainder
    k = 0
    while k < 2:
        d = rnd.randint(13, 29)
        q = rnd.randint(12, 29)
        r = rnd.randint(2, d - 1)
        n = q * d + r
        if d % 10 == 0 or n in used or n > 999 or r == q or q % 10 == 0 or r == q % 10:
            continue
        used.add(n)
        pq = area_parts(q)
        parts = [p * d for p in pq]
        svg = area_svg(d, [str(p) for p in parts], [str(x) for x in pq], "area model for %d divided by %d" % (q * d, d))
        e = ("The model uses %s = %d. %d − %d = %d is left, and %d is less than %d, so it is the remainder. "
             "%d ÷ %d = %s. %s" % (" + ".join(str(p) for p in parts), q * d, n, q * d, r, r, d, n, d, qr(q, r), check_txt(n, d)))
        its.append(mcqv(fig(svg) + "%s uses this area model to divide %d ÷ %d. What is %d ÷ %d?"
                        % (["Ms. Patel", "Mr. Tremblay"][k], n, d, n, d), qr(q, r),
                        [f(q), qr(q, r + d), qr(q + 1, r), qr(sum(x // 10 if x % 10 == 0 else x for x in pq), r)], e))
        k += 1
    assert len(its) == 20, len(its)
    return {"title": "Divide with an area model", "items": its}


# ============================================================ set 3: long division, no remainder
def exact(rnd, used, qlo, qhi, lo=100, dlo=12, dhi=98):
    while True:
        d = rnd.randint(dlo, dhi)
        q = rnd.randint(qlo, qhi)
        n = q * d
        if n < lo or n > 999 or n in used or d % 10 == 0 or (q >= 10 and q % 10 == 0) or q == d:
            continue
        used.add(n)
        return n, d


def item_div(n, d, figure):
    q, r = divmod(n, d)
    qtxt = (fig(bracket_svg(n, d)) + "Divide.") if figure else "What is %d ÷ %d?" % (n, d)
    cands = rem_cands(n, d) if r else no_rem_cands(n, d)
    return mcqv(qtxt, qr(q, r), cands, ld_steps(n, d))


def set_exact(rnd, used, P):
    its = []
    for i in range(6):                                       # one-digit quotients
        n, d = exact(rnd, used, 3, 9)
        its.append(item_div(n, d, i % 2 == 0))
    for i in range(6):                                       # two-digit quotients
        n, d = exact(rnd, used, 11, 49, 200, 12, 49)
        its.append(item_div(n, d, i % 2 == 1))
    for q in (20, 30, 40):                                   # zero in the ones place of the quotient
        while True:
            d = rnd.randint(12, 24)
            n = q * d
            if d % 10 and n <= 999 and n not in used:
                break
        used.add(n)
        e = ld_steps(n, d) + " The 0 in the ones place matters: %d is not %d." % (q, q // 10)
        its.append(mcqv("What is %d ÷ %d?" % (n, d), f(q), [f(q // 10), f(q * 10), f(q + 1), f(q - 1)], e))
    # how big is the quotient
    for kind in (1, 2):
        while True:
            d = rnd.randint(12, 98)
            n = rnd.randint(120, 999)
            if d % 10 == 0 or n in used or n % d or len(str(n // d)) != kind:
                continue
            break
        used.add(n)
        q = n // d
        first = int(str(n)[:2])
        why = ("The first two digits make %d, which is less than %d. So the quotient has no tens digit: it is a one-digit number."
               % (first, d)) if kind == 1 else (
              "The first two digits make %d, which is at least %d. So the quotient has a tens digit: it is a two-digit number." % (first, d))
        ch = ["between 1 and 9", "between 10 and 99", "between 100 and 999", "1000 or more"]
        its.append(mcq("Without dividing, how big is the answer to %d ÷ %d?" % (n, d), ch[kind - 1],
                       [c for c in ch if c != ch[kind - 1]], why + " %d ÷ %d = %d." % (n, d, q)))
    # check with multiplication
    n, d = exact(rnd, used, 11, 39, 200, 12, 29)
    q = n // d
    its.append(mcq("%d ÷ %d = %d. Which multiplication checks this answer?" % (n, d, q), "%d × %d = %d" % (q, d, n),
                   ["%d × %d = %s" % (n, d, f(n * d)), "%d × %d = %s" % (q, n, f(q * n)), "%d × %d = %d" % (d, d, d * d)],
                   "Multiplication undoes division: quotient × divisor = dividend. %d × %d = %d, so the answer is right." % (q, d, n)))
    # what should they do next
    for kind in ("up", "down"):
        name, he, his = P.next()
        while True:
            d = rnd.randint(12, 98)
            q = rnd.randint(3, 9)
            n = q * d
            if d % 10 == 0 or n < 100 or n > 999 or n in used:
                continue
            D, e_ = first_try(n, d)
            if (kind == "up" and e_ == q - 1) or (kind == "down" and e_ == q + 1):
                break
        used.add(n)
        lead = "%s divides %d ÷ %d. %s rounds %d to %d and tries %d. " % (name, n, d, cap(he), d, D, e_)
        if kind == "up":
            lead += "%d × %d = %d and %d − %d = %d." % (e_, d, e_ * d, n, e_ * d, n - e_ * d)
            cands = ["Try %d instead" % (e_ - 1), "Write %d R %d" % (e_, n - e_ * d), "Keep %d" % e_]
            expl = ("%d is not less than the divisor %d, so %d fits one more time. Try %d: %d × %d = %d. So %d ÷ %d = %d."
                    % (n - e_ * d, d, d, q, q, d, n, n, d, q))
        else:
            lead += "%d × %d = %d, which is more than %d." % (e_, d, e_ * d, n)
            cands = ["Keep %d" % e_, "Try %d instead" % (e_ + 1), "Write %d R %d" % (e_, e_ * d - n)]
            expl = ("%d is more than %d, so %d is too big. Try %d: %d × %d = %d. So %d ÷ %d = %d."
                    % (e_ * d, n, e_, q, q, d, n, n, d, q))
        its.append(mcq(lead + " What should %s do next?" % he, "Try %d instead" % q, cands, expl))
    assert len(its) == 20, len(its)
    return {"title": "Long division without remainders", "items": its}


# ============================================================ set 4: remainders
def pick_rem(rnd, used, qlo, qhi, dlo=12, dhi=98):
    while True:
        d = rnd.randint(dlo, dhi)
        n = rnd.randint(100, 999)
        q, r = divmod(n, d)
        if r < 2 or d % 10 == 0 or n in used or not (qlo <= q <= qhi) or r in (q, q % 10, d - r) or (q >= 10 and q % 10 == 0):
            continue
        used.add(n)
        return n, d


def set_remainders(rnd, used, P):
    its = []
    for i in range(6):
        n, d = pick_rem(rnd, used, 3, 9) if i < 3 else pick_rem(rnd, used, 11, 49, 12, 49)
        its.append(item_div(n, d, i % 2 == 0))
    # mistakes
    name, he, his = P.next()
    n, d = pick_rem(rnd, used, 11, 39, 12, 39)
    q, r = divmod(n, d)
    M = ["The remainder is too big", "%s left out the remainder" % cap(he),
         "The quotient is in the wrong place", "There is no mistake"]
    its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he), M[0], M[1:],
                   "The remainder must be less than the divisor. %d is more than %d, so %d fits one more time: %d − %d = %d. "
                   "The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    name, he, his = P.next()
    n, d = pick_rem(rnd, used, 11, 39, 12, 39)
    q, r = divmod(n, d)
    M = ["%s left out the remainder" % cap(he), "The remainder is too big",
         "The quotient is in the wrong place", "There is no mistake"]
    its.append(mcq("%s says %d ÷ %d = %d. What mistake did %s make?" % (name, n, d, q, he), M[0], M[1:],
                   "%d × %d = %d, not %d. %d − %d = %d is left over, so the answer is %s."
                   % (q, d, q * d, n, n, q * d, r, qr(q, r))))
    name, he, his = P.next()
    n, d = pick_rem(rnd, used, 3, 9, 21, 98)
    q, r = divmod(n, d)
    M = ["The quotient is in the wrong place", "%s left out the remainder" % cap(he),
         "The remainder is too big", "There is no mistake"]
    its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q * 10, r), he), M[0], M[1:],
                   "%d is less than %d, so there are no tens in the quotient. The first digit goes above the ones place. "
                   "%d × %d = %d, not %d. The answer is %s." % (int(str(n)[:2]), d, q * 10, d, q * 10 * d, n, qr(q, r))))
    # possible remainder
    d = 24
    its.append(mcq("You divide a number by %d. Which of these could be the remainder?" % d, "23", ["24", "25", "30"],
                   "A remainder is always less than the divisor. When you divide by %d, the remainder can be 0 to 23. "
                   "So 23 is the only possible one." % d))
    # remainder as a fraction (mixed number)
    for n, d in [(125, 12), (137, 11), (163, 10), (130, 20), (290, 60)]:
        q, r = divmod(n, d)
        g = gcd(r, d)
        ans = mixed(q, r // g, d // g)
        if g > 1:
            how = ("%d ÷ %d = %d R %d. Put the remainder over the divisor: %s. %s = %s, so the answer is %s."
                   % (n, d, q, r, fr(r, d), fr(r, d), fr(r // g, d // g), ans))
        else:
            how = "%d ÷ %d = %d R %d. Put the remainder over the divisor: %s. The answer is %s." % (n, d, q, r, fr(r, d), ans)
        cands = [qr(q, r), mixed(q, d - r, d), mixed(q, r, q) if r < q else mixed(q, 1, d), "%d.%d" % (q, r) if d != 10 else mixed(q + 1, r, d),
                 mixed(q, 1, r), mixed(q + 1, r, d)]
        its.append(mcqv("Write the answer to %d ÷ %d as a mixed number." % (n, d), ans, cands,
                        how + " (%d R %d is not %d.%d.)" % (q, r, q, r) if d != 10 else how))
    # what to do with the remainder
    its.append(mcq("Which story needs the answer <b>rounded up</b> to the next whole number?",
                   "230 students, 48 on each bus",
                   ["230 cookies, boxes of 48, full boxes", "230 m of rope cut into 48 pieces", "230 cards, piles of 48, cards left"],
                   "230 ÷ 48 = 4 R 38. With 4 buses, 38 students still need a seat, so you need 5 buses. "
                   "The cookies question asks for full boxes (4), the rope can be cut (a fraction), and the cards question asks for the remainder (38)."))
    its.append(mcq("Which story uses the <b>remainder</b> as the answer?",
                   "How many cards are not in a full pile?",
                   ["How many piles can be filled?", "How many piles are needed for all the cards?", "How many cards are in each full pile?"],
                   "“Not in a full pile” means the cards left over, which is the remainder. Full piles use the quotient, "
                   "and “all the cards” means rounding up."))
    its.append(mcq("Which story uses a <b>fraction</b> for the remainder?",
                   "125 L of water shared by 12 tanks",
                   ["125 hikers, 12 in each van", "125 eggs in cartons of 12", "125 students in teams of 12"],
                   "Water can be split into any amount, so each tank gets 10 " + fr(5, 12) + " L: 125 ÷ 12 = 10 R 5. "
                   "You cannot split a hiker, an egg or a student, so those remainders stay whole numbers."))
    # round up, short stories
    for n, d, one, many, who in [(150, 16, "change room", "change rooms", "players"), (290, 24, "row", "rows", "people")]:
        q, r = divmod(n, d)
        assert r and r != q
        ans = units(q + 1, one, many)
        if one == "change room":
            t = "%d hockey players come to a tournament. Each change room holds %d players. How many change rooms are needed?" % (n, d)
        else:
            t = "%d people come to a school concert. Each row has %d chairs. How many rows are needed so everyone has a seat?" % (n, d)
        e = ("%d ÷ %d = %s. %s hold %d %s, so %d %s still need a place. Round up: %s."
             % (n, d, qr(q, r), cap(units(q, one, many)), q * d, who, r, who, ans))
        its.append(mcqv(t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e))
    assert len(its) == 20, len(its)
    return {"title": "Remainders: whole numbers, fractions or round up", "items": its}


# ============================================================ set 5: word problems
def set_story(P):
    its = []
    D = lambda v: "$" + f(v)

    def exact_item(t, n, d, U):
        q, r = divmod(n, d)
        assert r == 0
        cands = [U(int(x)) for x in no_rem_cands(n, d) if " R " not in x]
        cands.insert(1, U(n - d))
        its.append(mcqv(t, U(q), cands, "Share equally, so divide: " + ld_steps(n, d, end=False) + " " + check_txt(n, d)))

    def up_item(t, n, d, one, many, still):
        q, r = divmod(n, d)
        assert r and r != q and r > 1
        ans = units(q + 1, one, many)
        e = ld_steps(n, d, end=False) + " %s are not enough: %s. Round up to %s." % (cap(units(q, one, many)), still % r, ans)
        its.append(mcqv(t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e))

    def down_item(t, n, d, one, many, why):
        q, r = divmod(n, d)
        assert r and r != q and r > 1
        ans = units(q, one, many)
        e = ld_steps(n, d, end=False) + " " + why % r + " The answer is %s." % ans
        its.append(mcqv(t, ans, [units(q + 1, one, many), qr(q, r), units(r, one, many), units(q - 1, one, many)], e))

    def left_item(t, n, d, one, many):
        q, r = divmod(n, d)
        assert r and r != q and r > 1
        ans = units(r, one, many)
        e = ld_steps(n, d, end=False) + " The question asks what is left over. That is the remainder: %s." % ans
        its.append(mcqv(t, ans, [units(q, one, many), units(d - r, one, many), qr(q, r), units(r + d, one, many)], e))

    # buses and other round-up stories
    up_item("230 students from a school go on a field trip. Each bus holds 48 students. How many buses are needed?",
            230, 48, "bus", "buses", "%d students still need a seat")
    up_item("A school board takes 410 students to a play in Toronto. Each school bus holds 72 students. How many buses are needed?",
            410, 72, "bus", "buses", "%d students still need a seat")
    up_item("118 students visit the CN Tower. Each tour group can have up to 15 students. How many tour groups are needed?",
            118, 15, "tour group", "tour groups", "%d students still need a group")
    up_item("A library is moving 650 books. Each box holds 28 books. How many boxes are needed to pack all the books?",
            650, 28, "box", "boxes", "%d books still need a box")
    # full boxes (round down)
    down_item("A bakery makes 470 butter tarts. It packs them in boxes of 24. How many boxes can it fill completely?",
              470, 24, "box", "boxes", "The %d tarts left over cannot fill another box.")
    down_item("A farm collects 315 eggs. The eggs go in cartons of 12. How many cartons can the farm fill?",
              315, 12, "carton", "cartons", "The %d eggs left over cannot fill another carton.")
    nm, he, his = P.next()
    down_item("%s has $250 to buy hockey tickets for a class trip. Each ticket costs $18. How many tickets can %s buy?" % (nm, he),
              250, 18, "ticket", "tickets", "The $%d left over is not enough for another ticket.")
    down_item("The gym has 340 chairs for a concert. They are set out in rows of 24. How many full rows are there?",
              340, 24, "row", "rows", "The %d chairs left over do not make another full row.")
    # left over
    left_item("A teacher has 370 sheets of paper. She gives the same number to each of 28 students, as many as she can. How many sheets are left over?",
              370, 28, "sheet", "sheets")
    nm, he, his = P.next()
    left_item("%s has 400 hockey cards. %s puts them in piles of 36. How many cards are not in a full pile?" % (nm, cap(he)),
              400, 36, "card", "cards")
    # equal sharing, exact
    exact_item("For the Terry Fox Run, 18 classes raise $702 in all. Each class raises the same amount. How much does each class raise?",
               702, 18, D)
    exact_item("A hockey arena has 864 seats in 32 equal rows. How many seats are in each row?",
               864, 32, lambda v: units(v, "seat", "seats"))
    exact_item("A sugar bush makes 345 L of maple syrup. It fills 15 big pails with the same amount. How much syrup is in each pail?",
               345, 15, lambda v: "%d L" % v)
    exact_item("A school buys 528 pencils in boxes of 24. How many boxes does it buy?",
               528, 24, lambda v: units(v, "box", "boxes"))
    # fraction answers
    for t, n, d, u in [("A 125 m rope is cut into 12 equal pieces for a canoe trip. How long is each piece?", 125, 12, "m"),
                       ("A camp pours 137 L of water equally into 11 coolers. How much water is in each cooler?", 137, 11, "L")]:
        q, r = divmod(n, d)
        ans = mixed(q, r, d) + " " + u
        e = ("%d ÷ %d = %d R %d. The %d %s left over can be split too, so each one gets %s %s more. Answer: %s. "
             "(%d R %d is not %d.%d.)" % (n, d, q, r, r, u, fr(r, d), u, ans, q, r, q, r))
        its.append(mcqv(t, ans, [mixed(q, d - r, d) + " " + u, "%d.%d %s" % (q, r, u), "%d %s" % (q, u),
                                  "%d %s" % (q + 1, u), mixed(q, 1, r) + " " + u], e))
    # two steps
    its.append(mcqv("A school buys 6 boxes of 48 freezies. The freezies are shared equally among 24 classes. How many freezies does each class get?",
                    "12 freezies", ["288 freezies", "2 freezies", "120 freezies", "13 freezies"],
                    "Step 1: 6 × 48 = 288 freezies. Step 2: " + ld_steps(288, 24, end=False) + " Each class gets 12 freezies."))
    nm, he, his = P.next()
    its.append(mcqv("%s's class raises $500 at a bake sale. They spend $68 on supplies and share the rest equally among 16 charities. How much does each charity get?" % nm,
                    "$27", ["$31", "$432", "$26", "$270"],
                    "Step 1: $500 − $68 = $432. Step 2: " + ld_steps(432, 16, end=False) + " Each charity gets $27. "
                    "($31 comes from dividing $500 by 16 and forgetting to take away the $68 first.)"))
    # which number sentence
    its.append(mcq("For a soccer day, 156 students are put into teams of 12. Which number sentence finds the number of teams?",
                   "156 ÷ 12 = 13", ["12 ÷ 156 = 13", "156 × 12 = 1872", "156 − 12 = 144"],
                   "You know the total (156) and the size of each team (12), so divide the total by 12: 156 ÷ 12 = 13 teams. "
                   "Check: 13 × 12 = 156. 12 ÷ 156 divides the wrong way: the total always comes first."))
    # is the answer right?
    nm, he, his = P.next()
    assert divmod(340, 52) == (6, 28)
    its.append(mcq("340 students go to a hockey game. Each bus holds 52 students. %s says 6 buses are enough because 340 ÷ 52 = 6 R 28. Is %s right?" % (nm, he),
                   "No, 7 buses are needed",
                   ["Yes, 6 buses are enough", "No, 28 buses are needed", "No, 5 buses are needed"],
                   "6 buses hold 6 × 52 = 312 students. 340 − 312 = 28 students would have no seat, so one more bus is needed: 7 buses."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: buses, boxes and more", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    f_area = area_svg(32, ["640", "32"], ["20", "1"], "area model for 672 divided by 32")
    f_ld = bracket_svg(672, 32, fs=26, work=True)
    f_rem = bracket_svg(230, 48, fs=26, work=True)
    return (
        "<h2>The big idea</h2>"
        "<p>Dividing asks: how many groups of the divisor fit into the number? "
        "With a two-digit divisor, you <b>estimate</b> first. Round the divisor to the nearest ten, "
        "try a digit, then check it.</p>"
        "<h2>Divide by multiples of 10</h2>"
        "<p>Use a basic fact. Cross out one 0 in each number: 240 ÷ 30 = 24 ÷ 3 = 8. "
        "If the dividend has two zeros, keep one in the answer: 600 ÷ 20 = 60 ÷ 2 = 30.</p>"
        + ex("Estimate", "Estimate 243 ÷ 31.", "Round 31 to 30. 240 is close to 243, and 24 ÷ 3 = 8, so 240 ÷ 30 = 8.",
             "about 8 (exactly 7 R 26)") +
        "<h2>The area model</h2>"
        "<p>Draw a rectangle with the divisor on the side. Split the dividend into parts that are easy multiples "
        "of the divisor, like 10 or 20 times. Divide each part, then add the tops.</p>"
        "<figure class='sn-fig'>" + f_area +
        "<figcaption>672 ÷ 32: 32 × 20 = 640 and 32 × 1 = 32. 640 + 32 = 672, so 672 ÷ 32 = 20 + 1 = 21.</figcaption></figure>"
        "<h2>Long division</h2>"
        "<p>Long division does the same work in place-value order: <b>divide, multiply, subtract, bring down</b>.</p>"
        "<figure class='sn-fig'>" + f_ld +
        "<figcaption>672 ÷ 32: 67 tens ÷ 32 is 2 tens (2 × 32 = 64). 67 − 64 = 3. Bring down 2 to make 32. "
        "32 ÷ 32 = 1. Answer: 21.</figcaption></figure>"
        "<p>The two methods match: the 2 in the tens place is the 20 part of the area model, "
        "and the 640 in the area model is the 64 tens in long division.</p>"
        "<h2>Remainders</h2>"
        "<p>The <b>remainder</b> is what is left when no more full groups fit. It is always <b>less than the divisor</b>.</p>"
        "<figure class='sn-fig'>" + f_rem +
        "<figcaption>230 ÷ 48: 23 is less than 48, so start with 230. Round 48 to 50: about 4. "
        "4 × 48 = 192, 230 − 192 = 38. Answer: 4 R 38.</figcaption></figure>"
        "<p>In a story, decide what the remainder means.</p>"
        + table(["The question asks", "Use the remainder like this", "230 students, 48 on each bus"], [
            ["How many are needed for everyone?", "Round up: add 1", "5 buses"],
            ["How many full groups?", "Leave the remainder out", "4 full buses"],
            ["How many are left over?", "The remainder is the answer", "38 students"],
        ]) +
        "<p>If the leftovers can be split, like metres of rope or litres of water, write the remainder as a "
        "<b>fraction</b> of the divisor: 125 ÷ 12 = 10 R 5 = 10 " + fr(5, 12) + ".</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Ignoring the remainder (230 students need 4 buses)", "4 buses leave 38 students behind: 5 buses"],
            ["First digit in the wrong place (192 ÷ 48 = 40)", "19 is less than 48, so start above the ones: 4"],
            ["Losing a 0 (720 ÷ 24 = 3)", "Every place after the first needs a digit: 30"],
            ["A remainder that is too big (230 ÷ 48 = 3 R 86)", "86 is more than 48, so one more group fits: 4 R 38"],
            ["Writing the remainder as a decimal (125 ÷ 12 = 10.5)", "R 5 means 5 out of 12: 10 " + fr(5, 12)],
        ])
    )


FAQ = [
    {"q": "What division do Grade 5 students learn in Ontario?",
     "a": "The Ontario math curriculum asks Grade 5 students to divide three-digit whole numbers by two-digit whole numbers, using the area model and long division, and to show the remainder in a way that fits the problem."},
    {"q": "How do you divide by a two-digit number?",
     "a": "Round the divisor to the nearest ten to estimate each digit, then multiply, subtract and bring down the next digit. If the product is too big, try one less; if what is left is the divisor or more, try one more."},
    {"q": "How does the area model help with division?",
     "a": "It splits the dividend into easy parts, such as 32 × 20 = 640 and 32 × 1 = 32 for 672 ÷ 32. Adding the parts on top (20 + 1 = 21) gives the quotient, and it shows why long division works."},
    {"q": "What should you do with a remainder in a word problem?",
     "a": "Round up when everyone must fit, like students on buses. Leave it out when you count full boxes, give the remainder when the question asks what is left, and write it as a fraction when the leftovers can be split."},
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
    rnd = random.Random(45805)
    P = People(rnd)
    used = set()
    sets = [set_tens(rnd, used), set_area(rnd, used), set_exact(rnd, used, P), set_remainders(rnd, used, P), set_story(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "dividing-by-two-digit-numbers", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Dividing by Two-Digit Numbers",
        "seo_title": "Grade 5 Dividing by Two-Digit Numbers Worksheets: Area Model, Long Division, Remainders (Free, Ontario)",
        "short_title": "Dividing by two-digit numbers",
        "domain": "Number",
        "standard_code": "Grade 5: B2.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the division of three-digit whole numbers by two-digit whole numbers using the area model and using algorithms, and make connections between the two methods, while expressing any remainder appropriately",
        "meta_desc": "Free Grade 5 math worksheets on dividing three-digit numbers by two-digit numbers for the Ontario curriculum: multiples of 10, the area model, long division, remainders as whole numbers, fractions or rounded up, and word problems. 100 questions with an answer key.",
        "key_big": "Round the divisor to estimate each digit, then check it. The remainder is always less than the divisor.",
        "key_sub": "672 ÷ 32: the area model splits 672 into 640 + 32, so the answer is 20 + 1 = 21. In a story, decide what the remainder means: round up for buses, leave it out for full boxes, or write it as a fraction.",
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
    mark_large(u, "area model")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
