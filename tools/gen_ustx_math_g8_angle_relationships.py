# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Parallel Lines, Transversals and Triangle Angles (TEKS 8.8D)
  python3 tools/gen_ustx_math_g8_angle_relationships.py
Naming angle pairs, finding angles when parallel lines are cut by a transversal, triangle angle sums and exterior
angles, angle equations, and reasoning (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: thinking alternate interior angles are supplementary, adding the exterior
angle to 180°, and mixing up corresponding and vertical angles.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_angle_relationships_parallel_lines as apl
adopt(apl)
apl.R = random.Random(680130)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Name the angle pair", [("run", apl.set_names, (), 20)]),
        ("Find the angle", [("run", apl.set_find, (), 20)]),
        ("Triangle angles and exterior angles", [("run", apl.set_tri, (), 20)]),
        ("Angle equations", [("run", apl.set_eq, (), 20)]),
        ("Reasoning with angles", [("run", apl.set_reason, (), 20)]),
    ], 68013)
    finish(sets, R)
    body = lesson('<ul><li>When parallel lines are cut by a transversal, <b>corresponding</b>, <b>alternate interior</b> and <b>alternate exterior</b> angles are equal.</li><li><b>Same-side interior</b> angles add to 180°.</li><li>The angles of a triangle add to 180°. An <b>exterior angle</b> equals the sum of the two remote interior angles.</li><li>Two triangles with two pairs of equal angles are similar (angle-angle).</li></ul>',
        [example("∠2 = 65°, ∠2 and ∠6 are corresponding", ["Corresponding angles are equal"], "∠6 = 65°"), example("Exterior angle with remote angles 40° and 75°", ["40 + 75"], "115°")],
        [['Thinking alternate interior angles add to 180°', 'They are equal when the lines are parallel.'], ['Adding the exterior angle to 180°', 'The exterior angle = sum of the two remote interior angles.'], ['Mixing up corresponding and vertical angles', 'Corresponding angles are in matching corners at each intersection.']])
    faq = [('What does TEKS 8.8D ask?', 'Use informal arguments to establish facts about the angle sum and exterior angle of triangles, the angles created when parallel lines are cut by a transversal and the angle-angle criterion for similarity of triangles.'), ('What is a transversal?', 'A line that crosses two or more other lines.'), ('Why are corresponding angles equal?', 'A translation along the transversal maps one onto the other.'), ('What is the angle-angle criterion?', 'If two angles of one triangle equal two angles of another, the triangles are similar.')]
    make('angle-relationships-and-parallel-lines', 13, 'Expressions, Equations and Relationships', '8.8D',
         '8.8D use informal arguments to establish facts about the angle sum and exterior angle of triangles, the angles created when parallel lines are cut by a transversal, and the angle-angle criterion for similarity of triangles',
         'Parallel Lines, Transversals and Triangle Angles', 'Angle Relationships',
         'Free Grade 8 worksheets for Texas TEKS 8.8D: parallel lines and transversals, angle pairs, triangle angle sums, exterior angles and angle equations. 100 questions with answers.',
         'Corresponding and alternate angles are equal; same-side interior angles add to 180°.', 'An exterior angle equals the sum of the two remote interior angles.',
         body, faq, sets, seo_title='Grade 8 Parallel Lines and Transversals Worksheets (TEKS 8.8D, STAAR)')


if __name__ == "__main__":
    build()
