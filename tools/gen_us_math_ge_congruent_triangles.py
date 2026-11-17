# -*- coding: utf-8 -*-
"""
US Geometry: Congruent Triangles (Common Core G-CO.B.8, G-CO.B.7, G-SRT.B.5)
  python3 tools/gen_us_math_ge_congruent_triangles.py
Choosing SSS, SAS, ASA, AAS or HL from marked figures, corresponding parts in a congruence statement,
the missing piece of information, CPCTC with algebra, and shared sides and vertical angles.
Wrong answers come from real mistakes: calling SSA or AAA a congruence test, mixing up ASA and AAS,
matching vertices in the wrong order, and choosing SAS when the angle is not between the two sides.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS
from us_geo import Canvas, RED, GREEN, BLUE, INK

R = random.Random(93001)
CRIT = ["SSS", "SAS", "ASA", "AAS", "HL", "Not enough information"]
NEAR = {"SSS": ["SAS", "ASA", "Not enough information"], "SAS": ["SSS", "ASA", "Not enough information"],
        "ASA": ["AAS", "SAS", "Not enough information"], "AAS": ["ASA", "SAS", "Not enough information"],
        "HL": ["SAS", "SSS", "Not enough information"], "Not enough information": ["SAS", "ASA", "AAS"]}


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


SHAPES = [[(0, 120), (150, 120), (40, 10)], [(0, 120), (160, 110), (100, 0)], [(10, 120), (150, 120), (120, 20)]]
RIGHT = [(0, 120), (150, 120), (0, 20)]


def marks(c, P, sides, angles, right=None):
    for i, n in sides.items():
        c.ticks(P[i], P[(i + 1) % 3], n)
    for i, n in angles.items():
        c.arc(P[i], P[(i + 1) % 3], P[(i + 2) % 3], 18, GREEN, n)
    if right is not None:
        c.right(P[right], P[(right + 1) % 3], P[(right + 2) % 3])


def pair_fig(shape, sides, angles, names1="ABC", names2="DEF", right=None, mirror=True):
    c = Canvas()
    P1 = [(x + 20, y + 20) for x, y in shape]
    P2 = [((200 - x if mirror else x) + 230, y + 20) for x, y in shape]
    if mirror:
        P2 = [(400 - x + 40, y + 20) for x, y in shape]
    for P, names in ((P1, names1), (P2, names2)):
        c.poly(P)
        marks(c, P, sides, angles, right)
        c.vlabels(P, names)
    return c.svg("two triangles with matching marks, not drawn to scale")


def setup(kind, r):
    """return (sides, angles, right) marking dicts on a triangle with vertices 0,1,2 (side i = P_i P_i+1)"""
    k = r.randint(0, 2)
    rot = lambda i: (i + k) % 3
    if kind == "SSS":
        return {0: 1, 1: 2, 2: 3}, {}, None
    if kind == "SAS":
        return {rot(0): 1, rot(1): 2}, {rot(1): 1}, None
    if kind == "ASA":
        return {rot(0): 1}, {rot(0): 1, rot(1): 2}, None
    if kind == "AAS":
        return {rot(1): 1}, {rot(0): 1, rot(1): 2}, None
    if kind == "SSA":
        return {rot(0): 1, rot(1): 2}, {rot(0): 1}, None
    if kind == "AAA":
        return {}, {0: 1, 1: 2, 2: 3}, None
    if kind == "HL":
        return {0: 1, 1: 2}, {}, 0


# ------------------------------------------------------------ set 1: which criterion
def one_crit(r):
    kind = r.choice(["SSS", "SAS", "ASA", "AAS", "HL", "SSA", "AAA", "SAS", "ASA", "AAS"])
    sides, angles, right = setup(kind, r)
    shape = RIGHT if kind == "HL" else r.choice(SHAPES)
    svg = pair_fig(shape, sides, angles, right=right, mirror=r.random() < 0.5)
    ans = kind if kind in CRIT else "Not enough information"
    q = "Which shortcut proves the triangles congruent? Choose \"Not enough information\" if none does.%s" % fig(svg)
    e = {"SSS": "All three pairs of sides are marked congruent: <b>SSS</b>.",
         "SAS": "Two pairs of sides and the angle <b>between</b> them: <b>SAS</b>.",
         "ASA": "Two pairs of angles and the side <b>between</b> them: <b>ASA</b>.",
         "AAS": "Two pairs of angles and a side that is <b>not</b> between them: <b>AAS</b>.",
         "HL": "Right triangles with congruent hypotenuses and one pair of congruent legs: <b>HL</b>.",
         "SSA": "Two sides and an angle that is <b>not</b> between them (SSA) is not a congruence test: <b>Not enough information</b>.",
         "AAA": "Three angles (AAA) only shows the same shape, not the same size: <b>Not enough information</b>."}[kind]
    near = NEAR[ans] if kind not in ("SSA", "AAA") else (["SAS", "AAS", "HL"] if kind == "SSA" else ["ASA", "AAS", "SSS"])
    return T(q, ans, near, e)


# ------------------------------------------------------------ set 2: corresponding parts
def one_corr(r):
    L1 = r.sample("ABCDEFGHJKLMNPQRSTUVWXYZ", 6)
    a, b, c_ = L1[:3]
    d, e_, f = L1[3:]
    stmt = "△%s%s%s ≅ △%s%s%s" % (a, b, c_, d, e_, f)
    m = {a: d, b: e_, c_: f}
    kind = r.choice(["side", "side", "angle", "angle", "stmt"])
    if kind == "side":
        p, q_ = r.sample([a, b, c_], 2)
        right = "<span class='ov'>%s%s</span>" % (m[p], m[q_])
        others = [(x, y) for x, y in [(d, e_), (e_, f), (d, f)] if {x, y} != {m[p], m[q_]}]
        wr = ["<span class='ov'>%s%s</span>" % o for o in others] + ["<span class='ov'>%s%s</span>" % (m[q_], [v for v in (d, e_, f) if v not in (m[p], m[q_])][0])]
        q = "Given %s, which segment is congruent to %s?" % (B(stmt), "<span class='ov'>%s%s</span>" % (p, q_))
        e = "Match the letters in order: %s → %s and %s → %s. So %s%s ≅ <b>%s</b>." % (p, m[p], q_, m[q_], p, q_, right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    if kind == "angle":
        p = r.choice([a, b, c_])
        right = "∠%s" % m[p]
        wr = ["∠%s" % v for v in (d, e_, f) if v != m[p]] + ["∠%s" % [x for x in (a, b, c_) if x != p][0]]
        q = "Given %s, which angle is congruent to ∠%s?" % (B(stmt), p)
        e = "%s is in the same position as %s in the statement, so ∠%s ≅ <b>%s</b>." % (p, m[p], p, right)
        return T(q, right, wr[:3], e)
    perm = r.sample([0, 1, 2], 3)
    if perm == [0, 1, 2]:
        return None
    src = [a, b, c_]
    dst = [d, e_, f]
    s2 = "△%s%s%s" % tuple(src[i] for i in perm)
    right = "△%s%s%s" % tuple(dst[i] for i in perm)
    wr = ["△%s%s%s" % (d, e_, f), "△%s%s%s" % tuple(dst[i] for i in perm[::-1]), "△%s%s%s" % (f, e_, d)]
    q = "Given %s, complete the statement: %s ≅ ?" % (B(stmt), s2)
    e = "Keep each pair of matching vertices together: %s. So %s ≅ <b>%s</b>." % (", ".join("%s ↔ %s" % (src[i], dst[i]) for i in perm), s2, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: what else is needed
def one_need(r):
    want = r.choice(["SAS", "ASA", "AAS", "SSS", "HL"])
    names = "ABC", "DEF"
    if want == "SAS":
        given = "<span class='ov'>AB</span> ≅ <span class='ov'>DE</span> and ∠B ≅ ∠E"
        right = "<span class='ov'>BC</span> ≅ <span class='ov'>EF</span>"
        wr = ["<span class='ov'>AC</span> ≅ <span class='ov'>DF</span>", "∠A ≅ ∠D", "∠C ≅ ∠F"]
        why = "SAS needs the angle between the two sides. ∠B is between <span class='ov'>AB</span> and <span class='ov'>BC</span>"
    elif want == "ASA":
        given = "∠A ≅ ∠D and ∠B ≅ ∠E"
        right = "<span class='ov'>AB</span> ≅ <span class='ov'>DE</span>"
        wr = ["<span class='ov'>BC</span> ≅ <span class='ov'>EF</span>", "<span class='ov'>AC</span> ≅ <span class='ov'>DF</span>", "∠C ≅ ∠F"]
        why = "ASA needs the side between the two angles. <span class='ov'>AB</span> is between ∠A and ∠B"
    elif want == "AAS":
        given = "∠A ≅ ∠D and ∠B ≅ ∠E"
        right = "<span class='ov'>BC</span> ≅ <span class='ov'>EF</span>"
        wr = ["<span class='ov'>AB</span> ≅ <span class='ov'>DE</span>", "∠C ≅ ∠F", "<span class='ov'>AB</span> ≅ <span class='ov'>EF</span>"]
        why = "AAS needs a side that is not between the two angles, such as <span class='ov'>BC</span>"
    elif want == "SSS":
        given = "<span class='ov'>AB</span> ≅ <span class='ov'>DE</span> and <span class='ov'>BC</span> ≅ <span class='ov'>EF</span>"
        right = "<span class='ov'>AC</span> ≅ <span class='ov'>DF</span>"
        wr = ["∠B ≅ ∠E", "∠A ≅ ∠D", "<span class='ov'>AC</span> ≅ <span class='ov'>EF</span>"]
        why = "SSS needs the third pair of sides"
    else:
        given = "∠C and ∠F are right angles, and <span class='ov'>AB</span> ≅ <span class='ov'>DE</span> (the hypotenuses)"
        right = "<span class='ov'>AC</span> ≅ <span class='ov'>DF</span>"
        wr = ["∠A ≅ ∠E", "∠B ≅ ∠D", "<span class='ov'>AB</span> ≅ <span class='ov'>EF</span>"]
        why = "HL needs the hypotenuses and one pair of legs. <span class='ov'>AC</span> and <span class='ov'>DF</span> are legs"
    # rename letters to vary the question
    pool = [("ABC", "DEF"), ("PQR", "XYZ"), ("JKL", "MNO"), ("RST", "UVW"), ("GHI", "LMN")]
    s1, s2 = r.choice(pool)
    tr = str.maketrans("ABCDEF", s1 + s2)
    given, right, wr, why = given.translate(tr), right.translate(tr), [w.translate(tr) for w in wr], why.translate(tr)
    why = why.replace("%s needs" % want.translate(tr), "%s needs" % want)
    q = "In △%s and △%s, %s. What else do you need to prove △%s ≅ △%s by %s?" % (s1, s2, given, s1, s2, want)
    return T(q, right, wr, why + ": <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: CPCTC with algebra
def one_cpctc(r):
    s1, s2 = r.choice([("ABC", "DEF"), ("PQR", "XYZ"), ("JKL", "MNP"), ("RST", "UVW"), ("GHK", "LMN")])
    x = r.randint(2, 14)
    k1, k2 = r.sample(range(1, 8), 2)
    if r.random() < 0.5:
        i, j = r.sample(range(3), 2)
        val = r.randint(8, 40)
        d1 = val - k1 * x
        if abs(d1) > 30:
            return None
        sideA = s1[i] + s1[j]
        sideB = s2[i] + s2[j]
        ask = r.choice(["x", "len"])
        if ask == "x":
            q = "△%s ≅ △%s. %s = %s and %s = %s. Find <i>x</i>." % (s1, s2, sideA, lin(k1, d1), sideB, num(val))
            e = "Corresponding parts of congruent triangles are congruent (CPCTC): %s = %s, so %s = %d and <i>x</i> = <b>%d</b>." % (
                sideA, sideB, lin(k1, d1), val, x)
            wr = [val, x + 1, x + 2, (val + d1) // k1 if (val + d1) % k1 == 0 else x - 1]
            return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e)
        d2 = val - k2 * x
        if abs(d2) > 30:
            return None
        q = "△%s ≅ △%s. %s = %s and %s = %s. Find %s." % (s1, s2, sideA, lin(k1, d1), sideB, lin(k2, d2), sideB)
        diff = abs(k1 - k2)
        e = "CPCTC: %s = %s, so %s<i>x</i> = %d and <i>x</i> = %d. %s = %s = <b>%d</b>." % (
            lin(k1, d1), lin(k2, d2), num(diff) if diff > 1 else "", abs(d2 - d1), x, sideB, lin(k2, d2).replace("<i>x</i>", "(%d)" % x) if k2 > 1 else "%d %s %d" % (x, "+" if d2 >= 0 else MINUS, abs(d2)), val)
        e = e.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(d2 - d1), ", so <i>x</i> = ")
        return T(q, num(val), [num(w) for w in dict.fromkeys([x, val + k1, 2 * val, val - 2]) if w != val and w > 0][:3], e)
    i = r.randint(0, 2)
    others = [t for t in range(3) if t != i]
    a1, a2 = r.randint(30, 80), r.randint(30, 70)
    a3 = 180 - a1 - a2
    if a3 < 20:
        return None
    k = r.randint(2, 6)
    d = a3 - k * x
    if abs(d) > 40:
        return None
    q = "△%s ≅ △%s. m∠%s = %d°, m∠%s = %d° and m∠%s = (%s)°. Find <i>x</i>." % (s1, s2, s1[others[0]], a1, s1[others[1]], a2, s2[i], lin(k, d))
    e = ("∠%s corresponds to ∠%s, so m∠%s = 180 %s %d %s %d = %d. Then %s = %d, so <i>x</i> = <b>%d</b>." % (
        s2[i], s1[i], s1[i], MINUS, a1, MINUS, a2, a3, lin(k, d), a3, x))
    bad = (a1 - d) / k
    wr = [int(bad) if bad == int(bad) and bad > 0 else x + 2, a3, x + 1, x - 1]
    return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e)


# ------------------------------------------------------------ set 5: shared parts and reasoning
def kite_fig(kind):
    c = Canvas()
    if kind == "shared":
        A, Bp, C, D = (20, 90), (150, 10), (280, 90), (150, 170)
        c.poly([A, Bp, C, D])
        c.seg(Bp, D)
        c.vlabels([A, Bp, C, D], "ABCD")
        c.ticks(A, Bp, 1)
        c.ticks(Bp, C, 1)
        c.ticks(A, D, 2)
        c.ticks(C, D, 2)
        return c.svg("quadrilateral ABCD with diagonal BD")
    A, Bp, M, C, D = (20, 20), (20, 160), (150, 90), (280, 160), (280, 20)
    c.seg(A, C)
    c.seg(Bp, D)
    c.seg(A, Bp)
    c.seg(D, C)
    c.vlabels([A, Bp, C, D], "ABCD")
    c.text((150, 66), "M", 15)
    c.ticks(A, M, 1)
    c.ticks(M, C, 1)
    c.ticks(Bp, M, 2)
    c.ticks(M, D, 2)
    return c.svg("segments AC and BD crossing at M")


def one_reason(r):
    kind = r.choice(["shared", "vert", "tf", "tf", "perim", "perim", "ang", "ang"])
    if kind in ("perim", "ang"):
        s1, s2 = r.choice([("ABC", "DEF"), ("PQR", "XYZ"), ("JKL", "MNP"), ("RST", "UVW"), ("GHK", "LMN")])
        perm = r.sample([0, 1, 2], 3)
        t1 = "".join(s1[i] for i in perm)
        t2 = "".join(s2[i] for i in perm)
        if kind == "perim":
            a, b, c_ = r.randint(5, 20), r.randint(5, 20), r.randint(5, 20)
            if max(a, b, c_) >= a + b + c_ - max(a, b, c_):
                return None
            q = "△%s ≅ △%s. %s = %d, %s = %d and %s = %d. What is the perimeter of △%s?" % (t1, t2, s1[0] + s1[1], a, s1[1] + s1[2], b, s1[0] + s1[2], c_, s2)
            ans = a + b + c_
            return T(q, num(ans), [num(w) for w in dict.fromkeys([a + b, 2 * ans, ans - c_ + 1, ans + 2]) if w != ans][:3],
                     "Congruent triangles have congruent corresponding sides, so the perimeters are equal: %d + %d + %d = <b>%d</b>." % (a, b, c_, ans))
        a1, a2 = r.randint(30, 85), r.randint(30, 80)
        a3 = 180 - a1 - a2
        if a3 < 20:
            return None
        i = r.randint(0, 2)
        known = [j for j in range(3) if j != i]
        vals = {known[0]: a1, known[1]: a2, i: a3}
        q = "△%s ≅ △%s. m∠%s = %d° and m∠%s = %d°. Find m∠%s." % (t1, t2, s1[known[0]], a1, s2[known[1]], a2, s2[i])
        return T(q, "%d°" % a3, ["%d°" % w for w in dict.fromkeys([a1, a2, 180 - a1, 360 - a1 - a2]) if w != a3][:3],
                 "∠%s matches ∠%s, and ∠%s matches ∠%s. The third angle is 180 %s %d %s %d = <b>%d°</b>." % (
                     s1[known[0]], s2[known[0]], s2[known[1]], s1[known[1]], MINUS, a1, MINUS, a2, a3))
    if kind == "shared":
        q = "In the figure, which shortcut proves △ABD ≅ △CBD?%s" % fig(kite_fig("shared"))
        return T(q, "SSS", ["SAS", "ASA", "HL"],
                 "AB ≅ CB and AD ≅ CD are marked. BD ≅ BD by the Reflexive Property (a shared side). Three pairs of sides: <b>SSS</b>.")
    if kind == "vert":
        q = "Segments AC and BD bisect each other at M. Which shortcut proves △AMB ≅ △CMD?%s" % fig(kite_fig("vert"))
        return T(q, "SAS", ["SSS", "ASA", "AAS"],
                 "AM ≅ CM and BM ≅ DM. ∠AMB ≅ ∠CMD because they are vertical angles, and that angle is between the two pairs of sides: <b>SAS</b>.")
    items = [("Is AAA a way to prove two triangles congruent?", "No, because the triangles can be different sizes", ["Yes, always", "Yes, if the angles are acute", "No, because triangles have only two angles"],
              "Two equilateral triangles with sides 2 and 5 have the same angles but are not congruent."),
             ("Is SSA a way to prove two triangles congruent?", "No, because two different triangles can have the same SSA parts", ["Yes, always", "Yes, it is the same as SAS", "No, because a triangle has no SSA parts"],
              "The angle is not between the sides, so the third side can swing to two places."),
             ("What does CPCTC stand for?", "Corresponding parts of congruent triangles are congruent", ["Congruent parts can prove triangles congruent", "Corresponding points create two congruent triangles",
              "Congruent polygons can touch corners"], "Once triangles are proved congruent, every pair of corresponding sides and angles is congruent."),
             ("Why is HL a special case that works for right triangles?", "The Pythagorean theorem fixes the third side", ["Right angles are always congruent, so any two parts work", "The hypotenuse is always the shortest side", "HL is the same as SSA for all triangles"],
              "With the hypotenuse and one leg, the other leg is determined, so it becomes SSS."),
             ("Two triangles are congruent if one can be mapped onto the other by", "A sequence of rigid motions", ["A dilation", "Any transformation", "A sequence of dilations and translations"],
              "Congruence is defined by rigid motions (translations, reflections, rotations), which keep sizes the same."),
             ("In a proof, which reason shows that a side shared by two triangles is congruent to itself?", "Reflexive Property of Congruence", ["Symmetric Property of Congruence", "Vertical Angles Theorem", "CPCTC"],
              "Any segment is congruent to itself."),
             ("△ABC ≅ △DEF. Which must be true?", "The perimeters are equal", ["AB = EF", "∠A ≅ ∠F", "The triangles have the same orientation"],
              "All corresponding sides are equal, so the perimeters are equal. Orientation can change with a reflection.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Which shortcut proves congruence?", collect(one_crit, 20, R)),
            S("Corresponding parts", collect(one_corr, 20, R)),
            S("What else is needed?", collect(one_need, 20, R)),
            S("CPCTC with algebra", collect(one_cpctc, 20, R)),
            S("Shared sides and reasoning", collect(one_reason, 20, R))]
    body = lesson(
        "<p>Two triangles are <b>congruent</b> if a sequence of rigid motions maps one onto the other. Then all six pairs of corresponding parts are congruent. "
        "You only need to check three of them with a shortcut:</p>"
        "<ul><li><b>SSS</b>: three pairs of sides.</li><li><b>SAS</b>: two sides and the angle <b>between</b> them.</li>"
        "<li><b>ASA</b>: two angles and the side <b>between</b> them.</li><li><b>AAS</b>: two angles and a side <b>not</b> between them.</li>"
        "<li><b>HL</b>: right triangles with congruent hypotenuses and one pair of congruent legs.</li></ul>"
        "<p><b>AAA</b> and <b>SSA</b> do not prove congruence. In a congruence statement such as △ABC ≅ △DEF, the order of the letters shows which parts match. "
        "Look for hidden parts: a <b>shared side</b> (Reflexive Property) and <b>vertical angles</b>.</p>",
        [("△PQR ≅ △XYZ. Which side is congruent to <span class='ov'>QR</span>?", ["Q ↔ Y and R ↔ Z"], "<span class='ov'>YZ</span>"),
         ("∠A ≅ ∠D, ∠B ≅ ∠E and <span class='ov'>BC</span> ≅ <span class='ov'>EF</span>. Which shortcut?",
          ["The side BC is not between ∠A and ∠B"], "AAS")],
        ["Using SSA or AAA. They do not prove triangles congruent.",
         "Mixing up ASA and AAS. Check whether the side is between the two angles.",
         "Matching letters out of order. In △ABC ≅ △DEF, B matches E, not F.",
         "Forgetting the shared side or the vertical angles that the figure gives for free."])
    faq = [("What are the five ways to prove triangles congruent?", "SSS, SAS, ASA, AAS and HL (for right triangles)."),
           ("Why doesn't SSA prove triangles congruent?", "Two different triangles can have two equal sides and an equal angle that is not between them, so the parts do not fix one triangle."),
           ("What is the difference between ASA and AAS?", "In ASA the congruent side is between the two angles. In AAS the side is not between them."),
           ("What does CPCTC mean?", "Corresponding parts of congruent triangles are congruent. It is used after proving triangles congruent to show that other sides or angles are congruent.")]
    make("congruent-triangles", 10, "G-CO.B.8",
         "Congruent Triangles: SSS, SAS, ASA, AAS, and HL",
         "Congruent Triangles Worksheet: SSS, SAS, ASA, AAS, HL and CPCTC (Geometry) | 100 Questions",
         "Congruent Triangles",
         "Explain how the criteria for triangle congruence (ASA, SAS, and SSS) follow from the definition of congruence in terms of rigid motions.",
         "Free Geometry worksheet on congruent triangles: choose SSS, SAS, ASA, AAS or HL, corresponding parts, missing information and CPCTC with algebra. 100 questions with answers.",
         "SSS, SAS, ASA, AAS and HL prove triangles congruent. SSA and AAA do not.",
         "The order of the letters in △ABC ≅ △DEF shows which parts match.",
         body, faq, sets, R, domain="Triangles", grade="geometry")


if __name__ == "__main__":
    build()
