# -*- coding: utf-8 -*-
"""
US Geometry: Parallel Lines and Transversals (Common Core G-CO.C.9)
  python3 tools/gen_us_math_ge_parallel_lines_and_transversals.py
Naming angle pairs (corresponding, alternate interior, alternate exterior, same-side interior), finding
angle measures, solving for x, proving lines parallel with the converse theorems, and word problems.
Wrong answers come from real mistakes: mixing up alternate interior and same-side interior angles,
setting same-side interior angles equal instead of adding to 180°, and using the angle theorems when the
lines are not parallel.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, pol, RED, GREEN, BLUE, INK

R = random.Random(92601)
ANG = "∠"
ACUTE = {2, 3, 6, 7}
PAIRS = {
    "corresponding angles": [(1, 5), (2, 6), (3, 7), (4, 8)],
    "alternate interior angles": [(3, 6), (4, 5)],
    "alternate exterior angles": [(1, 8), (2, 7)],
    "same-side interior angles": [(3, 5), (4, 6)],
    "vertical angles": [(1, 4), (2, 3), (5, 8), (6, 7)],
    "a linear pair": [(1, 2), (1, 3), (2, 4), (3, 4), (5, 6), (5, 7), (6, 8), (7, 8)],
}


def kind_of(a, b):
    for k, v in PAIRS.items():
        if (a, b) in v or (b, a) in v:
            return k


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def trans_fig(labels, acute=62, marks=True, names=("ℓ", "<i>m</i>", "<i>t</i>"), skew=0):
    """two horizontal lines (top: angles 1-4, bottom: 5-8) cut by a transversal; labels {n: text}"""
    c = Canvas()
    y1, y2 = 50, 150
    dx = (y2 - y1) / math.tan(math.radians(acute))
    P = (150 + dx / 2, y1)
    Q = (150 - dx / 2, y2)
    c.fullline((40, y1), (260, y1 - skew), 14)
    c.fullline((40, y2), (260, y2 + skew), 14)
    ux, uy = (P[0] - Q[0]), (P[1] - Q[1])
    d = math.hypot(ux, uy)
    ux, uy = ux / d, uy / d
    c.fullline((Q[0] - ux * 40, Q[1] - uy * 40), (P[0] + ux * 40, P[1] + uy * 40), 12)
    if marks and not skew:
        c.chevrons((60, y1), (110, y1))
        c.chevrons((60, y2), (110, y2))
    c.text((282, y1 - skew), names[0], 16, italic=True)
    c.text((282, y2 + skew), names[1], 16)
    c.text((P[0] + ux * 60 + 10, P[1] + uy * 60), names[2], 16)
    up = math.degrees(math.atan2(-uy, ux))       # direction of the transversal going up, as on paper
    mids = {1: (up + 180) / 2, 2: up / 2, 3: (180 + up + 180) / 2, 4: (up + 180 + 360) / 2}
    for n in range(1, 9):
        t = labels.get(n)
        if not t:
            continue
        O = P if n <= 4 else Q
        k = (n - 1) % 4 + 1
        col = GREEN if t.isdigit() else INK
        if len(t) <= 4 or "<i>x</i>°" == t:
            mid = mids[k]
            rr = 30 if n in ACUTE else 24
            c.text(pol(O[0], O[1], rr, mid), t, 14 if t.isdigit() else 13, col)
            continue
        sh = 14 / math.tan(math.radians(acute))
        pos = {1: ((O[0] - 6, O[1] - 14), "end"), 2: ((O[0] + sh + 6, O[1] - 14), "start"),
               3: ((O[0] - sh - 6, O[1] + 15), "end"), 4: ((O[0] + 6, O[1] + 15), "start")}[k]
        c.text(pos[0], t, 13, col, anchor=pos[1])
    return c.svg("two lines cut by a transversal, not drawn to scale")


NUMS = {n: str(n) for n in range(1, 9)}


# ------------------------------------------------------------ set 1: name the pair
def one_name(r):
    k = r.choice(["corresponding angles", "alternate interior angles", "alternate exterior angles", "same-side interior angles",
                  "corresponding angles", "alternate interior angles", "vertical angles", "a linear pair"])
    a, b = r.choice(PAIRS[k])
    if r.random() < 0.5:
        a, b = b, a
    if r.random() < 0.7:
        q = "How are %s%d and %s%d related?%s" % (ANG, a, ANG, b, fig(trans_fig(NUMS)))
        others = [x for x in PAIRS if x != k]
        near = {"corresponding angles": ["alternate interior angles", "alternate exterior angles", "same-side interior angles"],
                "alternate interior angles": ["same-side interior angles", "alternate exterior angles", "corresponding angles"],
                "alternate exterior angles": ["alternate interior angles", "corresponding angles", "vertical angles"],
                "same-side interior angles": ["alternate interior angles", "corresponding angles", "a linear pair"],
                "vertical angles": ["corresponding angles", "a linear pair", "alternate exterior angles"],
                "a linear pair": ["vertical angles", "same-side interior angles", "corresponding angles"]}[k]
        why = {"corresponding angles": "They are in the same position at each intersection (both %s)." % ("above" if a in (1, 2, 5, 6) else "below"),
               "alternate interior angles": "They are between the two lines and on opposite sides of the transversal.",
               "alternate exterior angles": "They are outside the two lines and on opposite sides of the transversal.",
               "same-side interior angles": "They are between the two lines and on the same side of the transversal.",
               "vertical angles": "They are across from each other at the same intersection.",
               "a linear pair": "They are side by side at the same intersection and form a straight line."}[k]
        return T(q, k.capitalize(), [x.capitalize() for x in near], why + " <b>%s</b>." % k.capitalize())
    q = "Which angle and %s%d are %s?%s" % (ANG, a, B(k.replace("a linear pair", "a linear pair")), fig(trans_fig(NUMS)))
    others = [x for x in range(1, 9) if x != a and x != b and kind_of(a, x) != k]
    r.shuffle(others)
    return T(q, "%s%d" % (ANG, b), ["%s%d" % (ANG, x) for x in others[:3]],
             "%s%d and <b>%s%d</b> are %s." % (ANG, a, ANG, b, k))


# ------------------------------------------------------------ set 2: find a measure
def one_find(r):
    a = r.randint(35, 80)
    known = r.randint(1, 8)
    ask = r.choice([x for x in range(1, 9) if x != known and not ((known <= 4) == (x <= 4) and kind_of(known, x) in ("vertical angles", "a linear pair") and r.random() < 0.6)])
    vk = a if known in ACUTE else 180 - a
    va = a if ask in ACUTE else 180 - a
    lab = {known: "%d°" % vk, ask: "<i>x</i>°"}
    q = "Lines ℓ and <i>m</i> are parallel. Find <i>x</i>.%s" % fig(trans_fig(lab, acute=a if a > 40 else 45))
    k = kind_of(known, ask)
    if va == vk:
        why = ("The angles are %s, so they are congruent." % k) if k else (
            "Both angles are %s. With parallel lines, all the %s angles are congruent." % ("acute" if vk < 90 else "obtuse", "acute" if vk < 90 else "obtuse"))
        e = why + " <i>x</i> = <b>%d</b>." % va
    else:
        why = ("The angles are %s, so they add to 180°." % k) if k else (
            "One angle is acute and the other is obtuse. With parallel lines, an acute angle and an obtuse angle add to 180°.")
        e = why + " <i>x</i> = 180 %s %d = <b>%d</b>." % (MINUS, vk, va)
    wr = [180 - va, 90 - va if va < 90 else va - 90, 360 - va]
    return T(q, num(va), [num(w) for w in dict.fromkeys(wr) if w != va and w > 0][:3], e)


# ------------------------------------------------------------ set 3: algebra
def one_alg(r):
    k = r.choice(["corresponding angles", "alternate interior angles", "alternate exterior angles", "same-side interior angles", "same-side interior angles"])
    a, b = r.choice(PAIRS[k])
    x = r.randint(5, 25)
    c1 = r.randint(2, 7)
    d1 = r.randint(-20, 30)
    v1 = c1 * x + d1
    if not (30 <= v1 <= 150) or v1 == 90:
        return None
    if k == "same-side interior angles":
        v2 = 180 - v1
        c2 = r.randint(1, 6)
        d2 = v2 - c2 * x
    else:
        v2 = v1
        c2 = r.choice([c for c in range(1, 8) if c != c1])
        d2 = v2 - c2 * x
    if abs(d2) > 60:
        return None
    acute = v1 if (a in ACUTE) == (v1 < 90) else 180 - v1
    if (a in ACUTE) != (v1 < 90):
        return None
    lab = {a: lin(c1, d1) + "°", b: lin(c2, d2) + "°"}
    ask = r.choice(["x", "x", "angle"])
    q = "Lines ℓ and <i>m</i> are parallel. %s%s" % ("Find <i>x</i>." if ask == "x" else "Find the measure of the angle labeled (%s)°." % lin(c1, d1),
                                                      fig(trans_fig(lab, acute=min(acute, 180 - acute) if min(acute, 180 - acute) >= 40 else 45)))
    if k == "same-side interior angles":
        steps = "Same-side interior angles add to 180°: (%s) + (%s) = 180, so %d<i>x</i> = %d and <i>x</i> = %d." % (
            lin(c1, d1), lin(c2, d2), c1 + c2, 180 - d1 - d2, x)
        alt = (d2 - d1) / (c1 - c2) if c1 != c2 else None
    else:
        diff = abs(c1 - c2)
        steps = "%s are congruent: %s = %s, so %s<i>x</i> = %d and <i>x</i> = %d." % (
            k.capitalize(), lin(c1, d1), lin(c2, d2), num(diff) if diff > 1 else "", abs(d2 - d1), x)
        steps = steps.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(d2 - d1), ", so <i>x</i> = ")
        alt = (180 - d1 - d2) / (c1 + c2)
    if ask == "x":
        wr = [int(alt) if alt and alt == int(alt) and alt > 0 else x + 2, v1, x + 1, x - 1]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3],
                 steps[:steps.rindex("= %d." % x)] + "= <b>%d</b>." % x)
    wr = [180 - v1, x, v1 + 10]
    return T(q, "%d°" % v1, ["%d°" % w for w in dict.fromkeys(wr) if w != v1 and w > 0][:3],
             steps + " The angle is %d(%d) %s %d = <b>%d°</b>." % (c1, x, "+" if d1 >= 0 else MINUS, abs(d1), v1))


# ------------------------------------------------------------ set 4: proving lines parallel
def one_conv(r):
    kind = r.choice(["yes", "no", "which", "which"])
    if kind == "which":
        k = r.choice(["corresponding angles", "alternate interior angles", "alternate exterior angles", "same-side interior angles"])
        a, b = r.choice(PAIRS[k])
        if k == "same-side interior angles":
            right = "m%s%d + m%s%d = 180°" % (ANG, a, ANG, b)
            wr = ["%s%d ≅ %s%d" % (ANG, a, ANG, b)]
            why = "If same-side interior angles are supplementary, the lines are parallel."
        else:
            right = "%s%d ≅ %s%d" % (ANG, a, ANG, b)
            wr = ["m%s%d + m%s%d = 180°" % (ANG, a, ANG, b)]
            why = "If %s are congruent, the lines are parallel (converse of the %s theorem)." % (k, k[:-1])
        vp = r.choice(PAIRS["vertical angles"])
        lp = r.choice(PAIRS["a linear pair"])
        wr += ["%s%d ≅ %s%d" % (ANG, vp[0], ANG, vp[1]), "m%s%d + m%s%d = 180°" % (ANG, lp[0], ANG, lp[1])]
        q = "Which fact is enough to prove ℓ ∥ <i>m</i>?%s" % fig(trans_fig(NUMS, marks=False))
        return T(q, right, wr, why + " Vertical angles and linear pairs are always true, so they prove nothing. <b>%s</b>" % right)
    k = r.choice(["corresponding angles", "alternate interior angles", "alternate exterior angles", "same-side interior angles"])
    a, b = r.choice(PAIRS[k])
    va = r.randint(40, 80) if a in ACUTE else r.randint(100, 140)
    if k == "same-side interior angles":
        vb = 180 - va if kind == "yes" else 180 - va + r.choice([-6, -4, 4, 6])
    else:
        vb = va if kind == "yes" else va + r.choice([-5, -3, 3, 5])
    sk = 0 if kind == "yes" else r.choice([-6, 6])
    lab = {a: "%d°" % va, b: "%d°" % vb}
    q = "Is ℓ parallel to <i>m</i>?%s" % fig(trans_fig(lab, acute=va if va < 90 else 180 - va, marks=False, skew=sk))
    if kind == "yes":
        right = "Yes"
        e = ("The angles are %s and they %s, so ℓ ∥ <i>m</i>. <b>Yes</b>." % (
            k, "add to %d° + %d° = 180°" % (va, vb) if k == "same-side interior angles" else "are congruent (%d°)" % va))
    else:
        right = "No"
        e = ("The angles are %s. For parallel lines they would %s, but here %s. <b>No</b>." % (
            k, "add to 180°" if k == "same-side interior angles" else "be congruent",
            "%d° + %d° = %d°" % (va, vb, va + vb) if k == "same-side interior angles" else "%d° ≠ %d°" % (va, vb)))
    return T(q, right, ["No" if right == "Yes" else "Yes", "Only if the transversal is perpendicular", "There is not enough information"], e)


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["street", "rail", "stairs", "perp", "zig", "zig"])
    if kind == "street":
        a = r.randint(48, 78)
        q = ("Oak Street and Pine Street are parallel. Main Street crosses both. The angle on the north side of Oak Street, east of Main Street, is %d°. "
             "What is the corresponding angle at Pine Street?" % a)
        ans, wr = a, [180 - a, 90 - a, 2 * a]
        e = "Corresponding angles formed by parallel streets are congruent: <b>%d°</b>." % a
    elif kind == "rail":
        a = r.randint(40, 75)
        q = ("A road crosses two parallel railroad tracks. One angle between the road and the first track is %d°. "
             "What is the same-side interior angle at the second track?" % a)
        ans, wr = 180 - a, [a, 90 - a, 360 - a]
        e = "Same-side interior angles with parallel lines are supplementary: 180° %s %d° = <b>%d°</b>." % (MINUS, a, ans)
    elif kind == "stairs":
        a = r.randint(30, 45)
        q = ("The handrail of a staircase is parallel to the line of the stairs. The stairs make a %d° angle with the floor. "
             "The handrail post is vertical. What acute angle does the handrail make with the post?" % a)
        ans, wr = 90 - a, [a, 180 - a, 90 + a]
        e = ("The handrail makes a %d° angle with the horizontal (corresponding angles). The post is vertical, at 90° to the horizontal, "
             "so the angle between the rail and the post is 90° %s %d° = <b>%d°</b>." % (a, MINUS, a, ans))
    elif kind == "perp":
        q = "Line <i>t</i> is perpendicular to line ℓ, and line ℓ is parallel to line <i>m</i>. What angle does <i>t</i> make with <i>m</i>?"
        return T(q, "90°", ["45°", "180°", "It cannot be known"],
                 "Corresponding angles are congruent. <i>t</i> makes 90° with ℓ, so it also makes <b>90°</b> with <i>m</i>.")
    else:
        a, b = r.randint(25, 60), r.randint(25, 60)
        c = Canvas()
        c.fullline((30, 40), (270, 40), 12)
        c.fullline((30, 160), (270, 160), 12)
        c.chevrons((40, 40), (90, 40))
        c.chevrons((40, 160), (90, 160))
        V = (200, 100)
        A = (V[0] - 60 / math.tan(math.radians(a)), 40)
        Bp = (V[0] - 60 / math.tan(math.radians(b)), 160)
        c.seg(A, V)
        c.seg(V, Bp)
        c.dot(V, 3.5)
        c.angle(A, V, (270, 40), "%d°" % a, r=22, tr=40)
        c.angle(Bp, V, (270, 160), "%d°" % b, r=22, tr=40)
        c.angle(V, A, Bp, "<i>x</i>°", r=18, tr=30)
        c.text((292, 40), "ℓ", 16, italic=True)
        c.text((292, 160), "<i>m</i>", 16)
        svg = c.svg("two parallel lines with a bent path between them, not drawn to scale")
        q = "Lines ℓ and <i>m</i> are parallel. Find <i>x</i>.%s" % fig(svg)
        ans = a + b
        wr = [180 - a - b, abs(a - b), 360 - a - b]
        e = ("Draw a line through the bend, parallel to ℓ and <i>m</i>. It splits <i>x</i> into two parts that are alternate interior angles "
             "with %d° and %d°. So <i>x</i> = %d + %d = <b>%d</b>." % (a, b, a, b, ans))
        return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)
    return T(q, "%d°" % ans, ["%d°" % w for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


def build():
    sets = [S("Name the angle pair", collect(one_name, 20, R)),
            S("Find angle measures", collect(one_find, 20, R)),
            S("Solve for x", collect(one_alg, 20, R)),
            S("Prove lines parallel", collect(one_conv, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>A <b>transversal</b> crosses two lines and makes eight angles. When the two lines are <b>parallel</b>:</p>"
        "<ul><li><b>Corresponding</b> angles (same position) are congruent.</li>"
        "<li><b>Alternate interior</b> angles (between the lines, opposite sides) are congruent.</li>"
        "<li><b>Alternate exterior</b> angles (outside the lines, opposite sides) are congruent.</li>"
        "<li><b>Same-side interior</b> angles (between the lines, same side) add to 180°.</li></ul>"
        "<p>Shortcut: every acute angle in the picture is equal, every obtuse angle is equal, and an acute plus an obtuse is 180°.</p>"
        "<p>The <b>converses</b> are also true: if corresponding angles are congruent (or same-side interior angles are supplementary), the lines are parallel.</p>",
        [("ℓ ∥ <i>m</i>. Alternate interior angles are (4<i>x</i> + 6)° and (6<i>x</i> %s 30)°. Find <i>x</i>." % MINUS,
          ["Alternate interior angles are congruent: 4<i>x</i> + 6 = 6<i>x</i> %s 30" % MINUS, "36 = 2<i>x</i>"], "<i>x</i> = 18"),
         ("ℓ ∥ <i>m</i>. Same-side interior angles are (3<i>x</i>)° and (2<i>x</i> + 30)°. Find both angles.",
          ["They add to 180: 5<i>x</i> + 30 = 180, <i>x</i> = 30"], "90° and 90°")],
        ["Setting same-side interior angles equal. They add to 180°.",
         "Mixing up alternate interior (opposite sides) and same-side interior (same side).",
         "Using these rules when the lines are not marked parallel.",
         "Using vertical angles to prove lines parallel. Vertical angles are always congruent, so they prove nothing."])
    faq = [("What are alternate interior angles?",
            "Angles between the two lines and on opposite sides of the transversal. When the lines are parallel, they are congruent."),
           ("Are same-side interior angles congruent?", "No. When the lines are parallel, same-side interior angles are supplementary: they add to 180 degrees."),
           ("How do you prove two lines are parallel?",
            "Show that a pair of corresponding, alternate interior or alternate exterior angles is congruent, or that same-side interior angles are supplementary."),
           ("What are corresponding angles?", "Angles in the same relative position at each intersection, such as both above the line and to the right of the transversal.")]
    make("parallel-lines-and-transversals", 6, "G-CO.C.9",
         "Parallel Lines and Transversals",
         "Parallel Lines and Transversals Worksheet (Geometry, G-CO.C.9) | 100 Questions with Answers",
         "Parallel Lines and Transversals",
         "Prove theorems about lines and angles. Theorems include: vertical angles are congruent; when a transversal crosses parallel lines, alternate interior angles are congruent and corresponding angles are congruent; points on a perpendicular bisector of a line segment are exactly those equidistant from the segment's endpoints.",
         "Free Geometry worksheet on parallel lines cut by a transversal: corresponding, alternate interior and same-side interior angles, solving for x, and proving lines parallel. 100 questions.",
         "Parallel lines: corresponding and alternate angles are congruent.",
         "Same-side interior angles add to 180°. The converses prove lines parallel.",
         body, faq, sets, R, domain="Parallel and Perpendicular Lines", grade="geometry")


if __name__ == "__main__":
    build()
