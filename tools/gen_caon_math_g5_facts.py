# -*- coding: utf-8 -*-
"""
CA Grade 5 Math (Ontario Mathematics Curriculum 2020, B2.2): multiplication facts from 0 x 0 to 12 x 12
and the related division facts.
  python3 tools/gen_caon_math_g5_facts.py
Sets: 11s and 12s, facts with 0 and 1, strategies (12 x 7 = 10 x 7 + 2 x 7), related division facts,
mixed facts and word problems (eggs by the dozen).
Wrong answers come from real mistakes: 0 x n = n, 0 x n = n0 (mixing up 0 and 10), n x 1 = n + 1,
12 x 8 = 86 (80 + 16 added without the carried ten), 10 x n + 2 (forgetting to multiply the 2),
11 x 12 = 1212, the fact next door, and turning division around.
Every product, quotient and missing number is checked in code.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
FILL2 = "#fbe3c4"
EDGE2 = "#b86e12"
INK = "#2b2b2b"
EGG = "#fffaf0"
EGG_EDGE = "#a08a6a"
CARTON = "#d8cdb8"
CARTON_EDGE = "#8a7b62"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
X = "×"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^\$?0\d", c):
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


def array_svg(rows, cols, cell=22):
    o = 6
    s = "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                % (o + c * cell + cell // 2, o + r * cell + cell // 2, cell // 3, GREEN)
                for r in range(rows) for c in range(cols))
    return svg_wrap(cols * cell + 2 * o, rows * cell + 2 * o, s,
                    "array of %d rows with %d dots in each row" % (rows, cols))


def area_svg(n, cell=18):
    """Grid of n rows and 12 columns, split into a 10-column part and a 2-column part."""
    lx, ty = 30, 26
    W = lx + 12 * cell + 10
    H = ty + n * cell + 6
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (lx, ty, 10 * cell, n * cell, FILL),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (lx + 10 * cell, ty, 2 * cell, n * cell, FILL2)]
    for c in range(13):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#9ab' stroke-width='1'/>"
                 % (lx + c * cell, ty, lx + c * cell, ty + n * cell))
    for r in range(n + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#9ab' stroke-width='1'/>"
                 % (lx, ty + r * cell, lx + 12 * cell, ty + r * cell))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (lx, ty, 10 * cell, n * cell, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (lx + 10 * cell, ty, 2 * cell, n * cell, EDGE2))
    s.append(text(lx + 5 * cell, ty - 8, "10", 16, col=GREEN))
    s.append(text(lx + 11 * cell, ty - 8, "2", 16, col=EDGE2))
    s.append(text(lx - 10, ty + n * cell / 2 + 6, str(n), 16))
    return svg_wrap(W, H, "".join(s), "grid of %d rows and 12 columns split into 10 columns and 2 columns" % n)


def cartons_svg(k):
    """k egg cartons, each with 2 rows of 6 eggs (1 dozen)."""
    cell, pad, gap = 24, 6, 12
    cw, ch = 6 * cell + 2 * pad, 2 * cell + 2 * pad
    per_row = 2 if k > 1 else 1
    nrows = (k + per_row - 1) // per_row
    W = per_row * cw + (per_row - 1) * gap + 4
    H = nrows * ch + (nrows - 1) * gap + 4
    s = []
    for i in range(k):
        r, c = divmod(i, per_row)
        x = 2 + c * (cw + gap)
        y = 2 + r * (ch + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, cw, ch, CARTON, CARTON_EDGE))
        for er in range(2):
            for ec in range(6):
                s.append("<ellipse cx='%d' cy='%d' rx='9' ry='10.5' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x + pad + ec * cell + cell // 2, y + pad + er * cell + cell // 2, EGG, EGG_EDGE))
    lab = "%d egg cartons with 12 eggs in each" % k if k > 1 else "1 egg carton with 12 eggs"
    return svg_wrap(W, H, "".join(s), lab)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def calc(expr):
    """Evaluate a short expression written with × and ÷ (digits, spaces and + − × ÷ only)."""
    assert re.fullmatch(r"[0-9 +×÷−]+", expr), expr
    return eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-"))


def ok_sentence(s):
    lhs, rhs = s.split(" = ")
    return calc(lhs) == int(rhs)


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    vals = [calc(w) for w in wrong]
    assert len(set(vals)) == len(vals), (ask, wrong)
    return mcq(ask, right, wrong, e)


def true_sentence_q(ask, right, wrong, e, want=True):
    assert ok_sentence(right) == want and all(ok_sentence(w) != want for w in wrong), (right, wrong)
    return mcq(ask, right, wrong, e)


def num_q(q, ans, check, wrong, e):
    assert ans == check, (q, ans, check)
    assert ans not in wrong, (q, wrong)
    return mcq(q, ans, wrong, e)


# ------------------------------------------------------------ 11s and 12s
def tip12(n):
    p = 12 * n
    return "12 %s %d = 10 %s %d + 2 %s %d = %d + %d = <b>%d</b>." % (X, n, X, n, X, n, 10 * n, 2 * n, p)


def tip11(n):
    p = 11 * n
    return "11 %s %d = 10 %s %d + %d = %d + %d = <b>%d</b>." % (X, n, X, n, n, 10 * n, n, p)


def cands12(n):
    p = 12 * n
    if n == 12:
        return [132, 134, 124]
    pool = []
    if 2 * n >= 10:
        pool.append(p - 10)        # 12 × 8 = 86: the carried ten is lost
    pool += [10 * n + 2, 11 * n, 12 * (n + 1), n + 12]
    return [v for v in pool if v != p]


def cands11(n):
    if n == 10:
        return [1010, 100, 111]
    if n == 11:
        return [111, 122, 132]
    if n == 12:
        return [1212, 122, 121]
    return [11 * (n + 1), 11 * (n - 1), 10 * n, n + 11]


def fact12(n, rnd):
    x, y = (12, n) if rnd.random() < 0.5 else (n, 12)
    e = tip12(n)
    if 2 * n > 10 and n != 12:
        e += " Do not lose the ten: %d + %d is %d, not %d." % (10 * n, 2 * n, 12 * n, 12 * n - 10)
    return mcq("%d %s %d = ?" % (x, X, y), 12 * n, cands12(n), e)


def fact11(n, rnd):
    x, y = (11, n) if rnd.random() < 0.5 else (n, 11)
    e = tip11(n)
    if n == 12:
        e += " 1212 just writes 12 twice; that pattern only works up to 11 %s 9." % X
    elif n <= 9:
        e += " For 11 %s 1 to 11 %s 9, the digit is written twice." % (X, X)
    return mcq("%d %s %d = ?" % (x, X, y), 11 * n, cands11(n), e)


# ============================================================ set 1: 11s and 12s
def set_11_12(rnd):
    its = [
        num_q(fig(array_svg(3, 12)) + "How many dots are in this array?", 36, 3 * 12, [15, 33, 24],
              "There are 3 rows with 12 dots in each row. 3 %s 12 = 30 + 6 = <b>36</b>. "
              "15 is 3 + 12, which adds instead of multiplies." % X),
        num_q(fig(array_svg(2, 11)) + "How many dots are in this array?", 22, 2 * 11, [13, 24, 20],
              "There are 2 rows with 11 dots in each row. 2 %s 11 = <b>22</b>. 13 is 2 + 11." % X),
        num_q("Skip count by 12s. What comes next?<br>12, 24, 36, 48, ?", 60, 48 + 12, [58, 50, 72],
              "Each number is 12 more than the one before: 48 + 12 = <b>60</b>. So 12 %s 5 = 60." % X),
        num_q("Skip count by 11s. What comes next?<br>11, 22, 33, 44, ?", 55, 44 + 11, [54, 45, 66],
              "Each number is 11 more than the one before: 44 + 11 = <b>55</b>. So 11 %s 5 = 55." % X),
    ]
    a = [4, 5, 6, 7, 8, 9, 12]
    rnd.shuffle(a)
    its += [fact12(n, rnd) for n in a]
    b = [3, 6, 8, 9, 10, 11, 12]
    rnd.shuffle(b)
    its += [fact11(n, rnd) for n in b]
    right, wrong = 84, [74, 86, 94]
    assert right % 12 == 0 and all(w % 12 for w in wrong)
    its.append(mcq("Which number is in the 12s?", right, wrong,
                   "Skip count by 12s: 12, 24, 36, 48, 60, 72, <b>84</b>, 96. 84 = 12 %s 7. "
                   "74 and 86 come from adding 70 + 14 or 80 + 16 wrong." % X))
    right, wrong = 99, [98, 101, 111]
    assert right % 11 == 0 and all(w % 11 for w in wrong)
    its.append(mcq("Which number is in the 11s?", right, wrong,
                   "<b>99</b> = 11 %s 9. 111 is not in the 11s: 11 %s 10 = 110 and 11 %s 11 = 121." % (X, X, X)))
    assert len(its) == 20, len(its)
    return {"title": "The 11s and 12s", "items": its}


# ============================================================ set 2: facts with 0 and 1
def set_0_1(rnd):
    its = []
    for x, y in [(9, 0), (0, 12), (6, 0), (10, 0)]:
        k = x or y
        e = ("%d %s %d means %s. That is <b>0</b>. The answer is not %d: any number times 0 is 0."
             % (x, X, y, "%d groups of 0" % k if y == 0 else "0 groups of %d" % k, k))
        e += " %d is %d %s 10, not %d %s 0." % (k * 10, k, X, k, X)
        its.append(num_q("%d %s %d = ?" % (x, X, y), 0, x * y, [k, 1, k * 10], e))
    for x, y in [(1, 8), (11, 1), (1, 12), (7, 1)]:
        k = max(x, y)
        e = ("%d %s %d means %s. That is <b>%d</b>. Times 1 keeps the number the same; it does not add 1."
             % (x, X, y, "1 group of %d" % k if x == 1 else "%d groups of 1" % k, k))
        its.append(num_q("%d %s %d = ?" % (x, X, y), k, x * y, [k + 1, 1, 0], e))
    its.append(mcq("Any number times 0 equals ___.", "0", ["the same number", "1", "the number with a 0 after it"],
                   "No groups, or groups with nothing in them, make <b>0</b>. 7 %s 0 = 0 and 0 %s 12 = 0. "
                   "Putting a 0 after the number is the rule for %s 10." % (X, X, X)))
    its.append(mcq("Any number times 1 equals ___.", "the same number", ["1", "0", "the number plus 1"],
                   "One group of a number is just that number, so the answer is <b>the same number</b>. "
                   "9 %s 1 = 9 and 1 %s 12 = 12." % (X, X)))
    its.append(num_q("? %s 9 = 9" % X, 1, 9 // 9, [0, 9, 10],
                     "1 group of 9 is 9, so ? = <b>1</b>. 9 %s 9 = 81 and 0 %s 9 = 0." % (X, X)))
    its.append(num_q("? %s 11 = 0" % X, 0, 0, [1, 11, 10],
                     "Only 0 times a number makes 0, so ? = <b>0</b>. 1 %s 11 = 11, not 0." % X))
    its.append(num_q("9 ÷ 1 = ?", 9, 9 // 1, [1, 0, 10],
                     "Put 9 into groups of 1: there are 9 groups. 9 ÷ 1 = <b>9</b>. Check: 1 %s 9 = 9." % X))
    its.append(num_q("7 ÷ 7 = ?", 1, 7 // 7, [7, 0, 49],
                     "7 shared into groups of 7 makes 1 group. 7 ÷ 7 = <b>1</b>. Check: 7 %s 1 = 7. "
                     "49 is 7 %s 7, which multiplies instead of divides." % (X, X)))
    its.append(num_q("12 ÷ 12 = ?", 1, 12 // 12, [12, 0, 144],
                     "Any number (not 0) divided by itself is <b>1</b>. Check: 12 %s 1 = 12. 144 is 12 %s 12." % (X, X)))
    its.append(true_sentence_q("Which number sentence is true?", "0 ÷ 8 = 0", ["0 ÷ 8 = 8", "8 ÷ 8 = 0", "8 %s 0 = 8" % X],
                               "0 shared among 8 groups gives 0 in each group, so <b>0 ÷ 8 = 0</b>. "
                               "8 ÷ 8 = 1 and 8 %s 0 = 0." % X))
    its.append(true_sentence_q("Which number sentence is <b>not</b> true?", "6 %s 0 = 6" % X,
                               ["6 %s 1 = 6" % X, "6 ÷ 6 = 1", "0 ÷ 6 = 0"],
                               "<b>6 %s 0 = 6</b> is wrong: 6 groups of 0 is 0, so 6 %s 0 = 0. The other three are true."
                               % (X, X), want=False))
    its.append(choice_calc_q("Which has the answer 0?", 0, "12 %s 0" % X, ["12 %s 1" % X, "1 %s 1" % X, "7 + 0"],
                             "<b>12 %s 0</b> = 0. 12 %s 1 = 12, 1 %s 1 = 1 and 7 + 0 = 7. "
                             "Adding 0 keeps the number, but multiplying by 0 gives 0." % (X, X, X)))
    nm, he, his = rnd.choice(GIRLS), "she", "her"
    its.append(num_q("%s puts 1 granola bar in each of 11 lunch bags. How many granola bars does %s use?" % (nm, he),
                     11, 11 * 1, [12, 1, 0],
                     "11 bags with 1 bar in each: 11 %s 1 = <b>11</b>. 12 adds 1 instead of multiplying." % X))
    its.append(num_q("Owen stacks 7 empty egg cartons. How many eggs are in the cartons?", 0, 7 * 0, [7, 1, 84],
                     "The cartons are empty: 7 groups of 0 eggs. 7 %s 0 = <b>0</b>. 84 is 7 %s 12, "
                     "the number of eggs if the cartons were full." % (X, X)))
    assert len(its) == 20, len(its)
    return {"title": "Facts with 0 and 1", "items": its}


# ============================================================ set 3: strategies
def set_strategies(rnd):
    its = []
    for n in [3, 4, 9, 11]:
        p = 12 * n
        e = "12 is 10 + 2, so 12 %s %d = %d + %d = <b>%d</b>." % (X, n, 10 * n, 2 * n, p)
        wrong = [10 * n + 2, p - 10, 11 * n, 12 * (n + 1)]
        if 2 * n < 10:
            wrong.remove(p - 10)
        e += " %d forgets to multiply the 2." % (10 * n + 2)
        its.append(num_q("10 %s %d = %d and 2 %s %d = %d. What is 12 %s %d?" % (X, n, 10 * n, X, n, 2 * n, X, n),
                         p, 10 * n + 2 * n, wrong, e))
    for n in [5, 6]:
        p = 12 * n
        e = ("The green part is 10 %s %d = %d. The orange part is 2 %s %d = %d. "
             "Together: %d + %d = <b>%d</b>, so 12 %s %d = %d." % (X, n, 10 * n, X, n, 2 * n, 10 * n, 2 * n, p, X, n, p))
        its.append(num_q(fig(area_svg(n)) + "The grid shows 12 %s %d split into 10 %s %d and 2 %s %d. What is 12 %s %d?"
                         % (X, n, X, n, X, n, X, n), p, 10 * n + 2 * n, [p - 10, 10 * n + 2, 11 * n, 12 * (n + 1)], e))
    for n, wrong in [(7, ["10 %s 7 + 2" % X, "10 %s 7 + 7" % X, "10 %s 2 + 7" % X]),
                     (8, ["10 %s 8 + 2" % X, "10 + 2 %s 8" % X, "12 %s 10 + 8" % X])]:
        right = "10 %s %d + 2 %s %d" % (X, n, X, n)
        its.append(choice_calc_q("Which is a correct way to work out 12 %s %d?" % (X, n), 12 * n, right, wrong,
                                 "Split 12 into 10 and 2 and multiply <b>both</b> parts by %d: "
                                 "<b>%s</b> = %d + %d = %d." % (n, right, 10 * n, 2 * n, 12 * n)))
    its.append(choice_calc_q("Which has the same answer as 12 %s 9?" % X, 108, "6 %s 9 + 6 %s 9" % (X, X),
                             ["12 + 9", "6 %s 9 + 2" % X, "10 %s 9 + 9" % X],
                             "12 is double 6, so 12 %s 9 is double 6 %s 9: <b>6 %s 9 + 6 %s 9</b> = 54 + 54 = 108."
                             % (X, X, X, X)))
    for a, wrong, note in [(7, [44, 74, 48], "74 loses the carried ten."),
                           (8, [50, 86, 54], "86 loses the carried ten.")]:
        b, p = 6 * a, 12 * a
        its.append(num_q("6 %s %d = %d. Use it to find 12 %s %d." % (X, a, b, X, a), p, 2 * b, wrong,
                         "12 is double 6, so 12 %s %d is double %d: %d + %d = <b>%d</b>. %s" % (X, a, b, b, b, p, note)))
    its.append(num_q("Ava works out 12 %s 8 like this: 10 %s 8 = 80 and 2 %s 8 = 16, so 12 %s 8 = 86. "
                     "What is the correct answer?" % (X, X, X, X), 96, 80 + 16, [86, 88, 82],
                     "Her steps are right, but 80 + 16 = <b>96</b>. 86 forgets the ten in 16."))
    for n, wrong in [(12, [112, 122, 1212]), (8, [80, 89, 98])]:
        p = 11 * n
        its.append(num_q("11 %s %d = 10 %s %d + 1 %s %d. What is 11 %s %d?" % (X, n, X, n, X, n, X, n), p, 10 * n + n, wrong,
                         "10 %s %d = %d and 1 %s %d = %d. %d + %d = <b>%d</b>." % (X, n, 10 * n, X, n, n, 10 * n, n, p)))
    for n, wrong in [(7, [69, 73, 56]), (8, [79, 82, 64])]:
        p = 9 * n
        its.append(num_q("10 %s %d = %d. Use it to find 9 %s %d." % (X, n, 10 * n, X, n), p, 10 * n - n, wrong,
                         "9 %s %d is one group of %d less than 10 %s %d: %d − %d = <b>%d</b>. "
                         "%d takes away 1 instead of %d." % (X, n, n, X, n, 10 * n, n, p, 10 * n - 1, n)))
    its.append(num_q("4 %s 7 = 28. Use it to find 8 %s 7." % (X, X), 56, 2 * 28, [30, 46, 35],
                     "8 is double 4, so 8 %s 7 is double 28: 28 + 28 = <b>56</b>. 46 loses the carried ten." % X))
    its.append(num_q("7 %s 6 = 5 %s 6 + 2 %s 6. What is 7 %s 6?" % (X, X, X, X), 42, 5 * 6 + 2 * 6, [32, 36, 48],
                     "5 %s 6 = 30 and 2 %s 6 = 12. 30 + 12 = <b>42</b>. 32 adds 2 instead of 2 %s 6." % (X, X, X)))
    its.append(num_q("11 %s 7 = 10 %s 7 + ?" % (X, X), 7, 11 * 7 - 10 * 7, [1, 11, 70],
                     "11 groups of 7 is 10 groups of 7 and 1 more group of 7. So ? = <b>7</b>: 70 + 7 = 77."))
    its.append(num_q("12 %s 8 = 10 %s 8 + ?" % (X, X), 16, 12 * 8 - 10 * 8, [2, 8, 12],
                     "12 groups of 8 is 10 groups of 8 and 2 more groups of 8. So ? = 2 %s 8 = <b>16</b>. "
                     "2 forgets to multiply by 8." % X))
    assert len(its) == 20, len(its)
    return {"title": "Strategies: 12 × 7 = 10 × 7 + 2 × 7", "items": its}


# ============================================================ set 4: related division facts
def div_q(p, d, rnd):
    q = p // d
    assert q * d == p and 1 <= q <= 12
    wrong = [q + 1, q - 1, q + 2]
    e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
    if d == 12 and q >= 5:
        e += " Check: 10 %s %d + 2 %s %d = %d + %d = %d." % (X, q, X, q, 10 * q, 2 * q, p)
    return mcq("%d ÷ %d = ?" % (p, d), q, wrong, e)


def set_division(rnd):
    its = []
    for p, d in [(36, 12), (60, 12), (77, 11), (96, 12), (99, 11), (84, 12), (56, 8), (63, 9),
                 (108, 12), (72, 8), (121, 11), (144, 12)]:
        its.append(div_q(p, d, rnd))
    its.append(num_q("12 %s ? = 108" % X, 9, 108 // 12, [8, 10, 96],
                     "Ask: 12 times what makes 108? 108 ÷ 12 = 9. Check: 12 %s 9 = 108, so ? = <b>9</b>. "
                     "96 is 108 − 12, which subtracts instead of divides." % X))
    its.append(num_q("? %s 11 = 132" % X, 12, 132 // 11, [11, 13, 121],
                     "Ask: what times 11 makes 132? 132 ÷ 11 = 12. Check: 12 %s 11 = 120 + 12 = 132, so ? = <b>12</b>." % X))
    its.append(num_q("? ÷ 12 = 6", 72, 12 * 6, [18, 2, 84],
                     "Use the related multiplication fact: ? = 12 %s 6 = <b>72</b>. Check: 72 ÷ 12 = 6. "
                     "18 is 12 + 6 and 2 is 12 ÷ 6." % X))
    its.append(true_sentence_q("12 %s 7 = 84. Which division fact is also true?" % X, "84 ÷ 7 = 12",
                               ["7 ÷ 84 = 12", "84 ÷ 12 = 8", "84 ÷ 7 = 11"],
                               "7, 12 and 84 make a fact family: 12 %s 7 = 84, so <b>84 ÷ 7 = 12</b> and 84 ÷ 12 = 7. "
                               "Division starts with the biggest number, 84." % X))
    its.append(mcq("Which fact helps you work out 108 ÷ 12?", "12 %s 9 = 108" % X,
                   ["12 %s 8 = 96" % X, "108 − 12 = 96", "108 + 12 = 120"],
                   "108 ÷ 12 asks: 12 times what makes 108? <b>12 %s 9 = 108</b>, so 108 ÷ 12 = 9." % X))
    assert 12 * 9 == 108 and 12 * 8 == 96
    fam = ["11 %s 12 = 132" % X, "132 ÷ 11 = 12", "132 ÷ 12 = 11"]
    assert all(ok_sentence(f) for f in fam)
    its.append(true_sentence_q("Which fact is <b>not</b> in the fact family for 11, 12 and 132?", "12 ÷ 11 = 132", fam,
                               "<b>12 ÷ 11 = 132</b> is turned around. A division fact starts with the biggest number: "
                               "132 ÷ 11 = 12.", want=False))
    its.append(num_q("132 ÷ 11 = 12. So what is 132 ÷ 12?", 11, 132 // 12, [12, 10, 121],
                     "11 %s 12 = 132, so 132 ÷ 11 = 12 and 132 ÷ 12 = <b>11</b>. They are in the same fact family." % X))
    its.append(num_q("8 %s 9 = 72. So what is 72 ÷ 9?" % X, 8, 72 // 9, [9, 7, 63],
                     "8 %s 9 = 72, so 72 ÷ 9 = <b>8</b> and 72 ÷ 8 = 9. 63 is 7 %s 9." % (X, X)))
    assert len(its) == 20, len(its)
    return {"title": "Related division facts", "items": its}


# ============================================================ set 5: mixed facts and word problems
def set_words(P, rnd):
    its = []
    for a, b, wrong, e in [
        (7, 8, [54, 63, 15], "7 %s 8 = <b>56</b>. Say it as 5, 6, 7, 8: 56 = 7 %s 8. 54 is 6 %s 9." % (X, X, X)),
        (6, 9, [56, 45, 63], "6 %s 9 = <b>54</b>. 10 %s 6 = 60, and 60 − 6 = 54. 56 is 7 %s 8." % (X, X, X)),
        (9, 12, [98, 96, 118], "12 %s 9 = 90 + 18 = <b>108</b>. 98 loses the carried ten." % X),
        (9, 7, [56, 72, 64], "9 %s 7 = 70 − 7 = <b>63</b>. 56 is 8 %s 7 and 72 is 9 %s 8." % (X, X, X)),
    ]:
        its.append(num_q("%d %s %d = ?" % (a, X, b), a * b, a * b, wrong, e))

    def w(q, ans, unit, check, wrong, e):
        assert ans == check, (q, ans, check)
        assert ans not in wrong
        u = (lambda v: "$%d" % v) if unit == "$" else (lambda v: "%d %s" % (v, unit))
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    w(fig(cartons_svg(3)) + "Each carton holds 12 eggs. How many eggs are there?", 36, "eggs", 3 * 12, [15, 33, 24],
      "3 cartons of 12: 3 %s 12 = 30 + 6 = <b>36</b>. 15 is 3 + 12, which adds instead of multiplies." % X)
    nm, he, his = P.next()
    w("%s buys 5 dozen eggs for a pancake breakfast. A dozen is 12. How many eggs is that?" % nm,
      60, "eggs", 5 * 12, [17, 50, 72], "5 %s 12 = 50 + 10 = <b>60</b>. 50 is only 5 %s 10; it forgets 5 %s 2." % (X, X, X))
    w("A farm packs 84 eggs into cartons of 12. How many cartons does it fill?", 7, "cartons", 84 // 12, [8, 6, 72],
      "84 ÷ 12 = ? Think 12 %s ? = 84. 12 %s 7 = 84, so it fills <b>7 cartons</b>. 72 is 84 − 12." % (X, X))
    w("The school kitchen has 144 eggs for a Thanksgiving lunch. How many dozen is that?", 12, "dozen", 144 // 12,
      [11, 14, 132], "A dozen is 12. 144 ÷ 12 = ? 12 %s 12 = 144, so it is <b>12 dozen</b>." % X)
    nm, he, his = P.next()
    w("%s buys 3 dozen eggs. %s uses 8 eggs to bake muffins. How many eggs are left?" % (nm, he.capitalize()),
      28, "eggs", 3 * 12 - 8, [36, 44, 32], "First 3 %s 12 = 36. Then 36 − 8 = <b>28</b>. "
      "36 forgets the 8 eggs that were used." % X)
    w(fig(cartons_svg(4)) + "Each carton holds 12 eggs. 5 eggs are cracked. How many eggs are not cracked?", 43, "eggs",
      4 * 12 - 5, [48, 53, 7], "4 %s 12 = 48 eggs. 48 − 5 = <b>43</b>. 53 adds the 5 instead of taking it away." % X)
    w("Each hockey team brings 12 players to the tournament. There are 9 teams. How many players is that?", 108,
      "players", 9 * 12, [98, 96, 21], "9 %s 12 = 90 + 18 = <b>108</b>. 98 loses the carried ten. "
      "21 is 9 + 12, which adds instead of multiplies." % X)
    w("There are 12 months in a year. How many months are in 11 years?", 132, "months", 11 * 12, [122, 121, 23],
      "11 %s 12 = 110 + 22 = <b>132</b>. 121 is 11 %s 11." % (X, X))
    nm, he, his = P.next()
    w("%s’s baby sister is 48 months old. How many years old is she?" % nm, 4, "years", 48 // 12, [3, 5, 36],
      "There are 12 months in a year. 48 ÷ 12 = ? 12 %s 4 = 48, so she is <b>4 years</b> old." % X)
    w("A store sells maple syrup in boxes of 12 bottles. It sells 7 boxes. How many bottles is that?", 84, "bottles",
      7 * 12, [74, 72, 19], "7 %s 12 = 70 + 14 = <b>84</b>. 74 loses the carried ten. 72 is 6 %s 12." % (X, X))
    w("A school has 8 soccer teams with 11 players on each team. How many players is that?", 88, "players", 8 * 11,
      [19, 77, 99], "8 %s 11 = 80 + 8 = <b>88</b>. 19 is 8 + 11, which adds instead of multiplies." % X)
    w("Pencils come in packs of 12. The teacher needs 132 pencils. How many packs is that?", 11, "packs", 132 // 12,
      [12, 10, 120], "132 ÷ 12 = ? 12 %s 11 = 132, so the teacher needs <b>11 packs</b>." % X)
    w("Skating at the rink costs $7 for each student. 12 students go skating. How much do they pay in all?", 84, "$",
      12 * 7, [19, 74, 77], "12 %s $7 = $70 + $14 = <b>$84</b>. $74 loses the carried ten. $19 is 12 + 7." % X)
    nm, he, his = P.next()
    w("%s shares 72 maple cookies equally among 8 friends. How many cookies does each friend get?" % nm, 9, "cookies",
      72 // 8, [8, 64, 10], "72 ÷ 8 = ? Think 8 %s ? = 72. 8 %s 9 = 72, so each friend gets <b>9 cookies</b>." % (X, X))
    w("For the Grade 5 assembly, the gym has 8 rows of chairs with 12 chairs in each row. How many chairs is that?", 96,
      "chairs", 8 * 12, [86, 88, 20], "8 %s 12 = 80 + 16 = <b>96</b>. 86 loses the carried ten. 88 is 8 %s 11." % (X, X))
    w("On a canoe trip, 6 groups each carry 12 bottles of water. How many bottles is that?", 72, "bottles", 6 * 12,
      [62, 66, 18], "6 %s 12 = 60 + 12 = <b>72</b>. 62 loses the carried ten. 18 is 6 + 12." % X)
    assert len(its) == 20, len(its)
    return {"title": "Mixed facts and word problems: eggs by the dozen", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k), "11 %s %d = %d" % (X, k, 11 * k), "12 %s %d = %d" % (X, k, 12 * k)] for k in range(1, 13)]
    return (
        "<h2>The 11s and 12s come from the 10s</h2>"
        "<p>In Grade 5 you learn every fact from 0 %s 0 to 12 %s 12. The new ones are the 11s and 12s. "
        "Split 12 into <b>10 + 2</b>. Multiply both parts, then add.</p>" % (X, X)
        + "<figure class='sn-fig'>" + area_svg(7)
        + "<figcaption>12 %s 7 = 10 %s 7 + 2 %s 7 = 70 + 14 = 84.</figcaption></figure>" % (X, X, X)
        + "<p>For the 11s, split 11 into 10 + 1: 11 %s 8 = 80 + 8 = 88.</p>" % X
        + "<figure class='sn-fig'>" + cartons_svg(2)
        + "<figcaption>A dozen is 12. Two cartons hold 2 %s 12 = 24 eggs.</figcaption></figure>" % X
        + table(["", "11s", "12s"], rows)
        + ex("Example", "12 %s 8 = ?" % X, "10 %s 8 = 80 and 2 %s 8 = 16. 80 + 16 = 96." % (X, X), "96")
        + "<h2>Facts with 0 and 1</h2>"
        + table(["Rule", "Example"], [
            ["Any number %s 0 = 0" % X, "9 %s 0 = 0, 0 %s 12 = 0" % (X, X)],
            ["Any number %s 1 = the same number" % X, "1 %s 11 = 11" % X],
            ["0 ÷ any number (not 0) = 0", "0 ÷ 8 = 0"],
            ["A number ÷ 1 = the same number", "9 ÷ 1 = 9"],
            ["A number ÷ itself = 1", "12 ÷ 12 = 1"],
        ])
        + "<h2>More strategies</h2>"
        + table(["Fact", "Strategy", "Example"], [
            ["%s 12" % X, "Double the %s 6 fact" % X, "12 %s 7: double 42 = 84" % X],
            ["%s 9" % X, "%s 10, then take away one group" % X, "9 %s 7 = 70 − 7 = 63" % X],
            ["%s 8" % X, "Double the %s 4 fact" % X, "8 %s 7: double 28 = 56" % X],
            ["%s 7" % X, "%s 5 plus %s 2" % (X, X), "7 %s 6 = 30 + 12 = 42" % X],
        ])
        + "<h2>Every fact gives division facts</h2>"
        "<p>12, 9 and 108 make a <b>fact family</b>: 12 %s 9 = 108, 9 %s 12 = 108, 108 ÷ 12 = 9 and 108 ÷ 9 = 12. "
        "A division fact starts with the biggest number.</p>" % (X, X)
        + ex("Division", "96 ÷ 12 = ?", "Think: 12 %s ? = 96. 12 %s 8 = 96." % (X, X), "8")
        + ex("Word problem", "A farm packs 60 eggs into cartons of 12. How many cartons does it fill?",
             "60 ÷ 12 = ? 12 %s 5 = 60." % X, "5 cartons")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0 %s 7 = 7" % X, "0 groups of 7 is nothing: 0 %s 7 = 0" % X],
            ["12 %s 8 = 86" % X, "80 + 16 = 96. Keep the ten from 16"],
            ["12 %s 7 = 72 (70 + 2)" % X, "Multiply the 2 as well: 70 + 2 %s 7 = 70 + 14 = 84" % X],
            ["11 %s 12 = 1212" % X, "The double-digit pattern stops at 11 %s 9. 11 %s 12 = 120 + 12 = 132" % (X, X)],
            ["Turning division around: 12 ÷ 84 = 7", "Start with the biggest number: 84 ÷ 12 = 7"],
        ])
    )


FAQ = [
    {"q": "What multiplication facts should a Grade 5 student know in Ontario?",
     "a": "The Ontario Mathematics Curriculum (2020) asks Grade 5 students to recall the multiplication facts from 0 × 0 to 12 × 12 and the related division facts. The 11s and 12s are new in Grade 5."},
    {"q": "What is the easiest way to learn the 12 times table?",
     "a": "Split 12 into 10 and 2: 12 × 7 = 70 + 14 = 84. You can also double the 6s, because 12 × 7 is double 6 × 7 = 42."},
    {"q": "Why is any number times 0 equal to 0?",
     "a": "5 × 0 means 5 groups with nothing in them, and 0 × 5 means no groups at all, so both are 0. Any number times 1 stays the same."},
    {"q": "Do Grade 5 students in Ontario write EQAO?",
     "a": "No. Ontario students write the EQAO math assessment in Grade 3 and Grade 6. Knowing the facts to 12 × 12 well in Grade 5 makes multi-digit multiplication, division and fractions easier in Grade 6."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(45801)
    P = People(rnd)
    sets = [set_11_12(rnd), set_0_1(rnd), set_strategies(rnd), set_division(rnd), set_words(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "multiplication-facts-to-12-x-12", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication Facts to 12 × 12",
        "seo_title": "Grade 5 Multiplication Facts to 12 × 12 Worksheets with Answer Key (Ontario)",
        "short_title": "Multiplication facts to 12 × 12",
        "domain": "Number",
        "standard_code": "Grade 5: B2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Recall and demonstrate multiplication facts from 0 × 0 to 12 × 12, and related division facts",
        "meta_desc": "Free Grade 5 math worksheets on multiplication facts to 12 × 12: the 11s and 12s, facts with 0 and 1, strategies, related division facts and word problems with eggs by the dozen. 100 questions with an answer key, following the Ontario curriculum.",
        "key_big": "12 × 7 = 10 × 7 + 2 × 7 = 70 + 14 = 84",
        "key_sub": "Split 12 into 10 and 2, or 11 into 10 and 1, then add. Any number times 0 is 0, and any number times 1 stays the same. Every fact gives division facts: 12 × 7 = 84, so 84 ÷ 12 = 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(array of [0-9]+ rows with 1[12]|[0-9]+ egg cartons|grid of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
