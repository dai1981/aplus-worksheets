# -*- coding: utf-8 -*-
"""
CA-BC Grade 1 Math: Ways to make 10 (BC Mathematics Curriculum, Grade 1: Number)
  python3 tools/gen_cabc_math_g1_make_10.py
Ten frames (how many more make 10), number bonds to 10, pairs that make 10,
missing parts (7 + □ = 10) and BC word problems. Every answer and picture count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
CRED = "#d9443a"
CGREEN = "#3fa34d"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
Q = "<b>?</b>"
C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", pink="#e86aa6", brown="#c68a4a", grey="#555555", white="#ffffff")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique, positive distractors. Positions are set later by balance()."""
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
    """Tag wide pictures (rows of objects, number lines, cube trains) so they print larger."""
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


def solve(eq):
    """The one whole number 0-30 that makes eq (with one ?) true."""
    ok = [n for n in range(0, 31) if eq_true(eq.replace("?", str(n)))]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


def on_list(a, b):
    return ", ".join(str(a + i) for i in range(1, b + 1))


def back_list(a, b):
    return ", ".join(str(a - i) for i in range(1, b + 1))


def u(n, sing, plur):
    return "%d %s" % (n, sing if n == 1 else plur)


NAMES = dict(apple=("apple", "apples"), star=("star", "stars"), ball=("ball", "balls"), flower=("flower", "flowers"),
             block=("block", "blocks"), balloon=("balloon", "balloons"), car=("toy car", "toy cars"),
             duck=("duck", "ducks"), fish=("fish", "fish"), puck=("puck", "pucks"), child=("child", "children"),
             snowball=("snowball", "snowballs"), crayon=("crayon", "crayons"))


def nm(n, kind):
    s, p = NAMES[kind]
    return u(n, s, p)


# ------------------------------------------------------------ pictures: objects (each fits a 28 x 28 cell)
PITCH = 28
DEF_COL = dict(apple="red", star="gold", fish="orange", ball="blue", flower="pink", block="green", balloon="purple",
               car="blue", duck="yellow", puck="grey", child="blue", snowball="white", crayon="blue")


def obj(kind, cx, cy, colour=None):
    col = C[colour or DEF_COL[kind]]
    s = "<g data-o='1'>"
    if kind == "apple":
        s += ("<path d='M%.1f %.1f q1 -4 3 -5' fill='none' stroke='#7a4a1e' stroke-width='2'/>" % (cx, cy - 7)
              + "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
              % (cx + 5, cy - 10, C["green"], cx + 5, cy - 10)
              + "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 1, col, INK))
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
    elif kind == "duck":
        s += ("<ellipse cx='%.1f' cy='%.1f' rx='9' ry='6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx + 2, cy + 4, col, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='0.8'/>"
              % (cx - 7.5, cy - 6, cx - 11.5, cy - 4.5, cx - 7.5, cy - 3, C["orange"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='4.6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx - 4, cy - 5, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.1' fill='%s'/>" % (cx - 4.5, cy - 6, INK))
    elif kind == "puck":
        s += ("<ellipse cx='%.1f' cy='%.1f' rx='10' ry='5' fill='%s'/>" % (cx, cy + 4, INK)
              + "<rect x='%.1f' y='%.1f' width='20' height='6' fill='%s'/>" % (cx - 10, cy - 2, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 2, col, INK))
    elif kind == "child":
        s += ("<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s' stroke='%s' stroke-width='1'/>" % (cx, cy - 7, "#f1c9a5", INK)
              + "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1'/>"
              % (cx - 9, cy + 12, cx, cy - 6, cx + 9, cy + 12, col, INK))
    elif kind == "snowball":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#ffffff' stroke='%s' stroke-width='1.6'/>" % (cx, cy, C["blue"])
              + "<circle cx='%.1f' cy='%.1f' r='2' fill='#cfe0f5'/>" % (cx - 3, cy - 3))
    elif kind == "crayon":
        s += ("<rect x='%.1f' y='%.1f' width='16' height='8' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 10, cy - 4, col, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx + 6, cy - 4, cx + 12, cy, cx + 6, cy + 4, col, INK))
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
    """n objects in one row (gap after 5); the last k are crossed out."""
    o = 6
    body, w, h, cen = group_body(o, o, n, kind, cols=10)
    col = INK if DEF_COL[kind] == "red" else RED
    xs = "".join(cross(cx, cy, col) for cx, cy in cen[n - k:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %s, %d crossed out" % (nm(n, kind), k))
    assert svg.count("<g data-o='1'>") == n and svg.count("<g data-x='1'>") == k
    return svg


def row_svg(n, kind, colours=None):
    """n objects in one row (no plus sign). colours: list of (count, colour)."""
    o = 6
    s = []
    cols = [c for m, c in colours for _ in range(m)] if colours else [None] * n
    assert len(cols) == n
    for i, cc in enumerate(cols):
        s.append(obj(kind, row_x(o, i), o + PITCH / 2, cc))
    svg = svg_wrap(int(row_w(n) + 2 * o + 0.99), PITCH + 2 * o, "".join(s), "picture: %s in a row" % nm(n, kind))
    assert svg.count("<g data-o='1'>") == n
    return svg


def compare_svg(n1, name1, n2, name2, kind):
    """Two rows lined up, one object above the other, so the extra ones stand out."""
    o, lw = 6, 62
    rows = []
    for r, (n, name) in enumerate([(n1, name1), (n2, name2)]):
        y = o + r * (PITCH + 8)
        rows.append(text(o, y + PITCH / 2 + 6, name, 15, anchor="start"))
        for c in range(n):
            rows.append(obj(kind, row_x(o + lw, c), y + PITCH / 2))
    W = o + lw + row_w(max(n1, n2)) + o
    H = o + 2 * PITCH + 8 + o
    svg = svg_wrap(int(W + 0.99), int(H), "".join(rows),
                   "picture: %s has %s, %s has %s" % (name1, nm(n1, kind), name2, nm(n2, kind)))
    assert svg.count("<g data-o='1'>") == n1 + n2
    return svg


# ------------------------------------------------------------ pictures: number line, ten frame, part-whole, dominoes, cubes
def number_line_svg(lo, hi, start=None, hops=(), qhop=None, step=30):
    """Number line lo..hi. start: green dot. hops: (from, to) arcs with +n / −n. qhop: (from, to) arc labelled ?."""
    arcs = list(hops) + ([qhop] if qhop else [])
    L, Y = 18, 66 if arcs else 22
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    for k, (a, b) in enumerate(arcs):
        assert lo <= min(a, b) and max(a, b) <= hi
        mid = (X(a) + X(b)) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (X(a), Y - 9, mid, Y - 54, X(b), Y - 9, GREEN))
        lab = "?" if (qhop and k == len(arcs) - 1) else ("+%d" if b > a else MINUS + "%d") % abs(b - a)
        s.append(text(mid, Y - 36, lab, 16, col=RED if lab == "?" else GREEN))
    label = "number line from %d to %d" % (lo, hi)
    if start is not None:
        assert lo <= start <= hi
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, GREEN))
        label += " with a green dot on %d" % start
    if qhop:
        label += " and a hop from %d to %d" % qhop
    return svg_wrap(W, Y + 34, "".join(s), label)


CELL = 30
FW, FH = 5 * CELL, 2 * CELL


def frame(x0, y0, colours, crossed=0):
    """A ten frame. colours: one colour per counter. The last `crossed` counters get a cross."""
    assert len(colours) <= 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + CELL, x0 + FW, y0 + CELL, INK))
    for k, col in enumerate(colours):
        r, c = divmod(k, 5)
        cx, cy = x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2
        s.append("<circle data-c='1' cx='%d' cy='%d' r='10' fill='%s'/>" % (cx, cy, col))
        if k >= len(colours) - crossed:
            s.append("<g data-x='1'><line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
                     "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/></g>"
                     % (cx - 11, cy - 11, cx + 11, cy + 11, INK, cx + 11, cy - 11, cx - 11, cy + 11, INK))
    return "".join(s)


def frame_svg(a, b=0, crossed=0):
    """One ten frame: a red then b green counters; the last `crossed` counters get an X."""
    assert a + b <= 10
    o = 6
    lab = "ten frame with %d red%s counters" % (a, " and %d green" % b if b else "")
    if crossed:
        lab += ", %d crossed out" % crossed
    svg = svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, [CRED] * a + [CGREEN] * b, crossed), lab)
    assert svg.count("data-c='1'") == a + b and svg.count("data-x='1'") == crossed
    return svg


def pw_svg(whole, a, b):
    """Part-whole model: the whole on top, two parts below. Values may be '?'."""
    W, H, r = 176, 136, 26
    top, left, right = (88, 32), (34, 104), (142, 104)
    s = []
    for p in (left, right):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (top[0], top[1], p[0], p[1], INK))
    for (cx, cy), v, fill in [(top, whole, FILL), (left, a, "#fff"), (right, b, "#fff")]:
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    if "?" not in (whole, a, b):
        assert a + b == whole
    return svg_wrap(W, H, "".join(s), "part-whole model: whole %s, parts %s and %s" % (whole, a, b))


PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)],
        4: [(0, 0), (2, 0), (0, 2), (2, 2)], 5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
        6: [(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2)]}


def domino_body(x0, y0, a, b, half=60):
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, 2 * half, half, INK),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
         % (x0 + half, y0 + 6, x0 + half, y0 + half - 6, INK)]
    step = half // 4
    for k, n in enumerate((a, b)):
        for cx, cy in PIPS[n]:
            s.append("<circle data-p='1' cx='%d' cy='%d' r='6' fill='%s'/>"
                     % (x0 + k * half + step * (cx + 1), y0 + step * (cy + 1), INK))
    return "".join(s)


def domino_svg(a, b):
    o = 6
    svg = svg_wrap(120 + 2 * o, 60 + 2 * o, domino_body(o, o, a, b), "domino with %d and %d dots" % (a, b))
    assert svg.count("data-p='1'") == a + b
    return svg


def dominoes_abcd_svg(pairs):
    """Four dominoes in a 2 x 2 grid, labelled A, B, C, D."""
    assert len(pairs) == 4
    o, lw, gx, gy = 6, 22, 22, 14
    s = []
    for i, (a, b) in enumerate(pairs):
        r, c = divmod(i, 2)
        x = o + c * (lw + 120 + gx)
        y = o + r * (60 + gy)
        s.append(text(x + 8, y + 37, "ABCD"[i], 18, col=GREEN))
        s.append(domino_body(x + lw, y, a, b))
    W = o + 2 * (lw + 120) + gx + o
    H = o + 2 * 60 + gy + o
    svg = svg_wrap(W, H, "".join(s), "dominoes A to D: " + ", ".join("%d and %d" % p for p in pairs))
    assert svg.count("data-p='1'") == sum(a + b for a, b in pairs)
    return svg


def cubes_svg(a, b):
    """A train of a red then b blue cubes."""
    n = a + b
    o, size = 6, 26
    s = []
    for i in range(n):
        col = C["red"] if i < a else C["blue"]
        s.append("<rect data-q='1' x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (o + i * size, o, size, size, col, INK))
    svg = svg_wrap(n * size + 2 * o, size + 2 * o, "".join(s), "cube train: %d red and %d blue cubes" % (a, b))
    assert svg.count("data-q='1'") == n
    return svg



# ------------------------------------------------------------ extra pictures for making 10
BOX = "□"
QB = "<b>□</b>"
NAMES.update(salmon=("salmon", "salmon"), sticker=("sticker", "stickers"))


def need_svg(have, kind, colours=None):
    """10 spots in a row (gap after 5): `have` objects, then dashed empty circles."""
    assert 1 <= have <= 9
    o = 6
    cols = [c for m, c in colours for _ in range(m)] if colours else [None] * have
    assert len(cols) == have
    s = []
    for i in range(10):
        cx, cy = row_x(o, i), o + PITCH / 2
        if i < have:
            s.append(obj(kind, cx, cy, cols[i]))
        else:
            s.append("<circle data-e='1' cx='%.1f' cy='%.1f' r='10' fill='none' stroke='%s' stroke-width='2' "
                     "stroke-dasharray='4 3'/>" % (cx, cy, INK))
    svg = svg_wrap(int(row_w(10) + 2 * o + 0.99), PITCH + 2 * o, "".join(s),
                   "picture: %s and %s" % (nm(have, kind), u(10 - have, "empty spot", "empty spots")))
    assert svg.count("<g data-o='1'>") == have and svg.count("data-e='1'") == 10 - have
    return svg


def cubes_gap_svg(a):
    """a red cubes, then dashed outlines up to 10."""
    o, size = 6, 26
    s = []
    for i in range(10):
        if i < a:
            s.append("<rect data-q='1' x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (o + i * size, o, size, size, C["red"], INK))
        else:
            s.append("<rect data-e='1' x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2' "
                     "stroke-dasharray='4 3'/>" % (o + i * size + 2, o + 2, size - 4, size - 4, INK))
    svg = svg_wrap(10 * size + 2 * o, size + 2 * o, "".join(s), "cube train: %s and %s" % (u(a, "red cube", "red cubes"), u(10 - a, "empty space", "empty spaces")))
    assert svg.count("data-q='1'") == a and svg.count("data-e='1'") == 10 - a
    return svg


def frames_abcd_svg(frames):
    """Four ten frames in a 2 x 2 grid, labelled A to D. frames: (red, green) counts."""
    assert len(frames) == 4
    o, lw, gx, gy = 6, 22, 22, 14
    s = []
    for i, (a, b) in enumerate(frames):
        r, c = divmod(i, 2)
        x = o + c * (lw + FW + gx)
        y = o + r * (FH + gy)
        s.append(text(x + 8, y + FH / 2 + 7, "ABCD"[i], 18, col=GREEN))
        s.append(frame(x + lw, y, [CRED] * a + [CGREEN] * b))
    W = o + 2 * (lw + FW) + gx + o
    H = o + 2 * FH + gy + o
    svg = svg_wrap(W, H, "".join(s), "ten frames A to D: " + ", ".join(
        "%d red and %d green" % (a, b) if b else "%d red" % a for a, b in frames))
    assert svg.count("data-c='1'") == sum(a + b for a, b in frames)
    return svg


def cards_svg(nums):
    """Number cards in a row."""
    o, cw, ch, gap = 6, 40, 50, 10
    s = []
    for i, n in enumerate(nums):
        x = o + i * (cw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#fff' stroke='%s' stroke-width='2.5'/>"
                 % (x, o, cw, ch, GREEN))
        s.append(text(x + cw / 2, o + ch / 2 + 8, str(n), 22))
    W = o + len(nums) * cw + (len(nums) - 1) * gap + o
    return svg_wrap(W, ch + 2 * o, "".join(s), "number cards: " + ", ".join(str(n) for n in nums))


def abcd(q, right, e):
    it = {"q": q, "c": ["A", "B", "C", "D"], "a": "ABCD".index(right), "e": e, "fixed": True}
    return it


def more_e(n, k):
    return "A ten frame has 10 boxes. %d %s full. Count the empty boxes: <b>%d</b>. %d + %d = 10." % (
        n, "box is" if n == 1 else "boxes are", k, n, k)


def ev2(expr):
    return ev(expr)


def solve_box(eq):
    ok = [n for n in range(1, 21) if eq_true(eq.replace(BOX, str(n)))]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


# ============================================================ set 1: ten frames
def set_frames():
    its = []
    for n in [7, 5, 8, 3, 9, 6, 2, 4, 1]:
        k = 10 - n
        q = fig(frame_svg(n)) + "How many more counters make 10?"
        its.append(mcq(q, k, [n, 10 + n, k + 1, k - 1, k + 2], more_e(n, k)))

    for n in [7, 4, 8]:
        k = 10 - n
        right = "%d + %d" % (n, k)
        wrong = ["%d + %d" % (n, k + 1), "%d + %d" % (n, k - 1), "%d + %d" % (n, n)]
        vals = [ev(right)] + [ev(w) for w in wrong]
        assert vals[0] == 10 and len(set(vals)) == 4, vals
        q = fig(frame_svg(n)) + "Which one makes 10?"
        e = "%d counters and %d empty boxes. %d + %d = 10. So <b>%s</b> makes 10." % (n, k, n, k, right)
        its.append(mcq(q, right, wrong, e))

    for a, b in [(5, 2), (3, 3), (4, 2), (6, 1), (2, 5)]:
        k = 10 - a - b
        q = fig(frame_svg(a, b)) + "%d red. %d green. How many more make 10?" % (a, b)
        e = "%d + %d = %d counters. %d boxes are empty. %d + %d = 10. So <b>%d</b> more." % (
            a, b, a + b, k, a + b, k, k)
        its.append(mcq(q, k, [a + b, 10 - a, 10 - b, k + 1, k - 1], e))

    for frames, right, need in [([(3, 0), (7, 0), (6, 0), (4, 0)], "B", 3),
                                ([(5, 0), (8, 0), (2, 0), (6, 0)], "C", 8),
                                ([(4, 0), (9, 0), (5, 0), (6, 0)], "D", 4)]:
        idx = "ABCD".index(right)
        assert 10 - frames[idx][0] == need and sum(1 for f in frames if 10 - f[0] == need) == 1
        q = fig(frames_abcd_svg(frames)) + "Which ten frame needs %d more to make 10?" % need
        e = "Count the empty boxes. Frame %s has %d counters and %d empty boxes. %d + %d = 10. So <b>%s</b>." % (
            right, frames[idx][0], need, frames[idx][0], need, right)
        its.append(abcd(q, right, e))
    assert len(its) == 20, len(its)
    return {"title": "Ten frames: how many more make 10?", "items": its}


# ============================================================ set 2: number bonds to 10
def set_bonds():
    its = []
    for known, left in [(8, True), (3, False), (6, True), (1, False), (5, True), (9, False), (2, True),
                        (7, False), (4, True)]:
        k = 10 - known
        pic = pw_svg(10, known, "?") if left else pw_svg(10, "?", known)
        e = "The whole is 10. One part is %d. %d + %d = 10. The missing part is <b>%d</b>." % (known, known, k, k)
        its.append(mcq(fig(pic) + "What is the missing part?", k, [10 + known, known, k + 1, k - 1], e))

    for a, b in [(6, 4), (3, 7)]:
        q = fig(pw_svg("?", a, b)) + "The parts are %d and %d. What is the whole?" % (a, b)
        e = "Put the parts together. %d + %d = <b>10</b>." % (a, b)
        its.append(mcq(q, 10, [abs(a - b), 9, 11], e))

    for a, b in [(6, 4), (2, 8), (9, 1), (5, 5)]:
        q = fig(cubes_svg(a, b)) + "There are 10 cubes. %d are red. How many are blue?" % a
        e = "%d + %d = 10. Count the blue cubes: <b>%d</b>." % (a, b, b)
        its.append(mcq(q, b, [10 + a, b + 1, b - 1, a], e))

    for kind, a, b, ca, cb in [("flower", 4, 6, "pink", "yellow"), ("ball", 7, 3, "blue", "red"),
                               ("balloon", 2, 8, "purple", "orange"), ("star", 3, 7, "gold", "blue"),
                               ("apple", 6, 4, "green", "red")]:
        right = "%d and %d" % (a, b)
        wrong = ["%d and %d" % (a, b - 1), "%d and %d" % (a + 1, b), "%d and %d" % (a - 1, b) if a > 1 else "%d and %d" % (a, b + 1)]
        assert len({right} | set(wrong)) == 4
        q = fig(row_svg(10, kind, [(a, ca), (b, cb)])) + "Which number bond to 10 does it show?"
        e = "Count each colour. %d %s and %d %s. %d + %d = 10. So <b>%s</b>." % (a, ca, b, cb, a, b, right)
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 10", "items": its}


# ============================================================ set 3: pairs that make 10
def set_pairs():
    its = []
    for right, wrong in [("6 + 4", ["6 + 5", "5 + 4", "3 + 5"]), ("3 + 7", ["3 + 8", "3 + 6", "2 + 6"]),
                         ("8 + 2", ["8 + 3", "7 + 2", "6 + 1"]), ("1 + 9", ["2 + 9", "1 + 8", "1 + 7"]),
                         ("5 + 5", ["5 + 6", "5 + 4", "4 + 4"]), ("2 + 8", ["2 + 9", "2 + 7", "1 + 6"])]:
        vals = [ev(right)] + [ev(w) for w in wrong]
        assert vals[0] == 10 and len(set(vals)) == 4, (right, vals)
        a, b = right.split(" + ")
        q = fig(pw_svg(10, "?", "?")) + "Which pair makes 10?"
        e = "%s = 10. So <b>%s</b> makes 10. The others make %s." % (
            right, right, ", ".join(str(v) for v in vals[1:]))
        its.append(mcq(q, right, wrong, e))

    for pairs, right in [([(4, 5), (6, 3), (4, 6), (6, 5)], "C"),
                         ([(5, 5), (5, 4), (6, 5), (3, 5)], "A"),
                         ([(6, 3), (3, 4), (5, 6), (6, 4)], "D")]:
        idx = "ABCD".index(right)
        sums = [a + b for a, b in pairs]
        assert sums[idx] == 10 and sums.count(10) == 1
        a, b = pairs[idx]
        others = ", ".join("%s makes %d" % ("ABCD"[i], s) for i, s in enumerate(sums) if i != idx)
        q = fig(dominoes_abcd_svg(pairs)) + "Which domino has 10 dots?"
        e = "Domino %s has %d and %d. %d + %d = 10. So <b>%s</b>. %s." % (right, a, b, a, b, right, others)
        its.append(abcd(q, right, e))

    for cards, with_n in [([2, 3, 4, 8], 7), ([5, 7, 6, 3], 4), ([1, 9, 8, 2], 9)]:
        k = 10 - with_n
        assert k in cards and sum(1 for c in cards if c + with_n == 10) == 1
        wrong = [c for c in cards if c != k]
        q = fig(cards_svg(cards)) + "Which card goes with %d to make 10?" % with_n
        e = "%d + %d = 10. So the card is <b>%d</b>." % (with_n, k, k)
        its.append(mcq(q, k, wrong, e))

    for a, b in [(2, 8), (7, 3)]:
        eq = "%d + %s = 10" % (b, BOX)
        assert solve_box(eq) == a
        q = fig(cubes_svg(a, b)) + "%d + %d = 10. So %d + %s = 10." % (a, b, b, QB)
        e = "Turn the pair around. %d + %d = 10 and %d + <b>%d</b> = 10." % (a, b, b, a)
        its.append(mcq(q, a, [b, 10 + b, a + 1, a - 1], e))

    q = fig(frame_svg(5, 5)) + "Use the same number twice.<br>%s + %s = 10" % (QB, QB)
    its.append(mcq(q, 5, [10, 4, 6], "5 red and 5 green. 5 + 5 = 10. The number is <b>5</b>."))

    for frames, right in [([(6, 3), (4, 6), (5, 4), (7, 2)], "B"), ([(3, 6), (2, 7), (8, 2), (5, 3)], "C"),
                          ([(9, 1), (4, 4), (6, 3), (2, 6)], "A")]:
        idx = "ABCD".index(right)
        sums = [a + b for a, b in frames]
        assert sums[idx] == 10 and sums.count(10) == 1
        a, b = frames[idx]
        q = fig(frames_abcd_svg(frames)) + "Which ten frame shows a way to make 10?"
        e = "Frame %s is full: %d red and %d green. %d + %d = 10. So <b>%s</b>." % (right, a, b, a, b, right)
        its.append(abcd(q, right, e))

    for name, a, b in [("Hana", 6, 5), ("Ryan", 7, 4)]:
        k = 10 - a
        right = "%d + %d = 10" % (a, k)
        wrong = ["%d + %d = 10" % (a, b), "%d + %d = 10" % (a, a), "%d + %d = 10" % (b, k)]
        assert eq_true(right) and not any(eq_true(w) for w in wrong)
        assert len({ev(x.split(" = ")[0]) for x in [right] + wrong}) == 4
        pro = "She" if name == "Hana" else "He"
        q = fig(frame_svg(a, k)) + "%s says %d + %d = 10. %s is wrong. Which is right?" % (name, a, b, pro)
        e = "%d + %d = %d, not 10. Look at the frame: %d red and %d green fill it. <b>%s</b>." % (
            a, b, a + b, a, k, right)
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Pairs that make 10", "items": its}


# ============================================================ set 4: missing part
def set_missing():
    its = []

    def miss(eq, pic, e):
        r = solve_box(eq)
        nums = [int(x) for x in re.findall(r"\d+", eq) if x != "10"]
        known = nums[0]
        cands = [10 + known, known, r + 1, r - 1, r + 2]
        for w in cands:
            if w != r and w > 0:
                assert not eq_true(eq.replace(BOX, str(w))), (eq, w)
        its.append(mcq(fig(pic) + "Find the missing number.<br>" + eq.replace(BOX, QB), r, cands, e))

    for n in [7, 4, 9]:
        k = 10 - n
        miss("%d + %s = 10" % (n, BOX), cubes_gap_svg(n),
             "%d cubes. %s empty. %d + <b>%d</b> = 10." % (n, u(k, "space is", "spaces are"), n, k))
    for n in [6, 2, 8]:
        k = 10 - n
        miss("%d + %s = 10" % (n, BOX), number_line_svg(0, 10, qhop=(n, 10)),
             "Count on from %d to 10: %s. You said %d numbers. %d + <b>%d</b> = 10." % (
                 n, on_list(n, k), k, n, k))
    for n in [3, 5, 1]:
        k = 10 - n
        miss("%s + %d = 10" % (BOX, n), pw_svg(10, "?", n),
             "The whole is 10. One part is %d. %d + %d = 10. So %s is <b>%d</b>." % (n, k, n, BOX, k))
    for kind, n in [("puck", 6), ("flower", 8), ("duck", 2), ("balloon", 5)]:
        k = 10 - n
        miss("%s + %d = 10" % (BOX, n), need_svg(n, kind),
             "%d %s. %s empty. <b>%d</b> + %d = 10." % (n, NAMES[kind][1], u(k, "spot is", "spots are"), k, n))
    for n in [7, 3, 9]:
        k = 10 - n
        miss("10 = %d + %s" % (n, BOX), pw_svg(10, n, "?"),
             "10 is the whole. %d and %d make 10. 10 = %d + <b>%d</b>." % (n, k, n, k))
    for n in [6, 3, 8, 4]:
        k = 10 - n
        miss("10 %s %d = %s" % (MINUS, n, BOX), frame_svg(10, crossed=n),
             "10 counters. %d have an X. %d are left. %d + %d = 10, so 10 %s %d = <b>%d</b>." % (
                 n, k, n, k, MINUS, n, k))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing part", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def word(q, ans, wrong, e, pic):
        its.append(mcq(fig(pic) + q, ans, wrong, e))

    word("Liam has 6 hockey pucks. He wants 10. How many more does he need?", 4, [6, 16, 5, 3],
         "6 + %s = 10. 6 + 4 = 10. He needs <b>4</b> more." % BOX, need_svg(6, "puck"))
    word("Ava sees 8 ducks at Stanley Park. 2 more swim over. How many ducks now?", 10, [6, 9, 11],
         "8 + 2 = <b>10</b>.", two_groups_svg(8, 2, "duck"))
    word("Mei has 3 star stickers. Her card holds 10. How many more fill it?", 7, [3, 13, 6, 8],
         "3 + %s = 10. 3 + 7 = 10. She needs <b>7</b> more." % BOX, need_svg(3, "star"))
    word("Noah kicks 5 soccer balls. Owen kicks 5. How many balls in all?", 10, [9, 11, 6],
         "5 + 5 = <b>10</b>. It is a double.", two_groups_svg(5, 5, "ball", "red"))
    word("Arjun picks 7 apples in the Okanagan. He wants 10. How many more?", 3, [7, 17, 4, 2],
         "7 + %s = 10. 7 + 3 = 10. He needs <b>3</b> more." % BOX, need_svg(7, "apple"))
    word("Kai builds a tower with 4 blocks. It needs 10. How many more blocks?", 6, [4, 14, 7, 5],
         "4 + %s = 10. 4 + 6 = 10. He needs <b>6</b> more." % BOX, need_svg(4, "block"))
    word("Chloe has 10 crayons. She gives 3 to Zara. How many are left?", 7, [13, 3, 6, 8],
         "Take away 3. 10 %s 3 = <b>7</b>. Check: 3 + 7 = 10." % MINUS, take_svg(10, 3, "crayon"))
    word("Sofia counts 10 salmon in the river. 4 are red. The rest are silver. How many are silver?", 6,
         [4, 14, 5, 7], "4 + %s = 10. 4 + 6 = 10. So <b>6</b> are silver." % BOX,
         row_svg(10, "fish", [(4, "red"), (6, "grey")]))
    word("Mateo has 8 flowers. He wants 10 for his mom. How many more?", 2, [8, 18, 3, 1],
         "8 + %s = 10. 8 + 2 = 10. He needs <b>2</b> more." % BOX, need_svg(8, "flower"))
    word("Hana makes 10 snowballs on Grouse Mountain. One melts. How many are left?", 9, [11, 8, 10],
         "Take away 1. 10 %s 1 = <b>9</b>. Check: 9 + 1 = 10." % MINUS, take_svg(10, 1, "snowball"))
    word("3 cars drive onto a BC Ferry. Then 7 more drive on. How many cars?", 10, [4, 9, 11],
         "3 + 7 = <b>10</b>.", two_groups_svg(3, 7, "car"))
    word("There are 10 seats at the table. 9 children sit down. How many seats are empty?", 1, [9, 19, 2],
         "9 + %s = 10. 9 + 1 = 10. <b>1</b> seat is empty." % BOX, need_svg(9, "child"))
    word("10 children go on a field trip. 6 ride in a van. The rest walk. How many walk?", 4, [6, 16, 5, 3],
         "6 + %s = 10. 6 + 4 = 10. So <b>4</b> walk." % BOX, row_svg(10, "child", [(6, "blue"), (4, "orange")]))
    word("Leah has 5 toy cars. Ethan has some too. They have 10 in all. How many does Ethan have?", 5,
         [15, 4, 6], "5 + %s = 10. 5 + 5 = 10. Ethan has <b>5</b>." % BOX, need_svg(5, "car"))
    word("Jasleen has 10 stickers. 2 are gold. The rest are blue. How many are blue?", 8, [2, 12, 7, 9],
         "2 + %s = 10. 2 + 8 = 10. So <b>8</b> are blue." % BOX, row_svg(10, "star", [(2, "gold"), (8, "blue")]))
    word("10 students run in the Terry Fox Run. 7 have finished. How many are still running?", 3,
         [7, 17, 4, 2], "7 + %s = 10. 7 + 3 = 10. <b>3</b> are still running." % BOX,
         row_svg(10, "child", [(7, "green"), (3, "blue")]))
    word("Simran has 2 balloons. Her dad gives her 8 more. How many balloons now?", 10, [6, 9, 11],
         "2 + 8 = <b>10</b>.", two_groups_svg(2, 8, "balloon"))
    word("Ryan has 4 apples. He picks 2 more. How many more does he need to have 10?", 4,
         [6, 8, 16, 5], "Step 1: 4 + 2 = 6. Step 2: 6 + 4 = 10. He needs <b>4</b> more.",
         need_svg(6, "apple", [(4, "red"), (2, "green")]))
    word("Harjot has 3 red blocks and 4 blue blocks. How many more blocks make 10?", 3,
         [7, 6, 17, 4], "Step 1: 3 + 4 = 7. Step 2: 7 + 3 = 10. He needs <b>3</b> more.",
         need_svg(7, "block", [(3, "red"), (4, "blue")]))
    word("Lucas has 6 balls. He thinks 6 + 5 = 10. How many more balls make 10?", 4, [5, 16, 3],
         "6 + 5 = 11, not 10. Count the empty spots. 6 + 4 = 10. He needs <b>4</b> more.",
         need_svg(6, "ball"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: make 10", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What does “make 10” mean?</h2>"
        "<p>Two numbers make 10 when they add up to 10.</p>"
        "<p>A ten frame has 10 boxes. The full boxes are one part. The empty boxes are the other part.</p>"
        "<figure class='sn-fig'>" + frame_svg(7) +
        "<figcaption>7 counters and 3 empty boxes. 7 + 3 = 10.</figcaption></figure>"
        + ex("Example", "How many more make 10? The ten frame has 6 counters.",
             "Count the empty boxes: 4. 6 + 4 = 10.", "4")
        + "<h2>Number bonds to 10</h2>"
        "<p>A number bond shows a whole and two parts. The whole is 10.</p>"
        "<figure class='sn-fig'>" + pw_svg(10, 8, 2) +
        "<figcaption>10 is 8 and 2. 8 + 2 = 10.</figcaption></figure>"
        + table(["Pairs that make 10", "Turned around"],
                [["%d + %d" % (a, 10 - a), "%d + %d" % (10 - a, a)] for a in range(1, 6)])
        + "<h2>Find the missing part</h2>"
        "<p>Think: what goes with this number to make 10?</p>"
        + ex("Example", "7 + □ = 10", "Start at 7. Count on to 10: 8, 9, 10. That is 3.", "3")
        + ex("Example", "Liam has 4 pucks. He wants 10. How many more?", "4 + □ = 10. 4 + 6 = 10.", "6 more")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["7 counters: “7 more make 10”", "Count the empty boxes, not the full ones. 3 more make 10"],
            ["6 + 5 = 10", "6 + 5 = 11. The partner of 6 is 4: 6 + 4 = 10"],
            ["7 + □ = 10, so □ = 17", "Do not add 10. Find the part: 7 + 3 = 10"],
            ["Counting 7, 8, 9, 10 to get 4", "Do not count the 7. Say 8, 9, 10. That is 3"],
        ])
    )


FAQ = [
    {"q": "What are ways to make 10 in Grade 1 math in BC?",
     "a": "In the Number area of the BC Grade 1 math curriculum, students learn the ways to make 10, such as 7 and 3 or 6 and 4. They show them with ten frames, number bonds and objects."},
    {"q": "What are the pairs that make 10?",
     "a": "1 + 9, 2 + 8, 3 + 7, 4 + 6 and 5 + 5, plus the same pairs turned around, such as 9 + 1. 10 + 0 makes 10 too."},
    {"q": "Why do Grade 1 students use ten frames?",
     "a": "A ten frame shows 10 boxes. Children can see how many are full and how many are empty, so they see both parts of 10 at once."},
    {"q": "How can I help my child practise ways to make 10 at home?",
     "a": "Use 10 small objects, like buttons or blocks. Hide some under a cup and ask how many are hidden. A few minutes a day builds quick recall."},
]


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), (s["title"], [it["a"] for it in s["items"]])
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.fullmatch(r"\d+", c) for c in it["c"]):
                assert all(0 < int(c) <= 20 for c in it["c"]), it["c"]
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
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+ and (\d+) [a-z ]+'", it["q"]):
                assert it["q"].count("data-o='1'") + it["q"].count("data-e='1'") == int(m.group(1)) + int(m.group(2))
            for m in re.finditer(r"aria-label='ten frame with (\d+) red(?: and (\d+) green)? counters", it["q"]):
                assert it["q"].count("data-c='1'") == int(m.group(1)) + int(m.group(2) or 0)
            plain = re.sub(r"<svg.*?</svg>", "", it["q"])
            for n in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", plain)):
                assert int(n) <= 10, it["q"]


def gen():
    rnd = random.Random(51802)
    sets = [set_frames(), set_bonds(), set_pairs(), set_missing(), set_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "ways-to-make-10",
        "sort": 2, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Ways to Make 10",
        "seo_title": "Grade 1 Ways to Make 10 Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Ways to make 10",
        "domain": "Number",
        "standard_code": "Grade 1: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Ways to make 10",
        "meta_desc": "Free Grade 1 math worksheets on ways to make 10 for the BC curriculum: ten frames, number bonds, "
                     "pairs that make 10, missing parts like 7 + □ = 10 and simple word problems. "
                     "100 questions with pictures and an answer key.",
        "key_big": "Two numbers make 10 when they fill a ten frame: 7 and 3, 6 and 4, 5 and 5.",
        "key_sub": "Count the empty boxes to find how many more make 10. 6 + 5 is 11, not 10: the partner of 6 is 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u_, "picture|number line|cube train|dominoes|ten frames A")


if __name__ == "__main__":
    u_ = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u_["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u_, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
