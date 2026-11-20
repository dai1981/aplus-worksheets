# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Number Sentences: Writing and Solving (Grade 4: 2.3 Number sentences)
  python3 tools/gen_za_maths_g4_number_sentences.py
Fact families, unknowns in number sentences, the equal sign, solving by inspection and by trial and improvement, and
writing number sentences for problems (Australia Year 4 and Ontario Grade 4 makers with South African names).
Wrong answers come from real mistakes: writing the answer of one side in the box, thinking = means "the answer
is", and writing the operations in the wrong order.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_number_sentences as aun
adopt(aun)
if hasattr(aun, 'R'): aun.R = random.Random(804140)
import gen_caon_math_g4_equations as cae
adopt(cae)
if hasattr(cae, 'R'): cae.R = random.Random(804141)
za_common.GRADE = "grade-4"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def nodec(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return not _re.search(r"\d\.\d", t)



def build():
    sets, R = build_sets([
        ("Fact families", [("run", aun.set_families, (), 20)]),
        ("Find the unknown", [("run", aun.set_unknowns, (), 20)]),
        ("The equal sign", [("run", aun.set_equals, (aun.People,), 20)]),
        ("Solve by trial and improvement", [("run", cae.set_solve, (), 10), ("run", cae.set_check, (cae.People,), 10)]),
        ("Write number sentences", [("run", aun.set_words, (aun.People,), 10), ("run", cae.set_words, (cae.People,), 10)]),
    ], 80414)
    finish(sets, R)
    body = lesson('<ul><li>A <b>number sentence</b> uses numbers and signs: 25 + ☐ = 60.</li><li>The equal sign means both sides have the <b>same value</b>.</li><li>Solve by <b>inspection</b> (just see it) or by <b>trial and improvement</b>: try a number, check, and improve.</li><li>Write a number sentence for a problem, solve it, and check by <b>substitution</b>: put the answer back in.</li></ul>',
        [example("☐ × 6 = 54", ["try 8: 48, too small", "try 9: 54"], "9")],
        [["One side's answer", 'In 25 + ☐ = 30 + 15, ☐ is 20, not 45.'], ['= means the answer', '= means the same value.'], ['Wrong order', 'Follow the story.']])
    faq = [('What does CAPS Grade 4 say about number sentences?', 'Write number sentences to describe problem situations, and solve and complete them by inspection and trial and improvement, checking the solution by substitution.'), ('What is substitution?', 'Putting the answer back into the number sentence to check it.'), ('Why use a box?', 'It stands for the unknown number.'), ('Is this algebra?', 'Yes, it is an introduction to algebraic expressions.')]
    make('number-sentences', 14, 'Patterns, Functions and Algebra', 'Grade 4: 2.3 Number sentences',
         'Write number sentences to describe problem situations; solve and complete number sentences by inspection and trial and improvement; check solutions by substitution.',
         'Number Sentences: Writing and Solving', 'Number Sentences',
         'Free CAPS Grade 4 number sentences worksheets: fact families, unknowns, the equal sign, trial and improvement and writing number sentences. 100 questions with memos.',
         '= means both sides have the same value.', 'Check by substitution.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
