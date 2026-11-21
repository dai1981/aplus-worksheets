# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 6: Triangles (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c10_triangles.py
Basic Proportionality Theorem (Thales theorem) and its converse with a figure, criteria for similarity (AA, SSS, SAS),
triangles cut by a line parallel to a side, scale factors and missing sides (US Geometry, AU Year 8 and SG Secondary 3
makers with Indian wording), and problems (shadows, lamp posts, perimeters).
Wrong answers come from real mistakes: AD/AB = AE/EC (mixing part and whole), adding the difference instead of
multiplying, matching the wrong pairs of sides, and thinking SSA proves similarity.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, QN, fv, People, adopt, svg_wrap, text, INK, RED, BLUE, FILL
import gen_sg_maths_s3_congruent_and_similar_triangles as sgc

R = random.Random(910006)
P = People(R)
adopt(sgc, R)
adopt(sgc.us, R)
adopt(sgc.au, R)

FIX = [("m∠", "∠"), ("Triangle Proportionality Theorem", "Basic Proportionality Theorem"), ("pairs of congruent angles", "pairs of equal angles"),
       ("Two pairs of congruent angles", "Two pairs of equal angles"), ("included angles are congruent", "included angles are equal"), ("congruent angles", "equal angles")]


def indian(fn):
    def f(r):
        it = fn(r)
        if not it:
            return None
        for k in ("q", "e"):
            for a, b in FIX:
                it[k] = it[k].replace(a, b)
        it["c"] = [c.replace("m∠", "∠") for c in it["c"]]
        return it
    f.__name__ = getattr(fn, "__name__", "f")
    return f


def bpt_svg(lab):
    """△ABC with DE ∥ BC; lab: dict of segment labels AD, DB, AE, EC, DE, BC"""
    A, B, C = (150, 22), (30, 210), (290, 210)
    t = 0.45
    D = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
    E = (A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t)
    s = ["<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2.6'/>" % (A + B + C + (FILL, INK)),
         "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6'/>" % (D + E + (RED,))]
    for p, n, dx, dy in ((A, "A", 0, -6), (B, "B", -12, 18), (C, "C", 12, 18), (D, "D", -14, 4), (E, "E", 14, 4)):
        s.append(text(p[0] + dx, p[1] + dy + (0 if n != "A" else 0), n, 17))
    mid = lambda P1, P2: ((P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2)
    pos = {"AD": (mid(A, D), -30, 0), "DB": (mid(D, B), -30, 0), "AE": (mid(A, E), 30, 0), "EC": (mid(E, C), 30, 0),
           "DE": (mid(D, E), 0, -8), "BC": (mid(B, C), 0, 24)}
    for k, v in lab.items():
        (x, y), dx, dy = pos[k]
        s.append(text(x + dx, y + dy + 5, v, 16, col=BLUE))
    return svg_wrap(320, 240, "".join(s), "triangle ABC with DE parallel to BC")


# ---------------------------------------------------------------- set 1: Basic Proportionality Theorem
def one_bpt(r):
    kind = r.choice(["ec", "ec", "x", "conv", "ab"])
    ad, db = r.randint(2, 9), r.randint(2, 9)
    k = F(r.choice([1, 2, 3, 3, 4, 5]), r.choice([1, 2]))
    ae = ad * k
    ec = db * k
    if ae.denominator != 1 or ec.denominator != 1 or ad == db:
        return None
    if kind == "ec":
        pic = bpt_svg({"AD": "%s cm" % num(ad), "DB": "%s cm" % num(db), "AE": "%s cm" % num(ae), "EC": "?"})
        return QN(pic + "In △ABC, DE ∥ BC. AD = %s cm, DB = %s cm and AE = %s cm. Find EC." % (num(ad), num(db), num(ae)), ec,
                  [F(ad * db, ae), ae + db - ad, F(ae * (ad + db), ad)],
                  "Basic Proportionality Theorem: AD/DB = AE/EC, so %s/%s = %s/EC and EC = <b>%s cm</b>." % (num(ad), num(db), num(ae), num(ec)), unit=" cm")
    if kind == "ab":
        pic = bpt_svg({"AD": "%s cm" % num(ad), "DB": "%s cm" % num(db), "DE": "%s cm" % num(ae), "BC": "?"})
        bc = F(ae * (ad + db), ad)
        if bc.denominator != 1:
            return None
        return QN(pic + "In △ABC, DE ∥ BC. AD = %s cm, DB = %s cm and DE = %s cm. Find BC." % (num(ad), num(db), num(ae)), bc,
                  [F(ae * db, ad), ae + db, F(ae * ad, ad + db)],
                  "△ADE ~ △ABC, so DE/BC = AD/AB = %s/%s. BC = %s × %s ÷ %s = <b>%s cm</b>." % (num(ad), num(ad + db), num(ae), num(ad + db), num(ad), num(bc)), unit=" cm")
    if kind == "x":
        # AD = x, DB = x − p, AE = x + q, EC = x − t: x(x − t) = (x − p)(x + q) gives x = pq/(q + t − p)
        p, q, t = r.randint(1, 4), r.randint(1, 5), r.randint(1, 4)
        if q + t - p <= 0 or (p * q) % (q + t - p):
            return None
        x = p * q // (q + t - p)
        if x <= max(p, t) + 1:
            return None
        ad_s, db_s, ae_s, ec_s = "x", "x − %d" % p, "x + %d" % q, "x − %d" % t
        return T("In △ABC, DE ∥ BC with AD = %s cm, DB = (%s) cm, AE = (%s) cm and EC = (%s) cm. Find x." % (ad_s, db_s, ae_s, ec_s), "x = %d" % x,
                 ["x = %d" % (x + 1), "x = %d" % (x - 1), "x = %d" % (x + p)],
                 "AD/DB = AE/EC: x(x − %d) = (x − %d)(x + %d). The x² terms cancel: %dx = %d, so <b>x = %d</b>." % (t, p, q, q + t - p, p * q, x))
    par = r.random() < 0.5
    ae2 = ae if par else ae + r.choice([1, 2])
    ec2 = ec
    return T("D and E are points on AB and AC of △ABC with AD = %s cm, DB = %s cm, AE = %s cm and EC = %s cm. Is DE ∥ BC?" % (num(ad), num(db), num(ae2), num(ec2)),
             "Yes, because AD/DB = AE/EC" if par else "No, because AD/DB ≠ AE/EC",
             ["No, because AD/DB ≠ AE/EC" if par else "Yes, because AD/DB = AE/EC", "Yes, because AD + DB = AE + EC" if par else "Yes, because D and E are on the sides", "It cannot be decided without angles"],
             "Converse of the BPT: AD/DB = %s and AE/EC = %s. %s" % (fv(F(ad, db)), fv(F(ae2, ec2)), "<b>They are equal, so DE ∥ BC.</b>" if par else "<b>They are not equal, so DE is not parallel to BC.</b>"))


# ---------------------------------------------------------------- set 5: problems (own)
def one_lamp(r):
    kind = r.choice(["lamp", "pole"])
    name, he, his = P.next()
    if kind == "lamp":
        L = r.choice([F(18, 5), 4, F(9, 2), 5, 6])
        h = r.choice([F(6, 5), F(3, 2), F(8, 5)])
        sp = r.choice([F(6, 5), F(3, 2), 2])
        t = r.choice([2, 3, 4])
        d = sp * t
        sh = h * d / (L - h)
        if (sh * 100).denominator != 1:
            return None
        return QN("A girl %s m tall walks away from the base of a lamp post at %s m/s. The lamp is %s m above the ground. Find the length of her shadow after %d seconds." % (num(h), num(sp), num(L), t),
                  sh, [h * d / L, d * L / h, d - h], "Distance walked = %s m. Similar triangles: shadow/(%s + shadow) = %s/%s, so shadow = <b>%s m</b>." % (num(d), num(d), num(h), num(L), num(sh)), unit=" m")
    p = r.choice([6, 8, 10, 12])
    s1 = r.choice([4, 5, 6, 8])
    s2 = r.choice([20, 24, 28, 30, 36])
    H = F(p * s2, s1)
    if H.denominator != 1:
        return None
    return QN("A vertical pole %d m long casts a shadow %d m long. At the same time a tower casts a shadow %d m long. Find the height of the tower." % (p, s1, s2), H,
              [F(s1 * s2, p), s2 + p - s1, F(p * s1, s2)], "Pole/shadow = tower/shadow: %d/%d = h/%d, so h = <b>%s m</b>." % (p, s1, s2, num(H)), unit=" m")


def main():
    seen = set()
    sets = [
        S("Basic Proportionality Theorem", mix(R, [(one_bpt, 20)], seen)),
        S("Criteria for similarity", mix(R, [(indian(sgc.us.one_crit), 20)], seen)),
        S("Triangles with a parallel line", mix(R, [(indian(sgc.us.one_nest), 20)], seen)),
        S("Scale factors and missing sides", mix(R, [(indian(sgc.au.one_sf), 10), (indian(sgc.au.one_tri), 10)], seen)),
        S("Problems", mix(R, [(indian(sgc.one_prob), 12), (one_lamp, 8)], seen)),
    ]
    body = lesson(
        "<p>Two triangles are <b>similar</b> if their corresponding angles are equal and their corresponding sides are in the same ratio.</p>"
        "<p><b>Basic Proportionality Theorem</b> (Thales theorem): a line parallel to one side of a triangle divides the other two sides in the same ratio. If DE ∥ BC, then AD/DB = AE/EC. The converse is also true.</p>"
        "<p>Criteria: <b>AA</b> (two pairs of equal angles), <b>SSS</b> (all sides in the same ratio), <b>SAS</b> (two sides in the same ratio and the included angles equal).</p>",
        [("In △ABC, DE ∥ BC, AD = 3 cm, DB = 6 cm, AE = 4 cm. Find EC.", ["AD/DB = AE/EC", "3/6 = 4/EC"], "EC = 8 cm"),
         ("A 6 m pole casts a 4 m shadow. A tower casts a 28 m shadow at the same time. How tall is the tower?", ["6/4 = h/28"], "42 m")],
        ["Mixing a part and a whole: AD/AB = AE/EC is wrong. Use AD/DB = AE/EC or AD/AB = AE/AC.",
         "Adding the difference instead of multiplying by the scale factor.",
         "Matching sides in the wrong order. Use the order of the letters in △ABC ~ △PQR."])
    faq = [
        ("What is the Basic Proportionality Theorem?", "If a line is drawn parallel to one side of a triangle to meet the other two sides at distinct points, it divides those two sides in the same ratio. It is also called Thales theorem."),
        ("What are the criteria for similarity of triangles?", "AA (or AAA): two pairs of equal angles. SSS: the three pairs of sides are in the same ratio. SAS: two pairs of sides in the same ratio with the included angles equal."),
        ("What is the difference between similar and congruent triangles?", "Congruent triangles have the same shape and size. Similar triangles have the same shape but may differ in size."),
        ("How are shadows used with similar triangles?", "At the same time of day, an object and its shadow form triangles similar to those of another object, so height ÷ shadow length is the same for both."),
    ]
    make(10, "triangles", 6, "IV", 6, "Triangles: Similarity and the Basic Proportionality Theorem", "triangles",
         "Definitions, examples, counter examples of similar triangles; the Basic Proportionality Theorem and its converse; criteria for similarity of triangles (AA, SSS, SAS) (summary of the CBSE syllabus)",
         "Class 10 Triangles worksheet (NCERT Chapter 6): Basic Proportionality Theorem, similarity criteria, parallel lines in triangles, scale factors and shadow problems. 100 questions with answers.",
         "DE ∥ BC ⇒ AD/DB = AE/EC", "Basic Proportionality Theorem (Thales theorem).",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
