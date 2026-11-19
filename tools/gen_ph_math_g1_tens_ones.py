# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Tens and Ones: Place Value of 2-Digit Numbers (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_tens_ones.py
Counting tens and ones with blocks, the place value and value of a digit, the digit in a given place, and breaking a
2-digit number into tens and ones (Australia Year 1, US Grade 1 and Texas Grade 1 makers).
Wrong answers come from real mistakes: reading 4 tens 7 ones as 74, saying the value of the 3 in 35 is 3, and
mixing up the tens and ones places.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y1_tens_ones as aut
adopt(aut)
if hasattr(aut, 'R'): aut.R = random.Random(701130)
import gen_us_math_g1_place_value as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(701131)
import gen_ustx_math_g1_tens_and_ones as txt
adopt(txt)
if hasattr(txt, 'R'): txt.R = random.Random(701132)
ph_common.GRADE = "grade-1"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"])
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "")) for x in _re.findall(r"\d[\d,]*", t)]


def le100(it):
    return all(n <= 100 for n in _nums(it))


def le20(it):
    return all(n <= 20 for n in _nums(it))



def build():
    sets, R = build_sets([
        ("Count tens and ones", [("run", usp.set_blocks, ("rnd", "seen"), 20, le100)]),
        ("Place value of a digit", [("run", aut.set_digits, ("rnd", "seen"), 10, le100), ("run", usp.set_digits, ("rnd", "seen"), 10, le100)]),
        ("Tens and ones in numbers", [("collect", txt.one_blocks, 20)]),
        ("Break a number into tens and ones", [("collect", txt.one_expand, 10), ("run", aut.set_partition, ("rnd", "seen"), 10, le100)]),
        ("Tens and ones stories", [("collect", txt.one_story, 10), ("collect", txt.one_missing, 10)]),
    ], 70113)
    finish(sets, R)
    body = lesson('<ul><li>A 2-digit number has a <b>tens</b> digit and a <b>ones</b> digit. In 47, 4 is in the tens place and 7 is in the ones place.</li><li>The <b>value</b> of the 4 in 47 is 40, because it means 4 tens.</li><li>47 = 40 + 7 = 4 tens and 7 ones.</li><li>10 ones make 1 ten.</li></ul>',
        [example("63", ["6 tens = 60", "3 ones = 3"], "60 + 3")],
        [['4 tens 7 ones as 74', 'Write the tens first: 47.'], ['Value of 3 in 35', 'It is 30, not 3.'], ['Tens or ones?', 'The left digit is the tens.']])
    faq = [('What does MATATAG Math 1 ask about place value?', 'Determine the place value of a digit in a 2-digit number, the value of a digit, and the digit of a number given its place value, and decompose any 2-digit number into tens and ones.'), ('What is the value of 0 in 50?', '0.'), ('How many tens are in 90?', '9 tens.'), ('Why use bundles of 10 sticks?', 'Children see that 10 ones make 1 ten.')]
    make('tens-and-ones', 13, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Determine a. the place value of a digit in a 2-digit number, b. the value of a digit, and c. the digit of a number, given its place value; decompose any 2-digit number into tens and ones.',
         'Tens and Ones: Place Value of 2-Digit Numbers', 'Tens and Ones',
         'Free Grade 1 tens and ones worksheets for the DepEd MATATAG curriculum: place value, the value of a digit, and breaking 2-digit numbers into tens and ones. 100 questions with pictures and answers.',
         '47 = 4 tens and 7 ones = 40 + 7.', 'The value of a digit depends on its place.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
