# -*- coding: utf-8 -*-
"""
US Geometry: Segment Addition and Midpoints (Common Core G-CO.A.1)
  python3 tools/gen_us_math_ge_segment_addition_and_midpoints.py
Distance on a number line, the Segment Addition Postulate with numbers and with algebra, midpoints and
segment bisectors, and word problems with points on a straight road.
Wrong answers come from real mistakes: adding coordinates instead of subtracting, adding when a part is
missing, giving x instead of the length that was asked for, and doubling or halving at the wrong time.
"""
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, RED

R = random.Random(92201)


def ov(s):
    return "<span class='ov'>%s</span>" % s


def sg(n):
    return num(n) if n >= 0 else MINUS + num(-n)


def lin(a, b):
    """a x + b"""
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def seg_fig(names, labels, total=None, ticks=False):
    """points along a segment; labels[i] is the text above part i"""
    c = Canvas()
    n = len(names)
    xs = [30 + 260 * i / (n - 1) for i in range(n)]
    c.seg((xs[0], 60), (xs[-1], 60))
    for x, nm in zip(xs, names):
        c.dot((x, 60))
        c.text((x, 82), nm, 16)
    for i, t in enumerate(labels):
        if t:
            c.text(((xs[i] + xs[i + 1]) / 2, 40), t, 15)
        if ticks:
            c.ticks((xs[i], 60), (xs[i + 1], 60), 1)
    if total:
        c.path("M%.1f 104 L%.1f 112 L%.1f 112 L%.1f 104" % (xs[0], xs[0], xs[-1], xs[-1]), w=1.5, pts=[(xs[0], 104), (xs[-1], 112)])
        c.text(((xs[0] + xs[-1]) / 2, 128), total, 15)
    return c.svg("points on a segment, not drawn to scale")


def nl_fig(pts):
    lo = min(p[1] for p in pts) - 2
    hi = max(p[1] for p in pts) + 2
    c = Canvas()
    W = 340
    def X(v):
        return 20 + (v - lo) * W / (hi - lo)
    c.seg((X(lo), 50), (X(hi), 50), w=2)
    c.head((X(hi) + 10, 50), (X(lo), 50))
    c.head((X(lo) - 10, 50), (X(hi), 50))
    step = 1 if hi - lo <= 12 else 2
    for v in range(lo, hi + 1):
        c.seg((X(v), 45), (X(v), 55), w=1.5)
        if v % step == 0:
            c.text((X(v), 72), sg(v), 12, weight=400)
    for n, v in pts:
        c.dot((X(v), 50), 5.5, RED)
        c.text((X(v), 28), n, 16, RED)
    return c.svg("number line", big=True)


# ------------------------------------------------------------ set 1: distance on a number line
def one_nl(r):
    a = r.randint(-12, 8)
    b = a + r.randint(3, 14)
    n1, n2 = r.sample("ABCDEPQRST", 2)
    pts = [(n1, a), (n2, b)]
    r.shuffle(pts)
    d = b - a
    q = "Find %s.%s" % (B(ov(pts[0][0] + pts[1][0]).replace("<b>", "")), fig(nl_fig(pts)))
    q = "Find the length of %s.%s" % (ov(pts[0][0] + pts[1][0]), fig(nl_fig(pts)))
    wr = [abs(a + b), a if a > 0 else -a, d + 1, d - 1]
    e = "Length is the distance between the coordinates: |%s %s %s| = <b>%s</b>." % (
        sg(b), MINUS, "(%s)" % sg(a) if a < 0 else sg(a), num(d))
    if a < 0:
        e += " Subtracting a negative number adds: %s + %s." % (sg(b), num(-a))
    return T(q, num(d), [num(w) for w in dict.fromkeys(wr) if w != d and w > 0][:3], e)


# ------------------------------------------------------------ set 2: segment addition with numbers
def one_add(r):
    A, Bn, C = sorted(r.sample("ABCDEFGHJKLMNPQRSTUVWXYZ", 3)) if r.random() < 0.6 else r.sample("PQRSTUVW", 3)
    p, q_ = r.randint(3, 19), r.randint(3, 19)
    if r.random() < 0.3:
        p, q_ = p + r.choice([0.5, 0.25]) if False else p, q_
    kind = r.choice(["whole", "part", "part"])
    if kind == "whole":
        svg = seg_fig([A, Bn, C], [num(p), num(q_)])
        q = "%s is between %s and %s. %s = %d and %s = %d. Find %s.%s" % (Bn, A, C, A + Bn, p, Bn + C, q_, A + C, fig(svg))
        ans = p + q_
        wr = [abs(p - q_), p * q_, ans + 1]
        e = "Segment Addition Postulate: %s + %s = %s, so %d + %d = <b>%d</b>." % (A + Bn, Bn + C, A + C, p, q_, ans)
    else:
        tot = p + q_
        svg = seg_fig([A, Bn, C], [num(p), "?"], num(tot))
        q = "%s is between %s and %s. %s = %d and %s = %d. Find %s.%s" % (Bn, A, C, A + C, tot, A + Bn, p, Bn + C, fig(svg))
        ans = q_
        wr = [tot + p, tot, abs(ans - 1) if ans > 1 else ans + 2]
        e = "%s + %s = %s, so %d + %s = %d. Subtract: %d %s %d = <b>%d</b>." % (A + Bn, Bn + C, A + C, p, Bn + C, tot, tot, MINUS, p, ans)
    wr = [w for w in dict.fromkeys(wr) if w != ans and w > 0]
    wr += [ans + 2, ans - 2]
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


# ------------------------------------------------------------ set 3: segment addition with algebra
def one_alg(r):
    A, Bn, C = r.choice([("A", "B", "C"), ("P", "Q", "R"), ("J", "K", "L"), ("D", "E", "F"), ("R", "S", "T"), ("X", "Y", "Z")])
    x = r.randint(2, 12)
    a1, b1 = r.randint(1, 5), r.randint(-6, 9)
    a2, b2 = r.randint(1, 5), r.randint(-6, 9)
    L1, L2 = a1 * x + b1, a2 * x + b2
    if L1 < 2 or L2 < 2:
        return None
    tot = L1 + L2
    ask = r.choice(["x", "x", "AB", "BC"])
    svg = seg_fig([A, Bn, C], [lin(a1, b1), lin(a2, b2)], num(tot))
    q = "%s is between %s and %s. %s = %s, %s = %s and %s = %d. %s%s" % (
        Bn, A, C, A + Bn, lin(a1, b1), Bn + C, lin(a2, b2), A + C, tot,
        "Find <i>x</i>." if ask == "x" else "Find %s." % ((A + Bn) if ask == "AB" else (Bn + C)), fig(svg))
    steps = "(%s) + (%s) = %d, so %s = %d, %s<i>x</i> = %d, <i>x</i> = %d." % (
        lin(a1, b1), lin(a2, b2), tot, lin(a1 + a2, b1 + b2) if b1 + b2 else ("%s<i>x</i>" % num(a1 + a2)), tot,
        num(a1 + a2), tot - b1 - b2, x)
    if ask == "x":
        ans = x
        wr = [L1, L2, x + 1, (tot + b1 + b2) // (a1 + a2) if (tot + b1 + b2) % (a1 + a2) == 0 else x + 2]
        e = steps.replace("<i>x</i> = %d." % x, "<b><i>x</i> = %d</b>." % x)
    else:
        ans = L1 if ask == "AB" else L2
        wr = [x, L2 if ask == "AB" else L1, tot]
        e = steps + " Now substitute: %s = <b>%d</b>." % ((A + Bn) if ask == "AB" else (Bn + C), ans)
    if x == 0 or a1 + a2 == 0:
        return None
    wr = [w for w in dict.fromkeys(wr) if w != ans and w > 0] + [ans + 1, ans + 2]
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans][:3], e)


# ------------------------------------------------------------ set 4: midpoints and bisectors
def one_mid(r):
    A, M, Bn = r.choice([("A", "M", "B"), ("P", "M", "Q"), ("C", "D", "E"), ("R", "S", "T"), ("J", "K", "L"), ("F", "G", "H")])
    kind = r.choice(["eq", "eq", "eq", "half", "dbl", "nl"])
    if kind == "nl":
        a = r.randint(-14, 4)
        b = a + 2 * r.randint(2, 8)
        m = (a + b) // 2
        svg = nl_fig([(A, a), (Bn, b)])
        q = "%s is the midpoint of %s. What is the coordinate of %s?%s" % (M, ov(A + Bn), M, fig(svg))
        e = "The midpoint is the average of the endpoints: (%s + %s) ÷ 2 = <b>%s</b>." % (sg(a), "(%s)" % sg(b) if b < 0 else sg(b), sg(m))
        wr = [b - a, (b - a) // 2, m + 1, a + b]
        return T(q, sg(m), [sg(w) for w in dict.fromkeys(wr) if w != m][:3], e)
    if kind in ("half", "dbl"):
        L = r.randint(4, 30) * 2 + (0 if r.random() < 0.8 else 1)
        if kind == "half":
            q = "%s is the midpoint of %s, and %s = %s. Find %s." % (M, ov(A + Bn), A + Bn, num(L), A + M)
            ans = L / 2
            e = "A midpoint splits the segment into two congruent halves: %s ÷ 2 = <b>%s</b>." % (num(L), num(ans))
            wr = [L, L * 2, L / 2 + 1]
        else:
            ans = L
            q = "%s is the midpoint of %s, and %s = %s. Find %s." % (M, ov(A + Bn), M + Bn, num(L / 2 if L % 2 == 0 else L / 2), A + Bn)
            ans = L
            e = "%s = %s, so %s = 2 × %s = <b>%s</b>." % (A + M, num(L / 2), A + Bn, num(L / 2), num(L))
            wr = [L / 2, L + 1, L / 4]
        return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans][:3], e)
    x = r.randint(2, 11)
    a1, a2 = r.sample(range(1, 8), 2)
    b1 = r.randint(-8, 12)
    b2 = a1 * x + b1 - a2 * x
    if abs(b2) > 30 or a1 * x + b1 < 3:
        return None
    half = a1 * x + b1
    ask = r.choice(["x", "whole", "half"])
    svg = seg_fig([A, M, Bn], [lin(a1, b1), lin(a2, b2)], ticks=True)
    q = "%s is the midpoint of %s. %s = %s and %s = %s. %s%s" % (
        M, ov(A + Bn), A + M, lin(a1, b1), M + Bn, lin(a2, b2),
        {"x": "Find <i>x</i>.", "whole": "Find %s." % (A + Bn), "half": "Find %s." % (A + M)}[ask], fig(svg))
    lo, hi = (a1, a2) if a1 > a2 else (a2, a1)
    steps = "A midpoint makes the two halves equal: %s = %s, so %d<i>x</i> = %d and <i>x</i> = %d." % (
        lin(a1, b1), lin(a2, b2), abs(a1 - a2), abs(b2 - b1), x)
    if ask == "x":
        ans, wr = x, [half, 2 * half, x + 1, (b1 + b2) // (a1 + a2) if a1 + a2 and (b1 + b2) % (a1 + a2) == 0 else x - 1]
        e = steps.replace("<i>x</i> = %d." % x, "<b><i>x</i> = %d</b>." % x)
    elif ask == "half":
        ans, wr = half, [x, 2 * half, half + 1]
        e = steps + " %s = %s = <b>%d</b>." % (A + M, lin(a1, b1).replace("<i>x</i>", "(%d)" % x), half)
    else:
        ans, wr = 2 * half, [half, x, 2 * half + 2]
        e = steps + " Each half is %d, so %s = 2 × %d = <b>%d</b>." % (half, A + Bn, half, 2 * half)
    wr = [w for w in dict.fromkeys(wr) if w != ans and w > 0] + [ans + 1, ans + 3]
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans][:3], e)


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["road", "road2", "mid", "trail", "board"])
    if kind == "road":
        t1, t2, t3 = r.sample(["Ashford", "Brookfield", "Cedar Falls", "Dover", "Elmwood", "Fairview", "Glenwood", "Hillsdale"], 3)
        d1, d2 = r.randint(12, 60), r.randint(12, 60)
        q = ("%s, %s and %s are on a straight highway, in that order. It is %d miles from %s to %s and %d miles from %s to %s. "
             "How far is it from %s to %s?" % (t1, t2, t3, d1, t1, t2, d2, t2, t3, t1, t3))
        ans, wr = d1 + d2, [abs(d1 - d2), max(d1, d2), d1 + d2 + 10]
        e = "%s is between the other two, so the distances add: %d + %d = <b>%d miles</b>." % (t2, d1, d2, ans)
        unit = " miles"
    elif kind == "road2":
        t1, t2, t3 = r.sample(["Ashford", "Brookfield", "Cedar Falls", "Dover", "Elmwood", "Fairview", "Glenwood", "Hillsdale"], 3)
        tot, d1 = r.randint(60, 140), r.randint(15, 50)
        q = ("%s drives on a straight road from %s to %s, which is %d miles. %s stops in %s, %d miles from %s. "
             "How many more miles does %s drive to %s?" % (nm, t1, t3, tot, he.capitalize(), t2, d1, t1, he, t3))
        ans, wr = tot - d1, [tot + d1, d1, tot - d1 + 10]
        e = "From %s to %s plus the rest equals the whole trip: %d %s %d = <b>%d miles</b>." % (t1, t2, tot, MINUS, d1, ans)
        unit = " miles"
    elif kind == "mid":
        tot = r.randint(6, 40) * 2
        q = ("A straight bike path is %d miles long. A water station is at the midpoint. %s starts at one end and rides to the station. "
             "How far does %s ride?" % (tot, nm, he))
        ans, wr = tot // 2, [tot, tot // 4, tot * 2]
        e = "The midpoint is halfway: %d ÷ 2 = <b>%d miles</b>." % (tot, ans)
        unit = " miles"
    elif kind == "trail":
        x = r.randint(3, 9)
        a, b = r.randint(2, 5), r.randint(1, 5)
        c_ = r.randint(1, 4)
        L1, L2 = a * x + b, c_ * x
        q = ("A hiking trail goes straight from the parking lot P to a lake L, passing a bridge B. PB = (%s) km and BL = %s km. "
             "The whole trail is %d km. How long is PB?" % (lin(a, b), lin(c_, 0), L1 + L2))
        ans, wr = L1, [x, L2, L1 + L2]
        e = "PB + BL = PL: (%s) + %s = %d, so %d<i>x</i> = %d and <i>x</i> = %d. PB = %d(%d) + %d = <b>%d km</b>." % (
            lin(a, b), lin(c_, 0), L1 + L2, a + c_, L1 + L2 - b, x, a, x, b, L1)
        unit = " km"
    else:
        tot = r.choice([72, 84, 96, 60, 48, 120])
        k = r.choice([2, 3, 4])
        q = ("A board is %d inches long. %s cuts it into %d pieces of equal length. How long is each piece?" % (tot, nm, k))
        ans, wr = tot // k, [tot // (k + 1), tot // (k - 1) if k > 1 else tot, tot - k]
        e = "Equal pieces split the length evenly: %d ÷ %d = <b>%d inches</b>." % (tot, k, ans)
        unit = " inches"
    wr = [w for w in dict.fromkeys(wr) if w != ans and w > 0] + [ans + 5, ans - 5]
    return T(q, num(ans) + unit, [num(w) + unit for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


def build():
    sets = [S("Distance on a number line", collect(one_nl, 20, R)),
            S("Segment Addition Postulate", collect(one_add, 20, R)),
            S("Segment addition with algebra", collect(one_alg, 20, R)),
            S("Midpoints and bisectors", collect(one_mid, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>The <b>length</b> of a segment is the distance between its endpoints. On a number line, subtract the coordinates and take the "
        "absolute value: AB = |<i>b</i> %s <i>a</i>|.</p>"
        "<p><b>Segment Addition Postulate</b>: if B is between A and C, then AB + BC = AC. The two parts add up to the whole.</p>"
        "<p>The <b>midpoint</b> M of %s splits it into two congruent segments: AM = MB, and each is half of AB. "
        "With algebra, set the two halves equal and solve.</p>" % (MINUS, ov("AB")),
        [("B is between A and C. AB = 2<i>x</i> + 1, BC = 3<i>x</i> %s 4 and AC = 32. Find BC." % MINUS,
          ["(2<i>x</i> + 1) + (3<i>x</i> %s 4) = 32" % MINUS, "5<i>x</i> %s 3 = 32, so <i>x</i> = 7" % MINUS, "BC = 3(7) %s 4 = 17" % MINUS], "17"),
         ("M is the midpoint of %s. AM = 4<i>x</i> %s 3 and MB = 2<i>x</i> + 9. Find AB." % (ov("AB"), MINUS),
          ["4<i>x</i> %s 3 = 2<i>x</i> + 9, so <i>x</i> = 6" % MINUS, "AM = 21, so AB = 2 × 21 = 42"], "42")],
        ["Stopping at <i>x</i>. Read the question again: it often asks for a length.",
         "Adding the two parts when the whole is given. Subtract to find the missing part.",
         "Adding coordinates on a number line. Length is the difference, not the sum.",
         "Forgetting to double. If M is the midpoint, AB = 2 × AM."])
    faq = [("What is the Segment Addition Postulate?",
            "If point B is between A and C on a segment, then AB + BC = AC. The lengths of the parts add up to the length of the whole segment."),
           ("How do you find the midpoint on a number line?", "Add the two coordinates and divide by 2. It is the average of the endpoints."),
           ("What is a segment bisector?", "A point, line, ray or segment that passes through the midpoint of a segment and splits it into two equal parts."),
           ("How do you solve a midpoint problem with x?",
            "Set the two halves equal to each other, solve for x, then substitute to find the lengths. Double one half to get the whole segment.")]
    make("segment-addition-and-midpoints", 2, "G-CO.A.1",
         "Segment Addition and Midpoints",
         "Segment Addition Postulate and Midpoints Worksheet (Geometry) | 100 Questions with Answers",
         "Segment Addition and Midpoints",
         "Know precise definitions of angle, circle, perpendicular line, parallel line, and line segment, based on the undefined notions of point, line, distance along a line, and distance around a circular arc.",
         "Free Geometry worksheet on the Segment Addition Postulate and midpoints: lengths on a number line, algebra with x, and word problems. 100 questions with answers.",
         "If B is between A and C, then AB + BC = AC.",
         "A midpoint splits a segment into two equal halves: AM = MB = AB ÷ 2.",
         body, faq, sets, R, domain="Foundations of Geometry", grade="geometry")


if __name__ == "__main__":
    build()
