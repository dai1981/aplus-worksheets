# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Position and Directions (Australian Curriculum v9.0, AC9M1SP02)
  python3 tools/gen_au_maths_y1_position.py
Position words (above, below, next to, between, in front of, behind), left and right,
following directions on a grid (forward, turn right / left), finding the way to the sandpit on a
playground map, and quarter and half turns at school.
Every picture is drawn from the data that the answer is worked out from, so picture and answer agree.
"Left" and "right" in a row mean the left and right of the picture as the child looks at it;
"turn right" means the robot's or person's own right (clockwise, seen from above).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
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
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A-D pictures, turns, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c >= 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    if w == h:
        w += 1                     # keep figures out of the larger 'square' print size unless wanted
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
        "book": (12, 12, 30), "koala": (19, 19, 44)}
NAME = {k: k for k in SIZE}


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
    elif kind == "koala":
        g = colour or "#9aa0a6"
        s = ("<ellipse cx='%.1f' cy='%.1f' rx='13' ry='12' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='7' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='7' fill='%s' stroke='%s' stroke-width='2'/>"
             "<circle cx='%.1f' cy='%.1f' r='3.5' fill='#efe8df'/><circle cx='%.1f' cy='%.1f' r='3.5' fill='#efe8df'/>"
             "<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='%s' stroke-width='2'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='3.5' ry='4.5' fill='%s'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>"
             % (x, b - 13, g, INK, x - 12, b - 36, g, INK, x + 12, b - 36, g, INK,
                x - 12, b - 36, x + 12, b - 36, x, b - 30, g, INK, x, b - 27, INK,
                x - 5, b - 33, INK, x + 5, b - 33, INK))
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
    """A table, and one object on / under / above / next to it."""
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
    elif where == "next to":
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
    elif where == "next to":
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
        s.append(icon(k, 8 + step / 2 + i * step, F - 1.5, (colours or {}).get(i)))
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
    """Children in a line to a door. names[0] is nearest the door (first)."""
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
def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dirv(deg):
    t = math.radians(deg)
    return (math.cos(t), -math.sin(t))


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def head(tip, d, col, L=11, W=7):
    d = norm(d)
    nr = (-d[1], d[0])
    b = add(tip, d, -L)
    pts = [tip, add(b, nr, W), add(b, nr, -W)]
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col)


def turn_svg(frac, cw=True, r=30):
    """Dashed line for the start, a curved arrow for the turn and a solid line for the end."""
    c = (r + 22, r + 22)
    s = []
    up = add(c, dirv(90), r + 14)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' stroke-dasharray='5 4'/>"
             % (c[0], c[1], up[0], up[1], INK))
    sweep = 360.0 * frac
    sg = -1 if cw else 1
    drawn = min(sweep - 20, 330.0)
    n = max(8, int(drawn / 5))
    pts = [add(c, dirv(90 + sg * drawn * i / n), r) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (" ".join("%.1f,%.1f" % p for p in pts), GREEN))
    end_a = 90 + sg * drawn
    end = add(c, dirv(end_a), r)
    s.append(head(add(end, dirv(end_a + sg * 90), 8), dirv(end_a + sg * 90), GREEN))
    if frac < 1:
        e = add(c, dirv(90 + sg * sweep), r + 14)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (c[0], c[1], e[0], e[1], INK))
    s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (c[0], c[1], INK))
    S = 2 * (r + 22)
    return "".join(s), S, S


TURNS = ["quarter turn", "half turn", "three-quarter turn", "whole turn"]
QT = {"quarter turn": 1, "half turn": 2, "three-quarter turn": 3, "whole turn": 4}
PLACES = ["tree", "house", "pond", "swings"]     # top, right, bottom, left (clockwise)


def facing_svg(face, names=PLACES):
    """A child seen from above in the middle, with an arrow to the way she faces;
    the 4 places are written on the 4 sides."""
    W, H = 264, 172
    c = (W / 2, H / 2 + 2)
    s = []
    pos = [(c[0], 20), (W - 8, c[1] + 5), (c[0], H - 8), (8, c[1] + 5)]
    anc = ["middle", "end", "middle", "start"]
    for i, t in enumerate(names):
        s.append(text(pos[i][0], pos[i][1], t, 17, anc[i]))
    d = [(0, -1), (1, 0), (0, 1), (-1, 0)][face]
    s.append("<circle cx='%.1f' cy='%.1f' r='12' fill='%s' stroke='%s' stroke-width='2.5'/>" % (c[0], c[1], FILL, GREEN))
    a = add(c, d, 14)
    b = add(c, d, 34)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.4'/>" % (a[0], a[1], b[0], b[1], INK))
    s.append(head(add(c, d, 43), d, INK, 10, 7))
    return svg_wrap(W, H, "".join(s), "a child seen from above facing the %s; %s at the top, %s on the right, %s at the bottom, %s on the left" % ((names[face],) + tuple(names)))


def arrow_body(d, x, y, L=34):
    """Arrow centred at (x, y) pointing d (0 up, 1 right, 2 down, 3 left)."""
    v = [(0, -1), (1, 0), (0, 1), (-1, 0)][d]
    a = add((x, y), v, -L / 2)
    b = add((x, y), v, L / 2 - 10)
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
            % (a[0], a[1], b[0], b[1], GREEN) + head(add((x, y), v, L / 2), v, GREEN, 13, 9))


def before_after_svg(d0, d1):
    W, H = 200, 82
    s = [arrow_body(d0, 45, 34), arrow_body(d1, 155, 34), text(45, 76, "start", 15), text(155, 76, "end", 15)]
    s.append("<line x1='82' y1='34' x2='112' y2='34' stroke='%s' stroke-width='2'/>" % SOFT)
    s.append(head((120, 34), (1, 0), SOFT, 9, 6))
    names = ["up", "right", "down", "left"]
    return svg_wrap(W, H, "".join(s), "arrow pointing %s at the start and %s at the end" % (names[d0], names[d1]))
GC, GR, CS = 7, 4, 36
DIRS = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}
FACE_I = {"up": 0, "right": 1, "down": 2, "left": 3}


def robot(cx, cy, face):
    s = ("<rect x='%.1f' y='%.1f' width='24' height='22' rx='5' fill='#9fb4c8' stroke='%s' stroke-width='2'/>"
         "<circle cx='%.1f' cy='%.1f' r='2.6' fill='%s'/><circle cx='%.1f' cy='%.1f' r='2.6' fill='%s'/>"
         % (cx - 12, cy - 11, INK, cx - 5, cy - 3, INK, cx + 5, cy - 3, INK))
    v = [(0, -1), (1, 0), (0, 1), (-1, 0)][FACE_I[face]]
    s += head(add((cx, cy), v, 17.5), v, COL["red"], 7, 6)
    return s


def grid_svg(start, face, items):
    """items: {(col, row): kind}."""
    W, H = GC * CS + 8, GR * CS + 8
    s = []
    for r in range(GR):
        for c in range(GC):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                     % (4 + c * CS, 4 + r * CS, CS, CS, GRAY))
    for (c, r), k in sorted(items.items()):
        assert 0 <= c < GC and 0 <= r < GR and (c, r) != start
        hl, hr, hh = SIZE[kind_ok(k)]
        kk = 0.66
        s.append(scaled(k, 4 + c * CS + CS / 2 - (hr - hl) * kk / 2, 4 + r * CS + CS / 2 + hh * kk / 2, kk))
    s.append(robot(4 + start[0] * CS + CS / 2, 4 + start[1] * CS + CS / 2, face))
    return svg_wrap(W, H, "".join(s), "grid with a toy robot and objects")


def kind_ok(k):
    assert k in SIZE and k not in ("balloon", "car", "book"), k
    return k


def mv(p, d, n):
    return (p[0] + DIRS[d][0] * n, p[1] + DIRS[d][1] * n)


OPP = {"right": "left", "left": "right", "up": "down", "down": "up"}
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



DN = ["up", "right", "down", "left"]


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


# ============================================================ set 1: position words
def set_position(rnd, pos):
    its = []
    other = {"on": ["above", "under", "next to"], "under": ["on", "next to", "above"],
             "above": ["on", "under", "next to"], "next to": ["on", "under", "above"]}
    why_t = {
        "on": "The %s is <b>on</b> the table. It touches the table top.",
        "under": "The %s is <b>under</b> the table. It is below the table top.",
        "above": "The %s is <b>above</b> the table. It is higher than the table, with a gap.",
        "next to": "The %s is <b>next to</b> the table. It is at the side, close by.",
    }
    for kind, where in [("koala", "on"), ("ball", "under"), ("balloon", "above"), ("duck", "next to"),
                        ("teddy", "on"), ("cat", "under")]:
        e = why_t[where] % kind
        if where == "on":
            e += " Above would have a gap."
        if where == "above":
            e += " It does not touch the table, so it is not on it."
        its.append(mcq(fig(table_svg(kind, where, "a %s %s a table" % (kind, where))) + "Where is the %s?" % kind,
                       where + " the table", [w + " the table" for w in other[where]], e))
    bx = {"in front of": ["behind", "on", "next to"], "behind": ["in front of", "on", "next to"]}
    for kind, where in [("koala", "behind"), ("ball", "in front of"), ("teddy", "in front of"), ("duck", "behind")]:
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
    row = ["teddy", "koala", "ball"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a teddy, a koala and a ball in a row")) +
                   "What is <b>between</b> the teddy and the ball?", "the koala", ["the teddy", "the ball", "the cat"],
                   "Between means in the middle. The <b>koala</b> is in the middle."))
    row = ["star", "duck", "apple", "car"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a star, a duck, an apple and a car in a row")) +
                   "What is between the duck and the car?", "the apple", ["the star", "the duck", "the car"],
                   "Find the duck and the car. The <b>apple</b> is in the middle of them."))
    row = ["cat", "book", "duck"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a cat, a book and a duck in a row")) +
                   "Where is the book?", "between the cat and the duck",
                   ["on the duck", "under the cat", "above the duck"],
                   "The cat is on one side. The duck is on the other side. The book is <b>between</b> them."))
    # shelves: above and below
    sh1 = [["star", "ball"], ["koala", "apple"], ["cat", "duck"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh1), "a bookcase with 3 shelves of toys")) +
                   "What is just <b>above</b> the koala?", "the star", ["the cat", "the apple", "the ball"],
                   "Look up from the koala. The <b>star</b> is on the shelf above. The cat is below."))
    sh2 = [["teddy", "car"], ["apple", "star"], ["ball", "koala"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh2), "a bookcase with 3 shelves of toys")) +
                   "What is just <b>below</b> the star?", "the koala", ["the car", "the apple", "the ball"],
                   "Look down from the star. The <b>koala</b> is on the shelf below. The car is above."))
    sh3 = [["duck", "apple"], ["car", "teddy"], ["cat", "star"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh3), "a bookcase with 3 shelves of toys")) +
                   "Where is the apple?", "above the teddy", ["below the teddy", "next to the teddy", "below the star"],
                   "The apple is on the top shelf. The teddy is on the shelf under it. The apple is <b>above</b> the teddy."))
    sh4 = [["ball", "book"], ["duck", "koala"], ["star", "cat"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh4), "a bookcase with 3 shelves of toys")) +
                   "Where is the star?", "below the duck", ["above the duck", "next to the koala", "above the cat"],
                   "The star is on the bottom shelf. The duck is on the shelf over it. The star is <b>below</b> the duck."))
    # A-D pictures
    its.append(pick4("Which picture shows the duck <b>under</b> the table?",
                     [table_scene("duck", "under"), table_scene("duck", "on"), table_scene("duck", "next to"),
                      table_scene("ball", "under", COL["red"])],
                     "The duck is below the table top. In one picture a ball is under the table, not the duck.",
                     pos, "four pictures labelled A to D of a table"))
    its.append(pick4("Which picture shows the koala <b>behind</b> the box?",
                     [box_scene("koala", "behind"), box_scene("koala", "in front of"), box_scene("koala", "on"),
                      box_scene("koala", "next to")],
                     "The box hides part of the koala. So the koala is behind the box.",
                     pos, "four pictures labelled A to D of a box"))
    its.append(pick4("Which picture shows the balloon <b>above</b> the table?",
                     [table_scene("balloon", "above"), table_scene("teddy", "on"), table_scene("cat", "under"),
                      table_scene("teddy", "next to")],
                     "The balloon is higher than the table. There is a gap.",
                     pos, "four pictures labelled A to D of a table"))
    assert len(its) == 20, len(its)
    return {"title": "Above, below, next to, between, in front of, behind", "items": its}


# ============================================================ set 2: left and right
NTH = ["1st", "2nd", "3rd", "4th", "5th", "6th"]


def set_left_right(rnd, pos):
    its = []

    def row_q(kinds, q, ans_i, wrong_i, e, labels):
        lab = "a row of toys: " + ", ".join(kinds)
        assert len(set(kinds)) == len(kinds)
        return mcq(fig(scene_svg(row_scene(kinds, labels=labels), lab)) + q,
                   "the " + kinds[ans_i], ["the " + kinds[j] for j in wrong_i], e)

    k = ["koala", "ball", "car", "duck", "star"]
    its.append(row_q(k, "Which toy is at the <b>left</b> end?", 0, [4, 1, 3],
                     "Left is the side of your left hand. The <b>koala</b> is at the left end.", True))
    k = ["apple", "teddy", "book", "cat"]
    its.append(row_q(k, "Which toy is at the <b>right</b> end?", 3, [0, 2, 1],
                     "Right is the side of your right hand. The <b>cat</b> is at the right end.", True))
    k = ["duck", "star", "koala", "apple", "ball"]
    its.append(row_q(k, "Which toy is at the <b>right</b> end?", 4, [0, 3, 1],
                     "Right is the side of your right hand. The <b>ball</b> is at the right end. The duck is at the left end.", False))
    k = ["car", "cat", "teddy", "book"]
    its.append(row_q(k, "Which toy is at the <b>left</b> end?", 0, [3, 1, 2],
                     "Left is the side of your left hand. The <b>car</b> is at the left end.", False))
    plans = [(["teddy", "duck", "ball", "koala", "car"], "left", 2, True),
             (["star", "apple", "cat", "duck", "book"], "right", 2, True),
             (["ball", "koala", "star", "teddy", "apple", "cat"], "left", 3, False),
             (["book", "car", "duck", "apple", "koala", "star"], "right", 3, False),
             (["cat", "teddy", "apple", "ball", "duck"], "left", 4, False),
             (["apple", "star", "car", "koala", "teddy", "ball"], "right", 2, False)]
    for kinds, side, n, lab in plans:
        L = len(kinds)
        i = n - 1 if side == "left" else L - n
        j_other = L - n if side == "left" else n - 1
        j_skip = i + (1 if side == "left" else -1)
        j_short = i - (1 if side == "left" else -1)
        wr = [j for j in [j_other, j_skip, j_short] + list(range(L)) if 0 <= j < L and j != i]
        e = ("Start at the %s end. Count %s: %s. The %s toy is the <b>%s</b>."
             % (side, ", ".join(str(t + 1) for t in range(n)),
                ", ".join("the " + kinds[(t if side == "left" else L - 1 - t)] for t in range(n)), NTH[n - 1], kinds[i]))
        its.append(row_q(kinds, "Which toy is <b>%s from the %s</b>?" % (NTH[n - 1], side), i, wr, e, lab))
    plans = [(["duck", "cat", "koala", "book", "ball"], 2, "right"), (["star", "car", "apple", "teddy", "duck"], 2, "left"),
             (["ball", "apple", "teddy", "koala", "cat"], 3, "left"), (["koala", "book", "duck", "star", "car"], 2, "right")]
    for kinds, ref, side in plans:
        i = ref + (1 if side == "right" else -1)
        o = ref - (1 if side == "right" else -1)
        two = ref + (2 if side == "right" else -2)
        cands = [o] + ([two] if 0 <= two < len(kinds) else []) + [t for t in range(len(kinds)) if t not in (i, o, two, ref)]
        e = ("Find the %s. Look to the %s side of it. The toy just to the %s is the <b>%s</b>. The %s is on the other side."
             % (kinds[ref], side, side, kinds[i], kinds[o]))
        its.append(row_q(kinds, "What is just to the <b>%s</b> of the %s?" % (side, kinds[ref]), i, cands[:3], e, False))
    for kinds, a, b in [(["koala", "ball"], 0, 1), (["star", "duck", "car"], 2, 0), (["apple", "cat", "teddy"], 1, 2)]:
        side = "to the left" if a < b else "to the right"
        e = ("The %s is on the %s side of the %s. So it is <b>%s</b> of the %s."
             % (kinds[a], "left" if a < b else "right", kinds[b], side, kinds[b]))
        its.append(mcq(fig(scene_svg(row_scene(kinds), "a row of toys: " + ", ".join(kinds))) +
                       "Where is the %s?" % kinds[a], side + " of the " + kinds[b],
                       [("to the right" if a < b else "to the left") + " of the " + kinds[b],
                        "above the " + kinds[b], "behind the " + kinds[b]], e))

    def lr(a, b):
        return row_scene([a, b], step=62)
    its.append(pick4("Which picture shows the koala to the <b>left</b> of the ball?",
                     [lr("koala", "ball"), lr("ball", "koala"), lr("teddy", "ball"), lr("ball", "teddy")],
                     "The koala is on the left side. The ball is on the right side.",
                     pos, "four pictures labelled A to D of two toys"))
    its.append(pick4("Which picture shows the duck to the <b>right</b> of the star?",
                     [lr("star", "duck"), lr("duck", "star"), lr("star", "cat"), lr("cat", "duck")],
                     "The star is on the left side. The duck is on the right side.",
                     pos, "four pictures labelled A to D of two toys"))
    k = ["car", "koala", "apple", "duck"]
    its.append(mcq(fig(scene_svg(row_scene(k, labels=True), "a row of toys: " + ", ".join(k))) +
                   "The car is 1st from the left. What is it from the right?", "4th", ["1st", "3rd", "5th"],
                   "Start at the right end: duck 1st, apple 2nd, koala 3rd, car <b>4th</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Left and right", "items": its}


# ============================================================ set 3: robot on a grid
POOL = ["apple", "ball", "cat", "teddy", "duck", "star", "koala"]


def inside(c):
    return 0 <= c[0] < GC and 0 <= c[1] < GR


def turned(face, way):
    return DN[(FACE_I[face] + (1 if way == "right" else -1)) % 4]


def pick_cells(start, cands):
    assert inside(cands[0]) and cands[0] != start, (start, cands[0])
    out = []
    for c in cands:
        if inside(c) and c != start and c not in out:
            out.append(c)
    assert len(out) >= 4, (start, out)
    return out[:4]


def items_for(rnd, cells):
    kinds = rnd.sample(POOL, 4)
    return dict(zip(cells, kinds)), kinds


def forward_q(rnd, start, face, n):
    cells = pick_cells(start, [mv(start, face, n), mv(start, face, n - 1), mv(start, face, n + 1),
                               mv(start, OPP[face], n), mv(start, turned(face, "right"), 1),
                               mv(start, turned(face, "left"), 1)])
    items, kinds = items_for(rnd, cells)
    q = (fig(grid_svg(start, face, items)) + "The robot goes <b>%s forward</b>. Where does it stop?" % sq(n))
    e = ("Forward is the way the red arrow points. Do not count the robot’s own square. "
         "Count %s. It stops on the <b>%s</b>." % (", ".join(str(i) for i in range(1, n + 1)), kinds[0]))
    return mcq(q, "the " + kinds[0], ["the " + k for k in kinds[1:]], e)


def turn_q(rnd, start, face, way, n):
    nd = turned(face, way)
    other = turned(face, "left" if way == "right" else "right")
    cells = pick_cells(start, [mv(start, nd, n), mv(start, other, n), mv(start, face, n), mv(start, nd, n - 1),
                               mv(start, nd, n + 1), mv(start, face, n - 1), mv(start, face, n + 1)])
    items, kinds = items_for(rnd, cells)
    q = (fig(grid_svg(start, face, items)) +
         "The robot turns <b>%s</b>. Then it goes <b>%s forward</b>. Where does it stop?" % (way, sq(n)))
    e = ("Turn first. The robot points %s. A %s turn makes it point <b>%s</b>. "
         "Then count %s. It stops on the <b>%s</b>."
         % (face, way, nd, ", ".join(str(i) for i in range(1, n + 1)), kinds[0]))
    return mcq(q, "the " + kinds[0], ["the " + k for k in kinds[1:]], e)


def two_move_q(rnd, start, face, n1, way, n2):
    mid = mv(start, face, n1)
    nd = turned(face, way)
    other = turned(face, "left" if way == "right" else "right")
    cells = pick_cells(start, [mv(mid, nd, n2), mv(mid, other, n2), mv(mid, face, n2), mv(mid, nd, n2 - 1),
                               mv(mv(start, face, n1 + 1), nd, n2), mv(mid, nd, n2 + 1), mv(mv(start, face, n1 - 1), nd, n2)])
    assert inside(mid) and mid not in cells
    items, kinds = items_for(rnd, cells)
    q = (fig(grid_svg(start, face, items)) +
         "The robot goes <b>%s forward</b>. It turns <b>%s</b>. Then it goes <b>%s forward</b>. Where does it stop?"
         % (sq(n1), way, sq(n2)))
    e = ("It points %s, so go %s %s first. Turn %s: now it points %s. Go %s more. It stops on the <b>%s</b>."
         % (face, sq(n1), face, way, nd, sq(n2), kinds[0]))
    return mcq(q, "the " + kinds[0], ["the " + k for k in kinds[1:]], e)


def robot_big_svg(face):
    body = "<g transform='translate(36 36) scale(2)'>%s</g>" % robot(0, 0, face)
    return svg_wrap(72, 72, body, "a toy robot pointing %s" % face)


def set_robot(rnd, pos):
    its = []
    for start, face, n in [((0, 1), "right", 3), ((6, 2), "left", 2), ((2, 3), "up", 2), ((4, 0), "down", 2),
                           ((1, 2), "right", 4), ((5, 3), "up", 2)]:
        its.append(forward_q(rnd, start, face, n))
    for start, d, n, wr in [((1, 1), "right", 4, [5, 3, 2]), ((6, 3), "left", 3, [4, 2, 5]), ((3, 3), "up", 3, [4, 2, 1])]:
        k = rnd.choice(POOL)
        items = {mv(start, d, n): k}
        its.append(mcq_num(fig(grid_svg(start, d, items)) +
                           "How many squares forward to get to the %s?" % k, n, wr,
                           "Do not count the robot’s own square. Count each move: %s. That is <b>%d</b>."
                           % (", ".join(str(i) for i in range(1, n + 1)), n)))
    for start, face, way, n in [((3, 3), "up", "right", 2), ((3, 2), "up", "left", 2), ((1, 1), "right", "right", 2),
                                ((2, 3), "right", "left", 2), ((5, 3), "left", "right", 2), ((5, 0), "left", "left", 3)]:
        its.append(turn_q(rnd, start, face, way, n))
    for args in [((0, 3), "right", 2, "left", 2), ((1, 0), "down", 2, "left", 3), ((6, 3), "up", 1, "left", 3)]:
        its.append(two_move_q(rnd, *args))
    for face, way in [("up", "right"), ("right", "right")]:
        nd = turned(face, way)
        its.append(mcq_fixed(fig(robot_big_svg(face)) + "The robot points %s. It turns <b>%s</b>. Which way does it point now?"
                             % (face, way), DN, nd,
                             "A right turn goes the same way as clock hands. From %s, it now points <b>%s</b>." % (face, nd)))
    assert len(its) == 20, len(its)
    return {"title": "Follow directions on a grid: forward, turn left, turn right", "items": its}


# ============================================================ set 4: playground map
MC, MH, MCOLS, MROWS = 64, 58, 6, 3
PLAY = {(0, 0): "tree", (3, 0): "slide", (5, 0): "swings",
        (5, 1): "cubby",
        (0, 2): "gate", (2, 2): "sandpit", (4, 2): "tap", (5, 2): "bin"}
AT = {v: k for k, v in PLAY.items()}


def place_icon(kind, cx, cy):
    if kind == "tree":
        return ("<rect x='%.1f' y='%.1f' width='6' height='13' fill='#8a5a33'/>"
                "<circle cx='%.1f' cy='%.1f' r='12' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx - 3, cy + 2, cx, cy - 5, COL["green"], INK))
    if kind == "slide":
        s = ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
             % (cx - 16, cy + 14, cx - 16, cy - 12, INK, cx - 9, cy + 14, cx - 9, cy - 12, INK))
        for y in (cy - 6, cy + 1, cy + 8):
            s += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (cx - 16, y, cx - 9, y, INK)
        s += ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
              % (cx - 9, cy - 12, cx + 6, cy - 8, cx + 17, cy + 13, COL["red"]))
        return s
    if kind == "swings":
        s = ("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
             % (cx - 20, cy + 15, cx - 15, cy - 13, cx + 15, cy - 13, cx + 20, cy + 15, INK))
        for x in (cx - 7, cx + 7):
            s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
                  "<rect x='%.1f' y='%.1f' width='10' height='3.5' fill='%s'/>" % (x, cy - 13, x, cy + 5, INK, x - 5, cy + 5, COL["blue"]))
        return s
    if kind == "cubby":
        return ("<rect x='%.1f' y='%.1f' width='28' height='16' fill='#f2d7a6' stroke='%s' stroke-width='1.5'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                "<rect x='%.1f' y='%.1f' width='8' height='10' fill='%s'/>"
                % (cx - 14, cy - 1, INK, cx - 18, cy - 1, cx, cy - 15, cx + 18, cy - 1, COL["red"], INK, cx - 4, cy + 5, WOOD))
    if kind == "sandpit":
        return ("<rect x='%.1f' y='%.1f' width='38' height='20' rx='3' fill='#f1d8a0' stroke='%s' stroke-width='2.5'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1'/>"
                "<circle cx='%.1f' cy='%.1f' r='1.5' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.5' fill='%s'/>"
                % (cx - 19, cy - 6, WOOD, cx + 3, cy - 2, cx + 13, cy - 2, cx + 11, cy + 9, cx + 5, cy + 9, COL["blue"], INK,
                   cx - 11, cy + 2, SOFT, cx - 5, cy + 7, SOFT))
    if kind == "tap":
        return ("<rect x='%.1f' y='%.1f' width='6' height='28' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<rect x='%.1f' y='%.1f' width='13' height='5' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<rect x='%.1f' y='%.1f' width='8' height='3' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>"
                % (cx - 10, cy - 13, GRAY, INK, cx - 4, cy - 9, GRAY, INK, cx - 11, cy - 17, INK, cx + 6, cy + 3, COL["blue"]))
    if kind == "gate":
        s = ("<rect x='%.1f' y='%.1f' width='4' height='28' fill='%s'/><rect x='%.1f' y='%.1f' width='4' height='28' fill='%s'/>"
             % (cx - 18, cy - 13, INK, cx + 14, cy - 13, INK))
        for y in (cy - 7, cy + 1, cy + 9):
            s += "<rect x='%.1f' y='%.1f' width='28' height='3' fill='%s'/>" % (cx - 14, y, WOOD)
        return s
    if kind == "bin":
        return ("<rect x='%.1f' y='%.1f' width='20' height='22' rx='2' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%.1f' y='%.1f' width='24' height='5' rx='1' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx - 10, cy - 7, COL["green"], INK, cx - 12, cy - 13, COL["yellow"], INK))
    raise ValueError(kind)


def map_svg(start=None, name=None):
    W, H = MCOLS * MC + 8, MROWS * MH + 8
    s = []
    for r in range(MROWS):
        for c in range(MCOLS):
            fillc = FILL if (c, r) == start else "#fff"
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (4 + c * MC, 4 + r * MH, MC, MH, fillc, GRAY))
    for (c, r), k in sorted(PLAY.items()):
        assert (c, r) != start
        cx, top = 4 + c * MC + MC / 2, 4 + r * MH
        s.append(place_icon(k, cx, top + 22))
        s.append(text(cx, top + 53, k, 14))
    lab = "a playground map with a tree, slide, swings, cubby, gate, sandpit, tap and bin"
    if start:
        cx, top = 4 + start[0] * MC + MC / 2, 4 + start[1] * MH
        s.append("<g transform='translate(%.1f %.1f) scale(0.8)'>%s</g>" % (cx, top + 38, child(0, 0, SHIRT[1])))
        s.append(text(cx, top + 53, name, 14, col=GREEN))
        lab += "; %s is on a square" % name
    return svg_wrap(W, H, "".join(s), lab)


def walk(p, d, n):
    """Cells passed on the way (not the start), all must be inside the map."""
    out = []
    for i in range(1, n + 1):
        out.append(mv(p, d, i))
    return out


def route(start, dests):
    """dests: [(dir, n), ...]. Checks that every square passed before the end is empty."""
    p, path = start, []
    for d, n in dests:
        path += walk(p, d, n)
        p = path[-1]
    for c in path:
        assert 0 <= c[0] < MCOLS and 0 <= c[1] < MROWS, (start, dests)
    for c in path[:-1]:
        assert c not in PLAY, ("passes through", PLAY[c], start, dests)
    return p


def say(steps):
    return ", then ".join("%s %s" % (sq(n), d) for d, n in steps)


def set_map(rnd, pos):
    its = []
    names = ["Mia", "Jack", "Ava", "Leo", "Isla", "Kai", "Ruby", "Noah", "Zara", "Liam"]
    ni = [0]

    def nm():
        n = names[ni[0] % len(names)]
        ni[0] += 1
        return n

    # one direction
    for start, place, d, n in [((2, 0), "sandpit", "down", 2), ((2, 1), "cubby", "right", 3),
                               ((4, 0), "tap", "down", 2), ((1, 0), "slide", "right", 2), ((3, 2), "sandpit", "left", 1)]:
        assert route(start, [(d, n)]) == AT[place]
        who = nm()
        perp = "up" if d in ("left", "right") else "left"
        wrong = [say([(OPP[d], n)]), say([(d, n + 1)]), say([(d, n - 1)]) if n > 1 else say([(perp, n)])]
        e = ("Go %s. Do not count %s’s own square. Count %s. That is <b>%s %s</b>."
             % (d, who, ", ".join(str(i) for i in range(1, n + 1)), sq(n), d))
        its.append(mcq(fig(map_svg(start, who)) + "Which way does %s go to get to the <b>%s</b>?" % (who, place),
                       say([(d, n)]), wrong, e))
    # two steps
    for start, place, steps in [((0, 1), "sandpit", [("right", 2), ("down", 1)]), ((0, 1), "slide", [("right", 3), ("up", 1)]),
                                ((4, 1), "tree", [("left", 4), ("up", 1)]), ((1, 1), "tap", [("right", 3), ("down", 1)]),
                                ((3, 1), "gate", [("left", 3), ("down", 1)])]:
        assert route(start, steps) == AT[place], (start, place)
        who = nm()
        (d1, n1), (d2, n2) = steps
        wrong = [say([(OPP[d1], n1), (d2, n2)]), say([(d1, n1 + 1), (d2, n2)]), say([(d1, n1), (OPP[d2], n2)])]
        e = "First go <b>%s %s</b>. Then go <b>%s %s</b>. Count moves, not %s’s own square." % (sq(n1), d1, sq(n2), d2, who)
        its.append(mcq(fig(map_svg(start, who)) + "Which way does %s go to get to the <b>%s</b>?" % (who, place),
                       say(steps), wrong, e))
    # where do they get to?
    for start, steps in [((1, 1), [("left", 1), ("up", 1)]), ((2, 1), [("right", 2), ("down", 1)]),
                         ((4, 1), [("up", 1), ("right", 1)]), ((3, 1), [("right", 2)]), ((4, 0), [("left", 1)])]:
        end = route(start, steps)
        place = PLAY[end]
        who = nm()
        cand = []
        alt = [[(OPP[steps[0][0]], steps[0][1])] + steps[1:],
               [(steps[0][0], steps[0][1] + 1)] + steps[1:],
               steps[:-1] + [(steps[-1][0], steps[-1][1] + 1)],
               steps[:-1] + [(OPP[steps[-1][0]], steps[-1][1])]]
        for a in alt:
            p = start
            for d, n in a:
                p = mv(p, d, n)
            if p in PLAY and PLAY[p] != place:
                cand.append(PLAY[p])
        # nearest other places to the right end
        rest = sorted((k for k in PLAY if PLAY[k] != place),
                      key=lambda k: (abs(k[0] - end[0]) + abs(k[1] - end[1]), k))
        cand += [PLAY[k] for k in rest]
        e = "Go %s. %s gets to the <b>%s</b>." % (" then ".join("%s %s" % (sq(n), d) for d, n in steps), who, place)
        its.append(mcq(fig(map_svg(start, who)) + "%s goes <b>%s</b>. Where is %s now?" % (
            who, say(steps), "she" if who in ("Mia", "Ava", "Isla", "Ruby", "Zara") else "he"),
            "the " + place, ["the " + c for c in cand], e))
    # position words on the map
    f0 = fig(map_svg())
    its.append(mcq(f0 + "What is just to the <b>left</b> of the bin?", "the tap", ["the cubby", "the sandpit", "the swings"],
                   "Look at the bin. The square on its left side has the <b>tap</b>. The cubby is above the bin."))
    its.append(mcq(f0 + "What is just <b>above</b> the bin?", "the cubby", ["the tap", "the swings", "the sandpit"],
                   "Look up from the bin. The <b>cubby</b> is in the square above it."))
    its.append(mcq(f0 + "What is in the <b>top right</b> corner?", "the swings", ["the tree", "the bin", "the gate"],
                   "Top is the top row. Right is the side of your right hand. The <b>swings</b> are there. The tree is top left."))
    # how far
    st = (0, 1)
    assert route(st, [("right", 5)]) == AT["cubby"]
    its.append(mcq_num(fig(map_svg(st, "Ava")) + "How many squares does Ava move to the right to get to the cubby?", 5, [6, 4, 3],
                       "Do not count Ava’s own square. Count 1, 2, 3, 4, 5. That is <b>5</b> squares."))
    its.append(mcq_num(fig(map_svg((1, 2), "Leo")) + "How many squares does Leo move to the <b>right</b> to get to the sandpit?",
                       1, [2, 3, 4], "The sandpit is in the very next square. That is <b>1</b> square."))
    assert route((1, 2), [("right", 1)]) == AT["sandpit"]
    assert len(its) == 20, len(its)
    return {"title": "Which way to the sandpit? Directions on a playground map", "items": its}


# ============================================================ set 5: turns and directions at school
TURN4 = ["quarter turn right", "quarter turn left", "half turn", "whole turn"]
YARD = ["oval", "canteen", "library", "gate"]          # top, right, bottom, left
ROOM = ["board", "door", "window", "shelves"]
GIRLS = {"Ava", "Mia", "Isla", "Ruby", "Zara", "Grace", "Mei", "Chloe", "Harper", "Amelia"}


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


def after(face, turn):
    return (face + {"quarter turn right": 1, "quarter turn left": -1, "half turn": 2, "whole turn": 0}[turn]) % 4


def set_school(rnd, pos):
    its = []
    for who, f0, turn in [("Ava", 0, "quarter turn right"), ("Leo", 1, "quarter turn left"),
                          ("Isla", 0, "half turn"), ("Noah", 3, "quarter turn right")]:
        end = after(f0, turn)
        pr = "she" if who in GIRLS else "he"
        wrong_way = after(f0, "quarter turn left" if turn == "quarter turn right" else "quarter turn right")
        cands = [YARD[wrong_way], YARD[(f0 + 2) % 4], YARD[f0], YARD[(f0 + 1) % 4], YARD[(f0 + 3) % 4]]
        if turn == "half turn":
            e = "A half turn makes you face the opposite way. Opposite the %s is the <b>%s</b>." % (YARD[f0], YARD[end])
        else:
            side = turn.split()[-1]
            e = ("Stand like %s and turn to your %s. From the %s, a quarter turn %s faces the <b>%s</b>. "
                 "Turning the other way would face the %s." % (who, side, YARD[f0], side, YARD[end], YARD[wrong_way]))
        its.append(mcq(fig(facing_svg(f0, YARD)) + "%s faces the %s. %s makes a <b>%s</b>. What does %s face now?"
                       % (who, YARD[f0], pr.capitalize(), turn, pr), "the " + YARD[end],
                       ["the " + c for c in cands if c != YARD[end]], e))
    for who, f0, f1 in [("Mia", 0, 1), ("Kai", 0, 3), ("Chloe", 1, 3)]:
        turn = [t for t in TURN4 if after(f0, t) == f1][0]
        pr = "She" if who in GIRLS else "He"
        e = {"quarter turn right": "The %s is on the right side. Turning to face it is a <b>quarter turn right</b>.",
             "quarter turn left": "The %s is on the left side. Turning to face it is a <b>quarter turn left</b>.",
             "half turn": "The %s is the opposite way. Turning to face it is a <b>half turn</b>."}[turn] % YARD[f1]
        its.append(mcq_fixed(fig(facing_svg(f0, YARD)) + "%s faces the %s. %s turns to face the %s. What turn is that?"
                             % (who, YARD[f0], pr, YARD[f1]), TURN4, turn, e))
    its.append(mcq_num("How many quarter turns make a <b>half turn</b>?", 2, [1, 3, 4],
                       "A quarter turn, then another quarter turn, makes a <b>half turn</b>. That is <b>2</b>."))
    its.append(mcq_fixed("Liam makes a quarter turn right. Then he makes another quarter turn right. What is that the same as?",
                         TURN4, "half turn", "2 quarter turns make a <b>half turn</b>. Liam now faces the opposite way."))
    # canteen line
    line = ["Ava", "Leo", "Mia", "Kai", "Ruby"]
    g = fig(queue_svg(line, True))
    its.append(mcq(g + "The children line up at the canteen door. Who is just <b>behind</b> Leo?", "Mia",
                   ["Ava", "Kai", "Ruby"],
                   "Behind Leo means further from the door. That is <b>Mia</b>. Ava is in front of Leo."))
    its.append(mcq(g + "Who is just <b>in front of</b> Kai?", "Mia", ["Ruby", "Leo", "Ava"],
                   "In front of Kai means closer to the door. That is <b>Mia</b>. Ruby is behind Kai."))
    its.append(mcq_num(g + "How many children are in front of Mia?", 2, [3, 1, 4],
                       "Ava and Leo are in front of Mia. That is <b>2</b>. Do not count Mia."))
    # classroom and playground turns
    its.append(mcq(fig(facing_svg(0, ROOM)) + "Oliver faces the board. He makes a <b>half turn</b>. What does he face now?",
                   "the window", ["the door", "the shelves", "the board"],
                   "A half turn makes you face the opposite way. Opposite the board is the <b>window</b>."))
    its.append(mcq(fig(facing_svg(1, ROOM)) + "Grace faces the door. She makes a <b>quarter turn left</b>. What does she face now?",
                   "the board", ["the window", "the shelves", "the door"],
                   "Stand like Grace and turn to your left. From the door, she faces the <b>board</b>. "
                   "A right turn would face the window."))
    its.append(mcq(fig(facing_svg(0, YARD)) + "Ruby faces the oval. She makes a <b>whole turn</b>. What does she face now?",
                   "the oval", ["the library", "the canteen", "the gate"],
                   "A whole turn goes all the way round. Ruby faces the <b>oval</b> again."))
    # sitting in a row
    row = ["Isla", "Jack", "Mei", "Noah", "Zara"]
    r = fig(kids_row_svg(row))
    its.append(mcq(r + "Who sits just to the <b>right</b> of Jack?", "Mei", ["Isla", "Noah", "Zara"],
                   "Find Jack. Look to the right side. <b>Mei</b> is next. Isla is on Jack’s left side."))
    its.append(mcq(r + "Who sits <b>between</b> Mei and Zara?", "Noah", ["Jack", "Isla", "Mei"],
                   "Mei is on one side. Zara is on the other side. <b>Noah</b> is in the middle."))
    its.append(mcq(r + "Where does Isla sit?", "at the left end",
                   ["at the right end", "between Jack and Mei", "next to Zara"],
                   "Isla is the first child on the left side. She sits <b>at the left end</b>."))
    # no picture
    its.append(mcq("Kai takes 3 steps forward. Then he takes 3 steps back. Where is he now?",
                   "where he started", ["3 steps forward", "6 steps forward", "3 steps back"],
                   "3 steps forward and 3 steps back cancel out. Kai is back <b>where he started</b>."))
    its.append(mcq("Zara stands in front of Leo in a line. Where is Leo?", "behind Zara",
                   ["in front of Zara", "above Zara", "under Zara"],
                   "If Zara is in front of Leo, then Leo is <b>behind Zara</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Turns and directions at school", "items": its}


# ============================================================ lesson
def body_html():
    f1 = strip([table_scene("koala", "on"), table_scene("ball", "under"), table_scene("balloon", "above"),
                table_scene("duck", "next to")], ["on", "under", "above", "next to"],
               "a table with a koala on it, a ball under it, a balloon above it and a duck next to it", k=0.62)
    f2 = strip([box_scene("teddy", "behind"), box_scene("ball", "in front of")], ["behind", "in front of"],
               "a teddy behind a box and a ball in front of a box", k=0.8)
    f3 = scene_svg(row_scene(["koala", "ball", "apple", "teddy", "duck"], labels=True),
                   "a row of toys with left and right marked")
    f4 = grid_svg((1, 2), "up", {(3, 2): "apple", (1, 0): "star"})
    f5 = map_svg((0, 1), "Mia")
    tq = [turn_svg(0.25, True), turn_svg(0.25, False), turn_svg(0.5, True)]
    f6 = strip(tq, ["quarter right", "quarter left", "half turn"], "a quarter turn right, a quarter turn left and a half turn", k=0.9)
    return (
        "<h2>Where is it?</h2>"
        "<p>Position words tell us <b>where</b> something is.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption><b>On</b> touches the top. <b>Above</b> is higher, with a gap. <b>Under</b> or <b>below</b> is lower.</figcaption></figure>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption><b>Behind</b>: the box hides part of the teddy. <b>In front of</b>: the ball is closer to us.</figcaption></figure>"
        "<p><b>Between</b> means in the middle of two things.</p>"
        "<h2>Left and right</h2>"
        "<p><b>Left</b> is the side of your left hand. <b>Right</b> is the side of your right hand.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>The koala is at the left end. The ball is 2nd from the left. The duck is at the right end.</figcaption></figure>"
        "<h2>Follow directions</h2>"
        "<p>A robot moves <b>forward</b> the way its arrow points. <b>Turn right</b> or <b>turn left</b> first, then move.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>The robot points up. Go 2 squares forward: the star. Turn right, then go 2 squares forward: the apple.</figcaption></figure>"
        "<p>Count the <b>moves</b>, not the square you start on.</p>"
        "<h2>Which way to the sandpit?</h2>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>Mia goes 2 squares right, then 1 square down. She gets to the sandpit.</figcaption></figure>"
        "<h2>Quarter and half turns</h2>"
        "<p>A <b>quarter turn</b> makes you face the side. A <b>half turn</b> makes you face the opposite way. "
        "A <b>whole turn</b> brings you back.</p>"
        "<figure class='sn-fig'>" + f6 + "</figure>" +
        ex("Example 1", "Ava faces the oval. She makes a half turn. What does she face now?",
           "A half turn makes her face the opposite way. The library is opposite the oval.", "the library") +
        ex("Example 2", "Mia is 2 squares to the left of the slide. Which way does she go?",
           "Count the moves: 1, 2. Do not count her own square.", "2 squares right") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up left and right", "Hold up your hands. Your left hand makes an L shape"],
            ["Counting the start square", "Count the moves: 1, 2, 3 …"],
            ["Moving before turning", "Turn first, then go forward"],
            ["Saying on when it is above", "On touches. Above has a gap"],
            ["Mixing up a quarter turn and a half turn", "Quarter turn: face the side. Half turn: face the opposite way"],
        ])
    )


FAQ = [
    {"q": "What do Year 1 students learn about position and direction in the Australian Curriculum?",
     "a": "In Year 1 (AC9M1SP02) students give and follow directions to move people and objects around a space. They use words like above, below, next to, between, in front of, behind, left, right, forward and turn."},
    {"q": "How can I help my child learn left and right?",
     "a": "Hold up both hands, fingers up and thumbs out. The left hand makes an L shape. Play “touch your left ear” and say left and right on the walk to school."},
    {"q": "What are good direction games for Year 1?",
     "a": "Play “robot”: one child gives directions like “2 steps forward, turn right” and the other follows. A treasure hunt to the sandpit or the canteen works well too."},
    {"q": "Why does my child get one square too many?",
     "a": "Many children count the square they start on. Show them to count each move instead: touch the next square and say 1, then 2, and so on."},
]


def gen():
    rnd = random.Random(1811)
    pos = Pos(rnd)
    sets = [set_position(rnd, pos), set_left_right(rnd, pos), set_robot(rnd, pos), set_map(rnd, pos),
            set_school(rnd, pos)]
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
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "position-and-directions", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Position and Directions: Left, Right, Forward and Turns",
        "seo_title": "Year 1 Position and Directions Worksheets: Left, Right and Following Directions (Free)",
        "short_title": "Position and directions",
        "domain": "Space",
        "standard_code": "AC9M1SP02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Give and follow directions to move people and objects to different locations within a space",
        "meta_desc": "Free Year 1 maths worksheets on position and directions: above, below, next to, between, in front of and behind, left and right, moving a robot forward and turning on a grid, finding the way to the sandpit on a playground map, and quarter and half turns. 100 picture questions with an answer key, following the Australian Curriculum.",
        "key_big": "Turn first, then go forward. Count the moves, not the square you start on.",
        "key_sub": "Left is the side of your left hand and right is the side of your right hand. A quarter turn faces the side; a half turn faces the opposite way.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four pictures labelled A to D|a row of toys|a teddy, a koala|a star, a duck|a cat, a book|grid with|a playground map|children in a line|children sitting)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
