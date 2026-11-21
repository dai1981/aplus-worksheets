# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 11: Data Handling
Tally marks, pictographs with a key, tables, comparing and totals (UK Year 2 and SG Primary 2 set makers)."""
from in_prim import unit, mod, rn
uk = mod("gen_uk_maths_y2_statistics", 602111)
sg = mod("gen_sg_maths_p2_picture_graphs", 602112)
unit(2, "data-handling", 11, "D", 11, "Data Handling", "Tally Marks, Pictographs and Tables", "data handling",
     "Data handling: collecting data, recording with tally marks, and reading and drawing simple pictographs and tables (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Data Handling worksheet (Joyful Mathematics Chapter 11): tally marks, pictographs with a key, tables, most and fewest, totals. 100 questions with answers.",
     "Use the key: one picture may stand for 2 or more.", "Tally marks are grouped in fives.",
     "<ul><li>Tally marks: |||| with a line across = 5.</li><li>In a pictograph, read the <b>key</b>: if one picture = 2, then 4 pictures = 8.</li></ul>",
     [("Key: one star = 2 children. Mangoes has 5 stars.", ["5 × 2"], "10 children")],
     [["Counting pictures without using the key", "Multiply by what each picture stands for."], ["Reading the wrong row", "Put your finger on the row's name first."]],
     [("What is a pictograph?", "A chart that uses pictures to show data, with a key saying how much each picture stands for."), ("What are tally marks?", "Marks drawn in groups of five to count.")],
     [("Tally marks", [rn(uk, "set_tally", 20)]),
      ("Pictographs", [rn(uk, "set_pic1", 10), rn(sg, "set_one", 10)]),
      ("Pictographs with a key", [rn(uk, "set_pic_key", 10), rn(sg, "set_scales", 10)]),
      ("Tables", [rn(uk, "set_block_table", 20)]),
      ("Compare and total", [rn(sg, "set_compare", 10), rn(sg, "set_totals", 10)])], 60211)
