# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Fractions, Decimals and Percents (TEKS 6.4E, 6.4F, 6.4G, 6.5C)
  python3 tools/gen_ustx_math_g6_fractions_decimals_percents.py
Percent as per 100 with grids, benchmark percents, converting between fractions, decimals and percents, comparing
and ordering numbers in different forms, and finding the form that is not equivalent (the US Grade 6 makers, plus
own makers).
Wrong answers come from real mistakes: writing 3/5 as 35%, moving the decimal point the wrong way, and comparing
digits instead of values.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_percents as pc
adopt(pc)
tx_common.GRADE = "grade-6"

from fractions import Fraction as F

NICE = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20), (7, 20), (9, 20), (11, 20),
        (1, 25), (3, 25), (6, 25), (12, 25), (1, 8), (3, 8), (5, 8), (7, 8), (5, 4), (3, 2), (7, 4), (6, 5), (1, 50), (13, 50)]


def dec(v):
    s = ("%.3f" % float(v)).rstrip("0").rstrip(".")
    return s


def pct(v):
    p = v * 100
    return (str(p.numerator) if p.denominator == 1 else dec(p)) + "%"


def frs(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    w, n = divmod(v.numerator, v.denominator)
    return (str(w) if w else "") + fr(n, v.denominator)


def one_convert(r):
    a, b = r.choice(NICE)
    v = F(a, b)
    kind = r.choice(["f2d", "f2p", "d2p", "p2f", "p2d", "d2f"])
    if kind == "f2d":
        return mcq("Write %s as a decimal." % fr(a, b), dec(v), [dec(F(a, b) / 10), "%d.%d" % (a, b), dec(F(b, a)) if a != 0 else "0"], "%s = %d ÷ %d = <b>%s</b>." % (fr(a, b), a, b, dec(v)))
    if kind == "f2p":
        return mcq("Write %s as a percent." % fr(a, b), pct(v), ["%d%%" % (a * 10 + b), pct(v / 10), pct(v * 10)], "%s = %s = <b>%s</b>." % (fr(a, b), dec(v), pct(v)))
    if kind == "d2p":
        return mcq("Write %s as a percent." % dec(v), pct(v), [pct(v / 100), pct(v / 10), pct(v * 10)], "Multiply by 100 (move the decimal point 2 places right): <b>%s</b>." % pct(v))
    if kind == "p2f":
        return mcq("Write %s as a fraction in simplest form." % pct(v), frs(v), [frs(v / 10), frs(1 - v) if v < 1 else frs(v - 1), frs(F(b, a))],
                   "%s = %s/100 = <b>%s</b>." % (pct(v), dec(v * 100), frs(v)))
    if kind == "p2d":
        return mcq("Write %s as a decimal." % pct(v), dec(v), [dec(v * 100), dec(v * 10), dec(v / 10)], "Divide by 100 (move the decimal point 2 places left): <b>%s</b>." % dec(v))
    return mcq("Write %s as a fraction in simplest form." % dec(v), frs(v), [frs(F(b, a)), fr(a, b * 10), frs(v + 1) if v < 1 else frs(v - 1)], "%s = <b>%s</b>." % (dec(v), frs(v)))


def form(r, v):
    t = r.choice(["f", "d", "p"])
    return {"f": frs(v), "d": dec(v), "p": pct(v)}[t]


def one_order(r):
    vals = r.sample(NICE, 4)
    vs = [F(a, b) for a, b in vals]
    if len(set(vs)) < 4:
        return None
    big = r.random() < 0.5
    t = max(vs) if big else min(vs)
    shown = [form(r, v) for v in vs]
    if len({s[-1] == "%" for s in shown}) == 1 and r.random() < 0.7:
        return None
    i = vs.index(t)
    return mcq("Which number is %s?" % ("greatest" if big else "least"), shown[i], [s for j, s in enumerate(shown) if j != i],
               "As decimals: %s. The %s is <b>%s</b>." % (", ".join(dec(v) for v in vs), "greatest" if big else "least", shown[i]))


def one_noteq(r):
    a, b = r.choice(NICE)
    v = F(a, b)
    good = [frs(v), dec(v), pct(v), fr(a * 2, b * 2) if b * 2 <= 100 else fr(a * 3, b * 3)]
    wrong = r.choice(["%d%%" % (a * 10 + b), dec(v / 10), "%d.%d" % (a, b), pct(v / 10)])
    if wrong in good:
        return None
    r.shuffle(good)
    return mcq("Three of these show the same part of a whole. Which one does <b>not</b>?", wrong, good[:3],
               "%s = %s = %s. <b>%s</b> is a different amount." % (frs(v), dec(v), pct(v), wrong))


def build():
    sets, R = build_sets([
        ("Percent means per 100", [("run", pc.set_per100, ("rnd",), 20)]),
        ("Benchmark percents", [("run", pc.set_bench, ("rnd",), 20)]),
        ("Convert fractions, decimals and percents", [("collect", one_convert, 20)]),
        ("Compare and order", [("collect", one_order, 20)]),
        ("Which one is not equivalent?", [("collect", one_noteq, 20)]),
    ], 66009)
    finish(sets, R)
    body = lesson('<ul><li><b>Percent</b> means per 100: 35% = 35/100 = 0.35.</li><li>Fraction to decimal: divide the top by the bottom. 3/8 = 3 ÷ 8 = 0.375.</li><li>Decimal to percent: multiply by 100 (move the decimal point 2 places right). Percent to decimal: divide by 100.</li><li>Benchmarks: 1/2 = 50%, 1/4 = 25%, 3/4 = 75%, 1/10 = 10%, 1/5 = 20%.</li></ul>',
        [example("3/5", ["3 ÷ 5 = 0.6", "0.6 × 100"], "60%"), example("Order 0.7, 2/3, 72%", ["2/3 ≈ 0.667, 72% = 0.72"], "2/3, 0.7, 72%")],
        [['Writing 3/5 as 35%', '3/5 = 3 ÷ 5 = 0.6 = 60%.'], ['Moving the decimal point the wrong way', '0.4 = 40%, not 0.004%.'], ['Comparing digits instead of values', 'Change everything to decimals before you compare.']])
    faq = [('What does TEKS 6.4G ask?', 'Generate equivalent forms of fractions, decimals and percents using real-world problems, including problems that involve money.'), ('What does TEKS 6.4F ask?', 'Represent benchmark fractions and percents such as 1%, 10%, 25%, 33 1/3% and multiples of these values using 10 by 10 grids, strip diagrams, number lines and numbers.'), ('What does TEKS 6.5C ask?', 'Use equivalent fractions, decimals and percents to show equal parts of the same whole.'), ('Can a percent be more than 100%?', 'Yes. 125% = 1.25 = 5/4, more than one whole.')]
    make('fractions-decimals-and-percents', 9, 'Proportionality', '6.4E, 6.4F, 6.4G, 6.5C',
         '6.4E represent ratios and percents with concrete models, fractions, and decimals; 6.4F represent benchmark fractions and percents such as 1%, 10%, 25%, 33 1/3%, and multiples of these values using 10 by 10 grids, strip diagrams, number lines, and numbers; 6.4G generate equivalent forms of fractions, decimals, and percents using real-world problems, including problems that involve money; 6.5C use equivalent fractions, decimals, and percents to show equal parts of the same whole',
         'Fractions, Decimals and Percents', 'Fractions, Decimals and Percents',
         'Free Grade 6 worksheets for Texas TEKS 6.4E, 6.4F, 6.4G and 6.5C: percent grids, benchmark percents, convert fractions, decimals and percents, and compare and order. 100 questions with answers.',
         'Fraction → decimal: divide. Decimal → percent: × 100.', '3/5 = 0.6 = 60%. 1/4 = 0.25 = 25%.',
         body, faq, sets, seo_title='Grade 6 Fractions, Decimals and Percents Worksheets (TEKS 6.4G, 6.5C, STAAR)')


if __name__ == "__main__":
    build()
