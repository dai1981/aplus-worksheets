# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 7: Finding the Unknown
  python3 tools/gen_in_maths_c7_finding_the_unknown.py
Simple linear equations: one-step and two-step equations, checking a solution, writing an equation from a statement,
and word problems (ages, money, perimeter, think-of-a-number). Reuses the UK Year 7 and AU Year 7 makers.
Wrong answers come from real mistakes: doing the inverse operation to one side only, subtracting instead of dividing,
and solving 3x + 5 = 20 as x = 25 ÷ 3.
"""
import random
from in_common import unit, T, QN, adopt, gb, inr
import gen_uk_maths_y7_solving_equations as uk
import gen_au_maths_y7_solving_linear_equations as au

R = random.Random(907015)
adopt(uk, R)
adopt(au, R)


def one_check(r):
    a, x, b = r.randint(2, 9), r.randint(1, 12), r.randint(1, 20)
    c = a * x + b
    t = x + r.choice([-2, -1, 1, 2]) if r.random() < 0.5 else x
    ok = t == x
    return T("Is x = %d a solution of %dx + %d = %d?" % (t, a, b, c), "Yes" if ok else "No", ["No" if ok else "Yes", "Only if x is even", "You cannot tell"],
             "%d × %d + %d = %d, %s %d: <b>%s</b>." % (a, t, b, a * t + b, "which equals" if ok else "not", c, "Yes" if ok else "No"))


def one_write(r):
    a, b, x = r.randint(2, 6), r.randint(3, 20), r.randint(3, 15)
    c = a * x + b
    return T("‘%d times a number, plus %d, is %d.’ Which equation shows this?" % (a, b, c), "%dx + %d = %d" % (a, b, c),
             ["%d(x + %d) = %d" % (a, b, c), "x + %d = %d × %d" % (b, a, c), "%dx − %d = %d" % (a, b, c)], "<b>%dx + %d = %d</b>, so x = %d." % (a, b, c, x))


def one_word(r):
    kind = r.choice(["age", "money", "perim", "think"])
    if kind == "age":
        x, d = r.randint(8, 15), r.randint(20, 35)
        return QN("A mother is %d years older than her son. The sum of their ages is %d. How old is the son?" % (d, 2 * x + d), x, [x + d, (2 * x + d) // 2, 2 * x + d - d // 2],
                  "x + (x + %d) = %d, so 2x = %d and <b>x = %d</b>." % (d, 2 * x + d, 2 * x, x), unit=" years")
    if kind == "money":
        p, n, k = r.choice([10, 12, 15, 20, 25]), r.randint(3, 9), r.choice([20, 30, 40, 50])
        return QN("Ravi buys %d pens and pays %s with %s change from %s. What is the price of one pen (in rupees)?" % (n, inr(n * p), inr(k), inr(n * p + k)) if False else
                  "Ravi buys %d pens. He pays with %s and gets %s change. What is the price of one pen (in rupees)?" % (n, inr(n * p + k), inr(k)), p, [(n * p + k) // n if (n * p + k) % n == 0 and (n * p + k) // n != p else p + 5, n * p, p + k],
                  "%dx = %d − %d = %d, so <b>x = %d</b>." % (n, n * p + k, k, n * p, p))
    if kind == "perim":
        w = r.randint(3, 20)
        l = w + r.randint(2, 10)
        return QN("A rectangle's length is %d cm more than its width and its perimeter is %d cm. Find the width." % (l - w, 2 * (l + w)), w, [l, (l + w) // 2, 2 * (l + w) // 4],
                  "2(x + x + %d) = %d, so 4x = %d and <b>x = %d cm</b>." % (l - w, 2 * (l + w), 4 * w, w), unit=" cm")
    a, b, x = r.randint(2, 5), r.randint(3, 15), r.randint(3, 20)
    return QN("I think of a number, multiply it by %d and subtract %d. The answer is %d. What was my number?" % (a, b, a * x - b), x, [(a * x - b - b) // a if (a * x - 2 * b) % a == 0 and (a * x - 2 * b) // a != x else x + 2, a * x - b + b, x * a],
              "%dx − %d = %d, so %dx = %d and <b>x = %d</b>." % (a, b, a * x - b, a, a * x, x))


def main():
    unit(7, 2, 7, "finding-the-unknown", 15, "A", "Finding the Unknown: Simple Linear Equations", "finding the unknown",
         "Simple equations in one variable: forming equations, solving them by balancing (doing the same to both sides) and solving word problems (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Finding the Unknown worksheet (Ganita Prakash Part 2, Chapter 7): one-step and two-step equations, checking solutions, forming equations and word problems. 100 questions with answers.",
         "Keep the balance: do the same to both sides", "Undo + and − first, then × and ÷.",
         "<p>An <b>equation</b> says two expressions are equal, like 3x + 5 = 20. Solving it means finding the value of the unknown that makes it true.</p>"
         "<p>Keep it balanced: do the same to both sides. 3x + 5 = 20 → 3x = 15 (subtract 5) → x = 5 (divide by 3). Check: 3 × 5 + 5 = 20.</p>",
         [("Solve 4x − 7 = 21.", ["4x = 28", "x = 28 ÷ 4"], "x = 7"),
          ("Solve x/3 + 2 = 9.", ["x/3 = 7", "x = 21"], "x = 21")],
         ["Doing an operation to one side only.", "Subtracting the number in front of x instead of dividing.", "Adding before dividing in the wrong order (3x + 5 = 20 as x = 25 ÷ 3)."],
         [("What does it mean to solve an equation?", "To find the value of the unknown that makes both sides equal."),
          ("How do you keep an equation balanced?", "Whatever you do to one side — add, subtract, multiply or divide — do the same to the other side."),
          ("How can you check your answer?", "Put the value back into the equation; both sides should be equal.")],
         [("One-step equations", [(gb(uk.one_step), 20)]),
          ("Two-step equations", [(gb(au.one_step), 20)]),
          ("Checking solutions", [(one_check, 20)]),
          ("Writing equations", [(one_write, 20)]),
          ("Word problems", [(one_word, 20)])], R)


if __name__ == "__main__":
    main()
