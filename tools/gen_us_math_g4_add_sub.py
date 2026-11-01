# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Add and Subtract Multi-Digit Whole Numbers (4.NBT.B.4)
  python tools/gen_us_math_g4_add_sub.py
HTML attributes use single quotes (no backslashes in the JSON).
Numbers of 1,000 or more are written with commas (also in the column pictures).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
ONE = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand", "million"]


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
        lead = lead.lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead in ("0", ""):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def and_list(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------ column picture
def borrow_digits(a, b):
    """Top digits after all the regrouping of the standard algorithm (ones first)."""
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


def vertical_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line. Commas sit in their own narrow slot.
    answer: also write the answer.  marks: small red regroup marks (carried 1s, or new top digits)."""
    cw, kw = fs * (0.82 if marks else 0.62), fs * 0.32
    res = a + b if op == "+" else a - b
    rows = [f(a), f(b)] + ([f(res)] if answer else [])
    width_chars = max(len(r) for r in rows)
    k = max(nlen(a), nlen(b), nlen(res) if answer else 0)

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
    top = 10 + (int(fs * 0.62) if marks else 0)
    s = []

    def put(text, y, color, size=fs):
        cx, _ = xs(text)
        for ch, x in zip(text, cx):
            if ch == ",":
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                         "font-family='monospace'>,</text>" % (right - x, y, size, color))
            else:
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                         "font-family='monospace'>%s</text>" % (right - x, y, size, color, ch))
        return cx

    y1, y2 = top + fs, top + int(fs * 2.15)
    cx_a = put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    # x of each place (ones first) from the top row
    place_x = [right - x for ch, x in zip(reversed(rows[0]), reversed(cx_a)) if ch != ","]
    sign_x = right - longest - cw * 0.9
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, y2, fs, GREEN, "+" if op == "+" else "−"))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.6, ly, right, ly, INK))
    H = ly + 10
    if answer:
        put(rows[2], ly + fs + 6, GREEN)
        H = ly + fs + 16
    if marks:
        sm = int(fs * 0.55)
        if op == "+":
            ka = nlen(a)
            da, db = digits(a, ka + 1), digits(b, ka + 1)
            c = 0
            for i in range(max(nlen(a), nlen(b)) - 1):
                c = 1 if da[i] + db[i] + c >= 10 else 0
                if c and i + 1 < len(place_x):
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                             % (place_x[i + 1], top - 4, sm, RED))
        else:
            nd = borrow_digits(a, b)
            od = digits(a, nlen(a))
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%s %s %s written in columns" % (f(a), "plus" if op == "+" else "minus", f(b))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ the methods, step by step
def add_steps(a, b, compact=None):
    k = max(nlen(a), nlen(b))
    if compact is None:
        compact = k >= 5
    da, db = digits(a, k), digits(b, k)
    kb = min(nlen(a), nlen(b))
    carry, parts, regs = 0, [], []
    for i in range(k):
        t = da[i] + db[i] + carry
        if i >= kb:
            big = da[i] if nlen(a) > nlen(b) else db[i]
            expr = "%d + 1" % big if carry else None
        else:
            expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        P = cap(PLACE[i])
        if t >= 10 and i == k - 1:
            msg = "%s: %s = %d, write %d." % (P, expr, t, t)
            parts.append(msg)
            regs.append(msg)
            carry = 0
        elif t >= 10:
            msg = "%s: %s = %d, write %d and regroup 1 %s." % (P, expr, t, t % 10, ONE[i + 1])
            parts.append(msg)
            regs.append(msg)
            carry = 1
        else:
            parts.append("%s: bring down %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    s = a + b
    end = " Answer: %s. Check: %s − %s = %s." % (f(s), f(s), f(b), f(a))
    if not compact:
        return "Line up the places and start with the ones. " + " ".join(parts) + end
    if not regs:
        return "No column makes 10 or more, so add each place. " + end.strip()
    rest = " The other places add without regrouping." if len(regs) < k else ""
    return "Line up the places and start with the ones. " + " ".join(regs) + rest + end


def sub_steps(a, b, compact=None):
    k = nlen(a)
    if compact is None:
        compact = k >= 5
    d, db = digits(a, k), digits(b, k)
    kb = nlen(b)
    parts, regs = [], []
    for i in range(k):
        P = cap(PLACE[i])
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                zeros = and_list(["0 %s" % PLACE[m] for m in range(i + 1, j)])
                old = d[j]
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d needs a regroup, but there are %s. Regroup across the zeros: %d %s %s %d, "
                       "each 0 becomes 9, and the %s become %d. %d − %d = %d."
                       % (P, cur, db[i], zeros, old, PLACE[j] if old != 1 else ONE[j], "become" if old != 1 else "becomes",
                          d[j], PLACE[i], d[i], d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d needs a regroup. 1 %s becomes 10 %s: %d − %d = %d."
                       % (P, cur, db[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
            parts.append(msg)
            regs.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                parts.append("%s: bring down %d." % (P, d[i]))
        else:
            parts.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    end = " Answer: %s. Check: %s + %s = %s." % (f(r), f(r), f(b), f(a))
    if not compact:
        return "Line up the places and start with the ones. " + " ".join(parts) + end
    rest = " The other places subtract without regrouping." if len(regs) < k else ""
    return "Line up the places and start with the ones. " + " ".join(regs) + rest + end


# ------------------------------------------------------------ typical mistakes
def add_no_carry(a, b):
    """Never adds the regrouped 1 (writes the full sum only in the last column)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    return sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))


def add_carry_cols(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    c, cols = 0, []
    for i in range(k - 1):
        c = 1 if da[i] + db[i] + c >= 10 else 0
        if c:
            cols.append(i)
    return cols


def add_forgot_one(a, b, which):
    """Forgot just one regrouped 1 (the first or the last one)."""
    cols = add_carry_cols(a, b)
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return a + b - 10 ** (i + 1)


def add_misalign(a, b):
    """Lined up the shorter number one place too far left."""
    if nlen(a) == nlen(b):
        return None
    big, small = max(a, b), min(a, b)
    return big + small * 10


def add_extra_one(a, b):
    """Added a regrouped 1 to a column that did not get one (one answer for each such column)."""
    cols = set(add_carry_cols(a, b))
    k = max(nlen(a), nlen(b))
    return [a + b + 10 ** (i + 1) for i in range(k - 1) if i not in cols]


def regroups_add(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    c, n = 0, 0
    for i in range(k):
        t = da[i] + db[i] + c
        c = 1 if t >= 10 else 0
        n += c
    return n


def sub_small_from_big(a, b):
    """Took the smaller digit from the bigger one in every column."""
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))


def sub_forgot_reduce(a, b, only_first=False):
    """Regrouped (made 10 more) but did not take 1 away from the next place."""
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


def sub_misalign(a, b):
    if nlen(a) == nlen(b):
        return None
    return a - b * 10


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
    """True if some regroup has to cross a 0."""
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
    s = a + b
    return clean([add_no_carry(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b)] + add_extra_one(a, b) + [abs(a - b)])


def sub_cands(a, b):
    return clean([sub_small_from_big(a, b), sub_zero_as_ten(a, b), sub_forgot_reduce(a, b),
                  sub_forgot_reduce(a, b, only_first=True), sub_misalign(a, b), a + b])


def item_add(a, b, rnd, col):
    q = (fig(vertical_svg(a, b, "+")) + "Add.") if col else "What is %s + %s?" % (f(a), f(b))
    return mcq(q, f(a + b), [f(v) for v in add_cands(a, b)], add_steps(a, b), rnd)


def item_sub(a, b, rnd, col):
    q = (fig(vertical_svg(a, b, "-")) + "Subtract.") if col else "What is %s − %s?" % (f(a), f(b))
    return mcq(q, f(a - b), [f(v) for v in sub_cands(a, b)], sub_steps(a, b), rnd)


# ------------------------------------------------------------ sets
def pick_add(rnd, seen, la, lb, want, top=999999):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 5, 10 ** la - 10 ** (la - 1) // 2)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 5, 10 ** lb - 10 ** (lb - 1) // 2)
        if a + b > top or (a, b) in seen or (b, a) in seen or a % 10 == 0 or b % 10 == 0:
            continue
        if regroups_add(a, b) in want:
            seen.add((a, b))
            return a, b


def set_add4(rnd, seen):
    its = []
    plan = [(1,)] * 6 + [(2,)] * 7 + [(3,)] * 4 + [(4,)] * 3          # number of regroups
    for i, want in enumerate(plan):
        if i in (5, 12):                                             # 4-digit + 3-digit
            a, b = pick_add(rnd, seen, 4, 3, want, top=9999)
        else:
            a, b = pick_add(rnd, seen, 4, 4, want, top=9999 if want[0] < 4 else 19999)
        its.append(item_add(a, b, rnd, i % 2 == 0))
    return {"title": "Add 4-digit numbers", "items": its}


def set_add56(rnd, seen):
    its = []
    for i in range(6):
        a, b = pick_add(rnd, seen, 5, 5, (2, 3, 4), top=99999 if i < 3 else 199999)
        its.append(item_add(a, b, rnd, True))
    for i in range(6):
        a, b = pick_add(rnd, seen, 6, 6, (2, 3, 4))
        its.append(item_add(a, b, rnd, True))
    for i in range(3):
        a, b = pick_add(rnd, seen, 6, 5, (2, 3))
        its.append(item_add(a, b, rnd, False))
    for i in range(3):
        a, b = pick_add(rnd, seen, 5, 4, (2, 3))
        its.append(item_add(a, b, rnd, False))
    a = 63482
    its.append(item_add(a, 100000 - a, rnd, True))                  # makes exactly 100,000
    a = 637425
    its.append(item_add(a, 1000000 - a, rnd, False))                # makes exactly 1,000,000
    rnd.shuffle(its)
    return {"title": "Add 5- and 6-digit numbers", "items": its}


def pick_sub(rnd, seen, la, lb, want):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 2, 10 ** la - 1)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 10, min(10 ** lb - 1, a - 10 ** (la - 1) // 4))
        if (a, b) in seen or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if regroups_sub(a, b) == want:
            seen.add((a, b))
            return a, b


def set_sub4(rnd, seen):
    its = []
    plan = [1] * 6 + [2] * 8 + [3] * 6
    for i, want in enumerate(plan):
        lb = 3 if i in (4, 11) else 4
        a, b = pick_sub(rnd, seen, 4, lb, want)
        its.append(item_sub(a, b, rnd, i % 2 == 0))
    return {"title": "Subtract 4-digit numbers", "items": its}


def set_zeros(rnd, seen):
    its = []
    tops = [10000, 40005]                                            # the classic ones are in the lesson / first
    pairs = [(10000, 3467)]
    # patterns: digits of the top number, x = any digit 1-9, 0 = zero
    pats = ["x000", "x00x", "x0x0", "x0,000", "x0,00x", "x0,0x0", "x0,x00", "xx,00x", "x0,0xx",
            "x00,000", "x00,00x", "xx0,00x", "x0x,0x0", "x00,x0x", "xx,000", "x00x", "x0,000", "x00,000", "x0,00x"]
    for p in pats:
        while True:
            t = "".join(str(rnd.randint(1, 9)) if ch == "x" else ch for ch in p.replace(",", ""))
            a = int(t)
            la = nlen(a)
            lb = la if rnd.random() < 0.7 else la - 1
            lo = 10 ** (lb - 1) + 10 ** (lb - 1) // 10
            hi = min(10 ** lb - 1, a - 10 ** (la - 1) // 5)
            if hi <= lo:
                continue
            b = rnd.randint(lo, hi)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or regroups_sub(a, b) < 2:
                continue
            tops.append(a)
            seen.add((a, b))
            pairs.append((a, b))
            break
    for i, (a, b) in enumerate(pairs):
        its.append(item_sub(a, b, rnd, i % 2 == 0))
    rnd.shuffle(its)
    return {"title": "Subtract across zeros", "items": its}


# ------------------------------------------------------------ word problems
def unit_c(vals, unit):
    return ["%s %s" % (f(v), unit) for v in vals]


def money_c(vals):
    return ["$%s" % f(v) for v in vals]


def story_add(q, a, b, unit, rnd, lead):
    s = a + b
    c = add_cands(a, b) + [abs(a - b)]
    return mcq(q, "%s %s" % (f(s), unit), unit_c(c, unit), lead + " " + add_steps(a, b), rnd)


def story_sub(q, a, b, unit, rnd, lead, money=False):
    r = a - b
    c = sub_cands(a, b)
    if money:
        return mcq(q, "$%s" % f(r), money_c(c), lead + " " + sub_steps(a, b), rnd)
    return mcq(q, "%s %s" % (f(r), unit), unit_c(c, unit), lead + " " + sub_steps(a, b), rnd)


def set_story(rnd):
    P = People(rnd)
    its = []
    # one-step stories
    its.append(story_sub("A stadium has 68,450 seats. At a football game, 52,786 seats were filled. How many seats were empty?",
                         68450, 52786, "seats", rnd, "Take the filled seats away from all the seats: subtract."))
    n, he, his = P.next()
    its.append(story_add("A pilot named %s flew 23,684 miles in May and 19,857 miles in June. How many miles did %s fly in the two months?" % (n, he),
                         23684, 19857, "miles", rnd, "Put the two distances together: add."))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    its.append(story_sub("In a video game, %s scored 145,860 points and %s scored 98,975 points. How many more points did %s score than %s?"
                         % (n1, n2, n1, n2), 145860, 98975, "points", rnd, "How many more means find the difference: subtract."))
    its.append(story_add("The town of Cedar Falls had 48,307 people. Over ten years, 6,895 more people moved there. "
                         "How many people live in Cedar Falls now?", 48307, 6895, "people", rnd,
                         "The town got bigger: add."))
    its.append(story_sub("A city library has 120,000 books. 34,586 books are checked out. How many books are still in the library?",
                         120000, 34586, "books", rnd, "Take the checked-out books away: subtract."))
    its.append(story_sub("Mount Everest is 29,032 feet tall. Mount Whitney is 14,505 feet tall. How much taller is Mount Everest?",
                         29032, 14505, "feet", rnd, "How much taller means find the difference: subtract."))
    its.append(story_sub("A school wants to raise $20,000 for a new playground. So far it has raised $12,450. How much more money does it need?",
                         20000, 12450, "", rnd, "Find what is missing from the goal: subtract.", money=True))
    its.append(story_add("An airport had 186,394 passengers in June and 207,758 passengers in July. How many passengers did it have in the two months?",
                         186394, 207758, "passengers", rnd, "Put the two months together: add."))
    # two-step stories
    a, b, c = 9500, 3486, 4275
    its.append(mcq("A theater has 9,500 tickets to sell for a show. It sold 3,486 tickets on Friday and 4,275 tickets on Saturday. "
                   "How many tickets are left?", "%s tickets" % f(a - b - c),
                   unit_c([b + c, a - b, a - c, sub_small_from_big(a, b + c)], "tickets"),
                   "Step 1, tickets sold: 3,486 + 4,275 = 7,761. Step 2, tickets left: 9,500 − 7,761 = 1,739. "
                   "Check: 1,739 + 7,761 = 9,500.", rnd))
    a, b, c = 25640, 8975, 6380
    its.append(mcq("An orchard had 25,640 apples in storage. It sold 8,975 apples and then picked 6,380 more. "
                   "How many apples are in storage now?", "%s apples" % f(a - b + c),
                   unit_c([a - b, a - b - c, a + b + c, a - b + c - 10000], "apples"),
                   "Step 1, after selling: 25,640 − 8,975 = 16,665. Step 2, after picking: 16,665 + 6,380 = 23,045. "
                   "Check with estimates: 26,000 − 9,000 + 6,000 = 23,000.", rnd))
    a, b = 14268, 2795
    its.append(mcq("A factory made 14,268 toy cars on Monday. On Tuesday, it made 2,795 more toy cars than on Monday. "
                   "How many toy cars did it make on both days?", "%s toy cars" % f(a + a + b),
                   unit_c([a + b, a + (a - b), 2 * a, a + b + b], "toy cars"),
                   "Step 1, Tuesday: 14,268 + 2,795 = 17,063. Step 2, both days: 14,268 + 17,063 = 31,331.", rnd))
    a, b, c = 3500, 1248, 986
    n, he, his = P.next()
    its.append(mcq("%s's family is driving 3,500 miles across the country. They drove 1,248 miles in the first week and 986 miles in the second week. "
                   "How many miles are left?" % n, "%s miles" % f(a - b - c),
                   unit_c([b + c, a - b, a - c, a - b + c], "miles"),
                   "Step 1, miles driven: 1,248 + 986 = 2,234. Step 2, miles left: 3,500 − 2,234 = 1,266. Check: 1,266 + 2,234 = 3,500.", rnd))
    # missing numbers
    x, b = 35729, 27486
    s = x + b
    its.append(mcq("What number goes in the box?  <b>☐ + %s = %s</b>" % (f(b), f(s)), f(x),
                   [f(v) for v in [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b)]],
                   "Use subtraction: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(b), f(x), f(x), f(b), f(s)), rnd))
    a, r = 82040, 35678
    x = a - r
    its.append(mcq("What number goes in the box?  <b>%s − ☐ = %s</b>" % (f(a), f(r)), f(x),
                   [f(v) for v in [a + r, sub_small_from_big(a, r), sub_zero_as_ten(a, r)]],
                   "Think: %s − ? = %s. The missing part is %s − %s = %s. Check: %s − %s = %s."
                   % (f(a), f(r), f(a), f(r), f(x), f(a), f(x), f(r)), rnd))
    r, b = 48726, 15394
    x = r + b
    its.append(mcq("What number goes in the box?  <b>☐ − %s = %s</b>" % (f(b), f(r)), f(x),
                   [f(v) for v in [r - b, add_no_carry(r, b), add_forgot_one(r, b, "last")]],
                   "The box is the starting number, so add: %s + %s = %s. Check: %s − %s = %s."
                   % (f(r), f(b), f(x), f(x), f(b), f(r)), rnd))
    a, s = 245318, 600000
    x = s - a
    its.append(mcq("What number goes in the box?  <b>%s + ☐ = %s</b>" % (f(a), f(s)), f(x),
                   [f(v) for v in [sub_small_from_big(s, a), sub_zero_as_ten(s, a), s + a]],
                   "Use subtraction: %s − %s. " % (f(s), f(a)) + sub_steps(s, a), rnd))
    # estimate to check (nearest thousand)
    for a, b, op in [(34682, 18415, "+"), (72309, 28746, "−")]:
        ra, rb = round(a, -3), round(b, -3)
        est = ra + rb if op == "+" else ra - rb
        exact = a + b if op == "+" else a - b
        trunc = (a // 1000 * 1000) + (b // 1000 * 1000) if op == "+" else (a // 1000 * 1000) - (b // 1000 * 1000)
        tth = round(a, -4) + round(b, -4) if op == "+" else round(a, -4) - round(b, -4)
        other = ra - rb if op == "+" else ra + rb
        assert est not in (trunc, tth)
        its.append(mcq("Round each number to the nearest thousand. Which is the best estimate for %s %s %s?" % (f(a), op, f(b)),
                       "about %s" % f(est), ["about %s" % f(v) for v in [trunc, tth, other]],
                       "%s rounds to %s and %s rounds to %s. %s %s %s = %s. The exact answer, %s, is close to %s."
                       % (f(a), f(ra), f(b), f(rb), f(ra), op, f(rb), f(est), f(exact), f(est)), rnd))
    n, he, his = P.next()
    a, b = 46215, 27890
    wrong = add_forgot_one(a, b, "last")
    est = round(a, -3) + round(b, -3)
    assert wrong == 64105 and est == 74000
    its.append(mcq("%s added %s + %s and got %s. Round each number to the nearest thousand to check. What does the estimate show?"
                   % (n, f(a), f(b), f(wrong)), "Too small by about 10,000",
                   ["The answer is reasonable", "Too big by about 10,000", "Too small by about 1,000"],
                   "Estimate: 46,000 + 28,000 = 74,000, but %s's answer is about 64,000, so it is about 10,000 too small. "
                   "%s forgot the regrouped 1 in the ten thousands. The correct sum is %s." % (n, cap(he), f(a + b)), rnd))
    n, he, his = P.next()
    a, b = 83104, 37658
    wrong = sub_small_from_big(a, b)
    est = round(a, -3) - round(b, -3)
    assert est == 45000 and 9000 < wrong - (a - b) < 11000, (wrong, a - b)
    its.append(mcq("%s subtracted %s − %s and got %s. Round each number to the nearest thousand to check. What does the estimate show?"
                   % (n, f(a), f(b), f(wrong)), "Too big by about 10,000",
                   ["The answer is reasonable", "Too small by about 10,000", "Too big by about 1,000"],
                   "Estimate: 83,000 − 38,000 = 45,000, but %s's answer is about 55,000, so it is about 10,000 too big. "
                   "%s took the smaller digit from the bigger one instead of regrouping. The correct difference is %s."
                   % (n, cap(he), f(a - b)), rnd))
    rnd.shuffle(its)
    return {"title": "Word problems, missing numbers and estimates", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    A1, B1 = 45867, 38596
    A2, B2 = 7352, 2874
    A3, B3 = 40005, 12768
    assert A1 + B1 == 84463 and A2 - B2 == 4478 and A3 - B3 == 27237
    assert add_no_carry(A1, B1) == 73353 and sub_small_from_big(A2, B2) == 5522 and sub_forgot_reduce(A2, B2) == 5588
    return (
        "<h2>The idea: line up the places</h2>"
        "<p>Big numbers work just like small ones. Write them in columns so <b>ones are under ones</b>, tens under tens, "
        "and so on up to the hundred thousands. Then work one place at a time, starting with the <b>ones</b> on the right.</p>"
        "<p>When a column adds up to 10 or more, write the ones digit and <b>regroup 1</b> to the next place on the left.</p>"
        "<figure class='sn-fig'>" + vertical_svg(A1, B1, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 + 6 = 13, write 3 and regroup 1 ten. Tens: 6 + 9 + 1 = 16, write 6 and regroup 1 hundred. "
        "Hundreds: 8 + 5 + 1 = 14, write 4 and regroup 1 thousand. Thousands: 5 + 8 + 1 = 14, write 4 and regroup 1 ten thousand. "
        "Ten thousands: 4 + 3 + 1 = 8. Answer: 84,463.</figcaption></figure>"
        "<h2>Subtract with regrouping</h2>"
        "<p>If the top digit is smaller than the bottom digit, <b>regroup</b>: take 1 from the next place on the left "
        "and make 10 more in this place. Cross out the old digit and write the new one above it.</p>"
        "<figure class='sn-fig'>" + vertical_svg(A2, B2, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 4 needs a regroup, so 12 − 4 = 8. Tens: now 4 − 7 needs a regroup, so 14 − 7 = 7. "
        "Hundreds: now 2 − 8 needs a regroup, so 12 − 8 = 4. Thousands: 6 − 2 = 4. Answer: 4,478.</figcaption></figure>"
        "<h2>Subtract across zeros</h2>"
        "<p>When the next place is 0, there is nothing to take. Keep moving left to the first digit that is not 0. "
        "Take 1 from it. Every 0 you passed becomes <b>9</b>, and the column you started in gets 10 more.</p>"
        "<figure class='sn-fig'>" + vertical_svg(A3, B3, "-", answer=True, marks=True, fs=34) +
        "<figcaption>40,005 is 4 ten thousands and 5 ones. Regroup 1 ten thousand: 3 ten thousands, 9 thousands, 9 hundreds, "
        "9 tens and 15 ones. Now subtract: 15 − 8 = 7, 9 − 6 = 3, 9 − 7 = 2, 9 − 2 = 7, 3 − 1 = 2. Answer: 27,237.</figcaption></figure>" +
        ex("Subtract across zeros", "What is 10,000 − 3,467?",
           "Regroup 1 ten thousand: 9 thousands, 9 hundreds, 9 tens and 10 ones. "
           "Ones: 10 − 7 = 3. Tens: 9 − 6 = 3. Hundreds: 9 − 4 = 5. Thousands: 9 − 3 = 6.", "6,533") +
        "<h2>Check your answer</h2>"
        "<p><b>Add back.</b> Addition and subtraction undo each other. Add your answer to the number you took away: "
        "27,237 + 12,768 = 40,005, so the subtraction is right.</p>"
        "<p><b>Estimate.</b> Round each number to the nearest thousand and do the easy problem. "
        "45,867 + 38,596 is about 46,000 + 39,000 = 85,000, so 84,463 makes sense. An answer like 73,353 is too far away.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the regrouped 1 (45,867 + 38,596 = 73,353)", "Write a small 1 above the next column and add it in"],
            ["Taking the smaller digit from the bigger one (7,352 − 2,874 = 5,522)", "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Regrouping but not crossing out (7,352 − 2,874 = 5,588)", "When you take 1 from a place, that digit gets 1 smaller"],
            ["Changing zeros to 10 instead of 9 (10,000 − 3,467 = 7,643)", "Each 0 you pass gives 1 to the right, so it becomes 9"],
            ["Lining up the numbers on the left (48,307 + 6,895)", "Line up the ones on the right. Commas line up too"],
        ])
    )


FAQ = [
    {"q": "What is the standard algorithm for addition and subtraction?",
     "a": "It is the column method: line up the numbers by place value, start with the ones, and regroup when a column needs it. Grade 4 students use it with numbers up to 1,000,000."},
    {"q": "How do you subtract across zeros, like 40,005 − 12,768?",
     "a": "Go left to the first digit that is not 0 and take 1 from it. Every 0 you pass becomes 9 and the ones get 10 more, so 40,005 becomes 3 ten thousands, 9 thousands, 9 hundreds, 9 tens and 15 ones. Then subtract each place to get 27,237."},
    {"q": "How can my child check a multi-digit subtraction answer?",
     "a": "Add the answer to the number that was subtracted. If you get the starting number, the answer is right: 27,237 + 12,768 = 40,005. A quick estimate, like 40,000 − 13,000 = 27,000, also catches big mistakes."},
    {"q": "What does 4.NBT.B.4 mean?",
     "a": "It is the Common Core standard for Grade 4: fluently add and subtract multi-digit whole numbers using the standard algorithm. In Grade 4 the numbers go up to 1,000,000."},
]


def gen_add_sub():
    rnd = random.Random(109)
    seen_a, seen_s = set(), set()
    sets = [set_add4(rnd, seen_a), set_add56(rnd, seen_a), set_sub4(rnd, seen_s), set_zeros(rnd, seen_s), set_story(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "add-subtract-multi-digit", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Multi-Digit Numbers",
        "seo_title": "Grade 4 Multi-Digit Addition and Subtraction Worksheets: Regrouping, Subtracting Across Zeros and Word Problems",
        "short_title": "Add and subtract multi-digit numbers",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "4.NBT.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NBT/B/4/",
        "standard_text": "Fluently add and subtract multi-digit whole numbers using the standard algorithm.",
        "meta_desc": "Free Grade 4 worksheets for adding and subtracting 4-, 5- and 6-digit numbers with the standard algorithm: regrouping, subtracting across zeros, missing numbers, estimating to check and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Line up the places. Start with the ones. Regroup when you need to.",
        "key_sub": "Adding: a column of 10 or more sends 1 to the next place. Subtracting: if the top digit is smaller, take 1 from the next place, and zeros you pass become 9. Check by adding back or estimating.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_add_sub()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
