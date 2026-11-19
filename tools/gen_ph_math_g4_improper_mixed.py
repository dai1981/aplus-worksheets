# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Proper Fractions, Improper Fractions and Mixed Numbers (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_improper_mixed.py
Naming proper and improper fractions and mixed numbers from models, changing between improper fractions and mixed
numbers (Singapore Primary 4 makers), and fractions with denominators 2, 4, 5 and 10 on the number line (own maker).
Wrong answers come from real mistakes: counting all the parts as the denominator, putting the remainder on the bottom,
and counting tick marks instead of spaces.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_p4_mixed_numbers as sgm
adopt(sgm)
if hasattr(sgm, 'R'): sgm.R = random.Random(704110)
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


from ws_common import svg_wrap, text, GREEN, INK, RED


def nl_svg(d, wholes, k, letter="P"):
    """number line 0..wholes with ticks every 1/d and a point at k/d"""
    W, x0, x1, y = 380, 20, 360, 40
    step = (x1 - x0) / (wholes * d)
    b = "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, y, x1, y, INK)
    for i in range(wholes * d + 1):
        x = x0 + i * step
        big = i % d == 0
        b += "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>" % (x, y - (10 if big else 6), x, y + (10 if big else 6), INK, 2 if big else 1)
        if big:
            b += text(x, y + 28, str(i // d), 15)
    x = x0 + k * step
    b += "<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (x, y, RED) + text(x, y - 16, letter, 15, col=RED)
    return svg_wrap(W, 80, b, "number line from 0 to %d with a point %s" % (wholes, letter))


KINDS = ["Proper fraction", "Improper fraction", "Mixed number", "Whole number"]


def one_kind(r):
    d = r.randint(2, 12)
    kind = r.choice(["p", "i", "m"])
    if kind == "p":
        n = r.randint(1, d - 1)
        t, right = fr(n, d), KINDS[0]
        why = "The numerator %d is less than the denominator %d." % (n, d)
    elif kind == "i":
        n = r.randint(d + 1, 3 * d)
        if n % d == 0:
            raise AssertionError
        t, right = fr(n, d), KINDS[1]
        why = "The numerator %d is greater than the denominator %d." % (n, d)
    else:
        w, n = r.randint(1, 9), r.randint(1, d - 1)
        t, right = "%d %s" % (w, fr(n, d)), KINDS[2]
        why = "It has a whole number and a proper fraction."
    return mcq("What kind of number is %s?" % t, right, [k for k in KINDS if k != right], why + " <b>%s</b>." % right)


def one_nl(r):
    d = r.choice([2, 4, 5, 10])
    wholes = 3 if d < 10 else 2
    k = r.randint(1, wholes * d - 1)
    if k % d == 0:
        raise AssertionError
    form = r.choice(["mixed", "improper"]) if k > d else "proper"
    w_, n_ = divmod(k, d)
    if form == "mixed":
        right = "%d %s" % (w_, fr(n_, d))
        wr = ["%d %s" % (w_, fr(n_, d + 1)), "%d %s" % (w_ + 1, fr(n_, d)), fr(k, d)]
        ask = "as a mixed number"
    elif form == "improper":
        right = fr(k, d)
        wr = [fr(k, d + 1), fr(k + 1, d), "%d %s" % (w_, fr(n_, d))]
        ask = "as an improper fraction"
    else:
        right = fr(k, d)
        wr = [fr(k, d + 1), fr(k + 1, d), fr(d - k, d) if d - k != k else fr(k, d * 2)]
        ask = "as a fraction"
    return mcq(fig(nl_svg(d, wholes, k)) + "Each whole is split into %d equal parts. What number is at point P? Write it %s." % (d, ask), right, wr,
               "Count the spaces: P is %d parts of %s from 0, which is %s. <b>%s</b>." % (k, fr(1, d), fr(k, d), right))


def build():
    sets, R = build_sets([
        ("Proper, improper or mixed?", [("collect", uniq(one_kind), 20)]),
        ("Improper fractions from models", [("run", sgm.set_improper, ("rnd",), 20)]),
        ("Mixed numbers from models", [("run", sgm.set_mixed, ("rnd",), 20)]),
        ("Change between improper fractions and mixed numbers", [("run", sgm.set_convert, ("rnd",), 20)]),
        ("Fractions on the number line", [("collect", uniq(one_nl), 20)]),
    ], 70411)
    finish(sets, R)
    body = lesson("<ul><li>A <b>proper fraction</b> is less than 1: the numerator is smaller than the denominator (<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>).</li><li>An <b>improper fraction</b> is 1 or more: the numerator is greater than or equal to the denominator (<span class='fr'><span class='fn'>7</span><span class='fd'>4</span></span>).</li><li>A <b>mixed number</b> has a whole number and a proper fraction (1 <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>).</li><li>Improper to mixed: divide the numerator by the denominator. The quotient is the whole number; the remainder is the new numerator. Mixed to improper: whole × denominator + numerator.</li></ul>",
        [example("<span class='fr'><span class='fn'>11</span><span class='fd'>4</span></span>", ["11 ÷ 4 = 2 remainder 3"], "2 <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>"), example("3 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>", ["3 × 5 + 2 = 17"], "<span class='fr'><span class='fn'>17</span><span class='fd'>5</span></span>")],
        [['Counting all the parts as the denominator', 'The denominator is the number of parts in one whole.'], ['The remainder on the bottom', 'The remainder is the numerator; the denominator stays.'], ['Counting tick marks', 'Count the spaces from 0.']])
    faq = [('What does MATATAG Math 4 ask about fractions?', 'Identify proper fractions, improper fractions, and mixed numbers, rewrite improper fractions into mixed numbers and vice versa, and plot fractions with denominators 2, 4, 5, and 10 on the number line.'), ('Is 4/4 a proper fraction?', 'No. It equals 1, so it is improper.'), ('Why use mixed numbers?', 'They show how many wholes there are.'), ('Do the denominator change when I convert?', 'No. It stays the same.')]
    make('proper-improper-fractions-and-mixed-numbers', 11, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Identify proper fractions, improper fractions, and mixed numbers; rewrite improper fractions into mixed numbers, and vice versa; plot fractions (proper fractions, improper fractions, and mixed numbers) with denominators 2, 4, 5, and 10 on the number line.',
         'Proper Fractions, Improper Fractions and Mixed Numbers', 'Improper Fractions and Mixed Numbers',
         'Free Grade 4 worksheets on proper and improper fractions and mixed numbers for the DepEd MATATAG curriculum: identify, convert and plot on the number line. 100 questions with answers.',
         'Improper to mixed: divide; the remainder is the new numerator.', 'Mixed to improper: whole × denominator + numerator.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
