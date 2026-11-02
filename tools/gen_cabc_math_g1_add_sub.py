# -*- coding: utf-8 -*-
"""
CA-BC Grade 1 Math: Addition and subtraction to 20 (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g1_add_sub.py
For 6- and 7-year-olds: adding with pictures and ten frames, subtracting by taking away,
counting on and back on a number line, doubles and near doubles, and fact families
in BC word problems. Every answer and every wrong answer is checked in code.
HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#2e6fb7"
ORANGE = "#e67e22"
PURPLE = "#7d3c98"
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


def holds(eq, ans=None):
    """'8 + ? = 15' is true with ? = ans (real minus sign allowed)."""
    s = eq.replace(B, "?")
    if ans is not None:
        s = s.replace("?", str(ans))
    s = s.replace("−", "-")
    vals = [eval(p.strip(), {"__builtins__": {}}) for p in s.split("=")]
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


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
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
    """Two ten frames stacked (compact for print)."""
    o, gap = 6, 12
    body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(FW + 2 * o, 2 * FH + gap + 2 * o, body, label)


def frames_fill(a, b):
    """a red then b blue counters, filling the top frame first (shows make ten)."""
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


def frames_split(a, b, extra_b=0):
    """a red counters in the top frame, b counters in the bottom frame (the last extra_b of them blue)."""
    return two_frames_svg([RED] * a, [RED] * (b - extra_b) + [BLUE] * extra_b,
                          "two ten frames with %d and %d counters" % (a, b))


# ------------------------------------------------------------ pictures: make-ten split
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


# ------------------------------------------------------------ pictures: part-whole model
def part_whole_svg(whole, p1, p2):
    """Whole on top, two parts below. Values are numbers or '?'."""
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
    return svg_wrap(W, H, "".join(s), "part-whole model: whole %s, parts %s and %s" % (whole, p1, p2))


# ------------------------------------------------------------ pictures: number lines
STEP = 32


def numline_svg(lo, hi, start, hops):
    """Number line lo..hi with a dot at start. hops > 0: jumps right, hops < 0: jumps left, one jump per number."""
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
        lo = max(0, start - 3)
        hi = lo + 11
    else:
        hi = start + 3
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
    if kind == "puck":
        return ("<ellipse cx='%d' cy='%d' rx='12' ry='6' fill='%s'/>"
                "<rect x='%d' y='%d' width='24' height='7' fill='%s'/>"
                "<ellipse cx='%d' cy='%d' rx='12' ry='6' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx, cy + 5, INK, cx - 12, cy - 2, INK, cx, cy - 2, col, INK))
    if kind == "child":
        return ("<circle cx='%d' cy='%d' r='6' fill='%s'/>"
                "<path d='M %d %d Q %d %d %d %d Z' fill='%s'/>"
                % (cx, cy - 8, col, cx - 10, cy + 13, cx, cy - 8, cx + 10, cy + 13, col))
    if kind == "salmon":
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
    if kind == "eagle":
        return ("<ellipse cx='%d' cy='%d' rx='8' ry='10' fill='%s'/>"
                "<circle cx='%d' cy='%d' r='5.5' fill='#fff' stroke='%s' stroke-width='1.2'/>"
                "<path d='M %d %d L %d %d L %d %d Z' fill='#f1c40f'/>"
                % (cx, cy + 4, col, cx, cy - 9, INK, cx + 4, cy - 10, cx + 10, cy - 8, cx + 4, cy - 6))
    if kind == "goose":
        return ("<ellipse cx='%d' cy='%d' rx='11' ry='6' fill='%s'/>"
                "<path d='M %d %d L %d %d' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
                "<circle cx='%d' cy='%d' r='4' fill='%s'/>"
                "<circle cx='%d' cy='%d' r='1.8' fill='#fff'/>"
                % (cx - 2, cy + 6, col, cx + 6, cy + 3, cx + 8, cy - 9, INK, cx + 8, cy - 11, INK, cx + 7, cy - 10))
    if kind == "bead":
        return ("<circle cx='%d' cy='%d' r='11' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<circle cx='%d' cy='%d' r='3' fill='#fff'/>" % (cx, cy, col, INK, cx, cy))
    if kind == "card":
        return ("<rect x='%d' y='%d' width='18' height='24' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%d' y='%d' width='10' height='9' fill='#fff'/>"
                % (cx - 9, cy - 12, col, INK, cx - 5, cy - 8))
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


# ============================================================ set 1: doubles and near doubles
# ============================================================ set 1: add with pictures and ten frames
def set_add_pictures():
    its = []
    add = adder(its)
    for kind, a, b, c1, c2, noun in [("apple", 3, 4, RED, GREEN, "apples"), ("bead", 5, 3, BLUE, ORANGE, "beads"),
                                     ("salmon", 2, 6, RED, "#e9967a", "salmon"), ("puck", 6, 4, "#555", BLUE, "pucks"),
                                     ("shell", 7, 2, "#f5deb3", "#f4a6a6", "shells")]:
        v = a + b
        add(fig(objects_svg(kind, [(a, c1), (b, c2)], noun=noun)) +
            "%d %s and %d more. How many in all?" % (a, noun, b), v, [v - 1, v + 1, a - b if a > b else b - a],
            "Count on from %d: %s. %d + %d = <b>%d</b>." % (a, seq(a + 1, v), a, b, v), "%d + %d = ?" % (a, b))
    for a, b in [(9, 2), (8, 4), (7, 6), (6, 5), (8, 6), (9, 7)]:
        v = a + b
        need = 10 - a
        add(fig(frames_fill(a, b)) + "Fill the top frame first. What is %d + %d?" % (a, b), v,
            [v - 1, v + 1, a - b],
            "The top frame has 10. %d %s in the bottom frame. 10 + %d = <b>%d</b>."
            % (b - need, "is" if b - need == 1 else "are", b - need, v), "%d + %d = ?" % (a, b))
    for n in (7, 4, 8):
        k = 10 - n
        add(fig(ten_frame_svg(n)) + "How many more make 10?", k, [k + 1, k - 1, n + 10],
            "Count the empty boxes. There are %d. %d + %d = 10. So <b>%d</b> more." % (k, n, k, k),
            "%d + ? = 10" % n)
    for b in (5, 8):
        add(fig(frames_split(10, b)) + "The top frame is full. What is 10 + %d?" % b, 10 + b,
            [10 + b - 1, 10 + b + 1, 10 - b],
            "A full frame is 10. 10 and %d more is <b>%d</b>." % (b, 10 + b), "10 + %d = ?" % b)
    opts = ["6 + 7 = 13", "6 + 4 = 10", "7 + 7 = 14", "6 + 6 = 12"]
    assert all(holds(o) for o in opts)
    add(fig(frames_fill(6, 7)) + "There are 6 red and 7 blue. Which one matches?", opts[0], opts[1:],
        "6 red and 7 blue make 13 in all. <b>6 + 7 = 13</b>.")
    add(fig(frames_fill(5, 9)) + "5 + 9 = 14. What is 9 + 5?", 14, [13, 15, 4],
        "You can add in any order. The total stays the same. 9 + 5 = <b>14</b>.", "9 + 5 = ?")
    add(fig(objects_svg("bead", [(4, RED), (6, BLUE), (3, GREEN)])) + "What is 4 + 6 + 3?", 13, [12, 14, 10],
        "4 + 6 = 10. Then 10 + 3 = <b>13</b>.", "4 + 6 + 3 = ?")
    add(fig(objects_svg("apple", [(8, RED), (3, GREEN)])) + "Ryan counts 8 + 3. He says “8, 9, 10.” "
        "What is the right answer?", 11, [10, 12, 5],
        "Do not say the 8 again. Say 9, 10, 11. So 8 + 3 = <b>11</b>.", "8 + 3 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Add with pictures and ten frames", "items": its}


# ============================================================ set 2: subtract by taking away
def set_take_away():
    its = []
    add = adder(its)
    for kind, n, k, col, noun in [("apple", 7, 3, RED, "apples"), ("bead", 9, 4, BLUE, "beads"),
                                  ("salmon", 8, 5, RED, "salmon"), ("car", 11, 2, BLUE, "cars"),
                                  ("shell", 12, 5, "#f5deb3", "shells"), ("puck", 15, 4, "#555", "pucks")]:
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
    add(fig(objects_svg("bead", [(12, ORANGE)], crossed=5)) + "Ava sees 12 − 5. She says 17. What is right?",
        7, [17, 8, 6], "17 is 12 + 5. Ava added. Take away 5 from 12. 12 − 5 = <b>7</b>.", "12 − 5 = ?")
    add(fig(objects_svg("salmon", [(12, RED)], crossed=4, noun="salmon")) +
        "There were 12. Now 8 are left. How many were taken away?", 4, [8, 20, 5],
        "Count the ones with an X. 12 − 4 = 8. So <b>4</b> were taken away.", "12 − ? = 8")
    add(fig(frames_take(15, 9)) + "What is 15 − 9?", 6, [7, 5, 24],
        "Take away 5 from the bottom. Then 4 from the top. 6 are left. 15 − 9 = <b>6</b>.", "15 − 9 = ?")
    add(fig(objects_svg("car", [(18, ORANGE)], crossed=6, noun="cars")) + "What is 18 − 6?", 12, [13, 11, 24],
        "18 cars. 6 have an X. Count the rest: <b>12</b>.", "18 − 6 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Subtract by taking away", "items": its}


# ============================================================ set 3: count on and count back
def set_number_line():
    its = []
    add = adder(its)
    for s, n in [(7, 3), (11, 4), (5, 3), (14, 2), (16, 3), (10, 4)]:
        v = s + n
        add(fig(nl(s, n)) + "Start at %d. Count on %d. What is %d + %d?" % (s, n, s, n), v,
            [v - 1, v + 1, s - n],
            "Start at %d. Say %s. You land on <b>%d</b>. (Do not count the %d.)"
            % (s, seq(s + 1, v), v, s), "%d + %d = ?" % (s, n))
    for s, n in [(12, 3), (15, 4), (18, 2), (10, 3), (19, 4), (13, 2)]:
        v = s - n
        add(fig(nl(s, -n)) + "Start at %d. Count back %d. What is %d − %d?" % (s, n, s, n), v,
            [v + 1, v - 1, s + n],
            "Start at %d. Say %s. You land on <b>%d</b>. (Do not count the %d.)"
            % (s, seq(s - 1, v), v, s), "%d − %d = ?" % (s, n))
    opts = ["9 + 4 = 13", "9 + 3 = 12", "13 − 4 = 9", "4 + 4 = 8"]
    assert all(holds(o) for o in opts)
    add(fig(nl(9, 4)) + "Which one matches the jumps?", opts[0], opts[1:],
        "Start at 9. There are 4 jumps to the right. That is adding: <b>9 + 4 = 13</b>.")
    opts = ["17 − 3 = 14", "17 + 3 = 20", "14 + 3 = 17", "17 − 2 = 15"]
    assert all(holds(o) for o in opts)
    add(fig(nl(17, -3)) + "Which one matches the jumps?", opts[0], opts[1:],
        "Start at 17. There are 3 jumps to the left. That is taking away: <b>17 − 3 = 14</b>.")
    add(fig(nl(8, 3)) + "Start with the bigger number. What is 3 + 8?", 11, [10, 12, 5],
        "Start at 8, not 3. Count on 3: 9, 10, 11. So 3 + 8 = <b>11</b>.", "3 + 8 = ?")
    add(fig(nl(13, 2)) + "Start with the bigger number. What is 2 + 13?", 15, [14, 16, 11],
        "Start at 13, not 2. Count on 2: 14, 15. So 2 + 13 = <b>15</b>.", "2 + 13 = ?")
    add(fig(nl(6, 3)) + "Owen counts on for 6 + 3. He says “6, 7, 8.” What went wrong?",
        "He said 6 too", ["He went back", "He made 4 jumps", "Nothing. He is right."],
        "Do not say the start number. Start at 6. Say 7, 8, 9. <b>He said 6 too</b>. 6 + 3 = 9.")
    add(fig(nl(14, -2)) + "Nadia counts back for 14 − 2. She says “14, 13.” What went wrong?",
        "She said 14 too", ["She went on", "She made 3 jumps", "Nothing. She is right."],
        "Do not say the start number. Start at 14. Say 13, 12. <b>She said 14 too</b>. 14 − 2 = 12.")
    add(fig(nl(12, 5)) + "How many jumps from 12 to 17?", 5, [6, 4, 17],
        "Count the jumps, not the numbers: 13, 14, 15, 16, 17. That is <b>5</b> jumps. So 12 + 5 = 17.",
        "12 + ? = 17")
    add(fig(nl(20, -3)) + "How many jumps back from 20 to 17?", 3, [4, 2, 17],
        "Count the jumps: 19, 18, 17. That is <b>3</b> jumps. So 20 − 3 = 17.", "20 − ? = 17")
    assert len(its) == 20, len(its)
    return {"title": "Count on and count back on a number line", "items": its}


# ============================================================ set 4: doubles and near doubles
def set_doubles():
    its = []
    add = adder(its)
    for a in (2, 4, 6, 9, 10):
        add(fig(frames_split(a, a)) + "Each frame has %d. What is %d + %d?" % (a, a, a), 2 * a,
            [2 * a - 1, 2 * a + 1, a],
            "Both frames have %d. This is a double. %d + %d = <b>%d</b>." % (a, a, a, 2 * a), "%d + %d = ?" % (a, a))
    for a, col2 in ((3, GREEN), (5, ORANGE), (8, GREEN)):
        add(fig(objects_svg("apple", [(a, RED), (a, col2)])) + "Each row has %d apples. What is double %d?" % (a, a),
            2 * a, [2 * a - 1, 2 * a + 1, a],
            "Double %d means %d + %d. %d + %d = <b>%d</b>." % (a, a, a, a, a, 2 * a), "%d + %d = ?" % (a, a))
    for a in (3, 5, 6, 8, 9):
        b = a + 1
        add(fig(frames_split(a, b, 1)) + "Use double %d. What is %d + %d?" % (a, a, b), a + b,
            [2 * a, 2 * b, b],
            "Double %d is %d. The blue counter is 1 more. %d + 1 = <b>%d</b>."
            % (a, 2 * a, 2 * a, a + b), "%d + %d = ?" % (a, b))
    add(fig(frames_split(7, 8, 1)) + "What is 8 + 7?", 15, [14, 16, 1],
        "Double 7 is 14. 8 is 1 more than 7. 14 + 1 = <b>15</b>.", "8 + 7 = ?")
    opts = ["7 + 7", "7 + 8", "6 + 7", "7 + 4"]
    add("Which one is a double?", opts[0], opts[1:],
        "A double adds a number to itself. <b>7 + 7</b> is a double.")
    opts = ["4 + 5", "4 + 4", "4 + 8", "3 + 9"]
    add("Which one is a near double?", opts[0], opts[1:],
        "A near double uses two numbers that are 1 apart. 4 and 5 are 1 apart. So <b>4 + 5</b> is a near double.")
    add(fig(objects_svg("apple", [(8, RED), (8, GREEN)])) + "Double what number makes 16?", 8, [16, 7, 9],
        "8 + 8 = 16. So double <b>8</b> makes 16. (16 is the total.)", "? + ? = 16")
    assert 7 + 8 == 15 and 7 + 7 == 14
    add(fig(frames_split(7, 8, 1)) + "Arjun says 7 + 8 = 14. What did he forget?", "To add 1",
        ["To take away 1", "To add 2", "Nothing. He is right."],
        "7 + 7 = 14. But 8 is 1 more than 7. So 7 + 8 = 14 + 1 = 15. Arjun forgot <b>to add 1</b>.")
    add(fig(objects_svg("apple", [(7, RED), (7, RED)], crossed=7)) + "Double 7 is 14. What is 14 − 7?", 7,
        [21, 6, 8], "7 + 7 = 14. So 14 − 7 = <b>7</b>. (21 adds instead of taking away.)", "14 − 7 = ?")
    add(fig(frames_split(5, 6, 1)) + "5 + 6 = 11. What is 6 + 5?", 11, [10, 12, 1],
        "Same numbers, other order. The total is the same. 6 + 5 = <b>11</b>.", "6 + 5 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Doubles and near doubles", "items": its}


# ============================================================ set 5: fact families and word problems
def set_words():
    its = []
    add_s = adder(its)
    PL = {"salmon": "salmon", "people": "person", "cars": "car", "shells": "shell", "students": "student",
          "eagles": "eagle", "days": "day", "laps": "lap", "orcas": "orca", "cards": "card", "children": "child", "apples": "apple"}

    def add(q, right, unit, wrong, e, check, pic=None):
        assert check, q
        one = PL[unit]
        f = lambda v: "%d %s" % (v, one if v == 1 else unit)
        its.append(mcq((fig(pic) if pic else "") + q, f(right), [f(v) for v in wrong], e))

    # fact families
    opts = ["13 − 5 = 8", "13 + 5 = 18", "8 − 5 = 3", "5 + 3 = 8"]
    assert all(holds(o) for o in opts)
    add_s(fig(part_whole_svg(13, 8, 5)) + "Which fact is in this family?", opts[0], opts[1:],
          "This family uses 8, 5 and 13. <b>13 − 5 = 8</b> uses all three.")
    opts = ["4 + 7 = 11", "11 − 4 = 7", "7 − 4 = 3", "11 + 4 = 15"]
    assert all(holds(o) for o in opts)
    add_s(fig(part_whole_svg(11, 7, 4)) + "7 + 4 = 11. Which is the turn-around fact?", opts[0], opts[1:],
          "A turn-around fact adds the same numbers in the other order: <b>4 + 7 = 11</b>.")
    opts = ["9 − 6 = 3", "6 + 9 = 15", "15 − 6 = 9", "15 − 9 = 6"]
    assert all(holds(o) for o in opts)
    add_s(fig(part_whole_svg(15, 9, 6)) + "Which fact is NOT in this family?", opts[0], opts[1:],
          "The family uses 6, 9 and 15. <b>9 − 6 = 3</b> does not use 15.")
    opts = ["17 − 8 = 9", "17 + 8 = 25", "9 − 8 = 1", "8 + 9 = 17"]
    assert all(holds(o) for o in opts)
    add_s(fig(part_whole_svg(17, 9, 8)) + "Which subtraction goes with 9 + 8 = 17?", opts[0], opts[1:],
          "Start with the whole, 17. Take away a part, 8. <b>17 − 8 = 9</b>.")
    add_s(fig(part_whole_svg(12, "?", 5)) + "What is the missing part?", 7, [17, 8, 6],
          "Think: ? + 5 = 12. 7 + 5 = 12. So the missing part is <b>7</b>.", "? + 5 = 12")
    add_s(fig(part_whole_svg(14, 6, "?")) + "What is the missing part?", 8, [20, 9, 7],
          "Think: 6 + ? = 14. 6 + 8 = 14. So the missing part is <b>8</b>.", "6 + ? = 14")
    add_s(fig(part_whole_svg(12, 9, 3)) + "How many facts are in the family of 9, 3 and 12?", 4, [2, 3, 12],
          "9 + 3 = 12, 3 + 9 = 12, 12 − 3 = 9, 12 − 9 = 3. That is <b>4</b> facts.")
    # word problems
    add("Kai sees 9 salmon in the creek. 4 more swim in. How many salmon now?", 13, "salmon", [12, 14, 5],
        "9 + 1 = 10. 3 more is <b>13</b>. 9 + 4 = 13.", 9 + 4 == 13,
        objects_svg("salmon", [(9, RED), (4, "#e9967a")], noun="salmon"))
    add("8 cars wait for the ferry. 7 more come. How many cars now?", 15, "cars", [14, 16, 1],
        "Near double. Double 7 is 14. 1 more is <b>15</b>.", 8 + 7 == 15,
        objects_svg("car", [(8, BLUE), (7, ORANGE)], noun="cars"))
    add("Olivia finds 14 shells at the beach. She gives 6 to Lucas. How many does she have now?", 8, "shells",
        [20, 9, 7], "Take away 6. 14 − 6 = <b>8</b>. Check: 8 + 6 = 14.", 14 - 6 == 8,
        objects_svg("shell", [(14, "#f5deb3")], crossed=6, noun="shells"))
    add("7 bald eagles sit in a cedar tree. 2 fly away. How many are still in the tree?", 5, "eagles",
        [9, 6, 4], "Count back 2: 6, 5. So <b>5</b> are still there. 7 − 2 = 5.", 7 - 2 == 5,
        objects_svg("eagle", [(7, "#5d4037")], crossed=2, noun="eagles"))
    add("It rains in Vancouver on 6 days. Then it rains on 6 more days. How many rainy days?", 12, "days",
        [11, 13, 6], "This is a double. 6 + 6 = <b>12</b>.", 6 + 6 == 12, frames_split(6, 6))
    add("Mei walks 5 laps in the Terry Fox Run. Wei walks 9 laps. How many more laps does Wei walk?", 4,
        "laps", [14, 5, 3], "Count up from 5 to 9: 6, 7, 8, 9. That is <b>4</b>. Check: 5 + 4 = 9.",
        9 - 5 == 4, hop_line_svg(5, 9))
    add("Some orcas swim by. Then 3 more come. Now there are 10. How many came first?", 7, "orcas",
        [13, 10, 8], "Think: ? + 3 = 10. 7 + 3 = 10. So <b>7</b> came first.", 7 + 3 == 10,
        part_whole_svg(10, "?", 3))
    add("Noah has 15 hockey cards. He wants 20. How many more does he need?", 5, "cards", [35, 6, 4],
        "Think: 15 + ? = 20. Count up: 16, 17, 18, 19, 20. That is <b>5</b>.", 20 - 15 == 5, hop_line_svg(15, 20))
    add("13 people ride the SkyTrain. 4 get off. How many are still on?", 9, "people",
        [17, 10, wrong_way(13, 4)], "13 − 3 = 10. Take away 1 more: <b>9</b>. Check: 9 + 4 = 13.", 13 - 4 == 9,
        objects_svg("child", [(13, BLUE)], crossed=4, noun="people"))
    add("Jasleen’s class has 10 students on a hike. 6 more join. How many students now?", 16, "students",
        [15, 17, 4], "10 and 6 more is <b>16</b>. 10 + 6 = 16.", 10 + 6 == 16,
        objects_svg("child", [(10, PURPLE), (6, ORANGE)], noun="children"))
    add("Simran picks 17 apples in the Okanagan. 8 are red. The rest are green. How many are green?", 9,
        "apples", [25, 10, wrong_way(17, 8)], "Think: 8 + ? = 17. 8 + 9 = 17. So <b>9</b> are green.",
        17 - 8 == 9, part_whole_svg(17, 8, "?"))
    add("10 children play soccer at recess. 3 go inside. Then 4 come out. How many play now?", 11, "children",
        [7, 17, 3], "Step 1: 10 − 3 = 7. Step 2: 7 + 4 = <b>11</b>. (7 stops after step 1.)", 10 - 3 + 4 == 11)
    opts = ["16 − 9 = 7", "16 + 9 = 25", "9 − 7 = 2", "7 + 7 = 14"]
    assert all(holds(o) for o in opts)
    add_s(fig(part_whole_svg(16, 7, 9)) + "Harjot says 7 + 9 = 16. Which fact checks it?", opts[0], opts[1:],
          "Take one part away from the whole. <b>16 − 9 = 7</b>, so Harjot is right.")
    assert len(its) == 20, len(its)
    return {"title": "Fact families and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add: put groups together</h2>"
        "<p>To <b>add</b>, put two groups together. Then find how many in all.</p>"
        "<p>A ten frame helps. Fill the top frame first. A full frame is 10.</p>"
        "<figure class='sn-fig'>" + frames_fill(8, 5) +
        "<figcaption>8 + 5: the top frame is full (10). 3 more is 13.</figcaption></figure>"
        + ex("Example", "What is 9 + 4?", "9 + 1 = 10. 3 are left. 10 + 3 = 13.", "13")
        + "<h2>Subtract: take away</h2>"
        "<p>To <b>subtract</b>, start with a group. Take some away. Count what is left.</p>"
        "<figure class='sn-fig'>" + objects_svg("apple", [(9, RED)], crossed=4) +
        "<figcaption>9 apples. 4 are crossed out. 5 are left. 9 − 4 = 5.</figcaption></figure>"
        "<h2>Count on and count back</h2>"
        "<p>To add a small number, start at the big number. <b>Count on</b>. "
        "To take away a small number, <b>count back</b>. Do not say the start number.</p>"
        "<figure class='sn-fig'>" + nl(8, 3) +
        "<figcaption>8 + 3: start at 8. Say 9, 10, 11. You land on 11.</figcaption></figure>"
        + ex("Example", "What is 14 − 3?", "Start at 14. Count back 3: 13, 12, 11.", "11")
        + "<h2>Doubles and near doubles</h2>"
        "<p>A <b>double</b> adds a number to itself: 6 + 6 = 12. "
        "A <b>near double</b> uses two numbers that are 1 apart. Use the double. Then add 1.</p>"
        + table(["Double", "Near double"], [["%d + %d = %d" % (a, a, 2 * a), "%d + %d = %d" % (a, a + 1, 2 * a + 1)]
                                            for a in range(3, 10, 2)])
        + "<h2>Fact families</h2>"
        "<p>Three numbers make a <b>fact family</b>. If you know 8 + 5 = 13, you know 3 more facts.</p>"
        "<figure class='sn-fig'>" + part_whole_svg(13, 8, 5) +
        "<figcaption>8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8, 13 − 8 = 5.</figcaption></figure>"
        + ex("Example", "What is 12 − 9?", "Think: 9 + ? = 12. Count up: 10, 11, 12. That is 3.", "3")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["8 + 3 = 10 (saying 8, 9, 10)", "Do not say the start number. Say 9, 10, 11. So 8 + 3 = 11."],
            ["12 − 5 = 17", "That adds. “Take away” means subtract. 12 − 5 = 7."],
            ["7 + 8 = 14", "7 + 7 = 14. 8 is 1 more, so 7 + 8 = 15."],
            ["2 + 9: counting on 9 from 2", "Start with the bigger number. Say 10, 11. So 2 + 9 = 11."],
        ])
    )


FAQ = [
    {"q": "What does Grade 1 math in BC expect for addition and subtraction?",
     "a": "The BC Grade 1 curriculum lists addition and subtraction to 20 under Computational fluency. Students learn what adding and taking away mean, and use pictures, ten frames and number lines to solve facts to 20."},
    {"q": "What strategies help Grade 1 students add and subtract to 20?",
     "a": "Useful strategies are counting on from the bigger number, counting back, filling a ten frame to make 10, doubles and near doubles (6 + 7 is double 6 and 1 more), and using fact families."},
    {"q": "Why is my child’s answer 1 off when counting on?",
     "a": "They are usually saying the start number as the first count, like “8, 9, 10” for 8 + 3. Have them hold the 8 in their head and count the jumps: 9, 10, 11."},
    {"q": "What is a fact family in Grade 1?",
     "a": "A fact family is a set of facts that use the same three numbers. For 8, 5 and 13: 8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8 and 13 − 8 = 5."},
]


def gen():
    rnd = random.Random(51803)
    sets = [set_add_pictures(), set_take_away(), set_number_line(), set_doubles(), set_words()]
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
            m = re.search(r"aria-label='(?:two )?ten frames? with (\d+) counters", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)), it["q"]
            m = re.search(r"aria-label='two ten frames with (\d+) (?:red )?and (\d+)", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2)), it["q"]
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert int(n) <= 40, c
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "addition-and-subtraction-to-20",
        "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Addition and Subtraction to 20",
        "seo_title": "Grade 1 Addition and Subtraction to 20 Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Addition and subtraction to 20",
        "domain": "Computational fluency",
        "standard_code": "Grade 1: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Addition and subtraction to 20 (understanding of operation and process)",
        "meta_desc": "Free Grade 1 math worksheets on addition and subtraction to 20 for the BC curriculum: add with pictures and ten frames, take away, count on and back on a number line, doubles, near doubles and fact families. 100 questions with pictures and an answer key.",
        "key_big": "Adding puts groups together. Subtracting takes some away. Count on from the bigger number.",
        "key_sub": "8 + 3: say 9, 10, 11 (not 8). 6 + 7 is double 6 and 1 more: 13. If 8 + 5 = 13, then 13 − 5 = 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line|1\\d (?:apples|beads|cars|shells|pucks|salmon|people|children)|"
                         "\\d+ (?:apples|beads|cars|salmon|pucks|shells|children) in groups of (?:[5-9]|1\\d)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
