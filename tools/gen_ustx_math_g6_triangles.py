# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Triangle Properties: Angles and Side Lengths (TEKS 6.8A)
  python3 tools/gen_ustx_math_g6_triangles.py
The angle sum of a triangle, finding a missing angle, whether three lengths can make a triangle, possible third
sides, and the relationship between the largest angle and the longest side.
Wrong answers come from real mistakes: using 360° instead of 180°, adding only two sides when the third is the
longest, and matching the largest angle with the wrong side.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import math
tx_common.GRADE = "grade-6"

INK = "#1f2937"


def tri_pts(A, B):
    C = 180 - A - B
    a = math.radians(A)
    b = math.radians(B)
    # base from (0, 0) to (1, 0); third vertex where the two angle rays meet
    t = math.sin(b) / math.sin(math.radians(C))
    return [(0.0, 0.0), (1.0, 0.0), (t * math.cos(a), t * math.sin(a))]


def tri_svg(A, B, labels, names=("A", "B", "C"), sides=None):
    pts = tri_pts(A, B)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    sc = min(260 / w, 150 / h)
    P = [(30 + (x - min(xs)) * sc, 175 - (y - min(ys)) * sc) for x, y in pts]
    cx, cy = sum(p[0] for p in P) / 3, sum(p[1] for p in P) / 3
    s = ["<svg viewBox='0 0 320 205' width='320' role='img' aria-label='triangle'><polygon points='%s' fill='#dbeafe' stroke='%s' stroke-width='2'/>" % (" ".join("%.1f,%.1f" % p for p in P), INK)]
    for (x, y), lab, nm, ang in zip(P, labels, names, (A, B, 180 - A - B)):
        dx, dy = cx - x, cy - y
        d = math.hypot(dx, dy) or 1
        off = 30 if ang >= 50 else 30 + (50 - ang) * 0.9
        s.append("<text x='%.1f' y='%.1f' font-size='14' text-anchor='middle' fill='%s'>%s</text>" % (x + dx / d * off, y + dy / d * off + 5, INK, lab))
        s.append("<text x='%.1f' y='%.1f' font-size='14' font-weight='bold' text-anchor='middle' fill='%s'>%s</text>" % (x - dx / d * 13, y - dy / d * 13 + 5, INK, nm))
    if sides:
        for i, lab in enumerate(sides):
            (x1, y1), (x2, y2) = P[i], P[(i + 1) % 3]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = mx - cx, my - cy
            d = math.hypot(dx, dy) or 1
            s.append("<text x='%.1f' y='%.1f' font-size='14' text-anchor='middle' fill='#b45309'>%s</text>" % (mx + dx / d * 16, my + dy / d * 16 + 5, lab))
    s.append("</svg>")
    return fig("".join(s))


def angles(r):
    A = r.randint(25, 110)
    B = r.randint(25, 150 - A)
    C = 180 - A - B
    if C < 20 or len({A, B, C}) < 3:
        return None
    return A, B, C


def one_missing(r):
    t = angles(r)
    if not t:
        return None
    A, B, C = t
    i = r.randrange(3)
    labs = ["%d°" % v for v in t]
    labs[i] = "?"
    rot = r.randrange(3)
    order = [(0, 1, 2), (1, 2, 0), (2, 0, 1)][rot]
    vals = [t[j] for j in order]
    pic = tri_svg(vals[0], vals[1], [labs[j] for j in order])
    known = [v for j, v in enumerate(t) if j != i]
    ans = t[i]
    return mcq(pic + "What is the measure of the missing angle?", "%d°" % ans, ["%d°" % (360 - sum(known)), "%d°" % (180 - known[0]), "%d°" % (sum(known))],
               "The angles of a triangle add to 180°. 180° − %d° − %d° = <b>%d°</b>." % (known[0], known[1], ans))


def one_sum(r):
    kind = r.choice(["can", "can", "right", "equal"])
    if kind == "can":
        t = angles(r)
        if not t:
            return None
        bad = []
        for _ in range(3):
            a, b = r.randint(30, 100), r.randint(30, 100)
            c = r.choice([190, 170, 200, 160]) - a - b
            if c > 0 and a + b + c != 180:
                bad.append((a, b, c))
        if len(bad) < 3:
            return None
        return mcq("Which set of angle measures could be the angles of a triangle?", "%d°, %d°, %d°" % t, ["%d°, %d°, %d°" % b for b in bad],
                   "%d + %d + %d = 180, so <b>%d°, %d°, %d°</b> works. The others do not add to 180°." % (t + t))
    if kind == "right":
        a = r.randint(20, 70)
        return mcq("A right triangle has one angle of %d°. What is the third angle?" % a, "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % (270 - a), "%d°" % (90 + a)],
                   "A right angle is 90°. 180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    a = r.randint(20, 80)
    return mcq("A triangle has two equal angles. The third angle is %d°. What is each of the equal angles?" % (180 - 2 * a), "%d°" % a, ["%d°" % (180 - a), "%d°" % (2 * a), "%d°" % (180 - (180 - 2 * a))],
               "180° − %d° = %d°. %d° ÷ 2 = <b>%d°</b>." % (180 - 2 * a, 2 * a, 2 * a, a))


def one_sides(r):
    good = None
    while not good:
        a, b = r.randint(3, 15), r.randint(3, 15)
        c = r.randint(abs(a - b) + 1, a + b - 1)
        good = (a, b, c) if len({a, b, c}) == 3 else None
    bad = []
    for _ in range(20):
        x, y = r.randint(2, 10), r.randint(2, 10)
        z = x + y + r.choice([0, 1, 3, 5])
        t = tuple(r.sample([x, y, z], 3))
        if len(set(t)) == 3 and t not in bad:
            bad.append(t)
        if len(bad) == 3:
            break
    if len(bad) < 3:
        return None
    if r.random() < 0.5:
        g = sorted(good)
        return mcq("Which three lengths can make a triangle? (All lengths are in centimeters.)", "%d, %d, %d" % good, ["%d, %d, %d" % t for t in bad],
                   "The two shorter sides must add to more than the longest side: %d + %d = %d &gt; %d. So <b>%d, %d, %d</b> works." % (g[0], g[1], g[0] + g[1], g[2], good[0], good[1], good[2]))
    t = bad[0]
    s = sorted(t)
    return mcq("Can sides of %d in, %d in and %d in make a triangle?" % t, "No, because %d + %d is not greater than %d" % (s[0], s[1], s[2]),
               ["Yes, because any three lengths make a triangle", "Yes, because %d + %d + %d is more than 10" % t, "No, because the sides are all different"],
               "%d + %d = %d, which is not greater than %d. The two short sides cannot meet, so <b>no triangle</b>." % (s[0], s[1], s[0] + s[1], s[2]))


def one_third(r):
    a, b = r.sample(range(3, 16), 2)
    lo, hi = abs(a - b), a + b
    good = r.randint(lo + 1, hi - 1)
    bad = [lo, hi, hi + r.randint(1, 5), max(1, lo - r.randint(1, 2))]
    bad = [x for x in dict.fromkeys(bad) if x != good and x > 0][:3]
    if len(bad) < 3:
        return None
    return mcq("Two sides of a triangle are %d m and %d m. Which could be the length of the third side?" % (a, b), "%d m" % good, ["%d m" % x for x in bad],
               "The third side must be more than %d − %d = %d and less than %d + %d = %d. <b>%d m</b> works." % (max(a, b), min(a, b), lo, a, b, hi, good))


def one_largest(r):
    t = angles(r)
    if not t:
        return None
    A, B, C = t
    rot = r.randrange(3)
    names = ["A", "B", "C"]
    pic = tri_svg(A, B, ["%d°" % A, "%d°" % B, "%d°" % C])
    opp = {0: "BC", 1: "AC", 2: "AB"}
    big = r.random() < 0.6
    i = max(range(3), key=lambda j: t[j]) if big else min(range(3), key=lambda j: t[j])
    adj = [s for s in ["AB", "BC", "AC"] if s != opp[i]]
    return mcq(pic + "Which side of triangle ABC is the %s?" % ("longest" if big else "shortest"), opp[i], adj + [opp[(i + 1) % 3]] if opp[(i + 1) % 3] not in adj else adj + ["They are all equal"],
               "The %s side is across from the %s angle. Angle %s is %d°, so the side is <b>%s</b>." % ("longest" if big else "shortest", "largest" if big else "smallest", names[i], t[i], opp[i]))


def one_sideangle(r):
    s = sorted(r.sample(range(4, 20), 3))
    if s[0] + s[1] <= s[2]:
        return None
    sides = {"AB": s[0], "BC": s[1], "AC": s[2]}
    keys = list(sides)
    r.shuffle(keys)
    vals = dict(zip(keys, s))
    big = r.random() < 0.6
    k = max(vals, key=vals.get) if big else min(vals, key=vals.get)
    opp = {"BC": "A", "AC": "B", "AB": "C"}
    txt = ", ".join("%s = %d cm" % (x, vals[x]) for x in ["AB", "BC", "AC"])
    return mcq("In triangle ABC, %s. Which angle is the %s?" % (txt, "largest" if big else "smallest"), "Angle " + opp[k], ["Angle " + a for a in "ABC" if a != opp[k]] + ["All the angles are equal"],
               "The %s angle is across from the %s side, %s = %d cm. That is <b>angle %s</b>." % ("largest" if big else "smallest", "longest" if big else "shortest", k, vals[k], opp[k]))


def build():
    sets, R = build_sets([
        ("Find the missing angle", [("collect", one_missing, 20)]),
        ("The angle sum is 180°", [("collect", one_sum, 20)]),
        ("Can the lengths make a triangle?", [("collect", one_sides, 20)]),
        ("Possible third sides", [("collect", one_third, 20)]),
        ("Largest angle and longest side", [("collect", one_largest, 10), ("collect", one_sideangle, 10)]),
    ], 66016)
    finish(sets, R)
    body = lesson('<ul><li>The three angles of every triangle add to <b>180°</b>.</li><li>Three lengths make a triangle only if the <b>two shorter sides add to more than the longest side</b>.</li><li>The third side must be longer than the difference and shorter than the sum of the other two sides.</li><li>The <b>largest angle</b> is across from the <b>longest side</b>; the smallest angle is across from the shortest side.</li></ul>',
        [example("Angles 48° and 75°. Find the third.", ["48 + 75 = 123", "180 − 123"], "57°"), example("Can 4, 6 and 11 make a triangle?", ["4 + 6 = 10", "10 is not greater than 11"], "no")],
        [['Using 360° instead of 180°', '360° is for a full turn or a quadrilateral. A triangle has 180°.'], ['Checking only one pair of sides', 'Check that the two shortest sides add to more than the longest.'], ['Matching the largest angle with a side next to it', 'The longest side is across from the largest angle.']])
    faq = [('What does TEKS 6.8A ask?', 'Extend previous knowledge of triangles and their properties to include the sum of angles of a triangle, the relationship between the lengths of sides and measures of angles in a triangle, and determining when three lengths form a triangle.'), ('Why do the angles add to 180°?', 'Tear off the three corners and line them up. They make a straight angle, 180°.'), ('Can a triangle have two right angles?', 'No. Two right angles already make 180°, leaving 0° for the third.'), ('Do 5, 5 and 10 make a triangle?', 'No. 5 + 5 = 10 is not greater than 10, so the sides lie flat.')]
    make('triangle-properties', 16, 'Geometry and Measurement', '6.8A',
         '6.8A extend previous knowledge of triangles and their properties to include the sum of angles of a triangle, the relationship between the lengths of sides and measures of angles in a triangle, and determining when three lengths form a triangle',
         'Triangle Properties: Angles and Side Lengths', 'Triangle Properties',
         'Free Grade 6 triangle worksheets for Texas TEKS 6.8A: angle sum of a triangle, missing angles, triangle side lengths, possible third sides and largest angle versus longest side. 100 questions with answers.',
         'Angles add to 180°; the two shorter sides must add to more than the longest.', 'The largest angle is across from the longest side.',
         body, faq, sets, seo_title='Grade 6 Triangle Properties Worksheets: Angle Sum and Side Lengths (TEKS 6.8A, STAAR)')


if __name__ == "__main__":
    build()
