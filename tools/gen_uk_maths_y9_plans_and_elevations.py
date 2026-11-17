# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Plans and Elevations (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y9_plans_and_elevations.py
Plans (from above), front elevations and side elevations of solids made from cubes, elevations from a plan with
heights written on it, counting cubes, and the plans and elevations of common 3-D shapes.
Wrong answers come from real mistakes: drawing the side elevation for the front, mirroring a view, counting
only the visible cubes, and confusing the plan with an elevation.
"""
import math
import random
import uk_ks3
from uk_ks3 import num, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, INK, RED, BLUE

R = random.Random(91301)
A, K, H2 = 24, 20.8, 12.0
TOPC, FRONTC, SIDEC = "#ffffff", "#bcd4ef", "#7fa9da"
LET = "ABCD"


KX, KR, HC, HR = 26, 14, 6, 12


def P(ox, oy, c, r, z):
    return (ox + c * KX - r * KR, oy + c * HC + r * HR - z * A)


def poly(pts, fill):
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.3' stroke-linejoin='round'/>" % (
        " ".join("%.1f,%.1f" % p for p in pts), fill, INK)


def solid(h, ox, oy):
    Rn, Cn = len(h), len(h[0])
    cubes = [(c, r, z) for r in range(Rn) for c in range(Cn) for z in range(h[r][c])]
    cubes.sort(key=lambda t: (t[0] + t[1] + t[2], t[2]))
    s = []
    for c, r, z in cubes:
        p = lambda cc, rr, zz: P(ox, oy, cc, rr, zz)
        s.append(poly([p(c, r, z + 1), p(c + 1, r, z + 1), p(c + 1, r + 1, z + 1), p(c, r + 1, z + 1)], TOPC))
        s.append(poly([p(c, r + 1, z), p(c + 1, r + 1, z), p(c + 1, r + 1, z + 1), p(c, r + 1, z + 1)], FRONTC))
        s.append(poly([p(c + 1, r, z), p(c + 1, r + 1, z), p(c + 1, r + 1, z + 1), p(c + 1, r, z + 1)], SIDEC))
    # direction arrows
    fx, fy = P(ox, oy, Cn / 2.0, Rn, 0)
    s.append(line(fx - 34, fy + 30, fx - 10, fy + 16, RED, 2))
    s.append("<path d='M%.1f %.1f l-9 1 l5 6 Z' fill='%s'/>" % (fx - 8, fy + 15, RED))
    s.append(text(fx - 40, fy + 44, "Front", 13, col=RED))
    sx, sy = P(ox, oy, Cn, Rn / 2.0, 0)
    s.append(line(sx + 34, sy + 30, sx + 10, sy + 16, BLUE, 2))
    s.append("<path d='M%.1f %.1f l9 1 l-5 6 Z' fill='%s'/>" % (sx + 8, sy + 15, BLUE))
    s.append(text(sx + 40, sy + 44, "Side", 13, col=BLUE))
    return "".join(s)


def plan(h):
    return frozenset((r, c) for r in range(len(h)) for c in range(len(h[0])) if h[r][c] > 0)


def front(h):
    Cn = len(h[0])
    cols = [max(h[r][c] for r in range(len(h))) for c in range(Cn)]
    return frozenset((row, c) for c in range(Cn) for row in range(cols[c]))


def side(h):
    Rn = len(h)
    cols = [max(h[r]) for r in range(Rn - 1, -1, -1)]
    return frozenset((row, i) for i in range(Rn) for row in range(cols[i]))


def mirror(v):
    if not v:
        return v
    mc = max(c for _, c in v)
    return frozenset((row, mc - c) for row, c in v)


def bump(v, r):
    cols = sorted(set(c for _, c in v))
    c = r.choice(cols)
    top = max(row for row, cc in v if cc == c)
    if r.random() < 0.5 and top > 0:
        return frozenset(x for x in v if x != (top, c))
    return frozenset(list(v) + [(top + 1, c)])


def grid_view(v, x, y, s=16, kind="elev"):
    """Draw cells. For an elevation, row 0 is at the bottom. For a plan, row 0 is at the top."""
    out = []
    if not v:
        return ""
    mr = max(rw for rw, _ in v)
    for rw, c in v:
        yy = y + (mr - rw) * s if kind == "elev" else y + rw * s
        out.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#dbe8f7' stroke='%s' stroke-width='1.3'/>" % (x + c * s, yy, s, s, INK))
    return "".join(out)


def options_svg(h, views, kinds, title):
    Rn, Cn = len(h), len(h[0])
    ox = 60 + Rn * KR
    zmax = max(max(rw) for rw in h)
    oy = 20 + zmax * A
    body = [solid(h, ox, oy)]
    sh = oy + Cn * HC + Rn * HR + 50
    s16 = 16
    cellw = 86
    y0 = sh + 10
    maxh = max(max(rw for rw, _ in v) + 1 for v in views)
    for i, (v, kd) in enumerate(zip(views, kinds)):
        x = 14 + i * cellw
        body.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='none' stroke='#c9c9c9'/>" % (x - 6, y0 - 4, cellw - 10, maxh * s16 + 34))
        body.append(text(x + 4, y0 + 12, LET[i], 14, anchor="start"))
        mw = max(c for _, c in v) + 1
        gx = x + (cellw - 16 - mw * s16) / 2.0
        gy = y0 + 22 + (maxh - (max(rw for rw, _ in v) + 1)) * s16
        body.append(grid_view(v, gx, gy, s16, kd))
    W = max(14 + 4 * cellw, int(ox + Cn * KX + 90))
    return svg_wrap(W, int(y0 + maxh * s16 + 36), "".join(body), title)


def rand_solid(r, need_gap=False):
    Rn, Cn = r.choice([(2, 3), (3, 3), (2, 4), (3, 2), (2, 2)])
    for _ in range(100):
        h = [[r.choice([0, 1, 1, 2, 2, 3]) for _ in range(Cn)] for _ in range(Rn)]
        if all(v == 0 for v in h[-1]) or all(h[r_][0] == 0 for r_ in range(Rn)) or all(h[r_][-1] == 0 for r_ in range(Rn)):
            continue
        if all(v == 0 for v in h[0]):
            continue
        if sum(map(sum, h)) < 4 or sum(map(sum, h)) > 14:
            continue
        if need_gap and all(v > 0 for row in h for v in row):
            continue
        ok = True
        for rr in range(Rn - 1):
            for c in range(Cn):
                if h[rr][c] and (h[rr + 1][c] > h[rr][c] or (c + 1 < Cn and h[rr + 1][c + 1] > h[rr][c])):
                    ok = False
        if not ok:
            continue
        return h
    return None


_POS = [0]


def next_pos():
    _POS[0] += 1
    return [0, 2, 1, 3, 2, 0, 3, 1][_POS[0] % 8]


def mcq_views(r, correct, cands, kinds_of, title, q, e, h):
    wr = []
    for cv in cands:
        if cv and cv != correct and cv not in wr:
            wr.append(cv)
    if len(wr) < 3:
        return None
    wr = wr[:3]
    r.shuffle(wr)
    idx = next_pos()
    allv = wr[:idx] + [correct] + wr[idx:]
    svg = options_svg(h, allv, [kinds_of(v) for v in allv], title)
    others = [LET[i] for i in range(4) if i != idx]
    return T(fig(svg) + q, LET[idx], others, e)


# ------------------------------------------------------------ sets 1-3
def one_plan(r):
    h = rand_solid(r, need_gap=True)
    if not h:
        return None
    pv = plan(h)
    cands = [mirror(pv), front(h), frozenset((len(h) - 1 - rw, c) for rw, c in pv), bump(pv, r), side(h)]
    return mcq_views(r, pv, cands, lambda v: "plan", "solid made of cubes with four views",
                     "Which drawing shows the <b>plan</b> (the view from above)?",
                     "From above you see one square for every column of cubes, whatever its height. The front is at the bottom of the plan.", h)


def one_front(r):
    h = rand_solid(r)
    if not h:
        return None
    fv = front(h)
    cands = [side(h), mirror(fv), bump(fv, r), plan(h), bump(fv, r)]
    return mcq_views(r, fv, cands, lambda v: "elev", "solid made of cubes with four views",
                     "Which drawing shows the <b>front elevation</b> (the view from the front)?",
                     "From the front each column shows its tallest stack. Read the columns from left to right as you look at the front.", h)


def one_side(r):
    h = rand_solid(r)
    if not h:
        return None
    sv = side(h)
    cands = [front(h), mirror(sv), bump(sv, r), bump(sv, r), plan(h)]
    return mcq_views(r, sv, cands, lambda v: "elev", "solid made of cubes with four views",
                     "Which drawing shows the <b>side elevation</b> (the view from the side arrow)?",
                     "From the side each row of the solid shows its tallest stack. The front of the solid is on the left of this view.", h)


# ------------------------------------------------------------ set 4: numbered plans
def numbered_plan_svg(h, extra_views=None):
    Rn, Cn = len(h), len(h[0])
    s = 34
    x0, y0 = 30, 20
    out = []
    for rr in range(Rn):
        for c in range(Cn):
            if h[rr][c]:
                out.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#f2f7fd' stroke='%s' stroke-width='1.5'/>" % (x0 + c * s, y0 + rr * s, s, s, INK))
                out.append(text(x0 + c * s + s / 2, y0 + rr * s + s / 2 + 6, str(h[rr][c]), 17))
    out.append(text(x0 + Cn * s / 2.0, y0 + Rn * s + 22, "Front", 13, col=RED))
    return out, x0 + Cn * s + 30, y0 + Rn * s + 30


def one_numbered(r):
    h = rand_solid(r)
    if not h:
        return None
    if r.random() < 0.4:
        out, W, Hh = numbered_plan_svg(h)
        n = sum(map(sum, h))
        q = fig(svg_wrap(W, Hh, "".join(out), "plan with heights")) + "The plan shows how many cubes are stacked in each place. How many cubes are there altogether?"
        cnt = sum(1 for rw in h for v in rw if v)
        return T(q, str(n), [str(cnt), str(n + 1), str(sum(max(h[rr][c] for rr in range(len(h))) for c in range(len(h[0]))))] if sum(max(h[rr][c] for rr in range(len(h))) for c in range(len(h[0]))) not in (n, cnt, n + 1) else [str(cnt), str(n + 1), str(n - 1)],
                 "Add the numbers on the plan: <b>%d</b> cubes." % n)
    fv = front(h)
    cands = [side(h), mirror(fv), bump(fv, r), bump(fv, r), mirror(side(h))]
    wr = []
    for cv in cands:
        if cv != fv and cv not in wr:
            wr.append(cv)
    if len(wr) < 3:
        return None
    wr = wr[:3]
    r.shuffle(wr)
    idx = next_pos()
    allv = wr[:idx] + [fv] + wr[idx:]
    out, W, Hh = numbered_plan_svg(h)
    s16, cellw = 16, 86
    maxh = max(max(rw for rw, _ in v) + 1 for v in allv)
    y0 = Hh + 6
    for i, v in enumerate(allv):
        x = 14 + i * cellw
        out.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='none' stroke='#c9c9c9'/>" % (x - 6, y0 - 4, cellw - 10, maxh * s16 + 34))
        out.append(text(x + 4, y0 + 12, LET[i], 14, anchor="start"))
        mw = max(c for _, c in v) + 1
        gx = x + (cellw - 16 - mw * s16) / 2.0
        gy = y0 + 22 + (maxh - (max(rw for rw, _ in v) + 1)) * s16
        out.append(grid_view(v, gx, gy, s16, "elev"))
    svg = svg_wrap(max(W, 14 + 4 * cellw), int(y0 + maxh * s16 + 36), "".join(out), "plan with heights and four views")
    q = fig(svg) + "The plan shows how many cubes are stacked in each place. Which drawing is the <b>front elevation</b>?"
    e = "From the front, each column shows its tallest stack: %s, reading left to right." % ", ".join(str(max(h[rr][c] for rr in range(len(h)))) for c in range(len(h[0])))
    return T(q, LET[idx], [LET[i] for i in range(4) if i != idx], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("What is the plan of a solid?", "The view from directly above", ["The view from the front", "The view from the side", "The net of the solid"],
         "The plan is <b>the view from directly above</b>."),
        ("What is an elevation?", "The view from the front or side", ["The view from above", "The total surface area", "The number of faces"],
         "Elevations are views from <b>the front or side</b>."),
        ("A cylinder stands on its circular base. What is its plan?", "A circle", ["A rectangle", "A triangle", "A square"],
         "From above you see the circular top: <b>a circle</b>."),
        ("A cylinder stands on its circular base. What is its front elevation?", "A rectangle", ["A circle", "A triangle", "An oval"],
         "From the front you see the height and the width: <b>a rectangle</b>."),
        ("A cone stands on its base. What is its front elevation?", "A triangle", ["A circle", "A rectangle", "A trapezium"],
         "From the side the cone narrows to its point: <b>a triangle</b>."),
        ("A cone stands on its base. What is its plan?", "A circle with a dot at the centre", ["A triangle", "A square", "A rectangle"],
         "From above you see the circular base and the point above the centre: <b>a circle with a dot at the centre</b>."),
        ("What are the plan and elevations of a sphere?", "All three are circles", ["All three are squares", "Plan circle, elevations rectangles", "Plan square, elevations circles"],
         "A sphere looks the same from every direction: <b>all three are circles</b>."),
        ("A square-based pyramid stands on its base. What is its plan?", "A square with its diagonals drawn", ["A triangle", "A circle", "A plain square only"],
         "From above you see the square base and the edges meeting at the top: <b>a square with its diagonals drawn</b>."),
        ("A square-based pyramid stands on its base. What is its front elevation?", "A triangle", ["A square", "A circle", "A rectangle"],
         "From the front you see a sloping face: <b>a triangle</b>."),
        ("A solid has plan a circle and front and side elevations that are rectangles. What is it?", "A cylinder", ["A cone", "A sphere", "A cube"],
         "Circle from above and rectangles from the sides: <b>a cylinder</b>."),
        ("A solid has plan a circle and front and side elevations that are triangles. What is it?", "A cone", ["A cylinder", "A sphere", "A pyramid"],
         "<b>A cone</b>."),
        ("A solid has a plan, front elevation and side elevation that are all squares. What is it?", "A cube", ["A cuboid", "A cylinder", "A square-based pyramid"],
         "<b>A cube</b>."),
        ("A cuboid is 5 cm long, 3 cm wide and 2 cm high. What are the dimensions of its plan?", "5 cm by 3 cm", ["5 cm by 2 cm", "3 cm by 2 cm", "5 cm by 5 cm"],
         "From above you see the length and the width: <b>5 cm by 3 cm</b>."),
        ("A cuboid is 5 cm long, 3 cm wide and 2 cm high. What are the dimensions of its front elevation (looking at the long side)?", "5 cm by 2 cm", ["5 cm by 3 cm", "3 cm by 2 cm", "2 cm by 2 cm"],
         "From the front you see the length and the height: <b>5 cm by 2 cm</b>."),
        ("A triangular prism lies on one of its rectangular faces. Its end faces the side. What is its side elevation?", "A triangle", ["A rectangle", "A circle", "A square"],
         "From the end you see the cross-section: <b>a triangle</b>."),
        ("A triangular prism lies on one of its rectangular faces. What is its plan?", "A rectangle", ["A triangle", "A circle", "A pentagon"],
         "From above you see the sloping rectangular faces: <b>a rectangle</b> (with a line along the top edge)."),
        ("Why do two different solids sometimes have the same plan?", "The plan does not show heights", ["Every solid has a different plan", "The plan shows the front", "Plans are always squares"],
         "A plan only shows what is seen from above, so <b>the plan does not show heights</b>."),
        ("In an elevation drawn on squared paper, what does a hidden cube behind another one do?", "It does not change the elevation", ["It adds an extra square", "It makes the view taller", "It is drawn dashed in red"],
         "A cube hidden behind another is not seen, so <b>it does not change the elevation</b>."),
        ("A solid made of cubes has front elevation 3 squares wide and 2 squares tall. What is the greatest number of cubes in that view?", "6", ["5", "3", "2"],
         "3 × 2 = <b>6</b> squares can be seen at most."),
        ("Which view would show the difference between a cylinder and a cuboid with a square base?", "The plan", ["The front elevation", "Neither view", "The side elevation only if it is wider"],
         "From the front both can look like rectangles. <b>The plan</b> shows a circle or a square."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>plan</b> is the view of a 3-D solid from <b>directly above</b>. "
        "An <b>elevation</b> is the view from the <b>front</b> or the <b>side</b>. Each view is a flat 2-D drawing.</p>"
        "<p>For solids made of cubes: the plan shows one square for each column of cubes. "
        "An elevation shows the <b>tallest stack</b> in each column you can see from that direction. Cubes behind other cubes do not show.</p>",
        [("Plan of an L-shape made from 4 cubes in a row with 1 cube on top.", ["From above you see 4 squares."], "4 squares in a row"),
         ("Front elevation of the same solid.", ["The column with 2 cubes is taller."], "4 squares with 1 on top"),
         ("A cylinder standing up.", ["Above: circle. Front: rectangle."], "Circle; rectangle")],
        ["Swapping the front and side elevations.",
         "Drawing a view the wrong way round (mirrored).",
         "Showing the heights on a plan drawing. A plan only shows the outline from above.",
         "Counting only the cubes you can see when a numbered plan gives the heights."])


def letters_in_order(sets, rnd, _orig=uk_ks3.balance):
    """Balance as usual, then put A, B, C, D choices back in order (the letters name the drawings)."""
    _orig(sets, rnd)
    for st in sets:
        for it in st["items"]:
            if sorted(it["c"]) == list(LET):
                ans = it["c"][it["a"]]
                it["c"] = list(LET)
                it["a"] = LET.index(ans)


uk_ks3.balance = letters_in_order


def main():
    sets = [S("Plans", collect(one_plan, 20, R)),
            S("Front elevations", collect(one_front, 20, R)),
            S("Side elevations", collect(one_side, 20, R)),
            S("Plans with heights", collect(one_numbered, 20, R)),
            S("Plans and elevations of 3-D shapes", problems())]
    make(9, "plans-and-elevations", 13, "G",
         "Plans and Elevations",
         "Year 9 Plans and Elevations Worksheets: Views of 3-D Solids from Above, Front and Side",
         "Plans and Elevations",
         "Use the properties of faces, surfaces, edges and vertices of cubes, cuboids, prisms, cylinders, pyramids, cones and "
         "spheres to solve problems in 3-D; interpret mathematical relationships both algebraically and geometrically.",
         "Free Year 9 plans and elevations worksheets: the plan, front elevation and side elevation of solids made from cubes, "
         "numbered plans, and views of cylinders, cones, pyramids and prisms. 100 questions with answers.",
         "Plan: from above. Elevation: from the front or side.",
         "Each view shows the tallest stack in each column you can see.",
         body(),
         [("What is a plan view?", "The 2-D view of a solid seen from directly above."),
          ("What is the difference between a front and a side elevation?", "The front elevation is the view from the front; the side elevation is the view from the side. They often look different."),
          ("How do I draw the elevation of a solid made of cubes?", "For each column you can see, draw the tallest stack. Cubes hidden behind others are not shown."),
          ("What are the views of a cylinder?", "The plan is a circle and the front and side elevations are rectangles.")],
         sets, R)


if __name__ == "__main__":
    main()
