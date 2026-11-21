# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 4: Another Peek Beyond the Point
  python3 tools/gen_in_maths_c7_another_peek_beyond_the_point.py
Multiplying and dividing decimals by 10, 100 and 1,000, multiplying a decimal by a whole number and by a decimal,
dividing a decimal by a whole number and by a decimal, and money and measurement problems.
Wrong answers come from real mistakes: moving the point the wrong way, counting the decimal places of only one factor,
and dividing by a decimal without moving both points.
"""
import random
from fractions import Fraction as F
from in_common import num, unit, QN, T

R = random.Random(907012)


def one_ten(r):
    x = F(r.randint(11, 99999), r.choice([10, 100, 1000]))
    k = r.choice([10, 100, 1000])
    if r.random() < 0.5:
        return QN("Work out %s × %d." % (num(x), k), x * k, [x / k, x * k * 10, x * k / 10], "Move the point %d place%s right: <b>%s</b>." % (len(str(k)) - 1, "" if k == 10 else "s", num(x * k)))
    return QN("Work out %s ÷ %d." % (num(x), k), x / k, [x * k, x / k * 10, x / k / 10], "Move the point %d place%s left: <b>%s</b>." % (len(str(k)) - 1, "" if k == 10 else "s", num(x / k)))


def one_mul(r):
    kind = r.choice(["whole", "whole", "dec", "dec"])
    if kind == "whole":
        x = F(r.randint(11, 999), r.choice([10, 100]))
        n = r.randint(2, 12)
        v = x * n
        return QN("Work out %s × %d." % (num(x), n), v, [v * 10, v / 10, v + n], "%s × %d = <b>%s</b>." % (num(x), n, num(v)))
    a, b = F(r.randint(2, 99), 10), F(r.randint(2, 99), 10)
    if a.denominator == 1 or b.denominator == 1:
        return None
    v = a * b
    return QN("Work out %s × %s." % (num(a), num(b)), v, [v * 10, v / 10, a + b], "Multiply %d × %d = %d, then 2 decimal places: <b>%s</b>." % (a * 10, b * 10, a * b * 100, num(v)))


def one_div(r):
    kind = r.choice(["whole", "whole", "dec", "dec"])
    if kind == "whole":
        n = r.randint(2, 9)
        v = F(r.randint(11, 999), 100)
        x = v * n
        return QN("Work out %s ÷ %d." % (num(x), n), v, [v * 10, v / 10, x - n], "%s ÷ %d = <b>%s</b>." % (num(x), n, num(v)))
    d = F(r.randint(2, 9), 10) if r.random() < 0.6 else F(r.randint(2, 25), 100)
    v = r.randint(2, 40)
    x = d * v
    if (x * 100).denominator != 1:
        return None
    return QN("Work out %s ÷ %s." % (num(x), num(d)), v, [F(v, 10), v * 10, x * d if (x * d * 1000).denominator == 1 else v + 1],
              "Multiply both by %d: %s ÷ %s = <b>%d</b>." % (d.denominator, num(x * d.denominator), num(d * d.denominator), v))


def one_story(r):
    kind = r.choice(["cost", "share", "fuel", "cloth"])
    if kind == "cost":
        p = F(r.randint(1001, 9999), 100)
        n = r.randint(2, 9)
        return T("One kg of grapes costs ₹%s. What do %d kg cost?" % (num(p), n), "₹%s" % num(p * n), ["₹%s" % num(p * n * 10), "₹%s" % num(p + n), "₹%s" % num(p * n / 10)],
                 "%s × %d = <b>₹%s</b>." % (num(p), n, num(p * n)))
    if kind == "share":
        n = r.choice([4, 5, 8])
        v = F(r.randint(1001, 9999), 100) if n != 8 else F(r.randint(101, 999), 4)
        tot = v * n
        if (tot * 100).denominator != 1 or (v * 100).denominator != 1:
            return None
        return T("₹%s is shared equally among %d friends. How much does each get?" % (num(tot), n), "₹%s" % num(v), ["₹%s" % num(v * 10), "₹%s" % num(tot - n), "₹%s" % num(v / 10)],
                 "%s ÷ %d = <b>₹%s</b>." % (num(tot), n, num(v)))
    if kind == "fuel":
        m = F(r.randint(120, 480), 10)
        l = F(r.randint(15, 95), 10)
        v = m * l
        return QN("A car goes %s km on 1 litre of petrol. How far does it go on %s litres?" % (num(m), num(l)), v, [v / 10, m + l, v * 10], "%s × %s = <b>%s km</b>." % (num(m), num(l), num(v)), unit=" km")
    piece = F(r.randint(2, 9), 4)
    n = r.randint(3, 12)
    tot = piece * n
    return QN("A cloth %s m long is cut into pieces of %s m each. How many pieces?" % (num(tot), num(piece)), n, [n * 10, F(n, 10), n + 1], "%s ÷ %s = <b>%d</b>." % (num(tot), num(piece), n))


def main():
    unit(7, 2, 4, "another-peek-beyond-the-point", 12, "N", "Another Peek Beyond the Point: Multiplying and Dividing Decimals", "another peek beyond the point",
         "Multiplication and division of decimals by powers of 10, by whole numbers and by decimals, and their use in money and measurement problems (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Another Peek Beyond the Point worksheet (Ganita Prakash Part 2, Chapter 4): multiplying and dividing decimals by 10, 100, 1,000, by whole numbers and by decimals. 100 questions with answers.",
         "Count the decimal places in both numbers", "To divide by a decimal, multiply both numbers by 10 or 100 first.",
         "<p>× 10, 100, 1,000 moves the point 1, 2, 3 places <b>right</b>; ÷ moves it <b>left</b>.</p>"
         "<p>To <b>multiply</b> decimals, multiply as whole numbers, then give the answer as many decimal places as both numbers together: 1.2 × 0.3 = 0.36.</p>"
         "<p>To <b>divide</b> by a decimal, multiply both numbers by the same power of 10 to make the divisor whole: 4.8 ÷ 0.6 = 48 ÷ 6 = 8.</p>",
         [("Work out 2.5 × 1.4.", ["25 × 14 = 350", "2 decimal places"], "3.5"),
          ("Work out 7.2 ÷ 0.08.", ["720 ÷ 8"], "90")],
         ["Moving the decimal point the wrong way when multiplying by 10.", "Counting the decimal places of only one number.", "Dividing by a decimal without changing both numbers."],
         [("How do you multiply two decimals?", "Multiply as whole numbers, then put in as many decimal places as the two numbers have altogether."),
          ("How do you divide by a decimal?", "Multiply both numbers by 10, 100 … until the divisor is a whole number, then divide."),
          ("Why does multiplying by 0.5 make a number smaller?", "0.5 is a half, so you are finding half of the number.")],
         [("Multiplying and dividing by 10, 100 and 1,000", [(one_ten, 20)]),
          ("Multiplying decimals", [(one_mul, 20)]),
          ("Dividing decimals", [(one_div, 20)]),
          ("Mixed calculations", [(one_mul, 7), (one_div, 7), (one_ten, 6)]),
          ("Money and measurement problems", [(one_story, 20)])], R)


if __name__ == "__main__":
    main()
