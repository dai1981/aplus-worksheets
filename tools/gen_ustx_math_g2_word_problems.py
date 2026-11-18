# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Word Problems and Number Sentences (TEKS 2.4D, 2.7C)
  python3 tools/gen_ustx_math_g2_word_problems.py
Finding the result, finding a part, and finding the start in addition and subtraction stories (the US Grade 2
makers with Texas names), and matching number sentences to stories (own maker).
Wrong answers come from real mistakes: adding when you should subtract, using the wrong numbers, and mixing up the
whole and the parts.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_word_problems as wp
adopt(wp)
tx_common.GRADE = "grade-2"

THINGS = ["stickers", "marbles", "crayons", "shells", "cards", "pecans", "books", "rocks"]


def one_sentence(r):
    k = Kid(r).next()
    t = r.choice(THINGS)
    a, b = r.randint(12, 80), r.randint(5, 60)
    kind = r.choice(["more", "gave", "start", "compare"])
    if kind == "more":
        q = "%s has %d %s. %s gets %d more. Which number sentence shows how many %s has now?" % (k["n"], a, t, k["He"], b, k["he"])
        right, w = "%d + %d = ?" % (a, b), ["%d − %d = ?" % (a, b), "%d + ? = %d" % (a, b), "? − %d = %d" % (b, a)]
    elif kind == "gave":
        if b >= a:
            return None
        q = "%s has %d %s. %s gives away %d. Which number sentence shows how many are left?" % (k["n"], a, t, k["He"], b)
        right, w = "%d − %d = ?" % (a, b), ["%d + %d = ?" % (a, b), "%d − ? = %d" % (b, a), "? + %d = %d" % (a, b)]
    elif kind == "start":
        q = "%s had some %s. %s got %d more. Now %s has %d. Which number sentence fits?" % (k["n"], t, k["He"], b, k["he"], a + b)
        right, w = "? + %d = %d" % (b, a + b), ["%d + %d = ?" % (b, a + b), "%d − ? = %d" % (b, a + b), "? − %d = %d" % (b, a + b)]
    else:
        k2 = Kid(r).next()
        if k2["n"] == k["n"] or a == b:
            return None
        big, small = max(a, b), min(a, b)
        q = "%s has %d %s. %s has %d %s. Which number sentence shows how many more %s has?" % (k["n"], big, t, k2["n"], small, t, k["n"])
        right, w = "%d − %d = ?" % (big, small), ["%d + %d = ?" % (big, small), "%d − %d = ?" % (small, big), "? − %d = %d" % (small, big)]
    return mcq(q, right, w, "The story matches <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Find the result", [("run", wp.set_result, ("rnd", wp.People), 20)]),
        ("Find a part", [("run", wp.set_parts, ("rnd", wp.People), 20)]),
        ("Which number sentence fits?", [("collect", one_sentence, 20)]),
        ("Mixed stories", [("run", wp.set_result, ("rnd", wp.People), 10), ("run", wp.set_parts, ("rnd", wp.People), 10)]),
        ("Stories and number sentences", [("collect", one_sentence, 10), ("run", wp.set_parts, ("rnd", wp.People), 10)]),
    ], 69208)
    finish(sets, R)
    body = lesson('<ul><li>Read the story. What do you know? What do you need to find?</li><li><b>Joining</b> or putting together: add. <b>Taking away</b> or comparing: subtract.</li><li>The unknown can be the start, the change or the end. Use ? for the unknown in a number sentence.</li><li>Check that your answer makes sense in the story.</li></ul>',
        [example("Ava had some shells. She found 15 more. Now she has 42.", ["? + 15 = 42", "42 − 15"], "27 shells")],
        [['Adding when you should subtract', 'Gives away or how many more usually means subtract.'], ['Using the wrong numbers', 'Underline the numbers that matter.'], ['Mixing up the whole and the parts', 'The whole is the total; the parts add up to it.']])
    faq = [('What does TEKS 2.4D ask?', 'Generate and solve problem situations for a given mathematical number sentence involving addition and subtraction of whole numbers within 1,000.'), ('What does TEKS 2.7C ask?', 'Represent and solve addition and subtraction word problems where unknowns may be any one of the terms in the problem.'), ('What is a number sentence?', 'A math sentence like 27 + 15 = 42.'), ('What does the ? mean?', 'It stands for the number you need to find.')]
    make('word-problems-and-number-sentences', 8, 'Algebraic Reasoning', '2.4D, 2.7C',
         '2.4D generate and solve problem situations for a given mathematical number sentence involving addition and subtraction of whole numbers within 1,000; 2.7C represent and solve addition and subtraction word problems where unknowns may be any one of the terms in the problem',
         'Word Problems and Number Sentences', 'Word Problems and Number Sentences',
         'Free Grade 2 word problem worksheets for Texas TEKS 2.4D and 2.7C: addition and subtraction stories with the unknown in any place and matching number sentences. 100 questions with answers.',
         'Find what you know and what you need; then add or subtract.', '? + 15 = 42, so ? = 27.',
         body, faq, sets, seo_title='Grade 2 Addition and Subtraction Word Problems Worksheets (TEKS 2.4D, 2.7C)')


if __name__ == "__main__":
    build()
