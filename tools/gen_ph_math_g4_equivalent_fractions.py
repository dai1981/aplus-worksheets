# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Equivalent Fractions and Reducing Fractions to Simplest Form (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_equivalent_fractions.py
Equivalent fractions from models, multiplying and dividing the numerator and denominator by the same number (US Grade
4 makers), reducing fractions to simplest form (Singapore Primary 3 maker and own maker), and word problems.
Wrong answers come from real mistakes: adding the same number to the top and bottom, changing only one of the two
numbers, and stopping before the fraction is in simplest form.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_equivalent_fractions as use
adopt(use)
if hasattr(use, 'R'): use.R = random.Random(704160)
import gen_sg_maths_p3_equivalent_fractions as sge
adopt(sge)
if hasattr(sge, 'R'): sge.R = random.Random(704161)
ph_common.GRADE = "grade-4"

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


from math import gcd


def one_simplest(r):
    d = r.randint(4, 60)
    n = r.randint(2, d - 1)
    g = gcd(n, d)
    if g == 1 or d // g > 12:
        raise AssertionError
    a, b = n // g, d // g
    divs = [k for k in range(2, g) if g % k == 0 and n % k == 0 and d % k == 0]
    w = []
    if divs:
        k = divs[0]
        w.append(fr(n // k, d // k))
    w += [fr(n - (g - 1) if n - (g - 1) > 0 else n + 1, d - (g - 1)), fr(a, d), fr(n, b)]
    q = "Write %s in simplest form." % fr(n, d)
    e = "The greatest number that divides both %d and %d is %d. %d ÷ %d = %d and %d ÷ %d = %d. <b>%s</b>." % (n, d, g, n, g, a, d, g, b, fr(a, b))
    return mcq(q, fr(a, b), w + [fr(a + 1, b)], e)


def build():
    sets, R = build_sets([
        ("Equivalent fractions from models", [("run", use.set_models, ("rnd",), 20)]),
        ("Multiply to find equivalent fractions", [("run", use.set_multiply, ("rnd",), 20)]),
        ("Divide to find equivalent fractions", [("run", use.set_divide, ("rnd",), 20)]),
        ("Reduce to simplest form", [("run", sge.set_simplest, ("rnd",), 8), ("collect", uniq(one_simplest), 12)]),
        ("Equivalent fractions word problems", [("run", use.set_words, ("rnd",), 20)]),
    ], 70416)
    finish(sets, R)
    body = lesson("<ul><li><b>Equivalent fractions</b> name the same amount, like <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> = <span class='fr'><span class='fn'>2</span><span class='fd'>4</span></span> = <span class='fr'><span class='fn'>4</span><span class='fd'>8</span></span>.</li><li>Multiply or divide the numerator <b>and</b> the denominator by the same number.</li><li>A fraction is in <b>simplest form</b> when 1 is the only number that divides both the numerator and the denominator.</li><li>To reduce, divide both by their greatest common factor. You can also divide in small steps until you cannot go on.</li></ul>",
        [example("<span class='fr'><span class='fn'>18</span><span class='fd'>24</span></span> in simplest form", ["18 ÷ 6 = 3", "24 ÷ 6 = 4"], "<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>")],
        [['Adding the same number', "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> is not <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>. Multiply instead."], ['Changing only one number', 'Do the same to the top and the bottom.'], ['Stopping too soon', "<span class='fr'><span class='fn'>6</span><span class='fd'>8</span></span> can still be reduced to <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>."]])
    faq = [('What does MATATAG Math 4 ask about equivalent fractions?', 'Generate equivalent fractions using models, determine equivalent fractions, and reduce fractions to simplest form.'), ('How do I know a fraction is in simplest form?', 'No number except 1 divides both the numerator and the denominator.'), ('Is 5/5 in simplest form?', 'It equals 1, the simplest name for it.'), ('Why learn equivalent fractions?', 'You need them to compare, add and subtract dissimilar fractions.')]
    make('equivalent-fractions-and-simplest-form', 16, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Generate equivalent fractions using models; determine equivalent fractions; reduce fractions to simplest form.',
         'Equivalent Fractions and Reducing Fractions to Simplest Form', 'Equivalent Fractions',
         'Free Grade 4 equivalent fractions worksheets for the DepEd MATATAG curriculum: models, multiplying and dividing, simplest form and word problems. 100 questions with answers.',
         'Multiply or divide the top and bottom by the same number.', 'Simplest form: only 1 divides both.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
