# -*- coding: utf-8 -*-
"""
US Precalculus: Conic Sections (Common Core G-GPE.A.2, G-GPE.A.3)
  python3 tools/gen_us_math_pc_conic_sections.py
Parabolas from focus and directrix, ellipses and hyperbolas (center, vertices, foci, asymptotes),
identifying a conic from its equation, and applications such as satellite dishes and whispering galleries.
Wrong answers come from real mistakes: using c² = a² + b² for an ellipse (or a² − b² for a hyperbola),
forgetting that 4p is not p, mixing up the major axis direction, and flipping the signs of h and k.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf
from pc_common import GRADE, rt

R = random.Random(98301)
X, Y = "<i>x</i>", "<i>y</i>"
ELL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (10, 8, 6), (10, 6, 8), (17, 15, 8), (13, 5, 12)]
HYP = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (12, 5, 13)]


def sh(v, var):
    """(x − h) or x"""
    if v == 0:
        return var
    return "(%s %s %s)" % (var, MINUS if v > 0 else "+", num(abs(v)))


def pt(x, y):
    return "(%s, %s)" % (sf(x), sf(y))


def pts(ps):
    return " and ".join(pt(*p) for p in ps)


def frac_eq(h, k, A, Bv, minus=False):
    return "<span class='fr'><span class='fn'>%s²</span><span class='fd'>%s</span></span> %s <span class='fr'><span class='fn'>%s²</span><span class='fd'>%s</span></span> = 1" % (
        sh(h, X), num(A), MINUS if minus else "+", sh(k, Y), num(Bv))


# ------------------------------------------------------------ set 1: parabolas
def one_par(r):
    p = r.choice([1, 2, 3, -1, -2, -3, F(1, 2), F(-1, 2), 4])
    h, k = r.choice([0, 0, 1, -2, 3]), r.choice([0, 0, -1, 2, 4])
    vert = r.random() < 0.6  # opens up/down: (x − h)² = 4p(y − k)
    lhs = "%s²" % sh(h, X) if vert else "%s²" % sh(k, Y)
    rhs = "%s%s" % (sf(4 * p), sh(k, Y) if vert else sh(h, X))
    eq = "%s = %s" % (lhs, rhs)
    want = r.choice(["focus", "focus", "directrix", "vertex"])
    if want == "vertex":
        right = pt(h, k)
        return T("What is the vertex of the parabola %s?" % eq, right, [pt(-h, -k), pt(k, h) if h != k else pt(h + 1, k), pt(h, k + p) if vert else pt(h + p, k)],
                 "The equation is in the form with (<i>h</i>, <i>k</i>) = <b>%s</b>." % right)
    focus = pt(h, k + p) if vert else pt(h + p, k)
    direc = "%s = %s" % (Y, sf(k - p)) if vert else "%s = %s" % (X, sf(h - p))
    if want == "focus":
        right = focus
        wr = [pt(h, k + 4 * p) if vert else pt(h + 4 * p, k), pt(h, k - p) if vert else pt(h - p, k), pt(h + p, k) if vert else pt(h, k + p)]
    else:
        right = direc
        wr = ["%s = %s" % (Y if vert else X, sf((k if vert else h) + p)), "%s = %s" % (Y if vert else X, sf((k if vert else h) - 4 * p)), "%s = %s" % (X if vert else Y, sf((k if vert else h) - p))]
    return T("What is the %s of the parabola %s?" % (want, eq), right, wr,
             "4<i>p</i> = %s, so <i>p</i> = %s. The parabola opens %s. Focus %s, directrix %s. <b>%s</b>." % (
                 sf(4 * p), sf(p), ("up" if p > 0 else "down") if vert else ("right" if p > 0 else "left"), focus, direc, right))


# ------------------------------------------------------------ set 2: ellipses
def one_ell(r):
    a, b, c = r.choice(ELL)
    h, k = r.choice([0, 0, 1, -2, 3]), r.choice([0, 0, -1, 2, -3])
    horiz = r.random() < 0.5
    eq = frac_eq(h, k, a * a, b * b) if horiz else frac_eq(h, k, b * b, a * a)
    want = r.choice(["foci", "foci", "vert", "center", "major"])
    if want == "center":
        right = pt(h, k)
        return T("What is the center of the ellipse %s?" % eq, right, [pt(-h, -k), pt(h, -k) if k else pt(h + a, k), pt(k, h) if h != k else pt(h, k + b)],
                 "The center is (<i>h</i>, <i>k</i>) = <b>%s</b>." % right)
    if want == "major":
        right = str(2 * a)
        return T("What is the length of the major axis of %s?" % eq, right, [str(a), str(2 * b), str(a * a)], "The larger denominator is <i>a</i>² = %d, so <i>a</i> = %d and the major axis is 2<i>a</i> = <b>%d</b>." % (a * a, a, 2 * a))
    off = (lambda d: [(h + d, k), (h - d, k)]) if horiz else (lambda d: [(h, k + d), (h, k - d)])
    swap = (lambda d: [(h, k + d), (h, k - d)]) if horiz else (lambda d: [(h + d, k), (h - d, k)])
    cw = int(math.isqrt(a * a + b * b)) if math.isqrt(a * a + b * b) ** 2 == a * a + b * b else None
    if want == "foci":
        right = pts(off(c))
        wr = [pts(off(a)), pts(swap(c)), pts(off(cw)) if cw else pts(off(b))]
        return T("What are the foci of the ellipse %s?" % eq, right, wr,
                 "For an ellipse, <i>c</i>² = <i>a</i>² − <i>b</i>² = %d − %d = %d, so <i>c</i> = %d. The major axis is %s. <b>%s</b>." % (a * a, b * b, c * c, c, "horizontal" if horiz else "vertical", right))
    right = pts(off(a))
    return T("What are the vertices (ends of the major axis) of %s?" % eq, right, [pts(off(b)), pts(swap(a)), pts(off(c))],
             "<i>a</i>² = %d is under %s, so the major axis is %s and <i>a</i> = %d. <b>%s</b>." % (a * a, "<i>x</i>" if horiz else "<i>y</i>", "horizontal" if horiz else "vertical", a, right))


# ------------------------------------------------------------ set 3: hyperbolas
def one_hyp(r):
    a, b, c = r.choice(HYP)
    h, k = r.choice([0, 0, 0, 2, -1]), r.choice([0, 0, 0, 1, -3])
    horiz = r.random() < 0.6
    if horiz:
        eq = frac_eq(h, k, a * a, b * b, True)
    else:
        eq = "<span class='fr'><span class='fn'>%s²</span><span class='fd'>%s</span></span> %s <span class='fr'><span class='fn'>%s²</span><span class='fd'>%s</span></span> = 1" % (
            sh(k, Y), num(a * a), MINUS, sh(h, X), num(b * b))
    want = r.choice(["foci", "foci", "vert", "asym", "asym"])
    off = (lambda d: [(h + d, k), (h - d, k)]) if horiz else (lambda d: [(h, k + d), (h, k - d)])
    if want == "foci":
        right = pts(off(c))
        ce = int(math.isqrt(abs(a * a - b * b))) if math.isqrt(abs(a * a - b * b)) ** 2 == abs(a * a - b * b) and a != b else None
        wr = [pts(off(a)), pts(off(ce)) if ce else pts(off(b)), pts([(h, k + c), (h, k - c)]) if horiz else pts([(h + c, k), (h - c, k)])]
        return T("What are the foci of the hyperbola %s?" % eq, right, wr,
                 "For a hyperbola, <i>c</i>² = <i>a</i>² + <i>b</i>² = %d + %d = %d, so <i>c</i> = %d. <b>%s</b>." % (a * a, b * b, c * c, c, right))
    if want == "vert":
        right = pts(off(a))
        return T("What are the vertices of the hyperbola %s?" % eq, right, [pts(off(b)), pts(off(c)), pts([(h, k + a), (h, k - a)]) if horiz else pts([(h + a, k), (h - a, k)])],
                 "The positive term is %s, so the hyperbola opens %s and <i>a</i> = %d. <b>%s</b>." % ("the <i>x</i> term" if horiz else "the <i>y</i> term", "left and right" if horiz else "up and down", a, right))
    if h or k:
        return None
    m = F(b, a) if horiz else F(a, b)
    right = "%s = ±%s%s" % (Y, sf(m), X)
    return T("What are the asymptotes of the hyperbola %s?" % eq, right, ["%s = ±%s%s" % (Y, sf(1 / m), X), "%s = ±%s%s" % (Y, sf(m * m), X), "%s = ±%s%s" % (Y, sf(F(c, a)), X) if F(c, a) not in (m, 1 / m) else "%s = %s%s" % (Y, sf(m), X)],
             "For %s, the asymptotes are %s = ±%s. Here that is <b>%s</b>." % ("<i>x</i>²/<i>a</i>² − <i>y</i>²/<i>b</i>² = 1" if horiz else "<i>y</i>²/<i>a</i>² − <i>x</i>²/<i>b</i>² = 1", Y,
                                                                                   "(<i>b</i>/<i>a</i>)<i>x</i>" if horiz else "(<i>a</i>/<i>b</i>)<i>x</i>", right))


# ------------------------------------------------------------ set 4: identifying conics
def one_id(r):
    kind = r.choice(["type", "type", "type", "circle"])
    if kind == "circle":
        h, k = r.randint(-6, 6), r.randint(-6, 6)
        rr = r.randint(2, 7)
        D, E, Fc = -2 * h, -2 * k, h * h + k * k - rr * rr
        def t(c, s):
            return "" if c == 0 else " %s %s%s" % ("+" if c > 0 else MINUS, num(abs(c)), s)
        eq = "%s² + %s²%s%s%s = 0" % (X, Y, t(D, X), t(E, Y), t(Fc, ""))
        want = r.choice(["center", "radius"])
        if want == "center":
            right = pt(h, k)
            return T("Complete the square to find the center of the circle %s." % eq, right, [pt(-h, -k), pt(D, E), pt(k, h) if h != k else pt(h, -k) if k else pt(h + 1, k)],
                     "%s² + %s² = %d. The center is <b>%s</b>." % (sh(h, X), sh(k, Y), rr * rr, right))
        right = str(rr)
        return T("Complete the square to find the radius of the circle %s." % eq, right, [str(rr * rr), rt(abs(Fc)) if abs(Fc) != rr * rr and Fc else str(rr + 1), str(abs(h) + abs(k)) if abs(h) + abs(k) != rr else str(rr + 2)],
                 "Adding %d and %d to both sides gives %s² + %s² = %d, so <i>r</i> = √%d = <b>%d</b>." % (h * h, k * k, sh(h, X), sh(k, Y), rr * rr, rr * rr, rr))
    shape = r.choice(["circle", "ellipse", "parabola", "hyperbola"])
    a = r.choice([1, 2, 3, 4, 9])
    c = {"circle": a, "ellipse": r.choice([v for v in [1, 2, 4, 9, 16] if v != a]), "parabola": 0, "hyperbola": -r.choice([1, 2, 4, 9])}[shape]
    d, e = r.choice([0, 4, -6, 8]), r.choice([0, 2, -4, 10])
    if shape == "parabola":
        e = r.choice([2, -4, 6, 8])
    f = r.choice([-20, -36, 5, 0, 12])
    swap = r.random() < 0.3
    def t(cf, s, first=False):
        if cf == 0:
            return ""
        if first:
            return ("" if cf == 1 else MINUS if cf == -1 else sf(cf)) + s
        return " %s %s%s" % ("+" if cf > 0 else MINUS, "" if abs(cf) == 1 and s else num(abs(cf)), s)
    terms = [(a, X + "²"), (c, Y + "²")]
    if swap:
        terms = terms[::-1]
    eq = t(terms[0][0], terms[0][1], True) + t(terms[1][0], terms[1][1]) + t(d, X) + t(e, Y) + t(f, "") + " = 0"
    if eq.startswith(" "):
        return None
    why = {"circle": "The <i>x</i>² and <i>y</i>² coefficients are equal", "ellipse": "The <i>x</i>² and <i>y</i>² coefficients have the same sign but are different",
           "parabola": "Only one variable is squared", "hyperbola": "The <i>x</i>² and <i>y</i>² coefficients have opposite signs"}[shape]
    names = ["Circle", "Ellipse", "Parabola", "Hyperbola"]
    right = shape.capitalize()
    return T("Which conic section is %s?" % eq, right, [n for n in names if n != right], "%s. <b>%s</b>." % (why, right))


# ------------------------------------------------------------ set 5: applications
def one_app(r):
    kind = r.choice(["dish", "dish", "gallery", "arch", "hyper"])
    if kind == "dish":
        w = r.choice([4, 6, 8, 10, 12, 16])
        d = r.choice([1, 2, 3, 4])
        p = F(w * w, 16 * d)
        if p.denominator not in (1, 2, 4, 8) or w > 6 * d:
            return None
        q = "A satellite dish is shaped like a parabola. It is %d ft wide and %d ft deep. How far from the vertex should the receiver be placed (at the focus)?" % (w, d)
        right = "%s ft" % num(p)
        return T(q, right, ["%s ft" % num(4 * p), "%s ft" % num(F(w, 2)), "%s ft" % num(F(w * w, 4 * d)) if F(w * w, 4 * d) != 4 * p else "%s ft" % num(p * 2)],
                 "Use %s² = 4<i>p</i>%s with the point (%d, %d): %d = 4<i>p</i>(%d), so <i>p</i> = <b>%s</b>." % (X, Y, w // 2, d, (w // 2) ** 2, d, right))
    if kind == "gallery":
        a, b, c = r.choice(ELL)
        k = r.choice([1, 2, 3])
        q = ("A whispering gallery is shaped like half of an ellipse. It is %d ft long and %d ft high at the center. "
             "How far from the center is each focus, where a whisper can be heard across the room?" % (2 * a * k, b * k))
        right = "%d ft" % (c * k)
        cw = math.isqrt(a * a + b * b)
        return T(q, right, ["%d ft" % (a * k), "%s ft" % (num(cw * k) if cw * cw == a * a + b * b else rt(k * k * (a * a + b * b))), "%d ft" % ((a - b) * k) if a - b != c else "%d ft" % (b * k)],
                 "<i>a</i> = %d and <i>b</i> = %d, so <i>c</i> = √(%d² − %d²) = <b>%s</b>." % (a * k, b * k, a * k, b * k, right))
    if kind == "arch":
        a = r.choice([10, 15, 20, 25])
        b = r.choice([6, 8, 9, 12])
        x = r.choice([F(3, 5), F(4, 5)]) * a
        y = b * math.sqrt(1 - float(x / a) ** 2)
        q = ("A bridge arch is half an ellipse, %d m wide and %d m high at the center. How high is the arch %s m from the center?" % (2 * a, b, num(x)))
        right = "%s m" % num(F(round(y * 10)) / 10)
        return T(q, right, ["%s m" % num(F(round(b * (1 - float(x / a)) * 10)) / 10), "%s m" % num(F(round(b * float(x / a) * 10)) / 10), "%s m" % num(b)],
                 "<i>x</i>²/%d + <i>y</i>²/%d = 1 with <i>x</i> = %s: <i>y</i>² = %d(1 − %s), so <i>y</i> = <b>%s</b>." % (a * a, b * b, num(x), b * b, sf((x / a) ** 2), right))
    a, b, c = r.choice(HYP)
    q = ("Two radio stations are %d miles apart. A ship receives their signals and finds it is always %d miles closer to one station than to the other, "
         "so it lies on a hyperbola with the stations as foci. What is <i>b</i>² for this hyperbola?" % (2 * c, 2 * a))
    return T(q, str(b * b), [str(c * c + a * a), str(a * a), str(c * c)],
             "2<i>c</i> = %d and 2<i>a</i> = %d, so <i>c</i> = %d and <i>a</i> = %d. <i>b</i>² = <i>c</i>² − <i>a</i>² = %d − %d = <b>%d</b>." % (2 * c, 2 * a, c, a, c * c, a * a, b * b))


def build():
    sets = [S("Parabolas", collect(one_par, 20, R)),
            S("Ellipses", collect(one_ell, 20, R)),
            S("Hyperbolas", collect(one_hyp, 20, R)),
            S("Identifying conics", collect(one_id, 20, R)),
            S("Applications", collect(one_app, 20, R))]
    body = lesson(
        "<ul><li><b>Parabola</b> (<i>x</i> − <i>h</i>)² = 4<i>p</i>(<i>y</i> − <i>k</i>): vertex (<i>h</i>, <i>k</i>), focus <i>p</i> units from the vertex, directrix <i>p</i> units on the other side.</li>"
        "<li><b>Ellipse</b> <i>x</i>²/<i>a</i>² + <i>y</i>²/<i>b</i>² = 1 (<i>a</i> &gt; <i>b</i>): vertices at ±<i>a</i>, foci at ±<i>c</i> with <b><i>c</i>² = <i>a</i>² − <i>b</i>²</b>. The larger denominator shows the major axis.</li>"
        "<li><b>Hyperbola</b> <i>x</i>²/<i>a</i>² − <i>y</i>²/<i>b</i>² = 1: vertices at ±<i>a</i>, foci at ±<i>c</i> with <b><i>c</i>² = <i>a</i>² + <i>b</i>²</b>, asymptotes <i>y</i> = ±(<i>b</i>/<i>a</i>)<i>x</i>.</li>"
        "<li>From <i>Ax</i>² + <i>Cy</i>² + …: <i>A</i> = <i>C</i> circle; same sign ellipse; opposite signs hyperbola; one squared term parabola.</li></ul>",
        [("Find the foci of " + frac_eq(0, 0, 25, 9) + ".", ["<i>a</i>² = 25 under <i>x</i>: horizontal", "<i>c</i>² = 25 − 9 = 16, <i>c</i> = 4"], "(4, 0) and (−4, 0)"),
         ("Find the focus and directrix of <i>x</i>² = 8<i>y</i>.", ["4<i>p</i> = 8, <i>p</i> = 2", "Opens up"], "focus (0, 2), directrix <i>y</i> = −2")],
        ["Using <i>c</i>² = <i>a</i>² + <i>b</i>² for an ellipse. That is for hyperbolas.",
         "Using 4<i>p</i> as the distance to the focus. The distance is <i>p</i>.",
         "Choosing the major axis from the first term instead of the larger denominator.",
         "Flipping the signs of <i>h</i> and <i>k</i>: (<i>x</i> − 3) means <i>h</i> = 3."])
    faq = [("How do you find the foci of an ellipse?", "Use c² = a² − b², where a² is the larger denominator. The foci are c units from the center along the major axis."),
           ("How do you find the foci of a hyperbola?", "Use c² = a² + b². The foci are c units from the center, on the same axis as the vertices."),
           ("How do you find the focus of a parabola?", "Write it as (x − h)² = 4p(y − k) or (y − k)² = 4p(x − h). The focus is p units from the vertex, inside the curve."),
           ("How can you tell which conic an equation is?", "Look at the squared terms: equal coefficients give a circle, same signs an ellipse, opposite signs a hyperbola, and only one squared term a parabola.")]
    make("conic-sections", 13, "G-GPE.A.3",
         "Conic Sections: Parabolas, Ellipses and Hyperbolas",
         "Conic Sections Worksheet: Parabolas, Ellipses, Hyperbolas | 100 Questions with Answers",
         "Conic Sections",
         "Derive the equations of ellipses and hyperbolas given the foci, using the fact that the sum or difference of distances from the foci is constant.",
         "Free precalculus worksheet on conic sections: parabolas, ellipses and hyperbolas with foci, vertices, directrix and asymptotes, identifying conics and applications. 100 questions.",
         "Ellipse: c² = a² − b². Hyperbola: c² = a² + b².",
         "Parabola: the focus is p units from the vertex.",
         body, faq, sets, R, domain="Conic Sections", grade=GRADE)


if __name__ == "__main__":
    build()
