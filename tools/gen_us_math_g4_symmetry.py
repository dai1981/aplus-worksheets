# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Line Symmetry (4.G.A.3)
  python tools/gen_us_math_g4_symmetry.py
Every figure is built from exact coordinates and its lines of symmetry are found in code:
a line is a line of symmetry when reflecting every edge (with its color) across it gives exactly
the same set of edges. The number of lines given in every answer is the number found here, and
every dashed line in a question is tested the same way. Letters are drawn as strokes, not with a
font, so their symmetry is exact. Grid pictures are checked square by square.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
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
    "right isosceles triangle": lambda: S1([(-48, -48), (-48, 48), (48, 48)]),
    "right triangle": lambda: S1([(-58, -36), (-58, 36), (58, 36)]),
    "circle": lambda: [Circ((0, 0), 50)],
    "rhombus": lambda: S1(diamond(84, 128)),
    "parallelogram": lambda: S1(para(100, 70, 20)),
    "kite": lambda: S1(kite(84, 124, 36)),
    "isosceles trapezoid": lambda: S1(itrap(130, 70, 74)),
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
         "scalene triangle": 0, "right isosceles triangle": 1, "right triangle": 0, "circle": INF, "rhombus": 2,
         "parallelogram": 0, "kite": 1, "isosceles trapezoid": 1, "regular pentagon": 5,
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


def flag(parts, w=120, h=80):
    F = [Poly(rect(w, h), parts[0], INK, 1.5)]
    for pts, col in parts[1:]:
        F.append(Poly(pts, col, col, 1))
    F.append(Poly(rect(w, h), "none", INK, 1.5))
    return F


def flag_stripes():
    return flag([GREEN, (rect(120, 80 / 3.0), YELLOW)])


def flag_cross():
    return flag([GREEN, ([(-24, -40), (-8, -40), (-8, 40), (-24, 40)], WHITE),
                 ([(-60, -8), (60, -8), (60, 8), (-60, 8)], WHITE)])


def flag_band():
    return flag([GREEN, ([(-60, -40), (-36, -40), (60, 40), (36, 40)], YELLOW)])


def flag_two():
    return flag([GREEN, ([(-60, -40), (60, -40), (60, 0), (-60, 0)], BLUE)])


def sign_stop():
    return [Poly(reg(8, 56, -90 + 22.5), RED, RED, 2), Poly(reg(8, 49, -90 + 22.5), "none", WHITE, 3)]


def sign_yield():
    return [Poly(reg(3, 62, 90), RED, RED, 2), Poly(reg(3, 36, 90), WHITE, WHITE, 1)]


def sign_diamond():
    return [Poly(reg(4, 56), YELLOW, INK, 2), Poly(reg(4, 48), "none", INK, 2)]


def pinwheel():
    blade = [(0, 0), (0, -50), (30, -30)]
    return [Poly(rot(blade, 90 * i), FILL if i % 2 == 0 else SHADE2, GREEN, 2.5) for i in range(4)] + [Circ((0, 0), 5, INK, INK, 1)]


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
    """SVG elements for figure F (and dashed segments) scaled to fit a bw x bh box centered at (cx, cy)."""
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
    return (r, c)


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


# ============================================================ set 1: is it a line of symmetry?
Y_ = "Yes, the halves match"
N1_ = "No, one half is bigger"
N2_ = "No, same size but they do not match"
T_ = "Yes, it cuts it in half"
U_ = "No, it must go up and down"


def line_q(name, F, p, a, rnd):
    kind = split_kind(F, p, a)
    seg = dash_seg(F, p, a)
    noun = {"isosceles trapezoid": "trapezoid", "equilateral triangle": "triangle", "ellipse": "oval"}.get(name, name)
    pic = fig(single_svg(F, [seg], label="%s with a dashed line" % noun))
    qs = pic + "Fold the %s along the dashed line. Is the dashed line a line of symmetry?" % noun
    slant = "goes across" if abs(a) < 1e-9 else "is slanted"
    if kind == "Y":
        e = ("Fold on the line: the two halves land exactly on each other, so it <b>is</b> a line of symmetry. "
             "The line %s. A line of symmetry can go in any direction, not only up and down." % slant)
        return mcq(qs, Y_, [N2_, N1_, U_], e, rnd)
    if kind == "N2":
        e = ("The line cuts the %s into 2 parts of the <b>same size</b>, but when you fold on it the corners stick out "
             "and the halves do not land on each other. Cutting a shape in half is not enough: the halves must match "
             "when folded." % noun)
        if name == "ellipse":
            e = ("The line cuts the oval into 2 parts of the same size, but when you fold on a slanted line the ends "
                 "do not land on each other. An oval has only 2 lines of symmetry: across and up and down.")
        return mcq(qs, N2_, [T_, Y_, N1_], e, rnd)
    e = ("The line is not in the middle, so one part is bigger than the other. When you fold, the small part cannot "
         "cover the big part, so it is <b>not</b> a line of symmetry.")
    return mcq(qs, N1_, [Y_, T_, N2_], e, rnd)


def it(name, a=None, frac=None, F=None):
    """A shape with one dashed line: through the center at angle a, or a vertical/horizontal line at a fraction of the width/height."""
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


WHY = {"Y": "the halves match", "N1": "the line is not in the middle", "N2": "same size, but the halves do not match"}


def set_is_line(rnd):
    its = []
    r = shp("rectangle")
    rd = math.degrees(math.atan2(76, 132))
    singles = [
        it("square", 90, 0.32), it("rectangle", 0), (("rectangle", r, center(r), rd)), it("square", 45),
        it("isosceles trapezoid", 0, 0.5), it("parallelogram", 90), it("rhombus", 0), it("kite", 0, 36 / 124.0),
        it("equilateral triangle", 30), it("ellipse", 35),
    ]
    kinds = []
    for name, F, p, a in singles:
        its.append(line_q(name, F, p, a, rnd))
        kinds.append(split_kind(F, p, a))
    assert kinds.count("Y") == 4 and kinds.count("N1") == 3 and kinds.count("N2") == 3, kinds

    # the parallelogram's diagonals: from the top-left corner to the bottom-right corner
    P = shp("parallelogram")
    pa = P[0]["pts"]
    pd = math.degrees(math.atan2(pa[2][1] - pa[0][1], pa[2][0] - pa[0][0]))
    rs = math.degrees(math.atan2(76, 132)) + 18          # a slanted line through the middle of a rectangle
    POOL = {
        "sq_v": it("square", 90), "sq_d": it("square", 135), "rect_h": it("rectangle", 0), "trect_v": it("tall rectangle", 90),
        "eq_v": it("equilateral triangle", 90), "iso_v": it("isosceles triangle", 90), "kite_v": it("kite", 90),
        "rh_v": it("rhombus", 90), "trap_v": it("isosceles trapezoid", 90), "hex_h": it("regular hexagon", 0),
        "hex_d": it("regular hexagon", 150), "pent_v": it("regular pentagon", 90), "circ": it("circle", 35),
        "arrow_h": it("arrow", 0), "semi_v": it("semicircle", 90), "heart_v": it("heart", 90), "oct_d": it("regular octagon", 22.5),
        "ri_d": it("right isosceles triangle", 135),
        # not lines of symmetry
        "rect_d": ("rectangle", r, center(r), rd), "rect_s": ("rectangle", r, center(r), rs),
        "para_d": ("parallelogram", P, center(P), pd), "para_v": it("parallelogram", 90), "para_h": it("parallelogram", 0),
        "sq_off": it("square", 0, 0.3), "rect_off": it("tall rectangle", 90, 0.3), "iso_h": it("isosceles triangle", 0, 0.5),
        "trap_h": it("isosceles trapezoid", 0, 0.5), "kite_h": it("kite", 0, 36 / 124.0), "hex_off": it("regular hexagon", 90, 0.3),
        "rt_m": it("right triangle", math.degrees(math.atan2(-36 - 36, 58 + 58)) % 180), "ell_s": it("ellipse", 30),
        "rh_s": it("rhombus", math.degrees(math.atan2(64, 42)) % 180),
        "eq_h": it("equilateral triangle", 0, 0.5),
    }
    for k, (name, F, p, a) in POOL.items():
        POOL[k] = (name, F, p, a, split_kind(F, p, a))
    is_panels = [("sq_v", ["rect_d", "para_d", "hex_off"]), ("eq_v", ["iso_h", "rt_m", "rect_s"]),
                 ("hex_h", ["sq_off", "para_h", "rh_s"]), ("kite_v", ["trap_h", "ell_s", "rect_off"]),
                 ("circ", ["kite_h", "para_v", "eq_h"])]
    not_panels = [("rect_d", ["sq_d", "trect_v", "circ"]), ("para_v", ["trap_v", "iso_v", "hex_d"]),
                  ("kite_h", ["rh_v", "pent_v", "arrow_h"]), ("rh_s", ["semi_v", "oct_d", "heart_v"]),
                  ("ell_s", ["ri_d", "eq_v", "rect_h"])]
    plans = []
    for i in range(5):
        plans.append(("is", is_panels[i]))
        plans.append(("not", not_panels[i]))
    spots = Spots(rnd)
    used = set()
    for mode, (good, bads) in plans:
        g = POOL[good]
        assert (g[4] == "Y") == (mode == "is"), (good, g[4])
        for b in bads:
            assert (POOL[b][4] == "Y") == (mode == "not"), (b, POOL[b][4])
        names = [g[0]] + [POOL[b][0] for b in bads]
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
        others = "; ".join("%s: %s" % ("ABCD"[j], WHY[POOL[k][4]]) for j, k in enumerate(keys) if j != pos)
        if mode == "is":
            qs = fig(svg) + "Which dashed line <b>is</b> a line of symmetry?"
            e = "Fold each shape on its dashed line. Only in <b>%s</b> do the halves land exactly on each other. Others: %s." % (L, others)
        else:
            qs = fig(svg) + "Which dashed line is <b>not</b> a line of symmetry?"
            why = {"N2": "the line cuts the %s into 2 parts of the same size, but they do not match when folded",
                   "N1": "the line is not in the middle of the %s, so one part is bigger"}[g[4]] % {"ellipse": "oval"}.get(g[0], g[0])
            e = "In <b>%s</b> %s. In the other 3 pictures the halves fold exactly onto each other." % (L, why)
        if "rect_d" in keys and good != "rect_d":
            e += " Remember: a rectangle’s diagonal cuts it in half, but it is not a line of symmetry."
        its.append(mcq_fixed(qs, ["A", "B", "C", "D"], pos, e))
    assert len(its) == 20
    return {"title": "Is it a line of symmetry?", "items": its}


# ============================================================ set 2: how many lines of symmetry?
NUMS = ["0", "1", "2", "3", "4", "5", "6", "8", INF]

COUNT_Q = [
    ("square", "a square", ["2", "8", "1"],
     "A square has <b>4</b> lines of symmetry: 1 up and down, 1 across, and 2 along the diagonals, corner to corner. "
     "Do not forget the diagonals."),
    ("rectangle", "a rectangle", ["4", "1", "0"],
     "A rectangle has <b>2</b> lines of symmetry: up and down and across, through the middles of the sides. "
     "The diagonals cut it in half, but folded on a diagonal the corners stick out."),
    ("equilateral triangle", "a triangle with 3 equal sides", ["1", "6", "0"],
     "Each line goes from a corner to the middle of the opposite side. There are 3 corners, so there are <b>3</b> lines."),
    ("isosceles triangle", "a triangle with 2 equal sides", ["3", "2", "0"],
     "Only the line from the top corner down to the middle of the bottom side works, so there is <b>1</b> line."),
    ("scalene triangle", "a triangle with 3 different sides", ["1", "3", "2"],
     "All 3 sides have different lengths, so no fold makes the halves match. There are <b>0</b> lines of symmetry."),
    ("circle", "a circle", ["4", "2", "1"],
     "Every line through the center of a circle folds it into matching halves. There are <b>infinitely many</b> lines."),
    ("rhombus", "a rhombus", ["4", "1", "0"],
     "A rhombus that is not a square has <b>2</b> lines of symmetry, and both go corner to corner (its diagonals). "
     "Lines through the middles of the sides do not work."),
    ("parallelogram", "a parallelogram", ["2", "1", "4"],
     "A slanted parallelogram has <b>0</b> lines of symmetry. Its diagonals cut it in half, but folded the corners stick out."),
    ("kite", "a kite", ["2", "0", "4"],
     "Only the long line from the top corner to the bottom corner works, so a kite has <b>1</b> line of symmetry."),
    ("isosceles trapezoid", "a trapezoid with 2 equal slanted sides", ["2", "0", "4"],
     "Only the up-and-down line through the middles of the top and bottom works. A line across does not, because "
     "the top is shorter than the bottom. <b>1</b> line."),
    ("tilted rectangle", "a rectangle that is turned", ["0", "4", "1"],
     "Turning a shape does not change its lines of symmetry. It is still a rectangle, so it has <b>2</b> lines. "
     "They are slanted now, along with the rectangle."),
    ("regular pentagon", "a pentagon with 5 equal sides and 5 equal angles", ["1", "2", "10"],
     "Each line goes from a corner to the middle of the opposite side. 5 corners, so <b>5</b> lines."),
    ("regular hexagon", "a hexagon with 6 equal sides and 6 equal angles", ["3", "2", "4"],
     "3 lines go corner to corner and 3 more go through the middles of opposite sides: 3 + 3 = <b>6</b> lines."),
    ("plus sign", "this plus sign (all 4 arms the same)", ["2", "8", "1"],
     "Up and down and across work, and so do the 2 slanted lines corner to corner: <b>4</b> lines, like a square."),
    ("regular octagon", "an octagon with 8 equal sides and 8 equal angles", ["4", "2", "6"],
     "4 lines go corner to corner and 4 go through the middles of opposite sides: 4 + 4 = <b>8</b> lines."),
    ("L shape", "this L shape (both arms the same size)", ["0", "2", "4"],
     "Up and down and across do not work. But the slanted line from the inside corner to the outside corner folds one arm "
     "onto the other: <b>1</b> line."),
]


def set_count(rnd):
    its = []
    for name, desc, wrong, e in COUNT_Q:
        F = shp(name)
        n = LINES[name]
        right = INF if n == INF else str(n)
        its.append(mcq(fig(single_svg(F, label=name.replace("regular ", ""))) +
                       "How many lines of symmetry does %s have?" % desc, right, wrong, e, rnd))
    panels = [
        ("Which shape has exactly 2 lines of symmetry?", "rectangle", ["square", "isosceles triangle", "parallelogram"]),
        ("Which shape has <b>no</b> lines of symmetry?", "scalene triangle", ["isosceles triangle", "equilateral triangle", "right isosceles triangle"]),
        ("Which shape has the <b>most</b> lines of symmetry?", "regular hexagon", ["square", "regular pentagon", "equilateral triangle"]),
        ("Which shape has exactly 1 line of symmetry?", "isosceles trapezoid", ["rectangle", "parallelogram", "rhombus"]),
    ]
    pnames = {"rectangle": "rectangle", "square": "square", "isosceles triangle": "triangle with 2 equal sides",
              "parallelogram": "parallelogram", "scalene triangle": "triangle with 3 different sides",
              "equilateral triangle": "triangle with 3 equal sides", "right isosceles triangle": "right triangle with 2 equal sides",
              "regular hexagon": "hexagon", "regular pentagon": "pentagon", "isosceles trapezoid": "trapezoid", "rhombus": "rhombus"}
    spots = Spots(rnd)
    for qs, good, bads in panels:
        pos = spots.next()
        bads = bads[:]
        rnd.shuffle(bads)
        keys = bads[:pos] + [good] + bads[pos:]
        cnt = [LINES[k] for k in keys]
        if "most" in qs:
            assert all(c < LINES[good] for k, c in zip(keys, cnt) if k != good)
        else:
            assert sum(1 for c in cnt if c == LINES[good]) == 1, (keys, cnt)
        svg = panel_svg([(shp(k), []) for k in keys], "four shapes A to D")
        e = "Count the lines for each shape: " + ", ".join(
            "%s (%s) %s" % ("ABCD"[j], pnames[k], lines_word(LINES[k])) for j, k in enumerate(keys)) + \
            ". The answer is <b>%s</b>." % "ABCD"[pos]
        its.append(mcq_fixed(fig(svg) + qs, ["A", "B", "C", "D"], pos, e))
    assert len(its) == 20
    return {"title": "How many lines of symmetry?", "items": its}


# ============================================================ set 3: capital letters
KCH = ["Vertical only", "Horizontal only", "Both", "None"]
KI = {"v": 0, "h": 1, "b": 2, "n": 3}
WHY_L = {
    "A": "A fold straight down the middle matches the two slanted sides. A fold across does not: the top is a point and the bottom is open.",
    "M": "A fold straight down the middle matches the two halves of M. Folded across, the top and bottom do not match.",
    "U": "A fold straight down the middle matches the two sides of U. Folded across, the round bottom does not match the open top.",
    "B": "Fold B across the middle: the top bump lands on the bottom bump. Folded up and down, the bumps on the right have nothing to match on the left.",
    "C": "Fold C across the middle: the top half lands on the bottom half. Up and down does not work, because C is open on the right only.",
    "E": "Fold E across the middle: the top arm lands on the bottom arm. Up and down does not work, because all the arms point right.",
    "H": "H folds into matching halves straight down the middle <b>and</b> across the middle, so it has both.",
    "O": "This O is taller than it is wide. It folds into matching halves up and down and across: both. (It is not a circle, so the slanted folds do not work.)",
    "X": "This X is taller than it is wide. It matches when folded up and down and when folded across: both.",
    "N": "No fold makes N match. N looks the same after a half turn, but turning is not folding, so N has <b>no</b> line of symmetry.",
    "S": "No fold makes S match. S looks the same after a half turn, but a turn is not a fold, so S has <b>no</b> line of symmetry.",
    "R": "Folded up and down, the bump and the leg are on one side only. Folded across, the bump does not match the leg. R has no line of symmetry.",
}


def letter_svg(ch):
    return single_svg(letter(ch), bw=80, bh=72, label="the capital letter %s" % ch)


def letter_row_svg(keys, cw=74):
    """Four letters in a row. The choices are the letters themselves, in the same order."""
    el = []
    H = 92
    for k, ch in enumerate(keys):
        e, bb = render(letter(ch), [], 50, 70, k * cw + cw / 2.0, H / 2.0)
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 2 and bb[3] <= H - 2, (ch, bb)
        el += e
        if k:
            el.append("<line x1='%d' y1='6' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (k * cw, k * cw, H - 6, GRAY))
    return svg_wrap(cw * len(keys), H, "".join(el), "four letters in a row: " + ", ".join(keys))


def set_letters(rnd):
    its = []
    order = ["A", "B", "H", "R", "C", "M", "O", "N", "E", "U", "X", "S"]
    for ch in order:
        k = KIND[ch]
        qs = fig(letter_svg(ch)) + "Which lines of symmetry does the letter %s have: vertical (up and down), horizontal (across), both, or none?" % ch
        its.append(mcq_fixed(qs, KCH, KI[k], WHY_L[ch]))
    panels = [
        ("Which letter has a line of symmetry?", "T", "FLJ", "T has a vertical line of symmetry. F, L and J have none."),
        ("Which letter has a line of symmetry?", "D", "GPR", "D has a horizontal line of symmetry. G, P and R have none."),
        ("Which letter has <b>no</b> line of symmetry?", "Z", "THE", "Z has none: it looks the same after a half turn, but no fold matches. T (vertical), H (both) and E (horizontal) each have at least one."),
        ("Which letter has <b>no</b> line of symmetry?", "G", "CUW", "G has none: the bar inside G breaks the match across. C (horizontal), U and W (vertical) each have one."),
        ("Which letter has a <b>horizontal</b> line of symmetry?", "D", "AVY", "Fold D across the middle and the halves match. A, V and Y have a vertical line, not a horizontal one."),
        ("Which letter has a <b>vertical</b> line of symmetry?", "W", "BEC", "Fold W straight down the middle and the halves match. B, E and C have a horizontal line, not a vertical one."),
        ("Which letter has <b>2</b> lines of symmetry?", "I", "TEY", "I matches when folded up and down and when folded across: 2 lines. T and Y have only a vertical line, and E only a horizontal line."),
        ("Which letter has <b>no</b> line of symmetry?", "N", "HIX", "H, I and X have 2 lines each. N looks the same after a half turn, like H, I and X, but no fold matches, so N has none."),
    ]
    spots = Spots(rnd)
    for qs, good, bads, e0 in panels:
        pos = spots.next()
        bads = list(bads)
        rnd.shuffle(bads)
        keys = bads[:pos] + [good] + bads[pos:]
        a = {k: axes(letter(k)) for k in keys}
        if "no</b>" in qs:
            ok = [k for k in keys if a[k] == []]
        elif "horizontal" in qs:
            ok = [k for k in keys if 0.0 in a[k]]
        elif "vertical" in qs:
            ok = [k for k in keys if 90.0 in a[k]]
        elif "<b>2</b>" in qs:
            ok = [k for k in keys if len(a[k]) == 2]
        else:
            ok = [k for k in keys if a[k]]
        assert ok == [good], (qs, keys, a)
        svg = letter_row_svg(keys)
        its.append(mcq_fixed(fig(svg) + qs, keys, pos, e0))
    assert len(its) == 20
    return {"title": "Symmetry in capital letters", "items": its}


# ============================================================ set 4: complete the picture on a grid
def options(half, line, cols, rows, rnd, kinds):
    full = frozenset(half | {mir(x, line) for x in half})
    out = {"ok": full}
    other = sorted(full - half)
    for k in kinds:
        if k == "slide":
            if line[0] == "v":
                d = int(line[1])
                s = frozenset(half | {(c + d, r) for c, r in half})
            else:
                d = int(line[1])
                s = frozenset(half | {(c, r + d) for c, r in half})
        elif k == "turn":
            s = frozenset(half | {(cols - 1 - c, rows - 1 - r) for c, r in half})
        elif k == "moved":
            s = None
            cand = other[:]
            rnd.shuffle(cand)
            for x in cand:
                for dc, dr in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    y = (x[0] + dc, x[1] + dr)
                    if (0 <= y[0] < cols and 0 <= y[1] < rows and y not in full and mir(y, line) not in full
                            and y != mir(y, line)):
                        s = frozenset((full - {x}) | {y})
                        break
                if s:
                    break
        elif k == "missing":
            cand = [x for x in other if mir(x, line) != x]
            s = frozenset(full - {rnd.choice(cand)})
        out[k] = s
    for k, s in out.items():
        assert all(0 <= c < cols and 0 <= r < rows for c, r in s), k
        assert gsym(s, line) == (k == "ok"), k
    assert len(set(out.values())) == len(out)
    return out


OPT_WHY = {"slide": "the half was slid over, not flipped", "turn": "the half was turned upside down, not just flipped",
           "moved": "one square is in the wrong place", "missing": "one square is missing"}


V_HALVES = [
    ["..#", ".##", "###", "..#", "..#"],
    ["#..", "##.", ".##", "..#", ".##"],
    [".#.", "###", "..#", ".##", "#.."],
    ["...#", "..##", ".#.#", "####", "...#"],
    ["##..", ".#.#", ".###", "...#", "..##"],
    ["#...", ".#..", "..##", ".###", "#..#"],
    ["..#", "#.#", "###", ".#.", "##."],
    ["...#", ".###", "#..#", "..##"],
]
H_HALVES = [
    ["#.....", "##..#.", "######"],
    ["..#...", ".###..", "#.####"],
    ["...##.", "#..#..", "####.#"],
    [".#....", "###.##", "..####"],
]
D_HALVES = [
    ["#....", "##...", ".##..", "..#..", ".###."],
    [".....", "#....", "##...", "#.##.", "##..#"],
]


def set_grid(rnd):
    its = []
    spots = Spots(rnd)
    plans = []
    for i, h in enumerate(V_HALVES):
        w = len(h[0])
        plans.append(("v", h, 2 * w, len(h), ("v", w), ["slide", "turn", "moved" if i % 2 == 0 else "missing"]))
    for i, h in enumerate(H_HALVES):
        plans.append(("h", h, len(h[0]), 2 * len(h), ("h", len(h)), ["slide", "turn", "moved" if i % 2 else "missing"]))
    for i, h in enumerate(D_HALVES):
        plans.append(("d", h, 5, 5, ("d",), ["turn", "moved", "missing"]))
    seen = set()
    for kind, h, cols, rows, line, wrongs in plans:
        half = cells_of(h)
        if kind == "d":
            assert all(r >= c for c, r in half)
        opts = options(half, line, cols, rows, rnd, wrongs)
        pos = spots.next()
        rnd.shuffle(wrongs)
        keys = wrongs[:pos] + ["ok"] + wrongs[pos:]
        cs = 12 if cols >= 8 else 14 if kind != "d" else 15
        svg = grid_panel(cols, rows, [opts[k] for k in keys], line, cs, "four grid pictures A to D with a dashed line")
        assert svg not in seen
        seen.add(svg)
        side = {"v": "left", "h": "top", "d": "bottom-left"}[kind]
        qs = (fig(svg) + "The dashed line is a line of symmetry. The %s half is the same in every picture. "
              "Which picture is completed correctly?" % side)
        rule = {"v": "Each square needs a partner in the same row, the same distance from the line on the other side.",
                "h": "Each square needs a partner in the same column, the same distance from the line on the other side.",
                "d": "Each square needs a partner straight across the slanted line, the same distance away: rows and "
                     "columns swap, so the square in row 3, column 2 pairs with the square in row 2, column 3."}[kind]
        others = "; ".join("%s: %s" % ("ABCD"[j], OPT_WHY[k]) for j, k in enumerate(keys) if k != "ok")
        e = "%s Only <b>%s</b> is a mirror image. Others: %s." % (rule, "ABCD"[pos], others)
        its.append(mcq_fixed(qs, ["A", "B", "C", "D"], pos, e))

    # how many squares?  The line goes through the middle of a column (or row), so those squares are their own partners.
    counts = [
        ("v", ["..#.", ".##.", "####", "..##", "...#"], 7, 5, "all"),
        ("v", ["...#", "..##", ".#..", "####", "..#."], 7, 5, "more"),
        ("h", ["...#..", "..##..", ".####.", "##.###"], 6, 7, "all"),
        ("v", ["#...", "##.#", ".###", "...#", "..##"], 7, 5, "more"),
        ("h", ["..#...", ".###..", ".#.##.", "######"], 6, 7, "all"),
        ("v", ["...#", ".#.#", "####", "#..#", "..##"], 7, 5, "all"),
    ]
    for kind, h, cols, rows, ask in counts:
        half = cells_of(h)
        line = ("v", 3.5) if kind == "v" else ("h", 3.5)
        on = [x for x in half if mir(x, line) == x]
        n, m = len(half), len(on)
        assert m >= 1 and n - m >= 2
        full = half | {mir(x, line) for x in half}
        assert gsym(full, line) and len(full) == 2 * (n - m) + m
        where = "column" if kind == "v" else "row"
        svg = grid_svg(cols, rows, half, line, 18 if kind == "v" else 16, "grid with shaded squares on one side of a dashed line")
        side = "right" if kind == "v" else "bottom"
        if ask == "all":
            qs = (fig(svg) + "The dashed line goes through the middle of a %s. Shade squares on the %s so the dashed line is "
                  "a line of symmetry. How many squares will be shaded in all?" % (where, side))
            right = 2 * (n - m) + m
            wrong = [2 * n, 2 * (n - m), n]
            e = ("%d squares are shaded now. %s of them %s on the line, so they are their own partners: count them once. "
                 "The other %d get a partner each. %d + %d + %d = <b>%d</b>."
                 % (n, m, "is" if m == 1 else "are", n - m, n - m, n - m, m, right))
        else:
            qs = (fig(svg) + "The dashed line goes through the middle of a %s. How many more squares must you shade "
                  "so the dashed line is a line of symmetry?" % where)
            right = n - m
            wrong = [n, 2 * n - m, m]
            e = ("Only squares that are not on the line need a partner. %d squares are shaded and %d %s on the line, "
                 "so %d - %d = <b>%d</b> more squares." % (n, m, "is" if m == 1 else "are", n, m, right))
        its.append(mcq(qs, right, wrong, e, rnd))
    # easy -> hard: vertical, horizontal, counts, slanted line
    its = its[:12] + its[14:] + its[12:14]
    assert len(its) == 20
    return {"title": "Complete the picture on a grid", "items": its}


# ============================================================ set 5: real-world pictures and word problems
OBJ = [
    (butterfly, "this butterfly picture", "butterfly", 1, ["2", "0", "4"],
     "Only the line straight down the body works: each wing lands on the wing on the other side. "
     "Folded across, the big top wings would not match the small bottom wings. <b>1</b> line."),
    (leaf, "this leaf", "leaf with a stem", 1, ["2", "0", "4"],
     "The line down the middle vein works: the veins on each side match. Folded across, the stem has nothing to match, "
     "so there is only <b>1</b> line."),
    (flag_stripes, "this flag", "flag with 3 stripes", 2, ["1", "4", "0"],
     "The top and bottom stripes are the same color, so folding across works, and folding up and down works too: "
     "<b>2</b> lines. The diagonals do not work, just like in a rectangle."),
    (flag_two, "this flag", "flag with 2 stripes", 1, ["2", "0", "4"],
     "Folding across puts blue on green, so that does not work. Folding up and down matches blue to blue and green to green: "
     "<b>1</b> line. Colors must match too."),
    (flag_cross, "this flag", "flag with a cross that is not in the middle", 1, ["2", "4", "0"],
     "The cross is to the left of the middle, so folding up and down does not work. Folding across does: <b>1</b> line."),
    (flag_band, "this flag", "flag with a slanted band", 0, ["1", "2", "4"],
     "Folding on the band itself does not work, because the flag is not a square: the corners stick out. "
     "Up and down and across do not work either. <b>0</b> lines."),
    (sign_stop, "a sign with this shape (no words on it)", "octagon sign", 8, ["4", "2", "6"],
     "The sign is a regular octagon: 4 lines go corner to corner and 4 go through the middles of opposite sides. "
     "<b>8</b> lines. (With the word STOP written on it, it would have none.)"),
    (sign_yield, "this sign", "triangle sign pointing down", 3, ["1", "6", "2"],
     "The sign is a triangle with 3 equal sides. Each line goes from a corner to the middle of the opposite side: <b>3</b> lines."),
    (sign_diamond, "this sign", "diamond sign", 4, ["2", "1", "8"],
     "The sign is a square turned on its corner, and turning does not change symmetry. 2 lines go corner to corner "
     "and 2 go through the middles of the sides: <b>4</b> lines."),
    (pinwheel, "this pinwheel", "pinwheel", 0, ["4", "2", "8"],
     "The pinwheel looks the same after a quarter turn, but every blade leans the same way, so no fold matches. "
     "Turning is not folding: <b>0</b> lines."),
]


def set_world(rnd):
    its = []
    for make, desc, label, n, wrong, e in OBJ:
        F = expect(make(), n, label)
        its.append(mcq(fig(single_svg(F, label=label)) + "How many lines of symmetry does %s have?" % desc,
                       str(n), wrong, e, rnd))
    W = [
        ("Ava has a square sheet of paper. In how many different ways can she fold it in half so that the two halves match exactly?",
         "4", ["2", "8", "1"],
         "A square has 4 lines of symmetry: up and down, across, and the 2 diagonals. So there are 4 ways."),
        ("Leo folds a rectangular rug that is 6 feet long and 4 feet wide along its diagonal, from corner to corner. Do the two halves match?",
         "No, the corners stick out", ["Yes, both halves are the same size", "Yes, every line through the middle works", "No, a rug has no line of symmetry"],
         "The diagonal cuts the rug into 2 triangles of the same size, but they do not land on each other when folded, "
         "because the rug is not a square. A rectangle has only 2 lines of symmetry."),
        ("Noah says every line through the middle of a rectangle is a line of symmetry. Is he right?",
         "No, only 2 lines work", ["Yes, every line works", "No, only 4 lines work", "No, only 1 line works"],
         "Only the line up and down and the line across fold a rectangle into matching halves. "
         "Slanted lines and diagonals do not."),
        ("Mia writes these words in capital letters. Which word has a <b>horizontal</b> line of symmetry?",
         "BOX", ["MOM", "TOT", "SIX"],
         "B, O and X each have a horizontal line of symmetry through their middles, so the whole word BOX does too. "
         "MOM and TOT have a vertical line through the middle letter, not a horizontal one. S has no line at all."),
        ("Which word has a <b>vertical</b> line of symmetry through its middle letter?",
         "WOW", ["BOB", "DAD", "ZOO"],
         "W and O each have a vertical line of symmetry, so a vertical line through the O folds the first W onto the last W. "
         "In BOB and DAD the B and D face right, so their mirror images would be backward. Z has no line of symmetry."),
        ("A shape has exactly 1 line of symmetry. Which shape could it be?",
         "A trapezoid with 2 equal slanted sides", ["A rectangle", "A parallelogram", "A square"],
         "A trapezoid with 2 equal slanted sides has only the up-and-down line. A rectangle has 2, a square has 4 "
         "and a slanted parallelogram has 0."),
        ("Kai draws a shape with 4 equal sides. It has exactly 2 lines of symmetry, and both go from corner to corner. What shape is it?",
         "A rhombus that is not a square", ["A square", "A rectangle", "A kite"],
         "A rhombus has 2 lines of symmetry along its diagonals. A square would have 4, a rectangle’s 2 lines go "
         "through the middles of the sides, and a kite has 1."),
        ("Lily folds a sheet of paper in half, cuts out a shape along the fold, and opens it. What must be true?",
         "The fold is a line of symmetry", ["The shape has no line of symmetry", "The shape has exactly 2 lines of symmetry",
                                            "One half is bigger than the other"],
         "Both halves were cut at the same time, so they are mirror images. The fold line is always a line of symmetry. "
         "The shape could have other lines too, but it does not have to."),
        ("Ben says the letter S has a line of symmetry because it looks the same upside down. Is he right?",
         "No, a turn is not a fold", ["Yes, it looks the same upside down", "Yes, it has a horizontal line", "No, S has 2 lines"],
         "S looks the same after a half turn, but no fold makes the two halves match. A line of symmetry is about "
         "folding, so S has 0 lines."),
        ("Zoe cuts out a circle. How many different lines can she fold it on so that the two halves match?",
         INF, ["4", "2", "1"],
         "Every line through the center of a circle is a line of symmetry, so there are infinitely many. "
         "Up and down, across and the 2 diagonals are just 4 of them."),
    ]
    for qs, right, wrong, e in W:
        its.append(mcq(qs, right, wrong, e, rnd))
    assert len(its) == 20
    return {"title": "Pictures and word problems", "items": its}


# ============================================================ lesson
def body_html():
    r = shp("rectangle")
    rd = math.degrees(math.atan2(76, 132))
    f1 = strip_svg([(r, [dash_seg(r, center(r), 90)], "Line of symmetry"),
                    (r, [dash_seg(r, center(r), rd)], "Not a line")],
                   "a rectangle with an up-and-down dashed line and a rectangle with a diagonal dashed line", cw=170)
    shapes = ["square", "rectangle", "equilateral triangle", "parallelogram"]
    f2 = strip_svg([(shp(k), all_axis_segs(shp(k)), lines_word(LINES[k])) for k in shapes],
                   "a square with 4 lines of symmetry, a rectangle with 2, a triangle with 3 and a parallelogram with 0")
    f3 = strip_svg([(letter(c), all_axis_segs(letter(c)), cap) for c, cap in
                    [("A", "Vertical"), ("B", "Horizontal"), ("H", "Both"), ("N", "None")]],
                   "the letters A, B, H and N with their lines of symmetry", cw=110, box=(80, 82))
    half = cells_of(["..#", ".##", "###", "..#", "..#"])
    full = half | {mir(x, ("v", 3)) for x in half}
    f4 = grid_svg(6, 5, full, ("v", 3), 24, "a grid picture completed across a dashed line",
                  light=full - half)
    return (
        "<h2>The fold test</h2>"
        "<p>A <b>line of symmetry</b> is a line across a figure so that, if you fold the figure on the line, "
        "the two halves <b>match exactly</b>. Each half is the mirror image of the other.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Fold the first rectangle on the up-and-down line: the halves match. The diagonal also cuts the "
        "rectangle into 2 equal triangles, but folded on it the corners stick out, so it is not a line of symmetry.</figcaption></figure>"
        "<h2>A figure can have many lines, or none</h2>"
        "<p>Try every way to fold. A line of symmetry can go up and down, across or slanted.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>A square has 4 lines (2 are diagonals). A rectangle has only 2. A triangle with 3 equal sides has 3. "
        "A slanted parallelogram has none.</figcaption></figure>" +
        table(["Figure", "Lines of symmetry"], [
            ["Square", "4"], ["Rectangle (not a square)", "2"], ["Rhombus (not a square)", "2 (corner to corner)"],
            ["Triangle with 3 equal sides", "3"], ["Triangle with 2 equal sides", "1"], ["Triangle with 3 different sides", "0"],
            ["Kite", "1"], ["Trapezoid with 2 equal slanted sides", "1"], ["Parallelogram (slanted)", "0"],
            ["Regular pentagon, hexagon, octagon", "5, 6, 8 (one for each side)"], ["Circle", "Infinitely many"],
        ]) +
        "<h2>Letters</h2>"
        "<p>Capital letters can have a vertical line, a horizontal line, both, or none.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>A, M, T, U, V, W, Y: vertical. B, C, D, E: horizontal. H, I, O, X: both. "
        "F, G, J, L, N, P, Q, R, S, Z: none.</figcaption></figure>"
        "<h2>Complete a picture</h2>"
        "<p>To finish a symmetric picture, give every square a partner the same distance from the line on the other side. "
        "Flip it like a mirror; do not slide it.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>The dark squares were given. The light squares are their mirror images: same row, same distance from the line.</figcaption></figure>" +
        ex("Example", "How many lines of symmetry does a regular hexagon have?",
           "3 lines go corner to corner. 3 more go through the middles of opposite sides. 3 + 3 = 6.", "6") +
        ex("Example", "Does the letter Z have a line of symmetry?",
           "Fold up and down: the top line goes right but the bottom goes left. Fold across: the slant does not match. "
           "Z looks the same after a half turn, but a turn is not a fold.", "No, 0 lines") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a rectangle’s diagonals (4 lines)", "Fold on a diagonal: the corners stick out. A rectangle has 2"],
            ["Forgetting a square’s diagonals (2 lines)", "A square folds on its diagonals too: 4 lines"],
            ["Thinking only up-and-down lines count", "Lines can go across or slant. Try every way to fold"],
            ["Saying N, S or Z have a line because they look the same upside down", "That is a turn, not a fold. They have 0 lines"],
            ["Sliding the half when completing a picture", "Flip it: each square goes the same distance on the other side"],
        ])
    )


FAQ = [
    {"q": "What is a line of symmetry in 4th grade math?",
     "a": "A line of symmetry is a line across a figure so that the figure can be folded on it into two matching halves. A heart has 1 line of symmetry, straight down the middle."},
    {"q": "Does a rectangle have 4 lines of symmetry?",
     "a": "No. A rectangle that is not a square has 2 lines of symmetry: up and down and across. Its diagonals cut it in half, but the halves do not match when folded."},
    {"q": "Which capital letters have a line of symmetry?",
     "a": "A, M, T, U, V, W and Y have a vertical line; B, C, D and E have a horizontal line; H, I, O and X have both. F, G, J, L, N, P, Q, R, S and Z have none (in simple block letters)."},
    {"q": "How many lines of symmetry does a circle have?",
     "a": "Infinitely many. Every line through the center of a circle folds it into two matching halves."},
]


def gen_symmetry():
    rnd = random.Random(116)
    sets = [set_is_line(rnd), set_count(rnd), set_letters(rnd), set_grid(rnd), set_world(rnd)]
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
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "line-symmetry", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Line Symmetry",
        "seo_title": "Grade 4 Line Symmetry Worksheets: Lines of Symmetry in Shapes, Letters and Pictures",
        "short_title": "Line symmetry",
        "domain": "Geometry",
        "standard_code": "4.G.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/G/A/3/",
        "standard_text": "Recognize a line of symmetry for a two-dimensional figure as a line across the figure such that the figure can be folded along the line into matching parts. Identify line-symmetric figures and draw lines of symmetry.",
        "meta_desc": "Free Grade 4 line symmetry worksheets with pictures: test a dashed line with the fold test, count the lines of symmetry of squares, rectangles, triangles and regular polygons, find symmetric capital letters, complete symmetric pictures on a grid, and solve word problems. 100 practice questions with answers.",
        "key_big": "A line of symmetry folds a figure into two halves that match exactly.",
        "key_sub": "A square has 4 lines, a rectangle only 2: its diagonals cut it in half, but folded on a diagonal the corners stick out. Letters like N, S and Z look the same upside down but have no line of symmetry.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices) so their labels stay readable."""
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
