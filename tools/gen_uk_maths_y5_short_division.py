# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Short division (the bus stop method) by a one-digit number
(National Curriculum in England, Year 5: Multiplication and division)
  python3 tools/gen_uk_maths_y5_short_division.py
Every quotient and remainder comes from divmod / Fraction, and every figure is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
Year 5 style: numbers 1,000 and above are written with commas (not inside the written layouts). Remainders are written "r".
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
MONO = "monospace"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ helpers
def f(n):
    """1,000 and above with commas."""
    return "{:,}".format(n)


def qr(q, r):
    return "%s r %d" % (f(q), r) if r else f(q)


def V(x):
    return Fraction(x)


def R(q, r):
    """Value key of a 'q r r' answer (never equal to a plain number)."""
    return ("r", q, r) if r else Fraction(q)


def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def mixed(x):
    x = Fraction(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return f(w)
    return (f(w) + " " if w else "") + fr(r, x.denominator)


def mx(w, n, d):
    """Mixed number exactly as written (not simplified), for a pupil's mistake."""
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
            parts.append("%d does not go into %d, so write 0 in the answer%s"
                         % (d, cur, (" and carry the %d to make %d" % (c, rows[i + 1][1])) if c else ""))
        elif q == 0:
            parts.append("%d does not go into %d, so write 0 in the answer and the remainder is %d" % (d, cur, c))
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
    """Short division ('bus stop'). With work=True the answer, the small carried remainders
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
    """Missing a zero in the answer (1,007 -> 17, 406 -> 46)."""
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
    """n in [lo, hi] divided by a digit from ds. rem: remainder (>= 1) or not. zero: a 0 inside the answer.
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
    """Answer with a fixed pattern of zeros: '100x', 'x0y', 'x0yz' ..."""
    while True:
        q = int("".join(str(rnd.randint(1, 9)) if ch == "x" else ch for ch in shape))
        r = rnd.randint(1, d - 1) if rem else 0
        n = q * d + r
        if 1000 <= n <= 9999 and n not in used and n % 10:
            used.add(n)
            return n


# ============================================================ set 1: no remainder
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


def set_exact(rnd, used, P):
    its = []
    # 2-digit numbers (first digit at least the divisor, one carry)
    for i in range(5):
        n, d = pick(rnd, used, [3, 4, 5, 6, 7], 30, 99, False, first_small=False)
        its.append(sd_item(n, d, i % 2 == 0, rnd))
    # 3-digit numbers
    for i, (fs, z) in enumerate([(False, False), (False, False), (False, False), (False, False),
                                 (True, False), (True, False), (False, False), (False, True)]):
        n, d = pick(rnd, used, [3, 4, 6, 7, 8, 9], 100, 999, False, zero=z, carries=1 if z else 2, first_small=fs)
        its.append(sd_item(n, d, i % 2 == 1, rnd))
    # what do you divide next?
    for d in (3, 4, 6):
        its.append(what_next(rnd, used, P, d))
    # check with the inverse
    for _ in range(2):
        n, d = pick(rnd, used, [4, 6, 7, 8], 100, 999, False, carries=2)
        q = n // d
        good = "%d × %d" % (q, d)
        its.append(mcq("%d ÷ %d = %d. Which calculation checks this answer?" % (n, d, q), (good, "m"),
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
                       [("%s missed a 0 in the answer" % cap(he), "z"), ("%s divided by the wrong number" % cap(he), "w"),
                        ("There is no mistake", "n")],
                       "%s divided each digit on its own and threw the remainders away. Each remainder must be carried "
                       "to the next digit. " % name + sd_steps(n, d)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Short division with no remainder: 2-digit and 3-digit numbers", "items": its}


# ============================================================ set 2: 3-digit numbers with remainders
def set_rem3(rnd, used, P):
    its = []
    for i, fs in enumerate([False] * 8 + [True] * 2 + [False] * 2):
        n, d = pick(rnd, used, [3, 4, 5, 6, 7, 8, 9], 100, 999, True, carries=1 if fs else 2, first_small=fs)
        its.append(sd_item(n, d, i % 3 == 0, rnd))
    # the remainder only
    for _ in range(3):
        n, d = pick(rnd, used, [4, 6, 7, 8, 9], 100, 999, True, carries=1)
        q, r = divmod(n, d)
        cands = [(str(d - r), V(d - r)), (str(r + d), V(r + d)), (str(d), V(d)), (str(q), V(q)), (str(r + 1), V(r + 1))]
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), (str(r), V(r)), cands,
                       "The question asks for the remainder, not the answer to the division. " + sd_steps(n, d)))
    # remainder bigger than the divisor
    for _ in range(2):
        name, he, his = P.next()
        while True:
            n, d = pick(rnd, used, [3, 4, 5, 6, 7], 100, 999, True, carries=1)
            q, r = divmod(n, d)
            if r + d <= 9:
                break
        its.append(mcq("%s works out %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he),
                       ("The remainder is too big", "b"),
                       [("%s did not carry the remainders" % cap(he), "c"), ("%s missed a 0 in the answer" % cap(he), "z"),
                        ("There is no mistake", "n")],
                       "A remainder must be less than the divisor. %d is more than %d, so %d goes in once more: %d − %d = %d. "
                       "The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    # which remainder is possible?
    for d in (4, 6, 9):
        r = rnd.randint(1, d - 1)
        wrong = [d, d + 1, d + 3, 2 * d - 1]
        its.append(mcq("You divide a number by %d. Which of these could be the remainder?" % d, (str(r), V(r)),
                       [(str(w), V(w)) for w in wrong],
                       "A remainder is always less than the divisor. When you divide by %d, the remainder can only be 1 to %d "
                       "(or 0). If you have %d or more left, %d goes in again." % (d, d - 1, d, d)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Short division with remainders: 3-digit numbers", "items": its}


# ============================================================ set 3: 4-digit numbers, zeros in the answer
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
                       ("%s missed a 0 in the answer" % cap(he), "z"),
                       [("%s forgot the remainder" % cap(he), "f"), ("%s did not carry the remainders" % cap(he), "c"),
                        ("There is no mistake", "n")],
                       "Check: %s × %d = %s, not %s. When %d does not go into a digit, write 0 in the answer. "
                       % (f(wq), d, f(wq * d), f(n), d) + sd_steps(n, d)))
    # how many digits in the answer
    for big in (True, False):
        while True:
            d = rnd.randint(3, 9)
            n = rnd.randint(1000, 9999)
            if n not in used and n % d and (int(str(n)[0]) >= d) == big:
                break
        used.add(n)
        q = n // d
        L = len(str(q))
        why = ("%s is at least %d, so the answer starts in the thousands place." % (str(n)[0], d)) if big else (
            "%s is less than %d, so there are no thousands. The answer starts in the hundreds place." % (str(n)[0], d))
        its.append(mcq("How many digits will the answer to %s ÷ %d have (not counting the remainder)?" % (f(n), d),
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
    return {"title": "4-digit numbers ÷ 1-digit numbers, with zeros in the answer", "items": its}


# ============================================================ set 4: remainders in context
UP = [  # (text, one, many, left-over words, divisors)
    ("{n} children are going on a school trip. Each minibus holds {d} children.", "minibus", "minibuses", "child", "children", [8, 9]),
    ("{n} Scouts are going camping. Each tent sleeps {d} people.", "tent", "tents", "person", "people", [4, 6]),
    ("{n} guests are coming to a party. Each table seats {d} guests.", "table", "tables", "guest", "guests", [6, 8]),
    ("{n} people want a boat ride on the lake. Each boat trip takes {d} people.", "trip", "trips", "person", "people", [7, 9]),
]
DOWN = [
    ("A baker has {n} cupcakes. Each box holds {d} cupcakes.", "box", "boxes", "cupcake", "cupcakes", "fill", [4, 6]),
    ("A teacher has {n} pencils. She puts {d} pencils in each pot.", "pot", "pots", "pencil", "pencils", "fill", [6, 8]),
    ("A shop has {n} batteries. It sells them in packs of {d}.", "pack", "packs", "battery", "batteries", "make", [4, 8]),
    ("A library has {n} books. Each shelf holds {d} books.", "shelf", "shelves", "book", "books", "fill", [9]),
]
QUP = {"minibus": "How many minibuses are needed?", "tent": "How many tents are needed?",
       "table": "How many tables are needed?", "trip": "How many boat trips are needed?"}
QDOWN = {"box": "How many boxes can the baker fill?", "pot": "How many pots can she fill?",
         "pack": "How many full packs can the shop make?", "shelf": "How many shelves can be filled?"}
FRAC = [
    ("{d} friends share {n} pizzas equally. How much pizza does each friend get?", "pizza", "pizzas"),
    ("{n} cakes are shared equally between {d} tables. How many cakes does each table get?", "cake", "cakes"),
    ("A {n} m rope is cut into {d} equal pieces. How long is each piece?", "m", "m"),
    ("{n} litres of juice are poured equally into {d} jugs. How much juice is in each jug?", "litre", "litres"),
]


def ctx_num(rnd, used, lo, hi, ds, frac=False):
    while True:
        d = rnd.choice(ds)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if n in used or r == 0 or r in (q, q + 1, q - 1) or (frac and Fraction(r, d).denominator != d) or (not frac and r < 2):
            continue
        used.add(n)
        return n, d


def set_context(rnd, used, P):
    its = []
    for text, one, many, lo1, lom, ds in UP:
        n, d = ctx_num(rnd, used, 40, 250, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        e = ("%d %s hold %d × %d = %d %s. %s still %s a place, so you need 1 more: %s. Round up."
             % (q, many, q, d, q * d, lom, cap(units(r, lo1, lom)), "needs" if r == 1 else "need", U(q + 1)))
        its.append(mcq(text.format(n=n, d=d) + " %d ÷ %d = %s. %s" % (n, d, qr(q, r), QUP[one]), (U(q + 1), V(q + 1)),
                       [(U(q), V(q)), (qr(q, r), R(q, r)), (U(r), V(r)), (U(q + 2), V(q + 2))], e))
    for text, one, many, lo1, lom, verb, ds in DOWN:
        n, d = ctx_num(rnd, used, 40, 250 if one != "shelf" else 500, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        e = ("%d ÷ %d = %s. The %s left over %s not enough to %s another %s, so ignore the remainder. Round down: %s."
             % (n, d, qr(q, r), units(r, lo1, lom), "is" if r == 1 else "are", verb, one, U(q)))
        its.append(mcq(text.format(n=n, d=d) + " %d ÷ %d = %s. %s" % (n, d, qr(q, r), QDOWN[one]), (U(q), V(q)),
                       [(U(q + 1), V(q + 1)), (qr(q, r), R(q, r)), (U(r), V(r)), (U(q - 1), V(q - 1))], e))
    for (text, one, many), (lo, hi, ds) in zip(FRAC, [(13, 39, [4]), (10, 29, [3]), (21, 59, [4, 8]), (11, 39, [3, 4])]):
        n, d = ctx_num(rnd, used, lo, hi, ds, frac=True)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        cands = []
        if r < q and Fraction(r, q).denominator == q:
            cands.append((mx(q, r, q) + " " + many, q + Fraction(r, q)))       # remainder over the answer
        cands += [(qr(q, r), R(q, r)),
                  (mixed(q + Fraction(d - r, d)) + " " + many, q + Fraction(d - r, d)),
                  (units(q, one, many), V(q)),
                  (mixed(q + 1 + Fraction(r, d)) + " " + many, q + 1 + Fraction(r, d))]
        e = ("%d ÷ %d = %s. The %d left over can be shared too: %d ÷ %d = %s. So the answer is %s %s."
             % (n, d, qr(q, r), r, r, d, fr(r, d), mixed(x), many))
        its.append(mcq(text.format(n=n, d=d) + " Give your answer as a mixed number.", (mixed(x) + " " + many, x), cands, e))
    # which calculation checks the answer?
    for rem in (True, True, False, False):
        n, d = pick(rnd, used, [3, 4, 6, 7, 8, 9], 100, 999, rem, carries=1)
        q, r = divmod(n, d)
        if rem:
            good = "%d × %d + %d" % (q, d, r)
            cands = [("%d × %d − %d" % (q, d, r), "s"), ("%d × %d + %d" % (q, r, d), "w"), ("%d × %d" % (q, d), "m"),
                     ("%d ÷ %d + %d" % (q, d, r), "x")]
            e = "Multiply the answer by the divisor, then add the remainder: %d × %d = %d and %d + %d = %d." % (q, d, q * d, q * d, r, n)
            its.append(mcq("%d ÷ %d = %s. Which calculation checks this answer?" % (n, d, qr(q, r)), (good, "g"), cands, e))
        else:
            good = "%d × %d" % (q, d)
            cands = [("%d ÷ %d" % (q, d), "d"), ("%d × %d" % (n, d), "n"), ("%d + %d" % (q, d), "a")]
            e = "Multiplication is the inverse of division. %d × %d = %d, which matches." % (q, d, n)
            its.append(mcq("%d ÷ %d = %d. Which calculation checks this answer?" % (n, d, q), (good, "g"), cands, e))
    # missing number: ? ÷ d = q r r
    for _ in range(4):
        while True:
            d = rnd.randint(3, 9)
            q = rnd.randint(21, 199)
            r = rnd.randint(2, d - 1) if d > 3 else 2
            n = q * d + r
            if n not in used and q % 10 and r != d - r:
                break
        used.add(n)
        cands = [(f(q * d), V(q * d)), (f(q * d - r), V(q * d - r)), (f(q * r + d), V(q * r + d)), (f(q * d + d), V(q * d + d))]
        its.append(mcq("What is the missing number? ? ÷ %d = %s" % (d, qr(q, r)), (f(n), V(n)), cands,
                       "Use the inverse. Multiply, then add the remainder: %d × %d = %s and %s + %d = %s. "
                       "Check: %s ÷ %d = %s." % (q, d, f(q * d), f(q * d), r, f(n), f(n), d, qr(q, r))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Remainders in context: round up, round down or a fraction", "items": its}


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
        if kind == "frac" and (r == 0 or Fraction(r, d).denominator != d):
            continue
        if r > 1 and r not in (q, q + 1, q - 1) and n not in used and n % 10 and n_carries(n, d) >= 1:
            used.add(n)
            return n, d


def story(kind, text, lo, hi, ds, one, many, rnd, P, used, why=None):
    name, he, his = P.next()
    n, d = find(rnd, lo, hi, ds, kind, used)
    q, r = divmod(n, d)
    q_txt = text.format(n=f(n), d=d, name=name, he=he, He=cap(he), his=his)
    U = lambda k: units(k, one, many)
    if sum(1 for row in sd_rows(n, d) if row[2] is not None) == 1:
        base = "Divide: %d ÷ %d = %s. " % (n, d, qr(q, r))
    else:
        base = "Divide: " + sd_steps(n, d, end=False) + " "
    rq = (qr(q, r), R(q, r))
    if kind == "up":
        e = base + "%s %s not enough: %s %s. You need 1 more, so the answer is %s." % (
            U(q), "are" if q != 1 else "is", units(r, why[0], why[1]), why[2], U(q + 1))
        return mcq(q_txt, (U(q + 1), V(q + 1)), [(U(q), V(q)), rq, (U(r), V(r)), (U(q + 2), V(q + 2))], e)
    if kind == "down":
        left = ("£%d" % r, "is") if why[0] == "£" else (units(r, why[0], why[1]), "is" if r == 1 else "are")
        e = base + "The %s left over %s not enough %s, so ignore the remainder. The answer is %s." % (
            left[0], left[1], why[2], U(q))
        return mcq(q_txt, (U(q), V(q)), [(U(q + 1), V(q + 1)), rq, (U(r), V(r)), (U(q - 1), V(q - 1))], e)
    if kind == "rem":
        e = base + "The question asks how many are left over. That is the remainder: %s." % U(r)
        return mcq(q_txt, (U(r), V(r)), [(U(q), V(q)), (U(d - r), V(d - r)), rq, (U(r + d), V(r + d))], e)
    if kind == "frac":
        x = Fraction(n, d)
        e = base + "The %d left over can be shared too: %d ÷ %d = %s. Each gets %s %s." % (r, r, d, fr(r, d), mixed(x), many)
        return mcq(q_txt, (mixed(x) + " " + many, x),
                   [rq, (U(q), V(q)), (mixed(q + 1 - Fraction(r, d)) + " " + many, q + 1 - Fraction(r, d)), (U(q + 1), V(q + 1))], e)
    e = base + "There is no remainder, so the answer is %s." % U(q)
    return mcq(q_txt, (U(q), V(q)), [(U(int(c.replace(",", ""))), v) for c, v in exact_cands(n, d, rnd)], e)


def money_story(rnd, P, used, text, lo, hi, ds):
    name, he, his = P.next()
    n, d = find(rnd, lo, hi, ds, "exact", used)
    q = n // d
    q_txt = text.format(n=f(n), d=d, name=name, he=he, He=cap(he), his=his)
    e = "Divide: " + sd_steps(n, d, end=False) + " The answer is £%s. %s" % (f(q), check_txt(n, d))
    return mcq(q_txt, ("£" + f(q), V(q)), [("£" + c, v) for c, v in exact_cands(n, d, rnd)], e)


def set_story(rnd, P, used):
    S = [
        ("up", "{n} pupils are going to a museum. Each minibus has {d} seats for pupils. How many minibuses are needed?",
         100, 250, [8], "minibus", "minibuses", ("pupil", "pupils", "would still need a seat")),
        ("up", "A farm collects {n} eggs. It packs them in boxes of {d}. How many boxes does it need for all the eggs?",
         500, 2000, [6], "box", "boxes", ("egg", "eggs", "would still need a box")),
        ("up", "{name} is putting {n} photos into an album. Each page holds {d} photos. How many pages does {he} need?",
         150, 450, [4, 6], "page", "pages", ("photo", "photos", "would still need a page")),
        ("up", "{n} people are coming to a school concert. The chairs are put out in rows of {d}. How many rows are needed so everyone has a seat?",
         150, 400, [9, 8], "row", "rows", ("person", "people", "would still need a seat")),
        ("down", "A farm has {n} eggs. It packs them in boxes of {d}. How many boxes can it fill completely?",
         500, 2000, [6], "box", "boxes", ("egg", "eggs", "to fill another box")),
        ("down", "{name} has £{n}. Cinema tickets cost £{d} each. How many tickets can {he} buy?",
         40, 99, [7, 8, 9], "ticket", "tickets", ("£", "£", "to buy another ticket")),
        ("down", "{name} is making necklaces. Each necklace needs {d} beads. {He} has {n} beads. How many necklaces can {he} make?",
         100, 400, [7, 9], "necklace", "necklaces", ("bead", "beads", "to make another necklace")),
        ("down", "There are {n} children at a netball tournament. Each team needs exactly {d} players. How many full teams can be made?",
         100, 200, [7], "team", "teams", ("child", "children", "to make another team")),
        ("rem", "{name} shares {n} sweets equally into {d} party bags. Each bag gets as many as possible. How many sweets are left over?",
         100, 300, [6, 8, 9], "sweet", "sweets", None),
        ("rem", "{n} playing cards are dealt out equally to {d} players. Each player gets as many as possible. How many cards are left over?",
         100, 400, [3, 4, 6, 7], "card", "cards", None),
        ("rem", "A garden centre has {n} bulbs. It packs them in bags of {d} and fills as many bags as it can. How many bulbs are not in a bag?",
         1000, 2000, [6, 8], "bulb", "bulbs", None),
        ("frac", "{name} bakes {n} flapjacks. {He} shares them equally between {d} friends. How many flapjacks does each friend get?",
         20, 49, [3, 4], "flapjack", "flapjacks", None),
        ("frac", "{n} pizzas are shared equally between {d} tables at a party. How much pizza does each table get?",
         20, 49, [4, 8], "pizza", "pizzas", None),
        ("exact", "{name} runs {n} m by running {d} laps of the school field. Each lap is the same length. How long is one lap?",
         1200, 3200, [6, 8], "m", "m", None),
        ("exact", "A book has {n} pages. {name} reads the same number of pages each day and finishes it in {d} days. How many pages does {he} read each day?",
         150, 450, [3, 4, 6, 7], "page", "pages", None),
        ("exact", "A school orders {n} exercise books. They come in packs of {d}. How many packs does the school order?",
         1000, 3000, [4, 6, 8], "pack", "packs", None),
        ("exact", "{name} swims {n} m in {d} days. {He} swims the same distance every day. How far does {he} swim each day?",
         1000, 3000, [4, 5], "m", "m", None),
    ]
    its = [story(kind, text, lo, hi, ds, one, many, rnd, P, used, why) for kind, text, lo, hi, ds, one, many, why in S]
    its.append(money_story(rnd, P, used, "{d} friends win £{n} in a raffle. They share the money equally. How much does each friend get?",
                           100, 999, [3, 4, 6]))
    its.append(money_story(rnd, P, used, "A class raises £{n} at a cake sale. The money is shared equally between {d} charities. How much does each charity get?",
                           100, 999, [3, 4]))
    its.append(money_story(rnd, P, used, "A school spends £{n} on {d} new laptops. Each laptop costs the same. How much does one laptop cost?",
                           1000, 3999, [6, 7, 8, 9]))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: sharing, grouping and what to do with the remainder", "items": its}


# ============================================================ lesson
def body_html():
    f1 = bus_svg(738, 6, work=True, fs=26)
    f2 = bus_svg(957, 4, work=True, fs=26)
    f3 = bus_svg(4028, 4, work=True, fs=26)
    return (
        "<h2>The big idea</h2>"
        "<p>Short division shares a number into equal groups, one digit at a time, from the left. "
        "Write the number under the “bus stop” and the divisor outside. Divide each digit. "
        "If there is a remainder, carry it: write it as a small digit in front of the next digit.</p>"
        "<h2>Worked examples</h2>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>738 ÷ 6: 7 ÷ 6 = 1 r 1, carry the 1 to make 13. 13 ÷ 6 = 2 r 1, carry the 1 to make 18. "
        "18 ÷ 6 = 3. Answer: 123.</figcaption></figure>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>957 ÷ 4: 9 ÷ 4 = 2 r 1, carry 1 to make 15. 15 ÷ 4 = 3 r 3, carry 3 to make 37. "
        "37 ÷ 4 = 9 r 1. Nothing is left to carry to, so the answer is 239 r 1.</figcaption></figure>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>4,028 ÷ 4: 4 ÷ 4 = 1. 4 does not go into 0, so write 0. 4 does not go into 2, so write 0 and carry 2 "
        "to make 28. 28 ÷ 4 = 7. Answer: 1,007.</figcaption></figure>"
        + ex("Check with the inverse", "957 ÷ 4 = 239 r 1. Is it right?",
             "Multiply the answer by the divisor, then add the remainder: 239 × 4 = 956 and 956 + 1 = 957.", "Yes, it is right")
        + "<p>If the first digit is smaller than the divisor, carry it straight away: for 296 ÷ 8, 8 does not go into 2, "
        "so divide 29 next. The answer has one digit fewer: 37.</p>"
        "<h2>Remainders: what does the question want?</h2>"
        + table(["The question asks", "Do this", "61 children, 8 in each minibus: 61 ÷ 8 = 7 r 5"], [
            ["How many are needed for everyone?", "Round up", "8 minibuses"],
            ["How many full groups?", "Round down", "7 full minibuses"],
            ["How many are left over?", "The remainder is the answer", "5 children"],
        ])
        + "<p>When the thing can be split, such as a pizza, a cake or a length, write the remainder as a fraction: "
        "the remainder over the divisor. 23 pizzas ÷ 4 = 5 r 3 = 5 " + fr(3, 4) + " pizzas each.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Missing a zero (4,028 ÷ 4 = 107)", "When the divisor does not go into a digit, write 0 in the answer: 1,007"],
            ["Not carrying the remainder (72 ÷ 4 = 10)", "7 ÷ 4 = 1 r 3. Carry the 3 to make 32: the answer is 18"],
            ["A remainder bigger than the divisor (238 r 5 for ÷ 4)", "The divisor goes in once more: 239 r 1"],
            ["Rounding the wrong way (7 minibuses for 61 children)", "Ask: does everyone need a place? Then round up"],
        ])
    )


FAQ = [
    {"q": "What is the bus stop method of division?",
     "a": "It is the everyday name for short division. The number goes under a line shaped like a bus stop, the divisor sits outside, and you divide one digit at a time, carrying any remainder to the next digit."},
    {"q": "How do you teach short division in Year 5?",
     "a": "Start with 2-digit and 3-digit numbers with no remainder, then add remainders and 4-digit numbers. Ask children to check every answer by multiplying, and to say what the remainder means in a word problem."},
    {"q": "What division should a Year 5 child know?",
     "a": "Year 5 children divide numbers up to 4 digits by a one-digit number using short division. They also decide whether to round a remainder up or down, or write it as a fraction, depending on the question."},
    {"q": "How do you explain a remainder to a child?",
     "a": "A remainder is what is left over when a number cannot be shared equally. It is always smaller than the number you divide by; if it is not, the divisor goes in once more."},
]


def gen():
    rnd = random.Random(5507)
    P = People(rnd)
    used = set()
    sets = [set_exact(rnd, used, P), set_rem3(rnd, used, P), set_four(rnd, used, P),
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
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "short-division", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Short Division: the Bus Stop Method",
        "seo_title": "Year 5 Short Division Worksheets: Bus Stop Method, Remainders and Word Problems",
        "short_title": "Short division",
        "domain": "Multiplication and division",
        "standard_code": "Year 5: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Divide numbers up to 4 digits by a one-digit number using the formal written method of short division and interpret remainders appropriately for the context.",
        "meta_desc": "Free Year 5 maths worksheets on short division (the bus stop method): 2-, 3- and 4-digit numbers ÷ 1-digit numbers, zeros in the answer, remainders, rounding up or down in context, and word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Divide one digit at a time from the left. Carry any remainder to the next digit.",
        "key_sub": "4,028 ÷ 4 = 1,007: when the divisor does not go into a digit, write 0 in the answer. A remainder is always less than the divisor. In word problems, decide: round up, round down, or write the remainder as a fraction.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
