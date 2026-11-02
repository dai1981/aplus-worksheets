# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 1 Math: Equal Groups and Fair Shares (Ontario Mathematics Curriculum 2020)
B2.5 equal groups (total no more than 10, including groups that are a half),
B1.6 fair shares for 2 and 4 sharers with 1 or 2 left over, B1.7 one half = two fourths,
B1.8 more sharers means smaller pieces.
  python3 tools/gen_caon_math_g1_groups_shares.py
Grade 1 (6-7 year olds): very short sentences, a picture in every question, no × or ÷ signs,
fraction words only (a half, a fourth, two fourths), never 1/2 or 1/4.
Wrong answers come from real mistakes: calling unequal groups or unequal parts equal, counting the
groups instead of the things, adding the groups and the things, leaving the leftover out, giving the
leftover to one friend, cutting 1 leftover into halves for 4 friends, and thinking a fourth is bigger
than a half because 4 is more than 2.
Every count, share and area is checked in code. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
PLATE = "#eef6f0"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
PURPLE = "#7b4a9e"
TAN = "#d8a868"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FILL = "#4fae74"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def build_item(build):
    """A-D picture question: build(pos) returns the item with the right picture at pos."""
    return {"build": build}


def balance(sets, rnd):
    """Every set: each answer position (A, B, C, D) is used exactly 5 times."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        out = []
        for it, t in zip(s["items"], targets):
            if "build" in it:
                it = it["build"](t)
                assert it["a"] == t
            else:
                c = it["c"]
                right = c[it["a"]]
                wrong = [x for i, x in enumerate(c) if i != it["a"]]
                rnd.shuffle(wrong)
                it["c"] = wrong[:t] + [right] + wrong[t:]
                it["a"] = t
            out.append(it)
        s["items"] = out


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


def svg_wrap(w, h, body, label, large=False):
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", math.ceil(w), math.ceil(h), math.ceil(w), math.ceil(h),
               label, FONT, body))


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


def adds(a, k):
    return " + ".join([str(a)] * k)


def lst(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def is_wide(w, h):
    return w > 2.2 * h


# ------------------------------------------------------------ small things to count (each one is a <g class='o'>)
def item(kind, cx, cy, r=8.5):
    if kind == "counter":
        s = "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, GREEN)
    elif kind == "apple":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
             % (cx, cy + 1, r * 0.85, RED, cx, cy - r * 0.6, cx + 2, cy - r * 1.1, GREEN))
    elif kind == "grape":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
             "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#ffffff' opacity='0.55'/>"
             % (cx, cy, r * 0.8, PURPLE, cx - r * 0.3, cy - r * 0.3, r * 0.2))
    elif kind == "strawberry":
        s = ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='%s'/>"
             "<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='%s'/>"
             % (cx - r, cy - r * 0.45, cx - r * 0.9, cy + r * 0.6, cx, cy + r * 1.05,
                cx + r * 0.9, cy + r * 0.6, cx + r, cy - r * 0.45, RED,
                cx - r * 0.8, cy - r * 0.5, cx - r * 0.3, cy - r * 1.05, cx, cy - r * 0.7,
                cx + r * 0.3, cy - r * 1.05, cx + r * 0.8, cy - r * 0.5, GREEN))
    elif kind == "cookie":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='#9a6a2a' stroke-width='1.2'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='#6b4a2a'/><circle cx='%.1f' cy='%.1f' r='1.6' fill='#6b4a2a'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='#6b4a2a'/>"
             % (cx, cy, r * 0.9, TAN, cx - 3, cy - 2, cx + 3, cy - 1, cx, cy + 3))
    elif kind == "cracker":
        s = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='#e9c46a' stroke='#b08a2e' stroke-width='1.2'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.2' fill='#b08a2e'/><circle cx='%.1f' cy='%.1f' r='1.2' fill='#b08a2e'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.2' fill='#b08a2e'/><circle cx='%.1f' cy='%.1f' r='1.2' fill='#b08a2e'/>"
             % (cx - r * 0.85, cy - r * 0.85, r * 1.7, r * 1.7, cx - 3, cy - 3, cx + 3, cy - 3, cx - 3, cy + 3, cx + 3, cy + 3))
    elif kind == "mitt":
        s = ("<path d='M %.1f %.1f L %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f L %.1f %.1f Z' fill='%s'/>"
             "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s'/>"
             "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f2f2f2' stroke='%s' stroke-width='1'/>"
             % (cx - r * 0.55, cy + r * 0.7, cx - r * 0.55, cy - r * 0.4, cx - r * 0.55, cy - r, cx, cy - r,
                cx + r * 0.55, cy - r, cx + r * 0.55, cy - r * 0.4, cx + r * 0.55, cy + r * 0.7, BLUE,
                cx - r * 0.7, cy + r * 0.05, r * 0.3, r * 0.45, BLUE,
                cx - r * 0.65, cy + r * 0.6, r * 1.3, r * 0.4, BLUE))
    elif kind == "kid":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#f6dcc0' stroke='#9a6a3a' stroke-width='1.2'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>"
             "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.3'/>"
             % (cx, cy, r * 0.95, cx - r * 0.35, cy - r * 0.2, INK, cx + r * 0.35, cy - r * 0.2, INK,
                cx - r * 0.4, cy + r * 0.3, cx, cy + r * 0.65, cx + r * 0.4, cy + r * 0.3, INK))
    else:
        raise ValueError(kind)
    return "<g class='o'>" + s + "</g>"


NAMES = {"counter": "counters", "apple": "apples", "grape": "grapes", "strawberry": "strawberries",
         "cookie": "cookies", "cracker": "crackers", "mitt": "mitts", "kid": "children"}


def n_items(svg):
    return svg.count("<g class='o'>")


def face(x, y):
    cx, cy = x + 20, y + 20
    return ("<g class='k'><circle cx='%d' cy='%d' r='19' fill='#f6dcc0' stroke='#9a6a3a' stroke-width='1.5'/>"
            "<circle cx='%d' cy='%d' r='3.2' fill='%s'/><circle cx='%d' cy='%d' r='3.2' fill='%s'/>"
            "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='%s' stroke-width='2'/></g>"
            % (cx, cy, cx - 7, cy - 4, INK, cx + 7, cy - 4, INK, cx - 7, cy + 6, cx, cy + 12, cx + 7, cy + 6, INK))


def n_faces(svg):
    return svg.count("<g class='k'>")


# ------------------------------------------------------------ groups (rings or plates)
S = 24


def loose_svg(n, kind):
    M = 5
    el = []
    for i in range(n):
        rr, cc = divmod(i, 5)
        el.append(item(kind, M + cc * S + S / 2.0, M + rr * S + S / 2.0))
    cols = min(n, 5)
    w, h = cols * S + 2 * M, ((n + 4) // 5) * S + 2 * M
    svg = svg_wrap(w, h, "".join(el), "%d %s" % (n, NAMES[kind]), large=is_wide(w, h))
    assert n_items(svg) == n
    return svg


def layout(n):
    if n <= 3:
        return 1, max(n, 1)
    if n <= 6:
        return 2, (n + 1) // 2
    return 2, 5


def groups_body(sizes, x0, y0, kind, style, s, r, per_row, G):
    rows_in, cols_in = layout(max(sizes))
    P = 6
    bw, bh = cols_in * s + 2 * P, rows_in * s + 2 * P
    el = []
    for k, n in enumerate(sizes):
        br, bc = divmod(k, per_row)
        bx, by = x0 + bc * (bw + G), y0 + br * (bh + G)
        if style == "plate":
            el.append("<rect class='p' x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='%s' stroke='%s' "
                      "stroke-width='2.5'/>" % (bx, by, bw, bh, min(bw, bh) / 2.0, PLATE, GREEN))
        else:
            el.append("<rect class='g' x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='12' fill='none' stroke='%s' "
                      "stroke-width='2.5' stroke-dasharray='6 4'/>" % (bx, by, bw, bh, GREY))
        rows_n = 1 if n <= cols_in else 2
        top = by + (bh - rows_n * s) / 2.0
        for i in range(n):
            rr, cc = divmod(i, cols_in)
            in_row = min(cols_in, n - rr * cols_in)
            left = bx + (bw - in_row * s) / 2.0
            el.append(item(kind, left + cc * s + s / 2.0, top + rr * s + s / 2.0, r))
    nrow = (len(sizes) + per_row - 1) // per_row
    ncol = min(len(sizes), per_row)
    return "".join(el), ncol * bw + (ncol - 1) * G, nrow * bh + (nrow - 1) * G


def per_row_for(sizes):
    big = max(sizes)
    lim = 3 if big >= 7 else (4 if big >= 4 else 5)
    if len(sizes) <= lim:
        return len(sizes)
    rows = (len(sizes) + lim - 1) // lim
    return (len(sizes) + rows - 1) // rows


def groups_svg(sizes, kind, style="ring", label=None):
    assert sum(sizes) <= 10, sizes
    M = 5
    body, w, h = groups_body(sizes, M, M, kind, style, S, 8.5, per_row_for(sizes), 12)
    word = "plates" if style == "plate" else "groups"
    if label is None:
        if len(set(sizes)) == 1:
            label = "%d %s of %d %s" % (len(sizes), word, sizes[0], NAMES[kind])
        else:
            label = "%d %s with %s %s" % (len(sizes), word, lst(sizes), NAMES[kind])
    svg = svg_wrap(w + 2 * M, h + 2 * M, body, label, large=is_wide(w + 2 * M, h + 2 * M))
    assert n_items(svg) == sum(sizes)
    assert svg.count("class='%s'" % ("p" if style == "plate" else "g")) == len(sizes)
    return svg


def abcd_groups_svg(panels, kind, style):
    s, r, G, PAD = 18, 6.5, 6, 10
    built = []
    for p in panels:
        assert len(p) <= 5 and sum(p) <= 10
        pr = {4: 2, 5: 3}.get(len(p), len(p))
        built.append(groups_body(p, 0, 0, kind, style, s, r, pr, G))
    PW = max(b[1] for b in built) + 2 * PAD
    H = 30 + max(b[2] for b in built) + 8
    el = []
    for k, (body, w, h) in enumerate(built):
        x0 = k * PW
        if k:
            el.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, x0, H - 4, GREY))
        el.append(text(x0 + 8, 20, "ABCD"[k], 18, "start"))
        el.append("<g transform='translate(%.1f,30)'>%s</g>" % (x0 + (PW - w) / 2.0, body))
    svg = svg_wrap(4 * PW, H, "".join(el), "four pictures labelled A to D", large=True)
    assert n_items(svg) == sum(sum(p) for p in panels)
    return svg


def abcd_groups(prompt, right, wrong, kind, style, e_fn, rnd):
    wrong = [list(w) for w in wrong]
    assert len(wrong) == 3 and right not in wrong and len({tuple(w) for w in wrong}) == 3
    rnd.shuffle(wrong)

    def build(pos):
        panels = wrong[:pos] + [right] + wrong[pos:]
        return {"q": fig(abcd_groups_svg(panels, kind, style)) + prompt, "c": ["A", "B", "C", "D"], "a": pos,
                "e": e_fn("ABCD"[pos])}
    return build_item(build)


# ------------------------------------------------------------ food that can be cut (whole, half, fourth)
CUT = {"cookie": ("cookie", "cookies"), "pancake": ("pancake", "pancakes"), "bar": ("granola bar", "granola bars"),
       "sandwich": ("sandwich", "sandwiches"), "orange": ("orange", "oranges"), "muffin": ("muffin", "muffins")}
CS = 34        # one cell for a piece of food
CR = 13        # radius of round food


def food(kind, cx, cy, part="w"):
    """Whole ('w'), half ('h') or fourth ('f') of a round or square food, centred in a cell at (cx, cy).
    A half keeps the left half; a fourth keeps the top-left quarter."""
    tag = {"w": "o", "h": "hf", "H": "hf", "f": "qf"}[part]
    if kind in ("cookie", "pancake", "orange", "muffin"):
        fill, stroke = {"cookie": (TAN, "#9a6a2a"), "pancake": ("#f0c27a", "#b9822e"),
                        "orange": ("#f5a623", ORANGE), "muffin": ("#b5835a", "#7a5232")}[kind]
        r = CR
        if part == "w":
            s = "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, r, fill, stroke)
        elif part in "hH":
            s = ("<path d='M %.1f %.1f A %d %d 0 0 %d %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.6' "
                 "stroke-linejoin='round'/>" % (cx, cy - r, r, r, 0 if part == "h" else 1, cx, cy + r, fill, stroke))
        else:
            s = ("<path d='M %.1f %.1f L %.1f %.1f A %d %d 0 0 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.6' "
                 "stroke-linejoin='round'/>" % (cx, cy, cx, cy - r, r, r, cx - r, cy, fill, stroke))
        if kind == "cookie":
            dots = {"w": [(-5, -4), (4, -5), (-2, 4), (5, 4)], "h": [(-6, -4), (-5, 5)], "H": [(6, -4), (5, 5)],
                    "f": [(-5, -5)]}[part]
            s += "".join("<circle cx='%.1f' cy='%.1f' r='1.7' fill='#6b4a2a'/>" % (cx + dx, cy + dy) for dx, dy in dots)
        if kind == "pancake" and part == "w":
            s += "<rect x='%.1f' y='%.1f' width='7' height='5' fill='#fff1a8'/>" % (cx - 3.5, cy - 2.5)
    else:
        if kind == "bar":
            W, H, fill, stroke = 28.0, 13.0, "#c8a165", "#8a6a34"
        else:
            W, H, fill, stroke = 24.0, 24.0, "#f3dfb0", "#b08a4a"
        x0, y0 = cx - W / 2, cy - H / 2
        if part == "w":
            w, h = W, H
        elif part == "h":
            w, h = W / 2, H
        elif part == "H":
            x0, w, h = cx, W / 2, H
        else:
            w, h = (W / 4, H) if kind == "bar" else (W / 2, H / 2)
        s = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='1.6'/>"
             % (x0, y0, w, h, fill, stroke))
    return "<g class='%s'>%s</g>" % (tag, s)


def count_parts(svg):
    return svg.count("<g class='o'>"), svg.count("<g class='hf'>"), svg.count("<g class='qf'>")


def share_svg(n, k, kind):
    """n whole foods on top, k children below: still to be shared."""
    M = 5
    per = n if n <= 6 else (n + 1) // 2
    rows = (n + per - 1) // per
    w = per * CS
    fw = k * 46 - 6
    W = max(w, fw) + 2 * M
    ox = (W - w) / 2.0
    el = []
    for i in range(n):
        r, c = divmod(i, per)
        el.append(food(kind, ox + c * CS + CS / 2.0, M + r * CS + CS / 2.0))
    fy = M + rows * CS + 10
    fx = (W - fw) / 2.0
    el += [face(fx + i * 46, fy) for i in range(k)]
    H = fy + 40 + M
    one, many = CUT[kind]
    svg = svg_wrap(W, H, "".join(el), "%d %s to share between %d children" % (n, one if n == 1 else many, k),
                   large=is_wide(W, H))
    assert count_parts(svg) == (n, 0, 0) and n_faces(svg) == k
    return svg


def plates_svg(plates, kind, label, extra=0):
    """Plates with pieces of food. plates: list of strings like 'wwh' (whole, whole, half).
    extra: whole foods still left over, drawn on the right under the words "left over"."""
    k = len(plates)
    per_row = 2 if k == 4 else k
    big = max(len(p) for p in plates)
    P, G, M = 6, 12, 5
    bw, bh = big * CS + 2 * P, CS + 2 * P
    el = []
    for i, p in enumerate(plates):
        r, c = divmod(i, per_row)
        bx, by = M + c * (bw + G), M + r * (bh + G)
        el.append("<rect class='p' x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='%s' stroke='%s' "
                  "stroke-width='2.5'/>" % (bx, by, bw, bh, bh / 2.0, PLATE, GREEN))
        left = bx + (bw - len(p) * CS) / 2.0
        for j, part in enumerate(p):
            el.append(food(kind, left + j * CS + CS / 2.0, by + bh / 2.0, part))
    nrow = (k + per_row - 1) // per_row
    W = 2 * M + per_row * bw + (per_row - 1) * G
    H = 2 * M + nrow * bh + (nrow - 1) * G
    if extra:
        LW = 78
        lx = W + 8
        el.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1' stroke-dasharray='4 3'/>"
                  % (W, W, H - 4, GREY))
        el.append(text(lx + LW / 2.0, M + 16, "left over", 15))
        x0 = lx + (LW - extra * CS) / 2.0
        for j in range(extra):
            el.append(food(kind, x0 + j * CS + CS / 2.0, M + 22 + CS / 2.0))
        W = lx + LW + M
        H = max(H, M + 22 + CS + M)
    svg = svg_wrap(W, H, "".join(el), label, large=is_wide(W, H))
    assert svg.count("class='p'") == k
    want = (sum(p.count("w") for p in plates) + extra, sum(p.count("h") for p in plates), sum(p.count("f") for p in plates))
    assert count_parts(svg) == want
    return svg


def halves_svg(m, kind):
    """m halves of a food in a row: a left half and a right half side by side, then a gap."""
    M = 5
    el = []
    for i in range(m):
        pair, j = divmod(i, 2)
        cx = M + CR + 4 + pair * (2 * CR + 22) + (j * 6)
        el.append(food(kind, cx, M + CR + 2, "h" if j == 0 else "H"))
    pairs = (m + 1) // 2
    W = 2 * M + pairs * (2 * CR + 22) - 22 + 6 + 8
    H = 2 * CR + 4 + 2 * M
    one, many = CUT[kind]
    svg = svg_wrap(W, H, "".join(el), "%d halves of %s" % (m, many), large=is_wide(W, H))
    assert count_parts(svg) == (0, m, 0)
    return svg


# ------------------------------------------------------------ shapes made of exact pieces (halves and fourths)
def poly(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    d = "M" + " L".join("%.1f %.1f" % p for p in pts) + " Z"
    return {"d": d, "area": abs(a) / 2}


def shape(kind, w, h, pieces):
    return {"kind": kind, "w": w, "h": h, "pieces": pieces, "n": len(pieces)}


def r_vstrips(fracs, w=110, h=66, kind="rectangle"):
    assert abs(sum(fracs) - 1) < 1e-9
    ps, x = [], 0.0
    for f in fracs:
        ps.append(poly([(x, 0), (x + f * w, 0), (x + f * w, h), (x, h)]))
        x += f * w
    return shape(kind, w, h, ps)


def r_hstrips(fracs, w=110, h=66, kind="rectangle"):
    assert abs(sum(fracs) - 1) < 1e-9
    ps, y = [], 0.0
    for f in fracs:
        ps.append(poly([(0, y), (w, y), (w, y + f * h), (0, y + f * h)]))
        y += f * h
    return shape(kind, w, h, ps)


def r_grid(w=110, h=66, kind="rectangle"):
    ps = []
    for r in range(2):
        for c in range(2):
            x0, y0 = w * c / 2, h * r / 2
            ps.append(poly([(x0, y0), (x0 + w / 2, y0), (x0 + w / 2, y0 + h / 2), (x0, y0 + h / 2)]))
    return shape(kind, w, h, ps)


def r_diag(w=80, h=80, kind="square"):
    return shape(kind, w, h, [poly([(0, 0), (w, 0), (w, h)]), poly([(0, 0), (w, h), (0, h)])])


def r_x(w=80, h=80, kind="square"):
    c = (w / 2, h / 2)
    return shape(kind, w, h, [poly([(0, 0), (w, 0), c]), poly([(w, 0), (w, h), c]),
                              poly([(w, h), (0, h), c]), poly([(0, h), (0, 0), c])])


def r_cross(fx, fy, w=110, h=66, kind="rectangle"):
    X, Y = fx * w, fy * h
    return shape(kind, w, h, [poly([(0, 0), (X, 0), (X, Y), (0, Y)]), poly([(X, 0), (w, 0), (w, Y), (X, Y)]),
                              poly([(0, Y), (X, Y), (X, h), (0, h)]), poly([(X, Y), (w, Y), (w, h), (X, h)])])


def sq(fn, *a, s=80):
    return fn(*a, w=s, h=s, kind="square")


def c_sectors(angles, r=40, start=0):
    assert abs(sum(angles) - 360) < 1e-9 and len(angles) > 1
    ps, a0 = [], float(start)
    for a in angles:
        a1 = a0 + a
        t0, t1 = math.radians(a0 - 90), math.radians(a1 - 90)
        x0, y0 = r + r * math.cos(t0), r + r * math.sin(t0)
        x1, y1 = r + r * math.cos(t1), r + r * math.sin(t1)
        d = "M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" % (r, r, x0, y0, r, r, 1 if a > 180 else 0, x1, y1)
        ps.append({"d": d, "area": math.pi * r * r * a / 360.0})
        a0 = a1
    return shape("circle", 2 * r, 2 * r, ps)


def c_chord(off, r=40):
    """Circle cut by one up-and-down line at x = off * r from the centre."""
    def left_area(d):
        return r * r * (math.acos(-d) + d * math.sqrt(1 - d * d))
    k = r * math.sqrt(1 - off * off)
    tx, ty, bx, by = r + off * r, r - k, r + off * r, r + k
    d1 = "M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z" % (tx, ty, r, r, 1 if off > 0 else 0, bx, by)
    d2 = "M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" % (tx, ty, r, r, 1 if off < 0 else 0, bx, by)
    return shape("circle", 2 * r, 2 * r, [{"d": d1, "area": left_area(off)},
                                          {"d": d2, "area": math.pi * r * r - left_area(off)}])


def is_equal(sh):
    a = [p["area"] for p in sh["pieces"]]
    return max(a) - min(a) < 1e-6 * max(a)


def EQ(sh):
    assert is_equal(sh), [p["area"] for p in sh["pieces"]]
    return sh


def UN(sh):
    a = [p["area"] for p in sh["pieces"]]
    assert max(a) / min(a) >= 1.4, ("not visibly unequal", a)
    return sh


def draw(sh, shaded=(), ox=0, oy=0):
    s = []
    for i, p in enumerate(sh["pieces"]):
        s.append("<path transform='translate(%.1f %.1f)' d='%s' fill='%s' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (ox, oy, p["d"], FILL if i in shaded else "#fff", INK))
    return "".join(s)


def shaded_area(sh, shaded):
    tot = sum(p["area"] for p in sh["pieces"])
    return sum(sh["pieces"][i]["area"] for i in shaded) / tot


def one_svg(sh, shaded=(), label=None):
    pad = 5
    lab = label or "%s cut into %d pieces%s" % (sh["kind"], sh["n"], ", %d shaded" % len(shaded) if shaded else "")
    return svg_wrap(sh["w"] + 2 * pad, sh["h"] + 2 * pad, draw(sh, shaded, pad, pad), lab)


def panel_svg(shapes, label, letters="ABCD", cols=2):
    n = len(shapes)
    cw = max(s["w"] for s, _ in shapes)
    ch = max(s["h"] for s, _ in shapes)
    LW, gap, pad = 24, 18, 6
    rws = (n + cols - 1) // cols
    W = pad + cols * (LW + cw) + (cols - 1) * gap + pad
    H = pad + rws * ch + (rws - 1) * gap + pad
    s = []
    for i, (sh, shaded) in enumerate(shapes):
        r, c = divmod(i, cols)
        x0 = pad + c * (LW + cw + gap)
        y0 = pad + r * (ch + gap)
        s.append(text(x0, y0 + 17, letters[i], 20, "start"))
        s.append(draw(sh, shaded, x0 + LW + (cw - sh["w"]) / 2, y0 + (ch - sh["h"]) / 2))
    return svg_wrap(W, H, "".join(s), label)


def labeled_row(shapes, labels, label, gap=30):
    pad = 6
    cw = max(max(s["w"] for s, _ in shapes), 8.6 * max(len(t) for t in labels))
    ch = max(s["h"] for s, _ in shapes)
    W = pad * 2 + len(shapes) * cw + (len(shapes) - 1) * gap
    H = pad * 2 + ch + 26
    s = []
    for i, ((sh, shaded), t) in enumerate(zip(shapes, labels)):
        x0 = pad + i * (cw + gap)
        s.append(draw(sh, shaded, x0 + (cw - sh["w"]) / 2, pad + (ch - sh["h"]) / 2))
        s.append(text(x0 + cw / 2, pad + ch + 20, t, 16))
    return svg_wrap(W, H, "".join(s), label, large=is_wide(W, H))


def abcd_shapes(good, bads, question, label, e_fn, rnd):
    bads = bads[:]
    rnd.shuffle(bads)

    def build(pos):
        shapes = bads[:pos] + [good] + bads[pos:]
        return {"q": fig(panel_svg(shapes, label)) + question, "c": ["A", "B", "C", "D"], "a": pos,
                "e": e_fn("ABCD"[pos])}
    return build_item(build)


# ------------------------------------------------------------ fair share words
def each_gets(n, k):
    """Words for one share of n things between k children: '2 and a half', '1 and a fourth'."""
    w, r = divmod(n, k)
    if r == 0:
        return str(w)
    part = {(2, 1): "a half", (4, 2): "a half", (4, 1): "a fourth"}[(k, r)]
    return "%d and %s" % (w, part) if w else part


def share_plates(n, k):
    """The fair share on k plates, as plate strings."""
    w, r = divmod(n, k)
    if r == 0:
        return ["w" * w] * k
    return ["w" * w + ("f" if (k, r) == (4, 1) else "h")] * k


# ============================================================ set 1: equal or not equal groups
def set_equal(P, rnd):
    its = []
    for sizes, kd in [([2, 2, 2], "apple"), ([4, 3], "grape"), ([5, 5], "strawberry"), ([2, 3, 2], "cookie"),
                      ([2, 2, 2, 2], "counter"), ([3, 3], "cracker"), ([3, 4, 3], "apple")]:
        n, k = sum(sizes), len(sizes)
        if len(set(sizes)) == 1:
            a = sizes[0]
            right = "Yes, %d in each" % a
            e = "Every group has %d. They are all the same, so the groups are <b>equal</b>." % a
            w = ["Yes, %d in each" % k, "Yes, %d in each" % n, "No, not equal"]
        else:
            right = "No, not equal"
            e = ("The groups have %s. They are not all the same, so they are <b>not equal</b>." % lst(sizes))
            w = ["Yes, %d in each" % max(sizes), "Yes, %d in each" % min(sizes), "Yes, %d in each" % n]
        its.append(mcq(fig(groups_svg(sizes, kd)) + "Are these groups equal?", right, w, e))

    for n, k, kd, wrong in [(8, 2, "apple", [[5, 3], [6, 2], [2, 2, 2, 2]]),
                            (6, 3, "strawberry", [[3, 2, 1], [4, 1, 1], [3, 3]]),
                            (10, 2, "grape", [[6, 4], [7, 3], [2, 2, 2, 2, 2]]),
                            (9, 3, "counter", [[4, 3, 2], [4, 4, 1], [5, 4]]),
                            (8, 4, "cookie", [[4, 4], [3, 2, 2, 1], [3, 3, 2]])]:
        a = n // k
        assert all(sum(w) == n for w in wrong)
        e = (lambda k, a: lambda L: "<b>%s</b> has %d groups with %d in each. Check two things: the right number of "
             "groups, and the same number in every group." % (L, k, a))(k, a)
        its.append(abcd_groups("Which shows %d %s in %d equal groups?" % (n, NAMES[kd], k), [a] * k, wrong, kd,
                               "ring", e, rnd))

    for right, wrong, kd in [([4, 3], [[2, 2], [5, 5], [3, 3]], "apple"),
                             ([2, 3, 2], [[3, 3, 3], [2, 2, 2], [1, 1, 1]], "grape"),
                             ([2, 2, 1, 2], [[2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2]], "cracker")]:
        assert all(len(set(w)) == 1 for w in wrong) and len(set(right)) > 1
        e = (lambda right: lambda L: "<b>%s</b> has %s. One group is different, so it is not equal. "
             "In the other pictures every group has the same number." % (L, lst(right)))(right)
        its.append(abcd_groups("Which groups are <b>not</b> equal?", right, wrong, kd, "ring", e, rnd))

    for sizes, kd in [([5, 3], "grape"), ([4, 2], "strawberry"), ([6, 2], "apple"), ([7, 3], "counter")]:
        big, small = sizes
        mv = (big - small) // 2
        a = (big + small) // 2
        one = NAMES[kd] if mv > 1 else {"strawberries": "strawberry"}.get(NAMES[kd], NAMES[kd][:-1])
        e = ("%d and %d make %d. Equal is %d and %d. Move <b>%d</b> %s from the %d to the %d. "
             "(Moving %d gives %d and %d. That is still not equal.)"
             % (big, small, big + small, a, a, mv, one, big, small, big - small, small, big))
        its.append(mcq(fig(groups_svg(sizes, kd, "plate")) +
                       "Make the 2 plates equal. How many %s must move?" % NAMES[kd],
                       mv, [big - small, a, mv + 1, small, big], e))

    n1, he1, _ = P.next()
    n2, _, _ = P.next()
    its.append(mcq(fig(groups_svg([5, 3], "cracker", "plate")) +
                   "%s and %s share 8 crackers. %s gets 5. %s gets 3. Is it fair?" % (n1, n2, n1, n2),
                   "No, %s has more" % n1, ["Yes, it makes 8", "No, %s has more" % n2, "Yes, both get 5"],
                   "5 and 3 are not the same. <b>%s has more.</b> It is not fair. Fair is 4 each." % n1))
    assert len(its) == 20, len(its)
    return {"title": "Equal or not equal groups?", "items": its}


# ============================================================ set 2: how many in all?
def set_total(P, rnd):
    its = []
    for g, n, kd in [(2, 4, "apple"), (3, 2, "strawberry"), (2, 5, "counter"), (4, 2, "cookie"),
                     (3, 3, "grape"), (5, 2, "cracker"), (2, 3, "apple")]:
        t = g * n
        assert t <= 10
        e = ("There are %d groups of %d. Add: %s = <b>%d</b>. (%d is the number of groups.)"
             % (g, n, adds(n, g), t, g))
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are there in all?" % NAMES[kd],
                       t, [g, g + n, t + 1, t - 1, n], e))
    for g, n, kd in [(2, 2, "strawberry"), (3, 3, "cookie"), (2, 4, "cracker"), (5, 2, "grape")]:
        t = g * n
        e = ("Each plate has %d. There are %d plates. %s = <b>%d</b>. (Not %d: that is just the plates.)"
             % (n, g, adds(n, g), t, g))
        its.append(mcq(fig(groups_svg([n] * g, kd, "plate")) +
                       "Each plate has %d %s. How many %s in all?" % (n, NAMES[kd], NAMES[kd]),
                       t, [g, g + n, t + 1, t - 1, n], e))
    for g, n, kd in [(3, 2, "counter"), (2, 5, "apple"), (4, 2, "grape")]:
        right = "%d groups of %d" % (g, n)
        e = "Count the rings: %d. Count in one ring: %d. So it is <b>%s</b>. That is %d in all." % (g, n, right, g * n)
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which words match the picture?", right,
                       ["%d groups of %d" % (n, g), "%d groups of %d" % (g, n + 1), "%d groups of %d" % (g + 1, n)], e))
    for t, g, kd in [(8, 2, "counter"), (10, 2, "strawberry")]:
        a = t // g
        e = ("Give one to each group, again and again, until none are left. Each group gets <b>%d</b>. "
             "Check: %s = %d." % (a, adds(a, g), t))
        its.append(mcq(fig(loose_svg(t, kd)) + "Put the %d %s in %d equal groups. How many in each group?"
                       % (t, NAMES[kd], g), a, [g, t, a + 1, t - g, a - 1], e))
    # each group is a half
    for m, kd, who in [(4, "orange", "4 children each get half an orange."),
                       (6, "sandwich", "6 children each get half a sandwich."),
                       (10, "muffin", "10 children each get half a muffin."),
                       (8, "pancake", "8 children each get half a pancake.")]:
        one, many = CUT[kd]
        a = m // 2
        unit = one if a == 1 else many
        e = ("2 halves make 1 whole %s. Make pairs of halves: there are <b>%d</b>. So that is %d %s."
             % (one, a, a, unit))
        its.append(mcq(fig(halves_svg(m, kd)) + "%s How many whole %s is that?" % (who, many),
                       "%d %s" % (a, unit), ["%d %s" % (x, one if x == 1 else many) for x in [m, a + 1, m * 2, m - 1]],
                       e))
    assert len(its) == 20, len(its)
    return {"title": "How many in all?", "items": its}


# ============================================================ set 3: fair shares with leftovers
def set_leftover(P, rnd):
    its = []
    for n, k, kd in [(5, 2, "cookie"), (7, 2, "bar"), (6, 4, "pancake"), (9, 4, "muffin")]:
        one, many = CUT[kd]
        w, r = divmod(n, k)
        e = ("Give out whole %s, one to each child, again and again. Each child gets %d. That uses %d. "
             "%d − %d = <b>%d</b> left over." % (many, w, w * k, n, w * k, r))
        its.append(mcq(fig(share_svg(n, k, kd)) + "%d children share %d %s. Each gets the same number of whole %s. "
                       "How many are left over?" % (k, n, many, many), r, [0, w, r + 1, w + 1, k], e))
    for n, k, kd in [(9, 2, "cookie"), (7, 2, "sandwich"), (10, 4, "bar"), (5, 4, "orange")]:
        one, many = CUT[kd]
        w, r = divmod(n, k)
        e = ("Give one to each child, again and again. Each child gets <b>%d</b> whole %s, and %d %s left over. "
             "(%d each would need %d %s.)" % (w, one if w == 1 else many, r, "is" if r == 1 else "are",
                                               w + 1, (w + 1) * k, many))
        its.append(mcq(fig(share_svg(n, k, kd)) + "Share %d %s between %d children. How many <b>whole</b> %s "
                       "does each child get?" % (n, many, k, many), w, [w + 1, n, r, k, w - 1 or None], e))
    for n, k, kd in [(5, 2, "pancake"), (7, 2, "cookie"), (3, 2, "bar"), (6, 4, "sandwich"), (10, 4, "muffin"),
                     (5, 4, "cookie"), (9, 4, "pancake")]:
        one, many = CUT[kd]
        w, r = divmod(n, k)
        right = each_gets(n, k)
        if k == 2:
            e = ("Each child gets %d whole. 1 is left over. Cut it into <b>halves</b>. Each child gets a half. "
                 "So each gets <b>%s</b> %s." % (w, right, many))
            cands = [str(w), str(w + 1), "%d and a fourth" % w]
        elif r == 2:
            e = ("Each child gets %d whole. 2 are left over. Cut each one into <b>halves</b>. That makes 4 halves, "
                 "one for each child. So each gets <b>%s</b> %s." % (w, right, many))
            cands = [str(w), "%d and a fourth" % w, str(w + 1)]
        else:
            e = ("Each child gets %d whole. 1 is left over. 4 children need 4 pieces, so cut it into <b>fourths</b>. "
                 "Each gets a fourth. So each gets <b>%s</b> %s." % (w, right, many))
            cands = ["%d and a half" % w, str(w), str(w + 1)]
        its.append(mcq(fig(share_svg(n, k, kd)) + "%d children share %d %s fairly. How much does each child get?"
                       % (k, n, many), right, cands, e))
    left_q = [
        (5, 2, "cookie", "Cut it into halves",
         ["Cut it into fourths", "Give it to 1 child", "Put it away"],
         "2 children need 2 equal pieces. Cut the last cookie into <b>halves</b>. Each child gets a half. "
         "All the cookies are shared."),
        (5, 4, "bar", "Cut it into fourths",
         ["Cut it into halves", "Give it to 1 child", "Put it away"],
         "4 children need 4 equal pieces. Cut the last granola bar into <b>fourths</b>. "
         "Halves make only 2 pieces."),
        (6, 4, "pancake", "Cut each in half",
         ["Cut one in half", "Give them to 2", "Put them away"],
         "2 are left and 4 children wait. Cut <b>each one in half</b>. That makes 4 halves: one for each child."),
    ]
    for n, k, kd, right, wrong, e in left_q:
        one, many = CUT[kd]
        w, r = divmod(n, k)
        q = ("%d %s for %d children. Each child has %d. %d %s left over. What is fair?"
             % (n, many, k, w, r, "is" if r == 1 else "are"))
        its.append(mcq(fig(plates_svg(["w" * w] * k, kd, "%d plates with %d whole %s each and %d left over"
                                      % (k, w, one if w == 1 else many, r), extra=r))
                       + q,
                       right, wrong, e))
    nm, he, _ = P.next()
    its.append(mcq(fig(plates_svg(["wwh", "wwh"], "cookie", "2 plates with 2 and a half cookies each")) +
                   "%s shares 5 cookies with 1 friend like this. Is it fair?" % nm,
                   "Yes, the same", ["No, one has more", "No, 1 is left", "Yes, 5 each"],
                   "Each plate has 2 cookies and a half. Both are <b>the same</b>, and all 5 cookies are shared. "
                   "It is fair."))
    nm, he, _ = P.next()
    its.append(mcq(fig(plates_svg(["ww", "w", "w", "w"], "muffin", "4 plates with 2, 1, 1 and 1 muffins")) +
                   "%s shares 5 muffins with 3 friends like this. Is it fair?" % nm,
                   "No, one has more", ["Yes, the same", "Yes, all shared", "No, 1 is left"],
                   "One plate has 2 muffins. The others have 1. <b>One has more</b>, so it is not fair. "
                   "Fair is to cut the last muffin into fourths: 1 and a fourth each."))
    assert len(its) == 20, len(its)
    return {"title": "Fair shares with leftovers", "items": its}


# ============================================================ set 4: halves and fourths
def set_parts(P, rnd):
    its = []
    for sh, want in [(EQ(c_sectors([180, 180])), 2), (UN(r_vstrips([.3, .7])), 2), (EQ(sq(r_diag)), 2),
                     (EQ(r_grid()), 4), (UN(r_cross(.3, .35)), 4)]:
        n = sh["n"]
        noun = sh["kind"]
        W = "halves" if want == 2 else "fourths"
        if not is_equal(sh):
            right = "No, not equal"
            e = "There are %d pieces, but they are <b>not the same size</b>. %s must be equal." % (n, cap(W))
            cands = ["Yes, %d pieces" % n, "Yes, %s" % W, "Yes, %d cut%s" % (n // 2, "s" if n > 2 else "")]
        else:
            right = "Yes, %s" % W
            e = "There are <b>%d equal pieces</b>. %d equal pieces are %s." % (n, n, W)
            cands = ["No, not equal", "No, %s" % ("fourths" if want == 2 else "halves"),
                     "No, only 1 line" if want == 2 else "No, only 2 lines"]
        its.append(mcq(fig(one_svg(sh)) + "Is this %s cut into %s?" % (noun, W), right, cands, e))

    def which(n, good, bads):
        W = "halves" if n == 2 else "fourths"
        e = (lambda W, n: lambda L: "Shape <b>%s</b> has %d pieces that are the <b>same size</b>. "
             "That is %s." % (L, n, W))(W, n)
        return abcd_shapes((good, ()), [(b, ()) for b in bads], "Which shape shows <b>%s</b>?" % W,
                           "four shapes A to D", e, rnd)
    its.append(which(2, EQ(c_sectors([180, 180], start=90)),
                     [UN(c_chord(-0.45)), EQ(c_sectors([90] * 4)), UN(c_sectors([240, 120]))]))
    its.append(which(2, EQ(r_hstrips([.5, .5], h=60)),
                     [UN(r_hstrips([.3, .7], h=60)), EQ(r_grid(h=60)), UN(r_vstrips([.65, .35], h=60))]))
    its.append(which(4, EQ(c_sectors([90] * 4, start=45)),
                     [UN(c_sectors([140, 50, 100, 70])), EQ(c_sectors([180, 180])), UN(c_sectors([120, 60, 120, 60]))]))
    its.append(which(4, EQ(r_vstrips([.25] * 4, h=60)),
                     [UN(r_vstrips([.15, .35, .2, .3], h=60)), EQ(r_vstrips([.5, .5], h=60)), UN(r_cross(.3, .35, h=60))]))

    # what part is shaded?
    for sh, shd, right, cands in [
            (EQ(r_vstrips([.5, .5])), (0,), "one half", ["one fourth", "two halves", "two fourths"]),
            (EQ(c_sectors([90] * 4)), (1,), "one fourth", ["one half", "four fourths", "two fourths"]),
            (EQ(sq(r_grid)), (0, 1), "two fourths", ["one fourth", "two halves", "four fourths"]),
            (EQ(sq(r_x)), (3,), "one fourth", ["one half", "two fourths", "four halves"])]:
        k, n = len(shd), sh["n"]
        e = ("The %s has <b>%d equal pieces</b>. %d %s shaded. So <b>%s</b> is shaded."
             % (sh["kind"], n, k, "is" if k == 1 else "are", right))
        if right == "two fourths":
            e += " Two fourths is the same as one half."
        its.append(mcq(fig(one_svg(sh, shd)) + "What part of the %s is shaded?" % sh["kind"], right, cands, e))

    # one half = two fourths
    a, b = EQ(c_sectors([180, 180], start=90)), EQ(c_sectors([90] * 4))
    assert abs(shaded_area(a, (0,)) - shaded_area(b, (0, 1))) < 1e-9
    its.append(mcq(fig(panel_svg([(a, (0,)), (b, (0, 1))], "two same-size circles A and B", letters="AB")) +
                   "A shows one half. B shows two fourths. Which is more?", "They are the same",
                   ["A is more", "B is more", "You cannot tell"],
                   "Both circles are the same size. The shaded parts cover the same space. "
                   "<b>Two fourths is the same as one half.</b>"))
    sh = EQ(r_grid())
    its.append(mcq(fig(one_svg(sh, (0, 2), "rectangle cut into 4 equal pieces, 2 shaded")) +
                   "How many fourths make one half?", "2", ["1", "4", "3"],
                   "The shaded part is one half of the rectangle. It is <b>2 fourths</b>."))
    sh = EQ(sq(r_vstrips, [.5, .5]))
    its.append(mcq(fig(one_svg(sh, (0,), "square cut into 2 equal pieces, 1 shaded")) +
                   "Cut each half of this square into 2 equal pieces. What is the shaded part now?", "two fourths",
                   ["two halves", "one fourth", "four fourths"],
                   "Cut each half of the square in 2 and the square has 4 equal pieces. "
                   "The shaded half becomes <b>two fourths</b>."))

    def same_as_half(good, bads, e_extra):
        e = (lambda L: "Shape <b>%s</b> has 4 equal pieces and 2 are shaded: two fourths. "
             "Two fourths is the same as one half. %s" % (L, e_extra))
        return abcd_shapes(good, bads, "Which shape has <b>one half</b> shaded?", "four shapes A to D with shading",
                           e, rnd)
    its.append(same_as_half((EQ(r_grid(h=60)), (0, 1)),
                            [(EQ(r_grid(h=60)), (0,)), (EQ(r_grid(h=60)), (0, 1, 2)), (UN(r_vstrips([.3, .7], h=60)), (0,))],
                            "One fourth is too little. Three fourths is too much."))
    its.append(same_as_half((EQ(c_sectors([90] * 4)), (2, 3)),
                            [(EQ(c_sectors([90] * 4)), (3,)), (UN(c_sectors([240, 120])), (1,)),
                             (EQ(c_sectors([90] * 4)), (0, 1, 2))],
                            "A small piece of 2 pieces is not a half."))
    sh = EQ(c_sectors([90] * 4))
    its.append(mcq(fig(one_svg(sh, (0, 1, 2, 3), "circle cut into 4 equal pieces, all shaded")) +
                   "How many fourths make the whole circle?", "4", ["2", "1", "3"],
                   "The circle has 4 equal pieces. All are shaded. <b>4 fourths</b> make the whole."))
    sh = EQ(r_vstrips([.5, .5]))
    its.append(mcq(fig(one_svg(sh, (0, 1), "rectangle cut into 2 equal pieces, both shaded")) +
                   "How many halves make the whole rectangle?", "2", ["1", "4", "3"],
                   "The rectangle has 2 equal pieces. Both are shaded. <b>2 halves</b> make the whole."))
    assert len(its) == 20, len(its)
    return {"title": "Halves and fourths", "items": its}


# ============================================================ set 5: more sharers, smaller pieces; stories
def set_story(P, rnd):
    its = []
    SAME, A_BIG, B_BIG = "Same size", "A is bigger", "B is bigger"
    for a, sa, b, sb, right, e in [
        (EQ(c_sectors([180, 180])), (0,), EQ(c_sectors([90] * 4)), (1,), A_BIG,
         "A is cut into halves: 2 pieces. B is cut into fourths: 4 pieces. More pieces means smaller pieces. "
         "So <b>A is bigger</b>."),
        (EQ(r_grid(w=100, h=60)), (2,), EQ(r_vstrips([.5, .5], w=100, h=60)), (0,), B_BIG,
         "A is cut into fourths. B is cut into halves. A half is bigger than a fourth, so <b>B is bigger</b>."),
        (EQ(sq(r_x)), (0,), EQ(sq(r_grid)), (3,), SAME,
         "Both squares are cut into fourths. A triangle fourth and a square fourth of the same square are the "
         "<b>same size</b>."),
    ]:
        its.append(mcq(fig(panel_svg([(a, sa), (b, sb)], "same-size shapes A and B, one piece shaded in each",
                                     letters="AB")) +
                       "A and B are the same size. Which shaded piece is bigger?", right,
                       [SAME, A_BIG, B_BIG, "You cannot tell"], e))

    def row(shapes, labels, lab):
        return fig(labeled_row(shapes, labels, lab))

    nm1, _, _ = P.next()
    nm2, _, _ = P.next()
    its.append(mcq(row([(EQ(c_sectors([180, 180])), (0,)), (EQ(c_sectors([90] * 4)), (0,))], [nm1, nm2],
                       "two same-size pizzas, one in halves and one in fourths") +
                   "%s shares a pizza with 1 friend. %s shares the same size pizza with 3 friends. "
                   "Who gets a bigger piece?" % (nm1, nm2),
                   nm1, [nm2, "The same", "You cannot tell"],
                   "%s’s pizza is cut into 2 pieces: halves. %s’s is cut into 4 pieces: fourths. "
                   "Fewer sharers means bigger pieces. <b>%s</b> gets more." % (nm1, nm2, nm1)))
    nm1, _, _ = P.next()
    nm2, _, _ = P.next()
    its.append(mcq(row([(EQ(c_sectors([180, 180], start=90)), ()), (EQ(c_sectors([90] * 4, start=45)), ())],
                       [nm1, nm2], "two same-size pancakes, one in halves and one in fourths") +
                   "It is a snow day! %s cuts a pancake into halves. %s cuts the same size pancake into fourths. "
                   "Whose pieces are bigger?" % (nm1, nm2),
                   "%s’s" % nm1, ["%s’s" % nm2, "The same", "You cannot tell"],
                   "Halves are 2 pieces. Fourths are 4 pieces. More pieces means smaller pieces. "
                   "<b>%s’s</b> pieces are bigger." % nm1))
    nm, he, _ = P.next()
    its.append(mcq(fig(one_svg(EQ(r_vstrips([.5, .5], w=120, h=40)), (), "granola bar cut into 2 equal pieces")) +
                   "At recess, %s shares a granola bar fairly with 1 friend. What does each get?" % nm,
                   "a half", ["a fourth", "the whole bar", "two halves"],
                   "%s and 1 friend are <b>2 children</b>. 2 equal pieces are halves. Each gets <b>a half</b>." % nm))
    nm, he, _ = P.next()
    its.append(mcq(fig(one_svg(EQ(sq(r_grid)), (), "sandwich cut into 4 equal pieces")) +
                   "At lunch, %s shares a sandwich fairly with 3 friends. What does each get?" % nm,
                   "a fourth", ["a half", "the whole", "3 pieces"],
                   "%s and 3 friends are <b>4 children</b>. 4 equal pieces are fourths. Each gets <b>a fourth</b>. "
                   "Do not forget to count %s." % (nm, nm)))
    nm1, _, _ = P.next()
    nm2, _, _ = P.next()
    its.append(mcq(row([(EQ(c_sectors([90] * 4)), (0, 1)), (EQ(c_sectors([180, 180], start=90)), (1,))],
                       [nm1, nm2], "two same-size pies, two fourths and one half shaded") +
                   "On Thanksgiving, %s eats two fourths of a pumpkin pie. %s eats one half of the same size pie. "
                   "Who eats more?" % (nm1, nm2), "The same", [nm1, nm2, "You cannot tell"],
                   "Two fourths is the same as one half. They eat <b>the same</b> amount."))
    its.append(mcq(row([(EQ(r_vstrips([.5, .5], w=100, h=56)), ()), (EQ(r_vstrips([.25] * 4, w=100, h=56)), ())],
                       ["2 people", "4 people"], "the same cake cut for 2 people and for 4 people") +
                   "More people share the same cake. What happens to each piece?", "It gets smaller",
                   ["It gets bigger", "It stays the same", "The cake grows"],
                   "The cake does not change. More people means more pieces, so each piece is <b>smaller</b>."))
    nm, he, _ = P.next()
    its.append(mcq(row([(EQ(c_sectors([180, 180])), (0,)), (EQ(c_sectors([90] * 4)), (0,))],
                       ["a half", "a fourth"], "a half and a fourth of two same-size circles") +
                   "%s says, “A fourth is bigger than a half, because 4 is more than 2.” Is %s right?" % (nm, he),
                   "No, a half is bigger", ["Yes, 4 is more", "No, they are the same", "Yes, a fourth is bigger"],
                   "4 pieces are smaller than 2 pieces of the same thing. <b>A half is bigger</b> than a fourth."))
    nm, he, his = P.next()
    its.append(mcq(fig(one_svg(UN(sq(r_vstrips, [.3, .7])), (), "toast cut into a small piece and a big piece")) +
                   "%s cuts %s toast like this. Did %s cut it in half?" % (nm, his, he),
                   "No, not equal", ["Yes, 2 pieces", "Yes, 1 cut", "No, fourths"],
                   "Halves must be the <b>same size</b>. One piece is big and one is small, so they are not halves."))
    nm, he, _ = P.next()
    its.append(mcq(fig(share_svg(3, 2, "bar")) +
                   "%s shares 3 granola bars fairly with 1 friend. How much does each get?" % nm,
                   "1 and a half", ["1", "2", "1 and a fourth"],
                   "Each gets 1 whole bar. 1 is left over. Cut it into halves. Each gets <b>1 and a half</b> bars."))
    its.append(mcq(fig(share_svg(2, 4, "orange")) +
                   "At the cottage, 4 friends share 2 oranges fairly. How much does each get?",
                   "a half", ["a fourth", "1 orange", "2 oranges"],
                   "There are fewer oranges than friends. Cut each orange into halves. That makes 4 halves. "
                   "Each friend gets <b>a half</b>."))
    its.append(mcq(fig(share_svg(6, 4, "cookie")) +
                   "At the skating rink, 4 friends share 6 cookies fairly. How much does each get?",
                   "1 and a half", ["1", "1 and a fourth", "2"],
                   "Each friend gets 1 whole cookie. 2 are left over. Cut each one into halves. That makes 4 halves, "
                   "one for each friend. Each gets <b>1 and a half</b> cookies."))
    its.append(mcq(fig(groups_svg([2, 2, 2, 2], "kid", label="4 canoes with 2 children each")) +
                   "On a canoe trip, 2 children sit in each canoe. There are 4 canoes. How many children?",
                   8, [4, 6, 2, 10],
                   "4 groups of 2: 2 + 2 + 2 + 2 = <b>8</b> children. (4 is the number of canoes.)"))
    nm, he, _ = P.next()
    its.append(mcq(fig(groups_svg([3, 3, 3], "cookie", "plate")) +
                   "%s gives 3 maple cookies to each of 3 friends. How many cookies is that?" % nm,
                   9, [3, 6, 12, 10],
                   "3 groups of 3: 3 + 3 + 3 = <b>9</b> cookies."))
    nm, he, _ = P.next()
    its.append(mcq(fig(loose_svg(10, "mitt")) +
                   "%s has 10 mitts. A pair is 2 mitts. How many pairs?" % nm,
                   5, [10, 2, 8, 4],
                   "Make groups of 2: 2, 4, 6, 8, 10. That is <b>5</b> pairs."))
    its.append(mcq(fig(groups_svg([5, 5], "kid", label="2 teams of 5 children")) +
                   "In gym class, there are 2 basketball teams. Each team has 5 players. How many players?",
                   10, [2, 7, 5, 9],
                   "2 groups of 5: 5 + 5 = <b>10</b> players."))
    its.append(mcq(fig(halves_svg(6, "orange")) +
                   "At soccer, 6 children each get half an orange. How many whole oranges is that?",
                   "3 oranges", ["6 oranges", "12 oranges", "2 oranges"],
                   "2 halves make 1 orange. 6 halves make 3 pairs. That is <b>3 oranges</b>."))
    nm, he, _ = P.next()
    its.append(mcq(fig(one_svg(EQ(c_sectors([90] * 4, start=45)), (0, 1), "pizza cut into 4 equal pieces, 2 shaded")) +
                   "%s eats the 2 shaded pieces of this pizza. How much of the pizza is that?" % nm,
                   "one half", ["one fourth", "two halves", "the whole pizza"],
                   "2 of 4 equal pieces are two fourths. <b>Two fourths is the same as one half.</b>"))
    assert len(its) == 20, len(its)
    return {"title": "More sharers, smaller pieces: stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Equal groups</h2>"
        "<p>Equal groups have the <b>same number</b> in each group. "
        "Count one group. Then check every group.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4], "apple") +
        "<figcaption>2 groups of 4. 4 + 4 = 8 apples in all.</figcaption></figure>"
        "<figure class='sn-fig'>" + groups_svg([4, 3], "apple") +
        "<figcaption>4 and 3: not equal groups.</figcaption></figure>"
        + ex("Example", "There are 3 plates. Each plate has 2 cookies. How many cookies in all?",
             "Add one 2 for each plate: 2 + 2 + 2 = 6.", "6 cookies")
        + "<h2>Fair shares with leftovers</h2>"
        "<p>A fair share means every person gets the <b>same amount</b>, and <b>everything</b> is shared. "
        "Give out the whole things first. Then cut what is left.</p>"
        "<figure class='sn-fig'>" + share_svg(5, 2, "cookie") +
        "<figcaption>5 cookies for 2 children.</figcaption></figure>"
        "<figure class='sn-fig'>" + plates_svg(share_plates(5, 2), "cookie", "2 plates with 2 and a half cookies each") +
        "<figcaption>Each child gets 2. Cut the last cookie into halves. Each child gets 2 and a half.</figcaption></figure>"
        + table(["Children", "Left over", "Cut it into"], [
            ["2", "1", "halves"],
            ["4", "1", "fourths"],
            ["4", "2", "halves (one each)"],
        ])
        + "<h2>Halves and fourths</h2>"
        "<p>2 equal pieces are <b>halves</b>. 4 equal pieces are <b>fourths</b>. "
        "The pieces must be the same size.</p>"
        "<figure class='sn-fig'>" + labeled_row([(EQ(c_sectors([180, 180])), (0,)), (EQ(c_sectors([90] * 4)), (0, 1)),
                                                 (UN(c_chord(0.4)), ())],
                                                ["one half", "two fourths", "not halves"],
                                                "one half, two fourths and two pieces that are not equal") +
        "<figcaption>One half and two fourths cover the same part. The last circle has 2 pieces, "
        "but they are not equal.</figcaption></figure>"
        + "<h2>More sharers, smaller pieces</h2>"
        "<p>Share the same thing with <b>more</b> people, and each piece gets <b>smaller</b>. "
        "A half is bigger than a fourth.</p>"
        + ex("Example", "Liam shares a pizza with 1 friend. Maya shares the same size pizza with 3 friends. "
             "Who gets more?", "Liam’s pizza is cut into halves. Maya’s is cut into fourths. A half is bigger.",
             "Liam")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Calling a big piece and a small piece halves", "Halves must be the same size"],
            ["Thinking a fourth is bigger than a half because 4 is more than 2", "More pieces means smaller pieces"],
            ["Counting the groups, not the things: 2 groups of 4 = 2", "Count all the things: 4 + 4 = 8"],
            ["Leaving the leftover out, or giving it to one child", "Cut the leftover so everyone gets the same"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about fractions in Ontario?",
     "a": "Grade 1 students share things fairly between 2 and 4 people and name the pieces as halves and fourths. "
          "They also learn that two fourths are the same as one half, and that a half is bigger than a fourth."},
    {"q": "What is a fair share in Grade 1 math?",
     "a": "A fair share means every person gets the same amount and nothing is left out. "
          "If 1 cookie is left for 2 children, it is cut into halves so each child gets a half."},
    {"q": "Why does my child think a fourth is bigger than a half?",
     "a": "Many children think 4 is more than 2, so a fourth must be bigger. "
          "Cut two same-size pieces of toast, one into halves and one into fourths, and compare the pieces."},
    {"q": "How can I practise equal groups and fair shares at home?",
     "a": "Share snacks like crackers or grapes fairly between family members, then ask what to do with the leftover. "
          "Make equal groups of mitts, socks or toys and count how many in all."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(41806)
    P = People(rnd)
    sets = [set_equal(P, rnd), set_total(P, rnd), set_leftover(P, rnd), set_parts(P, rnd), set_story(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") == 1, it["q"]
            key = json.dumps([it["q"], it["c"]])
            assert key not in seen, it["q"]
            seen.add(key)
            txt = re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
            assert not re.search(r"\b\d+/\d+\b", txt), it["q"]
            assert "×" not in txt and "÷" not in txt
            assert "{" not in txt
            for tok in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", it["q"] + " ".join(it["c"]))):
                assert int(tok) <= 50, tok
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "equal-groups-and-fair-shares", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Equal Groups and Fair Shares: Halves and Fourths",
        "seo_title": "Grade 1 Equal Groups and Fair Shares Worksheets: Halves and Fourths (Free, Answer Key, Ontario)",
        "short_title": "Equal groups and fair shares",
        "domain": "Number",
        "standard_code": "Grade 1: B2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve equal-group problems where the total number of items is no more than 10, "
                         "including problems in which each group is a half, using tools and drawings",
        "meta_desc": "Free Grade 1 math worksheets on equal groups and fair shares for the Ontario curriculum: spot "
                     "equal groups, find how many in all, share between 2 and 4 friends with leftovers, halves and "
                     "fourths, and why more sharers means smaller pieces. 100 picture questions with an answer key.",
        "key_big": "Equal groups have the same number in each group. Fair shares are the same size, and everything is shared.",
        "key_sub": "5 cookies for 2 children: 2 each, then cut the last cookie into halves, so each gets 2 and a half. "
                   "Two fourths are the same as one half. More sharers means smaller pieces, so a half is bigger than a fourth.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four shapes A to D|same-size shapes A and B|two same-size circles A and B)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
