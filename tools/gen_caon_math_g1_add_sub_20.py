# -*- coding: utf-8 -*-
"""
CA-ON Grade 1 Math: Adding and subtracting to 20 (Ontario Curriculum 2020, B2.3 with B2.1)
  python3 tools/gen_caon_math_g1_add_sub_20.py
Mental math strategies for 6- and 7-year-olds: doubles and near doubles, make ten
(8 + 5 = 8 + 2 + 3), counting on and back on a number line to 20, thinking addition to
subtract, and choosing a strategy and checking it in Canadian word problems.
Every answer and every wrong answer is checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
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
def set_doubles():
    its = []
    add = adder(its)
    for a in (2, 3, 5, 6, 9, 10):
        add(fig(frames_split(a, a)) + "Each frame has %d counters. What is %d + %d?" % (a, a, a), 2 * a,
            [2 * a - 1, 2 * a + 1, a],
            "Both frames have %d. This is a double. %d + %d = <b>%d</b>." % (a, a, a, 2 * a), "%d + %d = ?" % (a, a))
    for a, col2 in ((4, GREEN), (7, ORANGE), (8, GREEN)):
        add(fig(objects_svg("apple", [(a, RED), (a, col2)])) + "Each row has %d apples. What is double %d?" % (a, a),
            2 * a, [2 * a - 1, 2 * a + 1, a],
            "Double %d means %d + %d. %d + %d = <b>%d</b>." % (a, a, a, a, a, 2 * a), "%d + %d = ?" % (a, a))
    for a in (4, 5, 6, 8):
        b = a + 1
        add(fig(frames_split(a, b, 1)) + "Use double %d. What is %d + %d?" % (a, a, b), a + b,
            [2 * a, 2 * b, b],
            "Double %d is %d. The blue counter is 1 more. %d + 1 = <b>%d</b>."
            % (a, 2 * a, 2 * a, a + b), "%d + %d = ?" % (a, b))
    add(fig(frames_split(7, 8, 1)) + "What is 8 + 7?", 15, [14, 16, 1],
        "Double 7 is 14. 8 is 1 more than 7. 14 + 1 = <b>15</b>.", "8 + 7 = ?")
    opts = ["6 + 6", "6 + 7", "5 + 6", "6 + 9"]
    add("Which one is a double?", opts[0], opts[1:],
        "A double adds a number to itself. <b>6 + 6</b> is a double.")
    opts = ["5 + 6", "5 + 5", "5 + 8", "2 + 9"]
    add("Which one is a near double?", opts[0], opts[1:],
        "A near double uses two numbers that are 1 apart. 5 and 6 are 1 apart. So <b>5 + 6</b> is a near double.")
    add(fig(objects_svg("apple", [(7, RED), (7, GREEN)])) + "Double what number makes 14?", 7, [14, 6, 8],
        "7 + 7 = 14. So double <b>7</b> makes 14. (14 is the total.)", "? + ? = 14")
    assert 6 + 7 == 13 and 6 + 6 == 12
    add(fig(frames_split(6, 7, 1)) + "Owen says 6 + 7 = 12. What did he forget?", "To add 1",
        ["To take away 1", "To add 2", "Nothing. He is right."],
        "6 + 6 = 12. But 7 is 1 more than 6. So 6 + 7 = 12 + 1 = 13. Owen forgot <b>to add 1</b>.")
    add(fig(objects_svg("apple", [(6, RED), (6, RED)], crossed=6)) + "Double 6 is 12. What is 12 − 6?", 6,
        [18, 5, 7], "6 + 6 = 12. So 12 − 6 = <b>6</b>. (18 adds instead of taking away.)", "12 − 6 = ?")
    add(fig(objects_svg("apple", [(8, GREEN), (8, GREEN)], crossed=8)) + "Double 8 is 16. What is 16 − 8?", 8,
        [24, 7, 9], "8 + 8 = 16. So 16 − 8 = <b>8</b>. (24 adds instead of taking away.)", "16 − 8 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Doubles and near doubles", "items": its}


# ============================================================ set 2: make ten
def set_make_ten():
    its = []
    add = adder(its)
    for n in (7, 4, 9, 6):
        k = 10 - n
        add(fig(ten_frame_svg(n)) + "How many more counters make 10?", k, [n, k + 1, k - 1, 10 + n],
            "There %s %d empty %s. %d + %d = 10. So <b>%d</b> more %s 10."
            % ("is" if k == 1 else "are", k, "space" if k == 1 else "spaces", n, k, k, "makes" if k == 1 else "make"),
            "%d + ? = 10" % n)
    add("What goes with 2 to make 10?", 8, [12, 7, 9],
        "2 + 8 = 10. So the number is <b>8</b>. (12 adds 10 to 2.)", "2 + ? = 10")
    opts = ["4 + 6", "4 + 5", "3 + 6", "5 + 6"]
    assert eval(opts[0]) == 10 and all(eval(o) != 10 for o in opts[1:])
    add("Which pair makes 10?", opts[0], opts[1:], "4 + 6 = 10. So <b>4 + 6</b> makes 10.")
    opts = ["3 + 6", "1 + 9", "2 + 8", "5 + 5"]
    assert eval(opts[0]) != 10 and all(eval(o) == 10 for o in opts[1:])
    add("Which pair does NOT make 10?", opts[0], opts[1:], "3 + 6 = 9, not 10. So <b>3 + 6</b> does not make 10.")
    add(fig(frames_split(10, 6)) + "One frame is full. What is 10 + 6?", 16, [15, 17, 4],
        "A full frame is 10. 10 and 6 more is <b>16</b>.", "10 + 6 = ?")
    for a, b in [(9, 3), (8, 5), (9, 6), (7, 4), (8, 6)]:
        need = 10 - a
        add(fig(frames_fill(a, b)) + "Fill the top frame first. What is %d + %d?" % (a, b), a + b,
            [a + b - 1, a + b + 1, 10 + b, a - b],
            "%d + %d = 10. %d %s left. 10 + %d = <b>%d</b>."
            % (a, need, b - need, "is" if b - need == 1 else "are", b - need, a + b), "%d + %d = ?" % (a, b))
    for a, b in [(8, 5), (9, 4), (9, 7), (7, 5)]:
        need = 10 - a
        rest = b - need
        add(fig(split_svg(a, b, need, "?")) + "%d + %d = %d + %d + %s. What is the missing number?"
            % (a, b, a, need, B), rest, [b, need, rest + 1, rest - 1],
            "%d + %d makes 10. Split the %d into %d and <b>%d</b>. So %d + %d = 10 + %d = %d."
            % (a, need, b, need, rest, a, b, rest, a + b), "%d + %d = %d + %d + ?" % (a, b, a, need))
    for a, b, w in [(9, 5, ["10 + 5", "10 + 3", "9 + 10"]), (8, 4, ["10 + 4", "10 + 1", "8 + 10"])]:
        need = 10 - a
        right = "10 + %d" % (b - need)
        assert all(eval(x) != a + b for x in w) and eval(right) == a + b
        add(fig(frames_fill(a, b)) + "Make ten. %d + %d is the same as which?" % (a, b), right, w,
            "Move %d to make 10. %d %s left. So %d + %d = <b>%s</b> = %d."
            % (need, b - need, "is" if b - need == 1 else "are", a, b, right, a + b))
    add(fig(frames_fill(9, 4)) + "Start with the bigger number. What is 4 + 9?", 13, [12, 14, 5],
        "Start with 9. 9 + 1 = 10. 3 are left. 10 + 3 = <b>13</b>.", "4 + 9 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Make ten to add", "items": its}


# ============================================================ set 3: count on and count back
def set_number_line():
    its = []
    add = adder(its)
    for s, n in [(8, 3), (12, 2), (6, 4), (15, 3), (9, 2), (13, 4)]:
        v = s + n
        add(fig(nl(s, n)) + "Start at %d. Count on %d. What is %d + %d?" % (s, n, s, n), v,
            [v - 1, v + 1, s - n],
            "Start at %d. Jump %d times: %s. You land on <b>%d</b>. (Do not count the %d.)"
            % (s, n, seq(s + 1, v), v, s), "%d + %d = ?" % (s, n))
    for s, n in [(11, 3), (14, 2), (17, 4), (9, 3), (20, 3), (16, 2)]:
        v = s - n
        add(fig(nl(s, -n)) + "Start at %d. Count back %d. What is %d − %d?" % (s, n, s, n), v,
            [v + 1, v - 1, s + n],
            "Start at %d. Jump back %d times: %s. You land on <b>%d</b>. (Do not count the %d.)"
            % (s, n, seq(s - 1, v), v, s), "%d − %d = ?" % (s, n))
    opts = ["7 + 4 = 11", "7 + 3 = 10", "11 − 4 = 7", "4 + 4 = 8"]
    assert all(holds(o) for o in opts)
    add(fig(nl(7, 4)) + "Which number sentence matches the jumps?", opts[0], opts[1:],
        "Start at 7. There are 4 jumps to the right. That is adding: <b>7 + 4 = 11</b>.")
    opts = ["15 − 3 = 12", "15 + 3 = 18", "12 + 3 = 15", "15 − 2 = 13"]
    assert all(holds(o) for o in opts)
    add(fig(nl(15, -3)) + "Which number sentence matches the jumps?", opts[0], opts[1:],
        "Start at 15. There are 3 jumps to the left. That is taking away: <b>15 − 3 = 12</b>.")
    add(fig(nl(9, 2)) + "Start with the bigger number. What is 2 + 9?", 11, [10, 12, 7],
        "Start at 9, not 2. Count on 2: 10, 11. So 2 + 9 = <b>11</b>.", "2 + 9 = ?")
    add(fig(nl(12, 3)) + "Start with the bigger number. What is 3 + 12?", 15, [14, 16, 9],
        "Start at 12, not 3. Count on 3: 13, 14, 15. So 3 + 12 = <b>15</b>.", "3 + 12 = ?")
    add(fig(nl(7, 3)) + "Ethan counts on for 7 + 3. He says “7, 8, 9.” What went wrong?",
        "He said 7 too", ["He jumped back", "He jumped 4", "Nothing. He is right."],
        "Do not say the start number. Start at 7 and say 8, 9, 10. <b>He said 7 too</b>. 7 + 3 = 10.")
    add(fig(nl(12, -2)) + "Leah counts back for 12 − 2. She says “12, 11.” What went wrong?",
        "She said 12 too", ["She jumped on", "She jumped 3", "Nothing. She is right."],
        "Do not say the start number. Start at 12 and say 11, 10. <b>She said 12 too</b>. 12 − 2 = 10.")
    add(fig(nl(14, 4)) + "How many jumps from 14 to 18?", 4, [5, 3, 18],
        "Count the jumps, not the numbers: 15, 16, 17, 18. That is <b>4</b> jumps. So 14 + 4 = 18.", "14 + ? = 18")
    add(fig(nl(19, -4)) + "How many jumps back from 19 to 15?", 4, [5, 3, 15],
        "Count the jumps: 18, 17, 16, 15. That is <b>4</b> jumps. So 19 − 4 = 15.", "19 − ? = 15")
    assert len(its) == 20, len(its)
    return {"title": "Count on and count back", "items": its}


# ============================================================ set 4: think addition to subtract
def set_think_add():
    its = []
    add = adder(its)
    for a, b in [(8, 5), (9, 3), (7, 5)]:
        s = a + b
        add(fig(frames_fill(a, b)) + "%d + %d = %d. What is %d − %d?" % (a, b, s, s, b), a,
            [a + 1, s + b, wrong_way(s, b)],
            "Take away the %d blue counters. %d red counters are left. %d − %d = <b>%d</b>."
            % (b, a, s, b, a), "%d − %d = ?" % (s, b))
    for w, p in [(11, 8), (14, 9), (15, 7), (12, 4)]:
        d = w - p
        add(fig(part_whole_svg(w, p, "?")) + "What is the missing part?", d, [w + p, d + 1, wrong_way(w, p)],
            "Think: %d + ? = %d. %d + %d = %d. So the missing part is <b>%d</b>." % (p, w, p, d, w, d),
            "%d + ? = %d" % (p, w))
    opts = ["6 + 9 = 15", "15 + 6 = 21", "6 + 6 = 12", "9 − 6 = 3"]
    assert all(holds(o) for o in opts)
    add(fig(frames_fill(6, 9)) + "Which addition helps with 15 − 6?", opts[0], opts[1:],
        "Think: 6 + what = 15? <b>6 + 9 = 15</b>. So 15 − 6 = 9.")
    opts = ["4 + 7 = 11", "11 + 4 = 15", "4 + 4 = 8", "7 − 4 = 3"]
    assert all(holds(o) for o in opts)
    add(fig(frames_fill(4, 7)) + "Which addition helps with 11 − 4?", opts[0], opts[1:],
        "Think: 4 + what = 11? <b>4 + 7 = 11</b>. So 11 − 4 = 7.")
    opts = ["13 − 4 = 9", "13 + 4 = 17", "9 − 4 = 5", "4 + 5 = 9"]
    assert all(holds(o) for o in opts)
    add(fig(part_whole_svg(13, 9, 4)) + "Which fact goes with 9 + 4 = 13?", opts[0], opts[1:],
        "A fact family uses the same 3 numbers: 9, 4 and 13. <b>13 − 4 = 9</b> uses them.")
    add(fig(ten_frame_svg(10, crossed=4)) + "6 + 4 = 10. What is 10 − 4?", 6, [14, 5, 7],
        "If 6 + 4 = 10, then 10 − 4 = <b>6</b>. (14 adds instead.)", "10 − 4 = ?")
    for a, b in [(12, 9), (16, 8), (17, 9), (13, 7)]:
        d = a - b
        add(fig(hop_line_svg(b, a)) + "Count up from %d to %d. What is %d − %d?" % (b, a, a, b), d,
            [d + 1, a + b, wrong_way(a, b)],
            "Count up: %s. That is %d jumps. %d + %d = %d. So %d − %d = <b>%d</b>."
            % (seq(b + 1, a), d, b, d, a, a, b, d), "%d − %d = ?" % (a, b))
    add(fig(hop_line_svg(14, 20)) + "Count up from 14 to 20. What is 20 − 14?", 6, [7, 34, 5],
        "Count up: 15, 16, 17, 18, 19, 20. That is 6 jumps. 14 + 6 = 20. So 20 − 14 = <b>6</b>.", "20 − 14 = ?")
    assert wrong_way(14, 5) == 11 and 14 - 5 == 9
    add(fig(part_whole_svg(14, 5, "?")) + "Kai says 14 − 5 = 11. What did he do?", "He did 5 − 4",
        ["He added 5", "He counted on", "Nothing. He is right."],
        "You cannot take 5 from 4, so Kai did 5 − 4 = 1. That is the wrong way. Think: 5 + 9 = 14. "
        "So 14 − 5 = 9.")
    opts = ["8 + 7 = 15", "15 + 7 = 22", "8 + 15 = 23", "7 + 7 = 14"]
    assert all(holds(o) for o in opts)
    add(fig(part_whole_svg(15, 7, 8)) + "15 − 7 = 8. Which addition checks it?", opts[0], opts[1:],
        "Add the answer and the number you took away. <b>8 + 7 = 15</b>. So 15 − 7 = 8 is right.")
    add(fig(frames_fill(8, 9)) + "8 + 9 = 17. What is 17 − 9?", 8, [26, 9, wrong_way(17, 9)],
        "If 8 + 9 = 17, then 17 − 9 = <b>8</b>. Take away the 9 blue counters.", "17 − 9 = ?")
    opts = ["4 + 9 = 13", "13 − 4 = 9", "9 − 4 = 5", "4 + 9 = 14"]
    assert holds(opts[0]) and not holds(opts[3])
    add(fig(frames_fill(9, 4)) + "9 + 4 = 13. Which is the turn-around fact?", opts[0], opts[1:],
        "A turn-around fact adds the same numbers the other way. The total stays the same: <b>4 + 9 = 13</b>.")
    assert len(its) == 20, len(its)
    return {"title": "Think addition to subtract", "items": its}


# ============================================================ set 5: choose the strategy and check
def set_words():
    its = []
    add_s = adder(its)

    def add(q, right, unit, wrong, e, check, pic=None):
        assert check, q
        one = {"geese": "goose", "pairs": "pair", "leaves": "leaf"}.get(unit, unit[:-1])
        f = lambda v: "%d %s" % (v, one if v == 1 else unit)
        its.append(mcq((fig(pic) if pic else "") + q, f(right), [f(v) for v in wrong], e))

    add_s(fig(frames_split(7, 7)) + "What is the best way to add 7 + 7?", "Use a double",
          ["Make ten", "Count back", "Count on 1"],
          "7 + 7 adds a number to itself. <b>Use a double</b>: 7 + 7 = 14.")
    add_s(fig(frames_fill(9, 6)) + "What is a good way to add 9 + 6?", "Make ten",
          ["Use a double", "Count back", "Take away 6"],
          "9 needs just 1 to make 10. <b>Make ten</b>: 9 + 1 = 10, then 10 + 5 = 15.")
    add_s(fig(nl(15, 2)) + "What is a good way to add 15 + 2?", "Count on 2",
          ["Count back 2", "Make ten", "Use a double"],
          "2 is small. Start at 15 and <b>count on 2</b>: 16, 17. So 15 + 2 = 17.")
    add_s(fig(hop_line_svg(9, 13)) + "What is a good way to find 13 − 9?", "Think 9 + ? = 13",
          ["Think 13 + 9", "Count back 13", "Use double 9"],
          "9 and 13 are close. <b>Think 9 + ? = 13</b>. Count up: 10, 11, 12, 13. That is 4.")
    add("Liam has 6 hockey pucks. He gets 6 more. How many pucks now?", 12, "pucks", [11, 13, 6],
        "This is a double. 6 + 6 = <b>12</b>.", 6 + 6 == 12, objects_svg("puck", [(6, "#555"), (6, BLUE)]))
    add("9 students are on the bus. 4 more get on. How many now?", 13, "students", [12, 14, 5],
        "Make ten. 9 + 1 = 10. 3 more is <b>13</b>.", 9 + 4 == 13,
        objects_svg("child", [(9, BLUE), (4, ORANGE)], noun="children"))
    add("Emma picks 7 apples. Noah picks 8 apples. How many apples?", 15, "apples", [14, 16, 1],
        "Near double. Double 7 is 14. 1 more is <b>15</b>.", 7 + 8 == 15,
        objects_svg("apple", [(7, RED), (8, GREEN)]))
    add("12 Canada geese are on the pond. 3 fly away. How many are left?", 9, "geese",
        [15, 10, wrong_way(12, 3)], "Count back 3: 11, 10, 9. So <b>9</b> are left.", 12 - 3 == 9,
        objects_svg("goose", [(6, "#8d7b68"), (6, "#8d7b68")], crossed=3, noun="geese"))
    add("14 students skate at the rink. 5 go home. How many still skate?", 9, "students",
        [19, 10, wrong_way(14, 5)], "14 − 4 = 10. Take away 1 more: <b>9</b>. Check: 9 + 5 = 14.", 14 - 5 == 9,
        objects_svg("child", [(7, BLUE), (7, BLUE)], crossed=5, noun="children"))
    add("Maya reads 8 pages on Monday. She reads 8 on Tuesday. How many pages?", 16, "pages", [15, 17, 8],
        "This is a double. 8 + 8 = <b>16</b>.", 8 + 8 == 16, frames_split(8, 8))
    add("Ava has 15 hockey cards. Kai has 9. How many more does Ava have?", 6, "cards",
        [24, 7, wrong_way(15, 9)], "Count up from 9 to 15: 10, 11, 12, 13, 14, 15. That is <b>6</b>.", 15 - 9 == 6,
        hop_line_svg(9, 15))
    add("The bus has 20 seats. 14 students sit down. How many seats are empty?", 6, "seats", [34, 7, 5],
        "Think: 14 + ? = 20. 14 + 6 = 20. So <b>6</b> seats are empty.", 20 - 14 == 6, hop_line_svg(14, 20))
    add("Some loons swim on the lake. 5 more come. Now there are 13. How many were there at first?", 8,
        "loons", [18, 13, 9], "Think: ? + 5 = 13. 8 + 5 = 13. So there were <b>8</b> loons.", 8 + 5 == 13,
        part_whole_svg(13, "?", 5))
    add("Zoe has 7 stickers. She gets some more. Now she has 12. How many did she get?", 5, "stickers",
        [19, 6, 12], "Count up from 7 to 12: 8, 9, 10, 11, 12. That is <b>5</b>. Check: 7 + 5 = 12.", 7 + 5 == 12,
        hop_line_svg(7, 12))
    add("10 pairs of mitts are in the lost and found. 4 pairs go home. How many pairs are left?", 6, "pairs",
        [14, 7, 4], "6 + 4 = 10. So 10 − 4 = <b>6</b>.", 10 - 4 == 6, ten_frame_svg(10, crossed=4))
    add("Mateo picks 18 maple leaves. He gives 9 to Hana. How many does he have now?", 9, "leaves",
        [27, 8, 10], "Double 9 is 18. So 18 − 9 = <b>9</b>. Check: 9 + 9 = 18.", 18 - 9 == 9,
        part_whole_svg(18, 9, "?"))
    add("Sofia puts 5 red, 5 blue and 4 green beads on a string. How many beads?", 14, "beads", [13, 15, 10],
        "5 + 5 = 10. Then 10 + 4 = <b>14</b>.", 5 + 5 + 4 == 14,
        objects_svg("bead", [(5, RED), (5, BLUE), (4, GREEN)]))
    add("11 students play in the snow at recess. 3 go inside. Then 5 come out. How many are outside now?", 13,
        "students", [8, 19, 3], "Step 1: 11 − 3 = 8. Step 2: 8 + 5 = <b>13</b>. (8 stops after step 1.)",
        11 - 3 + 5 == 13)
    opts = ["14 − 5 = 9", "14 + 5 = 19", "9 − 5 = 4", "5 + 5 = 10"]
    assert all(holds(o) for o in opts)
    add_s(fig(part_whole_svg(14, 9, 5)) + "Arjun says 9 + 5 = 14. Which fact checks it?", opts[0], opts[1:],
          "Take one part away from the whole. <b>14 − 5 = 9</b>, so Arjun is right.")
    assert 16 - 7 == 9 and 8 + 7 == 15
    add_s(fig(hop_line_svg(7, 16)) + "Priya says 16 − 7 = 8. Is she right?", "No. It is 9.",
          ["Yes. She is right.", "No. It is 7.", "No. It is 23."],
          "Check with addition: 8 + 7 = 15, not 16. Count up from 7 to 16: that is 9. <b>No. It is 9.</b>")
    assert len(its) == 20, len(its)
    return {"title": "Choose a strategy and check", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Doubles and near doubles</h2>"
        "<p>A <b>double</b> adds a number to itself. 6 + 6 = 12. 8 + 8 = 16.</p>"
        "<p>A <b>near double</b> uses two numbers that are 1 apart. Use the double. Then add 1.</p>"
        "<figure class='sn-fig'>" + frames_split(7, 8, 1) +
        "<figcaption>7 + 8 is double 7 and 1 more. 14 + 1 = 15.</figcaption></figure>"
        "<h2>Make ten</h2>"
        "<p>Learn the pairs that make 10. To add past 10, make a 10 first. Then add the rest.</p>"
        + table(["Makes 10", "Turn-around"], [["%d + %d" % (a, 10 - a), "%d + %d" % (10 - a, a)] for a in range(1, 6)]) +
        "<figure class='sn-fig'>" + split_svg(8, 5, 2, 3) +
        "<figcaption>Split the 5 into 2 and 3. 8 + 2 = 10. 10 + 3 = 13.</figcaption></figure>"
        + ex("Example", "What is 9 + 4?", "9 + 1 = 10. 3 are left. 10 + 3 = 13.", "13")
        + "<h2>Count on and count back</h2>"
        "<p>To add a small number, start at the big number and <b>count on</b>. "
        "To take away a small number, <b>count back</b>. Count the jumps, not the start number.</p>"
        "<figure class='sn-fig'>" + nl(8, 3) +
        "<figcaption>8 + 3: start at 8. Say 9, 10, 11. You land on 11.</figcaption></figure>"
        + ex("Example", "What is 13 − 2?", "Start at 13. Count back 2: 12, 11.", "11")
        + "<h2>Think addition to subtract</h2>"
        "<p>Adding and taking away go together. If you know 8 + 5 = 13, you know 13 − 5 = 8 and 13 − 8 = 5.</p>"
        "<figure class='sn-fig'>" + part_whole_svg(13, 8, 5) +
        "<figcaption>8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8, 13 − 8 = 5.</figcaption></figure>"
        + ex("Example", "What is 12 − 9?", "Think: 9 + ? = 12. Count up: 10, 11, 12. That is 3.", "3")
        + "<p>Check a subtraction with an addition. 12 − 9 = 3, and 3 + 9 = 12. It checks.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["8 + 3 = 10 (saying 8, 9, 10)", "Do not say the start number. Say 9, 10, 11. So 8 + 3 = 11."],
            ["13 − 5 = 12 (doing 5 − 3)", "You cannot take 5 from 3. Think: 5 + 8 = 13. So 13 − 5 = 8."],
            ["7 + 8 = 14", "7 + 7 = 14. 8 is 1 more, so 7 + 8 = 15."],
            ["2 + 9: counting on 9 from 2", "Start with the bigger number. 9, then 10, 11. So 2 + 9 = 11."],
        ])
    )


FAQ = [
    {"q": "What does Grade 1 math in Ontario expect for adding and subtracting?",
     "a": "The Ontario Mathematics Curriculum (2020) asks Grade 1 students to use mental math strategies to add and subtract whole numbers that add up to no more than 20, and to explain the strategy they used."},
    {"q": "What are mental math strategies for adding to 20?",
     "a": "Common Grade 1 strategies are doubles (6 + 6), near doubles (6 + 7 is double 6 and 1 more), making ten (8 + 5 = 8 + 2 + 3), and counting on from the bigger number."},
    {"q": "Why does my child get answers that are 1 off when counting on?",
     "a": "They are usually saying the start number as the first count, like “8, 9, 10” for 8 + 3. Have them hold the 8 in their head and count the jumps: 9, 10, 11."},
    {"q": "How can I help my child subtract at home?",
     "a": "Link each subtraction to an addition fact. For 13 − 5, ask “5 plus what makes 13?” A ten frame drawn on paper and some coins or buttons make it easy to see."},
]


def gen():
    rnd = random.Random(41804)
    sets = [set_doubles(), set_make_ten(), set_number_line(), set_think_add(), set_words()]
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
            m = re.search(r"aria-label='ten frame with (\d+) counters", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)), it["q"]
            m = re.search(r"aria-label='two ten frames with (\d+) (?:red )?and (\d+)", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2)), it["q"]
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert int(n) <= 40, c
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "adding-and-subtracting-to-20",
        "sort": 4, "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to 20",
        "seo_title": "Grade 1 Adding and Subtracting to 20 Worksheets with Answer Key (Ontario)",
        "short_title": "Adding and subtracting to 20",
        "domain": "Number",
        "standard_code": "Grade 1: B2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use mental math strategies, including estimation, to add and subtract whole numbers that add up to no more than 20, and explain the strategies used",
        "meta_desc": "Free Grade 1 math worksheets on adding and subtracting to 20: doubles, near doubles, make ten, counting on and back on a number line, and thinking addition to subtract. 100 questions with pictures and an answer key, following the Ontario curriculum.",
        "key_big": "Use a strategy, not just your fingers: doubles, make ten, count on, or think addition.",
        "key_sub": "6 + 7 is double 6 and 1 more: 13. 8 + 5 = 8 + 2 + 3 = 13. For 13 − 5, think 5 + 8 = 13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line|1\\d (?:children|geese)|\\d+ apples in groups of [5-9]|\\d+ (?:pucks|beads) in groups")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
