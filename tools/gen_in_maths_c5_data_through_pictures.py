# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 15: Data Through Pictures (Pictographs, Bar Graphs and Line Graphs)
Reading tables, double bar graphs and line graphs, comparing and drawing conclusions (UK Year 5, BC Grade 5 and AU Year 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_line_graphs_tables", 605150)
bc = mod("gen_cabc_math_g5_double_bar_graphs", 605151)
au = mod("gen_au_maths_y5_line_graphs", 605152)
unit(5, "data-through-pictures", 15, "D", 15, "Data Through Pictures", "Pictographs, Bar Graphs and Line Graphs", "data through pictures",
     "Data handling: collecting and representing data in tables, pictographs and bar graphs, reading line graphs, and interpreting data (summary of NCERT Maths Mela Class 5)",
     "Class 5 Data Through Pictures worksheet (Maths Mela Chapter 15): tables, bar graphs, double bar graphs, line graphs and conclusions. 100 questions with answers.",
     "Read the title, axes and scale first.", "Line graphs show change over time.",
     "<ul><li>A <b>bar graph</b> compares amounts; a <b>double bar graph</b> compares two sets side by side.</li><li>A <b>line graph</b> shows how something changes over time.</li></ul>",
     [('The line rises from 20 to 35 between May and June.', ['35 − 20'], 'It rose by 15')],
     [['Reading between grid lines wrongly', 'Work out what each grid step is worth.'], ['Mixing up the two bars', 'Check the key for each colour.']],
     [('When is a line graph used?', 'To show how something changes over time, like temperature through a day.'), ('What is a double bar graph?', 'A bar graph comparing two groups for each category.')],
     [('Read a table', [rn(uk, "set_tables", 14), rn(uk, "set_timetables", 6)]),
      ('Double bar graphs', [rn(bc, "set_read", 20)]),
      ('Read a line graph', [rn(uk, "set_read", 10), rn(au, "set_read", 10)]),
      ('Changes over time', [rn(au, "set_change", 14), rn(au, "set_two", 6)]),
      ('What does the data say?', [rn(au, "set_words", 12), rn(bc, "set_concl", 4), rn(au, "set_mode", 4)])], 60515)
