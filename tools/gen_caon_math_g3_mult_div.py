# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Multiplication and division (Ontario Mathematics Curriculum 2020, B2.6 and B2.1)
Equal groups and arrays, repeated addition and the commutative property, division as sharing and grouping,
multiplication and division as inverse operations (fact families), word problems.
Facts up to 10 × 10 and 100 ÷ 10.
  python3 tools/gen_ca_math_g3_mult_div.py
HTML attributes use single quotes (no backslashes in the JSON). Every drawn picture is counted in code.
Canadian style: Canadian English, $ and ¢, numbers under 1000 (no separators needed).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
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


def family_svg(a, b):
    """Fact family triangle: the product on top, the two factors at the bottom corners."""
    n = a * b
    W, H = 200, 150
    s = ["<polygon points='100,8 14,140 186,140' fill='%s' stroke='%s' stroke-width='2.5'/>" % (FILL2, GREEN),
         text(100, 56, n, 22, col=RED), text(52, 128, a, 22), text(148, 128, b, 22),
         text(100, 128, "×, ÷", 16, col=GREEN)]
    return svg_wrap(W, H, "".join(s), "fact triangle with %d at the top and %d and %d at the bottom" % (n, a, b))


# ------------------------------------------------------------ set 1: equal groups and arrays
def set_groups():
    its = []
    # A: equal groups picture, how many altogether?
    for g, k in [(3, 4), (2, 5), (4, 5), (5, 3), (2, 6)]:
        n = g * k
        e = ("There are %d groups. Each group has %d counters. Count by %ds: %s. So %d × %d = <b>%d</b>."
             % (g, k, k, skip(k, g), g, k, n))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "How many counters are there altogether?",
                       n, [g + k, g, k, (g + 1) * k], e))
    # B: which multiplication matches the array?
    for r, c in [(2, 6), (3, 7), (4, 5), (5, 8), (3, 9)]:
        right = "%d × %d = %d" % (r, c, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c + 1, r * (c + 1)),
                 "%d × %d = %d" % (r + 1, c, (r + 1) * c)]
        e = ("Count the rows: %d. Count one row: %d. %d rows of %d is <b>%s</b>. "
             "%d + %d only adds the two numbers. It does not count the dots."
             % (r, c, r, c, right, r, c))
        its.append(mcq(fig(array_svg(r, c)) + "Which number sentence matches this array?", right, wrong, e))
    # C: how many dots in the array?
    for r, c in [(5, 5), (4, 7), (2, 9), (3, 10), (5, 6)]:
        e = ("There are %d rows of %d. Count by %ds: %s. So %d × %d = <b>%d</b>."
             % (r, c, c, skip(c, r), r, c, r * c))
        its.append(mcq(fig(array_svg(r, c)) + "How many dots are in this array?",
                       r * c, [r + c, (r + 1) * c, (r - 1) * c, c], e))
    # D: which number sentence matches the groups?
    for g, k, wrong in [(3, 6, ["3 + 6 = 9", "6 + 6 = 12", "3 × 7 = 21"]),
                        (4, 5, ["4 + 5 = 9", "5 + 5 + 5 = 15", "4 × 6 = 24"]),
                        (5, 3, ["5 + 3 = 8", "3 + 3 + 3 + 3 = 12", "5 × 4 = 20"])]:
        right = "%d × %d = %d" % (g, k, g * k)
        e = ("There are %d groups of %d: %s = %d. That is <b>%s</b>. Make sure you count every group."
             % (g, k, rep(k, g), g * k, right))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "Which number sentence matches the picture?", right, wrong, e))
    # E: pick the picture
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
    return {"title": "Equal groups and arrays", "items": its}


# ------------------------------------------------------------ set 2: repeated addition and the commutative property
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
    for r, c in [(4, 9), (3, 8), (5, 6), (6, 4)]:
        right = rep(c, r)
        wrong = ["%d + %d" % (r, c), rep(c, r - 1), rep(c, r + 1)]
        e = ("%d × %d means %d groups of %d. Add %d %ds: <b>%s</b> = %d."
             % (r, c, r, c, r, c, right, r * c))
        its.append(mcq("Which addition is the same as <b>%d × %d</b>?" % (r, c), right, wrong, e))
    # C: commutative property
    for a, b in [(4, 7), (2, 9), (6, 5), (3, 10), (8, 6), (9, 4)]:
        right = "%d × %d" % (b, a)
        wrong = ["%d × %d" % (a, b + 1), "%d + %d" % (b, a), "%d × %d" % (b, b)]
        e = ("You can multiply in any order and get the same answer. %d × %d = %d and %d × %d = %d. "
             "So <b>%s</b> has the same answer." % (a, b, a * b, b, a, a * b, right))
        its.append(mcq("Which has the <b>same answer</b> as %d × %d?" % (a, b), right, wrong, e))
    # D: missing number with the turnaround fact
    for a, b in [(6, 9), (5, 8), (7, 3)]:
        e = ("The order of the numbers can change. The answer stays the same. "
             "%d × %d = %d × %d, so the missing number is <b>%d</b>. Both are %d."
             % (a, b, b, a, a, a * b))
        its.append(mcq("What number goes in the box?  <b>%d × %d = %d × ☐</b>" % (a, b, b), a,
                       [b, a * b, a + b], e))
    # E: turn the array
    for r, c in [(3, 5), (4, 6)]:
        right = "%d × %d = %d" % (c, r, r * c)
        wrong = ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, r, r * r), "%d × %d = %d" % (c, c, c * c)]
        e = ("Turn the array a quarter turn. %d rows of %d become %d rows of %d. "
             "The number of dots does not change, so <b>%s</b>." % (r, c, c, r, right))
        its.append(mcq(fig(array_svg(r, c)) + "This array shows %d × %d = %d. Which other number sentence also matches it?"
                       % (r, c, r * c), right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Repeated addition and turnaround facts", "items": its}


# ------------------------------------------------------------ set 3: sharing and grouping
def set_divide():
    its = []
    # A: share counters
    for n, k in [(12, 3), (20, 4), (15, 5), (18, 2), (24, 6)]:
        a = n // k
        e = ("Sharing: give the counters out one at a time until none are left. "
             "Each of the %d plates gets <b>%d</b>. %d ÷ %d = %d." % (k, a, n, k, a))
        its.append(mcq(fig(counters_svg(n)) + "Share these %d counters equally on %d plates. How many go on each plate?"
                       % (n, k), a, [k, n - k, a + 1, a - 1], e))
    # B: grouping picture, count the groups
    for n, k in [(20, 5), (24, 4), (18, 3), (30, 10)]:
        g = n // k
        e = ("Grouping: you know there are %d in each group. Count the rings: %d groups. So %d ÷ %d = <b>%d</b>."
             % (k, g, n, k, g))
        its.append(mcq(fig(groups_svg([k] * g, "ring")) + "%d counters are put in groups of %d. How many groups are there?"
                       % (n, k), g, [k, n - k, g + 1, n], e))
    # C: which division matches the sharing picture?
    for n, k in [(28, 4), (21, 3), (16, 2)]:
        a = n // k
        right = "%d ÷ %d = %d" % (n, k, a)
        wrong = ["%d ÷ %d = %d" % (k, n, a), "%d − %d = %d" % (n, k, n - k), "%d ÷ %d = %d" % (n, k, a + 1)]
        e = ("%d counters are shared on %d plates. Each plate has %d. That is <b>%s</b>. "
             "Always start with the total, %d. %d ÷ %d is the wrong way around."
             % (n, k, a, right, n, k, n))
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
    # F: division facts
    for n, k in [(42, 6), (56, 8), (63, 9), (100, 10), (36, 4)]:
        a = n // k
        e = ("Think multiplication: %d × ☐ = %d. %d × %d = %d, so %d ÷ %d = <b>%d</b>."
             % (k, n, k, a, n, n, k, a))
        its.append(mcq("What is %d ÷ %d?  <i>Think: %d × ☐ = %d.</i>" % (n, k, k, n), a,
                       [a + 1, a - 1, n - k, k], e))
    assert len(its) == 20, len(its)
    return {"title": "Division as sharing and grouping", "items": its}


# ------------------------------------------------------------ set 4: multiplication and division are inverses
def set_inverse():
    its = []
    # A: division fact that goes with a multiplication fact
    for a, b in [(6, 7), (4, 9), (8, 5), (7, 8), (9, 6)]:
        n = a * b
        right = "%d ÷ %d = %d" % (n, b, a)
        wrong = ["%d ÷ %d = %d" % (b, n, a), "%d − %d = %d" % (n, b, n - b), "%d ÷ %d = %d" % (n, b, a + 1)]
        e = ("Division undoes multiplication. %d groups of %d make %d, so %d split into groups of %d makes %d groups: "
             "<b>%s</b>. Start with the biggest number, %d." % (a, b, n, n, b, a, right, n))
        its.append(mcq("Which division fact goes with <b>%d × %d = %d</b>?" % (a, b, n), right, wrong, e))
    # B: which is NOT in the fact family?
    for a, b in [(3, 8), (5, 6), (4, 7), (9, 10)]:
        n = a * b
        right = "%d ÷ %d = %d" % (a, n, b)
        wrong = ["%d ÷ %d = %d" % (n, a, b), "%d × %d = %d" % (b, a, n), "%d ÷ %d = %d" % (n, b, a)]
        q = fig(family_svg(a, b)) + "Which is <b>not</b> in the fact family for %d, %d and %d?" % (a, b, n)
        e = ("The fact family is %d × %d = %d, %d × %d = %d, %d ÷ %d = %d and %d ÷ %d = %d. "
             "<b>%s</b> is wrong: in these facts the biggest number, %d, comes first when you divide."
             % (a, b, n, b, a, n, n, a, b, n, b, a, right, n))
        its.append(mcq(q, right, wrong, e))
    # C: missing numbers
    for q_, d in [(7, 4), (9, 5)]:
        n = q_ * d
        e = "Use multiplication to undo the division: ☐ = %d × %d = <b>%d</b>. Check: %d ÷ %d = %d." % (q_, d, n, n, d, q_)
        its.append(mcq("What number goes in the box?  <b>☐ ÷ %d = %d</b>" % (d, q_), n, [q_ + d, q_ - d, q_, n + d], e))
    for d, q_ in [(6, 8), (9, 7)]:
        n = d * q_
        e = "How many groups of %d make %d? Use division: %d ÷ %d = <b>%d</b>. Check: %d × %d = %d." % (d, n, n, d, q_, d, q_, n)
        its.append(mcq("What number goes in the box?  <b>%d × ☐ = %d</b>" % (d, n), q_, [n - d, n + d, q_ + 1], e))
    for n, q_ in [(32, 8), (54, 9)]:
        d = n // q_
        e = "%d split into how many groups makes %d in each? %d × %d = %d, so ☐ = <b>%d</b>. Check: %d ÷ %d = %d." % (
            n, q_, d, q_, n, d, n, d, q_)
        its.append(mcq("What number goes in the box?  <b>%d ÷ ☐ = %d</b>" % (n, q_), d, [q_, n - q_, d + 1], e))
    # D: use multiplication to divide or check
    for n, d in [(45, 5), (72, 8), (30, 3)]:
        right = "%d × ☐ = %d" % (d, n)
        wrong = ["%d × %d = ☐" % (n, d), "%d + ☐ = %d" % (d, n), "%d × ☐ = %d" % (n, d)]
        e = ("To find %d ÷ %d, ask: %d times what makes %d? That is <b>%s</b>. ☐ = %d."
             % (n, d, d, n, right, n // d))
        its.append(mcq("Which multiplication helps you find <b>%d ÷ %d</b>?" % (n, d), right, wrong, e))
    its.append(mcq("Liam says 56 ÷ 7 = 9. Use multiplication to check. Is he right?",
                   "No. 7 × 8 = 56, so 56 ÷ 7 = 8.",
                   ["Yes. 7 × 9 = 56.", "No. 56 ÷ 7 = 7.", "Yes. 56 − 7 = 49."],
                   "Check: 7 × 9 = 63, not 56. 7 × 8 = 56, so <b>56 ÷ 7 = 8</b>. Liam is not right."))
    its.append(mcq("Hana says 48 ÷ 6 = 8. Use multiplication to check. Is she right?",
                   "Yes. 6 × 8 = 48.",
                   ["No. 48 ÷ 6 = 7.", "No. 48 ÷ 6 = 9.", "No. 48 − 6 = 42."],
                   "Check: 6 × 8 = 48. The multiplication matches, so <b>Hana is right</b>: 48 ÷ 6 = 8."))
    assert len(its) == 20, len(its)
    return {"title": "Multiplication and division fact families", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story():
    its = []
    mult = [
        ("The class sets up chairs in the gym. There are 6 rows. Each row has 8 chairs. How many chairs are there?", 6, 8),
        ("A pack of hockey cards has 8 cards. Owen buys 4 packs. How many cards does he get?", 4, 8),
        ("At camp, 7 canoes go out on the lake. Each canoe holds 3 people. How many people can the canoes hold?", 7, 3),
        ("Emma skates 4 laps around the rink each day. How many laps does she skate in 7 days?", 7, 4),
        ("Each ringette team has 6 players on the ice. 4 teams line up on the ice for a photo. How many players is that?", 4, 6),
        ("Canada geese fly in groups. There are 10 geese in each group. How many geese are in 7 groups?", 7, 10),
        ("At lunch, 8 students sit at each table. There are 9 full tables. How many students are at the tables?", 9, 8),
    ]
    for q, g, k in mult:
        n = g * k
        e = ("There are %d equal groups of %d, so multiply: %d × %d = <b>%d</b>. "
             "Adding %d + %d = %d only joins the two numbers." % (g, k, g, k, n, g, k, g + k))
        its.append(mcq(q, n, [g + k, (g - 1) * k, (g + 1) * k, k], e))
    its.append(mcq("Zoe has 9 toonies. A toonie is worth $2. How much money does she have?", "$18",
                   ["$11", "$9", "$20"],
                   "9 toonies is 9 groups of $2: 9 × $2 = <b>$18</b>. $11 comes from adding 9 + 2."))
    div = [
        ("Arjun shares 36 hockey cards equally among 4 friends. How many cards does each friend get?", 9,
         [4, 32, 40, 8], "Sharing among 4 friends: 36 ÷ 4. 4 × 9 = 36, so each friend gets <b>9</b> cards."),
        ("In gym class, 30 students make teams of 5. How many teams are there?", 6,
         [5, 25, 35, 7], "Grouping in 5s: 30 ÷ 5. 5 × 6 = 30, so there are <b>6</b> teams."),
        ("There are 56 chairs in the gym. They are in 7 equal rows. How many chairs are in each row?", 8,
         [7, 49, 63, 9], "56 chairs in 7 equal rows: 56 ÷ 7. 7 × 8 = 56, so each row has <b>8</b> chairs."),
        ("A farm packs 24 small bottles of maple syrup in boxes of 6. How many boxes does it fill?", 4,
         [6, 18, 30, 5], "Grouping in 6s: 24 ÷ 6. 6 × 4 = 24, so it fills <b>4</b> boxes."),
        ("32 students go on a field trip. Each parent driver takes 4 students. How many cars are needed?", 8,
         [4, 28, 36, 128], "Groups of 4: 32 ÷ 4. 4 × 8 = 32, so <b>8</b> cars are needed."),
        ("Ethan has 45¢ in nickels. A nickel is 5¢. How many nickels does he have?", 9,
         [5, 40, 50, 8], "How many 5s make 45? 45 ÷ 5. 5 × 9 = 45, so he has <b>9</b> nickels."),
        ("Priya reads 10 pages each day. How many days does it take her to read 90 pages?", 9,
         [10, 80, 100, 8], "How many 10s make 90? 90 ÷ 10 = <b>9</b> days. Check: 9 × 10 = 90."),
        ("Leah has 63 stickers. She puts 9 stickers on each page. How many pages does she fill?", 7,
         [9, 54, 72, 6], "Groups of 9: 63 ÷ 9. 9 × 7 = 63, so she fills <b>7</b> pages."),
    ]
    for q, a, wrong, e in div:
        its.append(mcq(q, a, wrong, e))
    its.append(mcq("Noah buys 3 hot chocolates at the rink. Each one costs $2. He pays with a $10 bill. How much change does he get?",
                   "$4", ["$6", "$7", "$16"],
                   "Step 1: cost: 3 × $2 = $6. Step 2: change: $10 − $6 = <b>$4</b>. ($6 is the cost, not the change.)"))
    its.append(mcq("Amira has 4 packs of hockey cards. Each pack has 5 cards. She gives 6 cards to her brother. How many cards does she have left?",
                   "14", ["20", "26", "3"],
                   "Step 1: 4 × 5 = 20 cards. Step 2: 20 − 6 = <b>14</b> cards left. (3 comes from 4 + 5 − 6.)"))
    its.append(mcq("Kai has 3 bags of marbles with 8 marbles in each bag. He shares all the marbles equally among 4 friends. How many marbles does each friend get?",
                   "6", ["24", "2", "8"],
                   "Step 1: 3 × 8 = 24 marbles. Step 2: 24 ÷ 4 = <b>6</b>, because 4 × 6 = 24. (24 is only step 1.)"))
    its.append(mcq("For the Terry Fox Run, the gym teacher puts 40 students into 5 equal lines. Then each line splits into 2 equal teams. How many students are on each team?",
                   "4", ["8", "20", "16"],
                   "Step 1: 40 ÷ 5 = 8 students in each line. Step 2: 8 ÷ 2 = <b>4</b> students on each team. "
                   "(8 is only step 1. 16 comes from 8 × 2.)"))
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
        "<h2>Equal groups and arrays</h2>"
        "<p><b>Multiplication</b> counts equal groups. 3 groups of 4 is 3 × 4. "
        "An <b>array</b> puts the groups in equal rows. Count the rows. Then count one row.</p>"
        "<figure class='sn-fig'>" + lesson_array_svg(3, 4) +
        "<figcaption>3 rows of 4: 4 + 4 + 4 = 12, so 3 × 4 = 12.</figcaption></figure>"
        "<p>Multiplication is a fast way to do <b>repeated addition</b>. 4 + 4 + 4 is the same as 3 × 4.</p>"
        "<h2>Turnaround facts</h2>"
        "<p>You can multiply in any order. The answer stays the same. Turn the array a quarter turn: "
        "3 rows of 4 become 4 rows of 3. Both have 12 dots, so 3 × 4 = 4 × 3. "
        "If you know one fact, you know two.</p>" +
        ex("Turnaround fact", "You know 6 × 9 = 54. What is 9 × 6?", "Same numbers, other order. The answer does not change.", "54") +
        "<h2>Division: sharing and grouping</h2>"
        "<p><b>Sharing:</b> you know how many groups. Give the items out one at a time. "
        "12 shared on 3 plates is 4 on each plate.</p>"
        "<figure class='sn-fig'>" + groups_svg([4, 4, 4], "plate", "12 counters shared on 3 plates") +
        "<figcaption>Sharing: 12 ÷ 3 = 4 on each plate.</figcaption></figure>"
        "<p><b>Grouping:</b> you know how many in each group. 12 in groups of 3 makes 4 groups. "
        "Both are 12 ÷ 3 = 4. Always start with the total.</p>"
        "<h2>Fact families</h2>"
        "<p>Division undoes multiplication. 3, 8 and 24 make a <b>fact family</b> of four facts.</p>"
        "<figure class='sn-fig'>" + family_svg(3, 8) +
        "<figcaption>3 × 8 = 24, 8 × 3 = 24, 24 ÷ 3 = 8, 24 ÷ 8 = 3.</figcaption></figure>" +
        ex("Divide with a times fact", "What is 42 ÷ 6?", "Think: 6 × ☐ = 42. 6 × 7 = 42.", "7") +
        "<p>Use multiplication to check a division. If 56 ÷ 7 = 8, then 7 × 8 must be 56. It is, so the answer is right.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding instead of multiplying (3 × 4 = 7)", "3 × 4 means 3 groups of 4: 4 + 4 + 4 = 12"],
            ["Giving the number of groups, not the total (3 groups of 4 = 3)", "Count all the items: 3 × 4 = 12"],
            ["Mixing up groups and items (3 groups of 4 drawn as 4 groups of 3)", "The first number is the number of groups"],
            ["Dividing the wrong way (4 ÷ 20 = 5)", "Start with the total: 20 ÷ 4 = 5"],
            ["Mixing up sharing and grouping", "“Among 4” means 4 groups. “Groups of 4” means 4 in each group"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division do Grade 3 students learn in Ontario?",
     "a": "The Ontario math curriculum asks Grade 3 students to show multiplication up to 10 × 10 and division up to 100 ÷ 10 with tools, drawings and arrays. They also learn that division undoes multiplication and that you can multiply in any order."},
    {"q": "What is the difference between sharing and grouping in division?",
     "a": "In sharing you know the number of groups and find how many go in each, like 12 shared on 3 plates. In grouping you know how many go in each group and find the number of groups, like 12 in groups of 3. Both give 12 ÷ 3 = 4."},
    {"q": "Why do Grade 3 students use arrays for multiplication?",
     "a": "An array shows equal rows, so students can see that 3 rows of 4 is 4 + 4 + 4 = 12. Turning the array also shows that 3 × 4 = 4 × 3, and splitting it into rows shows division."},
    {"q": "Is multiplication and division on the Grade 3 EQAO math test?",
     "a": "Yes. The Grade 3 EQAO math assessment is based on the Ontario curriculum, which includes multiplication and division with equal groups and arrays. Mixed word problems like the ones on this page are good practice."},
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


def gen():
    rnd = random.Random(33804)
    sets = [set_groups(), set_repeated(), set_divide(), set_inverse(), set_story()]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "multiplication-and-division", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication and Division",
        "seo_title": "Grade 3 Multiplication and Division Worksheets: Arrays, Equal Groups, Sharing and Grouping (Free, Ontario)",
        "short_title": "Multiplication and division",
        "domain": "Number",
        "standard_code": "Grade 3: B2.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent multiplication of numbers up to 10 × 10 and division up to 100 ÷ 10, using a variety of tools and drawings, including arrays",
        "meta_desc": "Free Grade 3 math worksheets on multiplication and division for the Ontario curriculum: equal groups and arrays, repeated addition, turnaround facts, sharing and grouping, fact families and word problems. 100 questions with an answer key, great for EQAO practice.",
        "key_big": "Multiplication counts equal groups. Division splits a total into equal groups.",
        "key_sub": "3 × 4 means 3 groups of 4: 4 + 4 + 4 = 12. You can multiply in any order: 3 × 4 = 4 × 3. Division undoes multiplication: 12 ÷ 3 = 4 because 3 × 4 = 12.",
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
    mark_large(u, "(array of \\d+ rows of ([6-9]|10) |\\d+ counters|\\d+ groups of|\\d+ plates of|four pictures)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
