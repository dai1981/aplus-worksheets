# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Whole Numbers, Integers and Rational Numbers (TEKS 6.2A, 6.2B)
  python3 tools/gen_ustx_math_g6_integers_rational.py
Classifying numbers as whole numbers, integers and rational numbers with a Venn diagram, picking a number from a
set, positive and negative numbers in real life, opposites, and absolute value (the US Grade 6 makers with Texas
names, plus own makers).
Wrong answers come from real mistakes: thinking negative numbers are not integers, thinking fractions are not
rational, and giving a negative absolute value.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_negative_numbers as nn
import gen_us_math_g6_absolute_value as av
adopt(nn)
adopt(av)
from ws_common import num
from fractions import Fraction as F
tx_common.GRADE = "grade-6"

VENN = ("<svg viewBox='0 0 340 200' width='340' role='img' aria-label='Venn diagram: whole numbers inside integers inside rational numbers'>"
        "<rect x='5' y='5' width='330' height='190' rx='20' fill='#eff6ff' stroke='#1f2937' stroke-width='2'/>"
        "<rect x='60' y='45' width='240' height='140' rx='18' fill='#dbeafe' stroke='#1f2937' stroke-width='2'/>"
        "<rect x='130' y='85' width='160' height='90' rx='16' fill='#bfdbfe' stroke='#1f2937' stroke-width='2'/>"
        "<text x='170' y='28' font-size='15' text-anchor='middle' fill='#1f2937'>Rational numbers</text>"
        "<text x='180' y='68' font-size='15' text-anchor='middle' fill='#1f2937'>Integers</text>"
        "<text x='210' y='108' font-size='15' text-anchor='middle' fill='#1f2937'>Whole numbers</text>"
        "<text x='210' y='150' font-size='15' text-anchor='middle' fill='#1f2937'>0, 1, 2, 3, …</text>"
        "<text x='95' y='130' font-size='15' text-anchor='middle' fill='#1f2937'>−1, −2, …</text>"
        "<text x='32' y='110' font-size='14' text-anchor='middle' fill='#1f2937'>1/2</text>"
        "<text x='32' y='150' font-size='14' text-anchor='middle' fill='#1f2937'>−0.7</text></svg>")

ST = ["It is a whole number, an integer and a rational number.", "It is an integer and a rational number, but not a whole number.",
      "It is a rational number, but not an integer.", "It is a whole number, but not a rational number."]


def pick(r, kind):
    if kind == 0:
        v = r.randint(0, 60)
        return v, str(v)
    if kind == 1:
        v = -r.randint(1, 60)
        return v, num(v)
    t = r.choice(["f", "d", "nf", "nd", "m"])
    if t in ("f", "nf"):
        b = r.choice([2, 3, 4, 5, 6, 8, 10])
        a = r.randint(1, b - 1)
        if F(a, b).denominator != b:
            return None
        return (-1 if t == "nf" else 1) * F(a, b), ("−" if t == "nf" else "") + fr(a, b)
    if t == "m":
        b, w = r.choice([2, 3, 4]), r.randint(1, 5)
        return w + F(1, b), "%d%s" % (w, fr(1, b))
    v = r.randint(1, 99) / 10.0
    if v == int(v):
        return None
    return v, ("−" if t == "nd" else "") + ("%.1f" % v)


def one_classify(r):
    k = r.choice([0, 1, 1, 2, 2])
    p = pick(r, k)
    if not p:
        return None
    pic = figure(VENN, "Whole numbers are inside the integers, and integers are inside the rational numbers.") if r.random() < 0.3 else ""
    why = ["%s is a counting number or 0, so it is in all three sets." % p[1], "%s is a negative whole number: an integer, and every integer is rational. It is not a whole number." % p[1],
           "%s can be written as a fraction, so it is rational, but it is not a whole number or its opposite, so it is not an integer." % p[1]][k]
    return mcq(pic + "Which statement about %s is true?" % p[1], ST[k], [s for i, s in enumerate(ST) if i != k], why)


def one_which(r):
    k = r.choice([0, 1, 2])
    want = ["a whole number", "an integer but not a whole number", "a rational number but not an integer"][k]
    right = pick(r, k)
    others = [pick(r, j) for j in range(3) if j != k]
    others.append(pick(r, r.choice([j for j in range(3) if j != k])))
    if not right or not all(others) or len({o[1] for o in others} | {right[1]}) < 4:
        return None
    return mcq("Which number is %s?" % want, right[1], [o[1] for o in others], "<b>%s</b> is %s." % (right[1], want))


def build():
    sets, R = build_sets([
        ("Whole numbers, integers or rational numbers?", [("collect", one_classify, 20)]),
        ("Find a number in each set", [("collect", one_which, 20)]),
        ("Positive and negative numbers in real life", [("run", nn.set_situations, ("rnd", nn.People), 20)]),
        ("Opposites", [("run", nn.set_opposites, ("rnd", nn.People), 20)]),
        ("Absolute value", [("run", av.set_abs, ("rnd", av.People), 20)]),
    ], 66001)
    finish(sets, R)
    body = lesson('<ul><li><b>Whole numbers</b>: 0, 1, 2, 3, …</li><li><b>Integers</b>: the whole numbers and their opposites: ..., −2, −1, 0, 1, 2, ...</li><li><b>Rational numbers</b>: any number that can be written as a fraction a/b, including integers, fractions and decimals like −0.7.</li><li>The <b>opposite</b> of a number is the same distance from 0 on the other side. <b>Absolute value</b> is the distance from 0, so it is never negative: |−8| = 8.</li></ul>',
        [example("Classify −12.", ["Not 0, 1, 2, ...", "It is the opposite of 12", "−12 = −12/1"], "integer and rational"), example("|−3.5|", ["Distance from 0"], "3.5")],
        [['Thinking negative numbers are not integers', '−5 is an integer; it is the opposite of 5.'], ['Thinking fractions are not rational', 'Every fraction and terminating decimal is rational.'], ['Giving a negative absolute value', 'Distance is never negative: |−8| = 8.']])
    faq = [('What does TEKS 6.2A ask?', 'Classify whole numbers, integers and rational numbers using a visual representation such as a Venn diagram to describe relationships between sets of numbers.'), ('What does TEKS 6.2B ask?', 'Identify a number, its opposite and its absolute value.'), ('Is 0 a whole number?', 'Yes. 0 is a whole number, an integer and a rational number.'), ('Is every integer a rational number?', 'Yes. Any integer n can be written as n/1.')]
    make('integers-and-rational-numbers', 1, 'Number and Operations', '6.2A, 6.2B',
         '6.2A classify whole numbers, integers, and rational numbers using a visual representation such as a Venn diagram to describe relationships between sets of numbers; 6.2B identify a number, its opposite, and its absolute value',
         'Whole Numbers, Integers and Rational Numbers', 'Integers and Rational Numbers',
         'Free Grade 6 worksheets for Texas TEKS 6.2A and 6.2B: classify whole numbers, integers and rational numbers with a Venn diagram, opposites, absolute value and real-life negative numbers. 100 questions with answers.',
         'Whole numbers ⊂ integers ⊂ rational numbers.', '−5 is an integer; 1/2 and −0.7 are rational but not integers. |−8| = 8.',
         body, faq, sets, seo_title='Grade 6 Integers and Rational Numbers Worksheets: Venn Diagram, Opposites and Absolute Value (TEKS 6.2A, 6.2B, STAAR)')


if __name__ == "__main__":
    build()
