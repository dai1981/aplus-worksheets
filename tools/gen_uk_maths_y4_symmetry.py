# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Lines of Symmetry (National Curriculum in England, Geometry – properties of shapes)
  python3 tools/gen_uk_maths_y4_symmetry.py
Every figure is built from exact coordinates and its lines of symmetry are found in code:
a line is a line of symmetry when reflecting every edge (with its colour) across it gives exactly
the same set of edges. Every count in an answer is the count found here, and every dashed line in a
question is tested the same way. Letters are drawn as strokes, so their symmetry is exact.
Grid pictures are checked square by square (vertical, horizontal and both diagonal mirror lines).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
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
    "right-angled isosceles triangle": lambda: S1([(-48, -48), (-48, 48), (48, 48)]),
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
         "scalene triangle": 0, "right-angled isosceles triangle": 1, "right-angled triangle": 0, "circle": INF, "rhombus": 2,
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


def flag(parts, w=120, h=72):
    F = [Poly(rect(w, h), parts[0], INK, 1.5)]
    for pts, col in parts[1:]:
        F.append(Poly(pts, col, col, 1))
    F.append(Poly(rect(w, h), "none", INK, 1.5))
    return F


def flag_cross_mid():
    """White flag with a red cross through the middle (like England's flag)."""
    return flag([WHITE, ([(-8, -36), (8, -36), (8, 36), (-8, 36)], RED),
                 ([(-60, -8), (60, -8), (60, 8), (-60, 8)], RED)])


def flag_saltire():
    """Blue flag with a white cross from corner to corner (like Scotland's flag)."""
    d, e = 13, 9
    band = [(-60, -36), (-60 + d, -36), (60, 36 - e), (60, 36), (60 - d, 36), (-60, -36 + e)]
    return flag([BLUE, (band, WHITE), ([(-x, y) for x, y in reversed(band)], WHITE)])


def flag_halves():
    """White top half, green bottom half (like the Welsh flag without its dragon)."""
    return flag([GREEN, ([(-60, -36), (60, -36), (60, 0), (-60, 0)], WHITE)])


def flag_cross_side():
    """A cross that is to the left of the middle."""
    return flag([BLUE, ([(-30, -36), (-14, -36), (-14, 36), (-30, 36)], YELLOW),
                 ([(-60, -8), (60, -8), (60, 8), (-60, 8)], YELLOW)])


def sign_octagon():
    return [Poly(reg(8, 56, -90 + 22.5), RED, RED, 2), Poly(reg(8, 49, -90 + 22.5), "none", WHITE, 3)]


def sign_warning():
    """Red triangle pointing up with a white middle (no picture inside)."""
    return [Poly(reg(3, 62), RED, RED, 2), Poly(reg(3, 38), WHITE, WHITE, 1)]


def sign_no_entry():
    """Red circle with a white bar across the middle."""
    return [Circ((0, 0), 50, RED, RED, 2), Poly(rect(70, 16), WHITE, WHITE, 1)]


def sign_arrow():
    """Blue circle with a white arrow pointing up."""
    arr = [(0, -34), (22, -10), (8, -10), (8, 32), (-8, 32), (-8, -10), (-22, -10)]
    return [Circ((0, 0), 50, BLUE, BLUE, 2), Poly(arr, WHITE, WHITE, 1)]


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
        "upside-down isosceles triangle": "triangle", "right-angled isosceles triangle": "triangle", "ellipse": "oval",
        "regular hexagon": "hexagon", "turned hexagon": "hexagon", "turned square": "square", "turned rectangle": "rectangle",
        "tall rectangle": "rectangle", "turned kite": "kite", "turned parallelogram": "parallelogram"}


def noun(name):
    return NOUN.get(name, name)


# ============================================================ set 1: is the dashed line a mirror line?
Y_ = "Yes, both halves match"
N1_ = "No, one part is bigger"
N2_ = "No, same size but not matching"
T_ = "Yes, the parts are the same size"
U_ = "No, mirror lines must be vertical"


def line_q(name, F, p, a, rnd, turned=False):
    kind = split_kind(F, p, a)
    seg = dash_seg(F, p, a)
    nn = noun(name)
    pic = fig(single_svg(F, [seg], label="%s with a dashed line" % nn))
    if turned:
        qs = pic + "This %s has been turned. Is the dashed line a mirror line?" % nn
    else:
        qs = pic + "Imagine folding the %s along the dashed line. Is the dashed line a line of symmetry?" % nn
    vert = abs(a - 90) < 1e-9
    if kind == "Y":
        e = "Fold along the dashed line: one half lands exactly on top of the other, so it <b>is</b> a mirror line."
        if not vert:
            e += " It is not vertical, and that is fine: a mirror line can go in any direction."
        return mcq(qs, Y_, [N2_, N1_, U_ if not vert else T_], e, rnd)
    if kind == "N2":
        e = ("The dashed line splits the %s into 2 parts of the <b>same size</b>, but if you fold along it, the corners "
             "do not land on each other. Equal halves are not enough: they must fit exactly when folded." % nn)
        if name == "ellipse":
            e = ("The dashed line splits the oval into 2 equal parts, but folded on this slanting line the ends do not "
                 "land on each other. An oval has just 2 mirror lines: one across and one up and down.")
        return mcq(qs, N2_, [T_, Y_, N1_], e, rnd)
    e = ("The dashed line is not through the middle, so one part is bigger. The smaller part cannot cover the bigger "
         "part when you fold, so it is <b>not</b> a mirror line.")
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


def corner_line(name, i, j):
    """Dashed line through corners i and j of a one-polygon shape."""
    F = shp(name)
    P = F[0]["pts"]
    a = math.degrees(math.atan2(P[j][1] - P[i][1], P[j][0] - P[i][0])) % 180
    return (name, F, P[i], a)


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
            qs = fig(svg) + "Which dashed line <b>is</b> a mirror line?"
            e = "Imagine folding each shape on its dashed line. Only in <b>%s</b> does one half fit exactly on the other. Others: %s." % (L, others)
        else:
            qs = fig(svg) + "Which dashed line is <b>not</b> a mirror line?"
            why = {"N2": "the line splits the %s into 2 equal parts, but they do not fit when folded",
                   "N1": "the line is not through the middle of the %s, so one part is bigger"}[g[4]] % noun(g[0])
            e = "In <b>%s</b> %s. In the other 3 pictures the halves fold exactly onto each other." % (L, why)
        if extra_rect and extra_rect in keys and good != extra_rect:
            e += " Remember: the diagonal of a rectangle splits it in half, but it is not a mirror line."
        out.append(mcq_fixed(qs, ["A", "B", "C", "D"], pos, e))
    return out


def set_is_line(rnd):
    its = []
    r = shp("rectangle")
    rd = math.degrees(math.atan2(76, 132))
    singles = [
        it("rectangle", 90), it("square", 90, 0.3), it("isosceles triangle", 90), ("rectangle", r, center(r), rd),
        it("regular hexagon", 90), it("isosceles trapezium", 0, 0.5), it("rhombus", 0), it("parallelogram", 90),
        it("square", 45), it("kite", 0, 36 / 124.0), it("ellipse", 35), it("equilateral triangle", 0, 0.5),
    ]
    kinds = []
    for name, F, p, a in singles:
        its.append(line_q(name, F, p, a, rnd))
        kinds.append(split_kind(F, p, a))
    assert kinds.count("Y") == 5 and kinds.count("N1") == 4 and kinds.count("N2") == 3, kinds

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
             ("is", ("eq_v", ["para_h", "trect_off", "ell_s"])), ("not", ("para_v", ["kite_v", "oct_h", "heart_v"])),
             ("is", ("trap_v", ["rect_d", "iso_h", "sq_off"])), ("not", ("iso_h", ["rh_h", "hex_v", "semi_v"])),
             ("is", ("sq_d", ["para_v", "trap_h", "ell_s"])), ("not", ("ell_s", ["iso_v", "trect_h", "pent_v"]))]
    its += panel_qs(plans, POOL, rnd, extra_rect="rect_d")
    assert len(its) == 20
    return {"title": "Is the dashed line a mirror line?", "items": its}


# ============================================================ set 2: how many lines of symmetry?
COUNT_Q = [
    ("square", "a square", ["2", "8", "1"],
     "A square has <b>4</b> mirror lines: one up and down, one across and 2 along the diagonals, from corner to corner. "
     "Pupils often forget the diagonals."),
    ("rectangle", "a rectangle", ["4", "1", "0"],
     "A rectangle has <b>2</b> mirror lines: up and down, and across, through the middles of the sides. "
     "A diagonal splits it into 2 equal triangles, but they do not fit when folded, so the diagonals do not count."),
    ("equilateral triangle", "an equilateral triangle (3 equal sides)", ["1", "6", "0"],
     "Each mirror line goes from a corner to the middle of the side opposite. 3 corners, so <b>3</b> lines."),
    ("isosceles triangle", "an isosceles triangle (2 equal sides)", ["3", "2", "0"],
     "Only the line from the top corner to the middle of the bottom side works: <b>1</b> line."),
    ("scalene triangle", "a scalene triangle (no equal sides)", ["1", "3", "2"],
     "The 3 sides are all different lengths, so no fold makes the halves fit. <b>0</b> lines of symmetry."),
    ("circle", "a circle", ["4", "2", "0"],
     "Any straight line through the centre of a circle is a mirror line. You could never draw them all, so a circle "
     "has <b>infinitely many</b>."),
    ("rhombus", "a rhombus", ["4", "1", "0"],
     "This rhombus (not a square) has <b>2</b> mirror lines, both from corner to corner. Lines through the middles "
     "of the sides do not work."),
    ("parallelogram", "a parallelogram", ["2", "1", "4"],
     "A parallelogram with slanting sides has <b>0</b> mirror lines. Its diagonals and its middle lines split it into equal "
     "halves, but none of them fit when folded."),
    ("kite", "a kite", ["2", "0", "4"],
     "Only the line from the top corner to the bottom corner works, so a kite has <b>1</b> mirror line."),
    ("isosceles trapezium", "an isosceles trapezium", ["2", "0", "4"],
     "Only the up-and-down line through the middles of the top and bottom works. Folding across does not, because the "
     "top is shorter than the bottom: <b>1</b> line."),
    ("regular pentagon", "a regular pentagon", ["1", "2", "10"],
     "Each mirror line goes from a corner to the middle of the side opposite. 5 corners, so <b>5</b> lines."),
    ("regular hexagon", "a regular hexagon", ["3", "2", "4"],
     "3 lines join opposite corners and 3 more join the middles of opposite sides: 3 + 3 = <b>6</b> lines."),
    ("regular octagon", "a regular octagon", ["4", "2", "6"],
     "4 lines join opposite corners and 4 join the middles of opposite sides: 4 + 4 = <b>8</b> lines."),
    ("semicircle", "a semicircle", ["2", "0", INF],
     "Only the line straight up through the middle of the flat side works: <b>1</b> line. Folding across puts the curve on the "
     "flat side."),
    ("ellipse", "this oval", ["1", "4", INF],
     "An oval has <b>2</b> mirror lines: one across the long way and one up and down. Slanting lines do not work, "
     "because it is not a circle."),
    ("plus sign", "this cross (all 4 arms the same)", ["2", "8", "1"],
     "Up and down and across both work, and so do the 2 slanting lines through the inside corners: <b>4</b> lines, just like a square."),
]
PNAMES = {"rectangle": "rectangle", "square": "square", "isosceles triangle": "isosceles triangle",
          "parallelogram": "parallelogram", "equilateral triangle": "equilateral triangle", "rhombus": "rhombus",
          "regular hexagon": "regular hexagon", "regular pentagon": "regular pentagon", "regular octagon": "regular octagon",
          "isosceles trapezium": "isosceles trapezium", "kite": "kite", "scalene triangle": "scalene triangle"}


def set_count(rnd):
    its = []
    for name, desc, wrong, e in COUNT_Q:
        F = shp(name)
        n = LINES[name]
        right = INF if n == INF else str(n)
        its.append(mcq(fig(single_svg(F, label=noun(name).replace("regular ", ""))) +
                       "How many lines of symmetry does %s have?" % desc, right, wrong, e, rnd))
    panels = [
        ("Which shape has exactly <b>3</b> lines of symmetry?", "equilateral triangle", ["isosceles triangle", "square", "rectangle"]),
        ("Which shape has <b>no</b> lines of symmetry?", "parallelogram", ["rectangle", "rhombus", "kite"]),
        ("Which shape has the <b>most</b> lines of symmetry?", "regular octagon", ["regular hexagon", "square", "regular pentagon"]),
        ("Which shape has exactly <b>1</b> line of symmetry?", "kite", ["rhombus", "rectangle", "parallelogram"]),
    ]
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
        e = "Count the mirror lines of each shape: " + ", ".join(
            "%s (%s) %s" % ("ABCD"[j], PNAMES[k], lines_word(LINES[k])) for j, k in enumerate(keys)) + \
            ". So the answer is <b>%s</b>." % "ABCD"[pos]
        its.append(mcq_fixed(fig(svg) + qs, ["A", "B", "C", "D"], pos, e))
    assert len(its) == 20
    return {"title": "How many lines of symmetry?", "items": its}


# ============================================================ set 3: shapes in different orientations
TURN_Q = [
    ("turned square", "This square has been turned so it stands on a corner. How many lines of symmetry does it have?",
     ["2", "0", "1"],
     "Turning a shape does not change its mirror lines. It is still a square, so it has <b>4</b>: one up and down and "
     "one across (these now join the corners), plus 2 slanting ones."),
    ("turned rectangle", "This rectangle has been turned. How many lines of symmetry does it have?",
     ["0", "4", "1"],
     "It is still a rectangle, so it still has <b>2</b> mirror lines. They have turned with it, so now they slant. "
     "Do not say 0 just because no line is straight up and down."),
    ("turned isosceles triangle", "This isosceles triangle is lying on its side. How many lines of symmetry does it have?",
     ["0", "2", "3"],
     "The mirror line now goes <b>across</b>, from the corner on the right to the middle of the side on the left: <b>1</b> line."),
    ("upside-down isosceles triangle", "This isosceles triangle is upside down. How many lines of symmetry does it have?",
     ["0", "2", "3"],
     "Upside down, it still has the same mirror line, straight down from the middle of the top side to the bottom corner: <b>1</b> line."),
    ("turned equilateral triangle", "This equilateral triangle has been turned a little. How many lines of symmetry does it have?",
     ["0", "1", "6"],
     "It still has 3 equal sides, so it still has <b>3</b> mirror lines, one from each corner. They are all slanting now."),
    ("turned kite", "This kite has been turned. How many lines of symmetry does it have?",
     ["0", "2", "4"],
     "The mirror line still joins the 2 corners where the equal sides meet. It slants now, but there is still <b>1</b> line."),
    ("turned parallelogram", "This parallelogram has been turned. How many lines of symmetry does it have?",
     ["2", "1", "4"],
     "A parallelogram has <b>0</b> mirror lines, whichever way it is turned. Its diagonals split it into equal halves, but they do not fit when folded."),
    ("right-angled isosceles triangle", "This right-angled triangle has 2 equal sides. How many lines of symmetry does it have?",
     ["0", "2", "3"],
     "The mirror line is <b>slanting</b>: from the right angle to the middle of the longest side. No line goes straight up "
     "or across, but there is still <b>1</b> line."),
    ("L shape", "Both arms of this L shape are the same size. How many lines of symmetry does it have?",
     ["0", "2", "4"],
     "Up and down and across do not work. The slanting line from the inside corner to the outside corner folds one arm onto "
     "the other: <b>1</b> line."),
    ("turned hexagon", "This regular hexagon has been turned. How many lines of symmetry does it have?",
     ["0", "3", "2"],
     "Turning does not change the shape, so it still has <b>6</b> mirror lines: 3 join opposite corners and 3 join the middles of opposite sides."),
]


def set_turned(rnd):
    its = []
    singles = [it("turned rectangle", 62), it("turned square", 90), it("turned isosceles triangle", 0),
               it("turned rectangle", 90), corner_line("turned parallelogram", 0, 2), it("right-angled isosceles triangle", 135)]
    kinds = []
    for name, F, p, a in singles:
        its.append(line_q(name, F, p, a % 180, rnd, turned=True))
        kinds.append(split_kind(F, p, a % 180))
    assert kinds.count("Y") == 4 and kinds.count("N2") == 2, kinds
    for name, qs, wrong, e in TURN_Q:
        F = shp(name)
        lab = "%s that has been turned" % noun(name) if name.startswith(("turned", "upside")) else noun(name)
        its.append(mcq(fig(single_svg(F, label=lab)) + qs, str(LINES[name]), wrong, e, rnd))
    POOL = pool_kinds({
        "tr_a": it("turned rectangle", 62), "tr_b": it("turned rectangle", 152), "tr_v": it("turned rectangle", 90),
        "tsq_v": it("turned square", 90), "tsq_h": it("turned square", 0), "tiso_h": it("turned isosceles triangle", 0),
        "uiso_v": it("upside-down isosceles triangle", 90), "teq_a": it("turned equilateral triangle", 105),
        "tkite_a": it("turned kite", 150), "thex_a": it("turned hexagon", 15), "ttrap_h": it("turned trapezium", 0),
        "ri_d": it("right-angled isosceles triangle", 135), "tpara_d": corner_line("turned parallelogram", 0, 2),
        "tpara_v": it("turned parallelogram", 90), "tr_d": corner_line("turned rectangle", 0, 2),
        "tsq_off": it("turned square", 90, 0.3), "thex_off": it("turned hexagon", 0, 0.28),
    })
    plans = [("is", ("teq_a", ["tr_d", "tpara_v", "thex_off"])), ("not", ("tr_v", ["tsq_h", "tkite_a", "ri_d"])),
             ("is", ("tiso_h", ["tr_v", "tpara_d", "tsq_off"])), ("not", ("tpara_d", ["thex_a", "uiso_v", "ttrap_h"]))]
    its += panel_qs(plans, POOL, rnd, extra_rect="tr_d")
    assert len(its) == 20
    return {"title": "Turned shapes and slanting mirror lines", "items": its}


# ============================================================ set 4: complete the figure on a grid
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
        elif k == "upright":
            # flipped as if the mirror line went straight up and down through the middle of the grid
            s = frozenset(half | {(cols - 1 - c, r) for c, r in half})
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


OPT_WHY = {"slide": "the half was slid across, not flipped (squares counted from the wrong edge)",
           "turn": "the half was turned upside down, not flipped",
           "upright": "it was flipped as if the mirror line went straight up and down",
           "moved": "one square is in the wrong place", "missing": "one square is missing"}

V_HALVES = [
    ["..#", ".##", "#.#", "###", "..#"],
    ["#..", "##.", "###", ".#.", ".##"],
    ["...#", "..##", ".###", "#..#", "...#"],
    ["#..#", ".###", "..##", ".#.#", "##.#"],
    [".#.", "###", "#.#", "..#", ".##"],
    ["##..", ".##.", "..##", ".#.#", "...#"],
]
H_HALVES = [
    ["...#..", "..###.", "#####."],
    ["#.....", "###...", ".#####"],
    ["..##..", "#.#..#", "######"],
    [".#....", "##.##.", "######"],
]
D_HALVES = [
    ("d", ["#....", "##...", "#.#..", "###..", "..##."]),
    ("a", ["###..", "#.#..", "##...", "#....", "....."]),
    ("d", [".....", "#....", ".#...", "####.", "#..##"]),
    ("a", ["..##.", ".##..", "#.#..", "##...", "#...."]),
    ("d", ["#....", ".#...", "###..", ".#.#.", "#####"]),
    ("a", ["#.#.#", "###..", "#.#..", ".#...", "#...."]),
]
COUNTS = [
    ("v", ["...#", "..##", ".#.#", "####", "#..."], "all"),
    ("h", ["..#...", ".##...", "####..", "#.####"], "all"),
    ("v", [".#..", "####", "..##", ".#.#", "...#"], "more"),
    ("h", ["....#.", "...##.", "#..###", "######"], "more"),
]


def grid_q(kind, h, rnd, spots):
    if kind == "v":
        w = len(h[0])
        cols, rows, line, wrongs = 2 * w, len(h), ("v", w), ["slide", "turn", "missing"]
    elif kind == "h":
        cols, rows, line, wrongs = len(h[0]), 2 * len(h), ("h", len(h)), ["slide", "turn", "moved"]
    else:
        cols = rows = 5
        line, wrongs = (("d",) if kind == "d" else ("a", 5)), ["upright", "turn", "moved"]
    half = cells_of(h)
    if kind == "d":
        assert all(r >= c for c, r in half)
    if kind == "a":
        assert all(c + r <= 4 for c, r in half)
    opts = options(half, line, cols, rows, rnd, wrongs)
    pos = spots.next()
    rnd.shuffle(wrongs)
    keys = wrongs[:pos] + ["ok"] + wrongs[pos:]
    cs = 12 if cols >= 8 else 14 if kind in "vh" else 15
    svg = grid_panel(cols, rows, [opts[k] for k in keys], line, cs, "four grid pictures A to D with a dashed mirror line")
    side = {"v": "left", "h": "top", "d": "bottom-left", "a": "top-left"}[kind]
    qs = (fig(svg) + "The dashed line is a mirror line. The %s half is the same in all 4 pictures. "
          "In which picture is the shape completed correctly?" % side)
    rule = {"v": "Each shaded square needs a partner in the same row, the same number of squares from the mirror line on the other side.",
            "h": "Each shaded square needs a partner in the same column, the same number of squares from the mirror line on the other side.",
            "d": "Each shaded square needs a partner straight across the slanting line, the same distance away. Row and column swap: "
                 "the square in row 4, column 2 pairs with the square in row 2, column 4.",
            "a": "Each shaded square needs a partner straight across the slanting line, the same distance away. "
                 "For example, the square in the top-left corner pairs with the square in the bottom-right corner."}[kind]
    others = "; ".join("%s: %s" % ("ABCD"[j], OPT_WHY[k]) for j, k in enumerate(keys) if k != "ok")
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
    svg = grid_svg(cols, rows, half, line, 18 if kind == "v" else 16, "grid with shaded squares on one side of a dashed mirror line")
    side = "to the right of the line" if kind == "v" else "below the line"
    if ask == "all":
        qs = (fig(svg) + "The mirror line runs through the middle of a %s. Shade squares %s to make the picture "
              "symmetrical. How many squares will be shaded altogether?" % (where, side))
        right = 2 * (n - m) + m
        wrong = [2 * n, 2 * (n - m), n]
        e = ("%d squares are shaded now. %d of them %s on the mirror line, so %s own partner: count %s once. "
             "The other %d each need a partner. %d + %d + %d = <b>%d</b>."
             % (n, m, "sits" if m == 1 else "sit", "it is its" if m == 1 else "each is its", "it" if m == 1 else "them",
                n - m, n - m, n - m, m, right))
    else:
        qs = (fig(svg) + "The mirror line runs through the middle of a %s. How many more squares must be shaded "
              "to make the picture symmetrical?" % where)
        right = n - m
        wrong = [n, 2 * n - m, m]
        e = ("Squares on the mirror line are their own partners. %d squares are shaded and %d %s on the line, "
             "so %d − %d = <b>%d</b> more squares." % (n, m, "sits" if m == 1 else "sit", n, m, right))
    return mcq(qs, right, wrong, e, rnd)


def set_grid(rnd):
    spots = Spots(rnd)
    seen = set()
    v, h, d, c = [], [], [], []
    for x in V_HALVES:
        q_, svg = grid_q("v", x, rnd, spots)
        v.append(q_); assert svg not in seen; seen.add(svg)
    for x in H_HALVES:
        q_, svg = grid_q("h", x, rnd, spots)
        h.append(q_); assert svg not in seen; seen.add(svg)
    for kind, x in D_HALVES:
        q_, svg = grid_q(kind, x, rnd, spots)
        d.append(q_); assert svg not in seen; seen.add(svg)
    for kind, x, ask in COUNTS:
        c.append(count_q(kind, x, ask, rnd))
    its = v + h + c + d
    assert len(its) == 20
    return {"title": "Complete the symmetrical picture on a grid", "items": its}


# ============================================================ set 5: symmetry in real life
OBJ = [
    (butterfly, "How many lines of symmetry does this butterfly picture have?", "butterfly", 1, ["2", "0", "4"],
     "Only the line straight down the body works: each wing lands on the wing opposite. Folded across, the big top wings "
     "would land on the small bottom wings. <b>1</b> line."),
    (leaf, "How many lines of symmetry does this leaf have?", "leaf with a stalk", 1, ["2", "0", "4"],
     "Fold along the middle vein: the veins on each side match. Folded across, the stalk has nothing to match, so there is just <b>1</b> line."),
    (flag_cross_mid, "This flag has a cross through the middle, like the flag of England. How many lines of symmetry does it have?",
     "flag with a cross through the middle", 2, ["4", "1", "0"],
     "Fold it up and down or across: the cross lands on itself both times. The diagonals do not work, because the flag is a "
     "rectangle, not a square. <b>2</b> lines."),
    (flag_saltire, "This flag has a cross from corner to corner, like the flag of Scotland. How many lines of symmetry does it have?",
     "flag with a cross from corner to corner", 2, ["4", "0", "1"],
     "The cross runs along the diagonals, but the diagonals of a rectangle are not mirror lines. Folding up and down or across "
     "does match the 2 bands: <b>2</b> lines."),
    (flag_halves, "This flag has a white top half and a green bottom half. How many lines of symmetry does it have?",
     "flag with a white top half and a green bottom half", 1, ["2", "0", "4"],
     "Folding across puts white on green, so it does not work: colours must match too. Folding up and down matches white with "
     "white and green with green: <b>1</b> line."),
    (flag_cross_side, "On this flag the cross is to the left of the middle. How many lines of symmetry does it have?",
     "flag with a cross to the left of the middle", 1, ["2", "0", "4"],
     "Folding up and down does not work, because the upright bar is not in the middle. Folding across does: <b>1</b> line."),
    (sign_octagon, "A road sign has this shape, with no writing on it. How many lines of symmetry does it have?",
     "octagon road sign", 8, ["4", "2", "6"],
     "It is a regular octagon: 4 lines join opposite corners and 4 join the middles of opposite sides. <b>8</b> lines. "
     "(With the word STOP on it, it would have none.)"),
    (sign_warning, "This warning sign has no picture inside yet. How many lines of symmetry does it have?",
     "red warning triangle", 3, ["1", "6", "2"],
     "It is an equilateral triangle. Each mirror line goes from a corner to the middle of the side opposite: <b>3</b> lines."),
    (sign_no_entry, "This road sign is a red circle with a white bar across it. How many lines of symmetry does it have?",
     "red circle with a white bar", 2, [INF, "1", "4"],
     "A plain circle has infinitely many, but the bar spoils most of them. Only the line across and the line up and down "
     "keep the bar on itself: <b>2</b> lines."),
    (sign_arrow, "This blue road sign has a white arrow pointing up. How many lines of symmetry does it have?",
     "blue circle with an arrow pointing up", 1, ["2", INF, "0"],
     "Only the line straight up through the arrow works. Folding across would put the arrow’s point on its tail: <b>1</b> line."),
]
LETTER_PANELS = [
    ("Which capital letter has a <b>horizontal</b> mirror line?", "E", "MTV",
     "Fold E across the middle and the top arm lands on the bottom arm. M, T and V have a vertical mirror line instead."),
    ("Which capital letter has <b>no</b> mirror line?", "F", "HAC",
     "F has no mirror line. H has 2, A has a vertical one and C has a horizontal one."),
    ("Which capital letter has <b>2</b> mirror lines?", "X", "AEW",
     "X matches when folded up and down and when folded across. A and W have only a vertical line, and E only a horizontal one."),
    ("Which capital letter has a <b>vertical</b> mirror line?", "Y", "BDC",
     "Fold Y straight down the middle and the 2 arms match. B, D and C have a horizontal line, not a vertical one."),
]
WORDS = [
    ("Amelia has a square paper napkin. In how many different ways can she fold it in half so that the two halves match exactly?",
     "4", ["2", "8", "1"],
     "A square has 4 lines of symmetry: up and down, across, and the 2 diagonals. So there are 4 ways."),
    ("Harry folds a rectangular tablecloth, 2 m long and 1 m wide, from one corner to the opposite corner. Do the two halves match?",
     "No, the corners stick out", ["Yes, the halves are equal", "Yes, every fold works", "No, it has no mirror lines"],
     "The diagonal splits the tablecloth into 2 equal triangles, but they do not fit on top of each other, because it is not "
     "a square. A rectangle has only 2 mirror lines."),
    ("Isla says a parallelogram has 2 lines of symmetry because its diagonals cut it in half. Is she right?",
     "No, it has 0", ["Yes, it has 2", "No, it has 4", "No, it has 1"],
     "Cutting a shape in half is not enough: the halves must fit when folded. Fold a slanting parallelogram any way and "
     "the corners stick out, so it has 0 lines of symmetry."),
    ("Oliver writes words in capital letters. Which word has a horizontal mirror line?",
     "CODE", ["TOY", "BOAT", "SAND"],
     "C, O, D and E each have a horizontal mirror line, so a fold across the middle of the whole word CODE works. "
     "T, Y and A only have vertical lines, and S and N have none."),
    ("Aisha cuts out a paper circle. How many different fold lines will make the two halves match?",
     INF, ["4", "2", "0"],
     "Every line through the centre of a circle is a line of symmetry, so there are infinitely many. Up and down, across "
     "and the 2 diagonals are just 4 of them."),
    ("Poppy folds a sheet of paper in half, cuts a shape along the fold and opens it out. What must be true?",
     "The fold is a mirror line", ["It has no mirror lines", "It has exactly 2 mirror lines", "One half is bigger"],
     "Both halves were cut at the same time, so each is the mirror image of the other. The fold is always a line of symmetry. "
     "The shape might have other mirror lines too, but it does not have to."),
]


def set_world(rnd):
    its = []
    for make, qs, label, n, wrong, e in OBJ:
        F = expect(make(), n, label)
        its.append(mcq(fig(single_svg(F, label=label)) + qs, str(n), wrong, e, rnd))
    spots = Spots(rnd)
    for qs, good, bads, e0 in LETTER_PANELS:
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
        else:
            ok = [k for k in keys if len(a[k]) == 2]
        assert ok == [good], (qs, keys, a)
        its.append(mcq_fixed(fig(letter_row_svg(keys)) + qs, keys, pos, e0))
    # check the letters named in the word questions
    for w in ("CODE",):
        assert all(KIND[ch] in "hb" for ch in w)
    for w in ("TOY", "BOAT", "SAND"):
        assert not all(KIND[ch] in "hb" for ch in w if ch in KIND)
    for qs, right, wrong, e in WORDS:
        its.append(mcq(qs, right, wrong, e, rnd))
    assert len(its) == 20
    return {"title": "Symmetry in real life: flags, signs and letters", "items": its}


def letter_row_svg(keys, cw=74):
    el = []
    H = 92
    for k, ch in enumerate(keys):
        e, bb = render(letter(ch), [], 50, 70, k * cw + cw / 2.0, H / 2.0)
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 2 and bb[3] <= H - 2, (ch, bb)
        el += e
        if k:
            el.append("<line x1='%d' y1='6' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (k * cw, k * cw, H - 6, GRAY))
    return svg_wrap(cw * len(keys), H, "".join(el), "four letters in a row: " + ", ".join(keys))


# ============================================================ lesson
def body_html():
    r = shp("rectangle")
    rd = math.degrees(math.atan2(76, 132))
    f1 = strip_svg([(r, [dash_seg(r, center(r), 90)], "Mirror line"),
                    (r, [dash_seg(r, center(r), rd)], "Not a mirror line")],
                   "a rectangle with an up-and-down dashed line and a rectangle with a diagonal dashed line", cw=170)
    shapes = ["square", "rectangle", "equilateral triangle", "parallelogram"]
    f2 = strip_svg([(shp(k), all_axis_segs(shp(k)), lines_word(LINES[k])) for k in shapes],
                   "a square with 4 lines of symmetry, a rectangle with 2, an equilateral triangle with 3 and a parallelogram with 0")
    turned = ["turned square", "turned rectangle", "turned isosceles triangle", "right-angled isosceles triangle"]
    f3 = strip_svg([(shp(k), all_axis_segs(shp(k)), lines_word(LINES[k])) for k in turned],
                   "a turned square with 4 mirror lines, a turned rectangle with 2, an isosceles triangle on its side with 1 "
                   "and a right-angled isosceles triangle with 1 slanting mirror line")
    half = cells_of(["..#", ".##", "#.#", "###", "..#"])
    full = half | {mir(x, ("v", 3)) for x in half}
    f4 = grid_svg(6, 5, full, ("v", 3), 24, "a grid picture completed across a vertical dashed mirror line", light=full - half)
    dh = cells_of(["#....", "##...", "#.#..", "###..", "..##."])
    dfull = dh | {mir(x, ("d",)) for x in dh}
    f5 = grid_svg(5, 5, dfull, ("d",), 24, "a grid picture completed across a diagonal dashed mirror line", light=dfull - dh)
    return (
        "<h2>What is a line of symmetry?</h2>"
        "<p>A <b>line of symmetry</b> (also called a <b>mirror line</b>) splits a shape into two halves that fit exactly on "
        "top of each other when you fold along it. Each half is a mirror image of the other.</p>"
        "<p>To test a line, imagine folding the shape along it, or stand a small mirror on the line: if the reflection shows the "
        "whole shape, it is a mirror line.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Fold the first rectangle along the dashed line: the halves match. The diagonal also splits the rectangle "
        "into 2 equal triangles, but when you fold, the corners stick out. So it is not a mirror line.</figcaption></figure>"
        "<h2>Count every mirror line</h2>"
        "<p>Try every way to fold: up and down, across and slanting. A shape can have many mirror lines, one, or none.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>A square has 4 mirror lines (2 are diagonals). A rectangle has only 2. An equilateral triangle has 3. "
        "A parallelogram has none.</figcaption></figure>" +
        table(["Shape", "Lines of symmetry"], [
            ["Square", "4"], ["Rectangle (not a square)", "2"], ["Rhombus (not a square)", "2 (corner to corner)"],
            ["Equilateral triangle", "3"], ["Isosceles triangle", "1"], ["Scalene triangle", "0"],
            ["Kite", "1"], ["Isosceles trapezium", "1"], ["Parallelogram (slanting sides)", "0"],
            ["Regular pentagon, hexagon, octagon", "5, 6, 8 (as many as the sides)"], ["Circle", "Infinitely many"],
        ]) +
        "<h2>Turned shapes</h2>"
        "<p>Turning a shape does <b>not</b> change how many mirror lines it has. The lines simply turn with the shape, so they "
        "may now slant. Do not look only for lines that go straight up and down.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>A square standing on a corner still has 4 mirror lines. A turned rectangle still has 2. "
        "These triangles have 1 each, going across or slanting.</figcaption></figure>"
        "<h2>Complete a symmetrical picture</h2>"
        "<p>Give every shaded square a partner on the other side of the mirror line, the <b>same number of squares away</b> "
        "from the line. Count from the mirror line, not from the edge of the grid. Flip the half; do not slide it.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>The dark squares were given. The light squares are their reflections: same row, same distance from the line.</figcaption></figure>"
        "<p>With a diagonal mirror line, each square’s partner is straight across the line at a right angle, the same "
        "distance away. Its row and column numbers swap over.</p>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>Reflected in the diagonal line: the square in row 4, column 2 has its partner in row 2, column 4.</figcaption></figure>" +
        ex("Worked example", "How many lines of symmetry does a regular hexagon have?",
           "3 lines join opposite corners. 3 more join the middles of opposite sides. 3 + 3 = 6.", "6") +
        ex("Worked example", "A rectangle is turned so its sides slant. How many mirror lines does it have now?",
           "Turning does not change the shape. It is still a rectangle, so its 2 mirror lines just slant too.", "2") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a rectangle’s diagonals as mirror lines", "Fold on a diagonal: the corners stick out. A rectangle has 2"],
            ["Saying a parallelogram has 2 lines", "Its diagonals cut it in half, but the halves do not fit. It has 0"],
            ["Looking only for vertical lines", "Mirror lines can go across or slant, especially on turned shapes"],
            ["Sliding the half when completing a picture", "Flip it: each square goes the same distance on the other side"],
            ["Counting squares from the edge of the grid", "Count from the mirror line on both sides"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 children learn about symmetry?",
     "a": "In the National Curriculum, Year 4 pupils find lines of symmetry in 2-D shapes, including shapes that are turned, and complete a simple symmetrical figure using a given mirror line."},
    {"q": "Is a mirror line the same as a line of symmetry?",
     "a": "Yes. Both names mean a line that splits a shape into two halves that match exactly when folded. If you stand a mirror on it, the reflection completes the shape."},
    {"q": "Does a rectangle have 4 lines of symmetry?",
     "a": "No. A rectangle that is not a square has 2 lines of symmetry: up and down, and across. Its diagonals split it in half, but the halves do not fit when folded."},
    {"q": "How many lines of symmetry does a circle have?",
     "a": "Infinitely many. Any straight line through the centre of a circle is a line of symmetry."},
]


def gen_symmetry():
    rnd = random.Random(4415)
    sets = [set_is_line(rnd), set_count(rnd), set_turned(rnd), set_grid(rnd), set_world(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "lines-of-symmetry", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Lines of Symmetry",
        "seo_title": "Year 4 Lines of Symmetry Worksheets: Mirror Lines in Shapes and Grids (Free, with Answers)",
        "short_title": "Lines of symmetry",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 4: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Identify lines of symmetry in 2-D shapes presented in different orientations; complete a simple symmetric figure with respect to a specific line of symmetry.",
        "meta_desc": "Free Year 4 lines of symmetry worksheets for the National Curriculum: test mirror lines, count lines of symmetry in 2-D shapes, spot them in turned shapes, complete symmetrical pictures on a grid, and find symmetry in flags, road signs and letters. 100 questions with an answer key.",
        "key_big": "A mirror line splits a shape into two halves that fit exactly when folded – whichever way the shape is turned.",
        "key_sub": "A square has 4 mirror lines, a rectangle only 2, a parallelogram none. Turning a shape does not change its mirror lines; they just slant.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, grids) so their labels stay readable."""
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
