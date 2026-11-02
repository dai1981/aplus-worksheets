# -*- coding: utf-8 -*-
"""
CA-BC Grade 5 Math: Adding and subtracting whole numbers to 1 000 000
(BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g5_add_sub.py
Column addition of 5- and 6-digit numbers, subtracting across zeros (like 600 000 − 248 365),
estimating first, checking with the inverse, and BC word problems (2021 census populations, distances).
Canadian English. 4-digit numbers have no separator (4536); 5+ digits use a no-break space (245 300).
Every answer and every wrong answer is computed in code.
HTML attributes use single quotes (no backslashes in the JSON).
Column helpers are copied from gen_cabc_math_g4_add_sub.py (same method, extended to 1 000 000).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
ONE = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]
MILLION = "1" + NB + "000" + NB + "000"


def f(n):
    """4 digits no separator, 5+ digits a no-break space between groups of three."""
    s = str(n)
    if len(s) <= 4:
        return s
    return "{:,}".format(n).replace(",", NB)


def num(s):
    return int(s.replace(NB, "").replace("$", ""))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique sensible distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$+")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead in ("0", ""):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


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


def digits(n, k=None):
    k = k or nlen(n)
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def clean(vals):
    return [v for v in vals if v is not None and v > 0]



def column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line. The space in a 5-digit number gets its own narrow slot.
    answer: also write the answer.  marks: red regrouping marks
    (+: the regrouped 1s written small under the answer line;  −: old digits crossed out, new digits above)."""
    cw, kw = fs * (0.82 if marks else 0.62), fs * 0.3
    res = a + b if op == "+" else a - b
    wide = max(nlen(a), nlen(b), nlen(res)) >= 5
    g = (lambda n: "{:,}".format(n).replace(",", NB)) if wide else f     # 3775 under 30 934 needs the gap too
    rows = [g(a), g(b)] + ([g(res)] if answer else [])

    def xs(s):                     # x centre of every char, right-aligned
        out, x = [], 0.0
        for ch in reversed(s):
            w = kw if ch == NB else cw
            out.append(x + w / 2)
            x += w
        return list(reversed(out)), x

    longest = max(xs(r)[1] for r in rows)
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 12)
    right = W - 12
    top = 10 + (int(fs * 0.62) if marks and op != "+" else 0)
    s = []

    def put(t, y, color):
        cx, _ = xs(t)
        for ch, x in zip(t, cx):
            if ch == NB:
                continue
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - x, y, fs, color, ch))

    y1, y2 = top + fs, top + int(fs * 2.15)
    put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    longrow = max(rows, key=lambda r: xs(r)[1])
    lx, _ = xs(longrow)
    place_x = [right - x for ch, x in zip(reversed(longrow), reversed(lx)) if ch != NB]
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
            nd = regroup_digits(a, b)
            od = digits(a)
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%s %s %s written in columns" % (f(a), "plus" if op == "+" else "minus", f(b))
    return svg_wrap(W, int(H), "".join(s), label)


# ------------------------------------------------------------ column methods
def regroup_digits(a, b):
    """Top digits after all the regrouping of column subtraction (ones first)."""
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


def regroups_sub(a, b):
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
    """True if some regrouping has to go across a 0."""
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


def add_steps(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    kb = min(nlen(a), nlen(b))
    carry, ps = 0, []
    for i in range(k):
        t = da[i] + db[i] + carry
        if i >= kb:
            big = da[i] if nlen(a) > nlen(b) else db[i]
            expr = "%d + 1" % big if carry else None
        else:
            expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        P = cap(PLACE[i])
        if t >= 10 and i == k - 1:
            ps.append("%s: %s = %d, write %d." % (P, expr, t, t))
            carry = 0
        elif t >= 10:
            ps.append("%s: %s = %d. Write %d and regroup 10 %s as 1 %s." % (P, expr, t, t % 10, PLACE[i], ONE[i + 1]))
            carry = 1
        else:
            ps.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    s = a + b
    return ("Line up the ones and start on the right. " + " ".join(ps) +
            " Answer: <b>%s</b>. Check with the inverse: %s − %s = %s." % (f(s), f(s), f(b), f(a)))


def sub_steps(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    kb = nlen(b)
    ps = []
    for i in range(k):
        P = cap(PLACE[i])
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                zl = ["0 %s" % PLACE[m] for m in range(i + 1, j)]
                zeros = zl[0] if len(zl) == 1 else ", ".join(zl[:-1]) + " and " + zl[-1]
                chain = ", then ".join("1 %s as 10 %s" % (ONE[m], PLACE[m - 1]) for m in range(j, i, -1))
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. There are %s, so regroup %s. Each 0 becomes 9. %d − %d = %d."
                       % (P, cur, db[i], zeros, chain, d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d. Regroup 1 %s as 10 %s: %d − %d = %d."
                       % (P, cur, db[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
            ps.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                ps.append("%s: write %d." % (P, d[i]))
        else:
            ps.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    return ("Line up the ones and start on the right. " + " ".join(ps) +
            " Answer: <b>%s</b>. Check with the inverse: %s + %s = %s." % (f(r), f(r), f(b), f(a)))


# ------------------------------------------------------------ typical mistakes
def add_no_regroup(a, b):
    """Never adds the regrouped 1s (writes the full sum only in the last column)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    return sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))


def add_forgot_one(a, b, which):
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return a + b - 10 ** (i + 1)


def add_misalign(a, b):
    """Lined up the shorter number one place too far left."""
    if nlen(a) == nlen(b):
        return None
    return max(a, b) + min(a, b) * 10


def add_extra_one(a, b):
    cols = set(add_carry_cols(a, b))
    k = max(nlen(a), nlen(b))
    return [a + b + 10 ** (i + 1) for i in range(k - 1) if i not in cols]


def sub_small_from_big(a, b):
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))


def sub_forgot_reduce(a, b):
    """Made 10 more but did not take 1 away from the next place."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    out = 0
    for i in range(k):
        if d[i] < db[i]:
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out


def sub_zero_as_ten(a, b):
    """Regrouping across zeros: changed the zeros to 10 instead of 9."""
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
    """Did not regroup across the zero: took 1 straight from the next non-zero digit, left the zeros as 0,
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


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_regroup(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b)] + every + add_extra_one(a, b) + [abs(a - b)])


def sub_cands(a, b):
    return clean([sub_zero_skip(a, b), sub_zero_as_ten(a, b), sub_small_from_big(a, b), sub_forgot_reduce(a, b),
                  sub_misalign(a, b), a - b + 10, a - b - 10, a - b + 100, a + b])



def rnd_to(n, p):
    return (n + p // 2) // p * p


def down_to(n, p):
    return n // p * p


PNAME = {1000: "thousand", 10000: "ten thousand", 100000: "hundred thousand"}


# ------------------------------------------------------------ set 1: column addition
LESSON_A = {(458769, 276548), (352846, 41275)}
LESSON_S = {(600000, 248365), (503214, 186597)}


def item_add(a, b, col):
    q = (fig(column_svg(a, b, "+")) + "Add. Line up the ones and regroup when a column makes 10 or more.") if col else \
        "Use column addition. What is %s + %s?" % (f(a), f(b))
    return mcq(q, f(a + b), [f(v) for v in add_cands(a, b)], add_steps(a, b))


def item_sub(a, b, col):
    q = (fig(column_svg(a, b, "-")) + "Subtract. Regroup when the top digit is smaller.") if col else \
        "Use column subtraction. What is %s − %s?" % (f(a), f(b))
    return mcq(q, f(a - b), [f(v) for v in sub_cands(a, b)], sub_steps(a, b))


def pick_add(rnd, seen, la, lb, want, top=999999):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 5, 10 ** la - 10 ** (la - 1) // 2)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 5, 10 ** lb - 10 ** (lb - 1) // 2)
        if a + b > top or (a, b) in seen or (b, a) in seen or (a, b) in LESSON_A or a % 10 == 0 or b % 10 == 0:
            continue
        if len(add_carry_cols(a, b)) != want:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = ([(5, 5, 1)] * 2 + [(5, 5, 2)] * 2 + [(5, 4, 2)] + [(6, 5, 2)] * 2 + [(6, 6, 2)] +
            [(6, 5, 3)] * 2 + [(6, 4, 3)] + [(6, 6, 3)] * 2 + [(6, 5, 4)] * 2 + [(6, 6, 4)] * 3 + [(6, 6, 5)])
    for i, (la, lb, want) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, want)
        if la != lb and i % 3 == 2:          # in words: the numbers have different lengths, so lining up matters
            assert add_misalign(a, b)
        its.append(item_add(a, b, i % 3 != 2))
    its.append(item_add(637485, 362515, True))          # regroup in every column: exactly 1 000 000
    assert 637485 + 362515 == 1000000
    assert len(its) == 20
    return {"title": "Column addition of large numbers", "items": its}


# ------------------------------------------------------------ set 2: subtraction across zeros
def pick_sub(rnd, seen, la, lb, want):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 2, 10 ** la - 1)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 10, min(10 ** lb - 1, a - 10 ** (la - 1) // 4))
        if (a, b) in seen or (a, b) in LESSON_S or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if regroups_sub(a, b) == want:
            seen.add((a, b))
            return a, b


def set_sub(rnd, seen):
    its = []
    for i, (la, lb, want) in enumerate([(5, 5, 1), (5, 4, 2), (6, 5, 2), (6, 6, 3)]):
        a, b = pick_sub(rnd, seen, la, lb, want)
        its.append(item_sub(a, b, i % 3 != 2))
    tops = {600000, 503214}                              # lesson examples
    pats = [("x0xxx", 4), ("x00xx", 4), ("x00xx", 5), ("x000x", 4), ("x0000", 5), ("xx00xx", 5),
            ("x000xx", 5), ("x00x0x", 5), ("x0000x", 5), ("x0000x", 6), ("x00000", 5), ("x00000", 6),
            ("xx000x", 6), ("x0x00x", 6), ("100000", 5), ("1000000", 6)]
    for n, (p, lb) in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lo = 10 ** (lb - 1) + 10 ** (lb - 1) // 10
            hi = min(10 ** lb - 1, a - 10 ** (len(p) - 1) // 5)
            if hi <= lo:
                continue
            b = rnd.randint(lo, hi)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or regroups_sub(a, b) < 2:
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, (n + 4) % 3 != 2))
            break
    assert len(its) == 20
    return {"title": "Subtraction across zeros", "items": its}


# ------------------------------------------------------------ set 3: estimate first
def est_round(rnd, seen, op, p):
    """Round both numbers to place p. At least one number rounds up, so cutting off gives a different estimate."""
    while True:
        a = rnd.randint(150000, 880000)
        b = rnd.randint(30000, 420000) if op == "−" else rnd.randint(60000, 990000 - a)
        if op == "−" and b >= a - 50000:
            continue
        if a % 10 == 0 or b % 10 == 0 or (a, b) in seen:
            continue
        ra, rb = rnd_to(a, p), rnd_to(b, p)
        if ra == down_to(a, p) and rb == down_to(b, p):
            continue
        if op == "−" and ra - rb < 2 * p:
            continue
        if rb == 0 or a % p < p // 10 or b % p < p // 10 or abs(a % p - p // 2) < p // 10 or abs(b % p - p // 2) < p // 10:
            continue
        seen.add((a, b))
        return a, b


def item_est(a, b, op, p):
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    est = ra + rb if op == "+" else ra - rb
    exact = a + b if op == "+" else a - b
    cut = (down_to(a, p) + down_to(b, p)) if op == "+" else (down_to(a, p) - down_to(b, p))
    other = {1000: 10000, 10000: 100000, 100000: 10000}[p]
    oe = rnd_to(a, other) + rnd_to(b, other) if op == "+" else rnd_to(a, other) - rnd_to(b, other)
    ways = lambda x, rx: "rounds up to" if rx > x else "rounds down to"
    e = ("%s %s %s. %s %s %s. %s %s %s = <b>%s</b>. (The exact answer is %s.)"
         % (f(a), ways(a, ra), f(ra), f(b), ways(b, rb), f(rb), f(ra), op, f(rb), f(est), f(exact)))
    if abs(cut - exact) > abs(est - exact):
        e += " Cutting off the digits instead of rounding gives %s, which is not as close." % f(cut)
    return mcq("Round each number to the nearest %s to estimate %s %s %s." % (PNAME[p], f(a), op, f(b), ),
               f(est), [f(v) for v in clean([cut, exact, oe, est + p, est - p])], e)


def set_estimate(rnd, P):
    its, seen = [], set()
    # (a) rounding estimates, easy to hard
    for op, p in [("+", 1000), ("−", 1000), ("+", 10000), ("−", 10000), ("+", 10000), ("+", 100000), ("−", 100000),
                  ("−", 100000)]:
        a, b = est_round(rnd, seen, op, p)
        its.append(item_est(a, b, op, p))
    # (b) best estimate: numbers close to friendly numbers
    for a, b, op, ra, rb in [(299850, 449920, "+", 300000, 450000), (700150, 199890, "−", 700000, 200000),
                             (498760, 251080, "+", 500000, 250000)]:
        est = ra + rb if op == "+" else ra - rb
        exact = a + b if op == "+" else a - b
        right = "%s %s %s = %s" % (f(ra), op, f(rb), f(est))
        ca, cb = down_to(a, 100000), down_to(b, 100000)
        w1 = "%s %s %s = %s" % (f(ca), op, f(cb), f(ca + cb if op == "+" else ca - cb))
        w2 = "%s %s %s = %s" % (f(ra), op, f(rb + 100000), f(est + 100000 if op == "+" else est - 100000))
        w3 = "%s %s %s = %s" % (f(ra - 100000), op, f(rb), f(est - 100000))
        its.append(mcq("Which is the best estimate for %s %s %s?" % (f(a), op, f(b)), right, [w1, w2, w3],
                       "%s is very close to %s and %s is very close to %s. <b>%s</b>. The exact answer is %s."
                       % (f(a), f(ra), f(b), f(rb), right, f(exact))))
    # (c) is the answer reasonable?
    cases = [(386542, 247815, "+", add_no_regroup(386542, 247815), 10000),
             (452378, 36541, "+", add_misalign(452378, 36541), 10000),
             (712406, 285739, "−", 712406 - 285739, 10000),
             (630000, 274568, "−", sub_small_from_big(630000, 274568), 10000)]
    for a, b, op, got, p in cases:
        n, he, his = P.next()
        exact = a + b if op == "+" else a - b
        ra, rb = rnd_to(a, p), rnd_to(b, p)
        est = ra + rb if op == "+" else ra - rb
        ok = got == exact
        assert ok or abs(got - est) >= 50000, (a, b, got, est)
        alt = rnd_to(a, 100000) + rnd_to(b, 100000) if op == "+" else rnd_to(a, 100000) - rnd_to(b, 100000)
        if alt == est:
            alt = est + 100000
        yes = "Yes. The estimate is %s" % f(est)
        no = "No. The estimate is %s" % f(est)
        right = yes if ok else no
        wrong = [no if ok else yes, "Yes. The estimate is %s" % f(got if not ok else alt),
                 "No. The estimate is %s" % f(alt)]
        why = ("%s is close to %s, so <b>the answer is reasonable</b>." % (f(got), f(est)) if ok else
               "%s is far from %s, so <b>the answer is not reasonable</b>. The exact answer is %s." % (f(got), f(est), f(exact)))
        e = "%s rounds to %s and %s rounds to %s. %s %s %s = %s. " % (f(a), f(ra), f(b), f(rb), f(ra), op, f(rb), f(est)) + why
        if not ok:
            e += {0: " (%s did not regroup.)" % n, 1: " (%s lined up %s on the left, not under the ones.)" % (n, f(b)),
                  3: " (%s took the smaller digit from the larger one in each column.)" % n}[cases.index((a, b, op, got, p))]
        its.append(mcq("%s worked out %s %s %s = %s. Estimate to the nearest ten thousand. Is %s answer reasonable?"
                       % (n, f(a), op, f(b), f(got), his), right, wrong, e))
    # (d) use an estimate to pick the only answer that could be right
    for a, b, op in [(345612, 228475, "+"), (806254, 379618, "−"), (126837, 584296, "+"), (900215, 462738, "−")]:
        exact = a + b if op == "+" else a - b
        ra, rb = rnd_to(a, 100000), rnd_to(b, 100000)
        est = ra + rb if op == "+" else ra - rb
        if op == "+":
            wrong = [a + b * 10, a - b if a > b else b - a, a + b // 10, exact + 200000, exact + 300000, exact - 300000]
        else:
            wrong = [a + b, a - b // 10, exact + 300000, exact - 200000, exact + 200000]
        gap = abs(exact - est)
        wrong = [w for w in clean(wrong) if abs(w - est) >= max(0.3 * est, 2.5 * gap) and w < 1000000]
        its.append(mcq("Estimate first. Only one answer can be right. What is %s %s %s?" % (f(a), op, f(b)),
                       f(exact), [f(w) for w in wrong],
                       "Round to the nearest hundred thousand: %s %s %s = %s. Only <b>%s</b> is close to %s."
                       % (f(ra), op, f(rb), f(est), f(exact), f(est))))
    # (e) estimate in a story
    a, b = 286450, 362480
    assert rnd_to(a, 10000) + rnd_to(b, 10000) == 650000 and down_to(a, 10000) + down_to(b, 10000) == 640000
    its.append(mcq("A ferry route carried " + f(a) + " passengers in July and " + f(b) + " in August. "
                   "Round to the nearest ten thousand. About how many passengers is that?",
                   f(650000), [f(v) for v in [640000, a + b, 700000]],
                   "%s rounds up to %s. %s rounds down to %s. %s + %s = <b>%s</b>. (The exact total is %s.)"
                   % (f(a), f(290000), f(b), f(360000), f(290000), f(360000), f(650000), f(a + b))))
    assert len(its) == 20, len(its)
    return {"title": "Estimate first", "items": its}


# ------------------------------------------------------------ set 4: check with the inverse
def set_inverse(rnd, P):
    its = []
    for a, b in [(624150, 387462), (800403, 256718)]:
        c = a - b
        its.append(mcq("Which calculation checks <b>%s − %s = %s</b>?" % (f(a), f(b), f(c)),
                       "%s + %s" % (f(c), f(b)),
                       ["%s + %s" % (f(a), f(b)), "%s + %s" % (f(a), f(c)),
                        "%s − %s" % (f(c), f(b)) if c > b else "%s − %s" % (f(b), f(c))],
                       "Addition is the inverse of subtraction. Add the answer to the number you took away: "
                       "%s + %s = %s. You get back to the start, so the answer is right." % (f(c), f(b), f(a))))
    a, b = 357286, 264519
    s = a + b
    its.append(mcq("Which calculation checks <b>%s + %s = %s</b>?" % (f(a), f(b), f(s)),
                   "%s − %s" % (f(s), f(b)),
                   ["%s + %s" % (f(s), f(b)), "%s − %s" % (f(a), f(b)), "%s + %s" % (f(s), f(a))],
                   "Subtraction is the inverse of addition. Take one number away from the answer: "
                   "%s − %s = %s. You get the other number, so the answer is right." % (f(s), f(b), f(a))))
    for a, b in [(738205, 249687), (95412, 47658)]:
        c = a - b
        its.append(mcq("%s − %s = %s. Which number sentence is also true?" % (f(a), f(b), f(c)),
                       "%s + %s = %s" % (f(c), f(b), f(a)),
                       ["%s − %s = %s" % (f(c), f(b), f(a)), "%s + %s = %s" % (f(a), f(b), f(c)),
                        "%s + %s = %s" % (f(a), f(c), f(b))],
                       "The three numbers make a fact family. The two smaller numbers add to make the biggest: "
                       "<b>%s + %s = %s</b>." % (f(c), f(b), f(a))))
    # missing numbers
    miss = []
    x, b = 46275, 38946
    s = x + b
    miss.append(("<b>☐ + %s = %s</b>" % (f(b), f(s)), x, [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b)],
                 "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(b), f(x), f(x), f(b), f(s))))
    a, s = 248637, 500000
    x = s - a
    miss.append(("<b>%s + ☐ = %s</b>" % (f(a), f(s)), x, [s + a, sub_small_from_big(s, a), sub_zero_as_ten(s, a)],
                 "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s))))
    r, b = 372846, 185379
    x = r + b
    miss.append(("<b>☐ − %s = %s</b>" % (f(b), f(r)), x, [r - b, add_no_regroup(r, b), add_forgot_one(r, b, "first")],
                 "The box is the starting number, so use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                 % (f(r), f(b), f(x), f(x), f(b), f(r))))
    a, r = 704050, 268375
    x = a - r
    miss.append(("<b>%s − ☐ = %s</b>" % (f(a), f(r)), x, [a + r, sub_small_from_big(a, r), sub_zero_as_ten(a, r)],
                 "Think: %s take away what leaves %s? Work out %s − %s = %s. Check: %s − %s = %s."
                 % (f(a), f(r), f(a), f(r), f(x), f(a), f(x), f(r))))
    a, s = 415862, 693207
    x = s - a
    miss.append(("<b>%s + ☐ = %s</b>" % (f(a), f(s)), x, [s + a, sub_small_from_big(s, a), sub_forgot_reduce(s, a)],
                 "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s))))
    r, b = 529468, 94753
    x = r + b
    miss.append(("<b>☐ − %s = %s</b>" % (f(b), f(r)), x, [r - b, add_no_regroup(r, b), add_misalign(r, b)],
                 "The box is the starting number, so use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                 % (f(r), f(b), f(x), f(x), f(b), f(r))))
    for q, x, wrong, e in miss:
        its.append(mcq("What number goes in the box?  " + q, f(x), [f(v) for v in clean(wrong)], e))
    # missing numbers in words
    a, s = 386475, 1000000
    x = s - a
    its.append(mcq("What number do you add to 386" + NB + "475 to make " + MILLION + "?", f(x),
                   [f(v) for v in clean([sub_zero_as_ten(s, a), sub_small_from_big(s, a), s + a, x + 10])],
                   "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s))))
    r, b = 158264, 247839
    x = r + b
    its.append(mcq("A number minus 247" + NB + "839 is 158" + NB + "264. What is the number?", f(x),
                   [f(v) for v in clean([b - r, add_no_regroup(r, b), add_forgot_one(r, b, "last"), x + 1000])],
                   "Work backwards and add: %s + %s = <b>%s</b>. Check: %s − %s = %s." % (f(r), f(b), f(x), f(x), f(b), f(r))))
    # did they get it right?
    YES = "Yes, it is correct"
    checks = [(562413, 278546, "−", 562413 - 278546),
              (468275, 297846, "+", add_no_regroup(468275, 297846)),
              (700306, 258427, "−", sub_zero_skip(700306, 258427)),
              (184596, 627835, "+", 184596 + 627835),
              (831052, 46378, "−", sub_misalign(831052, 46378)),
              (94368, 75846, "+", add_forgot_one(94368, 75846, "last")),
              (605140, 327465, "−", sub_small_from_big(605140, 327465))]
    for a, b, op, got in checks:
        assert got
        n, he, his = P.next()
        exact = a + b if op == "+" else a - b
        if op == "−":
            back = got + b
            chk = "%s + %s = %s" % (f(got), f(b), f(back))
        else:
            back = got - b
            chk = "%s − %s = %s" % (f(got), f(b), f(back))
        ok = back == a
        assert ok == (got == exact)
        if ok:
            ans = YES
            why = "The check gives %s, the number %s started with, so the answer is right." % (f(a), he)
            wrong = ["No, it should be %s" % f(v) for v in clean(
                [sub_small_from_big(a, b), sub_forgot_reduce(a, b), exact + 1000] if op == "−"
                else [add_no_regroup(a, b), add_forgot_one(a, b, "last"), exact - 1000])]
        else:
            ans = "No, it should be %s" % f(exact)
            why = ("The check gives %s, not %s, so the answer is wrong. The correct answer is <b>%s</b>."
                   % (f(back), f(a), f(exact)))
            wrong = [YES, "No, it should be %s" % f(back),
                     "No, it should be %s" % f(exact + 10000), "No, it should be %s" % f(exact - 100)]
        its.append(mcq("%s worked out %s %s %s = %s. Use the inverse to check. Is %s answer correct?"
                       % (n, f(a), op, f(b), f(got), his), ans, wrong,
                       "Check with the inverse: %s. " % chk + why))
    assert len(its) == 20, len(its)
    return {"title": "Check with the inverse", "items": its}


# ------------------------------------------------------------ set 5: word problems
def unit(v, u):
    return "$" + f(v) if u == "$" else "%s %s" % (f(v), u)


def eu(v, u):
    return "$" + f(v) if u == "$" else f(v)


def story(q, ans, cands, u, e):
    assert 0 < ans <= 1000000
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e)


def one_add(q, a, b, u, lead):
    s = a + b
    e = lead + " %s + %s = <b>%s</b>. Check: %s − %s = %s." % (eu(a, u), eu(b, u), eu(s, u), eu(s, u), eu(b, u), eu(a, u))
    return story(q, s, add_cands(a, b), u, e)


def one_sub(q, a, b, u, lead):
    r = a - b
    e = lead + " %s − %s = <b>%s</b>. Check: %s + %s = %s." % (eu(a, u), eu(b, u), eu(r, u), eu(r, u), eu(b, u), eu(a, u))
    return story(q, r, sub_cands(a, b), u, e)


def start_add(q, now, more, u):
    x = now - more
    e = ("Work backwards. Take away the %s that came later: %s − %s = <b>%s</b>. Check: %s + %s = %s."
         % (f(more), eu(now, u), eu(more, u), eu(x, u), eu(x, u), eu(more, u), eu(now, u)))
    return story(q, x, [now + more] + sub_cands(now, more), u, e)


def both_left(q, A, B, C, u, s1, s2):
    """A − (B + C)."""
    t = B + C
    r = A - t
    e = ("Step 1, %s: %s + %s = %s. Step 2, %s: %s − %s = <b>%s</b>."
         % (s1, eu(B, u), eu(C, u), eu(t, u), s2, eu(A, u), eu(t, u), eu(r, u)))
    return story(q, r, [A - B, t, sub_small_from_big(A, t), sub_zero_as_ten(A, t), sub_forgot_reduce(A, t), A - B + C], u, e)


def out_then_in(q, A, B, C, u, s1, s2):
    """A − B + C."""
    m = A - B
    r = m + C
    e = "Step 1, %s: %s − %s = %s. Step 2, %s: %s + %s = <b>%s</b>." % (
        s1, eu(A, u), eu(B, u), eu(m, u), s2, eu(m, u), eu(C, u), eu(r, u))
    return story(q, r, [m, A - B - C, sub_small_from_big(A, B) + C, add_forgot_one(m, C, "last"), A + B + C], u, e)


def more_total(q, A, B, u, who2):
    """A + (A + B)."""
    m = A + B
    r = A + m
    e = ("Step 1, %s: %s + %s = %s. Step 2, both together: %s + %s = <b>%s</b>."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + B + B, add_forgot_one(A, m, "last"), A + A], u, e)


def less_total(q, A, B, u, who2):
    """A + (A − B)."""
    m = A - B
    r = A + m
    e = ("Step 1, %s: %s − %s = %s. Step 2, both together: %s + %s = <b>%s</b>."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + B, A + A + B, add_forgot_one(A, m, "last")], u, e)


def combine_compare(q, B, C, D, u, s1):
    """|(B + C) − D|."""
    t = B + C
    r = abs(t - D)
    big, small = max(t, D), min(t, D)
    e = ("Step 1, %s: %s + %s = %s. Step 2, find the difference: %s − %s = <b>%s</b>."
         % (s1, eu(B, u), eu(C, u), eu(t, u), eu(big, u), eu(small, u), eu(r, u)))
    return story(q, r, [t, sub_small_from_big(big, small), t + D, sub_zero_as_ten(big, small), abs(B - D)], u, e)


def N(n):
    return f(n)


# 2021 Census of Population (Statistics Canada), city populations
POP = {"Vancouver": 662248, "Surrey": 568322, "Burnaby": 249125, "Richmond": 209937, "Kelowna": 144576,
       "Kamloops": 97902, "Nanaimo": 99863, "Prince George": 76708, "Victoria": 91867, "Saanich": 117735}


def set_story(P):
    n = [P.next() for _ in range(3)]
    C = "In the 2021 census, "
    its = [
        one_add(C + "Kelowna had %s people and Kamloops had %s people. How many people lived in the two cities altogether?"
                % (N(POP["Kelowna"]), N(POP["Kamloops"])), POP["Kelowna"], POP["Kamloops"], "people",
                "Altogether means add."),
        one_sub(C + "Nanaimo had %s people and Prince George had %s people. How many more people lived in Nanaimo?"
                % (N(POP["Nanaimo"]), N(POP["Prince George"])), POP["Nanaimo"], POP["Prince George"], "people",
                "How many more means find the difference, so subtract."),
        one_add(C + "Victoria had %s people and its neighbour Saanich had %s people. How many people lived in the two "
                "places altogether?" % (N(POP["Victoria"]), N(POP["Saanich"])), POP["Victoria"], POP["Saanich"], "people",
                "Altogether means add."),
        one_sub(C + "Burnaby had %s people and Richmond had %s people. How many more people lived in Burnaby?"
                % (N(POP["Burnaby"]), N(POP["Richmond"])), POP["Burnaby"], POP["Richmond"], "people",
                "How many more means find the difference, so subtract."),
        one_add(C + "Vancouver had %s people and Burnaby had %s people. How many people lived in the two cities altogether?"
                % (N(POP["Vancouver"]), N(POP["Burnaby"])), POP["Vancouver"], POP["Burnaby"], "people",
                "Altogether means add."),
        one_sub(C + "Vancouver had %s people and Surrey had %s people. How many fewer people lived in Surrey?"
                % (N(POP["Vancouver"]), N(POP["Surrey"])), POP["Vancouver"], POP["Surrey"], "people",
                "How many fewer means find the difference, so subtract."),
        one_sub("When the Dhillon family bought their van, the odometer showed 48" + NB + "579 km. Now it shows "
                "213" + NB + "006 km. How far have they driven the van?", 213006, 48579, "km",
                "Find the distance between the two readings, so subtract."),
        one_add("Before a road trip from Surrey to Prince George and back, the odometer on the Gill family’s car showed "
                "99" + NB + "865 km. The trip was 1586 km. What did the odometer show after the trip?", 99865, 1586, "km",
                "The car drove more kilometres, so add."),
        one_sub("A floatplane company plans to fly 250" + NB + "000 km this year between Vancouver and Vancouver Island. "
                "So far its planes have flown 168" + NB + "475 km. How many kilometres are left?", 250000, 168475, "km",
                "Find the distance still to fly, so subtract."),
        one_add("One BC ferry sailed 48" + NB + "675 km in the spring and 52" + NB + "390 km in the summer. "
                "How far did it sail in the two seasons?", 48675, 52390, "km", "Put the two seasons together, so add."),
        one_add("Volunteers counted 486" + NB + "275 sockeye salmon on the Adams River in one week and 357" + NB + "948 "
                "the next week. How many sockeye did they count in the two weeks?", 486275, 357948, "sockeye",
                "Put the two weeks together, so add."),
        one_sub("Students in a school district set a goal to walk and bike 300" + NB + "000 km to school this year. "
                "So far they have logged 186" + NB + "475 km. How many more kilometres do they need?", 300000, 186475, "km",
                "Find what is still needed, so subtract."),
        start_add("A ski hill had some visits before New Year’s Day. After New Year’s Day it had 186" + NB + "395 more visits. "
                  "The season total was 452" + NB + "080 visits. How many visits were there before New Year’s Day?",
                  452080, 186395, "visits"),
        more_total("A SkyTrain station had 248" + NB + "675 riders in September. In October it had 36" + NB + "480 more "
                   "riders than in September. How many riders did it have in the two months?", 248675, 36480, "riders",
                   "October’s riders"),
        less_total("A hockey arena in Kamloops sold 186" + NB + "425 tickets last season. This season it sold "
                   "24" + NB + "860 fewer. How many tickets did it sell in the two seasons?", 186425, 24860, "tickets",
                   "this season’s tickets"),
        out_then_in("A tree nursery had 450" + NB + "000 cedar seedlings. It sent 286" + NB + "475 to be planted in forests. "
                    "Then it grew 175" + NB + "650 more. How many seedlings does the nursery have now?",
                    450000, 286475, 175650, "seedlings", "after sending some out", "after growing more"),
        both_left("A library system in the Lower Mainland has 750" + NB + "000 books. 286" + NB + "450 books are checked out "
                  "and 48" + NB + "675 are being repaired. How many books are on the shelves?", 750000, 286450, 48675,
                  "books", "books not on the shelves", "books on the shelves"),
        both_left(C + "Vancouver had %s people. Burnaby had %s and Richmond had %s. How many more people lived in Vancouver "
                  "than in Burnaby and Richmond together?" % (N(POP["Vancouver"]), N(POP["Burnaby"]), N(POP["Richmond"])),
                  POP["Vancouver"], POP["Burnaby"], POP["Richmond"], "people", "Burnaby and Richmond together",
                  "the difference"),
        combine_compare(C + "Kamloops had %s people and Nanaimo had %s. Kelowna had %s. How many more people lived in "
                        "Kamloops and Nanaimo together than in Kelowna?"
                        % (N(POP["Kamloops"]), N(POP["Nanaimo"]), N(POP["Kelowna"])),
                        POP["Kamloops"], POP["Nanaimo"], POP["Kelowna"], "people", "Kamloops and Nanaimo together"),
        combine_compare("%s’s family drove 2486 km on a trip to the Okanagan and 1375 km on a trip around Vancouver "
                        "Island. %s’s family drove 5000 km on a summer road trip through Alberta and back. How many "
                        "more kilometres did %s’s family drive?" % (n[0][0], n[1][0], n[1][0]), 2486, 1375, 5000, "km",
                        "%s’s family" % n[0][0]),
    ]
    assert len(its) == 20
    return {"title": "Word problems: BC populations and distances", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    A, B = 458769, 276548
    assert A + B == 735317 and add_carry_cols(A, B) == [0, 1, 2, 3, 4]
    assert add_no_regroup(A, B) == 624207, add_no_regroup(A, B)
    S, T = 600000, 248365
    assert S - T == 351635 and sub_zero_as_ten(S, T) == 362745, sub_zero_as_ten(S, T)
    assert 503214 - 186597 == 316617 and sub_small_from_big(503214, 186597) == 483383
    assert 352846 + 41275 == 394121 and add_misalign(352846, 41275) == 765596
    assert rnd_to(A, 100000) + rnd_to(B, 100000) == 800000
    assert 351635 + 248365 == 600000
    return (
        "<h2>The idea: use place value</h2>"
        "<p>Numbers to " + MILLION + " have hundred thousands, ten thousands, thousands, hundreds, tens and ones. "
        "Add or subtract the <b>same places</b>. When a place gets 10 or more, <b>regroup</b> 10 of them as 1 of the next place.</p>"
        "<p>The method is the same as with smaller numbers. There are just more columns, so line them up carefully.</p>"
        "<h2>Column addition</h2>"
        "<p>Put <b>ones under ones</b>. Start on the right. If a column makes 10 or more, write the ones digit "
        "and regroup 1 into the next column.</p>"
        "<figure class='sn-fig'>" + column_svg(A, B, "+", answer=True, marks=True, fs=30) +
        "<figcaption>Ones: 9 + 8 = 17, write 7, regroup 1. Tens: 6 + 4 + 1 = 11. Hundreds: 7 + 5 + 1 = 13. "
        "Thousands: 8 + 6 + 1 = 15. Ten thousands: 5 + 7 + 1 = 13. Hundred thousands: 4 + 2 + 1 = 7. "
        "Answer: 735" + NB + "317.</figcaption></figure>" +
        ex("Line up the ones", "What is 352" + NB + "846 + 41" + NB + "275?",
           "41" + NB + "275 has only five digits. Its 5 goes under the 6 in the ones column, not under the 3. "
           "352" + NB + "846 + 41" + NB + "275 = 394" + NB + "121.", "394" + NB + "121") +
        "<h2>Subtraction across zeros</h2>"
        "<p>Take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, regroup 1 from the next column. "
        "If the next column is 0, go left to the first digit that is not 0. Every 0 you pass becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + column_svg(S, T, "-", answer=True, marks=True, fs=30) +
        "<figcaption>Ones: 0 − 5, and the next five places are 0. Regroup from the 6 hundred thousands. "
        "600" + NB + "000 becomes 5 hundred thousands, 9 ten thousands, 9 thousands, 9 hundreds, 9 tens and 10 ones. "
        "10 − 5 = 5, 9 − 6 = 3, 9 − 3 = 6, 9 − 8 = 1, 9 − 4 = 5, 5 − 2 = 3. Answer: 351" + NB + "635.</figcaption></figure>"
        "<h2>Estimate first, then check with the inverse</h2>"
        "<p>Before you start, <b>estimate</b>. Round each number and work it out in your head. "
        "For 458" + NB + "769 + 276" + NB + "548, 500" + NB + "000 + 300" + NB + "000 = 800" + NB + "000, "
        "so the answer should be close to 800" + NB + "000.</p>"
        "<p>When you finish, <b>check with the inverse</b>. Addition and subtraction undo each other. "
        "To check 600" + NB + "000 − 248" + NB + "365 = 351" + NB + "635, add: 351" + NB + "635 + 248" + NB + "365 = "
        "600" + NB + "000. You get back to the start, so the answer is right.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the numbers on the left (352" + NB + "846 + 41" + NB + "275 = 765" + NB + "596)",
             "Line up the ones on the right: 352" + NB + "846 + 41" + NB + "275 = 394" + NB + "121"],
            ["Not regrouping (458" + NB + "769 + 276" + NB + "548 = 624" + NB + "207)",
             "Write the regrouped 1 under the next column and add it in"],
            ["Taking the smaller digit from the larger one (503" + NB + "214 − 186" + NB + "597 = 483" + NB + "383)",
             "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Making each 0 into 10 instead of 9 (600" + NB + "000 − 248" + NB + "365 = 362" + NB + "745)",
             "Only the ones get 10. Each 0 you pass gives 1 away, so it becomes 9"],
        ])
    )


FAQ = [
    {"q": "What does Grade 5 learn about adding and subtracting in the BC math curriculum?",
     "a": "Under Computational fluency, Grade 5 students add and subtract whole numbers to 1 000 000. They use the column "
          "method with regrouping, estimate first and check their answers with the inverse."},
    {"q": "How do you subtract across zeros, like 600 000 − 248 365?",
     "a": "Go left to the first digit that is not 0 and regroup from there; each 0 you pass becomes 9. "
          "600 000 becomes 5 hundred thousands, 9 ten thousands, 9 thousands, 9 hundreds, 9 tens and 10 ones, "
          "so 600 000 − 248 365 = 351 635."},
    {"q": "Why should students estimate before adding or subtracting large numbers?",
     "a": "An estimate shows about how big the answer should be. If the exact answer is far from the estimate, "
          "a column was misaligned or a regrouping was missed."},
    {"q": "How do you check a subtraction answer with the inverse?",
     "a": "Add the answer to the number you took away. For 600 000 − 248 365 = 351 635, "
          "351 635 + 248 365 = 600 000, so the answer is right."},
]
for _q in FAQ:
    _q["q"] = re.sub(r"(\d) (\d{3})", "\\1" + NB + "\\2", re.sub(r"(\d) (\d{3})", "\\1" + NB + "\\2", _q["q"]))
    _q["a"] = re.sub(r"(\d) (\d{3})", "\\1" + NB + "\\2", re.sub(r"(\d) (\d{3})", "\\1" + NB + "\\2", _q["a"]))


def verify(sets):
    """Recompute every plain calculation answer from the question."""
    Nre = r"(\d+(?:" + NB + r"\d{3})*)"
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='" + Nre + " (plus|minus) " + Nre + " written in columns'", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"What is " + Nre + " ([+−]) " + Nre + r"\?$", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "+" else a - b), it["q"]


def gen():
    rnd = random.Random(55805)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_add(rnd, seen_a), set_sub(rnd, seen_s), set_estimate(rnd, P), set_inverse(rnd, P), set_story(P)]
    balance(sets, rnd)
    verify(sets)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "adding-and-subtracting-whole-numbers", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting Whole Numbers to " + MILLION,
        "seo_title": "Grade 5 Adding and Subtracting Whole Numbers Worksheets: Large Numbers and Regrouping (BC)",
        "short_title": "Adding and subtracting whole numbers",
        "domain": "Computational fluency",
        "standard_code": "Grade 5: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Addition and subtraction of whole numbers to 1" + NB + "000" + NB + "000",
        "meta_desc": "Free Grade 5 math worksheets on adding and subtracting whole numbers to " + MILLION + ", matched to the "
                     "BC curriculum: column addition, subtracting across zeros, estimating first, checking with the inverse "
                     "and BC word problems. 100 questions with an answer key.",
        "key_big": "Line up the ones. Regroup when you need to. Check with the inverse.",
        "key_sub": "Estimate before you start. In columns, start on the right; every 0 you regroup across becomes 9. "
                   "Then add back what you took away to check.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
