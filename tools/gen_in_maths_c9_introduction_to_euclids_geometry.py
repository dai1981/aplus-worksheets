# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 5: Introduction to Euclid's Geometry (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c9_introduction_to_euclids_geometry.py
Euclid's definitions and undefined terms, the seven common notions (axioms) and naming the axiom used, the five postulates
and their consequences (a unique line through two points, two lines meet in at most one point), using the axioms with
numbers (points between, mid-points, equals added or doubled), and true-or-false reasoning.
Wrong answers come from real mistakes: mixing up axioms and postulates, thinking two points have many lines through
them, “the part is greater than the whole”, and confusing a theorem with a postulate.
"""
import random
from in_common import num, S, make, lesson, mix, T

R = random.Random(909005)

TERMS = [
    ("According to Euclid, a point is", "that which has no part", ["that which has length only", "a very small circle", "that which has length and breadth"]),
    ("According to Euclid, a line is", "breadthless length", ["that which has no part", "a surface with length and breadth", "the shortest path between three points"]),
    ("According to Euclid, the ends of a line are", "points", ["surfaces", "lines", "planes"]),
    ("According to Euclid, a surface is", "that which has length and breadth only", ["breadthless length", "that which has no part", "that which has length, breadth and height"]),
    ("According to Euclid, the edges of a surface are", "lines", ["points", "solids", "planes"]),
    ("A solid has how many dimensions?", "Three", ["Two", "One", "None"]),
    ("A surface has how many dimensions?", "Two", ["Three", "One", "None"]),
    ("A line has how many dimensions?", "One", ["Two", "Three", "None"]),
    ("A point has how many dimensions?", "None", ["One", "Two", "Three"]),
    ("In modern geometry, which terms are taken as undefined?", "Point, line and plane", ["Circle, square and line", "Angle, ray and segment", "Triangle, point and arc"]),
    ("A statement that is proved using definitions, axioms and earlier results is called a", "theorem", ["postulate", "axiom", "definition"]),
    ("Euclid's book on geometry is called the", "Elements", ["Principia", "Sulbasutras", "Aryabhatiya"]),
    ("Euclid lived in", "Alexandria, Egypt, around 300 BCE", ["Athens, around 1000 CE", "Babylon, around 3000 BCE", "Rome, around 500 CE"]),
    ("The Sulbasutras of ancient India were manuals for", "constructing fire altars", ["measuring rainfall", "writing poetry", "keeping accounts"]),
    ("Two lines which do not meet, however far they are extended, are called", "parallel lines", ["intersecting lines", "concurrent lines", "perpendicular lines"]),
    ("Two distinct lines in a plane can have at most how many points in common?", "One", ["Two", "None", "Infinitely many"]),
    ("Three or more lines that pass through the same point are called", "concurrent lines", ["parallel lines", "collinear points", "perpendicular lines"]),
    ("Points that lie on the same line are called", "collinear points", ["concurrent points", "parallel points", "coplanar lines"]),
    ("A line segment has", "two end points", ["one end point", "no end points", "three end points"]),
    ("A ray has", "one end point", ["two end points", "no end points", "three end points"]),
    ("A line has", "no end points", ["one end point", "two end points", "a fixed length"]),
    ("Euclid's assumptions about geometry, which are not proved, are called", "postulates", ["theorems", "corollaries", "lemmas"]),
    ("Euclid's assumptions that are used throughout mathematics, not only in geometry, are called", "axioms (common notions)", ["postulates", "theorems", "definitions"]),
]

AXIOMS = {
    1: "Things which are equal to the same thing are equal to one another.",
    2: "If equals are added to equals, the wholes are equal.",
    3: "If equals are subtracted from equals, the remainders are equal.",
    4: "Things which coincide with one another are equal to one another.",
    5: "The whole is greater than the part.",
    6: "Things which are double of the same things are equal to one another.",
    7: "Things which are halves of the same things are equal to one another.",
}

POSTULATES = [
    ("Euclid's Postulate 1 says", "a straight line may be drawn from any one point to any other point", ["a terminated line can be produced indefinitely", "all right angles are equal", "a circle can be drawn with any centre and radius"]),
    ("Euclid's Postulate 2 says", "a terminated line can be produced indefinitely", ["a straight line may be drawn from any one point to any other point", "all right angles are equal", "a circle can be drawn with any centre and radius"]),
    ("Euclid's Postulate 3 says", "a circle can be drawn with any centre and any radius", ["all right angles are equal", "a terminated line can be produced indefinitely", "parallel lines never meet"]),
    ("Euclid's Postulate 4 says", "all right angles are equal to one another", ["a circle can be drawn with any centre and any radius", "the whole is greater than the part", "two lines meet in one point"]),
    ("Euclid's fifth postulate is about", "parallel lines", ["circles", "right angles", "equal chords"]),
    ("How many lines can pass through two distinct points?", "Exactly one", ["Two", "Infinitely many", "None"]),
    ("How many lines can pass through a single point?", "Infinitely many", ["Exactly one", "Two", "None"]),
    ("Through a point P not on a line l, how many lines can be drawn parallel to l (Playfair's axiom)?", "Exactly one", ["None", "Two", "Infinitely many"]),
    ("Given two distinct points, there is a unique line through them. This is", "an axiom (Axiom 5.1 in NCERT)", ["Theorem 5.1", "Euclid's fifth postulate", "a definition"]),
    ("“Two distinct lines cannot have more than one point in common” is", "a theorem proved from the axioms", ["Euclid's first postulate", "an undefined term", "a definition"]),
    ("Which postulate lets us extend a line segment AB beyond B?", "Postulate 2", ["Postulate 1", "Postulate 3", "Postulate 4"]),
    ("Which postulate lets us draw a circle with centre A and radius AB?", "Postulate 3", ["Postulate 1", "Postulate 2", "Postulate 5"]),
    ("Which postulate lets us join any two points with a straight line?", "Postulate 1", ["Postulate 2", "Postulate 3", "Postulate 4"]),
    ("Equivalent versions of Euclid's fifth postulate include", "two distinct intersecting lines cannot both be parallel to the same line", ["all right angles are equal", "the whole is greater than the part", "a point has no part"]),
    ("If a straight line falling on two straight lines makes the interior angles on the same side less than two right angles, then", "the two lines meet on that side when produced", ["the two lines are parallel", "the two lines meet on the other side", "the lines are perpendicular"]),
    ("Postulates are", "assumptions specific to geometry", ["results proved from axioms", "the same as definitions", "assumptions used only in algebra"]),
    ("A system of axioms is consistent if", "it is impossible to deduce a statement that contradicts another axiom or proved statement", ["every statement is a postulate", "it has exactly five axioms", "it contains no definitions"]),
    ("How many common points can a line and a circle have at most?", "Two", ["One", "Three", "Infinitely many"]),
    ("Can two distinct lines both pass through the two points A and B?", "No, only one line passes through two points", ["Yes, always", "Yes, if they are parallel", "Only if A and B are close"]),
    ("Can every line segment be extended on both sides?", "Yes, by Postulate 2", ["No, only on one side", "Only if it is horizontal", "No, a segment has fixed ends"]),
    ("If C is the mid-point of AB, how many mid-points can AB have?", "Exactly one", ["Two", "Infinitely many", "None"]),
]


def statement(q, a, w):
    return T(q if q.endswith("?") else q + " ___.", a, w, "<b>%s</b>." % a)


# ---------------------------------------------------------------- set 1: terms and definitions
def one_term(r):
    q, a, w = r.choice(TERMS)
    return statement(q, a, w)


# ---------------------------------------------------------------- set 2: naming the axiom
def one_ax(r):
    kind = r.choice(["name", "name", "num", "num", "text"])
    names = ["AB", "CD", "EF", "PQ", "RS", "XY"]
    if kind == "text":
        k = r.randint(1, 7)
        return T("Which of Euclid's axioms says: “%s”" % AXIOMS[k], "Axiom %d" % k, ["Axiom %d" % j for j in r.sample([j for j in range(1, 8) if j != k], 3)], "This is <b>Axiom %d</b>." % k)
    if kind == "name":
        a, b, c = r.sample(names, 3)
        t = r.choice([1, 2, 3, 6, 7])
        if t == 1:
            q = "If %s = %s and %s = %s, then %s = %s." % (a, b, c, b, a, c)
        elif t == 2:
            q = "If %s = %s, then %s + %s = %s + %s (the same length added to both)." % (a, b, a, c, b, c)
        elif t == 3:
            q = "If %s = %s, then %s − %s = %s − %s." % (a, b, a, c, b, c)
        elif t == 6:
            q = "If 2 × %s = 2 × %s, then %s = %s." % (a, b, a, b)
        else:
            q = "If ½ %s = ½ %s, then %s = %s." % (a, b, a, b)
        return T("Which axiom is used? %s" % q, "Axiom %d: %s" % (t, AXIOMS[t]), ["Axiom %d: %s" % (j, AXIOMS[j]) for j in r.sample([j for j in (1, 2, 3, 4, 5, 6, 7) if j != t], 3)],
                 "<b>Axiom %d</b>: %s" % (t, AXIOMS[t]))
    x = r.randint(3, 30)
    y = r.randint(2, 20)
    t = r.choice([1, 2, 3, 5])
    if t == 1:
        return T("Ali and Kavi each have the same number of pencils as Rahul, who has %d. How many pencils does Kavi have, and which axiom gives this?" % x,
                 "%d, by Axiom 1" % x, ["%d, by Axiom 2" % x, "%d, by Axiom 1" % (2 * x), "%d, by Axiom 5" % x],
                 "Things equal to the same thing are equal to one another (Axiom 1): <b>%d</b>." % x)
    if t == 2:
        return T("AB = CD = %d cm. A length of %d cm is added to each. Which statement is correct?" % (x, y), "The new lengths are equal (%d cm each), by Axiom 2" % (x + y),
                 ["The new lengths are equal (%d cm each), by Axiom 3" % (x + y), "The new lengths are %d cm and %d cm" % (x + y, x), "The new lengths are equal (%d cm each), by Axiom 2" % (x * y)],
                 "Equals added to equals give equal wholes (Axiom 2): <b>%d cm each</b>." % (x + y))
    if t == 3:
        if y >= x:
            return None
        return T("Two ropes are each %d m long. %d m is cut from each. Which statement is correct?" % (x, y), "The remaining pieces are equal (%d m each), by Axiom 3" % (x - y),
                 ["The remaining pieces are equal (%d m each), by Axiom 2" % (x - y), "The remaining pieces are %d m and %d m" % (x - y, x), "The remaining pieces are equal (%d m each), by Axiom 3" % (x + y)],
                 "Equals subtracted from equals leave equal remainders (Axiom 3): <b>%d m each</b>." % (x - y))
    return T("C lies between A and B on a line, with AC = %d cm and CB = %d cm. Which is true?" % (x, y), "AB &gt; AC, by Axiom 5 (the whole is greater than the part)",
             ["AC &gt; AB, by Axiom 5", "AB = AC, by Axiom 1", "AB &lt; CB, by Axiom 3"], "AB = %d cm is the whole and AC is a part: <b>AB &gt; AC</b> (Axiom 5)." % (x + y))


# ---------------------------------------------------------------- set 3: postulates
def one_post(r):
    q, a, w = r.choice(POSTULATES)
    return statement(q, a, w)


# ---------------------------------------------------------------- set 4: using the axioms with lengths
def one_len(r):
    kind = r.choice(["between", "between", "mid", "mid", "twice"])
    if kind == "between":
        ac, cb = r.randint(2, 15), r.randint(2, 15)
        want = r.choice(["AB", "CB"])
        if want == "AB":
            return T("Point C lies between A and B. AC = %d cm and CB = %d cm. Find AB." % (ac, cb), "%d cm" % (ac + cb), ["%d cm" % abs(ac - cb) if ac != cb else "%d cm" % (ac * 2 + 1), "%d cm" % (ac * cb), "%d cm" % max(ac, cb)],
                     "C is between A and B, so AB = AC + CB = <b>%d cm</b>." % (ac + cb))
        ab = ac + cb
        return T("Point C lies between A and B. AB = %d cm and AC = %d cm. Find CB." % (ab, ac), "%d cm" % cb, ["%d cm" % (ab + ac), "%d cm" % ac if ac != cb else "%d cm" % (cb + 1), "%d cm" % (ab // 2) if ab // 2 != cb else "%d cm" % (cb + 2)],
                 "AC + CB = AB, so CB = %d − %d = <b>%d cm</b>." % (ab, ac, cb))
    if kind == "mid":
        ab = 2 * r.randint(3, 25)
        return T("C is the mid-point of AB and AB = %d cm. Find AC." % ab, "%d cm" % (ab // 2), ["%d cm" % ab, "%d cm" % (ab * 2), "%d cm" % (ab // 4) if ab % 4 == 0 else "%d cm" % (ab // 2 + 1)],
                 "AC = CB and AC + CB = AB, so 2AC = AB and AC = <b>%d cm</b>." % (ab // 2))
    x = r.randint(3, 20)
    return T("On a line the points are in the order A, B, C, D with AC = BD. If AB = %d cm, find CD." % x, "%d cm" % x, ["%d cm" % (2 * x), "%d cm" % (x + 1), "It cannot be found"],
             "AC = AB + BC and BD = BC + CD. Subtracting BC from equals (Axiom 3) gives AB = CD = <b>%d cm</b>." % x)


# ---------------------------------------------------------------- set 5: true or false
TF = [
    ("Only one line can pass through a single point.", "False", "Infinitely many lines pass through one point."),
    ("There are infinitely many lines that pass through two distinct points.", "False", "Exactly one line passes through two distinct points."),
    ("A terminated line can be produced indefinitely on both sides.", "True", "This is Euclid's second postulate."),
    ("If two circles are equal, then their radii are equal.", "True", "Equal circles coincide when placed on each other, so their radii are equal."),
    ("If AB = PQ and PQ = XY, then AB = XY.", "True", "Things equal to the same thing are equal to one another (Axiom 1)."),
    ("The part can be greater than the whole.", "False", "Axiom 5: the whole is greater than the part."),
    ("Two distinct intersecting lines can both be parallel to the same line.", "False", "This contradicts an equivalent form of the fifth postulate."),
    ("Euclid's definitions of point and line are now accepted as precise.", "False", "Words like “part” and “breadth” need further definition, so point and line are taken as undefined."),
    ("All right angles are equal to one another.", "True", "This is Euclid's fourth postulate."),
    ("A line segment has a definite length.", "True", "It has two end points and a fixed length."),
    ("A ray can be measured with a ruler.", "False", "A ray goes on forever in one direction, so it has no length."),
    ("Two lines in a plane always meet at a point.", "False", "Parallel lines never meet."),
    ("Postulates and axioms are proved using theorems.", "False", "Axioms and postulates are assumed; theorems are proved from them."),
    ("If x + y = 10 and x = z, then z + y = 10.", "True", "Replacing x by the equal thing z keeps the sum equal (Axiom 1 with Axiom 2)."),
    ("A circle can be drawn with any point as centre and any length as radius.", "True", "This is Euclid's third postulate."),
    ("Every point of a line segment AB, except A and B, lies between A and B.", "True", "That is what “between” means for a segment."),
    ("Things which are halves of the same things are equal to one another.", "True", "This is Euclid's seventh axiom."),
    ("Euclid's fifth postulate is about circles.", "False", "It is about parallel lines."),
    ("Through a point not on a line, more than one parallel to that line can be drawn.", "False", "Playfair's axiom: exactly one parallel can be drawn."),
    ("The edges of a surface are curves only.", "False", "Euclid said the edges of a surface are lines."),
    ("A theorem is a statement that is proved.", "True", "Theorems are proved from definitions, axioms and earlier results."),
]


def one_tf(r):
    q, a, e = r.choice(TF)
    return T("True or false? %s" % q, a, ["False" if a == "True" else "True", "True only for straight lines", "It cannot be decided"], "<b>%s</b>. %s" % (a, e))


def main():
    seen = set()
    sets = [
        S("Definitions and undefined terms", mix(R, [(one_term, 20)], seen)),
        S("Euclid's axioms", mix(R, [(one_ax, 20)], seen)),
        S("Euclid's postulates", mix(R, [(one_post, 20)], seen)),
        S("Using the axioms with lengths", mix(R, [(one_len, 20)], seen)),
        S("True or false?", mix(R, [(one_tf, 20)], seen)),
    ]
    body = lesson(
        "<p>Euclid (about 300 BCE) collected geometry in his <b>Elements</b>. He started from definitions, <b>axioms</b> (common notions used in all mathematics) and <b>postulates</b> (assumptions about geometry), and proved <b>theorems</b> from them.</p>"
        "<p>Axioms include: things equal to the same thing are equal; equals added to equals give equals; the whole is greater than the part.</p>"
        "<p>Postulates: a line can be drawn through any two points; a segment can be extended; a circle can be drawn with any centre and radius; all right angles are equal; the fifth postulate is about parallel lines.</p>",
        [("If AC = BD and C, D lie on AB as A, C, D, B, show AD = CB.", ["AC + CD = BD + CD (Axiom 2)", "So AD = CB"], "AD = CB"),
         ("How many lines pass through two points A and B?", ["Axiom 5.1: a unique line"], "Exactly one")],
        ["Mixing up axioms and postulates. Postulates are about geometry only.",
         "Thinking many lines can pass through two points. Only one can.",
         "Calling a proved result a postulate. Proved results are theorems."])
    faq = [
        ("What is the difference between an axiom and a postulate?", "Euclid used axioms (common notions) for assumptions used throughout mathematics, and postulates for assumptions specific to geometry. Today both words are often used for any basic assumption."),
        ("What are Euclid's five postulates?", "1) A straight line can be drawn between any two points. 2) A segment can be produced indefinitely. 3) A circle can be drawn with any centre and radius. 4) All right angles are equal. 5) The parallel postulate."),
        ("Why are point, line and plane undefined?", "Defining them needs other words (part, breadth, length) that would also need defining, so they are taken as undefined terms."),
        ("What is Playfair's axiom?", "For every line l and every point P not on l, there is exactly one line through P parallel to l. It is equivalent to Euclid's fifth postulate."),
    ]
    make(9, "introduction-to-euclids-geometry", 5, "IV", 5, "Introduction to Euclid's Geometry: Axioms and Postulates", "Euclid's geometry",
         "History: geometry in India and Euclid's geometry; Euclid's method of formalising observed phenomena into rigorous mathematics with definitions, common notions, axioms and postulates and theorems; the five postulates of Euclid; showing the relationship between axiom and theorem (summary of the CBSE syllabus)",
         "Class 9 Introduction to Euclid's Geometry worksheet (NCERT Chapter 5): definitions, undefined terms, Euclid's axioms and postulates, using the axioms and true-or-false reasoning. 100 questions with answers.",
         "Axioms and postulates are assumed; theorems are proved", "Through two distinct points there is exactly one line.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
