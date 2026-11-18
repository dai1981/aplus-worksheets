# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Similar Figures: Ratios Within and Between Shapes (TEKS 7.5A, 7.5C)
  python3 tools/gen_ustx_math_g7_similar_figures.py
Scale factor and missing sides, ratios within and between similar shapes, angles of similar triangles, perimeter of
similar figures, and mixed problems (US Grade 8 makers with a new seed, plus own makers).
Wrong answers come from real mistakes: adding instead of multiplying, matching the wrong sides, and thinking angles
change with size.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_congruence_and_similarity as cs
adopt(cs)
cs.R = random.Random(670100)
tx_common.GRADE = "grade-7"

INK = "#1f2937"


def rect_pair(a, b, k):
    W = 330
    s1 = 10.0
    while (a + b * k) * s1 > 260 or max(b, a) * k * s1 > 140:
        s1 *= 0.8
    while (a + a * k) * s1 < 140 and max(b, b * k) * s1 < 70:
        s1 *= 1.2
    w1, h1, w2, h2 = a * s1, b * s1, a * k * s1, b * k * s1
    H = int(max(h1, h2) + 50)
    s = ["<svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='two similar rectangles'>" % (W, H, W)]
    s.append("<rect x='20' y='%.1f' width='%.1f' height='%.1f' fill='#dbeafe' stroke='%s' stroke-width='2'/>" % (H - 30 - h1, w1, h1, INK))
    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#fde68a' stroke='%s' stroke-width='2'/>" % (60 + w1, H - 30 - h2, w2, h2, INK))
    return s, H, w1, h1, w2, h2


def one_within(r):
    a, b = r.sample([2, 3, 4, 5, 6, 8, 9, 10, 12], 2)
    k = r.choice([2, 3, 4, 1.5, 2.5])
    A, B = a * k, b * k
    if A != int(A) or B != int(B):
        return None
    A, B = int(A), int(B)
    if r.random() < 0.5:
        return mcq("Rectangle P is %d cm by %d cm. Rectangle Q is similar, and its length is %d cm. What is the ratio of length to width in rectangle Q?" % (a, b, A), "%d : %d" % (a, b), ["%d : %d" % (A, b), "%d : %d" % (a, A), "%d : %d" % (b, a)],
                   "Similar shapes have the <b>same ratio within</b> each shape: length : width = %d : %d in both." % (a, b))
    return mcq("Two similar triangles have matching sides %d m and %d m. What is the ratio of the sides of the small triangle to the big triangle?" % (a, A), "1 : %s" % ("%g" % k), ["%d : %d" % (a, A + a), "%s : 1" % ("%g" % k), "1 : %d" % (A - a)],
               "%d : %d = 1 : %s. This ratio <b>between</b> the shapes is the scale factor." % (a, A, "%g" % k))


def one_missing(r):
    a, b = r.sample([3, 4, 5, 6, 8, 9, 10, 12], 2)
    k = r.choice([2, 3, 4, 1.5, 2.5])
    A, B = a * k, b * k
    if A != int(A) or B != int(B):
        return None
    A, B = int(A), int(B)
    s, H, w1, h1, w2, h2 = rect_pair(a, b, k)
    s.append("<text x='%.1f' y='%d' font-size='13' text-anchor='middle' fill='%s'>%d ft</text>" % (20 + w1 / 2, H - 12, INK, a))
    s.append("<text x='%.1f' y='%.1f' font-size='13' text-anchor='end' fill='%s'>%d ft</text>" % (16, H - 30 - h1 / 2 + 4, INK, b))
    s.append("<text x='%.1f' y='%d' font-size='13' text-anchor='middle' fill='%s'>%d ft</text>" % (60 + w1 + w2 / 2, H - 12, INK, A))
    s.append("<text x='%.1f' y='%.1f' font-size='13' fill='%s'>x</text></svg>" % (64 + w1 + w2, H - 30 - h2 / 2 + 4, INK))
    return mcq(fig("".join(s)) + "The rectangles are similar. Find x.", "%d ft" % B, ["%d ft" % (b + A - a), "%d ft" % (A * b // a + 1) if A * b % a == 0 else "%d ft" % (B + 2), "%d ft" % (b * A)],
               "Scale factor = %d ÷ %d = %s. x = %d × %s = <b>%d ft</b>." % (A, a, "%g" % k, b, "%g" % k, B))


def one_perim(r):
    a, b, c = sorted(r.sample(range(3, 13), 3))
    if a + b <= c:
        return None
    k = r.choice([2, 3, 4])
    p = a + b + c
    if r.random() < 0.5:
        return mcq("A triangle has sides %d in., %d in. and %d in. A similar triangle is %d times as large. What is its perimeter?" % (a, b, c, k), "%d in." % (p * k), ["%d in." % (p + k), "%d in." % p, "%d in." % (p * k * k)],
                   "Each side is multiplied by %d, so the perimeter is %d × %d = <b>%d in.</b>" % (k, p, k, p * k))
    return mcq("Two similar triangles have a scale factor of %d. The small one has a perimeter of %d cm. What is the perimeter of the large one?" % (k, p), "%d cm" % (p * k), ["%d cm" % (p + k), "%d cm" % (p * k * k), "%d cm" % (p // k if p % k == 0 else p - k)],
               "Perimeters grow by the same scale factor: %d × %d = <b>%d cm</b>." % (p, k, p * k))


def build():
    sets, R = build_sets([
        ("Ratios within and between similar shapes", [("collect", one_within, 20)]),
        ("Find a missing side", [("collect", one_missing, 20)]),
        ("Scale factor and missing sides", [("run", cs.set_sides, (), 20)]),
        ("Angles of similar triangles", [("run", cs.set_angles, (), 20)]),
        ("Perimeter and mixed problems", [("collect", one_perim, 10), ("run", cs.set_mixed, (), 10)]),
    ], 67010)
    finish(sets, R)
    body = lesson('<ul><li><b>Similar</b> figures have the same shape: matching angles are equal and matching sides are proportional.</li><li>The <b>ratio between</b> shapes (big side ÷ matching small side) is the <b>scale factor</b>.</li><li>The <b>ratio within</b> one shape (length : width) is the same in both shapes.</li><li>Perimeters change by the scale factor too.</li></ul>',
        [example("5 ft by 8 ft rectangle; similar one has short side 15 ft.", ["Scale factor 15 ÷ 5 = 3", "8 × 3"], "24 ft")],
        [['Adding instead of multiplying', '5 → 15 is × 3, not + 10.'], ['Matching the wrong sides', 'Match shortest with shortest and longest with longest.'], ['Thinking angles change with size', 'Similar shapes have equal angles.']])
    faq = [('What does TEKS 7.5A ask?', 'Generalize the critical attributes of similarity, including ratios within and between similar shapes.'), ('What does TEKS 7.5C ask?', 'Solve mathematical and real-world problems involving similar shape and scale drawings.'), ('Are all squares similar?', 'Yes. All their angles are 90° and their sides are always in the ratio 1 : 1.'), ('Do similar shapes have the same area?', 'No. Area changes by the scale factor squared.')]
    make('similar-figures', 10, 'Proportionality', '7.5A, 7.5C',
         '7.5A generalize the critical attributes of similarity, including ratios within and between similar shapes; 7.5C solve mathematical and real-world problems involving similar shape and scale drawings',
         'Similar Figures: Ratios Within and Between Shapes', 'Similar Figures',
         'Free Grade 7 worksheets for Texas TEKS 7.5A and 7.5C: similar figures, ratios within and between shapes, scale factor, missing sides, angles and perimeter. 100 questions with answers.',
         'Similar: equal angles, proportional sides.', 'Scale factor = big side ÷ matching small side.',
         body, faq, sets, seo_title='Grade 7 Similar Figures Worksheets: Scale Factor and Missing Sides (TEKS 7.5A, STAAR)')


if __name__ == "__main__":
    build()
