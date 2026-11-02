# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Addition and subtraction within 20 (Australian Curriculum v9.0, AC9M1N04)
  python3 tools/gen_au_maths_y1_add_sub.py
Pictures to count, ten frames, part-whole models, dominoes and number lines.
Add with pictures, number bonds to 10, count on and back, doubles and make ten,
take away and find the difference.
Every answer, every picture count and every number sentence is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
Q = "<b>?</b>"
C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", pink="#e86aa6", brown="#c68a4a")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique, positive distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^\$?0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


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
    """Tag wide pictures (rows of objects, lines, ten frames) so they print larger."""
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
             block=("block", "blocks"), biscuit=("biscuit", "biscuits"), balloon=("balloon", "balloons"),
             car=("toy car", "toy cars"), duck=("duck", "ducks"), fish=("fish", "fish"))


def nm(n, kind):
    s, p = NAMES[kind]
    return u(n, s, p)


# ------------------------------------------------------------ pictures: objects (each fits a 28 x 28 cell)
PITCH = 28
DEF_COL = dict(apple="red", star="gold", fish="orange", ball="blue", flower="pink", block="green",
               biscuit="brown", balloon="purple", car="blue", duck="yellow")


def obj(kind, cx, cy):
    col = C[DEF_COL[kind]]
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
    elif kind == "biscuit":
        s += "<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
        for dx, dy in [(-4, -3), (3, -4), (0, 3), (5, 3), (-4, 4)]:
            s += "<circle cx='%.1f' cy='%.1f' r='1.5' fill='#5a3a1a'/>" % (cx + dx, cy + dy)
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
    else:
        raise ValueError(kind)
    return s + "</g>"


def cross(cx, cy, col=RED):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - 10, cy - 10, cx + 10, cy + 10, col, cx - 10, cy + 10, cx + 10, cy - 10, col))


def row_x(x0, c):
    """Centre of column c in a row, with a small gap after every 5."""
    return x0 + c * PITCH + PITCH / 2 + 8 * (c // 5)


def row_w(n):
    return n * PITCH + 8 * ((n - 1) // 5)


def group_body(x0, y0, n, kind, cols=5):
    """n objects in rows of `cols` (gap after every 5)."""
    s, centres = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx, cy = row_x(x0, c), y0 + r * PITCH + PITCH / 2
        centres.append((cx, cy))
        s.append(obj(kind, cx, cy))
    w = row_w(min(n, cols))
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centres


def two_groups_svg(a, b, kind):
    """Two groups with a + between them."""
    assert a <= 10 and b <= 10
    o, gap = 6, 34
    b1, w1, h1, _ = group_body(o, o, a, kind)
    b2, w2, h2, _ = group_body(o + w1 + gap, o, b, kind)
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
    col = INK if DEF_COL[kind] == "red" else RED
    xs = "".join(cross(cx, cy, col) for cx, cy in cen[n - k:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %s, %d crossed out" % (nm(n, kind), k))
    assert svg.count("<g data-o='1'>") == n and svg.count("<g data-x='1'>") == k
    return svg


def compare_svg(n1, name1, n2, name2, kind):
    """Two rows lined up, one object above the other, so the extra ones stand out."""
    o, lw = 6, 78
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


# ------------------------------------------------------------ pictures: number line, ten frames, part-whole, dominoes
def number_line_svg(lo, hi, start=None, end=None, hops=(), step=30):
    """Number line lo..hi. start: green dot. end: red ring. hops: list of (from, to) arcs with a +/− label."""
    L, Y = 18, 66 if hops else 22
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    for a, b in hops:
        assert lo <= min(a, b) and max(a, b) <= hi
        mid = (X(a) + X(b)) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (X(a), Y - 9, mid, Y - 54, X(b), Y - 9, GREEN))
        s.append(text(mid, Y - 36, ("+%d" if b > a else MINUS + "%d") % abs(b - a), 16, col=GREEN))
    label = "number line from %d to %d" % (lo, hi)
    if start is not None:
        assert lo <= start <= hi
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, GREEN))
        label += " with a green dot on %d" % start
    if end is not None:
        assert lo <= end <= hi
        s.append("<circle cx='%d' cy='%d' r='7' fill='#fff' stroke='%s' stroke-width='3'/>" % (X(end), Y, RED))
        label += " and a red ring on %d" % end
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


def frames_svg(a, b=0):
    """a red then b green counters. One ten frame if a + b <= 10, else two (the first is filled first)."""
    cols = [RED] * a + [GREEN] * b
    assert a + b <= 20
    o, gap = 6, 12
    lab = "%s with %d red%s counters" % ("ten frame" if a + b <= 10 else "two ten frames", a,
                                         " and %d green" % b if b else "")
    if a + b <= 10:
        svg = svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, cols), lab)
    else:
        svg = svg_wrap(2 * FW + gap + 2 * o, FH + 2 * o, frame(o, o, cols[:10]) + frame(o + FW + gap, o, cols[10:]), lab)
    assert svg.count("data-c='1'") == a + b
    return svg


def take_frames_svg(n, k):
    """n red counters in two ten frames; the last k are crossed out."""
    assert 10 < n <= 20 and k < n
    o, gap = 6, 12
    k2 = min(k, n - 10)
    body = frame(o, o, [RED] * 10, crossed=k - k2) + frame(o + FW + gap, o, [RED] * (n - 10), crossed=k2)
    svg = svg_wrap(2 * FW + gap + 2 * o, FH + 2 * o, body, "two ten frames with %d counters, %d crossed out" % (n, k))
    assert svg.count("data-c='1'") == n and svg.count("data-x='1'") == k
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


def dominoes_svg(pairs):
    o, gap = 6, 24
    body = "".join(domino_body(o + i * (120 + gap), o, a, b) for i, (a, b) in enumerate(pairs))
    W = len(pairs) * 120 + (len(pairs) - 1) * gap + 2 * o
    return svg_wrap(W, 60 + 2 * o, body, "dominoes " + " and ".join("%d and %d" % p for p in pairs))


# ------------------------------------------------------------ explanations
def on_e(a, b):
    return "Start at %d. Count on %d: %s. Do not count the %d. %d + %d = <b>%d</b>." % (
        a, b, on_list(a, b), a, a, b, a + b)


def back_e(a, b):
    return "Start at %d. Count back %d: %s. Do not count the %d. %d %s %d = <b>%d</b>." % (
        a, b, back_list(a, b), a, a, MINUS, b, a - b)


def via10_e(a, b):
    """a − b crossing 10 (a > 10 > a − b)."""
    part = a - 10
    assert 0 < part < b
    return "Go back to 10 first: %d %s %d = 10. Then take away %d more: 10 %s %d = <b>%d</b>." % (
        a, MINUS, part, b - part, MINUS, b - part, a - b)


def make10_e(a, b):
    """a + b > 10 by filling up a ten."""
    big, small = max(a, b), min(a, b)
    need = 10 - big
    left = small - need
    assert need > 0 and left > 0
    first = "Start with %d. " % big if big != a else ""
    return ("%s%d needs %d to make 10. Take %d from the %d, and %d is left. 10 + %d = <b>%d</b>."
            % (first, big, need, need, small, left, left, a + b))


def swap_mistake(a, b):
    """Teen number take away ones, taking the smaller digit from the larger: 12 − 5 → 13."""
    assert 10 < a < 20 and b < 10
    return 10 + abs(a - 10 - b)


def sent_item(q, right, wrong, e):
    """A 'which number sentence' question: right is true; no wrong one is the same fact
    (same two numbers, same sign, true)."""
    assert eq_true(right), right
    key = lambda s: (sorted(s.split()[0:3:2]), s.split()[1])
    for w in wrong:
        assert w != right and not (eq_true(w) and key(w) == key(right)), w
    return mcq(q, right, wrong, e)


# ============================================================ set 1: add with pictures and ten frames
def set_add():
    its = []

    def group_q(kind, a, b):
        s = a + b
        plur = NAMES[kind][1]
        big, small = max(a, b), min(a, b)
        q = fig(two_groups_svg(a, b, kind)) + "How many %s altogether?<br>%d + %d = %s" % (plur, a, b, Q)
        e = ("Start at the bigger number, %d. Count on %d: %s. Do not count the %d. %d + %d = <b>%d</b>."
             % (big, small, on_list(big, small), big, a, b, s))
        return mcq(q, s, [s - 1, s + 1, abs(a - b), b], e)

    for kind, a, b in [("apple", 2, 3), ("duck", 4, 2), ("ball", 3, 5), ("flower", 6, 2),
                       ("car", 5, 4), ("star", 7, 3), ("biscuit", 6, 5)]:
        its.append(group_q(kind, a, b))

    for a, b in [(3, 4), (5, 2), (6, 3), (4, 4), (2, 6)]:
        s = a + b
        q = fig(frames_svg(a, b)) + "How many counters altogether?<br>%d + %d = %s" % (a, b, Q)
        if a == 5:
            e = "The top row has 5 red. Count on the %d green: %s. 5 + %d = <b>%d</b>." % (b, on_list(5, b), b, s)
        else:
            e = ("%d red and %d green. Count the full boxes: %d. %s empty. %d + %d = <b>%d</b>."
                 % (a, b, s, "1 box is" if s == 9 else "%d boxes are" % (10 - s), a, b, s))
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), 10], e))

    for a, b in [(7, 4), (8, 5), (6, 6), (9, 6), (10, 7)]:
        s = a + b
        q = fig(frames_svg(a, b)) + "How many counters altogether?<br>%d + %d = %s" % (a, b, Q)
        if a == 10:
            e = "The first ten frame is full: 10. The second has %d. 10 + %d = <b>%d</b>." % (b, b, s)
        else:
            e = ("%d red and %d green. The first ten frame is full: 10. The second has %d. 10 + %d = %d. "
                 "So %d + %d = <b>%d</b>." % (a, b, s - 10, s - 10, s, a, b, s))
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), 10], e))

    for kind, a, b in [("block", 8, 3), ("balloon", 9, 4), ("fish", 7, 6)]:
        its.append(group_q(kind, a, b))
    assert len(its) == 20, len(its)
    return {"title": "Add with pictures and ten frames", "items": its}


# ============================================================ set 2: number bonds to 10
def bond_wrong(r, g):
    out = []
    for x, y in [(r + 1, g - 1), (r - 1, g + 1), (r, g - 1), (r + 1, g), (r - 1, g)]:
        if x > 0 and y > 0 and (x, y) not in [(r, g), (g, r)]:
            out.append("%d + %d = %d" % (x, y, x + y))
    return out


def set_bonds():
    its = []
    for n in [7, 4, 9, 6, 3, 2]:
        k = 10 - n
        q = fig(frames_svg(n)) + "How many more counters make 10?"
        e = "A ten frame has 10 boxes. %d %s full, so <b>%d</b> %s empty. %d + %d = 10." % (
            n, "box is" if n == 1 else "boxes are", k, "is" if k == 1 else "are", n, k)
        its.append(mcq(q, k, [k + 1, k - 1, n, 10], e))

    for i, a in enumerate([3, 6, 8, 1]):
        k = 10 - a
        q = fig(pw_svg(10, a, "?") if i % 2 == 0 else pw_svg(10, "?", a)) + "What is the missing part?"
        e = "The whole is 10. One part is %d. %d + %d = 10. So the missing part is <b>%d</b>." % (a, a, k, k)
        its.append(mcq(q, k, [k + 1, k - 1, a, 10 + a], e))

    for r, g in [(7, 3), (4, 6), (2, 8), (1, 9)]:
        q = fig(frames_svg(r, g)) + "Which number bond to 10 does it show?"
        e = "Count the red: %d. Count the green: %d. So <b>%d + %d = 10</b>." % (r, g, r, g)
        its.append(sent_item(q, "%d + %d = 10" % (r, g), bond_wrong(r, g), e))

    for qt, a in [("Which two numbers make 10?", 3), ("Which pair adds up to 10?", 8), ("Pick the pair that makes 10.", 1)]:
        k = 10 - a
        wrong = []
        for x, y in [(a, k + 1), (a, k - 1), (a + 1, k), (a - 1, k)]:
            if x > 0 and y > 0:
                assert x + y != 10
                wrong.append("%d and %d" % (x, y))
        e = "%d + %d = 10, so <b>%d and %d</b> make 10. The others make 9 or 11." % (a, k, a, k)
        its.append(mcq(qt, "%d and %d" % (a, k), wrong, e))

    for a, b, pic in [(6, 4, pw_svg(10, 6, "?")), (2, 8, pw_svg(10, "?", 2))]:
        q = fig(pic) + "Use the number bond.<br>10 %s %d = %s" % (MINUS, a, Q)
        e = "%d + %d = 10. Take away the part %d. The part %d is left. 10 %s %d = <b>%d</b>." % (
            a, b, a, b, MINUS, a, b)
        its.append(mcq(q, b, [10 + a, b + 1, b - 1, a], e))

    right, wrong = "4 + 5", ["3 + 7", "9 + 1", "2 + 8"]
    assert ev(right) != 10 and all(ev(w) == 10 for w in wrong)
    its.append(mcq("Which is <b>not</b> a number bond to 10?", right, wrong,
                   "4 + 5 = 9, not 10. So <b>4 + 5</b> is not a number bond to 10. The others all make 10."))
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 10", "items": its}


# ============================================================ set 3: count on and count back on a number line
def set_lines():
    its = []
    for a, b in [(5, 3), (8, 4), (11, 3), (9, 5), (13, 4), (14, 2)]:
        s = a + b
        lo = max(0, min(a - 2, 10))
        hi = lo + 10
        assert lo <= a and s <= hi
        q = fig(number_line_svg(lo, hi, start=a)) + "Start at %d. Count on %d.<br>%d + %d = %s" % (a, b, a, b, Q)
        its.append(mcq(q, s, [s - 1, a - b, s + 1, b], on_e(a, b)))

    for a, b in [(9, 3), (12, 4), (15, 3), (11, 5), (17, 4), (20, 3)]:
        d = a - b
        lo = min(max(0, a - 9), 10)
        hi = lo + 10
        assert lo <= d and a <= hi
        q = fig(number_line_svg(lo, hi, start=a)) + "Start at %d. Count back %d.<br>%d %s %d = %s" % (a, b, a, MINUS, b, Q)
        its.append(mcq(q, d, [d + 1, a + b, d - 1], back_e(a, b)))

    q = fig(number_line_svg(5, 15, hops=[(7, 10), (10, 13)])) + "Jump to 10 first.<br>7 + 6 = %s" % Q
    its.append(mcq(q, 13, [12, 1, 14],
                   "7 needs 3 to get to 10. 6 is 3 and 3. Jump 3 to 10, then 3 more to 13. 7 + 6 = <b>13</b>."))
    q = fig(number_line_svg(6, 15, hops=[(13, 10), (10, 8)])) + "Jump back to 10 first.<br>13 %s 5 = %s" % (MINUS, Q)
    assert swap_mistake(13, 5) == 12
    its.append(mcq(q, 8, [12, 18, 9], via10_e(13, 5)))

    for lo, hi, a, b in [(4, 12, 6, 9), (8, 16, 14, 10), (10, 20, 12, 17), (11, 20, 18, 13)]:
        k = abs(b - a)
        if b > a:
            right = "%d + %d = %d" % (a, k, b)
            wrong = ["%d %s %d = %d" % (a, MINUS, k, a - k), "%d + %d = %d" % (a, k, b + 1), "%d + %d = %d" % (b, k, b + k)]
            e = "The jump starts at %d. It goes on %d and lands on %d. <b>%s</b>." % (a, k, b, right)
        else:
            right = "%d %s %d = %d" % (a, MINUS, k, b)
            wrong = ["%d + %d = %d" % (a, k, a + k), "%d %s %d = %d" % (a, MINUS, k, b + 1), "%d %s %d = %d" % (b, MINUS, k, b - k)]
            e = "The jump starts at %d. It goes back %d and lands on %d. <b>%s</b>." % (a, k, b, right)
        q = fig(number_line_svg(lo, hi, hops=[(a, b)])) + "Which number sentence matches the jump?"
        its.append(sent_item(q, right, wrong, e))

    q = fig(number_line_svg(6, 16, start=8, end=13)) + "How many jumps from 8 to 13?<br>8 + %s = 13" % Q
    assert solve("8 + ? = 13") == 5
    its.append(mcq(q, 5, [13, 21, 6, 4],
                   "Start at 8. Count the jumps: 9, 10, 11, 12, 13. That is <b>5</b> jumps. 8 + 5 = 13."))
    q = fig(number_line_svg(9, 17, start=15, end=11)) + "How many jumps back from 15 to 11?<br>15 %s %s = 11" % (MINUS, Q)
    assert solve("15 %s ? = 11" % MINUS) == 4
    its.append(mcq(q, 4, [11, 26, 5, 3],
                   "Start at 15. Count back the jumps: 14, 13, 12, 11. That is <b>4</b> jumps. 15 %s 4 = 11." % MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Count on and count back on a number line", "items": its}


# ============================================================ set 4: doubles and make ten
HOOK = {2: "", 3: "", 4: "A spider has 8 legs: 4 on each side.",
        5: "Two hands have 10 fingers: 5 and 5.",
        6: "An egg carton has 2 rows of 6 eggs: 12 eggs.",
        7: "Two weeks have 14 days: 7 and 7.",
        8: "8 + 2 = 10, and 6 more is 16.",
        9: "10 + 10 = 20. Take away 2, and you get 18."}


def set_doubles():
    its = []
    for n in [2, 3, 4, 5, 6]:
        q = fig(domino_svg(n, n)) + "Double %d.<br>%d + %d = %s" % (n, n, n, Q)
        e = ("%d + %d is a double. %d + %d = <b>%d</b>. %s" % (n, n, n, n, 2 * n, HOOK[n])).strip()
        its.append(mcq(q, 2 * n, [2 * n - 1, 2 * n + 1, n, 2 * n + 2], e))
    for n in [7, 8, 9]:
        q = fig(frames_svg(n, n)) + "Double %d.<br>%d + %d = %s" % (n, n, n, Q)
        e = "%d + %d is a double. %d + %d = <b>%d</b>. %s" % (n, n, n, n, 2 * n, HOOK[n])
        its.append(mcq(q, 2 * n, [2 * n - 1, 2 * n + 1, 2 * n - 2], e))

    for a, b in [(2, 3), (3, 4), (5, 4), (5, 6), (7, 8), (9, 8)]:
        lo, hi = min(a, b), max(a, b)
        pic = domino_svg(a, b) if hi <= 6 else frames_svg(a, b)
        q = fig(pic) + "Use a double.<br>%d + %d = %s" % (a, b, Q)
        e = "%d + %d = %d. %d is 1 more than %d, so add 1 more: %d + 1 = <b>%d</b>." % (
            lo, lo, 2 * lo, hi, lo, 2 * lo, a + b)
        its.append(mcq(q, a + b, [2 * lo, 2 * hi, 2 * lo - 1], e))

    for a, b in [(9, 4), (8, 6), (7, 5)]:
        need = 10 - a
        k = b - need
        q = (fig(frames_svg(a, b)) + "Move %d green to fill the first ten frame.<br>%d + %d = 10 + %s"
             % (need, a, b, Q))
        assert solve("%d + %d = 10 + ?" % (a, b)) == k
        e = ("%d needs %d to make 10. Take %d from the %d. %d %s left. So %d + %d = 10 + <b>%d</b> = %d."
             % (a, need, need, b, k, "is" if k == 1 else "are", a, b, k, a + b))
        its.append(mcq(q, k, [b, need, k + 1, k - 1], e))

    for a, b in [(9, 3), (8, 7), (6, 9)]:
        s = a + b
        q = fig(frames_svg(a, b)) + "Make 10 first.<br>%d + %d = %s" % (a, b, Q)
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), "10%d" % (s - 10)], make10_e(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Doubles and make ten", "items": its}


# ============================================================ set 5: take away and find the difference
def set_subtract():
    its = []

    def take_e(word, n, k):
        if n > 10 > n - k:
            return word + via10_e(n, k)
        if k <= 3:
            return word + back_e(n, k)
        return word + "Cross out %d. Count the ones with no cross: <b>%d</b>. %d %s %d = %d." % (
            k, n - k, n, MINUS, k, n - k)

    # take away with pictures
    for kind, n, k, story, word in [
        ("balloon", 8, 3, "Zara has 8 balloons at her party. 3 balloons pop. How many balloons are left?", "Pop means gone, so take away. "),
        ("apple", 11, 3, "The class has 11 apples for recess. The students eat 3. How many apples are left?", "Eaten apples are gone, so take away. "),
        ("biscuit", 12, 4, "Mum bakes 12 Anzac biscuits. The family eats 4. How many biscuits are left?", "Eaten biscuits are gone, so take away. "),
        ("fish", 15, 6, "15 fish swim in a rock pool. 6 fish swim away. How many fish are left?", "Some swim away, so take away. "),
        ("ball", 17, 5, "There are 17 balls in the sport shed. Class 1B takes 5 to the oval. How many balls are left in the shed?", "Some are taken, so take away. "),
    ]:
        d = n - k
        unit = NAMES[kind]
        cands = [n + k, d + 1, d - 1, k]
        if n > 10:
            cands = [n + k, swap_mistake(n, k), d + 1, d - 1] if swap_mistake(n, k) not in (d, n) else cands
        its.append(mcq(fig(take_svg(n, k, kind)) + story, u(d, *unit), [u(x, *unit) for x in cands],
                       take_e(word, n, k)))
    its.append(mcq(fig(take_frames_svg(13, 4))
                   + "13 children are in the pool at swimming lessons. 4 get out. How many are still in the pool?",
                   "9 children", ["17 children", "11 children", "10 children"],
                   "Getting out means take away. " + via10_e(13, 4)))
    assert swap_mistake(13, 4) == 11

    # difference with pictures
    diffs = [
        (9, "Mia", 6, "Leo", "star", "Mia has 9 star stickers. Leo has 6. How many more stickers does Mia have?", "sticker", "stickers"),
        (12, "Jack", 8, "Noah", "car", "Jack has 12 toy cars. Noah has 8. How many more toy cars does Jack have?", "toy car", "toy cars"),
        (13, "Isla", 7, "Ruby", "flower", "Isla picks 13 flowers. Ruby picks 7. How many fewer flowers does Ruby pick?", "flower", "flowers"),
        (15, "Kai", 10, "Sienna", "block", "Kai has a row of 15 blocks. Sienna has a row of 10. How many more blocks does Kai have?", "block", "blocks"),
    ]
    for n1, a1, n2, a2, kind, story, sg, pl in diffs:
        d = n1 - n2
        cands = [n1 + n2, n2, d + 1, d - 1]
        e = ("Match them up. %d of %s’s %s have a partner. <b>%d</b> do not. The difference is %d. %d %s %d = %d."
             % (n2, a1, pl, d, d, n1, MINUS, n2, d))
        its.append(mcq(fig(compare_svg(n1, a1, n2, a2, kind)) + story, u(d, sg, pl), [u(x, sg, pl) for x in cands], e))

    for big, small in [(14, 9), (16, 12)]:
        d = big - small
        q = (fig(number_line_svg(small - 2, small + 8, start=small, end=big))
             + "What is the difference between %d and %d?<br>Count up from %d to %d." % (big, small, small, big))
        e = "Count up from %d: %s. That is <b>%d</b> jumps. %d %s %d = %d." % (
            small, on_list(small, d), d, big, MINUS, small, d)
        its.append(mcq(q, d, [big + small, d + 1, d - 1], e))

    # harder stories
    its.append(mcq(fig(take_frames_svg(20, 6))
                   + "There are 20 sausages at the school sausage sizzle. 6 are sold. How many sausages are left?",
                   "14 sausages", ["26 sausages", "15 sausages", "13 sausages"],
                   "Sold sausages are gone, so take away. 20 is 10 and 10. 10 %s 6 = 4. 10 and 4 is 14. 20 %s 6 = <b>14</b>."
                   % (MINUS, MINUS)))
    assert swap_mistake(15, 6) == 11
    its.append(mcq(fig(number_line_svg(5, 15, start=15))
                   + "Grace has $15. She spends $6 on a book. How much money does she have left?",
                   "$9", ["$21", "$11", "$10"], "Spending means take away. " + via10_e(15, 6)))
    its.append(mcq(fig(number_line_svg(5, 14, start=7, end=12))
                   + "Noah is 7. His sister Matilda is 12. How many years older is Matilda?",
                   "5 years", ["19 years", "6 years", "4 years"],
                   "Find the difference. Count up from 7 to 12: 8, 9, 10, 11, 12. That is <b>5</b> years. 12 %s 7 = 5." % MINUS))
    its.append(sent_item(fig(take_frames_svg(16, 4))
                         + "16 students are in the class. 4 go to the library. Which number sentence shows how many are left?",
                         "16 %s 4 = 12" % MINUS, ["16 + 4 = 20", "16 %s 4 = 13" % MINUS, "12 %s 4 = 8" % MINUS],
                         "4 students go, so take them away from 16. <b>16 %s 4 = 12</b>." % MINUS))
    its.append(mcq(fig(number_line_svg(9, 19, start=11, end=18))
                   + "Liam has 11 marbles. Chloe has 18 marbles. How many more marbles does Chloe have?",
                   "7 marbles", ["29 marbles", "8 marbles", "6 marbles"],
                   "Find the difference. Count up from 11 to 18: 12, 13, 14, 15, 16, 17, 18. That is <b>7</b> more."))
    its.append(mcq(fig(take_frames_svg(19, 7))
                   + "At the beach, 19 children swim between the flags. 7 get out. How many are still swimming?",
                   "12 children", ["26 children", "13 children", "11 children"],
                   "Getting out means take away. 19 is 10 and 9. 9 %s 7 = 2. 10 and 2 is 12. 19 %s 7 = <b>12</b>." % (MINUS, MINUS)))
    assert solve("? %s 5 = 8" % MINUS) == 13
    its.append(mcq("Some kangaroos are in a paddock. 5 hop away. Now 8 are left. How many kangaroos were there at the start?",
                   "13 kangaroos", ["3 kangaroos", "12 kangaroos", "14 kangaroos"],
                   "Put back the 5 that hopped away: 8 + 5 = <b>13</b>. Check: 13 %s 5 = 8. (8 %s 5 = 3 is the wrong way.)"
                   % (MINUS, MINUS)))
    assert swap_mistake(14, 9) == 15
    its.append(mcq("Charlotte has 14 shells. William has 9 shells. What is the difference?",
                   "5 shells", ["23 shells", "15 shells", "6 shells"],
                   "Count up from 9 to 14: 10, 11, 12, 13, 14. That is <b>5</b>. 14 %s 9 = 5." % MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Subtract: take away and find the difference", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add: put together and count on</h2>"
        "<p>Adding means putting groups together. The sign is <b>+</b>. Say “add” or “plus”.</p>"
        "<p>You can count all of them. It is faster to start at the bigger number and <b>count on</b>.</p>"
        "<figure class='sn-fig'>" + two_groups_svg(5, 3, "apple") +
        "<figcaption>5 apples and 3 apples. Start at 5. Count on 3: 6, 7, 8. So 5 + 3 = 8.</figcaption></figure>"
        + ex("Count on", "9 + 3 = ?", "Say 9. Then count 3 more: 10, 11, 12.", "12") +
        "<h2>Number bonds to 10</h2>"
        "<p>Two parts make a whole. These pairs make 10. Learn them well. They help with bigger numbers.</p>"
        "<figure class='sn-fig'>" + frames_svg(7, 3) +
        "<figcaption>7 red and 3 green fill the ten frame. 7 + 3 = 10.</figcaption></figure>"
        + table(["Number bond to 10", "Turned around"], [["1 + 9", "9 + 1"], ["2 + 8", "8 + 2"], ["3 + 7", "7 + 3"],
                                                         ["4 + 6", "6 + 4"], ["5 + 5", "5 + 5 is a double"]]) +
        "<h2>Count back on a number line</h2>"
        "<p>Subtracting means taking away. The sign is <b>−</b>. Say “take away” or “minus”. "
        "On a number line, start at the first number and jump back.</p>"
        "<figure class='sn-fig'>" + number_line_svg(8, 14, hops=[(13, 10), (10, 9)], step=40) +
        "<figcaption>13 − 4. Jump back 3 to 10. Then jump back 1 more to 9. So 13 − 4 = 9.</figcaption></figure>"
        "<h2>Doubles and make ten</h2>"
        "<p>A <b>double</b> adds a number to itself: 6 + 6 = 12. A near double is 1 more: 6 + 7 = 13.</p>"
        "<figure class='sn-fig'>" + dominoes_svg([(5, 5), (5, 6)]) +
        "<figcaption>5 + 5 = 10. The second domino has 1 more dot. So 5 + 6 = 11.</figcaption></figure>"
        "<p>To <b>make ten</b>, fill a ten frame first. Then add what is left.</p>"
        "<figure class='sn-fig'>" + frames_svg(8, 6) +
        "<figcaption>8 + 6. 2 of the green fill the first frame. 4 are left. 8 + 6 = 10 + 4 = 14.</figcaption></figure>"
        "<h2>Take away or find the difference</h2>"
        "<p>Take away: cross some out and count what is left.</p>"
        "<figure class='sn-fig'>" + take_svg(8, 3, "ball") +
        "<figcaption>8 balls. Cross out 3. 5 balls are left. So 8 − 3 = 5.</figcaption></figure>"
        "<p>Find the difference: line up two groups. Count the extra ones. Or count up from the smaller number.</p>"
        "<figure class='sn-fig'>" + compare_svg(7, "Ava", 4, "Ethan", "star") +
        "<figcaption>Ava has 7 stars. Ethan has 4. 3 stars have no partner. The difference is 3. 7 − 4 = 3.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the start number: 9 + 3 → “9, 10, 11”, so 11", "Say 9, then count 3 more: 10, 11, 12. 9 + 3 = 12"],
            ["Adding when you should take away: 12 − 5 = 17", "Look at the sign. Words like “left” and “fewer” mean subtract"],
            ["Taking the small digit from the big one: 12 − 5 = 13", "Go back to 10 first: 12 − 2 = 10, then 10 − 3 = 7"],
            ["Writing 10 + 4 as 104", "10 + 4 is 1 ten and 4 ones. That is 14"],
            ["Adding to find the difference: 9 and 6 → 15", "Difference means how many more. 9 − 6 = 3"],
        ])
    )


FAQ = [
    {"q": "What addition and subtraction does Year 1 learn in the Australian Curriculum?",
     "a": "Year 1 students add and subtract numbers within 20 (AC9M1N04). They use objects, ten frames, part-part-whole knowledge to 10 and strategies such as counting on, counting back, doubles and making ten."},
    {"q": "What are number bonds to 10?",
     "a": "They are the pairs of numbers that make 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6 and 5 + 5, and the same pairs turned around. Many Australian classrooms call them “friends of ten” or “rainbow facts”."},
    {"q": "What is the make ten strategy?",
     "a": "Fill up a ten first, then add the rest. For 8 + 6, take 2 from the 6 to make 10, so 8 + 6 = 10 + 4 = 14."},
    {"q": "How can I help my Year 1 child with adding and subtracting at home?",
     "a": "Use 10 to 20 small objects, a ten frame or a dice game for a few minutes a day. Ask questions like “I have 6. How many more make 10?” and “How many more does Jack have than Mia?”"},
]


# ============================================================ checks
def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.match(r"^\$?\d+( [a-z ]+)?$", c) for c in it["c"]):
                vals = [c.lstrip("$").split(" ")[0] for c in it["c"]]
                assert len(set(vals)) == 4, it["c"]
                assert all(0 < int(v) for v in vals), it["c"]
            key = re.sub(r"<[^>]+>", " ", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            assert it["q"].count("<svg") <= 1
            for t in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in t and '"' not in t and ".." not in t, t
                assert not re.search(r"(?<![\d$])\b1 [a-z]+s\b", re.sub(r"<[^>]+>", " ", t)), t
            # a number sentence with one ? on the last line: the answer solves it
            last = re.sub(r"<[^>]+>", "", re.split(r"<br>", it["q"])[-1]).strip()
            if re.fullmatch(r"[\d?]+( [+−] [\d?]+)* = [\d?]+( [+−] [\d?]+)*", last) and last.count("?") == 1:
                assert it["c"][it["a"]].split()[0] == str(solve(last)), (last, it["c"])
            # 'which number sentence' answers are true
            right = it["c"][it["a"]]
            if re.fullmatch(r"\d+ [+−] \d+ = \d+", right):
                assert eq_true(right), right
            # pictures match their labels
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+ and (\d+) [a-z ]+'", it["q"]):
                assert it["q"].count("data-o='1'") == int(m.group(1)) + int(m.group(2))
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+, (\d+) crossed out'", it["q"]):
                assert it["q"].count("data-o='1'") == int(m.group(1))
                assert it["q"].count("data-x='1'") == int(m.group(2))


def gen():
    rnd = random.Random(1803)
    sets = [set_add(), set_bonds(), set_lines(), set_doubles(), set_subtract()]
    balance(sets, rnd)
    check(sets)
    u_ = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "addition-and-subtraction-within-20", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction within 20",
        "seo_title": "Year 1 Addition and Subtraction within 20 Worksheets: Number Bonds, Doubles and Make Ten",
        "short_title": "Addition and subtraction within 20",
        "domain": "Number",
        "standard_code": "AC9M1N04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Add and subtract numbers within 20, using physical and virtual materials, part-part-whole "
                         "knowledge to 10 and a variety of calculation strategies",
        "meta_desc": "Free Year 1 maths worksheets on addition and subtraction within 20, matched to the Australian "
                     "Curriculum (AC9M1N04): adding with pictures and ten frames, number bonds to 10, counting on and back "
                     "on a number line, doubles, make ten, taking away and finding the difference. 100 questions with an answer key.",
        "key_big": "Add: count on. Take away: count back. Know your bonds to 10.",
        "key_sub": "9 + 3: say 9, then count 10, 11, 12. 8 + 6: fill a ten first, so 10 + 4 = 14. "
                   "13 − 4: go back to 10, then 1 more to 9.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u_, "picture|number line|two ten frames|dominoes")


if __name__ == "__main__":
    u_ = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u_["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u_, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
