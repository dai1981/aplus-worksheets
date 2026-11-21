# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 14: The Surajkund Fair (Money, Patterns and Data)
Money up to ₹500 (counting, making amounts, buying and change), number patterns and reading data (in_money, Ontario Grade 3 and AU Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le
import in_money as m
pa = mod("gen_caon_math_g3_patterns", 603140)
da = mod("gen_au_maths_y3_data", 603141)
unit(3, "the-surajkund-fair", 14, "N", 14, "The Surajkund Fair", "Money, Patterns and Data", "money and the fair",
     "Money: adding and subtracting amounts, making bills and giving change; number and shape patterns; reading simple data (summary of NCERT Maths Mela Class 3)",
     "Class 3 The Surajkund Fair worksheet (Maths Mela Chapter 14): Indian money, buying and change, number patterns and data. 100 questions with answers.",
     "Change = money paid − cost.", "Count notes from the biggest.",
     "<ul><li>Count money from the biggest note: ₹200 + ₹100 + ₹50 + ₹20 = ₹370.</li><li>Total cost: add the prices. Change: subtract the cost from what you pay.</li></ul>",
     [('A clay pot costs ₹135. You pay ₹200.', ['₹200 − ₹135'], '₹65 change')],
     [['Adding the change to the price', 'Change is what is left: subtract.'], ['Counting notes as 1 each', 'Count the value written on each note.']],
     [('What is the Surajkund fair?', 'A crafts fair held every year in Haryana, where children see stalls, prices and patterns.'), ('Which notes are used up to ₹500?', '₹10, ₹20, ₹50, ₹100, ₹200 and ₹500.')],
     [('Count the money', [co(m.one_count(500, (3, 5)), 20)]),
      ('Make the amount', [co(m.one_make(500), 20)]),
      ('Shopping at the fair', [co(m.one_buy(500), 20)]),
      ('Number patterns', [rn(pa, "set_numbers", 10), rn(pa, "set_growing", 10)]),
      ('Fair data', [rn(da, "set_column", 10), rn(da, "set_compare", 10)])], 60314)
