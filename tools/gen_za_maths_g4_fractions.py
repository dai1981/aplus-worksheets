# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Common Fractions: Describing, Comparing, Adding and Equivalent Fractions (Grade 4: 1.2 Common fractions)
  python3 tools/gen_za_maths_g4_fractions.py
Fractions from diagrams, comparing and ordering fractions, equivalent fractions, adding and subtracting fractions
with the same denominator, and fractions of whole numbers (UK Year 3 and Year 4 makers). Denominators are halves to
eighths, as in CAPS Grade 4.
Wrong answers come from real mistakes: thinking a bigger denominator means a bigger fraction, adding the
denominators, and dividing by the numerator when finding a fraction of a number.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_fractions as ukf
adopt(ukf)
if hasattr(ukf, 'R'): ukf.R = random.Random(804100)
import gen_uk_maths_y3_fractions as uk3
adopt(uk3)
if hasattr(uk3, 'R'): uk3.R = random.Random(804101)
import gen_au_maths_y4_equivalent_fractions as aue
adopt(aue)
if hasattr(aue, 'R'): aue.R = random.Random(804102)
za_common.GRADE = "grade-4"

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


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def le100k(it):
    return all(n <= 99999 for n in _nums(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 12 for d in ds)


def den8(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 8 for d in ds)


def one_addf(r):
    d = r.randint(3, 8)
    a, b = r.randint(1, d - 1), r.randint(1, d - 1)
    if r.random() < 0.6:
        if a + b > d:
            raise AssertionError
        s_ = a + b
        right = "1" if s_ == d else fr(s_, d)
        wr = [fr(a + b, d + d), fr(a * b, d) if a * b < d and a * b != s_ else fr(s_, d * 2 - 1), fr(s_ + 1, d) if s_ + 1 <= d else fr(a, d + b)]
        return mcq("<b>%s + %s</b> = ?" % (fr(a, d), fr(b, d)), right, wr, "Add the numerators and keep the denominator: %d + %d = %d. <b>%s</b>%s" % (a, b, s_, right, " (a whole)." if s_ == d else "."))
    if a <= b:
        a, b = b, a
    if a == b:
        raise AssertionError
    right = fr(a - b, d)
    return mcq("<b>%s − %s</b> = ?" % (fr(a, d), fr(b, d)), right, [fr(a - b, 0 + 1) if False else fr(a - b, d - d + d * 2), fr(a + b, d) if a + b <= d else fr(a - b + 1, d), fr(b, d) if b != a - b else fr(a, d)],
               "Subtract the numerators and keep the denominator: %d − %d = %d. <b>%s</b>." % (a, b, a - b, right))


def one_wordf(r):
    k = Kid(r).next()
    d = r.randint(3, 8)
    a, b = r.randint(1, d - 2), r.randint(1, d - 2)
    if a + b >= d:
        raise AssertionError
    what = r.choice(["pizza", "melktert", "chocolate slab", "loaf of bread", "watermelon"])
    q = "%s eats %s of a %s and %s friend eats %s of it. What fraction of the %s did they eat together?" % (k["n"], fr(a, d), what, k["his"], fr(b, d), what)
    return mcq(q, fr(a + b, d), [fr(a + b, 2 * d), fr(d - a - b, d), fr(a * b, d) if a * b < d and a * b != a + b else fr(a + b + 1, d)], "%s + %s = <b>%s</b>." % (fr(a, d), fr(b, d), fr(a + b, d)))


def build():
    sets, R = build_sets([
        ("Fractions in diagrams", [("run", uk3.set_shaded, ("rnd",), 10, den8), ("run", ukf.set_diagrams, ("rnd",), 10, den8)]),
        ("Compare and order fractions", [("run", uk3.set_compare, ("rnd",), 20, den8)]),
        ("Equivalent fractions", [("run", uk3.set_equiv, ("rnd",), 10, den12), ("run", aue.set_missing, ("rnd",), 5, den12), ("run", aue.set_shapes, ("rnd",), 5, den12)]),
        ("Add and subtract fractions", [("collect", uniq(one_addf), 14), ("collect", uniq(one_wordf), 6)]),
        ("Fractions of whole numbers", [("run", ukf.set_amounts, ("rnd",), 10, den8), ("run", ukf.set_words, ("rnd",), 10, den8)]),
    ], 80410)
    finish(sets, R)
    body = lesson("<ul><li>A <b>common fraction</b> has a numerator and a denominator: <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> means 3 of 5 equal parts.</li><li>With the same numerator, the smaller denominator is the bigger fraction: <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> &gt; <span class='fr'><span class='fn'>1</span><span class='fd'>6</span></span>.</li><li><b>Equivalent fractions</b> name the same amount: <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> = <span class='fr'><span class='fn'>2</span><span class='fd'>4</span></span> = <span class='fr'><span class='fn'>4</span><span class='fd'>8</span></span>.</li><li>Add fractions with the same denominator: add the numerators, keep the denominator.</li><li><span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> of 20: 20 ÷ 4 = 5, 5 × 3 = 15.</li></ul>",
        [example("<span class='fr'><span class='fn'>2</span><span class='fd'>7</span></span> + <span class='fr'><span class='fn'>3</span><span class='fd'>7</span></span>", ["add the numerators: 2 + 3"], "<span class='fr'><span class='fn'>5</span><span class='fd'>7</span></span>")],
        [['Bigger denominator, bigger fraction', 'Eighths are smaller than quarters.'], ['Adding denominators', 'Keep the denominator.'], ['Fraction of a number', 'Divide by the denominator, then multiply by the numerator.']])
    faq = [('What does CAPS Grade 4 say about fractions?', 'Count, compare and order common fractions (halves to eighths), describe and represent them in diagrams, add common fractions with the same denominators, recognise equivalent fractions, and find fractions of whole numbers.'), ('What are sevenths?', 'Seven equal parts of a whole; new in Grade 4.'), ('Is 2/4 the same as 1/2?', 'Yes, they are equivalent.'), ('Which is bigger, 3/8 or 3/5?', '3/5.')]
    make('common-fractions', 10, 'Numbers, Operations and Relationships', 'Grade 4: 1.2 Common fractions',
         'Count forwards and backwards in fractions; compare and order common fractions with different denominators (halves, thirds, quarters, fifths, sixths, sevenths, eighths); describe and compare common fractions in diagram form; add common fractions with the same denominators; recognise, describe and use the equivalence of division and fractions; recognise and use equivalent forms of common fractions; solve problems involving fractions of whole numbers.',
         'Common Fractions: Describing, Comparing, Adding and Equivalent Fractions', 'Common Fractions',
         'Free CAPS Grade 4 common fractions worksheets: fractions in diagrams, comparing and ordering, equivalent fractions, adding fractions and fractions of whole numbers. 100 questions with memos.',
         'Same denominator: add the numerators.', 'Same numerator: smaller denominator, bigger fraction.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
