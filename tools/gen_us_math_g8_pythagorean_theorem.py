# -*- coding: utf-8 -*-
"""
US Grade 8 Math: The Pythagorean Theorem (8.G.B.6, 8.G.B.7)
  python3 tools/gen_us_math_g8_pythagorean_theorem.py
Find the hypotenuse, find a missing leg, decide if a triangle is a right triangle (the converse),
and solve real-world problems in 2D and 3D. Wrong answers come from real mistakes: adding the sides
without squaring, forgetting the square root, adding when finding a leg, and using a leg as the hypotenuse.
"""
import math, random
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, svg_wrap, text, line, INK, RED, GREEN, FILL

R = random.Random(81001)
UPDATED = "2026-11-16"


def rt(n):
    return "√<span style='text-decoration:overline'>%s</span>" % num(n)


def tri_svg(a, b, c, unit="", flip=False):
    """Right triangle with legs a (bottom) and b (side). Labels are strings ('?' in red)."""
    W, H = 260, 190
    x0, y0 = 40, 160
    x1, y1 = 220, 160
    x2, y2 = (40, 30) if not flip else (220, 30)
    if flip:
        x0, x1 = 220, 40
    s = ["<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y0, x1, y1, x2, y2, FILL, GREEN)]
    d = 14 if not flip else -14
    s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='1.6'/>" % (x0 + d, y0, x0 + d, y0 - 14, x0, y0 - 14, INK))
    lab = lambda t: (t + (" " + unit if unit and t != "?" else ""))
    s.append(text((x0 + x1) / 2, y0 + 22, lab(a), 16, col=RED if a == "?" else INK))
    s.append(text(x0 - (26 if not flip else -30), (y0 + y2) / 2 + 5, lab(b), 16, col=RED if b == "?" else INK))
    s.append(text((x1 + x2) / 2 + (18 if not flip else -18), (y1 + y2) / 2 - 6, lab(c), 16, col=RED if c == "?" else INK))
    return svg_wrap(W, H, "".join(s), "right triangle")


def eq_root(v):
    """'√25 = 5' or '√2 ≈ 1.4' (for explanations)."""
    r = math.isqrt(v)
    return "%s = <b>%d</b>" % (rt(v), r) if r * r == v else "<b>%s ≈ %.1f</b>" % (rt(v), math.sqrt(v))


def fmt(v):
    """Whole number, or exact root and decimal."""
    r = math.isqrt(v)
    if r * r == v:
        return num(r), r
    return "%s ≈ %.1f" % (rt(v), math.sqrt(v)), round(math.sqrt(v), 1)


# ============================================================ set 1: hypotenuse
def set_hyp():
    its = []
    for a, b in [(3, 4), (6, 8), (5, 12), (8, 15), (9, 12), (7, 24), (12, 16), (20, 21), (10, 24), (15, 20),
                 (1, 1), (2, 3), (4, 5), (1, 2), (6, 7), (3, 5), (5, 5), (2, 6), (9, 40), (12, 35)]:
        c2 = a * a + b * b
        ans, key = fmt(c2)
        q = fig(tri_svg(num(a), num(b), "?", flip=bool(len(its) % 2))) + "Find the length of the hypotenuse."
        e = "c² = %d² + %d² = %d + %d = %d. c = %s." % (a, b, a * a, b * b, c2, eq_root(c2))
        wr = [num(a + b), num(c2), fmt(abs(b * b - a * a))[0] if b != a else num(2 * a), num(max(a, b) + 1),
              fmt(c2 + 1)[0], fmt(c2 + 3)[0], fmt(c2 + 5)[0]]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[10], o[3], o[11], o[4], o[12], o[5], o[13], o[6], o[14], o[7], o[15], o[8], o[16], o[9],
             o[17], o[18], o[19]]
    return {"title": "Find the hypotenuse", "items": order}


# ============================================================ set 2: missing leg
def set_leg():
    its = []
    for a, c in [(3, 5), (5, 13), (8, 17), (6, 10), (9, 15), (12, 13), (7, 25), (20, 29), (16, 20), (24, 26),
                 (1, 2), (2, 4), (3, 6), (4, 7), (5, 8), (6, 9), (10, 12), (1, 3), (12, 37), (11, 61)]:
        b2 = c * c - a * a
        ans, key = fmt(b2)
        q = fig(tri_svg(num(a), "?", num(c), flip=bool(len(its) % 2))) + "Find the missing leg."
        e = "a² + b² = c², so b² = %d² − %d² = %d − %d = %d. b = %s." % (c, a, c * c, a * a, b2, eq_root(b2))
        wr = [fmt(c * c + a * a)[0], num(c - a), num(b2), num(c + a)]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[10], o[2], o[3], o[11], o[4], o[12], o[5], o[13], o[6], o[14], o[7], o[15], o[8], o[16], o[9],
             o[17], o[18], o[19]]
    return {"title": "Find a missing leg", "items": order}


# ============================================================ set 3: converse
def set_converse():
    its = []
    YES, NO = "Yes, it is a right triangle", "No, it is not a right triangle"
    for a, b, c in [(3, 4, 5), (5, 12, 13), (4, 5, 6), (6, 8, 10), (7, 8, 11), (8, 15, 17), (2, 3, 4), (9, 12, 15), (5, 6, 8),
                    (20, 21, 29), (10, 10, 14), (7, 24, 25), (6, 7, 9), (12, 35, 37), (11, 60, 61), (4, 7, 8)]:
        ok = a * a + b * b == c * c
        ans = YES if ok else NO
        q = "Can a triangle with sides %s be a right triangle?" % B("%d, %d and %d" % (a, b, c))
        e = "Check a² + b² = c² with the longest side as c: %d + %d = %d, and %d² = %d. " % (a * a, b * b, a * a + b * b, c, c * c)
        e += ("They are equal: <b>yes</b>." if ok else "They are not equal: <b>no</b>.")
        its.append(mcq(q, (ans, ans), [(c_, c_) for c_ in [YES, NO, "Only if the sides are whole numbers", "We cannot tell without a drawing"]
                                       if c_ != ans], e))
    for q, ans, wr, e in [
        ("In a right triangle, which side is the hypotenuse?", "The longest side, across from the right angle",
         ["The shortest side", "The side at the bottom", "Either leg"], "The hypotenuse is <b>the longest side, across from the right angle</b>."),
        ("Which set of sides makes a right triangle?", "9, 40, 41", ["9, 40, 45", "5, 10, 12", "6, 9, 12"],
         "81 + 1,600 = 1,681 = 41². The answer is <b>9, 40, 41</b>."),
        ("A triangle has sides 5, 13 and 12. Which is the hypotenuse?", "13", ["5", "12", "Any side"], "The longest side is the hypotenuse: <b>13</b>."),
        ("Lee checks 13, 12, 5 with 13² + 12² = 5². What went wrong?", "He used a leg as c", ["Nothing, it is right", "He forgot to add",
         "He should multiply the sides"], "c must be the longest side: 5² + 12² = 13². <b>He used a leg as c</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[16], o[0], o[1], o[2], o[18], o[3], o[4], o[5], o[17], o[6], o[7], o[8], o[19], o[9], o[10], o[11], o[12],
             o[13], o[14], o[15]]
    return {"title": "Is it a right triangle?", "items": order}


# ============================================================ set 4: real world 2D
def set_world():
    its = []
    for q, ans, wr, e in [
        ("A 10-foot ladder leans on a wall. Its foot is 6 feet from the wall. How high up the wall does it reach?", "8 ft",
         ["16 ft", "4 ft", "11.7 ft"], "6² + h² = 10², so h² = 100 − 36 = 64 and h = <b>8 ft</b>."),
        ("A TV screen is 32 in. wide and 24 in. tall. How long is the diagonal?", "40 in.", ["56 in.", "28 in.", "21.2 in."],
         "d² = 32² + 24² = 1,024 + 576 = 1,600, so d = <b>40 in.</b>"),
        ("A rectangular park is 60 m by 80 m. How long is the path from one corner to the opposite corner?", "100 m", ["140 m", "70 m", "52.9 m"],
         "d² = 60² + 80² = 3,600 + 6,400 = 10,000, so d = <b>100 m</b>."),
        ("A boat sails 9 km east and then 12 km north. How far is it from where it started?", "15 km", ["21 km", "3 km", "7.9 km"],
         "d² = 9² + 12² = 81 + 144 = 225, so d = <b>15 km</b>."),
        ("A kite string is 50 m long. The kite is right above a point 30 m away. How high is the kite?", "40 m", ["80 m", "20 m", "58.3 m"],
         "h² = 50² − 30² = 2,500 − 900 = 1,600, so h = <b>40 m</b>."),
        ("A ramp rises 3 ft over a run of 4 ft. How long is the ramp?", "5 ft", ["7 ft", "1 ft", "2.6 ft"],
         "ℓ² = 3² + 4² = 25, so ℓ = <b>5 ft</b>."),
        ("A square has sides of 5 cm. How long is its diagonal, to the nearest tenth?", "7.1 cm", ["10 cm", "5 cm", "25 cm"],
         "d² = 5² + 5² = 50, so d = √50 ≈ <b>7.1 cm</b>."),
        ("A soccer field is 100 yd by 60 yd. About how long is the diagonal, to the nearest yard?", "117 yd", ["160 yd", "80 yd", "40 yd"],
         "d² = 100² + 60² = 13,600, so d = √13,600 ≈ <b>117 yd</b>."),
        ("A 13-ft ladder reaches 12 ft up a wall. How far is its foot from the wall?", "5 ft", ["1 ft", "25 ft", "17.7 ft"],
         "x² = 13² − 12² = 169 − 144 = 25, so x = <b>5 ft</b>."),
        ("Sam walks 5 blocks north and 12 blocks east. How many blocks shorter is the straight path?", "4 blocks", ["13 blocks", "17 blocks", "7 blocks"],
         "Straight path: √(25 + 144) = 13. Walked: 5 + 12 = 17. 17 − 13 = <b>4 blocks</b> shorter."),
        ("A phone is 6 in. tall and 3 in. wide. About how long is the diagonal, to the nearest tenth?", "6.7 in.", ["9 in.", "5.2 in.", "45 in."],
         "d² = 36 + 9 = 45, so d = √45 ≈ <b>6.7 in.</b>"),
        ("A wire runs from the top of a 15-m pole to a stake 8 m from its base. How long is the wire?", "17 m", ["23 m", "7 m", "12.7 m"],
         "w² = 15² + 8² = 225 + 64 = 289, so w = <b>17 m</b>."),
        ("A right triangle has legs 1 and 1. What is the exact length of the hypotenuse?", "√2", ["2", "1", "1.5"],
         "c² = 1 + 1 = 2, so c = <b>√2</b>."),
        ("A gate is 4 ft wide and 3 ft tall. A brace goes corner to corner. How long is the brace?", "5 ft", ["7 ft", "12 ft", "1 ft"],
         "b² = 4² + 3² = 25, so b = <b>5 ft</b>."),
        ("A plane flies 120 miles north and 50 miles west. How far is it from the start?", "130 miles", ["170 miles", "70 miles", "109 miles"],
         "d² = 120² + 50² = 14,400 + 2,500 = 16,900, so d = <b>130 miles</b>."),
        ("A slide is 10 ft long and its top is 6 ft high. How far along the ground does it reach?", "8 ft", ["4 ft", "16 ft", "11.7 ft"],
         "g² = 10² − 6² = 64, so g = <b>8 ft</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for a, b in [(5, 12), (8, 6), (7, 24), (9, 40)]:
        c = int(math.sqrt(a * a + b * b))
        q = fig(tri_svg("%d m" % a, "%d m" % b, "?")) + "A path cuts across a field. How long is the path (the hypotenuse)?"
        e = "c² = %d + %d = %d, so c = <b>%d m</b>." % (a * a, b * b, c * c, c)
        its.append(mcq(q, ("%d m" % c, c), [("%d m" % (a + b), a + b), ("%d m" % (c * c), c * c), ("%d m" % (b - a if b > a else a - b), "d")], e))
    o = its
    order = [o[0], o[16], o[1], o[2], o[17], o[3], o[4], o[18], o[5], o[6], o[19], o[7], o[8], o[9], o[10], o[11], o[12],
             o[13], o[14], o[15]]
    return {"title": "Real-world problems", "items": order}


# ============================================================ set 5: 3D and reasoning
def set_3d():
    its = []
    for l, w, h in [(3, 4, 12), (2, 3, 6), (4, 4, 7), (6, 8, 24), (1, 2, 2), (2, 6, 9), (12, 16, 21), (8, 9, 12)]:
        d2 = l * l + w * w + h * h
        ans, key = fmt(d2)
        q = "A box is %d × %d × %d units. How long is the longest diagonal from a bottom corner to the opposite top corner?" % (l, w, h)
        e = ("First the floor diagonal: %d² + %d² = %d. Then with the height: %d + %d² = %d. d = %s."
             % (l, w, l * l + w * w, l * l + w * w, h, d2, eq_root(d2)))
        wr = [num(l + w + h), fmt(l * l + w * w)[0], num(d2), num(h + 1)]
        its.append(mcq(q, (ans, ans), [(x, x) for x in wr], e))
    for q, ans, wr, e in [
        ("Which equation is the Pythagorean theorem for legs a and b and hypotenuse c?", "a² + b² = c²", ["a + b = c", "a² + c² = b²", "2a + 2b = c"],
         "The squares of the legs add up to the square of the hypotenuse: <b>a² + b² = c²</b>."),
        ("Does the Pythagorean theorem work for every triangle?", "No, only right triangles", ["Yes, every triangle", "Only for triangles with equal sides", "Only for small triangles"],
         "It only works when one angle is 90°: <b>no, only right triangles</b>."),
        ("A right triangle has legs 6 and 8. Ana says the hypotenuse is 14. What did she do?", "She added the legs", ["She squared the legs", "She found the area", "Nothing, she is right"],
         "6 + 8 = 14, but c = √(36 + 64) = 10. <b>She added the legs</b>."),
        ("A right triangle has legs 6 and 8. Ben says the hypotenuse is 100. What did he forget?", "To take the square root", ["To add", "To square", "To divide by 2"],
         "c² = 100, so c = 10. <b>He forgot to take the square root</b>."),
        ("The hypotenuse is 10 and one leg is 6. Kim does 10² + 6². What should she do?", "Subtract: 10² − 6²", ["Add: 10 + 6", "Multiply: 10 × 6", "Nothing, she is right"],
         "To find a leg, subtract: b² = 10² − 6² = 64, so b = 8. <b>Subtract: 10² − 6²</b>."),
        ("In a right triangle, can a leg be longer than the hypotenuse?", "No, the hypotenuse is always the longest", ["Yes, sometimes", "Only if the legs are equal", "Yes, always"],
         "c² = a² + b² is bigger than a² or b². <b>No, the hypotenuse is always the longest</b>."),
        ("A cube has edges of 1 m. How long is a diagonal of one face, exactly?", "√2 m", ["2 m", "1 m", "√3 m"],
         "1² + 1² = 2, so the face diagonal is <b>√2 m</b>."),
        ("A cube has edges of 1 m. How long is the diagonal through the cube, exactly?", "√3 m", ["√2 m", "3 m", "2 m"],
         "1² + 1² + 1² = 3, so the space diagonal is <b>√3 m</b>."),
        ("Will a 30-in. stick fit flat in a box that is 24 in. by 18 in.?", "Yes, the diagonal is 30 in.", ["No, it is too long", "Only if the box is deep", "We cannot tell"],
         "√(24² + 18²) = √900 = 30. <b>Yes, the diagonal is 30 in.</b>"),
        ("A right triangle has legs 9 and 12. What is its perimeter?", "36", ["21", "15", "54"],
         "c = √(81 + 144) = 15. Perimeter = 9 + 12 + 15 = <b>36</b>."),
        ("An isosceles right triangle has a hypotenuse of √50. How long is each leg?", "5", ["25", "√25 ≈ 2.5", "10"],
         "a² + a² = 50, so a² = 25 and a = <b>5</b>."),
        ("A rectangle’s diagonal is 26 cm and one side is 10 cm. What is its area?", "240 cm²", ["260 cm²", "24 cm²", "360 cm²"],
         "Other side: √(26² − 10²) = √576 = 24. Area = 10 × 24 = <b>240 cm²</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[8], o[9], o[10], o[11], o[12], o[13], o[0], o[14], o[1], o[15], o[2], o[16], o[3], o[17], o[4], o[18], o[5],
             o[19], o[6], o[7]]
    return {"title": "3D and reasoning", "items": order}


def body():
    return ("<h2>The Pythagorean theorem</h2>"
            "<p>In a <b>right triangle</b>, the two shorter sides are the <b>legs</b> (a and b). "
            "The longest side, across from the right angle, is the <b>hypotenuse</b> (c).</p>"
            "<p style='font-size:1.2em'><b>a² + b² = c²</b></p>"
            "<figure class='sn-fig'>" + tri_svg("3", "4", "5") + "<figcaption>3² + 4² = 9 + 16 = 25 = 5².</figcaption></figure>"
            + example("Find the hypotenuse when the legs are 6 and 8.", ["c² = 6² + 8² = 36 + 64 = 100.", "c = √100 = 10."], "10")
            + example("Find the missing leg when a = 5 and c = 13.", ["b² = 13² − 5² = 169 − 25 = 144.", "b = √144 = 12."], "12")
            + "<h2>Is it a right triangle?</h2><p>If a² + b² = c² (with c the longest side), the triangle is a right triangle. If not, it is not.</p>"
            + table(["Common right triangles"], [["3, 4, 5"], ["5, 12, 13"], ["8, 15, 17"], ["7, 24, 25"]])
            + "<h2>Common mistakes</h2><ul><li>Adding the sides: 6 + 8 is not the hypotenuse. Square first.</li>"
            "<li>Forgetting the square root at the end: c² = 100 means c = 10.</li>"
            "<li>Adding when finding a leg. Subtract: b² = c² − a².</li>"
            "<li>Using a leg as c. c is always the longest side.</li></ul>")


def main():
    sets = [set_hyp(), set_leg(), set_converse(), set_world(), set_3d()]
    balance(sets, R)
    unit = {
        "slug": "pythagorean-theorem",
        "title": "The Pythagorean Theorem",
        "seo_title": "Grade 8 Pythagorean Theorem Worksheets: Hypotenuse, Missing Leg, Converse and Word Problems",
        "short_title": "Pythagorean theorem",
        "domain": "Geometry",
        "standard_code": "8.G.B.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/G/B/7/",
        "standard_text": "Apply the Pythagorean Theorem to determine unknown side lengths in right triangles in real-world and mathematical problems in two and three dimensions.",
        "meta_desc": "Free Grade 8 Pythagorean theorem worksheets: find the hypotenuse and missing legs, decide if a triangle is a right triangle, and solve ladder, diagonal and 3D box problems. 100 questions with an answer key.",
        "key_big": "In a right triangle, a² + b² = c², where c is the hypotenuse (the longest side).",
        "key_sub": "To find c: add the squares, then take the square root. To find a leg: subtract.",
        "body_html": body(),
        "faq": [
            {"q": "What is the Pythagorean theorem?", "a": "In a right triangle with legs a and b and hypotenuse c, a² + b² = c². For legs 3 and 4, c² = 9 + 16 = 25, so c = 5."},
            {"q": "How do you find a missing leg?", "a": "Subtract: b² = c² − a². Then take the square root. For c = 13 and a = 5, b² = 169 − 25 = 144, so b = 12."},
            {"q": "How do you know if a triangle is a right triangle?", "a": "Use the converse: if the squares of the two shorter sides add up to the square of the longest side, it is a right triangle."},
            {"q": "Does the Pythagorean theorem work in 3D?", "a": "Yes. The diagonal of a box is √(l² + w² + h²), found by using the theorem twice."}],
        "sets": sets, "pdf_url": "", "sort": 10, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
