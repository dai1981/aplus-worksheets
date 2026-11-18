# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Halves and Fourths: Equal Parts (TEKS 1.6G, 1.6H)
  python3 tools/gen_ustx_math_g1_halves_fourths.py
Halves, fourths, equal or not equal shares, which part is shaded, and sharing stories (the US Grade 1 makers).
Wrong answers come from real mistakes: calling unequal parts halves, counting parts that are not the same size, and
thinking more parts means bigger parts.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_halves_fourths as hf
adopt(hf)
tx_common.GRADE = "grade-1"



def resolved(fn):
    """Picture-answer items are built later with build(pos); build them now at a random position."""
    def f(rnd):
        st = fn(rnd)
        st["items"] = [it["build"](rnd.randrange(4)) if "build" in it else it for it in st["items"]]
        return st
    f.__name__ = fn.__name__
    return f


def build():
    sets, R = build_sets([
        ("Halves", [("run", resolved(hf.set_halves), ("rnd",), 20)]),
        ("Fourths and quarters", [("run", resolved(hf.set_fourths), ("rnd",), 20)]),
        ("Equal or not equal shares?", [("run", resolved(hf.set_equal), ("rnd",), 20)]),
        ("What part is shaded?", [("run", resolved(hf.set_shaded), ("rnd",), 20)]),
        ("Bigger or smaller? Sharing stories", [("run", resolved(hf.set_stories), ("rnd",), 20)]),
    ], 69116)
    finish(sets, R)
    body = lesson('<ul><li><b>Halves</b>: 2 equal parts. Each part is one half.</li><li><b>Fourths</b> (quarters): 4 equal parts. Each part is one fourth.</li><li>The parts must be the <b>same size</b>.</li><li>More equal parts means smaller parts: a fourth is smaller than a half.</li></ul>',
        [example("A pizza cut into 4 equal parts", ["4 equal parts"], "fourths")],
        [['Calling unequal parts halves', 'Halves must be the same size.'], ['Counting parts that are not equal', 'Check that each part is the same size.'], ['Thinking a fourth is bigger than a half', 'More parts means smaller parts.']])
    faq = [('What does TEKS 1.6G ask?', 'Partition two-dimensional figures into two and four fair shares or equal parts and describe the parts using words.'), ('What does TEKS 1.6H ask?', 'Identify examples and non-examples of halves and fourths.'), ('Is a quarter the same as a fourth?', 'Yes.'), ('Which is bigger, a half or a fourth of the same pizza?', 'A half.')]
    make('halves-and-fourths', 16, 'Geometry and Measurement', '1.6G, 1.6H',
         '1.6G partition two-dimensional figures into two and four fair shares or equal parts and describe the parts using words; 1.6H identify examples and non-examples of halves and fourths',
         'Halves and Fourths: Equal Parts', 'Halves and Fourths',
         'Free Grade 1 halves and fourths worksheets for Texas TEKS 1.6G and 1.6H: equal parts, examples and non-examples, shaded parts and sharing stories. 100 questions with answers.',
         'Halves are 2 equal parts; fourths are 4 equal parts.', 'A fourth is smaller than a half.',
         body, faq, sets, seo_title='Grade 1 Halves and Fourths Worksheets (TEKS 1.6G)')


if __name__ == "__main__":
    build()
