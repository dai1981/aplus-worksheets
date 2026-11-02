# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Add and Subtract Within 100 (2.NBT.B.5-6)
  python tools/gen_us_math_g2_add_sub_100.py
All numbers are 2-digit (sums and starting numbers up to 100). Every answer is computed in code.
Wrong answers come from real Grade 2 mistakes (forgetting the regrouped ten, subtracting the smaller
digit from the bigger one, regrouping without crossing out, mixing tens and ones, missing a number).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def pl(n, word):
    return "%d %s" % (n, word if n == 1 else word + "s")


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, lg=False):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, fam=None):
    f = " font-family='%s'" % fam if fam else ""
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, col, anchor, f, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (base-ten blocks) so every block can be counted."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
CELL = 11          # one unit cube; a ten rod is 10 cubes tall


def blocks_group(x0, base, n_tens, n_ones):
    """Draw tens rods and ones cubes standing on the line y = base. Returns (svg, width)."""
    s = []
    x = x0
    for _ in range(n_tens):
        top = base - 10 * CELL
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x, top, CELL, 10 * CELL, FILL, GREEN))
        for k in range(1, 10):
            y = top + k * CELL
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y, x + CELL, y, GREEN))
        x += CELL + 5
    if n_tens and n_ones:
        x += 6
    cols = (n_ones + 4) // 5
    for c in range(cols):
        for r in range(min(5, n_ones - 5 * c)):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x, base - (r + 1) * (CELL + 3) + 3, CELL, CELL, FILL, GREEN))
        x += CELL + 4
    return "".join(s), x - x0 - (4 if cols else 5)


def blocks_svg(groups, labels=True):
    """groups: list of (tens, ones). Two groups are joined with a + sign."""
    o, top = 8, 8
    base = top + 10 * CELL
    H = base + (30 if labels else 8)
    body, x = [], o
    for gi, (t, n) in enumerate(groups):
        if gi:
            body.append(text(x + 16, base - 5 * CELL + 10, "+", 30, col=GREEN))
            x += 32
        g, w = blocks_group(x, base, t, n)
        body.append(g)
        if labels:
            body.append(text(x + w / 2, base + 22, str(10 * t + n), 18))
        x += w
    W = x + o
    what = " plus ".join("%s and %s" % (pl(t, "ten"), pl(n, "one")) for t, n in groups)
    return svg_wrap(W, H, "".join(body), "base-ten blocks: " + what)


def digits(n, k=3):
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def column_svg(nums, op, big=False, marks=False):
    """Numbers in columns (ones under ones), sign and line, ready to solve.
    marks=True (lesson only) adds the regrouping marks in red."""
    fs = 34 if big else 28
    cw = fs * (0.9 if marks else 0.64)
    pad = 22 if marks else 6
    W = int(cw * 4 + 22)
    rows = len(nums)
    H = int(pad + fs * rows + 22)
    right = W - 10
    s = []

    def cx(i):                       # centre of column i (0 = ones)
        return right - cw * (i + 0.5)

    for row, n in enumerate(nums):
        y = pad + fs * (row + 1) - 4
        for i, ch in enumerate(reversed(str(n))):
            s.append(text(cx(i), y, ch, fs, col=INK, fam="monospace"))
    s.append(text(right - cw * 3.4, pad + fs * rows - 4, "+" if op == "+" else "−", fs, col=GREEN))
    ly = pad + fs * rows + 8
    s.append("<line x1='%.0f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
             % (right - cw * 3.9, ly, right, ly, INK))
    if marks and op == "+":
        carry = sum(digits(n)[0] for n in nums) // 10
        if carry:
            s.append(text(cx(1), pad - 4, str(carry), 18, col=RED))
    if marks and op == "-":
        a, b = nums
        da = digits(a)
        if da[0] < digits(b)[0]:
            y0 = pad + fs - 4
            s.append("<line x1='%.0f' y1='%.0f' x2='%.0f' y2='%.0f' stroke='%s' stroke-width='2.5'/>"
                     % (cx(1) - cw * 0.3, y0 + 2, cx(1) + cw * 0.28, y0 - fs * 0.68, RED))
            s.append(text(cx(1), pad - 4, str(da[1] - 1), 18, col=RED))
            s.append(text(cx(0) - cw * 0.34, pad + fs * 0.4, "1", 16, col=RED))
    word = "plus" if op == "+" else "minus"
    return svg_wrap(W, H, "".join(s), (" %s " % word).join(str(n) for n in nums) + " written in columns")


# ------------------------------------------------------------ the methods, step by step
def add_steps(nums):
    ones = [n % 10 for n in nums]
    tens = [n // 10 for n in nums]
    os_ = sum(ones)
    carry = os_ // 10
    t = sum(tens) + carry
    parts = []
    if carry:
        parts.append("Ones: %s = %d. Write %d and regroup %s." % (" + ".join(map(str, ones)), os_, os_ % 10, pl(carry, "ten")))
        if len(nums) == 2:
            parts.append("Tens: %s + %d = %d." % (" + ".join(map(str, tens)), carry, t))
        else:
            parts.append("Tens: %s = %d, plus the regrouped %s = %d."
                         % (" + ".join(map(str, tens)), sum(tens), pl(carry, "ten"), t))
    else:
        parts.append("Ones: %s = %d." % (" + ".join(map(str, ones)), os_))
        parts.append("Tens: %s = %d." % (" + ".join(map(str, tens)), t))
    if t == 10:
        parts.append("10 tens make 100.")
    return " ".join(parts) + " Answer: %d." % sum(nums)


def sub_steps(a, b, check=True):
    a1, a10 = a % 10, a // 10
    b1, b10 = b % 10, b // 10
    if a == 100:
        s = ("100 is 10 tens. Trade 1 ten for 10 ones: now 9 tens and 10 ones. Ones: 10 − %d = %d. Tens: 9 − %d = %d."
             % (b1, 10 - b1, b10, 9 - b10))
    elif a1 < b1:
        s = ("Ones: %d − %d needs a regroup. Trade 1 ten for 10 ones: %d − %d = %d. Tens: %d − %d = %d."
             % (a1, b1, a1 + 10, b1, a1 + 10 - b1, a10 - 1, b10, a10 - 1 - b10))
    else:
        s = "Ones: %d − %d = %d. Tens: %d − %d = %d." % (a1, b1, a1 - b1, a10, b10, a10 - b10)
    s += " Answer: %d." % (a - b)
    if check:
        s += " Check: %d + %d = %d." % (a - b, b, a)
    return s


# ------------------------------------------------------------ typical mistakes
def add_no_carry(nums):
    """Forgot the regrouped ten."""
    return sum(nums) - 10 * (sum(n % 10 for n in nums) // 10)


def add_concat(a, b):
    """Wrote the whole ones sum: 46 + 37 = 7|13 = 713."""
    return int("%d%d" % (a // 10 + b // 10, a % 10 + b % 10))


def sub_small_from_big(a, b):
    """Took the smaller digit from the bigger one in each column: 52 − 27 = 35."""
    da, db = digits(a), digits(b)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(3))


def sub_forgot_reduce(a, b):
    """Regrouped the ones but did not cross out the ten: 52 − 27 = 35 (12 − 7 = 5, 5 − 2 = 3)."""
    r = a - b
    if a % 10 < b % 10:
        r += 10
    return r


def add_cands(a, b):
    s = a + b
    c = []
    if a % 10 + b % 10 >= 10:
        c += [add_no_carry([a, b]), add_concat(a, b)]
    return c + [s + 10, s - 10, s + 1, s - 1]


def sub_cands(a, b):
    r = a - b
    return [sub_small_from_big(a, b), sub_forgot_reduce(a, b), a + b, r - 10, r + 10, r + 1, r - 1]


# ------------------------------------------------------------ number pickers
def pick_add(rnd, carry, seen, max_tens=9, top=99):
    while True:
        a, b = rnd.randint(11, 89), rnd.randint(11, 89)
        if a % 10 == 0 or b % 10 == 0 or a + b > top or a // 10 > max_tens or b // 10 > max_tens:
            continue
        if (a % 10 + b % 10 >= 10) != carry or (a, b) in seen or (b, a) in seen:
            continue
        seen.add((a, b))
        return a, b


def pick_sub(rnd, regroup, seen, round_ten=False):
    while True:
        a = rnd.randint(4, 9) * 10 if round_ten else rnd.randint(31, 99)
        if not round_ten and a % 10 == 0:
            continue
        b = rnd.randint(12, a - 8)
        if b % 10 == 0 or (a, b) in seen:
            continue
        if (a % 10 < b % 10) != regroup:
            continue
        if not regroup and a % 10 == b % 10:
            continue
        seen.add((a, b))
        return a, b


def item_add(a, b, col):
    q = (fig(column_svg([a, b], "+")) + "Add.") if col else "What is %d + %d?" % (a, b)
    return mcq(q, a + b, add_cands(a, b), add_steps([a, b]))


def item_sub(a, b, col):
    q = (fig(column_svg([a, b], "-")) + "Subtract.") if col else "What is %d − %d?" % (a, b)
    return mcq(q, a - b, sub_cands(a, b), sub_steps(a, b))


# ============================================================ set 1: base-ten blocks
def set_blocks(rnd, seen):
    its = []
    for _ in range(6):                                  # no regrouping, with blocks
        a, b = pick_add(rnd, False, seen, max_tens=5)
        s = a + b
        rev = int(str(s)[::-1])
        e = ("Count the tens: %d + %d = %s. Count the ones: %d + %d = %s. %s and %s is %d."
             % (a // 10, b // 10, pl(s // 10, "ten"), a % 10, b % 10, pl(s % 10, "one"),
                cap(pl(s // 10, "ten")), pl(s % 10, "one"), s))
        its.append(mcq(fig(blocks_svg([(a // 10, a % 10), (b // 10, b % 10)])) + "Use the blocks. What is %d + %d?" % (a, b),
                       s, [rev, s + 10, s - 10, s + 1, s - 1], e))
    for _ in range(6):                                  # regrouping: 10 ones make a new ten
        a, b = pick_add(rnd, True, seen, max_tens=4)
        s = a + b
        o = a % 10 + b % 10
        e = ("Tens: %d + %d = %s. Ones: %d + %d = %d ones. 10 ones make 1 more ten. Now there are %s and %s: %d."
             % (a // 10, b // 10, pl(a // 10 + b // 10, "ten"), a % 10, b % 10, o,
                pl(s // 10, "ten"), pl(s % 10, "one"), s))
        its.append(mcq(fig(blocks_svg([(a // 10, a % 10), (b // 10, b % 10)])) +
                       "Use the blocks. Make a ten with the ones. What is %d + %d?" % (a, b),
                       s, [add_no_carry([a, b]), add_concat(a, b), s + 10, s - 1], e))
    for t, n in [(4, 12), (3, 15)]:                     # more than 9 ones
        v = 10 * t + n
        e = ("There are %d ones. 10 ones make 1 ten, so %d tens and %d ones is %d tens and %s. That is %d."
             % (n, t, n, t + 1, pl(n - 10, "one"), v))
        its.append(mcq(fig(blocks_svg([(t, n)], labels=False)) + "There are %d tens and %d ones. What number is it?" % (t, n),
                       v, [int("%d%d" % (t, n)), 10 * t + n - 10, v + 10], e))
    for a, t in [(47, 3), (26, 5), (58, 2)]:             # add tens
        s = a + 10 * t
        e = ("%d is %s. Add to the tens only: %d tens + %d tens = %d tens. The ones stay %d. %d + %d = %d."
             % (10 * t, pl(t, "ten"), a // 10, t, s // 10, a % 10, a, 10 * t, s))
        its.append(mcq("What is %d + %d?" % (a, 10 * t), s, [a + t, s + 10, s - 10], e))
    for a, n in [(52, 6), (31, 7), (64, 4)]:             # add ones
        s = a + n
        e = ("%d is %s. Add to the ones only: %d + %d = %d. The tens stay %d. %d + %d = %d."
             % (n, pl(n, "one"), a % 10, n, s % 10, a // 10, a, n, s))
        its.append(mcq("What is %d + %d?" % (a, n), s, [a + 10 * n, s + 10, s + 1, s - 1], e))
    assert len(its) == 20, len(its)
    its = its[:6] + its[14:] + its[6:12] + its[12:14]
    return {"title": "Add tens and ones with base-ten blocks", "items": its}


# ============================================================ set 2: add with regrouping
def set_add(rnd, P, seen):
    its = []
    for i in range(12):
        a, b = pick_add(rnd, True, seen)
        its.append(item_add(a, b, i % 3 != 2))
    for a, b in [(38, 25), (29, 34), (47, 36), (19, 57)]:     # make a ten
        need = 10 - a % 10
        assert b % 10 >= need
        nm, he, his = P.next()
        q = ("To add %d + %d, %s makes a ten. %s moves %d from %d to %d. Which is the same as %d + %d?"
             % (a, b, nm, cap(he), need, b, a, a, b))
        e = ("%d + %d = %d. Then %d − %d = %d. So %d + %d = %d + %d = %d. Moving %d does not change the total."
             % (a, need, a + need, b, need, b - need, a, b, a + need, b - need, a + b, need))
        its.append(mcq(q, "%d + %d" % (a + need, b - need),
                       ["%d + %d" % (a + need, b), "%d + %d" % (a + need, b + need), "%d + %d" % (a + need - 10, b)], e))
    for a, b in [(46, 37), (28, 54)]:                          # break apart: which is the same
        t1, o1, t2, o2 = a // 10 * 10, a % 10, b // 10 * 10, b % 10
        e = ("%d is %d + %d. %d is %d + %d. Tens: %d + %d = %d. Ones: %d + %d = %d. %d + %d = %d."
             % (a, t1, o1, b, t2, o2, t1, t2, t1 + t2, o1, o2, o1 + o2, t1 + t2, o1 + o2, a + b))
        its.append(mcq("Break apart the tens and ones. Which is the same as %d + %d?" % (a, b),
                       "%d + %d + %d + %d" % (t1, t2, o1, o2),
                       ["%d + %d + %d + %d" % (t1 // 10, t2 // 10, o1, o2), "%d + %d + %d + %d" % (t1, t2 // 10, o1, o2),
                        "%d + %d + %d" % (t1, t2, o1)], e))
    for a, b in [(35, 48), (57, 26)]:                          # break apart: the ones part
        t, o = a // 10 * 10 + b // 10 * 10, a % 10 + b % 10
        e = ("Tens: %d + %d = %d. Ones: %d + %d = %d. So %d + %d = %d + %d = %d."
             % (a // 10 * 10, b // 10 * 10, t, a % 10, b % 10, o, a, b, t, o, a + b))
        its.append(mcq("Break apart the tens and ones: %d + %d = %d + ☐. What number goes in the box?" % (a, b, t),
                       o, [o % 10, a + b, o + 1, o - 1], e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Add 2-digit numbers with regrouping", "items": its}


# ============================================================ set 3: subtract
def set_sub(rnd, seen):
    its = []
    for i in range(6):                                          # no regrouping
        a, b = pick_sub(rnd, False, seen)
        r = a - b
        its.append(mcq((fig(column_svg([a, b], "-")) + "Subtract.") if i % 2 else "What is %d − %d?" % (a, b), r,
                       [a - 10 * (b // 10), a - b % 10, r + 10, r - 10, r + 1], sub_steps(a, b)))
    for i in range(13):                                         # with regrouping
        a, b = pick_sub(rnd, True, seen)
        its.append(item_sub(a, b, i % 2 == 0))
    its.append(mcq(fig(blocks_svg([(5, 2)], labels=False)) +
                   "These blocks show 52. You want to take away 27. There are only 2 ones, so you cannot take away 7 ones. "
                   "What should you do first?",
                   "Trade 1 ten for 10 ones",
                   ["Take away 2 ones instead", "Take 2 from 7 to get 5", "Take away 3 tens"],
                   "Trade 1 ten for 10 ones. Now there are 4 tens and 12 ones. Take away 7 ones: 12 − 7 = 5. "
                   "Take away 2 tens: 4 − 2 = 2. 52 − 27 = 25."))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Subtract 2-digit numbers", "items": its}


# ============================================================ set 4: across tens, missing numbers, checking
def set_missing(rnd, P, seen):
    its = []
    for i in range(5):                                          # 60 − 27
        a, b = pick_sub(rnd, True, seen, round_ten=True)
        r = a - b
        up = (b // 10 + 1) * 10
        e = sub_steps(a, b) + " Or count up: %d + %d = %d, then %d + %d = %d. %d + %d = %d." % (
            b, up - b, up, up, a - up, a, up - b, a - up, r)
        q = (fig(column_svg([a, b], "-")) + "Subtract.") if i % 2 == 0 else "What is %d − %d?" % (a, b)
        its.append(mcq(q, r, sub_cands(a, b), e))
    its.append(mcq("What is 100 − 46?", 54, [64, 146, 44, 56],
                   sub_steps(100, 46) + " Or count up: 46 + 4 = 50, then 50 + 50 = 100. 4 + 50 = 54."))
    for k in range(5):                                          # ☐ + b = s  /  a + ☐ = s
        while True:
            x, b = rnd.randint(13, 58), rnd.randint(14, 47)
            s = x + b
            if s <= 99 and s % 10 < b % 10 and s % 10 != 0 and (s, b) not in seen:
                break
        seen.add((s, b))
        if k % 2 == 0:
            q = "What number goes in the box?  <b>☐ + %d = %d</b>" % (b, s)
            e = "Use subtraction: %d − %d = ☐. " % (s, b) + sub_steps(s, b, check=False) + " Check: %d + %d = %d." % (x, b, s)
        else:
            q = "What number goes in the box?  <b>%d + ☐ = %d</b>" % (b, s)
            e = "Use subtraction: %d − %d = ☐. " % (s, b) + sub_steps(s, b, check=False) + " Check: %d + %d = %d." % (b, x, s)
        its.append(mcq(q, x, [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b), x + 10, x - 10], e))
    for _ in range(3):                                          # a − ☐ = r
        while True:
            a, x = rnd.randint(52, 96), rnd.randint(15, 49)
            r = a - x
            if r >= 11 and a % 10 < r % 10 and a % 10 != 0 and (a, x) not in seen:
                break
        seen.add((a, x))
        e = ("Think: %d take away what number leaves %d? Find %d − %d. " % (a, r, a, r) + sub_steps(a, r, check=False)
             + " Check: %d − %d = %d." % (a, x, r))
        its.append(mcq("What number goes in the box?  <b>%d − ☐ = %d</b>" % (a, r), x,
                       [a + r, sub_small_from_big(a, r), sub_forgot_reduce(a, r), r, x + 10], e))
    for a, b in [(72, 35), (81, 47), (64, 29)]:                 # which addition checks it
        r = a - b
        nm, he, his = P.next()
        e = ("Add the answer to the number you took away: %d + %d = %d. You get back %d, so the answer is right."
             % (r, b, a, a))
        its.append(mcq("%s found %d − %d = %d. Which addition checks %s answer?" % (nm, a, b, r, his),
                       "%d + %d = %d" % (r, b, a),
                       ["%d + %d = %d" % (a, b, a + b), "%d + %d = %d" % (a, r, a + r), "%d − %d = %d" % (max(r, b), min(r, b), abs(r - b))], e))
    for a, b, said in [(63, 28, 45), (91, 56, 35), (74, 38, 44)]:  # is it right?
        r = a - b
        nm, he, his = P.next()
        if said == r:
            e = ("Check by adding: %d + %d = %d. You get back %d, so %s is right. %s"
                 % (r, b, a, a, he, sub_steps(a, b, check=False)))
            ans = "Yes, %s is right" % he
            cands = ["No, it is %d" % v for v in (sub_small_from_big(a, b), a + b, r + 10, r - 10)]
        else:
            e = ("Check by adding: %d + %d = %d, not %d. So %d is wrong. %s"
                 % (said, b, said + b, a, said, sub_steps(a, b)))
            ans = "No, it is %d" % r
            cands = ["Yes, %s is right" % he] + ["No, it is %d" % v for v in (r - 10, a + b, sub_small_from_big(a, b))]
        its.append(mcq("%s says %d − %d = %d. Is %s right?" % (nm, a, b, said, he), ans, cands, e))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Subtract from tens, missing numbers and checking", "items": its}


# ============================================================ set 5: several numbers and stories
def three_numbers(rnd, seen, tens_pair):
    while True:
        a, b, c = rnd.randint(11, 39), rnd.randint(11, 39), rnd.randint(11, 39)
        if 0 in (a % 10, b % 10, c % 10) or a + b + c > 99:
            continue
        key = tuple(sorted((a, b, c)))
        if key in seen:
            continue
        if tens_pair and a % 10 + b % 10 != 10:
            continue
        if not tens_pair and (a % 10 + b % 10 + c % 10 < 10 or a % 10 + b % 10 == 10 or a % 10 + c % 10 == 10
                              or b % 10 + c % 10 == 10):
            continue
        seen.add(key)
        return a, b, c


def set_several(rnd, P, seen):
    its = []
    for _ in range(3):                                          # look for a ten
        a, b, c = three_numbers(rnd, seen, True)
        s = a + b + c
        order = [a, c, b]
        e = ("Look for ones that make 10: %d + %d = 10. So %d + %d = %d. Then %d + %d = %d."
             % (a % 10, b % 10, a, b, a + b, a + b, c, s))
        its.append(mcq("What is %s?" % " + ".join(map(str, order)), s, [s - 10, a + c, s + 10, s - 1], e))
    for _ in range(3):                                          # three numbers in columns
        a, b, c = three_numbers(rnd, seen, False)
        s = a + b + c
        its.append(mcq(fig(column_svg([a, b, c], "+")) + "Add.", s,
                       [add_no_carry([a, b, c]), a + b, s - 10, s + 10, s - 1], add_steps([a, b, c])))
    four = []
    while len(four) < 4:                                        # four numbers in columns
        ns = [rnd.randint(11, 29) for _ in range(4)]
        if 0 in [n % 10 for n in ns] or sum(ns) > 99 or tuple(sorted(ns)) in seen:
            continue
        o = sum(n % 10 for n in ns)
        if (len(four) < 2 and not 10 <= o < 20) or (len(four) >= 2 and o < 20):
            continue
        seen.add(tuple(sorted(ns)))
        four.append(ns)
    for ns in four:
        s = sum(ns)
        carry = sum(n % 10 for n in ns) // 10
        cands = [add_no_carry(ns)] + ([s - 10] if carry == 2 else []) + [s - ns[-1], s + 10, s - 1]
        its.append(mcq(fig(column_svg(ns, "+")) + "Add.", s, cands,
                       add_steps(ns) + " Remember to add all 4 numbers."))

    def story(t, ans, unit, cands, e):
        its.append(mcq(t, "%d %s" % (ans, unit), ["%d %s" % (v, unit) for v in cands if v > 0], e))

    nm, he, his = P.next()
    a, b = 38, 25
    story("%s has %d stickers. %s friend gives %s %d more. How many stickers does %s have now?"
          % (nm, a, cap(his), "her" if he == "she" else "him", b, nm),
          a + b, "stickers", add_cands(a, b), "Getting more means add. " + add_steps([a, b]))
    a, b = 52, 27
    story("A bus has %d seats. %d children get on, and each child takes a seat. How many seats are empty?" % (a, b),
          a - b, "seats", sub_cands(a, b), "Take the full seats away from all the seats: subtract. " + sub_steps(a, b))
    nm, he, his = P.next()
    a, b = 64, 29
    story("%s picks %d apples. %s gives away %d of them. How many apples are left?" % (nm, a, cap(he), b),
          a - b, "apples", sub_cands(a, b), "Giving away means subtract. " + sub_steps(a, b))
    nm, he, his = P.next()
    ns = [23, 18, 31]
    story("%s read %d pages on Monday, %d pages on Tuesday and %d pages on Wednesday. How many pages did %s read in all?"
          % (nm, ns[0], ns[1], ns[2], he), sum(ns), "pages", [add_no_carry(ns), ns[0] + ns[1], sum(ns) + 10],
          "Add all three days. " + add_steps(ns))
    a, t = 45, 80
    story("The class has %d crayons. They need %d crayons. How many more crayons do they need?" % (a, t),
          t - a, "crayons", [t + a, sub_small_from_big(t, a), sub_forgot_reduce(t, a), t - a - 10],
          "Find the missing part: %d + ☐ = %d. Count up: %d + 5 = 50, then 50 + 30 = 80. 5 + 30 = 35. Check: 45 + 35 = 80."
          % (a, t, a))
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    a, b = 71, 46
    story("%s has %d cents. %s has %d cents. How many more cents does %s have than %s?" % (n1, a, n2, b, n1, n2),
          a - b, "cents", sub_cands(a, b), "How many more means find the difference: subtract. " + sub_steps(a, b))
    ns = [17, 26, 14, 22]
    story("A garden has %d red flowers, %d yellow flowers, %d pink flowers and %d white flowers. How many flowers are there?"
          % tuple(ns), sum(ns), "flowers", [add_no_carry(ns), sum(ns) - ns[-1], sum(ns) + 10],
          "Add all 4 colors. " + add_steps(ns))
    r, b = 35, 18
    story("Some birds sit in a tree. %d birds fly away. Now %d birds are left. How many birds were in the tree at first?"
          % (b, r), r + b, "birds", [r - b, add_no_carry([r, b]), r + b + 10],
          "The birds that left plus the birds that stayed make all the birds: add. " + add_steps([r, b])
          + " Check: %d − %d = %d." % (r + b, b, r))
    nm, he, his = P.next()
    a, b = 90, 36
    story("%s has %d cents. %s buys a pencil for %d cents. How much money does %s have left?" % (nm, a, cap(he), b, he),
          a - b, "cents", sub_cands(a, b), "Spending money means subtract. " + sub_steps(a, b))
    a, b = 48, 37
    story("A bakery makes %d muffins in the morning and %d muffins in the afternoon. How many muffins does it make in all?"
          % (a, b), a + b, "muffins", add_cands(a, b), "In all means add. " + add_steps([a, b]))
    assert len(its) == 20, len(its)
    return {"title": "Add three or four numbers and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Tens and ones</h2>"
        "<p>A 2-digit number has <b>tens</b> and <b>ones</b>. 34 is 3 tens and 4 ones. To add, put the tens together "
        "and put the ones together.</p>"
        "<figure class='sn-fig'>" + blocks_svg([(3, 4), (2, 5)]) +
        "<figcaption>34 + 25. Tens: 3 + 2 = 5 tens. Ones: 4 + 5 = 9 ones. 5 tens and 9 ones is 59.</figcaption></figure>"
        "<h2>10 ones make a new ten</h2>"
        "<p>If the ones add up to 10 or more, <b>regroup</b>: trade 10 ones for 1 ten. In columns, write the ones digit "
        "and put a small 1 on top of the tens.</p>"
        "<figure class='sn-fig'>" + column_svg([46, 37], "+", big=True, marks=True) +
        "<figcaption>Ones: 6 + 7 = 13. Write 3 and regroup 1 ten. Tens: 4 + 3 + 1 = 8. Answer: 83.</figcaption></figure>"
        + ex("Make a ten", "What is 38 + 25?",
             "38 needs 2 more to make 40. Take 2 from 25 to get 23. Now add 40 + 23.", "63") +
        "<h2>Subtract with regrouping</h2>"
        "<p>Start with the ones. If the top digit is smaller, trade 1 ten for 10 ones. Cross out the tens digit and "
        "write 1 less.</p>"
        "<figure class='sn-fig'>" + column_svg([52, 27], "-", big=True, marks=True) +
        "<figcaption>Ones: 2 − 7 needs a regroup. 5 tens become 4 tens, and 2 ones become 12 ones. 12 − 7 = 5. "
        "Tens: 4 − 2 = 2. Answer: 25. Check: 25 + 27 = 52.</figcaption></figure>"
        + ex("Count up", "What is 60 − 27?",
             "Start at 27. 27 + 3 = 30. 30 + 30 = 60. You counted up 3 + 30.", "33") +
        "<h2>Add three or four numbers</h2>"
        "<p>Look for ones that make 10 and add them first. You can add in any order.</p>"
        + ex("Look for a ten", "What is 26 + 35 + 14?",
             "6 + 4 = 10, so 26 + 14 = 40. Then 40 + 35 = 75.", "75") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Forgetting the new ten: 46 + 37 = 73", "Write the small 1 on top of the tens and add it"],
            ["Writing 13 in the ones: 46 + 37 = 713", "Only one digit goes in each column. Regroup the ten"],
            ["Taking the small digit from the big one: 52 − 27 = 35", "Always take the bottom digit from the top. Regroup when the top is smaller"],
            ["Regrouping but not crossing out: 63 − 28 = 45", "When you trade 1 ten, the tens digit gets 1 smaller"],
            ["Skipping a number when adding four numbers", "Touch each number as you add it"],
        ])
    )


FAQ = [
    {"q": "How do you teach 2-digit addition with regrouping?",
     "a": "Start with base-ten blocks: add the ones, and when there are 10 or more, trade 10 ones for 1 ten. Then show the same steps in columns, with a small 1 written on top of the tens."},
    {"q": "How do you subtract 2-digit numbers with regrouping, like 52 − 27?",
     "a": "Start with the ones. 2 − 7 does not work, so trade 1 ten for 10 ones: 12 − 7 = 5. Now there are 4 tens: 4 − 2 = 2. The answer is 25."},
    {"q": "How can my child check a subtraction answer?",
     "a": "Add the answer to the number that was taken away. For 52 − 27 = 25, check 25 + 27 = 52. If you get the starting number, the answer is right."},
    {"q": "What does 2.NBT.B.5 mean?",
     "a": "It is the Common Core standard for Grade 2: fluently add and subtract within 100 using place value and the link between addition and subtraction. Standard 2.NBT.B.6 adds up to four 2-digit numbers."},
]


def gen():
    rnd = random.Random(202)
    P = People(rnd)
    seen_a, seen_s, seen_n = set(), set(), set()
    sets = [set_blocks(rnd, seen_a), set_add(rnd, P, seen_a), set_sub(rnd, seen_s),
            set_missing(rnd, P, seen_s), set_several(rnd, P, seen_n)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "add-subtract-within-100", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Within 100",
        "seo_title": "Grade 2 Addition and Subtraction Within 100 Worksheets: 2-Digit Regrouping, Base-Ten Blocks and Word Problems",
        "short_title": "Add and subtract within 100",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "2.NBT.B.5–6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/NBT/B/",
        "standard_text": "Fluently add and subtract within 100 using strategies based on place value, properties of operations, and/or the relationship between addition and subtraction. Add up to four two-digit numbers using strategies based on place value and properties of operations.",
        "meta_desc": "Free Grade 2 worksheets for adding and subtracting 2-digit numbers within 100: base-ten blocks, regrouping, subtracting from tens, missing numbers, adding three or four numbers and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Add or subtract the ones first, then the tens. 10 ones make 1 ten.",
        "key_sub": "Adding: if the ones make 10 or more, regroup 1 ten. Subtracting: if the top ones digit is smaller, trade 1 ten for 10 ones. Check a subtraction by adding back.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base-ten blocks")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
