# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Numbers up to 1,000,000: Place Value, Reading, Writing and Comparing (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_numbers_to_1000000.py
Place value and value of digits, numbers in words and expanded form, partitioning, and comparing numbers up to
1,000,000 (US Grade 4 and UK Year 4 makers with Filipino names).
Wrong answers come from real mistakes: giving the digit instead of its value, leaving out a zero, and comparing the
first digits of numbers with different lengths.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_place_value as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(704040)
import gen_uk_maths_y4_place_value as ukp
adopt(ukp)
if hasattr(ukp, 'R'): ukp.R = random.Random(704041)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Place value and the value of a digit", [("run", usp.set_value, ("rnd", "seen"), 20)]),
        ("Numbers in words and expanded form", [("run", usp.set_forms, ("rnd", "seen"), 20)]),
        ("Ten times as much", [("run", usp.set_ten_times, ("rnd", "seen"), 20)]),
        ("Break numbers into parts", [("run", ukp.set_partition, ("rnd", "seen"), 20)]),
        ("Compare numbers", [("run", usp.set_compare, ("rnd", "seen", usp.People), 20)]),
    ], 70404)
    finish(sets, R)
    body = lesson('<ul><li>Each digit has a <b>place</b> (ones, tens, hundreds, thousands, ten thousands, hundred thousands) and a <b>value</b> (the digit times its place).</li><li>In 482,375 the 8 is in the ten thousands place; its value is 80,000.</li><li>Read big numbers in groups of three: 482 thousand, 375.</li><li>To compare, first count the digits. If they have the same number of digits, compare from the left.</li></ul>',
        [example("Value of 6 in 361,042", ["6 is in the ten thousands place"], "60,000"), example("Compare 98,750 and 102,300", ["5 digits vs 6 digits"], "98,750 &lt; 102,300")],
        [['The digit instead of its value', 'The value of 6 in 361,042 is 60,000, not 6.'], ['Leaving out a zero', 'Three hundred five thousand is 305,000.'], ['Comparing first digits of different lengths', 'Count the digits first.']])
    faq = [('What does MATATAG Math 4 ask about numbers?', 'Read and write numbers up to 1 000 000 in numerals and in words, determine the place value and value of a digit, and compare numbers up to 1 000 000 using =, < and >.'), ('What is the largest 6-digit number?', '999,999.'), ('Why do we use commas?', 'They split a number into groups of three digits so it is easy to read.'), ('What comes after 999,999?', '1,000,000, one million.')]
    make('numbers-up-to-1000000', 4, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Read and write numbers up to 1 000 000 in numerals and in words; determine the place value of a digit in a 6-digit number, the value of a digit, and the digit of number, given its place value; compare numbers up to 1 000 000 using =, < and >.',
         'Numbers up to 1,000,000: Place Value, Reading, Writing and Comparing', 'Numbers up to 1,000,000',
         'Free Grade 4 place value worksheets for the DepEd MATATAG curriculum: read, write and compare numbers up to 1,000,000, place value and value of digits, words and expanded form. 100 questions with answers.',
         'Value = digit × place.', 'Compare: count the digits, then compare from the left.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
