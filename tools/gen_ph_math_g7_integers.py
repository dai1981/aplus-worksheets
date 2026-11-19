# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Integers, Opposites and Absolute Value (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_integers.py
Positive and negative numbers in real life, integers on the number line, opposites, comparing and ordering, and
absolute value (US Grade 6 makers with Filipino names).
Wrong answers come from real mistakes: thinking −8 is greater than −3, giving a negative absolute value, and
mixing up the opposite and the absolute value.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g6_negative_numbers as unn
adopt(unn)
if hasattr(unn, 'R'): unn.R = random.Random(707210)
import gen_us_math_g6_absolute_value as uav
adopt(uav)
if hasattr(uav, 'R'): uav.R = random.Random(707211)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Integers in real life", [("run", unn.set_situations, ("rnd", unn.People), 20)]),
        ("Integers on the number line", [("run", unn.set_read, ("rnd", unn.People), 20)]),
        ("Opposites", [("run", unn.set_opposites, ("rnd", unn.People), 20)]),
        ("Compare and order integers", [("run", uav.set_compare, ("rnd", uav.People), 10), ("run", uav.set_order, ("rnd", uav.People), 10)]),
        ("Absolute value", [("run", uav.set_abs, ("rnd", uav.People), 10), ("run", uav.set_vs, ("rnd", uav.People), 10)]),
    ], 70721)
    finish(sets, R)
    body = lesson('<ul><li>The <b>integers</b> are …, −3, −2, −1, 0, 1, 2, 3, … Positive and negative numbers describe opposites: above or below sea level, gain or loss, deposit or withdrawal.</li><li>On a number line, numbers increase to the right. −3 &gt; −8.</li><li>Opposites are the same distance from 0 on different sides: 5 and −5.</li><li>The <b>absolute value</b> |a| is the distance from 0, so it is never negative: |−7| = 7.</li></ul>',
        [example("Order −4, 2, −9, 0", ["farthest left first"], "−9, −4, 0, 2"), example("|−12|", ["12 units from 0"], "12")],
        [['−8 &gt; −3', '−8 is farther left, so it is smaller.'], ['Negative absolute value', '|−7| = 7.'], ['Opposite or absolute value?', 'The opposite of −7 is 7; the opposite of 7 is −7.']])
    faq = [('What does MATATAG Math 7 ask about integers?', 'Describe the set of integers, use positive and negative numbers for directions or opposites, locate integers on the number line, compare and order them, and identify the absolute value.'), ('Is 0 positive or negative?', 'Neither.'), ('What is the opposite of 0?', '0.'), ('What does |−4| mean?', 'The distance of −4 from 0, which is 4.')]
    make('integers-and-absolute-value', 21, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Describe the set of integers; use positive and negative numbers to describe directions or opposites in real-life situations; locate integers on the number line; compare and order integers; identify the absolute value of an integer, and its meaning on the number line.',
         'Integers, Opposites and Absolute Value', 'Integers and Absolute Value',
         'Free Grade 7 integers worksheets for the DepEd MATATAG curriculum: integers in real life, the number line, opposites, comparing and ordering, and absolute value. 100 questions with answers.',
         'Numbers increase to the right on a number line.', '|a| is the distance from 0: never negative.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
