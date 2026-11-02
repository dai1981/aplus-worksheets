# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Volume (5.MD.C.3-5)
  python tools/gen_us_math_g5_volume.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.

Pictures (checked in code):
  cube prisms   every unit cube is drawn (back to front), so the hidden cubes really are there;
                the number of drawn cubes must equal l × w × h (or the sum of the two parts)
  plain prisms  oblique view, 3 hidden edges dashed, edge labels outside the box
  two-part      an L-shaped solid: a long bottom prism with a shorter prism on its left end
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"          # prism A (front, top, right side)
FILL2, TOP2, SIDE2 = "#f6dcb4", "#fbecd3", "#e8c48f"       # prism B in two-part solids
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
UNITS = [("cm", "cu cm", "sq cm"), ("in", "cu in", "sq in"), ("ft", "cu ft", "sq ft"), ("m", "cu m", "sq m")]
DZX, DZY = 0.55, 0.40          # one unit of depth goes this far right and up (oblique view)


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 5 style: 2400 -> 2,400."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors (no zero or negative amounts). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$").replace(",", "")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


class Canvas:
    """Collects shapes and text, tracks the bounding box, then writes a tight SVG."""
    def __init__(self):
        self.el, self.boxes = [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4):
        self.el.append(("l", a, b, dashed, sw))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:                                   # labels never touch each other
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def svg(self, label, pad=5):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1                                  # keep cube pictures out of the 'square' print size
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "l":
                a, b = e[1], e[2]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, GREEN, 1.6 if e[3] else e[4],
                            " stroke-dasharray='5 4'" if e[3] else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def proj(X, Y, Z, k):
    """x to the right, y up, z (depth) to the back."""
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


# ------------------------------------------------------------ unit-cube pictures
def cubes_box(l, w, h, x=0, y=0, z=0, part=0):
    return [(x + i, y + j, z + m, part) for i in range(l) for j in range(h) for m in range(w)]


def cube_svg(cubes, label, k=22, gap=0.0):
    """Draw every unit cube back to front. gap > 0 pulls the layers apart."""
    keys = {(c[0], c[1], c[2]) for c in cubes}
    assert len(keys) == len(cubes)                         # no cube is drawn twice
    cv = Canvas()
    for x, y, z, part in sorted(cubes, key=lambda c: (-c[2], c[1], c[0])):
        Y = y * (1 + gap)
        p = lambda a, b, c: proj(x + a, Y + b, z + c, k)
        fr, tp, sd = (FILL, TOP, SIDE) if part == 0 else (FILL2, TOP2, SIDE2)
        # a face that touches another cube is covered by it, so it is left out (keeps the SVG small)
        if (x, y, z - 1) not in keys:
            cv.poly([p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)], fr)
        if gap or (x, y + 1, z) not in keys:
            cv.poly([p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)], tp)
        if (x + 1, y, z) not in keys:
            cv.poly([p(1, 0, 0), p(1, 0, 1), p(1, 1, 1), p(1, 1, 0)], sd)
    return cv.svg(label)


def prism_cubes(l, w, h, label=None, gap=0.0):
    cubes = cubes_box(l, w, h)
    assert len(cubes) == l * w * h
    return cube_svg(cubes, label or "rectangular prism made of unit cubes", gap=gap)


def visible_cubes(l, w, h):
    """Cubes that show at least one face: front, top or right side."""
    return l * w * h - (l - 1) * (w - 1) * (h - 1)


def l_cubes(a, b, h1, h2, d):
    """Bottom prism a × d × h1, with a b × d × h2 prism on its left end."""
    cubes = cubes_box(a, d, h1) + cubes_box(b, d, h2, y=h1, part=1)
    assert len(cubes) == a * d * h1 + b * d * h2
    return cube_svg(cubes, "solid made of two prisms of unit cubes")


# ------------------------------------------------------------ plain prisms with labels
def scale(L, W, H, max_w=165, max_h=100):
    return min(max_w / (L + W * DZX), max_h / (H + W * DZY), 26)


def box_faces(cv, x, y, z, L, W, H, k, cols=(FILL, TOP, SIDE), sw=2.4):
    p = lambda a, b, c: proj(x + a, y + b, z + c, k)
    cv.poly([p(0, 0, 0), p(L, 0, 0), p(L, H, 0), p(0, H, 0)], cols[0], sw)
    cv.poly([p(0, H, 0), p(L, H, 0), p(L, H, W), p(0, H, W)], cols[1], sw)
    cv.poly([p(L, 0, 0), p(L, 0, W), p(L, H, W), p(L, H, 0)], cols[2], sw)
    return p


def prism_svg(L, W, H, lab_l, lab_w, lab_h, label, disp=None):
    """Box drawn to scale (disp = other sizes to draw it with, e.g. when the numbers are far apart).
    lab_* are the edge labels ('' = none). A label with '?' is red."""
    dL, dW, dH = disp or (L, W, H)
    k = scale(dL, dW, dH)
    cv = Canvas()
    p = box_faces(cv, 0, 0, 0, dL, dW, dH, k)
    for a, b in [((0, 0, dW), (dL, 0, dW)), ((0, 0, dW), (0, dH, dW)), ((0, 0, dW), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True)
    col = lambda t: RED if "?" in t else INK
    if lab_l:
        x, y = p(dL / 2, 0, 0)
        cv.text(x, y + 17, lab_l, 16, col=col(lab_l))
    if lab_h:
        x, y = p(0, dH / 2, 0)
        cv.text(x - 8, y, lab_h, 16, "end", col(lab_h))
    if lab_w:
        x, y = p(dL, 0, dW / 2)
        cv.text(x + 7, y + 11, lab_w, 16, "start", col(lab_w))
    return cv.svg(label)


def two_part_svg(a, b, h1, h2, d, u, label, show=("a", "b", "h1", "h2", "d")):
    """Bottom prism A (a long, h1 tall) with prism B (b long, h2 tall) on its left end; both d deep."""
    assert b < a
    k = min(175 / (a + d * DZX), 125 / (h1 + h2 + d * DZY), 24)
    cv = Canvas()
    pa = box_faces(cv, 0, 0, 0, a, d, h1, k)
    pb = box_faces(cv, 0, h1, 0, b, d, h2, k, (FILL2, TOP2, SIDE2))
    lab = lambda v: "%d %s" % (v, u)
    if "a" in show:
        x, y = pa(a / 2, 0, 0)
        cv.text(x, y + 17, lab(a), 16)
    if "d" in show:
        x, y = pa(a, 0, d / 2)
        cv.text(x + 7, y + 11, lab(d), 16, "start")
    if "h1" in show:
        x, y = pa(0, h1 / 2, 0)
        cv.text(x - 8, y, lab(h1), 16, "end")
    if "h2" in show:
        x, y = pb(0, h2 / 2, 0)
        cv.text(x - 8, y, lab(h2), 16, "end")
    if "b" in show:
        x, y = pb(b / 2, h2, d)
        cv.text(x, y - 13, lab(b), 16)
    xa = b + (a - b) / 2 if (a - b) * k > 26 else a / 2       # part names on the front faces
    for t, (xx, yy) in [("A", (xa, h1 / 2)), ("B", (b / 2, h1 + h2 / 2))]:
        x, y = proj(xx, yy, 0, k)
        cv.el.append(("t", x, y + 6, t, 17, "middle", GREEN))
    return cv.svg(label)


# ------------------------------------------------------------ set 1: count unit cubes
def pick_dims(rnd, seen, lr, wr, hr, hidden=True):
    while True:
        l, w, h = rnd.randint(*lr), rnd.randint(*wr), rnd.randint(*hr)
        if (l, w, h) in seen or l < w:
            continue
        if hidden and (l - 1) * (w - 1) * (h - 1) == 0:
            continue
        seen.add((l, w, h))
        return l, w, h


def cu(n):
    return "%s cubic units" % f(n) if n != 1 else "1 cubic unit"


def set_count(rnd):
    its, seen = [], set()
    # whole prism
    for i in range(8):
        l, w, h = pick_dims(rnd, seen, (2, 5), (2, 3), (2, 4))
        V, vis = l * w * h, visible_cubes(l, w, h)
        faces = l * h + l * w + w * h
        q = fig(prism_cubes(l, w, h)) + "Each small cube is 1 cubic unit. What is the volume of this prism?"
        e = ("Each layer has %d rows of %d cubes = %d cubes. There are %d layers: %d × %d = %d cubic units. "
             "Count the cubes you cannot see, too (only %d cubes show a face)." % (w, l, l * w, h, l * w, h, V, vis))
        its.append(mcq(q, cu(V), [cu(vis), cu(faces), cu(l + w + h), cu(l * h), cu(l * w + h)], e))
    # bottom layer
    used_lw = set()
    for i in range(4):
        while True:
            l, w, h = pick_dims(rnd, seen, (3, 5), (2, 4), (2, 4))
            if l != w and (l, w) not in used_lw and h != w:
                break
        used_lw.add((l, w))
        q = fig(prism_cubes(l, w, h)) + "How many unit cubes are in the bottom layer of this prism?"
        e = ("The bottom layer is %d cubes across and %d cubes deep: %d × %d = %d cubes. "
             "The front face shows %d × %d = %d cubes, but that is not a layer." % (l, w, l, w, l * w, l, h, l * h))
        its.append(mcq(q, str(l * w), [l * h, l + w, l * w * h, w * h, l * h + w * h, l * w + h], e))
    # layers pulled apart
    for i in range(4):
        l, w, h = pick_dims(rnd, seen, (3, 5), (2, 3), (2, 4))
        V = l * w * h
        q = (fig(prism_cubes(l, w, h, "rectangular prism of unit cubes with its layers pulled apart", gap=0.45)) +
             "The layers of this prism are pulled apart. How many unit cubes are in the whole prism?")
        e = ("One layer: %d × %d = %d cubes. %d layers: %d × %d = %d cubes." % (l, w, l * w, h, l * w, h, V))
        its.append(mcq(q, str(V), [l * w, l * w + h, visible_cubes(l, w, h), l * w * (h - 1)], e))
    # no picture
    for i, (r, c, n, thing) in enumerate([(4, 6, 3, "box"), (5, 3, 4, "crate"), (6, 5, 2, "tray"), (7, 4, 5, "bin")]):
        V = r * c * n
        q = ("The bottom layer of a %s has %d rows of %d unit cubes. The %s holds %d layers. How many unit cubes fill it?"
             % (thing, r, c, thing, n))
        e = "One layer: %d × %d = %d cubes. %d layers: %d × %d = %s cubes." % (r, c, r * c, n, r * c, n, f(V))
        its.append(mcq(q, f(V), [r + c + n, r * c, r * c + n, r * c * (n + 1)], e))
    rnd.shuffle(its)
    return {"title": "Count unit cubes", "items": its}


# ------------------------------------------------------------ set 2: V = l × w × h and V = B × h
def disp_dims(L, W, H):
    """Draw very different sizes a little closer together so the box stays readable."""
    m = max(L, W, H)
    return tuple(max(v, m / 3.2) for v in (L, W, H))


def vol_e(L, W, H, cuu):
    V = L * W * H
    return "V = l × w × h = %d × %d × %d = %s × %d = %s %s." % (L, W, H, f(L * W), H, f(V), cuu)


def set_formula(rnd, seen):
    its = []
    for i in range(10):
        while True:
            L, W, H = rnd.randint(4, 15), rnd.randint(2, 9), rnd.randint(2, 12)
            if L > W and (L, W, H) not in seen and L * W * H not in (L + W + H, L * W) and L * W != W * H:
                break
        seen.add((L, W, H))
        u, cuu, squ = UNITS[i % 4]
        V = L * W * H
        SA = 2 * (L * W + L * H + W * H)
        lab = lambda v: "%d %s" % (v, u)
        q = (fig(prism_svg(L, W, H, lab(L), lab(W), lab(H), "rectangular prism %d by %d by %d" % (L, W, H),
                           disp_dims(L, W, H))) + "What is the volume of this rectangular prism?")
        pool = ["%s %s" % (f(L * W), cuu), "%d %s" % (L + W + H, cuu), "%s %s" % (f(V), squ), "%s %s" % (f(SA), cuu)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = vol_e(L, W, H, cuu) + " Volume uses all 3 edges, and the unit is cubic: %s." % cuu
        its.append(mcq(q, "%s %s" % (f(V), cuu), pool, e))
    for s, (u, cuu, squ) in zip([6, 9, 11], [UNITS[0], UNITS[1], UNITS[3]]):
        V = s ** 3
        q = "A cube has edges that are %d %s long. What is its volume?" % (s, u)
        e = ("Every edge of a cube is %d %s, so V = %d × %d × %d = %d × %d = %s %s."
             % (s, u, s, s, s, s * s, s, f(V), cuu))
        its.append(mcq(q, "%s %s" % (f(V), cuu), ["%d %s" % (3 * s, cuu), "%d %s" % (s * s, cuu), "%s %s" % (f(V), squ)], e))
    for i, (B, h) in enumerate([(24, 5), (36, 7), (48, 9), (15, 12), (120, 8)]):
        u, cuu, squ = UNITS[(i + 1) % 4]
        V = B * h
        q = ("The base of a rectangular prism has an area of %d %s. The prism is %d %s tall. What is its volume?"
             % (B, squ, h, u))
        e = ("V = B × h, where B is the area of the base: %d × %d = %s %s. "
             "Think of %d layers with %d cubes in each." % (B, h, f(V), cuu, h, B))
        its.append(mcq(q, "%s %s" % (f(V), cuu), ["%d %s" % (B + h, cuu), "%s %s" % (f(V), squ), "%d %s" % (B, cuu)], e))
    for L, W, H, u in [(6, 4, 3, "cm"), (8, 5, 2, "ft")]:
        q = ("A box is %d %s long, %d %s wide and %d %s tall. Which expression gives its volume?" % (L, u, W, u, H, u))
        right = "%d × %d × %d" % (L, W, H)
        e = "Volume = length × width × height = %s = %d cubic %s." % (right, L * W * H, "centimeters" if u == "cm" else "feet")
        its.append(mcq(q, right, ["%d + %d + %d" % (L, W, H), "%d × %d" % (L, W), "2 × %d + 2 × %d" % (L, W)], e))
    rnd.shuffle(its)
    return {"title": "Use V = l × w × h and V = B × h", "items": its}


# ------------------------------------------------------------ set 3: missing edge length
def set_missing(rnd, seen):
    its = []
    for i in range(12):
        while True:
            L, W, H = rnd.randint(4, 12), rnd.randint(2, 8), rnd.randint(3, 10)
            V = L * W * H
            if L > W and (L, W, H) not in seen and V - L - W > 0 and H not in (L, W):
                break
        seen.add((L, W, H))
        u, cuu, squ = UNITS[i % 4]
        miss = ["h", "l", "w"][i % 3]
        known = {"h": (L, W), "l": (W, H), "w": (L, H)}[miss]
        ans = {"h": H, "l": L, "w": W}[miss]
        a, b = known
        cands = ["%d %s" % (V // a, u), "%d %s" % (V - a - b, u), "%d %s" % (ans, cuu), "%d %s" % (a * b, u)]
        if V % (a + b) == 0:
            cands.insert(1, "%d %s" % (V // (a + b), u))
        e = ("%d × %d × ? = %s, so %d × ? = %s. %s ÷ %d = %d %s. Check: %d × %d × %d = %s."
             % (a, b, f(V), a * b, f(V), f(V), a * b, ans, u, L, W, H, f(V)))
        if i < 6:
            labs = {"l": "%d %s" % (L, u), "w": "%d %s" % (W, u), "h": "%d %s" % (H, u)}
            labs[miss] = "? %s" % u
            q = (fig(prism_svg(L, W, H, labs["l"], labs["w"], labs["h"], "rectangular prism with one unknown edge",
                               disp_dims(L, W, H))) +
                 "The volume of this prism is %s %s. What is the length of the edge marked ?" % (f(V), cuu))
        else:
            word = {"h": "How tall is it?", "l": "How long is it?", "w": "How wide is it?"}[miss]
            given = {"h": "%d %s long and %d %s wide" % (L, u, W, u),
                     "l": "%d %s wide and %d %s tall" % (W, u, H, u),
                     "w": "%d %s long and %d %s tall" % (L, u, H, u)}[miss]
            q = "A rectangular prism has a volume of %s %s. It is %s. %s" % (f(V), cuu, given, word)
        its.append(mcq(q, "%d %s" % (ans, u), cands, e))
    for i, (V, B) in enumerate([(96, 16), (150, 25), (252, 36), (480, 40)]):
        u, cuu, squ = UNITS[(i + 2) % 4]
        h = V // B
        q = "A prism has a volume of %d %s. The area of its base is %d %s. What is its height?" % (V, cuu, B, squ)
        e = "V = B × h, so %d × h = %d. h = %d ÷ %d = %d %s." % (B, V, V, B, h, u)
        its.append(mcq(q, "%d %s" % (h, u), ["%d %s" % (V - B, u), "%d %s" % (h, cuu), "%d %s" % (B, u)], e))
    for i, (V, h) in enumerate([(180, 5), (336, 8)]):
        u, cuu, squ = UNITS[i * 2 + 1]
        B = V // h
        q = "A prism has a volume of %d %s and a height of %d %s. What is the area of its base?" % (V, cuu, h, u)
        e = "V = B × h, so B × %d = %d. B = %d ÷ %d = %d %s. Area is in square units." % (h, V, V, h, B, squ)
        its.append(mcq(q, "%d %s" % (B, squ), ["%d %s" % (B, cuu), "%d %s" % (V - h, squ), "%s %s" % (f(V * h), squ)], e))
    for V, s, u, cuu in [(64, 4, "in", "cu in"), (1000, 10, "cm", "cu cm")]:
        q = "A cube has a volume of %s %s. How long is each edge?" % (f(V), cuu)
        e = ("All 3 edges of a cube are equal. Find the number that you multiply 3 times to get %s: "
             "%d × %d × %d = %s. Each edge is %d %s." % (f(V), s, s, s, f(V), s, u))
        wrong = [V // 2, V // 4, int(math.isqrt(V))] if V == 64 else [V // 2, V // 4, V // 10]
        its.append(mcq(q, "%d %s" % (s, u), ["%s %s" % (f(x), u) for x in wrong], e))
    rnd.shuffle(its)
    return {"title": "Find a missing edge", "items": its}


# ------------------------------------------------------------ set 4: two prisms put together
def two_part_e(a, b, h1, h2, d, cuu):
    A, B = a * h1 * d, b * h2 * d
    return ("Prism A: %d × %d × %d = %d. Prism B: %d × %d × %d = %d. Add: %d + %d = %s %s."
            % (a, d, h1, A, b, d, h2, B, A, B, f(A + B), cuu))


def pick_two(rnd, used, ar=(6, 12), dr=(2, 6), hr=(2, 6)):
    while True:
        a, d = rnd.randint(*ar), rnd.randint(*dr)
        b = rnd.randint(2, a - 2)
        h1, h2 = rnd.randint(*hr), rnd.randint(*hr)
        key = (a, b, h1, h2, d)
        if key in used or b == d or h1 == h2:
            continue
        used.add(key)
        return key


def set_two(rnd, P):
    its, used = [], set()
    for i in range(8):
        a, b, h1, h2, d = pick_two(rnd, used)
        u, cuu, squ = UNITS[i % 4]
        A, B = a * h1 * d, b * h2 * d
        q = (fig(two_part_svg(a, b, h1, h2, d, u, "solid made of two rectangular prisms")) +
             "This solid is made of two rectangular prisms, A and B. What is its total volume?")
        dbl = A + b * (h1 + h2) * d                   # B measured down to the floor: counts part of A twice
        box = a * (h1 + h2) * d                       # one big box around the whole solid
        e = two_part_e(a, b, h1, h2, d, cuu) + " Prism B starts on top of A, so its height is %d, not %d." % (h2, h1 + h2)
        pool = ["%s %s" % (f(dbl), cuu), "%s %s" % (f(box), cuu), "%s %s" % (f(A), cuu), "%s %s" % (f(A + B), squ)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        its.append(mcq(q, "%s %s" % (f(A + B), cuu), pool, e))
    for i in range(4):
        while True:
            a, b, h1, h2, d = pick_two(rnd, used, (4, 5), (2, 3), (1, 3))
            if h1 + h2 <= 5 and a * d * h1 + b * d * h2 != visible_two(a, b, h1, h2, d):
                break
        V = a * d * h1 + b * d * h2
        q = (fig(l_cubes(a, b, h1, h2, d)) +
             "This solid is made of unit cubes. What is its volume?")
        e = ("Bottom prism: %d × %d × %d = %d cubes. Top prism: %d × %d × %d = %d cubes. "
             "%d + %d = %d cubic units. Count the hidden cubes, too."
             % (a, d, h1, a * d * h1, b, d, h2, b * d * h2, a * d * h1, b * d * h2, V))
        its.append(mcq(q, cu(V), [cu(visible_two(a, b, h1, h2, d)), cu(a * d * (h1 + h2)), cu(a * d * h1),
                                  cu(a * h1 + b * h2)], e))
    for i, (p1, p2, u, thing) in enumerate([((5, 4, 3), (2, 4, 6), "in", "Two wooden blocks are glued together to make a toy."),
                                            ((10, 6, 4), (6, 6, 5), "ft", "A storage shed has two parts shaped like rectangular prisms."),
                                            ((8, 3, 2), (3, 3, 4), "m", "A set of concrete steps is made of two rectangular prisms."),
                                            ((12, 9, 7), (8, 5, 7), "cm", "A model building has two parts shaped like rectangular prisms.")]):
        cuu = "cu " + u
        A, B = p1[0] * p1[1] * p1[2], p2[0] * p2[1] * p2[2]
        q = ("%s One part is %d %s by %d %s by %d %s. The other part is %d %s by %d %s by %d %s. What is the total volume?"
             % ((thing,) + sum(((v, u) for v in p1 + p2), ())))
        e = ("First part: %d × %d × %d = %s. Second part: %d × %d × %d = %s. Add: %s + %s = %s %s."
             % (p1 + (f(A),) + p2 + (f(B),) + (f(A), f(B), f(A + B), cuu)))
        its.append(mcq(q, "%s %s" % (f(A + B), cuu), ["%s %s" % (f(A), cuu), "%d %s" % (sum(p1 + p2), cuu),
                                                       "%s %s" % (f(B), cuu),
                                                       "%s %s" % (f(A + B), "sq " + u)], e))
    for (T, a1, l2, w2), u in [((150, 90, 5, 3), "cm"), ((200, 120, 4, 5), "in")]:
        Bv = T - a1
        h = Bv // (l2 * w2)
        n, he, his = P.next()
        q = ("%s builds a solid from two rectangular prisms. The total volume is %d cu %s. Prism A has a volume of %d cu %s. "
             "Prism B is %d %s long and %d %s wide. How tall is prism B?" % (n, T, u, a1, u, l2, u, w2, u))
        e = ("Prism B: %d − %d = %d cu %s. Then %d × %d × h = %d, so %d × h = %d and h = %d ÷ %d = %d %s."
             % (T, a1, Bv, u, l2, w2, Bv, l2 * w2, Bv, Bv, l2 * w2, h, u))
        its.append(mcq(q, "%d %s" % (h, u), ["%d %s" % (Bv, u), "%d %s" % (Bv // l2, u), "%d %s" % (T // (l2 * w2), u)], e))
    for i in range(2):
        a, b, h1, h2, d = pick_two(rnd, used, (6, 10), (2, 5), (2, 5))
        u, cuu, squ = UNITS[i * 2]
        q = (fig(two_part_svg(a, b, h1, h2, d, u, "solid made of two rectangular prisms")) +
             "Which expression gives the volume of this solid?")
        right = "%d×%d×%d + %d×%d×%d" % (a, d, h1, b, d, h2)
        wrong = ["%d×%d×%d + %d×%d×%d" % (a, d, h1, b, d, h1 + h2), "%d×%d×%d" % (a, d, h1 + h2),
                 "%d×%d×%d + %d×%d" % (a, d, h1, b, h2)]
        e = (two_part_e(a, b, h1, h2, d, cuu) + " Each prism needs all 3 of its own edges, and B is only %d %s tall." % (h2, u))
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Add the volumes of two prisms", "items": its}


def visible_two(a, b, h1, h2, d):
    """Cubes of the L-shaped solid that show a face (front, top or right side)."""
    cubes = {(c[0], c[1], c[2]) for c in cubes_box(a, d, h1) + cubes_box(b, d, h2, y=h1)}
    vis = 0
    for x, y, z in cubes:
        if z == 0 or (x + 1, y, z) not in cubes or (x, y + 1, z) not in cubes:
            vis += 1
    return vis


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s's aquarium is 20 inches long, 10 inches wide and 12 inches tall. What is its volume?" % n,
                   "2,400 cu in", ["42 cu in", "200 cu in", "2,400 sq in"],
                   "V = 20 × 10 × 12 = 200 × 12 = 2,400 cu in. 200 is only the area of the bottom."))
    n, he, his = P.next()
    its.append(mcq("%s fills a sandbox that is 6 feet long and 5 feet wide with sand 2 feet deep. "
                   "How many cubic feet of sand does %s need?" % (n, he),
                   "60 cu ft", ["30 cu ft", "13 cu ft", "60 sq ft"],
                   "V = 6 × 5 × 2 = 30 × 2 = 60 cu ft. The depth of the sand is the height."))
    its.append(mcq("Storage unit A is 10 ft by 10 ft by 8 ft. Storage unit B is 12 ft by 8 ft by 8 ft. Which holds more, and how much more?",
                   "A, by 32 cu ft", ["B, by 32 cu ft", "Same volume", "A, by 4 cu ft"],
                   "A: 10 × 10 × 8 = 800 cu ft. B: 12 × 8 × 8 = 768 cu ft. 800 − 768 = 32 cu ft. "
                   "(Adding the edges gives 28 for both, but that is not volume.)"))
    its.append(mcq("A cereal box is 8 inches wide, 3 inches deep and 12 inches tall. What is its volume?",
                   "288 cu in", ["23 cu in", "96 cu in", "288 sq in"],
                   "V = 8 × 3 × 12 = 24 × 12 = 288 cu in."))
    its.append(mcq("Which unit could be used to measure the volume of a swimming pool?",
                   "cubic meters", ["square meters", "meters", "kilograms"],
                   "Volume is the space inside a solid, so it uses cubic units. Square meters measure area, "
                   "meters measure length, and kilograms measure mass."))
    its.append(mcq("Which of these could be the volume of a shoebox?",
                   "600 cu in", ["600 sq in", "600 in", "600 cu ft"],
                   "A volume is in cubic units, and a shoebox is about 12 in × 7 in × 5 in = 420 cu in. "
                   "600 cu ft would be bigger than a closet."))
    n, he, his = P.next()
    its.append(mcq("%s packs 1-foot cubes into a crate that is 4 feet long, 3 feet wide and 2 feet tall. "
                   "How many cubes fit?" % n, "24", ["12", "9", "14"],
                   "One layer: 4 × 3 = 12 cubes. 2 layers: 12 × 2 = 24 cubes, so the crate is 24 cu ft."))
    n, he, his = P.next()
    its.append(mcq("%s fills a sandbox that is 5 ft long, 4 ft wide and 1 ft deep. Sand costs $3 for each cubic foot. "
                   "How much does the sand cost?" % n, "$60", ["$20", "$30", "$23"],
                   "Step 1: V = 5 × 4 × 1 = 20 cu ft. Step 2: 20 × $3 = $60."))
    its.append(mcq("A garden bed is made of two rectangular prisms. One is 6 ft by 3 ft by 2 ft. "
                   "The other is 3 ft by 3 ft by 2 ft. How much soil fills the bed?",
                   "54 cu ft", ["36 cu ft", "19 cu ft", "18 cu ft"],
                   "6 × 3 × 2 = 36 and 3 × 3 × 2 = 18. Add the two parts: 36 + 18 = 54 cu ft."))
    its.append(mcq("A fish tank is 30 cm long, 20 cm wide and 25 cm tall. Water fills it to a height of 20 cm. "
                   "What is the volume of the water?", "12,000 cu cm", ["15,000 cu cm", "600 cu cm", "3,000 cu cm"],
                   "Use the height of the water, not the tank: 30 × 20 × 20 = 600 × 20 = 12,000 cu cm."))
    its.append(mcq("A moving box holds 3,000 cubic inches. It is 20 inches long and 15 inches wide. How tall is it?",
                   "10 in", ["150 in", "2,965 in", "10 sq in"],
                   "Base: 20 × 15 = 300 sq in. 300 × h = 3,000, so h = 3,000 ÷ 300 = 10 in."))
    n, he, his = P.next()
    its.append(mcq("%s packs cubes with 2-inch edges into a box that is 8 in long, 6 in wide and 4 in tall. "
                   "How many cubes fit?" % n, "24", ["192", "96", "9"],
                   "Along each edge: 8 ÷ 2 = 4, 6 ÷ 2 = 3, 4 ÷ 2 = 2. Cubes: 4 × 3 × 2 = 24. "
                   "(192 would be 1-inch cubes.)"))
    its.append(mcq("Box A is 6 cm by 5 cm by 4 cm. Box B is a cube with 5 cm edges. Which has the greater volume?",
                   "B, by 5 cu cm", ["A, by 5 cu cm", "Same volume", "B, by 1 cu cm"],
                   "A: 6 × 5 × 4 = 120 cu cm. B: 5 × 5 × 5 = 125 cu cm. B is greater by 125 − 120 = 5 cu cm."))
    n, he, his = P.next()
    its.append(mcq("%s's toy chest is 3 ft long, 2 ft wide and 2 ft tall. How much space is inside it?" % n,
                   "12 cu ft", ["7 cu ft", "6 cu ft", "12 sq ft"],
                   "V = 3 × 2 × 2 = 12 cu ft."))
    its.append(mcq("A swimming pool is 25 m long and 10 m wide. The water is 2 m deep everywhere. How much water is in the pool?",
                   "500 cu m", ["250 cu m", "37 cu m", "500 sq m"],
                   "V = 25 × 10 × 2 = 250 × 2 = 500 cu m. 250 is only the area of the pool."))
    its.append(mcq("A shipping container is 40 ft long, 8 ft wide and 8 ft tall. What is its volume?",
                   "2,560 cu ft", ["56 cu ft", "320 cu ft", "2,560 sq ft"],
                   "V = 40 × 8 × 8 = 320 × 8 = 2,560 cu ft."))
    its.append(mcq("Each layer of cubes in a box has 15 cubes. The box holds 90 cubes when it is full. How many layers are there?",
                   "6", ["75", "105", "1,350"],
                   "Layers × cubes in each layer = total, so ? × 15 = 90. 90 ÷ 15 = 6 layers."))
    its.append(mcq("A box is 4 in long, 3 in wide and 5 in tall. A second box has the same base but is twice as tall. "
                   "What is the volume of the second box?", "120 cu in", ["60 cu in", "65 cu in", "480 cu in"],
                   "The second box is 4 × 3 × 10 = 120 cu in. Doubling the height doubles the volume: 2 × 60 = 120. "
                   "(480 would double every edge.)"))
    n, he, his = P.next()
    its.append(mcq("%s stacks 3 boxes that are all the same. Each box is 12 in by 10 in by 6 in. "
                   "What is the total volume of the 3 boxes?" % n, "2,160 cu in", ["720 cu in", "84 cu in", "240 cu in"],
                   "One box: 12 × 10 × 6 = 720 cu in. Three boxes: 3 × 720 = 2,160 cu in."))
    its.append(mcq("A brick is 8 in long, 4 in wide and 2 in tall. What is the total volume of 10 bricks?",
                   "640 cu in", ["64 cu in", "140 cu in", "74 cu in"],
                   "One brick: 8 × 4 × 2 = 64 cu in. Ten bricks: 64 × 10 = 640 cu in."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Volume word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>What volume means</h2>"
        "<p><b>Volume</b> is the amount of space inside a solid. We measure it by counting how many "
        "<b>unit cubes</b> fill the solid with no gaps and no overlaps. A cube with 1 cm edges is 1 cubic centimeter.</p>"
        "<figure class='sn-fig'>" + prism_cubes(4, 3, 3, "prism of unit cubes with its 3 layers pulled apart", gap=0.45) +
        "<figcaption>Each layer has 4 × 3 = 12 cubes. There are 3 layers: 12 × 3 = 36 cubic units. "
        "The cubes you cannot see count, too.</figcaption></figure>"
        "<h2>The two formulas</h2>"
        "<p><b>V = l × w × h</b> (length × width × height). <b>V = B × h</b>, where B is the area of the base. "
        "Both say the same thing: cubes in one layer × number of layers.</p>"
        "<figure class='sn-fig'>" + prism_svg(6, 4, 5, "6 cm", "4 cm", "5 cm", "rectangular prism 6 by 4 by 5") +
        "<figcaption>B = 6 × 4 = 24 sq cm. V = 24 × 5 = 120 cu cm.</figcaption></figure>" +
        ex("Find a missing edge", "A box has a volume of 120 cu in. It is 5 in long and 4 in wide. How tall is it?",
           "5 × 4 × h = 120, so 20 × h = 120. 120 ÷ 20 = 6.", "6 in") +
        "<h2>Two prisms put together</h2>"
        "<p>Volume is additive. Split the solid into two rectangular prisms that do not overlap, find each volume, then add.</p>"
        "<figure class='sn-fig'>" + two_part_svg(8, 3, 2, 4, 3, "m", "solid made of two rectangular prisms") +
        "<figcaption>A: 8 × 3 × 2 = 48. B: 3 × 3 × 4 = 36. Total: 48 + 36 = 84 cu m.</figcaption></figure>"
        "<h2>Units</h2>" +
        table(["Measure", "Unit", "Example"], [
            ["Length (1 edge)", "cm, in, ft, m", "5 cm"],
            ["Area (a flat face)", "sq cm, sq in, sq ft", "24 sq cm"],
            ["Volume (space inside)", "cu cm, cu in, cu ft, cu m", "120 cu cm"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting only the cubes you can see", "Count one layer, then multiply by the number of layers"],
            ["Adding the edges: 6 + 4 + 5 = 15", "Multiply them: 6 × 4 × 5 = 120"],
            ["Stopping at one face: 6 × 4 = 24", "That is the base. Multiply by the height, too"],
            ["Writing sq cm for a volume", "Volume is in cubic units: cu cm"],
            ["Measuring prism B down to the floor", "Use only B's own height, so no part is counted twice"],
        ])
    )


FAQ = [
    {"q": "What is the formula for the volume of a rectangular prism?",
     "a": "V = l × w × h (length × width × height), or V = B × h, where B is the area of the base. The answer is in cubic units, such as cu cm or cu ft."},
    {"q": "How do you teach volume to 5th graders?",
     "a": "Start by filling a box with unit cubes: count the cubes in one layer, then multiply by the number of layers. Then show that this is the same as l × w × h."},
    {"q": "How do you find the volume of a shape made of two rectangular prisms?",
     "a": "Split it into two prisms that do not overlap, find the volume of each one with l × w × h, and add the two volumes."},
    {"q": "Why is volume measured in cubic units?",
     "a": "Volume counts how many cubes fill a solid, and each cube has length, width and height. So 1 cubic inch is a cube with 1-inch edges."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_volume():
    rnd = random.Random(506)
    P = People(rnd)
    seen = set()
    sets = [set_count(rnd), set_formula(rnd, seen), set_missing(rnd, seen), set_two(rnd, P), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "volume", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Volume of Rectangular Prisms",
        "seo_title": "Grade 5 Volume Worksheets: Unit Cubes, V = l × w × h, Missing Edges and Two-Prism Solids",
        "short_title": "Volume",
        "domain": "Measurement and Data",
        "standard_code": "5.MD.C.3–5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/MD/C/",
        "standard_text": "Recognize volume as an attribute of solid figures and understand concepts of volume measurement. Measure volumes by counting unit cubes, using cubic cm, cubic in, cubic ft, and improvised units. Relate volume to the operations of multiplication and addition and solve real world and mathematical problems involving volume. Apply the formulas V = l × w × h and V = b × h for rectangular prisms to find volumes of right rectangular prisms with whole-number edge lengths in the context of solving real world and mathematical problems. Recognize volume as additive. Find volumes of solid figures composed of two non-overlapping right rectangular prisms by adding the volumes of the non-overlapping parts.",
        "meta_desc": "Free Grade 5 volume worksheets: count unit cubes, use V = l × w × h and V = B × h, find a missing edge, add the volumes of two prisms, and solve real-world word problems in cubic units. 100 practice questions with answers.",
        "key_big": "Volume = length × width × height (V = l × w × h).",
        "key_sub": "Volume counts the unit cubes that fill a solid: cubes in one layer × number of layers. It is in cubic units (cu cm, cu ft). For two prisms put together, find each volume and add.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(rectangular prism made of unit cubes|rectangular prism of unit cubes|solid made of two)")


if __name__ == "__main__":
    u = gen_volume()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
