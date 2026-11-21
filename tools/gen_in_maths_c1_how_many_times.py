# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 11: How Many Times? (Multiplication)
Equal groups, adding the same number again, skip counting in 2s, 5s and 10s, arrays (SG Primary 1, AU Year 1 and UK Year 1 set makers)."""
from in_prim import unit, mod, rn
sg = mod("gen_sg_maths_p1_mult_div", 601111)
au = mod("gen_au_maths_y1_sharing_grouping", 601112)
uk = mod("gen_uk_maths_y1_counting_in_steps", 601113)
unit(1, "how-many-times", 11, "N", 11, "How Many Times?", "Equal Groups and Early Multiplication", "how many times",
     "Early multiplication: making equal groups, repeated addition, skip counting and arranging objects in rows (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 How Many Times? worksheet (Joyful Mathematics Chapter 11): equal groups, adding the same number again, skip counting and arrays. 100 picture questions with answers.",
     "3 groups of 2 is 2 + 2 + 2 = 6.", "Skip count to add equal groups quickly.",
     "<ul><li><b>Equal groups</b> have the same number in each group.</li><li>3 groups of 4 = 4 + 4 + 4 = 12.</li><li>Skip count: 2, 4, 6, 8 … or 5, 10, 15 ….</li></ul>",
     [("How many legs do 4 birds have?", ["2 + 2 + 2 + 2"], "8")],
     [["Counting the groups instead of the things", "Count everything, or add the group size again and again."], ["Groups that are not equal", "Each group must have the same number."]],
     [("Do Class 1 children learn times tables?", "Not yet: they make equal groups and add the same number again."), ("What is skip counting?", "Counting in jumps, such as 5, 10, 15, 20.")],
     [("Equal groups", [rn(sg, "set_groups", 12), rn(au, "set_equal", 8)]),
      ("Add the same number", [rn(sg, "set_repeated", 20)]),
      ("Rows and arrays", [rn(sg, "set_arrays", 20)]),
      ("Skip counting", [rn(uk, "set_twos", 7), rn(uk, "set_fives", 7), rn(uk, "set_tens", 6)]),
      ("Group stories", [rn(au, "set_total", 10), rn(uk, "set_groups", 10)])], 60111)
