# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 13: So Many Toys (Data Handling)
Sorting, tally marks and picture graphs: counting, most and fewest, how many more, totals."""
from in_prim import unit, mod, rn
pg = mod("gen_sg_maths_p1_picture_graphs", 601131)
ad = mod("gen_au_maths_y1_data", 601132)
ud = mod("gen_us_math_g1_data", 601133)
unit(1, "so-many-toys", 13, "D", 13, "So Many Toys", "Sorting, Tally Marks and Picture Graphs", "data handling",
     "Data handling: collecting, sorting and counting objects, recording with tally marks and pictures, and answering questions from them (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 So Many Toys worksheet (Joyful Mathematics Chapter 13): sorting, tally marks and picture graphs, most and fewest, how many more. 100 picture questions with answers.",
     "Sort, count, then compare.", "Each picture or tally stands for one.",
     "<ul><li><b>Sort</b> things into groups, then count each group.</li><li><b>Tally marks</b> are drawn in fives: |||| with a line across is 5.</li><li>A <b>picture graph</b> shows how many with pictures.</li></ul>",
     [("Balls: 6, cars: 4. How many more balls than cars?", ["6 − 4"], "2")],
     [["Counting a tally group of 5 as 4", "The line across is the fifth mark."], ["Adding when asked 'how many more'", "'How many more' means find the difference."]],
     [("What is data handling in Class 1?", "Sorting, counting and showing things with tallies and pictures."), ("Why use tally marks?", "Groups of five are quick to count.")],
     [("Sort and count", [rn(ad, "set_sort", 10), rn(ud, "set_sort", 10)]),
      ("Tally marks", [rn(ad, "set_tally", 20)]),
      ("Read a picture graph", [rn(pg, "set_count", 20)]),
      ("Most and fewest", [rn(pg, "set_most", 20)]),
      ("How many more?", [rn(pg, "set_more", 10), rn(pg, "set_total", 10)])], 60113)
