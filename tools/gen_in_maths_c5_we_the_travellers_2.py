# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 4: We the Travellers – II (Adding and Subtracting Large Numbers)
Column addition and subtraction of large numbers, mental methods, estimating and checking, travel stories (UK Year 5 and BC Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_column_add_sub", 605040)
bc = mod("gen_cabc_math_g5_add_sub", 605041)
unit(5, "we-the-travellers-2", 4, "N", 4, "We the Travellers – II", "Adding and Subtracting Large Numbers", "add and subtract large numbers",
     "Addition and subtraction of large numbers, estimation and checking, and solving problems about travel and distances (summary of NCERT Maths Mela Class 5)",
     "Class 5 We the Travellers – II worksheet (Maths Mela Chapter 4): column addition and subtraction, estimating, checking and travel stories. 100 questions with answers.",
     "Estimate, calculate, then check.", "Line up the digits by place.",
     "<ul><li>Line up the ones and regroup where needed.</li><li>Round to estimate: 48,615 + 23,290 ≈ 49,000 + 23,000 = 72,000.</li><li>Check subtraction by adding.</li></ul>",
     [('A train travels 1,348 km and then 2,795 km.', ['1,348 + 2,795'], '4,143 km')],
     [['Misaligned columns', 'Line up from the ones.'], ['Forgetting to regroup', 'Carry or borrow when a column needs it.']],
     [('Why estimate first?', 'So you can tell if the exact answer is sensible.'), ('How do I check subtraction?', 'Add the answer to the number subtracted.')],
     [('Column addition', [rn(uk, "set_add", 20)]),
      ('Column subtraction', [rn(uk, "set_sub", 20)]),
      ('Mental methods', [rn(uk, "set_mental", 20)]),
      ('Estimate and check', [rn(uk, "set_check", 10), rn(bc, "set_estimate", 10)]),
      ('Travel stories', [rn(uk, "set_story", 14), rn(bc, "set_story", 6)])], 60504)
