# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 7: Proportional Reasoning–1
  python3 tools/gen_in_maths_c8_proportional_reasoning_1.py
Ratios and their simplest form, equivalent ratios, checking whether four numbers are in proportion, the unitary method,
sharing in a ratio, and ratio as a fraction of the whole.
Wrong answers come from real mistakes: comparing differences instead of ratios (additive thinking), reversing the order
of a ratio, and dividing by one part instead of the total number of parts.
"""
import random
from in_common import num, unit, T, QN, adopt, gb, inr
import gen_uk_maths_y7_ratio_and_proportion as uk

R = random.Random(908007)
adopt(uk, R)


def one_prop(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    if a == b:
        return None
    k = r.randint(2, 6)
    if r.random() < 0.5:
        return QN("Find x if %d : %d = %d : x." % (a, b, a * k), b * k, [b + a * k - a, b * a, b * k + 1],
                  "%d was multiplied by %d, so x = %d × %d = <b>%d</b>." % (a, k, b, k, b * k))
    yes = r.random() < 0.5
    d = b * k if yes else b * k + r.choice([1, 2, -1])
    return T("Are %d, %d, %d and %d in proportion (%d : %d = %d : %d)?" % (a, b, a * k, d, a, b, a * k, d), "Yes" if yes else "No",
             ["No" if yes else "Yes", "Only if all four are even", "You cannot tell"],
             "%d × %d = %d and %d × %d = %d: products of extremes and means are %s, so <b>%s</b>." % (a, d, a * d, b, a * k, b * a * k, "equal" if yes else "not equal", "Yes" if yes else "No"))


def one_unitary(r):
    kind = r.choice(["cost", "dist", "work"])
    n, m = r.randint(3, 12), r.randint(2, 15)
    if n == m:
        return None
    if kind == "cost":
        p = r.choice([12, 15, 18, 24, 25, 30, 35, 40, 45, 60])
        item = r.choice(["notebooks", "pens", "kg of rice", "mangoes", "bus tickets"])
        return T("%d %s cost %s. How much do %d %s cost?" % (n, item, inr(n * p), m, item), inr(m * p), [inr(n * p + m - n), inr(n * p * m), inr(m * p + p)],
                 "One costs %s ÷ %d = %s, so %d cost <b>%s</b>." % (inr(n * p), n, inr(p), m, inr(m * p)))
    if kind == "dist":
        v = r.choice([40, 45, 50, 60, 72, 80])
        return QN("A car travels %d km in %d hours at a steady speed. How far does it travel in %d hours?" % (v * n, n, m), v * m, [v * n + m, v * n * m // n + v, v * (m + 1)],
                  "%d km per hour × %d = <b>%d km</b>." % (v, m, v * m), unit=" km")
    p = r.randint(2, 6)
    return QN("%d pages are typed in %d minutes. How many pages are typed in %d minutes at the same rate?" % (p * n, n, m), p * m, [p * n + m - n, p * m + p, m],
              "%d pages a minute × %d = <b>%d</b>." % (p, m, p * m))


def one_share(r):
    a, b = r.randint(1, 7), r.randint(1, 7)
    if a == b or __import__("math").gcd(a, b) != 1:
        return None
    one = r.choice([10, 15, 20, 25, 40, 50, 60, 75, 100, 120])
    total = (a + b) * one
    x, y = r.sample(["Asha", "Ravi", "Meena", "Arjun", "Priya", "Kabir", "Neha", "Rohan"], 2)
    who = r.choice([0, 1])
    ans = (a, b)[who] * one
    return T("Share %s between %s and %s in the ratio %d : %d. How much does %s get?" % (inr(total), x, y, a, b, (x, y)[who]), inr(ans),
             [inr((b, a)[who] * one), inr(total // (a, b)[who]) if total % (a, b)[who] == 0 and total // (a, b)[who] != ans else inr(ans + one), inr(total // 2) if total % 2 == 0 and total // 2 != ans else inr(ans * 2)],
             "%d + %d = %d parts. One part = %s ÷ %d = %s, so %s gets %d × %s = <b>%s</b>." % (a, b, a + b, inr(total), a + b, inr(one), (x, y)[who], (a, b)[who], inr(one), inr(ans)))


def one_additive(r):
    a, b = r.randint(2, 6), r.randint(7, 12)
    k = r.randint(2, 4)
    return QN("A drink is made with %d cups of juice and %d cups of water. To make more with the same taste, you use %d cups of juice. How much water?" % (a, b, a * k), b * k,
              [b + a * k - a, b * k - 1, b * a], "Juice is multiplied by %d, so water is too: %d × %d = <b>%d cups</b>. (Adding the same amount changes the taste.)" % (k, b, k, b * k), unit=" cups")


def main():
    unit(8, 1, 7, "proportional-reasoning-1", 7, "N", "Proportional Reasoning–1: Ratios and Proportions", "proportional reasoning 1",
         "Ratios, equivalent ratios, proportion, the unitary method and sharing in a given ratio (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Proportional Reasoning–1 worksheet (Ganita Prakash Part 1, Chapter 7): ratios, simplest form, equivalent ratios, proportions, unitary method and sharing. 100 questions with answers.",
         "a : b = c : d means a × d = b × c", "Multiply or divide both parts of a ratio by the same number.",
         "<p>A <b>ratio</b> a : b compares two quantities by division. Equivalent ratios come from multiplying or dividing both parts by the same number: 6 : 4 = 3 : 2.</p>"
         "<p>Four numbers are in <b>proportion</b> if a : b = c : d, that is a × d = b × c.</p>"
         "<p><b>Unitary method</b>: find the value of one, then multiply. To share in the ratio 2 : 3, split into 5 equal parts.</p>",
         [("Share ₹450 in the ratio 4 : 5.", ["9 parts: 1 part = ₹50"], "₹200 and ₹250"),
          ("Find x if 3 : 8 = 12 : x.", ["3 × 4 = 12, so 8 × 4"], "32")],
         ["Adding the same number to both parts instead of multiplying (additive thinking).", "Writing the ratio in the wrong order.", "Dividing by one part instead of the total number of parts when sharing."],
         [("What is a ratio?", "A comparison of two quantities by division, written a : b."),
          ("How do you check whether four numbers are in proportion?", "a : b = c : d if a × d = b × c."),
          ("What is the unitary method?", "Find the value for one unit, then multiply to find the value for any number of units.")],
         [("Simplifying ratios", [(gb(uk.one_simplify), 20)]),
          ("Equivalent ratios and proportion", [(one_prop, 16), (one_additive, 4)]),
          ("The unitary method", [(one_unitary, 14), (gb(uk.one_recipe), 6)]),
          ("Sharing in a ratio", [(one_share, 12), (gb(uk.one_frac), 8)]),
          ("Ratio problems", [(gb(uk.one_part), 10), (one_unitary, 5), (one_additive, 5)])], R)


if __name__ == "__main__":
    main()
