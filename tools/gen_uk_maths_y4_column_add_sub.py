# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Column Addition and Subtraction (National Curriculum in England, Year 4: Addition and subtraction)
  python3 tools/gen_uk_maths_y4_column_add_sub.py
HTML attributes use single quotes (no backslashes in the JSON).
British English. Numbers of 1,000 or more are written with commas (also in the column pictures).
English school word: "exchange" (not regroup / carry / borrow).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
ONE = ["one", "ten", "hundred", "thousand", "ten thousand"]


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
    # x of every place (ones first): use the longest row so a 5-digit answer has a place too
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
            parts.append("%s: %s = %d. Write %d and exchange 10 %s for 1 %s." % (P, expr, t, t % 10, PLACE[i], ONE[i + 1]))
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
                zeros = " and ".join("0 %s" % PLACE[m] for m in range(i + 1, j))
                chain = ", then ".join("1 %s for 10 %s" % (ONE[m], PLACE[m - 1]) for m in range(j, i, -1))
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. Exchange, but there are %s. Exchange %s. %d − %d = %d."
                       % (P, cur, db[i], zeros, chain, d[i], db[i], d[i] - db[i]))
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
    """Wrote the whole column total (e.g. 13) instead of exchanging: only the first exchange column."""
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    s = ""
    for i in reversed(range(k)):
        s += str(da[i] + db[i])
    v = int(s)
    return v if v != a + b and v < 10 ** 6 else None


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
    """Did not exchange across the zero: took 1 straight from the next non-zero digit, left the zeros as 0,
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
    return [v for v in vals if v is not None and v > 0]


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
    return mcq(q, f(a - b), [f(v) for v in sub_cands(a, b)], sub_steps(a, b), rnd)


# ------------------------------------------------------------ set 1 and 2: column addition
def pick_add(rnd, seen, la, lb, want, top=9999, cols=None):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 5, 10 ** la - 10 ** (la - 1) // 2)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 5, 10 ** lb - 10 ** (lb - 1) // 2)
        if a + b > top or (a, b) in seen or (b, a) in seen or a % 10 == 0 or b % 10 == 0:
            continue
        cc = add_carry_cols(a, b)
        if len(cc) != want or (cols is not None and cc != cols):
            continue
        seen.add((a, b))
        return a, b


def set_add_easy(rnd, seen):
    its = []
    # no exchange (5), then one exchange in each column in turn
    plan = [(4, 4, [])] * 3 + [(4, 3, [])] * 2 + \
           [(4, 4, [0])] * 4 + [(4, 3, [0])] + [(4, 4, [1])] * 3 + [(4, 3, [1])] + [(4, 4, [2])] * 5 + [(4, 3, [2])]
    for i, (la, lb, cols) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, len(cols), cols=cols)
        if rnd.random() < 0.3:
            a, b = b, a
            if nlen(a) < nlen(b):
                a, b = b, a
        its.append(item_add(a, b, rnd, i % 3 != 2))
    return {"title": "Column addition with no exchange or one exchange", "items": its}


def set_add_hard(rnd, seen):
    its = []
    plan = [(4, 4, 2, 9999)] * 6 + [(4, 3, 2, 9999)] * 2 + [(4, 4, 3, 9999)] * 5 + [(4, 3, 3, 9999)] * 2 + \
           [(4, 4, 4, 19999)] * 2 + [(4, 2, 2, 9999)]
    for i, (la, lb, want, top) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, want, top=top)
        its.append(item_add(a, b, rnd, i % 3 != 1))
    # exchanges that run on through 9s
    for a, b in [(4968, 1035), (2995, 3008)]:
        assert exchanges_add(a, b) == 3
        seen.add((a, b))
        its.append(item_add(a, b, rnd, True))
    rnd.shuffle(its)
    return {"title": "Column addition with several exchanges", "items": its}


# ------------------------------------------------------------ set 3: column subtraction
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
    plan = [(4, 4, 1)] * 3 + [(4, 3, 1)] + [(4, 4, 2)] * 3 + [(4, 3, 2)] + [(4, 4, 3)] * 2
    for i, (la, lb, want) in enumerate(plan):
        a, b = pick_sub(rnd, seen, la, lb, want)
        its.append(item_sub(a, b, rnd, i % 3 != 2))
    # across zeros: the top number has zeros where the exchange must pass
    tops = {4002}                                     # 4,002 − 1,358 is the lesson example
    pats = ["x00x", "x00x", "x000", "x000", "x0x0", "x0xx", "x0xx", "xx0x", "x00x", "x000"]
    for n, p in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lb = 3 if n in (3, 6) else 4
            lo = 10 ** (lb - 1) + 10 ** (lb - 1) // 10
            hi = min(10 ** lb - 1, a - 600)
            if hi <= lo:
                continue
            b = rnd.randint(lo, hi)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or exchanges_sub(a, b) < 2:
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, rnd, n % 3 != 2))
            break
    return {"title": "Column subtraction with exchanges and zeros", "items": its}


# ------------------------------------------------------------ set 4: estimate and check with the inverse
def r100(n):
    return int(round(n / 100.0)) * 100


def set_check(rnd):
    P = People(rnd)
    its = []
    # (a) which calculation checks a subtraction?
    for a, b in [(5213, 2768), (6004, 2537), (8152, 3679)]:
        c = a - b
        other = "%s − %s" % (f(c), f(b)) if c > b else "%s − %s" % (f(b), f(c))
        its.append(mcq("Which calculation checks <b>%s − %s = %s</b>?" % (f(a), f(b), f(c)),
                       "%s + %s" % (f(c), f(b)),
                       ["%s + %s" % (f(a), f(b)), "%s + %s" % (f(a), f(c)), other],
                       "Addition is the inverse of subtraction. Add the answer to the number you took away: "
                       "%s + %s = %s. That is the number you started with, so the answer is right." % (f(c), f(b), f(a)), rnd))
    # (b) which calculation checks an addition?
    for a, b in [(3687, 2456), (4528, 3794)]:
        s = a + b
        other = "%s − %s" % (f(a), f(b)) if a > b else "%s − %s" % (f(b), f(a))
        its.append(mcq("Which calculation checks <b>%s + %s = %s</b>?" % (f(a), f(b), f(s)),
                       "%s − %s" % (f(s), f(b)),
                       ["%s + %s" % (f(s), f(b)), other, "%s + %s" % (f(s), f(a))],
                       "Subtraction is the inverse of addition. Take one of the numbers away from the answer: "
                       "%s − %s = %s. You get the other number, so the answer is right." % (f(s), f(b), f(a)), rnd))
    # (c) estimates: round each number to the nearest hundred
    for a, b, op in [(3486, 2357, "+"), (4762, 1851, "+"), (2649, 5278, "+"), (7382, 2834, "−"), (6183, 3746, "−")]:
        ra, rb = r100(a), r100(b)
        est = ra + rb if op == "+" else ra - rb
        exact = a + b if op == "+" else a - b
        down = (a // 100 * 100) + (b // 100 * 100) if op == "+" else (a // 100 * 100) - (b // 100 * 100)
        other = ra - rb if op == "+" else ra + rb
        up = -(-a // 100) * 100 + (-(-b // 100) * 100 if op == "+" else -(-(-b // 100) * 100))  # rounded both up
        wrong_exchange = est - 1000 if op == "+" else est + 1000
        assert down != est and abs(est - exact) < 100
        its.append(mcq("Round each number to the nearest hundred. Which is the best estimate for %s %s %s?" % (f(a), op, f(b)),
                       "about %s" % f(est), ["about %s" % f(v) for v in [down, other, wrong_exchange, up] if v > 0],
                       "%s rounds to %s and %s rounds to %s. %s %s %s = %s. The exact answer is %s, which is close to %s."
                       % (f(a), f(ra), f(b), f(rb), f(ra), op, f(rb), f(est), f(exact), f(est)), rnd))
    # (d) is the answer sensible?
    OK, BIG, SMALL, BIG2 = ("Yes, it is sensible", "No, about 1,000 too big", "No, about 1,000 too small",
                            "No, about 2,000 too big")
    checks = [(3486, 2357, "+", 3486 + 2357, "right"),
              (5213, 2768, "−", sub_small_from_big(5213, 2768), "small from big"),
              (4675, 2548, "+", add_forgot_one(4675, 2548, "last"), "forgot"),
              (8140, 3965, "−", 8140 - 3965, "right"),
              (7326, 4581, "−", sub_forgot_reduce(7326, 4581), "no reduce")]
    for a, b, op, got, kind in checks:
        n, he, his = P.next()
        exact = a + b if op == "+" else a - b
        ra, rb = r100(a), r100(b)
        est = ra + rb if op == "+" else ra - rb
        err = got - exact
        if kind == "right":
            ans, why = OK, "%s's answer, %s, is close to the estimate, so it is sensible." % (n, f(got))
        else:
            assert 800 < abs(err) < 1300, (a, b, got, err)
            ans = BIG if err > 0 else SMALL
            fix = {"small from big": "%s took the smaller digit from the bigger one in each column instead of exchanging." % cap(he),
                   "forgot": "%s forgot to add the exchanged 1 in the thousands." % cap(he),
                   "no reduce": "%s made 10 more in a column but did not take 1 away from the next column." % cap(he)}[kind]
            why = ("%s's answer, %s, is about 1,000 %s than the estimate. %s The correct answer is %s."
                   % (n, f(got), "bigger" if err > 0 else "smaller", fix, f(exact)))
        assert abs(got - est) < 1300
        its.append(mcq("%s worked out %s %s %s = %s. Round each number to the nearest hundred to estimate. "
                       "Is %s answer sensible?" % (n, f(a), op, f(b), f(got), his),
                       ans, [OK, BIG, SMALL, BIG2],
                       "Estimate: %s %s %s = %s. " % (f(ra), op, f(rb), f(est)) + why, rnd))
    # (e) missing numbers: use the inverse
    x, b = 3729, 2486
    s = x + b
    its.append(mcq("What number goes in the box?  <b>☐ + %s = %s</b>" % (f(b), f(s)), f(x),
                   [f(v) for v in [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b)]],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(b), f(x), f(x), f(b), f(s)), rnd))
    a, s = 2648, 7003
    x = s - a
    its.append(mcq("What number goes in the box?  <b>%s + ☐ = %s</b>" % (f(a), f(s)), f(x),
                   [f(v) for v in [s + a, sub_small_from_big(s, a), sub_zero_as_ten(s, a)]],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s)), rnd))
    r, b = 4726, 1395
    x = r + b
    its.append(mcq("What number goes in the box?  <b>☐ − %s = %s</b>" % (f(b), f(r)), f(x),
                   [f(v) for v in [r - b, add_no_exchange(r, b), add_forgot_one(r, b, "first")]],
                   "The box is the starting number, so use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                   % (f(r), f(b), f(x), f(x), f(b), f(r)), rnd))
    a, r = 8040, 3578
    x = a - r
    its.append(mcq("What number goes in the box?  <b>%s − ☐ = %s</b>" % (f(a), f(r)), f(x),
                   [f(v) for v in [a + r, sub_small_from_big(a, r), sub_zero_as_ten(a, r)]],
                   "Think: %s take away what leaves %s? Work out %s − %s = %s. Check: %s − %s = %s."
                   % (f(a), f(r), f(a), f(r), f(x), f(a), f(x), f(r)), rnd))
    r, b = 2867, 3458
    x = r + b
    its.append(mcq("What number goes in the box?  <b>☐ − %s = %s</b>" % (f(b), f(r)), f(x),
                   [f(v) for v in [b - r, add_no_exchange(r, b), add_forgot_one(r, b, "last")]],
                   "Use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                   % (f(r), f(b), f(x), f(x), f(b), f(r)), rnd))
    return {"title": "Estimate and check with the inverse", "items": its}


# ------------------------------------------------------------ set 5: two-step problems
def money(v):
    return "£" + f(v)


def unit(v, u):
    return money(v) if u == "£" else "%s %s" % (f(v), u)


def eu(v, u):
    """Number in an explanation: keep £ and km, leave plain counts as numbers."""
    return unit(v, u) if u in ("£", "km") else f(v)


def story(q, ans, cands, u, e, rnd):
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e, rnd)


def sold_both_left(q, A, B, C, u, rnd, what_used, what_left):
    """A − (B + C)."""
    t = B + C
    r = A - t
    e = ("Step 1, %s: %s + %s = %s. Step 2, %s: %s − %s = %s. Check: %s + %s = %s."
         % (what_used, eu(B, u), eu(C, u), eu(t, u), what_left, eu(A, u), eu(t, u), eu(r, u),
            eu(r, u), eu(t, u), eu(A, u)))
    return story(q, r, [t, A - B, sub_small_from_big(A, t), sub_zero_as_ten(A, t), sub_forgot_reduce(A, t), A - B + C], u, e, rnd)


def out_then_in(q, A, B, C, u, rnd, s1, s2):
    """A − B + C."""
    m = A - B
    r = m + C
    e = ("Step 1, %s: %s − %s = %s. Step 2, %s: %s + %s = %s."
         % (s1, f(A), f(B), f(m), s2, f(m), f(C), f(r)))
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
    """(B + C) − D, or D − (B + C): the difference between a total and another amount."""
    t = B + C
    r = abs(t - D)
    big, small = max(t, D), min(t, D)
    e = ("Step 1, %s: %s + %s = %s. Step 2, find the difference: %s − %s = %s."
         % (s1, eu(B, u), eu(C, u), eu(t, u), eu(big, u), eu(small, u), eu(r, u)))
    return story(q, r, [t, abs(B - D) + C if B < D else B - D + C, sub_small_from_big(big, small), t + D,
                        sub_zero_as_ten(big, small)], u, e, rnd)


def set_story(rnd):
    P = People(rnd)
    its = []
    its.append(sold_both_left(
        "A school wants to raise £3,000 for new playground equipment. The summer fair raised £1,286 and a sponsored walk raised £948. "
        "How much more money does the school need?", 3000, 1286, 948, "£", rnd, "money raised", "money still needed"))
    n, he, his = P.next()
    its.append(sold_both_left(
        "%s’s family is driving 4,000 km on a camping holiday around Europe. They drove 1,348 km in the first week and 1,275 km in the second week. "
        "How many kilometres are left?" % n, 4000, 1348, 1275, "km", rnd, "kilometres driven", "kilometres left"))
    its.append(sold_both_left(
        "A theatre has 6,000 tickets for a pantomime. It sold 2,358 tickets in November and 1,947 tickets in December. "
        "How many tickets are left?", 6000, 2358, 1947, "tickets", rnd, "tickets sold", "tickets left"))
    its.append(more_than_total(
        "Oakfield Primary School has 486 pupils. Hillside Primary School has 128 more pupils than Oakfield. "
        "How many pupils are there in the two schools altogether?", 486, 128, "pupils", rnd, "pupils at Hillside"))
    its.append(out_then_in(
        "A library had 4,326 books. It lent out 1,258 books, then it bought 375 new books. How many books are in the library now?",
        4326, 1258, 375, "books", rnd, "after lending", "after buying"))
    its.append(out_then_in(
        "A garden centre had 2,405 plants. It sold 1,368 plants, then a lorry delivered 850 more. How many plants does it have now?",
        2405, 1368, 850, "plants", rnd, "after selling", "after the delivery"))
    its.append(less_than_total(
        "On Saturday, 3,846 people visited a castle. On Sunday, 1,529 fewer people visited. How many people visited over the weekend?",
        3846, 1529, "people", rnd, "Sunday"))
    its.append(more_than_total(
        "A museum had 2,764 visitors in March. In April, it had 1,385 more visitors than in March. "
        "How many visitors did it have in the two months?", 2764, 1385, "visitors", rnd, "April"))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    its.append(less_than_total(
        "%s’s class raised £1,450 for charity. %s’s class raised £375 less. How much did the two classes raise altogether?" % (n1, n2),
        1450, 375, "£", rnd, "%s’s class" % n2))
    its.append(sold_both_left(
        "A family saved £3,200 for a holiday. The flights cost £1,486 and the hotel cost £1,295. How much money is left?",
        3200, 1486, 1295, "£", rnd, "money spent", "money left"))
    n, he, his = P.next()
    its.append(sold_both_left(
        "A lorry driver wants to drive 5,000 km this month. %s drove 2,385 km in the first two weeks and 1,976 km in the next week. "
        "How many more kilometres must %s drive?" % (cap(he), he), 5000, 2385, 1976, "km", rnd, "kilometres driven", "kilometres left"))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    its.append(combine_compare(
        "%s walked 4,568 steps on Saturday and 3,895 steps on Sunday. %s walked 9,000 steps over the weekend. "
        "How many more steps did %s walk than %s?" % (n1, n2, n2, n1), 4568, 3895, 9000, "steps", rnd, "%s’s steps" % n1))
    its.append(combine_compare(
        "A concert sold 3,475 tickets online and 1,868 tickets at the door. A second concert sold 4,926 tickets. "
        "How many more tickets did the first concert sell?", 3475, 1868, 4926, "tickets", rnd, "tickets for the first concert"))
    its.append(out_then_in(
        "A secondary school had 1,236 pupils. In July, 247 pupils left. In September, 315 new pupils joined. "
        "How many pupils does the school have now?", 1236, 247, 315, "pupils", rnd, "after July", "after September"))
    its.append(sold_both_left(
        "A water tank holds 5,000 litres. On Monday, 1,750 litres were used. On Tuesday, 2,368 litres were used. "
        "How much water is left?", 5000, 1750, 2368, "litres", rnd, "water used", "water left"))
    its.append(combine_compare(
        "Plane A flies from London to Rome (1,434 km) and then from Rome to Athens (1,050 km). Plane B flies straight from London to Athens (2,394 km). "
        "How much further does Plane A fly?", 1434, 1050, 2394, "km", rnd, "Plane A’s distance"))
    its.append(sold_both_left(
        "A factory made 4,750 packets of biscuits. It sent 1,836 packets to one shop and 2,479 packets to another shop. "
        "How many packets are left?", 4750, 1836, 2479, "packets", rnd, "packets sent", "packets left"))
    n, he, his = P.next()
    its.append(combine_compare(
        "%s’s school collected 1,285 books in the first week of a book drive and 968 books in the second week. "
        "It gave 1,500 books to a charity shop. How many books are left?" % n, 1285, 968, 1500, "books", rnd, "books collected"))
    its.append(sold_both_left(
        "A car park has 1,200 spaces. At 9 am, 785 cars are parked. By lunchtime, 296 more cars arrive. "
        "How many spaces are empty now?", 1200, 785, 296, "spaces", rnd, "cars parked", "empty spaces"))
    its.append(less_than_total(
        "A sponsored run raised £2,846. A cake sale raised £1,958 less than the run. How much did they raise altogether?",
        2846, 1958, "£", rnd, "the cake sale"))
    rnd.shuffle(its)
    return {"title": "Two-step word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    A1, B1 = 4567, 3856
    A2, B2 = 5213, 2768
    A3, B3 = 4002, 1358
    assert A1 + B1 == 8423 and A2 - B2 == 2445 and A3 - B3 == 2644
    assert add_no_exchange(A1, B1) == 7313 and sub_small_from_big(A2, B2) == 3555
    assert sub_zero_skip(A3, B3) == 2354, sub_zero_skip(A3, B3)
    assert add_misalign(4567, 382) == 8387
    return (
        "<h2>The idea: line up the columns</h2>"
        "<p>Write the numbers in columns so <b>ones are under ones</b>, tens under tens, hundreds under hundreds and thousands under thousands. "
        "Always start with the <b>ones</b> on the right.</p>"
        "<p>When a column adds up to 10 or more, write the ones digit and <b>exchange</b> 10 for 1 in the next column on the left. "
        "Write the exchanged 1 small, under the answer line.</p>"
        "<figure class='sn-fig'>" + column_svg(A1, B1, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 + 6 = 13. Write 3 and exchange 10 ones for 1 ten. Tens: 6 + 5 + 1 = 12. Write 2 and exchange 10 tens for 1 hundred. "
        "Hundreds: 5 + 8 + 1 = 14. Write 4 and exchange 10 hundreds for 1 thousand. Thousands: 4 + 3 + 1 = 8. Answer: 8,423.</figcaption></figure>"
        "<h2>Column subtraction with exchanging</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, <b>exchange</b>: "
        "take 1 from the next column on the left and make 10 more in this column. Cross out the old digit and write the new one above it.</p>"
        "<figure class='sn-fig'>" + column_svg(A2, B2, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 3 − 8. Exchange 1 ten for 10 ones: 13 − 8 = 5. Tens: now 0 − 6. Exchange 1 hundred for 10 tens: 10 − 6 = 4. "
        "Hundreds: now 1 − 7. Exchange 1 thousand for 10 hundreds: 11 − 7 = 4. Thousands: 4 − 2 = 2. Answer: 2,445.</figcaption></figure>"
        "<h2>Exchanging across zeros</h2>"
        "<p>If the next column is 0, there is nothing to take. Move left to the first digit that is not 0 and exchange from there, "
        "one column at a time. Every 0 you pass becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + column_svg(A3, B3, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 8. There are 0 tens and 0 hundreds. Exchange 1 thousand for 10 hundreds, then 1 hundred for 10 tens, "
        "then 1 ten for 10 ones. Now the top number is 3 thousands, 9 hundreds, 9 tens and 12 ones. "
        "12 − 8 = 4, 9 − 5 = 4, 9 − 3 = 6, 3 − 1 = 2. Answer: 2,644.</figcaption></figure>" +
        ex("Different numbers of digits", "What is 4,567 + 382?",
           "Write 382 under the 567 so the ones line up: 2 under 7, 8 under 6, 3 under 5. "
           "Ones: 7 + 2 = 9. Tens: 6 + 8 = 14, write 4 and exchange. Hundreds: 5 + 3 + 1 = 9. Thousands: 4.", "4,949") +
        "<h2>Check your answer</h2>"
        "<p><b>Use the inverse.</b> Addition and subtraction undo each other. To check 5,213 − 2,768 = 2,445, add: "
        "2,445 + 2,768 = 5,213. You get back to the start, so the answer is right.</p>"
        "<p><b>Estimate.</b> Round each number to the nearest hundred and do the easier calculation. "
        "5,213 − 2,768 is about 5,200 − 2,800 = 2,400. An answer of 2,445 is sensible. An answer of 3,555 is not.</p>"
        "<h2>Two-step problems</h2>"
        "<p>Read the question and ask: what do I need to find first? Decide whether each step is adding (putting together, more) "
        "or subtracting (taking away, how many left, how many more). Then check the answer makes sense.</p>" +
        ex("Two steps", "A theatre has 9,500 tickets. It sold 3,486 on Friday and 4,275 on Saturday. How many tickets are left?",
           "Step 1, tickets sold: 3,486 + 4,275 = 7,761. Step 2, tickets left: 9,500 − 7,761 = 1,739. "
           "Check: 1,739 + 7,761 = 9,500.", "1,739 tickets") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the exchanged 1 (4,567 + 3,856 = 7,313)", "Write the exchanged 1 under the next column and add it in"],
            ["Taking the smaller digit from the bigger one (5,213 − 2,768 = 3,555)", "Always take the bottom digit from the top digit. Exchange when the top is smaller"],
            ["Not exchanging across a zero (4,002 − 1,358 = 2,354)", "Go left to the first digit that is not 0. Each 0 you pass becomes 9"],
            ["Lining up the numbers on the left (4,567 + 382 = 8,387)", "Line up the ones on the right"],
        ])
    )


FAQ = [
    {"q": "What is column addition and subtraction in Year 4?",
     "a": "It is the formal written method: write the numbers in columns by place value and work from the ones to the left, exchanging when needed. In Year 4 pupils use it with numbers up to 4 digits."},
    {"q": "What does “exchange” mean in column subtraction?",
     "a": "Exchanging means swapping 1 from the next column for 10 in this column, for example 1 ten for 10 ones. It is what older books call borrowing or carrying."},
    {"q": "How do you subtract from a number with zeros, like 4,002 − 1,358?",
     "a": "Go left to the first digit that is not 0 and exchange from there. 4,002 becomes 3 thousands, 9 hundreds, 9 tens and 12 ones, and the answer is 2,644."},
    {"q": "How can my child check an addition or subtraction answer?",
     "a": "Use the inverse: for 5,213 − 2,768 = 2,445, check that 2,445 + 2,768 = 5,213. A quick estimate, such as 5,200 − 2,800 = 2,400, also shows whether the answer is sensible."},
]


def gen():
    rnd = random.Random(4405)
    seen_a, seen_s = set(), set()
    sets = [set_add_easy(rnd, seen_a), set_add_hard(rnd, seen_a), set_sub(rnd, seen_s), set_check(rnd), set_story(rnd)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "column-addition-and-subtraction", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Column Addition and Subtraction",
        "seo_title": "Year 4 Column Addition and Subtraction Worksheets: Exchanging, Checking and Two-Step Problems",
        "short_title": "Column addition and subtraction",
        "domain": "Addition and subtraction",
        "standard_code": "Year 4: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Add and subtract numbers with up to 4 digits using the formal written methods of columnar addition and subtraction "
                         "where appropriate; estimate and use inverse operations to check answers to a calculation; solve addition and "
                         "subtraction two-step problems in contexts, deciding which operations and methods to use and why.",
        "meta_desc": "Free Year 4 maths worksheets on column addition and subtraction with 4-digit numbers, following the National Curriculum: "
                     "exchanging, subtracting across zeros, estimating, checking with the inverse and two-step word problems. "
                     "100 questions with an answer key.",
        "key_big": "Line up the ones. Start on the right. Exchange when you need to.",
        "key_sub": "Adding: a column of 10 or more exchanges 1 into the next column. Subtracting: if the top digit is smaller, "
                   "exchange 1 from the next column, and every 0 you pass becomes 9. Check with the inverse or an estimate.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
