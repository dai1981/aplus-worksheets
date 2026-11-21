# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 3: Double Century (Numbers up to 200)
Numbers to 200: hundreds, tens and ones, values of digits, partitioning, comparing and counting in steps (Ontario Grade 2 set makers)."""
from in_prim import unit, mod, rn, co, le, num_maker
N = num_maker(100, 200)

nu = mod("gen_caon_math_g2_numbers", 603030)
cn = mod("gen_caon_math_g2_counting", 603031)
unit(3, "double-century", 3, "N", 3, "Double Century", "Numbers up to 200", "numbers to 200",
     "Numbers up to 200: counting, grouping in hundreds, tens and ones, reading, writing, comparing and ordering (summary of NCERT Maths Mela Class 3)",
     "Class 3 Double Century worksheet (Maths Mela Chapter 3): hundreds, tens and ones, place value, comparing and counting to 200. 100 questions with answers.",
     "146 is 1 hundred, 4 tens and 6 ones.", "Compare hundreds, then tens, then ones.",
     "<ul><li>100 is 10 tens. 146 = 100 + 40 + 6.</li><li>To compare, look at the hundreds, then tens, then ones.</li></ul>",
     [('What is 1 hundred, 7 tens and 3 ones?', ['100 + 70 + 3'], '173')],
     [['Writing one hundred and five as 1005', '105: the tens place holds 0.'], ['Comparing ones first', 'Start from the biggest place.']],
     [('What does double century mean?', '200, like a batter scoring 200 runs.'), ('How do we write numbers past 100?', 'Use the hundreds place: 100, 101, …, 199, 200.')],
     [('Hundreds, tens and ones', [rn(nu, "set_blocks", 6, keep=le(200)), co(num_maker(100, 200, ("build", "expand")), 14)]),
      ('Value of a digit', [rn(nu, "set_value", 8, keep=le(200)), co(num_maker(100, 200, ("place", "words")), 12)]),
      ('Partitioning', [rn(nu, "set_decompose", 12, keep=le(200)), rn(nu, "set_estimate", 8, keep=le(200))]),
      ('Compare and order', [rn(nu, "set_compare", 10, keep=le(200)), co(num_maker(100, 200, ("cmp", "order", "near")), 10)]),
      ('Counting to 200', [rn(cn, "set_twenties", 7, keep=le(200)), rn(cn, "set_fifties", 7, keep=le(200)), rn(cn, "set_ones_tens", 6, keep=le(200))])], 60303)
