# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Systems of Linear Equations: Solving by Graphing (TEKS 8.9A)
  python3 tools/gen_ustx_math_g8_systems.py
Solving by graphing, checking a solution in both equations (own), one, none or infinitely many solutions, solving
by substitution to check, and word problems (US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: reading only one line, checking only one equation, and switching x and y.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_systems_of_equations as sys
adopt(sys)
sys.R = random.Random(680120)
tx_common.GRADE = "grade-8"

from fractions import Fraction as F
from ws_common import num

INK = "#1f2937"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return ("−" if v < 0 else "") + comma(abs(int(a))) + "." + b
    return num(int(s))


def pt(p):
    return "(%s, %s)" % (g(p[0]), g(p[1]))


def one_check(r):
    x, y = r.randint(-6, 6), r.randint(-6, 6)
    m1, m2 = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    b1, b2 = y - m1 * x, y - m2 * x

    def eq(m, b):
        mm = "" if m == 1 else "−" if m == -1 else num(m)
        return "y = %sx%s" % (mm, "" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b))
    cands = [(x, y), (y, x), (x + 1, m1 * (x + 1) + b1), (x, y + 2)]
    cands = [c for c in dict.fromkeys(cands)]
    if len(cands) < 4 or (y, x) == (x, y):
        return None
    return mcq("Which ordered pair is the solution of the system?<br>%s<br>%s" % (eq(m1, b1), eq(m2, b2)), pt((x, y)), [pt(c) for c in cands[1:]],
               "Check both equations: %s = %s × %s %s and %s = %s × %s %s. Only <b>%s</b> works in both." % (num(y), num(m1), "(%s)" % num(x) if x < 0 else num(x), ("+ %d" % b1) if b1 >= 0 else "− %d" % -b1, num(y), num(m2), "(%s)" % num(x) if x < 0 else num(x), ("+ %d" % b2) if b2 >= 0 else "− %d" % -b2, pt((x, y))))


def build():
    sets, R = build_sets([
        ("Solve by graphing", [("run", sys.set_graph, (), 20)]),
        ("Check a solution in both equations", [("collect", one_check, 20)]),
        ("One, none or infinitely many solutions", [("run", sys.set_count, (), 20)]),
        ("Find the intersection with substitution", [("run", sys.set_sub, (), 20)]),
        ("Word problems", [("run", sys.set_words, (), 20)]),
    ], 68012)
    finish(sets, R)
    body = lesson('<ul><li>The <b>solution</b> of a system is the point (x, y) that makes both equations true.</li><li>On a graph, it is where the two lines <b>intersect</b>.</li><li>Check your answer by substituting it into <b>both</b> equations.</li><li>Parallel lines (same slope, different intercepts) have no solution; the same line has infinitely many.</li></ul>',
        [example("y = x + 1 and y = −x + 5", ["Lines cross at (2, 3)", "3 = 2 + 1 ✓, 3 = −2 + 5 ✓"], "(2, 3)")],
        [['Reading a point on only one line', 'The solution is on both lines.'], ['Checking only one equation', 'Substitute into both.'], ['Switching x and y', 'Write (x, y): across, then up.']])
    faq = [('What does TEKS 8.9A ask?', 'Identify and verify the values of x and y that simultaneously satisfy two linear equations in the form y = mx + b from the intersections of the graphed equations.'), ('What if the lines are parallel?', 'They never meet, so there is no solution.'), ('Can a system have two solutions?', 'Not with two different straight lines: they meet at most once.'), ('Why check with substitution?', 'Reading a graph can be off by a little; substitution proves the answer.')]
    make('systems-of-equations', 12, 'Expressions, Equations and Relationships', '8.9A',
         '8.9A identify and verify the values of x and y that simultaneously satisfy two linear equations in the form y = mx + b from the intersections of the graphed equations',
         'Systems of Linear Equations: Solving by Graphing', 'Systems of Equations',
         'Free Grade 8 systems of equations worksheets for Texas TEKS 8.9A: solve by graphing, verify solutions, one, none or infinitely many solutions and word problems. 100 questions with answers.',
         'The solution is where the lines intersect.', 'Check (x, y) in both equations.',
         body, faq, sets, seo_title='Grade 8 Systems of Equations by Graphing Worksheets (TEKS 8.9A, STAAR)')


if __name__ == "__main__":
    build()
