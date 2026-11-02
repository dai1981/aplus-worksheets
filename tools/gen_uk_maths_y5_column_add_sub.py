# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Column Addition and Subtraction (National Curriculum in England, Year 5: Addition and subtraction)
  python3 tools/gen_uk_maths_y5_column_add_sub.py
HTML attributes use single quotes (no backslashes in the JSON).
British English. Numbers of 1,000 or more are written with commas (also in the column pictures).
English school word: "exchange" (not regroup / carry / borrow).
Year 5 goes beyond Year 4: 5- and 6-digit numbers, mental methods with large numbers,
rounding to check and to a sensible level of accuracy, multi-step problems.
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
ONE = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]
LIMIT = 1000000


def f(n):
    return "{:,}".format(n)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[-1] if c.startswith("about") else c.split(" ")[0]
        lead = lead.lstrip("£")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead in ("0", ""):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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


def nlen(n):
    return len(str(n))


def digits(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def andlist(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------ column picture
def exchange_digits(a, b):
    """Top digits after all the exchanges of column subtraction (ones first)."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return d


def add_carry_cols(a, b):
    """Columns (ones = 0) that make 10 or more and send 1 to the next column."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    c, cols = 0, []
    for i in range(k):
        c = 1 if da[i] + db[i] + c >= 10 else 0
        if c:
            cols.append(i)
    return cols


def column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line. Commas sit in their own narrow slot.
    answer: also write the answer.  marks: red exchange marks
    (+: the exchanged 1s written small under the answer line;  −: old digits crossed out, new digits above)."""
    cw, kw = fs * (0.82 if marks else 0.62), fs * 0.32
    res = a + b if op == "+" else a - b
    rows = [f(a), f(b)] + ([f(res)] if answer else [])

    def xs(s):                     # x centre of every char, right-aligned
        out, x = [], 0.0
        for ch in reversed(s):
            w = kw if ch == "," else cw
            out.append(x + w / 2)
            x += w
        return list(reversed(out)), x

    longest = max(xs(r)[1] for r in rows)
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 12)
    right = W - 12
    top = 10 + (int(fs * 0.62) if marks and op != "+" else 0)
    s = []

    def put(text, y, color, size=fs):
        cx, _ = xs(text)
        for ch, x in zip(text, cx):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - x, y, size, color, ch))
        return cx

    y1, y2 = top + fs, top + int(fs * 2.15)
    put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    longrow = max(rows, key=lambda r: xs(r)[1])
    lx, _ = xs(longrow)
    place_x = [right - x for ch, x in zip(reversed(longrow), reversed(lx)) if ch != ","]
    sign_x = right - longest - cw * 0.9
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, y2, fs, GREEN, "+" if op == "+" else "−"))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.6, ly, right, ly, INK))
    H = ly + 10
    if answer:
        ay = ly + fs + 6
        put(rows[2], ay, GREEN)
        H = ay + 12
        if op == "+":
            ly2 = ay + 11
            s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
                     % (sign_x - cw * 0.6, ly2, right, ly2, INK))
            H = ly2 + 8
    if marks:
        sm = int(fs * 0.55)
        if op == "+":
            assert answer
            yy = H + sm - 2
            for i in add_carry_cols(a, b):
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (place_x[i + 1], yy, sm, RED))
            H = yy + 8
        else:
            nd = exchange_digits(a, b)
            od = digits(a, nlen(a))
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%s %s %s written in columns" % (f(a), "plus" if op == "+" else "minus", f(b))
    return svg_wrap(W, int(H), "".join(s), label)


# ------------------------------------------------------------ the methods, step by step
def add_steps(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    kb = min(nlen(a), nlen(b))
    carry, parts = 0, []
    for i in range(k):
        t = da[i] + db[i] + carry
        if i >= kb:
            big = da[i] if nlen(a) > nlen(b) else db[i]
            expr = "%d + 1" % big if carry else None
        else:
            expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        P = cap(PLACE[i])
        if t >= 10 and i == k - 1:
            parts.append("%s: %s = %d, write %d." % (P, expr, t, t))
            carry = 0
        elif t >= 10:
            parts.append("%s: %s = %d, write %d and exchange." % (P, expr, t, t % 10))
            carry = 1
        else:
            parts.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    s = a + b
    return ("Line up the ones and start on the right. " + " ".join(parts) +
            " Answer: %s. Check with the inverse: %s − %s = %s." % (f(s), f(s), f(b), f(a)))


def sub_steps(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    kb = nlen(b)
    parts = []
    for i in range(k):
        P = cap(PLACE[i])
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                zeros = andlist([PLACE[m] for m in range(i + 1, j)])
                old = d[j]
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. The %s are 0, so exchange from the %d %s: it becomes %d, each 0 becomes 9 "
                       "and the %s become %d. %d − %d = %d."
                       % (P, cur, db[i], zeros, old, PLACE[j], d[j], PLACE[i], d[i], d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d. Exchange 1 %s for 10 %s: %d − %d = %d."
                       % (P, cur, db[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
            parts.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                parts.append("%s: write %d." % (P, d[i]))
        else:
            parts.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    return ("Line up the ones and start on the right. " + " ".join(parts) +
            " Answer: %s. Check with the inverse: %s + %s = %s." % (f(r), f(r), f(b), f(a)))


# ------------------------------------------------------------ typical mistakes
def add_no_exchange(a, b):
    """Never adds the exchanged 1s (writes the full sum only in the last column)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    return sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))


def add_forgot_one(a, b, which):
    """Forgot just one exchanged 1 (the first or the last one)."""
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return a + b - 10 ** (i + 1)


def add_tens_written(a, b):
    """Wrote the whole column total (e.g. 13) instead of exchanging."""
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    s = ""
    for i in reversed(range(k)):
        s += str(da[i] + db[i])
    v = int(s)
    return v if v != a + b and v < LIMIT else None


def add_misalign(a, b):
    """Lined up the shorter number one place too far left."""
    if nlen(a) == nlen(b):
        return None
    big, small = max(a, b), min(a, b)
    return big + small * 10


def add_extra_one(a, b):
    """Added an exchanged 1 to a column that did not get one."""
    cols = set(add_carry_cols(a, b))
    k = max(nlen(a), nlen(b))
    return [a + b + 10 ** (i + 1) for i in range(k - 1) if i not in cols]


def exchanges_add(a, b):
    return len(add_carry_cols(a, b))


def sub_small_from_big(a, b):
    """Took the smaller digit from the bigger one in every column."""
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))


def sub_forgot_reduce(a, b, only_first=False):
    """Made 10 more but did not take 1 away from the next place."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    out, done = 0, False
    for i in range(k):
        if d[i] < db[i]:
            if only_first and done:
                j = i + 1
                while d[j] == 0:
                    j += 1
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
            else:
                d[i] += 10
                done = True
        out += (d[i] - db[i]) * 10 ** i
    return out


def sub_zero_as_ten(a, b):
    """Exchanging across zeros: changed the zeros to 10 instead of 9."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    hit = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            d[j] -= 1
            if j > i + 1:
                hit = True
                for m in range(i + 1, j):
                    d[m] = 10
            d[i] += 10
    if not hit:
        return None
    return sum((d[i] - db[i]) * 10 ** i for i in range(k))


def sub_zero_skip(a, b):
    """Did not exchange across the zeros: took 1 straight from the next non-zero digit, left the zeros as 0,
    then took the smaller digit from the bigger one in those zero columns."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    skipped, hit, out = set(), False, 0
    for i in range(k):
        if i in skipped:
            out += abs(d[i] - db[i]) * 10 ** i
            continue
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                hit = True
                skipped |= set(range(i + 1, j))
            d[j] -= 1
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out if hit else None


def sub_misalign(a, b):
    if nlen(a) == nlen(b) or a - b * 10 <= 0:
        return None
    return a - b * 10


def exchanges_sub(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    n = 0
    for i in range(k):
        if d[i] < db[i]:
            n += 1
            d[i] += 10
            d[i + 1] -= 1
    return n


def zero_chain(a, b):
    """True if some exchange has to go across a 0."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    chain = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                chain = True
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return chain


def clean(vals):
    return [v for v in vals if v is not None and 0 < v < LIMIT * 2]


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_exchange(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b)] + every + add_extra_one(a, b) + [abs(a - b), add_tens_written(a, b)])


def sub_cands(a, b):
    return clean([sub_small_from_big(a, b), sub_zero_as_ten(a, b), sub_zero_skip(a, b), sub_forgot_reduce(a, b),
                  sub_forgot_reduce(a, b, only_first=True), sub_misalign(a, b), a + b])


def item_add(a, b, rnd, col):
    q = (fig(column_svg(a, b, "+")) + "Use column addition.") if col else \
        "Use column addition. What is %s + %s?" % (f(a), f(b))
    return mcq(q, f(a + b), [f(v) for v in add_cands(a, b)], add_steps(a, b), rnd)


def item_sub(a, b, rnd, col):
    q = (fig(column_svg(a, b, "-")) + "Use column subtraction.") if col else \
        "Use column subtraction. What is %s − %s?" % (f(a), f(b))
    return mcq(q, f(a - b), [f(v) for v in sub_cands(a, b) if v not in (a, b)], sub_steps(a, b), rnd)


# ------------------------------------------------------------ set 1: column addition, 5 and 6 digits
def pick_add(rnd, seen, la, lb, want, top=LIMIT - 1):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 5, 10 ** la - 10 ** (la - 1) // 2)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 5, 10 ** lb - 10 ** (lb - 1) // 2)
        if a + b > top or (a, b) in seen or (b, a) in seen or a % 10 == 0 or b % 10 == 0 or a // 1000 == b // 1000:
            continue
        if exchanges_add(a, b) != want:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = [(5, 5, 1)] * 2 + [(5, 4, 2)] * 2 + [(5, 5, 2)] * 3 + [(5, 5, 3)] * 2 + [(5, 4, 3)] + \
           [(6, 5, 2)] + [(6, 5, 3)] * 2 + [(6, 6, 3)] * 2 + [(6, 4, 3)] + [(6, 6, 4)] * 2
    for i, (la, lb, want) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, want)
        if rnd.random() < 0.25 and la == lb:
            a, b = b, a
        its.append(item_add(a, b, rnd, i % 3 != 2))
    # exchanges that run on through 9s
    for a, b, n in [(39996, 25007, 4), (299985, 46027, 5)]:
        assert exchanges_add(a, b) == n
        seen.add((a, b))
        its.append(item_add(a, b, rnd, True))
    return {"title": "Column addition with 5- and 6-digit numbers", "items": its}


# ------------------------------------------------------------ set 2: column subtraction
def pick_sub(rnd, seen, la, lb, want):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 2, 10 ** la - 1)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 10, min(10 ** lb - 1, a - 10 ** (la - 1) // 4))
        if (a, b) in seen or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if exchanges_sub(a, b) == want:
            seen.add((a, b))
            return a, b


def set_sub(rnd, seen):
    its = []
    plan = [(5, 5, 2)] * 2 + [(5, 4, 2)] + [(5, 5, 3)] * 2 + [(6, 5, 3)] * 2 + [(6, 6, 3)] + [(6, 6, 4)] * 2
    for i, (la, lb, want) in enumerate(plan):
        a, b = pick_sub(rnd, seen, la, lb, want)
        its.append(item_sub(a, b, rnd, i % 3 != 2))
    # across zeros: the top number has zeros where the exchange must pass
    tops = {300000, 61248, 70004}                      # lesson / check examples
    pats = [("x000x", 4), ("x00xx", 5), ("x0000", 4), ("xx00x", 5), ("x0x00", 5),
            ("x0000x", 5), ("x00x0x", 5), ("xx000x", 6), ("x00000", 5), ("x00000", 6)]
    for n, (p, lb) in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lo = 10 ** (lb - 1) + 10 ** (lb - 1) // 10
            hi = min(10 ** lb - 1, a - a // 8)
            if hi <= lo:
                continue
            b = rnd.randint(lo, hi)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or exchanges_sub(a, b) < 2:
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, rnd, n % 3 != 2))
            break
    return {"title": "Column subtraction with exchanges across zeros", "items": its}


# ------------------------------------------------------------ set 3: mental methods with large numbers
GROUP = {3: "thousands", 4: "ten thousands"}


def mental_scaled(a, b, z, op, rnd):
    """a and b are counts of 10**z (e.g. 45 thousands + 7 thousands)."""
    u = 10 ** z
    A, B = a * u, b * u
    if op == "+":
        r = a + b
        cands = add_cands(a, b)
        how = "%d + %d = %d" % (a, b, r)
    else:
        r = a - b
        cands = sub_cands(a, b)
        how = "%d − %d = %d" % (a, b, r)
    vals = [v * u for v in cands] + [r * u // 10]              # last: one zero too few
    vals = [v for v in vals if 0 < v < LIMIT and v != r * u]
    e = ("Think in %s: %s is %d %s and %s is %d %s. %s, so the answer is %s."
         % (GROUP[z], f(A), a, GROUP[z], f(B), b, GROUP[z], how, f(r * u)))
    return mcq("Work it out in your head. What is %s %s %s?" % (f(A), op, f(B)), f(r * u), [f(v) for v in vals], e, rnd)


def mental_near(a, n, k, op, rnd):
    """a ± (n − k) where n is a round number: use n, then adjust by k."""
    b = n - k
    if op == "+":
        r = a + b
        vals = [a + n + k, a + n, a - n + k]
        e = ("%s is %s − %d. Add %s: %s + %s = %s. Then take away %d: %s − %d = %s."
             % (f(b), f(n), k, f(n), f(a), f(n), f(a + n), k, f(a + n), k, f(r)))
    else:
        r = a - b
        vals = [a - n - k, a - n, a + n - k]
        e = ("%s is %s − %d. Take away %s: %s − %s = %s. You took away %d too many, so add %d back: %s + %d = %s."
             % (f(b), f(n), k, f(n), f(a), f(n), f(a - n), k, k, f(a - n), k, f(r)))
    return mcq("Use a mental method. What is %s %s %s?" % (f(a), op, f(b)), f(r), [f(v) for v in vals], e, rnd)


def mental_place(a, x, op, rnd):
    """a ± x where x is one digit times a power of ten."""
    z = nlen(x) - 1
    u = 10 ** z
    lead, rest = a // u, a % u
    n = x // u
    r = a + x if op == "+" else a - x
    nl = lead + n if op == "+" else lead - n
    vals = [a + x * 10 if op == "+" else a - x * 10, a + x // 10 if op == "+" else a - x // 10,
            a - x if op == "+" else a + x, a + x // 100 if op == "+" else a - x // 100]
    if op == "−" and lead % 10 < n:                          # exchanged but did not change the next digit
        vals.insert(0, r + 10 * u)
    wq = "more" if op == "+" else "less"
    e = ("Think in %s: %s has %s %s. %s %s %d = %s, so the answer is %s."
         % (PLACE[z], f(a), f(lead), PLACE[z], f(lead), op, n, f(nl), f(r)))
    assert nl * u + rest == r
    return mcq("What is %s %s than %s?" % (f(x), wq, f(a)), f(r), [f(v) for v in vals if 0 < v < LIMIT], e, rnd)


def bond_digit10(x, total):
    """Made each digit up to 10 (a common mistake)."""
    s = str(x).rstrip("0")
    z = len(str(x)) - len(s)
    return int("".join(str(10 - int(c)) if c != "0" else "0" for c in s)) * 10 ** z


def bond_digit9(x, total):
    """Made each digit up to 9, even the last one."""
    s = str(x).rstrip("0")
    z = len(str(x)) - len(s)
    return int("".join(str(9 - int(c)) for c in s)) * 10 ** z


def mental_bond(total, x, rnd):
    r = total - x
    vals = [bond_digit10(x, total), bond_digit9(x, total), total + x]
    e = ("Find the number that makes %s with %s. Make the digits up to 9, but the last digit that is not 0 up to 10: "
         "%s + %s = %s." % (f(total), f(x), f(x), f(r), f(total)))
    return mcq("What is %s − %s?" % (f(total), f(x)), f(r), [f(v) for v in vals], e, rnd)


def set_mental(rnd):
    its = []
    its.append(mental_scaled(45, 7, 3, "+", rnd))
    its.append(mental_place(348215, 30000, "+", rnd))
    its.append(mental_scaled(82, 46, 3, "−", rnd))
    its.append(mental_place(703450, 10000, "−", rnd))
    its.append(mental_scaled(64, 28, 3, "+", rnd))
    its.append(mental_bond(100000, 36000, rnd))
    its.append(mental_scaled(23, 9, 4, "−", rnd))
    its.append(mental_place(96540, 5000, "+", rnd))
    its.append(mental_scaled(370, 85, 3, "+", rnd))
    its.append(mental_bond(1000000, 250000, rnd))
    its.append(mental_scaled(610, 250, 3, "−", rnd))
    its.append(mental_place(250600, 200000, "−", rnd))
    its.append(mental_scaled(26, 57, 4, "+", rnd))
    its.append(mental_bond(1000000, 420000, rnd))
    # choosing a method for near multiples
    its.append(mcq("What is the easiest way to work out <b>47,385 + 19,999</b> in your head?",
                   "Add 20,000, then take away 1",
                   ["Add 20,000, then add 1", "Take away 20,000, then add 1", "Add 19,000, then take away 1"],
                   "19,999 is 1 less than 20,000. Add 20,000: 47,385 + 20,000 = 67,385. "
                   "You added 1 too many, so take away 1: 67,384.", rnd))
    its.append(mental_near(56789, 10000, 1, "+", rnd))
    its.append(mental_near(84312, 20000, 2, "−", rnd))
    its.append(mcq("What is the easiest way to work out <b>182,640 − 49,998</b> in your head?",
                   "Take away 50,000, then add 2",
                   ["Take away 50,000, then take away 2", "Add 50,000, then take away 2", "Take away 50,000, then add 1"],
                   "49,998 is 2 less than 50,000. Take away 50,000: 182,640 − 50,000 = 132,640. "
                   "You took away 2 too many, so add 2 back: 132,642.", rnd))
    its.append(mental_near(138452, 30000, 2, "+", rnd))
    its.append(mental_near(405260, 100000, 1, "−", rnd))
    return {"title": "Mental addition and subtraction with large numbers", "items": its}


# ------------------------------------------------------------ set 4: rounding to estimate and check
def rnd_to(n, p):
    return (n + p // 2) // p * p


def set_check(rnd):
    P = People(rnd)
    its = []
    # (a) best estimate
    for a, b, op, p in [(38412, 24906, "+", 1000), (61248, 29875, "−", 1000), (57694, 18350, "+", 1000),
                        (84107, 46782, "−", 1000), (436820, 285370, "+", 10000), (712450, 368900, "−", 10000)]:
        ra, rb = rnd_to(a, p), rnd_to(b, p)
        exact = a + b if op == "+" else a - b
        est = ra + rb if op == "+" else ra - rb
        down = a // p * p + b // p * p if op == "+" else a // p * p - b // p * p
        wa, wb = rnd_to(a, p * 10), rnd_to(b, p * 10)
        wrong_place = wa + wb if op == "+" else wa - wb
        other = ra - rb if op == "+" else ra + rb
        slip = est - 10 * p if op == "+" else est + 10 * p
        assert down != est and abs(est - exact) < p, (a, b)
        name = "thousand" if p == 1000 else "ten thousand"
        its.append(mcq("Round each number to the nearest %s. Which is the best estimate for %s %s %s?" % (name, f(a), op, f(b)),
                       "about %s" % f(est), ["about %s" % f(v) for v in [down, wrong_place, other, slip] if 0 < v < LIMIT],
                       "%s rounds to %s and %s rounds to %s. %s %s %s = %s. The exact answer is %s, which is close to %s."
                       % (f(a), f(ra), f(b), f(rb), f(ra), op, f(rb), f(est), f(exact), f(est)), rnd))
    # (b) is the answer sensible?
    checks = [(72315, 38742, "−", 72315 - 38742 + 10000, "no reduce"),
              (63857, 24968, "+", 63857 + 24968, "right"),
              (58673, 27519, "+", add_forgot_one(58673, 27519, "last"), "forgot"),
              (524316, 287452, "−", sub_small_from_big(524316, 287452), "small from big"),
              (518264, 296835, "+", 518264 + 296835, "right"),
              (386475, 247839, "+", add_forgot_one(386475, 247839, "last"), "forgot")]
    for a, b, op, got, kind in checks:
        n, he, his = P.next()
        exact = a + b if op == "+" else a - b
        p = 1000 if nlen(a) == 5 else 10000
        M = p * 10
        ra, rb = rnd_to(a, p), rnd_to(b, p)
        est = ra + rb if op == "+" else ra - rb
        err = got - exact
        OK, BIG, SMALL, BIG2 = ("Yes, it is sensible", "No, about %s too big" % f(M), "No, about %s too small" % f(M),
                                "No, about %s too big" % f(2 * M))
        if kind == "right":
            ans, why = OK, "%s's answer, %s, is close to the estimate, so it is sensible." % (n, f(got))
        else:
            assert 0.75 * M < abs(err) < 1.3 * M, (a, b, got, err)
            ans = BIG if err > 0 else SMALL
            fix = {"small from big": "%s took the smaller digit from the bigger one in some columns instead of exchanging." % cap(he),
                   "forgot": "%s forgot to add the exchanged 1 in the %s." % (cap(he), PLACE[add_carry_cols(a, b)[-1] + 1]),
                   "no reduce": "%s exchanged 1 ten thousand for 10 thousands but did not change the %d to %d."
                                % (cap(he), a // 10000, a // 10000 - 1)}[kind]
            why = ("%s's answer, %s, is about %s %s than the estimate. %s The correct answer is %s."
                   % (n, f(got), f(M), "bigger" if err > 0 else "smaller", fix, f(exact)))
        assert abs(got - est) < 1.4 * M
        name = "thousand" if p == 1000 else "ten thousand"
        its.append(mcq("%s worked out %s %s %s = %s. Round each number to the nearest %s to estimate. "
                       "Is %s answer sensible?" % (n, f(a), op, f(b), f(got), name, his),
                       ans, [OK, BIG, SMALL, BIG2],
                       "Estimate: %s %s %s = %s. " % (f(ra), op, f(rb), f(est)) + why, rnd))
    # (c) levels of accuracy in context: work out exactly, then round the answer
    a, b = 48520, 27640
    t = a + b
    its.append(mcq("A charity raised £48,520 at a fun run and £27,640 online. A poster gives the total to the nearest "
                   "thousand pounds. What does the poster say?", "£%s" % f(rnd_to(t, 1000)),
                   ["£%s" % f(rnd_to(a, 1000) + rnd_to(b, 1000)), "£%s" % f(rnd_to(t, 100)), "£%s" % f(rnd_to(t, 10000))],
                   "Work out the exact total first: £48,520 + £27,640 = £76,160. Then round to the nearest thousand: £76,000. "
                   "Rounding each amount first gives £49,000 + £28,000 = £77,000, which is too far out.", rnd))
    a, b = 34862, 29418
    d = a - b
    assert d == 5444 and rnd_to(a, 100) - rnd_to(b, 100) == 5500
    its.append(mcq("A football club sold 34,862 tickets for one match and 29,418 tickets for the next. A report gives the "
                   "difference to the nearest hundred. What does it say?", "%s tickets" % f(rnd_to(d, 100)),
                   ["%s tickets" % f(v) for v in [rnd_to(a, 100) - rnd_to(b, 100), rnd_to(d, 1000), rnd_to(d, 10)]],
                   "Work out the exact difference first: 34,862 − 29,418 = 5,444. Then round to the nearest hundred: 5,400. "
                   "Rounding each number first gives 34,900 − 29,400 = 5,500, which is not accurate.", rnd))
    pop = 186450 + 12780 - 4935
    assert pop == 194295
    its.append(mcq("A town had 186,450 people. Then 12,780 people moved in and 4,935 people moved out. The council gives "
                   "the new population to the nearest ten thousand. What does it say?", f(rnd_to(pop, 10000)),
                   [f(rnd_to(pop, 1000)), f(190000 + 10000 - 0), f(rnd_to(pop, 100))],
                   "Work out the exact number first: 186,450 + 12,780 = 199,230, then 199,230 − 4,935 = 194,295. "
                   "Round to the nearest ten thousand: 190,000. Rounding each number first gives 190,000 + 10,000 − 0 = 200,000, "
                   "which is wrong.", rnd))
    # (d) which calculation checks it? (the inverse)
    for a, b in [(524316, 287452), (70004, 36518)]:
        c = a - b
        other = "%s − %s" % (f(b), f(c)) if b > c else "%s − %s" % (f(c), f(b))
        its.append(mcq("Which calculation checks <b>%s − %s = %s</b>?" % (f(a), f(b), f(c)),
                       "%s + %s" % (f(c), f(b)),
                       ["%s + %s" % (f(a), f(b)), "%s + %s" % (f(a), f(c)), other],
                       "Addition is the inverse of subtraction. Add the answer to the number you took away: "
                       "%s + %s = %s. That is the number you started with, so the answer is right." % (f(c), f(b), f(a)), rnd))
    a, b = 47586, 38749
    s = a + b
    its.append(mcq("Which calculation checks <b>%s + %s = %s</b>?" % (f(a), f(b), f(s)),
                   "%s − %s" % (f(s), f(b)),
                   ["%s + %s" % (f(s), f(b)), "%s − %s" % (f(a), f(b)), "%s + %s" % (f(s), f(a))],
                   "Subtraction is the inverse of addition. Take one of the numbers away from the answer: "
                   "%s − %s = %s. You get the other number, so the answer is right." % (f(s), f(b), f(a)), rnd))
    # (e) missing numbers
    x, b = 52418, 38749
    s = x + b
    its.append(mcq("What number goes in the box?  <b>☐ + %s = %s</b>" % (f(b), f(s)), f(x),
                   [f(v) for v in [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b)]],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(b), f(x), f(x), f(b), f(s)), rnd))
    r, b = 136795, 45280
    x = r + b
    its.append(mcq("What number goes in the box?  <b>☐ − %s = %s</b>" % (f(b), f(r)), f(x),
                   [f(v) for v in [r - b, add_no_exchange(r, b), add_forgot_one(r, b, "last")]],
                   "The box is the starting number, so use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                   % (f(r), f(b), f(x), f(x), f(b), f(r)), rnd))
    return {"title": "Round to estimate and check", "items": its}


# ------------------------------------------------------------ set 5: multi-step problems
def money(v):
    return "£" + f(v)


def unit(v, u):
    return money(v) if u == "£" else "%s %s" % (f(v), u)


def eu(v, u):
    return unit(v, u) if u in ("£", "km") else f(v)


def story(q, ans, cands, u, e, rnd):
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e, rnd)


def sold_both_left(q, A, B, C, u, rnd, what_used, what_left):
    """A − (B + C)."""
    t = B + C
    r = A - t
    assert r > 0
    e = ("Step 1, %s: %s + %s = %s. Step 2, %s: %s − %s = %s. Check: %s + %s = %s."
         % (what_used, eu(B, u), eu(C, u), eu(t, u), what_left, eu(A, u), eu(t, u), eu(r, u),
            eu(r, u), eu(t, u), eu(A, u)))
    return story(q, r, [t, A - B, sub_small_from_big(A, t), sub_zero_as_ten(A, t), sub_forgot_reduce(A, t), A - B + C], u, e, rnd)


def out_then_in(q, A, B, C, u, rnd, s1, s2):
    """A − B + C."""
    m = A - B
    r = m + C
    e = ("Step 1, %s: %s − %s = %s. Step 2, %s: %s + %s = %s."
         % (s1, eu(A, u), eu(B, u), eu(m, u), s2, eu(m, u), eu(C, u), eu(r, u)))
    return story(q, r, [m, A - B - C, A + B + C, add_forgot_one(m, C, "last"), sub_small_from_big(A, B) + C], u, e, rnd)


def more_than_total(q, A, B, u, rnd, who2):
    """A + (A + B)."""
    m = A + B
    r = A + m
    e = ("Step 1, %s: %s + %s = %s. Step 2, both together: %s + %s = %s."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + A, m + B, add_forgot_one(A, m, "last")], u, e, rnd)


def less_than_total(q, A, B, u, rnd, who2):
    """A + (A − B)."""
    m = A - B
    r = A + m
    e = ("Step 1, %s: %s − %s = %s. Step 2, both together: %s + %s = %s."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + B, A + A + B, add_forgot_one(A, m, "last")], u, e, rnd)


def combine_compare(q, B, C, D, u, rnd, s1):
    """(B + C) − D, or D − (B + C)."""
    t = B + C
    r = abs(t - D)
    big, small = max(t, D), min(t, D)
    e = ("Step 1, %s: %s + %s = %s. Step 2, find the difference: %s − %s = %s."
         % (s1, eu(B, u), eu(C, u), eu(t, u), eu(big, u), eu(small, u), eu(r, u)))
    return story(q, r, [t, abs(B - D) + C if B < D else B - D + C, sub_small_from_big(big, small), t + D,
                        sub_zero_as_ten(big, small), sub_forgot_reduce(big, small)], u, e, rnd)


def spend_then_gift(q, A, B, C, D, u, rnd):
    """A − B − C + D (three steps)."""
    t = B + C
    m = A - t
    r = m + D
    e = ("Step 1, money spent: %s + %s = %s. Step 2, money left: %s − %s = %s. Step 3, add the gift: %s + %s = %s."
         % (eu(B, u), eu(C, u), eu(t, u), eu(A, u), eu(t, u), eu(m, u), eu(m, u), eu(D, u), eu(r, u)))
    return story(q, r, [m, m - D, A - B + C + D, A + t + D], u, e, rnd)


def set_story(rnd):
    P = People(rnd)
    its = []
    its.append(sold_both_left(
        "A children’s charity wants to raise £50,000. A fun run raised £18,465 and an online appeal raised £23,890. "
        "How much more money does the charity need?", 50000, 18465, 23890, "£", rnd, "money raised", "money still needed"))
    n, he, his = P.next()
    its.append(sold_both_left(
        "%s’s %s is a lorry driver. This year %s plans to drive 100,000 km. %s drove 45,120 km from January to June "
        "and 37,465 km from July to October. How many kilometres are left to drive this year?"
        % (n, "mum" if he == "she" else "dad", "she" if he == "she" else "he", "She" if he == "she" else "He"),
        100000, 45120, 37465, "km", rnd, "kilometres driven", "kilometres left"))
    its.append(sold_both_left(
        "A stadium has 90,000 tickets for a concert. It sold 46,758 tickets on the first day and 28,965 tickets on the "
        "second day. How many tickets are left?", 90000, 46758, 28965, "tickets", rnd, "tickets sold", "tickets left"))
    its.append(more_than_total(
        "Ashford has 74,385 people. Brookfield has 18,640 more people than Ashford. "
        "How many people live in the two towns altogether?", 74385, 18640, "people", rnd, "people in Brookfield"))
    its.append(out_then_in(
        "A house was worth £285,000. Its value fell by £17,450, then rose by £32,800. What is the house worth now?",
        285000, 17450, 32800, "£", rnd, "after the fall", "after the rise"))
    its.append(combine_compare(
        "A family sold their flat for £186,500. They also have £48,750 in savings. The house they want costs £249,995. "
        "How much more money do they need?", 186500, 48750, 249995, "£", rnd, "money they have"))
    its.append(less_than_total(
        "In 2024, 128,460 people visited a museum. In 2025, 15,875 fewer people visited. "
        "How many people visited in the two years?", 128460, 15875, "people", rnd, "visitors in 2025"))
    its.append(out_then_in(
        "A warehouse had 125,400 parcels. It sent out 87,965 parcels, then a lorry delivered 46,580 more. "
        "How many parcels are in the warehouse now?", 125400, 87965, 46580, "parcels", rnd, "after sending", "after the delivery"))
    n, he, his = P.next()
    its.append(combine_compare(
        "%s’s family drove 12,486 km in 2023 and 14,075 km in 2024. In 2025 they drove 11,938 km. How much further "
        "did they drive in 2023 and 2024 together than in 2025?" % n, 12486, 14075, 11938, "km", rnd, "2023 and 2024"))
    its.append(sold_both_left(
        "A school raised £24,000 for a new library. It spent £13,875 on books and £6,480 on furniture. "
        "How much money is left?", 24000, 13875, 6480, "£", rnd, "money spent", "money left"))
    its.append(less_than_total(
        "A theatre sold 65,820 tickets in 2024. In 2025 it sold 8,475 fewer tickets. "
        "How many tickets did it sell in the two years?", 65820, 8475, "tickets", rnd, "tickets in 2025"))
    its.append(more_than_total(
        "A charity raised £136,250 in its first year. In its second year it raised £27,480 more than in the first year. "
        "How much did it raise in the two years?", 136250, 27480, "£", rnd, "the second year"))
    its.append(combine_compare(
        "On Saturday, 34,568 fans watched a match at one stadium and 28,795 fans watched a match at another. "
        "On Sunday, 72,000 fans watched the cup final. How many more fans watched the cup final than the two Saturday matches?",
        34568, 28795, 72000, "fans", rnd, "fans on Saturday"))
    its.append(out_then_in(
        "A shop had £42,350 in its bank account. It paid £18,965 for new stock, then took £27,480 in sales. "
        "How much money is in the account now?", 42350, 18965, 27480, "£", rnd, "after paying for stock", "after the sales"))
    its.append(sold_both_left(
        "A delivery company’s vans must drive 250,000 km this year. They drove 98,476 km in the first four months and "
        "87,950 km in the next four months. How many kilometres are left?", 250000, 98476, 87950, "km", rnd,
        "kilometres driven", "kilometres left"))
    n, he, his = P.next()
    its.append(sold_both_left(
        "%s’s family wants to buy a house for £325,000. They have saved £42,750 and sold their flat for £215,800. "
        "How much more money do they need?" % n, 325000, 42750, 215800, "£", rnd, "money they have", "money still needed"))
    its.append(combine_compare(
        "A website had 286,450 visitors in January and 315,780 visitors in February. Another website had 650,000 visitors "
        "in the same two months. How many more visitors did the other website have?", 286450, 315780, 650000, "visitors", rnd,
        "visitors to the first website"))
    its.append(less_than_total(
        "A theme park had 452,600 visitors in the summer. In the winter it had 186,750 fewer visitors. "
        "How many visitors did it have in the summer and winter altogether?", 452600, 186750, "visitors", rnd, "visitors in the winter"))
    its.append(out_then_in(
        "A city library had 64,005 books. It gave away 8,368 old books and then bought 5,275 new books. "
        "How many books does it have now?", 64005, 8368, 5275, "books", rnd, "after giving away", "after buying"))
    its.append(spend_then_gift(
        "A charity had £82,450. It spent £36,780 on a minibus and £19,965 on sports equipment. Then a local business gave "
        "it £15,000. How much money does the charity have now?", 82450, 36780, 19965, 15000, "£", rnd))
    rnd.shuffle(its)
    return {"title": "Multi-step word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    A1, B1 = 47586, 38749
    A2, B2 = 61248, 29875
    A3, B3 = 300000, 47586
    assert A1 + B1 == 86335 and A2 - B2 == 31373 and A3 - B3 == 252414
    m1 = add_no_exchange(A1, B1)
    m2 = sub_small_from_big(A2, B2)
    m3 = sub_zero_skip(A3, B3)
    m4 = add_misalign(A1, 3874)
    return (
        "<h2>The idea: line up the columns</h2>"
        "<p>Column addition and subtraction work the same way for big numbers. Write the numbers so <b>ones are under ones</b>, "
        "tens under tens, and so on up to the hundred thousands. Always start with the <b>ones</b> on the right.</p>"
        "<p>When a column adds up to 10 or more, write the ones digit and <b>exchange</b> 10 for 1 in the next column on the left. "
        "Write the exchanged 1 small, under the answer line.</p>"
        "<figure class='sn-fig'>" + column_svg(A1, B1, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 6 + 9 = 15, write 5 and exchange. Tens: 8 + 4 + 1 = 13, write 3 and exchange. "
        "Hundreds: 5 + 7 + 1 = 13, write 3 and exchange. Thousands: 7 + 8 + 1 = 16, write 6 and exchange. "
        "Ten thousands: 4 + 3 + 1 = 8. Answer: 86,335.</figcaption></figure>"
        "<h2>Column subtraction with exchanging</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, <b>exchange</b>: "
        "take 1 from the next column on the left and make 10 more in this column. Cross out the old digit and write the new one above it.</p>"
        "<figure class='sn-fig'>" + column_svg(A2, B2, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 8 − 5 = 3. Tens: 4 − 7, exchange 1 hundred: 14 − 7 = 7. Hundreds: now 1 − 8, exchange 1 thousand: 11 − 8 = 3. "
        "Thousands: now 0 − 9, exchange 1 ten thousand: 10 − 9 = 1. Ten thousands: 5 − 2 = 3. Answer: 31,373.</figcaption></figure>"
        "<h2>Exchanging across zeros</h2>"
        "<p>If the next column is 0, there is nothing to take. Move left to the first digit that is not 0 and exchange from there. "
        "Every 0 you pass becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + column_svg(A3, B3, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 0 − 6. The tens, hundreds, thousands and ten thousands are all 0, so exchange from the 3 hundred thousands. "
        "The 3 becomes 2, each 0 becomes 9 and the ones become 10. Then 10 − 6 = 4, 9 − 8 = 1, 9 − 5 = 4, 9 − 7 = 2, "
        "9 − 4 = 5, 2 − 0 = 2. Answer: 252,414.</figcaption></figure>"
        "<h2>Mental methods with large numbers</h2>"
        "<p>You do not always need columns. Look at the numbers first and choose a quick method.</p>" +
        table(["Calculation", "Quick method"], [
            ["45,000 + 7,000", "Think in thousands: 45 + 7 = 52, so 52,000"],
            ["230,000 − 90,000", "Think in ten thousands: 23 − 9 = 14, so 140,000"],
            ["348,215 + 30,000", "Only the ten thousands change: 34 + 3 = 37, so 378,215"],
            ["56,789 + 9,999", "Add 10,000, then take away 1: 66,788"],
            ["84,312 − 19,998", "Take away 20,000, then add 2 back: 64,314"],
            ["100,000 − 36,000", "Number bonds: 36,000 + 64,000 = 100,000"],
        ]) +
        "<h2>Round to check</h2>"
        "<p>Round each number and do the easier calculation. For 5-digit numbers, round to the nearest thousand. "
        "For 6-digit numbers, round to the nearest ten thousand.</p>" +
        ex("Is it sensible?", "Ruby says 61,248 − 29,875 = 41,373. Is she right?",
           "Estimate: 61,000 − 30,000 = 31,000. Her answer is about 10,000 too big, so it is wrong. "
           "She did not change the 6 to 5 after exchanging. The correct answer is 31,373.", "No, it should be 31,373") +
        "<p>Use the <b>inverse</b> for an exact check: 31,373 + 29,875 = 61,248, which is the number you started with.</p>"
        "<p>When a problem asks for an answer to the nearest thousand (or hundred), work out the exact answer <b>first</b>, "
        "then round it. Rounding every number before you calculate can give the wrong answer.</p>"
        "<h2>Multi-step problems</h2>"
        "<p>Read the question and ask: what do I need to find first? Decide whether each step is adding (putting together, more) "
        "or subtracting (taking away, how many left, how many more). Use columns for hard steps and mental methods for easy ones.</p>" +
        ex("Two steps", "A charity wants to raise £50,000. A fun run raised £18,465 and an online appeal raised £23,890. How much more does it need?",
           "Step 1, money raised: £18,465 + £23,890 = £42,355. Step 2, money still needed: £50,000 − £42,355 = £7,645. "
           "Check: £7,645 + £42,355 = £50,000.", "£7,645") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the exchanged 1s (47,586 + 38,749 = %s)" % f(m1), "Write each exchanged 1 under the next column and add it in"],
            ["Taking the smaller digit from the bigger one (61,248 − 29,875 = %s)" % f(m2),
             "Always take the bottom digit from the top digit. Exchange when the top is smaller"],
            ["Not exchanging across the zeros (300,000 − 47,586 = %s)" % f(m3), "Go left to the first digit that is not 0. Each 0 you pass becomes 9"],
            ["Lining up the numbers on the left (47,586 + 3,874 = %s)" % f(m4), "Line up the ones on the right"],
            ["Rounding to the wrong place when checking", "Round 5-digit numbers to the nearest thousand and 6-digit numbers to the nearest ten thousand"],
        ])
    )


FAQ = [
    {"q": "What addition and subtraction do children learn in Year 5?",
     "a": "Year 5 pupils add and subtract whole numbers with more than 4 digits using column methods, and do mental calculations with large numbers. They also round to check answers and solve multi-step word problems."},
    {"q": "How do you teach column subtraction with zeros, like 300,000 − 47,586?",
     "a": "Go left to the first digit that is not 0 and exchange from there: 300,000 becomes 2 hundred thousands, 9 in each zero column and 10 ones. Then subtract column by column to get 252,414."},
    {"q": "How can children check a big addition or subtraction answer?",
     "a": "Round each number to estimate, for example 61,000 − 30,000 = 31,000 for 61,248 − 29,875. For an exact check, use the inverse: 31,373 + 29,875 = 61,248."},
    {"q": "When should Year 5 pupils use a mental method instead of columns?",
     "a": "Use a mental method when the numbers are round or close to round, such as 230,000 − 90,000 or 56,789 + 9,999. Use columns when there are many exchanges."},
]


def gen():
    rnd = random.Random(5504)
    seen_a, seen_s = set(), set()
    sets = [set_add(rnd, seen_a), set_sub(rnd, seen_s), set_mental(rnd), set_check(rnd), set_story(rnd)]
    balance(sets, rnd)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
    return {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "column-addition-and-subtraction", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Column Addition and Subtraction",
        "seo_title": "Year 5 Column Addition and Subtraction Worksheets: Large Numbers, Mental Methods and Multi-Step Problems",
        "short_title": "Column addition and subtraction",
        "domain": "Addition and subtraction",
        "standard_code": "Year 5: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Add and subtract whole numbers with more than 4 digits, including using formal written methods (columnar "
                         "addition and subtraction); add and subtract numbers mentally with increasingly large numbers; use rounding "
                         "to check answers to calculations and determine, in the context of a problem, levels of accuracy; solve "
                         "addition and subtraction multi-step problems in contexts, deciding which operations and methods to use and why.",
        "meta_desc": "Free Year 5 maths worksheets on column addition and subtraction with 5- and 6-digit numbers, following the "
                     "National Curriculum: exchanging across zeros, mental methods, rounding to check and multi-step word problems. "
                     "100 questions with an answer key.",
        "key_big": "Line up the ones, start on the right, and round to check.",
        "key_sub": "Big numbers work just like small ones: exchange when a column makes 10 or more, or when the top digit is smaller. "
                   "Every 0 you pass becomes 9. Use a mental method when the numbers are round.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
