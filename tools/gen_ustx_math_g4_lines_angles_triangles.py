# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Lines, Angles and Classifying Figures (TEKS 4.6A, 4.6C, 4.6D)
  python3 tools/gen_ustx_math_g4_lines_angles_triangles.py
Points, lines, line segments and rays; parallel, perpendicular and intersecting lines; acute, right, obtuse and
straight angles; acute, right and obtuse triangles; classifying shapes by parallel sides and angles. The question
makers come from the US Grade 4 lines and angles unit with Texas names. Wrong answers come from real mistakes:
mixing up a ray and a line segment, calling any crossing lines perpendicular, and naming a triangle by its longest side.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, build_sets, example, figure)
import gen_us_math_g4_lines_angles as usl
adopt(usl)
tx_common.GRADE = "grade-4"


def build():
    sets, R = build_sets([
        ("Points, lines, line segments and rays", [("run", usl.set_figures, ("rnd",), 20)]),
        ("Parallel, perpendicular and intersecting lines", [("run", usl.set_parallel, ("rnd",), 20)]),
        ("Acute, right, obtuse and straight angles", [("run", usl.set_angles, ("rnd",), 20)]),
        ("Acute, right and obtuse triangles", [("run", usl.set_triangles, ("rnd",), 20)]),
        ("Classify figures by sides and angles", [("run", usl.set_classify, ("rnd", usl.People), 20)]),
    ], 64018)
    finish(sets, R)
    body = lesson('<ul><li>A <b>line</b> goes on forever both ways; a <b>ray</b> has one endpoint; a <b>line segment</b> has two endpoints.</li><li><b>Parallel</b> lines never meet. <b>Perpendicular</b> lines meet at a right angle.</li><li>Angles: <b>acute</b> (less than 90°), <b>right</b> (90°), <b>obtuse</b> (more than 90°, less than 180°), straight (180°).</li><li>A triangle with a right angle is a right triangle; with an obtuse angle, an obtuse triangle; with 3 acute angles, an acute triangle.</li></ul>',
        [example("Two lines cross and make 4 square corners. What are they?", ["Square corners are right angles."], "perpendicular lines"), example("A triangle has angles of 30°, 40° and 110°. What kind of triangle is it?", ["110° is more than 90°."], "an obtuse triangle")],
        [['Calling a ray a line segment', 'Count the endpoints: a ray has 1, a segment has 2.'], ['Calling any crossing lines perpendicular', 'Perpendicular lines must meet at a right angle.'], ['Thinking a right triangle has more than one right angle', 'A triangle can have at most one right angle.']])
    faq = [('What does TEKS 4.6A ask?', 'Identify points, lines, line segments, rays, angles, and perpendicular and parallel lines.'), ('What does TEKS 4.6C ask?', 'Use what you know about right angles to identify acute, right and obtuse triangles.'), ('What does TEKS 4.6D ask?', 'Classify 2D figures by whether they have parallel or perpendicular lines, or angles of a given size.'), ('How can I check for a right angle?', 'Hold the corner of a sheet of paper in the angle. If it fits exactly, it is a right angle.')]
    make('lines-angles-and-triangles', 18, 'Geometry and Measurement', '4.6A, 4.6C, 4.6D',
         '4.6A identify points, lines, line segments, rays, angles, and perpendicular and parallel lines; 4.6C apply knowledge of right angles to identify acute, right, and obtuse triangles; 4.6D classify two-dimensional figures based on the presence or absence of parallel or perpendicular lines or the presence or absence of angles of a specified size',
         'Lines, Angles and Classifying Figures', 'Lines, Angles and Classifying Figures',
         'Free Grade 4 geometry worksheets for Texas TEKS 4.6A, 4.6C and 4.6D: points, lines, segments and rays, parallel and perpendicular lines, kinds of angles, acute, right and obtuse triangles, and classifying shapes. 100 questions with answers.',
         'Parallel lines never meet. Perpendicular lines meet at a right angle.', 'Acute is less than 90°, right is 90°, obtuse is between 90° and 180°.',
         body, faq, sets, seo_title='Grade 4 Lines, Angles and Triangles Worksheets (TEKS 4.6A, 4.6C, 4.6D, STAAR)')


if __name__ == "__main__":
    build()
