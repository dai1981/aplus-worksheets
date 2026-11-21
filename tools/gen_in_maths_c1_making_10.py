# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 4: Making 10 (Numbers 10 to 20)
Ten-frames, ways to make 10, teen numbers as 10 and some more, counting, comparing and ordering to 20."""
from in_prim import unit, mod, rn
nu = mod("gen_au_maths_f_numbers_to_20", 601041)
mk = mod("gen_cabc_math_g1_make_10", 601042)
uk = mod("gen_uk_maths_y1_number_bonds", 601043)
unit(1, "making-10", 4, "N", 4, "Making 10", "Numbers 10 to 20", "numbers 10 to 20",
     "Numbers 10 to 20: making 10, ten and some more, counting, reading and writing numbers to 20, comparing and ordering (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Making 10 worksheet (Joyful Mathematics Chapter 4): ways to make 10, teen numbers, counting, comparing and ordering to 20. 100 picture questions with answers.",
     "13 is 10 and 3 more.", "A full ten-frame holds 10.",
     "<ul><li>Pairs that make 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.</li><li>Teen numbers are <b>10 and some more</b>: 16 = 10 + 6.</li></ul>",
     [("How many more make 10 if you have 7?", ["7 + 3 = 10"], "3"), ("What is 10 and 4 more?", ["10 + 4"], "14")],
     [["Writing 13 as 31", "The 1 (one ten) comes first: 13."], ["Thinking 7 and 4 make 10", "7 needs 3 more to make 10."]],
     [("Why is making 10 important?", "Adding and subtracting become easier when you use 10 as a stepping stone."), ("What are teen numbers?", "11 to 19: each is 10 and some more ones.")],
     [("Ten-frames", [rn(mk, "set_frames", 10), rn(uk, "set_frames", 10)]),
      ("Ways to make 10", [rn(mk, "set_bonds", 10), rn(mk, "set_pairs", 10)]),
      ("Teen numbers", [rn(nu, "set_teens", 14), rn(nu, "set_story", 6)]),
      ("Counting to 20", [rn(nu, "set_count", 12), rn(uk, "set_twenty", 8)]),
      ("Compare and order", [rn(nu, "set_compare", 10), rn(nu, "set_order", 10)])], 60104, max_num=20)
