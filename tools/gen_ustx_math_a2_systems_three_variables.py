# -*- coding: utf-8 -*-
"""
Texas Algebra II: Systems of Three Linear Equations in Three Variables (TEKS 2A.3A, 2A.3B)
  python3 tools/gen_ustx_math_a2_systems_three_variables.py
Checking an ordered triple, eliminating a variable, back-substitution (Gaussian elimination), solving systems of three
equations, and writing and solving systems from word problems (own makers).
Wrong answers come from real mistakes: subtracting instead of adding, a sign error in the constant, and swapping x and y.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "algebra-2"

import us_hs
adopt(us_hs)


def W(fn, keep=None):
    """Use an item maker of another generator: its odd failures count as a skipped try, and a question text
    is used only once (not again with other wrong answers)."""
    seen = set()

    def f(r):
        try:
            it = fn(r)
        except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            raise AssertionError("skip")
        if not it or (keep and not keep(it)) or it["q"] in seen:
            raise AssertionError("skip")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def PR(fn, keep=None):
    """A fixed word-problem list of another generator as a set maker: a shuffled share of it."""
    def f(r):
        its = [it for it in fn() if keep is None or keep(it)]
        r.shuffle(its)
        return {"title": fn.__name__, "items": its * 3}
    f.__name__ = fn.__name__
    return f


MINUS = "−"
X = "<i>x</i>"


def sg(v):
    return ("−%s" % abs(v)) if v < 0 else str(v)


def poly(cs, v="<i>x</i>"):
    """[a, b, c] highest power first, e.g. 2x² − 3x + 1."""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        if p == 0:
            body = str(mag)
        else:
            body = ("" if mag == 1 else str(mag)) + v + ("<sup>%d</sup>" % p if p > 1 else "")
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"
def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


from fractions import Fraction as Fr


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)


VARS = ["<i>x</i>", "<i>y</i>", "<i>z</i>"]


def term_list(cs, vs=VARS):
    out = ""
    for c, v in zip(cs, vs):
        if c == 0:
            continue
        body = ("" if abs(c) == 1 else str(abs(c))) + v
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"


def eqn(cs, d):
    return "%s = %s" % (term_list(cs), sg(d))


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def system(r, sol, low=-3, high=3):
    for _ in range(200):
        m = [[r.randint(low, high) for _ in range(3)] for _ in range(3)]
        if any(all(c == 0 for c in row) for row in m) or any(sum(1 for c in row if c) < 2 for row in m):
            continue
        if det3(m) == 0:
            continue
        return m, [sum(c * s for c, s in zip(row, sol)) for row in m]
    raise AssertionError


def show(m, d):
    return "<br>".join("(%d) %s" % (i + 1, eqn(row, v)) for i, (row, v) in enumerate(zip(m, d)))


def trip(t):
    return "(%s, %s, %s)" % tuple(sg(v) for v in t)


def rsol(r):
    return [r.randint(-5, 6) for _ in range(3)]


def one_check(r):
    sol = rsol(r)
    m, d = system(r, sol)
    t = list(sol)
    if r.random() < 0.65:
        i = r.randrange(3)
        t[i] += r.choice([-2, -1, 1, 2])
    fails = [i + 1 for i, (row, v) in enumerate(zip(m, d)) if sum(c * s for c, s in zip(row, t)) != v]
    def lab(fs):
        if not fs:
            return "Yes, it makes all three equations true"
        if len(fs) == 1:
            return "No, it does not work in equation (%d)" % fs[0]
        if len(fs) == 3:
            return "No, it does not work in any of the equations"
        return "No, it does not work in equations " + " and ".join("(%d)" % f for f in fs)
    right = lab(fails)
    opts = [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    r.shuffle(opts)
    w = [lab(o) for o in opts if o != fails]
    if fails:
        w = [lab([])] + w
    calc = "; ".join("(%d) %s" % (i + 1, "✓" if (i + 1) not in fails else "✗") for i in range(3))
    return mcq("Is %s a solution of the system?<br>%s" % (trip(t), show(m, d)), right, w, "Substitute into each equation: %s. <b>%s</b>." % (calc, right))


def one_elim(r):
    sol = rsol(r)
    for _ in range(100):
        c = r.choice([1, 2, 3, -1, -2])
        a1, b1, a2, b2 = [r.randint(-4, 4) for _ in range(4)]
        if (a1 + a2) == 0 or (b1 + b2) == 0 or a1 * b2 - a2 * b1 == 0:
            continue
        e1, e2 = [a1, b1, c], [a2, b2, -c]
        if sum(1 for v in e1 if v) < 3 or sum(1 for v in e2 if v) < 3:
            continue
        break
    else:
        raise AssertionError
    d1 = sum(p * s for p, s in zip(e1, sol))
    d2 = sum(p * s for p, s in zip(e2, sol))
    right = eqn([a1 + a2, b1 + b2], d1 + d2).replace("<i>z</i>", "")
    right = "%s = %s" % (term_list([a1 + a2, b1 + b2]), sg(d1 + d2))
    w = ["%s = %s" % (term_list([a1 - a2, b1 - b2]), sg(d1 - d2)), "%s = %s" % (term_list([a1 + a2, b1 + b2]), sg(d1 - d2)), "%s = %s" % (term_list([a1 + a2, b1 - b2]), sg(d1 + d2)),
         "%s = %s" % (term_list([a1 + a2, b1 + b2]), sg(-(d1 + d2)))]
    w = [v for v in w if v != right]
    return mcq("Add equations (1) and (2) to eliminate <i>z</i>. Which equation do you get?<br>(1) %s<br>(2) %s" % (eqn(e1, d1), eqn(e2, d2)), right, w,
               "The <i>z</i>-terms %s<i>z</i> and %s<i>z</i> cancel. Add the <i>x</i>-terms, the <i>y</i>-terms and the constants: <b>%s</b>." % (sg(c) if abs(c) > 1 else ("" if c == 1 else MINUS), sg(-c) if abs(c) > 1 else ("" if -c == 1 else MINUS), right))


def one_back(r):
    x, y, z = rsol(r)
    a, b = r.choice([n for n in range(-4, 5) if n]), r.choice([n for n in range(-4, 5) if n])
    c = r.choice([n for n in range(-4, 5) if n])
    e1 = eqn([1, a, b], x + a * y + b * z)
    e2 = eqn([0, 1, c], y + c * z)
    e3 = "<i>z</i> = %s" % sg(z)
    want = r.choice(["x", "y"])
    if want == "y":
        right = sg(y)
        w = [sg(y + 2 * c * z), sg(c * z), sg(-y), sg(y + c)]
        e = "<i>y</i> + (%s)(%s) = %s, so <i>y</i> = %s." % (sg(c), sg(z), sg(y + c * z), sg(y))
    else:
        right = sg(x)
        w = [sg(x + 2 * a * y), sg(x + 2 * b * z), sg(-x), sg(y), sg(x + 1)]
        e = "From (3), <i>z</i> = %s. From (2), <i>y</i> = %s − (%s)(%s) = %s. Then (1): <i>x</i> = %s − (%s)(%s) − (%s)(%s) = %s." % (
            sg(z), sg(y + c * z), sg(c), sg(z), sg(y), sg(x + a * y + b * z), sg(a), sg(y), sg(b), sg(z), sg(x))
    w = [v for v in w if v != right]
    return mcq("Gaussian elimination gave this system. Use back-substitution to find <i>%s</i>.<br>(1) %s<br>(2) %s<br>(3) %s" % (want, e1, e2, e3), right, w, e + " <b>%s</b>." % right)


def one_solve(r):
    sol = rsol(r)
    m, d = system(r, sol, -2, 3)
    x, y, z = sol
    cands = [(y, x, z), (x, y, -z), (-x, y, z), (x, z, y), (x + 1, y, z - 1), (z, y, x)]
    w = []
    for c in cands:
        if list(c) != sol and all(sum(p * s for p, s in zip(row, c)) == v for row, v in zip(m, d)) is False:
            w.append(trip(c))
    w = [v for v in dict.fromkeys(w) if v != trip(sol)]
    return mcq("Solve the system.<br>%s" % show(m, d), trip(sol), w,
               "Eliminate one variable from two pairs of equations, solve the 2 × 2 system, then substitute back. Check in all three equations: <b>%s</b>." % trip(sol))


def one_word(r):
    kind = r.choice(["tickets", "shots", "fruit", "numbers", "angles", "coins"])
    if kind == "tickets":
        c = r.randint(10, 60)
        a = 2 * c
        s = c + r.randint(5, 40)
        pa, ps, pc = r.choice([(12, 8, 5), (15, 10, 6), (10, 7, 4), (14, 9, 6), (18, 12, 8)])
        n, tot = a + s + c, a * pa + s * ps + c * pc
        ask = r.choice([("student tickets", s), ("adult tickets", a), ("child tickets", c)])
        q = "A school play sold %d tickets for $%d. Adult tickets cost $%d, student tickets $%d and child tickets $%d. They sold twice as many adult tickets as child tickets. How many %s did they sell?" % (n, comma(tot) if False else tot, pa, ps, pc, ask[0])
        q = q.replace("for $%d." % tot, "for $%s." % comma(tot))
        vals = [a, s, c]
        e = "<i>a</i> + <i>s</i> + <i>c</i> = %d, %d<i>a</i> + %d<i>s</i> + %d<i>c</i> = %s, <i>a</i> = 2<i>c</i>. Solving gives <i>a</i> = %d, <i>s</i> = %d, <i>c</i> = %d." % (n, pa, ps, pc, comma(tot), a, s, c)
    elif kind == "shots":
        f, two, three = r.randint(3, 12), r.randint(6, 20), r.randint(2, 10)
        two = three + r.randint(1, 10)
        n, pts = f + two + three, f + 2 * two + 3 * three
        k = two - three
        ask = r.choice([("3-point shots", three), ("2-point shots", two), ("free throws", f)])
        q = "A basketball team made %d baskets for %d points: free throws (1 point), 2-point shots and 3-point shots. They made %d more 2-point shots than 3-point shots. How many %s did they make?" % (n, pts, k, ask[0])
        vals = [f, two, three]
        e = "<i>f</i> + <i>t</i> + <i>h</i> = %d, <i>f</i> + 2<i>t</i> + 3<i>h</i> = %d, <i>t</i> = <i>h</i> + %d. Solving gives <i>f</i> = %d, <i>t</i> = %d, <i>h</i> = %d." % (n, pts, k, f, two, three)
    elif kind == "fruit":
        p = [r.randint(1, 4), r.randint(1, 6), r.randint(2, 7)]
        items = r.choice([(("apple", "apples"), ("banana", "bananas"), ("mango", "mangoes")), (("taco", "tacos"), ("drink", "drinks"), ("salad", "salads")),
                          (("pen", "pens"), ("notebook", "notebooks"), ("folder", "folders")), (("muffin", "muffins"), ("bagel", "bagels"), ("juice", "juices"))])
        rows = [[r.randint(1, 4) for _ in range(3)] for _ in range(3)]
        if det3(rows) == 0:
            raise AssertionError
        tots = [sum(c * v for c, v in zip(row, p)) for row in rows]
        who = r.sample(["Ana", "Luis", "Kim", "Omar", "Jada", "Ben"], 3)
        lines = ["%s buys %d %s, %d %s and %d %s for $%d." % (w_, row[0], items[0][row[0] > 1], row[1], items[1][row[1] > 1], row[2], items[2][row[2] > 1], t) for w_, row, t in zip(who, rows, tots)]
        j = r.randrange(3)
        ask = ("", p[j])
        q = " ".join(lines) + " How many dollars does one %s cost?" % items[j][0]
        vals = p
        e = "Write one equation for each person and solve the 3 × 3 system: the prices are $%d, $%d and $%d." % tuple(p)
    elif kind == "numbers":
        b = r.randint(2, 20)
        a = 2 * b
        c = r.randint(1, 30) + a
        k = c - a
        n = a + b + c
        ask = r.choice([("first number", a), ("second number", b), ("third number", c)])
        q = "The sum of three numbers is %d. The first number is twice the second. The third number is %d more than the first. What is the %s?" % (n, k, ask[0])
        vals = [a, b, c]
        e = "<i>a</i> + <i>b</i> + <i>c</i> = %d, <i>a</i> = 2<i>b</i>, <i>c</i> = <i>a</i> + %d. Then 2<i>b</i> + <i>b</i> + 2<i>b</i> + %d = %d, so <i>b</i> = %d, <i>a</i> = %d, <i>c</i> = %d." % (n, k, k, n, b, a, c)
    elif kind == "angles":
        B = r.randint(20, 50)
        A = B + r.randint(5, 30)
        C = 180 - A - B
        if C <= 10:
            raise AssertionError
        k = A - B
        ask = r.choice([("angle A", A), ("angle B", B), ("angle C", C)])
        q = "The angles of a triangle add to 180°. Angle A is %d° more than angle B, and angle C is %d° more than angle B. What is the measure of %s, in degrees?" % (k, C - B, ask[0]) if C > B else None
        if q is None:
            raise AssertionError
        vals = [A, B, C]
        e = "<i>A</i> + <i>B</i> + <i>C</i> = 180, <i>A</i> = <i>B</i> + %d, <i>C</i> = <i>B</i> + %d. So 3<i>B</i> + %d = 180 and <i>B</i> = %d, <i>A</i> = %d, <i>C</i> = %d." % (k, C - B, k + C - B, B, A, C)
    else:
        nk, d, qt = r.randint(4, 20), r.randint(4, 20), r.randint(2, 15)
        nk = qt + r.randint(1, 8)
        n, cents = nk + d + qt, 5 * nk + 10 * d + 25 * qt
        ask = r.choice([("dimes", d), ("quarters", qt), ("nickels", nk)])
        q = "A jar has %d coins worth $%s: nickels, dimes and quarters. There are %d more nickels than quarters. How many %s are in the jar?" % (n, "%d.%02d" % (cents // 100, cents % 100), nk - qt, ask[0])
        vals = [nk, d, qt]
        e = "<i>n</i> + <i>d</i> + <i>q</i> = %d, 5<i>n</i> + 10<i>d</i> + 25<i>q</i> = %d, <i>n</i> = <i>q</i> + %d. Solving gives <i>n</i> = %d, <i>d</i> = %d, <i>q</i> = %d." % (n, cents, nk - qt, nk, d, qt)
    right = ask[1]
    w = [v for v in vals if v != right] + [right + 2, right - 1, right + 5, 2 * right]
    return mcq(q, right, w, e + " <b>%s</b>." % comma(right))


def build():
    sets, R = build_sets([
        ("Is it a solution?", [("collect", uniq(one_check), 20)]),
        ("Eliminate a variable", [("collect", uniq(one_elim), 20)]),
        ("Back-substitution", [("collect", uniq(one_back), 20)]),
        ("Solve the system", [("collect", uniq(one_solve), 20)]),
        ("Systems of three equations word problems", [("collect", uniq(one_word), 20)]),
    ], 69704)
    finish(sets, R)
    body = lesson('<ul><li>A solution of a system of three equations in <i>x</i>, <i>y</i> and <i>z</i> is an <b>ordered triple</b> (<i>x</i>, <i>y</i>, <i>z</i>) that makes all three equations true.</li><li>Use two pairs of equations to eliminate the same variable. You get a system of two equations in two variables.</li><li>Solve it, then substitute back to find the third variable.</li><li>Gaussian elimination puts the system in a stair shape; then solve from the bottom up (back-substitution).</li></ul>',
        [example("<i>x</i> + <i>y</i> + <i>z</i> = 6, <i>y</i> + 2<i>z</i> = 8, <i>z</i> = 3", ["<i>y</i> = 8 − 6 = 2", "<i>x</i> = 6 − 2 − 3 = 1"], "(1, 2, 3)")],
        [['Subtracting when the terms are opposites', 'Add 2<i>z</i> and −2<i>z</i> to eliminate <i>z</i>.'], ['Checking only one equation', 'A solution must work in all three.'], ['Mixing up the order', 'Write the triple as (<i>x</i>, <i>y</i>, <i>z</i>).']])
    faq = [('What does TEKS 2A.3A ask?', 'Formulate systems of equations, including systems consisting of three linear equations in three variables and systems consisting of two equations, the first linear and the second quadratic.'), ('What does TEKS 2A.3B ask?', 'Solve systems of three linear equations in three variables by using Gaussian elimination, technology with matrices, and substitution.'), ('What does a system of three equations look like as a graph?', 'Three planes. A single solution is the one point where all three meet.'), ('Can a system have no solution?', 'Yes, when the planes have no common point.')]
    make('systems-of-three-equations', 4, 'Systems of Equations and Inequalities', '2A.3A, 2A.3B',
         '2A.3A formulate systems of equations, including systems consisting of three linear equations in three variables and systems consisting of two equations, the first linear and the second quadratic; 2A.3B solve systems of three linear equations in three variables by using Gaussian elimination, technology with matrices, and substitution',
         'Systems of Three Linear Equations in Three Variables', 'Systems of Three Equations',
         'Free Algebra II worksheets on systems of three linear equations for Texas TEKS 2A.3A and 2A.3B: check ordered triples, elimination, back-substitution, solving and word problems. 100 questions with answers.',
         'Eliminate one variable twice, solve the 2 × 2 system, then substitute back.', 'The solution is an ordered triple (x, y, z).',
         body, faq, sets, seo_title='Algebra II Systems of Three Equations Worksheets (TEKS 2A.3A, 2A.3B)')


if __name__ == "__main__":
    build()
