# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Square Roots and Cube Roots (8.EE.A.2)
  python3 tools/gen_us_math_g8_square_and_cube_roots.py
Perfect squares and cubes, square roots and cube roots (also of fractions and negative numbers for
cube roots), solving x² = p and x³ = p, estimating roots between whole numbers, and area and volume
problems. Wrong answers come from real mistakes: dividing by 2 or 3 instead of taking the root,
forgetting the negative solution of x² = p, and squaring instead of taking a root.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fr, MINUS

R = random.Random(80801)
UPDATED = "2026-11-16"
SQ = "√"


def rt(n):
    return "√<span style='text-decoration:overline'>%s</span>" % n


def cr(n):
    return "<sup>3</sup>√<span style='text-decoration:overline'>%s</span>" % n


def v(x):
    x = F(x)
    if x.denominator == 1:
        return num(x)
    return (MINUS if x < 0 else "") + fr(abs(x.numerator), x.denominator)


# ============================================================ set 1: square roots
def set_sqrt():
    its = []
    for n in [4, 9, 25, 49, 64, 81, 100, 121, 144, 169, 196, 225, 36, 400, 256, 324, 625, 900]:
        r = int(n ** 0.5)
        q = "What is %s?" % B(rt(num(n)))
        e = "%d × %d = %s, so %s = <b>%d</b>." % (r, r, num(n), rt(num(n)), r)
        its.append(mcq(q, (num(r), F(r)), [(num(F(n, 2)), F(n, 2)), (num(n * n), F(n * n)), (num(r + 1), F(r + 1)), (num(r - 1), F(r - 1))], e))
    for a, b in [(1, 4), (9, 16)]:
        r = F(int(a ** 0.5), int(b ** 0.5))
        q = "What is %s?" % B(rt(fr(a, b)))
        e = "Take the root of the top and the bottom: %s ÷ %s = <b>%s</b>." % (rt(a), rt(b), v(r))
        its.append(mcq(q, (v(r), r), [(v(F(a, b) / 2), F(a, b) / 2), (v(F(a, b) ** 2), F(a, b) ** 2), (v(1 / r), 1 / r)], e))
    o = its
    order = [o[0], o[1], o[2], o[18], o[3], o[4], o[5], o[12], o[6], o[7], o[19], o[8], o[13], o[9], o[10], o[14], o[11],
             o[15], o[16], o[17]]
    return {"title": "Square roots", "items": order}


# ============================================================ set 2: cube roots
def set_cbrt():
    its = []
    for n in [8, 27, 64, 125, 1000, 216, 343, 512, 729, 1, -8, -27, -125, -1000]:
        r = round(abs(n) ** (1 / 3)) * (1 if n > 0 else -1)
        q = "What is %s?" % B(cr(num(n)))
        e = "%s × %s × %s = %s, so %s = <b>%s</b>." % (num(r), num(r), num(r), num(n), cr(num(n)), num(r))
        if n < 0:
            e += " A cube root of a negative number is negative."
        wr = [F(n, 3), -F(r), F(r) + 1, F(r) * F(r), F(r) - 1]
        its.append(mcq(q, (num(r), F(r)), [(v(w), w) for w in wr], e))
    for a, b in [(1, 8), (8, 27), (27, 64), (1, 125)]:
        r = F(round(a ** (1 / 3)), round(b ** (1 / 3)))
        q = "What is %s?" % B(cr(fr(a, b)))
        e = "Take the cube root of the top and the bottom: <b>%s</b>." % v(r)
        its.append(mcq(q, (v(r), r), [(v(F(a, b) / 3), F(a, b) / 3), (v(1 / r), 1 / r), (v(r * r), r * r), (v(-r), -r)], e))
    for q, ans, wr, e in [
        ("Which number is a perfect cube?", "64", ["36", "50", "100"], "4 × 4 × 4 = 64. The answer is <b>64</b>."),
        ("Which number is a perfect square?", "81", ["27", "50", "125"], "9 × 9 = 81. The answer is <b>81</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[18], o[2], o[9], o[3], o[14], o[10], o[4], o[19], o[5], o[11], o[15], o[6], o[12], o[16], o[7],
             o[13], o[17], o[8]]
    return {"title": "Cube roots", "items": order}


# ============================================================ set 3: solve
def set_solve():
    its = []
    for p in [49, 16, 100, 81, 144, 36, 1, 225, F(1, 9), F(25, 64)]:
        r = F(round(float(p) ** 0.5 * 1000)) / 1000
        r = F(int(p.numerator ** 0.5), int(p.denominator ** 0.5)) if isinstance(p, F) else F(int(p ** 0.5))
        q = "Solve %s." % B("<i>x</i><sup>2</sup> = %s" % v(p))
        ans = "<i>x</i> = %s or <i>x</i> = %s%s" % (v(r), MINUS, v(r))
        e = "Both %s and %s%s square to %s. So <b>%s</b>." % (v(r), MINUS, v(r), v(p), ans)
        wr = ["<i>x</i> = %s" % v(r), "<i>x</i> = %s" % v(F(p) / 2), "<i>x</i> = %s or <i>x</i> = %s%s" % (v(F(p) / 2), MINUS, v(F(p) / 2))]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for p in [27, 125, -64, 1000, 8, -1, 343, F(8, 27), -216, 512]:
        p = F(p)
        r = F(round(abs(p.numerator) ** (1 / 3)) * (1 if p > 0 else -1), round(p.denominator ** (1 / 3)))
        q = "Solve %s." % B("<i>x</i><sup>3</sup> = %s" % v(p))
        ans = "<i>x</i> = %s" % v(r)
        e = "%s × %s × %s = %s, and there is only one real cube root. So <b>%s</b>." % (v(r), v(r), v(r), v(p), ans)
        wr = ["<i>x</i> = %s or <i>x</i> = %s" % (v(r), v(-r)), "<i>x</i> = %s" % v(p / 3), "<i>x</i> = %s" % v(-r)]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    return {"title": "Solve x² = p and x³ = p", "items": order}


# ============================================================ set 4: estimate
def set_estimate():
    its = []
    for n in [20, 50, 10, 70, 30, 90, 45, 3, 110, 8, 60, 130, 150, 2, 85]:
        lo = int(n ** 0.5)
        hi = lo + 1
        q = "%s is between which two whole numbers?" % B(rt(n))
        ans = "%d and %d" % (lo, hi)
        e = "%d² = %d and %d² = %d. %d is between them, so %s is between <b>%d and %d</b>." % (lo, lo * lo, hi, hi * hi, n, rt(n), lo, hi)
        wr = ["%d and %d" % (n // 2 - 1, n // 2) if n // 2 > 2 else "%d and %d" % (n, n + 1), "%d and %d" % (hi, hi + 1),
              "%d and %d" % (lo - 1, lo), "%d and %d" % (hi + 1, hi + 2)]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for n, ans, wr, e in [
        (40, "6", ["7", "20", "5"], "6² = 36 and 7² = 49. 40 is closer to 36, so √40 ≈ <b>6</b>."),
        (80, "9", ["8", "40", "10"], "9² = 81 is very close to 80, so √80 ≈ <b>9</b>."),
        (26, "5", ["6", "13", "4"], "5² = 25 is closest to 26, so √26 ≈ <b>5</b>."),
        (60, "8", ["7", "30", "6"], "7² = 49 and 8² = 64. 60 is closer to 64, so √60 ≈ <b>8</b>."),
        (20, "3", ["2", "7", "4"], "2³ = 8 and 3³ = 27. 20 is closer to 27, so the cube root of 20 ≈ <b>3</b>."),
    ]:
        q = ("To the nearest whole number, what is %s?" % B(rt(n))) if "cube" not in e else ("To the nearest whole number, what is %s?" % B(cr(n)))
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[15], o[3], o[4], o[16], o[5], o[6], o[17], o[7], o[8], o[18], o[9], o[10], o[19], o[11],
             o[12], o[13], o[14]]
    return {"title": "Estimate roots", "items": order}


# ============================================================ set 5: area and volume
def set_words():
    its = []
    for q, ans, wr, e in [
        ("A square garden has an area of 64 m². How long is each side?", "8 m", ["16 m", "32 m", "4 m"], "Side = √64 = <b>8 m</b>."),
        ("A square tile has an area of 144 cm². How long is each side?", "12 cm", ["72 cm", "36 cm", "14 cm"], "Side = √144 = <b>12 cm</b>."),
        ("A cube has a volume of 125 cm³. How long is each edge?", "5 cm", ["25 cm", "41.7 cm", "11 cm"], "Edge = ∛125 = <b>5 cm</b>."),
        ("A cube-shaped box holds 1,000 in³. How long is each edge?", "10 in.", ["100 in.", "333 in.", "31.6 in."], "Edge = ∛1,000 = <b>10 in.</b>"),
        ("A square rug has an area of 49 ft². What is its perimeter?", "28 ft", ["7 ft", "24.5 ft", "196 ft"],
         "Side = √49 = 7 ft. Perimeter = 4 × 7 = <b>28 ft</b>."),
        ("A cube has a volume of 27 m³. What is the area of one face?", "9 m²", ["3 m²", "6 m²", "81 m²"],
         "Edge = ∛27 = 3 m. One face = 3 × 3 = <b>9 m²</b>."),
        ("A square park has an area of 10,000 m². How long is one side?", "100 m", ["1,000 m", "5,000 m", "2,500 m"],
         "Side = √10,000 = <b>100 m</b>."),
        ("A cube of ice has a volume of 8 cm³. How long is each edge?", "2 cm", ["4 cm", "2.67 cm", "64 cm"], "Edge = ∛8 = <b>2 cm</b>."),
        ("A square photo has an area of 50 in². About how long is each side?", "About 7 in.", ["About 25 in.", "About 12 in.", "About 5 in."],
         "√50 is between 7 and 8, close to 7 (7² = 49). <b>About 7 in.</b>"),
        ("A cube has a volume of 64 ft³. What is its total surface area?", "96 ft²", ["16 ft²", "64 ft²", "24 ft²"],
         "Edge = ∛64 = 4 ft. Each face is 16 ft², and a cube has 6 faces: 6 × 16 = <b>96 ft²</b>."),
        ("Which is true?", "√81 = 9 because 9² = 81", ["√81 = 40.5 because 81 ÷ 2 = 40.5", "√81 = 6,561 because 81² = 6,561", "√81 = 3 because 3⁴ = 81"],
         "Square root means the number that multiplies by itself: <b>√81 = 9 because 9² = 81</b>."),
        ("Which is true?", "∛64 = 4", ["∛64 = 8", "∛64 = 21.3", "∛64 = 32"], "4 × 4 × 4 = 64, so <b>∛64 = 4</b>. (8 is √64.)"),
        ("Which is greater: √50 or 7?", "√50", ["7", "They are equal", "We cannot tell"], "7 = √49, and 50 > 49, so <b>√50</b> is greater."),
        ("Which is greater: ∛30 or 3?", "∛30", ["3", "They are equal", "We cannot tell"], "3 = ∛27, and 30 > 27, so <b>∛30</b> is greater."),
        ("Which is less: √15 or 4?", "√15", ["4", "They are equal", "We cannot tell"], "4 = √16, and 15 < 16, so <b>√15</b> is less."),
        ("Why does x² = 36 have two solutions?", "Because 6² = 36 and (−6)² = 36", ["Because 36 is even", "Because 36 ÷ 2 = 18", "It has only one solution"],
         "A positive and a negative number both square to 36: <b>6 and −6</b>."),
        ("Why does x³ = −8 have a solution, but x² = −4 does not?", "(−2)³ = −8, but no real number squared is negative",
         ["Because −8 is bigger", "Because cubes are always positive", "Both have no solution"],
         "A negative times a negative times a negative is negative, but any square is 0 or more. <b>(−2)³ = −8, but no real number squared is negative</b>."),
        ("A square has a side of √20 cm. What is its area?", "20 cm²", ["√20 cm²", "400 cm²", "10 cm²"], "Area = (√20)² = <b>20 cm²</b>."),
        ("Ana says √36 = 18. What did she do?", "She divided by 2", ["She took the square root", "She squared 36", "She added 2"],
         "√36 = 6. Ana found 36 ÷ 2. <b>She divided by 2</b>."),
        ("Leo says ∛27 = 9. What is right?", "∛27 = 3", ["∛27 = 9", "∛27 = 81", "∛27 = 13.5"], "3 × 3 × 3 = 27, so <b>∛27 = 3</b>. 9 is 27 ÷ 3."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    return {"title": "Area, volume and reasoning", "items": its}


def body():
    return ("<h2>Square roots and cube roots</h2>"
            "<p>The <b>square root</b> of a number is the number that, multiplied by itself, gives it: √49 = 7 because 7 × 7 = 49. "
            "The <b>cube root</b> uses three equal factors: ∛64 = 4 because 4 × 4 × 4 = 64.</p>"
            + table(["n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], [
                ["n²", "1", "4", "9", "16", "25", "36", "49", "64", "81", "100"],
                ["n³", "1", "8", "27", "64", "125", "216", "343", "512", "729", "1,000"]])
            + "<h2>Solving x² = p and x³ = p</h2><p>x² = 49 has two solutions: x = 7 or x = −7. "
            "x³ = −8 has one solution: x = −2.</p>"
            + example("Between which two whole numbers is √50?", ["7² = 49 and 8² = 64.", "50 is between 49 and 64."], "7 and 8 (close to 7)")
            + "<h2>Common mistakes</h2><ul><li>Dividing by 2: √36 is 6, not 18.</li>"
            "<li>Dividing by 3: ∛27 is 3, not 9.</li>"
            "<li>Forgetting the negative answer of x² = p.</li>"
            "<li>Thinking a cube root of a negative number does not exist: ∛(−8) = −2.</li></ul>")


def main():
    sets = [set_sqrt(), set_cbrt(), set_solve(), set_estimate(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "square-and-cube-roots",
        "title": "Square Roots and Cube Roots",
        "seo_title": "Grade 8 Square Roots and Cube Roots Worksheets: Perfect Squares, x² = p, Estimating",
        "short_title": "Square and cube roots",
        "domain": "Expressions & Equations",
        "standard_code": "8.EE.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/EE/A/2/",
        "standard_text": "Use square root and cube root symbols to represent solutions to equations of the form x² = p and x³ = p, where p is a positive rational number. Evaluate square roots of small perfect squares and cube roots of small perfect cubes. Know that √2 is irrational.",
        "meta_desc": "Free Grade 8 square roots and cube roots worksheets: perfect squares and cubes, roots of fractions, solve x² = p and x³ = p, estimate roots between whole numbers, and area and volume problems. 100 questions with an answer key.",
        "key_big": "√49 = 7 because 7 × 7 = 49. ∛64 = 4 because 4 × 4 × 4 = 64.",
        "key_sub": "x² = 49 has two solutions (7 and −7). x³ = 64 has one (4).",
        "body_html": body(),
        "faq": [
            {"q": "What is the difference between a square root and a cube root?", "a": "A square root uses two equal factors (√25 = 5 because 5 × 5 = 25). A cube root uses three (∛125 = 5 because 5 × 5 × 5 = 125)."},
            {"q": "Why does x² = 25 have two answers?", "a": "Both 5 and −5 square to 25, so x = 5 or x = −5."},
            {"q": "Can you take the cube root of a negative number?", "a": "Yes. ∛(−27) = −3 because (−3) × (−3) × (−3) = −27."},
            {"q": "How do you estimate a square root?", "a": "Find the two perfect squares around the number. √50 is between √49 = 7 and √64 = 8, close to 7."}],
        "sets": sets, "pdf_url": "", "sort": 8, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
