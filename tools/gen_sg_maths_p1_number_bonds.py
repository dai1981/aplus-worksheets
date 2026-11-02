# -*- coding: utf-8 -*-
"""
SG Primary 1 Maths: Number bonds (MOE 2021 Primary Mathematics Syllabus, Primary 1: Addition and Subtraction)
  python3 tools/gen_sg_maths_p1_number_bonds.py
Number bonds to 10 and to 20 (whole and two parts in circles), finding the missing part,
fact families from a number bond and Singapore word problems. Every answer and picture count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
CRED = "#d9443a"
CGREEN = "#3fa34d"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
BOX = "□"
QB = "<b>□</b>"
C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", pink="#e86aa6", brown="#c68a4a", grey="#555555", white="#ffffff")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique, positive distractors. Positions are set later."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def abcd(q, right, e):
    return {"q": q, "c": ["A", "B", "C", "D"], "a": "ABCD".index(right), "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures (rows of objects, number lines, ten frames, A-D grids) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def ev(expr):
    """Value of '8 − 1', '4 + 1', '6'."""
    toks = expr.split()
    v = int(toks[0])
    for op, n in zip(toks[1::2], toks[2::2]):
        assert op in ("+", MINUS), expr
        v = v + int(n) if op == "+" else v - int(n)
    return v


def eq_true(eq):
    lhs, rhs = eq.split(" = ")
    return ev(lhs) == ev(rhs)


def solve_box(eq):
    ok = [n for n in range(0, 41) if eq_true(eq.replace(BOX, str(n)))]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


def on_list(a, b):
    return ", ".join(str(a + i) for i in range(1, b + 1))


def u(n, sing, plur):
    return "%d %s" % (n, sing if n == 1 else plur)


NAMES = dict(apple=("apple", "apples"), star=("star sticker", "star stickers"), ball=("ball", "balls"),
             flower=("flower", "flowers"), block=("block", "blocks"), balloon=("balloon", "balloons"),
             car=("toy car", "toy cars"), fish=("fish", "fish"), child=("child", "children"),
             sweet=("sweet", "sweets"), orange=("mandarin orange", "mandarin oranges"), marble=("marble", "marbles"))


def nm(n, kind):
    s, p = NAMES[kind]
    return u(n, s, p)


# ------------------------------------------------------------ pictures: objects (each fits a 28 x 28 cell)
PITCH = 28
DEF_COL = dict(apple="red", star="gold", fish="orange", ball="blue", flower="pink", block="green", balloon="purple",
               car="blue", child="blue", sweet="pink", orange="orange", marble="blue")


def obj(kind, cx, cy, colour=None):
    col = C[colour or DEF_COL[kind]]
    s = "<g data-o='1'>"
    if kind == "apple":
        s += ("<path d='M%.1f %.1f q1 -4 3 -5' fill='none' stroke='#7a4a1e' stroke-width='2'/>" % (cx, cy - 7)
              + "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
              % (cx + 5, cy - 10, C["green"], cx + 5, cy - 10)
              + "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 1, col, INK))
    elif kind == "orange":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 2, col, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='5' ry='2.4' fill='%s' stroke='%s' stroke-width='0.8' "
                "transform='rotate(-25 %.1f %.1f)'/>" % (cx + 4, cy - 8, C["green"], INK, cx + 4, cy - 8)
              + "<circle cx='%.1f' cy='%.1f' r='1.3' fill='%s'/>" % (cx, cy - 7, INK))
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 11 if k % 2 == 0 else 4.6
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
        s += "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), col, INK)
    elif kind == "fish":
        s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx + 3, cy, cx + 11, cy - 6.5, cx + 11, cy + 6.5, col, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='8' ry='6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx - 3, cy, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx - 7, cy - 1.5, INK))
    elif kind == "ball":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
              + "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='1.8'/>"
              % (cx - 9, cy - 2, cx, cy + 5, cx + 9, cy - 2))
    elif kind == "marble":
        s += ("<circle cx='%.1f' cy='%.1f' r='8' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='2.4' fill='#ffffff' opacity='0.8'/>" % (cx - 3, cy - 3))
    elif kind == "flower":
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            s += "<circle cx='%.1f' cy='%.1f' r='4.6' fill='%s' stroke='%s' stroke-width='0.8'/>" % (
                cx + 5.6 * math.cos(a), cy + 5.6 * math.sin(a), col, INK)
        s += "<circle cx='%.1f' cy='%.1f' r='3.4' fill='%s' stroke='%s' stroke-width='0.8'/>" % (cx, cy, C["yellow"], INK)
    elif kind == "block":
        s += ("<rect x='%.1f' y='%.1f' width='19' height='19' rx='3' fill='%s' stroke='%s' stroke-width='1.4'/>"
              % (cx - 9.5, cy - 9.5, col, INK))
    elif kind == "balloon":
        s += ("<path d='M%.1f %.1f q-2 4 1 7' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy + 6, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (cx, cy + 4, cx - 2, cy + 7, cx + 2, cy + 7, col)
              + "<ellipse cx='%.1f' cy='%.1f' rx='7' ry='8.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 3, col, INK))
    elif kind == "car":
        s += ("<rect x='%.1f' y='%.1f' width='10' height='6' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 5, cy - 7, col, INK)
              + "<rect x='%.1f' y='%.1f' width='21' height='8' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 10.5, cy - 2, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx - 6, cy + 6.5, INK)
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx + 6, cy + 6.5, INK))
    elif kind == "child":
        s += ("<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s' stroke='%s' stroke-width='1'/>" % (cx, cy - 7, "#d9a77c", INK)
              + "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1'/>"
              % (cx - 9, cy + 12, cx, cy - 6, cx + 9, cy + 12, col, INK))
    elif kind == "sweet":
        s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1'/>"
              % (cx - 6, cy, cx - 12, cy - 5, cx - 12, cy + 5, col, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1'/>"
              % (cx + 6, cy, cx + 12, cy - 5, cx + 12, cy + 5, col, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='7' ry='5.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK))
    else:
        raise ValueError(kind)
    return s + "</g>"


def cross(cx, cy, col=INK):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - 10, cy - 10, cx + 10, cy + 10, col, cx - 10, cy + 10, cx + 10, cy - 10, col))


def row_x(x0, c):
    """Centre of column c in a row, with a small gap after every 5."""
    return x0 + c * PITCH + PITCH / 2 + 8 * (c // 5)


def row_w(n):
    return n * PITCH + 8 * ((n - 1) // 5)


def group_body(x0, y0, n, kind, cols=5, colour=None):
    s, centres = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx, cy = row_x(x0, c), y0 + r * PITCH + PITCH / 2
        centres.append((cx, cy))
        s.append(obj(kind, cx, cy, colour))
    w = row_w(min(n, cols))
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centres


def two_groups_svg(a, b, kind, c2=None):
    """Two groups with a + between them."""
    assert 1 <= a <= 10 and 1 <= b <= 10
    o, gap = 6, 34
    b1, w1, h1, _ = group_body(o, o, a, kind)
    b2, w2, h2, _ = group_body(o + w1 + gap, o, b, kind, colour=c2)
    H = o + max(h1, h2) + o
    W = o + w1 + gap + w2 + o
    body = b1 + text(o + w1 + gap / 2, H / 2 + 8, "+", 24) + b2
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), body, "picture: %s and %s" % (nm(a, kind), nm(b, kind)))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def take_svg(n, k, kind):
    """n objects in rows of 10 (gap after 5); the last k are crossed out."""
    o = 6
    body, w, h, cen = group_body(o, o, n, kind, cols=10)
    col = INK if DEF_COL[kind] in ("red", "pink", "orange") else RED
    xs = "".join(cross(cx, cy, col) for cx, cy in cen[n - k:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %s, %d crossed out" % (nm(n, kind), k))
    assert svg.count("<g data-o='1'>") == n and svg.count("<g data-x='1'>") == k
    return svg


def row_svg(n, kind, colours):
    """n objects in one row (gap after 5). colours: list of (count, colour)."""
    o = 6
    cols = [c for m, c in colours for _ in range(m)]
    assert len(cols) == n
    s = [obj(kind, row_x(o, i), o + PITCH / 2, cc) for i, cc in enumerate(cols)]
    lab = "picture: " + " and ".join("%d %s" % (m, c) for m, c in colours) + " " + NAMES[kind][1]
    svg = svg_wrap(int(row_w(n) + 2 * o + 0.99), PITCH + 2 * o, "".join(s), lab)
    assert svg.count("<g data-o='1'>") == n
    return svg


def need_svg(have, total, kind, colours=None):
    """`total` spots in a row (gap after 5): `have` objects, then dashed empty circles."""
    assert 1 <= have < total <= 12
    o = 6
    cols = [c for m, c in colours for _ in range(m)] if colours else [None] * have
    assert len(cols) == have
    s = []
    for i in range(total):
        cx, cy = row_x(o, i), o + PITCH / 2
        if i < have:
            s.append(obj(kind, cx, cy, cols[i]))
        else:
            s.append("<circle data-e='1' cx='%.1f' cy='%.1f' r='10' fill='none' stroke='%s' stroke-width='2' "
                     "stroke-dasharray='4 3'/>" % (cx, cy, INK))
    svg = svg_wrap(int(row_w(total) + 2 * o + 0.99), PITCH + 2 * o, "".join(s),
                   "picture: %s and %s" % (nm(have, kind), u(total - have, "empty spot", "empty spots")))
    assert svg.count("<g data-o='1'>") == have and svg.count("data-e='1'") == total - have
    return svg


def hidden_svg(shown, kind):
    """`shown` objects in rows of 5, and a closed box with ? on it (some objects are inside)."""
    o, gap, bw = 6, 22, 64
    body, w, h, _ = group_body(o, o, shown, kind)
    H = max(h, bw) + 2 * o
    bx, by = o + w + gap, (H - bw) / 2
    box = ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2.5'/>"
           % (bx, by, bw, bw, "#e9c58f", INK)
           + "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
           % (bx, by + 16, bx + bw, by + 16, INK)
           + text(bx + bw / 2, by + 48, "?", 26, col=RED))
    svg = svg_wrap(int(bx + bw + o + 0.99), int(H + 0.99), body + box,
                   "picture: %s and a box with some inside" % nm(shown, kind))
    assert svg.count("<g data-o='1'>") == shown
    return svg


# ------------------------------------------------------------ number bond, ten frames, number line
def bond_body(x0, y0, whole, a, b, side=False, r=26, fs=20):
    """Number bond: the whole (shaded) joined to two parts. Values may be '?'."""
    if side:
        top, p1, p2 = (x0 + r + 8, y0 + 72), (x0 + r + 100, y0 + r + 2), (x0 + r + 100, y0 + 142 - r)
    else:
        sx = r / 26.0
        top = (x0 + 88 * sx, y0 + r + 6)
        p1, p2 = (x0 + (r + 8), y0 + r + 6 + 72 * sx), (x0 + 176 * sx - r - 8, y0 + r + 6 + 72 * sx)
    s = []
    for p in (p1, p2):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                 % (top[0], top[1], p[0], p[1], INK))
    for (cx, cy), v, fill in [(top, whole, FILL), (p1, a, "#fff"), (p2, b, "#fff")]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + fs * 0.35, str(v), fs, col=RED if v == "?" else INK))
    return "".join(s)


def pw_svg(whole, a, b, side=False):
    """A number bond. side=False: whole on top; side=True: whole on the left."""
    if "?" not in (whole, a, b):
        assert a + b == whole
    W, H = (160, 156) if side else (176, 136)
    return svg_wrap(W, H, bond_body(0, 0, whole, a, b, side),
                    "number bond: whole %s, parts %s and %s" % (whole, a, b))


def bonds_abcd_svg(bonds):
    """Four small number bonds in a 2 x 2 grid, labelled A to D."""
    assert len(bonds) == 4
    o, lw, gx, gy, bw, bh = 6, 24, 20, 12, 150, 116
    s = []
    for i, (w, a, b) in enumerate(bonds):
        r_, c_ = divmod(i, 2)
        x = o + c_ * (lw + bw + gx)
        y = o + r_ * (bh + gy)
        s.append(text(x + 8, y + 30, "ABCD"[i], 18, col=GREEN))
        s.append(bond_body(x + lw, y - 6 + 2, w, a, b, r=22, fs=18))
    W = o + 2 * (lw + bw) + gx + o
    H = o + 2 * bh + gy + o
    return svg_wrap(W, H, "".join(s), "number bonds A to D: " + ", ".join(
        "whole %d, parts %d and %d" % t for t in bonds))


CELL = 30
FW, FH = 5 * CELL, 2 * CELL


def frame(x0, y0, colours):
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + CELL, x0 + FW, y0 + CELL, INK))
    for k, col in enumerate(colours):
        r, c = divmod(k, 5)
        s.append("<circle data-c='1' cx='%d' cy='%d' r='10' fill='%s'/>"
                 % (x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2, col))
    return "".join(s)


def two_frames_svg(n):
    """Two ten frames: the first full (red), the second with n - 10 green counters."""
    assert 11 <= n <= 19
    o, gap = 6, 16
    body = frame(o, o, [CRED] * 10) + frame(o + FW + gap, o, [CGREEN] * (n - 10))
    svg = svg_wrap(2 * FW + gap + 2 * o, FH + 2 * o, body, "two ten frames with %d counters" % n)
    assert svg.count("data-c='1'") == n
    return svg


def number_line_svg(lo, hi, start, qhop, step=30):
    """Number line lo..hi with a green dot on `start` and a hop to qhop[1] labelled ?."""
    L, Y = 18, 66
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    a, b = qhop
    assert lo <= a < b <= hi and a == start
    mid = (X(a) + X(b)) / 2
    s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (X(a), Y - 9, mid, Y - 54, X(b), Y - 9, GREEN))
    s.append(text(mid, Y - 36, "?", 16, col=RED))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, GREEN))
    return svg_wrap(W, Y + 34, "".join(s), "number line from %d to %d with a hop from %d to %d" % (lo, hi, a, b))


# ============================================================ set 1: number bonds to 10
def set_to_10():
    its = []
    for w, known, left in [(10, 7, True), (8, 2, False), (9, 4, True), (7, 3, False), (6, 1, True), (10, 9, False)]:
        k = w - known
        pic = pw_svg(w, known, "?") if left else pw_svg(w, "?", known)
        e = "The whole is %d. One part is %d. %d and %d make %d. The missing part is <b>%d</b>." % (
            w, known, known, k, w, k)
        its.append(mcq(fig(pic) + "What is the missing part?", k, [w + known, known, w, k + 1, k - 1], e))

    for a, b in [(4, 3), (5, 4), (2, 6)]:
        q = fig(pw_svg("?", a, b)) + "The parts are %d and %d. What is the whole?" % (a, b)
        e = "Put the parts together. %d + %d = <b>%d</b>." % (a, b, a + b)
        its.append(mcq(q, a + b, [abs(a - b), a + b - 1, a + b + 1], e))

    for kind, a, b, ca, cb in [("ball", 5, 3, "blue", "red"), ("flower", 4, 2, "pink", "yellow"),
                               ("apple", 6, 3, "red", "green"), ("balloon", 3, 4, "purple", "orange"),
                               ("star", 7, 3, "gold", "blue")]:
        w = a + b
        right = "%d and %d" % (a, b)
        wrong = ["%d and %d" % (a, b + 1), "%d and %d" % (a + 1, b), "%d and %d" % (a - 1, b)]
        assert len({right} | set(wrong)) == 4
        q = fig(row_svg(w, kind, [(a, ca), (b, cb)])) + "There are %d %s. Which two parts make %d?" % (
            w, NAMES[kind][1], w)
        e = "Count each colour: %d %s and %d %s. %d + %d = %d. So <b>%s</b>." % (a, ca, b, cb, a, b, w, right)
        its.append(mcq(q, right, wrong, e))

    for bonds, right in [([(8, 5, 4), (8, 5, 3), (8, 6, 3), (8, 4, 3)], "B"),
                         ([(9, 5, 3), (9, 7, 1), (9, 3, 5), (9, 6, 3)], "D"),
                         ([(7, 4, 3), (7, 5, 3), (7, 2, 4), (7, 6, 2)], "A")]:
        idx = "ABCD".index(right)
        assert [w == a + b for w, a, b in bonds].count(True) == 1 and bonds[idx][0] == bonds[idx][1] + bonds[idx][2]
        w, a, b = bonds[idx]
        others = ", ".join("%s: %d + %d = %d" % ("ABCD"[i], x[1], x[2], x[1] + x[2]) for i, x in enumerate(bonds) if i != idx)
        q = fig(bonds_abcd_svg(bonds)) + "Which number bond is correct?"
        e = "The parts must add up to the whole. %s: %d + %d = %d. So <b>%s</b>. (%s.)" % (right, a, b, w, right, others)
        its.append(abcd(q, right, e))

    for w, right, wrong in [(9, "6 and 3", ["6 and 4", "5 and 3", "9 and 1"]),
                            (7, "5 and 2", ["5 and 3", "4 and 2", "7 and 1"]),
                            (8, "4 and 4", ["4 and 5", "3 and 4", "8 and 1"])]:
        a, b = [int(x) for x in right.split(" and ")]
        assert a + b == w and all(sum(int(x) for x in c.split(" and ")) != w for c in wrong)
        q = fig(pw_svg(w, "?", "?")) + "Which two parts make %d?" % w
        e = "%d + %d = %d. So <b>%s</b> make %d." % (a, b, w, right, w)
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 10", "items": its}


# ============================================================ set 2: number bonds to 20
def set_to_20():
    its = []
    for n, left in [(13, True), (17, False), (11, True), (15, False), (19, True)]:
        k = n - 10
        pic = pw_svg(n, 10, "?") if left else pw_svg(n, "?", 10)
        e = "%d is 10 and %d. 10 + %d = %d. The missing part is <b>%d</b>." % (n, k, k, n, k)
        its.append(mcq(fig(pic) + "What is the missing part?", k, [n + 10, n, k + 1, k - 1, k + 2], e))

    for n in [14, 16, 12, 18]:
        k = n - 10
        right = "%d is 10 and %d" % (n, k)
        wrong = ["%d is 10 and %d" % (n + 1, k + 1), "%d is 10 and %d" % (n, k + 1), "%d is 1 and %d" % (n, k)]
        q = fig(two_frames_svg(n)) + "Count the counters. Which number bond is it?"
        e = "One full ten frame is 10. The other has %d. 10 + %d = %d. So <b>%s</b>." % (k, k, n, right)
        its.append(mcq(q, right, wrong, e))

    for w, known in [(12, 7), (14, 6), (16, 9), (11, 8), (15, 6)]:
        k = w - known
        pic = pw_svg(w, known, "?") if w % 2 == 0 else pw_svg(w, "?", known)
        e = "Count on from %d to %d: %s. That is %d. So the missing part is <b>%d</b>." % (
            known, w, on_list(known, k), k, k)
        its.append(mcq(fig(pic) + "What is the missing part?", k, [w + known, known, k + 1, k - 1], e))

    for a, b in [(8, 5), (9, 7), (6, 6)]:
        q = fig(pw_svg("?", a, b)) + "The parts are %d and %d. What is the whole?" % (a, b)
        e = "Put the parts together. %d + %d = <b>%d</b>." % (a, b, a + b)
        its.append(mcq(q, a + b, [abs(a - b), a + b - 1, a + b + 1, a], e))

    for bonds, right in [([(13, 9, 3), (14, 8, 5), (12, 6, 6), (15, 7, 7)], "C"),
                         ([(16, 10, 6), (17, 9, 7), (18, 10, 7), (11, 5, 5)], "A"),
                         ([(15, 8, 8), (19, 10, 8), (13, 6, 8), (14, 9, 5)], "D")]:
        idx = "ABCD".index(right)
        assert [w == a + b for w, a, b in bonds].count(True) == 1 and bonds[idx][0] == bonds[idx][1] + bonds[idx][2]
        w, a, b = bonds[idx]
        others = ", ".join("%s: %d + %d = %d" % ("ABCD"[i], x[1], x[2], x[1] + x[2]) for i, x in enumerate(bonds) if i != idx)
        q = fig(bonds_abcd_svg(bonds)) + "Which number bond is correct?"
        e = "Add the parts. %s: %d + %d = %d. So <b>%s</b>. (%s.)" % (right, a, b, w, right, others)
        its.append(abcd(q, right, e))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 20", "items": its}


# ============================================================ set 3: missing part
def set_missing():
    its = []

    def miss(eq, known, whole, pic, e, ask="Find the missing number.<br>"):
        r = solve_box(eq)
        cands = [whole + known, known, r + 1, r - 1, r + 2]
        for w_ in cands:
            if w_ != r and w_ > 0:
                assert not eq_true(eq.replace(BOX, str(w_))), (eq, w_)
        its.append(mcq(fig(pic) + ask + eq.replace(BOX, QB), r, cands, e))

    for w, a in [(12, 8), (9, 3), (15, 8), (13, 7), (17, 9)]:
        k = w - a
        miss("%d + %s = %d" % (a, BOX, w), a, w, pw_svg(w, a, "?", side=True),
             "The whole is %d. One part is %d. %d + %d = %d. So %s is <b>%d</b>." % (w, a, a, k, w, BOX, k))
    for w, a in [(11, 5), (14, 9), (16, 8), (13, 4), (10, 3)]:
        k = w - a
        miss("%d %s %d = %s" % (w, MINUS, a, BOX), a, w, pw_svg(w, a, "?"),
             "Take a part from the whole. %d and %d make %d, so %d %s %d = <b>%d</b>." % (a, k, w, w, MINUS, a, k))
    for total, shown, kind in [(11, 7, "star"), (14, 8, "sweet"), (12, 9, "ball"), (16, 10, "block"),
                               (13, 6, "flower")]:
        k = total - shown
        q = fig(hidden_svg(shown, kind)) + "There are %d %s in all. Some are in the box. How many are in the box?" % (
            total, NAMES[kind][1])
        e = "You can see %d. %d and %d make %d. So <b>%d</b> are in the box." % (shown, shown, k, total, k)
        its.append(mcq(q, k, [total + shown, shown, k + 1, k - 1], e))
    for a, w in [(6, 13), (9, 14), (8, 17), (5, 11), (11, 19)]:
        k = w - a
        miss("%d + %s = %d" % (a, BOX, w), a, w, number_line_svg(a - 1, w + 1, a, (a, w)),
             "Count on from %d to %d: %s. You said %d numbers. %d + <b>%d</b> = %d." % (
                 a, w, on_list(a, k), k, a, k, w))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing part", "items": its}


# ============================================================ set 4: fact families
def set_families():
    its = []
    for w, a, b in [(9, 5, 4), (12, 8, 4), (15, 9, 6), (11, 7, 4), (14, 6, 8)]:
        right = "%d + %d = %d" % (a, b, w)
        wrong = ["%d + %d = %d" % (w, a, w + a), "%d + %d = %d" % (w, b, w + b), "%d + %d = %d" % (a, b, w + 1)]
        q = fig(pw_svg(w, a, b)) + "Which addition sentence goes with this number bond?"
        e = "Add the two parts to get the whole: <b>%s</b>. Do not add the whole and a part." % right
        its.append(mcq(q, right, wrong, e))

    for w, a, b in [(8, 5, 3), (13, 9, 4), (16, 7, 9), (10, 6, 4), (17, 8, 9)]:
        right = "%d %s %d = %d" % (w, MINUS, a, b)
        hi, lo = max(a, b), min(a, b)
        wrong = ["%d %s %d = %d" % (hi, MINUS, lo, hi - lo), "%d %s %d = %d" % (w, MINUS, a, b + 1),
                 "%d %s %d = %d" % (w, MINUS, b, b)]
        assert not any(w_ == right for w_ in wrong)
        q = fig(pw_svg(w, a, b)) + "Which subtraction sentence goes with this number bond?"
        e = "Start with the whole. Take away one part. The other part is left: <b>%s</b>." % right
        its.append(mcq(q, right, wrong, e))

    fams = [(9, 5, 4, ["5 + 4 = 9", "4 + 5 = 9", "9 − 5 = 4", "9 − 4 = □"]),
            (12, 7, 5, ["7 + 5 = 12", "5 + 7 = 12", "12 − 5 = 7", "12 − 7 = □"]),
            (14, 8, 6, ["8 + 6 = 14", "6 + 8 = 14", "14 − 8 = 6", "□ − 6 = 8"]),
            (16, 9, 7, ["9 + 7 = 16", "16 − 7 = 9", "16 − 9 = 7", "7 + □ = 16"]),
            (13, 10, 3, ["10 + 3 = 13", "3 + 10 = 13", "13 − 3 = 10", "13 − □ = 3"])]
    for w, a, b, lines in fams:
        for ln in lines[:3]:
            assert eq_true(ln) and set(int(x) for x in re.findall(r"\d+", ln)) == {w, a, b}, ln
        last = lines[3]
        r = solve_box(last)
        assert r in (w, a, b)
        known = [int(x) for x in re.findall(r"\d+", last)]
        cands = [sum(known), known[0], r + 1, r - 1]
        for c_ in cands:
            assert c_ == r or not eq_true(last.replace(BOX, str(c_)))
        q = fig(pw_svg(w, a, b)) + "Complete the fact family.<br>" + "<br>".join(lines[:3]) + "<br>" + last.replace(BOX, QB)
        e = "The bond is %d: %d and %d. Every sentence uses these 3 numbers. %s." % (
            w, a, b, last.replace(BOX, "<b>%d</b>" % r))
        its.append(mcq(q, r, cands, e))

    for sent, (w, a, b), right in [("8 + 5 = 13", (13, 8, 5), "A"), ("14 − 6 = 8", (14, 6, 8), "C"),
                                   ("7 + 4 = 11", (11, 7, 4), "D"), ("15 − 9 = 6", (15, 9, 6), "B"),
                                   ("6 + 10 = 16", (16, 6, 10), "C")]:
        assert eq_true(sent) and a + b == w
        good = (w, a, b)
        bad = [(w, a, b + 1), (b, w, a), (w + a, w, a)]
        idx = "ABCD".index(right)
        bonds = bad[:idx] + [good] + bad[idx:]
        assert len(set(bonds)) == 4
        q = fig(bonds_abcd_svg(bonds)) + "Which number bond goes with %s?" % sent
        e = "In %s, the whole is %d and the parts are %d and %d. The whole goes on top. So <b>%s</b>." % (
            sent, w, a, b, right)
        its.append(abcd(q, right, e))
    assert len(its) == 20, len(its)
    return {"title": "Fact families from a number bond", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def word(q, ans, wrong, e, pic):
        its.append(mcq(fig(pic) + q, ans, wrong, e))

    word("Ali has 6 red balloons and 4 blue balloons. How many balloons does he have?", 10, [2, 9, 11],
         "6 and 4 make 10. 6 + 4 = <b>10</b>.", two_groups_svg(6, 4, "balloon", "blue"))
    word("Mei Ling has 9 star stickers. She gets 5 more. How many does she have now?", 14, [4, 13, 15],
         "9 and 5 make 14. 9 + 5 = <b>14</b>.", two_groups_svg(9, 5, "star"))
    word("13 children play at the void deck. 8 wear red. The rest wear blue. How many wear blue?", 5,
         [21, 8, 6, 4], "13 is 8 and 5. 13 %s 8 = <b>5</b>." % MINUS,
         row_svg(13, "child", [(8, "red"), (5, "blue")]))
    word("Raju has 15 marbles. 6 are in his hand. The rest are in a box. How many are in the box?", 9,
         [21, 6, 10, 8], "15 is 6 and 9. 6 + 9 = 15. So <b>9</b> are in the box.", hidden_svg(6, "marble"))
    word("Hui Min has 14 sweets. She eats 6. How many sweets are left?", 8, [20, 6, 9, 7],
         "14 is 6 and 8. 14 %s 6 = <b>8</b>." % MINUS, take_svg(14, 6, "sweet"))
    word("12 children are on a bus. 5 get off at the MRT station. How many are still on the bus?", 7,
         [17, 5, 8, 6], "12 is 5 and 7. 12 %s 5 = <b>7</b>." % MINUS, take_svg(12, 5, "child"))
    word("Wei Ming reads 7 books in the June holidays. Jun Jie reads 6 books. How many books do they read in all?",
         13, [1, 12, 14], "7 and 6 make 13. 7 + 6 = <b>13</b>.", pw_svg("?", 7, 6))
    word("Xin Yi has 16 mandarin oranges. She gives 9 to her grandma. How many are left?", 7, [25, 9, 8, 6],
         "16 is 9 and 7. 16 %s 9 = <b>7</b>." % MINUS, take_svg(16, 9, "orange"))
    word("Devi puts out 11 oil lamps for Deepavali. 3 are big. The rest are small. How many are small?", 8,
         [14, 3, 9, 7], "11 is 3 and 8. 11 %s 3 = <b>8</b>." % MINUS, pw_svg(11, 3, "?"))
    word("There are 17 pupils in a group. 9 go to the library. The rest go to the field. How many go to the field?",
         8, [26, 9, 7, 10], "17 is 9 and 8. 17 %s 9 = <b>8</b>." % MINUS, pw_svg(17, 9, "?"))
    word("At the Singapore Zoo, Chloe sees 5 monkeys in a tree and 7 on the ground. How many monkeys does she see in all?",
         12, [2, 11, 13], "5 and 7 make 12. 5 + 7 = <b>12</b>.", pw_svg("?", 5, 7))
    word("Kumar has 18 blocks. Some are in a box. He can see 10. How many blocks are in the box?", 8,
         [28, 10, 9, 7], "18 is 10 and 8. So <b>8</b> blocks are in the box.", hidden_svg(10, "block"))
    word("Farah has 13 flowers. 4 are red. The rest are yellow. How many are yellow?", 9, [17, 4, 10, 8],
         "13 is 4 and 9. 13 %s 4 = <b>9</b>." % MINUS, row_svg(13, "flower", [(4, "red"), (9, "yellow")]))
    word("Hafiz has 7 toy cars. He wants 12. How many more toy cars does he need?", 5, [19, 7, 6, 4],
         "12 is 7 and 5. 7 + 5 = 12. He needs <b>5</b> more.", need_svg(7, 12, "car"))
    word("Ryan and Sarah have 15 balls in all. Ryan has 8 balls. How many balls does Sarah have?", 7,
         [23, 8, 6, 9], "15 is 8 and 7. 8 + 7 = 15. Sarah has <b>7</b> balls.", pw_svg(15, 8, "?"))
    word("Nurul has 9 apples. Ahmad gives her 6 more. How many apples does she have now?", 15, [3, 14, 16],
         "9 and 6 make 15. 9 + 6 = <b>15</b>.", two_groups_svg(9, 6, "apple"))
    word("Zhi Hao has 4 red toy cars and 5 blue toy cars. How many more does he need to have 12?", 3, [9, 8, 21, 4],
         "Step 1: 4 + 5 = 9. Step 2: 12 is 9 and 3. He needs <b>3</b> more.",
         need_svg(9, 12, "car", [(4, "red"), (5, "blue")]))
    word("Kavya has 12 star stickers. 7 are gold. The rest are blue. She says 19 are blue. She is wrong. How many are blue?",
         5, [19, 6, 4, 7], "Do not add the whole and a part. 12 is 7 and 5. So <b>5</b> are blue.",
         row_svg(12, "star", [(7, "gold"), (5, "blue")]))
    word("Mrs Lim has 20 bottles of water for Sports Day. She gives out 11. How many are left?", 9,
         [31, 11, 10, 8], "20 is 11 and 9. 20 %s 11 = <b>9</b>." % MINUS, pw_svg(20, 11, "?"))
    word("Jun Jie has 8 star stickers. He gets 4 more. Then he gives 5 to Ali. How many are left?", 7,
         [12, 17, 3, 8], "Step 1: 8 + 4 = 12. Step 2: 12 %s 5 = <b>7</b>." % MINUS, two_groups_svg(8, 4, "star"))
    assert len(its) == 20, len(its)
    return {"title": "Number bond word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a number bond?</h2>"
        "<p>A number bond shows a whole and two parts.</p>"
        "<p>The whole goes in the top circle. The parts go in the circles below.</p>"
        "<p>The two parts make the whole.</p>"
        "<figure class='sn-fig'>" + row_svg(7, "apple", [(4, "red"), (3, "green")]) +
        "<figcaption>4 red apples and 3 green apples. 7 apples in all.</figcaption></figure>"
        "<figure class='sn-fig'>" + pw_svg(7, 4, 3) +
        "<figcaption>7 is 4 and 3. 4 + 3 = 7.</figcaption></figure>"
        + "<h2>Number bonds to 10</h2>"
        + table(["Whole", "Parts"], [["10", "%d and %d" % (a, 10 - a)] for a in range(1, 6)])
        + "<h2>Number bonds to 20</h2>"
        "<p>A number from 11 to 20 is 10 and some more.</p>"
        "<figure class='sn-fig'>" + two_frames_svg(14) +
        "<figcaption>14 is 10 and 4.</figcaption></figure>"
        + ex("Example", "What is the missing part? Whole 13, one part 8.",
             "Count on from 8: 9, 10, 11, 12, 13. That is 5. 8 + 5 = 13.", "5")
        + "<h2>Fact family</h2>"
        "<p>One number bond gives four number sentences.</p>"
        "<figure class='sn-fig'>" + pw_svg(9, 5, 4) +
        "<figcaption>5 + 4 = 9, 4 + 5 = 9, 9 − 5 = 4, 9 − 4 = 5.</figcaption></figure>"
        + ex("Example", "Siti has 12 sweets. 7 are red. The rest are green. How many are green?",
             "12 is 7 and 5. 12 − 7 = 5.", "5 green sweets")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Whole 10, part 4: “the missing part is 14”", "Do not add the whole and a part. 10 is 4 and 6"],
            ["6 + 5 = 10", "6 + 5 = 11. The partner of 6 in 10 is 4"],
            ["Putting the whole in a bottom circle", "The whole is the biggest number. It goes on top"],
            ["Counting 8, 9, 10, 11 to get 4 for 8 + □ = 11", "Do not count the 8. Say 9, 10, 11. That is 3"],
        ])
    )


FAQ = [
    {"q": "What is a number bond in P1 maths?",
     "a": "A number bond shows how a whole splits into two parts, such as 10 is 7 and 3. Primary 1 students use number bonds to add and subtract within 20."},
    {"q": "How do I teach number bonds to my child?",
     "a": "Start with real things, like 8 buttons split into two groups. Then draw the circles and ask which part is missing. A few minutes a day helps."},
    {"q": "What is the most common mistake with number bonds?",
     "a": "Many children add the whole and a part, so whole 10 and part 4 gives 14. Remind them that the parts are smaller than the whole."},
    {"q": "Are number bonds in the MOE syllabus?",
     "a": "Yes. The MOE Primary 1 syllabus teaches addition and subtraction with number bonds and the link between them. They are also used later for mental maths."},
]


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), (s["title"], [it["a"] for it in s["items"]])
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.fullmatch(r"\d+", c) for c in it["c"]):
                assert all(0 < int(c) <= 40 for c in it["c"]), it["c"]
            key = re.sub(r"<[^>]+>", " ", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            assert it["q"].count("<svg") <= 1
            for t in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in t and '"' not in t and ".." not in t, t
                assert not re.search(r"(?<![\d$])\b1 (?!is\b|was\b)[a-z]+s\b", re.sub(r"<[^>]+>", " ", t)), t
            last = re.sub(r"<[^>]+>", "", re.split(r"<br>", it["q"])[-1]).strip()
            if re.fullmatch(r"[\d□]+( [+−] [\d□]+)* = [\d□]+( [+−] [\d□]+)*", last) and last.count(BOX) == 1:
                assert it["c"][it["a"]] == str(solve_box(last)), (last, it["c"])
            right = it["c"][it["a"]]
            if re.fullmatch(r"\d+ [+−] \d+ = \d+", right):
                assert eq_true(right), right
            # number bond pictures: the parts must add up to the whole
            m = re.search(r"aria-label='number bond: whole (\d+), parts (\d+) and (\d+)'", it["q"])
            if m:
                assert int(m.group(1)) == int(m.group(2)) + int(m.group(3)), m.group(0)
            for m in re.finditer(r"aria-label='two ten frames with (\d+) counters'", it["q"]):
                assert it["q"].count("data-c='1'") == int(m.group(1))
            plain = re.sub(r"<svg.*?</svg>", "", it["q"])
            for n in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", plain)):
                assert int(n) <= 20, it["q"]


def gen():
    rnd = random.Random(61803)
    sets = [set_to_10(), set_to_20(), set_missing(), set_families(), set_words()]
    for s in sets:
        fixed = [it["a"] for it in s["items"] if it.get("fixed")]
        free = [it for it in s["items"] if not it.get("fixed")]
        targets = [0, 1, 2, 3] * 5
        for a in fixed:
            targets.remove(a)
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)
    check(sets)
    u_ = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "number-bonds",
        "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Number Bonds",
        "seo_title": "P1 Number Bonds Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Number bonds",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Addition and Subtraction",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Concepts of addition and subtraction; relationship between addition and subtraction",
        "meta_desc": "Free P1 maths practice on number bonds to 10 and 20: missing parts, fact families and "
                     "word problems with pictures. 100 questions with answers.",
        "key_big": "A number bond shows a whole and two parts. The two parts make the whole.",
        "key_sub": "10 is 7 and 3, so 7 + 3 = 10 and 10 − 7 = 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u_["meta_desc"]) <= 160, len(u_["meta_desc"])
    return mark_large(u_, "picture|number line|number bonds A|two ten frames")


if __name__ == "__main__":
    u_ = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u_["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u_, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
