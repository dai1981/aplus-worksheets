# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Missing Factors and Input-Output Tables (TEKS 3.5D, 3.5E)
  python3 tools/gen_ustx_math_g3_missing_factors_and_tables.py
Missing factors (the Ontario Grade 4 maker with Texas names), unknowns in division equations, input-output
tables, finding the rule in words, and real-world tables of number pairs (wheels on tricycles, legs on spiders,
tickets and prices).
Wrong answers come from real mistakes: giving the product instead of the missing factor, using an adding rule
that only works for the first pair, and reading the table from the wrong column.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, run, adopt, table, example)
import gen_caon_math_g4_facts as on

adopt(on)
R = random.Random(60901)


def io_table(head, rows):
    return "<div class='qfig'>" + table(head, [[str(a), str(b)] for a, b in rows]) + "</div>"


# ------------------------------------------------------------ set 2: unknowns in division equations
def one_div(r):
    d, q = r.randint(2, 10), r.randint(2, 10)
    t = d * q
    kind = r.choice(["total", "divisor", "quot", "mult_prod"])
    if kind == "total":
        return mcq("☐ ÷ %d = %d. What number goes in the box?" % (d, q), t, [q - d if q > d else d - q + 1, d + q, t + d, q], "Think: %d × %d = %d. So <b>%d</b> ÷ %d = %d." % (d, q, t, t, d, q))
    if kind == "divisor":
        return mcq("%d ÷ ☐ = %d. What number goes in the box?" % (t, q), d, [t - q, t * q if t * q <= 100 else t + q, d + 1, q if q != d else d - 1],
                   "Think: %d × ☐ = %d. %d × %d = %d, so the box is <b>%d</b>." % (q, t, q, d, t, d))
    if kind == "quot":
        return mcq("%d = %d × ☐. What number goes in the box?" % (t, d), q, [t - d, t + d, q + 1, d if d != q else q - 1], "%d × %d = %d, so the box is <b>%d</b>." % (d, q, t, q))
    return mcq("%d × %d = ☐ ÷ 1. What number goes in the box?" % (d, q), t, [d + q, t + 1, t - 1, d * (q + 1)], "%d × %d = %d, and %d ÷ 1 = %d. The box is <b>%d</b>." % (d, q, t, t, t, t))


# ------------------------------------------------------------ set 3: input-output tables
def rule_of(r):
    kind = r.choice(["×", "×", "+", "÷"])
    if kind == "×":
        m = r.randint(2, 10)
        return ("Multiply by %d" % m, lambda x: x * m, lambda r: r.sample(range(1, 11), 4))
    if kind == "+":
        m = r.randint(3, 25)
        return ("Add %d" % m, lambda x: x + m, lambda r: sorted(r.sample(range(1, 40), 4)))
    m = r.randint(2, 10)
    return ("Divide by %d" % m, lambda x: x // m, lambda r: [m * k for k in r.sample(range(1, 11), 4)])


def one_io(r):
    name, f, ins = rule_of(r)
    xs = ins(r)
    rows = [(x, f(x)) for x in xs]
    j = r.randrange(4)
    miss = r.choice(["out", "out", "in"])
    shown = [(a if not (i == j and miss == "in") else "?", b if not (i == j and miss == "out") else "?") for i, (a, b) in enumerate(rows)]
    q = io_table(["Input", "Output"], shown) + "The rule is <b>%s</b>. What is the missing number?" % name
    ans = rows[j][1] if miss == "out" else rows[j][0]
    other = rows[j][0] if miss == "out" else rows[j][1]
    wrong = [other, ans + 1, ans - 1 if ans > 1 else ans + 2, ans * 2]
    return mcq(q, ans, wrong, "%s: %s → %s. The missing number is <b>%s</b>." % (name, rows[j][0], rows[j][1], comma(ans)))


# ------------------------------------------------------------ set 4: find the rule
def one_rule(r):
    m = r.randint(2, 10)
    xs = sorted(r.sample(range(1, 11), 4))
    rows = [(x, x * m) for x in xs]
    if r.random() < 0.3:
        a = r.randint(3, 20)
        rows = [(x, x + a) for x in xs]
        right = "Add %d" % a
        wrong = ["Multiply by %d" % (rows[0][1] // rows[0][0]) if rows[0][1] % rows[0][0] == 0 and rows[0][1] // rows[0][0] != 1 else "Add %d" % (a + 1), "Subtract %d" % a, "Add %d" % (rows[1][1] - rows[0][1]) if rows[1][1] - rows[0][1] != a else "Add %d" % (a + 2)]
    else:
        right = "Multiply by %d" % m
        d = rows[0][1] - rows[0][0]
        wrong = ["Add %d" % d if d > 0 else "Add %d" % (m + 1), "Multiply by %d" % (m + 1), "Divide by %d" % m]
    q = io_table(["Input", "Output"], rows) + "Which rule works for every pair in the table?"
    return mcq(q, right, wrong, "Check every row: %s. The rule is <b>%s</b>." % ("; ".join("%d → %d" % p for p in rows), right))


# ------------------------------------------------------------ set 5: real-world tables
THINGS = [("Tricycles", "Wheels", 3), ("Spiders", "Legs", 8), ("Cars", "Wheels", 4), ("Packs", "Juice boxes", 6),
          ("Hands", "Fingers", 5), ("Weeks", "Days", 7), ("Bikes", "Wheels", 2), ("Tickets", "Dollars", 9),
          ("Bags", "Oranges", 10), ("Boxes", "Crayons", 8)]


def one_real(r):
    a, b, m = r.choice(THINGS)
    xs = sorted(r.sample(range(1, 7), 3))
    rows = [(x, x * m) for x in xs]
    kind = r.choice(["next", "words", "big"])
    if kind == "next":
        n = r.randint(xs[-1] + 1, 10)
        q = io_table([a, b], rows) + "The table keeps going the same way. How many %s for %d %s?" % (b.lower(), n, a.lower())
        return mcq(q, n * m, [n * m + m, n * m - m, n + m, rows[-1][1] + (n - xs[-1])], "Each one has %d %s, so multiply by %d: %d × %d = <b>%d</b>." % (m, b.lower(), m, n, m, n * m))
    if kind == "words":
        q = io_table([a, b], rows) + "Which sentence describes the table?"
        right = "The number of %s is %d times the number of %s" % (b.lower(), m, a.lower())
        wrong = ["The number of %s is %d more than the number of %s" % (b.lower(), m, a.lower()),
                 "The number of %s is %d times the number of %s" % (a.lower(), m, b.lower()),
                 "The number of %s is %d times the number of %s" % (b.lower(), m + 1, a.lower())]
        return mcq(q, right, wrong, "%d × %d = %d, %d × %d = %d: <b>%s</b>." % (xs[0], m, rows[0][1], xs[1], m, rows[1][1], right))
    t = r.randint(4, 10) * m
    q = io_table([a, b], rows) + "The table keeps going the same way. How many %s have %d %s?" % (a.lower(), t, b.lower())
    return mcq(q, t // m, [t - m, t // m + 1, t + m, m], "%d ÷ %d = <b>%d</b>, because %d × %d = %d." % (t, m, t // m, t // m, m, t))


def build():
    s1 = run(on.set_missing, "rnd", seed=101)["items"]
    sets = [S("Missing factors", s1),
            S("Unknowns in multiplication and division equations", collect(one_div, 20, R, avoid=[s1])),
            S("Input-output tables", collect(one_io, 20, R)),
            S("Find the rule", collect(one_rule, 20, R)),
            S("Real-world tables", collect(one_real, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>A <b>missing factor</b> is a missing number in a multiplication. For 6 × ☐ = 42, ask: 6 times what is 42? The answer is 7.</li>"
        "<li>For a division with a box, think of the multiplication fact: ☐ ÷ 4 = 9 means 4 × 9 = ☐, so ☐ = 36.</li>"
        "<li>An <b>input-output table</b> uses one rule for every pair. Check the rule on every row, not just the first.</li>"
        "<li>Real-world tables show number pairs: 1 tricycle has 3 wheels, 2 tricycles have 6, 3 have 9. The number of wheels is 3 times the number of tricycles.</li></ul>",
        [table(["Tricycles", "Wheels"], [["1", "3"], ["2", "6"], ["3", "9"], ["4", "?"]]),
         example("What is the missing output?", ["Each tricycle has 3 wheels.", "4 × 3 = 12"], "12 wheels")],
        [["Giving the product instead of the missing factor: 6 × ☐ = 42, answer 42", "Ask: 6 times what is 42?"],
         ["Using a rule that fits only the first row", "Test the rule on every pair in the table."],
         ["Reading the table the wrong way", "Find the column the question asks about before you answer."]])
    faq = [("What does TEKS 3.5D ask?", "Find the unknown number in a multiplication or division equation with three whole numbers, when the unknown is a missing factor or a product."),
           ("What does TEKS 3.5E ask?", "Show real-world relationships with number pairs in a table and describe them in words, such as 'the number of legs is 8 times the number of spiders'."),
           ("How do you find the rule in a table?", "Look at how each input becomes its output. Try multiplying and adding, then check that the rule works for every pair."),
           ("Why use a box or a letter for the unknown?", "It shows which number you are looking for, so you can write an equation for a word problem.")]
    make("missing-factors-and-input-output-tables", 9, "Algebraic Reasoning", "3.5D, 3.5E",
         "3.5D determine the unknown whole number in a multiplication or division equation relating three whole numbers when the unknown is either a missing factor or product; 3.5E represent real-world relationships using number pairs in a table and verbal descriptions",
         "Missing Factors and Input-Output Tables", "Missing Factors and Input-Output Tables",
         "Free Grade 3 worksheets for Texas TEKS 3.5D and 3.5E: missing factors, unknowns in division equations, input-output tables, finding the rule and real-world tables of number pairs. 100 questions with answers.",
         "Use the multiplication fact to find a missing number.", "A table follows one rule for every pair. Check the rule on every row.",
         body, faq, sets, seo_title="Grade 3 Missing Factors and Input-Output Tables Worksheets (TEKS 3.5D, 3.5E)")


if __name__ == "__main__":
    build()
