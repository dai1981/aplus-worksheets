# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Cumulative Frequency and Box Plots
  python3 tools/gen_uk_maths_y11_cumulative_frequency_and_box_plots.py
Runs the question makers of gen_sg_maths_s4_cumulative_frequency_and_box_plots with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s4_cumulative_frequency_and_box_plots', 91112, 11, 'cumulative-frequency-and-box-plots', 12, 'S',
         'Construct and interpret cumulative frequency graphs and box plots; find quartiles and the interquartile range and compare distributions.',
         'Cumulative Frequency and Box Plots', 'Cumulative frequency and box plots',
         meta='Free Year 11 GCSE maths worksheets on cumulative frequency curves, median, quartiles, interquartile range and box plots. 100 questions with answers.',
         rep=[])
