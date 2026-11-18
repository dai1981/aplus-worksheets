# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Writing and Solving Equations with Angles (TEKS 7.11C)
  python3 tools/gen_ustx_math_g7_angle_equations.py
Complementary and supplementary angles, angles on a line and around a point, vertical angles, the angle sum of a
triangle with x, and word problems (US Grade 7 makers with a new seed, plus own triangle equations).
Wrong answers come from real mistakes: using 180° for complementary angles, setting vertical angles to add to 180°,
and forgetting to find the angle after finding x.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_angle_relationships as ar
adopt(ar)
ar.R = random.Random(670190)
tx_common.GRADE = "grade-7"

def one_tri(r):
    kind = r.choice(["mult", "plus", "three"])
    if kind == "mult":
        a = r.choice([2, 3, 4])
        c = r.randint(20, 80)
        if (180 - c) % (a + 1):
            return None
        x = (180 - c) // (a + 1)
        eq = "x + %dx + %d = 180" % (a, c)
        q = "A triangle has angles x°, %dx° and %d°. What is the value of x?" % (a, c)
        return mcq(q, str(x), [str((180 - c) // a) if (180 - c) % a == 0 else str(x + 5), str(180 - c), str((360 - c) // (a + 1)) if (360 - c) % (a + 1) == 0 else str(x * 2)],
                   "%s, so %dx = %d and x = <b>%d</b>." % (eq, a + 1, 180 - c, x))
    if kind == "plus":
        b, c = r.randint(5, 30), r.randint(25, 70)
        if (180 - b - c) % 2:
            return None
        x = (180 - b - c) // 2
        if x <= 10:
            return None
        return mcq("A triangle has angles x°, (x + %d)° and %d°. What is the measure of the largest angle?" % (b, c), "%d°" % max(x + b, c), ["%d°" % x, "%d°" % min(x + b, c), "%d°" % (180 - c)] if max(x + b, c) != 180 - c else ["%d°" % x, "%d°" % min(x + b, c), "%d°" % (x + b + 10)],
                   "x + x + %d + %d = 180, so 2x = %d and x = %d. The angles are %d°, %d° and %d°. The largest is <b>%d°</b>." % (b, c, 180 - b - c, x, x, x + b, c, max(x + b, c)))
    x = r.randint(10, 40)
    a, b = r.choice([(2, 3), (1, 4), (3, 4), (2, 5)])
    if a * x + b * x >= 170:
        return None
    c = 180 - a * x - b * x
    return mcq("The angles of a triangle are %dx°, %dx° and %d°. What is x?" % (a, b, c), str(x), [str((180 - c) // a) if (180 - c) % a == 0 else str(x + 3), str(c // (a + b)) if c % (a + b) == 0 else str(x - 2), str((360 - c) // (a + b)) if (360 - c) % (a + b) == 0 else str(x * 2)],
               "%dx + %dx + %d = 180, so %dx = %d and x = <b>%d</b>." % (a, b, c, a + b, 180 - c, x))


def build():
    sets, R = build_sets([
        ("Complementary and supplementary angles", [("run", ar.set_words, (), 20)]),
        ("Write and solve equations", [("run", ar.set_equations, (), 20)]),
        ("Straight lines and angles around a point", [("run", ar.set_lines, (), 10), ("run", ar.set_vertical, (), 10)]),
        ("The angle sum of a triangle", [("collect", one_tri, 20)]),
        ("Word problems", [("run", ar.set_problems, (), 20)]),
    ], 67019)
    finish(sets, R)
    body = lesson('<ul><li><b>Complementary</b> angles add to 90°. <b>Supplementary</b> angles add to 180°.</li><li>Angles on a straight line add to 180°; angles around a point add to 360°.</li><li><b>Vertical angles</b> are equal.</li><li>The angles of a triangle add to 180°. Write an equation such as x + 2x + 30 = 180, then solve.</li></ul>',
        [example("Angles x°, 2x° and 30° in a triangle", ["x + 2x + 30 = 180", "3x = 150"], "x = 50"), example("x° and 50° are complementary", ["x + 50 = 90"], "x = 40")],
        [['Using 180° for complementary angles', 'Complementary angles add to 90°.'], ['Adding vertical angles to 180°', 'Vertical angles are equal.'], ['Stopping at x when the angle is asked', 'Substitute x to find the angle.']])
    faq = [('What does TEKS 7.11C ask?', 'Write and solve equations using geometry concepts, including the sum of the angles in a triangle, and angle relationships.'), ('What are adjacent angles?', 'Angles that share a side and a vertex but do not overlap.'), ('Can two obtuse angles be supplementary?', 'No. Two angles over 90° add to more than 180°.'), ('How do I check my answer?', 'Substitute x and add the angles.')]
    make('equations-with-angles-and-triangles', 19, 'Expressions, Equations and Relationships', '7.11C',
         '7.11C write and solve equations using geometry concepts, including the sum of the angles in a triangle, and angle relationships',
         'Writing and Solving Equations with Angles', 'Equations with Angles',
         'Free Grade 7 worksheets for Texas TEKS 7.11C: complementary, supplementary and vertical angles, angles on a line, triangle angle sum equations and word problems. 100 questions with answers.',
         'Complementary 90°, supplementary 180°, triangle 180°.', 'x + 2x + 30 = 180 → x = 50. Vertical angles are equal.',
         body, faq, sets, seo_title='Grade 7 Angle Equations Worksheets: Triangles and Angle Relationships (TEKS 7.11C, STAAR)')


if __name__ == "__main__":
    build()
