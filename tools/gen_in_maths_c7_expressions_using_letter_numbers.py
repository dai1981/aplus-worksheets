# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 4: Expressions Using Letter-Numbers
  python3 tools/gen_in_maths_c7_expressions_using_letter_numbers.py
Using letters for numbers: writing expressions from words and situations, algebraic notation (3a, a²), finding the value
of an expression, like terms and simplifying, and patterns described by formulas.
Wrong answers come from real mistakes: 3a read as 3 + a, a² as 2a, adding unlike terms, and substituting into only one term.
"""
import random
from in_common import unit, QN, adopt, gb
import gen_uk_maths_y7_algebraic_notation_and_substitution as an
import gen_uk_maths_y7_simplifying_expressions as se
import gen_au_maths_y7_formulas_and_substitution as fs

R = random.Random(907004)
for m in (an, se, fs):
    adopt(m, R)


def one_pattern(r):
    kind = r.choice(["sticks", "age", "cost"])
    n = r.randint(5, 30)
    if kind == "sticks":
        k = r.choice([3, 4, 5, 6])
        shape = {3: "triangles", 4: "squares", 5: "pentagons", 6: "hexagons"}[k]
        return QN("Separate %s are made with matchsticks: n %s need %dn matchsticks. How many matchsticks for %d %s?" % (shape, shape, k, n, shape), k * n, [k + n, k * n + k, n],
                  "%d × %d = <b>%d</b>." % (k, n, k * n))
    if kind == "age":
        d = r.randint(20, 35)
        return QN("Meena's mother is %d years older than Meena. If Meena is m years old, her mother is m + %d. How old is her mother when Meena is %d?" % (d, d, n), n + d, [n * d, d - n, n + d + 1],
                  "%d + %d = <b>%d</b>." % (n, d, n + d))
    p = r.choice([5, 8, 10, 12, 15, 20])
    c = r.choice([10, 20, 30, 50])
    return QN("A shop charges ₹%d for each kg of rice plus ₹%d for delivery: ₹(%dk + %d). What is the cost for %d kg?" % (p, c, p, c, n), p * n + c, [p * (n + c), p + n + c, p * n],
              "%d × %d + %d = <b>₹%d</b>." % (p, n, c, p * n + c))


def main():
    unit(7, 1, 4, "expressions-using-letter-numbers", 4, "A", "Expressions Using Letter-Numbers: Algebraic Expressions", "expressions using letter-numbers",
         "Using letters to stand for numbers, writing algebraic expressions, evaluating expressions, like terms and simplifying expressions (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Expressions Using Letter-Numbers worksheet (Ganita Prakash Part 1, Chapter 4): writing algebraic expressions, notation, substitution, like terms and simplifying. 100 questions with answers.",
         "A letter-number stands for any number", "3a means 3 × a; a² means a × a.",
         "<p>A <b>letter-number</b> such as n can stand for any number. 3n means 3 × n; n² means n × n; n + 5 means 5 more than n.</p>"
         "<p>To find the <b>value</b> of an expression, replace each letter by its number: if n = 4, then 3n + 5 = 17.</p>"
         "<p><b>Like terms</b> have the same letter part and can be added: 4a + 7a = 11a. 4a + 7b cannot be simplified.</p>",
         [("Simplify 5x + 3y − 2x + y.", ["5x − 2x = 3x", "3y + y = 4y"], "3x + 4y"),
          ("Find 4p − 7 when p = 5.", ["4 × 5 − 7"], "13")],
         ["Reading 3a as 3 + a.", "Writing a² as 2a.", "Adding unlike terms: 2a + 3b = 5ab is wrong."],
         [("Why do we use letters in maths?", "A letter stands for a number we do not know yet or for any number, so one expression can describe many cases."),
          ("What are like terms?", "Terms with exactly the same letters and powers, such as 3x and −5x."),
          ("How do you evaluate an expression?", "Replace each letter by its value and follow the order of operations.")],
         [("Algebraic notation", [(gb(an.one_notation), 12), (gb(fs.one_notation), 8)]),
          ("Writing expressions", [(gb(an.one_words), 14), (gb(an.one_context), 6)]),
          ("Finding the value of an expression", [(gb(an.one_sub), 12), (gb(fs.one_sub), 8)]),
          ("Like terms and simplifying", [(gb(se.one_like1), 10), (gb(se.one_like2), 10)]),
          ("Patterns and formulas", [(one_pattern, 14), (gb(fs.one_sub2), 6)])], R)


if __name__ == "__main__":
    main()
