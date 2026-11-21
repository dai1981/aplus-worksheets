# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 5: Number Play
  python3 tools/gen_in_maths_c8_number_play.py
Divisibility tests (2, 3, 4, 5, 6, 8, 9, 10, 11), missing digits, remainders from digit sums, the parity of sums and
products, consecutive numbers, and number puzzles (reversing and subtracting, digit cryptarithms).
Wrong answers come from real mistakes: the test for 4 applied to the last digit only, a number divisible by 3 and 4
taken as divisible by 6 only, and the digit sum used for 11 instead of the alternating sum.
"""
import random
from in_common import num, unit, T, QN

R = random.Random(908005)


def one_div(r):
    d = r.choice([3, 4, 6, 8, 9, 11, 11, 4, 9])
    while True:
        n = r.randint(1000, 99999)
        if n % d == 0 and n % 10:
            break
    test = {3: "the digit sum %d is divisible by 3" % sum(map(int, str(n))), 9: "the digit sum %d is divisible by 9" % sum(map(int, str(n))),
            4: "the last two digits %02d form a multiple of 4" % (n % 100), 8: "the last three digits %03d form a multiple of 8" % (n % 1000),
            6: "it is even and its digit sum %d is divisible by 3" % sum(map(int, str(n))),
            11: "the alternating digit sum is a multiple of 11"}[d]
    others = []
    while len(others) < 3:
        m = n + r.choice([-1, 1]) * r.randint(1, 40)
        if m % d and m not in others and m % 10:
            others.append(m)
    lst = ", ".join(num(x) for x in sorted(others + [n]))
    return T("Which of these numbers is divisible by %d: %s?" % (d, lst), num(n), [num(x) for x in others], "<b>%s</b>: %s." % (num(n), test))


def one_missing(r):
    d = r.choice([9, 11, 9])
    while True:
        s = list(str(r.randint(10000, 99999)))
        i = r.randrange(1, 5)
        cands = [x for x in range(10) if int("".join(s[:i] + [str(x)] + s[i + 1:])) % d == 0]
        if len(cands) == 1:
            x = cands[0]
            break
    shown = "".join(s[:i] + ["□"] + s[i + 1:])
    w = [y for y in range(10) if y != x]
    r.shuffle(w)
    return QN("What digit goes in the box so that %s is divisible by %d?" % (shown, d), x, w[:3],
              "Try the test for %d: only <b>%d</b> works (%s)." % (d, x, num(int("".join(s[:i] + [str(x)] + s[i + 1:])))))


def one_rem(r):
    kind = r.choice(["r9", "r9", "r3", "parity", "parity2"])
    if kind in ("r9", "r3"):
        d = 9 if kind == "r9" else 3
        n = r.randint(10000, 999999)
        while n % d == 0:
            n += 1
        ds = sum(map(int, str(n)))
        return QN("What is the remainder when %s is divided by %d? (Use the digit sum.)" % (num(n), d), n % d, [ds % 10, d - n % d, (n % 10) % d if (n % 10) % d != n % d else n % d + 1],
                  "Digit sum = %d, and %d leaves remainder <b>%d</b> when divided by %d." % (ds, ds, n % d, d))
    if kind == "parity":
        k = r.randint(5, 20)
        odd = r.randint(1, k)
        res = "Odd" if odd % 2 else "Even"
        return T("%d numbers are added. %d of them are odd and the rest are even. Is the sum odd or even?" % (k, odd), res, ["Even" if res == "Odd" else "Odd", "It depends on the numbers", "Neither"],
                 "Only the odd numbers matter: %d odd numbers make an <b>%s</b> sum." % (odd, res.lower()))
    a, b = r.choice([("odd", "odd"), ("odd", "even"), ("even", "even")])
    res = "odd" if a == b == "odd" else "even"
    return T("Is the product of an %s number and an %s number odd or even?" % (a, b), res.capitalize(), ["Even" if res == "odd" else "Odd", "It depends on the numbers", "Neither"],
             "A product is odd only when both numbers are odd, so it is <b>%s</b>." % res)


def one_puzzle(r):
    kind = r.choice(["consec", "consec", "rev", "rev3", "sum1n"])
    if kind == "consec":
        k = r.choice([3, 5])
        m = r.randint(10, 80)
        s = k * m
        return QN("The sum of %d consecutive numbers is %d. What is the smallest of them?" % (k, s), m - k // 2, [m, s // k + k // 2, m - k],
                  "The middle number is %d ÷ %d = %d, so the smallest is <b>%d</b>." % (s, k, m, m - k // 2))
    if kind == "rev":
        a, b = r.sample(range(1, 10), 2)
        n, m = 10 * a + b, 10 * b + a
        return QN("Take %d, reverse its digits and subtract the smaller from the larger. What do you get?" % n, abs(n - m), [n + m, abs(a - b), abs(n - m) + 9],
                  "%d − %d = <b>%d</b>, always 9 × (difference of the digits)." % (max(n, m), min(n, m), abs(n - m)))
    if kind == "rev3":
        a, c = r.sample(range(1, 10), 2)
        b = r.randint(0, 9)
        n, m = 100 * a + 10 * b + c, 100 * c + 10 * b + a
        return QN("Take %d, reverse its digits and subtract the smaller from the larger. What do you get?" % n, abs(n - m), [abs(n - m) + 90, abs(a - c) * 9, n + m],
                  "%d − %d = <b>%d</b> = 99 × %d." % (max(n, m), min(n, m), abs(n - m), abs(a - c)))
    n = r.randint(10, 60)
    return QN("What is 1 + 2 + 3 + … + %d?" % n, n * (n + 1) // 2, [n * n, n * (n + 1), n * (n - 1) // 2],
              "n(n + 1) ÷ 2 = %d × %d ÷ 2 = <b>%s</b>." % (n, n + 1, num(n * (n + 1) // 2)))


def one_crypt(r):
    while True:
        a, b = r.randint(12, 89), r.randint(12, 89)
        s = a + b
        if s >= 100 or a % 10 == b % 10:
            continue
        break
    pos = r.choice(["a1", "b1"])
    if pos == "a1":
        x = a % 10
        shown = "%d□ + %d = %d" % (a // 10, b, s)
    else:
        x = b // 10
        shown = "%d + □%d = %d" % (a, b % 10, s)
    w = [(x + 1) % 10, (x + 9) % 10, (x + 2) % 10]
    return QN("Find the missing digit: %s" % shown, x, w, "Work it out column by column: the digit is <b>%d</b> (%d + %d = %d)." % (x, a, b, s))


def main():
    unit(8, 1, 5, "number-play", 5, "N", "Number Play: Divisibility, Remainders and Number Puzzles", "number play",
         "Divisibility tests, remainders and digit sums, parity, consecutive numbers and number puzzles (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Number Play worksheet (Ganita Prakash Part 1, Chapter 5): divisibility rules, missing digits, remainders, parity and number puzzles. 100 questions with answers.",
         "Divisible by 9 ⇔ the digit sum is divisible by 9", "By 4: last two digits; by 8: last three; by 11: alternating sum.",
         "<p><b>Divisibility tests</b>: by 3 or 9, use the digit sum; by 4, the last two digits; by 8, the last three digits; by 6, test 2 and 3; by 11, the alternating sum of digits.</p>"
         "<p>A number and its digit sum leave the <b>same remainder</b> when divided by 9 (or 3).</p>"
         "<p>A sum is odd when it has an odd number of odd terms; a product is odd only when every factor is odd.</p>",
         [("Is 7,128 divisible by 8?", ["Last three digits: 128 = 8 × 16"], "Yes"),
          ("Find the remainder when 52,417 is divided by 9.", ["Digit sum = 19", "19 = 2 × 9 + 1"], "1")],
         ["Testing divisibility by 4 with the last digit only.", "Using the plain digit sum for 11 instead of the alternating sum.", "Thinking an even number of numbers always has an even sum."],
         [("How do you check divisibility by 11?", "Add the digits in odd places and in even places; if the difference is 0 or a multiple of 11, the number is divisible by 11."),
          ("Why does the digit sum give the remainder for 9?", "Because 10, 100, 1,000 … each leave remainder 1 when divided by 9."),
          ("When is a sum of whole numbers odd?", "When it contains an odd number of odd numbers.")],
         [("Divisibility tests", [(one_div, 20)]),
          ("Missing digits", [(one_missing, 14), (one_crypt, 6)]),
          ("Remainders and parity", [(one_rem, 20)]),
          ("Number puzzles", [(one_puzzle, 20)]),
          ("Mixed number play", [(one_div, 5), (one_missing, 5), (one_rem, 5), (one_puzzle, 5)])], R)


if __name__ == "__main__":
    main()
