# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 2: Operations with Integers
  python3 tools/gen_in_maths_c7_operations_with_integers.py
Adding and subtracting integers (revision), multiplying and dividing integers (sign rules), squares of negative numbers,
the order of operations with integers, and problems (temperature changes, scores, profit and loss).
Wrong answers come from real mistakes: (−) × (−) taken as negative, −3² read as (−3)², and adding instead of
multiplying the signs.
"""
import random
from in_common import unit, QN, adopt, gb, MINUS
import gen_uk_maths_y7_negative_numbers as ng
import gen_au_maths_y8_integers_and_rational_numbers as ai

R = random.Random(907010)
adopt(ng, R)
adopt(ai, R)
sn = lambda v: (MINUS + str(-v)) if v < 0 else str(v)


def one_story(r):
    kind = r.choice(["temp", "quiz", "shop", "dive"])
    if kind == "temp":
        d, h = r.randint(2, 5), r.randint(3, 8)
        t0 = r.randint(-5, 10)
        return QN("The temperature is %s°C and falls by %d°C every hour. What is it after %d hours?" % (sn(t0), d, h), t0 - d * h, [t0 + d * h, -d * h, t0 - d - h],
                  "%s − %d × %d = <b>%s°C</b>." % (sn(t0), d, h, sn(t0 - d * h)), unit="°C")
    if kind == "quiz":
        c, w = r.randint(3, 15), r.randint(2, 12)
        return QN("In a quiz, a correct answer gets +4 and a wrong answer gets −2. Kavya gets %d right and %d wrong. What is her score?" % (c, w), 4 * c - 2 * w, [4 * c + 2 * w, 4 * c - w, 2 * (c - w)],
                  "%d × 4 + %d × (−2) = %d − %d = <b>%s</b>." % (c, w, 4 * c, 2 * w, sn(4 * c - 2 * w)))
    if kind == "shop":
        p, l = r.randint(2, 9) * 50, r.randint(2, 9) * 50
        dp, dl = r.randint(2, 5), r.randint(2, 5)
        v = p * dp - l * dl
        return QN("A shop makes a profit of ₹%d a day on %d days and a loss of ₹%d a day on %d days. What is the total (profit +, loss −) in rupees?" % (p, dp, l, dl), v,
                  [p * dp + l * dl, p - l, -v if v else 50], "%d × %d − %d × %d = <b>%s</b>." % (p, dp, l, dl, sn(v)))
    k, d = r.randint(3, 9), r.choice([5, 6, 8, 10])
    return QN("A diver goes down %d m every minute from the surface (0 m). Where is she after %d minutes? (Below the surface is negative.)" % (d, k), -d * k, [d * k, -d - k, -d * (k - 1)],
              "%d × (−%d) = <b>%s m</b>." % (k, d, sn(-d * k)), unit=" m")


def main():
    unit(7, 2, 2, "operations-with-integers", 10, "N", "Operations with Integers: Multiplying and Dividing Integers", "operations with integers",
         "Addition, subtraction, multiplication and division of integers, properties of operations with integers and problems in daily life (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Operations with Integers worksheet (Ganita Prakash Part 2, Chapter 2): adding, subtracting, multiplying and dividing integers, sign rules and word problems. 100 questions with answers.",
         "Same signs → positive; different signs → negative", "(−3) × (−4) = 12; (−12) ÷ 4 = −3.",
         "<p>Adding a negative moves left on the number line; subtracting a negative moves right: 5 − (−3) = 8.</p>"
         "<p><b>Multiplying or dividing</b>: if the signs are the same the answer is positive, if they are different it is negative. (−6) × (−7) = 42, (−6) × 7 = −42, 42 ÷ (−6) = −7.</p>"
         "<p>(−3)² = 9, but −3² = −9 (the square comes before the minus).</p>",
         [("Work out (−8) × (−5).", ["Same signs: positive"], "40"),
          ("Work out −36 ÷ 4.", ["Different signs: negative"], "−9")],
         ["Thinking a negative times a negative is negative.", "Reading −3² as 9 (it is −9; (−3)² is 9).", "Adding the numbers instead of multiplying them."],
         [("Why is a negative times a negative positive?", "Multiplying by −1 reverses direction on the number line; reversing twice brings you back to the positive side."),
          ("What are the sign rules for division?", "The same as for multiplication: same signs give a positive answer, different signs a negative one."),
          ("Is (−5)² the same as −5²?", "No. (−5)² = 25 but −5² = −25.")],
         [("Adding and subtracting integers", [(gb(ng.one_add), 7), (gb(ng.one_sub_pos), 6), (gb(ng.one_sub_neg), 7)]),
          ("Multiplying integers", [(gb(ng.one_mul), 10), (gb(ai.one_mul), 10)]),
          ("Dividing integers", [(gb(ng.one_div), 10), (gb(ai.one_div), 10)]),
          ("Squares and order of operations", [(gb(ng.one_sq), 8), (gb(ng.one_mixed), 6), (gb(ai.one_mixed), 6)]),
          ("Integers in daily life", [(one_story, 20)])], R)


if __name__ == "__main__":
    main()
