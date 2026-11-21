# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 8: Fair Share (Fractions and Equal Sharing)
Equal parts, halves, thirds and quarters of shapes and groups, fractions on a line and comparing (UK Year 3, Ontario and AU Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y3_fractions", 603080)
ca = mod("gen_caon_math_g3_fractions", 603081)
au = mod("gen_au_maths_y3_fractions", 603082)
unit(3, "fair-share", 8, "N", 8, "Fair Share", "Fractions and Equal Sharing", "fractions",
     "Fractions: sharing equally, half, one-third, one-fourth of shapes and collections, and comparing simple fractions (summary of NCERT Maths Mela Class 3)",
     "Class 3 Fair Share worksheet (Maths Mela Chapter 8): equal shares, halves, thirds and quarters, fractions of a group, comparing. 100 questions with answers.",
     "Fair shares are equal parts.", "1/4 means 1 of 4 equal parts.",
     "<ul><li>A fraction names equal parts of a whole: 3/4 means 3 of 4 equal parts.</li><li>1/4 of 12 rotis: 12 ÷ 4 = 3.</li><li>More equal parts make each part smaller: 1/4 &lt; 1/2.</li></ul>",
     [('What is 1/3 of 15?', ['15 ÷ 3'], '5')],
     [['Calling unequal parts halves', 'Halves must be the same size.'], ['Thinking 1/4 is bigger than 1/3', '4 parts are smaller than 3 parts.']],
     [('What is a fair share?', 'Sharing so everyone gets exactly the same amount.'), ('What is a unit fraction?', 'One equal part: 1/2, 1/3, 1/4 ….')],
     [('Equal parts', [rn(ca, "set_shares", 10), rn(au, "set_unit", 10)]),
      ('Shaded fractions', [rn(uk, "set_shaded", 20)]),
      ('Fractions of a group', [rn(uk, "set_objects", 10), rn(au, "set_collection", 10)]),
      ('Compare fractions', [rn(ca, "set_compare", 10), rn(uk, "set_compare", 10)]),
      ('Sharing stories', [rn(ca, "set_words", 10), rn(au, "set_words", 10)])], 60308)
