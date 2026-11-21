# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 4: Thousands Around Us (Numbers up to 9,999)
4-digit numbers: place value, expanded form, number names, comparing and ordering, more and less (UK Year 4 set makers and own makers)."""
from in_prim import unit, mod, rn, co, le
from in_prim import num_maker
pv = mod("gen_uk_maths_y4_place_value", 604040)
unit(4, "thousands-around-us", 4, "N", 4, "Thousands Around Us", "Numbers up to 9,999", "numbers to 9,999",
     "Numbers up to 9,999: thousands, hundreds, tens and ones, reading, writing and comparing 4-digit numbers (summary of NCERT Maths Mela Class 4)",
     "Class 4 Thousands Around Us worksheet (Maths Mela Chapter 4): thousands, place value, expanded form, number names, comparing. 100 questions with answers.",
     "4,536 = 4,000 + 500 + 30 + 6.", "Compare from the thousands place.",
     "<ul><li>10 hundreds = 1 thousand. 4,536 has 4 thousands, 5 hundreds, 3 tens and 6 ones.</li><li>Read it as four thousand five hundred and thirty-six.</li><li>Compare the thousands, then the hundreds, and so on.</li></ul>",
     [('What is 1,000 more than 3,507?', ['Add 1 to the thousands'], '4,507')],
     [['Writing four thousand and seven as 4007 with the wrong zeros', 'Fill empty places with 0: 4,007.'], ['Comparing by the last digit', 'Start with the biggest place.']],
     [('How many hundreds make a thousand?', '10.'), ('What is the biggest 4-digit number?', '9,999.')],
     [('Place value', [rn(pv, "set_value", 10, keep=le(9999)), co(num_maker(1000, 9999, ("place",)), 10)]),
      ('Expanded form', [rn(pv, "set_partition", 10, keep=le(9999)), co(num_maker(1000, 9999, ("expand", "build")), 10)]),
      ('More and less', [rn(pv, "set_more_less_count", 10, keep=le(9999)), co(num_maker(1000, 9999, ("more", "near")), 10)]),
      ('Compare and order', [rn(pv, "set_compare_zero", 10, keep=le(9999)), co(num_maker(1000, 9999, ("cmp", "order")), 10)]),
      ('Number names', [rn(pv, "set_words", 10, keep=le(9999)), co(num_maker(1000, 9999, ("words",)), 10)])], 60404)
