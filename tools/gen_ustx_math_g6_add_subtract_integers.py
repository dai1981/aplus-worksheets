# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Adding and Subtracting Integers (TEKS 6.3C, 6.3D)
  python3 tools/gen_ustx_math_g6_add_subtract_integers.py
Number line models and zero pairs, adding integers, subtracting by adding the opposite, mixed practice, and word
problems with temperature, elevation and money (the US makers with a new seed, plus own mixed practice).
Wrong answers come from real mistakes: adding the absolute values when the signs differ, keeping the wrong sign,
and subtracting a negative as if it were positive.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_add_subtract_integers as asi
adopt(asi)
asi.R = random.Random(66003)
from ws_common import num, par
tx_common.GRADE = "grade-6"

def one_mixed(r):
    a, b = r.randint(-25, 25), r.randint(-25, 25)
    if 0 in (a, b) or abs(a) == abs(b):
        return None
    op = r.choice(["+", "−"])
    v = a + b if op == "+" else a - b
    w = [a - b if op == "+" else a + b, -v, abs(a) + abs(b) if abs(a) + abs(b) != abs(v) else -(abs(a) + abs(b))]
    w = [num(x) for x in dict.fromkeys(w) if x != v]
    how = ("Add the opposite: %s + %s = <b>%s</b>." % (num(a), par(-b), num(v))) if op == "−" else "<b>%s</b>." % num(v)
    return mcq("Find %s %s %s." % (num(a), op, par(b)), num(v), w, how, allow_zero=True)


def build():
    sets, R = build_sets([
        ("Number lines, opposites and zero pairs", [("run", asi.set_number_line, (), 20)]),
        ("Add integers", [("run", asi.set_add, (), 20)]),
        ("Subtract integers: add the opposite", [("run", asi.set_sub, (), 20)]),
        ("Mixed practice", [("collect", one_mixed, 20)]),
        ("Word problems: temperature, elevation and money", [("run", asi.set_words, (), 20)]),
    ], 66003)
    finish(sets, R)
    body = lesson('<ul><li><b>Same signs</b>: add the absolute values and keep the sign. −4 + (−6) = −10.</li><li><b>Different signs</b>: subtract the absolute values and use the sign of the number with the greater absolute value. −9 + 4 = −5.</li><li>To <b>subtract</b>, add the opposite: 3 − (−5) = 3 + 5 = 8.</li><li>A positive and a negative counter make a <b>zero pair</b>.</li></ul>',
        [example("−9 + 4", ["Different signs: 9 − 4 = 5", "9 > 4, so use the sign of −9"], "−5"), example("−2 − (−7)", ["Add the opposite: −2 + 7"], "5")],
        [['Adding absolute values when the signs differ: −9 + 4 = −13', 'Different signs: subtract, 9 − 4 = 5, then −5.'], ['Subtracting a negative as a positive: 3 − (−5) = −2', 'Add the opposite: 3 + 5 = 8.'], ['Keeping the wrong sign', 'Use the sign of the number with the greater absolute value.']])
    faq = [('What does TEKS 6.3C ask?', 'Represent integer operations with concrete models and connect the actions with the models to standardized algorithms.'), ('What does TEKS 6.3D ask?', 'Add, subtract, multiply and divide integers fluently.'), ('Why is subtracting a negative the same as adding?', 'Taking away a debt makes you richer: 3 − (−5) = 3 + 5.'), ('What is a zero pair?', 'A positive 1 and a negative 1 together. Their sum is 0.')]
    make('adding-and-subtracting-integers', 3, 'Number and Operations', '6.3C, 6.3D',
         '6.3C represent integer operations with concrete models and connect the actions with the models to standardized algorithms; 6.3D add, subtract, multiply, and divide integers fluently',
         'Adding and Subtracting Integers', 'Adding and Subtracting Integers',
         'Free Grade 6 worksheets for Texas TEKS 6.3C and 6.3D: add and subtract integers with number lines and zero pairs, subtract by adding the opposite, mixed practice and word problems. 100 questions with answers.',
         'Same signs: add. Different signs: subtract. To subtract, add the opposite.', '−9 + 4 = −5. 3 − (−5) = 3 + 5 = 8.',
         body, faq, sets, seo_title='Grade 6 Adding and Subtracting Integers Worksheets (TEKS 6.3C, 6.3D, STAAR)')


if __name__ == "__main__":
    build()
