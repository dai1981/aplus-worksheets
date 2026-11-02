# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Line symmetry
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 4: Geometry — identifying symmetric figures;
 determining whether a line is a line of symmetry; completing a symmetric figure on a square grid)
  python3 tools/gen_sg_maths_p4_symmetry.py
Every figure is built from exact coordinates and its symmetry is found in code: a line is a line of
symmetry when reflecting every edge (with its colour) across it gives exactly the same set of edges.
Every count in an answer is the count found here, and every dashed line in a question is tested the
same way. Letters are drawn as strokes, so their symmetry is exact. Grid pictures (vertical and
horizontal lines of symmetry, as in the MOE syllabus) are checked square by square.
Wrong answers come from real P4 mistakes: counting the diagonals of a rectangle as lines of symmetry,
looking only for vertical lines, giving a parallelogram 2 lines, sliding instead of flipping, reflecting
in the wrong direction (flipping upside down across a vertical line), counting squares from the edge of
the grid, and mixing up "looks the same when turned" with a fold.
HTML attributes use single quotes (no backslashes in the JSON). British spelling as used in Singapore.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
DASH = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
BLUE = "#2f6db5"
YELLOW = "#f2c230"
WHITE = "#ffffff"
SHADE = "#4fae74"
SHADE2 = "#a9d8b8"
THIN = "#a8a8a8"
INF = "Infinitely many"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
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
    """Choices keep their order (A B C D, or a fixed list). The answer position is not moved later."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


class Spots:
    """Answer letters for A-D picture questions: each of A-D used equally often, in a shuffled order."""
    def __init__(self, rnd):
        self.rnd, self.left = rnd, []

    def next(self):
        if not self.left:
            self.left = [0, 1, 2, 3]
            self.rnd.shuffle(self.left)
        return self.left.pop()


def balance(s, rnd):
    """Move the answers of the free questions so every position (A-D) is right 5 times in the set."""
    cnt, free = [0] * 4, []
    for it in s["items"]:
        if it.pop("_fix", False):
            cnt[it["a"]] += 1
        else:
            free.append(it)
    targets = []
    for p in range(4):
        assert cnt[p] <= 5, (s["title"], cnt)
        targets += [p] * (5 - cnt[p])
    assert len(targets) == len(free)
    rnd.shuffle(targets)
    for it, t in zip(free, targets):
        c = it["c"]
        c[it["a"]], c[t] = c[t], c[it["a"]]
        it["a"] = t


def lines_word(n):
    return "1 line" if n == 1 else "%d lines" % n


# ------------------------------------------------------------ figures made of exact primitives
def _clean(pts):
    out = []
    for p in pts:
        p = (float(p[0]), float(p[1]))
        if not out or q(out[-1]) != q(p):
            out.append(p)
    return out


def Poly(pts, fill=FILL, sc=GREEN, sw=3.0):
    pts = _clean(pts)
    if q(pts[0]) == q(pts[-1]):
        pts = pts[:-1]
    return {"t": "poly", "pts": pts, "fill": fill, "sc": sc, "sw": sw}


def Line(pts, sc=INK, sw=8.0):
    return {"t": "line", "pts": _clean(pts), "sc": sc, "sw": sw}


def Circ(c, r, fill=FILL, sc=GREEN, sw=3.0):
    return {"t": "circle", "c": (float(c[0]), float(c[1])), "r": float(r), "fill": fill, "sc": sc, "sw": sw}


def q(p):
    return (int(round(p[0] * 100)), int(round(p[1] * 100)))


def arc(cx, cy, rx, ry, a0, a1, n):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def refl(p, c, a):
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    v = (p[0] - c[0], p[1] - c[1])
    t = v[0] * d[0] + v[1] * d[1]
    return (2 * (c[0] + d[0] * t) - p[0], 2 * (c[1] + d[1] * t) - p[1])


def edges(pr):
    pts = pr["pts"]
    n = len(pts)
    rng = range(n) if pr["t"] == "poly" else range(n - 1)
    return [(pts[i], pts[(i + 1) % n]) for i in rng]


def tag(pr):
    return (pr["t"], pr.get("fill"), pr["sc"], pr["sw"])


def keyset(F):
    ks = set()
    for pr in F:
        if pr["t"] == "circle":
            ks.add((tag(pr), q(pr["c"]), int(round(pr["r"] * 100))))
        else:
            for a, b in edges(pr):
                ks.add((tag(pr), frozenset((q(a), q(b)))))
    return ks


def is_axis(F, c, a):
    K = keyset(F)
    for pr in F:
        if pr["t"] == "circle":
            if (tag(pr), q(refl(pr["c"], c, a)), int(round(pr["r"] * 100))) not in K:
                return False
        else:
            for p1, p2 in edges(pr):
                if (tag(pr), frozenset((q(refl(p1, c, a)), q(refl(p2, c, a))))) not in K:
                    return False
    return True


def all_pts(F):
    out = []
    for pr in F:
        out += [pr["c"]] if pr["t"] == "circle" else pr["pts"]
    return out


def center(F):
    u = {q(p): p for p in all_pts(F)}
    return (sum(p[0] for p in u.values()) / len(u), sum(p[1] for p in u.values()) / len(u))


def axes(F):
    """Angles (degrees, 0 = across, 90 = up and down) of all lines of symmetry, or INF."""
    if all(pr["t"] == "circle" for pr in F) and len({q(pr["c"]) for pr in F}) == 1:
        return INF
    c = center(F)
    cands = [i * 0.5 for i in range(360)]
    pts = all_pts(F)
    for pr in F:
        if pr["t"] != "circle":
            pts += [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in edges(pr)]
    for p in pts:
        if math.hypot(p[0] - c[0], p[1] - c[1]) > 1e-6:
            cands.append(round(math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])), 6) % 180)
    res = []
    for a in sorted(cands):
        if any(abs(a - b) < 1e-3 or abs(abs(a - b) - 180) < 1e-3 for b in res):
            continue
        if is_axis(F, c, a):
            res.append(a)
    return res


def nlines(F):
    a = axes(F)
    return INF if a == INF else len(a)


def expect(F, n, name=""):
    got = nlines(F)
    assert got == n, (name, got, n)
    return F


def area(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def clip(pts, p, a, side):
    """Part of a polygon on one side of the line through p at angle a."""
    nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
    f = lambda v: side * ((v[0] - p[0]) * nx + (v[1] - p[1]) * ny)
    out = []
    for i in range(len(pts)):
        A, B = pts[i], pts[(i + 1) % len(pts)]
        fa, fb = f(A), f(B)
        if fa >= 0:
            out.append(A)
        if (fa >= 0) != (fb >= 0):
            t = fa / (fa - fb)
            out.append((A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t))
    return out


def split_kind(F, p, a):
    """'Y' line of symmetry, 'N2' two parts of the same size that do not match, 'N1' one part clearly bigger."""
    if is_axis(F, p, a):
        return "Y"
    pts = F[0]["pts"]
    a1, a2 = area(clip(pts, p, a, 1)), area(clip(pts, p, a, -1))
    assert a1 > 0 and a2 > 0, "line misses the shape"
    if abs(a1 - a2) < 1e-6 * (a1 + a2):
        return "N2"
    assert max(a1, a2) / min(a1, a2) >= 1.3, ("parts too close in size", a1, a2)
    return "N1"


# ------------------------------------------------------------ shapes (y goes down, like SVG)
def rot(pts, deg):
    t = math.radians(deg)
    return [(x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)) for x, y in pts]


def reg(n, r=50, start=-90):
    return [(r * math.cos(math.radians(start + 360.0 * i / n)), r * math.sin(math.radians(start + 360.0 * i / n)))
            for i in range(n)]


def rect(w, h):
    return [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]


def isos(w, h):
    return [(0, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]


def para(w, h, off):
    return [(-w / 2 + off, -h / 2), (w / 2 + off, -h / 2), (w / 2 - off, h / 2), (-w / 2 - off, h / 2)]


def diamond(w, h):
    return [(0, -h / 2), (w / 2, 0), (0, h / 2), (-w / 2, 0)]


def kite(w, h, a):
    return [(0, -h / 2), (w / 2, -h / 2 + a), (0, h / 2), (-w / 2, -h / 2 + a)]


def itrap(bot, top, h):
    return [(-top / 2, -h / 2), (top / 2, -h / 2), (bot / 2, h / 2), (-bot / 2, h / 2)]


def ellipse(rx, ry, n=72):
    return arc(0, 0, rx, ry, 0, 360, n)[:-1]


def semicircle(r, n=36):
    return arc(0, 0, r, r, 180, 360, n)


def plus(a, t):
    return [(-t, -a), (t, -a), (t, -t), (a, -t), (a, t), (t, t), (t, a), (-t, a), (-t, t), (-a, t), (-a, -t), (-t, -t)]


def ell(L, t):
    return [(0, 0), (t, 0), (t, L - t), (L, L - t), (L, L), (0, L)]


def arrow():
    return [(0, 30), (60, 30), (60, 0), (100, 50), (60, 100), (60, 70), (0, 70)]


def heart(n=64):
    out = []
    for k in range(n):
        t = 2 * math.pi * k / n
        out.append((3.2 * 16 * math.sin(t) ** 3,
                    -3.2 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))))
    return out


def S1(pts, fill=FILL):
    return [Poly(pts, fill)]


SHAPES = {
    "square": lambda: S1(rect(96, 96)),
    "rectangle": lambda: S1(rect(132, 76)),
    "tall rectangle": lambda: S1(rect(70, 112)),
    "equilateral triangle": lambda: S1(reg(3, 60)),
    "isosceles triangle": lambda: S1(isos(84, 116)),
    "scalene triangle": lambda: S1([(-60, 40), (60, 40), (28, -42)]),
    "isosceles right-angled triangle": lambda: S1([(-48, -48), (-48, 48), (48, 48)]),
    "right-angled triangle": lambda: S1([(-58, -36), (-58, 36), (58, 36)]),
    "circle": lambda: [Circ((0, 0), 50)],
    "rhombus": lambda: S1(diamond(84, 128)),
    "parallelogram": lambda: S1(para(100, 70, 20)),
    "kite": lambda: S1(kite(84, 124, 36)),
    "isosceles trapezium": lambda: S1(itrap(130, 70, 74)),
    "regular pentagon": lambda: S1(reg(5, 58)),
    "regular hexagon": lambda: S1(reg(6, 58)),
    "regular octagon": lambda: S1(reg(8, 58, -90 + 22.5)),
    "tilted rectangle": lambda: S1(rot(rect(120, 62), -25)),
    "plus sign": lambda: S1(plus(54, 18)),
    "L shape": lambda: S1(ell(100, 34)),
    "arrow": lambda: S1(arrow()),
    "heart": lambda: S1(heart()),
    "semicircle": lambda: S1(semicircle(62)),
    "ellipse": lambda: S1(ellipse(64, 38)),
}
LINES = {"square": 4, "rectangle": 2, "tall rectangle": 2, "equilateral triangle": 3, "isosceles triangle": 1,
         "scalene triangle": 0, "isosceles right-angled triangle": 1, "right-angled triangle": 0, "circle": INF, "rhombus": 2,
         "parallelogram": 0, "kite": 1, "isosceles trapezium": 1, "regular pentagon": 5,
         "regular hexagon": 6, "regular octagon": 8, "tilted rectangle": 2, "plus sign": 4, "L shape": 1,
         "arrow": 1, "heart": 1, "semicircle": 1, "ellipse": 2}


def shp(name):
    return expect(SHAPES[name](), LINES[name], name)


# ------------------------------------------------------------ capital letters as strokes
def letter(ch):
    L = lambda *p: Line(p)
    if ch == "A":
        return [L((-22, 32), (0, -32), (22, 32)), L((-13.75, 8), (13.75, 8))]
    if ch == "B":
        return [L((-18, -32), (-18, 32)), Line([(-18, -32)] + arc(2, -16, 16, 16, -90, 90, 16) + [(-18, 0)]),
                Line([(-18, 0)] + arc(2, 16, 16, 16, -90, 90, 16) + [(-18, 32)])]
    if ch == "C":
        return [Line(arc(0, 0, 24, 32, 45, 315, 36))]
    if ch == "D":
        return [L((-20, -32), (-20, 32)), Line([(-20, -32)] + arc(-2, 0, 22, 32, -90, 90, 24) + [(-20, 32)])]
    if ch == "E":
        return [L((18, -32), (-18, -32), (-18, 32), (18, 32)), L((-18, 0), (12, 0))]
    if ch == "F":
        return [L((18, -32), (-16, -32), (-16, 32)), L((-16, 0), (10, 0))]
    if ch == "G":
        return [Line(arc(0, 0, 24, 32, 315, 0, 40)), L((24, 0), (6, 0))]
    if ch == "H":
        return [L((-20, -32), (-20, 32)), L((20, -32), (20, 32)), L((-20, 0), (20, 0))]
    if ch == "I":
        return [L((0, -32), (0, 32)), L((-14, -32), (14, -32)), L((-14, 32), (14, 32))]
    if ch == "J":
        return [Line([(14, -32)] + arc(-4, 12, 18, 18, 0, 180, 20))]
    if ch == "L":
        return [L((-16, -32), (-16, 32), (18, 32))]
    if ch == "M":
        return [L((-24, 32), (-24, -32), (0, 10), (24, -32), (24, 32))]
    if ch == "N":
        return [L((-20, 32), (-20, -32), (20, 32), (20, -32))]
    if ch == "O":
        return [Line(arc(0, 0, 24, 32, 0, 360, 48))]
    if ch == "P":
        return [L((-18, 32), (-18, -32)), Line([(-18, -32)] + arc(0, -14, 18, 18, -90, 90, 18) + [(-18, 4)])]
    if ch == "Q":
        return [Line(arc(0, 0, 24, 32, 0, 360, 48)), L((6, 14), (24, 34))]
    if ch == "R":
        return letter("P") + [L((0, 4), (20, 32))]
    if ch == "S":
        return [Line(arc(0, -16, 20, 16, 330, 90, 24) + arc(0, 16, 20, 16, -90, 150, 24))]
    if ch == "T":
        return [L((-24, -32), (24, -32)), L((0, -32), (0, 32))]
    if ch == "U":
        return [Line([(-22, -32)] + arc(0, 10, 22, 22, 180, 0, 24) + [(22, -32)])]
    if ch == "V":
        return [L((-22, -32), (0, 32), (22, -32))]
    if ch == "W":
        return [L((-28, -32), (-14, 32), (0, -10), (14, 32), (28, -32))]
    if ch == "X":
        return [L((-20, -32), (20, 32)), L((20, -32), (-20, 32))]
    if ch == "Y":
        return [L((-22, -32), (0, 0), (22, -32)), L((0, 0), (0, 32))]
    if ch == "Z":
        return [L((-20, -32), (20, -32), (-20, 32), (20, 32))]
    raise ValueError(ch)


VERT = set("AMTUVWY")
HORI = set("BCDE")
BOTH = set("HIOX")
NONE = set("FGJLNPQRSZ")
KIND = {}
for _c in "ABCDEFGHIJLMNOPQRSTUVWXYZ":
    _a = axes(letter(_c))
    _k = ("v" if _a == [90.0] else "h" if _a == [0.0] else "b" if _a == [0.0, 90.0] else "n" if _a == [] else "?")
    KIND[_c] = _k
    assert _k == ("v" if _c in VERT else "h" if _c in HORI else "b" if _c in BOTH else "n"), (_c, _a)


# ------------------------------------------------------------ real-world pictures
def mirror_x(F):
    """Copy of a figure reflected across the line x = 0."""
    out = []
    for pr in F:
        p = dict(pr)
        if pr["t"] == "circle":
            p["c"] = (-pr["c"][0], pr["c"][1])
        else:
            p["pts"] = [(-x, y) for x, y in reversed(pr["pts"])]
        out.append(p)
    return out


def butterfly():
    up = Poly([(x + 26, y - 16) for x, y in rot(ellipse(25, 16, 48), -35)], "#f2c230", GREEN, 2.5)
    lo = Poly([(x + 19, y + 17) for x, y in rot(ellipse(16, 11, 40), 35)], "#f2c230", GREEN, 2.5)
    s1 = Circ((32, -20), 6, "#ffffff", GREEN, 2)
    s2 = Circ((20, 18), 4, "#ffffff", GREEN, 2)
    right = [up, lo, s1, s2]
    body = Poly(ellipse(5, 28, 40), INK, INK, 1)
    ant = [Line([(0, -24), (10, -42)], INK, 2.5), Line([(0, -24), (-10, -42)], INK, 2.5)]
    return right + mirror_x(right) + [body] + ant


def leaf():
    side = [(26 * math.sin(math.pi * i / 24), -42 + 84.0 * i / 24) for i in range(25)]
    outline = side + [(-x, y) for x, y in reversed(side)][1:-1]
    veins = [Line([(0, y0), (16, y0 - 14)], GREEN, 2) for y0 in (-12, 4, 20)]
    return ([Poly(outline, "#9fd3a8", GREEN, 2.5), Line([(0, -38), (0, 58)], GREEN, 3)] +
            veins + mirror_x(veins))


# ------------------------------------------------------------ drawing
def dash_seg(F, p, a, ext=0.16):
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    ts = []
    for pr in F:
        if pr["t"] == "circle":
            t0 = (pr["c"][0] - p[0]) * d[0] + (pr["c"][1] - p[1]) * d[1]
            ts += [t0 - pr["r"], t0 + pr["r"]]
        else:
            ts += [(x - p[0]) * d[0] + (y - p[1]) * d[1] for x, y in pr["pts"]]
    t0, t1 = min(ts), max(ts)
    e = ext * (t1 - t0)
    return ((p[0] + d[0] * (t0 - e), p[1] + d[1] * (t0 - e)), (p[0] + d[0] * (t1 + e), p[1] + d[1] * (t1 + e)))


def render(F, segs, bw, bh, cx, cy):
    """SVG elements for figure F (and dashed segments) scaled to fit a bw x bh box centred at (cx, cy)."""
    xs, ys = [], []
    for pr in F:
        if pr["t"] == "circle":
            xs += [pr["c"][0] - pr["r"], pr["c"][0] + pr["r"]]
            ys += [pr["c"][1] - pr["r"], pr["c"][1] + pr["r"]]
        else:
            xs += [p[0] for p in pr["pts"]]
            ys += [p[1] for p in pr["pts"]]
    for s in segs:
        xs += [s[0][0], s[1][0]]
        ys += [s[0][1], s[1][1]]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    T = lambda p: (cx + (p[0] - mx) * k, cy + (p[1] - my) * k)
    el, box = [], []
    for pr in F:
        h = pr["sw"] / 2
        if pr["t"] == "circle":
            c, r = T(pr["c"]), pr["r"] * k
            el.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%g'/>"
                      % (c[0], c[1], r, pr["fill"], pr["sc"], pr["sw"]))
            box += [(c[0] - r - h, c[1] - r - h), (c[0] + r + h, c[1] + r + h)]
            continue
        P = [T(p) for p in pr["pts"]]
        s = " ".join("%.1f,%.1f" % p for p in P)
        if pr["t"] == "poly":
            el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                      % (s, pr["fill"], pr["sc"], pr["sw"]))
        else:
            el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linecap='round' "
                      "stroke-linejoin='round'/>" % (s, pr["sc"], pr["sw"]))
        box += [(x - h, y - h) for x, y in P] + [(x + h, y + h) for x, y in P]
    for a, b in segs:
        A, B = T(a), T(b)
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='8 5'/>"
                  % (A + B + (DASH,)))
        box += [(A[0] - 2, A[1] - 2), (B[0] + 2, B[1] + 2), (A[0] + 2, A[1] + 2), (B[0] - 2, B[1] - 2)]
    bb = (min(p[0] for p in box), min(p[1] for p in box), max(p[0] for p in box), max(p[1] for p in box))
    return el, bb


def single_svg(F, segs=(), bw=118, bh=84, label="shape"):
    _, bb = render(F, segs, bw, bh, 0, 0)
    pad = 5
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1
    el, bb2 = render(F, segs, bw, bh, W / 2.0 - (bb[0] + bb[2]) / 2, H / 2.0 - (bb[1] + bb[3]) / 2)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H, bb2
    return svg_wrap(W, H, "".join(el), label)


CELL = 116


def panel_svg(items, label, box=76):
    """2 x 2 pictures labeled A-D. items: list of (figure, dashed segments)."""
    el = []
    W = H = 2 * CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    el.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY))
    for k, (F, segs) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb = render(F, segs, box, box, x0 + 66, y0 + 62)
        assert bb[0] >= x0 + 20 and bb[1] >= y0 + 4 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, (label, bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, label, cw=124, box=(92, 86)):
    """Lesson figure: a row of pictures with a caption under each. items: (figure, dashed segments, caption)."""
    top = box[1] + 10
    el = []
    for k, (F, segs, cap) in enumerate(items):
        e, bb = render(F, segs, box[0], box[1], k * cw + cw / 2.0, top / 2.0)
        assert bb[0] >= k * cw + 1 and bb[2] <= (k + 1) * cw - 1 and bb[1] >= 0 and bb[3] <= top, (cap, bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (k * cw + cw / 2, top + 18, INK, cap))
    return svg_wrap(cw * len(items), top + 26, "".join(el), label)


def all_axis_segs(F):
    a = axes(F)
    c = center(F)
    return [dash_seg(F, c, x) for x in a]


# ------------------------------------------------------------ grid pictures
def cells_of(rows, dc=0, dr=0):
    return frozenset((c + dc, r + dr) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "#")


def mir(cell, line):
    c, r = cell
    if line[0] == "v":
        return (int(round(2 * line[1] - 1 - c)), r)
    if line[0] == "h":
        return (c, int(round(2 * line[1] - 1 - r)))
    if line[0] == "a":                      # top-right corner to bottom-left corner of an n x n grid
        return (line[1] - 1 - r, line[1] - 1 - c)
    return (r, c)                           # "d": top-left corner to bottom-right corner


def gsym(cells, line):
    return all(mir(x, line) in cells for x in cells)


def grid_el(cols, rows, cells, line, cs, ox, oy, light=()):
    el = []
    for (c, r) in sorted(cells):
        assert 0 <= c < cols and 0 <= r < rows, (c, r)
        el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s'/>"
                  % (ox + c * cs, oy + r * cs, cs, cs, SHADE2 if (c, r) in light else SHADE))
    for c in range(1, cols):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox + c * cs, oy, ox + c * cs, oy + rows * cs, THIN))
    for r in range(1, rows):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox, oy + r * cs, ox + cols * cs, oy + r * cs, THIN))
    el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
              % (ox, oy, cols * cs, rows * cs, INK))
    o = 7
    if line[0] == "v":
        x = ox + line[1] * cs
        seg = (x, oy - o, x, oy + rows * cs + o)
    elif line[0] == "h":
        y = oy + line[1] * cs
        seg = (ox - o, y, ox + cols * cs + o, y)
    elif line[0] == "a":
        seg = (ox + cols * cs + o, oy - o, ox - o, oy + rows * cs + o)
    else:
        seg = (ox - o, oy - o, ox + cols * cs + o, oy + rows * cs + o)
    el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='8 5'/>"
              % (seg + (DASH,)))
    bb = (min(ox, seg[0], seg[2]) - 1.5, min(oy, seg[1], seg[3]) - 1.5,
          max(ox + cols * cs, seg[0], seg[2]) + 1.5, max(oy + rows * cs, seg[1], seg[3]) + 1.5)
    return el, bb


def grid_svg(cols, rows, cells, line, cs, label, light=()):
    pad = 6
    W, H = cols * cs + 2 * (pad + 8), rows * cs + 2 * (pad + 8)
    if W == H:
        W += 1
    el, bb = grid_el(cols, rows, cells, line, cs, (W - cols * cs) / 2.0, (H - rows * cs) / 2.0, light)
    assert bb[0] >= 0 and bb[1] >= 0 and bb[2] <= W and bb[3] <= H
    return svg_wrap(W, H, "".join(el), label)


def grid_panel(cols, rows, opts, line, cs, label):
    LW, gap, pad, o = 22, 16, 8, 8
    gw, gh = cols * cs, rows * cs
    W = 2 * pad + 2 * (LW + gw + 2 * o) + gap
    H = 2 * pad + 2 * (gh + 2 * o) + gap
    el = []
    for k, cells in enumerate(opts):
        cx, cy = k % 2, k // 2
        x0 = pad + cx * (LW + gw + 2 * o + gap)
        y0 = pad + cy * (gh + 2 * o + gap)
        e, bb = grid_el(cols, rows, cells, line, cs, x0 + LW + o, y0 + o)
        assert bb[0] >= x0 + LW - 1 and bb[1] >= y0 - 1 and bb[3] <= y0 + gh + 2 * o + 1, bb
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0, y0 + o + 16, INK, "ABCD"[k]))
    if W == H:
        W += 1
    return svg_wrap(W, H, "".join(el), label)

# ------------------------------------------------------------ turned shapes (set 3)
SHAPES.update({
    "turned square": lambda: S1(rot(rect(96, 96), 45)),
    "turned rectangle": lambda: S1(rot(rect(124, 64), -28)),
    "turned isosceles triangle": lambda: S1(rot(isos(84, 116), 90)),
    "upside-down isosceles triangle": lambda: S1(rot(isos(84, 116), 180)),
    "turned equilateral triangle": lambda: S1(reg(3, 60, -90 + 15)),
    "turned kite": lambda: S1(rot(kite(84, 124, 36), 60)),
    "turned parallelogram": lambda: S1(rot(para(100, 64, 20), 25)),
    "turned hexagon": lambda: S1(reg(6, 58, -90 + 15)),
    "turned trapezium": lambda: S1(rot(itrap(130, 70, 74), 90)),
})
LINES.update({"turned square": 4, "turned rectangle": 2, "turned isosceles triangle": 1,
              "upside-down isosceles triangle": 1, "turned equilateral triangle": 3, "turned kite": 1,
              "turned parallelogram": 0, "turned hexagon": 6, "turned trapezium": 1})
NOUN = {"isosceles trapezium": "trapezium", "turned trapezium": "trapezium", "equilateral triangle": "triangle",
        "turned equilateral triangle": "triangle", "isosceles triangle": "triangle", "turned isosceles triangle": "triangle",
        "upside-down isosceles triangle": "triangle", "isosceles right-angled triangle": "triangle", "ellipse": "oval",
        "regular hexagon": "hexagon", "turned hexagon": "hexagon", "turned square": "square", "turned rectangle": "rectangle",
        "tall rectangle": "rectangle", "turned kite": "kite", "turned parallelogram": "parallelogram"}



def noun(name):
    return NOUN.get(name, name)


# ============================================================ set 1: is the dashed line a line of symmetry?
Y_ = "Yes, both halves match"
N1_ = "No, one part is bigger"
N2_ = "No, same size but not matching"
T_ = "Yes, the parts are the same size"
U_ = "No, mirror lines must be vertical"


def line_q(name, F, p, a, rnd):
    kind = split_kind(F, p, a)
    seg = dash_seg(F, p, a)
    nn = noun(name)
    pic = fig(single_svg(F, [seg], label="%s with a dashed line" % nn))
    qs = pic + "Imagine folding the %s along the dashed line. Is the dashed line a line of symmetry?" % nn
    vert = abs(a - 90) < 1e-9
    if kind == "Y":
        e = "Fold along the dashed line: one half lands exactly on top of the other, so it <b>is</b> a line of symmetry."
        if not vert:
            e += " It is not vertical, and that is fine: a line of symmetry can go in any direction."
        return mcq(qs, Y_, [N2_, N1_, U_ if not vert else T_], e, rnd)
    if kind == "N2":
        e = ("The dashed line splits the %s into 2 parts of the <b>same size</b>, but if you fold along it, the corners "
             "do not land on each other. Equal halves are not enough: they must fit exactly when folded." % nn)
        if name in ("rectangle", "tall rectangle"):
            e = ("The diagonal splits the rectangle into 2 equal triangles, but fold along it and the corners stick out. "
                 "A diagonal of a rectangle is <b>not</b> a line of symmetry. Only a square’s diagonals are.")
        if name == "ellipse":
            e = ("The dashed line splits the oval into 2 equal parts, but folded on this slanting line the ends do not "
                 "land on each other. An oval has just 2 lines of symmetry: one across and one up and down.")
        return mcq(qs, N2_, [T_, Y_, N1_], e, rnd)
    e = ("The dashed line is not through the middle, so one part is bigger. The smaller part cannot cover the bigger "
         "part when you fold, so it is <b>not</b> a line of symmetry.")
    return mcq(qs, N1_, [Y_, T_, N2_], e, rnd)


def it(name, a=None, frac=None, F=None):
    """A shape with one dashed line: through the centre at angle a, or a vertical/horizontal line at a fraction of the width/height."""
    F = F or shp(name)
    c = center(F)
    if frac is not None:
        xs = [p[0] for p in all_pts(F)]
        ys = [p[1] for p in all_pts(F)]
        if a == 90:
            c = (min(xs) + frac * (max(xs) - min(xs)), c[1])
        else:
            c = (c[0], min(ys) + frac * (max(ys) - min(ys)))
    return (name, F, c, a)


WHY = {"Y": "the halves match", "N1": "the line is not through the middle", "N2": "equal parts, but they do not fit when folded"}


def pool_kinds(pool):
    for k, (name, F, p, a) in list(pool.items()):
        pool[k] = (name, F, p, a, split_kind(F, p, a))
    return pool


def panel_qs(plans, POOL, rnd, extra_rect=None):
    out, used = [], set()
    spots = Spots(rnd)
    for mode, (good, bads) in plans:
        g = POOL[good]
        assert (g[4] == "Y") == (mode == "is"), (good, g[4])
        for b in bads:
            assert (POOL[b][4] == "Y") == (mode == "not"), (b, POOL[b][4])
        names = [noun(g[0])] + [noun(POOL[b][0]) for b in bads]
        assert len(set(names)) == 4, names
        pos = spots.next()
        bads = bads[:]
        rnd.shuffle(bads)
        keys = bads[:pos] + [good] + bads[pos:]
        assert tuple(keys) not in used
        used.add(tuple(keys))
        items = [(POOL[k][1], [dash_seg(POOL[k][1], POOL[k][2], POOL[k][3])]) for k in keys]
        svg = panel_svg(items, "four shapes A to D with dashed lines")
        L = "ABCD"[pos]
        if mode == "is":
            others = "; ".join("%s: %s" % ("ABCD"[j], WHY[POOL[k][4]]) for j, k in enumerate(keys) if j != pos)
            qs = fig(svg) + "Which dashed line <b>is</b> a line of symmetry?"
            e = "Imagine folding each shape on its dashed line. Only in <b>%s</b> does one half fit exactly on the other. Others: %s." % (L, others)
        else:
            qs = fig(svg) + "Which dashed line is <b>not</b> a line of symmetry?"
            why = {"N2": "the line splits the %s into 2 equal parts, but they do not fit when folded",
                   "N1": "the line is not through the middle of the %s, so one part is bigger"}[g[4]] % noun(g[0])
            e = "In <b>%s</b> %s. In the other 3 pictures the halves fold exactly onto each other." % (L, why)
        if extra_rect and extra_rect in keys and good != extra_rect:
            e += " Remember: the diagonal of a rectangle splits it in half, but it is not a line of symmetry."
        out.append(mcq_fixed(qs, ["A", "B", "C", "D"], pos, e))
    return out


def set_is_line(rnd):
    its = []
    r = shp("rectangle")
    rd = math.degrees(math.atan2(76, 132))
    tr = shp("tall rectangle")
    td = math.degrees(math.atan2(112, 70))
    singles = [
        it("rectangle", 90), it("square", 90, 0.3), it("isosceles triangle", 90), ("rectangle", r, center(r), rd),
        it("regular pentagon", 90), it("isosceles triangle", 0, 0.5), it("regular hexagon", 90),
        it("isosceles trapezium", 0, 0.5), it("rhombus", 0), it("parallelogram", 90), ("tall rectangle", tr, center(tr), -td),
        it("square", 45), it("kite", 0, 36 / 124.0), it("regular octagon", 45), it("ellipse", 35),
        it("equilateral triangle", 0, 0.5),
    ]
    kinds = []
    for name, F, p, a in singles:
        its.append(line_q(name, F, p, a, rnd))
        kinds.append(split_kind(F, p, a))
    assert kinds.count("Y") == 7 and kinds.count("N1") == 5 and kinds.count("N2") == 4, kinds

    P = shp("parallelogram")
    pa = P[0]["pts"]
    pd = math.degrees(math.atan2(pa[2][1] - pa[0][1], pa[2][0] - pa[0][0]))
    POOL = pool_kinds({
        "sq_h": it("square", 0), "sq_d": it("square", 135), "rect_v": it("rectangle", 90), "trect_h": it("tall rectangle", 0),
        "eq_v": it("equilateral triangle", 90), "iso_v": it("isosceles triangle", 90), "kite_v": it("kite", 90),
        "rh_h": it("rhombus", 0), "trap_v": it("isosceles trapezium", 90), "hex_v": it("regular hexagon", 90),
        "oct_h": it("regular octagon", 0), "pent_v": it("regular pentagon", 90), "circ": it("circle", 60),
        "semi_v": it("semicircle", 90), "heart_v": it("heart", 90),
        "rect_d": ("rectangle", r, center(r), rd), "para_d": ("parallelogram", P, center(P), pd),
        "para_v": it("parallelogram", 90), "para_h": it("parallelogram", 0), "sq_off": it("square", 90, 0.3),
        "trect_off": it("tall rectangle", 0, 0.3), "iso_h": it("isosceles triangle", 0, 0.5),
        "trap_h": it("isosceles trapezium", 0, 0.5), "kite_h": it("kite", 0, 36 / 124.0),
        "hex_off": it("regular hexagon", 0, 0.3), "ell_s": it("ellipse", 30),
    })
    plans = [("is", ("rect_v", ["para_d", "kite_h", "hex_off"])), ("not", ("rect_d", ["sq_d", "trap_v", "circ"])),
             ("not", ("para_v", ["kite_v", "oct_h", "heart_v"])), ("is", ("trap_v", ["rect_d", "iso_h", "sq_off"]))]
    its += panel_qs(plans, POOL, rnd, extra_rect="rect_d")
    assert len(its) == 20
    return {"title": "Is the dashed line a line of symmetry?", "items": its}


# ============================================================ set 2: how many lines of symmetry?
COUNT_Q = [
    ("rectangle", "a rectangle", ["4", "1", "0"],
     "A rectangle has <b>2</b> lines of symmetry: up and down, and across, through the middles of the sides. "
     "A diagonal splits it into 2 equal triangles, but they do not fit when folded, so the diagonals do not count."),
    ("square", "a square", ["2", "8", "1"],
     "A square has <b>4</b> lines of symmetry: one up and down, one across and 2 along the diagonals, from corner to corner. "
     "Students often forget the diagonals."),
    ("isosceles triangle", "an isosceles triangle (2 equal sides)", ["3", "2", "0"],
     "Only the line from the top corner to the middle of the bottom side works: <b>1</b> line."),
    ("equilateral triangle", "an equilateral triangle (3 equal sides)", ["1", "6", "0"],
     "It is a regular shape with 3 sides. Each line of symmetry goes from a corner to the middle of the side opposite. "
     "3 corners, so <b>3</b> lines. Do not stop at the up-and-down line."),
    ("scalene triangle", "a scalene triangle (no equal sides)", ["1", "3", "2"],
     "The 3 sides are all different lengths, so no fold makes the halves fit. <b>0</b> lines of symmetry."),
    ("circle", "a circle", ["4", "2", "0"],
     "Any straight line through the centre of a circle is a line of symmetry. You could never draw them all, so a circle "
     "has <b>infinitely many</b>."),
    ("kite", "a kite", ["2", "0", "4"],
     "Only the line from the top corner to the bottom corner works, so a kite has <b>1</b> line of symmetry."),
    ("rhombus", "a rhombus", ["4", "1", "0"],
     "This rhombus (not a square) has <b>2</b> lines of symmetry, both from corner to corner. Lines through the middles "
     "of the sides do not work."),
    ("parallelogram", "a parallelogram", ["2", "1", "4"],
     "A parallelogram with slanting sides has <b>0</b> lines of symmetry. Its diagonals and its middle lines split it into equal "
     "halves, but none of them fit when folded."),
    ("isosceles trapezium", "an isosceles trapezium", ["2", "0", "4"],
     "Only the up-and-down line through the middles of the top and bottom works. Folding across does not, because the "
     "top is shorter than the bottom: <b>1</b> line."),
    ("regular pentagon", "a regular pentagon", ["1", "2", "10"],
     "A regular shape has as many lines of symmetry as sides. Each line goes from a corner to the middle of the side opposite. "
     "5 sides, so <b>5</b> lines."),
    ("regular hexagon", "a regular hexagon", ["3", "1", "12"],
     "A regular shape has as many lines of symmetry as sides. 3 lines join opposite corners and 3 more join the middles of "
     "opposite sides: 3 + 3 = <b>6</b> lines."),
    ("regular octagon", "a regular octagon", ["4", "1", "16"],
     "A regular shape has as many lines of symmetry as sides. 4 lines join opposite corners and 4 join the middles of "
     "opposite sides: 4 + 4 = <b>8</b> lines."),
    ("semicircle", "a semicircle", ["2", "0", INF],
     "Only the line straight up through the middle of the flat side works: <b>1</b> line. Folding across puts the curve on the "
     "flat side."),
    ("ellipse", "this oval", ["1", "4", INF],
     "An oval has <b>2</b> lines of symmetry: one across the long way and one up and down. Slanting lines do not work, "
     "because it is not a circle."),
    ("plus sign", "this cross (all 4 arms the same)", ["2", "8", "1"],
     "Up and down and across both work, and so do the 2 slanting lines through the inside corners: <b>4</b> lines, just like a square."),
]
PNAMES = {"rectangle": "rectangle", "square": "square", "isosceles triangle": "isosceles triangle",
          "parallelogram": "parallelogram", "equilateral triangle": "equilateral triangle", "rhombus": "rhombus",
          "regular hexagon": "regular hexagon", "regular pentagon": "regular pentagon", "regular octagon": "regular octagon",
          "isosceles trapezium": "trapezium", "kite": "kite", "scalene triangle": "scalene triangle"}


COUNT_USE = ["rectangle", "square", "isosceles triangle", "equilateral triangle", "scalene triangle", "kite", "rhombus",
             "parallelogram", "isosceles trapezium", "regular hexagon", "circle"]
LETTER_COUNT = [
    ("A", ["2", "0", "3"],
     "Fold A straight down the middle and the 2 slanting sides match. Folded across, the point would land on the open "
     "bottom. So A has <b>1</b> line of symmetry."),
    ("H", ["1", "4", "0"],
     "Fold H up and down and the 2 posts match. Fold it across and the top lands on the bottom. <b>2</b> lines. "
     "Do not stop after finding the vertical line."),
    ("F", ["1", "2", "4"],
     "Folded up and down, the arms of F point the wrong way. Folded across, the top arm has no partner at the bottom. "
     "<b>0</b> lines."),
    ("S", ["1", "2", "4"],
     "S looks the same when you turn it upside down, but that is a turn, not a fold. No fold makes the halves match: "
     "<b>0</b> lines."),
]


def set_count(rnd):
    its = []
    for name, desc, wrong, e in COUNT_Q:
        if name not in COUNT_USE:
            continue
        F = shp(name)
        n = LINES[name]
        right = INF if n == INF else str(n)
        its.append(mcq(fig(single_svg(F, label=noun(name).replace("regular ", ""))) +
                       "How many lines of symmetry does %s have?" % desc, right, wrong, e, rnd))
    assert len(its) == len(COUNT_USE)
    for ch, wrong, e in LETTER_COUNT:
        n = nlines(letter(ch))
        assert str(n) not in wrong
        its.append(mcq(fig(single_svg(letter(ch), bw=60, bh=80, label="capital letter " + ch)) +
                       "How many lines of symmetry does the capital letter %s have?" % ch, str(n), wrong, e, rnd))
    panels = [
        ("Which shape has exactly <b>3</b> lines of symmetry?", "equilateral triangle", ["isosceles triangle", "square", "rectangle"]),
        ("Which shape has <b>no</b> lines of symmetry?", "parallelogram", ["rectangle", "rhombus", "kite"]),
    ]
    spots = Spots(rnd)
    for qs, good, bads in panels:
        pos = spots.next()
        bads = bads[:]
        rnd.shuffle(bads)
        keys = bads[:pos] + [good] + bads[pos:]
        cnt = [LINES[k] for k in keys]
        assert sum(1 for c in cnt if c == LINES[good]) == 1, (keys, cnt)
        svg = panel_svg([(shp(k), []) for k in keys], "four shapes A to D")
        e = "Count the lines of symmetry of each shape: " + ", ".join(
            "%s (%s) %s" % ("ABCD"[j], PNAMES[k], lines_word(LINES[k])) for j, k in enumerate(keys)) + \
            ". So the answer is <b>%s</b>." % "ABCD"[pos]
        its.append(mcq_fixed(fig(svg) + qs, ["A", "B", "C", "D"], pos, e))
    for qs, good, bads, e0 in (LETTER_PANELS[0], LETTER_PANELS[2]):
        its.append(panel_letters(qs, good, bads, e0, spots, rnd, letter, axis_test(qs), "four letters in a row"))
    hw = lambda w: all(KIND[c] in "hb" for c in w)
    assert hw("CODE") and not any(hw(w) for w in ("TOY", "MOON", "BOAT"))
    its.append(mcq("Mei Ling writes 4 words in capital letters. Which word has a <b>horizontal</b> line of symmetry through the whole word?",
                   "CODE", ["TOY", "MOON", "BOAT"],
                   "C, O, D and E each have a horizontal line of symmetry, so a fold across the middle of CODE works. "
                   "TOY, MOON and BOAT each have a letter that does not (T, Y, M, N, A).", rnd))
    assert len(its) == 20
    return {"title": "How many lines of symmetry? Shapes and letters", "items": its}


# ============================================================ set 3: complete the figure on a grid
def options(half, line, cols, rows, rnd, kinds):
    full = frozenset(half | {mir(x, line) for x in half})
    out = {"ok": full}
    other = sorted(full - half)
    for k in kinds:
        if k == "slide":
            d = int(line[1])
            if line[0] == "v":
                s = frozenset(half | {(c + d, r) for c, r in half})
            else:
                s = frozenset(half | {(c, r + d) for c, r in half})
        elif k == "turn":
            s = frozenset(half | {(cols - 1 - c, rows - 1 - r) for c, r in half})
        elif k == "wrongway":
            d = int(line[1])
            if line[0] == "v":
                s = frozenset(half | {(c + d, rows - 1 - r) for c, r in half})
            else:
                s = frozenset(half | {(cols - 1 - c, r + d) for c, r in half})
        elif k == "moved":
            s = None
            cand = other[:]
            rnd.shuffle(cand)
            for x in cand:
                for dc, dr in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    y = (x[0] + dc, x[1] + dr)
                    if (0 <= y[0] < cols and 0 <= y[1] < rows and y not in full and mir(y, line) not in full
                            and y != mir(y, line) and frozenset((full - {x}) | {y}) not in out.values()):
                        s = frozenset((full - {x}) | {y})
                        break
                if s:
                    break
        elif k == "missing":
            cand = [x for x in other if mir(x, line) != x and frozenset(full - {x}) not in out.values()]
            s = frozenset(full - {rnd.choice(cand)})
        out[k] = s
    for k, s in out.items():
        assert all(0 <= c < cols and 0 <= r < rows for c, r in s), k
        assert gsym(s, line) == (k == "ok"), k
    assert len(set(out.values())) == len(out)
    return out


OPT_WHY = {"slide": "the half was slid across, not flipped",
           "turn": "the half was turned upside down, not flipped",
           "moved": "one square is in the wrong place", "missing": "one square is missing"}
WRONGWAY = {"v": "the half was flipped upside down instead of across the line",
            "h": "the half was flipped from left to right instead of across the line"}

V_HALVES = [
    ["..#", ".##", "#.#", "###", "..#"],
    ["#..", "##.", "###", ".#.", ".##"],
    ["...#", "..##", ".###", "#..#", "...#"],
    ["#..#", ".###", "..##", ".#.#", "##.#"],
    [".#.", "###", "#.#", "..#", ".##"],
    ["##..", ".##.", "..##", ".#.#", "...#"],
    ["...#", ".###", "##.#", "...#", "..##"],
    ["..#", "###", ".##", "..#", ".#."],
]
H_HALVES = [
    ["...#..", "..###.", "#####."],
    ["#.....", "###...", ".#####"],
    ["..##..", "#.#..#", "######"],
    [".#....", "##.##.", "######"],
    [".#.#..", "#####.", "..####"],
    ["...##.", ".####.", "###..#"],
    ["..#..#", ".##.##", "######"],
    ["....##", "..###.", "######"],
]
WRONG_SETS = [["slide", "turn", "missing"], ["slide", "wrongway", "moved"], ["turn", "wrongway", "missing"],
              ["slide", "wrongway", "missing"], ["turn", "wrongway", "moved"], ["slide", "turn", "moved"],
              ["wrongway", "moved", "missing"], ["slide", "wrongway", "turn"]]
COUNTS = [
    ("v", ["...#", "..##", ".#.#", "####", "#..."], "all"),
    ("h", ["..#...", ".##...", "####..", "#.####"], "all"),
    ("v", [".#..", "####", "..##", ".#.#", "...#"], "more"),
    ("h", ["....#.", "...##.", "#..###", "######"], "more"),
]


def grid_q(kind, h, rnd, spots, wrongs):
    wrongs = list(wrongs)
    if kind == "v":
        w = len(h[0])
        cols, rows, line = 2 * w, len(h), ("v", w)
    else:
        cols, rows, line = len(h[0]), 2 * len(h), ("h", len(h))
    half = cells_of(h)
    opts = options(half, line, cols, rows, rnd, wrongs)
    pos = spots.next()
    rnd.shuffle(wrongs)
    keys = wrongs[:pos] + ["ok"] + wrongs[pos:]
    cs = 12 if cols >= 8 else 14
    svg = grid_panel(cols, rows, [opts[k] for k in keys], line, cs, "four grid pictures A to D with a dashed line of symmetry")
    side = {"v": "left", "h": "top"}[kind]
    qs = (fig(svg) + "The dashed line is a line of symmetry. The %s half is the same in all 4 pictures. "
          "In which picture is the symmetric figure completed correctly?" % side)
    rule = {"v": "Each shaded square needs a partner in the same row, the same number of squares from the line on the other side.",
            "h": "Each shaded square needs a partner in the same column, the same number of squares from the line on the other side."}[kind]
    why = dict(OPT_WHY, wrongway=WRONGWAY[kind])
    others = "; ".join("%s: %s" % ("ABCD"[j], why[k]) for j, k in enumerate(keys) if k != "ok")
    e = "%s Only <b>%s</b> is a true mirror image. Others: %s." % (rule, "ABCD"[pos], others)
    return mcq_fixed(qs, ["A", "B", "C", "D"], pos, e), svg


def count_q(kind, h, ask, rnd):
    half = cells_of(h)
    line = ("v", 3.5) if kind == "v" else ("h", 3.5)
    cols, rows = (7, 5) if kind == "v" else (6, 7)
    on = [x for x in half if mir(x, line) == x]
    n, m = len(half), len(on)
    assert m >= 1 and n - m >= 2
    full = half | {mir(x, line) for x in half}
    assert gsym(full, line) and len(full) == 2 * (n - m) + m
    where = "column" if kind == "v" else "row"
    svg = grid_svg(cols, rows, half, line, 18 if kind == "v" else 16, "grid with shaded squares on one side of a dashed line of symmetry")
    side = "to the right of the line" if kind == "v" else "below the line"
    if ask == "all":
        qs = (fig(svg) + "The line of symmetry runs through the middle of a %s. Shade squares %s to make the picture "
              "symmetric. How many squares will be shaded altogether?" % (where, side))
        right = 2 * (n - m) + m
        wrong = [2 * n, 2 * (n - m), n]
        e = ("%d squares are shaded now. %d of them %s on the line, so %s own partner: count %s once. "
             "The other %d each need a partner. %d + %d + %d = <b>%d</b>."
             % (n, m, "sits" if m == 1 else "sit", "it is its" if m == 1 else "each is its", "it" if m == 1 else "them",
                n - m, n - m, n - m, m, right))
    else:
        qs = (fig(svg) + "The line of symmetry runs through the middle of a %s. How many more squares must be shaded "
              "to make the picture symmetric?" % where)
        right = n - m
        wrong = [n, 2 * n - m, m]
        e = ("Squares on the line are their own partners. %d squares are shaded and %d %s on the line, "
             "so %d − %d = <b>%d</b> more squares." % (n, m, "sits" if m == 1 else "sit", n, m, right))
    return mcq(qs, right, wrong, e, rnd)


def set_grid(rnd):
    spots = Spots(rnd)
    seen = set()
    v, h, c = [], [], []
    for i, x in enumerate(V_HALVES):
        q_, svg = grid_q("v", x, rnd, spots, WRONG_SETS[i])
        v.append(q_); assert svg not in seen; seen.add(svg)
    for i, x in enumerate(H_HALVES):
        q_, svg = grid_q("h", x, rnd, spots, WRONG_SETS[(i + 3) % 8])
        h.append(q_); assert svg not in seen; seen.add(svg)
    for kind, x, ask in COUNTS:
        c.append(count_q(kind, x, ask, rnd))
    its = v[:4] + h[:4] + v[4:] + h[4:] + c
    assert len(its) == 20
    return {"title": "Complete a symmetric figure on a square grid", "items": its}


# ============================================================ letters in a row
def row_svg(figs, names, label, cw=74):
    el = []
    H = 92
    for k, F in enumerate(figs):
        e, bb = render(F, [], 50, 70, k * cw + cw / 2.0, H / 2.0)
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 2 and bb[3] <= H - 2, (names[k], bb)
        el += e
        if k:
            el.append("<line x1='%d' y1='6' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (k * cw, k * cw, H - 6, GRAY))
    return svg_wrap(cw * len(figs), H, "".join(el), label + ": " + ", ".join(names))


LETTER_PANELS = [
    ("Which capital letter has a <b>horizontal</b> line of symmetry?", "E", "MTV",
     "Fold E across the middle and the top arm lands on the bottom arm. M, T and V have a vertical line instead."),
    ("Which capital letter has <b>no</b> line of symmetry?", "R", "HAC",
     "R has no line of symmetry: the leg at the bottom right has no partner. H has 2, A has a vertical one and C has a horizontal one."),
    ("Which capital letter has <b>2</b> lines of symmetry?", "O", "AEW",
     "O matches when folded up and down and when folded across. A and W have only a vertical line, and E only a horizontal one. "
     "Remember to check across as well as up and down."),
    ("Which capital letter has a <b>vertical</b> line of symmetry?", "Y", "BDC",
     "Fold Y straight down the middle and the 2 arms match. B, D and C have a horizontal line, not a vertical one."),
]
def panel_letters(qs, good, bads, e0, spots, rnd, mk, test, label):
    pos = spots.next()
    bads = list(bads)
    rnd.shuffle(bads)
    keys = bads[:pos] + [good] + bads[pos:]
    ok = [k for k in keys if test(axes(mk(k)))]
    assert ok == [good], (qs, keys)
    return mcq_fixed(fig(row_svg([mk(k) for k in keys], keys, label)) + qs, keys, pos, e0)


def axis_test(qs):
    if "no</b>" in qs:
        return lambda a: a == []
    if "horizontal" in qs:
        return lambda a: 0.0 in a
    if "vertical" in qs:
        return lambda a: 90.0 in a
    return lambda a: len(a) == 2




# ============================================================ set 1: is the figure symmetric?
def pinwheel():
    P = [(-20, -20), (20, -20), (20, 20), (-20, 20)]
    T = [(30, -48), (48, 30), (-30, 48), (-48, -30)]
    pts = []
    for k in range(4):
        pts += [P[k], T[k]]
    return pts


SHAPES.update({
    "pinwheel": lambda: S1(pinwheel()),
    "right trapezium": lambda: S1([(-50, -35), (15, -35), (50, 35), (-50, 35)]),
    "four-sided shape": lambda: S1([(-50, -30), (40, -45), (55, 35), (-35, 40)]),
    "turned semicircle": lambda: S1(rot(semicircle(62), 90)),
})
LINES.update({"pinwheel": 0, "right trapezium": 0, "four-sided shape": 0, "turned semicircle": 1})
FNAME = {"heart": "heart", "kite": "kite", "isosceles trapezium": "isosceles trapezium", "arrow": "arrow",
         "turned isosceles triangle": "isosceles triangle on its side", "turned semicircle": "semicircle on its side",
         "L shape": "L shape", "isosceles right-angled triangle": "right-angled triangle with 2 equal sides",
         "turned kite": "tilted kite", "parallelogram": "parallelogram", "scalene triangle": "scalene triangle",
         "pinwheel": "pinwheel shape", "right-angled triangle": "right-angled triangle", "right trapezium": "right-angled trapezium",
         "four-sided shape": "four-sided shape", "square": "square", "rectangle": "rectangle",
         "isosceles triangle": "isosceles triangle", "rhombus": "rhombus", "regular hexagon": "hexagon",
         "semicircle": "semicircle", "equilateral triangle": "equilateral triangle", "circle": "circle",
         "plus sign": "cross"}
SYM_CH = ["Yes, up and down", "Yes, across", "Yes, slanting", "No, not symmetric"]
SYM_SINGLE = [
    ("heart", "Fold the heart straight down the middle: the two bumps match. So it is symmetric, with an "
              "<b>up-and-down</b> line of symmetry. Folded across, the point would land on the bumps."),
    ("arrow", "Fold the arrow along a line across its middle, from the tail to the tip: the top half lands on the bottom half. "
              "Its line of symmetry goes <b>across</b>."),
    ("L shape", "Fold the L along the slanting line from its outside corner to its inside corner: the two arms match. "
                "Its line of symmetry is <b>slanting</b>. Folds up and down or across do not work."),
    ("parallelogram", "Try every fold: up and down, across and corner to corner. The slanting sides never land on each other, "
                      "so a parallelogram is <b>not symmetric</b>."),
    ("kite", "Fold the kite from its top corner to its bottom corner: the two sides match. Its line of symmetry goes "
             "<b>up and down</b>."),
    ("turned isosceles triangle", "This isosceles triangle lies on its side. Fold it across, from its point to the middle "
                                  "of the opposite side: the halves match. The line goes <b>across</b>."),
    ("isosceles right-angled triangle", "The two short sides are equal. Fold from the right angle to the middle of the long "
                                        "side: the halves match. That line is <b>slanting</b>."),
    ("pinwheel", "The pinwheel looks the same after a quarter turn, but that is a turn, not a fold. No fold makes its blades "
                 "match, so it is <b>not symmetric</b>."),
    ("isosceles trapezium", "Fold the trapezium straight down the middle: the two slanting sides match. Folded across, the "
                            "short top would land on the long bottom. The line goes <b>up and down</b>."),
    ("turned semicircle", "This semicircle stands on its side. Fold it across the middle: the top half of the curve lands on "
                          "the bottom half. The line goes <b>across</b>."),
    ("turned kite", "This kite is tilted. Its line of symmetry still joins the two corners where the equal sides meet, so the "
                    "line is <b>slanting</b>. A line of symmetry can go in any direction."),
    ("scalene triangle", "All 3 sides have different lengths, so no fold makes two halves match. It is <b>not symmetric</b>."),
]
SYM_PANELS = [
    ("is", "heart", ["parallelogram", "scalene triangle", "pinwheel"]),
    ("not", "pinwheel", ["square", "isosceles triangle", "rectangle"]),
    ("is", "L shape", ["right-angled triangle", "right trapezium", "parallelogram"]),
    ("not", "parallelogram", ["rhombus", "rectangle", "kite"]),
    ("is", "isosceles right-angled triangle", ["scalene triangle", "pinwheel", "right trapezium"]),
    ("not", "right trapezium", ["isosceles trapezium", "semicircle", "arrow"]),
    ("is", "turned kite", ["parallelogram", "right-angled triangle", "four-sided shape"]),
    ("not", "scalene triangle", ["equilateral triangle", "regular hexagon", "plus sign"]),
]


def axis_dir(F):
    a = axes(F)
    assert a != INF and len(a) <= 1, a
    if not a:
        return 3
    return 0 if abs(a[0] - 90) < 1e-6 else 1 if abs(a[0]) < 1e-6 or abs(a[0] - 180) < 1e-6 else 2


def and_list(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def set_symmetric(rnd):
    its = []
    got = [0] * 4
    for name, e in SYM_SINGLE:
        F = shp(name)
        k = axis_dir(F)
        got[k] += 1
        qs = (fig(single_svg(F, label=FNAME[name])) +
              "Is this figure symmetric? If it is, which way does its line of symmetry go?")
        its.append(mcq_fixed(qs, SYM_CH, k, e))
    assert got == [3, 3, 3, 3], got
    spots = Spots(rnd)
    for mode, good, bads in SYM_PANELS:
        assert (LINES[good] != 0) == (mode == "is"), good
        for b in bads:
            assert (LINES[b] != 0) == (mode == "not"), b
        pos = spots.next()
        bads = bads[:]
        rnd.shuffle(bads)
        keys = bads[:pos] + [good] + bads[pos:]
        svg = panel_svg([(shp(k), []) for k in keys], "four figures A to D")
        L = "ABCD"[pos]
        if mode == "is":
            qs = fig(svg) + "Which figure <b>is</b> symmetric?"
            e = ("Only <b>%s</b> (the %s) can be folded so that both halves match exactly. The %s cannot."
                 % (L, FNAME[good], and_list([FNAME[k] for k in keys if k != good])))
        else:
            qs = fig(svg) + "Which figure is <b>not</b> symmetric?"
            e = ("<b>%s</b> (the %s) has no line of symmetry: no fold makes its halves match. The %s each have at least 1 line."
                 % (L, FNAME[good], and_list([FNAME[k] for k in keys if k != good])))
        its.append(mcq_fixed(qs, ["A", "B", "C", "D"], pos, e))
    order = its[:6] + its[12:16] + its[6:12] + its[16:]
    assert len(order) == 20
    return {"title": "Is the figure symmetric?", "items": order}


# ============================================================ set 5: symmetry in real life
SG_RED = "#e1262d"
GOLD = "#e8b828"


def star(n, R=54, r=24, c=(0, 0), start=-90):
    pts = []
    for i in range(2 * n):
        rr = R if i % 2 == 0 else r
        t = math.radians(start + 180.0 * i / n)
        pts.append((c[0] + rr * math.cos(t), c[1] + rr * math.sin(t)))
    return pts


def sg_flag():
    F = [Poly([(-60, -40), (60, -40), (60, 0), (-60, 0)], SG_RED, SG_RED, 1),
         Poly([(-60, 0), (60, 0), (60, 40), (-60, 40)], WHITE, WHITE, 1),
         Circ((-38, -20), 14, WHITE, WHITE, 1), Circ((-33, -20), 13, SG_RED, SG_RED, 1)]
    for k in range(5):
        t = math.radians(-90 + 72 * k)
        F.append(Poly(star(5, 3.6, 1.5, (-25 + 7 * math.cos(t), -20 + 7 * math.sin(t))), WHITE, WHITE, 0.5))
    F.append(Poly(rect(120, 80), "none", INK, 1.5))
    return F


def star_fruit():
    return [Poly(star(5, 56, 28), "#f2d14a", "#a88412", 3), Poly(star(5, 22, 11), "#fbe99a", "#a88412", 2),
            Circ((0, 0), 4, "#7a5a10", "#7a5a10", 1)]


def sign_stop():
    return [Poly(reg(8, 56, -90 + 22.5), RED, RED, 2), Poly(reg(8, 49, -90 + 22.5), "none", WHITE, 3)]


def sign_give_way():
    return [Poly(reg(3, 62, 90), RED, RED, 2), Poly(reg(3, 38, 90), WHITE, WHITE, 1)]


def badminton_court():
    w, h = 130, 60
    L = lambda pts, sc=WHITE, sw=2.5: Line(pts, sc, sw)
    return [Poly(rect(w + 16, h + 16), "#2e7d4f", "#2e7d4f", 1), Poly(rect(w, h), SHADE, WHITE, 2.5),
            L([(-w / 2, -24), (w / 2, -24)]), L([(-w / 2, 24), (w / 2, 24)]),
            L([(-20, -h / 2), (-20, h / 2)]), L([(20, -h / 2), (20, h / 2)]),
            L([(-57, -h / 2), (-57, h / 2)]), L([(57, -h / 2), (57, h / 2)]),
            L([(-w / 2, 0), (-20, 0)]), L([(20, 0), (w / 2, 0)]),
            L([(0, -h / 2 - 4), (0, h / 2 + 4)], INK, 3)]


def red_packet():
    return [Poly(rect(70, 110), SG_RED, "#9e1c12", 2.5), Line([(-35, -55), (0, -30), (35, -55)], "#9e1c12", 2.5),
            Circ((0, 8), 16, GOLD, "#a88412", 2)]


def fish():
    body = Poly(ellipse(46, 18, 48), "#8fb8de", "#2f5f8f", 2.5)
    tail = Poly([(40, 0), (64, -18), (58, 0), (64, 18)], "#8fb8de", "#2f5f8f", 2.5)
    fin = Poly([(-6, -17), (8, -30), (14, -16)], "#8fb8de", "#2f5f8f", 2.5)
    eye = Circ((-30, -5), 3.5, INK, INK, 1)
    return [fin, tail, body, eye]


def rangoli():
    F = []
    for k in range(6):
        F.append(Poly([(x, y - 27) for x, y in ellipse(10, 20, 40)], "#e0823a", "#a3521c", 2))
        F[-1]["pts"] = rot(F[-1]["pts"], 60 * k)
    F.append(Circ((0, 0), 9, YELLOW, "#a3521c", 2))
    for k in range(6):
        t = math.radians(-60 + 60 * k)
        F.append(Circ((44 * math.cos(t), 44 * math.sin(t)), 5, RED, RED, 1))
    return F


OBJ = [
    (butterfly, "How many lines of symmetry does this butterfly picture have?", "butterfly", 1, ["2", "0", "4"],
     "Only the line straight down the body works: each wing lands on the wing opposite. Folded across, the big top wings "
     "would land on the small bottom wings. <b>1</b> line."),
    (leaf, "Xin Yi draws a leaf she found in the school garden. How many lines of symmetry does her drawing have?",
     "leaf", 1, ["2", "0", "4"],
     "Fold it along the middle vein: the two sides of the leaf match. Folded across, the stem has nothing to match. <b>1</b> line."),
    (sg_flag, "The flag of Singapore is red on top and white below, with a white crescent moon and 5 white stars. "
              "How many lines of symmetry does it have?", "flag of Singapore", 0, ["1", "2", "4"],
     "Fold it up and down: the crescent and stars land on the plain red part. Fold it across: red lands on white. "
     "So the flag has <b>0</b> lines of symmetry, even though it is a rectangle."),
    (star_fruit, "Ahmad cuts a slice of star fruit. It has 5 points that are all the same. How many lines of symmetry does it have?",
     "slice of star fruit", 5, ["10", "1", "4"],
     "Each line of symmetry runs from one point, through the centre, to the gap between the 2 points opposite. "
     "5 points, so <b>5</b> lines."),
    (sign_stop, "A stop sign in Singapore has this shape. Without the word STOP, how many lines of symmetry does it have?",
     "red octagon road sign", 8, ["4", "2", "1"],
     "It is a regular octagon: 4 lines join opposite corners and 4 join the middles of opposite sides. <b>8</b> lines. "
     "(With the word on it, it would have none.)"),
    (sign_give_way, "A give way sign is a triangle pointing down like this. Without any words, how many lines of symmetry does it have?",
     "red triangle sign pointing down", 3, ["1", "6", "2"],
     "It is an equilateral triangle, just upside down. Each line of symmetry goes from a corner to the middle of the side "
     "opposite: <b>3</b> lines."),
    (badminton_court, "This is a badminton court seen from above, with the net across the middle. How many lines of symmetry does it have?",
     "badminton court seen from above", 2, ["4", "1", "0"],
     "Fold it along the net: each half of the court matches. Fold it the long way: the top lands on the bottom. "
     "<b>2</b> lines. The corner-to-corner lines do not work, because the court is not a square."),
    (red_packet, "Siti’s red packet for Chinese New Year has a flap at the top and a gold circle. How many lines of symmetry does it have?",
     "red packet with a flap", 1, ["2", "4", "0"],
     "Fold it up and down through the middle: the flap and the circle match. Folded across, the flap at the top has no partner "
     "at the bottom. So it has <b>1</b> line, not 2 like a plain rectangle."),
    (fish, "This fish is drawn from the side. How many lines of symmetry does it have?",
     "fish seen from the side", 0, ["1", "2", "4"],
     "Folded the long way, the fin on top has nothing below it to match. Folded up and down, the head would land on the "
     "tail. <b>0</b> lines."),
    (rangoli, "Kavya draws this rangoli pattern for Deepavali. It has 6 petals and 6 dots. How many lines of symmetry does it have?",
     "rangoli pattern with 6 petals", 6, ["3", "12", "1"],
     "3 lines go along pairs of opposite petals, and 3 more go between the petals through the dots. 3 + 3 = <b>6</b> lines."),
]
WORDS = [
    ("Siti has a square sheet of origami paper. In how many different ways can she fold it in half so that the two halves match exactly?",
     "4", ["2", "8", "1"],
     "A square has 4 lines of symmetry: up and down, across, and the 2 diagonals. So there are 4 ways."),
    ("Wei Ming folds his beach towel at East Coast Park from one corner to the opposite corner. The towel is 2 m long and 1 m wide. "
     "Do the two halves match?",
     "No, the corners stick out", ["Yes, the halves are equal", "Yes, every fold works", "No, it has no lines"],
     "The diagonal splits the towel into 2 equal triangles, but they do not fit on top of each other, because the towel is "
     "not a square. A rectangle has only 2 lines of symmetry."),
    ("A P4 class makes a plain rectangular banner for National Day. Ryan says it has 4 lines of symmetry. "
     "How many does it really have?", "2", ["4", "1", "0"],
     "A rectangle that is not a square has 2 lines: up and down, and across. Ryan counted the diagonals, but they do not work."),
    ("Priya traces a pattern block shaped like a regular hexagon. How many lines of symmetry does it have?",
     "6", ["3", "1", "2"],
     "A regular shape has as many lines of symmetry as sides. 6 sides, so 6 lines: 3 through opposite corners and 3 through "
     "the middles of opposite sides."),
    ("Jun Jie draws a triangle with 3 equal sides. He finds the up-and-down line of symmetry and stops. How many lines does it have?",
     "3", ["1", "2", "6"],
     "A triangle with 3 equal sides has 3 lines of symmetry, one from each corner to the middle of the opposite side. "
     "Look for slanting lines, not only vertical ones."),
    ("Hafiz has a round paper plate from the hawker centre. How many different fold lines will make the two halves match?",
     INF, ["4", "2", "0"],
     "Every line through the centre of a circle is a line of symmetry, so there are infinitely many. Up and down, across "
     "and the 2 diagonals are just 4 of them."),
    ("Chloe folds a sheet of red paper in half, cuts a shape along the fold and opens it out for a Chinese New Year "
     "decoration. What must be true?",
     "The fold is a line of symmetry", ["It has no lines of symmetry", "It has exactly 2 lines", "One half is bigger"],
     "Both halves were cut at the same time, so each is the mirror image of the other. The fold is always a line of symmetry. "
     "The shape might have other lines too, but it does not have to."),
    ("Arjun is completing a symmetric figure on a square grid. A shaded square is 3 squares to the left of the line of symmetry. "
     "Where does its partner go?", "3 squares to the right of the line",
     ["3 squares from the right edge", "6 squares to the right of the line", "Right next to the line"],
     "A partner is the same distance from the line on the other side: 3 squares to the right of the line. Count from the line, "
     "not from the edge of the grid."),
    ("Nurul wants a figure with exactly 1 line of symmetry for her art lesson. Which shape should she choose?",
     "An isosceles triangle", ["A square", "A rectangle", "A parallelogram"],
     "An isosceles triangle (with only 2 equal sides) has 1 line of symmetry, down the middle. A square has 4, a rectangle has 2, "
     "and a parallelogram has 0."),
    ("Zhi Hao says a regular pentagon has only 1 line of symmetry, because he only looks for up-and-down lines. How many does it have?",
     "5", ["1", "2", "10"],
     "A regular pentagon has 5 sides, so it has 5 lines of symmetry, one from each corner to the middle of the opposite side. "
     "Only 1 of them is vertical."),
]


def set_world(rnd):
    its = []
    for make, qs, label, n, wrong, e in OBJ:
        F = expect(make(), n, label)
        its.append(mcq(fig(single_svg(F, label=label)) + qs, str(n), wrong, e, rnd))
    assert LINES["isosceles triangle"] == 1 and LINES["square"] == 4 and LINES["rectangle"] == 2 and LINES["parallelogram"] == 0
    assert LINES["regular hexagon"] == 6 and LINES["regular pentagon"] == 5 and LINES["equilateral triangle"] == 3
    for qs, right, wrong, e in WORDS:
        its.append(mcq(qs, right, wrong, e, rnd))
    assert len(its) == 20
    return {"title": "Symmetry in real life: flags, signs and patterns", "items": its}


# ============================================================ lesson
def body_html():
    r = shp("rectangle")
    rd = math.degrees(math.atan2(76, 132))
    f1 = strip_svg([(r, [dash_seg(r, center(r), 90)], "Line of symmetry"),
                    (r, [dash_seg(r, center(r), rd)], "Not a line of symmetry")],
                   "a rectangle with an up-and-down dashed line and a rectangle with a diagonal dashed line", cw=190)
    f0 = strip_svg([(shp("heart"), [], "Symmetric"), (shp("L shape"), [], "Symmetric"),
                    (shp("parallelogram"), [], "Not symmetric"), (shp("pinwheel"), [], "Not symmetric")],
                   "a heart and an L shape that are symmetric, and a parallelogram and a pinwheel shape that are not", cw=136)
    shapes = ["rectangle", "square", "equilateral triangle", "parallelogram"]
    f2 = strip_svg([(shp(k), all_axis_segs(shp(k)), lines_word(LINES[k])) for k in shapes],
                   "a rectangle with 2 lines of symmetry, a square with 4, an equilateral triangle with 3 and a parallelogram with 0")
    half = cells_of(["..#", ".##", "#.#", "###", "..#"])
    full = half | {mir(x, ("v", 3)) for x in half}
    f4 = grid_svg(6, 5, full, ("v", 3), 24, "a grid figure completed across a vertical dashed line of symmetry", light=full - half)
    half2 = cells_of(["...#..", "..###.", "#####."])
    full2 = half2 | {mir(x, ("h", 3)) for x in half2}
    f4b = grid_svg(6, 6, full2, ("h", 3), 20, "a grid figure completed across a horizontal dashed line of symmetry", light=full2 - half2)
    lets = ["A", "E", "H", "F"]
    f5 = strip_svg([(letter(c), all_axis_segs(letter(c)), lines_word(nlines(letter(c)))) for c in lets],
                   "the letters A, E, H and F with their lines of symmetry", cw=110, box=(56, 76))
    return (
        "<h2>What is a symmetric figure?</h2>"
        "<p>A figure is <b>symmetric</b> if you can fold it along a line so that the two halves match exactly. "
        "That fold line is called a <b>line of symmetry</b>. Each half is the mirror image of the other.</p>"
        "<figure class='sn-fig'>" + f0 +
        "<figcaption>The heart and the L shape can be folded into matching halves. The parallelogram and the pinwheel "
        "cannot, even though they look the same when turned.</figcaption></figure>"
        "<h2>Is the line a line of symmetry?</h2>"
        "<p>Fold a paper copy along the line, or stand a small mirror on it. The two parts must be the same size "
        "<b>and</b> land exactly on each other.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Fold the first rectangle along the dashed line: the halves match. The diagonal also splits the rectangle "
        "into 2 equal triangles, but when you fold, the corners stick out. So it is not a line of symmetry.</figcaption></figure>" +
        ex("Worked example", "Is the diagonal of a rectangle (not a square) a line of symmetry?",
           "Fold along the diagonal. The two triangles are the same size, but the corners do not land on each other.",
           "No. A rectangle has 2 lines of symmetry.") +
        "<h2>Count every line</h2>"
        "<p>Try every way to fold: up and down, across and slanting. A figure can have many lines of symmetry, one, or none.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>A rectangle has only 2 lines. A square has 4 (2 are diagonals). An equilateral triangle has 3. "
        "A parallelogram has none.</figcaption></figure>" +
        table(["Shape", "Lines of symmetry"], [
            ["Square", "4"], ["Rectangle (not a square)", "2"], ["Rhombus (not a square)", "2 (corner to corner)"],
            ["Parallelogram (slanting sides)", "0"], ["Equilateral triangle", "3"], ["Isosceles triangle", "1"],
            ["Kite", "1"], ["Isosceles trapezium", "1"], ["Regular hexagon", "6"], ["Circle", "Infinitely many"],
        ]) +
        "<h2>Complete a symmetric figure on a square grid</h2>"
        "<p>Give every shaded square a partner on the other side of the line, the <b>same number of squares away</b> "
        "from the line. Count from the line, not from the edge of the grid. Flip the half across the line; do not slide it "
        "or flip it the other way.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>Vertical line: each partner is in the same row, the same distance from the line. The light squares are the "
        "new ones.</figcaption></figure>"
        "<figure class='sn-fig'>" + f4b +
        "<figcaption>Horizontal line: each partner is in the same column, the same distance from the line.</figcaption></figure>" +
        ex("Worked example", "A shaded square is 2 squares to the left of a vertical line of symmetry, in the top row. Where is its partner?",
           "Stay in the top row. Count 2 squares from the line on the right side.",
           "In the top row, 2 squares to the right of the line.") +
        "<h2>Letters and real life</h2>"
        "<p>Some capital letters have a vertical line, some a horizontal line, some both, and some none. Check across as well as up and down.</p>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>A has a vertical line. E has a horizontal line. H has both. F has none.</figcaption></figure>"
        "<p>Look for symmetry around you: a butterfly, a slice of star fruit, a stop sign, a badminton court, a rangoli pattern. "
        "Some things are not symmetric at all, such as the flag of Singapore.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a rectangle’s diagonals as lines of symmetry", "Fold on a diagonal: the corners stick out. A rectangle has 2"],
            ["Looking only for vertical lines", "Also fold across and on slants. A square has 4 lines, the letter E has a horizontal one"],
            ["Thinking equal halves are enough", "The halves must land exactly on each other when folded"],
            ["Sliding the half when completing a figure", "Flip it: each square goes the same distance on the other side"],
            ["Reflecting in the wrong direction", "For a vertical line, flip left to right and stay in the same row. "
                                                  "For a horizontal line, flip top to bottom and stay in the same column"],
            ["Calling “looks the same when turned” symmetric", "That is a turn. S, N and a pinwheel have 0 lines"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 symmetry?",
     "a": "In Primary 4, the MOE syllabus covers line symmetry: identifying symmetric figures, deciding whether a line is a line of symmetry, and completing a symmetric figure on a square grid. The line of symmetry is usually vertical or horizontal."},
    {"q": "How do I check if a line is a line of symmetry?",
     "a": "Fold along the line or stand a small mirror on it. If the two halves match exactly, it is a line of symmetry; two halves of the same size are not enough."},
    {"q": "Does a rectangle have 4 lines of symmetry?",
     "a": "No. A rectangle that is not a square has 2 lines of symmetry: up and down, and across. Its diagonals split it in half, but the halves do not fit when folded."},
    {"q": "What is the most common mistake when completing a symmetric figure?",
     "a": "Sliding the half or flipping it the wrong way. Each shaded square must go the same number of squares from the line on the other side, in the same row for a vertical line or the same column for a horizontal line."},
]


def gen_symmetry():
    rnd = random.Random(64815)
    sets = [set_symmetric(rnd), set_is_line(rnd), set_count(rnd), set_grid(rnd), set_world(rnd)]
    for s in sets:
        balance(s, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0] * 4
        for x in s["items"]:
            assert len(set(x["c"])) == 4, x
            pos[x["a"]] += 1
            k = x["q"] + "|" + "|".join(sorted(x["c"]))
            assert k not in seen, x["q"]
            seen.add(k)
            assert len(re.findall("<svg", x["q"])) <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "line-symmetry", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Line Symmetry",
        "seo_title": "P4 Line Symmetry Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Line symmetry",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 4: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Identifying symmetric figures; determining whether a line is a line of symmetry; completing a symmetric figure on a square grid",
        "meta_desc": "Free P4 maths practice on line symmetry: spot symmetric figures, count lines of symmetry and complete figures on a square grid. 100 questions with answers.",
        "key_big": "A line of symmetry folds a figure into two halves that match exactly.",
        "key_sub": "A rectangle has 2 lines of symmetry, not 4: its diagonals make equal halves that do not match when folded.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, grids, rows of letters) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for x in s["items"]:
            x["q"] = rx.sub("<svg data-pf='lg' ", x["q"])
    return u


if __name__ == "__main__":
    u = gen_symmetry()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(four [a-z ]+ A to D|four letters)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
