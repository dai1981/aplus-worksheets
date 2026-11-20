# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Common Fractions: Comparing, Ordering and Equivalent Fractions to Twelfths (Grade 5: 1.2 Common fractions)
  python3 tools/gen_za_maths_g5_fractions.py
Equivalent fractions, comparing and ordering fractions to twelfths, mixed numbers (Australia Year 5 makers) and
fractions in diagrams (UK Year 5 maker).
Wrong answers come from real mistakes: thinking a bigger denominator means a bigger fraction, changing only the
numerator, and ordering by the numerators only.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y5_compare_fractions as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(805090)
import gen_uk_maths_y5_equivalent_fractions as uke
adopt(uke)
if isinstance(getattr(uke, 'R', None), random.Random): uke.R = random.Random(805091)
za_common.GRADE = "grade-5"

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


def one_eqmiss(r):
    a, b = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 6), (5, 6)])
    k = r.choice([x for x in (2, 3, 4, 6) if b * x <= 12])
    if r.random() < 0.5:
        return mcq("%s = <span class='fr'><span class='fn'>☐</span><span class='fd'>%d</span></span>. What is ☐?" % (fr(a, b), b * k), a * k, [a + (b * k - b), a * k + 1 if a * k + 1 != b * k else a, a * k - 1 if a * k > 1 else a * k + 2],
                   "%d × %d = %d, so multiply the numerator by %d too: %d × %d = <b>%d</b>." % (b, k, b * k, k, a, k, a * k))
    return mcq("%s = <span class='fr'><span class='fn'>%d</span><span class='fd'>☐</span></span>. What is ☐?" % (fr(a, b), a * k), b * k, [b + (a * k - a), b * k + 1, b * k - 1],
               "%d × %d = %d, so multiply the denominator by %d too: %d × %d = <b>%d</b>." % (a, k, a * k, k, b, k, b * k))


def build():
    sets, R = build_sets([
        ("Fractions in diagrams", [("run", uke.set_diagrams, ("rnd",), 12, den12), ("run", auc.set_words, ("rnd",), 8, den12)]),
        ("Equivalent fractions", [("run", auc.set_equivalent, ("rnd",), 10, den12), ("run", uke.set_missing, ("rnd",), 5, den12), ("collect", uniq(one_eqmiss), 5)]),
        ("Compare fractions", [("run", auc.set_compare, ("rnd",), 15, den12), ("run", uke.set_compare, ("rnd",), 5, den12)]),
        ("Order fractions", [("run", auc.set_order, ("rnd",), 20, den12)]),
        ("Mixed numbers", [("run", auc.set_mixed, ("rnd",), 10, den12), ("run", uke.set_mixed, ("rnd",), 10, den12)]),
    ], 80509)
    finish(sets, R)
    body = lesson("<ul><li>Fractions in Grade 5 go up to twelfths.</li><li>Equivalent fractions: multiply or divide the numerator and denominator by the same number: <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> = <span class='fr'><span class='fn'>8</span><span class='fd'>12</span></span>.</li><li>To compare, give the fractions the same denominator first.</li><li>A <b>mixed number</b> has a whole number and a fraction: 2 <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>.</li></ul>",
        [example("Compare <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> and <span class='fr'><span class='fn'>5</span><span class='fd'>8</span></span>", ["<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> = <span class='fr'><span class='fn'>6</span><span class='fd'>8</span></span>", "6 &gt; 5"], "<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> &gt; <span class='fr'><span class='fn'>5</span><span class='fd'>8</span></span>")],
        [['Bigger denominator, bigger fraction', 'Twelfths are smaller than sixths.'], ['Changing one number', 'Do the same to the top and bottom.'], ['Ordering by numerators', 'Use the same denominator first.']])
    faq = [('What does CAPS Grade 5 say about fractions?', 'Count, compare and order common fractions to at least twelfths, recognise equivalent fractions where one denominator is a multiple of the other, and work with mixed numbers.'), ('Are 3/6 and 1/2 equivalent?', 'Yes.'), ('What is an improper fraction?', 'A fraction bigger than 1, like 7/4.'), ('Which is bigger, 5/12 or 1/2?', '1/2 = 6/12, so 1/2.')]
    make('common-fractions', 9, 'Numbers, Operations and Relationships', 'Grade 5: 1.2 Common fractions',
         'Count forwards and backwards in fractions; compare and order common fractions to at least twelfths; recognise, describe and use the equivalence of division and fractions; recognise and use equivalent forms of common fractions with 1-digit or 2-digit denominators (fractions where one denominator is a multiple of the other).',
         'Common Fractions: Comparing, Ordering and Equivalent Fractions to Twelfths', 'Common Fractions',
         'Free CAPS Grade 5 common fractions worksheets: fractions to twelfths, equivalent fractions, comparing, ordering and mixed numbers. 100 questions with memos.',
         'Same denominator first, then compare.', 'Equivalent: multiply top and bottom by the same number.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
