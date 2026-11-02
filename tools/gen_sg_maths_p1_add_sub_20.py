# -*- coding: utf-8 -*-
"""
SG Primary 1 Maths: Addition and subtraction within 20 (MOE 2021 Primary Mathematics Syllabus)
  python3 tools/gen_sg_maths_p1_add_sub_20.py
For 6- and 7-year-olds: adding with pictures, taking away, making 10 to add (8 + 5 = 8 + 2 + 3),
adding three numbers and word problems in Singapore settings. Every answer and every wrong
answer is checked in code. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#2e6fb7"
ORANGE = "#e67e22"
PURPLE = "#7d3c98"
YELLOW = "#f1c40f"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
B = "<b>?</b>"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
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


def ev(s):
    return eval(s.replace("−", "-"), {"__builtins__": {}})


def holds(eq, ans=None):
    """'8 + ? = 15' is true with ? = ans (real minus sign allowed)."""
    s = eq.replace(B, "?")
    if ans is not None:
        s = s.replace("?", str(ans))
    vals = [ev(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def wrong_way(a, b):
    """The 'smaller from bigger' mistake for a teen number minus a one-digit number: 13 − 5 -> 10 + (5 − 3) = 12."""
    t, o = divmod(a, 10)
    assert t == 1 and b < 10 and b > o
    return 10 * t + (b - o)


def seq(a, b):
    """'9, 10, 11' from a to b (inclusive), either direction."""
    st = 1 if b >= a else -1
    return ", ".join(str(v) for v in range(a, b + st, st))


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


def mark_large(u, min_w=200):
    """Tag wide pictures (rows of objects, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*viewBox='0 0 (\d+) (\d+)')")

    def tag(m):
        return "<svg data-pf='lg' " if int(m.group(1)) >= min_w else m.group(0)
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub(tag, it["q"])
    return u


# ------------------------------------------------------------ pictures: ten frames
CELL = 30
FW, FH = 5 * CELL, 2 * CELL     # one ten frame: 150 x 60


def cross(cx, cy, r=12):
    return ("<path d='M %d %d L %d %d M %d %d L %d %d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, INK))


def frame(x0, y0, colors, crossed=0):
    """One ten frame. colors: up to 10 counter colours, top row first. The last `crossed` counters get an X."""
    assert len(colors) <= 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + CELL, x0 + FW, y0 + CELL, INK))
    for k, col in enumerate(colors):
        r, c = divmod(k, 5)
        cx, cy = x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s'/>" % (cx, cy, col))
        if k >= len(colors) - crossed:
            s.append(cross(cx, cy))
    return "".join(s)


def ten_frame_svg(n, crossed=0):
    o = 6
    label = "ten frame with %d counters" % n + (", %d crossed out" % crossed if crossed else "")
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, [RED] * n, crossed), label)


def two_frames_svg(top, bottom, label):
    o, gap = 6, 12
    body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(FW + 2 * o, 2 * FH + gap + 2 * o, body, label)


def frames_fill(a, b):
    """a red then b blue counters, filling the top frame first (shows make 10)."""
    cols = [RED] * a + [BLUE] * b
    return two_frames_svg(cols[:10], cols[10:], "two ten frames with %d red and %d blue counters" % (a, b))


def frames_take(n, k):
    """n red counters (top frame filled first); the last k are crossed out."""
    assert 10 < n <= 20 and 0 < k <= n
    bot = n - 10
    cb = min(k, bot)
    ct = k - cb
    o, gap = 6, 12
    body = frame(o, o, [RED] * 10, ct) + frame(o, o + FH + gap, [RED] * bot, cb)
    return svg_wrap(FW + 2 * o, 2 * FH + gap + 2 * o, body,
                    "two ten frames with %d counters, %d crossed out" % (n, k))


def frames_split(a, b):
    """a red counters in the top frame, b blue counters in the bottom frame."""
    return two_frames_svg([RED] * a, [BLUE] * b, "two ten frames with %d red and %d blue counters" % (a, b))


# ------------------------------------------------------------ pictures: number bonds
def split_svg(a, b, p1, p2):
    """'a + b' with b split into two parts below (p1 makes 10 with a). Parts may be '?'."""
    W, H = 176, 134
    xa, xp, xb, ty = 48, 88, 128, 32
    s = [text(xa, ty, str(a), 28), text(xp, ty, "+", 28), text(xb, ty, str(b), 28)]
    c1, c2, cy, r = (100, 156, 108, 20)
    for cx in (c1, c2):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>"
                 % (xb, ty + 8, cx, cy - r, GREEN))
    for cx, v in ((c1, p1), (c2, p2)):
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, FILL if v != "?" else "#fff", GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    if "?" not in (p1, p2):
        assert p1 + p2 == b and a + p1 == 10
    return svg_wrap(W, H, "".join(s), "%d + %d with the %d split into %s and %s" % (a, b, b, p1, p2))


def bond_svg(whole, p1, p2):
    """Number bond: whole on top, two parts below. Values are numbers or '?'."""
    r = 28
    W, H = 184, 148
    cw, cy0 = W / 2, 6 + r
    c1, c2, cy1 = 8 + r, W - 8 - r, H - 6 - r
    s = []
    for cx in (c1, c2):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (cw, cy0 + r - 2, cx, cy1 - r + 2, INK))
    for cx, cy, v, fill in [(cw, cy0, whole, FILL), (c1, cy1, p1, "#fff"), (c2, cy1, p2, "#fff")]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    if "?" not in (whole, p1, p2):
        assert p1 + p2 == whole
    return svg_wrap(W, H, "".join(s), "number bond: whole %s, parts %s and %s" % (whole, p1, p2))


# ------------------------------------------------------------ pictures: number lines
STEP = 32


def numline_svg(lo, hi, start, hops):
    """Number line lo..hi with a dot at start. hops > 0: jumps right, hops < 0: jumps left."""
    L, Y = 22, 50
    W = 2 * L + (hi - lo) * STEP
    X = lambda v: L + (v - lo) * STEP
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 14, Y, W - L + 14, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 28, str(v), 16, col=RED if v == start else INK))
    d = 1 if hops > 0 else -1
    for k in range(abs(hops)):
        a, b = start + d * k, start + d * (k + 1)
        assert lo <= b <= hi
        xa, xb = X(a), X(b)
        mid = (xa + xb) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xa, Y - 10, mid, Y - 44, xb, Y - 10, GREEN))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>"
                 % (xb, Y - 9, xb - d * 2, Y - 20, xb - d * 10, Y - 13, GREEN))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, RED))
    label = "number line from %d to %d with %d jumps %s from %d" % (lo, hi, abs(hops), "right" if d > 0 else "left", start)
    return svg_wrap(W, Y + 36, "".join(s), label)


def nl(start, hops):
    """A 12-number line (0 to 20 at most) that holds start and every jump."""
    end = start + hops
    if hops > 0:
        lo = max(0, start - 2)
        hi = lo + 11
    else:
        hi = start + 2
        lo = hi - 11
    if hi > 20:
        hi, lo = 20, 9
    if lo < 0:
        lo, hi = 0, 11
    assert lo <= min(start, end) and max(start, end) <= hi <= 20
    return numline_svg(lo, hi, start, hops)


def hop_line_svg(lo, hi, label="?"):
    """Number line from lo to hi, one tick per number, one big hop from lo to hi."""
    L, step, Y = 22, 36, 70
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 12, Y, W - L + 12, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    x1, x2 = X(lo), X(hi)
    s.append("<path d='M %d %d A %.1f %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (x1, Y - 2, (x2 - x1) / 2, 40, x2, Y - 2, GREEN))
    s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
             "stroke-linejoin='round'/>" % (x2 - 6, Y - 12, x2, Y - 3, x2 + 6, Y - 12, GREEN))
    s.append(text((x1 + x2) / 2, Y - 48, label, 17, col=RED if label == "?" else GREEN))
    return svg_wrap(W, Y + 36, "".join(s), "number line from %d to %d with one hop" % (lo, hi))


# ------------------------------------------------------------ pictures: things to count
def icon(kind, cx, cy, col):
    if kind == "apple":
        return ("<circle cx='%d' cy='%d' r='11' fill='%s'/>"
                "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                "<ellipse cx='%d' cy='%d' rx='5' ry='3' fill='%s'/>"
                % (cx, cy + 2, col, cx, cy - 7, cx + 1, cy - 13, cx + 3, cy - 15, INK, cx + 7, cy - 12, GREEN))
    if kind == "orange":     # mandarin orange with a leaf
        return ("<circle cx='%d' cy='%d' r='11' fill='%s' stroke='#b9560f' stroke-width='1.2'/>"
                "<ellipse cx='%d' cy='%d' rx='5' ry='2.6' fill='%s' transform='rotate(-25 %d %d)'/>"
                "<circle cx='%d' cy='%d' r='1.6' fill='#7a4a12'/>"
                % (cx, cy + 2, col, cx + 5, cy - 10, GREEN, cx + 5, cy - 10, cx, cy - 8))
    if kind == "packet":     # red or green packet
        return ("<rect x='%d' y='%d' width='18' height='24' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<circle cx='%d' cy='%d' r='4' fill='%s'/>"
                % (cx - 9, cy - 12, col, INK, cx, cy - 2, YELLOW))
    if kind == "child":
        return ("<circle cx='%d' cy='%d' r='6' fill='%s'/>"
                "<path d='M %d %d Q %d %d %d %d Z' fill='%s'/>"
                % (cx, cy - 8, col, cx - 10, cy + 13, cx, cy - 8, cx + 10, cy + 13, col))
    if kind == "fish":
        return ("<path d='M %d %d L %d %d L %d %d Z' fill='%s'/>"
                "<ellipse cx='%d' cy='%d' rx='10' ry='6' fill='%s'/>"
                "<circle cx='%d' cy='%d' r='1.8' fill='#fff'/>"
                % (cx - 6, cy, cx - 13, cy - 6, cx - 13, cy + 6, col, cx + 1, cy, col, cx + 6, cy - 1))
    if kind == "car":
        return ("<rect x='%d' y='%d' width='24' height='9' rx='3' fill='%s'/>"
                "<path d='M %d %d L %d %d L %d %d L %d %d Z' fill='%s'/>"
                "<circle cx='%d' cy='%d' r='3.5' fill='%s'/><circle cx='%d' cy='%d' r='3.5' fill='%s'/>"
                % (cx - 12, cy - 1, col, cx - 7, cy - 1, cx - 4, cy - 8, cx + 5, cy - 8, cx + 8, cy - 1, col,
                   cx - 6, cy + 8, INK, cx + 6, cy + 8, INK))
    if kind == "shell":
        return ("<path d='M %d %d A 11 11 0 0 1 %d %d Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<path d='M %d %d L %d %d M %d %d L %d %d M %d %d L %d %d' stroke='%s' stroke-width='1.5'/>"
                % (cx - 11, cy + 6, cx + 11, cy + 6, col, INK,
                   cx, cy + 6, cx, cy - 5, cx, cy + 6, cx - 7, cy - 2, cx, cy + 6, cx + 7, cy - 2, INK))
    if kind == "bird":
        return ("<ellipse cx='%d' cy='%d' rx='10' ry='7' fill='%s'/>"
                "<circle cx='%d' cy='%d' r='5' fill='%s'/>"
                "<path d='M %d %d L %d %d L %d %d Z' fill='%s'/>"
                "<circle cx='%d' cy='%d' r='1.3' fill='#fff'/>"
                % (cx - 2, cy + 4, col, cx + 7, cy - 4, col, cx + 11, cy - 6, cx + 16, cy - 4, cx + 11, cy - 2,
                   ORANGE, cx + 8, cy - 5))
    if kind == "bead":
        return ("<circle cx='%d' cy='%d' r='11' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<circle cx='%d' cy='%d' r='3' fill='#fff'/>" % (cx, cy, col, INK, cx, cy))
    if kind == "book":
        return ("<rect x='%d' y='%d' width='20' height='24' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#fff' stroke-width='2'/>"
                % (cx - 10, cy - 12, col, INK, cx - 6, cy - 12, cx - 6, cy + 12))
    if kind == "lamp":       # small clay oil lamp with a flame
        return ("<path d='M %d %d Q %d %d %d %d Z' fill='%s' stroke='%s' stroke-width='1.2'/>"
                "<path d='M %d %d Q %d %d %d %d Q %d %d %d %d Z' fill='%s'/>"
                % (cx - 12, cy + 2, cx, cy + 16, cx + 12, cy + 2, col, INK,
                   cx, cy - 1, cx - 5, cy - 7, cx, cy - 14, cx + 5, cy - 7, cx, cy - 1, YELLOW))
    if kind == "star":
        pts = []
        for k in range(10):
            rr = 12 if k % 2 == 0 else 5
            ang = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(ang), cy + 1 - rr * math.sin(ang)))
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (" ".join(pts), col, INK)
    if kind == "cup":
        return ("<path d='M %d %d L %d %d L %d %d L %d %d Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx - 9, cy - 10, cx + 9, cy - 10, cx + 6, cy + 11, cx - 6, cy + 11, col, INK))
    raise ValueError(kind)


def objects_svg(kind, groups, crossed=0, noun=None):
    """groups: list of (count, colour). One row per group when every group is 10 or less,
    else rows of 10. A gap after 5 in each row. The last `crossed` items get an X."""
    cols = [c for n, c in groups for _ in range(n)]
    n = len(cols)
    assert 1 <= n <= 20
    step, gap, o = 30, 12, 6
    if len(groups) > 1 and all(g[0] <= 10 for g in groups):
        pos = [(r, c) for r, g in enumerate(groups) for c in range(g[0])]
    else:
        per = 10 if n > 5 else n
        pos = [divmod(k, per) for k in range(n)]
    rows = max(r for r, c in pos) + 1
    width_items = max(c for r, c in pos) + 1
    W = 2 * o + width_items * step + (gap if width_items > 5 else 0)
    H = 2 * o + rows * step + 4
    s = []
    for k, (col, (r, c)) in enumerate(zip(cols, pos)):
        cx = o + c * step + step // 2 + (gap if c >= 5 else 0)
        cy = o + r * step + step // 2 + 2
        s.append(icon(kind, cx, cy, col))
        if k >= n - crossed:
            s.append(cross(cx, cy, 11))
    label = "%d %s" % (n, noun or (kind + "s"))
    if len(groups) > 1:
        label += " in groups of " + " and ".join(str(g[0]) for g in groups)
    if crossed:
        label += ", %d crossed out" % crossed
    return svg_wrap(W, H, "".join(s), label)


def adder(its):
    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert w == right or not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))
    return add


# ============================================================ set 1: add with pictures
def set_add_pictures():
    its = []
    add = adder(its)
    for kind, a, b, c1, c2, noun in [("apple", 3, 4, RED, GREEN, "apples"), ("bead", 5, 3, BLUE, ORANGE, "beads"),
                                     ("orange", 2, 6, ORANGE, ORANGE, "oranges"), ("car", 6, 4, RED, BLUE, "cars"),
                                     ("shell", 7, 2, "#f5deb3", "#f4a6a6", "shells"),
                                     ("packet", 4, 5, RED, RED, "red packets"), ("fish", 5, 5, ORANGE, BLUE, "fish"),
                                     ("star", 6, 3, YELLOW, PURPLE, "stars")]:
        v = a + b
        add(fig(objects_svg(kind, [(a, c1), (b, c2)], noun=noun)) +
            "%d %s and %d more. How many in all?" % (a, noun, b), v,
            [v - 1, v + 1, abs(a - b), v + 2],
            "Start at the bigger number, %d. Count on %d: %s. %d + %d = <b>%d</b>."
            % (max(a, b), min(a, b), seq(max(a, b) + 1, v), a, b, v), "%d + %d = ?" % (a, b))
    for n in (7, 4, 8):
        k = 10 - n
        add(fig(ten_frame_svg(n)) + "How many more make 10?", k, [n, k + 1, k - 1],
            "Count the empty boxes. There are %d. %d + %d = 10. So <b>%d</b> more." % (k, n, k, k),
            "%d + ? = 10" % n)
    for b in (5, 8, 3):
        add(fig(frames_split(10, b)) + "The top frame is full. What is 10 + %d?" % b, 10 + b,
            [10 + b - 1, 10 + b + 1, 10 - b],
            "A full frame is 10. 10 and %d more is <b>%d</b>." % (b, 10 + b), "10 + %d = ?" % b)
    opts = ["4 + 5 = 9", "5 − 4 = 1", "4 + 4 = 8", "5 + 5 = 10"]
    assert all(holds(o) for o in opts)
    add(fig(objects_svg("bead", [(4, RED), (5, BLUE)])) + "4 red and 5 blue. Which one matches?", opts[0], opts[1:],
        "4 red and 5 blue make 9 in all. <b>4 + 5 = 9</b>.")
    add(fig(objects_svg("apple", [(3, RED), (6, GREEN)])) + "3 + 6 = 9. What is 6 + 3?", 9, [8, 10, 3],
        "You can add in any order. The answer stays the same. 6 + 3 = <b>9</b>.", "6 + 3 = ?")
    add(fig(objects_svg("orange", [(6, ORANGE), (3, ORANGE)], noun="oranges")) +
        "Ryan counts 6 + 3. He says “6, 7, 8.” What is the right answer?", 9, [8, 10, 3],
        "Do not say the 6 again. Start after 6: 7, 8, 9. So 6 + 3 = <b>9</b>.", "6 + 3 = ?")
    add(fig(objects_svg("bead", [(2, RED), (5, BLUE)])) + "In 2 + 5 = 7, what does + mean?", "add",
        ["take away", "is equal to", "count back"],
        "The + sign means <b>add</b>. We put 2 and 5 together to get 7.")
    add(fig(objects_svg("star", [(4, YELLOW), (4, PURPLE)], noun="stars")) + "In 4 + 4 = 8, what does = mean?",
        "is equal to", ["add", "take away", "more than"],
        "The = sign means <b>is equal to</b>. 4 + 4 is the same as 8.")
    add(fig(bond_svg(9, 4, "?")) + "What is the missing part?", 5, [13, 4, 6],
        "Think: 4 + ? = 9. 4 + 5 = 9. So the missing part is <b>5</b>.", "4 + ? = 9")
    assert len(its) == 20, len(its)
    return {"title": "Add with pictures", "items": its}


# ============================================================ set 2: subtract by taking away
def set_take_away():
    its = []
    add = adder(its)
    for kind, n, k, col, noun in [("apple", 7, 3, RED, "apples"), ("bead", 9, 4, BLUE, "beads"),
                                  ("fish", 8, 5, ORANGE, "fish"), ("car", 11, 2, BLUE, "cars"),
                                  ("shell", 12, 5, "#f5deb3", "shells"), ("orange", 15, 4, ORANGE, "oranges")]:
        v = n - k
        add(fig(objects_svg(kind, [(n, col)], crossed=k, noun=noun)) +
            "There are %d. %d are crossed out. How many are left?" % (n, k), v, [v + 1, v - 1, n + k],
            "Take away %d. Count the ones with no X. %d − %d = <b>%d</b>." % (k, n, k, v), "%d − %d = ?" % (n, k))
    for n, k in [(10, 3), (8, 2), (6, 5)]:
        v = n - k
        add(fig(ten_frame_svg(n, crossed=k)) + "What is %d − %d?" % (n, k), v, [v + 1, v - 1, n + k, k],
            "%d counters. %d have an X. <b>%d</b> %s left." % (n, k, v, "is" if v == 1 else "are"), "%d − %d = ?" % (n, k))
    for n, k in [(13, 3), (16, 4), (14, 5), (12, 9), (17, 8), (20, 7)]:
        v = n - k
        add(fig(frames_take(n, k)) + "What is %d − %d?" % (n, k), v, [v + 1, v - 1, n + k],
            "Start with %d. Take away %d. Count what is left: <b>%d</b>." % (n, k, v), "%d − %d = ?" % (n, k))
    opts = ["11 − 4 = 7", "11 + 4 = 15", "7 − 4 = 3", "4 + 4 = 8"]
    assert all(holds(o) for o in opts)
    add(fig(objects_svg("apple", [(11, GREEN)], crossed=4)) + "Which one matches the picture?", opts[0], opts[1:],
        "There are 11. 4 are crossed out. 7 are left. <b>11 − 4 = 7</b>.")
    add(fig(objects_svg("bead", [(12, ORANGE)], crossed=5)) + "Siti sees 12 − 5. She says 17. What is right?",
        7, [17, 8, 6], "17 is 12 + 5. Siti added. Take away 5 from 12. 12 − 5 = <b>7</b>.", "12 − 5 = ?")
    add(fig(objects_svg("fish", [(12, BLUE)], crossed=4, noun="fish")) +
        "There were 12. Now 8 are left. How many were taken away?", 4, [8, 20, 5],
        "Count the ones with an X. 12 − 4 = 8. So <b>4</b> were taken away.", "12 − ? = 8")
    add(fig(nl(12, -3)) + "Ali counts back for 12 − 3. He says “12, 11, 10.” What is right?", 9, [10, 15, 8],
        "Do not say 12 again. Start after 12: 11, 10, 9. So 12 − 3 = <b>9</b>.", "12 − 3 = ?")
    add(fig(frames_take(15, 9)) + "What is 15 − 9?", 6, [7, 5, 24],
        "Take away 5 from the bottom. Then 4 from the top. 6 are left. 15 − 9 = <b>6</b>.", "15 − 9 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Subtract by taking away", "items": its}


# ============================================================ set 3: make 10 to add
MAKE10 = [(8, 5), (9, 4), (7, 6), (9, 6), (8, 7), (7, 5), (9, 8), (8, 4), (6, 5), (7, 8), (9, 3), (6, 8)]


def set_make_ten():
    its = []
    add = adder(its)
    # which part makes 10 with the first number?
    for a, b in [(8, 5), (9, 4), (7, 6), (6, 5)]:
        p1, p2 = 10 - a, b - (10 - a)
        add(fig(split_svg(a, b, "?", "?")) + "%d + %d. Split %d to make 10. What goes with %d?" % (a, b, b, a), p1,
            [p2, b, p1 + 1, 10],
            "%d + %d = 10. So split %d into %d and %d. The part is <b>%d</b>." % (a, p1, b, p1, p2, p1),
            "%d + ? = 10" % a)
    # ten frames: fill the top frame first
    for a, b in [(9, 2), (8, 6), (7, 4), (9, 7), (8, 8), (6, 7)]:
        v = a + b
        need = 10 - a
        add(fig(frames_fill(a, b)) + "Fill the top frame first. What is %d + %d?" % (a, b), v,
            [v - 1, v + 1, abs(a - b), v + 2],
            "%d + %d = 10. The top frame is full. %d %s left. 10 + %d = <b>%d</b>."
            % (a, need, b - need, "is" if b - need == 1 else "are", b - need, v), "%d + %d = ?" % (a, b))
    # a + b = 10 + ?
    for a, b in [(9, 5), (8, 3), (7, 7), (6, 6)]:
        p1, p2 = 10 - a, b - (10 - a)
        add(fig(split_svg(a, b, p1, "?")) + "%d + %d = 10 + ?" % (a, b), p2, [b, p1, p2 + 1, p2 - 1, a + b],
            "%d + %d = 10. %d is left from the %d. So %d + %d = 10 + <b>%d</b> = %d."
            % (a, p1, p2, b, a, b, p2, a + b), "%d + %d = 10 + ?" % (a, b))
    # which is the same as?
    for a, b in [(9, 4), (8, 5)]:
        p1, p2 = 10 - a, b - (10 - a)
        opts = ["10 + %d" % p2, "10 + %d" % b, "10 + %d" % p1, "10 + %d" % (b + p1)]
        assert len({ev(o) for o in opts}) == 4 and ev(opts[0]) == a + b
        add(fig(frames_fill(a, b)) + "%d + %d is the same as which?" % (a, b), opts[0], opts[1:],
            "Move %d to make 10. %d is left. <b>%s</b> = %d." % (p1, p2, opts[0], a + b))
    # make 10 with the bigger number
    for a, b in [(4, 9), (3, 8)]:
        p1, p2 = 10 - b, a - (10 - b)
        v = a + b
        add(fig(split_svg(b, a, p1, p2)) + "What is %d + %d? Make 10 with the %d." % (a, b, b), v,
            [v - 1, v + 1, b - a],
            "Start with the bigger number, %d. %d + %d = 10. %d is left. 10 + %d = <b>%d</b>."
            % (b, b, p1, p2, p2, v), "%d + %d = ?" % (a, b))
    add(fig(split_svg(8, 5, 2, 3)) + "Jun Jie says 8 + 5 = 10 + 5 = 15. What is right?", 13, [15, 12, 14],
        "He used 2 of the 5 to make 10. Only 3 are left. 8 + 5 = 10 + 3 = <b>13</b>.", "8 + 5 = ?")
    opts = ["7 and 3", "7 and 4", "6 and 3", "5 and 4"]
    assert ev("7+3") == 10 and all(ev(o.replace(" and ", "+")) != 10 for o in opts[1:])
    add(fig(bond_svg(10, "?", "?")) + "Which pair makes 10?", opts[0], opts[1:],
        "7 + 3 = 10. So <b>7 and 3</b> make 10.")
    assert len(its) == 20, len(its)
    return {"title": "Make 10 to add", "items": its}


# ============================================================ set 4: add three numbers
def set_three():
    its = []
    add = adder(its)
    for kind, (a, b, c), noun in [("bead", (3, 7, 4), "beads"), ("apple", (5, 5, 6), "apples"),
                                  ("star", (2, 3, 4), "stars"), ("orange", (6, 4, 2), "oranges"),
                                  ("fish", (4, 2, 8), "fish"), ("shell", (7, 1, 5), "shells"),
                                  ("car", (5, 3, 5), "cars"), ("book", (8, 2, 9), "books"),
                                  ("bead", (6, 6, 3), "beads"), ("packet", (1, 9, 7), "red packets")]:
        v = a + b + c
        cols = [RED, BLUE, GREEN] if kind not in ("orange", "packet", "shell") else {
            "orange": [ORANGE] * 3, "packet": [RED] * 3, "shell": ["#f5deb3", "#f4a6a6", "#bcd9ef"]}[kind]
        tens = [(x, y) for x, y in [(a, b), (b, c), (a, c)] if x + y == 10]
        if tens:
            x, y = tens[0]
            rest = v - 10
            e = "Look for 10 first. %d + %d = 10. Then 10 + %d = <b>%d</b>." % (x, y, rest, v)
        else:
            e = "Add two first. %d + %d = %d. Then %d + %d = <b>%d</b>." % (a, b, a + b, a + b, c, v)
        add(fig(objects_svg(kind, [(a, cols[0]), (b, cols[1]), (c, cols[2])], noun=noun)) +
            "What is %d + %d + %d?" % (a, b, c), v, [a + b, v - 1, b + c, v + 1], e, "%d + %d + %d = ?" % (a, b, c))
    for a, b, c in [(3, 6, 7), (8, 5, 2), (4, 9, 6)]:
        pr = sorted([(a, b), (a, c), (b, c)], key=lambda p: p[0] + p[1] != 10)
        good = pr[0]
        assert good[0] + good[1] == 10 and all(p[0] + p[1] != 10 for p in pr[1:])
        opts = ["%d and %d" % p for p in pr] + ["No two make 10"]
        add(fig(objects_svg("bead", [(a, RED), (b, BLUE), (c, GREEN)])) +
            "%d + %d + %d. Which two make 10?" % (a, b, c), opts[0], opts[1:],
            "%d + %d = 10. Add them first. Then add %d. The answer is %d."
            % (good[0], good[1], a + b + c - 10, a + b + c))
    for a, c, v in [(5, 3, 12), (2, 6, 15)]:
        m = v - a - c
        add(fig(objects_svg("bead", [(a, RED), (c, BLUE)])) + "%d + ? + %d = %d. What is the missing number?" % (a, c, v),
            m, [v - a, m + 1, v + a + c],
            "%d + %d = %d. %d + ? = %d. So the missing number is <b>%d</b>." % (a, c, a + c, a + c, v, m),
            "%d + ? + %d = %d" % (a, c, v))
    add(fig(objects_svg("apple", [(2, RED), (8, GREEN), (5, RED)])) +
        "Farah says 2 + 8 + 5 = 10. What did she forget?", "To add the 5",
        ["To add the 2", "To take away 5", "Nothing. She is right."],
        "2 + 8 = 10. She stopped there. She forgot <b>to add the 5</b>. 10 + 5 = 15.")
    add(fig(objects_svg("star", [(4, YELLOW), (6, PURPLE), (5, ORANGE)])) + "4 + 6 + 5 = 15. What is 5 + 6 + 4?",
        15, [14, 16, 11], "Same numbers, other order. The answer is the same: <b>15</b>.", "5 + 6 + 4 = ?")
    for a, b, c in [(6, 4, 7), (3, 7, 8), (2, 8, 6)]:
        v = a + b + c
        opts = ["10 + %d" % c, "10 + %d" % (c - 1), "%d + %d" % (a, c), "10 + %d" % (c + 1)]
        assert len({ev(o) for o in opts}) == 4 and ev(opts[0]) == v
        add(fig(objects_svg("bead", [(a, RED), (b, BLUE), (c, GREEN)])) +
            "%d + %d + %d is the same as which?" % (a, b, c), opts[0], opts[1:],
            "%d + %d = 10. So %d + %d + %d = <b>%s</b> = %d." % (a, b, a, b, c, opts[0], v))
    assert len(its) == 20, len(its)
    return {"title": "Add three numbers", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    PL = {"oranges": "orange", "red packets": "red packet", "green packets": "green packet", "children": "child",
          "people": "person", "books": "book", "birds": "bird", "lamps": "lamp", "stickers": "sticker",
          "beads": "bead", "fish": "fish", "apples": "apple", "cars": "car", "students": "student", "cups": "cup",
          "shells": "shell"}

    def add(q, right, unit, wrong, e, check, pic=None):
        assert check, q
        one = PL[unit]
        f = lambda v: "%d %s" % (v, one if v == 1 else unit)
        its.append(mcq((fig(pic) if pic else "") + q, f(right), [f(v) for v in wrong], e))

    add("Wei Ming has 9 mandarin oranges. His grandma gives him 4 more. How many oranges now?", 13, "oranges",
        [12, 14, 5], "9 + 1 = 10. 3 more is <b>13</b>. 9 + 4 = 13.", 9 + 4 == 13,
        objects_svg("orange", [(9, ORANGE), (4, ORANGE)], noun="oranges"))
    add("Mei Ling has 15 red packets. She gives 6 away. How many are left?", 9, "red packets",
        [21, 10, wrong_way(15, 6)], "Take away 6. 15 − 5 = 10. 10 − 1 = <b>9</b>.", 15 - 6 == 9,
        objects_svg("packet", [(15, RED)], crossed=6, noun="red packets"))
    add("8 children play at the void deck. 5 more come. How many children now?", 13, "children",
        [12, 14, 3], "8 + 2 = 10. 3 more is <b>13</b>. 8 + 5 = 13.", 8 + 5 == 13,
        objects_svg("child", [(8, PURPLE), (5, ORANGE)], noun="children"))
    add("12 people are on the MRT train. 5 get off. How many are still on?", 7, "people",
        [17, 8, wrong_way(12, 5)], "12 − 2 = 10. 10 − 3 = <b>7</b>. Check: 7 + 5 = 12.", 12 - 5 == 7,
        objects_svg("child", [(12, BLUE)], crossed=5, noun="people"))
    add("Siti borrows 7 library books. Ali borrows 6. How many books in all?", 13, "books", [12, 14, 1],
        "7 + 3 = 10. 3 more is <b>13</b>. 7 + 6 = 13.", 7 + 6 == 13,
        objects_svg("book", [(7, RED), (6, BLUE)], noun="books"))
    add("17 birds sit on a tree at the zoo. 9 fly away. How many birds are left?", 8, "birds",
        [26, 9, wrong_way(17, 9)], "17 − 7 = 10. 10 − 2 = <b>8</b>. Check: 8 + 9 = 17.", 17 - 9 == 8,
        objects_svg("bird", [(17, "#5d4037")], crossed=9, noun="birds"))
    add("Priya lights 6 oil lamps for Deepavali. Then she lights 6 more. How many lamps now?", 12, "lamps",
        [11, 13, 10], "6 + 6 is a double. 6 + 6 = <b>12</b>.", 6 + 6 == 12,
        objects_svg("lamp", [(6, "#a0522d"), (6, "#a0522d")], noun="lamps"))
    add("Hafiz gets 5 green packets on Hari Raya. Then he gets 8 more. How many now?", 13, "green packets",
        [12, 14, 3], "8 + 2 = 10. 3 more is <b>13</b>. 5 + 8 = 13.", 5 + 8 == 13,
        objects_svg("packet", [(5, GREEN), (8, GREEN)], noun="green packets"))
    add("Raju has 5 stickers. Kavya has 9 stickers. How many more stickers does Kavya have?", 4, "stickers",
        [14, 5, 3], "Count on from 5 to 9: 6, 7, 8, 9. That is <b>4</b>. 9 − 5 = 4.", 9 - 5 == 4,
        hop_line_svg(5, 9))
    add("Chloe has 16 beads. She needs 20 for a bracelet. How many more beads does she need?", 4, "beads",
        [36, 5, 3], "Count on from 16: 17, 18, 19, 20. That is <b>4</b>. 20 − 16 = 4.", 20 - 16 == 4,
        hop_line_svg(16, 20))
    add("There are 13 fish in a tank. 6 are orange. The rest are blue. How many are blue?", 7, "fish",
        [19, 8, 6], "13 − 6 = <b>7</b>. Check: 6 + 7 = 13.", 13 - 6 == 7, bond_svg(13, 6, "?"))
    add("Mrs Lim buys 6 red apples, 4 green apples and 3 more red apples. How many apples in all?", 13, "apples",
        [10, 12, 14], "6 + 4 = 10. Then 10 + 3 = <b>13</b>.", 6 + 4 + 3 == 13,
        objects_svg("apple", [(6, RED), (4, GREEN), (3, RED)], noun="apples"))
    add("Ryan sees 8 red cars, 2 blue cars and 7 grey cars. How many cars in all?", 17, "cars",
        [10, 9, 16], "8 + 2 = 10. Then 10 + 7 = <b>17</b>.", 8 + 2 + 7 == 17,
        objects_svg("car", [(8, RED), (2, BLUE), (7, "#8a8a8a")], noun="cars"))
    add("10 children are in the pool. 4 get out. Then 3 jump in. How many are in the pool now?", 9, "children",
        [6, 17, 11], "Step 1: 10 − 4 = 6. Step 2: 6 + 3 = <b>9</b>.", 10 - 4 + 3 == 9,
        objects_svg("child", [(10, BLUE)], crossed=4, noun="children"))
    add("There are 18 students in a class. 9 go to the library. How many stay in class?", 9, "students",
        [27, 10, 8], "Double 9 is 18. So 18 − 9 = <b>9</b>.", 18 - 9 == 9,
        objects_svg("child", [(18, PURPLE)], crossed=9, noun="students"))
    add("7 people are on a bus. At the next stop, 6 more get on. How many are on the bus now?", 13, "people",
        [12, 14, 1], "7 + 3 = 10. 3 more is <b>13</b>. 7 + 6 = 13.", 7 + 6 == 13,
        objects_svg("child", [(7, BLUE), (6, ORANGE)], noun="people"))
    add("Nurul has 12 mandarin oranges. She eats 3. She says 15 are left. How many are really left?", 9, "oranges",
        [15, 10, 8], "Eating means taking away, not adding. 12 − 3 = <b>9</b>.", 12 - 3 == 9,
        objects_svg("orange", [(12, ORANGE)], crossed=3, noun="oranges"))
    add("The school canteen has 20 cups. 7 cups are used. How many cups are left?", 13, "cups",
        [27, 14, 12], "20 − 7 = <b>13</b>. Check: 13 + 7 = 20.", 20 - 7 == 13,
        objects_svg("cup", [(20, "#bcd9ef")], crossed=7, noun="cups"))
    add("Kavya finds 9 shells at Sentosa. Arjun finds 8 shells. How many shells in all?", 17, "shells",
        [16, 18, 1], "9 + 1 = 10. 7 more is <b>17</b>. 9 + 8 = 17.", 9 + 8 == 17,
        objects_svg("shell", [(9, "#f5deb3"), (8, "#f4a6a6")], noun="shells"))
    add("Xin Yi has some stickers. She gets 5 more. Now she has 14. How many did she have at first?", 9,
        "stickers", [19, 14, 10], "Think: ? + 5 = 14. 14 − 5 = <b>9</b>. Check: 9 + 5 = 14.", 14 - 5 == 9,
        bond_svg(14, "?", 5))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add: put groups together</h2>"
        "<p>To <b>add</b>, put two groups together. Then find how many in all. "
        "The sign + means add. The sign = means is equal to.</p>"
        "<figure class='sn-fig'>" + objects_svg("apple", [(5, RED), (3, GREEN)]) +
        "<figcaption>5 red apples and 3 green apples. 5 + 3 = 8.</figcaption></figure>"
        "<p>To count on, start at the bigger number. Do not say it again. For 5 + 3, say 6, 7, 8.</p>"
        + "<h2>Subtract: take away</h2>"
        "<p>To <b>subtract</b>, start with a group. Take some away. Count what is left. The sign − means take away.</p>"
        "<figure class='sn-fig'>" + objects_svg("orange", [(9, ORANGE)], crossed=4, noun="oranges") +
        "<figcaption>9 oranges. 4 are crossed out. 5 are left. 9 − 4 = 5.</figcaption></figure>"
        + ex("Example", "What is 14 − 6?", "14 − 4 = 10. Take away 2 more. 10 − 2 = 8.", "8")
        + "<h2>Make 10 to add</h2>"
        "<p>Adding to 10 is easy. So split the second number. Use one part to make 10.</p>"
        "<figure class='sn-fig'>" + split_svg(8, 5, 2, 3) +
        "<figcaption>8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.</figcaption></figure>"
        + ex("Example", "What is 9 + 6?", "9 + 1 = 10. 5 is left. 10 + 5 = 15.", "15")
        + "<h2>Add three numbers</h2>"
        "<p>Add two numbers first. Then add the third. Look for two numbers that make 10.</p>"
        + ex("Example", "What is 3 + 5 + 7?", "3 + 7 = 10. Then 10 + 5 = 15.", "15")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["6 + 3 = 8 (saying 6, 7, 8)", "Do not say the start number. Say 7, 8, 9. So 6 + 3 = 9."],
            ["12 − 5 = 17", "That adds. “Take away” means subtract. 12 − 5 = 7."],
            ["8 + 5 = 10 + 5 = 15", "2 of the 5 made the 10. Only 3 are left. 8 + 5 = 13."],
            ["2 + 8 + 5 = 10", "Add all three numbers. 10 + 5 = 15."],
        ])
    )


FAQ = [
    {"q": "What is taught in P1 addition and subtraction?",
     "a": "In Primary 1, students use the signs +, − and = and add and subtract within 20 in their heads. They also add three 1-digit numbers and solve simple word problems."},
    {"q": "How do I teach my child to make 10 to add?",
     "a": "Split the smaller number so one part fills up 10. For 8 + 5, split 5 into 2 and 3: 8 + 2 = 10, and 10 + 3 = 13."},
    {"q": "What is the most common mistake in P1 addition?",
     "a": "When counting on, many children say the start number again, so 6 + 3 becomes “6, 7, 8” and the answer is 1 too small. Have them start counting from the next number: 7, 8, 9."},
    {"q": "Is this in the MOE Primary 1 maths syllabus?",
     "a": "Yes. Addition and subtraction within 20, the signs +, − and =, and adding three 1-digit numbers are part of Number and Algebra in the MOE 2021 Primary 1 syllabus."},
]


def gen():
    rnd = random.Random(61804)
    sets = [set_add_pictures(), set_take_away(), set_make_ten(), set_three(), set_words()]
    balance(sets, rnd)
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in allq, it["q"]
            allq.add(it["q"])
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                for j, c in enumerate(it["c"]):
                    assert (int(c) == v) == (j == it["a"]), it["q"]
            m = re.search(r"What is (\d+) \+ (\d+) \+ (\d+)\?$", it["q"])
            if m:
                v = sum(int(x) for x in m.groups())
                for j, c in enumerate(it["c"]):
                    assert (int(c) == v) == (j == it["a"]), it["q"]
            m = re.search(r"aria-label='(?:two )?ten frames? with (\d+) counters", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)), it["q"]
            m = re.search(r"aria-label='two ten frames with (\d+) red and (\d+)", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2)), it["q"]
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert int(n) <= 40, c
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "addition-and-subtraction-within-20",
        "sort": 4, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Addition and Subtraction within 20",
        "seo_title": "P1 Addition and Subtraction within 20 Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Addition and subtraction within 20",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Addition and Subtraction",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Use of +, − and =; adding more than two 1-digit numbers; mental calculation within 20",
        "meta_desc": "Free P1 maths practice: add and subtract within 20, make 10 to add, add three numbers and "
                     "solve word problems. 100 questions with pictures and answers.",
        "key_big": "To add, put groups together. To subtract, take some away.",
        "key_sub": "Make 10 to add: 8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u)


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
