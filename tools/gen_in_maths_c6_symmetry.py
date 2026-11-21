# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 9: Symmetry
  python3 tools/gen_in_maths_c6_symmetry.py
Lines of symmetry of shapes, regular polygons and capital letters, rotational symmetry (order and angle of symmetry), and
shapes with both kinds of symmetry.
Wrong answers come from real mistakes: counting the diagonals of a rectangle as lines of symmetry, giving order 0 to a
shape with no rotational symmetry (it has order 1), and the angle of symmetry taken as 360° × order.
"""
import random
from in_common import unit, T, QN

R = random.Random(906009)
SHAPES = [("square", 4, 4), ("rectangle", 2, 2), ("equilateral triangle", 3, 3), ("isosceles triangle (not equilateral)", 1, 1), ("scalene triangle", 0, 1),
          ("rhombus (not a square)", 2, 2), ("parallelogram (not a rectangle or rhombus)", 0, 2), ("kite", 1, 1), ("circle", None, None),
          ("regular pentagon", 5, 5), ("regular hexagon", 6, 6), ("regular octagon", 8, 8), ("regular heptagon", 7, 7), ("regular nonagon", 9, 9), ("regular decagon", 10, 10), ("regular dodecagon (12 sides)", 12, 12), ("isosceles trapezium", 1, 1), ("semicircle", 1, 1)]
LETTERS = {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 0, "G": 0, "H": 2, "I": 2, "J": 0, "K": 1, "L": 0, "M": 1, "N": 0, "O": 2, "P": 0, "Q": 0,
           "R": 0, "S": 0, "T": 1, "U": 1, "V": 1, "W": 1, "X": 2, "Y": 1, "Z": 0}


def art(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def one_lines(r):
    name, l, _ = r.choice([s for s in SHAPES if s[1] is not None])
    return QN("How many lines of symmetry does %s have?" % art(name), l, [l * 2 if l else 2, l + 1, 4 if l != 4 else 2],
              "%s has <b>%d</b> line%s of symmetry." % (art(name).capitalize(), l, "" if l == 1 else "s"))


def one_letter(r):
    kind = r.choice(["count", "which", "which"])
    if kind == "count":
        c = r.choice(list(LETTERS))
        n = LETTERS[c]
        return QN("How many lines of symmetry does the capital letter %s have (in a plain font)?" % c, n, [n + 1, 2 if n != 2 else 0, 4], "<b>%d</b>." % n)
    want = r.choice([0, 1, 2])
    good = [c for c, v in LETTERS.items() if v == want]
    bad = [c for c, v in LETTERS.items() if v != want]
    a = r.choice(good)
    return T("Which capital letter has %s?" % ("no line of symmetry" if want == 0 else "exactly one line of symmetry" if want == 1 else "two lines of symmetry"), a, r.sample(bad, 3),
             "<b>%s</b>." % a)


def one_rot(r):
    kind = r.choice(["order", "order", "angle", "back", "fan", "fan"])
    if kind == "fan":
        k = r.randint(3, 12)
        thing = r.choice(["A ceiling fan has %d identical blades" % k, "A flower has %d identical petals" % k, "A rangoli design has %d identical parts arranged in a circle" % k, "A wheel has %d identical spokes" % k])
        if r.random() < 0.5:
            return QN("%s. What is its order of rotational symmetry?" % thing, k, [k * 2, k - 1, 1], "It fits onto itself %d times in a full turn: <b>%d</b>." % (k, k))
        if 360 % k:
            return None
        return QN("%s. What is its angle of rotational symmetry?" % thing, 360 // k, [360 // k * 2, k * 10, 180 if 360 // k != 180 else 90], "360° ÷ %d = <b>%d°</b>." % (k, 360 // k), unit="°")
    name, _, o = r.choice([s for s in SHAPES if s[2] is not None])
    if kind == "order":
        return QN("What is the order of rotational symmetry of %s?" % art(name), o, [0 if o == 1 else o * 2, o + 1, 4 if o != 4 else 2],
                  "It looks the same <b>%d</b> time%s in a full turn." % (o, "" if o == 1 else "s"))
    if kind == "angle":
        if o == 1:
            return None
        return QN("What is the angle of rotational symmetry of %s?" % art(name), 360 // o, [360 // o * 2 if 360 // o * 2 < 360 else 360 // o // 2, o * 30, 180 if 360 // o != 180 else 90],
                  "360° ÷ %d = <b>%d°</b>." % (o, 360 // o), unit="°")
    o = r.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
    return QN("A figure looks the same after every turn of %d°. What is its order of rotational symmetry?" % (360 // o), o, [360 // o // 10, o + 1, o * 2], "360° ÷ %d° = <b>%d</b>." % (360 // o, o))


def one_both(r):
    t = r.choice([("Which shape has rotational symmetry but no line of symmetry?", "A parallelogram that is not a rectangle or rhombus", ["A square", "An isosceles triangle", "A kite"]),
                  ("Which shape has exactly one line of symmetry and no rotational symmetry (order 1)?", "An isosceles triangle", ["A square", "A rectangle", "A regular hexagon"]),
                  ("Which shape has an infinite number of lines of symmetry?", "A circle", ["A square", "A regular octagon", "A semicircle"]),
                  ("A regular polygon with n sides has how many lines of symmetry?", "n", ["n − 1", "2n", "n ÷ 2"]),
                  ("Which letter looks the same after a half turn?", "S", ["E", "A", "K"]),
                  ("Which letter looks the same after a half turn?", "N", ["M", "T", "Y"]),
                  ("Which shape has both 2 lines of symmetry and rotational symmetry of order 2?", "A rectangle", ["A kite", "A square", "An equilateral triangle"]),
                  ("Which number has a line of symmetry when written in digits?", "8", ["2", "4", "7"]),
                  ("What is the smallest order of rotational symmetry any shape can have?", "1", ["0", "2", "4"])])
    return T(t[0], t[1], t[2], "<b>%s</b>." % t[1])


def main():
    unit(6, 0, 9, "symmetry", 9, "G", "Symmetry: Lines of Symmetry and Rotational Symmetry", "symmetry",
         "Line of symmetry (reflection symmetry) and rotational symmetry, order and angle of rotational symmetry of figures (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Symmetry worksheet (Ganita Prakash Chapter 9): lines of symmetry of shapes and letters, order and angle of rotational symmetry. 100 questions with answers.",
         "A regular polygon with n sides has n lines of symmetry", "Angle of rotational symmetry = 360° ÷ order.",
         "<p>A <b>line of symmetry</b> divides a figure into two mirror halves. A rectangle has 2 (not along its diagonals); a square has 4; a regular n-sided polygon has n.</p>"
         "<p>A figure has <b>rotational symmetry</b> if it looks the same after a turn of less than 360°. The <b>order</b> is how many times it fits onto itself in a full turn; the <b>angle of symmetry</b> is 360° ÷ order.</p>",
         [("What is the angle of symmetry of a regular hexagon?", ["Order 6", "360° ÷ 6"], "60°"),
          ("How many lines of symmetry does a rectangle have?", ["Through the mid-points of opposite sides"], "2")],
         ["Counting the diagonals of a rectangle as lines of symmetry.", "Saying a shape with no rotational symmetry has order 0 (it has order 1).", "Multiplying instead of dividing 360° by the order."],
         [("What is a line of symmetry?", "A line that divides a figure into two parts that are mirror images of each other."),
          ("What is the order of rotational symmetry?", "The number of times a figure looks the same during one full turn."),
          ("How many lines of symmetry does a circle have?", "Infinitely many — every diameter is a line of symmetry.")],
         [("Lines of symmetry of shapes", [(one_lines, 14), (one_both, 6)]),
          ("Symmetry of letters", [(one_letter, 20)]),
          ("Order of rotational symmetry", [(one_rot, 20)]),
          ("Angle of symmetry", [(one_rot, 18), (one_both, 2)]),
          ("Both kinds of symmetry", [(one_letter, 8), (one_rot, 10), (one_lines, 2)])], R)


if __name__ == "__main__":
    main()
