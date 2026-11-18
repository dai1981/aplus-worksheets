# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Trigonometry, SOH CAH TOA (Sec 2 Geometry and measures)
  python3 gen_sg_maths_s2_trigonometric_ratios.py
Naming the opposite, adjacent and hypotenuse; choosing sin, cos or tan; finding a side; finding a side when
the unknown is the denominator; finding an angle with inverse trigonometry; exact values and problems.
Wrong answers come from real mistakes: choosing the wrong ratio, multiplying instead of dividing when the
unknown is the hypotenuse, and using sin instead of sin⁻¹ for an angle.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from sg_sec import num, mcq, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, INK, RED, GREEN

R = random.Random(821300)
TH = "<i>θ</i>"


def d1(x):
    return "{:,.1f}".format(float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))


def tri(opp_lab, adj_lab, hyp_lab, ang_lab, ang_deg=35):
    """Right angle bottom-left; angle of size ang_deg at bottom-right."""
    W = 220
    H = W * math.tan(math.radians(ang_deg))
    if H > 150:
        W = 150 / math.tan(math.radians(ang_deg)); H = 150
    if H < 50:
        H = 50; W = H / math.tan(math.radians(ang_deg))
    x0, y0 = 70, 30 + H
    s = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % (x0, y0, x0 + W, y0, x0, y0 - H, INK),
         "<path d='M%.1f %.1f l14 0 l0 14' fill='none' stroke='%s' stroke-width='1.8'/>" % (x0, y0 - 14, GREEN)]
    a = math.radians(180 - ang_deg)
    s.append("<path d='M%.1f %.1f A30 30 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (
        x0 + W - 30, y0, x0 + W + 30 * math.cos(a), y0 - 30 * math.sin(a), GREEN))
    is_th = ang_lab == TH
    s.append(text(x0 + W - 46, y0 - 8, "θ" if is_th else ang_lab, 15 if is_th else 14, col=RED if is_th else INK, italic=is_th))
    s.append(text(x0 - 8, y0 - H / 2 + 5, opp_lab, 15, anchor="end", col=RED if opp_lab == "x" else INK, italic=opp_lab == "x"))
    s.append(text(x0 + W / 2, y0 + 22, adj_lab, 15, col=RED if adj_lab == "x" else INK, italic=adj_lab == "x"))
    s.append(text(x0 + W / 2 + 16, y0 - H / 2 - 8, hyp_lab, 15, anchor="start", col=RED if hyp_lab == "x" else INK, italic=hyp_lab == "x"))
    return svg_wrap(int(x0 + W + 80), int(y0 + 34), "".join(s), "right-angled triangle, not drawn accurately")


def dg(v):
    return "%s°" % num(v)


# ------------------------------------------------------------ set 1: labelling and choosing the ratio
def one_label(r):
    if r.random() < 0.5:
        side = r.choice(["opposite", "adjacent", "hypotenuse"])
        letters = r.sample(r.choice([["A", "B", "C"], ["P", "Q", "R"], ["X", "Y", "Z"]]), 3)
        ang = r.choice([30, 35, 40, 50])
        svg = tri(letters[0], letters[1], letters[2], TH, ang)
        right = {"opposite": letters[0], "adjacent": letters[1], "hypotenuse": letters[2]}[side]
        q = "Which side is the %s, relative to the angle %s?%s" % (B(side), TH, fig(svg))
        e = {"opposite": "The opposite side is across from %s: <b>%s</b>." % (TH, right),
             "adjacent": "The adjacent side is next to %s (and is not the hypotenuse): <b>%s</b>." % (TH, right),
             "hypotenuse": "The hypotenuse is the longest side, opposite the right angle: <b>%s</b>." % right}[side]
        return T(q, right, [x for x in letters if x != right] + ["None of them"], e)
    known, want = r.choice([(("opp", "hyp"), "sin"), (("adj", "hyp"), "cos"), (("opp", "adj"), "tan")])
    names = {"opp": "opposite side", "adj": "adjacent side", "hyp": "hypotenuse"}
    v1, v2 = r.randint(3, 12), r.randint(13, 20)
    if want == "tan":
        v2 = r.randint(3, 15)
    goal = r.choice(["the angle", "an angle"])
    q = "In a right-angled triangle, the %s is %d cm and the %s is %d cm. Which ratio finds %s?" % (names[known[0]], v1, names[known[1]], v2, goal)
    right = {"sin": "sin (SOH)", "cos": "cos (CAH)", "tan": "tan (TOA)"}[want]
    return T(q, right, [v for v in ["sin (SOH)", "cos (CAH)", "tan (TOA)", "Pythagoras' theorem"] if v != right],
             "SOH: sin = O/H. CAH: cos = A/H. TOA: tan = O/A. With the %s and %s, use <b>%s</b>." % (names[known[0]], names[known[1]], right))


# ------------------------------------------------------------ set 2: find a side (multiply)
def one_side_mul(r):
    ang = r.choice([25, 30, 35, 40, 42, 50, 55, 60, 65, 38, 47])
    k = r.choice([5, 6, 7, 8, 9, 10, 12, 15, 20])
    kind = r.choice(["sin", "cos", "tan"])
    if kind == "sin":
        x = k * math.sin(math.radians(ang))
        svg = tri("x", "", "%d cm" % k, dg(ang), ang)
        e = "Opposite and hypotenuse: SOH. <i>x</i> = %d × sin %d° = <b>%s cm</b>." % (k, ang, d1(x))
        wr = [k * math.cos(math.radians(ang)), k / math.sin(math.radians(ang)), k * math.tan(math.radians(ang))]
    elif kind == "cos":
        x = k * math.cos(math.radians(ang))
        svg = tri("", "x", "%d cm" % k, dg(ang), ang)
        e = "Adjacent and hypotenuse: CAH. <i>x</i> = %d × cos %d° = <b>%s cm</b>." % (k, ang, d1(x))
        wr = [k * math.sin(math.radians(ang)), k / math.cos(math.radians(ang)), k * math.tan(math.radians(ang))]
    else:
        x = k * math.tan(math.radians(ang))
        svg = tri("x", "%d cm" % k, "", dg(ang), ang)
        e = "Opposite and adjacent: TOA. <i>x</i> = %d × tan %d° = <b>%s cm</b>." % (k, ang, d1(x))
        wr = [k * math.sin(math.radians(ang)), k / math.tan(math.radians(ang)), k * math.cos(math.radians(ang))]
    q = "Find %s to 1 decimal place.%s" % (B("<i>x</i>"), fig(svg))
    right = d1(x) + " cm"
    cands = [(d1(w) + " cm", d1(w)) for w in wr if d1(w) != d1(x)] + [(d1(x + 1) + " cm", "n")]
    return mcq(q, (right, right), cands, e)


# ------------------------------------------------------------ set 3: unknown in the denominator
def one_side_div(r):
    ang = r.choice([25, 30, 35, 40, 50, 55, 60, 28, 62])
    k = r.choice([4, 5, 6, 7, 8, 9, 10, 12])
    kind = r.choice(["sin", "cos", "tan"])
    if kind == "sin":
        x = k / math.sin(math.radians(ang))
        svg = tri("%d cm" % k, "", "x", dg(ang), ang)
        e = "sin %d° = %d ÷ <i>x</i>, so <i>x</i> = %d ÷ sin %d° = <b>%s cm</b>." % (ang, k, k, ang, d1(x))
        wr = [k * math.sin(math.radians(ang)), k / math.cos(math.radians(ang)), k * math.cos(math.radians(ang))]
    elif kind == "cos":
        x = k / math.cos(math.radians(ang))
        svg = tri("", "%d cm" % k, "x", dg(ang), ang)
        e = "cos %d° = %d ÷ <i>x</i>, so <i>x</i> = %d ÷ cos %d° = <b>%s cm</b>." % (ang, k, k, ang, d1(x))
        wr = [k * math.cos(math.radians(ang)), k / math.sin(math.radians(ang)), k * math.sin(math.radians(ang))]
    else:
        x = k / math.tan(math.radians(ang))
        svg = tri("%d cm" % k, "x", "", dg(ang), ang)
        e = "tan %d° = %d ÷ <i>x</i>, so <i>x</i> = %d ÷ tan %d° = <b>%s cm</b>." % (ang, k, k, ang, d1(x))
        wr = [k * math.tan(math.radians(ang)), k / math.sin(math.radians(ang)), k * math.cos(math.radians(ang))]
    q = "Find %s to 1 decimal place.%s" % (B("<i>x</i>"), fig(svg))
    right = d1(x) + " cm"
    cands = [(d1(w) + " cm", d1(w)) for w in wr if d1(w) != d1(x)] + [(d1(x + 1.5) + " cm", "n")]
    return mcq(q, (right, right), cands, e)


# ------------------------------------------------------------ set 4: find an angle
def one_angle(r):
    kind = r.choice(["sin", "cos", "tan"])
    if kind == "tan":
        o, a = r.randint(3, 15), r.randint(3, 15)
        if o == a:
            return None
        ang = math.degrees(math.atan2(o, a))
        svg = tri("%d cm" % o, "%d cm" % a, "", TH, ang)
        e = "tan %s = %d ÷ %d. %s = tan<sup>−1</sup>(%d ÷ %d) = <b>%s°</b>." % (TH, o, a, TH, o, a, d1(ang))
        wr = [math.degrees(math.atan2(a, o)), math.tan(o / a) * 10, math.degrees(math.asin(min(1, o / (o + a))))]
    elif kind == "sin":
        h = r.randint(6, 16)
        o = r.randint(2, h - 1)
        ang = math.degrees(math.asin(o / h))
        svg = tri("%d cm" % o, "", "%d cm" % h, TH, ang)
        e = "sin %s = %d ÷ %d. %s = sin<sup>−1</sup>(%d ÷ %d) = <b>%s°</b>." % (TH, o, h, TH, o, h, d1(ang))
        wr = [math.degrees(math.acos(o / h)), math.degrees(math.atan(o / h)), 90 - ang + 5]
    else:
        h = r.randint(6, 16)
        a = r.randint(2, h - 1)
        ang = math.degrees(math.acos(a / h))
        svg = tri("", "%d cm" % a, "%d cm" % h, TH, ang)
        e = "cos %s = %d ÷ %d. %s = cos<sup>−1</sup>(%d ÷ %d) = <b>%s°</b>." % (TH, a, h, TH, a, h, d1(ang))
        wr = [math.degrees(math.asin(a / h)), math.degrees(math.atan(a / h)), ang + 10]
    if not 12 < ang < 78:
        return None
    q = "Find the angle %s to 1 decimal place.%s" % (B(TH), fig(svg))
    right = d1(ang) + "°"
    cands = [(d1(w) + "°", d1(w)) for w in wr if d1(w) != d1(ang) and 0 < w < 180] + [(d1(ang + 3) + "°", "n")]
    return mcq(q, (right, right), cands, e)


# ------------------------------------------------------------ set 5: problems and exact values
def problems():
    its = []
    data = [
        ("What is the exact value of sin 30°?", "0.5", ["√3/2", "1", "0.3"], "sin 30° = <b>1/2</b> = 0.5."),
        ("What is the exact value of cos 60°?", "0.5", ["√3/2", "0", "0.6"], "cos 60° = <b>1/2</b> = 0.5."),
        ("What is the exact value of tan 45°?", "1", ["0.5", "√2", "45"], "In a right-angled isosceles triangle opposite = adjacent, so tan 45° = <b>1</b>."),
        ("What is the exact value of sin 90°?", "1", ["0", "0.9", "90"], "sin 90° = <b>1</b>."),
        ("What is the exact value of cos 0°?", "1", ["0", "−1", "Undefined"], "cos 0° = <b>1</b>."),
        ("A 6 m ladder leans against a wall at 70° to the ground. How high up the wall does it reach, to 1 decimal place?", "5.6 m", ["2.1 m", "16.5 m", "6.4 m"], "Opposite = 6 × sin 70° = 5.64… ≈ <b>5.6 m</b>."),
        ("From 50 m away, the angle of elevation of the top of a tower is 32°. How tall is the tower, to the nearest metre?", "31 m", ["26 m", "42 m", "80 m"], "Height = 50 × tan 32° = 31.2… ≈ <b>31 m</b>."),
        ("A ramp is 4 m long and rises 0.5 m. What angle does it make with the ground, to 1 decimal place?", "7.2°", ["7.1°", "82.8°", "8.0°"], "sin θ = 0.5 ÷ 4. θ = sin<sup>−1</sup>(0.125) = 7.18… ≈ <b>7.2°</b>."),
        ("A kite string is 40 m long and makes an angle of 55° with the ground. How high is the kite, to 1 decimal place?", "32.8 m", ["22.9 m", "57.1 m", "48.8 m"], "40 × sin 55° = 32.76… ≈ <b>32.8 m</b>."),
        ("A boat sails 8 km east and then 5 km north. On what bearing must it sail to return directly? (Hint: first find the angle at the end, then use a bearing.)", "238°", ["212°", "058°", "032°"],
         "tan<sup>−1</sup>(8 ÷ 5) = 58.0° west of south, so the bearing is 180 + 58 = <b>238°</b>."),
        ("Which of these is TOA?", "tan θ = opposite ÷ adjacent", ["tan θ = adjacent ÷ opposite", "tan θ = opposite ÷ hypotenuse", "tan θ = opposite × adjacent"], "<b>tan θ = opposite ÷ adjacent</b>."),
        ("To find an angle from sin θ = 0.6, which calculator button do you use?", "sin<sup>−1</sup>", ["sin", "tan", "√"], "Use the inverse: θ = <b>sin<sup>−1</sup></b>(0.6) = 36.9°."),
        ("In a right-angled triangle, the side opposite the right angle is called…", "the hypotenuse", ["the adjacent", "the opposite", "the base"], "<b>The hypotenuse</b> is opposite the right angle and is the longest side."),
        ("Mia works out <i>x</i> = 10 × sin 40° when the 10 cm side is opposite 40° and <i>x</i> is the hypotenuse. What should she do?", "Work out 10 ÷ sin 40°", ["Work out 10 × cos 40°", "Work out sin 40° ÷ 10", "Her answer is correct"],
         "sin 40° = 10 ÷ <i>x</i>, so <i>x</i> = <b>10 ÷ sin 40°</b> = 15.6 cm."),
        ("A plane takes off at an angle of 12°. After flying 2000 m along its path, how high is it, to the nearest metre?", "416 m", ["1956 m", "425 m", "9619 m"], "2000 × sin 12° = 415.8… ≈ <b>416 m</b>."),
        ("The angle of depression from a cliff top 80 m high to a boat is 20°. How far is the boat from the foot of the cliff, to the nearest metre?", "220 m", ["29 m", "234 m", "85 m"], "tan 20° = 80 ÷ <i>d</i>, so <i>d</i> = 80 ÷ tan 20° = 219.8… ≈ <b>220 m</b>."),
        ("Which is larger, sin 50° or cos 50°?", "sin 50°", ["cos 50°", "They are equal", "It depends on the triangle"], "sin 50° ≈ 0.766 and cos 50° ≈ 0.643, so <b>sin 50°</b>."),
        ("If sin θ = 0.5, what is θ (between 0° and 90°)?", "30°", ["60°", "45°", "0.5°"], "sin 30° = 0.5, so θ = <b>30°</b>."),
        ("A rectangle is 12 cm long and 5 cm wide. What angle does its diagonal make with the long side, to 1 decimal place?", "22.6°", ["67.4°", "24.6°", "65.4°"], "tan θ = 5 ÷ 12. θ = tan<sup>−1</sup>(5/12) = 22.6…° ≈ <b>22.6°</b>."),
        ("Why can sin θ never be bigger than 1 in a right-angled triangle?", "The opposite side is always shorter than the hypotenuse", ["Because angles are less than 90°", "Because the calculator says so", "It can be bigger than 1"],
         "sin θ = opposite ÷ hypotenuse, and <b>the hypotenuse is the longest side</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>Label the sides from the angle <i>θ</i>: <b>opposite</b> (across from <i>θ</i>), <b>adjacent</b> (next to <i>θ</i>) and "
        "<b>hypotenuse</b> (longest, opposite the right angle). Then use <b>SOH CAH TOA</b>:</p>"
        "<ul><li>sin <i>θ</i> = O ÷ H</li><li>cos <i>θ</i> = A ÷ H</li><li>tan <i>θ</i> = O ÷ A</li></ul>"
        "<p>To find an angle, use the inverse buttons sin<sup>−1</sup>, cos<sup>−1</sup>, tan<sup>−1</sup>.</p>"
        + fig(tri("opposite", "adjacent", "hypotenuse", TH, 35)),
        [("The hypotenuse is 10 cm and the angle is 30°. Find the opposite side.", ["SOH: O = 10 × sin 30°."], "5 cm"),
         ("Opposite = 7 cm, adjacent = 9 cm. Find the angle.", ["TOA: θ = tan<sup>−1</sup>(7 ÷ 9)."], "37.9°"),
         ("The adjacent side is 8 cm and the angle is 40°. Find the hypotenuse.", ["CAH: cos 40° = 8 ÷ H.", "H = 8 ÷ cos 40°."], "10.4 cm")],
        ["Labelling the sides from the right angle instead of from <i>θ</i>.",
         "Choosing the wrong ratio. Write down which two sides you have first.",
         "Multiplying when the unknown is on the bottom: if sin 40° = 10 ÷ <i>x</i>, then <i>x</i> = 10 ÷ sin 40°.",
         "Using sin instead of sin<sup>−1</sup> to find an angle, or having the calculator in radians."])


def main():
    sets = [S("Labelling sides and choosing a ratio", collect(one_label, 20, R)),
            S("Finding a side", collect(one_side_mul, 20, R)),
            S("Finding the hypotenuse or adjacent side", collect(one_side_div, 20, R)),
            S("Finding an angle", collect(one_angle, 20, R)),
            S("Exact values and problems", problems())]
    make(2, "trigonometric-ratios", 12, "G4",
         "Trigonometry: SOH CAH TOA in Right-Angled Triangles",
         "Secondary 2 Trigonometry Worksheets: SOH CAH TOA, Finding Sides and Angles, and Angles of Elevation",
         "Trigonometry",
         "Use Pythagoras' Theorem and trigonometric ratios in similar triangles to solve problems involving right-angled triangles.",
         "Free Secondary 2 trigonometry worksheets with diagrams: label opposite, adjacent and hypotenuse, choose sin, cos or tan, "
         "find missing sides and angles, exact values and elevation problems. 100 questions with answers.",
         "SOH CAH TOA: sin = O/H, cos = A/H, tan = O/A.",
         "Label the sides from the angle first. To find an angle, use sin⁻¹, cos⁻¹ or tan⁻¹.",
         body(),
         [("What does SOH CAH TOA mean?", "sin = opposite ÷ hypotenuse, cos = adjacent ÷ hypotenuse, tan = opposite ÷ adjacent."),
          ("How do I choose which ratio to use?", "Write down the two sides involved (the one you know and the one you want). The pair tells you the ratio."),
          ("How do I find a missing angle?", "Work out the ratio of the two sides, then use the inverse button, for example tan⁻¹(7 ÷ 9)."),
          ("What is the difference between Pythagoras and trigonometry?", "Pythagoras links three sides. Trigonometry links two sides and an angle.")],
         sets, R)


if __name__ == "__main__":
    main()
