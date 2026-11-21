# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 3: Finding Common Ground
  python3 tools/gen_in_maths_c7_finding_common_ground.py
Common factors and the highest common factor (HCF), common multiples and the lowest common multiple (LCM), finding them by
listing and by prime factorisation, HCF × LCM = product of two numbers, and problems (equal groups, tiles, bells, buses).
Wrong answers come from real mistakes: the product taken as the LCM, the smaller number taken as the HCF, and HCF and
LCM swapped in a problem.
"""
import random
from math import gcd
from in_common import unit, QN, adopt, gb
import gen_uk_maths_y7_factors_multiples_and_primes as fm
import gen_in_maths_c6_prime_time as c6

R = random.Random(907011)
adopt(fm, R)


def one_rel(r):
    a, b = r.choice([(12, 18), (8, 20), (15, 25), (14, 21), (16, 24), (18, 30), (20, 30), (24, 36), (9, 15), (10, 25), (27, 36), (35, 42)])
    g, l = gcd(a, b), a * b // gcd(a, b)
    kind = r.choice(["lcm", "hcf"])
    if kind == "lcm":
        return QN("The HCF of %d and %d is %d. Use HCF × LCM = product to find their LCM." % (a, b, g), l, [a * b, a * b // 2 if a * b // 2 != l else l * 2, l + g],
                  "LCM = %d × %d ÷ %d = <b>%d</b>." % (a, b, g, l))
    return QN("The LCM of %d and %d is %d. Find their HCF." % (a, b, l), g, [l // a if l // a != g else g * 2, a * b // l * 2 if a * b // l * 2 != g else g + 1, min(a, b)],
              "HCF = %d × %d ÷ %d = <b>%d</b>." % (a, b, l, g))


def one_word(r):
    kind = r.choice(["tile", "rope", "bus", "pack"])
    if kind == "tile":
        a, b = r.choice([(240, 180), (360, 300), (420, 280), (160, 120), (450, 300), (180, 135)])
        g = gcd(a, b)
        return QN("A floor is %d cm by %d cm. What is the largest square tile that fits exactly, with no cutting? (side in cm)" % (a, b), g, [a * b // g, b // 2, g // 2], "HCF of %d and %d = <b>%d cm</b>." % (a, b, g), unit=" cm")
    if kind == "rope":
        a, b, c = r.choice([(24, 36, 48), (30, 45, 60), (18, 27, 45), (40, 60, 100), (12, 18, 30)])
        g = gcd(gcd(a, b), c)
        return QN("Three ropes are %d m, %d m and %d m long. They are cut into equal pieces as long as possible. How long is each piece?" % (a, b, c), g, [a, g // 2 if g % 2 == 0 else g + 1, a + b + c],
                  "HCF of %d, %d and %d = <b>%d m</b>." % (a, b, c, g), unit=" m")
    if kind == "bus":
        a, b = r.choice([(12, 15), (10, 18), (8, 12), (15, 20), (20, 25), (9, 12)])
        l = a * b // gcd(a, b)
        return QN("Buses on two routes leave together at 8 a.m., one every %d minutes and the other every %d minutes. After how many minutes do they next leave together?" % (a, b), l,
                  [a * b if a * b != l else l + a, gcd(a, b), a + b], "LCM of %d and %d = <b>%d minutes</b>." % (a, b, l), unit=" minutes")
    a, b = r.choice([(6, 8), (12, 18), (10, 15), (8, 12), (9, 15), (20, 30)])
    l = a * b // gcd(a, b)
    return QN("Pencils come in packs of %d and erasers in packs of %d. What is the smallest number of each you can buy to have the same number of both?" % (a, b), l,
              [a * b if a * b != l else l * 2, gcd(a, b), a + b], "LCM of %d and %d = <b>%d</b>." % (a, b, l))


def main():
    unit(7, 2, 3, "finding-common-ground", 11, "N", "Finding Common Ground: HCF and LCM", "finding common ground",
         "Common factors and common multiples, highest common factor (HCF) and lowest common multiple (LCM) by listing and by prime factorisation, and their use in problems (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Finding Common Ground worksheet (Ganita Prakash Part 2, Chapter 3): HCF, LCM, prime factorisation, HCF × LCM and word problems. 100 questions with answers.",
         "HCF × LCM = the product of the two numbers", "HCF: the largest number dividing both. LCM: the smallest number both divide.",
         "<p>The <b>HCF</b> (highest common factor) is the largest number that divides all the given numbers. The <b>LCM</b> (lowest common multiple) is the smallest number that is a multiple of all of them.</p>"
         "<p>With prime factors: 24 = 2³ × 3 and 36 = 2² × 3². HCF takes the lower powers: 2² × 3 = 12. LCM takes the higher powers: 2³ × 3² = 72.</p>"
         "<p>For two numbers, HCF × LCM = product: 12 × 72 = 24 × 36.</p>",
         [("Find the HCF and LCM of 18 and 24.", ["18 = 2 × 3²", "24 = 2³ × 3"], "HCF 6, LCM 72"),
          ("Two bells ring every 6 and 8 minutes. When do they ring together again?", ["LCM of 6 and 8"], "After 24 minutes")],
         ["Taking the product of the two numbers as the LCM.", "Taking the smaller number as the HCF.", "Using HCF where the problem needs LCM (things happening together again)."],
         [("What is the difference between HCF and LCM?", "The HCF is the largest common factor; the LCM is the smallest common multiple."),
          ("When do we use the LCM in a problem?", "When things repeat and we want them to happen together again, such as bells or buses."),
          ("When do we use the HCF in a problem?", "When we cut or share into the largest equal groups or pieces.")],
         [("Highest common factor", [(gb(fm.one_hcf), 20)]),
          ("Lowest common multiple", [(gb(fm.one_lcm), 20)]),
          ("Using prime factors", [(gb(fm.one_pf), 10), (gb(fm.one_pf_use), 10)]),
          ("HCF × LCM", [(one_rel, 14), (c6.one_common, 6)]),
          ("Problems", [(one_word, 14), (c6.one_prob, 6)])], R)


if __name__ == "__main__":
    main()
