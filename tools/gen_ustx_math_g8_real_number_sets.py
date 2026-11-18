# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Sets of Real Numbers: Rational and Irrational (TEKS 8.2A)
  python3 tools/gen_ustx_math_g8_real_number_sets.py
Classifying real numbers with a Venn diagram, rational or irrational, fractions and repeating decimals, and true or
false statements about the sets (US Grade 8 makers with a new seed, plus own makers).
Wrong answers come from real mistakes: thinking every square root is irrational, thinking repeating decimals are
irrational, and thinking π = 3.14 exactly.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_rational_and_irrational_numbers as rai
adopt(rai)
rai.R = random.Random(680010)
tx_common.GRADE = "grade-8"

import math
from fractions import Fraction as F
from ws_common import num


def sq(n):
    return "√%d" % n


def realval(s):
    return s[1]

INK = "#1f2937"
VENN = ("<svg viewBox='0 0 380 230' width='380' role='img' aria-label='Venn diagram of the real numbers'>"
        "<rect x='5' y='5' width='370' height='220' rx='18' fill='#f8fafc' stroke='%s' stroke-width='2'/>"
        "<rect x='15' y='32' width='245' height='185' rx='16' fill='#eff6ff' stroke='%s' stroke-width='2'/>"
        "<rect x='70' y='62' width='182' height='147' rx='14' fill='#dbeafe' stroke='%s' stroke-width='2'/>"
        "<rect x='125' y='92' width='120' height='109' rx='12' fill='#bfdbfe' stroke='%s' stroke-width='2'/>"
        "<rect x='160' y='122' width='78' height='70' rx='10' fill='#93c5fd' stroke='%s' stroke-width='2'/>"
        "<rect x='270' y='32' width='97' height='185' rx='16' fill='#fef3c7' stroke='%s' stroke-width='2'/>"
        "<text x='190' y='24' font-size='13' text-anchor='middle' fill='%s'>Real numbers</text>"
        "<text x='137' y='52' font-size='12' text-anchor='middle' fill='%s'>Rational</text>"
        "<text x='161' y='81' font-size='12' text-anchor='middle' fill='%s'>Integers</text>"
        "<text x='185' y='111' font-size='12' text-anchor='middle' fill='%s'>Whole</text>"
        "<text x='199' y='140' font-size='12' text-anchor='middle' fill='%s'>Natural</text>"
        "<text x='199' y='170' font-size='12' text-anchor='middle' fill='%s'>1, 2, 3</text>"
        "<text x='42' y='130' font-size='12' text-anchor='middle' fill='%s'>2/3</text>"
        "<text x='318' y='52' font-size='12' text-anchor='middle' fill='%s'>Irrational</text>"
        "<text x='318' y='110' font-size='13' text-anchor='middle' fill='%s'>π</text>"
        "<text x='318' y='150' font-size='13' text-anchor='middle' fill='%s'>√2</text></svg>") % ((INK,) * 16)

ST = ["Natural, whole, integer, rational and real", "Whole, integer, rational and real only", "Integer, rational and real only", "Rational and real only", "Irrational and real only"]
NONSQ = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50]


def pick(r, k):
    if k == 0:
        return r.choice([str(r.randint(1, 60)), "√%d" % (r.randint(2, 12) ** 2)])
    if k == 1:
        return r.choice(["0", "√0"])
    if k == 2:
        return r.choice([num(-r.randint(1, 60)), "−√%d" % (r.randint(2, 12) ** 2)])
    if k == 3:
        t = r.choice(["f", "d", "rep"])
        if t == "f":
            b = r.choice([3, 4, 5, 7, 8, 9])
            return ("−" if r.random() < 0.5 else "") + fr(r.randint(1, b - 1), b)
        if t == "d":
            return ("−" if r.random() < 0.5 else "") + "%d.%d" % (r.randint(0, 9), r.randint(1, 9))
        return r.choice(["0.<span class='ov'>3</span>", "1.<span class='ov'>27</span>", "−2.<span class='ov'>6</span>", "0.1<span class='ov'>6</span>"])
    return r.choice(["√%d" % r.choice(NONSQ), "π", "−√%d" % r.choice(NONSQ), "2π", "π ÷ 2"])


def one_classify(r):
    k = r.choice([0, 1, 2, 3, 3, 4, 4, 4])
    p = pick(r, k)
    pic = figure(VENN, "Rational and irrational numbers together make the real numbers.") if r.random() < 0.3 else ""
    why = ["%s is a counting number." % p, "%s is 0: whole, but not natural." % p, "%s is a negative integer." % p,
           "%s can be written as a fraction of integers, so it is rational, but it is not an integer." % p,
           "%s cannot be written as a fraction of integers: its decimal never ends or repeats. It is irrational." % p][k]
    return mcq(pic + "Which sets does %s belong to?" % p, ST[k], r.sample([s for i, s in enumerate(ST) if i != k], 3), why)


def one_true(r):
    facts = [("Every real number is either rational or irrational.", True), ("√9 is a rational number.", True), ("√10 is an irrational number.", True),
             ("π is exactly 3.14.", False), ("Every square root is irrational.", False), ("A repeating decimal is irrational.", False),
             ("Every integer is a real number.", True), ("Some irrational numbers are integers.", False), ("Every whole number is a natural number.", False),
             ("The decimal for an irrational number never ends and never repeats.", True)]
    tr = [f for f, t in facts if t]
    fl = [f for f, t in facts if not t]
    if r.random() < 0.6:
        right = r.choice(tr)
        return mcq("Which statement is true?", right, r.sample(fl, 3), "<b>%s</b>" % right)
    right = r.choice(fl)
    return mcq("Which statement is <b>false</b>?", right, r.sample(tr, 3), "<b>%s</b> is false." % right[:-1])


def build():
    sets, R = build_sets([
        ("Which sets does the number belong to?", [("collect", one_classify, 20)]),
        ("Rational or irrational?", [("run", rai.set_classify, (), 20)]),
        ("Fractions as decimals", [("run", rai.set_to_dec, (), 20)]),
        ("Repeating decimals to fractions", [("run", rai.set_to_frac, (), 20)]),
        ("True or false about the number sets", [("collect", one_true, 20)]),
    ], 68001)
    finish(sets, R)
    body = lesson('<ul><li>The <b>real numbers</b> are all the rational and irrational numbers.</li><li><b>Rational</b>: can be written as a fraction of integers. Terminating and repeating decimals are rational, and so are perfect-square roots like √49 = 7.</li><li><b>Irrational</b>: the decimal never ends and never repeats, such as π, √2 and √50.</li><li>Inside the rationals: integers ⊃ whole numbers ⊃ natural numbers.</li></ul>',
        [example("Classify √36.", ["√36 = 6"], "natural, whole, integer, rational, real"), example("Classify √20.", ["20 is not a perfect square"], "irrational, real")],
        [['Thinking every square root is irrational', '√49 = 7 is rational.'], ['Thinking repeating decimals are irrational', '0.333… = 1/3 is rational.'], ['Thinking π = 3.14 exactly', '3.14 is only an approximation; π is irrational.']])
    faq = [('What does TEKS 8.2A ask?', 'Extend previous knowledge of sets and subsets using a visual representation to describe relationships between sets of real numbers.'), ('Can a number be rational and irrational?', 'No. Every real number is one or the other.'), ('Is √0.25 rational?', 'Yes. √0.25 = 0.5.'), ('How do I know if √n is rational?', 'For a whole number n, √n is rational only if n is a perfect square.')]
    make('sets-of-real-numbers', 1, 'Number and Operations', '8.2A',
         '8.2A extend previous knowledge of sets and subsets using a visual representation to describe relationships between sets of real numbers',
         'Sets of Real Numbers: Rational and Irrational', 'Sets of Real Numbers',
         'Free Grade 8 worksheets for Texas TEKS 8.2A: classify real numbers with a Venn diagram, rational and irrational numbers, repeating decimals and number set facts. 100 questions with answers.',
         'Real numbers = rational + irrational.', '√49 = 7 is rational; √50 and π are irrational.',
         body, faq, sets, seo_title='Grade 8 Sets of Real Numbers Worksheets: Rational and Irrational (TEKS 8.2A, STAAR)')


if __name__ == "__main__":
    build()
