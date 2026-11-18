# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Sample Spaces and Compound Events (TEKS 7.6A, 7.6H)
  python3 tools/gen_ustx_math_g7_compound_probability.py
Counting outcomes with lists and tree diagrams, probability from a sample space, independent events, tables and
simulations, and word problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: adding the outcomes instead of multiplying, missing outcomes in a list, and
adding probabilities of independent events.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_compound_probability as cpb
adopt(cpb)
cpb.R = random.Random(670210)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Sample spaces: counting outcomes", [("run", cpb.set_count, (), 20)]),
        ("Probability from the sample space", [("run", cpb.set_from_space, (), 20)]),
        ("Independent events: multiply", [("run", cpb.set_multiply, (), 20)]),
        ("Tables, tree diagrams and simulations", [("run", cpb.set_tables, (), 20)]),
        ("Word problems", [("run", cpb.set_words, (), 20)]),
    ], 67021)
    finish(sets, R)
    body = lesson('<ul><li>A <b>sample space</b> is the list of all possible outcomes. Use an organized list, a table or a tree diagram.</li><li>Counting principle: 4 sandwiches × 3 drinks = 12 combos.</li><li>P(event) = favorable outcomes ÷ total outcomes.</li><li>For independent events, P(A and B) = P(A) × P(B).</li></ul>',
        [example("Flip a coin and roll a number cube.", ["2 × 6 = 12 outcomes", "P(heads and 3) = 1/12"], "1/12")],
        [['Adding instead of multiplying', '2 coins and 6 numbers make 2 × 6 = 12 outcomes.'], ['Missing outcomes', 'Use a tree diagram so you do not skip any.'], ['Adding probabilities of independent events', 'P(A and B) = P(A) × P(B).']])
    faq = [('What does TEKS 7.6A ask?', 'Represent sample spaces for simple and compound events using lists and tree diagrams.'), ('What does TEKS 7.6H ask?', 'Solve problems using qualitative and quantitative predictions and comparisons from simple experiments.'), ('What is a compound event?', 'An event made of two or more simple events, like flipping a coin and rolling a cube.'), ('What is a simulation?', 'A model, such as spinning a spinner, that acts like the real situation.')]
    make('sample-spaces-and-compound-events', 21, 'Proportionality', '7.6A, 7.6H',
         '7.6A represent sample spaces for simple and compound events using lists and tree diagrams; 7.6H solve problems using qualitative and quantitative predictions and comparisons from simple experiments',
         'Sample Spaces and Compound Events', 'Sample Spaces and Compound Events',
         'Free Grade 7 probability worksheets for Texas TEKS 7.6A and 7.6H: sample spaces, tree diagrams, compound events, independent events, tables and word problems. 100 questions with answers.',
         'P(event) = favorable outcomes ÷ total outcomes.', 'Coin and cube: 2 × 6 = 12 outcomes.',
         body, faq, sets, seo_title='Grade 7 Sample Spaces and Compound Events Worksheets (TEKS 7.6A, STAAR)')


if __name__ == "__main__":
    build()
