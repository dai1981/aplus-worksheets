# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 6: Algebra Play
  python3 tools/gen_in_maths_c8_algebra_play.py
Explaining number tricks with algebra (think of a number), writing expressions for patterns, the nth term of a sequence,
solving linear equations (unknowns on both sides, brackets) and puzzles about ages and consecutive numbers.
Wrong answers come from real mistakes: moving a term without changing its sign, multiplying only part of a bracket, and
writing the nth term as n + d instead of dn + c.
"""
import random
from in_common import num, unit, T, QN, adopt, gb
import gen_uk_maths_y8_equations_with_unknowns_on_both_sides as eq
import gen_uk_maths_y7_sequences as sq

R = random.Random(908013)
adopt(eq, R)
adopt(sq, R)


def one_trick(r):
    a, b = r.randint(2, 5), r.randint(2, 20)
    a = 2 * a // 2 * 1
    m = r.randint(2, 5)
    steps = "Think of a number. Multiply it by %d. Add %d. Divide by %d. Subtract the number you first thought of." % (m, m * b, m)
    return QN(steps + " What is the answer, whatever number you start with?", b, [m * b, b + m, 0],
              "Let the number be x: (%dx + %d) ÷ %d − x = x + %d − x = <b>%d</b>." % (m, m * b, m, b, b))


def one_expr(r):
    kind = r.choice(["age", "age", "consec", "perim", "cost"])
    if kind == "age":
        k, d = r.randint(2, 4), r.randint(3, 15)
        total = r.randint(40, 90)
        x = (total - d) // (k + 1)
        if (total - d) % (k + 1):
            return None
        return QN("Ravi's father is %d times as old as Ravi will be in %d years... (simplified) — A father is %d times as old as his son, and together their ages add up to %d. How old is the son?" % (k, d, k, total) if False else
                  "A father is %d times as old as his son. Their ages add up to %d. How old is the son?" % (k, total + 0 * d) if total % (k + 1) == 0 else None,
                  total // (k + 1), [total // k, total - total // (k + 1), total // (k + 1) + k], "x + %dx = %d, so %dx = %d and <b>x = %d</b>." % (k, total, k + 1, total, total // (k + 1)), unit=" years")
    if kind == "consec":
        n = r.randint(10, 90)
        return QN("The sum of three consecutive numbers is %d. What is the largest?" % (3 * n + 3), n + 2, [n + 1, n, n + 3],
                  "x + (x + 1) + (x + 2) = %d, so 3x + 3 = %d and x = %d. Largest = <b>%d</b>." % (3 * n + 3, 3 * n + 3, n, n + 2))
    if kind == "perim":
        w = r.randint(3, 20)
        d = r.randint(2, 9)
        p = 2 * (2 * w + d)
        return QN("A rectangle is %d cm longer than it is wide. Its perimeter is %d cm. How wide is it?" % (d, p), w, [w + d, p // 4, (p - d) // 2],
                  "2(x + x + %d) = %d, so 4x + %d = %d and <b>x = %d cm</b>." % (d, p, 2 * d, p, w), unit=" cm")
    n, p = r.randint(3, 9), r.choice([12, 15, 20, 25, 30])
    k = r.choice([5, 8, 10, 12, 15, 20])
    return QN("%d pencils and a ₹%d eraser cost ₹%d altogether. How much is one pencil (in rupees)?" % (n, k, n * p + k), p, [(n * p + k) // n if (n * p + k) % n == 0 else p + 5, p + k, n * p],
              "%dx + %d = %d, so %dx = %d and <b>x = %d</b>." % (n, k, n * p + k, n, n * p, p))


def main():
    unit(8, 2, 6, "algebra-play", 13, "A", "Algebra Play: Number Tricks, Sequences and Equations", "algebra play",
         "Using algebra to explain number tricks and patterns, the general term of a sequence, and solving linear equations in one variable (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Algebra Play worksheet (Ganita Prakash Part 2, Chapter 6): number tricks, nth term of a sequence, linear equations and puzzles. 100 questions with answers.",
         "Use a letter for the unknown and keep both sides balanced", "Do the same to both sides of an equation.",
         "<p>Number tricks work because the unknown <b>cancels out</b>: think of x, double it, add 10, halve it, take away x → always 5.</p>"
         "<p>A sequence that goes up by d each time has nth term <b>dn + c</b>, such as 5, 8, 11, … = 3n + 2.</p>"
         "<p>To solve an equation, collect the letter terms on one side and the numbers on the other, doing the same to both sides.</p>",
         [("Solve 5x − 7 = 2x + 8.", ["3x − 7 = 8", "3x = 15"], "x = 5"),
          ("Find the nth term of 4, 9, 14, 19, …", ["Goes up by 5: 5n", "5n − 1 gives 4"], "5n − 1")],
         ["Moving a term across the equals sign without changing its sign.", "Multiplying only the first term of a bracket.", "Writing the nth term of 4, 9, 14 as n + 5."],
         [("Why do 'think of a number' tricks work?", "Writing the number as x shows that the steps cancel x, so the answer does not depend on the starting number."),
          ("How do you find the nth term of a sequence?", "If it goes up by d each time, the nth term is dn + c, where c makes the first term right."),
          ("How do you solve an equation with the unknown on both sides?", "Subtract the smaller letter term from both sides, then solve the simpler equation.")],
         [("Number tricks and general terms", [(one_trick, 12), (gb(sq.one_use), 8)]),
          ("Sequences and the nth term", [(gb(sq.one_find_nth), 10), (gb(sq.one_next), 10)]),
          ("Unknowns on both sides", [(gb(eq.one_basic), 10), (gb(eq.one_neg), 10)]),
          ("Equations with brackets", [(gb(eq.one_br), 20)]),
          ("Puzzles with equations", [(one_expr, 20)])], R)


if __name__ == "__main__":
    main()
