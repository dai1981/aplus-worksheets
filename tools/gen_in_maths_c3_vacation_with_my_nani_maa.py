# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 4: Vacation with My Nani Maa (Addition and Subtraction)
Mental addition and subtraction strategies, inverse facts, missing numbers and word problems (AU Year 3 and Ontario Grade 3 set makers)."""
from in_prim import unit, mod, rn, co, le

me = mod("gen_au_maths_y3_mental", 603040)
ca = mod("gen_caon_math_g3_add_sub", 603041)
unit(3, "vacation-with-my-nani-maa", 4, "N", 4, "Vacation with My Nani Maa", "Addition and Subtraction", "adding and subtracting",
     "Addition and subtraction of 2- and 3-digit numbers using mental strategies, the link between addition and subtraction, and daily-life problems (summary of NCERT Maths Mela Class 3)",
     "Class 3 Vacation with My Nani Maa worksheet (Maths Mela Chapter 4): mental strategies, fact families, missing numbers and word problems. 100 questions with answers.",
     "Subtraction undoes addition.", "If 45 + 38 = 83, then 83 − 38 = 45.",
     "<ul><li>Add tens first, then ones: 45 + 38 = 75 + 8 = 83.</li><li>Use a near ten: 57 + 19 = 57 + 20 − 1 = 76.</li><li>Check a subtraction by adding back.</li></ul>",
     [('64 + 29', ['64 + 30 = 94', '94 − 1'], '93')],
     [['Forgetting to take back the 1 after adding 20 for 19', 'Adding 20 adds 1 too many.'], ['Subtracting the smaller digit from the bigger in each place', 'Break a ten when the top digit is smaller.']],
     [('What is a fact family?', 'Facts with the same three numbers: 8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8, 13 − 8 = 5.'), ('Why use mental strategies?', 'They make many sums quick without writing.')],
     [('Number facts', [rn(me, "set_facts", 14), rn(ca, "set_add", 6)]),
      ('Mental strategies', [rn(me, "set_strategies", 10), rn(ca, "set_mental", 10)]),
      ('Add and subtract are linked', [rn(me, "set_inverse", 10), rn(ca, "set_inverse", 10)]),
      ('Missing numbers', [rn(me, "set_unknowns", 20)]),
      ('Travel stories', [rn(me, "set_words", 10), rn(ca, "set_story", 10)])], 60304, max_num=1000)
