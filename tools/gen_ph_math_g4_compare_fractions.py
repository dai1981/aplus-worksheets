# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Comparing and Ordering Dissimilar Fractions (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_compare_fractions.py
Comparing fractions with different denominators (up to 10) with models, common denominators and common numerators (US
Grade 4 makers with Filipino names), ordering fractions (Australia Year 5 maker and own maker), and word problems.
Wrong answers come from real mistakes: thinking a bigger denominator means a bigger fraction, comparing only the
numerators, and comparing parts of different-sized wholes.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_compare_fractions as usc
adopt(usc)
if hasattr(usc, 'R'): usc.R = random.Random(704150)
import gen_au_maths_y5_compare_fractions as auc
adopt(auc)
if hasattr(auc, 'R'): auc.R = random.Random(704151)
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


import re as _re


def den10(it):
    """Grade 4 MATATAG: dissimilar fractions with denominators up to 10."""
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 10 for d in ds)


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 12 for d in ds)


def den_q12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"])]
    return all(d <= 12 for d in ds)


def den_q10(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"])]
    return all(d <= 10 for d in ds)


from fractions import Fraction as F


def one_sym(r):
    d1, d2 = r.sample([2, 3, 4, 5, 6, 8, 9, 10], 2)
    a, b = F(r.randint(1, d1 - 1), d1), F(r.randint(1, d2 - 1), d2)
    if a.denominator != d1 or b.denominator != d2:
        raise AssertionError
    A, B = fr(a.numerator, d1), fr(b.numerator, d2)
    st = lambda x, sym, y: "%s %s %s" % (x, sym, y)
    true = st(A, "&lt;", B) if a < b else st(A, "&gt;", B) if a > b else st(A, "=", B)
    opts = [st(A, "&lt;", B), st(A, "&gt;", B), st(A, "=", B), st(B, "&gt;", A) if a > b else st(B, "&lt;", A)]
    L = d1 * d2 // __import__("math").gcd(d1, d2)
    return mcq("Compare %s and %s. Which statement is true?" % (A, B), true, [o for o in opts if o != true],
               "Use the common denominator %d: %s = %s and %s = %s. <b>%s</b>." % (L, A, fr(a.numerator * L // d1, L), B, fr(b.numerator * L // d2, L), true))


def one_order(r):
    for _ in range(50):
        ds = r.sample([2, 3, 4, 5, 6, 8, 10], 3)
        fs = []
        for d in ds:
            fs.append(F(r.randint(1, d - 1), d))
        if len(set(fs)) == 3 and all(f.denominator in ds for f in fs) and len({f.denominator for f in fs}) == 3:
            break
    else:
        raise AssertionError
    show = lambda f: fr(f.numerator, f.denominator)
    up = r.random() < 0.5
    srt = sorted(fs, reverse=not up)
    right = ", ".join(show(f) for f in srt)
    by_den = sorted(fs, key=lambda f: f.denominator, reverse=up)
    by_num = sorted(fs, key=lambda f: (f.numerator, f.denominator), reverse=not up)
    rev = list(reversed(srt))
    w = [", ".join(show(f) for f in x) for x in (by_den, by_num, rev)]
    w = [x for x in w if x != right]
    w += [", ".join(show(f) for f in (srt[1], srt[0], srt[2])), ", ".join(show(f) for f in (srt[0], srt[2], srt[1]))]
    order = "smallest to largest" if up else "largest to smallest"
    vals = "; ".join("%s ≈ %s" % (show(f), ("%.2f" % float(f)).rstrip("0").rstrip(".")) for f in srt)
    return mcq("Order from %s: %s" % (order, ", ".join(show(f) for f in fs)), right, w,
               "Compare each fraction with %s and 1, or rename them with a common denominator. %s. <b>%s</b>." % (fr(1, 2), vals, right))


def build():
    sets, R = build_sets([
        ("Compare with fraction models", [("run", usc.set_models, ("rnd", usc.People), 20, den10)]),
        ("Compare with a common denominator", [("run", usc.set_common_den, ("rnd", usc.People), 14, den12), ("collect", uniq(one_sym), 6)]),
        ("Compare with a common numerator", [("run", usc.set_common_num, ("rnd", usc.People), 12, den12), ("collect", uniq(one_sym), 8)]),
        ("Order dissimilar fractions", [("run", auc.set_order, ("rnd",), 8, den10), ("collect", uniq(one_order), 12)]),
        ("Compare fractions word problems", [("run", usc.set_words, ("rnd", usc.People), 20, den10)]),
    ], 70415)
    finish(sets, R)
    body = lesson("<ul><li><b>Dissimilar fractions</b> have different denominators, like <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> and <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>.</li><li>Same numerator: the fraction with the <b>smaller</b> denominator is bigger (the parts are bigger).</li><li>Different numerators and denominators: rename both with a <b>common denominator</b>, then compare the numerators.</li><li>Benchmarks help: compare each fraction with <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> or 1.</li><li>Only compare fractions of the same whole.</li></ul>",
        [example("<span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> ☐ <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>", ["<span class='fr'><span class='fn'>8</span><span class='fd'>12</span></span> and <span class='fr'><span class='fn'>9</span><span class='fd'>12</span></span>", "8 &lt; 9"], "&lt;")],
        [['A bigger denominator is bigger', "<span class='fr'><span class='fn'>1</span><span class='fd'>8</span></span> &lt; <span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span>: eighths are smaller parts."], ['Comparing only the numerators', 'Rename with the same denominator first.'], ['Different wholes', 'Half of a big pizza is more than half of a small one.']])
    faq = [('What does MATATAG Math 4 ask about dissimilar fractions?', 'Represent dissimilar fractions with denominators up to 10 using models, compare them using the symbols =, >, and <, and order them from smallest to largest, and vice versa.'), ('What is a common denominator?', 'A number that both denominators divide into, like 12 for thirds and fourths.'), ('Which is bigger, 3/5 or 3/8?', '3/5, because fifths are bigger parts than eighths.'), ('Can two different fractions be equal?', 'Yes. 2/4 and 1/2 are equivalent.')]
    make('comparing-and-ordering-dissimilar-fractions', 15, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Represent dissimilar fractions, with denominators up to 10, using models; compare dissimilar fractions using the symbols =, >, and <; order dissimilar fractions from smallest to largest, and vice versa.',
         'Comparing and Ordering Dissimilar Fractions', 'Comparing Dissimilar Fractions',
         'Free Grade 4 worksheets on comparing and ordering dissimilar fractions for the DepEd MATATAG curriculum: models, common denominators, ordering and word problems. 100 questions with answers.',
         'Rename with a common denominator, then compare the numerators.', 'Same numerator: smaller denominator, bigger fraction.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
