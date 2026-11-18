# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Two-Step Inequalities (TEKS 7.10A, 7.10B, 7.11A, 7.11B)
  python3 tools/gen_ustx_math_g7_two_step_inequalities.py
Inequality basics and graphs, solving with positive and negative coefficients, solving and graphing, and word
problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: forgetting to flip the sign when dividing by a negative, using an open
circle for ≥, and shading the wrong way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_two_step_inequalities as ti
adopt(ti)
ti.R = random.Random(670180)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Inequality basics and graphs", [("run", ti.set_basics, (), 20)]),
        ("Solve with positive coefficients", [("run", ti.set_positive, (), 20)]),
        ("Solve with negative coefficients", [("run", ti.set_negative, (), 20)]),
        ("Solve and graph", [("run", ti.set_graph_solutions, (), 20)]),
        ("Word problems", [("run", ti.set_words, (), 20)]),
    ], 67018)
    finish(sets, R)
    body = lesson('<ul><li>Solve a two-step inequality like an equation: undo + or −, then × or ÷.</li><li>When you multiply or divide both sides by a <b>negative</b> number, <b>flip</b> the inequality sign.</li><li>Graph: open circle for &lt; and &gt;, closed circle for ≤ and ≥.</li><li>Check a number from the shaded part in the original inequality.</li></ul>',
        [example("2x + 3 > 11", ["2x > 8", "x > 4"], "x > 4"), example("−2x + 3 > 11", ["−2x > 8", "Divide by −2 and flip"], "x < −4")],
        [['Not flipping when dividing by a negative', '−2x > 8 gives x < −4.'], ['Using an open circle for ≥', '≥ and ≤ include the number: closed circle.'], ['Shading the wrong way', 'Test a point to check the direction.']])
    faq = [('What does TEKS 7.10B ask?', 'Represent solutions for one-variable, two-step equations and inequalities on number lines.'), ('Why flip the sign for a negative?', 'Multiplying by a negative reverses order: 2 < 3, but −2 > −3.'), ('What does at most mean?', 'Less than or equal to: ≤.'), ('How do I check my graph?', 'Pick a number in the shaded part and test it.')]
    make('two-step-inequalities', 18, 'Expressions, Equations and Relationships', '7.10A, 7.10B, 7.11A, 7.11B',
         '7.10A write one-variable, two-step equations and inequalities to represent constraints or conditions within problems; 7.10B represent solutions for one-variable, two-step equations and inequalities on number lines; 7.11A model and solve one-variable, two-step equations and inequalities; 7.11B determine if the given value(s) make(s) one-variable, two-step equations and inequalities true',
         'Two-Step Inequalities', 'Two-Step Inequalities',
         'Free Grade 7 two-step inequality worksheets for Texas TEKS 7.10 and 7.11: basics, solving with positive and negative coefficients, graphing and word problems. 100 questions with answers.',
         'Flip the sign when you multiply or divide by a negative.', '2x + 3 > 11 → x > 4. −2x + 3 > 11 → x < −4.',
         body, faq, sets, seo_title='Grade 7 Two-Step Inequalities Worksheets (TEKS 7.10B, 7.11A, STAAR)')


if __name__ == "__main__":
    build()
