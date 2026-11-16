# -*- coding: utf-8 -*-
"""
Pictures for the US Kindergarten units (gen_us_math_gk_*.py).
Big, simple objects that 5-6 year olds can point at and count.
Every layout returns an inline SVG (viewBox set, single-quoted attributes, no backslashes).
"""
import math, random
from ws_common import svg_wrap, text, GREEN, FILL, INK, RED

CUBE = "#f2c94c"

# kind -> (singular, plural)
NAMES = {
    "apple": ("apple", "apples"), "star": ("star", "stars"), "ball": ("ball", "balls"),
    "button": ("button", "buttons"), "fish": ("fish", "fish"), "flower": ("flower", "flowers"),
    "heart": ("heart", "hearts"), "duck": ("duck", "ducks"), "cup": ("cup", "cups"),
    "dot": ("dot", "dots"), "cube": ("cube", "cubes"), "bug": ("ladybug", "ladybugs"),
}
KINDS = ["apple", "star", "ball", "button", "fish", "flower", "heart", "duck", "cup", "bug"]


def name(kind, n=2):
    s, p = NAMES[kind]
    return s if n == 1 else p


def obj(kind, cx, cy, r=13):
    """One object centred at (cx, cy), about 2r wide."""
    k = r / 13.0
    if kind == "apple":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#e05a4f' stroke='#9b2d24' stroke-width='1.4'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2.4' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                % (cx, cy + 2 * k, 11 * k, cx, cy - 8 * k, cx + 1.5 * k, cy - 13 * k,
                   cx + 6 * k, cy - 11 * k, 5 * k, 2.6 * k, GREEN, cx + 6 * k, cy - 11 * k))
    if kind == "star":
        pts = []
        for i in range(10):
            rr = (13.5 if i % 2 == 0 else 5.8) * k
            a = -math.pi / 2 + i * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + 1.5 * k + rr * math.sin(a)))
        return "<polygon points='%s' fill='#f4c430' stroke='#a57c00' stroke-width='1.4'/>" % " ".join(pts)
    if kind == "ball":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#5b9bd5' stroke='#2e5f8a' stroke-width='1.4'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='2'/>"
                % (cx, cy, 12 * k, cx - 12 * k, cy, cx, cy - 8 * k, cx + 12 * k, cy))
    if kind == "button":
        s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, 12 * k, FILL, GREEN)]
        for dx, dy in [(-3.4, -3.4), (3.4, -3.4), (-3.4, 3.4), (3.4, 3.4)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx + dx * k, cy + dy * k, 1.8 * k, GREEN))
        return "".join(s)
    if kind == "fish":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#f39c4a' stroke='#a85a12' stroke-width='1.4'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#f39c4a' stroke='#a85a12' stroke-width='1.4'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                % (cx - 2 * k, cy, 10 * k, 7 * k, cx + 7 * k, cy, cx + 14 * k, cy - 7 * k, cx + 14 * k, cy + 7 * k,
                   cx - 7 * k, cy - 2 * k, 1.8 * k, INK))
    if kind == "flower":
        s = []
        for i in range(5):
            a = -math.pi / 2 + i * 2 * math.pi / 5
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#e78fb3' stroke='#a8476f' stroke-width='1.1'/>"
                     % (cx + 7 * k * math.cos(a), cy + 7 * k * math.sin(a), 5.6 * k))
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#f4c430' stroke='#a57c00' stroke-width='1.1'/>" % (cx, cy, 4.4 * k))
        return "".join(s)
    if kind == "heart":
        return ("<path d='M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f Z' "
                "fill='#d9534f' stroke='#8e2a27' stroke-width='1.4'/>"
                % (cx, cy + 11 * k, cx - 16 * k, cy, cx - 9 * k, cy - 14 * k, cx, cy - 5 * k,
                   cx + 9 * k, cy - 14 * k, cx + 16 * k, cy, cx, cy + 11 * k))
    if kind == "duck":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#f4d03f' stroke='#a57c00' stroke-width='1.3'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#f4d03f' stroke='#a57c00' stroke-width='1.3'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e67e22'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                % (cx - 1 * k, cy + 4 * k, 11 * k, 7 * k, cx + 5 * k, cy - 6 * k, 6 * k,
                   cx + 10 * k, cy - 7 * k, cx + 16 * k, cy - 5 * k, cx + 10 * k, cy - 3 * k,
                   cx + 6 * k, cy - 8 * k, 1.4 * k, INK))
    if kind == "cup":
        return ("<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='#9fd3c7' stroke='#2e7d6b' stroke-width='1.5'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#2e7d6b' stroke-width='2'/>"
                % (cx - 10 * k, cy - 10 * k, cx + 8 * k, cy - 10 * k, cx + 6 * k, cy + 11 * k, cx - 8 * k, cy + 11 * k,
                   cx + 7 * k, cy - 5 * k, cx + 15 * k, cy, cx + 6.5 * k, cy + 5 * k))
    if kind == "bug":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#c0392b' stroke='#6e1f17' stroke-width='1.4'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6e1f17' stroke-width='1.4'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/><circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                % (cx, cy + 2 * k, 11 * k, 10 * k, cx, cy - 8 * k, cx, cy + 12 * k,
                   cx, cy - 9 * k, 4.5 * k, INK, cx - 5 * k, cy + 3 * k, 2 * k, INK, cx + 5 * k, cy + 3 * k, 2 * k, INK))
    if kind == "dot":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 10 * k, RED)
    if kind == "cube":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='1.6'/>"
                % (cx - 11 * k, cy - 11 * k, 22 * k, 22 * k, CUBE, GREEN))
    raise ValueError(kind)


CELL, M = 36, 8      # space for one object, margin


def label(kind, how):
    return "%s %s" % (name(kind), how)


def row_svg(n, kind, per_row=10, gap5=True):
    """n objects in rows (default rows of 10, small gap after 5 like a ten-frame)."""
    rows = [per_row] * (n // per_row) + ([n % per_row] if n % per_row else [])
    g = 14 if gap5 and per_row > 5 else 0
    W = 2 * M + min(n, per_row) * CELL + (g if min(n, per_row) > 5 else 0)
    H = 2 * M + len(rows) * CELL
    s = []
    for r, c in enumerate(rows):
        for i in range(c):
            s.append(obj(kind, M + CELL / 2 + i * CELL + (g if i >= 5 else 0), M + CELL / 2 + r * CELL))
    return svg_wrap(W, H, "".join(s), label(kind, "in a row" if len(rows) == 1 else "in rows"))


def array_svg(rows, cols, kind):
    W, H = 2 * M + cols * CELL, 2 * M + rows * CELL
    s = [obj(kind, M + CELL / 2 + c * CELL, M + CELL / 2 + r * CELL) for r in range(rows) for c in range(cols)]
    return svg_wrap(W, H, "".join(s), label(kind, "in an array"))


def circle_svg(n, kind):
    """n objects around a circle (one of them marked as the start with a small green dot)."""
    R = max(46, n * CELL / (2 * math.pi) + 6)
    W = H = int(2 * (R + CELL / 2 + M))
    c = W / 2.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='#bbbbbb' stroke-width='1.2' stroke-dasharray='4 4'/>" % (c, c, R)]
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n
        s.append(obj(kind, c + R * math.cos(a), c + R * math.sin(a)))
    return svg_wrap(W, H, "".join(s), label(kind, "in a circle"))


def scatter_svg(n, kind, seed, cols=None, rows=None):
    """n objects scattered: n cells of a grid picked at random (seeded), each shifted a little.
    The grid grows with n so the picture stays compact."""
    if cols is None:
        cols, rows = (3, 2) if n <= 4 else (3, 3) if n <= 6 else (4, 3) if n <= 9 else (4, 4)
    assert n <= cols * rows
    rnd = random.Random(seed)
    cells = rnd.sample([(r, c) for r in range(rows) for c in range(cols)], n)
    sp = CELL + 8
    W, H = 2 * M + cols * sp, 2 * M + rows * sp
    s = []
    for r, c in cells:
        s.append(obj(kind, M + sp / 2 + c * sp + rnd.uniform(-6, 6), M + sp / 2 + r * sp + rnd.uniform(-6, 6)))
    return svg_wrap(W, H, "".join(s), label(kind, "scattered"))


TF = 34


def tenframe_svg(n, frames=None, kind="dot"):
    """One or two ten-frames; the first fills up before the second."""
    frames = frames or (1 if n <= 10 else 2)
    assert 0 <= n <= 10 * frames
    gap = 18
    W = 2 * M + frames * 5 * TF + (frames - 1) * gap
    H = 2 * M + 2 * TF
    s = []
    for f in range(frames):
        x0 = M + f * (5 * TF + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2.2'/>"
                 % (x0, M, 5 * TF, 2 * TF, GREEN))
        for i in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (x0 + i * TF, M, x0 + i * TF, M + 2 * TF, GREEN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (x0, M + TF, x0 + 5 * TF, M + TF, GREEN))
        for i in range(10):
            if f * 10 + i < n:
                s.append(obj(kind, x0 + (i % 5) * TF + TF / 2, M + (i // 5) * TF + TF / 2, 11))
    return svg_wrap(W, H, "".join(s), "ten-frame" if frames == 1 else "two ten-frames")


def groups_svg(groups, gap=30):
    """Several groups side by side: groups = [(n, kind), ...], each group in rows of up to 5."""
    s = []
    x = M
    H = 0
    for n, kind in groups:
        cols = min(5, max(1, n))
        rows = (n + 4) // 5
        for i in range(n):
            s.append(obj(kind, x + CELL / 2 + (i % 5) * CELL, M + CELL / 2 + (i // 5) * CELL))
        x += cols * CELL + gap
        H = max(H, rows * CELL)
    return svg_wrap(int(x - gap + M), H + 2 * M, "".join(s), "groups of objects")


def lettered_groups_svg(groups, per_row=5):
    """Groups in boxes stacked in a 2 x 2 grid, each with a letter: groups = [(n, kind), ...] (up to 4)."""
    bw = 2 * 6 + per_row * CELL
    rows_max = max((n + per_row - 1) // per_row for n, _ in groups)
    bh = 2 * 6 + rows_max * CELL + 24
    gap = 14
    s = []
    for g, (n, kind) in enumerate(groups):
        x0 = M + (g % 2) * (bw + gap)
        y0 = M + (g // 2) * (bh + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='1.8'/>"
                 % (x0, y0, bw, bh, GREEN))
        s.append(text(x0 + 14, y0 + 20, "ABCD"[g], 18, col=GREEN))
        for i in range(n):
            s.append(obj(kind, x0 + 6 + CELL / 2 + (i % per_row) * CELL, y0 + 24 + 6 + CELL / 2 + (i // per_row) * CELL))
    cols = min(2, len(groups))
    rws = (len(groups) + 1) // 2
    return svg_wrap(2 * M + cols * bw + (cols - 1) * gap, 2 * M + rws * bh + (rws - 1) * gap, "".join(s), "groups A to %s" % "ABCD"[len(groups) - 1])


def number_line_svg(lo, hi, marks=None, sp=40):
    """Number line lo..hi. marks: {value: text or '?'}; default shows every number."""
    n = hi - lo
    m = 26
    W = 2 * m + n * sp
    y = 16
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (6, y, W - 6, y, INK)]
    for v in range(lo, hi + 1):
        x = m + (v - lo) * sp
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 7, x, y + 7, INK))
        t = (marks or {}).get(v, None if marks else str(v))
        if t is not None:
            s.append(text(x, y + 30, t, 18, col=RED if t == "?" else INK))
    return svg_wrap(W, y + 40, "".join(s), "number line from %d to %d" % (lo, hi))


def cards_svg(items, w=50, h=56):
    """A row of number cards. items: list of text ('?' is drawn red on a green card)."""
    gap = 10
    W = 2 * M + len(items) * w + (len(items) - 1) * gap
    s = []
    for i, t in enumerate(items):
        x = M + i * (w + gap)
        q = t == "?"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, M, w, h, FILL if q else "#ffffff", GREEN))
        s.append(text(x + w / 2, M + h / 2 + 9, t, 26, col=RED if q else INK))
    return svg_wrap(W, h + 2 * M, "".join(s), "number cards")


CW, CH = 50, 38


def chart_svg(tl, nrows, ncols, target=None, hide=()):
    """A piece of the hundred chart. tl = top-left number. target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 100
    m = 4
    W, H = 2 * m + ncols * CW, 2 * m + nrows * CH
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CW, m + r * CH
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x, y, CW, CH, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CW / 2, y + 26, "?", 20, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CW / 2, y + 26, str(tl + 10 * r + c), 18))
    return svg_wrap(W, H, "".join(s), "piece of a hundred chart")


def rods_svg(t, o=0, u=9):
    """t ten rods (10 cubes each, standing up) and o single cubes."""
    m, gap = 6, 8
    F = 10 * u
    s = []
    x = m
    for k in range(t):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x, m, u + 2, F, FILL, GREEN))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.8'/>" % (x, m + i * u, x + u + 2, m + i * u, GREEN))
        x += u + 2 + gap
    x += 10 if o else 0
    for k in range(o):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x + (k // 5) * (u + 6), m + F - u - 2 - (k % 5) * (u + 6), u + 2, u + 2, CUBE, GREEN))
    right = x + ((o - 1) // 5 + 1) * (u + 6) if o else x - gap
    return svg_wrap(right + m, F + 2 * m, "".join(s), "ten rods and cubes")


def plate_svg(n, kind, per_row=5):
    """A plate with n objects on it (n can be 0: an empty plate)."""
    rows = max(1, (n + per_row - 1) // per_row)
    cols = per_row if n >= per_row else max(n, 3)
    w = cols * CELL + 40
    h = rows * CELL + 34
    W, H = w + 2 * M, h + 2 * M
    s = ["<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#f7f7f2' stroke='#8a8a80' stroke-width='2'/>"
         % (W / 2, H / 2, w / 2, h / 2),
         "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='none' stroke='#c9c9bf' stroke-width='1.4'/>"
         % (W / 2, H / 2, w / 2 - 9, h / 2 - 8)]
    x0 = W / 2 - min(n, per_row) * CELL / 2
    y0 = H / 2 - rows * CELL / 2
    for i in range(n):
        s.append(obj(kind, x0 + CELL / 2 + (i % per_row) * CELL, y0 + CELL / 2 + (i // per_row) * CELL))
    return svg_wrap(W, H, "".join(s), "a plate with %s" % ("nothing on it" if n == 0 else name(kind, n)))


DICE = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
        5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}


def dice_svg(values):
    """One or more dot cubes (number cubes) side by side."""
    size, gap = 74, 14
    s = []
    for k, v in enumerate(values):
        x0 = M + k * (size + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='12' fill='#ffffff' stroke='%s' stroke-width='2.4'/>"
                 % (x0, M, size, size, INK))
        for cx, cy in DICE[v]:
            s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (x0 + 16 + cx * 21, M + 16 + cy * 21, INK))
    return svg_wrap(2 * M + len(values) * size + (len(values) - 1) * gap, size + 2 * M, "".join(s), "dot cube")


BLUE_DOT = "#1f5fa8"


def match_svg(rows, label_w=None):
    """Rows lined up one under the other so they can be matched one to one.
    rows = [(n, kind, label or '', spacing)], spacing = space per object (default CELL)."""
    lw = label_w if label_w is not None else (70 if any(r[2] for r in rows) else 0)
    W = 0
    s = []
    for i, (n, kind, lab, sp) in enumerate(rows):
        sp = sp or CELL
        y = M + CELL / 2 + i * (CELL + 8)
        if lab:
            s.append(text(M, y + 6, lab, 16, anchor="start", col=GREEN))
        for k in range(n):
            s.append(obj(kind, M + lw + sp / 2 + k * sp, y))
        W = max(W, M + lw + n * sp + M)
    H = 2 * M + len(rows) * (CELL + 8) - 8
    return svg_wrap(int(W), int(H), "".join(s), "rows to compare")


def cross(cx, cy, r=14):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            % (cx - r, cy - r, cx + r, cy + r, INK, cx - r, cy + r, cx + r, cy - r, INK))


def crossed_row_svg(n, kind, k, per_row=5):
    """n objects in rows of per_row; the last k are crossed out (taken away)."""
    rows = (n + per_row - 1) // per_row
    W = 2 * M + min(n, per_row) * CELL
    H = 2 * M + rows * CELL
    s = []
    for i in range(n):
        cx, cy = M + CELL / 2 + (i % per_row) * CELL, M + CELL / 2 + (i // per_row) * CELL
        s.append(obj(kind, cx, cy))
        if i >= n - k:
            s.append(cross(cx, cy))
    return svg_wrap(W, H, "".join(s), "%s, %d crossed out" % (name(kind), k))


def tenframe_mix_svg(cells, frames=None):
    """Ten-frame(s) from a list of cell marks: 'r' red dot, 'b' blue dot, 'x' red dot crossed out, '' empty."""
    n = len(cells)
    frames = frames or (1 if n <= 10 else 2)
    gap = 18
    W = 2 * M + frames * 5 * TF + (frames - 1) * gap
    H = 2 * M + 2 * TF
    s = []
    for f in range(frames):
        x0 = M + f * (5 * TF + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2.2'/>"
                 % (x0, M, 5 * TF, 2 * TF, GREEN))
        for i in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (x0 + i * TF, M, x0 + i * TF, M + 2 * TF, GREEN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (x0, M + TF, x0 + 5 * TF, M + TF, GREEN))
        for i in range(10):
            j = f * 10 + i
            if j >= n or not cells[j]:
                continue
            cx, cy = x0 + (i % 5) * TF + TF / 2, M + (i // 5) * TF + TF / 2
            col = BLUE_DOT if cells[j] == "b" else RED
            s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='%s'/>" % (cx, cy, col))
            if cells[j] == "x":
                s.append(cross(cx, cy, 12))
    return svg_wrap(W, H, "".join(s), "ten-frame")


def two_groups_svg(a, ka, b, kb=None, word="and"):
    """Two groups side by side with a word or sign between them (each group in rows of up to 5)."""
    kb = kb or ka
    s = []
    x = M
    hmax = 0
    for idx, (n, kind) in enumerate([(a, ka), (b, kb)]):
        cols = min(5, max(1, n))
        rows = max(1, (n + 4) // 5)
        for i in range(n):
            s.append(obj(kind, x + CELL / 2 + (i % 5) * CELL, M + CELL / 2 + (i // 5) * CELL))
        x += cols * CELL
        hmax = max(hmax, rows * CELL)
        if idx == 0:
            s.append("<!--mid-->")
            mid_x = x + 26
            x += 52
    H = hmax + 2 * M
    s = [t if t != "<!--mid-->" else text(mid_x, H / 2 + 7, word, 20 if len(word) == 1 else 16, col=GREEN) for t in s]
    return svg_wrap(int(x + M), int(H), "".join(s), "%d %s %s %d %s" % (a, name(ka, a), word, b, name(kb, b)))


def box_svg(n, kind, per_row=5):
    """n objects next to a closed box with a ? on it (some are hidden in the box)."""
    rows = max(1, (n + per_row - 1) // per_row)
    cols = min(n, per_row)
    s = []
    for i in range(n):
        s.append(obj(kind, M + CELL / 2 + (i % per_row) * CELL, M + CELL / 2 + (i // per_row) * CELL))
    bx = M + cols * CELL + 18
    bh = max(rows * CELL, 56)
    s.append("<rect x='%d' y='%d' width='70' height='%d' rx='6' fill='#d9b27c' stroke='#8a6233' stroke-width='2'/>" % (bx, M, bh))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#8a6233' stroke-width='2'/>" % (bx, M + 14, bx + 70, M + 14))
    s.append(text(bx + 35, M + bh / 2 + 16, "?", 26, col=RED))
    return svg_wrap(bx + 70 + M, bh + 2 * M, "".join(s), "%s and a closed box" % name(kind))


def hop_line_svg(start, hops, lo=0, hi=10, sp=40):
    """Number line lo..hi with a red dot at start and `hops` equal hops of 1 (right if hops > 0, left if < 0)."""
    m = 22
    W = 2 * m + (hi - lo) * sp
    y = 58
    X = lambda v: m + (v - lo) * sp
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (4, y, W - 4, y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), y - 7, X(v), y + 7, INK))
        s.append(text(X(v), y + 28, str(v), 17))
    d = 1 if hops > 0 else -1
    for k in range(abs(hops)):
        a, b = start + d * k, start + d * (k + 1)
        xa, xb = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='#1f5fa8' stroke-width='2.5'/>"
                 % (xa, y - 4, (xa + xb) / 2, y - 46, xb, y - 4))
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='#1f5fa8'/>" % (xb, y - 3, xb - 8 * d, y - 12, xb - 2 * d, y - 13))
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(start), y, RED))
    return svg_wrap(W, y + 38, "".join(s), "number line from %d to %d with hops" % (lo, hi))
