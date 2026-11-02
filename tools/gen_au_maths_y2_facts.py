# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Addition and subtraction facts to 20 (Australian Curriculum v9.0, AC9M2A02)
  python3 tools/gen_au_maths_y2_facts.py
Number bonds to 10 with ten frames, doubles, near doubles and make ten, related subtraction
facts and fact families, missing numbers, and quick word problems.
Every answer and every wrong answer is checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
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


# ------------------------------------------------------------ pictures: fruit, children, shells
def icon(kind, cx, cy, col):
    if kind == "apple":
        return ("<circle cx='%d' cy='%d' r='11' fill='%s'/>"
                "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                "<ellipse cx='%d' cy='%d' rx='5' ry='3' fill='%s'/>"
                % (cx, cy + 2, col, cx, cy - 7, cx + 1, cy - 13, cx + 3, cy - 15, INK, cx + 7, cy - 12, GREEN))
    if kind == "orange":
        return ("<circle cx='%d' cy='%d' r='11' fill='%s'/><circle cx='%d' cy='%d' r='2' fill='%s'/>"
                % (cx, cy + 1, col, cx, cy - 7, GREEN))
    if kind == "grape":
        return ("<circle cx='%d' cy='%d' r='10' fill='%s'/><circle cx='%d' cy='%d' r='3' fill='#fff' opacity='0.5'/>"
                % (cx, cy + 1, col, cx - 3, cy - 3))
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


# ============================================================ set 1: number bonds to 10
def set_bonds_10():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert w == right or not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    for n in (7, 4, 9, 2, 6):
        k = 10 - n
        add(fig(ten_frame_svg([RED] * n, "ten frame with %d counters" % n)) + "How many more counters make 10?",
            k, [n, k + 1, k - 1, n + 10],
            "There %s %d %s and %d empty %s. %d + %d = 10, so <b>%d</b> more %s 10."
            % ("is" if n == 1 else "are", n, "counter" if n == 1 else "counters", k, "space" if k == 1 else "spaces",
               n, k, k, "makes" if k == 1 else "make"), "%d + ? = 10" % n)
    for n in (6, 3, 8):
        m = 10 - n
        right = "%d + %d = 10" % (n, m)
        wrong = ["%d − %d = %d" % (max(n, m), min(n, m), abs(n - m)), "%d + %d = 10" % (n, m + 1),
                 "10 + %d = %d" % (n, 10 + n)]
        assert holds(right) and not holds(wrong[1])
        add(fig(ten_frame_svg([RED] * n + [BLUE] * m, "ten frame with %d red and %d blue counters" % (n, m)))
            + "Which number sentence matches the ten frame?", right, wrong,
            "There are %d red counters and %d blue counters. Together they fill the frame: <b>%s</b>." % (n, m, right))
    for k in (3, 6, 8, 1):
        a = 10 - k
        add(fig(ten_frame_svg([RED] * 10, "ten frame with 10 counters, %d crossed out" % k, crossed=k))
            + "%d %s crossed out. What is 10 − %d?" % (k, "counter is" if k == 1 else "counters are", k),
            a, [k, a + 1, 10 + k, a - 1],
            "Count the counters with no X. 10 − %d = <b>%d</b>. Check: %d + %d = 10." % (k, a, a, k),
            "10 − %d = ?" % k)
    for whole, p1, p2, ans in [(10, 2, "?", 8), (10, "?", 5, 5), (10, "?", 7, 3)]:
        part = p1 if p2 == "?" else p2
        add(fig(part_whole_svg(whole, p1, p2)) + "What is the missing part?", ans, [10 + part, ans - 1, ans + 1, part],
            "The two parts make 10. %d + %d = 10, so the missing part is <b>%d</b>." % (part, ans, ans),
            "%d + ? = 10" % part)
    add("Which pair makes 10?", "3 + 7", ["3 + 6", "4 + 7", "2 + 7"],
        "3 + 7 = 10, so <b>3 + 7</b> makes 10. 3 + 6 = 9, 4 + 7 = 11 and 2 + 7 = 9.")
    assert 3 + 7 == 10 and 3 + 6 != 10 and 4 + 7 != 10 and 2 + 7 != 10
    add("Which pair does NOT make 10?", "4 + 5", ["1 + 9", "2 + 8", "5 + 5"],
        "4 + 5 = 9, not 10. So <b>4 + 5</b> is not a number bond to 10.")
    assert 4 + 5 != 10 and 1 + 9 == 10 and 2 + 8 == 10 and 5 + 5 == 10
    add("Find the missing number: %s + 8 = 10" % B, 2, [18, 3, 8],
        "2 + 8 = 10, so the missing number is <b>2</b>. (18 adds instead: 10 + 8.)", "? + 8 = 10")
    add("Find the missing number: %s + 1 = 10" % B, 9, [11, 8, 1],
        "9 + 1 = 10, so the missing number is <b>9</b>. (11 adds instead: 10 + 1.)", "? + 1 = 10")
    add("Find the missing number: 10 − %s = 4" % B, 6, [14, 4, 5],
        "Think: 4 + 6 = 10. So 10 − 6 = 4, and the missing number is <b>6</b>.", "10 − ? = 4")
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 10 with ten frames", "items": its}


# ============================================================ set 2: doubles, near doubles, make ten
def set_facts_20():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert w == right or not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    # doubles
    for a in (5, 6, 8):
        add(fig(frames_split(a, a)) + "Each frame has %d counters. What is %d + %d?" % (a, a, a), 2 * a,
            [2 * a - 1, 2 * a + 1, a],
            "This is a double. Double %d is <b>%d</b>." % (a, 2 * a), "%d + %d = ?" % (a, a))
    add("What is double 9?", 18, [17, 19, 9],
        "Double 9 is 9 + 9. 9 + 9 = <b>18</b>. (Think: 10 + 10 = 20, then take away 2.)", "9 + 9 = ?")
    # near doubles
    for a, show in [(4, False), (6, True), (7, True), (8, False)]:
        b = a + 1
        q = (fig(frames_split(a, b, 1)) + "Double %d and 1 more. What is %d + %d?" % (a, a, b)) if show else \
            "Use double %d. What is %d + %d?" % (a, a, b)
        add(q, a + b, [2 * a, 2 * b, b - a, a + b - 1],
            "%d + %d is a near double. Double %d is %d. %d is 1 more than %d, so add 1: <b>%d</b>."
            % (a, b, a, 2 * a, b, a, a + b), "%d + %d = ?" % (a, b))
    add("Which double helps you work out 6 + 7?", "6 + 6, then add 1",
        ["6 + 6, then take 1", "7 + 8, then add 1", "5 + 5, then add 1"],
        "7 is 1 more than 6. Double 6 is 12, then add 1: 13. So use <b>6 + 6, then add 1</b>.")
    # make ten
    for a, b in [(9, 4), (8, 5), (9, 7), (8, 6), (7, 5)]:
        need = 10 - a
        add(fig(frames_fill(a, b)) + "Fill the top frame first. What is %d + %d?" % (a, b), a + b,
            [a + b - 1, 10 + b, a + b + 1, a - b],
            "%d needs %d more to make 10. Take %d from the %d: %d is left. 10 + %d = <b>%d</b>."
            % (a, need, need, b, b - need, b - need, a + b), "%d + %d = ?" % (a, b))
    add("Make ten. 8 + 5 is the same as which?", "10 + 3", ["10 + 5", "10 + 2", "8 + 10"],
        "Move 2 from the 5 to the 8. 8 + 2 = 10 and 3 is left. So 8 + 5 = <b>10 + 3</b> = 13.")
    assert 8 + 5 == 10 + 3 and 10 + 5 != 13 and 10 + 2 != 13 and 8 + 10 != 13
    add("Make ten. 9 + 6 is the same as which?", "10 + 5", ["10 + 6", "10 + 4", "9 + 10"],
        "Move 1 from the 6 to the 9. 9 + 1 = 10 and 5 is left. So 9 + 6 = <b>10 + 5</b> = 15.")
    assert 9 + 6 == 10 + 5 and 10 + 6 != 15 and 10 + 4 != 15 and 9 + 10 != 15
    add("Start with the bigger number. What is 3 + 9?", 12, [11, 13, 6],
        "Start at 9 and count on 3: 10, 11, 12. So 3 + 9 = <b>12</b>. (11 counts the 9 as well.)", "3 + 9 = ?")
    add("Make ten. What is 6 + 9?", 15, [14, 16, 3],
        "Start with 9. Take 1 from the 6 to make 10. 5 is left. 10 + 5 = <b>15</b>.", "6 + 9 = ?")
    add("Make ten. What is 4 + 8?", 12, [11, 13, 4],
        "Start with 8. Take 2 from the 4 to make 10. 2 is left. 10 + 2 = <b>12</b>.", "4 + 8 = ?")
    add("Kai says 7 + 8 = 14. What did he do wrong?", "He did double 7 and forgot 1",
        ["He took away", "He did double 8", "Nothing. He is right."],
        "7 + 7 = 14. But 8 is 1 more than 7, so 7 + 8 = 14 + 1 = <b>15</b>. He did double 7 and forgot 1.")
    assert 7 + 8 == 15
    assert len(its) == 20, len(its)
    return {"title": "Facts to 20: doubles, near doubles and make ten", "items": its}


# ============================================================ set 3: related subtraction facts, fact families
def set_fact_families():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert w == right or not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    for a, b, wrong in [(8, 5, [9, 18, 5]), (9, 6, [10, 21, 6])]:
        add(fig(frames_fill(a, b)) + "The frames show %d + %d = %d. Take away the blue counters. What is %d − %d?"
            % (a, b, a + b, a + b, b), a, wrong,
            "Take away the %d blue counters. The %d red counters are left. %d − %d = <b>%d</b>."
            % (b, a, a + b, b, a), "%d − %d = ?" % (a + b, b))
    for a, b, wrong in [(7, 5, [6, 19, 7]), (8, 6, [7, 22, 8])]:
        add(fig(frames_fill(a, b)) + "%d + %d = %d. Use this fact. What is %d − %d?" % (a, b, a + b, a + b, a), b,
            wrong, "If %d + %d = %d, then %d − %d = <b>%d</b>. Take away the red counters and the blue ones are left."
            % (a, b, a + b, a + b, a, b), "%d − %d = ?" % (a + b, a))
    for a, b, wrong in [(6, 5, [6, 17, 4]), (9, 8, [9, 26, 7])]:
        add("%d + %d = %d. Use this fact. What is %d − %d?" % (a, b, a + b, a + b, a), b, wrong,
            "If %d + %d = %d, then %d − %d = <b>%d</b>. Subtraction undoes addition." % (a, b, a + b, a + b, a, b),
            "%d − %d = ?" % (a + b, a))
    add(fig(part_whole_svg(16, 9, "?")) + "What is the missing part?", 7, [25, 8, 9],
        "Whole − part = the other part. 16 − 9 = <b>7</b>. Check: 9 + 7 = 16.", "9 + ? = 16")
    add(fig(part_whole_svg("?", 7, 6)) + "What is the whole?", 13, [1, 12, 14],
        "The whole is the two parts added: 7 + 6 = <b>13</b>. (1 is 7 − 6.)", "7 + 6 = ?")
    add(fig(part_whole_svg(14, "?", 8)) + "What is the missing part?", 6, [22, 7, 5],
        "14 − 8 = <b>6</b>. Check: 6 + 8 = 14. (22 adds instead of taking away.)", "? + 8 = 14")
    opts = ["14 − 8 = 6", "8 − 6 = 2", "14 + 6 = 20", "14 + 8 = 22"]
    assert all(holds(o) for o in opts)
    add(fig(part_whole_svg(14, 8, 6)) + "Which subtraction matches the model?", opts[0], opts[1:],
        "Start with the whole and take away one part. The other part is left: <b>14 − 8 = 6</b>.")
    opts = ["7 + 8 = 15", "8 − 7 = 1", "15 + 7 = 22", "7 + 8 = 14"]
    assert holds(opts[0]) and not holds(opts[3])
    add(fig(part_whole_svg(15, 7, 8)) + "Which addition matches the model?", opts[0], opts[1:],
        "Add the two parts to get the whole: <b>7 + 8 = 15</b>. (7 + 8 is not 14. That is 7 + 7.)")
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
    # think addition: count up on a number line
    for a, b, wrong in [(12, 9, [4, 21, 7]), (13, 6, [8, 19, 3]), (15, 8, [8, 23, 3]), (17, 8, [10, 25, 1])]:
        d = a - b
        add(fig(hop_line_svg(b, a)) + "Count up from %d to %d. What is %d − %d?" % (b, a, a, b), d, wrong,
            "Think addition: %d + <b>%d</b> = %d. So %d − %d = <b>%d</b>." % (b, d, a, a, b, d), "%d − %d = ?" % (a, b))
    opts = ["8 + 6 = 14", "14 + 6 = 20", "8 + 14 = 22", "6 + 6 = 12"]
    assert all(holds(o) for o in opts)
    add("Mia says 14 − 6 = 8. Which addition checks it?", opts[0], opts[1:],
        "Add the answer to the number you took away. <b>8 + 6 = 14</b>, so Mia is right.")
    assert len(its) == 20, len(its)
    return {"title": "Related subtraction facts and fact families", "items": its}


# ============================================================ set 4: missing numbers
def set_missing():
    its = []

    def add(eq, right, wrong, e, pic=None):
        assert holds(eq, right), eq
        for w in wrong:
            assert not holds(eq, w), (eq, w)
        its.append(mcq((fig(pic) if pic else "") + "Find the missing number: " + eq.replace("?", B), right, wrong, e))

    for a, t, wrong in [(9, 12, [4, 21, 12]), (7, 11, [5, 18, 11]), (8, 15, [8, 23, 15]), (6, 13, [8, 19, 13])]:
        k = t - a
        add("%d + ? = %d" % (a, t), k, wrong,
            "Count up from %d to %d: %s. That is %d jumps, so the missing number is <b>%d</b>. "
            "(Do not count the %d you start on.)" % (a, t, ", ".join(str(v) for v in range(a + 1, t + 1)), k, k, a),
            hop_line_svg(a, t))
    add("? + 5 = 12", 7, [17, 8, 12], "Whole − part: 12 − 5 = <b>7</b>. Check: 7 + 5 = 12.",
        part_whole_svg(12, "?", 5))
    add("? + 8 = 17", 9, [25, 10, 17], "Whole − part: 17 − 8 = <b>9</b>. Check: 9 + 8 = 17.",
        part_whole_svg(17, "?", 8))
    add("14 = 6 + ?", 8, [20, 9, 14],
        "The = sign means both sides are the same. 6 + 8 = 14, so the missing number is <b>8</b>.",
        hop_line_svg(6, 14))
    add("15 − ? = 9", 6, [24, 7, 9],
        "Count up from 9 to 15: that is 6. So 15 − 6 = 9, and the missing number is <b>6</b>.",
        hop_line_svg(9, 15))
    add("13 − ? = 5", 8, [18, 9, 5],
        "Think: 5 + 8 = 13. So 13 − 8 = 5, and the missing number is <b>8</b>.", part_whole_svg(13, "?", 5))
    add("? − 4 = 9", 13, [5, 12, 14],
        "You took 4 away and 9 were left. Put the 4 back: 9 + 4 = <b>13</b>. Check: 13 − 4 = 9. (5 takes away instead.)",
        part_whole_svg("?", 4, 9))
    add("? − 7 = 8", 15, [1, 14, 16],
        "Put the 7 back: 8 + 7 = <b>15</b>. Check: 15 − 7 = 8. (8 + 7 is not 14.)", part_whole_svg("?", 7, 8))
    add("20 − ? = 14", 6, [34, 7, 5], "Count up from 14 to 20: that is 6. So the missing number is <b>6</b>.",
        hop_line_svg(14, 20))
    add("? + 6 = 20", 14, [26, 4, 13],
        "6 + 4 = 10, and 10 more makes 20. 4 + 10 = 14, so the missing number is <b>14</b>. (4 only makes 10.)",
        part_whole_svg(20, "?", 6))
    add("11 + ? = 18", 7, [29, 8, 6], "1 + 7 = 8, so 11 + 7 = 18. The missing number is <b>7</b>.",
        hop_line_svg(11, 18))
    add("17 = ? + 9", 8, [26, 9, 7], "Think: 9 + 8 = 17. So the missing number is <b>8</b>.",
        part_whole_svg(17, "?", 9))
    add("12 = 20 − ?", 8, [32, 9, 7], "Count up from 12 to 20: that is 8. So 20 − 8 = 12. The missing number is <b>8</b>.",
        hop_line_svg(12, 20))
    add("9 + 9 = ? + 10", 8, [18, 28, 9],
        "9 + 9 = 18. So ? + 10 must also be 18. 8 + 10 = 18, so the missing number is <b>8</b>. "
        "(18 is only the left side.)")
    add("7 + 8 = 10 + ?", 5, [15, 25, 4],
        "7 + 8 = 15. So 10 + ? must also be 15. 10 + 5 = 15, so the missing number is <b>5</b>. "
        "(4 comes from 7 + 8 = 14.)")
    add("6 + 7 = 7 + ?", 6, [13, 7, 20],
        "You can add in any order. 6 + 7 = 7 + 6, so the missing number is <b>6</b>.")
    opts = ["8 + 7 = 15", "8 + 7 = 14", "15 − 7 = 9", "9 + 6 = 14"]
    assert holds(opts[0]) and not any(holds(o) for o in opts[1:])
    its.append(mcq("Which number sentence is true?", opts[0], opts[1:],
                   "8 + 7 = 15, so <b>8 + 7 = 15</b> is true. 15 − 7 = 8, not 9, and 9 + 6 = 15, not 14."))
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def add(q, right, unit, wrong, e, check, pic=None):
        assert check, q
        one = {"strawberries": "strawberry", "students": "student"}.get(unit, unit[:-1])
        f = lambda v: "%d %s" % (v, one if v == 1 else unit)
        its.append(mcq((fig(pic) if pic else "") + q, f(right), [f(v) for v in wrong], e))

    add("Isla has 8 apples. She gets 5 more. How many apples does she have now?", 13, "apples", [12, 3, 14],
        "Add. 8 + 2 = 10, then 3 more is <b>13</b>. (12 counts the 8 as well.)", 8 + 5 == 13,
        objects_svg("apple", [(8, RED), (5, GREEN)]))
    add("There are 9 students on the bus. 6 more get on. How many students are on the bus now?", 15, "students",
        [14, 3, 16], "Add. 9 + 1 = 10, then 5 more is <b>15</b>.", 9 + 6 == 15,
        objects_svg("child", [(9, BLUE), (6, ORANGE)], noun="children"))
    add("Jack eats 7 grapes at recess. Mia eats 7 grapes too. How many grapes do they eat?", 14, "grapes",
        [13, 15, 7], "This is a double. 7 + 7 = <b>14</b>.", 7 + 7 == 14,
        objects_svg("grape", [(7, PURPLE), (7, GREEN)]))
    add("Noah has 6 strawberries. Ava has 7 strawberries. How many strawberries do they have altogether?",
        13, "strawberries", [12, 14, 1], "Near double: double 6 is 12, and 1 more is <b>13</b>.", 6 + 7 == 13)
    add("There are 16 oranges in the fruit bowl. Year 2 eats 8 at recess. How many oranges are left?", 8, "oranges",
        [24, 9, 7], "Take away. 8 + 8 = 16, so 16 − 8 = <b>8</b>.", 16 - 8 == 8,
        objects_svg("orange", [(16, ORANGE)], crossed=8))
    add("4 koalas sit in one tree. 9 koalas sit in another tree. How many koalas are there?", 13, "koalas",
        [12, 5, 14], "Start with the bigger number: 9 + 1 = 10, then 3 more is <b>13</b>.", 4 + 9 == 13)
    add("There are 14 students on the bus. 6 get off. How many students are still on the bus?", 8, "students",
        [20, 9, 12], "Take away. 14 − 4 = 10, then take away 2 more: <b>8</b>. (20 adds instead of taking away.)",
        14 - 6 == 8, objects_svg("child", [(14, BLUE)], crossed=6, noun="children"))
    add("12 kookaburras sit on a fence. 5 fly away. How many kookaburras are left?", 7, "kookaburras",
        [17, 8, 6], "Take away. 12 − 2 = 10, then take away 3 more: <b>7</b>.", 12 - 5 == 7)
    add("Grace reads 9 pages on Monday and 9 pages on Tuesday. How many pages does she read?", 18, "pages",
        [17, 19, 9], "This is a double. 9 + 9 = <b>18</b>.", 9 + 9 == 18)
    add("Our footy team kicks 6 goals, then 8 more goals. How many goals is that?", 14, "goals",
        [13, 2, 15], "Near double: double 6 is 12, and 8 is 2 more than 6, so 12 + 2 = <b>14</b>.", 6 + 8 == 14)
    add("The canteen has 17 icy poles. It sells 9. How many icy poles are left?", 8, "icy poles",
        [26, 9, 12], "Think addition: 9 + 8 = 17. So 17 − 9 = <b>8</b>.", 17 - 9 == 8)
    add("Ruby finds 18 shells at the beach. She gives 9 to her brother. How many shells does she have now?",
        9, "shells", [27, 10, 11], "Half of 18 is 9, because 9 + 9 = 18. So 18 − 9 = <b>9</b>.", 18 - 9 == 9)
    add("Leo has 15 footy cards. Kai has 9 footy cards. How many more cards does Leo have?", 6, "cards",
        [24, 7, 5], "Find the difference. Count up from 9 to 15: that is <b>6</b>. (24 adds them.)", 15 - 9 == 6)
    add("The bus has 20 seats. 13 students sit down. How many seats are empty?", 7, "seats",
        [33, 17, 8], "Count up from 13 to 20: 13 + 7 = 20. So <b>7</b> seats are empty.", 20 - 13 == 7)
    add("Some students are on the bus. 7 more get on. Now there are 16. How many were on the bus at first?",
        9, "students", [23, 16, 8], "Take away the 7 that got on: 16 − 7 = <b>9</b>. Check: 9 + 7 = 16.",
        9 + 7 == 16)
    add("Zara has 8 stickers. She gets some more. Now she has 15. How many stickers did she get?", 7, "stickers",
        [23, 8, 6], "Count up from 8 to 15: that is <b>7</b>. Check: 8 + 7 = 15.", 8 + 7 == 15)
    its.append(mcq("Cooper has $12. He spends $5 at the school fete. How much money does he have left?",
                   "$7", ["$17", "$8", "$6"],
                   "Take away. $12 − $2 = $10, then take away $3 more: <b>$7</b>."))
    assert 12 - 5 == 7
    add("13 students are in the pool at the swimming carnival. 5 get out. How many are still in the pool?",
        8, "students", [18, 9, 7], "Take away. 13 − 3 = 10, then take away 2 more: <b>8</b>.", 13 - 5 == 8)
    add("There are 11 students on the bus. 4 get off. Then 6 get on. How many students are on the bus now?",
        13, "students", [7, 21, 1], "Step 1: 11 − 4 = 7. Step 2: 7 + 6 = <b>13</b>. (7 stops after step 1.)",
        11 - 4 + 6 == 13)
    opts = ["7 + 8 = 15", "7 + 8 = 14", "8 − 7 = 1", "15 + 7 = 22"]
    assert holds(opts[0]) and not holds(opts[1])
    its.append(mcq(fig(objects_svg("apple", [(7, RED), (8, GREEN)])) +
                   "Chloe has 7 apples. She buys 8 more. Which number sentence shows how many she has?",
                   opts[0], opts[1:],
                   "She gets more, so add. 7 + 8 is double 7 and 1 more: <b>7 + 8 = 15</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Start with number bonds to 10</h2>"
        "<p>Two numbers that make 10 are a <b>number bond to 10</b>. A ten frame shows them. "
        "Count the counters and the empty spaces.</p>"
        "<figure class='sn-fig'>" + ten_frame_svg([RED] * 7, "ten frame with 7 counters") +
        "<figcaption>7 counters and 3 empty spaces: 7 + 3 = 10.</figcaption></figure>"
        + table(["Bond to 10", "Turned around"], [["%d + %d" % (a, 10 - a), "%d + %d" % (10 - a, a)] for a in range(1, 6)]) +
        "<h2>Three ways to add to 20</h2>"
        "<p><b>Doubles.</b> 6 + 6 = 12, 7 + 7 = 14, 8 + 8 = 16, 9 + 9 = 18.</p>"
        "<p><b>Near doubles.</b> 7 + 8 is double 7 and 1 more: 14 + 1 = 15.</p>"
        "<p><b>Make ten.</b> Fill a ten frame first, then add the rest.</p>"
        "<figure class='sn-fig'>" + frames_fill(9, 4) +
        "<figcaption>9 + 4: move 1 blue counter to fill the top frame. 10 + 3 = 13.</figcaption></figure>"
        + ex("Example", "What is 8 + 5?", "8 needs 2 more to make 10. Take 2 from the 5. 3 is left. 10 + 3 = 13.", "13")
        + "<h2>Use addition to subtract</h2>"
        "<p>Three numbers make a <b>fact family</b>. If you know 8 + 5 = 13, you also know 13 − 5 = 8 and 13 − 8 = 5.</p>"
        "<figure class='sn-fig'>" + part_whole_svg(13, 8, 5) +
        "<figcaption>8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8 and 13 − 8 = 5.</figcaption></figure>"
        + ex("Example", "What is 12 − 9?", "Think: 9 + what = 12? Count up: 10, 11, 12. That is 3.", "3")
        + "<h2>Missing numbers</h2>"
        "<p>For 8 + ? = 15, count up from 8 to 15. Do not count the 8 you start on.</p>"
        "<figure class='sn-fig'>" + hop_line_svg(8, 15, "+7") +
        "<figcaption>From 8 to 15 is 7 jumps, so 8 + 7 = 15.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the start number: 9 + 4 = 12 (9, 10, 11, 12)", "Start on 9 and count the jumps: 10, 11, 12, 13"],
            ["Mixing + and −: 14 − 6 = 20", "Read the sign first. Taking away gives a smaller number"],
            ["7 + 8 = 14", "7 + 7 = 14, so 7 + 8 is 1 more: 15"],
            ["8 + ? = 15, so ? = 15", "15 is the total. Find the part: 15 − 8 = 7"],
        ])
    )


FAQ = [
    {"q": "What addition facts should a Year 2 student know?",
     "a": "The Australian Curriculum expects Year 2 students to recall addition facts to 20, such as 7 + 8 = 15, and use them to work out the related subtraction facts, such as 15 − 8 = 7."},
    {"q": "What are near doubles in maths?",
     "a": "A near double is two numbers that are 1 apart, like 6 + 7. Use the double you know, 6 + 6 = 12, then add 1 to get 13."},
    {"q": "What is the make ten strategy?",
     "a": "Move part of one number to make 10 first. For 9 + 4, move 1 to the 9 to make 10, then add the 3 left: 10 + 3 = 13."},
    {"q": "How can I help my child learn facts to 20 at home?",
     "a": "Practise bonds to 10 with fingers or an egg carton, then doubles, for a few minutes every day. Ask “if 8 + 5 = 13, what is 13 − 5?” so your child links adding and subtracting."},
]


def gen():
    rnd = random.Random(2802)
    sets = [set_bonds_10(), set_facts_20(), set_fact_families(), set_missing(), set_words()]
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
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "addition-and-subtraction-facts-to-20",
        "sort": 2, "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Facts to 20",
        "seo_title": "Year 2 Addition and Subtraction Facts to 20 Worksheets: Bonds to 10, Doubles and Fact Families",
        "short_title": "Addition and subtraction facts to 20",
        "domain": "Algebra",
        "standard_code": "AC9M2A02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recall and demonstrate proficiency with addition facts to 20; extend and apply facts to develop the related subtraction facts",
        "meta_desc": "Free Year 2 maths worksheets on addition and subtraction facts to 20: number bonds to 10 with ten frames, doubles, near doubles, make ten, fact families, missing numbers and word problems. 100 questions with an answer key, matched to the Australian Curriculum.",
        "key_big": "Know your bonds to 10 and your doubles, and every fact to 20 gets easy.",
        "key_sub": "7 + 3 = 10. 7 + 8 is double 7 and 1 more: 15. 9 + 4 = 10 + 3 = 13. If 8 + 5 = 13, then 13 − 5 = 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line|\\d+ (?:apples|grapes|children) in groups|1\\d (?:oranges|children)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
