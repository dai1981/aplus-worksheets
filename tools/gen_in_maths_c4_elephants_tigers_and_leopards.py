# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 10: Elephants, Tigers and Leopards (4-Digit Addition, Subtraction and Estimation)
Adding and subtracting 4-digit numbers, numbers with zeros, estimating by rounding and mental shortcuts in animal census stories (US Grade 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

us = mod("gen_us_math_g4_add_sub", 604100)
ro = mod("gen_au_maths_y4_rounding_estimation", 604101)
au = mod("gen_au_maths_y4_add_sub", 604102)
unit(4, "elephants-tigers-and-leopards", 10, "N", 10, "Elephants, Tigers and Leopards", "4-Digit Addition, Subtraction and Estimation", "4-digit add and subtract",
     "Addition and subtraction of 4-digit numbers, estimation, mental calculation and problems using data (summary of NCERT Maths Mela Class 4)",
     "Class 4 Elephants, Tigers and Leopards worksheet (Maths Mela Chapter 10): 4-digit adding and subtracting, estimating and mental shortcuts. 100 questions with answers.",
     "Estimate first, then calculate.", "8,787 − 99 = 8,787 − 100 + 1.",
     "<ul><li>Round to estimate: 2,489 + 3,512 ≈ 2,500 + 3,500 = 6,000.</li><li>Use friendly numbers: 3,459 + 21 = 3,480.</li></ul>",
     [('A state has 3,128 elephants and another has 2,946. How many in all?', ['3,128 + 2,946'], '6,074')],
     [['Lining up digits from the left', 'Line up the ones.'], ['Not checking with an estimate', 'An estimate shows if the answer is sensible.']],
     [('Why estimate?', 'To check that an exact answer is reasonable.'), ('What is a mental shortcut?', 'Using easy numbers, like adding 100 and taking away 1 to add 99.')],
     [('Add 4-digit numbers', [rn(us, "set_add4", 20, keep=le(99999))]),
      ('Subtract 4-digit numbers', [rn(us, "set_sub4", 20, keep=le(99999))]),
      ('Subtract across zeros', [rn(us, "set_zeros", 20, keep=le(99999))]),
      ('Estimate', [rn(ro, "set_sums", 10), rn(ro, "set_reasonable", 10)]),
      ('Animal census stories', [rn(au, "set_mental", 10), rn(us, "set_story", 10, keep=le(99999))])], 60410)
