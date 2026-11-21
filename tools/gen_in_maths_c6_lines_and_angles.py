# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 2: Lines and Angles
  python3 tools/gen_in_maths_c6_lines_and_angles.py
Points, lines, line segments and rays (naming and counting), angles as turns, types of angles (acute, right, obtuse,
straight, reflex), angles on a clock face and on compass turns, and angles on a straight line and around a point.
Wrong answers come from real mistakes: confusing a ray with a segment, calling 90° obtuse, and reading the wrong scale.
"""
import random
from in_common import num, unit, T, QN, adopt, gb
import gen_us_math_ge_points_lines_and_planes as pl
import gen_uk_maths_y7_angles as an

R = random.Random(906002)
adopt(pl, R)
adopt(an, R)
TYPES = [("acute", 1, 89), ("right", 90, 90), ("obtuse", 91, 179), ("straight", 180, 180), ("reflex", 181, 359)]


def one_type(r):
    name, lo, hi = r.choice(TYPES)
    a = r.randint(lo, hi)
    return T("What type of angle is %d°?" % a, name.capitalize() + " angle", [t[0].capitalize() + " angle" for t in TYPES if t[0] != name][:3],
             "%s: <b>%s angle</b>." % ({"acute": "Less than 90°", "right": "Exactly 90°", "obtuse": "Between 90° and 180°", "straight": "Exactly 180°", "reflex": "Between 180° and 360°"}[name], name))


def one_turn(r):
    kind = r.choice(["turn", "clock", "clock", "compass"])
    if kind == "turn":
        t, d = r.choice([("a quarter turn", 90), ("a half turn", 180), ("three-quarters of a turn", 270), ("a full turn", 360), ("one-third of a turn", 120), ("one-sixth of a turn", 60)])
        return QN("How many degrees is %s?" % t, d, [d // 2, 360 - d if 360 - d != d else d + 90, d + 90], "A full turn is 360°, so %s is <b>%d°</b>." % (t, d), unit="°")
    if kind == "clock":
        h = r.randint(1, 11)
        a = 30 * min(h, 12 - h)
        return QN("What is the smaller angle between the hands of a clock at %d o'clock?" % h, a, [h * 5, 360 - a, a + 30], "Each hour mark is 30°. %d hours apart → <b>%d°</b>." % (min(h, 12 - h), a), unit="°")
    dirs = ["North", "East", "South", "West"]
    i = r.randrange(4)
    k = r.randint(1, 3)
    cw = r.random() < 0.5
    j = (i + k) % 4 if cw else (i - k) % 4
    return T("You face %s and turn %d° %s. Which way do you face now?" % (dirs[i], 90 * k, "clockwise" if cw else "anticlockwise"), dirs[j],
             [d for d in dirs if d != dirs[j]], "Each 90° is a quarter turn. You face <b>%s</b>." % dirs[j])


def main():
    unit(6, 0, 2, "lines-and-angles", 2, "G", "Lines and Angles: Points, Rays, Segments and Angles", "lines and angles",
         "Points, lines, line segments and rays; angles as turns; measuring angles; types of angles (acute, right, obtuse, straight and reflex) (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Lines and Angles worksheet (Ganita Prakash Chapter 2): points, lines, rays and segments, types of angles, turns, clocks and angles on a line. 100 questions with answers.",
         "A right angle is 90°; a straight angle is 180°", "Acute < 90° < obtuse < 180° < reflex < 360°.",
         "<p>A <b>line segment</b> has two endpoints, a <b>ray</b> has one endpoint and goes on in one direction, and a <b>line</b> goes on in both directions.</p>"
         "<p>An <b>angle</b> is made by two rays from a common point (the vertex). It measures the amount of turn: a full turn is 360°, a half turn 180°, a quarter turn 90°.</p>"
         "<p>Types: <b>acute</b> (less than 90°), <b>right</b> (90°), <b>obtuse</b> (between 90° and 180°), <b>straight</b> (180°), <b>reflex</b> (more than 180°).</p>",
         [("What type of angle is 135°?", ["Between 90° and 180°"], "Obtuse"),
          ("Angles on a straight line are x and 65°. Find x.", ["180° − 65°"], "115°")],
         ["Calling a ray a line segment (a ray has only one endpoint).", "Calling 90° obtuse or acute. It is a right angle.", "Reading the wrong scale of the protractor (40° instead of 140°)."],
         [("What is the difference between a line, a ray and a segment?", "A segment has two endpoints, a ray has one, and a line has none — it goes on in both directions."),
          ("What are the types of angles?", "Acute (less than 90°), right (90°), obtuse (90° to 180°), straight (180°) and reflex (180° to 360°)."),
          ("How many degrees are in a full turn?", "360°.")],
         [("Points, lines, rays and segments", [(gb(pl.one_name), 12), (gb(pl.one_count), 8)]),
          ("Types of angles", [(one_type, 20)]),
          ("Angles as turns", [(one_turn, 20)]),
          ("Angles on a straight line", [(gb(an.one_line), 20)]),
          ("Angles around a point", [(gb(an.one_point), 14), (one_turn, 6)])], R)


if __name__ == "__main__":
    main()
