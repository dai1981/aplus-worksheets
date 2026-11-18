# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Volume of Prisms and Pyramids (TEKS 7.8A, 7.8B, 7.9A)
  python3 tools/gen_ustx_math_g7_volume.py
Volume of rectangular prisms (US Grade 7 maker), triangular prisms, rectangular and triangular pyramids, the
prism–pyramid relationship, and word problems (own makers).
Wrong answers come from real mistakes: forgetting the 1/3 for a pyramid, forgetting the 1/2 for a triangular base,
and using a slant height.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_area_surface_area_volume as asv
adopt(asv)
asv.R = random.Random(670140)
tx_common.GRADE = "grade-7"

INK = "#1f2937"
FILL = "#dbeafe"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return comma(int(a)) + "." + b
    return comma(int(s))


def txt(x, y, t, anchor="middle", col=INK):
    return "<text x='%.1f' y='%.1f' font-size='13' text-anchor='%s' fill='%s'>%s</text>" % (x, y, anchor, col, t)


def one_triprism(r):
    b, h, L = r.randint(3, 12), r.randint(2, 10), r.randint(4, 20)
    B = b * h / 2.0
    V = B * L
    return mcq("A triangular prism has a triangle base with base %d cm and height %d cm. The prism is %d cm long. What is its volume?" % (b, h, L), "%s cm³" % g(V), ["%s cm³" % g(b * h * L), "%s cm³" % g(V / 3), "%s cm³" % g(B + L)],
               "B = ½ × %d × %d = %s cm². V = B × h = %s × %d = <b>%s cm³</b>." % (b, h, g(B), g(B), L, g(V)))


def one_pyr(r):
    kind = r.choice(["rect", "rect", "tri"])
    h = r.choice([3, 6, 9, 12, 15])
    if kind == "rect":
        l, w = r.randint(2, 12), r.randint(2, 12)
        B = l * w
        V = B * h / 3.0
        return mcq("A rectangular pyramid has a %d in. by %d in. base and a height of %d in. What is its volume?" % (l, w, h), "%s in³" % g(V), ["%s in³" % g(B * h), "%s in³" % g(B * h / 2.0), "%s in³" % g(B + h)],
                   "V = ⅓ × B × h = ⅓ × %d × %d = <b>%s in³</b>." % (B, h, g(V)))
    b, t = r.randint(2, 12), r.randint(2, 12)
    B = b * t / 2.0
    V = B * h / 3.0
    return mcq("A triangular pyramid has a base triangle with base %d m and height %d m. The pyramid is %d m tall. What is its volume?" % (b, t, h), "%s m³" % g(V), ["%s m³" % g(B * h), "%s m³" % g(b * t * h / 3.0), "%s m³" % g(b * t * h)],
               "B = ½ × %d × %d = %s. V = ⅓ × %s × %d = <b>%s m³</b>." % (b, t, g(B), g(B), h, g(V)))


def one_rel(r):
    kind = r.choice(["fill", "prism", "pyr", "same"])
    V = r.choice([30, 45, 60, 72, 90, 120, 150])
    if kind == "fill":
        return mcq("A pyramid and a prism have the same base and the same height. How many pyramids full of sand fill the prism?", "3", ["2", "4", "1"],
                   "The volume of a pyramid is ⅓ of the prism with the same base and height, so <b>3</b> pyramids fill it.")
    if kind == "prism":
        return mcq("A pyramid has a volume of %d cm³. A prism has the same base and height. What is the volume of the prism?" % V, "%d cm³" % (V * 3), ["%d cm³" % (V // 3) if V % 3 == 0 else "%d cm³" % (V * 2), "%d cm³" % (V * 2), "%d cm³" % V],
                   "A prism holds 3 times as much: 3 × %d = <b>%d cm³</b>." % (V, V * 3))
    if kind == "pyr":
        return mcq("A triangular prism has a volume of %d ft³. A triangular pyramid has the same base and height. What is the volume of the pyramid?" % V, "%d ft³" % (V // 3), ["%d ft³" % (V * 3), "%d ft³" % (V // 2), "%d ft³" % V],
                   "A pyramid is ⅓ of the prism: %d ÷ 3 = <b>%d ft³</b>." % (V, V // 3))
    return mcq("Which formula gives the volume of a pyramid with base area B and height h?", "V = ⅓Bh", ["V = Bh", "V = ½Bh", "V = 3Bh"], "A pyramid is one third of a prism with the same base and height: <b>V = ⅓Bh</b>.")


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["tent", "sand", "box", "candle", "trough"])
    if kind == "tent":
        b, h, L = r.choice([6, 8, 10]), r.choice([4, 5, 6]), r.choice([7, 8, 9, 12])
        V = b * h * L / 2
        return mcq("A camping tent at Big Bend is a triangular prism. The front triangle has base %d ft and height %d ft. The tent is %d ft long. How much space is inside?" % (b, h, L), "%s ft³" % comma(V), ["%s ft³" % comma(b * h * L), "%s ft³" % comma(V // 3), "%s ft³" % comma(b + h + L)],
                   "B = ½ × %d × %d = %d. V = %d × %d = <b>%s ft³</b>." % (b, h, b * h // 2, b * h // 2, L, comma(V)))
    if kind == "sand":
        s, h = r.choice([3, 6, 9]), r.choice([4, 5, 6, 8])
        V = s * s * h / 3.0
        return mcq("A sand sculpture is a square pyramid with base edges of %d ft and a height of %d ft. How much sand is in it?" % (s, h), "%s ft³" % g(V), ["%s ft³" % g(s * s * h), "%s ft³" % g(s * s * h / 2.0), "%s ft³" % g(s * h)],
                   "V = ⅓ × %d × %d × %d = <b>%s ft³</b>." % (s, s, h, g(V)))
    if kind == "box":
        l, w, h = r.randint(10, 24), r.randint(6, 15), r.randint(4, 12)
        c = r.choice([2, 3, 4])
        return mcq("%s fills a %d in. by %d in. by %d in. box with %d in. cubes of foam. How many cubes fit if they fill it exactly?" % (k["n"], l * c, w * c, h * c, c), "%s" % comma(l * w * h), ["%s" % comma(l * w * h * c * c * c), "%s" % comma(l * w * h * c), "%s" % comma(l + w + h)],
                   "%d ÷ %d = %d, %d ÷ %d = %d, %d ÷ %d = %d. %d × %d × %d = <b>%s</b>." % (l * c, c, l, w * c, c, w, h * c, c, h, l, w, h, comma(l * w * h)))
    if kind == "candle":
        s, h = r.choice([2, 3, 4, 6]), r.choice([6, 9, 12])
        V = s * s * h / 3.0
        return mcq("A candle is a square pyramid %d cm on each base edge and %d cm tall. How much wax does it use?" % (s, h), "%s cm³" % g(V), ["%s cm³" % g(s * s * h), "%s cm³" % g(V * 2), "%s cm³" % g(s * s + h)],
                   "V = ⅓ × %d × %d = <b>%s cm³</b>." % (s * s, h, g(V)))
    b, h, L = r.choice([2, 3, 4]), r.choice([2, 3]), r.choice([8, 10, 12])
    V = b * h * L / 2.0
    return mcq("A water trough is a triangular prism. Its triangle end has base %d ft and height %d ft, and it is %d ft long. How many cubic feet of water does it hold?" % (b, h, L), "%s ft³" % g(V), ["%s ft³" % g(b * h * L), "%s ft³" % g(V / 3), "%s ft³" % g(b * L)],
               "B = ½ × %d × %d = %s. V = %s × %d = <b>%s ft³</b>." % (b, h, g(b * h / 2.0), g(b * h / 2.0), L, g(V)))


def build():
    sets, R = build_sets([
        ("Volume of rectangular prisms", [("run", asv.set_volume, (), 20)]),
        ("Volume of triangular prisms", [("collect", one_triprism, 20)]),
        ("Volume of pyramids", [("collect", one_pyr, 20)]),
        ("Prisms and pyramids with the same base and height", [("collect", one_rel, 6), ("collect", one_pyr, 14)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 67014)
    finish(sets, R)
    body = lesson('<ul><li>Volume of any <b>prism</b>: V = Bh, where B is the area of the base and h is the height.</li><li>For a triangular prism, B = ½ × base × height of the triangle.</li><li>Volume of a <b>pyramid</b>: V = ⅓Bh. It is one third of the prism with the same base and height.</li><li>Volume is in cubic units, such as cm³ or ft³.</li></ul>',
        [example("Rectangular pyramid: base 6 in. by 4 in., height 9 in.", ["B = 24", "⅓ × 24 × 9"], "72 in³"), example("Triangular prism: base 5, height 4, length 10", ["B = ½ × 5 × 4 = 10", "10 × 10"], "100 cubic units")],
        [['Forgetting the ⅓ for a pyramid', 'A pyramid holds one third of the prism.'], ['Forgetting the ½ for a triangle base', 'B = ½ × b × h for a triangle.'], ['Using a slant height', 'Use the height that is perpendicular to the base.']])
    faq = [('What does TEKS 7.8A ask?', 'Model the relationship between the volume of a rectangular prism and a rectangular pyramid having both congruent bases and heights and connect that relationship to the formulas.'), ('What does TEKS 7.8B ask?', 'Explain verbally and symbolically the relationship between the volume of a triangular prism and a triangular pyramid having both congruent bases and heights and connect that relationship to the formulas.'), ('What does TEKS 7.9A ask?', 'Solve problems involving the volume of rectangular prisms, triangular prisms, rectangular pyramids and triangular pyramids.'), ('Why is a pyramid one third?', 'It takes three pyramids of sand to fill a prism with the same base and height.')]
    make('volume-of-prisms-and-pyramids', 14, 'Expressions, Equations and Relationships', '7.8A, 7.8B, 7.9A',
         '7.8A model the relationship between the volume of a rectangular prism and a rectangular pyramid having both congruent bases and heights and connect that relationship to the formulas; 7.8B explain verbally and symbolically the relationship between the volume of a triangular prism and a triangular pyramid having both congruent bases and heights and connect that relationship to the formulas; 7.9A solve problems involving the volume of rectangular prisms, triangular prisms, rectangular pyramids, and triangular pyramids',
         'Volume of Prisms and Pyramids', 'Volume of Prisms and Pyramids',
         'Free Grade 7 volume worksheets for Texas TEKS 7.8A, 7.8B and 7.9A: rectangular and triangular prisms, rectangular and triangular pyramids, V = Bh and V = ⅓Bh, and word problems. 100 questions with answers.',
         'Prism: V = Bh. Pyramid: V = ⅓Bh.', 'Three pyramids fill a prism with the same base and height.',
         body, faq, sets, seo_title='Grade 7 Volume of Prisms and Pyramids Worksheets (TEKS 7.9A, STAAR)')


if __name__ == "__main__":
    build()
