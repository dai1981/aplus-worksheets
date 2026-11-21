# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 6: House of Hundreds – I (Numbers up to 1,000 and Place Value)
Hundreds, tens and ones up to 1,000: place value, number names, 10 and 100 more or less, comparing and problems (UK Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

pv = mod("gen_uk_maths_y3_place_value", 603060)
unit(3, "house-of-hundreds-1", 6, "N", 6, "House of Hundreds – I", "Numbers up to 1,000 and Place Value", "numbers to 1,000",
     "Numbers up to 1,000: place value, reading and writing numerals and number names, comparing and ordering, 10 and 100 more or less (summary of NCERT Maths Mela Class 3)",
     "Class 3 House of Hundreds – I worksheet (Maths Mela Chapter 6): hundreds, tens and ones, number names, 10 and 100 more or less, comparing. 100 questions with answers.",
     "Each place is 10 times the place to its right.", "10 hundreds make 1,000.",
     "<ul><li>586 = 5 hundreds + 8 tens + 6 ones = 500 + 80 + 6.</li><li>100 more changes the hundreds digit: 586 → 686.</li></ul>",
     [('What is 100 more than 347?', ['Add 1 to the hundreds'], '447')],
     [['Writing four hundred and six as 4006', '406: 0 holds the tens place.'], ['Changing the wrong digit for 10 more', '10 more changes the tens digit.']],
     [('How many hundreds make a thousand?', '10.'), ('What is place value?', 'The value of a digit depends on its place: in 586, the 5 means 500.')],
     [('Hundreds, tens and ones', [rn(pv, "set_hto", 20)]),
      ('Number names', [rn(pv, "set_words", 20)]),
      ('10 and 100 more or less', [rn(pv, "set_more_less", 20)]),
      ('Compare and order', [rn(pv, "set_compare", 20)]),
      ('Number problems', [rn(pv, "set_problems", 20)])], 60306, max_num=1000)
