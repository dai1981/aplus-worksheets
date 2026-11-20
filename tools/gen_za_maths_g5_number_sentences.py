# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Number Sentences: Missing Numbers and Equations (Grade 5: 2.3 Number sentences)
  python3 tools/gen_za_maths_g5_number_sentences.py
Number sentences with a missing number or a letter, checking a solution by substitution, writing a number sentence
for a story, and fact families (BC Grade 5, Ontario Grade 5 and Australia Year 5 makers).
Wrong answers come from real mistakes: doing the same operation instead of the inverse, reading = as "the answer is
next", and choosing the wrong operation for the story.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g5_equations as cbe
adopt(cbe)
if isinstance(getattr(cbe, 'R', None), random.Random): cbe.R = random.Random(805140)
import gen_caon_math_g5_equations as cae
adopt(cae)
if isinstance(getattr(cae, 'R', None), random.Random): cae.R = random.Random(805141)
import gen_au_maths_y5_number_sentences as aun
adopt(aun)
if isinstance(getattr(aun, 'R', None), random.Random): aun.R = random.Random(805142)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Missing numbers in + and −", [("run", cbe.set_add_sub, (cbe.People,), 20, six)]),
        ("Missing numbers in × and ÷", [("run", cbe.set_mul_div, (cbe.People,), 20, six)]),
        ("Solve number sentences", [("run", cae.set_solve, ("rnd", cae.People), 20, six)]),
        ("Check the solution", [("run", cbe.set_check, (cbe.People,), 10, six), ("run", cae.set_check, ("rnd", cae.People), 10, six)]),
        ("Write a number sentence", [("run", cbe.set_words, (cbe.People,), 10, six), ("run", aun.set_words, (aun.People,), 10, six)]),
    ], 80514)
    finish(sets, R)
    body = lesson('<ul><li>A number sentence uses = to show that both sides have the same value: 45 + ☐ = 120.</li><li>Use the inverse operation to find the missing number: ☐ = 120 − 45 = 75.</li><li>A letter can stand for the missing number: 8 × n = 96, so n = 12.</li><li>Check by putting the number back into the sentence (substitution).</li></ul>',
        [example("☐ ÷ 6 = 34", ["inverse: 34 × 6"], "☐ = 204")],
        [['The same operation', 'Use the inverse.'], ['= means the answer', '= means the same value on both sides.'], ['Wrong operation', 'Read what the story does.']])
    faq = [('What does CAPS Grade 5 say about number sentences?', 'Write number sentences to describe problem situations, solve and complete number sentences by inspection and by trial and improvement, and check solutions by substitution.'), ('What is substitution?', 'Putting a number in place of the letter or ☐ to check.'), ('What is trial and improvement?', 'Trying a number, checking, and trying a better one.'), ('Can the ☐ be on either side?', 'Yes.')]
    make('number-sentences', 14, 'Patterns, Functions and Algebra', 'Grade 5: 2.3 Number sentences',
         'Write number sentences to describe problem situations; solve and complete number sentences by inspection and by trial and improvement; check solutions by substitution.',
         'Number Sentences: Missing Numbers and Equations', 'Number Sentences',
         'Free CAPS Grade 5 number sentences worksheets: missing numbers, letters for unknowns, checking by substitution and writing number sentences. 100 questions with memos.',
         'Use the inverse operation.', 'Check by substitution.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
