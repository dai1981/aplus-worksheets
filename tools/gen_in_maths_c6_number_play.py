# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 3: Number Play
  python3 tools/gen_in_maths_c6_number_play.py
Supercells (a number bigger than its neighbours), patterns of numbers on the number line, palindromes (reverse and add),
the Kaprekar routine (6174), digit sums, the Collatz sequence, and estimating large quantities.
Wrong answers come from real mistakes: subtracting the numbers in the wrong order in the Kaprekar step, forgetting to
reverse all the digits, and halving an odd number in the Collatz rule.
"""
import random
from in_common import num, unit, T, QN

R = random.Random(906003)


def one_super(r):
    xs = r.sample(range(100, 999), 5)
    i = r.randrange(5)
    sup = [j for j in range(5) if all(xs[j] > xs[k] for k in (j - 1, j + 1) if 0 <= k < 5)]
    return QN("A cell is a <b>supercell</b> if its number is greater than the numbers next to it. In the row %s, how many supercells are there?" % " | ".join(num(x) for x in xs),
              len(sup), [len(sup) + 1, 5 - len(sup) if 5 - len(sup) != len(sup) else len(sup) + 2, max(len(sup) - 1, 0) if len(sup) > 1 else 4],
              "Supercells: %s. That makes <b>%d</b>." % (", ".join(num(xs[j]) for j in sup), len(sup)))


def one_pal(r):
    kind = r.choice(["rev", "rev", "is", "count"])
    if kind == "rev":
        n = r.randint(12, 98)
        if n % 10 == 0 or str(n) == str(n)[::-1]:
            return None
        s = n + int(str(n)[::-1])
        steps = 1
        while str(s) != str(s)[::-1] and steps < 3:
            s += int(str(s)[::-1])
            steps += 1
        if str(s) != str(s)[::-1]:
            return None
        first = n + int(str(n)[::-1])
        return QN("Reverse the digits of %d and add: %d + %s. Keep reversing and adding until you get a palindrome. Which palindrome do you reach?" % (n, n, str(n)[::-1]), s,
                  [first if first != s else s + 11, int(str(n) + str(n)[::-1]), s + 10 if str(s + 10) != str(s + 10)[::-1] else s + 1],
                  "%d + %s = %d … → <b>%s</b>, which reads the same both ways." % (n, str(n)[::-1], first, num(s)))
    if kind == "is":
        p = r.choice([int(str(a) + str(a)[::-1][1:]) for a in range(100, 999)] + [int(str(a) + str(a)[::-1]) for a in range(10, 99)])
        w = []
        while len(w) < 3:
            x = p + r.randint(1, 99)
            if str(x) != str(x)[::-1] and x not in w:
                w.append(x)
        return T("Which of these numbers is a palindrome?", num(p), [num(x) for x in w], "<b>%s</b> reads the same forwards and backwards." % num(p))
    d = r.choice([2, 3, 4])
    c = 9 if d == 2 else 90
    return QN("How many %d-digit palindromes are there?" % d, c, [10 if d == 2 else 100, c * 10, c - 1 if d == 2 else 81],
              "%s: <b>%d</b>." % ("11, 22, …, 99" if d == 2 else "first digit 1–9 and middle digit 0–9 give 9 × 10", c))


def kap(n):
    s = "%04d" % n
    return int("".join(sorted(s, reverse=True))) - int("".join(sorted(s)))


def one_kap(r):
    while True:
        n = r.randint(1000, 9999)
        if len(set(str(n))) >= 2 and n != 6174:
            break
    k = kap(n)
    big, small = "".join(sorted(str(n), reverse=True)), "".join(sorted(str(n)))
    return QN("Kaprekar routine: arrange the digits of %s in decreasing order and in increasing order, and subtract. What do you get?" % num(n), k,
              [int(big) + int(small), int(big) - n if int(big) - n not in (0, k) else k + 99, k + 1000 if k + 1000 < 10000 else k - 1000],
              "%s − %s = <b>%s</b>. Repeating this always reaches 6174." % (num(int(big)), small, num(k)))


def one_collatz(r):
    n = r.randint(3, 60)
    seq = [n]
    while seq[-1] != 1 and len(seq) < 4:
        x = seq[-1]
        seq.append(x // 2 if x % 2 == 0 else 3 * x + 1)
    if len(seq) < 4:
        return None
    x = seq[2]
    nxt = x // 2 if x % 2 == 0 else 3 * x + 1
    return QN("Collatz rule: if a number is even, halve it; if it is odd, multiply by 3 and add 1. Starting at %d you get %d, %d, … What comes next?" % (n, seq[1], seq[2]), nxt,
              [x * 3 + 1 if x % 2 == 0 else x // 2 + 1, x * 2, nxt + 1], "%d is %s, so the next is <b>%d</b>." % (x, "even" if x % 2 == 0 else "odd", nxt))


def one_digits(r):
    kind = r.choice(["sum", "sum", "count", "est"])
    if kind == "sum":
        n = r.randint(1000, 99999)
        return QN("What is the digit sum of %s?" % num(n), sum(map(int, str(n))), [sum(map(int, str(n))) + 1, len(str(n)), sum(map(int, str(n))) - 2],
                  "%s = <b>%d</b>." % (" + ".join(str(n)), sum(map(int, str(n)))))
    if kind == "count":
        a, b = r.choice([(1, 100), (1, 50), (1, 99), (10, 99)])
        d = r.randint(1, 9)
        c = sum(str(x).count(str(d)) for x in range(a, b + 1))
        return QN("How many times is the digit %d written when you write all the numbers from %d to %d?" % (d, a, b), c, [c - 1, c + 9 if c + 9 != c else c + 2, c + 1],
                  "Count it in the ones place and in the tens place: <b>%d</b>." % c)
    t = r.choice([("How many seconds are there in one day?", 86400, [8640, 3600, 1440]), ("About how many days are there in 10 years?", 3652, [365, 1000, 36520]),
                  ("How many minutes are there in one week?", 10080, [1440, 168, 604800]), ("How many hours are there in a year (365 days)?", 8760, [365, 1440, 525600])])
    return QN(t[0], t[1], t[2], "Multiply step by step: <b>%s</b>." % num(t[1]))


def main():
    unit(6, 0, 3, "number-play", 3, "N", "Number Play: Supercells, Palindromes and Number Puzzles", "number play",
         "Numbers in patterns and puzzles: supercells, palindromes, the Kaprekar constant 6174, digit sums, the Collatz conjecture and estimation (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Number Play worksheet (Ganita Prakash Chapter 3): supercells, palindromes, the Kaprekar routine, digit sums, Collatz sequences and estimating. 100 questions with answers.",
         "Numbers hide patterns: 6174 always appears in the Kaprekar routine", "A palindrome reads the same forwards and backwards.",
         "<p>A <b>palindrome</b> reads the same both ways, like 4,334. Reversing a number and adding often leads to a palindrome: 57 + 75 = 132, 132 + 231 = 363.</p>"
         "<p><b>Kaprekar routine</b>: take a 4-digit number, arrange its digits from largest to smallest and smallest to largest, and subtract. Repeat — you always reach 6174.</p>"
         "<p><b>Collatz</b>: halve even numbers, and do 3 × n + 1 for odd numbers. Every starting number tried so far reaches 1.</p>",
         [("Kaprekar step for 3,524.", ["5,432 − 2,345"], "3,087"),
          ("Collatz sequence from 6.", ["6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1"], "It reaches 1")],
         ["Subtracting the larger arrangement from the smaller.", "Forgetting to reverse every digit when making a palindrome.", "Halving an odd number in the Collatz rule instead of doing 3n + 1."],
         [("What is the Kaprekar constant?", "6174. Arranging the digits of a 4-digit number in descending and ascending order and subtracting, again and again, always reaches 6174 (if not all digits are the same)."),
          ("What is a palindrome number?", "A number that reads the same forwards and backwards, such as 121 or 4,554."),
          ("What is the Collatz conjecture?", "The guess that the rule 'halve if even, 3n + 1 if odd' always reaches 1, whatever number you start with.")],
         [("Supercells and digit sums", [(one_super, 10), (one_digits, 10)]),
          ("Palindromes", [(one_pal, 20)]),
          ("The Kaprekar routine", [(one_kap, 20)]),
          ("Collatz sequences", [(one_collatz, 20)]),
          ("Counting and estimating", [(one_digits, 12), (one_pal, 4), (one_super, 4)])], R)


if __name__ == "__main__":
    main()
