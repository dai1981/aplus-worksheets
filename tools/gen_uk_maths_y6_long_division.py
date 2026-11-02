# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Long division and short division by two-digit numbers
(National Curriculum in England, Year 6: Addition, subtraction, multiplication and division)
  python3 tools/gen_uk_maths_y6_long_division.py
Every quotient and remainder comes from divmod / Fraction, and every figure is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
Year 6 style: numbers 1,000 and above are written with commas (not inside the written layouts). Remainders are written "r".
"""
import json, os, random, re
from fractions import Fraction
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
MONO = "monospace"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
PLACE = ["ones", "tens", "hundreds", "thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """1,000 and above with commas."""
    return "{:,}".format(n)


def qr(q, r):
    return "%s r %d" % (f(q), r) if r else f(q)


def V(x):
    """Value key of a plain number."""
    return Fraction(x)


def R(q, r):
    """Value key of a 'q r r' answer (never equal to a plain number)."""
    return ("r", q, r) if r else Fraction(q)


def dec(x):
    """Exact decimal text of a Fraction with a terminating decimal: 309/4 -> 77.25."""
    x = Fraction(x)
    d = Decimal(x.numerator) / Decimal(x.denominator)
    s = format(d.normalize(), "f")
    assert Fraction(s) == x, (x, s)
    return f(int(s.split(".")[0])) + ("." + s.split(".")[1] if "." in s else "")


def money(x):
    x = Fraction(x)
    assert (x * 100).denominator == 1
    p = int(x * 100)
    return "£%s.%02d" % (f(p // 100), p % 100)


def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def mixed(x):
    """Mixed number HTML for a Fraction: 36 1/3."""
    x = Fraction(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return f(w)
    return (f(w) + " " if w else "") + fr(r, x.denominator)


def mx(w, n, d):
    """Mixed number exactly as written (not simplified), for a pupil's mistake."""
    return f(w) + " " + fr(n, d)


def mixed_txt(x):
    x = Fraction(x)
    w, r = divmod(x.numerator, x.denominator)
    return "%s %d/%d" % (f(w), r, x.denominator) if r else f(w)


def positive(v):
    if isinstance(v, tuple):
        return v[1] > 0 and v[2] > 0
    if isinstance(v, str):
        return True
    return v > 0


def mcq(q, correct, cands, e):
    """correct and cands are (label, value). 4 choices with 4 different values. Positions are set by balance()."""
    lab, val = correct
    seen_l, seen_v = {lab}, {val}
    pick = []
    for c, v in cands:
        if c in seen_l or v in seen_v or not positive(v):
            continue
        seen_l.add(c)
        seen_v.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [lab] + pick, "a": 0, "e": e}


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


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, MONO, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %s × %d + %d = %s." % (f(q), d, r, f(n))
    return "Check: %s × %d = %s." % (f(q), d, f(n))


# ------------------------------------------------------------ short division (bus stop)
def sd_rows(n, d):
    """Short division, digit by digit: list of (digit index, number divided, quotient digit or None, remainder carried)."""
    rows, carry, started = [], 0, False
    ds = str(n)
    for i, ch in enumerate(ds):
        cur = carry * 10 + int(ch)
        q, carry = divmod(cur, d)
        if q or started or i == len(ds) - 1:
            started = True
            rows.append((i, cur, q, carry))
        else:
            rows.append((i, cur, None, carry))
    return rows


def sd_steps(n, d, end=True):
    rows = sd_rows(n, d)
    L = len(rows)
    parts = []
    for i, cur, q, c in rows:
        if q is None:
            parts.append("%d ÷ %d: %d does not go into %d, so carry the %d to make %d"
                         % (cur, d, d, cur, cur, rows[i + 1][1]))
        elif c and i < L - 1:
            parts.append("%d ÷ %d = %d r %d, carry the %d to make %d" % (cur, d, q, c, c, rows[i + 1][1]))
        elif c:
            parts.append("%d ÷ %d = %d r %d" % (cur, d, q, c))
        else:
            parts.append("%d ÷ %d = %d" % (cur, d, q))
    q, r = divmod(n, d)
    s = "; ".join(parts) + ". "
    if end:
        return s + "Answer: %s. %s" % (qr(q, r), check_txt(n, d))
    return s + "So %s ÷ %d = %s." % (f(n), d, qr(q, r))


def bus_svg(n, d, work=False, fs=24):
    """Short division ('bus stop'). With work=True the quotient, the small carried remainders
    and the remainder are drawn."""
    ds = str(n)
    L = len(ds)
    rows = sd_rows(n, d)
    cl = max([len(str(c)) for (_, _, _, c) in rows[:-1] if c] + [0]) if work else 0
    cw = fs * (0.78 + (0.42 * cl if cl else 0))
    dw = len(str(d)) * fs * 0.62
    x0 = 8 + dw + 14
    top = fs * 1.3 if work else 6
    bh = fs * 1.3
    by = top + bh - fs * 0.3
    s = []

    def col(j):
        return x0 + fs * 0.62 + cw * j

    for j, ch in enumerate(ds):
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (col(j), by, fs, INK, ch))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 8, by, fs, GREEN, d))
    right = col(L - 1) + fs * 0.5
    W = right + 6
    if work:
        cfs = int(fs * 0.58)
        for i, cur, q, c in rows:
            if q is not None:
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                         % (col(i), top - 7, fs, GREEN, q))
            if c and i < L - 1:
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
                         % (col(i + 1) - fs * 0.3, by - fs * 0.38, cfs, RED, c))
        r = n % d
        if r:
            rt = "r %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>"
                     % (right + 6, top - 7, fs, GREEN, rt))
            W = max(W, right + 6 + len(rt) * fs * 0.62 + 6)
    s.append("<path d='M%.1f %.1f V%.1f M%.1f %.1f H%.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0, top + bh, top, x0 - 1.5, top, right, INK))
    H = top + bh + 6
    label = ("%s divided by %d worked out with short division" if work else "%s divided by %d written as short division") % (f(n), d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label)


# ------------------------------------------------------------ long division
def ld_rows(n, d):
    """The steps of long division: list of (index of digit, partial dividend, quotient digit), remainder."""
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


def ld_steps(n, d, end=True):
    """Divide, multiply, subtract, bring down — in words."""
    ds = str(n)
    steps, r = ld_rows(n, d)
    q = n // d
    parts = []
    for k, (i, cur, qd) in enumerate(steps):
        if k == 0:
            head = ("%d is less than %d, so start with %d. " % (int(ds[:i]), d, cur)) if i > 0 else ""
            parts.append(head + "%d ÷ %d = %d: %d × %d = %d, %d − %d = %d."
                         % (cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
        elif cur == 0:
            parts.append("Bring down %s: there is nothing to divide, so write 0 in the answer." % ds[i])
        elif qd == 0:
            parts.append("Bring down %s to make %d: %d does not go into %d, so write 0 in the answer." % (ds[i], cur, d, cur))
        else:
            parts.append("Bring down %s to make %d: %d ÷ %d = %d: %d × %d = %d, %d − %d = %d."
                         % (ds[i], cur, cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
    if r:
        parts.append("Nothing is left to bring down, so the remainder is %d." % r)
    if end:
        parts.append("Answer: %s. %s" % (qr(q, r), check_txt(n, d)))
    else:
        parts.append("So %s ÷ %d = %s." % (f(n), d, qr(q, r)))
    return " ".join(parts)


def ld_svg(n, d, fs=24, work=False):
    """Long division layout (same 'bus stop' shape as short division). With work=True the full
    worked example (answer, products, differences, brought-down digits) is drawn."""
    cw = fs * 0.85
    ds = str(n)
    L = len(ds)
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18 + (cw if work else 0)                  # room for the minus signs
    steps, r = ld_rows(n, d)
    q = n // d
    rh = fs * 1.25
    top = (rh + 6) if work else 6
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def digits_at(txt, last, y, colr=INK):
        for k, ch in enumerate(reversed(txt)):
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (col(last - k), y, fs, colr, ch))

    bh = rh + 2
    by = top + bh - fs * 0.3
    digits_at(ds, L - 1, by)
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 14, by, fs, GREEN, d))
    W = x0 + cw * L + 8
    H = top + bh + 6
    if work:
        digits_at(str(q), L - 1, top - 8, GREEN)
        if r:
            rt = "r %d" % r
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
                     % (col(left) - cw * 0.9, y, fs, RED))
            ly = y + fs * 0.3
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (col(left) - cw * 1.3, ly, col(i) + cw * 0.5, ly, INK))
            y += rh
            if k + 1 < len(steps):
                nxt = steps[k + 1][1]
                digits_at(str(nxt), steps[k + 1][0], y)
                for j in range(i + 1, steps[k + 1][0] + 1):     # arrow for each digit brought down
                    s.append("<path d='M%.1f %.1f V%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='3 3' "
                             "marker-end='url(#ah)'/>" % (col(j), by + fs * 0.3, y - fs * 0.95, GREEN))
            else:
                digits_at(str(cur - p), i, y, GREEN if cur - p else INK)
        H = y + 12
        s.insert(0, "<defs><marker id='ah' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='6' markerHeight='6' "
                    "orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN)
    s.append("<path d='M%.1f %.1f V%.1f M%.1f %.1f H%.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 8, top + bh, top, x0 - 9.5, top, x0 + cw * L + 4, INK))
    label = ("%s divided by %d worked out with long division" if work else "%s divided by %d written as long division") % (f(n), d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label)


def first_est(n, d):
    D = (d + 5) // 10 * 10
    return D, max(1, min(9, n // D))


def est_steps(n, d):
    """One-digit answer: estimate with the rounded divisor, then adjust."""
    q, r = divmod(n, d)
    D, e = first_est(n, d)
    parts = []
    if n // D > 9:
        parts.append("Round %d to %d. %d ÷ %d is about %d, but the answer has only one digit, so try 9." % (d, D, n, D, n // D))
    elif D != d:
        parts.append("Round %d to %d. %d ÷ %d is about %d, so try %d." % (d, D, n, D, e, e))
    else:
        parts.append("%d ÷ %d is about %d, so try %d." % (n, d, e, e))
    while e * d > n:
        parts.append("%d × %d = %d, which is more than %d, so %d is too big. Try %d." % (e, d, e * d, n, e, e - 1))
        e -= 1
    while n - e * d >= d:
        parts.append("%d × %d = %d and %d − %d = %d, which is not less than %d, so %d is too small. Try %d."
                     % (e, d, e * d, n, e * d, n - e * d, d, e, e + 1))
        e += 1
    assert e == q
    parts.append("%d × %d = %d and %d − %d = %d." % (q, d, q * d, n, q * d, r))
    parts.append("Answer: %s. %s" % (qr(q, r), check_txt(n, d)))
    return " ".join(parts)


# ------------------------------------------------------------ typical mistakes
def drop_zero(q):
    """Missing a zero in the answer (260 -> 26, 302 -> 32)."""
    s = str(q).replace("0", "")
    return int(s) if s else 0


def ignore_carry(n, d):
    """Divided each digit on its own and threw the remainders away (936 ÷ 4 -> 2, 0, 1 -> 201)."""
    s = "".join(str(int(c) // d) for c in str(n)).lstrip("0")
    return int(s) if s else 0


def exact_cands(n, d):
    q = n // d
    c = []
    if "0" in str(q):
        c.append(drop_zero(q))
    ic = ignore_carry(n, d)
    if len(str(ic)) == len(str(q)):
        c.append(ic)
    c += [q * 10, q + 10, q - 10, q + 1, q - 1]
    return [(f(x), V(x)) for x in c if x > 0]


def rem_cands(n, d):
    q, r = divmod(n, d)
    c = []
    if "0" in str(q):
        c.append((qr(drop_zero(q), r), R(drop_zero(q), r)))
    c += [(qr(q - 1, r + d), R(q - 1, r + d)),            # remainder bigger than the divisor
          (qr(q, d - r), R(q, d - r)),                    # wrote how many more are needed
          (f(q), V(q)),                                   # left the remainder out
          (qr(q + 1, r), R(q + 1, r)), (qr(q - 1, r), R(q - 1, r)), (qr(q + 10, r), R(q + 10, r))]
    return c


def div_cands(n, d):
    return rem_cands(n, d) if n % d else exact_cands(n, d)


# ============================================================ set 1: short division
def pick_exact(rnd, used, d, lo, hi, zero=None, carries=True):
    while True:
        q = rnd.randint(-(-lo // d), hi // d)
        n = q * d
        if n in used or n % 10 == 0 or (zero is not None and ("0" in str(q)) != zero):
            continue
        if carries and sum(1 for row in sd_rows(n, d)[:-1] if row[3]) < (1 if zero else 2):
            continue
        used.add(n)
        return n


def pick_rem(rnd, used, d, lo, hi):
    while True:
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if n in used or r < 2 or "0" in str(q) or sum(1 for row in sd_rows(n, d)[:-1] if row[3]) < 2:
            continue
        used.add(n)
        return n


def sd_item(n, d, figure):
    q, r = divmod(n, d)
    qtxt = (fig(bus_svg(n, d)) + "Use short division.") if figure else "Use short division to work out %s ÷ %d." % (f(n), d)
    corr = (qr(q, r), R(q, r))
    return mcq(qtxt, corr, div_cands(n, d), sd_steps(n, d))


def set_short(rnd, used, P):
    its = []
    # 1-digit divisors, exact (2 with a zero in the answer)
    for i, (d, lo, hi, z) in enumerate([(4, 500, 999, False), (6, 1000, 5999, False), (7, 1000, 6999, False),
                                        (8, 2000, 9999, False), (3, 1000, 2999, True), (6, 4000, 9999, True)]):
        its.append(sd_item(pick_exact(rnd, used, d, lo, hi, z), d, i % 2 == 0))
    # 1-digit divisors, remainder
    for i, d in enumerate([7, 9, 8]):
        its.append(sd_item(pick_rem(rnd, used, d, 1000, 9999), d, i == 1))
    # easy 2-digit divisors
    for i, d in enumerate([11, 12, 15, 25, 12]):
        its.append(sd_item(pick_exact(rnd, used, d, 400 if d < 15 else 1000, 9999, False), d, i % 2 == 1))
    for i, d in enumerate([11, 25]):
        its.append(sd_item(pick_rem(rnd, used, d, 1000, 9999), d, i == 0))
    # what do you divide next?
    for d in (4, 7):
        name, he, his = P.next()
        while True:
            n = rnd.randint(100, 999)
            a, b = int(str(n)[0]), int(str(n)[1])
            if a > d and a % d and b > 0 and n not in used and a % d + b != b and (a % d) * 10 + b >= d:
                break
        used.add(n)
        q1, c1 = divmod(a, d)
        nxt = c1 * 10 + b
        e = ("%d ÷ %d = %d r %d. The remainder %d is %d hundred%s, which is %d tens. Write it as a small %d in front of the %d, "
             "so you divide %d next: %d ÷ %d = %d r %d. %s"
             % (a, d, q1, c1, c1, c1, "" if c1 == 1 else "s", c1 * 10, c1, b, nxt, nxt, d, nxt // d, nxt % d,
                "The whole answer: " + qr(n // d, n % d) + "."))
        its.append(mcq("%s uses short division for %d ÷ %d. First, %d ÷ %d = %d r %d. What does %s divide next?"
                       % (name, n, d, a, d, q1, c1, he), (str(nxt), V(nxt)),
                       [(str(b), V(b)), (str(c1 + b), V(c1 + b)), (str(b * 10 + c1), V(b * 10 + c1)), (str(nxt + 10), V(nxt + 10))], e))
    # check with the inverse
    for d in (6, 12):
        n = pick_exact(rnd, used, d, 1000, 4999, False)
        q = n // d
        good = "%s × %d" % (f(q), d)
        its.append(mcq("%s ÷ %d = %s. Which calculation checks this answer?" % (f(n), d, f(q)), (good, "m"),
                       [("%s ÷ %d" % (f(q), d), "d"), ("%s + %d" % (f(q), d), "a"), ("%s × %d" % (f(n), d), "n")],
                       "Multiplication is the inverse of division. %s × %d = %s, which matches, so the answer is right." % (f(q), d, f(n))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Short division: the bus stop method", "items": its}


# ============================================================ set 2: 3-digit ÷ 2-digit (long division)
def pick_ld(rnd, used, lo, hi, rem, qlo, qhi, dlo=12, dhi=98, zero=False):
    while True:
        d = rnd.randint(dlo, dhi)
        if d % 10 == 0 or d in (11, 12, 15, 25):
            continue
        if rem:
            n = rnd.randint(lo, hi)
            q, r = divmod(n, d)
            if r < 2:
                continue
        else:
            q = rnd.randint(qlo, qhi)
            n = q * d
        q = n // d
        if not (lo <= n <= hi) or n in used or not (qlo <= q <= qhi) or ("0" in str(q)) != zero:
            continue
        used.add(n)
        return n, d


def ld_item(n, d, figure):
    q, r = divmod(n, d)
    qtxt = (fig(ld_svg(n, d)) + "Use long division.") if figure else "Use long division to work out %s ÷ %d." % (f(n), d)
    return mcq(qtxt, (qr(q, r), R(q, r)), div_cands(n, d), ld_steps(n, d))


def set_long3(rnd, used, P):
    its = []
    for i, rem in enumerate([False, False, False, False, True, True, True, True]):
        n, d = pick_ld(rnd, used, 300, 999, rem, 11, 49)
        its.append(ld_item(n, d, i % 2 == 0))
    # one-digit answers: estimate, then adjust
    for kind in ("up", "down", "up"):
        while True:
            d = rnd.randint(13, 89)
            q = rnd.randint(3, 9)
            r = rnd.randint(1, d - 1)
            n = q * d + r
            if d % 10 == 0 or not (100 <= n <= 999) or n in used:
                continue
            D, e = first_est(n, d)
            if (kind == "up" and e == q - 1) or (kind == "down" and e == q + 1):
                break
        used.add(n)
        cands = [(qr(e, n - e * d), R(e, n - e * d))] if e < q else [(f(e), V(e))]
        its.append(mcq("What is %d ÷ %d?" % (n, d), (qr(q, r), R(q, r)), cands + rem_cands(n, d), est_steps(n, d)))
    # which multiple do you subtract? (list the multiples)
    for _ in range(3):
        n, d = pick_ld(rnd, used, 300, 999, rnd.random() < 0.5, 21, 89, 13, 39)
        steps, _ = ld_rows(n, d)
        i, cur, qd = steps[0]
        mult = ", ".join(str(d * k) for k in range(1, 6))
        e = ("List the multiples of %d: %s, … The largest one that is not more than %d is %d × %d = %d. "
             "%d − %d = %d. Then bring down the next digit. The whole answer: %s ÷ %d = %s."
             % (d, mult, cur, qd, d, qd * d, cur, qd * d, cur - qd * d, f(n), d, qr(n // d, n % d)))
        cands = [(str(m), V(m)) for m in [(qd + 1) * d, (qd - 1) * d, (qd + 2) * d, (qd - 2) * d] if m > 0]
        its.append(mcq("You use long division for %d ÷ %d. The first step is %d ÷ %d. Which multiple of %d do you subtract from %d?"
                       % (n, d, cur, d, d, cur), (str(qd * d), V(qd * d)), cands, e))
    # what do you divide next?
    for _ in range(3):
        while True:
            n, d = pick_ld(rnd, used, 300, 999, rnd.random() < 0.5, 11, 49)
            steps, _ = ld_rows(n, d)
            i, cur, qd = steps[0]
            diff = cur - qd * d
            b = int(str(n)[i + 1])
            if diff > 0 and b > 0 and diff * 10 + b != b * 10 + diff and diff + b != b:
                break
        nxt = diff * 10 + b
        e = ("%d ÷ %d = %d. %d × %d = %d and %d − %d = %d. Bring down the %d next to the %d to make %d. "
             "Then %d ÷ %d = %d. The whole answer: %s." % (cur, d, qd, qd, d, qd * d, cur, qd * d, diff, b, diff, nxt,
                                                          nxt, d, nxt // d, qr(n // d, n % d)))
        its.append(mcq("You use long division for %d ÷ %d. After %d − %d = %d, you bring down the next digit. What do you divide next?"
                       % (n, d, cur, qd * d, diff, ), (str(nxt), V(nxt)),
                       [(str(b), V(b)), (str(diff + b), V(diff + b)), (str(b * 10 + diff), V(b * 10 + diff)), (str(nxt + d), V(nxt + d))], e))
    # the remainder
    for _ in range(3):
        n, d = pick_ld(rnd, used, 300, 999, True, 11, 49)
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), (str(r), V(r)),
                       [(str(q), V(q)), (str(d - r), V(d - r)), (str(r + d), V(r + d)), (str(d), V(d))],
                       "The question asks for the remainder, not the answer to the division. " + ld_steps(n, d)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Long division: 3-digit numbers ÷ 2-digit numbers", "items": its}


# ============================================================ set 3: 4-digit ÷ 2-digit, SATs style
def zero_pick(rnd, used, shape, rem):
    while True:
        d = rnd.randint(12, 49)
        if d % 10 == 0:
            continue
        q = int(shape.replace("x", str(rnd.randint(1, 9)), 1).replace("y", str(rnd.randint(1, 9))))
        r = rnd.randint(2, d - 1) if rem else 0
        n = q * d + r
        if 1000 <= n <= 9999 and n not in used and (n % 10 or shape.endswith("0")):
            used.add(n)
            return n, d


def set_long4(rnd, used, P):
    its = []
    for i in range(7):                                       # exact, 2- or 3-digit answers
        n, d = pick_ld(rnd, used, 1000, 9999, False, 21, 199 if i < 4 else 99, 13, 49 if i < 4 else 98)
        its.append(ld_item(n, d, i % 2 == 0))
    for i, shape in enumerate(["x0y", "xy0", "x0y"]):        # zeros in the answer
        n, d = zero_pick(rnd, used, shape, False)
        its.append(ld_item(n, d, i != 1))
    for i in range(4):                                       # remainders
        n, d = pick_ld(rnd, used, 1000, 9999, True, 21, 199)
        its.append(ld_item(n, d, i % 2 == 1))
    # missing a zero
    for shape in ("xy0", "x0y"):
        name, he, his = P.next()
        n, d = zero_pick(rnd, used, shape, False)
        q = n // d
        wq = drop_zero(q)
        its.append(mcq("%s works out %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, f(wq), he),
                       ("%s missed a 0 in the answer" % cap(he), "z"),
                       [("%s forgot the remainder" % cap(he), "f"), ("%s divided the wrong way round" % cap(he), "w"),
                        ("There is no mistake", "n")],
                       "Check: %s × %d = %s, not %s. Every digit you bring down needs a digit in the answer, even 0. "
                       % (f(wq), d, f(wq * d), f(n)) + ld_steps(n, d)))
    # remainder bigger than the divisor
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick_ld(rnd, used, 1000, 9999, True, 21, 199)
        q, r = divmod(n, d)
        its.append(mcq("%s works out %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, qr(q - 1, r + d), he),
                       ("The remainder is too big", "b"),
                       [("%s missed a 0 in the answer" % cap(he), "z"), ("%s forgot to bring down a digit" % cap(he), "g"),
                        ("There is no mistake", "n")],
                       "A remainder must be less than the divisor. %d is more than %d, so %d goes in once more: %d − %d = %d. "
                       "The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    # how many digits in the answer
    for big in (True, False):
        while True:
            d = rnd.randint(13, 98)
            n = rnd.randint(1000, 9999)
            if d % 10 and n not in used and n % d and (int(str(n)[:2]) >= d) == big:
                break
        used.add(n)
        q = n // d
        L = len(str(q))
        why = ("%d is at least %d, so the answer starts in the hundreds place." % (int(str(n)[:2]), d)) if big else (
            "%d is less than %d, so there are no hundreds. The answer starts in the tens place." % (int(str(n)[:2]), d))
        its.append(mcq("How many digits will the answer to %s ÷ %d have (not counting the remainder)?" % (f(n), d),
                       ("%d digits" % L, L), [("%d digits" % x, x) for x in (4, 3, 2) if x != L] + [("1 digit", 1)],
                       why + " %s ÷ %d = %s." % (f(n), d, qr(q, n % d))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Long division: 4-digit numbers ÷ 2-digit numbers", "items": its}


# ============================================================ set 4: remainders as r, fractions and decimals
def pick_frac(rnd, used, simp):
    while True:
        d = rnd.randint(12, 48)
        n = rnd.randint(1000, 4999) if rnd.random() < 0.6 else rnd.randint(300, 999)
        q, r = divmod(n, d)
        if d % 10 == 0 or n in used or r < 2 or (Fraction(r, d).denominator != d) != simp:
            continue
        used.add(n)
        return n, d


def pick_dec(rnd, used, dp):
    while True:
        d = rnd.choice([16, 25, 20, 40, 50, 24, 32, 15, 12, 35, 45])
        n = rnd.randint(500, 4999)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        if n in used or r == 0 or n % 10 == 0 or (x * 10 ** dp).denominator != 1 or (x * 10 ** (dp - 1)).denominator == 1:
            continue
        used.add(n)
        return n, d


def set_remainders(rnd, used, P):
    its = []
    # as r
    for i in range(3):
        n, d = pick_ld(rnd, used, 1000, 9999, True, 21, 199)
        q, r = divmod(n, d)
        its.append(mcq("Work out %s ÷ %d. Give the remainder as a whole number." % (f(n), d), (qr(q, r), R(q, r)),
                       rem_cands(n, d), ld_steps(n, d)))
    # as a fraction (4 that simplify, 3 that do not)
    for simp in (True, True, True, True, False, False, False):
        n, d = pick_frac(rnd, used, simp)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = ("%s ÷ %d = %s. The remainder %d is %d out of %d, so the fraction is %s."
             % (f(n), d, qr(q, r), r, r, d, fr(r, d)))
        if simp:
            g = r // rf.numerator
            e += " Simplify: divide the numerator and the denominator by %d to get %s." % (g, fr(rf.numerator, rf.denominator))
        e += " Answer: %s." % mixed(x)
        cands = []
        if simp:
            g = r // rf.numerator
            cands.append((mx(q, r // g, d), q + Fraction(r // g, d)))         # divided the numerator only
        elif r < q:
            cands.append((mx(q, r, q), q + Fraction(r, q)))                     # remainder over the answer
        cands += [(mixed(q + Fraction(d - r, d)), q + Fraction(d - r, d)),     # used the part that is missing
                  (mixed(q + 1 + rf), q + 1 + rf), (mixed(q - 1 + rf), q - 1 + rf)]
        its.append(mcq("Work out %s ÷ %d. Give your answer as a mixed number%s." % (f(n), d, " in its simplest form" if simp else ""),
                       (mixed(x), x), cands, e))
    # as a decimal
    for dp in (1, 2, 2, 2, 1, 2):
        n, d = pick_dec(rnd, used, dp)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = ("%s ÷ %d = %s. The remainder %d out of %d is %s = %d ÷ %d = %s. So the answer is %s, not %s."
             % (f(n), d, qr(q, r), r, d, fr(r, d), r, d, dec(rf), dec(x), f(q) + "." + str(r)))
        cands = [(f(q) + "." + str(r), Fraction(f(q).replace(",", "") + "." + str(r))),    # r written as a decimal
                 (dec(q + 1 - rf), q + 1 - rf), (dec(q + 1 + rf), q + 1 + rf), (dec(q - 1 + rf), q - 1 + rf)]
        its.append(mcq("Work out %s ÷ %d. Give your answer as a decimal." % (f(n), d), (dec(x), x), cands, e))
    # rounded to 1 decimal place
    for _ in range(2):
        while True:
            d = rnd.choice([12, 14, 18, 21, 22, 24, 26, 27, 28, 32, 36])
            n = rnd.randint(500, 4999)
            x = Fraction(n, d)
            t = int(x * 10)                                     # tenths, cut off
            h = int(x * 100) % 10
            if n in used or x.denominator == 1 or h < 5 or (x * 100).denominator == 1 or t % 10 == 9:
                continue
            break
        used.add(n)
        q, r = divmod(n, d)
        good = Fraction(t + 1, 10)
        e = ("%s ÷ %d = %s, and %s ÷ %d = %s… (keep dividing: add a decimal point and zeros). "
             "The hundredths digit is %d, which is 5 or more, so round the tenths up: %s."
             % (f(n), d, qr(q, r), f(n), d, dec(Fraction(int(x * 1000), 1000)), h, dec(good)))
        cands = [(dec(Fraction(t, 10)), Fraction(t, 10)),
                 (f(q) + "." + str(r) if r < 10 else dec(Fraction(t + 2, 10)), Fraction(q * 10 + r, 10) if r < 10 else Fraction(t + 2, 10)),
                 (f(q + 1), V(q + 1)), (dec(Fraction(t - 1, 10)), Fraction(t - 1, 10))]
        its.append(mcq("Work out %s ÷ %d. Give your answer to 1 decimal place." % (f(n), d), (dec(good), good), cands, e))
    # remainder written as a decimal by mistake
    for d in (8, 25):
        name, he, his = P.next()
        while True:
            n = rnd.randint(1000, 4999) if d == 8 else rnd.randint(1000, 2999)
            q, r = divmod(n, d)
            if n not in used and r > 1 and Fraction(r, d) != Fraction(r, 10) and n % 10:
                break
        used.add(n)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        wrong = f(q) + "." + str(r)
        cands = [(wrong, Fraction(q * 10 + r, 10) if r < 10 else Fraction(q * 100 + r, 100)),
                 (dec(q + 1 - rf), q + 1 - rf), (dec(q + Fraction(1, r)), q + Fraction(1, r)) if (Fraction(1, r) * 100).denominator == 1 else
                 (dec(q + 1 + rf), q + 1 + rf), (dec(q - 1 + rf), q - 1 + rf)]
        its.append(mcq("%s works out %s ÷ %d = %s and writes the answer as %s. What is the correct decimal answer?"
                       % (name, f(n), d, qr(q, r), wrong), (dec(x), x), cands,
                       "The remainder %d is not %s. It means %d out of %d, so it is %s = %d ÷ %d = %s. "
                       "The answer is %s." % (r, "0." + str(r), r, d, fr(r, d), r, d, dec(rf), dec(x))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Remainders as whole numbers, fractions and decimals", "items": its}


# ============================================================ set 5: word problems
def find(rnd, lo, hi, ds, kind, used):
    while True:
        d = rnd.choice(ds)
        if kind == "exact":
            q = rnd.randint(-(-lo // d), hi // d)
            n = q * d
            if n % 10 == 0 or n in used:
                continue
            used.add(n)
            return n, d
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if kind in ("frac", "dec", "money"):
            if r == 0:
                continue
            if kind != "frac" and (Fraction(n, d) * 100).denominator != 1:
                continue
            if kind == "frac" and Fraction(r, d).denominator > 12:
                continue
        if r > 1 and r not in (q, q + 1, q - 1) and n not in used and n % 10:
            used.add(n)
            return n, d


def story(kind, text, lo, hi, ds, one, many, rnd, P, used, why=None):
    name, he, his = P.next()
    n, d = find(rnd, lo, hi, ds, kind, used)
    q, r = divmod(n, d)
    q_txt = text.format(n=f(n), d=d, name=name, he=he, He=cap(he), his=his)
    U = lambda k: units(k, one, many)
    base = "Divide: " + ld_steps(n, d, end=False) + " "
    rq = (qr(q, r), R(q, r))
    if kind == "up":
        e = base + "%s %s %s not enough: %s %s. You need 1 more, so the answer is %s." % (
            f(q), many if q != 1 else one, "are" if q != 1 else "is", units(r, why[0], why[1]), why[2], U(q + 1))
        return mcq(q_txt, (U(q + 1), V(q + 1)), [(U(q), V(q)), rq, (U(r), V(r)), (U(q + 2), V(q + 2))], e)
    if kind == "down":
        e = base + "The %s left over %s not enough %s, so ignore the remainder. The answer is %s." % (
            units(r, why[0], why[1]), "is" if r == 1 else "are", why[2], U(q))
        return mcq(q_txt, (U(q), V(q)), [(U(q + 1), V(q + 1)), rq, (U(r), V(r)), (U(q - 1), V(q - 1))], e)
    if kind == "rem":
        e = base + "The question asks how many are left over. That is the remainder: %s." % U(r)
        return mcq(q_txt, (U(r), V(r)), [(U(q), V(q)), (U(d - r), V(d - r)), rq, (U(r + d), V(r + d))], e)
    if kind == "frac":
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = (base + "The remainder can be shared too: %d %s ÷ %d = %s %s. "
             % (r, many, d, fr(r, d), one if r < d else many))
        if rf.denominator != d:
            e += "Simplify: %s = %s. " % (fr(r, d), fr(rf.numerator, rf.denominator))
        e += "Each gets %s %s." % (mixed(x), many)
        return mcq(q_txt, (mixed(x) + " " + many, x),
                   [rq, (U(q), V(q)),
                    (mixed(q + 1 - rf) + " " + many, q + 1 - rf), (U(q + 1), V(q + 1))], e)
    if kind == "dec":
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = (base + "Lengths can be split into parts, so write the remainder as a decimal: %s = %d ÷ %d = %s. "
             "Each piece is %s %s, not %s.%d %s." % (fr(r, d), r, d, dec(rf), dec(x), many, f(q), r, many))
        wrong = Fraction(q * 10 ** len(str(r)) + r, 10 ** len(str(r)))
        return mcq(q_txt, (dec(x) + " " + many, x),
                   [(f(q) + "." + str(r) + " " + many, wrong), rq, (U(q), V(q)),
                    (dec(q + 1 - rf) + " " + many, q + 1 - rf), (U(q + 1), V(q + 1))], e)
    if kind == "money":
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = (base + "Money can be shared into pence, so write the remainder as a decimal: £%d ÷ %d = %s. "
             "Each share is %s." % (r, d, money(rf), money(x)))
        wrong = Fraction(q * 10 ** len(str(r)) + r, 10 ** len(str(r)))
        return mcq(q_txt, (money(x), x),
                   [(money(wrong), wrong), rq, ("£" + f(q), V(q)), (money(q + 1 - rf), q + 1 - rf), ("£" + f(q + 1), V(q + 1))], e)
    # exact
    e = base + "There is no remainder, so the answer is %s." % U(q)
    return mcq(q_txt, (U(q), V(q)), [(U(int(c.replace(",", ""))), v) for c, v in exact_cands(n, d)], e)


def set_story(rnd, P, used):
    S = [
        ("up", "A school is taking {n} pupils and adults on a trip to the seaside. Each coach has {d} seats. How many coaches are needed?",
         310, 690, [49, 53, 57], "coach", "coaches", ("person", "people", "would still need a seat")),
        ("up", "A school library is packing {n} books into boxes. Each box holds {d} books. How many boxes are needed for all the books?",
         1050, 1990, [24, 32, 36], "box", "boxes", ("book", "books", "would still need a box")),
        ("up", "There are {n} people coming to a summer fair lunch. Each table seats {d} people. How many tables are needed so everyone has a seat?",
         210, 490, [12, 14, 16], "table", "tables", ("person", "people", "would still need a seat")),
        ("up", "A ferry carries {d} cars on each crossing. {n} cars are waiting in the car park. How many crossings are needed to take every car?",
         310, 690, [18, 22, 26], "crossing", "crossings", ("car", "cars", "would still be waiting")),
        ("up", "{name} is putting {n} photos into an album. Each page holds {d} photos. How many pages does {he} need?",
         300, 690, [12, 16], "page", "pages", ("photo", "photos", "would still need a page")),
        ("down", "A factory has {n} biscuits. It puts {d} biscuits in each packet. How many full packets can it make?",
         2010, 3990, [24, 28, 36], "packet", "packets", ("biscuit", "biscuits", "to fill another packet")),
        ("down", "A farm collected {n} eggs. It packs them in boxes of {d}. How many boxes can it fill completely?",
         1010, 2490, [12, 15, 18], "box", "boxes", ("egg", "eggs", "to fill another box")),
        ("down", "A school has £{n} to spend on footballs. Each football costs £{d}. How many footballs can the school buy?",
         310, 890, [14, 16, 18], "football", "footballs", ("pound", "pounds", "to buy another football")),
        ("down", "{name} has a roll of ribbon {n} cm long. {He} cuts it into pieces that are each {d} cm long. How many full pieces can {he} cut?",
         510, 990, [15, 24, 35], "piece", "pieces", ("centimetre", "centimetres", "to cut another piece")),
        ("down", "There are {n} children at a football tournament. Each team needs exactly {d} players. How many full teams can be made?",
         150, 290, [11], "team", "teams", ("child", "children", "to make another team")),
        ("rem", "{name} shares {n} stickers equally among {d} pupils. Each pupil gets as many as possible. How many stickers are left over?",
         310, 690, [24, 26, 28], "sticker", "stickers", None),
        ("rem", "A garden centre has {n} bulbs. It packs them in bags of {d} and fills as many bags as it can. How many bulbs are not in a bag?",
         1010, 1990, [36, 48], "bulb", "bulbs", None),
        ("frac", "{name} bakes {n} cakes for a party. They are shared equally between {d} tables. How many cakes does each table get?",
         35, 99, [12, 16], "cake", "cakes", None),
        ("frac", "A pizza restaurant shares {n} pizzas equally between {d} children at a party. How much pizza does each child get?",
         30, 99, [24, 18], "pizza", "pizzas", None),
        ("frac", "{n} bars of chocolate are shared equally between {d} pupils. How many bars does each pupil get?",
         30, 99, [15, 21, 28], "bar", "bars", None),
        ("dec", "A rope is {n} cm long. It is cut into {d} equal pieces. How long is each piece?",
         510, 1990, [16, 25, 40, 20], "cm", "cm", None),
        ("money", "A class raises £{n} at a cake sale. The money is shared equally between {d} charities. How much does each charity get?",
         310, 1990, [16, 25, 20, 40], "£", "£", None),
        ("money", "{d} friends share a holiday cottage that costs £{n}. They each pay the same amount. How much does each person pay?",
         810, 1990, [12, 16, 15], "£", "£", None),
        ("exact", "A school orders {n} pencils. They come in packs of {d}. How many packs does the school order?",
         1010, 3990, [12, 24, 36], "pack", "packs", None),
        ("exact", "A train travels {n} km in {d} hours. It goes the same distance every hour. How far does it travel each hour?",
         710, 1490, [12, 14, 16], "km", "km", None),
    ]
    its = [story(kind, text, lo, hi, ds, one, many, rnd, P, used, why) for kind, text, lo, hi, ds, one, many, why in S]
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: what to do with the remainder", "items": its}


# ============================================================ lesson
def body_html():
    f_bus = bus_svg(936, 4, work=True, fs=26)
    f_bus2 = bus_svg(1375, 25, work=True, fs=26)
    f_ld = ld_svg(7248, 24, fs=24, work=True)
    f_rem = ld_svg(2385, 48, fs=24, work=True)
    return (
        "<h2>The big idea</h2>"
        "<p>Long division and short division both share a number into equal groups, one digit at a time, from the left. "
        "You <b>divide</b>, <b>multiply</b>, <b>subtract</b> and <b>bring down</b> the next digit. "
        "Short division does the subtracting in your head. Long division writes every step down, which helps with two-digit numbers.</p>"
        "<h2>Short division: the bus stop method</h2>"
        "<p>Write the number under the “bus stop” and the divisor outside. Divide each digit. If there is a remainder, "
        "write it as a small digit in front of the next digit.</p>"
        "<figure class='sn-fig'>" + f_bus +
        "<figcaption>936 ÷ 4: 9 ÷ 4 = 2 r 1, carry the 1 to make 13. 13 ÷ 4 = 3 r 1, carry the 1 to make 16. 16 ÷ 4 = 4. "
        "Answer: 234.</figcaption></figure>"
        "<p>Short division also works for easy two-digit numbers such as 11, 12, 15 and 25.</p>"
        "<figure class='sn-fig'>" + f_bus2 +
        "<figcaption>1,375 ÷ 25: 25 does not go into 1, so carry 1 to make 13. 25 does not go into 13, so carry 13 to make 137. "
        "137 ÷ 25 = 5 r 12, carry 12 to make 125. 125 ÷ 25 = 5. Answer: 55.</figcaption></figure>"
        "<h2>Long division by a two-digit number</h2>"
        "<p>First list some multiples of the divisor. Then each step is easy: find the largest multiple that fits.</p>"
        + table(["× 1", "× 2", "× 3", "× 4", "× 5", "× 6", "× 7", "× 8", "× 9"],
                [[str(24 * k) for k in range(1, 10)]]) +
        "<figure class='sn-fig'>" + f_ld +
        "<figcaption>7,248 ÷ 24: 7 is less than 24, so start with 72. 72 ÷ 24 = 3, 72 − 72 = 0. "
        "Bring down 4: 24 does not go into 4, so write 0. Bring down 8 to make 48: 48 ÷ 24 = 2. Answer: 302.</figcaption></figure>"
        + ex("SATs-style arithmetic", "6,240 ÷ 24 = ?",
             "62 ÷ 24 = 2, 62 − 48 = 14. Bring down 4: 144 ÷ 24 = 6, 144 − 144 = 0. Bring down 0: 24 does not go into 0, so write 0. "
             "Check: 260 × 24 = 6,240.", "260 (not 26)") +
        "<h2>Remainders: r, fraction or decimal</h2>"
        "<figure class='sn-fig'>" + f_rem +
        "<figcaption>2,385 ÷ 48 = 49 r 33. The remainder is always less than the divisor.</figcaption></figure>"
        + table(["Write it as", "How", "17 ÷ 4"], [
            ["a remainder", "Write r and the whole number left over", "4 r 1"],
            ["a fraction", "Put the remainder over the divisor, then simplify", "4 " + fr(1, 4)],
            ["a decimal", "Change the fraction to a decimal (or keep dividing)", "4.25 (not 4.1)"],
        ]) +
        "<h2>Word problems: what does the remainder mean?</h2>"
        + table(["The question asks", "Do this", "500 people, 48 seats on each coach: 500 ÷ 48 = 10 r 20"], [
            ["How many are needed for everyone?", "Round up", "11 coaches"],
            ["How many full groups?", "Round down", "10 full coaches"],
            ["How many are left over?", "The remainder is the answer", "20 people"],
            ["Sharing something that can be split (cake, money, length)", "Use a fraction or a decimal", "3 cakes ÷ 4 = " + fr(3, 4) + " cake each"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Missing a zero (6,240 ÷ 24 = 26)", "Every digit you bring down needs a digit in the answer, even 0: 260"],
            ["A remainder bigger than the divisor (49 r 81 for ÷ 48)", "The divisor goes in once more: 50 r 33"],
            ["Writing r 5 as .5 (39 r 5 = 39.5 for ÷ 8)", "r 5 means " + fr(5, 8) + " = 0.625, so 39.625"],
            ["Rounding the wrong way (10 coaches for 500 people)", "Ask: does everyone need a place? Then round up"],
        ])
    )


FAQ = [
    {"q": "How do you do long division in Year 6?",
     "a": "Divide, multiply, subtract and bring down the next digit, working from the left. For a two-digit divisor it helps to list its multiples first, then pick the largest one that fits at each step."},
    {"q": "What is the difference between short division and long division?",
     "a": "Both work digit by digit. In short division (the bus stop method) you work out the subtraction in your head and write the remainder small; in long division you write every multiplication and subtraction underneath."},
    {"q": "How do you write a remainder as a fraction or a decimal?",
     "a": "Put the remainder over the divisor and simplify: 17 ÷ 4 = 4 r 1 = 4 1/4. Then change the fraction to a decimal: 4 1/4 = 4.25."},
    {"q": "Is long division in the Year 6 SATs?",
     "a": "Yes. The arithmetic paper usually asks pupils to divide a 3-digit or 4-digit number by a two-digit number, and the reasoning papers include word problems where the remainder must be interpreted."},
]


def gen():
    rnd = random.Random(6603)
    P = People(rnd)
    used = set()
    sets = [set_short(rnd, used, P), set_long3(rnd, used, P), set_long4(rnd, used, P),
            set_remainders(rnd, used, P), set_story(rnd, P, used)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "long-division", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Long Division and Short Division",
        "seo_title": "Year 6 Long Division Worksheets: Dividing by 2-Digit Numbers, Remainders and Word Problems",
        "short_title": "Long division",
        "domain": "Multiplication and division",
        "standard_code": "Year 6: Addition, subtraction, multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Divide numbers up to 4 digits by a two-digit whole number using the formal written method of long division, and interpret remainders as whole number remainders, fractions, or by rounding, as appropriate for the context; divide numbers up to 4 digits by a two-digit number using the formal written method of short division where appropriate, interpreting remainders according to the context.",
        "meta_desc": "Free Year 6 maths worksheets on long division and short division: the bus stop method, 3-digit and 4-digit numbers ÷ 2-digit numbers, SATs-style questions, remainders as fractions and decimals, and word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Divide, multiply, subtract, bring down. Every digit you bring down needs a digit in the answer, even 0.",
        "key_sub": "7,248 ÷ 24: 72 ÷ 24 = 3, 4 ÷ 24 = 0, 48 ÷ 24 = 2, so the answer is 302. A remainder is always less than the divisor. In word problems, decide: round up, round down, or write the remainder as a fraction or decimal.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their digits stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
