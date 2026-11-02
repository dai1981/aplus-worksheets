# -*- coding: utf-8 -*-
"""
CA Grade 1 Math: Position and directions (Ontario Mathematics Curriculum 2020, E1.4 and E1.5)
  python3 tools/gen_caon_math_g1_position.py
Position words (above, below, on, under, beside, between, in front of, behind), left and right
(from your view, as you look at the picture), following moves on a simple grid (2 squares right,
then 1 square up), finding the way on a classroom map, and word problems at school and in the
neighbourhood.
Every picture is drawn from the data that the answer is worked out from, so picture and answer agree.
Wrong answers come from real mistakes: left and right mixed up, up and down mixed up, counting the
start square (stopping 1 square short, or reading a distance 1 too big), going 1 square too far,
"on" chosen for "above", and the two numbers of a move swapped.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
FONT = "Arial, Helvetica, sans-serif"
INK = "#2b2b2b"
GREEN = "#006633"
FILL = "#cfe6d6"
GRAY = "#c9c2b8"
SOFT = "#8a8378"
WOOD = "#b98a5a"
BOX = "#d9a86c"
FLOOR = "#ebe6de"
COL = {"red": "#d6453b", "blue": "#3b7dd8", "green": "#4fae74", "yellow": "#f2c230",
       "orange": "#f08a24", "purple": "#8e6ccf"}
GIRLS = {"Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"}


def he(n):
    return "she" if n in GIRLS else "he"


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """Free order: positions are set later by balance()."""
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (re.sub("<svg.*?</svg>", "[svg]", q), correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A-D pictures, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c > 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label, label
    w, h = int(math.ceil(w)), int(math.ceil(h))
    if w == h:
        w += 1                     # keep figures out of the larger 'square' print size
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


class Pos:
    """Answer positions for picture questions (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ toys and objects
# icon(kind, x, base): drawn with its bottom centre at (x, base). SIZE = (half width left, half width right, height).
SIZE = {"ball": (15, 15, 30), "apple": (14, 14, 33), "cat": (12, 21, 40), "teddy": (12, 12, 40),
        "duck": (15, 22, 30), "car": (20, 20, 27), "balloon": (12, 12, 54), "star": (15, 15, 29),
        "book": (12, 12, 30), "beaver": (23, 20, 40), "mitt": (16, 10, 35), "puck": (15, 15, 18)}


def icon(kind, x, base, colour=None, flip=False):
    b = base
    if kind == "ball":
        s = ("<circle cx='%.1f' cy='%.1f' r='14' fill='%s' stroke='%s' stroke-width='2'/>"
             "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='#fff' stroke-width='2.5'/>"
             "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='#fff' stroke-width='2.5'/>"
             % (x, b - 15, colour or COL["blue"], INK, x - 13, b - 19, x, b - 9, x + 13, b - 19,
                x - 4, b - 28, x + 4, b - 15, x - 4, b - 2))
    elif kind == "apple":
        s = ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4a2b' stroke-width='3' stroke-linecap='round'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='6' ry='3' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
             "<circle cx='%.1f' cy='%.1f' r='13' fill='%s' stroke='%s' stroke-width='2'/>"
             % (x, b - 24, x + 2, b - 32, x + 8, b - 29, COL["green"], x + 8, b - 29,
                x, b - 14, colour or COL["red"], INK))
    elif kind == "cat":
        g = colour or "#8a8f99"
        s = ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='11' ry='11' fill='%s' stroke='%s' stroke-width='2'/>"
             "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             "<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.7' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.7' fill='%s'/>"
             % (x + 9, b - 6, x + 22, b - 8, x + 18, b - 22, g,
                x, b - 12, g, INK,
                x - 8, b - 29, x - 7, b - 39, x - 1, b - 34, g, INK,
                x + 8, b - 29, x + 7, b - 39, x + 1, b - 34, g, INK,
                x, b - 28, g, INK, x - 3, b - 29, INK, x + 3, b - 29, INK))
    elif kind == "teddy":
        c = colour or "#b07a45"
        s = ("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s' stroke='%s' stroke-width='1.5'/>"
             "<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s' stroke='%s' stroke-width='1.5'/>"
             "<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='3.5' fill='#ecd2b0'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>"
             % (x - 7, b - 34, c, INK, x + 7, b - 34, c, INK, x, b - 12, c, INK, x, b - 29, c, INK,
                x, b - 25, x - 3.5, b - 31, INK, x + 3.5, b - 31, INK))
    elif kind == "duck":
        c = colour or COL["yellow"]
        s = ("<ellipse cx='%.1f' cy='%.1f' rx='14' ry='9' fill='%s' stroke='%s' stroke-width='2'/>"
             "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             "<circle cx='%.1f' cy='%.1f' r='7.5' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>"
             % (x, b - 10, c, INK, x + 13, b - 25, x + 21, b - 22, x + 13, b - 19, COL["orange"], INK,
                x + 8, b - 22, c, INK, x + 10, b - 24, INK))
    elif kind == "car":
        c = colour or COL["red"]
        s = ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
             "<rect x='%.1f' y='%.1f' width='38' height='11' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             "<rect x='%.1f' y='%.1f' width='4' height='4' fill='#fff3b0' stroke='%s' stroke-width='1'/>"
             "<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/><circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>"
             % (x - 13, b - 16, x - 10, b - 26, x + 3, b - 26, x + 12, b - 16, "#dfeef8", INK,
                x - 19, b - 17, c, INK, x + 14, b - 15, INK,
                x - 11, b - 5, INK, x + 11, b - 5, INK))
        if flip:
            s = "<g transform='translate(%.1f 0) scale(-1 1) translate(%.1f 0)'>%s</g>" % (x, -x, s)
    elif kind == "balloon":
        c = colour or COL["red"]
        s = ("<path d='M%.1f %.1f q-4 6 0 12 q4 6 0 12 q-3 4 0 6' fill='none' stroke='%s' stroke-width='1.5'/>"
             "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='11' ry='14' fill='%s' stroke='%s' stroke-width='2'/>"
             % (x, b - 30, INK, x, b - 27, x - 3, b - 23, x + 3, b - 23, c,
                x, b - 40, c, INK))
    elif kind == "star":
        pts = []
        for i in range(10):
            r = 15 if i % 2 == 0 else 6.5
            t = math.radians(-90 + 36 * i)
            pts.append("%.1f,%.1f" % (x + r * math.cos(t), b - 15 + r * math.sin(t)))
        s = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
             % (" ".join(pts), colour or COL["yellow"], INK))
    elif kind == "book":
        s = ("<rect x='%.1f' y='%.1f' width='22' height='29' rx='2' fill='%s' stroke='%s' stroke-width='2'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
             % (x - 11, b - 30, colour or COL["purple"], INK, x - 6, b - 30, x - 6, b - 1, INK))
    elif kind == "beaver":
        c = colour or "#a0703f"
        s = ("<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4.5' fill='#5a3d22' stroke='%s' stroke-width='1.5'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='13' ry='12' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='3.2' fill='%s' stroke='%s' stroke-width='1.5'/>"
             "<circle cx='%.1f' cy='%.1f' r='3.2' fill='%s' stroke='%s' stroke-width='1.5'/>"
             "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='2'/>"
             "<rect x='%.1f' y='%.1f' width='4' height='4.5' fill='#fff' stroke='%s' stroke-width='1'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.7' fill='%s'/><circle cx='%.1f' cy='%.1f' r='2.2' fill='%s'/>"
             % (x - 13, b - 5, INK,
                x + 1, b - 13, c, INK,
                x + 4, b - 36, c, INK, x + 14, b - 36, c, INK,
                x + 10, b - 29, c, INK,
                x + 14, b - 23.5, INK,
                x + 12, b - 32, INK, x + 17.5, b - 28, INK))
    elif kind == "mitt":
        c = colour or COL["red"]
        s = ("<ellipse cx='%.1f' cy='%.1f' rx='5' ry='8' fill='%s' stroke='%s' stroke-width='2' transform='rotate(-25 %.1f %.1f)'/>"
             "<rect x='%.1f' y='%.1f' width='20' height='27' rx='9' fill='%s' stroke='%s' stroke-width='2'/>"
             "<rect x='%.1f' y='%.1f' width='22' height='9' rx='2' fill='#f4f1ea' stroke='%s' stroke-width='2'/>"
             % (x - 10, b - 21, c, INK, x - 10, b - 21,
                x - 10, b - 34, c, INK,
                x - 11, b - 10, INK))
    elif kind == "puck":
        s = ("<rect x='%.1f' y='%.1f' width='28' height='8' fill='#222'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='14' ry='5' fill='#222'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='14' ry='5' fill='#555' stroke='#111' stroke-width='1.5'/>"
             % (x - 14, b - 13, x, b - 5, x, b - 13))
    else:
        raise ValueError(kind)
    return s


def scaled(kind, x, base, k, colour=None, flip=False):
    return "<g transform='translate(%.1f %.1f) scale(%.2f)'>%s</g>" % (x, base, k, icon(kind, 0, 0, colour, flip))


# ------------------------------------------------------------ position scenes (body, W, H)
def floor(W, y):
    return "<line x1='2' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (y, W - 2, y, SOFT)


TBL = {"W": 214, "H": 146, "F": 140, "top": 86, "x0": 52, "x1": 162}


def table_scene(kind, where, colour=None):
    """A table, and one object on / under / above / beside it."""
    W, H, F, T, x0, x1 = TBL["W"], TBL["H"], TBL["F"], TBL["top"], TBL["x0"], TBL["x1"]
    mid = (x0 + x1) / 2
    s = [floor(W, F)]
    s.append("<rect x='%d' y='%d' width='7' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x0 + 5, T + 6, F - T - 6, WOOD, INK))
    s.append("<rect x='%d' y='%d' width='7' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x1 - 12, T + 6, F - T - 6, WOOD, INK))
    s.append("<rect x='%d' y='%d' width='%d' height='7' rx='2' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x0, T, x1 - x0, WOOD, INK))
    hl, hr, hh = SIZE[kind]
    if where == "on":
        s.append(icon(kind, mid, T, colour))
    elif where == "under":
        assert F - hh > T + 7 + 4, kind
        s.append(icon(kind, mid, F - 1.5, colour))
    elif where == "above":
        assert kind == "balloon"
        s.append(icon(kind, mid, T - 24, colour))
        assert T - 24 - hh >= 4
    elif where == "beside":
        x = x1 + 8 + hl
        assert x + hr <= W - 2, kind
        s.append(icon(kind, x, F - 1.5, colour))
    else:
        raise ValueError(where)
    return "".join(s), W, H


BXS = {"W": 196, "H": 112, "bx0": 62, "bx1": 136, "btop": 60, "bbot": 92}


def box_scene(kind, where, colour=None):
    """A cardboard box on the floor. Behind: the object is further back (higher up) and partly hidden.
    In front: the object is nearer (lower down) and hides part of the box."""
    W, H = BXS["W"], BXS["H"]
    x0, x1, top, bot = BXS["bx0"], BXS["bx1"], BXS["btop"], BXS["bbot"]
    s = ["<rect x='0' y='%d' width='%d' height='%d' fill='%s'/>" % (top + 6, W, H - top - 6, FLOOR)]
    boxsvg = ("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
              "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
              % (x0, top, x1 - x0, bot - top, BOX, INK, (x0 + x1) // 2, top, (x0 + x1) // 2, top + 12, INK))
    mid = (x0 + x1) / 2
    hl, hr, hh = SIZE[kind]
    if where == "behind":
        base = top + 10
        assert base - hh < top - 12, "too little shows above the box"
        s.append(icon(kind, x1 - 10, base, colour))       # peeks out over the top and the side
        s.append(boxsvg)
    elif where == "in front of":
        s.append(boxsvg)
        s.append(icon(kind, mid - 6, H - 3, colour))
        assert H - 3 > bot + 8
    elif where == "on":
        s.append(boxsvg)
        s.append(icon(kind, mid, top, colour))
        assert top - hh >= 4
    elif where == "beside":
        s.append(boxsvg)
        x = x1 + 8 + hl
        assert x + hr <= W - 2
        s.append(icon(kind, x, bot, colour))
    else:
        raise ValueError(where)
    return "".join(s), W, H


def row_scene(kinds, step=56, labels=False, colours=None, fs=15):
    """Objects standing in a row on a line. labels=True writes 'left' and 'right' at the two ends."""
    n = len(kinds)
    W = 16 + n * step
    F = 46
    H = F + (26 if labels else 6)
    s = [floor(W, F)]
    for i, k in enumerate(kinds):
        hl, hr, hh = SIZE[k]
        assert hh <= F - 2
        s.append(icon(k, 8 + step / 2 + i * step - (hr - hl) / 2, F - 1.5, (colours or {}).get(i)))
    if labels:
        s.append(text(8, F + 20, "left", fs, "start", SOFT))
        s.append(text(W - 8, F + 20, "right", fs, "end", SOFT))
    return "".join(s), W, H


def shelf_scene(grid):
    """A bookcase: grid[r][c] = object kind; row 0 is the top shelf."""
    rows, cols = len(grid), len(grid[0])
    cw, rh, pad = 58, 50, 6
    W = 2 * pad + cols * cw + 8
    H = 2 * pad + rows * rh + 8
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#f6eee2' stroke='%s' stroke-width='3'/>"
         % (pad, pad, cols * cw + 8, rows * rh + 8, WOOD)]
    for r in range(rows):
        y = pad + 4 + (r + 1) * rh
        s.append("<rect x='%d' y='%d' width='%d' height='4' fill='%s'/>" % (pad, y, cols * cw + 8, WOOD))
        for c in range(cols):
            k = grid[r][c]
            assert SIZE[k][2] <= rh - 6
            x = pad + 4 + cw / 2 + c * cw - (SIZE[k][1] - SIZE[k][0]) / 2
            s.append(icon(k, x, y, None))
    return "".join(s), W, H


def scene_svg(scene, label, y0=0):
    """y0 crops empty sky off the top of a scene."""
    body, W, H = scene
    if y0:
        body = "<g transform='translate(0 %d)'>%s</g>" % (-y0, body)
    return svg_wrap(W, H - y0, body, label)


def table_svg(kind, where, label):
    y0 = 0 if where == "above" else max(0, TBL["top"] - (SIZE[kind][2] if where == "on" else 0) - 8)
    return scene_svg(table_scene(kind, where), label, y0)


def grid4_svg(scenes, label, k=None):
    """2 x 2 panels labelled A-D."""
    if k is None:
        k = min(1.0, 140.0 / max(sc[1] for sc in scenes))
    cw = max(sc[1] for sc in scenes) * k
    ch = max(sc[2] for sc in scenes) * k
    LW, gap = 22, 10
    W = 2 * (LW + cw) + gap + 8
    H = 2 * ch + gap + 8
    s = ["<line x1='%.1f' y1='4' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (W / 2, W / 2, H - 4, GRAY),
         "<line x1='4' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (H / 2, W - 4, H / 2, GRAY)]
    for i, (body, w, h) in enumerate(scenes):
        r, c = divmod(i, 2)
        x0 = 4 + c * (LW + cw + gap)
        y0 = 4 + r * (ch + gap)
        s.append(text(x0 + 2, y0 + 18, "ABCD"[i], 18, "start"))
        s.append("<g transform='translate(%.1f %.1f) scale(%.2f)'>%s</g>"
                 % (x0 + LW + (cw - w * k) / 2, y0 + (ch - h * k) / 2, k, body))
    return svg_wrap(W, H, "".join(s), label)


def pick4(q, scenes, why, pos, label):
    """scenes[0] is the right picture; it goes to position p."""
    p = pos.next()
    cells = scenes[1:]
    cells.insert(p, scenes[0])
    return mcq_fixed(fig(grid4_svg(cells, label)) + q, ["A", "B", "C", "D"], "ABCD"[p],
                     "Picture <b>%s</b>. %s" % ("ABCD"[p], why))


def child(x, base, colour):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            "<rect x='%.1f' y='%.1f' width='18' height='19' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
            "<circle cx='%.1f' cy='%.1f' r='8' fill='#f1c9a0' stroke='%s' stroke-width='2'/>"
            % (x - 4, base - 14, x - 5, base - 1, INK, x + 4, base - 14, x + 5, base - 1, INK,
               x - 9, base - 32, colour, INK, x, base - 41, INK))


SHIRT = ["#d6453b", "#3b7dd8", "#4fae74", "#f2c230", "#8e6ccf", "#f08a24"]


def queue_svg(names, door_left=True):
    """Children in a line to the gym door. names[0] is nearest the door (first)."""
    n = len(names)
    step = 54
    W = 52 + n * step + 6
    H = 80
    s = [floor(W, 60)]
    dx = 6 if door_left else W - 6 - 30
    s.append("<rect x='%d' y='6' width='30' height='54' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%d' cy='34' r='2.5' fill='%s'/>" % (dx, WOOD, INK, dx + (24 if door_left else 6), INK))
    for i, nm in enumerate(names):
        x = (52 + step / 2 + i * step) if door_left else (W - 52 - step / 2 - i * step)
        assert len(nm) * 15 * 0.6 < step - 4
        s.append(child(x, 58, SHIRT[i % len(SHIRT)]))
        s.append(text(x, 77, nm, 15))
    return svg_wrap(W, H, "".join(s), "%d children in a line to a door on the %s" % (n, "left" if door_left else "right"))


def kids_row_svg(names):
    n = len(names)
    step = 56
    W = n * step + 12
    H = 100
    s = [floor(W, 60)]
    for i, nm in enumerate(names):
        x = 6 + step / 2 + i * step
        assert len(nm) * 15 * 0.6 < step - 4
        s.append(child(x, 58, SHIRT[i % len(SHIRT)]))
        s.append(text(x, 78, nm, 15))
    s.append(text(6, 97, "left", 15, "start", SOFT))
    s.append(text(W - 6, 97, "right", 15, "end", SOFT))
    return svg_wrap(W, H, "".join(s), "children sitting in a row: " + ", ".join(names))


def cubbies_svg(rows):
    """Coat cubbies with a name on each. rows[0] is the top row."""
    cw, ch = 62, 50
    nr, nc = len(rows), len(rows[0])
    W, H = nc * cw + 8, nr * ch + 8
    s = ["<rect x='4' y='4' width='%d' height='%d' fill='#f6eee2' stroke='%s' stroke-width='3'/>" % (nc * cw, nr * ch, WOOD)]
    for r in range(nr):
        for c in range(nc):
            x, y = 4 + c * cw, 4 + r * ch
            nm = rows[r][c]
            assert len(nm) * 15 * 0.6 < cw - 8
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (x, y, cw, ch, WOOD))
            s.append("<circle cx='%.1f' cy='%d' r='3' fill='%s'/>" % (x + cw / 2, y + 12, SOFT))
            s.append(text(x + cw / 2, y + 38, nm, 15))
    return svg_wrap(W, H, "".join(s), "cubbies in %d rows with a name on each: %s" % (nr, " / ".join(", ".join(r) for r in rows)))


def strip(scenes, caps, label, k=0.8, fs=15):
    cw = max(sc[1] for sc in scenes) * k + 12
    ch = max(sc[2] for sc in scenes) * k
    s = []
    for i, ((body, w, h), cap) in enumerate(zip(scenes, caps)):
        x0 = i * cw
        s.append("<g transform='translate(%.1f %.1f) scale(%.2f)'>%s</g>" % (x0 + (cw - w * k) / 2, ch - h * k, k, body))
        s.append(text(x0 + cw / 2, ch + 20, cap, fs))
    return svg_wrap(cw * len(scenes), ch + 27, "".join(s), label)


def balance(sets, rnd):
    """Correct answers exactly 5/5/5/5. Fixed-order questions keep their order; the others fill the gaps."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [5 - c for c in cnt]
        assert min(need) >= 0 and sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


DIRS = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}
OPP = {"right": "left", "left": "right", "up": "down", "down": "up"}


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


def mv(p, d, n):
    return (p[0] + DIRS[d][0] * n, p[1] + DIRS[d][1] * n)


def walk(p, moves):
    for d, n in moves:
        p = mv(p, d, n)
    return p


def count_txt(n):
    return ", ".join(str(i) for i in range(1, n + 1))


# ============================================================ set 1: position words
def set_position(rnd, pos):
    its = []
    other = {"on": ["above", "under", "beside"], "under": ["on", "beside", "above"],
             "above": ["on", "under", "beside"], "beside": ["on", "under", "above"]}
    why_t = {
        "on": "The %s is <b>on</b> the table. It touches the table top.",
        "under": "The %s is <b>under</b> the table. It is below the table top.",
        "above": "The %s is <b>above</b> the table. It is higher than the table, with a gap.",
        "beside": "The %s is <b>beside</b> the table. It is at the side, close by.",
    }
    for kind, where in [("beaver", "on"), ("ball", "under"), ("balloon", "above"), ("duck", "beside"),
                        ("teddy", "on"), ("cat", "under")]:
        e = why_t[where] % kind
        if where == "on":
            e += " Above would have a gap."
        if where == "above":
            e += " It does not touch the table, so it is not on it."
        its.append(mcq(fig(table_svg(kind, where, "a %s %s a table" % (kind, where))) + "Where is the %s?" % kind,
                       where + " the table", [w + " the table" for w in other[where]], e))
    bx = {"in front of": ["behind", "on", "beside"], "behind": ["in front of", "on", "beside"]}
    for kind, where in [("beaver", "behind"), ("ball", "in front of"), ("teddy", "in front of"), ("duck", "behind")]:
        sc = box_scene(kind, where)
        if where == "behind":
            e = "The box hides part of the %s. The %s is further back. It is <b>behind</b> the box." % (kind, kind)
        else:
            e = ("We can see all of the %s. It is closer to us than the box. "
                 "It is <b>in front of</b> the box." % kind)
        y0 = max(0, BXS["btop"] - (SIZE[kind][2] - 10 if where == "behind" else 0) - 8)
        its.append(mcq(fig(scene_svg(sc, "a %s %s a box" % (kind, where), y0)) + "Where is the %s?" % kind,
                       where + " the box", [w + " the box" for w in bx[where]], e))
    # between
    row = ["teddy", "beaver", "ball"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a teddy, a beaver and a ball in a row")) +
                   "What is <b>between</b> the teddy and the ball?", "the beaver", ["the teddy", "the ball", "the cat"],
                   "Between means in the middle. The <b>beaver</b> is in the middle."))
    row = ["star", "duck", "mitt", "car"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a star, a duck, a mitt and a car in a row")) +
                   "What is between the duck and the car?", "the mitt", ["the star", "the duck", "the car"],
                   "Find the duck and the car. The <b>mitt</b> is in the middle of them."))
    row = ["cat", "book", "duck"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a cat, a book and a duck in a row")) +
                   "Where is the book?", "between the cat and the duck",
                   ["on the duck", "under the cat", "above the duck"],
                   "The cat is on one side. The duck is on the other side. The book is <b>between</b> them."))
    # shelves: above and below
    sh1 = [["star", "ball"], ["beaver", "apple"], ["cat", "duck"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh1), "a bookcase with 3 shelves of toys")) +
                   "What is just <b>above</b> the beaver?", "the star", ["the cat", "the apple", "the ball"],
                   "Look up from the beaver. The <b>star</b> is on the shelf above. The cat is below."))
    sh2 = [["teddy", "car"], ["apple", "star"], ["ball", "mitt"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh2), "a bookcase with 3 shelves of toys")) +
                   "What is just <b>below</b> the star?", "the mitt", ["the car", "the apple", "the ball"],
                   "Look down from the star. The <b>mitt</b> is on the shelf below. The car is above."))
    sh3 = [["duck", "apple"], ["car", "teddy"], ["cat", "star"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh3), "a bookcase with 3 shelves of toys")) +
                   "Where is the apple?", "above the teddy", ["below the teddy", "beside the car", "below the star"],
                   "The apple is on the top shelf. The teddy is on the shelf under it. The apple is <b>above</b> the teddy."))
    sh4 = [["ball", "book"], ["duck", "beaver"], ["star", "cat"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh4), "a bookcase with 3 shelves of toys")) +
                   "Where is the star?", "below the duck", ["above the duck", "beside the beaver", "above the cat"],
                   "The star is on the bottom shelf. The duck is on the shelf over it. The star is <b>below</b> the duck."))
    # A-D pictures
    its.append(pick4("Which picture shows the duck <b>under</b> the table?",
                     [table_scene("duck", "under"), table_scene("duck", "on"), table_scene("duck", "beside"),
                      table_scene("ball", "under", COL["red"])],
                     "The duck is below the table top. In one picture a ball is under the table, not the duck.",
                     pos, "four pictures labelled A to D of a table"))
    its.append(pick4("Which picture shows the beaver <b>behind</b> the box?",
                     [box_scene("beaver", "behind"), box_scene("beaver", "in front of"), box_scene("beaver", "on"),
                      box_scene("beaver", "beside")],
                     "The box hides part of the beaver. So the beaver is behind the box.",
                     pos, "four pictures labelled A to D of a box"))
    its.append(pick4("Which picture shows the balloon <b>above</b> the table?",
                     [table_scene("balloon", "above"), table_scene("teddy", "on"), table_scene("cat", "under"),
                      table_scene("teddy", "beside")],
                     "The balloon is higher than the table. There is a gap.",
                     pos, "four pictures labelled A to D of a table"))
    assert len(its) == 20, len(its)
    return {"title": "Above, below, beside, between, in front of, behind", "items": its}


# ============================================================ set 2: left and right
NTH = ["1st", "2nd", "3rd", "4th", "5th", "6th"]


def set_left_right(rnd, pos):
    its = []

    def row_q(kinds, q, ans_i, wrong_i, e, labels):
        lab = "a row of toys: " + ", ".join(kinds)
        assert len(set(kinds)) == len(kinds)
        return mcq(fig(scene_svg(row_scene(kinds, labels=labels), lab)) + q,
                   "the " + kinds[ans_i], ["the " + kinds[j] for j in wrong_i], e)

    k = ["beaver", "ball", "car", "duck", "star"]
    its.append(row_q(k, "Which toy is at the <b>left</b> end?", 0, [4, 1, 3],
                     "Left is the side of your left hand. The <b>beaver</b> is at the left end.", True))
    k = ["apple", "teddy", "book", "cat"]
    its.append(row_q(k, "Which toy is at the <b>right</b> end?", 3, [0, 2, 1],
                     "Right is the side of your right hand. The <b>cat</b> is at the right end.", True))
    k = ["duck", "star", "mitt", "apple", "ball"]
    its.append(row_q(k, "Which toy is at the <b>right</b> end?", 4, [0, 3, 1],
                     "Right is the side of your right hand. The <b>ball</b> is at the right end. The duck is at the left end.", False))
    k = ["car", "cat", "teddy", "puck"]
    its.append(row_q(k, "Which toy is at the <b>left</b> end?", 0, [3, 1, 2],
                     "Left is the side of your left hand. The <b>car</b> is at the left end.", False))
    plans = [(["teddy", "duck", "ball", "beaver", "car"], "left", 2, True),
             (["star", "apple", "cat", "duck", "book"], "right", 2, True),
             (["ball", "mitt", "star", "teddy", "apple", "cat"], "left", 3, False),
             (["book", "car", "duck", "apple", "beaver", "star"], "right", 3, False),
             (["cat", "teddy", "apple", "ball", "duck"], "left", 4, False),
             (["apple", "star", "car", "mitt", "teddy", "ball"], "right", 2, False)]
    for kinds, side, n, lab in plans:
        L = len(kinds)
        i = n - 1 if side == "left" else L - n
        j_other = L - n if side == "left" else n - 1
        j_skip = i + (1 if side == "left" else -1)
        j_short = i - (1 if side == "left" else -1)
        wr = [j for j in [j_other, j_skip, j_short] + list(range(L)) if 0 <= j < L and j != i]
        e = ("Start at the %s end. Count %s: %s. The %s toy is the <b>%s</b>."
             % (side, count_txt(n),
                ", ".join("the " + kinds[(t if side == "left" else L - 1 - t)] for t in range(n)), NTH[n - 1], kinds[i]))
        if j_other != i:
            e += " The %s is %s from the %s." % (kinds[j_other], NTH[n - 1], OPP[side])
        its.append(row_q(kinds, "Which toy is <b>%s from the %s</b>?" % (NTH[n - 1], side), i, wr, e, lab))
    plans = [(["duck", "cat", "beaver", "book", "ball"], 2, "right"), (["star", "car", "apple", "teddy", "duck"], 2, "left"),
             (["ball", "apple", "teddy", "mitt", "cat"], 3, "left"), (["beaver", "book", "duck", "star", "car"], 2, "right")]
    for kinds, ref, side in plans:
        i = ref + (1 if side == "right" else -1)
        o = ref - (1 if side == "right" else -1)
        two = ref + (2 if side == "right" else -2)
        cands = [o] + ([two] if 0 <= two < len(kinds) else []) + [t for t in range(len(kinds)) if t not in (i, o, two, ref)]
        e = ("Find the %s. Look to the %s side of it. The toy just to the %s is the <b>%s</b>. The %s is on the other side."
             % (kinds[ref], side, side, kinds[i], kinds[o]))
        its.append(row_q(kinds, "What is just to the <b>%s</b> of the %s?" % (side, kinds[ref]), i, cands[:3], e, False))
    for kinds, a, b in [(["beaver", "ball"], 0, 1), (["star", "duck", "car"], 2, 0), (["apple", "cat", "teddy"], 1, 2)]:
        side = "to the left" if a < b else "to the right"
        e = ("The %s is on the %s side of the %s. So it is <b>%s</b> of the %s."
             % (kinds[a], "left" if a < b else "right", kinds[b], side, kinds[b]))
        its.append(mcq(fig(scene_svg(row_scene(kinds), "a row of toys: " + ", ".join(kinds))) +
                       "Where is the %s?" % kinds[a], side + " of the " + kinds[b],
                       [("to the right" if a < b else "to the left") + " of the " + kinds[b],
                        "above the " + kinds[b], "behind the " + kinds[b]], e))

    def lr(a, b):
        return row_scene([a, b], step=62)
    its.append(pick4("Which picture shows the beaver to the <b>left</b> of the ball?",
                     [lr("beaver", "ball"), lr("ball", "beaver"), lr("teddy", "ball"), lr("ball", "teddy")],
                     "The beaver is on the left side. The ball is on the right side.",
                     pos, "four pictures labelled A to D of two toys"))
    its.append(pick4("Which picture shows the duck to the <b>right</b> of the star?",
                     [lr("star", "duck"), lr("duck", "star"), lr("star", "cat"), lr("cat", "duck")],
                     "The star is on the left side. The duck is on the right side.",
                     pos, "four pictures labelled A to D of two toys"))
    k = ["car", "mitt", "apple", "duck"]
    its.append(mcq(fig(scene_svg(row_scene(k, labels=True), "a row of toys: " + ", ".join(k))) +
                   "The car is 1st from the left. What is it from the right?", "4th", ["1st", "3rd", "5th"],
                   "Start at the right end: duck 1st, apple 2nd, mitt 3rd, car <b>4th</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Left and right (from your view)", "items": its}


# ============================================================ set 3: follow moves on a grid
GC, GR, CS = 7, 4, 36
GPOOL = ["apple", "ball", "cat", "teddy", "duck", "star", "mitt", "puck"]


def ginside(c):
    return 0 <= c[0] < GC and 0 <= c[1] < GR


def grid_svg(start, items, path=None, label="grid with a beaver and toys"):
    """items: {(col, row): kind}. The beaver stands on the green start square.
    path: list of moves drawn as a dashed arrow (lesson only)."""
    W, H = GC * CS + 8, GR * CS + 8
    s = []
    for r in range(GR):
        for c in range(GC):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (4 + c * CS, 4 + r * CS, CS, CS, FILL if (c, r) == start else "#fff", GRAY))
    kk = 0.66
    for (c, r), k in sorted(items.items()):
        assert ginside((c, r)) and (c, r) != start and k in GPOOL
        hl, hr, hh = SIZE[k]
        s.append(scaled(k, 4 + c * CS + CS / 2 - (hr - hl) * kk / 2, 4 + r * CS + CS / 2 + hh * kk / 2, kk))
    hl, hr, hh = SIZE["beaver"]
    s.append(scaled("beaver", 4 + start[0] * CS + CS / 2 - (hr - hl) * kk / 2, 4 + start[1] * CS + CS / 2 + hh * kk / 2, kk))
    if path:
        pts = [start]
        for d, n in path:
            pts.append(mv(pts[-1], d, n))
        assert all(ginside(p) for p in pts)
        xy = [(4 + c * CS + CS / 2, 4 + r * CS + CS / 2) for c, r in pts]
        # stop the line short of the end so the arrow head sits at the edge of the last square
        d = DIRS[path[-1][0]]
        tip = (xy[-1][0] - d[0] * 12, xy[-1][1] - d[1] * 12)
        line = xy[:-1] + [(tip[0] - d[0] * 6, tip[1] - d[1] * 6)]
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='6 4'/>"
                 % (" ".join("%.1f,%.1f" % p for p in line), GREEN))
        nr = (-d[1], d[0])
        tri = [tip, (tip[0] - d[0] * 9 + nr[0] * 6, tip[1] - d[1] * 9 + nr[1] * 6),
               (tip[0] - d[0] * 9 - nr[0] * 6, tip[1] - d[1] * 9 - nr[1] * 6)]
        s.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in tri), GREEN))
    return svg_wrap(W, H, "".join(s), label)


def moves_txt(moves):
    return ", then ".join("<b>%s %s</b>" % (sq(n), d) for d, n in moves)


def moves_short(moves):
    return ", then ".join("%d %s" % (n, d) for d, n in moves)


def mistakes(moves):
    """(kind, wrong moves) from real mistakes, in a useful order."""
    out = []
    for i, (d, n) in enumerate(moves):
        m = list(moves)
        m[i] = (OPP[d], n)
        out.append(("flip", m))
    for i, (d, n) in enumerate(moves):
        if n > 1:
            m = list(moves)
            m[i] = (d, n - 1)
            out.append(("start", m))
    if len(moves) == 2 and moves[0][1] != moves[1][1]:
        out.append(("swap", [(moves[0][0], moves[1][1]), (moves[1][0], moves[0][1])]))
    for i, (d, n) in enumerate(moves):
        m = list(moves)
        m[i] = (d, n + 1)
        out.append(("far", m))
    if len(moves) == 1:                      # last resort: went a wrong way (up instead of right, ...)
        d, n = moves[0]
        for w in (("up", "down") if d in ("left", "right") else ("left", "right")):
            out.append(("flip", [(w, n)]))
    return out


def walk_e(moves):
    parts = []
    for d, n in moves:
        parts.append("Go %s: %s." % (d, count_txt(n)))
    return "Do not count the beaver’s own square. " + " ".join(parts)


def set_grid(rnd, pos):
    its = []

    def stop_q(start, moves):
        end = walk(start, moves)
        assert ginside(end) and end != start
        cells, kinds_why = [], []
        for kind, m in mistakes(moves):
            c = walk(start, m)
            if ginside(c) and c != end and c != start and c not in cells:
                cells.append(c)
                kinds_why.append(kind)
        assert len(cells) >= 3, (start, moves, cells)
        cells, kinds_why = cells[:3], kinds_why[:3]
        kinds = rnd.sample(GPOOL, 4)
        items = dict(zip([end] + cells, kinds))
        q = fig(grid_svg(start, items)) + "The beaver goes %s. Where does it stop?" % moves_txt(moves)
        e = walk_e(moves) + " It stops on the <b>%s</b>." % kinds[0]
        tip = {"flip": " Going the wrong way gets to the %s.", "start": " Counting the beaver’s square stops on the %s.",
               "swap": " Mixing up the two numbers gets to the %s.", "far": " One square too far is the %s."}
        e += tip[kinds_why[0]] % kinds[1]
        its.append(mcq(q, "the " + kinds[0], ["the " + k for k in kinds[1:]], e))

    for start, d, n in [((3, 0), "right", 3), ((6, 3), "left", 3), ((2, 3), "up", 2), ((4, 0), "down", 2),
                        ((3, 2), "left", 2), ((5, 2), "up", 1)]:
        stop_q(start, [(d, n)])
    for start, d, n in [((1, 1), "right", 4), ((6, 3), "left", 3), ((3, 3), "up", 3)]:
        k = rnd.choice(GPOOL)
        its.append(mcq_num(fig(grid_svg(start, {mv(start, d, n): k})) +
                           "How many squares <b>%s</b> to get to the %s?" % (d, k), n, [n + 1, n - 1, n + 2],
                           "Do not count the beaver’s own square. Count each move: %s. That is <b>%d</b>."
                           % (count_txt(n), n)))
    for start, moves in [((0, 3), [("right", 2), ("up", 1)]), ((1, 3), [("right", 3), ("up", 2)]),
                         ((6, 3), [("left", 2), ("up", 2)]), ((5, 0), [("left", 3), ("down", 2)]),
                         ((0, 0), [("down", 2), ("right", 3)]), ((3, 0), [("down", 3), ("left", 2)]),
                         ((2, 1), [("right", 1), ("down", 2)])]:
        stop_q(start, moves)

    def which_q(start, target):
        dx, dy = target[0] - start[0], target[1] - start[1]
        assert dx and dy
        mvs = [("right" if dx > 0 else "left", abs(dx)), ("up" if dy < 0 else "down", abs(dy))]
        assert walk(start, mvs) == target
        wrong = [[(OPP[mvs[0][0]], mvs[0][1]), mvs[1]], [mvs[0], (OPP[mvs[1][0]], mvs[1][1])],
                 [(mvs[0][0], mvs[0][1] + 1), (mvs[1][0], mvs[1][1] + 1)]]
        if mvs[0][1] != mvs[1][1]:
            wrong.insert(2, [(mvs[0][0], mvs[1][1]), (mvs[1][0], mvs[0][1])])
        for w in wrong:
            assert walk(start, w) != target
        k = rnd.choice(GPOOL)
        e = ("Do not count the beaver’s own square. Count the moves: %s %s, then %s %s."
             % (sq(mvs[0][1]), mvs[0][0], sq(mvs[1][1]), mvs[1][0]))
        its.append(mcq(fig(grid_svg(start, {target: k})) + "Which moves take the beaver to the %s?" % k,
                       moves_short(mvs), [moves_short(w) for w in wrong], e))

    which_q((0, 3), (2, 2))
    which_q((6, 3), (3, 1))
    which_q((1, 0), (4, 2))
    which_q((5, 1), (1, 0))
    assert len(its) == 20, len(its)
    return {"title": "Follow moves on a grid: 2 squares right, then 1 up", "items": its}


# ============================================================ set 4: classroom map
MC, MH, MCOLS, MROWS = 64, 58, 6, 3
ROOM = {(0, 0): "door", (3, 0): "easel", (5, 0): "shelf",
        (5, 1): "sink",
        (0, 2): "coats", (2, 2): "carpet", (4, 2): "plant", (5, 2): "desk"}
AT = {v: k for k, v in ROOM.items()}


def place_icon(kind, cx, cy):
    if kind == "door":
        return ("<rect x='%.1f' y='%.1f' width='22' height='30' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<circle cx='%.1f' cy='%.1f' r='2' fill='%s'/>" % (cx - 11, cy - 16, WOOD, INK, cx + 6, cy, INK))
    if kind == "easel":
        return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                "<rect x='%.1f' y='%.1f' width='28' height='20' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                "<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/><rect x='%.1f' y='%.1f' width='7' height='7' fill='%s'/>"
                % (cx - 5, cy - 6, cx - 14, cy + 14, WOOD, cx + 5, cy - 6, cx + 14, cy + 14, WOOD,
                   cx - 14, cy - 15, INK, cx - 5, cy - 5, COL["red"], cx + 2, cy - 9, COL["blue"]))
    if kind == "shelf":
        s = ("<rect x='%.1f' y='%.1f' width='34' height='30' fill='#f6eee2' stroke='%s' stroke-width='2'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
             % (cx - 17, cy - 15, WOOD, cx - 17, cy, cx + 17, cy, WOOD))
        cols = [COL["red"], COL["blue"], COL["green"], COL["yellow"], COL["purple"]]
        for i in range(5):
            s += "<rect x='%.1f' y='%.1f' width='5' height='12' fill='%s'/>" % (cx - 14 + i * 6, cy - 13, cols[i])
            s += "<rect x='%.1f' y='%.1f' width='5' height='12' fill='%s'/>" % (cx - 14 + i * 6, cy + 2, cols[(i + 2) % 5])
        return s
    if kind == "sink":
        return ("<path d='M%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#dfe7ee' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='4' height='12' fill='%s'/><rect x='%.1f' y='%.1f' width='11' height='4' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='2.5' fill='%s'/>"
                % (cx - 17, cy, cx + 17, cy, cx + 17, cy + 13, cx + 8, cy + 13, cx - 8, cy + 13, cx - 17, cy + 13, cx - 17, cy, INK,
                   cx - 2, cy - 14, SOFT, cx - 2, cy - 14, SOFT, cx + 7, cy - 6, COL["blue"]))
    if kind == "coats":
        s = "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx - 19, cy - 14, cx + 19, cy - 14, WOOD)
        for x, c in ((cx - 9, COL["red"]), (cx + 9, COL["blue"])):
            s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                  % (x - 4, cy - 12, x + 4, cy - 12, x + 8, cy + 14, x - 8, cy + 14, c, INK))
        return s
    if kind == "carpet":
        return ("<rect x='%.1f' y='%.1f' width='42' height='24' rx='4' fill='#e7b9c9' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='32' height='14' rx='3' fill='none' stroke='#fff' stroke-width='2'/>"
                % (cx - 21, cy - 10, INK, cx - 16, cy - 5))
    if kind == "plant":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='5' ry='10' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='5' ry='10' fill='%s' transform='rotate(30 %.1f %.1f)'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='5' ry='11' fill='%s'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx - 7, cy - 6, COL["green"], cx - 7, cy - 6, cx + 7, cy - 6, COL["green"], cx + 7, cy - 6,
                   cx, cy - 9, GREEN, cx - 10, cy + 2, cx + 10, cy + 2, cx + 7, cy + 15, cx - 7, cy + 15, "#c26a3d", INK))
    if kind == "desk":
        return ("<rect x='%.1f' y='%.1f' width='38' height='6' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%.1f' y='%.1f' width='4' height='14' fill='%s'/><rect x='%.1f' y='%.1f' width='4' height='14' fill='%s'/>"
                "<rect x='%.1f' y='%.1f' width='12' height='8' fill='%s' stroke='%s' stroke-width='1'/>"
                % (cx - 19, cy - 2, WOOD, INK, cx - 17, cy + 4, WOOD, cx + 13, cy + 4, WOOD, cx - 6, cy - 10, COL["purple"], INK))
    raise ValueError(kind)


def map_svg(start=None, name=None):
    W, H = MCOLS * MC + 8, MROWS * MH + 8
    s = []
    for r in range(MROWS):
        for c in range(MCOLS):
            fillc = FILL if (c, r) == start else "#fff"
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (4 + c * MC, 4 + r * MH, MC, MH, fillc, GRAY))
    for (c, r), k in sorted(ROOM.items()):
        assert (c, r) != start
        cx, top = 4 + c * MC + MC / 2, 4 + r * MH
        s.append(place_icon(k, cx, top + 22))
        s.append(text(cx, top + 53, k, 14))
    lab = "a classroom map with a door, easel, shelf, sink, coats, carpet, plant and desk"
    if start:
        assert len(name) * 14 * 0.6 < MC - 4
        cx, top = 4 + start[0] * MC + MC / 2, 4 + start[1] * MH
        s.append("<g transform='translate(%.1f %.1f) scale(0.8)'>%s</g>" % (cx, top + 41, child(0, 0, SHIRT[1])))
        s.append(text(cx, top + 53, name, 14, col=GREEN))
        lab += "; %s is on a square" % name
    return svg_wrap(W, H, "".join(s), lab)


def route(start, steps):
    """Checks the walk stays on the map and passes only empty squares before the end."""
    p, path = start, []
    for d, n in steps:
        for i in range(1, n + 1):
            path.append(mv(p, d, i))
        p = path[-1]
    for c in path:
        assert 0 <= c[0] < MCOLS and 0 <= c[1] < MROWS, (start, steps)
    for c in path[:-1]:
        assert c not in ROOM, ("passes through", ROOM[c], start, steps)
    return p


def say(steps):
    return ", then ".join("%s %s" % (sq(n), d) for d, n in steps)


def set_map(rnd, pos):
    its = []
    names = ["Maya", "Liam", "Zoe", "Owen", "Priya", "Kai", "Hana", "Noah", "Amira", "Lucas", "Mei", "Ethan", "Chloe",
             "Mateo", "Leah"]
    ni = [0]

    def nm():
        n = names[ni[0] % len(names)]
        ni[0] += 1
        return n

    # one direction
    for start, place, d, n in [((2, 0), "carpet", "down", 2), ((2, 1), "sink", "right", 3),
                               ((4, 0), "plant", "down", 2), ((1, 0), "easel", "right", 2), ((3, 2), "carpet", "left", 1)]:
        assert route(start, [(d, n)]) == AT[place]
        who = nm()
        perp = "up" if d in ("left", "right") else "left"
        wrong = [say([(OPP[d], n)]), say([(d, n + 1)]), say([(d, n - 1)]) if n > 1 else say([(perp, n)])]
        e = ("Go %s. Do not count %s’s own square. Count %s. That is <b>%s %s</b>."
             % (d, who, count_txt(n), sq(n), d))
        its.append(mcq(fig(map_svg(start, who)) + "Which way does %s go to get to the <b>%s</b>?" % (who, place),
                       say([(d, n)]), wrong, e))
    # two steps
    for start, place, steps in [((0, 1), "carpet", [("right", 2), ("down", 1)]), ((0, 1), "easel", [("right", 3), ("up", 1)]),
                                ((4, 1), "door", [("left", 4), ("up", 1)]), ((1, 1), "plant", [("right", 3), ("down", 1)]),
                                ((3, 1), "coats", [("left", 3), ("down", 1)])]:
        assert route(start, steps) == AT[place], (start, place)
        who = nm()
        (d1, n1), (d2, n2) = steps
        wrong = [say([(OPP[d1], n1), (d2, n2)]), say([(d1, n1 + 1), (d2, n2)]), say([(d1, n1), (OPP[d2], n2)])]
        e = "First go <b>%s %s</b>. Then go <b>%s %s</b>. Count the moves, not %s’s own square." % (sq(n1), d1, sq(n2), d2, who)
        its.append(mcq(fig(map_svg(start, who)) + "Which way does %s go to get to the <b>%s</b>?" % (who, place),
                       say(steps), wrong, e))
    # where do they get to?
    for start, steps in [((1, 1), [("left", 1), ("up", 1)]), ((2, 1), [("right", 2), ("down", 1)]),
                         ((4, 1), [("up", 1), ("right", 1)]), ((3, 1), [("right", 2)]), ((4, 0), [("left", 1)])]:
        end = route(start, steps)
        place = ROOM[end]
        who = nm()
        cand = []
        alt = [[(OPP[steps[0][0]], steps[0][1])] + steps[1:],
               [(steps[0][0], steps[0][1] + 1)] + steps[1:],
               steps[:-1] + [(steps[-1][0], steps[-1][1] + 1)],
               steps[:-1] + [(OPP[steps[-1][0]], steps[-1][1])]]
        for a in alt:
            p = walk(start, a)
            if p in ROOM and ROOM[p] != place and ROOM[p] not in cand:
                cand.append(ROOM[p])
        rest = sorted((k for k in ROOM if ROOM[k] != place),
                      key=lambda k: (abs(k[0] - end[0]) + abs(k[1] - end[1]), k))
        cand += [ROOM[k] for k in rest]
        e = "Go %s. %s gets to the <b>%s</b>." % (" then ".join("%s %s" % (sq(n), d) for d, n in steps), who, place)
        its.append(mcq(fig(map_svg(start, who)) + "%s goes <b>%s</b>. Where is %s now?" % (who, say(steps), he(who)),
                       "the " + place, ["the " + c for c in cand], e))
    # position words on the map
    f0 = fig(map_svg())
    assert ROOM[(4, 2)] == "plant" and ROOM[(5, 1)] == "sink" and ROOM[(5, 0)] == "shelf"
    its.append(mcq(f0 + "What is just to the <b>left</b> of the desk?", "the plant", ["the sink", "the carpet", "the shelf"],
                   "Look at the desk. The square on its left side has the <b>plant</b>. The sink is above the desk."))
    its.append(mcq(f0 + "What is just <b>above</b> the desk?", "the sink", ["the plant", "the shelf", "the carpet"],
                   "Look up from the desk. The <b>sink</b> is in the square above it."))
    its.append(mcq(f0 + "What is in the <b>top right</b> corner?", "the shelf", ["the door", "the desk", "the coats"],
                   "Top is the top row. Right is the side of your right hand. The <b>shelf</b> is there. The door is top left."))
    # how far
    st = (0, 1)
    assert route(st, [("right", 5)]) == AT["sink"]
    its.append(mcq_num(fig(map_svg(st, "Ava")) + "How many squares does Ava move to the right to get to the sink?", 5, [6, 4, 3],
                       "Do not count Ava’s own square. Count 1, 2, 3, 4, 5. That is <b>5</b> squares."))
    assert route((1, 2), [("right", 1)]) == AT["carpet"]
    its.append(mcq_num(fig(map_svg((1, 2), "Arjun")) + "How many squares does Arjun move to the <b>right</b> to get to the carpet?",
                       1, [2, 3, 4], "The carpet is in the very next square. That is <b>1</b> square."))
    assert len(its) == 20, len(its)
    return {"title": "Which way to the carpet? Directions on a classroom map", "items": its}


# ============================================================ set 5: word problems
STREET = {0: "home", 2: "store", 4: "school", 5: "rink", 7: "library"}
SN = 8
SW = 66


def street_icon(kind, cx, cy):
    if kind == "home":
        return ("<rect x='%.1f' y='%.1f' width='26' height='18' fill='#f2d7a6' stroke='%s' stroke-width='1.5'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                "<rect x='%.1f' y='%.1f' width='7' height='10' fill='%s'/>"
                % (cx - 13, cy - 2, INK, cx - 17, cy - 2, cx, cy - 16, cx + 17, cy - 2, COL["red"], INK, cx - 3.5, cy + 6, WOOD))
    if kind == "store":
        s = "<rect x='%.1f' y='%.1f' width='32' height='22' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (cx - 16, cy - 6, INK)
        for i in range(4):
            s += "<rect x='%.1f' y='%.1f' width='8' height='7' fill='%s'/>" % (cx - 16 + i * 8, cy - 13, COL["red"] if i % 2 == 0 else "#fff")
        s += "<rect x='%.1f' y='%.1f' width='32' height='7' fill='none' stroke='%s' stroke-width='1.5'/>" % (cx - 16, cy - 13, INK)
        s += "<rect x='%.1f' y='%.1f' width='8' height='10' fill='%s'/>" % (cx - 4, cy + 6, WOOD)
        return s
    if kind == "school":
        return ("<rect x='%.1f' y='%.1f' width='34' height='20' fill='#e8c39a' stroke='%s' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%.1f' y='%.1f' width='10' height='6' fill='%s'/>"
                "<rect x='%.1f' y='%.1f' width='6' height='6' fill='#dfeef8' stroke='%s' stroke-width='1'/>"
                "<rect x='%.1f' y='%.1f' width='6' height='6' fill='#dfeef8' stroke='%s' stroke-width='1'/>"
                "<rect x='%.1f' y='%.1f' width='7' height='9' fill='%s'/>"
                % (cx - 17, cy - 4, INK, cx, cy - 4, cx, cy - 17, INK, cx, cy - 17, COL["red"],
                   cx - 13, cy + 1, INK, cx + 7, cy + 1, INK, cx - 3.5, cy + 7, WOOD))
    if kind == "rink":
        return ("<rect x='%.1f' y='%.1f' width='38' height='24' rx='9' fill='#e3f2fb' stroke='%s' stroke-width='2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                "<circle cx='%.1f' cy='%.1f' r='4' fill='none' stroke='%s' stroke-width='1.5'/>"
                % (cx - 19, cy - 10, INK, cx, cy - 10, cx, cy + 14, COL["red"], cx, cy + 2, COL["blue"]))
    if kind == "library":
        s = ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#d8d2c8' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             "<rect x='%.1f' y='%.1f' width='32' height='20' fill='#efe9df' stroke='%s' stroke-width='1.5'/>"
             % (cx - 18, cy - 4, cx, cy - 15, cx + 18, cy - 4, INK, cx - 16, cy - 4, INK))
        for x in (cx - 11, cx - 4, cx + 3, cx + 10):
            s += "<rect x='%.1f' y='%.1f' width='3' height='16' fill='%s'/>" % (x - 1.5, cy - 2, SOFT)
        return s
    raise ValueError(kind)


def street_svg():
    W, H = SN * SW + 8, 82
    s = []
    for i in range(SN):
        s.append("<rect x='%d' y='4' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (4 + i * SW, SW, 50, GRAY))
        if i in STREET:
            s.append(street_icon(STREET[i], 4 + i * SW + SW / 2, 28))
            assert len(STREET[i]) * 15 * 0.6 < SW
            s.append(text(4 + i * SW + SW / 2, 74, STREET[i], 15))
    return svg_wrap(W, H, "".join(s), "a path of 8 squares: home, store, school, rink and library")


def set_word(rnd, pos):
    its = []
    # line at the gym door
    line = ["Liam", "Maya", "Owen", "Zoe", "Arjun"]
    g = fig(queue_svg(line, True))
    its.append(mcq(g + "The class lines up at the gym door. Who is just <b>behind</b> Maya?", "Owen",
                   ["Liam", "Zoe", "Arjun"],
                   "Behind Maya means further from the door. That is <b>Owen</b>. Liam is in front of Maya."))
    its.append(mcq(g + "Who is just <b>in front of</b> Zoe?", "Owen", ["Arjun", "Maya", "Liam"],
                   "In front of Zoe means closer to the door. That is <b>Owen</b>. Arjun is behind Zoe."))
    its.append(mcq_num(g + "How many children are in front of Owen?", 2, [3, 1, 4],
                       "Liam and Maya are in front of Owen. That is <b>2</b>. Do not count Owen."))
    # sitting on the carpet
    row = ["Mei", "Noah", "Emma", "Kai", "Leah"]
    r = fig(kids_row_svg(row))
    its.append(mcq(r + "The class sits on the carpet. Who sits just to the <b>right</b> of Noah?", "Emma",
                   ["Mei", "Kai", "Leah"],
                   "Find Noah. Look to the right side. <b>Emma</b> is next. Mei is on Noah’s left side."))
    its.append(mcq(r + "Who sits <b>between</b> Emma and Leah?", "Kai", ["Noah", "Mei", "Emma"],
                   "Emma is on one side. Leah is on the other side. <b>Kai</b> is in the middle."))
    its.append(mcq(r + "Where does Mei sit?", "at the left end",
                   ["at the right end", "between Noah and Emma", "beside Leah"],
                   "Mei is the first child on the left side. She sits <b>at the left end</b>."))
    # coat cubbies
    cub = [["Liam", "Maya", "Owen", "Zoe"], ["Mei", "Kai", "Ava", "Noah"]]
    c = fig(cubbies_svg(cub))
    its.append(mcq(c + "Each child puts winter boots in a cubby. Whose cubby is just <b>above</b> Ava’s?", "Owen’s",
                   ["Noah’s", "Kai’s", "Zoe’s"],
                   "Find Ava’s cubby. Look straight up. It is <b>Owen’s</b>. Noah’s and Kai’s are beside it."))
    its.append(mcq(c + "Whose cubby is just <b>below</b> Zoe’s?", "Noah’s", ["Ava’s", "Owen’s", "Mei’s"],
                   "Find Zoe’s cubby. Look straight down. It is <b>Noah’s</b>."))
    its.append(mcq(c + "Whose cubby is just to the <b>right</b> of Kai’s?", "Ava’s", ["Mei’s", "Maya’s", "Noah’s"],
                   "Find Kai’s cubby. Look to the right side. It is <b>Ava’s</b>. Mei’s is on the left side."))
    # path in the neighbourhood
    st = fig(street_svg())
    AT_S = {v: k for k, v in STREET.items()}
    assert AT_S["home"] + 4 == AT_S["school"]
    its.append(mcq(st + "Ethan is at home. He walks <b>4 squares right</b>. Where is he?", "the school",
                   ["the rink", "the store", "the library"],
                   "Do not count the home square. Count 1, 2, 3, 4. Ethan is at the <b>school</b>. 5 squares would be the rink."))
    assert AT_S["library"] - 2 == AT_S["rink"]
    its.append(mcq(st + "Sofia is at the library. She walks <b>2 squares left</b> to skate. Where is she?", "the rink",
                   ["the school", "the store", "home"],
                   "Do not count the library square. Count 1, 2 to the left. Sofia is at the <b>rink</b>."))
    its.append(mcq_num(st + "How many squares is it from home to the school?", 4, [5, 3, 6],
                       "Do not count the home square. Count the moves: 1, 2, 3, 4. That is <b>4</b>."))
    d = AT_S["rink"] - AT_S["store"]
    assert d == 3
    its.append(mcq(st + "Jayden is at the rink. Which way does he go to get to the store?", "3 squares left",
                   ["3 squares right", "4 squares left", "2 squares left"],
                   "The store is on the left side of the rink. Count the moves: 1, 2, 3. That is <b>3 squares left</b>."))
    # bookcase in the classroom
    sh = [["star", "ball", "duck"], ["mitt", "beaver", "apple"], ["teddy", "cat", "puck"]]
    b = fig(scene_svg(shelf_scene(sh), "a bookcase with 3 shelves of toys"))
    its.append(mcq(b + "Olivia wants the toy on the middle shelf, just to the <b>right</b> of the beaver. What does she get?",
                   "the apple", ["the mitt", "the duck", "the puck"],
                   "The middle shelf has the mitt, the beaver and the apple. Just to the right of the beaver is the <b>apple</b>."))
    its.append(mcq(b + "Aiden puts away the puck. What is just <b>above</b> the puck?", "the apple",
                   ["the cat", "the duck", "the teddy"],
                   "The puck is on the bottom shelf. Look up one shelf. The <b>apple</b> is there. The cat is beside the puck."))
    # grid: how many more squares
    start, tgt = (1, 3), (3, 0)
    k = "star"
    its.append(mcq_num(fig(grid_svg(start, {tgt: k})) + "The beaver goes 2 squares right. How many squares <b>up</b> to get to the star now?",
                       start[1] - tgt[1], [4, 2, 5],
                       "After 2 squares right, the star is straight up. Count 1, 2, 3. That is <b>3</b>."))
    assert walk(start, [("right", 2), ("up", 3)]) == tgt
    # no picture
    its.append(mcq("Kai takes 3 steps forward. Then he takes 3 steps back. Where is he now?",
                   "where he started", ["3 steps forward", "6 steps forward", "3 steps back"],
                   "3 steps forward and 3 steps back cancel out. Kai is back <b>where he started</b>."))
    its.append(mcq("Zoe stands in front of Lucas in a line. Where is Lucas?", "behind Zoe",
                   ["in front of Zoe", "above Zoe", "under Zoe"],
                   "If Zoe is in front of Lucas, then Lucas is <b>behind Zoe</b>."))
    its.append(mcq_num("Nathan walks 3 squares up. Then he walks 2 squares right. How many squares does he walk in all?",
                       5, [6, 1, 4], "Add the moves: 3 + 2 = <b>5</b>. Do not count the square he starts on."))
    its.append(mcq("Emma says, “Go 2 squares right, then 1 square up.” Liam goes 2 squares left, then 1 square up. What did Liam mix up?",
                   "left and right", ["up and down", "how many squares", "nothing"],
                   "Emma said right. Liam went left. He mixed up <b>left and right</b>. The up move was correct."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: lines, cubbies and the way to the rink", "items": its}


# ============================================================ lesson
def body_html():
    f1 = strip([table_scene("beaver", "on"), table_scene("ball", "under"), table_scene("balloon", "above"),
                table_scene("duck", "beside")], ["on", "under", "above", "beside"],
               "a table with a beaver on it, a ball under it, a balloon above it and a duck beside it", k=0.62)
    f2 = strip([box_scene("teddy", "behind"), box_scene("ball", "in front of")], ["behind", "in front of"],
               "a teddy behind a box and a ball in front of a box", k=0.8)
    f3 = scene_svg(row_scene(["beaver", "ball", "apple", "teddy", "duck"], labels=True),
                   "a row of toys with left and right marked")
    f4 = grid_svg((1, 3), {(3, 2): "star", (4, 1): "ball"}, path=[("right", 2), ("up", 1)],
                  label="grid with a beaver and a dashed path 2 squares right then 1 square up to a star")
    f5 = map_svg((0, 1), "Maya")
    assert route((0, 1), [("right", 2), ("down", 1)]) == AT["carpet"]
    return (
        "<h2>Where is it?</h2>"
        "<p>Position words tell us <b>where</b> something is.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption><b>On</b> touches the top. <b>Above</b> is higher, with a gap. <b>Under</b> or <b>below</b> is lower. <b>Beside</b> is at the side.</figcaption></figure>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption><b>Behind</b>: the box hides part of the teddy. <b>In front of</b>: the ball is closer to us.</figcaption></figure>"
        "<p><b>Between</b> means in the middle of two things.</p>"
        "<h2>Left and right</h2>"
        "<p><b>Left</b> is the side of your left hand. <b>Right</b> is the side of your right hand. "
        "Look at the picture from where you sit.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>The beaver is at the left end. The ball is 2nd from the left. The duck is at the right end.</figcaption></figure>"
        "<h2>Follow moves on a grid</h2>"
        "<p>Move one square at a time. Say each number as you move.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>2 squares right, then 1 square up. The beaver gets to the star.</figcaption></figure>"
        "<p>Count the <b>moves</b>, not the square you start on.</p>"
        "<h2>Which way to the carpet?</h2>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>Maya goes 2 squares right, then 1 square down. She gets to the carpet.</figcaption></figure>" +
        ex("Example 1", "Zoe stands in front of Owen in a line. Where is Owen?",
           "Zoe is closer to the front. Owen is further back.", "behind Zoe") +
        ex("Example 2", "Maya is 2 squares to the left of the easel. Which way does she go?",
           "The easel is on her right side. Count the moves: 1, 2.", "2 squares right") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up left and right", "Hold up your hands. Your left hand makes an L shape"],
            ["Counting the start square", "Count the moves: 1, 2, 3 …"],
            ["Mixing up up and down", "Up is toward the top of the page"],
            ["Saying on when it is above", "On touches. Above has a gap"],
            ["Doing the moves in the wrong order", "Do the first move, then the second move"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about position and directions in Ontario math?",
     "a": "In the Ontario curriculum (Spatial Sense, E1.4 and E1.5), Grade 1 students describe where things are with words like above, below, beside, between, in front of, behind, left and right. They also give and follow directions to move from one place to another."},
    {"q": "How can I help my child learn left and right?",
     "a": "Hold up both hands, fingers up and thumbs out. The left hand makes an L shape. Play “touch your left ear” and say left and right on the walk to school."},
    {"q": "What are good direction games for Grade 1?",
     "a": "Play “robot”: one child gives directions like “3 steps forward, then 2 steps right” and the other follows. A treasure hunt to the carpet or the cubbies works well too."},
    {"q": "Why does my child get one square too many or too few?",
     "a": "Many children count the square they start on. Show them to count each move instead: touch the next square and say 1, then 2, and so on."},
]


def gen():
    rnd = random.Random(41812)
    pos = Pos(rnd)
    sets = [set_position(rnd, pos), set_left_right(rnd, pos), set_grid(rnd, pos), set_map(rnd, pos),
            set_word(rnd, pos)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"][-120:]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "position-and-directions", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Position and Directions: Left, Right and Moves on a Grid",
        "seo_title": "Grade 1 Position and Directions Worksheets: Left, Right and Maps (Free)",
        "short_title": "Position and directions",
        "domain": "Spatial Sense",
        "standard_code": "Grade 1: E1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Give and follow directions for moving from one location to another",
        "meta_desc": "Free Grade 1 math worksheets on position and directions for the Ontario curriculum: above, below, beside, between, in front of and behind, left and right, following moves like 2 squares right and 1 up on a grid, and finding the way on a classroom map. 100 picture questions with an answer key.",
        "key_big": "Count the moves, not the square you start on.",
        "key_sub": "Left is the side of your left hand. Right is the side of your right hand. Do the first move, then the second move.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four pictures labelled A to D|a row of toys|a teddy, a beaver|a star, a duck|a cat, a book|grid with|a classroom map|children in a line|children sitting|a path of squares|cubbies)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
