# -*- coding: utf-8 -*-
"""
US Algebra 1: Simplifying Radicals (Common Core N-RN.A.2, N-RN.B.3)
  python3 tools/gen_us_math_a1_simplifying_radicals.py
Simplifying square roots by taking out perfect squares, radicals with variables, adding and subtracting
like radicals, multiplying radicals and rationalizing a denominator, and rational or irrational results
with exact answers in geometry.
Wrong answers come from real mistakes: taking out a factor that is not the largest perfect square, adding
the numbers under the root (√2 + √3 ≠ √5), adding unlike radicals, and multiplying the outside number into
the root.
"""
import random
from math import isqrt
from us_hs import num, B, S, make, lesson, collect, T, fr, MINUS

R = random.Random(91101)
FREE = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]


def rad(c, n, v=""):
    """c√(n v); c may be 1; n square-free."""
    if n == 1 and not v:
        return num(c)
    inside = (num(n) if n != 1 else "") + v
    inner = "√" + (inside if len(inside) <= 3 and "<" not in inside else "(%s)" % inside)
    if "<" in inside:
        inner = "√(%s)" % inside
    return (num(c) if c != 1 else "") + inner


def simp(n):
    a = 1
    for k in range(isqrt(n), 1, -1):
        if n % (k * k) == 0:
            a = k
            break
    return a, n // (a * a)


# ------------------------------------------------------------ set 1: simplify √n
def one_simp(r):
    a = r.choice([2, 3, 4, 5, 6, 7, 8, 10])
    b = r.choice(FREE)
    n = a * a * b
    if n > 600:
        return None
    q = "Simplify %s." % B("√%s" % num(n))
    right = rad(a, b)
    small = [k for k in range(2, a) if a % k == 0]
    wr = []
    if small:
        k = small[0]
        wr.append(rad(k, n // (k * k)))
    wr += [rad(b, a * a) if a * a < 50 else rad(a * a, b), rad(a, b * 2) if b * 2 not in (4,) else rad(a + 1, b), rad(a * 2, b), rad(b, a)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    e = "Find the largest perfect square factor: %s = %d × %d. So √%s = √%d × √%d = <b>%s</b>." % (num(n), a * a, b, num(n), a * a, b, right)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 2: with variables
def one_var(r):
    a = r.choice([2, 3, 4, 5, 6])
    b = r.choice([1, 2, 3, 5, 6, 7])
    p = r.choice([2, 3, 4, 5, 6, 7])
    n = a * a * b
    inside = "%s<i>x</i><sup>%d</sup>" % (num(n), p)
    q = "Simplify %s, where <i>x</i> ≥ 0." % B("√(%s)" % inside)
    outx = "<i>x</i>" + ("<sup>%d</sup>" % (p // 2) if p // 2 > 1 else "")
    inx = "<i>x</i>" if p % 2 else ""
    coef = num(a) + outx
    rest = (num(b) if b != 1 else "") + inx
    right = coef + (("√%s" % rest if "<" not in rest else "√(%s)" % rest) if rest else "")
    def mk(c, rest):
        if not rest:
            return c
        return c + ("√%s" % rest if "<" not in rest else "√(%s)" % rest)
    wr = [mk(num(a) + "<i>x</i><sup>%d</sup>" % p, (num(b) if b != 1 else "")),
          mk(num(a * a) + outx, (num(b) if b != 1 else "") + inx),
          mk(num(a) + ("<i>x</i><sup>%d</sup>" % (p - 1) if p > 2 else "<i>x</i>"), (num(b) if b != 1 else "") + ("<i>x</i>" if not inx else ""))]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    e = "√%s = %d%s, and <i>x</i><sup>%d</sup> = %s. Take the square roots of the perfect squares: <b>%s</b>." % (
        num(a * a), a, "" if b == 1 else " (leaving %d inside)" % b,
        p, ("(<i>x</i><sup>%d</sup>)<sup>2</sup>" % (p // 2) if p // 2 > 1 else "(<i>x</i>)<sup>2</sup>") + (" · <i>x</i>" if inx else ""), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: add and subtract
def one_add(r):
    b = r.choice([2, 3, 5, 6, 7])
    k1, k2 = r.choice([1, 2, 3, 4, 5]), r.choice([2, 3, 4])
    c1 = r.choice([1, 2, 3, 4, 5])
    sign = r.choice([1, -1])
    n2 = k2 * k2 * b
    q = "Simplify %s." % B("%s %s √%s" % (rad(c1, b), "+" if sign > 0 else MINUS, num(n2)))
    tot = c1 + sign * k2
    if tot == 0:
        return None
    right = rad(tot, b) if tot > 0 else MINUS + rad(-tot, b)
    wr = [rad(c1 + 1, b) if sign > 0 else rad(c1 + k2, b),
          "√%s" % num(b + n2) if sign > 0 else "√%s" % num(abs(n2 - b)),
          (rad(c1 * k2, b) if sign > 0 else rad(c1 + k2, b)),
          rad(tot, b * 2) if tot > 0 else rad(-tot, b)]
    wr = [w for w in dict.fromkeys(wr) if w != right][:3]
    e = "Simplify first: √%s = %s. Now the radicals are alike, so combine the numbers in front: %d %s %d = %s. <b>%s</b>." % (
        num(n2), rad(k2, b), c1, "+" if sign > 0 else MINUS, k2, num(tot), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: multiply and rationalize
def one_mul(r):
    kind = r.choice(["mm", "mm", "dist", "conj", "rat"])
    if kind == "mm":
        a, b = r.choice([2, 3, 5, 6, 10, 12, 15]), r.choice([2, 3, 5, 6, 8, 10, 15])
        c1, c2 = r.choice([1, 2, 3]), r.choice([1, 2, 4])
        o, i = simp(a * b)
        right = rad(c1 * c2 * o, i)
        q = "Simplify %s." % B("%s · %s" % (rad(c1, a), rad(c2, b)))
        wr = [rad(c1 * c2, a * b) if o != 1 else rad(c1 + c2, a * b), rad(c1 + c2, i) if c1 + c2 != c1 * c2 else rad(c1 * c2 + 1, i), rad(o, i * c1 * c2) if c1 * c2 > 1 else rad(o * 2, i)]
        e = "Multiply outside numbers and inside numbers: %d√%d = %s. <b>%s</b>." % (c1 * c2, a * b, "%d × √%d" % (c1 * c2, a * b) if o == 1 else "%d × %d√%d" % (c1 * c2, o, i), right)
    elif kind == "dist":
        a = r.choice([2, 3, 5])
        k = r.choice([2, 3, 4])
        c = r.choice([2, 3, 5, 6])
        q = "Simplify %s." % B("√%d(%d + √%d)" % (a, k, a))
        right = "%s + %d" % (rad(k, a), a)
        wr = ["%s + %d" % (rad(k, a), a * a), "%d + √%d" % (k, a * 2), rad(k + 1, a)]
        e = "Distribute: √%d × %d = %s and √%d × √%d = %d. <b>%s</b>." % (a, k, rad(k, a), a, a, a, right)
    elif kind == "conj":
        a = r.choice([3, 4, 5, 6, 7])
        b = r.choice([2, 3, 5, 7])
        if a * a == b:
            return None
        q = "Simplify %s." % B("(%d + √%d)(%d − √%d)" % (a, b, a, b))
        v = a * a - b
        right = num(v)
        wr = [num(a * a + b), "%d − %d√%d" % (a * a, 2, b), num(a * a - b * b)]
        e = "This is a difference of squares: %d<sup>2</sup> − (√%d)<sup>2</sup> = %d − %d = <b>%d</b>." % (a, b, a * a, b, v)
    else:
        b = r.choice([2, 3, 5, 6, 7])
        k = r.choice([1, 2, 3])
        top = k * b
        q = "Rationalize the denominator: %s." % B(fr(num(top), "√%d" % b))
        right = rad(k, b)
        wr = [fr(rad(top, b), num(b * b)) if False else rad(top, b), fr(num(top), num(b)), num(top * b)]
        e = "Multiply top and bottom by √%d: %s = <b>%s</b>." % (b, fr(rad(top, b), num(b)), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 5: exact answers and rational/irrational
def problems():
    data = [
        ("A right triangle has legs 4 cm and 8 cm. What is the exact length of the hypotenuse?", "4√5 cm", ["12 cm", "√12 cm", "8√2 cm"], "√(16 + 64) = √80 = √16 × √5 = <b>4√5 cm</b>."),
        ("A square has a diagonal of 10 in. What is the exact side length?", "5√2 in.", ["5 in.", "10√2 in.", "√50 + 0 in."], "<i>s</i>√2 = 10, so <i>s</i> = 10/√2 = <b>5√2 in.</b>"),
        ("A square has an area of 72 m². What is its exact side length?", "6√2 m", ["36 m", "8.5 m exactly", "2√6 m"], "√72 = √36 × √2 = <b>6√2 m</b>."),
        ("Is √2 + √8 rational or irrational?", "Irrational, it equals 3√2", ["Rational, it equals √10", "Rational, it equals 4", "Irrational, it equals √10"], "√8 = 2√2, so the sum is 3√2, which is <b>irrational</b>."),
        ("Is √3 × √12 rational or irrational?", "Rational, it equals 6", ["Irrational, it equals √36", "Irrational, it equals 6√3", "Rational, it equals 36"], "√3 × √12 = √36 = <b>6</b>, a rational number."),
        ("Which sum is rational?", "(3 + √5) + (2 − √5)", ["3 + √5", "√5 + √5", "2 + √4 + √3"], "The √5 terms cancel, leaving <b>5</b>."),
        ("The sum of a rational number and an irrational number is always…", "Irrational", ["Rational", "An integer", "Zero"], "If it were rational, subtracting the rational number would make the irrational number rational. So the sum is <b>irrational</b>."),
        ("The product of a nonzero rational number and an irrational number is always…", "Irrational", ["Rational", "An integer", "1"], "For example 3√2 is irrational. The product is always <b>irrational</b>."),
        ("Which is equal to √50?", "5√2", ["25√2", "2√5", "10√5"], "50 = 25 × 2, so √50 = <b>5√2</b>."),
        ("Ethan writes √9 + √16 = √25 = 5. What is the correct value?", "7", ["5", "25", "12"], "√9 = 3 and √16 = 4, so the sum is <b>7</b>. You cannot add the numbers under the roots."),
        ("Which pair are like radicals?", "2√3 and 5√3", ["2√3 and 3√2", "√3 and √30", "3√5 and 5√3"], "Like radicals have the same number under the root: <b>2√3 and 5√3</b>."),
        ("A rectangle is √12 cm by √3 cm. What is its area?", "6 cm²", ["√15 cm²", "3√2 cm²", "36 cm²"], "√12 × √3 = √36 = <b>6 cm²</b>."),
        ("A rectangle is √12 cm by √3 cm. What is its perimeter in simplest form?", "6√3 cm", ["2√15 cm", "√30 cm", "3√3 cm"], "2(2√3 + √3) = 2 × 3√3 = <b>6√3 cm</b>."),
        ("Which is between 7 and 8?", "√58", ["√48", "√65", "√70"], "7<sup>2</sup> = 49 and 8<sup>2</sup> = 64, so <b>√58</b> is between them."),
        ("Simplify √(<i>x</i><sup>2</sup>), where <i>x</i> ≥ 0.", "<i>x</i>", ["<i>x</i><sup>2</sup>", "2<i>x</i>", "√<i>x</i>"], "The square root undoes the square: <b><i>x</i></b>."),
        ("Which is the simplest form of " + fr("√20", "2") + "?", "√5", ["√10", "2√5", "10"], "√20 = 2√5, and 2√5 ÷ 2 = <b>√5</b>."),
        ("The distance between (1, 2) and (4, 8) is √45. What is this in simplest form?", "3√5", ["5√3", "9√5", "√45 is already simplest"], "45 = 9 × 5, so √45 = <b>3√5</b>."),
        ("Which is larger: 3√5 or 5√2?", "3√5", ["5√2", "They are equal", "You cannot tell"], "3√5 = √45 and 5√2 = √50… compare: √45 &lt; √50, so <b>5√2</b> is larger."),
        ("Simplify (√7)<sup>2</sup>.", "7", ["49", "√14", "14"], "Squaring a square root gives the number inside: <b>7</b>."),
        ("Simplify 2√3 · 4√3.", "24", ["8√3", "8√6", "6√3"], "2 × 4 = 8 and √3 × √3 = 3, so 8 × 3 = <b>24</b>."),
    ]
    out = []
    for q, a, w, e in data:
        if q.startswith("Which is larger: 3√5 or 5√2?"):
            a, w, e = "5√2", ["3√5", "They are equal", "You cannot tell"], "3√5 = √45 and 5√2 = √50. Since 45 &lt; 50, <b>5√2</b> is larger."
        if q.startswith("A square has a diagonal"):
            w = ["5 in.", "10√2 in.", "√5 in."]
        if q.startswith("A square has an area of 72"):
            w = ["36 m", "8√2 m", "2√6 m"]
        out.append(T(q, a, w, e))
    return out


def body():
    return lesson(
        "<p>To simplify a square root, find the <b>largest perfect square factor</b> and take its root outside: "
        "√72 = √36 × √2 = 6√2. With variables, even powers come out: √(<i>x</i><sup>6</sup>) = <i>x</i><sup>3</sup>.</p>"
        "<p>Add or subtract only <b>like radicals</b> (same number under the root): 3√2 + 5√2 = 8√2. Simplify first: √2 + √8 = √2 + 2√2 = 3√2.</p>"
        "<p>Multiply: √<i>a</i> · √<i>b</i> = √(<i>ab</i>). To <b>rationalize</b> a denominator, multiply top and bottom by the root: "
        "6/√3 = 6√3/3 = 2√3.</p>",
        [("Simplify √48.", ["48 = 16 × 3.", "√16 = 4."], "4√3"),
         ("Simplify 3√2 + √18.", ["√18 = 3√2.", "3√2 + 3√2."], "6√2"),
         ("Simplify √6 · √10.", ["√60 = √4 × √15."], "2√15")],
        ["Not using the largest perfect square: √72 = 2√18 is not finished; it is 6√2.",
         "Adding the numbers under the root: √2 + √3 is not √5.",
         "Combining unlike radicals: 2√3 + 3√2 cannot be simplified.",
         "Putting the outside number under the root: 3√2 is √18, not √6."])


def main():
    sets = [S("Simplify square roots", collect(one_simp, 20, R)),
            S("Radicals with variables", collect(one_var, 20, R)),
            S("Add and subtract radicals", collect(one_add, 20, R)),
            S("Multiply radicals and rationalize", collect(one_mul, 20, R)),
            S("Exact answers, rational and irrational", problems())]
    make("simplifying-radicals", 11, "N-RN.A.2",
         "Simplifying Radicals: Square Roots, Variables, Adding and Multiplying",
         "Algebra 1 Simplifying Radicals Worksheets: Square Roots, Adding, Multiplying and Rationalizing (Free, Answer Key)",
         "Simplifying radicals",
         "Rewrite expressions involving radicals and rational exponents using the properties of exponents.",
         "Free Algebra 1 simplifying radicals worksheets (N-RN.A.2, N-RN.B.3): simplify square roots, radicals with variables, add and "
         "subtract like radicals, multiply and rationalize denominators, and exact answers. 100 questions with an answer key.",
         "Take out the largest perfect square: √72 = √36 · √2 = 6√2.",
         "Only like radicals can be added. √a · √b = √(ab).",
         body(),
         [("How do you simplify a radical?", "Write the number as a perfect square times another factor, using the largest perfect square you can. Take the square root of the perfect square outside: √50 = √25 · √2 = 5√2."),
          ("Can you add √2 and √3?", "No. Only like radicals (the same number under the root) can be added. √2 + √3 stays as it is."),
          ("How do you multiply radicals?", "Multiply the numbers outside and the numbers inside separately, then simplify: 2√3 · 5√6 = 10√18 = 30√2."),
          ("What does it mean to rationalize the denominator?", "Rewrite a fraction so there is no square root in the denominator, by multiplying the top and bottom by that root.")],
         sets, R, domain="Exponents & Exponential Functions")


if __name__ == "__main__":
    main()
