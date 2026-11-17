# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Real-Life Graphs (KS3 Algebra)
  python3 tools/gen_uk_maths_y9_real_life_graphs.py
Conversion graphs, distance-time graphs (reading, stops, speed from the gradient), cost graphs with a fixed charge,
and interpreting graphs of real situations such as filling containers.
Wrong answers come from real mistakes: reading the wrong axis, reading a flat section as moving, working out speed
as time ÷ distance, and taking the fixed charge as the cost per unit.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, B, S, make, lesson, collect, T, QN, svg_wrap, line, text, fig, INK, RED, BLUE, gbp, GIRLS, BOYS

R = random.Random(91401)
U = 26
L, TOP = 60, 16


def graph_svg(nx, xs, ny, ys, xl, yl, pts, x0=0, y0=0, xlab_every=1, ylab_every=1, xfmt=None, yfmt=None, marks=()):
    X = lambda u: L + u * U
    Y = lambda u: TOP + (ny - u) * U
    xf = xfmt or (lambda v: num(v))
    yf = yfmt or (lambda v: num(v))
    s = []
    for i in range(nx + 1):
        s.append(line(X(i), Y(0), X(i), Y(ny), "#e2e2e2", 1))
    for j in range(ny + 1):
        s.append(line(X(0), Y(j), X(nx), Y(j), "#e2e2e2", 1))
    s.append(line(X(0), Y(0), X(nx) + 6, Y(0), INK, 2))
    s.append(line(X(0), Y(0), X(0), Y(ny) - 6, INK, 2))
    for i in range(0, nx + 1, xlab_every):
        s.append(text(X(i), Y(0) + 16, xf(x0 + xs * i), 11, weight=400))
    for j in range(0, ny + 1, ylab_every):
        s.append(text(X(0) - 6, Y(j) + 4, yf(y0 + ys * j), 11, weight=400, anchor="end"))
    s.append(text(X(nx / 2.0), Y(0) + 36, xl, 13))
    s.append("<text x='14' y='%d' font-size='13' font-weight='700' fill='%s' text-anchor='middle' transform='rotate(-90 14 %d)'>%s</text>"
             % (Y(ny / 2.0), INK, Y(ny / 2.0), yl))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (
        " ".join("%.1f,%.1f" % (X(a), Y(b)) for a, b in pts), BLUE))
    for (a, b, lab) in marks:
        s.append(text(X(a), Y(b) - 8, lab, 13, col=RED))
    return svg_wrap(L + nx * U + 32, TOP + ny * U + 46, "".join(s), "graph")


def who(r):
    return r.choice(GIRLS + BOYS)


# ------------------------------------------------------------ set 1: conversion graphs
CONV = [
    # name, xlabel, ylabel, x per unit, y per unit, rate y per x (as Fraction), x unit fmt, y unit fmt
    ("money", "Pounds (£)", "Euros (€)", 10, 10, F(6, 5), lambda v: "£%s" % num(v), lambda v: "€%s" % num(v)),
    ("dist", "Miles", "Kilometres", 5, 8, F(8, 5), lambda v: "%s miles" % num(v), lambda v: "%s km" % num(v)),
    ("usd", "Pounds (£)", "US dollars ($)", 10, 10, F(5, 4), lambda v: "£%s" % num(v), lambda v: "$%s" % num(v)),
    ("mass", "Kilograms", "Pounds (lb)", 2, 4, F(11, 5), lambda v: "%s kg" % num(v), lambda v: "%s lb" % num(v)),
]


def one_conv(r):
    nm, xl, yl, xs, ys, rate, fx, fy = r.choice(CONV)
    nx, ny = 10, 10
    # choose x (in units) where y lands on a grid line
    cands = [i for i in range(1, nx + 1) if (rate * xs * i / ys).denominator == 1 and rate * xs * i / ys <= ny]
    if nm == "mass":
        cands = [5, 10] if rate * xs * 5 / ys <= ny else [5]
    if not cands:
        return None
    xu = r.choice(cands)
    yv = rate * xs * xu
    xv = xs * xu
    xmax_u = min(nx, int(ny * ys / (rate * xs)))
    end = (xmax_u, float(rate * xs * xmax_u / ys))
    g = fig(graph_svg(nx, xs, ny, ys, xl, yl, [(0, 0), end], xlab_every=2, ylab_every=2))
    if r.random() < 0.5:
        q = g + "Use the conversion graph to change %s." % fx(xv)
        right = fy(yv)
        wr = [fy(yv + ys), fy(xv) if xv != yv else fy(yv - ys), fx(F(xv) / rate) if (F(xv) / rate).denominator == 1 else fy(yv - ys), fy(yv - ys)]
        e = "Go up from %s to the line, then across: <b>%s</b>." % (fx(xv), right)
    else:
        q = g + "Use the conversion graph to change %s." % fy(yv)
        right = fx(xv)
        wr = [fx(xv + xs), fx(yv) if xv != yv else fx(xv + 2 * xs), fx(xv - xs), fy(xv)]
        e = "Go across from %s to the line, then down: <b>%s</b>." % (fy(yv), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ distance-time journeys
def journey(r):
    """Return list of (t_units, d_units) with t step 1 unit = 15 or 30 min, d step 1 unit = some km."""
    for _ in range(200):
        pts = [(0, 0)]
        t, d = 0, 0
        segs = r.randint(3, 4)
        for i in range(segs):
            kind = r.choice(["go", "go", "stop", "back"]) if i else "go"
            dt = r.randint(1, 3)
            if kind == "go":
                dd = r.randint(1, 4)
                d += dd
            elif kind == "stop":
                dd = 0
            else:
                dd = -r.randint(1, d) if d else 0
                d += dd
            t += dt
            pts.append((t, d))
        if t <= 10 and 2 <= max(p[1] for p in pts) <= 8 and len(set(pts)) == len(pts):
            return pts
    return None


def seg_desc(pts):
    out = []
    for (t1, d1), (t2, d2) in zip(pts, pts[1:]):
        out.append((t1, t2, d1, d2))
    return out


def dt_svg(pts, tstep_min, dstep):
    def tf(v):
        mins = int(v)
        h, m = 9 + mins // 60, mins % 60
        return "%d:%02d" % (h, m)
    return graph_svg(10, tstep_min, 8, dstep, "Time", "Distance from home (km)", pts, xlab_every=2, ylab_every=1, xfmt=tf)


def clock(tu, tstep):
    mins = tu * tstep
    return "%d:%02d" % (9 + mins // 60, mins % 60)


def one_dt(r):
    pts = journey(r)
    if not pts:
        return None
    tstep, dstep = r.choice([(15, 2), (30, 5), (15, 1), (30, 4)])
    g = fig(dt_svg(pts, tstep, dstep))
    nm = who(r)
    k = r.randint(0, 3)
    segs = seg_desc(pts)
    if k == 0:
        t1, t2, d1, d2 = r.choice(segs)
        tu = t2
        q = g + "%s goes on a journey. How far from home is %s at %s?" % (nm, "she" if nm in GIRLS else "he", clock(tu, tstep).replace(":00", ":00"))
        dv = d2 * dstep
        right = "%s km" % num(dv)
        wr = ["%s km" % num(dv + dstep), "%s km" % num(abs(dv - dstep)) if dv != dstep else "%s km" % num(dv + 2 * dstep), "%s km" % num(dv + 2 * dstep)]
        e = "Go up from %s to the graph, then across: <b>%s</b>." % (clock(tu, tstep), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    if k == 1:
        stops = [(t1, t2) for t1, t2, d1, d2 in segs if d1 == d2]
        if not stops:
            return None
        t1, t2 = stops[0]
        q = g + "%s stops for a rest. How long is the stop?" % nm
        mins = (t2 - t1) * tstep
        right = "%d minutes" % mins
        wr = ["%d minutes" % (mins + tstep), "%d minutes" % (mins - tstep) if mins > tstep else "%d minutes" % (mins + 2 * tstep), "%d minutes" % (mins + 2 * tstep)]
        e = "The graph is flat from %s to %s, so the stop lasts <b>%s</b>." % (clock(t1, tstep), clock(t2, tstep), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    if k == 2:
        moving = [(t1, t2, d1, d2) for t1, t2, d1, d2 in segs if d1 != d2]
        t1, t2, d1, d2 = r.choice(moving)
        dist = abs(d2 - d1) * dstep
        hrs = F((t2 - t1) * tstep, 60)
        sp = F(dist) / hrs
        if sp.denominator != 1:
            return None
        q = g + "What is %s's speed between %s and %s?" % (nm, clock(t1, tstep), clock(t2, tstep))
        right = "%s km/h" % num(sp)
        wr = ["%s km/h" % num(dist), "%s km/h" % num(F(dist) / ((t2 - t1) * tstep)) if (F(dist) / ((t2 - t1) * tstep)).denominator == 1 else "%s km/h" % num(sp * 2),
              "%s km/h" % num(sp / 2) if (sp / 2).denominator == 1 else "%s km/h" % num(sp + dstep), "%s km/h" % num(sp * 2)]
        e = "Speed = distance ÷ time = %s km ÷ %s h = <b>%s</b>." % (num(dist), num(hrs), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    far = max(d for _, d in pts)
    q = g + "What is the furthest %s gets from home?" % nm
    right = "%s km" % num(far * dstep)
    tfar = [t for t, d in pts if d == far][0]
    wr = ["%s km" % num(far * dstep + dstep), "%s km" % num(sum(abs(d2 - d1) for _, _, d1, d2 in segs) * dstep), "%s km" % num(far * dstep - dstep)]
    e = "The highest point of the graph is at %s: <b>%s</b>." % (right, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: interpreting distance-time graphs
INTERP = [
    ("On a distance-time graph, what does a horizontal (flat) line show?", "The person is not moving", ["The person is moving fast", "The person is going home", "The person is speeding up"],
     "Distance does not change, so <b>the person is not moving</b>."),
    ("On a distance-time graph, what does a steeper line show?", "A faster speed", ["A slower speed", "Stopping", "Going backwards in time"],
     "More distance in the same time means <b>a faster speed</b>."),
    ("On a distance-time graph (distance from home), what does a line sloping down show?", "Travelling back towards home", ["Travelling away from home", "Stopping", "Slowing down only"],
     "The distance from home is getting smaller: <b>travelling back towards home</b>."),
    ("What does the gradient of a distance-time graph represent?", "Speed", ["Distance", "Time", "Acceleration"],
     "Gradient = distance ÷ time = <b>speed</b>."),
    ("A distance-time graph goes up 30 km in 2 hours. What is the speed?", "15 km/h", ["60 km/h", "32 km/h", "28 km/h"],
     "30 ÷ 2 = <b>15 km/h</b>."),
    ("A distance-time graph goes up 12 km in 30 minutes. What is the speed?", "24 km/h", ["6 km/h", "0.4 km/h", "360 km/h"],
     "30 minutes = 0.5 hours. 12 ÷ 0.5 = <b>24 km/h</b>."),
    ("A cyclist rides 20 km in 1 hour, stops for 30 minutes, then rides 10 km in 30 minutes. Which part is fastest?", "Both riding parts are the same speed", ["The first part", "The last part", "The stop"],
     "First: 20 km/h. Last: 10 ÷ 0.5 = 20 km/h. <b>Both riding parts are the same speed.</b>"),
    ("Why can a distance-time graph never go straight up (vertical)?", "That would mean moving a distance in no time", ["Because people cannot stop", "Because the axes are the wrong way round", "It can, if you are fast"],
     "A vertical line means distance changes with zero time passing: <b>moving a distance in no time</b>, which is impossible."),
    ("Two walkers' graphs cross. What does the crossing point show?", "They are at the same place at the same time", ["They have the same speed", "They have both stopped", "They have both gone home"],
     "Same distance and same time: <b>they are at the same place at the same time</b>."),
    ("A graph of a car's journey is a curve that gets steeper. What is the car doing?", "Speeding up", ["Slowing down", "Stopped", "Going at a steady speed"],
     "The gradient (speed) is increasing: <b>speeding up</b>."),
    ("A distance-time graph is a straight line from (0, 0) to (3 hours, 150 km). What is the average speed?", "50 km/h", ["450 km/h", "150 km/h", "153 km/h"],
     "150 ÷ 3 = <b>50 km/h</b>."),
    ("A train travels at a steady 80 km/h. Which graph shape shows this on a distance-time graph?", "A straight line sloping upwards", ["A horizontal line", "A curve getting steeper", "A vertical line"],
     "Steady speed is a constant gradient: <b>a straight line sloping upwards</b>."),
    ("On a speed-time graph, what does a horizontal line show?", "A constant speed", ["Not moving", "Going home", "Speeding up"],
     "On a speed-time graph the height is the speed, so a flat line means <b>a constant speed</b>. (On a distance-time graph it would mean stopped.)"),
    ("Water is poured at a steady rate into a cylinder. What does the graph of depth against time look like?", "A straight line", ["A curve getting steeper", "A curve getting less steep", "A horizontal line"],
     "A cylinder has the same width all the way up, so the depth rises steadily: <b>a straight line</b>."),
    ("Water is poured at a steady rate into a cone standing on its point. What does the graph of depth against time look like?", "A curve that gets less steep", ["A straight line", "A curve that gets steeper", "A horizontal line"],
     "The cone gets wider higher up, so the depth rises more slowly: <b>a curve that gets less steep</b>."),
    ("Water is poured at a steady rate into a bowl that is narrow at the top. What happens to the depth graph near the top?", "It gets steeper", ["It gets less steep", "It becomes flat", "It goes down"],
     "A narrower part fills up faster, so <b>it gets steeper</b>."),
    ("A plumber charges £40 call-out plus £30 per hour. Where does the cost graph cross the cost axis?", "£40", ["£30", "£70", "£0"],
     "At 0 hours you still pay the call-out fee: <b>£40</b>."),
    ("A cost graph is a straight line from (0, £5) to (10 km, £25). What is the cost per km?", "£2", ["£2.50", "£20", "£5"],
     "(25 − 5) ÷ 10 = <b>£2</b> per km."),
    ("Which of these graphs would go through the origin?", "Pounds against euros", ["Taxi fare against distance", "Phone bill with a monthly fee", "Plumber's bill with a call-out charge"],
     "0 pounds is 0 euros, so <b>pounds against euros</b> goes through (0, 0). The others have a fixed charge."),
    ("A temperature graph rises from 8 am to 2 pm, then falls. When was it warmest?", "2 pm", ["8 am", "Midnight", "11 am"],
     "The highest point is at <b>2 pm</b>."),
]


def interp():
    return [T(q, a, w, e) for q, a, w, e in INTERP]


# ------------------------------------------------------------ set 4: cost graphs with a fixed charge
COST = [("taxi", "Distance (miles)", "Fare (£)", "mile"), ("plumber", "Time (hours)", "Cost (£)", "hour"),
        ("hire", "Time (days)", "Cost (£)", "day"), ("phone", "Data used (GB)", "Monthly bill (£)", "GB")]


def one_cost(r):
    nm, xl, yl, per = r.choice(COST)
    ys = {"taxi": 2, "plumber": 20, "hire": 10, "phone": 2}[nm]
    fixed_u = r.randint(1, 3)
    rate_u = r.choice([F(1, 2), F(1), F(1, 1) * 1, F(3, 4)]) if nm != "plumber" else r.choice([F(1, 2), F(1)])
    xs = 1
    end_x = 10
    end_y = fixed_u + rate_u * end_x
    if end_y > 10:
        end_x = int((10 - fixed_u) / rate_u)
        end_y = fixed_u + rate_u * end_x
    if end_x < 4:
        return None
    pts = [(0, fixed_u), (end_x, float(end_y))]
    g = fig(graph_svg(10, xs, 10, ys, xl, yl, pts, xlab_every=2, ylab_every=2, yfmt=lambda v: "£%s" % num(v)))
    fixed = fixed_u * ys
    rate = rate_u * ys
    k = r.randint(0, 2)
    if k == 0:
        q = g + "The graph shows the cost of a %s. What is the fixed charge?" % {"taxi": "taxi ride", "plumber": "plumber", "hire": "bike hire", "phone": "phone contract"}[nm]
        right = gbp(fixed)
        wr = [gbp(rate), gbp(fixed + rate), gbp(0)]
        e = "The fixed charge is where the line meets the cost axis (when nothing is used): <b>%s</b>." % right
    elif k == 1:
        q = g + "The graph shows the cost of a %s. How much is charged for each %s?" % ({"taxi": "taxi ride", "plumber": "plumber", "hire": "bike hire", "phone": "phone contract"}[nm], per)
        right = gbp(rate)
        wr = [gbp(fixed), gbp(fixed + rate), gbp(rate * 2) if rate * 2 != fixed else gbp(rate + ys)]
        e = "The line rises %s for every 1 %s: the gradient is <b>%s</b>." % (gbp(rate), per, right)
    else:
        xu = r.choice([x for x in range(1, end_x + 1) if (fixed_u + rate_u * x).denominator == 1 or ys % (fixed_u + rate_u * x).denominator == 0])
        cost = fixed + rate * xu
        q = g + "Use the graph to find the cost for %d %s%s." % (xu, per, "" if xu == 1 or per == "GB" else "s")
        right = gbp(cost)
        wr = [gbp(rate * xu), gbp(cost + ys), gbp(cost - ys) if cost - ys > 0 else gbp(cost + 2 * ys)]
        e = "Fixed charge %s + %d × %s = <b>%s</b>." % (gbp(fixed), xu, gbp(rate), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


def body():
    return lesson(
        "<p>Real-life graphs show how one quantity changes with another. On a <b>conversion graph</b>, go up from one axis to the line, "
        "then across to the other axis.</p>"
        "<p>On a <b>distance-time graph</b>, a flat line means stopped, a steeper line means faster, and the <b>gradient is the speed</b>. "
        "On a <b>cost graph</b>, where the line meets the vertical axis is the <b>fixed charge</b> and the gradient is the <b>cost per unit</b>.</p>",
        [("A line goes up 20 km in 30 minutes.", ["30 minutes = 0.5 h.", "20 ÷ 0.5."], "40 km/h"),
         ("A taxi graph starts at £3 and rises £2 per mile.", ["Fixed charge £3, rate £2 per mile."], "Cost for 5 miles: £13"),
         ("A flat section from 10:00 to 10:45.", ["Distance does not change."], "Stopped for 45 minutes")],
        ["Reading the wrong axis.",
         "Thinking a flat line on a distance-time graph means moving at a steady speed.",
         "Working out speed as time ÷ distance, or forgetting to change minutes into hours.",
         "Taking the fixed charge as the cost per unit."])


def problems():
    return interp()


def main():
    sets = [S("Conversion graphs", collect(one_conv, 20, R)),
            S("Reading distance-time graphs", collect(one_dt, 20, R)),
            S("Interpreting real-life graphs", interp()),
            S("Cost graphs", collect(one_cost, 20, R)),
            S("Distance-time graph practice", collect(one_dt, 20, R))]
    make(9, "real-life-graphs", 14, "A",
         "Real-Life Graphs",
         "Year 9 Real-Life Graphs Worksheets: Conversion Graphs, Distance-Time Graphs and Cost Graphs",
         "Real-Life Graphs",
         "Reduce a given linear equation in two variables to the standard form y = mx + c; calculate and interpret gradients "
         "and intercepts of graphs of such linear equations numerically, graphically and algebraically; find approximate "
         "solutions to contextual problems from given graphs of a variety of functions, including piece-wise linear graphs.",
         "Free Year 9 real-life graphs worksheets: read conversion graphs, distance-time graphs (stops and speed), cost graphs "
         "with a fixed charge, and filling containers. 100 questions with answers.",
         "On a distance-time graph, the gradient is the speed.",
         "Flat line: stopped. Steeper line: faster.",
         body(),
         [("How do I read a conversion graph?", "Find the value on one axis, go to the line, then across or down to the other axis."),
          ("How do I find speed from a distance-time graph?", "Speed = distance ÷ time for that section, which is the gradient of the line. Change minutes into hours for km/h."),
          ("What does a horizontal line mean on a distance-time graph?", "The distance is not changing, so the person or vehicle has stopped."),
          ("What is the fixed charge on a cost graph?", "The cost when nothing has been used: where the line crosses the vertical axis.")],
         sets, R)


if __name__ == "__main__":
    main()
