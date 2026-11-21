# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 1: We the Travellers – I (Large Numbers and Place Value (Lakhs))
Numbers up to 10 lakh in the Indian system: place value, expanded form, number names, comparing and ordering (own makers and Ontario Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le
from in_prim import num_maker
ca = mod("gen_caon_math_g5_numbers", 605010)
unit(5, "we-the-travellers-1", 1, "N", 1, "We the Travellers – I", "Large Numbers and Place Value (Lakhs)", "large numbers",
     "Numbers beyond 10,000: reading and writing numbers in lakhs using the Indian place-value system, comparing and ordering, and place value (summary of NCERT Maths Mela Class 5)",
     "Class 5 We the Travellers – I worksheet (Maths Mela Chapter 1): lakhs, place value, expanded form, number names and comparing. 100 questions with answers.",
     "1 lakh = 1,00,000 = 100 thousand.", "Indian commas: 3 digits, then groups of 2.",
     "<ul><li>Places: ones, tens, hundreds, thousands, ten thousands, <b>lakhs</b>, ten lakhs.</li><li>3,45,678 is three lakh forty-five thousand six hundred and seventy-eight.</li><li>Compare from the biggest place.</li></ul>",
     [('What is the value of 6 in 2,63,450?', ['6 is in the ten thousands place'], '60,000')],
     [['Writing 1 lakh as 10,000', '1 lakh = 1,00,000.'], ['Putting commas every 3 digits', 'In India: 12,34,567.']],
     [('How many thousands make a lakh?', '100 thousands.'), ('How is the Indian system different?', 'After the thousands, commas come every two digits: lakhs and crores.')],
     [('Place value', [co(num_maker(10000, 999999, ("place",)), 20)]),
      ('Expanded form', [co(num_maker(10000, 999999, ("expand", "build")), 20)]),
      ('Number names', [co(num_maker(10000, 99999, ("words",)), 14), rn(ca, "set_read", 6)]),
      ('Compare and order', [co(num_maker(10000, 999999, ("cmp", "order")), 20)]),
      ('More and less', [co(num_maker(10000, 999999, ("more", "near")), 14), rn(ca, "set_life", 6)])], 60501)
