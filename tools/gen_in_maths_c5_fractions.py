# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 2: Fractions (Equivalent Fractions, Comparing, Adding and Subtracting)
Equivalent fractions, mixed numbers, comparing and ordering, adding and subtracting fractions (AU Year 5 and UK Year 5 set makers)."""
from in_prim import unit, mod, rn, co, le

cf = mod("gen_au_maths_y5_compare_fractions", 605020)
ef = mod("gen_uk_maths_y5_equivalent_fractions", 605021)
af = mod("gen_au_maths_y5_add_sub_fractions", 605022)
unit(5, "fractions", 2, "N", 2, "Fractions", "Equivalent Fractions, Comparing, Adding and Subtracting", "fractions",
     "Fractions: equivalent fractions, comparing and ordering fractions, mixed numbers, and adding and subtracting fractions with the same or related denominators (summary of NCERT Maths Mela Class 5)",
     "Class 5 Fractions worksheet (Maths Mela Chapter 2): equivalent fractions, comparing, mixed numbers, adding and subtracting. 100 questions with answers.",
     "Multiply top and bottom by the same number.", "Make the denominators the same to add.",
     "<ul><li>2/3 = 4/6 = 8/12: equivalent fractions.</li><li>To compare, use the same denominator: 3/4 = 9/12 &gt; 8/12 = 2/3.</li><li>1/4 + 3/8 = 2/8 + 3/8 = 5/8.</li></ul>",
     [('Add 1/2 + 1/6.', ['1/2 = 3/6', '3/6 + 1/6 = 4/6'], '2/3')],
     [['Adding denominators', 'Only the numerators are added once denominators match.'], ['Comparing only numerators', 'Make the denominators equal first.']],
     [('How do you make an equivalent fraction?', 'Multiply or divide the numerator and denominator by the same number.'), ('What is a mixed number?', 'A whole number and a fraction, like 2 1/4.')],
     [('Equivalent fractions', [rn(cf, "set_equivalent", 10), rn(ef, "set_missing", 10)]),
      ('Mixed numbers', [rn(cf, "set_mixed", 10), rn(ef, "set_mixed", 10)]),
      ('Compare and order', [rn(cf, "set_compare", 10), rn(cf, "set_order", 10)]),
      ('Add and subtract', [rn(af, "set_same", 10), rn(af, "set_related", 10)]),
      ('Fraction problems', [rn(af, "set_words", 10), rn(cf, "set_words", 10)])], 60502)
