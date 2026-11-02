# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Perimeter and Area (Australian Curriculum v9.0, AC9M5M02)
  python3 tools/gen_au_maths_y5_perimeter_area.py
Perimeter of regular shapes and rectangles; perimeter of composite rectilinear shapes with missing
sides; area by counting squares and with length × width; area of composite shapes and estimating
irregular areas on a grid; practical problems. Units cm, m, cm², m².
Wrong choices come from real mistakes (adding for area, multiplying for perimeter, missing hidden
sides, cm instead of cm²). Every answer is worked out in code.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
SQ = {"cm": "cm²", "m": "m²"}
NBSP = " "


# ------------------------------------------------------------ helpers
def fmt(n):
    """4536 -> 4536, 10800 -> 10 800 (no-break space, Australian Curriculum style)."""
    return "{:,}".format(n).replace(",", NBSP) if n >= 10000 else str(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.replace("$", "").split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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
    return (len(t) - t.count(NBSP) * 0.3 - t.count(" ") * 0.3) * fs * 0.6


def text(x, y, t, fs=17, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, fs, col, t))


def plus(nums):
    return " + ".join(str(n) for n in nums)


def u2(u):
    return SQ[u]


# ------------------------------------------------------------ labelled shapes (drawn to scale)
FS = 17


def shape_svg(pts, labels, label, extra=(), inner=()):
    """Polygon with horizontal/vertical sides. labels[i] belongs to the side pts[i] -> pts[i+1]
    ('' = no label, a label with '?' is red). Labels sit outside the middle of their side and slide
    along it if they would touch another label or a side. extra = dashed lines (split lines);
    inner = (x, y, text) labels drawn inside the shape. Returns None if no place is found."""
    n = len(pts)
    sa = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))

    def clash(bx, placed):
        for B in placed:
            if bx[0] < B[2] + 16 and B[0] < bx[2] + 16 and bx[1] < B[3] + 8 and B[1] < bx[3] + 8:
                return True
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            if x1 == x2:
                if bx[0] - 3 < x1 < bx[2] + 3 and min(y1, y2) < bx[3] and bx[1] < max(y1, y2):
                    return True
            elif bx[1] - 3 < y1 < bx[3] + 3 and min(x1, x2) < bx[2] and bx[0] < max(x1, x2):
                return True
        return False

    boxes, texts = [], []
    for (x, y, t) in inner:
        hw = tw(t, 15) / 2
        boxes.append((x - hw, y - 10, x + hw, y + 10))
    for i in range(n):
        t = labels[i]
        if not t:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = (dy / L, -dx / L) if sa > 0 else (-dy / L, dx / L)       # outward normal
        hw = tw(t, FS) / 2
        off = 8 + abs(nx) * hw + abs(ny) * 11
        for fr in (0.5, 0.62, 0.38, 0.72, 0.28, 0.8, 0.2):
            mx, my = x1 + dx * fr, y1 + dy * fr
            cx, cy = mx + nx * off, my + ny * off
            bx = (cx - hw, cy - 11, cx + hw, cy + 11)
            if not clash(bx, boxes):
                break
        else:
            return None
        boxes.append(bx)
        texts.append((cx, cy, t))
    xs = [p[0] for p in pts] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for p in pts] + [b[1] for b in boxes] + [b[3] for b in boxes]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.0f,%.0f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for (a, b) in extra:
        s.append("<line x1='%.0f' y1='%.0f' x2='%.0f' y2='%.0f' stroke='%s' stroke-width='2' stroke-dasharray='6 4'/>"
                 % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, INK))
    for (x, y, t) in inner:
        s.append(text(x - ox, y - oy + 5, t, 15, GREEN))
    for cx, cy, t in texts:
        s.append(text(cx - ox, cy - oy + 6, t, FS, RED if "?" in t else INK))
    return svg_wrap(W, H, "".join(s), label)


def rect_svg(L, W, top, left, label, max_w=200, max_h=100):
    k = min(max_w / L, max_h / W, 26)
    pts = [(0, 0), (L * k, 0), (L * k, W * k), (0, W * k)]
    s = shape_svg(pts, [top, "", "", left], label)
    assert s, (L, W)
    return s


def l_sides(Wt, Ht, cw, ch):
    """Sides of an L (Wt by Ht with a cw by ch corner cut), in drawing order."""
    return [Wt - cw, ch, cw, Ht - ch, Wt, Ht]


def l_pts(Wt, Ht, cw, ch, corner, k):
    p = [(0, 0), (Wt - cw, 0), (Wt - cw, ch), (Wt, ch), (Wt, Ht), (0, Ht)]
    if corner in ("tl", "bl"):
        p = [(Wt - x, y) for x, y in p]
    if corner in ("br", "bl"):
        p = [(x, Ht - y) for x, y in p]
    return [(x * k, y * k) for x, y in p]


def l_split(Wt, Ht, cw, ch, corner, k):
    """Dashed line that splits the L into (Wt − cw) × ch and Wt × (Ht − ch)."""
    a, b = (0, ch), (Wt - cw, ch)
    pts = [a, b]
    if corner in ("tl", "bl"):
        pts = [(Wt - x, y) for x, y in pts]
    if corner in ("br", "bl"):
        pts = [(x, Ht - y) for x, y in pts]
    return [tuple((x * k, y * k) for x, y in pts)]


def l_svg(Wt, Ht, cw, ch, corner, labels, label="rectilinear L-shape with side lengths", split=False):
    k = min(240 / Wt, 130 / Ht)
    extra = l_split(Wt, Ht, cw, ch, corner, k) if split else ()
    return shape_svg(l_pts(Wt, Ht, cw, ch, corner, k), labels, label, extra)


def step_sides(W, H, x1, x2, y1, y2):
    """Staircase: (0,0)->(x1,0)->(x1,y1)->(x2,y1)->(x2,y2)->(W,y2)->(W,H)->(0,H)."""
    return [x1, y1, x2 - x1, y2 - y1, W - x2, H - y2, W, H]


def step_svg(W, H, x1, x2, y1, y2, labels, flip, label="rectilinear step shape with side lengths"):
    k = min(300 / W, 170 / H)
    p = [(0, 0), (x1, 0), (x1, y1), (x2, y1), (x2, y2), (W, y2), (W, H), (0, H)]
    if flip:
        p = [(W - x, y) for x, y in p]
    return shape_svg([(x * k, y * k) for x, y in p], labels, label)


def u_sides(W, H, a, n, d):
    """U-shape: W by H rectangle with an n by d gap cut from the top, a from the left."""
    return [a, d, n, d, W - a - n, H, W, H]


def u_svg(W, H, a, n, d, labels, flip, label="rectilinear U-shape with side lengths"):
    k = min(300 / W, 160 / H)
    p = [(0, 0), (a, 0), (a, d), (a + n, d), (a + n, 0), (W, 0), (W, H), (0, H)]
    if flip:
        p = [(x, H - y) for x, y in p]
    return shape_svg([(x * k, y * k) for x, y in p], labels, label)


# ------------------------------------------------------------ irregular shapes on a cm grid
def blob_r(params, th):
    R, sx, sy, waves = params
    r = 1 + sum(a * math.sin(k * th + ph) for a, k, ph in waves)
    return R * r


def inside_blob(params, cx, cy, x, y):
    R, sx, sy, waves = params
    dx, dy = (x - cx) / sx, (y - cy) / sy
    return math.hypot(dx, dy) < blob_r(params, math.atan2(dy, dx))


def blob_poly(params, cx, cy, n=180):
    R, sx, sy, waves = params
    out = []
    for i in range(n):
        th = 2 * math.pi * i / n
        r = blob_r(params, th)
        out.append((cx + sx * r * math.cos(th), cy + sy * r * math.sin(th)))
    return out


def coverage(params, cx, cy, cols, rows, S):
    """Fraction of each grid square covered by the blob (numpy array rows x cols)."""
    R, sx, sy, waves = params
    xs = (np.arange(cols * S) + 0.5) / S
    ys = (np.arange(rows * S) + 0.5) / S
    X, Y = np.meshgrid(xs, ys)
    dx, dy = (X - cx) / sx, (Y - cy) / sy
    th = np.arctan2(dy, dx)
    r = R * (1 + sum(a * np.sin(k * th + ph) for a, k, ph in waves))
    ins = (np.hypot(dx, dy) < r).astype(float)
    return ins.reshape(rows, S, cols, S).mean(axis=(1, 3))


def blob_counts(params, cx, cy, cols, rows, S=12):
    """(whole squares, half-or-more part squares, less-than-half part squares, coverage sum).
    Returns None when a square is close to half covered (hard to judge by eye)."""
    for s in (S, 40):                       # quick check, then a fine check
        fr = coverage(params, cx, cy, cols, rows, s)
        if ((fr > 0.33) & (fr < 0.67)).any():
            return None
    whole = int((fr == 1).sum())
    more = int(((fr >= 0.67) & (fr < 1)).sum())
    less = int(((fr > 0) & (fr <= 0.33)).sum())
    return whole, more, less, float(fr.sum())


def make_blob(rnd, used, nmin=10, nmax=26):
    for _ in range(40000):
        R = rnd.uniform(1.9, 3.0)
        sx, sy = rnd.uniform(1.0, 1.5), rnd.uniform(0.8, 1.05)
        waves = [(rnd.uniform(0.06, 0.16), 2, rnd.uniform(0, 6.28)), (rnd.uniform(0.04, 0.12), 3, rnd.uniform(0, 6.28)),
                 (rnd.uniform(0.0, 0.06), 5, rnd.uniform(0, 6.28))]
        params = (R, sx, sy, waves)
        ext = max(blob_r(params, 2 * math.pi * i / 90) for i in range(90))
        cols = int(math.ceil(2 * ext * sx)) + 2
        rows = int(math.ceil(2 * ext * sy)) + 2
        if cols > 10 or rows > 7:
            continue
        cx = cols / 2 + rnd.uniform(-0.3, 0.3)
        cy = rows / 2 + rnd.uniform(-0.3, 0.3)
        poly = blob_poly(params, cx, cy)
        if min(x for x, y in poly) < 0.5 or max(x for x, y in poly) > cols - 0.5:
            continue
        if min(y for x, y in poly) < 0.5 or max(y for x, y in poly) > rows - 0.5:
            continue
        res = blob_counts(params, cx, cy, cols, rows)
        if not res:
            continue
        whole, more, less, tot = res
        N = whole + more
        if not (nmin <= N <= nmax) or more < 3 or less < 3 or abs(tot - N) > 1.5:
            continue
        key = (whole, more, less)
        if key in used:
            continue
        used.add(key)
        return poly, cols, rows, whole, more, less
    raise RuntimeError("no blob")


def blob_svg(poly, cols, rows, label, cell=22):
    m = 6
    W, H = cols * cell + 2 * m, rows * cell + 2 * m
    pts = " ".join("%.1f,%.1f" % (m + x * cell, m + y * cell) for x, y in poly)
    g = ["<polygon points='%s' fill='%s'/>" % (pts, FILL)]
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m + i * cell, m, m + i * cell, m + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m, m + j * cell, m + cols * cell, m + j * cell, GRIDC))
    g.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (pts, GREEN))
    return svg_wrap(W, H, "".join(g), label)


# ------------------------------------------------------------ shape pickers
def pick_l(rnd, used, lo=(12, 8), hi=(30, 20)):
    while True:
        Wt, Ht = rnd.randint(lo[0], hi[0]), rnd.randint(lo[1], hi[1])
        if Wt <= Ht or Wt / Ht > 2:
            continue
        cw = rnd.randint(int(math.ceil(Wt * 0.35)), int(Wt * 0.6))
        ch = rnd.randint(int(math.ceil(Ht * 0.35)), int(Ht * 0.6))
        if cw == Wt - cw or ch == Ht - ch or cw == ch or (Wt, Ht, cw, ch) in used:
            continue
        if len(set(l_sides(Wt, Ht, cw, ch))) < 6:
            continue
        used.add((Wt, Ht, cw, ch))
        return Wt, Ht, cw, ch


def l_figure(rnd, used, labeller, lo=(12, 8), hi=(30, 20), label="rectilinear L-shape with side lengths", corner=None):
    for _ in range(300):
        Wt, Ht, cw, ch = pick_l(rnd, used, lo, hi)
        cn = corner or rnd.choice(["tr", "tl", "br", "bl"])
        sides = l_sides(Wt, Ht, cw, ch)
        svg = l_svg(Wt, Ht, cw, ch, cn, labeller(sides), label)
        if svg:
            return Wt, Ht, cw, ch, sides, svg
    raise RuntimeError("no L fits")


def pick_step(rnd, used):
    while True:
        W, H = rnd.randint(12, 24), rnd.randint(8, 15)
        if W / H > 2.2 or W <= H:
            continue
        x1 = rnd.randint(3, W - 7)
        x2 = rnd.randint(x1 + 3, W - 3)
        y1 = rnd.randint(2, H - 5)
        y2 = rnd.randint(y1 + 2, H - 3)
        sides = step_sides(W, H, x1, x2, y1, y2)
        if len(set(sides)) < 7 or (W, H, x1, x2, y1, y2) in used:
            continue
        return W, H, x1, x2, y1, y2


def step_figure(rnd, used, labeller, flip):
    for _ in range(5000):
        W, H, x1, x2, y1, y2 = pick_step(rnd, used)
        sides = step_sides(W, H, x1, x2, y1, y2)
        svg = step_svg(W, H, x1, x2, y1, y2, labeller(sides), flip)
        if svg:
            used.add((W, H, x1, x2, y1, y2))
            return W, H, x1, x2, y1, y2, sides, svg
    raise RuntimeError("no step fits")


def pick_u(rnd, used):
    while True:
        W, H = rnd.randint(14, 30), rnd.randint(8, 16)
        if W <= H or W / H > 2.2:
            continue
        a = rnd.randint(int(math.ceil(W * 0.22)), int(W * 0.35))
        n = rnd.randint(int(math.ceil(W * 0.35)), int(W * 0.5))
        r = W - a - n
        d = rnd.randint(int(math.ceil(H * 0.35)), int(H * 0.65))
        if r < W * 0.2 or len({a, n, r, d, W, H}) < 6 or (W, H, a, n, d) in used:
            continue
        used.add((W, H, a, n, d))
        return W, H, a, n, d


def u_figure(rnd, used, labeller, flip):
    for _ in range(3000):
        W, H, a, n, d = pick_u(rnd, used)
        sides = u_sides(W, H, a, n, d)
        svg = u_svg(W, H, a, n, d, labeller(sides), flip)
        if svg:
            return W, H, a, n, d, sides, svg
    raise RuntimeError("no U fits")

# ------------------------------------------------------------ regular shapes
POLY = {3: "equilateral triangle", 4: "square", 5: "regular pentagon", 6: "regular hexagon", 8: "regular octagon"}


def reg_svg(n, lab, label, side_px=None):
    """Regular polygon with its bottom side horizontal, a tick on every side (all equal) and a
    label under the bottom side."""
    side_px = side_px or {3: 110, 4: 84, 5: 70, 6: 54, 8: 40}[n]
    R = side_px / (2 * math.sin(math.pi / n))
    pts = [(R * math.cos(math.pi / 2 + math.pi / n + 2 * math.pi * i / n),
            R * math.sin(math.pi / 2 + math.pi / n + 2 * math.pi * i / n)) for i in range(n)]
    ticks = []
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        L = math.hypot(x2 - x1, y2 - y1)
        nx, ny = (y2 - y1) / L * 6, -(x2 - x1) / L * 6
        ticks.append((mx - nx, my - ny, mx + nx, my + ny))
    bottom = max(y for x, y in pts)
    lw = tw(lab, FS)
    xs = [p[0] for p in pts] + [-lw / 2, lw / 2]
    ys = [p[1] for p in pts] + [bottom + 30]
    pad = 6
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for a, b, c, d in ticks:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                 % (a - ox, b - oy, c - ox, d - oy, INK))
    s.append(text(-ox, bottom + 24 - oy, lab, FS, RED if "?" in lab else INK))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ shapes on a squared grid (count the squares)
def grid_svg(cells, cols, rows, label, cell=22):
    """cells = set of (col, row) that are shaded; grid of cols × rows squares."""
    m = 4
    W, H = cols * cell + 2 * m, rows * cell + 2 * m
    g = []
    for (c, r) in sorted(cells):
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (m + c * cell, m + r * cell, cell, cell, FILL))
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m + i * cell, m, m + i * cell, m + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m, m + j * cell, m + cols * cell, m + j * cell, GRIDC))
    # outline: every edge of a shaded cell that borders an unshaded cell
    for (c, r) in sorted(cells):
        x, y = m + c * cell, m + r * cell
        for (dc, dr, x1, y1, x2, y2) in [(0, -1, 0, 0, 1, 0), (0, 1, 0, 1, 1, 1), (-1, 0, 0, 0, 0, 1), (1, 0, 1, 0, 1, 1)]:
            if (c + dc, r + dr) not in cells:
                g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                         % (x + x1 * cell, y + y1 * cell, x + x2 * cell, y + y2 * cell, GREEN))
    return svg_wrap(W, H, "".join(g), label)


def cell_perimeter(cells):
    return sum(1 for (c, r) in cells for d in [(0, 1), (0, -1), (1, 0), (-1, 0)] if (c + d[0], r + d[1]) not in cells)


# ------------------------------------------------------------ set 1: perimeter of regular shapes and rectangles
def set_regular(rnd):
    its = []

    def side_q(n, s, u, k):
        name = POLY[n]
        P = n * s
        q = (fig(reg_svg(n, "%d %s" % (s, u), "%s with sides of %d %s" % (name, s, u))) +
             "This is %s %s. Every side is %d %s. What is its perimeter?" % ("an" if name[0] in "aeiou" else "a", name, s, u))
        e = ("%s has %d equal sides. Perimeter = %d × %d = %d %s." % (cap(name if n != 4 else "a square"),
                                                                      n, n, s, P, u))
        if n == 4:
            e = "A square has 4 equal sides. Perimeter = 4 × %d = %d %s. (%d × %d = %d would be the area.)" % (s, P, u, s, s, s * s)
            cands = ["%d %s" % (2 * s, u), "%d %s" % (s * s, u), "%d %s" % (s, u), "%d %s" % (3 * s, u)]
        elif n == 3:
            e = "An equilateral triangle has 3 equal sides. Perimeter = 3 × %d = %d %s." % (s, P, u)
            cands = ["%d %s" % (4 * s, u), "%d %s" % (s, u), "%d %s" % (2 * s, u)]
        elif n == 6:
            e = "A regular hexagon has 6 equal sides. Perimeter = 6 × %d = %d %s." % (s, P, u)
            cands = ["%d %s" % (4 * s, u), "%d %s" % (5 * s, u), "%d %s" % (s, u)]
        elif n == 5:
            e = "A regular pentagon has 5 equal sides. Perimeter = 5 × %d = %d %s." % (s, P, u)
            cands = ["%d %s" % (4 * s, u), "%d %s" % (6 * s, u), "%d %s" % (s, u)]
        else:
            e = "A regular octagon has 8 equal sides. Perimeter = 8 × %d = %d %s." % (s, P, u)
            cands = ["%d %s" % (6 * s, u), "%d %s" % (4 * s, u), "%d %s" % (s, u)]
        r = k % 3
        cands = cands[r:3] + cands[:r] + cands[3:]
        return mcq(q, "%d %s" % (P, u), cands, e, rnd)

    k = 0
    for n, s, u in [(4, 6, "cm"), (4, 9, "m"), (4, 13, "cm"), (3, 8, "cm"), (3, 12, "m"), (3, 25, "cm"),
                    (6, 5, "cm"), (6, 7, "m"), (6, 15, "cm"), (5, 9, "cm"), (8, 6, "m")]:
        its.append(side_q(n, s, u, k))
        k += 1
    # rectangles
    for i, (L, W, u) in enumerate([(9, 4, "cm"), (14, 6, "m"), (12, 7, "cm"), (25, 18, "m"), (40, 15, "cm")]):
        P = 2 * (L + W)
        if i < 2:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
                 "What is the perimeter of this rectangle?")
        else:
            q = "A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u)
        e = ("Add all 4 sides: %d + %d + %d + %d = %d %s. Or 2 × (%d + %d) = %d %s."
             % (L, W, L, W, P, u, L, W, P, u))
        cands = ["%d %s" % (L + W, u), "%d %s" % (L * W, u), "%d %s" % (2 * L + W, u)]
        r = i % 3
        cands = cands[r:] + cands[:r]
        its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    # missing side from the perimeter
    its.append(mcq(fig(reg_svg(4, "? cm", "square with a missing side length")) +
                   "The perimeter of this square is 36 cm. How long is each side?", "9 cm",
                   ["18 cm", "6 cm", "12 cm"],
                   "A square has 4 equal sides. 36 ÷ 4 = 9 cm. Check: 4 × 9 = 36. (6 cm comes from 6 × 6 = 36, "
                   "which is area thinking.)", rnd))
    its.append(mcq("An equilateral triangle has a perimeter of 48 cm. How long is each side?", "16 cm",
                   ["12 cm", "24 cm", "144 cm"],
                   "An equilateral triangle has 3 equal sides. 48 ÷ 3 = 16 cm. Check: 3 × 16 = 48.", rnd))
    its.append(mcq("A regular hexagon has a perimeter of 72 m. How long is each side?", "12 m",
                   ["18 m", "36 m", "432 m"],
                   "A regular hexagon has 6 equal sides. 72 ÷ 6 = 12 m. Check: 6 × 12 = 72.", rnd))
    its.append(mcq(fig(rect_svg(9, 6, "9 m", "? m", "rectangle with a missing side length")) +
                   "The perimeter of this rectangle is 30 m. How wide is it?", "6 m",
                   ["21 m", "12 m", "15 m"],
                   "The two long sides make 9 + 9 = 18 m. 30 − 18 = 12 m for the two short sides, "
                   "so each one is 12 ÷ 2 = 6 m.", rnd))
    assert len(its) == 20
    return {"title": "Perimeter of regular shapes and rectangles", "items": its}


# ------------------------------------------------------------ set 2: perimeter of composite rectilinear shapes
def set_perimeter(rnd, used):
    its = []
    for i in range(4):
        u = ["cm", "m"][i % 2]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lambda s, u=u: ["%d %s" % (v, u) for v in s])
        P = sum(sides)
        assert P == 2 * (Wt + Ht)
        e = ("Add all 6 sides: %s = %d %s. Do not skip the two short sides at the inside corner."
             % (plus(sides), P, u))
        cands = ["%d %s" % (P - cw - ch, u), "%d %s" % (Wt + Ht, u), "%d %s" % (P, u2(u)), "%d %s" % (P - sides[1], u)]
        its.append(mcq(fig(svg) + "What is the perimeter of this shape?", "%d %s" % (P, u), cands, e, rnd))
    for i in range(6):
        u = ["m", "cm"][i % 2]
        hide = [(0, 3), (1, 2)][i % 2]

        def lab(s, hide=hide, u=u):
            return ["" if j in hide else "%d %s" % (v, u) for j, v in enumerate(s)]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lab)
        P = sum(sides)
        shown = sum(v for j, v in enumerate(sides) if j not in hide)
        if hide == (0, 3):
            miss = "%d − %d = %d %s and %d − %d = %d %s" % (Wt, cw, Wt - cw, u, Ht, ch, Ht - ch, u)
        else:
            miss = "%d − %d = %d %s and %d − %d = %d %s" % (Ht, Ht - ch, ch, u, Wt, Wt - cw, cw, u)
        e = ("First find the two missing sides: %s. Then add all 6 sides: %s = %d %s."
             % (miss, plus(sides), P, u))
        cands = ["%d %s" % (shown, u), "%d %s" % (shown + sides[hide[0]], u), "%d %s" % (shown + sides[hide[1]], u),
                 "%d %s" % (Wt + Ht, u)]
        if i % 2:
            cands = [cands[0], cands[2], cands[1], cands[3]]
        q = fig(svg) + "Two sides are not labelled. What is the perimeter of the shape?"
        its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    for i in range(5):
        u = ["cm", "m"][i % 2]
        W, H, x1, x2, y1, y2, sides, svg = step_figure(
            rnd, used, lambda s, u=u: ["" if j >= 6 else "%d %s" % (v, u) for j, v in enumerate(s)], i % 2 == 1)
        P = sum(sides)
        shown = sum(sides[:6])
        e = ("The long side across = %s = %d %s. The long side going up = %s = %d %s. "
             "Add all 8 sides: %s = %d %s."
             % (plus([sides[0], sides[2], sides[4]]), W, u, plus([sides[1], sides[3], sides[5]]), H, u,
                plus(sides), P, u))
        cands = ["%d %s" % (shown, u), "%d %s" % (shown + W, u), "%d %s" % (W + H, u), "%d %s" % (P, u2(u))]
        q = fig(svg) + "Two sides are not labelled. What is the perimeter of the shape?"
        its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    for i in range(5):
        u = ["m", "cm"][i % 2]
        W, H, a, n, d, sides, svg = u_figure(
            rnd, used, lambda s, u=u: ["" if j in (3, 4) else "%d %s" % (v, u) for j, v in enumerate(s)], i % 2 == 1)
        P = sum(sides)
        assert P == 2 * (W + H) + 2 * d
        r = W - a - n
        e = ("Missing sides: the two sides of the gap are the same, %d %s, and %d − %d − %d = %d %s. "
             "Add all 8 sides: %s = %d %s. Do not forget the sides inside the gap."
             % (d, u, W, a, n, r, u, plus(sides), P, u))
        cands = ["%d %s" % (2 * (W + H), u), "%d %s" % (P - d, u), "%d %s" % (P - d - r, u), "%d %s" % (P - r, u)]
        q = fig(svg) + "Two sides are not labelled. What is the perimeter of the shape?"
        its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    assert len(its) == 20
    return {"title": "Perimeter of composite shapes with missing sides", "items": its}


# ------------------------------------------------------------ set 3: area by counting squares and length × width
def set_rect_area(rnd):
    its = []
    # rectangles on a grid
    for k, (L, W) in enumerate([(5, 3), (7, 2), (6, 4), (8, 3)]):
        A, P = L * W, 2 * (L + W)
        assert A != P
        cells = {(c, r) for c in range(1, L + 1) for r in range(1, W + 1)}
        svg = grid_svg(cells, L + 2, W + 2, "rectangle on a squared grid")
        q = fig(svg) + "Each square is 1 cm². What is the area of the shaded rectangle?"
        e = ("Count the squares: %d rows of %d. %d × %d = %d cm². %d cm is the distance around it (the perimeter)."
             % (W, L, W, L, A, P))
        cands = ["%d cm²" % P, "%d cm²" % (L + W), "%d cm" % A]
        r = k % 3
        cands = cands[r:] + cands[:r]
        its.append(mcq(q, "%d cm²" % A, cands, e, rnd))
    # rectilinear shapes on a grid
    for k, (Wt, Ht, cw, ch, corner) in enumerate([(6, 4, 3, 2, "tr"), (7, 5, 3, 2, "bl"), (5, 5, 2, 3, "tl"),
                                                   (8, 4, 3, 2, "br")]):
        cells = set()
        for c in range(Wt):
            for r in range(Ht):
                cc = c if corner in ("tr", "br") else Wt - 1 - c
                rr = r if corner in ("tr", "tl") else Ht - 1 - r
                if not (cc >= Wt - cw and rr < ch):
                    cells.add((c + 1, r + 1))
        A = len(cells)
        assert A == Wt * Ht - cw * ch
        P = cell_perimeter(cells)
        svg = grid_svg(cells, Wt + 2, Ht + 2, "rectilinear shape on a squared grid")
        q = fig(svg) + "Each square is 1 cm². What is the area of the shaded shape?"
        e = ("Count the whole squares inside the shape: %d. Or: %d × %d = %d for the whole rectangle, "
             "take away the empty corner %d × %d = %d: %d − %d = %d cm²."
             % (A, Wt, Ht, Wt * Ht, cw, ch, cw * ch, Wt * Ht, cw * ch, A))
        cands = ["%d cm²" % (Wt * Ht), "%d cm²" % P, "%d cm" % A]
        r = k % 3
        cands = cands[r:] + cands[:r]
        its.append(mcq(q, "%d cm²" % A, cands, e, rnd))
    # rectangles with labelled sides
    for i, (L, W, u) in enumerate([(8, 5, "cm"), (12, 4, "m"), (9, 7, "cm"), (15, 6, "m"), (11, 8, "cm")]):
        A, P = L * W, 2 * (L + W)
        assert A != P
        if i < 2:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
                 "What is the area of this rectangle?")
        else:
            q = "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
        e = ("Area of a rectangle = length × width: %d × %d = %d %s. "
             "%d %s would be the perimeter." % (L, W, A, u2(u), P, u))
        cands = ["%d %s" % (P, u2(u)), "%d %s" % (L + W, u2(u)), "%d %s" % (A, u)]
        r = i % 3
        cands = cands[r:] + cands[:r]
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    # squares
    for k, (s, u) in enumerate([(7, "cm"), (12, "m"), (15, "cm")]):
        A = s * s
        if k < 1:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u), max_h=95)) +
                 "This is a square. What is its area?")
        else:
            q = "A square has sides of %d %s. What is its area?" % (s, u)
        e = ("All the sides of a square are the same, so length and width are both %d %s: %d × %d = %d %s."
             % (s, u, s, s, A, u2(u)))
        cands = ["%d %s" % (4 * s, u2(u)), "%d %s" % (2 * s, u2(u)), "%d %s" % (A, u)]
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    # missing side from the area
    for k, (A, L, u) in enumerate([(48, 8, "cm"), (63, 9, "m"), (84, 12, "cm"), (90, 15, "m")]):
        w = A // L
        assert w * L == A and A // 2 - L > 0 and A // 2 - L != w
        if k < 2:
            q = (fig(rect_svg(L, w, "%d %s" % (L, u), "? %s" % u, "rectangle with one side missing")) +
                 "The area of this rectangle is %d %s. What is the length of the side marked ?" % (A, u2(u)))
        else:
            q = "A rectangle has an area of %d %s. It is %d %s long. How wide is it?" % (A, u2(u), L, u)
        e = ("Length × width = area, so width = area ÷ length: %d ÷ %d = %d %s. Check: %d × %d = %d %s."
             % (A, L, w, u, L, w, A, u2(u)))
        cands = ["%d %s" % (A - L, u), "%d %s" % (A // 2 - L, u), "%s %s" % (fmt(A * L), u)]
        its.append(mcq(q, "%d %s" % (w, u), cands, e, rnd))
    assert len(its) == 20
    return {"title": "Area: count squares or use length × width", "items": its}


# ------------------------------------------------------------ set 4: composite areas and estimating irregular areas
BLOB_THINGS = [("leaf", "cm"), ("puddle", "cm"), ("ink blot", "cm"), ("dam", "m"), ("handprint", "cm"),
               ("lake", "m")]


def blob_q(rnd, used, thing, u, nmin=10, nmax=26):
    poly, cols, rows, whole, more, less = make_blob(rnd, used, nmin, nmax)
    N = whole + more
    T = whole + more + less
    svg = blob_svg(poly, cols, rows, "irregular shape of a %s on a squared grid" % thing)
    return svg, whole, more, less, N, T, cols, rows


def set_composite(rnd, used, used_blobs):
    its = []
    for i in range(5):
        u = ["cm", "m"][i % 2]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lambda s, u=u: ["%d %s" % (v, u) for v in s],
                                              lo=(8, 5), hi=(20, 14))
        a1, a2 = (Wt - cw) * ch, Wt * (Ht - ch)
        A = a1 + a2
        assert A == Wt * Ht - cw * ch
        dbl = (Wt - cw) * Ht + Wt * (Ht - ch)
        e = ("Split it into two rectangles: %d × %d = %d and %d × %d = %d. Add them: %d + %d = %d %s. "
             "(Or %d × %d − %d × %d = %d %s.)"
             % (Wt - cw, ch, a1, Wt, Ht - ch, a2, a1, a2, A, u2(u), Wt, Ht, cw, ch, A, u2(u)))
        cands = ["%d %s" % (Wt * Ht, u2(u)), "%d %s" % (dbl, u2(u)), "%d %s" % (sum(sides), u2(u)), "%d %s" % (A, u)]
        r = i % 3
        cands = cands[r:3] + cands[:r] + cands[3:]
        its.append(mcq(fig(svg) + "What is the area of this shape?", "%d %s" % (A, u2(u)), cands, e, rnd))
    for i in range(3):
        u = ["m", "cm"][i % 2]

        def lab(s, u=u):
            return ["" if j in (0, 3) else "%d %s" % (v, u) for j, v in enumerate(s)]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lab, lo=(8, 5), hi=(20, 14))
        a1, a2 = (Wt - cw) * ch, Wt * (Ht - ch)
        A = a1 + a2
        e = ("Missing sides: %d − %d = %d %s and %d − %d = %d %s. Split into two rectangles: "
             "%d × %d = %d and %d × %d = %d. Area = %d + %d = %d %s."
             % (Wt, cw, Wt - cw, u, Ht, ch, Ht - ch, u, Wt - cw, ch, a1, Wt, Ht - ch, a2, a1, a2, A, u2(u)))
        wrong1 = a1 + Wt * Ht
        cands = ["%d %s" % (Wt * Ht, u2(u)), "%d %s" % (wrong1, u2(u)), "%d %s" % (Wt * Ht - (Wt - cw) * (Ht - ch), u2(u)),
                 "%d %s" % (sum(sides), u2(u))]
        q = fig(svg) + "Two sides are not labelled. What is the area of the shape?"
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    for i in range(2):
        u = ["cm", "m"][i % 2]
        W, H, a, n, d, sides, svg = u_figure(
            rnd, used, lambda s, u=u: ["" if j == 3 else "%d %s" % (v, u) for j, v in enumerate(s)], i % 2 == 1)
        A = W * H - n * d
        P = sum(sides)
        e = ("Think of the whole rectangle and take away the gap: %d × %d = %d, gap %d × %d = %d. "
             "%d − %d = %d %s." % (W, H, W * H, n, d, n * d, W * H, n * d, A, u2(u)))
        cands = ["%d %s" % (W * H, u2(u)), "%d %s" % (W * H - 2 * n * d, u2(u)), "%d %s" % (P, u2(u)),
                 "%d %s" % (W * H - n * H, u2(u))]
        q = fig(svg) + "What is the area of this shape?"
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    for i in range(2):
        u = ["m", "cm"][i % 2]
        W, H, x1, x2, y1, y2, sides, svg = step_figure(
            rnd, used, lambda s, u=u: ["%d %s" % (v, u) for v in s], i % 2 == 0)
        parts = [(x1, H), (x2 - x1, H - y1), (W - x2, H - y2)]
        ar = [p * q for p, q in parts]
        A = sum(ar)
        e = ("Split it into three rectangles standing side by side: %d × %d = %d, %d × (%d − %d) = %d × %d = %d, "
             "%d × (%d − %d) = %d × %d = %d. Add: %s = %d %s."
             % (x1, H, ar[0], x2 - x1, H, y1, x2 - x1, H - y1, ar[1], W - x2, H, y2, W - x2, H - y2, ar[2],
                plus(ar), A, u2(u)))
        cands = ["%d %s" % (W * H, u2(u)), "%d %s" % (A - ar[2], u2(u)), "%d %s" % (sum(sides), u2(u)),
                 "%d %s" % (x1 * H + (x2 - x1) * (y2 - y1) + (W - x2) * (H - y2), u2(u))]
        q = fig(svg) + "What is the area of this shape?"
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    # estimating irregular areas on a grid
    for k, (thing, u) in enumerate(BLOB_THINGS):
        svg, whole, more, less, N, T, cols, rows = blob_q(rnd, used_blobs, thing, u)
        q = (fig(svg) + "Each square is 1 %s. Estimate the area of the %s. Count whole squares and squares that "
             "are half or more covered." % (u2(u), thing))
        e = ("Whole squares: %d. Squares half or more covered: %d. Estimate: %d + %d = %d %s. "
             "Squares less than half covered (%d) are not counted." % (whole, more, whole, more, N, u2(u), less))
        cands = ["%d %s" % (whole, u2(u)), "%d %s" % (T, u2(u)), "%d %s" % (whole + less, u2(u)), "%d %s" % (N, u)]
        r = k % 3
        cands = cands[r:3] + cands[:r] + cands[3:]
        its.append(mcq(q, "%d %s" % (N, u2(u)), cands, e, rnd))
    w, m, l = 21, 8, 7
    its.append(mcq("A map of an island is drawn on a grid. Each square is 1 cm². The island covers %d whole squares "
                   "and %d squares that are half or more covered. %d more squares are less than half covered. "
                   "Estimate its area." % (w, m, l), "%d cm²" % (w + m),
                   ["%d cm²" % w, "%d cm²" % (w + m + l), "%d cm²" % (m + l)],
                   "Count whole squares and squares half or more covered: %d + %d = %d cm². "
                   "Leave out the %d squares that are less than half covered." % (w, m, w + m, l), rnd))
    its.append(mcq("You estimate the area of an irregular shape on a squared grid. Which squares do you count?",
                   "Whole and half or more covered",
                   ["Only whole squares", "Every square it touches", "Only part squares"],
                   "Count every whole square, and count a square as 1 if half or more of it is covered. "
                   "Leave out squares that are less than half covered. The parts you count and leave out "
                   "roughly balance.", rnd))
    assert len(its) == 20
    return {"title": "Area of composite shapes and estimating irregular areas", "items": its}


# ------------------------------------------------------------ set 5: practical problems
def set_story(rnd, P, used, used_blobs):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    n, he, his = P.next()
    L, W = 18, 12
    add("%s’s family is putting a new fence around their rectangular backyard. It is %d m long and %d m wide. "
        "How many metres of fence do they need?" % (n, L, W), "%d m" % (2 * (L + W)),
        ["%d m" % (L * W), "%d m" % (L + W), "%d m" % (2 * L + W)],
        "The fence goes along all 4 sides: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)))
    L, W, g = 25, 16, 3
    Pm = 2 * (L + W)
    add("A rectangular paddock is %d m long and %d m wide. A fence goes all the way around, except for a gate %d m "
        "wide. How much fence is needed?" % (L, W, g), "%d m" % (Pm - g),
        ["%d m" % Pm, "%d m" % (L + W - g), "%d m" % (Pm + g)],
        "Perimeter: %d + %d + %d + %d = %d m. No fence across the gate: %d − %d = %d m."
        % (L, W, L, W, Pm, Pm, g, Pm - g))
    add("The reading corner in a classroom is 4 m long and 3 m wide. It will be covered with carpet tiles. "
        "Four tiles cover 1 m². How many tiles are needed?", "48 tiles", ["12 tiles", "56 tiles", "3 tiles"],
        "Area: 4 × 3 = 12 m². Each square metre needs 4 tiles: 12 × 4 = 48 tiles.")
    add("A school office floor is 6 m by 5 m. Each box of carpet tiles covers 4 m². How many boxes are needed to "
        "cover the floor?", "8 boxes", ["7 boxes", "30 boxes", "22 boxes"],
        "Area: 6 × 5 = 30 m². 30 ÷ 4 = 7 remainder 2. 7 boxes cover only 28 m², so 8 boxes are needed.")
    n, he, his = P.next()
    add("%s is building a raised garden bed 3 m long and 2 m wide. What area of soil can %s plant in?" % (n, he),
        "6 m²", ["10 m²", "5 m²", "6 m"],
        "Planting space is area: 3 × 2 = 6 m². (3 + 2 + 3 + 2 = 10 m is the edge of the bed.)")
    Pm, L = 34, 11
    W = Pm // 2 - L
    add("A rectangular vegetable garden bed has timber edging all the way around. The edging is %d m long. "
        "The bed is %d m long. How wide is it?" % (Pm, L), "%d m" % W,
        ["%d m" % (Pm - L), "%d m" % (Pm - 2 * L), "%d m" % (Pm // 2)],
        "The two long sides make 2 × %d = %d m. %d − %d = %d m for the two short sides, so each is %d ÷ 2 = %d m."
        % (L, 2 * L, Pm, 2 * L, Pm - 2 * L, Pm - 2 * L, W))
    add("A cricket pitch is about 20 m long and 3 m wide. Estimate its area.", "60 m²",
        ["46 m²", "23 m²", "60 m"],
        "Area = length × width: 20 × 3 = 60 m². 46 m is the distance around it.")
    L, W = 28, 15
    add("A basketball court is %d m long and %d m wide. What is its area?" % (L, W), "%d m²" % (L * W),
        ["%d m²" % (2 * (L + W)), "%d m²" % (L + W), "%d m" % (L * W)],
        "Length × width: %d × %d = %d m². Tip: 28 × 10 = 280 and 28 × 5 = 140, 280 + 140 = 420." % (L, W, L * W))
    L, W, c = 9, 6, 12
    add("A front lawn is %d m long and %d m wide. New turf costs $%d per square metre. How much does turf for the "
        "whole lawn cost?" % (L, W, c), "$%d" % (L * W * c),
        ["$%d" % (2 * (L + W) * c), "$%d" % ((L + W) * c), "$%d" % (L * W)],
        "Area: %d × %d = %d m². Cost: %d × $%d = $%d." % (L, W, L * W, L * W, c, L * W * c))
    for _ in range(300):
        Wt, Ht, cw, ch = pick_l(rnd, used, (7, 5), (10, 8))
        sides = l_sides(Wt, Ht, cw, ch)
        if (Wt - cw) * Ht == Wt * ch:
            continue
        svg = l_svg(Wt, Ht, cw, ch, "tr", ["%d m" % v for v in sides], "plan of a rectilinear L-shaped room")
        if svg:
            break
    a1, a2 = (Wt - cw) * ch, Wt * (Ht - ch)
    A = a1 + a2
    add(fig(svg) + "This is the plan of an L-shaped family room. What area of carpet covers the whole floor?",
        "%d m²" % A, ["%d m²" % (Wt * Ht), "%d m²" % ((Wt - cw) * Ht + Wt * (Ht - ch)), "%d m²" % sum(sides)],
        "Split into two rectangles: %d × %d = %d and %d × %d = %d. Total: %d + %d = %d m²."
        % (Wt - cw, ch, a1, Wt, Ht - ch, a2, a1, a2, A))
    g1, g2 = P.next(), P.next()
    add("%s’s backyard is 8 m by 6 m. %s’s backyard is 7 m by 7 m. Which backyard has the larger area, and by "
        "how much?" % (g1[0], g2[0]), "%s’s, by 1 m²" % g2[0],
        ["%s’s, by 1 m²" % g1[0], "They are the same", "%s’s, by 2 m²" % g2[0]],
        "%s: 8 × 6 = 48 m². %s: 7 × 7 = 49 m². 49 − 48 = 1 m². The perimeters are both 28 m, "
        "but the areas are different." % (g1[0], g2[0]))
    add("A square playground has a perimeter of 64 m. What is its area?", "256 m²",
        ["64 m²", "16 m²", "4096 m²"],
        "Each side: 64 ÷ 4 = 16 m. Area: 16 × 16 = 256 m².")
    add("A rectangular poster for the school athletics carnival has an area of 600 cm². It is 30 cm wide. "
        "How tall is it?", "20 cm", ["570 cm", "270 cm", "18" + NBSP + "000 cm"],
        "Area = width × height, so height = 600 ÷ 30 = 20 cm. Check: 30 × 20 = 600 cm².")
    add("A patio is 6 m long and 4 m wide. Each pallet of pavers covers 5 m². How many pallets are needed?",
        "5 pallets", ["4 pallets", "24 pallets", "2 pallets"],
        "Area: 6 × 4 = 24 m². 24 ÷ 5 = 4 remainder 4. 4 pallets cover only 20 m², so 5 pallets are needed.")
    n, he, his = P.next()
    add("%s is making a chook pen with an area of 36 m². It could be 9 m by 4 m or 6 m by 6 m. "
        "Which pen needs less wire fencing?" % n, "6 m by 6 m",
        ["9 m by 4 m", "They need the same", "You cannot tell"],
        "Both have an area of 36 m². Fence: 9 + 4 + 9 + 4 = 26 m and 6 + 6 + 6 + 6 = 24 m. "
        "The square needs less fence.")
    n, he, his = P.next()
    add("%s has 20 m of edging to make a rectangular vegetable patch. Which patch has the largest area?" % n,
        "5 m by 5 m", ["9 m by 1 m", "8 m by 2 m", "7 m by 3 m"],
        "All four use 20 m of edging. Areas: 9 × 1 = 9 m², 8 × 2 = 16 m², 7 × 3 = 21 m², 5 × 5 = 25 m². "
        "The square has the largest area.")
    add("A bedroom wall is 5 m long and 3 m high. It has a door about 1 m wide and 2 m high. What area of wall "
        "needs painting?", "13 m²", ["15 m²", "17 m²", "16 m²"],
        "Wall: 5 × 3 = 15 m². Door: 1 × 2 = 2 m². Take away the door: 15 − 2 = 13 m².")
    L, W = 120, 90
    add("A classroom pinboard is %d cm long and %d cm wide. What is its area?" % (L, W),
        "%s cm²" % fmt(L * W), ["%d cm²" % (2 * (L + W)), "%d cm²" % (L + W), "%s cm²" % fmt(L * W // 10)],
        "Length × width: %d × %d = %s cm². Tip: 12 × 9 = 108, then × 100." % (L, W, fmt(L * W)))
    L, W, pl, pw = 15, 10, 8, 4
    add("A backyard is %d m long and %d m wide. A swimming pool %d m by %d m is in the backyard. The rest is lawn. "
        "What area of lawn is there?" % (L, W, pl, pw), "%d m²" % (L * W - pl * pw),
        ["%d m²" % (L * W), "%d m²" % (L * W - pl - pw), "%d m²" % (L * W - 2 * (pl + pw))],
        "Backyard: %d × %d = %d m². Pool: %d × %d = %d m². Lawn: %d − %d = %d m²."
        % (L, W, L * W, pl, pw, pl * pw, L * W, pl * pw, L * W - pl * pw))
    svg, whole, more, less, N, T, cols, rows = blob_q(rnd, used_blobs, "pond", "m", 12, 24)
    svg = svg.replace("irregular shape of a pond", "plan of a pond")
    add(fig(svg) + "This plan of a new pond is drawn on a grid. Each square is 1 m². About how much pond liner "
        "is needed to cover the bottom of the pond?", "%d m²" % N,
        ["%d m²" % whole, "%d m²" % T, "%d m²" % (whole + less)],
        "Whole squares: %d. Squares half or more covered: %d. Estimate: %d + %d = %d m²."
        % (whole, more, whole, more, N))
    assert len(its) == 20, len(its)
    return {"title": "Practical problems: fences, carpet and gardens", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

def lesson_blob():
    rnd = random.Random(58110)
    poly, cols, rows, whole, more, less = make_blob(rnd, set(), 12, 20)
    return blob_svg(poly, cols, rows, "irregular shape of a leaf on a squared grid"), whole, more, less


def body_html():
    assert l_sides(13, 9, 6, 4) == [7, 4, 6, 5, 13, 9]
    lab_p = ["", "4 m", "6 m", "", "13 m", "9 m"]
    assert l_sides(14, 9, 6, 4) == [8, 4, 6, 5, 14, 9]
    lab_a = ["8 m", "4 m", "6 m", "5 m", "14 m", "9 m"]
    k = min(240 / 14, 130 / 9)
    l_area = shape_svg(l_pts(14, 9, 6, 4, "tr", k), lab_a, "rectilinear L-shape split into two rectangles",
                       l_split(14, 9, 6, 4, "tr", k),
                       [(4 * k, 2 * k, "A"), (7 * k, 6.5 * k, "B")])
    assert l_area
    assert 8 * 4 + 14 * 5 == 102 == 14 * 9 - 6 * 4 and 7 + 4 + 6 + 5 + 13 + 9 == 44
    grid = grid_svg({(c, r) for c in range(1, 6) for r in range(1, 4)}, 7, 5, "rectangle on a squared grid")
    bsvg, whole, more, less = lesson_blob()
    return (
        "<h2>Perimeter and area</h2>"
        "<p><b>Perimeter</b> is the distance <b>all the way around</b> a shape. It is a length: cm or m.</p>"
        "<p><b>Area</b> is the space <b>inside</b> a shape. It is measured in square units: "
        "<b>cm²</b> (square centimetres) or <b>m²</b> (square metres).</p>"
        "<h2>Perimeter of regular shapes</h2>"
        "<p>A regular shape has all sides the same length. Multiply the side length by the number of sides.</p>"
        "<figure class='sn-fig'>" + reg_svg(6, "5 cm", "regular hexagon with sides of 5 cm") +
        "<figcaption>A regular hexagon has 6 equal sides. Perimeter = 6 × 5 = 30 cm.</figcaption></figure>"
        "<p>For a rectangle, add all 4 sides: 2 lengths and 2 widths.</p>" +
        ex("Example", "A rectangle is 9 cm long and 4 cm wide. What is its perimeter?",
           "9 + 4 + 9 + 4 = 26. Or 2 × (9 + 4) = 26.", "26 cm") +
        "<h2>Perimeter of composite shapes</h2>"
        "<p>A composite rectilinear shape is made of rectangles joined together. Find the missing sides first, "
        "then add every side.</p>"
        "<figure class='sn-fig'>" + l_svg(13, 9, 6, 4, "tr", lab_p) +
        "<figcaption>Missing sides: 13 − 6 = 7 m and 9 − 4 = 5 m. "
        "Perimeter: 7 + 4 + 6 + 5 + 13 + 9 = 44 m.</figcaption></figure>"
        "<p>The short sides going across add up to the long side opposite. The same is true going up and down.</p>"
        "<h2>Area: count squares or use length × width</h2>"
        "<p>Count the 1 cm² squares inside the shape. For a rectangle, it is quicker to multiply.</p>"
        "<figure class='sn-fig'>" + grid +
        "<figcaption>3 rows of 5 squares: 3 × 5 = 15 cm².</figcaption></figure>" +
        ex("Example", "A rectangle has an area of 48 cm². It is 8 cm long. How wide is it?",
           "Length × width = area, so width = 48 ÷ 8 = 6. Check: 8 × 6 = 48.", "6 cm") +
        "<h2>Area of composite shapes</h2>"
        "<p>Split the shape into rectangles. Find the area of each one, then add.</p>"
        "<figure class='sn-fig'>" + l_area +
        "<figcaption>A: 8 × 4 = 32 m². B: 14 × 5 = 70 m². Total: 32 + 70 = 102 m². "
        "Or: whole rectangle 14 × 9 = 126, take away the corner 6 × 4 = 24: 126 − 24 = 102 m².</figcaption></figure>"
        "<h2>Estimating the area of irregular shapes</h2>"
        "<p>Curved shapes do not fit the squares exactly, so we estimate. "
        "Count each whole square. Count a square as 1 if <b>half or more</b> is covered. "
        "Leave out squares that are less than half covered.</p>"
        "<figure class='sn-fig'>" + bsvg +
        "<figcaption>Each square is 1 cm². Whole squares: %d. Half or more covered: %d. "
        "Estimate: %d + %d = %d cm².</figcaption></figure>" % (whole, more, whole, more, whole + more) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the sides to find the area (8 + 5 = 13)", "Area = length × width: 8 × 5 = 40 cm²"],
            ["Multiplying to find the perimeter", "Perimeter: add all the sides"],
            ["Using 4 sides for every shape", "Count the sides: a triangle has 3, a hexagon has 6"],
            ["Missing a hidden side in an L-shape", "Find the missing sides first, then add every side"],
            ["Counting every part square as a whole one", "Count only squares that are half or more covered"],
            ["Writing cm for an area", "Area is in cm² or m². Perimeter is in cm or m"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about perimeter and area in the Australian Curriculum?",
     "a": "They solve practical problems with the perimeter and area of regular and irregular shapes, using cm, m, cm² and m² (AC9M5M02). This includes composite rectangle shapes and estimating the area of curved shapes on a grid."},
    {"q": "What is the difference between perimeter and area?",
     "a": "Perimeter is the distance around the outside of a shape, measured in cm or m. Area is the space inside, measured in square units such as cm² or m²."},
    {"q": "How do you find the area of an irregular shape in Year 5?",
     "a": "Split a shape with straight sides into rectangles and add their areas. For a curved shape, put it on a 1 cm grid and count the whole squares and the squares that are half or more covered."},
    {"q": "Are perimeter and area on the Year 5 NAPLAN numeracy test?",
     "a": "NAPLAN numeracy is based on the Australian Curriculum, so Year 5 students can meet perimeter and area questions. Practising missing sides, length × width and word problems helps them prepare."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position) in every set."""
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
    rnd = random.Random(5811)
    P = People(rnd)
    used, used_blobs = set(), set()
    sets = [set_regular(rnd), set_perimeter(rnd, used), set_rect_area(rnd),
            set_composite(rnd, used, used_blobs), set_story(rnd, P, used, used_blobs)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(k) == 5 for k in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "perimeter-and-area", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Perimeter and Area",
        "seo_title": "Year 5 Perimeter and Area Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Perimeter and area",
        "domain": "Measurement",
        "standard_code": "AC9M5M02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve practical problems involving the perimeter and area of regular and irregular shapes using appropriate metric units",
        "meta_desc": "Free Year 5 perimeter and area worksheets for the Australian Curriculum (AC9M5M02): regular shapes, composite shapes with missing sides, length × width in cm² and m², estimating irregular areas on a grid and practical problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "Perimeter: add every side. Area of a rectangle: length × width.",
        "key_sub": "Find missing sides first. Split composite shapes into rectangles and add their areas. Perimeter is in cm or m; area is in cm² or m².",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*(grid|rectilinear)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
