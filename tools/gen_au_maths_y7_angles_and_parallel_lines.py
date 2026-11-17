# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Angles and parallel lines (Australian Curriculum v9.0: AC9M7M04)
  python3 tools/gen_au_maths_y7_angles_and_parallel_lines.py
Corresponding, alternate and co-interior angles formed when a transversal crosses parallel lines: naming the
relationship, finding unknown angles from diagrams, equations with parallel lines, deciding whether lines are
parallel, and giving reasons.
Wrong answers come from real mistakes: thinking co-interior angles are equal, subtracting from 360°, and using
the rules when the lines are not parallel.
"""
import math
import random
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, GREEN

R = random.Random(71601)
POS = {"UR": 0, "UL": 1, "LL": 2, "LR": 3}


def parallel_svg(theta, top_pos, top_lab, bot_pos, bot_lab):
    W, H = 340, 230
    y1, y2 = 70, 160
    cx1 = 170 + (y2 - y1) / 2 / math.tan(math.radians(theta))
    cx2 = 170 - (y2 - y1) / 2 / math.tan(math.radians(theta))
    s = [line(20, y1, W - 20, y1, INK, 2.5), line(20, y2, W - 20, y2, INK, 2.5)]
    for y in (y1, y2):     # parallel arrows
        s.append("<path d='M%d %d l-9 -6 M%d %d l-9 6' stroke='%s' stroke-width='2.5' fill='none'/>" % (W - 60, y, W - 60, y, INK))
    L = 120
    dx, dy = math.cos(math.radians(theta)), -math.sin(math.radians(theta))
    s.append(line(cx1 + dx * 70, y1 + dy * 70, cx2 - dx * 70, y2 - dy * 70, INK, 2.5))
    def lab(cx, cy, pos, t):
        mids = {"UR": theta / 2, "UL": theta + (180 - theta) / 2, "LL": 180 + theta / 2, "LR": 180 + theta + (180 - theta) / 2}
        a = math.radians(mids[pos])
        rr = 30 if (pos in ("UR", "LL") and theta < 50) or (pos in ("UL", "LR") and theta > 130) else 24
        return text(cx + math.cos(a) * rr, cy - math.sin(a) * rr + 6, t, 15, col=RED if t in ("x", "y") else INK, italic=t in ("x", "y"))
    s.append(lab(cx1, y1, top_pos, top_lab))
    s.append(lab(cx2, y2, bot_pos, bot_lab))
    return svg_wrap(W, H, "".join(s), "two parallel lines crossed by a transversal")


def val(theta, pos):
    return theta if pos in ("UR", "LL") else 180 - theta


def relation(tp, bp):
    if tp == bp:
        return "corresponding"
    if (tp, bp) in (("LL", "UR"), ("LR", "UL")):
        return "alternate"
    if (tp, bp) in (("LL", "UL"), ("LR", "UR")):
        return "co-interior"
    return None


# ------------------------------------------------------------ set 1: parallel lines with diagrams
def one_parallel(r):
    theta = r.choice([35, 40, 48, 55, 62, 65, 70, 72, 110, 115, 118, 125, 130, 138])
    tp = r.choice(list(POS))
    bp = r.choice(list(POS))
    rel = relation(tp, bp)
    if rel is None:
        return None
    given = val(theta, tp)
    x = val(theta, bp)
    svg = parallel_svg(theta, tp, "%d°" % given, bp, "x")
    q = "The two lines with arrows are parallel. Find %s.%s<br><small>Not drawn to scale.</small>" % (B("<i>x</i>"), fig(svg))
    if rel == "co-interior":
        e = "These are <b>co-interior</b> angles (a C shape), so they add up to 180°: <i>x</i> = 180 − %d = <b>%d°</b>." % (given, x)
    else:
        e = "These are <b>%s</b> angles (%s), so they are equal: <b><i>x</i> = %d°</b>." % (rel, "an F shape" if rel == "corresponding" else "a Z shape", x)
    return QN(q, x, [180 - x, 360 - given, 90 - given if given < 90 else given - 90], e, unit="°")


def one_name(r):
    theta = r.choice([50, 60, 65, 70, 115, 120])
    tp = r.choice(list(POS))
    bp = r.choice(list(POS))
    rel = relation(tp, bp)
    if rel is None:
        return None
    svg = parallel_svg(theta, tp, "a", bp, "b")
    names = {"corresponding": "Corresponding (equal)", "alternate": "Alternate (equal)", "co-interior": "Co-interior (add to 180°)"}
    right = names[rel]
    q = "The lines with arrows are parallel. What is the relationship between angles <i>a</i> and <i>b</i>?%s" % fig(svg)
    e = "Look for the shape: F for corresponding, Z for alternate, C (or U) for co-interior. These are <b>%s</b>." % right.lower()
    return T(q, right, [v for v in names.values() if v != right] + ["Vertically opposite (equal)"], e)




def one_parallel2(r):
    return one_parallel(r)


# ------------------------------------------------------------ set 3: equations with parallel lines
def one_alg(r):
    kind = r.choice(["co", "alt", "corr", "co2"])
    if kind == "co":
        k = r.choice([2, 3, 4, 5, 8, 9])
        x = 180 // (k + 1)
        if 180 % (k + 1):
            return None
        q = "Two co-interior angles between parallel lines are <i>x</i> and %d<i>x</i>. Find <i>x</i>." % k
        return QN(q, x, [180 // k if 180 % k == 0 else x + 10, 360 // (k + 1) if 360 % (k + 1) == 0 else x * 2, 90 - x if 90 - x > 0 else x + 20],
                  "Co-interior angles add to 180°: %d<i>x</i> = 180, so <i>x</i> = <b>%d°</b>." % (k + 1, x), unit="°")
    if kind == "alt":
        a, x = r.randint(2, 5), r.randint(10, 30)
        b = r.randint(5, 30)
        ang = a * x + b
        if ang >= 180:
            return None
        q = "Alternate angles between parallel lines are %d<i>x</i> + %d and %d°. Find <i>x</i>." % (a, b, ang)
        return QN(q, x, [ang - b, (180 - ang - b) // a if (180 - ang - b) % a == 0 and (180 - ang - b) > 0 else x + 5, (ang + b) // a if (ang + b) % a == 0 else x + 3],
                  "Alternate angles are equal: %d<i>x</i> + %d = %d, so %d<i>x</i> = %d and <i>x</i> = <b>%d°</b>." % (a, b, ang, a, ang - b, x), unit="°")
    if kind == "corr":
        a, x = r.randint(2, 6), r.randint(10, 25)
        ang = a * x
        if ang >= 180:
            return None
        q = "Corresponding angles between parallel lines are %d<i>x</i> and %d°. Find <i>x</i>." % (a, ang)
        return QN(q, x, [ang * a if ang * a < 400 else x + 4, (180 - ang) // a if (180 - ang) % a == 0 else x + 6, ang - a], "Corresponding angles are equal: %d<i>x</i> = %d, so <i>x</i> = <b>%d°</b>." % (a, ang, x), unit="°")
    x = r.randint(20, 50)
    b = r.randint(10, 40)
    other = 180 - (x + b)
    if other <= 20:
        return None
    q = "Co-interior angles between parallel lines are (<i>x</i> + %d)° and %d°. Find <i>x</i>." % (b, other)
    return QN(q, x, [other - b, 180 - other, 180 - other + b], "They add to 180°: <i>x</i> + %d + %d = 180, so <i>x</i> = <b>%d°</b>." % (b, other, x), unit="°")


# ------------------------------------------------------------ set 4: are the lines parallel?
def one_check(r):
    rel = r.choice(["corresponding", "alternate", "co-interior"])
    a = r.randint(40, 140)
    par_ = r.random() < 0.5
    if rel == "co-interior":
        b = 180 - a if par_ else 180 - a + r.choice([-6, -4, 4, 6])
    else:
        b = a if par_ else a + r.choice([-5, -3, 3, 5])
    q = "A line crosses two other lines. A pair of %s angles measure %d° and %d°. Are the two lines parallel?" % (rel, a, b)
    if par_:
        right = "Yes, because %s" % ("the co-interior angles add to 180°" if rel == "co-interior" else "the %s angles are equal" % rel)
    else:
        right = "No, because %s" % ("the co-interior angles add to %d°, not 180°" % (a + b) if rel == "co-interior" else "the %s angles are not equal" % rel)
    wr = ["Yes, because %s" % ("the co-interior angles are equal" if rel == "co-interior" else "the angles add to 180°"),
          "No, because all angles must be 90°", "You cannot tell without measuring the lines"]
    if not par_:
        wr[0] = "Yes, because the angles are close"
    e = ("For parallel lines, corresponding and alternate angles are equal and co-interior angles add to 180°. Here %s, so <b>%s</b>."
         % ("%d + %d = %d" % (a, b, a + b) if rel == "co-interior" else "%d° and %d° are %s" % (a, b, "equal" if a == b else "different"), "yes" if par_ else "no"))
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems and reasons
def problems():
    data = [
        ("Which pair of angles are equal when lines are parallel?", "Alternate angles", ["Co-interior angles", "Angles on a straight line", "Angles in a triangle"], "<b>Alternate angles</b> (Z shape) are equal. Co-interior angles add to 180°."),
        ("Which shape helps you spot corresponding angles?", "An F shape", ["A Z shape", "A C shape", "An X shape"], "Corresponding angles sit in matching positions, like an <b>F shape</b>."),
        ("Which shape helps you spot co-interior angles?", "A C (or U) shape", ["A Z shape", "An F shape", "An X shape"], "Co-interior angles are on the same side, between the lines: <b>a C shape</b>."),
        ("What do co-interior angles between parallel lines add up to?", "180°", ["90°", "360°", "They are equal"], "Co-interior angles are <b>supplementary</b>: they add to 180°."),
        ("A transversal crosses two parallel lines. One angle is 72°. Which other angle is NOT possible at either crossing?", "100°", ["72°", "108°", "All of these are possible"], "Every angle is either 72° or 180° − 72° = 108°. <b>100°</b> is not possible."),
        ("Vertically opposite angles are…", "always equal", ["always 180° apart", "only equal for parallel lines", "always 90°"], "Where two lines cross, opposite angles are <b>always equal</b>."),
        ("A railway track has two parallel rails. A road crosses at 64° to one rail. What angle does it make with the other rail, in the same position?", "64°", ["116°", "26°", "128°"], "Corresponding angles are equal: <b>64°</b>."),
        ("In a parallelogram one angle is 70°. Using co-interior angles, what is the next angle around the shape?", "110°", ["70°", "20°", "290°"], "Opposite sides are parallel, so neighbouring angles are co-interior: 180 − 70 = <b>110°</b>."),
        ("Which reason is correct? “Angle <i>x</i> = 55° because…” (the angles form a Z between parallel lines)", "alternate angles are equal", ["co-interior angles add to 180°", "angles in a triangle add to 180°", "angles at a point add to 360°"],
         "A Z shape means <b>alternate angles are equal</b>."),
        ("Two angles form a C shape between parallel lines. One is 95°. What is the other?", "85°", ["95°", "265°", "5°"], "Co-interior: 180 − 95 = <b>85°</b>."),
        ("Ladder rungs are parallel. One rung meets the side rail at 82°. What angle does the next rung make with the rail, on the same side and in the same position?", "82°", ["98°", "8°", "164°"], "Corresponding angles are equal: <b>82°</b>."),
        ("Why must you check for arrows on the lines before using these rules?", "The rules only work when the lines are parallel", ["Arrows show the angle size", "Arrows mean the lines meet", "Arrows show right angles"],
         "Corresponding, alternate and co-interior rules <b>only work when the lines are parallel</b>."),
        ("An angle on a straight line is 38°. What is the other angle on that line?", "142°", ["38°", "52°", "322°"], "Angles on a straight line add to 180°: <b>142°</b>."),
        ("Lines AB and CD are parallel. Angle ABC is 47° and angle BCD is an alternate angle. What is angle BCD?", "47°", ["133°", "43°", "94°"], "Alternate angles are equal: <b>47°</b>."),
        ("In a trapezium the two parallel sides are crossed by a slanted side. One angle on that side is 112°. What is the other angle on the same slanted side?", "68°", ["112°", "22°", "248°"], "They are co-interior: 180 − 112 = <b>68°</b>."),
        ("Corresponding angles are 4<i>x</i> and 3<i>x</i> + 15. Find <i>x</i>.", "15°", ["60°", "45°", "27.5°"], "4<i>x</i> = 3<i>x</i> + 15, so <i>x</i> = <b>15°</b>."),
        ("Co-interior angles are 2<i>x</i> and 3<i>x</i>. What is the larger angle?", "108°", ["72°", "36°", "90°"], "5<i>x</i> = 180, so <i>x</i> = 36 and 3<i>x</i> = <b>108°</b>."),
        ("How many angles are made when one line crosses two parallel lines?", "8", ["4", "6", "2"], "4 at each crossing: <b>8</b> angles, with only two different sizes."),
        ("At one crossing a transversal makes an angle of 90° with a parallel line. What is every angle in the diagram?", "90°", ["45°", "180°", "Some are 90° and some are 270°"], "All eight angles are <b>90°</b>."),
        ("Alternate angles are (5<i>x</i> − 10)° and 65°. Find <i>x</i>.", "15", ["11", "38", "13"], "5<i>x</i> − 10 = 65, so 5<i>x</i> = 75 and <i>x</i> = <b>15</b>."),
    ]
    return [T(q, a[0].upper() + a[1:], [w[0].upper() + w[1:] for w in ws], e) for q, a, ws, e in data]


def body():
    return lesson(
        "<p>When a line (a <b>transversal</b>) crosses two <b>parallel</b> lines, eight angles are made, in two sizes.</p><ul>"
        "<li><b>Corresponding</b> angles (F shape) are equal.</li><li><b>Alternate</b> angles (Z shape) are equal.</li>"
        "<li><b>Co-interior</b> angles (C shape) add up to 180°.</li></ul>"
        "<p>Always give a reason, such as “alternate angles in parallel lines are equal”. If corresponding or alternate angles are "
        "equal, the lines must be parallel.</p>"
        + fig(parallel_svg(65, "UR", "65°", "UR", "x")),
        [("Find <i>x</i> in the diagram above.", ["The angles are corresponding (F shape)."], "<i>x</i> = 65°"),
         ("Co-interior angles are 70° and <i>y</i>. Find <i>y</i>.", ["They add to 180°: 180 − 70."], "<i>y</i> = 110°")],
        ["Thinking co-interior angles are equal. They add up to 180°.",
         "Subtracting from 360° instead of 180°.",
         "Mixing up the F, Z and C shapes.",
         "Using these rules when the lines are not parallel (look for the arrows)."])


def main():
    sets = [S("Naming angle pairs", collect(one_name, 20, R)),
            S("Finding angles in parallel lines", collect(one_parallel, 20, R)),
            S("Equations with parallel lines", collect(one_alg, 20, R)),
            S("Are the lines parallel?", collect(one_check, 20, R)),
            S("Reasons and problems", problems())]
    make(7, "angles-and-parallel-lines", 16, "AC9M7M04",
         "Angles and Parallel Lines: Corresponding, Alternate and Co-interior Angles",
         "Year 7 Parallel Lines Worksheets: Corresponding, Alternate and Co-interior Angles (Free, Answer Key)",
         "Angles and parallel lines",
         "identify corresponding, alternate and co-interior relationships between angles formed when parallel lines are crossed by a transversal; "
         "use them to solve problems and explain reasons",
         "Free Year 7 maths worksheets on angles and parallel lines for the Australian Curriculum (AC9M7M04): corresponding, "
         "alternate and co-interior angles, finding unknown angles, equations and reasons. 100 questions with an answer key.",
         "Corresponding and alternate angles are equal; co-interior angles add up to 180°.",
         "Look for the F, Z and C shapes, and check the lines are parallel.",
         body(),
         [("What are corresponding angles?", "Angles in matching positions at each crossing, like an F shape. When the lines are parallel they are equal."),
          ("What are alternate angles?", "Angles on opposite sides of the transversal, between the parallel lines, like a Z shape. They are equal."),
          ("What are co-interior angles?", "Angles on the same side of the transversal, between the parallel lines, like a C shape. They add up to 180°."),
          ("How can I tell if two lines are parallel?", "If a pair of corresponding or alternate angles are equal, or co-interior angles add to 180°, the lines are parallel.")],
         sets, R)


if __name__ == "__main__":
    main()
