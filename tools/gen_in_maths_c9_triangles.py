# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 7: Triangles — Congruence (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c9_triangles.py
Congruence criteria SAS, ASA, AAS, SSS and RHS with marked figures, corresponding parts (CPCT), what else is needed for a
criterion, properties of isosceles triangles (angles opposite equal sides), and CPCT with algebra. Sets 1–3 and 5 reuse the
US Geometry makers with Indian names for the criteria (RHS instead of HL, CPCT instead of CPCTC).
Wrong answers come from real mistakes: AAA or SSA taken as congruence, the angle not between the sides used for SAS,
matching vertices out of order, and the equal angles of an isosceles triangle taken at the wrong vertices.
"""
import random, re
from in_common import num, S, make, lesson, mix, T, QN, adopt, gb
import gen_us_math_ge_congruent_triangles as us

R = random.Random(909007)
adopt(us, R)


def ind(fn):
    g = gb(fn)

    def f(r):
        it = g(r)
        if not it:
            return None
        fix = lambda t: re.sub(r"\bHL\b", "RHS", t).replace("Hypotenuse-Leg", "RHS").replace("shortcut", "criterion")
        it["q"], it["e"] = fix(it["q"]), fix(it["e"])
        it["c"] = [fix(c) for c in it["c"]]
        return it
    f.__name__ = fn.__name__
    return f


# ---------------------------------------------------------------- set 4: isosceles triangles
def one_iso(r):
    kind = r.choice(["base", "base", "apex", "apex", "ext", "equi"])
    if kind == "base":
        a = r.choice(range(20, 160, 2))
        b = (180 - a) // 2
        return QN("In △ABC, AB = AC and ∠A = %d°. Find ∠B." % a, b, [180 - a, a, 90 - a // 2 if 90 - a // 2 != b else b + 10],
                  "Angles opposite equal sides are equal, so ∠B = ∠C = (180° − %d°) ÷ 2 = <b>%d°</b>." % (a, b), unit="°")
    if kind == "apex":
        b = r.randint(20, 85)
        return QN("In △PQR, PQ = PR and ∠Q = %d°. Find ∠P." % b, 180 - 2 * b, [180 - b, b, 90 - b if 90 - b != 180 - 2 * b else b + 5],
                  "∠R = ∠Q = %d° (opposite equal sides). ∠P = 180° − 2 × %d° = <b>%d°</b>." % (b, b, 180 - 2 * b), unit="°")
    if kind == "ext":
        b = r.randint(25, 80)
        return QN("In △ABC, AB = AC. BC is produced to D, and ∠ACD = %d°. Find ∠A." % (180 - b), 180 - 2 * b, [b, 180 - b, 2 * b],
                  "∠ACB = 180° − %d° = %d°, so ∠B = %d° too. ∠A = 180° − 2 × %d° = <b>%d°</b>." % (180 - b, b, b, b, 180 - 2 * b), unit="°")
    t = r.choice([("Each angle of an equilateral triangle is", "60°", ["90°", "45°", "180°"], "All sides are equal, so all angles are equal: 180° ÷ 3 = 60°."),
                  ("In an isosceles right triangle, each acute angle is", "45°", ["60°", "30°", "90°"], "The two acute angles are equal and add up to 90°."),
                  ("If two angles of a triangle are equal, then the sides opposite them are", "equal", ["perpendicular", "parallel", "in the ratio 1 : 2"], "This is the converse of the isosceles triangle theorem."),
                  ("In △ABC, ∠B = ∠C. Which two sides are equal?", "AB and AC", ["AB and BC", "BC and AC", "No two sides"], "The sides opposite the equal angles B and C are AC and AB."),
                  ("The angles opposite the equal sides of an isosceles triangle are", "equal", ["supplementary", "complementary", "right angles"], "Theorem 7.2 (NCERT)."),
                  ("In △XYZ, XY = XZ. Which two angles are equal?", "∠Y and ∠Z", ["∠X and ∠Y", "∠X and ∠Z", "No two angles"], "The equal angles are opposite the equal sides XZ and XY."),
                  ("The bisector of the vertical angle of an isosceles triangle", "bisects the base at right angles", ["is parallel to the base", "is equal to the base", "meets the base at 45°"], "The two halves are congruent (SAS), so it cuts the base into equal parts at 90°.")])
    q, a, w, e = t
    return T(q if q.endswith("?") else q + " ___.", a, w, e + " <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        S("Which criterion proves congruence?", mix(R, [(ind(us.one_crit), 20)], seen)),
        S("Corresponding parts (CPCT)", mix(R, [(ind(us.one_corr), 20)], seen)),
        S("What else is needed?", mix(R, [(ind(us.one_need), 20)], seen)),
        S("Isosceles triangles", mix(R, [(one_iso, 20)], seen)),
        S("CPCT with algebra", mix(R, [(ind(us.one_cpctc), 20)], seen)),
    ]
    body = lesson(
        "<p>Two triangles are <b>congruent</b> if their corresponding sides and angles are equal. Write the vertices in matching order: △ABC ≅ △PQR means A ↔ P, B ↔ Q, C ↔ R.</p>"
        "<p>Criteria: <b>SAS</b> (two sides and the included angle), <b>ASA</b>, <b>AAS</b>, <b>SSS</b> and <b>RHS</b> (right angle, hypotenuse, one side). AAA and SSA do not prove congruence.</p>"
        "<p>Corresponding parts of congruent triangles are equal (<b>CPCT</b>). In an isosceles triangle the angles opposite the equal sides are equal.</p>",
        [("AB = PQ, ∠B = ∠Q, BC = QR. Are △ABC and △PQR congruent?", ["Two sides and the included angle"], "Yes, by SAS"),
         ("In △ABC, AB = AC and ∠B = 50°. Find ∠A.", ["∠C = 50°", "180° − 100°"], "80°")],
        ["Using SAS when the angle is not between the two sides (SSA).",
         "Thinking three equal angles (AAA) prove congruence. They only give the same shape.",
         "Matching the vertices out of order when writing △ABC ≅ △PQR."])
    faq = [
        ("What are the criteria for congruence of triangles?", "SAS, ASA, AAS, SSS and RHS (for right triangles: right angle, hypotenuse and one side)."),
        ("What does CPCT mean?", "Corresponding Parts of Congruent Triangles are equal. Once two triangles are proved congruent, their matching sides and angles are equal."),
        ("Why is SSA not a congruence criterion?", "Two sides and an angle that is not between them can make two different triangles, so they do not fix the triangle."),
        ("What is special about an isosceles triangle?", "The angles opposite its equal sides are equal, and conversely, sides opposite equal angles are equal."),
    ]
    make(9, "triangles", 7, "IV", 7, "Triangles: Congruence of Triangles", "triangles",
         "Congruence of triangles: SAS (motivate after illustrating), ASA, SSS and RHS congruence; the angles opposite equal sides of a triangle are equal, and the sides opposite equal angles are equal (summary of the CBSE syllabus)",
         "Class 9 Triangles worksheet (NCERT Chapter 7): congruence criteria SAS, ASA, AAS, SSS and RHS, CPCT, isosceles triangle properties and algebra. 100 questions with answers.",
         "SAS, ASA, AAS, SSS, RHS", "AAA and SSA do not prove congruence. Then use CPCT.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
