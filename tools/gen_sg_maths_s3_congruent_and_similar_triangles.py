# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Congruent and Similar Triangles (MOE syllabus G2: determining whether two triangles are
congruent or similar)
  python3 tools/gen_sg_maths_s3_congruent_and_similar_triangles.py
Congruence tests (SSS, SAS, AAS, RHS), similarity tests (AA, SSS, SAS), triangles with a pair of parallel
lines, scale factors and missing sides, and problems. Sets 2 to 4 reuse the US Geometry and AU Year 8 makers
with Singapore wording.
Wrong answers come from real mistakes: thinking AAA or SSA proves congruence, matching the wrong pairs of
sides, using the part DB instead of the whole side AB, and adding the difference instead of multiplying.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, QN, fr, MINUS, People, adopt
import gen_us_math_ge_similar_triangles as us
import gen_au_maths_y8_congruent_and_similar_triangles as au

R = random.Random(831000)
adopt(us, R)
adopt(au, R)
P = People(R)

SG_FIX = [("m∠", "∠"), ("pairs of congruent angles", "pairs of equal angles"), ("Two pairs of congruent angles", "Two pairs of equal angles"),
          ("included angles are congruent", "included angles are equal"), ("Triangle Proportionality Theorem: ", ""), ("(corresponding angles)", "(corresponding angles are equal)")]


def sgw(it):
    for k in ("q", "e"):
        for a, b in SG_FIX:
            it[k] = it[k].replace(a, b)
    it["c"] = [c for c in it["c"]]
    return it


def wrap(fn):
    def f(r):
        it = fn(r)
        return sgw(it) if it else None
    return f


TESTS = ["SSS", "SAS", "AAS", "RHS"]


# ------------------------------------------------------------ set 1: congruence tests
def one_cong(r):
    kind = r.choice(["SSS", "SAS", "AAS", "AAS", "RHS", "AAA", "SSA"])
    if kind == "SSS":
        a, b, c = sorted(r.sample(range(4, 16), 3))
        if a + b <= c:
            return None
        o = [b, c, a]
        r.shuffle(o)
        q = "△ABC has sides %d cm, %d cm and %d cm. △PQR has sides %d cm, %d cm and %d cm. Are the triangles congruent?" % (a, b, c, o[0], o[1], o[2])
        right = "Yes, by SSS"
        e = "The same three lengths appear in both triangles, so they are congruent by <b>SSS</b>."
    elif kind == "SAS":
        a, b = r.sample(range(4, 15), 2)
        ang = r.randint(30, 120)
        q = "In △ABC, AB = %d cm, AC = %d cm and ∠BAC = %d°. In △PQR, PQ = %d cm, PR = %d cm and ∠QPR = %d°. Are the triangles congruent?" % (a, b, ang, a, b, ang)
        right = "Yes, by SAS"
        e = "Two pairs of equal sides and the angle <b>between</b> them is equal: <b>SAS</b>."
    elif kind == "AAS":
        x, y = r.randint(30, 80), r.randint(30, 80)
        s = r.randint(4, 15)
        z = 180 - x - y
        if z < 20:
            return None
        q = "In △ABC, ∠A = %d°, ∠B = %d° and BC = %d cm. In △PQR, ∠P = %d°, ∠R = %d° and QR = %d cm. Are the triangles congruent?" % (x, y, s, x, z, s)
        right = "Yes, by AAS"
        e = "∠Q = 180° − %d° − %d° = %d°, so both triangles have angles %d°, %d° and %d°, and BC and QR are both opposite the %d° angle. <b>AAS</b>." % (x, z, y, x, y, z, x)
    elif kind == "RHS":
        a, c = r.choice([(3, 5), (5, 13), (6, 10), (8, 17), (7, 25), (9, 15), (12, 13)])
        q = "△ABC and △PQR both have a right angle. Both hypotenuses are %d cm and both have another side of %d cm. Are the triangles congruent?" % (c, a)
        right = "Yes, by RHS"
        e = "Right angle, equal Hypotenuses and one other equal Side: <b>RHS</b>."
    elif kind == "AAA":
        x, y = r.randint(35, 80), r.randint(35, 80)
        if 180 - x - y < 20:
            return None
        q = "Both △ABC and △PQR have angles %d°, %d° and %d°. Are they congruent?" % (x, y, 180 - x - y)
        right = "Not necessarily: they are similar, but could be different sizes"
        return T(q, right, ["Yes, by AAS", "Yes, by AAA", "Yes, by SAS"], "Equal angles only show the triangles have the same shape: <b>similar, not necessarily congruent</b>.")
    else:
        a, b = r.sample(range(5, 14), 2)
        ang = r.randint(25, 60)
        q = "In △ABC, AB = %d cm, BC = %d cm and ∠A = %d°. In △PQR, PQ = %d cm, QR = %d cm and ∠P = %d°. The angle is not between the two sides. Are the triangles definitely congruent?" % (a, b, ang, a, b, ang)
        right = "Not necessarily: the angle is not between the two sides"
        return T(q, right, ["Yes, by SAS", "Yes, by SSS", "Yes, by RHS"], "SAS needs the <b>included</b> angle. Two sides and a non-included angle can give two different triangles, so <b>not necessarily</b>.")
    return T(q, right, ["Yes, by %s" % t for t in TESTS if "Yes, by %s" % t != right][:2] + ["No"], e)


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["shadow", "shadow", "perim", "cong_ang", "cong_side", "ratio"])
    nm, he, his = P.next()
    if kind == "shadow":
        h = r.choice([F(3, 2), F(8, 5), F(17, 10), F(9, 5)])
        sh = r.choice([2, F(5, 2), 3, F(12, 5)])
        big = r.choice([10, 12, 15, 18, 20, 24])
        H = h * big / sh
        if (H * 100).denominator != 1:
            return None
        q = "%s is %s m tall and casts a shadow %s m long. At the same time, a tree casts a shadow %s m long. How tall is the tree?" % (nm, num(h), num(sh), num(big))
        return QN(q, H, [h * big, big - sh + h, sh * big / h], "The sun's rays make similar triangles, so height ÷ shadow is the same: %s ÷ %s = <i>h</i> ÷ %s, <i>h</i> = <b>%s m</b>." % (num(h), num(sh), num(big), num(H)), unit=" m")
    if kind == "perim":
        p = r.randint(12, 40)
        a, b = r.sample(range(3, 12), 2)
        k = F(b, a)
        P2 = p * k
        if P2.denominator != 1:
            return None
        q = "Two triangles are similar. A side of %d cm in the smaller triangle matches a side of %d cm in the larger one. The smaller triangle has a perimeter of %d cm. Find the perimeter of the larger triangle." % (a, b, p)
        return QN(q, P2, [p + b - a, p * k * k if (p * k * k).denominator == 1 else p * b, F(p * a, b) if F(p * a, b).denominator == 1 else p * a], "Lengths scale by %s ÷ %s = %s, and perimeter is a length: %s × %s = <b>%s cm</b>." % (num(b), num(a), num(k), num(p), num(k), num(P2)), unit=" cm")
    if kind == "cong_ang":
        x, y = r.randint(30, 80), r.randint(30, 80)
        z = 180 - x - y
        if z < 20:
            return None
        q = "△ABC ≡ △PQR. ∠A = %d° and ∠B = %d°. Find ∠R." % (x, y)
        return QN(q, z, [x, y, 180 - x], "The letters match in order: ∠R matches ∠C. ∠C = 180° − %d° − %d° = %d°, so <b>∠R = %d°</b>." % (x, y, z, z), unit="°")
    if kind == "cong_side":
        a, b, c = r.sample(range(4, 16), 3)
        pairs = [("AB", "PQ", a), ("BC", "QR", b), ("AC", "PR", c)]
        x = r.choice(pairs)
        q = "△ABC ≡ △PQR with AB = %d cm, BC = %d cm and AC = %d cm. What is the length of %s?" % (a, b, c, x[1])
        others = [p[2] for p in pairs if p != x]
        return QN(q, x[2], others + [a + b + c - x[2]], "In △ABC ≡ △PQR the order of the letters matches, so %s corresponds to %s: <b>%d cm</b>." % (x[1], x[0], x[2]), unit=" cm")
    a, b = r.sample(range(2, 9), 2)
    s = r.randint(2, 6)
    q = "In △ABC, DE is parallel to BC, with D on AB and E on AC. AD = %d cm, DB = %d cm and DE = %d cm. Find BC." % (a, b, s)
    BC = F(s * (a + b), a)
    return QN(q, BC, [F(s * b, a), s + b, F(s * a, a + b)], "△ADE and △ABC are similar (equal corresponding angles). AB = %d + %d = %d. BC ÷ DE = AB ÷ AD, so BC = %d × %d ÷ %d = <b>%s cm</b>." % (a, b, a + b, s, a + b, a, num(BC)), unit=" cm")


def build():
    sets = [S("Congruence tests", collect(one_cong, 20, R)),
            S("Similarity tests", collect(wrap(us.one_crit), 20, R)),
            S("Triangles with parallel lines", collect(wrap(us.one_nest), 20, R)),
            S("Scale factors and missing sides", collect(wrap(au.one_sf), 10, R) + collect(wrap(au.one_tri), 10, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<p><b>Congruent</b> triangles are exactly the same shape and size. Tests: <b>SSS</b>, <b>SAS</b> (the angle must be between the sides), "
        "<b>AAS</b> and <b>RHS</b> (right angle, hypotenuse, side). AAA does not prove congruence.</p>"
        "<p><b>Similar</b> triangles are the same shape: corresponding angles are equal and corresponding sides are in the same ratio. Tests: "
        "<b>AA</b> (two pairs of equal angles), <b>SSS</b> (all three ratios equal) and <b>SAS</b> (two ratios equal and the included angle equal).</p>"
        "<p>Write the letters in matching order: in △ABC ≡ △PQR, A matches P, B matches Q and C matches R.</p>",
        [("In △ABC, DE ∥ BC, AD = 4 cm, DB = 2 cm and DE = 6 cm. Find BC.", ["△ADE and △ABC are similar (AA)", "AB = 6 cm, so the scale factor is 6 ÷ 4 = 1.5"], "BC = 9 cm"),
         ("△ABC has sides 6, 8, 10. △PQR has sides 9, 12, 15. Are they similar?", ["9 ÷ 6 = 12 ÷ 8 = 15 ÷ 10 = 1.5"], "Yes, by SSS similarity")],
        ["Thinking three equal angles (AAA) prove two triangles are congruent.",
         "Using SAS when the angle is not between the two sides.",
         "Matching the wrong sides. Match shortest to shortest and longest to longest.",
         "Using DB instead of the whole side AB when DE ∥ BC."])
    faq = [("What are the tests for congruent triangles?", "SSS (three sides), SAS (two sides and the included angle), AAS (two angles and a corresponding side) and RHS (right angle, hypotenuse and one other side)."),
           ("What are the tests for similar triangles?", "AA (two pairs of equal angles), SSS (all three pairs of sides in the same ratio) and SAS (two pairs of sides in the same ratio with the included angles equal)."),
           ("What is the difference between congruent and similar?", "Congruent triangles are the same shape and the same size. Similar triangles are the same shape but can be different sizes."),
           ("Why does the order of letters matter?", "△ABC ≡ △PQR tells you A matches P, B matches Q and C matches R, so you can find corresponding sides and angles.")]
    make(3, "congruent-and-similar-triangles", 10, "G2",
         "Congruent and Similar Triangles: Tests and Problems",
         "", "Congruent and similar triangles", "",
         "Free Secondary 3 maths worksheets on congruent and similar triangles: SSS, SAS, AAS and RHS congruence tests, AA, SSS and SAS similarity tests, parallel lines, scale factors and problems. 100 questions with answers.",
         "Congruent: same shape and size (SSS, SAS, AAS, RHS). Similar: same shape (AA, SSS, SAS).",
         "Match the letters in order to find corresponding sides and angles.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
