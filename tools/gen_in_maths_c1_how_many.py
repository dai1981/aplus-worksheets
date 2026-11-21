# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 5: How Many? (Addition and Subtraction of Single Digit Numbers)
Putting together and taking away with pictures, number lines and stories, facts to 10 (AU Foundation and Ontario Grade 1 set makers)."""
from in_prim import unit, mod, rn
at = mod("gen_au_maths_f_adding_and_taking_away", 601051)
fa = mod("gen_caon_math_g1_facts_10", 601052)
unit(1, "how-many", 5, "N", 5, "How Many?", "Adding and Taking Away Single-Digit Numbers", "add and take away",
     "Addition and subtraction of single-digit numbers: putting together, taking away, using objects, pictures and number lines (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 How Many? worksheet (Joyful Mathematics Chapter 5): adding and taking away single-digit numbers with pictures, number lines and stories. 100 questions with answers.",
     "Put together to add. Take away to subtract.", "4 + 3 = 7 and 7 − 3 = 4.",
     "<ul><li><b>Add</b>: put groups together and count all, or count on: 5 + 3 → 6, 7, 8.</li><li><b>Subtract</b>: take some away and count what is left: 7 − 2 = 5.</li></ul>",
     [("3 + 4", ["Count on from 4: 5, 6, 7"], "7"), ("9 − 3", ["Count back 3: 8, 7, 6"], "6")],
     [["Counting the starting number again", "Count on from the next number."], ["Adding when things are taken away", "'Ate', 'gave away', 'flew away' mean subtract."]],
     [("What are single-digit numbers?", "The numbers 0 to 9."), ("How can I help my child add?", "Use real things like spoons or beads and say the number sentence together.")],
     [("Put together", [rn(at, "set_join", 20)]),
      ("Take away", [rn(at, "set_take", 20)]),
      ("On the number line", [rn(at, "set_line", 20)]),
      ("Add or subtract?", [rn(at, "set_which", 10), rn(fa, "set_add", 10)]),
      ("Number stories", [rn(at, "set_story", 10), rn(fa, "set_subtract", 10)])], 60105, max_num=18)
