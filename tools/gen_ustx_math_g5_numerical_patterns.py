# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Numerical Patterns, Input-Output Tables and Graphs (TEKS 5.4C, 5.4D)
  python3 tools/gen_ustx_math_g5_numerical_patterns.py
Generating patterns from a rule, telling additive and multiplicative patterns apart, finding a rule y = ax or
y = x + a from a table, graphing ordered pairs (the US Grade 5 makers), and input-output tables in word problems.
Wrong answers come from real mistakes: looking only at one pair, adding when the rule multiplies, and switching x
and y.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_patterns as pt
adopt(pt)
tx_common.GRADE = "grade-5"

def table(xs, ys, xn="x", yn="y"):
    th = "".join("<td>%s</td>" % comma(x) for x in xs)
    td = "".join("<td>%s</td>" % (comma(y) if y is not None else "?") for y in ys)
    return "<div class='sn-tw'><table class='sn-table'><tbody><tr><th>%s</th>%s</tr><tr><th>%s</th>%s</tr></tbody></table></div>" % (xn, th, yn, td)


def one_kind(r):
    a = r.randint(2, 9)
    start = r.randint(1, 4)
    xs = list(range(start, start + 4))
    mult = r.random() < 0.5
    ys = [x * a if mult else x + a for x in xs]
    if not mult and xs[0] * 2 == ys[0]:
        return None
    right = "Multiplicative: y = %d × x" % a if mult else "Additive: y = x + %d" % a
    w = ["Additive: y = x + %d" % (ys[0] - xs[0]), "Multiplicative: y = %d × x" % (ys[1] - ys[0]), "Additive: y = x + %d" % (ys[1] - ys[0]), "Multiplicative: y = %d × x" % (ys[0] // xs[0] if ys[0] % xs[0] == 0 else a + 1)]
    e = ("Each y is %d times x (%s), so the pattern is <b>multiplicative</b>." % (a, ", ".join("%d × %d = %d" % (a, x, y) for x, y in zip(xs, ys))) if mult
         else "Each y is x plus %d (%s), so the pattern is <b>additive</b>." % (a, ", ".join("%d + %d = %d" % (x, a, y) for x, y in zip(xs, ys))))
    return mcq(table(xs, ys) + "Is this pattern additive or multiplicative? What is the rule?", right, [x for x in dict.fromkeys(w) if x != right], e)


def one_missing(r):
    a = r.randint(2, 12)
    mult = r.random() < 0.5
    xs = sorted(r.sample(range(1, 13), 4))
    f = (lambda x: a * x) if mult else (lambda x: x + a)
    ask = r.randint(13, 30)
    rule = "y = %d × x" % a if mult else "y = x + %d" % a
    v = f(ask)
    w = [ask + a, a * ask, f(xs[-1]) + (f(xs[-1]) - f(xs[-2])), v + a]
    w = [str(t) for t in dict.fromkeys(w) if t != v]
    return mcq(table(xs + [ask], [f(x) for x in xs] + [None]) + "The rule is %s. What is y when x is %d?" % (rule, ask), str(v), w,
               "%s: %s = <b>%d</b>." % (rule, ("%d × %d" % (a, ask)) if mult else ("%d + %d" % (ask, a)), v))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["ticket", "save", "legs", "age"])
    n = r.randint(6, 15)
    if kind == "ticket":
        p = r.randint(4, 12)
        return mcq("Tickets to a rodeo cost $%d each. Which rule gives the cost y for x tickets? What do %d tickets cost?" % (p, n), "y = %d × x; $%d" % (p, p * n), ["y = x + %d; $%d" % (p, n + p), "y = %d × x; $%d" % (p, p * n + p), "y = x + %d; $%d" % (p, p * n)],
                   "Each ticket adds $%d, so the cost is %d times the number of tickets: y = %d × x. %d × %d = <b>$%d</b>." % (p, p, p, p, n, p * n))
    if kind == "save":
        s = r.randint(15, 60)
        return mcq("%s has $%d more than %s brother. Which rule gives %s's money y if %s brother has x dollars? How much does %s have if %s brother has $%d?" % (k["n"], s, k["his"], k["n"], k["his"], k["n"], k["his"], n * 3), "y = x + %d; $%d" % (s, n * 3 + s),
                   ["y = %d × x; $%d" % (s, s * n * 3), "y = x + %d; $%d" % (s, n * 3), "y = x − %d; $%d" % (s, n * 3 - s if n * 3 > s else s - n * 3)],
                   "%s always has $%d more, so add: y = x + %d. %d + %d = <b>$%d</b>." % (k["n"], s, s, n * 3, s, n * 3 + s))
    if kind == "legs":
        return mcq("Each spider has 8 legs. Which rule gives the number of legs y for x spiders? How many legs do %d spiders have?" % n, "y = 8 × x; %d" % (8 * n), ["y = x + 8; %d" % (n + 8), "y = 8 × x; %d" % (8 * n + 8), "y = x + 8; %d" % (8 * n)],
                   "Each spider adds 8 legs: y = 8 × x. 8 × %d = <b>%d</b>." % (n, 8 * n))
    d = r.randint(3, 9)
    return mcq("%s is %d years older than %s cousin. Which rule gives %s's age y when the cousin is x years old? How old is %s when the cousin is %d?" % (k["n"], d, k["his"], k["n"], k["n"], n), "y = x + %d; %d" % (d, n + d), ["y = %d × x; %d" % (d, d * n), "y = x + %d; %d" % (d, n + d + 1), "y = x − %d; %d" % (d, n - d if n > d else n)],
               "The difference in age never changes, so add %d: y = x + %d. %d + %d = <b>%d</b>." % (d, d, n, d, n + d))


def build():
    sets, R = build_sets([
        ("Generate patterns from a rule", [("run", pt.set_generate, ("rnd",), 20)]),
        ("Additive or multiplicative?", [("collect", one_kind, 20)]),
        ("Use the rule to find y", [("collect", one_missing, 20)]),
        ("Ordered pairs and graphs", [("run", pt.set_graph, ("rnd",), 20)]),
        ("Rules in word problems", [("collect", one_story, 20)]),
    ], 65014)
    finish(sets, R)
    body = lesson('<ul><li>An <b>additive</b> pattern adds the same number to x: y = x + 4 gives 1 → 5, 2 → 6, 3 → 7.</li><li>A <b>multiplicative</b> pattern multiplies x by the same number: y = 4 × x gives 1 → 4, 2 → 8, 3 → 12.</li><li>Check the rule with <b>every</b> pair in the table, not just one.</li><li>Each pair (x, y) is a point you can graph on the coordinate plane.</li></ul>',
        [example("x: 1, 2, 3, 4  y: 6, 7, 8, 9", ["7 − 2 = 5 for every pair", "Additive"], "y = x + 5"), example("x: 1, 2, 3, 4  y: 6, 12, 18, 24", ["12 ÷ 2 = 6 for every pair", "Multiplicative"], "y = 6 × x")],
        [['Checking only one pair', 'y = x + 5 and y = 6 × x both give 1 → 6. Test the next pair too.'], ['Using the change in y as the rule', 'If y goes up by 6, the rule may be y = 6 × x, not y = x + 6.'], ['Switching x and y on the graph', 'x is across, y is up: (2, 12) means 2 right, 12 up.']])
    faq = [('What does TEKS 5.4C ask?', 'Generate a numerical pattern when given a rule in the form y = ax or y = x + a and graph.'), ('What does TEKS 5.4D ask?', 'Recognize the difference between additive and multiplicative numerical patterns given in a table or graph.'), ('How can I tell additive from multiplicative?', 'Subtract x from y for each pair. If it is always the same, it is additive. If y ÷ x is always the same, it is multiplicative.'), ('What does a multiplicative pattern look like on a graph?', 'The points line up on a line that starts at (0, 0).')]
    make('numerical-patterns-and-graphs', 14, 'Algebraic Reasoning', '5.4C, 5.4D',
         '5.4C generate a numerical pattern when given a rule in the form y = ax or y = x + a and graph; 5.4D recognize the difference between additive and multiplicative numerical patterns given in a table or graph',
         'Numerical Patterns, Input-Output Tables and Graphs', 'Numerical Patterns and Graphs',
         'Free Grade 5 worksheets for Texas TEKS 5.4C and 5.4D: generate patterns from a rule, tell additive and multiplicative patterns apart, use y = ax and y = x + a, graph ordered pairs and word problems. 100 questions with answers.',
         'Additive: y = x + a. Multiplicative: y = a × x.', 'Test the rule with every pair in the table.',
         body, faq, sets, seo_title='Grade 5 Numerical Patterns and Input-Output Tables Worksheets (TEKS 5.4C, 5.4D, STAAR)')


if __name__ == "__main__":
    build()
