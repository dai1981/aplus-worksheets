# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Input-Output Tables and Number Patterns (TEKS 4.5B)
  python3 tools/gen_ustx_math_g4_patterns.py
Using a rule to extend a pattern, finding the rule, features of patterns, input-output tables (the US Grade 4
pattern makers with Texas names), and tables that relate each term to its position, with an expression such as
4 × n.
Wrong answers come from real mistakes: using the difference between terms when the rule multiplies the position,
checking only the first pair, and mixing up the position and the value.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_patterns as usp
adopt(usp)
tx_common.GRADE = "grade-4"

def pos_table(rows):
    h = "".join("<th>%d</th>" % p for p, v in rows)
    b = "".join("<td>%s</td>" % v for p, v in rows)
    return "<div class='qfig'><div class='sn-tw'><table class='sn-table'><tbody><tr><th>Position</th>%s</tr><tr><th>Value</th>%s</tr></tbody></table></div></div>" % (h, b)


def one_pos(r):
    m = r.randint(2, 12)
    a = r.choice([0, 0, r.randint(1, 9)])
    f = lambda n: m * n + a
    rows = [(n, f(n)) for n in range(1, 5)]
    kind = r.choice(["expr", "nth", "nth", "back"])
    expr = "%d × n" % m + (" + %d" % a if a else "")
    if kind == "expr":
        q = pos_table(rows) + "Which expression gives the value of the term in position n?"
        wrong = ["n + %d" % m, "%d × n" % (m + 1), "%d × n + %d" % (m, a + 1) if a else "%d × n + %d" % (m, m)]
        return mcq(q, expr, wrong, "Check every column: %s. The rule is <b>%s</b>." % ("; ".join("%d → %d" % p for p in rows), expr))
    if kind == "nth":
        n = r.randint(8, 25)
        q = pos_table(rows) + "The pattern continues. What is the value in position %d?" % n
        return mcq(q, f(n), [rows[-1][1] + (n - 4), f(n) + m, f(n - 1), n * (m + 1) + a], "Use the rule %s: %s = <b>%s</b>." % (expr, expr.replace("n", str(n)), comma(f(n))))
    v = f(r.randint(6, 15))
    q = pos_table(rows) + "The pattern continues. In which position is the value %s?" % comma(v)
    n = (v - a) // m
    return mcq(q, n, [v // m if v // m != n else n + 1, n + 1, v - m * 4, n - 1], "Undo the rule: (%d − %d) ÷ %d = <b>%d</b>." % (v, a, m, n) if a else "Undo the rule: %d ÷ %d = <b>%d</b>." % (v, m, n))


def build():
    sets, R = build_sets([
        ("Use a rule: find the next numbers", [("run", usp.set_extend, ("rnd",), 20)]),
        ("Find the rule and the missing number", [("run", usp.set_find_rule, ("rnd",), 20)]),
        ("Input-output tables and word problems", [("run", usp.set_words, ("rnd", usp.People), 20)]),
        ("Position and value: expressions", [("collect", one_pos, 20)]),
        ("Features of a pattern", [("run", usp.set_features, ("rnd", usp.People), 20)]),
    ], 64013)
    finish(sets, R)
    body = lesson('<ul><li>A <b>rule</b> tells how to get each number in a pattern, such as add 6 or multiply by 4.</li><li>In an <b>input-output table</b>, the same rule turns every input into its output. Test the rule on every pair.</li><li>A table can link each <b>position</b> to its <b>value</b>. If position 1 is 5, position 2 is 10 and position 3 is 15, the value is 5 × n.</li></ul>',
        [pos_table([(1, 7), (2, 14), (3, 21), (4, 28)]) + "<p>Each value is 7 times its position: 7 × n. Position 10 has 70.</p>", example("The rule is multiply by 3, then add 2. What is the output for 6?", ["6 × 3 = 18", "18 + 2 = 20"], "20")],
        [['Adding the difference when the rule multiplies the position', 'Compare each value with its position, not only with the term before.'], ['Checking the rule on one pair only', 'A rule must work for every pair.'], ['Mixing up the position and the value', 'Read the row labels before you answer.']])
    faq = [('What does TEKS 4.5B ask?', 'Represent problems with an input-output table and numerical expressions that generate a number pattern, showing the relationship between each value and its position.'), ('How do you find the rule of a table?', 'Look at how each input becomes its output. Try adding and multiplying, then check the rule on every pair.'), ('What does 4 × n mean?', 'Multiply the position number n by 4 to get the value. Position 7 has 4 × 7 = 28.'), ('How can a table help with word problems?', 'It organizes number pairs, like weeks and dollars saved, so you can see the rule and predict later values.')]
    make('input-output-tables-and-number-patterns', 13, 'Algebraic Reasoning', '4.5B',
         '4.5B represent problems using an input-output table and numerical expressions to generate a number pattern that follows a given rule representing the relationship of the values in the resulting sequence and their position in the sequence',
         'Input-Output Tables and Number Patterns', 'Input-Output Tables and Patterns',
         'Free Grade 4 pattern worksheets for Texas TEKS 4.5B: extend patterns with a rule, find the rule, input-output tables, position and value with expressions like 4 × n, and pattern features. 100 questions with answers.',
         'One rule works for every pair in a table.', 'If the value is always 6 times the position, the expression is 6 × n.',
         body, faq, sets, seo_title='Grade 4 Input-Output Tables and Number Patterns (TEKS 4.5B, STAAR)')


if __name__ == "__main__":
    build()
