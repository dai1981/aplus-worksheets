# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Probability: Tree Diagrams and Combined Events
  python3 tools/gen_uk_maths_y10_probability_tree_diagrams.py
Runs the question makers of gen_sg_maths_s4_probability_of_combined_events with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s4_probability_of_combined_events', 91017, 10, 'probability-tree-diagrams', 17, 'P',
         'Calculate the probability of independent and dependent combined events, using tree diagrams and other representations.',
         'Probability: Tree Diagrams and Combined Events', 'Probability tree diagrams',
         meta='Free Year 10 GCSE maths worksheets on sample space diagrams, tree diagrams and independent and dependent events. 100 questions with answers.',
         rep=[])
