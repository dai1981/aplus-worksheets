# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 9: Some Applications of Trigonometry — Heights and Distances (CBSE Unit V Trigonometry)
  python3 tools/gen_in_maths_c10_some_applications_of_trigonometry.py
Angles of elevation and depression with 30°, 45° and 60°: finding a height, finding a distance, angles of depression,
problems with two right triangles (moving closer, a flagstaff on a building, two poles), and situations (kites, ladders,
ramps, shadows) with exact answers in surd form or using √3 = 1.73.
Wrong answers come from real mistakes: tan swapped with cot (h = d/tan θ), using sin for a horizontal distance,
the angle of depression placed at the bottom, and tan 30° = √3.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, fv, People, svg_wrap, text, line, INK, RED, BLUE, FILL

R = random.Random(910009)
P = People(R)
TAN = {30: (F(1, 3), 1), 45: (F(1), 0), 60: (F(1), 1)}   # tan θ = c·√3^e


def sv(a, b=0):
    """a + b√3 as text (a, b Fractions)"""
    a, b = F(a), F(b)
    def rt(k):
        if k == 1:
            return "√3"
        if k.denominator == 1:
            return "%s√3" % num(k)
        return "%s√3/%d" % (num(k.numerator) if k.numerator != 1 else "", k.denominator)
    if b == 0:
        return fv(a) if a.denominator != 1 else num(a)
    if a == 0:
        return rt(b)
    if a < 0 < b:
        return "%s − %s" % (rt(b), num(-a) if a.denominator == 1 else fv(-a))
    return "%s + %s" % (num(a) if a.denominator == 1 else fv(a), rt(b)) if b > 0 else "%s − %s" % (num(a), rt(-b))


def times_tan(d, ang):
    """d · tan(ang) as (a, b) meaning a + b√3"""
    c, e = TAN[ang]
    return (d * c, 0) if e == 0 else (0, d * c)


def div_tan(h, ang):
    """h / tan(ang)"""
    if ang == 45:
        return (h, 0)
    if ang == 60:
        return (0, F(h, 3))   # h/√3 = h√3/3
    return (0, h)            # h/(1/√3) = h√3


def fig(ang, top="", side="", base="", label="angle of elevation", depression=False):
    W, H = 320, 220
    Bx, By = 260, 190
    Ax = 50
    import math
    h = min(150, (Bx - Ax) * math.tan(math.radians(ang)))
    Tx, Ty = Bx, By - h
    s = ["<polygon points='%d,%d %d,%d %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.4'/>" % (Ax, By, Bx, By, Tx, Ty, FILL, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2'/>" % (Bx - 12, By, Bx - 12, By - 12, Bx, By - 12, INK)]
    if not depression:
        s.append("<path d='M%d %d A 34 34 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (Ax + 34, By, Ax + 34 * math.cos(math.radians(ang)), By - 34 * math.sin(math.radians(ang)), RED))
        s.append(text(Ax + 52, By - 8, "%d°" % ang, 15, col=RED))
    else:
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-dasharray='6 4'/>" % (Tx, Ty, Ax - 10, Ty, INK))
        s.append("<path d='M%.1f %.1f A 34 34 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (Tx - 34, Ty, Tx - 34 * math.cos(math.radians(ang)), Ty + 34 * math.sin(math.radians(ang)), RED))
        s.append(text(Tx - 54, Ty + 20, "%d°" % ang, 15, col=RED))
    if side:
        s.append(text(Bx + 10, (By + Ty) / 2 + 5, side, 16, col=BLUE, anchor="start"))
    if base:
        s.append(text((Ax + Bx) / 2, By + 24, base, 16, col=BLUE))
    return svg_wrap(W, H, "".join(s), label)


def ans_m(a, b=0):
    return sv(a, b) + " m"


def wrongs(a, b, alts):
    out = []
    a, b = F(a), F(b)
    alts = list(alts) + [(2 * a, 2 * b), (b, a) if (b, a) != (a, b) else (a + 1, b), (F(a, 2), F(b, 2)), (a + b, 0), (0, a + b)]
    for x in alts:
        s = ans_m(*x)
        if s != ans_m(a, b) and s not in out and s != "0 m":
            out.append(s)
    return out[:3]


# ---------------------------------------------------------------- set 1: find a height
def one_h(r):
    ang = r.choice([30, 45, 60, 60, 30])
    d = r.choice([10, 15, 20, 24, 30, 36, 40, 45, 50, 60]) if ang != 30 else r.choice([15, 21, 24, 30, 36, 45, 60])
    a, b = times_tan(d, ang)
    obj = r.choice(["tower", "tree", "building", "temple tower", "water tank"])
    pic = fig(ang, side="h", base="%d m" % d)
    alt = [div_tan(d, ang), (d, 0) if ang != 45 else (2 * d, 0), times_tan(d, 90 - ang) if ang != 45 else (0, d)]
    return T(pic + "From a point on the ground %d m from the foot of a %s, the angle of elevation of its top is %d°. Find the height of the %s." % (d, obj, ang, obj), ans_m(a, b), wrongs(a, b, alt),
             "tan %d° = h/%d, so h = %d × tan %d° = <b>%s</b>." % (ang, d, d, ang, ans_m(a, b)))


# ---------------------------------------------------------------- set 2: find a distance
def one_d(r):
    ang = r.choice([30, 45, 60])
    h = r.choice([10, 15, 20, 30, 45, 60, 75]) if ang != 60 else r.choice([15, 30, 45, 60, 75, 90])
    a, b = div_tan(h, ang)
    obj = r.choice(["tower", "pole", "building", "lighthouse"])
    pic = fig(ang, side="%d m" % h, base="d")
    alt = [times_tan(h, ang), times_tan(h, 90 - ang) if ang != 45 else (2 * h, 0), (h, 0) if ang != 45 else (0, h)]
    return T(pic + "A %s is %d m high. The angle of elevation of its top from a point on the ground is %d°. How far is the point from the foot of the %s?" % (obj, h, ang, obj), ans_m(a, b), wrongs(a, b, alt),
             "tan %d° = %d/d, so d = %d ÷ tan %d° = <b>%s</b>." % (ang, h, h, ang, ans_m(a, b)))


# ---------------------------------------------------------------- set 3: angles of depression
def one_dep(r):
    ang = r.choice([30, 45, 60])
    h = r.choice([15, 20, 30, 45, 60, 75, 90, 100])
    kind = r.choice(["boat", "car", "ground"])
    a, b = div_tan(h, ang)
    pic = fig(ang, side="%d m" % h, base="d", label="angle of depression", depression=True)
    obj = {"boat": ("the top of a %d m high lighthouse" % h, "a boat"), "car": ("the top of a %d m high building" % h, "a car on the road"),
           "ground": ("a balcony %d m above the ground" % h, "a scooter parked on the road")}[kind]
    alt = [times_tan(h, ang), times_tan(h, 90 - ang) if ang != 45 else (2 * h, 0), (h, 0) if ang != 45 else (0, h)]
    return T(pic + "From %s, the angle of depression of %s is %d°. How far is it from the foot of the %s?" % (obj[0], obj[1], ang, {"boat": "lighthouse", "car": "building", "ground": "building"}[kind]),
             ans_m(a, b), wrongs(a, b, alt),
             "The angle of depression equals the angle of elevation from the object (alternate angles). tan %d° = %d/d, so d = <b>%s</b>." % (ang, h, ans_m(a, b)))


# ---------------------------------------------------------------- set 4: two right triangles
def one_two(r):
    kind = r.choice(["closer", "closer", "flag", "poles"])
    if kind == "closer":
        a1, a2 = 30, 60
        x = r.choice([10, 15, 20, 25, 30, 40, 50])   # distance walked
        # h = x·√3/2, distance from second point = x/2
        h = (0, F(x, 2))
        return T("The angle of elevation of the top of a tower from a point on the ground is 30°. After walking %d m towards the tower, the angle becomes 60°. Find the height of the tower." % x,
                 ans_m(*h), wrongs(*h, [(F(x, 2), 0), (0, x), (x, 0)]),
                 "Let the height be h and the second distance y: h = y√3 and h = (y + %d)/√3. So 3y = y + %d, y = %s m and h = <b>%s</b>." % (x, x, fv(F(x, 2)), ans_m(*h)))
    if kind == "flag":
        d = r.choice([10, 15, 20, 30])
        hb = d   # building with elevation 45° to top of building
        # flagstaff top at 60°: total = d√3, flag = d√3 − d
        return T("From a point on the ground %d m from a building, the angles of elevation of the bottom and the top of a flagstaff on the building are 45° and 60°. Find the length of the flagstaff." % d,
                 ans_m(-d, d), wrongs(-d, d, [(0, d), (d, 0), (d, d)]),
                 "Building: tan 45° = h/%d, h = %d m. Top: tan 60° = H/%d, H = %d√3 m. Flagstaff = <b>%s</b> = %d(√3 − 1) m." % (d, d, d, d, ans_m(-d, d), d))
    w = r.choice([40, 60, 80, 100, 120])
    # two equal poles, opposite sides of a road w wide, angles 60 and 30 from a point between them -> h = w√3/4
    h = (0, F(w, 4))
    return T("Two poles of equal height stand on either side of a road %d m wide. From a point on the road between them, the angles of elevation of their tops are 60° and 30°. Find the height of each pole." % w,
             ans_m(*h), wrongs(*h, [(0, F(w, 2)), (F(w, 4), 0), (0, F(w, 3))]),
             "Distances x and %d − x: h = x√3 and h = (%d − x)/√3. So 3x = %d − x, x = %s m and h = <b>%s</b>." % (w, w, w, fv(F(w, 4)), ans_m(*h)))


# ---------------------------------------------------------------- set 5: situations
def one_sit(r):
    kind = r.choice(["kite", "ladder", "slide", "shadow", "tree", "approx"])
    name, he, his = P.next()
    if kind == "kite":
        L = r.choice([40, 60, 80, 100, 120])
        ang = r.choice([30, 60])
        h = (F(L, 2), 0) if ang == 30 else (0, F(L, 2))
        return T("%s flies a kite with a string %d m long, making an angle of %d° with the ground. Assuming the string is straight, how high is the kite?" % (name, L, ang),
                 ans_m(*h), wrongs(*h, [(0, F(L, 2)) if ang == 30 else (F(L, 2), 0), (L, 0), (0, L)]),
                 "The string is the hypotenuse: h = %d × sin %d° = <b>%s</b>." % (L, ang, ans_m(*h)))
    if kind == "ladder":
        h = r.choice([6, 8, 10, 12])
        ang = r.choice([30, 60])
        L = 2 * h if ang == 30 else None
        if ang == 30:
            return T("A ladder reaches a window %d m above the ground and makes an angle of 30° with the ground. How long is the ladder?" % h, ans_m(L), wrongs(L, 0, [(h, 0), (0, h), (0, F(2 * h, 3))]),
                     "sin 30° = %d/L, so L = %d ÷ ½ = <b>%s</b>." % (h, h, ans_m(L)))
        return T("A ladder reaches a window %d m above the ground and makes an angle of 60° with the ground. How long is the ladder?" % h, ans_m(0, F(2 * h, 3)), wrongs(0, F(2 * h, 3), [(2 * h, 0), (0, h), (h, 0)]),
                 "sin 60° = %d/L, so L = %d ÷ (√3/2) = 2 × %d/√3 = <b>%s</b>." % (h, h, h, ans_m(0, F(2 * h, 3))))
    if kind == "slide":
        h = r.choice([F(3, 2), 2, F(5, 2), 3])
        return T("A slide in a park is %s m high and is inclined at 30° to the ground. How long is the slide?" % fv(h), ans_m(2 * h), wrongs(2 * h, 0, [(h, 0), (0, h), (0, 2 * h)]),
                 "sin 30° = %s/L, so L = 2 × %s = <b>%s</b>." % (fv(h), fv(h), ans_m(2 * h)))
    if kind == "shadow":
        h = r.choice([10, 15, 20, 30])
        return T("A tower %d m high casts a shadow %d√3 m long on the ground. What is the angle of elevation of the sun?" % (h, h), "30°", ["60°", "45°", "90°"],
                 "tan θ = %d / (%d√3) = 1/√3, so <b>θ = 30°</b>." % (h, h))
    if kind == "tree":
        d = r.choice([6, 8, 10, 12, 15])
        # tree broken: top touches ground at distance d, makes 30° with ground: broken part = 2d/√3, standing = d/√3 -> total = d√3
        return T("The top of a tree, broken by the wind, touches the ground %d m from the foot of the tree, making an angle of 30° with the ground. Find the original height of the tree." % d,
                 ans_m(0, d), wrongs(0, d, [(d, 0), (0, F(d, 3)), (2 * d, 0)]),
                 "Standing part = %d tan 30° = %d/√3 m, broken part = %d/cos 30° = 2 × %d/√3 m. Total = 3 × %d/√3 = <b>%s</b>." % (d, d, d, d, d, ans_m(0, d)))
    h = r.choice([20, 25, 30, 40, 50, 60])
    ang = r.choice([30, 60])
    a, b = div_tan(h, ang)
    approx = float(a) + float(b) * 1.73
    return T("A pole is %d m high. Find the length of its shadow when the sun's altitude is %d°. (Use √3 = 1.73.)" % (h, ang), "%s m" % num(F(round(approx * 100), 100)),
             ["%s m" % num(F(round(h * (1.73 if ang == 60 else 1 / 1.73) * 100), 100)), "%s m" % num(h), "%s m" % num(F(round(h / 1.73 * 2 * 100), 100)) if ang == 60 else "%s m" % num(F(round(h * 2 * 100), 100))],
             "shadow = %d ÷ tan %d° = %s ≈ <b>%s m</b>." % (h, ang, ans_m(a, b), num(F(round(approx * 100), 100))))


def main():
    seen = set()
    sets = [
        S("Finding a height", mix(R, [(one_h, 20)], seen)),
        S("Finding a distance", mix(R, [(one_d, 20)], seen)),
        S("Angles of depression", mix(R, [(one_dep, 20)], seen)),
        S("Two right triangles", mix(R, [(one_two, 8), (one_h, 6), (one_d, 6)], seen)),
        S("Word problems", mix(R, [(one_sit, 20)], seen)),
    ]
    body = lesson(
        "<p>The <b>angle of elevation</b> is the angle between the horizontal and the line of sight when you look <b>up</b>. The <b>angle of depression</b> is the angle when you look <b>down</b>.</p>"
        "<p>Draw the right triangle, mark the angle, then use tan θ = height/distance (or sin, cos when a slanting length is involved).</p>"
        "<p>tan 30° = 1/√3, tan 45° = 1, tan 60° = √3. The angle of depression from A to B equals the angle of elevation from B to A.</p>",
        [("A tower is 30 m from a point where the angle of elevation is 60°. Find its height.", ["tan 60° = h/30", "h = 30√3"], "30√3 m ≈ 51.9 m"),
         ("From the top of a 75 m lighthouse, the angle of depression of a ship is 45°. How far is the ship?", ["tan 45° = 75/d"], "75 m")],
        ["Writing h = d/tan θ when the distance is known. It is h = d × tan θ.",
         "Marking the angle of depression at the bottom of the figure. It is at the observer's eye, below the horizontal.",
         "Using tan 30° = √3. tan 30° = 1/√3 and tan 60° = √3."])
    faq = [
        ("What is an angle of elevation?", "The angle between the horizontal line and the line of sight to an object above the observer's eye."),
        ("What is an angle of depression?", "The angle between the horizontal line and the line of sight to an object below the observer's eye. It equals the angle of elevation seen from the object."),
        ("Which ratio is used in heights and distances?", "Usually tan θ = height/horizontal distance. Use sin or cos when a slanting length such as a ladder or kite string is given."),
        ("Why is the answer often left as 20√3 m?", "Exact answers keep the surd. If asked, use √3 ≈ 1.73 to get a decimal, for example 20√3 ≈ 34.6 m."),
    ]
    make(10, "some-applications-of-trigonometry", 9, "V", 9, "Some Applications of Trigonometry: Heights and Distances", "heights and distances",
         "Heights and distances: angle of elevation, angle of depression; simple problems on heights and distances; problems should not involve more than two right triangles; angles of elevation / depression should be only 30°, 45° and 60° (summary of the CBSE syllabus)",
         "Class 10 Heights and Distances worksheet (NCERT Chapter 9): angles of elevation and depression, towers, lighthouses, kites, ladders and two-triangle problems. 100 questions with answers.",
         "tan θ = height ÷ distance", "Angles of elevation and depression use 30°, 45° and 60°.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
