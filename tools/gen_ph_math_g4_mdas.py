# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): The MDAS Rules: Order of Operations (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_mdas.py
Evaluating expressions with the MDAS rules (multiplication and division first, from left to right, then addition and
subtraction), finding mistakes, comparing expressions, missing numbers and matching expressions to situations (own
makers).
Wrong answers come from real mistakes: working from left to right only, adding before multiplying, and doing
multiplication before a division that comes first.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)

ph_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import operator
OPS = {"+": operator.add, "−": operator.sub, "×": operator.mul, "÷": operator.floordiv}


def mdas(tokens):
    t = list(tokens)
    i = 1
    while i < len(t):
        if t[i] in ("×", "÷"):
            a, b = t[i - 1], t[i + 1]
            if t[i] == "÷" and a % b:
                raise AssertionError
            t[i - 1:i + 2] = [OPS[t[i]](a, b)]
        else:
            i += 2
    v = t[0]
    for j in range(1, len(t), 2):
        v = OPS[t[j]](v, t[j + 1])
    return v


def l2r(tokens):
    v = tokens[0]
    for j in range(1, len(tokens), 2):
        if tokens[j] == "÷" and v % tokens[j + 1]:
            return None
        v = OPS[tokens[j]](v, tokens[j + 1])
    return v


def add_first(tokens):
    t = list(tokens)
    i = 1
    while i < len(t):
        if t[i] in ("+", "−"):
            t[i - 1:i + 2] = [OPS[t[i]](t[i - 1], t[i + 1])]
        else:
            i += 2
    try:
        return mdas(t)
    except (AssertionError, ZeroDivisionError):
        return None


def term(r, kind):
    if kind == "n":
        return [r.randint(2, 40)]
    if kind == "m":
        return [r.randint(2, 12), "×", r.randint(2, 9)]
    if kind == "d":
        d = r.randint(2, 9)
        return [d * r.randint(2, 9), "÷", d]
    if kind == "md":
        a, b, d = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6)
        if r.random() < 0.5:
            return [d * a, "÷", d, "×", b]
        return [a * d, "×", b, "÷", d] if (a * d * b) % d == 0 else [a, "×", b]


def rand_expr(r, n):
    for _ in range(200):
        if n == 2:
            kinds = r.choice([("n", "m"), ("m", "n"), ("n", "d"), ("d", "n"), ("m", "d"), ("n", "md"), ("md", "n")])
        else:
            kinds = r.choice([("n", "m", "n"), ("n", "d", "m"), ("m", "n", "d"), ("n", "n", "m"), ("d", "m", "n"), ("n", "md", "n")])
        t = []
        for i, kd in enumerate(kinds):
            if i:
                t.append(r.choice(["+", "−"]))
            t += term(r, kd)
        if len(t) // 2 > 4:
            continue
        v = mdas(t)
        if v < 0 or l2r(t) == v:
            continue
        return t, v
    raise AssertionError


def show(t):
    return " ".join(str(x) if isinstance(x, int) else x for x in t)


def one_eval(r):
    t, v = rand_expr(r, r.choice([2, 2, 3]))
    w = [l2r(t), add_first(t), v + 2]
    w = [x for x in w if x is not None and x >= 0 and x != v]
    return mcq("Use the MDAS rules. What is %s?" % show(t), v, w + [v + 10, v - 1 if v > 1 else v + 3],
               "Multiply and divide first, from left to right; then add and subtract from left to right. <b>%s = %s</b>." % (show(t), comma(v)))


def one_err(r):
    k = Kid(r).next()
    t, v = rand_expr(r, 2)
    bad = l2r(t)
    if bad is None or bad == v or bad < 0:
        raise AssertionError
    q = "%s says %s = %s. What did %s do wrong, and what is the correct value?" % (k["n"], show(t), comma(bad), k["he"])
    right = "%s worked from left to right; it is %s" % (k["He"], comma(v))
    w = ["%s is correct" % k["He"], "%s worked from left to right; it is %s" % (k["He"], comma(v + 1)), "%s added first; it is %s" % (k["He"], comma(bad + 2))]
    return mcq(q, right, w, "MDAS: do × and ÷ before + and −. %s = <b>%s</b>." % (show(t), comma(v)))


def one_cmp(r):
    t1, v1 = rand_expr(r, 2)
    t2, v2 = rand_expr(r, 2)
    if v1 == v2:
        raise AssertionError
    pairs = [(show(t1), v1), (show(t2), v2)]
    big = max(pairs, key=lambda p: p[1])
    t3, v3 = rand_expr(r, 2)
    t4, v4 = rand_expr(r, 2)
    allp = [(show(t1), v1), (show(t2), v2), (show(t3), v3), (show(t4), v4)]
    if len({p[1] for p in allp}) < 4:
        raise AssertionError
    most = r.random() < 0.6
    best = (max if most else min)(allp, key=lambda p: p[1])
    return mcq("Use MDAS. Which has the %s value? %s" % ("greatest" if most else "least", " &nbsp;|&nbsp; ".join(p[0] for p in allp)), best[0], [p[0] for p in allp if p != best],
               "Values: " + "; ".join("%s = %s" % (p[0], comma(p[1])) for p in allp) + ". <b>%s</b>." % best[0])


def one_fill(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(5, 50)
    kind = r.choice(["mul", "add"])
    if kind == "mul":
        q = "%d + ☐ × %d = %d. What number goes in the box?" % (c, b, c + a * b)
        right, w = a, [(c + a * b) // b - c if (c + a * b) % b == 0 and (c + a * b) // b - c > 0 else a + 2, a * b, c + a]
        e = "%d + ☐ × %d = %d, so ☐ × %d = %d and ☐ = %d." % (c, b, c + a * b, b, a * b, a)
    else:
        q = "%d × %d − ☐ = %d. What number goes in the box?" % (a, b, a * b - (c % (a * b - 1)) - 1 if a * b > 2 else 1)
        x = (c % (a * b - 1)) + 1 if a * b > 2 else 1
        q = "%d × %d − ☐ = %d. What number goes in the box?" % (a, b, a * b - x)
        right, w = x, [a * b + x, a * b - x, x + a]
        e = "%d × %d = %d, and %d − ☐ = %d, so ☐ = %d." % (a, b, a * b, a * b, a * b - x, x)
    return mcq(q, right, w, e.replace("☐ = %d." % right, "☐ = <b>%d</b>." % right))


def one_word(r):
    k = Kid(r).next()
    a, b, c = r.randint(3, 9), r.randint(5, 60), r.randint(2, 9)
    p = r.choice([10, 12, 15, 20, 25, 35])
    q = "%s buys %d notebooks at %s each and a bag for %s. Which expression gives the total cost?" % (k["n"], a, peso(p), peso(b * 5))
    right = "%d × %d + %d" % (a, p, b * 5)
    w = ["(%d + %d) × %d" % (a, b * 5, p), "%d + %d × %d" % (a, p, b * 5), "%d × %d × %d" % (a, p, b * 5)]
    return mcq(q, right, w, "By MDAS, %d × %d + %d means (%d × %d) + %d = %s. <b>%s</b>." % (a, p, b * 5, a, p, b * 5, peso(a * p + b * 5), right))


def build():
    sets, R = build_sets([
        ("Evaluate with MDAS", [("collect", uniq(one_eval), 20)]),
        ("Find the mistake", [("collect", uniq(one_err), 20)]),
        ("Missing numbers", [("collect", uniq(one_fill), 20)]),
        ("Greatest and least", [("collect", uniq(one_cmp), 20)]),
        ("Expressions for situations", [("collect", uniq(one_word), 20)]),
    ], 70410)
    finish(sets, R)
    body = lesson('<ul><li><b>MDAS</b>: Multiplication and Division first, then Addition and Subtraction.</li><li>Do × and ÷ in order from <b>left to right</b>. Then do + and − from left to right.</li><li>Example: 18 + 6 × 2 = 18 + 12 = 30, not 24 × 2.</li><li>Check by writing the value of each step under the expression.</li></ul>',
        [example("40 − 12 ÷ 4 × 3", ["12 ÷ 4 = 3", "3 × 3 = 9", "40 − 9"], "31")],
        [['Left to right only', '× and ÷ come before + and −.'], ['Adding first', '18 + 6 × 2 is 30.'], ['× before an earlier ÷', '× and ÷ are done in order from the left.']])
    faq = [('What does MATATAG Math 4 ask about MDAS?', 'Perform two or more different operations by applying the MDAS rules.'), ('What does MDAS stand for?', 'Multiplication, Division, Addition, Subtraction.'), ('Is multiplication always before division?', 'No. Multiplication and division are done together, from left to right.'), ('Why do we need MDAS?', 'So everyone gets the same answer for the same expression.')]
    make('order-of-operations-mdas', 10, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Perform two or more different operations by applying the MDAS rules.',
         'The MDAS Rules: Order of Operations', 'MDAS Rules',
         'Free Grade 4 MDAS worksheets for the DepEd MATATAG curriculum: order of operations with multiplication, division, addition and subtraction, mistakes and expressions for situations. 100 questions with answers.',
         'Multiply and divide first, then add and subtract.', 'Same level: left to right.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
