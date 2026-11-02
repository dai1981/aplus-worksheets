# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Division (Australian Curriculum v9.0, AC9M5N07)
  python3 tools/gen_au_maths_y5_division.py
Short division (the "bus stop" layout) of 2-, 3- and 4-digit numbers by a 1-digit number,
zeros in the quotient, remainders as whole numbers, fractions and decimals (17 ÷ 4 = 4 r 1 = 4 1/4 = 4.25),
and interpreting the remainder in context (round up, round down, the remainder is the answer, share it).
Every quotient and remainder comes from divmod / Fraction, and every figure is drawn from the numbers in the question.
Wrong choices come from real mistakes; a wrong choice is never equal in value to the right answer or another choice.
Australian style: 4-digit numbers have no separator (4536); 5+ digits use a no-break space (10 000). Money in $ and c.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, os, random, re
from decimal import Decimal
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
MONO = "monospace"
NBSP = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ numbers
def f(n):
    """Australian style: 4 digits with no separator, 5 or more digits grouped with a no-break space."""
    s = str(n)
    if len(s) <= 4:
        return s
    return "{:,}".format(n).replace(",", NBSP)


def qr(q, r):
    return "%s r %d" % (f(q), r) if r else f(q)


def V(x):
    return Fraction(x)


def R(q, r):
    """Value key of a 'q r r' answer (never equal to a plain number)."""
    return ("r", q, r) if r else Fraction(q)


def dec(x):
    """Exact decimal text of a Fraction with a terminating decimal: 17/4 -> 4.25."""
    x = Fraction(x)
    d = Decimal(x.numerator) / Decimal(x.denominator)
    s = format(d.normalize(), "f")
    assert Fraction(s) == x, (x, s)
    return f(int(s.split(".")[0])) + ("." + s.split(".")[1] if "." in s else "")


def rdot(q, r):
    """The mistake of writing 'r 1' as '.1'."""
    return Fraction("%d.%d" % (q, r))


def money(x):
    x = Fraction(x)
    assert (x * 100).denominator == 1
    c = int(x * 100)
    if c % 100 == 0:
        return "$" + f(c // 100)
    return "$%s.%02d" % (f(c // 100), c % 100)


def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def mixed(x):
    """Mixed numeral HTML for a Fraction: 4 1/4."""
    x = Fraction(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return f(w)
    return (f(w) + " " if w else "") + fr(r, x.denominator)


def mx(w, n, d):
    """Mixed numeral exactly as written (not simplified), for a student's mistake."""
    return f(w) + " " + fr(n, d)


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


def n_carries(n, d):
    return sum(1 for row in sd_rows(n, d)[:-1] if row[3])


def sd_steps(n, d, end=True):
    rows = sd_rows(n, d)
    L = len(rows)
    parts = []
    for i, cur, q, c in rows:
        if q is None:
            parts.append("%d does not go into %d, so carry the %d to make %d" % (d, cur, cur, rows[i + 1][1]))
        elif q == 0 and i < L - 1:
            parts.append("%d does not go into %d, so write 0 in the quotient%s"
                         % (d, cur, (" and carry the %d to make %d" % (c, rows[i + 1][1])) if c else ""))
        elif q == 0:
            parts.append("%d does not go into %d, so write 0 in the quotient and the remainder is %d" % (d, cur, c))
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


def short_steps(n, d):
    """A one-line division when there is only one step, otherwise the full short division."""
    q, r = divmod(n, d)
    if sum(1 for row in sd_rows(n, d) if row[2] is not None) == 1:
        return "%s ÷ %d = %s." % (f(n), d, qr(q, r))
    return sd_steps(n, d, end=False)


def bus_svg(n, d, work=False, fs=24):
    """Short division ('bus stop'). With work=True the quotient, the small carried remainders
    and the remainder are drawn."""
    ds = str(n)
    L = len(ds)
    rows = sd_rows(n, d)
    cw = fs * (0.78 + (0.42 if work else 0))
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
        cfs = max(14, int(fs * 0.58))
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


# ------------------------------------------------------------ typical mistakes
def drop_zero(q):
    """Missing a zero in the quotient (1007 -> 17, 406 -> 46)."""
    s = str(q).replace("0", "")
    return int(s) if s else 0


def no_carry(n, d):
    """Divided each digit on its own and dropped the carried remainders (72 ÷ 4 -> 1, 0 -> 10)."""
    ds = str(n)
    s = "".join(str(int(c) // d) for c in ds).lstrip("0")
    return (int(s) if s else 0), int(ds[-1]) % d


def add_carry(n, d):
    """Added the carried remainder to the next digit instead of putting it in front (72 ÷ 4: 3 + 2 = 5)."""
    carry, out = 0, ""
    for ch in str(n):
        cur = carry + int(ch)
        q, carry = divmod(cur, d)
        out += str(q)
    s = out.lstrip("0")
    return (int(s) if s else 0), carry


def exact_cands(n, d, rnd):
    q = n // d
    real = []
    if "0" in str(q):
        real.append(drop_zero(q))
    L = len(str(q))
    a, ar = no_carry(n, d)
    if ar == 0 and len(str(a)) >= L:
        real.append(a)
    b, br = add_carry(n, d)
    if br == 0 and len(str(b)) >= L:
        real.append(b)
    rnd.shuffle(real)
    c = real + [q * 10, q + 10, q - 10, q + 1, q - 1]
    return [(f(x), V(x)) for x in c if x > 0]


def rem_cands(n, d, rnd):
    q, r = divmod(n, d)
    real = [(qr(q - 1, r + d), R(q - 1, r + d)),            # remainder bigger than the divisor
            (f(q), V(q))]                                    # left the remainder out
    L = len(str(q))
    a, ar = no_carry(n, d)
    if len(str(a)) >= L:
        real.append((qr(a, ar), R(a, ar)))                   # dropped the carried remainders
    b, br = add_carry(n, d)
    if len(str(b)) >= L:
        real.append((qr(b, br), R(b, br)))                   # added the carry
    if "0" in str(q):
        real.append((qr(drop_zero(q), r), R(drop_zero(q), r)))
    rnd.shuffle(real)
    return real + [(qr(q, d - r), R(q, d - r)), (qr(q + 1, r), R(q + 1, r)), (qr(q - 1, r), R(q - 1, r)),
                   (qr(q + 10, r), R(q + 10, r))]


def div_cands(n, d, rnd):
    return rem_cands(n, d, rnd) if n % d else exact_cands(n, d, rnd)


def sd_item(n, d, figure, rnd):
    q, r = divmod(n, d)
    qtxt = (fig(bus_svg(n, d)) + "Use short division.") if figure else "Use short division to work out %s ÷ %d." % (f(n), d)
    return mcq(qtxt, (qr(q, r), R(q, r)), div_cands(n, d, rnd), sd_steps(n, d))


# ------------------------------------------------------------ number pickers
def pick(rnd, used, ds, lo, hi, rem, zero=False, carries=1, first_small=None):
    """n in [lo, hi] divided by a digit from ds. rem: remainder (>= 1) or not. zero: a 0 inside the quotient.
    first_small: the first digit is smaller than the divisor (True), not (False) or either (None)."""
    while True:
        d = rnd.choice(ds)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if n in used or n % 10 == 0 or (r > 0) != rem or q < 10:
            continue
        if ("0" in str(q)) != zero or n_carries(n, d) < carries:
            continue
        if first_small is not None and (int(str(n)[0]) < d) != first_small:
            continue
        if rem and (r == q % 10 or r == 1 and rnd.random() < 0.5):
            continue
        used.add(n)
        return n, d


def pick_shape(rnd, used, d, shape, rem=False):
    """Quotient with a fixed pattern of zeros: '100x', 'x0y', 'x0yz' ..."""
    while True:
        q = int("".join(str(rnd.randint(1, 9)) if ch == "x" else ch for ch in shape))
        r = rnd.randint(1, d - 1) if rem else 0
        n = q * d + r
        if 1000 <= n <= 9999 and n not in used and n % 10:
            used.add(n)
            return n


# ============================================================ set 1: 2- and 3-digit numbers
def what_next(rnd, used, P, d):
    name, he, his = P.next()
    while True:
        n = rnd.randint(100, 999)
        a, b = int(str(n)[0]), int(str(n)[1])
        if a > d and a % d and b > 0 and n not in used and (a % d) * 10 + b >= d and n % 10:
            break
    used.add(n)
    q1, c1 = divmod(a, d)
    nxt = c1 * 10 + b
    e = ("%d ÷ %d = %d r %d. The remainder %d is %d hundred%s, which is %d tens. Write it as a small %d in front of the %d, "
         "so you divide %d next: %d ÷ %d = %s. The whole answer: %s."
         % (a, d, q1, c1, c1, c1, "" if c1 == 1 else "s", c1 * 10, c1, b, nxt, nxt, d, qr(nxt // d, nxt % d), qr(n // d, n % d)))
    return mcq("%s uses short division for %d ÷ %d. First, %d ÷ %d = %d r %d. What does %s divide next?"
               % (name, n, d, a, d, q1, c1, he), (str(nxt), V(nxt)),
               [(str(b), V(b)), (str(c1 + b), V(c1 + b)), (str(b * 10 + c1), V(b * 10 + c1)), (str(nxt + 10), V(nxt + 10))], e)


def set_small(rnd, used, P):
    its = []
    # 2-digit numbers: 3 with no remainder, 2 with a remainder
    for i, rem in enumerate([False, False, False, True, True]):
        n, d = pick(rnd, used, [3, 4, 5, 6, 7], 30, 99, rem, first_small=False)
        its.append(sd_item(n, d, i % 2 == 0, rnd))
    # 3-digit numbers: 5 with no remainder, 3 with a remainder
    for i, (fs, rem) in enumerate([(False, False), (False, False), (False, False), (True, False), (True, False),
                                   (False, True), (False, True), (True, True)]):
        n, d = pick(rnd, used, [3, 4, 6, 7, 8, 9], 100, 999, rem, carries=1 if fs else 2, first_small=fs)
        its.append(sd_item(n, d, i % 2 == 1, rnd))
    # what do you divide next?
    for d in (3, 4, 6):
        its.append(what_next(rnd, used, P, d))
    # check with the inverse
    for _ in range(2):
        n, d = pick(rnd, used, [4, 6, 7, 8], 100, 999, False, carries=2)
        q = n // d
        good = "%d × %d" % (q, d)
        its.append(mcq("%d ÷ %d = %d. Which number sentence checks this answer?" % (n, d, q), (good, "m"),
                       [("%d ÷ %d" % (q, d), "d"), ("%d + %d" % (q, d), "a"), ("%d × %d" % (n, d), "n")],
                       "Multiplication is the inverse of division. %d × %d = %d, which matches, so the answer is right." % (q, d, n)))
    # forgot the carried remainder
    for _ in range(2):
        name, he, his = P.next()
        while True:
            n, d = pick(rnd, used, [3, 4, 6, 7, 8], 30, 999, False, carries=1, first_small=False)
            w, wr = no_carry(n, d)
            if w != n // d and w > 0:
                break
        wtxt = qr(w, wr)
        its.append(mcq("%s works out %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, wtxt, he),
                       ("%s did not carry the remainders" % cap(he), "c"),
                       [("%s missed a 0 in the quotient" % cap(he), "z"), ("%s divided by the wrong number" % cap(he), "w"),
                        ("There is no mistake", "n")],
                       "%s divided each digit on its own and threw the remainders away. Each remainder must be carried "
                       "to the next digit. " % name + sd_steps(n, d)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Short division: 2-digit and 3-digit numbers ÷ 1-digit numbers", "items": its}


# ============================================================ set 2: 4-digit numbers, zeros in the quotient
def set_four(rnd, used, P):
    its = []
    for i, fs in enumerate([False, False, False, True, True, True]):
        n, d = pick(rnd, used, [3, 4, 6, 7, 8, 9], 1000, 9999, False, carries=2, first_small=fs)
        its.append(sd_item(n, d, i % 2 == 0, rnd))
    for i, (d, shape) in enumerate([(4, "100x"), (6, "x0xx"), (3, "xx0x"), (7, "x0x")]):
        n = pick_shape(rnd, used, d, shape)
        its.append(sd_item(n, d, i % 2 == 1, rnd))
    for i, (d, shape) in enumerate([(5, "xxx"), (8, "xxx"), (6, "x0xx")]):
        while True:
            n = pick_shape(rnd, used, d, shape, rem=True)
            if n_carries(n, d) >= 2 and n % d != (n // d) % 10:
                break
        its.append(sd_item(n, d, i == 1, rnd))
    # missing a zero
    for d, shape in ((4, "x00x"), (5, "x0x"), (8, "xx0x")):
        name, he, his = P.next()
        n = pick_shape(rnd, used, d, shape)
        q = n // d
        wq = drop_zero(q)
        its.append(mcq("%s works out %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, f(wq), he),
                       ("%s missed a 0 in the quotient" % cap(he), "z"),
                       [("%s forgot the remainder" % cap(he), "f"), ("%s did not carry the remainders" % cap(he), "c"),
                        ("There is no mistake", "n")],
                       "Check: %s × %d = %s, not %s. When %d does not go into a digit, write 0 in the quotient. "
                       % (f(wq), d, f(wq * d), f(n), d) + sd_steps(n, d)))
    # how many digits in the quotient
    for big in (True, False):
        while True:
            d = rnd.randint(3, 9)
            n = rnd.randint(1000, 9999)
            if n not in used and n % d and n % 10 and (int(str(n)[0]) >= d) == big:
                break
        used.add(n)
        q = n // d
        L = len(str(q))
        why = ("%s is at least %d, so the quotient starts in the thousands place." % (str(n)[0], d)) if big else (
            "%s is less than %d, so there are no thousands. The quotient starts in the hundreds place." % (str(n)[0], d))
        its.append(mcq("How many digits will the quotient of %s ÷ %d have (not counting the remainder)?" % (f(n), d),
                       ("%d digits" % L, L), [("%d digits" % x, x) for x in (4, 3, 2) if x != L] + [("1 digit", 1)],
                       why + " %s ÷ %d = %s." % (f(n), d, qr(q, n % d))))
    # estimate
    for d in (6, 7):
        while True:
            k = rnd.randint(2, 9)
            n = k * d * 100 + rnd.randint(-2 * d, 2 * d)
            if n not in used and n % d and n % 10:
                break
        used.add(n)
        est = k * 100
        its.append(mcq("Which is the best estimate for %s ÷ %d?" % (f(n), d), (f(est), V(est)),
                       [(f(k * 10), V(k * 10)), (f(k * 1000), V(k * 1000)), (f(k * d * 100), V(k * d * 100))],
                       "%s is close to %s, and %d ÷ %d = %d, so %s ÷ %d = %s. The exact answer is %s."
                       % (f(n), f(k * d * 100), k * d, d, k, f(k * d * 100), d, f(est), qr(n // d, n % d))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "4-digit numbers ÷ 1-digit numbers, with zeros in the quotient", "items": its}


# ============================================================ set 3: remainders as whole numbers, fractions and decimals
def pick_rem(rnd, used, ds, lo, hi, ok=lambda n, d, q, r: True):
    while True:
        d = rnd.choice(ds)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if n in used or r == 0 or n % 10 == 0 or r in (q % 10,) or not ok(n, d, q, r):
            continue
        used.add(n)
        return n, d


def dec_cands(q, r, d):
    """Wrong decimals: r written as .r, the missing part, one too many / too few wholes."""
    rf = Fraction(r, d)
    return [(dec(rdot(q, r)), rdot(q, r)), (dec(q + 1 - rf), q + 1 - rf),
            (dec(q + 1 + rf), q + 1 + rf), (dec(q - 1 + rf), q - 1 + rf)]


def set_remainders(rnd, used, P):
    its = []
    # the remainder only
    n, d = pick_rem(rnd, used, [6, 7, 8, 9], 100, 999)
    q, r = divmod(n, d)
    its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), (str(r), V(r)),
                   [(str(d - r), V(d - r)), (str(r + d), V(r + d)), (str(q), V(q)), (str(d), V(d)), (str(r + 1), V(r + 1))],
                   "The question asks for the remainder, not the quotient. " + sd_steps(n, d)))
    # remainder as a whole number
    for _ in range(2):
        n, d = pick_rem(rnd, used, [3, 4, 6, 7, 8, 9], 100, 999, lambda n, d, q, r: n_carries(n, d) >= 1)
        q, r = divmod(n, d)
        its.append(mcq("Work out %d ÷ %d. Give the remainder as a whole number." % (n, d), (qr(q, r), R(q, r)),
                       rem_cands(n, d, rnd), sd_steps(n, d)))
    # as a fraction: 4 that do not simplify, 1 that does (Year 5: halves)
    for ds, lo, hi in (([3], 10, 99), ([4], 10, 99), ([5], 10, 99), ([6, 7], 30, 99), ([8], 30, 99)):
        n, d = pick_rem(rnd, used, ds, lo, hi, lambda n, d, q, r: Fraction(r, d).denominator == d and r != d - r)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        cands = []
        if r < q:
            cands.append((mx(q, r, q), q + Fraction(r, q)))                 # remainder over the quotient
        cands += [(mx(q, r, 10), q + Fraction(r, 10)),                        # r over 10, the same mistake as .r
                  (mixed(q + Fraction(d - r, d)), q + Fraction(d - r, d)),  # the part that is missing
                  (mixed(q + 1 + Fraction(r, d)), q + 1 + Fraction(r, d))]
        e = ("%d ÷ %d = %s. The remainder %d is %d out of %d, so it is %s. Answer: %s."
             % (n, d, qr(q, r), r, r, d, fr(r, d), mixed(x)))
        its.append(mcq("Work out %d ÷ %d. Give your answer as a mixed numeral." % (n, d), (mixed(x), x), cands, e))
    n, d = pick_rem(rnd, used, [4, 6, 8], 20, 99, lambda n, d, q, r: Fraction(r, d) == Fraction(1, 2))
    q, r = divmod(n, d)
    x = Fraction(n, d)
    its.append(mcq("Work out %d ÷ %d. Give your answer as a mixed numeral in its simplest form." % (n, d), (mixed(x), x),
                   ([(mx(q, r, q), q + Fraction(r, q))] if r < q else []) +
                   [(mx(q, 1, d), q + Fraction(1, d)),                               # divided the numerator only
                    (mx(q, r, 10), q + Fraction(r, 10)),
                    (mixed(q + 1 + Fraction(1, 2)), q + 1 + Fraction(1, 2)), (mixed(q - 1 + Fraction(1, 2)), q - 1 + Fraction(1, 2))],
                   "%d ÷ %d = %s. The remainder %d out of %d is %s. Simplify: divide the numerator and the denominator by %d "
                   "to get %s. Answer: %s." % (n, d, qr(q, r), r, d, fr(r, d), r, fr(1, 2), mixed(x))))
    # as a decimal (divisors 2, 4 and 5 give tenths or hundredths)
    for ds in ([4], [4], [5], [5], [2]):
        n, d = pick_rem(rnd, used, ds, 10, 99 if ds != [2] else 99)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = ("%d ÷ %d = %s. The remainder %d out of %d is %s = %s. So the answer is %s, not %s."
             % (n, d, qr(q, r), r, d, fr(r, d), dec(rf), dec(x), dec(rdot(q, r))))
        its.append(mcq("Work out %d ÷ %d. Give your answer as a decimal." % (n, d), (dec(x), x), dec_cands(q, r, d), e))
    # from r to a decimal: the 17 ÷ 4 chain
    for d in (4, 5):
        n, d = pick_rem(rnd, used, [d], 10, 99, lambda n, d, q, r: r > 1)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        its.append(mcq("%d ÷ %d = %s = %s. Which decimal is the same?" % (n, d, qr(q, r), mixed(x)), (dec(x), x),
                       dec_cands(q, r, d),
                       "%s = %d ÷ %d = %s, so %s = %s. The remainder %d is not 0.%d: it is %d out of %d."
                       % (fr(r, d), r, d, dec(rf), mixed(x), dec(x), r, r, r, d)))
    # r 1 written as .1
    for d in (4, 2):
        name, he, his = P.next()
        n, d = pick_rem(rnd, used, [d], 10, 99, lambda n, d, q, r: r == 1)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        wrong = dec(rdot(q, r))
        its.append(mcq("%s works out %d ÷ %d = %s and writes the answer as %s. What is the correct decimal answer?"
                       % (name, n, d, qr(q, r), wrong), (dec(x), x),
                       [(dec(q + 1 - rf), q + 1 - rf) if d != 2 else (dec(q + Fraction(1, 4)), q + Fraction(1, 4)),
                        (dec(q + 1 + rf), q + 1 + rf), (dec(q - 1 + rf), q - 1 + rf), (wrong, rdot(q, r))],
                       "r 1 does not mean 0.1. It means 1 out of %d, so it is %s = 1 ÷ %d = %s. The answer is %s."
                       % (d, fr(1, d), d, dec(rf), dec(x))))
    # which remainder is possible / remainder too big
    d = 6
    r = rnd.randint(1, d - 1)
    its.append(mcq("You divide a number by %d. Which of these could be the remainder?" % d, (str(r), V(r)),
                   [(str(w), V(w)) for w in (d, d + 1, d + 3, 2 * d - 1)],
                   "A remainder is always less than the divisor. When you divide by %d, the remainder can only be 1 to %d "
                   "(or 0). If you have %d or more left, %d goes in again." % (d, d - 1, d, d)))
    name, he, his = P.next()
    while True:
        n, d = pick(rnd, used, [3, 4, 5, 6, 7], 100, 999, True, carries=1)
        q, r = divmod(n, d)
        if r + d <= 9:
            break
    its.append(mcq("%s works out %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he),
                   ("The remainder is too big", "b"),
                   [("%s did not carry the remainders" % cap(he), "c"), ("%s missed a 0 in the quotient" % cap(he), "z"),
                    ("There is no mistake", "n")],
                   "A remainder must be less than the divisor. %d is more than %d, so %d goes in once more: %d − %d = %d. "
                   "The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Remainders as whole numbers, fractions and decimals", "items": its}


# ============================================================ set 4: interpret the remainder in context
UP = [  # (text, question, one, many, left-over one, left-over many, divisors)
    ("{n} students are going to the swimming carnival. Each minibus has {d} seats for students.", "How many minibuses are needed?",
     "minibus", "minibuses", "student", "students", [8, 9]),
    ("{n} Year 5 students are going on school camp. Each tent sleeps {d} students.", "How many tents are needed?",
     "tent", "tents", "student", "students", [4, 6]),
    ("{n} guests are coming to the school trivia night. Each table seats {d} guests.", "How many tables are needed?",
     "table", "tables", "guest", "guests", [8]),
    ("{n} students are going on an excursion. Each parent’s car can take {d} students.", "How many cars are needed?",
     "car", "cars", "student", "students", [3, 4]),
    ("A teacher needs {n} glue sticks for the term. Glue sticks come in packs of {d}.", "How many packs must she buy?",
     "pack", "packs", "glue stick", "glue sticks", [6, 8]),
]
DOWN = [  # (text, question, one, many, left-over one, left-over many, verb, divisors)
    ("A bakery has {n} lamingtons. Each box holds {d} lamingtons.", "How many boxes can be filled?",
     "box", "boxes", "lamington", "lamingtons", "fill", [6]),
    ("A farmer has {n} avocados. She packs them in bags of {d}.", "How many full bags can she pack?",
     "bag", "bags", "avocado", "avocados", "fill", [4, 6]),
    ("{n} students sign up for tug of war at the sports carnival. Each team needs exactly {d} students.", "How many full teams can be made?",
     "team", "teams", "student", "students", "make", [8, 9]),
    ("A shop has {n} batteries. It sells them in packs of {d}.", "How many full packs can the shop make?",
     "pack", "packs", "battery", "batteries", "make", [4]),
    ("The school library has {n} new books. Each shelf holds {d} books.", "How many shelves can be filled completely?",
     "shelf", "shelves", "book", "books", "fill", [9]),
]
REM = [  # (text, one, many, divisors)
    ("A teacher shares {n} stickers equally between {d} groups. Each group gets as many as possible. How many stickers are left over?",
     "sticker", "stickers", [6, 7]),
    ("A coach puts {n} tennis balls into buckets of {d} and fills as many buckets as possible. How many balls are not in a bucket?",
     "ball", "balls", [8, 9]),
    ("At the athletics carnival, {n} students line up in rows of {d} for the march past. How many students are in the last row, which is not full?",
     "student", "students", [4, 6]),
]
WAYS = ["Round up", "Round down", "The remainder is the answer", "Write it as a fraction"]


def ctx_num(rnd, used, lo, hi, ds, frac=False, r_min=2):
    while True:
        d = rnd.choice(ds)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if n in used or r == 0 or r in (q, q + 1, q - 1, q % 10) or r < r_min or n % 10 == 0:
            continue
        if frac and Fraction(r, d).denominator != d:
            continue
        used.add(n)
        return n, d


def set_context(rnd, used, P):
    its = []
    for text, qtxt, one, many, lo1, lom, ds in UP:
        n, d = ctx_num(rnd, used, 40, 250, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        e = ("%d ÷ %d = %s. %d %s hold %d × %d = %d %s. %s still %s a place, so you need 1 more: %s. Round up."
             % (n, d, qr(q, r), q, many, q, d, q * d, lom, cap(units(r, lo1, lom)), "needs" if r == 1 else "need", U(q + 1)))
        if one == "pack":
            e = ("%d ÷ %d = %s. %d packs give %d × %d = %d %s. She still needs %s more, so she must buy 1 more pack: %s. Round up."
                 % (n, d, qr(q, r), q, q, d, q * d, lom, units(r, lo1, lom), U(q + 1)))
        its.append(mcq(text.format(n=n, d=d) + " " + qtxt, (U(q + 1), V(q + 1)),
                       [(U(q), V(q)), (qr(q, r), R(q, r)), (U(r), V(r)), (U(q + 2), V(q + 2))], e))
    for text, qtxt, one, many, lo1, lom, verb, ds in DOWN:
        n, d = ctx_num(rnd, used, 40, 250 if one != "shelf" else 500, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        e = ("%d ÷ %d = %s. The %s left over %s not enough to %s another %s, so ignore the remainder. Round down: %s."
             % (n, d, qr(q, r), units(r, lo1, lom), "is" if r == 1 else "are", verb, one, U(q)))
        its.append(mcq(text.format(n=n, d=d) + " " + qtxt, (U(q), V(q)),
                       [(U(q + 1), V(q + 1)), (qr(q, r), R(q, r)), (U(r), V(r)), (U(q - 1), V(q - 1))], e))
    for text, one, many, ds in REM:
        n, d = ctx_num(rnd, used, 60, 250, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        e = "%d ÷ %d = %s. The question asks how many are left over, so the remainder is the answer: %s." % (n, d, qr(q, r), U(r))
        its.append(mcq(text.format(n=n, d=d), (U(r), V(r)),
                       [(U(q), V(q)), (U(d - r), V(d - r)), (qr(q, r), R(q, r)), (U(r + d), V(r + d))], e))
    # which way? (choices kept short)
    ways = [
        ("{n} people are going to a footy match. Each car takes {d} people. {n} ÷ {d} = {qr}. To find how many cars are needed,", 0,
         "Everyone needs a seat, so the left-over people need 1 more car. Round up.", [4]),
        ("A farm packs {n} eggs into cartons of {d}. {n} ÷ {d} = {qr}. To find how many cartons are full,", 1,
         "A carton with fewer than {d} eggs is not full, so ignore the remainder. Round down.", [6]),
        ("{d} friends share {n} pizzas equally. {n} ÷ {d} = {qr}. To find how much pizza each friend gets,", 3,
         "Pizzas can be cut into equal parts, so the left-over pizzas are shared too. Write the remainder as a fraction.", [3, 4]),
    ]
    for text, k, why, ds in ways:
        n, d = ctx_num(rnd, used, 13 if k == 3 else 40, 39 if k == 3 else 99, ds, frac=(k == 3))
        q, r = divmod(n, d)
        res = {0: units(q + 1, "car", "cars"), 1: units(q, "full carton", "full cartons"), 3: mixed(Fraction(n, d)) + " pizzas"}[k]
        its.append(mcq(text.format(n=n, d=d, qr=qr(q, r)) + " what should you do with the remainder?", (WAYS[k], WAYS[k]),
                       [(w, w) for i, w in enumerate(WAYS) if i != k],
                       why.format(d=d) + " The answer is %s." % res))
    # share it: fraction and decimal
    n, d = ctx_num(rnd, used, 13, 39, [4, 3], frac=True)
    q, r = divmod(n, d)
    x = Fraction(n, d)
    cands = []
    if r < q and Fraction(r, q).denominator == q:
        cands.append((mx(q, r, q) + " cakes", q + Fraction(r, q)))
    cands += [(qr(q, r), R(q, r)), (mixed(q + Fraction(d - r, d)) + " cakes", q + Fraction(d - r, d)),
              (units(q, "cake", "cakes"), V(q)), (mixed(q + 1 + Fraction(r, d)) + " cakes", q + 1 + Fraction(r, d))]
    its.append(mcq("%d cakes are shared equally between %d classes for an end-of-term party. How much cake does each class get? "
                   "Give your answer as a mixed numeral." % (n, d), (mixed(x) + " cakes", x), cands,
                   "%d ÷ %d = %s. The %d left-over cakes can be cut and shared too: %d ÷ %d = %s. Each class gets %s cakes."
                   % (n, d, qr(q, r), r, r, d, fr(r, d), mixed(x))))
    n, d = ctx_num(rnd, used, 21, 59, [4, 5])
    q, r = divmod(n, d)
    x = Fraction(n, d)
    rf = Fraction(r, d)
    its.append(mcq("A %d m rope is cut into %d equal pieces. How long is each piece? Give your answer as a decimal." % (n, d),
                   (dec(x) + " m", x),
                   [(dec(rdot(q, r)) + " m", rdot(q, r)), (qr(q, r) + " m", R(q, r)), (units(q, "m", "m"), V(q)),
                    (dec(q + 1 - rf) + " m", q + 1 - rf)],
                   "%d ÷ %d = %s. Rope can be cut into parts, so share the %d m left over: %s = %d ÷ %d = %s. "
                   "Each piece is %s m, not %s m." % (n, d, qr(q, r), r, fr(r, d), r, d, dec(rf), dec(x), dec(rdot(q, r)))))
    # rounded the wrong way
    name, he, his = P.next()
    n, d = ctx_num(rnd, used, 100, 250, [9])
    q, r = divmod(n, d)
    its.append(mcq("%d students are going on a school excursion. Each minibus has %d seats for students. %s works out %d ÷ %d = %s "
                   "and says %d minibuses are needed. What is the right answer?" % (n, d, name, n, d, qr(q, r), q),
                   ("Round up: %d minibuses" % (q + 1), "u"),
                   [("%s is right: %d minibuses" % (name, q), "k"), ("Use the remainder: %s" % units(r, "minibus", "minibuses"), "r"),
                    ("Write %s minibuses" % dec(rdot(q, r)), "d")],
                   "%d minibuses only seat %d × %d = %d students. The other %d students still need seats, so %s rounded the wrong way. "
                   "Round up: %d minibuses." % (q, q, d, q * d, r, name, q + 1)))
    name, he, his = P.next()
    n, d = ctx_num(rnd, used, 100, 250, [6])
    q, r = divmod(n, d)
    its.append(mcq("A canteen has %d muffins. It packs them in boxes of %d. %s works out %d ÷ %d = %s "
                   "and says %d boxes can be filled. What is the right answer?" % (n, d, name, n, d, qr(q, r), q + 1),
                   ("Round down: %d boxes" % q, "d"),
                   [("%s is right: %d boxes" % (name, q + 1), "k"), ("Use the remainder: %s" % units(r, "box", "boxes"), "r"),
                    ("Write %s boxes" % dec(rdot(q, r)), "x")],
                   "%d boxes would need %d × %d = %d muffins, but there are only %d. The %d muffins left over cannot fill a box, "
                   "so %s rounded the wrong way. Round down: %d boxes." % (q + 1, q + 1, d, (q + 1) * d, n, r, name, q)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Interpret the remainder: round up, round down or share it", "items": its}


# ============================================================ set 5: word problems
def find(rnd, lo, hi, ds, kind, used):
    while True:
        d = rnd.choice(ds)
        if kind == "exact":
            q = rnd.randint(-(-lo // d), hi // d)
            n = q * d
            if n % 10 == 0 or n in used or n_carries(n, d) < 1:
                continue
            used.add(n)
            return n, d
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if r == 0 or n in used or n % 10 == 0:
            continue
        if kind == "frac" and Fraction(r, d).denominator != d:
            continue
        if kind in ("dec", "money") and (Fraction(n, d) * 20).denominator != 1:   # money to the nearest 5c
            continue
        if kind not in ("frac", "dec", "money") and (r < 2 or n_carries(n, d) < 1):
            continue
        if r in (q, q + 1, q - 1, q % 10):
            continue
        used.add(n)
        return n, d


def story(kind, text, lo, hi, ds, one, many, rnd, P, used, why=None):
    name, he, his = P.next()
    n, d = find(rnd, lo, hi, ds, kind, used)
    q, r = divmod(n, d)
    q_txt = text.format(n=f(n), d=d, name=name, he=he, He=cap(he), his=his)
    U = lambda k: units(k, one, many)
    base = "Divide: " + short_steps(n, d) + " "
    rq = (qr(q, r), R(q, r))
    if kind == "up":
        e = base + "%s %s not enough: %s %s. You need 1 more, so round up. The answer is %s." % (
            U(q), "are" if q != 1 else "is", units(r, why[0], why[1]), why[2], U(q + 1))
        return mcq(q_txt, (U(q + 1), V(q + 1)), [(U(q), V(q)), rq, (U(r), V(r)), (U(q + 2), V(q + 2))], e)
    if kind == "down":
        left = ("$%d" % r, "is") if why[0] == "$" else (units(r, why[0], why[1]), "is" if r == 1 else "are")
        e = base + "The %s left over %s not enough %s, so round down. The answer is %s." % (left[0], left[1], why[2], U(q))
        return mcq(q_txt, (U(q), V(q)), [(U(q + 1), V(q + 1)), rq, (U(r), V(r)), (U(q - 1), V(q - 1))], e)
    if kind == "rem":
        e = base + "The question asks how many are left over. That is the remainder: %s." % U(r)
        return mcq(q_txt, (U(r), V(r)), [(U(q), V(q)), (U(d - r), V(d - r)), rq, (U(r + d), V(r + d))], e)
    if kind == "frac":
        x = Fraction(n, d)
        e = base + "The %d left over can be shared too: %d ÷ %d = %s. Each gets %s %s." % (r, r, d, fr(r, d), mixed(x), many)
        return mcq(q_txt, (mixed(x) + " " + many, x),
                   [rq, (U(q), V(q)), (mixed(q + 1 - Fraction(r, d)) + " " + many, q + 1 - Fraction(r, d)), (U(q + 1), V(q + 1))], e)
    if kind == "dec":
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = (base + "A length can be split into parts, so write the remainder as a decimal: %s = %d ÷ %d = %s. "
             "Each piece is %s %s, not %s %s." % (fr(r, d), r, d, dec(rf), dec(x), many, dec(rdot(q, r)), many))
        return mcq(q_txt, (dec(x) + " " + many, x),
                   [(dec(rdot(q, r)) + " " + many, rdot(q, r)), rq, (U(q), V(q)), (dec(q + 1 - rf) + " " + many, q + 1 - rf)], e)
    if kind == "money":
        x = Fraction(n, d)
        rf = Fraction(r, d)
        e = (base + "Dollars can be shared into cents, so share the $%d left over: $%d ÷ %d = %dc. Each share is %s, not %s."
             % (r, r, d, int(rf * 100), money(x), money(rdot(q, r))))
        return mcq(q_txt, (money(x), x),
                   [(money(rdot(q, r)), rdot(q, r)), ("$" + qr(q, r), R(q, r)), (money(q), V(q)), (money(q + 1 - rf), q + 1 - rf)], e)
    e = base + "There is no remainder, so the answer is %s. %s" % (U(q), check_txt(n, d))
    return mcq(q_txt, (U(q), V(q)), [(U(int(c)), v) for c, v in exact_cands(n, d, rnd)], e)


def money_story(rnd, P, used, text, lo, hi, ds):
    name, he, his = P.next()
    n, d = find(rnd, lo, hi, ds, "exact", used)
    q = n // d
    q_txt = text.format(n=f(n), d=d, name=name, he=he, He=cap(he), his=his)
    e = "Divide: " + sd_steps(n, d, end=False) + " The answer is $%s. %s" % (f(q), check_txt(n, d))
    return mcq(q_txt, ("$" + f(q), V(q)), [("$" + c, v) for c, v in exact_cands(n, d, rnd)], e)


def set_story(rnd, P, used):
    S = [
        ("up", "{n} students are going to the athletics carnival. Each minibus has {d} seats for students. How many minibuses are needed?",
         100, 250, [8, 9], "minibus", "minibuses", ("student", "students", "would still need a seat")),
        ("up", "A farm collects {n} eggs. It packs them in cartons of {d}. How many cartons does it need for all the eggs?",
         500, 2000, [6], "carton", "cartons", ("egg", "eggs", "would still need a carton")),
        ("up", "{name} is putting {n} photos into an album. Each page holds {d} photos. How many pages does {he} need?",
         150, 450, [4, 6], "page", "pages", ("photo", "photos", "would still need a page")),
        ("up", "{n} people are coming to the school concert. The chairs are put out in rows of {d}. How many rows are needed so everyone has a seat?",
         150, 400, [9, 8], "row", "rows", ("person", "people", "would still need a seat")),
        ("down", "{n} students are at the athletics carnival. Each relay team needs exactly {d} runners. How many full relay teams can be made?",
         100, 250, [4], "team", "teams", ("student", "students", "to make another team")),
        ("down", "{n} students sign up for netball. Each team needs exactly {d} players. How many full teams can be made?",
         100, 200, [7], "team", "teams", ("student", "students", "to make another team")),
        ("down", "The class has ${n} to spend on skipping ropes. Each skipping rope costs ${d}. How many skipping ropes can the class buy?",
         100, 199, [7, 8, 9], "skipping rope", "skipping ropes", ("$", "$", "to buy another skipping rope")),
        ("down", "A farm packs {n} mangoes into trays of {d}. How many full trays can it pack?",
         1000, 2500, [8, 9], "tray", "trays", ("mango", "mangoes", "to fill another tray")),
        ("rem", "{name} deals {n} playing cards equally to {d} players. Each player gets as many as possible. How many cards are left over?",
         100, 400, [3, 4, 6, 7], "card", "cards", None),
        ("rem", "A nursery has {n} seedlings. It plants them in trays of {d} and fills as many trays as it can. How many seedlings are not in a tray?",
         1000, 2000, [6, 8], "seedling", "seedlings", None),
        ("frac", "{name} bakes {n} slices of banana bread. {He} shares them equally between {d} friends. How many slices does each friend get?",
         20, 49, [3, 4], "slice", "slices", None),
        ("dec", "A {n} m length of fencing is cut into {d} equal pieces. How long is each piece? Give your answer as a decimal.",
         21, 99, [4, 5], "m", "m", None),
        ("money", "{d} friends earn ${n} washing cars. They share the money equally. How much does each friend get?",
         50, 199, [4], "dollar", "dollars", None),
        ("money", "{name} and {d_minus} friends have lunch at a café. They split the ${n} bill equally. How much does each person pay?",
         40, 99, [5], "dollar", "dollars", None),
        ("exact", "{name} runs {n} m by running {d} laps of the school oval. Each lap is the same length. How long is one lap?",
         1200, 3200, [6, 8], "m", "m", None),
        ("exact", "A book has {n} pages. {name} reads the same number of pages each day and finishes it in {d} days. How many pages does {he} read each day?",
         150, 450, [3, 4, 6, 7], "page", "pages", None),
        ("exact", "A school orders {n} exercise books. They come in packs of {d}. How many packs does the school order?",
         1000, 3000, [4, 6, 8], "pack", "packs", None),
    ]
    its = []
    for kind, text, lo, hi, ds, one, many, why in S:
        if "{d_minus}" in text:
            text = text.replace("{d_minus}", str(ds[0] - 1))
        its.append(story(kind, text, lo, hi, ds, one, many, rnd, P, used, why))
    its.append(money_story(rnd, P, used, "A class raises ${n} at a sausage sizzle. The money is shared equally between {d} charities. How much does each charity get?",
                           100, 999, [3, 4]))
    its.append(money_story(rnd, P, used, "{d} friends win ${n} in a school art competition. They share the prize equally. How much does each friend get?",
                           100, 999, [3, 4, 6]))
    its.append(money_story(rnd, P, used, "A school spends ${n} on {d} new laptops. Each laptop costs the same. How much does one laptop cost?",
                           2000, 5999, [6, 7, 8, 9]))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: sharing money, sports teams and packing", "items": its}


# ============================================================ lesson
def body_html():
    f1 = bus_svg(738, 6, work=True, fs=26)
    f2 = bus_svg(957, 4, work=True, fs=26)
    f3 = bus_svg(4028, 4, work=True, fs=26)
    return (
        "<h2>The big idea</h2>"
        "<p>Division shares a number into equal groups. Short division works one digit at a time, from the left. "
        "Write the number under the “bus stop” and the divisor outside. Divide each digit. "
        "If there is a remainder, carry it: write it as a small digit in front of the next digit. "
        "The answer is called the quotient.</p>"
        "<h2>Worked examples</h2>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>738 ÷ 6: 7 ÷ 6 = 1 r 1, carry the 1 to make 13. 13 ÷ 6 = 2 r 1, carry the 1 to make 18. "
        "18 ÷ 6 = 3. Answer: 123.</figcaption></figure>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>957 ÷ 4: 9 ÷ 4 = 2 r 1, carry 1 to make 15. 15 ÷ 4 = 3 r 3, carry 3 to make 37. "
        "37 ÷ 4 = 9 r 1. Nothing is left to carry to, so the answer is 239 r 1.</figcaption></figure>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>4028 ÷ 4: 4 ÷ 4 = 1. 4 does not go into 0, so write 0. 4 does not go into 2, so write 0 and carry 2 "
        "to make 28. 28 ÷ 4 = 7. Answer: 1007.</figcaption></figure>"
        + ex("Check with the inverse", "957 ÷ 4 = 239 r 1. Is it right?",
             "Multiply the quotient by the divisor, then add the remainder: 239 × 4 = 956 and 956 + 1 = 957.", "Yes, it is right")
        + "<h2>Three ways to write a remainder</h2>"
        "<p>17 ÷ 4 = 4 r 1. The 1 left over is 1 out of 4, so it is " + fr(1, 4) + ". "
        "As a decimal, " + fr(1, 4) + " = 0.25.</p>"
        + table(["Write it as", "How", "17 ÷ 4"], [
            ["a whole number remainder", "Write r and what is left", "4 r 1"],
            ["a fraction", "Remainder over the divisor", "4 " + fr(1, 4)],
            ["a decimal", "Change the fraction to a decimal", "4.25 (not 4.1)"],
        ])
        + "<h2>Remainders in context: what does the question want?</h2>"
        + table(["The question asks", "Do this", "61 students, 8 in each minibus: 61 ÷ 8 = 7 r 5"], [
            ["How many are needed for everyone?", "Round up", "8 minibuses"],
            ["How many full groups?", "Round down", "7 full minibuses"],
            ["How many are left over?", "The remainder is the answer", "5 students"],
        ])
        + "<p>When the thing can be split, such as a pizza, a length or money, share the remainder too: "
        "23 pizzas ÷ 4 = 5 r 3 = 5 " + fr(3, 4) + " pizzas each, and $45 ÷ 4 = $11.25 each.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Missing a zero (4028 ÷ 4 = 107)", "When the divisor does not go into a digit, write 0 in the quotient: 1007"],
            ["A remainder bigger than the divisor (238 r 5 for ÷ 4)", "The divisor goes in once more: 239 r 1"],
            ["Writing r 1 as .1 (17 ÷ 4 = 4.1)", "r 1 means 1 out of 4: " + fr(1, 4) + " = 0.25, so 4.25"],
            ["Rounding the wrong way (7 minibuses for 61 students)", "Ask: does everyone need a place? Then round up"],
        ])
    )


FAQ = [
    {"q": "What division do Year 5 students learn in the Australian Curriculum?",
     "a": "Year 5 students solve division problems with efficient strategies such as short division, and interpret any remainder to suit the context, writing the result as a whole number, a decimal or a fraction (AC9M5N07)."},
    {"q": "What is the bus stop method of division?",
     "a": "It is the everyday name for short division. The number goes under a line shaped like a bus stop, the divisor sits outside, and you divide one digit at a time, carrying any remainder to the next digit."},
    {"q": "How do you write a remainder as a fraction or a decimal?",
     "a": "Put the remainder over the divisor: 17 ÷ 4 = 4 r 1 = 4 1/4. Then change the fraction to a decimal: 1/4 = 0.25, so 17 ÷ 4 = 4.25, not 4.1."},
    {"q": "Is division on the Year 5 NAPLAN numeracy test?",
     "a": "NAPLAN numeracy is based on the Australian Curriculum, so Year 5 students can meet division and remainder word problems in March. Practising when to round up or down helps with these questions."},
]


def gen():
    rnd = random.Random(5807)
    P = People(rnd)
    used = set()
    sets = [set_small(rnd, used, P), set_four(rnd, used, P), set_remainders(rnd, used, P),
            set_context(rnd, used, P), set_story(rnd, P, used)]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "division", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Division: Short Division and Remainders",
        "seo_title": "Year 5 Division Worksheets: Short Division, Remainders and Word Problems (Australian Curriculum)",
        "short_title": "Division",
        "domain": "Number",
        "standard_code": "AC9M5N07",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve problems involving division, choosing efficient strategies and using digital tools where appropriate; interpret any remainder according to the context and express results as a whole number, decimal or fraction",
        "meta_desc": "Free Year 5 maths worksheets on division, aligned to the Australian Curriculum (AC9M5N07): short division (the bus stop method) of 2-, 3- and 4-digit numbers, zeros in the quotient, remainders as fractions and decimals, rounding up or down in context, and word problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "Divide one digit at a time from the left. Then decide what the remainder means.",
        "key_sub": "17 ÷ 4 = 4 r 1 = 4 1/4 = 4.25 (not 4.1). Round up when everyone needs a place, round down for full groups, and share the remainder when the thing can be split.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
