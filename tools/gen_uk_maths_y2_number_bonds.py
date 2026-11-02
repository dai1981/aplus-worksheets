# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Number bonds to 20 and 100 (National Curriculum in England)
  python3 tools/gen_uk_maths_y2_number_bonds.py
Number bonds to 10 and 20, related subtraction facts and fact families, bonds of tens to 100,
order (commutative addition) and the inverse, and word problems.
Ten frames, part-whole models, tens rods and number lines. Every answer is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#2e6fb7"
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
    """'13 + ? = 20' with ? = ans is true (− is the real minus sign)."""
    s = eq.replace(B, "?").replace("?", str(ans)).replace("−", "-").replace(",", "")
    parts = [p.strip() for p in s.split("=")]
    vals = [eval(p, {"__builtins__": {}}) for p in parts]
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


def frame(x0, y0, colors):
    """One ten frame. colors: up to 10 counter colours, top row first, left to right."""
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
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s'/>"
                 % (x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2, col))
    return "".join(s)


def ten_frame_svg(n):
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, [RED] * n), "ten frame with %d counters" % n)


def two_frames_svg(colors, label):
    """Two ten frames stacked (compact for print). colors: up to 20 counter colours."""
    o, gap = 6, 12
    body = frame(o, o, colors[:10]) + frame(o, o + FH + gap, colors[10:])
    return svg_wrap(FW + 2 * o, 2 * FH + gap + 2 * o, body, label)


# ------------------------------------------------------------ pictures: part-whole model
def part_whole_svg(whole, p1, p2):
    """Whole on top, two parts below. Values are numbers or '?'."""
    r = 28
    W, H = 184, 148
    cw, cy0 = (W / 2, 6 + r)
    c1, c2, cy1 = (8 + r, W - 8 - r, H - 6 - r)
    s = []
    for cx in (c1, c2):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (cw, cy0 + r - 2, cx, cy1 - r + 2, INK))
    for cx, cy, v, fill in [(cw, cy0, whole, FILL), (c1, cy1, p1, "#fff"), (c2, cy1, p2, "#fff")]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "part-whole model: whole %s, parts %s and %s" % (whole, p1, p2))


# ------------------------------------------------------------ pictures: tens rods
def tens_rods_svg(k):
    """10 rods of ten (100 in all). The first k are shaded."""
    C, gap, o = 10, 6, 6
    s = []
    for i in range(10):
        x = o + i * (C + gap)
        fill = FILL if i < k else "#fff"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, o, C, 10 * C, fill, GREEN))
        for g in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.7'/>"
                     % (x, o + g * C, x + C, o + g * C, GREEN))
    W = 2 * o + 10 * C + 9 * gap
    return svg_wrap(W, 2 * o + 10 * C, "".join(s), "100 shown as 10 tens, %d tens shaded" % k)


# ------------------------------------------------------------ pictures: number line
def number_line_svg(ticks, hops, unit):
    """ticks: values with a label; hops: list of (from, to, label). unit: px per 1."""
    lo, hi = ticks[0], ticks[-1]
    L, ly, ry = 22, 58, 26
    W = 2 * L + (hi - lo) * unit
    X = lambda v: L + (v - lo) * unit
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 14, ly, W - L + 14, ly, INK)]
    for a, b, lab in hops:
        x1, x2 = X(a), X(b)
        s.append("<path d='M %d %d A %.1f %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, (x2 - x1) / 2, ry, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 8, lab, 16, col=RED if lab == "?" else GREEN))
    for v in ticks:
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), ly - 7, X(v), ly + 7, INK))
        s.append(text(X(v), ly + 26, str(v), 15))
    return svg_wrap(W, ly + 34, "".join(s), "number line from %d to %d" % (lo, hi))


# ------------------------------------------------------------ typical mistakes for bonds
def bond_wrong(a, total):
    """Wrong answers for a + ? = total (and total − a)."""
    c = total - a
    if total == 10:
        return [c - 1, c + 1, a + 10]
    if total == 20:
        if a > 10:
            return [20 - a % 10, c - 1, c + 1, a + 20]       # 13 + ? = 20 → 17 (bond of 3 to 20)
        return [10 - a, c - 1, c + 1, a + 20]                 # 4 + ? = 20 → 6 (bond to 10 only)
    return [c // 10, c - 10, c + 10, a + 100]                 # 60 + ? = 100 → 4, 30, 50, 160


def bond_e(a, total):
    c = total - a
    if total == 10:
        return "%d and %d make 10. So the missing number is <b>%d</b>. Check: %d + %d = 10." % (a, c, c, a, c)
    if total == 20:
        if a > 10:
            o = a % 10
            return ("%d is 10 and %d. %d + %d = 10, and 10 + 10 = 20. So the missing number is <b>%d</b>. "
                    "Check: %d + %d = 20." % (a, o, o, c, c, a, c))
        return ("%d + %d = 10. You need 10 more to make 20. %d + 10 = %d, so the missing number is <b>%d</b>. "
                "Check: %d + %d = 20." % (a, 10 - a, 10 - a, c, c, a, c))
    tn = lambda k: "%d %s" % (k, "ten" if k == 1 else "tens")
    return ("%d + %d = 10, so %s + %s = 10 tens = 100. The missing number is <b>%d</b>."
            % (a // 10, c // 10, tn(a // 10), tn(c // 10), c))


# ============================================================ set 1: number bonds to 10 and 20
def set_bonds_10_20():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    for n in (7, 4, 9):
        add(fig(ten_frame_svg(n)) + "How many more counters fill the ten frame?", 10 - n,
            [n, 10 - n - 1, 10 - n + 1, n + 10],
            "There are %d counters and %d empty %s. %d + %d = 10, so <b>%d</b> more %s the frame."
            % (n, 10 - n, "space" if n == 9 else "spaces", n, 10 - n, 10 - n, "fills" if n == 9 else "fill"),
            "%d + ? = 10" % n)
    add(fig(part_whole_svg(10, 2, "?")) + "What is the missing part?", 8, [12, 7, 9],
        "The parts make the whole. 2 + 8 = 10, so the missing part is <b>8</b>. (12 adds instead: 10 + 2.)", "2 + ? = 10")
    for eq, a in [("6 + %s = 10", 6), ("%s + 5 = 10", 5), ("10 = 3 + %s", 3), ("1 + %s = 10", 1)]:
        e = eq % B
        add("Find the missing number: " + e, 10 - a, bond_wrong(a, 10), bond_e(a, 10), e)
    add("Which pair is a number bond to 10?", "6 + 4", ["6 + 5", "7 + 4", "3 + 6"],
        "6 + 4 = 10, so <b>6 + 4</b> is a number bond to 10. 6 + 5 = 11, 7 + 4 = 11 and 3 + 6 = 9.")
    assert 6 + 4 == 10 and 6 + 5 != 10 and 7 + 4 != 10 and 3 + 6 != 10
    for n in (14, 17):
        add(fig(two_frames_svg([RED] * n, "two ten frames with %d counters" % n))
            + "How many more counters make 20?", 20 - n, bond_wrong(n, 20),
            "The top frame is full: 10. The bottom frame has %d, with %d empty spaces. So <b>%d</b> more make 20."
            % (n - 10, 20 - n, 20 - n), "%d + ? = 20" % n)
    add(fig(part_whole_svg(20, 15, "?")) + "What is the missing part?", 5, bond_wrong(15, 20),
        "15 is 10 and 5. 5 + 5 = 10, and 10 + 10 = 20. So the missing part is <b>5</b>. Check: 15 + 5 = 20.",
        "15 + ? = 20")
    for eq, a in [("13 + %s = 20", 13), ("16 + %s = 20", 16), ("%s + 12 = 20", 12), ("20 = 11 + %s", 11),
                  ("5 + %s = 20", 5), ("3 + %s = 20", 3)]:
        e = eq % B
        add("Find the missing number: " + e, 20 - a, bond_wrong(a, 20), bond_e(a, 20), e)
    add(fig(number_line_svg(list(range(10, 21)), [(18, 20, "?")], 28)) + "How many more from 18 make 20?",
        2, [8, 3, 38], "Count on from 18: 19, 20. That is <b>2</b>. 8 + 2 = 10, so 18 + 2 = 20.", "18 + ? = 20")
    add("Which pair makes 20?", "14 + 6", ["4 + 6", "14 + 7", "13 + 6"],
        "4 + 6 = 10, so 14 + 6 = <b>20</b>. 4 + 6 only makes 10. 14 + 7 = 21 and 13 + 6 = 19.")
    assert 14 + 6 == 20 and 4 + 6 != 20 and 14 + 7 != 20 and 13 + 6 != 20
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 10 and 20", "items": its}


# ============================================================ set 2: related facts and fact families
def set_fact_families():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    def true(s):
        return holds(s)

    add(fig(two_frames_svg([RED] * 8 + [BLUE] * 5, "two ten frames with 8 red and 5 blue counters"))
        + "The frames show 8 + 5 = 13. What is 13 − 5?", 8, [7, 18, 5],
        "Take away the 5 blue counters. The 8 red counters are left. 13 − 5 = <b>8</b>.", "13 − 5 = ?")
    add("8 + 5 = 13. Use this fact. What is 13 − 8?", 5, [6, 21, 8],
        "If 8 + 5 = 13, then 13 − 8 = <b>5</b>. Subtraction undoes addition.", "13 − 8 = ?")
    add("7 + 6 = 13. Use this fact. What is 13 − 6?", 7, [8, 19, 6],
        "If 7 + 6 = 13, then 13 − 6 = <b>7</b>.", "13 − 6 = ?")
    add("9 + 6 = 15. Use this fact. What is 15 − 9?", 6, [7, 24, 9],
        "If 9 + 6 = 15, then 15 − 9 = <b>6</b>.", "15 − 9 = ?")
    opts = ["13 − 8 = 5", "8 − 5 = 3", "13 + 8 = 21", "5 + 13 = 18"]
    assert all(true(o) for o in opts)
    add(fig(part_whole_svg(13, 8, 5)) + "Which subtraction matches the model?", opts[0], opts[1:],
        "Start with the whole and take away one part. The other part is left: <b>13 − 8 = 5</b>.")
    opts = ["12 + 8 = 20", "12 − 8 = 4", "20 + 8 = 28", "20 + 12 = 32"]
    assert all(true(o) for o in opts)
    add(fig(part_whole_svg(20, 12, 8)) + "Which addition matches the model?", opts[0], opts[1:],
        "Add the two parts to get the whole: <b>12 + 8 = 20</b>.")
    opts = ["11 − 4 = 7", "11 + 4 = 15", "7 − 4 = 3", "4 + 11 = 15"]
    assert all(true(o) for o in opts)
    add("Which fact is in the same family as 7 + 4 = 11?", opts[0], opts[1:],
        "A fact family uses the same three numbers: 7, 4 and 11. <b>11 − 4 = 7</b> uses them all.")
    opts = ["9 − 6 = 3", "9 + 6 = 15", "15 − 6 = 9", "15 − 9 = 6"]
    assert all(true(o) for o in opts)
    add("Which fact is NOT in the fact family for 6, 9 and 15?", opts[0], opts[1:],
        "<b>9 − 6 = 3</b> uses the number 3, not 15. The others use only 6, 9 and 15.")
    add("How many facts are in the fact family for 5, 8 and 13?", 4, [2, 3, 8],
        "5 + 8 = 13, 8 + 5 = 13, 13 − 5 = 8, 13 − 8 = 5. That is <b>4</b> facts.")
    for a, b, wrong, e in [
            (13, 5, [7, 18, 12], "Think: 5 + 8 = 13. So 13 − 5 = <b>8</b>. (12 comes from 5 − 3 in the ones.)"),
            (14, 6, [7, 20, 12], "Think: 6 + 8 = 14. So 14 − 6 = <b>8</b>. (12 comes from 6 − 4 in the ones.)"),
            (15, 7, [12, 22, 7], "Think: 7 + 8 = 15. So 15 − 7 = <b>8</b>."),
            (20, 6, [4, 26, 13], "Think: 6 + 14 = 20. So 20 − 6 = <b>14</b>. (4 is the bond to 10, not to 20.)"),
            (20, 13, [17, 8, 33], "Think: 13 + 7 = 20. So 20 − 13 = <b>7</b>."),
            (11, 3, [12, 14, 7], "Think: 3 + 8 = 11. So 11 − 3 = <b>8</b>. (12 comes from 3 − 1 in the ones.)"),
            (12, 9, [17, 21, 4], "Think: 9 + 3 = 12. So 12 − 9 = <b>3</b>.")]:
        eq = "%d − %d = ?" % (a, b)
        add("What is %d − %d?" % (a, b), a - b, wrong, e, eq)
    opts = ["8 + 8 = 16", "16 + 8 = 24", "8 + 16 = 24", "6 + 8 = 14"]
    assert all(true(o) for o in opts)
    add("16 − 8 = 8. Which addition checks it?", opts[0], opts[1:],
        "Add the answer to the number you took away. <b>8 + 8 = 16</b>, so 16 − 8 = 8 is right.")
    add("9 + 8 = 17. Use this fact. What is 17 − 8?", 9, [10, 25, 11],
        "If 9 + 8 = 17, then 17 − 8 = <b>9</b>.", "17 − 8 = ?")
    add(fig(part_whole_svg("?", 6, 9)) + "What is the whole?", 15, [3, 14, 16],
        "The whole is the two parts added: 6 + 9 = <b>15</b>. (3 is 9 − 6.)", "6 + 9 = ?")
    add(fig(part_whole_svg(17, 9, "?")) + "What is the missing part?", 8, [26, 7, 12],
        "Whole − part = the other part. 17 − 9 = <b>8</b>. Check: 9 + 8 = 17.", "9 + ? = 17")
    assert len(its) == 20, len(its)
    return {"title": "Related facts and fact families", "items": its}


# ============================================================ set 3: number bonds to 100
def set_bonds_100():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    add("3 + 7 = 10. Use this fact. What is 30 + 70?", 100, [10, "1,000", 110],
        "3 tens + 7 tens = 10 tens. 10 tens = <b>100</b>.", "30 + 70 = ?")
    add("4 + 6 = 10. Use this fact. What is 40 + 60?", 100, [10, 90, "1,000"],
        "4 tens + 6 tens = 10 tens = <b>100</b>.", "40 + 60 = ?")
    for k in (6, 3):
        a = 10 * k
        add(fig(tens_rods_svg(k)) + "The rods show 100. %d tens are shaded. Find the missing number: %d + %s = 100"
            % (k, a, B), 100 - a, bond_wrong(a, 100),
            "Count the white rods: %d tens = <b>%d</b>. Check: %d + %d = 100." % (10 - k, 100 - a, a, 100 - a),
            "%d + ? = 100" % a)
    for eq, a in [("80 + %s = 100", 80), ("%s + 50 = 100", 50), ("100 = 10 + %s", 10)]:
        e = eq % B
        add("Find the missing number: " + e, 100 - a, bond_wrong(a, 100), bond_e(a, 100), e)
    for a in (40, 70, 90):
        c = 100 - a
        add("What is 100 − %d?" % a, c, [c // 10, c + 10, 100 + a],
            "Think: %d + %d = 100. So 100 − %d = <b>%d</b>." % (a, c, a, c), "100 − %d = ?" % a)
    add(fig(part_whole_svg(100, 20, "?")) + "What is the missing part?", 80, [8, 120, 90],
        "2 + 8 = 10, so 20 + 80 = 100. The missing part is <b>80</b>.", "20 + ? = 100")
    add("Which pair makes 100?", "30 + 70", ["30 + 60", "40 + 70", "3 + 7"],
        "3 + 7 = 10, so <b>30 + 70</b> = 100. 3 + 7 only makes 10. 30 + 60 = 90 and 40 + 70 = 110.")
    assert 30 + 70 == 100 and 30 + 60 != 100 and 40 + 70 != 100
    add("Which pair does NOT make 100?", "50 + 60", ["50 + 50", "20 + 80", "90 + 10"],
        "5 + 6 = 11, so <b>50 + 60</b> = 110, not 100. The others are bonds to 100: 5 + 5, 2 + 8 and 9 + 1 make 10.")
    assert 50 + 60 != 100 and 50 + 50 == 100 and 20 + 80 == 100 and 90 + 10 == 100
    add(fig(number_line_svg([70, 80, 90, 100], [(70, 80, "+10"), (80, 90, "+10"), (90, 100, "+10")], 6))
        + "Count on in tens from 70 to 100. How much is that?", 30, [3, 40, 170],
        "There are 3 jumps of 10. 3 tens = <b>30</b>. Check: 70 + 30 = 100.", "70 + ? = 100")
    add("8 − 3 = 5. Use this fact. What is 80 − 30?", 50, [5, 110, 500],
        "8 tens − 3 tens = 5 tens = <b>50</b>.", "80 − 30 = ?")
    add("6 − 4 = 2. Use this fact. What is 60 − 40?", 20, [2, 100, 200],
        "6 tens − 4 tens = 2 tens = <b>20</b>.", "60 − 40 = ?")
    add("5 + 4 = 9. Use this fact. What is 50 + 40?", 90, [9, 900, 80],
        "5 tens + 4 tens = 9 tens = <b>90</b>.", "50 + 40 = ?")
    add("3 + 4 = 7. Use this fact. What is 23 + 4?", 27, [63, 7, 28],
        "4 is 4 ones. Add it to the 3 ones: 3 + 4 = 7. The 2 tens stay. 23 + 4 = <b>27</b>. "
        "(63 adds 4 tens by mistake.)", "23 + 4 = ?")
    add("8 − 3 = 5. Use this fact. What is 58 − 3?", 55, [28, 5, 54],
        "3 is 3 ones. Take it from the 8 ones: 8 − 3 = 5. The 5 tens stay. 58 − 3 = <b>55</b>. "
        "(28 takes away 3 tens by mistake.)", "58 − 3 = ?")
    add("4 + 5 = 9. Use this fact. What is 34 + 5?", 39, [84, 9, 38],
        "5 is 5 ones. 4 ones + 5 ones = 9 ones. The 3 tens stay. 34 + 5 = <b>39</b>.", "34 + 5 = ?")
    assert len(its) == 20, len(its)
    return {"title": "Number bonds to 100", "items": its}


# ============================================================ set 4: order and the inverse
def set_order_inverse():
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    add("6 + 9 = 15. What is 9 + 6?", 15, [3, 14, 16],
        "You can add in any order. 9 + 6 is the same as 6 + 9, so the answer is <b>15</b>.", "9 + 6 = ?")
    add("Which has the same answer as 7 + 8?", "8 + 7", ["8 − 7", "7 − 8", "7 + 9"],
        "Addition can be done in any order. <b>8 + 7</b> = 15, and 7 + 8 = 15.")
    add("Which is true?", "6 + 9 = 9 + 6", ["9 − 6 = 6 − 9", "6 + 9 = 6 − 9", "9 + 6 = 9 − 6"],
        "Swapping the numbers in an addition gives the same answer: <b>6 + 9 = 9 + 6</b>. "
        "You cannot swap the numbers in a subtraction.")
    add("12 − 5 = 7. Is 5 − 12 the same?", "No, it is different", ["Yes, it is 7", "Yes, it is 17", "Yes, it is 5"],
        "<b>No.</b> 12 − 5 means take 5 from 12. 5 − 12 means take 12 from 5. "
        "Order matters in subtraction.")
    add("You can swap the numbers in one of these and get the same answer. Which one?", "4 + 11",
        ["11 − 4", "15 − 4", "4 − 11"],
        "Only addition can be done in any order. 4 + 11 = 11 + 4 = 15. So the answer is <b>4 + 11</b>.")
    add("Ruby says 10 − 3 is the same as 3 − 10. Is she right?", "No, order matters",
        ["Yes, order does not matter", "Yes, both are 7", "No, 3 − 10 is 13"],
        "10 − 3 = 7, but you cannot take 10 from 3 and get 7. <b>Order matters</b> in subtraction.")
    opts = ["8 + 6 and 6 + 8", "8 − 6 and 6 − 8", "14 + 8 and 8 + 14", "14 + 6 and 6 + 14"]
    add(fig(part_whole_svg(14, 8, 6)) + "Which two additions match the model?", opts[0], opts[1:],
        "The parts are 8 and 6. You can add them in any order: <b>8 + 6 = 14</b> and <b>6 + 8 = 14</b>.")
    assert 8 + 6 == 14
    for eq, right, wrong, e in [
            ("? − 6 = 9", 15, [3, 14, 16], "Use the inverse. 9 + 6 = <b>15</b>. Check: 15 − 6 = 9. (3 is 9 − 6.)"),
            ("? + 7 = 15", 8, [22, 7, 9], "Use the inverse. 15 − 7 = <b>8</b>. Check: 8 + 7 = 15."),
            ("14 − ? = 6", 8, [20, 7, 9], "Think: 6 + ? = 14. 6 + 8 = 14, so the missing number is <b>8</b>."),
            ("? − 30 = 50", 80, [20, 70, 90], "Use the inverse. 50 + 30 = <b>80</b>. Check: 80 − 30 = 50."),
            ("? + 40 = 100", 60, [140, 6, 70], "Use the inverse. 100 − 40 = <b>60</b>. Check: 60 + 40 = 100."),
            ("17 − ? = 9", 8, [26, 7, 10], "Think: 9 + ? = 17. 9 + 8 = 17, so the missing number is <b>8</b>."),
            ("? − 8 = 12", 20, [4, 19, 21], "Use the inverse. 12 + 8 = <b>20</b>. Check: 20 − 8 = 12."),
            ("8 + 5 = 5 + ?", 8, [13, 5, 3], "You can add in any order. 8 + 5 = 5 + <b>8</b>. Both are 13."),
            ("? + 9 = 9 + 4", 4, [13, 9, 5], "You can add in any order. <b>4</b> + 9 = 9 + 4. Both are 13."),
            ("20 − ? = 11", 9, [31, 8, 10], "Think: 11 + ? = 20. 11 + 9 = 20, so the missing number is <b>9</b>.")]:
        q = eq.replace("?", B)
        add("Find the missing number: " + q, right, wrong, e, eq)
    opts = ["8 + 7 = 15", "15 + 7 = 22", "8 − 7 = 1", "15 + 8 = 23"]
    assert all(holds(o) for o in opts)
    add("15 − 7 = 8. Which addition checks it?", opts[0], opts[1:],
        "Add the answer to the number you took away. <b>8 + 7 = 15</b>, so 15 − 7 = 8 is right.")
    add("Isla says 13 − 4 = 8. Check with addition. Is she right?", "No, 8 + 4 = 12",
        ["Yes, 8 + 4 = 13", "Yes, 13 + 4 = 17", "No, 13 + 4 = 8"],
        "Add the answer and the number taken away: 8 + 4 = 12, not 13. So <b>she is not right</b>. 13 − 4 = 9.")
    assert 8 + 4 == 12 and 13 - 4 == 9
    opts = ["40 + 60 = 100", "100 + 60 = 160", "40 + 40 = 80", "60 − 40 = 20"]
    assert all(holds(o) for o in opts)
    add("Harry says 100 − 60 = 40. Which addition checks it?", opts[0], opts[1:],
        "Add the answer to the number taken away: <b>40 + 60 = 100</b>. So Harry is right.")
    assert len(its) == 20, len(its)
    return {"title": "Order and the inverse", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def add(q, right, unit, wrong, e, check):
        assert check, q
        fmt = (lambda v: "%s %s" % (v, unit[:-1] if v == 1 and unit.endswith("s") else unit)) if unit else (lambda v: str(v))
        its.append(mcq(q, fmt(right), [fmt(w) for w in wrong], e))

    add("A page in Oliver’s football sticker album holds 20 stickers. He has stuck in 13. "
        "How many more stickers does he need to fill the page?", 7, "stickers", [17, 33, 6],
        "13 + ? = 20. 3 + 7 = 10, so 13 + 7 = 20. He needs <b>7 stickers</b>.", 13 + 7 == 20)
    add("Amelia has 15 sweets. She eats 6. How many sweets are left?", 9, "sweets", [21, 11, 8],
        "She eats some, so subtract. 15 − 6 = <b>9</b>. Check: 9 + 6 = 15.", 15 - 6 == 9)
    add("There are 20 children on a bus. 8 children get off. How many children are still on the bus?",
        12, "children", [28, 2, 13],
        "Children get off, so subtract. 20 − 8 = <b>12</b>. Check: 12 + 8 = 20.", 20 - 8 == 12)
    add("There are 12 children on a bus. 8 more get on. How many children are on the bus now?",
        20, "children", [4, 19, 21],
        "More get on, so add. 2 + 8 = 10, so 12 + 8 = <b>20</b>.", 12 + 8 == 20)
    add("A box holds 10 eggs. There are 6 eggs in it. How many more eggs will fill the box?", 4, "eggs",
        [16, 3, 5], "6 + 4 = 10. So <b>4 eggs</b> will fill the box.", 6 + 4 == 10)
    add("A jigsaw has 100 pieces. Harry has put in 60 pieces. How many pieces are left?", 40, "pieces",
        [4, 160, 50], "6 + 4 = 10, so 60 + 40 = 100. <b>40 pieces</b> are left.", 60 + 40 == 100)
    its.append(mcq("Lily has 30p. A comic costs £1. How much more money does she need?", "70p",
                   ["7p", "80p", "£1.30"],
                   "£1 = 100p. 30 + 70 = 100, so she needs <b>70p</b> more."))
    assert 30 + 70 == 100
    add("Grace has run 70 m of a 100 m race. How far is it to the finish?", 30, "m", [3, 170, 40],
        "70 + 30 = 100. It is <b>30 m</b> to the finish.", 70 + 30 == 100)
    add("There are 20 pupils in a class. 11 are girls. How many are boys?", 9, "boys", [31, 8, 10],
        "20 − 11 = <b>9</b>. Check: 11 + 9 = 20.", 20 - 11 == 9)
    add("Arjun has 7 red pencils and 8 blue pencils. How many pencils does he have?", 15, "pencils",
        [1, 14, 16], "Put them together, so add. 7 + 8 = <b>15</b>. (1 is 8 − 7.)", 7 + 8 == 15)
    add("Freya had some marbles. She gave away 5. Now she has 9. How many marbles did she have at first?",
        14, "marbles", [4, 13, 15],
        "Use the inverse. Add back the 5 she gave away: 9 + 5 = <b>14</b>. Check: 14 − 5 = 9.", 14 - 5 == 9)
    its.append(mcq("Noah scores 6 points and then 9 points. Kai scores 9 points and then 6 points. "
                   "Who has more points?", "They have the same", ["Noah", "Kai", "Kai has 3 more"],
                   "6 + 9 = 15 and 9 + 6 = 15. You can add in any order, so <b>they have the same</b>."))
    assert 6 + 9 == 9 + 6
    add("A plate has 16 biscuits. The children eat 9. How many biscuits are left?", 7, "biscuits",
        [25, 13, 8], "16 − 9 = <b>7</b>. Check: 7 + 9 = 16.", 16 - 9 == 7)
    add("Ava has 40 beads. She needs 100 beads for a necklace. How many more beads does she need?", 60, "beads",
        [6, 140, 70], "4 + 6 = 10, so 40 + 60 = 100. She needs <b>60 beads</b>.", 40 + 60 == 100)
    add("A car park has 100 spaces. 50 cars are parked. How many spaces are empty?", 50, "spaces",
        [5, 150, 60], "5 + 5 = 10, so 50 + 50 = 100. <b>50 spaces</b> are empty.", 50 + 50 == 100)
    add("George counts 14 people on the top deck of a bus. There are 20 seats. How many seats are empty?",
        6, "seats", [34, 16, 7], "14 + 6 = 20. So <b>6 seats</b> are empty.", 14 + 6 == 20)
    add("Maya has 18 stickers. She gives 9 to her friend. How many stickers does she have now?", 9, "stickers",
        [27, 11, 8], "18 − 9 = <b>9</b>. Check: 9 + 9 = 18.", 18 - 9 == 9)
    add("Jack has some football cards. He gets 6 more. Now he has 13. How many did he have at first?",
        7, "cards", [19, 6, 8],
        "Use the inverse. Take away the 6 new cards: 13 − 6 = <b>7</b>. Check: 7 + 6 = 13.", 7 + 6 == 13)
    its.append(mcq("Zara has 80p. She spends 30p on a pencil. How much money does she have left?", "50p",
                   ["5p", "£1.10", "60p"],
                   "8 tens − 3 tens = 5 tens. 80p − 30p = <b>50p</b>."))
    assert 80 - 30 == 50
    add("Charlie had 20 conkers. He lost some. Now he has 12. How many conkers did he lose?", 8, "conkers",
        [32, 7, 9], "20 − ? = 12. Think: 12 + 8 = 20. He lost <b>8 conkers</b>.", 20 - 8 == 12)
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a number bond?</h2>"
        "<p>A <b>number bond</b> is a pair of numbers that make a total. 7 and 3 make 10, so 7 + 3 = 10 is a number bond to 10. "
        "Learn the bonds to 10 by heart. Then you can use them to make 20 and 100.</p>"
        + table(["Bonds to 10", "Bonds to 20", "Bonds to 100"], [
            ["1 + 9", "11 + 9", "10 + 90"],
            ["2 + 8", "12 + 8", "20 + 80"],
            ["3 + 7", "13 + 7", "30 + 70"],
            ["4 + 6", "14 + 6", "40 + 60"],
            ["5 + 5", "15 + 5", "50 + 50"],
        ]) +
        "<figure class='sn-fig'>" + ten_frame_svg(7) +
        "<figcaption>7 counters and 3 empty spaces: 7 + 3 = 10.</figcaption></figure>"
        "<h2>From 10 to 20 and 100</h2>"
        "<p>13 is 10 and 3. You know 3 + 7 = 10. So 13 + 7 = 20. "
        "In the same way, 3 tens + 7 tens = 10 tens, so 30 + 70 = 100.</p>"
        "<figure class='sn-fig'>" + tens_rods_svg(3) +
        "<figcaption>3 tens are shaded and 7 tens are white: 30 + 70 = 100.</figcaption></figure>"
        + ex("Example", "Find the missing number: 60 + ? = 100", "6 + 4 = 10, so 6 tens + 4 tens = 10 tens = 100.", "40")
        + "<h2>Fact families</h2>"
        "<p>A part-whole model shows two parts and the whole. One model gives four facts. "
        "If you know 8 + 5 = 13, you also know 13 − 5 = 8.</p>"
        "<figure class='sn-fig'>" + part_whole_svg(13, 8, 5) +
        "<figcaption>8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8, 13 − 8 = 5.</figcaption></figure>"
        "<h2>Does the order matter?</h2>"
        "<p>You can <b>add in any order</b>: 6 + 9 = 9 + 6. You <b>cannot</b> swap the numbers in a subtraction: "
        "9 − 6 = 3, but 6 − 9 is not 3.</p>"
        "<h2>Check with the inverse</h2>"
        "<p>Addition and subtraction undo each other. To check 15 − 7 = 8, add: 8 + 7 = 15. "
        "Use the same idea for missing numbers.</p>"
        + ex("Example", "Find the missing number: ? − 6 = 9", "Add back the 6: 9 + 6 = 15. Check: 15 − 6 = 9.", "15")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Bonds to 10 out by one: 6 + 5 = 10", "Use a ten frame: 6 counters and 4 spaces, so 6 + 4 = 10"],
            ["13 + ? = 20 gives 17", "13 is 10 and 3. 3 + 7 = 10, so 13 + 7 = 20"],
            ["30 + 70 = 10 or 1,000", "3 tens + 7 tens = 10 tens, and 10 tens = 100"],
            ["13 − 5 = 18, or 7", "Think: 5 + 8 = 13, so 13 − 5 = 8"],
            ["Swapping a subtraction: 9 − 6 = 6 − 9", "Only addition can be done in any order"],
        ])
    )


FAQ = [
    {"q": "What are number bonds in Year 2?",
     "a": "Number bonds are pairs of numbers that make a total, like 7 + 3 = 10 or 13 + 7 = 20. In Year 2, children use bonds to 10 to find bonds to 20 and bonds of tens to 100, such as 30 + 70 = 100."},
    {"q": "What number bonds should a Year 2 child know?",
     "a": "By the end of Year 2, the National Curriculum expects children to recall addition and subtraction facts to 20 fluently. They should also use them to work out related facts up to 100, like 40 + 60 = 100 and 100 − 40 = 60."},
    {"q": "What is a fact family?",
     "a": "A fact family is the set of four facts made from the same three numbers. For 8, 5 and 13 they are 8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8 and 13 − 8 = 5."},
    {"q": "How can I help my child learn number bonds at home?",
     "a": "Use a ten frame, an egg box or ten fingers to show the pairs that make 10, and practise for a few minutes every day. Once bonds to 10 are quick, ask “if 3 + 7 = 10, what is 13 + 7 or 30 + 70?”"},
]


def gen():
    rnd = random.Random(2203)
    sets = [set_bonds_10_20(), set_fact_families(), set_bonds_100(), set_order_inverse(), set_words()]
    balance(sets, rnd)
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in allq, it["q"]
            allq.add(k)
            # "What is a ± b?" answers
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(it["c"][it["a"]]) == (a + b if op == "+" else a - b), it["q"]
            # counters drawn match the label
            m = re.search(r"aria-label='(?:ten frame|two ten frames) with (\d+) counters'", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)), it["q"]
            # numbers stay within 0-100 (except the "1,000" mistake)
            for c in it["c"]:
                for n in re.findall(r"\d[\d,]*", c):
                    assert int(n.replace(",", "")) <= 1000, c
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "number-bonds-to-20-and-100", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Number Bonds to 20 and 100",
        "seo_title": "Year 2 Number Bonds Worksheets: Bonds to 10, 20 and 100, Fact Families and Missing Numbers",
        "short_title": "Number bonds to 20 and 100",
        "domain": "Addition and subtraction",
        "standard_code": "Year 2: Addition and subtraction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recall and use addition and subtraction facts to 20 fluently, and derive and use related facts up to 100; show that addition of two numbers can be done in any order (commutative) and subtraction of one number from another cannot; recognise and use the inverse relationship between addition and subtraction and use this to check calculations and solve missing number problems.",
        "meta_desc": "Free Year 2 maths worksheets on number bonds: bonds to 10 and 20 with ten frames, fact families, bonds of tens to 100, adding in any order, missing numbers using the inverse, and word problems. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Know your bonds to 10, and you can make 20 and 100.",
        "key_sub": "3 + 7 = 10, so 13 + 7 = 20 and 30 + 70 = 100. If 8 + 5 = 13, then 13 − 5 = 8. You can add in any order, but you cannot swap the numbers in a subtraction.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
