# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 1: A Square and a Cube
  python3 tools/gen_in_maths_c8_a_square_and_a_cube.py
Perfect squares and their units digits, sums of odd numbers, numbers between consecutive squares, square roots (also by
prime factorisation and estimation), cubes and cube roots, the smallest multiplier that makes a perfect square or cube.
Wrong answers come from real mistakes: 2n instead of n², halving instead of taking the root, n³ read as 3n, and
multiplying by the whole unpaired factor list instead of the missing factors.
"""
import random
from in_common import num, unit, T, QN, adopt, gb
import gen_au_maths_y7_square_numbers_and_square_roots as au
import gen_uk_maths_y7_powers_and_roots as uk

R = random.Random(908001)
adopt(au, R)
adopt(uk, R)
SUP = lambda n, k: "%d<sup>%d</sup>" % (n, k)


def one_units(r):
    kind = r.choice(["digit", "digit", "cannot", "odd"])
    if kind == "digit":
        n = r.randint(11, 99)
        d = n * n % 10
        return QN("What is the units digit of %s?" % SUP(n, 2), d, [n % 10, n % 10 * 2 % 10, (d + 5) % 10],
                  "Only the units digit matters: %d × %d ends in <b>%d</b>." % (n % 10, n % 10, d))
    if kind == "cannot":
        good = [x * x for x in range(31, 99)]
        bad = r.choice([n for n in range(1000, 9999) if n % 10 in (2, 3, 7, 8)])
        w = r.sample(good, 3)
        return T("Three of these are perfect squares. Which one can <b>not</b> be a perfect square?", num(bad), [num(x) for x in w],
                 "A perfect square never ends in 2, 3, 7 or 8, so <b>%s</b> is not a square." % num(bad))
    n = r.randint(5, 30)
    return QN("What is the sum of the first %d odd numbers (1 + 3 + 5 + …)?" % n, n * n, [2 * n, 2 * n - 1, n * (n + 1)],
              "The sum of the first n odd numbers is n², so it is %d² = <b>%d</b>." % (n, n * n))


def one_between(r):
    n = r.randint(6, 60)
    return QN("How many whole numbers lie between %s and %s?" % (SUP(n, 2), SUP(n + 1, 2)), 2 * n, [2 * n + 1, n, 2 * n - 1],
              "Between n² and (n + 1)² there are 2n numbers: 2 × %d = <b>%d</b>." % (n, 2 * n))


def one_cube(r):
    kind = r.choice(["cube", "cube", "root", "root", "neg"])
    n = r.randint(2, 15)
    if kind == "cube":
        return QN("Work out %s." % SUP(n, 3), n ** 3, [3 * n, n * n, n ** 3 + n],
                  "%d × %d × %d = <b>%s</b>." % (n, n, n, num(n ** 3)))
    if kind == "root":
        n = r.randint(4, 25)
        return QN("Find the cube root: ∛%s" % num(n ** 3), n, [n ** 3 // 3, n * n, n + 1],
                  "%d × %d × %d = %s, so ∛%s = <b>%d</b>." % (n, n, n, num(n ** 3), num(n ** 3), n))
    n = r.randint(2, 12)
    return QN("Find ∛(−%s)." % num(n ** 3), -n, [n, -3 * n, -n * n],
              "(−%d)³ = −%s, so the cube root is <b>−%d</b>." % (n, num(n ** 3), n))


def pf(n):
    out, p = {}, 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out


def one_mult(r):
    k = r.choice([2, 2, 3])
    base = r.choice([2, 3, 5, 6, 7, 10, 12])
    extra = r.choice([2, 3, 5, 6, 7, 10, 11])
    n = base ** k * extra
    f = pf(n)
    need = 1
    for p, e in f.items():
        need *= p ** ((-e) % k)
    if need == 1:
        return None
    word = "square" if k == 2 else "cube"
    fs = " × ".join(" × ".join([str(p)] * e) for p, e in sorted(f.items()))
    if r.random() < 0.5:
        return QN("What is the smallest number by which %s must be multiplied to get a perfect %s?" % (num(n), word), need,
                  [extra if extra != need else need * 2, n, need * need],
                  "%s = %s. Group the factors in %ss; the missing factors multiply to <b>%d</b>." % (num(n), fs, "pair" if k == 2 else "triple", need))
    div = 1
    for p, e in f.items():
        div *= p ** (e % k)
    if div == 1:
        return None
    return QN("What is the smallest number by which %s must be divided to get a perfect %s?" % (num(n), word), div,
              [need if need != div else div * 2, n // div, div * div],
              "%s = %s. Divide out the factors left over after making %ss: <b>%d</b>." % (num(n), fs, "pair" if k == 2 else "triple", div))


def one_pfroot(r):
    k = r.choice([2, 3])
    m = r.choice([6, 10, 12, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 42])
    n = m ** k
    f = pf(n)
    fs = " × ".join(" × ".join([str(p)] * e) for p, e in sorted(f.items()))
    sym = "√" if k == 2 else "∛"
    return QN("Using prime factorisation, find %s%s." % (sym, num(n)), m, [n // k if n % k == 0 else m * k, m * 2, m + 2],
              "%s = %s. Take one factor from each %s: <b>%d</b>." % (num(n), fs, "pair" if k == 2 else "group of three", m))


def one_word(r):
    kind = r.choice(["garden", "rows", "cubebox", "tiles"])
    if kind == "garden":
        s = r.randint(12, 45)
        return QN("A square garden has an area of %s m². How long is each side?" % num(s * s), s, [s * s // 4, 2 * s, s + 1],
                  "Side = √%s = <b>%d m</b>." % (num(s * s), s), unit=" m")
    if kind == "rows":
        s = r.randint(15, 40)
        n = s * s + r.randint(1, 2 * s)
        return QN("%s students stand in rows to make the largest possible square. How many are left out?" % num(n), n - s * s,
                  [n - (s - 1) ** 2, (s + 1) ** 2 - n, s], "%d² = %s ≤ %s < %d². Left out: %s − %s = <b>%d</b>." % (s, num(s * s), num(n), s + 1, num(n), num(s * s), n - s * s))
    if kind == "cubebox":
        s = r.randint(3, 12)
        return QN("A cube-shaped box holds exactly %s unit cubes. How many unit cubes fit along one edge?" % num(s ** 3), s, [s ** 3 // 3, s * s, s + 1],
                  "Edge = ∛%s = <b>%d</b>." % (num(s ** 3), s))
    s = r.randint(8, 30)
    t = r.choice([20, 25, 30, 50])
    return QN("A square floor of side %d m is covered with square tiles of side %d cm. How many tiles are needed?" % (s, t),
              (s * 100 // t) ** 2 if (s * 100) % t == 0 else None, [s * 100 // t * 4 if (s * 100) % t == 0 else None, s * s * t, (s * 100 // t) ** 2 // 2 if (s * 100) % t == 0 else None],
              "Tiles along a side: %d ÷ %d = %d. Number of tiles = %d² = <b>%s</b>." % (s * 100, t, s * 100 // t, s * 100 // t, num((s * 100 // t) ** 2)))


def main():
    unit(8, 1, 1, "a-square-and-a-cube", 1, "N", "A Square and a Cube: Squares, Cubes and Their Roots", "squares and cubes",
         "Perfect squares and their properties, square roots, perfect cubes and cube roots, and estimating roots (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 A Square and a Cube worksheet (Ganita Prakash Part 1, Chapter 1): perfect squares, square roots, cubes, cube roots and prime factorisation. 100 questions with answers.",
         "A square is n × n; a cube is n × n × n", "Square roots and cube roots undo them.",
         "<p>A <b>perfect square</b> is a number like 49 = 7². A perfect square never ends in 2, 3, 7 or 8, and the sum of the first n odd numbers is n².</p>"
         "<p>A <b>perfect cube</b> is a number like 125 = 5³. To find a root by prime factorisation, group the prime factors in pairs (square root) or triples (cube root) and take one from each group.</p>",
         [("Find √1,764 by prime factorisation.", ["1,764 = 2 × 2 × 3 × 3 × 7 × 7", "Take one from each pair: 2 × 3 × 7"], "42"),
          ("What is the smallest number to multiply 72 by to make a perfect square?", ["72 = 2 × 2 × 2 × 3 × 3", "One 2 has no partner"], "2")],
         ["Working out 7² as 7 × 2 = 14.", "Halving a number instead of taking its square root (√64 is 8, not 32).", "Writing 4³ as 12 instead of 4 × 4 × 4 = 64."],
         [("What is a perfect square?", "A number that is a whole number multiplied by itself, such as 1, 4, 9, 16 and 25."),
          ("Which digits can a perfect square end in?", "0, 1, 4, 5, 6 or 9. A number ending in 2, 3, 7 or 8 is never a perfect square."),
          ("How do you find a cube root by prime factorisation?", "Write the number as a product of primes, group equal primes in threes and multiply one prime from each group.")],
         [("Squares and square roots", [(gb(au.one_square), 10), (gb(au.one_root), 10)]),
          ("Properties of square numbers", [(one_units, 12), (one_between, 4), (gb(au.one_est), 4)]),
          ("Cubes, cube roots and powers", [(one_cube, 16), (gb(uk.one_mix), 4)]),
          ("Roots by prime factorisation", [(one_pfroot, 10), (one_mult, 10)]),
          ("Problems with squares and cubes", [(one_word, 12), (gb(au.one_calc), 8)])], R)


if __name__ == "__main__":
    main()
