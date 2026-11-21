# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 2: The Baudhayana–Pythagoras Theorem
  python3 tools/gen_in_maths_c8_the_baudhayana_pythagoras_theorem.py
The theorem (stated by Baudhayana in the Shulba Sutras): finding the hypotenuse and a shorter side, testing for a right
angle, Pythagorean (Baudhayana) triples, and problems with ladders, diagonals and distances.
Wrong answers come from real mistakes: adding the sides without squaring, adding instead of subtracting for a shorter
side, forgetting the square root, and testing the converse with the wrong side as the longest.
"""
import random
from in_common import num, unit, T, QN, adopt, gb
import gen_uk_maths_y9_pythagoras_theorem as py

R = random.Random(908009)
adopt(py, R)
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37), (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25), (10, 24, 26)]


def one_triple(r):
    kind = r.choice(["which", "which", "missing", "gen"])
    a, b, c = r.choice(TRIPLES)
    if kind == "which":
        bad = [(a, b, c + 1), (a + 1, b, c), (a, b + 1, c + 1)]
        return T("Which set of numbers is a Baudhayana–Pythagoras triple?", "%d, %d, %d" % (a, b, c), ["%d, %d, %d" % t for t in bad],
                 "%d² + %d² = %d + %d = %d = %d². <b>%d, %d, %d</b>." % (a, b, a * a, b * b, c * c, c, a, b, c))
    if kind == "missing":
        k = r.choice([2, 3, 4, 10])
        return QN("%d, %d and x form a triple with x the largest. Find x." % (a * k, b * k), c * k, [a * k + b * k, c, c * k + 1],
                  "x = √(%d² + %d²) = <b>%d</b>." % (a * k, b * k, c * k))
    m = r.randint(2, 9)
    return T("Using 2m, m² − 1 and m² + 1, which triple does m = %d give?" % m, "%d, %d, %d" % (2 * m, m * m - 1, m * m + 1),
             ["%d, %d, %d" % (2 * m, m * m, m * m + 1), "%d, %d, %d" % (m, m * m - 1, m * m + 1), "%d, %d, %d" % (2 * m, m * m - 1, m * m + 2)],
             "2m = %d, m² − 1 = %d, m² + 1 = %d: <b>%d, %d, %d</b>." % (2 * m, m * m - 1, m * m + 1, 2 * m, m * m - 1, m * m + 1))


def one_word(r):
    a, b, c = r.choice(TRIPLES)
    k = r.choice([1, 1, 2])
    a, b, c = a * k, b * k, c * k
    kind = r.choice(["ladder", "rect", "walk", "pole"])
    if kind == "ladder":
        return QN("A %d m ladder leans against a wall. Its foot is %d m from the wall. How high up the wall does it reach?" % (c, a), b, [c - a, c + a, b + 1],
                  "√(%d² − %d²) = √%d = <b>%d m</b>." % (c, a, c * c - a * a, b), unit=" m")
    if kind == "rect":
        return QN("A rectangular field is %d m by %d m. How long is its diagonal?" % (a, b), c, [a + b, c * c, c + 1],
                  "√(%d² + %d²) = √%d = <b>%d m</b>." % (a, b, c * c, c), unit=" m")
    if kind == "walk":
        return QN("Anil walks %d km east and then %d km north. How far is he from his starting point?" % (a, b), c, [a + b, abs(b - a), c + 1],
                  "√(%d² + %d²) = <b>%d km</b>." % (a, b, c), unit=" km")
    return QN("A %d m rope is tied to the top of a %d m pole and pegged to the ground. How far from the foot of the pole is the peg?" % (c, b), a, [c - b, c + b, a + 1],
              "√(%d² − %d²) = <b>%d m</b>." % (c, b, a), unit=" m")


def main():
    unit(8, 2, 2, "the-baudhayana-pythagoras-theorem", 9, "G", "The Baudhayana–Pythagoras Theorem: Right-Angled Triangles", "baudhayana–pythagoras theorem",
         "The Baudhayana–Pythagoras theorem for right-angled triangles, its converse, Baudhayana–Pythagoras triples and applications (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Baudhayana–Pythagoras Theorem worksheet (Ganita Prakash Part 2, Chapter 2): hypotenuse, shorter sides, right-angle test, triples and word problems. 100 questions with answers.",
         "a² + b² = c²", "c is the hypotenuse, the side opposite the right angle.",
         "<p>In a right-angled triangle, the square on the <b>hypotenuse</b> equals the sum of the squares on the other two sides: a² + b² = c². Baudhayana stated this in the Shulba Sutras.</p>"
         "<p>To find a shorter side, subtract: a² = c² − b². If a² + b² = c² for the sides of a triangle, it has a right angle (the converse).</p>"
         "<p>Whole numbers that fit, like 3, 4, 5 or 5, 12, 13, are <b>Baudhayana–Pythagoras triples</b>.</p>",
         [("The legs are 9 cm and 12 cm. Find the hypotenuse.", ["81 + 144 = 225", "√225"], "15 cm"),
          ("The hypotenuse is 25 cm and one leg is 7 cm. Find the other leg.", ["625 − 49 = 576", "√576"], "24 cm")],
         ["Adding the sides: 3 + 4 = 7 instead of √(9 + 16) = 5.", "Adding the squares when finding a shorter side (subtract instead).", "Forgetting to take the square root at the end."],
         [("What is the Baudhayana–Pythagoras theorem?", "In a right-angled triangle, the square of the hypotenuse equals the sum of the squares of the other two sides."),
          ("Why is it named after Baudhayana?", "Baudhayana's Shulba Sutra (about 800 BCE) states the result for the diagonal of a rectangle."),
          ("What is a Baudhayana–Pythagoras triple?", "Three whole numbers a, b, c with a² + b² = c², such as 3, 4, 5.")],
         [("Finding the hypotenuse", [(gb(py.one_hyp), 20)]),
          ("Finding a shorter side", [(gb(py.one_short), 20)]),
          ("Is it a right angle?", [(gb(py.one_test), 20)]),
          ("Baudhayana–Pythagoras triples", [(one_triple, 20)]),
          ("Problems", [(one_word, 20)])], R)


if __name__ == "__main__":
    main()
