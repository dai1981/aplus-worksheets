# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 10: Fun at Class Party! (Division, Sharing and Grouping)
Division as sharing and grouping, division facts, the link with multiplication and party stories (Ontario Grade 3, AU Year 3 and UK Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

ca = mod("gen_caon_math_g3_mult_div", 603100)
au = mod("gen_au_maths_y3_mult_div", 603101)
tt = mod("gen_uk_maths_y3_times_tables", 603102)
fa = mod("gen_caon_math_g3_facts", 603103)
unit(3, "fun-at-class-party", 10, "N", 10, "Fun at Class Party!", "Division, Sharing and Grouping", "division",
     "Division as equal sharing and grouping, its relation to multiplication, and solving problems (summary of NCERT Maths Mela Class 3)",
     "Class 3 Fun at Class Party! worksheet (Maths Mela Chapter 10): sharing, grouping, division facts and stories. 100 questions with answers.",
     "12 ÷ 3 = 4 because 3 × 4 = 12.", "Division shares equally or makes equal groups.",
     "<ul><li><b>Sharing</b>: 20 sweets among 4 children → 20 ÷ 4 = 5 each.</li><li><b>Grouping</b>: 20 sweets in packets of 4 → 5 packets.</li><li>Use a times table: 4 × 5 = 20, so 20 ÷ 4 = 5.</li></ul>",
     [('Share 18 laddoos among 3 friends.', ['3 × 6 = 18'], '6 each')],
     [['Subtracting instead of dividing', 'Share into equal groups.'], ['Using the wrong table', 'Think: ? × 3 = 18.']],
     [('How are multiplication and division linked?', 'Division undoes multiplication: 6 × 3 = 18, so 18 ÷ 3 = 6.'), ('What is a remainder?', 'What is left over when things cannot be shared equally.')],
     [('Sharing equally', [rn(ca, "set_divide", 16), rn(fa, "set_mixed", 4)]),
      ('Grouping', [rn(au, "set_divide", 16), rn(fa, "set_missing", 4)]),
      ('Division facts', [rn(fa, "set_division", 10), rn(tt, "set_division", 10)]),
      ('Multiply or divide?', [rn(ca, "set_inverse", 10), rn(au, "set_choose", 10)]),
      ('Party stories', [rn(au, "set_story", 10), rn(tt, "set_words", 10)])], 60310)
