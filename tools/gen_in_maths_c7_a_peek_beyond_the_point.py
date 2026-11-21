# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 3: A Peek Beyond the Point
  python3 tools/gen_in_maths_c7_a_peek_beyond_the_point.py
Decimals: tenths and hundredths, place value of digits after the point, decimals as fractions, decimals on the number line,
comparing decimals, converting units (cm and m, g and kg, paise and rupees), and adding and subtracting decimals.
Wrong answers come from real mistakes: 0.25 thought smaller than 0.3 because 25 > 3 is ignored the other way round (0.25 > 0.3),
lining up the last digits instead of the points, and 5 cm written as 0.5 m.
"""
import random
from fractions import Fraction as F
from in_common import num, unit, T, QN, fr

R = random.Random(907003)


def one_place(r):
    kind = r.choice(["digit", "digit", "frac", "dec"])
    if kind == "digit":
        x = r.randint(1000, 99999)
        s = "%d.%02d" % (x // 100, x % 100)
        k = r.choice([1, 2])
        d = s.split(".")[1][k - 1]
        if d == "0":
            return None
        name = ["tenths", "hundredths"][k - 1]
        return T("In %s, what is the value of the digit %s in the %s place?" % (s, d, name), fr(d, "10" if k == 1 else "100"),
                 [d, fr(d, "100" if k == 1 else "10"), d + "0"], "<b>%s/%s</b>." % (d, "10" if k == 1 else "100"))
    if kind == "frac":
        n = r.randint(1, 99)
        if n % 10 == 0:
            return None
        return T("Write %s as a decimal." % fr(str(n), "100"), "0.%02d" % n, ["0.%d" % n if n >= 10 else "0.%d" % n + "0", "%d.0" % n, "0.00%d" % n], "<b>0.%02d</b>." % n)
    t = r.randint(1, 99)
    if t % 10 == 0:
        return None
    return T("Write 0.%02d as a fraction." % t, fr(str(t), "100"), [fr(str(t), "10"), fr(str(t), "1000"), fr("1", str(t))], "%02d hundredths = <b>%d/100</b>." % (t, t))


def one_cmp(r):
    a = r.randint(1, 9)
    b = r.randint(10, 99)
    x, y = F(a, 10), F(b, 100)
    if x == y:
        return None
    big = max(x, y)
    fmt = lambda v: num(v)
    return T("Which is greater: %s or %s?" % (fmt(x), fmt(y)), fmt(big), [fmt(min(x, y)), "They are equal", fmt(F(b, 10)) if F(b, 10) not in (x, y) else "0.%d" % (a * 11)],
             "Compare tenths first: %s = %s/100 and %s = %d/100, so <b>%s</b>." % (fmt(x), a * 10, fmt(y), b, fmt(big)))


def one_unit(r):
    kind = r.choice(["cm", "g", "p", "mm", "ml"])
    if kind == "cm":
        c = r.randint(1, 450)
        return T("Write %d cm in metres." % c, num(F(c, 100)) + " m", [num(F(c, 10)) + " m", num(F(c, 1000)) + " m", str(c) + " m"], "100 cm = 1 m, so <b>%s m</b>." % num(F(c, 100)))
    if kind == "g":
        g = r.randint(5, 4500)
        if g % 10 == 0:
            return None
        return T("Write %s g in kilograms." % num(g), num(F(g, 1000)) + " kg", [num(F(g, 100)) + " kg", num(F(g, 10)) + " kg", num(F(g, 10000)) + " kg"], "1,000 g = 1 kg: <b>%s kg</b>." % num(F(g, 1000)))
    if kind == "p":
        p = r.randint(105, 9995)
        if p % 5:
            return None
        return T("Write %s paise in rupees." % num(p), "₹%s" % num(F(p, 100)), ["₹%s" % num(F(p, 10)), "₹%s" % num(F(p, 1000)), "₹%s" % num(p)], "100 paise = ₹1: <b>₹%s</b>." % num(F(p, 100)))
    if kind == "mm":
        m = r.randint(1, 99)
        return T("Write %d mm in centimetres." % m, num(F(m, 10)) + " cm", [num(F(m, 100)) + " cm", str(m * 10) + " cm", num(F(m, 1000)) + " cm"], "10 mm = 1 cm: <b>%s cm</b>." % num(F(m, 10)))
    ml = r.randint(5, 4500)
    if ml % 5:
        return None
    return T("Write %s ml in litres." % num(ml), num(F(ml, 1000)) + " litres", [num(F(ml, 100)) + " litres", num(F(ml, 10)) + " litres", num(ml) + " litres"],
             "1,000 ml = 1 litre: <b>%s litres</b>." % num(F(ml, 1000)))


def one_add(r):
    a = F(r.randint(10, 9999), 100)
    b = F(r.randint(1, 99), 10)
    op = r.choice(["+", "−"])
    if op == "−" and b >= a:
        return None
    v = a + b if op == "+" else a - b
    wrong = a + F(b.numerator, 100) if op == "+" else a - F(b.numerator, 100)
    return QN("Work out %s %s %s." % (num(a), op, num(b)), v, [wrong, v + 1, v + F(1, 10)], "Line up the decimal points: <b>%s</b>." % num(v))


def one_story(r):
    kind = r.choice(["shop", "run", "rain"])
    if kind == "shop":
        a, b = F(r.randint(1000, 9999), 100), F(r.randint(1000, 9999), 100)
        return T("Neha buys a book for ₹%s and a pen for ₹%s. How much does she spend?" % (num(a), num(b)), "₹%s" % num(a + b), ["₹%s" % num(a + b + 1), "₹%s" % num(a + b - F(1, 10)), "₹%s" % num(abs(a - b))],
                 "%s + %s = <b>₹%s</b>." % (num(a), num(b), num(a + b)))
    if kind == "run":
        a, b = F(r.randint(15, 95), 10), F(r.randint(5, 50), 100)
        return QN("Arjun ran %s km in the morning and %s km in the evening. How far did he run in all?" % (num(a), num(b)), a + b, [a + F(b.numerator, 10), a + b + 1, abs(a - b)],
                  "%s + %s = <b>%s km</b>." % (num(a), num(b), num(a + b)), unit=" km")
    a, b = F(r.randint(100, 999), 10), F(r.randint(10, 99), 10)
    return QN("A town had %s cm of rain in July and %s cm in August. How much more rain fell in July?" % (num(a), num(b)), a - b, [a + b, a - b + 1, a - F(b.numerator, 100)],
              "%s − %s = <b>%s cm</b>." % (num(a), num(b), num(a - b)), unit=" cm")


def main():
    unit(7, 1, 3, "a-peek-beyond-the-point", 3, "N", "A Peek Beyond the Point: Decimals", "a peek beyond the point",
         "Decimal fractions: tenths and hundredths, place value, decimals on the number line, comparing decimals, units of measurement and adding and subtracting decimals (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 A Peek Beyond the Point worksheet (Ganita Prakash Part 1, Chapter 3): decimals, tenths and hundredths, place value, comparing, unit conversions and adding decimals. 100 questions with answers.",
         "0.1 = one tenth, 0.01 = one hundredth", "Line up the decimal points to add or subtract.",
         "<p>After the decimal point come the <b>tenths</b>, then the <b>hundredths</b>: 3.47 = 3 + 4/10 + 7/100.</p>"
         "<p>To <b>compare</b> decimals, compare the whole parts, then the tenths, then the hundredths: 0.3 = 0.30 is greater than 0.25.</p>"
         "<p>Units: 100 cm = 1 m, 1,000 g = 1 kg, 100 paise = ₹1. To add or subtract, line up the points.</p>",
         [("Which is greater: 0.4 or 0.38?", ["0.4 = 0.40", "40 hundredths > 38 hundredths"], "0.4"),
          ("Work out 12.5 + 3.75.", ["12.50 + 3.75"], "16.25")],
         ["Thinking 0.25 > 0.3 because 25 > 3.", "Lining up the last digits instead of the decimal points.", "Writing 5 cm as 0.5 m (it is 0.05 m)."],
         [("What does each digit after the decimal point mean?", "The first is tenths, the second hundredths, the third thousandths."),
          ("How do you compare decimals?", "Compare the whole numbers, then the tenths, then the hundredths. Writing them with the same number of decimal places helps."),
          ("How do you add decimals?", "Write them with the decimal points in a column and add as with whole numbers.")],
         [("Tenths and hundredths", [(one_place, 20)]),
          ("Comparing decimals", [(one_cmp, 20)]),
          ("Units and decimals", [(one_unit, 20)]),
          ("Adding and subtracting decimals", [(one_add, 20)]),
          ("Decimal problems", [(one_story, 20)])], R)


if __name__ == "__main__":
    main()
