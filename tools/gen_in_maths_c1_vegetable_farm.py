# -*- coding: utf-8 -*-
"""
India Class 1 Maths, Joyful Mathematics Chapter 6: Vegetable Farm (Addition and Subtraction up to 20)
  python3 tools/gen_in_maths_c1_vegetable_farm.py
Adding with pictures, making 10, doubles, taking away within 20 and number stories (Singapore Primary 1, US Grade 1 and
Ontario Grade 1 set makers, with Indian names).
"""
from in_prim import unit, mod, rn

sga = mod("gen_sg_maths_p1_add_sub_20", 601061)
usa = mod("gen_us_math_g1_add_sub_20", 601062)

unit(1, "vegetable-farm", 6, "N", 6, "Vegetable Farm", "Addition and Subtraction up to 20", "add and subtract to 20",
     "Addition and subtraction of numbers up to 20 using objects, pictures and number stories (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Vegetable Farm worksheet (Joyful Mathematics Chapter 6): adding and subtracting up to 20 with pictures, making 10, doubles and number stories. 100 questions with answers.",
     "Count on to add. Count back to take away.", "9 + 4: 9 + 1 = 10, then 3 more is 13.",
     "<ul><li>To add, start at the bigger number and count on: 8 + 3 → 9, 10, 11.</li><li>Make 10 first: 9 + 5 = 10 + 4 = 14.</li><li>To take away, count back: 15 − 3 → 14, 13, 12.</li></ul>",
     [("8 + 5", ["8 + 2 = 10", "10 + 3"], "13"), ("16 − 4", ["Count back 4: 15, 14, 13, 12"], "12")],
     [["Counting the first number again", "Start counting at the next number."], ["Adding when the story says 'gave away'", "Gave away, ate or lost means take away."]],
     [("How do I add on my fingers past 10?", "Make 10 first, then add what is left."), ("What is a double?", "A number added to itself, like 6 + 6 = 12."),
      ("How do I take away?", "Count back from the bigger number, or think of the addition fact: 12 − 5 = 7 because 7 + 5 = 12.")],
     [("Add with pictures", [rn(sga, "set_add_pictures", 20)]),
      ("Make 10 to add", [rn(usa, "set_make10", 20)]),
      ("Doubles", [rn(usa, "set_doubles", 20)]),
      ("Take away", [rn(sga, "set_take_away", 10), rn(usa, "set_sub20", 10)]),
      ("Number stories", [rn(usa, "set_sub10", 10), rn(usa, "set_add10", 10)])], 60106)
