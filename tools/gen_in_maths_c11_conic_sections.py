# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 10: Conic Sections (CBSE Unit III Coordinate Geometry)
  python3 tools/gen_in_maths_c11_conic_sections.py
Circles (centre, radius, equation, completing the square), parabolas y² = ±4ax and x² = ±4ay (focus, directrix, axis,
latus rectum), ellipses and hyperbolas in standard form (vertices, foci, axes, eccentricity, latus rectum), and
finding the equation from given facts (own makers and US Geometry / Precalculus makers).
Wrong answers come from real mistakes: radius² taken as the radius, the focus at (4a, 0), c² = a² + b² for an
ellipse (or a² − b² for a hyperbola), e &gt; 1 for an ellipse, and a latus rectum of 2b/a.
"""
import random, math
from fractions import Fraction as F
from in_sr import U, T2, use, X, Y, rt
from in_common import num, fv
import gen_us_math_ge_equations_of_circles as uc
import gen_us_math_pc_conic_sections as pc

R = random.Random(911110)
cwrite = use(uc, "one_write", R)
cread = use(uc, "one_read", R)
ccs = use(uc, "one_cs", R)
_app = use(pc, "one_app", R)


def app(r):
    it = _app(r)
    return None if it is None or " ft" in it["q"] + " ".join(it["c"]) else it


def pt(x, y):
    return "(%s, %s)" % (fv(x) if isinstance(x, F) else num(x), fv(y) if isinstance(y, F) else num(y))


PAR = [("y", "x", 1), ("y", "x", -1), ("x", "y", 1), ("x", "y", -1)]


def one_par(r):
    sq, ln, s = r.choice(PAR)
    a = r.randint(1, 8)
    eq = "<i>%s</i>² = %s%d<i>%s</i>" % (sq, "" if s > 0 else "−", 4 * a, ln)
    foc = pt(s * a, 0) if ln == "x" else pt(0, s * a)
    dire = "<i>%s</i> = %s" % (ln, num(-s * a))
    k = r.choice(["focus", "dir", "lr", "write"])
    if k == "focus":
        return T2("Find the focus of the parabola %s." % eq, foc, [pt(s * 4 * a, 0) if ln == "x" else pt(0, s * 4 * a), pt(-s * a, 0) if ln == "x" else pt(0, -s * a), pt(0, s * a) if ln == "x" else pt(s * a, 0)],
                  "Compare with %s: 4a = %d, so a = %d and the focus is <b>%s</b>." % ("<i>%s</i>² = %s4a<i>%s</i>" % (sq, "" if s > 0 else "−", ln), 4 * a, a, foc))
    if k == "dir":
        return T2("Find the directrix of the parabola %s." % eq, dire, ["<i>%s</i> = %s" % (ln, num(s * a)), "<i>%s</i> = %s" % (sq, num(-s * a)), "<i>%s</i> = %s" % (ln, num(-s * 4 * a))],
                  "a = %d. The directrix is on the other side of the vertex from the focus: <b>%s</b>." % (a, dire))
    if k == "lr":
        return T2("Find the length of the latus rectum of %s." % eq, str(4 * a), [str(a), str(2 * a), str(8 * a)],
                  "The latus rectum has length 4a = <b>%d</b>." % (4 * a))
    return T2("Find the equation of the parabola with vertex (0, 0) and focus %s." % foc, eq,
              ["<i>%s</i>² = %s%d<i>%s</i>" % (sq, "" if s > 0 else "−", a, ln), "<i>%s</i>² = %s%d<i>%s</i>" % (sq, "−" if s > 0 else "", 4 * a, ln), "<i>%s</i>² = %s%d<i>%s</i>" % (ln, "" if s > 0 else "−", 4 * a, sq)],
              "The focus is on the %s-axis with a = %d, so the equation is <b>%s</b>." % (ln, a, eq))


ELL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (17, 15, 8), (25, 24, 7), (3, 2, None), (4, 2, None), (6, 4, None), (4, 3, None)]


def frac_eq(A, B, minus=False, swap=False):
    p = "<i>x</i>²/%d" % (A * A)
    q = "<i>y</i>²/%d" % (B * B)
    if swap:
        p, q = "<i>x</i>²/%d" % (B * B), "<i>y</i>²/%d" % (A * A)
    if minus:
        return ("%s − %s = 1" % (q, p)) if swap else ("%s − %s = 1" % (p, q))
    return "%s + %s = 1" % (p, q)


def one_ell(r):
    a, b, c = r.choice(ELL)
    vert = r.random() < 0.4
    eq = frac_eq(a, b, swap=vert)
    cc = c if c else None
    cs = num(c) if c else rt(a * a - b * b)
    on = (lambda v: "(0, ±%s)" % v) if vert else (lambda v: "(±%s, 0)" % v)
    k = r.choice(["foci", "e", "lr", "axes", "vert"])
    if k == "foci":
        return T2("Find the foci of the ellipse %s." % eq, on(cs), [on(rt(a * a + b * b)), on(num(a)), ("(±%s, 0)" if vert else "(0, ±%s)") % cs],
                  "a² = %d, b² = %d, so c = √(a² − b²) = %s. The major axis is along the %s-axis: foci <b>%s</b>." % (a * a, b * b, cs, "y" if vert else "x", on(cs)))
    if k == "e":
        ev = fv(F(c, a)) if c else "%s/%d" % (rt(a * a - b * b), a)
        return T2("Find the eccentricity of the ellipse %s." % eq, ev, [fv(F(a, c)) if c else "%d/%s" % (a, rt(a * a - b * b)), fv(F(b, a)), ("%s/%d" % (rt(a * a + b * b), a))],
                  "e = c ÷ a = %s ÷ %d = <b>%s</b> (less than 1 for an ellipse)." % (cs, a, ev))
    if k == "lr":
        return T2("Find the length of the latus rectum of the ellipse %s." % eq, fv(F(2 * b * b, a)), [fv(F(2 * b, a)), fv(F(2 * a * a, b)), fv(F(b * b, a))],
                  "Latus rectum = 2b² ÷ a = 2 × %d ÷ %d = <b>%s</b>." % (b * b, a, fv(F(2 * b * b, a))))
    if k == "axes":
        return T2("Find the lengths of the major and minor axes of %s." % eq, "%d and %d" % (2 * a, 2 * b), ["%d and %d" % (a, b), "%d and %d" % (a * a, b * b), "%d and %d" % (2 * b, 2 * a)],
                  "a = %d and b = %d, so the axes are 2a = %d and 2b = %d: <b>%d and %d</b>." % (a, b, 2 * a, 2 * b, 2 * a, 2 * b))
    return T2("Find the vertices of the ellipse %s." % eq, on(num(a)), [on(num(b)), on(num(a * a)), ("(±%s, 0)" if vert else "(0, ±%s)") % num(a)],
              "The larger denominator %d = a² is under %s², so the vertices are <b>%s</b>." % (a * a, "y" if vert else "x", on(num(a))))


HYP = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (2, 1, None), (1, 2, None), (2, 3, None), (3, 1, None)]


def one_hyp(r):
    a, b, c = r.choice(HYP)
    vert = r.random() < 0.35
    eq = frac_eq(a, b, minus=True, swap=vert)
    cs = num(c) if c else rt(a * a + b * b)
    on = (lambda v: "(0, ±%s)" % v) if vert else (lambda v: "(±%s, 0)" % v)
    k = r.choice(["foci", "e", "lr", "vert"])
    if k == "foci":
        return T2("Find the foci of the hyperbola %s." % eq, on(cs), [on(rt(abs(a * a - b * b))) if a != b else on("0"), on(num(a)), ("(±%s, 0)" if vert else "(0, ±%s)") % cs],
                  "For a hyperbola c² = a² + b² = %d, so c = %s and the foci are <b>%s</b>." % (a * a + b * b, cs, on(cs)))
    if k == "e":
        ev = fv(F(c, a)) if c else "%s/%d" % (rt(a * a + b * b), a)
        return T2("Find the eccentricity of the hyperbola %s." % eq, ev, [fv(F(a, c)) if c else "%d/%s" % (a, rt(a * a + b * b)), fv(F(b, a)), "%s/%d" % (rt(abs(a * a - b * b)), a) if a != b else "1"],
                  "e = c ÷ a = %s ÷ %d = <b>%s</b> (greater than 1 for a hyperbola)." % (cs, a, ev))
    if k == "lr":
        return T2("Find the length of the latus rectum of the hyperbola %s." % eq, fv(F(2 * b * b, a)), [fv(F(2 * b, a)), fv(F(2 * a * a, b)), fv(F(b * b, a))],
                  "Latus rectum = 2b² ÷ a = <b>%s</b>." % fv(F(2 * b * b, a)))
    return T2("Find the vertices of the hyperbola %s." % eq, on(num(a)), [on(num(b)), on(cs), ("(±%s, 0)" if vert else "(0, ±%s)") % num(a)],
              "The positive term is in %s², with a² = %d, so the vertices are <b>%s</b>." % ("y" if vert else "x", a * a, on(num(a))))


def one_circle(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    rad = r.randint(1, 9)
    g, f, c = -h, -k, h * h + k * k - rad * rad
    eq = "<i>x</i>² + <i>y</i>²" + "".join(t for t in [(" %s %d<i>x</i>" % ("+" if 2 * g > 0 else "−", abs(2 * g))) if g else "",
                                                       (" %s %d<i>y</i>" % ("+" if 2 * f > 0 else "−", abs(2 * f))) if f else "",
                                                       (" %s %d" % ("+" if c > 0 else "−", abs(c))) if c else ""]) + " = 0"
    if r.random() < 0.5:
        return T2("Find the radius of the circle %s." % eq, str(rad), [str(rad * rad), rt(abs(c)) if c and rt(abs(c)) != str(rad) else str(rad + 1), str(2 * rad)],
                  "Centre (%s, %s), and r = √(g² + f² − c) = √%d = <b>%d</b>." % (num(h), num(k), rad * rad, rad))
    return T2("Find the centre of the circle %s." % eq, pt(h, k), [pt(-h, -k), pt(2 * h, 2 * k), pt(k, h)],
              "x² + y² + 2g<i>x</i> + 2f<i>y</i> + c = 0 has centre (−g, −f) = <b>%s</b>." % pt(h, k))


U(11, 10, "conic-sections", 10, "III", "Conic Sections: Circle, Parabola, Ellipse and Hyperbola", "conic sections",
  "Sections of a cone: circle, ellipse, parabola, hyperbola, a point, a straight line and a pair of intersecting lines as a degenerated case of a conic section; standard equations and simple properties of parabola, ellipse and hyperbola; standard equation of a circle (summary of the CBSE syllabus)",
  "Class 11 Conic Sections worksheet (NCERT Chapter 10): circles, parabolas, ellipses and hyperbolas in standard form: centre, radius, focus, directrix, foci, vertices, eccentricity and latus rectum. 100 questions with answers.",
  "Ellipse: c² = a² − b², e &lt; 1. Hyperbola: c² = a² + b², e &gt; 1.", "Parabola y² = 4ax: focus (a, 0), directrix x = −a, latus rectum 4a.",
  "<ul><li>Circle: (<i>x</i> − h)² + (<i>y</i> − k)² = r², centre (h, k), radius r.</li>"
  "<li>Parabola <i>y</i>² = 4a<i>x</i>: vertex (0, 0), focus (a, 0), directrix <i>x</i> = −a, latus rectum 4a.</li>"
  "<li>Ellipse <i>x</i>²/a² + <i>y</i>²/b² = 1 (a &gt; b): foci (±c, 0) with c² = a² − b², e = c/a &lt; 1, latus rectum 2b²/a.</li>"
  "<li>Hyperbola <i>x</i>²/a² − <i>y</i>²/b² = 1: foci (±c, 0) with c² = a² + b², e = c/a &gt; 1, latus rectum 2b²/a.</li></ul>",
  [("Find the foci and eccentricity of <i>x</i>²/25 + <i>y</i>²/9 = 1.", ["a = 5, b = 3, c = √(25 − 9) = 4", "e = 4/5"], "(±4, 0), e = 4/5")],
  ["Taking r² as the radius.", "Using c² = a² + b² for an ellipse.", "Putting the focus of y² = 12x at (12, 0) instead of (3, 0)."],
  [("How do I know which axis is the major axis?", "The larger denominator goes with the major axis."), ("What is the eccentricity of a circle?", "0.")],
  [("Circles", [(one_circle, 8), (cwrite, 6), (cread, 3), (ccs, 3)]),
   ("Parabolas", [(one_par, 20)]),
   ("Ellipses", [(one_ell, 20)]),
   ("Hyperbolas", [(one_hyp, 20)]),
   ("Mixed problems", [(one_ell, 6), (one_hyp, 5), (one_par, 6), (app, 3)])], 911110)
