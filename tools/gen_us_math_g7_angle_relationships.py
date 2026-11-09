# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Angle Relationships (7.G.B.5)
  python tools/gen_us_math_g7_angle_relationships.py
Complementary, supplementary, vertical and adjacent angles, and angles around a point.
Wrong answers come from real mistakes: mixing up 90° and 180°, thinking vertical angles add
to 180°, using 360° on a straight line, giving x instead of the angle, and solving the
equation without combining like terms.
"""
import math
import random
from ws_common import (mcq, balance, People, B, fig, figure, svg_wrap, text, line, table, example,
                       write_unit, GREEN, BLUE, RED, INK, X)

R = random.Random(70801)
UPDATED = "2026-11-09"
DEG = "°"


def rays_svg(dirs, labels, label="angle diagram", full_lines=(), right=None):
    """Rays from a centre point. dirs: directions in degrees (0 = right, counter-clockwise).
    labels: [(from_dir, to_dir, text)] placed inside the angle. full_lines: directions drawn
    through the centre as whole lines. right: (from_dir) draws a right-angle box from that ray."""
    W, H, cx, cy, L = 300, 240, 150, 120, 110
    upper = all(0 <= d <= 180 for d in dirs) and all(f == 0 for f in full_lines) and all(0 <= a1 <= 180 and 0 <= a2 <= 180 for a1, a2, _ in labels)
    if upper:
        H, cy = 140, 125
    pt = lambda a, r: (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    s = []
    for a in full_lines:
        x1, y1 = pt(a, L)
        x2, y2 = pt(a + 180, L)
        s.append(line(x1, y1, x2, y2, INK, 2.5))
    for a in dirs:
        x, y = pt(a, L)
        s.append(line(cx, cy, x, y, INK, 2.5))
    if right is not None:
        p1, p2, p3 = pt(right, 16), pt(right + 45, 16 * math.sqrt(2)), pt(right + 90, 16)
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.5'/>" % (p1 + p2 + p3 + (INK,)))
    for k, (a1, a2, t) in enumerate(labels):
        span = (a2 - a1) % 360
        mid = a1 + span / 2
        r_arc = 26 + 6 * (k % 2)
        x1, y1 = pt(a1, r_arc)
        x2, y2 = pt(a2, r_arc)
        large = 1 if span > 180 else 0
        col = [GREEN, BLUE, RED, "#8a5a00"][k % 4]
        s.append("<path d='M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x1, y1, r_arc, r_arc, large, x2, y2, col))
        tx, ty = pt(mid, 62 if span < 50 else 54)
        s.append(text(tx, ty + 5, t, 15, col=col))
    s.append("<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK))
    return svg_wrap(W, H, "".join(s), label)


def par_e(expr):
    """(2x + 10) needs brackets before a degree sign; a single term does not."""
    return "(%s)" % expr if " " in expr else expr


def ang(v):
    return "%d%s" % (v, DEG)


def mc_angle(q, v, ws, e):
    seen = []
    cands = []
    for w in ws:
        if w != v and 0 < w < 360 and w not in seen:
            seen.append(w)
            cands.append((ang(w), w))
    return mcq(q, (ang(v), v), cands, e)


# ------------------------------------------------------------ set 1
def set_words():
    its = []
    for a in [35, 62, 18, 81, 47, 74]:
        its.append(mc_angle("What is the complement of a %s angle?" % ang(a), 90 - a, [180 - a, a, 360 - a, 90 + a],
                            "Complementary angles add to 90%s: 90 − %d = %d. Not %s: that is the supplement (180%s)." % (DEG, a, 90 - a, ang(180 - a), DEG)))
    for a in [70, 125, 33, 148, 96, 15]:
        its.append(mc_angle("What is the supplement of a %s angle?" % ang(a), 180 - a, [90 - a, a, 360 - a, 180 + a],
                            "Supplementary angles add to 180%s: 180 − %d = %d.%s" % (DEG, a, 180 - a, " Not %s: that is the complement (90%s)." % (ang(90 - a), DEG) if a < 90 else "")))
    defs = [("Two angles that add to 90" + DEG + " are called", "complementary", ["supplementary", "vertical", "adjacent"]),
            ("Two angles that add to 180" + DEG + " are called", "supplementary", ["complementary", "vertical", "congruent"]),
            ("When two lines cross, the angles opposite each other are called", "vertical angles", ["adjacent angles", "complementary angles", "right angles"]),
            ("Two angles that share a vertex and a side, but do not overlap, are called", "adjacent angles", ["vertical angles", "complementary angles", "opposite angles"]),
            ("Vertical angles are always", "equal", ["supplementary", "complementary", "right angles"])]
    for qq, good, bad in defs:
        its.append(mcq(qq + " ____.", (good, good), [(b, b) for b in bad],
                       {"complementary": "Complementary angles add to 90" + DEG + ". Tip: C comes before S, and 90 comes before 180.",
                        "supplementary": "Supplementary angles add to 180" + DEG + ", like the two angles on a straight line.",
                        "vertical angles": "Vertical angles are across from each other where two lines cross. They are equal.",
                        "adjacent angles": "Adjacent means next to each other: same vertex, one shared side, no overlap.",
                        "equal": "Vertical angles are always equal (congruent). They add to 180" + DEG + " only if both are 90" + DEG + "."}[good]))
    its.append(mcq("Can two angles of 40" + DEG + " and 50" + DEG + " be complementary?", ("Yes, 40 + 50 = 90.", "y"),
                   [("No, they must be equal.", "n1"), ("No, they add to 180" + DEG + ".", "n2"), ("Only if they are adjacent.", "n3")],
                   "40 + 50 = 90, so they are complementary. Complementary angles do not have to be next to each other."))
    its.append(mcq("Which pair of angles is supplementary?", ("115" + DEG + " and 65" + DEG, "a"),
                   [("115" + DEG + " and 25" + DEG, "b"), ("60" + DEG + " and 30" + DEG, "c"), ("90" + DEG + " and 180" + DEG, "d")],
                   "115 + 65 = 180. 115 + 25 = 140 and 60 + 30 = 90 (complementary)."))
    its.append(mcq("An angle is equal to its complement. How big is it?", ("45" + DEG, 45), [("90" + DEG, 90), ("30" + DEG, 30), ("60" + DEG, 60)],
                   "x + x = 90, so 2x = 90 and x = 45" + DEG + "."))
    return {"title": "Complementary and supplementary angles", "items": its}


# ------------------------------------------------------------ set 2
def set_lines():
    its = []
    # straight line split into two
    for a in [130, 72, 145, 58, 101, 34]:
        svg = rays_svg([a], [(0, a, "?"), (a, 180, ang(180 - a))], "straight line with a ray", full_lines=[0])
        its.append(mc_angle("The angles are on a straight line. Find the missing angle." + fig(svg), a, [180 - a, 360 - (180 - a), 90 - (180 - a) if 180 - a < 90 else a + 10, a - 10],
                            "Angles on a straight line add to 180%s: 180 − %d = %d%s. Not %s: a straight line is 180%s, not 360%s." % (DEG, 180 - a, a, DEG, ang(360 - (180 - a)), DEG, DEG)))
    # straight line split into three
    for a, b in [(40, 65), (50, 90), (35, 110), (70, 45)]:
        c = 180 - a - b
        svg = rays_svg([a, a + b], [(0, a, ang(a)), (a, a + b, ang(b)), (a + b, 180, "?")], "straight line split into three angles", full_lines=[0])
        its.append(mc_angle("The angles are on a straight line. Find the missing angle." + fig(svg), c, [360 - a - b, 90 - a if a < 90 else c + 20, a + b, c + 10],
                            "%d + %d + ? = 180, so ? = 180 − %d = %d%s." % (a, b, a + b, c, DEG)))
    # right angle split
    for a in [28, 55, 63, 17, 41]:
        svg = rays_svg([0, 90, a], [(0, a, ang(a)), (a, 90, "?")], "right angle split into two angles", right=None)
        its.append(mc_angle("The two angles make a right angle. Find the missing angle." + fig(svg), 90 - a, [180 - a, a, 90 + a, 100 - a],
                            "A right angle is 90%s: 90 − %d = %d%s. Not %s: that uses 180%s." % (DEG, a, 90 - a, DEG, ang(180 - a), DEG)))
    # around a point
    for a, b, c in [(120, 95, 80), (90, 150, 60), (110, 110, 75), (100, 135, 45), (85, 140, 70)]:
        d = 360 - a - b - c
        dirs = [0, a, a + b, a + b + c]
        svg = rays_svg(dirs, [(0, a, ang(a)), (a, a + b, ang(b)), (a + b, a + b + c, ang(c)), (a + b + c, 360, "?")], "angles around a point")
        its.append(mc_angle("The angles are around a point. Find the missing angle." + fig(svg), d, [180 - (a + b + c) % 180, 360 - a - b, d + 10, d - 10],
                            "Angles around a point add to 360%s: %d + %d + %d = %d, and 360 − %d = %d%s." % (DEG, a, b, c, a + b + c, a + b + c, d, DEG)))
    return {"title": "Straight lines, right angles and around a point", "items": its}


# ------------------------------------------------------------ set 3
def set_vertical():
    its = []
    for a in [40, 65, 110, 32, 125, 78, 140, 55]:
        # lines at 0 and a; angle a between them, ask the vertical one
        svg = rays_svg([], [(0, a, ang(a)), (180, 180 + a, "?")], "two crossing lines", full_lines=[0, a])
        its.append(mc_angle("Two lines cross. Find the angle marked ?." + fig(svg), a, [180 - a, 90 - a, a + 10, a - 10],
                            "The angle marked ? is across from the %s angle, so they are vertical angles. Vertical angles are equal: %s. Not %s: that is the angle next to it (supplementary)." % (
                                ang(a), ang(a), ang(180 - a))))
    for a in [50, 120, 74, 36, 138, 95]:
        svg = rays_svg([], [(0, a, ang(a)), (a, 180, "?")], "two crossing lines", full_lines=[0, a])
        its.append(mc_angle("Two lines cross. Find the angle marked ?." + fig(svg), 180 - a, [a, 90 - a, 180 - a + 10, 180 - a - 10, 270 - a],
                            "The two angles are next to each other on a straight line, so they add to 180%s: 180 − %d = %d%s." % (DEG, a, 180 - a, DEG)))
    # all four angles
    for a in [60, 145, 48]:
        its.append(mcq("Two lines cross. One angle is %s. What are the other three angles?" % ang(a),
                       ("%s, %s and %s" % (ang(180 - a), ang(a), ang(180 - a)), "a"),
                       [("%s, %s and %s" % (ang(a), ang(a), ang(a)), "b"), ("%s, %s and %s" % (ang(90 - a) if a < 90 else ang(360 - a), ang(a), ang(180 - a)), "c"),
                        ("%s, %s and %s" % (ang(180 - a), ang(180 - a), ang(180 - a)), "d")],
                       "The vertical angle is also %s. The two angles next to it are 180 − %d = %d%s each." % (ang(a), a, 180 - a, DEG)))
    its.append(mcq("Two lines cross and one angle is 90" + DEG + ". What are the other angles?", ("All 90" + DEG, "a"),
                   [("90" + DEG + ", 180" + DEG + " and 90" + DEG, "b"), ("45" + DEG + " each", "c"), ("It cannot be found", "d")],
                   "The vertical angle is 90" + DEG + ", and the angles next to it are 180 − 90 = 90" + DEG + ". The lines are perpendicular."))
    its.append(mcq("Two lines cross. The sum of two vertical angles is 100" + DEG + ". How big is each of them?", ("50" + DEG, 50),
                   [("100" + DEG, 100), ("80" + DEG, 80), ("130" + DEG, 130)], "Vertical angles are equal, so each is 100 ÷ 2 = 50" + DEG + "."))
    its.append(mcq("Two lines cross. One angle is 3 times as big as the angle next to it. What is the smaller angle?", ("45" + DEG, 45),
                   [("60" + DEG, 60), ("30" + DEG, 30), ("135" + DEG, 135)], "The two angles are supplementary: x + 3x = 180, so 4x = 180 and x = 45" + DEG + "."))
    return {"title": "Vertical and adjacent angles", "items": its}


# ------------------------------------------------------------ set 4
def set_equations():
    its = []
    # (p x + q) + known = total
    cases = [  # p, q, known, total
        (1, 0, 50, 90), (2, 0, 40, 180), (1, 15, 35, 90), (3, 0, 60, 180), (2, 10, 50, 90), (4, 20, 40, 180),
        (5, -10, 40, 180), (3, 6, 24, 90)]
    for p, q, known, total in cases:
        x = (total - known - q) / p
        assert x == int(x)
        x = int(x)
        expr = ("%s" % X if p == 1 else "%d%s" % (p, X)) + ("" if q == 0 else (" + %d" % q if q > 0 else " − %d" % -q))
        kind = "complementary" if total == 90 else "supplementary"
        wrong_total = 180 if total == 90 else 90
        wx = (wrong_total - known - q) / p
        ws = [p * x + q, (total - known) // p if (total - known) % p == 0 else x + 5, (total + known - q) // p if (total + known - q) % p == 0 else x + 3]
        if wx > 0 and wx == int(wx):
            ws.insert(0, int(wx))
        e = "The angles are %s, so %s + %d = %d. Subtract %d: %s = %d." % (kind, par_e(expr), known, total, known + q,
                                                                     "%d%s" % (p, X) if p != 1 else X, total - known - q)
        if p != 1:
            e += " Divide by %d: %s = %d." % (p, X, x)
        cands = []
        for w in ws:
            if w != x and w > 0 and w not in [c[1] for c in cands]:
                cands.append((str(w), w))
        cands += [(str(x + 1), x + 1), (str(x * 2), x * 2)]
        its.append(mcq("Angles of %s%s and %s are %s. What is the value of %s?" % (par_e(expr), DEG, ang(known), kind, X), (str(x), x), cands,
                       e + (" Not %d: that is the size of the angle, not %s." % (p * x + q, X) if p * x + q != x else "")))
    # two expressions
    for p1, q1, p2, q2, total in [(1, 20, 1, 40, 180), (2, 0, 3, 0, 90), (3, 10, 2, 20, 180), (1, 0, 4, 10, 90), (5, 0, 1, 0, 180), (2, 5, 1, 25, 90)]:
        x = (total - q1 - q2) / (p1 + p2)
        assert x == int(x)
        x = int(x)
        e1 = ("%s" % X if p1 == 1 else "%d%s" % (p1, X)) + (" + %d" % q1 if q1 else "")
        e2 = ("%s" % X if p2 == 1 else "%d%s" % (p2, X)) + (" + %d" % q2 if q2 else "")
        kind = "complementary" if total == 90 else "supplementary"
        big = max(p1 * x + q1, p2 * x + q2)
        comb = "%d%s" % (p1 + p2, X) + (" + %d" % (q1 + q2) if q1 + q2 else "")
        mid = ("so %d%s = %d and " % (p1 + p2, X, total - q1 - q2)) if q1 + q2 else "so "
        e = "%s + %s = %d. Combine like terms: %s = %d, %s%s = %d. The angles are %s and %s." % (
            e1, e2, total, comb, total, mid, X, x, ang(p1 * x + q1), ang(p2 * x + q2))
        ws = [big, (total - q1 - q2) // max(p1, p2), total // (p1 + p2) if total % (p1 + p2) == 0 else x + 4, x + 5, x * 2]
        cands = []
        for w in ws:
            if w != x and w > 0 and w not in [c[1] for c in cands]:
                cands.append((str(w), w))
        its.append(mcq("Angles of %s%s and %s%s are %s. What is %s?" % (par_e(e1), DEG, par_e(e2), DEG, kind, X), (str(x), x), cands, e))
    # vertical angles equation
    for p1, q1, p2, q2 in [(2, 10, 1, 40), (3, 0, 1, 50), (4, -20, 2, 30), (5, 10, 3, 30), (3, 15, 1, 55), (6, 0, 4, 24)]:
        x = (q2 - q1) // (p1 - p2)
        e1 = "%d%s" % (p1, X) + ("" if q1 == 0 else (" + %d" % q1 if q1 > 0 else " − %d" % -q1))
        e2 = ("%s" % X if p2 == 1 else "%d%s" % (p2, X)) + (" + %d" % q2 if q2 else "")
        v = p1 * x + q1
        its.append(mc_angle("Two lines cross. Vertical angles measure (%s)%s and (%s)%s. How big is each angle?" % (e1, DEG, e2, DEG), v,
                            [x, 180 - v, v + 10, (180 - q1 - q2) // (p1 + p2) * p1 + q1 if (180 - q1 - q2) % (p1 + p2) == 0 else v - 10],
                            "Vertical angles are equal: %s = %s, so %s = %d. Each angle is %s = %s." % (e1, e2, X, x, e1.replace(X, "(%d)" % x), ang(v))))
    return {"title": "Write and solve equations", "items": its}


# ------------------------------------------------------------ set 5
def set_problems():
    its = []
    its.append(mc_angle("A ladder leans against a wall. It makes a 68" + DEG + " angle with the ground. What angle does it make with the wall? (The wall meets the ground at 90" + DEG + ".)",
                        22, [112, 68, 292, 158], "The ground, wall and ladder make a triangle with a right angle. The two other angles are complementary: 90 − 68 = 22" + DEG + "."))
    its.append(mc_angle("A road crosses a railway track. One angle between them is 57" + DEG + ". What is the angle next to it on the same side of the track?",
                        123, [57, 33, 303, 133], "The two angles are on a straight line: 180 − 57 = 123" + DEG + "."))
    its.append(mc_angle("A pizza is cut into slices from the centre. Three slices have angles 70" + DEG + ", 85" + DEG + " and 95" + DEG + ". The rest is one slice. What is its angle?",
                        110, [290, 70, 30, 120], "Angles around the centre add to 360" + DEG + ": 360 − (70 + 85 + 95) = 360 − 250 = 110" + DEG + "."))
    its.append(mc_angle("The hands of a clock at 3:00 make a right angle. A second hand splits it into two angles. One is 34" + DEG + ". What is the other?",
                        56, [146, 34, 326, 66], "The two angles make 90" + DEG + ": 90 − 34 = 56" + DEG + "."))
    its.append(mc_angle("Two angles are supplementary. One is 4 times the other. What is the larger angle?", 144,
                        [36, 72, 180, 120], "x + 4x = 180, so 5x = 180 and x = 36. The larger angle is 4 × 36 = 144" + DEG + ". Not 36" + DEG + ": that is the smaller angle."))
    its.append(mc_angle("Two angles are complementary. One is 20" + DEG + " more than the other. What is the smaller angle?", 35,
                        [55, 70, 80, 45], "x + (x + 20) = 90, so 2x = 70 and x = 35" + DEG + ". The other is 55" + DEG + "."))
    its.append(mc_angle("Two angles are supplementary. One is 30" + DEG + " less than twice the other. What is the smaller angle?", 70,
                        [110, 50, 75, 40], "x + (2x − 30) = 180, so 3x = 210 and x = 70" + DEG + ". The other is 2(70) − 30 = 110" + DEG + "."))
    its.append(mc_angle("A door is opened so it makes a 115" + DEG + " angle with the wall on one side. What angle does it make with the wall on the other side?",
                        65, [115, 25, 245, 75], "The wall is a straight line, so the two angles add to 180" + DEG + ": 180 − 115 = 65" + DEG + "."))
    its.append(mc_angle("A kite string makes a 38" + DEG + " angle with the ground. What is the angle between the string and a pole standing straight up from the same point?",
                        52, [142, 38, 322, 62], "The pole and the ground make 90" + DEG + ". 90 − 38 = 52" + DEG + "."))
    its.append(mc_angle("A fan has 5 blades spaced evenly around the centre. What is the angle between two blades next to each other?",
                        72, [36, 90, 60, 180], "The blades split 360" + DEG + " into 5 equal parts: 360 ÷ 5 = 72" + DEG + ". Not 36" + DEG + ": that splits 180" + DEG + "."))
    its.append(mc_angle("Three rays split a straight line into angles of x" + DEG + ", 2x" + DEG + " and 3x" + DEG + ". What is the largest angle?",
                        90, [30, 60, 180, 120], "x + 2x + 3x = 180, so 6x = 180 and x = 30. The largest is 3 × 30 = 90" + DEG + "."))
    its.append(mc_angle("The angles around a point are x" + DEG + ", x" + DEG + ", 100" + DEG + " and 120" + DEG + ". What is x?",
                        70, [140, 40, 30, 80], "x + x + 100 + 120 = 360, so 2x = 140 and x = 70" + DEG + "."))
    its.append(mc_angle("An angle's supplement is 3 times its complement. How big is the angle?", 45,
                        [135, 30, 60, 90], "180 − x = 3(90 − x). So 180 − x = 270 − 3x, which gives 2x = 90 and x = 45" + DEG + ". Check: 135 = 3 × 45."))
    its.append(mc_angle("A ramp makes a 12" + DEG + " angle with the flat ground. What is the angle between the ramp and the ground on the other side of the ramp's bottom edge?",
                        168, [78, 12, 348, 102], "The ground is a straight line, so 180 − 12 = 168" + DEG + "."))
    its.append(mc_angle("Two streets cross. One corner has an angle of (2x + 30)" + DEG + ". The corner across from it is (4x − 10)" + DEG + ". How big is that corner angle?",
                        70, [20, 110, 40, 140], "Vertical angles are equal: 2x + 30 = 4x − 10, so 40 = 2x and x = 20. The angle is 2(20) + 30 = 70" + DEG + ". Not 20: that is x."))
    its.append(mc_angle("An angle is 40" + DEG + " more than its supplement. How big is the angle?", 110,
                        [70, 140, 65, 40], "x + (x − 40) = 180, so 2x = 220 and x = 110" + DEG + ". Its supplement is 70" + DEG + "."))
    its.append(mc_angle("A beam of light hits a flat mirror. It comes in at 35" + DEG + " to the mirror and leaves at 35" + DEG + " on the other side. What is the angle between the two beams?",
                        110, [70, 145, 35, 290], "The three angles are on the straight mirror: 35 + ? + 35 = 180, so ? = 110" + DEG + "."))
    its.append(mc_angle("A wheel has 8 spokes evenly spaced. What is the angle between two spokes next to each other?", 45,
                        [22, 90, 40, 60], "360 ÷ 8 = 45" + DEG + "."))
    its.append(mc_angle("A ceiling fan blade turns from pointing north to pointing east. Then it turns 30" + DEG + " more. How far has it turned in all?", 120,
                        [60, 90, 150, 30], "North to east is a quarter turn, 90" + DEG + ". 90 + 30 = 120" + DEG + "."))
    its.append(mc_angle("Angle A and angle B are complementary. Angle B and angle C are supplementary. Angle A is 25" + DEG + ". What is angle C?", 115,
                        [65, 155, 25, 90], "B = 90 − 25 = 65" + DEG + ". C = 180 − 65 = 115" + DEG + "."))
    return {"title": "Word problems", "items": its}


def body():
    s1 = rays_svg([60], [(0, 60, "60" + DEG), (60, 180, "120" + DEG)], "supplementary angles on a straight line", full_lines=[0])
    s2 = rays_svg([], [(0, 50, "50" + DEG), (180, 230, "50" + DEG)], "vertical angles", full_lines=[0, 50])
    rows = [["Complementary", "add to 90" + DEG, "35" + DEG + " and 55" + DEG],
            ["Supplementary", "add to 180" + DEG + " (a straight line)", "60" + DEG + " and 120" + DEG],
            ["Vertical", "across from each other, equal", "50" + DEG + " and 50" + DEG],
            ["Around a point", "add to 360" + DEG, "100" + DEG + " + 120" + DEG + " + 140" + DEG]]
    return ("<h2>Angle pairs</h2><p>Many angle problems use just three facts: a right angle is 90" + DEG + ", a straight line is 180" + DEG + ", and a full turn is 360" + DEG + ".</p>"
            + table(["Name", "Rule", "Example"], rows)
            + figure(s1, "On a straight line: 60" + DEG + " + 120" + DEG + " = 180" + DEG + ".")
            + figure(s2, "Vertical angles are equal.")
            + example("Angles of (2" + X + " + 10)" + DEG + " and 50" + DEG + " are supplementary. Find " + X + ".",
                      ["Write an equation: 2" + X + " + 10 + 50 = 180.", "Combine: 2" + X + " + 60 = 180, so 2" + X + " = 120.", "Divide: " + X + " = 60."], X + " = 60")
            + "<h2>Common mistakes</h2><ul><li>Mixing up the totals: complementary is 90" + DEG + ", supplementary is 180" + DEG + ".</li>"
            "<li>Adding vertical angles to 180" + DEG + ": vertical angles are equal. The angles next to each other add to 180" + DEG + ".</li>"
            "<li>Stopping at " + X + ": if the question asks for the angle, put " + X + " back into the expression.</li></ul>")


def main():
    sets = [set_words(), set_lines(), set_vertical(), set_equations(), set_problems()]
    balance(sets, R)
    unit = {
        "slug": "angle-relationships",
        "title": "Angle Relationships",
        "seo_title": "Grade 7 Angle Relationships Worksheets: Complementary, Supplementary, Vertical and Adjacent Angles",
        "short_title": "Angle relationships",
        "domain": "Geometry",
        "standard_code": "7.G.B.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/G/B/5/",
        "standard_text": "Use facts about supplementary, complementary, vertical, and adjacent angles in a multi-step problem to write and solve simple equations for an unknown angle in a figure.",
        "meta_desc": "Free Grade 7 angle relationships worksheets: complementary, supplementary, vertical and adjacent angles, angles on a line and around a point, and equations for unknown angles. 100 practice questions with diagrams and an answer key.",
        "key_big": "Complementary angles add to 90°. Supplementary angles add to 180°. Vertical angles are equal.",
        "key_sub": "Angles on a straight line add to 180° and angles around a point add to 360°. Write an equation, then solve it.",
        "body_html": body(),
        "faq": [
            {"q": "What is the difference between complementary and supplementary angles?", "a": "Complementary angles add to 90°, like 30° and 60°. Supplementary angles add to 180°, like 30° and 150°."},
            {"q": "What are vertical angles?", "a": "When two lines cross, the angles across from each other are vertical angles. They are always equal."},
            {"q": "What are adjacent angles?", "a": "Angles that share a vertex and one side without overlapping. Two adjacent angles on a straight line are supplementary."},
            {"q": "How do I find an unknown angle with x?", "a": "Use the angle fact to write an equation, such as (2x + 10) + 50 = 180. Solve for x, then put x back in if the question asks for the angle."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 8,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
