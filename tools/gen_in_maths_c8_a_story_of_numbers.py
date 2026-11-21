# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 3: A Story of Numbers
  python3 tools/gen_in_maths_c8_a_story_of_numbers.py
How people wrote numbers: tally marks and grouping, Roman numerals, Egyptian hieroglyph values, place-value systems in
other bases (base 2, base 5, the Mesopotamian base 60) and the Indian place-value system with zero.
Wrong answers come from real mistakes: adding a smaller Roman symbol that should be subtracted (IX as 11), reading base-2
digits as base-10, and forgetting that a place is worth base × the place to its right.
"""
import random
from in_common import num, unit, T, QN

R = random.Random(908003)
RM = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def roman(n):
    s = ""
    for v, t in RM:
        while n >= v:
            s += t
            n -= v
    return s


def naive(n):   # 4 -> IIII, 9 -> VIIII (no subtraction)
    s = ""
    for v, t in [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]:
        while n >= v:
            s += t
            n -= v
    return s


def one_roman(r):
    n = r.choice([x for x in range(14, 2000) if any(k in roman(x) for k in ("IV", "IX", "XL", "XC", "CD", "CM"))])
    if r.random() < 0.5:
        s = roman(n)
        wrong_add = sum(dict((t, v) for v, t in RM if len(t) == 1)[c] for c in s)
        return QN("What number is the Roman numeral %s?" % s, n, [wrong_add, n + 2 if n + 2 != wrong_add else n - 2, n + 10],
                  "%s = <b>%s</b>. A smaller symbol before a larger one is subtracted." % (s, num(n)))
    return T("Write %s in Roman numerals." % num(n), roman(n), [naive(n), roman(n + 2), roman(n - 1) if roman(n - 1) != naive(n) else roman(n + 10)],
             "<b>%s</b>." % roman(n))


def digits(n, b):
    d = []
    while n:
        d.append(n % b)
        n //= b
    return "".join(map(str, reversed(d))) or "0"


def one_base(r):
    b = r.choice([2, 2, 5])
    n = r.randint(5, 60 if b == 2 else 120)
    s = digits(n, b)
    if r.random() < 0.5:
        places = " + ".join("%s × %d" % (c, b ** i) for i, c in enumerate(reversed(s)) if c != "0")
        return QN("A number is written in base %d as %s. What is it in our base-10 system?" % (b, s), n, [sum(map(int, s)), n * 2, n + b],
                  "Places are worth %s from the right. %s = <b>%d</b>." % (", ".join(str(b ** i) for i in range(len(s))), places, n))
    w = [digits(n + 1, b), digits(n - 1, b), s[::-1] if s[::-1] != s and s[-1] != "0" else digits(n + 2, b)]
    return T("Write %d in base %d." % (n, b), s, w, "Use the place values %s: %d = <b>%s</b> in base %d." % (", ".join(str(b ** i) for i in reversed(range(len(s)))), n, s, b))


def one_places(r):
    kind = r.choice(["b60", "b60", "egypt", "place", "zero", "count"])
    if kind == "b60":
        a, b = r.randint(1, 20), r.randint(1, 59)
        return QN("In the Mesopotamian base-60 system, a number has %d in the sixties place and %d in the ones place. What is its value?" % (a, b), 60 * a + b,
                  [10 * a + b, a + b, 100 * a + b], "%d × 60 + %d = <b>%s</b>." % (a, b, num(60 * a + b)))
    if kind == "egypt":
        th, h, t, o = r.randint(1, 4), r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
        n = 1000 * th + 100 * h + 10 * t + o
        return QN("An Egyptian number uses %d lotus flowers (1,000 each), %d coils of rope (100 each), %d heel bones (10 each) and %d strokes (1 each). What number is it?" % (th, h, t, o),
                  n, [th + h + t + o, n + 100, int("%d%d%d%d" % (o, t, h, th))], "%d × 1,000 + %d × 100 + %d × 10 + %d = <b>%s</b>." % (th, h, t, o, num(n)))
    if kind == "place":
        b = r.choice([2, 5, 10, 60])
        k = r.randint(2, 4 if b != 60 else 2)
        return QN("In a base-%d place-value system, what is the value of the %s place (counting the ones place as the first)?" % (b, ["", "", "third", "fourth", "fifth"][k]),
                  b ** (k - 1), [b * (k - 1), b ** k, 10 ** (k - 1) if b != 10 else b * k], "Each place is %d times the place to its right: %d<sup>%d</sup> = <b>%s</b>." % (b, b, k - 1, num(b ** (k - 1))))
    if kind == "zero":
        t = r.choice([("Which idea lets the Indian system write any number using only ten digits?", "Place value with a symbol for zero", ["A new symbol for every number", "Adding the values of all symbols", "Subtracting a smaller symbol before a larger one"]),
                      ("Why is a symbol for zero needed in a place-value system?", "To show that a place is empty, as in 305", ["To show a negative number", "To mark the end of a number", "To separate thousands"]),
                      ("Which system has no symbol for zero?", "Roman numerals", ["The Indian (Hindu–Arabic) system", "Base 2", "Base 5"])])
        return T(t[0], t[1], t[2], "<b>%s</b>." % t[1])
    n = r.choice([x for x in range(12, 49) if x % 5])
    return T("How is %d shown with tally marks grouped in fives?" % n, "%d groups of five and %d more" % (n // 5, n % 5),
             ["%d groups of five and %d more" % (n // 5 - 1, n % 5 + 5), "%d groups of five and %d more" % (n // 5 + 1, n % 5), "%d single marks in one row" % (n + 5)],
             "%d = 5 × %d + %d: <b>%d groups of five and %d more</b>." % (n, n // 5, n % 5, n // 5, n % 5))


def main():
    unit(8, 1, 3, "a-story-of-numbers", 3, "N", "A Story of Numbers: Number Systems Through History", "a story of numbers",
         "The development of number systems: counting and grouping, Roman and Egyptian numerals, place-value systems in other bases (2, 5 and 60) and the Indian place-value system with zero (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 A Story of Numbers worksheet (Ganita Prakash Part 1, Chapter 3): Roman numerals, Egyptian numbers, base 2, base 5, base 60 and the Indian place-value system. 100 questions with answers.",
         "Place value: each place is worth base × the place to its right", "With a zero symbol, ten digits are enough for every number.",
         "<p>Early systems added symbols: Egyptian numbers repeat a symbol for 1, 10, 100, 1,000 … Roman numerals also subtract: IV = 4, XC = 90.</p>"
         "<p>A <b>place-value system</b> in base b has places worth 1, b, b², b³ … from the right. Base 2 uses only 0 and 1: 1011 = 8 + 2 + 1 = 11. The Mesopotamians used base 60.</p>"
         "<p>The Indian system is base 10 with a symbol for <b>zero</b>, so any number can be written with ten digits.</p>",
         [("What is 10110 in base 2?", ["Places 16, 8, 4, 2, 1", "16 + 4 + 2"], "22"),
          ("Write 94 in Roman numerals.", ["90 = XC", "4 = IV"], "XCIV")],
         ["Adding every Roman symbol: IX is 9, not 11.", "Reading 101 in base 2 as one hundred and one. It is 4 + 1 = 5.", "Thinking zero is just ‘nothing’. In a place-value system it holds a place."],
         [("How do Roman numerals work?", "I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1,000. Symbols are added, but a smaller symbol before a larger one is subtracted (IV = 4)."),
          ("What is base 2?", "A place-value system with only the digits 0 and 1; the places are worth 1, 2, 4, 8, 16 …"),
          ("Why was zero important?", "It lets a place be empty, so the same ten digits can write every number in a place-value system.")],
         [("Roman numerals", [(one_roman, 20)]),
          ("Ancient systems and tally marks", [(one_places, 20)]),
          ("Base 2 and base 5", [(one_base, 20)]),
          ("Place value in any base", [(one_places, 10), (one_base, 10)]),
          ("Mixed problems", [(one_roman, 8), (one_base, 6), (one_places, 6)])], R)


if __name__ == "__main__":
    main()
