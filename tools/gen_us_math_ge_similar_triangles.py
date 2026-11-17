# -*- coding: utf-8 -*-
"""
US Geometry: Similar Triangles (Common Core G-SRT.B.5, G-SRT.A.3, G-SRT.B.4)
  python3 tools/gen_us_math_ge_similar_triangles.py
AA, SSS and SAS similarity, finding sides in nested similar triangles, the Triangle Proportionality
Theorem, the geometric mean in right triangles, and indirect measurement.
Wrong answers come from real mistakes: using the part of a side instead of the whole side in nested
triangles, adding instead of multiplying, matching the wrong pairs of sides, and using the whole hypotenuse
instead of a segment.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, RED, GREEN, BLUE

R = random.Random(93401)


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def nest_fig(lab, t=0.45):
    """triangle ABC with D on AB, E on AC and DE parallel to BC. lab keys: AD, DB, AE, EC, DE, BC"""
    A, Bp, C = (150, 15), (20, 200), (300, 200)
    t = max(0.38, min(0.62, t))
    D = (A[0] + (Bp[0] - A[0]) * t, A[1] + (Bp[1] - A[1]) * t)
    E = (A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t)
    c = Canvas()
    c.poly([A, Bp, C])
    c.seg(D, E)
    c.chevrons(D, E)
    c.chevrons(Bp, C)
    c.vlabels([A, Bp, C], "ABC")
    c.text((D[0] - 14, D[1]), "D", 15)
    c.text((E[0] + 14, E[1]), "E", 15)
    cen = (150, 140)
    for k, (p, q) in {"AD": (A, D), "DB": (D, Bp), "AE": (A, E), "EC": (E, C)}.items():
        if lab.get(k):
            c.side_label(p, q, lab[k], cen, 26 if len(lab[k]) > 3 else 18, 13)
    if lab.get("DE"):
        c.text(((D[0] + E[0]) / 2, D[1] + 16), lab["DE"], 13)
    if lab.get("BC"):
        c.text((160, 220), lab["BC"], 13)
    return c.svg("triangle ABC with segment DE parallel to BC, not drawn to scale")


def alt_fig(lab, t=0.32):
    """right triangle ABC (right angle at C) with altitude CD to the hypotenuse AB"""
    A, Bp = (20, 170), (300, 170)
    t = max(0.22, min(0.78, t))
    D = (A[0] + (Bp[0] - A[0]) * t, 170)
    h = math.sqrt((D[0] - A[0]) * (Bp[0] - D[0]))
    C = (D[0], 170 - h)
    c = Canvas()
    c.poly([A, Bp, C])
    c.seg(C, D, col=BLUE)
    c.right(D, Bp, C)
    c.right(C, A, Bp)
    c.vlabels([A, Bp, C], "ABC")
    c.text((D[0], 190), "D", 15)
    if lab.get("AD"):
        c.text(((A[0] + D[0]) / 2, 156), lab["AD"], 13)
    if lab.get("DB"):
        c.text(((D[0] + Bp[0]) / 2, 156), lab["DB"], 13)
    if lab.get("CD"):
        c.text((D[0] + 16, (C[1] + D[1]) / 2), lab["CD"], 13, BLUE, anchor="start")
    if lab.get("AC"):
        c.side_label(A, C, lab["AC"], (150, 170), 16, 13)
    if lab.get("BC"):
        c.side_label(C, Bp, lab["BC"], (150, 170), 16, 13)
    return c.svg("right triangle ABC with altitude CD to the hypotenuse, not drawn to scale")


# ------------------------------------------------------------ set 1: are they similar?
def one_crit(r):
    kind = r.choice(["AA", "AA", "SSS", "SAS", "no_sss", "no_aa", "no_sas"])
    if kind in ("AA", "no_aa"):
        a, b = r.randint(30, 80), r.randint(30, 80)
        c_ = 180 - a - b
        if c_ < 15:
            return None
        if kind == "AA":
            q = "△ABC has angles of %d° and %d°. △DEF has angles of %d° and %d°. Are the triangles similar?" % (a, b, b, c_)
            right = "Yes, by AA similarity"
            e = "The third angle of △ABC is %d°, so both triangles have angles %d°, %d° and %d°. Two pairs of congruent angles: <b>%s</b>." % (c_, a, b, c_, right)
        else:
            d = r.choice([-6, -4, 4, 6])
            q = "△ABC has angles of %d° and %d°. △DEF has angles of %d° and %d°. Are the triangles similar?" % (a, b, a, b + d)
            right = "No"
            e = "Only one pair of angles matches (%d°). The other angles of △DEF are %d° and %d°, not %d° and %d°. <b>No</b>." % (a, b + d, 180 - a - b - d, b, c_)
        return T(q, right, [x for x in ["Yes, by AA similarity", "Yes, by SSS similarity", "Yes, by SAS similarity", "No"] if x != right][:3], e)
    s = sorted(r.sample(range(3, 15), 3))
    if s[0] + s[1] <= s[2]:
        return None
    k = F(r.choice([2, 3, F(3, 2), F(5, 2), F(1, 2)]))
    if any((k * x).denominator > 1 for x in s):
        return None
    t = [k * x for x in s]
    if kind == "SSS":
        q = "△ABC has sides %d, %d and %d. △DEF has sides %s, %s and %s. Are the triangles similar?" % (s[0], s[1], s[2], num(t[0]), num(t[1]), num(t[2]))
        right = "Yes, by SSS similarity"
        e = "Shortest to shortest, middle to middle, longest to longest: every ratio is %s. <b>%s</b>." % (num(k), right)
    elif kind == "no_sss":
        t[2] += 1
        q = "△ABC has sides %d, %d and %d. △DEF has sides %s, %s and %s. Are the triangles similar?" % (s[0], s[1], s[2], num(t[0]), num(t[1]), num(t[2]))
        right = "No"
        e = "%s ÷ %d = %s, but %s ÷ %d = %s. The ratios are not all equal. <b>No</b>." % (num(t[0]), s[0], num(k), num(t[2]), s[2], num(F(t[2]) / s[2]) or "%s/%d" % (num(t[2]), s[2]))
    else:
        ang = r.randint(35, 110)
        if kind == "SAS":
            q = ("In △ABC, AB = %d, AC = %d and m∠A = %d°. In △DEF, DE = %s, DF = %s and m∠D = %d°. Are the triangles similar?" % (s[0], s[1], ang, num(t[0]), num(t[1]), ang))
            right = "Yes, by SAS similarity"
            e = "AB : DE and AC : DF are both 1 : %s, and the included angles are congruent. <b>%s</b>." % (num(k), right)
        else:
            q = ("In △ABC, AB = %d, AC = %d and m∠A = %d°. In △DEF, DE = %s, DF = %s and m∠D = %d°. Are the triangles similar?" % (s[0], s[1], ang, num(t[0]), num(t[1] + 2), ang))
            right = "No"
            e = "The angles match, but %s ÷ %d ≠ %s ÷ %d, so the sides are not proportional. <b>No</b>." % (num(t[0]), s[0], num(t[1] + 2), s[1])
    return T(q, right, [x for x in ["Yes, by AA similarity", "Yes, by SSS similarity", "Yes, by SAS similarity", "No"] if x != right][:3], e)


# ------------------------------------------------------------ set 2: nested triangles
def one_nest(r):
    ad, db = r.randint(2, 12), r.randint(2, 12)
    ab = ad + db
    de = r.randint(2, 10) * ad // math.gcd(ad, ab) if False else None
    k = F(ab, ad)
    de = r.randint(2, 12)
    bc = k * de
    if bc.denominator > 1:
        de = ad * r.randint(1, 3)
        bc = k * de
    kind = r.choice(["BC", "BC", "DE", "DB"])
    if kind == "BC":
        q = "<span class='ov'>DE</span> ∥ <span class='ov'>BC</span>. Find BC.%s" % fig(nest_fig({"AD": num(ad), "DB": num(db), "DE": num(de), "BC": "?"}, ad / ab))
        e = "△ADE ~ △ABC by AA (corresponding angles). AB = %d + %d = %d. BC : DE = AB : AD, so BC = %d × %d ÷ %d = <b>%s</b>." % (ad, db, ab, de, ab, ad, num(bc))
        wr = [F(de * db, ad), de + db, F(de * ad, ab)]
        return T(q, num(bc), [num(w) for w in dict.fromkeys(wr) if w != bc and num(w)][:3] + ([num(bc + 1)] if len(set(wr)) < 3 else []), e)
    if kind == "DE":
        q = "<span class='ov'>DE</span> ∥ <span class='ov'>BC</span>. Find DE.%s" % fig(nest_fig({"AD": num(ad), "DB": num(db), "DE": "?", "BC": num(bc)}, ad / ab))
        e = "△ADE ~ △ABC. AB = %d. DE : BC = AD : AB, so DE = %s × %d ÷ %d = <b>%s</b>." % (ab, num(bc), ad, ab, num(de))
        wr = [bc * F(ad, db), bc - db, bc * F(db, ab)]
        opts = [num(w) for w in dict.fromkeys(wr) if w != de and w > 0 and num(w)]
        while len(opts) < 3:
            opts.append(num(de + len(opts) + 1))
        return T(q, num(de), opts[:3], e)
    q = "<span class='ov'>DE</span> ∥ <span class='ov'>BC</span>. Find DB.%s" % fig(nest_fig({"AD": num(ad), "DB": "?", "DE": num(de), "BC": num(bc)}, ad / ab))
    e = "AB : AD = BC : DE, so AB = %d × %s ÷ %d = %d. DB = AB %s AD = %d %s %d = <b>%d</b>." % (ad, num(bc), de, ab, MINUS, ab, MINUS, ad, db)
    wr = [ab, F(ad * de, bc) if bc else db + 1, db + 2, ad]
    return T(q, num(db), [num(w) for w in dict.fromkeys(wr) if w != db and num(w)][:3], e)


# ------------------------------------------------------------ set 3: triangle proportionality
def one_prop(r):
    ad, db = r.randint(2, 12), r.randint(2, 12)
    m = r.choice([F(1, 2), 1, F(3, 2), 2, 3])
    ae, ec = m * ad, m * db
    if ae.denominator > 1 or ec.denominator > 1 or ad == db:
        return None
    kind = r.choice(["num", "num", "alg"])
    if kind == "num":
        q = "<span class='ov'>DE</span> ∥ <span class='ov'>BC</span>. Find EC.%s" % fig(nest_fig({"AD": num(ad), "DB": num(db), "AE": num(ae), "EC": "?"}, ad / (ad + db)))
        e = "Triangle Proportionality Theorem: AD/DB = AE/EC. %d/%d = %s/EC, so EC = %s × %d ÷ %d = <b>%s</b>." % (ad, db, num(ae), num(ae), db, ad, num(ec))
        wr = [ae * F(ad, db), ae + db - ad, ae * F(ad + db, ad)]
        opts = [num(w) for w in dict.fromkeys(wr) if w != ec and w > 0 and num(w)]
        while len(opts) < 3:
            opts.append(num(ec + len(opts) + 1))
        return T(q, num(ec), opts[:3], e)
    x = r.randint(2, 9)
    a, b = r.randint(1, 4), r.randint(-3, 6)
    ec2 = a * x + b
    if ec2 < 2:
        return None
    # AD/DB = AE/EC with AE given, EC = ax+b
    ad, db = r.randint(2, 9), r.randint(2, 9)
    if (ad * ec2) % db:
        return None
    ae = ad * ec2 // db
    q = "<span class='ov'>DE</span> ∥ <span class='ov'>BC</span>. AD = %d, DB = %d, AE = %d and EC = %s. Find <i>x</i>.%s" % (
        ad, db, ae, lin(a, b), fig(nest_fig({"AD": num(ad), "DB": num(db), "AE": num(ae), "EC": lin(a, b)}, ad / (ad + db))))
    e = "AD/DB = AE/EC: %d/%d = %d/(%s). Cross-multiply: %d(%s) = %d × %d, so %s = %d and <i>x</i> = <b>%d</b>." % (
        ad, db, ae, lin(a, b), ad, lin(a, b), db, ae, lin(a, b), ec2, x)
    bad = (F(ae * ad, db) - b) / a
    wr = [ec2, int(bad) if bad.denominator == 1 and bad > 0 else x + 2, x + 1, x - 1]
    return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e)


# ------------------------------------------------------------ set 4: geometric mean in right triangles
def one_gm(r):
    p, q_ = r.choice([(4, 9), (2, 8), (3, 12), (4, 16), (1, 9), (9, 16), (5, 20), (2, 18), (3, 27), (4, 25), (8, 18), (6, 24), (1, 4), (4, 36)])
    if r.random() < 0.5:
        p, q_ = q_, p
    kind = r.choice(["h", "h", "leg", "seg"])
    h = math.isqrt(p * q_)
    if kind == "h":
        q = "CD is the altitude to the hypotenuse. AD = %d and DB = %d. Find CD.%s" % (p, q_, fig(alt_fig({"AD": num(p), "DB": num(q_), "CD": "?"}, p / (p + q_))))
        e = "The altitude is the geometric mean of the two segments: CD² = AD × DB = %d × %d = %d, so CD = <b>%d</b>." % (p, q_, p * q_, h)
        wr = [F(p + q_, 2), p * q_, abs(q_ - p)]
        return T(q, num(h), [num(w) for w in dict.fromkeys(wr) if w != h and w > 0][:3], e)
    if kind == "leg":
        c_ = p + q_
        L2 = p * c_
        L = math.isqrt(L2)
        if L * L != L2:
            return None
        q = "CD is the altitude to the hypotenuse. AD = %d and DB = %d. Find AC.%s" % (p, q_, fig(alt_fig({"AD": num(p), "DB": num(q_), "AC": "?"}, p / (p + q_))))
        e = "A leg is the geometric mean of the hypotenuse and the segment next to it: AC² = AD × AB = %d × %d = %d, so AC = <b>%d</b>." % (p, c_, L2, L)
        wr = [h, math.isqrt(q_ * c_) if math.isqrt(q_ * c_) ** 2 == q_ * c_ else L + 2, L2]
        return T(q, num(L), [num(w) for w in dict.fromkeys(wr) if w != L and w > 0][:3], e)
    q = "CD is the altitude to the hypotenuse. CD = %d and AD = %d. Find DB.%s" % (h, p, fig(alt_fig({"AD": num(p), "DB": "?", "CD": num(h)}, p / (p + q_))))
    e = "CD² = AD × DB, so %d = %d × DB and DB = %d ÷ %d = <b>%d</b>." % (h * h, p, h * h, p, q_)
    wr = [h - p if h > p else h + p, h * h, F(h * h, 2)]
    return T(q, num(q_), [num(w) for w in dict.fromkeys(wr) if w != q_ and w > 0][:3], e)


# ------------------------------------------------------------ set 5: indirect measurement
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["shadow", "shadow", "mirror", "pole", "river"])
    if kind == "shadow":
        h = r.choice([F(5), F(6), F(11, 2), F(9, 2), F(5, 1)])
        sh = r.choice([3, 4, 8, 6, 9])
        tsh = r.choice([24, 30, 36, 40, 48, 60])
        H = h * tsh / sh
        if H.denominator > 2:
            return None
        obj = r.choice(["a tree", "a flagpole", "a building", "a light pole"])
        q = "%s is %s ft tall and casts %s %d ft shadow. At the same time, %s casts a %d ft shadow. How tall is %s?" % (nm, num(h), "an" if sh == 8 else "a", sh, obj, tsh, obj.replace("a ", "the "))
        wr = [F(tsh) * sh / h, h + tsh - sh, F(tsh) * h / (sh + 1)]
        return T(q, "%s ft" % num(H), ["%s ft" % num(w) for w in dict.fromkeys(wr) if w != H and num(w)][:3],
                 "The sun's rays make similar triangles: height/shadow is the same. %s/%d = <i>h</i>/%d, so <i>h</i> = %s × %d ÷ %d = <b>%s ft</b>." % (
                     num(h), sh, tsh, num(h), tsh, sh, num(H)))
    if kind == "mirror":
        eye = r.choice([5, F(11, 2), 6])
        d1 = r.choice([2, 3, 4])
        d2 = r.choice([12, 15, 18, 20, 24])
        H = eye * F(d2, d1)
        if num(H) is None or H.denominator > 4:
            return None
        q = ("%s puts a mirror on the ground %d ft from %s and %d ft from a wall. %s eyes are %s ft above the ground, and %s sees the top of a sign on the wall in the mirror. "
             "How high is the top of the sign?" % (nm, d1, "herself" if he == "she" else "himself", d2, his.capitalize(), num(eye), he))
        wr = [F(d2) * d1 / eye, eye + d2 - d1, F(eye) * d2]
        return T(q, "%s ft" % num(H), ["%s ft" % num(w) for w in dict.fromkeys(wr) if w != H and num(w)][:3],
                 "The angles at the mirror are equal, so the triangles are similar: %s/%d = <i>h</i>/%d, <i>h</i> = <b>%s ft</b>." % (num(eye), d1, d2, num(H)))
    if kind == "pole":
        s1, h1 = r.choice([(2, 3), (4, 6), (3, 4), (5, 8)])
        k = r.choice([5, 6, 8, 10])
        q = "A %d ft post casts a %d ft shadow. A nearby tower casts a %d ft shadow. How tall is the tower?" % (h1, s1, s1 * k)
        return T(q, "%d ft" % (h1 * k), ["%s ft" % num(w) for w in dict.fromkeys([F(s1 * k * s1, h1), h1 + s1 * k - s1, s1 * k]) if w != h1 * k and num(w)][:3],
                 "Heights and shadows are proportional: %d/%d = <i>h</i>/%d, so <i>h</i> = <b>%d ft</b>." % (h1, s1, s1 * k, h1 * k))
    a, b, c_ = r.choice([(20, 30, 24), (15, 45, 12), (12, 36, 10), (25, 50, 18), (16, 40, 14)])
    w = F(c_ * b, a)
    q = ("To find the width of a river, surveyors make two similar right triangles. The small triangle has legs %d m and %d m. "
         "The matching legs of the large triangle are %d m and <i>w</i> m. Find <i>w</i>." % (a, c_, b))
    return T(q, "%s m" % num(w), ["%s m" % num(x) for x in dict.fromkeys([F(a * b, c_), c_ + b - a, F(c_ * a, b)]) if x != w and num(x)][:3],
             "Matching legs are proportional: <i>w</i>/%d = %d/%d, so <i>w</i> = %d × %d ÷ %d = <b>%s m</b>." % (c_, b, a, c_, b, a, num(w)))


def build():
    sets = [S("Are the triangles similar?", collect(one_crit, 20, R)),
            S("Nested similar triangles", collect(one_nest, 20, R)),
            S("Triangle Proportionality Theorem", collect(one_prop, 20, R)),
            S("Geometric mean in right triangles", collect(one_gm, 20, R)),
            S("Indirect measurement", collect(one_word, 20, R))]
    body = lesson(
        "<p>Triangles are <b>similar</b> when their angles are congruent and their sides are proportional. Three shortcuts prove it:</p>"
        "<ul><li><b>AA</b>: two pairs of congruent angles.</li><li><b>SSS~</b>: all three pairs of sides in the same ratio.</li>"
        "<li><b>SAS~</b>: two pairs of sides in the same ratio and the angles between them congruent.</li></ul>"
        "<p>If <span class='ov'>DE</span> ∥ <span class='ov'>BC</span>, then △ADE ~ △ABC, and AD/DB = AE/EC (<b>Triangle Proportionality Theorem</b>). "
        "When you compare the small and large triangles, use the <b>whole</b> side AB = AD + DB.</p>"
        "<p>In a right triangle, the altitude to the hypotenuse makes two smaller similar triangles: CD² = AD × DB, and AC² = AD × AB.</p>",
        [("<span class='ov'>DE</span> ∥ <span class='ov'>BC</span>, AD = 4, DB = 6 and DE = 5. Find BC.", ["AB = 4 + 6 = 10", "BC/5 = 10/4"], "BC = 12.5"),
         ("A 6 ft person casts a 4 ft shadow, and a tree casts a 30 ft shadow. How tall is the tree?", ["6/4 = <i>h</i>/30"], "45 ft")],
        ["Using DB instead of the whole side AB when comparing △ADE with △ABC.",
         "Calling triangles similar by SSA or by one pair of angles.",
         "Matching sides in the wrong order. Match shortest to shortest and longest to longest.",
         "Using the whole hypotenuse in CD² = AD × DB. Use the two segments."])
    faq = [("How do you prove triangles are similar?", "Use AA (two pairs of congruent angles), SSS similarity (all sides proportional) or SAS similarity (two sides proportional with the included angle congruent)."),
           ("What is the Triangle Proportionality Theorem?", "If a line parallel to one side of a triangle crosses the other two sides, it divides them proportionally."),
           ("What is the geometric mean in a right triangle?", "The altitude to the hypotenuse is the geometric mean of the two hypotenuse segments: h² = (segment 1)(segment 2)."),
           ("How do shadows show similar triangles?", "At the same time of day, the sun's rays hit objects at the same angle, so each object and its shadow form similar right triangles.")]
    make("similar-triangles", 14, "G-SRT.B.5",
         "Similar Triangles: AA, SSS, SAS and Proportions",
         "Similar Triangles Worksheet: AA, SSS, SAS, Side Splitter (Geometry, G-SRT.B.5) | 100 Questions",
         "Similar Triangles",
         "Use congruence and similarity criteria for triangles to solve problems and to prove relationships in geometric figures.",
         "Free Geometry worksheet on similar triangles: AA, SSS and SAS similarity, nested triangles, the Triangle Proportionality Theorem, geometric mean and shadows. 100 questions with answers.",
         "AA, SSS~ and SAS~ prove triangles similar.",
         "If DE ∥ BC, then AD/DB = AE/EC. Use the whole side when comparing the small and large triangles.",
         body, faq, sets, R, domain="Similarity", grade="geometry")


if __name__ == "__main__":
    build()
