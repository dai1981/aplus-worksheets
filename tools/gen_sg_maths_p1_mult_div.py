# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Multiplication and division (MOE 2021 Primary Mathematics Syllabus, Standard,
Number and Algebra: concepts of multiplication and division, use of ×, multiplying within 40, dividing within 20)
  python3 tools/gen_sg_maths_p1_mult_div.py
Equal groups, repeated addition and the × sign, arrays, sharing equally and grouping, one-step word problems.
P1 does not use the ÷ sign here: division is said in words (share equally, put into groups of).
Every picture is counted in code. Wrong answers are real mistakes: mixing up the number of groups and the
number in each group, unequal groups, adding the two numbers instead of multiplying, giving one group only.
Singapore English, $ (whole dollars only). HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
BROWN = "#7a4a1e"
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
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=18, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def item(cx, cy, r=9, kind="dot"):
    """One thing to count: a green counter or an apple (one circle each, so pictures can be counted)."""
    if kind == "apple":
        return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                % (cx, cy - r + 1, cx + 1, cy - r - 4, BROWN, cx + 4, cy - r - 2, r * 0.4, r * 0.22, GREEN,
                   cx, cy + 1, r - 0.5, RED))
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, GREEN)


def n_items(svg):
    return svg.count("<circle ")


def rep(n, times):
    return " + ".join([str(n)] * times)


def skip(n, times):
    return ", ".join(str(n * (i + 1)) for i in range(times))


def noun(kind, n):
    return ("apple" if kind == "apple" else "counter") + ("" if n == 1 else "s")


# ------------------------------------------------------------ figures
def array_svg(rows, cols):
    assert 1 <= rows <= 5 and 1 <= cols <= 10
    S, o = 28, 6
    body = "".join(item(o + c * S + S / 2.0, o + i * S + S / 2.0, 9.5) for i in range(rows) for c in range(cols))
    svg = svg_wrap(cols * S + 2 * o, rows * S + 2 * o, body, "array of %d rows of %d dots" % (rows, cols))
    assert n_items(svg) == rows * cols
    return svg


def lesson_array_svg(rows, cols):
    """Array with each row's count written on the right."""
    S, R, x0, y0 = 34, 11, 10, 10
    el = [item(x0 + c * S + S / 2.0, y0 + i * S + S / 2.0, R) for i in range(rows) for c in range(cols)]
    for i in range(rows):
        el.append(text(x0 + cols * S + 20, y0 + i * S + S / 2 + 6, str(cols), 17, col=RED))
    svg = svg_wrap(x0 + cols * S + 36, y0 + rows * S + 10, "".join(el),
                   "array of %d rows of %d dots, with each row counted" % (rows, cols))
    assert n_items(svg) == rows * cols
    return svg


def counters_svg(n, kind="dot"):
    """n things in rows of 10 (small gap after 5), not yet shared or grouped."""
    S, M = 24, 5
    top = 6 if kind == "apple" else 0
    el = []
    for i in range(n):
        rr, cc = divmod(i, 10)
        el.append(item(M + cc * S + (8 if cc >= 5 else 0) + S / 2.0, M + top + rr * (S + top) + S / 2.0, 8.5, kind))
    cols = min(n, 10)
    rows = (n + 9) // 10
    svg = svg_wrap(M * 2 + cols * S + (8 if cols > 5 else 0), M * 2 + rows * (S + top), "".join(el),
                   "%d %s in rows of 10" % (n, noun(kind, n)))
    assert n_items(svg) == n
    return svg


def groups_body(sizes, x0, y0, style, per_row=5, kind="dot"):
    """Rings (groups) or plates (sharing). Each box fits the largest group: up to 3 in a line, then 2 rows."""
    S, r, G, P = 24, 8.5, 10, 6
    top = 6 if kind == "apple" else 0
    m = max(sizes)
    ri, ci = (1, max(m, 1)) if m <= 3 else (2, (m + 1) // 2)
    bw, bh = ci * S + 2 * P, ri * (S + top) + 2 * P
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
            el.append(item(bx + P + cc * S + S / 2.0, by + P + top + rr * (S + top) + S / 2.0, r, kind))
    nrow = (len(sizes) + per_row - 1) // per_row
    ncol = min(len(sizes), per_row)
    return "".join(el), ncol * bw + (ncol - 1) * G, nrow * bh + (nrow - 1) * G


def groups_svg(sizes, style="ring", kind="dot", label=None):
    M = 5
    m = max(sizes)
    bw = (max(m, 1) if m <= 3 else (m + 1) // 2) * 24 + 12
    cap = max(1, (520 + 10) // (bw + 10))
    rows = -(-len(sizes) // cap)
    per_row = -(-len(sizes) // rows)
    body, w, h = groups_body(sizes, M, M, style, per_row, kind)
    if label is None:
        what = "plates" if style == "plate" else "groups"
        if len(set(sizes)) == 1:
            label = "%d %s of %d %s" % (len(sizes), what, sizes[0], noun(kind, 2))
        else:
            label = "%d %s with %s %s" % (len(sizes), what, ", ".join(map(str, sizes)), noun(kind, 2))
    svg = svg_wrap(w + 2 * M, h + 2 * M, body, label)
    assert n_items(svg) == sum(sizes)
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
    svg = svg_wrap(4 * PW, H, "".join(el), "four pictures labelled A to D")
    assert n_items(svg) == sum(sum(p) for p in panels)
    return svg


def jumps_svg(step, n):
    """Number line from 0 to step × n with n equal jumps from 0. Labels on every jump."""
    end = step * n
    L, R = 16, 444
    sc = (R - L) / float(end)
    yl = 64
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 8, yl, R + 8, yl, INK)]
    for v in range(0, end + 1):
        x = L + v * sc
        big = v % step == 0
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (x, yl - (8 if big else 4), x, yl + (8 if big else 4), INK, 2 if big else 1))
        if big:
            s.append(text(x, yl + 26, str(v), 15))
    for k in range(n):
        a, b = L + k * step * sc, L + (k + 1) * step * sc
        mid = (a + b) / 2
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (a, yl - 4, mid, yl - 46, b, yl - 4, RED))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>"
                 % (b, yl - 3, b - 9, yl - 10, b - 1, yl - 14, RED))
    svg = svg_wrap(R + 16, yl + 34, "".join(s), "number line with %d jumps of %d from 0 to %d" % (n, step, end))
    assert svg.count("<path ") == n
    return svg


# ------------------------------------------------------------ set 1: equal groups
def set_groups():
    its = []
    # A: how many altogether?
    for g, k, kind in [(3, 4, "dot"), (2, 5, "apple"), (4, 5, "dot"), (5, 3, "apple"), (2, 6, "dot"), (4, 2, "apple")]:
        n = g * k
        e = ("There are %d groups. Each group has %d. Count: %s. So %d groups of %d make <b>%d</b>."
             % (g, k, skip(k, g), g, k, n))
        its.append(mcq(fig(groups_svg([k] * g, "ring", kind)) + "How many %s are there altogether?" % noun(kind, 2),
                       n, [g + k, k, g, (g + 1) * k], e))
    # B: describe the picture (groups vs items in each group)
    for g, k in [(4, 3), (2, 6), (5, 4), (3, 5)]:
        right = "%d groups of %d" % (g, k)
        wrong = ["%d groups of %d" % (k, g), "%d groups of %d" % (g, k + 1), "%d groups of %d" % (g + 1, k)]
        e = ("Count the rings: %d groups. Count one ring: %d in each. So it is <b>%s</b>. "
             "%d groups of %d mixes up the groups and the number in each group." % (g, k, right, k, g))
        its.append(mcq(fig(groups_svg([k] * g)) + "What does the picture show?", right, wrong, e))
    # C: how many groups / how many in each group?
    for g, k, ask in [(3, 6, "groups"), (5, 2, "each"), (2, 7, "each")]:
        if ask == "groups":
            q, a, wrong = "How many <b>groups</b> are there?", g, [k, g * k, g + k]
            e = "Count the rings: there are <b>%d</b> groups. %d is the number in each group." % (g, k)
        else:
            q, a, wrong = "How many counters are in <b>each group</b>?", k, [g, g * k, g + k]
            e = "Look at one ring. It has <b>%d</b> counters. %d is the number of groups." % (k, g)
        its.append(mcq(fig(groups_svg([k] * g)) + q, a, wrong, e))
    # D: equal or not?
    its.append(mcq(fig(groups_svg([4, 4, 3])) + "Are these equal groups?",
                   "No. One group has 3.",
                   ["Yes. 3 groups of 4.", "Yes. All have 3.", "No. There are 4 groups."],
                   "Equal groups have the same number in each group. Two groups have 4, but one has 3. "
                   "So the groups are <b>not equal</b>."))
    its.append(mcq(fig(groups_svg([5, 5, 5], "ring", "apple")) + "Are these equal groups?",
                   "Yes. 3 groups of 5.",
                   ["No. 5 groups of 3.", "No. They are different.", "Yes. 3 groups of 3."],
                   "Every group has 5 apples, so the groups are equal. There are 3 groups. It is <b>3 groups of 5</b>."))
    # E: in words, with a picture
    its.append(mcq(fig(groups_svg([5] * 4)) +
                   "Siti has 4 bags. Each bag has 5 sweets. How many sweets does she have?", 20,
                   [9, 5, 4, 25],
                   "4 groups of 5: 5, 10, 15, 20. She has <b>20</b> sweets. 9 comes from 4 + 5. 5 is only one bag."))
    its.append(mcq(fig(groups_svg([2] * 5, "plate")) +
                   "There are 5 plates. Each plate has 2 curry puffs. How many curry puffs are there?", 10,
                   [7, 2, 5],
                   "5 groups of 2: 2, 4, 6, 8, 10. There are <b>10</b> curry puffs. 7 comes from 5 + 2."))
    its.append(mcq(fig(groups_svg([6] * 3)) +
                   "Ali has 3 boxes. Each box has 6 crayons. How many crayons does he have?", 18,
                   [9, 6, 3],
                   "3 groups of 6: 6 + 6 + 6 = <b>18</b>. 9 comes from 3 + 6. 6 is only one box."))
    # F: pick the picture
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("3 groups of 4 means 3 groups with 4 in each group. <b>{L}</b> shows this. "
                      "4 groups of 3 mixes up the groups and the number in each group. "
                      "The other pictures have the wrong number of groups or groups that are not equal."),
                "_abcd": ("Which picture shows <b>3 groups of 4</b>?",
                          [4, 4, 4], [[3, 3, 3, 3], [4, 4], [4, 4, 3]], "ring")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("2 groups of 5 means 2 groups with 5 in each group. <b>{L}</b> shows this. "
                      "5 groups of 2 mixes up the groups and the number in each group. "
                      "3 groups of 5 has one group too many. 5 and 4 are not equal groups."),
                "_abcd": ("Which picture shows <b>2 groups of 5</b>?",
                          [5, 5], [[2, 2, 2, 2, 2], [5, 5, 5], [5, 4]], "ring")})
    assert len(its) == 20, len(its)
    return {"title": "Equal groups", "items": its}


# ------------------------------------------------------------ set 2: repeated addition and ×
def set_repeated():
    its = []
    # A: picture -> repeated addition
    for g, k, kind in [(3, 5, "dot"), (4, 2, "apple"), (2, 7, "dot"), (5, 4, "dot"), (4, 6, "apple")]:
        right = rep(k, g)
        wrong = ["%d + %d" % (g, k), rep(k, g - 1), rep(k, g + 1)]
        e = ("There are %d groups of %d. Add %d, %d times: <b>%s</b> = %d."
             % (g, k, k, g, right, g * k))
        its.append(mcq(fig(groups_svg([k] * g, "ring", kind)) + "Which addition matches the picture?", right, wrong, e))
    # B: repeated addition -> ×
    for n, k in [(4, 3), (5, 2), (10, 3), (2, 5), (6, 4)]:
        right = "%d × %d" % (k, n)
        wrong = ["%d × %d" % (n, n), "%d + %d" % (k, n), "%d × %d" % (k - 1, n)]
        e = ("Count the %ds: there are %d of them. So it is %d groups of %d: <b>%s</b> = %d. "
             "Do not count the + signs." % (n, k, k, n, right, k * n))
        its.append(mcq(fig(groups_svg([n] * k)) + "Which is the same as <b>%s</b>?" % rep(n, k), right, wrong, e))
    # C: number line jumps
    for k, n in [(5, 4), (2, 6), (3, 5), (10, 3)]:
        right = "%d × %d = %d" % (n, k, n * k)
        wrong = ["%d + %d = %d" % (n, k, n + k), "%d × %d = %d" % (n - 1, k, (n - 1) * k),
                 "%d × %d = %d" % (n + 1, k, (n + 1) * k)]
        e = ("Count the arrows: %d jumps of %d. %s. So <b>%s</b>."
             % (n, k, skip(k, n), right))
        its.append(mcq(fig(jumps_svg(k, n)) + "Which number sentence matches the jumps?", right, wrong, e))
    # D: find the product with a picture
    for a, b in [(2, 8), (4, 5), (3, 10), (5, 7)]:
        e = "%d × %d means %d groups of %d: %s = <b>%d</b>." % (a, b, a, b, rep(b, a), a * b)
        its.append(mcq(fig(groups_svg([b] * a)) + "What is <b>%d × %d</b>?" % (a, b), a * b,
                       [a + b, (a + 1) * b, (a - 1) * b, b], e))
    # E: common mistakes
    its.append(mcq(fig(groups_svg([4, 4, 4])) + "Raju says 3 × 4 = 7. What did he do?", "He added 3 and 4.",
                   ["He counted the groups.", "He is right.", "He took away 4."],
                   "3 + 4 = 7. But 3 × 4 means 3 groups of 4: 4 + 4 + 4 = <b>12</b>. Raju <b>added</b> the two numbers."))
    its.append(mcq("Mei Ling writes <b>6 + 6 + 6 + 6 + 6 = 30</b>. Which multiplication is the same?", "5 × 6 = 30",
                   ["6 × 6 = 36", "4 × 6 = 24", "5 + 6 = 11"],
                   "There are five 6s. That is 5 groups of 6: <b>5 × 6 = 30</b>. 4 × 6 counts the + signs, not the 6s."))
    assert len(its) == 20, len(its)
    return {"title": "Repeated addition and ×", "items": its}


# ------------------------------------------------------------ set 3: arrays
def set_arrays():
    its = []
    # A: how many dots?
    for r, c in [(2, 4), (3, 5), (4, 4), (2, 9), (5, 6)]:
        e = "There are %d rows of %d. Count: %s. So %d × %d = <b>%d</b>." % (r, c, skip(c, r), r, c, r * c)
        its.append(mcq(fig(array_svg(r, c)) + "How many dots are there?", r * c, [r + c, (r + 1) * c, c, r * (c - 1)], e))
    # B: which number sentence?
    for r, c in [(2, 6), (3, 7), (4, 5), (5, 8)]:
        right = "%d × %d = %d" % (r, c, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c + 1, r * (c + 1)),
                 "%d × %d = %d" % (r + 1, c, (r + 1) * c)]
        e = ("Count the rows: %d. Count one row: %d. %d rows of %d is <b>%s</b>. "
             "%d + %d only adds the two numbers." % (r, c, r, c, right, r, c))
        its.append(mcq(fig(array_svg(r, c)) + "Which number sentence matches the dots?", right, wrong, e))
    # C: how many rows / in each row?
    for r, c, ask in [(3, 6, "rows"), (4, 7, "rows"), (2, 8, "each")]:
        if ask == "rows":
            q, a, wrong = "How many <b>rows</b> are there?", r, [c, r * c, r + c]
            e = "Rows go across. Count down the side: <b>%d</b> rows. %d is the number of dots in each row." % (r, c)
        else:
            q, a, wrong = "How many dots are in <b>each row</b>?", c, [r, r * c, r + c]
            e = "Look along one row: <b>%d</b> dots. %d is the number of rows." % (c, r)
        its.append(mcq(fig(array_svg(r, c)) + q, a, wrong, e))
    # D: turnaround facts
    for a, b in [(4, 7), (2, 9), (5, 3), (3, 10)]:
        right = "%d × %d" % (b, a)
        wrong = ["%d × %d" % (a, b + 1), "%d + %d" % (b, a), "%d × %d" % (b, b)]
        e = ("Turn the dots around. %d rows of %d become %d rows of %d. The number of dots stays the same. "
             "So %d × %d = %d × %d = %d. The answer is <b>%s</b>." % (a, b, b, a, a, b, b, a, a * b, right))
        its.append(mcq(fig(array_svg(a, b)) + "Which has the <b>same answer</b> as %d × %d?" % (a, b), right, wrong, e))
    # E: turn the array
    for r, c in [(3, 5), (2, 7)]:
        right = "%d × %d = %d" % (c, r, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, r, r * r), "%d × %d = %d" % (c, c, c * c)]
        e = ("Turn the dots around. %d rows of %d become %d rows of %d. "
             "The number of dots does not change, so <b>%s</b>." % (r, c, c, r, right))
        its.append(mcq(fig(array_svg(r, c)) + "This shows %d × %d = %d. Which also matches it?" % (r, c, r * c),
                       right, wrong, e))
    # F: missing number with the turnaround fact
    for a, b in [(4, 6), (5, 8)]:
        e = ("The order can change. The answer stays the same. %d × %d = %d × %d. "
             "The missing number is <b>%d</b>. Both make %d." % (a, b, b, a, a, a * b))
        its.append(mcq(fig(array_svg(a, b)) + "What is the missing number?  <b>%d × %d = %d × ☐</b>" % (a, b, b),
                       a, [b, a * b, a + b], e))
    assert len(its) == 20, len(its)
    return {"title": "Arrays", "items": its}


# ------------------------------------------------------------ set 4: sharing equally
def set_share():
    its = []
    # A: share counters on plates
    for n, k, kind in [(12, 3, "dot"), (10, 2, "apple"), (15, 5, "dot"), (20, 4, "dot"), (8, 2, "apple"), (18, 3, "dot")]:
        a = n // k
        e = ("Give them out one at a time until none are left. Each of the %d plates gets <b>%d</b>. "
             "Check: %d groups of %d make %d." % (k, a, k, a, n))
        its.append(mcq(fig(counters_svg(n, kind)) +
                       "Share these %d %s equally on %d plates. How many go on each plate?" % (n, noun(kind, n), k),
                       a, [k, n - k, a + 1, a - 1], e))
    # B: plates already shared
    its.append(mcq(fig(groups_svg([7, 7], "plate")) + "14 counters are shared equally. How many are on each plate?", 7,
                   [2, 14, 12],
                   "There are 2 plates. Each plate has <b>7</b>. 7 + 7 = 14. 2 is the number of plates."))
    its.append(mcq(fig(groups_svg([3] * 5, "plate")) + "15 counters are shared equally. How many plates are there?", 5,
                   [3, 15, 10],
                   "Count the plates: <b>5</b>. Each plate has 3. 3 + 3 + 3 + 3 + 3 = 15."))
    its.append(mcq(fig(groups_svg([4] * 4, "plate", "apple")) +
                   "These apples are shared equally on 4 plates. How many apples are there altogether?", 16,
                   [4, 8, 12],
                   "4 plates of 4: 4, 8, 12, 16. There are <b>16</b> apples. 4 is only one plate."))
    # C: fair or not?
    its.append(mcq(fig(groups_svg([4, 3, 5], "plate")) + "Is this an equal share?",
                   "No. The plates are different.",
                   ["Yes. Each plate has 4.", "Yes. There are 3 plates.", "No. There are 4 plates."],
                   "An equal share has the same number on every plate. The plates have 4, 3 and 5. "
                   "So it is <b>not</b> an equal share. Moving 1 from the plate of 5 to the plate of 3 makes it equal."))
    its.append(mcq(fig(groups_svg([6, 6, 6], "plate")) + "Is this an equal share?",
                   "Yes. Each plate has 6.",
                   ["No. The plates are different.", "Yes. Each plate has 3.", "No. One plate has 5."],
                   "Every plate has 6. So it is an <b>equal share</b>: 18 shared equally on 3 plates is 6 each."))
    # D: pick the sharing picture
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing on 3 plates means 3 plates with the same number. <b>{L}</b> has 3 plates of 5. "
                      "5 plates of 3 has the wrong number of plates. 6, 5 and 4 are not equal. 3 plates of 4 is only 12."),
                "_abcd": ("Share 15 counters equally on 3 plates. Which picture shows this?",
                          [5, 5, 5], [[3, 3, 3, 3, 3], [6, 5, 4], [4, 4, 4]], "plate")})
    its.append({"q": "", "c": ["A", "B", "C", "D"], "a": 0,
                "e": ("Sharing 16 between 2 plates means 2 plates with the same number. <b>{L}</b> has 8 and 8. "
                      "9 and 7 are not equal. 7 and 7 is only 14. 4 plates of 4 has the wrong number of plates."),
                "_abcd": ("Share 16 counters equally between 2 plates. Which picture shows this?",
                          [8, 8], [[9, 7], [7, 7], [4, 4, 4, 4]], "plate")})
    # E: sharing in words
    words = [
        ("Mrs Lim shares 10 pencils equally among 5 pupils. How many pencils does each pupil get?", 10, 5, [5, 15, 50]),
        ("Hui Min and her friend share 14 stickers equally. How many stickers does each of them get?", 14, 2, [2, 12, 16]),
        ("Mdm Wong puts 20 mandarin oranges equally into 4 bags. How many go in each bag?", 20, 4, [4, 16, 24]),
        ("Mr Rahman shares 12 rambutans equally among 3 children. How many rambutans does each child get?", 12, 3, [3, 9, 15]),
    ]
    for q, n, k, wrong in words:
        a = n // k
        e = "Share %d equally into %d groups. %d groups of %d make %d, so each gets <b>%d</b>." % (n, k, k, a, n, a)
        its.append(mcq(fig(counters_svg(n)) + q, a, wrong, e))
    # F: think of equal groups
    for g, total in [(3, 15), (2, 18), (4, 12)]:
        a = total // g
        e = "Count one plate: %d. Check: %d groups of %d make %d. So each plate has <b>%d</b>." % (a, g, a, total, a)
        its.append(mcq(fig(groups_svg([a] * g, "plate")) + "%d counters are shared equally on %d plates. How many are on each plate?"
                       % (total, g), a, [g, total - g, total + g], e))
    assert len(its) == 20, len(its)
    return {"title": "Sharing equally", "items": its}


# ------------------------------------------------------------ set 5: grouping and word problems
def set_story():
    its = []
    # A: grouping picture, count the groups
    for n, k in [(20, 5), (12, 2), (18, 3), (16, 4)]:
        g = n // k
        e = "There are %d in each group. Count the rings: <b>%d</b> groups. Check: %s." % (k, g, skip(k, g))
        its.append(mcq(fig(groups_svg([k] * g)) + "%d counters are put in groups of %d. How many groups are there?"
                       % (n, k), g, [k, n - k, g + 1, n], e))
    # B: make the groups yourself
    for n, k, wrong in [(10, 2, [2, 8, 12]), (20, 10, [10, 18, 30])]:
        g = n // k
        e = "Circle %d at a time: %s. That is <b>%d</b> groups." % (k, skip(k, g), g)
        its.append(mcq(fig(counters_svg(n)) + "Put these %d counters into groups of %d. How many groups can you make?"
                       % (n, k), g, wrong, e))
    # C: sharing or grouping?
    its.append(mcq("Which one is <b>grouping</b>?", "Put 12 eggs in boxes of 6.",
                   ["Share 12 eggs between 2 boxes.", "Add 6 eggs to 12 eggs.", "Eat 6 of the 12 eggs."],
                   "Grouping means you know how many go in each group. “Boxes of 6” tells you there are 6 in each box. "
                   "12 eggs make 2 boxes of 6."))
    its.append(mcq("Which one is <b>sharing</b>?", "Share 10 sweets among 5 children.",
                   ["Put 10 sweets in bags of 5.", "Buy 5 more sweets.", "Give away 5 of 10 sweets."],
                   "Sharing means you know how many groups. “Among 5 children” tells you there are 5 groups. "
                   "Each child gets 2 sweets."))
    # D: multiplication word problems (products within 40)
    mult = [
        ("In the canteen, 5 pupils sit at each table. There are 4 tables. How many pupils are there?", 4, 5, "dot", "plate"),
        ("A packet has 2 curry puffs. Mrs Ng buys 6 packets. How many curry puffs does she buy?", 6, 2, "dot", "ring"),
        ("There are 7 bicycles at the void deck. Each bicycle has 2 wheels. How many wheels are there?", 7, 2, "dot", "ring"),
        ("Xin Yi puts 3 stickers on each page. She fills 8 pages. How many stickers does she use?", 8, 3, "dot", "ring"),
        ("A box has 10 crayons. Priya has 4 boxes. How many crayons does she have?", 4, 10, "dot", "ring"),
        ("Zhi Hao has 5 boxes of mooncakes. Each box has 4 mooncakes. How many mooncakes are there?", 5, 4, "dot", "ring"),
        ("Each bowl has 3 apples. There are 5 bowls. How many apples are there?", 5, 3, "apple", "plate"),
    ]
    for q, g, k, kind, style in mult:
        n = g * k
        assert n <= 40
        e = ("%d groups of %d: %s. So %d × %d = <b>%d</b>. Adding %d + %d = %d is a mistake."
             % (g, k, skip(k, g), g, k, n, g, k, g + k))
        its.append(mcq(fig(groups_svg([k] * g, style, kind)) + q, n, [g + k, k, (g + 1) * k, (g - 1) * k], e))
    its.append(mcq(fig(groups_svg([5] * 3, "ring", "dot", "3 red packets with $5 in each")) +
                   "Wei Ming gets 3 red packets. Each red packet has $5. How much money does he get?", "$15",
                   ["$8", "$5", "$20"],
                   "3 groups of $5: $5, $10, $15. He gets <b>$15</b>. $8 comes from adding 3 + 5."))
    # E: division word problems (totals within 20)
    div = [
        ("Mr Tan puts 20 pupils into groups of 4. How many groups are there?", 20, 4, [4, 16, 24],
         "Make groups of 4: 4, 8, 12, 16, 20. That is <b>5</b> groups. 16 comes from 20 − 4."),
        ("Hafiz has 15 marbles. He puts 5 marbles in each bag. How many bags does he need?", 15, 5, [5, 10, 20],
         "Make groups of 5: 5, 10, 15. He needs <b>3</b> bags. 5 is the number in each bag."),
        ("On Sports Day, 18 pupils make 3 equal teams. How many pupils are in each team?", 18, 3, [3, 15, 21],
         "Share 18 equally into 3 teams. 3 groups of 6 make 18, so each team has <b>6</b> pupils. 3 is the number of teams."),
        ("A pencil costs $2. Ethan has $10. How many pencils can he buy?", 10, 2, [2, 8, 12],
         "Each pencil uses $2. Count in 2s: $2, $4, $6, $8, $10. He can buy <b>5</b> pencils."),
    ]
    for q, n, k, wrong, e in div:
        a = n // k
        assert n <= 20 and a * k == n and ("<b>%d</b>" % a) in e
        svg = counters_svg(n)
        if "$" in q:
            svg = svg.replace("aria-label='%d counters in rows of 10'" % n,
                              "aria-label='%d dollars as %d counters in rows of 10'" % (n, n))
        its.append(mcq(fig(svg) + q, a, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Grouping and word problems", "items": its}


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
        "<p>Equal groups have the same number in each group. "
        "First count the groups. Then count one group.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "ring", "apple") +
        "<figcaption>3 groups of 4 apples: 4 + 4 + 4 = 12.</figcaption></figure>"
        "<h2>Repeated addition and ×</h2>"
        "<p>We add the same number again and again. We can write it with the <b>×</b> sign. "
        "3 groups of 4 is 3 × 4. We say “3 times 4”.</p>" +
        ex("Write it with ×", "What is 5 + 5 + 5 + 5?", "There are four 5s. 4 groups of 5 is 4 × 5. "
           "Count: 5, 10, 15, 20.", "4 × 5 = 20") +
        "<figure class='sn-fig'>" + jumps_svg(5, 4) +
        "<figcaption>4 jumps of 5: 5, 10, 15, 20. So 4 × 5 = 20.</figcaption></figure>"
        "<h2>Arrays</h2>"
        "<p>An <b>array</b> puts things in rows. Each row has the same number.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(3, 5) +
        "<figcaption>3 rows of 5: 3 × 5 = 15.</figcaption></figure>"
        "<p>Turn it around and you get 5 rows of 3. It is still 15. So 3 × 5 = 5 × 3.</p>"
        "<h2>Sharing equally</h2>"
        "<p>Give out the things one at a time until none are left. Every plate gets the same number.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "plate", "dot", "12 counters shared on 3 plates") +
        "<figcaption>12 shared equally on 3 plates: 4 on each plate.</figcaption></figure>"
        "<h2>Grouping</h2>"
        "<p>Put the things in groups of the same size. Then count the groups.</p>" +
        ex("Grouping", "Put 12 counters in groups of 3. How many groups?", "Count in 3s: 3, 6, 9, 12. "
           "That is 4 groups.", "4 groups") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do"], [
            ["Adding the two numbers (3 × 4 = 7)", "3 × 4 is 3 groups of 4: 4 + 4 + 4 = 12"],
            ["Mixing up groups and the number in each group", "3 groups of 4 is 3 rings with 4 in each ring"],
            ["Giving one group, not the total (3 groups of 4 = 4)", "Count all of them: 12"],
            ["Groups that are not equal (4, 4 and 3)", "Every group must have the same number"],
            ["Counting the + signs (5 + 5 + 5 = 2 × 5)", "Count the 5s: 3 × 5 = 15"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division is taught in Primary 1?",
     "a": "In P1, children learn what multiplication and division mean, using pictures and objects. "
          "They multiply within 40 with equal groups, repeated addition and arrays, and divide within 20 by sharing equally and by grouping."},
    {"q": "Does my P1 child need to memorise multiplication tables?",
     "a": "Not yet. The multiplication tables of 2, 3, 4, 5 and 10 come in Primary 2, so in P1 it is enough to count equal groups and add the same number again and again."},
    {"q": "What is the most common mistake in P1 multiplication?",
     "a": "The most common mistake is adding the two numbers, such as 3 × 4 = 7. "
          "Ask your child to draw 3 groups of 4 and count them: 4 + 4 + 4 = 12."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics syllabus puts multiplication and division in Primary 1: "
          "the ideas of equal groups and sharing, the × sign, multiplying within 40 and dividing within 20."},
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
    """Check every number sentence in the choices: the right one is true, a wrong × one is false."""
    ops = {"×": lambda a, b: a * b, "+": lambda a, b: a + b, "−": lambda a, b: a - b}
    for s in sets:
        for it in s["items"]:
            r = it["c"][it["a"]]
            for c in it["c"]:
                m = re.fullmatch(r"(\d+) ([×+−]) (\d+) = (\d+)", c)
                if not m:
                    continue
                a, op, b, v = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
                ok = ops[op](a, b) == v
                assert ok, ("false sentence in choices", c)
            # a correct × answer must stay within 40 (P1)
            for m in re.finditer(r"(\d+) × (\d+)", r):
                assert int(m.group(1)) * int(m.group(2)) <= 40, r
            assert "÷" not in it["q"] + "".join(it["c"]) + it["e"]


def gen():
    rnd = random.Random(61806)
    sets = [set_groups(), set_repeated(), set_arrays(), set_share(), set_story()]
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
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "multiplication-and-division", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Multiplication and Division",
        "seo_title": "P1 Multiplication and Division Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Multiplication and division",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Multiplication and Division",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Concepts of multiplication and division; use of ×; multiplying within 40; dividing within 20",
        "meta_desc": "Free P1 maths worksheets on multiplication and division: equal groups, repeated addition, "
                     "arrays, sharing and grouping. 100 questions with answers.",
        "key_big": "Equal groups have the same number in each group. Count the groups, then count one group.",
        "key_sub": "3 groups of 4 is 4 + 4 + 4 = 12, so 3 × 4 = 12 (not 3 + 4 = 7).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160
    return u


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
    mark_large(u, "(array of \\d+ rows of ([6-9]|10) |\\d+ (counters|apples|dollars)|[4-9] (groups|plates)|"
                  "\\d+ red packets|four pictures|number line)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
