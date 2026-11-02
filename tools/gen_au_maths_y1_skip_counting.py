# -*- coding: utf-8 -*-
"""
AU Year 1 Maths (Australian Curriculum v9.0): skip counting by 2s, 5s and 10s.
AC9M1A01 (skip-counting patterns) and AC9M1N03 (count collections in equal groups).
  python3 tools/gen_au_maths_y1_skip_counting.py
Year 1 has no × or ÷ signs: we say "groups of", "pairs", "bundles of 10".
Numbers stay within 120. Australian coins only (5c, 10c here; no 1c or 2c coins).
Every answer, every wrong answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
SKIN = "#cfe6d6"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
SILVER = ("#dfe3e7", "#7a828a")
COIN = {5: (19, 14), 10: (23, 15)}      # radius, font size (the 10c coin is bigger than the 5c coin)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\D*$", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def abcd_item(prompt, right, wrong, e):
    """A-D picture question. The picture is built in balance() so the right letter lands on its target."""
    assert len(wrong) == 3 and right not in wrong and len({repr(w) for w in wrong}) == 3
    return {"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e, "_abcd": (prompt, right, wrong)}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def lst(xs):
    return ", ".join(str(x) for x in xs)


def steps(step, n, start=None):
    """Skip count: steps(2, 4) -> [2, 4, 6, 8]."""
    a = step if start is None else start
    return [a + step * k for k in range(n)]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, large=False):
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", w, h, w, h, label, FONT, body))


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


def rows_of(n, per):
    """Split n things into rows of at most `per`, as even as possible (7 -> 4 + 3)."""
    r = (n + per - 1) // per
    base, extra = divmod(n, r)
    return [base + (1 if i < extra else 0) for i in range(r)]


def grid(n, per, w, h, gx, gy, m, draw):
    """Lay out n tiles of w x h in rows (at most `per` a row). draw(i, x, y) -> svg. Returns body, W, H."""
    rows = rows_of(n, per)
    W = 2 * m + max(rows) * w + (max(rows) - 1) * gx
    H = 2 * m + len(rows) * h + (len(rows) - 1) * gy
    s, i = [], 0
    for r, k in enumerate(rows):
        for c in range(k):
            s.append(draw(i, m + c * (w + gx), m + r * (h + gy)))
            i += 1
    assert i == n
    return "".join(s), W, H


# ------------------------------------------------------------ small objects
def counter(kind, cx, cy, r=8):
    if kind == "counter":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, GREEN)
    if kind == "lolly":
        return ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                % (cx - r * 0.4, cy, cx - r * 1.05, cy - r * 0.5, cx - r * 1.05, cy + r * 0.5, ORANGE,
                   cx + r * 0.4, cy, cx + r * 1.05, cy - r * 0.5, cx + r * 1.05, cy + r * 0.5, ORANGE,
                   cx, cy, r * 0.62, ORANGE))
    if kind == "apple":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                % (cx, cy + 1, r * 0.85, RED, cx, cy - r * 0.6, cx + 2, cy - r * 1.1, GREEN))
    if kind == "shell":
        # a scallop shell: a fan with ridges and a small hinge at the bottom
        bx, by = cx, cy + r * 0.85
        R = r * 1.15
        s = ["<path d='M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z' fill='#f4d7b5' stroke='#a0623a' "
             "stroke-width='1.2' stroke-linejoin='round'/>"
             % (bx, by, bx - R * 0.87, by - R * 0.5, R, R, bx + R * 0.87, by - R * 0.5)]
        for a in (-40, -15, 15, 40):
            t = math.radians(a - 90)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#a0623a' stroke-width='0.9'/>"
                     % (bx, by, bx + R * 0.95 * math.cos(t), by + R * 0.95 * math.sin(t)))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#e8bf8f' stroke='#a0623a' stroke-width='1'/>"
                 % (bx - r * 0.35, by - r * 0.1, r * 0.7, r * 0.3))
        return "".join(s)
    raise ValueError(kind)


NAMES = {"counter": "counters", "lolly": "lollies", "apple": "apples", "shell": "shells"}


def sock(x, y):
    return ("<path d='M %d %d H %d V %d H %d Q %d %d %d %d Q %d %d %d %d H %d Q %d %d %d %d Z' "
            "fill='#f3c6c6' stroke='%s' stroke-width='1.5'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
            % (x, y, x + 12, y + 20, x + 21, x + 26, y + 20, x + 26, y + 25, x + 26, y + 30, x + 21, y + 30,
               x + 4, x, y + 30, x, y + 26, RED, x, y + 5, x + 12, y + 5, RED))


def shoe(x, y):
    return ("<path d='M %d %d Q %d %d %d %d H %d Q %d %d %d %d Q %d %d %d %d V %d H %d Z' "
            "fill='#c9d8ea' stroke='%s' stroke-width='1.5'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
            % (x, y + 10, x, y, x + 8, y, x + 13, x + 17, y + 8, x + 27, y + 10, x + 32, y + 11, x + 32, y + 17,
               y + 22, x, BLUE, x, y + 19, x + 32, y + 19, BLUE))


def pairs_svg(n, kind):
    """n pairs of socks or shoes, each pair in a dashed loop."""
    one, w, h = {"socks": (sock, 26, 30), "shoes": (shoe, 32, 22)}[kind]
    pw, ph = 2 * w + 4 + 12, h + 12

    def draw(i, x, y):
        return ("<rect x='%d' y='%d' width='%d' height='%d' rx='9' fill='none' stroke='%s' stroke-width='1.5' "
                "stroke-dasharray='4 3'/>" % (x, y, pw, ph, GREY) + one(x + 6, y + 6) + one(x + 6 + w + 4, y + 6))
    body, W, H = grid(n, 4, pw, ph, 8, 8, 4, draw)
    return svg_wrap(W, H, body, "%d pairs of %s" % (n, kind))


def face(x, y):
    cx, cy = x + 20, y + 20
    return ("<circle cx='%d' cy='%d' r='19' fill='#f6dcc0' stroke='%s' stroke-width='1.5'/>"
            "<circle cx='%d' cy='%d' r='3.2' fill='%s'/><circle cx='%d' cy='%d' r='3.2' fill='%s'/>"
            "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='%s' stroke-width='2'/>"
            % (cx, cy, "#9a6a3a", cx - 7, cy - 4, INK, cx + 7, cy - 4, INK, cx - 7, cy + 6, cx, cy + 12, cx + 7, cy + 6, INK))


def faces_svg(n):
    body, W, H = grid(n, 6, 40, 40, 8, 8, 4, lambda i, x, y: face(x, y))
    return svg_wrap(W, H, body, "%d children" % n)


def bird(x, y):
    """A kookaburra (side view) with 2 legs, in a 48 x 48 box."""
    return ("<ellipse cx='%d' cy='%d' rx='15' ry='11' fill='#b98a5a' stroke='#6b4a2a' stroke-width='1.5'/>"
            "<path d='M %d %d L %d %d L %d %d Z' fill='%s'/>"
            "<circle cx='%d' cy='%d' r='9' fill='#f1ece2' stroke='#6b4a2a' stroke-width='1.5'/>"
            "<path d='M %d %d L %d %d L %d %d Z' fill='#4a4a4a'/>"
            "<circle cx='%d' cy='%d' r='1.8' fill='%s'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
            % (x + 20, y + 26, x + 5, y + 24, x - 0, y + 34, x + 8, y + 30, BLUE,
               x + 31, y + 15, x + 37, y + 12, x + 47, y + 16, x + 37, y + 18,
               x + 32, y + 13, INK,
               x + 16, y + 36, x + 14, y + 46, INK, x + 24, y + 36, x + 26, y + 46, INK))


def birds_svg(n):
    body, W, H = grid(n, 5, 48, 48, 8, 6, 4, lambda i, x, y: bird(x, y))
    return svg_wrap(W, H, body, "%d kookaburras" % n)


def coin(v, cx, cy):
    r, fs = COIN[v]
    fill, edge = SILVER
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>"
            % (cx, cy, r, fill, edge, cx, cy, r - 4, edge) + text(cx, cy + fs * 0.36, "%dc" % v, fs))


def coins_svg(v, n):
    d = 2 * COIN[v][0]
    body, W, H = grid(n, 5, d, d, 6, 6, 4, lambda i, x, y: coin(v, x + d / 2, y + d / 2))
    return svg_wrap(W, H, body, "%d coins of %dc" % (n, v))


def hand(x, y):
    """One hand, 4 fingers and a thumb, in a 40 x 58 box."""
    s = []
    for k, top in enumerate([10, 3, 5, 12]):
        s.append("<rect x='%.1f' y='%.1f' width='6.5' height='%d' rx='3.2' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x + 11 + k * 7, y + top, 36 - top, SKIN, GREEN))
    s.append("<rect x='%.1f' y='%.1f' width='7' height='20' rx='3.5' fill='%s' stroke='%s' stroke-width='1.5' "
             "transform='rotate(-38 %.1f %.1f)'/>" % (x + 6, y + 22, SKIN, GREEN, x + 9.5, y + 42))
    s.append("<rect x='%.1f' y='%.1f' width='30' height='26' rx='8' fill='%s' stroke='%s' stroke-width='1.5'/>"
             % (x + 9, y + 30, SKIN, GREEN))
    return "".join(s)


def hands_svg(n):
    body, W, H = grid(n, 5, 40, 58, 10, 8, 6, lambda i, x, y: hand(x, y))
    return svg_wrap(W, H, body, "%d hands" % n)


def hand_pairs_svg(n):
    """n children, each holding up 2 hands (10 fingers), each pair in a dashed loop."""
    pw, ph = 2 * 40 + 4 + 12, 58 + 12

    def draw(i, x, y):
        return ("<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='none' stroke='%s' stroke-width='1.5' "
                "stroke-dasharray='4 3'/>" % (x, y, pw, ph, GREY) + hand(x + 6, y + 6) + hand(x + 50, y + 6))
    body, W, H = grid(n, 3, pw, ph, 10, 8, 4, draw)
    return svg_wrap(W, H, body, "%d pairs of hands" % n)


def starfish(x, y):
    cx, cy = x + 20, y + 21
    pts = []
    for k in range(10):
        rr = 19 if k % 2 == 0 else 7.5
        a = -math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return ("<polygon points='%s' fill='#f2a65a' stroke='#a3561c' stroke-width='1.5' stroke-linejoin='round'/>"
            "<circle cx='%d' cy='%d' r='2.5' fill='#a3561c'/>" % (" ".join(pts), cx, cy))


def starfish_svg(n):
    body, W, H = grid(n, 5, 40, 38, 8, 8, 4, lambda i, x, y: starfish(x, y))
    return svg_wrap(W, H, body, "%d starfish with 5 arms each" % n)


def tally_body(x, y, groups, ones=0):
    """Tally marks: `groups` bundles of 5 (4 lines and a line across), then `ones` single lines."""
    s, gx, right = [], x, x
    for g in range(groups):
        for k in range(4):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (gx + 4 + k * 9, y, gx + 4 + k * 9, y + 34, INK))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                 % (gx - 2, y + 28, gx + 37, y + 6, RED))
        right = gx + 39
        gx += 50
    for k in range(ones):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                 % (gx + 4 + k * 9, y, gx + 4 + k * 9, y + 34, INK))
        right = gx + 4 + k * 9 + 2
    return "".join(s), right - x


def tally_svg(groups, ones=0):
    body, w = tally_body(10, 8, groups, ones)
    return svg_wrap(w + 18, 50, body, "tally marks: %d groups of 5%s" % (groups, " and %d more" % ones if ones else ""),
                    large=groups + (1 if ones else 0) > 4)


def rod(x, y):
    return "".join("<rect x='%d' y='%d' width='14' height='13' fill='%s' stroke='%s' stroke-width='1.2'/>"
                   % (x, y + k * 13, "#f1d77a", "#9a7a1c") for k in range(10))


def rods_svg(n):
    body, W, H = grid(n, 10, 14, 130, 9, 8, 6, lambda i, x, y: rod(x, y))
    return svg_wrap(W, H, body, "%d tens sticks" % n, large=n > 6)


def bundle(x, y):
    """A bundle of 10 paddle-pop sticks with a rubber band, in a 46 x 70 box."""
    s = []
    for k in range(10):
        s.append("<rect x='%.1f' y='%d' width='4' height='66' rx='2' fill='#f0d9a8' stroke='#a07a3a' stroke-width='0.8'/>"
                 % (x + 1 + k * 4.4, y + 2))
    s.append("<rect x='%d' y='%d' width='46' height='7' rx='2' fill='%s'/>" % (x - 1, y + 31, RED))
    return "".join(s)


def bundles_svg(n, loose=0):
    """n bundles of 10 and `loose` single sticks."""
    s = []
    rows = rows_of(n, 6)
    W = 0
    i = 0
    for r, k in enumerate(rows):
        for c in range(k):
            s.append(bundle(6 + c * 54, 6 + r * 78))
            i += 1
        W = max(W, 6 + k * 54 - 8)
    H = 6 + len(rows) * 78 - 8 + 6
    if loose:
        lx = W + 14 if len(rows) == 1 else 6 + rows[-1] * 54
        ly = 6 + (len(rows) - 1) * 78
        for k in range(loose):
            s.append("<rect x='%d' y='%d' width='4' height='66' rx='2' fill='#f0d9a8' stroke='#a07a3a' stroke-width='0.8'/>"
                     % (lx + k * 10, ly + 2))
        W = max(W, lx + loose * 10 - 6)
    return svg_wrap(W + 6, H, "".join(s), "%d bundles of 10 sticks%s" % (n, " and %d single sticks" % loose if loose else ""),
                    large=n + loose > 4)


def ten_frame(x, y, k=10):
    s = ["<rect x='%d' y='%d' width='90' height='36' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x, y, GREEN)]
    for c in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x + 18 * c, y, x + 18 * c, y + 36, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y + 18, x + 90, y + 18, GREEN))
    for j in range(k):
        r, c = divmod(j, 5)
        s.append("<circle cx='%d' cy='%d' r='6.5' fill='%s'/>" % (x + 9 + 18 * c, y + 9 + 18 * r, RED))
    return "".join(s)


def frames_svg(n, last=10):
    """n ten frames; all full except the last, which has `last` counters."""
    body, W, H = grid(n, 3, 90, 36, 10, 10, 4,
                      lambda i, x, y: ten_frame(x, y, last if i == n - 1 else 10))
    return svg_wrap(W, H, body, "%d ten frames" % n, large=n > 3)


def bike(x, y):
    return ("<circle cx='%d' cy='%d' r='10' fill='none' stroke='%s' stroke-width='2.5'/>"
            "<circle cx='%d' cy='%d' r='10' fill='none' stroke='%s' stroke-width='2.5'/>"
            "<polyline points='%d,%d %d,%d %d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
            "stroke-linejoin='round'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>"
            % (x + 11, y + 24, INK, x + 47, y + 24, INK,
               x + 11, y + 24, x + 24, y + 24, x + 19, y + 11, x + 40, y + 11, x + 47, y + 24, RED,
               x + 15, y + 8, x + 23, y + 8, INK, x + 40, y + 11, x + 38, y + 4, RED))


def bikes_svg(n):
    body, W, H = grid(n, 5, 58, 35, 8, 8, 4, lambda i, x, y: bike(x, y))
    return svg_wrap(W, H, body, "%d bikes" % n)


# ------------------------------------------------------------ groups and arrays
S = 22  # spacing of counters inside a group


def group_box(k):
    cols = min(k, 5)
    rows = (k + 4) // 5
    return cols * S + 12, rows * S + 12


def group_body(x, y, k, kind, w=None, h=None):
    bw, bh = group_box(k)
    w, h = w or bw, h or bh
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x, y, w, h, FILL, GREEN)]
    cols = min(k, 5)
    ox, oy = x + (w - bw) / 2.0, y + (h - bh) / 2.0
    for j in range(k):
        r, c = divmod(j, cols)
        s.append(counter(kind, ox + 6 + c * S + S / 2.0, oy + 6 + r * S + S / 2.0))
    return "".join(s)


def groups_layout(sizes, kind, x0, y0, per_row):
    """Groups side by side (wrapping after per_row). Boxes in one picture share the same height."""
    bh = max(group_box(k)[1] for k in sizes)
    gap = 10
    nrows = -(-len(sizes) // per_row)
    per_row = -(-len(sizes) // nrows)
    rows = [sizes[i:i + per_row] for i in range(0, len(sizes), per_row)]
    s, W = [], 0
    for r, row in enumerate(rows):
        x = x0
        for k in row:
            bw = group_box(k)[0]
            s.append(group_body(x, y0 + r * (bh + gap), k, kind, bw, bh))
            x += bw + gap
        W = max(W, x - gap - x0)
    H = len(rows) * bh + (len(rows) - 1) * gap
    return "".join(s), W, H


def groups_svg(g, k, kind="counter"):
    per = 5 if k <= 2 else (3 if k <= 5 else 2)
    body, W, H = groups_layout([k] * g, kind, 4, 4, per)
    return svg_wrap(W + 8, H + 8, body, "%d groups of %d %s" % (g, k, NAMES[kind]), large=(k == 10 and g > 2))


def array_body(rows_len, x0, y0, sp=26, r=9, kind="counter"):
    return "".join(counter(kind, x0 + c * sp + sp / 2.0, y0 + i * sp + sp / 2.0, r)
                   for i, n in enumerate(rows_len) for c in range(n))


def array_svg(rows, cols, kind="counter"):
    o = 6
    return svg_wrap(cols * 26 + 2 * o, rows * 26 + 2 * o, array_body([cols] * rows, o, o, kind=kind),
                    "%d rows with %d %s in each row" % (rows, cols, NAMES[kind]), large=cols >= 10)


def panel(p, x0, y0):
    """p = ('groups', sizes, kind) | ('rows', row lengths, kind). Returns body, w, h."""
    t, data, kind = p
    if t == "groups":
        return groups_layout(data, kind, x0, y0, 5)
    body = array_body(data, x0, y0, 22, 7.5, kind)
    return body, max(data) * 22, len(data) * 22


def abcd_svg(panels):
    """Four pictures labelled A to D, two on each line."""
    sizes = [panel(p, 0, 0)[1:] for p in panels]
    cw = max(w for w, h in sizes) + 34
    ch = max(h for w, h in sizes) + 12
    s = []
    for k, p in enumerate(panels):
        r, c = divmod(k, 2)
        x, y = c * cw, r * ch
        w, h = sizes[k]
        s.append(text(x + 10, y + 22, "ABCD"[k], 18, "start"))
        s.append(panel(p, x + 30 + (cw - 34 - w) / 2.0, y + 6 + (ch - 12 - h) / 2.0)[0])
    s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cw - 2, cw - 2, 2 * ch - 4, GREY))
    s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (ch, 2 * cw - 4, ch, GREY))
    return svg_wrap(2 * cw, 2 * ch, "".join(s), "four pictures labelled A to D", large=True)


def track_svg(cells, label=None):
    """Number track. cells: list of numbers or '?'."""
    w, h, m = 46, 40, 3
    s = []
    for i, v in enumerate(cells):
        q = v == "?"
        x = m + i * w
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, m, w, h, FILL if q else "#ffffff", GREEN))
        s.append(text(x + w / 2.0, m + 27, str(v), 18, col=RED if q else INK))
    return svg_wrap(2 * m + len(cells) * w, 2 * m + h, "".join(s), label or "number track", large=True)


def chart_svg(lo, hi, shaded):
    """Part of a number chart (10 a row) from lo to hi; `shaded` numbers are coloured."""
    w, h, m = 30, 28, 3
    s = []
    for v in range(lo, hi + 1):
        r, c = divmod(v - lo, 10)
        x, y = m + c * w, m + r * h
        on = v in shaded
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                 % (x, y, w, h, "#f6d7a6" if on else "#ffffff", GREEN))
        s.append(text(x + w / 2.0, y + 19, str(v), 14))
    rows = (hi - lo) // 10 + 1
    return svg_wrap(2 * m + 10 * w, 2 * m + rows * h, "".join(s),
                    "number chart from %d to %d with some numbers coloured" % (lo, hi), large=True)


# ============================================================ sequence questions
def seq_next(nums, step, its, back=False):
    """Count on (or back) in steps: what comes next? Wrong: count in 1s, jump too far, go the wrong way."""
    last = nums[-1]
    d = -step if back else step
    ans = last + d
    assert all(b - a == d for a, b in zip(nums, nums[1:]))
    one = last - 1 if back else last + 1
    far = last + 2 * d
    wrong_way = last - d
    word = "back " if back else ""
    q = fig(track_svg(nums + ["?"])) + "Count %sby %ds. What comes next?" % (word, step)
    e = ("Each number is %d %s. %d %s %d = <b>%d</b>. %d is counting %sby 1s."
         % (step, "less" if back else "more", last, "−" if back else "+", step, ans, one, word))
    its.append(mcq(q, ans, [one, far, wrong_way], e))


def seq_gap(a, step, its):
    """a, a+s, ?, a+3s: what is missing? Wrong: 1 more, 1 less than the next, jump too far."""
    ans = a + 2 * step
    q = fig(track_svg([a, a + step, "?", a + 3 * step])) + "Count by %ds. What number is missing?" % step
    e = "%d + %d = <b>%d</b>. Then %d + %d = %d. It fits." % (a + step, step, ans, ans, step, a + 3 * step)
    its.append(mcq(q, ans, [a + step + 1, a + 3 * step - 1, a + 4 * step], e))


# ============================================================ set 1: count pairs by 2s
def set_twos(P):
    its = []

    def pairs(n, kind):
        t = 2 * n
        e = ("Each pair has 2 %s. Count by 2s: %s. There are <b>%d</b> %s. %d counts the pairs, not the %s."
             % (kind, lst(steps(2, n)), t, kind, n, kind))
        its.append(mcq(fig(pairs_svg(n, kind)) + "How many %s? Count by 2s." % kind, t, [n, t - 2, t + 1], e))

    def eyes(n):
        t = 2 * n
        e = "Each child has 2 eyes. Count by 2s: %s. There are <b>%d</b> eyes." % (lst(steps(2, n)), t)
        its.append(mcq(fig(faces_svg(n)) + "How many eyes? Count by 2s.", t, [n, t - 2, t + 2, t + 1], e))

    def wheels(n):
        t = 2 * n
        e = "A bike has 2 wheels. Count by 2s: %s. There are <b>%d</b> wheels." % (lst(steps(2, n)), t)
        its.append(mcq(fig(bikes_svg(n)) + "How many wheels? Count by 2s.", t, [n, t + 1, t - 2], e))

    def legs(n):
        t = 2 * n
        e = "A kookaburra has 2 legs. Count by 2s: %s. There are <b>%d</b> legs." % (lst(steps(2, n)), t)
        its.append(mcq(fig(birds_svg(n)) + "How many legs? Count by 2s.", t, [n, 5 * n, t - 2], e))

    pairs(3, "socks")
    eyes(3)
    seq_next([2, 4, 6, 8], 2, its)
    wheels(3)
    pairs(4, "shoes")
    legs(4)
    seq_next([12, 14, 16], 2, its)
    pairs(5, "socks")
    its.append(mcq(fig(track_svg([0, 2, 4, 6, 8, 10])) + "Keep counting by 2s. Which number will you say?", 14,
                   [7, 9, 15],
                   "0, 2, 4, 6, 8, 10, 12, <b>14</b>. Counting by 2s from 0, you say every second number. "
                   "7, 9 and 15 are skipped."))
    eyes(6)
    seq_gap(6, 2, its)
    pairs(6, "shoes")
    wheels(5)
    seq_next([20, 18, 16], 2, its, back=True)
    pairs(7, "socks")
    legs(7)
    seq_next([24, 26, 28], 2, its)
    its.append(mcq(fig(track_svg([0, 2, 4, 6, 8, 10])) + "Keep counting by 2s. Which number do you NOT say?", 13,
                   [12, 16, 18],
                   "0, 2, 4 … 10, 12, 14, 16, 18. You say 12, 16 and 18. You jump over <b>13</b>."))
    eyes(9)
    pairs(10, "socks")
    assert len(its) == 20, len(its)
    return {"title": "Count pairs by 2s", "items": its}


# ============================================================ set 2: count hands by 5s
def set_fives(P):
    its = []

    def hands(n):
        t = 5 * n
        e = ("Each hand has 5 fingers. Count by 5s: %s. There are <b>%d</b> fingers. %d is counting by 2s, not 5s."
             % (lst(steps(5, n)), t, 2 * n))
        its.append(mcq(fig(hands_svg(n)) + "How many fingers? Count by 5s.", t, [n, 2 * n, t - 5], e))

    def coins(n):
        t = 5 * n
        e = "Each coin is 5c. Count by 5s: %s. That is <b>%dc</b>." % (lst(steps(5, n)), t)
        its.append(mcq(fig(coins_svg(5, n)) + "Each coin is 5c. How much money?", "%dc" % t,
                       ["%dc" % v for v in (n, t - 5, 2 * n, t + 1)], e))

    def stars(n):
        t = 5 * n
        e = "Each starfish has 5 arms. Count by 5s: %s. There are <b>%d</b> arms." % (lst(steps(5, n)), t)
        its.append(mcq(fig(starfish_svg(n)) + "How many arms? Count by 5s.", t, [n, t - 5, t + 1], e))

    def tally(g, ones=0):
        t = 5 * g + ones
        if ones:
            e = ("Count each bundle of tally marks by 5s: %s. Then count on by 1s: %s. That is <b>%d</b>."
                 % (lst(steps(5, g)), lst(range(5 * g + 1, t + 1)), t))
            its.append(mcq(fig(tally_svg(g, ones)) + "Count by 5s, then by 1s. How many?",
                           t, [g + ones, 5 * (g + ones), t - 5, t + 1], e))
        else:
            e = ("A bundle of tally marks is 5: 4 lines and 1 line across. Count by 5s: %s. That is <b>%d</b>. "
                 "Count the line across too." % (lst(steps(5, g)), t))
            its.append(mcq(fig(tally_svg(g)) + "How many tally marks? Count by 5s.", t, [g, 4 * g, t - 5, t + 5], e))

    hands(2)
    seq_next([5, 10, 15], 5, its)
    stars(3)
    hands(3)
    tally(4)
    coins(3)
    seq_next([30, 35, 40], 5, its)
    stars(4)
    its.append(mcq(fig(track_svg([5, 10, 15, 20, 25, 30])) + "Count by 5s. How do the numbers end?", "in 0 or 5",
                   ["only in 5", "only in 0", "in any digit"],
                   "5, 10, 15, 20, 25, 30 … The last digit goes 5, 0, 5, 0. They always end <b>in 0 or 5</b>."))
    hands(4)
    seq_gap(20, 5, its)
    coins(6)
    tally(5)
    seq_next([50, 45, 40], 5, its, back=True)
    hands(6)
    its.append(mcq(fig(track_svg([25, 30, 35, 40])) + "Keep counting by 5s. Which number will you say?", 55,
                   [52, 54, 46],
                   "40, 45, 50, <b>55</b>. Counting by 5s, every number ends in 0 or 5. 52, 54 and 46 do not."))
    coins(9)
    tally(7)
    seq_next([85, 90, 95, 100], 5, its)
    seq_next([115, 110, 105], 5, its, back=True)
    assert len(its) == 20, len(its)
    return {"title": "Count hands by 5s", "items": its}


# ============================================================ set 3: count bundles by 10s
def set_tens(P):
    its = []

    def rods(n):
        t = 10 * n
        e = "Each stick has 10 cubes. Count by 10s: %s. There are <b>%d</b> cubes." % (lst(steps(10, n)), t)
        its.append(mcq(fig(rods_svg(n)) + "Each stick has 10 cubes. How many cubes?", t, [n, t - 10, t + 1], e))

    def bundles(n):
        t = 10 * n
        e = ("Each bundle has 10 sticks. Count by 10s: %s. There are <b>%d</b> sticks. %d counts the bundles, not the sticks."
             % (lst(steps(10, n)), t, n))
        its.append(mcq(fig(bundles_svg(n)) + "Each bundle has 10 sticks. How many sticks?", t, [n, t - 10, t + 10], e))

    def coins(n):
        t = 10 * n
        e = "Each coin is 10c. Count by 10s: %s. That is <b>%dc</b>." % (lst(steps(10, n)), t)
        its.append(mcq(fig(coins_svg(10, n)) + "Each coin is 10c. How much money?", "%dc" % t,
                       ["%dc" % v for v in (n, t - 10, 5 * n, t + 1)], e))

    def hand_pairs(n):
        t = 10 * n
        e = ("Each child shows 2 hands. That is 10 fingers. Count by 10s: %s. There are <b>%d</b> fingers."
             % (lst(steps(10, n)), t))
        its.append(mcq(fig(hand_pairs_svg(n)) + "How many fingers? Count by 10s.", t, [n, 5 * n, t - 10, 2 * n], e))

    def frames(n):
        t = 10 * n
        e = "A full ten frame has 10 counters. Count by 10s: %s. There are <b>%d</b> counters." % (lst(steps(10, n)), t)
        its.append(mcq(fig(frames_svg(n)) + "Each ten frame is full. How many counters?", t, [n, t - 10, t + 1], e))

    bundles(3)
    seq_next([10, 20, 30], 10, its)
    rods(4)
    hand_pairs(2)
    coins(4)
    frames(5)
    seq_next([40, 50, 60], 10, its)
    bundles(5)
    its.append(mcq(fig(track_svg([20, "?", "?"])) + "Which one counts by 10s?", "20, 30, 40",
                   ["20, 21, 22", "20, 25, 30", "20, 22, 24"],
                   "Counting by 10s, each number is 10 more: <b>20, 30, 40</b>. "
                   "20, 21, 22 is 1s. 20, 22, 24 is 2s. 20, 25, 30 is 5s."))
    rods(6)
    seq_gap(30, 10, its)
    hand_pairs(3)
    seq_next([90, 80, 70], 10, its, back=True)
    coins(7)
    its.append(mcq(fig(bundles_svg(5)) + "How many bundles of 10 make 50?", 5, [50, 10, 6],
                   "Count by 10s: 10, 20, 30, 40, 50. That is <b>5</b> bundles."))
    bundles(8)
    seq_next([80, 90, 100], 10, its)
    frames(6)
    its.append(mcq(fig(track_svg([0, 10, 20, 30, 40])) + "Keep counting by 10s. Which number do you NOT say?", 75,
                   [70, 90, 110],
                   "0, 10, 20 … 60, 70, 80, 90, 100, 110. Every number ends in 0. <b>75</b> ends in 5, so you do not say it."))
    bundles(11)
    assert len(its) == 20, len(its)
    return {"title": "Count bundles by 10s", "items": its}


# ============================================================ set 4: continue patterns, missing numbers
def set_patterns(P):
    its = []

    def rule(nums, step):
        q = fig(track_svg(nums)) + "How does this pattern count?"
        others = {2: "by 2s", 5: "by 5s", 10: "by 10s"}
        e = "Each number is %d more than the one before. %d + %d = %d. It counts <b>by %ds</b>." % (
            step, nums[0], step, nums[1], step)
        its.append(mcq(q, others[step], [v for k, v in others.items() if k != step] + ["by 1s"], e))

    def chart(step, upto, lo=1, hi=30):
        shaded = [v for v in range(step, upto + 1, step)]
        ans = upto + step
        assert ans <= hi
        q = fig(chart_svg(lo, hi, shaded)) + "The coloured numbers count by %ds. Which is coloured next?" % step
        e = ("The last coloured number is %d. %d + %d = <b>%d</b>. %d is only 1 more."
             % (upto, upto, step, ans, upto + 1))
        its.append(mcq(q, ans, [upto + 1, ans + 1, ans + step, upto + 2], e))

    def wrong_one(nums, bad_i, bad, step):
        shown = list(nums)
        shown[bad_i] = bad
        q = fig(track_svg(shown)) + "Count by %ds. Which number is wrong?" % step
        e = ("Count by %ds: %s. It should be %d, not <b>%d</b>." % (step, lst(nums), nums[bad_i], bad))
        others = [v for i, v in enumerate(shown) if i != bad_i]
        its.append(mcq(q, bad, others[1:] + others[:1], e))

    def two_gaps(cells, a, b, step, wrong):
        q = fig(track_svg(cells)) + "Count by %ds. Which numbers are missing?" % step
        full = []
        it = iter([a, b])
        for c in cells:
            full.append(next(it) if c == "?" else c)
        assert all(y - x == step for x, y in zip(full, full[1:]))
        e = "Add %d each time: %s. The missing numbers are <b>%d and %d</b>." % (step, lst(full), a, b)
        its.append(mcq(q, "%d and %d" % (a, b), ["%d and %d" % w for w in wrong], e))

    seq_next([15, 20, 25], 5, its)
    seq_next([50, 60, 70], 10, its)
    seq_next([6, 8, 10], 2, its)
    rule([5, 10, 15, 20], 5)
    seq_gap(14, 2, its)
    seq_gap(60, 10, its)
    chart(2, 12)
    seq_next([35, 30, 25], 5, its, back=True)
    wrong_one([2, 4, 6, 8, 10], 3, 9, 2)
    two_gaps(["?", 20, 30, "?"], 10, 40, 10, [(19, 31), (15, 35), (10, 31)])
    its.append(mcq(fig(track_svg([1, 3, 5, 7, "?"])) + "Count by 2s from 1. What comes next?", 9, [8, 10, 11],
                   "Each number is 2 more. 7 + 2 = <b>9</b>. 8 is counting by 1s. 10 jumps to an even number."))
    chart(5, 20)
    seq_next([70, 80, 90, 100], 10, its)
    rule([30, 40, 50, 60], 10)
    seq_next([30, 28, 26], 2, its, back=True)
    seq_gap(65, 5, its)
    its.append(mcq(fig(track_svg([3, 13, 23, "?"])) + "Count by 10s from 3. What comes next?", 33, [24, 30, 43],
                   "Adding 10 changes the tens and keeps the ones digit. 23 + 10 = <b>33</b>. "
                   "24 is 1 more. 30 forgets the 3 ones."))
    wrong_one([40, 45, 50, 55, 60], 3, 56, 5)
    seq_next([100, 105, 110], 5, its)
    two_gaps([20, "?", 24, "?"], 22, 26, 2, [(21, 25), (22, 28), (21, 26)])
    assert len(its) == 20, len(its)
    return {"title": "Continue the pattern and find missing numbers", "items": its}


# ============================================================ set 5: count a collection in groups
def set_stories(P):
    its = []

    def story(q, ans, wrong, e, pic, unit=""):
        u = (lambda v: "%d%s" % (v, unit))
        its.append(mcq(fig(pic) + q, u(ans), [u(v) for v in wrong], e))

    def text_item(q, ans, wrong, e, pic):
        its.append(mcq(fig(pic) + q, ans, wrong, e))

    nm, he, his = P.next()
    story("%s puts %s shells in groups of 2. How many shells?" % (nm, his), 8, [4, 6, 9],
          "Count by 2s, one group at a time: 2, 4, 6, 8. There are <b>8</b> shells.", groups_svg(4, 2, "shell"))
    story("A kookaburra has 2 wings. How many wings do 6 kookaburras have?", 12, [6, 10, 13],
          "Count by 2s: 2, 4, 6, 8, 10, 12. There are <b>12</b> wings.", birds_svg(6))
    nm, he, his = P.next()
    story("%s buys a bun at the canteen. %s pays with these 10c coins. How much does %s pay?" % (nm, cap(he), he), 50, [5, 40, 25],
          "Count by 10s: 10c, 20c, 30c, 40c, 50c. That is <b>50c</b>.", coins_svg(10, 5), "c")
    story("The class lines up in pairs. There are 6 pairs. How many children?", 12, [6, 10, 14],
          "Count by 2s: 2, 4, 6, 8, 10, 12. There are <b>12</b> children.", groups_svg(6, 2, "counter"))
    nm, he, his = P.next()
    story("%s has 3 packs of footy cards. Each pack has 5 cards. How many cards?" % nm, 15, [3, 6, 10],
          "Count by 5s: 5, 10, 15. There are <b>15</b> cards. 6 is counting by 2s.", groups_svg(3, 5, "counter"))
    nm, he, his = P.next()
    story("%s ties paddle-pop sticks in bundles of 10. How many sticks?" % nm, 34, [7, 43, 30],
          "Count the bundles by 10s: 10, 20, 30. Then count on by 1s: 31, 32, 33, 34. "
          "There are <b>34</b> sticks.", bundles_svg(3, 4))
    story("The tally shows who came to sport. How many children?", 22, [6, 30, 17],
          "Count by 5s: 5, 10, 15, 20. Then by 1s: 21, 22. That is <b>22</b>.", tally_svg(4, 2))
    nm, he, his = P.next()
    its.append(mcq(fig(hands_svg(4)) + "%s counts the fingers: 5, 10, 15. What went wrong?" % nm,
                   "missed a hand", ["counted by 2s", "counted by 1s", "nothing"],
                   "There are 4 hands, but %s said only 3 numbers. %s <b>missed a hand</b>. "
                   "5, 10, 15, 20: there are 20 fingers. Touch each hand as you count." % (nm, cap(he))))
    its.append(abcd_item("Which picture shows 3 groups of 5?", ("groups", [5, 5, 5], "apple"),
                         [("groups", [3, 3, 3, 3, 3], "apple"), ("groups", [5, 5], "apple"),
                          ("groups", [5, 4, 5], "apple")],
                         "<b>{L}</b> has 3 groups, with 5 in each group. Count by 5s: 5, 10, 15."))
    nm, he, his = P.next()
    story("%s has 20 lollies in rows of 5. How many rows?" % nm, 4, [20, 5, 3],
          "Count by 5s, one row at a time: 5, 10, 15, 20. That is <b>4</b> rows.", array_svg(4, 5, "lolly"))
    nm, he, his = P.next()
    story("%s pegs 8 pairs of socks on the line. How many socks?" % nm, 16, [8, 14, 40],
          "Count by 2s: 2, 4, 6, 8, 10, 12, 14, 16. There are <b>16</b> socks. 40 is counting by 5s.",
          pairs_svg(8, "socks"))
    its.append(abcd_item("Which picture shows equal groups?", ("groups", [2, 2, 2, 2], "lolly"),
                         [("groups", [2, 3, 2, 2], "lolly"), ("groups", [1, 2, 2, 2], "lolly"),
                          ("groups", [2, 2, 3, 1], "lolly")],
                         "Equal groups all have the same number. In <b>{L}</b>, every group has 2."))
    nm, he, his = P.next()
    story("%s has these 5c coins for the sausage sizzle. How much money?" % nm, 40, [8, 16, 35],
          "Count by 5s: 5c, 10c, 15c, 20c, 25c, 30c, 35c, 40c. That is <b>40c</b>. 16c is counting by 2s.",
          coins_svg(5, 8), "c")
    nm, he, his = P.next()
    text_item("%s counts these socks: 5, 10, 15. What went wrong?" % nm,
              "counted by 5s", ["missed a pair", "counted by 1s", "nothing"],
              "A pair is 2, so count by 2s: 2, 4, 6. There are 6 socks. %s <b>counted by 5s</b> by mistake." % nm,
              pairs_svg(3, "socks"))
    story("Bread rolls come in bags of 10. How many rolls are in 6 bags?", 60, [6, 50, 16],
          "Count by 10s: 10, 20, 30, 40, 50, 60. There are <b>60</b> rolls. 16 adds 10 and 6.", groups_svg(6, 10, "counter"))
    nm, he, his = P.next()
    story("%s has 40c in 10c coins. How many coins does %s have?" % (nm, he), 4, [40, 10, 8],
          "Count by 10s up to 40: 10c, 20c, 30c, 40c. That is <b>4</b> coins. 8 coins would be 5c coins.",
          track_svg([10, 20, 30, 40]))
    story("5 children sit at each table. There are 5 tables. How many children?", 25, [5, 10, 20],
          "Count by 5s, one table at a time: 5, 10, 15, 20, 25. There are <b>25</b> children. "
          "20 misses a table.", groups_svg(5, 5, "counter"))
    nm, he, his = P.next()
    story("%s collects shells in groups of 10. How many shells?" % nm, 30, [3, 20, 13],
          "Count by 10s: 10, 20, 30. There are <b>30</b> shells.", groups_svg(3, 10, "shell"))
    story("3 ten frames are full. One has 5. How many counters?", 35, [4, 40, 30],
          "Count the full frames by 10s: 10, 20, 30. Then add 5 more: <b>35</b>. 40 counts the last frame as 10.",
          frames_svg(4, 5))
    story("Each hand has 5 fingers. How many fingers on 9 hands?", 45, [9, 18, 40],
          "Count by 5s: 5, 10, 15, 20, 25, 30, 35, 40, 45. There are <b>45</b> fingers. "
          "18 is counting by 2s. 40 misses a hand.", hands_svg(9))
    assert len(its) == 20, len(its)
    return {"title": "Count a collection in groups", "items": its}


def cap(s):
    return s[0].upper() + s[1:]


# ============================================================ balance (and build A-D pictures)
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, right, wrong = it.pop("_abcd")
                wrong = list(wrong)
                rnd.shuffle(wrong)
                panels = wrong[:t] + [right] + wrong[t:]
                it["q"] = fig(abcd_svg(panels)) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is skip counting?</h2>"
        "<p>Skip counting means counting in equal jumps. "
        "Socks come in pairs, so count by 2s. A hand has 5 fingers, so count by 5s. "
        "A bundle has 10 sticks, so count by 10s. It is faster than counting by 1s.</p>"
        + table(["Count by", "Say", "Think of"], [
            ["2s", "2, 4, 6, 8, 10, 12", "pairs of socks, eyes, bike wheels"],
            ["5s", "5, 10, 15, 20, 25, 30", "fingers on a hand, tally marks, 5c coins"],
            ["10s", "10, 20, 30, 40, 50, 60", "bundles of 10 sticks, ten frames, 10c coins"],
        ])
        + "<h2>Count a collection in groups</h2>"
        "<p>Touch one group at a time. Say one number for each group.</p>"
        + "<figure class='sn-fig'>" + pairs_svg(4, "socks")
        + "<figcaption>4 pairs of socks: 2, 4, 6, 8. There are 8 socks.</figcaption></figure>"
        + "<figure class='sn-fig'>" + hands_svg(3)
        + "<figcaption>3 hands: 5, 10, 15. There are 15 fingers.</figcaption></figure>"
        + "<figure class='sn-fig'>" + bundles_svg(4)
        + "<figcaption>4 bundles of 10: 10, 20, 30, 40. There are 40 sticks.</figcaption></figure>"
        + ex("Example", "How many tally marks?", "Count each bundle by 5s: 5, 10, 15. Then count on by 1s: 16, 17.",
             "17")
        + "<figure class='sn-fig'>" + tally_svg(3, 2)
        + "<figcaption>3 bundles of 5 and 2 more: 5, 10, 15, 16, 17.</figcaption></figure>"
        + "<h2>Skip-counting patterns</h2>"
        "<p>In a pattern, the jump is always the same. Find the jump. Then keep going, or fill the gap.</p>"
        + "<figure class='sn-fig'>" + track_svg([15, 20, 25, "?"])
        + "<figcaption>Each number is 5 more. 25 + 5 = 30.</figcaption></figure>"
        + ex("Example", "What is missing? 40, 50, ?, 70", "The jump is 10. 50 + 10 = 60. Check: 60 + 10 = 70.", "60")
        + "<p>Counting by 2s from 0 gives 2, 4, 6, 8. Counting by 5s ends in 0 or 5. "
        "Counting by 10s ends in 0. You can count back too: 30, 28, 26.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Going back to 1s: 2, 4, 6, 7", "Keep the same jump: 2, 4, 6, 8"],
            ["Mixing 2s and 5s: 3 pairs of socks as 5, 10, 15", "A pair is 2: 2, 4, 6 socks"],
            ["Missing a group: 4 hands, but only 5, 10, 15", "Touch each hand as you count: 5, 10, 15, 20"],
            ["Counting the groups, not the things: 3 bundles = 3 sticks", "Each bundle is 10: 10, 20, 30 sticks"],
        ])
    )


FAQ = [
    {"q": "What does skip counting mean in Year 1 maths?",
     "a": "Skip counting is counting in equal jumps, such as 2, 4, 6 or 5, 10, 15. In the Australian Curriculum, Year 1 students recognise, continue and create skip-counting patterns by twos, fives and tens (AC9M1A01)."},
    {"q": "Why do Year 1 students count collections in groups?",
     "a": "Counting in equal groups is faster and more accurate than counting by ones. Year 1 students partition collections into equal groups and skip count to find the total (AC9M1N03), which prepares them for multiplication in later years."},
    {"q": "How can I help my child skip count at home?",
     "a": "Count real things: pairs of socks by 2s, fingers by 5s and 10c coins by 10s. Ask your child to touch each group as they say the number, so no group is missed."},
    {"q": "How far should a Year 1 student skip count?",
     "a": "Year 1 students work with numbers to at least 120. They should be able to count by 2s, 5s and 10s from zero, keep going past 100 and find missing numbers in a pattern."},
]


def gen():
    rnd = random.Random(1804)
    P = People(rnd)
    sets = [set_twos(P), set_fives(P), set_tens(P), set_patterns(P), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "_abcd" not in it and "{" not in it["e"]
            assert it["q"].count("<svg") == 1, it["q"]
            assert "×" not in it["q"] + it["e"] and "÷" not in it["q"] + it["e"]
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 <= int(tok) <= 120, c
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            m = re.search(r"aria-label='(\d+) groups of (\d+) (\w+)'", it["q"])
            if m:
                assert it["q"].count("rx='10' fill='%s'" % FILL) == int(m.group(1))
            m = re.search(r"aria-label='(\d+) coins of (\d+)c'", it["q"])
            if m:
                assert it["q"].count("r='%d' fill='%s'" % (COIN[int(m.group(2))][0], SILVER[0])) == int(m.group(1))
            m = re.search(r"aria-label='(\d+) bundles of 10 sticks", it["q"])
            if m:
                assert it["q"].count("height='7' rx='2'") == int(m.group(1))
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "skip-counting-by-2s-5s-and-10s", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Skip Counting by 2s, 5s and 10s",
        "seo_title": "Year 1 Skip Counting Worksheets: Count by 2s, 5s and 10s (Free, Australian Curriculum)",
        "short_title": "Skip counting by 2s, 5s and 10s",
        "domain": "Algebra",
        "standard_code": "AC9M1A01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise, continue and create pattern sequences, with numbers, symbols, shapes and objects, formed by skip counting, initially by twos, fives and tens",
        "meta_desc": "Free Year 1 maths worksheets on skip counting by 2s, 5s and 10s: pairs of socks, fingers on hands, tally marks, bundles of 10, 5c and 10c coins, missing numbers in patterns and counting collections in groups. 100 picture questions with an answer key, following the Australian Curriculum.",
        "key_big": "Count in equal jumps: 2, 4, 6 … 5, 10, 15 … 10, 20, 30.",
        "key_sub": "Pairs go by 2s, hands by 5s and bundles of 10 by 10s. Touch each group as you count so none is missed, and keep the same jump all the way.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
