# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: The Constant of Proportionality (TEKS 7.4C)
  python3 tools/gen_ustx_math_g7_constant_of_proportionality.py
Deciding whether a table is proportional, finding k = y/x in tables, graphs and equations, writing y = kx, and word
problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: dividing x by y, checking only one pair, and thinking every straight line is
proportional.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_proportional_relationships as pr
adopt(pr)
pr.R = random.Random(670070)
tx_common.GRADE = "grade-7"

def no_foreign(it):
    """Skip exchange-rate items that use other countries' money."""
    return "Canadian" not in it["q"] + " ".join(it["c"]) + it["e"]


def build():
    sets, R = build_sets([
        ("Is it proportional? Tables", [("run", pr.set_tables, (), 20)]),
        ("Find k in a table", [("run", pr.set_constant, (), 20)]),
        ("Find k on a graph", [("run", pr.set_graphs, (), 20)]),
        ("Write the equation y = kx", [("run", pr.set_equations, (), 20)]),
        ("Word problems", [("run", pr.set_words, (), 20, no_foreign)]),
    ], 67007)
    finish(sets, R)
    body = lesson('<ul><li>In a <b>proportional relationship</b>, y ÷ x is the same for every pair. That number is the <b>constant of proportionality</b>, k.</li><li>The equation is <b>y = kx</b>.</li><li>On a graph, a proportional relationship is a straight line through (0, 0). The point (1, k) shows the constant.</li><li>In words, k is the unit rate: $12 per hour means y = 12x.</li></ul>',
        [example("x: 2, 4, 6  y: 14, 28, 42", ["14 ÷ 2 = 7, 28 ÷ 4 = 7"], "k = 7, y = 7x")],
        [['Dividing x by y', 'k = y ÷ x.'], ['Checking only one pair', 'Every pair must give the same quotient.'], ['Thinking every line is proportional', 'It must pass through (0, 0).']])
    faq = [('What does TEKS 7.4C ask?', 'Determine the constant of proportionality (k = y/x) within mathematical and real-world problems.'), ('Is y = 3x + 2 proportional?', 'No. Its graph does not pass through (0, 0).'), ('What does k mean in a story?', 'It is the unit rate, such as the cost of 1 item.'), ('How do I find k on a graph?', 'Find the y-value when x = 1, or divide y by x for any point.')]
    make('constant-of-proportionality', 7, 'Proportionality', '7.4C',
         '7.4C determine the constant of proportionality (k = y/x) within mathematical and real-world problems',
         'The Constant of Proportionality', 'Constant of Proportionality',
         'Free Grade 7 worksheets for Texas TEKS 7.4C: proportional tables, the constant of proportionality in tables, graphs and equations, y = kx and word problems. 100 questions with answers.',
         'k = y ÷ x, the same for every pair.', 'y = kx. The graph is a straight line through (0, 0).',
         body, faq, sets, seo_title='Grade 7 Constant of Proportionality Worksheets: y = kx (TEKS 7.4C, STAAR)')


if __name__ == "__main__":
    build()
