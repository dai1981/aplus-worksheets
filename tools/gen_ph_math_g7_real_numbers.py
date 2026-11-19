# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Subsets of the Real Numbers (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_real_numbers.py
Natural numbers, whole numbers, integers, rational and irrational numbers: classifying numbers, which sets a number
belongs to, and true or false statements (Texas Grade 7 and Grade 8 makers).
Wrong answers come from real mistakes: thinking fractions are not rational, putting negative numbers in the whole
numbers, and calling every square root irrational.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_ustx_math_g7_rational_number_sets as tx7
adopt(tx7)
if hasattr(tx7, 'R'): tx7.R = random.Random(707140)
import gen_ustx_math_g8_real_number_sets as tx8
adopt(tx8)
if hasattr(tx8, 'R'): tx8.R = random.Random(707141)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


POOL = {"natural": ["7", "12", "1", "25", "100"], "zero": ["0"], "negint": ["−3", "−15", "−1", "−42"], "frac": ["<span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>", "−0.75", "3.4", "0.333…", "−<span class='fr'><span class='fn'>7</span><span class='fd'>3</span></span>", "√49 ÷ 2"],
        "irr": ["√7", "π", "∛20", "√2", "0.1010010001…"]}
ASK = [("a whole number but not a natural number", "zero", ["natural", "negint", "frac"]),
       ("an integer but not a whole number", "negint", ["natural", "zero", "frac"]),
       ("a rational number but not an integer", "frac", ["natural", "negint", "irr"]),
       ("a real number but not a rational number", "irr", ["natural", "frac", "negint"]),
       ("a natural number", "natural", ["zero", "negint", "frac"]),
       ("an irrational number", "irr", ["frac", "natural", "negint"])]


_SEEN = set()


def one_but(r):
    t, good, bad = r.choice(ASK)
    g = r.choice(POOL[good])

    w = [r.choice(POOL[b]) for b in bad]
    allv = [g] + w
    r.shuffle(allv)
    return mcq("Which of these numbers is %s: %s?" % (t, ", ".join(allv)), g, w, "Natural ⊂ whole ⊂ integers ⊂ rational ⊂ real. <b>%s</b> is %s." % (g, t))


def build():
    sets, R = build_sets([
        ("Classify rational numbers", [("collect", tx7.one_classify, 20)]),
        ("Which number fits?", [("collect", tx7.one_which, 20)]),
        ("Classify real numbers", [("collect", tx8.one_classify, 20)]),
        ("True or false: rational numbers", [("collect", tx7.one_true, 20)]),
        ("Which set is it in?", [("collect", one_but, 20)]),
    ], 70714)
    finish(sets, R)
    body = lesson("<ul><li><b>Natural</b> (counting) numbers: 1, 2, 3, … <b>Whole</b> numbers: 0, 1, 2, 3, …</li><li><b>Integers</b>: …, −2, −1, 0, 1, 2, …</li><li><b>Rational</b> numbers can be written as a fraction of integers: −3, 0.25, <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>, 0.333…</li><li><b>Irrational</b> numbers cannot: √2, π. Rational and irrational numbers together make the <b>real</b> numbers. Each set sits inside the next: natural ⊂ whole ⊂ integers ⊂ rational ⊂ real.</li></ul>",
        [example("−7", ["not whole", "integer", "rational", "real"], "integer, rational, real")],
        [['Fractions are not rational', 'Every fraction of integers is rational.'], ['Negatives as whole numbers', 'Whole numbers start at 0.'], ['Every root is irrational', '√25 = 5 is rational.']])
    faq = [('What does MATATAG Math 7 ask about real numbers?', 'Illustrate the different subsets of real numbers.'), ('Is 0 a natural number?', 'In the Philippine curriculum, natural numbers start at 1; 0 is a whole number.'), ('Is every integer rational?', 'Yes: −4 = −4/1.'), ('Can a number be both rational and irrational?', 'No.')]
    make('subsets-of-real-numbers', 14, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Illustrate the different subsets of real numbers.',
         'Subsets of the Real Numbers', 'Subsets of Real Numbers',
         'Free Grade 7 real number worksheets for the DepEd MATATAG curriculum: natural numbers, whole numbers, integers, rational and irrational numbers. 100 questions with answers.',
         'Natural ⊂ whole ⊂ integers ⊂ rational ⊂ real.', 'Irrational numbers are real but not rational.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
