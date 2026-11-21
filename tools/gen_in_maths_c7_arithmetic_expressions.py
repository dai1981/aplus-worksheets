# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 2: Arithmetic Expressions
  python3 tools/gen_in_maths_c7_arithmetic_expressions.py
Reading and evaluating arithmetic expressions: terms, the order of operations (brackets, then × and ÷, then + and −),
placing brackets, removing brackets after a minus sign, comparing expressions without calculating, and writing an
expression for a situation.
Wrong answers come from real mistakes: working strictly left to right, changing only the first sign after removing
brackets with a minus, and adding before multiplying.
"""
import random
from in_common import num, unit, T, QN, adopt, gb, inr
import gen_uk_maths_y7_order_of_operations as oo

R = random.Random(907002)
adopt(oo, R)


def one_terms(r):
    k = r.randint(2, 4)
    ts = []
    for _ in range(k):
        a, b = r.randint(2, 12), r.randint(2, 12)
        ts.append(r.choice(["%d × %d" % (a, b), "%d" % (a * b + r.randint(1, 9)), "%d ÷ %d" % (a * b, b)]))
    e = ts[0] + "".join(" %s %s" % (r.choice(["+", "−"]), t) for t in ts[1:])
    return QN("How many terms are there in the expression %s?" % e, k, [k + 1, len(e.split()) // 2, k * 2], "Terms are separated by + and −: <b>%d</b>." % k)


def one_minus(r):
    a, b, c = r.randint(40, 99), r.randint(5, 30), r.randint(2, 20)
    kind = r.choice(["val", "val", "form"])
    if kind == "val":
        return QN("Work out %d − (%d − %d)." % (a, b, c), a - b + c, [a - b - c, a - (b + c), a + b - c], "Removing the brackets: %d − %d + %d = <b>%d</b>." % (a, b, c, a - b + c))
    return T("Which expression equals %d − (%d + %d)?" % (a, b, c), "%d − %d − %d" % (a, b, c), ["%d − %d + %d" % (a, b, c), "%d + %d − %d" % (a, b, c), "%d + %d + %d" % (a, b, c)],
             "A minus before the bracket changes both signs: <b>%d − %d − %d</b>." % (a, b, c))


def one_cmp(r):
    a, b = r.randint(100, 999), r.randint(10, 99)
    kind = r.choice(["add", "sub", "swap"])
    if kind == "add":
        d = r.randint(1, 9)
        return T("Without calculating, which sign is correct? %d + %d ___ %d + %d" % (a, b, a + d, b - d), "=", ["&lt;", "&gt;", "You must calculate"],
                 "%d is %d more and %d is %d less, so the sums are equal: <b>=</b>." % (a + d, d, b - d, d))
    if kind == "sub":
        d = r.randint(1, 9)
        return T("Without calculating, which sign is correct? %d − %d ___ %d − %d" % (a, b, a + d, b + d), "=", ["&lt;", "&gt;", "You must calculate"],
                 "Adding the same number to both parts of a difference does not change it: <b>=</b>.")
    d = r.randint(1, 9)
    return T("Without calculating, which sign is correct? %d − %d ___ %d − %d" % (a, b, a, b + d), "&gt;", ["&lt;", "=", "You must calculate"],
             "Taking away more gives less, so the first is greater: <b>&gt;</b>.")


def one_story(r):
    n, p, m, q = r.randint(2, 6), r.choice([12, 15, 20, 25, 30]), r.randint(2, 5), r.choice([40, 45, 50, 60])
    have = r.choice([500, 1000])
    tot = n * p + m * q
    return T("Irfan buys %d pencils at %s each and %d notebooks at %s each. He pays with a %s note. How much change does he get?" % (n, inr(p), m, inr(q), inr(have)),
             inr(have - tot), [inr(have - n * p - q), inr(tot), inr(have - (n + m) * (p + q) // 2)],
             "%s − (%d × %d + %d × %d) = %s − %s = <b>%s</b>." % (num(have), n, p, m, q, num(have), num(tot), inr(have - tot)))


def main():
    unit(7, 1, 2, "arithmetic-expressions", 2, "N", "Arithmetic Expressions: Terms, Brackets and Order of Operations", "arithmetic expressions",
         "Arithmetic expressions and their values, terms, order of operations (brackets, then × and ÷, then + and −), removing brackets and comparing expressions (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Arithmetic Expressions worksheet (Ganita Prakash Part 1, Chapter 2): terms, order of operations, brackets, removing brackets after a minus and comparing expressions. 100 questions with answers.",
         "Brackets first, then × and ÷, then + and −", "a − (b − c) = a − b + c.",
         "<p>An <b>expression</b> such as 30 − 4 × 5 has <b>terms</b> separated by + and −: here 30 and 4 × 5. Work out each term first, then add or subtract: 30 − 20 = 10.</p>"
         "<p><b>Brackets</b> are worked out first. A minus sign before brackets changes the signs inside: 50 − (12 − 7) = 50 − 12 + 7.</p>"
         "<p>You can often compare expressions without calculating: 78 + 25 = 80 + 23.</p>",
         [("Work out 18 + 6 × 4 − 10.", ["Terms: 18, 6 × 4 = 24, 10", "18 + 24 − 10"], "32"),
          ("Work out 100 − (45 − 15).", ["100 − 45 + 15"], "70")],
         ["Working from left to right: 18 + 6 × 4 = 24 × 4 is wrong.", "Changing only the first sign: 100 − (45 − 15) = 100 − 45 − 15 is wrong.", "Ignoring the brackets."],
         [("What is a term in an expression?", "A part of the expression separated from the others by + or − signs, such as 4 × 5 in 30 − 4 × 5."),
          ("What is the order of operations?", "Brackets first, then multiplication and division, then addition and subtraction."),
          ("What happens to the signs when a minus is in front of brackets?", "They change: a − (b + c) = a − b − c and a − (b − c) = a − b + c.")],
         [("Terms of an expression", [(one_terms, 10), (gb(oo.one_md), 10)]),
          ("Order of operations", [(gb(oo.one_md), 10), (gb(oo.one_br), 10)]),
          ("Brackets and the minus sign", [(one_minus, 14), (gb(oo.one_place), 6)]),
          ("Comparing without calculating", [(one_cmp, 20)]),
          ("Writing and evaluating expressions", [(one_story, 14), (gb(oo.one_br), 6)])], R)


if __name__ == "__main__":
    main()
