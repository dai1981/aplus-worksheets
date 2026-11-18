# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Similarity and Congruence (Sec 2 Geometry and measures)
  python3 gen_sg_maths_s2_congruence_and_similarity.py
Congruence conditions (SSS, SAS, ASA, RHS), scale factors between similar shapes, missing sides in similar
shapes and triangles, deciding whether shapes are similar, and real-life problems.
Wrong answers come from real mistakes: adding the difference instead of multiplying by the scale factor,
using the scale factor the wrong way round, thinking AAA proves congruence, and matching the wrong sides.
"""
import random
from fractions import Fraction as F
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, text, fig, INK, RED

R = random.Random(821100)


def tri_pair(a, b, c, k, unknown, big_unknown=True):
    """Two similar triangles drawn side by side; a,b,c small sides; scale k. unknown: index of side shown as x."""
    def tri(x0, y0, s, labs):
        A = (x0, y0)
        Bp = (x0 + 110 * s, y0)
        C = (x0 + 30 * s, y0 - 70 * s)
        out = "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % (A + Bp + C + (INK,))
        out += text((A[0] + Bp[0]) / 2, y0 + 20, labs[0], 14, col=RED if labs[0] == "x" else INK, italic=labs[0] == "x")
        out += text((A[0] + C[0]) / 2 - 18, (A[1] + C[1]) / 2, labs[1], 14, col=RED if labs[1] == "x" else INK, italic=labs[1] == "x", anchor="end")
        out += text((Bp[0] + C[0]) / 2 + 12, (Bp[1] + C[1]) / 2, labs[2], 14, col=RED if labs[2] == "x" else INK, italic=labs[2] == "x", anchor="start")
        return out
    small = ["%s cm" % num(v) for v in (a, b, c)]
    big = ["%s cm" % num(v * k) for v in (a, b, c)]
    if big_unknown:
        big = ["x" if i == unknown else (big[i] if i != (unknown + 1) % 3 else "") for i in range(3)]
        big[(unknown + 1) % 3] = "%s cm" % num([a, b, c][(unknown + 1) % 3] * k)
        big[(unknown + 2) % 3] = ""
    else:
        small = ["x" if i == unknown else small[i] for i in range(3)]
        small[(unknown + 2) % 3] = ""
        big = ["%s cm" % num(v * k) if i in (unknown, (unknown + 1) % 3) else "" for i, v in enumerate((a, b, c))]
    s = tri(50, 120, 0.8, small) + tri(220, 150, 1.25, big)
    return svg_wrap(400, 180, s, "two similar triangles, not drawn accurately")


# ------------------------------------------------------------ set 1: congruence
CONDS = [
    ("All three sides of one triangle are equal to all three sides of the other.", "SSS"),
    ("Two sides and the angle between them are equal.", "SAS"),
    ("Two angles and the side between them are equal.", "ASA"),
    ("Both have a right angle, equal hypotenuses and one other equal side.", "RHS"),
    ("Two angles and a side that is not between them are equal (AAS).", "ASA"),
]


def one_congruence(r):
    kind = r.random()
    if kind < 0.6:
        desc, ans = r.choice(CONDS)
        opts = ["SSS", "SAS", "ASA", "RHS", "AAA"]
        q = "Two triangles are congruent. Which condition is this? %s" % B(desc)
        return T(q, ans, [o for o in opts if o != ans][:3] if ans != "ASA" else ["SSS", "SAS", "AAA"], "This is <b>%s</b>." % ans)
    cases = [
        ("Both triangles have angles 40°, 60° and 80°. Are they definitely congruent?", "No — they are similar, but could be different sizes", ["Yes, by AAA", "Yes, by ASA", "No, because the angles are different"],
         "Equal angles only prove the triangles are the same shape: <b>similar, not necessarily congruent</b>."),
        ("Triangle 1 has sides 5, 7, 9 cm. Triangle 2 has sides 9, 5, 7 cm. Are they congruent?", "Yes, by SSS", ["No, the sides are in a different order", "Yes, by RHS", "You cannot tell"],
         "The same three side lengths in any order: <b>yes, by SSS</b>."),
        ("Two triangles each have sides 6 cm and 8 cm with a 50° angle between them. Are they congruent?", "Yes, by SAS", ["Yes, by SSS", "No", "Yes, by RHS"], "Two sides and the included angle: <b>SAS</b>."),
        ("Two right-angled triangles both have a hypotenuse of 13 cm and a side of 5 cm. Are they congruent?", "Yes, by RHS", ["No", "Yes, by SAS", "Only if they face the same way"], "Right angle, hypotenuse, side: <b>RHS</b>."),
        ("Which of these does NOT prove two triangles are congruent?", "AAA", ["SSS", "SAS", "RHS"], "Three equal angles only show the triangles are similar: <b>AAA</b>."),
        ("A shape is reflected. Is the image congruent to the original?", "Yes", ["No, it is reversed", "Only if the mirror line is vertical", "No, it is similar"], "Reflection keeps all lengths and angles, so <b>yes</b>."),
    ]
    q, a, w, e = r.choice(cases)
    return T(q, a, w, e)


# ------------------------------------------------------------ set 2: scale factors and missing sides
def one_sf(r):
    k = r.choice([2, 3, F(3, 2), F(5, 2), 4, F(1, 2), F(4, 3)])
    a = r.randint(2, 12)
    if (a * k).denominator != 1:
        return None
    b = r.randint(2, 15)
    if (b * k).denominator > 2 or a == b:
        return None
    kind = r.random()
    if kind < 0.4:
        q = "Two shapes are similar. A side of %s cm in the small shape matches a side of %s cm in the large shape. What is the scale factor from small to large?" % (num(min(a, a * k)), num(max(a, a * k)))
        kk = max(k, 1 / k)
        return QN(q, kk, [1 / kk, max(a, a * k) - min(a, a * k), kk + 1], "Scale factor = %s ÷ %s = <b>%s</b>." % (num(max(a, a * k)), num(min(a, a * k)), num(kk)))
    q = "Shapes A and B are similar. A side of %d cm in A matches %s cm in B. Another side of A is %d cm. How long is the matching side in B?" % (a, num(a * k), b)
    e = "Scale factor = %s ÷ %d = %s. %d × %s = <b>%s cm</b>." % (num(a * k), a, num(k), b, num(k), num(b * k))
    return QN(q, b * k, [b + (a * k - a), F(b) / k if (F(b) / k).denominator <= 2 else None, b * k + 1], e, unit=" cm", near=(2, -2))


# ------------------------------------------------------------ set 3: similar triangles
def one_tri(r):
    a, b, c = r.choice([(4, 5, 6), (3, 5, 7), (6, 8, 9), (5, 6, 8), (4, 7, 8)])
    k = r.choice([2, 3, F(3, 2), F(5, 2)])
    u = r.randrange(3)
    if r.random() < 0.6:
        known = (u + 1) % 3
        sides = [a, b, c]
        svg = tri_pair(a, b, c, k, u, True)
        x = sides[u] * k
        e = "Matching sides: %s cm → %s cm, so the scale factor is %s. <i>x</i> = %s × %s = <b>%s cm</b>." % (
            num(sides[known]), num(sides[known] * k), num(k), num(sides[u]), num(k), num(x))
        return QN("The triangles are similar. Find %s.%s<small>Not drawn accurately.</small>" % (B("<i>x</i>"), fig(svg)), x, [sides[u] + sides[known] * k - sides[known], sides[u] * k + 1, F(sides[u]) / k], e, unit=" cm")
    sides = [a, b, c]
    svg = tri_pair(a, b, c, k, u, False)
    known = (u + 1) % 3
    x = F(sides[u])
    e = "Scale factor from small to large = %s ÷ %s = %s. Going back to the small triangle, divide: %s ÷ %s = <b>%s cm</b>." % (
        num(sides[known] * k), num(sides[known]), num(k), num(sides[u] * k), num(k), num(x))
    return QN("The triangles are similar. Find %s.%s<small>Not drawn accurately.</small>" % (B("<i>x</i>"), fig(svg)), x, [sides[u] * k * k, sides[u] * k - (sides[known] * k - sides[known]), x + 1], e, unit=" cm")


# ------------------------------------------------------------ set 4: are they similar?
def one_check(r):
    a, b = r.randint(2, 10), r.randint(2, 10)
    if a == b:
        return None
    k = r.choice([2, 3, F(3, 2), F(5, 2)])
    similar = r.random() < 0.5
    c, d = a * k, b * k
    if not similar:
        d = d + r.choice([1, 2, -1])
    if (c.denominator if isinstance(c, F) else 1) > 2 or d <= 0:
        return None
    q = "Rectangle A is %d cm by %d cm. Rectangle B is %s cm by %s cm. Are they similar?" % (a, b, num(c), num(d))
    if similar:
        right = "Yes, both sides are multiplied by %s" % num(k)
        wr = ["No, because the areas are different", "No, because %s − %d ≠ %s − %d" % (num(c), a, num(d), b), "Only if they are squares"]
    else:
        right = "No, the sides are not multiplied by the same number"
        wr = ["Yes, both are rectangles", "Yes, because all the angles are 90°", "Yes, because B is bigger"]
    e = "%s ÷ %d = %s and %s ÷ %d = %s. %s" % (num(c), a, num(F(c) / a), num(d), b, num(F(d) / b),
                                              "<b>The scale factors match, so they are similar.</b>" if similar else "<b>The scale factors differ, so they are not similar.</b>")
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A 1.5 m post casts a 2 m shadow. At the same time a tree casts a 12 m shadow. How tall is the tree?", "9 m", ["11.5 m", "16 m", "18 m"], "Scale factor 12 ÷ 2 = 6. 1.5 × 6 = <b>9 m</b>."),
        ("A photo 10 cm by 15 cm is enlarged so that the short side is 25 cm. How long is the long side?", "37.5 cm", ["30 cm", "40 cm", "16.7 cm"], "Scale factor 2.5. 15 × 2.5 = <b>37.5 cm</b>."),
        ("A model boat is made to a scale of 1 : 50. The model is 60 cm long. How long is the real boat?", "30 m", ["3 m", "300 m", "110 cm"], "60 × 50 = 3000 cm = <b>30 m</b>."),
        ("Two similar triangles have corresponding angles. One triangle has angles 35°, 65° and 80°. What are the angles of the other?", "35°, 65° and 80°", ["70°, 130° and 160°", "They depend on the scale factor", "17.5°, 32.5° and 40°"],
         "Similar shapes have <b>equal angles</b>; only the lengths change."),
        ("In similar triangles, which statement is always true?", "Corresponding angles are equal", ["Corresponding sides are equal", "The areas are equal", "The perimeters are equal"], "Similar means same shape: <b>corresponding angles are equal</b>."),
        ("Are all squares similar?", "Yes", ["No", "Only if they are the same size", "Only if their sides are whole numbers"], "Every square has 90° angles and sides in the ratio 1 : 1, so <b>yes</b>."),
        ("Are all rectangles similar?", "No", ["Yes", "Only if they have the same area", "Only if one is double the other"], "A 1 × 2 rectangle and a 1 × 5 rectangle are different shapes, so <b>no</b>."),
        ("A triangle has sides 3, 4 and 5 cm. A similar triangle has its shortest side 9 cm. What is its longest side?", "15 cm", ["11 cm", "12 cm", "45 cm"], "Scale factor 3. 5 × 3 = <b>15 cm</b>."),
        ("A map uses a scale of 1 : 25 000. A lake is 3.2 cm long on the map. How long is it in real life?", "800 m", ["80 m", "8 km", "78 m"], "3.2 × 25 000 = 80 000 cm = <b>800 m</b>."),
        ("In triangle ABC, DE is parallel to BC. AD = 4 cm, AB = 10 cm and DE = 6 cm. How long is BC?", "15 cm", ["12 cm", "24 cm", "9.6 cm"], "Triangles ADE and ABC are similar with scale factor 10 ÷ 4 = 2.5. BC = 6 × 2.5 = <b>15 cm</b>."),
        ("Triangle P has two sides of 6 cm with an angle of 60° between them. Triangle Q has three sides of 6 cm. Are they congruent?", "Yes — P is also equilateral with sides of 6 cm",
         ["No — P has only two sides given", "No — Q has no angles given", "Only if they face the same way"],
         "P is isosceles with a 60° angle between the equal sides, so all its angles are 60° and its third side is also 6 cm. <b>Yes</b>, they are congruent (SSS)."),
        ("A shape is enlarged by scale factor 3. What happens to the perimeter?", "It is multiplied by 3", ["It is multiplied by 9", "It stays the same", "It increases by 3"], "All lengths × 3, so the perimeter <b>× 3</b>."),
        ("A door 2 m tall is shown as 4 cm on a plan. What is the scale?", "1 : 50", ["1 : 2", "1 : 500", "2 : 4"], "2 m = 200 cm. 200 ÷ 4 = 50: <b>1 : 50</b>."),
        ("A person 1.8 m tall stands 4 m from a lamp post and has a 2 m shadow. How tall is the lamp post?", "5.4 m", ["3.6 m", "7.2 m", "5.8 m"],
         "The big triangle's base is 4 + 2 = 6 m, which is 3 times the 2 m shadow. 1.8 × 3 = <b>5.4 m</b>."),
        ("Two similar cylinders have heights 6 cm and 9 cm. The smaller has radius 4 cm. What is the radius of the larger?", "6 cm", ["7 cm", "13.5 cm", "2.7 cm"], "Scale factor 1.5. 4 × 1.5 = <b>6 cm</b>."),
        ("Which pair of triangles must be similar?", "Two triangles with angles 30°, 70° and 80°", ["Two triangles with a side of 5 cm", "Two isosceles triangles", "Two right-angled triangles"],
         "Equal angles mean <b>similar</b>."),
        ("A rectangle 4 cm by 6 cm is similar to one that is 10 cm by <i>y</i> cm, where 10 cm matches 4 cm. Find <i>y</i>.", "15 cm", ["12 cm", "2.4 cm", "24 cm"], "Scale factor 2.5. <i>y</i> = 6 × 2.5 = <b>15 cm</b>."),
        ("Congruent shapes are…", "exactly the same shape and size", ["the same shape but a different size", "the same area but any shape", "always the same way round"], "Congruent means <b>exactly the same shape and size</b> (they may be reflected or rotated)."),
        ("A triangle with sides 6, 8 and 10 cm is reduced by scale factor ½. What are the new sides?", "3, 4 and 5 cm", ["5.5, 7.5 and 9.5 cm", "12, 16 and 20 cm", "3, 8 and 10 cm"], "Halve every side: <b>3, 4 and 5 cm</b>."),
        ("The scale factor from shape A to shape B is 4. What is the scale factor from B to A?", "¼", ["4", "−4", "16"], "Going back divides by 4, so the scale factor is <b>¼</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p><b>Congruent</b> shapes are identical in shape and size. Two triangles are congruent if they match by "
        "<b>SSS</b>, <b>SAS</b>, <b>ASA</b> or <b>RHS</b>.</p>"
        "<p><b>Similar</b> shapes have equal angles and every length is multiplied by the same <b>scale factor</b>. "
        "Scale factor = new length ÷ matching old length.</p>",
        [("Two similar shapes have matching sides 4 cm and 10 cm. Another side of the small shape is 6 cm. Find the matching side.", ["Scale factor = 10 ÷ 4 = 2.5.", "6 × 2.5 = 15."], "15 cm"),
         ("Are a 3 × 5 rectangle and a 6 × 9 rectangle similar?", ["6 ÷ 3 = 2 but 9 ÷ 5 = 1.8."], "No")],
        ["Adding the difference instead of multiplying: from 4 to 10 is × 2.5, not + 6.",
         "Using the scale factor the wrong way round when going from the large shape to the small one.",
         "Thinking three equal angles (AAA) prove congruence. They only prove similarity.",
         "Matching the wrong pair of sides. Match sides opposite equal angles."])


def main():
    cong = collect(one_congruence, 11, R)
    extra = [T("Which word means “exactly the same shape and size”?", "Congruent", ["Similar", "Symmetrical", "Equal"], "<b>Congruent</b> shapes are identical in shape and size."),
             T("Which word means “the same shape but possibly a different size”?", "Similar", ["Congruent", "Parallel", "Regular"], "<b>Similar</b> shapes have equal angles and proportional sides."),
             T("Two triangles have all three angles equal. They must be…", "similar", ["congruent", "right-angled", "isosceles"], "Equal angles prove they are <b>similar</b>."),
             T("Triangle ABC has AB = 5 cm, BC = 7 cm and angle B = 40°. Triangle PQR has PQ = 5 cm, QR = 7 cm and angle Q = 40°. Why are they congruent?", "SAS", ["SSS", "ASA", "RHS"], "Two sides and the included angle: <b>SAS</b>."),
             T("Two triangles each have angles 50° and 60° and the side between them is 8 cm. Why are they congruent?", "ASA", ["SAS", "SSS", "RHS"], "Two angles and the side between them: <b>ASA</b>."),
             T("Two triangles have sides 4, 5, 6 cm and 4, 5, 6 cm. Why are they congruent?", "SSS", ["SAS", "ASA", "RHS"], "Three sides equal: <b>SSS</b>."),
             T("What does RHS stand for?", "Right angle, Hypotenuse, Side", ["Right, Height, Side", "Radius, Height, Side", "Rotation, Height, Size"], "<b>Right angle, Hypotenuse, Side</b>."),
             T("A triangle is rotated 90°. Is the image congruent to the original?", "Yes", ["No", "Only if it is equilateral", "It is similar but not congruent"], "Rotations keep size and shape: <b>yes</b>."),
             T("A triangle is enlarged by scale factor 2. Is the image congruent to the original?", "No, it is similar", ["Yes", "Yes, by SSS", "No, it is a different shape"], "The sides are doubled, so it is <b>similar, not congruent</b>.")]
    sets = [S("Congruent triangles", cong + extra),
            S("Scale factors and missing sides", collect(one_sf, 20, R)),
            S("Similar triangles", collect(one_tri, 20, R)),
            S("Are the shapes similar?", collect(one_check, 20, R)),
            S("Problems", problems())]
    make(2, "congruence-and-similarity", 10, "G2",
         "Similarity and Congruence: Scale Factors and Congruent Triangles",
         "Secondary 2 Similarity and Congruence Worksheets: SSS, SAS, ASA, RHS, Scale Factors and Similar Triangles",
         "Similarity and congruence",
         "Use the standard conventions for labelling the sides and angles of triangle ABC, and know and use the criteria "
         "for congruence of triangles; identify and construct congruent triangles, and construct similar shapes by "
         "enlargement, with and without coordinate grids; apply the concepts of congruence and similarity, including "
         "the relationships between lengths in similar figures.",
         "Free Secondary 2 similarity and congruence worksheets: congruence conditions SSS, SAS, ASA and RHS, scale factors, "
         "missing sides in similar triangles and shapes, and shadow and model problems. 100 questions with answers.",
         "Similar shapes: equal angles, and every length × the same scale factor.",
         "Congruent triangles match by SSS, SAS, ASA or RHS. AAA only proves similarity.",
         body(),
         [("What is the difference between similar and congruent?", "Congruent shapes are identical in size and shape. Similar shapes are the same shape, but one can be an enlargement of the other."),
          ("What are the conditions for congruent triangles?", "SSS (three sides), SAS (two sides and the included angle), ASA (two angles and a side) and RHS (right angle, hypotenuse and a side)."),
          ("How do I find a missing side in similar shapes?", "Find the scale factor from a pair of matching sides, then multiply (or divide) the side you know."),
          ("Why does AAA not prove congruence?", "Triangles with the same angles can be different sizes, so they are similar but not always congruent.")],
         sets, R)


if __name__ == "__main__":
    main()
