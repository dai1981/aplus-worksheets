# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Sets of Rational Numbers: Natural, Whole, Integers and Rational (TEKS 7.2)
  python3 tools/gen_ustx_math_g7_rational_number_sets.py
Classifying numbers as natural numbers, whole numbers, integers and rational numbers with a Venn diagram, finding a
number in each set, terminating and repeating decimals, and comparing rational numbers (US Grade 7 makers with a
new seed, plus own makers).
Wrong answers come from real mistakes: calling 0 a natural number, thinking repeating decimals are not rational,
and thinking negative fractions are integers.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_converting_fractions_to_decimals as cfd
adopt(cfd)
cfd.R = random.Random(670010)
from fractions import Fraction as F
from ws_common import num
tx_common.GRADE = "grade-7"

INK = "#1f2937"
VENN = ("<svg viewBox='0 0 360 220' width='360' role='img' aria-label='Venn diagram: natural numbers inside whole numbers inside integers inside rational numbers'>"
        "<rect x='5' y='5' width='350' height='210' rx='20' fill='#eff6ff' stroke='%s' stroke-width='2'/>"
        "<rect x='70' y='38' width='275' height='170' rx='18' fill='#dbeafe' stroke='%s' stroke-width='2'/>"
        "<rect x='150' y='72' width='185' height='126' rx='16' fill='#bfdbfe' stroke='%s' stroke-width='2'/>"
        "<rect x='210' y='106' width='115' height='82' rx='14' fill='#93c5fd' stroke='%s' stroke-width='2'/>"
        "<text x='180' y='26' font-size='14' text-anchor='middle' fill='%s'>Rational numbers</text>"
        "<text x='207' y='58' font-size='14' text-anchor='middle' fill='%s'>Integers</text>"
        "<text x='243' y='92' font-size='14' text-anchor='middle' fill='%s'>Whole numbers</text>"
        "<text x='268' y='126' font-size='13' text-anchor='middle' fill='%s'>Natural numbers</text>"
        "<text x='268' y='160' font-size='13' text-anchor='middle' fill='%s'>1, 2, 3, …</text>"
        "<text x='180' y='160' font-size='13' text-anchor='middle' fill='%s'>0</text>"
        "<text x='110' y='130' font-size='13' text-anchor='middle' fill='%s'>−1, −2, …</text>"
        "<text x='37' y='110' font-size='13' text-anchor='middle' fill='%s'>2/3</text>"
        "<text x='37' y='160' font-size='13' text-anchor='middle' fill='%s'>−0.25</text></svg>") % ((INK,) * 13)

ST = ["Natural number, whole number, integer and rational number", "Whole number, integer and rational number only", "Integer and rational number only", "Rational number only"]
WHY = ["%s is a counting number, so it belongs to all four sets.", "0 is a whole number but not a natural (counting) number.", "%s is a negative integer. It is not a whole number.", "%s can be written as a fraction, but it is not an integer."]


def pick(r, k):
    if k == 0:
        v = r.randint(1, 99)
        return str(v)
    if k == 1:
        return "0"
    if k == 2:
        return num(-r.randint(1, 99))
    t = r.choice(["f", "nf", "d", "nd", "rep", "m"])
    if t in ("f", "nf"):
        b = r.choice([3, 4, 5, 7, 8, 9])
        a = r.randint(1, b - 1)
        if F(a, b).denominator != b:
            return None
        return ("−" if t == "nf" else "") + fr(a, b)
    if t == "rep":
        return r.choice(["0.333…", "0.<span class='ov'>6</span>", "−1.<span class='ov'>3</span>", "2.<span class='ov'>18</span>", "0.<span class='ov'>45</span>"])
    if t == "m":
        return "−%d%s" % (r.randint(1, 9), fr(1, r.choice([2, 3, 4])))
    v = r.randint(1, 999) / 100.0
    if v == int(v):
        return None
    return ("−" if t == "nd" else "") + ("%.2f" % v).rstrip("0")


def one_classify(r):
    k = r.choice([0, 1, 2, 2, 3, 3, 3])
    p = pick(r, k)
    if not p:
        return None
    pic = figure(VENN, "Each set is inside the next one.") if r.random() < 0.3 else ""
    return mcq(pic + "Which sets does %s belong to?" % p, ST[k], [s for i, s in enumerate(ST) if i != k], WHY[k] % p if "%s" in WHY[k] else WHY[k])


def one_which(r):
    k = r.choice([0, 1, 2, 3])
    want = ["a natural number", "a whole number but not a natural number", "an integer but not a whole number", "a rational number but not an integer"][k]
    right = pick(r, k)
    others = []
    for j in [x for x in range(4) if x != k]:
        o = pick(r, j)
        if not o:
            return None
        others.append(o)
    if not right or len(set(others + [right])) < 4:
        return None
    return mcq("Which number is %s?" % want, right, others, "<b>%s</b> is %s." % (right, want))


def one_true(r):
    facts = [("Every integer is a rational number.", True), ("Every rational number is an integer.", False), ("Every natural number is a whole number.", True),
             ("Every whole number is a natural number.", False), ("Every whole number is an integer.", True), ("Some integers are not whole numbers.", True),
             ("A repeating decimal is a rational number.", True), ("Negative fractions are integers.", False), ("0 is a natural number.", False), ("0 is a rational number.", True)]
    tr = [f for f, t in facts if t]
    fl = [f for f, t in facts if not t]
    if r.random() < 0.6:
        right = r.choice(tr)
        return mcq("Which statement is true?", right, r.sample(fl, 3), "<b>%s</b> Look at the Venn diagram: each set is inside the next." % right)
    right = r.choice(fl)
    return mcq("Which statement is <b>false</b>?", right, r.sample(tr, 3), "<b>%s</b> is false. Check the Venn diagram of the number sets." % right[:-1])


def build():
    sets, R = build_sets([
        ("Which sets does the number belong to?", [("collect", one_classify, 20)]),
        ("Find a number in each set", [("collect", one_which, 14), ("collect", one_true, 6)]),
        ("Fractions as terminating decimals", [("run", cfd.set_terminating, (), 20)]),
        ("Repeating decimals are rational", [("run", cfd.set_repeating, (), 20)]),
        ("Compare and order rational numbers", [("run", cfd.set_compare, (), 20)]),
    ], 67001)
    finish(sets, R)
    body = lesson('<ul><li><b>Natural numbers</b> (counting numbers): 1, 2, 3, …</li><li><b>Whole numbers</b>: 0, 1, 2, 3, …</li><li><b>Integers</b>: … −2, −1, 0, 1, 2, …</li><li><b>Rational numbers</b>: any number that can be written as a fraction a/b, including terminating and repeating decimals. Each set is inside the next one.</li></ul>',
        [example("Classify −7.", ["Not a counting number or 0", "It is the opposite of 7"], "integer and rational"), example("Is 0.666… rational?", ["0.666… = 2/3"], "yes")],
        [['Calling 0 a natural number', 'Natural numbers start at 1. 0 is a whole number.'], ['Thinking repeating decimals are not rational', '0.333… = 1/3, so it is rational.'], ['Calling negative fractions integers', '−1/2 is rational but not an integer.']])
    faq = [('What does TEKS 7.2 ask?', 'Extend previous knowledge of sets and subsets using a visual representation to describe relationships between sets of rational numbers.'), ('Is every integer rational?', 'Yes. Any integer n can be written as n/1.'), ('What is the difference between natural and whole numbers?', 'Whole numbers include 0; natural numbers start at 1.'), ('Is π a rational number?', 'No. π cannot be written as a fraction of integers. You will study such numbers in Grade 8.')]
    make('sets-of-rational-numbers', 1, 'Number and Operations', '7.2',
         '7.2 extend previous knowledge of sets and subsets using a visual representation to describe relationships between sets of rational numbers',
         'Sets of Rational Numbers: Natural, Whole, Integers and Rational', 'Sets of Rational Numbers',
         'Free Grade 7 worksheets for Texas TEKS 7.2: classify natural numbers, whole numbers, integers and rational numbers with a Venn diagram, terminating and repeating decimals. 100 questions with answers.',
         'Natural ⊂ whole ⊂ integers ⊂ rational numbers.', '0 is whole but not natural. 0.333… = 1/3 is rational.',
         body, faq, sets, seo_title='Grade 7 Sets of Rational Numbers Worksheets: Venn Diagram (TEKS 7.2, STAAR)')


if __name__ == "__main__":
    build()
