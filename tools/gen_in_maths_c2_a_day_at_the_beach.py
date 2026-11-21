# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 1: A Day at the Beach (Counting in Groups)
Counting in 2s, 3s, 5s and 10s, missing numbers in skip-counting rows and group stories up to 100 (UK Year 2 and AU Year 2 set makers)."""
from in_prim import unit, mod, rn
uk = mod("gen_uk_maths_y2_counting", 602011)
tw = mod("gen_au_maths_y2_twos", 602012)
unit(2, "a-day-at-the-beach", 1, "N", 1, "A Day at the Beach", "Counting in Groups", "counting in groups",
     "Counting in groups: skip counting in 2s, 3s, 5s and 10s, and counting objects arranged in groups up to 100 (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 A Day at the Beach worksheet (Joyful Mathematics Chapter 1): counting in 2s, 3s, 5s and 10s, missing numbers and group stories. 100 questions with answers.",
     "Count in groups: 5, 10, 15, 20 …", "Counting in groups is quicker than counting one by one.",
     "<ul><li>Count shells in <b>2s</b>: 2, 4, 6, 8 ….</li><li>Count fingers in <b>5s</b>: 5, 10, 15 …; count bundles in <b>10s</b>: 10, 20, 30 ….</li></ul>",
     [("How many legs do 6 birds have? Count in 2s.", ["2, 4, 6, 8, 10, 12"], "12")],
     [["Counting each object one by one", "Make groups of 2, 5 or 10 and skip count."], ["Skipping a group", "Touch each group as you say its number."]],
     [("Why count in groups?", "It is faster and fewer mistakes are made when there are many things."), ("Which groups should Class 2 children count in?", "2s, 3s, 5s and 10s up to 100.")],
     [("Count in 2s", [rn(tw, "set_count", 12), rn(uk, "set_twos_fives", 8)]),
      ("Count in 5s and 10s", [rn(uk, "set_twos_fives", 8), rn(uk, "set_tens", 12)]),
      ("Count in 3s", [rn(uk, "set_threes", 20)]),
      ("Missing numbers", [rn(uk, "set_missing", 20)]),
      ("Group stories", [rn(uk, "set_stories", 20)])], 60201, max_num=100)
