# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 1: Finding the Furry Cat! (Pre-number Concepts)
Position words (on, under, inside, near, far, left, right), more and fewer, and sorting (AU Foundation and UK Year 1 set makers)."""
from in_prim import unit, mod, rn
p = mod("gen_au_maths_f_position", 601011)
c = mod("gen_au_maths_f_counting_and_comparing", 601012)
so = mod("gen_au_maths_f_sorting_and_data", 601013)
uk = mod("gen_uk_maths_y1_position", 601014)
unit(1, "finding-the-furry-cat", 1, "G", 1, "Finding the Furry Cat!", "Position, More and Fewer, and Sorting", "position and sorting",
     "Pre-number concepts: describing position (top, bottom, inside, outside, near, far, left, right), comparing groups (more, fewer, same) and sorting objects (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Finding the Furry Cat worksheet (Joyful Mathematics Chapter 1): position words, left and right, more and fewer, and sorting. 100 picture questions with answers.",
     "Where is it? On, under, inside, next to.", "Compare groups: more, fewer or the same.",
     "<ul><li>Position words tell where things are: <b>on</b>, <b>under</b>, <b>inside</b>, <b>next to</b>, <b>behind</b>.</li><li>Your <b>left</b> hand and <b>right</b> hand help you tell left from right.</li><li>Match things one to one to see which group has <b>more</b>.</li></ul>",
     [("The cat is under the table. Where is the table?", ["The table is above the cat"], "Over the cat")],
     [["Mixing up left and right", "Hold up your right hand: right is that side."], ["Saying the group of bigger things has more", "Count or match them: more means a bigger number."]],
     [("What are pre-number concepts?", "Ideas children need before counting well: position, size, more and fewer, and sorting."), ("How can I practise left and right?", "Play games like 'Touch your left ear' and talk about where things are in the room.")],
     [("Where is it?", [rn(p, "set_table", 10), rn(p, "set_box", 10)]),
      ("In a line", [rn(p, "set_shelf", 10), rn(p, "set_line", 10)]),
      ("Left and right", [rn(uk, "set_left_right", 12), rn(uk, "set_position", 8)]),
      ("More and fewer", [rn(c, "set_most", 10), rn(c, "set_rows", 10)]),
      ("Sorting", [rn(so, "set_rules", 12), rn(p, "set_words", 8)])], 60101)
