# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Fractions of Whole Numbers and Multiplying Fractions by Whole Numbers (Grade 6: 1.2 Common fractions)
  python3 tools/gen_za_maths_g6_fractions_of_amounts.py
Fractions of whole numbers and amounts, multiplying a fraction by a whole number, fractions and division, and
problems (own makers, UK Year 6 and Ontario Grade 6 makers).
Wrong answers come from real mistakes: dividing by the numerator, multiplying the denominator as well, and giving the
part that is left instead of the part asked for.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_mult_div_fractions as ukm
adopt(ukm)
if isinstance(getattr(ukm, 'R', None), random.Random): ukm.R = random.Random(806110)
import gen_caon_math_g6_mult_div_fractions as cam
adopt(cam)
if isinstance(getattr(cam, 'R', None), random.Random): cam.R = random.Random(806111)
import gen_za_maths_g5_add_sub_fractions as zf5
adopt(zf5)
if isinstance(getattr(zf5, 'R', None), random.Random): zf5.R = random.Random(806112)
za_common.GRADE = "grade-6"

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


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)


def one_fow6(r):
    d = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    n = r.randint(1, d - 1)
    if __import__("math").gcd(n, d) > 1:
        raise AssertionError
    k = r.randint(12, 120)
    w = d * k
    right = n * k
    return mcq("What is %s of %s?" % (fr(n, d), comma(w)), comma(right), [comma(k), comma(w - right) if w - right != right else comma(right + n), comma(w * n)],
               "%s ÷ %d = %s, and %s × %d = <b>%s</b>." % (comma(w), d, comma(k), comma(k), n, comma(right)))


def one_fstory(r):
    kk = Kid(r).next()
    d = r.choice([3, 4, 5, 6, 8, 10])
    n = r.randint(1, d - 1)
    if __import__("math").gcd(n, d) > 1:
        raise AssertionError
    k = r.randint(5, 60)
    w = d * k
    t = r.choice([("%s has R%s and spends %s of it on a school bag. How much does the bag cost?", "R"),
                  ("A farm has %s sheep. %s of them are black. How many sheep are black?", ""),
                  ("A school has %s learners. %s of them walk to school. How many learners walk?", ""),
                  ("A tank holds %s ℓ of water. %s of the water is used. How many litres are used?", " ℓ")])
    if t[1] == "R":
        q = t[0] % (kk["n"], comma(w), fr(n, d))
        f = lambda v: "R" + comma(v)
    else:
        q = t[0] % (comma(w), fr(n, d))
        f = lambda v: comma(v) + t[1]
    return mcq(q, f(n * k), [f(k), f(w - n * k) if w - n * k != n * k else f(n * k + 1), f(n * d)],
               "%s ÷ %d = %s. %s × %d = <b>%s</b>." % (comma(w), d, comma(k), comma(k), n, f(n * k)))


def one_ftimes(r):
    d = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    n = r.randint(1, d - 1)
    w = r.randint(2, 12)
    t = n * w
    whole, rem = divmod(t, d)
    g = __import__("math").gcd(rem, d) if rem else d
    right = (str(whole) + " " if whole else "") + (fr(rem // g, d // g) if rem else "") if rem else str(whole)
    wr = [fr(t, d * w), fr(n * w, d * w) if n * w != t else fr(n + w, d), fr(n + w, d)]
    wr = [x for x in dict.fromkeys(wr) if x != right]
    if not whole and not rem:
        raise AssertionError
    return mcq("%d × %s = ?" % (w, fr(n, d)), right, wr + [str(whole + 1)],
               "%d × %s = %s%s. Answer: <b>%s</b>." % (w, fr(n, d), fr(t, d), (" = " + right) if t >= d or g > 1 else "", right))


def build():
    sets, R = build_sets([
        ("Fractions of whole numbers", [("collect", uniq(one_fow6), 20)]),
        ("Fractions of amounts", [("run", ukm.set_amounts, (), 10, den12), ("run", cam.set_quantity, (), 10, den12)]),
        ("Whole number × fraction", [("collect", uniq(one_ftimes), 20)]),
        ("Fractions and division", [("collect", zf5.uniq(zf5.one_divfr), 20)]),
        ("Fraction problems", [("collect", uniq(one_fstory), 20)]),
    ], 80611)
    finish(sets, R)
    body = lesson("<ul><li>To find a fraction of a number, divide by the denominator and multiply by the numerator.</li><li><span class='fr'><span class='fn'>3</span><span class='fd'>8</span></span> of 240: 240 ÷ 8 = 30, 30 × 3 = 90.</li><li>Whole number × fraction: multiply the numerator. 5 × <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> = <span class='fr'><span class='fn'>10</span><span class='fd'>3</span></span> = 3 <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>.</li><li>Division is a fraction: 3 ÷ 4 = <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>.</li></ul>",
        [example("<span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span> of R350", ["R350 ÷ 5 = R70", "R70 × 2"], "R140")],
        [['Dividing by the numerator', 'Divide by the denominator first.'], ['Multiplying the bottom', 'Only the numerator is multiplied.'], ['The part left', 'Read what the question asks for.']])
    faq = [('What does CAPS Grade 6 say about fractions of whole numbers?', 'Find fractions of whole numbers, and multiply common fractions and mixed numbers by whole numbers.'), ('What is 3/4 of 100?', '75.'), ('Is 4 × 1/4 = 1?', 'Yes.'), ('Why divide by the denominator?', 'It finds one equal part.')]
    make('fractions-of-whole-numbers', 11, 'Numbers, Operations and Relationships', 'Grade 6: 1.2 Common fractions',
         'Find fractions of whole numbers; multiply common fractions and mixed numbers by whole numbers; recognise, describe and use the equivalence of division and fractions.',
         'Fractions of Whole Numbers and Multiplying Fractions by Whole Numbers', 'Fractions of Whole Numbers',
         'Free CAPS Grade 6 worksheets: fractions of whole numbers and amounts, multiplying fractions by whole numbers and fraction problems. 100 questions with memos.',
         '÷ by the denominator, × by the numerator.', 'Whole number × fraction: multiply the numerator.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
