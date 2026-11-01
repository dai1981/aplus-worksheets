# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Partition Shapes into Equal Parts (3.G.A.2)
  python tools/gen_us_math_g3_partition_shapes.py
Every picture is computed from exact coordinates. The area of every part is checked in code:
"equal" pictures have parts of exactly the same area, "not equal" pictures have a biggest part
at least 1.4 times the smallest, so the difference can be seen.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
THIN = "#a8a8a8"      # unit-square lines on a grid
NAMES = ["Maya", "Leo", "Ava", "Noah", "Mia", "Eli", "Zoe", "Sam", "Lily", "Ben", "Emma", "Omar", "Kai", "Nora", "Ruby", "Jack"]
WORD = {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths", 8: "eighths"}
ONE = {1: "one whole", 2: "one half", 3: "one third", 4: "one fourth", 5: "one fifth", 6: "one sixth",
       7: "one seventh", 8: "one eighth", 9: "one ninth"}
SQ3 = math.sqrt(3)


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order (A, B, C, D or a fixed list of statements)."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def parts(n):
    return "1 part" if n == 1 else "%d parts" % n


def squ(n):
    return "1 square" if n == 1 else "%d squares" % n


# ------------------------------------------------------------ shapes made of exact pieces
# A shape is a dict: kind, w, h, pieces [{"d": path, "area": float}], lines (cut lines a child might count).
def poly(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    d = "M" + " L".join("%.1f %.1f" % p for p in pts) + " Z"
    return {"d": d, "area": abs(a) / 2}


def shape(kind, w, h, pieces, lines):
    return {"kind": kind, "w": w, "h": h, "pieces": pieces, "lines": lines, "n": len(pieces)}


def r_vstrips(fracs, w=160, h=96, kind="rectangle"):
    assert abs(sum(fracs) - 1) < 1e-9
    ps, x = [], 0.0
    for f in fracs:
        ps.append(poly([(x, 0), (x + f * w, 0), (x + f * w, h), (x, h)]))
        x += f * w
    return shape(kind, w, h, ps, len(fracs) - 1)


def r_hstrips(fracs, w=160, h=96, kind="rectangle"):
    ps, y = [], 0.0
    for f in fracs:
        ps.append(poly([(0, y), (w, y), (w, y + f * h), (0, y + f * h)]))
        y += f * h
    return shape(kind, w, h, ps, len(fracs) - 1)


def r_grid(rows, cols, w=160, h=96, kind="rectangle"):
    ps = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = w * c / cols, h * r / rows
            ps.append(poly([(x0, y0), (x0 + w / cols, y0), (x0 + w / cols, y0 + h / rows), (x0, y0 + h / rows)]))
    return shape(kind, w, h, ps, rows - 1 + cols - 1)


def r_diag1(w=160, h=96, kind="rectangle"):
    return shape(kind, w, h, [poly([(0, 0), (w, 0), (w, h)]), poly([(0, 0), (w, h), (0, h)])], 1)


def r_x(w=160, h=96, kind="rectangle"):
    c = (w / 2, h / 2)
    return shape(kind, w, h, [poly([(0, 0), (w, 0), c]), poly([(w, 0), (w, h), c]),
                              poly([(w, h), (0, h), c]), poly([(0, h), (0, 0), c])], 2)


def r_cross(fx, fy, w=160, h=96, kind="rectangle"):
    X, Y = fx * w, fy * h
    return shape(kind, w, h, [poly([(0, 0), (X, 0), (X, Y), (0, Y)]), poly([(X, 0), (w, 0), (w, Y), (X, Y)]),
                              poly([(0, Y), (X, Y), (X, h), (0, h)]), poly([(X, Y), (w, Y), (w, h), (X, h)])], 2)


def r_corner(t, w=160, h=96, kind="rectangle"):
    """Cut from the top-left corner to a point on the bottom side: a triangle and a 4-sided piece."""
    return shape(kind, w, h, [poly([(0, 0), (t * w, h), (0, h)]), poly([(0, 0), (w, 0), (w, h), (t * w, h)])], 1)


def sq(fn, *a, s=104):
    return fn(*a, w=s, h=s, kind="square")


def c_sectors(angles, r=60):
    assert abs(sum(angles) - 360) < 1e-9
    ps, a0 = [], 0.0
    for a in angles:
        a1 = a0 + a
        t0, t1 = math.radians(a0 - 90), math.radians(a1 - 90)
        x0, y0 = r + r * math.cos(t0), r + r * math.sin(t0)
        x1, y1 = r + r * math.cos(t1), r + r * math.sin(t1)
        d = "M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" % (r, r, x0, y0, r, r, 1 if a > 180 else 0, x1, y1)
        ps.append({"d": d, "area": math.pi * r * r * a / 360.0})
        a0 = a1
    n = len(angles)
    eq = max(angles) - min(angles) < 1e-9
    return shape("circle", 2 * r, 2 * r, ps, n // 2 if eq and n % 2 == 0 else n)


def c_chord(off, r=60):
    """Straight cut that misses the center by off*r: a big piece (left) and a small piece (right)."""
    d = off * r
    k = math.sqrt(r * r - d * d)
    x = r + d
    seg = r * r * math.acos(d / r) - d * k
    big = "M%.1f %.1f A%d %d 0 1 0 %.1f %.1f Z" % (x, r - k, r, r, x, r + k)
    small = "M%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z" % (x, r - k, r, r, x, r + k)
    return shape("circle", 2 * r, 2 * r, [{"d": big, "area": math.pi * r * r - seg}, {"d": small, "area": seg}], 1)


def hex_v(r=58):
    """Pointy-top regular hexagon. v0 top, then clockwise. Returns vertices and center."""
    cx, cy = r * SQ3 / 2, r
    return [(cx + r * math.cos(math.radians(-90 + 60 * i)), cy + r * math.sin(math.radians(-90 + 60 * i)))
            for i in range(6)], (cx, cy)


def hexagon(cut, r=58):
    v, c = hex_v(r)
    w, h = r * SQ3, 2 * r
    if cut == "six":
        return shape("hexagon", w, h, [poly([c, v[i], v[(i + 1) % 6]]) for i in range(6)], 3)
    if cut == "thirds":
        return shape("hexagon", w, h, [poly([c, v[i], v[i + 1], v[(i + 2) % 6]]) for i in (0, 2, 4)], 3)
    if cut == "half_v":
        return shape("hexagon", w, h, [poly([v[0], v[1], v[2], v[3]]), poly([v[3], v[4], v[5], v[0]])], 1)
    if cut == "half_m":
        ml, mr = (0, c[1]), (w, c[1])
        return shape("hexagon", w, h, [poly([ml, v[5], v[0], v[1], mr]), poly([mr, v[2], v[3], v[4], ml])], 1)
    if cut == "cut02":
        return shape("hexagon", w, h, [poly([v[0], v[1], v[2]]), poly([v[2], v[3], v[4], v[5], v[0]])], 1)
    if cut == "thirds_bad":
        return shape("hexagon", w, h, [poly([c, v[0], v[1]]), poly([c, v[1], v[2], v[3]]),
                                       poly([c, v[3], v[4], v[5], v[0]])], 3)
    raise ValueError(cut)


def triangle(cut, s=132, fracs=None):
    H = s * SQ3 / 2
    A, B, C = (s / 2, 0), (0, H), (s, H)

    def mid(p, q):
        return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    if cut == "half":
        M = mid(B, C)
        return shape("triangle", s, H, [poly([A, B, M]), poly([A, M, C])], 1)
    if cut == "four":
        ab, bc, ca = mid(A, B), mid(B, C), mid(C, A)
        return shape("triangle", s, H, [poly([A, ab, ca]), poly([ab, B, bc]), poly([ca, bc, C]), poly([ab, bc, ca])], 3)
    if cut == "three":
        G = (s / 2, H * 2 / 3)
        return shape("triangle", s, H, [poly([A, B, G]), poly([B, C, G]), poly([C, A, G])], 3)
    if cut == "apex":
        xs, x = [0.0], 0.0
        for f in fracs:
            x += f * s
            xs.append(x)
        return shape("triangle", s, H, [poly([A, (xs[i], H), (xs[i + 1], H)]) for i in range(len(fracs))], len(fracs) - 1)
    raise ValueError(cut)


def is_equal(sh):
    a = [p["area"] for p in sh["pieces"]]
    return max(a) - min(a) < 1e-6 * max(a)


def check_unequal(sh):
    a = [p["area"] for p in sh["pieces"]]
    assert max(a) / min(a) >= 1.4, ("not visibly unequal", a)
    return sh


def check_equal(sh):
    assert is_equal(sh), [p["area"] for p in sh["pieces"]]
    return sh


def draw(sh, shaded=(), ox=0, oy=0):
    """SVG elements for a shape placed at (ox, oy)."""
    if sh["kind"] == "grid":
        return draw_grid(sh, shaded, ox, oy)
    s = []
    for i, p in enumerate(sh["pieces"]):
        s.append("<path transform='translate(%.1f %.1f)' d='%s' fill='%s' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (ox, oy, p["d"], FILL if i in shaded else "#fff", LINE))
    return "".join(s)


NOUN = {"rectangle": "rectangle", "square": "square", "circle": "circle", "hexagon": "hexagon",
        "triangle": "triangle", "grid": "rectangle"}


def one_svg(sh, shaded=(), label=None):
    pad = 6
    w, h = sh["w"] + 2 * pad, sh["h"] + 2 * pad
    lab = label or "%s split into %d parts%s" % (NOUN[sh["kind"]], sh["n"], ", 1 part shaded" if shaded else "")
    return svg_wrap(int(math.ceil(w)), int(math.ceil(h)), draw(sh, shaded, pad, pad), lab)


# ------------------------------------------------------------ rectangles on a grid
def g_map(rows, cell=26):
    """rows: list of strings, one letter per unit square = which part the square belongs to."""
    H, W = len(rows), len(rows[0])
    ids = sorted({ch for r in rows for ch in r})
    count = {k: sum(r.count(k) for r in rows) for k in ids}
    for k in ids:                                    # every part must be one connected piece
        cells = [(c, r) for r in range(H) for c in range(W) if rows[r][c] == k]
        seen, todo = {cells[0]}, [cells[0]]
        while todo:
            c, r = todo.pop()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (c + dc, r + dr)
                if q in cells and q not in seen:
                    seen.add(q)
                    todo.append(q)
        assert len(seen) == len(cells), ("part not connected", rows, k)
    pieces = [{"id": k, "area": float(count[k])} for k in ids]
    return {"kind": "grid", "rows": rows, "cols_n": W, "rows_n": H, "cell": cell, "w": W * cell, "h": H * cell,
            "pieces": pieces, "n": len(ids), "lines": None, "total": W * H, "sizes": [count[k] for k in ids]}


def draw_grid(sh, shaded, ox, oy):
    rows, cell, W, H = sh["rows"], sh["cell"], sh["cols_n"], sh["rows_n"]
    ids = [p["id"] for p in sh["pieces"]]
    sh_ids = {ids[i] for i in shaded}
    s = []
    for r in range(H):
        for c in range(W):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s'/>"
                     % (ox + c * cell, oy + r * cell, cell, cell, FILL if rows[r][c] in sh_ids else "#fff"))
    for c in range(1, W):                            # thin unit lines
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (ox + c * cell, oy, ox + c * cell, oy + H * cell, THIN))
    for r in range(1, H):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (ox, oy + r * cell, ox + W * cell, oy + r * cell, THIN))
    for r in range(H):                               # thick lines between parts
        for c in range(W):
            if c + 1 < W and rows[r][c] != rows[r][c + 1]:
                x = ox + (c + 1) * cell
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                         % (x, oy + r * cell, x, oy + (r + 1) * cell, LINE))
            if r + 1 < H and rows[r][c] != rows[r + 1][c]:
                y = oy + (r + 1) * cell
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                         % (ox + c * cell, y, ox + (c + 1) * cell, y, LINE))
    s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (ox, oy, W * cell, H * cell, LINE))
    return "".join(s)


def grid_svg(rows, shaded=(), cell=26):
    sh = g_map(rows, cell)
    return one_svg(sh, shaded, "rectangle on a grid split into %d parts" % sh["n"]), sh


# ------------------------------------------------------------ several shapes in one picture
def panel_svg(shapes, label, letters="ABCD", cols=2):
    """shapes: list of (shape, shaded). Each gets a letter at its top left."""
    n = len(shapes)
    cw = max(s["w"] for s, _ in shapes)
    ch = max(s["h"] for s, _ in shapes)
    LW, gap, pad = 24, 18, 6
    rws = (n + cols - 1) // cols
    W = pad + cols * (LW + cw) + (cols - 1) * gap + pad
    H = pad + rws * ch + (rws - 1) * gap + pad
    s = []
    for i, (sh, shaded) in enumerate(shapes):
        r, c = divmod(i, cols)
        x0 = pad + c * (LW + cw + gap)
        y0 = pad + r * (ch + gap)
        s.append("<text x='%.1f' y='%.1f' font-size='20' font-weight='800' fill='%s'>%s</text>"
                 % (x0, y0 + 17, LINE, letters[i]))
        s.append(draw(sh, shaded, x0 + LW + (cw - sh["w"]) / 2, y0 + (ch - sh["h"]) / 2))
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s), label)


# ------------------------------------------------------------ catalogs of exact pictures (size fits a panel)
P = 100   # panel size


def EQ(n, i):
    """i-th equal picture with n parts."""
    lib = {
        2: [lambda: r_vstrips([.5, .5], w=P, h=62), lambda: r_diag1(w=P, h=62), lambda: c_sectors([180, 180], r=P / 2),
            lambda: hexagon("half_v", r=P / 2 / SQ3 * 2 * 0.97), lambda: hexagon("half_m", r=P / 2 / SQ3 * 2 * 0.97),
            lambda: triangle("half", s=P)],
        3: [lambda: r_vstrips([1 / 3.0] * 3, w=P, h=62), lambda: c_sectors([120] * 3, r=P / 2),
            lambda: hexagon("thirds", r=P / SQ3 * 0.97), lambda: triangle("three", s=P),
            lambda: r_hstrips([1 / 3.0] * 3, w=P, h=62)],
        4: [lambda: r_grid(2, 2, w=P, h=62), lambda: c_sectors([90] * 4, r=P / 2), lambda: triangle("four", s=P),
            lambda: r_vstrips([.25] * 4, w=P, h=62), lambda: r_x(w=P, h=62)],
        6: [lambda: r_grid(2, 3, w=P, h=62), lambda: c_sectors([60] * 6, r=P / 2), lambda: hexagon("six", r=P / SQ3 * 0.97)],
        8: [lambda: r_grid(2, 4, w=P, h=62), lambda: c_sectors([45] * 8, r=P / 2)],
    }
    return check_equal(lib[n][i % len(lib[n])]())


def UNEQ(n, i):
    lib = {
        2: [lambda: c_chord(0.4, r=P / 2), lambda: hexagon("cut02", r=P / SQ3 * 0.97), lambda: triangle("apex", s=P, fracs=[.25, .75]),
            lambda: r_corner(.5, w=P, h=62), lambda: r_vstrips([.3, .7], w=P, h=62)],
        3: [lambda: r_vstrips([.2, .5, .3], w=P, h=62), lambda: c_sectors([170, 100, 90], r=P / 2),
            lambda: hexagon("thirds_bad", r=P / SQ3 * 0.97), lambda: triangle("apex", s=P, fracs=[.2, .3, .5])],
        4: [lambda: r_cross(.3, .35, w=P, h=62), lambda: r_vstrips([.15, .35, .2, .3], w=P, h=62),
            lambda: c_sectors([140, 50, 100, 70], r=P / 2), lambda: triangle("apex", s=P, fracs=[.15, .25, .3, .3])],
        6: [lambda: c_sectors([90, 30, 60, 45, 75, 60], r=P / 2), lambda: r_vstrips([.1, .2, .15, .25, .12, .18], w=P, h=62)],
        8: [lambda: c_sectors([60, 30, 45, 30, 60, 45, 30, 60], r=P / 2),
            lambda: r_vstrips([.08, .16, .1, .14, .09, .17, .11, .15], w=P, h=62)],
    }
    return check_unequal(lib[n][i % len(lib[n])]())


# grid partitions: (rows, equal?)
GRIDS = {
    "h8_eq": ["AAAA", "BBBB"], "h8_eq2": ["AABB", "AABB"], "h8_eq3": ["AAAB", "ABBB"], "h8_eq4": ["ABBB", "AAAB"],
    "h8_bad": ["AAAB", "AABB"], "h8_bad2": ["AAAA", "ABBB"], "h8_bad3": ["ABBB", "ABBB"],
    "f12_eq": ["AAAB", "CCBB", "CDDD"], "f12_eq2": ["AABB", "ACBD", "CCDD"], "f12_eq3": ["ABCD", "ABCD", "ABCD"],
    "f12_bad": ["ABBB", "ACCD", "ACCD"], "f12_bad2": ["AAAB", "AAAB", "CCDD"], "f12_bad3": ["AABB", "AABB", "CCCD"],
    "t12_eq": ["AAAA", "BBBB", "CCCC"], "t12_eq2": ["AABB", "AABB", "CCCC"], "t12_eq3": ["AAAB", "ACBB", "CCCB"],
    "t12_bad": ["AAAB", "AAAB", "CCCC"], "t12_bad2": ["AABB", "AABB", "AACC"], "t12_bad3": ["AAAA", "BBBB", "BCCC"],
    "t12w_eq": ["AABBCC", "AABBCC"], "t12w_eq2": ["AAAABB", "CCCCBB"], "t12w_bad": ["AAABBC", "AAABBC"],
    "s12_eq": ["AABB", "CCDD", "EEFF"], "s12_eq2": ["AABC", "DEBC", "DEFF"],
    "f16_eq": ["AABB", "AABB", "CCDD", "CCDD"], "f16_eq2": ["AAAB", "ACBB", "CCDB", "CDDD"],
    "f16_eq3": ["ABBB", "ABCC", "AACC", "DDDD"], "f16_bad": ["AABB", "AABB", "CCCD", "CCCD"],
    "f16_bad2": ["AAAB", "AAAB", "CCDD", "CCDD"],
    "f24_eq": ["AAABBB", "AAABBB", "CCCDDD", "CCCDDD"], "e24_eq": ["AAABBB", "CCCDDD", "EEEFFF", "GGGHHH"],
    "s24_eq": ["AABBCC", "AABBCC", "DDEEFF", "DDEEFF"], "t24_eq": ["AABBCC", "AABBCC", "AABBCC", "AABBCC"],
    "s18_eq": ["ABCDEF", "ABCDEF", "ABCDEF"], "t18_eq": ["AABBCC", "AABBCC", "AABBCC"],
    "t9_eq": ["AAB", "ABB", "CCC"], "e16_eq": ["ABCDEFGH", "ABCDEFGH"],
    "f20_eq": ["AAAAA", "BBBBB", "CCCCC", "DDDDD"], "f20_eq2": ["AAAAB", "CCABB", "CCDBB", "CDDDD"],
    "s30_eq": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF"],
}
for _k, _rows in GRIDS.items():
    _g = g_map(_rows)
    _eq = len(set(_g["sizes"])) == 1
    assert _eq == ("_eq" in _k), (_k, _g["sizes"])
    if not _eq:
        assert max(_g["sizes"]) / min(_g["sizes"]) >= 1.4, _k


def G(key, cell=26):
    return g_map(GRIDS[key], cell)


# ============================================================ set 1: equal parts or not?
class Spots:
    """Answer letters for picture questions: each of A-D used equally often, in a shuffled order."""
    def __init__(self, rnd):
        self.rnd, self.left = rnd, []

    def next(self):
        if not self.left:
            self.left = [0, 1, 2, 3]
            self.rnd.shuffle(self.left)
        return self.left.pop()


def count_choice(k):
    return "1 equal part" if k == 1 else "%d equal parts" % k


NOT_EQ = "Not equal parts"


def set_equal(rnd):
    its = []
    singles = [
        (r_grid(2, 4), True), (c_sectors([45] * 8), True), (hexagon("thirds"), True), (triangle("four"), True),
        (r_hstrips([1 / 3.0] * 3), True), (c_sectors([120] * 3), True),
        (r_vstrips([.15, .35, .2, .3]), False), (c_sectors([150, 60, 90, 60]), False), (hexagon("cut02"), False),
        (triangle("apex", fracs=[.2, .3, .5]), False), (r_cross(.3, .35), False), (c_chord(0.35), False),
    ]
    rnd.shuffle(singles)
    for sh, ok in singles:
        (check_equal if ok else check_unequal)(sh)
        n, L = sh["n"], sh["lines"]
        noun = NOUN[sh["kind"]]
        cands = [count_choice(n), count_choice(L), NOT_EQ, count_choice(n + 1), count_choice(n - 1)]
        if ok:
            e = ("Count the <b>parts</b>, not the cut lines: there are %d parts. They are all the same size, "
                 "so the %s is split into <b>%d equal parts</b> (%s)." % (n, noun, n, WORD[n]))
            right = count_choice(n)
        else:
            e = ("There are %d parts, but they are <b>not the same size</b>. %s, "
                 "so these are not equal parts." % (n, "One part is clearly bigger than the other" if n == 2
                                                    else "Some parts are clearly bigger than others"))
            right = NOT_EQ
        its.append(mcq(fig(one_svg(sh)) + "Is this %s split into equal parts? If yes, how many?" % noun,
                       right, cands, e, rnd))

    # which shape is (not) split into equal parts?  All four shapes have the same number of parts.
    plan = [(2, False), (3, False), (4, False), (6, False), (8, False), (3, True), (4, True), (2, True)]
    spots = Spots(rnd)
    for qi, (n, find_not) in enumerate(plan):
        pos = spots.next()
        if not find_not:
            good = EQ(n, qi)
            bad = [UNEQ(n, qi + j) for j in range(3)]
        else:
            good = UNEQ(n, qi)
            bad = [EQ(n, qi + j) for j in range(3)]
        rnd.shuffle(bad)
        shapes = bad[:pos] + [good] + bad[pos:]
        L = "ABCD"[pos]
        svg = panel_svg([(s, ()) for s in shapes], "four shapes A to D, each split into %d parts" % n)
        if not find_not:
            q = fig(svg) + "Each shape has %d parts. Which shape is split into <b>equal</b> parts?" % n
            e = ("All four shapes have %d parts, so counting is not enough. Only in shape <b>%s</b> are all the parts "
                 "the same size. That shape shows %s." % (n, L, WORD[n]))
        else:
            q = fig(svg) + "Which shape is <b>not</b> split into equal parts?"
            e = ("In shape <b>%s</b> some parts are bigger than others. The other three shapes have %d parts "
                 "that are all the same size." % (L, n))
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], pos, e))
    assert len(its) == 20
    return {"title": "Equal parts or not?", "items": its}


# ============================================================ set 2: name the unit fraction
def set_unit(rnd):
    its = []
    shaded_q = [(r_vstrips([.25] * 4), 0), (c_sectors([60] * 6), 2), (hexagon("thirds"), 1), (triangle("four"), 3),
                (r_grid(2, 4), 5), (c_sectors([120] * 3), 0), (sq(r_x), 1), (hexagon("six"), 4)]
    for sh, k in shaded_q:
        check_equal(sh)
        n = sh["n"]
        e = ("The %s has <b>%d equal parts</b> and 1 part is shaded, so the shaded part is %s. "
             "The bottom number is all the parts, not the parts that are left." % (NOUN[sh["kind"]], n, fr(1, n)))
        its.append(mcq(fig(one_svg(sh, (k,))) + "What fraction of the %s is shaded?" % NOUN[sh["kind"]],
                       fr(1, n), [fr(1, n - 1), fr(n - 1, n), fr(n, 1), fr(1, n + 1)], e, rnd))

    each_q = [r_grid(2, 3), c_sectors([45] * 8), triangle("three"), sq(r_grid, 2, 2), hexagon("half_m")]
    for sh in each_q:
        check_equal(sh)
        n, L = sh["n"], sh["lines"]
        e = "There are <b>%d equal parts</b>. Each part is 1 out of %d, so each part is %s of the whole." % (n, n, fr(1, n))
        if L != n and L > 1:
            e += " Count parts, not lines: there are %d cut lines but %d parts." % (L, n)
        its.append(mcq(fig(one_svg(sh)) + "The parts are equal. Each part is what fraction of the whole %s?" % NOUN[sh["kind"]],
                       fr(1, n), [fr(1, L) if L != n and L > 1 else None, fr(n, 1), fr(1, n - 1) if n > 2 else fr(1, 6),
                                  fr(1, n + 1)], e, rnd))

    word_q = [r_vstrips([1 / 6.0] * 6), c_sectors([90] * 4), triangle("half"), r_hstrips([.125] * 8, h=112)]
    for sh in word_q:
        check_equal(sh)
        n, L = sh["n"], sh["lines"]
        e = "%d equal parts are called <b>%s</b>. Each part is %s, which we say as <b>%s</b>." % (n, WORD[n], fr(1, n), ONE[n])
        its.append(mcq(fig(one_svg(sh)) + "The parts are equal. What do we call 1 part?", ONE[n],
                       [ONE[L] if L != n else None, ONE[n - 1], ONE[n + 1], ONE[n // 2] if n > 2 else None, ONE.get(2 * n)], e, rnd))

    its.append(mcq("A shape is split into 6 equal parts. What fraction of the shape is 1 part?", fr(1, 6),
                   [fr(6, 1), fr(1, 5), fr(5, 6)],
                   "6 equal parts, and you want 1 of them: %s. The bottom number tells how many equal parts make the whole." % fr(1, 6), rnd))
    its.append(mcq("Which fraction names 1 of 3 equal parts?", fr(1, 3), [fr(3, 1), fr(1, 2), fr(2, 3)],
                   "1 part out of 3 equal parts is %s. The 1 goes on top and the 3 equal parts go on the bottom. "
                   "(%s would be the other 2 parts.)" % (fr(1, 3), fr(2, 3)), rnd))
    its.append(mcq("A rectangle is cut into 8 equal pieces. What unit fraction names 1 piece?",
                   fr(1, 8), [fr(8, 1), fr(1, 7), fr(7, 8)],
                   "8 equal pieces make the whole, so 1 piece is %s." % fr(1, 8), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Name the unit fraction", "items": its}


# ============================================================ set 3: same area, different shape
SAME, A_BIG, B_BIG, CANT = "They are equal", "A is bigger", "B is bigger", "You can’t tell"


def pair_svg(a, sa, b, sb, label):
    return panel_svg([(a, sa), (b, sb)], label, letters="AB", cols=2)


def set_shape(rnd):
    its = []
    S = 92
    pairs = [
        (sq(r_x, s=S), (0,), sq(r_vstrips, [.25] * 4, s=S), (1,), SAME,
         "Both squares are split into 4 equal parts, so each shaded part is %s of the same square. "
         "A triangle and a strip can have the <b>same area</b>." % fr(1, 4)),
        (sq(r_diag1, s=S), (1,), sq(r_vstrips, [.5, .5], s=S), (0,), SAME,
         "Each square is cut into 2 equal parts. Half of a square is %s, whether the cut is straight or on the diagonal." % fr(1, 2)),
        (sq(r_grid, 2, 2, s=S), (3,), sq(r_x, s=S), (2,), SAME,
         "Each square is cut into 4 equal parts. The small square and the triangle are both %s of the same square." % fr(1, 4)),
        (hexagon("half_v", r=52), (0,), hexagon("half_m", r=52), (1,), SAME,
         "Both hexagons are cut into 2 equal parts. Each shaded part is %s of the same hexagon, so they are equal." % fr(1, 2)),
        (sq(r_x, s=S), (1,), sq(r_vstrips, [1 / 3.0] * 3, s=S), (0,), B_BIG,
         "A is cut into 4 equal parts, so its shaded part is %s. B is cut into 3 equal parts, so its shaded part is %s. "
         "Fewer parts means bigger parts, so B is bigger." % (fr(1, 4), fr(1, 3))),
        (triangle("half", s=S + 12), (0,), triangle("three", s=S + 12), (2,), A_BIG,
         "A is cut into 2 equal parts (%s). B is cut into 3 equal parts (%s). A half is bigger than a third, so A is bigger."
         % (fr(1, 2), fr(1, 3))),
    ]
    rnd.shuffle(pairs)
    for a, sa, b, sb, right, e in pairs:
        check_equal(a)
        check_equal(b)
        q = fig(pair_svg(a, sa, b, sb, "shapes A and B of the same size, each with 1 part shaded")) + \
            "Shapes A and B are the same size. Compare the shaded parts."
        its.append(mcq_fixed(q, [SAME, A_BIG, B_BIG, CANT], [SAME, A_BIG, B_BIG, CANT].index(right), e))

    # rectangle cut on both diagonals: the four triangles have 2 shapes but the same area
    sh = check_equal(r_x(w=168, h=90))
    its.append(mcq_fixed(fig(one_svg(sh, (0, 3), "rectangle cut along both diagonals, top and left triangles shaded")) +
                         "The rectangle is cut along both diagonals. Compare the 2 shaded triangles.",
                         ["The top one is bigger", "The left one is bigger", "Each is " + fr(1, 4), "You can’t tell"], 2,
                         "Draw a line across and a line down through the middle: you get 4 equal small rectangles. "
                         "Each triangle is made of 2 halves of small rectangles, which is as much as 1 small rectangle. So every triangle is %s of the rectangle. "
                         "The top one is wider but shorter." % fr(1, 4)))

    # are the parts on the grid equal?
    YES = "Yes, same area"
    grid_q = [("f12_eq", True), ("t12w_eq2", True), ("f16_eq3", True), ("t12_eq3", True), ("f12_bad", False), ("t12_bad3", False)]
    for key, ok in grid_q:
        g = G(key)
        n, k = g["n"], g["sizes"][0]
        if ok:
            right = "Yes, %s each" % squ(k)
            cands = ["No, not the same shape", "No, some are bigger", "Yes, all the same shape"]
            e = ("Count the squares in each part: every part has <b>%s</b>. The parts have different shapes, "
                 "but the same area, so they are equal parts. Each part is %s of the rectangle." % (squ(k), fr(1, n)))
        else:
            right = "No, some are bigger"
            sizes = sorted(g["sizes"], reverse=True)
            cands = ["Yes, %d parts" % n, "Yes, %s each" % squ(sizes[-1]), "Yes, all the same shape"]
            e = ("Count the squares in each part: %s. The parts do not have the same area, so they are "
                 "<b>not</b> equal parts." % (", ".join(str(v) for v in sizes[:-1]) + " and " + str(sizes[-1])))
        q = fig(one_svg(g, (), "rectangle on a grid split into %d parts" % n)) + "Are these %d parts equal?" % n
        its.append(mcq(q, right, cands, e, rnd))

    # which grid shows fourths / thirds / halves?  The right one has parts of different shapes.
    plan = [(4, "f12_eq", ["f12_bad", "f12_bad2", "f12_bad3"]), (3, "t12_eq3", ["t12_bad", "t12_bad2", "t12_bad3"]),
            (2, "h8_eq3", ["h8_bad", "h8_bad2", "h8_bad3"]), (4, "f16_eq2", ["f16_bad", "f16_bad2", "f12_bad"])]
    spots = Spots(rnd)
    for n, good, bads in plan:
        pos = spots.next()
        bads = bads[:]
        rnd.shuffle(bads)
        keys = bads[:pos] + [good] + bads[pos:]
        shapes = [(G(k, cell=22), ()) for k in keys]
        g = G(good)
        svg = panel_svg(shapes, "four rectangles on grids, each split into %d parts" % n)
        e = ("Count the squares in each part. In <b>%s</b> every part has %s, so the parts are equal, even though they "
             "are not simple strips. In the others, some parts have more squares than others." % ("ABCD"[pos], squ(g["sizes"][0])))
        its.append(mcq_fixed(fig(svg) + "Which rectangle is split into <b>%s</b>?" % WORD[n], ["A", "B", "C", "D"], pos, e))

    # stories
    its.append(mcq("Noah cuts a square sandwich in half on the diagonal. Lily cuts the same size sandwich in half "
                   "straight down the middle. Whose half is bigger?", "They are the same size",
                   ["Noah’s triangle", "Lily’s rectangle", "You can’t tell"],
                   "Both sandwiches are cut into 2 equal parts, so each half is %s of the same sandwich. "
                   "Different shape, same area." % fr(1, 2), rnd))
    its.append(mcq("Two gardens are the same size. Garden A is split into 4 equal square beds. Garden B is split into "
                   "4 equal long, thin beds. Which is bigger: one bed in A or one bed in B?", "They are the same size",
                   ["A bed in garden A", "A bed in garden B", "You can’t tell"],
                   "Each garden is split into 4 equal parts, so every bed is %s of a same-size garden. "
                   "Square or thin, the beds have the same area." % fr(1, 4), rnd))
    its.append(mcq("Eli cuts a rectangle into 3 parts: a triangle, a square and a strip. Each part covers 4 unit squares. "
                   "What fraction of the rectangle is each part?", fr(1, 3),
                   ["They are not equal", fr(1, 4), fr(1, 12)],
                   "The parts have different shapes, but each one has an area of 4 square units, so they are 3 equal parts. "
                   "Each part is %s. (The 4 is the size of a part, and 12 is the number of squares, not parts.)" % fr(1, 3), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Same area, different shape", "items": its}


# ============================================================ set 4: area of each part on a grid
def set_area(rnd):
    its = []
    area_q = [("f12_eq", 0), ("s24_eq", 4), ("t24_eq", 1), ("e24_eq", 6), ("t12w_eq2", 2), ("s18_eq", 3),
              ("f20_eq2", 1), ("f24_eq", 3)]
    for key, k in area_q:
        g = G(key, cell=22)
        n, T, a = g["n"], g["total"], g["sizes"][0]
        assert a != n
        q = (fig(one_svg(g, (k,), "rectangle of %d unit squares split into %d equal parts" % (T, n))) +
             "Each small square is 1 square unit. The rectangle is split into %d equal parts. "
             "What is the area of the shaded part?" % n)
        e = ("Count the squares in the shaded part: %d. Check: %d squares ÷ %d equal parts = %d. "
             "Each part is %d square units." % (a, T, n, a, a))
        its.append(mcq(q, "%d sq units" % a, ["%d sq units" % v for v in [n, T, T - n, a + 1]], e, rnd))

    both_q = [("t12_eq2", 2), ("s30_eq", 1), ("s12_eq2", 4), ("t18_eq", 0)]
    for key, k in both_q:
        g = G(key, cell=24)
        n, T, a = g["n"], g["total"], g["sizes"][0]
        right = "%d sq units, %s" % (a, fr(1, n))
        cands = ["%d sq units, %s" % (a, fr(1, a)), "%d sq units, %s" % (n, fr(1, n)), "%d sq units, %s" % (a, fr(1, T))]
        e = ("The shaded part covers <b>%d squares</b>, so its area is %d square units. The rectangle has %d equal parts, "
             "so the part is %s of the whole. The bottom number counts parts, not squares." % (a, a, n, fr(1, n)))
        its.append(mcq(fig(one_svg(g, (k,), "rectangle on a grid split into %d equal parts, 1 part shaded" % n)) +
                       "The parts are equal. What is the area of the shaded part, and what fraction of the whole is it?",
                       right, cands, e, rnd))

    frac_q = [("f20_eq2", 2), ("t9_eq", 1)]
    for key, k in frac_q:
        g = G(key, cell=24)
        n, T, a = g["n"], g["total"], g["sizes"][0]
        e = ("Every part covers %s, so the parts are equal. There are %d equal parts, so the shaded part is %s of the "
             "rectangle." % (squ(a), n, fr(1, n)))
        its.append(mcq(fig(one_svg(g, (k,), "rectangle on a grid split into %d equal parts, 1 part shaded" % n)) +
                       "What fraction of the rectangle is shaded?", fr(1, n),
                       [fr(1, a), fr(1, T), fr(n, 1), fr(1, n + 1)], e, rnd))

    for T, n in [(24, 6), (18, 3), (16, 8)]:
        a = T // n
        e = "Equal parts share the area equally: %d ÷ %d = %d. Each part is %d square units and %s of the rectangle." % (
            T, n, a, a, fr(1, n))
        its.append(mcq("A rectangle has an area of %d square units. It is split into %d equal parts. "
                       "What is the area of each part?" % (T, n),
                       "%d sq units" % a, ["%d sq units" % v for v in [n, T - n, T, T + n]], e, rnd))
    for n, a in [(4, 5), (3, 7)]:
        T = n * a
        e = ("%s means the whole is %d equal parts. Each part is %d square units, so the whole is %d × %d = %d square units."
             % (fr(1, n), n, a, n, a, T))
        its.append(mcq("Each part of a rectangle is %s of the rectangle and has an area of %d square units. "
                       "What is the area of the whole rectangle?" % (fr(1, n), a),
                       "%d sq units" % T, ["%d sq units" % v for v in [a, a + n, a * (n - 1)]], e, rnd))
    its.append(mcq("A rectangle has an area of 12 square units. It is split into equal parts of 2 square units each. "
                   "What fraction of the rectangle is each part?", fr(1, 6), [fr(1, 2), fr(1, 12), fr(6, 1)],
                   "12 ÷ 2 = 6, so there are 6 equal parts. Each part is %s of the rectangle. "
                   "(%s would use the size of the part, not the number of parts.)" % (fr(1, 6), fr(1, 2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of each part", "items": its}


# ============================================================ set 5: which picture? word problems
def set_words(rnd):
    its = []
    # which picture shows 1/d shaded?
    pics = [
        (3, [(EQ(3, 0), (1,))], [(UNEQ(3, 1), (0,)), (EQ(4, 0), (2,)), (EQ(3, 1), (0, 1))]),
        (4, [(EQ(4, 1), (3,))], [(UNEQ(4, 0), (0,)), (r_vstrips([.2] * 5, w=P, h=62), (1,)), (EQ(4, 2), (0, 1, 3))]),
        (2, [(EQ(2, 5), (1,))], [(UNEQ(2, 0), (1,)), (EQ(3, 2), (0,)), (UNEQ(2, 2), (0,))]),
        (6, [(EQ(6, 2), (0,))], [(UNEQ(6, 0), (2,)), (c_sectors([360 / 7.0] * 7, r=P / 2), (3,)), (EQ(6, 1), (0, 1, 2, 3, 4))]),
    ]
    spots = Spots(rnd)
    for d, good, bads in pics:
        for s, _ in good:
            check_equal(s)
        pos = spots.next()
        bads = bads[:]
        rnd.shuffle(bads)
        shapes = bads[:pos] + good + bads[pos:]
        svg = panel_svg(shapes, "four shapes A to D with parts shaded")
        L = "ABCD"[pos]
        e = ("Shape <b>%s</b> has %d equal parts with 1 part shaded: %s. Check the others: the parts must be equal, "
             "and the bottom number counts <b>all</b> the parts, not only the white ones." % (L, d, fr(1, d)))
        its.append(mcq_fixed(fig(svg) + "Which shape has %s shaded?" % fr(1, d), ["A", "B", "C", "D"], pos, e))

    # how many parts make the whole?
    for d, thing, part in [(3, "flag", "stripe"), (6, "garden", "bed"), (8, "rug", "piece")]:
        e = "Each %s is %s, so the whole %s is %d equal %ss: %s = 1 whole." % (part, fr(1, d), thing, d, part, fr(d, d))
        its.append(mcq("Each %s of a %s is %s of the %s. How many equal %ss make the whole %s?" % (part, thing, fr(1, d), thing, part, thing),
                       "%d %ss" % (d, part), ["1 %s" % part, "%d %ss" % (d - 1, part), "%d %ss" % (d + 1, part)], e, rnd))

    its.append(mcq("Maya and 3 friends share a square cake equally. What fraction of the cake does each person get?",
                   fr(1, 4), [fr(1, 3), fr(4, 1), fr(3, 4)],
                   "Maya and 3 friends are <b>4 people</b>, so the cake is cut into 4 equal parts. Each person gets %s. "
                   "Do not forget to count Maya." % fr(1, 4), rnd))
    its.append(mcq("Leo and 5 friends share a pan of brownies equally. What fraction of the pan does each person get?",
                   fr(1, 6), [fr(1, 5), fr(6, 1), fr(5, 6)],
                   "Leo and 5 friends are <b>6 people</b>, so the pan is cut into 6 equal parts. Each person gets %s." % fr(1, 6), rnd))
    its.append(mcq("A garden has an area of 18 square meters. It is split into 3 equal beds. What is the area of each bed?",
                   "6 sq m", ["3 sq m", "15 sq m", "21 sq m"],
                   "Equal beds share the garden equally: 18 ÷ 3 = 6 square meters. Each bed is %s of the garden." % fr(1, 3), rnd))
    its.append(mcq("A garden is split into equal beds. Each bed is 6 square meters and the garden is 24 square meters. "
                   "What fraction of the garden is one bed?", fr(1, 4), [fr(1, 6), fr(1, 24), fr(4, 1)],
                   "24 ÷ 6 = 4, so there are 4 equal beds. One bed is %s of the garden. "
                   "The bottom number is the number of beds, not the size of a bed." % fr(1, 4), rnd))
    its.append(mcq("A window has 6 equal panes. 1 pane is broken. What fraction of the window is broken?",
                   fr(1, 6), [fr(1, 5), fr(5, 6), fr(6, 1)],
                   "The window is 6 equal panes and 1 is broken: %s. (%s compares broken panes to the 5 good panes. "
                   "The bottom number must be all 6 panes.)" % (fr(1, 6), fr(1, 5)), rnd))
    flag = check_unequal(r_vstrips([.25, .5, .25], w=150, h=90))
    its.append(mcq(fig(one_svg(flag, (1,), "flag with 3 stripes, the wide middle stripe shaded")) +
                   "A flag has 3 stripes. Is the shaded stripe %s of the flag?" % fr(1, 3),
                   "No, the stripes are not equal", ["Yes, it is 1 of 3 stripes", "Yes, it is in the middle", "No, it is " + fr(3, 1)],
                   "The middle stripe is wider than the other two. %s needs 3 <b>equal</b> parts, so the shaded stripe is not %s."
                   % (fr(1, 3), fr(1, 3)), rnd))
    its.append(mcq("Sam cuts a pizza into 8 pieces of different sizes. He says each piece is %s of the pizza. Is he right?" % fr(1, 8),
                   "No, the pieces are not equal", ["Yes, there are 8 pieces", "No, each piece is " + fr(8, 1), "No, each piece is " + fr(1, 7)],
                   "%s means 1 of 8 <b>equal</b> parts. Sam’s pieces are different sizes, so they are not eighths." % fr(1, 8), rnd))
    its.append(mcq("Flag A has 3 equal stripes that go up and down. Flag B is the same size and has 3 equal stripes that go "
                   "across. Each flag has 1 red stripe. Which flag has more red?", "The same, " + fr(1, 3) + " each",
                   ["Flag A", "Flag B", "You can’t tell"],
                   "Both flags are cut into 3 equal stripes, so each red stripe is %s of the same size flag. "
                   "The stripes point different ways but have the same area." % fr(1, 3), rnd))
    its.append(mcq("Kai folds a sheet of paper in half, then in half again the same way. He opens it and sees 4 equal strips. "
                   "Each strip is what fraction of the paper?", fr(1, 4), [fr(1, 3), fr(1, 2), fr(4, 1)],
                   "There are 4 equal strips, so each strip is %s. The paper has 3 fold lines, but you count the parts, "
                   "not the lines." % fr(1, 4), rnd))
    its.append(mcq("Ruby and 2 friends share a chocolate bar of 12 equal squares. Each person gets the same amount. "
                   "How much does each person get?", "4 squares, " + fr(1, 3),
                   ["6 squares, " + fr(1, 2), "4 squares, " + fr(1, 4), "3 squares, " + fr(1, 4)],
                   "Ruby and 2 friends are 3 people. 12 ÷ 3 = 4 squares each, and each share is %s of the bar." % fr(1, 3), rnd))
    its.append(mcq("A square garden is split into 4 equal parts. Ava plants beans in 1 part. What fraction of the garden "
                   "has <b>no</b> beans?", fr(3, 4), [fr(1, 4), fr(1, 3), fr(3, 1)],
                   "There are 4 equal parts. 1 part has beans, so 3 parts have no beans: %s." % fr(3, 4), rnd))
    its.append(mcq("Omar splits a rectangle of 4 by 2 unit squares into 2 equal parts shaped like stairs. "
                   "What is the area of each part?", "4 sq units", ["2 sq units", "8 sq units", "6 sq units"],
                   "The rectangle has 4 × 2 = 8 unit squares. 2 equal parts: 8 ÷ 2 = 4 square units each. "
                   "The stair shape does not change the area.", rnd))
    its.append(mcq("Jack wants to split a rectangle of 6 by 2 unit squares into 3 equal parts. "
                   "How many unit squares should each part have?", "4 squares", ["3 squares", "6 squares", "2 squares"],
                   "The rectangle has 6 × 2 = 12 squares. 3 equal parts: 12 ÷ 3 = 4 squares in each part, "
                   "and each part is %s of the rectangle." % fr(1, 3), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Pictures and word problems", "items": its}


# ============================================================ lesson
def labeled_row(shapes, labels, label):
    """Shapes in a row with a caption under each."""
    gap, pad = 26, 6
    cw = max(s["w"] for s, _ in shapes)
    ch = max(s["h"] for s, _ in shapes)
    W = pad * 2 + len(shapes) * cw + (len(shapes) - 1) * gap
    H = pad * 2 + ch + 30
    s = []
    for i, ((sh, shaded), t) in enumerate(zip(shapes, labels)):
        x0 = pad + i * (cw + gap)
        s.append(draw(sh, shaded, x0 + (cw - sh["w"]) / 2, pad + (ch - sh["h"]) / 2))
        s.append("<text x='%.1f' y='%.1f' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x0 + cw / 2, pad + ch + 24, LINE, t))
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s), label)


def body_html():
    f1 = labeled_row([(check_equal(r_grid(2, 2, w=140, h=90)), ()), (check_unequal(r_cross(.3, .35, w=140, h=90)), ())],
                     ["Equal parts", "Not equal parts"], "a rectangle cut into 4 equal parts and one cut into 4 unequal parts")
    f2 = one_svg(check_equal(r_vstrips([.25] * 4, w=240, h=80)), (0,), "rectangle split into 4 equal parts, 1 part shaded")
    S = 96
    f3 = labeled_row([(check_equal(sq(r_x, s=S)), (0,)), (check_equal(sq(r_grid, 2, 2, s=S)), (0,)),
                      (check_equal(sq(r_vstrips, [.25] * 4, s=S)), (0,))],
                     ["1/4", "1/4", "1/4"], "three same-size squares, each cut into 4 equal parts of different shapes")
    f4, g = grid_svg(GRIDS["f12_eq"], (0,), cell=34)
    return (
        "<h2>Equal parts</h2>"
        "<p>To <b>partition</b> a shape means to cut it into parts. For fractions, the parts must be <b>equal</b>: "
        "they must have the <b>same area</b> (cover the same amount of space).</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Both rectangles have 4 parts. Only the first one shows fourths, because its parts are the same size.</figcaption></figure>"
        "<h2>Name each part with a unit fraction</h2>"
        "<p>If a shape is cut into equal parts, each part is a <b>unit fraction</b> of the whole: "
        "1 on top, the number of equal parts on the bottom.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>4 equal parts. The shaded part is " + fr(1, 4) + " (one fourth) of the area of the rectangle.</figcaption></figure>" +
        table(["Equal parts", "Name", "Each part"], [
            ["2", "halves", fr(1, 2) + " (one half)"],
            ["3", "thirds", fr(1, 3) + " (one third)"],
            ["4", "fourths", fr(1, 4) + " (one fourth)"],
            ["6", "sixths", fr(1, 6) + " (one sixth)"],
            ["8", "eighths", fr(1, 8) + " (one eighth)"],
        ]) +
        "<h2>Same area, different shape</h2>"
        "<p>Equal parts do <b>not</b> have to be the same shape. They only need the same area.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>Three same-size squares, each cut into 4 equal parts. A triangle, a small square and a strip: "
        "each is " + fr(1, 4) + " of the square.</figcaption></figure>"
        "<p>On a grid, count the unit squares in each part to check.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>12 squares, 4 parts of different shapes. Every part covers 3 squares, so each part is "
        "3 square units and " + fr(1, 4) + " of the rectangle.</figcaption></figure>" +
        ex("Example", "A rectangle has an area of 20 square units. It is split into 4 equal parts. What is the area of each part, "
           "and what fraction of the whole is it?",
           "Equal parts share the area: 20 ÷ 4 = 5. There are 4 equal parts, so each is " + fr(1, 4) + ".",
           "5 square units, " + fr(1, 4)) +
        ex("Example", "Mia and 2 friends share a sandwich equally. What fraction does each person get?",
           "Mia and 2 friends are 3 people, so the sandwich is cut into 3 equal parts.", fr(1, 3)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the parts without checking they are equal", "First check that every part has the same area"],
            ["Thinking parts of different shapes cannot be equal", "Compare the area, not the shape. Count squares on a grid"],
            ["Calling 1 shaded part out of 4 “" + fr(1, 3) + "” (1 shaded, 3 white)", "The bottom number is <b>all</b> the parts: " + fr(1, 4)],
            ["Counting the cut lines instead of the parts", "Count the parts: 3 cut lines can make 4 parts"],
            ["Using the squares in one part as the bottom number", "The bottom number is the number of equal parts"],
        ])
    )


FAQ = [
    {"q": "What does partition shapes mean in 3rd grade math?",
     "a": "It means cutting a shape into parts with equal area, then naming each part with a unit fraction. A rectangle cut into 4 equal parts has parts that are each 1/4 of its area."},
    {"q": "Do equal parts have to be the same shape?",
     "a": "No. Equal parts need the same area, not the same shape. A square cut on both diagonals and a square cut into 4 strips both have parts that are 1/4 of the square."},
    {"q": "How do you find the area of each equal part?",
     "a": "Divide the area of the whole by the number of equal parts. A rectangle of 12 square units cut into 4 equal parts has parts of 3 square units, and each part is 1/4 of the whole."},
    {"q": "What is a unit fraction?",
     "a": "A unit fraction has 1 on top, like 1/2, 1/3 or 1/8. It names one of the equal parts that make the whole."},
]


def gen_partition():
    rnd = random.Random(46)
    sets = [set_equal(rnd), set_unit(rnd), set_shape(rnd), set_area(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "partition-shapes", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Partition Shapes into Equal Parts",
        "seo_title": "Grade 3 Partitioning Shapes Worksheets: Equal Parts, Unit Fractions and Area of Each Part",
        "short_title": "Partition Shapes",
        "domain": "Geometry",
        "standard_code": "3.G.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/G/A/2/",
        "standard_text": "Partition shapes into parts with equal areas. Express the area of each part as a unit fraction of the whole. For example, partition a shape into 4 parts with equal area, and describe the area of each part as 1/4 of the area of the shape.",
        "meta_desc": "Free Grade 3 partitioning shapes worksheets with pictures: tell equal from unequal parts, name halves, thirds, fourths, sixths and eighths, see that equal parts can have different shapes, and find the area of each part on a grid. 100 practice questions with answers.",
        "key_big": "Equal parts have the same area. Each part is 1 over the number of equal parts.",
        "key_sub": "Cut into 4 equal parts, each part is 1/4 of the whole. Equal parts can have different shapes: a triangle and a strip can both be 1/4 of the same square.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rulers, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_partition()
    path = os.path.join(OUT, "partition-shapes.json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(four shapes A to D|shapes A and B)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
