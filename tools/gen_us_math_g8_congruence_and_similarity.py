# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Congruence and Similarity (8.G.A.2, 8.G.A.4, 8.G.A.5)
  python3 tools/gen_us_math_g8_congruence_and_similarity.py
Congruent figures (same size and shape: rigid motions), similar figures (same shape: rigid motions and
a dilation), sequences of moves, scale factors and missing sides, angle-angle similarity and shadow
problems. Wrong answers come from real mistakes: adding the difference instead of multiplying by the
scale factor, matching the wrong sides, and thinking similar means congruent.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, svg_wrap, text, RED, BLUE, GREEN, INK, FILL
from g8_common import grid_svg, sl

R = random.Random(81201)
UPDATED = "2026-11-16"
CONG, SIM, NEITHER = "Congruent", "Similar but not congruent", "Neither"


def two_tri(t1, t2, l1=(), l2=()):
    """Two triangles side by side; t1/t2 = point lists scaled already, labels: [(x, y, text)]."""
    W, H = 380, 200
    s = []
    for pts, col, labs, dx in [(t1, RED, l1, 0), (t2, BLUE, l2, 190)]:
        s.append("<polygon points='%s' fill='%s' fill-opacity='0.25' stroke='%s' stroke-width='2.2'/>"
                 % (" ".join("%.1f,%.1f" % (x + dx, y) for x, y in pts), col, col))
        for x, y, t in labs:
            s.append(text(x + dx, y, t, 14, col=RED if t.startswith("?") else INK))
    return svg_wrap(W, H, "".join(s), "two triangles")


# ============================================================ set 1: congruent or similar on a grid
def set_grid():
    its = []
    base = [(1, 1), (4, 1), (1, 3)]
    cases = [
        ([(-x, y) for x, y in base], CONG, "It is a reflection over the y-axis, so the size and shape stay the same."),
        ([(2 * x, 2 * y) for x, y in base], SIM, "Every side is twice as long (a dilation by 2): same shape, different size."),
        ([(x - 6, y - 5) for x, y in base], CONG, "It is a translation: only the position changes."),
        ([(-x, -y) for x, y in base], CONG, "It is a rotation of 180°: same size and shape."),
        ([(-1, -1), (-4, -1), (-1, -5)], NEITHER, "One leg changed from 2 to 4 but the other stayed 3: the shape changed."),
        ([(1, -2), (5, -2), (1, -5)], NEITHER, "The legs are 4 and 3 instead of 3 and 2: not the same shape."),
        ([(-y, x) for x, y in base], CONG, "It is a 90° rotation: same size and shape."),
        ([(-2 * x, -2 * y) for x, y in base], SIM, "It is dilated by 2 and turned 180°: same shape, bigger size."),
    ]
    for img, ans, why in cases:
        svg = grid_svg(-7, 7, polys=[(base, "#c0392b", RED), (img, "#1f5fa8", BLUE)], unit=16)
        q = fig(svg) + "How are the red and blue triangles related?"
        its.append(mcq(q, (ans, ans), [(c, c) for c in [CONG, SIM, NEITHER, "They are the same triangle"] if c != ans],
                       why + " <b>%s</b>." % ans))
    for q, ans, wr, e in [
        ("Which moves always give a congruent figure?", "Translations, reflections and rotations", ["Dilations", "Only reflections", "Any move"],
         "These rigid motions keep size and shape: <b>translations, reflections and rotations</b>."),
        ("Two figures are similar. Which must be true?", "Their angles are equal", ["Their sides are equal", "Their areas are equal", "They are in the same place"],
         "Similar figures have the same shape: <b>their angles are equal</b> and their sides are in proportion."),
        ("Are all congruent figures similar?", "Yes, with scale factor 1", ["No, never", "Only triangles", "Only if they are moved"],
         "Same size and shape means also same shape: <b>yes, with scale factor 1</b>."),
        ("Are all similar figures congruent?", "No, they can be different sizes", ["Yes, always", "Only squares", "Only circles"],
         "A small square and a big square are similar but not congruent: <b>no, they can be different sizes</b>."),
        ("Are any two squares similar?", "Yes, always", ["No, never", "Only if they are the same size", "Only if they touch"],
         "All squares have 4 right angles and sides in the same ratio: <b>yes, always</b>."),
        ("Are any two rectangles similar?", "Not always", ["Yes, always", "Never", "Only if they have equal perimeters"],
         "A 1 × 2 rectangle and a 1 × 5 rectangle have different shapes: <b>not always</b>."),
        ("A figure is dilated by 3 and then rotated. Compared with the first figure, the result is …", "similar", ["congruent", "neither", "the same size"],
         "The dilation changes the size, the rotation keeps the shape: <b>similar</b>."),
        ("A figure is reflected and then translated. Compared with the first figure, the result is …", "congruent", ["similar but not congruent", "bigger", "neither"],
         "Both moves are rigid: <b>congruent</b>."),
        ("Two triangles have sides 3, 4, 5 and 6, 8, 10. How are they related?", SIM, [CONG, NEITHER, "They are the same triangle"],
         "Each side doubled: scale factor 2. <b>%s</b>." % SIM),
        ("Two triangles have sides 3, 4, 5 and 5, 4, 3. How are they related?", CONG, [SIM, NEITHER, "We cannot tell"],
         "The same three side lengths: <b>%s</b>." % CONG),
        ("Two triangles have sides 3, 4, 5 and 4, 5, 6. How are they related?", NEITHER, [CONG, SIM, "They are the same triangle"],
         "4/3, 5/4 and 6/5 are not equal: <b>%s</b>." % NEITHER),
        ("A photo 4 in. × 6 in. is enlarged to 8 in. × 12 in. Is the enlargement similar?", "Yes, scale factor 2", ["No, it is bigger", "Yes, scale factor 4", "No, the sides changed"],
         "8/4 = 12/6 = 2: <b>yes, scale factor 2</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[8], o[0], o[1], o[9], o[2], o[16], o[3], o[17], o[4], o[18], o[10], o[5], o[11], o[19], o[6], o[12], o[7],
             o[13], o[14], o[15]]
    return {"title": "Congruent or similar?", "items": order}


# ============================================================ set 2: sequences of moves
def set_moves():
    its = []
    for (a, b), (ans, wr, e) in [
        (((1, 2), (4, 2)), ("A translation 3 units right", ["A reflection over the y-axis", "A rotation of 90°", "A dilation by 4"],
                            "Every point moves 3 to the right: <b>a translation 3 units right</b>.")),
        (((2, 3), (-2, 3)), ("A reflection over the y-axis", ["A reflection over the x-axis", "A translation 4 units up", "A dilation by −1"],
                             "x changes sign, y stays: <b>a reflection over the y-axis</b>.")),
        (((2, 3), (-2, -3)), ("A rotation of 180° about the origin", ["A reflection over the x-axis", "A translation 4 units left", "A dilation by 2"],
                              "Both signs change: <b>a rotation of 180° about the origin</b>.")),
        (((2, 3), (6, 9)), ("A dilation by 3 from the origin", ["A translation 4 right and 6 up only", "A rotation of 90°", "A reflection over the x-axis"],
                            "Both coordinates are multiplied by 3: <b>a dilation by 3 from the origin</b>.")),
        (((2, 3), (3, -2)), ("A rotation of 90° clockwise about the origin", ["A rotation of 90° counterclockwise", "A reflection over the x-axis", "A translation"],
                             "(x, y) → (y, −x) is <b>a rotation of 90° clockwise about the origin</b>.")),
        (((2, 3), (-3, 2)), ("A rotation of 90° counterclockwise about the origin", ["A rotation of 90° clockwise", "A reflection over the y-axis", "A translation"],
                             "(x, y) → (−y, x) is <b>a rotation of 90° counterclockwise about the origin</b>.")),
    ]:
        q = "Point %s is mapped to %s. Which single move could do this?" % (B("(%s, %s)" % (num(a[0]), num(a[1]))), B("(%s, %s)" % (num(b[0]), num(b[1]))))
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for start, steps, end_ in [((1, 2), ["reflect over the x-axis", "translate 3 right"], (4, -2)),
                               ((3, 1), ["rotate 180° about the origin", "translate 2 up"], (-3, 1)),
                               ((2, 4), ["dilate by 1/2 from the origin", "reflect over the y-axis"], (-1, 2)),
                               ((-1, 3), ["translate 4 right", "reflect over the x-axis"], (3, -3)),
                               ((4, -2), ["reflect over the y-axis", "rotate 180° about the origin"], (4, 2)),
                               ((1, 1), ["dilate by 3 from the origin", "translate 1 left and 2 down"], (2, 1)),
                               ((5, 0), ["rotate 90° counterclockwise about the origin", "translate 2 left"], (-2, 5)),
                               ((-2, -3), ["reflect over the x-axis", "reflect over the y-axis"], (2, 3))]:
        q = "Start at %s. First %s, then %s. Where does the point end?" % (B("(%s, %s)" % (num(start[0]), num(start[1]))), steps[0], steps[1])
        e = "Do the moves in order. The point ends at <b>(%s, %s)</b>." % (num(end_[0]), num(end_[1]))
        wr = [(-end_[0], end_[1]), (end_[0], -end_[1]), (end_[1], end_[0]), (-end_[0], -end_[1])]
        its.append(mcq(q, ("(%s, %s)" % (num(end_[0]), num(end_[1])), end_),
                       [("(%s, %s)" % (num(w[0]), num(w[1])), w) for w in wr], e))
    for q, ans, wr, e in [
        ("To show two figures are congruent, you need …", "a sequence of rigid motions that maps one onto the other",
         ["a dilation that maps one onto the other", "the same color", "the same position"], "Congruent means <b>a sequence of rigid motions that maps one onto the other</b>."),
        ("To show two figures are similar, you can use …", "rigid motions and one dilation", ["only translations", "only reflections", "a ruler only"],
         "Similar means you can map one onto the other with <b>rigid motions and one dilation</b>."),
        ("Does the order of a translation and a reflection matter?", "Sometimes, it can give a different result", ["Never", "Only for squares", "It always gives the same point"],
         "Reflect then translate can land somewhere else than translate then reflect: <b>sometimes, it can give a different result</b>."),
        ("Triangle ABC ≅ triangle DEF. Which side matches AB?", "DE", ["EF", "DF", "BC"], "Corresponding letters match: A↔D, B↔E, so AB ↔ <b>DE</b>."),
        ("Triangle ABC ~ triangle XYZ. Which angle equals angle B?", "Angle Y", ["Angle X", "Angle Z", "Angle C"], "B is the second letter, Y is the second letter: <b>angle Y</b>."),
        ("A figure is rotated 90° and then rotated 90° again (same direction, same center). One move that does the same is …", "a rotation of 180°",
         ["a reflection", "a translation", "a dilation by 2"], "90° + 90° = <b>a rotation of 180°</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[14], o[3], o[17], o[4], o[5], o[18], o[6], o[15], o[7], o[8], o[19], o[9], o[16], o[10],
             o[11], o[12], o[13]]
    return {"title": "Sequences of moves", "items": order}


# ============================================================ set 3: scale factor and missing sides
def set_sides():
    its = []
    for (a, b, c), k, ask in [((3, 4, 5), 2, 2), ((6, 8, 10), F(1, 2), 1), ((5, 12, 13), 3, 0), ((4, 6, 7), F(3, 2), 2), ((9, 12, 15), F(1, 3), 0),
                              ((2, 5, 6), 4, 1), ((8, 10, 14), F(3, 2), 1), ((7, 7, 10), 2, 2), ((10, 15, 20), F(2, 5), 0), ((6, 9, 12), F(4, 3), 2)]:
        big = [F(a) * k, F(b) * k, F(c) * k]
        known = [i for i in range(3) if i != ask][0]
        sides = [a, b, c]
        t1 = [(20, 170), (20 + 120, 170), (20, 170 - 90)]
        q = ("Triangle 1 has sides %s. A similar Triangle 2 has a side of %s that matches the side of %s. "
             "What is the length in Triangle 2 that matches the side of %s?" % (
                 B("%d, %d and %d" % (a, b, c)), num(big[known]), num(sides[known]), num(sides[ask])))
        e = ("Scale factor = %s ÷ %s = %s. Multiply: %s × %s = <b>%s</b>." % (num(big[known]), num(sides[known]), sl(k),
                                                                            num(sides[ask]), sl(k), num(big[ask])))
        diff = big[known] - sides[known]
        wr = [F(sides[ask]) + diff, F(sides[ask]) / k, big[known], F(sides[ask]) * k + 1]
        its.append(mcq(q, (num(big[ask]), big[ask]), [(num(w) if num(w) else num(w, "f"), w) for w in wr], e))
    for (w1, h1), w2 in [((4, 6), 10), ((3, 5), 12), ((8, 12), 6), ((5, 8), 15), ((6, 9), 4)]:
        k = F(w2, w1)
        h2 = h1 * k
        q = "A %d cm by %d cm rectangle is similar to a rectangle that is %d cm wide. How tall is the larger or smaller rectangle?" % (w1, h1, w2)
        q = "Rectangle A is %d cm wide and %d cm tall. Rectangle B is similar and %d cm wide. How tall is Rectangle B?" % (w1, h1, w2)
        e = "Scale factor = %d ÷ %d = %s. Height = %d × %s = <b>%s cm</b>." % (w2, w1, sl(k), h1, sl(k), num(h2))
        wr = [h1 + (w2 - w1), F(h1) / k, w2, h1 * k + 1]
        its.append(mcq(q, (num(h2) + " cm", h2), [(num(F(x)) + " cm", F(x)) for x in wr if num(F(x))], e))
    for q, ans, wr, e in [
        ("Two similar triangles have scale factor 3. The small one has perimeter 12 cm. What is the perimeter of the large one?", "36 cm",
         ["15 cm", "108 cm", "4 cm"], "Perimeter scales by the same factor: 12 × 3 = <b>36 cm</b>."),
        ("Two similar figures have scale factor 2. The small one has area 10 cm². What is the area of the large one?", "40 cm²",
         ["20 cm²", "12 cm²", "100 cm²"], "Area scales by the square of the factor: 10 × 2² = <b>40 cm²</b>."),
        ("A map uses a scale factor of 1/1,000. A road is 8 cm on the map. How long is it in real life?", "80 m", ["8 m", "800 m", "0.8 m"],
         "8 cm × 1,000 = 8,000 cm = <b>80 m</b>."),
        ("A model car is 1/24 of the real size. The model is 18 cm long. How long is the real car?", "432 cm", ["42 cm", "0.75 cm", "24 cm"],
         "18 × 24 = <b>432 cm</b>."),
        ("Leo says a 2 × 3 rectangle and a 4 × 5 rectangle are similar because he added 2 to each side. Is he right?", "No, you must multiply, not add",
         ["Yes, adding keeps the shape", "Yes, both are rectangles", "No, they are congruent"], "4/2 = 2 but 5/3 ≠ 2: <b>no, you must multiply, not add</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[15], o[3], o[12], o[4], o[16], o[5], o[13], o[6], o[17], o[7], o[14], o[8],
             o[18], o[9], o[19]]
    return {"title": "Scale factor and missing sides", "items": order}


# ============================================================ set 4: angles and AA similarity
def set_angles():
    its = []
    for a, b in [(50, 60), (35, 90), (72, 48), (40, 40), (100, 30), (65, 55), (25, 120), (90, 45)]:
        c = 180 - a - b
        q = "Two triangles are similar. One has angles %d° and %d°. What is the third angle of the other triangle?" % (a, b)
        e = "Similar triangles have equal angles. The third angle is 180° − %d° − %d° = <b>%d°</b>." % (a, b, c)
        its.append(mcq(q, ("%d°" % c, c), [("%d°" % (a + b), a + b), ("%d°" % (360 - a - b), 360 - a - b), ("%d°" % (180 - a), 180 - a), ("%d°" % (180 - b), 180 - b),
                                          ("%d°" % (c + 10), c + 10)], e))
    for (a1, b1), (a2, b2), ok in [((40, 70), (70, 40), True), ((50, 60), (50, 75), False), ((90, 30), (60, 90), True), ((45, 45), (45, 90), True),
                                   ((35, 80), (35, 75), False), ((100, 50), (30, 100), True)]:
        c1, c2 = 180 - a1 - b1, 180 - a2 - b2
        same = sorted([a1, b1, c1]) == sorted([a2, b2, c2])
        assert same == ok
        ans = "Yes, by angle-angle (AA)" if ok else "No, the angles are different"
        q = "Triangle 1 has angles %d° and %d°. Triangle 2 has angles %d° and %d°. Are they similar?" % (a1, b1, a2, b2)
        e = "Find the third angles: %d° and %d°. Triangle 1: %d°, %d°, %d°. Triangle 2: %d°, %d°, %d°. <b>%s</b>." % (
            c1, c2, a1, b1, c1, a2, b2, c2, ans)
        its.append(mcq(q, (ans, ans), [(w, w) for w in ["Yes, by angle-angle (AA)", "No, the angles are different",
                                                         "Yes, all triangles are similar", "We need the side lengths"] if w != ans], e))
    for q, ans, wr, e in [
        ("A 6-ft man casts a 4-ft shadow. At the same time a tree casts a 20-ft shadow. How tall is the tree?", "30 ft", ["22 ft", "13.3 ft", "120 ft"],
         "The triangles are similar: 6/4 = h/20, so h = 20 × 1.5 = <b>30 ft</b>."),
        ("A 1-m stick casts a 1.5-m shadow. A pole casts a 9-m shadow. How tall is the pole?", "6 m", ["13.5 m", "8.5 m", "10.5 m"],
         "1/1.5 = h/9, so h = 9 ÷ 1.5 = <b>6 m</b>."),
        ("A 5-ft girl casts a 3-ft shadow. A flagpole casts a 12-ft shadow. How tall is the flagpole?", "20 ft", ["14 ft", "7.2 ft", "36 ft"],
         "5/3 = h/12, so h = 12 × 5/3 = <b>20 ft</b>."),
        ("Why are two triangles with two equal angles always similar?", "The third angles must also be equal", ["Because all triangles are similar",
         "Because their sides are equal", "Because they are congruent"], "Angles add to 180°, so the third angles match too: <b>the third angles must also be equal</b>."),
        ("A line parallel to one side of a triangle cuts off a small triangle. Is the small triangle similar to the big one?", "Yes, they share angles",
         ["No, it is smaller", "Only if it is half", "No, the sides change"], "Parallel lines make equal corresponding angles: <b>yes, they share angles</b>."),
        ("Two right triangles each have a 30° angle. Are they similar?", "Yes", ["No", "Only if the hypotenuses are equal", "We cannot tell"],
         "Both have 90° and 30° (so also 60°): AA. <b>Yes</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[8], o[1], o[9], o[17], o[2], o[10], o[3], o[11], o[18], o[4], o[12], o[14], o[5], o[13], o[15], o[6],
             o[16], o[7], o[19]]
    return {"title": "Angles and AA similarity", "items": order}


# ============================================================ set 5: mixed reasoning
def set_mixed():
    its = []
    for (a, b, c), (d, e_, f), ans in [((3, 4, 5), (9, 12, 15), "Similar, scale factor 3"), ((2, 2, 3), (2, 3, 2), CONG),
                                       ((5, 6, 7), (10, 12, 15), NEITHER), ((4, 4, 4), (7, 7, 7), "Similar, scale factor 7/4"),
                                       ((6, 8, 9), (3, 4, 4.5), "Similar, scale factor 1/2"), ((5, 5, 8), (10, 10, 12), NEITHER)]:
        q = "Triangle A has sides %s. Triangle B has sides %s. How are they related?" % (B("%s, %s, %s" % (a, b, c)), B("%s, %s, %s" % (d, e_, f)))
        r = [F(str(x)) / F(str(y)) for x, y in zip(sorted([d, e_, f]), sorted([a, b, c]))]
        e = "Compare matching sides (smallest with smallest): ratios %s. " % ", ".join(num(x, "f") for x in r)
        e += "<b>%s</b>." % ans
        ch = [CONG, NEITHER, "Similar, scale factor 2", "Similar, scale factor 3", "Similar, scale factor 1/2", "Similar, scale factor 7/4"]
        wr = [c_ for c_ in ch if c_ != ans][:3] if ans != CONG else [NEITHER, "Similar, scale factor 2", "Similar, scale factor 1/2"]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for k, perim, area in [(2, 18, 15), (3, 10, 4), (F(1, 2), 40, 64), (4, 7, 2), (5, 12, 6), (F(1, 3), 27, 36)]:
        ks = sl(k)
        newp, newa = perim * F(k), area * F(k) ** 2
        q = "A figure has perimeter %d and area %d. It is dilated by %s. What are the new perimeter and area?" % (perim, area, ks)
        ans = "Perimeter %s, area %s" % (num(newp), num(newa))
        e = "Perimeter × %s = %s. Area × (%s)² = %s. <b>%s</b>." % (ks, num(newp), ks, num(newa), ans)
        wr = ["Perimeter %s, area %s" % (num(newp), num(area * F(k))), "Perimeter %s, area %s" % (num(perim * F(k) ** 2), num(newa)),
              "Perimeter %s, area %s" % (num(perim), num(area))]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("A rectangle is 5 by 8. A similar rectangle has a short side of 15. What is its long side?", "24", ["18", "40", "13"], "Scale factor 3: 8 × 3 = <b>24</b>."),
        ("A triangle’s sides are 6, 9 and 12. A similar triangle’s shortest side is 4. What is its longest side?", "8", ["10", "18", "6"],
         "Scale factor 4/6 = 2/3: 12 × 2/3 = <b>8</b>."),
        ("A door is 2 m tall and 0.8 m wide. A model door is 10 cm tall. How wide is it?", "4 cm", ["8 cm", "12.5 cm", "0.4 cm"],
         "Scale: 10 cm for 200 cm, so 1/20. 80 cm ÷ 20 = <b>4 cm</b>."),
        ("Two similar cylinders: one is twice as tall. How many times as much area does a matching face have?", "4 times", ["2 times", "8 times", "6 times"],
         "Area scales by 2² = <b>4 times</b>."),
        ("Triangle PQR ≅ triangle STU. PQ = 7 cm and angle Q = 50°. Which is true?", "ST = 7 cm and angle T = 50°", ["ST = 7 cm and angle S = 50°",
         "TU = 7 cm and angle T = 50°", "ST = 50 cm"], "P↔S, Q↔T, R↔U, so <b>ST = 7 cm and angle T = 50°</b>."),
        ("A 3-4-5 triangle is dilated by 2.5. What are the new sides?", "7.5, 10, 12.5", ["5.5, 6.5, 7.5", "6, 8, 10", "0.75, 1, 1.25"],
         "Multiply each side by 2.5: <b>7.5, 10, 12.5</b>."),
        ("Ana says two triangles with all sides equal to 5 and all sides equal to 6 are not similar. Is she right?", "No, all equilateral triangles are similar",
         ["Yes, the sides are different", "Yes, 6 is not 5", "No, they are congruent"], "Every equilateral triangle has 60° angles: <b>no, all equilateral triangles are similar</b>."),
        ("A shape is dilated by 1. What is the result?", "A congruent shape", ["A bigger shape", "A smaller shape", "A reflection"],
         "Scale factor 1 keeps the size: <b>a congruent shape</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[12], o[0], o[6], o[13], o[1], o[7], o[14], o[2], o[8], o[15], o[3], o[9], o[16], o[4], o[10], o[17], o[5],
             o[11], o[18], o[19]]
    return {"title": "Mixed reasoning", "items": order}


def body():
    return ("<h2>Congruent and similar</h2>"
            + table(["Word", "Meaning", "Moves"], [
                ["Congruent (≅)", "same size and same shape", "translations, reflections, rotations"],
                ["Similar (~)", "same shape, maybe a different size", "rigid motions plus a dilation"]])
            + "<p>In similar figures, matching <b>angles are equal</b> and matching <b>sides are in proportion</b>. "
            "The <b>scale factor</b> is new side ÷ old side.</p>"
            + example("Triangles 3-4-5 and 6-8-10 are similar. A side of 7 in the first matches what in a similar triangle with scale factor 2?",
                      ["Multiply by the scale factor: 7 × 2."], "14")
            + "<h2>Angle-angle (AA)</h2><p>If two angles of one triangle equal two angles of another, the triangles are similar. "
            "Shadow problems use this: a person and a tree with their shadows make similar triangles.</p>"
            + "<h2>Common mistakes</h2><ul><li>Adding instead of multiplying: a 2 × 3 rectangle doubled is 4 × 6, not 4 × 5.</li>"
            "<li>Matching the wrong sides: match shortest with shortest.</li>"
            "<li>Thinking similar means congruent. Similar figures can be different sizes.</li>"
            "<li>Forgetting that area scales by k², not k.</li></ul>")


def main():
    sets = [set_grid(), set_moves(), set_sides(), set_angles(), set_mixed()]
    balance(sets, R)
    unit = {
        "slug": "congruence-and-similarity",
        "title": "Congruence and Similarity",
        "seo_title": "Grade 8 Congruence and Similarity Worksheets: Rigid Motions, Dilations, Scale Factor, AA",
        "short_title": "Congruence and similarity",
        "domain": "Geometry",
        "standard_code": "8.G.A.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/G/A/4/",
        "standard_text": "Understand that a two-dimensional figure is similar to another if the second can be obtained from the first by a sequence of rotations, reflections, translations, and dilations; given two similar two-dimensional figures, describe a sequence that exhibits the similarity between them.",
        "meta_desc": "Free Grade 8 congruence and similarity worksheets: congruent figures and rigid motions, similar figures and dilations, sequences of moves, scale factors and missing sides, angle-angle similarity and shadow problems. 100 questions with an answer key.",
        "key_big": "Congruent: same size and shape (rigid motions). Similar: same shape (rigid motions and a dilation).",
        "key_sub": "In similar figures, angles are equal and sides are multiplied by the same scale factor.",
        "body_html": body(),
        "faq": [
            {"q": "What is the difference between congruent and similar?", "a": "Congruent figures have the same size and shape. Similar figures have the same shape, but can be different sizes."},
            {"q": "How do you find a missing side in similar figures?", "a": "Find the scale factor by dividing two matching sides, then multiply the side you know by it."},
            {"q": "What is AA similarity?", "a": "If two angles of one triangle are equal to two angles of another, the triangles are similar."},
            {"q": "What happens to area when a figure is dilated?", "a": "Lengths and perimeter are multiplied by the scale factor k, but area is multiplied by k²."}],
        "sets": sets, "pdf_url": "", "sort": 12, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
