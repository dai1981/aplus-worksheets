# -*- coding: utf-8 -*-
"""
US Algebra 1: Adding, Subtracting and Multiplying Polynomials (Common Core A-APR.A.1)
  python3 tools/gen_us_math_a1_polynomial_operations.py
Degree, leading coefficient and standard form; adding and subtracting polynomials; multiplying a monomial by a
polynomial and two binomials (FOIL); special products and a binomial times a trinomial; and area and
perimeter expressions.
Wrong answers come from real mistakes: subtracting only the first term of the second polynomial, adding
exponents when adding like terms, (x + 3)² = x² + 9, and missing the middle terms when multiplying.
"""
import random
from us_hs import num, B, S, make, lesson, collect, T, expr, MINUS

R = random.Random(91401)


def xp(k, v="x"):
    if k == 0:
        return ""
    if k == 1:
        return "<i>%s</i>" % v
    return "<i>%s</i><sup>%d</sup>" % (v, k)


def P(poly, v="x"):
    """poly: dict degree -> coefficient, printed in standard form."""
    terms = [(poly[k], xp(k, v)) for k in sorted(poly, reverse=True) if poly[k]]
    return expr(terms) if terms else "0"


def add(p, q, s=1):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, 0) + s * c
    return {k: c for k, c in out.items() if c}


def mul(p, q):
    out = {}
    for a, c in p.items():
        for b, d in q.items():
            out[a + b] = out.get(a + b, 0) + c * d
    return {k: c for k, c in out.items() if c}


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


def rpoly(r, deg, lo=-9, hi=9):
    p = {deg: nz(r, -6, 7)}
    for k in range(deg - 1, -1, -1):
        if r.random() < 0.75:
            c = r.randint(lo, hi)
            if c:
                p[k] = c
    return p


def uniq(right, wr):
    out = [w for w in dict.fromkeys(wr) if w != right]
    return out[:3] if len(out) >= 3 else None


# ------------------------------------------------------------ set 1: classify and standard form
NAMES = {1: "linear", 2: "quadratic", 3: "cubic", 4: "quartic"}
TERMS = {1: "monomial", 2: "binomial", 3: "trinomial"}


def one_class(r):
    deg = r.randint(1, 4)
    p = rpoly(r, deg)
    keys = list(p)
    r.shuffle(keys)
    shuffled = expr([(p[k], xp(k)) for k in keys])
    kind = r.choice(["std", "deg", "lead", "name"])
    if kind == "std":
        if keys == sorted(keys, reverse=True) or len(p) < 3:
            return None
        q = "Write %s in standard form." % B(shuffled)
        right = P(p)
        wr = uniq(right, [expr([(p[k], xp(k)) for k in sorted(p)]), P({k: abs(c) for k, c in p.items()}), P({k: -c for k, c in p.items()})])
        e = "Standard form lists the terms from the highest power to the lowest: <b>%s</b>." % right
    elif kind == "deg":
        q = "What is the degree of %s?" % B(shuffled)
        right = num(deg)
        wr = uniq(right, [num(len(p)), num(sum(p.keys())), num(p[deg]), num(deg + 1), num(deg - 1) if deg > 1 else "0"])
        e = "The degree is the highest power of <i>x</i>: <b>%d</b>." % deg
    elif kind == "lead":
        if len(p) < 2 or keys[0] == deg:
            return None
        q = "What is the leading coefficient of %s?" % B(shuffled)
        right = num(p[deg])
        wr = uniq(right, [num(p[keys[0]]), num(deg), num(-p[deg])])
        e = "Write it in standard form, %s. The leading coefficient is the number in front of the highest power: <b>%s</b>." % (P(p), right)
    else:
        if len(p) > 3:
            return None
        q = "Name %s by its degree and number of terms." % B(P(p))
        right = "%s %s" % (NAMES[deg], TERMS[len(p)])
        others = [NAMES[d] for d in NAMES if d != deg]
        wr = uniq(right, ["%s %s" % (others[0], TERMS[len(p)]), "%s %s" % (NAMES[deg], TERMS[len(p) % 3 + 1]), "%s %s" % (NAMES[len(p)] if len(p) in NAMES and len(p) != deg else others[1], TERMS[deg] if deg in TERMS and deg != len(p) else TERMS[(len(p) + 1) % 3 + 1])])
        e = "Degree %d is <b>%s</b>, and %d term%s a <b>%s</b>." % (deg, NAMES[deg], len(p), " makes" if len(p) == 1 else "s make", TERMS[len(p)])
        right = right[0].upper() + right[1:]
        wr = [w[0].upper() + w[1:] for w in wr] if wr else None
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: add and subtract
def one_addsub(r):
    deg = r.randint(1, 3)
    p, q_ = rpoly(r, deg), rpoly(r, r.randint(1, deg))
    sub = r.random() < 0.6
    res = add(p, q_, -1 if sub else 1)
    if not res or len(res) < 2:
        return None
    q = "Simplify %s." % B("(%s) %s (%s)" % (P(p), MINUS if sub else "+", P(q_)))
    right = P(res)
    if sub:
        lead = max(q_)
        only_first = add(p, {lead: q_[lead]}, -1)
        for k, c in q_.items():
            if k != lead:
                only_first = add(only_first, {k: c})
        wr = [P(only_first), P(add(p, q_)), P(add(q_, p, -1))]
    else:
        wr = [P(add(p, q_, -1)), P({k + (1 if k in p and k in q_ else 0): c for k, c in res.items()}), P(add(p, {k: 2 * c for k, c in q_.items()}))]
    wr = uniq(right, wr)
    if not wr:
        return None
    e = ("Change the sign of <b>every</b> term in the second polynomial, then combine like terms: <b>%s</b>." % right) if sub else (
        "Combine like terms (same power of <i>x</i>); the exponents stay the same: <b>%s</b>." % right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: multiply
def one_mul(r):
    if r.random() < 0.35:
        c, k = nz(r, -5, 6), r.randint(1, 3)
        p = rpoly(r, r.randint(1, 2))
        mono = {k: c}
        q = "Multiply %s." % B("%s(%s)" % (P(mono), P(p)))
        right = P(mul(mono, p))
        wr = uniq(right, [P({a: c * b for a, b in p.items()}), P(add(mul(mono, {max(p): p[max(p)]}), {a: b for a, b in p.items() if a != max(p)})), P({a * k if a else k: c * b for a, b in p.items()})])
        e = "Multiply %s by every term, adding the exponents: <b>%s</b>." % (P(mono), right)
    else:
        a, b, c, d = r.choice([1, 1, 2, 3]), nz(r, -9, 9), r.choice([1, 1, 2, 3, 4]), nz(r, -9, 9)
        p1, p2 = {1: a, 0: b}, {1: c, 0: d}
        q = "Multiply %s." % B("(%s)(%s)" % (P(p1), P(p2)))
        right = P(mul(p1, p2))
        wr = uniq(right, [P({2: a * c, 0: b * d}), P({2: a * c, 1: a * d - b * c, 0: b * d}) if a * d - b * c != a * d + b * c else P({2: a * c, 1: a * d + b * c + 1, 0: b * d}),
                          P({2: a * c, 1: a * d + b * c, 0: b + d})])
        e = "Use FOIL: First %s, Outer %s, Inner %s, Last %s. Combine the middle terms: <b>%s</b>." % (
            P({2: a * c}), P({1: a * d}), P({1: b * c}), num(b * d), right)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: special products and longer products
def one_special(r):
    kind = r.choice(["sq+", "sq-", "diff", "tri"])
    a, b = r.choice([1, 1, 2, 3]), r.randint(1, 9)
    if kind in ("sq+", "sq-"):
        s = 1 if kind == "sq+" else -1
        p1 = {1: a, 0: s * b}
        q = "Expand %s." % B("(%s)<sup>2</sup>" % P(p1))
        right = P(mul(p1, p1))
        wr = uniq(right, [P({2: a * a, 0: b * b}), P({2: a * a, 1: s * a * b, 0: b * b}), P({2: a * a, 1: s * 2 * a * b, 0: -b * b}) if s > 0 else P({2: a * a, 1: 2 * a * b, 0: b * b})])
        e = "(<i>a</i> %s <i>b</i>)<sup>2</sup> = <i>a</i><sup>2</sup> %s 2<i>ab</i> + <i>b</i><sup>2</sup>. Don't forget the middle term: <b>%s</b>." % ("+" if s > 0 else MINUS, "+" if s > 0 else MINUS, right)
    elif kind == "diff":
        q = "Multiply %s." % B("(%s)(%s)" % (P({1: a, 0: b}), P({1: a, 0: -b})))
        right = P({2: a * a, 0: -b * b})
        wr = uniq(right, [P({2: a * a, 0: b * b}), P({2: a * a, 1: -2 * a * b, 0: -b * b}), P({2: a * a, 1: 2 * a * b, 0: -b * b})])
        e = "(<i>a</i> + <i>b</i>)(<i>a</i> − <i>b</i>) = <i>a</i><sup>2</sup> − <i>b</i><sup>2</sup>; the middle terms cancel: <b>%s</b>." % right
    else:
        b1 = nz(r, -5, 5)
        t = {2: 1, 1: nz(r, -5, 5), 0: nz(r, -6, 6)}
        p1 = {1: 1, 0: b1}
        q = "Multiply %s." % B("(%s)(%s)" % (P(p1), P(t)))
        full = mul(p1, t)
        right = P(full)
        wr = uniq(right, [P(add(mul({1: 1}, t), {0: b1 * t[0]})), P(add(full, {1: 1})), P(add(full, {2: -2 * b1 if b1 else 1}))])
        e = "Multiply each term of (%s) by every term of the trinomial (6 products), then combine like terms: <b>%s</b>." % (P(p1), right)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: applications
def problems():
    x = "<i>x</i>"
    data = [
        ("A rectangle is (%s + 5) ft long and (%s − 2) ft wide. Which expression gives its area?" % (x, x), "<i>x</i><sup>2</sup> + 3<i>x</i> − 10",
         ["<i>x</i><sup>2</sup> − 10", "2<i>x</i> + 3", "<i>x</i><sup>2</sup> + 7<i>x</i> − 10"], "(<i>x</i> + 5)(<i>x</i> − 2) = <i>x</i><sup>2</sup> − 2<i>x</i> + 5<i>x</i> − 10 = <b><i>x</i><sup>2</sup> + 3<i>x</i> − 10</b>."),
        ("The same rectangle is (%s + 5) ft by (%s − 2) ft. Which expression gives its perimeter?" % (x, x), "4<i>x</i> + 6", ["2<i>x</i> + 3", "<i>x</i><sup>2</sup> + 3<i>x</i> − 10", "4<i>x</i> + 14"], "2(<i>x</i> + 5) + 2(<i>x</i> − 2) = <b>4<i>x</i> + 6</b>."),
        ("A square has side (2%s + 3) cm. Which expression gives its area?" % x, "4<i>x</i><sup>2</sup> + 12<i>x</i> + 9", ["4<i>x</i><sup>2</sup> + 9", "2<i>x</i><sup>2</sup> + 9", "4<i>x</i><sup>2</sup> + 6<i>x</i> + 9"],
         "(2<i>x</i> + 3)<sup>2</sup> = 4<i>x</i><sup>2</sup> + 12<i>x</i> + 9."),
        ("Which is equal to (<i>x</i> + 4)<sup>2</sup>?", "<i>x</i><sup>2</sup> + 8<i>x</i> + 16", ["<i>x</i><sup>2</sup> + 16", "<i>x</i><sup>2</sup> + 4<i>x</i> + 16", "2<i>x</i> + 8"], "(<i>x</i> + 4)(<i>x</i> + 4) has two middle terms of 4<i>x</i>: <b><i>x</i><sup>2</sup> + 8<i>x</i> + 16</b>."),
        ("Liam writes (3<i>x</i><sup>2</sup> + 2<i>x</i>) + (<i>x</i><sup>2</sup> + 5<i>x</i>) = 4<i>x</i><sup>4</sup> + 7<i>x</i><sup>2</sup>. What is the correct answer?", "4<i>x</i><sup>2</sup> + 7<i>x</i>",
         ["4<i>x</i><sup>4</sup> + 7<i>x</i><sup>2</sup>", "11<i>x</i><sup>3</sup>", "3<i>x</i><sup>2</sup> + 7<i>x</i>"], "When you add like terms, the exponents stay the same: <b>4<i>x</i><sup>2</sup> + 7<i>x</i></b>."),
        ("A box has length <i>x</i>, width <i>x</i> + 1 and height <i>x</i> + 2. Which expression gives its volume?", "<i>x</i><sup>3</sup> + 3<i>x</i><sup>2</sup> + 2<i>x</i>",
         ["3<i>x</i> + 3", "<i>x</i><sup>3</sup> + 2", "<i>x</i><sup>3</sup> + 3<i>x</i> + 2"], "<i>x</i>(<i>x</i> + 1)(<i>x</i> + 2) = <i>x</i>(<i>x</i><sup>2</sup> + 3<i>x</i> + 2) = <b><i>x</i><sup>3</sup> + 3<i>x</i><sup>2</sup> + 2<i>x</i></b>."),
        ("Is the sum of two polynomials always a polynomial?", "Yes, polynomials are closed under addition", ["No, the degree can change", "Only if they have the same degree", "No, never"],
         "Adding like terms always gives another polynomial: <b>yes</b>. The same is true for subtraction and multiplication."),
        ("What is the degree of (<i>x</i><sup>3</sup> + 1)(<i>x</i><sup>2</sup> − 4)?", "5", ["6", "3", "2"], "The highest-power terms multiply: <i>x</i><sup>3</sup> · <i>x</i><sup>2</sup> = <i>x</i><sup>5</sup>, so the degree is <b>5</b>."),
        ("A company's revenue is 5<i>x</i><sup>2</sup> + 40<i>x</i> and its costs are 2<i>x</i><sup>2</sup> + 10<i>x</i> + 300. Which expression gives the profit?", "3<i>x</i><sup>2</sup> + 30<i>x</i> − 300",
         ["3<i>x</i><sup>2</sup> + 30<i>x</i> + 300", "7<i>x</i><sup>2</sup> + 50<i>x</i> + 300", "3<i>x</i><sup>2</sup> + 50<i>x</i> − 300"], "Profit = revenue − costs. Subtract every term: <b>3<i>x</i><sup>2</sup> + 30<i>x</i> − 300</b>."),
        ("Which expression is equivalent to 98 × 102 using a special product?", "(100 − 2)(100 + 2) = 10,000 − 4", ["(100 − 2)<sup>2</sup>", "100<sup>2</sup> + 4", "98<sup>2</sup> + 2 × 98"],
         "Difference of squares: 100<sup>2</sup> − 2<sup>2</sup> = 9,996."),
        ("Which product has no <i>x</i>-term?", "(<i>x</i> + 7)(<i>x</i> − 7)", ["(<i>x</i> + 7)(<i>x</i> + 7)", "(<i>x</i> − 7)(<i>x</i> − 7)", "(<i>x</i> + 7)(<i>x</i> − 1)"], "The middle terms +7<i>x</i> and −7<i>x</i> cancel: <b>(<i>x</i> + 7)(<i>x</i> − 7)</b> = <i>x</i><sup>2</sup> − 49."),
        ("Simplify 2<i>x</i>(<i>x</i> − 3) − <i>x</i>(<i>x</i> + 4).", "<i>x</i><sup>2</sup> − 10<i>x</i>", ["<i>x</i><sup>2</sup> − 2<i>x</i>", "3<i>x</i><sup>2</sup> − 10<i>x</i>", "<i>x</i><sup>2</sup> + 10<i>x</i>"],
         "2<i>x</i><sup>2</sup> − 6<i>x</i> − <i>x</i><sup>2</sup> − 4<i>x</i> = <b><i>x</i><sup>2</sup> − 10<i>x</i></b>."),
        ("A picture is 8 in. by 10 in. A frame of width <i>x</i> in. goes around it. Which expression gives the total area?", "4<i>x</i><sup>2</sup> + 36<i>x</i> + 80",
         ["<i>x</i><sup>2</sup> + 18<i>x</i> + 80", "4<i>x</i><sup>2</sup> + 80", "2<i>x</i><sup>2</sup> + 36<i>x</i> + 80"], "(8 + 2<i>x</i>)(10 + 2<i>x</i>) = 80 + 16<i>x</i> + 20<i>x</i> + 4<i>x</i><sup>2</sup> = <b>4<i>x</i><sup>2</sup> + 36<i>x</i> + 80</b>."),
        ("Which expression is a polynomial?", "3<i>x</i><sup>2</sup> − <i>x</i> + 5", ["2/<i>x</i> + 1", "√<i>x</i> + 4", "<i>x</i><sup>−2</sup> + 3"], "Polynomials only have whole-number powers of <i>x</i>: <b>3<i>x</i><sup>2</sup> − <i>x</i> + 5</b>."),
        ("What is the constant term of (2<i>x</i> − 3)(<i>x</i> + 5)?", "−15", ["2", "7", "15"], "The constant term is Last × Last: −3 × 5 = <b>−15</b>."),
        ("What is the coefficient of <i>x</i> in (2<i>x</i> − 3)(<i>x</i> + 5)?", "7", ["−15", "10", "−3"], "Outer + Inner: 10<i>x</i> − 3<i>x</i> = <b>7<i>x</i></b>."),
        ("Find the missing number: (<i>x</i> + ☐)<sup>2</sup> = <i>x</i><sup>2</sup> + 12<i>x</i> + 36.", "6", ["12", "36", "3"], "The middle term is 2 × ☐ × <i>x</i> = 12<i>x</i>, so ☐ = <b>6</b>."),
        ("Subtract 4<i>x</i><sup>2</sup> − 3<i>x</i> + 1 from 7<i>x</i><sup>2</sup> + <i>x</i> − 5.", "3<i>x</i><sup>2</sup> + 4<i>x</i> − 6", ["−3<i>x</i><sup>2</sup> − 4<i>x</i> + 6", "3<i>x</i><sup>2</sup> − 2<i>x</i> − 4", "11<i>x</i><sup>2</sup> − 2<i>x</i> − 4"],
         "“Subtract A from B” means B − A: (7<i>x</i><sup>2</sup> + <i>x</i> − 5) − (4<i>x</i><sup>2</sup> − 3<i>x</i> + 1) = <b>3<i>x</i><sup>2</sup> + 4<i>x</i> − 6</b>."),
        ("A garden is <i>x</i> m by <i>x</i> m. The length is increased by 3 m and the width by 2 m. By how much does the area increase?", "5<i>x</i> + 6 m²", ["5 m²", "6 m²", "<i>x</i><sup>2</sup> + 5<i>x</i> + 6 m²"],
         "New area (<i>x</i> + 3)(<i>x</i> + 2) = <i>x</i><sup>2</sup> + 5<i>x</i> + 6. The increase is <b>5<i>x</i> + 6 m²</b>."),
        ("Expand (<i>x</i> − 1)<sup>3</sup>.", "<i>x</i><sup>3</sup> − 3<i>x</i><sup>2</sup> + 3<i>x</i> − 1", ["<i>x</i><sup>3</sup> − 1", "<i>x</i><sup>3</sup> + 3<i>x</i><sup>2</sup> − 3<i>x</i> − 1", "<i>x</i><sup>3</sup> − 3<i>x</i> − 1"],
         "(<i>x</i> − 1)<sup>2</sup> = <i>x</i><sup>2</sup> − 2<i>x</i> + 1; multiply by (<i>x</i> − 1): <b><i>x</i><sup>3</sup> − 3<i>x</i><sup>2</sup> + 3<i>x</i> − 1</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>polynomial</b> is a sum of terms like 3<i>x</i><sup>2</sup>, −5<i>x</i> and 7. Write it in <b>standard form</b> (highest power first). "
        "The <b>degree</b> is the highest power, and the <b>leading coefficient</b> is the number in front of it.</p>"
        "<p><b>Add or subtract</b> by combining like terms (the same power). When subtracting, change the sign of <b>every</b> term in the second polynomial. "
        "<b>Multiply</b> by multiplying every term by every term (FOIL for two binomials), adding exponents.</p>"
        "<p>Special products: (<i>a</i> + <i>b</i>)<sup>2</sup> = <i>a</i><sup>2</sup> + 2<i>ab</i> + <i>b</i><sup>2</sup>, "
        "(<i>a</i> − <i>b</i>)<sup>2</sup> = <i>a</i><sup>2</sup> − 2<i>ab</i> + <i>b</i><sup>2</sup>, (<i>a</i> + <i>b</i>)(<i>a</i> − <i>b</i>) = <i>a</i><sup>2</sup> − <i>b</i><sup>2</sup>.</p>",
        [("Simplify (4<i>x</i><sup>2</sup> − 3<i>x</i> + 2) − (<i>x</i><sup>2</sup> + 5<i>x</i> − 6).", ["4<i>x</i><sup>2</sup> − 3<i>x</i> + 2 − <i>x</i><sup>2</sup> − 5<i>x</i> + 6."], "3<i>x</i><sup>2</sup> − 8<i>x</i> + 8"),
         ("Multiply (2<i>x</i> + 3)(<i>x</i> − 4).", ["F: 2<i>x</i><sup>2</sup>. O: −8<i>x</i>. I: 3<i>x</i>. L: −12."], "2<i>x</i><sup>2</sup> − 5<i>x</i> − 12")],
        ["Subtracting only the first term: −(<i>x</i><sup>2</sup> + 5<i>x</i> − 6) is −<i>x</i><sup>2</sup> − 5<i>x</i> + 6.",
         "Adding exponents when adding like terms: 3<i>x</i><sup>2</sup> + <i>x</i><sup>2</sup> = 4<i>x</i><sup>2</sup>, not 4<i>x</i><sup>4</sup>.",
         "Squaring a binomial without the middle term: (<i>x</i> + 3)<sup>2</sup> = <i>x</i><sup>2</sup> + 6<i>x</i> + 9, not <i>x</i><sup>2</sup> + 9.",
         "Missing a product when multiplying: two binomials give four products before you combine."])


def main():
    sets = [S("Degree, leading coefficient and standard form", collect(one_class, 20, R)),
            S("Add and subtract polynomials", collect(one_addsub, 20, R)),
            S("Multiply polynomials", collect(one_mul, 20, R)),
            S("Special products", collect(one_special, 20, R)),
            S("Polynomial applications", problems())]
    make("polynomial-operations", 14, "A-APR.A.1",
         "Adding, Subtracting and Multiplying Polynomials",
         "Algebra 1 Polynomials Worksheets: Adding, Subtracting, Multiplying and FOIL (Free, Answer Key)",
         "Polynomial operations",
         "Understand that polynomials form a system analogous to the integers, namely, they are closed under the operations of addition, "
         "subtraction, and multiplication; add, subtract, and multiply polynomials.",
         "Free Algebra 1 polynomial worksheets (A-APR.A.1): degree and standard form, adding and subtracting polynomials, multiplying with "
         "FOIL, special products and area expressions. 100 questions with an answer key.",
         "Combine like terms to add. Change every sign to subtract. Multiply every term by every term.",
         "(a + b)² = a² + 2ab + b²; (a + b)(a − b) = a² − b².",
         body(),
         [("How do you subtract polynomials?", "Change the sign of every term in the polynomial being subtracted, then combine like terms."),
          ("What is FOIL?", "A way to multiply two binomials: First, Outer, Inner, Last. Then combine the like terms in the middle."),
          ("What is the degree of a polynomial?", "The highest power of the variable. 4x³ − x + 2 has degree 3."),
          ("Why is (x + 3)² not x² + 9?", "(x + 3)² means (x + 3)(x + 3), which has two middle terms of 3x: x² + 6x + 9.")],
         sets, R, domain="Polynomials & Factoring")


if __name__ == "__main__":
    main()
