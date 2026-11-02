# -*- coding: utf-8 -*-
"""
Australia Year 3 Maths: 3-D objects (Australian Curriculum v9.0, AC9M3SP01)
  python3 tools/gen_au_maths_y3_objects.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English.

Year 3 students make, compare and classify objects (cube, rectangular prism, triangular prism,
square-based pyramid, cylinder, cone, sphere), name their key features (faces, edges, vertices,
flat and curved surfaces) and explain why those features suit their uses (rolling, sliding, stacking).

Pictures (checked in code):
  objects with flat faces  drawn from 3-D vertices and faces, turned (yaw) and seen from a little above (pitch);
              a face is shown when it faces the viewer, edges of hidden faces only are dashed;
              faces, edges and vertices are counted from the same data (V − E + F = 2), and the
              "only counted what you can see" wrong answers are counted from the same picture
  models      straw-and-connector models: one straw for each edge, one connector for each vertex
Wrong answers come from real student mistakes: counting only the faces you can see, edges and vertices
swapped, prism vs pyramid, a cylinder called a circle (2-D name for a 3-D object), cylinder vs cone,
cube vs rectangular prism.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
STRAW = "#d99a2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

CUBE, RP, TP, SP = "cube", "rectangular prism", "triangular prism", "square-based pyramid"
CYL, CONE, SPH = "cylinder", "cone", "sphere"


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


class Pos:
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ drawing
def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count("-") * 0.3) * fs * 0.6


def circle_pts(c, r, n=72):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


class Canvas:
    """Collects shapes (screen coordinates, y down), tracks the bounding box, then writes a tight SVG."""

    def __init__(self):
        self.el = []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.4, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=2.4, col=GREEN):
        self.el.append(("c", c, r, fill, sw, col))
        self.grow(c[0] - r - sw, c[1] - r - sw, c[0] + r + sw, c[1] + r + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("pl", pts, dashed, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                st = " stroke='%s' stroke-width='%g'" % (col, sw) if sw else ""
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'%s/>" % (c[0] - ox, c[1] - oy, r, fill, st))
            elif e[0] == "l":
                _, a, b, dashed, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, pts, dashed, sw, col = e
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
        return "".join(s)

    def size(self):
        return self.x1 - self.x0, self.y1 - self.y0

    def svg(self, label, pad=5):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1                                    # keep figures out of the larger 'square' print size
        return svg_wrap(W, H, self.body(ox, oy), label)


def row_svg(cvs, caps, label, gap=24, fs=16, col=INK):
    """Pictures side by side with a caption under each."""
    H = max(cv.size()[1] for cv in cvs)
    parts, x = [], 0
    for cv, cap in zip(cvs, caps):
        w, h = cv.size()
        cw = max(w, tw(cap, fs) + 4)
        ox = cv.x0 - (x + (cw - w) / 2)
        oy = cv.y0 - (H - h) / 2
        parts.append(cv.body(ox, oy))
        if cap:
            parts.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x + cw / 2, H + 8 + fs * 0.86, fs, col, cap))
        x += cw + gap
    W = x - gap
    pad = 5
    capH = 8 + fs * 1.1 if any(caps) else 0
    body = "<g transform='translate(%d,%d)'>%s</g>" % (pad, pad, "".join(parts))
    return svg_wrap(int(math.ceil(W + 2 * pad)), int(math.ceil(H + capH + 2 * pad)), body, label)


def grid_svg(cvs, label, cell=118):
    """2 x 2 grid of pictures labelled A-D."""
    W = H = 2 * cell
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, cell, H - 4, GRAY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, W - 4, cell, GRAY)]
    for k, cv in enumerate(cvs):
        x0, y0 = (k % 2) * cell, (k // 2) * cell
        aw, ah = cell - 26, cell - 10
        w, h = cv.size()
        assert w <= aw and h <= ah, ("too big for the grid", w, h)
        ox = cv.x0 - (x0 + 21 + (aw - w) / 2)
        oy = cv.y0 - (y0 + 5 + (ah - h) / 2)
        s.append(cv.body(ox, oy))
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(s), label)

# ------------------------------------------------------------ 3-D shapes
class Solid:
    def __init__(self, verts, faces):
        self.v, self.f = verts, faces
        edges = {}
        for fi, fc in enumerate(faces):
            for i in range(len(fc)):
                e = tuple(sorted((fc[i], fc[(i + 1) % len(fc)])))
                edges.setdefault(e, []).append(fi)
        assert all(len(x) == 2 for x in edges.values())
        self.edges = edges
        F, E, V = len(faces), len(edges), len(verts)
        assert V - E + F == 2, (V, E, F)
        self.count = {"faces": F, "edges": E, "vertices": V}

    def view(self, yaw, pitch):
        """Turn the solid by yaw about the up axis, then tip it towards the viewer by pitch.
        Returns the points in view space and which faces the viewer can see (viewer at -z)."""
        cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
        pts = []
        for x, y, z in self.v:
            x1, z1 = x * cy_ + z * sy_, -x * sy_ + z * cy_
            y2, z2 = y * cp + z1 * sp, -y * sp + z1 * cp
            pts.append((x1, y2, z2))
        c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
        vis, nrm = [], []
        for fc in self.f:
            a, b, d = (pts[i] for i in fc[:3])
            u = [b[i] - a[i] for i in range(3)]
            w = [d[i] - a[i] for i in range(3)]
            n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
            m = [sum(pts[i][j] for i in fc) / len(fc) for j in range(3)]
            if sum(n[i] * (m[i] - c[i]) for i in range(3)) < 0:
                n = [-x for x in n]
            L = math.sqrt(sum(x * x for x in n))
            n = [x / L for x in n]
            nrm.append(n)
            vis.append(n[2] < -1e-6)
        return pts, vis, nrm

    def seen(self, yaw, pitch):
        """How many faces, edges and vertices can be seen in this picture."""
        _, vis, _ = self.view(yaw, pitch)
        F = sum(vis)
        E = sum(1 for fs in self.edges.values() if any(vis[f] for f in fs))
        V = len({i for fi, fc in enumerate(self.f) if vis[fi] for i in fc})
        return {"faces": F, "edges": E, "vertices": V}

    def cv(self, k, yaw=30, pitch=20):
        pts, vis, nrm = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        cv = Canvas()
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = nrm[fi]
                col = TOP3 if n[1] > 0.5 else SIDE if n[0] > 0.3 else FILL
                cv.poly([P(pts[i]) for i in fc], col, 2.4)
        for (a, b), fs in self.edges.items():
            if not any(vis[f] for f in fs):
                cv.line(P(pts[a]), P(pts[b]), dashed=True, sw=1.6)
        return cv

    def model_cv(self, k, yaw=30, pitch=20):
        """Straw-and-connector model: every edge is a straw, every vertex a connector."""
        pts, vis, _ = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        cv = Canvas()
        back = [e for e, fs in self.edges.items() if not any(vis[f] for f in fs)]
        front = [e for e in self.edges if e not in back]
        for a, b in back:
            cv.line(P(pts[a]), P(pts[b]), sw=3.5, col="#e9c27a")
        for a, b in front:
            cv.line(P(pts[a]), P(pts[b]), sw=4, col=STRAW)
        for i in sorted(range(len(pts)), key=lambda i: -pts[i][2]):
            cv.circle(P(pts[i]), 6, fill=RED, sw=1.2, col="#7a2318")
        return cv


def box(L, H, W):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid(v, f)


def prism_lying(w=1.2, h=0.95, D=1.8):
    """Triangular prism lying on a rectangle face: triangle ends in the y-z plane, length along x."""
    tri = [(0, 0), (w, 0), (w / 2, h)]          # (z, y)
    v = [(0, y, z) for z, y in tri] + [(D, y, z) for z, y in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(v, f)


def prism_standing(w=1.1, d=0.95, H=1.5):
    """Triangular prism standing on a triangle face."""
    tri = [(0, 0), (w, 0), (w / 2, d)]          # (x, z)
    v = [(x, 0, z) for x, z in tri] + [(x, H, z) for x, z in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(v, f)


def pyramid(s=1.3, h=1.3):
    v = [(0, 0, 0), (s, 0, 0), (s, 0, s), (0, 0, s), (s / 2, h, s / 2)]
    f = [[0, 1, 2, 3]] + [[i, (i + 1) % 4, 4] for i in range(4)]
    return Solid(v, f)


COUNTS = {CUBE: (6, 12, 8), RP: (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5)}
for _s, _k in [(box(1, 1, 1), CUBE), (box(1.8, 1, 0.9), RP), (prism_lying(), TP), (prism_standing(), TP), (pyramid(), SP)]:
    assert tuple(_s.count[x] for x in ("faces", "edges", "vertices")) == COUNTS[_k], _k

# every picture used: (solid, yaw, pitch)
VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "rp_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "rp_tall": (lambda: box(0.8, 1.8, 0.7), 35, 18),
    "rp_turned": (lambda: box(1.6, 1.0, 0.8), -35, 24),
    "tp_lying": (lambda: prism_lying(), 30, 20),
    "tp_end": (lambda: prism_lying(), 120, 25),
    "tp_standing": (lambda: prism_standing(), 20, 35),
    "sp": (lambda: pyramid(), 25, 18),
    "sp_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "rp_flat": RP, "rp_tall": RP, "rp_turned": RP,
             "tp_lying": TP, "tp_end": TP, "tp_standing": TP, "sp": SP, "sp_turned": SP}
for _v, (_f, _y, _p) in VIEWS.items():
    _s = _f()
    assert tuple(_s.count[x] for x in ("faces", "edges", "vertices")) == COUNTS[VIEW_KIND[_v]], _v
    _seen = _s.seen(_y, _p)
    assert 1 < _seen["faces"] < _s.count["faces"], (_v, _seen)


def solid_cv(view, k=50):
    f, yaw, pitch = VIEWS[view]
    return f().cv(k, yaw, pitch)


def model_cv(view, k=55):
    f, yaw, pitch = VIEWS[view]
    return f().model_cv(k, yaw, pitch)


def seen(view):
    f, yaw, pitch = VIEWS[view]
    return f().seen(yaw, pitch)


# ------------------------------------------------------------ curved 3-D shapes (drawn flat, then turned)
def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _rot90(pts, on):
    return [(-y, x) for x, y in pts] if on else pts


def cylinder_cv(s=1.0, lying=False):
    rx, ry, h = 36 * s, 11 * s, 72 * s
    R = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(R(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), FILL, 0.01)
    cv.poly(R(ellipse(0, 0, rx, ry, 0, 360)[:-1]), TOP3, 2.4)
    cv.pline(R([(-rx, 0), (-rx, h)]))
    cv.pline(R([(rx, 0), (rx, h)]))
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def cone_cv(s=1.0, how="up"):
    """how: 'up' (point at the top), 'down' (point at the bottom, like an ice-cream cone), 'side' (lying down)."""
    rx, ry, h = 38 * s, 11 * s, 80 * s
    cv = Canvas()
    if how == "down":
        cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), FILL, 0.01)
        cv.pline([(-rx, 0), (0, h), (rx, 0)])
        cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
        return cv
    R = lambda p: _rot90(p, how == "side")
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 180, 0)), FILL, 0.01)
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 0, 180)), FILL, 0.01)
    cv.pline(R([(-rx, h), (0, 0), (rx, h)]))
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def sphere_cv(s=1.0):
    r = 40 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill=FILL, sw=2.4)
    cv.pline(ellipse(0, 0, r, r * 0.3, 0, 180), sw=1.6)
    cv.pline(ellipse(0, 0, r, r * 0.3, 180, 360), dashed=True, sw=1.2)
    return cv


def pic3d(key, s=1.0):
    """Any 3-D picture by key. s scales it (1.0 = full size for one picture)."""
    if key in VIEWS:
        return solid_cv(key, 50 * s)
    if key == "cyl":
        return cylinder_cv(s)
    if key == "cyl_lying":
        return cylinder_cv(s, lying=True)
    if key.startswith("cone"):
        return cone_cv(s, {"cone": "up", "cone_down": "down", "cone_side": "side"}[key])
    if key == "sphere":
        return sphere_cv(s)
    raise KeyError(key)


KIND = dict(VIEW_KIND, cyl=CYL, cyl_lying=CYL, cone=CONE, cone_down=CONE, cone_side=CONE, sphere=SPH)


def art(n):
    return "an" if n[0] in "aeiou" else "a"

def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. A-D picture questions keep their order."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [5 - c for c in cnt]
        assert min(need) >= 0 and sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, pairs) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u



# ------------------------------------------------------------ set 1: naming objects
WRONG3 = {CUBE: [RP, "square", SP], RP: [CUBE, "rectangle", TP], TP: [SP, RP, "triangle"],
          SP: [TP, CONE, "square"], CYL: ["circle", CONE, TP], CONE: [CYL, "triangle", SP], SPH: ["circle", CYL, CONE]}
E3 = {
    CUBE: "It has 6 faces and they are all squares of the same size, so it is a cube.",
    RP: "It has 6 rectangle faces and they are not all squares, so it is a rectangular prism.",
    TP: "It has 2 triangle faces at the ends, joined by 3 rectangles, so it is a triangular prism.",
    SP: "It has a square face at the bottom and 4 triangle faces that meet at a point, so it is a square-based pyramid.",
    CYL: "It has 2 flat circle faces at the ends and a curved surface, so it is a cylinder. A circle is only a flat 2-D shape.",
    CONE: "It has 1 flat circle face and a curved surface that comes to a point, so it is a cone.",
    SPH: "It is round all over, like a ball, so it is a sphere. A circle is a flat 2-D shape.",
}
TURN3 = {"cube_turned": " It is turned, but it is still a cube.",
         "rp_tall": " It is standing on its end, but it is still a rectangular prism.",
         "rp_turned": " It is turned, but it is still a rectangular prism.",
         "tp_end": " It is turned so you see a triangle end at the front.",
         "tp_standing": " It is standing on a triangle face, but it is still a triangular prism.",
         "sp_turned": " It is turned, but it is still a square-based pyramid.",
         "cyl_lying": " It is lying on its side, but it is still a cylinder.",
         "cone_down": " It is upside down, but it is still a cone.",
         "cone_side": " It is lying on its side, but it is still a cone."}


def set_name(rnd, pos):
    its = []
    asks = ["What is the name of this object?", "Name this 3-D object.", "What is this object called?"]
    keys = ["cube", "cube_turned", "rp_flat", "rp_tall", "rp_turned", "tp_lying", "tp_standing", "tp_end", "sp", "sp_turned",
            "cyl", "cyl_lying", "cone", "cone_down", "cone_side", "sphere"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        e = E3[kind] + TURN3.get(k, "")
        if kind == TP:
            e += " A pyramid comes to a point; a prism does not."
        its.append(mcq(fig(pic3d(k).svg("a 3-D object")) + asks[i % 3], kind, WRONG3[kind], e))
    q = (fig(row_svg([pic3d("tp_lying", 0.8), pic3d("tp_standing", 0.8)], ["", ""], "the same 3-D object in two positions", gap=40))
         + "Both pictures show the same object in different positions. What is it?")
    its.append(mcq(q, TP, WRONG3[TP], E3[TP] + " Turning an object does not change its name."))
    for kind, right, others, why in [
            (CONE, "cone_side", ["cyl_lying", "sp", "tp_end"], "it has 1 circle face and comes to a point. It is lying on its side"),
            (RP, "rp_tall", ["cube", "tp_lying", "cyl"], "it has 6 rectangle faces that are not all squares. It is standing on its end"),
            (CYL, "cyl_lying", ["cone", "sphere", "rp_flat"], "it has 2 circle faces and a curved surface. It is lying on its side"),
    ]:
        p = pos.next()
        cells = [pic3d(k, 0.62) for k in others]
        cells.insert(p, pic3d(right, 0.62))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 3-D objects labelled A to D")) + "Which picture shows %s %s?" % (art(kind), kind),
                             list("ABCD"), "ABCD"[p], "%s is %s %s: %s." % ("ABCD"[p], art(kind), kind, why)))
    assert len(its) == 20, len(its)
    return {"title": "Name 3-D objects in any position", "items": its}


# ------------------------------------------------------------ set 2: faces, edges and vertices
def set_fev(rnd):
    its = []
    its.append(mcq("A flat surface of an object is called a …", "face", ["edge", "vertex", "corner"],
                   "A face is a flat surface. An edge is where two faces meet. A vertex is a corner."))
    its.append(mcq("The line where two faces of an object meet is called an …", "edge", ["vertex", "face", "angle"],
                   "Where two faces meet there is an edge."))
    its.append(mcq("A corner of an object, where edges meet, is called a …", "vertex", ["edge", "face", "side"],
                   "A corner is a vertex. More than one vertex are called vertices."))
    hidden = {"faces": "Some faces are at the back or underneath. You cannot see them, but you must count them too.",
              "edges": "The dashed lines show edges at the back. Count them too.",
              "vertices": "Some vertices are at the back, where the dashed lines meet. Count them too."}
    for view, what in [("cube", "faces"), ("cube", "edges"), ("cube_turned", "vertices"), ("rp_flat", "faces"),
                       ("rp_turned", "edges"), ("tp_lying", "faces"), ("tp_lying", "edges"), ("tp_standing", "vertices"),
                       ("sp", "faces"), ("sp", "edges"), ("sp_turned", "vertices")]:
        kind = VIEW_KIND[view]
        F, E, V = COUNTS[kind]
        cnt = {"faces": F, "edges": E, "vertices": V}
        ans = cnt[what]
        vis = seen(view)[what]
        assert vis < ans
        others = [cnt[w] for w in ("faces", "edges", "vertices") if w != what]
        wrong = [vis] + others + [ans + 1, ans - 1]
        q = fig(solid_cv(view).svg("a %s" % kind)) + "This is %s %s. How many %s does it have?" % (art(kind), kind, what)
        e = "%s %s has %d faces, %d edges and %d vertices. %s" % (art(kind).capitalize(), kind, F, E, V, hidden[what])
        if kind == SP and what == "vertices":
            e += " Do not forget the vertex at the top."
        its.append(mcq(q, ans, wrong, e))
    its.append(mcq("Which 2-D shapes are the faces of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "2 triangles and 2 rectangles", "1 triangle and 4 rectangles"],
                   "A triangular prism has a triangle at each end (2 triangles) and 3 rectangles joining them: 5 faces."))
    its.append(mcq("Which 2-D shapes are the faces of a square-based pyramid?", "1 square and 4 triangles",
                   ["4 squares and 1 triangle", "1 square and 3 triangles", "2 squares and 4 triangles"],
                   "A square-based pyramid has 1 square at the bottom and 4 triangles that meet at the top: 5 faces."))
    its.append(mcq("Which object has 5 vertices?", SP, [TP, CUBE, CONE],
                   "A square-based pyramid has 4 vertices round the square and 1 at the top: 4 + 1 = 5. A triangular prism has 6."))
    its.append(mcq("How many vertices does a rectangular prism have?", 8, [12, 6, 4],
                   "A rectangular prism has 8 vertices: 4 at the top and 4 at the bottom. 12 is the number of edges."))
    its.append(mcq("Leo says a cube has 8 edges. He is wrong. What did he count?", "the vertices",
                   ["the faces", "the edges at the front", "the hidden faces"],
                   "A cube has 8 vertices (corners) and 12 edges. Leo counted the vertices."))
    its.append(mcq("Zara counts 12 on a rectangular prism. She is right. What did she count?", "the edges",
                   ["the faces", "the vertices", "the faces she can see"],
                   "A rectangular prism has 6 faces, 12 edges and 8 vertices. So 12 is the number of edges."))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 3: flat and curved surfaces
def set_surfaces(rnd, pos, P):
    its = []
    its.append(mcq("Which object has only flat surfaces?", CUBE, [CYL, CONE, SPH],
                   "A cube has 6 flat faces and no curved surface. A cylinder, a cone and a sphere all have a curved surface."))
    its.append(mcq("Which object has only a curved surface?", SPH, [CYL, CONE, CUBE],
                   "A sphere is curved all over. It has no flat faces, no edges and no vertices."))
    its.append(mcq("Which object has 2 flat faces and 1 curved surface?", CYL, [CONE, SPH, TP],
                   "A cylinder has a flat circle face at each end and 1 curved surface round the side. A cone has only 1 flat face."))
    its.append(mcq(fig(cone_cv().svg("a cone")) + "How many flat faces does a cone have?", 1, [2, 0, 3],
                   "A cone has 1 flat circle face at the bottom. The rest is a curved surface that comes to a point."))
    its.append(mcq(fig(cylinder_cv().svg("a cylinder")) + "How many curved surfaces does a cylinder have?", 1, [2, 0, 3],
                   "A cylinder has 1 curved surface that goes all the way round. The 2 circles at the ends are flat faces, not curved surfaces."))
    its.append(mcq("Which object can roll in every direction?", SPH, [CYL, CONE, CUBE],
                   "A sphere is curved all over, so it can roll any way you push it. A cylinder rolls only in a straight line."))
    its.append(mcq(fig(cylinder_cv(lying=True).svg("a cylinder lying on its side")) + "You give this cylinder a push. What does it do?",
                   "It rolls in a straight line.", ["It rolls round in a circle.", "It cannot move.", "It rolls in every direction."],
                   "Lying on its curved surface, a cylinder rolls in a straight line. A cone rolls round in a circle and a sphere rolls in every direction."))
    its.append(mcq(fig(cone_cv(how="side").svg("a cone lying on its side")) + "You give this cone a push. What does it do?",
                   "It rolls round in a circle.", ["It rolls in a straight line.", "It cannot roll at all.", "It rolls in every direction."],
                   "The point of the cone stays in one place and the wide end goes round it, so a cone rolls round in a circle."))
    its.append(mcq(fig(cylinder_cv().svg("a cylinder standing on a flat face")) + "This cylinder stands on a flat face. You push it gently. What does it do?",
                   "It slides.", ["It rolls.", "It rolls round in a circle.", "It bounces."],
                   "It is standing on a flat circle face, so it slides. It can roll only when it lies on its curved surface."))
    its.append(mcq("Which object can slide but cannot roll?", RP, [CYL, SPH, CONE],
                   "A rectangular prism has only flat faces, so it slides. Objects with a curved surface can roll."))
    its.append(mcq("Which object can roll and can also slide?", CYL, [CUBE, TP, SP],
                   "A cylinder rolls on its curved surface and slides on a flat face. Objects with only flat faces cannot roll."))
    its.append(mcq("Which object is best for building a tall, steady tower?", CUBE, [SPH, CONE, SP],
                   "A cube has flat faces on top and underneath, so cubes sit flat on each other. Spheres roll off, and you cannot stack on a point."))
    its.append(mcq("Why is it hard to stack one sphere on top of another?", "It has no flat face to sit on.",
                   ["It has too many faces.", "It has 8 vertices.", "It is too heavy."],
                   "A sphere has only a curved surface. There is no flat face to sit on, so it rolls off."))
    its.append(mcq("Can you stack cylinders?", "Yes, if they stand on their flat faces.",
                   ["Yes, if they lie on their sides.", "No, they always roll.", "No, they have no faces."],
                   "A cylinder has 2 flat circle faces. Standing on them, cylinders stack like tins on a shelf."))
    its.append(mcq("Why can you not stack a block on top of a square-based pyramid?", "It comes to a point at the top.",
                   ["It has a curved surface.", "It has no flat faces.", "Its base is a circle."],
                   "The 4 triangle faces meet at a point at the top, so there is no flat face for a block to sit on."))
    its.append(mcq("How many surfaces does a cone have altogether?", 2, [1, 3, 0],
                   "A cone has 1 flat face (the circle) and 1 curved surface: 1 + 1 = 2 surfaces."))
    n, he, his = P.next()
    its.append(mcq("%s sorts objects into “rolls” and “does not roll”. Which object goes in “does not roll”?" % n, TP, [CYL, CONE, SPH],
                   "A triangular prism has only flat faces, so it does not roll. A cylinder, a cone and a sphere have a curved surface."))
    n, he, his = P.next()
    its.append(mcq("%s has a cube, a cylinder, a sphere, a cone and a rectangular prism. How many of them can roll?" % n, 3, [2, 4, 5],
                   "The cylinder, the sphere and the cone have curved surfaces, so they can roll: 3 objects. The cube and the rectangular prism cannot."))
    for q, right, others, e in [
            ("Which object can roll?", "cyl_lying", ["cube", "tp_lying", "sp"],
             "is a cylinder. It has a curved surface, so it can roll. The other objects have only flat faces."),
            ("Which object has only flat surfaces?", "rp_flat", ["cyl", "cone", "sphere"],
             "is a rectangular prism. All 6 of its faces are flat. The others each have a curved surface."),
    ]:
        p = pos.next()
        cells = [pic3d(k, 0.62) for k in others]
        cells.insert(p, pic3d(right, 0.62))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 3-D objects labelled A to D")) + q, list("ABCD"), "ABCD"[p],
                             "%s %s" % ("ABCD"[p], e)))
    assert len(its) == 20, len(its)
    return {"title": "Flat and curved surfaces: roll, slide or stack", "items": its}


# ------------------------------------------------------------ set 4: classify and compare
def set_classify(rnd, pos):
    its = []
    its.append(mcq("Which object is a pyramid?", SP, [TP, RP, CYL],
                   "A pyramid has a base and triangle faces that meet at a point. A square-based pyramid has a square base."))
    its.append(mcq("Which object is a prism?", RP, [SP, CONE, SPH],
                   "A prism has the same shape at both ends, joined by rectangles. A rectangular prism has rectangle ends."))
    its.append(mcq("A prism has the same shape at both ends. What shape are the ends of a triangular prism?", "triangles",
                   ["rectangles", "squares", "circles"],
                   "A triangular prism is named after its ends: 2 triangles. The 3 faces joining them are rectangles."))
    its.append(mcq("What is the difference between a prism and a pyramid?",
                   "A pyramid comes to a point; a prism does not.",
                   ["A prism comes to a point; a pyramid does not.", "A prism has a curved surface.", "A pyramid has no flat faces."],
                   "The triangle faces of a pyramid meet at a point (the apex). A prism has the same shape at both ends, so it has no point."))
    its.append(mcq("Is a cube a prism?", "Yes, it is a special rectangular prism.",
                   ["No, it is a pyramid.", "No, it has a curved surface.", "No, a prism must have triangles."],
                   "A cube has the same square at both ends, joined by squares. It is a rectangular prism with all faces the same size."))
    for q, right, others, why in [
            ("Which picture shows a prism?", "tp_standing", ["sp", "cone", "sphere"],
             "is a triangular prism: it has the same triangle at both ends. The others are a pyramid, a cone and a sphere."),
            ("Which picture shows a pyramid?", "sp_turned", ["tp_lying", "rp_turned", "cube"],
             "is a square-based pyramid: its triangle faces meet at a point. The others are prisms."),
    ]:
        p = pos.next()
        cells = [pic3d(k, 0.62) for k in others]
        cells.insert(p, pic3d(right, 0.62))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 3-D objects labelled A to D")) + q, list("ABCD"), "ABCD"[p],
                             "%s %s" % ("ABCD"[p], why)))
    its.append(mcq("Which group has only prisms?", "cube, triangular prism, rectangular prism",
                   ["cone, cube, rectangular prism", "triangular prism, square-based pyramid, cube", "cylinder, sphere, cube"],
                   "A cube, a triangular prism and a rectangular prism all have the same shape at both ends. A pyramid and a cone come to a point."))
    its.append(mcq("Cube, cylinder, rectangular prism, triangular prism. Which is the odd one out, and why?",
                   "the cylinder: it has a curved surface",
                   ["the cube: it has 8 faces", "the triangular prism: it can roll", "the rectangular prism: it has no vertices"],
                   "The cube and the two prisms have only flat faces. The cylinder is the only one with a curved surface. The other reasons are not true."))
    its.append(mcq("Square-based pyramid, cone, sphere, cylinder. Which is the odd one out, and why?",
                   "the square-based pyramid: it has no curved surface",
                   ["the cone: it has no point", "the sphere: it has 1 flat face", "the cylinder: it has 4 vertices"],
                   "The cone, sphere and cylinder each have a curved surface. The pyramid has only flat faces. The other reasons are not true."))
    its.append(mcq("Which has more faces, a cube or a square-based pyramid? How many more?", "the cube, 1 more",
                   ["the pyramid, 1 more", "the cube, 3 more", "they have the same"],
                   "A cube has 6 faces and a square-based pyramid has 5. 6 − 5 = 1, so the cube has 1 more face."))
    its.append(mcq("Which has more vertices, a triangular prism or a square-based pyramid?", "the triangular prism",
                   ["the square-based pyramid", "they have the same", "neither has vertices"],
                   "A triangular prism has 6 vertices and a square-based pyramid has 5. 6 is more than 5."))
    its.append(mcq("Which two objects have the same number of faces, edges and vertices?", "a cube and a rectangular prism",
                   ["a cube and a square-based pyramid", "a cylinder and a cone", "a triangular prism and a cube"],
                   "A cube and a rectangular prism both have 6 faces, 12 edges and 8 vertices. Only the shape of their faces is different."))
    its.append(mcq("How is a cone like a square-based pyramid?", "Both come to a point.",
                   ["Both have a circle face.", "Both can roll in a straight line.", "Both have 8 edges."],
                   "A cone and a pyramid both narrow to a point at the top. A cone has a circle base; a pyramid has a square base."))
    its.append(mcq("How is a cylinder different from a cone?", "A cylinder has 2 circle faces; a cone has 1.",
                   ["A cylinder comes to a point.", "A cone has no curved surface.", "A cylinder has 8 vertices."],
                   "A cylinder has a flat circle face at each end. A cone has only 1 circle face and a point at the other end."))
    its.append(mcq("How is a cube different from a rectangular prism?", "All the faces of a cube are the same size.",
                   ["A cube has more faces.", "A cube has fewer edges.", "A cube can roll."],
                   "Both have 6 faces, 12 edges and 8 vertices. A cube is special: all 6 faces are squares of the same size."))
    q = (fig(row_svg([pic3d("tp_lying", 0.8), pic3d("sp", 0.8)], ["", ""], "a triangular prism and a square-based pyramid", gap=40))
         + "What is the same about these two objects?")
    its.append(mcq(q, "Both have 5 faces.", ["Both have 6 vertices.", "Both come to a point.", "Both have 8 edges."],
                   "The triangular prism has 2 triangles and 3 rectangles: 5 faces. The pyramid has 1 square and 4 triangles: 5 faces. "
                   "Their vertices (6 and 5) and edges (9 and 8) are different."))
    its.append(mcq("Which object has 5 faces, 9 edges and 6 vertices?", TP, [SP, CUBE, RP],
                   "A triangular prism: 2 triangles and 3 rectangles (5 faces), 9 edges and 6 vertices."))
    its.append(mcq("Which object has 8 edges and 5 vertices?", SP, [TP, CUBE, CONE],
                   "A square-based pyramid: 4 edges round the base and 4 up to the point (8), 4 vertices round the base and 1 at the top (5)."))
    its.append(mcq("Which object has the most edges?", CUBE, [TP, SP, CYL],
                   "A cube has 12 edges, a triangular prism has 9, a square-based pyramid has 8 and a cylinder has 2 curved edges."))
    assert len(its) == 20, len(its)
    return {"title": "Classify and compare: prisms and pyramids", "items": its}


# ------------------------------------------------------------ set 5: uses and making objects
def set_problems(rnd, P):
    its = []
    its.append(mcq("Why are wheels round?", "So they roll smoothly.",
                   ["So they stack in a tower.", "So they stand still on a hill.", "So they have more vertices."],
                   "A round wheel has no vertices or flat sides to bump on, so it rolls smoothly along the road."))
    its.append(mcq("Most boxes are rectangular prisms. Why is this a good shape for boxes?", "Their flat faces stack with no gaps.",
                   ["They roll easily.", "They come to a point.", "They have a curved surface."],
                   "Flat faces and square corners let boxes sit on top of and next to each other with no gaps, in a truck or on a shelf."))
    its.append(mcq("Why is a traffic cone shaped like a cone?", "Its wide, flat base helps it stand up.",
                   ["So it rolls away quickly.", "So it has lots of vertices.", "So it can stand on its point."],
                   "A traffic cone stands on its wide circle face, so it is steady. It is narrow at the top, so empty cones also fit inside each other."))
    its.append(mcq("A drink can is a cylinder. Which feature lets it stand up in the fridge?", "its flat circle faces",
                   ["its curved surface", "its vertices", "its point"],
                   "The can stands on a flat circle face at the bottom. On its curved surface it would roll."))
    its.append(mcq("A netball is a sphere. Why is that a good shape for a ball?", "It bounces and rolls the same way in every direction.",
                   ["It stacks well.", "It has flat faces to catch.", "It has 8 vertices to grip."],
                   "A sphere is curved all over, so it rolls and bounces evenly whichever way it lands."))
    its.append(mcq("Jack says a drink can is a circle. What should he say?", "It is a cylinder.",
                   ["It is a sphere.", "It is a cone.", "It is a rectangle."],
                   "A circle is a flat 2-D shape. The ends of a can are circles, but the whole can is a 3-D object: a cylinder."))
    for obj, kind, wrong, e in [
            ("a tin of baked beans", CYL, ["circle", CONE, RP], "A tin has 2 circle ends and a curved side, so it is a cylinder."),
            ("a tent with a triangle at each end", TP, [SP, RP, CONE], "2 triangle ends joined by rectangles make a triangular prism."),
            ("a party hat that comes to a point", CONE, [SP, CYL, "triangle"], "It has a circle at the bottom, a curved side and a point at the top, so it is a cone."),
            ("a cereal box", RP, [CUBE, "rectangle", TP], "A cereal box has 6 rectangle faces that are not all squares, so it is a rectangular prism."),
    ]:
        its.append(mcq("%s is shaped like which object?" % (obj[0].upper() + obj[1:]), kind, wrong, e))
    its.append(mcq("A tin of baked beans has a paper label all the way round. Which part of the tin does the label cover?",
                   "the curved surface", ["a flat face", "an edge", "the vertices"],
                   "The label goes round the side of the tin. That is the curved surface of the cylinder. The 2 flat faces are the top and bottom."))
    rule = " Each straw makes an edge and each connector makes a vertex."
    n, he, his = P.next()
    its.append(mcq("%s makes a cube from straws and connectors. How many straws does %s need?" % (n, he), 12, [8, 6, 24],
                   "A cube has 12 edges, so %s needs 12 straws. 8 is the number of vertices (connectors)." % n + rule))
    n, he, his = P.next()
    its.append(mcq("%s makes a rectangular prism from straws and connectors. How many connectors does %s need?" % (n, he), 8, [12, 6, 4],
                   "A rectangular prism has 8 vertices: 4 at the top and 4 at the bottom. 12 is the number of edges (straws)." + rule))
    n, he, his = P.next()
    its.append(mcq("%s makes a square-based pyramid from straws and connectors. What does %s need?" % (n, he), "8 straws and 5 connectors",
                   ["5 straws and 8 connectors", "8 straws and 4 connectors", "4 straws and 5 connectors"],
                   "Edges: 4 round the square and 4 up to the top = 8 straws. Vertices: 4 round the square and 1 at the top = 5 connectors."))
    q = (fig(model_cv("tp_lying").svg("a model made from straws and connectors"))
         + "This model is made from straws and connectors. Which object is it?")
    its.append(mcq(q, TP, [SP, RP, CUBE],
                   "It has 9 straws (edges) and 6 connectors (vertices). 2 triangles at the ends are joined by 3 straws, so it is a triangular prism."))
    n, he, his = P.next()
    its.append(mcq("%s has 6 connectors and 9 straws. %s uses them all to make one object. Which object?" % (n, he.capitalize()),
                   TP, [SP, CUBE, RP],
                   "6 vertices and 9 edges: that is a triangular prism. A square-based pyramid has 5 vertices and 8 edges."))
    n, he, his = P.next()
    its.append(mcq("%s has 20 straws. %s makes one cube. How many straws are left?" % (n, he.capitalize()), 8, [12, 14, 32],
                   "A cube uses 12 straws (12 edges). 20 − 12 = 8 straws left. 14 comes from taking away 6 faces instead of 12 edges."))
    n, he, his = P.next()
    its.append(mcq("%s makes a triangular prism and a square-based pyramid. How many connectors does %s use altogether?" % (n, he),
                   11, [17, 10, 12],
                   "A triangular prism has 6 vertices and a square-based pyramid has 5. 6 + 5 = 11 connectors. 17 adds the edges (9 + 8)."))
    its.append(mcq("Which object can you NOT make from straight straws and connectors?", SPH, [CUBE, TP, SP],
                   "A sphere is curved all over and has no edges or vertices, so straight straws cannot make it."))
    n, he, his = P.next()
    its.append(mcq("%s makes 2 cubes from straws and connectors. How many straws does %s use?" % (n, he), 24, [16, 12, 20],
                   "1 cube needs 12 straws (12 edges). 2 cubes: 12 + 12 = 24 straws. 16 counts the vertices (8 + 8) instead."))
    assert len(its) == 20, len(its)
    return {"title": "Objects in real life and making models", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    flat = row_svg([solid_cv("cube", 44), solid_cv("rp_flat", 44), solid_cv("tp_lying", 46), solid_cv("sp", 46)],
                   ["cube", "rectangular prism", "triangular prism", "square-based pyramid"],
                   "cube, rectangular prism, triangular prism and square-based pyramid", gap=22, fs=14)
    curved = row_svg([cylinder_cv(0.85), cone_cv(0.85), sphere_cv(0.9)], ["cylinder", "cone", "sphere"],
                     "cylinder, cone and sphere", gap=40, fs=14)
    positions = row_svg([solid_cv("rp_flat", 40), solid_cv("rp_tall", 40), cone_cv(0.8), cone_cv(0.8, "side")],
                        ["lying down", "standing up", "point up", "on its side"],
                        "a rectangular prism and a cone in different positions", gap=26, fs=14)
    model = row_svg([solid_cv("cube", 52), model_cv("cube", 52)], ["cube", "straw-and-connector model"],
                    "a cube and a model of a cube made from straws and connectors", gap=40, fs=14)
    return (
        "<h2>What is a 3-D object?</h2>"
        "<p>A 3-D object is <b>solid</b>, like a box or a ball. You can pick it up and turn it round. "
        "A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. A <b>vertex</b> is a corner where edges meet. "
        "Two or more are called <b>vertices</b>. Dashed lines show edges at the back that you cannot see.</p>"
        "<figure class='sn-fig'>" + flat +
        "<figcaption>These objects have only flat faces. Prisms have the same shape at both ends; a pyramid comes to a point.</figcaption></figure>"
        "<figure class='sn-fig'>" + curved +
        "<figcaption>A cylinder, a cone and a sphere have a curved surface, so they can roll.</figcaption></figure>" +
        table(["Object", "Faces", "Edges", "Vertices", "Example"], [
            ["Cube", "6 (all squares)", "12", "8", "a dice"],
            ["Rectangular prism", "6 (rectangles)", "12", "8", "a cereal box"],
            ["Triangular prism", "5 (2 triangles, 3 rectangles)", "9", "6", "a tent"],
            ["Square-based pyramid", "5 (1 square, 4 triangles)", "8", "5", "a pyramid in Egypt"],
            ["Cylinder", "2 flat circles and 1 curved surface", "2 curved", "0", "a drink can"],
            ["Cone", "1 flat circle and 1 curved surface", "1 curved", "1 (the point)", "a traffic cone"],
            ["Sphere", "1 curved surface", "0", "0", "a netball"]]) +
        "<p>An object keeps its name when it is turned, lying down or upside down.</p>"
        "<figure class='sn-fig'>" + positions + "</figure>" +
        ex("Example 1", "How many faces does a cube have?",
           "You can see 3 faces in a picture. There are 3 more at the back, on the side and underneath. 3 + 3 = 6.", "6 faces") +
        "<h2>Roll, slide or stack?</h2>"
        "<p>The features of an object tell you how it moves and what it is good for.</p>" +
        table(["Feature", "What it does", "Used for"], [
            ["Curved surface", "rolls", "wheels, balls, rolling pins"],
            ["Flat faces", "slides and stacks", "boxes, bricks, building blocks"],
            ["Wide flat base and a point", "stands steady, fits inside another", "traffic cones, party hats"],
            ["Flat ends and a curved side", "stands up, or rolls on its side", "drink cans, tins of food"]]) +
        ex("Example 2", "Why are boxes in a supermarket rectangular prisms, not spheres?",
           "Rectangular prisms have flat faces, so they stack on shelves with no gaps. Spheres would roll off.",
           "flat faces stack well") +
        "<h2>Making objects</h2>"
        "<p>You can make a model of an object with straws and connectors (or balls of modelling clay). "
        "Each <b>straw</b> is an <b>edge</b>. Each <b>connector</b> is a <b>vertex</b>.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>A cube needs 12 straws (12 edges) and 8 connectors (8 vertices).</figcaption></figure>" +
        ex("Example 3", "How many straws and connectors do you need for a square-based pyramid?",
           "Edges: 4 round the square and 4 up to the top = 8. Vertices: 4 round the square and 1 at the top = 5.",
           "8 straws and 5 connectors") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting only the faces you can see", "Remember the faces at the back and underneath"],
            ["Mixing up edges and vertices", "Edges are the lines (straws); vertices are the corners (connectors)"],
            ["Mixing up a prism and a pyramid", "A pyramid comes to a point; a prism has the same shape at both ends"],
            ["Calling a cylinder a circle", "A circle is flat (2-D). A can is a cylinder (3-D); its ends are circles"],
            ["Mixing up a cylinder and a cone", "A cylinder has 2 circle faces; a cone has 1 circle face and a point"],
        ])
    )


FAQ = [
    {"q": "What 3-D objects do Year 3 students learn in the Australian Curriculum?",
     "a": "Cubes, rectangular prisms, triangular prisms, square-based pyramids, cylinders, cones and spheres. Students name their faces, edges and vertices and explain why their features suit their uses (AC9M3SP01)."},
    {"q": "What is the difference between a face, an edge and a vertex?",
     "a": "A face is a flat surface, an edge is where two faces meet, and a vertex is a corner where edges meet. A cube has 6 faces, 12 edges and 8 vertices."},
    {"q": "What is the difference between a prism and a pyramid?",
     "a": "A prism has the same shape at both ends, joined by rectangles, so it has no point. A pyramid has one base and triangle faces that meet at a point."},
    {"q": "How can I help my child learn 3-D objects at home?",
     "a": "Hunt for objects in the kitchen, such as a tin (cylinder) or a cereal box (rectangular prism), and test which ones roll, slide or stack. Building objects with straws and connectors or modelling clay helps too."},
]


def gen():
    rnd = random.Random(3811)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_name(rnd, pos), set_fev(rnd), set_surfaces(rnd, pos, P), set_classify(rnd, pos), set_problems(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen_q = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen_q, it["q"]
            seen_q.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "3d-objects", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "3-D Objects: Faces, Edges, Vertices and Surfaces",
        "seo_title": "Year 3 3-D Objects Worksheets: Faces, Edges, Vertices, Prisms and Pyramids (Free, with Answers)",
        "short_title": "3-D objects",
        "domain": "Space",
        "standard_code": "AC9M3SP01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Make, compare and classify objects, identifying key features and explaining why these features make them suited to their uses",
        "meta_desc": "Free Year 3 maths worksheets on 3-D objects: name cubes, prisms, pyramids, cylinders, cones and spheres in any position, count faces, edges and vertices, sort objects that roll, slide or stack, and make models with straws and connectors. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Faces, edges and vertices describe an object. Flat faces stack and slide; curved surfaces roll.",
        "key_sub": "A face is a flat surface, an edge is where two faces meet, and a vertex is a corner. Count the faces you cannot see too. A prism has the same shape at both ends; a pyramid comes to a point.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four 3-D objects labelled A to D|the same 3-D object in two positions|a triangular prism and a square-based pyramid)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
