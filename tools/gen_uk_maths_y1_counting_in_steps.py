# -*- coding: utf-8 -*-
"""
UK Year 1 Maths (National Curriculum in England): counting in 2s, 5s and 10s,
equal groups, arrays and sharing.
  python3 tools/gen_uk_maths_y1_counting_in_steps.py
Year 1 has no × or ÷ signs: we say "groups of", "lots of" and "share".
Every answer, every wrong answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
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
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
COPPER = ("#d9915a", "#8a5428")
SILVER = ("#dfe3e7", "#7a828a")
COIN = {2: (22, COPPER, 15), 5: (18, SILVER, 14), 10: (21, SILVER, 14)}


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


def abcd_item(prompt, right, wrong, e, draw):
    """A-D picture question. The picture is built in balance() so the right letter lands on its target."""
    assert len(wrong) == 3 and right not in wrong and len({repr(w) for w in wrong}) == 3
    return {"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e, "_abcd": (prompt, right, wrong, draw)}


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


def lst(xs):
    return ", ".join(str(x) for x in xs)


def steps(step, n, start=None):
    """Count in steps: steps(2, 4) -> [2, 4, 6, 8]."""
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
    if kind == "sweet":
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
    if kind == "star":
        pts = []
        for k in range(10):
            rr = r * 1.1 if k % 2 == 0 else r * 0.46
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
        return "<polygon points='%s' fill='%s'/>" % (" ".join(pts), BLUE)
    raise ValueError(kind)


NAMES = {"counter": "counters", "sweet": "sweets", "apple": "apples", "star": "stars"}


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


def coin(v, cx, cy):
    r, (fill, edge), fs = COIN[v]
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>"
            % (cx, cy, r, fill, edge, cx, cy, r - 4, edge) + text(cx, cy + fs * 0.36, "%dp" % v, fs))


def coins_svg(v, n):
    d = 2 * COIN[v][0]
    body, W, H = grid(n, 5, d, d, 6, 6, 4, lambda i, x, y: coin(v, x + d / 2, y + d / 2))
    return svg_wrap(W, H, body, "%d coins of %dp" % (n, v))


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


def flower(x, y):
    cx, cy = x + 17, y + 17
    s = ["<circle cx='%.1f' cy='%.1f' r='7' fill='#f2b8d0' stroke='%s' stroke-width='1.2'/>"
         % (cx + 10 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5), cy + 10 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5),
            "#a0446c") for k in range(5)]
    s.append("<circle cx='%d' cy='%d' r='5' fill='#f1d77a' stroke='#9a7a1c' stroke-width='1'/>" % (cx, cy))
    return "".join(s)


def flowers_svg(n):
    body, W, H = grid(n, 5, 34, 34, 8, 8, 4, lambda i, x, y: flower(x, y))
    return svg_wrap(W, H, body, "%d flowers with 5 petals each" % n)


def rod(x, y):
    return "".join("<rect x='%d' y='%d' width='14' height='13' fill='%s' stroke='%s' stroke-width='1.2'/>"
                   % (x, y + k * 13, "#f1d77a", "#9a7a1c") for k in range(10))


def rods_svg(n):
    body, W, H = grid(n, 10, 14, 130, 9, 8, 6, lambda i, x, y: rod(x, y))
    return svg_wrap(W, H, body, "%d tens sticks" % n)


def ten_frame(x, y, k=10):
    s = ["<rect x='%d' y='%d' width='90' height='36' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x, y, GREEN)]
    for c in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x + 18 * c, y, x + 18 * c, y + 36, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y + 18, x + 90, y + 18, GREEN))
    for j in range(k):
        r, c = divmod(j, 5)
        s.append("<circle cx='%d' cy='%d' r='6.5' fill='%s'/>" % (x + 9 + 18 * c, y + 9 + 18 * r, RED))
    return "".join(s)


def frames_svg(n):
    body, W, H = grid(n, 3, 90, 36, 10, 10, 4, lambda i, x, y: ten_frame(x, y))
    return svg_wrap(W, H, body, "%d full ten frames" % n)


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


# ------------------------------------------------------------ groups, arrays, plates
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
    per_row = -(-len(sizes) // nrows)          # 6 groups, 5 a row -> 3 + 3, not 5 + 1
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
                    "array of %d rows with %d %s in each row" % (rows, cols, NAMES[kind]), large=cols >= 10)


PLATE_W, PLATE_H = 84, 50


def plate(x, y, k, kind):
    """A plate (seen from above) with k things on it, 3 a row."""
    cx, cy = x + PLATE_W / 2.0, y + PLATE_H / 2.0
    s = ["<ellipse cx='%.1f' cy='%.1f' rx='%d' ry='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         "<ellipse cx='%.1f' cy='%.1f' rx='%d' ry='%d' fill='none' stroke='%s' stroke-width='1'/>"
         % (cx, cy, PLATE_W / 2 - 1, PLATE_H / 2 - 1, GREY, cx, cy, PLATE_W / 2 - 9, PLATE_H / 2 - 7, GREY)]
    assert k <= 6
    rows = rows_of(k, 3) if k else []
    for r, n in enumerate(rows):
        yy = cy + (r - (len(rows) - 1) / 2.0) * 17
        for c in range(n):
            s.append(counter(kind, cx + (c - (n - 1) / 2.0) * 21, yy, 6.5))
    return "".join(s)


def plates_body(counts, kind, x0, y0):
    gap = 8
    s = [plate(x0 + i * (PLATE_W + gap), y0, k, kind) for i, k in enumerate(counts)]
    return "".join(s), len(counts) * PLATE_W + (len(counts) - 1) * gap, PLATE_H


def share_svg(n, g, kind="sweet"):
    """n things on top (rows of up to 10), g empty plates below."""
    rows = rows_of(n, 10)
    sp = 24
    top_w = max(rows) * sp
    pb, pw, ph = plates_body([0] * g, kind, 0, 0)
    W = max(top_w, pw) + 12
    s = []
    tx = (W - top_w) / 2.0
    for r, k in enumerate(rows):
        for c in range(k):
            s.append(counter(kind, tx + c * sp + sp / 2.0, 6 + r * sp + sp / 2.0, 8))
    y = 6 + len(rows) * sp + 10
    px = (W - pw) / 2.0
    pb, _, _ = plates_body([0] * g, kind, px, y)
    s.append(pb)
    H = y + PLATE_H + 6
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), "%d %s and %d empty plates" % (n, NAMES[kind], g),
                    large=True)


def panel(p, x0, y0):
    """p = ('groups', sizes, kind) | ('plates', counts, kind) | ('rows', row lengths, kind). Returns body, w, h."""
    t, data, kind = p
    if t == "groups":
        return groups_layout(data, kind, x0, y0, 5)
    if t == "plates":
        return plates_body(data, kind, x0, y0)
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
    q = fig(track_svg(nums + ["?"])) + "Count %sin %ds. What comes next?" % (word, step)
    e = ("Each number is %d %s. %d %s %d = <b>%d</b>. %d is counting %sin 1s."
         % (step, "less" if back else "more", last, "−" if back else "+", step, ans, one, word))
    its.append(mcq(q, ans, [one, far, wrong_way], e))


def seq_gap(a, step, its):
    """a, a+s, ?, a+3s: what is missing? Wrong: 1 more, 1 less than the next, jump too far."""
    ans = a + 2 * step
    q = fig(track_svg([a, a + step, "?", a + 3 * step])) + "Count in %ds. What number is missing?" % step
    e = "%d + %d = <b>%d</b>. Then %d + %d = %d. It fits." % (a + step, step, ans, ans, step, a + 3 * step)
    its.append(mcq(q, ans, [a + step + 1, a + 3 * step - 1, a + 4 * step], e))


# ============================================================ set 1: count in 2s
def set_twos(P):
    its = []

    def pairs(n, kind):
        t = 2 * n
        e = "Each pair has 2 %s. Count in 2s: %s. There are <b>%d</b> %s." % (kind, lst(steps(2, n)), t, kind)
        its.append(mcq(fig(pairs_svg(n, kind)) + "How many %s? Count in 2s." % kind, t, [n, t - 2, t + 1], e))

    def eyes(n):
        t = 2 * n
        e = "Each child has 2 eyes. Count in 2s: %s. There are <b>%d</b> eyes." % (lst(steps(2, n)), t)
        its.append(mcq(fig(faces_svg(n)) + "How many eyes? Count in 2s.", t, [n, t - 2, t + 1], e))

    def coins(n):
        t = 2 * n
        e = "Each coin is 2p. Count in 2s: %s. That is <b>%dp</b>." % (lst(steps(2, n)), t)
        its.append(mcq(fig(coins_svg(2, n)) + "Each coin is 2p. How much money?", "%dp" % t,
                       ["%dp" % v for v in (n, t - 2, t + 1)], e))

    pairs(3, "socks")
    seq_next([2, 4, 6, 8], 2, its)
    eyes(4)
    coins(3)
    pairs(4, "shoes")
    seq_next([12, 14, 16], 2, its)
    pairs(5, "socks")
    its.append(mcq("Count in 2s from 0. Which number do you say?", 14, [7, 9, 15],
                   "0, 2, 4, 6, 8, 10, 12, <b>14</b>. When you count in 2s from 0, every number is even. "
                   "7, 9 and 15 are odd."))
    coins(5)
    seq_gap(6, 2, its)
    eyes(6)
    seq_next([20, 18, 16], 2, its, back=True)
    pairs(7, "shoes")
    pairs(9, "socks")
    seq_next([24, 26, 28], 2, its)
    coins(8)
    seq_gap(32, 2, its)
    its.append(mcq("Count in 2s from 0. Which number do you NOT say?", 13, [10, 16, 18],
                   "0, 2, 4, 6, 8, 10, 12, 14, 16, 18. You say 10, 16 and 18. You jump over <b>13</b>."))
    eyes(10)
    seq_next([40, 38, 36], 2, its, back=True)
    assert len(its) == 20, len(its)
    return {"title": "Count in 2s", "items": its}


# ============================================================ set 2: count in 5s
def set_fives(P):
    its = []

    def hands(n):
        t = 5 * n
        e = "Each hand has 5 fingers. Count in 5s: %s. There are <b>%d</b> fingers." % (lst(steps(5, n)), t)
        its.append(mcq(fig(hands_svg(n)) + "How many fingers? Count in 5s.", t, [n, t - 5, t + 1], e))

    def coins(n):
        t = 5 * n
        e = "Each coin is 5p. Count in 5s: %s. That is <b>%dp</b>." % (lst(steps(5, n)), t)
        its.append(mcq(fig(coins_svg(5, n)) + "Each coin is 5p. How much money?", "%dp" % t,
                       ["%dp" % v for v in (n, t - 5, t + 1)], e))

    def flowers(n):
        t = 5 * n
        e = "Each flower has 5 petals. Count in 5s: %s. There are <b>%d</b> petals." % (lst(steps(5, n)), t)
        its.append(mcq(fig(flowers_svg(n)) + "How many petals? Count in 5s.", t, [n, t - 5, t + 1], e))

    hands(2)
    seq_next([5, 10, 15], 5, its)
    coins(3)
    hands(3)
    flowers(4)
    seq_next([30, 35, 40], 5, its)
    coins(4)
    its.append(mcq("Count in 5s from 0. How do the numbers end?", "in 0 or 5", ["only in 5", "only in 0", "in any digit"],
                   "0, 5, 10, 15, 20, 25 … The last digit goes 0, 5, 0, 5. So they always end <b>in 0 or 5</b>."))
    hands(4)
    seq_gap(20, 5, its)
    flowers(5)
    coins(7)
    seq_next([50, 45, 40], 5, its, back=True)
    hands(6)
    seq_next([55, 60, 65], 5, its)
    its.append(mcq("Count in 5s from 0. Which number do you say?", 45, [42, 54, 48],
                   "Counting in 5s, every number ends in 0 or 5. <b>45</b> ends in 5. 42, 54 and 48 do not."))
    coins(9)
    seq_next([80, 85, 90, 95], 5, its)
    its.append(mcq("Count in 5s up to 25. How many 5s do you count?", 5, [25, 4, 6],
                   "Say the numbers: 5, 10, 15, 20, 25. That is <b>5</b> numbers, so there are 5 fives in 25."))
    seq_next([100, 95, 90], 5, its, back=True)
    assert len(its) == 20, len(its)
    return {"title": "Count in 5s", "items": its}


# ============================================================ set 3: count in 10s
def set_tens(P):
    its = []

    def rods(n):
        t = 10 * n
        e = "Each stick has 10 cubes. Count in 10s: %s. There are <b>%d</b> cubes." % (lst(steps(10, n)), t)
        its.append(mcq(fig(rods_svg(n)) + "Each stick has 10 cubes. How many cubes?", t, [n, t - 10, t + 1], e))

    def coins(n):
        t = 10 * n
        e = "Each coin is 10p. Count in 10s: %s. That is <b>%dp</b>." % (lst(steps(10, n)), t)
        its.append(mcq(fig(coins_svg(10, n)) + "Each coin is 10p. How much money?", "%dp" % t,
                       ["%dp" % v for v in (n, t - 10, t + 1)], e))

    def hand_pairs(n):
        t = 10 * n
        e = ("Each child shows 2 hands. That is 10 fingers. Count in 10s: %s. There are <b>%d</b> fingers."
             % (lst(steps(10, n)), t))
        its.append(mcq(fig(hand_pairs_svg(n)) + "How many fingers? Count in 10s.", t, [n, 2 * n, t - 10], e))

    def frames(n):
        t = 10 * n
        e = "A full ten frame has 10 counters. Count in 10s: %s. There are <b>%d</b> counters." % (lst(steps(10, n)), t)
        its.append(mcq(fig(frames_svg(n)) + "Each ten frame is full. How many counters?", t, [n, t - 10, t + 1], e))

    rods(3)
    seq_next([10, 20, 30], 10, its)
    coins(4)
    hand_pairs(2)
    frames(5)
    seq_next([40, 50, 60], 10, its)
    rods(6)
    its.append(mcq("Which one counts in 10s?", "20, 30, 40", ["20, 21, 22", "20, 25, 30", "20, 22, 24"],
                   "Counting in 10s, each number is 10 more: <b>20, 30, 40</b>. "
                   "20, 21, 22 is 1s, 20, 22, 24 is 2s and 20, 25, 30 is 5s."))
    coins(7)
    seq_gap(30, 10, its)
    hand_pairs(3)
    seq_next([90, 80, 70], 10, its, back=True)
    frames(4)
    its.append(mcq("How many 10s make 50?", 5, [50, 10, 6],
                   "Count in 10s: 10, 20, 30, 40, 50. That is <b>5</b> tens."))
    rods(8)
    seq_next([60, 70, 80, 90], 10, its)
    coins(9)
    its.append(mcq("What is 10 more than 40?", 50, [41, 30, 14],
                   "Count on one 10 from 40: <b>50</b>. 41 is only 1 more. 30 is 10 less."))
    seq_next([50, 40, 30], 10, its, back=True)
    its.append(mcq("Count in 10s from 0. Which number do you NOT say?", 45, [40, 70, 90],
                   "0, 10, 20, 30, 40, 50 … Every number ends in 0. <b>45</b> ends in 5, so you do not say it."))
    assert len(its) == 20, len(its)
    return {"title": "Count in 10s", "items": its}


# ============================================================ set 4: equal groups and arrays
def set_groups(P):
    its = []

    def altogether(g, k, kind, lots=False):
        t = g * k
        word = "lots" if lots else "groups"
        e = ("There are %d %s of %d. Count in %ds: %s. That is <b>%d</b> altogether."
             % (g, word, k, k, lst(steps(k, g)), t))
        its.append(mcq(fig(groups_svg(g, k, kind)) + "%d %s of %d. How many %s altogether?" % (g, word, k, NAMES[kind]),
                       t, [g, t - k, g + k, t + 1], e))

    def how_many_groups(g, k, kind):
        e = "Count the circles, not the %s. There are <b>%d</b> groups, with %d in each group." % (NAMES[kind], g, k)
        its.append(mcq(fig(groups_svg(g, k, kind)) + "How many groups are there?", g, [g * k, k, g + 1, g - 1], e))

    def in_each(g, k, kind):
        e = "Look inside one circle. It has <b>%d</b> %s. Every group is the same." % (k, NAMES[kind])
        its.append(mcq(fig(groups_svg(g, k, kind)) + "How many %s are in each group?" % NAMES[kind], k,
                       [g, g * k, k + 1], e))

    def array(r, c, kind):
        t = r * c
        e = ("There are %d rows. Each row has %d. Count in %ds: %s. That is <b>%d</b>."
             % (r, c, c, lst(steps(c, r)), t))
        its.append(mcq(fig(array_svg(r, c, kind)) + "How many %s? Count in %ds." % (NAMES[kind], c),
                       t, [r + c, c, t - c, r, t + 1], e))

    altogether(4, 2, "counter")
    altogether(3, 5, "sweet")
    how_many_groups(5, 2, "apple")
    in_each(2, 5, "star")
    array(2, 5, "counter")
    altogether(2, 10, "counter")
    its.append(abcd_item("Which picture shows 3 groups of 2?", ("groups", [2, 2, 2], "counter"),
                         [("groups", [2, 3, 2], "counter"), ("groups", [3, 3], "counter"),
                          ("groups", [2, 2, 2, 2], "counter")],
                         "<b>{L}</b> has 3 groups, with 2 in each group. Check two things: the number of groups and "
                         "the number in each group.", None))
    array(4, 2, "star")
    altogether(6, 2, "apple")
    altogether(3, 10, "star", lots=True)
    its.append(abcd_item("Which picture shows equal groups?", ("groups", [4, 4, 4], "sweet"),
                         [("groups", [4, 3, 4], "sweet"), ("groups", [4, 4, 5], "sweet"),
                          ("groups", [2, 4, 3], "sweet")],
                         "Equal groups all have the same number. In <b>{L}</b>, every group has 4.", None))
    array(3, 5, "apple")
    altogether(4, 5, "counter")
    how_many_groups(4, 5, "star")
    array(2, 10, "sweet")
    its.append(abcd_item("Which picture shows 2 groups of 5?", ("groups", [5, 5], "apple"),
                         [("groups", [2, 2, 2, 2, 2], "apple"), ("groups", [5, 4], "apple"),
                          ("groups", [5, 5, 5], "apple")],
                         "<b>{L}</b> has 2 groups, with 5 in each group. 5 groups of 2 is not the same picture.", None))
    array(5, 2, "counter")
    altogether(4, 10, "counter", lots=True)
    array(4, 5, "star")
    its.append(abcd_item("Which picture is an array of 3 rows of 2?", ("rows", [2, 2, 2], "counter"),
                         [("rows", [3, 3], "counter"), ("rows", [2, 2, 2, 2], "counter"),
                          ("rows", [2, 1, 2], "counter")],
                         "Rows go across. <b>{L}</b> has 3 rows, and every row has 2.", None))
    assert len(its) == 20, len(its)
    return {"title": "Equal groups and arrays", "items": its}


# ============================================================ set 5: sharing and stories
def set_stories(P):
    its = []

    def share(n, g, who="plates"):
        each = n // g
        assert each * g == n
        e = ("Give 1 to each plate, then again, until none are left. Each plate gets <b>%d</b>. "
             "Check: %s = %d." % (each, " + ".join([str(each)] * g), n))
        q = (fig(share_svg(n, g)) + "Share %d sweets equally between %d plates. How many on each plate?" % (n, g))
        its.append(mcq(q, each, [n, g, each - 1, each + 1], e))

    def story(q, ans, wrong, e, pic=None, unit=""):
        u = (lambda v: "%d%s" % (v, unit)) if unit in ("", "p") else (lambda v: "%d %s" % (v, unit))
        its.append(mcq((fig(pic) if pic else "") + q, u(ans), [u(v) for v in wrong], e))

    def who():
        nm, he, his = P.next()
        return nm, he, his

    share(6, 2)
    share(10, 2)
    share(8, 2)
    its.append(abcd_item("6 sweets are shared between 2 plates. Which one is fair?",
                         ("plates", [3, 3], "sweet"),
                         [("plates", [4, 2], "sweet"), ("plates", [1, 5], "sweet"), ("plates", [6, 0], "sweet")],
                         "Fair means equal. In <b>{L}</b>, both plates have 3. 3 + 3 = 6.", None))
    share(12, 3)
    story("A bike has 2 wheels. How many wheels do 3 bikes have?", 6, [3, 4, 7],
          "Count in 2s for the wheels: 2, 4, 6. There are <b>6</b> wheels.", bikes_svg(3))
    share(20, 2)
    nm, he, his = who()
    story("%s has 4 bags. Each bag has 5 apples. How many apples?" % nm, 20, [4, 15, 9],
          "Count in 5s, one bag at a time: 5, 10, 15, 20. %s has <b>20</b> apples." % nm, groups_svg(4, 5, "apple"))
    share(15, 3)
    story("A box has 10 pencils. How many pencils are in 3 boxes?", 30, [3, 20, 13],
          "Count in 10s: 10, 20, 30. There are <b>30</b> pencils.")
    nm, he, his = who()
    m, mhe, _ = who()
    story("%s shares 10 biscuits with %s. They get the same. How many each?" % (nm, m), 5, [10, 2, 4],
          "Share 10 into 2 equal groups: 5 and 5. They get <b>5</b> each. Check: 5 + 5 = 10.")
    its.append(abcd_item("9 sweets are shared between 3 plates. Which one is fair?",
                         ("plates", [3, 3, 3], "sweet"),
                         [("plates", [4, 3, 2], "sweet"), ("plates", [1, 4, 4], "sweet"), ("plates", [5, 2, 2], "sweet")],
                         "Fair means every plate has the same. In <b>{L}</b>, each plate has 3. 3 + 3 + 3 = 9.", None))
    story("Each child has 2 hands. How many hands do 5 children have?", 10, [5, 8, 11],
          "Count in 2s: 2, 4, 6, 8, 10. 5 children have <b>10</b> hands.")
    nm, he, his = who()
    story("%s has six 5p coins. How much money does %s have?" % (nm, he), 30, [6, 25, 31],
          "Count in 5s six times: 5, 10, 15, 20, 25, 30. That is <b>30p</b>.", unit="p")
    share(16, 2)
    story("5 children sit at each table. There are 4 tables. How many children?", 20, [4, 9, 15],
          "Count in 5s, one table at a time: 5, 10, 15, 20. There are <b>20</b> children.")
    nm, he, his = who()
    story("%s shares 20 stickers equally between 4 friends. How many does each friend get?" % nm, 5, [20, 4, 6],
          "Give 1 to each friend, again and again. Each friend gets <b>5</b>. Check: 5, 10, 15, 20.")
    nm, he, his = who()
    story("%s has 7 pairs of socks. How many socks is that?" % nm, 14, [7, 12, 15],
          "A pair is 2. Count in 2s: 2, 4, 6, 8, 10, 12, 14. That is <b>14</b> socks.", pairs_svg(7, "socks"))
    story("12 children get into groups of 2. How many groups are there?", 6, [12, 2, 5],
          "Count in 2s until you reach 12: 2, 4, 6, 8, 10, 12. That is <b>6</b> groups.", faces_svg(12))
    nm, he, his = who()
    story("%s has 50p in 10p coins. How many coins does %s have?" % (nm, he), 5, [50, 10, 6],
          "Count in 10s up to 50: 10p, 20p, 30p, 40p, 50p. That is <b>5</b> coins.")
    assert len(its) == 20, len(its)
    return {"title": "Sharing and word problems", "items": its}


# ============================================================ balance (and build A-D pictures)
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, right, wrong, _ = it.pop("_abcd")
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
def lesson_share_svg():
    """10 sweets shared between 2 plates: 5 on each."""
    pb, pw, ph = plates_body([5, 5], "sweet", 6, 6)
    return svg_wrap(pw + 12, ph + 12, pb, "10 sweets shared equally on 2 plates, 5 on each")


def body_html():
    return (
        "<h2>Counting in 2s, 5s and 10s</h2>"
        "<p>Some things come in groups. Socks come in 2s. A hand has 5 fingers. "
        "A ten frame holds 10. Count the groups by saying every 2nd, 5th or 10th number. It is faster than counting in 1s.</p>"
        + table(["Count in", "Say", "Think of"], [
            ["2s", "2, 4, 6, 8, 10, 12", "pairs of socks, eyes, 2p coins"],
            ["5s", "5, 10, 15, 20, 25, 30", "fingers on a hand, 5p coins"],
            ["10s", "10, 20, 30, 40, 50, 60", "two hands, 10p coins, tens sticks"],
        ])
        + "<figure class='sn-fig'>" + pairs_svg(4, "socks")
        + "<figcaption>4 pairs of socks: 2, 4, 6, 8. There are 8 socks.</figcaption></figure>"
        + "<figure class='sn-fig'>" + hands_svg(3)
        + "<figcaption>3 hands: 5, 10, 15. There are 15 fingers.</figcaption></figure>"
        + "<figure class='sn-fig'>" + rods_svg(4)
        + "<figcaption>4 tens sticks: 10, 20, 30, 40. There are 40 cubes.</figcaption></figure>"
        + "<h2>Equal groups and arrays</h2>"
        "<p>Equal groups all have the same number. Say “3 groups of 5” or “3 lots of 5”. "
        "Count in 5s to find how many altogether. An <b>array</b> is equal rows. Count a row at a time.</p>"
        + "<figure class='sn-fig'>" + groups_svg(3, 5, "counter")
        + "<figcaption>3 groups of 5: 5, 10, 15. That is 15 altogether.</figcaption></figure>"
        + ex("Example", "How many socks are in 5 pairs?", "Count in 2s: 2, 4, 6, 8, 10.", "10 socks")
        + "<h2>Sharing equally</h2>"
        "<p>To share, give 1 to each, then 1 more to each, until none are left. "
        "Sharing is fair when everyone gets the same.</p>"
        + "<figure class='sn-fig'>" + lesson_share_svg()
        + "<figcaption>Share 10 sweets between 2 plates: 5 on each plate. 5 + 5 = 10.</figcaption></figure>"
        + ex("Example", "Share 12 biscuits equally between 3 children.",
             "Give them out one at a time. Each child gets 4. Check: 4, 8, 12.", "4 biscuits each")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Going back to 1s at the end: 2, 4, 6, 7", "Keep the same jump: 2, 4, 6, 8"],
            ["Missing a group: 4 hands, but only 5, 10, 15", "Touch each group as you count: 5, 10, 15, 20"],
            ["Counting the groups, not the things: 3 pairs = 3 socks", "Each pair is 2: 2, 4, 6 socks"],
            ["Sharing unfairly: 10 sweets as 6 and 4", "Give 1 at a time to each plate: 5 and 5"],
        ])
    )


FAQ = [
    {"q": "When do children learn to count in 2s, 5s and 10s?",
     "a": "In Year 1. The National Curriculum says pupils should count in multiples of twos, fives and tens, and use objects, pictures and arrays to solve simple grouping and sharing problems."},
    {"q": "Do Year 1 children learn times tables?",
     "a": "Not formally. In Year 1 they count in 2s, 5s and 10s and talk about “groups of”. The 2, 5 and 10 times tables, with the × sign, come in Year 2."},
    {"q": "How can I help my child count in 2s, 5s and 10s at home?",
     "a": "Count real things: pairs of socks in 2s, fingers in 5s and 10p coins in 10s. Ask your child to touch each group as they say the number."},
    {"q": "How do you teach sharing equally in Year 1?",
     "a": "Use plates and small objects. Give one to each plate in turn until none are left, then check that every plate has the same number."},
]


def gen():
    rnd = random.Random(1104)
    P = People(rnd)
    sets = [set_twos(P), set_fives(P), set_tens(P), set_groups(P), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "_abcd" not in it and "{" not in it["e"]
            assert it["q"].count("<svg") <= 1, it["q"]
            assert "×" not in it["q"] + it["e"] and "÷" not in it["q"] + it["e"]
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 <= int(tok) <= 110, c
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            # pictures match the numbers they claim
            m = re.search(r"aria-label='(\d+) groups of (\d+) (\w+)'", it["q"])
            if m:
                assert it["q"].count("rx='10' fill='%s'" % FILL) == int(m.group(1))
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "counting-in-2s-5s-and-10s", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Counting in 2s, 5s and 10s",
        "seo_title": "Year 1 Counting in 2s, 5s and 10s Worksheets: Equal Groups and Sharing",
        "short_title": "Counting in 2s, 5s and 10s",
        "domain": "Multiplication and division",
        "standard_code": "Year 1: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count in multiples of twos, fives and tens; solve one-step problems involving multiplication and division, by calculating the answer using concrete objects, pictorial representations and arrays with the support of the teacher.",
        "meta_desc": "Free Year 1 maths worksheets on counting in 2s, 5s and 10s: socks, hands, coins and tens sticks, equal groups, arrays and sharing equally. 100 picture questions with an answer key, following the National Curriculum.",
        "key_big": "Count in equal jumps: 2, 4, 6 … 5, 10, 15 … 10, 20, 30.",
        "key_sub": "3 pairs of socks: 2, 4, 6, so 6 socks. Equal groups all have the same number. To share fairly, give 1 to each until none are left.",
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
