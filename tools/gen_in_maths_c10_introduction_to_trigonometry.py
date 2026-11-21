# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 8: Introduction to Trigonometry (CBSE Unit V Trigonometry)
  python3 tools/gen_in_maths_c10_introduction_to_trigonometry.py
The six trigonometric ratios from a right triangle, finding the other ratios from one ratio, values at 0°, 30°, 45°, 60°
and 90° and expressions with them, the identities sin²A + cos²A = 1, 1 + tan²A = sec²A, 1 + cot²A = cosec²A, and
finding angles from values.
Wrong answers come from real mistakes: opposite/adjacent swapped, sec = 1/sin, sin 30° = √3/2, sin²A + cos²A = 2,
and sec²A + tan²A = 1.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, fv, svg_wrap, text, INK, RED, BLUE, FILL

R = random.Random(910008)
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]
RAT = ["sin", "cos", "tan", "cosec", "sec", "cot"]


def ratio(name, o, a, h):
    return {"sin": F(o, h), "cos": F(a, h), "tan": F(o, a), "cosec": F(h, o), "sec": F(h, a), "cot": F(a, o)}[name]


def frs(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else "%d/%d" % (v.numerator, v.denominator)


def tri_svg(o, a, h, show, ang="A"):
    """right angle at B, angle A at the left; opposite side BC (vertical), adjacent AB (horizontal)"""
    W, H = 300, 210
    sc = min(220.0 / a, 150.0 / o)
    A = (40, 180)
    B = (40 + a * sc, 180)
    C = (40 + a * sc, 180 - o * sc)
    s = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.6'/>" % (A + B + C + (FILL, INK)),
         "<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (B[0] - 14, B[1], B[0] - 14, B[1] - 14, B[0], B[1] - 14, INK),
         text(A[0] - 14, A[1] + 6, "A", 17), text(B[0] + 14, B[1] + 6, "B", 17), text(C[0] + 14, C[1] + 4, "C", 17)]
    lab = {"o": (C[0] + 26, (B[1] + C[1]) / 2 + 6, "start"), "a": ((A[0] + B[0]) / 2, A[1] + 24, "middle"), "h": ((A[0] + C[0]) / 2 - 16, (A[1] + C[1]) / 2 - 6, "end")}
    vals = {"o": o, "a": a, "h": h}
    for k in show:
        x, y, anc = lab[k]
        s.append(text(x - (16 if k == "o" else 0), y, "%s" % num(vals[k]), 16, col=BLUE, anchor=anc))
    return svg_wrap(W, H, "".join(s), "right triangle ABC with the right angle at B")


# ---------------------------------------------------------------- set 1: ratios from a right triangle
def one_tri(r):
    o, a, h = r.choice(TRIP)
    if r.random() < 0.5:
        o, a = a, o
    k = r.choice([1, 1, 2])
    o, a, h = o * k, a * k, h * k
    name = r.choice(RAT)
    v = ratio(name, o, a, h)
    pic = tri_svg(o, a, h, ["o", "a", "h"])
    swap = {"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan", "sec": "cosec", "cosec": "sec"}
    inv = {"sin": "cosec", "cos": "sec", "tan": "cot", "cot": "tan", "sec": "cos", "cosec": "sin"}
    w = [frs(ratio(swap[name], o, a, h)), frs(ratio(inv[name], o, a, h)), frs(F(o, h) if name != "sin" else F(a, o))]
    return T(pic + "In right △ABC (right angle at B), find %s A." % name, frs(v), w,
             "For angle A: opposite BC = %s, adjacent AB = %s, hypotenuse AC = %s. %s A = <b>%s</b>." % (num(o), num(a), num(h), name, frs(v)))


# ---------------------------------------------------------------- set 2: one ratio gives the others
def one_from(r):
    o, a, h = r.choice(TRIP)
    if r.random() < 0.5:
        o, a = a, o
    given = r.choice(["sin", "cos", "tan", "sec", "cot", "cosec"])
    want = r.choice([x for x in RAT if x != given])
    gv, wv = ratio(given, o, a, h), ratio(want, o, a, h)
    # wrong: use the given numbers as if they were other sides
    third = {"sin": (o, h), "cos": (a, h), "tan": (o, a), "cosec": (h, o), "sec": (h, a), "cot": (a, o)}[given]
    w = [frs(1 / wv), frs(ratio({"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan", "sec": "cosec", "cosec": "sec"}[want], o, a, h)), frs(F(third[0], third[0] + third[1]))]
    pic = tri_svg(o, a, h, [])
    return T("If %s A = %s, find %s A (A is acute)." % (given, frs(gv), want), frs(wv), w,
             "Draw a right triangle with %s A = %s: the sides are opposite %d, adjacent %d, hypotenuse %d (Pythagoras). So %s A = <b>%s</b>." % (given, frs(gv), o, a, h, want, frs(wv)))


# ---------------------------------------------------------------- set 3: specific angles
VAL = {  # value strings and numeric values
    ("sin", 0): ("0", 0.0), ("sin", 30): ("1/2", 0.5), ("sin", 45): ("1/√2", 2 ** -0.5), ("sin", 60): ("√3/2", 3 ** 0.5 / 2), ("sin", 90): ("1", 1.0),
    ("cos", 0): ("1", 1.0), ("cos", 30): ("√3/2", 3 ** 0.5 / 2), ("cos", 45): ("1/√2", 2 ** -0.5), ("cos", 60): ("1/2", 0.5), ("cos", 90): ("0", 0.0),
    ("tan", 0): ("0", 0.0), ("tan", 30): ("1/√3", 3 ** -0.5), ("tan", 45): ("1", 1.0), ("tan", 60): ("√3", 3 ** 0.5),
    ("sec", 0): ("1", 1.0), ("sec", 30): ("2/√3", 2 / 3 ** 0.5), ("sec", 45): ("√2", 2 ** 0.5), ("sec", 60): ("2", 2.0),
    ("cosec", 30): ("2", 2.0), ("cosec", 45): ("√2", 2 ** 0.5), ("cosec", 60): ("2/√3", 2 / 3 ** 0.5), ("cosec", 90): ("1", 1.0),
    ("cot", 30): ("√3", 3 ** 0.5), ("cot", 45): ("1", 1.0), ("cot", 60): ("1/√3", 3 ** -0.5), ("cot", 90): ("0", 0.0),
}
EXPRS = [  # (text, exact answer, wrong answers)
    ("sin 60° cos 30° + sin 30° cos 60°", "1", ["√3/2", "1/2", "3/2"]),
    ("2 tan² 45° + cos² 30° − sin² 60°", "2", ["1", "3", "5/2"]),
    ("cos 45° / (sec 30° + cosec 30°)", "(3√2 − √6)/8", ["1/2", "√2/4", "(√6 − √2)/4"]),
    ("sin 30° + cos 60°", "1", ["√3", "1/2", "√3/2"]),
    ("2 sin 30° cos 30°", "√3/2", ["1/2", "√3", "1"]),
    ("tan² 60° + 2 tan² 45°", "5", ["3", "4", "7"]),
    ("sin² 45° + cos² 45°", "1", ["1/2", "2", "√2"]),
    ("4 cos² 60° + 4 sin² 30°", "2", ["1", "4", "3"]),
    ("cos 0° + sin 90° + tan 45°", "3", ["2", "1", "0"]),
    ("(1 − tan² 45°)/(1 + tan² 45°)", "0", ["1", "1/2", "2"]),
    ("2 tan 30° / (1 + tan² 30°)", "√3/2", ["1/2", "1/√3", "√3"]),
    ("cos 60° cos 30° − sin 60° sin 30°", "0", ["1", "1/2", "√3/2"]),
    ("sec² 45° − tan² 45°", "1", ["0", "2", "√2"]),
    ("cosec² 30° − cot² 30°", "1", ["2", "4", "√3"]),
    ("sin 90° − cos 0°", "0", ["1", "2", "−1"]),
    ("3 sin² 30° + cos² 30°", "3/2", ["1", "2", "3/4"]),
]


def one_val(r):
    kind = r.choice(["val", "val", "expr", "expr", "expr"])
    if kind == "val":
        k = r.choice(sorted(VAL))
        v, _ = VAL[k]
        other = sorted(set(t for t, _ in VAL.values()) - {v})
        r.shuffle(other)
        return T("What is the value of %s %d°?" % k, v, other[:3], "From the table of special angles, <b>%s %d° = %s</b>." % (k[0], k[1], v))
    e, ans, w = r.choice(EXPRS)
    return T("Evaluate %s." % e, ans, w, "Substitute the values from the table and simplify: <b>%s</b>." % ans)


# ---------------------------------------------------------------- set 4: identities
IDS = [
    ("sin² A + cos² A", "1", ["0", "2", "sin A cos A"]),
    ("sec² A − tan² A", "1", ["0", "−1", "sec A + tan A"]),
    ("cosec² A − cot² A", "1", ["0", "2", "cosec A cot A"]),
    ("(1 + tan² A) cos² A", "1", ["sin² A", "tan² A", "sec² A"]),
    ("(1 − cos² A) cosec² A", "1", ["cos² A", "sin² A", "cot² A"]),
    ("(1 + cot² A) sin² A", "1", ["cos² A", "cot² A", "cosec² A"]),
    ("sin A / cos A", "tan A", ["cot A", "sec A", "cosec A"]),
    ("cos A / sin A", "cot A", ["tan A", "cosec A", "sec A"]),
    ("1 − sin² A", "cos² A", ["sin² A", "1 + cos² A", "tan² A"]),
    ("sec² A − 1", "tan² A", ["cot² A", "1", "sin² A"]),
    ("cosec² A − 1", "cot² A", ["tan² A", "1", "cos² A"]),
    ("tan A × cot A", "1", ["tan² A", "0", "sec A cosec A"]),
    ("sin A × cosec A", "1", ["sin² A", "0", "sec A"]),
    ("(sec A + tan A)(sec A − tan A)", "1", ["0", "sec² A + tan² A", "2 sec A"]),
    ("9 sec² A − 9 tan² A", "9", ["0", "1", "18"]),
    ("cos² A + cos² A tan² A", "1", ["cos² A", "tan² A", "2 cos² A"]),
]


def one_id(r):
    kind = r.choice(["id", "id", "id", "num", "num"])
    if kind == "id":
        e, ans, w = r.choice(IDS)
        return T("Simplify %s." % e, ans, w, "Use sin² A + cos² A = 1, 1 + tan² A = sec² A or 1 + cot² A = cosec² A: <b>%s</b>." % ans)
    o, a, h = r.choice(TRIP)
    if r.random() < 0.5:
        o, a = a, o
    t = r.choice(["sec_from_tan", "cos_from_sin", "cosec_from_cot"])
    if t == "sec_from_tan":
        return T("If tan A = %s (A acute), use 1 + tan² A = sec² A to find sec A." % frs(F(o, a)), frs(F(h, a)),
                 [frs(F(o * o + a * a, a * a)), frs(F(a, h)), frs(1 + F(o, a))],
                 "sec² A = 1 + %s = %s, so <b>sec A = %s</b>." % (frs(F(o * o, a * a)), frs(F(h * h, a * a)), frs(F(h, a))))
    if t == "cos_from_sin":
        return T("If sin A = %s (A acute), use sin² A + cos² A = 1 to find cos A." % frs(F(o, h)), frs(F(a, h)),
                 [frs(1 - F(o, h)), frs(F(a * a, h * h)), frs(F(h, a))],
                 "cos² A = 1 − %s = %s, so <b>cos A = %s</b>." % (frs(F(o * o, h * h)), frs(F(a * a, h * h)), frs(F(a, h))))
    return T("If cot A = %s (A acute), use 1 + cot² A = cosec² A to find cosec A." % frs(F(a, o)), frs(F(h, o)),
             [frs(F(h * h, o * o)), frs(F(o, h)), frs(1 + F(a, o))],
             "cosec² A = 1 + %s = %s, so <b>cosec A = %s</b>." % (frs(F(a * a, o * o)), frs(F(h * h, o * o)), frs(F(h, o))))


# ---------------------------------------------------------------- set 5: finding angles and true or false
def one_ang(r):
    kind = r.choice(["find", "find", "two", "tf", "tf"])
    if kind == "find":
        cand = [(k, v) for k, v in VAL.items() if 0 < k[1] < 90]
        (fn, ang), (vs, _) = r.choice(cand)
        m = r.choice([1, 2, 3])
        if ang % m:
            return None
        th = ang // m
        lhs = "%s %sθ" % (fn, "" if m == 1 else str(m))
        return T("Find the acute angle θ if %s = %s." % (lhs, vs), "θ = %d°" % th,
                 ["θ = %d°" % t for t in dict.fromkeys([90 - ang, ang, ang * m, th * 2, 45, 15]) if 0 < t <= 90 and t != th][:3],
                 "%s %d° = %s, so %s%s = %d° and <b>θ = %d°</b>." % (fn, ang, vs, "" if m == 1 else str(m), "θ", ang, th))
    if kind == "two":
        A, B = r.choice([(45, 15), (60, 30), (45, 30), (30, 15), (60, 15), (40, 20), (50, 10)])
        p, q = A + B, A - B
        f1 = {90: "sin(A + B) = 1", 60: "tan(A + B) = √3", 30: "cos(A + B) = √3/2", 45: "tan(A + B) = 1"}.get(p)
        f2 = {30: "sin(A − B) = 1/2", 15: None, 0: "cos(A − B) = 1", 60: "cos(A − B) = 1/2", 45: "tan(A − B) = 1"}.get(q)
        if not f1 or not f2:
            return None
        return T("If %s and %s, with 0° &lt; A + B ≤ 90° and A &gt; B, find A and B." % (f1, f2), "A = %d°, B = %d°" % (A, B),
                 ["A = %d°, B = %d°" % (B, A), "A = %d°, B = %d°" % (p, q), "A = %d°, B = %d°" % (A + 5, B - 5)],
                 "A + B = %d° and A − B = %d°. Adding: 2A = %d°, so <b>A = %d°, B = %d°</b>." % (p, q, p + q, A, B))
    st = r.choice([
        ("The value of tan A is always less than 1.", "False", "tan 60° = √3 &gt; 1."),
        ("sec A = 12/5 for some value of angle A.", "True", "sec A = hypotenuse/adjacent can be greater than 1."),
        ("cos A is the abbreviation used for the cosecant of angle A.", "False", "cos A is the cosine; the cosecant is cosec A."),
        ("cot A is the product of cot and A.", "False", "cot A is one symbol: the cotangent of angle A."),
        ("sin θ = 4/3 for some angle θ.", "False", "sin θ = opposite/hypotenuse is never greater than 1."),
        ("sin A = cos A when A = 45°.", "True", "sin 45° = cos 45° = 1/√2."),
        ("The value of sin θ increases as θ increases from 0° to 90°.", "True", "sin goes from 0 to 1."),
        ("The value of cos θ increases as θ increases from 0° to 90°.", "False", "cos goes from 1 down to 0."),
        ("sin (A + B) = sin A + sin B.", "False", "Take A = 60°, B = 30°: sin 90° = 1 but sin 60° + sin 30° ≠ 1."),
        ("cot A is not defined for A = 0°.", "True", "cot 0° = cos 0°/sin 0° = 1/0, which is not defined."),
    ])
    return T("True or false? %s" % st[0], st[1], ["False" if st[1] == "True" else "True", "True only for A = 0°", "It depends on the size of the triangle"],
             "<b>%s</b>. %s" % (st[1], st[2]))


def main():
    seen = set()
    sets = [
        S("Ratios from a right triangle", mix(R, [(one_tri, 20)], seen)),
        S("One ratio gives the others", mix(R, [(one_from, 20)], seen)),
        S("Ratios of 0°, 30°, 45°, 60° and 90°", mix(R, [(one_val, 20)], seen)),
        S("Trigonometric identities", mix(R, [(one_id, 20)], seen)),
        S("Finding angles; true or false", mix(R, [(one_ang, 20)], seen)),
    ]
    body = lesson(
        "<p>In a right triangle, for an acute angle A: <b>sin A</b> = opposite/hypotenuse, <b>cos A</b> = adjacent/hypotenuse, <b>tan A</b> = opposite/adjacent. "
        "Their reciprocals are cosec A, sec A and cot A.</p>"
        "<p>Values: sin 30° = 1/2, sin 45° = 1/√2, sin 60° = √3/2; cos goes the other way; tan 30° = 1/√3, tan 45° = 1, tan 60° = √3.</p>"
        "<p>Identities: <b>sin² A + cos² A = 1</b>, 1 + tan² A = sec² A, 1 + cot² A = cosec² A.</p>",
        [("If sin A = 3/4, find cos A and tan A.", ["Opposite 3, hypotenuse 4, adjacent √7", "cos A = √7/4"], "cos A = √7/4, tan A = 3/√7"),
         ("Evaluate sin 60° cos 30° + sin 30° cos 60°.", ["(√3/2)(√3/2) + (1/2)(1/2)", "3/4 + 1/4"], "1")],
        ["Swapping opposite and adjacent. Look from the angle you are working with.",
         "Writing sec A = 1/sin A. sec A = 1/cos A and cosec A = 1/sin A.",
         "Mixing up sin 30° = 1/2 with sin 60° = √3/2."])
    faq = [
        ("What are the six trigonometric ratios?", "sin, cos, tan and their reciprocals cosec, sec, cot. For angle A: sin A = opposite/hypotenuse, cos A = adjacent/hypotenuse, tan A = opposite/adjacent."),
        ("How do I remember the values for 0°, 30°, 45°, 60° and 90°?", "sin takes the values √0/2, √1/2, √2/2, √3/2, √4/2, that is 0, 1/2, 1/√2, √3/2, 1. cos takes the same values in reverse order, and tan = sin/cos."),
        ("What are the three trigonometric identities in Class 10?", "sin²A + cos²A = 1, 1 + tan²A = sec²A (for 0° ≤ A < 90°) and 1 + cot²A = cosec²A (for 0° < A ≤ 90°)."),
        ("Can sin A be greater than 1?", "No. The hypotenuse is the longest side, so opposite/hypotenuse is at most 1."),
    ]
    make(10, "introduction-to-trigonometry", 8, "V", 8, "Introduction to Trigonometry: Ratios and Identities", "introduction to trigonometry",
         "Trigonometric ratios of an acute angle of a right-angled triangle; values of the ratios of 30°, 45° and 60°; relationships between the ratios; proof and applications of the identity sin²A + cos²A = 1, only simple identities to be given (summary of the CBSE syllabus)",
         "Class 10 Introduction to Trigonometry worksheet (NCERT Chapter 8): six trigonometric ratios, values of 0° to 90°, identities and finding angles. 100 questions with answers.",
         "sin² A + cos² A = 1", "sin = opposite/hypotenuse, cos = adjacent/hypotenuse, tan = opposite/adjacent.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
