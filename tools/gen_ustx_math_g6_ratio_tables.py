# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Ratio Tables, Double Number Lines and Graphs (TEKS 6.5A)
  python3 tools/gen_ustx_math_g6_ratio_tables.py
Completing ratio tables, double number lines, graphing ratio pairs, unit prices, and comparing ratios in word
problems (the US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: adding the same number to both quantities, misreading the scale, and
switching x and y.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_ratio_tables as rt
import gen_us_math_g6_unit_rates as ur
adopt(rt)
adopt(ur)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Complete a ratio table", [("run", rt.set_tables, ("rnd",), 20)]),
        ("Double number lines", [("run", rt.set_lines, ("rnd",), 20)]),
        ("Plot ratio pairs on the coordinate plane", [("run", rt.set_graph, ("rnd",), 20)]),
        ("Unit price: the cost of one", [("run", ur.set_price, (ur.People,), 20)]),
        ("Compare ratios and word problems", [("run", rt.set_words, ("rnd",), 20)]),
    ], 66008)
    finish(sets, R)
    body = lesson('<ul><li>In a <b>ratio table</b>, multiply or divide both quantities by the same number.</li><li>A <b>double number line</b> lines up two quantities that grow together.</li><li>On a graph, equivalent ratios make points on a straight line through (0, 0).</li><li>Use a unit rate or a <b>scale factor</b> to find missing values.</li></ul>',
        [example("2 cups of juice for every 3 cups of water. Juice: 8 cups. Water?", ["8 ÷ 2 = 4 (scale factor)", "3 × 4"], "12 cups")],
        [['Adding the same number to both quantities', 'Equivalent ratios multiply both by the same number.'], ['Misreading the scale on a number line', 'Find the value of each step first.'], ['Switching x and y', 'Plot (first quantity, second quantity) in the order given.']])
    faq = [('What does TEKS 6.5A ask?', 'Represent mathematical and real-world problems involving ratios and rates using scale factors, tables, graphs and proportions.'), ('What is a scale factor?', 'The number you multiply both parts of a ratio by, such as 4 in 2 : 3 = 8 : 12.'), ('Why do ratio graphs go through (0, 0)?', '0 of one quantity always matches 0 of the other.'), ('How do I check a ratio table?', 'Divide each pair. The quotients should all be equal.')]
    make('ratio-tables-and-graphs', 8, 'Proportionality', '6.5A',
         '6.5A represent mathematical and real-world problems involving ratios and rates using scale factors, tables, graphs, and proportions',
         'Ratio Tables, Double Number Lines and Graphs', 'Ratio Tables and Graphs',
         'Free Grade 6 worksheets for Texas TEKS 6.5A: complete ratio tables, double number lines, graph ratio pairs, unit prices and ratio word problems. 100 questions with answers.',
         'Multiply or divide both quantities by the same number.', '2 : 3 = 8 : 12 (scale factor 4). Ratio graphs are lines through (0, 0).',
         body, faq, sets, seo_title='Grade 6 Ratio Tables, Double Number Lines and Graphs Worksheets (TEKS 6.5A, STAAR)')


if __name__ == "__main__":
    build()
