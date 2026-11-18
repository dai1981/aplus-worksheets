# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Addition and Subtraction Word Problems within 20 (TEKS 1.3B, 1.3F, 1.5D)
  python3 tools/gen_ustx_math_g1_word_problems.py
Joining and separating, parts and whole, comparing, unknowns in any position, and mixed problems (the US Grade 1
makers with Texas names).
Wrong answers come from real mistakes: adding when the story takes away, adding the two numbers in a compare story,
and answering with a number from the story.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_word_problems as wp
adopt(wp)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Join and separate", [("run", wp.set_result, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.JOIN)), 20)]),
        ("Parts and whole", [("run", wp.set_parts, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.PARTS)), 20)]),
        ("Compare: how many more, how many fewer", [("run", wp.set_compare, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.CMP)), 20)]),
        ("Find the missing number", [("run", wp.set_unknown, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.JOIN)), 20)]),
        ("Mixed word problems", [("run", wp.set_mixed, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.JOIN), lambda r: wp.Ctx(r, wp.PARTS), lambda r: wp.Ctx(r, wp.CMP)), 20)]),
    ], 69107)
    finish(sets, R)
    body = lesson('<ul><li>Read the story. Is something <b>joined</b>, <b>taken away</b>, or <b>compared</b>?</li><li>Join: add. Take away: subtract. How many more: subtract.</li><li>Write a number sentence with a box for the unknown: 7 + ☐ = 12.</li><li>Check: does the answer make sense in the story?</li></ul>',
        [example("Ava has 7 shells. She finds some more. Now she has 12.", ["7 + ☐ = 12"], "5 shells")],
        [['Adding when the story takes away', 'Look for words like gave away or ate.'], ['Adding in a compare story', 'How many more means subtract.'], ['Answering with a number from the story', 'Find the unknown.']])
    faq = [('What does TEKS 1.3B ask?', 'Use objects and pictorial models to solve word problems involving joining, separating, and comparing sets within 20 and unknowns as any one of the terms in the problem such as 2 + 4 = [ ]; 3 + [ ] = 7; and 5 = [ ] − 3.'), ('What does TEKS 1.3F ask?', 'Generate and solve problem situations when given a number sentence involving addition or subtraction of numbers within 20.'), ('What does TEKS 1.5D ask?', 'Represent word problems involving addition and subtraction of whole numbers up to 20 using concrete and pictorial models and number sentences.'), ('What is an unknown?', 'The number the story does not tell you.')]
    make('word-problems-within-20', 7, 'Number and Operations', '1.3B, 1.3F, 1.5D',
         '1.3B use objects and pictorial models to solve word problems involving joining, separating, and comparing sets within 20 and unknowns as any one of the terms in the problem; 1.3F generate and solve problem situations when given a number sentence involving addition or subtraction of numbers within 20; 1.5D represent word problems involving addition and subtraction of whole numbers up to 20 using concrete and pictorial models and number sentences',
         'Addition and Subtraction Word Problems within 20', 'Word Problems within 20',
         'Free Grade 1 word problem worksheets for Texas TEKS 1.3B, 1.3F and 1.5D: join, separate, compare and missing number stories within 20. 100 questions with answers.',
         'Join: add. Take away or compare: subtract.', '7 + ☐ = 12, so ☐ = 5.',
         body, faq, sets, seo_title='Grade 1 Word Problems within 20 Worksheets (TEKS 1.3B)')


if __name__ == "__main__":
    build()
