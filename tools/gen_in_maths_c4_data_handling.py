# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 14: Data Handling (Tables, Pictographs and Bar Graphs)
Tally tables, pictographs and bar graphs: reading, comparing and answering questions (UK Year 4, BC Grade 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y4_statistics", 604140)
bc = mod("gen_cabc_math_g4_graphs", 604141)
au = mod("gen_au_maths_y4_data", 604142)
unit(4, "data-handling", 14, "D", 14, "Data Handling", "Tables, Pictographs and Bar Graphs", "data handling",
     "Data handling: collecting data, recording in tables, drawing and reading pictographs and bar graphs, and drawing conclusions (summary of NCERT Maths Mela Class 4)",
     "Class 4 Data Handling worksheet (Maths Mela Chapter 14): tally tables, pictographs, bar graphs and comparing. 100 questions with answers.",
     "Read the scale on a bar graph carefully.", "In a pictograph, use the key.",
     "<ul><li>A <b>bar graph</b> shows amounts as bars; read across from the top of the bar to the scale.</li><li>A <b>pictograph</b> key tells what each picture stands for.</li></ul>",
     [('Bar for cricket reaches 35; for football 20.', ['35 − 20'], '15 more chose cricket')],
     [['Reading the bar between marks wrongly', 'Find what each step on the scale is worth.'], ['Ignoring the key', 'Multiply the pictures by the key.']],
     [('What is a bar graph?', 'A graph that uses bars of different lengths to show amounts.'), ('Why use a key?', 'One picture can stand for many, so big numbers fit.')],
     [('Tally tables', [rn(uk, "set_tally_table", 10), rn(au, "set_tally", 10)]),
      ('Pictographs', [rn(uk, "set_pictogram", 10), rn(bc, "set_pictograph", 10)]),
      ('Bar graphs', [rn(uk, "set_bar", 10), rn(bc, "set_bar", 10)]),
      ('Compare', [rn(bc, "set_compare", 10), rn(au, "set_compare", 10)]),
      ('Data questions', [rn(uk, "set_words", 8), rn(bc, "set_words", 5), rn(au, "set_words", 7)])], 60414)
