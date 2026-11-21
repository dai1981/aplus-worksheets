# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 1: What's in a Name? (Counting, Tally Marks and Data)
Counting with tally marks, tally tables, pictographs and comparing counts (UK Year 3, Ontario, BC and AU Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y3_statistics", 603010)
ca = mod("gen_caon_math_g3_data", 603011)
bc = mod("gen_cabc_math_g3_graphs", 603012)
au = mod("gen_au_maths_y3_data", 603013)
unit(3, "whats-in-a-name", 1, "D", 1, "What's in a Name?", "Counting, Tally Marks and Data", "tally marks and data",
     "Counting objects and letters, recording counts with tally marks, organising them in tables and comparing them (summary of NCERT Maths Mela Class 3)",
     "Class 3 What's in a Name? worksheet (Maths Mela Chapter 1): counting with tally marks, tally tables, pictographs and comparing. 100 questions with answers.",
     "Tally marks are drawn in fives.", "Count the groups of five, then the extra marks.",
     "<ul><li>Tally marks: four lines and one across = 5.</li><li>Count tallies in fives, then add the rest: two fives and 3 = 13.</li><li>A table lets us compare: which is most, fewest, how many more.</li></ul>",
     [('Count: two groups of five and 4 more.', ['5 + 5 + 4'], '14')],
     [['Counting the crossing line as a sixth mark', 'Four upright lines and one across make 5.'], ['Adding when asked how many more', 'How many more means subtract.']],
     [("Why is the chapter called What's in a Name?", 'Children count letters in names and record the counts with tally marks.'), ('What are tally marks?', 'Marks drawn in groups of five to keep count quickly.')],
     [('Read tally marks', [rn(ca, "set_tally", 10), rn(bc, "set_tally", 10)]),
      ('Tally tables', [rn(uk, "set_tally_table", 20)]),
      ('Pictographs', [rn(au, "set_pictograph", 10), rn(ca, "set_pictograph", 10)]),
      ('Compare the counts', [rn(uk, "set_compare", 10), rn(bc, "set_compare", 10)]),
      ('Data stories', [rn(uk, "set_words", 10), rn(au, "set_words", 10)])], 60301)
