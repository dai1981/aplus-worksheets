# -*- coding: utf-8 -*-
"""
BC Grade 3 Math: Multiplication and division concepts (BC Mathematics Curriculum, Computational fluency)
Equal groups, arrays, repeated addition and skip counting, division as sharing and grouping
(and repeated subtraction), word problems in BC settings.
  python3 tools/gen_cabc_math_g3_mult_div.py
HTML attributes use single quotes (no backslashes in the JSON). Every drawn picture is counted in code.
Canadian style: Canadian English, $ and ¢ (no pennies), numbers under 1000 (no separators needed).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=18, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def dot(cx, cy, r=9, col=GREEN):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, col)


def n_dots(svg):
    return svg.count("<circle ")


def rep(n, times):
    return " + ".join([str(n)] * times)


def skip(n, times):
    return ", ".join(str(n * (i + 1)) for i in range(times))


# ------------------------------------------------------------ figures
def array_svg(rows, cols, label=None):
    assert 1 <= rows <= 5 and 1 <= cols <= 10
    S, o = 28, 6
    body = "".join(dot(o + c * S + S / 2.0, o + i * S + S / 2.0, 9.5) for i in range(rows) for c in range(cols))
    svg = svg_wrap(cols * S + 2 * o, rows * S + 2 * o, body,
                   label or "array of %d rows of %d dots" % (rows, cols))
    assert n_dots(svg) == rows * cols
    return svg


def lesson_array_svg(rows, cols):
    """Array with each row's count written on the right."""
    S, R, x0, y0 = 34, 11, 10, 10
    el = [dot(x0 + c * S + S / 2.0, y0 + i * S + S / 2.0, R) for i in range(rows) for c in range(cols)]
    for i in range(rows):
        el.append(text(x0 + cols * S + 20, y0 + i * S + S / 2 + 6, str(cols), 17, col=RED))
    svg = svg_wrap(x0 + cols * S + 36, y0 + rows * S + 10, "".join(el),
                   "array of %d rows of %d dots, with each row counted" % (rows, cols))
    assert n_dots(svg) == rows * cols
    return svg


def counters_svg(n):
    """n counters in rows of 10 (small gap after 5), not yet shared."""
    S, M = 24, 5
    el = []
    for i in range(n):
        rr, cc = divmod(i, 10)
        el.append(dot(M + cc * S + (8 if cc >= 5 else 0) + S / 2.0, M + rr * S + S / 2.0, 8.5))
    cols = min(n, 10)
    svg = svg_wrap(M * 2 + cols * S + (8 if cols > 5 else 0), M * 2 + ((n + 9) // 10) * S, "".join(el),
                   "%d counters in rows of 10" % n)
    assert n_dots(svg) == n
    return svg


def groups_body(sizes, x0, y0, style, per_row=5):
    """Rings (grouping) or plates (sharing). Each box fits the largest group: up to 3 in a line, then 2 rows."""
    S, r, G, P = 24, 8.5, 10, 6
    m = max(sizes)
    ri, ci = (1, max(m, 1)) if m <= 3 else (2, (m + 1) // 2)
    bw, bh = ci * S + 2 * P, ri * S + 2 * P
    el = []
    for k, n in enumerate(sizes):
        br, bc = divmod(k, per_row)
        bx, by = x0 + bc * (bw + G), y0 + br * (bh + G)
        if style == "plate":
            el.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>"
                      % (bx, by, bw, bh, min(bw, bh) / 2.0, FILL2, GREEN))
        else:
            el.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='12' fill='none' stroke='%s' "
                      "stroke-width='2.5' stroke-dasharray='6 4'/>" % (bx, by, bw, bh, GREY))
        for i in range(n):
            rr, cc = divmod(i, ci)
            el.append(dot(bx + P + cc * S + S / 2.0, by + P + rr * S + S / 2.0, r))
    nrow = (len(sizes) + per_row - 1) // per_row
    ncol = min(len(sizes), per_row)
    return "".join(el), ncol * bw + (ncol - 1) * G, nrow * bh + (nrow - 1) * G


def groups_svg(sizes, style, label=None):
    M = 5
    body, w, h = groups_body(sizes, M, M, style)
    svg = svg_wrap(int(w + 2 * M), int(h + 2 * M), body, label or (
        "%d %s of %d counters" % (len(sizes), "plates" if style == "plate" else "groups", sizes[0])))
    assert n_dots(svg) == sum(sizes)
    return svg


def abcd_svg(panels, style):
    """Four pictures side by side, labelled A to D."""
    PAD = 10
    built = [groups_body(p, 0, 0, style, per_row=3 if len(p) > 4 else 2) for p in panels]
    PW = max(b[1] for b in built) + 2 * PAD
    H = int(30 + max(b[2] for b in built) + 8)
    el = []
    for k, (body, w, h) in enumerate(built):
        x0 = k * PW
        if k:
            el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, x0, H - 4, GREY))
        el.append(text(x0 + 8, 20, "ABCD"[k], 18, "start"))
        el.append("<g transform='translate(%.1f,30)'>%s</g>" % (x0 + (PW - w) / 2.0, body))
    svg = svg_wrap(int(4 * PW), H, "".join(el), "four pictures labelled A to D")
    assert n_dots(svg) == sum(sum(p) for p in panels)
    return svg


def jumps_svg(step, n):
    """Number line from 0 with n equal jumps of `step`. Ticks every 1, labels every 5 (or every step)."""
    end = step * n
    hi = end + (step if end + step <= 40 else 0)
    hi = max(hi, 10)
    U = 440.0 / hi
    x0, y = 20, 70
    el = ["<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 8, y, x0 + hi * U + 8, y, INK)]
    lab = 5 if hi > 20 else 2 if hi > 12 else 1
    for v in range(hi + 1):
        big = v % lab == 0
        el.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                  % (x0 + v * U, y - (8 if big else 5), x0 + v * U, y + (8 if big else 5), INK, "2" if big else "1"))
        if big:
            el.append(text(x0 + v * U, y + 28, v, 15))
    for j in range(n):
        a, b = x0 + j * step * U, x0 + (j + 1) * step * U
        el.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                  % (a, y - 4, (a + b) / 2, y - 4 - min(60, 18 + step * U * 0.5), b, y - 4, RED))
        el.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (b, y - 3, b - 7, y - 10, b + 1, y - 13, RED))
    svg = svg_wrap(int(x0 * 2 + hi * U), 106, "".join(el), "number line with %d jumps of %d" % (n, step))
    assert svg.count("<path ") == n
    return svg


# ------------------------------------------------------------ set 1: equal groups
def set_groups():
    its = []
    # A: how many altogether?
    for g, k in [(3, 4), (2, 5), (4, 5), (5, 3), (2, 6), (4, 2)]:
        n = g * k
        e = ("There are %d groups. Each group has %d counters. Count by %ds: %s. So %d groups of %d = %d × %d = <b>%d</b>."
             % (g, k, k, skip(k, g), g, k, g, k, n))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "How many counters are there altogether?",
                       n, [g + k, k, g, (g + 1) * k], e))
    # B: describe the picture (groups vs items)
    for g, k in [(4, 3), (2, 6), (5, 4), (3, 5)]:
        right = "%d groups of %d" % (g, k)
        wrong = ["%d groups of %d" % (k, g), "%d groups of %d" % (g, g * k), "%d groups of %d" % (g + k, 1)]
        e = ("Count the rings: %d groups. Count one ring: %d in each. So it is <b>%s</b>. "
             "%d groups of %d mixes up the groups and the counters in each group." % (g, k, right, k, g))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "What does this picture show?", right, wrong, e))
    # C: which number sentence matches the groups?
    for g, k, wrong in [(3, 6, ["3 + 6 = 9", "6 + 6 = 12", "3 × 7 = 21"]),
                        (4, 5, ["4 + 5 = 9", "5 + 5 + 5 = 15", "4 × 6 = 24"]),
                        (5, 2, ["5 + 2 = 7", "2 + 2 + 2 + 2 = 8", "5 × 3 = 15"])]:
        right = "%d × %d = %d" % (g, k, g * k)
        e = ("There are %d groups of %d: %s = %d. That is <b>%s</b>. %d + %d only adds the two numbers."
             % (g, k, rep(k, g), g * k, right, g, k))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "Which number sentence matches the picture?", right, wrong, e))
    # D: equal or not?
    its.append(mcq(fig(groups_svg([4, 4, 3], "ring", "3 groups of 4, 4 and 3 counters")) + "Are these equal groups?",
                   "No. One group has only 3.",
                   ["Yes. They are 3 groups of 4.", "Yes. All groups have 3.", "No. There are 4 groups."],
                   "Equal groups all have the same number. Two groups have 4, but one has 3. "
                   "So the groups are <b>not equal</b>, and this is not 3 × 4."))
    its.append(mcq(fig(groups_svg([5, 5, 5], "ring")) + "Are these equal groups?",
                   "Yes. 3 groups of 5.",
                   ["No. 5 groups of 3.", "No. They are not the same.", "Yes. 3 groups of 3."],
                   "Every group has 5 counters, so the groups are equal. There are 3 groups, so it is <b>3 groups of 5</b>."))
    # E: in words
    its.append(mcq("Hana has 4 bags. Each bag has 6 apples. Which shows how many apples she has?", "4 × 6",
                   ["4 + 6", "6 − 4", "4 × 4"],
                   "4 bags with 6 in each is 4 groups of 6. That is <b>4 × 6</b> = 24. 4 + 6 only joins the two numbers."))
    its.append(mcq("There are 5 plates. Each plate has 2 cookies. How many cookies are there?", 10,
                   [7, 2, 5],
                   "5 groups of 2: 2 + 2 + 2 + 2 + 2 = <b>10</b>. 7 comes from 5 + 2. 2 is only one plate."))
    its.append(mcq("Nadia makes 3 groups of 7 shells. How many shells does she use?", 21,
                   [10, 7, 28],
                   "3 groups of 7: 7 + 7 + 7 = <b>21</b>. 10 comes from 3 + 7. 7 is only one group."))
    # F: pick the picture
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("3 groups of 4 means 3 groups with 4 in each group. <b>{L}</b> shows this. "
                      "4 groups of 3 mixes up the groups and the counters in each group. "
                      "The other pictures do not have equal groups or have the wrong number of groups."),
                "_abcd": ("Which picture shows <b>3 groups of 4</b>?",
                          [4, 4, 4], [[3, 3, 3, 3], [4, 4], [4, 4, 3]], "ring")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("2 groups of 5 means 2 groups with 5 in each group. <b>{L}</b> shows this. "
                      "5 groups of 2 mixes up the groups and the counters in each group. "
                      "3 groups of 5 has one group too many, and 5 and 4 are not equal groups."),
                "_abcd": ("Which picture shows <b>2 groups of 5</b>?",
                          [5, 5], [[2, 2, 2, 2, 2], [5, 5, 5], [5, 4]], "ring")})
    assert len(its) == 20, len(its)
    return {"title": "Equal groups", "items": its}


# ------------------------------------------------------------ set 2: arrays
def set_arrays():
    its = []
    # A: how many dots?
    for r, c in [(2, 4), (3, 5), (4, 4), (2, 9), (5, 6)]:
        e = ("There are %d rows of %d. Count by %ds: %s. So %d × %d = <b>%d</b>."
             % (r, c, c, skip(c, r), r, c, r * c))
        its.append(mcq(fig(array_svg(r, c)) + "How many dots are in this array?",
                       r * c, [r + c, (r + 1) * c, c, r * (c - 1)], e))
    # B: which number sentence?
    for r, c in [(2, 6), (3, 7), (4, 5), (5, 8)]:
        right = "%d × %d = %d" % (r, c, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c + 1, r * (c + 1)),
                 "%d × %d = %d" % (r + 1, c, (r + 1) * c)]
        e = ("Count the rows: %d. Count one row: %d. %d rows of %d is <b>%s</b>. "
             "%d + %d only adds the two numbers. It does not count the dots." % (r, c, r, c, right, r, c))
        its.append(mcq(fig(array_svg(r, c)) + "Which number sentence matches this array?", right, wrong, e))
    # C: how many rows / in each row?
    for r, c, ask in [(3, 6, "rows"), (4, 7, "rows"), (2, 8, "each")]:
        if ask == "rows":
            q, a, wrong = "How many <b>rows</b> does this array have?", r, [c, r * c, r + c]
            e = "Rows go across. Count down the side: there are <b>%d</b> rows. %d is the number of dots in each row." % (r, c)
        else:
            q, a, wrong = "How many dots are in <b>each row</b>?", c, [r, r * c, r + c]
            e = "Look along one row from left to right: <b>%d</b> dots. %d is the number of rows." % (c, r)
        its.append(mcq(fig(array_svg(r, c)) + q, a, wrong, e))
    # D: turnaround facts
    for a, b in [(4, 7), (2, 9), (5, 3), (3, 10)]:
        right = "%d × %d" % (b, a)
        wrong = ["%d × %d" % (a, b + 1), "%d + %d" % (b, a), "%d × %d" % (b, b)]
        e = ("Turn the array a quarter turn. %d rows of %d become %d rows of %d. The dots do not change, "
             "so %d × %d = %d × %d = %d. <b>%s</b> has the same answer." % (a, b, b, a, a, b, b, a, a * b, right))
        its.append(mcq("Which has the <b>same answer</b> as %d × %d?" % (a, b), right, wrong, e))
    # E: turn the array
    for r, c in [(3, 5), (2, 7)]:
        right = "%d × %d = %d" % (c, r, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, r, r * r), "%d × %d = %d" % (c, c, c * c)]
        e = ("Turn the array a quarter turn. %d rows of %d become %d rows of %d. "
             "The number of dots does not change, so <b>%s</b>." % (r, c, c, r, right))
        its.append(mcq(fig(array_svg(r, c)) + "This array shows %d × %d = %d. Which other number sentence also matches it?"
                       % (r, c, r * c), right, wrong, e))
    # F: missing number with the turnaround fact
    for a, b in [(6, 4), (5, 8)]:
        e = ("The order can change. The answer stays the same. %d × %d = %d × %d, so the missing number is <b>%d</b>. "
             "Both are %d." % (a, b, b, a, a, a * b))
        its.append(mcq("What number goes in the box?  <b>%d × %d = %d × ☐</b>" % (a, b, b), a, [b, a * b, a + b], e))
    assert len(its) == 20, len(its)
    return {"title": "Arrays", "items": its}


# ------------------------------------------------------------ set 3: repeated addition and skip counting
def set_repeated():
    its = []
    # A: repeated addition -> multiplication
    for n, k in [(6, 4), (3, 5), (8, 3), (10, 4), (7, 2)]:
        right = "%d × %d" % (k, n)
        wrong = ["%d × %d" % (n, n), "%d + %d" % (k, n), "%d × %d" % (k + 1, n)]
        e = ("Count the %ds: there are %d of them. %d groups of %d is <b>%s</b> = %d."
             % (n, k, k, n, right, k * n))
        its.append(mcq("Which is the same as <b>%s</b>?" % rep(n, k), right, wrong, e))
    # B: multiplication -> repeated addition
    for r, c in [(4, 9), (3, 8), (5, 6)]:
        right = rep(c, r)
        wrong = ["%d + %d" % (r, c), rep(c, r - 1), rep(c, r + 1)]
        e = "%d × %d means %d groups of %d. Add %d, %d times: <b>%s</b> = %d." % (r, c, r, c, c, r, right, r * c)
        its.append(mcq("Which addition is the same as <b>%d × %d</b>?" % (r, c), right, wrong, e))
    # C: skip counting, what comes next?
    for k, shown in [(2, 4), (5, 4), (10, 3), (3, 4)]:
        seq = [k * (i + 1) for i in range(shown)]
        a = k * (shown + 1)
        e = "Each number is %d more than the one before. %d + %d = <b>%d</b>." % (k, seq[-1], k, a)
        its.append(mcq("Count by %ds: %s, ☐. What number comes next?" % (k, ", ".join(map(str, seq))),
                       a, [seq[-1] + 1, a + k, seq[-1] + k - 1, a + 1], e))
    # D: number line jumps
    for k, n in [(5, 4), (3, 6), (2, 7), (4, 5)]:
        right = "%d × %d = %d" % (n, k, n * k)
        wrong = ["%d + %d = %d" % (n, k, n + k), "%d × %d = %d" % (n - 1, k, (n - 1) * k),
                 "%d × %d = %d" % (n + 1, k, (n + 1) * k)]
        e = ("There are %d jumps of %d. Skip count: %s. So <b>%s</b>. Count the jumps (the arrows), not the marks."
             % (n, k, skip(k, n), right))
        its.append(mcq(fig(jumps_svg(k, n)) + "Which number sentence matches the jumps?", right, wrong, e))
    # E: 3 × 4 = 7 mistake
    its.append(mcq("Owen says 3 × 4 = 7. What did he do?", "He added 3 + 4.",
                   ["He counted by 3s.", "He multiplied right.", "He took away 4."],
                   "3 + 4 = 7. But 3 × 4 means 3 groups of 4: 4 + 4 + 4 = <b>12</b>. Owen <b>added</b> instead of multiplying."))
    its.append(mcq("Which is the right answer to <b>2 × 5</b>?", "10", ["7", "25", "3"],
                   "2 × 5 means 2 groups of 5: 5 + 5 = <b>10</b>. 7 is 2 + 5. 25 is 5 groups of 5. 3 is 5 − 2."))
    its.append(mcq("Mei skip counts by 4s. She says 4, 8, 12, 16. Which multiplication does this show?", "4 × 4 = 16",
                   ["4 + 4 = 8", "4 × 16 = 64", "4 × 3 = 12"],
                   "She says 4 numbers, so there are 4 groups of 4. The last number is the total: <b>4 × 4 = 16</b>."))
    its.append(mcq("Ji-woo skip counts by 5s to find 6 × 5. Where should she stop?", "30",
                   ["25", "35", "11"],
                   "Say 6 numbers: 5, 10, 15, 20, 25, 30. Stop at <b>30</b>. 25 is only 5 counts. 11 is 6 + 5."))
    assert len(its) == 20, len(its)
    return {"title": "Repeated addition and skip counting", "items": its}


# ------------------------------------------------------------ set 4: division as sharing and grouping
def set_divide():
    its = []
    # A: share counters
    for n, k in [(12, 3), (10, 2), (15, 5), (20, 4)]:
        a = n // k
        e = ("Sharing: give the counters out one at a time until none are left. "
             "Each of the %d plates gets <b>%d</b>. %d ÷ %d = %d." % (k, a, n, k, a))
        its.append(mcq(fig(counters_svg(n)) + "Share these %d counters equally on %d plates. How many go on each plate?"
                       % (n, k), a, [k, n - k, a + 1, a - 1], e))
    # B: grouping picture, count the groups
    for n, k in [(20, 5), (12, 2), (18, 3), (16, 4)]:
        g = n // k
        e = ("Grouping: you know there are %d in each group. Count the rings: %d groups. So %d ÷ %d = <b>%d</b>."
             % (k, g, n, k, g))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "%d counters are put in groups of %d. How many groups are there?"
                       % (n, k), g, [k, n - k, g + 1, n], e))
    # C: which division matches the sharing picture?
    for n, k in [(24, 4), (21, 3), (14, 2)]:
        a = n // k
        right = "%d ÷ %d = %d" % (n, k, a)
        wrong = ["%d ÷ %d = %d" % (k, n, a), "%d − %d = %d" % (n, k, n - k), "%d ÷ %d = %d" % (n, k, a + 1)]
        e = ("%d counters are shared on %d plates. Each plate has %d. That is <b>%s</b>. "
             "Always start with the total, %d. %d ÷ %d is the wrong way around." % (n, k, a, right, n, k, n))
        its.append(mcq(fig(groups_svg([a] * k, "plate")) +
                       "%d counters are shared equally on %d plates. Which division matches the picture?" % (n, k),
                       right, wrong, e))
    # D: sharing or grouping?
    its.append(mcq("Which one is <b>grouping</b>?", "Put 20 apples in bags of 5.",
                   ["Share 20 apples among 5 bags.", "Add 5 more apples to 20.", "Eat 5 of the 20 apples."],
                   "Grouping means you know how many go in each group. “Bags of 5” tells you there are 5 in each bag. "
                   "20 ÷ 5 = 4 bags. Sharing among 5 bags is sharing: you know the number of bags."))
    its.append(mcq("Which one is <b>sharing</b>?", "Share 18 hockey cards among 3 friends.",
                   ["Put 18 hockey cards in piles of 3.", "Buy 3 more hockey cards.", "Give away 3 of 18 hockey cards."],
                   "Sharing means you know how many groups. “Among 3 friends” tells you there are 3 groups. "
                   "18 ÷ 3 = 6 cards each. Piles of 3 is grouping: you know how many go in each pile."))
    # E: pick the sharing picture
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing among 3 plates means 3 plates, all the same. <b>{L}</b> has 3 plates of 5. "
                      "5 plates of 3 is groups of 3. 6, 5 and 4 are not equal, and 3 plates of 4 is only 12."),
                "_abcd": ("Share 15 counters equally on 3 plates. Which picture shows this?",
                          [5, 5, 5], [[3, 3, 3, 3, 3], [6, 5, 4], [4, 4, 4]], "plate")})
    # F: repeated subtraction
    for n, k in [(20, 5), (12, 3), (16, 4)]:
        g = n // k
        chain = " − ".join([str(n)] + [str(k)] * g) + " = 0"
        right = "%d ÷ %d = %d" % (n, k, g)
        wrong = ["%d ÷ %d = %d" % (n, k, g + 1), "%d ÷ %d = %d" % (k, n, g), "%d − %d = %d" % (n, k, n - k)]
        e = ("Count how many times %d is taken away: %d times. So %d has %d groups of %d: <b>%s</b>. "
             "Do not count the %d at the start." % (k, g, n, g, k, right, n))
        its.append(mcq("Sofia takes away %d again and again: <b>%s</b>. Which division does this show?" % (k, chain),
                       right, wrong, e))
    # G: think multiplication
    for n, k in [(30, 5), (40, 10), (18, 2)]:
        a = n // k
        e = "Think multiplication: %d × ☐ = %d. %d × %d = %d, so %d ÷ %d = <b>%d</b>." % (k, n, k, a, n, n, k, a)
        its.append(mcq("What is %d ÷ %d?  <i>Think: %d × ☐ = %d.</i>" % (n, k, k, n), a, [a + 1, a - 1, n - k, k], e))
    assert len(its) == 20, len(its)
    return {"title": "Division as sharing and grouping", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story():
    its = []
    mult = [
        ("The class sets up chairs for the winter concert. There are 6 rows with 8 chairs in each row. How many chairs are there?", 6, 8),
        ("A pack of hockey cards has 5 cards. Liam buys 4 packs. How many cards does he get?", 4, 5),
        ("At summer camp on Vancouver Island, 7 canoes go out on the lake. Each canoe holds 3 people. How many people can the canoes hold?", 7, 3),
        ("Chloe helps plant cedar seedlings. She plants 5 rows with 6 seedlings in each row. How many seedlings does she plant?", 5, 6),
        ("At a soccer tournament in Kelowna, each team brings 9 players. 4 teams play on Saturday morning. How many players is that?", 4, 9),
        ("Bald eagles sit in the trees by the Fraser River. There are 3 eagles in each of 8 trees. How many eagles are there?", 8, 3),
        ("At lunch, 8 students sit at each table. There are 5 full tables. How many students are at the tables?", 5, 8),
    ]
    for q, g, k in mult:
        n = g * k
        e = ("There are %d equal groups of %d, so multiply: %d × %d = <b>%d</b>. "
             "Adding %d + %d = %d only joins the two numbers." % (g, k, g, k, n, g, k, g + k))
        its.append(mcq(q, n, [g + k, k, (g + 1) * k, (g - 1) * k], e))
    its.append(mcq("Mateo has 9 toonies. A toonie is worth $2. How much money does he have?", "$18",
                   ["$11", "$9", "$20"],
                   "9 toonies is 9 groups of $2: 9 × $2 = <b>$18</b>. $11 comes from adding 9 + 2."))
    div = [
        ("Arjun shares 24 hockey cards equally among 4 friends. How many cards does each friend get?", 6,
         [4, 20, 28, 5], "Sharing among 4 friends: 24 ÷ 4. 4 × 6 = 24, so each friend gets <b>6</b> cards."),
        ("In gym class, 35 students make teams of 5. How many teams are there?", 7,
         [5, 30, 40, 8], "Grouping in 5s: 35 ÷ 5. 5 × 7 = 35, so there are <b>7</b> teams."),
        ("There are 32 chairs in the library. They are in 4 equal rows. How many chairs are in each row?", 8,
         [4, 28, 36, 9], "32 chairs in 4 equal rows: 32 ÷ 4. 4 × 8 = 32, so each row has <b>8</b> chairs."),
        ("On a field trip to Stanley Park, 27 students walk in groups of 3. How many groups are there?", 9,
         [3, 24, 30, 8], "Grouping in 3s: 27 ÷ 3. 3 × 9 = 27, so there are <b>9</b> groups."),
        ("15 students go on a field trip to Grouse Mountain. Each parent driver takes 3 students. How many cars are needed?", 5,
         [3, 12, 45], "Groups of 3: 15 ÷ 3. 3 × 5 = 15, so <b>5</b> cars are needed. (45 comes from 15 × 3.)"),
        ("Ethan has 40¢ in nickels. A nickel is 5¢. How many nickels does he have?", 8,
         [5, 35, 45, 9], "How many 5s make 40? 40 ÷ 5. 5 × 8 = 40, so he has <b>8</b> nickels."),
        ("Simran reads 10 pages each day. How many days does it take her to read 50 pages?", 5,
         [10, 40, 60, 6], "How many 10s make 50? 50 ÷ 10 = <b>5</b> days. Check: 5 × 10 = 50."),
        ("Wei shares 20 strawberries equally between 2 bowls. How many strawberries go in each bowl?", 10,
         [2, 18, 40], "Sharing between 2 bowls: 20 ÷ 2. 2 × 10 = 20, so each bowl gets <b>10</b>. (40 comes from 20 × 2.)"),
    ]
    for q, a, wrong, e in div:
        its.append(mcq(q, a, wrong, e))
    its.append(mcq("Noah buys 3 hot chocolates at the rink. Each one costs $2. He pays with a $10 bill. How much change does he get?",
                   "$4", ["$6", "$7", "$16"],
                   "Step 1: cost: 3 × $2 = $6. Step 2: change: $10 − $6 = <b>$4</b>. ($6 is the cost, not the change.)"))
    its.append(mcq("Ava has 4 packs of stickers. Each pack has 5 stickers. She gives 6 stickers to her brother. How many stickers does she have left?",
                   "14", ["20", "26", "3"],
                   "Step 1: 4 × 5 = 20 stickers. Step 2: 20 − 6 = <b>14</b> stickers left. (3 comes from 4 + 5 − 6.)"))
    its.append(mcq("Kai has 3 bags of marbles with 8 marbles in each bag. He shares all the marbles equally among 4 friends. How many marbles does each friend get?",
                   "6", ["24", "2", "8"],
                   "Step 1: 3 × 8 = 24 marbles. Step 2: 24 ÷ 4 = <b>6</b>, because 4 × 6 = 24. (24 is only step 1.)"))
    its.append(mcq("For the Terry Fox Run, Zara walks 3 laps of the field each day for 5 days. Owen walks 10 laps in all. How many more laps does Zara walk?",
                   "5", ["15", "8", "25"],
                   "Step 1: Zara walks 5 × 3 = 15 laps. Step 2: 15 − 10 = <b>5</b> more laps. (15 is only step 1.)"))
    assert len(its) == 20, len(its)
    return {"title": "Multiplication and division word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Equal groups</h2>"
        "<p><b>Multiplication</b> counts equal groups. 3 groups of 4 is 3 × 4. "
        "The first number tells how many groups. The second number tells how many in each group.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "ring") +
        "<figcaption>3 groups of 4: 4 + 4 + 4 = 12, so 3 × 4 = 12.</figcaption></figure>"
        "<h2>Arrays</h2>"
        "<p>An <b>array</b> puts equal groups in rows. Count the rows. Then count one row.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(3, 5) +
        "<figcaption>3 rows of 5: 3 × 5 = 15.</figcaption></figure>"
        "<p>Turn the array a quarter turn and you get 5 rows of 3. It is still 15 dots, so 3 × 5 = 5 × 3.</p>"
        "<h2>Repeated addition and skip counting</h2>"
        "<p>Multiplication is a fast way to add the same number again and again. "
        "You can also skip count on a number line.</p>"
        "<figure class='sn-fig'>" + jumps_svg(5, 4) +
        "<figcaption>4 jumps of 5: 5, 10, 15, 20. So 4 × 5 = 20.</figcaption></figure>" +
        ex("Repeated addition", "What is 4 × 6?", "4 groups of 6: 6 + 6 + 6 + 6 = 24.", "24") +
        "<h2>Division: sharing and grouping</h2>"
        "<p><b>Sharing:</b> you know how many groups. Give the items out one at a time. "
        "12 shared on 3 plates is 4 on each plate.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "plate", "12 counters shared on 3 plates") +
        "<figcaption>Sharing: 12 ÷ 3 = 4 on each plate.</figcaption></figure>"
        "<p><b>Grouping:</b> you know how many in each group. 12 in groups of 3 makes 4 groups. "
        "You can also take away 3 again and again: 12 − 3 − 3 − 3 − 3 = 0. That is 4 groups. "
        "Both ways give 12 ÷ 3 = 4. Always start with the total.</p>" +
        ex("Divide with a times fact", "What is 20 ÷ 5?", "Think: 5 × ☐ = 20. 5 × 4 = 20.", "4") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding instead of multiplying (3 × 4 = 7)", "3 × 4 means 3 groups of 4: 4 + 4 + 4 = 12"],
            ["Giving the number in one group, not the total (3 groups of 4 = 4)", "Count all the items: 3 × 4 = 12"],
            ["Mixing up groups and items (3 groups of 4 drawn as 4 groups of 3)", "The first number is the number of groups"],
            ["Dividing the wrong way (4 ÷ 20 = 5)", "Start with the total: 20 ÷ 4 = 5"],
            ["Mixing up sharing and grouping", "“Among 4” means 4 groups. “Groups of 4” means 4 in each group"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division does Grade 3 learn in the BC math curriculum?",
     "a": "In the BC curriculum, Grade 3 students learn multiplication and division concepts. They use equal groups, arrays, repeated addition and skip counting to multiply, and sharing and grouping to divide."},
    {"q": "Do Grade 3 students in BC need to memorize times tables?",
     "a": "Grade 3 in BC focuses on understanding what multiplication and division mean. Learning the multiplication and division facts to 100 is a Grade 4 goal, so early practice with groups and skip counting helps."},
    {"q": "What is the difference between sharing and grouping in division?",
     "a": "In sharing you know the number of groups and find how many go in each, like 12 shared on 3 plates. In grouping you know how many go in each group and find the number of groups, like 12 in groups of 3. Both give 12 ÷ 3 = 4."},
    {"q": "Why does my child use arrays for multiplication?",
     "a": "An array shows equal rows, so students can see that 3 rows of 5 is 5 + 5 + 5 = 15. Turning the array also shows that 3 × 5 = 5 × 3."},
]


# ------------------------------------------------------------ build
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, right, wrong, style = it.pop("_abcd")
                wrong = list(wrong)
                rnd.shuffle(wrong)
                panels = wrong[:t] + [right] + wrong[t:]
                it["q"] = fig(abcd_svg(panels, style)) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def verify(sets):
    """Check every number sentence with × or ÷ that is given as a correct answer."""
    for s in sets:
        for it in s["items"]:
            r = it["c"][it["a"]]
            m = re.fullmatch(r"(\d+) ([×÷]) (\d+) = (\d+)", r)
            if m:
                a, op, b, v = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
                assert (a * b == v) if op == "×" else (b * v == a), r
            for c in it["c"]:
                m = re.fullmatch(r"(\d+) ([×÷+−]) (\d+) = (\d+)", c)
                if m and c != r:
                    a, op, b, v = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
                    # a wrong choice may be a true fact only if it is an addition/subtraction or a reversed array
                    if op == "÷":
                        assert b * v != a, ("true wrong choice", c, it["q"])


def gen():
    rnd = random.Random(53804)
    sets = [set_groups(), set_arrays(), set_repeated(), set_divide(), set_story()]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    verify(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0] * 4
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            pos[it["a"]] += 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
        assert pos == [5, 5, 5, 5], pos
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "multiplication-and-division", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication and Division: Equal Groups, Arrays, Sharing and Grouping",
        "seo_title": "Grade 3 Math Multiplication and Division Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Multiplication and division",
        "domain": "Computational fluency",
        "standard_code": "Grade 3: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Multiplication and division concepts",
        "meta_desc": "Free Grade 3 math worksheets on multiplication and division concepts: equal groups, arrays, "
                     "repeated addition and skip counting, sharing and grouping, and word problems about hockey cards, "
                     "canoes and field trips. 100 questions with an answer key, following the BC curriculum.",
        "key_big": "Multiplication counts equal groups. Division splits a total into equal groups.",
        "key_sub": "3 × 4 means 3 groups of 4: 4 + 4 + 4 = 12, not 3 + 4 = 7. "
                   "12 ÷ 3 = 4: share 12 into 3 groups, or make groups of 3 and count them.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(array of \\d+ rows of ([6-9]|10) |\\d+ counters|\\d+ groups of|\\d+ plates of|four pictures|number line)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
