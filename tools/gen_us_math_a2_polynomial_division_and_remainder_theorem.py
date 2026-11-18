# -*- coding: utf-8 -*-
"""
US Algebra 2: Polynomial Division and the Remainder Theorem (Common Core A-APR.B.2, A-APR.D.6)
  python3 tools/gen_us_math_a2_polynomial_division_and_remainder_theorem.py
Dividing by a monomial, long division, synthetic division, the Remainder Theorem, the Factor Theorem and
factoring completely from one known factor.
Wrong answers come from real mistakes: using a instead of −a in synthetic division (or the reverse),
forgetting a zero placeholder for a missing term, adding instead of subtracting in long division, and
evaluating P(−a) instead of P(a).
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People
from a2_common import X, poly, sf, ps, lin, pmul, peval, synth, xp

R = random.Random(95201)


def rp(r, n, lo=-6, hi=6, lead=(1, 1, 2, 3)):
    cs = [r.choice(lead)] + [r.randint(lo, hi) for _ in range(n)]
    return cs


# ------------------------------------------------------------ set 1: divide by a monomial and long division
def one_long(r):
    if r.random() < 0.35:
        k = r.choice([2, 3, 4, 5])
        e_ = r.choice([1, 2])
        q_ = [r.randint(1, 6) * r.choice([1, -1]) for _ in range(3)]
        top = [c * k for c in q_] + [0] * e_
        q = "Divide %s by %s." % (B(poly(top)), B(num(k) + xp(e_)))
        right = poly(q_)
        wr = [poly([c * k for c in q_]), poly(q_ + [0]), poly(q_[:-1] + [q_[-1] * k])]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Divide every term by %s: divide each coefficient by %d and subtract %d from each exponent. <b>%s</b>." % (num(k) + xp(e_), k, e_, right))
    a = r.choice([x for x in range(-5, 6) if x])
    qt = rp(r, 1, -5, 6, (1, 1, 2))
    rem = r.choice([0, 0, r.randint(-9, 9)])
    p = pmul(qt, [1, -a])
    p[-1] += rem
    q = "Use long division: %s." % B("(%s) ÷ (%s)" % (poly(p), lin(a)))
    right = poly(qt) + (" + %s/(%s)" % (sf(rem), lin(a)) if rem > 0 else (" %s %s/(%s)" % (MINUS, num(-rem), lin(a)) if rem < 0 else ""))
    q2, r2 = synth(p, -a)
    wrong_sign = poly(q2) + (" + %s/(%s)" % (sf(r2), lin(a)) if r2 > 0 else (" %s %s/(%s)" % (MINUS, num(-r2), lin(a)) if r2 < 0 else ""))
    wr = [wrong_sign, poly(qt[:-1] + [qt[-1] + 1]) + right[len(poly(qt)):], poly(qt)]
    if rem == 0:
        wr[2] = poly(qt[:-1] + [qt[-1] - 2])
    e = "Divide the first terms, multiply, subtract, bring down, and repeat. The quotient is %s%s." % (
        poly(qt), " with remainder %s" % sf(rem) if rem else " with no remainder")
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: synthetic division
def one_syn(r):
    a = r.choice([x for x in range(-4, 5) if x])
    deg = r.choice([2, 3, 3])
    p = rp(r, deg, -7, 7, (1, 1, 2))
    if r.random() < 0.3 and deg == 3:
        p[2] = 0
    qt, rem = synth(p, a)
    q = "Use synthetic division to divide %s by (%s). What is the quotient and the remainder?" % (B(poly(p)), lin(a))
    right = "%s, remainder %s" % (poly(qt), sf(rem))
    q2, r2 = synth(p, -a)
    wr = ["%s, remainder %s" % (poly(q2), sf(r2)), "%s, remainder %s" % (poly(qt), sf(-rem)) if rem else "%s, remainder %s" % (poly(qt), sf(a)),
          "%s, remainder %s" % (poly(qt[:-1] + [qt[-1] - a]) if len(qt) > 1 else poly([qt[0] + 1]), sf(rem))]
    if 0 in p[1:]:
        wr.insert(0, "%s, remainder %s" % (poly(synth([c for c in p if c != 0] , a)[0]), sf(synth([c for c in p if c != 0], a)[1])))
    e = "Use %s (the zero of %s) in the box%s. Bring down %s, then multiply by %s and add across: %s. The last number is the remainder. <b>%s</b>." % (
        sf(a), lin(a), ", and write 0 for the missing term" if 0 in p[1:] else "", sf(p[0]), sf(a), ", ".join(sf(x) for x in qt + [rem]), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: remainder theorem
def one_rem(r):
    a = r.choice([x for x in range(-4, 5) if x])
    p = rp(r, r.choice([3, 3, 4]), -6, 6, (1, 1, 2, -1))
    rem = peval(p, a)
    kind = r.choice(["rem", "rem", "val"])
    if kind == "rem":
        q = "Use the Remainder Theorem to find the remainder when %s is divided by (%s)." % (B(poly(p)), lin(a))
        e = "The remainder is P(%s). Substitute %s: <b>%s</b>." % (sf(a), sf(a), sf(rem))
    else:
        q = "P(<i>x</i>) = %s. Synthetic division by (%s) gives remainder <i>r</i>. What is P(%s)?" % (poly(p), lin(a), sf(a))
        e = "Remainder Theorem: P(%s) equals the remainder after dividing by (%s). Substituting gives <b>%s</b>." % (sf(a), lin(a), sf(rem))
    wr = [peval(p, -a), -rem, peval(p, a) - p[-1], rem + 2 * a]
    return T(q, sf(rem), [sf(w) for w in dict.fromkeys(wr) if w != rem][:3], e)


# ------------------------------------------------------------ set 4: factor theorem
def one_fac(r):
    kind = r.choice(["is", "is", "k", "k"])
    if kind == "is":
        roots = r.sample([x for x in range(-5, 6) if x], 3)
        p = [1]
        for z in roots:
            p = pmul(p, [1, -z])
        good = r.random() < 0.5
        a = r.choice(roots) if good else r.choice([x for x in range(-5, 6) if x and x not in roots])
        val = peval(p, a)
        q = "Is (%s) a factor of %s?" % (lin(a), B(poly(p)))
        right = "Yes, because P(%s) = 0" % sf(a) if good else "No, because P(%s) = %s" % (sf(a), sf(val))
        wr = ["Yes, because P(%s) = 0" % sf(-a) if (-a) in roots and not good else ("Yes, because the constant term is divisible by %d" % abs(a)) if abs(a) > 1 else "Yes, because the leading coefficient is 1",
              "No, because P(%s) ≠ 0" % sf(-a) if good else "Yes, because P(%s) = %s" % (sf(a), sf(val)),
              "It cannot be decided without long division"]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Factor Theorem: (%s) is a factor exactly when P(%s) = 0. P(%s) = %s. <b>%s</b>." % (lin(a), sf(a), sf(a), sf(val), right))
    a = r.choice([x for x in range(-3, 4) if x])
    p = rp(r, 3, -6, 6, (1, 2))
    p[-1] = 0
    k = -peval(p, a)
    p[-1] = k
    if k == 0:
        return None
    shown = p[:-1]
    q = "Find <i>k</i> so that (%s) is a factor of %s + <i>k</i>." % (lin(a), B(poly(shown + [0])))
    return T(q, sf(k), [sf(w) for w in dict.fromkeys([-k, peval(shown + [0], -a) * -1, k + a]) if w != k][:3],
             "For (%s) to be a factor, P(%s) = 0. P(%s) = %s + <i>k</i> = 0, so <i>k</i> = <b>%s</b>." % (lin(a), sf(a), sf(a), sf(-k), sf(k)))


# ------------------------------------------------------------ set 5: factor completely and problems
def one_full(r):
    if r.random() < 0.7:
        roots = r.sample([x for x in range(-5, 6) if x], 3)
        p = [1]
        for z in roots:
            p = pmul(p, [1, -z])
        a = roots[0]
        q = "(%s) is a factor of %s. Factor the polynomial completely." % (lin(a), B(poly(p)))
        fs = sorted(roots, reverse=True)
        right = "".join("(%s)" % lin(z) for z in fs)
        wr = ["".join("(%s)" % lin(-z) for z in fs), "(%s)(%s)(%s)" % (lin(fs[0]), lin(-fs[1]), lin(fs[2])), "(%s)(%s)" % (lin(a), poly(synth(p, a)[0]))]
        b, c = roots[1], roots[2]
        e = "Divide by (%s) to get %s. Factor this quadratic: (%s)(%s). <b>%s</b>." % (lin(a), poly(synth(p, a)[0]), lin(b), lin(c), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    w = r.randint(2, 6)
    l2 = r.randint(1, 5)
    h2 = r.randint(1, 4)
    # volume (x + l2)(x + h2) * (x) ... box: V = x (x + l2)(x + h2)
    p = pmul(pmul([1, 0], [1, l2]), [1, h2])
    q = "The volume of a box is V(<i>x</i>) = %s. Its height is <i>x</i> + %d. What is the area of its base?" % (poly(p), h2)
    right = poly(pmul([1, 0], [1, l2]))
    return T(q, right, [poly(pmul([1, 0], [1, h2])), poly([1, l2 + h2, 0]) if l2 + h2 != l2 else poly([1, 1, 0]), poly([1, l2])],
             "Base area = volume ÷ height. Dividing %s by (<i>x</i> + %d) gives <b>%s</b>." % (poly(p), h2, right))


def build():
    sets = [S("Divide by a monomial and long division", collect(one_long, 20, R)),
            S("Synthetic division", collect(one_syn, 20, R)),
            S("Remainder Theorem", collect(one_rem, 20, R)),
            S("Factor Theorem", collect(one_fac, 20, R)),
            S("Factor completely and problems", collect(one_full, 20, R))]
    body = lesson(
        "<p><b>Long division</b> works like number division: divide the first terms, multiply, subtract, bring down, and repeat.</p>"
        "<p><b>Synthetic division</b> is a shortcut for dividing by (<i>x</i> %s <i>a</i>). Put <i>a</i> in the box, write the coefficients (0 for any missing term), "
        "bring down the first one, multiply by <i>a</i>, add, and repeat. The last number is the remainder.</p>"
        "<ul><li><b>Remainder Theorem</b>: dividing P(<i>x</i>) by (<i>x</i> %s <i>a</i>) leaves remainder P(<i>a</i>).</li>"
        "<li><b>Factor Theorem</b>: (<i>x</i> %s <i>a</i>) is a factor exactly when P(<i>a</i>) = 0.</li></ul>" % (MINUS, MINUS, MINUS),
        [("Divide <i>x</i>³ %s 2<i>x</i>² %s 5<i>x</i> + 6 by (<i>x</i> %s 3)." % (MINUS, MINUS, MINUS), ["Box: 3. Coefficients 1, %s2, %s5, 6" % (MINUS, MINUS), "Bottom row: 1, 1, %s2, 0" % MINUS],
          "<i>x</i>² + <i>x</i> %s 2, remainder 0" % MINUS),
         ("Is (<i>x</i> + 2) a factor of <i>x</i>³ + 8?", ["P(%s2) = %s8 + 8 = 0" % (MINUS, MINUS)], "Yes")],
        ["Putting %s3 in the box for (<i>x</i> %s 3). Use the zero of the divisor: 3." % (MINUS, MINUS),
         "Leaving out a missing term. Write 0 for it, or the columns shift.",
         "Subtracting wrongly in long division. Subtract the whole product: change every sign.",
         "Checking P(%s<i>a</i>) instead of P(<i>a</i>) for the factor (<i>x</i> %s <i>a</i>)." % (MINUS, MINUS)])
    faq = [("What is the Remainder Theorem?", "When a polynomial P(x) is divided by (x − a), the remainder is P(a)."),
           ("What is the Factor Theorem?", "(x − a) is a factor of P(x) exactly when P(a) = 0."),
           ("When can you use synthetic division?", "When you divide by a linear factor of the form x − a. For x + 3, use −3 in the box."),
           ("Why do you need a zero placeholder?", "Each column stands for one power of x. A missing term must be written as 0 so the other coefficients stay in the right columns.")]
    make("polynomial-division-and-remainder-theorem", 2, "A-APR.B.2",
         "Polynomial Division and the Remainder Theorem",
         "Polynomial Long and Synthetic Division Worksheet, Remainder Theorem (Algebra 2) | 100 Questions",
         "Polynomial Division",
         "Know and apply the Remainder Theorem: For a polynomial p(x) and a number a, the remainder on division by x − a is p(a), so p(a) = 0 if and only if (x − a) is a factor of p(x).",
         "Free Algebra 2 worksheet on polynomial division: long division, synthetic division, the Remainder Theorem, the Factor Theorem and factoring completely. 100 questions with answers.",
         "The remainder when P(x) is divided by (x − a) is P(a).",
         "(x − a) is a factor exactly when P(a) = 0.",
         body, faq, sets, R, domain="Polynomials", grade="algebra-2")


if __name__ == "__main__":
    build()
