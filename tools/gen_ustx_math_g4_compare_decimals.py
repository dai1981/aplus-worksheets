# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Comparing Decimals and Decimals on a Number Line (TEKS 4.2F, 4.2H, 4.3G)
  python3 tools/gen_ustx_math_g4_compare_decimals.py
Decimals and fractions on number lines (the US Grade 4 makers with Texas names), comparing and ordering decimals
to hundredths, and word problems.
Wrong answers come from real mistakes: thinking 0.45 > 0.5 because 45 > 5, counting tick marks instead of spaces,
and ordering from greatest when the question asks for least.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_decimals as usd
import gen_us_math_g4_equivalent_fractions as use
adopt(usd)
adopt(use)
tx_common.GRADE = "grade-4"

def pick2(r):
    a = r.randint(1, 99)
    kind = r.choice(["trap", "trap", "near"])
    if kind == "trap":
        t = r.randint(1, 9)
        h = r.randint(10, 99)
        if t * 10 == h:
            return None
        return (t * 10, 1), (h, 2)
    b = a + r.choice([-9, -1, 1, 9, 10])
    if not 1 <= b <= 99 or a == b:
        return None
    return (a, 2), (b, 2)


def txt(v):
    n, p = v
    return "0.%d" % (n // 10) if p == 1 else "0.%02d" % n


def one_cmp(r):
    pr = pick2(r)
    if not pr:
        return None
    a, b = pr
    if r.random() < 0.5:
        a, b = b, a
    w = r.randint(0, 9)
    ta, tb = ("%d" % w) + txt(a)[1:], ("%d" % w) + txt(b)[1:]
    sym = "&gt;" if a[0] > b[0] else "&lt;"
    return mcq("Compare: %s ☐ %s" % (ta, tb), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"],
               "Line up the decimal points and compare tenths, then hundredths. %s %s %s, so use <b>%s</b>." % (ta, "is greater than" if sym == "&gt;" else "is less than", tb, sym))


def one_order(r):
    vals = r.sample(range(1, 99), 3)
    reps = []
    for v in vals:
        reps.append((v, 1) if v % 10 == 0 else (v, 2))
    if r.random() < 0.5:
        t = r.randint(1, 9)
        reps[0] = (t * 10, 1)
    vs = sorted(set(reps), key=lambda x: x[0])
    if len(vs) < 3 or len(set(x[0] for x in vs)) < 3:
        return None
    up = r.random() < 0.5
    right = vs if up else vs[::-1]
    s = lambda L: "; ".join(txt(x) for x in L)
    wrong = [vs[::-1] if up else vs, sorted(vs, key=lambda x: int(txt(x)[2:])), [vs[1], vs[0], vs[2]], [vs[0], vs[2], vs[1]]]
    shown = vs[:]
    while shown in (vs, vs[::-1]):
        r.shuffle(shown)
    return mcq("Order from %s: %s" % ("least to greatest" if up else "greatest to least", s(shown)), s(right), [s(w) for w in wrong if w != right],
               "Write each with hundredths to compare: %s. <b>%s</b>." % ("; ".join("0.%02d" % x[0] for x in vs), s(right)))


def one_story(r):
    k1, k2 = Kid(r).next(), Kid(r).next()
    if k1["n"] == k2["n"]:
        return None
    pr = pick2(r)
    if not pr:
        return None
    a, b = pr
    w = r.randint(1, 5)
    ta, tb = ("%d" % w) + txt(a)[1:], ("%d" % w) + txt(b)[1:]
    what = r.choice([("ran", "kilometers", "farther"), ("jumped", "meters", "farther"), ("poured", "liters of water", "more")])
    win = k1["n"] if a[0] > b[0] else k2["n"]
    return mcq("%s %s %s %s. %s %s %s %s. Who %s %s?" % (k1["n"], what[0], ta, what[1], k2["n"], what[0], tb, what[1], what[0], what[2]), win,
               [k2["n"] if win == k1["n"] else k1["n"], "They are the same", "We cannot tell"],
               "Compare %s and %s: write both with hundredths. <b>%s</b> %s %s." % (ta, tb, win, what[0], what[2]))


def build():
    sets, R = build_sets([
        ("Decimals on a number line", [("run", usd.set_lines, ("rnd",), 20)]),
        ("Fractions and decimals as distances from 0", [("run", use.set_lines, ("rnd",), 20)]),
        ("Compare decimals", [("collect", one_cmp, 20)]),
        ("Order decimals", [("collect", one_order, 20)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 64004)
    finish(sets, R)
    body = lesson("<ul><li>To compare decimals, line up the decimal points and compare place by place from the left: ones, tenths, hundredths.</li><li>Write a zero so both have hundredths: 0.5 = 0.50, so 0.5 &gt; 0.45.</li><li>On a number line, count the equal spaces between 0 and 1: 10 spaces are tenths, 100 are hundredths. A point's decimal is its distance from 0.</li></ul>",
        [example("Compare 0.6 and 0.58.", ["0.6 = 0.60", "60 hundredths &gt; 58 hundredths"], "0.6 &gt; 0.58"), example("Order 0.4, 0.37, 0.09 from least to greatest.", ["0.40, 0.37, 0.09 in hundredths"], "0.09, 0.37, 0.4")],
        [['Thinking 0.45 &gt; 0.5 because 45 &gt; 5', 'Write 0.5 as 0.50, then compare.'], ['Counting tick marks instead of spaces on a number line', 'Count the jumps between marks.'], ['Ordering the wrong way', 'Read whether the question asks least to greatest or greatest to least.']])
    faq = [('What does TEKS 4.2F ask?', 'Compare and order decimals using concrete and visual models to the hundredths.'), ('What does TEKS 4.2H ask?', 'Determine the decimal to the tenths or hundredths place for a point on a number line.'), ('What does TEKS 4.3G ask?', 'Represent fractions and decimals to the tenths or hundredths as distances from zero on a number line.'), ('Why add a zero to compare decimals?', '0.5 and 0.50 are equal. Writing both numbers with hundredths makes it easy to compare the digits.')]
    make('comparing-decimals-and-number-lines', 4, 'Number and Operations', '4.2F, 4.2H, 4.3G',
         '4.2F compare and order decimals using concrete and visual models to the hundredths; 4.2H determine the corresponding decimal to the tenths or hundredths place of a specified point on a number line; 4.3G represent fractions and decimals to the tenths or hundredths as distances from zero on a number line',
         'Comparing Decimals and Decimals on a Number Line', 'Comparing Decimals and Number Lines',
         'Free Grade 4 worksheets for Texas TEKS 4.2F, 4.2H and 4.3G: decimals and fractions on number lines, compare and order decimals to hundredths, and word problems. 100 questions with answers.',
         'Line up the decimal points and compare from the left.', 'Write 0.5 as 0.50 to compare with hundredths. On a number line, a decimal is a distance from 0.',
         body, faq, sets, seo_title='Grade 4 Comparing Decimals and Number Lines Worksheets (TEKS 4.2F, 4.2H, STAAR)')


if __name__ == "__main__":
    build()
