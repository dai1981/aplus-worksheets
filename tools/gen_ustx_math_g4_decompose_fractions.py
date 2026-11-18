# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Decomposing Fractions: Sums of Unit Fractions and More (TEKS 4.3A, 4.3B)
  python3 tools/gen_ustx_math_g4_decompose_fractions.py
A fraction as a sum of unit fractions, breaking apart a fraction in more than one way, mixed numbers as sums,
fraction strips (the US Grade 4 decompose maker with Texas names), and word problems.
Wrong answers come from real mistakes: adding the denominators, using parts that do not add to the numerator, and
mixing up the whole and the parts of a mixed number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_add_subtract_fractions as usf
adopt(usf)
tx_common.GRADE = "grade-4"

DENS = [3, 4, 5, 6, 8, 10, 12]


def one_unit(r):
    d = r.choice(DENS)
    a = r.randint(2, d)
    kind = r.choice(["to_sum", "from_sum"])
    if kind == "to_sum":
        right = " + ".join([fr(1, d)] * a)
        wrong = [" + ".join([fr(1, d)] * (a - 1)) if a > 2 else fr(1, d) + " + " + fr(1, d) + " + " + fr(1, d), " + ".join([fr(1, a)] * d) if a != d else fr(1, d) + " + " + fr(a - 1, d), fr(1, a) + " + " + fr(1, d), fr(a, d) + " + " + fr(1, d)]
        return mcq("Which sum of unit fractions equals %s?" % fr(a, d), right, wrong, "%s is %d parts of size %s: <b>%s</b>." % (fr(a, d), a, fr(1, d), right))
    s = " + ".join([fr(1, d)] * a)
    return mcq("%s = ?" % s, fr(a, d), [fr(a, d * a), fr(1, d * a), fr(a + 1, d), fr(a, a + d)], "%d copies of %s make <b>%s</b>." % (a, fr(1, d), fr(a, d)))


def one_ways(r):
    d = r.choice(DENS)
    a = r.randint(3, d)
    x = r.randint(1, a - 1)
    y = a - x
    kind = r.choice(["which", "which", "missing", "not"])
    if kind == "which":
        right = "%s + %s" % (fr(x, d), fr(y, d))
        wrong = ["%s + %s" % (fr(x, d), fr(y + 1, d)), "%s + %s" % (fr(x, d - y) if d - y > 1 else fr(x, d + 1), fr(y, d)), "%s + %s" % (fr(x, d), fr(y, d - 1) if d - 1 > y else fr(y, d + 2)), "%s + %s" % (fr(x - 1, d) if x > 1 else fr(x + 2, d), fr(y, d))]
        return mcq("Which is another way to write %s?" % fr(a, d), right, wrong, "The numerators must add to %d and the denominator stays %d: <b>%s</b>." % (a, d, right))
    if kind == "missing":
        return mcq("%s = %s + %s" % (fr(a, d), fr(x, d), "<span class='fr'><span class='fn'>☐</span><span class='fd'>%d</span></span>" % d), y, [a, a + x, x if x != y else y + 1, d - x if d - x != y else y + 2],
                   "%d − %d = <b>%d</b>, so %s = %s + %s." % (a, x, y, fr(a, d), fr(x, d), fr(y, d)))
    z = a + r.choice([1, -1])
    p = r.randint(1, max(1, z - 1))
    q = z - p
    if q < 1:
        return None
    good = ["%s + %s" % (fr(x, d), fr(y, d)), " + ".join([fr(1, d)] * a)]
    for u in range(1, a):
        g = "%s + %s" % (fr(a - u, d), fr(u, d))
        if g not in good:
            good.append(g)
    return mcq("Which is <b>not</b> equal to %s?" % fr(a, d), "%s + %s" % (fr(p, d), fr(q, d)), good,
               "%s + %s = %s, not %s." % (fr(p, d), fr(q, d), fr(z, d), fr(a, d)))


def one_mixed(r):
    d = r.choice([2, 3, 4, 5, 6, 8])
    w = r.randint(1, 3)
    a = r.randint(1, d - 1)
    kind = r.choice(["sum", "improper"])
    mixed = "%d%s" % (w, fr(a, d))
    if kind == "sum":
        right = " + ".join(["1"] * w + [fr(a, d)])
        wrong = [" + ".join([fr(1, d)] * w + [fr(a, d)]), "%d + %s" % (w + 1, fr(a, d)), " + ".join(["1"] * w + [fr(a + 1, d) if a + 1 < d else fr(a - 1, d) if a > 1 else fr(a, d + 1)])]
        return mcq("Which sum equals %s?" % mixed, right, wrong, "%s is %d whole%s and %s: <b>%s</b>." % (mixed, w, "" if w == 1 else "s", fr(a, d), right))
    return mcq("%s = %s + %s. How many %ss is that in all?" % (mixed, fr(w * d, d), fr(a, d), {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 8: "eighth"}[d]),
               fr(w * d + a, d), [fr(w + a, d), fr(w * a, d) if w * a != w * d + a else fr(w * d, d), fr(w * d + a, d * w + 1)], "%d whole%s = %s. %s + %s = <b>%s</b>." % (w, "" if w == 1 else "s", fr(w * d, d), fr(w * d, d), fr(a, d), fr(w * d + a, d)))


def one_story(r):
    k = Kid(r).next()
    d = r.choice([4, 6, 8, 10, 12])
    a = r.randint(3, d)
    x = r.randint(1, a - 1)
    what = r.choice([("pizza", "slices", "ate"), ("pan of brownies", "pieces", "ate"), ("garden", "rows", "planted"), ("poster", "parts", "painted")])
    return mcq("%s %s %s of a %s. %s %s %s on Monday and the rest on Tuesday. What fraction did %s %s on Tuesday?" % (k["n"], what[2], fr(a, d), what[0], k["He"], what[2], fr(x, d), k["he"], {"ate": "eat", "planted": "plant", "painted": "paint"}[what[2]]),
               fr(a - x, d), [fr(a + x, d), fr(a - x, 2 * d), fr(x, d) if x != a - x else fr(x + 1, d)],
               "%s = %s + ☐, so ☐ = %s − %s = <b>%s</b>." % (fr(a, d), fr(x, d), fr(a, d), fr(x, d), fr(a - x, d)))


def build():
    sets, R = build_sets([
        ("A fraction as a sum of unit fractions", [("collect", one_unit, 20)]),
        ("Break apart in more than one way", [("collect", one_ways, 20)]),
        ("Break apart with fraction strips", [("run", usf.set_decompose, ("rnd",), 20)]),
        ("Mixed numbers as sums", [("collect", one_mixed, 20)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 64014)
    finish(sets, R)
    body = lesson('<ul><li>Every fraction a/b is a sum of unit fractions 1/b: 3/5 = 1/5 + 1/5 + 1/5.</li><li>A fraction can be broken apart in more than one way. The numerators must add to the same total, and the denominator stays the same: 5/8 = 2/8 + 3/8 = 1/8 + 4/8.</li><li>A mixed number is wholes plus a fraction: 2 1/4 = 1 + 1 + 1/4 = 4/4 + 4/4 + 1/4.</li></ul>',
        [example("Write 5/8 in two different ways.", ["5 = 2 + 3", "5 = 1 + 1 + 3"], "2/8 + 3/8 and 1/8 + 1/8 + 3/8"), example("Write 1 2/3 as a sum.", ["1 = 3/3"], "3/3 + 2/3")],
        [['Adding the denominators: 2/8 + 3/8 = 5/16', 'The size of the parts does not change. Keep eighths.'], ['Using parts that do not add to the numerator', 'Check: the numerators must add to the total.'], ['Forgetting the whole in a mixed number', 'Write each whole as b/b.']])
    faq = [('What does TEKS 4.3A ask?', 'Represent a fraction a/b as a sum of fractions 1/b, where a and b are whole numbers and b &gt; 0, including when a &gt; b.'), ('What does TEKS 4.3B ask?', 'Decompose a fraction in more than one way into a sum of fractions with the same denominator using models, and record the results with symbols.'), ('Can a fraction be decomposed in only one way?', 'No. 4/6 can be 1/6 + 3/6, 2/6 + 2/6 or 1/6 + 1/6 + 2/6.'), ('How does decomposing help?', 'It prepares you to add and subtract fractions and to rename mixed numbers.')]
    make('decomposing-fractions', 14, 'Number and Operations', '4.3A, 4.3B',
         '4.3A represent a fraction a/b as a sum of fractions 1/b, where a and b are whole numbers and b > 0, including when a > b; 4.3B decompose a fraction in more than one way into a sum of fractions with the same denominator using concrete and pictorial models and recording results with symbolic representations',
         'Decomposing Fractions: Sums of Unit Fractions and More', 'Decomposing Fractions',
         'Free Grade 4 fraction worksheets for Texas TEKS 4.3A and 4.3B: fractions as sums of unit fractions, decomposing in more than one way, fraction strips, mixed numbers as sums and word problems. 100 questions with answers.',
         'A fraction can be broken into parts with the same denominator.', '5/8 = 1/8 + 1/8 + 1/8 + 1/8 + 1/8 = 2/8 + 3/8. The numerators add up; the denominator stays the same.',
         body, faq, sets, seo_title='Grade 4 Decomposing Fractions Worksheets (TEKS 4.3A, 4.3B, STAAR)')


if __name__ == "__main__":
    build()
