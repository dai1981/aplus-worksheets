# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Measurement Conversions within a System (TEKS 5.7A)
  python3 tools/gen_ustx_math_g5_conversions.py
Converting customary length and weight, metric units with powers of 10, capacity and time, comparing
measurements, and multi-step word problems. The question makers come from the US Grade 5 conversion unit with
Texas names.
Wrong answers come from real mistakes: dividing when converting to a smaller unit, using 10 for customary units,
and comparing numbers without matching the units.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_conversions as usc
adopt(usc)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Customary length and weight", [("run", usc.set_customary, (), 20)]),
        ("Metric units: powers of 10", [("run", usc.set_metric, (), 20)]),
        ("Capacity and time", [("run", usc.set_capacity_time, (), 20)]),
        ("Compare and order measurements", [("run", usc.set_compare, (), 20)]),
        ("Multi-step word problems", [("run", usc.set_story, ("rnd",), 20)]),
    ], 65019)
    finish(sets, R)
    body = lesson('<ul><li>Larger unit to smaller unit: <b>multiply</b>. Smaller unit to larger unit: <b>divide</b>.</li><li>Metric units change by powers of 10: 1 km = 1,000 m, 1 m = 100 cm, 1 L = 1,000 mL, 1 kg = 1,000 g.</li><li>Customary: 12 in. = 1 ft, 3 ft = 1 yd, 5,280 ft = 1 mi, 16 oz = 1 lb, 2 c = 1 pt, 2 pt = 1 qt, 4 qt = 1 gal.</li><li>Change to the same unit before you compare.</li></ul>',
        [example("3.5 km = ? m", ["1 km = 1,000 m", "3.5 × 1,000"], "3,500 m"), example("54 in. = ? ft", ["54 ÷ 12 = 4 R6"], "4 1/2 ft")],
        [['Dividing when changing to a smaller unit', 'Smaller units mean more of them: multiply.'], ['Using 10 for customary units', 'Check the table: 12, 3, 16, 4 …'], ['Comparing 2 ft and 20 in. as 2 and 20', 'Convert to the same unit first: 24 in. &gt; 20 in.']])
    faq = [('What does TEKS 5.7A ask?', 'Solve problems by calculating conversions within a measurement system, customary or metric.'), ('Do I get a reference chart on the STAAR?', 'Yes, the Grade 5 STAAR has a reference chart, but knowing common conversions saves time.'), ('How do metric conversions work?', 'Multiply or divide by 10, 100 or 1,000 by moving the decimal point.'), ('How do I solve multi-step conversion problems?', 'Convert first, then add, subtract, multiply or divide in the same unit.')]
    make('measurement-conversions', 19, 'Geometry and Measurement', '5.7A',
         '5.7A solve problems by calculating conversions within a measurement system, customary or metric',
         'Measurement Conversions within a System', 'Measurement Conversions',
         'Free Grade 5 measurement worksheets for Texas TEKS 5.7A: customary and metric conversions, capacity and time, comparing measurements and multi-step word problems. 100 questions with answers.',
         'To a smaller unit: multiply. To a larger unit: divide.', 'Metric units use powers of 10. Change to the same unit before comparing.',
         body, faq, sets, seo_title='Grade 5 Measurement Conversions Worksheets (TEKS 5.7A, STAAR)')


if __name__ == "__main__":
    build()
