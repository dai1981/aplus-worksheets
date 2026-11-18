# -*- coding: utf-8 -*-
"""
US Algebra 2: Complex Numbers (Common Core N-CN.A.1, N-CN.A.2, N-CN.A.3, N-CN.C.7)
  python3 tools/gen_us_math_a2_complex_numbers.py
Square roots of negative numbers and powers of i, adding and subtracting, multiplying, dividing with the
conjugate, and solving quadratics with complex solutions.
Wrong answers come from real mistakes: writing i² as 1, multiplying √−a √−b as √(ab), forgetting to
distribute the minus sign, multiplying only the real parts, and dividing without the conjugate.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, expr

R = random.Random(95101)
I = "<i>i</i>"


def sf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def cx(a, b):
    """a + bi with nice signs"""
    a, b = F(a), F(b)
    if b == 0:
        return sf(a)
    if abs(b) == 1:
        bi = I
    else:
        bi = sf(abs(b)) + I
    if a == 0:
        return (MINUS if b < 0 else "") + bi
    return "%s %s %s" % (sf(a), "+" if b > 0 else MINUS, bi)


def rad(n):
    a = 1
    for k in range(math.isqrt(n), 1, -1):
        if n % (k * k) == 0:
            a = k
            break
    b = n // (a * a)
    return a, b


def radi(c, b):
    """c i √b"""
    if b == 1:
        return (num(c) if c != 1 else "") + I
    return (num(c) if c != 1 else "") + I + "√" + num(b)


def p(z):
    return "(%s)" % cx(*z)


# ------------------------------------------------------------ set 1: square roots of negatives and powers of i
def one_i(r):
    kind = r.choice(["sqrt", "sqrt", "pow", "pow", "prod"])
    if kind == "sqrt":
        a = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        b = r.choice([1, 1, 2, 3, 5, 6, 7])
        n = a * a * b
        q = "Simplify %s." % B("√%s%s" % (MINUS, num(n)))
        right = radi(a, b)
        wr = [MINUS + radi(a, b).replace(I, "") if b > 1 else MINUS + num(a), radi(1, n), (num(a) if a != 1 else "") + ("√" + num(b) if b > 1 else ""), MINUS + radi(a, b)]
        wr = [w for w in dict.fromkeys(wr) if w != right]
        e = "√%s%d = √%d · √%s1 = %s. <b>%s</b>." % (MINUS, n, n, MINUS, (num(a) + ("√" + num(b) if b > 1 else "")) + " · " + I, right)
        return T(q, right, wr[:3], e)
    if kind == "pow":
        n = r.randint(5, 99)
        val = ["1", I, MINUS + "1", MINUS + I][n % 4]
        q = "Simplify %s." % B(I + "<sup>%d</sup>" % n)
        e = "The powers of %s repeat every 4: %s, %s1, %s%s, 1. %d ÷ 4 leaves remainder %d, so %s<sup>%d</sup> = %s<sup>%d</sup> = <b>%s</b>." % (
            I, I, MINUS, MINUS, I, n, n % 4, I, n, I, n % 4, val)
        return T(q, val, [x for x in ["1", I, MINUS + "1", MINUS + I] if x != val], e)
    a, b = r.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    q = "Simplify %s." % B("√%s%d · √%s%d" % (MINUS, a * a, MINUS, b * b))
    ans = -a * b
    return T(q, sf(ans), [num(a * b), num(a * b) + I, MINUS + num(a * b) + I],
             "Write each root with %s first: %d%s · %d%s = %d%s² = %d(%s1) = <b>%s</b>. (Multiplying under one root, √%d, gives the wrong sign.)" % (
                 I, a, I, b, I, a * b, I, a * b, MINUS, sf(ans), a * a * b * b))


# ------------------------------------------------------------ set 2: add and subtract
def rz(r):
    return (r.randint(-9, 9), r.choice([x for x in range(-9, 10) if x != 0]))


def one_add(r):
    z, w = rz(r), rz(r)
    op = r.choice(["+", MINUS])
    s = 1 if op == "+" else -1
    ans = (z[0] + s * w[0], z[1] + s * w[1])
    if ans[1] == 0:
        return None
    q = "Simplify %s." % B("%s %s %s" % (p(z), op, p(w)))
    wr = [(z[0] + s * w[0], z[1] - s * w[1]), (z[0] - s * w[0], z[1] + s * w[1]), (z[0] + z[1], s * w[0] + w[1]) if False else (z[0] + s * w[1], z[1] + s * w[0])]
    if op == MINUS:
        wr.insert(0, (z[0] - w[0], z[1] + w[1]))
    right = cx(*ans)
    e = "Combine real parts and imaginary parts separately: (%s %s %s) + (%s %s %s)%s = <b>%s</b>." % (
        sf(z[0]), op, "(%s)" % sf(w[0]) if w[0] < 0 else sf(w[0]), sf(z[1]), op, "(%s)" % sf(w[1]) if w[1] < 0 else sf(w[1]), I, right)
    return T(q, right, [cx(*x) for x in dict.fromkeys(wr) if cx(*x) != right][:3], e)


# ------------------------------------------------------------ set 3: multiply
def one_mul(r):
    kind = r.choice(["bin", "bin", "bin", "conj", "sq"])
    z = rz(r)
    if kind == "conj":
        w = (z[0], -z[1])
    elif kind == "sq":
        w = z
    else:
        w = rz(r)
    a, b = z
    c, d = w
    ans = (a * c - b * d, a * d + b * c)
    if kind == "sq":
        q = "Simplify %s." % B("%s²" % p(z))
    else:
        q = "Simplify %s." % B("%s%s" % (p(z), p(w)))
    right = cx(*ans)
    wr = [(a * c + b * d, a * d + b * c), (a * c, b * d), (a * c - b * d, 0) if ans[1] != 0 else (a * c + b * d, 1), (a * c - b * d, a * d - b * c)]
    e = "FOIL: %s + %s%s + %s%s + %s%s². Since %s² = %s1, the last term is %s. Total: <b>%s</b>." % (
        sf(a * c), "(%s)" % sf(a * d) if a * d < 0 else sf(a * d), I, "(%s)" % sf(b * c) if b * c < 0 else sf(b * c), I,
        "(%s)" % sf(b * d) if b * d < 0 else sf(b * d), I, I, MINUS, sf(-b * d), right)
    return T(q, right, [cx(*x) for x in dict.fromkeys(wr) if cx(*x) != right][:3], e)


# ------------------------------------------------------------ set 4: divide, conjugate and modulus
def one_div(r):
    kind = r.choice(["div", "div", "div", "conj", "abs"])
    if kind == "conj":
        z = rz(r)
        q = "What is the complex conjugate of %s?" % B(cx(*z))
        right = cx(z[0], -z[1])
        return T(q, right, [cx(-z[0], z[1]), cx(-z[0], -z[1]), cx(z[1], z[0]) if z[0] != 0 else sf(z[1])],
                 "The conjugate keeps the real part and changes the sign of the imaginary part: <b>%s</b>. Their product is a real number." % right)
    if kind == "abs":
        a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)])
        a *= r.choice([1, -1])
        b *= r.choice([1, -1])
        q = "Find the absolute value (modulus) of %s." % B(cx(a, b))
        return T(q, num(c), [num(abs(a) + abs(b)), num(c * c), num(abs(a - b)) if a != b else num(c + 1)],
                 "|<i>a</i> + <i>bi</i>| = √(<i>a</i>² + <i>b</i>²) = √(%d + %d) = <b>%d</b>, the distance from 0 in the complex plane." % (a * a, b * b, c))
    w = rz(r)
    ans = rz(r)
    z = (ans[0] * w[0] - ans[1] * w[1], ans[0] * w[1] + ans[1] * w[0])
    if r.random() < 0.3:
        z = (r.randint(2, 30), 0)
        n2 = w[0] ** 2 + w[1] ** 2
        ans = (F(z[0] * w[0], n2), F(-z[0] * w[1], n2))
        if ans[0].denominator > 5 or ans[1].denominator > 5:
            return None
    q = "Simplify %s." % B("%s ÷ %s" % (cx(*z) if z[1] == 0 else p(z), p(w)))
    right = cx(*ans)
    n2 = w[0] ** 2 + w[1] ** 2
    wr = [(F(z[0], w[0]) if w[0] else F(z[0]), F(z[1], w[1])), (ans[0], -ans[1]), (-ans[0], ans[1]), (ans[1], ans[0])]
    e = "Multiply the top and bottom by the conjugate %s. The bottom becomes %d² + %d² = %d. Simplify: <b>%s</b>." % (
        cx(w[0], -w[1]), abs(w[0]), abs(w[1]), n2, right)
    return T(q, right, [cx(*x) for x in dict.fromkeys(wr) if cx(*x) != right][:3], e)


# ------------------------------------------------------------ set 5: quadratics with complex solutions
def one_quad(r):
    kind = r.choice(["sq", "sq", "formula", "formula", "disc"])
    if kind == "sq":
        a = r.choice([1, 2, 3, 4])
        k = r.randint(1, 9)
        c = a * k * k
        q = "Solve %s." % B("%s<i>x</i>² + %d = 0" % ("" if a == 1 else num(a), c))
        right = "<i>x</i> = ±%s" % radi(k, 1)
        return T(q, right, ["<i>x</i> = ±%d" % k, "<i>x</i> = %s" % radi(k, 1), "<i>x</i> = ±%s" % radi(k * k, 1)],
                 ("%s<i>x</i>² = %s%d, so <i>x</i>² = %s%d and " % ("" if a == 1 else num(a), MINUS, c, MINUS, k * k) if a > 1 else "<i>x</i>² = %s%d, so " % (MINUS, c)) +
                 "<i>x</i> = ±√%s%d = <b>±%s</b>." % (MINUS, k * k, radi(k, 1)))
    if kind == "disc":
        b = r.randint(-8, 8)
        c = r.randint(-10, 15)
        a = r.choice([1, 1, 2])
        D = b * b - 4 * a * c
        if c == 0 and b == 0:
            return None
        q = "How many real solutions and how many nonreal (complex) solutions does %s have?" % B(expr([(a, "<i>x</i>²"), (b, "<i>x</i>"), (c, "")]) + " = 0")
        right = "Two real solutions" if D > 0 else ("One real solution" if D == 0 else "Two nonreal solutions")
        return T(q, right, [x for x in ["Two real solutions", "One real solution", "Two nonreal solutions", "No solutions at all"] if x != right],
                 "Discriminant: <i>b</i>² %s 4<i>ac</i> = %d %s %s = %s. %s. <b>%s</b>." % (
                     MINUS, b * b, MINUS, "(%s)" % sf(4 * a * c) if 4 * a * c < 0 else sf(4 * a * c), sf(D), "Positive: two real" if D > 0 else ("Zero: one real" if D == 0 else "Negative: two nonreal conjugates"), right))
    h = r.randint(-6, 6)
    k = r.randint(1, 6)
    # x^2 - 2h x + (h^2 + k^2) = 0  ->  x = h ± ki
    b, c = -2 * h, h * h + k * k
    eqs = expr([(1, "<i>x</i>²"), (b, "<i>x</i>"), (c, "")]) + " = 0"
    q = "Solve %s." % B(eqs)
    right = "<i>x</i> = %s" % (cx(h, k).replace(" + ", " ± ") if h != 0 else "±" + cx(0, k))
    wr = ["<i>x</i> = %s" % (cx(-h, k).replace(" + ", " ± ") if h != 0 else "±%d" % k), "<i>x</i> = %s ± %d" % (sf(h), k) if h != 0 else "<i>x</i> = ±%d" % (2 * k),
          "<i>x</i> = %s" % (cx(h, 2 * k).replace(" + ", " ± ") if h != 0 else "±" + cx(0, 2 * k))]
    D = b * b - 4 * c
    e = "Quadratic formula: <i>x</i> = (%s ± √(%s)) ÷ 2. √(%s%d) = %s, so <i>x</i> = <b>%s</b>." % (
        sf(-b), sf(D), MINUS, -D, radi(2 * k, 1), right.replace("<i>x</i> = ", ""))
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


def build():
    sets = [S("Square roots of negatives and powers of i", collect(one_i, 20, R)),
            S("Add and subtract complex numbers", collect(one_add, 20, R)),
            S("Multiply complex numbers", collect(one_mul, 20, R)),
            S("Divide, conjugates and absolute value", collect(one_div, 20, R)),
            S("Quadratics with complex solutions", collect(one_quad, 20, R))]
    body = lesson(
        "<p>The imaginary unit is <b><i>i</i> = √%s1</b>, so <b><i>i</i>² = %s1</b>. A <b>complex number</b> is <i>a</i> + <i>bi</i>, with a real part <i>a</i> and an imaginary part <i>b</i>.</p>"
        "<ul><li>√%s<i>n</i> = <i>i</i>√<i>n</i>. Take out the <i>i</i> before multiplying roots.</li>"
        "<li>Powers of <i>i</i> repeat every 4: <i>i</i>, %s1, %s<i>i</i>, 1.</li>"
        "<li>Add and subtract real parts and imaginary parts separately. Multiply with FOIL, then replace <i>i</i>² with %s1.</li>"
        "<li>To divide, multiply the top and bottom by the <b>conjugate</b> of the bottom (<i>a</i> + <i>bi</i> → <i>a</i> %s <i>bi</i>).</li></ul>"
        "<p>If the discriminant <i>b</i>² %s 4<i>ac</i> is negative, a quadratic has two nonreal solutions that are conjugates.</p>" % (
            MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS),
        [("Simplify (3 + 2<i>i</i>)(4 %s <i>i</i>)." % MINUS, ["12 %s 3<i>i</i> + 8<i>i</i> %s 2<i>i</i>²" % (MINUS, MINUS), "12 + 5<i>i</i> + 2"], "14 + 5<i>i</i>"),
         ("Simplify 10 ÷ (1 + 3<i>i</i>).", ["Multiply by (1 %s 3<i>i</i>)/(1 %s 3<i>i</i>)" % (MINUS, MINUS), "(10 %s 30<i>i</i>) ÷ 10" % MINUS], "1 %s 3<i>i</i>" % MINUS)],
        ["Writing <i>i</i>² = 1. It is %s1." % MINUS,
         "Multiplying √%s4 · √%s9 as √36 = 6. Write 2<i>i</i> · 3<i>i</i> = %s6." % (MINUS, MINUS, MINUS),
         "Forgetting to distribute the minus sign when subtracting a complex number.",
         "Dividing the real and imaginary parts separately. Use the conjugate."])
    faq = [("What is i in math?", "i is the imaginary unit, defined so that i² = −1. It lets us take square roots of negative numbers: √−9 = 3i."),
           ("How do you simplify powers of i?", "Divide the exponent by 4 and use the remainder: remainder 0 gives 1, 1 gives i, 2 gives −1, 3 gives −i."),
           ("How do you divide complex numbers?", "Multiply the numerator and denominator by the conjugate of the denominator, so the denominator becomes a real number."),
           ("When does a quadratic have complex solutions?", "When its discriminant b² − 4ac is negative. The two solutions are complex conjugates, a + bi and a − bi.")]
    make("complex-numbers", 1, "N-CN.A.2",
         "Complex Numbers: Operations and Quadratics",
         "Complex Numbers Worksheet: Powers of i, Multiplying, Dividing (Algebra 2) | 100 Questions",
         "Complex Numbers",
         "Use the relation i² = −1 and the commutative, associative, and distributive properties to add, subtract, and multiply complex numbers.",
         "Free Algebra 2 worksheet on complex numbers: square roots of negatives, powers of i, adding, multiplying, dividing with conjugates and complex solutions of quadratics. 100 questions.",
         "i² = −1. Combine real parts and imaginary parts separately.",
         "To divide, multiply by the conjugate of the denominator.",
         body, faq, sets, R, domain="Complex Numbers", grade="algebra-2")


if __name__ == "__main__":
    build()
