# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 6: The Dairy Farm (Multiplication)
Mental multiplication, short and long multiplication, area models and dairy farm stories (UK Year 5, AU Year 5 and US Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_multiplication", 605060)
au = mod("gen_au_maths_y5_multiplication", 605061)
unit(5, "the-dairy-farm", 6, "N", 6, "The Dairy Farm", "Multiplication", "multiplication",
     "Multiplication of larger numbers: mental strategies, multiplying by 10, 100 and 1,000, the standard method for 2- and 3-digit numbers, and problems (summary of NCERT Maths Mela Class 5)",
     "Class 5 The Dairy Farm worksheet (Maths Mela Chapter 6): mental methods, area models, short and long multiplication and stories. 100 questions with answers.",
     "Split numbers to multiply in parts.", "Multiply by tens, then ones, and add.",
     "<ul><li>24 × 35 = 24 × 30 + 24 × 5 = 720 + 120 = 840.</li><li>Long multiplication: multiply by the ones, then the tens (add a 0), then add.</li></ul>",
     [('A farm gets 245 litres of milk a day. How much in 12 days?', ['245 × 10 = 2,450', '245 × 2 = 490', '2,450 + 490'], '2,940 litres')],
     [['Forgetting the 0 when multiplying by tens', 'The tens row starts with a 0.'], ['Adding the partial products wrongly', 'Line up the rows before adding.']],
     [('What is long multiplication?', 'A written method for multiplying by a 2-digit number using two rows of partial products.'), ('How do I check?', 'Estimate: 245 × 12 ≈ 250 × 10 = 2,500.')],
     [('Mental multiplication', [rn(uk, "set_mental", 10), rn(au, "set_mental", 10)]),
      ('Area models', [rn(au, "set_area", 20)]),
      ('Short multiplication', [rn(uk, "set_short", 10), rn(au, "set_short", 10)]),
      ('Long multiplication', [rn(uk, "set_2x2", 10), rn(au, "set_long", 10)]),
      ('Dairy farm stories', [rn(uk, "set_story", 10), rn(au, "set_story", 10)])], 60506)
