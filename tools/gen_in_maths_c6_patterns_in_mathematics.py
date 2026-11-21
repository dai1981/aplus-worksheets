# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 1: Patterns in Mathematics
  python3 tools/gen_in_maths_c6_patterns_in_mathematics.py
Number sequences (counting, odd, even, triangular, square, cube numbers, powers of 2 and 3, the Virahanka–Fibonacci
numbers), finding the next term and the rule, adding odd numbers (gives squares), adding counting numbers (gives
triangular numbers) and shape patterns (sides of polygons, dots).
Wrong answers come from real mistakes: adding the same step to a growing pattern, 2n for n², and mixing up triangular
and square numbers.
"""
import random
from in_common import num, unit, T, QN

R = random.Random(906001)
SEQS = [("square numbers", lambda n: n * n), ("triangular numbers", lambda n: n * (n + 1) // 2), ("cube numbers", lambda n: n ** 3),
        ("powers of 2", lambda n: 2 ** (n - 1)), ("powers of 3", lambda n: 3 ** (n - 1)), ("odd numbers", lambda n: 2 * n - 1),
        ("even numbers", lambda n: 2 * n), ("multiples of 7", lambda n: 7 * n)]


def fib(n):
    a, b = 1, 2
    for _ in range(n - 1):
        a, b = b, a + b
    return a


def one_name(r):
    name, f = r.choice(SEQS + [("Virahanka numbers", fib)])
    s = r.randint(1, 3)
    terms = [f(n) for n in range(s, s + 5)]
    others = [x for x, _ in SEQS + [("Virahanka numbers", fib)] if x != name]
    return T("What are these numbers called: %s, …?" % ", ".join(num(t) for t in terms), name.capitalize(), [o.capitalize() for o in r.sample(others, 3)],
             "These are the <b>%s</b>." % name)


def one_next(r):
    kind = r.choice(["seq", "seq", "fib", "step"])
    if kind == "seq":
        name, f = r.choice(SEQS)
        s = r.randint(1, 5)
        terms = [f(n) for n in range(s, s + 4)]
        nxt = f(s + 4)
        return QN("What comes next: %s, …? (These are the %s.)" % (", ".join(num(t) for t in terms), name), nxt,
                  [terms[-1] + (terms[-1] - terms[-2]), nxt + 1, terms[-1] * 2 if terms[-1] * 2 != nxt else nxt + 2],
                  "The next of the %s is <b>%s</b>." % (name, num(nxt)))
    if kind == "fib":
        s = r.randint(2, 8)
        terms = [fib(n) for n in range(s, s + 4)]
        return QN("In the Virahanka sequence each number is the sum of the two before it. What comes next: %s, …?" % ", ".join(map(str, terms)), terms[-1] + terms[-2],
                  [terms[-1] * 2, terms[-1] + 1, terms[-1] + (terms[-1] - terms[-2])], "%d + %d = <b>%d</b>." % (terms[-2], terms[-1], terms[-1] + terms[-2]))
    a, d = r.randint(2, 50), r.randint(3, 15)
    k = r.randint(8, 20)
    return QN("A pattern starts at %d and goes up by %d each time. What is the %dth number?" % (a, d, k), a + (k - 1) * d, [a + k * d, a * k, a + (k - 2) * d],
              "%d + %d × %d = <b>%d</b>." % (a, k - 1, d, a + (k - 1) * d))


def one_sum(r):
    kind = r.choice(["odd", "odd", "count", "count", "tri2"])
    n = r.randint(5, 30)
    if kind == "odd":
        last = 2 * n - 1
        return QN("Find 1 + 3 + 5 + … + %d." % last, n * n, [last * 2, n * (n + 1) // 2, n * n + 1],
                  "These are the first %d odd numbers; their sum is %d × %d = <b>%d</b>." % (n, n, n, n * n))
    if kind == "count":
        return QN("Find 1 + 2 + 3 + … + %d." % n, n * (n + 1) // 2, [n * n, n * (n + 1), n * (n - 1) // 2],
                  "Pair the numbers: %d × %d ÷ 2 = <b>%d</b> (a triangular number)." % (n, n + 1, n * (n + 1) // 2))
    return QN("Add two triangular numbers next to each other: the %dth and the %dth. What kind of number do you get, and what is it?" % (n, n + 1) if False else
              "The %dth triangular number is %d and the next one is %d. What is their sum?" % (n, n * (n + 1) // 2, (n + 1) * (n + 2) // 2), (n + 1) ** 2,
              [(n + 1) * (n + 2) // 2 * 2, n * n, (n + 1) ** 2 + 1], "%d + %d = <b>%d</b> = %d², a square number." % (n * (n + 1) // 2, (n + 1) * (n + 2) // 2, (n + 1) ** 2, n + 1))


def one_shape(r):
    kind = r.choice(["sides", "dots", "sticks", "grid"])
    if kind == "sides":
        names = [("triangle", 3), ("square", 4), ("pentagon", 5), ("hexagon", 6), ("heptagon", 7), ("octagon", 8), ("nonagon", 9), ("decagon", 10)]
        i = r.randrange(len(names) - 1)
        return T("Regular polygons are drawn in order: %s. Which polygon has %d sides?" % (", ".join(n for n, _ in names[:4]) + " and so on", names[i][1]), names[i][0].capitalize(),
                 [x[0].capitalize() for x in r.sample([y for y in names if y != names[i]], 3)], "A polygon with %d sides is a <b>%s</b>." % (names[i][1], names[i][0]))
    if kind == "dots":
        n = r.randint(4, 15)
        return QN("Dots are arranged in squares: 1, 4, 9, 16, … How many dots are in square number %d?" % n, n * n, [4 * n, 2 * n, (n - 1) ** 2 + 1],
                  "Square %d has %d rows of %d: <b>%d</b>." % (n, n, n, n * n))
    if kind == "sticks":
        n = r.randint(4, 20)
        return QN("Squares are made in a row with matchsticks: 1 square uses 4, 2 squares use 7, 3 squares use 10. How many matchsticks for %d squares?" % n, 3 * n + 1,
                  [4 * n, 3 * n, 3 * n + 4], "Each new square adds 3: 4 + 3 × %d = <b>%d</b>." % (n - 1, 3 * n + 1))
    n = r.randint(3, 10)
    return QN("How many small squares of all sizes are there in a %d by %d grid? (1 × 1, 2 × 2, … up to %d × %d)" % (n, n, n, n), sum(k * k for k in range(1, n + 1)),
              [n * n, n * n * 2, sum(k * k for k in range(1, n))], "1² + 2² + … + %d² = <b>%d</b>." % (n, sum(k * k for k in range(1, n + 1))))


def main():
    unit(6, 0, 1, "patterns-in-mathematics", 1, "A", "Patterns in Mathematics: Number Sequences and Shape Patterns", "patterns in mathematics",
         "Number sequences such as odd, even, triangular, square and cube numbers, powers and the Virahanka numbers; relations among sequences; visual patterns (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Patterns in Mathematics worksheet (Ganita Prakash Chapter 1): number sequences, triangular and square numbers, Virahanka numbers, sums of odd numbers and shape patterns. 100 questions with answers.",
         "1 + 3 + 5 + … (n odd numbers) = n × n", "1 + 2 + … + n is a triangular number.",
         "<p>Mathematics is the study of <b>patterns</b>. Famous sequences: odd numbers 1, 3, 5, …; triangular numbers 1, 3, 6, 10, …; square numbers 1, 4, 9, 16, …; powers of 2: 1, 2, 4, 8, ….</p>"
         "<p>Adding odd numbers gives squares: 1 + 3 + 5 = 9 = 3 × 3. Adding counting numbers gives triangular numbers: 1 + 2 + 3 + 4 = 10.</p>"
         "<p>In the <b>Virahanka numbers</b> 1, 2, 3, 5, 8, 13, … each number is the sum of the two before it.</p>",
         [("Find 1 + 3 + 5 + 7 + 9 + 11.", ["Six odd numbers", "6 × 6"], "36"),
          ("What comes next: 1, 3, 6, 10, 15, …?", ["Add 2, 3, 4, 5, then 6"], "21")],
         ["Adding the same step to a pattern that grows faster, like the squares.", "Thinking 6 × 6 is 12 (that is 6 + 6).", "Mixing up triangular numbers (1, 3, 6, 10) and square numbers (1, 4, 9, 16)."],
         [("What are triangular numbers?", "Numbers of dots that make a triangle: 1, 3, 6, 10, 15, … — the sums 1 + 2 + … + n."),
          ("Why does adding odd numbers give square numbers?", "Each odd number adds an L-shaped border to a square of dots, making the next square."),
          ("What are Virahanka numbers?", "The sequence 1, 2, 3, 5, 8, 13, … where each number is the sum of the two before it; Virahanka described it centuries before Fibonacci.")],
         [("Name the sequence", [(one_name, 20)]),
          ("What comes next?", [(one_next, 20)]),
          ("Adding odd and counting numbers", [(one_sum, 20)]),
          ("Shape patterns", [(one_shape, 20)]),
          ("Mixed patterns", [(one_next, 7), (one_sum, 6), (one_shape, 7)])], R)


if __name__ == "__main__":
    main()
