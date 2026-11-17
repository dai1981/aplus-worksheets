# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Properties of Quadrilaterals (Australian Curriculum v9.0: AC9M8SP02)
  python3 tools/gen_au_maths_y8_properties_of_quadrilaterals.py
Naming quadrilaterals from their properties, the properties of sides, angles and diagonals, finding angles in
parallelograms, kites, trapeziums and other quadrilaterals, using diagonal properties (including Pythagoras in a
rhombus), and reasoning with congruent triangles.
Wrong answers come from real mistakes: thinking a square is not a rectangle, mixing up the diagonal properties of
a rectangle and a rhombus, taking co-interior angles as equal, and using 180° instead of 360° for the angle sum.
"""
import random
from au_hs import B, S, make, lesson, collect, QN, T

R = random.Random(81601)
SHAPES = ["square", "rectangle", "rhombus", "parallelogram", "kite", "trapezium"]


# ------------------------------------------------------------ set 1: name the quadrilateral
CLUES = [
    ("has four equal sides and four right angles", "Square", ["Rhombus", "Rectangle", "Kite"]),
    ("has four equal sides, but its angles are not right angles", "Rhombus", ["Square", "Kite", "Parallelogram"]),
    ("has four right angles, but its sides are not all equal", "Rectangle", ["Square", "Parallelogram", "Trapezium"]),
    ("has exactly one pair of parallel sides", "Trapezium", ["Parallelogram", "Kite", "Rhombus"]),
    ("has two pairs of equal adjacent sides and its diagonals meet at right angles", "Kite", ["Rhombus", "Trapezium", "Parallelogram"]),
    ("has two pairs of parallel sides, but no right angles and not all sides equal", "Parallelogram", ["Rhombus", "Rectangle", "Trapezium"]),
    ("has diagonals that are equal in length and bisect each other at right angles", "Square", ["Rectangle", "Rhombus", "Kite"]),
    ("has diagonals that are equal in length and bisect each other, but do not meet at right angles", "Rectangle", ["Square", "Rhombus", "Parallelogram"]),
    ("has diagonals that bisect each other at right angles but are not equal", "Rhombus", ["Square", "Kite", "Rectangle"]),
    ("has diagonals that bisect each other but are not equal and do not meet at right angles", "Parallelogram", ["Rectangle", "Rhombus", "Kite"]),
    ("has one diagonal that cuts the other in half at right angles, but not the other way round", "Kite", ["Rhombus", "Square", "Trapezium"]),
    ("has one pair of parallel sides and its two non-parallel sides are equal", "Isosceles trapezium", ["Parallelogram", "Kite", "Rectangle"]),
]


def name_set(r):
    out = []
    for clue, ans, wr in CLUES:
        out.append(T("A quadrilateral %s. What is it?" % clue, ans, wr, "A quadrilateral that %s is a <b>%s</b>." % (clue, ans.lower())))
    extra = [
        ("Is every square a rectangle?", "Yes, because it has four right angles", ["No, because its sides are all equal", "No, a rectangle has two long sides", "Only if it is large"],
         "A rectangle needs four right angles. A square has them, so <b>every square is a rectangle</b>."),
        ("Is every rectangle a square?", "No, its sides need not all be equal", ["Yes, both have four right angles", "Yes, both have equal diagonals", "Only if it is small"],
         "A 3 cm by 5 cm rectangle is not a square, so <b>no</b>."),
        ("Is every rhombus a parallelogram?", "Yes, both pairs of opposite sides are parallel", ["No, a rhombus has equal sides", "No, a rhombus is a kite", "Only if it has right angles"],
         "A rhombus has two pairs of parallel sides, so <b>yes</b>."),
        ("Is every square a rhombus?", "Yes, it has four equal sides", ["No, a rhombus has no right angles", "No, a square is a rectangle", "Only if it is tilted"],
         "A rhombus needs four equal sides. A square has them, so <b>yes</b>."),
        ("Which of these is NOT always a parallelogram?", "Trapezium", ["Rectangle", "Rhombus", "Square"], "A trapezium has only one pair of parallel sides: <b>trapezium</b>."),
        ("Is a rhombus a special kind of kite?", "Yes, it has two pairs of equal adjacent sides", ["No, a kite has no parallel sides", "No, a kite has no equal sides", "Only if it is a square"],
         "All four sides of a rhombus are equal, so it has two pairs of equal adjacent sides: <b>yes</b>."),
        ("Which quadrilateral has both a rectangle's and a rhombus's properties?", "Square", ["Parallelogram", "Kite", "Trapezium"], "Four right angles and four equal sides: a <b>square</b>."),
        ("How many lines of symmetry does a rhombus (that is not a square) have?", "2", ["4", "1", "0"], "Its two diagonals are lines of symmetry: <b>2</b>."),
    ]
    for q, a, w, e in extra:
        out.append(T(q, a, w, e))
    return out


# ------------------------------------------------------------ set 2: properties
PROPS = [
    ("Which property does every parallelogram have?", "Opposite angles are equal", ["All angles are 90°", "Diagonals are equal", "Diagonals meet at right angles"],
     "In a parallelogram <b>opposite angles are equal</b> and opposite sides are equal and parallel."),
    ("Which property does every rectangle have?", "The diagonals are equal in length", ["The diagonals meet at right angles", "All sides are equal", "Exactly one pair of parallel sides"],
     "The diagonals of a rectangle are <b>equal</b> and bisect each other."),
    ("Which property does every rhombus have?", "The diagonals meet at right angles", ["The diagonals are equal", "All angles are 90°", "Only one pair of parallel sides"],
     "The diagonals of a rhombus <b>bisect each other at right angles</b>."),
    ("Which property does every kite have?", "One pair of opposite angles is equal", ["Both pairs of opposite angles are equal", "All sides are equal", "Two pairs of parallel sides"],
     "The angles between the unequal sides of a kite are equal: <b>one pair of opposite angles</b>."),
    ("Which property does every square have that a rhombus may not?", "Equal diagonals", ["Four equal sides", "Diagonals at right angles", "Opposite sides parallel"],
     "Both have equal sides and perpendicular diagonals, but only a square must have <b>equal diagonals</b>."),
    ("Which property does every rectangle have that a parallelogram may not?", "Four right angles", ["Opposite sides equal", "Opposite sides parallel", "Diagonals bisect each other"],
     "Every parallelogram has the other three; a rectangle also has <b>four right angles</b>."),
    ("The diagonals of a parallelogram…", "bisect each other", ["are always equal", "always meet at 90°", "are lines of symmetry"], "The diagonals of a parallelogram <b>bisect each other</b> (cut each other in half)."),
    ("Which quadrilateral can have exactly one line of symmetry?", "Kite", ["Rectangle", "Rhombus", "Square"], "A kite has <b>one</b> line of symmetry along its main diagonal."),
    ("Which quadrilateral has rotational symmetry of order 2 but no lines of symmetry (in general)?", "Parallelogram", ["Kite", "Rectangle", "Isosceles trapezium"],
     "A general <b>parallelogram</b> looks the same after a half turn but has no mirror lines."),
    ("Co-interior angles in a trapezium (between the parallel sides) add up to…", "180°", ["90°", "360°", "They are equal"], "Co-interior angles between parallel lines are supplementary: <b>180°</b>."),
    ("The angles in any quadrilateral add up to…", "360°", ["180°", "540°", "720°"], "A diagonal splits a quadrilateral into two triangles: 2 × 180° = <b>360°</b>."),
    ("In an isosceles trapezium, the two angles at the longer parallel side are…", "equal", ["supplementary", "right angles", "always 60°"], "An isosceles trapezium is symmetric, so its base angles are <b>equal</b>."),
    ("Which statement about a square is FALSE?", "Its diagonals are longer than its sides by 1 cm", ["Its diagonals are equal", "Its diagonals meet at 90°", "Its diagonals bisect its angles"],
     "The diagonal of a square is about 1.41 times the side, not 1 cm longer. The others are all true."),
    ("Which statement about a rhombus is TRUE?", "Its diagonals bisect its angles", ["Its diagonals are equal", "It has four right angles", "It has only one pair of parallel sides"],
     "Each diagonal of a rhombus cuts the angles at its ends in half: <b>its diagonals bisect its angles</b>."),
    ("How many pairs of parallel sides does a kite have (that is not a rhombus)?", "0", ["1", "2", "4"], "A kite has <b>no</b> parallel sides unless it is a rhombus."),
    ("Which quadrilateral has diagonals that are equal but do not bisect each other?", "Isosceles trapezium", ["Rectangle", "Square", "Rhombus"],
     "The diagonals of an <b>isosceles trapezium</b> are equal, but they do not cut each other in half."),
    ("Which two quadrilaterals have diagonals that meet at right angles?", "Rhombus and kite", ["Rectangle and parallelogram", "Trapezium and rectangle", "Parallelogram and trapezium"],
     "The diagonals of a <b>rhombus and a kite</b> are perpendicular (and so are a square's)."),
    ("A parallelogram has one right angle. What can you say about it?", "It is a rectangle", ["It is a rhombus", "It is a kite", "Nothing more"], "Opposite angles are equal and co-interior angles add to 180°, so all four are 90°: <b>a rectangle</b>."),
    ("A parallelogram has two adjacent sides equal. What can you say about it?", "It is a rhombus", ["It is a rectangle", "It is a trapezium", "Nothing more"], "Opposite sides are equal too, so all four sides are equal: <b>a rhombus</b>."),
    ("Which shape's diagonals divide it into four congruent triangles?", "Rhombus", ["Kite", "Trapezium", "Parallelogram (not a rhombus)"],
     "The diagonals of a <b>rhombus</b> bisect each other at right angles, making four congruent right-angled triangles."),
]


# ------------------------------------------------------------ set 3: angles in quadrilaterals
def one_angle(r):
    kind = r.choice(["para_opp", "para_adj", "kite", "trap", "any", "iso_trap"])
    if kind == "para_opp":
        a = r.randint(48, 132)
        q = "In parallelogram ABCD, angle A = %d°. What is angle C?" % a
        return QN(q, a, [180 - a, 360 - a, 90], "Opposite angles of a parallelogram are equal: <b>%d°</b>." % a, unit="°", near=(5, -5))
    if kind == "para_adj":
        a = r.randint(48, 132)
        if a == 90:
            return None
        q = "In parallelogram ABCD, angle A = %d°. What is angle B?" % a
        return QN(q, 180 - a, [a, 360 - a, 90 - a if a < 90 else a - 90], "Angles A and B are co-interior, so they add to 180°: 180° − %d° = <b>%d°</b>." % (a, 180 - a), unit="°", near=(5, -5))
    if kind == "kite":
        a, b = r.randint(50, 130), r.randint(40, 120)
        x = (360 - a - b) / 2
        if x != int(x) or not 30 < x < 150 or a == b:
            return None
        x = int(x)
        q = "A kite has angles of %d° and %d° at the ends of its line of symmetry. The other two angles are equal. Find one of them." % (a, b)
        return QN(q, x, [360 - a - b, 180 - x, (180 - a - b) if a + b < 180 else x + 10], "360° − %d° − %d° = %d°, shared equally: <b>%d°</b>." % (a, b, 360 - a - b, x), unit="°", near=(5, -5))
    if kind == "trap":
        a = r.randint(55, 125)
        q = "In trapezium ABCD, AB is parallel to DC and angle A = %d°. What is angle D?" % a
        return QN(q, 180 - a, [a, 360 - a, 90], "Angles A and D are co-interior between parallel lines, so they add to 180°: <b>%d°</b>." % (180 - a), unit="°", near=(5, -5))
    if kind == "iso_trap":
        a = r.randint(50, 85)
        q = "An isosceles trapezium has two angles of %d° at its longer parallel side. What is each of the other two angles?" % a
        return QN(q, 180 - a, [a, 360 - 2 * a, 90], "Each pair of co-interior angles adds to 180°: 180° − %d° = <b>%d°</b>." % (a, 180 - a), unit="°", near=(5, -5))
    a, b, c = r.randint(60, 130), r.randint(60, 130), r.randint(50, 120)
    d = 360 - a - b - c
    if not 30 < d < 170:
        return None
    q = "Three angles of a quadrilateral are %d°, %d° and %d°. What is the fourth angle?" % (a, b, c)
    return QN(q, d, [180 - a - b - c if 180 - a - b - c > 0 else d + 20, 540 - a - b - c, d + 10], "The angles add to 360°: 360° − %d° − %d° − %d° = <b>%d°</b>." % (a, b, c, d), unit="°", near=(5, -5))


# ------------------------------------------------------------ set 4: diagonals and sides
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)]


def one_diag(r):
    kind = r.choice(["rhombus", "rect", "para", "rhombus", "rect_x"])
    if kind == "rhombus":
        a, b, c = r.choice(TRIPLES)
        q = "The diagonals of a rhombus are %d cm and %d cm long. How long is each side?" % (2 * a, 2 * b)
        e = "The diagonals bisect each other at right angles, making right-angled triangles with legs %d cm and %d cm. Side = √(%d² + %d²) = <b>%d cm</b>." % (a, b, a, b, c)
        return QN(q, c, [2 * c, a + b, c * c], e, unit=" cm")
    if kind == "rect":
        d = r.randint(6, 30)
        q = "The diagonals of rectangle ABCD meet at E. AC = %d cm. How long is BE?" % (2 * d)
        e = "The diagonals of a rectangle are equal and bisect each other, so BE = ½ × %d = <b>%d cm</b>." % (2 * d, d)
        return QN(q, d, [2 * d, 4 * d, d + 2], e, unit=" cm")
    if kind == "para":
        x = r.randint(2, 9)
        a, b = r.randint(2, 4), r.randint(1, 6)
        c = r.randint(1, a - 1) if a > 1 else 1
        d = a * x + b - c * x
        if d <= 0 or c == a:
            return None
        q = "The diagonals of parallelogram PQRS meet at M. PM = %d<i>x</i> + %d and MR = %s<i>x</i> + %d. Find <i>x</i>." % (a, b, "" if c == 1 else str(c), d)
        e = "The diagonals bisect each other, so PM = MR: %d<i>x</i> + %d = %s<i>x</i> + %d. So %s<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (
            a, b, "" if c == 1 else str(c), d, "" if a - c == 1 else str(a - c), d - b, x)
        return QN(q, x, [d - b, (d + b) // (a - c) if (d + b) % (a - c) == 0 else x + 3, (d - b) * (a - c) if a - c > 1 else x + 4], e)
    if kind == "rect_x":
        x = r.randint(2, 9)
        a, b = r.randint(2, 5), r.randint(1, 8)
        L = a * x + b
        q = "In rectangle ABCD, AC = %d<i>x</i> + %d and BD = %d cm. Find <i>x</i>." % (a, b, L)
        e = "The diagonals of a rectangle are equal: %d<i>x</i> + %d = %d, so %d<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (a, b, L, a, L - b, x)
        return QN(q, x, [L - b, (L + b) // a if (L + b) % a == 0 else x + 2, L // a if L // a != x else x + 1], e)
    return None


# ------------------------------------------------------------ set 5: reasoning
def problems():
    data = [
        ("A diagonal is drawn in parallelogram ABCD, from A to C. Which test shows that triangles ABC and CDA are congruent?", "SSS", ["RHS", "AAA", "They are not congruent"],
         "AB = CD and BC = DA (opposite sides), and AC is shared: <b>SSS</b>."),
        ("Why are the opposite angles of a parallelogram equal?", "A diagonal splits it into two congruent triangles", ["All its angles are right angles", "Its diagonals are equal", "It has a line of symmetry"],
         "The diagonal makes two congruent triangles, so matching angles are equal: <b>two congruent triangles</b>."),
        ("In kite ABCD, AB = AD and CB = CD. Which test shows triangles ABC and ADC are congruent?", "SSS", ["SAS", "RHS", "AAS"], "AB = AD, CB = CD and AC is shared: <b>SSS</b>."),
        ("A quadrilateral has angles 90°, 90°, 90° and <i>x</i>°. What is <i>x</i>?", "90", ["180", "270", "45"], "360 − 270 = <b>90</b>, so it is a rectangle (or square)."),
        ("A rhombus has one angle of 64°. What are its other three angles?", "116°, 64° and 116°", ["64°, 64° and 64°", "116°, 116° and 116°", "26°, 64° and 26°"],
         "Opposite angles are equal and neighbouring angles add to 180°: <b>116°, 64°, 116°</b>."),
        ("A square has a side of 6 cm. How long is its diagonal, to 1 decimal place?", "8.5 cm", ["12 cm", "6 cm", "7.2 cm"], "√(6² + 6²) = √72 = <b>8.5 cm</b>."),
        ("A rectangle is 8 cm by 6 cm. How long is each diagonal?", "10 cm", ["14 cm", "7 cm", "12 cm"], "√(8² + 6²) = √100 = <b>10 cm</b>."),
        ("A rhombus has a side of 10 cm and one diagonal of 12 cm. How long is the other diagonal?", "16 cm", ["8 cm", "14 cm", "20 cm"], "Half-diagonals: 6 and √(10² − 6²) = 8. Other diagonal = 2 × 8 = <b>16 cm</b>."),
        ("The angles of a quadrilateral are <i>x</i>, 2<i>x</i>, 3<i>x</i> and 4<i>x</i>. What is the largest angle?", "144°", ["36°", "120°", "160°"], "10<i>x</i> = 360, so <i>x</i> = 36 and 4<i>x</i> = <b>144°</b>."),
        ("In parallelogram PQRS, angle P = 3<i>x</i> and angle Q = 2<i>x</i>. Find angle P.", "108°", ["72°", "36°", "90°"], "Co-interior: 5<i>x</i> = 180, so <i>x</i> = 36 and angle P = <b>108°</b>."),
        ("Which is the best name for a quadrilateral with vertices (0, 0), (4, 0), (4, 3) and (0, 3)?", "Rectangle", ["Square", "Rhombus", "Kite"], "Four right angles, sides 4 and 3: <b>rectangle</b>."),
        ("Which is the best name for a quadrilateral with vertices (0, 0), (3, 1), (4, 4) and (1, 3)?", "Rhombus", ["Square", "Rectangle", "Trapezium"],
         "Every side is √10 long, but the angles are not 90° (the diagonals are different lengths): <b>rhombus</b>."),
        ("Amelia says a shape with four equal sides must be a square. Is she right?", "No, it could be a rhombus", ["Yes", "No, it could be a kite with unequal sides", "No, it could be a trapezium"],
         "A rhombus has four equal sides without right angles, so <b>no</b>."),
        ("A kite has angles 110°, 70° and <i>y</i>, <i>y</i>, where the two <i>y</i> angles are equal. Find <i>y</i>.", "90°", ["180°", "110°", "70°"], "2<i>y</i> = 360 − 180 = 180, so <i>y</i> = <b>90°</b>."),
        ("The diagonals of a quadrilateral are equal and bisect each other at right angles. What is it?", "Square", ["Rectangle", "Rhombus", "Kite"], "Equal and bisecting → rectangle; at right angles → rhombus. Both: <b>square</b>."),
        ("A quadrilateral has exactly one pair of parallel sides, and its two angles at one base are 70° and 70°. What is it?", "Isosceles trapezium", ["Parallelogram", "Kite", "Rhombus"],
         "One pair of parallel sides with equal base angles: <b>isosceles trapezium</b>."),
        ("In rhombus ABCD, angle ABD = 35°. What is angle ABC?", "70°", ["35°", "110°", "145°"], "The diagonal BD bisects angle B, so angle ABC = 2 × 35° = <b>70°</b>."),
        ("In rectangle ABCD, the diagonals meet at E and angle AEB = 120°. What is angle EAB?", "30°", ["60°", "120°", "45°"],
         "AE = BE (half-diagonals are equal), so triangle AEB is isosceles: (180° − 120°) ÷ 2 = <b>30°</b>."),
        ("A trapezium has parallel sides 6 cm and 10 cm. How many pairs of equal angles must it have?", "None", ["One", "Two", "Four"],
         "A general trapezium only has co-interior angles adding to 180°. Equal angles are only guaranteed in an isosceles trapezium: <b>none</b>."),
        ("Which set of conditions proves a quadrilateral is a parallelogram?", "Both pairs of opposite sides are equal", ["One pair of sides is parallel", "The diagonals are perpendicular", "Two angles are equal"],
         "If both pairs of opposite sides are equal, a diagonal makes two congruent triangles (SSS), which makes the sides parallel: <b>parallelogram</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<ul><li><b>Parallelogram</b>: opposite sides parallel and equal; opposite angles equal; diagonals bisect each other.</li>"
        "<li><b>Rectangle</b>: a parallelogram with four right angles; diagonals are equal.</li>"
        "<li><b>Rhombus</b>: a parallelogram with four equal sides; diagonals meet at right angles and bisect the angles.</li>"
        "<li><b>Square</b>: both a rectangle and a rhombus.</li>"
        "<li><b>Kite</b>: two pairs of equal adjacent sides; diagonals meet at right angles; one pair of opposite angles equal.</li>"
        "<li><b>Trapezium</b>: exactly one pair of parallel sides; co-interior angles add to 180°.</li></ul>"
        "<p>The angles in any quadrilateral add to <b>360°</b>. Many properties can be proved by drawing a diagonal and using <b>congruent triangles</b>.</p>",
        [("In parallelogram ABCD, angle A = 65°. Find angles B, C and D.", ["B is co-interior with A: 180° − 65° = 115°.", "Opposite angles are equal."], "B = 115°, C = 65°, D = 115°"),
         ("The diagonals of a rhombus are 6 cm and 8 cm. Find the side length.", ["Half-diagonals are 3 cm and 4 cm and meet at 90°.", "√(3² + 4²) = 5."], "5 cm")],
        ["Thinking a square is not a rectangle. A square has four right angles, so it is a special rectangle.",
         "Mixing up diagonals: a rectangle's are equal; a rhombus's meet at right angles.",
         "Taking co-interior angles as equal. They add to 180°.",
         "Using 180° as the angle sum of a quadrilateral. It is 360°."])


def main():
    names = name_set(R)
    R.shuffle(names)
    sets = [S("Naming quadrilaterals", names),
            S("Properties of quadrilaterals", [T(q, a, w, e) for q, a, w, e in PROPS]),
            S("Angles in quadrilaterals", collect(one_angle, 20, R)),
            S("Using the diagonals", collect(one_diag, 20, R)),
            S("Reasoning with quadrilaterals", problems())]
    make(8, "properties-of-quadrilaterals", 16, "AC9M8SP02",
         "Properties of Quadrilaterals: Sides, Angles and Diagonals",
         "Year 8 Quadrilaterals Worksheets: Properties, Angles and Diagonals (Free, Answer Key)",
         "Properties of quadrilaterals",
         "establish properties of quadrilaterals using congruent triangles and angle properties, and solve related problems explaining reasoning",
         "Free Year 8 maths worksheets on quadrilaterals for the Australian Curriculum (AC9M8SP02): parallelograms, rectangles, rhombuses, "
         "squares, kites and trapeziums, their angles and diagonals, and reasoning with congruent triangles. 100 questions with an answer key.",
         "Parallelogram diagonals bisect each other. Rectangle diagonals are equal. Rhombus and kite diagonals meet at right angles.",
         "The angles in a quadrilateral add to 360°. A square is both a rectangle and a rhombus.",
         body(),
         [("What are the properties of a parallelogram?", "Opposite sides are parallel and equal, opposite angles are equal, neighbouring angles add to 180° and the diagonals bisect each other."),
          ("What is the difference between a rhombus and a square?", "Both have four equal sides, but a square also has four right angles and equal diagonals."),
          ("Is a square a rectangle?", "Yes. A rectangle is a quadrilateral with four right angles, and a square has four right angles."),
          ("How do congruent triangles prove properties of quadrilaterals?", "Drawing a diagonal splits the shape into two triangles. If they are congruent (for example by SSS), their matching sides and angles are equal.")],
         sets, R)


if __name__ == "__main__":
    main()
