# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Scale Drawings and Maps (TEKS 7.5C)
  python3 tools/gen_ustx_math_g7_scale_drawings.py
What a scale means, from a drawing to real life, from real life to a drawing, area and redrawing, and word problems
with maps, models and plans (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: dividing instead of multiplying, using the scale for area without squaring,
and mixing up units.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_scale_drawings as sd
adopt(sd)
sd.R = random.Random(670110)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("What a scale means", [("run", sd.set_meaning, (), 20)]),
        ("From the drawing to real life", [("run", sd.set_actual, (), 20)]),
        ("From real life to the drawing", [("run", sd.set_drawing, (), 20)]),
        ("Area, finding the scale and redrawing", [("run", sd.set_area_and_rescale, (), 20)]),
        ("Word problems: maps, models and plans", [("run", sd.set_words, (), 20)]),
    ], 67011)
    finish(sets, R)
    body = lesson('<ul><li>A <b>scale</b> such as 1 in. : 4 ft compares a length on the drawing with the real length.</li><li>Drawing to real life: multiply by the scale. 3 in. × 4 = 12 ft.</li><li>Real life to drawing: divide by the scale. 20 ft ÷ 4 = 5 in.</li><li>For area, find the real lengths first, then multiply them.</li></ul>',
        [example("Scale 1 in. : 15 mi. Map distance 3.5 in.", ["3.5 × 15"], "52.5 mi")],
        [['Dividing instead of multiplying', 'Real distances are bigger than drawing distances.'], ['Scaling area with the length scale', 'Convert each length first, then multiply.'], ['Mixing units', 'Keep inches on the drawing and feet in real life.']])
    faq = [('What does TEKS 7.5C ask?', 'Solve mathematical and real-world problems involving similar shape and scale drawings.'), ('What is a scale factor?', 'The number you multiply drawing lengths by to get real lengths.'), ('Can a scale make something bigger?', 'Yes. A model of a cell is bigger than the real cell.'), ('How do I find the scale?', 'Divide the real length by the drawing length.')]
    make('scale-drawings', 11, 'Proportionality', '7.5C',
         '7.5C solve mathematical and real-world problems involving similar shape and scale drawings',
         'Scale Drawings and Maps', 'Scale Drawings',
         'Free Grade 7 scale drawing worksheets for Texas TEKS 7.5C: what a scale means, drawing to real life, real life to drawing, area and map word problems. 100 questions with answers.',
         'Drawing to real life: multiply by the scale.', '1 in. : 15 mi, 3.5 in. → 52.5 mi.',
         body, faq, sets, seo_title='Grade 7 Scale Drawings and Maps Worksheets (TEKS 7.5C, STAAR)')


if __name__ == "__main__":
    build()
