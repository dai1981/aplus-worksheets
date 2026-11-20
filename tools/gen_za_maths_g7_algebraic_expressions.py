# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Algebraic Expressions: Notation, Writing, Simplifying and Substituting (Grade 7: 2.3 Algebraic expressions)
  python3 tools/gen_za_maths_g7_algebraic_expressions.py
Algebraic notation, writing expressions for words and situations, like terms, and substitution (UK Year 7 and
Australia Year 7 makers).
Wrong answers come from real mistakes: writing 3x as x + 3, adding unlike terms, and forgetting the order of
operations when substituting.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_algebraic_notation_and_substitution as ukn
adopt(ukn)
if isinstance(getattr(ukn, 'R', None), random.Random): ukn.R = random.Random(807150)
import gen_au_maths_y7_algebraic_expressions as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(807151)
import gen_uk_maths_y7_simplifying_expressions as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(807152)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Algebraic notation", [("collect", ukn.one_notation, 20)]),
        ("Write an expression", [("collect", ukn.one_words, 10), ("collect", aue.one_words, 10)]),
        ("Like terms", [("collect", uks.one_like1, 10), ("collect", aue.one_like1, 10)]),
        ("Substitution", [("collect", ukn.one_sub, 20)]),
        ("Expressions in context", [("collect", ukn.one_context, 9), ("collect", aue.one_situation, 11)]),
    ], 80715)
    finish(sets, R)
    body = lesson("<ul><li>3x means 3 × x. x² means x × x. <span class='fr'><span class='fn'>x</span><span class='fd'>4</span></span> means x ÷ 4.</li><li>Like terms have the same letter part: 5a + 2a = 7a, but 5a + 2b cannot be simplified.</li><li>Substitution: put the number in place of the letter and use the order of operations.</li><li>If a = 4, then 3a + 5 = 3 × 4 + 5 = 17.</li></ul>",
        [example("Simplify 4x + 7 − x + 2", ["4x − x = 3x", "7 + 2 = 9"], "3x + 9")],
        [['3x as x + 3', '3x = 3 × x.'], ['Unlike terms', 'Only add terms with the same letters.'], ['Order of operations', 'Multiply before you add.']])
    faq = [('What does CAPS Grade 7 say about algebraic expressions?', 'Recognise and interpret rules or relationships represented in symbolic form, and identify variables and constants in given formulae or equations.'), ('What is a term?', 'A part of an expression, like 3x or 5.'), ('What is a constant?', 'A number on its own.'), ('What is 2x² when x = 3?', '18.')]
    make('algebraic-expressions', 15, 'Patterns, Functions and Algebra', 'Grade 7: 2.3 Algebraic expressions',
         'Recognise and interpret rules or relationships represented in symbolic form; identify variables and constants in given formulae and/or equations; recognise and identify like and unlike terms; add and subtract like terms; use substitution to determine the value of an expression.',
         'Algebraic Expressions: Notation, Writing, Simplifying and Substituting', 'Algebraic Expressions',
         'Free CAPS Grade 7 algebraic expressions worksheets: notation, writing expressions, like terms, simplifying and substitution. 100 questions with memos.',
         '3x means 3 × x.', 'Only add like terms.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
