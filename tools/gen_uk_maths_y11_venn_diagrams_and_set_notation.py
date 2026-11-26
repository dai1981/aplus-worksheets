# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Venn Diagrams and Set Notation
  python3 tools/gen_uk_maths_y11_venn_diagrams_and_set_notation.py
Runs the question makers of gen_sg_maths_s4_sets_and_venn_diagrams with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s4_sets_and_venn_diagrams', 91111, 11, 'venn-diagrams-and-set-notation', 11, 'P',
         'Enumerate sets and combinations of sets systematically, using tables, grids, Venn diagrams and set notation; calculate probabilities from Venn diagrams.',
         'Venn Diagrams and Set Notation', 'Venn diagrams',
         meta='Free Year 11 GCSE maths worksheets on set notation, union, intersection and complement, and Venn diagram problems. 100 questions with answers.',
         rep=[])
