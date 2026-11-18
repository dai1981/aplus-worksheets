# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Understanding Fractions (TEKS 3.3A, 3.3C, 3.3D, 3.3E, 3.6E)
  python3 tools/gen_ustx_math_g3_fractions.py
What fraction is shaded, unit fractions as 1 of b equal parts, composing and decomposing a fraction as a sum of
unit fractions, equal areas in shapes cut in different ways, and sharing problems. Sets 1, 2 and 4 and half of
set 5 use the US Grade 3 fraction and partition makers with Texas names and new numbers.
Denominators are 2, 3, 4, 6 and 8, as in the TEKS.
Wrong answers come from real mistakes: counting all the parts as the numerator, using unequal parts, adding the
denominators (1/4 + 1/4 = 2/8), and thinking parts must be the same shape to be equal.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, fr, run, run_many, adopt, svg_wrap,
                       GREEN, FILL, INK, example)
import gen_us_math_g3_fractions as usf
import gen_us_math_g3_partition_shapes as usp

adopt(usf)
adopt(usp)
R = random.Random(61101)
DENS = [2, 3, 4, 6, 8]


def teks_dens(it):
    """The question and the answer use denominators 2, 3, 4, 6 or 8; wrong choices may be off by one part (3/5 for 3/4)."""
    import re
    main = [int(d) for d in re.findall(r"class='fd'>(\d+)<", it["q"] + it["c"][it["a"]])]
    alld = [int(d) for d in re.findall(r"class='fd'>(\d+)<", it["q"] + "".join(it["c"]) + it["e"])]
    return all(d in (1, 2, 3, 4, 6, 8) for d in main) and all(d <= 9 for d in alld)


def bar_svg(d, shaded, w=300, h=44):
    cw = w / float(d)
    s = []
    for i in range(d):
        s.append("<rect x='%.1f' y='4' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (4 + i * cw, cw, h, FILL if i < shaded else "#fff", GREEN))
    return svg_wrap(w + 8, h + 8, "".join(s), "fraction strip with %d equal parts, %d shaded" % (d, shaded))


# ------------------------------------------------------------ set 3: compose and decompose
def one_compose(r):
    d = r.choice(DENS)
    a = r.randint(2, d)
    kind = r.choice(["sum_to", "decomp", "decomp", "count"])
    unit = fr(1, d)
    if kind == "sum_to":
        s = " + ".join([unit] * a)
        return mcq("%s = ?" % s, fr(a, d), [fr(a, d * a), fr(1, d * a), fr(a + 1, d), fr(a, a * d) if a * d != d * a else fr(1, a)],
                   "Add the unit fractions: %d copies of %s make <b>%s</b>. The denominator stays %d." % (a, unit, fr(a, d), d))
    if kind == "decomp":
        right = " + ".join([unit] * a)
        wrong = [" + ".join([fr(1, d)] * (a - 1)) if a > 2 else fr(1, d) + " + " + fr(1, d) + " + " + fr(1, d), " + ".join([fr(a, d)] * a), fr(1, a) + " + " + fr(1, d), " + ".join([fr(1, d * 2 if d * 2 <= 8 else 2)] * a)]
        return mcq("Which shows %s as a sum of unit fractions?" % fr(a, d), right, wrong,
                   "%s is %d parts of size %s: <b>%s</b>." % (fr(a, d), a, unit, right))
    return mcq(fig(bar_svg(d, a)) + "How many %s parts make the shaded fraction?" % unit, a, [d, d - a if d - a not in (0, a) else a + 1, a + 1], "Each part is %s. %d of them are shaded: %s." % (unit, a, fr(a, d)))


# ------------------------------------------------------------ set 5 (half): sharing problems
SHARE = [("{n} friends share {w} sandwich{es} equally. How much does each friend get?", "sandwich"),
         ("{n} students share {w} pan{s} of cornbread equally. How much of a pan does each student get?", "pan"),
         ("{n} children share {w} pizza{s} equally. How much does each child get?", "pizza"),
         ("{n} friends share {w} granola bar{s} equally. How much does each friend get?", "bar")]


def one_share(r):
    t, what = r.choice(SHARE)
    n = r.choice([2, 3, 4, 6, 8])
    w = 1 if r.random() < 0.7 else r.choice([2, 3])
    if w >= n or (w > 1 and n not in (4, 6, 8)):
        return None
    pl = "" if w == 1 else ("es" if what == "sandwich" else "s")
    q = t.format(n=n, w=w, es=pl, s=pl)
    right = fr(w, n)
    wrong = [fr(1, n) if w > 1 else fr(1, n + 1 if n + 1 in DENS else n + 2), fr(n, w) if w > 1 else fr(1, 2 * n if 2 * n <= 8 else n - 1), fr(w, n * 2) if n * 2 <= 16 else fr(w + 1, n), str(n)]
    note = "Cut each %s into %d equal parts and give each person 1 part from each %s." % (what, n, what) if w > 1 else "Cut the %s into %d equal parts. Each gets 1 part." % (what, n)
    return mcq(q, right, wrong, "%s Each gets <b>%s</b>%s." % (note, right, " of a %s" % what if w == 1 else ""))


def build():
    sets = [S("What fraction is shaded?", run_many(usf.set_shaded, "rnd", seed=121, keep=teks_dens)),
            S("Unit fractions and equal parts", run_many(usp.set_unit, "rnd", seed=122, keep=teks_dens)),
            S("Compose and decompose with unit fractions", collect(one_compose, 20, R)),
            S("Same area, different shape", run_many(usp.set_shape, "rnd", seed=123, keep=teks_dens)),
            S("Sharing and fraction word problems", collect(one_share, 10, R) + run_many(usf.set_words, "rnd", seed=124, n=10, keep=teks_dens))]
    finish(sets, R)
    body = lesson(
        "<ul><li>A fraction names part of a whole that is cut into <b>equal parts</b>. The denominator (bottom) says how many equal parts; the numerator (top) says how many you have.</li>"
        "<li>A <b>unit fraction</b> is 1 equal part: %s is 1 of 4 equal parts.</li>"
        "<li>A fraction is a sum of unit fractions: %s = %s + %s + %s.</li>"
        "<li>Equal parts have the same <b>area</b>, even if they are not the same shape.</li></ul>" % (fr(1, 4), fr(3, 4), fr(1, 4), fr(1, 4), fr(1, 4)),
        [figure(bar_svg(4, 3), "3 of 4 equal parts are shaded: 3/4 = 1/4 + 1/4 + 1/4."),
         example("3 friends share 2 sandwiches equally. How much does each get?", ["Cut each sandwich into 3 equal parts.", "Each friend gets 1 part of each sandwich: 2 parts of size 1/3."], "2/3 of a sandwich")],
        [["Counting all the parts as the numerator", "The numerator counts only the shaded (or chosen) parts."],
         ["Using parts that are not equal", "A fraction needs equal parts. Check that the parts are the same size."],
         ["Adding the denominators: 1/4 + 1/4 = 2/8", "The parts stay fourths. 1/4 + 1/4 = 2/4."]])
    faq = [("Which fractions do Texas Grade 3 students learn?", "Fractions greater than 0 and less than or equal to 1 with denominators 2, 3, 4, 6 and 8 (TEKS 3.3A)."),
           ("What is a unit fraction?", "A fraction with numerator 1, like 1/6. It is 1 of 6 equal parts of a whole (TEKS 3.3C)."),
           ("What does decomposing a fraction mean?", "Writing it as a sum of unit fractions: 5/8 = 1/8 + 1/8 + 1/8 + 1/8 + 1/8 (TEKS 3.3D)."),
           ("Can equal parts have different shapes?", "Yes. Two halves of a square can be two rectangles or two triangles. What matters is that each part has the same area (TEKS 3.6E).")]
    make("fractions", 11, "Number and Operations", "3.3A, 3.3C, 3.3D, 3.3E, 3.6E",
         "3.3A represent fractions greater than zero and less than or equal to one with denominators of 2, 3, 4, 6, and 8 using concrete objects and pictorial models, including strip diagrams and number lines; 3.3C explain that the unit fraction 1/b represents the quantity formed by one part of a whole that has been partitioned into b equal parts where b is a non-zero whole number; 3.3D compose and decompose a fraction a/b with a numerator greater than zero and less than or equal to b as a sum of parts 1/b; 3.3E solve problems involving partitioning an object or a set of objects among two or more recipients using pictorial representations of fractions with denominators of 2, 3, 4, 6, and 8; 3.6E decompose two congruent two-dimensional figures into parts with equal areas and express the area of each part as a unit fraction of the whole and recognize that equal shares of identical wholes need not have the same shape",
         "Understanding Fractions: Unit Fractions, Equal Parts and Sharing", "Fractions",
         "Free Grade 3 fraction worksheets for Texas TEKS 3.3A, 3.3C, 3.3D, 3.3E and 3.6E: shaded fractions, unit fractions, fractions as sums of unit fractions, equal areas and sharing problems with denominators 2, 3, 4, 6 and 8. 100 questions with answers.",
         "The denominator tells how many equal parts. The numerator tells how many you have.", "3/4 is 3 unit fractions of 1/4. Equal parts have equal area, not always the same shape.",
         body, faq, sets, seo_title="Grade 3 Fractions Worksheets: Unit Fractions and Equal Parts (TEKS 3.3A, STAAR)")


if __name__ == "__main__":
    build()
