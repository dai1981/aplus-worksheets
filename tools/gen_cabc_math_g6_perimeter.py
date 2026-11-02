# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: Perimeter of complex shapes (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g6_perimeter.py
Every shape is drawn to scale from its side lengths. Shapes with square corners are stored as grid points,
so a missing side is worked out in code (the lengths going right equal the lengths going left, and the
lengths going down equal the lengths going up). Every answer is parsed back to millimetres and checked
with Decimal. Canadian English (centimetre, metre, colour), metric units only.
4-digit numbers have no separator; 5 or more digits use a no-break space (10 850).
HTML attributes use single quotes (no backslashes in the JSON).
Wrong answers come from real mistakes: missing a side, using the wrong length for a missing side
(the whole side instead of the part, or adding instead of subtracting), adding only the numbers shown,
counting a side that is inside the shape, using the wrong number of sides for a regular polygon,
finding the area, forgetting to halve, and mixing units (3 m + 45 cm = 48).
"""
import json, math, os, random, re
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "


# ------------------------------------------------------------ numbers, units and checking
UNIT = {"mm": D(1), "cm": D(10), "m": D(1000), "km": D(1000000)}
TOK = re.compile(r"([\d. ]+)\s*(km|mm|cm|m)(?![a-zA-Z])")


def parse(s):
    """'12.5 m' -> Decimal mm. None if the string is not a plain length."""
    s = s.strip()
    pos, tot, hit = 0, D(0), False
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        tot += D(mt.group(1).replace(NBSP, "")) * UNIT[mt.group(2)]
        pos, hit = mt.end(), True
    if not hit or s[pos:].strip():
        return None
    return tot


def n(v):
    """BC style: 4 digits plain (1250), 5 or more digits grouped with a no-break space (10 850). Decimals as 12.5."""
    v = D(v)
    if v == v.to_integral_value():
        i = int(v)
        return str(i) if abs(i) < 10000 else "{:,}".format(i).replace(",", NBSP)
    s = format(v.normalize(), "f")
    ip, fp = s.split(".")
    if abs(int(ip)) >= 10000:
        ip = "{:,}".format(int(ip)).replace(",", NBSP)
    return ip + "." + fp


def L(v, u):
    return "%s %s" % (n(v), u)


def plus(nums):
    return " + ".join(n(x) for x in nums)


def clean(v, places=3):
    v = D(v)
    return v > 0 and v == v.quantize(D(1).scaleb(-places))


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, want=None):
    """Correct answer + the first 3 usable distractors from cands (no repeats, no equal lengths,
    nothing zero or negative). want = (value, unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == D(want[0]) * UNIT[want[1]], (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc} if pc is not None else set()
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        lead = x.split(" ")[0].lstrip("$")
        if x in seen or not x or lead.startswith("-") or lead.startswith("−") or lead in ("0", "0.0"):
            continue
        pv = parse(x)
        if pv is not None:
            if pv in vals or pv <= 0:
                continue
            vals.add(pv)
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def lens(vals, u):
    """Distractor list in one unit, skipping values that are not positive or have more than 3 decimals."""
    return [L(v, u) for v in vals if clean(v)]


def fixed(q, choices, a, e):
    """Choices are picture labels (A, B, ...): keep this order; the answer position is fixed."""
    assert len(set(choices)) == 4
    return {"q": q, "c": list(choices), "a": a, "e": e, "fix": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.get("fix"):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fix", None)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ polygon figures
def inside(pt, pts):
    x, y = pt
    k = False
    m = len(pts)
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % m]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                k = not k
    return k


def poly_body(pts, labels, ticks=False, dashed=()):
    """Polygon (pixel points) with a label outside the middle of each side. Returns (body, W, H) with the
    picture moved to start at 0,0. A label of '' is not drawn; a label 'x' or with '?' is red.
    dashed = inside segments ((x1, y1), (x2, y2)) drawn as dashed lines."""
    CW, TH = 9.6, 13
    m = len(pts)
    texts, marks = [], []
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % m]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        Ln = math.hypot(dx, dy)
        nx, ny = dy / Ln, -dx / Ln
        if inside((mx + nx * 2, my + ny * 2), pts):
            nx, ny = -nx, -ny
        if ticks:
            marks.append((mx - nx * 7, my - ny * 7, mx + nx * 7, my + ny * 7))
        t = labels[i]
        if not t:
            continue
        hw = CW * len(t) / 2
        off = 8 + abs(nx) * hw + abs(ny) * TH + (6 if ticks else 0)
        texts.append([mx + nx * off, my + ny * off, hw, t, dx / Ln, dy / Ln, Ln, 0.0, nx, ny, False, mx, my, off])
    # labels at inside corners can bump into each other: slide them along their own side, apart
    def hit(A, B):
        return abs(A[0] - B[0]) < A[2] + B[2] + 10 and abs(A[1] - B[1]) < 2 * TH + 2

    for _ in range(60):
        moved = False
        for a in range(len(texts)):
            for b in range(a + 1, len(texts)):
                A, B = texts[a], texts[b]
                if hit(A, B):
                    # first choice: write the shorter side's label just inside the shape, next to its side
                    done = False
                    for P in sorted((A, B), key=lambda z: z[6]):
                        if P[10] or ticks:
                            continue
                        P[10] = True
                        nxp, nyp = P[11] - P[8] * (P[13] + 4), P[12] - P[9] * (P[13] + 4)
                        box = [(nxp + sx * (P[2] + 4), nyp + sy * 13) for sx in (-1, 1) for sy in (-1, 1)]
                        others = [Z for Z in texts if Z is not P]
                        deep = (P[11] - P[8] * (2 * P[13] + 14), P[12] - P[9] * (2 * P[13] + 14))
                        if all(inside(c, pts) for c in box + [deep]) and not any(
                                hit([nxp, nyp] + P[2:], Z) for Z in others):
                            P[0], P[1] = nxp, nyp
                            P[8], P[9] = -P[8], -P[9]
                            done = True
                            break
                    if done:
                        moved = True
                        continue
                    for P, Q in ((A, B), (B, A)):
                        d = (P[0] - Q[0]) * P[4] + (P[1] - Q[1]) * P[5]
                        sgn = 1 if d >= 0 else -1
                        if abs(P[7] + sgn * 2) <= P[6] / 2 - 6:
                            # slide along the side, but stay next to it
                            P[7] += sgn * 2
                            P[0] += sgn * 2 * P[4]
                            P[1] += sgn * 2 * P[5]
                        else:
                            # no room left along the side: step further out from it
                            P[0] += 2 * P[8]
                            P[1] += 2 * P[9]
                    moved = True
        if not moved:
            break
    texts = [(z[0], z[1], z[2], z[3]) for z in texts]
    xs = [p[0] for p in pts] + [x - hw for x, y, hw, t in texts] + [x + hw for x, y, hw, t in texts]
    ys = [p[1] for p in pts] + [y - TH for x, y, hw, t in texts] + [y + TH for x, y, hw, t in texts]
    pad = 8
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for (a, b) in dashed:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' "
                 "stroke-dasharray='6 5'/>" % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, GREEN))
    for (x1, y1, x2, y2) in marks:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (x1 - ox, y1 - oy, x2 - ox, y2 - oy, INK))
    for x, y, hw, t in texts:
        s.append(text(x - ox, y - oy + 6, t, 17, col=RED if (t == "x" or "?" in t) else INK))
    return "".join(s), W, H


def polygon_svg(pts, labels, label="polygon with side lengths", ticks=False, dashed=()):
    body, W, H = poly_body(pts, labels, ticks, dashed)
    return svg_wrap(W, H, body, label)


def pair_svg(a, b, label):
    """Two polygons side by side with the titles A and B. a, b = (pts, labels)."""
    ba, wa, ha = poly_body(*a)
    bb, wb, hb = poly_body(*b)
    gap, top = 30, 26
    W, H = wa + gap + wb, top + max(ha, hb)
    body = (text(wa / 2, 20, "A", 20) + text(wa + gap + wb / 2, 20, "B", 20) +
            "<g transform='translate(0,%d)'>%s</g>" % (top, ba) +
            "<g transform='translate(%d,%d)'>%s</g>" % (wa + gap, top, bb))
    return svg_wrap(W, H, body, label)


def rect_pts(Lg, Wd, max_w=190, max_h=95):
    Lg, Wd = float(Lg), float(Wd)
    k = min(max_w / Lg, max_h / Wd)
    return [(0, 0), (Lg * k, 0), (Lg * k, Wd * k), (0, Wd * k)]


def rect_svg(Lg, Wd, u, wlab=None, llab=None, label=None):
    """Rectangle drawn to scale, length on top and width on the left."""
    lab = [llab if llab is not None else L(Lg, u), "", "", wlab if wlab is not None else L(Wd, u)]
    return polygon_svg(rect_pts(Lg, Wd), lab, label or "rectangle %s by %s" % (n(Lg), n(Wd)))


def reg_pts(k, r=58):
    rot = -math.pi / 2 - (math.pi / k if k % 2 == 0 else 0)
    return [(r + r * math.cos(2 * math.pi * i / k + rot), r + r * math.sin(2 * math.pi * i / k + rot))
            for i in range(k)]


REG_NAME = {3: "equilateral triangle", 4: "square", 5: "regular pentagon", 6: "regular hexagon",
            8: "regular octagon", 9: "regular nonagon", 10: "regular decagon"}


def a_an(word):
    return ("an " if word[0] in "aeiou" else "a ") + word


def reg_svg(k, lab):
    return polygon_svg(reg_pts(k), [lab] + [""] * (k - 1), "%s with equal sides" % REG_NAME[k], ticks=True)


# ------------------------------------------------------------ shapes with square corners
def ortho_pts(units, max_w=260, max_h=150):
    W = max(x for x, y in units) - min(x for x, y in units)
    H = max(y for x, y in units) - min(y for x, y in units)
    k = min(max_w / W, max_h / H)
    return [(x * k, y * k) for x, y in units]


def ortho_sides(units):
    m = len(units)
    out = []
    for i in range(m):
        (x1, y1), (x2, y2) = units[i], units[(i + 1) % m]
        assert x1 == x2 or y1 == y2
        out.append(abs(x2 - x1) + abs(y2 - y1))
    return out


def ortho_area(units):
    m = len(units)
    a2 = sum(units[i][0] * units[(i + 1) % m][1] - units[(i + 1) % m][0] * units[i][1] for i in range(m))
    return abs(a2) // 2


def is_h(units, i):
    return units[i][1] == units[(i + 1) % len(units)][1]


def solve_side(units, i, sc):
    """A hidden side worked out from the other sides that run the same way (scaled by sc).
    Returns (value, opposite parts, same-way parts): value = sum(opposite) - sum(same)."""
    m = len(units)
    h = is_h(units, i)
    ax = 0 if h else 1
    sign = lambda j: (units[(j + 1) % m][ax] - units[j][ax])
    s_i = sign(i)
    opp, same = [], []
    for j in range(m):
        if j == i or is_h(units, j) != h:
            continue
        v = abs(sign(j)) * sc
        (same if (sign(j) > 0) == (s_i > 0) else opp).append(v)
    val = sum(opp) - sum(same)
    assert val == abs(s_i) * sc, (units, i)
    return val, opp, same


def flip(units, fx, fy):
    W = max(x for x, y in units)
    H = max(y for x, y in units)
    out = [((W - x) if fx else x, (H - y) if fy else y) for x, y in units]
    return out[::-1] if fx != fy else out


def shape_L(rnd):
    while True:
        a, d = rnd.randint(9, 15), rnd.randint(7, 11)
        c, b = rnd.randint(3, a - 4), rnd.randint(3, d - 4)
        u = [(0, 0), (a, 0), (a, b), (c, b), (c, d), (0, d)]
        if len(set(ortho_sides(u))) == 6 and 0.9 <= a / d <= 2:
            return flip(u, rnd.random() < 0.5, rnd.random() < 0.5)


def shape_T(rnd):
    while True:
        W, H = rnd.randint(11, 15), rnd.randint(8, 11)
        h = rnd.randint(3, 4)
        l = rnd.randint(4, W - 7)
        r = rnd.randint(l + 3, W - 4)
        u = [(0, 0), (W, 0), (W, h), (r, h), (r, H), (l, H), (l, h), (0, h)]
        s = ortho_sides(u)
        if len({W, h, W - r, H - h, r - l, l}) == 6:
            return flip(u, False, rnd.random() < 0.5)


# ============================================================ set 1: rectangles review
def set_rect():
    its = []
    for Lg, Wd, u in [(14, 9, "cm"), (23, 17, "m"), (D("8.5"), 4, "cm"), (D("12.5"), D("7.5"), "m"),
                      (D("6.4"), D("3.8"), "cm"), (145, 90, "m"), (D("2.75"), D("1.5"), "m"), (36, 24, "m")]:
        Lg, Wd = D(Lg), D(Wd)
        p = 2 * Lg + 2 * Wd
        cands = [Lg + Wd, 2 * Lg + Wd, Lg + 2 * Wd]
        if Lg * Wd < 2000 and clean(Lg * Wd, 2):
            cands.insert(1, Lg * Wd)
        cands.append(p + 10)
        e = ("A rectangle has 2 lengths and 2 widths: 2 × %s + 2 × %s = %s + %s = <b>%s %s</b>. "
             "%s + %s = %s is only two of the four sides." % (n(Lg), n(Wd), n(2 * Lg), n(2 * Wd), n(p), u,
                                                               n(Lg), n(Wd), n(Lg + Wd)))
        its.append(mcq(fig(rect_svg(Lg, Wd, u)) + "What is the perimeter of the rectangle?",
                       L(p, u), lens(cands, u), e, want=(p, u)))
    for s, u in [(D("13.5"), "cm"), (D(48), "m")]:
        p = 4 * s
        its.append(mcq(fig(polygon_svg(rect_pts(s, s), [L(s, u), "", "", ""], "square")) +
                       "This is a square. What is its perimeter?", L(p, u),
                       lens([2 * s, 3 * s, s * s if s * s < 1000 else s + 4, s + 4], u),
                       "All 4 sides of a square are equal: 4 × %s = <b>%s %s</b>. 2 × %s = %s counts only two sides."
                       % (n(s), n(p), u, n(s), n(2 * s)), want=(p, u)))
    its.append(mcq("A rectangle is <i>l</i> long and <i>w</i> wide. Which expression gives its perimeter?",
                   "2 × (<i>l</i> + <i>w</i>)", ["<i>l</i> × <i>w</i>", "<i>l</i> + <i>w</i>", "2 × <i>l</i> + <i>w</i>"],
                   "Add one length and one width, then double it, because there are two of each: "
                   "<b>2 × (<i>l</i> + <i>w</i>)</b>. This is the same as 2 × <i>l</i> + 2 × <i>w</i>. "
                   "<i>l</i> × <i>w</i> is the area."))
    its.append(mcq("Olivia finds the perimeter of a rectangle 12 m long and 5 m wide like this: "
                   "2 × 12 + 5 = 29 m. What went wrong?", "She left out one width.",
                   ["She found the area.", "She counted one length twice.", "Nothing. 29 m is correct."],
                   "2 × 12 counts both lengths, but + 5 adds only one width. The rectangle has two 5 m widths: "
                   "2 × 12 + 2 × 5 = 24 + 10 = 34 m."))
    # mixing units
    for big, bu, small, su in [(3, "m", 45, "cm"), (D("1.2"), "m", 80, "cm"), (2, "km", 750, "m"),
                               (25, "cm", 60, "mm")]:
        big, small = D(big), D(small)
        k = UNIT[bu] / UNIT[su]
        bigs = big * k
        p = 2 * bigs + 2 * small
        name = {"cm": "centimetres", "m": "metres", "mm": "millimetres"}[su]
        its.append(mcq(fig(polygon_svg(rect_pts(bigs, small), [L(big, bu), "", "", L(small, su)],
                                       "rectangle %s %s by %s %s" % (n(big), bu, n(small), su))) +
                       "What is the perimeter of the rectangle in <b>%s</b>?" % name,
                       L(p, su), lens([2 * big + 2 * small, bigs + small, 2 * bigs + small, big + small], su),
                       "The units are different. Change first: %s %s = %s %s. Then 2 × %s + 2 × %s = %s + %s = "
                       "<b>%s %s</b>. %s mixes %s and %s." % (n(big), bu, n(bigs), su, n(bigs), n(small),
                                                             n(2 * bigs), n(2 * small), n(p), su,
                                                             n(2 * big + 2 * small), bu, su), want=(p, su)))
    for P, Lg, u in [(58, 17, "cm"), (19, D("6.5"), "m"), (1000, 320, "m")]:
        P, Lg = D(P), D(Lg)
        Wd = (P - 2 * Lg) / 2
        assert 2 * Lg + 2 * Wd == P and 0 < Wd < Lg
        its.append(mcq(fig(rect_svg(Lg, Wd, u, wlab="? %s" % u, label="rectangle with unknown width")) +
                       "The perimeter of the rectangle is <b>%s %s</b>. How wide is it?" % (n(P), u),
                       L(Wd, u), lens([P - 2 * Lg, P - Lg, P / 4, Wd + 1], u),
                       "The two lengths use 2 × %s = %s %s. That leaves %s − %s = %s %s for the two widths. "
                       "Each width is %s ÷ 2 = <b>%s %s</b>." % (n(Lg), n(2 * Lg), u, n(P), n(2 * Lg),
                                                                n(P - 2 * Lg), u, n(P - 2 * Lg), n(Wd), u),
                       want=(Wd, u)))
    Lg, Wd = D(3250), D(2175)
    p = 2 * Lg + 2 * Wd
    its.append(mcq("A rectangular farm in the Fraser Valley is 3250 m long and 2175 m wide. "
                   "What is its perimeter?", L(p, "m"), lens([Lg + Wd, 2 * Lg + Wd, Lg + 2 * Wd], "m"),
                   "2 × 3250 + 2 × 2175 = 6500 + 4350 = <b>%s m</b>. 5425 m is one length and one width." % n(p),
                   want=(p, "m")))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter of rectangles: review", "items": its}


# ============================================================ set 2: L and T shapes with missing sides
def find_x_item(units, i, sc, u, kind, rnd):
    sides = [v * sc for v in ortho_sides(units)]
    x, opp, same = solve_side(units, i, sc)
    lab = [L(v, u) for v in sides]
    lab[i] = "x"
    if same:
        how = "%s − %s = <b>%s %s</b>" % (n(sum(opp)), n(sum(same)), n(x), u)
        part = ("the other part is %s %s" % (n(same[0]), u) if len(same) == 1 else
                "the other parts add up to %s = %s %s" % (plus(same), n(sum(same)), u))
        e = ("Look at the sides that run the same way as x. The whole side is %s %s, and %s. "
             "So x = %s. Using %s %s for x uses the whole side, not the part."
             % (n(sum(opp)), u, part, how, n(sum(opp)), u))
        cands = [sum(opp), sum(opp) + sum(same), sum(same)] + [v for v in sides if v != x]
    else:
        e = ("x is the whole side. It is made of the parts across from it: %s = <b>%s %s</b>. "
             "Subtracting the parts gives the wrong length." % (plus(opp), n(x), u))
        cands = [abs(opp[0] - opp[-1]) if len(opp) > 1 else None, max(opp), min(opp)] + [v for v in sides if v != x]
    cands = [v for v in cands if v is not None and v != x]
    q = (fig(polygon_svg(ortho_pts(units), lab, "%s with a missing side x" % kind)) +
         "All the corners are square corners. What is the length of side <b>x</b>?")
    return mcq(q, L(x, u), lens(cands, u), e, want=(x, u))


def perim_item(units, hide, sc, u, kind, extra=""):
    sides = [v * sc for v in ortho_sides(units)]
    p = sum(sides)
    lab = [L(v, u) for v in sides]
    for i in hide:
        lab[i] = "?"
    found, wrongs = [], []
    for i in hide:
        x, opp, same = solve_side(units, i, sc)
        found.append((i, x, opp, same))
    shown = sum(v for j, v in enumerate(sides) if j not in hide)
    cands = [shown]
    for i, x, opp, same in found:
        cands.append(p - x)
        if same:
            cands.append(p - x + sum(opp))      # used the whole side instead of the part
    cands.append(ortho_area(units) * sc * sc if ortho_area(units) * sc * sc != p else None)
    cands.append(p + 2 * sc)
    steps = []
    for i, x, opp, same in found:
        if same:
            grp = lambda v: n(v[0]) if len(v) == 1 else "(" + plus(v) + ")"
            steps.append("%s − %s = %s" % (grp(opp), grp(same), n(x)))
        else:
            steps.append("%s = %s" % (plus(opp), n(x)))
    e = ("First find the missing sides: %s. Then add all %d sides: %s = <b>%s %s</b>. "
         "%s %s is only the sides with numbers." % (" and ".join(steps), len(sides), plus(sides), n(p), u,
                                                    n(shown), u)) + extra
    q = (fig(polygon_svg(ortho_pts(units), lab, "%s with missing sides" % kind)) +
         "All the corners are square corners. What is the perimeter of the shape?")
    return mcq(q, L(p, u), lens([c for c in cands if c is not None], u), e, want=(p, u))


def set_lt(rnd):
    its = []
    # find x on L shapes: 6
    for k, (sc, u) in enumerate([(1, "cm"), (1, "m"), (D("0.5"), "m"), (2, "cm"), (10, "cm"), (1, "m")]):
        units = shape_L(rnd)
        hs = [i for i in range(6) if is_h(units, i)]
        vs = [i for i in range(6) if not is_h(units, i)]
        i = rnd.choice(hs if k % 2 == 0 else vs)
        its.append(find_x_item(units, i, D(sc), u, "L-shaped figure", rnd))
    # find x on T shapes: 3
    for sc, u in [(1, "cm"), (D("1.5"), "m"), (5, "cm")]:
        units = shape_T(rnd)
        hs = [i for i in range(8) if is_h(units, i)]
        # a shoulder or the bottom of the stem (never the long top, which needs three parts)
        cand = [i for i in hs if ortho_sides(units)[i] != max(ortho_sides(units))]
        i = rnd.choice(cand)
        its.append(find_x_item(units, i, D(sc), u, "T-shaped figure", rnd))
    # perimeter of L shapes with two missing sides: 7
    for sc, u in [(1, "cm"), (1, "m"), (2, "m"), (D("0.5"), "cm"), (1, "cm"), (10, "m"), (D("2.5"), "m")]:
        units = shape_L(rnd)
        hs = [i for i in range(6) if is_h(units, i)]
        vs = [i for i in range(6) if not is_h(units, i)]
        hide = [rnd.choice(hs), rnd.choice(vs)]
        W = max(x for x, y in units) * D(sc)
        H = max(y for x, y in units) * D(sc)
        extra = (" Shortcut: an L shape has the same perimeter as the rectangle around it, "
                 "2 × (%s + %s) = %s." % (n(W), n(H), n(2 * (W + H))))
        assert sum(ortho_sides(units)) * D(sc) == 2 * (W + H)
        its.append(perim_item(units, hide, D(sc), u, "L-shaped figure", extra))
    # perimeter of T shapes: 4
    for sc, u in [(1, "cm"), (1, "m"), (D("0.5"), "m"), (3, "cm")]:
        units = shape_T(rnd)
        S = ortho_sides(units)
        hs = [i for i in range(8) if is_h(units, i) and S[i] != max(S)]
        vs = [i for i in range(8) if not is_h(units, i)]
        hide = [rnd.choice(hs), rnd.choice(vs)]
        its.append(perim_item(units, hide, D(sc), u, "T-shaped figure"))
    order = [0, 1, 9, 10, 2, 3, 11, 12, 6, 16, 4, 13, 7, 17, 5, 14, 8, 18, 15, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "L and T shapes: find the missing sides", "items": its}


# ============================================================ set 3: regular polygons
def set_regular():
    its = []
    for k, s, u in [(3, "12.5", "cm"), (5, "14", "cm"), (6, "9.5", "cm"), (8, "15", "cm"), (10, "6", "m"),
                    (6, "2.5", "m"), (5, "3.4", "m"), (8, "0.75", "m"), (3, "45", "mm"), (10, "12.5", "cm")]:
        s = D(s)
        p = k * s
        cands = [(k - 1) * s, 4 * s, (k + 1) * s, k + s, 2 * s]
        e = ("%s has %d equal sides. Multiply: %d × %s = <b>%s %s</b>. "
             % (a_an(REG_NAME[k]).capitalize(), k, k, n(s), n(p), u))
        e += "%s × 4 = %s would treat it like a square." % (n(s), n(4 * s)) if k != 4 else ""
        its.append(mcq(fig(reg_svg(k, L(s, u))) +
                       "All the sides of this %s are the same length. What is its perimeter?" % REG_NAME[k],
                       L(p, u), lens(cands, u), e, want=(p, u)))
    for k, P, u in [(6, "57", "cm"), (8, "100", "m"), (5, "8.5", "m"), (10, "135", "cm")]:
        P = D(P)
        s = P / k
        assert s * k == P and clean(s, 2)
        cands = [P / 4, P / (k - 1), P / 2, P - k, s * 10]
        its.append(mcq("%s has a perimeter of <b>%s %s</b>. How long is each side?" % (a_an(REG_NAME[k]).capitalize(),
                                                                                       n(P), u), L(s, u),
                       lens([c for c in cands if clean(c, 2)], u),
                       "%s has %d equal sides: %s ÷ %d = <b>%s %s</b>. Check: %d × %s = %s. "
                       "Dividing by 4 only works for a square." % (a_an(REG_NAME[k]).capitalize(), k, n(P), k,
                                                                   n(s), u, k, n(s), n(P)), want=(s, u)))
    its.append(mcq("A regular octagon has a perimeter of 96 cm. Which number sentence finds the length of one side?",
                   "96 ÷ 8", ["96 ÷ 4", "96 × 8", "96 − 8"],
                   "An octagon has 8 equal sides, so share the perimeter into 8 parts: <b>96 ÷ 8</b> = 12 cm."))
    its.append(mcq("A regular polygon has sides of 7 cm. Its perimeter is 63 cm. How many sides does it have?",
                   "9", ["8", "7", "56"],
                   "Number of sides = perimeter ÷ side length: 63 ÷ 7 = <b>9</b>. It is a regular nonagon. "
                   "Check: 9 × 7 = 63."))
    assert 4 * 15 == 6 * 10
    its.append(mcq("Which has the longer perimeter: a square with 15 cm sides or a regular hexagon with 10 cm sides?",
                   "They are the same, 60 cm", ["The square, 225 cm", "The hexagon, 70 cm", "The square, 60 cm"],
                   "Square: 4 × 15 = 60 cm. Hexagon: 6 × 10 = 60 cm. <b>They are the same.</b> "
                   "225 is the area of the square, and 70 cm uses 7 sides for the hexagon."))
    its.append(mcq("Each regular polygon below has 6 cm sides. Which one has a perimeter of 48 cm?",
                   "a regular octagon", ["a regular hexagon", "a regular pentagon", "a regular decagon"],
                   "48 ÷ 6 = 8 sides, so it is <b>a regular octagon</b>. Check: 8 × 6 = 48 cm."))
    its.append(mcq("An equilateral triangle has sides of <b>1.25 m</b>. What is its perimeter in centimetres?",
                   "375 cm", ["3.75 cm", "37.5 cm", "250 cm"],
                   "3 × 1.25 = 3.75 m. 1 m = 100 cm, so 3.75 m = <b>375 cm</b>. 3.75 cm forgets to change "
                   "metres to centimetres.", want=(375, "cm")))
    its.append(mcq("A stop sign is shaped like a regular octagon. Each side is about 30 cm. About how long is the edge "
                   "all the way around, in metres?", "2.4 m", ["1.2 m", "2.1 m", "240 m"],
                   "8 × 30 = 240 cm. 100 cm = 1 m, so 240 cm = <b>2.4 m</b>. 1.2 m uses only 4 sides, and 2.1 m "
                   "uses 7 sides.", want=(D("2.4"), "m")))
    assert len(its) == 20, len(its)
    order = [0, 1, 8, 2, 3, 14, 4, 10, 5, 9, 6, 11, 16, 7, 12, 15, 13, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Regular polygons: side length × number of sides", "items": its}


# ============================================================ set 4: composite shapes
def house_pts(base, wall, roof, k=14):
    """Rectangle with a triangle roof (isosceles). Pixel points, top first, going clockwise."""
    base, wall, roof = float(base), float(wall), float(roof)
    th = math.sqrt(roof * roof - (base / 2) ** 2)
    return [(base / 2 * k, 0), (base * k, th * k), (base * k, (th + wall) * k), (0, (th + wall) * k), (0, th * k)], th


def hex_row_svg(count, lab):
    """Regular hexagons (pointy top) in a row, each sharing a side with the next."""
    s = 34
    w = math.sqrt(3) * s
    polys = []
    for i in range(count):
        cx, cy = w / 2 + i * w, s
        polys.append([(cx + s * math.cos(math.radians(-90 + 60 * j)), cy + s * math.sin(math.radians(-90 + 60 * j)))
                      for j in range(6)])
    pad, top = 10, 8
    W = int(math.ceil(count * w + 2 * pad + 40))
    H = int(math.ceil(2 * s + 2 * top))
    body = []
    for pts in polys:
        body.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
                    % (" ".join("%.1f,%.1f" % (x + pad + 40, y + top) for x, y in pts), FILL, GREEN))
    # label the left side of the first hexagon (vertices 4 and 5)
    (x1, y1), (x2, y2) = polys[0][4], polys[0][5]
    body.append(text((x1 + x2) / 2 + pad + 40 - 30, (y1 + y2) / 2 + top + 6, lab, 17))
    return svg_wrap(W, H, "".join(body), "%d regular hexagons in a row" % count)


def set_composite():
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, want=want))

    # U shape, all sides labelled (decimals)
    U = [(0, 0), (3, 0), (3, 5), (9, 5), (9, 0), (12, 0), (12, 8), (0, 8)]
    sc = D("1.5")
    s = [v * sc for v in ortho_sides(U)]
    p = sum(s)
    assert p == D(75)
    add(fig(polygon_svg(ortho_pts(U), [L(v, "m") for v in s], "U-shaped figure with side lengths")) +
        "What is the perimeter of this shape?", L(p, "m"),
        lens([2 * (12 * sc + 8 * sc), p - 9, p - D("7.5"), p - D("4.5")], "m"),
        "Add all 8 sides: %s = <b>%s m</b>. The notch adds two 7.5 m sides, so the answer is more than the "
        "%s m of a plain 18 m by 12 m rectangle." % (plus(s), n(p), n(2 * (12 * sc + 8 * sc))), want=(p, "m"))
    # U shape, notch depth and bottom missing
    U2 = [(0, 0), (4, 0), (4, 6), (10, 6), (10, 0), (14, 0), (14, 9), (0, 9)]
    s2 = ortho_sides(U2)
    p2 = sum(s2)
    assert s2 == [4, 6, 6, 6, 4, 9, 14, 9] and p2 == 58
    lab = ["4 cm", "?", "?", "", "4 cm", "9 cm", "14 cm", "9 cm"]
    lab[3] = "6 cm"
    add(fig(polygon_svg(ortho_pts(U2), lab, "U-shaped figure with missing sides")) +
        "All the corners are square corners. The two sides of the notch are the same length. "
        "What is the perimeter?", "58 cm", lens([46, 52, 64, 46 + 14], "cm"),
        "The notch is 6 cm deep, so its other side is also 6 cm. The bottom of the notch is 14 − 4 − 4 = 6 cm. "
        "Add all 8 sides: %s = <b>58 cm</b>. 46 cm adds only the sides with numbers." % plus(s2), want=(58, "cm"))
    # Kai's shortcut claim on a U shape
    add("Kai says a U-shaped figure has the same perimeter as the 12 cm by 8 cm rectangle around it. "
        "The notch in the U is 5 cm deep. What is the real perimeter?", "50 cm", ["40 cm", "45 cm", "96 cm"],
        "The rectangle around it has 2 × (12 + 8) = 40 cm. The notch adds two extra sides going in and out: "
        "2 × 5 = 10 cm. 40 + 10 = <b>50 cm</b>. The shortcut works for an L shape, but not when there is a notch.",
        want=(50, "cm"))
    # H shape
    H = [(0, 0), (3, 0), (3, 4), (9, 4), (9, 0), (12, 0), (12, 11), (9, 11), (9, 7), (3, 7), (3, 11), (0, 11)]
    sH = ortho_sides(H)
    pH = sum(sH)
    assert sH == [3, 4, 6, 4, 3, 11, 3, 4, 6, 4, 3, 11] and pH == 62
    labH = ["3 m", "", "", "", "3 m", "11 m", "3 m", "", "", "", "3 m", "11 m"]
    add(fig(polygon_svg(ortho_pts(H), labH, "H-shaped figure with side lengths")) +
        "All the corners are square corners. Each notch in this H shape is 6 m wide and 4 m deep. "
        "What is the perimeter?", L(pH, "m"),
        lens([2 * (12 + 11), pH - 6, pH - 8, 3 * 4 + 11 * 2 + 6 * 2 + 4 * 2], "m"),
        "Count the sides first: 12. Each notch has two 4 m sides and one 6 m side. Add them all: %s = <b>%d m</b>. "
        "46 m is the rectangle around it, which leaves out the four 4 m sides that go in and out of the notches."
        % (plus(sH), pH), want=(pH, "m"))
    # zigzag (Z) shape with missing sides
    Z = [(0, 0), (6, 0), (6, 3), (10, 3), (10, 7), (4, 7), (4, 4), (0, 4)]
    sZ = ortho_sides(Z)
    pZ = sum(sZ)
    assert sZ == [6, 3, 4, 4, 6, 3, 4, 4] and pZ == 34
    labZ = ["6 cm", "3 cm", "4 cm", "4 cm", "6 cm", "?", "?", "4 cm"]
    add(fig(polygon_svg(ortho_pts(Z), labZ, "step-shaped figure with missing sides")) +
        "All the corners are square corners. What is the perimeter?", "34 cm",
        lens([27, 30, 31, 37], "cm"),
        "Going down on the right: 3 + 4 = 7 cm, so going up on the left must also be 7 cm. The missing up side "
        "is 7 − 4 = 3 cm. Going right: 6 + 4 = 10 cm, so going left must be 10 cm. The missing side is "
        "10 − 6 = 4 cm. Add all 8 sides: %s = <b>34 cm</b>." % plus(sZ), want=(34, "cm"))
    # staircase, only the two big sides labelled
    for (w, h, steps, u) in [(D("7.5"), D("4.5"), 3, "m"), (D(12), D(9), 4, "cm")]:
        # outline: bottom-left (0, steps), up the left side, then down the stairs to the right
        units = [(0, steps), (0, 0), (1, 0)]
        for i in range(1, steps):
            units += [(i, i), (i + 1, i)]
        units += [(steps, steps)]
        kx, ky = 200 / steps, (200 / steps) * float(h / w)
        pts = [(x * kx, y * ky) for x, y in units]
        m = len(units)
        lab = [""] * m
        lab[0] = L(h, u)                # left side
        lab[m - 1] = L(w, u)            # bottom
        p = 2 * (w + h)
        assert sum(ortho_sides(units)) == 4 * steps
        add(fig(polygon_svg(pts, lab, "staircase figure with two side lengths")) +
            "All the corners are square corners. What is the perimeter of this staircase shape?", L(p, u),
            lens([w + h, w + 2 * h, w * h, p + 2 * h], u),
            "The steps that go across add up to %s %s, and the steps that go down add up to %s %s. So the perimeter "
            "is the same as a %s %s by %s %s rectangle: 2 × (%s + %s) = <b>%s %s</b>."
            % (n(w), u, n(h), u, n(w), u, n(h), u, n(w), n(h), n(p), u), want=(p, u))
    # plus shape
    P_ = [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1), (1, 1)]
    pp = ortho_pts(P_, 140, 140)
    labp = ["2.5 cm"] + [""] * 11
    assert len(ortho_sides(P_)) == 12
    add(fig(polygon_svg(pp, labp, "plus-shaped figure with 12 equal sides", ticks=True)) +
        "All 12 sides of this plus shape are 2.5 cm long. What is its perimeter?", "30 cm",
        lens([10, D("27.5"), 25, D("31.25")], "cm"),
        "12 sides × 2.5 cm = <b>30 cm</b>. 10 cm uses only 4 sides. Count the sides carefully: 3 on each arm, "
        "4 arms.", want=(30, "cm"))
    # house shapes (rectangle + triangle roof), the dashed line is inside
    for base, wall, roof, u, eq in [(8, 5, 8, "cm", True), (9, D("4.5"), D("6.5"), "m", False)]:
        base, wall, roof = D(base), D(wall), D(roof)
        pts, th = house_pts(base, wall, roof)
        dashed = [((0, th * 14), (float(base) * 14, th * 14))]
        lab = [L(roof, u), L(wall, u), L(base, u), L(wall, u), L(roof, u)]
        p = base + 2 * wall + 2 * roof
        rect_p = 2 * (base + wall)
        tri_p = base + 2 * roof
        add(fig(polygon_svg(pts, lab, "rectangle with a triangle on top", dashed=dashed)) +
            "A rectangle and a triangle are put together. What is the perimeter of the whole shape?",
            L(p, u), lens([p + base, rect_p + tri_p, rect_p, p - wall], u),
            "Go around the outside only: %s = <b>%s %s</b>. The dashed line is inside the shape, so it is not part of "
            "the perimeter. Adding the two perimeters (%s + %s = %s) counts the inside line twice."
            % (plus([roof, wall, base, wall, roof]), n(p), u, n(rect_p), n(tri_p), n(rect_p + tri_p)), want=(p, u))
    # rectangle with a corner cut off
    for units, u, full in [([(0, 0), (9, 0), (12, 4), (12, 8), (0, 8)], "cm", (12, 8)),
                           ([(0, 0), (16, 0), (16, 9), (4, 9), (0, 6)], "m", (16, 9))]:
        m = len(units)
        sides = []
        for i in range(m):
            (x1, y1), (x2, y2) = units[i], units[(i + 1) % m]
            v = math.hypot(x2 - x1, y2 - y1)
            assert v == int(v)
            sides.append(D(int(v)))
        p = sum(sides)
        fp = 2 * (full[0] + full[1])
        slant = [v for i, v in enumerate(sides) if units[i][0] != units[(i + 1) % m][0] and units[i][1] != units[(i + 1) % m][1]][0]
        add(fig(polygon_svg(ortho_pts(units), [L(v, u) for v in sides], "rectangle with one corner cut off")) +
            "A corner was cut off a rectangle. What is the perimeter of the new shape?", L(p, u),
            lens([fp, p - slant, full[0] * full[1], p - min(sides)], u),
            "Add the 5 sides, including the slanted one: %s = <b>%s %s</b>. %d %s is the perimeter of the whole "
            "rectangle before the corner was cut." % (plus(sides), n(p), u, fp, u), want=(p, u))
    # square joined to a rectangle (dashed shared side)
    J = [(0, 0), (6, 0), (6, 2), (16, 2), (16, 6), (0, 6)]
    sJ = ortho_sides(J)
    pJ = sum(sJ)
    assert sJ == [6, 2, 10, 4, 16, 6] and pJ == 44
    pts = ortho_pts(J)
    k = pts[1][0] / 6
    labJ = ["6 cm", "?", "10 cm", "4 cm", "?", "6 cm"]
    add(fig(polygon_svg(pts, labJ, "square joined to a rectangle", dashed=[((6 * k, 2 * k), (6 * k, 6 * k))])) +
        "A 6 cm square and a 10 cm by 4 cm rectangle are put together. What is the perimeter of the new shape?",
        "44 cm", lens([52, 48, 28, 34], "cm"),
        "Missing sides: 6 − 4 = 2 cm and 6 + 10 = 16 cm. Add the outside: 6 + 2 + 10 + 4 + 16 + 6 = <b>44 cm</b>. "
        "Adding the two perimeters (24 + 28 = 52) counts the 4 cm dashed side twice, and it is inside the shape.",
        want=(44, "cm"))
    add("Two rectangles, each 8 cm by 3 cm, are put end to end so their 3 cm sides touch. They make one long "
        "rectangle. What is its perimeter?", "38 cm", ["44 cm", "41 cm", "22 cm"],
        "The new rectangle is 8 + 8 = 16 cm long and 3 cm wide: 2 × (16 + 3) = <b>38 cm</b>. "
        "44 cm adds the two perimeters (22 + 22) and counts the two 3 cm sides that are now inside.",
        want=(38, "cm"))
    add("Five squares with 4 cm sides are put in a row, side by side. What is the perimeter of the row?",
        "48 cm", ["80 cm", "40 cm", "56 cm"],
        "The row is 5 × 4 = 20 cm long and 4 cm tall: 2 × (20 + 4) = <b>48 cm</b>. "
        "80 cm (5 × 16) counts the sides where the squares touch, which are inside.", want=(48, "cm"))
    add(fig(hex_row_svg(3, "5 cm")) +
        "Three regular hexagons with 5 cm sides are joined in a row like this. What is the perimeter of the whole shape?",
        "70 cm", ["90 cm", "80 cm", "60 cm"],
        "3 hexagons have 3 × 6 = 18 sides. Each place where two hexagons touch hides 2 sides (one from each), "
        "and there are 2 places: 18 − 4 = 14 sides on the outside. 14 × 5 = <b>70 cm</b>. "
        "90 cm counts every side, even the inside ones.", want=(70, "cm"))
    add("Ethan puts two equilateral triangles with 6 cm sides together along one side. They make a 4-sided shape. "
        "What is its perimeter?", "24 cm", ["36 cm", "30 cm", "18 cm"],
        "The new shape has 4 outside sides of 6 cm: 4 × 6 = <b>24 cm</b>. 36 cm adds both triangles "
        "(18 + 18) and counts the shared side twice.", want=(24, "cm"))
    # arrow (rectangle shaft + triangle head), two short sides missing
    A = [(0, 2), (10, 2), (10, 0), (13, 4), (10, 8), (10, 6), (0, 6)]
    k = 230 / 13
    pts = [(x * k, y * k) for x, y in A]
    sA = [D(10), D(2), D(5), D(5), D(2), D(10), D(4)]
    pA = sum(sA)
    assert pA == 38 and math.hypot(3, 4) == 5
    labA = ["10 cm", "?", "5 cm", "5 cm", "?", "10 cm", "4 cm"]
    add(fig(polygon_svg(pts, labA, "arrow shape with two missing sides")) +
        "This arrow is 8 cm across at its widest point. The two ? sides are the same length. "
        "What is the perimeter of the arrow?", "38 cm", lens([34, 42, 36], "cm"),
        "The arrowhead is 8 cm across and the shaft is 4 cm across, so the two ? sides share 8 − 4 = 4 cm: "
        "2 cm each. Add all 7 sides: 10 + 2 + 5 + 5 + 2 + 10 + 4 = <b>38 cm</b>. "
        "34 cm leaves out the two short sides, and 42 cm uses 4 cm for each one.", want=(38, "cm"))
    # same perimeter: rectangle vs L shape (picture choices keep their order)
    Ra = [(0, 0), (8, 0), (8, 5), (0, 5)]
    Lb = [(0, 0), (8, 0), (8, 2), (4, 2), (4, 5), (0, 5)]
    assert sum(ortho_sides(Ra)) == sum(ortho_sides(Lb)) == 26
    ka = 22
    pa = [(x * ka, y * ka) for x, y in Ra]
    pb = [(x * ka, y * ka) for x, y in Lb]
    its.append(fixed(fig(pair_svg((pa, ["8 cm", "5 cm", "", ""]), (pb, ["8 cm", "2 cm", "4 cm", "3 cm", "4 cm", "5 cm"]),
                                  "rectangle A and L-shaped figure B")) +
                     "Which shape has the <b>longer perimeter</b>?",
                     ["A", "B", "They are the same", "You can’t tell"], 2,
                     "A: 2 × (8 + 5) = 26 cm. B: 8 + 2 + 4 + 3 + 4 + 5 = 26 cm. <b>They are the same.</b> "
                     "Cutting a corner out of a rectangle moves two sides inward, but their lengths stay the same."))
    add("Two regular hexagons with 4 cm sides are joined along one side. What is the perimeter of the new shape?",
        "40 cm", ["48 cm", "44 cm", "24 cm"],
        "2 hexagons have 12 sides. The joined side is inside, and it hides one side from each hexagon: "
        "12 − 2 = 10 outside sides. 10 × 4 = <b>40 cm</b>. 44 cm takes away only one of the two hidden sides.",
        want=(40, "cm"))
    order = [7, 0, 3, 10, 11, 8, 9, 13, 14, 16, 19, 15, 12, 1, 4, 5, 6, 18, 17, 2]
    assert sorted(order) == list(range(20)), (len(its))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Composite shapes", "items": its}


# ============================================================ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, want=want))

    add("Simran’s family puts a fence around a rectangular vegetable garden in Kelowna. The garden is 14.5 m long "
        "and 9 m wide. How much fence do they need?", "47 m", ["23.5 m", "130.5 m", "38 m"],
        "2 × 14.5 + 2 × 9 = 29 + 18 = <b>47 m</b>. 23.5 m is only two sides, and 130.5 is the area.", want=(47, "m"))
    add("Harjot builds a dog run 15 m long and 8 m wide. It has a gate 1.5 m wide, and the gate is not part of "
        "the fence. How much fence does he need?", "44.5 m", ["46 m", "47.5 m", "21.5 m"],
        "Perimeter: 2 × 15 + 2 × 8 = 46 m. Take away the gate: 46 − 1.5 = <b>44.5 m</b>. "
        "47.5 m adds the gate instead of taking it away.", want=(D("44.5"), "m"))
    add("A chicken run is built against a barn. The 12 m side runs along the barn wall, so it needs no fence. "
        "The run is 6.5 m wide. How much fence is needed for the other 3 sides?", "25 m", ["37 m", "30.5 m", "18.5 m"],
        "Fence goes on one 12 m side and two 6.5 m sides: 12 + 6.5 + 6.5 = <b>25 m</b>. "
        "37 m puts fence along the barn wall too, and 30.5 m uses the wrong side as the wall.", want=(25, "m"))
    add("A rectangular field is 30 m long and 18 m wide. Fence posts go all the way around it, 2 m apart, with a post "
        "at every corner. How many posts are needed?", "48", ["49", "96", "24"],
        "Perimeter: 2 × (30 + 18) = 96 m. One post every 2 m: 96 ÷ 2 = <b>48 posts</b>. "
        "The fence is a closed loop, so the last post is also the first one. 49 would be right for a straight fence.")
    add("Fencing costs $12 per metre. Mateo’s garden is a rectangle 10 m long and 6.5 m wide. How much will it cost "
        "to fence all the way around?", "$396", ["$198", "$780", "$33"],
        "Perimeter: 2 × (10 + 6.5) = 33 m. Cost: 33 × $12 = <b>$396</b>. $198 fences only two sides, "
        "and $780 uses the area (65) instead of the perimeter.")
    add("For the Terry Fox Run, students run laps of a path around the school field. The field is 110 m long and "
        "65 m wide. How many laps make 3.5 km?", "10", ["20", "35", "5"],
        "One lap: 2 × (110 + 65) = 350 m. 3.5 km = 3500 m. 3500 ÷ 350 = <b>10 laps</b>. "
        "20 laps would be right only if one lap were 110 + 65 = 175 m.")
    add("A loop hiking trail near Squamish has 4 parts: 1.2 km, 850 m, 1.5 km and 950 m. How long is the whole loop?",
        "4.5 km", ["3.55 km", "2.7 km", "45 km"],
        "Change to one unit: 850 m = 0.85 km and 950 m = 0.95 km. 1.2 + 0.85 + 1.5 + 0.95 = <b>4.5 km</b>. "
        "2.7 km adds only the parts in kilometres, and 3.55 km leaves out the 950 m part.", want=(D("4.5"), "km"))
    add("A trail around a pond near Kamloops is shaped like a triangle. Its sides are 0.8 km, 1.25 km and 950 m. "
        "How long is the trail?", "3 km", ["2.05 km", "2.145 km", "952.05 km"],
        "950 m = 0.95 km. 0.8 + 1.25 + 0.95 = <b>3 km</b>. 2.05 km leaves out a side, 2.145 km changes 950 m to 0.095 km "
        "by mistake, and 952.05 adds 950 as if it were kilometres.", want=(3, "km"))
    add("A loop trail on Vancouver Island has 5 parts and is 6.4 km long. Four of the parts are 1.5 km, 1.2 km, "
        "0.9 km and 1.6 km. How long is the fifth part?", "1.2 km", ["11.6 km", "2.8 km", "5.2 km"],
        "Add the parts you know: 1.5 + 1.2 + 0.9 + 1.6 = 5.2 km. Subtract: 6.4 − 5.2 = <b>1.2 km</b>. "
        "2.8 km leaves out the 1.6 km part.", want=(D("1.2"), "km"))
    add("Owen uses 52 m of fence to go around a rectangular sheep pen. The pen is 15.5 m long. How wide is it?",
        "10.5 m", ["21 m", "36.5 m", "13 m"],
        "Two lengths: 2 × 15.5 = 31 m. 52 − 31 = 21 m for the two widths. 21 ÷ 2 = <b>10.5 m</b>. "
        "21 m forgets to halve.", want=(D("10.5"), "m"))
    add("A community garden in Surrey is a rectangle. It is twice as long as it is wide, and its perimeter is 84 m. "
        "How long is it?", "28 m", ["42 m", "21 m", "14 m"],
        "Width + length = 84 ÷ 2 = 42 m. The length is 2 widths, so 3 widths = 42 m and one width = 14 m. "
        "Length = 2 × 14 = <b>28 m</b>. Check: 2 × (28 + 14) = 84.", want=(28, "m"))
    add("Ms. Grewal’s bulletin board is 1.8 m long and 1.2 m wide. She has a 5 m roll of paper border. Is it enough "
        "to go all the way around?", "No, she needs 6 m.",
        ["Yes, she needs 3 m.", "Yes, she needs 4.8 m.", "Yes, she needs 2.16 m."],
        "Perimeter: 2 × (1.8 + 1.2) = 6 m. 5 &lt; 6, so <b>it is not enough</b>. 3 m is only one length and "
        "one width, and 2.16 is the area.")
    add("A gazebo in a Victoria park has a floor shaped like a regular hexagon with 2.4 m sides. A railing goes on "
        "every side except one, which is the entrance. How long is the railing?", "12 m",
        ["14.4 m", "9.6 m", "7.4 m"],
        "A hexagon has 6 sides. The railing is on 5 of them: 5 × 2.4 = <b>12 m</b>. "
        "14.4 m forgets the entrance.", want=(12, "m"))
    add("Ava jogs 4 times around a soccer field that is 100 m long and 64 m wide. How far does she jog, in kilometres?",
        "1.312 km", ["0.656 km", "0.328 km", "13.12 km"],
        "One lap: 2 × (100 + 64) = 328 m. 4 laps: 4 × 328 = 1312 m = <b>1.312 km</b>. "
        "0.656 km uses only 100 + 64 for each lap.", want=(D("1.312"), "km"))
    add("A hockey rink is about 61 m long and 26 m wide. About how long are the boards all the way around it?",
        "174 m", ["87 m", "148 m", "1586 m"],
        "2 × 61 + 2 × 26 = 122 + 52 = <b>174 m</b>. 87 m is one length and one width, and 1586 is the area.",
        want=(174, "m"))
    assert 4 * 9 == 36 and 2 * (12 + D("5.5")) == 35
    add("Garden A is a square with 9 m sides. Garden B is a rectangle 12 m by 5.5 m. Which garden needs more fence?",
        "A, by 1 m", ["B, by 1 m", "They need the same.", "A, by 15 m"],
        "A: 4 × 9 = 36 m. B: 2 × (12 + 5.5) = 35 m. 36 − 35 = 1, so <b>A needs 1 m more</b>. "
        "15 compares the areas (81 and 66), not the fences.")
    add("Lucas walks 3 times around a city block in Vancouver. The block is 185 m long and 95 m wide. "
        "How far does he walk, in kilometres?", "1.68 km", ["0.84 km", "0.56 km", "16.8 km"],
        "One time around: 2 × (185 + 95) = 560 m. 3 times: 3 × 560 = 1680 m = <b>1.68 km</b>. "
        "0.84 km uses only 185 + 95 for each lap.", want=(D("1.68"), "km"))
    # L-shaped yard with a figure
    Y = [(0, 0), (18, 0), (18, 7), (11, 7), (11, 15), (0, 15)]
    sY = ortho_sides(Y)
    pY = sum(sY)
    assert sY == [18, 7, 7, 8, 11, 15] and pY == 66
    labY = ["18 m", "7 m", "?", "?", "11 m", "15 m"]
    add(fig(polygon_svg(ortho_pts(Y), labY, "L-shaped backyard with missing sides")) +
        "Mei’s backyard in Burnaby is L-shaped. All the corners are square corners. How much fence goes all the way "
        "around it?", "66 m", lens([51, 59, 58, 76], "m"),
        "Missing sides: 18 − 11 = 7 m and 15 − 7 = 8 m. Add all 6 sides: 18 + 7 + 7 + 8 + 11 + 15 = <b>66 m</b>. "
        "Shortcut: 2 × (18 + 15) = 66. 51 m adds only the sides with numbers.", want=(66, "m"))
    add("Chloe frames a square painting with ribbon. Each side of the painting is 32.5 cm. How much ribbon goes all "
        "the way around, in metres?", "1.3 m", ["0.65 m", "13 m", "130 m"],
        "4 × 32.5 = 130 cm. 100 cm = 1 m, so 130 cm = <b>1.3 m</b>. 130 m forgets to change centimetres to metres.",
        want=(D("1.3"), "m"))
    add("A farm in the Fraser Valley is a rectangle 1.25 km long and 800 m wide. How many metres of fence go all the way "
        "around it?", "4100 m", ["2050 m", "1602.5 m", "3300 m"],
        "Change first: 1.25 km = 1250 m. 2 × (1250 + 800) = 2 × 2050 = <b>4100 m</b>. "
        "1602.5 comes from 2 × 1.25 + 2 × 800, which mixes kilometres and metres. 3300 m leaves out one width.", want=(4100, "m"))
    order = [0, 1, 2, 9, 3, 17, 4, 6, 12, 7, 18, 13, 5, 14, 11, 15, 16, 8, 10, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Word problems: fencing and trails", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


LESSON_L = [(0, 0), (12, 0), (12, 4), (7, 4), (7, 9), (0, 9)]


def body_html():
    sl = ortho_sides(LESSON_L)
    assert sl == [12, 4, 5, 5, 7, 9] and sum(sl) == 42
    lab = ["12 m", "4 m", "?", "?", "7 m", "9 m"]
    hp, th = house_pts(8, 5, 8)
    return (
        "<h2>What is perimeter?</h2>"
        "<p>Perimeter is the <b>distance all the way around</b> a shape. To find it, add every outside side. "
        "Perimeter is a length, so it uses mm, cm, m or km.</p>"
        "<p>Shortcuts: a rectangle has 2 lengths and 2 widths, so P = 2 × (<i>l</i> + <i>w</i>). "
        "A regular polygon has equal sides, so P = side length × number of sides.</p>"
        "<figure class='sn-fig'>" + reg_svg(6, "2.5 cm") +
        "<figcaption>A regular hexagon has 6 sides of 2.5 cm: 6 × 2.5 = 15 cm.</figcaption></figure>"
        "<h2>L and T shapes: find the missing sides first</h2>"
        "<p>When all the corners are square, the sides going right add up to the sides going left, and the sides "
        "going down add up to the sides going up. Use this to find each missing side. Then add <b>every</b> side.</p>"
        "<figure class='sn-fig'>" + polygon_svg(ortho_pts(LESSON_L), lab, "L-shaped figure with two missing sides") +
        "<figcaption>Missing sides: 12 − 7 = 5 m and 9 − 4 = 5 m. "
        "Perimeter: 12 + 4 + 5 + 5 + 7 + 9 = 42 m.</figcaption></figure>" +
        ex("Example 1: check with the shortcut",
           "Find the perimeter of the L shape above another way.",
           "An L shape has the same perimeter as the rectangle around it: 2 × (12 + 9) = 2 × 21 = 42.",
           "42 m, the same answer") +
        "<h2>Composite shapes: only the outside counts</h2>"
        "<p>When shapes are put together, the side where they touch is inside. It is not part of the perimeter.</p>"
        "<figure class='sn-fig'>" + polygon_svg(hp, ["8 cm", "5 cm", "8 cm", "5 cm", "8 cm"],
                                                "rectangle with a triangle on top",
                                                dashed=[((0, th * 14), (8 * 14, th * 14))]) +
        "<figcaption>Go around the outside: 8 + 5 + 8 + 5 + 8 = 34 cm. The dashed line is inside, so leave it out."
        "</figcaption></figure>" +
        ex("Example 2: fencing with a gate",
           "A dog run is 15 m long and 8 m wide. The 1.5 m gate is not fence. How much fence is needed?",
           "Perimeter: 2 × (15 + 8) = 46 m. Take away the gate: 46 − 1.5 = 44.5.", "44.5 m") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Missing a side, often a short one on an L or T shape",
             "Count the sides first, then check that you added that many numbers"],
            ["Using the wrong length for a missing side (the whole side instead of the part)",
             "Find the parallel sides. Whole side − known part = missing part"],
            ["Adding only the numbers shown", "Find the missing sides first, then add every side"],
            ["Counting a side where two shapes touch", "That side is inside. Only the outside counts"],
            ["Adding 3 m + 45 cm as 48", "Change to one unit first: 300 cm + 45 cm"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about perimeter in BC?",
     "a": "In the Geometry and measurement area of the BC Grade 6 math curriculum, students find the perimeter of "
          "complex shapes, such as L and T shapes, regular polygons and shapes made of rectangles and triangles."},
    {"q": "How do you find the perimeter of an L-shaped figure?",
     "a": "Find each missing side by subtracting the known part from the whole side across from it, then add all "
          "6 sides. As a check, an L shape has the same perimeter as the rectangle around it."},
    {"q": "How do you find the perimeter of a regular polygon?",
     "a": "Multiply the side length by the number of sides. A regular hexagon with 2.5 cm sides has a perimeter "
          "of 6 × 2.5 = 15 cm."},
    {"q": "What is the most common mistake with complex shapes?",
     "a": "Missing a short side or using the whole side for a missing part. Count the sides first, find every "
          "missing length, and then add them all."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (shapes with many side labels)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(56810)
    sets = [set_rect(), set_lt(rnd), set_regular(), set_composite(), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [parse(x) for x in it["c"]]
            vals = [v for v in vals if v is not None]
            assert len(vals) == len(set(vals)), it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["q"][:400] + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "perimeter-of-complex-shapes", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Perimeter of Complex Shapes",
        "seo_title": "Grade 6 Perimeter of Complex Shapes Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Perimeter of complex shapes",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 6: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Perimeter of complex shapes",
        "meta_desc": "Free Grade 6 math worksheets on the perimeter of complex shapes for the BC curriculum: review "
                     "rectangles, find missing sides on L and T shapes, multiply for regular polygons, add only the "
                     "outside of composite shapes, and solve fencing and trail word problems. 100 questions with an "
                     "answer key.",
        "key_big": "Find every missing side first, then add all the sides around the outside.",
        "key_sub": "Whole side − known part = missing part. Rectangle: 2 × (l + w). Regular polygon: side × number "
                   "of sides. A side where two shapes touch is inside, so leave it out.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*(L-shaped|T-shaped|U-shaped|H-shaped|step-shaped|staircase|joined|arrow|"
                         "rectangle A and|hexagons in a row)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
