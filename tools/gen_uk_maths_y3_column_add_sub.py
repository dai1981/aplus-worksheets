# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Column Addition and Subtraction (National Curriculum in England, Year 3: Addition and subtraction)
  python3 tools/gen_uk_maths_y3_column_add_sub.py
HTML attributes use single quotes (no backslashes in the JSON).
British English. Year 3 works with numbers up to 3 digits (answers up to 999, no commas).
English school word: "exchange" (not regroup / carry / borrow).
Helpers are copied from gen_uk_maths_y4_column_add_sub.py.
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
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


def sub_added_col(a, b, i):
    """Added the digits in column i instead of subtracting them (only when that column needs no exchange)."""
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    if i >= nlen(b) or db[i] == 0 or exchange_cols_sub(a, b):
        return None
    return a - b - (da[i] - db[i]) * 10 ** i + ((da[i] + db[i]) % 10) * 10 ** i


def sub_write_zero(a, b):
    """Wrote 0 in a column where the top digit is smaller, and did not exchange."""
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    if not exchange_cols_sub(a, b):
        return None
    return sum((da[i] - db[i] if da[i] >= db[i] else 0) * 10 ** i for i in range(k))


def exchange_cols_sub(a, b):
    """Columns (ones = 0) where the top digit is smaller, after earlier exchanges."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    cols = []
    for i in range(k):
        if d[i] < db[i]:
            cols.append(i)
            d[i] += 10
            d[i + 1] -= 1
    return cols


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_exchange(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b)] + every + [abs(a - b)] + add_extra_one(a, b) + [add_tens_written(a, b)])


def sub_cands(a, b):
    return clean([sub_small_from_big(a, b), sub_zero_as_ten(a, b), sub_zero_skip(a, b), sub_forgot_reduce(a, b),
                  sub_forgot_reduce(a, b, only_first=True), sub_misalign(a, b), a + b, sub_write_zero(a, b),
                  sub_added_col(a, b, 0), sub_added_col(a, b, 1), sub_added_col(a, b, 2)])


def item_add(a, b, rnd, col):
    q = (fig(column_svg(a, b, "+")) + "Use column addition.") if col else \
        "Use column addition. What is %s + %s?" % (f(a), f(b))
    return mcq(q, f(a + b), [f(v) for v in add_cands(a, b)], add_steps(a, b), rnd)


def item_sub(a, b, rnd, col):
    q = (fig(column_svg(a, b, "-")) + "Use column subtraction.") if col else \
        "Use column subtraction. What is %s − %s?" % (f(a), f(b))
    return mcq(q, f(a - b), [f(v) for v in sub_cands(a, b)], sub_steps(a, b), rnd)


# ------------------------------------------------------------ set 1: column addition (no exchange or one)
LESSON = {(245, 138), (367, 258), (345, 23), (563, 128), (452, 178), (402, 158)}


def pick_add(rnd, seen, lb, cols, top=999):
    while True:
        a = rnd.randint(112, 880)
        b = rnd.randint(112, 880) if lb == 3 else rnd.randint(12, 96)
        if a + b > top or (a, b) in seen or (b, a) in seen or (a, b) in LESSON or a % 10 == 0 or b % 10 == 0:
            continue
        if add_carry_cols(a, b) != cols:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = [(3, [], 899)] * 4 + [(2, [], 899)] * 2 + \
           [(3, [0], 999)] * 5 + [(2, [0], 999)] * 2 + [(3, [1], 999)] * 5 + [(2, [1], 999)] * 2
    for i, (lb, cols, top) in enumerate(plan):
        a, b = pick_add(rnd, seen, lb, cols, top)
        if lb == 3 and rnd.random() < 0.3:
            a, b = b, a
        its.append(item_add(a, b, rnd, i % 3 != 2))
    return {"title": "Column addition with no exchange or one exchange", "items": its}


# ------------------------------------------------------------ set 2: column subtraction (no exchange or one)
def pick_sub(rnd, seen, lb, cols):
    while True:
        a = rnd.randint(150, 989)
        b = rnd.randint(112, a - 25) if lb == 3 else rnd.randint(12, 96)
        if b >= a or (a, b) in seen or (a, b) in LESSON or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if b < 112 and lb == 3:
            continue
        if exchange_cols_sub(a, b) != cols or (a - b) < 100 and lb == 3 and rnd.random() < 0.7:
            continue
        seen.add((a, b))
        return a, b


def set_sub1(rnd, seen):
    its = []
    plan = [(3, [])] * 4 + [(2, [])] * 2 + [(3, [0])] * 5 + [(2, [0])] * 2 + [(3, [1])] * 5 + [(2, [1])] * 2
    for i, (lb, cols) in enumerate(plan):
        a, b = pick_sub(rnd, seen, lb, cols)
        its.append(item_sub(a, b, rnd, i % 3 != 2))
    return {"title": "Column subtraction with no exchange or one exchange", "items": its}


# ------------------------------------------------------------ set 3: two exchanges and across a zero
def set_hard(rnd, seen_a, seen_s):
    its = []
    for i in range(4):
        a, b = pick_add(rnd, seen_a, 3 if i < 3 else 2, [0, 1])
        its.append(item_add(a, b, rnd, i != 2))
    for a, b in [(296, 138), (395, 207)]:               # exchanges that run on through a 9
        assert add_carry_cols(a, b) == [0, 1] and a + b <= 999
        seen_a.add((a, b))
        its.append(item_add(a, b, rnd, True))
    for i in range(7):
        a, b = pick_sub(rnd, seen_s, 3 if i < 6 else 2, [0, 1])
        its.append(item_sub(a, b, rnd, i % 3 != 2))
    tops = {402}                                       # 402 − 158 is the lesson example
    pats = ["x0x", "x0x", "x00", "x0x", "x00", "x0x", "x00"]
    for n, p in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lb = 2 if n == 3 else 3
            b = rnd.randint(112, a - 60) if lb == 3 else rnd.randint(12, 96)
            if a in tops or (a, b) in seen_s or b % 10 == 0 or not zero_chain(a, b):
                continue
            tops.add(a)
            seen_s.add((a, b))
            its.append(item_sub(a, b, rnd, n % 3 != 2))
            break
    return {"title": "Two exchanges and exchanging across a zero", "items": its}


# ------------------------------------------------------------ set 4: estimate and check with the inverse
def r100(n):
    return int(round(n / 100.0)) * 100


def r10(n):
    return int(round(n / 10.0)) * 10


def set_check(rnd):
    P = People(rnd)
    its = []
    # (a) which calculation checks a subtraction?
    for a, b in [(523, 178), (604, 257), (812, 369)]:
        c = a - b
        other = "%s − %s" % (f(c), f(b)) if c > b else "%s − %s" % (f(b), f(c))
        its.append(mcq("Which calculation checks <b>%s − %s = %s</b>?" % (f(a), f(b), f(c)),
                       "%s + %s" % (f(c), f(b)),
                       ["%s + %s" % (f(a), f(b)), "%s + %s" % (f(a), f(c)), other],
                       "Addition is the inverse of subtraction. Add the answer to the number you took away: "
                       "%s + %s = %s. That is the number you started with, so the answer is right." % (f(c), f(b), f(a)), rnd))
    # (b) which calculation checks an addition?
    for a, b in [(368, 245), (457, 286)]:
        s = a + b
        other = "%s − %s" % (f(a), f(b)) if a > b else "%s − %s" % (f(b), f(a))
        its.append(mcq("Which calculation checks <b>%s + %s = %s</b>?" % (f(a), f(b), f(s)),
                       "%s − %s" % (f(s), f(b)),
                       ["%s + %s" % (f(s), f(b)), other, "%s + %s" % (f(s), f(a))],
                       "Subtraction is the inverse of addition. Take one of the numbers away from the answer: "
                       "%s − %s = %s. You get the other number, so the answer is right." % (f(s), f(b), f(a)), rnd))
    # (c) estimates: round each number to the nearest hundred
    for a, b, op in [(386, 247, "+"), (462, 318, "+"), (275, 549, "+"), (738, 283, "−"), (816, 374, "−")]:
        ra, rb = r100(a), r100(b)
        est = ra + rb if op == "+" else ra - rb
        exact = a + b if op == "+" else a - b
        down = (a // 100 * 100) + (b // 100 * 100) if op == "+" else (a // 100 * 100) - (b // 100 * 100)
        other = abs(ra - rb) if op == "+" else ra + rb
        up = -(-a // 100) * 100 + (-(-b // 100) * 100 if op == "+" else -(-(-b // 100) * 100))
        assert down != est and abs(est - exact) < 100
        its.append(mcq("Round each number to the nearest hundred. Which is the best estimate for %s %s %s?" % (f(a), op, f(b)),
                       "about %s" % f(est), ["about %s" % f(v) for v in [down, other, up, est + 100, est - 100] if v > 0],
                       "%s rounds to %s and %s rounds to %s. %s %s %s = %s. The exact answer is %s, which is close to %s."
                       % (f(a), f(ra), f(b), f(rb), f(ra), op, f(rb), f(est), f(exact), f(est)), rnd))
    # (d) is the answer sensible? (estimate to the nearest ten)
    OK, BIG, SMALL, BIG2 = ("Yes, it is sensible", "No, about 100 too big", "No, about 100 too small",
                            "No, about 200 too big")
    checks = [(531, 264, "−", 531 - 264, "right"),
              (634, 286, "−", sub_small_from_big(634, 286), "small from big"),
              (367, 258, "+", add_forgot_one(367, 258, "last"), "forgot"),
              (284, 453, "+", 284 + 453, "right"),
              (725, 368, "−", sub_forgot_reduce(725, 368), "no reduce")]
    for a, b, op, got, kind in checks:
        n, he, his = P.next()
        exact = a + b if op == "+" else a - b
        ra, rb = r10(a), r10(b)
        est = ra + rb if op == "+" else ra - rb
        err = got - exact
        if kind == "right":
            ans, why = OK, "%s’s answer, %s, is close to the estimate, so it is sensible." % (n, f(got))
        else:
            assert 80 < abs(err) < 130, (a, b, got, err)
            ans = BIG if err > 0 else SMALL
            fix = {"small from big": "%s took the smaller digit from the bigger one in each column instead of exchanging." % cap(he),
                   "forgot": "%s forgot to add the exchanged 1 in the hundreds." % cap(he),
                   "no reduce": "%s made 10 more in a column but did not take 1 away from the next column." % cap(he)}[kind]
            why = ("%s’s answer, %s, is about 100 %s than the estimate. %s The correct answer is %s."
                   % (n, f(got), "bigger" if err > 0 else "smaller", fix, f(exact)))
        assert abs(got - est) < 130 and (kind != "right" or abs(got - est) < 20)
        its.append(mcq("%s worked out %s %s %s = %s. Round each number to the nearest ten to estimate. "
                       "Is %s answer sensible?" % (n, f(a), op, f(b), f(got), his),
                       ans, [OK, BIG, SMALL, BIG2],
                       "Estimate: %s %s %s = %s. " % (f(ra), op, f(rb), f(est)) + why, rnd))
    # (e) missing numbers: use the inverse
    x, b = 366, 286
    s = x + b
    its.append(mcq("What number goes in the box?  <b>☐ + %s = %s</b>" % (f(b), f(s)), f(x),
                   [f(v) for v in [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b)]],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(b), f(x), f(x), f(b), f(s)), rnd))
    a, s = 348, 703
    x = s - a
    its.append(mcq("What number goes in the box?  <b>%s + ☐ = %s</b>" % (f(a), f(s)), f(x),
                   [f(v) for v in [s + a, sub_small_from_big(s, a), sub_zero_as_ten(s, a)]],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s)), rnd))
    r, b = 468, 175
    x = r + b
    its.append(mcq("What number goes in the box?  <b>☐ − %s = %s</b>" % (f(b), f(r)), f(x),
                   [f(v) for v in [r - b, add_no_exchange(r, b), add_forgot_one(r, b, "first")]],
                   "The box is the starting number, so use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                   % (f(r), f(b), f(x), f(x), f(b), f(r)), rnd))
    a, r = 804, 357
    x = a - r
    its.append(mcq("What number goes in the box?  <b>%s − ☐ = %s</b>" % (f(a), f(r)), f(x),
                   [f(v) for v in [a + r, sub_small_from_big(a, r), sub_zero_as_ten(a, r)]],
                   "Think: %s take away what leaves %s? Work out %s − %s = %s. Check: %s − %s = %s."
                   % (f(a), f(r), f(a), f(r), f(x), f(a), f(x), f(r)), rnd))
    a, s = 259, 500
    x = s - a
    its.append(mcq("What number goes in the box?  <b>%s + ☐ = %s</b>" % (f(a), f(s)), f(x),
                   [f(v) for v in [s + a, sub_small_from_big(s, a), sub_zero_as_ten(s, a)]],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s)), rnd))
    return {"title": "Estimate and check with the inverse", "items": its}


# ------------------------------------------------------------ set 5: word problems
def money(v):
    return "£" + f(v)


def unit(v, u):
    return money(v) if u == "£" else "%s %s" % (f(v), u)


def eu(v, u):
    return money(v) if u == "£" else f(v)


def story(q, ans, cands, u, e, rnd):
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e, rnd)


def one_add(q, a, b, u, rnd):
    s = a + b
    assert s <= 999
    e = "Add: %s + %s = %s. Check: %s − %s = %s." % (eu(a, u), eu(b, u), eu(s, u), eu(s, u), eu(b, u), eu(a, u))
    return story(q, s, add_cands(a, b), u, e, rnd)


def one_sub(q, a, b, u, rnd):
    r = a - b
    e = "Subtract: %s − %s = %s. Check: %s + %s = %s." % (eu(a, u), eu(b, u), eu(r, u), eu(r, u), eu(b, u), eu(a, u))
    return story(q, r, sub_cands(a, b), u, e, rnd)


def start_add(q, now, more, u, rnd):
    """Had some, got more, now has `now`: start = now − more."""
    x = now - more
    e = ("Use the inverse. Take away the %s that were added: %s − %s = %s. Check: %s + %s = %s."
         % (f(more), eu(now, u), eu(more, u), eu(x, u), eu(x, u), eu(more, u), eu(now, u)))
    return story(q, x, sub_cands(now, more), u, e, rnd)


def start_sub(q, now, lost, u, rnd):
    """Had some, lost some, now has `now`: start = now + lost."""
    x = now + lost
    assert x <= 999
    e = ("Use the inverse. Add back the %s that were lost: %s + %s = %s. Check: %s − %s = %s."
         % (f(lost), eu(now, u), eu(lost, u), eu(x, u), eu(x, u), eu(lost, u), eu(now, u)))
    return story(q, x, [now - lost] + add_cands(now, lost), u, e, rnd)


def sold_both_left(q, A, B, C, u, rnd, s1, s2):
    """A − (B + C)."""
    t = B + C
    r = A - t
    e = ("Step 1, %s: %s + %s = %s. Step 2, %s: %s − %s = %s. Check: %s + %s = %s."
         % (s1, eu(B, u), eu(C, u), eu(t, u), s2, eu(A, u), eu(t, u), eu(r, u), eu(r, u), eu(t, u), eu(A, u)))
    return story(q, r, [t, A - B, sub_small_from_big(A, t), sub_zero_as_ten(A, t), sub_forgot_reduce(A, t), A - B + C], u, e, rnd)


def out_then_in(q, A, B, C, u, rnd, s1, s2):
    """A − B + C."""
    m = A - B
    r = m + C
    e = "Step 1, %s: %s − %s = %s. Step 2, %s: %s + %s = %s." % (s1, f(A), f(B), f(m), s2, f(m), f(C), f(r))
    return story(q, r, [m, A - B - C, sub_small_from_big(A, B) + C, add_forgot_one(m, C, "last"), A + B + C], u, e, rnd)


def more_than_total(q, A, B, u, rnd, who2):
    """A + (A + B)."""
    m = A + B
    r = A + m
    assert r <= 999
    e = ("Step 1, %s: %s + %s = %s. Step 2, both together: %s + %s = %s."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + A, m + B, add_forgot_one(A, m, "last")], u, e, rnd)


def less_than_total(q, A, B, u, rnd, who2):
    """A + (A − B)."""
    m = A - B
    r = A + m
    e = ("Step 1, %s: %s − %s = %s. Step 2, both together: %s + %s = %s."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + B, add_forgot_one(A, m, "last"), A + A + B], u, e, rnd)


def set_story(rnd):
    its = [
        one_add("Class 3 raised £258 for the school trip. Class 4 raised £316. How much did they raise altogether?",
                258, 316, "£", rnd),
        one_add("A library had 476 books. It got 185 new books. How many books does it have now?", 476, 185, "books", rnd),
        one_add("Isla scored 347 points in a game. Then she scored 286 more points. How many points does she have now?",
                347, 286, "points", rnd),
        one_add("There are 268 children in the infants and 345 children in the juniors. How many children are there altogether?",
                268, 345, "children", rnd),
        one_add("The coach for a school trip costs £385. The tickets cost £249. What is the total cost?", 385, 249, "£", rnd),
        one_sub("A school trip to the zoo costs £600. The school has £364. How much more money does it need?",
                600, 364, "£", rnd),
        one_sub("A library has 742 books. 158 books are lent out. How many books are still on the shelves?",
                742, 158, "books", rnd),
        one_sub("Leo has 905 points in a game. Ruby has 678 points. How many more points does Leo have?",
                905, 678, "points", rnd),
        one_sub("A cinema has 450 seats. 287 seats are taken. How many seats are empty?", 450, 287, "seats", rnd),
        one_sub("A farmer had 634 eggs. He sold 279 eggs. How many eggs are left?", 634, 279, "eggs", rnd),
        one_sub("A book has 312 pages. Amelia has read 145 pages. How many pages does she have left to read?",
                312, 145, "pages", rnd),
        one_sub("A sticker book holds 500 stickers. Arjun has 263 stickers. How many more does he need to fill it?",
                500, 263, "stickers", rnd),
        start_add("Freya had some beads. She bought 145 more. Now she has 403 beads. How many beads did she have at the start?",
                  403, 145, "beads", rnd),
        start_sub("Mohammed had some points in a game. He lost 175 points. Now he has 389 points. "
                  "How many points did he have at the start?", 389, 175, "points", rnd),
        sold_both_left("A school trip costs £800. The cake sale raised £356. The summer fair raised £287. "
                       "How much more money is needed?", 800, 356, 287, "£", rnd, "money raised", "money still needed"),
        out_then_in("The library had 625 books. It lent out 248 books. Then 136 books came back. How many books are there now?",
                    625, 248, 136, "books", rnd, "after lending", "after the books came back"),
        more_than_total("Jack scored 286 points. Grace scored 157 more points than Jack. How many points did they score altogether?",
                        286, 157, "points", rnd, "Grace’s points"),
        sold_both_left("A shop had 512 bags of crisps. It sold 168 bags on Monday and 195 bags on Tuesday. How many bags are left?",
                       512, 168, 195, "bags", rnd, "bags sold", "bags left"),
        less_than_total("On Monday, 374 people visited a museum. On Tuesday, 128 fewer people visited. "
                        "How many people visited on the two days?", 374, 128, "people", rnd, "Tuesday"),
        sold_both_left("Year 3 collected 268 cans for recycling. Year 4 collected 315 cans. The target was 700 cans. "
                       "How many more cans do they need?", 700, 268, 315, "cans", rnd, "cans collected", "cans still needed"),
    ]
    return {"title": "Word problems and missing numbers", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    assert 245 + 138 == 383 and 367 + 258 == 625 and 563 - 128 == 435 and 452 - 178 == 274 and 402 - 158 == 244
    assert add_no_exchange(367, 258) == 515 and sub_small_from_big(452, 178) == 326
    assert sub_zero_skip(402, 158) == 254 and add_misalign(345, 23) == 575 and 345 + 23 == 368
    return (
        "<h2>The idea: line up the columns</h2>"
        "<p>Write the numbers in columns. Put <b>ones under ones</b>, tens under tens and hundreds under hundreds. "
        "Always start with the <b>ones</b> on the right.</p>"
        "<p>If a column adds up to 10 or more, write the ones digit. Then <b>exchange</b> 10 for 1 in the next column. "
        "Write the exchanged 1 small, under the answer line.</p>"
        "<figure class='sn-fig'>" + column_svg(245, 138, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 5 + 8 = 13. Write 3 and exchange 10 ones for 1 ten. Tens: 4 + 3 + 1 = 8. "
        "Hundreds: 2 + 1 = 3. Answer: 383.</figcaption></figure>" +
        ex("Two exchanges", "What is 367 + 258?",
           "Ones: 7 + 8 = 15. Write 5 and exchange 1 ten. Tens: 6 + 5 + 1 = 12. Write 2 and exchange 1 hundred. "
           "Hundreds: 3 + 2 + 1 = 6.", "625") +
        "<h2>Column subtraction with exchanging</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, <b>exchange</b>. "
        "Take 1 from the next column and make 10 more in this column. Cross out the old digit and write the new one above it.</p>"
        "<figure class='sn-fig'>" + column_svg(563, 128, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 3 − 8. Exchange 1 ten for 10 ones: 13 − 8 = 5. Tens: now 5 − 2 = 3. "
        "Hundreds: 5 − 1 = 4. Answer: 435.</figcaption></figure>"
        "<figure class='sn-fig'>" + column_svg(452, 178, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 8. Exchange 1 ten for 10 ones: 12 − 8 = 4. Tens: now 4 − 7. "
        "Exchange 1 hundred for 10 tens: 14 − 7 = 7. Hundreds: now 3 − 1 = 2. Answer: 274.</figcaption></figure>"
        "<h2>Exchanging across a zero</h2>"
        "<p>If the tens digit is 0, there are no tens to take. First exchange 1 hundred for 10 tens. "
        "Then exchange 1 ten for 10 ones. The 0 becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + column_svg(402, 158, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 8. There are 0 tens. Exchange 1 hundred for 10 tens, then 1 ten for 10 ones. "
        "Now the top number is 3 hundreds, 9 tens and 12 ones. 12 − 8 = 4, 9 − 5 = 4, 3 − 1 = 2. Answer: 244.</figcaption></figure>"
        "<h2>Check your answer</h2>"
        "<p><b>Use the inverse.</b> Addition and subtraction undo each other. To check 452 − 178 = 274, add: "
        "274 + 178 = 452. You get back to the start, so the answer is right.</p>"
        "<p><b>Estimate.</b> Round each number and do an easier sum. "
        "452 − 178 is about 450 − 180 = 270. An answer of 274 is sensible. An answer of 326 is not.</p>"
        "<h2>Missing numbers and word problems</h2>"
        "<p>For a missing number, use the inverse. For ☐ + 145 = 403, work out 403 − 145 = 258. "
        "In a word problem, ask: am I putting together (add) or taking away and finding the difference (subtract)?</p>" +
        ex("Two steps", "A school trip costs £800. The cake sale raised £356 and the fair raised £287. How much more is needed?",
           "Step 1, money raised: £356 + £287 = £643. Step 2, money still needed: £800 − £643 = £157.", "£157") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the exchanged 1 (367 + 258 = 515)", "Write the exchanged 1 under the next column and add it in"],
            ["Taking the smaller digit from the bigger one (452 − 178 = 326)", "Always take the bottom digit from the top digit. Exchange when the top is smaller"],
            ["Not exchanging across a zero (402 − 158 = 254)", "Exchange 1 hundred for 10 tens first. The 0 becomes 9"],
            ["Lining up the numbers on the left (345 + 23 = 575)", "Line up the ones on the right: 345 + 23 = 368"],
        ])
    )


FAQ = [
    {"q": "Do Year 3 children learn column addition and subtraction?",
     "a": "Yes. The National Curriculum says Year 3 pupils should add and subtract numbers with up to three digits using the formal written methods of column addition and subtraction."},
    {"q": "What does “exchange” mean in column subtraction?",
     "a": "Exchanging means swapping 1 from the next column for 10 in this column, for example 1 ten for 10 ones. It is what older books call borrowing or carrying."},
    {"q": "How do you subtract across a zero, like 402 − 158?",
     "a": "Exchange 1 hundred for 10 tens, then 1 ten for 10 ones. 402 becomes 3 hundreds, 9 tens and 12 ones, and the answer is 244."},
    {"q": "How can my child check an addition or subtraction answer?",
     "a": "Use the inverse: for 452 − 178 = 274, check that 274 + 178 = 452. A quick estimate, such as 450 − 180 = 270, also shows whether the answer is sensible."},
]


def gen():
    rnd = random.Random(3303)
    seen_a, seen_s = set(), set()
    sets = [set_add(rnd, seen_a), set_sub1(rnd, seen_s), set_hard(rnd, seen_a, seen_s), set_check(rnd), set_story(rnd)]
    balance(sets, rnd)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
    return {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "column-addition-and-subtraction", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Column Addition and Subtraction",
        "seo_title": "Year 3 Column Addition and Subtraction Worksheets: 3-Digit Numbers, Exchanging and Checking",
        "short_title": "Column addition and subtraction",
        "domain": "Addition and subtraction",
        "standard_code": "Year 3: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Add and subtract numbers with up to three digits, using formal written methods of columnar addition and "
                         "subtraction; estimate the answer to a calculation and use inverse operations to check answers; solve "
                         "problems, including missing number problems, using number facts, place value, and more complex addition "
                         "and subtraction.",
        "meta_desc": "Free Year 3 maths worksheets on column addition and subtraction with 3-digit numbers, following the National "
                     "Curriculum: exchanging, subtracting across a zero, estimating, checking with the inverse, missing numbers "
                     "and word problems. 100 questions with an answer key.",
        "key_big": "Line up the ones. Start on the right. Exchange when you need to.",
        "key_sub": "Adding: if a column makes 10 or more, exchange 1 into the next column. Subtracting: if the top digit is smaller, "
                   "exchange 1 from the next column. Check with the inverse or an estimate.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
