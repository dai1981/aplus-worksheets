# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 8: Grouping and Sharing (Multiplication and Division)
Equal groups, arrays, sharing and grouping, multiplication and division sentences and stories (UK Year 2 and SG Primary 2 set makers)."""
from in_prim import unit, mod, rn
uk = mod("gen_uk_maths_y2_mult_div", 602081)
sg = mod("gen_sg_maths_p2_mult_div", 602082)
unit(2, "grouping-and-sharing", 8, "N", 8, "Grouping and Sharing", "Multiplication and Division", "grouping and sharing",
     "Multiplication as repeated addition and equal groups; division as equal sharing and grouping; using arrays and stories (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Grouping and Sharing worksheet (Joyful Mathematics Chapter 8): equal groups, arrays, sharing and grouping, multiplication and division stories. 100 questions with answers.",
     "4 groups of 3 = 3 + 3 + 3 + 3 = 4 × 3 = 12.", "Share 12 equally among 3: each gets 4.",
     "<ul><li><b>Multiply</b> to find the total of equal groups: 5 groups of 2 = 5 × 2 = 10.</li><li><b>Divide</b> to share equally or to make groups: 15 ÷ 5 = 3.</li></ul>",
     [("3 plates with 4 laddoos each. How many laddoos?", ["4 + 4 + 4"], "12"), ("Share 10 bananas among 2 children.", ["10 ÷ 2"], "5 each")],
     [["Adding the number of groups and the group size", "3 groups of 4 is 4 + 4 + 4, not 3 + 4."], ["Unequal sharing", "In division every share is the same."]],
     [("What is multiplication?", "A quick way to add equal groups."), ("What is division?", "Sharing equally, or finding how many equal groups can be made.")],
     [("Equal groups", [rn(uk, "set_groups", 14), rn(sg, "set_grouping", 6)]),
      ("Arrays", [rn(uk, "set_arrays", 20)]),
      ("Sharing and grouping", [rn(uk, "set_share_group", 10), rn(sg, "set_sharing", 10)]),
      ("Number sentences", [rn(uk, "set_statements", 14), rn(sg, "set_facts", 6)]),
      ("Stories", [rn(uk, "set_story", 10), rn(sg, "set_story", 10)])], 60208)
