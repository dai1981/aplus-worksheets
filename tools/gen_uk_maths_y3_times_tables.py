# -*- coding: utf-8 -*-
"""
UK Year 3 Maths (National Curriculum in England): the 3, 4 and 8 times tables.
  python3 tools/gen_uk_maths_y3_times_tables.py
Every product, quotient and missing number is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
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


GROUP_SHAPE = {3: (1, 3), 4: (2, 2), 8: (2, 4)}


def groups_svg(g, n, cell=20, label_sizes=False):
    """g equal groups of n counters, each group in a rounded box. Up to 4 boxes per row (3 for groups of 8)."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = 3 if n == 8 else 4
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
                 % (x, y, bw, bh, FILL, GREEN, ))
        s.append(dots(x + pad, y + pad, gr, gc, cell))
        if label_sizes:
            s.append(text(x + bw / 2, y + bh + 17, str(n), 15))
    return svg_wrap(W, H, "".join(s), "%d equal groups with %d counters in each group" % (g, n))


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
    """Strategy for a × b, where b is the times table being practised."""
    p = a * b
    if b == 3:
        return "Double %d is %d. Add one more %d: %d + %d = <b>%d</b>." % (a, 2 * a, a, 2 * a, a, p)
    if b == 4:
        return "Double %d, then double again: %d → %d → <b>%d</b>." % (a, a, 2 * a, p)
    if b == 8:
        return "4 %s %d = %d. Double it: %d + %d = <b>%d</b>." % (X, a, 4 * a, 4 * a, 4 * a, p)
    raise ValueError(b)


def rev(n):
    s = str(n)
    if len(s) == 2 and s[0] != s[1] and s[1] != "0":
        return int(s[::-1])
    return None


def fact_cands(a, b, rnd):
    """Real mistakes: neighbouring fact, one group too many/few, adding, swapped digits."""
    p = a * b
    pool = [a * (b + 1), a * (b - 1), (a + 1) * b, (a - 1) * b, a + b]
    r = rev(p)
    if r:
        pool.append(r)
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 10, p - 10, p + 2, p - 2]


def fact_q(a, b, rnd):
    """Question shows a × b or b × a; b is the table being practised."""
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
    return mcq("Count in %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e.strip())


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


def multiple_q(ask, right, wrong, table_n, inside):
    assert (right % table_n == 0) == inside and all((w % table_n == 0) != inside for w in wrong)
    lst = ", ".join(str(table_n * k) for k in range(1, 13))
    e = "The %d times table is %s. <b>%d</b> %s." % (
        table_n, lst, right, "is on the list" if inside else "is not on the list")
    return mcq(ask, right, wrong, e)


def double_q(a, small, big):
    """small × a is known; double it to find big × a (big = 2 × small)."""
    k = small * a
    ans = big * a
    assert ans == 2 * k
    wrong = [k, k + small, k + a, 4 * k]
    e = ("%d is double %d, so %d %s %d is double %d %s %d: %d + %d = <b>%d</b>."
         % (big, small, big, X, a, small, X, a, k, k, ans))
    return mcq("%d %s %d = %d. Double it to find %d %s %d." % (small, X, a, k, big, X, a), ans, wrong, e)


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    return mcq(ask, right, wrong, e)


# ============================================================ set 1: the 3 times table
def set_three(rnd):
    its = [
        count_q(groups_svg(4, 3), 4, 3, [7, 9, 15], "groups"),
        count_q(groups_svg(6, 3), 6, 3, [9, 15, 21], "groups"),
        count_q(array_svg(3, 7), 3, 7, [10, 18, 24], "array"),
        count_q(array_svg(3, 9), 3, 9, [12, 24, 30], "array"),
    ]
    for r, c in [(5, 3), (4, 3)]:
        p = r * c
        wrong = [("%d + %d" % (r, c)), ("%d %s %d" % (r, X, c + 1)), ("%d %s %d" % (r - 1, X, c))]
        e = ("There are %d rows with %d dots in each row, so it shows %d %s %d = %d. "
             "%d %s %d gives the same answer: it is the array turned on its side." % (r, c, r, X, c, p, c, X, r))
        its.append(choice_calc_q(fig(array_svg(r, c)) + "Which multiplication matches this array?", p,
                                 "%d %s %d" % (r, X, c), wrong, e))
    its.append(seq_q([9, 12, 15], 3, [17, 21, 16], "So 3 %s 6 = 18." % X))
    its.append(seq_q([21, 24, 27], 3, [29, 33, 28], "So 3 %s 10 = 30." % X))
    its.append(seq_q([27, 30, 33], 3, [35, 39, 34], "So 3 %s 12 = 36." % X))
    its += facts(3, [2, 3, 5, 6, 7, 9, 10, 11, 12], rnd)
    its.append(multiple_q("Which number is in the 3 times table?", 27, [25, 28, 32], 3, True))
    its.append(multiple_q("Which number is <b>not</b> in the 3 times table?", 20, [18, 21, 24], 3, False))
    return {"title": "The 3 times table", "items": its}


# ============================================================ set 2: the 4 times table
def set_four(rnd):
    its = [
        count_q(groups_svg(5, 4), 5, 4, [9, 16, 24], "groups"),
        count_q(groups_svg(7, 4), 7, 4, [11, 24, 32], "groups"),
    ]
    for a in (7, 9, 12):
        its.append(double_q(a, 2, 4))
    its.append(seq_q([16, 20, 24], 4, [26, 32, 30], "So 4 %s 7 = 28." % X))
    its.append(seq_q([28, 32, 36], 4, [38, 44, 39], "So 4 %s 10 = 40." % X))
    its += facts(4, [2, 3, 4, 5, 6, 7, 8, 10, 11], rnd)
    its.append(multiple_q("Which number is in the 4 times table?", 36, [34, 30, 38], 4, True))
    its.append(multiple_q("Which number is <b>not</b> in the 4 times table?", 26, [24, 28, 32], 4, False))
    its.append(choice_calc_q("Which is the same as 4 %s 6?" % X, 24, "2 %s 6 + 2 %s 6" % (X, X),
                             ["2 %s 6 + 2" % X, "4 + 6", "2 %s 6 + 6" % X],
                             "4 lots of 6 is 2 lots of 6 and 2 more lots of 6: 12 + 12 = <b>24</b>. "
                             "The 4 times table is double the 2 times table."))
    its.append(mcq("Which is the same as 4 %s 9?" % X, "double 2 %s 9" % X,
                   ["double 9", "2 %s 9 + 4" % X, "4 + 9"],
                   "4 is double 2, so 4 %s 9 is double 2 %s 9: 18 + 18 = <b>36</b>. "
                   "Double 9 is only 2 %s 9." % (X, X, X)))
    assert 2 * (2 * 9) == 36 and 2 * 9 != 36 and 2 * 9 + 4 != 36 and 4 + 9 != 36
    assert len(its) == 20, len(its)
    return {"title": "The 4 times table: double the 2s", "items": its}


# ============================================================ set 3: the 8 times table
def set_eight(rnd):
    its = [
        count_q(groups_svg(3, 8), 3, 8, [11, 16, 32], "groups"),
        count_q(groups_svg(5, 8), 5, 8, [13, 32, 48], "groups"),
    ]
    for a in (6, 3, 11):
        its.append(double_q(a, 4, 8))
    its.append(seq_q([8, 16, 24], 8, [30, 40, 28], "So 8 %s 4 = 32." % X))
    its.append(seq_q([24, 32, 40], 8, [44, 56, 50], "So 8 %s 6 = 48." % X))
    its.append(seq_q([48, 56, 64], 8, [68, 80, 70], "So 8 %s 9 = 72." % X))
    its += facts(8, [2, 4, 5, 7, 8, 9, 10, 12], rnd)
    its.append(choice_calc_q("Which gives the answer to 8 %s 7?" % X, 56, "4 %s 7 + 4 %s 7" % (X, X),
                             ["4 %s 7 + 4" % X, "2 %s 7 + 2 %s 7" % (X, X), "8 + 7"],
                             "8 is double 4, so 8 %s 7 is double 4 %s 7: 28 + 28 = <b>56</b>. "
                             "2 %s 7 + 2 %s 7 is only 4 %s 7." % (X, X, X, X, X)))
    its.append(multiple_q("Which number is in the 8 times table?", 56, [54, 58, 46], 8, True))
    its.append(multiple_q("Which number is <b>not</b> in the 8 times table?", 36, [32, 40, 48], 8, False))
    its.append(mcq("Which number is in the 4 times table but <b>not</b> in the 8 times table?", 28, [24, 32, 16],
                   "4 %s 7 = <b>28</b>, but the 8 times table goes 24, 32: it jumps over 28. "
                   "24 = 8 %s 3, 32 = 8 %s 4 and 16 = 8 %s 2. Every number in the 8 times table is also in the 4 times table."
                   % (X, X, X, X)))
    assert 28 % 4 == 0 and 28 % 8 and all(v % 8 == 0 for v in (24, 32, 16))
    assert len(its) == 20, len(its)
    return {"title": "The 8 times table: double the 4s", "items": its}


# ============================================================ set 4: division and missing numbers
def set_division(rnd):
    its = []
    for d, q in [(3, 7), (4, 9), (8, 6), (3, 9), (8, 4), (4, 12), (8, 9), (3, 11)]:
        p = d * q
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, p, p - d, d], e))
    for a, b in [(3, 6), (8, 7), (4, 8)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, p], e))
    for a, b in [(9, 3), (5, 8), (11, 4)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [a + 1, a - 1, p - b, p], e))
    for g, n in [(5, 4), (3, 8)]:
        p = g * n
        e = "Count the groups: there are %d groups of %d. %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d." % (
            g, n, p, n, g, g, X, n, p)
        its.append(mcq(fig(groups_svg(g, n)) + "%d counters are put into groups of %d. How many groups are there?" % (p, n),
                       g, [g + 1, g - 1, p - n, p], e))
    for d, q in [(4, 6), (8, 3)]:
        p = d * q
        e = "Use the inverse: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d." % (q, X, d, p, p, d, q)
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, q - d, p + d, p - d], e))
    for a, b in [(3, 8), (4, 7)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, a, b)
        wrong = ["%d ÷ %d = %d" % (b, a, p), "%d ÷ %d = %d" % (p, b, a + 1), "%d ÷ %d = %d" % (p, a, b - 1)]
        assert p / a == b and all(int(w.split(" = ")[1]) != calc(w.split(" = ")[0]) for w in wrong)
        e = ("%d %s %d = %d, so %d ÷ %d = %d and %d ÷ %d = %d. "
             "Division starts with the biggest number, %d." % (a, X, b, p, p, a, b, p, b, a, p))
        e = e.replace("so %d ÷ %d = %d" % (p, a, b), "so <b>%d ÷ %d = %d</b>" % (p, a, b))
        its.append(mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Division facts and missing numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        u = (lambda v: "%d%s" % (v, unit)) if unit == "p" else (lambda v: "%d %s" % (v, unit))
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    nm, he, his = P.next()
    w("A tricycle has 3 wheels. %s sees 6 tricycles in the playground. How many wheels is that?" % nm, 18, "wheels",
      [9, 15, 21], "6 tricycles with 3 wheels each: 6 %s 3 = <b>18</b>. 9 is 6 + 3, which adds instead of multiplies." % X, 6 * 3)
    nm, he, his = P.next()
    w("A spider has 8 legs. %s finds 5 spiders in the garden. How many legs is that altogether?" % nm, 40, "legs",
      [13, 32, 48], "5 %s 8 = <b>40</b>. 32 is only 4 spiders." % X, 5 * 8)
    nm, he, his = P.next()
    w("Yoghurts come in packs of 4. %s buys 7 packs. How many yoghurts is that?" % nm, 28, "yoghurts",
      [11, 24, 32], "7 packs of 4: 7 %s 4 = <b>28</b>. Double 7 is 14, double 14 is 28." % X, 7 * 4)
    w("In a classroom, 3 children sit at each table. There are 9 tables. How many children are there?", 27, "children",
      [12, 24, 30], "9 tables of 3: 9 %s 3 = <b>27</b>. 24 is only 8 tables." % X, 9 * 3)
    w("A car has 4 wheels. There are 8 cars in the car park. How many wheels is that?", 32, "wheels",
      [12, 28, 36], "8 %s 4 = <b>32</b>. Double 8 is 16, double 16 is 32." % X, 8 * 4)
    w("An octopus has 8 arms. There are 3 octopuses at the aquarium. How many arms is that?", 24, "arms",
      [11, 16, 32], "3 %s 8 = <b>24</b>. 11 is 3 + 8, which adds instead of multiplies." % X, 3 * 8)
    w("A chair has 4 legs. How many legs do 9 chairs have?", 36, "legs",
      [13, 32, 40], "9 %s 4 = <b>36</b>. Double 9 is 18, double 18 is 36." % X, 9 * 4)
    nm, he, his = P.next()
    w("A football team gets 3 points for a win. The team wins 7 games. How many points is that?", 21, "points",
      [10, 18, 24], "7 wins with 3 points each: 7 %s 3 = <b>21</b>." % X, 7 * 3)
    nm, he, his = P.next()
    w("Pencils come in packs of 8. %s’s teacher buys 6 packs. How many pencils is that?" % nm, 48, "pencils",
      [14, 40, 56], "6 %s 8: 6 %s 4 = 24, double 24 is <b>48</b>." % (X, X), 6 * 8)
    nm, he, his = P.next()
    w("Stickers cost 3p each. %s buys 8 stickers. How much does %s spend?" % (nm, he), 24, "p",
      [11, 21, 27], "8 %s 3p = <b>24p</b>. 11p is 8 + 3, which adds instead of multiplies." % X, 8 * 3)
    w("There are 21 wheels on some tricycles. How many tricycles are there?", 7, "tricycles",
      [6, 8, 21], "Each tricycle has 3 wheels. 21 ÷ 3 = ? 3 %s 7 = 21, so there are <b>7 tricycles</b>." % X, 21 // 3)
    w("32 pupils get into teams of 4 for PE. How many teams are there?", 8, "teams",
      [7, 28, 9], "32 ÷ 4 = ? Think 4 %s ? = 32. 4 %s 8 = 32, so there are <b>8 teams</b>." % (X, X), 32 // 4)
    nm, he, his = P.next()
    w("%s shares 24 cupcakes equally onto 3 plates. How many cupcakes go on each plate?" % nm, 8, "cupcakes",
      [7, 21, 9], "24 ÷ 3 = ? 3 %s 8 = 24, so each plate has <b>8 cupcakes</b>." % X, 24 // 3)
    w("Some spiders have 56 legs altogether. Each spider has 8 legs. How many spiders are there?", 7, "spiders",
      [6, 48, 8], "56 ÷ 8 = ? 8 %s 7 = 56, so there are <b>7 spiders</b>." % X, 56 // 8)
    w("36 chairs are put in rows of 4 in the school hall. How many rows are there?", 9, "rows",
      [8, 32, 10], "36 ÷ 4 = ? 4 %s 9 = 36, so there are <b>9 rows</b>." % X, 36 // 4)
    nm, he, his = P.next()
    w("Sweets cost 8p each. %s has 40p. How many sweets can %s buy?" % (nm, he), 5, "sweets",
      [4, 32, 6], "40 ÷ 8 = ? 8 %s 5 = 40, so %s can buy <b>5 sweets</b>." % (X, he), 40 // 8)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s has 4 marbles. %s has 3 times as many. How many marbles does %s have?" % (nm, nm2, nm2), 12, "marbles",
      [7, 8, 16], "3 times as many as 4 means 3 %s 4 = <b>12</b>. 7 is 3 + 4, which adds instead of multiplies." % X, 3 * 4)
    w("There are 4 bikes and 3 tricycles in the bike shed. How many wheels is that altogether?", 17, "wheels",
      [7, 14, 21], "Bikes have 2 wheels: 4 %s 2 = 8. Tricycles have 3 wheels: 3 %s 3 = 9. 8 + 9 = <b>17</b>." % (X, X),
      4 * 2 + 3 * 3)
    nm, he, his = P.next()
    w("%s buys 3 packs of 4 yoghurts. %s eats 2 of them. How many yoghurts are left?" % (nm, he.capitalize()), 10, "yoghurts",
      [12, 5, 14], "3 %s 4 = 12. Then 12 − 2 = <b>10</b>. 12 forgets the 2 that were eaten." % X, 3 * 4 - 2)
    w("Hot cross buns come in packs of 4. How many packs are needed for 12 children to have one each?", 3, "packs",
      [2, 4, 12], "12 ÷ 4 = ? 4 %s 3 = 12, so <b>3 packs</b> are needed." % X, 12 // 4)
    assert len(its) == 20
    return {"title": "Times tables word problems", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k), "%d %s 3 = %d" % (k, X, 3 * k), "%d %s 4 = %d" % (k, X, 4 * k), "%d %s 8 = %d" % (k, X, 8 * k)]
            for k in range(1, 13)]
    return (
        "<h2>Multiplication is equal groups</h2>"
        "<p><b>4 %s 3</b> means 4 groups of 3. Count in 3s: 3, 6, 9, 12. So 4 %s 3 = 12. "
        "You can also turn it round: 3 %s 4 = 12 too.</p>" % (X, X, X)
        + "<figure class='sn-fig'>" + groups_svg(4, 3, 24, True)
        + "<figcaption>4 groups of 3: 3, 6, 9, 12. 4 %s 3 = 12.</figcaption></figure>" % X
        + "<h2>Use doubling</h2>"
        "<p>The 3 times table is the 2 times table plus one more group. "
        "The 4 times table is <b>double the 2s</b>. The 8 times table is <b>double the 4s</b>.</p>"
        + table(["Table", "Trick", "Example"], [
            ["%s 3" % X, "Double, then add one more", "3 %s 7: 14 + 7 = 21" % X],
            ["%s 4" % X, "Double, then double again", "4 %s 6: 12, 24" % X],
            ["%s 8" % X, "Double the 4 times table", "8 %s 6: 24 + 24 = 48" % X],
        ])
        + "<figure class='sn-fig'>" + groups_svg(2, 8, 20, True)
        + "<figcaption>2 groups of 8 make 16. That is double 2 groups of 4: 8 + 8 = 16.</figcaption></figure>"
        + table(["", "3 times table", "4 times table", "8 times table"], rows)
        + ex("Example", "8 %s 7 = ?" % X, "4 %s 7 = 28. 8 is double 4, so double 28: 28 + 28 = 56." % X, "56")
        + ex("Division", "24 ÷ 8 = ?", "Division is the inverse of multiplication. Think: 8 %s ? = 24. 8 %s 3 = 24." % (X, X), "3")
        + ex("Word problem", "A spider has 8 legs. How many legs do 4 spiders have?",
             "4 lots of 8: 8, 16, 24, 32. So 4 %s 8 = 32." % X, "32 legs")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up a neighbouring fact: 8 %s 7 = 48" % X, "Double 4 %s 7: 28 + 28 = 56" % X],
            ["Adding instead: 4 %s 3 = 7" % X, "%s means groups of: 4 groups of 3 = 12" % X],
            ["One group too few: 6 %s 3 = 15" % X, "Count the groups: 3, 6, 9, 12, 15, 18"],
            ["Giving the big number in division: 24 ÷ 8 = 24", "Ask: 8 times what makes 24? The answer is 3"],
        ])
    )


FAQ = [
    {"q": "What times tables should a Year 3 child know?",
     "a": "The 3, 4 and 8 times tables, as well as the 2, 5 and 10 times tables from Year 2. The National Curriculum says pupils should know the multiplication and division facts for each one."},
    {"q": "Why are the 4 and 8 times tables taught together?",
     "a": "Because the 8 times table is double the 4 times table, and the 4 times table is double the 2s. If a child knows 4 × 7 = 28, they can double it to get 8 × 7 = 56."},
    {"q": "How can I help my child learn the 3 times table?",
     "a": "Count in 3s out loud, then practise a few facts each day. A quick trick: 3 × 7 is double 7 (14) plus one more 7, which makes 21."},
    {"q": "When do children take the Multiplication Tables Check?",
     "a": "In June of Year 4. Learning the 3, 4 and 8 times tables well in Year 3 is the best start for it, because the check covers every table up to 12 × 12."},
]


def mark_large(u, pattern):
    """Tag wide pictures (many groups) so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(3304)
    P = People(rnd)
    sets = [set_three(rnd), set_four(rnd), set_eight(rnd), set_division(rnd), set_words(P)]
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
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "3-4-and-8-times-tables", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "The 3, 4 and 8 Times Tables",
        "seo_title": "Year 3 Times Tables Worksheets: 3, 4 and 8 Times Tables with Answers",
        "short_title": "3, 4 and 8 times tables",
        "domain": "Multiplication and division",
        "standard_code": "Year 3: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recall and use multiplication and division facts for the 3, 4 and 8 multiplication tables.",
        "meta_desc": "Free Year 3 maths worksheets on the 3, 4 and 8 times tables: equal groups, counting in 3s, 4s and 8s, doubling tricks, division facts and word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Double the 2s to get the 4s. Double the 4s to get the 8s.",
        "key_sub": "4 × 7 = 28, so 8 × 7 = 28 + 28 = 56. For the 3s, double the number and add one more: 3 × 6 = 12 + 6 = 18. Every fact also gives a division fact: 56 ÷ 8 = 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(([5-9]|1[0-9]) equal groups|array of 3 rows)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
