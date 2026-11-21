# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 10: The Other Side of Zero
  python3 tools/gen_in_maths_c6_the_other_side_of_zero.py
Negative numbers in daily life (floors below ground, temperatures, bank balances), integers on the number line,
comparing and ordering integers, and adding and subtracting integers (Brahmagupta's rules), with word problems.
Wrong answers come from real mistakes: −7 thought larger than −3, a sign lost when subtracting a negative, and moving
the wrong way on the number line.
"""
import random
from in_common import num, unit, T, QN, adopt, gb, MINUS
import gen_uk_maths_y7_negative_numbers as ng
import gen_uk_maths_y7_place_value_and_ordering as po

R = random.Random(906010)
adopt(ng, R)
adopt(po, R)
sn = lambda v: (MINUS + str(-v)) if v < 0 else str(v)


def one_cmp(r):
    kind = r.choice(["greater", "greater", "smaller", "between"])
    a, b = r.sample(range(-20, 21), 2)
    if kind in ("greater", "smaller"):
        if a > 0 and b > 0:
            return None
        ans = max(a, b) if kind == "greater" else min(a, b)
        return T("Which is %s: %s or %s?" % (kind, sn(a), sn(b)), sn(ans), [sn(min(a, b) if kind == "greater" else max(a, b)), "They are equal", sn(abs(ans)) if ans < 0 else sn(-ans)],
                 "On the number line the %s number is further %s: <b>%s</b>." % (kind, "right" if kind == "greater" else "left", sn(ans)))
    lo, hi = sorted((a, b))
    if hi - lo < 2:
        return None
    return QN("How many integers lie between %s and %s?" % (sn(lo), sn(hi)), hi - lo - 1, [hi - lo, hi - lo + 1, abs(abs(hi) - abs(lo)) if abs(abs(hi) - abs(lo)) not in (hi - lo - 1, hi - lo, hi - lo + 1) else hi - lo + 2],
              "From %s to %s there are %d steps, so <b>%d</b> integers in between." % (sn(lo), sn(hi), hi - lo, hi - lo - 1))


def one_life(r):
    kind = r.choice(["lift", "temp", "bank", "sea"])
    if kind == "lift":
        s = r.randint(-3, 8)
        m = r.choice([-1, 1]) * r.randint(2, 9)
        e = s + m
        fl = lambda v: "ground floor" if v == 0 else ("floor %s" % sn(v))
        return T("A lift is at %s. It goes %s %d floors. Which floor is it at now? (Floors below ground are negative.)" % (fl(s), "up" if m > 0 else "down", abs(m)), fl(e),
                 [fl(s - m), fl(e + 1), fl(-e) if e != 0 else fl(1)], "%s %s %d = <b>%s</b>." % (sn(s), "+" if m > 0 else MINUS, abs(m), fl(e)))
    if kind == "temp":
        t = r.randint(-8, 15)
        d = r.randint(3, 15)
        return QN("The temperature in Leh is %s°C at noon. By midnight it falls by %d°C. What is the temperature at midnight?" % (sn(t), d), t - d, [t + d, d - t, t - d + 2],
                  "%s − %d = <b>%s°C</b>." % (sn(t), d, sn(t - d)), unit="°C")
    if kind == "bank":
        b = r.choice([500, 800, 1000, 1500, 2000])
        w = b + r.choice([200, 300, 500, 700])
        return T("Ravi has ₹%s in his account and takes out ₹%s (the bank allows an overdraft). What is his balance now?" % (num(b), num(w)), "%s₹%s" % (MINUS, num(w - b)),
                 ["₹%s" % num(w - b), "₹%s" % num(w + b), "%s₹%s" % (MINUS, num(w + b))], "%s − %s = <b>%s₹%s</b>." % (num(b), num(w), MINUS, num(w - b)))
    h, d = r.randint(50, 900), r.randint(20, 300)
    return QN("A bird is %d m above sea level and a fish is %d m below sea level. How far apart are they vertically?" % (h, d), h + d, [h - d, abs(d - h) + 10, h + d + 100],
              "%d − (%s%d) = %d + %d = <b>%d m</b>." % (h, MINUS, d, h, d, h + d), unit=" m")


def main():
    unit(6, 0, 10, "the-other-side-of-zero", 10, "N", "The Other Side of Zero: Integers", "the other side of zero",
         "Negative numbers and integers, the number line, comparing integers, and adding and subtracting integers in daily-life situations (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 The Other Side of Zero worksheet (Ganita Prakash Chapter 10): integers, number line, comparing integers, adding and subtracting negative numbers. 100 questions with answers.",
         "Subtracting a negative is the same as adding", "On the number line, numbers increase to the right: −7 < −3 < 0 < 2.",
         "<p>Numbers less than zero are <b>negative</b>: floors below ground, temperatures below 0°C, a debt. Together with 0 and the positive whole numbers they are the <b>integers</b>.</p>"
         "<p>On the number line, the number further right is greater, so −3 &gt; −7.</p>"
         "<p>Adding a negative moves left: 5 + (−8) = −3. Subtracting a negative moves right: 2 − (−6) = 8. Brahmagupta wrote rules like these in 628 CE.</p>",
         [("Work out −4 + 9.", ["Start at −4, move 9 right"], "5"),
          ("Work out 3 − (−5).", ["Subtracting −5 is adding 5"], "8")],
         ["Thinking −7 is greater than −3 because 7 is greater than 3.", "Losing a sign: 3 − (−5) = −2 instead of 8.", "Moving left when adding a positive number."],
         [("What are integers?", "The whole numbers 0, 1, 2, 3, … together with the negative numbers −1, −2, −3, …."),
          ("Which is greater, −2 or −9?", "−2, because it is to the right of −9 on the number line."),
          ("What happens when you subtract a negative number?", "It is the same as adding the positive number: a − (−b) = a + b.")],
         [("Comparing integers", [(one_cmp, 16), (gb(po.one_neg_order), 4)]),
          ("Adding integers", [(gb(ng.one_add), 20)]),
          ("Subtracting integers", [(gb(ng.one_sub_pos), 10), (gb(ng.one_sub_neg), 10)]),
          ("Mixed calculations", [(gb(ng.one_add), 7), (gb(ng.one_sub_neg), 7), (gb(ng.one_sub_pos), 6)]),
          ("Integers in daily life", [(one_life, 20)])], R)


if __name__ == "__main__":
    main()
