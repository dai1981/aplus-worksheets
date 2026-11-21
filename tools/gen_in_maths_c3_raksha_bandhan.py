# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 7: Raksha Bandhan (Multiplication and Equal Groups)
Equal groups and repeated addition, multiplication tables of 2, 3, 4, 5, 8 and 10, and word problems (Ontario Grade 3, AU Year 3 and UK Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

ca = mod("gen_caon_math_g3_mult_div", 603070)
mf = mod("gen_au_maths_y3_multiplication_facts", 603071)
tt = mod("gen_uk_maths_y3_times_tables", 603072)
unit(3, "raksha-bandhan", 7, "N", 7, "Raksha Bandhan", "Multiplication and Equal Groups", "multiplication",
     "Multiplication as repeated addition and equal groups; multiplication facts and tables; using multiplication in daily life (summary of NCERT Maths Mela Class 3)",
     "Class 3 Raksha Bandhan worksheet (Maths Mela Chapter 7): equal groups, repeated addition, times tables and word problems. 100 questions with answers.",
     "4 × 6 means 4 groups of 6.", "Times tables help you find totals quickly.",
     "<ul><li>5 rakhis in each of 3 packets: 5 + 5 + 5 = 3 × 5 = 15.</li><li>Changing the order gives the same answer: 3 × 5 = 5 × 3.</li></ul>",
     [('6 sweets in each of 4 boxes.', ['4 × 6'], '24 sweets')],
     [['Adding the numbers (4 + 6)', '4 groups of 6 is 6 + 6 + 6 + 6.'], ['Skipping a step when skip counting', 'Say each multiple: 6, 12, 18, 24.']],
     [('Which tables do Class 3 children learn?', 'Tables of 2 to 10, starting with 2, 3, 4, 5 and 10.'), ('What is repeated addition?', 'Adding the same number again and again, which multiplication does in one step.')],
     [('Equal groups', [rn(ca, "set_groups", 14), rn(mf, "set_mixed", 6)]),
      ('Repeated addition', [rn(ca, "set_repeated", 20)]),
      ('Tables of 3, 4, 5 and 10', [rn(mf, "set_three_four", 10), rn(mf, "set_five_ten", 10)]),
      ('Tables of 3, 4 and 8', [rn(tt, "set_three", 7), rn(tt, "set_four", 7), rn(tt, "set_eight", 6)]),
      ('Multiplication stories', [rn(mf, "set_words", 10), rn(ca, "set_story", 10)])], 60307)
