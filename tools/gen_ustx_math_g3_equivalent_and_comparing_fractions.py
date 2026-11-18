# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Equivalent and Comparing Fractions (TEKS 3.3F, 3.3G, 3.3H)
  python3 tools/gen_ustx_math_g3_equivalent_and_comparing_fractions.py
Equivalent fractions with fraction strips (the US Grade 3 maker, denominators 2, 3, 4, 6 and 8), equivalent
fractions on two number lines, comparing fractions (the US Grade 3 maker), comparing with the same numerator or the
same denominator and explaining why, and word problems.
Wrong answers come from real mistakes: thinking a bigger denominator means a bigger fraction, comparing fractions
of different-size wholes, and thinking 2/4 and 2/8 are equal because the numerators match.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, fr, run_many, adopt, svg_wrap, text,
                       line, GREEN, RED, INK, FILL, example)
import gen_us_math_g3_fractions as usf
from gen_ustx_math_g3_fractions_on_number_line import frac_line, teks_dens
from gen_ustx_math_g3_fractions import bar_svg

adopt(usf)
R = random.Random(61301)
EQ = [(1, 2, 2, 4), (1, 2, 3, 6), (1, 2, 4, 8), (1, 3, 2, 6), (2, 3, 4, 6), (1, 4, 2, 8), (3, 4, 6, 8), (2, 4, 4, 8),
      (2, 2, 4, 4), (3, 6, 4, 8), (1, 1, 6, 6), (2, 4, 3, 6), (4, 4, 8, 8), (3, 3, 6, 6)]


def two_lines(d1, d2, k1, k2):
    a = frac_line(d1, [(k1, "", RED)], labels="all")
    b = frac_line(d2, [(k2, "", RED)], labels="all")
    return "<div class='qfig'>" + a + "<br>" + b + "</div>"


def one_strips(r):
    a, b, c, d = r.choice([e for e in EQ if e[1] != 1])
    q = "<div class='qfig'>" + bar_svg(b, a) + "<br>" + bar_svg(d, c) + "</div>The two strips are the same size. Which is true?"
    return mcq(q, "%s = %s" % (fr(a, b), fr(c, d)), ["%s &gt; %s" % (fr(a, b), fr(c, d)), "%s &lt; %s" % (fr(a, b), fr(c, d)), "%s = %s" % (fr(a, b), fr(a, d))],
               "The shaded parts are the same length, so <b>%s = %s</b>." % (fr(a, b), fr(c, d)))


def one_cmp_bars(r):
    if r.random() < 0.5:
        d = r.choice([3, 4, 6, 8])
        x, y = r.sample(range(1, d + 1), 2)
        b1, b2 = d, d
    else:
        x = y = r.choice([1, 2, 3])
        b1, b2 = r.sample([b for b in (2, 3, 4, 6, 8) if b >= x], 2)
    v1, v2 = x / float(b1), y / float(b2)
    if v1 == v2:
        return None
    sym = "&gt;" if v1 > v2 else "&lt;"
    q = "<div class='qfig'>" + bar_svg(b1, x) + "<br>" + bar_svg(b2, y) + "</div>Compare: %s ☐ %s" % (fr(x, b1), fr(y, b2))
    return mcq(q, sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"], "The shaded part of the %s strip is longer: <b>%s %s %s</b>." % ("top" if v1 > v2 else "bottom", fr(x, b1), sym, fr(y, b2)))


# ------------------------------------------------------------ set 2: equivalent on number lines
def one_lines(r):
    a, b, c, d = r.choice(EQ)
    if b == 1:
        return None
    kind = r.choice(["same", "which"])
    if kind == "same":
        q = two_lines(b, d, a, c) + "The red points are at the same place. Which is true?"
        right = "%s = %s" % (fr(a, b), fr(c, d))
        return mcq(q, right, ["%s &gt; %s" % (fr(a, b), fr(c, d)), "%s &lt; %s" % (fr(a, b), fr(c, d)), "%s = %s" % (fr(a, b), fr(c + 1, d) if c < d else fr(c - 1, d)), "%s = %s" % (fr(a, b), fr(a, d))],
                   "Both points are the same distance from 0, so the fractions are equivalent: <b>%s</b>." % right)
    pic = fig(frac_line(d, [], labels="all"))
    return mcq(pic + "Which fraction on this number line is equivalent to %s?" % fr(a, b), fr(c, d), [fr(a, d), fr(c + 1, d) if c + 1 <= d else fr(c - 1, d), fr(d - c, d) if d - c not in (0, c) else fr(1, d), fr(c - 1, d) if c > 1 else fr(c + 2, d), fr(c + 2, d) if c + 2 <= d else fr(1, d)],
               "%s is the same distance from 0 as <b>%s</b>." % (fr(a, b), fr(c, d)))


# ------------------------------------------------------------ set 4: same numerator or same denominator
def one_same(r):
    kind = r.choice(["den", "num", "why_num", "why_den"])
    if kind in ("den", "why_den"):
        d = r.choice([3, 4, 6, 8])
        x, y = r.sample(range(1, d + 1), 2)
        if kind == "den":
            sym = "&gt;" if x > y else "&lt;"
            return mcq("Compare: %s ☐ %s" % (fr(x, d), fr(y, d)), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"],
                       "Same denominator, so the parts are the same size. %d part%s %s %d part%s: <b>%s %s %s</b>." % (x, "" if x == 1 else "s", "is more than" if x > y else "is less than", y, "" if y == 1 else "s", fr(x, d), sym, fr(y, d)))
        big = max(x, y)
        return mcq("Why is %s greater than %s?" % (fr(big, d), fr(min(x, y), d)), "The parts are the same size, and %d parts are more than %d" % (big, min(x, y)),
                   ["Eighths are always bigger", "The denominators are different", "%d is an even number" % big if big % 2 == 0 else "%d is an odd number" % big],
                   "<b>The parts are the same size, and %d parts are more than %d</b>." % (big, min(x, y)))
    n = r.choice([1, 1, 2, 3])
    ds = [d for d in [2, 3, 4, 6, 8] if d >= n]
    d1, d2 = r.sample(ds, 2)
    if n > min(d1, d2):
        return None
    if kind == "num":
        sym = "&gt;" if d1 < d2 else "&lt;"
        return mcq("Compare: %s ☐ %s" % (fr(n, d1), fr(n, d2)), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "−"],
                   "Same numerator. Fewer parts in the whole means bigger parts, so %s is %s: <b>%s %s %s</b>." % (fr(n, min(d1, d2)), "greater", fr(n, d1), sym, fr(n, d2)))
    small, large = min(d1, d2), max(d1, d2)
    return mcq("Why is %s greater than %s?" % (fr(n, small), fr(n, large)), "A whole cut into %d parts has bigger parts than one cut into %d" % (small, large),
               ["%d is greater than %d" % (large, small), "The numerators are different", "Smaller numbers are always greater"],
               "Same numerator. <b>A whole cut into %d parts has bigger parts than one cut into %d</b>." % (small, large))


# ------------------------------------------------------------ set 5: word problems
def one_story(r):
    k1, k2 = Kid(r).next(), Kid(r).next()
    if k1["n"] == k2["n"]:
        return None
    food = r.choice(["pizza", "pan of enchiladas", "pie", "sandwich", "granola bar"])
    kind = r.choice(["more", "more", "same", "whole"])
    if kind == "more":
        if r.random() < 0.5:
            d = r.choice([4, 6, 8])
            x, y = r.sample(range(1, d), 2)
            a, b = fr(x, d), fr(y, d)
            win = k1["n"] if x > y else k2["n"]
        else:
            n = r.choice([1, 2])
            d1, d2 = r.sample([3, 4, 6, 8], 2)
            a, b = fr(n, d1), fr(n, d2)
            win = k1["n"] if d1 < d2 else k2["n"]
        q = "%s and %s each have the same size %s. %s eats %s of %s %s. %s eats %s of %s %s. Who eats more?" % (k1["n"], k2["n"], food, k1["n"], a, k1["his"], food, k2["n"], b, k2["his"], food)
        return mcq(q, win, [k2["n"] if win == k1["n"] else k1["n"], "They eat the same amount", "We cannot tell"],
                   "Compare %s and %s. <b>%s</b> eats more." % (a, b, win))
    if kind == "same":
        a, b, c, d = r.choice([e for e in EQ if e[1] != 1])
        q = "%s runs %s of a mile. %s runs %s of a mile. Who runs farther?" % (k1["n"], fr(a, b), k2["n"], fr(c, d))
        return mcq(q, "They run the same distance", [k1["n"], k2["n"], "We cannot tell"], "%s = %s, so <b>they run the same distance</b>." % (fr(a, b), fr(c, d)))
    q = "%s eats %s of a small pizza. %s eats %s of a large pizza. %s says they ate the same amount. Is that right?" % (k1["n"], fr(1, 2), k2["n"], fr(1, 2), k1["n"])
    return mcq(q, "No. Halves of different-size wholes are not the same amount", ["Yes. Both are " + fr(1, 2), "Yes. " + fr(1, 2) + " is always the same", "No. " + fr(1, 2) + " of a small pizza is more"],
               "To compare fractions, the wholes must be the same size. <b>No. Halves of different-size wholes are not the same amount</b>.")


def build():
    sets = [S("Equivalent fractions with strips", run_many(usf.set_equiv, "rnd", seed=141, n=12, keep=teks_dens) + collect(one_strips, 8, R)),
            S("Equivalent fractions on number lines", collect(one_lines, 20, R)),
            S("Compare fractions", run_many(usf.set_compare, "rnd", seed=142, n=8, keep=teks_dens) + collect(one_cmp_bars, 12, R)),
            S("Same numerator or same denominator: explain why", collect(one_same, 20, R)),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li><b>Equivalent fractions</b> name the same amount: %s = %s = %s. On number lines, they are at the same point.</li>"
        "<li><b>Same denominator</b>: the parts are the same size, so compare the numerators. %s &gt; %s.</li>"
        "<li><b>Same numerator</b>: the fraction with fewer parts in the whole has bigger parts. %s &gt; %s.</li>"
        "<li>Only compare fractions of the <b>same-size whole</b>.</li></ul>" % (fr(1, 2), fr(2, 4), fr(4, 8), fr(5, 8), fr(3, 8), fr(1, 3), fr(1, 6)),
        [two_lines(2, 4, 1, 2) + "<p>1/2 and 2/4 are at the same point, so they are equivalent.</p>",
         example("Compare 2/3 and 2/6.", ["The numerators are the same: 2 parts each.", "Thirds are bigger than sixths."], "2/3 &gt; 2/6")],
        [["Thinking a bigger denominator means a bigger fraction: 1/8 &gt; 1/4", "More parts in the whole means smaller parts."],
         ["Comparing halves of different-size wholes", "Use the same-size whole."],
         ["Thinking 2/4 = 2/8 because both have 2", "Fourths are bigger than eighths, so 2/4 &gt; 2/8."]])
    faq = [("What does TEKS 3.3F ask?", "Represent equivalent fractions with denominators 2, 3, 4, 6 and 8 using objects, pictures and number lines."),
           ("How do you explain that two fractions are equivalent?", "Show that they are at the same point on number lines of the same length, or that they cover the same part of same-size wholes (TEKS 3.3G)."),
           ("How do you compare fractions with the same numerator?", "Look at the denominators. The fraction with the smaller denominator has bigger parts, so it is greater (TEKS 3.3H)."),
           ("Why must the wholes be the same size?", "Half of a large pizza is more than half of a small pizza. Fractions can only be compared when they refer to the same whole.")]
    make("equivalent-and-comparing-fractions", 13, "Number and Operations", "3.3F, 3.3G, 3.3H",
         "3.3F represent equivalent fractions with denominators of 2, 3, 4, 6, and 8 using a variety of objects and pictorial models, including number lines; 3.3G explain that two fractions are equivalent if and only if they are both represented by the same point on the number line or represent the same portion of a same size whole for an area model; 3.3H compare two fractions having the same numerator or denominator in problems by reasoning about their sizes and justifying the conclusion using symbols, words, objects, and pictorial models",
         "Equivalent and Comparing Fractions", "Equivalent and Comparing Fractions",
         "Free Grade 3 worksheets for Texas TEKS 3.3F, 3.3G and 3.3H: equivalent fractions with strips and number lines, compare fractions with the same numerator or denominator, explain why, and word problems. 100 questions with answers.",
         "Equivalent fractions are at the same point on a number line.", "Same denominator: compare the numerators. Same numerator: fewer parts means bigger parts.",
         body, faq, sets, seo_title="Grade 3 Equivalent and Comparing Fractions Worksheets (TEKS 3.3F, 3.3H, STAAR)")


if __name__ == "__main__":
    build()
