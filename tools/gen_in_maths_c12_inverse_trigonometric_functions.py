# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 2: Inverse Trigonometric Functions (CBSE Unit I Relations and Functions)
  python3 tools/gen_in_maths_c12_inverse_trigonometric_functions.py
Principal values of all six inverse trigonometric functions, their domains and ranges (principal value branches),
sums of principal values, expressions such as sin⁻¹(sin 2π/3) and tan(sin⁻¹ x), and tan⁻¹ x + cot⁻¹ x = π/2
(own makers and US Precalculus makers).
Wrong answers come from real mistakes: giving an angle outside the principal branch, using [−π/2, π/2] for cos⁻¹,
sin⁻¹(sin θ) = θ for every θ, and confusing sin⁻¹ x with 1/sin x.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, pi, X
from in_common import num

R = random.Random(912102)
FX = [("(Quadrant IV)", "(fourth quadrant)"), ("(Quadrant III)", "(third quadrant)"), ("(Quadrant II)", "(second quadrant)"), ("(Quadrant I)", "(first quadrant)"), ("Quadrants I and IV", "the first and fourth quadrants"), ("Quadrants I and II", "the first and second quadrants"), ("Quadrants II and III", "the second and third quadrants"),
      ("one-to-one", "one-one")]
_ex = use(__import__("gen_us_math_pc_inverse_trigonometric_functions"), "one_exact", R, FX)
comp = use(__import__("gen_us_math_pc_inverse_trigonometric_functions"), "one_comp", R, FX)
dr = use(__import__("gen_us_math_pc_inverse_trigonometric_functions"), "one_dr", R, FX)


def exact(r):
    it = _ex(r)
    return None if it is None or "degree" in it["q"] else it


# value -> angle as a multiple of π, for each function on its principal branch
VALS = {
    "sin": {"0": 0, "1/2": F(1, 6), "1/√2": F(1, 4), "√3/2": F(1, 3), "1": F(1, 2), "−1/2": F(-1, 6), "−1/√2": F(-1, 4), "−√3/2": F(-1, 3), "−1": F(-1, 2)},
    "cos": {"1": 0, "√3/2": F(1, 6), "1/√2": F(1, 4), "1/2": F(1, 3), "0": F(1, 2), "−1/2": F(2, 3), "−1/√2": F(3, 4), "−√3/2": F(5, 6), "−1": 1},
    "tan": {"0": 0, "1/√3": F(1, 6), "1": F(1, 4), "√3": F(1, 3), "−1/√3": F(-1, 6), "−1": F(-1, 4), "−√3": F(-1, 3)},
    "cot": {"√3": F(1, 6), "1": F(1, 4), "1/√3": F(1, 3), "0": F(1, 2), "−1/√3": F(2, 3), "−1": F(3, 4), "−√3": F(5, 6)},
    "sec": {"1": 0, "2/√3": F(1, 6), "√2": F(1, 4), "2": F(1, 3), "−2": F(2, 3), "−√2": F(3, 4), "−2/√3": F(5, 6), "−1": 1},
    "cosec": {"2": F(1, 6), "√2": F(1, 4), "2/√3": F(1, 3), "1": F(1, 2), "−2": F(-1, 6), "−√2": F(-1, 4), "−2/√3": F(-1, 3), "−1": F(-1, 2)},
}
BR = {"sin": "[−π/2, π/2]", "cos": "[0, π]", "tan": "(−π/2, π/2)", "cot": "(0, π)", "sec": "[0, π] − {π/2}", "cosec": "[−π/2, π/2] − {0}"}
DOM = {"sin": "[−1, 1]", "cos": "[−1, 1]", "tan": "R", "cot": "R", "sec": "R − (−1, 1)", "cosec": "R − (−1, 1)"}


def one_pv(r):
    fn = r.choice(["cot", "sec", "cosec", "sin", "cos", "tan", "cot", "sec", "cosec"])
    v, ang = r.choice(list(VALS[fn].items()))
    if ang == 0 and r.random() < 0.7:
        return None
    other = {"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan", "sec": "cosec", "cosec": "sec"}[fn]
    wr = [pi(-ang) if ang else pi(F(1, 2)), pi(1 - ang) if 1 - ang != ang else pi(F(1, 2) - ang), pi(VALS[other].get(v, ang + F(1, 6)))]
    if ang < 0:
        wr[1] = pi(1 + ang) if 1 + ang != ang else pi(F(1, 3))
    return T2("Find the principal value of %s<sup>−1</sup>(%s)." % (fn, v), pi(ang), wr,
              "The principal branch of %s<sup>−1</sup> is %s. The angle there with %s θ = %s is <b>%s</b>." % (fn, BR[fn], fn, v, pi(ang)))


def one_branch(r):
    fn = r.choice(list(BR))
    if r.random() < 0.6:
        return T2("What is the range (principal value branch) of %s<sup>−1</sup>?" % fn, BR[fn], [w for k, w in BR.items() if k != fn and w != BR[fn]][:6:2],
                  "The principal value branch of %s<sup>−1</sup> is <b>%s</b>." % (fn, BR[fn]))
    wr = sorted(set(DOM.values()) - {DOM[fn]}) + ["[0, π]"]
    return T2("What is the domain of %s<sup>−1</sup>?" % fn, DOM[fn], wr[:3],
              "%s<sup>−1</sup> x is defined for x in <b>%s</b>, the range of %s." % (fn, DOM[fn], fn))


def one_sum(r):
    fns = r.sample(["sin", "cos", "tan", "cot", "sec", "cosec"], r.choice([2, 2, 3]))
    terms, tot = [], F(0)
    for fn in fns:
        v, ang = r.choice([kv for kv in VALS[fn].items() if kv[1] != 0])
        terms.append("%s<sup>−1</sup>(%s)" % (fn, v))
        tot += ang
    wrong = tot + F(1, 3) if tot + F(1, 3) != 0 else tot + F(1, 2)
    return T2("Find the value of %s." % " + ".join(terms), pi(tot), [pi(-tot) if tot else pi(1), pi(wrong), pi(tot + 1) if tot + 1 not in (-tot,) else pi(tot - F(1, 2))],
              "Find each principal value and add: <b>%s</b>." % pi(tot))


def one_ss(r):
    fn = r.choice(["sin", "cos", "tan"])
    ang = r.choice({"sin": [F(2, 3), F(3, 4), F(5, 6), F(7, 6), F(4, 3), F(5, 4)], "cos": [F(7, 6), F(4, 3), F(5, 3), F(7, 4), F(3, 2), F(-1, 3)],
                    "tan": [F(3, 4), F(2, 3), F(5, 6), F(7, 6), F(5, 4), F(4, 3)]}[fn])
    if fn == "sin":
        cand = [1 - ang, ang - 1, ang - 2, 2 - ang, ang + 1, -ang, ang]
        res = [c for c in cand if -F(1, 2) <= c <= F(1, 2)]
    elif fn == "cos":
        cand = [ang, -ang, 2 - ang, ang - 2, ang + 2]
        res = [c for c in cand if 0 <= c <= 1]
    else:
        cand = [ang - 1, ang + 1, ang - 2, ang]
        res = [c for c in cand if -F(1, 2) < c < F(1, 2)]
    if not res:
        return None
    val = res[0]
    return T2("Find the value of %s<sup>−1</sup>(%s %s)." % (fn, fn, pi(ang)), pi(val), [pi(ang), pi(-val) if val else pi(1), pi(1 - val) if 1 - val not in (val, ang) else pi(val + F(1, 2))],
              "%s<sup>−1</sup>(%s θ) = θ only when θ is in %s. %s %s = %s %s, and %s is in the branch, so the answer is <b>%s</b>." % (fn, fn, BR[fn], fn, pi(ang), fn, pi(val), pi(val), pi(val)))


def one_id(r):
    v = r.choice(["2", "3", "1/2", "√5", "−4", "7", "−1/3"])
    k = r.choice(["tc", "sc"])
    if k == "tc":
        return T2("Find tan<sup>−1</sup>(%s) + cot<sup>−1</sup>(%s)." % (v, v), "π/2", ["π", "0", "π/4"],
                  "For every real x, tan<sup>−1</sup> x + cot<sup>−1</sup> x = <b>π/2</b>.")
    w = r.choice(["1/3", "2/5", "−3/4", "0.6", "−1/5"])
    return T2("Find sin<sup>−1</sup>(%s) + cos<sup>−1</sup>(%s)." % (w, w), "π/2", ["π", "0", "π/4"],
              "For x in [−1, 1], sin<sup>−1</sup> x + cos<sup>−1</sup> x = <b>π/2</b>.")


U(12, 2, "inverse-trigonometric-functions", 2, "RF", "Inverse Trigonometric Functions: Principal Values, Domains and Ranges", "inverse trigonometric functions",
  "Definition, range, domain, principal value branch; graphs of inverse trigonometric functions (summary of the CBSE syllabus)",
  "Class 12 Inverse Trigonometric Functions worksheet (NCERT Chapter 2): principal values of sin⁻¹, cos⁻¹, tan⁻¹, cot⁻¹, sec⁻¹ and cosec⁻¹, domains, ranges and expressions. 100 questions with answers.",
  "The answer must lie in the principal value branch.", "sin⁻¹: [−π/2, π/2]; cos⁻¹: [0, π]; tan⁻¹: (−π/2, π/2).",
  "<ul><li>Principal value branches: sin<sup>−1</sup> [−π/2, π/2], cos<sup>−1</sup> [0, π], tan<sup>−1</sup> (−π/2, π/2), cot<sup>−1</sup> (0, π), sec<sup>−1</sup> [0, π] − {π/2}, cosec<sup>−1</sup> [−π/2, π/2] − {0}.</li>"
  "<li>Domains: sin<sup>−1</sup> and cos<sup>−1</sup> [−1, 1]; tan<sup>−1</sup> and cot<sup>−1</sup> R; sec<sup>−1</sup> and cosec<sup>−1</sup> R − (−1, 1).</li>"
  "<li>sin<sup>−1</sup>(sin θ) = θ only if θ is in [−π/2, π/2]; otherwise find the angle in the branch with the same sine.</li>"
  "<li>sin<sup>−1</sup> x + cos<sup>−1</sup> x = π/2 and tan<sup>−1</sup> x + cot<sup>−1</sup> x = π/2.</li></ul>",
  [("Find the principal value of cos<sup>−1</sup>(−1/2).", ["cos(π/3) = 1/2", "In [0, π], cos(π − π/3) = −1/2"], "2π/3")],
  ["Giving −π/3 for cos⁻¹(−1/2) (it is outside [0, π]).", "Writing sin⁻¹(sin 2π/3) = 2π/3.", "Reading sin⁻¹ x as 1/sin x."],
  [("Why is a principal value branch needed?", "sin x is not one-one on R, so its inverse needs a restricted range."),
   ("Is sin⁻¹ x the same as (sin x)⁻¹?", "No. sin⁻¹ x is an angle; (sin x)⁻¹ = cosec x.")],
  [("Principal values", [(one_pv, 14), (exact, 6)]),
   ("Domains and ranges", [(one_branch, 12), (dr, 8)]),
   ("Sums of principal values", [(one_sum, 16), (one_id, 4)]),
   ("sin⁻¹(sin θ) and similar", [(one_ss, 14), (comp, 6)]),
   ("Mixed problems", [(one_pv, 6), (comp, 8), (one_sum, 6)])], 912102)
