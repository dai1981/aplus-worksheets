# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Area: Covering with Square Units (TEKS 2.9F)
  python3 tools/gen_ustx_math_g2_area.py
Counting square units, covering with no gaps or overlaps, comparing areas by covering (Ontario makers with Texas
names), rows of squares in a rectangle, and area stories (own makers).
Wrong answers come from real mistakes: counting the edges instead of the squares, leaving gaps, and counting a
square twice.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_caon_math_g3_area as car
adopt(car)
from gen_us_math_g3 import grid_rect_svg
tx_common.GRADE = "grade-2"

def whole(it):
    return "½" not in it["q"] + " ".join(it["c"]) + it["e"]


def one_rows(r):
    w, h = r.randint(2, 8), r.randint(2, 6)
    pic = fig(grid_rect_svg(w, h))
    q = r.choice(["Each small square is 1 square unit. How many square units cover the rectangle?", "What is the area of the rectangle in square units?"])
    return mcq(pic + q, "%d square units" % (w * h), ["%d square units" % (2 * (w + h)), "%d square units" % (w + h), "%d square units" % (w * h - w)],
               "%d rows of %d squares: %s = <b>%d square units</b>." % (h, w, " + ".join([str(w)] * h), w * h))


def one_story(r):
    k = Kid(r).next()
    w, h = r.randint(2, 6), r.randint(2, 5)
    thing = r.choice(["sticky notes", "square tiles", "paper squares", "square crackers"])
    if r.random() < 0.5:
        return mcq("%s covers a book with %s. There are %d rows with %d in each row. No gaps or overlaps. What is the area of the book?" % (k["n"], thing, h, w), "%d square units" % (w * h), ["%d square units" % (w + h), "%d square units" % (w * h + w), "%d square units" % (2 * (w + h))],
                   "%d rows of %d = <b>%d square units</b>." % (h, w, w * h))
    a, b = w * h, (w + 1) * h
    return mcq("Rug A is covered by %d square tiles. Rug B is covered by %d square tiles of the same size. Which rug has the greater area?" % (a, b), "Rug B", ["Rug A", "They are the same", "You cannot tell"],
               "%d &gt; %d, so <b>Rug B</b> covers more space." % (b, a))


def build():
    sets, R = build_sets([
        ("Count square units", [("run", car.set_count, ("rnd", "seen"), 20, whole)]),
        ("Rows of squares", [("collect", one_rows, 20)]),
        ("No gaps or overlaps", [("run", car.set_gaps, ("rnd", car.People), 20)]),
        ("Compare areas by covering", [("run", car.set_cover, ("rnd", car.People, [1, 3, 0]), 20)]),
        ("Area stories", [("collect", one_story, 20)]),
    ], 69217)
    finish(sets, R)
    body = lesson('<ul><li><b>Area</b> is how much space a flat shape covers.</li><li>Cover the shape with <b>square units</b> with no gaps and no overlaps, then count the squares.</li><li>For a rectangle, count the squares in one row and add the rows.</li><li>Say the number and the unit: 12 square units.</li></ul>',
        [example("3 rows of 4 squares", ["4 + 4 + 4"], "12 square units")],
        [['Counting the edges instead of the squares', 'Count the squares inside.'], ['Leaving gaps', 'Squares must cover the whole shape.'], ['Counting a square twice', 'Mark each square as you count.']])
    faq = [('What does TEKS 2.9F ask?', 'Use concrete models of square units to find the area of a rectangle by covering it with no gaps or overlaps, counting to find the total number of square units, and describing the measurement using a number and the unit.'), ('Why no gaps or overlaps?', 'Gaps miss space and overlaps count space twice.'), ('Is area the same as perimeter?', 'No. Area covers the inside; perimeter goes around the edge.'), ('What is a square unit?', 'A square that is 1 unit on each side.')]
    make('area-with-square-units', 17, 'Geometry and Measurement', '2.9F',
         '2.9F use concrete models of square units to find the area of a rectangle by covering it with no gaps or overlaps, counting to find the total number of square units, and describing the measurement using a number and the unit',
         'Area: Covering with Square Units', 'Area with Square Units',
         'Free Grade 2 area worksheets for Texas TEKS 2.9F: count square units, rows of squares, no gaps or overlaps, comparing areas and area stories. 100 questions with answers.',
         'Cover with square units, then count.', '3 rows of 4 squares = 12 square units.',
         body, faq, sets, seo_title='Grade 2 Area with Square Units Worksheets (TEKS 2.9F)')


if __name__ == "__main__":
    build()
