# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Area of Rectangles (Australian Curriculum v9.0, AC9M6M02)
  python3 tools/gen_au_maths_y6_area_rectangles.py
Establish area = length × width from grids; areas in cm² and m² with decimals and mixed units;
missing side from the area; composite rectilinear shapes; practical problems (tiles, turf, paint,
netball courts). Wrong choices come from real mistakes (perimeter instead of area, adding instead
of multiplying, mixed units, remainder written as a decimal). Every answer is worked out in code.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
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

# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

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



def D(x):
    return Decimal(str(x))


def df(x):
    """Decimal -> '2.5', '10', '0.25' (no trailing zeros); 5+ digit whole numbers get a no-break space."""
    x = D(x)
    s = format(x, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if "." not in s:
        return fmt(int(s))
    return s


def du(x, u):
    return "%s %s" % (df(x), u)


def rot(c, k):
    r = k % len(c)
    return c[r:] + c[:r]


# ------------------------------------------------------------ partly covered rectangle (establish the formula)
def partial_svg(L, W, label, cell=22):
    """L × W rectangle: only the top row and the left column of unit squares are drawn."""
    m = 4
    Wd, Hd = L * cell + 2 * m, W * cell + 2 * m
    g = []
    cells = {(c, 0) for c in range(L)} | {(0, r) for r in range(W)}
    g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (m, m, L * cell, W * cell))
    for (c, r) in sorted(cells):
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (m + c * cell, m + r * cell, cell, cell, FILL, GRIDC))
    g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (m, m, L * cell, W * cell, GREEN))
    return svg_wrap(Wd, Hd, "".join(g), label)


# ------------------------------------------------------------ rectangle with a rectangular hole
def hole_svg(W, H, hw, hh, u, label):
    k = min(240 / W, 130 / H)
    top, left = "%s %s" % (df(W), u), "%s %s" % (df(H), u)
    inner = "%s %s × %s %s" % (df(hw), u, df(hh), u)
    lw = tw(left, FS) + 10
    pad = 5
    ox, oy = pad + lw, pad + 26
    Wp, Hp = float(W) * k, float(H) * k
    hwp, hhp = float(hw) * k, float(hh) * k
    assert hwp >= tw(inner, 15) + 12 and hhp >= 28, (W, H, hw, hh)
    hx, hy = ox + (Wp - hwp) / 2, oy + (Hp - hhp) / 2
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='3'/>"
         % (ox, oy, Wp, Hp, FILL, GREEN),
         "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         % (hx, hy, hwp, hhp, GREEN),
         text(ox + Wp / 2, oy - 9, top, FS),
         text(ox - lw / 2 - 2, oy + Hp / 2 + 6, left, FS),
         text(hx + hwp / 2, hy + hhp / 2 + 5, inner, 15)]
    return svg_wrap(int(math.ceil(ox + Wp + pad)), int(math.ceil(oy + Hp + pad)), "".join(s), label)


# ------------------------------------------------------------ set 1: area = length × width from grids
def set_grids(rnd):
    its = []
    for k, (L, W) in enumerate([(5, 3), (7, 2), (6, 4), (8, 3), (9, 4), (5, 5)]):
        A, P = L * W, 2 * (L + W)
        assert A != P
        cells = {(c, r) for c in range(1, L + 1) for r in range(1, W + 1)}
        svg = grid_svg(cells, L + 2, W + 2, "rectangle on a squared grid")
        q = fig(svg) + "Each square is 1 cm². What is the area of the shaded %s?" % ("square" if L == W else "rectangle")
        e = ("%d rows of %d squares: %d × %d = %d cm². (%d cm would be the distance around it, the perimeter.)"
             % (W, L, W, L, A, P))
        cands = rot(["%d cm²" % P, "%d cm²" % (L + W), "%d cm" % A], k)
        its.append(mcq(q, "%d cm²" % A, cands, e, rnd))
    for k, (L, W) in enumerate([(7, 3), (6, 5), (9, 4)]):
        A, shown = L * W, L + W - 1
        svg = partial_svg(L, W, "rectangle on a grid with only the top row and left column of squares drawn")
        q = (fig(svg) + "Only the top row and the left column of 1 cm² squares are drawn. "
             "How many squares would cover the whole rectangle?")
        e = ("There are %d squares in each row and %d rows. %d × %d = %d squares, so the area is %d cm². "
             "This is why area = length × width." % (L, W, W, L, A, A))
        cands = rot(["%d squares" % shown, "%d squares" % (L + W), "%d squares" % (2 * (L + W))], k)
        its.append(mcq(q, "%d squares" % A, cands, e, rnd))
    for i, (L, W, u) in enumerate([(8, 5, "cm"), (12, 4, "m"), (9, 7, "cm"), (15, 6, "m"), (11, 8, "cm"),
                                   (20, 9, "m")]):
        A, P = L * W, 2 * (L + W)
        assert A != P
        if i < 3:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
                 "What is the area of this rectangle?")
        else:
            q = "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
        e = "Area = length × width: %d × %d = %d %s. (%d %s is the perimeter.)" % (L, W, A, u2(u), P, u)
        cands = rot(["%d %s" % (P, u2(u)), "%d %s" % (L + W, u2(u)), "%d %s" % (A, u)], i)
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    for k, (s, u) in enumerate([(7, "cm"), (12, "m")]):
        A = s * s
        if k == 0:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u), max_h=95)) +
                 "This is a square. What is its area?")
        else:
            q = "A square has sides of %d %s. What is its area?" % (s, u)
        e = "Length and width of a square are the same: %d × %d = %d %s." % (s, s, A, u2(u))
        cands = ["%d %s" % (4 * s, u2(u)), "%d %s" % (2 * s, u2(u)), "%d %s" % (A, u)]
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    its.append(mcq("Which is the formula for the area of a rectangle?", "length × width",
                   ["length + width", "2 × (length + width)", "length × length"],
                   "Area counts the squares inside: rows × squares in each row, which is length × width. "
                   "2 × (length + width) gives the perimeter.", rnd))
    its.append(mcq("A rectangle is covered by 6 rows of 1 m² squares. There are 9 squares in each row. "
                   "What is its area?", "54 m²", ["15 m²", "30 m²", "54 m"],
                   "6 rows of 9 squares: 6 × 9 = 54 squares, so the area is 54 m². "
                   "Area is in square units (m²), not m.", rnd))
    its.append(mcq("Rectangle A is 6 cm by 4 cm. Rectangle B is 8 cm by 3 cm. Which has the larger area?",
                   "They are the same", ["Rectangle A", "Rectangle B", "You cannot tell"],
                   "A: 6 × 4 = 24 cm². B: 8 × 3 = 24 cm². The areas are the same, even though the shapes are "
                   "different (their perimeters are 20 cm and 22 cm).", rnd))
    assert len(its) == 20
    return {"title": "Area = length × width (from grids)", "items": its}


# ------------------------------------------------------------ set 2: cm², m² and decimals
def set_decimals(rnd):
    its = []
    rects = [("2.5", "4", "m"), ("3.5", "2", "m"), ("1.5", "6", "m"), ("4.5", "3", "m"), ("8", "0.5", "m"),
             ("5", "1.2", "m"), ("3", "0.8", "m"), ("6.5", "4", "cm"), ("7.5", "2", "cm"), ("12", "0.5", "cm"),
             ("2.5", "1.6", "m"), ("8", "3.5", "cm")]
    for i, (a, b, u) in enumerate(rects):
        L, W = D(a), D(b)
        A, P = L * W, 2 * (L + W)
        assert A != P and A != L + W
        whole = int(L) * int(W)
        shift = A * 10
        if i < 4:
            X, Y = max(L, W), min(L, W)          # draw the longer side across
            q = (fig(rect_svg(float(X), float(Y), du(X, u), du(Y, u), "rectangle %s %s by %s %s" % (a, u, b, u))) +
                 "What is the area of this rectangle?")
        else:
            q = "A rectangle is %s long and %s wide. What is its area?" % (du(L, u), du(W, u))
        e = "Area = length × width: %s × %s = %s %s." % (df(L), df(W), df(A), u2(u))
        X, Y = (L, W) if W == int(W) else (W, L)
        if X != int(X) and Y == int(Y) and int(X) > 0:
            e += " Tip: %s × %s = %s and %s × %s = %s, so %s + %s = %s." % (
                int(X), df(Y), df(int(X) * Y), df(X - int(X)), df(Y), df((X - int(X)) * Y),
                df(int(X) * Y), df((X - int(X)) * Y), df(A))
        cands = ["%s %s" % (df(P), u2(u)), "%s %s" % (df(L + W), u2(u)), "%s %s" % (df(shift), u2(u))]
        if whole and whole != A:
            cands.insert(i % 3, "%s %s" % (df(whole), u2(u)))
        its.append(mcq(q, "%s %s" % (df(A), u2(u)), rot(cands, i), e, rnd))
    for k, (s, u) in enumerate([("1.5", "m"), ("2.5", "m")]):
        S = D(s)
        A = S * S
        q = "A square has sides of %s. What is its area?" % du(S, u)
        e = "Square: side × side = %s × %s = %s %s." % (df(S), df(S), df(A), u2(u))
        cands = ["%s %s" % (df(4 * S), u2(u)), "%s %s" % (df(2 * S), u2(u)), "%s %s" % (df(int(S) * int(S) + D("0.25")), u2(u)),
                 "%s %s" % (df(A), u)]
        its.append(mcq(q, "%s %s" % (df(A), u2(u)), cands, e, rnd))
    its.append(mcq("A rug is 2 m long and 50 cm wide. What is its area in square metres?", "1 m²",
                   ["100 m²", "10 m²", "52 m²"],
                   "Use the same unit first: 50 cm = 0.5 m. Area = 2 × 0.5 = 1 m². "
                   "2 × 50 = 100 mixes metres and centimetres.", rnd))
    its.append(mcq("A garden bed is 3 m long and 40 cm wide. What is its area in square metres?", "1.2 m²",
                   ["120 m²", "12 m²", "6.8 m²"],
                   "40 cm = 0.4 m. Area = 3 × 0.4 = 1.2 m². (120 comes from 3 × 40, which mixes units.)", rnd))
    its.append(mcq("A poster is 1 m long and 60 cm wide. What is its area in square centimetres?", "6000 cm²",
                   ["60 cm²", "600 cm²", "320 cm²"],
                   "1 m = 100 cm. Area = 100 × 60 = 6000 cm². (320 cm is the perimeter.)", rnd))
    its.append(mcq("How many square centimetres are in 1 square metre?", "10" + NBSP + "000 cm²",
                   ["100 cm²", "1000 cm²", "400 cm²"],
                   "1 m² is a square 100 cm by 100 cm. 100 × 100 = 10" + NBSP + "000 cm². "
                   "100 cm² is only one row of it.", rnd))
    its.append(mcq("Which unit is best for the area of a school basketball court?", "m²",
                   ["cm²", "m", "km²"],
                   "A court is tens of metres long and wide, so square metres (m²) fit. m measures length, "
                   "not area.", rnd))
    its.append(mcq("Which unit is best for the area of a postage stamp?", "cm²",
                   ["m²", "cm", "km²"],
                   "A stamp is only a few centimetres long and wide, so square centimetres (cm²) fit.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area in cm² and m², with decimals", "items": its}


# ------------------------------------------------------------ set 3: missing side from the area
def set_missing(rnd):
    its = []

    def whole(A, L, u, figure):
        w = A // L
        assert w * L == A and w != L
        if figure:
            q = (fig(rect_svg(L, w, "%d %s" % (L, u), "? %s" % u, "rectangle with one side missing")) +
                 "The area of this rectangle is %d %s. What is the length of the side marked ?" % (A, u2(u)))
        else:
            q = "A rectangle has an area of %d %s. One side is %d %s. How long is the other side?" % (A, u2(u), L, u)
        e = ("Length × width = area, so the missing side = area ÷ known side: %d ÷ %d = %d %s. Check: %d × %d = %d %s."
             % (A, L, w, u, L, w, A, u2(u)))
        cands = ["%d %s" % (A - L, u)]
        if A // 2 - L > 0 and A % 2 == 0 and A // 2 - L != w:
            cands.append("%d %s" % (A // 2 - L, u))
        cands += ["%s %s" % (fmt(A * L), u), "%d %s" % (w, u2(u))]
        return mcq(q, "%d %s" % (w, u), cands, e, rnd)

    for A, L, u in [(48, 8, "cm"), (63, 9, "m"), (84, 12, "cm"), (72, 6, "m"), (56, 7, "cm"), (90, 15, "m")]:
        its.append(whole(A, L, u, True))
    for A, L, u in [(96, 8, "cm"), (108, 9, "m"), (150, 10, "cm"), (132, 11, "m"), (210, 14, "cm"), (240, 16, "m")]:
        its.append(whole(A, L, u, False))
    for k, (A, u) in enumerate([(49, "cm"), (81, "m"), (144, "cm")]):
        s = int(math.isqrt(A))
        q = "A square has an area of %d %s. How long is each side?" % (A, u2(u))
        e = ("Side × side = %d. %d × %d = %d, so each side is %d %s. (%d ÷ 4 would be the side if %d were the "
             "perimeter.)" % (A, s, s, A, s, u, A, A))
        cands = rot(["%s %s" % (df(D(A) / 4), u), "%s %s" % (df(D(A) / 2), u), "%d %s" % (A - s, u)], k)
        its.append(mcq(q, "%d %s" % (s, u), cands, e, rnd))
    for A, L in [(15, 6), (18, 4), (22, 4)]:
        w = D(A) / D(L)
        qq, r = divmod(A, L)
        assert r and w * L == A
        q = "A rectangular rug has an area of %d m². One side is %d m. How long is the other side?" % (A, L)
        e = ("Other side = %d ÷ %d = %s m. The remainder %d is %d out of %d, which is %s, so the answer is %s m, not %d.%d m. "
             "Check: %d × %s = %d m²." % (A, L, df(w), r, r, L, df(D(r) / L), df(w), qq, r, L, df(w), A))
        cands = ["%d.%d m" % (qq, r), "%d m" % (A - L), "%d m" % qq, "%d m" % (A * L)]
        its.append(mcq(q, "%s m" % df(w), cands, e, rnd))
    for A, L in [(40, 8), (54, 9)]:
        w = A // L
        P = 2 * (L + w)
        q = "A rectangle has an area of %d cm² and a length of %d cm. What is its perimeter?" % (A, L)
        e = ("First find the width: %d ÷ %d = %d cm. Then perimeter = %d + %d + %d + %d = %d cm."
             % (A, L, w, L, w, L, w, P))
        cands = ["%d cm" % (L + w), "%d cm" % (2 * L + w), "%d cm" % (L + 2 * w)]
        its.append(mcq(q, "%d cm" % P, cands, e, rnd))
    assert len(its) == 20
    return {"title": "Find the missing side from the area", "items": its}


# ------------------------------------------------------------ set 4: composite rectilinear shapes
def set_composite(rnd, used):
    its = []
    for i in range(6):
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
        cands = rot(["%d %s" % (Wt * Ht, u2(u)), "%d %s" % (dbl, u2(u)), "%d %s" % (sum(sides), u2(u))], i) + \
            ["%d %s" % (A, u)]
        its.append(mcq(fig(svg) + "What is the area of this shape?", "%d %s" % (A, u2(u)), cands, e, rnd))
    for i in range(4):
        u = ["m", "cm"][i % 2]

        def lab(s, u=u):
            return ["" if j in (0, 3) else "%d %s" % (v, u) for j, v in enumerate(s)]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lab, lo=(8, 5), hi=(20, 14))
        a1, a2 = (Wt - cw) * ch, Wt * (Ht - ch)
        A = a1 + a2
        e = ("Missing sides: %d − %d = %d %s and %d − %d = %d %s. Split into two rectangles: "
             "%d × %d = %d and %d × %d = %d. Area = %d + %d = %d %s."
             % (Wt, cw, Wt - cw, u, Ht, ch, Ht - ch, u, Wt - cw, ch, a1, Wt, Ht - ch, a2, a1, a2, A, u2(u)))
        cands = ["%d %s" % (Wt * Ht, u2(u)), "%d %s" % (a1 + Wt * Ht, u2(u)),
                 "%d %s" % (Wt * Ht - (Wt - cw) * (Ht - ch), u2(u)), "%d %s" % (sum(sides), u2(u))]
        q = fig(svg) + "Two sides are not labelled. What is the area of the shape?"
        its.append(mcq(q, "%d %s" % (A, u2(u)), cands, e, rnd))
    for i in range(3):
        u = ["cm", "m"][i % 2]
        W, H, a, n, d, sides, svg = u_figure(
            rnd, used, lambda s, u=u: ["" if j == 3 else "%d %s" % (v, u) for j, v in enumerate(s)], i % 2 == 1)
        A = W * H - n * d
        e = ("Take the whole rectangle and subtract the gap: %d × %d = %d, gap %d × %d = %d. "
             "%d − %d = %d %s." % (W, H, W * H, n, d, n * d, W * H, n * d, A, u2(u)))
        cands = ["%d %s" % (W * H, u2(u)), "%d %s" % (W * H - 2 * n * d, u2(u)), "%d %s" % (sum(sides), u2(u)),
                 "%d %s" % (W * H - n * H, u2(u))]
        its.append(mcq(fig(svg) + "What is the area of this shape?", "%d %s" % (A, u2(u)), cands, e, rnd))
    for i in range(3):
        u = ["m", "cm"][i % 2]
        W, H, x1, x2, y1, y2, sides, svg = step_figure(
            rnd, used, lambda s, u=u: ["%d %s" % (v, u) for v in s], i % 2 == 0)
        parts = [(x1, H), (x2 - x1, H - y1), (W - x2, H - y2)]
        ar = [p * q for p, q in parts]
        A = sum(ar)
        e = ("Split it into three rectangles side by side: %d × %d = %d, %d × (%d − %d) = %d × %d = %d, "
             "%d × (%d − %d) = %d × %d = %d. Add: %s = %d %s."
             % (x1, H, ar[0], x2 - x1, H, y1, x2 - x1, H - y1, ar[1], W - x2, H, y2, W - x2, H - y2, ar[2],
                plus(ar), A, u2(u)))
        cands = ["%d %s" % (W * H, u2(u)), "%d %s" % (A - ar[2], u2(u)), "%d %s" % (sum(sides), u2(u)),
                 "%d %s" % (x1 * H + (x2 - x1) * (y2 - y1) + (W - x2) * (H - y2), u2(u))]
        its.append(mcq(fig(svg) + "What is the area of this shape?", "%d %s" % (A, u2(u)), cands, e, rnd))
    for W, H, hw, hh, u in [(20, 12, 10, 4, "m"), (24, 15, 14, 6, "cm")]:
        A = W * H - hw * hh
        svg = hole_svg(W, H, hw, hh, u, "rectangle with a rectangular hole cut out")
        e = ("Big rectangle: %d × %d = %d. Hole: %d × %d = %d. Shaded part: %d − %d = %d %s."
             % (W, H, W * H, hw, hh, hw * hh, W * H, hw * hh, A, u2(u)))
        cands = ["%d %s" % (W * H, u2(u)), "%d %s" % (W * H - hw - hh, u2(u)), "%d %s" % (W * H + hw * hh, u2(u)),
                 "%d %s" % ((W - hw) * (H - hh), u2(u))]
        its.append(mcq(fig(svg) + "A rectangle is cut out of a larger rectangle. What is the area of the shaded part?",
                       "%d %s" % (A, u2(u)), cands, e, rnd))
    its.append(mcq("A shape is made of two rectangles that do not overlap: 4 m by 3.5 m and 2 m by 1.5 m. "
                   "What is its total area?", "17 m²", ["14 m²", "30 m²", "11 m²"],
                   "4 × 3.5 = 14 m² and 2 × 1.5 = 3 m². Total: 14 + 3 = 17 m². "
                   "Multiplying the added sides, (4 + 2) × (3.5 + 1.5) = 30, does not work.", rnd))
    its.append(mcq("A rectangle 10 cm by 6 cm has a 2.5 cm by 2 cm rectangle cut from one corner. "
                   "What area is left?", "55 cm²", ["60 cm²", "55.5 cm²", "65 cm²"],
                   "Whole rectangle: 10 × 6 = 60 cm². Corner: 2.5 × 2 = 5 cm². 60 − 5 = 55 cm². "
                   "(55.5 comes from taking away 2.5 + 2 instead of 2.5 × 2.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Composite shapes: split into rectangles", "items": its}


# ------------------------------------------------------------ set 5: practical problems
def set_story(rnd, P, used):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    add("A bathroom floor is 3 m long and 2 m wide. It is tiled with square tiles 50 cm by 50 cm. "
        "How many tiles are needed?", "24 tiles", ["6 tiles", "10 tiles", "12 tiles"],
        "Along the length: 300 cm ÷ 50 cm = 6 tiles. Across: 200 cm ÷ 50 cm = 4 tiles. 6 × 4 = 24 tiles. "
        "(6 is the area in m², not the number of tiles.)")
    add("A bathroom wall is 2.4 m wide and 2 m high. It is covered with square tiles 20 cm by 20 cm. "
        "How many tiles are needed?", "120 tiles", ["22 tiles", "44 tiles", "48 tiles"],
        "Across: 240 ÷ 20 = 12 tiles. Up: 200 ÷ 20 = 10 tiles. 12 × 10 = 120 tiles.")
    add("A netball court is about 30 m long and 15 m wide. About what is its area?", "450 m²",
        ["90 m²", "45 m²", "4500 m²"],
        "Area = length × width: 30 × 15 = 450 m². (30 + 15 + 30 + 15 = 90 m is the distance around it.)")
    add("A netball court about 30 m long and 15 m wide is marked into three equal thirds along its length. "
        "About what is the area of one third?", "150 m²", ["450 m²", "225 m²", "50 m²"],
        "Each third is 30 ÷ 3 = 10 m long and 15 m wide: 10 × 15 = 150 m². Check: 3 × 150 = 450 m².")
    n, he, his = P.next()
    add("%s’s family is laying new turf in a backyard 8 m long and 6.5 m wide. Turf costs $12 per square metre. "
        "How much will the turf cost?" % n, "$624", ["$348", "$174", "$52"],
        "Area: 8 × 6.5 = 52 m². Cost: 52 × $12 = $624. ($348 uses the perimeter, 29 m, instead of the area.)")
    add("A backyard is 9 m by 5 m. A concrete patio 3 m by 2 m is in one corner. The rest gets turf. "
        "How many square metres of turf are needed?", "39 m²", ["45 m²", "51 m²", "40 m²"],
        "Backyard: 9 × 5 = 45 m². Patio: 3 × 2 = 6 m². Turf: 45 − 6 = 39 m². "
        "(40 comes from taking away 3 + 2.)")
    add("A wall is 6 m long and 2.5 m high. It needs two coats of paint. One litre of paint covers 10 m². "
        "How many litres are needed?", "3 L", ["1.5 L", "1.7 L", "15 L"],
        "Wall: 6 × 2.5 = 15 m². Two coats: 2 × 15 = 30 m². 30 ÷ 10 = 3 L. (1.5 L is only one coat.)")
    add("A bedroom wall is 4 m long and 3 m high. It has a window 1.5 m by 1 m. What area of wall needs painting?",
        "10.5 m²", ["12 m²", "13.5 m²", "9.5 m²"],
        "Wall: 4 × 3 = 12 m². Window: 1.5 × 1 = 1.5 m². 12 − 1.5 = 10.5 m². "
        "(9.5 comes from taking away 1.5 + 1.)")
    add("A classroom floor is 9 m long and 7 m wide. New carpet costs $40 per square metre. "
        "How much does carpet for the floor cost?", "$2520", ["$1280", "$640", "$63"],
        "Area: 9 × 7 = 63 m². Cost: 63 × $40 = $2520. ($1280 uses the perimeter, 32 m.)")
    add("A patio is 5 m long and 4.5 m wide. Each box of pavers covers 2 m². How many boxes are needed?",
        "12 boxes", ["11 boxes", "23 boxes", "45 boxes"],
        "Area: 5 × 4.5 = 22.5 m². 22.5 ÷ 2 = 11.25, so 11 boxes are not enough. Buy 12 boxes.")
    add("A backyard pool is 10 m long and 4 m wide. The pool cover must be 0.5 m bigger than the pool on every "
        "side. What is the area of the cover?", "55 m²", ["40 m²", "47.25 m²", "50 m²"],
        "0.5 m on each side adds 1 m to each measurement: 11 m by 5 m. Area: 11 × 5 = 55 m². "
        "(47.25 comes from adding 0.5 m only once: 10.5 × 4.5.)")
    n, he, his = P.next()
    add("%s’s class has a vegetable garden bed 4 m long and 2.5 m wide. Each seedling needs 0.5 m². "
        "How many seedlings fit in the bed?" % n, "20 seedlings", ["5 seedlings", "13 seedlings", "10 seedlings"],
        "Area: 4 × 2.5 = 10 m². 10 ÷ 0.5 = 20 seedlings (there are 2 halves in each square metre).")
    add("A solar panel is 1.7 m long and 1 m wide. A school puts 12 panels on the roof of the hall. "
        "What area do the panels cover?", "20.4 m²", ["32.4 m²", "1.7 m²", "204 m²"],
        "One panel: 1.7 × 1 = 1.7 m². 12 panels: 12 × 1.7 = 20.4 m². (32.4 comes from 12 × (1.7 + 1).)")
    g1, g2 = P.next(), P.next()
    add("%s’s bedroom is 4.5 m by 4 m. %s’s bedroom is 6 m by 3 m. Which bedroom has the larger floor area?"
        % (g1[0], g2[0]), "They are the same", ["%s’s" % g1[0], "%s’s" % g2[0], "You cannot tell"],
        "%s: 4.5 × 4 = 18 m². %s: 6 × 3 = 18 m². The areas are the same, even though the perimeters "
        "(17 m and 18 m) are different." % (g1[0], g2[0]))
    add("A rectangular garden bed must have an area of 24 m². One side is 3 m. How much edging goes all the way "
        "around it?", "22 m", ["11 m", "24 m", "14 m"],
        "Other side: 24 ÷ 3 = 8 m. Edging: 3 + 8 + 3 + 8 = 22 m.")
    add("A path is 2 m long and 1 m wide. It is paved with bricks 20 cm long and 10 cm wide, long sides along the "
        "path. How many bricks are needed?", "100 bricks", ["20 bricks", "40 bricks", "1000 bricks"],
        "Along the path: 200 ÷ 20 = 10 bricks. Across: 100 ÷ 10 = 10 bricks. 10 × 10 = 100 bricks.")
    add("A rug is 3 m by 2 m. A new rug is twice as long and twice as wide. What is the area of the new rug?",
        "24 m²", ["12 m²", "6 m²", "20 m²"],
        "New rug: 6 m by 4 m. Area: 6 × 4 = 24 m². That is 4 times the old area (6 m²), not 2 times.")
    add("A classroom whiteboard is 2.4 m long and 1.2 m high. What is its area?", "2.88 m²",
        ["3.6 m²", "7.2 m²", "28.8 m²"],
        "2.4 × 1.2: 24 × 12 = 288, and there are 2 decimal places, so 2.88 m². (3.6 comes from adding.)")
    n, he, his = P.next()
    add("%s mows a lawn 12 m long and 8 m wide. %s mows about 8 m² each minute. About how long does it take?"
        % (n, cap(he)), "12 minutes", ["5 minutes", "96 minutes", "20 minutes"],
        "Area: 12 × 8 = 96 m². 96 ÷ 8 = 12 minutes. (5 minutes uses the perimeter, 40 m.)")
    for _ in range(300):
        Wt, Ht, cw, ch = pick_l(rnd, used, (8, 6), (14, 10))
        sides = l_sides(Wt, Ht, cw, ch)
        if (Wt - cw) * Ht == Wt * ch:
            continue
        svg = l_svg(Wt, Ht, cw, ch, "bl", ["%d m" % v for v in sides], "plan of a rectilinear L-shaped backyard")
        if svg:
            break
    a1, a2 = (Wt - cw) * ch, Wt * (Ht - ch)
    A = a1 + a2
    c = 11
    add(fig(svg) + "This is the plan of an L-shaped backyard. Turf costs $%d per square metre. "
        "How much does turf for the whole backyard cost?" % c, "$%d" % (A * c),
        ["$%d" % (Wt * Ht * c), "$%d" % (sum(sides) * c), "$%d" % A],
        "Split into two rectangles: %d × %d = %d and %d × %d = %d. Area: %d + %d = %d m². Cost: %d × $%d = $%d."
        % (Wt - cw, ch, a1, Wt, Ht - ch, a2, a1, a2, A, A, c, A * c))
    assert len(its) == 20, len(its)
    return {"title": "Practical problems: tiles, turf, paint and courts", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    grid = partial_svg(5, 3, "rectangle on a grid with only the top row and left column of squares drawn")
    full = grid_svg({(c, r) for c in range(1, 6) for r in range(1, 4)}, 7, 5, "rectangle on a squared grid")
    rect = rect_svg(4, 2.5, "4 m", "2.5 m", "rectangle 4 m by 2.5 m")
    assert l_sides(14, 9, 6, 4) == [8, 4, 6, 5, 14, 9]
    k = min(240 / 14, 130 / 9)
    l_area = shape_svg(l_pts(14, 9, 6, 4, "tr", k), ["8 m", "4 m", "6 m", "5 m", "14 m", "9 m"],
                       "rectilinear L-shape split into two rectangles", l_split(14, 9, 6, 4, "tr", k),
                       [(4 * k, 2 * k, "A"), (7 * k, 6.5 * k, "B")])
    assert l_area and 8 * 4 + 14 * 5 == 102 == 14 * 9 - 6 * 4
    assert D("2.5") * 4 == 10 and D(15) / 6 == D("2.5")
    return (
        "<h2>Why area = length × width</h2>"
        "<p>Area is the number of unit squares that cover a shape. "
        "It is measured in square units: <b>cm²</b> (square centimetres) or <b>m²</b> (square metres).</p>"
        "<p>Squares in a rectangle sit in equal rows. Count the squares in one row and the number of rows, "
        "then multiply.</p>"
        "<figure class='sn-fig'>" + grid +
        "<figcaption>5 squares in each row, 3 rows: 3 × 5 = 15 squares.</figcaption></figure>"
        "<figure class='sn-fig'>" + full +
        "<figcaption>Each square is 1 cm², so the area is 15 cm². The length is 5 cm and the width is 3 cm: "
        "5 × 3 = 15.</figcaption></figure>"
        "<p><b>Area of a rectangle = length × width.</b> For a square, side × side.</p>"
        "<h2>Decimals and units</h2>"
        "<p>The formula works with decimals too. Both sides must be in the <b>same unit</b> before you multiply.</p>"
        "<figure class='sn-fig'>" + rect +
        "<figcaption>4 × 2.5 = 10 m². Think 4 × 2 = 8 and 4 × 0.5 = 2, so 8 + 2 = 10.</figcaption></figure>" +
        ex("Example: mixed units", "A rug is 2 m long and 50 cm wide. What is its area in m²?",
           "Change 50 cm to 0.5 m. 2 × 0.5 = 1.", "1 m²") +
        "<h2>Finding a missing side</h2>"
        "<p>If you know the area and one side, divide: <b>width = area ÷ length</b>.</p>" +
        ex("Example", "A rectangle has an area of 15 m². It is 6 m long. How wide is it?",
           "15 ÷ 6 = 2.5. Check: 6 × 2.5 = 15.", "2.5 m") +
        "<h2>Composite shapes</h2>"
        "<p>Split the shape into rectangles. Find each area, then add. Or take the big rectangle and subtract the "
        "missing part.</p>"
        "<figure class='sn-fig'>" + l_area +
        "<figcaption>A: 8 × 4 = 32 m². B: 14 × 5 = 70 m². Total: 32 + 70 = 102 m². "
        "Or 14 × 9 = 126, take away the corner 6 × 4 = 24: 126 − 24 = 102 m².</figcaption></figure>"
        "<h2>Practical problems</h2>" +
        ex("Example: turf", "A backyard is 8 m by 6.5 m. Turf costs $12 per m². What does it cost?",
           "Area: 8 × 6.5 = 52 m². Cost: 52 × $12 = $624.", "$624") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Finding the perimeter (8 + 5 + 8 + 5 = 26)", "Area = length × width: 8 × 5 = 40 cm²"],
            ["Adding the length and width (8 + 5 = 13)", "Multiply, do not add"],
            ["Mixing units (2 m × 50 cm = 100)", "Change to one unit first: 2 × 0.5 = 1 m²"],
            ["Writing a remainder as a decimal (15 ÷ 6 = 2.3)", "15 ÷ 6 = 2.5, because 3 out of 6 is 0.5"],
            ["Using the whole rectangle for an L-shape", "Split it, or subtract the missing corner"],
            ["Writing m for an area", "Area is in cm² or m². Length is in cm or m"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about area in the Australian Curriculum?",
     "a": "They establish the formula for the area of a rectangle, length × width, and use it to solve practical problems (AC9M6M02). This includes decimals, cm² and m², missing sides and shapes made of rectangles."},
    {"q": "How do you explain area = length × width to a child?",
     "a": "Cover the rectangle with 1 cm squares. The squares form equal rows, so the number of rows times the squares in each row gives the area, which is the width times the length."},
    {"q": "How do you find the area of a rectangle with decimals?",
     "a": "Multiply the length by the width as usual, keeping both in the same unit. For example, 2.5 m × 4 m = 10 m²."},
    {"q": "How does this help with Year 7 maths and NAPLAN?",
     "a": "Year 7 students sit NAPLAN numeracy, which includes area problems. Being confident with length × width, missing sides and composite shapes in Year 6 prepares students for high school maths."},
]


def gen():
    rnd = random.Random(6813)
    P = People(rnd)
    used = set()
    sets = [set_grids(rnd), set_decimals(rnd), set_missing(rnd), set_composite(rnd, used), set_story(rnd, P, used)]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "area-of-rectangles", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Area of Rectangles",
        "seo_title": "Year 6 Area of Rectangles Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Area of rectangles",
        "domain": "Measurement",
        "standard_code": "AC9M6M02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Establish the formula for the area of a rectangle and use it to solve practical problems",
        "meta_desc": "Free Year 6 area of rectangles worksheets for the Australian Curriculum (AC9M6M02): length × width from grids, cm² and m² with decimals, missing sides, composite shapes and practical problems with tiles, turf and paint. 100 questions with an answer key.",
        "key_big": "Area of a rectangle = length × width.",
        "key_sub": "Put both sides in the same unit first. Width = area ÷ length. Split composite shapes into rectangles. Area is in cm² or m².",
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
