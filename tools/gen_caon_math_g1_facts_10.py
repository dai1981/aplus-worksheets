# -*- coding: utf-8 -*-
"""
CA-ON Grade 1 Math: Addition and subtraction facts to 10 (Ontario Curriculum 2020, B2.2)
  python3 tools/gen_caon_math_g1_facts_10.py
Add with pictures and ten frames, make 10 (number bonds), subtract by taking away and
counting back, fact families and turn-around facts, missing parts and Canadian word problems.
Every answer, every wrong answer and every picture count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
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


# ------------------------------------------------------------ explanations
def on_e(a, b):
    return "Start at %d. Count on %d: %s. Do not count the %d. %d + %d = <b>%d</b>." % (
        a, b, on_list(a, b), a, a, b, a + b)


def back_e(a, b):
    return "Start at %d. Count back %d: %s. Do not count the %d. %d %s %d = <b>%d</b>." % (
        a, b, back_list(a, b), a, a, MINUS, b, a - b)


def sent_item(q, right, wrong, e):
    assert eq_true(right), right
    return mcq(q, right, wrong, e)


# ============================================================ set 1: add with pictures and ten frames
def set_add():
    its = []
    for kind, a, b in [("apple", 2, 3), ("duck", 4, 2), ("ball", 3, 5), ("flower", 6, 2),
                       ("car", 5, 4), ("star", 1, 6), ("block", 3, 4), ("fish", 2, 7)]:
        s = a + b
        big, small = max(a, b), min(a, b)
        q = fig(two_groups_svg(a, b, kind)) + "How many %s in all?<br>%d + %d = %s" % (NAMES[kind][1], a, b, Q)
        e = ("Start at the bigger number, %d. Count on %d: %s. %d + %d = <b>%d</b>."
             % (big, small, on_list(big, small), a, b, s))
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), big], e))

    for a, b in [(5, 3), (6, 4), (4, 4), (7, 2), (2, 5), (3, 6)]:
        s = a + b
        q = fig(frame_svg(a, b)) + "How many counters in all?<br>%d + %d = %s" % (a, b, Q)
        if s == 10:
            e = "The ten frame is full. A full ten frame is 10. %d + %d = <b>10</b>." % (a, b)
        elif a == 5:
            e = "The top row is 5. Count on %d: %s. 5 + %d = <b>%d</b>." % (b, on_list(5, b), b, s)
        else:
            e = ("%d red and %d green. %s empty, so %d are full. %d + %d = <b>%d</b>."
                 % (a, b, "1 box is" if s == 9 else "%d boxes are" % (10 - s), s, a, b, s))
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), 10], e))

    for a, b in [(4, 3), (5, 5), (6, 2)]:
        s = a + b
        q = fig(domino_svg(a, b)) + "How many dots in all?<br>%d + %d = %s" % (a, b, Q)
        e = ("Count on from %d: %s. %d + %d = <b>%d</b>." % (a, on_list(a, b), a, b, s) if a != b else
             "5 and 5 is a double. 5 + 5 = <b>10</b>.")
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), a], e))

    for a, b in [(6, 3), (4, 5), (7, 3)]:
        s = a + b
        q = fig(number_line_svg(0, 10, start=a)) + "Start at %d. Count on %d.<br>%d + %d = %s" % (a, b, a, b, Q)
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b)], on_e(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Add with pictures and ten frames", "items": its}


# ============================================================ set 2: make 10 (number bonds)
def set_make10():
    its = []
    for n in [7, 4, 9, 2, 6, 3, 5, 8]:
        k = 10 - n
        q = fig(frame_svg(n)) + "How many more counters make 10?"
        e = "A ten frame has 10 boxes. %d %s full, so <b>%d</b> %s empty. %d + %d = 10." % (
            n, "box is" if n == 1 else "boxes are", k, "is" if k == 1 else "are", n, k)
        its.append(mcq(q, k, [n, k + 1, k - 1, 10 + n, k + 2], e))

    for whole, a, b in [(10, 8, "?"), (10, "?", 5), (10, 1, "?"), (10, "?", 4)]:
        known = a if b == "?" else b
        k = 10 - known
        q = fig(pw_svg(whole, a, b)) + "What is the missing part?"
        e = "The whole is 10. One part is %d. %d + %d = 10. So the missing part is <b>%d</b>." % (known, known, k, k)
        its.append(mcq(q, k, [10 + known, k + 1, k - 1, 10], e))

    for a, b in [(6, 4), (3, 7), (9, 1), (2, 8)]:
        q = fig(cubes_svg(a, b)) + "The train has 10 cubes. %d are red. How many are blue?" % a
        e = "%d + %d = 10. Count the blue cubes: <b>%d</b>." % (a, b, b)
        its.append(mcq(q, b, [b + 1, b - 1, a, 10 + a], e))

    pairs = [(4, 6), (4, 5), (3, 6), (5, 6)]
    assert [a + b for a, b in pairs] == [10, 9, 9, 11]
    it = mcq(fig(dominoes_abcd_svg(pairs)) + "Which domino has 10 dots in all?", "A", ["B", "C", "D"],
             "Domino A has 4 and 6. 4 + 6 = 10, so the answer is <b>A</b>. B and C make 9. D makes 11.")
    it["fixed"] = True
    its.append(it)
    pairs = [(5, 4), (6, 3), (5, 5), (6, 5)]
    assert [a + b for a, b in pairs] == [9, 9, 10, 11]
    it = mcq(fig(dominoes_abcd_svg(pairs)) + "Which domino has 10 dots in all?", "C", ["A", "B", "D"],
             "Domino C has 5 and 5. 5 + 5 = 10, so the answer is <b>C</b>. A and B make 9. D makes 11.")
    it["fixed"] = True
    its.append(it)

    right, wrong = "4 + 5", ["3 + 7", "9 + 1", "2 + 8"]
    assert ev(right) != 10 and all(ev(w) == 10 for w in wrong)
    its.append(mcq(fig(frame_svg(4, 5)) + "Which one does <b>not</b> make 10?", right, wrong,
                   "4 + 5 = 9, not 10. Look: 1 box is empty. So <b>4 + 5</b> does not make 10."))
    right, wrong = "3 + 7", ["3 + 6", "4 + 7", "2 + 7"]
    assert ev(right) == 10 and all(ev(w) != 10 for w in wrong)
    its.append(mcq(fig(row_svg(10, "balloon", [(3, "purple"), (7, "orange")])) + "Which pair makes 10?", right, wrong,
                   "3 purple and 7 orange balloons. 3 + 7 = 10. So <b>3 + 7</b> makes 10."))
    assert len(its) == 20, len(its)
    return {"title": "Make 10 (number bonds)", "items": its}


# ============================================================ set 3: subtract by taking away and counting back
def set_subtract():
    its = []
    for kind, n, k in [("apple", 5, 2), ("ball", 7, 3), ("star", 6, 4), ("flower", 8, 5),
                       ("fish", 9, 3), ("balloon", 10, 4), ("duck", 4, 1), ("block", 9, 6)]:
        d = n - k
        q = fig(take_svg(n, k, kind)) + "%d %s crossed out. How many are left?<br>%d %s %d = %s" % (
            k, "is" if k == 1 else "are", n, MINUS, k, Q)
        e = "There are %d. Take away %d. Count the ones with no X: <b>%d</b>. %d %s %d = %d." % (
            n, k, d, n, MINUS, k, d)
        its.append(mcq(q, d, [n + k, d + 1, d - 1, n], e))

    for n, k in [(7, 2), (10, 3), (8, 6), (6, 3)]:
        d = n - k
        q = fig(frame_svg(n, crossed=k)) + "Take away the counters with an X.<br>%d %s %d = %s" % (n, MINUS, k, Q)
        e = "%d counters. %d have an X. <b>%d</b> are left. %d %s %d = %d." % (n, k, d, n, MINUS, k, d)
        its.append(mcq(q, d, [n + k, d + 1, d - 1, k], e))

    for n, k in [(9, 3), (7, 4), (10, 2), (6, 5), (8, 4), (5, 3)]:
        d = n - k
        q = fig(number_line_svg(0, 10, start=n)) + "Start at %d. Count back %d.<br>%d %s %d = %s" % (n, k, n, MINUS, k, Q)
        its.append(mcq(q, d, [d + 1, n + k, d - 1, k], back_e(n, k)))

    assert 8 - 3 == 5
    its.append(mcq(fig(number_line_svg(0, 10, start=8)) + "Owen counts back 3 from 8. He says “8, 7, 6.” What is 8 "
                   + MINUS + " 3?", "5", ["6", "11", "4"],
                   "Owen counted the 8. Do not count the start. Say 7, 6, 5. 8 " + MINUS + " 3 = <b>5</b>."))
    assert 9 - 4 == 5 and 9 + 4 == 13
    its.append(mcq(fig(take_svg(9, 4, "car")) + "Maya says 9 " + MINUS + " 4 = 13. What did she do?",
                   "She added", ["She took away", "She counted back", "Nothing. She is right."],
                   "13 is 9 + 4. <b>She added</b>. Take away 4: 9 " + MINUS + " 4 = 5."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract: take away and count back", "items": its}


# ============================================================ set 4: fact families and turn-around facts
def set_families():
    its = []
    for kind, a, b in [("apple", 5, 3), ("ball", 2, 6), ("star", 4, 1)]:
        s = a + b
        q = fig(two_groups_svg(a, b, kind)) + "%d + %d = %d. What is %d + %d?" % (a, b, s, b, a)
        e = "You can add in any order. %d + %d is the turn-around fact. It is still <b>%d</b>." % (b, a, s)
        its.append(mcq(q, s, [abs(a - b), s - 1, s + 1], e))

    for a, b in [(6, 2), (7, 3), (5, 4)]:
        s = a + b
        right = "%d + %d = %d" % (b, a, s)
        wrong = ["%d %s %d = %d" % (s, MINUS, b, a), "%d %s %d = %d" % (a, MINUS, b, a - b), "%d + %d = %d" % (b, a, s + 1)]
        assert eq_true(wrong[0]) and eq_true(wrong[1]) and not eq_true(wrong[2])
        q = fig(domino_svg(min(a, 6), b) if a <= 6 else frame_svg(a, b)) + \
            "Which is the turn-around fact for %d + %d = %d?" % (a, b, s)
        e = "A turn-around fact adds the same numbers the other way. <b>%s</b>." % right
        its.append(sent_item(q, right, wrong, e))

    for whole, a, b in [(9, 6, 3), (7, 5, 2), (8, 2, 6), (10, 7, 3)]:
        right = "%d %s %d = %d" % (whole, MINUS, b, a)
        wrong = ["%d %s %d = %d" % (max(a, b), MINUS, min(a, b), abs(a - b)), "%d + %d = %d" % (whole, b, whole + b),
                 "%d + %d = %d" % (a, b, whole)]
        assert all(eq_true(w) for w in wrong) and a != b
        q = fig(pw_svg(whole, a, b)) + "Which <b>subtraction</b> matches the model?"
        e = "Start with the whole, %d. Take away one part, %d. The other part, %d, is left: <b>%s</b>." % (
            whole, b, a, right)
        its.append(sent_item(q, right, wrong, e))

    for a, b in [(4, 6), (3, 5), (2, 7), (6, 3)]:
        s = a + b
        q = fig(frame_svg(a, b)) + "%d + %d = %d. So what is %d %s %d?" % (a, b, s, s, MINUS, b)
        e = "Take away the %d green counters. The %d red ones are left. %d %s %d = <b>%d</b>." % (b, a, s, MINUS, b, a)
        its.append(mcq(q, a, [s + b, b, a + 1, a - 1], e))

    for whole, a in [(8, 3), (6, 4)]:
        b = whole - a
        q = fig(pw_svg(whole, a, b)) + "%d + %d = %d. So what is %d %s %d?" % (a, b, whole, whole, MINUS, a)
        e = "Same family: %d, %d and %d. %d %s %d = <b>%d</b>." % (a, b, whole, whole, MINUS, a, b)
        its.append(mcq(q, b, [whole + a, a, b + 1, b - 1], e))

    opts = ["5 %s 3 = 2" % MINUS, "3 + 5 = 8", "8 %s 5 = 3" % MINUS, "8 %s 3 = 5" % MINUS]
    assert all(eq_true(o) for o in opts)
    its.append(mcq(fig(pw_svg(8, 3, 5)) + "Which fact is <b>not</b> in the family for 3, 5 and 8?", opts[0], opts[1:],
                   "<b>5 %s 3 = 2</b> uses 2. The family uses only 3, 5 and 8." % MINUS))
    opts = ["4 + 2 = 6", "6 + 2 = 8", "6 %s 2 = 4" % MINUS, "2 + 4 = 6"]
    assert all(eq_true(o) for o in opts)
    its.append(mcq(fig(pw_svg(6, 2, 4)) + "Which fact is <b>not</b> in the family for 2, 4 and 6?", opts[1],
                   [opts[0], opts[2], opts[3]],
                   "<b>6 + 2 = 8</b> uses 8. The family uses only 2, 4 and 6."))
    its.append(mcq(fig(pw_svg(9, 2, 7)) + "How many facts are in the family for 2, 7 and 9?", 4, [2, 3, 1],
                   "2 + 7 = 9, 7 + 2 = 9, 9 %s 2 = 7, 9 %s 7 = 2. That is <b>4</b> facts." % (MINUS, MINUS)))
    right, wrong = "3, 4 and 7", ["3, 4 and 8", "2, 4 and 7", "3, 5 and 7"]
    assert 3 + 4 == 7 and 3 + 4 != 8 and 2 + 4 != 7 and 3 + 5 != 7
    its.append(mcq(fig(cubes_svg(3, 4)) + "Which three numbers make a fact family?", right, wrong,
                   "3 red and 4 blue cubes make 7. 3 + 4 = 7, so <b>3, 4 and 7</b> are a family."))
    assert len(its) == 20, len(its)
    return {"title": "Fact families and turn-around facts", "items": its}


# ============================================================ set 5: missing parts and word problems
def set_words():
    its = []

    def miss(eq, pic, e, extra):
        r = solve(eq)
        wrong = [w for w in extra if w != r]
        for w in wrong:
            assert not eq_true(eq.replace("?", str(w))), (eq, w)
        its.append(mcq(fig(pic) + "Find the missing number.<br>" + eq.replace("?", Q), r, wrong, e))

    miss("4 + ? = 10", frame_svg(4), "4 counters. 6 boxes are empty. 4 + <b>6</b> = 10.", [14, 4, 7, 5])
    miss("? + 3 = 7", pw_svg(7, "?", 3), "The whole is 7. One part is 3. 4 + 3 = 7, so the missing number is <b>4</b>.",
         [10, 3, 5])
    miss("6 + ? = 9", number_line_svg(0, 10, qhop=(6, 9)),
         "Count on from 6 to 9: 7, 8, 9. That is 3 hops. 6 + <b>3</b> = 9.", [15, 4, 9])
    miss("? + 5 = 8", pw_svg(8, "?", 5), "8 %s 5 = 3. Check: 3 + 5 = 8. The missing number is <b>3</b>." % MINUS,
         [13, 4, 8])
    miss("10 = ? + 2", cubes_svg(8, 2), "8 red and 2 blue make 10. 10 = <b>8</b> + 2.", [12, 7, 10])
    miss("2 + ? = 7", number_line_svg(0, 10, qhop=(2, 7)),
         "Count on from 2 to 7: 3, 4, 5, 6, 7. That is 5 hops. 2 + <b>5</b> = 7.", [9, 6, 7])
    miss("9 %s ? = 5" % MINUS, take_svg(9, 4, "ball"), "9 balls. 4 have an X. 5 are left. 9 %s <b>4</b> = 5." % MINUS,
         [14, 5, 3])
    miss("7 %s ? = 4" % MINUS, number_line_svg(0, 10, qhop=(7, 4)),
         "Count back from 7 to 4: 6, 5, 4. That is 3 hops. 7 %s <b>3</b> = 4." % MINUS, [11, 4, 2])

    def word(q, right, kind, wrong, e, check, pic):
        assert check, q
        s, p = NAMES[kind]
        f = lambda v: u(v, s, p)
        its.append(mcq(fig(pic) + q, f(right), [f(v) for v in wrong if v > 0], e))

    word("Liam has 4 hockey pucks. He gets 3 more. How many pucks does he have now?", 7, "puck", [6, 8, 1],
         "Add. 4 + 3 = <b>7</b>.", 4 + 3 == 7, two_groups_svg(4, 3, "puck"))
    word("3 children play at recess. 5 more come. How many children play now?", 8, "child", [7, 2, 9],
         "Add. Start at 5. Count on 3: 6, 7, 8. 3 + 5 = <b>8</b>.", 3 + 5 == 8, two_groups_svg(3, 5, "child", "orange"))
    word("6 ducks swim in the pond. 2 fly away. How many ducks are left?", 4, "duck", [8, 5, 3],
         "Take away. 6 %s 2 = <b>4</b>. (8 adds instead.)" % MINUS, 6 - 2 == 4, take_svg(6, 2, "duck"))
    word("It is a snow day. Owen makes 2 snowballs. Then he makes 6 more. How many snowballs does he make?", 8,
         "snowball", [7, 4, 9], "Add. Start at 6. Count on 2: 7, 8. 2 + 6 = <b>8</b>.", 2 + 6 == 8,
         two_groups_svg(2, 6, "snowball"))
    word("Emma picks 10 apples at the orchard. She uses 3 in a pie. How many apples are left?", 7, "apple",
         [13, 8, 6], "Take away. 10 %s 3 = <b>7</b>. (13 adds instead.)" % MINUS, 10 - 3 == 7, take_svg(10, 3, "apple"))
    word("Kai has 3 toy cars. He wants 10. How many more does he need?", 7, "car", [13, 3, 6],
         "3 + ? = 10. 3 + 7 = 10, so he needs <b>7</b> more.", 3 + 7 == 10, frame_svg(3))
    word("8 children are on the bus. Some get off. Now there are 5. How many got off?", 3, "child", [13, 5, 4],
         "8 %s ? = 5. Count back from 8 to 5: 7, 6, 5. That is <b>3</b>." % MINUS, 8 - 3 == 5, row_svg(8, "child"))
    word("Ava picks 9 flowers. Arjun picks 6 flowers. How many more flowers does Ava pick?", 3, "flower",
         [15, 4, 6], "Line them up. Ava has 3 with no partner. 9 %s 6 = <b>3</b>." % MINUS, 9 - 6 == 3,
         compare_svg(9, "Ava", 6, "Arjun", "flower"))
    word("Ethan scores 4 goals in hockey. Chloe scores 4 goals. How many goals in all?", 8, "puck",
         [7, 9, 4], "This is a double. 4 + 4 = <b>8</b>.", 4 + 4 == 8, two_groups_svg(4, 4, "puck"))
    word("Priya has 10 crayons. 4 are red. The rest are blue. How many are blue?", 6, "crayon", [14, 7, 4],
         "10 = 4 + ?. 4 + 6 = 10, so <b>6</b> are blue.", 4 + 6 == 10,
         row_svg(10, "crayon", [(4, "red"), (6, "blue")]))
    word("5 geese sit by the lake. 3 more land. Then 2 fly away. How many geese are there now?", 6, "duck",
         [8, 10, 4], "Step 1: 5 + 3 = 8. Step 2: 8 %s 2 = <b>6</b>. (8 stops after step 1.)" % MINUS,
         5 + 3 - 2 == 6, number_line_svg(0, 10, start=5))
    word("Noah has 7 balloons for Canada Day. One pops. How many balloons are left?", 6, "balloon", [8, 7, 5],
         "Take away 1. 7 %s 1 = <b>6</b>. (8 adds instead.)" % MINUS, 7 - 1 == 6, take_svg(7, 1, "balloon"))
    # the geese and the hockey goals use other pictures, so their units are fixed by hand
    for it in its:
        if "geese" in it["q"]:
            it["c"] = [c.replace("ducks", "geese").replace("duck", "goose") for c in it["c"]]
        if "goals" in it["q"]:
            it["c"] = [c.replace("pucks", "goals").replace("puck", "goal") for c in it["c"]]
    assert len(its) == 20, len(its)
    return {"title": "Missing parts and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add: put together</h2>"
        "<p>To add, put two groups together. Then count them all.</p>"
        "<p>A faster way: start at the bigger number. Count on.</p>"
        "<figure class='sn-fig'>" + two_groups_svg(5, 3, "apple") +
        "<figcaption>5 + 3: start at 5. Count on 6, 7, 8. So 5 + 3 = 8.</figcaption></figure>"
        + ex("Example", "What is 6 + 3?", "Start at 6. Count on 3: 7, 8, 9. Do not count the 6.", "9")
        + "<h2>Make 10</h2>"
        "<p>A ten frame has 10 boxes. The empty boxes show how many more make 10.</p>"
        "<figure class='sn-fig'>" + frame_svg(7) +
        "<figcaption>7 counters and 3 empty boxes. 7 + 3 = 10.</figcaption></figure>"
        + table(["Pairs that make 10", "Turn-around"],
                [["%d + %d" % (a, 10 - a), "%d + %d" % (10 - a, a)] for a in range(1, 6)])
        + "<h2>Subtract: take away</h2>"
        "<p>To subtract, take some away. Count what is left.</p>"
        "<p>Or start at the big number and count back.</p>"
        "<figure class='sn-fig'>" + take_svg(8, 3, "ball") +
        "<figcaption>8 balls. Take away 3. 5 are left. 8 − 3 = 5.</figcaption></figure>"
        + ex("Example", "What is 9 − 4?", "Start at 9. Count back 4: 8, 7, 6, 5. Do not count the 9.", "5")
        + "<h2>Fact families</h2>"
        "<p>You can add in any order: 2 + 6 = 6 + 2. This is a <b>turn-around fact</b>.</p>"
        "<p>Three numbers make a <b>fact family</b>. If you know 6 + 2 = 8, you know 8 − 2 = 6 too.</p>"
        "<figure class='sn-fig'>" + pw_svg(8, 6, 2) +
        "<figcaption>6 + 2 = 8, 2 + 6 = 8, 8 − 2 = 6, 8 − 6 = 2.</figcaption></figure>"
        + ex("Example", "Find the missing number: 4 + ? = 10", "Think: 4 and what make 10? 4 + 6 = 10.", "6")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["6 + 3 = 8 (counting 6, 7, 8)", "Do not count the start number. Say 7, 8, 9. So 6 + 3 = 9"],
            ["9 − 4 = 6 (counting 9, 8, 7, 6)", "Do not count the start number. Say 8, 7, 6, 5. So 9 − 4 = 5"],
            ["9 − 4 = 13", "13 adds. Look at the sign. − means take away"],
            ["4 + ? = 10, so ? = 10", "10 is the whole. Find the part: 4 + 6 = 10"],
        ])
    )


FAQ = [
    {"q": "What addition facts should a Grade 1 student know in Ontario?",
     "a": "The Ontario Mathematics Curriculum (2020) asks Grade 1 students to recall and show addition facts for numbers up to 10, such as 6 + 4 = 10, and the related subtraction facts, such as 10 − 4 = 6."},
    {"q": "What is a fact family in Grade 1 math?",
     "a": "A fact family is a group of facts made from the same three numbers. For 3, 5 and 8 the facts are 3 + 5 = 8, 5 + 3 = 8, 8 − 3 = 5 and 8 − 5 = 3."},
    {"q": "Why do Grade 1 students learn the pairs that make 10?",
     "a": "Pairs like 7 and 3 or 6 and 4 help children add and subtract quickly. Later they use them to add past 10, such as 8 + 5 = 10 + 3."},
    {"q": "How can I help my child practise facts to 10 at home?",
     "a": "Use 10 small objects, like buttons or dry pasta. Hide some under a cup and ask how many are hidden. A few minutes a day builds quick recall."},
]


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), (s["title"], [it["a"] for it in s["items"]])
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [c.split(" ")[0] for c in it["c"]]
            if all(re.fullmatch(r"\d+( [a-z ]+)?", c) for c in it["c"]):
                assert len(set(vals)) == 4, it["c"]
                assert all(0 < int(v) <= 20 for v in vals), it["c"]
            key = re.sub(r"<[^>]+>", " ", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            assert it["q"].count("<svg") <= 1
            for t in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in t and '"' not in t and ".." not in t, t
                assert not re.search(r"(?<![\d$])\b1 (?!is\b|was\b)[a-z]+s\b", re.sub(r"<[^>]+>", " ", t)), t
            # a number sentence with one ? on the last line: the answer solves it
            last = re.sub(r"<[^>]+>", "", re.split(r"<br>", it["q"])[-1]).strip()
            if re.fullmatch(r"[\d?]+( [+−] [\d?]+)* = [\d?]+( [+−] [\d?]+)*", last) and last.count("?") == 1:
                assert it["c"][it["a"]].split()[0] == str(solve(last)), (last, it["c"])
                for j, c in enumerate(it["c"]):
                    if j != it["a"]:
                        assert not eq_true(last.replace("?", c.split()[0])), (last, c)
            # 'What is a ± b?' questions
            m = re.search(r"(?:What is|So what is) (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                assert it["c"][it["a"]] == str(v), it["q"]
            right = it["c"][it["a"]]
            if re.fullmatch(r"\d+ [+−] \d+ = \d+", right):
                assert eq_true(right), right
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+ and (\d+) [a-z ]+'", it["q"]):
                assert it["q"].count("data-o='1'") == int(m.group(1)) + int(m.group(2))
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+, (\d+) crossed out'", it["q"]):
                assert it["q"].count("data-o='1'") == int(m.group(1))
                assert it["q"].count("data-x='1'") == int(m.group(2))
            for m in re.finditer(r"aria-label='ten frame with (\d+) red(?: and (\d+) green)? counters", it["q"]):
                assert it["q"].count("data-c='1'") == int(m.group(1)) + int(m.group(2) or 0)
            # facts to 10: no number above 10 in a question (except in wrong answers)
            plain = re.sub(r"<svg.*?</svg>", "", it["q"])
            for n in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", plain)):
                assert int(n) <= 10 or " says " in plain, it["q"]


def gen():
    rnd = random.Random(41803)
    sets = [set_add(), set_make10(), set_subtract(), set_families(), set_words()]
    # fixed A-D items keep their order; balance the rest around them
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
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "addition-and-subtraction-facts-to-10",
        "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Facts to 10",
        "seo_title": "Grade 1 Addition and Subtraction Facts to 10 Worksheets with Answer Key (Ontario)",
        "short_title": "Addition and subtraction facts to 10",
        "domain": "Number",
        "standard_code": "Grade 1: B2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Recall and demonstrate addition facts for numbers up to 10, and related subtraction facts",
        "meta_desc": "Free Grade 1 math worksheets on addition and subtraction facts to 10: adding with pictures and ten "
                     "frames, pairs that make 10, taking away, counting back, fact families and missing numbers. "
                     "100 questions with an answer key, following the Ontario curriculum.",
        "key_big": "Know the pairs that make 10, and every fact to 10 gets easy.",
        "key_sub": "6 + 3: start at 6 and count on 7, 8, 9. 9 − 4: count back 8, 7, 6, 5. "
                   "If 6 + 4 = 10, then 10 − 4 = 6.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u_, "picture|number line|cube train|dominoes")


if __name__ == "__main__":
    u_ = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u_["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u_, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
