# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Halves, Fourths and Eighths (TEKS 2.3A, 2.3B, 2.3C, 2.3D)
  python3 tools/gen_ustx_math_g2_fractions.py
Equal and unequal parts, naming halves and fourths (the US Grade 2 makers with Texas names, keeping only halves and
fourths), eighths, more parts make smaller parts, and counting parts beyond one whole (own makers).
Wrong answers come from real mistakes: calling unequal parts fourths, thinking more parts make bigger parts, and
not knowing how many parts make a whole.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_shares as shr
adopt(shr)
import math
tx_common.GRADE = "grade-2"

INK = "#1f2937"


def resolved(fn):
    """Picture-answer items are built later with build(pos); build them now at a random position."""
    def f(rnd):
        st = fn(rnd)
        st["items"] = [it["build"](rnd.randrange(4)) if "build" in it else it for it in st["items"]]
        return st
    f.__name__ = fn.__name__
    return f


def no_thirds(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return "third" not in t.lower()


def circle_svg(n, shaded):
    cx, cy, rr = 70, 70, 58
    s = ["<svg viewBox='0 0 140 140' width='140' role='img' aria-label='circle cut into %d equal parts'>" % n]
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n - math.pi / 2, 2 * math.pi * (i + 1) / n - math.pi / 2
        x0, y0 = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
        x1, y1 = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, x0, y0, rr, rr, x1, y1, "#60a5fa" if i < shaded else "#ffffff", INK))
    s.append("</svg>")
    return "".join(s)


def bar_svg(n, shaded):
    W = 280
    w = W / float(n)
    s = ["<svg viewBox='0 0 300 60' width='300' role='img' aria-label='bar cut into %d equal parts'>" % n]
    for i in range(n):
        s.append("<rect x='%.1f' y='10' width='%.1f' height='40' fill='%s' stroke='%s' stroke-width='2'/>" % (10 + i * w, w, "#fbbf24" if i < shaded else "#ffffff", INK))
    s.append("</svg>")
    return "".join(s)


def bars2(n, k):
    """two wholes, each a bar cut into n parts; k parts shaded in all."""
    w = 280 / float(n)
    s = ["<svg viewBox='0 0 300 110' width='300' role='img' aria-label='two bars, each cut into %d equal parts'>" % n]
    for row in range(2):
        for i in range(n):
            on = row * n + i < k
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='40' fill='%s' stroke='%s' stroke-width='2'/>" % (10 + i * w, 8 + row * 52, w, "#fbbf24" if on else "#ffffff", INK))
    s.append("</svg>")
    return "".join(s)


NAME = {2: ("half", "halves"), 4: ("fourth", "fourths"), 8: ("eighth", "eighths")}
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen"]


def one_eighths(r):
    n = r.choice([2, 4, 8, 8])
    k = r.randint(1, n - 1)
    pic = fig(circle_svg(n, k) if r.random() < 0.5 else bar_svg(n, k))
    right = "%s %s" % (NUM[k], NAME[n][0] if k == 1 else NAME[n][1])
    w = ["%s %s" % (NUM[n - k], NAME[n][0] if n - k == 1 else NAME[n][1]) if n - k != k else "%s %s" % (NUM[k], NAME[n * 2 if n < 8 else 4][1]), "%s %s" % (NUM[k], NAME[4 if n == 8 else 8][1]), "%s %s" % (NUM[n], NAME[n][1])]
    w = [x for x in dict.fromkeys(w) if x != right]
    if len(w) < 3:
        w.append("%s %s" % (NUM[k + 1], NAME[n][1]))
    return mcq(pic + "What part is shaded?", right, w[:3], "The whole has %d equal parts called %s. %d %s shaded: <b>%s</b>." % (n, NAME[n][1], k, "is" if k == 1 else "are", right))


def one_size(r):
    a, b = r.sample([2, 4, 8], 2)
    thing = r.choice(["pizza", "sandwich", "tortilla", "pan of cornbread"])
    big = a if a < b else b
    return mcq("Two same-size %ss are cut into equal parts. One is cut into %s, the other into %s. Which has the bigger pieces?" % (thing, NAME[a][1], NAME[b][1]), "The one cut into %s" % NAME[big][1],
               ["The one cut into %s" % NAME[max(a, b)][1], "The pieces are the same size", "You cannot tell"],
               "<b>Fewer parts</b> means bigger parts. %s are bigger than %s." % (NAME[big][1].capitalize(), NAME[max(a, b)][1]))


def one_beyond(r):
    n = r.choice([2, 4, 8])
    k = r.randint(n + 1, 2 * n)
    pic = fig(bars2(n, k))
    kind = r.choice(["count", "count", "whole", "two", "more"])
    if kind == "two":
        return mcq("How many %s make two wholes?" % NAME[n][1], str(2 * n), [str(n), str(n + 2), str(2 * n + 2)], "%d %s make one whole, so <b>%d</b> make two wholes." % (n, NAME[n][1], 2 * n))
    if kind == "more":
        return mcq("Is %s %s more than, less than or equal to one whole?" % (NUM[k], NAME[n][1]), "More than one whole" if k > n else "Equal to one whole",
                   ["Less than one whole", "Equal to one whole" if k > n else "More than one whole", "It is zero"],
                   "%d %s make one whole. %s %s is %s." % (n, NAME[n][1], NUM[k].capitalize(), NAME[n][1], "<b>more than one whole</b>" if k > n else "<b>one whole</b>"))
    if kind == "count":
        right = "%s %s" % (NUM[k], NAME[n][1])
        return mcq(pic + "Each bar is one whole. How many %s are shaded in all?" % NAME[n][1], right, ["%s %s" % (NUM[k - n], NAME[n][1]), "%s %s" % (NUM[n], NAME[n][1]), "%s %s" % (NUM[min(k + 1, 16)], NAME[n][1])],
                   "One whole is %s %s, plus %s more: <b>%s</b>." % (NUM[n], NAME[n][1], NUM[k - n], right))
    return mcq("How many %s make one whole?" % NAME[n][1], str(n), [str(n * 2), str(n // 2) if n > 2 else "1", str(n + 1)], "<b>%d %s</b> make one whole." % (n, NAME[n][1]))


def build():
    sets, R = build_sets([
        ("Equal parts or not?", [("run", resolved(shr.set_equal), ("rnd",), 20, no_thirds)]),
        ("Halves and fourths", [("run", resolved(shr.set_names), ("rnd",), 20, no_thirds)]),
        ("Halves, fourths and eighths", [("collect", one_eighths, 20)]),
        ("More parts, smaller parts", [("collect", one_size, 6), ("run", resolved(shr.set_whole), ("rnd",), 14, no_thirds)]),
        ("Counting parts beyond one whole", [("collect", one_beyond, 20)]),
    ], 69212)
    finish(sets, R)
    body = lesson('<ul><li>A fraction part must be one of several <b>equal</b> parts.</li><li>2 equal parts are <b>halves</b>, 4 are <b>fourths</b>, 8 are <b>eighths</b>.</li><li>The <b>more parts</b> a whole is cut into, the <b>smaller</b> each part.</li><li>2 halves, 4 fourths or 8 eighths make one whole. Five fourths is one whole and one more fourth.</li></ul>',
        [example("A pizza is cut into 8 equal slices. 3 are eaten.", ["8 equal parts are eighths"], "three eighths")],
        [['Calling unequal parts fourths', 'Fourths must be 4 equal parts.'], ['Thinking more parts make bigger parts', 'Eighths are smaller than fourths.'], ['Not knowing what makes a whole', '4 fourths make 1 whole.']])
    faq = [('What does TEKS 2.3A ask?', 'Partition objects into equal parts and name the parts, including halves, fourths and eighths, using words.'), ('What does TEKS 2.3B ask?', 'Explain that the more fractional parts used to make a whole, the smaller the part; and the fewer the fractional parts, the larger the part.'), ('What does TEKS 2.3C ask?', 'Use concrete models to count fractional parts beyond one whole using words and recognize how many parts it takes to equal one whole.'), ('What does TEKS 2.3D ask?', 'Identify examples and non-examples of halves, fourths and eighths.')]
    make('halves-fourths-and-eighths', 12, 'Number and Operations', '2.3A, 2.3B, 2.3C, 2.3D',
         '2.3A partition objects into equal parts and name the parts, including halves, fourths, and eighths, using words; 2.3B explain that the more fractional parts used to make a whole, the smaller the part; and the fewer the fractional parts, the larger the part; 2.3C use concrete models to count fractional parts beyond one whole using words and recognize how many parts it takes to equal one whole; 2.3D identify examples and non-examples of halves, fourths, and eighths',
         'Halves, Fourths and Eighths', 'Halves, Fourths and Eighths',
         'Free Grade 2 fraction worksheets for Texas TEKS 2.3: equal parts, halves, fourths and eighths, more parts make smaller parts and counting parts beyond one whole. 100 questions with answers.',
         'Halves, fourths and eighths are equal parts of a whole.', 'More parts make smaller parts. 4 fourths make one whole.',
         body, faq, sets, seo_title='Grade 2 Halves, Fourths and Eighths Worksheets (TEKS 2.3)')


if __name__ == "__main__":
    build()
