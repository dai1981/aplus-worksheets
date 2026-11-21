# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 9: House of Hundreds – II (Adding and Subtracting 3-Digit Numbers)
Column addition and subtraction of 3-digit numbers with regrouping, checking and word problems (UK Year 3 and US Grade 3 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y3_column_add_sub", 603090)
us = mod("gen_us_math_g3_add_sub", 603091)
unit(3, "house-of-hundreds-2", 9, "N", 9, "House of Hundreds – II", "Adding and Subtracting 3-Digit Numbers", "3-digit add and subtract",
     "Addition and subtraction of numbers up to 1,000 with and without regrouping, and solving problems (summary of NCERT Maths Mela Class 3)",
     "Class 3 House of Hundreds – II worksheet (Maths Mela Chapter 9): column addition and subtraction with regrouping, checking and word problems. 100 questions with answers.",
     "Line up ones, tens and hundreds.", "Regroup 10 ones as 1 ten, 10 tens as 1 hundred.",
     "<ul><li>Write the numbers in columns: hundreds, tens, ones.</li><li>Add ones first; carry 1 ten if needed.</li><li>To subtract, break a ten or hundred when the top digit is smaller.</li></ul>",
     [('358 + 276', ['8 + 6 = 14: write 4, carry 1', '5 + 7 + 1 = 13: write 3, carry 1', '3 + 2 + 1 = 6'], '634')],
     [['Forgetting the carried 1', 'Write it above the next column.'], ['Taking the smaller digit from the bigger', 'Borrow from the next place.']],
     [('What is regrouping?', 'Exchanging 10 ones for 1 ten (or 10 tens for 1 hundred) when adding or subtracting.'), ('How can I check a subtraction?', 'Add the answer to the number taken away; you should get the first number.')],
     [('Column addition', [rn(uk, "set_add", 10), rn(us, "set_add1", 10)]),
      ('Adding with regrouping', [rn(us, "set_add2", 20)]),
      ('Column subtraction', [rn(uk, "set_sub1", 10), rn(us, "set_sub1", 10)]),
      ('Subtracting with regrouping', [rn(us, "set_sub2", 14), rn(uk, "set_check", 6)]),
      ('Word problems', [rn(uk, "set_story", 10), rn(us, "set_story", 10)])], 60309, max_num=1000)
