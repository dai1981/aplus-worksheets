# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 12: Give and Take (Addition and Subtraction Practice)
More addition and subtraction up to 1,000: mental methods, column methods, checking and two-step stories (SG Primary 3 and AU Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

sg = mod("gen_sg_maths_p3_add_sub", 603120)
ca = mod("gen_cabc_math_g3_add_sub", 603122)
au = mod("gen_au_maths_y3_add_sub", 603121)
unit(3, "give-and-take", 12, "N", 12, "Give and Take", "Addition and Subtraction Practice", "give and take",
     "Addition and subtraction of numbers up to 1,000 in different situations, estimating and checking answers (summary of NCERT Maths Mela Class 3)",
     "Class 3 Give and Take worksheet (Maths Mela Chapter 12): mental and column methods, checking and word problems. 100 questions with answers.",
     "Give means add on; take means take away.", "Check with the opposite operation.",
     "<ul><li>Add or subtract in parts: 465 + 230 = 665 + 30 = 695.</li><li>Estimate first: 398 + 205 is about 400 + 200 = 600.</li><li>Check by doing the opposite.</li></ul>",
     [('Riya had ₹500 and spent ₹235. How much is left?', ['500 − 235'], '₹265')],
     [['Lining up digits from the left', 'Line up the ones.'], ["Adding in a 'how much is left' problem", 'Left means subtract.']],
     [('Why estimate?', 'To check that an answer is sensible.'), ('What is a two-step problem?', 'A problem that needs two calculations, such as adding and then subtracting.')],
     [('Mental adding and subtracting', [rn(sg, "set_mental", 10), rn(au, "set_partition", 10)]),
      ('Adding', [rn(ca, "set_add", 10), rn(au, "set_add", 10)]),
      ('Subtracting', [rn(ca, "set_sub", 10), rn(au, "set_sub", 10)]),
      ('Check your answer', [rn(ca, "set_mental", 10), rn(au, "set_jump", 10)]),
      ('Give and take stories', [rn(ca, "set_story", 10), rn(au, "set_story", 10)])], 60312, max_num=1000)
