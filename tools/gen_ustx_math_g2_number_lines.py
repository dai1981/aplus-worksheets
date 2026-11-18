# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Numbers on a Number Line (TEKS 2.2E, 2.2F, 2.9C)
  python3 tools/gen_ustx_math_g2_number_lines.py
Naming the number at a point, number lines that count by 2s, 5s, 10s and 100s, finding where a number goes, and
distances on a number line (own makers with number line pictures).
Wrong answers come from real mistakes: counting the tick marks instead of the jumps, using the wrong step, and
starting from 0 when the line starts somewhere else.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-2"

INK = "#1f2937"


def nl_svg(lo, step, n, marks, labels_at=None):
    """number line from lo with n steps of size step; marks = [(label, value)]; labels_at = values to print."""
    W, x0, x1 = 340, 38, 302
    hi = lo + step * n
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / float(hi - lo)
    labels_at = labels_at if labels_at is not None else [lo, hi]
    s = ["<svg viewBox='0 0 %d 90' width='%d' data-pf='lg' role='img' aria-label='number line'>" % (W, W)]
    s.append("<line x1='%d' y1='50' x2='%d' y2='50' stroke='%s' stroke-width='2'/>" % (x0 - 8, x1 + 8, INK))
    for i in range(n + 1):
        v = lo + i * step
        s.append("<line x1='%.1f' y1='42' x2='%.1f' y2='58' stroke='%s' stroke-width='2'/>" % (sx(v), sx(v), INK))
        if v in labels_at:
            s.append("<text x='%.1f' y='78' font-size='13' text-anchor='middle' fill='%s'>%s</text>" % (sx(v), INK, comma(v)))
    for lab, v in marks:
        s.append("<circle cx='%.1f' cy='50' r='6' fill='#2563eb'/><text x='%.1f' y='30' font-size='15' font-weight='bold' text-anchor='middle' fill='#2563eb'>%s</text>" % (sx(v), sx(v), lab))
    s.append("</svg>")
    return fig("".join(s))


def one_name(r, steps=(1, 2)):
    step = r.choice(steps)
    n = 10
    lo = r.randrange(0, 1200 - step * n, step)
    if step >= 10:
        lo = lo // step * step
    k = r.randint(1, n - 1)
    v = lo + k * step
    labels = [lo, lo + 5 * step, lo + n * step]
    if k == 5:
        return None
    pic = nl_svg(lo, step, n, [("A", v)], labels)
    w = [v + step, v - step, lo + k, v + 1] if step > 1 else [v + 1, v - 1, v + 2, v + 10]
    w = [comma(x) for x in dict.fromkeys(w) if x != v and x >= 0]
    return mcq(pic + "What number is at point A?", comma(v), w[:3], "Each jump is %d. Count from %s: A is <b>%s</b>." % (step, comma(lo), comma(v)))


def one_name_big(r):
    return one_name(r, (5, 10, 100) if r.random() < 0.6 else (10, 100))


def one_locate(r):
    step = r.choice([1, 2, 5, 10])
    n = 10
    lo = r.randrange(0, 1100, 10)
    ks = sorted(r.sample(range(1, n), 4))
    vals = [lo + k * step for k in ks]
    labs = "ABCD"
    pic = nl_svg(lo, step, n, list(zip(labs, vals)), [lo, lo + n * step])
    i = r.randrange(4)
    return mcq(pic + "Which point shows %s?" % comma(vals[i]), "Point %s" % labs[i], ["Point %s" % l for l in labs if l != labs[i]],
               "Count by %ds from %s. %s is at <b>point %s</b>." % (step, comma(lo), comma(vals[i]), labs[i]))


def one_dist(r):
    a = r.randint(0, 90)
    b = a + r.randint(5, 60)
    step = 10
    lo = a // 10 * 10
    hi = (b + 9) // 10 * 10
    if hi - lo > 100 or hi == lo:
        return None
    n = (hi - lo) // step
    pic = nl_svg(lo, step, n, [("A", a), ("B", b)], list(range(lo, hi + 1, step)))
    return mcq(pic + "How far is it from point A (%d) to point B (%d)?" % (a, b), "%d units" % (b - a), ["%d units" % (a + b), "%d units" % (b - a + 10), "%d units" % b],
               "%d − %d = <b>%d units</b>." % (b, a, b - a))


def one_story(r):
    k = Kid(r).next()
    a = r.randint(5, 60)
    j = r.randint(10, 40)
    if r.random() < 0.5:
        return mcq("%s starts at %d on a number line and jumps %d to the right. Where does %s land?" % (k["n"], a, j, k["he"]), str(a + j), [str(a - j) if a > j else str(a + j + 10), str(a + j + 1), str(j)],
                   "%d + %d = <b>%d</b>." % (a, j, a + j))
    b = a + j
    return mcq("%s walks from the 0-foot mark to the %d-foot mark on a track. Then %s walks back to the %d-foot mark. How far back did %s walk?" % (k["n"], b, k["he"], a, k["he"]), "%d feet" % j, ["%d feet" % b, "%d feet" % (a + b), "%d feet" % a],
               "%d − %d = <b>%d feet</b>." % (b, a, j))


def build():
    sets, R = build_sets([
        ("What number is at the point?", [("collect", one_name, 20)]),
        ("Count by 5s, 10s and 100s", [("collect", one_name_big, 20)]),
        ("Where does the number go?", [("collect", one_locate, 20)]),
        ("Distance on a number line", [("collect", one_dist, 20)]),
        ("Number line stories", [("collect", one_story, 20)]),
    ], 69203)
    finish(sets, R)
    body = lesson('<ul><li>Find the <b>step</b>: how much each jump between tick marks is worth.</li><li>Start at a number you know and count the jumps.</li><li>On a number line, numbers get bigger to the right.</li><li>The distance between two numbers is the bigger number minus the smaller one.</li></ul>',
        [example("Line from 300 to 400 with 10 jumps", ["Each jump is 10", "A is 4 jumps after 300"], "340")],
        [['Counting the tick marks instead of the jumps', 'Count the spaces between marks.'], ['Using the wrong step', "Check the labels to find each jump's value."], ['Starting from 0', 'Start at the first number on the line.']])
    faq = [('What does TEKS 2.2E ask?', 'Locate the position of a given whole number on an open number line.'), ('What does TEKS 2.2F ask?', 'Name the whole number that corresponds to a specific point on a number line.'), ('What does TEKS 2.9C ask?', 'Represent whole numbers as distances from any given location on a number line.'), ('What is an open number line?', 'A line with only a few numbers, where you place the others yourself.')]
    make('number-lines', 3, 'Number and Operations', '2.2E, 2.2F, 2.9C',
         '2.2E locate the position of a given whole number on an open number line; 2.2F name the whole number that corresponds to a specific point on a number line; 2.9C represent whole numbers as distances from any given location on a number line',
         'Numbers on a Number Line', 'Number Lines',
         'Free Grade 2 number line worksheets for Texas TEKS 2.2E, 2.2F and 2.9C: name points, count by 2s, 5s, 10s and 100s, locate numbers and find distances. 100 questions with answers.',
         'Find the size of each jump, then count.', '300 to 400 in 10 jumps: each jump is 10.',
         body, faq, sets, seo_title='Grade 2 Number Line Worksheets (TEKS 2.2E, 2.2F)')


if __name__ == "__main__":
    build()
