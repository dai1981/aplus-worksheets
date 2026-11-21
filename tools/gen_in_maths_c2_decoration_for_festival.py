# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 6: Decoration for Festival (Addition and Subtraction)
Adding and subtracting 2-digit numbers with and without regrouping, missing numbers and word problems (UK Year 2, US Grade 2 and AU Year 2 set makers)."""
from in_prim import unit, mod, rn
uk = mod("gen_uk_maths_y2_add_sub", 602061)
us = mod("gen_us_math_g2_add_sub_100", 602062)
au = mod("gen_au_maths_y2_add_sub", 602063)
unit(2, "decoration-for-festival", 6, "N", 6, "Decoration for Festival", "Addition and Subtraction of 2-Digit Numbers", "add and subtract",
     "Addition and subtraction of 2-digit numbers with and without regrouping, using objects, number lines and stories (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Decoration for Festival worksheet (Joyful Mathematics Chapter 6): adding and subtracting 2-digit numbers, regrouping, missing numbers and word problems. 100 questions with answers.",
     "Add the tens, then the ones.", "If the ones make 10 or more, regroup into a ten.",
     "<ul><li>34 + 25: tens 30 + 20 = 50, ones 4 + 5 = 9, so 59.</li><li>38 + 25: ones 8 + 5 = 13 = 1 ten 3 ones, so 63.</li><li>52 − 27: take 20, then 7: 52 → 32 → 25.</li></ul>",
     [("46 + 37", ["40 + 30 = 70", "6 + 7 = 13", "70 + 13"], "83"), ("61 − 24", ["61 − 20 = 41", "41 − 4"], "37")],
     [["Forgetting the regrouped ten", "Write the extra ten and add it to the tens."], ["Taking the smaller ones digit from the bigger", "52 − 27: 2 − 7 needs a ten to be broken."]],
     [("What is regrouping?", "Changing 10 ones into 1 ten (or 1 ten into 10 ones) when adding or subtracting."), ("Up to which numbers do Class 2 children add?", "Sums up to 100.")],
     [("Add ones and tens", [rn(uk, "set_ones", 10), rn(uk, "set_tens", 10)]),
      ("Add two 2-digit numbers", [rn(uk, "set_two", 10), rn(us, "set_add", 10)]),
      ("Subtract", [rn(us, "set_sub", 10), rn(au, "set_jump", 10)]),
      ("Missing numbers", [rn(us, "set_missing", 20)]),
      ("Festival stories", [rn(uk, "set_words", 12), rn(au, "set_words", 8)])], 60206, max_num=100)
