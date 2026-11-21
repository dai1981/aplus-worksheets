# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 6: Number Play
  python3 tools/gen_in_maths_c7_number_play.py
Parity (odd and even sums and products, and of expressions like 2n + 1), magic squares (the magic sum, the centre
number, missing numbers), the Virahanka–Fibonacci sequence, and digits in disguise (cryptarithms). The cryptarithms reuse
the Class 8 maker.
Wrong answers come from real mistakes: an odd number of odd numbers giving an even sum, the magic sum taken as the total
of all numbers, and adding the last two terms of the Virahanka sequence in the wrong place.
"""
import random
from in_common import num, unit, T, QN
import gen_in_maths_c8_number_play as c8

R = random.Random(907006)


def one_parity(r):
    kind = r.choice(["expr", "expr", "sum", "grid"])
    if kind == "expr":
        e, ans = r.choice([("2n", "Even"), ("2n + 1", "Odd"), ("2n − 1", "Odd"), ("4n + 2", "Even"), ("2n + 2", "Even"), ("6n + 3", "Odd"), ("n + n", "Even"), ("2n + 7", "Odd")])
        return T("If n is any whole number, is %s odd or even?" % e, ans, ["Even" if ans == "Odd" else "Odd", "It depends on n", "Neither"],
                 "%s is %s for every n: <b>%s</b>." % (e, "a multiple of 2" if ans == "Even" else "one more than a multiple of 2", ans))
    if kind == "sum":
        nums = [r.randint(10, 99) for _ in range(r.randint(4, 7))]
        odd = sum(1 for x in nums if x % 2)
        ans = "Odd" if sum(nums) % 2 else "Even"
        return T("Without adding, is %s odd or even?" % " + ".join(map(str, nums)), ans, ["Even" if ans == "Odd" else "Odd", "It depends on the order", "You must add first"],
                 "There %s %d odd number%s, so the sum is <b>%s</b>." % ("is" if odd == 1 else "are", odd, "" if odd == 1 else "s", ans.lower()))
    rr, c = r.randint(2, 9), r.randint(2, 9)
    ans = "Even" if (rr * c) % 2 == 0 else "Odd"
    return T("A grid has %d rows and %d columns. Is the number of boxes odd or even?" % (rr, c), ans, ["Even" if ans == "Odd" else "Odd", "It depends on the boxes", "Neither"],
             "%d × %d = %d: <b>%s</b>." % (rr, c, rr * c, ans.lower()))


def one_magic(r):
    base = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    k = r.randint(0, 20)
    sq = [[x + k for x in row] for row in base]
    if r.random() < 0.5:
        sq = [list(x) for x in zip(*sq)]
    if r.random() < 0.5:
        sq = [row[::-1] for row in sq]
    m = 15 + 3 * k
    kind = r.choice(["sum", "centre", "miss", "miss"])
    if kind == "sum":
        lo = 1 + k
        return QN("A magic square uses the numbers %d to %d once each. What is the magic sum (each row, column and diagonal)?" % (lo, lo + 8), m, [sum(range(lo, lo + 9)), m + 3, 5 + k],
                  "Total %d ÷ 3 rows = <b>%d</b>." % (sum(range(lo, lo + 9)), m))
    if kind == "centre":
        return QN("In a 3 × 3 magic square with magic sum %d, what number is in the centre?" % m, m // 3, [m // 2, m // 3 + 1, m - 10], "The centre is always the magic sum ÷ 3 = <b>%d</b>." % (m // 3))
    i, j = r.randrange(3), r.randrange(3)
    v = sq[i][j]
    cells = [["?" if (a, b) == (i, j) else str(sq[a][b]) for b in range(3)] for a in range(3)]
    grid = "<br>".join(" | ".join(row) for row in cells)
    return QN("Find the missing number in this magic square (magic sum %d):<br>%s" % (m, grid), v, [v + 1, m - v, v - 2 if v > 2 else v + 3], "Use the row or column with the ?: <b>%d</b>." % v)


def fib(n):
    a, b = 1, 2
    for _ in range(n - 1):
        a, b = b, a + b
    return a


def one_vir(r):
    kind = r.choice(["next", "next", "rhythm", "nth"])
    if kind == "next":
        s = r.randint(3, 10)
        t = [fib(i) for i in range(s, s + 4)]
        return QN("Virahanka numbers: %s, … What comes next?" % ", ".join(map(str, t)), t[-1] + t[-2], [t[-1] * 2, t[-1] + t[0], t[-1] + 1], "%d + %d = <b>%d</b>." % (t[-2], t[-1], t[-1] + t[-2]))
    if kind == "rhythm":
        n = r.randint(3, 10)
        return QN("Using short beats (1) and long beats (2), how many rhythms have a total of %d beats? (1 → 1 way, 2 → 2 ways, 3 → 3 ways …)" % n, fib(n), [fib(n - 1), 2 ** (n - 1), fib(n) + 1],
                  "Each count is the sum of the two before: <b>%d</b>." % fib(n))
    n = r.randint(6, 12)
    return QN("In the Virahanka sequence 1, 2, 3, 5, 8, …, what is the %dth number?" % n, fib(n), [fib(n - 1), fib(n + 1), fib(n) - 1], "Keep adding the last two: <b>%d</b>." % fib(n))


def main():
    unit(7, 1, 6, "number-play", 6, "N", "Number Play: Parity, Magic Squares and Virahanka Numbers", "number play",
         "Parity of sums and expressions, magic squares, the Virahanka–Fibonacci numbers and digit puzzles (cryptarithms) (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Number Play worksheet (Ganita Prakash Part 1, Chapter 6): odd and even, magic squares, Virahanka numbers and cryptarithms. 100 questions with answers.",
         "2n is always even; 2n + 1 is always odd", "In a 3 × 3 magic square, the centre is the magic sum ÷ 3.",
         "<p><b>Parity</b>: a sum is odd only if it has an odd number of odd terms. Every even number is 2n and every odd number is 2n + 1.</p>"
         "<p>In a <b>magic square</b> every row, column and diagonal has the same sum. With 1 to 9 the magic sum is 45 ÷ 3 = 15 and the centre is 5.</p>"
         "<p>The <b>Virahanka numbers</b> 1, 2, 3, 5, 8, 13, … count rhythms of short and long beats; each is the sum of the two before.</p>",
         [("Is 37 + 54 + 19 odd or even?", ["Two odd numbers: 37 and 19"], "Even"),
          ("Magic square with 1 to 9: what is the magic sum?", ["1 + 2 + … + 9 = 45", "45 ÷ 3"], "15")],
         ["Thinking any sum of odd numbers is odd (two odds make an even).", "Taking the magic sum as the total of all nine numbers.", "Adding the wrong two terms in the Virahanka sequence."],
         [("When is a sum odd?", "When it contains an odd number of odd numbers."),
          ("What is a magic square?", "A square grid of numbers in which every row, column and diagonal adds up to the same number."),
          ("What are Virahanka numbers?", "1, 2, 3, 5, 8, 13, 21, … — the number of rhythms made from short and long beats, described by Virahanka about 1,300 years ago.")],
         [("Odd and even", [(one_parity, 20)]),
          ("Magic squares", [(one_magic, 20)]),
          ("Virahanka numbers", [(one_vir, 16), (one_parity, 4)]),
          ("Digits in disguise", [(c8.one_crypt, 20)]),
          ("Mixed number play", [(one_parity, 8), (one_magic, 8), (one_vir, 4)])], R)


if __name__ == "__main__":
    main()
