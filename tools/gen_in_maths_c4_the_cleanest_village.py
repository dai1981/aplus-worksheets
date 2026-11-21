# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 7: The Cleanest Village (Addition and Subtraction)
Column addition and subtraction of 3- and 4-digit numbers, checking with the inverse and word problems (UK Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y4_column_add_sub", 604070)
unit(4, "the-cleanest-village", 7, "N", 7, "The Cleanest Village", "Addition and Subtraction", "adding and subtracting",
     "Addition and subtraction of numbers up to 9,999 with regrouping, and solving word problems (summary of NCERT Maths Mela Class 4)",
     "Class 4 The Cleanest Village worksheet (Maths Mela Chapter 7): column addition and subtraction, checking and word problems. 100 questions with answers.",
     "Line up the places and work from the ones.", "Check a subtraction by adding.",
     "<ul><li>Write numbers in columns: thousands, hundreds, tens, ones.</li><li>Regroup (carry or borrow) when a column needs it.</li><li>Check: 5,302 − 1,876 = 3,426 because 3,426 + 1,876 = 5,302.</li></ul>",
     [('2,457 + 1,368', ['7 + 8 = 15', '5 + 6 + 1 = 12', '4 + 3 + 1 = 8', '2 + 1 = 3'], '3,825')],
     [['Forgetting a carried ten', 'Write it at the top of the next column.'], ['Borrowing across a zero wrongly', 'In 4,005 − 1,238, break a thousand into 9 hundreds, 9 tens and 10 ones.']],
     [('What is the inverse of subtraction?', 'Addition: it undoes subtraction, so we use it to check.'), ('What is a word problem?', 'A story that needs a calculation to answer.')],
     [('Adding', [rn(uk, "set_add_easy", 20)]),
      ('Adding with regrouping', [rn(uk, "set_add_hard", 20)]),
      ('Subtracting', [rn(uk, "set_sub", 20)]),
      ('Check with the inverse', [rn(uk, "set_check", 20)]),
      ('Village stories', [rn(uk, "set_story", 20)])], 60407)
