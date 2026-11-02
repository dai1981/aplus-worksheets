# -*- coding: utf-8 -*-
"""
CA-BC Grade 2 Math: Addition and subtraction facts to 20 (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g2_facts.py
Doubles and near doubles, make ten with ten frames, fact families and turn-around facts,
missing addends, and mixed facts with British Columbia word problems.
Every answer and every wrong answer is checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
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


def ten_frame_svg(colors, label, crossed=0):
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, colors, crossed), label)


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


# ------------------------------------------------------------ pictures: number line
def hop_line_svg(lo, hi, label="?"):
    """Number line from lo to hi, one tick per number, one hop from lo to hi."""
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


# ------------------------------------------------------------ pictures: apples, pucks, children
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
    raise ValueError(kind)


def objects_svg(kind, groups, crossed=0, noun=None):
    """groups: list of (count, colour). Rows of 10 with a gap after 5. The last `crossed` items get an X."""
    cols = [c for n, c in groups for _ in range(n)]
    n = len(cols)
    assert 1 <= n <= 20
    step, gap, o = 30, 12, 6
    if len(groups) > 1 and all(g[0] <= 10 for g in groups):
        pos = [(r, c) for r, g in enumerate(groups) for c in range(g[0])]     # one row per group
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
    for a in (5, 8, 9):
        add(fig(frames_split(a, a)) + "Each frame has %d counters. What is %d + %d?" % (a, a, a), 2 * a,
            [2 * a - 1, 2 * a + 1, a],
            "This is a double. Double %d is <b>%d</b>." % (a, 2 * a), "%d + %d = ?" % (a, a))
    for a in (6, 7, 10):
        add("What is double %d?" % a, 2 * a, [2 * a - 1, 2 * a + 1, a],
            "Double %d means %d + %d. %d + %d = <b>%d</b>." % (a, a, a, a, a, 2 * a), "%d + %d = ?" % (a, a))
    for t in (12, 16):
        h = t // 2
        add("Double what number makes %d?" % t, h, [2 * t, h - 1, h + 1],
            "%d + %d = %d, so double <b>%d</b> makes %d." % (h, h, t, h, t), "? + ? = %d" % t)
    # near doubles with a picture: top frame a, bottom frame a + 1 (the extra one blue)
    for a in (6, 7, 8, 4):
        b = a + 1
        add(fig(frames_split(a, b, 1)) + "Double %d and 1 more. What is %d + %d?" % (a, a, b), a + b,
            [2 * a, 2 * b, b],
            "%d + %d is a near double. Double %d is %d. The blue counter is 1 more: <b>%d</b>."
            % (a, b, a, 2 * a, a + b), "%d + %d = ?" % (a, b))
    add("Use double 3. What is 3 + 4?", 7, [6, 8, 1],
        "Double 3 is 6. 4 is 1 more than 3, so add 1: <b>7</b>.", "3 + 4 = ?")
    add("Use double 5. What is 5 + 6?", 11, [10, 12, 1],
        "Double 5 is 10. 6 is 1 more than 5, so add 1: <b>11</b>. (1 is 6 − 5. That takes away.)", "5 + 6 = ?")
    add("Use double 9. What is 9 + 8?", 17, [18, 19, 16],
        "Double 9 is 18. 8 is 1 less than 9, so take away 1: <b>17</b>.", "9 + 8 = ?")
    add("Which double helps you work out 7 + 8?", "7 + 7, then add 1",
        ["7 + 7, then take 1", "8 + 9, then add 1", "6 + 6, then add 1"],
        "8 is 1 more than 7. Double 7 is 14, then add 1: 15. So use <b>7 + 7, then add 1</b>.")
    assert 7 + 7 + 1 == 7 + 8 and 7 + 7 - 1 != 15 and 8 + 9 + 1 != 15 and 6 + 6 + 1 != 15
    add("Which one is a near double?", "5 + 6", ["5 + 5", "5 + 8", "3 + 9"],
        "A near double uses two numbers that are 1 apart. 5 and 6 are 1 apart, so <b>5 + 6</b> is a near double. "
        "5 + 5 is a double.")
    add("Harjot says 8 + 9 = 16. What did he do wrong?", "He forgot to add 1",
        ["He took away", "He used double 9", "Nothing. He is right."],
        "8 + 8 = 16. But 9 is 1 more than 8, so 8 + 9 = 16 + 1 = 17. <b>He forgot to add 1</b>.")
    assert 8 + 9 == 17 and 8 + 8 == 16
    add("Double 7 is 14. What is 14 − 7?", 7, [21, 6, 8],
        "If 7 + 7 = 14, then 14 − 7 = <b>7</b>. (21 adds instead of taking away.)", "14 − 7 = ?")
    add("Double 9 is 18. What is 18 − 9?", 9, [27, 8, 10],
        "If 9 + 9 = 18, then 18 − 9 = <b>9</b>. (27 adds instead of taking away.)", "18 − 9 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Doubles and near doubles", "items": its}


# ============================================================ set 2: make ten
def set_make_ten():
    its = []
    add = adder(its)
    for n in (7, 4, 9, 2):
        k = 10 - n
        add(fig(ten_frame_svg([RED] * n, "ten frame with %d counters" % n)) + "How many more counters make 10?",
            k, [n, k + 1, k - 1, 10 + n],
            "There %s %d %s and %d empty %s. %d + %d = 10, so <b>%d</b> more %s 10."
            % ("is" if n == 1 else "are", n, "counter" if n == 1 else "counters", k, "space" if k == 1 else "spaces",
               n, k, k, "makes" if k == 1 else "make"), "%d + ? = 10" % n)
    add("Which pair makes 10?", "3 + 7", ["3 + 6", "4 + 7", "2 + 7"],
        "3 + 7 = 10, so <b>3 + 7</b> makes 10. 3 + 6 = 9, 4 + 7 = 11 and 2 + 7 = 9.")
    assert 3 + 7 == 10 and 3 + 6 != 10 and 4 + 7 != 10 and 2 + 7 != 10
    add("Which pair does NOT make 10?", "4 + 5", ["1 + 9", "2 + 8", "6 + 4"],
        "4 + 5 = 9, not 10. So <b>4 + 5</b> does not make 10.")
    assert 4 + 5 != 10 and 1 + 9 == 10 and 2 + 8 == 10 and 6 + 4 == 10
    add("What number goes with 6 to make 10?", 4, [16, 3, 5],
        "6 + 4 = 10, so the number is <b>4</b>. (16 adds 10 instead: 6 + 10.)", "6 + ? = 10")
    add("What number goes with 1 to make 10?", 9, [11, 8, 10],
        "1 + 9 = 10, so the number is <b>9</b>. (10 is the total, not the part.)", "1 + ? = 10")
    for a, b in [(9, 4), (8, 5), (9, 7), (8, 6), (7, 5)]:
        need = 10 - a
        add(fig(frames_fill(a, b)) + "Fill the top frame first. What is %d + %d?" % (a, b), a + b,
            [a + b - 1, a + b + 1, 10 + b, a - b],
            "%d needs %d more to make 10. Take %d from the %d: %d %s left. 10 + %d = <b>%d</b>."
            % (a, need, need, b, b - need, "is" if b - need == 1 else "are", b - need, a + b), "%d + %d = ?" % (a, b))
    for a, b, w in [(8, 5, ["10 + 5", "10 + 2", "8 + 10"]), (9, 6, ["10 + 6", "10 + 4", "9 + 10"]),
                    (7, 6, ["10 + 6", "10 + 4", "7 + 10"])]:
        need = 10 - a
        right = "10 + %d" % (b - need)
        assert all(eval(x) != a + b for x in w) and eval(right) == a + b
        add("Make ten. %d + %d is the same as which?" % (a, b), right, w,
            "Move %d from the %d to the %d. %d + %d = 10 and %d is left. So %d + %d = <b>%s</b> = %d."
            % (need, b, a, a, need, b - need, a, b, right, a + b))
    add("Start with the bigger number. What is 3 + 9?", 12, [11, 13, 6],
        "Start with 9. Take 1 from the 3 to make 10. 2 are left. 10 + 2 = <b>12</b>.", "3 + 9 = ?")
    add("Make ten. What is 6 + 9?", 15, [14, 16, 3],
        "Start with 9. Take 1 from the 6 to make 10. 5 are left. 10 + 5 = <b>15</b>.", "6 + 9 = ?")
    add("Make ten. What is 4 + 8?", 12, [11, 13, 4],
        "Start with 8. Take 2 from the 4 to make 10. 2 are left. 10 + 2 = <b>12</b>.", "4 + 8 = ?")
    add("Make ten. What is 7 + 9?", 16, [15, 17, 2],
        "Start with 9. Take 1 from the 7 to make 10. 6 are left. 10 + 6 = <b>16</b>.", "7 + 9 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Make ten to add", "items": its}


# ============================================================ set 3: fact families and turn-around facts
def set_fact_families():
    its = []
    add = adder(its)
    for a, b in [(8, 5), (6, 9)]:
        s = a + b
        right = "%d + %d = %d" % (b, a, s)
        wrong = ["%d − %d = %d" % (s, b, a), "%d − %d = %d" % (max(a, b), min(a, b), abs(a - b)),
                 "%d + %d = %d" % (b, a, s + 1)]
        add("%d + %d = %d. Which is the turn-around fact?" % (a, b, s), right, wrong,
            "A turn-around fact adds the same numbers in the other order. The total stays the same: <b>%s</b>."
            % right)
    add("Use a turn-around fact. 4 + 9 = 9 + %s" % B, 4, [9, 13, 5],
        "4 + 9 and 9 + 4 are the same. So the missing number is <b>4</b>.", "4 + 9 = 9 + ?")
    add("7 + 8 = 15. What is 8 + 7?", 15, [16, 14, 1],
        "8 + 7 is the turn-around fact for 7 + 8. The total is the same: <b>15</b>.", "8 + 7 = ?")
    for a, b in [(8, 5), (9, 6)]:
        s = a + b
        add(fig(frames_fill(a, b)) + "The frames show %d + %d = %d. Take away the blue counters. What is %d − %d?"
            % (a, b, s, s, b), a, [a + 1, s + b, wrong_way(s, b)],
            "Take away the %d blue counters. The %d red counters are left. %d − %d = <b>%d</b>."
            % (b, a, s, b, a), "%d − %d = ?" % (s, b))
    for a, b in [(7, 5), (8, 6)]:
        s = a + b
        add("%d + %d = %d. Use this fact. What is %d − %d?" % (a, b, s, s, a), b, [b + 1, s + a, wrong_way(s, a)],
            "If %d + %d = %d, then %d − %d = <b>%d</b>. Subtraction undoes addition." % (a, b, s, s, a, b),
            "%d − %d = ?" % (s, a))
    add(fig(part_whole_svg(16, 9, "?")) + "What is the missing part?", 7, [25, 8, wrong_way(16, 9)],
        "Whole − part = the other part. 16 − 9 = <b>7</b>. Check: 9 + 7 = 16.", "9 + ? = 16")
    add(fig(part_whole_svg("?", 7, 6)) + "What is the whole?", 13, [1, 12, 14],
        "The whole is the two parts added: 7 + 6 = <b>13</b>. (1 is 7 − 6.)", "7 + 6 = ?")
    opts = ["14 − 8 = 6", "8 − 6 = 2", "14 + 6 = 20", "14 + 8 = 22"]
    assert all(holds(o) for o in opts)
    add(fig(part_whole_svg(14, 8, 6)) + "Which subtraction matches the model?", opts[0], opts[1:],
        "Start with the whole and take away one part. The other part is left: <b>14 − 8 = 6</b>.")
    opts = ["13 − 4 = 9", "13 + 4 = 17", "9 − 4 = 5", "4 + 13 = 17"]
    assert all(holds(o) for o in opts)
    add("Which fact is in the same family as 9 + 4 = 13?", opts[0], opts[1:],
        "A fact family uses the same three numbers: 9, 4 and 13. <b>13 − 4 = 9</b> uses them all.")
    opts = ["9 − 6 = 3", "9 + 6 = 15", "15 − 6 = 9", "15 − 9 = 6"]
    assert all(holds(o) for o in opts)
    add("Which fact is NOT in the fact family for 6, 9 and 15?", opts[0], opts[1:],
        "<b>9 − 6 = 3</b> uses the number 3, not 15. The others use only 6, 9 and 15.")
    add("How many facts are in the fact family for 5, 8 and 13?", 4, [2, 3, 6],
        "5 + 8 = 13, 8 + 5 = 13, 13 − 5 = 8 and 13 − 8 = 5. That is <b>4</b> facts.")
    opts = ["7 + 9 = 16", "16 + 7 = 23", "7 + 6 = 13", "9 − 7 = 2"]
    assert all(holds(o) for o in opts)
    add("Which addition fact helps you work out 16 − 7?", opts[0], opts[1:],
        "Think: 7 + what = 16? <b>7 + 9 = 16</b>, so 16 − 7 = 9.")
    for a, b in [(12, 9), (15, 8), (17, 8)]:
        d = a - b
        add(fig(hop_line_svg(b, a)) + "Count up from %d to %d. What is %d − %d?" % (b, a, a, b), d,
            [d + 1, a + b, wrong_way(a, b)],
            "Think addition: %d + <b>%d</b> = %d. So %d − %d = <b>%d</b>." % (b, d, a, a, b, d), "%d − %d = ?" % (a, b))
    opts = ["8 + 6 = 14", "14 + 6 = 20", "8 + 14 = 22", "6 + 6 = 12"]
    assert all(holds(o) for o in opts)
    add("Simran says 14 − 6 = 8. Which addition checks it?", opts[0], opts[1:],
        "Add the answer to the number you took away. <b>8 + 6 = 14</b>, so Simran is right.")
    assert wrong_way(13, 4) == 11 and 13 - 4 == 9
    add("Lucas says 13 − 4 = 11. What did he do wrong?", "He took 3 from 4",
        ["He added 4", "He counted back 3", "Nothing. He is right."],
        "13 − 4 = 9. Lucas saw 3 and 4 and did 4 − 3 = 1 instead. <b>He took 3 from 4</b>. "
        "Think: 4 + 9 = 13.")
    assert len(its) == 20, len(its)
    return {"title": "Fact families and turn-around facts", "items": its}


# ============================================================ set 4: missing addends
def set_missing():
    its = []

    def add(eq, right, wrong, e, pic=None):
        assert holds(eq, right), eq
        for w in wrong:
            assert not holds(eq, w), (eq, w)
        its.append(mcq((fig(pic) if pic else "") + "Find the missing number: " + eq.replace("?", B), right, wrong, e))

    for a, t in [(9, 12), (7, 11), (8, 15), (6, 13)]:
        k = t - a
        add("%d + ? = %d" % (a, t), k, [k + 1, a + t, t],
            "Count up from %d to %d: %s. That is %d jumps, so the missing number is <b>%d</b>. "
            "(Do not count the %d you start on.)" % (a, t, ", ".join(str(v) for v in range(a + 1, t + 1)), k, k, a),
            hop_line_svg(a, t))
    add("? + 5 = 12", 7, [17, 8, 12], "Whole − part: 12 − 5 = <b>7</b>. Check: 7 + 5 = 12.",
        part_whole_svg(12, "?", 5))
    add("? + 8 = 17", 9, [25, 10, 17], "Whole − part: 17 − 8 = <b>9</b>. Check: 9 + 8 = 17.",
        part_whole_svg(17, "?", 8))
    add("5 + ? = 13", 8, [18, 9, wrong_way(13, 5)], "Whole − part: 13 − 5 = <b>8</b>. Check: 5 + 8 = 13.",
        part_whole_svg(13, 5, "?"))
    add("? + 9 = 16", 7, [25, 8, wrong_way(16, 9)], "Whole − part: 16 − 9 = <b>7</b>. Check: 7 + 9 = 16.",
        part_whole_svg(16, "?", 9))
    add("14 = 6 + ?", 8, [20, 9, 14],
        "The = sign means both sides are the same. 6 + 8 = 14, so the missing number is <b>8</b>.",
        hop_line_svg(6, 14))
    add("3 + ? = 11", 8, [9, 14, 11],
        "Count up from 3 to 11: that is 8 jumps. 3 + 8 = 11, so the missing number is <b>8</b>.",
        hop_line_svg(3, 11))
    add("? + 6 = 20", 14, [26, 4, 13],
        "6 + 4 = 10, and 10 more makes 20. 4 + 10 = 14, so the missing number is <b>14</b>. (4 only makes 10.)",
        part_whole_svg(20, "?", 6))
    add("11 + ? = 18", 7, [29, 8, 6], "1 + 7 = 8, so 11 + 7 = 18. The missing number is <b>7</b>.",
        hop_line_svg(11, 18))
    add("17 = ? + 9", 8, [26, 9, 7], "Think: 9 + 8 = 17. So the missing number is <b>8</b>.",
        part_whole_svg(17, "?", 9))
    add("8 + ? = 16", 8, [24, 9, 16], "Double 8 is 16, so the missing number is <b>8</b>.",
        part_whole_svg(16, 8, "?"))
    add("12 + ? = 19", 7, [31, 8, 6], "2 + 7 = 9, so 12 + 7 = 19. The missing number is <b>7</b>.",
        hop_line_svg(12, 19))
    add("? + 7 = 10", 3, [17, 4, 10], "7 + 3 = 10, so the missing number is <b>3</b>.",
        ten_frame_svg([RED] * 7, "ten frame with 7 counters"))
    add("9 + 9 = ? + 10", 8, [18, 28, 9],
        "9 + 9 = 18. So ? + 10 must also be 18. 8 + 10 = 18, so the missing number is <b>8</b>. "
        "(18 is only the left side.)")
    add("7 + 8 = 10 + ?", 5, [15, 25, 4],
        "7 + 8 = 15. So 10 + ? must also be 15. 10 + 5 = 15, so the missing number is <b>5</b>. "
        "(4 comes from 7 + 8 = 14.)")
    add("6 + 7 = 7 + ?", 6, [13, 7, 20],
        "You can add in any order. 6 + 7 = 7 + 6, so the missing number is <b>6</b>.")
    add("? + 6 = 4 + 9", 7, [13, 19, 8],
        "4 + 9 = 13. So ? + 6 must also be 13. 7 + 6 = 13, so the missing number is <b>7</b>. "
        "(13 is only the right side.)")
    assert len(its) == 20, len(its)
    return {"title": "Missing addends", "items": its}


# ============================================================ set 5: mixed facts and word problems
def set_words():
    its = []
    add_fact = adder(its)
    for a, op, b, wrong, e in [
        (14, "−", 9, [6, 23, wrong_way(14, 9)], "Think: 9 + 5 = 14. So 14 − 9 = <b>5</b>."),
        (9, "+", 5, [13, 15, 4], "9 + 1 = 10, then 4 more is <b>14</b>."),
        (16, "−", 8, [9, 24, wrong_way(16, 8)], "Double 8 is 16. So 16 − 8 = <b>8</b>."),
        (6, "+", 8, [13, 15, 2], "8 + 2 = 10, then 4 more is <b>14</b>."),
        (11, "−", 3, [9, 14, wrong_way(11, 3)], "11 − 1 = 10, then take away 2 more: <b>8</b>."),
        (20, "−", 7, [14, 27, 17], "Think: 7 + 13 = 20. So 20 − 7 = <b>13</b>. (17 comes from doing 7 − 0 in the ones. That subtracts the wrong way.)"),
    ]:
        v = a + b if op == "+" else a - b
        add_fact("What is %d %s %d?" % (a, op, b), v, wrong, e, "%d %s %d = ?" % (a, op, b))

    def add(q, right, unit, wrong, e, check, pic=None):
        assert check, q
        one = {"salmon": "salmon", "people": "person"}.get(unit, unit[:-1])
        f = lambda v: "%d %s" % (v, one if v == 1 else unit)
        its.append(mcq((fig(pic) if pic else "") + q, f(right), [f(v) for v in wrong], e))

    add("Liam has 8 hockey pucks. He gets 5 more. How many pucks does he have now?", 13, "pucks", [12, 3, 14],
        "Add. 8 + 2 = 10, then 3 more is <b>13</b>. (12 counts the 8 as well.)", 8 + 5 == 13,
        objects_svg("puck", [(8, "#555"), (5, BLUE)]))
    add("9 students are on the SkyTrain for a field trip. 6 more get on. How many students are on the train now?",
        15, "students", [14, 3, 16], "Add. 9 + 1 = 10, then 5 more is <b>15</b>.", 9 + 6 == 15,
        objects_svg("child", [(9, BLUE), (6, ORANGE)], noun="children"))
    add("Chloe picks 7 apples at an orchard in the Okanagan. Arjun picks 7 apples too. How many apples do they pick?",
        14, "apples", [13, 15, 7], "This is a double. 7 + 7 = <b>14</b>.", 7 + 7 == 14,
        objects_svg("apple", [(7, RED), (7, GREEN)]))
    add("6 bald eagles sit in a cedar tree. 7 more eagles land there. How many eagles are there now?", 13, "eagles",
        [12, 14, 1], "Near double: double 6 is 12, and 1 more is <b>13</b>.", 6 + 7 == 13)
    add("14 students are skating at the rink. 6 go home. How many students are still skating?", 8, "students",
        [20, 9, wrong_way(14, 6)], "Take away. 14 − 4 = 10, then take away 2 more: <b>8</b>. (20 adds instead.)",
        14 - 6 == 8, objects_svg("child", [(14, BLUE)], crossed=6, noun="children"))
    add("There are 16 rain jackets in the lost and found. Students take home 8 of them. How many jackets are left?",
        8, "jackets", [24, 9, wrong_way(16, 8)], "Double 8 is 16. So 16 − 8 = <b>8</b>.", 16 - 8 == 8)
    add("12 orcas swim near the BC Ferries boat. 5 swim away. How many orcas are left?", 7, "orcas",
        [17, 8, wrong_way(12, 5)], "Take away. 12 − 2 = 10, then take away 3 more: <b>7</b>.", 12 - 5 == 7)
    add("Mei reads 9 pages on Monday and 9 pages on Tuesday. How many pages does she read?", 18, "pages",
        [17, 19, 9], "This is a double. 9 + 9 = <b>18</b>.", 9 + 9 == 18)
    add("Our soccer team scores 6 goals in one game and 8 goals in the next game. How many goals is that?", 14,
        "goals", [13, 2, 15], "Near double: double 6 is 12, and 8 is 2 more than 6, so 12 + 2 = <b>14</b>.",
        6 + 8 == 14)
    add("Ava sees 15 salmon in the river. Kai sees 9 salmon. How many more salmon does Ava see?", 6, "salmon",
        [24, 7, wrong_way(15, 9)], "Find the difference. Count up from 9 to 15: that is <b>6</b>. (24 adds them.)",
        15 - 9 == 6)
    add("The bus to Stanley Park has 20 seats. 13 students sit down. How many seats are empty?", 7, "seats",
        [33, 8, 6], "Count up from 13 to 20: 13 + 7 = 20. So <b>7</b> seats are empty.", 20 - 13 == 7)
    add("Some people are on the gondola at Grouse Mountain. 7 more get on. Now there are 16. How many were on it at first?",
        9, "people", [23, 16, 8], "Take away the 7 that got on: 16 − 7 = <b>9</b>. Check: 9 + 7 = 16.",
        9 + 7 == 16)
    add("Zara has 8 stickers. She gets some more. Now she has 15. How many stickers did she get?", 7, "stickers",
        [23, 8, 6], "Count up from 8 to 15: that is <b>7</b>. Check: 8 + 7 = 15.", 8 + 7 == 15)
    add("11 students play outside at recess. It starts to rain and 4 go inside. Then 6 come out with rain jackets. "
        "How many students are outside now?", 13, "students", [7, 21, 1],
        "Step 1: 11 − 4 = 7. Step 2: 7 + 6 = <b>13</b>. (7 stops after step 1.)", 11 - 4 + 6 == 13)
    assert len(its) == 20, len(its)
    return {"title": "Mixed facts and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Doubles and near doubles</h2>"
        "<p>A <b>double</b> adds a number to itself: 6 + 6 = 12, 7 + 7 = 14, 8 + 8 = 16, 9 + 9 = 18.</p>"
        "<p>A <b>near double</b> uses two numbers that are 1 apart. Use the double, then add 1.</p>"
        "<figure class='sn-fig'>" + frames_split(7, 8, 1) +
        "<figcaption>7 + 8 is double 7 and 1 more: 14 + 1 = 15.</figcaption></figure>"
        "<h2>Make ten</h2>"
        "<p>Two numbers that make 10 are a pair to learn by heart.</p>"
        + table(["Makes 10", "Turn-around"], [["%d + %d" % (a, 10 - a), "%d + %d" % (10 - a, a)] for a in range(1, 6)]) +
        "<p>To add past 10, fill a ten frame first. Then add the rest.</p>"
        "<figure class='sn-fig'>" + frames_fill(9, 4) +
        "<figcaption>9 + 4: move 1 blue counter to fill the top frame. 10 + 3 = 13.</figcaption></figure>"
        + ex("Example", "What is 8 + 5?", "8 needs 2 more to make 10. Take 2 from the 5. 3 are left. 10 + 3 = 13.", "13")
        + "<h2>Fact families and turn-around facts</h2>"
        "<p>You can add in any order: 8 + 5 = 5 + 8. This is a <b>turn-around fact</b>.</p>"
        "<p>Three numbers make a <b>fact family</b>. If you know 8 + 5 = 13, you also know 13 − 5 = 8 and 13 − 8 = 5.</p>"
        "<figure class='sn-fig'>" + part_whole_svg(13, 8, 5) +
        "<figcaption>8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8 and 13 − 8 = 5.</figcaption></figure>"
        + ex("Example", "What is 12 − 9?", "Think: 9 + what = 12? Count up: 10, 11, 12. That is 3.", "3")
        + "<h2>Missing addends</h2>"
        "<p>For 8 + ? = 15, count up from 8 to 15. Do not count the 8 you start on.</p>"
        "<figure class='sn-fig'>" + hop_line_svg(8, 15, "+7") +
        "<figcaption>From 8 to 15 is 7 jumps, so 8 + 7 = 15.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the start number: 9 + 4 = 12 (9, 10, 11, 12)", "Start on 9 and count the jumps: 10, 11, 12, 13"],
            ["Subtracting the wrong way: 13 − 5 = 12 (5 − 3 = 2)", "You cannot take 5 from 3. Think: 5 + 8 = 13, so 13 − 5 = 8"],
            ["7 + 8 = 14", "7 + 7 = 14, so 7 + 8 is 1 more: 15"],
            ["8 + ? = 15, so ? = 15", "15 is the total. Find the part: 15 − 8 = 7"],
        ])
    )


FAQ = [
    {"q": "What addition and subtraction facts should a Grade 2 student know in BC?",
     "a": "The BC Mathematics Curriculum for Grade 2 lists “addition and subtraction facts to 20 (introduction of computational strategies)”. Students learn strategies such as doubles and making ten, so facts like 8 + 7 = 15 and 15 − 7 = 8 become quick to work out."},
    {"q": "What is a fact family in Grade 2 math?",
     "a": "A fact family is a set of facts that use the same three numbers. For 6, 9 and 15 they are 6 + 9 = 15, 9 + 6 = 15, 15 − 9 = 6 and 15 − 6 = 9."},
    {"q": "What are doubles and near doubles in Grade 2 math?",
     "a": "A double adds a number to itself, like 7 + 7 = 14. A near double adds two numbers that are 1 apart, like 7 + 8: use the double 14, then add 1 to get 15."},
    {"q": "How can I help my child learn facts to 20 at home?",
     "a": "Practise pairs that make 10 and the doubles for a few minutes each day, with fingers, coins or a ten frame drawn on paper. Then ask “if 8 + 5 = 13, what is 13 − 5?” so your child links adding and subtracting."},
]


def gen():
    rnd = random.Random(52803)
    sets = [set_doubles(), set_make_ten(), set_fact_families(), set_missing(), set_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "addition-and-subtraction-facts-to-20",
        "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Facts to 20: Doubles, Make Ten and Fact Families",
        "seo_title": "Grade 2 Math Addition and Subtraction Facts to 20 Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Addition and subtraction facts to 20",
        "domain": "Computational fluency",
        "standard_code": "Grade 2: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Addition and subtraction facts to 20 (introduction of computational strategies)",
        "meta_desc": "Free Grade 2 math worksheets on addition and subtraction facts to 20: doubles, near doubles, make ten, fact families, turn-around facts, missing addends and word problems. 100 questions with an answer key, following the BC curriculum.",
        "key_big": "Learn your doubles and the pairs that make 10, and every fact to 20 gets easy.",
        "key_sub": "7 + 8 is double 7 and 1 more: 15. 9 + 4 = 10 + 3 = 13. If 8 + 5 = 13, then 13 − 5 = 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line|\\d+ (?:apples|pucks|children) in groups|1\\d children")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
