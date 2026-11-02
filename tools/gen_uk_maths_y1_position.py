# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Position and Direction (National Curriculum in England, Year 1: Geometry – position and direction)
  python3 tools/gen_uk_maths_y1_position.py
Position words (on, under, above, below, next to, between, in front of, behind), left and right,
first / second / third / last, whole, half, quarter and three-quarter turns, and moving on a grid.
Every picture is drawn from the data that the answer is worked out from (positions in a row,
cells on a grid, turns as quarter steps), so the picture and the answer always agree.
"Left" and "right" always mean the left and right of the picture as the child looks at it.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
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
        "book": (12, 12, 30)}
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


# ============================================================ set 1: position words
def set_position(rnd, pos):
    its = []
    other = {"on": ["above", "under", "next to"], "under": ["on", "next to", "above"],
             "above": ["on", "under", "next to"], "next to": ["on", "under", "above"]}
    why_t = {
        "on": "The %s is <b>on</b> the table. It touches the top of the table.",
        "under": "The %s is <b>under</b> the table. The table top is over it.",
        "above": "The %s is <b>above</b> the table. It is higher than the table, but it does not touch it.",
        "next to": "The %s is <b>next to</b> the table. It is at the side, close to it.",
    }
    for kind, where in [("ball", "on"), ("cat", "under"), ("balloon", "above"), ("teddy", "next to"),
                        ("duck", "on"), ("car", "under")]:
        e = why_t[where] % kind
        if where == "on":
            e += " Above would mean higher, with a gap."
        if where == "above":
            e += " It is not on the table."
        its.append(mcq(fig(table_svg(kind, where, "a %s %s a table" % (kind, where))) + "Where is the %s?" % kind,
                       where + " the table", [w + " the table" for w in other[where]], e))
    bx = {"in front of": ["behind", "on", "next to"], "behind": ["in front of", "on", "next to"]}
    for kind, where in [("ball", "in front of"), ("teddy", "behind"), ("duck", "in front of"), ("cat", "behind")]:
        sc = box_scene(kind, where)
        if where == "behind":
            e = ("The box hides part of the %s. The %s is further back. It is <b>behind</b> the box." % (kind, kind))
        else:
            e = ("We can see all of the %s. It hides part of the box. It is nearer to us. "
                 "It is <b>in front of</b> the box." % kind)
        y0 = max(0, BXS["btop"] - (SIZE[kind][2] - 10 if where == "behind" else 0) - 8)
        its.append(mcq(fig(scene_svg(sc, "a %s %s a box" % (kind, where), y0)) + "Where is the %s?" % kind,
                       where + " the box", [w + " the box" for w in bx[where]], e))
    # between
    row = ["ball", "cat", "car"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a ball, a cat and a car in a row")) +
                   "What is <b>between</b> the ball and the car?", "the cat", ["the ball", "the car", "the duck"],
                   "Between means in the middle. The <b>cat</b> is in the middle of the ball and the car."))
    row = ["apple", "teddy", "duck", "star"]
    its.append(mcq(fig(scene_svg(row_scene(row), "an apple, a teddy, a duck and a star in a row")) +
                   "What is between the teddy and the star?", "the duck", ["the apple", "the teddy", "the star"],
                   "Find the teddy and the star. The <b>duck</b> is in the middle of them."))
    row = ["book", "duck", "ball"]
    its.append(mcq(fig(scene_svg(row_scene(row), "a book, a duck and a ball in a row")) +
                   "Where is the duck?", "between the book and the ball",
                   ["on the ball", "under the book", "above the ball"],
                   "The duck has the book on one side and the ball on the other. It is <b>between</b> them."))
    # shelves: above and below
    sh1 = [["ball", "star"], ["cat", "book"], ["duck", "apple"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh1), "a bookcase with 3 shelves of toys")) +
                   "What is just <b>above</b> the cat?", "the ball", ["the duck", "the book", "the star"],
                   "Look up from the cat. The shelf above has the <b>ball</b>. The duck is below the cat."))
    sh2 = [["car", "teddy"], ["star", "apple"], ["book", "ball"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh2), "a bookcase with 3 shelves of toys")) +
                   "What is just <b>below</b> the apple?", "the ball", ["the teddy", "the star", "the book"],
                   "Look down from the apple. The shelf below has the <b>ball</b>. The teddy is above the apple."))
    sh3 = [["apple", "duck"], ["teddy", "car"], ["star", "cat"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh3), "a bookcase with 3 shelves of toys")) +
                   "Where is the duck?", "above the car", ["below the car", "next to the car", "below the cat"],
                   "The duck is on the top shelf. The car is on the shelf under it. So the duck is <b>above</b> the car."))
    sh4 = [["book", "cat"], ["ball", "duck"], ["teddy", "star"]]
    its.append(mcq(fig(scene_svg(shelf_scene(sh4), "a bookcase with 3 shelves of toys")) +
                   "Where is the teddy?", "below the ball", ["above the ball", "next to the duck", "above the star"],
                   "The teddy is on the bottom shelf. The ball is on the shelf over it. So the teddy is <b>below</b> the ball."))
    # A-D pictures
    its.append(pick4("Which picture shows the ball <b>under</b> the table?",
                     [table_scene("ball", "under"), table_scene("ball", "on"), table_scene("ball", "next to"),
                      table_scene("apple", "under", COL["green"])],
                     "The ball is under the table top. In one picture the green apple is under the table, not the ball.",
                     pos, "four pictures labelled A to D of a table"))
    its.append(pick4("Which picture shows the cat <b>behind</b> the box?",
                     [box_scene("cat", "behind"), box_scene("cat", "in front of"), box_scene("cat", "on"),
                      box_scene("cat", "next to")],
                     "The box hides part of the cat, so the cat is behind the box.",
                     pos, "four pictures labelled A to D of a box"))
    its.append(pick4("Which picture shows the teddy <b>on</b> the table?",
                     [table_scene("teddy", "on"), table_scene("teddy", "under"), table_scene("teddy", "next to"),
                      table_scene("balloon", "above")],
                     "The teddy touches the top of the table, so it is on the table.",
                     pos, "four pictures labelled A to D of a table"))
    assert len(its) == 20, len(its)
    return {"title": "On, under, next to, behind", "items": its}


# ============================================================ set 2: left and right
ORD = ["first", "second", "third", "fourth", "fifth", "sixth"]
NTH = ["1st", "2nd", "3rd", "4th", "5th", "6th"]


def set_left_right(rnd, pos):
    its = []

    def row_q(kinds, q, ans_i, wrong_i, e, labels):
        lab = "a row of toys: " + ", ".join(kinds)
        assert len(set(kinds)) == len(kinds)
        return mcq(fig(scene_svg(row_scene(kinds, labels=labels), lab)) + q,
                   "the " + kinds[ans_i], ["the " + kinds[j] for j in wrong_i], e)

    # ends of the row
    k = ["duck", "ball", "teddy", "car", "apple"]
    its.append(row_q(k, "Which toy is at the <b>left</b> end?", 0, [4, 1, 3],
                     "Your left hand is on the left side. The <b>duck</b> is at the left end.", True))
    k = ["star", "cat", "book", "ball"]
    its.append(row_q(k, "Which toy is at the <b>right</b> end?", 3, [0, 2, 1],
                     "The right end is on the side of your right hand. It is the <b>ball</b>.", True))
    k = ["teddy", "apple", "duck", "cat", "car"]
    its.append(row_q(k, "Which toy is at the <b>right</b> end?", 4, [0, 3, 1],
                     "Right is the side of your right hand. The <b>car</b> is at the right end. The teddy is at the left end.", False))
    k = ["book", "car", "star", "duck"]
    its.append(row_q(k, "Which toy is at the <b>left</b> end?", 0, [3, 1, 2],
                     "Left is the side of your left hand. The <b>book</b> is at the left end.", False))
    # nth from left / right
    plans = [(["ball", "cat", "apple", "teddy", "duck"], "left", 2, True),
             (["car", "star", "teddy", "book", "ball"], "right", 2, True),
             (["apple", "duck", "book", "cat", "star", "car"], "left", 3, False),
             (["teddy", "ball", "car", "duck", "apple", "cat"], "right", 3, False),
             (["star", "book", "cat", "ball", "duck"], "left", 4, False),
             (["duck", "apple", "teddy", "star", "car", "book"], "right", 2, False)]
    for kinds, side, n, lab in plans:
        L = len(kinds)
        i = n - 1 if side == "left" else L - n
        j_other = L - n if side == "left" else n - 1          # counted from the wrong end
        j_skip = i + (1 if side == "left" else -1)            # counted one too many
        j_short = i - (1 if side == "left" else -1)           # counted one too few
        wr = [j for j in [j_other, j_skip, j_short] + list(range(L)) if 0 <= j < L and j != i]
        e = ("Start at the %s end. Count %s: %s. The %s toy is the <b>%s</b>."
             % (side, "1, 2" + (", 3" if n >= 3 else "") + (", 4" if n >= 4 else ""),
                ", ".join("the " + kinds[(t if side == "left" else L - 1 - t)] for t in range(n)), NTH[n - 1], kinds[i]))
        its.append(row_q(kinds, "Which toy is <b>%s from the %s</b>?" % (NTH[n - 1], side), i, wr, e, lab))
    # just to the left / right of
    plans = [(["cat", "ball", "duck", "apple", "star"], 2, "right"), (["teddy", "star", "car", "book", "ball"], 2, "left"),
             (["apple", "car", "cat", "teddy", "duck"], 3, "left"), (["book", "duck", "star", "teddy", "apple"], 2, "right")]
    for kinds, ref, side in plans:
        i = ref + (1 if side == "right" else -1)
        o = ref - (1 if side == "right" else -1)
        two = ref + (2 if side == "right" else -2)
        cands = [o] + ([two] if 0 <= two < len(kinds) else []) + [t for t in range(len(kinds)) if t not in (i, o, two, ref)]
        e = ("Find the %s. Look to the %s of it. The toy just to the %s is the <b>%s</b>."
             % (kinds[ref], side, side, kinds[i]))
        its.append(row_q(kinds, "What is just to the <b>%s</b> of the %s?" % (side, kinds[ref]), i, cands[:3], e, False))
    # to the left or right?
    for kinds, a, b in [(["cat", "ball"], 0, 1), (["apple", "car", "duck"], 2, 0), (["star", "teddy", "book"], 1, 2)]:
        side = "to the left" if a < b else "to the right"
        e = ("The %s is on the %s side of the %s. So it is <b>%s</b> of the %s."
             % (kinds[a], "left" if a < b else "right", kinds[b], side, kinds[b]))
        its.append(mcq(fig(scene_svg(row_scene(kinds), "a row of toys: " + ", ".join(kinds))) +
                       "Where is the %s?" % kinds[a], side + " of the " + kinds[b],
                       [("to the right" if a < b else "to the left") + " of the " + kinds[b],
                        "above the " + kinds[b], "under the " + kinds[b]], e))
    # A-D: left of
    def lr(a, b):
        return row_scene([a, b], step=62)
    its.append(pick4("Which picture shows the cat to the <b>left</b> of the ball?",
                     [lr("cat", "ball"), lr("ball", "cat"), lr("duck", "ball"), lr("ball", "duck")],
                     "The cat is on the left side, and the ball is on the right side.",
                     pos, "four pictures labelled A to D of two toys"))
    its.append(pick4("Which picture shows the car to the <b>right</b> of the apple?",
                     [lr("apple", "car"), lr("car", "apple"), lr("teddy", "car"), lr("car", "teddy")],
                     "The apple is on the left side and the car is on the right side.",
                     pos, "four pictures labelled A to D of two toys"))
    # 1st from the left is ... from the right
    k = ["ball", "teddy", "car", "star"]
    its.append(mcq(fig(scene_svg(row_scene(k, labels=True), "a row of toys: " + ", ".join(k))) +
                   "The ball is 1st from the left. What is it from the right?", "4th", ["1st", "3rd", "5th"],
                   "Start at the right end: star 1st, car 2nd, teddy 3rd, ball <b>4th</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Left and right", "items": its}


# ============================================================ set 3: first, second, third ... last
def race_svg(colours, flag_right=True):
    """Cars in a race. colours[0] is nearest the finish flag (first)."""
    n = len(colours)
    step, W = 56, 0
    W = 50 + n * step + 10
    H = 64
    s = ["<rect x='0' y='14' width='%d' height='44' fill='%s'/>" % (W, FLOOR)]
    fx = W - 26 if flag_right else 26
    # finish line and chequered flag
    s.append("<line x1='%.1f' y1='14' x2='%.1f' y2='58' stroke='%s' stroke-width='3' stroke-dasharray='4 4'/>" % (fx, fx, INK))
    px = fx + 8 if flag_right else fx - 8
    s.append("<line x1='%.1f' y1='4' x2='%.1f' y2='40' stroke='%s' stroke-width='2.5'/>" % (px, px, INK))
    fw = 14
    x0 = px if flag_right else px - fw
    for r in range(2):
        for c in range(3):
            s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='5' fill='%s' stroke='%s' stroke-width='0.6'/>"
                     % (x0 + c * fw / 3, 4 + r * 5, fw / 3, INK if (r + c) % 2 == 0 else "#fff", INK))
    for i, c in enumerate(colours):
        d = 50 + i * step
        x = fx - d if flag_right else fx + d
        s.append(icon("car", x, 52, COL[c], flip=not flag_right))
    lab = "a race of %d cars to a finish flag on the %s" % (n, "right" if flag_right else "left")
    return svg_wrap(W, H, "".join(s), lab)


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


def set_order(rnd, pos):
    its = []

    def car(c):
        return "the %s car" % c

    r1 = ["blue", "red", "green", "yellow", "purple"]
    f1 = fig(race_svg(r1, True))
    its.append(mcq(f1 + "The cars race to the flag. Which car is <b>first</b>?", car("blue"),
                   [car("purple"), car("red"), car("yellow")],
                   "First is the car <b>nearest the flag</b>. That is the blue car. Do not start counting at the wrong end."))
    its.append(mcq(f1 + "Which car is <b>second</b>?", car("red"), [car("yellow"), car("green"), car("blue")],
                   "Start at the flag. Blue is first, red is <b>second</b>."))
    its.append(mcq(f1 + "Which car is <b>last</b>?", car("purple"), [car("blue"), car("yellow"), car("green")],
                   "Last is the car furthest from the flag. It is the <b>purple</b> car."))
    its.append(mcq(f1 + "What position is the green car?", "third", ["second", "fourth", "fifth"],
                   "Count from the flag: blue first, red second, green <b>third</b>."))
    r2 = ["orange", "green", "red", "blue"]
    f2 = fig(race_svg(r2, False))
    its.append(mcq(f2 + "The flag is on the left. Which car is <b>first</b>?", car("orange"),
                   [car("blue"), car("green"), car("red")],
                   "The cars race to the left. The orange car is <b>nearest the flag</b>, so it is first."))
    its.append(mcq(f2 + "What position is the blue car?", "fourth", ["first", "third", "second"],
                   "Count from the flag: orange, green, red, blue. Blue is <b>fourth</b>. It is also last."))
    its.append(mcq(f2 + "Which car is <b>second</b>?", car("green"), [car("red"), car("orange"), car("blue")],
                   "Count from the flag on the left: orange first, green <b>second</b>."))
    its.append(mcq(f1 + "Which car is just <b>behind</b> the red car?", car("green"),
                   [car("blue"), car("yellow"), car("purple")],
                   "Behind means further from the flag. The car just behind red is <b>green</b>. Blue is in front of red."))
    r3 = ["yellow", "purple", "blue", "green", "red"]
    f3 = fig(race_svg(r3, True))
    its.append(mcq(f3 + "Which car is just <b>in front of</b> the blue car?", car("purple"),
                   [car("green"), car("yellow"), car("red")],
                   "In front means nearer the flag. The car just in front of blue is <b>purple</b>."))
    its.append(mcq(f3 + "Which car is <b>fourth</b>?", car("green"), [car("purple"), car("blue"), car("red")],
                   "Count from the flag: yellow 1st, purple 2nd, blue 3rd, green <b>4th</b>."))
    q1 = ["Ava", "Leo", "Zara", "Kai", "Ruby"]
    g1 = fig(queue_svg(q1, True))
    its.append(mcq(g1 + "The children wait at the door. Who is <b>first</b> in the line?", "Ava",
                   ["Ruby", "Leo", "Kai"],
                   "First is <b>nearest the door</b>. That is Ava. Ruby is last."))
    its.append(mcq(g1 + "Who is <b>third</b> in the line?", "Zara", ["Kai", "Leo", "Ruby"],
                   "Count from the door: Ava, Leo, <b>Zara</b>."))
    its.append(mcq(g1 + "What position is Kai?", "fourth", ["second", "third", "fifth"],
                   "Count from the door: Ava 1st, Leo 2nd, Zara 3rd, Kai <b>4th</b>."))
    its.append(mcq_num(g1 + "How many children are in front of Zara?", 2, [3, 1, 4],
                       "Ava and Leo are in front of Zara. That is <b>2</b>. Do not count Zara herself."))
    q2 = ["Noah", "Isla", "Jack", "Maya", "Evie"]
    g2 = fig(queue_svg(q2, False))
    its.append(mcq(g2 + "The door is on the right. Who is <b>last</b> in the line?", "Evie",
                   ["Noah", "Maya", "Jack"],
                   "First is nearest the door: Noah. The last one is furthest from the door: <b>Evie</b>."))
    its.append(mcq(g2 + "Who is just <b>behind</b> Isla?", "Jack", ["Noah", "Maya", "Evie"],
                   "Behind Isla means further from the door. That is <b>Jack</b>. Noah is in front of Isla."))
    its.append(mcq("Freya came second in a race. Jack was just in front of her. What position was Jack?",
                   "first", ["third", "second", "last"],
                   "Just in front of second is <b>first</b>."))
    its.append(mcq("Maya came third in a race. Alfie came just after her. What position was Alfie?",
                   "fourth", ["second", "third", "first"],
                   "Just after third comes <b>fourth</b>."))
    its.append(mcq("There are 4 children in a line. Poppy is first. Charlie is last. What position is Charlie?",
                   "fourth", ["first", "third", "fifth"],
                   "There are 4 children, so last is <b>fourth</b>."))
    its.append(mcq("Which word comes just after second?", "third", ["first", "fourth", "fifth"],
                   "first, second, <b>third</b>, fourth, fifth."))
    assert len(its) == 20, len(its)
    return {"title": "First, second, third and last", "items": its}


# ============================================================ turns
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
    return svg_wrap(W, H, "".join(s), "a child in the middle facing the %s; tree at the top, house on the right, pond at the bottom, swings on the left" % names[face])


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


def set_turns(rnd, pos):
    its = []
    for frac, cw in [(0.25, True), (0.5, True), (0.75, True), (1.0, True), (0.25, False), (0.5, False)]:
        body, W, H = turn_svg(frac, cw)
        name = TURNS[int(frac * 4) - 1]
        why = {"quarter turn": "The line turns to the side, like a square corner. That is a <b>quarter turn</b>.",
               "half turn": "The line ends pointing the opposite way. That is a <b>half turn</b>, not a quarter turn.",
               "three-quarter turn": "The arrow goes past the half turn and stops at the side. That is a <b>three-quarter turn</b>: 3 quarter turns.",
               "whole turn": "The arrow goes all the way round, back to the start. That is a <b>whole turn</b>."}[name]
        its.append(mcq_fixed(fig(svg_wrap(W, H, body, "a turn from a dashed start line, %s" % ("clockwise" if cw else "anticlockwise"))) +
                             "The arrow shows a turn. What turn is it?", TURNS, name, why))
    # facing questions
    plan = [(0, "half turn", None), (0, "quarter turn", True), (1, "quarter turn", True), (0, "three-quarter turn", True),
            (2, "whole turn", None), (0, "quarter turn", False), (3, "half turn", None)]
    girls = ["Ava", "Isla", "Lily", "Grace"]
    boys = ["Leo", "Noah", "George"]
    for i, (f0, turn, cw) in enumerate(plan):
        k = QT[turn]
        end = (f0 + (k if cw is not False else -k)) % 4
        nm = (girls + boys)[i]
        pr = "She" if nm in girls else "He"
        how = "" if cw is None else (" clockwise" if cw else " anticlockwise")
        q = "%s faces the %s. %s makes a <b>%s%s</b>. What does %s face now?" % (
            nm, PLACES[f0], pr, turn, how, pr.lower())
        steps = [PLACES[(f0 + (j if cw is not False else -j)) % 4] for j in range(1, k + 1)]
        if turn == "whole turn":
            e = "A whole turn goes all the way round. %s faces the <b>%s</b> again." % (nm, PLACES[end])
        elif turn == "half turn":
            e = "A half turn makes you face the opposite way. %s now faces the <b>%s</b>." % (nm, PLACES[end])
        elif k == 1:
            e = "%s A quarter turn from the %s makes %s face the <b>%s</b>." % (
                "Clockwise is the way the hands of a clock go." if cw else "Anticlockwise is the other way to the hands of a clock.",
                PLACES[f0], "her" if pr == "She" else "him", PLACES[end])
        else:
            e = "Turn %s one quarter at a time: %s. %s faces the <b>%s</b>." % (
                "clockwise, like the hands of a clock," if cw else "anticlockwise, the other way to a clock,",
                ", ".join(steps), nm, PLACES[end])
        wrong = [PLACES[(f0 + 2) % 4], PLACES[(f0 - k) % 4] if cw is not None else PLACES[(f0 + 1) % 4],
                 PLACES[f0], PLACES[(f0 + 1) % 4], PLACES[(f0 + 3) % 4]]
        its.append(mcq(fig(facing_svg(f0)) + q, "the " + PLACES[end], ["the " + w for w in wrong], e))
    # before and after arrows
    for d1, turn, cw in [(2, "half turn", None), (1, "quarter turn", True), (3, "three-quarter turn", True)]:
        q = "The arrow turns%s. What turn did it make?" % (" clockwise" if cw else "")
        e = {"half turn": "Up to down is the opposite way. That is a <b>half turn</b>.",
             "quarter turn": "Clockwise from up, one quarter turn points right. That is a <b>quarter turn</b>.",
             "three-quarter turn": "Clockwise from up: right, down, left. That is 3 quarter turns: a <b>three-quarter turn</b>."}[turn]
        its.append(mcq_fixed(fig(before_after_svg(0, d1)) + q, TURNS, turn, e))
    its.append(mcq_num("How many quarter turns make a <b>half turn</b>?", 2, [1, 3, 4],
                       "2 quarter turns make a half turn."))
    its.append(mcq_num("How many quarter turns make a <b>whole turn</b>?", 4, [2, 3, 1],
                       "4 quarter turns go all the way round. They make a whole turn."))
    its.append(mcq_fixed("Which turn makes you face the <b>same way</b> again?", TURNS, "whole turn",
                         "A <b>whole turn</b> goes all the way round. You end facing the same way."))
    its.append(mcq_fixed("Which turn makes you face the <b>opposite way</b>?", TURNS, "half turn",
                         "A <b>half turn</b> makes you face the opposite way, like turning round to look behind you."))
    assert len(its) == 20, len(its)
    return {"title": "Whole, half, quarter and three-quarter turns", "items": its}


# ============================================================ set 5: moving on a grid, real life
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


def land_q(start, d, n, kinds, forwards=False):
    """kinds: answer, start-square mistake (n-1), one too far (n+1), wrong way (opposite)."""
    def ok(c):
        return 0 <= c[0] < GC and 0 <= c[1] < GR and c != start

    cells = [mv(start, d, n), mv(start, d, n - 1), mv(start, d, n + 1)]
    assert all(ok(c) for c in cells), (start, d, n)
    perp = ["up", "down"] if d in ("left", "right") else ["left", "right"]
    for c in [mv(start, OPP[d], n), mv(start, perp[0], n), mv(start, perp[1], n),
              mv(start, perp[0], 1), mv(start, perp[1], 1)]:
        if ok(c) and c not in cells:
            cells.append(c)
            break
    assert len(cells) == 4, (start, d, n)
    items = {}
    for cell, k in zip(cells, kinds):
        items[cell] = k
    assert len(items) == 4
    face = d
    move = ("%d squares forwards" % n) if forwards else ("%d squares %s" % (n, d if d in ("up", "down") else "to the " + d))
    q = fig(grid_svg(start, face, items)) + "The robot moves <b>%s</b>. What does it land on?" % move
    if forwards:
        q = q.replace("The robot moves", "The robot faces the way of the red arrow. It moves")
    e = ("Do not count the square the robot is on. Count each move: %s. It lands on the <b>%s</b>."
         % (", ".join(str(i) for i in range(1, n + 1)), kinds[0]))
    return mcq(q, "the " + kinds[0], ["the " + k for k in kinds[1:]], e)


def set_moving(rnd, pos):
    its = []
    its.append(land_q((1, 1), "right", 3, ["apple", "star", "duck", "ball"]))
    its.append(land_q((5, 2), "left", 2, ["ball", "cat", "apple", "teddy"]))
    its.append(land_q((2, 3), "up", 2, ["star", "teddy", "apple", "duck"]))
    its.append(land_q((4, 0), "down", 2, ["duck", "apple", "cat", "star"]))
    its.append(land_q((0, 2), "right", 4, ["teddy", "ball", "star", "cat"]))
    its.append(land_q((3, 1), "right", 2, ["cat", "duck", "ball", "apple"], forwards=True))
    its.append(land_q((6, 0), "left", 3, ["ball", "teddy", "cat", "duck"], forwards=True))
    its.append(land_q((1, 0), "down", 2, ["apple", "duck", "teddy", "star"], forwards=True))
    # how many squares
    for start, d, n, k, wr in [((1, 2), "right", 4, "apple", [5, 3, 2]), ((5, 1), "left", 3, "star", [4, 2, 5]),
                               ((3, 3), "up", 3, "duck", [4, 2, 1])]:
        items = {mv(start, d, n): k}
        word = d if d in ("up", "down") else "to the " + d
        its.append(mcq_num(fig(grid_svg(start, d, items)) +
                           "How many squares must the robot move %s to reach the %s?" % (word, k), n, wr,
                           "Count the moves, not the square the robot starts on. It moves <b>%d</b> squares." % n))
    # two steps
    st = (1, 1)
    items = {(3, 2): "cat", (3, 0): "apple", (2, 2): "ball", (2, 1): "teddy"}
    assert mv(mv(st, "right", 2), "down", 1) == (3, 2)
    its.append(mcq(fig(grid_svg(st, "right", items)) +
                   "The robot moves 2 squares to the right. Then it moves 1 square down. What does it land on?",
                   "the cat", ["the apple", "the ball", "the teddy"],
                   "2 to the right, then 1 down. It lands on the <b>cat</b>. Up would be the apple."))
    # turn, then move
    st = (3, 2)
    items = {(5, 2): "star", (1, 2): "duck", (3, 0): "ball", (4, 2): "apple"}
    assert mv(st, "right", 2) == (5, 2)
    its.append(mcq(fig(grid_svg(st, "up", items)) +
                   "The robot faces up. It makes a <b>quarter turn clockwise</b>. Then it moves 2 squares forwards. "
                   "What does it land on?", "the star", ["the duck", "the ball", "the apple"],
                   "A quarter turn clockwise from up makes it face right. 2 squares to the right is the <b>star</b>."))
    # real life
    its.append(mcq("Leo sits on a roundabout. It makes a <b>whole turn</b>. Which way does Leo face now?",
                   "the same way", ["the opposite way", "to his left", "to his right"],
                   "A whole turn goes all the way round. Leo faces <b>the same way</b> as at the start."))
    its.append(mcq_num("Isla is <b>third</b> in the lunch queue. How many children are in front of her?", 2, [3, 1, 4],
                       "First and second are in front of her. That is <b>2</b> children. Do not count Isla."))
    its.append(mcq_fixed("Noah faces the board. He turns round to face the back of the classroom. What turn did he make?",
                         TURNS, "half turn",
                         "Facing the opposite way is a <b>half turn</b>."))
    its.append(mcq_fixed("Grace makes a quarter turn. Then she makes another quarter turn. How far has she turned?",
                         TURNS, "half turn",
                         "2 quarter turns make a <b>half turn</b>."))
    its.append(mcq("Kai walks 3 steps forwards. Then he walks 3 steps backwards. Where is he now?",
                   "where he started", ["3 steps forwards", "6 steps forwards", "3 steps backwards"],
                   "3 steps forwards and 3 steps back cancel out. He is back <b>where he started</b>."))
    its.append(mcq("Ruby faces the door. She makes a <b>whole turn</b>. What does she face now?",
                   "the door", ["the window behind her", "the wall on her left", "the wall on her right"],
                   "A whole turn takes you all the way round. Ruby faces <b>the door</b> again."))
    its.append(mcq("The shop is to the left of the house. Which side of the shop is the house?",
                   "to the right", ["to the left", "above it", "under it"],
                   "If the shop is on the left of the house, the house is <b>to the right</b> of the shop."))
    assert len(its) == 20, len(its)
    return {"title": "Moving and turning in real life", "items": its}


# ============================================================ lesson
def strip(scenes, caps, label, k=0.8, fs=15):
    cw = max(sc[1] for sc in scenes) * k + 12
    ch = max(sc[2] for sc in scenes) * k
    s = []
    for i, ((body, w, h), cap) in enumerate(zip(scenes, caps)):
        x0 = i * cw
        s.append("<g transform='translate(%.1f %.1f) scale(%.2f)'>%s</g>" % (x0 + (cw - w * k) / 2, ch - h * k, k, body))
        s.append(text(x0 + cw / 2, ch + 20, cap, fs))
    return svg_wrap(cw * len(scenes), ch + 27, "".join(s), label)


def body_html():
    f1 = strip([table_scene("ball", "on"), table_scene("cat", "under"), table_scene("balloon", "above"),
                table_scene("teddy", "next to")], ["on", "under", "above", "next to"],
               "a table with a ball on it, a cat under it, a balloon above it and a teddy next to it", k=0.62)
    f2 = strip([box_scene("teddy", "behind"), box_scene("ball", "in front of")], ["behind", "in front of"],
               "a teddy behind a box and a ball in front of a box", k=0.8)
    f3 = scene_svg(row_scene(["ball", "cat", "apple", "teddy", "duck"], labels=True),
                   "a row of toys with left and right marked")
    f4 = race_svg(["blue", "red", "green", "yellow"], True)
    tq = [turn_svg(f) for f in (0.25, 0.5, 0.75, 1.0)]
    f5 = strip(tq, ["quarter", "half", "three-quarter", "whole"], "quarter, half, three-quarter and whole turns", k=0.9)
    f6 = grid_svg((1, 1), "right", {(4, 1): "apple"})
    return (
        "<h2>Where is it?</h2>"
        "<p>Position words tell us <b>where</b> something is.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption><b>On</b> touches the top. <b>Above</b> is higher, with a gap. <b>Under</b> (or <b>below</b>) is lower.</figcaption></figure>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption><b>Behind</b>: the box hides part of the teddy. <b>In front of</b>: the ball hides part of the box.</figcaption></figure>"
        "<p><b>Between</b> means in the middle of two things.</p>"
        "<h2>Left and right</h2>"
        "<p>Look at the picture. <b>Left</b> is the side of your left hand. <b>Right</b> is the side of your right hand.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>The ball is at the left end. The cat is 2nd from the left. The duck is at the right end.</figcaption></figure>"
        "<h2>First, second, third</h2>"
        "<p>In a race, the one nearest the finish is <b>first</b>. Then <b>second</b>, <b>third</b>, <b>fourth</b>. The one at the back is <b>last</b>.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>Blue is first, red is second, green is third, yellow is last.</figcaption></figure>"
        "<h2>Turns</h2>"
        "<p>A <b>whole turn</b> goes all the way round. A <b>half turn</b> makes you face the opposite way. "
        "A <b>quarter turn</b> is like a square corner. A <b>three-quarter turn</b> is 3 quarter turns.</p>"
        "<figure class='sn-fig'>" + f5 + "</figure>" +
        table(["Turn", "Quarter turns", "You face"], [
            ["quarter turn", "1", "to the side"],
            ["half turn", "2", "the opposite way"],
            ["three-quarter turn", "3", "the other side"],
            ["whole turn", "4", "the same way again"],
        ]) +
        "<p><b>Clockwise</b> is the way the hands of a clock turn. <b>Anticlockwise</b> is the other way.</p>"
        "<h2>Moving on a grid</h2>"
        "<p>Count the <b>moves</b>, not the square you start on.</p>"
        "<figure class='sn-fig'>" + f6 +
        "<figcaption>The robot moves 3 squares to the right to reach the apple.</figcaption></figure>" +
        ex("Example 1", "Ava faces the tree. She makes a half turn. What does she face now?",
           "A half turn makes you face the opposite way. The pond is opposite the tree.", "the pond") +
        ex("Example 2", "5 children are in a line. Leo is third. How many children are in front of him?",
           "First and second are in front of Leo. Do not count Leo.", "2 children") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up left and right", "Hold up your hands. Your left hand makes an L shape"],
            ["Saying on when it is above", "On touches. Above has a gap"],
            ["Mixing up a half turn and a quarter turn", "Half turn: face the opposite way. Quarter turn: face the side"],
            ["Counting the start square", "Count the moves: 1, 2, 3 ..."],
            ["Counting first from the wrong end", "First is nearest the finish or the front of the line"],
        ])
    )


FAQ = [
    {"q": "What do Year 1 children learn about position and direction?",
     "a": "They use words like on, under, above, below, next to, between, in front of and behind, and left and right. They also learn whole, half, quarter and three-quarter turns."},
    {"q": "How can I help my child learn left and right?",
     "a": "Hold up both hands with the fingers up and thumbs out. The left hand makes an L shape. Play games like “touch your left ear” and say left and right on walks."},
    {"q": "What is a quarter turn for Year 1?",
     "a": "A quarter turn is a turn to the side, like a square corner. Two quarter turns make a half turn, and four make a whole turn."},
    {"q": "What is the difference between a half turn and a whole turn?",
     "a": "After a half turn you face the opposite way. After a whole turn you go all the way round and face the same way as at the start."},
]


# ============================================================ assemble
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


def gen():
    rnd = random.Random(1110)
    pos = Pos(rnd)
    sets = [set_position(rnd, pos), set_left_right(rnd, pos), set_order(rnd, pos), set_turns(rnd, pos),
            set_moving(rnd, pos)]
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
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "position-and-direction", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 1 Position and Direction",
        "seo_title": "Year 1 Position and Direction Worksheets: Left and Right, Turns and Position Words (Free, with Answers)",
        "short_title": "Position and direction",
        "domain": "Geometry – position and direction",
        "standard_code": "Year 1: Geometry – position and direction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Describe position, direction and movement, including whole, half, quarter and three-quarter turns.",
        "meta_desc": "Free Year 1 position and direction worksheets for the National Curriculum: on, under, above, next to, behind and between, left and right, first, second and third, whole, half, quarter and three-quarter turns, and moving on a grid. 100 picture questions with an answer key.",
        "key_big": "Position words tell us where something is. A half turn makes you face the opposite way; a whole turn brings you back.",
        "key_sub": "Left and right are the sides of your left and right hands. First is nearest the finish. On a grid, count the moves, not the square you start on.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four pictures labelled A to D|a row of toys|a race of|children in a line|grid with|a child in the middle|a ball, a cat|an apple, a teddy|a book, a duck)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
