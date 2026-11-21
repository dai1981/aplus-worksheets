# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 1: Geometric Twins
  python3 tools/gen_in_maths_c7_geometric_twins.py
Congruent figures (same shape and size), congruence of triangles by SSS, SAS, ASA and RHS, matching corresponding
vertices, sides and angles, and what extra information is needed. Reuses the US Geometry makers through the Class 9
wrapper (RHS for HL, CPCT for CPCTC).
Wrong answers come from real mistakes: AAA or SSA taken as a congruence condition, and corresponding parts matched in the
wrong order.
"""
import random
from in_common import unit, T, adopt
import gen_in_maths_c9_triangles as c9

R = random.Random(907009)
adopt(c9.us, R)

FACTS = [("Two figures are congruent if they have the same", "shape and size", ["shape only", "size only", "colour"]),
         ("Two line segments are congruent if they have the same", "length", ["direction", "position", "endpoints"]),
         ("Two angles are congruent if they have the same", "measure", ["arm lengths", "vertex", "position"]),
         ("Two circles are congruent if they have the same", "radius", ["centre", "colour", "position"]),
         ("Which condition does NOT prove two triangles congruent?", "AAA", ["SSS", "SAS", "RHS"]),
         ("Which condition does NOT prove two triangles congruent?", "SSA", ["ASA", "SAS", "SSS"]),
         ("In RHS congruence, the H stands for the", "hypotenuse", ["height", "half-side", "horizontal side"]),
         ("If △ABC ≅ △PQR, which side corresponds to BC?", "QR", ["PQ", "PR", "RQ is not a side"]),
         ("If △ABC ≅ △PQR, which angle is equal to ∠C?", "∠R", ["∠P", "∠Q", "∠A"]),
         ("If △XYZ ≅ △LMN, which side is equal to XZ?", "LN", ["LM", "MN", "XY"]),
         ("Two triangles have all three angles equal. Are they always congruent?", "No, they may be different sizes", ["Yes, always", "Only if they are right-angled", "Only if they are isosceles"]),
         ("Two squares are congruent when their ___ are equal.", "sides", ["diagonals' directions", "positions", "colours"])]


def one_fact(r):
    q, a, w = r.choice(FACTS)
    return T(q if q.endswith("?") or "___" in q else q + " ___.", a, w, "<b>%s</b>." % a)


def main():
    unit(7, 2, 1, "geometric-twins", 9, "G", "Geometric Twins: Congruent Figures and Triangles", "geometric twins",
         "Congruent figures; congruence of triangles by SSS, SAS, ASA and RHS; corresponding parts of congruent triangles (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Geometric Twins worksheet (Ganita Prakash Part 2, Chapter 1): congruent figures, SSS, SAS, ASA and RHS congruence and corresponding parts. 100 questions with answers.",
         "SSS, SAS, ASA and RHS prove two triangles congruent", "AAA and SSA do not.",
         "<p>Congruent figures — ‘geometric twins’ — have the same <b>shape and size</b>; one fits exactly on the other.</p>"
         "<p>Two triangles are congruent if they match by <b>SSS</b> (three sides), <b>SAS</b> (two sides and the angle between them), <b>ASA</b> (two angles and the side between) or <b>RHS</b> (right angle, hypotenuse, side).</p>"
         "<p>Write the vertices in matching order: △ABC ≅ △PQR means A ↔ P, B ↔ Q, C ↔ R, so AB = PQ and ∠C = ∠R.</p>",
         [("AB = PQ, BC = QR, CA = RP. Are △ABC and △PQR congruent?", ["Three pairs of equal sides"], "Yes, by SSS"),
          ("△LMN ≅ △XYZ. Which side equals MN?", ["M ↔ Y, N ↔ Z"], "YZ")],
         ["Thinking three equal angles (AAA) make triangles congruent.", "Using SAS when the angle is not between the two sides.", "Matching the vertices in the wrong order."],
         [("What does congruent mean?", "Having exactly the same shape and size."),
          ("What are the congruence conditions for triangles?", "SSS, SAS, ASA and RHS."),
          ("Why is AAA not a congruence condition?", "Triangles with the same angles can be different sizes (an enlargement), so they are similar but not congruent.")],
         [("Congruent figures", [(one_fact, 10), (c9.ind(c9.us.one_crit), 10)]),
          ("Which condition?", [(c9.ind(c9.us.one_crit), 20)]),
          ("Corresponding parts", [(c9.ind(c9.us.one_corr), 20)]),
          ("What else is needed?", [(c9.ind(c9.us.one_need), 20)]),
          ("Using congruence", [(c9.ind(c9.us.one_cpctc), 20)])], R)


if __name__ == "__main__":
    main()
