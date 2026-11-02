# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Area and Perimeter (MOE 2021 Primary Mathematics Syllabus, Standard,
Measurement and Geometry: Area and Volume)
  python3 tools/gen_sg_maths_p4_area_perimeter.py
Review of area = length × breadth and perimeter = 2 × (length + breadth); finding the length or breadth from
the area (divide) or the perimeter (halve first: length + breadth = half the perimeter); the side of a square
from its area (multiplication tables) or its perimeter (÷ 4); composite rectilinear figures made of rectangles
and squares (find the missing sides first, split into rectangles); word problems with fencing, tiles and paths,
and bar models (units) for length-and-breadth problems.
Wrong choices come from real mistakes: mixing up area and perimeter, adding only two sides, forgetting to halve,
halving the wrong thing, subtracting instead of dividing, using the whole side instead of the part in a
composite figure, counting the overlap twice, and dividing by the side instead of the area of a tile.
Every figure is drawn to scale from its numbers and every answer is worked out in code.
Helpers copied from gen_cabc_math_g5_area_perimeter.py, gen_cabc_math_g6_perimeter.py and
gen_sg_maths_p6_volume.py. MOE number style: 4 digits plain, 5 or more digits with a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
NB = " "
GREEN = "#006633"
FILL = "#cfe6d6"
UNIT_FILL, UNIT_FILL2, WHITE = "#cfe6d6", "#f6dcb4", "#ffffff"
PATH = "#ecd9b5"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Arjun", "Ethan", "Ryan", "Kumar"]
SQ = {"cm": "cm²", "m": "m²"}


# ------------------------------------------------------------ numbers and choices
def num(v):
    """MOE style: 4536, 10 000 (no-break space). Halves and quarters as decimals."""
    if isinstance(v, float):
        assert v * 4 == int(v * 4), v
        if v == int(v):
            v = int(v)
        else:
            return ("%.2f" % v).rstrip("0")
    s = str(v)
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return s


def q_(v, u):
    return "%s %s" % (num(v), u)


LEAD = re.compile(r"^\$?([\d. ]+)( [a-zA-Z²]+)?$")


def lead(c):
    m = LEAD.match(c)
    return float(m.group(1).replace(NB, "")) if m else None


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + the first 3 usable distractors (positive, unique, no two with the same number)."""
    correct = str(correct)
    seen = {correct}
    nums = {lead(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        v = lead(c)
        if c in seen or not c or c.startswith("−") or v == 0:
            continue
        if v is not None:
            if v in nums:
                continue
            nums.add(v)
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def opt(v, u):
    """A distractor only if it is a positive whole number, half or quarter."""
    if v is None or v <= 0 or v * 4 != int(v * 4):
        return None
    return q_(v, u)


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - (t.count(",") + t.count(".")) * 0.6 - (t.count(" ") + t.count(NB)) * 0.3) * fs * 0.6


def text(x, y, t, fs=17, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def colr(t):
    return RED if ("?" in t or t == "x") else INK


# ------------------------------------------------------------ labelled rectangle (drawn to scale)
FS = 17


def rect_svg(L, W, top, left, label, inner="", max_w=190, max_h=95):
    """L × W rectangle drawn to scale. top/left = side labels ('?' labels are red); inner = text inside."""
    k = min(max_w / L, max_h / W, 24)
    Wp, Hp = L * k, W * k
    pad = 5
    lw = tw(left, FS) + 10 if left else 0
    th = 26 if top else 0
    ox, oy = pad + lw, pad + th
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='3'/>"
         % (ox, oy, Wp, Hp, FILL, GREEN)]
    if top:
        s.append(text(ox + Wp / 2, oy - 9, top, FS, colr(top)))
    if left:
        s.append(text(ox - lw / 2 - 2, oy + Hp / 2 + 6, left, FS, colr(left)))
    if inner:
        assert Wp >= tw(inner, 15) + 10 and Hp >= 26, (L, W, inner)
        s.append(text(ox + Wp / 2, oy + Hp / 2 + 5, inner, 15, GREEN))
    W_ = max(ox + Wp + pad, tw(top, FS) + 2 * pad if top else 0)
    return svg_wrap(int(math.ceil(W_)), int(math.ceil(oy + Hp + pad)), "".join(s), label)


# ------------------------------------------------------------ squared grids
def cells_body(cells, x0, y0, cols, rows, cell, m=0):
    g = []
    for (c, r) in sorted(cells):
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + c * cell, y0 + r * cell, cell, cell, FILL))
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0 - m * cell + i * cell, y0 - m * cell, x0 - m * cell + i * cell, y0 - m * cell + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0 - m * cell, y0 - m * cell + j * cell, x0 - m * cell + cols * cell, y0 - m * cell + j * cell, GRIDC))
    for (c, r) in cells:
        x, y = x0 + c * cell, y0 + r * cell
        for (dc, dr, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                         (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (c + dc, r + dr) not in cells:
                g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='square'/>"
                         % (x1, y1, x2, y2, GREEN))
    return "".join(g)


def shape_svg(cells, label, cell=20):
    L = max(c for c, r in cells) + 1
    W = max(r for c, r in cells) + 1
    m = 4
    cols, rows = L + 2, W + 2
    body = cells_body(set(cells), m + cell, m + cell, cols, rows, cell, m=1)
    return svg_wrap(cols * cell + 2 * m, rows * cell + 2 * m, body, label)


def rect_cells(L, W):
    return {(c, r) for c in range(L) for r in range(W)}


def grid_perimeter(cells):
    return sum(1 for (c, r) in cells for (dc, dr) in [(0, 1), (0, -1), (1, 0), (-1, 0)] if (c + dc, r + dr) not in cells)


def edge_cells(cells):
    return sum(1 for (c, r) in cells if any((c + dc, r + dr) not in cells for dc in (-1, 0, 1) for dr in (-1, 0, 1)))


# ------------------------------------------------------------ rectilinear figures (side labels placed outside)
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


INSIDE_OK = False   # never move a label inside the figure (it looks like it belongs to another side)


def poly_body(pts, labels, dashed=()):
    """Polygon (pixel points) with a label outside the middle of each side ('' = no label; 'x' or '?' red).
    dashed = inside segments ((x1, y1), (x2, y2)) in the same pixel space. Returns (body, W, H)."""
    CW, TH = 9.6, 13
    m = len(pts)
    texts = []
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % m]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        Ln = math.hypot(dx, dy)
        nx, ny = dy / Ln, -dx / Ln
        if inside((mx + nx * 2, my + ny * 2), pts):
            nx, ny = -nx, -ny
        t = labels[i]
        if not t:
            continue
        hw = CW * len(t) / 2
        off = 8 + abs(nx) * hw + abs(ny) * TH
        texts.append([mx + nx * off, my + ny * off, hw, t, dx / Ln, dy / Ln, Ln, 0.0, nx, ny, False, mx, my, off])

    def hit(A, B):
        return abs(A[0] - B[0]) < A[2] + B[2] + 8 and abs(A[1] - B[1]) < 23

    for _ in range(80):
        moved = False
        for a in range(len(texts)):
            for b in range(a + 1, len(texts)):
                A, B = texts[a], texts[b]
                if hit(A, B):
                    done = False
                    for P in sorted((A, B), key=lambda z: z[6]):
                        if P[10] or not INSIDE_OK:
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
                            P[7] += sgn * 2
                            P[0] += sgn * 2 * P[4]
                            P[1] += sgn * 2 * P[5]
                        else:
                            P[0] += 2 * P[8]
                            P[1] += 2 * P[9]
                    moved = True
        if not moved:
            break
    for a in range(len(texts)):
        for b in range(a + 1, len(texts)):
            assert not hit(texts[a], texts[b]), (texts[a][3], texts[b][3])
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
    for x, y, hw, t in texts:
        s.append(text(x - ox, y - oy + 6, t, 17, colr(t)))
    return "".join(s), W, H


def polygon_svg(pts, labels, label, dashed=()):
    body, W, H = poly_body(pts, labels, dashed)
    return svg_wrap(W, H, body, label)


def scale_of(units, max_w=250, max_h=150):
    W = max(x for x, y in units) - min(x for x, y in units)
    H = max(y for x, y in units) - min(y for x, y in units)
    return min(max_w / W, max_h / H)


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


def solve_side(units, i):
    """A hidden side from the other sides that run the same way: value = sum(opposite) − sum(same)."""
    m = len(units)
    h = is_h(units, i)
    ax = 0 if h else 1
    sign = lambda j: (units[(j + 1) % m][ax] - units[j][ax])
    s_i = sign(i)
    opp, same = [], []
    for j in range(m):
        if j == i or is_h(units, j) != h:
            continue
        v = abs(sign(j))
        (same if (sign(j) > 0) == (s_i > 0) else opp).append(v)
    val = sum(opp) - sum(same)
    assert val == abs(s_i), (units, i)
    return val, opp, same


def flip_pt(p, W, H, fx, fy):
    return ((W - p[0]) if fx else p[0], (H - p[1]) if fy else p[1])


def make_L(a, d, c, b, fx, fy):
    """a × d rectangle with an (a − c) × (d − b) corner missing. Pieces: a × b and c × (d − b).
    Returns units (clockwise on screen) and the dashed split line."""
    u = [(0, 0), (a, 0), (a, b), (c, b), (c, d), (0, d)]
    u = [flip_pt(p, a, d, fx, fy) for p in u]
    if fx != fy:
        u = u[::-1]
    split = (flip_pt((0, b), a, d, fx, fy), flip_pt((c, b), a, d, fx, fy))
    assert ortho_area(u) == a * b + c * (d - b)
    return u, split


def make_T(W, H, h, l, r, fy=False):
    """Top bar W × h with a stem (r − l) × (H − h) under it."""
    u = [(0, 0), (W, 0), (W, h), (r, h), (r, H), (l, H), (l, h), (0, h)]
    u = [flip_pt(p, W, H, False, fy) for p in u]
    split = (flip_pt((l, h), W, H, False, fy), flip_pt((r, h), W, H, False, fy))
    assert ortho_area(u) == W * h + (r - l) * (H - h)
    return u, split


def ortho_svg(units, labels, label, split=None):
    k = scale_of(units)
    pts = [(x * k, y * k) for x, y in units]
    dashed = [((split[0][0] * k, split[0][1] * k), (split[1][0] * k, split[1][1] * k))] if split else ()
    return polygon_svg(pts, labels, label, dashed)


# ------------------------------------------------------------ drawing canvas for bar models and paths (y down)
class Canvas:
    def __init__(self):
        self.el, self.boxes, self.segs, self.fixed = [], [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        self.segs += [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def rect(self, x, y, w, h, fill, sw=1.6, col=GREEN):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, sw, col)

    def line(self, a, b, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text. Labels never touch each other and no line runs through them."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def check(self):
        for (x0, y0, x1, y1) in self.boxes:
            for a, b in self.segs:
                for i in range(61):
                    x, y = a[0] + (b[0] - a[0]) * i / 60, a[1] + (b[1] - a[1]) * i / 60
                    assert not (x0 - 1 < x < x1 + 1 and y0 - 1 < y < y1 + 1), ("line through a label", (x0, y0, x1, y1))

    def svg(self, label, pad=5):
        self.check()
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "l":
                _, a, b, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' "
                         "stroke-linecap='round'/>" % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def model_svg(rows, label="bar model", braces=(), unit=None, maxw=240):
    """rows = [(name, [(units, fill, text)], right_text)]. braces = [(row, u0, u1, text, 'above'|'below')].
    Whole units are drawn as equal boxes; a part that is not a whole unit is one box of its exact length.
    A segment's text goes under a brace below it."""
    braces = list(braces)
    for ri, (name, segs, right) in enumerate(rows):
        u0 = 0
        for n, fill, t in segs:
            if t:
                braces.append((ri, u0, u0 + n, t, "below"))
            u0 += n
    nw = max(tw(r[0], 15) for r in rows) + 10
    most = max(sum(s[0] for s in r[1]) for r in rows)
    U = unit or min(maxw / most, 46)
    cv = Canvas()
    y = 0
    BH = 28
    for ri, (name, segs, right) in enumerate(rows):
        if any(b[0] == ri and b[4] == "above" for b in braces):
            y += 30
        cv.text(nw - 10, y + BH / 2, name, 15, "end")
        x = nw
        for n, fill, t in segs:
            if n == int(n):
                for j in range(int(n)):
                    cv.rect(x + j * U, y, U, BH, fill, 1.6)
            else:
                cv.rect(x, y, n * U, BH, fill, 1.6)
            x += n * U
        if right:
            cv.text(x + 8, y + BH / 2, right, 15, "start", colr(right))
        for b in braces:
            if b[0] != ri:
                continue
            _, u0, u1, t, pos = b
            xa, xb = nw + u0 * U + 2, nw + u1 * U - 2
            yy = y - 8 if pos == "above" else y + BH + 8
            tick = 6 if pos == "above" else -6
            cv.line((xa, yy), (xb, yy), sw=1.6, col=INK)
            cv.line((xa, yy), (xa, yy + tick), sw=1.6, col=INK)
            cv.line((xb, yy), (xb, yy + tick), sw=1.6, col=INK)
            cv.text((xa + xb) / 2, yy - 11 if pos == "above" else yy + 11, t, 15, col=colr(t))
        y += BH
        if any(b[0] == ri and b[4] == "below" for b in braces):
            y += 30
        y += 12
    return cv.svg(label)


def path_svg(L, B, w, label="garden with a path around it", k=11):
    """Garden L × B (m) with a path w m wide all round it, drawn to scale."""
    cv = Canvas()
    OL, OB = (L + 2 * w) * k, (B + 2 * w) * k
    cv.rect(0, 0, OL, OB, PATH, 2.4, INK)
    cv.rect(w * k, w * k, L * k, B * k, FILL, 2.4, GREEN)
    cv.text(OL / 2, w * k + 16, "%d m" % L, 15)
    cv.text(w * k + 22, OB / 2 + 8, "%d m" % B, 15)
    cv.text(OL / 2 + 14, OB / 2 + 8, "Garden", 15, col=GREEN)
    cv.text(OL / 2, OB + 15, "Path %d m wide" % w, 15)
    return cv.svg(label)


def cross_svg(L, B, w, label="field with two paths crossing it", k=9):
    """Field L × B (m) with a path w m wide along the middle of its length and one along the middle of its breadth."""
    cv = Canvas()
    Lp, Bp = L * k, B * k
    cv.rect(0, 0, Lp, Bp, FILL, 2.4, GREEN)
    cv.rect(0, (Bp - w * k) / 2, Lp, w * k, PATH, 1.6, INK)
    cv.rect((Lp - w * k) / 2, 0, w * k, Bp, PATH, 1.6, INK)
    cv.text(Lp / 2, -14, "%d m" % L, 15)
    cv.text(-8, Bp / 2, "%d m" % B, 15, "end")
    cv.text(Lp / 2, Bp + 15, "Each path is %d m wide" % w, 15)
    return cv.svg(label)


# ============================================================ set 1: review
def set_review(rnd, P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e, rnd))

    for L, W, u in [(9, 6, "cm"), (12, 5, "m"), (8, 7, "cm")]:
        A, Pm = L * W, 2 * (L + W)
        assert len({A, Pm, L + W, 2 * A}) == 4
        add(fig(rect_svg(L, W, q_(L, u), q_(W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
            "What is the area of this rectangle?", q_(A, SQ[u]),
            [q_(Pm, SQ[u]), q_(L + W, SQ[u]), q_(2 * A, SQ[u])],
            "Area = length × breadth = %d × %d = %d %s. (%d %s is the perimeter, %d + %d = %d only adds two sides, "
            "and %d doubles the area.)" % (L, W, A, SQ[u], Pm, u, L, W, L + W, 2 * A))
    for L, W, u in [(11, 4, "cm"), (15, 6, "m"), (13, 8, "cm")]:
        A, Pm = L * W, 2 * (L + W)
        assert len({A, Pm, L + W, 2 * L + W}) == 4
        add(fig(rect_svg(L, W, q_(L, u), q_(W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
            "What is the perimeter of this rectangle?", q_(Pm, u),
            [q_(L + W, u), q_(2 * L + W, u), q_(A, u)],
            "Perimeter = 2 × (length + breadth) = 2 × (%d + %d) = 2 × %d = %d %s. "
            "(%d %s goes only halfway round; %d × %d = %d is the area.)"
            % (L, W, L + W, Pm, u, L + W, u, L, W, A))
    # area with 2-digit × 2-digit (P4: 3-digit by 2-digit multiplication)
    for L, W, u, thing in [(24, 15, "cm", "A rectangular poster"), (35, 18, "m", "A rectangular car park")]:
        A, Pm = L * W, 2 * (L + W)
        t, o = divmod(W, 10)
        slip = L * t + L * o            # forgot that the 1 in 15 is 1 ten
        assert A == L * 10 * t + L * o and len({A, Pm, L + W, slip}) == 4
        add("%s has a length of %d %s and a breadth of %d %s. What is its area?" % (thing, L, u, W, u),
            q_(A, SQ[u]), [q_(slip, SQ[u]), q_(Pm, SQ[u]), q_(L + W, SQ[u])],
            "Area = %d × %d. %d × 10 = %d and %d × %d = %d. %d + %d = %d %s. (%d comes from writing %d × 1 "
            "instead of %d × 10.)" % (L, W, L, L * 10, L, o, L * o, L * 10, L * o, A, SQ[u], slip, L, L))
    L, W = 125, 80
    add("A school field has a length of 125 m and a breadth of 80 m. What is its perimeter?", "410 m",
        ["205 m", "330 m", q_(L * W, "m")],
        "2 × (125 + 80) = 2 × 205 = 410 m. (205 m goes only halfway round, 330 m leaves out one breadth, "
        "and 125 × 80 = 10" + NB + "000 is the area.)")
    assert 2 * (125 + 80) == 410 and 125 * 80 == 10000
    add("A rectangular table top has a length of 1 m and a breadth of 45 cm. What is its perimeter in centimetres?", "290 cm",
        ["92 cm", "145 cm", "245 cm"],
        "Change to one unit first: 1 m = 100 cm. 2 × (100 + 45) = 2 × 145 = 290 cm. "
        "(92 comes from 2 × (1 + 45), mixing metres and centimetres.)")
    assert 2 * (100 + 45) == 290 and 2 * (1 + 45) == 92
    # squares
    add("A square has sides of 9 cm. What is its area?", "81 cm²", ["36 cm²", "18 cm²", "72 cm²"],
        "Area of a square = side × side = 9 × 9 = 81 cm². (4 × 9 = 36 is the perimeter; 72 is 9 × 8, "
        "a slip in the multiplication table.)")
    add("A square has sides of 14 m. What is its perimeter?", "56 m", ["196 m", "28 m", "42 m"],
        "A square has 4 equal sides: 4 × 14 = 56 m. (14 × 14 = 196 is the area; 28 m and 42 m count only "
        "2 or 3 sides.)")
    # counting squares on a grid
    cells = rect_cells(7, 4)
    assert len(cells) == 28 and grid_perimeter(cells) == 22 and edge_cells(cells) == 18
    add(fig(shape_svg(cells, "rectangle 7 squares by 4 squares on a 1-cm grid")) +
        "Each small square is 1 cm by 1 cm. What is the area of the shaded rectangle?", "28 cm²",
        ["22 cm²", "18 cm²", "11 cm²"],
        "4 rows of 7 squares: 4 × 7 = 28 squares, so the area is 28 cm². (22 cm is the perimeter; "
        "18 counts only the squares along the edge.)")
    cells = rect_cells(6, 5)
    assert len(cells) == 30 and grid_perimeter(cells) == 22 and edge_cells(cells) == 18
    add(fig(shape_svg(cells, "rectangle 6 squares by 5 squares on a 1-cm grid")) +
        "Each small square is 1 cm by 1 cm. What is the perimeter of the shaded rectangle?", "22 cm",
        ["30 cm", "18 cm", "11 cm"],
        "Count the 1-cm sides all round: 6 + 5 + 6 + 5 = 22 cm. (30 is the number of squares, the area. "
        "18 counts the edge squares, but each corner square has two sides on the edge.)")
    # units
    U4 = ["m", "cm", "m²", "cm²"]
    add("Which unit is best for the area of a classroom floor?", "m²", [x for x in U4 if x != "m²"],
        "Area is the space inside, so it needs a square unit. A floor is big, so use square metres, m².")
    add("Which unit is best for the length of ribbon round the edge of a birthday card?", "cm",
        [x for x in U4 if x != "cm"],
        "Ribbon round the edge is a perimeter, so it needs a length unit. A card is small, so use centimetres.")
    # rules
    add("Which gives the perimeter of a rectangle?", "2 × (length + breadth)",
        ["length × breadth", "length + breadth", "4 × length"],
        "Perimeter is the distance round: 2 lengths and 2 breadths, which is 2 × (length + breadth). "
        "length × breadth is the area.")
    add("Which gives the area of a rectangle?", "length × breadth",
        ["2 × (length + breadth)", "length + breadth", "2 × length × breadth"],
        "Area counts the unit squares inside: rows × squares in each row = length × breadth.")
    add("Rectangle A is 9 cm by 4 cm. Rectangle B is a square with sides of 6 cm. Both have an area of 36 cm². "
        "Which has the longer perimeter?", "A, by 2 cm", ["B, by 2 cm", "They are the same", "A, by 4 cm"],
        "A: 2 × (9 + 4) = 26 cm. B: 4 × 6 = 24 cm. 26 − 24 = 2, so A is longer by 2 cm. "
        "The same area does not mean the same perimeter.")
    assert 2 * (9 + 4) == 26 and 4 * 6 == 24
    add("Which rectangle has an area of 24 cm²?", "6 cm by 4 cm",
        ["8 cm by 4 cm", "20 cm by 4 cm", "12 cm by 12 cm"],
        "6 × 4 = 24 cm². (8 cm by 4 cm has a perimeter of 24 cm, not an area of 24 cm². 20 + 4 and 12 + 12 "
        "add to 24, but area means multiplying.)")
    assert 6 * 4 == 24 and 2 * (8 + 4) == 24 and 8 * 4 != 24
    assert len(its) == 20, len(its)
    return {"title": "Area and perimeter of rectangles and squares", "items": its}


# ============================================================ set 2: missing length or breadth
def set_missing(rnd, P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e, rnd))

    # from the area, with a figure
    for A, known, u, side in [(40, 8, "cm", "b"), (54, 9, "m", "b"), (36, 9, "cm", "b"), (60, 5, "m", "l"),
                              (78, 6, "cm", "l")]:
        x = A // known
        assert x * known == A and x != known
        if side == "b":
            svg = rect_svg(known, x, q_(known, u), "? " + u, "rectangle with an area of %d %s and its breadth missing"
                           % (A, SQ[u]), inner="Area = %d %s" % (A, SQ[u]))
            ask = "breadth"
        else:
            svg = rect_svg(x, known, "? " + u, q_(known, u), "rectangle with an area of %d %s and its length missing"
                           % (A, SQ[u]), inner="Area = %d %s" % (A, SQ[u]))
            ask = "length"
        add(fig(svg) + "The area of the rectangle is %d %s. What is its %s?" % (A, SQ[u], ask), q_(x, u),
            [opt(A - known, u), opt(A / 2 - known, u), opt(A / 2, u), opt(A / 4, u)],
            "Area = length × breadth, so %d × ? = %d. %d ÷ %d = %d. The %s is %d %s. Check: %d × %d = %d. "
            "(Subtracting, %d − %d = %d, is a common mistake.)"
            % (known, A, A, known, x, ask, x, u, known, x, A, A, known, A - known))
    # from the area, in words
    for A, B, u in [(96, 8, "cm"), (126, 9, "m"), (150, 10, "cm"), (168, 7, "m")]:
        L = A // B
        assert L * B == A and L > B
        add("A rectangle has an area of %d %s. Its breadth is %d %s. What is its length?" % (A, SQ[u], B, u),
            q_(L, u), [opt(A - B, u), opt(A / 2 - B, u), opt(A / 2, u), opt(A / 4, u)],
            "Length = area ÷ breadth = %d ÷ %d = %d %s. Check: %d × %d = %d %s." % (A, B, L, u, L, B, A, SQ[u]))
    # from the perimeter
    for Pm, known, u, kn, ask, figure in [(30, 9, "cm", "length", "breadth", True), (40, 12, "m", "length", "breadth", False),
                                          (54, 15, "cm", "length", "breadth", False),
                                          (36, 7, "cm", "breadth", "length", True), (70, 20, "m", "length", "breadth", False)]:
        half = Pm // 2
        x = half - known
        assert Pm % 2 == 0 and x > 0 and x != known and 2 * (x + known) == Pm
        assert (x < known) == (ask == "breadth")
        if figure:
            L, W = (known, x) if kn == "length" else (x, known)
            top = q_(L, u) if kn == "length" else "? " + u
            left = "? " + u if kn == "length" else q_(W, u)
            q = fig(rect_svg(L, W, top, left, "rectangle with a perimeter of %d %s and one side missing" % (Pm, u)))
            q += "The perimeter of the rectangle is %d %s. What is its %s?" % (Pm, u, ask)
        else:
            q = "A rectangle has a perimeter of %d %s. Its %s is %d %s. What is its %s?" % (Pm, u, kn, known, u, ask)
        add(q, q_(x, u), [opt(Pm - 2 * known, u), opt(Pm - known, u), opt(half, u), opt(Pm / 4, u)],
            "Half the perimeter is length + breadth: %d ÷ 2 = %d %s. %s = %d − %d = %d %s. "
            "(%d − %d − %d = %d is two %ss, so it still needs halving.)"
            % (Pm, half, u, ask.capitalize(), half, known, x, u, Pm, known, known, Pm - 2 * known, ask))
    # half the perimeter
    add("A rectangle has a perimeter of 54 cm. What is its length + breadth?", "27 cm",
        ["108 cm", "54 cm", "13.5 cm"],
        "The perimeter is 2 lengths + 2 breadths. Half of it is 1 length + 1 breadth: 54 ÷ 2 = 27 cm. "
        "(13.5 cm divides by 4, as for a square.)")
    add("The length + breadth of a rectangle is 19 m. What is its perimeter?", "38 m", ["19 m", "76 m", "57 m"],
        "Perimeter = 2 × (length + breadth) = 2 × 19 = 38 m. (76 m multiplies by 4, as for a square.)")
    # two steps: perimeter from area
    for A, L, u in [(48, 8, "cm"), (63, 9, "m")]:
        B = A // L
        Pm = 2 * (L + B)
        assert B * L == A
        add("A rectangle has an area of %d %s and a length of %d %s. What is its perimeter?" % (A, SQ[u], L, u),
            q_(Pm, u), [q_(A, u), q_(L + B, u), q_(2 * L + B, u)],
            "Step 1: breadth = %d ÷ %d = %d %s. Step 2: perimeter = 2 × (%d + %d) = %d %s. "
            "(%d %s is only length + breadth.)" % (A, L, B, u, L, B, Pm, u, L + B, u))
    # two steps: area from perimeter
    for Pm, L, u in [(36, 10, "cm"), (50, 15, "m")]:
        B = Pm // 2 - L
        A = L * B
        wrongB = Pm - 2 * L
        assert B > 0 and B < L
        add("A rectangle has a perimeter of %d %s and a length of %d %s. What is its area?" % (Pm, u, L, u),
            q_(A, SQ[u]), [q_(L * wrongB, SQ[u]), q_(Pm * L, SQ[u]), q_(Pm // 2, SQ[u])],
            "Step 1: length + breadth = %d ÷ 2 = %d, so breadth = %d − %d = %d %s. Step 2: area = %d × %d = %d %s. "
            "(%d comes from using %d − %d − %d = %d as the breadth without halving.)"
            % (Pm, Pm // 2, Pm // 2, L, B, u, L, B, A, SQ[u], L * wrongB, Pm, L, L, wrongB))
    assert len(its) == 20, len(its)
    return {"title": "Find the length or breadth", "items": its}


# ============================================================ set 3: side of a square
def set_square(rnd, P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e, rnd))

    for A, u, figure in [(49, "cm", True), (81, "cm", True), (36, "m", True), (25, "m", False), (64, "cm", False),
                         (100, "m", False)]:
        s = math.isqrt(A)
        assert s * s == A
        if figure:
            q = (fig(rect_svg(s, s, "? " + u, "", "square with an area of %d %s" % (A, SQ[u]),
                              inner=q_(A, SQ[u]), max_w=110, max_h=110)) +
                 "The area of this square is %d %s. How long is each side?" % (A, SQ[u]))
        else:
            q = "A square has an area of %d %s. How long is each side?" % (A, SQ[u])
        cands = [q_(A // 4, u) if A % 4 == 0 else None, q_(4 * s, u), q_(A // 2, u) if A % 2 == 0 else None,
                 q_(s + 1, u), q_(s - 1, u)]
        add(q, q_(s, u), cands,
            "Side × side = %d. Use the multiplication table: %d × %d = %d, so each side is %d %s. "
            "(Do not divide %d by 4 or by 2: that is for a perimeter. 4 × %d = %d %s is the perimeter.)"
            % (A, s, s, A, s, u, A, s, 4 * s, u))
    for Pm, u, figure in [(36, "cm", True), (52, "m", False), (80, "cm", False), (28, "m", True), (100, "cm", False)]:
        s = Pm // 4
        assert 4 * s == Pm
        if figure:
            q = (fig(rect_svg(s, s, "? " + u, "", "square with one side missing", max_w=90, max_h=90)) +
                 "The perimeter of this square is %d %s. How long is each side?" % (Pm, u))
        else:
            q = "A square has a perimeter of %d %s. How long is each side?" % (Pm, u)
        add(q, q_(s, u), [q_(Pm // 2, u), q_(Pm - 4, u), q_(4 * Pm, u)],
            "A square has 4 equal sides: %d ÷ 4 = %d %s. Check: 4 × %d = %d. "
            "(%d ÷ 2 = %d is two sides, not one.)" % (Pm, s, u, s, Pm, Pm, Pm // 2))
    # perimeter -> area
    for Pm, u, ctx in [(28, "cm", "A square has a perimeter of 28 cm."),
                       (40, "m", "A square garden has a perimeter of 40 m."),
                       (32, "cm", "A square tile has a perimeter of 32 cm."),
                       (48, "cm", "A piece of wire 48 cm long is bent to form a square.")]:
        s = Pm // 4
        A = s * s
        add(ctx + " What is its area?" if "wire" not in ctx else ctx + " What is the area of the square?",
            q_(A, SQ[u]), [q_(Pm * Pm, SQ[u]), q_((Pm // 2) ** 2, SQ[u]), q_(s, SQ[u])],
            "Step 1: side = %d ÷ 4 = %d %s. Step 2: area = %d × %d = %d %s. "
            "(%d uses half the perimeter, %d, as the side: halving instead of dividing by 4.)"
            % (Pm, s, u, s, s, A, SQ[u], (Pm // 2) ** 2, Pm // 2))
    # area -> perimeter
    for A, u in [(64, "cm"), (36, "cm"), (81, "m")]:
        s = math.isqrt(A)
        Pm = 4 * s
        add("A square has an area of %d %s. What is its perimeter?" % (A, SQ[u]), q_(Pm, u),
            [q_(A // 4, u) if A % 4 == 0 else None, q_(A, u), q_(s, u), q_(2 * s, u)],
            "Step 1: %d × %d = %d, so each side is %d %s. Step 2: perimeter = 4 × %d = %d %s. "
            "(%d %s is only one side.)" % (s, s, A, s, u, s, Pm, u, s, u))
    # compare with a rectangle
    assert 9 * 4 == 36 == 6 * 6 and 2 * (9 + 4) / 4 == 6.5
    add("A square has the same area as a rectangle 9 cm by 4 cm. How long is each side of the square?", "6 cm",
        ["6.5 cm", "9 cm", "13 cm"],
        "Area of the rectangle = 9 × 4 = 36 cm². The square also has 36 cm², and 6 × 6 = 36, so each side is 6 cm. "
        "(6.5 cm would give the same perimeter, 26 cm, not the same area.)")
    assert 4 * 6 == 2 * (8 + 4) == 24 and 6 * 6 - 8 * 4 == 4
    add("A square and a rectangle both have a perimeter of 24 cm. The rectangle is 8 cm long. "
        "Which has the bigger area?", "The square, by 4 cm²",
        ["The rectangle, by 4 cm²", "They are the same", "The square, by 2 cm²"],
        "Square: side = 24 ÷ 4 = 6 cm, area = 36 cm². Rectangle: breadth = 12 − 8 = 4 cm, area = 8 × 4 = 32 cm². "
        "36 − 32 = 4 cm². The same perimeter does not mean the same area.")
    assert len(its) == 20, len(its)
    return {"title": "Side of a square from its area or perimeter", "items": its}


# ============================================================ set 4: composite figures
def find_x(units, i, u, kind, rnd):
    sides = ortho_sides(units)
    x, opp, same = solve_side(units, i)
    lab = [q_(v, u) for v in sides]
    lab[i] = "x"
    if same:
        part = ("the other part is %d %s" % (same[0], u) if len(same) == 1 else
                "the other parts are %s, which make %d %s" % (" and ".join("%d %s" % (v, u) for v in same), sum(same), u))
        e = ("Look at the sides that run the same way as x. The whole side is %d %s and %s. "
             "x = %d − %d = %d %s. (Using %d %s for x takes the whole side, not the part.)"
             % (sum(opp), u, part, sum(opp), sum(same), x, u, sum(opp), u))
        cands = [sum(opp), sum(opp) + sum(same), sum(same)] + [v for v in sides if v != x]
    else:
        e = ("x is a whole side. The parts across from it add up to it: %s = %d %s. "
             "(Subtracting the parts gives the wrong length.)" % (" + ".join(str(v) for v in opp), x, u))
        cands = [abs(opp[0] - opp[-1]) if len(opp) > 1 else None, max(opp), min(opp)] + [v for v in sides if v != x]
    cands = [q_(v, u) for v in cands if v and v != x]
    q = (fig(ortho_svg(units, lab, "%s with a missing side x" % kind)) +
         "All the corners are right angles. What is the length of side x?")
    return mcq(q, q_(x, u), cands, e, rnd)


def perim(units, hide, u, kind, rnd, extra=""):
    sides = ortho_sides(units)
    p = sum(sides)
    lab = [q_(v, u) for v in sides]
    for i in hide:
        lab[i] = "?"
    shown = sum(v for j, v in enumerate(sides) if j not in hide)
    cands = [shown]
    steps = []
    for i in hide:
        x, opp, same = solve_side(units, i)
        cands.append(p - x)
        if same:
            cands.append(p - x + sum(opp))      # used the whole side instead of the part
            grp = lambda v: str(v[0]) if len(v) == 1 else "(" + " + ".join(map(str, v)) + ")"
            steps.append("%s − %s = %d" % (grp(opp), grp(same), x))
        else:
            steps.append("%s = %d" % (" + ".join(map(str, opp)), x))
    cands += [ortho_area(units), p + 2]
    e = ("First find the missing sides: %s. Then add all %d sides: %s = %d %s. (%d %s adds only the sides "
         "with numbers.)" % (" and ".join(steps), len(sides), " + ".join(map(str, sides)), p, u, shown, u)) + extra
    q = (fig(ortho_svg(units, lab, "%s with missing sides" % kind)) +
         "All the corners are right angles. What is the perimeter of the figure?")
    return mcq(q, q_(p, u), [q_(c, u) for c in cands if c and c != p], e, rnd)


def area_L(a, d, c, b, fx, fy, u, rnd, dashed, hide_one=False):
    units, split = make_L(a, d, c, b, fx, fy)
    sides = ortho_sides(units)
    lab = [q_(v, u) for v in sides]
    A1, A2 = a * b, c * (d - b)
    A = A1 + A2
    box, overlap, Pm = a * d, a * b + c * d, 2 * (a + d)
    assert len({A, box, overlap, Pm, A1}) == 5
    hidden = ""
    if hide_one:
        # hide the short inner side (the part d − b), which the student works out first
        for i, v in enumerate(sides):
            if not is_h(units, i) and v == d - b and v not in (b, d):
                lab[i] = "?"
                hidden = "First, the missing side is %d − %d = %d %s. " % (d, b, d - b, u)
                break
        assert hidden
    if dashed or hide_one:
        e = (hidden + "Split it into two rectangles: %d × %d = %d %s and %d × %d = %d %s. %d + %d = %d %s. "
             "(%d uses the whole side, %d %s, for the second rectangle, so the overlap is counted twice.)"
             % (a, b, A1, SQ[u], c, d - b, A2, SQ[u], A1, A2, A, SQ[u], overlap, d, u))
    else:
        e = ("Take the missing corner away from the big rectangle: %d × %d = %d %s, and the corner is %d × %d = %d %s. "
             "%d − %d = %d %s. Or split it into two rectangles: %d + %d = %d. (%d %s is the whole big rectangle.)"
             % (a, d, box, SQ[u], a - c, d - b, (a - c) * (d - b), SQ[u], box, (a - c) * (d - b), A, SQ[u],
                A1, A2, A, box, SQ[u]))
    q = (fig(ortho_svg(units, lab, "L-shaped figure made of two rectangles", split if dashed else None)) +
         ("The figure is split into two rectangles. " if dashed else "All the corners are right angles. ") +
         "What is the area of the figure?")
    return mcq(q, q_(A, SQ[u]), [q_(overlap, SQ[u]), q_(box, SQ[u]), q_(Pm, SQ[u]), q_(A1, SQ[u])], e, rnd)


def set_composite(rnd, P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e, rnd))

    # find x on L shapes (3) and a T shape (1)
    for a, d, c, b, fx, fy, u, hv in [(12, 9, 5, 3, False, False, "cm", "h"), (14, 10, 6, 3, True, False, "m", "v"),
                                      (11, 8, 4, 5, False, True, "cm", "v")]:
        units, _ = make_L(a, d, c, b, fx, fy)
        S = ortho_sides(units)
        assert len(set(S)) == 6
        # the inner side that is a part (not a whole side of the outline)
        want = (a - c) if hv == "h" else (d - b)
        i = [j for j in range(6) if (is_h(units, j) == (hv == "h")) and S[j] == want][0]
        its.append(find_x(units, i, u, "L-shaped figure", rnd))
    units, _ = make_T(13, 9, 3, 4, 9)
    S = ortho_sides(units)
    i = [j for j in range(8) if is_h(units, j) and S[j] == 4 and units[j][1] == 3][0]
    its.append(find_x(units, i, "cm", "T-shaped figure", rnd))
    # perimeter with missing sides: L (3) and T (1)
    for a, d, c, b, fx, fy, u in [(10, 7, 4, 2, False, False, "cm"), (15, 11, 6, 4, True, True, "m"),
                                  (13, 9, 8, 3, False, True, "cm")]:
        units, _ = make_L(a, d, c, b, fx, fy)
        S = ortho_sides(units)
        assert len(set(S)) == 6
        hs = [j for j in range(6) if is_h(units, j) and S[j] == a - c]
        vs = [j for j in range(6) if not is_h(units, j) and S[j] == d]
        extra = (" Shortcut: an L-shaped figure has the same perimeter as the rectangle round it: "
                 "2 × (%d + %d) = %d." % (a, d, 2 * (a + d)))
        assert sum(S) == 2 * (a + d)
        its.append(perim(units, [hs[0], vs[0]], u, "L-shaped figure", rnd, extra))
    units, _ = make_T(14, 10, 4, 5, 9, fy=True)
    S = ortho_sides(units)
    hide = [j for j in range(8) if is_h(units, j) and S[j] == 5][:1] + [j for j in range(8) if not is_h(units, j) and S[j] == 6][:1]
    assert len(hide) == 2
    its.append(perim(units, hide, "cm", "T-shaped figure", rnd))
    # area of L shapes
    for args in [(10, 8, 4, 3, False, False, "cm", True, False), (12, 9, 5, 4, True, False, "m", True, False),
                 (9, 7, 4, 3, False, True, "cm", False, True), (14, 10, 6, 4, True, True, "m", False, False),
                 (11, 9, 5, 4, False, False, "cm", False, False)]:
        its.append(area_L(*args[:7], rnd, dashed=args[7], hide_one=args[8]))
    # area of T shapes
    for W, H, h, l, r, fy, u, dashed in [(12, 9, 3, 4, 8, False, "cm", True), (15, 10, 4, 5, 10, True, "m", False)]:
        units, split = make_T(W, H, h, l, r, fy)
        S = ortho_sides(units)
        lab = [q_(v, u) for v in S]
        A1, A2 = W * h, (r - l) * (H - h)
        A = A1 + A2
        overlap, box = W * h + (r - l) * H, W * H
        add(fig(ortho_svg(units, lab, "T-shaped figure made of two rectangles", split if dashed else None)) +
            ("The figure is split into two rectangles. " if dashed else "All the corners are right angles. ") +
            "What is the area of the figure?", q_(A, SQ[u]),
            [q_(overlap, SQ[u]), q_(box, SQ[u]), q_(sum(S), SQ[u]), q_(A1, SQ[u])],
            "Top bar: %d × %d = %d %s. Stem: %d × %d = %d %s (its height is %d − %d = %d). %d + %d = %d %s. "
            "(%d uses the whole height, %d %s, for the stem and counts the overlap twice.)"
            % (W, h, A1, SQ[u], r - l, H - h, A2, SQ[u], H, h, H - h, A1, A2, A, SQ[u], overlap, H, u))
    # on a grid
    cells = {(x, y) for x in range(8) for y in range(5) if not (x >= 5 and y < 2)}
    A, Pg, ed = len(cells), grid_perimeter(cells), edge_cells(cells)
    assert A == 34 and Pg == 26 and 8 * 5 == 40
    add(fig(shape_svg(cells, "L-shaped figure on a 1-cm grid")) +
        "Each small square is 1 cm by 1 cm. What is the area of the shaded figure?", "34 cm²",
        ["40 cm²", "26 cm²", "%d cm²" % ed],
        "Split it into two rectangles: 5 × 5 = 25 and 3 × 3 = 9. 25 + 9 = 34 cm². "
        "(40 cm² counts the empty corner too; 26 cm is the perimeter.)")
    cells = {(x, y) for x in range(7) for y in range(6) if not (2 <= x < 5 and y >= 3)}
    A, Pg, ed = len(cells), grid_perimeter(cells), edge_cells(cells)
    assert A == 33 and Pg == 32 and 2 * (7 + 6) == 26
    add(fig(shape_svg(cells, "U-shaped figure on a 1-cm grid")) +
        "Each small square is 1 cm by 1 cm. What is the perimeter of the shaded figure?", "32 cm",
        ["26 cm", "33 cm", "%d cm" % ed],
        "Count the 1-cm sides all round: 7 + 6 + 2 + 3 + 3 + 3 + 2 + 6 = 32 cm. (26 cm is the rectangle round it, "
        "which misses the two 3-cm sides inside the gap; 33 is the number of squares, the area.)")
    # two squares side by side
    s1, s2 = 6, 4
    units = [(0, 0), (s1, 0), (s1, s1 - s2), (s1 + s2, s1 - s2), (s1 + s2, s1), (0, s1)]
    S = ortho_sides(units)
    Pm, A = sum(S), s1 * s1 + s2 * s2
    assert Pm == 32 and A == 52 and 4 * s1 + 4 * s2 == 40
    lab = ["6 cm", "", "4 cm", "", "", ""]
    svg = ortho_svg(units, lab, "figure made of two squares", ((s1, s1 - s2), (s1, s1)))
    add(fig(svg) + "The figure is made of a square of side 6 cm and a square of side 4 cm. "
        "What is its perimeter?", "32 cm", ["40 cm", "52 cm", "36 cm"],
        "Go round the outside: 6 + 2 + 4 + 4 + 10 + 6 = 32 cm. (40 cm adds both perimeters, 24 + 16, and counts "
        "the 4-cm line where the squares touch twice. 52 cm² is the area.)")
    s1, s2 = 7, 5
    units = [(0, 0), (s1, 0), (s1, s1 - s2), (s1 + s2, s1 - s2), (s1 + s2, s1), (0, s1)]
    A = s1 * s1 + s2 * s2
    assert A == 74 and 12 * 7 == 84
    svg = ortho_svg(units, ["7 m", "", "5 m", "", "", ""], "figure made of two squares", ((s1, s1 - s2), (s1, s1)))
    add(fig(svg) + "The figure is made of a square of side 7 m and a square of side 5 m. What is its area?",
        "74 m²", ["84 m²", "35 m²", "49 m²"],
        "Big square: 7 × 7 = 49 m². Small square: 5 × 5 = 25 m². 49 + 25 = 74 m². "
        "(84 m² is the whole 12 m by 7 m rectangle round it; 35 m² multiplies the two numbers shown, 7 × 5; "
        "49 m² is only the big square.)")
    assert 2 * (12 + 7) == 38
    # concept
    add("A rectangle 10 cm by 8 cm has a 3 cm by 2 cm piece cut from one corner, making an L-shaped figure. "
        "Which is true?", "The area is smaller but the perimeter is the same",
        ["Both the area and the perimeter are smaller", "The area and the perimeter stay the same",
         "The area is smaller and the perimeter is longer"],
        "Area: 80 − 6 = 74 cm², smaller. Perimeter: the two new sides inside the corner (3 cm and 2 cm) "
        "replace the 3 cm and 2 cm that were cut off, so it stays 36 cm.")
    assert 10 * 8 - 3 * 2 == 74 and 2 * (10 + 8) == 36
    order = [0, 4, 8, 1, 5, 9, 2, 6, 15, 10, 3, 16, 7, 11, 13, 12, 17, 14, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Composite figures: find the missing sides first", "items": its}


# ============================================================ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, r, w, e):
        its.append(mcq(q, r, w, e, rnd))

    n1 = P.next()
    assert 2 * (15 + 9) == 48 and 15 * 9 == 135
    add("Mr Tan’s community garden plot is 15 m long and 9 m wide. He puts a fence all round it. "
        "How long is the fence?", "48 m", ["135 m", "24 m", "39 m"],
        "A fence goes round the edge, so find the perimeter: 2 × (15 + 9) = 2 × 24 = 48 m. "
        "(135 is the area; 24 m goes only halfway; 39 m leaves out one side.)")
    add("A rectangular playground at a void deck is 18 m long and 12 m wide. A fence goes all round it, "
        "except for a gate 2 m wide. How long is the fence?", "58 m", ["60 m", "62 m", "28 m"],
        "Perimeter = 2 × (18 + 12) = 60 m. Take away the gate: 60 − 2 = 58 m. (62 m adds the gate instead.)")
    assert 2 * (18 + 12) - 2 == 58
    name, he, his = P.next()
    assert 2 * (10 + 6) * 12 == 384 and 10 * 6 * 12 == 720
    add("%s’s family fences a rectangular herb garden 10 m long and 6 m wide. The fencing costs $12 per metre. "
        "How much does the fencing cost?" % name, "$384", ["$720", "$192", "$44"],
        "Fence = perimeter = 2 × (10 + 6) = 32 m. Cost = 32 × $12 = $384. ($720 uses the area, 60 m², "
        "$192 uses only 16 m, and $44 adds 32 + 12.)")
    assert (120 // 20) * (80 // 20) == 24 and 120 * 80 // 20 == 480
    add("A rectangular notice board is 120 cm long and 80 cm wide. It is covered with square cards of side "
        "20 cm, with no gaps. How many cards are needed?", "24", ["480", "10", "20"],
        "Along the length: 120 ÷ 20 = 6 cards. Along the breadth: 80 ÷ 20 = 4 cards. 6 × 4 = 24 cards. "
        "(480 divides the area by the side, 9600 ÷ 20; 10 adds 6 + 4.)")
    assert (500 // 50) * (400 // 50) == 80
    add("Mrs Ng’s living room floor is 5 m long and 4 m wide. She covers it with square tiles of side 50 cm. "
        "How many tiles does she need?", "80", ["20", "18", "40"],
        "Change to centimetres: 500 cm by 400 cm. 500 ÷ 50 = 10 tiles along, 400 ÷ 50 = 8 tiles across. "
        "10 × 8 = 80 tiles. (20 is the number of 1-m tiles; 18 adds 10 + 8.)")
    assert 64 // (2 * 2) == 16
    add("A square courtyard has an area of 64 m². It is paved with square tiles of side 2 m. "
        "How many tiles are needed?", "16", ["32", "8", "128"],
        "One tile covers 2 × 2 = 4 m². 64 ÷ 4 = 16 tiles. Or: each side is 8 m, so 4 tiles along and 4 across. "
        "(32 divides by the side, 2, instead of by the area of a tile, 4.)")
    assert 3 * 2 * 15 == 90
    add("A kitchen wall is 3 m long and 2 m high. Tiles for it cost $15 per square metre. How much do the "
        "tiles cost?", "$90", ["$150", "$75", "$20"],
        "Area = 3 × 2 = 6 m². Cost = 6 × $15 = $90. ($150 uses the perimeter, 10 m; $75 uses 3 + 2 = 5.)")
    # garden path round a garden
    assert (12 + 2) * (8 + 2) - 12 * 8 == 44
    add(fig(path_svg(12, 8, 1)) + "A garden 12 m by 8 m has a path 1 m wide all round it. "
        "What is the area of the path?", "44 m²", ["40 m²", "140 m²", "96 m²"],
        "Garden and path together: (12 + 1 + 1) × (8 + 1 + 1) = 14 × 10 = 140 m². Garden: 12 × 8 = 96 m². "
        "Path: 140 − 96 = 44 m². (40 m² leaves out the 4 corner squares of the path.)")
    # crossing paths
    assert 20 * 12 - 20 * 2 - 12 * 2 + 4 == 180 and 20 * 12 - 20 * 2 - 12 * 2 == 176 and 18 * 10 == 180
    add(fig(cross_svg(20, 12, 2)) + "A school field is 20 m long and 12 m wide. Two paths, each 2 m wide, cross "
        "it as shown. The rest of the field is grass. What is the area of the grass?", "180 m²",
        ["176 m²", "216 m²", "200 m²"],
        "Slide the four grass pieces together: (20 − 2) × (12 − 2) = 18 × 10 = 180 m². "
        "(176 m² takes away 40 m² and 24 m², which counts the 2 m by 2 m square where the paths cross twice. "
        "200 m² and 216 m² take away only one path.)")
    # bar model 1: length 3 times the breadth
    svg = model_svg([("Length", [(3, UNIT_FILL, "")], ""), ("Breadth", [(1, UNIT_FILL2, "")], "")],
                    "bar model of the length and breadth of a rectangle")
    assert 64 // 2 == 32 and 32 // 4 == 8 and 24 * 8 == 192 and 48 * 16 == 768
    add(fig(svg) + "The length of a rectangle is 3 times its breadth. Its perimeter is 64 cm. "
        "What is its area?", "192 cm²", ["768 cm²", "256 cm²", "32 cm²"],
        "Length + breadth = 64 ÷ 2 = 32 cm. In the model this is 4 units, so 1 unit = 32 ÷ 4 = 8 cm. "
        "Breadth = 8 cm, length = 3 × 8 = 24 cm. Area = 24 × 8 = 192 cm². "
        "(768 cm² comes from 4 units = 64, forgetting to halve the perimeter.)")
    # bar model 2: length 5 m longer
    svg = model_svg([("Length", [(1, UNIT_FILL, ""), (0.5, UNIT_FILL2, "5 m")], ""),
                     ("Breadth", [(1, UNIT_FILL, "")], "")],
                    "bar model: the length is 5 m longer than the breadth", maxw=150)
    assert (50 // 2 - 5) // 2 == 10 and 10 + 5 == 15
    add(fig(svg) + "A rectangular badminton practice area has a perimeter of 50 m. Its length is 5 m longer "
        "than its breadth. What is its length?", "15 m", ["20 m", "12.5 m", "22.5 m"],
        "Length + breadth = 50 ÷ 2 = 25 m. Take away the extra 5 m: 25 − 5 = 20 m = 2 units, so 1 unit = 10 m. "
        "Breadth = 10 m, length = 10 + 5 = 15 m. (20 m is 2 units, not the length; 12.5 m is 25 ÷ 2, which leaves out the extra 5 m; "
        "22.5 m comes from (50 − 5) ÷ 2.)")
    # bar model 3: wire cut into two pieces
    svg = model_svg([("Wire", [(2, UNIT_FILL, "A"), (1, UNIT_FILL2, "B")], "")], "bar model of a wire cut into two pieces",
                    braces=[(0, 0, 3, "60 cm", "above")])
    assert 60 // 3 == 20 and 20 // 4 == 5
    add(fig(svg) + "A wire 60 cm long is cut into two pieces, A and B. Piece A is twice as long as piece B. "
        "Each piece is bent to make a square. How long is each side of the smaller square?", "5 cm",
        ["20 cm", "10 cm", "15 cm"],
        "3 units = 60 cm, so 1 unit = 20 cm. Piece B is 20 cm, the perimeter of the smaller square. "
        "Side = 20 ÷ 4 = 5 cm. (20 cm is the whole piece; 10 cm halves it instead of dividing by 4; 15 cm is 60 ÷ 4.)")
    name, he, his = P.next()
    assert 16 * 4 == 64 == 8 * 8 and 4 * 8 == 32 and 2 * (16 + 4) == 40
    add("%s’s square garden has the same area as a rectangular garden 16 m by 4 m. How much fence does %s need "
        "to go round %s square garden?" % (name, he, his), "32 m", ["40 m", "64 m", "16 m"],
        "Area = 16 × 4 = 64 m². 8 × 8 = 64, so each side is 8 m. Fence = 4 × 8 = 32 m. "
        "(40 m is the fence for the rectangular garden.)")
    assert 5 * 3 - 2 * 1 == 13
    add("Students paint a mural on a wall 5 m long and 3 m high for National Day. A door 2 m high and 1 m wide "
        "in the wall is not painted. What area do they paint?", "13 m²", ["15 m²", "17 m²", "16 m²"],
        "Wall: 5 × 3 = 15 m². Door: 2 × 1 = 2 m². 15 − 2 = 13 m². "
        "(17 m² adds the door instead of taking it away; 16 m is the perimeter of the wall.)")
    name, he, his = P.next()
    assert 6 * 5 - 4 * 3 == 18 and (6 - 4) * (5 - 3) == 4
    add("%s’s bedroom floor in an HDB flat is 6 m long and 5 m wide. A rug 4 m by 3 m lies on it. What area "
        "of the floor is not covered?" % name, "18 m²", ["12 m²", "4 m²", "30 m²"],
        "Floor: 6 × 5 = 30 m². Rug: 4 × 3 = 12 m². 30 − 12 = 18 m². "
        "(4 m² comes from (6 − 4) × (5 − 3), taking away the sides instead of the areas.)")
    assert 30 * 20 - 4 * 5 * 5 == 500 and 30 * 20 - 5 * 5 == 575 and 30 * 20 - 4 * 5 == 580
    add("A rectangular card is 30 cm by 20 cm. A square of side 5 cm is cut from each of its 4 corners. "
        "What area of card is left?", "500 cm²", ["575 cm²", "580 cm²", "600 cm²"],
        "Card: 30 × 20 = 600 cm². One corner square: 5 × 5 = 25 cm². Four corners: 4 × 25 = 100 cm². "
        "600 − 100 = 500 cm². (575 takes away only one square; 580 takes away 4 × 5, the sides, not the areas.)")
    add("A rectangular card is 30 cm by 20 cm. A square of side 5 cm is cut from each of its 4 corners. "
        "What is the perimeter of the card that is left?", "100 cm", ["80 cm", "140 cm", "60 cm"],
        "At each corner, two 5-cm sides are cut off and two new 5-cm sides go in. So the perimeter stays "
        "2 × (30 + 20) = 100 cm. (80 cm takes away 4 × 5; 140 cm adds 8 × 5.)")
    assert 2 * (30 + 20) == 100
    name, he, his = P.next()
    assert 81 == 9 * 9 and 4 * 9 == 36
    add("%s makes a square Teachers’ Day card with an area of 81 cm². %s glues ribbon all round its edge. "
        "How much ribbon does %s need?" % (name, he.capitalize(), he), "36 cm", ["81 cm", "18 cm", "324 cm"],
        "9 × 9 = 81, so each side is 9 cm. Ribbon = perimeter = 4 × 9 = 36 cm. "
        "(324 cm is 4 × 81, using the area as a side.)")
    assert (30 - 14) // 2 == 8 and 30 - 14 == 16 and 30 // 2 == 15
    add("Mr Rahman builds a rectangular pen for his chickens against a wall. The wall is one length, 14 m, so it "
        "needs no fence. He uses 30 m of fencing for the other three sides. What is the breadth of the pen?",
        "8 m", ["16 m", "15 m", "1 m"],
        "The fence covers 1 length + 2 breadths. 30 − 14 = 16 m for the 2 breadths, so 1 breadth = 16 ÷ 2 = 8 m. "
        "(15 m halves the whole 30 m; 1 m comes from fencing all four sides: 30 ÷ 2 − 14.)")
    name, he, his = P.next()
    assert 3 * 2 * (80 + 50) == 780 and 80 * 50 * 3 == 12000
    add("The school field is 80 m long and 50 m wide. During PE, %s runs round the edge of the field 3 times. "
        "How far does %s run?" % (name, he), "780 m", ["260 m", "390 m", "12" + NB + "000 m"],
        "Once round = perimeter = 2 × (80 + 50) = 260 m. 3 times: 3 × 260 = 780 m. "
        "(390 m uses half the perimeter; 12" + NB + "000 uses the area.)")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: fencing, tiles and paths", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    r1 = rect_svg(8, 5, "8 cm", "5 cm", "rectangle 8 cm by 5 cm")
    r2 = rect_svg(8, 6, "8 m", "? m", "rectangle with an area of 48 m² and its breadth missing", inner="Area = 48 m²")
    sq = rect_svg(7, 7, "? cm", "", "square with an area of 49 cm²", inner="49 cm²", max_w=110, max_h=110)
    units, split = make_L(10, 8, 4, 3, False, False)
    lfig = ortho_svg(units, [q_(v, "cm") for v in ortho_sides(units)], "L-shaped figure split into two rectangles", split)
    mod = model_svg([("Length", [(3, UNIT_FILL, "")], ""), ("Breadth", [(1, UNIT_FILL2, "")], "")],
                    "bar model of the length and breadth of a rectangle")
    assert 8 * 5 == 40 and 2 * (8 + 5) == 26 and 48 // 8 == 6 and 30 // 2 - 9 == 6
    assert 10 * 3 + 4 * 5 == 50 and ortho_area(units) == 50 and 32 // 4 == 8
    return (
        "<h2>Area and perimeter</h2>"
        "<p><b>Area</b> is the space inside a figure. It is measured in square units: <b>cm²</b> or <b>m²</b>. "
        "<b>Perimeter</b> is the distance all round the edge. It is a length: <b>cm</b> or <b>m</b>.</p>"
        "<figure class='sn-fig'>" + r1 +
        "<figcaption>Area = length × breadth = 8 × 5 = 40 cm². Perimeter = 2 × (8 + 5) = 26 cm.</figcaption></figure>"
        "<p>For a square, area = side × side and perimeter = 4 × side.</p>"
        "<h2>Find the length or breadth</h2>"
        "<p>Know the <b>area</b>? Divide: missing side = area ÷ the side you know.</p>"
        "<figure class='sn-fig'>" + r2 +
        "<figcaption>8 × ? = 48. 48 ÷ 8 = 6, so the breadth is 6 m.</figcaption></figure>"
        "<p>Know the <b>perimeter</b>? First halve it. Half the perimeter is length + breadth.</p>" +
        ex("Example", "A rectangle has a perimeter of 30 cm. Its length is 9 cm. Find its breadth.",
           "Length + breadth = 30 ÷ 2 = 15 cm. Breadth = 15 − 9 = 6 cm.", "6 cm") +
        "<h2>The side of a square</h2>"
        "<p>From the <b>perimeter</b>: divide by 4. From the <b>area</b>: find the number that times itself gives "
        "the area. Use your multiplication tables.</p>"
        "<figure class='sn-fig'>" + sq +
        "<figcaption>7 × 7 = 49, so each side is 7 cm. (Not 49 ÷ 4.)</figcaption></figure>" +
        ex("Example", "A square has a perimeter of 32 cm. What is its area?",
           "Side = 32 ÷ 4 = 8 cm. Area = 8 × 8 = 64 cm².", "64 cm²") +
        "<h2>Composite figures</h2>"
        "<p>A <b>composite figure</b> is made of rectangles and squares. Find the missing sides first: the sides "
        "going one way add up to the side across from them. For the area, split the figure into rectangles and add. "
        "For the perimeter, add every side of the outline.</p>"
        "<figure class='sn-fig'>" + lfig +
        "<figcaption>Area: 10 × 3 = 30 cm² and 4 × 5 = 20 cm². 30 + 20 = 50 cm². "
        "Perimeter: 10 + 3 + 6 + 5 + 4 + 8 = 36 cm.</figcaption></figure>"
        "<h2>Word problems</h2>"
        "<p>A fence, a border or a ribbon goes round the edge: find the <b>perimeter</b>. "
        "Tiles, carpet, paint or grass cover the inside: find the <b>area</b>.</p>"
        "<figure class='sn-fig'>" + mod +
        "<figcaption>The length is 3 times the breadth: 4 units = length + breadth.</figcaption></figure>" +
        ex("Model method", "The length of a rectangle is 3 times its breadth. Its perimeter is 64 cm. Find its area.",
           "Length + breadth = 64 ÷ 2 = 32 cm = 4 units. 1 unit = 8 cm. Breadth = 8 cm, length = 24 cm. "
           "Area = 24 × 8 = 192 cm².", "192 cm²") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up area and perimeter", "Inside: area, in cm² or m². Round the edge: perimeter, in cm or m"],
            ["Adding only one length and one breadth", "Perimeter = 2 × (length + breadth)"],
            ["30 − 9 = 21 for the breadth", "Halve the perimeter first: 30 ÷ 2 = 15, then 15 − 9 = 6"],
            ["Halving the area to find a side (48 ÷ 2)", "Divide by the side you know: 48 ÷ 8 = 6"],
            ["49 ÷ 4 for the side of a square of area 49 cm²", "Find the number that times itself gives 49: 7"],
            ["Using a whole side for a part in a composite figure", "Work out the part first: 8 − 3 = 5 cm"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 area and perimeter?",
     "a": "Primary 4 students find the length or breadth of a rectangle from its area or perimeter, the side of a "
          "square from its area or perimeter, and the area and perimeter of composite figures made of rectangles "
          "and squares."},
    {"q": "How do I find the breadth of a rectangle from its perimeter?",
     "a": "Halve the perimeter to get length + breadth, then take away the length. For a perimeter of 30 cm and a "
          "length of 9 cm: 30 ÷ 2 = 15, and 15 − 9 = 6 cm."},
    {"q": "What is the most common mistake in area and perimeter?",
     "a": "Mixing up the two: area is the space inside (cm², m²) and perimeter is the distance round (cm, m). "
          "Another is forgetting to halve the perimeter before finding a missing side."},
    {"q": "Is area and perimeter in the MOE syllabus for Primary 4?",
     "a": "Yes. It is part of Area and Volume in Measurement and Geometry. It builds on P3 area and perimeter and "
          "prepares for the area of triangles in P5 and circles in P6, which come up in the PSLE."},
]


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64812)
    P = People(rnd)
    sets = [set_review(rnd, P), set_missing(rnd, P), set_square(rnd, P), set_composite(rnd, P), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "area-and-perimeter", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Area and Perimeter",
        "seo_title": "P4 Area and Perimeter Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Area and perimeter",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 4: Area and Volume",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Finding one dimension of a rectangle given its area/perimeter; side of a square from its "
                         "area/perimeter; area and perimeter of composite figures made of rectangles and squares",
        "meta_desc": "Free P4 area and perimeter practice: missing length or breadth, sides of squares, composite "
                     "figures and word problems. 100 questions with answers.",
        "key_big": "Area = length × breadth. Perimeter = 2 × (length + breadth).",
        "key_sub": "Missing breadth from a perimeter of 30 cm and a length of 9 cm: 30 ÷ 2 = 15, then 15 − 9 = 6 cm.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "[^']*(grid|bar model|path)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
