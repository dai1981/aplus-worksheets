# -*- coding: utf-8 -*-
"""
AU Year 3 Maths (Australian Curriculum v9.0, AC9M3A03): multiplication facts for 3, 4, 5 and 10.
  python3 tools/gen_au_maths_y3_multiplication_facts.py
Every product, quotient and missing number is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
INK = "#2b2b2b"
COIN = "#d9dde2"
COIN_EDGE = "#7a828c"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
X = "×"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def dots(x0, y0, rows, cols, cell, col=GREEN):
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                   % (x0 + c * cell + cell // 2, y0 + r * cell + cell // 2, cell // 3, col)
                   for r in range(rows) for c in range(cols))


def array_svg(rows, cols, cell=24):
    o = 6
    return svg_wrap(cols * cell + 2 * o, rows * cell + 2 * o, dots(o, o, rows, cols, cell),
                    "array of %d rows with %d dots in each row" % (rows, cols))


GROUP_SHAPE = {3: (1, 3), 4: (2, 2), 5: (1, 5), 10: (2, 5)}


def groups_svg(g, n, cell=20, label_sizes=False):
    """g equal groups of n counters, each group in a rounded box."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = {3: 4, 4: 4, 5: 3, 10: 3}[n]
    per_row = min(per_row, g)
    nrows = (g + per_row - 1) // per_row
    lab = 22 if label_sizes else 0
    W = per_row * bw + (per_row - 1) * gap + 4
    H = nrows * (bh + lab) + (nrows - 1) * gap + 4
    s = []
    for i in range(g):
        r, c = divmod(i, per_row)
        x = 2 + c * (bw + gap)
        y = 2 + r * (bh + lab + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, bw, bh, FILL, GREEN))
        s.append(dots(x + pad, y + pad, gr, gc, cell))
        if label_sizes:
            s.append(text(x + bw / 2, y + bh + 17, str(n), 15))
    return svg_wrap(W, H, "".join(s), "%d equal groups with %d counters in each group" % (g, n))


def coins_svg(k, value):
    """k silver coins of the same value (5c or 10c), up to 5 in a row."""
    r = 19 if value == 10 else 16
    d = 2 * r + 8
    per_row = k if k <= 6 else (k + 1) // 2
    nrows = (k + per_row - 1) // per_row
    W, H = per_row * d + 4, nrows * d + 4
    s = []
    for i in range(k):
        row, col = divmod(i, per_row)
        cx = 2 + col * d + d / 2
        cy = 2 + row * d + d / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (cx, cy, r, COIN, COIN_EDGE))
        s.append(text(cx, cy + 5.5, "%dc" % value, 15))
    return svg_wrap(W, H, "".join(s), "%d coins worth %d cents each" % (k, value))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def calc(expr):
    """Evaluate a short expression written with × and ÷ (only digits, spaces and + − × ÷)."""
    assert re.fullmatch(r"[0-9 +×÷−]+", expr), expr
    return eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-"))


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the fact family being practised (3, 4, 5 or 10)."""
    p = a * b
    if b == 3:
        return "Double %d is %d. Add one more %d: %d + %d = <b>%d</b>." % (a, 2 * a, a, 2 * a, a, p)
    if b == 4:
        return "Double %d, then double again: %d → %d → <b>%d</b>." % (a, a, 2 * a, p)
    if b == 5:
        return "10 %s %d = %d. The 5s are half of the 10s: half of %d is <b>%d</b>." % (X, a, 10 * a, 10 * a, p)
    if b == 10:
        return "%d tens make %d. So %d %s 10 = <b>%d</b>." % (a, p, a, X, p)
    raise ValueError(b)


def rev(n):
    s = str(n)
    if len(s) == 2 and s[0] != s[1] and s[1] != "0":
        return int(s[::-1])
    return None


def fact_cands(a, b, rnd):
    """Real mistakes: the fact next door, one group too many/few, adding, swapped digits."""
    p = a * b
    pool = [a * (b + 1), a * (b - 1), (a + 1) * b, (a - 1) * b, a + b]
    r = rev(p) if p > 20 else None
    if r:
        pool.append(r)
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 1, p - 1, p + 10, p - 10]


def fact_q(a, b, rnd):
    """Question shows a × b or b × a; b is the fact family being practised."""
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def facts(b, mults, rnd):
    mults = list(mults)
    rnd.shuffle(mults)
    return [fact_q(a, b, rnd) for a in mults]


def seq_q(seq, step, wrong, extra=""):
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1)) and seq[0] % step == 0
    assert nxt not in wrong
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, nxt, extra)
    return mcq("Skip count by %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e.strip())


def count_q(svg_html, g, n, wrong, kind):
    p = g * n
    assert p not in wrong
    if kind == "groups":
        e = "There are %d groups of %d. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many counters are there altogether?"
    else:
        e = "There are %d rows with %d dots in each row. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many dots are in this array?"
    return mcq(fig(svg_html) + ask, p, wrong, e)


def coin_q(k, value, wrong):
    tot = k * value
    assert tot < 100 and tot not in wrong
    e = "Skip count by %ds %d times: %s. %d %s %dc = <b>%dc</b>." % (
        value, k, ", ".join(str(value * i) for i in range(1, k + 1)), k, X, value, tot)
    return mcq(fig(coins_svg(k, value)) + "How much money is this?", "%dc" % tot, ["%dc" % w for w in wrong], e)


def multiple_q(ask, right, wrong, table_n, inside):
    assert (right % table_n == 0) == inside and all((w % table_n == 0) != inside for w in wrong)
    lst = ", ".join(str(table_n * k) for k in range(1, 11))
    e = "Skip count by %ds: %s. <b>%d</b> %s." % (
        table_n, lst, right, "is in the list" if inside else "is not in the list")
    if table_n == 5:
        e += " Numbers in the 5s always end in 0 or 5."
    if table_n == 10:
        e += " Numbers in the 10s always end in 0."
    return mcq(ask, right, wrong, e)


def double_q(a):
    """2 × a is known; double it to find 4 × a."""
    k = 2 * a
    ans = 4 * a
    wrong = [k, k + 2, k + a, 3 * a]
    e = "4 is double 2, so 4 %s %d is double 2 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans)
    return mcq("2 %s %d = %d. Double it to find 4 %s %d." % (X, a, k, X, a), ans, wrong, e)


def half_q(a):
    """10 × a is known; halve it to find 5 × a."""
    t = 10 * a
    ans = 5 * a
    assert 2 * ans == t
    wrong = [t, t - 5, a + 5, 5 * (a + 1)]
    e = "5 is half of 10, so 5 %s %d is half of 10 %s %d. Half of %d is <b>%d</b>." % (X, a, X, a, t, ans)
    return mcq("10 %s %d = %d. Use it to find 5 %s %d." % (X, a, t, X, a), ans, wrong, e)


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    return mcq(ask, right, wrong, e)


def true_sentence_q(right, wrong, e, ask="Which number sentence is true?"):
    def ok(s):
        lhs, rhs = s.split(" = ")
        return calc(lhs) == int(rhs)
    assert ok(right) and not any(ok(w) for w in wrong), (right, wrong)
    return mcq(ask, right, wrong, e)


# ============================================================ set 1: the 3s and 4s
def set_three_four(rnd):
    its = [
        count_q(groups_svg(4, 3), 4, 3, [7, 9, 15], "groups"),
        count_q(groups_svg(5, 4), 5, 4, [9, 16, 24], "groups"),
        count_q(array_svg(3, 7), 3, 7, [10, 18, 24], "array"),
        count_q(array_svg(4, 6), 4, 6, [10, 18, 28], "array"),
    ]
    for r, c in [(5, 3), (4, 8)]:
        p = r * c
        wrong = ["%d + %d" % (r, c), "%d %s %d" % (r, X, c + 1), "%d %s %d" % (r - 1, X, c)]
        e = ("There are %d rows with %d dots in each row, so it shows %d %s %d = %d. "
             "%d %s %d gives the same answer: it is the array turned on its side." % (r, c, r, X, c, p, c, X, r))
        its.append(choice_calc_q(fig(array_svg(r, c)) + "Which number sentence matches this array?", p,
                                 "%d %s %d" % (r, X, c), wrong, e))
    its.append(seq_q([12, 15, 18], 3, [24, 20, 22], "So 3 %s 7 = 21." % X))
    its.append(seq_q([20, 24, 28], 4, [36, 30, 31], "So 4 %s 8 = 32." % X))
    for a in (7, 9, 10):
        its.append(double_q(a))
    its += facts(3, [3, 4, 6, 8, 9], rnd)
    its += facts(4, [2, 4, 5], rnd)
    its.append(multiple_q("Which number is in the 3s?", 21, [20, 22, 25], 3, True))
    assert len(its) == 20, len(its)
    return {"title": "The 3s and 4s: groups, arrays and doubling", "items": its}


# ============================================================ set 2: the 5s and 10s
def set_five_ten(rnd):
    its = [
        coin_q(6, 5, [11, 25, 35]),
        coin_q(9, 5, [14, 40, 50]),
        coin_q(7, 10, [17, 60, 80]),
        coin_q(8, 10, [18, 70, 90]),
        seq_q([15, 20, 25], 5, [35, 26, 40], "So 5 %s 6 = 30." % X),
        seq_q([40, 50, 60], 10, [80, 61, 71], "So 10 %s 7 = 70." % X),
    ]
    for a in (6, 8, 3):
        its.append(half_q(a))
    its += facts(5, [4, 7, 2], rnd)
    its += facts(10, [3, 4, 6, 9, 5], rnd)
    its.append(multiple_q("Which number is in the 5s?", 45, [42, 48, 54], 5, True))
    its.append(multiple_q("Which number is <b>not</b> in the 10s?", 55, [50, 60, 70], 10, False))
    its.append(mcq("Which is the same as 5 %s 8?" % X, "half of 10 %s 8" % X,
                   ["double 10 %s 8" % X, "5 + 8", "10 %s 8 − 5" % X],
                   "5 is half of 10, so 5 %s 8 is half of 10 %s 8. Half of 80 is <b>40</b>." % (X, X)))
    assert 10 * 8 // 2 == 5 * 8 and 2 * 80 != 40 and 5 + 8 != 40 and 80 - 5 != 40
    assert len(its) == 20, len(its)
    return {"title": "The 5s and 10s: coins and halving", "items": its}


# ============================================================ set 3: mixed facts and turnarounds
def set_mixed(rnd):
    its = []
    for a, b in [(4, 7), (3, 9), (5, 8), (10, 6)]:
        p = a * b
        e = ("Turnaround facts have the same answer. %d %s %d = %d, so %d %s %d = <b>%d</b> too."
             % (a, X, b, p, b, X, a, p))
        its.append(mcq("%d %s %d = %d. So %d %s %d = ?" % (a, X, b, p, b, X, a), p,
                       [a + b, p - a, p + a, p - b], e))
    for a, b in [(7, 4), (6, 5)]:
        p = a * b
        e = ("%d %s %d is the turnaround of %d %s %d. Both make <b>%d</b>." % (b, X, a, a, X, b, p))
        its.append(choice_calc_q("Which has the same answer as %d %s %d?" % (a, X, b), p, "%d %s %d" % (b, X, a),
                                 ["%d + %d" % (a, b), "%d %s %d" % (a, X, a), "%d %s %d" % (b, X, b)], e))
    for a, b in [(7, 3), (9, 4), (6, 5), (7, 10), (8, 4), (8, 5), (9, 5), (2, 3)]:
        its.append(fact_q(a, b, rnd))
    for target, right, wrong in [(20, "4 %s 5" % X, ["5 %s 5" % X, "4 %s 6" % X, "10 %s 3" % X]),
                                 (24, "3 %s 8" % X, ["4 %s 5" % X, "3 %s 7" % X, "4 %s 7" % X]),
                                 (30, "3 %s 10" % X, ["3 %s 9" % X, "5 %s 5" % X, "4 %s 10" % X])]:
        a, b = [int(v) for v in right.split(" %s " % X)]
        e = "%d %s %d = <b>%d</b>." % (a, X, b, target) + " Work out each one: " + ", ".join(
            "%s = %d" % (w, calc(w)) for w in wrong) + "."
        its.append(choice_calc_q("Which fact has the answer %d?" % target, target, right, wrong, e))
    its.append(true_sentence_q("4 %s 9 = 36" % X,
                               ["3 %s 9 = 24" % X, "5 %s 7 = 30" % X, "10 %s 4 = 14" % X],
                               "<b>4 %s 9 = 36</b>. 3 %s 9 = 27, 5 %s 7 = 35 and 10 %s 4 = 40." % (X, X, X, X)))
    its.append(true_sentence_q("5 %s 9 = 45" % X,
                               ["4 %s 6 = 20" % X, "3 %s 6 = 21" % X, "10 %s 5 = 15" % X],
                               "<b>5 %s 9 = 45</b>. 4 %s 6 = 24, 3 %s 6 = 18 and 10 %s 5 = 50." % (X, X, X, X),
                               "Only one of these number sentences is correct. Which one?"))
    its.append(mcq("3 %s 5 = 15. Use it to find 3 %s 6." % (X, X), 18, [16, 15, 21, 20],
                   "3 %s 6 is one more group of 3 than 3 %s 5: 15 + 3 = <b>18</b>. "
                   "16 adds 1 instead of 3." % (X, X)))
    assert 3 * 6 == 15 + 3
    assert len(its) == 20, len(its)
    return {"title": "Mixed facts and turnarounds", "items": its}


# ============================================================ set 4: related division facts
def set_division(rnd):
    its = []
    for d, q in [(3, 7), (4, 9), (5, 6), (10, 8), (3, 9), (4, 6), (5, 9), (10, 4)]:
        p = d * q
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, p, p - d, d], e))
    for a, b in [(3, 8), (10, 7)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, p], e))
    for a, b in [(9, 5), (7, 4)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [a + 1, a - 1, p - b, p], e))
    for g, n in [(3, 5), (5, 4)]:
        p = g * n
        e = "Count the groups: there are %d groups of %d. %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d." % (
            g, n, p, n, g, g, X, n, p)
        its.append(mcq(fig(groups_svg(g, n)) + "%d counters are put into groups of %d. How many groups are there?" % (p, n),
                       g, [g + 1, g - 1, p - n, p], e))
    for d, q in [(5, 7), (3, 6)]:
        p = d * q
        e = "Use the related multiplication fact: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d." % (q, X, d, p, p, d, q)
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, q - d, p + d, p - d], e))
    for a, b in [(4, 8), (5, 7)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, a, b)
        wrong = ["%d ÷ %d = %d" % (b, a, p), "%d ÷ %d = %d" % (p, b, a + 1), "%d ÷ %d = %d" % (p, a, b - 1)]
        assert p / a == b and all(int(w.split(" = ")[1]) != calc(w.split(" = ")[0]) for w in wrong)
        e = ("%d, %d and %d make a fact family. %d %s %d = %d, so <b>%d ÷ %d = %d</b> and %d ÷ %d = %d. "
             "Division starts with the biggest number, %d." % (a, b, p, a, X, b, p, p, a, b, p, b, a, p))
        its.append(mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e))
    its.append(mcq("Which fact helps you work out 40 ÷ 5?", "5 %s 8 = 40" % X,
                   ["5 %s 7 = 35" % X, "40 + 5 = 45", "40 − 5 = 35"],
                   "Division is the opposite of multiplication. 40 ÷ 5 asks: 5 times what makes 40? "
                   "<b>5 %s 8 = 40</b>, so 40 ÷ 5 = 8." % X))
    its.append(mcq("Which fact helps you work out 30 ÷ 3?", "3 %s 10 = 30" % X,
                   ["3 %s 9 = 27" % X, "30 − 3 = 27", "3 + 10 = 13"],
                   "30 ÷ 3 asks: 3 times what makes 30? <b>3 %s 10 = 30</b>, so 30 ÷ 3 = 10." % X))
    assert 5 * 8 == 40 and 3 * 10 == 30
    assert len(its) == 20, len(its)
    return {"title": "Related division facts", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        if unit == "c":
            u = lambda v: "%dc" % v
        elif unit == "$":
            u = lambda v: "$%d" % v
        else:
            u = lambda v: "%d %s" % (v, unit)
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    nm, he, his = P.next()
    w("A tricycle has 3 wheels. %s sees 6 tricycles at the preschool. How many wheels is that?" % nm, 18, "wheels",
      [9, 15, 21], "6 tricycles with 3 wheels each: 6 %s 3 = <b>18</b>. 9 is 6 + 3, which adds instead of multiplies." % X, 6 * 3)
    w("A chair has 4 legs. How many legs do 9 chairs have?", 36, "legs",
      [13, 32, 40], "9 %s 4 = <b>36</b>. Double 9 is 18, double 18 is 36." % X, 9 * 4)
    nm, he, his = P.next()
    w("Yoghurt tubs come in packs of 4. %s’s mum buys 7 packs. How many tubs is that?" % nm, 28, "tubs",
      [11, 24, 32], "7 packs of 4: 7 %s 4 = <b>28</b>. Double 7 is 14, double 14 is 28." % X, 7 * 4)
    nm, he, his = P.next()
    w("%s has six $5 notes. How much money does %s have?" % (nm, he), 30, "$",
      [11, 25, 35], "6 %s $5 = <b>$30</b>. $11 is 6 + 5, which adds instead of multiplies." % X, 6 * 5)
    w("Each student has 10 fingers. 7 students hold up all their fingers. How many fingers is that?", 70, "fingers",
      [17, 60, 80], "7 %s 10 = <b>70</b>. 7 tens make 70." % X, 7 * 10)
    w("A basketball team has 5 players on the court. There are 6 teams at the sports carnival. How many players is that?",
      30, "players", [11, 25, 35], "6 teams of 5: 6 %s 5 = <b>30</b>. 5, 10, 15, 20, 25, 30." % X, 6 * 5)
    w("At the sausage sizzle, each tray holds 10 sausages. There are 8 trays. How many sausages is that?", 80, "sausages",
      [18, 70, 90], "8 %s 10 = <b>80</b>. 8 tens make 80." % X, 8 * 10)
    nm, he, his = P.next()
    w("Stickers cost 5c each at the school fete. %s buys 9 stickers. How much does %s spend?" % (nm, he), 45, "c",
      [14, 40, 50], "9 %s 5c = <b>45c</b>. 14c is 9 + 5, which adds instead of multiplies." % X, 9 * 5)
    w("Students sit in groups of 3 for maths. There are 8 groups. How many students is that?", 24, "students",
      [11, 21, 27], "8 groups of 3: 8 %s 3 = <b>24</b>. 21 is only 7 groups." % X, 8 * 3)
    w("There are 24 wheels on some tricycles. How many tricycles are there?", 8, "tricycles",
      [7, 9, 24], "Each tricycle has 3 wheels. 24 ÷ 3 = ? 3 %s 8 = 24, so there are <b>8 tricycles</b>." % X, 24 // 3)
    w("35 students get into teams of 5 for sport. How many teams are there?", 7, "teams",
      [6, 30, 35], "35 ÷ 5 = ? Think 5 %s ? = 35. 5 %s 7 = 35, so there are <b>7 teams</b>." % (X, X), 35 // 5)
    nm, he, his = P.next()
    w("%s shares 40 cupcakes equally onto 4 plates. How many cupcakes go on each plate?" % nm, 10, "cupcakes",
      [9, 36, 40], "40 ÷ 4 = ? 4 %s 10 = 40, so each plate has <b>10 cupcakes</b>." % X, 40 // 4)
    nm, he, his = P.next()
    w("%s has $45 in $5 notes. How many notes does %s have?" % (nm, he), 9, "notes",
      [8, 40, 45], "45 ÷ 5 = ? 5 %s 9 = 45, so %s has <b>9 notes</b>." % (X, he), 45 // 5)
    w("Pencils come in packs of 10. The teacher has 60 pencils. How many packs is that?", 6, "packs",
      [5, 50, 60], "60 ÷ 10 = ? 10 %s 6 = 60, so there are <b>6 packs</b>." % X, 60 // 10)
    w("27 apples are put into bags of 3. How many bags are there?", 9, "bags",
      [8, 24, 27], "27 ÷ 3 = ? 3 %s 9 = 27, so there are <b>9 bags</b>." % X, 27 // 3)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s finds 4 shells at the beach. %s finds 5 times as many. How many shells does %s find?" % (nm, nm2, nm2),
      20, "shells", [9, 16, 24],
      "5 times as many as 4 means 5 %s 4 = <b>20</b>. 9 is 5 + 4, which adds instead of multiplies." % X, 5 * 4)
    w("There are 3 tricycles and 4 cars in a toy box. How many wheels is that altogether?", 25, "wheels",
      [7, 21, 28], "Tricycles: 3 %s 3 = 9. Cars have 4 wheels: 4 %s 4 = 16. 9 + 16 = <b>25</b>." % (X, X),
      3 * 3 + 4 * 4)
    nm, he, his = P.next()
    w("%s buys 5 packs of 4 muffins for the class. The class eats 3 muffins. How many are left?" % nm, 17, "muffins",
      [20, 23, 6], "5 %s 4 = 20. Then 20 − 3 = <b>17</b>. 20 forgets the 3 that were eaten." % X, 5 * 4 - 3)
    w("Bread rolls come in bags of 4. 32 students each need one roll for the sausage sizzle. How many bags are needed?",
      8, "bags", [7, 28, 32], "32 ÷ 4 = ? 4 %s 8 = 32, so <b>8 bags</b> are needed." % X, 32 // 4)
    nm, he, his = P.next()
    w("%s reads 3 pages of %s library book every night. How many pages does %s read in 5 nights?" % (nm, his, he),
      15, "pages", [8, 12, 18], "5 %s 3 = <b>15</b>. 8 is 5 + 3, which adds instead of multiplies." % X, 5 * 3)
    assert len(its) == 20
    return {"title": "Multiplication and division word problems", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k), "%d %s 3 = %d" % (k, X, 3 * k), "%d %s 4 = %d" % (k, X, 4 * k),
             "%d %s 5 = %d" % (k, X, 5 * k), "%d %s 10 = %d" % (k, X, 10 * k)] for k in range(1, 11)]
    return (
        "<h2>Multiplication is equal groups</h2>"
        "<p><b>4 %s 3</b> means 4 groups of 3. Skip count by 3s: 3, 6, 9, 12. So 4 %s 3 = 12. "
        "Turn it around and the answer stays the same: 3 %s 4 = 12 too.</p>" % (X, X, X)
        + "<figure class='sn-fig'>" + groups_svg(4, 3, 24, True)
        + "<figcaption>4 groups of 3: 3, 6, 9, 12. 4 %s 3 = 12.</figcaption></figure>" % X
        + "<h2>A trick for each fact family</h2>"
        + table(["Facts", "Trick", "Example"], [
            ["%s 3" % X, "Double, then add one more group", "3 %s 7: 14 + 7 = 21" % X],
            ["%s 4" % X, "Double, then double again", "4 %s 6: 12, 24" % X],
            ["%s 10" % X, "Count the tens; the answer ends in 0", "10 %s 6 = 60" % X],
            ["%s 5" % X, "Half of the 10s; the answer ends in 0 or 5", "5 %s 6: half of 60 = 30" % X],
        ])
        + "<figure class='sn-fig'>" + coins_svg(6, 5)
        + "<figcaption>Six 5c coins: 5, 10, 15, 20, 25, 30. 6 %s 5c = 30c.</figcaption></figure>" % X
        + table(["", "3s", "4s", "5s", "10s"], rows)
        + ex("Example", "4 %s 8 = ?" % X, "Double 8 is 16. Double 16 is 32." , "32")
        + "<h2>Every fact gives division facts</h2>"
        "<p>Division is the opposite of multiplication. 3, 7 and 21 make a <b>fact family</b>: "
        "3 %s 7 = 21, 7 %s 3 = 21, 21 ÷ 3 = 7 and 21 ÷ 7 = 3.</p>" % (X, X)
        + ex("Division", "28 ÷ 4 = ?", "Think: 4 %s ? = 28. 4 %s 7 = 28." % (X, X), "7")
        + ex("Missing number", "? %s 5 = 45" % X, "Think: 45 ÷ 5. Skip count by 5s to 45: that is 9 jumps.", "9")
        + ex("Word problem", "A tricycle has 3 wheels. How many wheels do 5 tricycles have?",
             "5 groups of 3: 3, 6, 9, 12, 15. So 5 %s 3 = 15." % X, "15 wheels")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the fact next door: 4 %s 7 = 24" % X, "Double 7 is 14, double 14 is 28"],
            ["Adding instead: 5 %s 3 = 8" % X, "%s means groups of: 5 groups of 3 = 15" % X],
            ["Skip counting one step too far: 5 %s 6 = 35" % X, "Count the jumps on your fingers: 6 jumps of 5 is 30"],
            ["Giving the big number in division: 28 ÷ 4 = 28", "Ask: 4 times what makes 28? The answer is 7"],
        ])
    )


FAQ = [
    {"q": "What multiplication facts should a Year 3 student know in Australia?",
     "a": "The Australian Curriculum (v9.0) asks Year 3 students to recall the multiplication facts for 3, 4, 5 and 10 and use them to work out the related division facts. In Year 4 this grows to all facts up to 10 × 10."},
    {"q": "Is multiplication on the Year 3 NAPLAN numeracy test?",
     "a": "Yes. The Year 3 numeracy test can include simple multiplication and division, often as short word problems. Quick recall of these facts gives students more time to think about the problem."},
    {"q": "How can I help my child learn the 3 and 4 times tables?",
     "a": "Skip count out loud, then practise a few facts each day. For the 4s, double and double again: 4 × 6 is 12, then 24. For the 3s, double the number and add one more: 3 × 7 is 14 + 7 = 21."},
    {"q": "Why learn the 5s and 10s together?",
     "a": "The 5s are half of the 10s. If your child knows 10 × 8 = 80, then 5 × 8 is half of 80, which is 40. Counting 5c and 10c coins is a good way to practise both."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(3804)
    P = People(rnd)
    sets = [set_three_four(rnd), set_five_ten(rnd), set_mixed(rnd), set_division(rnd), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "multiplication-facts-3-4-5-and-10", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication Facts for 3, 4, 5 and 10",
        "seo_title": "Year 3 Multiplication Facts Worksheets: 3, 4, 5 and 10 Times Tables with Answers",
        "short_title": "Multiplication facts: 3, 4, 5 and 10",
        "domain": "Algebra",
        "standard_code": "AC9M3A03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recall and demonstrate proficiency with multiplication facts for 3, 4, 5 and 10; extend and apply facts to develop the related division facts",
        "meta_desc": "Free Year 3 maths worksheets on the multiplication facts for 3, 4, 5 and 10: equal groups, arrays, skip counting, turnarounds, related division facts and word problems. 100 questions with an answer key, following the Australian Curriculum and useful for NAPLAN.",
        "key_big": "Double the 2s to get the 4s. Halve the 10s to get the 5s.",
        "key_sub": "For the 3s, double and add one more group: 3 × 7 = 14 + 7 = 21. Turnarounds have the same answer (4 × 7 = 7 × 4), and every fact gives a division fact: 28 ÷ 4 = 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(([5-9]|1[0-9]) equal groups|array of 4 rows with 8|[6-9] coins|10 coins)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
