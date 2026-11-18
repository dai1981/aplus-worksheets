# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Area of Triangles, Parallelograms and Trapezoids (TEKS 6.8B, 6.8C, 6.8D)
  python3 tools/gen_ustx_math_g6_area.py
Area of right triangles and any triangle, parallelograms and trapezoids, composite figures, and word problems (the
US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: forgetting to halve for a triangle, using a slanted side as the height, and
adding only one base of a trapezoid.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_area_polygons as ap
adopt(ap)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Area of right triangles", [("run", ap.set_right, ("rnd", "seen"), 20)]),
        ("Area of any triangle", [("run", ap.set_any, ("rnd", "seen"), 20)]),
        ("Parallelograms and trapezoids", [("run", ap.set_quads, ("rnd", "seen"), 20)]),
        ("Composite figures", [("run", ap.set_composite, ("rnd",), 20)]),
        ("Area word problems", [("run", ap.set_story, ("rnd", ap.People), 20)]),
    ], 66017)
    finish(sets, R)
    body = lesson("<ul><li>Parallelogram: A = b × h. Cut a triangle from one end and move it to make a rectangle.</li><li>Triangle: A = <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> × b × h. Two copies make a parallelogram.</li><li>Trapezoid: A = <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> × (b<sub>1</sub> + b<sub>2</sub>) × h.</li><li>The <b>height</b> is always perpendicular to the base, not a slanted side.</li></ul>",
        [example("Triangle: b = 10 cm, h = 7 cm", ["1/2 × 10 × 7"], "35 cm²"), example("Trapezoid: bases 6 m and 10 m, h = 4 m", ["1/2 × (6 + 10) × 4"], "32 m²")],
        [['Forgetting the 1/2 for a triangle', 'A triangle is half of a parallelogram.'], ['Using a slanted side as the height', 'The height meets the base at a right angle.'], ['Using only one base of a trapezoid', 'Add both bases, then multiply by h and 1/2.']])
    faq = [('What does TEKS 6.8B ask?', 'Model area formulas for parallelograms, trapezoids and triangles by decomposing and rearranging parts of these shapes.'), ('What does TEKS 6.8D ask?', 'Determine solutions for problems involving the area of rectangles, parallelograms, trapezoids and triangles and volume of right rectangular prisms where dimensions are positive rational numbers.'), ('Why is a triangle half of b × h?', 'Two copies of the same triangle make a parallelogram with area b × h.'), ('What units does area use?', 'Square units, such as cm² or ft².')]
    make('area-of-triangles-parallelograms-and-trapezoids', 17, 'Geometry and Measurement', '6.8B, 6.8C, 6.8D',
         '6.8B model area formulas for parallelograms, trapezoids, and triangles by decomposing and rearranging parts of these shapes; 6.8C write equations that represent problems related to the area of rectangles, parallelograms, trapezoids, and triangles and volume of right rectangular prisms where dimensions are positive rational numbers; 6.8D determine solutions for problems involving the area of rectangles, parallelograms, trapezoids, and triangles and volume of right rectangular prisms where dimensions are positive rational numbers',
         'Area of Triangles, Parallelograms and Trapezoids', 'Area of Triangles, Parallelograms and Trapezoids',
         'Free Grade 6 area worksheets for Texas TEKS 6.8B, 6.8C and 6.8D: area of triangles, parallelograms and trapezoids, composite figures and word problems. 100 questions with answers.',
         'Parallelogram b × h, triangle ½ × b × h, trapezoid ½ × (b₁ + b₂) × h.', 'The height is perpendicular to the base.',
         body, faq, sets, seo_title='Grade 6 Area of Triangles, Parallelograms and Trapezoids Worksheets (TEKS 6.8, STAAR)')


if __name__ == "__main__":
    build()
