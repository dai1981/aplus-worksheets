# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Adding and Subtracting Fractions and Mixed Numbers, and Fractions of Whole Numbers (Grade 5: 1.2 Common fractions)
  python3 tools/gen_za_maths_g5_add_sub_fractions.py
Adding and subtracting fractions with the same denominator and mixed numbers (UK Year 5 makers), fractions of whole
numbers and the link between division and fractions (own makers), and word problems.
Wrong answers come from real mistakes: adding the denominators, forgetting to regroup a whole in a mixed number, and
dividing by the numerator when finding a fraction of a number.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_add_sub_fractions as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(805100)
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


def one_fow(r):
    d = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    n = r.randint(1, d - 1)
    if __import__("math").gcd(n, d) > 1:
        raise AssertionError
    k = r.randint(2, 12)
    w = d * k
    if r.random() < 0.65:
        right = n * k
        return mcq("What is %s of %d?" % (fr(n, d), w), right, [k, w // n if w % n == 0 and w // n != right else right + n, w - right if w - right != right else right + k],
                   "%d ÷ %d = %d, and %d × %d = <b>%d</b>." % (w, d, k, k, n, right))
    kk = Kid(r).next()
    what = r.choice(["learners in a class", "sweets in a packet", "rand in a money box", "pages in a book"])
    q = "There are %d %s. %s of them are %s. How many is that?" % (w, what, fr(n, d), r.choice(["used", "taken", "spent", "read"]) if "learners" not in what else "girls")
    if "rand" in what:
        q = "%s has R%d in a money box and spends %s of it. How much does %s spend?" % (kk["n"], w, fr(n, d), kk["he"])
        return mcq(q, "R%d" % (n * k), ["R%d" % x for x in (k, w - n * k if w - n * k != n * k else n * k + 1, n * d)], "R%d ÷ %d = R%d. R%d × %d = <b>R%d</b>." % (w, d, k, k, n, n * k))
    return mcq(q, n * k, [k, w - n * k if w - n * k != n * k else n * k + 1, n * d if n * d != n * k else n * k + 2], "%d ÷ %d = %d. %d × %d = <b>%d</b>." % (w, d, k, k, n, n * k))


def one_divfr(r):
    a, b = r.randint(1, 11), r.randint(2, 12)
    if a >= b:
        raise AssertionError
    kind = r.choice(["div", "share"])
    if kind == "div":
        return mcq("Which fraction is the same as <b>%d ÷ %d</b>?" % (a, b), fr(a, b), [fr(b, a), fr(a, b + a), fr(a + 1, b)], "Dividing %d by %d is the same as %s." % (a, b, fr(a, b)) + " <b>%s</b>." % fr(a, b))
    what = r.choice(["pizzas", "loaves of bread", "slabs of chocolate", "melkterts"])
    return mcq("%d %s are shared equally among %d friends. How much does each friend get?" % (a, what, b) if a > 1 else "1 of the %s is shared equally among %d friends. How much does each friend get?" % (what, b),
               "%s of a %s" % (fr(a, b), what[:-1] if what != "loaves of bread" else "loaf"), ["%s of a %s" % (x, what[:-1] if what != "loaves of bread" else "loaf") for x in (fr(b, a), fr(1, b) if a != 1 else fr(1, b + 1), fr(a, b * 2))],
               "%d ÷ %d = %s. Each friend gets <b>%s</b>." % (a, b, fr(a, b), fr(a, b)))

def mx(w, n, d):
    return ("%d " % w if w else "") + fr(n, d) if n else str(w)


def one_mixed(r):
    d = r.randint(3, 12)
    a, b = r.randint(1, 5), r.randint(1, d - 1)
    c, e = r.randint(1, 4), r.randint(1, d - 1)
    if r.random() < 0.5:
        t = b + e
        w, n = a + c + t // d, t % d
        if n == 0:
            raise AssertionError
        right = mx(w, n, d)
        wr = [mx(a + c, t, d) if t >= d else mx(a + c, t, 2 * d), mx(a + c, t % d, d) if t >= d else mx(a + c + 1, t, d), mx(w, n, 2 * d)]
        ex = "Add the wholes: %d + %d = %d. Add the fractions: %s." % (a, c, a + c, fr(t, d)) + (" %s = 1 %s, so regroup." % (fr(t, d), fr(t - d, d)) if t >= d else "") + " Answer: <b>%s</b>." % right
        return mcq("%s + %s = ?" % (mx(a, b, d), mx(c, e, d)), right, wr, ex)
    if a <= c:
        a, c = c + 1, a
    t = (a * d + b) - (c * d + e)
    w, n = t // d, t % d
    if n == 0 or w == 0:
        raise AssertionError
    right = mx(w, n, d)
    wr = [mx(a - c, abs(b - e), d) if abs(b - e) and mx(a - c, abs(b - e), d) != right else mx(w + 1, n, d), mx(w, n, 2 * d), mx(w + 1, n, d) if b < e else mx(w - 1, n, d) if w > 1 else mx(w, d - n, d)]
    ex = ("%s is smaller than %s, so regroup 1 whole: %s = %s. " % (fr(b, d), fr(e, d), mx(a, b, d), mx(a - 1, b + d, d)) if b < e else "") + "Answer: <b>%s</b>." % right
    return mcq("%s − %s = ?" % (mx(a, b, d), mx(c, e, d)), right, wr, ex)


def build():
    sets, R = build_sets([
        ("Add and subtract fractions", [("run", ukf.set_same, ("rnd", ukf.People), 15, den12), ("run", ukf.set_related, ("rnd",), 5, den12)]),
        ("Improper fractions and mixed numbers", [("run", ukf.set_improper, ("rnd",), 20, den12)]),
        ("Add and subtract mixed numbers", [("collect", uniq(one_mixed), 12), ("run", ukf.set_mixed, ("rnd",), 8, lambda it: den12(it) and len(set(_re.findall(r"<span class='fd'>(\d+)</span>", it["q"]))) <= 1)]),
        ("Fractions of whole numbers", [("collect", uniq(one_fow), 20)]),
        ("Division and fractions", [("collect", uniq(one_divfr), 10), ("run", ukf.set_words, ("rnd", ukf.People), 10, lambda it: den12(it) and len(set(_re.findall(r"<span class='fd'>(\d+)</span>", it["q"]))) <= 1)]),
    ], 80510)
    finish(sets, R)
    body = lesson("<ul><li>Fractions with the same denominator: add or subtract the numerators and keep the denominator.</li><li>Mixed numbers: add the wholes and the fractions. If the fraction part is 1 or more, regroup it as a whole.</li><li>Fraction of a whole number: divide by the denominator, multiply by the numerator. <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> of 40: 40 ÷ 5 × 3 = 24.</li><li>Division and fractions: 3 ÷ 4 = <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>.</li></ul>",
        [example("2 <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> + 1 <span class='fr'><span class='fn'>4</span><span class='fd'>5</span></span>", ["3 + <span class='fr'><span class='fn'>7</span><span class='fd'>5</span></span>", "<span class='fr'><span class='fn'>7</span><span class='fd'>5</span></span> = 1 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>"], "4 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>")],
        [['Adding denominators', 'Keep the denominator.'], ['Not regrouping', '7/5 = 1 2/5.'], ['Dividing by the numerator', 'Divide by the denominator first.']])
    faq = [('What does CAPS Grade 5 say about fraction calculations?', 'Add and subtract common fractions with the same denominators and mixed numbers, and find fractions of whole numbers which result in whole numbers.'), ('How do I find 2/3 of 18?', '18 ÷ 3 = 6, 6 × 2 = 12.'), ('Is 5 ÷ 8 the same as 5/8?', 'Yes.'), ('What is regrouping?', 'Changing an improper fraction part into a whole.')]
    make('adding-and-subtracting-fractions', 10, 'Numbers, Operations and Relationships', 'Grade 5: 1.2 Common fractions',
         'Add and subtract common fractions in which one denominator is a multiple of another and mixed numbers (same denominators); solve problems involving common fractions, including grouping and equal sharing; find fractions of whole numbers which result in whole numbers; recognise, describe and use the equivalence of division and fractions.',
         'Adding and Subtracting Fractions and Mixed Numbers, and Fractions of Whole Numbers', 'Fraction Calculations',
         'Free CAPS Grade 5 fraction worksheets: adding and subtracting fractions and mixed numbers, fractions of whole numbers and division as fractions. 100 questions with memos.',
         'Same denominator: add the numerators.', 'Fraction of a number: ÷ denominator, × numerator.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
