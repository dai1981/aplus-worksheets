# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Addition and Subtraction Facts to 20 (TEKS 1.3D)
  python3 tools/gen_ustx_math_g1_facts.py
Adding and subtracting within 10, doubles and near doubles, making 10, and subtracting within 20 (the US Grade 1
makers with Texas names).
Wrong answers come from real mistakes: counting the start number again, adding instead of taking away, and being off by 1.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_add_sub_20 as fs
adopt(fs)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Add within 10", [("run", fs.set_add10, (fs.People,), 20)]),
        ("Subtract within 10", [("run", fs.set_sub10, (fs.People,), 20)]),
        ("Doubles and near doubles", [("run", fs.set_doubles, (fs.People,), 20)]),
        ("Make 10 to add", [("run", fs.set_make10, (fs.People,), 20)]),
        ("Subtract within 20 and word problems", [("run", fs.set_sub20, (fs.People,), 20)]),
    ], 69105)
    finish(sets, R)
    body = lesson('<ul><li><b>Count on</b> from the bigger number to add.</li><li><b>Doubles</b>: 6 + 6 = 12, so 6 + 7 is 1 more: 13.</li><li><b>Make 10</b>: 9 + 5 = 9 + 1 + 4 = 10 + 4 = 14.</li><li>To subtract, take away or think of addition: 13 − 4 = 9 because 9 + 4 = 13.</li></ul>',
        [example("8 + 5", ["8 + 2 = 10", "10 + 3"], "13")],
        [['Counting the start number again', 'Start counting at the next number.'], ['Adding instead of taking away', 'Look at the sign: − means take away.'], ['Being off by 1', 'Check with a related fact.']])
    faq = [('What does TEKS 1.3D ask?', 'Apply basic fact strategies to add and subtract within 20, including making 10 and decomposing a number leading to a 10.'), ('What is a near double?', 'A fact like 6 + 7, which is 1 more than the double 6 + 6.'), ('How does making 10 help?', 'Adding to 10 first is easy: 8 + 5 = 8 + 2 + 3 = 13.'), ('How can addition help subtraction?', '13 − 4 = ? Think 4 + ? = 13.')]
    make('addition-and-subtraction-facts-to-20', 5, 'Number and Operations', '1.3D',
         '1.3D apply basic fact strategies to add and subtract within 20, including making 10 and decomposing a number leading to a 10',
         'Addition and Subtraction Facts to 20', 'Facts to 20',
         'Free Grade 1 addition and subtraction facts worksheets for Texas TEKS 1.3D: add and subtract within 10 and 20, doubles, near doubles and making 10. 100 questions with answers.',
         'Count on, use doubles, or make 10.', '9 + 5 = 10 + 4 = 14',
         body, faq, sets, seo_title='Grade 1 Addition and Subtraction Facts to 20 Worksheets (TEKS 1.3D)')


if __name__ == "__main__":
    build()
