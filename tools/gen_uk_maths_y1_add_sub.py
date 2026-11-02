# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Addition and subtraction within 20 (National Curriculum in England)
  python3 tools/gen_uk_maths_y1_add_sub.py
Pictures to count, number tracks, number lines and ten frames. Number sentences with + − =,
missing numbers (7 = ? − 9) and one-step stories.
Every answer, every picture count and every number sentence is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
Q = "<b>?</b>"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", pink="#e86aa6", brown="#c68a4a")
ZERO_QS = []          # questions that use + 0 / − 0 (at most 3)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, zero_ok=False):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or c.startswith("-"):
            continue
        if not zero_ok and re.match(r"^0\b|^0p$", c):
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
    """Tag wide pictures (rows of objects, tracks, lines, ten frames) so they print larger."""
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


def show(eq):
    return eq.replace("?", Q)


def on_list(a, b):
    return ", ".join(str(a + i) for i in range(1, b + 1))


def back_list(a, b):
    return ", ".join(str(a - i) for i in range(1, b + 1))


NAMES = dict(apple=("apple", "apples"), star=("star", "stars"), ball=("ball", "balls"), flower=("flower", "flowers"),
             block=("block", "blocks"), biscuit=("biscuit", "biscuits"), balloon=("balloon", "balloons"),
             car=("toy car", "toy cars"), duck=("duck", "ducks"), fish=("fish", "fish"))


def nm(n, kind):
    s, p = NAMES[kind]
    return "%d %s" % (n, s if n == 1 else p)


def u(n, sing, plur):
    return "%d %s" % (n, sing if n == 1 else plur)


# ------------------------------------------------------------ pictures: objects (each fits a 28 x 28 cell)
PITCH = 28
DEF_COL = dict(apple="red", star="gold", fish="orange", ball="blue", flower="pink", block="green",
               biscuit="brown", balloon="red", car="blue", duck="yellow")


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


def group_body(x0, y0, n, kind, cols=5, gap5=0):
    """n objects in rows of `cols`; an extra gap after every 5 in a row (like a ten frame)."""
    s, centres = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * PITCH + PITCH / 2 + (gap5 if c >= 5 else 0)
        cy = y0 + r * PITCH + PITCH / 2
        centres.append((cx, cy))
        s.append(obj(kind, cx, cy))
    ncol = min(n, cols)
    w = ncol * PITCH + (gap5 if ncol > 5 else 0)
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
    body, w, h, cen = group_body(o, o, n, kind, cols=10, gap5=8)
    col = INK if DEF_COL[kind] == "red" else RED          # a red cross would hide on a red apple
    xs = "".join(cross(cx, cy, col) for cx, cy in cen[n - k:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %s, %d crossed out" % (nm(n, kind), k))
    assert svg.count("<g data-o='1'>") == n and svg.count("<g data-x='1'>") == k
    return svg


# ------------------------------------------------------------ pictures: number track, number line, ten frames
B = 30


def track_svg(lo, hi, start=None, end=None):
    """Number track: numbered squares lo..hi. start: green square. end: pink square."""
    o = 6
    s = []
    for v in range(lo, hi + 1):
        x = o + (v - lo) * B
        fill = FILL if v == start else PINK if v == end else "#ffffff"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, o, B, B, fill, INK))
        s.append(text(x + B / 2, o + 21, str(v), 15))
    label = "number track from %d to %d" % (lo, hi)
    if start is not None:
        label += ", %d is green" % start
    if end is not None:
        label += ", %d is pink" % end
    return svg_wrap((hi - lo + 1) * B + 2 * o, B + 2 * o, "".join(s), label)


def number_line_svg(lo, hi, start=None, hops=(), step=30):
    """Number line lo..hi. start: green dot. hops: list of (from, to) arcs with a +/− label."""
    L, Y = 18, 66 if hops else 22
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    for a, b in hops:
        mid = (X(a) + X(b)) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (X(a), Y - 9, mid, Y - 54, X(b), Y - 9, GREEN))
        s.append(text(mid, Y - 36, ("+%d" if b > a else MINUS + "%d") % abs(b - a), 16, col=GREEN))
    if start is not None:
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, GREEN))
    label = "number line from %d to %d" % (lo, hi) + (" with a dot on %d" % start if start is not None else "")
    return svg_wrap(W, Y + 34, "".join(s), label)


CELL = 30
FW, FH = 5 * CELL, 2 * CELL


def frame(x0, y0, colours):
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
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s'/>"
                 % (x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2, col))
    return "".join(s)


def frames_svg(a, b):
    """a red then b green counters, filling the first ten frame before the second."""
    cols = [RED] * a + [GREEN] * b
    assert a + b <= 20
    o, gap = 6, 12
    W, H = 2 * FW + gap + 2 * o, FH + 2 * o
    body = frame(o, o, cols[:10]) + frame(o + FW + gap, o, cols[10:])
    svg = svg_wrap(W, H, body, "ten frames with %d red and %d green counters" % (a, b))
    assert svg.count("<circle") == a + b
    return svg


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
    return "Go back to 10 first: %d %s %d = 10. Then take away %d more: 10 %s %d = <b>%d</b>." % (
        a, MINUS, part, b - part, MINUS, b - part, a - b)


def swap_mistake(a, b):
    """Teen number take away ones, where the pupil takes the smaller digit from the larger: 12 − 5 → 13."""
    assert 10 < a < 20 and b < 10
    return 10 + abs(a - 10 - b)


# ============================================================ set 1: add
def set_add():
    its = []
    for kind, a, b in [("apple", 3, 2), ("duck", 4, 3), ("car", 5, 4), ("ball", 6, 3),
                       ("star", 7, 5), ("flower", 8, 6), ("biscuit", 9, 4)]:
        s = a + b
        plur = NAMES[kind][1]
        q = fig(two_groups_svg(a, b, kind)) + "How many %s altogether?<br>%d + %d = %s" % (plur, a, b, Q)
        e = "Count all the %s. Or start at %d and count on %d: %s. %d + %d = <b>%d</b>." % (
            plur, a, b, on_list(a, b), a, b, s)
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), b], e))

    for a, b in [(7, 4), (8, 5), (9, 6), (10, 7)]:
        s = a + b
        q = fig(frames_svg(a, b)) + "How many counters altogether?<br>%d + %d = %s" % (a, b, Q)
        if a == 10:
            e = "The first ten frame is full: 10. The second has %d. 10 + %d = <b>%d</b>." % (b, b, s)
        else:
            e = ("%d red and %d green. Now the first ten frame is full: 10. The second has %d. 10 + %d = %d. "
                 "So %d + %d = <b>%d</b>." % (a, b, s - 10, s - 10, s, a, b, s))
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), 10], e))

    for a, b in [(6, 4), (9, 3), (11, 5), (13, 4), (8, 7), (15, 3)]:
        s = a + b
        hi = min(20, max(a + 9, s + 2))
        lo = hi - 11
        assert lo < a and s < hi
        q = fig(track_svg(lo, hi, start=a)) + "Start on %d. Jump on %d.<br>%d + %d = %s" % (a, b, a, b, Q)
        e = "Start on %d. Jump on %d squares: %s. Do not count the %d. %d + %d = <b>%d</b>." % (
            a, b, on_list(a, b), a, a, b, s)
        its.append(mcq(q, s, [s - 1, s + 1, b, abs(a - b)], e))

    q = "7 + 0 = %s" % Q
    ZERO_QS.append(q)
    its.append(mcq(q, 7, [8, 0, 70], "Adding 0 adds nothing. The number stays the same. 7 + 0 = <b>7</b>.", zero_ok=True))
    its.append(mcq("3 + 9 = %s" % Q, 12, [11, 13, 6],
                   "Start with the bigger number, 9. Count on 3: 10, 11, 12. 3 + 9 = <b>12</b>."))
    its.append(mcq("8 + 8 = %s" % Q, 16, [15, 17, 14],
                   "8 + 8 is a double. 8 + 2 = 10, and 6 more is 16. 8 + 8 = <b>16</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Add with pictures and a number track", "items": its}


# ============================================================ set 2: subtract
def set_sub():
    its = []
    for kind, n, k in [("apple", 5, 2), ("duck", 7, 3), ("balloon", 8, 4), ("fish", 9, 5),
                       ("car", 10, 6), ("block", 12, 4), ("biscuit", 15, 7)]:
        d = n - k
        plur = NAMES[kind][1]
        q = (fig(take_svg(n, k, kind))
             + "Some %s are crossed out. How many are left?<br>%d %s %d = %s" % (plur, n, MINUS, k, Q))
        e = "There are %s. %d %s crossed out. Count the ones with no cross: <b>%d</b>. %d %s %d = %d." % (
            nm(n, kind), k, "is" if k == 1 else "are", d, n, MINUS, k, d)
        its.append(mcq(q, d, [n + k, k, d + 1, d - 1], e))

    for a, b in [(9, 3), (12, 4), (14, 5), (16, 3), (11, 4), (18, 6)]:
        d = a - b
        hi = min(20, a + 2)
        lo = hi - 10
        assert lo < d
        q = fig(number_line_svg(lo, hi, start=a)) + "Start at %d. Count back %d.<br>%d %s %d = %s" % (a, b, a, MINUS, b, Q)
        its.append(mcq(q, d, [d + 1, a + b, d - 1], back_e(a, b)))

    q = "9 %s 0 = %s" % (MINUS, Q)
    ZERO_QS.append(q)
    its.append(mcq(q, 9, [8, 0, 10], "Taking away 0 takes nothing away. 9 %s 0 = <b>9</b>." % MINUS, zero_ok=True))

    its.append(mcq("13 %s 3 = %s" % (MINUS, Q), 10, [16, 11, 9],
                   "13 is 10 and 3. Take away the 3, and 10 is left. 13 %s 3 = <b>10</b>." % MINUS))
    its.append(mcq("17 %s 5 = %s" % (MINUS, Q), 12, [22, 13, 11],
                   "17 is 10 and 7. Take 5 from the 7: 7 %s 5 = 2. 10 and 2 is <b>12</b>." % MINUS))
    for a, b in [(12, 5), (15, 7), (14, 8), (16, 9)]:
        d = a - b
        its.append(mcq("%d %s %d = %s" % (a, MINUS, b, Q), d, [swap_mistake(a, b), a + b, d + 1, d - 1],
                       via10_e(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Take away and count back", "items": its}


# ============================================================ set 3: read and write number sentences
def sent_item(q, right, wrong, e, want_true=True, match=False):
    """match=True: a picture question. The wrong sentences may be true sums, but they never use
    the picture's two numbers with the picture's sign and the right total."""
    assert eq_true(right) == want_true, right
    for w in wrong:
        if match:
            assert w != right and not (eq_true(w) and sorted(w.split()[0:3:2]) == sorted(right.split()[0:3:2])
                                       and w.split()[1] == right.split()[1]), w
        else:
            assert eq_true(w) != want_true, w
    return mcq(q, right, wrong, e)


def set_sentences():
    its = []
    for kind, a, b in [("apple", 5, 3), ("car", 6, 2), ("star", 3, 6), ("balloon", 8, 5)]:
        s = a + b
        big, small = max(a, b), min(a, b)
        right = "%d + %d = %d" % (a, b, s)
        wrong = ["%d %s %d = %d" % (big, MINUS, small, big - small), "%d + %d = %d" % (a, b, s + 1),
                 "%d + %d = %d" % (s, b, s + b)]
        q = fig(two_groups_svg(a, b, kind)) + "Which number sentence matches the picture?"
        e = "%s and %s go together, so add. That makes %d. <b>%s</b>." % (nm(a, kind), nm(b, kind), s, right)
        its.append(sent_item(q, right, wrong, e, match=True))
    for kind, n, k in [("ball", 9, 4), ("fish", 7, 2), ("apple", 10, 3)]:
        d = n - k
        right = "%d %s %d = %d" % (n, MINUS, k, d)
        wrong = ["%d + %d = %d" % (n, k, n + k), "%d %s %d = %d" % (n, MINUS, k, d + 1),
                 "%d %s %d = %d" % (d, MINUS, k, d - k)]
        q = fig(take_svg(n, k, kind)) + "Which number sentence matches the picture?"
        e = "There are %s. %d %s crossed out, so take away. %d are left. <b>%s</b>." % (
            nm(n, kind), k, "is" if k == 1 else "are", d, right)
        its.append(sent_item(q, right, wrong, e, match=True))

    q = fig(frames_svg(10, 4)) + "Which number sentence matches the ten frames?"
    its.append(sent_item(q, "10 + 4 = 14", ["10 %s 4 = 6" % MINUS, "10 + 4 = 15", "4 + 4 = 8"],
                         "10 red counters and 4 green counters. Put them together: <b>10 + 4 = 14</b>.", match=True))
    q = fig(number_line_svg(0, 10, hops=[(8, 5)])) + "Which number sentence matches the jump?"
    its.append(sent_item(q, "8 %s 3 = 5" % MINUS, ["8 + 3 = 11", "8 %s 3 = 4" % MINUS, "5 %s 3 = 2" % MINUS],
                         "The jump starts at 8. It goes back 3 and lands on 5. <b>8 %s 3 = 5</b>." % MINUS, match=True))
    q = fig(number_line_svg(4, 14, hops=[(6, 11)])) + "Which number sentence matches the jump?"
    its.append(sent_item(q, "6 + 5 = 11", ["6 %s 5 = 1" % MINUS, "6 + 5 = 12", "11 + 5 = 16"],
                         "The jump starts at 6. It goes on 5 and lands on 11. <b>6 + 5 = 11</b>.", match=True))

    its.append(mcq("What does the = sign mean?", "is the same as", ["add", "take away", "write the answer next"],
                   "= means <b>is the same as</b>. Both sides have the same value: 4 + 3 = 7 and 7 = 4 + 3."))

    words = [
        ("Which one says “eleven take away three equals eight”?", "11 %s 3 = 8" % MINUS,
         ["11 + 3 = 8", "3 %s 11 = 8" % MINUS, "11 %s 8 = 3" % MINUS],
         "Eleven is 11. Take away is %s. Three is 3. Equals is =. Eight is 8. <b>11 %s 3 = 8</b>." % (MINUS, MINUS)),
        ("Which one says “six add seven equals thirteen”?", "6 + 7 = 13",
         ["6 %s 7 = 13" % MINUS, "6 + 7 = 31", "6 + 13 = 7"],
         "Add is +. Equals is =. Thirteen is 13: 1 ten and 3 ones. <b>6 + 7 = 13</b>."),
        ("Which one says “twenty is equal to twelve add eight”?", "20 = 12 + 8",
         ["20 + 12 = 8", "20 = 12 %s 8" % MINUS, "12 = 20 + 8"],
         "Write the words in order. Twenty, is equal to, twelve, add, eight: <b>20 = 12 + 8</b>."),
    ]
    for q, right, wrong, e in words:
        its.append(sent_item(q, right, wrong, e, match=True))

    truths = [
        ("Which number sentence is true?", "9 + 6 = 15", ["9 + 6 = 14", "9 %s 6 = 15" % MINUS, "15 + 6 = 9"],
         "9 + 6: start at 9 and count on 6: 10, 11, 12, 13, 14, 15. <b>9 + 6 = 15</b> is true."),
        ("Look at both sides of the =. Which one is true?", "14 = 8 + 6", ["14 = 8 + 7", "8 + 6 = 15", "14 + 8 = 6"],
         "8 + 6 = 14. The = can come first: <b>14 = 8 + 6</b> is true."),
        ("Check each one. Which is true?", "17 %s 9 = 8" % MINUS,
         ["17 %s 9 = 12" % MINUS, "17 + 9 = 8", "17 %s 8 = 10" % MINUS],
         "Think addition: 9 + 8 = 17. So <b>17 %s 9 = 8</b> is true." % MINUS),
    ]
    for q, right, wrong, e in truths:
        its.append(sent_item(q, right, wrong, e))
    its.append(sent_item("Which number sentence is NOT true?", "13 %s 4 = 8" % MINUS,
                         ["13 %s 4 = 9" % MINUS, "9 + 4 = 13", "13 = 9 + 4"],
                         "13 %s 4 is 9, not 8. So <b>13 %s 4 = 8</b> is not true. The other three are true."
                         % (MINUS, MINUS), want_true=False))

    its.append(sent_item("12 = 7 + 5. Which one means the same?", "7 + 5 = 12",
                         ["12 + 7 = 5", "12 %s 7 = 6" % MINUS, "7 %s 5 = 12" % MINUS],
                         "= means “is the same as”. You can swap the two sides: <b>7 + 5 = 12</b>."))
    its.append(sent_item("10 %s 3 = 7. Which one means the same?" % MINUS, "7 = 10 %s 3" % MINUS,
                         ["7 = 3 %s 10" % MINUS, "10 = 7 %s 3" % MINUS, "7 %s 3 = 10" % MINUS],
                         "Swap the two sides of the =. 10 %s 3 is the same as 7: <b>7 = 10 %s 3</b>." % (MINUS, MINUS)))
    assert len(its) == 20, len(its)
    return {"title": "Read and write number sentences", "items": its}


# ============================================================ set 4: missing numbers
def miss_item(eq, cands, e, pic="", lead="", zero=False):
    k = solve(eq)
    q = pic + lead + show(eq)
    if zero:
        ZERO_QS.append(q)
    else:
        assert k > 0, eq
    return mcq(q, k, cands, e, zero_ok=zero)


def set_missing():
    its = []
    for a, c in [(7, 12), (9, 15), (6, 13)]:
        k = c - a
        hi = min(20, c + 3)
        lo = hi - 11
        assert lo < a
        its.append(miss_item("%d + ? = %d" % (a, c), [c, a + c, k + 1, k - 1],
                             "Start on %d. Count the jumps to %d: %s. That is <b>%d</b> jumps. %d + %d = %d." % (
                                 a, c, on_list(a, k), k, a, k, c),
                             pic=fig(track_svg(lo, hi, start=a, end=c)),
                             lead="Start on %d. How many jumps to %d?<br>" % (a, c)))
    for kind, n, k in [("ball", 11, 4), ("apple", 9, 3)]:
        d = n - k
        its.append(miss_item("%d %s ? = %d" % (n, MINUS, d), [d, n + d, k + 1, k - 1],
                             "%s are crossed out. %d %s %d = %d. The missing number is <b>%d</b>." % (
                                 cap(str(k)), n, MINUS, k, d, k),
                             pic=fig(take_svg(n, k, kind)), lead="How many %s are crossed out?<br>" % NAMES[kind][1]))

    for a, c in [(4, 9), (8, 17), (11, 19)]:
        k = c - a
        its.append(miss_item("%d + ? = %d" % (a, c), [a + c, c, k + 1, k - 1],
                             "Count on from %d to %d: %s. That is <b>%d</b>. Check: %d + %d = %d." % (
                                 a, c, on_list(a, k), k, a, k, c)
                             if k <= 5 else
                             "Think: %d %s %d = %d. So the missing number is <b>%d</b>. Check: %d + %d = %d." % (
                                 c, MINUS, a, k, k, a, k, c)))
    its.append(miss_item("8 + ? = 8", [8, 16, 1],
                         "8 is already 8. Nothing more is added. 8 + <b>0</b> = 8.", zero=True))
    for b, c in [(4, 9), (6, 14), (9, 16)]:
        k = c - b
        its.append(miss_item("? + %d = %d" % (b, c), [b + c, c, k + 1, b],
                             "Think: %d %s %d = %d. The missing number is <b>%d</b>. Check: %d + %d = %d." % (
                                 c, MINUS, b, k, k, k, b, c)))
    for c, a in [(15, 10), (18, 9)]:
        k = c - a
        its.append(miss_item("%d = %d + ?" % (c, a), [a + c, c, k + 1],
                             "= means “is the same as”. %d + %d = %d, so the missing number is <b>%d</b>." % (
                                 a, k, c, k)))
    for a, c in [(12, 5), (16, 10)]:
        k = a - c
        its.append(miss_item("%d %s ? = %d" % (a, MINUS, c), [a + c, c, k + 1],
                             "Count up from %d to %d: %d + %d = %d. So %d %s <b>%d</b> = %d." % (
                                 c, a, c, k, a, a, MINUS, k, c)))
    for b, c in [(3, 8), (6, 7)]:
        k = b + c
        its.append(miss_item("? %s %d = %d" % (MINUS, b, c), [abs(c - b), c, k + 1],
                             "Put back the %d: %d + %d = <b>%d</b>. Check: %d %s %d = %d." % (
                                 b, c, b, k, k, MINUS, b, c)))
    for c, b in [(7, 9), (5, 8)]:
        k = b + c
        its.append(miss_item("%d = ? %s %d" % (c, MINUS, b), [abs(b - c), c, k - 1],
                             "Which number take away %d leaves %d? Add them: %d + %d = <b>%d</b>. Check: %d %s %d = %d." % (
                                 b, c, c, b, k, k, MINUS, b, c)))
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def person():
        n, he, his = P.next()
        return dict(N=n, he=he, He=cap(he), his=his, him="her" if he == "she" else "him")

    def other(p):
        while True:
            m = P.next()[0]
            if m != p["N"]:
                return m

    add, take = "More come, so add. ", "Some go away, so subtract. "

    # with pictures
    its.append(mcq(fig(two_groups_svg(6, 5, "duck"))
                   + "There are 6 ducks on a pond. 5 more ducks land. How many ducks are on the pond now?",
                   "11 ducks", ["10 ducks", "12 ducks", "1 duck"], add + on_e(6, 5)))
    p = person()
    its.append(mcq(fig(two_groups_svg(9, 6, "car"))
                   + "{N} has 9 toy cars. {He} gets 6 more for {his} birthday. How many toy cars does {he} have now?".format(**p),
                   "15 toy cars", ["14 toy cars", "16 toy cars", "3 toy cars"],
                   "More cars, so add. 9 + 1 = 10, and 5 more is 15. 9 + 6 = <b>15</b>."))
    its.append(mcq(fig(take_svg(14, 6, "duck"))
                   + "There are 14 ducks on a pond. 6 ducks fly away. How many ducks are left?",
                   "8 ducks", ["20 ducks", "9 ducks", "12 ducks"], take + via10_e(14, 6)))
    assert swap_mistake(14, 6) == 12
    its.append(mcq(fig(take_svg(15, 7, "biscuit"))
                   + "There are 15 biscuits on a plate. The children eat 7. How many biscuits are left?",
                   "8 biscuits", ["22 biscuits", "9 biscuits", "12 biscuits"],
                   "Eaten biscuits are gone, so subtract. " + via10_e(15, 7)))
    assert swap_mistake(15, 7) == 12

    # add / take away stories
    p = person()
    its.append(mcq("{N} has 12 apples. {He} gives 4 to Gran. How many apples does {he} have now?".format(**p),
                   "8 apples", ["16 apples", "9 apples", "7 apples"],
                   "Giving away means subtract. " + back_e(12, 4)))
    p = person()
    m = other(p)
    its.append(mcq("{N} has 8 stickers. {M} has 7 stickers. How many stickers do they have altogether?".format(M=m, **p),
                   "15 stickers", ["14 stickers", "16 stickers", "1 sticker"],
                   "Altogether means add. 8 + 7 is 1 more than 7 + 7 = 14. 8 + 7 = <b>15</b>."))
    its.append(mcq("There are 17 people on a bus. 5 people get off. How many people are on the bus now?",
                   "12 people", ["22 people", "13 people", "11 people"],
                   "Getting off means subtract. 17 is 10 and 7. 7 %s 5 = 2. 10 and 2 is 12. 17 %s 5 = <b>12</b>." % (MINUS, MINUS)))
    its.append(mcq("A bag has 10 red sweets and 9 yellow sweets. How many sweets are in the bag?",
                   "19 sweets", ["18 sweets", "20 sweets", "1 sweet"],
                   "Put the two colours together, so add. 10 + 9 is 1 ten and 9 ones. 10 + 9 = <b>19</b>."))
    p = person()
    its.append(mcq("{N} has 20p. {He} spends 6p on a lolly. How much money does {he} have left?".format(**p),
                   "14p", ["26p", "15p", "13p"],
                   "Spending means subtract. 20 %s 6: 20 is 10 and 10. 10 %s 6 = 4. 10 and 4 is 14. So <b>14p</b>." % (MINUS, MINUS)))
    p = person()
    its.append(mcq("{N} reads 7 pages before lunch. {He} reads 8 pages after lunch. How many pages does {he} read?".format(**p),
                   "15 pages", ["14 pages", "16 pages", "1 page"],
                   "Put the pages together, so add. 7 + 7 = 14, and 8 is 1 more than 7. 7 + 8 = <b>15</b>."))
    its.append(mcq("There are 19 books on a shelf. The class takes 5 books. How many books are left?",
                   "14 books", ["24 books", "15 books", "13 books"],
                   "Taking books away means subtract. 19 is 10 and 9. 9 %s 5 = 4. 10 and 4 is 14. 19 %s 5 = <b>14</b>." % (MINUS, MINUS)))
    p = person()
    its.append(mcq("{N} is 6. {His} brother is 3 years older. How old is {his} brother?".format(His=cap(p["his"]), **p),
                   "9 years old", ["3 years old", "8 years old", "10 years old"],
                   "Older means more years, so add. Start at 6. Count on 3: 7, 8, 9. 6 + 3 = <b>9</b>."))

    # missing number stories
    p = person()
    its.append(mcq("{N} has 6 conkers. {He} wants 13. How many more conkers does {he} need?".format(**p),
                   "7 conkers", ["19 conkers", "13 conkers", "8 conkers"],
                   "Think: 6 + ? = 13. 6 + 4 = 10, then 3 more is 13. 4 + 3 = 7. 6 + <b>7</b> = 13."))
    assert solve("6 + ? = 13") == 7
    its.append(mcq("There are 11 children in the playground. Some go inside. Now there are 4. How many children went inside?",
                   "7 children", ["15 children", "4 children", "8 children"],
                   "Think: 11 %s ? = 4. Count up from 4 to 11: 4 + 7 = 11. So <b>7</b> children went inside." % MINUS))
    assert solve("11 %s ? = 4" % MINUS) == 7
    its.append(mcq("Some ducks are on a pond. 5 more ducks come. Now there are 12 ducks. How many ducks were there at the start?",
                   "7 ducks", ["17 ducks", "12 ducks", "8 ducks"],
                   "Think: ? + 5 = 12. Take away the 5 that came: 12 %s 5 = <b>7</b>. Check: 7 + 5 = 12." % MINUS))
    assert solve("? + 5 = 12") == 7
    p = person()
    m = other(p)
    its.append(mcq("{N} has 13 marbles. {M} has 8 marbles. How many more marbles does {N} have than {M}?".format(M=m, **p),
                   "5 marbles", ["21 marbles", "8 marbles", "6 marbles"],
                   "Find the difference. Count up from 8 to 13: 9, 10, 11, 12, 13. That is <b>5</b> more."))
    its.append(mcq("There are 16 pencils in a pot. 9 are blue. The rest are red. How many pencils are red?",
                   "7 pencils", ["25 pencils", "9 pencils", "8 pencils"],
                   "Think: 9 + ? = 16. 9 + 1 = 10, then 6 more is 16. 1 + 6 = 7. So <b>7</b> are red."))

    # which number sentence?
    its.append(sent_item("18 children are in a class. 3 are away today. How many are at school? Which number sentence matches?",
                         "18 %s 3 = 15" % MINUS, ["18 + 3 = 21", "18 %s 3 = 16" % MINUS, "15 %s 3 = 12" % MINUS],
                         "3 children are away, so take them away from 18. <b>18 %s 3 = 15</b>." % MINUS, match=True))
    p = person()
    its.append(sent_item("{N} has 5 balloons. {He} gets 9 more. Which number sentence matches?".format(**p),
                         "5 + 9 = 14", ["9 %s 5 = 4" % MINUS, "5 + 9 = 13", "14 + 9 = 23"],
                         "{He} gets more, so add. <b>5 + 9 = 14</b>.".format(**p), match=True))
    p = person()
    its.append(sent_item("{N} has 15 grapes. {He} eats some. Now {he} has 9. Which number sentence matches?".format(**p),
                         "15 %s 6 = 9" % MINUS, ["15 + 6 = 9", "9 %s 6 = 15" % MINUS, "15 + 9 = 6"],
                         ("{He} starts with 15. {He} eats some, so take away. 9 are left, so {he} ate 6: "
                          "<b>15 − 6 = 9</b>.").format(**p), match=True))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Adding: put together</h2>"
        "<p>Adding means putting groups together. The sign is <b>+</b>. Say “add” or “plus”.</p>"
        "<p>You can count all of them. Or start at the first number and <b>count on</b>.</p>"
        "<figure class='sn-fig'>" + two_groups_svg(5, 3, "apple") +
        "<figcaption>5 apples and 3 apples. Start at 5. Count on 3: 6, 7, 8. So 5 + 3 = 8.</figcaption></figure>"
        "<figure class='sn-fig'>" + track_svg(7, 16, start=9) +
        "<figcaption>9 + 3 on a number track. Start on 9. Jump on 3 squares: 10, 11, 12. So 9 + 3 = 12.</figcaption></figure>"
        + ex("Count on", "6 + 4 = ?", "Say 6. Then count 4 more: 7, 8, 9, 10.", "10") +
        "<h2>Subtracting: take away</h2>"
        "<p>Subtracting means taking away. The sign is <b>−</b>. Say “take away” or “minus”.</p>"
        "<figure class='sn-fig'>" + take_svg(8, 3, "ball") +
        "<figcaption>8 balls. Cross out 3. 5 balls are left. So 8 − 3 = 5.</figcaption></figure>"
        "<p>You can also <b>count back</b> on a number line.</p>"
        "<figure class='sn-fig'>" + number_line_svg(8, 14, hops=[(13, 10), (10, 9)], step=40) +
        "<figcaption>13 − 4. Go back 3 to 10. Then go back 1 more to 9. So 13 − 4 = 9.</figcaption></figure>"
        "<h2>Reading number sentences</h2>"
        "<p>A number sentence uses numbers and signs. <b>=</b> means “is the same as”. "
        "Both sides of the = have the same value.</p>"
        + table(["Sign", "Say", "Example"], [
            ["+", "add, plus", "4 + 3 = 7"],
            ["−", "take away, minus", "9 − 2 = 7"],
            ["=", "equals, is the same as", "7 = 4 + 3"],
        ]) +
        "<p>Adding 0 or taking away 0 does not change a number: 6 + 0 = 6 and 6 − 0 = 6.</p>"
        "<h2>Missing numbers</h2>"
        "<p>Sometimes a number is missing. Use the other two numbers to find it.</p>"
        + ex("Missing number", "? + 4 = 9", "Something add 4 makes 9. Take the 4 away: 9 − 4 = 5.", "5")
        + ex("Missing number", "7 = ? − 9", "Which number take away 9 leaves 7? Put the 9 back: 7 + 9 = 16. Check: 16 − 9 = 7.", "16") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the start number: 9 + 3 → “9, 10, 11”, so 11", "Say 9, then count 3 more: 10, 11, 12. 9 + 3 = 12"],
            ["Adding when you should take away: 12 − 5 = 17", "Look at the sign. − means take away: 12 − 5 = 7"],
            ["Taking the small digit from the big one: 12 − 5 = 13", "Go back to 10 first: 12 − 2 = 10, then 10 − 3 = 7"],
            ["Writing the total as the missing number: 4 + ? = 9 → 9", "Ask: 4 add what makes 9? 4 + 5 = 9, so 5"],
            ["Thinking = means “the answer comes next”", "= means “is the same as”. 9 = 4 + 5 is true"],
        ])
    )


FAQ = [
    {"q": "What addition and subtraction does a Year 1 child learn?",
     "a": "In Year 1, children add and subtract one-digit and two-digit numbers to 20, including zero. They read and write number sentences with +, − and =, and solve simple problems and missing number questions such as 7 = ? − 9."},
    {"q": "How do you explain the equals sign to a Year 1 child?",
     "a": "Say that = means “is the same as”, not “the answer comes next”. Show that 4 + 3 = 7 and 7 = 4 + 3 are both true because each side has the same value."},
    {"q": "What is a number track in Year 1 maths?",
     "a": "A number track is a row of numbered squares. Children put a finger on the first number and jump on or back, counting the jumps but not the starting square."},
    {"q": "How can I help my child with missing number problems?",
     "a": "Use the two numbers you know. For ? + 4 = 9, take 4 from 9 to get 5. For 7 = ? − 9, add 7 and 9 to get 16, then check that 16 − 9 = 7."},
]


# ============================================================ checks
def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            # no two choices with the same value
            vals = [c.split(" ")[0] for c in it["c"]]
            if all(re.match(r"^\d+p?( [a-z ]+)?$", c) for c in it["c"]):
                assert len(set(vals)) == 4, it["c"]
            plain = re.sub(r"<[^>]+>", " ", it["q"])
            assert plain not in seen, plain
            seen.add(plain)
            assert it["q"].count("<svg") <= 1
            for t in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in t and '"' not in t and ".." not in t, t
                assert not re.search(r"\b1 (apples|ducks|balls|stickers|sweets|pages|books|biscuits|toy cars|conkers|"
                                     r"marbles|pencils|children|people|balloons|fish es)\b", t), t
            # answer key for plain sums: "... a ± b = ?"
            m = re.search(r"(\d+) ([+−]) (\d+) = \?\s*$", plain.strip())
            if m:
                x, op, y = int(m.group(1)), m.group(2), int(m.group(3))
                assert it["c"][it["a"]].split()[0] == str(x + y if op == "+" else x - y), (plain, it["c"])
            # missing-number questions
            m = re.search(r"(\d+|\?) ([+−]) (\d+|\?) = (\d+|\?)\s*$|(\d+) = (\d+|\?) ([+−]) (\d+|\?)\s*$", plain.strip())
            if m and "?" in m.group(0) and m.group(0).count("?") == 1:
                assert it["c"][it["a"]].split()[0] == str(solve(m.group(0).strip())), (plain, it["c"])
            # the answer is never 0 except in the zero questions
            if it["q"] not in ZERO_QS:
                assert not re.match(r"^0\b", it["c"][it["a"]]), it
            # pictures match their labels
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+ and (\d+) [a-z ]+'", it["q"]):
                assert it["q"].count("data-o='1'") == int(m.group(1)) + int(m.group(2))
            for m in re.finditer(r"aria-label='picture: (\d+) [a-z ]+, (\d+) crossed out'", it["q"]):
                assert it["q"].count("data-o='1'") == int(m.group(1))
                assert it["q"].count("data-x='1'") == int(m.group(2))
    assert len(ZERO_QS) <= 3, ZERO_QS


def gen():
    ZERO_QS.clear()
    rnd = random.Random(1103)
    P = People(rnd)
    sets = [set_add(), set_sub(), set_sentences(), set_missing(), set_words(P)]
    balance(sets, rnd)
    check(sets)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "addition-and-subtraction-within-20", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction within 20",
        "seo_title": "Year 1 Addition and Subtraction within 20 Worksheets: Number Sentences and Missing Numbers",
        "short_title": "Addition and subtraction within 20",
        "domain": "Addition and subtraction",
        "standard_code": "Year 1: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read, write and interpret mathematical statements involving addition (+), subtraction (−) and equals (=) signs; add and subtract one-digit and two-digit numbers to 20, including zero; solve one-step problems that involve addition and subtraction, using concrete objects and pictorial representations, and missing number problems such as 7 = ? − 9.",
        "meta_desc": "Free Year 1 maths worksheets on addition and subtraction within 20: add with pictures and a number track, take away and count back, read number sentences with +, − and =, find missing numbers and solve simple word problems. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Add: count on. Take away: count back. = means “is the same as”.",
        "key_sub": "9 + 3: say 9, then count 10, 11, 12. 12 − 5: go back to 10, then 3 more to 7. For 7 = ? − 9, put the 9 back: 7 + 9 = 16.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "picture|number track|number line|ten frames")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
