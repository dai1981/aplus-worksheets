# -*- coding: utf-8 -*-
"""
US Algebra 1: Systems of Linear Inequalities (Common Core A-REI.D.12, A-CED.A.3)
  python3 tools/gen_us_math_a1_systems_of_linear_inequalities.py
Testing whether a point is a solution, matching a linear inequality to its graph (dashed or solid boundary,
shading above or below), matching a system to the region where the shadings overlap, writing constraints
from words, and deciding which combinations are possible in real situations.
Wrong answers come from real mistakes: a solid line for < or >, shading the wrong side, testing a point in
only one inequality, and reversing ≥ and ≤ when writing "at least" and "at most".
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, expr, fr, MINUS, fig
from g8_common import grid_svg
from ws_common import BLUE, RED

R = random.Random(90901)
X, Y = "<i>x</i>", "<i>y</i>"
LT, LE, GT, GE = "&lt;", "≤", "&gt;", "≥"
LO, HI, U, M = -6, 6, 22, 22
GREEN2 = "#2e8b57"


def sf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def rhs(m, b):
    m, b = F(m), F(b)
    t = X if m == 1 else (MINUS + X if m == -1 else sf(m) + X)
    if m == 0:
        return sf(b)
    if b == 0:
        return t
    return "%s %s %s" % (t, "+" if b > 0 else MINUS, sf(abs(b)))


def ineq(m, b, sym):
    return "%s %s %s" % (Y, sym, rhs(m, b))


def clip(poly, m, b, above):
    """Keep the part of poly with y >= mx + b (above) or y <= mx + b."""
    f = lambda p: (p[1] - (m * p[0] + b)) * (1 if above else -1)
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = f(p), f(q)
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def picture(ineqs, label="graph of linear inequalities"):
    """ineqs: list of (m, b, sym, colour)."""
    svg = grid_svg(LO, HI, unit=U, label=label)
    Xp = lambda x: M + (x - LO) * U
    Yp = lambda y: M + (HI - y) * U
    box = [(F(LO), F(LO)), (F(HI), F(LO)), (F(HI), F(HI)), (F(LO), F(HI))]
    extra = ""
    for m, b, sym, col in ineqs:
        reg = clip(box, F(m), F(b), sym in (GT, GE))
        if reg:
            extra += "<polygon points='%s' fill='%s' fill-opacity='0.22' stroke='none'/>" % (" ".join("%.1f,%.1f" % (Xp(x), Yp(y)) for x, y in reg), col)
    for m, b, sym, col in ineqs:
        seg = clip(clip(box, F(m), F(b), True), F(m), F(b), False)
        pts = sorted(set((round(float(x), 3), round(float(y), 3)) for x, y in seg))
        if len(pts) >= 2:
            (x1, y1), (x2, y2) = pts[0], pts[-1]
            dash = "" if sym in (LE, GE) else " stroke-dasharray='7 5'"
            extra += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6'%s/>" % (Xp(x1), Yp(y1), Xp(x2), Yp(y2), col, dash)
    return svg.replace("</svg>", extra + "</svg>")


def holds(m, b, sym, x, y):
    v = F(y) - (F(m) * x + F(b))
    return {LT: v < 0, LE: v <= 0, GT: v > 0, GE: v >= 0}[sym]


def rand_line(r):
    m = F(r.choice([1, 2, -1, -2, 3, -3, F(1, 2), F(-1, 2), F(2, 3), 0]))
    b = F(r.randint(-3, 3))
    return m, b


# ------------------------------------------------------------ set 1: is the point a solution?
def one_point(r):
    (m1, b1), (m2, b2) = rand_line(r), rand_line(r)
    if m1 == m2:
        return None
    s1, s2 = r.choice([LT, LE, GT, GE]), r.choice([LT, LE, GT, GE])
    pts = [(x, y) for x in range(-4, 5) for y in range(-4, 5)]
    r.shuffle(pts)
    want = r.choice(["both", "first", "second", "neither"])
    for x, y in pts:
        h1, h2 = holds(m1, b1, s1, x, y), holds(m2, b2, s2, x, y)
        tag = "both" if h1 and h2 else ("first" if h1 else ("second" if h2 else "neither"))
        if tag == want:
            break
    else:
        return None
    q = "Is %s a solution of the system?<br>%s<br>%s" % (B("(%s, %s)" % (num(x), num(y))), B(ineq(m1, b1, s1)), B(ineq(m2, b2, s2)))
    v1, v2 = m1 * x + b1, m2 * x + b2
    right = "Yes" if want == "both" else "No"
    detail = "First: %s %s %s is %s. Second: %s %s %s is %s." % (num(y), s1, sf(v1), "true" if h1 else "false", num(y), s2, sf(v2), "true" if h2 else "false")
    if want == "both":
        e = detail + " It works in both, so <b>yes</b>."
        wr = ["No, it only works in the first", "No, it only works in the second", "No, it works in neither"]
    else:
        e = detail + " A solution must work in <b>both</b>, so <b>no</b>."
        right = {"first": "No, it only works in the first", "second": "No, it only works in the second", "neither": "No, it works in neither"}[want]
        wr = [w for w in ["Yes", "No, it only works in the first", "No, it only works in the second", "No, it works in neither"] if w != right]
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: one inequality from its graph
def one_graph1(r):
    m, b = rand_line(r)
    sym = r.choice([LT, LE, GT, GE])
    q = "Which inequality is shown by the graph?%s" % fig(picture([(m, b, sym, BLUE)]))
    right = ineq(m, b, sym)
    flip = {LT: GT, GT: LT, LE: GE, GE: LE}
    strict = {LT: LE, LE: LT, GT: GE, GE: GT}
    wr = [ineq(m, b, flip[sym]), ineq(m, b, strict[sym]), ineq(-m if m else m, b if m else -b, sym) if (m or b) else ineq(m, b + 1, sym)]
    e = "The boundary is %s. It is %s, so the sign is %s. The shading is %s the line, so <b>%s</b>." % (
        rhs(m, b) if True else "", "dashed (not included)" if sym in (LT, GT) else "solid (included)",
        "&lt; or &gt;" if sym in (LT, GT) else "≤ or ≥", "above" if sym in (GT, GE) else "below", right)
    e = "The boundary line is <i>y</i> = %s. " % rhs(m, b) + e.split(". ", 1)[1]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: a system from its graph
def one_graph2(r):
    (m1, b1), (m2, b2) = rand_line(r), rand_line(r)
    if m1 == m2:
        return None
    s1, s2 = r.choice([LT, LE, GT, GE]), r.choice([LT, LE, GT, GE])
    q = "Which system is shown? The solution region is where the two shadings overlap.%s" % fig(picture([(m1, b1, s1, BLUE), (m2, b2, s2, RED)], "graph of a system of inequalities"))
    sys_ = lambda a, c: "%s and %s" % (ineq(m1, b1, a), ineq(m2, b2, c))
    flip = {LT: GT, GT: LT, LE: GE, GE: LE}
    strict = {LT: LE, LE: LT, GT: GE, GE: GT}
    right = sys_(s1, s2)
    wr = [sys_(flip[s1], s2), sys_(s1, flip[s2]), sys_(strict[s1], strict[s2])]
    e = "Blue line <i>y</i> = %s: %s, shaded %s. Red line <i>y</i> = %s: %s, shaded %s. So <b>%s</b>." % (
        rhs(m1, b1), "dashed" if s1 in (LT, GT) else "solid", "above" if s1 in (GT, GE) else "below",
        rhs(m2, b2), "dashed" if s2 in (LT, GT) else "solid", "above" if s2 in (GT, GE) else "below", right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: writing constraints
def problems_write():
    data = [
        ("Ava works at most 20 hours a week at two jobs: <i>x</i> hours tutoring and <i>y</i> hours at a café. Which inequality shows this?", "<i>x</i> + <i>y</i> ≤ 20",
         ["<i>x</i> + <i>y</i> ≥ 20", "<i>x</i> + <i>y</i> &lt; 20", "<i>xy</i> ≤ 20"], "“At most” means ≤: <b><i>x</i> + <i>y</i> ≤ 20</b>."),
        ("Ava earns $15 an hour tutoring and $10 an hour at the café, and wants to earn at least $240. Which inequality shows this?", "15<i>x</i> + 10<i>y</i> ≥ 240",
         ["15<i>x</i> + 10<i>y</i> ≤ 240", "10<i>x</i> + 15<i>y</i> ≥ 240", "25(<i>x</i> + <i>y</i>) ≥ 240"], "“At least” means ≥: <b>15<i>x</i> + 10<i>y</i> ≥ 240</b>."),
        ("A school club sells pizza slices (<i>p</i>) for $3 and cookies (<i>c</i>) for $1. It needs more than $150. Which inequality fits?", "3<i>p</i> + <i>c</i> &gt; 150",
         ["3<i>p</i> + <i>c</i> ≥ 150", "<i>p</i> + 3<i>c</i> &gt; 150", "3<i>p</i> + <i>c</i> &lt; 150"], "“More than” means &gt;: <b>3<i>p</i> + <i>c</i> &gt; 150</b>."),
        ("A van holds no more than 12 people: <i>a</i> adults and <i>k</i> kids. There must be at least 2 adults. Which system fits?", "<i>a</i> + <i>k</i> ≤ 12 and <i>a</i> ≥ 2",
         ["<i>a</i> + <i>k</i> ≥ 12 and <i>a</i> ≥ 2", "<i>a</i> + <i>k</i> ≤ 12 and <i>a</i> ≤ 2", "<i>a</i> + <i>k</i> &lt; 12 and <i>k</i> ≥ 2"], "No more than 12 → ≤ 12; at least 2 adults → <b><i>a</i> ≥ 2</b>."),
        ("Why are <i>x</i> ≥ 0 and <i>y</i> ≥ 0 often included in a real-world system?", "Amounts like hours or items cannot be negative", ["To make the lines solid", "To make the region larger", "Because every system needs four inequalities"],
         "You cannot work −3 hours or buy −2 items, so <b>the amounts cannot be negative</b>."),
        ("A baker has 24 cups of flour. Bread uses 3 cups and muffins use 2 cups per batch. Which inequality shows the flour limit for <i>b</i> batches of bread and <i>m</i> batches of muffins?", "3<i>b</i> + 2<i>m</i> ≤ 24",
         ["2<i>b</i> + 3<i>m</i> ≤ 24", "3<i>b</i> + 2<i>m</i> ≥ 24", "<i>b</i> + <i>m</i> ≤ 24"], "Flour used must not be more than 24: <b>3<i>b</i> + 2<i>m</i> ≤ 24</b>."),
        ("A theater has 300 seats. Adult tickets (<i>a</i>) cost $10 and child tickets (<i>c</i>) cost $6. It needs at least $2,400 in sales. Which system fits?",
         "<i>a</i> + <i>c</i> ≤ 300 and 10<i>a</i> + 6<i>c</i> ≥ 2,400", ["<i>a</i> + <i>c</i> ≥ 300 and 10<i>a</i> + 6<i>c</i> ≥ 2,400", "<i>a</i> + <i>c</i> ≤ 300 and 10<i>a</i> + 6<i>c</i> ≤ 2,400", "10<i>a</i> + 6<i>c</i> ≤ 300 and <i>a</i> + <i>c</i> ≥ 2,400"],
         "Seats: at most 300. Money: at least $2,400. <b><i>a</i> + <i>c</i> ≤ 300 and 10<i>a</i> + 6<i>c</i> ≥ 2,400</b>."),
        ("Which phrase means ≥?", "At least", ["At most", "Fewer than", "No more than"], "<b>At least</b> 5 means 5 or more: ≥."),
        ("Which phrase means &lt;?", "Fewer than", ["At least", "No less than", "At most"], "<b>Fewer than</b> 10 means less than 10, not including 10."),
        ("Grace needs at least 3 servings of fruit (<i>f</i>) and vegetables (<i>v</i>) together, but no more than 2 servings of fruit. Which system fits?", "<i>f</i> + <i>v</i> ≥ 3 and <i>f</i> ≤ 2",
         ["<i>f</i> + <i>v</i> ≤ 3 and <i>f</i> ≥ 2", "<i>f</i> + <i>v</i> ≥ 3 and <i>f</i> ≥ 2", "<i>f</i> + <i>v</i> &gt; 3 and <i>v</i> ≤ 2"], "Together at least 3 → ≥ 3; fruit no more than 2 → <b><i>f</i> ≤ 2</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def problems_use():
    data = [
        ("For <i>x</i> + <i>y</i> ≤ 20 and 15<i>x</i> + 10<i>y</i> ≥ 240, can Ava work 12 hours tutoring and 6 at the café?", "Yes, both are true",
         ["No, the hours are too many", "No, she earns too little", "No, both are false"], "12 + 6 = 18 ≤ 20 ✓ and 180 + 60 = 240 ≥ 240 ✓: <b>yes</b>."),
        ("For <i>x</i> + <i>y</i> ≤ 20 and 15<i>x</i> + 10<i>y</i> ≥ 240, can Ava work 4 hours tutoring and 14 at the café?", "No, she earns too little",
         ["Yes, both are true", "No, the hours are too many", "No, both are false"], "4 + 14 = 18 ≤ 20 ✓, but 60 + 140 = 200, which is less than 240: <b>she earns too little</b>."),
        ("A van system is <i>a</i> + <i>k</i> ≤ 12 and <i>a</i> ≥ 2. Which group can go?", "3 adults and 9 kids", ["1 adult and 8 kids", "4 adults and 9 kids", "2 adults and 11 kids"], "3 + 9 = 12 ≤ 12 and 3 ≥ 2: <b>3 adults and 9 kids</b>."),
        ("Which point is in the solution region of <i>y</i> &gt; 2<i>x</i> and <i>y</i> &lt; 5?", "(1, 4)", ["(3, 4)", "(0, 6)", "(1, 2)"], "4 &gt; 2 ✓ and 4 &lt; 5 ✓: <b>(1, 4)</b>. (1, 2) fails because 2 is not greater than 2."),
        ("Which point is on the boundary but NOT a solution of <i>y</i> &lt; <i>x</i> + 1?", "(2, 3)", ["(2, 2)", "(0, 0)", "(3, 5)"], "3 = 2 + 1, so (2, 3) is on the dashed line, which is not included: <b>(2, 3)</b>."),
        ("How do you test which side of <i>y</i> ≥ −<i>x</i> + 3 to shade?", "Test a point like (0, 0) in the inequality", ["Always shade above", "Always shade to the right", "Shade both sides"],
         "0 ≥ 3 is false, so shade the side <b>without</b> (0, 0). Testing a point always works."),
        ("A system is <i>y</i> &gt; 2<i>x</i> + 1 and <i>y</i> &lt; 2<i>x</i> − 3. How many solutions does it have?", "None", ["Infinitely many", "Exactly one", "Exactly two"],
         "The lines are parallel; one shading is above the higher line and the other below the lower line, so they never overlap: <b>none</b>."),
        ("Which inequality has a solid boundary and shading below the line?", "<i>y</i> ≤ 3<i>x</i> − 2", ["<i>y</i> &lt; 3<i>x</i> − 2", "<i>y</i> ≥ 3<i>x</i> − 2", "<i>y</i> &gt; 3<i>x</i> − 2"], "≤ gives a solid line and shading below: <b><i>y</i> ≤ 3<i>x</i> − 2</b>."),
        ("To graph 2<i>x</i> + <i>y</i> &gt; 4, it is easiest to first rewrite it as…", "<i>y</i> &gt; −2<i>x</i> + 4", ["<i>y</i> &lt; −2<i>x</i> + 4", "<i>y</i> &gt; 2<i>x</i> + 4", "<i>x</i> &gt; −2<i>y</i> + 4"], "Subtract 2<i>x</i> from both sides: <b><i>y</i> &gt; −2<i>x</i> + 4</b>."),
        ("To graph −<i>y</i> ≤ <i>x</i> − 1, Ethan writes <i>y</i> ≤ −<i>x</i> + 1. What is the correct inequality?", "<i>y</i> ≥ −<i>x</i> + 1", ["<i>y</i> ≤ −<i>x</i> + 1", "<i>y</i> ≥ <i>x</i> − 1", "<i>y</i> ≤ <i>x</i> + 1"],
         "Dividing by −1 reverses the sign: <b><i>y</i> ≥ −<i>x</i> + 1</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>To graph a linear inequality, draw the boundary line <i>y</i> = <i>mx</i> + <i>b</i>. Use a <b>dashed</b> line for &lt; or &gt; "
        "(points on the line are not solutions) and a <b>solid</b> line for ≤ or ≥. Shade <b>above</b> for &gt; or ≥ and <b>below</b> for &lt; or ≤, "
        "or test a point such as (0, 0).</p>"
        "<p>The solution of a <b>system</b> of inequalities is the region where all the shadings <b>overlap</b>. A point is a solution only if "
        "it makes every inequality true.</p>"
        + fig(picture([(1, 1, GE, BLUE), (-2, 2, LT, RED)], "graph of y ≥ x + 1 and y < −2x + 2")),
        [("Is (1, 3) a solution of <i>y</i> ≥ <i>x</i> + 1 and <i>y</i> &lt; −2<i>x</i> + 6?", ["3 ≥ 2 ✓.", "3 &lt; 4 ✓."], "Yes"),
         ("Write a system: at most 10 items, and at least 3 of them are pens (<i>p</i>) with <i>q</i> pencils.", ["<i>p</i> + <i>q</i> ≤ 10.", "<i>p</i> ≥ 3."], "<i>p</i> + <i>q</i> ≤ 10 and <i>p</i> ≥ 3")],
        ["Using a solid line for &lt; or &gt;. Strict inequalities get a dashed line.",
         "Shading the wrong side. Test a point if you are not sure.",
         "Checking a point in only one inequality. It must work in all of them.",
         "Mixing up “at least” (≥) and “at most” (≤)."])


def main():
    sets = [S("Is the point a solution?", collect(one_point, 20, R)),
            S("Graph of one inequality", collect(one_graph1, 20, R)),
            S("Graph of a system", collect(one_graph2, 20, R)),
            S("Write a system of inequalities", problems_write() + collect(one_point, 10, R)),
            S("Systems of inequalities in context", problems_use() + collect(one_graph2, 10, R))]
    make("systems-of-linear-inequalities", 9, "A-REI.D.12",
         "Systems of Linear Inequalities: Graphs, Solutions and Word Problems",
         "Algebra 1 Systems of Inequalities Worksheets: Graphing, Shading and Word Problems (Free, Answer Key)",
         "Systems of linear inequalities",
         "Graph the solutions to a linear inequality in two variables as a half-plane (excluding the boundary in the case of a strict "
         "inequality), and graph the solution set to a system of linear inequalities in two variables as the intersection of the corresponding half-planes.",
         "Free Algebra 1 systems of inequalities worksheets (A-REI.D.12): test points, match inequalities and systems to graphs with dashed "
         "or solid boundaries and shading, and write and use systems of inequalities in word problems. 100 questions with an answer key.",
         "Dashed for < or >, solid for ≤ or ≥. Shade above for > and below for <.",
         "The solutions of a system are where all the shadings overlap.",
         body(),
         [("How do you graph a linear inequality?", "Graph the boundary line (dashed for < or >, solid for ≤ or ≥), then shade above the line for > or ≥ and below it for < or ≤."),
          ("What is the solution of a system of inequalities?", "The region where the shaded areas of all the inequalities overlap. Every point there makes every inequality true."),
          ("How do I know which side to shade?", "Pick a test point not on the line, such as (0, 0). If it makes the inequality true, shade its side; if not, shade the other side."),
          ("Can a system of inequalities have no solution?", "Yes. If the shaded regions never overlap, for example with parallel lines shaded away from each other, there is no solution.")],
         sets, R, domain="Systems")


if __name__ == "__main__":
    main()
