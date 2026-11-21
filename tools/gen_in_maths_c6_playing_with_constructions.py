# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 8: Playing with Constructions
  python3 tools/gen_in_maths_c6_playing_with_constructions.py
Circles drawn with a compass (centre, radius, diameter, points inside, on and outside a circle), rectangles and squares
and their properties (equal sides, right angles, diagonals), and constructing figures from given lengths.
Wrong answers come from real mistakes: the diameter taken as half the radius, a point at distance equal to the radius
taken as inside, and the diagonals of a rectangle taken as perpendicular.
"""
import random
from in_common import num, unit, T, QN

R = random.Random(906008)


def one_circle(r):
    kind = r.choice(["d", "r", "where", "where", "two", "compass"])
    if kind == "d":
        x = r.randint(2, 30)
        return QN("A circle has radius %d cm. What is its diameter?" % x, 2 * x, [x // 2 if x % 2 == 0 else x + 2, x * x, x + 2], "Diameter = 2 × radius = <b>%d cm</b>." % (2 * x), unit=" cm")
    if kind == "r":
        x = r.randint(2, 30)
        return QN("A circle has diameter %d cm. What is its radius?" % (2 * x), x, [4 * x, 2 * x + 2, x + 1], "Radius = diameter ÷ 2 = <b>%d cm</b>." % x, unit=" cm")
    if kind == "where":
        rad = r.randint(3, 12)
        d = rad + r.choice([-2, -1, 0, 0, 1, 3])
        ans = "Inside the circle" if d < rad else ("On the circle" if d == rad else "Outside the circle")
        return T("A circle has centre O and radius %d cm. A point P is %d cm from O. Where is P?" % (rad, d), ans,
                 [x for x in ["Inside the circle", "On the circle", "Outside the circle", "At the centre"] if x != ans],
                 "Compare %d cm with the radius %d cm: <b>%s</b>." % (d, rad, ans.lower()))
    if kind == "two":
        a, b = r.randint(2, 9), r.randint(2, 9)
        return QN("Two circles of radius %d cm and %d cm touch each other from outside. How far apart are their centres?" % (a, b), a + b, [abs(a - b) if a != b else a + b + 2, 2 * (a + b), a * b],
                  "The centres are a radius plus a radius apart: %d + %d = <b>%d cm</b>." % (a, b, a + b), unit=" cm")
    x = r.randint(3, 9)
    return QN("To draw a circle of diameter %d cm, how wide should the compass be opened?" % (2 * x), x, [2 * x, x + 1, 4 * x], "Open it to the radius: <b>%d cm</b>." % x, unit=" cm")


PROPS = [("In a rectangle, all four angles are", "right angles", ["acute angles", "obtuse angles", "equal to 60°"]),
         ("The opposite sides of a rectangle are", "equal and parallel", ["equal but not parallel", "always perpendicular", "of different lengths"]),
         ("The diagonals of a rectangle are", "equal and bisect each other", ["always perpendicular", "unequal", "equal to the sides"]),
         ("The diagonals of a square", "are equal and meet at right angles", ["are unequal", "never meet", "are equal to a side"]),
         ("A square is a rectangle with", "all sides equal", ["no right angles", "only two right angles", "unequal diagonals"]),
         ("How many lines can join two points?", "Exactly one straight line", ["Two lines", "No line", "Infinitely many straight lines"]),
         ("All points of a circle are at the same distance from", "the centre", ["the diameter", "any point inside", "the edge"]),
         ("A chord passing through the centre of a circle is called a", "diameter", ["radius", "tangent", "arc"]),
         ("Which tool is used to draw a circle?", "A compass", ["A protractor", "A set square", "A ruler only"]),
         ("Which tool is used to measure an angle?", "A protractor", ["A compass", "A divider", "A ruler"]),
         ("The longest chord of a circle is the", "diameter", ["radius", "arc", "sector"])]


def one_fact(r):
    q, a, w = r.choice(PROPS)
    return T(q if q.endswith("?") else q + " ___.", a, w, "<b>%s</b>." % a)


def one_rect(r):
    kind = r.choice(["diag", "half", "per", "side"])
    if kind == "diag":
        a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
        return QN("A rectangle ABCD has diagonal AC = %d cm. How long is the other diagonal BD?" % c, c, [c // 2 if c % 2 == 0 else c + 1, a + b, 2 * c], "The diagonals of a rectangle are equal: <b>%d cm</b>." % c, unit=" cm")
    if kind == "half":
        c = r.choice([8, 10, 12, 14, 16, 20, 24])
        return QN("The diagonals of a rectangle meet at O. If AC = %d cm, how long is OB?" % c, c // 2, [c, 2 * c, c // 2 + 2], "Diagonals are equal and bisect each other: %d ÷ 2 = <b>%d cm</b>." % (c, c // 2), unit=" cm")
    if kind == "per":
        s = r.randint(3, 15)
        return QN("A square is constructed with side %d cm. What is its perimeter?" % s, 4 * s, [s * s, 2 * s, 3 * s], "4 × %d = <b>%d cm</b>." % (s, 4 * s), unit=" cm")
    p = r.choice([20, 24, 28, 30, 36, 40])
    l = r.randint(p // 4 + 1, p // 2 - 1)
    return QN("A rectangle has perimeter %d cm and one side %d cm. What is the length of the other side?" % (p, l), p // 2 - l, [p - l, p // 2, p // 4], "%d ÷ 2 − %d = <b>%d cm</b>." % (p, l, p // 2 - l), unit=" cm")


def main():
    unit(6, 0, 8, "playing-with-constructions", 8, "G", "Playing with Constructions: Circles, Rectangles and Squares", "playing with constructions",
         "Constructions with a ruler and compass: circles (centre, radius, diameter), rectangles and squares and their properties, and the diagonals of rectangles and squares (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Playing with Constructions worksheet (Ganita Prakash Chapter 8): circles, radius and diameter, rectangles, squares and their diagonals. 100 questions with answers.",
         "Diameter = 2 × radius", "The diagonals of a rectangle are equal and bisect each other.",
         "<p>A <b>circle</b> is all the points at the same distance (the <b>radius</b>) from its <b>centre</b>. The <b>diameter</b> passes through the centre and is twice the radius. To draw a circle, open the compass to the radius.</p>"
         "<p>A <b>rectangle</b> has four right angles and opposite sides equal; its diagonals are equal and bisect each other. A <b>square</b> also has all sides equal, and its diagonals meet at right angles.</p>",
         [("A circle has diameter 14 cm. What is its radius?", ["14 ÷ 2"], "7 cm"),
          ("A point is 6 cm from the centre of a circle of radius 5 cm. Where is it?", ["6 > 5"], "Outside the circle")],
         ["Halving the radius to get the diameter.", "Thinking a point at exactly the radius is inside the circle (it is on it).", "Thinking the diagonals of every rectangle meet at right angles (only in a square)."],
         [("What is the relation between radius and diameter?", "The diameter is twice the radius."),
          ("What are the properties of a rectangle?", "Four right angles, opposite sides equal and parallel, and equal diagonals that bisect each other."),
          ("How is a square different from a rectangle?", "A square has all four sides equal, and its diagonals meet at right angles.")],
         [("Radius and diameter", [(one_circle, 20)]),
          ("Construction facts", [(one_fact, 11), (one_circle, 9)]),
          ("Rectangles and squares", [(one_rect, 20)]),
          ("Points and circles", [(one_circle, 12), (one_rect, 8)]),
          ("Mixed problems", [(one_rect, 10), (one_circle, 10)])], R)


if __name__ == "__main__":
    main()
