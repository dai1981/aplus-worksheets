# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Fractions on a Number Line (TEKS 3.3B, 3.7A)
  python3 tools/gen_ustx_math_g3_fractions_on_number_line.py
Naming the fraction at a point, finding the point for a fraction, distances from 0 in halves, fourths and eighths,
missing labels, and unit fraction jumps (the US Grade 3 number line maker with Texas names, denominators 2, 3,
4, 6 and 8 only).
Wrong answers come from real mistakes: counting the tick marks instead of the spaces, counting from 1 instead of
0, and using the number of ticks as the denominator.
"""
import random
from tx_common import (mcq, collect, finish, make, fig, figure, lesson, S, fr, run_many, adopt, svg_wrap, text, line,
                       GREEN, RED, INK, BLUE, example)
import gen_us_math_g3_fractions as usf

adopt(usf)
R = random.Random(61201)
DENS = [2, 3, 4, 6, 8]


def frac_line(d, points=(), labels="ends", jumps=0, W=440):
    """Number line 0 to 1 cut into d equal spaces. points: [(k, label, color)]. labels: 'ends', 'all' or a set of k."""
    x0, x1, y = 30, W - 30, 58 if not jumps else 78
    X = lambda k: x0 + (x1 - x0) * k / float(d)
    s = [line(x0 - 10, y, x1 + 10, y, INK, 2)]
    for k in range(d + 1):
        s.append(line(X(k), y - 9, X(k), y + 9, INK, 2))
        show = (k in (0, d)) if labels == "ends" else True if labels == "all" else k in labels
        if show:
            lab = "0" if k == 0 else "1" if k == d else fr(k, d)
            if k in (0, d):
                s.append(text(X(k), y + 30, lab, 16))
            else:
                s.append(text(X(k), y + 24, str(k), 13) + line(X(k) - 7, y + 28, X(k) + 7, y + 28, INK, 1.5) + text(X(k), y + 42, str(d), 13))
    for j in range(jumps):
        xa, xb = X(j), X(j + 1)
        mid = (xa + xb) / 2
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (xa, y - 4, mid, y - 40, xb, y - 4, BLUE))
    for k, lab, col in points:
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(k), y, col))
        if lab:
            s.append(text(X(k), y - 16, lab, 16, col=col))
    return svg_wrap(W, y + 50, "".join(s), "number line from 0 to 1 cut into %d equal parts" % d)


# ------------------------------------------------------------ set 1: name the point
def one_name(r):
    d = r.choice(DENS)
    k = r.randint(1, d)
    pic = fig(frac_line(d, [(k, "", RED)]))
    wrong = [fr(k, d + 1), fr(k + 1, d) if k < d else fr(k - 1, d), fr(1, k) if k > 1 else fr(1, d + 1), fr(d, k) if k not in (d,) else fr(k - 1, d)]
    right = fr(k, d) if k < d else fr(d, d)
    return mcq(pic + "What fraction is at the red point?", right, wrong,
               "There are %d equal spaces from 0 to 1, so each space is %s. The point is %d space%s from 0: <b>%s</b>%s." % (d, fr(1, d), k, "" if k == 1 else "s", right, " (which is 1 whole)" if k == d else ""))


# ------------------------------------------------------------ set 2: which point?
def one_point(r):
    d = r.choice([6, 8])
    ks = r.sample(range(1, d + 1), 4)
    j = r.randrange(4)
    pts = [(k, "ABCD"[i], RED if i == j else GREEN) for i, k in enumerate(sorted(ks))]
    pts = [(k, lab, GREEN) for k, lab, _ in pts]
    target = sorted(ks)[j]
    pic = fig(frac_line(d, pts))
    it = mcq(pic + "Which point shows %s?" % fr(target, d), "ABCD"[j], [l for l in "ABCD" if l != "ABCD"[j]],
             "Count %d equal spaces from 0. Point <b>%s</b> is at %s." % (target, "ABCD"[j], fr(target, d)))
    it["_fixed"] = False
    return it


# ------------------------------------------------------------ set 3: distance from zero (halves, fourths, eighths)
def one_dist(r):
    d = r.choice([2, 4, 8])
    k = r.randint(1, d)
    if r.random() < 0.4:
        pic = fig(frac_line(d, [(k, "", RED)], labels="all"))
        return mcq(pic + "How many hops of %s does it take to go from 0 to the red point?" % fr(1, d), k, [k + 1, d, k - 1 if k > 1 else k + 2, d - k if d - k not in (0, k) else k + 3],
                   "Each hop is %s. The red point is %s, so it takes <b>%d</b> hop%s." % (fr(1, d), fr(k, d), k, "" if k == 1 else "s"))
    pic = fig(frac_line(d, [(k, "", RED)], jumps=k))
    wrong = [fr(k, d + 1) if d + 1 <= 9 else fr(k, d * 2), fr(k + 1, d) if k < d else fr(k - 1, d) if k > 1 else fr(2, d), fr(1, d) if k > 1 else fr(2, d), fr(k, 2 * d) if 2 * d <= 8 else fr(1, k + 1)]
    right = fr(k, d)
    return mcq(pic + "A bug hops from 0 to the red point. Each hop is %s. How far from 0 is the bug?" % fr(1, d), right, wrong,
               "The bug makes %d hop%s of %s: <b>%s</b> of the distance from 0 to 1." % (k, "" if k == 1 else "s", fr(1, d), right))


# ------------------------------------------------------------ set 4: missing labels
def one_label(r):
    d = r.choice([3, 4, 6, 8])
    known = set(r.sample(range(1, d), min(2, d - 2)))
    k = r.choice([x for x in range(1, d) if x not in known])
    pic = fig(frac_line(d, [(k, "?", RED)], labels=known))
    wrong = [fr(k + 1, d), fr(k - 1, d) if k > 1 else fr(k + 2, d), fr(k, d + 1), fr(d, k)]
    return mcq(pic + "What fraction belongs at the ?", fr(k, d), wrong,
               "The labels count %s at a time. The ? is %d space%s from 0: <b>%s</b>." % (fr(1, d), k, "" if k == 1 else "s", fr(k, d)))


def teks_dens(it):
    import re
    main = [int(x) for x in re.findall(r"class='fd'>(\d+)<", it["q"] + it["c"][it["a"]])]
    alld = [int(x) for x in re.findall(r"class='fd'>(\d+)<", it["q"] + "".join(it["c"]) + it["e"])]
    return all(x in (1, 2, 3, 4, 6, 8) for x in main) and all(x <= 9 for x in alld)


def build():
    sets = [S("Name the point", collect(one_name, 20, R)),
            S("Which point shows the fraction?", collect(one_point, 20, R)),
            S("Distance from 0: halves, fourths, eighths", collect(one_dist, 20, R)),
            S("Missing labels", collect(one_label, 20, R)),
            S("Unit fractions and number lines", run_many(usf.set_line, "rnd", seed=131, keep=teks_dens))]
    for it in sets[1]["items"]:
        it["_fixed"] = True
    finish(sets, R)
    body = lesson(
        "<ul><li>On a number line from 0 to 1, count the <b>spaces</b>, not the tick marks. If there are 4 equal spaces, each space is %s.</li>"
        "<li>Start counting at 0. The point 3 spaces from 0 is %s.</li>"
        "<li>A fraction on a number line is a <b>distance from 0</b>. %s is 3 jumps of %s.</li>"
        "<li>The point at 1 can be named %s, %s or %s.</li></ul>" % (fr(1, 4), fr(3, 4), fr(3, 4), fr(1, 4), fr(4, 4), fr(8, 8), "1"),
        [figure(frac_line(4, [(3, "", RED)], labels="all", jumps=3), "3 jumps of 1/4 from 0 land on 3/4."),
         example("A number line from 0 to 1 has 9 tick marks. What is each space?", ["9 tick marks make 8 spaces.", "Each space is 1/8."], "1/8")],
        [["Counting tick marks instead of spaces", "Count the jumps between marks. 5 marks make 4 spaces."],
         ["Starting at 1 instead of 0", "The first jump starts at 0."],
         ["Thinking 1 is not a fraction", "1 whole can be written 4/4 or 8/8."]])
    faq = [("What does TEKS 3.3B ask?", "Name the fraction greater than 0 and less than or equal to 1 at a point on a number line, with denominators 2, 3, 4, 6 and 8."),
           ("What does TEKS 3.7A ask?", "Show halves, fourths and eighths as distances from 0 on a number line."),
           ("How do I find the denominator from a number line?", "Count the equal spaces between 0 and 1. That number is the denominator."),
           ("Why use number lines for fractions?", "They show that fractions are numbers with a place between whole numbers, which helps with comparing and equivalent fractions later.")]
    make("fractions-on-a-number-line", 12, "Number and Operations", "3.3B, 3.7A",
         "3.3B determine the corresponding fraction greater than zero and less than or equal to one with denominators of 2, 3, 4, 6, and 8 given a specified point on a number line; 3.7A represent fractions of halves, fourths, and eighths as distances from zero on a number line",
         "Fractions on a Number Line", "Fractions on a Number Line",
         "Free Grade 3 worksheets for Texas TEKS 3.3B and 3.7A: name the fraction at a point, find the point for a fraction, halves, fourths and eighths as distances from 0, and missing labels. 100 questions with answers.",
         "Count the equal spaces from 0, not the tick marks.", "If 0 to 1 has 8 equal spaces, each is 1/8. The point 5 spaces from 0 is 5/8.",
         body, faq, sets, seo_title="Grade 3 Fractions on a Number Line Worksheets (TEKS 3.3B, 3.7A, STAAR)")


if __name__ == "__main__":
    build()
