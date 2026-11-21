# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 9: Equal Groups (Multiplication)
Times tables to 10 × 10, multiplying by 10 and 100, factor pairs and multiplying 2- and 3-digit numbers (UK Year 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

tt = mod("gen_uk_maths_y4_times_tables", 604090)
mm = mod("gen_uk_maths_y4_mental_mult_div", 604091)
sm = mod("gen_uk_maths_y4_short_multiplication", 604092)
unit(4, "equal-groups", 9, "N", 9, "Equal Groups", "Multiplication", "multiplication",
     "Multiplication: equal groups and arrays, multiplication facts, multiplying 2- and 3-digit numbers by 1-digit numbers (summary of NCERT Maths Mela Class 4)",
     "Class 4 Equal Groups worksheet (Maths Mela Chapter 9): times tables, factor pairs, multiplying by 10 and short multiplication. 100 questions with answers.",
     "4 × 23 = 4 × 20 + 4 × 3 = 92.", "Multiplying by 10 moves the digits one place left.",
     "<ul><li>Know the tables to 10 × 10.</li><li>Split numbers: 6 × 34 = 6 × 30 + 6 × 4 = 180 + 24 = 204.</li><li>× 10: 37 → 370; × 100: 37 → 3,700.</li></ul>",
     [('7 × 46', ['7 × 40 = 280', '7 × 6 = 42', '280 + 42'], '322')],
     [['Multiplying only the tens', 'Multiply both the tens and the ones.'], ['Forgetting the carried ten', 'Add it to the next column.']],
     [('Which tables should Class 4 children know?', 'All tables up to 10 × 10.'), ('What is a factor pair?', 'Two numbers that multiply to make a number, like 4 and 6 for 24.')],
     [('Times tables', [rn(tt, "set_easy", 10), rn(tt, "set_679", 10)]),
      ('Multiplying by 10 and 100', [rn(mm, "set_place_value", 20)]),
      ('Factor pairs', [rn(mm, "set_factor_pairs", 20)]),
      ('Short multiplication', [rn(sm, "set_grid", 10), rn(sm, "set_short2", 10)]),
      ('Equal group stories', [rn(tt, "set_words", 10), rn(sm, "set_story", 10)])], 60409)
