# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 5: Sharing and Measuring (Fractions)
Fractions of shapes and amounts, equivalent fractions, comparing and counting in fractions (UK Year 4, Ontario Grade 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y4_fractions", 604050)
ca = mod("gen_caon_math_g4_fractions", 604051)
au = mod("gen_au_maths_y4_counting_fractions", 604052)
unit(4, "sharing-and-measuring", 5, "N", 5, "Sharing and Measuring", "Fractions", "fractions",
     "Fractions: equal sharing, fractions of a whole and of a collection, equivalent fractions, and comparing fractions in measuring contexts (summary of NCERT Maths Mela Class 4)",
     "Class 4 Sharing and Measuring worksheet (Maths Mela Chapter 5): fractions of shapes and amounts, equivalent fractions, comparing. 100 questions with answers.",
     "3/4 of 20: 20 ÷ 4 × 3 = 15.", "Equal parts make fair shares.",
     "<ul><li>To find 3/4 of 20, divide by 4 then multiply by 3: 15.</li><li>1/2 = 2/4 = 4/8: equivalent fractions name the same amount.</li></ul>",
     [('Find 2/5 of 30.', ['30 ÷ 5 = 6', '6 × 2'], '12')],
     [['Dividing by the numerator', 'Divide by the denominator, then multiply by the numerator.'], ['Thinking 1/8 > 1/4', 'Eighths are smaller pieces.']],
     [('What are equivalent fractions?', 'Fractions that show the same amount, like 1/2 and 3/6.'), ('How do I find a fraction of a number?', 'Divide by the bottom number, then multiply by the top number.')],
     [('Fractions of shapes', [rn(uk, "set_diagrams", 10), rn(ca, "set_shapes_sets", 10)]),
      ('Fractions of amounts', [rn(uk, "set_amounts", 20)]),
      ('Equivalent fractions', [rn(uk, "set_families", 20)]),
      ('Compare fractions', [rn(ca, "set_compare", 10), rn(au, "set_pictures", 10)]),
      ('Sharing problems', [rn(uk, "set_words", 10), rn(ca, "set_words", 10)])], 60405)
