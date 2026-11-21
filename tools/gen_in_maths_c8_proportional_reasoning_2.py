# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 3: Proportional Reasoning–2
  python3 tools/gen_in_maths_c8_proportional_reasoning_2.py
Direct and inverse proportion, recognising which kind a situation is, the constant of proportionality, sharing in a
ratio of three parts, and ratio problems with a difference or a total.
Wrong answers come from real mistakes: treating an inverse situation as direct (more workers, more days), adding instead
of multiplying, and dividing by one part instead of the total number of parts.
"""
import random
from in_common import unit, T, QN, adopt, gb, inr
import gen_uk_maths_y8_direct_and_inverse_proportion as di
import gen_uk_maths_y9_ratio_problems_and_best_buys as rp

R = random.Random(908010)
adopt(di, R)
adopt(rp, R)


def noeuro(fn):
    g = gb(fn)

    def f(r):
        it = g(r)
        if it and "euro" in it["q"]:
            return None
        return it
    f.__name__ = fn.__name__
    return f


def one_direct(r):
    n, m = r.sample(range(2, 13), 2)
    kind = r.choice(["cost", "fuel", "cloth"])
    if kind == "cost":
        p = r.choice([15, 20, 25, 30, 40, 45, 60, 80])
        return T("%d kg of apples cost %s. How much do %d kg cost?" % (n, inr(n * p), m), inr(m * p), [inr(n * p + m - n), inr(n * p * m), inr(m * p + p)],
                 "Cost is directly proportional: %s per kg × %d = <b>%s</b>." % (inr(p), m, inr(m * p)))
    if kind == "fuel":
        k = r.choice([12, 15, 18, 20])
        return QN("A scooter goes %d km on %d litres of petrol. How far does it go on %d litres?" % (k * n, n, m), k * m, [k * n + m, k * n * m, k * m + k],
                  "%d km per litre × %d = <b>%d km</b>." % (k, m, k * m), unit=" km")
    p = r.choice([80, 120, 150, 200, 250])
    return T("%d m of cloth cost %s. What is the cost of %d m?" % (n, inr(n * p), m), inr(m * p), [inr(n * p + m), inr(n * p // m) if n * p % m == 0 else inr(m * p + p), inr(m * p - p)],
             "%s per metre × %d = <b>%s</b>." % (inr(p), m, inr(m * p)))


def one_inv(r):
    kind = r.choice(["workers", "speed", "pipes"])
    a = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    b = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    k = a * b * r.choice([1, 2, 3])
    if k % a or k % b or a == b:
        return None
    if kind == "workers":
        return QN("%d workers build a wall in %d days. How many days would %d workers take at the same rate?" % (a, k // a, b), k // b, [k // a * b // a if (k // a * b) % a == 0 else k // a + b, k // a + a - b, k // b + 1],
                  "Worker-days = %d × %d = %d. Days = %d ÷ %d = <b>%d</b>." % (a, k // a, k, k, b, k // b), unit=" days")
    if kind == "speed":
        v1, v2 = 10 * a, 10 * b
        t1 = r.choice([2, 3, 4, 6])
        d = v1 * t1
        if d % v2:
            return None
        return QN("A bus takes %d hours at %d km/h. How long does it take at %d km/h for the same journey?" % (t1, v1, v2), d // v2, [t1 * v2 // v1 if (t1 * v2) % v1 == 0 else t1 + 1, t1 + (v1 - v2) // 10, d // v2 + 1],
                  "Distance = %d km. Time = %d ÷ %d = <b>%d hours</b>." % (d, d, v2, d // v2), unit=" hours")
    return QN("%d identical pipes fill a tank in %d hours. How long would %d such pipes take?" % (a, k // a, b), k // b, [k // a + b - a, k // a * b // a if (k // a * b) % a == 0 else k // a + 2, k // b + 1],
              "%d × %d = %d pipe-hours. %d ÷ %d = <b>%d hours</b>." % (a, k // a, k, k, b, k // b), unit=" hours")


def main():
    unit(8, 2, 3, "proportional-reasoning-2", 10, "N", "Proportional Reasoning–2: Direct and Inverse Proportion", "proportional reasoning 2",
         "Direct and inverse proportion, identifying proportional relationships and dividing in a given ratio (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Proportional Reasoning–2 worksheet (Ganita Prakash Part 2, Chapter 3): direct proportion, inverse proportion, sharing in a ratio and ratio problems. 100 questions with answers.",
         "Direct: y ÷ x stays the same. Inverse: x × y stays the same", "More workers → fewer days: that is inverse proportion.",
         "<p>In <b>direct proportion</b>, both quantities grow together and y ÷ x is constant (cost and number of items).</p>"
         "<p>In <b>inverse proportion</b>, one grows as the other shrinks and x × y is constant (workers and days, speed and time).</p>"
         "<p>To share in a ratio a : b : c, divide the total into a + b + c equal parts.</p>",
         [("6 workers take 10 days. How long do 4 workers take?", ["6 × 10 = 60 worker-days", "60 ÷ 4"], "15 days"),
          ("Share ₹900 in the ratio 2 : 3 : 4.", ["9 parts: 1 part = ₹100"], "₹200, ₹300, ₹400")],
         ["Treating an inverse situation as direct (more workers taking more days).", "Adding the same amount instead of multiplying.", "Dividing by one part instead of the total number of parts."],
         [("What is direct proportion?", "Two quantities are in direct proportion when their ratio y ÷ x stays the same, so doubling one doubles the other."),
          ("What is inverse proportion?", "Two quantities are in inverse proportion when their product x × y stays the same, so doubling one halves the other."),
          ("How do you tell them apart?", "Ask: if one quantity doubles, does the other double (direct) or halve (inverse)?")],
         [("Direct proportion", [(one_direct, 20)]),
          ("Inverse proportion", [(one_inv, 12), (gb(di.one_inverse), 8)]),
          ("Direct or inverse?", [(noeuro(di.one_which), 12), (gb(di.one_formula), 8)]),
          ("Sharing in a ratio", [(gb(rp.one_share3), 20)]),
          ("Ratio problems", [(gb(rp.one_diff), 10), (one_inv, 5), (one_direct, 5)])], R)


if __name__ == "__main__":
    main()
